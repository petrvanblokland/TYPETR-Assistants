# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     constants.py
#
from tnbits.analyzers.elements.constants import Constants
from tnbits.analyzers.elements.pointcontextlist import Vertical, Horizontal

class BoundingBox(Constants):

    def __init__(self):
        self.left = Vertical()  # List of PointContext instances as part of the bounding box.
        self.right = Vertical()
        self.bottom = Horizontal()
        self.top = Horizontal()

    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, tuple(self.asList()))

    def __getitem__(self, index):
        # Top, right, bottom, left
        return self.asList()[index]

    def asList(self):
        return [self.minX, self.minY, self.maxX, self.maxY]

    asRect = asList

    def asListOrNone(self):
        """Answer the boundings values as list @[self.minX, self.minY,
        self.maxX, self.maxY]@.  If one or more is @None@, then answer a single
        @None@ value."""
        boundings = self.asList()
        if None in boundings:
            return None
        return boundings

    # self.minX    Answer the x value of the left vertical

    def _get_minX(self):
        return self.left.x

    minX = property(_get_minX)

    # self.maxX

    def _get_maxX(self):
        return self.right.x

    maxX = property(_get_maxX)

    # self.maxY

    def _get_maxY(self):
        return self.top.y

    maxY = property(_get_maxY)

    # get.minY

    def _get_minY(self):
        return self.bottom.y

    minY = property(_get_minY)

    # self.pointContexts

    def _get_pointContexts(self):
        """The `self.pointContexts` method answers a list with all point
        contexts of this `self`, independent if the are located in the
        horizontals or verticals. The answered list does not contain any
        duplicate point contexts."""
        pcs = set()
        for pc in self.left:
            pcs.add(pc)
        for pc in self.right:
            pcs.add(pc)
        for pc in self.top:
            pcs.add(pc)
        for pc in self.bottom:
            pcs.add(pc)
        return list(pcs)

    pointContexts = property(_get_pointContexts)

    def extendByPointContext(self, pc, offset=None):
        """The `extendByPointContext` extends the current values of the bounding
        box with the position of `pc.p`. The optional _offset_ `(x,y)` is
        added to the point, to allow the transformation of composites be added
        to the bounding box."""
        if offset is not None:
            offsetx, offsety = offset
        else:
            offsetx = offsety = 0
        rx = int(round(pc.p.x + offsetx))
        ry = int(round(pc.p.y + offsety))
        # Xmin
        if not self.left or rx == self.left[0].rx:
            self.left.append(pc)
        elif rx < self.left[0].rx:
            self.left = Vertical([pc])
        # Xmax
        if not self.right or rx == self.right[0].rx:
            self.right.append(pc)
        elif rx > self.right[0].rx:
            self.right = Vertical([pc])
        # Ymin
        if not self.bottom or ry == self.bottom[0].ry:
            self.bottom.append(pc)
        elif ry < self.bottom[0].ry:
            self.bottom = Horizontal([pc])
        # Ymax
        if not self.top or ry == self.top[0].ry:
            self.top.append(pc)
        elif ry > self.top[0].ry:
            self.top = Horizontal([pc])
