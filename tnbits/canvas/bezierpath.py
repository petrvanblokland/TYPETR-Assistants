# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    bezierpath.py
#

import math
import AppKit
import CoreText
import Quartz

from fontTools.pens.basePen import BasePen
from tnbits.canvas.beziercontour import CanvasBezierContour
_FALLBACKFONT = "LucidaGrande"
import tnbits.canvas.opentype

# TODO: only import what's necessary.
#from AppKit import NSMoveToBezierPathElement, NSLineToBezierPathElement, \
#    NSCurveToBezierPathElement, NSBezierPath

class CanvasBezierPath(BasePen):
    """Wraps a Cocoa Bézier path object. Taken from DrawBot."""

    _instructionSegmentTypeMap = {
        AppKit.NSMoveToBezierPathElement: "move",
        AppKit.NSLineToBezierPathElement: "line",
        AppKit.NSCurveToBezierPathElement: "curve"
    }

    def __init__(self, path=None, glyphSet=None):
        """"""
        if path is None:
            self._path = AppKit.NSBezierPath.bezierPath()
        else:
            self._path = path
        BasePen.__init__(self, glyphSet)

    def __repr__(self):
        return "<BezierPath>"

    # pen support

    def _moveTo(self, pt):
        """Move to a point `x`, `y`."""
        self._path.moveToPoint_(pt)

    def _lineTo(self, pt):
        """Line to a point `x`, `y`."""
        self._path.lineToPoint_(pt)

    def _curveToOne(self, pt1, pt2, pt3):
        """Curve to a point `x3`, `y3`.
        With given bezier handles `x1`, `y1` and `x2`, `y2`.
        """
        self._path.curveToPoint_controlPoint1_controlPoint2_(pt3, pt1, pt2)

    def closePath(self):
        """Close the path."""
        self._path.closePath()

    def beginPath(self):
        """Begin path."""
        from fontTools.ufoLib.pointPen import PointToSegmentPen
        self._pointToSegmentPen = PointToSegmentPen(self)
        self._pointToSegmentPen.beginPath()

    def addPoint(self, *args, **kwargs):
        """
        Add a point to the path.
        """
        self._pointToSegmentPen.addPoint(*args, **kwargs)

    def endPath(self):
        """End the path.
        * When the bezier path is used as a pen, the path will be open.
        * When the bezier path is used as a point pen, the path will process all
        the points added with `addPoints`.
        """
        if hasattr(self, "_pointToSegmentPen"):
            # its been uses in a point pen world
            self._pointToSegmentPen.endPath()
            del self._pointToSegmentPen

    def drawToPen(self, pen):
        """Draw the bezier path into a pen."""
        contours = self.contours
        for contour in contours:
            contour.drawToPen(pen)

    def drawToPointPen(self, pointPen):
        """Draw the bezier path into a point pen."""
        contours = self.contours

        for contour in contours:
            contour.drawToPointPen(pointPen)

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        """Arc with `center` and a given `radius`, from `startAngle` to
        `endAngle`, going clockwise if `clockwise` is True and counter
        clockwise if `clockwise` is False."""
        self._path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
            center, radius, startAngle, endAngle, clockwise)

    def arcTo(self, pt1, pt2, radius):
        """
        Arc from one point to an other point with a given `radius`.
        """
        self._path.appendBezierPathWithArcFromPoint_toPoint_radius_(pt1, pt2, radius)

    def rect(self, x, y, w, h):
        """
        Add a rectangle at possition `x`, `y` with a size of `w`, `h`
        """
        self._path.appendBezierPathWithRect_(((x, y), (w, h)))

    def oval(self, x, y, w, h):
        """
        Add a oval at possition `x`, `y` with a size of `w`, `h`
        """
        self._path.appendBezierPathWithOvalInRect_(((x, y), (w, h)))
        self.closePath()

    def text(self, txt, font=_FALLBACKFONT, fontSize=10, offset=None, box=None):
        """Draws a `txt` with a `font` and `fontSize` at an `offset` in the bezier path.
        If a font path is given the font will be installed and used directly.

        Optionally `txt` can be a `FormattedString` and be drawn inside a
        `box`, a tuple of (x, y, width, height).
        """
        if isinstance(txt, FormattedString):
            attributedString = txt.getNSObject()
        else:
            try:
                txt = txt.decode("utf-8")
            except UnicodeEncodeError:
                pass
            fontName = _tryInstallFontFromFontName(font)
            font = AppKit.NSFont.fontWithName_size_(fontName, fontSize)
            if font is None:
                #warnings.warn("font: %s is not installed, back to the fallback font: %s" % (fontName, _FALLBACKFONT))
                font = AppKit.NSFont.fontWithName_size_(_FALLBACKFONT, fontSize)

            attributes = {
                AppKit.NSFontAttributeName: font
            }
            attributedString = AppKit.NSAttributedString.alloc().initWithString_attributes_(txt, attributes)
        w, h = attributedString.size()
        setter = CoreText.CTFramesetterCreateWithAttributedString(attributedString)
        path = Quartz.CGPathCreateMutable()
        if offset:
            x, y = offset
        else:
            x = y = 0
        if box:
            bx, by, w, h = box
            x += bx
            y += by
            Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(0, 0, w, h))
        else:
            Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(0, -h, w*2, h*2))
        box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CoreText.CTFrameGetLines(box)
        origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)

        if origins and box is not None:
            x -= origins[-1][0]
            y -= origins[-1][1]
        for i, (originX, originY) in enumerate(origins):
            ctLine = ctLines[i]
            ctRuns = CoreText.CTLineGetGlyphRuns(ctLine)
            for ctRun in ctRuns:
                attributes = CoreText.CTRunGetAttributes(ctRun)
                font = attributes.get(AppKit.NSFontAttributeName)
                baselineShift = attributes.get(AppKit.NSBaselineOffsetAttributeName, 0)
                glyphCount = CoreText.CTRunGetGlyphCount(ctRun)
                for i in range(glyphCount):
                    glyph = CoreText.CTRunGetGlyphs(ctRun, (i, 1), None)[0]
                    ax, ay = CoreText.CTRunGetPositions(ctRun, (i, 1), None)[0]
                    if glyph:
                        self._path.moveToPoint_((x+originX+ax, y+originY+ay+baselineShift))
                        self._path.appendBezierPathWithGlyph_inFont_(glyph, font)
        self.optimizePath()

    def traceImage(self, path, threshold=.2, blur=None, invert=False, turd=2,
            tolerance=0.2, offset=None):
        """Convert a given image to a vector outline.

        Optionally some tracing options can be provide:

        * `threshold`: the threshold used to bitmap an image
        * `blur`: the image can be blurred
        * `invert`: invert to the image
        * `turd`: the size of small turd that can be ignored
        * `tolerance`: the precision tolerance of the vector outline
        * `offset`: add the traced vector outline with an offset to the BezierPath
        """
        from tools import traceImage
        traceImage.TraceImage(path, self, threshold, blur, invert, turd, tolerance, offset)

    def getNSBezierPath(self):
        """
        Return the nsBezierPath.
        """
        return self._path

    def _getCGPath(self):
        path = Quartz.CGPathCreateMutable()
        count = self._path.elementCount()
        for i in range(count):
            instruction, points = self._path.elementAtIndex_associatedPoints_(i)
            if instruction == AppKit.NSMoveToBezierPathElement:
                Quartz.CGPathMoveToPoint(path, None, points[0].x, points[0].y)
            elif instruction == AppKit.NSLineToBezierPathElement:
                Quartz.CGPathAddLineToPoint(path, None, points[0].x, points[0].y)
            elif instruction == AppKit.NSCurveToBezierPathElement:
                Quartz.CGPathAddCurveToPoint(
                    path, None,
                    points[0].x, points[0].y,
                    points[1].x, points[1].y,
                    points[2].x, points[2].y
                )
            elif instruction == AppKit.NSClosePathBezierPathElement:
                Quartz.CGPathCloseSubpath(path)
        # hacking to get a proper close path at the end of the path
        x, y, _, _ = self.bounds()
        Quartz.CGPathMoveToPoint(path, None, x, y)
        Quartz.CGPathAddLineToPoint(path, None, x, y)
        Quartz.CGPathAddLineToPoint(path, None, x, y)
        Quartz.CGPathAddLineToPoint(path, None, x, y)
        Quartz.CGPathCloseSubpath(path)
        return path

    def setNSBezierPath(self, path):
        """
        Set a nsBezierPath.
        """
        self._path = path

    def pointInside(self, p):
        """
        Check if a point `x`, `y` is inside a path.
        """
        return self._path.containsPoint_(p)

    def bounds(self):
        """
        Return the bounding box of the path.
        """
        if self._path.isEmpty():
            return None
        (x, y), (w, h) = self._path.bounds()
        return x, y, x+w, y+h

    def controlPointBounds(self):
        """
        Return the bounding box of the path including the offcurve points.
        """
        (x, y), (w, h) = self._path.controlPointBounds()
        return x, y, x+w, y+h

    def optimizePath(self):
        count = self._path.elementCount()
        if self._path.elementAtIndex_(count-1) == AppKit.NSMoveToBezierPathElement:
            optimizedPath = AppKit.NSBezierPath.bezierPath()
            for i in range(count-1):
                instruction, points = self._path.elementAtIndex_associatedPoints_(i)
                if instruction == AppKit.NSMoveToBezierPathElement:
                    optimizedPath.moveToPoint_(*points)
                elif instruction == AppKit.NSLineToBezierPathElement:
                    optimizedPath.lineToPoint_(*points)
                elif instruction == AppKit.NSCurveToBezierPathElement:
                    p1, p2, p3 = points
                    optimizedPath.curveToPoint_controlPoint1_controlPoint2_(p3, p1, p2)
                elif instruction == AppKit.NSClosePathBezierPathElement:
                    optimizedPath.closePath()
            self._path = optimizedPath

    def copy(self):
        """
        Copy the bezier path.
        """
        new = self.__class__()
        new._path = self._path.copy()
        return new

    def reverse(self):
        """
        Reverse the path direction
        """
        self._path = self._path.bezierPathByReversingPath()

    def appendPath(self, otherPath):
        """
        Append a path.
        """
        self._path.appendBezierPath_(otherPath.getNSBezierPath())

    def __add__(self, otherPath):
        new = self.copy()
        new.appendPath(otherPath)
        return new

    def __iadd__(self, other):
        self.appendPath(other)
        return self

    # transformations

    def translate(self, x=0, y=0):
        """
        Translate the path with a given offset.
        """
        self.transform((1, 0, 0, 1, x, y))

    def rotate(self, angle):
        """
        Rotate the path around the origin point with a given angle in degrees.
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        self.transform((c, s, -s, c, 0, 0))

    def scale(self, x=1, y=None):
        """
        Scale the path with a given `x` (horizontal scale) and `y` (vertical scale).

        If only 1 argument is provided a proportional scale is applied.
        """
        if y is None:
            y = x
        self.transform((x, 0, 0, y, 0, 0))

    def skew(self, angle1, angle2=0):
        """
        Skew the path with given `angle1` and `angle2`.

        If only one argument is provided a proportional skew is applied.
        """
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)
        self.transform((1, math.tan(angle2), math.tan(angle1), 1, 0, 0))

    def transform(self, transformMatrix):
        """
        Transform a path with a transform matrix (xy, xx, yy, yx, x, y).
        """
        aT = AppKit.NSAffineTransform.transform()
        aT.setTransformStruct_(transformMatrix[:])
        self._path.transformUsingAffineTransform_(aT)

    # boolean operations

    def _contoursForBooleanOperations(self):
        # contours are very temporaly objects
        # redirect drawToPointPen to drawPoints
        contours = self.contours
        for contour in contours:
            contour.drawPoints = contour.drawToPointPen
        return contours

    def union(self, other):
        """
        Return the union between two bezier paths.
        """
        import booleanOperations
        contours = self._contoursForBooleanOperations() + other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.union(contours, result)
        return result

    def removeOverlap(self):
        """
        Remove all overlaps in a bezier path.
        """
        import booleanOperations
        contours = self._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.union(contours, result)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def difference(self, other):
        """
        Return the difference between two bezier paths.
        """
        import booleanOperations
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.difference(subjectContours, clipContours, result)
        return result

    def intersection(self, other):
        """
        Return the intersection between two bezier paths.
        """
        import booleanOperations
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.intersection(subjectContours, clipContours, result)
        return result

    def xor(self, other):
        """
        Return the xor between two bezier paths.
        """
        import booleanOperations
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.xor(subjectContours, clipContours, result)
        return result

    def __mod__(self, other):
        return self.difference(other)

    __rmod__ = __mod__

    def __imod__(self, other):
        result = self.difference(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def __or__(self, other):
        return self.union(other)

    __ror__ = __or__

    def __ior__(self, other):
        result = self.union(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def __and__(self, other):
        return self.intersection(other)

    __rand__ = __and__

    def __iand__(self, other):
        result = self.intersection(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def __xor__(self, other):
        return self.xor(other)

    __rxor__ = __xor__

    def __ixor__(self, other):
        result = self.xor(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def _points(self, onCurve=True, offCurve=True):
        points = []
        if not onCurve and not offCurve:
            return points
        for index in range(self._path.elementCount()):
            instruction, pts = self._path.elementAtIndex_associatedPoints_(index)
            if not onCurve:
                pts = pts[:-1]
            elif not offCurve:
                pts = pts[-1:]
            points.extend([(p.x, p.y) for p in pts])
        return points

    def _get_points(self):
        return self._points()

    points = property(_get_points, doc="Return a list of all points.")

    def _get_onCurvePoints(self):
        return self._points(offCurve=False)

    onCurvePoints = property(_get_onCurvePoints, doc="Return a list of all on curve points.")

    def _get_offCurvePoints(self):
        return self._points(onCurve=False)

    offCurvePoints = property(_get_offCurvePoints, doc="Return a list of all off curve points.")

    def _get_contours(self):
        contours = []
        for index in range(self._path.elementCount()):
            instruction, pts = self._path.elementAtIndex_associatedPoints_(index)

            if instruction == AppKit.NSMoveToBezierPathElement:
                contours.append(CanvasBezierContour())

            if instruction == AppKit.NSClosePathBezierPathElement:
                contours[-1].open = False

            if pts:
                contours[-1].append([(p.x, p.y) for p in pts])

        if len(contours) >= 2 and len(contours[-1]) == 1 and contours[-1][0] == contours[-2][0]:
            contours.pop()
        return contours

    contours = property(_get_contours, doc="Return a list of contours with all point coordinates sorted in segments. A contour object has an `open` attribute.")

    def __len__(self):
        return len(self.contours)

    def __getitem__(self, index):
        return self.contours[index]

    def __iter__(self):
        contours = self.contours
        count = len(contours)
        index = 0
        while index < count:
            contour = contours[index]
            yield contour
            index += 1

