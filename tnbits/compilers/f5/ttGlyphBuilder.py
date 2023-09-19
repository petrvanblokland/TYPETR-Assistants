from fontTools.pens.basePen import AbstractPen, BasePen
from fontTools.misc.bezierTools import calcQuadraticParameters, calcCubicParameters, solveCubic
from fontTools.misc import bezierTools
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates, GlyphComponent
from fontTools.ttLib.tables.ttProgram import Program


class TTGlyphBuilderPen(AbstractPen):

    # XXX compare with fontTools.pens.ttGlyphPen.TTGlyphPen

    """Pen object to facilitate building TrueType glyph objects. After drawing onto
    the pen, use the buildTTGlyph() method to get a FontTools Glyph object.

        >>> from fontTools.ttLib import TTFont
        >>> from tnTestFonts import getFontPath
        >>> font = TTFont(getFontPath("Arial Unicode.ttf"))
        >>> gs = font.getGlyphSet()
        >>> glyphName = "perthousand"
        >>> ttg = font["glyf"][glyphName]
        >>> pen = TTGlyphBuilderPen()
        >>> gs[glyphName].draw(pen)
        >>> pPoints, pEndPts, pFlags = pen.getOutline()
        >>> tPoints, tEndPts, tFlags = ttg.getCoordinates(font["glyf"])
        >>> assert pPoints == tPoints
        >>> assert pEndPts == tEndPts
        >>> assert pFlags == tFlags.tolist()
        >>> glyphName = "aring"
        >>> ttg2 = pen.buildTTGlyph()
        >>> tPoints2, tEndPts2, tFlags2 = ttg2.getCoordinates(font["glyf"])
        >>> assert tPoints == tPoints2
        >>> assert tEndPts == tEndPts2
        >>> assert tFlags.tolist() == tFlags2
        >>> ttg2.compact(font['glyf'])
        >>> ttg = font["glyf"][glyphName]
        >>> pen = TTGlyphBuilderPen()
        >>> gs[glyphName].draw(pen)
        >>> pen.getComponents()
        [('a', (1, 0, 0, 1, 0, 0)), ('ring', (1, 0, 0, 1, 228, 0))]
        >>> ttg2 = pen.buildTTGlyph()
        >>> ttg2.compact(font['glyf'])
    """

    def __init__(self):
        self.contours = []
        self.components = []

    def _checkComponentsVsOutlines(self):
        if self.components and self.contours:
            # XXX We should decompose selectively.
            raise ValueError("Can't mix outlines and components for TT.")

    def isComposite(self):
        self._checkComponentsVsOutlines()
        return bool(self.components)

    def getOutline(self, reverseContours=False):
        self._checkComponentsVsOutlines()
        points = []
        flags = []
        endPts = []
        for contour in self.contours:
            if len(contour) > 1 and contour[0] == contour[-1] and contour[0][1]:
                del contour[-1]
            if reverseContours:
                firstPt = contour[0]
                rest = contour[1:]
                rest.reverse()
                contour = [firstPt] + rest
            for pt, flag in contour:
                points.append(pt)
                flags.append(flag)
            endPts.append(len(points) - 1)

        return GlyphCoordinates(points), endPts, flags

    def getComponents(self):
        self._checkComponentsVsOutlines()
        return self.components

    def buildTTGlyph(self, reverseContours=False):
        ttg = Glyph()
        if self.isComposite():
            ttg.components = []
            ttg.numberOfContours = -1
            for baseGlyphName, transformation in self.components:
                component = GlyphComponent()
                component.glyphName = baseGlyphName
                x, y = transformation[4:]
                component.x = x
                component.y = y
                scalex, scale01, scale10, scaley = transformation[:4]
                component.transform = [[scalex, scale01], [scale10, scaley]]
                component.flags = 0  # (UN)SCALED_COMPONENT_OFFSET?
                ttg.components.append(component)
        else:
            points, endPtsOfContours, flags = self.getOutline(reverseContours)
            ttg.endPtsOfContours = endPtsOfContours
            ttg.coordinates = points
            ttg.flags = flags
            ttg.numberOfContours = len(endPtsOfContours)
            ttg.program = Program()
            ttg.program.fromBytecode([])
        return ttg

    def _newContour(self):
        self.contours.append([])

    def _addPoint(self, point, flag):
        x, y = point
        x = int(round(x))
        y = int(round(y))
        self.contours[-1].append(((x, y), flag))

    # Pen interface

    def moveTo(self, pt):
        self._newContour()
        self._addPoint(pt, True)

    def lineTo(self, pt):
        self._addPoint(pt, True)

    def curveTo(self, *pts):
        raise NotImplementedError("TTGlyphBuilderPen does not support cubic beziers. Use CubicToQuadFilterPen() to convert them.")

    def qCurveTo(self, *pts):
        offCurves = pts[:-1]
        lastPt = pts[-1]
        if lastPt is None:
            self._newContour()
        for pt in offCurves:
            self._addPoint(pt, False)
        if lastPt is not None:
            self._addPoint(lastPt, True)

    def addComponent(self, glyphName, transformation, **kwargs):
        assert len(transformation) == 6
        self.components.append((glyphName, transformation))


