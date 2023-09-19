#!/usr/bin/python

# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   otfstorage.py
#
import traceback
from fontTools.ufoLib.pointPen import PointToSegmentPen, SegmentToPointPen

try:
    from extractor.formats.opentype import _extractOpenTypeKerningFromGPOS, \
            _extractOpenTypeKerningFromKern
except:
    print('No extractor module founde')

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.O_S_2f_2 import Panose
from tnbits.compilers.f5.ttfTools import getBestCmap
from tnbits.compilers.f5.ttGlyphBuilder import TTGlyphBuilderPen, CubicToQuadFilterPen
from tnbits.model.storage.basestorage import BaseStorage
from tnbits.model.toolbox.pens.pointcollector import PointCollector, drawPointsFromPack
from tnbits.model.storage.packdefinitions import os2SelectionFields
from tnbits.variations.otfvarglyph import OTFVarGlyph

def readOS2Selection(storage, selection):
    """Convert the OS/2 selection bit field into a dictionary.

        >>> d = readOS2Selection(None, 0xff)
        >>> sorted(d)
        ['bold', 'italic', 'negative', 'oblique', 'outlines', 'regular', 'strikeout', 'underscore', 'useTypoMetrics', 'wws']
        >>> any(readOS2Selection(None, 0x0).values())
        False
        >>> all(readOS2Selection(None, 0x3ff).values())
        True
    """
    selDict = {}
    for i, fieldName in enumerate(os2SelectionFields):
        selDict[fieldName] = bool(selection & (0x01 << i))
    return selDict

def writeOS2Selection(storage, selDict):
    """Collapse the OS/2 selection dict into a single integer bit field.

        >>> d = readOS2Selection(None, 0x3ff)
        >>> print(hex(writeOS2Selection(None, d)))
        0x3ff
        >>> for i in range(10):
        ...   v = 0x01 << i
        ...   v2 = writeOS2Selection(None, readOS2Selection(None, v))
        ...   assert v == v2
        ...   v2 = writeOS2Selection(None, readOS2Selection(None, 0x3ff - v))
        ...   assert 0x3ff - v == v2
    """
    selection = 0
    for i, fieldName in enumerate(os2SelectionFields):
        if selDict[fieldName]:
            selection |= 0x01 << i
    return selection

_panoseMapping = [
    # our attr name     # fontTools attr name
    ("familyType",      "bFamilyType"),
    ("serifStyle",      "bSerifStyle"),
    ("weight",          "bWeight"),
    ("proportion",      "bProportion"),
    ("contrast",        "bContrast"),
    ("strokeVariation", "bStrokeVariation"),
    ("armStyle",        "bArmStyle"),
    ("letterForm",      "bLetterForm"),
    ("midline",         "bMidline"),
    ("xHeight",         "bXHeight"),
]

def readPanose(storage, panose):
    panoseDict = {}
    for dst, src in _panoseMapping:
        panoseDict[dst] = getattr(panose, src)
    return panoseDict

def writePanose(storage, panoseDict):
    panose = Panose()
    for dst, src in _panoseMapping:
        setattr(panose, src, panoseDict[dst])
    return panose

def readIsFixedPitch(storage, value):
    return bool(value)

def writeIsFixedPitch(storage, value):
    if value:
        return 1
    else:
        return 0

def readNameEntry(storage, nameID):
    entry = storage._font["name"].getName(nameID, 3, 1)
    if entry is not None:
        #return unicode(entry.string, "utf-16-be", "replace")
        return str(entry.string)
    else:
        # XXX fall back to (0, *) if no (3, 1) data available
        # XXX perhaps even to MacRoman if _that_ isn't there
        return ''

def writeNameEntry(storage, nameID):
    raise NotImplementedError
    #    for index, item in enumerate(self.nameTable.names):
    #        if item.nameID == nameId:
    #            self.nameTable.names[index] = NameRecord(name, nameId)
    #            return
    #    # Otherwise we cannot replace. Add to the table.
    #    self.nameTable.names.append(NameRecord(name, nameId))

