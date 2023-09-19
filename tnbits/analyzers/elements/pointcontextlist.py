# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     pointcontextlist.py
#
from tnbits.analyzers.elements.pointcontext import PointContext

class PointContextList(list):
    """The `PointContextList` us a group of related `PointContext`
    instances that can be queried and selected on their attributes."""
    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, list(self))

    def append(self, pc):
        assert isinstance(pc, PointContext)
        list.append(self, pc)

class Vertical(PointContextList):
    """The `Vertical` class is a list of point contexts that share the same
    x-value self.append, self.x, self.y, self.alternates, self.minY,
    self.max.Y"""
    # self.x

    def _get_x(self):
        if len(self):
            return self[0].p.x
        return None

    x = property(_get_x)

    # self.y

    def _get_y(self):
        # Vertical has not one defined y
        return None

    y = property(_get_y)

    # self.minYPoint    Answer the point context with the minimum Y of all vertical point contexts

    def _get_minYPoint(self):
        bottomPC = None
        for pc in self:
            if bottomPC is None or pc.y < bottomPC.y:
                bottomPC = pc
        return bottomPC

    minYPoint = property(_get_minYPoint)

    # self.maxYPoint    Answer the point context with the maximum Y of all vertical point contexts

    def _get_maxYPoint(self):
        topPC = None
        for pc in self:
            if topPC is None or pc.y > topPC.y:
                topPC = pc
        return topPC

    maxYPoint = property(_get_maxYPoint)

    # self.alternates

    def _get_alternates(self):
        """Answers the list of points that are not top or bottom."""
        alternates = []
        topBottom = (self.minYPoint, self.maxYPoint)
        for pc in self:
            if not pc in topBottom:
                alternates.append(pc)
        return alternates

    alternates = property(_get_alternates)

class Horizontal(PointContextList):
    """The `Horizontal` class is a list of point contexts that share the same
    y-value self.append, self.x, self.y, self.alternates, self.minX,
    self.maxX."""

    # self.x

    def _get_x(self):
        # Horizontal has no defined x
        return None

    x = property(_get_x)

    # self.y

    def _get_y(self):
        if len(self):
            return self[0].p.y
        return None

    y = property(_get_y)

    # self.minX    Answer the point context with the minimum X of all horizontal point contexts

    def _get_minXPoint(self):
        leftPC = None
        for pc in self:
            if leftPC is None or pc.x < leftPC.x:
                leftPC = pc
        return leftPC

    minXPoint = property(_get_minXPoint)

    # self.maxXPoint    Answer the point context with the maximum X of all horizontal point contexts

    def _get_maxXPoint(self):
        rightPC = None
        for pc in self:
            if rightPC is None or pc.x > rightPC.x:
                rightPC = pc
        return rightPC

    maxXPoint = property(_get_maxXPoint)

    # self.alternates

    def _get_alternates(self):
        """Answers the list of points that are not left or right extremes."""
        alternates = []
        leftRight = (self.minXPoint, self.maxXPoint)
        for pc in self:
            if not pc in leftRight:
                alternates.append(pc)
        return alternates

    alternates = property(_get_alternates)

class Diagonal(PointContextList):
    pass
