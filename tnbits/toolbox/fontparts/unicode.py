# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#from collections import OrderedDict
#import unicodedata
#from fontTools.ttLib import TTFont

from tnbits.toolbox.transformer import TX
from tnbits.toolbox.glyph import GlyphTX
from tnbits.toolbox.fontparts.repertoire import RepertoireTX
from tnbits.constants import Constants as C
from tnbits.base.future import chr

class UnicodeRangeTX:
    """`UnicodeRangeTX` helps access and transform unicode ranges, and provide
    information for the OS/2 table unicode ranges value."""

    @classmethod
    def rangeForUnicode(cls, u):
        """`rangeForUnicode` provides a unicode range for a given decimal
        unicode."""
        uniRanges = []

        for uniRange in C.UNICODE_RANGES.keys():
            min, max = uniRange
            if min <= u < max:
                uniRanges.append(uniRange)

        return uniRanges

    @classmethod
    def unicodesForRange(cls, uniRange):
        """`unicodesForRange` return a range of unicodes for a min, max
        tuple."""
        min, max = uniRange
        return range(min, max)

    @classmethod
    def charsForRange(cls, uniRange):
        return [chr(u) for u in cls.unicodesForRange(uniRange)]

    @classmethod
    def bitForRange(cls, uniRange):
        """`bitForRange` provides a OS/2.ulCodePageRanges bit for a given range
        tuple."""
        if uniRange in C.FONTINFO_OS2_UNICODE_RANGES:
            return C.FONTINFO_OS2_UNICODE_RANGES[uniRange]

    @classmethod
    def rangesForBit(cls, bit):
        """`rangesForBit` provides a all ranges that are covered by a given
        OS/2.ulCodePageRanges bit."""
        uniRanges = []
        for uniRange, b in C.FONTINFO_OS2_UNICODE_RANGES.items():
            if b == bit:
                uniRanges.append(uniRange)
        return uniRanges

    @classmethod
    def nameForRange(cls, uniRange):
        """`nameForRange` is a shortcut to get the name of a unicode range."""
        if uniRange in C.UNICODE_RANGES:
            return C.UNICODE_RANGES[uniRange]

    @classmethod
    def rangeForName(cls, name):
        """`nameForRange` is a shortcut to get the name of a unicode range."""
        for range, compareName in C.UNICODE_RANGES.items():
            if compareName == name:
                return range

    @classmethod
    def getSupport(cls, uniRange, chars):
        """`getSupport` splits a list of unicode _chars_ into those included in
        the _uniRange_ and those that are not."""
        min, max = uniRange
        rangeChars = []
        notRangeChars = []
        for char in chars:
            if min <= char < max:
                rangeChars.append(char)
            else:
                notRangeChars.append(char)
        return rangeChars, notRangeChars

    @classmethod
    def getUnicodeRanges(cls, f, minPresence=1, minProportion=None, DEBUG=False):
        """`getOS2UnicodeRanges`: Given a font _f_, return a tuple of bits for
        ranges that are supported. By default, it only takes one participating
        glyph to be admitted to the tuple. This can be changed by
        _minPresence_, which specifies a minimum number of glyphs, and/or
        _minProportion_, which specifies that participation much reach a
        proportion between 0 and 1."""
        allChars = UnicodeTX.collectFromFont(f)
        supportedUnicodeRanges = []
        for (min, max), bit in C.FONTINFO_OS2_UNICODE_RANGES.items():
            name = cls.nameForRange((min, max))
            rangeChars, notRangeChars = cls.getSupport((min, max), allChars)
            go = True
            if minPresence and len(rangeChars) < minPresence:
                go = False
            if minProportion and len(rangeChars) < len(range(min, max)) * minProportion:
                go = False
            if go:
                if DEBUG:
                    print(name, len(rangeChars), len(range(min, max)))
                if bit not in supportedUnicodeRanges:
                    supportedUnicodeRanges.append(name)
        return supportedUnicodeRanges

    @classmethod
    def getOS2UnicodeRanges(cls, f, minPresence=1, minProportion=None, DEBUG=False):
        """`getOS2UnicodeRanges`: Given a font _f_, return a tuple of bits for
        ranges that are supported. By default, it only takes one participating
        glyph to be admitted to the tuple. This can be changed by
        _minPresence_, which specifies a minimum number of glyphs, and/or
        _minProportion_, which specifies that participation much reach a
        proportion between 0 and 1."""
        allChars = UnicodeTX.collectFromFont(f)
        supportedUnicodeRanges = []
        for (min, max), bit in C.FONTINFO_OS2_UNICODE_RANGES.items():
            name = cls.nameForRange((min, max))
            rangeChars, notRangeChars = cls.getSupport((min, max), allChars)
            go = True
            if minPresence and len(rangeChars) < minPresence:
                go = False
            if minProportion and len(rangeChars) < len(range(min, max)) * minProportion:
                go = False
            if go:
                if DEBUG:
                    print(name, len(rangeChars), len(range(min, max)))
                if bit not in supportedUnicodeRanges:
                    supportedUnicodeRanges.append(bit)
        supportedUnicodeRanges.sort()
        return tuple(supportedUnicodeRanges)

    @classmethod
    def getOS2UnicodeRangesForTTX(cls, os2UnicodeRanges=() ):
        """`getOS2UnicodeRangesForTTX`: Given a font _f_, return two binary
        outputs for os_2 ulUnicodeRange1 and ulUnicodeRange2 that can be pasted
        directly into a TTX file."""
        from ufo2fdk.fontInfoData import intListToNum
        supportedRanges = os2UnicodeRanges
        ulUnicodeRange1 = intListToNum(supportedRanges, 0, 32)
        ulUnicodeRange2 = intListToNum(supportedRanges, 32, 32)
        ulUnicodeRange3 = intListToNum(supportedRanges, 64, 32)
        ulUnicodeRange4 = intListToNum(supportedRanges, 96, 32)
        output1 = TX.formatBinaryForTTX(bin(ulUnicodeRange1))
        output2 = TX.formatBinaryForTTX(bin(ulUnicodeRange2))
        output3 = TX.formatBinaryForTTX(bin(ulUnicodeRange3))
        output4 = TX.formatBinaryForTTX(bin(ulUnicodeRange4))
        return output1, output2, output3, output4