class CubicToQuadFilterPen(BasePen):

    """Pen that converts all its incoming curveTo() calls into qCurveTo() calls,
    converting cubic bezier segments into quadratic segments.
    """

    def __init__(self, otherPen, errorMargin=1.0, cubicToQuadConverter=None):
        self.otherPen = otherPen
        self.errorMargin = errorMargin
        if cubicToQuadConverter is None:
            cubicToQuadConverter = cubicToQuad
        self.cubicToQuadConverter = cubicToQuadConverter
        self._offCurvePoints = []  # for visualisation
        self._onCurvePoints = []   # for visualisation
        super(CubicToQuadFilterPen, self).__init__(None)

    def _moveTo(self, pt):
        self._onCurvePoints.append(pt)
        self.otherPen.moveTo(pt)

    def _lineTo(self, pt):
        self._onCurvePoints.append(pt)
        self.otherPen.lineTo(pt)

    def _curveToOne(self, pt2, pt3, pt4):
        pt1 = self._getCurrentPoint()
        points = self.cubicToQuadConverter(pt1, pt2, pt3, pt4, self.errorMargin)
        self.qCurveTo(*points[1:])

    def qCurveTo(self, *pts):
        self.otherPen.qCurveTo(*pts)
        self._offCurvePoints.extend(pts[:-1])
        # Ok, BasePen could offer a current point setter <grmbl @ self>
        self._BasePen__currentPoint = pts[-1]
        if pts[-1] is not None:
            self._onCurvePoints.append(pts[-1])

    def _closePath(self):
        self.otherPen.closePath()

    def _endPath(self):
        self.otherPen.endPath()

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


def cubicToQuad(pt1, pt2, pt3, pt4, errorMargin=1.0):
    """Convert the cubic bezier described by (pt1, pt2, pt3, pt4) to a
    quadratic bezier, using one or more off curve points. The return value
    is [pt1, offCurve1...offCurveN, pt4].
    """
    if not polygonIsConvex([pt1, pt2, pt3, pt4]):
        # Use the other algorithm, the primary one doesn't handle
        # inflexions well. (Inflexions are implied by the fact that
        # the cubic hull is concave.)
        return cubicToQuadAlgorithm2(pt1, pt2, pt3, pt4, errorMargin)
    else:
        return cubicToQuadAlgorithm1(pt1, pt2, pt3, pt4, errorMargin)


