# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR glyphAnalyzer.py
#
import weakref
import math
import operator
import functools

SPANSTEP = 4 # Stepping around a point to see if it black or white
PARALLEL_TOLERANCE = 3 # Difference tolerance angle in degrees to take point contexts as parallel

def pointDistance(p1, p2):
    return distance(p1.x, p1.y, p1.y, p2.y)

def squareDistance(x1, y1, x2, y2):
    """Answers the square of the distance for relative comparison and to save the time of the math.sqrt."""
    tx, ty = x2 - x1, y2 - y1
    return tx * tx + ty * ty

def distance(x1, y1, x2, y2):
    """Answers the distance between the points."""
    return math.sqrt(squareDistance(x1, y1, x2, y2))

def dotProduct(v1, v2):
    return functools.reduce(operator.add, map(operator.mul, v1, v2))

def pointProjectedOnLine(x1, y1, x2, y2, px, py):
    """Answers the projected point `(px, py)` on line `((x1, y1), (x2, y2))`.
    Answers `(x1, y1)` if there is not distance between the two points of the line."""
    # Line vector.
    tx, ty = x2 - x1, y2 - y1
    v1 = tx, ty

    # Vector from line start to point.
    t1x, t1y = px - x1, py - y1
    v2 = t1x, t1y

    # Square length of line to normalize.
    dd = tx * tx + ty * ty

    if dd == 0:
        return x1, y1

    dot = dotProduct(v1, v2)
    return  x1 + (dot * tx) / dd, y1 + (dot * ty) / dd

def point2Line(x1, y1, x2, y2, px, py):
    """Answers the distance from point (px, py) to line ((x1, y1), (x2, y2))."""
    x, y = pointProjectedOnLine(x1, y1, x2, y2, px, py) # Calculate the projected point
    return distance(x, y, px, py) # Length of p1->p2        

