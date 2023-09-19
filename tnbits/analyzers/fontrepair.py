# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    A CERTIFICATE TO JILL
#
#    This is an initial sketch class to make a tool that shows if a font meets
#    certain standard of quality, before it is passed to the next phase
#    in the production process.
#
#    Glyph scale repairs:
#
#    Interpolatability (like Prepolator) - ?
#         Contour Order - FBfabWrapperGlyph.autoContourOrder()
#         Path Direction - FBfabWrapperGlyph.correctDirection()
#    Point Smoothness - @@@@@
#    Open Contours - @@@@
#    Double points - ?
#    Double components - ?
#    Sort components - tnbits.toolbox.GlyphTX.component.sortByHeight()
#    Round coordinates to nearest integer - ?
#
#    Check if fontinfo metrics values are same as certain glyphs (GlyphAnalyzer detection)
#
#    Font-scale:
#    Check glyph names according to path and landing patterns 
#    Repertoire check
#
#    Spacing
#        Table figures...are they actually tabular?
#        Consistency of similar/identical side shapes. @@@@@@@@@
#         dimensions stuff...
#
#    Clean References: 
#        Kerning: tnbits.toolbox.font.FontTX.kerning.clean()
#        Groups: tnbits.toolbox.font.FontTX.groups.clean()
#        Features: check for glyph presence in groups.........
#
class FontRepair(object):
    # The FontRepair takes a font (UFO, TrueTypeFont?) and repairs
    # all values that are obviously wrong. It is a safe run, as it never
    # will overwrite deliberate changes to the standard, unless forced
    # to do so.

    @classmethod
    def repair(cls, font):
        # To be developed
        cls.repairInfo(font)
        cls.repairKerning(font)
        cls.repairFeatures(font)
        for glyph in font:
            cls.repairGlyph(glyph)

    @classmethod
    def repairInfo(cls, font):
        # to be developed
        pass

    @classmethod
    def repairKerning(cls, font):
        # to be developed
        pass

    @classmethod
    def repairFeatures(cls, font):
        # to be developed
        pass

    @classmethod
    def repairGlyph(cls, glyph):
        # to be developed
        pass

