# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     ufostorage.py
#
#     DEPRECATED: using fontParts RFont for all UFO's.

import traceback
from fontTools.ufoLib import UFOReader
from defcon import Font as DefConFont
from tnbits.model.storage.basestorage import BaseStorage
from tnbits.model.storage.packdefinitions import os2SelectionFields
from tnbits.model.toolbox.pens.pointcollector import PointCollector

def readOS2Selection(storage, selection):
    """
        >>> readOS2Selection(None, [1, 4, 8])
        {'useTypoMetrics': False, 'strikeout': True, 'bold': False, 'wws': True, 'oblique': False, 'negative': False, 'italic': False, 'underscore': True, 'outlines': False, 'regular': False}
    """
    selDict = {}
    selection = set(selection)

    for i, fieldName in enumerate(os2SelectionFields):
        selDict[fieldName] = bool(i in selection)
    return selDict

def writeOS2Selection(storage, selDict):
    """
        >>> d = readOS2Selection(None, [1, 4, 8])
        >>> writeOS2Selection(None, d)
        [1, 4, 8]
    """
    selection = []
    for i, fieldName in enumerate(os2SelectionFields):
        if selDict[fieldName]:
            selection.append(i)
    return selection


_panoseKeys = [
    "familyType",
    "serifStyle",
    "weight",
    "proportion",
    "contrast",
    "strokeVariation",
    "armStyle",
    "letterForm",
    "midline",
    "xHeight"
]

def readPanose(storage, panose):
    """Convert panose tuple into a dictionary.

        >>> readPanose(None, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        {'weight': 0, 'proportion': 0, 'letterForm': 0, 'familyType': 0, 'xHeight': 0, 'serifStyle': 0, 'strokeVariation': 0, 'armStyle': 0, 'contrast': 0, 'midline': 0}
        >>> any(readPanose(None, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)).values())
        False
        >>> all(readPanose(None, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)).values())
        True
    """
    if panose is None:
        panose = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    panoseDict = {}
    for i, key in enumerate(_panoseKeys):
        panoseDict[key] = panose[i]
    return panoseDict

def writePanose(storage, panoseDict):
    """Convert panose dictionary into a tuple with booleans.

        >>> d = readPanose(None, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        >>> writePanose(None, d)
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        >>> d = readPanose(None, (1, 0, 0, 0, 0, 1, 0, 0, 0, 0))
        >>> writePanose(None, d)
        (1, 0, 0, 0, 0, 1, 0, 0, 0, 0)
        >>> for i in range(10):
        ...   p = [0] * 10
        ...   p[i] = 1
        ...   p = tuple(p)
        ...   d = readPanose(None, p)
        ...   assert writePanose(None, d) == p
    """
    panose = []
    for key in _panoseKeys:
        panose.append(panoseDict[key])
    return tuple(panose)


UFOINFOMAPPING = dict(
    familyName              =  ("familyName", None, None),
    styleName               =  ("styleName", None, None),
    familyClass             =  ("openTypeOS2FamilyClass", None, None),

    #   M E T R I C S

    unitsPerEm              =  ("unitsPerEm", None, None),
    minPPEM                 =  ("openTypeHeadLowestRecPPEM", None, None),
    ascender                =  ("ascender", None, None),
    descender               =  (("descender", "openTypeHheaDescender"), None, None),
    winAscender             =  ("openTypeOS2WinAscent", None, None),
    winDescender            =  ("openTypeOS2WinDescent", None, None),
    typoAscender            =  ("openTypeOS2TypoAscender", None, None),
    typoDescender           =  ("openTypeOS2TypoDescender", None, None),
    xHeight                 =  ("xHeight", None, None),
    capHeight               =  ("capHeight", None, None),
    widthClass              =  ("openTypeOS2WidthClass", None, None),
    weightClass             =  ("openTypeOS2WeightClass", None, None),
    lineGap                 =  ("openTypeHheaLineGap", None, None),
    typoLineGap             =  ("openTypeOS2TypoLineGap", None, None),
    averageWidth            =  (None, None, None),  # Does not exist in UFO
    italicAngle             =  (("italicAngle", "postscriptSlantAngle"), None, None),
    underlinePosition       =  ("postscriptUnderlinePosition", None, None),
    underlineThickness      =  ("postscriptUnderlineThickness", None, None),
    isFixedPitch            =  ("postscriptIsFixedPitch", None, None),
    caretOffset             =  ("openTypeHheaCaretOffset", None, None),
    caretSlopeRise          =  ("openTypeHheaCaretSlopeRise", None, None),
    caretSlopeRun           =  ("openTypeHheaCaretSlopeRun", None, None),
    verticalCaretOffset     =  ("openTypeVheaCaretOffset", None, None),
    verticalCaretSlopeRise  =  ("openTypeVheaCaretSlopeRise", None, None),
    verticalCaretSlopeRun   =  ("openTypeVheaCaretSlopeRun", None, None),
    os2Selection            =  ("openTypeOS2Selection", readOS2Selection, writeOS2Selection),
    panose                  =  ("openTypeOS2Panose", readPanose, writePanose),

    subscriptXOffset        =  ("openTypeOS2SubscriptXOffset", None, None),
    subscriptXSize          =  ("openTypeOS2SubscriptXSize", None, None),
    subscriptYOffset        =  ("openTypeOS2SubscriptYOffset", None, None),
    subscriptYSize          =  ("openTypeOS2SubscriptYSize", None, None),

    superscriptXOffset      =  ("openTypeOS2SuperscriptXOffset", None, None),
    superscriptXSize        =  ("openTypeOS2SuperscriptXSize", None, None),
    superscriptYOffset      =  ("openTypeOS2SuperscriptYOffset", None, None),
    superscriptYSize        =  ("openTypeOS2SuperscriptYSize", None, None),

    strikeoutSize           =  ("openTypeOS2StrikeoutSize", None, None),
    strikeoutPosition       =  ("openTypeOS2StrikeoutPosition", None, None),

    #   N A M E S

    compatibleFullName      =  ("openTypeNameCompatibleFullName", None, None),
    manufacturerName        =  ("openTypeNameManufacturer", None, None),
    manufacturerUrl         =  ("openTypeNameManufacturerURL", None, None),
    vendorID                =  ("openTypeOS2VendorID", None, None),
    designerName            =  ("openTypeNameDesigner", None, None),
    designerUrl             =  ("openTypeNameDesignerURL", None, None),
    copyright               =  ("copyright", None, None),
    trademark               =  ("trademark", None, None),
    license                 =  ("openTypeNameLicense", None, None),
    licenseUrl              =  ("openTypeNameLicenseURL", None, None),
    description             =  ("openTypeNameDescription", None, None),
    sampleText              =  ("openTypeNameSampleText", None, None),
    note                    =  ("note", None, None),

    horizontalCaretOffset   =  ("openTypeHheaCaretOffset", None, None),
    horizontalCaretSlopeRise=  ("openTypeHheaCaretSlopeRise", None, None),
    horizontalCaretSlopeRun =  ("openTypeHheaCaretSlopeRun", None, None),
)