OTFINFOMAPPING = dict(
    # TODO: Change these names to match with the real font.info names.
    # tn attr name              OTF table   attr name   read func   write func
    unitsPerEm                  =  ("head", "unitsPerEm", None, None),
    minPPEM                     =  ("head", "lowestRecPPEM", None, None),
    ascender                    =  ("hhea", "ascent", None, None),
    descender                   =  ("hhea", "descent", None, None),
    winAscender                 =  ("OS/2", "usWinAscent", None, None),
    winDescender                =  ("OS/2", "usWinDescent", None, None),
    typoAscender                =  ("OS/2", "sTypoAscender", None, None),
    typoDescender               =  ("OS/2", "sTypoDescender", None, None),
    xHeight                     =  ("OS/2", "sxHeight", None, None),  # XXX will fail for OS/2 table version 0 or 1
    capHeight                   =  ("OS/2", "sCapHeight", None, None),  # XXX will fail for OS/2 table version 0 or 1
    lineGap                     =  ("hhea", "lineGap", None, None),
    typoLineGap                 =  ("OS/2", "sTypoLineGap", None, None),
    italicAngle                 =  ("post", "italicAngle", None, None),
    underlinePosition           =  ("post", "underlinePosition", None, None),
    underlineThickness          =  ("post", "underlineThickness", None, None),
    isFixedPitch                =  ("post", "isFixedPitch", readIsFixedPitch, writeIsFixedPitch),
    widthClass                  =  ("OS/2", "usWidthClass", None, None),
    weightClass                 =  ("OS/2", "usWeightClass", None, None),  # TODO Round weightValue to valid whole-100 number range 100-900
    horizontalCaretOffset       =  ("hhea", "caretOffset", None, None),
    horizontalCaretSlopeRise    =  ("hhea", "caretSlopeRise", None, None),
    horizontalCaretSlopeRun     =  ("hhea", "caretSlopeRun", None, None),
    verticalCaretOffset         =  ("vhea", "caretOffset", None, None),
    verticalCaretSlopeRise      =  ("vhea", "caretSlopeRise", None, None),
    verticalCaretSlopeRun       =  ("vhea", "caretSlopeRun", None, None),
    os2Selection                =  ("OS/2", "fsSelection", readOS2Selection, writeOS2Selection),
    panose                      =  ("OS/2", "panose", readPanose, writePanose),
    vendorID                    =  ("OS/2", "achVendID", None, None),
    familyClass                 =  ("OS/2", "sFamilyClass", None, None),

    subscriptXOffset            =  ("OS/2", "ySubscriptXOffset", None, None),
    subscriptXSize              =  ("OS/2", "ySubscriptXSize", None, None),
    subscriptYOffset            =  ("OS/2", "ySubscriptYOffset", None, None),
    subscriptYSize              =  ("OS/2", "ySubscriptYSize", None, None),
    superscriptXOffset          =  ("OS/2", "ySuperscriptXOffset", None, None),
    superscriptXSize            =  ("OS/2", "ySuperscriptXSize", None, None),
    superscriptYOffset          =  ("OS/2", "ySuperscriptYOffset", None, None),
    superscriptYSize            =  ("OS/2", "ySuperscriptYSize", None, None),
    strikeoutSize               =  ("OS/2", "yStrikeoutSize", None, None),
    strikeoutPosition           =  ("OS/2", "yStrikeoutPosition", None, None),

    averageWidth                =  ("OS/2", "xAvgCharWidth", None, None),

    familyName                  =  ('name',  1, readNameEntry, writeNameEntry),
    styleName                   =  ('name',  2, readNameEntry, writeNameEntry),
    compatibleFullName          =  ('name', 18, readNameEntry, writeNameEntry),
    copyright                   =  ('name',  0, readNameEntry, writeNameEntry),
    trademark                   =  ('name',  7, readNameEntry, writeNameEntry),
    license                     =  ('name', 13, readNameEntry, writeNameEntry),
    licenseUrl                  =  ('name', 14, readNameEntry, writeNameEntry),
    description                 =  ('name', 10, readNameEntry, writeNameEntry),
    sampleText                  =  ('name', 19, readNameEntry, writeNameEntry),
    note                        =  ('name', 10, readNameEntry, writeNameEntry),
    manufacturerName            =  ('name',  8, readNameEntry, writeNameEntry),
    manufacturerUrl             =  ('name', 11, readNameEntry, writeNameEntry),
    designerName                =  ('name',  9, readNameEntry, writeNameEntry),
    designerUrl                 =  ('name', 12, readNameEntry, writeNameEntry),
)

