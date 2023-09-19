# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     stem.py
#
from tnbits.toolbox.mathematics import Mathematics
from tnbits.objects.point import Point
from tnbits.analyzers.elements.pointanalyzer import PointAnalyzer
from tnbits.analyzers.elements.pointcontext import PointContext
from tnbits.analyzers.elements.boundingbox import BoundingBox

class Stem(PointAnalyzer):
    """
    The `Stem` class instant takes the CVT related to this stem, and the  left and point `Vertical
    ` instance that stem binds.
    """

    def __init__(self, parent, point, glyphName=None, offset=None):
        assert parent is None or isinstance(parent, PointContext)
        assert point is None or isinstance(point, PointContext)
        self.parent = parent
        self.point = point
        self.offset = offset or (0,0) # Optional offset (dx, dy) tuple, e.g. used for stems derived from component references.
        self.glyphName = glyphName

    def __repr__(self):
        if self.offset in (None, (0,0)):
             return '[%s.%s: %s --> %s]' % (self.glyphName, self.__class__.__name__, self.parent, self.point)
        return '[%s.%s: %s+%s --> %s+%d]' % (self.glyphName, self.__class__.__name__, self.parent, self.point, self.offset[0], self.offset[1])

    def copy(self):
        return self.__class__(self.parent, self.point, self.glyphName, self.offset)

    def addOffset(self, offset):
        """In case of multiple chained component reference, analyzer will add incremental offset this way."""
        self.offset = self.offset[0] + offset[0], self.offset[1] + offset[1]

    # self.size

    def _get_size(self):
        return abs(self.parent.p.x - self.point.p.x)
    size = property(_get_size)

    # self.x    # Answers the tuple of both x value, shifted by x-offset

    def _get_x(self):
        dx = self.offset[0]
        return self.parent.p.x + dx, self.point.p.x + dx
    x = property(_get_x)

    # self.y    Answers the tuple of both y values, shifted by y-offset

    def _get_y(self):
        dy = self.offset[1]
        return self.parent.p.y + dy, self.point.p.y + dy
    y = property(_get_y)

    def isWhite(self):
        return False

    # self.nearestPoint

    def _get_nearestPoint(self):
        """
        The `getNearestPoint` method gets the nearest point in the `self.point` point context
        to `self.parent`.
        """
        nearp = self.point.p
        d = abs(self.parent.p.y - nearp.y)
        if self.isOnCurve(self.point.p1):
            d1 = abs(self.parent.p.y - self.point.p1.y)
            if d1 < d:
                nearp = self.point.p1
                d = d1
        if self.isOnCurve(self.point.p_1):
            d1 = abs(self.parent.p.y - self.point.p_1.y)
            if d1 < d:
                nearp = self.point.p_1
        return nearp
    nearestPoint = property(_get_nearestPoint)

    def isTerminal(self):
        """The stem is also a terminal, if the end of the parallel lines also are connected point contexts."""
        return False

class Counter(Stem):

    def __init__(self, parent, point, value, offset=None):
        Stem.__init__(self, parent, point, value, offset=offset)

    def isWhite(self):
        return True

class Width(Stem):

    def __init__(self, pc, value=None, offset=None):
        Stem.__init__(self, None, pc, offset=offset)
        self.value = value

    # self.size

    def _get_size(self):
        if self.value is not None:
            return self.value
        return self.point.p.x
    size = property(_get_size)

class Height(Width):

    # self.size

    def _get_size(self):
        if self.value is not None:
            return self.value
        return self.point.p.y
    size = property(_get_size)

class Bar(Stem):

    # self.size

    def _get_size(self):
        return abs(self.parent.p.y - self.point.p.y)
    size = property(_get_size)

    def _get_nearestPoint(self):
        """
        The `getNearestPoint` method gets the nearest point in the `self.point` point context
        to `self.parent`.
        """
        nearp = self.point.p
        d = abs(self.parent.p.x - nearp.x)
        if self.isOnCurve(self.point.p1):
            d1 = abs(self.parent.p.x - self.point.p1.x)
            if d1 < d:
                nearp = self.point.p1
                d = d1
        if self.isOnCurve(self.point.p_1):
            d1 = abs(self.parent.p.x - self.point.p_1.x)
            if d1 < d:
                nearp = self.point.p_1
        return nearp

    nearestPoint = property(_get_nearestPoint)