class UFOStorage(BaseStorage):

    def __init__(self, path):
        self._font = DefConFont(path)
        self.path = path
        self._reader = UFOReader(path)
        self._glyphSet = self._reader.getGlyphSet()
        self._info = DumbInfo()
        self._reader.readInfo(self._info)

    def __getattr__(self, name):
        return getattr(self._info, name, None)

    def getGlyphNames(self):
        return sorted(self._glyphSet.keys())

    def _get_lib(self):
        if self._font.lib is None:
            self._font.lib = {}
        return self._font.lib

    lib = property(_get_lib)

    def _readInfoPack(self):
        pack = self._getInfoPack()
        return pack

    def _getInfoPack(self, definitions=None):
        pack = {}
        for key in definitions or UFOINFOMAPPING.keys():
            ufoMapping = UFOINFOMAPPING.get(key)
            if ufoMapping is None:
                # missing mapping
                continue
            ufoAttrName, readFunc, writeFunc = ufoMapping
            if isinstance(ufoAttrName, tuple):
                ufoAttrName = ufoAttrName[0]
            if ufoAttrName is None:
                # This value is not supported by UFO
                value = None
            else:
                value = getattr(self._info, ufoAttrName, None)
                if readFunc is not None and value is not None:
                    value = readFunc(self, value)
            pack[key] = value
        return pack

    def readGlyphPack(self, glyphName):
        """Reads data for a single glyph."""
        # FIXME: missing width for component glyphs?
        # FIXME: problem with unicode references?
        pack = {}
        glyph = DumbGlyph()
        collector = PointCollector()

        try:
            self._glyphSet.readGlyph(glyphName, glyph, collector)
        except Exception as e:
            print('Error while reading glyph %s' % glyphName)
            print(e)
            print(traceback.format_exc())

        collector.filterAnchors() # Filter the anchors from the contours.

        try:
            pack["glyphName"] = glyphName

            # FIXME: sometimes width or curveType are missing.
            if hasattr(glyph, 'width'):
                pack["width"] = glyph.width

            if hasattr(glyph, 'curveType'):
                pack["curveType"] = collector.curveType

            if collector.contours:
                pack["contours"] = collector.contours

            if collector.components:
                pack["components"] = collector.components

            if collector.anchors:
                pack["anchors"] = collector.anchors

            if hasattr(glyph, "unicodes"):
                pack["unicodes"] = glyph.unicodes

            if hasattr(glyph, "note"):
                pack["note"] = glyph.note

            if hasattr(glyph, "lib"):
                lib = glyph.lib
                if glyph.lib is None:
                    glyph.lib = {}
                pack["lib"] = glyph.lib

        except Exception as e:
            print('Error in glyph pack %s' % glyphName)
            print(e)
            print(traceback.format_exc())

        return pack

    def readLibPack(self):
        """"""
        return self._font.lib

    def readFeaturesPack(self):
        return self._font.features

    def readKerningPack(self):
        return self._font.kerning, self._font.groups

    def readAxesPack(self):
        return {}

    def readCharacterMapping(self):
        return

class DumbGlyph(object):
    # to gather the attributes readGlyph is setting
    pass

class DumbInfo(object):
    # to gather the attributes readInfo is setting
    pass

def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