def glyphsToQuadratic(glyphs, errorMargin=1.0, reverseDirection=False):
    # Copied and adjusted from google's cu2u package, using their logic,
    # but our own conversion algorithm.
    """Convert the curves of a set of compatible of glyphs to quadratic.

    All curves will be converted to quadratic at once, ensuring interpolation
    compatibility. If this is not required, calling glyphs_to_quadratic with one
    glyph at a time may yield slightly more optimized results.

    Return True if glyphs were modified, else return False.

    Raises IncompatibleGlyphsError if glyphs have non-interpolatable outlines.
    """
    from cu2qu.ufo import _get_segments, _set_segments, zip, UnequalZipLengthsError, IncompatibleGlyphsError

    try:
        segments_by_location = zip(*[_get_segments(g) for g in glyphs])
    except UnequalZipLengthsError:
        raise IncompatibleGlyphsError(*glyphs)
    if not any(segments_by_location):
        return False

    # always modify input glyphs if reverseDirection is True
    glyphs_modified = reverseDirection

    new_segments_by_location = []
    for segments in segments_by_location:
        tag = segments[0][0]
        if not all(s[0] == tag for s in segments[1:]):
            raise IncompatibleGlyphsError(*glyphs)
        if tag == 'curve':
            segments = segmentsToQuad(segments, errorMargin=errorMargin)
            ##segments = _segments_to_quadratic(segments, max_err, None)
            glyphs_modified = True
        new_segments_by_location.append(segments)

    if glyphs_modified:
        new_segments_by_glyph = zip(*new_segments_by_location)
        for glyph, new_segments in zip(glyphs, new_segments_by_glyph):
            _set_segments(glyph, new_segments, reverseDirection)

    return glyphs_modified


def segmentsToQuad(cubicSegments, errorMargin):
    cubics = []
    for curveType, cubic in cubicSegments:
        assert curveType == "curve"
        assert len(cubic) == 4
        cubics.append(cubic)
    quads = cubicToQuadMultiple(cubics, errorMargin)
    quadSegments = []
    prevLen = None
    for quad in quads:
        quadSegments.append(("qcurve", quad))
    return quadSegments


def cubicToQuadMultiple(cubics, errorMargin=1.0):
    converter = cubicToQuadAlgorithm1
    for cubic in cubics:
        assert len(cubic) == 4, cubic
        if not polygonIsConvex(cubic):
            # if any of the segments is concave, use the concave-friendly algorithm
            converter = cubicToQuadAlgorithm2
            break
    firstQuads = []
    for cubic in cubics:
        quad = converter(*cubic, errorMargin=errorMargin)
        firstQuads.append(quad)
    assert len(cubics) == len(firstQuads)
    maxNumPoints = max(len(q) for q in firstQuads)
    quads = []
    for quad, cubic in zip(firstQuads, cubics):
        if len(quad) < maxNumPoints:
            quad = converter(*cubic, errorMargin=errorMargin, numOffCurves=maxNumPoints-2)
        assert len(quad) == maxNumPoints, (len(quad), maxNumPoints)
        quads.append(quad)
    assert len(cubics) == len(quads)
    return quads


