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
#     otfglyphset.py
#
# FIXME: DEPRECATED
from fontTools.varLib.models import normalizeLocation
from tnbits.variations.otfglyph import OTFGlyph

class OTFGlyphSet(object):
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
        return OTFGlyph(self._ttFont, glyphName, self.location)

    def get(self, glyphName, default=None):
        try:
            return self[glyphName]
        except KeyError:
            return default
