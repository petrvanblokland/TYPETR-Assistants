# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     pointanalyzer.py
#
from tnbits.analyzers.elements.constants import Constants

class PointAnalyzer(Constants):

    def isOnCurve(self, point):
        # Test the type of defcon point
        return point.segmentType is not None

    def isOffCurve(self, point):
        # Test the type of defcon point
        return point.segmentType is None

    def isCurve(self, point):
        # Test the type of defcon point
        return point.segmentType in self.CURVES

    def isInflection(self, pc):
        """Answers if the point context has an inflection
        point between the current point and the next point."""
        pass