class BaseUnicodeMap:
    """`BaseUnicodeMap`: Maps unicode values to glyph names using the FB Glyph
    List."""

    @classmethod
    def unicodesForGlyphName(cls, target):
        """`unicodesForGlyphName`: Get all unicodes that match a glyph name."""
        u = cls.mapGlyphNamesToUnicode().get(target)
        if u is not None:
            return sorted(u)
        # OBSOLETE (SLOW) method. mapGlyphNamesToUnicode is better with reversed mapping in cache.
        #source = cls.mapUnicodeToGlyphNames()
        #result = []
        #for uni, glyphNames in source.items():
        #    if target in glyphNames:
        #        result.append(uni)
        #result.sort()
        #return result
        return []

    @classmethod
    def primaryUnicodeForGlyphName(cls, target, index=0):
        """`primaryUnicodeForGlyphName`: Get the primary unicode codepoint
        associated with the given glyphName. (Not to be confused with the
        following, plural method that returns a list.)"""
        u = cls.mapGlyphNamesToUnicode().get(target)
        if u is not None:
            return u[0]
        # OBSOLETE (SLOW) method. mapGlyphNamesToUnicode is better with reversed mapping in cache.
        #source = cls.mapUnicodeToGlyphNames()
        #checked = 0  # keep track of whether any items were checked
        #for uni, glyphNames in source.items():
        #    if len(glyphNames) > index:  # so we don't get an index-out-of-range error
        #        checked += 1  # keep track of whether any items were checked
        #        if glyphNames[index] == target:
        #            return uni  # when we find a match, we're done
        # As long as there were items checked, and if no match yet, then recurse with an incremented index
        #if checked > 1:
        #    index +=1
        #    return cls.primaryUnicodeForGlyphName(target, index=index)

        # If nothing left to check in the FBGL, then see if the name is a "uni" name
        elif "uni" in target:
            return GlyphTX.name.getUnicodeSequence(target)
        # If all else fails, return empty string (under some circumstances returning None can result in a _set_unicodes iterable error)
        else:
            return ''

    @classmethod
    def primaryUnicodesForGlyphName(cls, target):
        """`primaryUnicodesForGlyphName`: Get all unicodes for which the given
        glyphName is the primary match."""
        u = cls.mapGlyphNamesToUnicode().get(target)
        if u is not None:
            return u
        # OBSOLETE (SLOW) method. mapGlyphNamesToUnicode is better with reversed mapping in cache.
        #source = cls.mapUnicodeToGlyphNames()
        #result = []
        #for uni, glyphNames in source.items():
        #    if target == glyphNames[0]:
        #        result.append(uni)
        #return result
        return []

    @classmethod
    def alternateUnicodesForGlyphName(cls, target):
        """`alternateUnicodesForGlyphName`: Get all unicodes for which the
        given glyphName is a match, but not the primary match."""
        u = cls.mapGlyphNamesToUnicode().get(target)
        if u is not None and len(u) > 1:
            return u[1:]
        # OBSOLETE (SLOW) method. mapGlyphNamesToUnicode is better with reversed mapping in cache.
        #source = cls.mapUnicodeToGlyphNames()
        #result = []
        #for uni, glyphNames in source.items():
        #    if len(glyphNames) > 1 and target in glyphNames[1:]:
        #        result.append(uni)
        #return result
        return []

    @classmethod
    def glyphNameForUnicode(cls, u):
        """`glyphNameForUnicode`: Get the primary glyphName from FBGL for a
        given unicode value."""
        if isinstance(u, str):
            u = TX.hex2dec(u)
        source = cls.mapUnicodeToGlyphNames()
        if u in source:
            return source[u][0]

    @classmethod
    def strictGlyphNameForUnicode(cls, u):
        """`strictGlyphNameForUnicode`: Get the primary glyphName from the
        AGLFN for a given unicode value, else return the uniXXXX name."""
        if isinstance(u, str):
            u = TX.hex2dec(u)
        source = TX.reverseDict(C.AGLFN)
        if u in source:
            return source[u]
        else:
            return GlyphTX.name.getUnicodeName(u)

    @classmethod
    def allGlyphNamesForUnicode(cls, u):
        """`allGlyphNamesForUnicode`: Get all possible glyph names from FBGL
        for a given unicode value."""
        if isinstance(u, str):
            u = TX.hex2dec(u)
        source = cls.mapUnicodeToGlyphNames()
        if u in source:
            return source[u]

    @classmethod
    def alternateGlyphNamesForUnicode(cls, u):
        """`alternateGlyphNamesForUnicode`: Get all alternate (non-primary)
        glyph names for a given unicode value."""
        if isinstance(u, str):
            u = TX.hex2dec(u)
        source = cls.mapUnicodeToGlyphNames()
        if u in source and len(source[u]) > 1:
            return source[u][1:]

    # interaction

    @classmethod
    def removeExistingUnicodes(cls, unicodeList, target, map={}):
        """`removeExistingUnicodes`: Remove any unicodes in _unicodeList_ that
        already exist in _map_, excepting the _target_ glyph."""
        for glyphName, sourceUnicodeList in map.items():
            if glyphName != target:
                for sourceUnicode in sourceUnicodeList:
                    if sourceUnicode in unicodeList:
                        unicodeList.remove(sourceUnicode)
        return unicodeList

    @classmethod
    def getUnicodeNameUnicodes(cls, glyphNames, map=None, allowDuplicates=False):
        """`getUnicodeNameUnicodes`: Map glyph names to unicodes for all glyph
        names whose unicode value is expressed in its name (uniXXXX or uXXXXX)."""
        if map is None:
            map = {}
        for gname in glyphNames:
            unicodeList = GlyphTX.name.getUnicodeSequence(gname)
            if unicodeList:
                if not allowDuplicates:
                    unicodeList = cls.removeExistingUnicodes(unicodeList, gname, map)
                if unicodeList:
                    if gname in map:
                        map[gname] = TX.makeUniqueList(map[gname] + unicodeList)
                    else:
                        map[gname] = TX.makeUniqueList(unicodeList)
        return map

    @classmethod
    def getPrimaryNameUnicodes(cls, glyphNames, map=None, allowDuplicates=False):
        """`getPrimaryNameUnicodes`: Map glyph names to unicodes for all glyph
        names which are the primary name for a unicode."""
        if map is None:
            map = {}
        for gname in glyphNames:
            unicodeList = cls.primaryUnicodesForGlyphName(gname)
            if unicodeList:
                if not allowDuplicates:
                    unicodeList = cls.removeExistingUnicodes(unicodeList, gname, map)
                if unicodeList:
                    if gname in map:
                        map[gname] = TX.makeUniqueList(map[gname] + unicodeList)
                    else:
                        map[gname] = TX.makeUniqueList(unicodeList)
        return map

    @classmethod
    def getAlternateNameUnicodes(cls, glyphNames, map={}, allowDuplicates=False):
        """`getAlternateNameUnicodes`: Map glyph names to unicodes for all
        glyph names which are the alternate name for a unicode. This is done as
        a separate step so that primary names are assigned first, and alternate
        name are only assigned if the primary glyph doesn't exist."""
        if map is None:
            map = {}
        for gname in glyphNames:
            unicodeList = cls.alternateUnicodesForGlyphName(gname)
            if unicodeList:
                if not allowDuplicates:
                    unicodeList = cls.removeExistingUnicodes(unicodeList, gname, map)
                if unicodeList:
                    if gname in map:
                        map[gname] = TX.makeUniqueList(map[gname] + unicodeList)
                    else:
                        map[gname] = TX.makeUniqueList(unicodeList)
        return map

    # font transformations

    @classmethod
    def clearUnicodes(cls, f):
        """`clearUnicodes`: Clear all unicodes in the given font."""
        for g in f:
            g.unicodes = []

    @classmethod
    def getUnicodeAssignmentMap(cls, f, clear=True, allowDuplicates=False):
        """`getUnicodeAssignmentMap`: Given a font, return a dictionary of
        glyphName: [unicode, unicode] that can be assigned to the font."""
        map = {}
        if clear:
            cls.clearUnicodes(f)
        else:
            for g in f:
                map[g.name] = g.unicodes
        glyphNames = f.keys()
        # first get all the unicodes from glyphs with uniXXXX or uXXXXX names.
        cls.getUnicodeNameUnicodes(glyphNames, map, allowDuplicates=False)
        # then get all unicodes for glyphs that are the primary glyph name for
        # that unicode value
        cls.getPrimaryNameUnicodes(glyphNames, map, allowDuplicates=False)
        # then get all unicodes for glyphs that are alternative glyph name for
        # that unicode value
        cls.getAlternateNameUnicodes(glyphNames, map, allowDuplicates=False)
        return map

    @classmethod
    def set(cls, f, clear=True, allowDuplicates=False):
        """`setUnicodes`: Given a font, assign unicodes to this font."""
        map = cls.getUnicodeAssignmentMap(f, clear=clear, allowDuplicates=allowDuplicates)
        for gname, unicodeList in map.items():
            if gname in f:
                f[gname].unicodes = unicodeList

    @classmethod
    def setPUAForUnencoded(cls, f, start=983040):
        u = start
        glyphOrder = f.lib.get('public.glyphOrder')
        if glyphOrder:
            allGlyphsInOrder = ( set(f.glyphOrder) - set(f.keys()) ) + ( set( sorted( f.keys() ) ) - set(f.glyphOrder) )
        else:
            allGlyphsInOrder = sorted(f.keys())
        for gname in allGlyphsInOrder:
            g = f[gname]
            if not g.unicodes:
                g.unicodes = [u]
                u+=1