class Point:
    """Constructed point, compatible with self.glyph.contours.points[0] point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))

class PointContext:
    def __init__(self, cIndex, pIndex, pp):
        self.cIndex = cIndex
        self.pIndex = pIndex
        self.pp = pp # (p_2, p_1, p, p1, p2)

    def __repr__(self):
        return f'PC(c={self.cIndex}, p={self.pIndex}, x={self.x}, y={self.y})'

    # self.angle    Answer angle of the point context
    def _get_angle(self):
        """Answer the angle of pointContext (p_1, p)"""
        xDiff = self.p_1.x - self.p.x
        yDiff = self.p_1.y - self.p.y
        return int(round(math.atan2(yDiff, xDiff) * 180 / math.pi, 3))
    angle = property(_get_angle)

    def _get_x(self):
        return self.p.x
    x = property(_get_x)

    def _get_y(self):
        return self.p.y
    y = property(_get_y)

    def _get_p_2(self):
        return self.pp[0]
    p_2 = property(_get_p_2)
    
    def _get_p_1(self):
        return self.pp[1]
    p_1 = property(_get_p_1)
    
    def _get_p(self):
        return self.pp[2]
    p = property(_get_p)
    
    def _get_p1(self):
        return self.pp[3]
    p1 = property(_get_p1)
    
    def _get_p2(self):
        return self.pp[4]
    p2 = property(_get_p2)
    
    def _get_index(self):
        return self.cIndex, self.pIndex
    index = property(_get_index)

    def _get_normalizedAngle(self):
        angle = self.angle
        while angle < 0:
            angle += 180
        while angle > 360:
            angle -= 180
        return angle
    normalizedAngle = property(_get_normalizedAngle)

    def _get_isDiagonal(self):
        """Answer the boolean flag if the point context (p-1, p) is different form 0 and 90"""
        return self.p_1.x != self.p.x and self.p_1.y != self.p.y
    isDiagonal = property(_get_isDiagonal)

    def inBoundingBox(self, p):
        return (self.p.x <= p.x <= self.p_1.x or self.p_1.x <= p.x <= self.p.x) and (self.p.y <= p.y <= self.p_1.y or self.p_1.y <= p.y <= self.p.y)

    def averageDistance(self, pc):
        (p00, p01), (p10, p11), (p20, p21), (p30, p31) = self.getProjectedWindowLines(pc)
        if None in (p00, p01, p10, p11, p20, p21, p30, p31):
            return None # Points not in projected window
        return ((pointDistance(p00, p01) + pointDistance(p10, p11) + pointDistance(p20, p21) + pointDistance(p30, p31)))/4

    def isParallel(self, pc, tolerance=None):
        """Answer if self is parallel to _pc_ point context. Optional attribute _tolerance_
        is the margin to interpret point context lines to be parallel. Default is PARALLEL_TOLERANCE."""
        if tolerance is None:
            tolerance = PARALLEL_TOLERANCE
        return abs(self.normalizedAngle - pc.normalizedAngle) <= tolerance

    def projectedOnLine(self, p):
        """Answer the point context _pc_ projects on the line of `self`."""
        x, y = pointProjectedOnLine(self.p_1.x, self.p_1.y, self.p.x, self.p.y, p.x, p.y)
        return Point(x, y)

    def getProjectedPoint(self, p):
        """Answer the perpendicular projection of point _p_ in the line segment of `self`.
        If the projection in not within the range of the line segment, then answer `None`.
        """
        pp = self.projectedOnLine(p)
        if self.inBoundingBox(pp): # Is the projected point in inside the line segment
            return pp
        return None # Projection not within the line segment window.

    def getProjectedWindowLines(self, pc):
        """Answer all 4 projected window lines. Note that some of them can be None
        is the projects falls outside the window (the overlapping area of a perpendicular line that
        intersects with both line segments). This method is different from self.getProjectedWindowLine
        as that one only answers one of the projected points that is not None. For efficiency
        reasons only one of the projections is made there. For almost parallel lines all projects are
        more or less identical."""
        return (
            (pc.p, self.getProjectedPoint(pc.p)),
            (pc.p_1, self.getProjectedPoint(pc.p_1)),
            (self.p, pc.getProjectedPoint(self.p)),
            (self.p_1, pc.getProjectedPoint(self.p_1))
        )

    def getProjectedWindowLine(self, pc):
        """Answer a tuple of one of the 4 points of (self.p, self.p_1, pc.p, pc.p_1)
        that has a projection on the other line and its projection point.
        If no projection exists in the window of the two line segments, then answer
        (None, None)."""
        pp = self.getProjectedPoint(pc.p)
        if pp is not None:
            return pc.p, pp
        pp = self.getProjectedPoint(pc.p_1)
        if pp is not None:
            return pc.p_1, pp
        pp = pc.getProjectedPoint(self.p)
        if pp is not None:
            return self.p, pp
        pp = pc.getProjectedPoint(self.p_1)
        if pp is not None:
            return self.p_1, pp
        return None, None

class Stem:
    isBlack = True

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def __repr__(self):
        return f'Stem(x1={self.v1.x}, x2={self.v2.x})'

    def _get_x(self):
        return min(self.v1.x, self.v2.x)
    x = property(_get_x)

    def _get_width(self):
        return abs(self.v1.x - self.v2.x)
    width = property(_get_width)

class HCounter(Stem):
    isBlack = False

class Bar:
    isBlack = True

    def __init__(self, h1, h2):
        self.h1 = h1
        self.h2 = h2

    def __repr__(self):
        return f'Bar(y1={self.h1.y}, y2={self.h2.y})'

    def _get_y(self):
        return min(self.h1.y, self.h2.y)
    y = property(_get_y)

    def _get_height(self):
        return abs(self.h1.y - self.h2.y)
    height = property(_get_height)

class VCounter(Bar):
    isBlack = False

class GlyphAnalyzer:
    """The GlyphAnalyzer gets diagonals, verticals, horizontal, stems and bars from a glyph contour."""

    def __init__(self, g):
        self.glyph = g # Save as weakref and store the path in self.glyphPath
        self.reset()

    def _get_glyph(self):
        return self._glyph()
    def _set_glyph(self, glyph):
        self._glyph = weakref.ref(glyph)
        self.glyphPath = glyph.getRepresentation("defconAppKit.NSBezierPath")
    glyph = property(_get_glyph, _set_glyph)

    def reset(self):
        """There's changes in the glyph or attributes were not yet analyzed: examine the glyph."""
        assert self.glyph is not None

        self.pointContexts = []

        self.diagonalStems = {}
        self.diagonals = {} # Angle (different from 0, 90) is the key for point context (p-1, p)

        self.stems = {} # Holds dictionary for horizonal relation between verticals
        self.verticals = {} # Dictioanry with all verticals (round and straight)
        self.roundVerticals = {} # Dictionary with only round verticals
        self.straightVerticals = {}

        self.bars = {} # Holds dictionary for vertical relation between horizontals
        self.horizontals = {} # Dictionary with all horizontals (round and straight)
        self.roundHorizontals = {} # Dictionary with only round horizontals
        self.straightHorizontals = {} # Dictionary with only straight horizontals

        for cIndex, contour in enumerate(self.glyph.contours):
            points = contour.points
            for pIndex in range(len(points)):
                p_2, p_1, p, p1, p2 = pp = points[pIndex-4], points[pIndex-3], points[pIndex-2], points[pIndex-1], points[pIndex] # Trick to run over edge of point list
                if p.type == 'offcurve': # Skip the off-curve points as main focus of interest.
                    continue

                pointContext = PointContext(cIndex, pIndex-2, pp) # Context reference of a point: contourIndex, pointIndex, (p-2, p-1, p, p+1, p+2)
                self.pointContexts.append(pointContext)

                # Horizontals
                if p_1.y == p.y == p1.y and p.type in ('curve', 'qcurve'):
                    if p.y not in self.horizontals:
                        self.horizontals[p.y] = []
                    self.horizontals[p.y].append(pointContext)
                    if p.y not in self.roundHorizontals:
                        self.roundHorizontals[p.y] = []
                    self.roundHorizontals[p.y].append(pointContext)

                elif p_1.y == p.y:
                    if p.y not in self.horizontals:
                        self.horizontals[p.y] = []
                    self.horizontals[p.y].append(pointContext)
                    if p.y not in self.straightHorizontals:
                        self.straightHorizontals[p.y] = []
                    self.straightHorizontals[p.y].append(pointContext)

                # Verticals
                if p_1.x == p.x == p1.x and p.type in ('curve', 'qcurve'):
                    if p.x not in self.verticals:
                        self.verticals[p.x] = []
                    self.verticals[p.x].append(pointContext)
                    if p.y not in self.roundVerticals:
                        self.roundVerticals[p.x] = []
                    self.roundVerticals[p.x].append(pointContext)

                elif p_1.x == p.x:
                    if p.y not in self.verticals:
                        self.verticals[p.x] = []
                    self.verticals[p.x].append(pointContext)
                    if p.x not in self.straightVerticals:
                        self.straightVerticals[p.x] = []
                    self.straightVerticals[p.x].append(pointContext)

        # Now we have all point contexts stores, try to find diagonals and store them by angle
        # Find the dictionary of all point contexts, where the key is the
        # normalized integer rounded angle. Definition of a diagonal is that it
        # cannot be a vertical or horizontal."""

        for pc in self.pointContexts: 
            if pc.isDiagonal: # Optimized check on not horizontal or vertical
                angle = pc.normalizedAngle
                if not angle in self.diagonals: # In case there is no angle entry yet, create one.
                    self.diagonals[angle] = []
                self.diagonals[angle].append(pc)

        # Find Diagonal Stems

        found = set()
        for diagonals1 in self.diagonals.values(): # Loop through all pointContexts that are diagonal
            for pc0 in diagonals1:
                for diagonals2 in self.diagonals.values(): # angle1, diagonals2
                    for pc1 in diagonals2:
                        if (pc0.index, pc1.index) in found:
                            continue
                        # Test if the y values are in range so this can be seen as stem pair
                        # and test if this pair is spanning a black space
                        if not self.isDiagonalStem(pc0, pc1):
                            continue
                        found.add((pc0.index, pc1.index))
                        found.add((pc1.index, pc0.index))

                        distance = pc0.averageDistance(pc1) # Average length of the diagonal projected lines
                        if distance is not None:
                            if not distance in self.diagonalStems:
                                self.diagonalStems[distance] = []
                            self.diagonalStems[distance].append((pc0, pc1))
        # Try to find stems
        xx = None # Previous x
        vv = None # Previous vertical

        for x, vertical in sorted(self.verticals.items()):
            v = vertical[0]
            if xx is not None:
                if xx not in self.stems:
                    self.stems[xx] = []
                if self.isBlackStem(vv, v): # Middle between the verticals is black?
                    stem = Stem(vv, v)
                else:
                    stem = HCounter(vv, v)
                self.stems[xx].append(stem)
            xx = x
            vv = v

        # Try to find bars
        yy = None # Previous y
        hh = None # Previous horizontal

        for y, horizontal in sorted(self.horizontals.items()):
            h = horizontal[0]
            if yy is not None:
                if yy not in self.bars:
                    self.bars[yy] = []
                if self.isBlackBar(hh, h): # Middle between the horizontals is black?
                    bar = Bar(hh, h)
                else:
                    bar = VCounter(hh, h)
                self.bars[yy].append(bar)
            yy = y
            hh = h


    def isBlackStem(self, v1, v2):
        """Test if these two verticals span a stem, black in the middle."""
        tx, ty = min(v1.x, v2.x) + abs(v1.x - v2.x)/2, min(v1.y, v2.y) + abs(v1.y - v2.y)/2
        return self.onBlack(tx, ty)
        
    def isBlackBar(self, h1, h2):
        """Test if these two verticals span a bar, black in the middle."""
        tx, ty = min(h1.y, h2.y) + abs(h1.y - h2.y)/2, min(h1.y, h2.y) + abs(h1.y - h2.y)/2
        return self.onBlack(tx, ty)
                
    def onBlack(self, x, y):
        """Answers if the single point `(x, y)` is on black."""
        return self.glyphPath.containsPoint_((x, y))

    def spanBlack(self, x1, y1, x2, y2, step=SPANSTEP):
        """The `spanBlack` method answers if the number of
        recursive steps between _pc0_ and _pc1_ are on black area of the glyph.
        If step is smaller than the distance between the points, then just
        check in the middle of the line.  The method does not check on the end
        points of the segment, allowing to test these separate through
        `self.onBlack` or `self.coveredInBlack`."""
        dx = x2 - x1
        dy = y2 - y1
        distance = dx*dx + dy*dy # Save sqrt time, compare with square of step
        mx = x1 + dx/2
        my = y1 + dy/2
        result = self.onBlack(mx, my) # Check the middle of the vector distance.
        if distance > step*step: # Check for the range of steps if the middle point of the line is still on black
            result = result and self.spanBlack(x1, y1, mx, my, step) and self.spanBlack(mx, my, x2, y2, step)
        # Check if distance is still larger than step, otherwise just check in the middle
        return result

    def lineOnBlack(self, pc0, pc1=None, step=SPANSTEP):
        """Answers if the line betweep _pc0_ and _pc1_ is entirely running on
        black, except for the end point. To test if the line is entirely on
        black, use `self.lineInBlack()`. If _pc1_ is omitted, then test the
        line between _pc0_ and the next point on the contour."""
        if pc1 is None:
            pc1 = pc0.p_1
        return self.spanBlack(pc0.x, pc0.y, pc1.x, pc1.y, step)

    def isDiagonalStem(self, pc0, pc1):
        """Test on more or less parallel."""
        return pc0.isParallel(pc1) and self.overlappingLinesInWindowOnBlack(pc0, pc1)

    def overlappingLinesInWindowOnBlack(self, pc0, pc1, step=SPANSTEP):
        """Answers if the vertical span between _pc0_ and _pc1_ just spans
        black area, by stepping from a point on one line to a point on the
        other line. The trick is to fine the right points. If the line it too
        angled (e.g. under certain circumstances the line between the middle
        points is almost parallel to the line, then our trick with testing on
        the blackness the 4 one-unit points around a point fails, when the
        segments is tested close to one of the main points. So we need to test
        on from the middle of the overlapping window perpendicular to the other
        line."""
        pp0, pp1 = pc0.getProjectedWindowLine(pc1)
        return not None in (pp0, pp1) and self.lineOnBlack(pp0, pp1, step)


