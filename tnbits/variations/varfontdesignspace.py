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
#     varfontdesignspace.py
#
# FIXME: DEPRECATED, contained in Floq Model.
from __future__ import division

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph as TTGlyph, GlyphCoordinates
from fontTools.varLib.models import VariationModel, supportScalar, normalizeLocation
from tnbits.variations.designspacemodel import DesignSpaceBase, Axis
from tnbits.compilers.f5.ttfTools import getBestCmap
from fontTools.varLib.iup import iup_delta

def setCoordinates(glyph, coord, glyfTable):
    """Handles phantom points for (left, right, top, bottom) positions."""
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

    # TODO: Handle vertical
    # NOTE: Remove the round when
    # https://github.com/behdad/fonttools/issues/593 is fixed
    # font["hmtx"].metrics[glyphName] = int(round(horizontalAdvanceWidth)),
    # int(round(leftSideBearing))
    return horizontalAdvanceWidth, leftSideBearing

class TTVarFontGlyphSet(object):
    """Wrapper for a TrueType font with variations."""

    def __init__(self, ttFont):
        self._ttFont = ttFont
        self._axes = self.getAxesDict()
        self.setLocation({})

    def getAxesDict(self):
        try:
            axes = self._ttFont['fvar'].axes
            axesDict = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in axes}
        except KeyError as e:
            axesDict = {} # This is not a var font.

        return axesDict

    def setLocation(self, location):
        self.location = normalizeLocation(location, self._axes)

    def keys(self):
        return list(self._ttFont['glyf'].keys())

    def __contains__(self, glyphName):
        return glyphName in self._ttFont['glyf']

    def __getitem__(self, glyphName):
        return TTVarGlyph(self._ttFont, glyphName, self.location)

    def get(self, glyphName, default=None):
        try:
            return self[glyphName]
        except KeyError:
            return default

class TTVarGlyph(object):
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
        glyph = TTGlyph(glyph.compile(glyfTable))
        glyph.expand(glyfTable)
        return glyph

    def draw(self, pen):
        glyfTable = self._ttFont['glyf']
        varTable = self._ttFont['gvar']
        glyph = glyfTable[self._glyphName]
        glyph = self._copyGlyph(glyph, self.glyfTable)
        variations = varTable.variations[self._glyphName]
        coordinates, _ = glyfTable.getCoordinatesAndControls(self._glyphName,
                self._ttFont)
        origCoords, endPts = None, None

        for var in variations:
            scalar = supportScalar(self._location, var.axes)

            if not scalar:
                continue

            delta = var.coordinates

            if None in delta:
                if origCoords is None:
                    origCoords, control =
                    glyf.getCoordinatesAndControls(self._glyphName,
                            self._ttFont)
                    endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
                delta = iup_delta(delta, origCoords, endPts)

            coordinates += GlyphCoordinates(delta) * scalar

        horizontalAdvanceWidth, leftSideBearing = setCoordinates(glyph,
                coordinates, self._ttFont['glyf'])
        self.width = horizontalAdvanceWidth
        glyph.draw(pen, self._ttFont['glyf'])  # XXX offset based on lsb

class TTVarFontDesignSpace(DesignSpaceBase):

    @classmethod
    def fromVarFontPath(cls, path):
        ttFont = TTFont(path, lazy=True)
        return cls(ttFont)

    def __init__(self, ttFont):
        self.ttFont = ttFont
        self.cmap = getBestCmap(ttFont)
        axes = []
        fvar = self.ttFont["fvar"]
        for a in fvar.axes:
            nameRecord = self.ttFont["name"].getName(a.axisNameID, 3, 1)
            if nameRecord is None:
                nameRecord = self.ttFont["name"].getName(a.axisNameID, 1, 0)
            name = nameRecord.toUnicode()
            axes.append(Axis(name, a.minValue, a.defaultValue, a.maxValue, a.axisTag))

        super(TTVarFontDesignSpace, self).__init__(axes)
        self.glyphSet = TTVarFontGlyphSet(ttFont)

    def getGlyphName(self, charCode):
        return self.cmap.get(charCode, ".notdef")

    def getOutline(self, glyphName, location, penFactory):
        pen = penFactory(self.glyphSet)
        self.glyphSet.setLocation(location)
        if glyphName in self.glyphSet:
            varGlyph = self.glyphSet[glyphName]
        else:
            varGlyph = self.glyphSet[".notdef"]
        varGlyph.draw(pen)
        os2 = self.ttFont["OS/2"]
        if hasattr(os2, "sxHeight"):
            xHeight = os2.sxHeight
            capHeight = os2.sCapHeight
        else:
            capHeight = self.ttFont["hhea"].ascent
            xHeight = 0.7 * self.ttFont["hhea"].ascent  # XXX
        centerPoint = (varGlyph.width / 2, xHeight / 2)
        size = capHeight
        return pen, centerPoint, size

if __name__ == "__main__":
    # FIXME: traceback when importing drawingTools.
    # File
    # "/Users/michiel/Code/TnBits/src/tnbits/toolparts/buildvariations/varglyphcell.py",
    # line 7, in <module>
    #      from mojo.drawingTools import *

    class DesignSpaceExplorerTest(object):

        def __init__(self, designSpace, previewCharacter="e"):
            from vanilla import Window
            from tnbits.tools.toolparts.buildvariations.designspaceexplorer import DesignSpaceExplorer
            self.w = Window((1000, 500), "DesignSpace Explorer", minSize=(600, 300))
            self.w.designSpaceExplorer = DesignSpaceExplorer((0, 0, 0, 0), designSpace,
                previewCharacter=previewCharacter)
            self.w.open()

    from tnTestFonts import getFontPath
    p = getFontPath("Noordzij_e_varfont.ttf")
    ds = TTVarFontDesignSpace.fromVarFontPath(p)
    DesignSpaceExplorerTest(ds, "e")
