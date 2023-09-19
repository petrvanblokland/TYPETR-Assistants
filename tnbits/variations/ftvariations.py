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
#     ftvariations.py
#
#   FontTools-specific global functions.
#

from fontTools.ttLib.tables._g_l_y_f import Glyph as FTGlyph, GlyphCoordinates
from fontTools.varLib.models import supportScalar
from fontTools.varLib.iup import iup_delta

# DEPRECATED, use OTFVarGlyph instead.

def getVarGlyph(font, glyphName, location):
    glyfTable = font['glyf']
    varTable = font['gvar']
    glyph = glyfTable[glyphName]
    glyph = copyFTGlyph(glyph, glyfTable)
    variations = varTable.variations[glyphName]
    coordinates, _ = glyfTable.getCoordinatesAndControls(glyphName, font)
    origCoords, endPts = None, None

    for var in variations:
        scalar = supportScalar(location, var.axes)

        if not scalar:
            continue

        delta = var.coordinates

        if None in delta:
            if origCoords is None:
                origCoords, control = glyfTable.getCoordinatesAndControls(glyphName, font)
                endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
            delta = iup_delta(delta, origCoords, endPts)

        coordinates += GlyphCoordinates(delta) * scalar

    horizontalAdvanceWidth, leftSideBearing = setCoordinates(glyph, coordinates, glyfTable)
    return glyph, horizontalAdvanceWidth, leftSideBearing

def copyFTGlyph(glyph, glyfTable):
    """Deep copy?"""
    glyph = FTGlyph(glyph.compile(glyfTable))
    glyph.expand(glyfTable)
    return glyph

def setCoordinates(glyph, coord, glyfTable):
    """Sets width, LSB and handles phantom points for (left, right, top,
    bottom) positions."""
    # TODO: Handle vertical
    assert len(coord) >= 4

    if not hasattr(glyph, 'xMin'):
        glyph.recalcBounds(glyfTable)

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
    elif glyph.numberOfContours is 0:
        assert len(coord) == 0
    else:
        assert len(coord) == len(glyph.coordinates)
        glyph.coordinates = coord

    glyph.recalcBounds(glyfTable)
    horizontalAdvanceWidth = rightSideX - leftSideX
    leftSideBearing = glyph.xMin - leftSideX
    return horizontalAdvanceWidth, leftSideBearing
