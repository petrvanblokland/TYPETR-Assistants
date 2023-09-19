# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#         contour.py
#
import copy
from tnbits.constants import Constants

class Contour(object):
    """The Contour holds a list of Point objects and the (automatic) clockwise boolean attribute."""

    C = Constants

    def __init__(self, clockwise=None, points=None):
        if points is None:
            points = [] # Point objects.
        self.points = points
        # Make clockwise as a property, so we can check if it is not defined and otherwise calculate it from the points.
        self._clockwise = clockwise # None is uninitialized. Will be calculated upon request.

    def __repr__(self):
        return 'Contour(clockwise:%s,points:%s)' % (self.clockwise, self.points)

    def __len__(self):
        return len(self.points)

    #
    # Usage and development moved to floqmodel/objects/glyph as global functions.
    #
    # self.clockwise        Simple and fast.
    # http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order

    def calcClockWise(self):
        p = None
        total = 0
        for index, nextP in enumerate(self.points):
            p = self.points[index-1] # Takes last point of list if index == 0 :)
            total += (nextP.x - p.x) * (nextP.y + p.y)
        return total > 0

    # self.clockwise

    def _get_clockwise(self):
        if self._clockwise is None: # If not set, then always calculate.
            self._clockwise = self.calcClockWise()
        return self._clockwise

    def _set_clockwise(self, clockwise):
        self._clockwise = clockwise # If None, then it will be (re)calculated upon request.

    clockwise = property(_get_clockwise, _set_clockwise)

    # self.normalizedStartPoints    Same as self.points, but now to shifted, so the start is an onCurve point.
    #                               The point.start value of the original start point is not changed.
    #                               Answer None for the unlikely situation that all points are off curve or
    #                               if there are no points in the list.

    def _get_normalizedStartPoints(self):
        points = self.points[:] # Create a copy of the original list
        found = False # Remember if we found an on curve point
        for index in range(len(points)):
            if not points[index].type in self.C.POINTTYPE_OFFCURVES:
                # This is the first on curve in the list.
                found = True
                points = points[index:]+points[0:index] # Reconstruct the list
                break
        if not found:
            return None
        return points

    normalizedStartPoints = property(_get_normalizedStartPoints)

    def copyByOffset(self, dx, dy):
        """In case the contour needs to transform (as e.g. inside a component),
        then we can't just add the @(dx,dy)@ to the points, because these are originals
        from the font. The only solution is to make a copy of contour and points
        and answer it. We'll try with a deep copy first."""
        contour = copy.deepcopy(self)
        for point in contour.points:
            point.x += dx
            point.y += dy
        return contour