class OTFStorage(BaseStorage):
    """Storage for binary OpenType and TrueType formats. Is used by Style to
    extract information for tools.

    >>> from pprint import pprint
    >>> from tnbits.model.storage.basestorage import getStorage
    >>> from tnTestFonts import getFontPath
    >>> path = getFontPath("Condor-Bold.ufo")
    >>> otfStorage = getStorage(path)
    >>> gp_from_ufo = otfStorage.readGlyphPack("O")
    >>> otfStorage = getStorage(path)
    >>> path = getFontPath("CusterRE-RegularS2.ttf")
    >>> otfStorage = getStorage(path)
    >>> infoPack = otfStorage.readInfoPack()
    >>> infoPack.get('licenseUrl')
    u'http://www.typenetwork.com'
    >>> infoPack.get('capHeight')
    384
    >>> kerningPack = otfStorage.readKerningPack()
    >>> len(kerningPack)
    0
    >>> gp = otfStorage.readGlyphPack("adieresis")
    >>> pprint(gp)
    {'components': [{'baseGlyphName': 'a', 'transformation': (1, 0, 0, 1, 0, 0)},
                    {'baseGlyphName': 'dieresis',
                     'transformation': (1, 0, 0, 1, -4, 0)}],
     'curveType': None,
     'unicodes': [228],
     'width': 320}
    >>> otfStorage.writeGlyphPack("adieresis.alt", gp)
    >>> gp = otfStorage.readGlyphPack("period")
    >>> pprint(gp)
    {'contours': [{'isClosed': True,
                   'points': [{'onCurve': True,
                               'smooth': True,
                               'x': 65,
                               'y': 45},
                              {'x': 65, 'y': 65},
                              {'x': 93, 'y': 94},
                              {'onCurve': True,
                               'smooth': True,
                               'x': 112,
                               'y': 94},
                              {'x': 131, 'y': 94},
                              {'x': 158, 'y': 65},
                              {'onCurve': True,
                               'smooth': True,
                               'x': 158,
                               'y': 45},
                              {'x': 158, 'y': 24},
                              {'x': 131, 'y': -3},
                              {'onCurve': True,
                               'smooth': True,
                               'x': 112,
                               'y': -3},
                              {'x': 93, 'y': -3},
                              {'x': 65, 'y': 24}]}],
     'curveType': 'quadratic',
     'unicodes': [46],
     'width': 224}
     >>> otfStorage.writeGlyphPack("period.alt", gp)
     >>> gp2 = otfStorage.readGlyphPack("period.alt")
     >>> gp == gp2
     True
     >>> otfStorage.writeGlyphPack("O.alt", gp_from_ufo)
    """

    def __init__(self, path):
        """Tests for valid file, then copies glyph set and reversed character map.
        """

        '''
        # TODO: maybe assert path is correct for font if both?
        if font is not None:
            if path is not None:
                raise TypeError("[OTFStorage] Path must be None if a font is given.")
            path = font.path
        else:
        '''
        self._font = TTFont(path)
        self.path = path
        #self._font = font
        self._reverseCmap = self._getReversedCmap()

        try:
            self._glyphSet = self._font.getGlyphSet()
        except Exception as e:
            print(traceback.format_exc())
            print('FIXME: setting glyph set to empty dictionary for %s' % path)
            self._glyphSet = {}

    def getId(self):
        return id(self._font)

    def _getReversedCmap(self):
        """
        Inverted?
        """
        #self.cmap = getBestCmap(ttFont)
        # NOTE: is the (3, 1) assumption too wild?
        cmap = self._font["cmap"].getcmap(3, 1)

        if cmap is not None:
            cmap = cmap.cmap
        else:
            return {}

        reverseCmap = {}
        for unicode, name in cmap.items():
            reverseCmap[name] = unicode
        return reverseCmap

    def getGlyphNames(self):
        return self._font.getGlyphOrder()

    # Reading.

    def getGlyphName(self, charCode):
        return self.cmap.get(charCode, ".notdef")

    def readGlyphPack(self, glyphName):
        """Reads data for a single non-var glyph."""
        pack = {}
        collector = PointCollector()
        pen = SegmentToPointPen(collector)
        glyph = self._glyphSet[glyphName]
        glyph.draw(pen)
        pack["width"] = glyph.width
        pack["curveType"] = collector.curveType

        if collector.contours:
            pack["contours"] = collector.contours

        if collector.components:
            pack["components"] = collector.components
        uni = self._reverseCmap.get(glyphName)

        if uni is not None:
            pack["unicodes"] = [uni]

        return pack

    def isVar(self):
        u"""Checks if this stores a variation font."""
        if 'gvar' in self._font:
            return True
        else:
            return False

    def getOTFVarGlyph(self, glyphName, location):
        return OTFVarGlyph(self._font, glyphName, location)

    def getVarWidth(self, glyphName, location):
        glyph = self.getOTFVarGlyph(glyphName, location)
        return glyph.getVarWidth()

    def getRepresentation(self, glyphName, location, bezierPath):
        """Renders a var outline for a given location to a path."""
        # TODO: offset based on LSB?
        assert 'glyf' in self._font
        assert 'gvar' in self._font

        otfVarGlyph = self.getOTFVarGlyph(glyphName, location)
        otfVarGlyph.draw(bezierPath)
        return bezierPath

    def getVarBounds(self, glyphName, location, parent):
        # NOTE: bounds are none in case of whitespace.
        # TODO: test.
        otfVarGlyph = self.getOTFVarGlyph(glyphName, location)
        from fontTools.pens.boundsPen import BoundsPen
        pen = BoundsPen(parent)
        otfVarGlyph.draw(pen)
        return pen.bounds

    def readAxesPack(self):
        try:
            axes = self._font['fvar'].axes
            axesPack = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in axes}
        except KeyError as e:
            axesPack = {} # This is not a var font.

        return axesPack

    def readInfoPack(self):
        # TODO: compare to extractor _extractOpenTypeInfo results.
        pack = {}
        for name, (otfTable, otfAttrName, readFunc, writeFunc) in OTFINFOMAPPING.items():
            if isinstance(otfAttrName, str):
                if otfTable in self._font:
                    table = self._font[otfTable]
                    value = getattr(table, otfAttrName, None)
                else:
                    # table not available
                    value = None
            else:
                assert readFunc is not None and writeFunc is not None
                value = otfAttrName
            if readFunc is not None and value is not None:
                value = readFunc(self, value)
            pack[name] = value
        return pack

    def readFeaturesPack(self):
        """Reads the feature [GSUB] table, if it exists and try to decompile as
        well as possible."""
        featurePack = {}

        if 'GSUB' in self._font:
            gsub = self._font['GSUB']
            # TODO: Read features Scripts/Languages/Lookups and make them
            # accessable in the pack.
            featurePack['gsub'] = gsub

        return featurePack

    def readKerningPack(self):
        """Reads the [GPOS] or [kern] using extractor.

        NOTE: We need to merge here? How about preserving classes in GPOS?
        NOTE: group names are collected but aren't stored in a pack."""
        kerningPack = {}
        groupsPack = {}
        kerning = {}
        groups = {}

        if "GPOS" in self._font:
            kerning, groups = _extractOpenTypeKerningFromGPOS(self._font)
        elif "kern" in self._font:
            kerning = _extractOpenTypeKerningFromKern(self._font)
            groups = {}

        for pair, value in kerning.items():
            kerningPack[pair] = value

        for name, group in groups.items():
            groupsPack[name] = list(sorted(group))

        return kerningPack, groupsPack

    def readLibPack(self):
        """NOTE: For now there is no storage of RoboFont.lib as table info in TTF
        or OTF table. We can solve this by adding custom tables or by adding a
        font.json file with the information."""
        # TODO implement storage of font.lib.
        return {}

    def readCharacterMapping(self):
        from tnbits.compilers.f5.ttfTools import getBestCmap
        cmap = getBestCmap(self._font)
        for k in cmap:
            # Turns values into lists of glyph names for compatibility: UFO
            # supports multiple glyphs per unicode value.
            cmap[k] = [cmap[k]]
        return cmap

    def readOpenTypeInfo(self):
        return {}
        # {SCRIPTTAG: {LANGUAGETAG: [FEATURETAGS]}}

    #   Writing

    def writeLibPack(self, pack):
        """Ignores writing the lib pack for now."""
        # TODO implement storage of font.lib
        pass

    def writeGlyphPack(self, glyphName, glyphPack):
        if "glyf" in self._font:
            self.writeGlyphPackTT(glyphName, glyphPack)
        else:
            assert "CFF " in self._font
            self.writeGlyphPackCFF(glyphName, glyphPack)

    def writeGlyphPackCFF(self, glyphName, glyphPack):
        # insert glyph in CharStrings
        raise NotImplementedError

    def writeGlyphPackTT(self, glyphName, glyphPack):
        builderPen = TTGlyphBuilderPen()

        if glyphPack.get("curveType") == "cubic":
            # XXX/TODO what precision settings to use for the conversion to quads?
            pointPen = MyPointToSegmentPen(CubicToQuadFilterPen(builderPen))
        else:
            pointPen = MyPointToSegmentPen(builderPen)

        drawPointsFromPack(glyphPack, pointPen)
        glyph = builderPen.buildTTGlyph()
        self._font['glyf'][glyphName] = glyph
        glyph.recalcBounds(self._font['glyf'])
        self._font["hmtx"][glyphName] = glyphPack["width"], glyph.xMin
        unicodes = glyphPack.get("unicodes", [])
        cmap = self._font["cmap"].getcmap(3, 1)  # XXX update *all* supported Unicode cmap subtables

        for uni in unicodes:
            cmap.cmap[uni] = glyphName

        # update our internal reversed cmap
        if unicodes:
            self._reverseCmap[glyphName] = unicodes[0]
        else:
            if glyphName in self._reverseCmap:
                del self._reverseCmap[glyphName]

        # Tables to edit:
        # LTSH
        # VDMX
        # cmap
        # glyf  *
        # hdmx
        # head?
        # hhea?
        # hmtx  *
        # vmtx?
        # post

    def deleteGlyph(self, glyphName):
        # glyf, hmtx
        # delete GPOS/GSUB/GDEF etc refs.
        raise NotImplementedError

class MyPointToSegmentPen(PointToSegmentPen):
    """Workaround for PointToSegmentPen, whose addComponent() doesn't take
    keyword arguments."""

    def addComponent(self, glyphName, transformation, **kwargs):
        self.pen.addComponent(glyphName, transformation, **kwargs)

def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
