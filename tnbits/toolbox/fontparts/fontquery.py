# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
class FontQuery(object):

    CURVE_TEST_GLYPHS = 'OoCcDd'
    @classmethod
    def isBezierFont(cls, f):
        for glyphName in cls.CURVE_TEST_GLYPHS:
            if glyphName in f:
                glyph = f[glyphName]
                return glyph.naked().hasBezierCurves
        return False

    @classmethod
    def isQuadraticFont(cls, f):
        for glyphName in cls.CURVE_TEST_GLYPHS:
            if glyphName in f:
                glyph = f[glyphName]
                return glyph.naked().hasSplinesCurves
        return False
