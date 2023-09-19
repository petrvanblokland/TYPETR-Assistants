# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     gaussprofile.py
#
import weakref
from tnbits.toolbox.transformer import TX
from tntools._lab.petr.ErikGauss.gaussTools import getKernel

    #   G A U S S

class GaussProfile(object):

    RADIUS = 100
    GRID = 10
    KERNELS = {RADIUS/GRID: getKernel(RADIUS/GRID)} # Initialize default kernel.

    def __init__(self, glyph, x, y0, y1, step, radius=None, grid=None, normalize=1000):
        self.x = x
        self.y0 = y0
        self.y1 = y1
        self.minY = y1 # Will be adjusted to the smallest y where the level is not zero.
        self.maxY = y0 # Will be adjusted to the largest y where the level is not zero.
        self.step = step
        self.normalize = normalize # Scale factor of levels, to make the result store as integer.
        self.radius = radius or self.RADIUS
        self.grid = grid or self.GRID
        self.glyph = glyph # Weakref to glyph. Levels-info are cached directly into the the glyph.lib
        self.levels = []
        self.calculate()

    def _set_glyph(self, glyph):
        self._glyph = weakref.ref(glyph)
    def _get_glyph(self):
        return self._glyph()
    glyph = property(_get_glyph, _set_glyph)

    def __repr__(self):
        return '[GaussProfile %s %s]' % (TX.path2StyleName(self.glyph.font.path), self.glyph.name)

    def getKernel(self):
        kernelKey = self.radius/self.grid
        if not kernelKey in self.KERNELS:
            self.KERNELS[kernelKey] = getKernel(kernelKey)
        return self.KERNELS[kernelKey]

    def getAverage(self):
        """Answer the average level for all levels that are not zero."""
        levels = []
        for level in self.levels:
            if level:
                levels.append(level)
        if len(levels):
            return sum(levels)/len(levels)
        return 0

    def compare(self, profile, tolerance):
        """Answer the Gauss values.
        It is assumed that the number of scan lines of self is equal to the number of profile, otherwise the
        range compare is ignored. If the answer dictionary is empty, there is no range where these profiles
        are similar."""
        # Only compare with identical number of level, otherwise ignore profile height.
        allEmpty = True
        if len(profile.levels) == len(self.levels):
            for index, line1 in enumerate(profile.levels):
                line2 = self.levels[index]
                if line1 or line2: # Avoid comparing empty with empty
                    allEmpty = False
                if tolerance < abs(line2 - line1): # If difference larger than tolerance, abort
                    return False
        return not allEmpty

    def calculate(self):
        """Calculate the photons in each pixel on position self.x between the vertical range (self.y0, self.y1).
        Truncate the descender to a whole number of steps, to we get exactly to the baseline."""

        glyph = self.glyph
        if glyph is not None:
            nsPathObject = self.glyph.getRepresentation("defconAppKit.NSBezierPath")

            kernel = self.getKernel() # Get cached kernel or create one for the current radius/grid measure.
            for y in range(int(self.y0/self.step)*self.step, int(self.y1/self.step)*self.step, self.step):
                level = 0
                for pos, val in kernel.items():
                    if nsPathObject.containsPoint_((self.x+pos[0]*self.GRID, y+pos[1]*self.GRID)):
                        level += val * self.normalize # Normalize on 1000x.
                self.levels.append(level)
                if level: # If there is any light level on this y, then adjust the min/max
                    self.minY = min(self.minY, y)
                    self.maxY = max(self.maxY, y)
