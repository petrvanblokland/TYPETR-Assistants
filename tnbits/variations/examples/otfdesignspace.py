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
#     otfdesignspace.py
#
# FIXME: DEPRECATED

from fontTools.ttLib import TTFont
from tnbits.variations.designspacemodel import DesignSpaceBase, Axis
from tnbits.variations.otfglyphset import OTFGlyphSet
from tnbits.compilers.f5.ttfTools import getBestCmap

class OTFDesignSpace(DesignSpaceBase):

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

        super(OTFDesignSpace, self).__init__(axes)
        self.glyphSet = OTFGlyphSet(ttFont)

    '''
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

    @classmethod
    def fromVarFontPath(cls, path):
        ttFont = TTFont(path, lazy=True)
        return cls(ttFont)
    '''

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
    ds = OTFDesignSpace.fromVarFontPath(p)
    DesignSpaceExplorerTest(ds, "e")
