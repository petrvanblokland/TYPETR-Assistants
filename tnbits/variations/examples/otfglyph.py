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
#     otfglyph.py
#
# FIXME: DEPRECATED
from fontTools.ttLib.tables._g_l_y_f import Glyph as FTGlyph, GlyphCoordinates
from fontTools.varLib.models import supportScalar
from fontTools.varLib.iup import iup_delta
from tnbits.variations.ftvariations import *

class OTFGlyph(object):
    """Wraps a TrueType variation glyph."""

    def __init__(self, ttFont, glyphName, location):
        self._ttFont = ttFont
        self._glyphName = glyphName
        self._location = location

        try:
            self.width, self.lsb = ttFont['hmtx'][glyphName]
        except KeyError:
            self.width = 1000
            self.lsb = 50

    @staticmethod
    def _copyGlyph(glyph, glyfTable):
        """Deep copy?"""
        glyph = FTGlyph(glyph.compile(glyfTable))
        glyph.expand(glyfTable)
        return glyph

    def draw(self, pen):
        glyfTable = self._ttFont['glyf']
        glyph = glyfTable[self._glyphName]
        glyph = self._copyGlyph(glyph, glyfTable)
        variations = self._ttFont['gvar'].variations[self._glyphName]
        coordinates, _ = glyfTable.getCoordinatesAndControls(self._glyphName, self._ttFont)
        origCoords, endPts = None, None

        for var in variations:
            scalar = supportScalar(self._location, var.axes)

            if not scalar:
                continue

            delta = var.coordinates

            if None in delta:
                if origCoords is None:
                    origCoords, control = glyfTable.getCoordinatesAndControls(self._glyphName, self.ttFont)
                    endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
                delta = iup_delta(delta, origCoords, endPts)

        coordinates += GlyphCoordinates(delta) * scalar

        horizontalAdvanceWidth, leftSideBearing = setCoordinates(glyph,
                coordinates, self._ttFont['glyf'])
        self.width = horizontalAdvanceWidth
        glyph.draw(pen, self._ttFont['glyf'])  # XXX offset based on lsb
