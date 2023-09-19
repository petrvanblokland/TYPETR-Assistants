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
#     otfvarglyph.py
#
#

from fontTools.ttLib.tables._g_l_y_f import Glyph as FTGlyph, GlyphCoordinates
from fontTools.varLib.models import supportScalar
from fontTools.varLib.iup import iup_delta

class OTFVarGlyph(object):
    """Calculates a TrueType variation glyph at a specific location."""

    def __init__(self, font, glyphName, location):
        # TODO: assert TTFont
        self.font = font
        self.glyphName = glyphName
        self.location = location
        self.glyfTable = font['glyf']
        self.setVarGlyph(self.font, self.glyphName, self.location)

    def setVarGlyph(self, font, glyphName, location):
        varTable = font['gvar']
        glyph = self.glyfTable[glyphName]
        glyph = self.copyFTGlyph(glyph)
        variations = varTable.variations[glyphName]
        coordinates, _ = self.glyfTable.getCoordinatesAndControls(glyphName, font)
        origCoords, endPts = None, None

        for var in variations:
            scalar = supportScalar(location, var.axes)

            if not scalar:
                continue

            delta = var.coordinates

            if None in delta:
                if origCoords is None:
                    origCoords, control = self.glyfTable.getCoordinatesAndControls(glyphName, font)
                    endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
                delta = iup_delta(delta, origCoords, endPts)

            coordinates += GlyphCoordinates(delta) * scalar

        self.setCoordinates(glyph, coordinates)
        self.varGlyph = glyph

    def getVarGlyph(self):
        return self.varGlyph

    def draw(self, bezierPath):
        self.varGlyph.draw(bezierPath, self.glyfTable)

    def getVarWidth(self):
        return self.horizontalAdvanceWidth

    def getVarLSB(self):
        return self.leftSideBearing

    def copyFTGlyph(self, glyph):
        """Deep copies glyph object."""
        glyph = FTGlyph(glyph.compile(self.glyfTable))
        glyph.expand(self.glyfTable)
        return glyph

    def setCoordinates(self, glyph, coord):
        """Sets width, LSB and handles phantom points for (left, right, top,
        bottom) positions."""
        # TODO: Handle vertical
        assert len(coord) >= 4

        if not hasattr(glyph, 'xMin'):
            glyph.recalcBounds(self.glyfTable)

        leftSideX = coord[-4][0]
        rightSideX = coord[-3][0]
        topSideY = coord[-2][1]
        bottomSideY = coord[-1][1]

        for _ in range(4):
            del coord[-1]

        if glyph.isComposite():
            assert len(coord) == len(glyph.components)
            for p,comp in zip(coord, glyph.components):
                if hasattr(comp, 'x'):
                    comp.x,comp.y = p
        elif glyph.numberOfContours == 0:
            assert len(coord) == 0
        else:
            assert len(coord) == len(glyph.coordinates)
            glyph.coordinates = coord

        glyph.recalcBounds(self.glyfTable)
        self.horizontalAdvanceWidth = rightSideX - leftSideX
        self.leftSideBearing = glyph.xMin - leftSideX
