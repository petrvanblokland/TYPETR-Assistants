# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.toolbox.fontparts.repertoire import RepertoireTX
from tnbits.toolbox.fontparts.fontinfo import FontInfoTX
from tnbits.toolbox.fontparts.groups import GroupsTX
from tnbits.toolbox.fontparts.kerning import KerningTX
from tnbits.toolbox.fontparts.glyphorder import GlyphOrderTX
from tnbits.toolbox.fontparts.unicode import UnicodeTX
from tnbits.toolbox.fontparts.codepage import CodepageTX
from tnbits.toolbox.fontparts.features import FeaturesTX
from tnbits.toolbox.fontparts.collection import CollectionTX
from tnbits.toolbox.fontparts.compile import CompileTX
#from tnbits.toolbox.fontparts.fontquery import FontQuery
from tnbits.toolbox.fontparts.hinting import HintingTX

class FontTX:
    glyphs = RepertoireTX
    kerning = KerningTX
    groups = GroupsTX
    info = FontInfoTX
    sort = GlyphOrderTX
    unicodes = UnicodeTX
    codepages = CodepageTX
    features = FeaturesTX
    collection = CollectionTX
    compile = CompileTX
    hinting = HintingTX

    @classmethod
    def scale(cls, f, multiplier=(1, 1),
              scaleGlyphs=True,
              scaleComponentOffset=True,
              scaleComponent=False,
              scaleKerning=True,
              scaleInfo=True,
              scaleHints=False,
              ):
        # if multiplier can't be iterated, make it a tuple
        try:
            for x in multiplier:
                pass
        except:
            multiplier = (multiplier, multiplier)
        # scale glyphs
        if scaleGlyphs:
            for g in f:
                g.scale(multiplier)
                # scale component offsets
                for c in g.components:
                    if scaleComponentOffset:
                        c.offset = c.offset[0]*multiplier[0], c.offset[1]*multiplier[1]
                    if scaleComponent:
                        c.scale = c.scale[0]*multiplier[0], c.scale[1]*multiplier[1]
                # scale set width
                g.width = g.width * multiplier[0]
        # scale kerning
        if scaleKerning:
            for pair, value in f.kerning.items():
                f.kerning[pair] = value * multiplier[0]
        if scaleInfo:
            # scale font info
            cls.info.scale(f.info, multiplier)
        if scaleHints:
            print('Unable to scale hints.')

    @classmethod
    def setSlug(cls, f, gname, components, tracking=0, kerning=True, decompose=False, clear=True):
        """Generates composite."""
        if not gname in f:
            f.newGlyph(gname)
        if clear:
            f[gname].clear()
        pairs = f.kerning.asDict()
        groups = f.groups
        left = f[components[0]].leftMargin
        right = f[components[-1]].rightMargin
        tick = 0
        xoffset = 0
        for component in components:
            if component in f:
                xoffset = xoffset + round(tracking/2)
                kern = 0
                if (tick+1) < len(components) and kerning is True:
                    nextComponent = components[tick+1]
                    kern = cls.kerning.getValue((component, nextComponent), pairs, groups)
                if f[component].components != []:
                    for c in f[component].components:
                        f[gname].appendComponent(c.baseGlyph, (c.offset[0]+xoffset, c.offset[1]), c.scale)
                    for contour in f[component].contours:
                        contourCopy = contour.copy()
                        contourCopy.move((xoffset, 0))
                        f[gname].appendContour(contourCopy)
                else:
                    f[gname].appendComponent(component,(xoffset,0))
                xoffset = xoffset + f[component].width + kern + round(tracking/2)
            else:
                print('Skipping component', component, 'in', str(f) +'. Glyph does not exist.')
            tick = tick + 1
        # set sidebearings
        f[gname].leftMargin = left + tracking/2
        f[gname].rightMargin = right + tracking/2
        if decompose:
            f[gname].decompose()
