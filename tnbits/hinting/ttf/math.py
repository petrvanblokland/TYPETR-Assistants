#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    log.py
#

class Math(object):
    """
    Converts units.
    """

    def pixelsToFUnits(self, pixels):
        #TODO: to be implemented.
        pass

    def fUnitsToPixels(self, funits):
        """
        Converting FUnits to pixels.

        Values in the em square are converted to values in the pixel coordinate system
        by multiplying them by a scale. This scale is:

        pointSize * resolution / ( 72 points per inch * units_per_em )

        where pointSize is the size at which the glyph is to be displayed, and
        resolution is the resolution of the output device. The 72 in the denominator
        reflects the number of points per inch.

        For example, assume that a glyph feature is 550 FUnits in length on a 72 dpi
        screen at 18 point. There are 2048 units per em. The following calculation
        reveals that the feature is 4.83 pixels long.

        550 * 18 * 72 / ( 72 * 2048 ) = 4.83
        """
        return (funits * self.gstate.metrics['ppem'] * self.gstate.metrics['resolution']) /\
               (72 * self.gstate.metrics['em'])