class UnicodeMap(BaseUnicodeMap):
    """`UnicodeMap`: Maps unicode values to glyph names using the FB Glyph
    List."""

    unicodeToGlyphNames = C.CMAP_FBGLYPHLIST

    @classmethod
    def mapUnicodeToGlyphNames(cls):
        return cls.unicodeToGlyphNames

    glyphNamesToUnicode = C.CMAP_FBUNICODELIST

    @classmethod
    def mapGlyphNamesToUnicode(cls):
        return cls.glyphNamesToUnicode

class UnicodeTX(UnicodeRangeTX, UnicodeMap):
    """`UnicodeTX` covers transformations that aren't in Defcon unicodeData."""

    """
    Unicode transformations.
    """

    @classmethod
    def getLowerFromUpper(cls, g):
        """
        Given a lowercase glyph, get the corresponding uppercase glyph in the font.
        """
        f = g.getParent()
        suffix = GlyphTX.name.getSuffix(g.name)
        unicodeData = cls.getUnicodeData(g.getParent())
        ucUnicode = unicodeData.pseudoUnicodeForGlyphName(g.name)
        d = C.UNICODE_UPPER_TO_SINGLE_LOWER
        if ucUnicode and ucUnicode in d:
            lcUnicode = d[ucUnicode]
            lcGname = unicodeData.glyphNameForUnicode(lcUnicode)
            if lcGname and suffix:
                lcGname = GlyphTX.name.join(lcGname, suffix)
            if lcGname and lcGname in f:
                return f[lcGname]
            else:
                return None
        else:
            return None

    @classmethod
    def getUpperFromLower(cls, g):
        """Given an uppercase glyph, get the corresponding lowercase glyph in
        the font."""
        f = g.getParent()
        suffix = GlyphTX.name.getSuffix(g.name)
        unicodeData = cls.getUnicodeData(f)
        lcUnicode = unicodeData.pseudoUnicodeForGlyphName(g.name)
        d = C.UNICODE_LOWER_TO_SINGLE_UPPER
        if lcUnicode and lcUnicode in d:
            ucUnicode = d[lcUnicode]
            ucGname = unicodeData.glyphNameForUnicode(ucUnicode)
            if ucGname in f and suffix:
                ucGname = GlyphTX.name.join(ucGname, suffix)
            if ucGname in f and ucGname in f:
                return f[ucGname]
            else:
                return None
        else:
            return None

    @classmethod
    def collectFromFont(cls, f):
        """`collectFromFont` returns all unicode values from a font."""
        unicodes = []
        for g in f:
            for u in g.unicodes:
                if u not in unicodes:
                    unicodes.append(u)
        return unicodes

    @classmethod
    def mapUnicodeToGlyphName(cls, f):
        """`collectFromFont` returns a dictionary of unicode values to glyph
        names. Identical to `RFont.getCharacterMapping()`."""
        unicodes = {}
        for g in f:
            for u in g.unicodes:
                if u in unicodes:
                    unicodes[u].append(g.name)
                else:
                    unicodes[u] = [g.name]

    @classmethod
    def checkForDuplicates(cls, f):
        """`checkForDuplicates` finds any duplicate unicode values within a
        font."""
        #map unicodes to glyph names
        unicodeToGlyphName = cls.mapUnicodeToGlyphName(f)
        # get duplicates
        duplicates = {}
        for u, gnames in unicodeToGlyphName.items():
            if len(gnames) <= 1:
                duplicates[u] = gnames
        return duplicates

    @classmethod
    def strictGlyphNameRename(cls, f):
        for g in f:
            baseNameElements, suffixElements = GlyphTX.name.splitIntoElements(g.name)
            for i, baseNameElement in enumerate(baseNameElements):
                elementUnicode = cls.unicodesForGlyphName(baseNameElement) #KL Edit
                if not elementUnicode:
                    print('Strict Rename: error invalid base name element', g.name, baseNameElement)
                else:
                    newBaseNameElement = cls.strictGlyphNameForUnicode(elementUnicode[0]) #KLEdit
                    baseNameElements[i] = newBaseNameElement
            newGname = GlyphTX.name.join(baseNameElements, suffixElements)
            RepertoireTX.renameGlyphAndReferences(g.name, newGname, f)

    @classmethod
    def split(cls, f, skipGlyphs=[]):
        """Detect glyphs with multiple unicode values, and create duplicate
        versions for each."""
        for g in f:
            if len(g.unicodes) > 1 and g.name not in skipGlyphs:
                for u in g.unicodes[1:]:
                    newGname = cls.strictGlyphNameForUnicode(u)
                    if newGname in f:
                        newGname = GlyphTX.name.getUnicodeName(u)
                    RepertoireTX.duplicateGlyphAndReferences(g.name, newGname, f)
                    f[newGname].unicodes = [u]
                g.unicodes = [g.unicodes[0]]

    @classmethod
    def getUnicodeData(cls, f):
        if hasattr(f, 'naked'):
            return f.naked().unicodeData
        else:
            return f.unicodeData

    @classmethod
    def cmapDuplicate(cls, ttfont, duplicateMap, DEBUG=False):
        if 'cmap' in ttfont:
            for table in ttfont['cmap'].tables:
                if table.format == 4:
                    for u, gname in duplicateMap.items():
                        table.cmap[u] = gname
                        if DEBUG: print('cmap duplicate 4', u, gname)
                if ( table.format == 6 or table.format == 0 ) and table.platformID == 1 and table.platEncID == 0 and table.language == 0:
                    for p, u in C.CODEPAGE_MAC_ROMAN_POSITIONS.items():
                        if u in duplicateMap:
                            table.cmap[p] = duplicateMap[u]
                            if DEBUG: print('cmap duplicate', table.format, p, u)

if __name__ == "__main__":
    print(UnicodeTX.primaryUnicodeForGlyphName('quoteleft'))
    print(UnicodeTX.primaryUnicodeForGlyphName('commaturnedmod'))
    print(UnicodeTX.primaryUnicodeForGlyphName('okina'))
    print(UnicodeTX.primaryUnicodeForGlyphName('afii61352'))
    print(UnicodeTX.primaryUnicodeForGlyphName('nonsense'))