def cubicToQuadAlgorithm1(pt1, pt2, pt3, pt4, errorMargin=1.0, numOffCurves=None):
    sqrErrorMargin = errorMargin * errorMargin
    maxSteps = 10
    initSteps = 1
    if numOffCurves is not None:
        assert numOffCurves >= 1
        initSteps = maxSteps = numOffCurves
    for steps in range(initSteps, maxSteps + 1):
        foundError = False
        testPoints = []
        offCurvePoints = []
        ts = [i/float(steps) for i in range(1, steps)]
        for c1, c2, c3, c4 in bezierTools.splitCubicAtT(pt1, pt2, pt3, pt4, *ts):
            offCurve = intersect(c1, c2, c3, c4)
            if offCurve is None:
                # curve may be a line, just use the middle between the handles
                offCurve = midPoint(c2, c3)
            offCurvePoints.append(offCurve)
            testPoint = pointOnCubic(c1, c2, c3, c4, 0.5)[0]
            testPoints.append(testPoint)

        onCurvePoints = []
        # calc implied points for error testing
        for i in range(len(offCurvePoints)-1):
            onCurvePoints.append(midPoint(offCurvePoints[i], offCurvePoints[i+1]))
        onCurvePoints.append(pt4)

        currentPoint = pt1
        for i in range(len(testPoints)):
            testPoint = testPoints[i]
            offCurve = offCurvePoints[i]
            onCurve = onCurvePoints[i]

            a, b, c = calcQuadraticParameters(currentPoint, offCurve, onCurve)
            roots = findClosestTsOnQuadParms(testPoint, a, b, c)
            if roots:
                t = roots[0]
                # Ignoring possible other roots. It should be very very rare there's more than
                # one, and if there is one, I assume we're very far beyond our errorMargin.
                qTestPoint = pointOnQuadParms(a, b, c, t)[0]
                dx = qTestPoint[0] - testPoint[0]
                dy = qTestPoint[1] - testPoint[1]
                if (dx*dx + dy*dy) > sqrErrorMargin:
                    foundError = True
                    break
            else:
                foundError = True
                break

            currentPoint = onCurve

        if not foundError:
            break

    assert len(offCurvePoints) == steps, (len(offCurvePoints), steps)
    return [pt1] + offCurvePoints + [pt4]


def cubicToQuadAlgorithm2(pt1, pt2, pt3, pt4, errorMargin=1.0, numOffCurves=None):
    # This version is less flexible (it will always add an even number of
    # off curve points) but it's more stable when the original curve has
    # inflexions.
    maxSteps = 5
    initSteps = 1
    if numOffCurves is not None:
        assert numOffCurves >= 1
        initSteps = maxSteps = numOffCurves // 2 # To make numOffCurves compatible with cubicToQuadAlgorithm1()
    sqrErrorMargin = errorMargin * errorMargin
    for steps in range(initSteps, maxSteps + 1):
        foundError = False
        errorsx = []
        errorsy = []
        offCurvePoints = []
        ts = [i/float(steps) for i in range(1, steps)]
        for c1, c2, c3, c4 in bezierTools.splitCubicAtT(pt1, pt2, pt3, pt4, *ts):
            offCurve1 = scaleHandle(c1, c2, 0.75)
            offCurve2 = scaleHandle(c4, c3, 0.75)
            offCurvePoints.append(offCurve1)
            offCurvePoints.append(offCurve2)
            implied = midPoint(offCurve1, offCurve2)
            qTestPoint1 = quadMid(c1, offCurve1, implied)
            qTestPoint2 = quadMid(implied, offCurve2, c4)
            testPoint1, testPoint2 = pointOnCubic(c1, c2, c3, c4, 0.25, 0.75)

            dx = qTestPoint1[0] - testPoint1[0]
            dy = qTestPoint1[1] - testPoint1[1]
            if (dx*dx + dy*dy) > sqrErrorMargin:
                foundError = True
                break
            dx = qTestPoint2[0] - testPoint2[0]
            dy = qTestPoint2[1] - testPoint2[1]
            if (dx*dx + dy*dy) > sqrErrorMargin:
                foundError = True
                break

        if not foundError:
            break

    return [pt1] + offCurvePoints + [pt4]


# Helper functions

def polygonIsConvex(points):
    """Return True if the polygon is convex."""
    # http://csharphelper.com/blog/2014/07/determine-whether-a-polygon-is-convex-in-c/
    #
    # For each set of three adjacent points A, B, C,
    # find the cross product AB x BC. If the sign of
    # all the cross products is the same, the angles
    # are all positive or negative (depending on the
    # order in which we visit them) so the polygon
    # is convex.
    gotNegative = False
    gotPositive = False
    numPoints = len(points)

    for i in range(len(points)):
        crossProduct = _crossProductLength(
                points[i-2],  # A
                points[i-1],  # B
                points[i]     # C
            )
        if crossProduct < 0:
            gotNegative = True
        elif crossProduct > 0:
            gotPositive = True
        if gotNegative and gotPositive:
            return False

    # If we got this far, the polygon is convex.
    return True


