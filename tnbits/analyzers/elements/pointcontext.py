# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     pointcontext.py
#
import math
from tnbits.toolbox.mathematics import Mathematics
from tnbits.analyzers.elements.pointanalyzer import PointAnalyzer
from tnbits.objects.point import Point

def calculateAngle(p1, p2, inDegrees=True):
    xDiff = p2.x - p1.x
    yDiff = p2.y - p1.y
    angle = math.atan2(yDiff, xDiff)
    if inDegrees:
        angle = math.degrees(angle)
    return angle

def angleOfLines(p1, p2, q1, q2):
    angle1 = calculateAngle(p1, p2)
    angle2 = calculateAngle(q1, q2)
    angle = angle2 - angle1
    if angle < -180: angle += 360
    elif angle > 180: angle -= 360
    return angle

class PointContext(PointAnalyzer):
    """
    The `PointContext` instance is a `Point` wrapper, that also takes the 3 points previous
    and next 3 points on the contour. The instance behaves like a normal point _p_, but additional information is
    available as interpreted from the point context in relation to the neighbor points. The total of 6 points is derived
    from the average construction of a serif, so it is possible to hold (and interpret) an entire serif sequence inside
    one point context.
    """
    PARALLEL_TOLERANCE = 2 # Difference tolerance angle in degrees to take point contexts as parallel

    def __init__(self, p_4, p_3, p_2, p_1, p, p1, p2, p3, p4, index, pIndex, contourIndex, clockwise, glyphName=None):
        self.p_4 = p_4
        self.p_3 = p_3
        self.p_2 = p_2
        self.p_1 = p_1
        self.p = p
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.contourIndex = contourIndex
        self.index = index # Index of onCurves
        self.pIndex = pIndex # Sequential index for all point.
        self.clockwise = clockwise
        self.glyphName = glyphName
        self._direction = None  # Cache direction once calculated.
        self._angle = None  # Cache axis once calculated.

    # self.x

    def _get_x(self):
        return self.p.x

    x = property(_get_x)

    # self.y

    def _get_y(self):
        return self.p.y

    y = property(_get_y)

    # self.rx

    def _get_rx(self):
        # Get rounded value.
        return int(round(self.x))

    rx = property(_get_x)

    # self.ry

    def _get_ry(self):
        # Get rounded value
        return int(round(self.y))

    ry = property(_get_ry)

    # self.angle    Answer angle of the point context
    def _get_angle(self):
        if self._angle is None:
            xDiff = self.p1.x - self.p.x
            yDiff = self.p1.y - self.p.y
            self._angle = round(math.atan2(yDiff, xDiff) * 180 / math.pi, 3)
        return self._angle

    angle = property(_get_angle)

    # self.normalizedAngle    Answer the normalized angle of self, -90 <= angle <= 90

    def _get_normalizedAngle(self):
        angle = self.angle
        while angle < 0:
            angle += 180
        while angle > 360:
            angle -= 180
        return angle

    normalizedAngle = property(_get_normalizedAngle)

    def __repr__(self):
        s = 'pc[%s] (%s,%s)' % (self.index, self.p.x, self.p.y)
        if self.isNextVertical():
            s += ' vertical'
        if self.isNextHorizontal():
            s += ' horizontal'
        if self.isRoundStemExtreme():
            s += ' roundstem'
        if self.isRoundBarExtreme():
            s += ' roundbar'
        if self.isTerminal():
            s += ' terminal'
        if self.clockwise:
            s += ' c%d CW' % self.contourIndex
        else:
            s += ' c%s CCW' % self.contourIndex
        if self.glyphName is not None:
            s += ' (%s)' % self.glyphName
        return s

    def isStart(self):
        return self.index == 0

    def isUp(self):
        return self.p.y < self.p1.y

    def isDown(self):
        return self.p.y > self.p1.y

    def isLeft(self):
        return self.p.x < self.p1.x

    def isRight(self):
        return self.p.y > self.p1.y

    def isHorizontalExtreme(self):
        """
        The `isHorizontalExtreme` method answers if the point context is an extreme
        (such as the side of an O).
        """
        # Is the point context a vertical and extreme in x-direction?
        # @@@ Also test on non-inflection point.
        return self.isNextVertical()\
            and self.isPrevVertical()\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isLeftRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.x < nextP.x\
            and self.p.x < prevP.x

    def isRightRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.x > nextP.x\
            and self.p.x > prevP.x

    def isTopRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.y > nextP.y\
            and self.p.y > prevP.y

    def isBottomRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.y < nextP.y\
            and self.p.y < prevP.y

    def isVerticalRoundExtreme(self):
        return self.isTopRoundExtreme() or self.isBottomRoundExtreme()

    def isHorizontalRoundExtreme(self):
        return self.isLeftRoundExtreme() or self.isRightRoundExtreme()

    def isNextVertical(self):
        return self.p.x == self.p1.x

    isVertical = isNextVertical

    def isPrevVertical(self):
        return self.p.x == self.p_1.x

    def isVerticalExtreme(self):
        """
        Is the point context a horizontal and extreme in y-direction?
        """
        return self.isNextHorizontal()\
            and self.isPrevHorizontal()\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isNextHorizontal(self):
        return self.p.y == self.p1.y

    isHorizontal = isNextHorizontal

    def isPrevHorizontal(self):
        return self.p.y == self.p_1.y

    def isInflection(self):
        valid = self.isOnCurve(self.p) and self.isOffCurve(self.p_1) and self.isOffCurve(self.p1)
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        if valid and nextP is not None and prevP is not None:
            a1 = angleOfLines(self.p, self.p1, self.p, nextP)
            a2 = angleOfLines(self.p, self.p_1, self.p, prevP)
            if a1 * a2 > 0:
                return True
        return False

    def isDiagonal(self):
        return not (self.isVertical() or self.isHorizontal())

    def isParallel(self, pc, tolerance=None):
        """Answer if self is parallel to _pc_ point context. Optional attribute _tolerance_
        is the margin to interpret point context lines to be parallel. Default is `self.PARALLEL_TOLERANCE`."""
        if tolerance is None:
            tolerance = self.PARALLEL_TOLERANCE
        return abs(self.normalizedAngle - pc.normalizedAngle) <= tolerance

    def isRoundStemExtreme(self):
        return self.isHorizontalExtreme()\
            and (self.isLeftRoundExtreme() or self.isRightRoundExtreme())\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isRoundBarExtreme(self):
        return self.isVerticalExtreme()\
            and (self.isTopRoundExtreme() or self.isBottomRoundExtreme())\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isTerminal(self):
        return False

    def inVerticalWindow(self, pc):
        """
        The `inVerticalWindow` method checks if there is any overlap in X-direction to make
        the vertical comparison optically define as a "bar".

        True    self.minx-------------self.maxx
                            p.minx----------------p.maxx

        True               self.minx----------------------p.maxx
                p.minx---------------p.maxx

        True               self.minx------------self.maxx
                p.minx-------------------------------p.maxx

        False                               self.minx----------self.maxx
                p.minx--------p.maxx

        False   self.minx--------self.maxx
                                                 p.minx------------------------p.maxx
        """
        return pc.minx() < self.maxx() and self.minx() < pc.maxx()

    def inHorizontalWindow(self, pc):
        """
        The `inHorizontalWindow` method checks if there is any overlap in X-direction to make
        the vertical comparison optically define as a "stem".

        True    self.miny-------------self.maxy
                            p.miny----------------p.maxy

        True               self.miny----------------------p.maxy
                p.miny---------------p.maxy

        True               self.miny------------self.maxy
                p.miny-------------------------------p.maxy

        False                               self.miny----------self.maxy
                p.miny--------p.maxy

        False   self.miny--------self.maxy
                                                 p.miny------------------------p.maxy
        """
        return pc.miny() < self.maxy() and self.miny() < pc.maxy()

    def inDiagonalWindow(self, pc):
        """Answer if _pc_ fits in the diagonal window of `self`."""
        return not None in self.getProjectedWindowLine(pc)

    def getProjectedPoint(self, p):
        """Answer the perpendicular projection of point _p_ in the line segment of `self`.
        If the projection in not within the range of the line segment, then answer `None`.
        """
        pp = self.projectedOnLine(p)
        if self.inBoundingBox(pp): # Is the projected point in inside the line segment
            return pp
        return None # Projection not within the line segment window.

    def getProjectedWindowLines(self, pc):
        """Answer all 4 projected window lines. Note that some of them can be `None`
        is the projects falls outside the window (the overlapping area of a perpendicular line that
        intersects with both line segments). This method is different from `self.getProjectedWindowLine`
        as that one only answers one of the projected points that is not `None`. For efficiency
        reasons only one of the projections is made there. For almost parallel lines all projects are
        more or less identical."""
        return (
            (pc.p, self.getProjectedPoint(pc.p)),
            (pc.p1, self.getProjectedPoint(pc.p1)),
            (self.p, pc.getProjectedPoint(self.p)),
            (self.p1, pc.getProjectedPoint(self.p1))
        )

    def getProjectedWindowLine(self, pc):
        """Answer a tuple of one of the 4 points of `(self.p, self.p1, pc.p, pc.p1)`
        that has a projection on the other line and its projection point.
        If no projection exists in the window of the two line segments, then answer
        `(None, None)`."""
        pp = self.getProjectedPoint(pc.p)
        if pp is not None:
            return pc.p, pp
        pp = self.getProjectedPoint(pc.p1)
        if pp is not None:
            return pc.p1, pp
        pp = pc.getProjectedPoint(self.p)
        if pp is not None:
            return self.p, pp
        pp = pc.getProjectedPoint(self.p1)
        if pp is not None:
            return self.p1, pp
        return None, None

    def inBoundingBox(self, p):
        return (self.p.x <= p.x <= self.p1.x or self.p1.x <= p.x <= self.p.x) and (self.p.y <= p.y <= self.p1.y or self.p1.y <= p.y <= self.p.y)

    def minx(self):
        return min(self.p_1.x, self.p.x, self.p1.x)

    def maxx(self):
        return max(self.p_1.x, self.p.x, self.p1.x)

    def miny(self):
        return min(self.p_1.y, self.p.y, self.p1.y)

    def maxy(self):
        return max(self.p_1.y, self.p.y, self.p1.y)

    def middle(self, p1=None):
        """Answer the `Point` instance of the middle between the optional attribute points _p0_ and _p1_.
        If the points are omitted, then use respectively `self.p` and `self.p1`."""
        if p1 is None:
            p1 = self.p1
        return Point(int(round((self.x + p1.x)/2)), int(round((self.y + p1.y)/2)))

    def distanceTo(self, p):
        """Answer the distance of point _p_ to the line of self."""
        return Mathematics.point2Line(self.p.x, self.p.y, self.p1.x, self.p1.y, p.x, p.y)

    def projectedOnLine(self, p):
        """Answer the point context _pc_ projects on the line of `self`."""
        x, y = Mathematics.pointProjectedOnLine(self.p.x, self.p.y, self.p1.x, self.p1.y, p.x, p.y)
        return Point(x, y)

    # self.nextOnCurvePoint

    def _get_nextOnCurvePoint(self):
        if self.isOnCurve(self.p1):
            return self.p1
        if self.isOnCurve(self.p2):
            return self.p2
        if self.isOnCurve(self.p3):
            return self.p3
        if self.isOnCurve(self.p4):
            return self.p4
        return None

    nextOnCurvePoint = property(_get_nextOnCurvePoint)

    # self.prevOnCurvePoint

    def _get_prevOnCurvePoint(self):
        if self.isOnCurve(self.p_1):
            return self.p_1
        if self.isOnCurve(self.p_2):
            return self.p_2
        if self.isOnCurve(self.p_3):
            return self.p_3
        if self.isOnCurve(self.p_4):
            return self.p_4
        return None

    prevOnCurvePoint = property(_get_prevOnCurvePoint)