class BlueBar(PointAnalyzer):

    def __init__(self, y, size, glyphName=None, offset=None):
        self.x = 0
        self._y = y
        self.size = size
        self.offset = offset or (0,0) # Optional offset (dx, dy) tuple, e.g. used for stems derived from component references.
        self.glyphName = glyphName

    def __repr__(self):
        if self.offset in (None, (0,0)):
             return '[%s.%s: %s --> %s]' % (self.glyphName, self.__class__.__name__, self.y, self.size)
        return '[%s.%s: %s+%s --> %s+%d]' % (self.glyphName, self.__class__.__name__, self.y, self.offset[0], self.y+self.size, self.offset[1])

    # self.y    Answers the tuple of both y values, shifted by y-offset
    def _get_y(self):
        return self._y + self.offset[1]
    y = property(_get_y)


class VerticalCounter(Bar):

    def __init__(self, parent, point, value, offset=None):
        Bar.__init__(self, parent, point, value, offset=offset)

    def isWhite(self):
        return True

class DiagonalStem(Stem):

    # self.run answers the horizontal run of the diagonal.

    # self.nearestPoint

    def _get_nearestPoint(self):
        """The `getNearestPoint` method gets the nearest point in the `self.point` point context
        to `self.parent`. Default for a diagonal is always to answer `self.point.p`.
        """
        return self.point.p

    nearestPoint = property(_get_nearestPoint)

    # self.size    Average distance between the diagonal projected line segments.

    def _get_size(self):
        d = 0
        projectionLines = self.projectionLines
        for p, projectedP in projectionLines: # p is PointContext instance, projectP is Point instance.
            d += Mathematics.distance(p.x, p.y, projectedP.x, projectedP.y)
        return int(round(d/len(projectionLines)))

    size = property(_get_size)

    """A diagonal is a special kind of `Stem`, as it also is able to calculate
    the projected window points."""

    # self.projectionLines    Answer the list of valid projection lines (tuple of point + projected point)

    def _get_projectionLines(self):
        projectionLines = []
        for projectionLine in self.point.getProjectedWindowLines(self.parent):
            if not None in projectionLine:
                projectionLines.append(projectionLine)
        return projectionLines

    projectionLines = property(_get_projectionLines)

    # self.perpendicularMiddleLine     Answer the line that is average perpendicular and in the middle of the projected window

    def _get_perpendicularMiddleLine(self):
        # Calculate the average middle from the projections
        mx = my = 0
        projectionLines = self.projectionLines
        count = len(projectionLines)*2 # Avoid double division of average
        for p, projectedP in projectionLines:
            mx += p.x + projectedP.x
            my += p.y + projectedP.y
        m = Point(mx/count, my/count)
        # Now project this window middle points on the two lines again.
        pp0 = self.point.getProjectedPoint(m)
        pp1 = self.parent.getProjectedPoint(m)
        return pp0, pp1

    perpendicularMiddleLine = property(_get_perpendicularMiddleLine)

    # self.perpendicularLines   Answer the relevant perpendicular lines (start, middle, end) of the projectionLines.

    def _get_perpendicularLines(self):
        projectionLines = self.projectionLines
        if len(projectionLines) == 2:
            return projectionLines[0], self.perpendicularMiddleLine, self.projectionLines[1]
        return [self.perpendicularMiddleLine]

    perpendicularLines = property(_get_perpendicularLines)

class Serif(Stem):
    """
    The `Serif` class holds the two point contexts (`self.parent` and `self.point`)
    that span a continuous set of point contexts defining a serif.
    """

    def _get_boundingBox(self):
        bb = BoundingBox()
        bb.extendByPointContext(self.parent)
        bb.extendByPointContext(self.point)
        return bb

    boundingBox = property(_get_boundingBox)

class Overshoot(PointAnalyzer):

    def __init__(self, pc, reference):
        self.pc = pc
        self.reference = reference

    def _get_size(self):
        return self.pc.p.y - self.reference.y

    size = property(_get_size)