def _crossProductLength(A, B, C):
    """Return the cross product AB x BC."""
    # Helper for polygonIsConvex()
    #
    # The cross product is a vector perpendicular to AB
    # and BC having length |AB| * |BC| * Sin(theta) and
    # with direction given by the right-hand rule.
    # For two vectors in the X-Y plane, the result is a
    # vector with X and Y components 0 so the Z component
    # gives the vector's length and direction.
    Ax, Ay = A
    Bx, By = B
    Cx, Cy = C
    # Get the vectors' coordinates.
    BAx = Ax - Bx
    BAy = Ay - By
    BCx = Cx - Bx
    BCy = Cy - By
    # Calculate the Z coordinate of the cross product.
    return (BAx * BCy - BAy * BCx)


def findClosestTsOnQuadParms(P, a, b, c):
    Px, Py = P
    ax, ay = a
    bx, by = b
    cx, cy = c
    ad = 2*ax*ax + 2*ay*ay
    bd = 3*ax*bx + 3*ay*by
    cd = bx*bx + by*by + 2*ax*(cx-Px) + 2*ay*(cy-Py)
    dd = bx*(cx-Px) + by*(cy-Py)
    return [root for root in solveCubic(ad, bd, cd, dd) if 0 < root < 1]


def pointOnQuad(pt1, pt2, pt3, *ts):
    a, b, c = calcQuadraticParameters(pt1, pt2, pt3)
    return pointOnQuadParms(a, b, c, *ts)


def pointOnQuadParms(a, b, c, *ts):
    ax, ay = a
    bx, by = b
    cx, cy = c

    points = []
    for t in ts:
        x = ax * t*t + bx * t + cx
        y = ay * t*t + by * t + cy
        points.append((x, y))
    return points

def pointOnCubic(pt1, pt2, pt3, pt4, *ts):
    a, b, c, d = calcCubicParameters(pt1, pt2, pt3, pt4)
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    points = []
    for t in ts:
        x = ax * t*t*t + bx * t*t + cx * t + dx
        y = ay * t*t*t + by * t*t + cy * t + dy
        points.append((x, y))
    return points


def intersect(pt1, pt2, pt3, pt4):
    """Return the intersection point of pt1-pt2 and pt3-pt4
    Return None if there is no intersection.
    """
    b1x, b1y = pt1
    a1x, a1y = pt2[0] - b1x, pt2[1] - b1y
    b2x, b2y = pt3
    a2x, a2y = pt4[0] - b2x, pt4[1] - b2y
    determinant = (a2y*a1x - a2x*a1y)
    if abs(determinant) < 0.0001:
        intersection = None
    else:
        t = ((b2x - b1x)*a2y + (b1y - b2y)*a2x) / float(determinant)
        intersection = a1x * t + b1x, a1y * t + b1y
    return intersection


def scaleHandle(pt1, pt2, t):
    pt1x, pt1y = pt1
    pt2x, pt2y = pt2
    dx = pt2x - pt1x
    dy = pt2y - pt1y
    return pt1x + t * dx, pt1y + t * dy

def midPoint(pt1, pt2):
    pt1x, pt1y = pt1
    pt2x, pt2y = pt2
    return (pt1x + pt2x) * 0.5, (pt1y + pt2y) * 0.5

def cubicMid(pt1, pt2, pt3, pt4):
    m1 = midPoint(pt1, pt2)
    m2 = midPoint(pt2, pt3)
    m3 = midPoint(pt3, pt4)
    m4 = midPoint(m1, m2)
    m5 = midPoint(m2, m3)
    return midPoint(m4, m5)

def quadMid(pt1, pt2, pt3):
    m1 = midPoint(pt1, pt2)
    m2 = midPoint(pt2, pt3)
    return midPoint(m1, m2)


# XXX This doesn't belong here anymore, but it's still a useful bit of math.
def findInflexions(pt1, pt2, pt3, pt4):
    # http://www.caffeineowl.com/graphics/2d/vectorial/cubic-inflexion.html
    ax = pt2[0] - pt1[0]
    ay = pt2[1] - pt1[1]

    bx = pt3[0] - pt2[0] - ax
    by = pt3[1] - pt2[1] - ay

    cx = pt4[0] - pt3[0] - ax - 2*bx
    cy = pt4[1] - pt3[1] - ay - 2*by

    #(bx*cy - by*cx) * (t ** 2)  +  t*(ax*cy - ay*cx)  +  ax*by - ay*bx
    a = (bx*cy - by*cx)
    b = (ax*cy - ay*cx)
    c = ax*by - ay*bx
    roots = bezierTools.solveQuadratic(a, b, c)
    roots = [r for r in roots if 0 < r < 1]
    return roots


def _runDocTests():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    _runDocTests()

    # DrawBot test code

    class DrawBotPen(BasePen):

        # So we can draw quads

        def _moveTo(self, pt):
            moveTo(pt)

        def _lineTo(self, pt):
            lineTo(pt)

        def _curveToOne(self, pt1, pt2, pt3):
            curveTo(pt1, pt2, pt3)

        def _closePath(self):
            closePath()

    def dot(pt, r=4):
        d = r * 2
        x, y = pt
        oval(x-r, y-r, d, d)

    def drawCubic(pt1, pt2, pt3, pt4):
        fill(None)
        stroke(0.7)
        strokeWidth(1)
        newPath()
        # moveTo(pt1)
        # curveTo(pt2, pt3, pt4)

        moveTo(pt1)
        curveTo(pt2, pt3, pt4)

        drawPath()
        strokeWidth(0.25)
        line(pt1, pt2)
        line(pt3, pt4)
        fill(0.7)
        stroke(None)
        for pt in [pt1, pt2, pt3, pt4]:
            dot(pt)

    if False:
        pt1 = (96, 690)
        pt2 = (330, 716)
        pt3 = (449, 647)
        pt4 = (396, 437)

        drawCubic(pt1, pt2, pt3, pt4)

        points = cubicToQuad(pt1, pt2, pt3, pt4, 0.8)

        fill(0, 0, 1, 0.8)
        for pt in points[1:-1]:
            dot(pt)

        fill(None)
        stroke(1, 0, 0, 0.5)
        strokeWidth(1)

        newPath()
        pen = DrawBotPen(None)
        pen.moveTo(points[0])
        pen.qCurveTo(*points[1:])
        drawPath()

    if False:
        pen = CubicToQuadFilterPen(DrawBotPen(None), 1.8)

        newPath()
        pen.moveTo((150, 148))

        pen.curveTo((126, 516), (400, 800), (632, 596))

        fill(None)
        stroke(0.4)
        drawPath()

        fill(0, 0, 1)
        stroke(None)
        for pt in pen._offCurvePoints:
            dot(pt)
        # print(len(pen._offCurvePoints))

    if False:
        from fontTools.ttLib import TTFont
        from tnTestFonts import getFontPath
        from tnbits.compilers.f5.ttfTools import getBestCmap
        path = getFontPath("ProW6.otf")
        font = TTFont(path)
        glyphSet = font.getGlyphSet()
        dbPen = DrawBotPen(glyphSet)
        newPath()

        testGlyph = getBestCmap(font)[ord("a")]
        glyphSet[testGlyph].draw(dbPen)

        translate(120, 300)
        scale(0.8)
        fill(None)
        stroke(0.6)
        drawPath()

        stroke(1, 0, 0, 0.6)
        newPath()
        pen = CubicToQuadFilterPen(DrawBotPen(glyphSet), 1.0)
        glyphSet[testGlyph].draw(pen)
        drawPath()

        # print(pen._offCurvePoints)
        fill(0, 0.2, 1)
        stroke(None)
        for pt in pen._offCurvePoints:
            dot(pt)
        fill(0.75, 0, 0)
        for pt in pen._onCurvePoints:
            dot(pt)
