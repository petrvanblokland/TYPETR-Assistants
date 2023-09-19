# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    fontinfo.py
#
from __future__ import division, print_function
import os
import string
from random import choice
import tempfile
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._n_a_m_e import NameRecord

#Original import: from fontTools.ttLib.xmlImport import importXML
from tnbits.toolbox.parsers.xmlImport import importXML

from tnbits.constants import Constants as C
from tnbits.toolbox.mathematics import M
from tnbits.toolbox.fontparts.codepage import CodepageTX
from tnbits.toolbox.fontparts.unicode import UnicodeTX
from tnbits.model.objects.utils import getCharacterMapping

class TTFontNameRecord(NameRecord):
    """This is is a custom name record to take care of the bug/issue where it
    will write windows namerecord strings weirdly (as chinese characters or
    other stuff)."""
    def toXML(self, writer, ttFont):
        writer.begintag("namerecord", [
                ("nameID", self.nameID),
                ("platformID", self.platformID),
                ("platEncID", self.platEncID),
                ("langID", hex(self.langID)),
                        ])
        writer.newline()
        if self.platformID == 0 or (self.platformID == 3 and self.platEncID in (0, 1)):
            if len(self.string) % 2:
                # no, shouldn't happen, but some of the Apple
                # tools cause this anyway :-(
                ######
                #writer.write(self.string + "\0")
                writer.write(self.string)
                ######
            else:
                # DO NOT ENCODE THIS. JUST WRITE THE STRING.
                ######
                writer.write(self.string)
                ######
        else:
            writer.write8bit(self.string)
        writer.newline()
        writer.endtag("namerecord")
        writer.newline()

class TTFontNameTableTX:
    """
    Some special methods for hackishly setting font info stuff in TTX.
    """

    @classmethod
    def setTTFontNameTable(cls, ttfont, records):
        """
        This creates a new table. Has this been tested? !!!
        """
        ttfont['name'] = name = newTable('name')
        name.names = []
        for record in records:
            name.names.append(cls.createTTFontNameRecord(record))

    @classmethod
    def writeTTFontTableFromXML(cls, tableName, xml, ttfont):
        pathToXML = tempfile.mkstemp()[1]
        temp = open(pathToXML, "w")
        temp.write(xml)
        temp.close()
        ttfont[tableName] = newTable(tableName)
        importXML(ttfont, pathToXML)
        os.remove(pathToXML)

    @classmethod
    def formatNameRecordString(cls, content):
        return content
        #s = ""
        #for element in content:
        #    s = s + element
        #s = unicode(s, "utf8")
        #return s
        #s = s.strip()
        #return s.encode("utf_16_be")

    @classmethod
    def updateTTFontNameTable(cls, ttfont, records):
        name = ttfont['name']
        for record in records:
            newRecord = cls.createTTFontNameRecord(record)
            nameID, platformID, platEncID, langID, value = record
            value = value.strip()
            replaced = False
            for i, origRecord in enumerate(name.names):
                if origRecord.nameID == nameID and origRecord.platformID == platformID and origRecord.platEncID == platEncID and origRecord.langID == langID:
                    name.names[i] = newRecord
                    replaced = True
            if not replaced:
                name.names.append(newRecord)
        # there is a weird encoding issue with some namerecords
        # this is a roundabout solution.
        # so what we do is save a temp TTX file (which works), then load that file into the font.
        pathToXML = tempfile.mkstemp()[1]
        ttfont.saveXML(pathToXML, tables=['name'])
        ttfont['name'] = newTable('name')
        importXML(ttfont, pathToXML)
        os.remove(pathToXML)

    @classmethod
    def removeTTFontNameTableRecords(cls, ttfont, records):
        """Remove certain records from the name table."""
        name = ttfont['name']

        for record in records:
            for i, origRecord in enumerate(name.names):
                if (record[0] is None or record[0] == origRecord.nameID) and \
                    (record[1] is None or record[1] == origRecord.platformID) and  \
                    (record[2] is None or record[2] == origRecord.platEncID) and \
                    (record[3] is None or record[3] == origRecord.langID):
                    name.names.pop(name.names.index(origRecord))

    @classmethod
    def createTTFontNameRecord(cls, record):
        nameID, platformID, platEncID, langID, value = record
        r = TTFontNameRecord()
        r.nameID = nameID
        r.platformID = platformID
        r.platEncID = platEncID
        r.langID = langID
        r.string = cls.formatNameRecordString(value)
        return r

    @classmethod
    def setTTFontVerticalMetrics(cls, ttfont, info, gap=1.2, contexts=[], DEBUG=True):
        """Sets the values that deal with vertical metrics."""
        hhea = ttfont['hhea']
        os2 = ttfont['OS/2']

        idealAscender, idealDescender = cls.getIdealAscenderAndDescender(info)
        realAscender, realDescender = cls.getRealAscenderAndDescender(info, gap)
        # usWin
        os2.usWinAscent = realAscender
        os2.usWinDescent = abs(realDescender)
        # Hhea
        hhea.ascent = realAscender
        hhea.descent = realDescender
        hhea.lineGap = 0
        # sTypo
        os2.sTypoAscender = idealAscender
        os2.sTypoDesender = idealDescender
        os2.sTypoLineGap = ( realAscender + abs(realDescender) ) - ( idealAscender + abs(idealDescender) )
        if DEBUG:
            print('\t\tos2.usWinAscent', os2.usWinAscent)
            print('\t\tos2.usWinDescent', os2.usWinDescent)
            print('\t\thhea.ascent', hhea.ascent)
            print('\t\thhea.descent', hhea.descent)
            print('\t\thhea.lineGap', hhea.lineGap)
            print('\t\tos2.sTypoAscender', os2.sTypoAscender)
            print('\t\tos2.sTypoDesender', os2.sTypoDesender)
            print('\t\tos2.sTypoLineGap', os2.sTypoLineGap)

class FontInfoTX(TTFontNameTableTX):
    """
    `FontInfoTX` provides some transformations for setting and checking font info. Classmethods are fed a font info object.
    """

    # B A S I C S

    @classmethod
    def format(cls, name):
        name = name.replace('_', ' ')
        return name

    @classmethod
    def formatForFile(cls, name):
        name = name.replace(' ', '_')
        return name



    @classmethod
    def copy(cls, source, dest, attrs=C.FONTINFO_ATTRS):
        for attributeName in attrs:
            setattr(dest, attributeName, getattr(source, attributeName))

    @classmethod
    def replaceText(cls, find, replace, info, attrs=C.FONTINFO_ATTRS):
        for attributeName in attrs:
            try:
                setattr(info, attributeName, getattr(info, attributeName).replace(find, replace))
            except:
                pass

    @classmethod
    def checkLengths(cls, info):
        """

        `checkLengths` returns a list of attributes from _info_ that exceed the maximum length.

        """
        errors = []
        for attr, length in C.FONTINFO_NAME_LENGTHS.items():
            if hasattr(info, attr):
                value = getattr(info, attr)
                if len(value) > length:
                    errors.append((attr, value, len(value), length))
        return errors

    @classmethod
    def clear(cls, info):
        """

        `clear` clears all font info attributes to defaults for the given _info_ object.

        """
        for attr, (value, _) in C.FONTINFO_DEFAULTS.items():
            if hasattr(info, attr):
                try:
                    setattr(info, attr, value)
                except:
                    setattr(info.naked(), attr, value)

    @classmethod
    def clearAdvanced(cls, info):
        """

        `clear` returns all font info attributes to defaults for the given _info_ object.

        """
        for attr, (value, _) in C.FONTINFO_DEFAULTS.items():
            if attr not in C.FONTINFO_ATTRS_BASIC and hasattr(info, attr):
                try:
                    setattr(info, attr, value)
                except:
                    setattr(info.naked(), attr, value)

    @classmethod
    def scale(cls, info, multiplier=(1, 1)):
        """s

        `scale` Scale font info.
        """
        for attr in C.FONTINFO_ATTRS_SCALABLE_X:
            value = getattr(info, attr)
            if value:
                if isinstance(value, list):
                    newList = []
                    for item in value:
                        newList.append(item*multiplier[0])
                    value = newList
                else:
                    value = value*multiplier[0]
                setattr(info, attr, value)
        for attr in C.FONTINFO_ATTRS_SCALABLE_Y:
            value = getattr(info, attr)
            if value:
                if isinstance(value, list):
                    newList = []
                    for item in value:
                        newList.append(item*multiplier[1])
                    value = newList
                else:
                    value = value*multiplier[1]
                setattr(info, attr, value)

    ####### N A M E  M A N I P U L A T I O N

    @classmethod
    def getName(cls, name):
        pass

    @classmethod
    def getSeriesAndStyle(cls, name):
        elements = name.split('-')
        if len(elements) > 1:
            style = elements[-1]
            series = '-'.join(elements[:-1])
            return series, style
        else:
            return elements[0], ''

    @classmethod
    def getSeriesAndStyleFromFileName(cls, path):
        _, fileAndExt = os.path.split(path) # basePath, fileAndExt
        fileName, _ = os.path.splitext(fileAndExt) # fileName, ext
        if '-' in fileName:
            elements = fileName.split('-')
            series = elements[0].replace('_', ' ')
            style = '-'.join(elements[1:]).replace('_', ' ')
        else:
            series, style = fileName.replace('_', ' '), ''
        if series[0] == ' ' or series[0] == '~':
            series = series[1:]
        return series, style

    @classmethod
    def getStyleInfo(cls, style, DEBUG=False):
        map = {}
        style = style.replace('-', ' ')
        for axis,spectrum in C.STYLENAME_PREFERRED_VALUES.items():
            for word,score in sorted(spectrum, key=lambda s: len(s[0])*-1):
                if word and word in style:
                    map[axis] = word
                    if DEBUG: print(axis, word)
                    style = style.replace(word, '')
                    style = style.replace('  ', ' ')

        if style and style != ' ':
            map['tags'] = style.strip().split(' ')

        return map

    @classmethod
    def abbreviate(cls, name, include=None, exclude=[], abbrevMap=None, DEBUG=True):
        if not abbrevMap:
            abbrevMap = C.PREFERRED_ABBREVIATIONS
        elements = name.split(' ')
        for i, element in enumerate(elements):
            if element in abbrevMap and element not in exclude:
                if not include or include and element in include:
                    elements[i] = abbrevMap[element]
        return ' '.join(elements)

    ############### N A M E  G E T T E R S

    @classmethod
    def getFamilyAndStyleFromFileName(cls, path):
        series, style = cls.getSeriesAndStyleFromFileName(path)
        print('getFamilyAndStyleFromFile DEPRECATED')
        return cls.getFontInfoFamilyAndStyle(series, style)

    @classmethod
    def getFontInfoFamilyAndStyle(cls, series, style, regularSubstitute=None):
        return series, style

    @classmethod
    def getStyleMapStyleName(cls, style):
        styleInfo = cls.getStyleInfo(style)
        if not 'weight' in styleInfo:
            styleInfo['weight'] = 'Regular'
        if not 'posture' in styleInfo:
            styleInfo['posture'] = 'Roman'
        if styleInfo['weight'] == 'Bold' and ( styleInfo['posture'] == 'Italic' or styleInfo['posture'] == 'Oblique' ):
            return 'bold italic'
        elif styleInfo['weight'] == 'Bold':
            return 'bold'
        elif styleInfo['posture'] == 'Italic' or styleInfo['posture'] == 'Oblique':
            return 'italic'
        else:
            return 'regular'

    @classmethod
    def getPostscriptWeightName(cls, style, regularSubstitute=None):
        """
        """
        styleInfo = cls.getStyleInfo(style)
        if 'weight' in styleInfo:
            return styleInfo['weight']
        else:
            if regularSubstitute:
                return regularSubstitute
            else:
                return 'Regular'

    @classmethod
    def getPostscriptName(cls, fiFamily, fiStyle):
        return "%s-%s" %(fiFamily.replace(' ', ''), fiStyle.replace(' ', ''))

    @classmethod
    def getOpenTypeNameCompatibleFullName(cls, fiFamily, fiStyle):
        return "%s %s" %(fiFamily, fiStyle)

    @classmethod
    def getOpenTypeNameVersion(cls, info):
        return "Version " + str(info.versionMajor) + "." + str(info.versionMinor)

    @classmethod
    def getStyleMapFamilyName(cls, fiFamily, fiStyle, baseFamilyName=None, delimiter=' '):
        return fiFamily + ' ' + fiStyle

    @classmethod
    def getPostscriptFullName(cls, fiFamily, fiStyle, regularSubstitute=None):
        return fiFamily + ' ' + fiStyle

    ########## M E T R I C S  G E T T E R S

    @classmethod
    def getHheaCaretRiseAndRun(cls, info):
        angle = info.italicAngle or 0

        if angle:
            unitsPerEm = cls.getUnitsPerEm(info)
            print('CARET RISE AND RUN', int(unitsPerEm), int(M.getItalicOffset(unitsPerEm, info.italicAngle)))
            return int(unitsPerEm), int(M.getItalicOffset(unitsPerEm, info.italicAngle))
        else:
            return 1, 0

    @classmethod
    def amplifyValue(cls, value, amount):
        if value >= 0:
            return value + amount
        else:
            return value - amount

    @classmethod
    def getIdealAscenderAndDescender(cls, info):
        """
        We assume these are set correctly. If they do not add up to the em, we increase or decrease them evenly.
        """
        unitsPerEm = cls.getUnitsPerEm(info)
        diff = unitsPerEm - (info.ascender + abs(info.descender))
        if diff:
            ascDiff = int(round(diff/2.0))
            descDiff = int(diff/2.0)
            print('%s %s: Ideal ascender %s and descender %s do not sum UPM value of %s. Adding %s units evenly.' %(info.familyName, info.styleName, info.ascender, info.descender, unitsPerEm, diff))
            ascender = int(cls.amplifyValue(info.ascender, ascDiff))
            descender = int(cls.amplifyValue(info.descender, descDiff))
        else:
            ascender = info.ascender
            descender = info.descender
        return ascender, descender


    @classmethod
    def getRealAscenderAndDescender(cls, info, gap=1.2):
        """
        We determine these based on a given gap.
        """
        idealAscender, idealDescender = cls.getIdealAscenderAndDescender(info)
        return int(round(idealAscender * gap)), int(round(idealDescender * gap))

    @classmethod
    def calculateAscentAndDescent(cls, info, contexts=[]):
        """
        We determine these based on the highest and lowest points in the font.
        """
        unitsPerEm = cls.getUnitsPerEm(info)
        unitsPerEmParent = cls.getUnitsPerEm(g.getParent.info)
        lowestBox = 1000000
        lowestGlyph = None
        highestBox = -1000000
        highestGlyph = None
        for f in contexts:
            for g in f:
                if g.name not in cls.ignore and g.box and g.box[3] / float(unitsPerEmParent) > highestBox:
                    highestBox = g.box[3] / float(g.getParent().info.unitsPerEm)
                    highestGlyph = g
                if g.name not in cls.ignore and g.box and g.box[1] / float(unitsPerEmParent) < lowestBox:
                    lowestBox = g.box[1] / float(g.getParent().unitsPerEmParent)
                    lowestGlyph = g
        return int(round(highestBox*unitsPerEm)), int(round(lowestBox*unitsPerEm))


    # STRIKEOUT

    @classmethod
    def getOpenTypeOS2StrikeoutSize(cls, info, multiplier=.05):
        unitsPerEm = cls.getUnitsPerEm(info)
        return int(round(unitsPerEm * multiplier))

    @classmethod
    def getOpenTypeOS2StrikeoutPosition(cls, info, multiplier=.225):
        unitsPerEm = cls.getUnitsPerEm(info)
        return int(round(unitsPerEm * multiplier))

    # SUBSCRIPT AND SUPERSCRIPT

    @classmethod
    def getUnitsPerEm(cls, info):
        unitsPerEm = info.unitsPerEm
        if unitsPerEm is None:
            unitsPerEm = 1000
            print('Warning: no units per em defined in font.info, default to %d' % unitsPerEm)
        return unitsPerEm

    @classmethod
    def getOpenTypeOS2SmallFigureSize(cls, info, xMultiplier=1, yMultiplier=1):
        """
        Generic small figure size calculator, to be shared by subscript and superscript.
        """
        unitsPerEm = cls.getUnitsPerEm(info)
        return int(xMultiplier*unitsPerEm), int(yMultiplier*unitsPerEm)

    @classmethod
    def getOpenTypeOS2SmallFigureOffset(cls, info, yMultiplier=1):
        """
        Generic small figure offset calculator, to be shared by subscript and superscript.
        """
        unitsPerEm = cls.getUnitsPerEm(info)
        yoffset = int(yMultiplier * unitsPerEm)
        xoffset = int(M.getItalicOffset(yoffset, info.italicAngle or 0))
        return xoffset, yoffset

    @classmethod
    def getOpenTypeOS2SubscriptSize(cls, info, xMultiplier=650/1000, yMultiplier=600/1000):
        return cls.getOpenTypeOS2SmallFigureSize(info, xMultiplier, yMultiplier)

    @classmethod
    def getOpenTypeOS2SuperscriptSize(cls, info, xMultiplier=650/1000, yMultiplier=600/1000):
        return cls.getOpenTypeOS2SmallFigureSize(info, xMultiplier, yMultiplier)

    @classmethod
    def getOpenTypeOS2SubscriptOffset(cls, info, yMultiplier=-75/1000):
        return cls.getOpenTypeOS2SmallFigureOffset(info, yMultiplier)

    @classmethod
    def getOpenTypeOS2SuperscriptOffset(cls, info, yMultiplier=350/1000):
        return cls.getOpenTypeOS2SmallFigureOffset(info, yMultiplier)

    @classmethod
    def getPanose(cls, info):
        """
        `setPanose` uses the imperfect `Panose` setter to set the panose value for the given _info_.
        """
        p = FBPanose(info.getParent())
        return p.get()

    @classmethod
    def getCodePageRanges(cls, info, minPresence=1, minProportion=None, omitControls=True, DEBUG=False):
        """
        `setCodepageRanges` sets the codepage range for the given font info, based on the unicode coverage of the parent font.
        """
        c = CodepageTX.getOS2CodepageRanges(info.getParent(), minPresence=minPresence, minProportion=minProportion, omitControls=omitControls)
        if DEBUG: print(c)
        return c

    @classmethod
    def getUnicodeRanges(cls, info, DEBUG=False):
        """
        `setUnicodeRanges` sets the unicode range for the given font info, based on the unicode coverage of the parent font.
        """
        u = UnicodeTX.getOS2UnicodeRanges(info.getParent())
        if DEBUG: print(u)
        return u

    ###################### S E T T E R S

    ancillaryInfo = {
                        'openTypeNameDesigner': None,
                        'openTypeNameDesignerURL': None,
                        'openTypeNameManufacturer': None,
                        'openTypeNameManufacturerURL': None,
                        'openTypeNameLicense': None,
                        'openTypeNameLicenseURL': None,
                        'openTypeNameUniqueID': None,
                        'openTypeNameDescription': None,
                        'openTypeNameSampleText': None,
                        'openTypeOS2VendorID': None,
                        'postscriptUniqueID': None,
                        'macintoshFONDFamilyID': None,
                        'versionMajor': None,
                        'versionMinor': None,
                        'copyright': None,
                        'trademark': None,
                        'note': None,
                        'openTypeHeadCreated': None,
                        'openTypeHeadLowestRecPPEM': None,
                        'openTypeHeadFlags': None,
                        }

    @classmethod
    def setInfoValues(cls, info, values={}, defaults={}, reset=False):
        if reset:
            for attribute, value in defaults.items():
                setattr(info, attribute, value)
        for attribute, value in values.items():
            setattr(info, attribute, value)

    @classmethod
    def setAncillaryInfo(cls, info, values={}, defaults=ancillaryInfo, reset=True):
        cls.setInfoValues(info, values, defaults, reset)

    @classmethod
    def unmergeNames(cls, info):
        info.styleMapFamilyName = cls.getStyleMapFamilyName(info.familyName, '')
        info.familyName = info.styleMapFamilyName
        info.styleMapStyleName = 'regular'
        info.italicAngle = 0


    @classmethod
    def setNames(cls, info, series, style, fiFamily=None, fiStyle=None, DEBUG=False):
        print('SETNAMES', series, style, fiFamily, fiStyle)
        """
        Set our names.
        """
        derivedFiFamily, derivedFiStyle = cls.getFontInfoFamilyAndStyle(series, style)
        styleInfo = cls.getStyleInfo(style)
        if not fiFamily:
            fiFamily = derivedFiFamily
        if not fiStyle:
            fiStyle = derivedFiStyle
        if DEBUG: print('\t\t', 'setNames')
        if DEBUG: print('\t\t\tseries:', series)
        if DEBUG: print('\t\t\tstyle:', style)
        styleMapStyleName = cls.getStyleMapStyleName(style)
        info.familyName = fiFamily
        info.styleName = fiStyle
        if DEBUG: print('\t\t\tfamilyName:', info.familyName)
        if DEBUG: print('\t\t\tstyleName:', info.styleName)
        info.styleMapFamilyName = cls.getStyleMapFamilyName(fiFamily, fiStyle)
        if DEBUG: print('\t\t\tstyleMapFamilyName:', info.styleMapFamilyName)
        info.styleMapStyleName = styleMapStyleName
        if DEBUG: print('\t\t\tstyleMapStyleName:', info.styleMapStyleName)
        info.postscriptFontName = cls.getPostscriptName(fiFamily, fiStyle)
        if DEBUG: print('\t\t\tpostscriptFontName:', info.postscriptFontName)
        info.postscriptWeightName = cls.getPostscriptWeightName(style)
        if DEBUG: print('\t\t\tpostscriptWeightName:', info.postscriptWeightName)
        info.openTypeNameCompatibleFullName = None #
        info.postscriptFullName = None #cls.getPostscriptFullName(fiFamily, fiStyle)
        info.openTypeNamePreferredFamilyName = None
        info.openTypeNamePreferredSubfamilyName = None
        info.openTypeNameWWSFamilyName = None
        info.openTypeNameWWSSubfamilyName = None
        info.macintoshFONDName = None
        info.openTypeNameVersion = cls.getOpenTypeNameVersion(info)
        # weight and width
        # ok these aren't really names, but they are derived from the names
        widthValue = cls.getOS2Width(styleInfo)
        if widthValue:
            info.openTypeOS2WidthClass = widthValue
        weightValue = cls.getOS2Weight(styleInfo)
        if weightValue:
            info.openTypeOS2WeightClass = weightValue


    @classmethod
    def updateTTFontNameTableNames(cls, ttfont, series, style, fiFamily=None, fiStyle=None, uniqueID=None, format=None):
        """
        Set our names in the TTFont.
        """
        derivedFiFamily, derivedFiStyle = cls.getFontInfoFamilyAndStyle(series, style)
        styleInfo = cls.getStyleInfo(style)
        if not fiFamily:
            fiFamily = derivedFiFamily
        if not fiStyle:
            fiStyle = derivedFiStyle
        records = [
                   (1, 1, 0, 0, fiFamily),
                   (2, 1, 0, 0,  fiStyle),
                   (4, 1, 0, 0, cls.getPostscriptFullName(fiFamily, fiStyle) ),
                    # these aren't writing all the time, so here they are
                   (17, 1, 0, 0, fiStyle ),
                   (17, 3, 1, 1033, fiStyle ),
                    ]
        if format == 'otf':
            records.append((4, 3, 1, 1033, cls.getPostscriptName(fiFamily, fiStyle) ))
        elif format == 'ttf':
            records.append((4, 3, 1, 1033, cls.getPostscriptFullName(fiFamily, fiStyle) ))
        if uniqueID:
            records.append((3, 1, 0, 0,  uniqueID))
            records.append((3, 3, 1, 1033,  uniqueID))
        cls.updateTTFontNameTable(ttfont, records)

    @classmethod
    def setOS2Info(cls, info, embedding=[2]):
        """
        Set some information about the font.
        """
        font = info.getParent()
        # panose
        info.openTypeOS2Panose = cls.getPanose(info)
        # unicodes and codepages
        info.openTypeOS2UnicodeRanges = cls.getUnicodeRanges(info)
        info.openTypeOS2CodePageRanges = cls.getCodePageRanges(info, minProportion=.96)
        # family and selection values
        info.openTypeOS2FamilyClass = None
        info.openTypeOS2Selection = None
        # embedding
        info.openTypeOS2Type = embedding

    @classmethod
    def setOS2Strikeout(cls, info):
        """
        Strikeout!
        """
        # strikethrough size and postion
        info.openTypeOS2StrikeoutSize = cls.getOpenTypeOS2StrikeoutSize(info)
        info.openTypeOS2StrikeoutPosition = cls.getOpenTypeOS2StrikeoutPosition(info)

    @classmethod
    def setOS2SuperscriptAndSubscript(cls, info):
        """
        Strikeout!
        """
        # sub/superscript. I am just gonna use default values like adobe
        info.openTypeOS2SubscriptXSize, info.openTypeOS2SubscriptYSize = cls.getOpenTypeOS2SubscriptSize(info)
        info.openTypeOS2SubscriptXOffset, info.openTypeOS2SubscriptYOffset = cls.getOpenTypeOS2SubscriptOffset(info)
        info.openTypeOS2SuperscriptXSize, info.openTypeOS2SuperscriptYSize = cls.getOpenTypeOS2SuperscriptSize(info)
        info.openTypeOS2SuperscriptXOffset, info.openTypeOS2SuperscriptYOffset = cls.getOpenTypeOS2SuperscriptOffset(info)

    @classmethod
    def setOS2(cls, info):
        """
        A shortcut for applying all OS2 junk.
        """
        cls.setOS2Info(info)
        cls.setOS2SuperscriptAndSubscript(info)
        cls.setOS2Strikeout(info)

    @classmethod
    def setVerticalMetrics(cls, info, gap=1.2, contexts=[], DEBUG=False):
        """
        Sets the values that deal with vertical metrics.
        """
        idealAscender, idealDescender = cls.getIdealAscenderAndDescender(info)
        realAscender, realDescender = cls.getRealAscenderAndDescender(info, gap)
        # usWin
        info.openTypeOS2WinAscent = realAscender
        info.openTypeOS2WinDescent = abs(realDescender)
        # Hhea
        info.openTypeHheaAscender = realAscender
        info.openTypeHheaDescender = realDescender
        info.openTypeHheaLineGap = 0
        info.openTypeHheaCaretSlopeRise, info.openTypeHheaCaretSlopeRun = cls.getHheaCaretRiseAndRun(info)
        info.openTypeHheaCaretOffset = None
        # sTypo
        info.openTypeOS2TypoAscender = idealAscender
        info.openTypeOS2TypoDescender = idealDescender
        info.openTypeOS2TypoLineGap = ( realAscender + abs(realDescender) ) - ( idealAscender + abs(idealDescender) )
        if DEBUG:
            print('openTypeOS2WinAscent', info.openTypeOS2WinAscent)
            print('openTypeOS2WinDescent', info.openTypeOS2WinDescent)
            print('openTypeHheaAscender', info.openTypeHheaAscender)
            print('openTypeHheaDescender', info.openTypeHheaDescender)
            print('openTypeHheaLineGap', info.openTypeHheaLineGap)
            print('openTypeHheaCaretSlopeRise+Run', info.openTypeHheaCaretSlopeRise, info.openTypeHheaCaretSlopeRun)
            print('openTypeHheaCaretOffset', info.openTypeHheaCaretOffset)
            print('openTypeOS2TypoAscender', info.openTypeOS2TypoAscender)
            print('openTypeOS2TypoDescender', info.openTypeOS2TypoDescender)
            print('openTypeOS2TypoLineGap', info.openTypeOS2TypoLineGap)

    @classmethod
    def resetPostscriptHinting(cls, info):
        info.postscriptBlueValues = None
        info.postscriptOtherBlues = None
        info.postscriptFamilyBlues = None
        info.postscriptFamilyOtherBlues = None
        info.postscriptStemSnapH = None
        info.postscriptStemSnapV = None
        info.postscriptBlueFuzz = None
        info.postscriptBlueShift = None
        info.postscriptBlueScale = None
        info.postscriptForceBold = None

    @classmethod
    def setPostscriptHinting(cls, info):
        print('Warning: Did not set Postscript hinting.')

    @classmethod
    def setPostscriptMisc(cls, info):
        info.postscriptSlantAngle = None
        info.postscriptUnderlineThickness = None
        info.postscriptUnderlinePosition = None
        info.postscriptIsFixedPitch = None
        info.postscriptDefaultWidthX = None
        info.postscriptNominalWidthX = None
        info.postscriptDefaultCharacter = None
        info.postscriptWindowsCharacterSet = None

    @classmethod
    def setPostscript(cls, info):
        """
        """
        cls.setPostscriptHinting(info)
        cls.setPostscriptMisc(info)

    @classmethod
    def setBasic(cls, f):
        FontInfoTX.clearAdvanced(f)
        family, style = cls.getFamilyAndStyleFromFileName(f.path)
        f.info.familyName = family
        f.info.styleName = style or 'Regular'
        styleInfo = FontInfoTX.getStyleInfo(family+' '+style)
        f.info.openTypeOS2WidthClass = cls.getOS2Width(styleInfo) or 5
        f.info.openTypeOS2WeightClass = cls.getOS2Weight(styleInfo) or 400

    @classmethod
    def getOS2Weight(cls, styleInfo={}):
        if 'weight' in styleInfo:
            #info.postscriptWeightName = styleInfo['weight']
            for name, value in C.STYLENAME_PREFERRED_VALUES['weight']:
                if name == styleInfo['weight']:
                    return int(value)
        else:
            return 400

    @classmethod
    def getOS2Width(cls, styleInfo={}):
        if 'width' in styleInfo:
            for name, value in C.STYLENAME_PREFERRED_VALUES['width']:
                if name == styleInfo['width']:
                    return int(round(value/100.0))
        #else:
        #    return 5

class DesktopFontInfoTX(FontInfoTX):
    """
    """

    # NAMES
    # Processing name stuff.
    familyAttributes = ['optical', 'width', 'grade']
    styleAttributes = ['weight', 'posture']

    @classmethod
    def getFontInfoFamilyAndStyle(cls, series, style, regularSubstitute=None):
        familyName = series
        styleName = ''
        map = FontInfoTX.getStyleInfo(style)

        for familyAttr in cls.familyAttributes:
            if familyAttr in map:
                familyName += ' '
                familyName += map[familyAttr]

        for styleAttr in cls.styleAttributes:
            if styleAttr in map:
                if styleName != '':
                    styleName += ' '
                styleName += map[styleAttr]

        if 'tags' in map:
            if regularSubstitute and regularSubstitute in map['tags']:
                map['tags'].pop(map['tags'].index(regularSubstitute))
            elif 'Roman' in map['tags']:
                map['tags'].pop(map['tags'].index('Roman'))
                regularSubstitute = 'Roman'
            if 'Small' in map['tags'] and 'Caps' in map['tags']:
                map['tags'].pop(map['tags'].index('Small'))
                map['tags'].pop(map['tags'].index('Caps'))
                styleName += ' SC'
                print(map['tags'])
            familyName += ' ' + ' '.join(map['tags'])

        familyName = familyName.replace('  ', ' ')
        styleName = styleName.replace('  ', ' ')

        if not styleName or styleName[0] == ' ':
            if regularSubstitute:
                styleName = regularSubstitute + styleName
            else:
                styleName = 'Regular' + styleName
        return familyName.strip(), styleName.strip()


    @classmethod
    def getStyleMapFamilyName(cls, fiFamily, fiStyle, baseFamilyName=None, delimiter=' '):
        """
        """
        smFamily = fiFamily
        smStyle = fiStyle
        styleMapStyleName = string.capwords(cls.getStyleMapStyleName(fiStyle))
        baseStyle = smStyle.replace(styleMapStyleName, '')
        baseStyle = baseStyle.replace('Roman', '')
        if len(smFamily) > 20:
            elements = smFamily.split(' ')
            elements.reverse()
            for i, element in enumerate(elements):
                if len(''.join(elements)) > 20:
                    elements[i] = cls.abbreviate(element)
            elements.reverse()
            smFamily = ''.join(elements)
        if len(baseStyle) > 7:
            baseStyle = cls.abbreviate(baseStyle, abbrevMap=C.PREFERRED_ABBREVIATIONS_GENERIC)
        smFamily = smFamily.replace(' ', '')
        baseStyle = baseStyle.replace(' ', '')
        if baseStyle:
            smFamily += delimiter + baseStyle
        elif baseFamilyName:
            smFamily += delimiter + baseFamilyName
        # warn if we still don't make length
        if len(smFamily) > C.FONTINFO_NAME_LENGTHS['styleMapFamilyName']:
            print('Length warning for styleMapFamilyName "%s": %s (limit is %s)' %(smFamily, len(smFamily), C.FONTINFO_NAME_LENGTHS['styleMapFamilyName']))
        return smFamily.strip()

    @classmethod
    def getPostscriptFullName(cls, fiFamily, fiStyle, regularSubstitute=None):
        """
        """

        # make sure roman is always substituted for regular
        if 'Roman' in fiStyle and not regularSubstitute:
            regularSubstitute = 'Roman'

        # get the style map family name
        smFamily = cls.getStyleMapFamilyName(fiFamily, fiStyle,baseFamilyName=None, delimiter=' ')

        if ' ' in smFamily:
            smFamilyFamily, smFamilyStyle = smFamily.split(' ')
            smFamilyFamily += ' '
        else:
            smFamilyFamily = smFamily + ' '
            smFamilyStyle = ''

        smsn = string.capwords(cls.getStyleMapStyleName(fiStyle))

        if smsn == 'Regular':
            smsn = ''

        fullStyle = smFamilyStyle.strip() + ' ' + smsn.strip()
        elements = fullStyle.split(' ')

        for i, element in enumerate(elements):
            if element == 'Italic' and len(elements) > 1:
                elements[i] = 'Ita'
        #if elements == ['']:
        #    if regularSubstitute:
        #        elements = [regularSubstitute]
        #    else:
        #        elements = ['Regular']
        if len(smFamily) > C.FONTINFO_NAME_LENGTHS['postscriptFullName']:
            print('Length warning for postscriptFullName "%s": %s (limit is %s)' %(smFamily, len(smFamily), C.FONTINFO_NAME_LENGTHS['postscriptFullName']))
        output = smFamilyFamily + ''.join(elements)
        return output.strip()

    OS2_WEIGHT_VALUES = (
        ('Hairline',    250),
        ('Thin',        250),
        ('Extra Light',    275),
        ('Light',        300),
        ('Book',        350),
        ('Regular',        400),
        ('Roman',       400),
        ('Standard',    450),
        ('Medium',        500),
        ('Semibold',      600),
        ('Semi Bold',    600),
        ('Bold',        700),
        ('Extra Bold',    750),
        ('Black',        800),
        ('Extra Black',    850),
        ('Ultra',    860),
        ('Ultra Black',    900),
    )

    @classmethod
    def getOS2Weight(cls, styleInfo={}):
        if 'weight' in styleInfo:
            #info.postscriptWeightName = styleInfo['weight']
            for name, value in cls.OS2_WEIGHT_VALUES:
                if name == styleInfo['weight']:
                    return int(value)
        else:
            return 400

    @classmethod
    def getOS2Width(cls, styleInfo={}):
        if 'width' in styleInfo:
            for name, value in C.STYLENAME_PREFERRED_VALUES['width']:
                if name == styleInfo['width']:
                    return int(round(value/100.0))
        #else:
        #    return 5

class WebFontInfoTX(DesktopFontInfoTX):

    OS2_WEIGHT_VALUES = (
        ('Hairline',    300),
        ('Thin',        300),
        ('Extra Light',    300),
        ('Light',        300),
        ('Book',        300),
        ('Regular',        400),
        ('Roman',       400),
        ('Standard',    400),
        ('Medium',        500),
        ('Semibold',      600),
        ('Semi Bold',    600),
        ('Bold',        700),
        ('Extra Bold',    800),
        ('Black',        800),
        ('Extra Black',    900),
        ('Ultra',    900),
        ('Ultra Black',    900),
    )

    @classmethod
    def getOS2Weight(cls, styleInfo={}):
        if 'weight' in styleInfo:
            for name, value in cls.OS2_WEIGHT_VALUES:
                if name == styleInfo['weight']:
                    return int(value)
        else:
            return 400

    @classmethod
    def getOS2Width(cls, styleInfo={}):
        if 'width' in styleInfo:
            for name, value in C.STYLENAME_PREFERRED_VALUES['width']:
                if name == styleInfo['width']:
                    return int(round(value/100.0))
        #else:
        #    return 5


    @classmethod
    def getFourStyleFontInfoFamilyAndStyle(cls, series, style=''):
        attributes = C.STYLENAME_DEFAULT_ORDER[:]
        si = cls.getStyleInfo(style)
        if si.get('weight') in ['Regular', 'Bold']:
            attributes.pop(attributes.index('weight'))
        styleMapStyleName = cls.getStyleMapStyleName(style)
        name = series
        for attr in attributes:
            if attr in si:
                name += ' '
                name += si[attr]
        return name, styleMapStyleName

    @classmethod
    def getWebFontInfoFamilyAndStyle(cls, series, style=''):
        attributes = C.STYLENAME_DEFAULT_ORDER[:]
        attributes.pop(attributes.index('posture'))
        attributes.pop(attributes.index('weight'))
        si = cls.getStyleInfo(style)
        name = series
        for attr in attributes:
            if attr in si:
                name += ' '
                name += si[attr]
        if 'tags' in si:
            name += ' ' + ' '.join(si['tags'])
        return name, si.get('posture') or 'normal'






    @classmethod
    def getWebsafePath(cls, path, maxLength=42):
        basePath, fileAndExt = os.path.split(path)
        fileName, ext = os.path.splitext(fileAndExt)
        newFileName = fileName

        if len(newFileName+ext) > maxLength:
            # remove preceding underscore
            if newFileName[0] == '_':
                newFileName = newFileName[1:]
            # remove web identifiers
            newFileName = newFileName.replace('_WebTT', '')
            newFileName = newFileName.replace('WebTT', '')
            newFileName = newFileName.replace('_Web', '')
            newFileName = newFileName.replace('Web', '')

        if len(newFileName+ext) > maxLength:
            elements = newFileName.split('-')
            series = elements[0]
            if len(elements) > 1:
                style = '_'.join(elements[1:])
            newStyle = cls.formatForFile(cls.abbreviate(cls.format(style)))
            newFileName = '-'.join([series, newStyle])

        if len(newFileName+ext) > maxLength:
            newFileName = newFileName.replace('_', '')

        if len(newFileName+ext) > maxLength:
            diff = len(newFileName) - maxLength
            elements = fileName.split('-')
            series = elements[0]
            if len(elements) > 1:
                style = '_'.join(elements[1:])
            if len(series) > diff:
                series = series[:-diff]
            newFileName = '-'.join([series, newStyle])

        newPath = os.path.join(basePath, newFileName+ext)
        return newPath


    @classmethod
    def getAtFontFace(cls, path, relativePath, usePathInfo=False, family=None, style=None, weight=None, chopExtension=True):
        fileseries, filestyle = cls.getSeriesAndStyleFromFileName(path)
        fiFamily, fiStyle = cls.getFontInfoFamilyAndStyle(fileseries, filestyle)
        fontFamily = family or fiFamily
        fontWeight = weight or 'normal'
        fontStyle = style or 'normal'
        if usePathInfo:
            fontStyle = cls.getStyleMapStyleName(fiStyle)
            fontWeight = cls.getOS2Weight(cls.getStyleInfo(filestyle))
        elif not style and not weight:
            try:
                f = TTFont(path)
                fontWeight = f['OS/2'].usWeightClass
                if f['OS/2'].fsSelection == 64:
                    fontStyle = 'italic'
                else:
                    fontStyle = 'normal'
            except:
                pass
        if fontWeight == 400 or not fontWeight:
            fontWeight = 'normal'
        basePath, fileNameAndExt = os.path.split(path)
        fileName, ext = os.path.splitext(fileNameAndExt) if chopExtension else (fileNameAndExt,'')
        relativePathNoExt = os.path.join(relativePath, fileName)
        aff = """@font-face {
                           src: url('%s.eot'); /* IE < 9 */
                           src: url('%s.eot?#') format("embedded-opentype"), /* IE 9 */
                                url('%s.woff') format("woff"),
                            url('%s.ttf') format("opentype"),
                                url('%s.svg#web') format("svg");
                           font-family: '%s';
                           font-style: %s;
                           font-weight: %s;
                           }
                """ %(relativePathNoExt,
                      relativePathNoExt,
                      relativePathNoExt,
                      relativePathNoExt,
                      relativePathNoExt,
                      fontFamily,
                      fontStyle,
                      fontWeight,
                      )
        """
                    .%s {
                         font-family: %s, "Zero Width Space", "FB Unicode Fallback";
                         }
        """
        return aff

class AppFontInfoTX(DesktopFontInfoTX):

    @classmethod
    def getObfuscatedName(cls,length):
        chars = ['f', 'b']
        string_letters = string.digits[:] + string.letters[:]
        while length > 0:
            length -= 1
            chars.append(choice(string_letters))
        return ''.join(chars)

    @classmethod
    def getFontInfoFamilyAndStyle(cls, series, style):
        fiFamily, fiStyle = DesktopFontInfoTX.getFontInfoFamilyAndStyle(series, style)
        fiFamily = cls.getObfuscatedName(8)
        return fiFamily, fiStyle

# LEGACY NAMES
PrintFontInfoLandingPattern = DesktopFontInfoTX
AppFontInfoLandingPattern = AppFontInfoTX


class Panose:
    """`Panose` takes a font, which it uses to determine panose
    values.  This object is my first attempt to fill out panose values based on
    the information here:

    <a href="http://panose.com/ProductsServices/pan2.aspx">http://panose.com/ProductsServices/pan2.aspx</a>.
    """

    def __init__(self, f):
        self.f = f

    @classmethod
    def getStemAndHair(cls, f, measureGlyphs=('H', 'O'), measureProportions=(4, 2)):
        """
        `getStemAndHair`: Get the lowercase stem and hair for the font using n and o.

        ***IN THE FUTURE, USE GLYPH ANALYZER FOR THIS!!!***

        _measure proportions_:
        4 = measure one quarter of the height/width
        2 = measure half way of the height/width

        """
        try:
            from fontPens.marginPen import MarginPen
            stemGlyph, hairGlyph = measureGlyphs
            stemWeight = None
            hairWeight = None
            if stemGlyph in f:
                height = f[stemGlyph].box[1]
                height += (f[stemGlyph].box[3]-f[stemGlyph].box[1])/ measureProportions[0]
                pen = MarginPen(f, height)
                f[stemGlyph].draw(pen)
                stemCrossings = list(pen.getAll())
                stemWeight = stemCrossings[1] - stemCrossings[0]
                stemWeight = int(round(stemWeight))
            if hairGlyph in f:
                middle = (f[hairGlyph].box[2] - f[hairGlyph].box[0]) / measureProportions[1]
                middle += f[hairGlyph].leftMargin
                pen = MarginPen(f, middle, isHorizontal=False)
                f[hairGlyph].draw(pen)
                hairCrossings = list(pen.getAll())
                hairWeight = hairCrossings[1] - hairCrossings[0]
                hairWeight = int(round(hairWeight))
            return stemWeight, hairWeight
        except:
            return 1, 1

    def getFamilyKind(self):
        """
        `getFamilyKind` sets the familyKind. Currently PanoseSetter only knows Latin Text Family kind.

        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-Latin Text</li>
        <li>3-Latin Hand Written</li>
        <li>4-Latin Decorative</li>
        <li>5-Latin Symbol</li>
        </ul>
        """
        return 2

    def getSerifValue(self):
        """
        `getSerifValue` currently cannot calculate serif value, and returns Any.

        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-Cove</li>
        <li>3-Obtuse Cove</li>
        <li>4-Square Cove</li>
        <li>5-Obtuse Square Cove</li>
        <li>6-Square</li>
        <li>7-Thin</li>
        <li>8-Oval</li>
        <li>9-Exaggerated</li>
        <li>10-Triangle</li>
        <li>11-Normal Sans</li>
        <li>12-Obtuse Sans</li>
        <li>13-Perpendicular Sans</li>
        <li>14-Flared</li>
        <li>15-Rounded</li>
        </ul>

        """
        return 0

    def getWeightValue(self):
        """
        `getWeightValue` calculates stem and weight. We actually do a pretty good job here.
        <ul>
        0-Any</li>
        1-No Fit</li>
        2-Very Light</li>
        3-Light</li>
        4-Thin</li>
        5-Book</li>
        6-Medium</li>
        7-Demi</li>
        8-Bold</li>
        9-Heavy</li>
        10-Black</li>
        11-Extra Black</li>
        </ul>

        """

        f = self.f
        stem, hair = self.getStemAndHair(f)
        if not 'H' in f:
            return 0
        CapH = f['H'].box[3]
        weightRat = CapH / stem

        if weightRat >= 35:
            panoseWeightValue = 2
        elif 18 <= weightRat < 35:
            panoseWeightValue = 3
        elif 10 <= weightRat < 18:
            panoseWeightValue = 4
        elif 7.5 <= weightRat < 10:
            panoseWeightValue = 5
        elif 5.5 <= weightRat < 7.5:
            panoseWeightValue = 6
        elif 4.5 <= weightRat < 5.5:
            panoseWeightValue = 7
        elif 3.5 <= weightRat < 4.5:
            panoseWeightValue = 8
        elif 2.5 <= weightRat < 3.5:
            panoseWeightValue = 9
        elif 2<= weightRat < 2.5:
            panoseWeightValue = 10
        elif weightRat < 2:
            panoseWeightValue = 11
        else:
            panoseWeightValue = 0
        return panoseWeightValue

    def getWidthValue(self):
        """
        `getWidthValue` calculates the width value, and actually does a pretty good job.
        <ul>
        <li>0-Any</li>
        <li>1-No fit</li>
        <li>2-Old Style</li>
        <li>3-Modern</li>
        <li>4-Even Width</li>
        <li>5-Extended</li>
        <li>6-Condensed</li>
        <li>7-Very Extended</li>
        <li>8-Very Condensed</li>
        <li>9-Monospaced</li>
        </ul>
        """
        f = self.f
        if not 'H' in f or not 'E' in f or not 'S' in f or not 'O' in f or not 'J' in f or not 'M' in f or not 'O' in f:
            return 0

        CapH = f['H'].box[3]
        EWid = f['E'].box[2] - f['E'].box[0]
        SWid = f['S'].box[2] - f['S'].box[0]
        OWid = f['O'].box[2] - f['O'].box[0]
        HWid = f['H'].box[2] - f['H'].box[0]
        JWid = f['J'].box[2] - f['J'].box[0]
        MWid = f['M'].box[2] - f['M'].box[0]
        OTall = f['O'].box[3] - f['O'].box[1]

        ThinAv = (EWid + SWid) / 2
        WideAv = (OWid + HWid) / 2
        CalcEm = CapH * 1.5
        ThinRat = CalcEm / ThinAv
        WideRat = CalcEm / WideAv
        PropRat = WideRat / ThinRat
        JMRat = JWid / MWid
        ORat = OTall / OWid
        print(JMRat, ORat)

        if JMRat < 0.78 and 0.92 <= ORat < 1.27 and PropRat < 0.70:
            panoseWidthValue = 2
        elif JMRat < 0.78 and 0.92 <= ORat < 1.27 and 0.70 <= PropRat < 0.83:
            panoseWidthValue = 3
        elif JMRat < 0.78 and 0.92 <= ORat < 1.27 and 0.83 <= PropRat < 0.91:
            panoseWidthValue = 4
        elif JMRat < 0.78 and 0.90 <= ORat <= 0.92:
            panoseWidthValue = 5
        elif JMRat < 0.78 and 1.27 <= ORat < 2.1:
            panoseWidthValue = 6
        elif JMRat < 0.78 and 0.85 <= ORat < 0.90:
            panoseWidthValue = 7
        elif JMRat < 0.78 and 2.1 <= ORat < 2.6:
            panoseWidthValue = 8
        elif JMRat > 0.78:
            panoseWidthValue = 9
        else:
            panoseWidthValue = 0
        return panoseWidthValue

    def getContrastValue(self):
        """
        `getContrastValue` does an okay job calculating the contrast value.
        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-None</li>
        <li>3-Very Low</li>
        <li>4-Low</li>
        <li>5-Medium Low</li>
        <li>6-Medium</li>
        <li>7-Medium High</li>
        <li>8-High</li>
        <li>9-Very High</li>
        </ul>

        """
        f = self.f
        if not 'O' in f:
            return 0
        WideO, NarO = self.getStemAndHair(f, measureGlyphs=('O', 'O'), measureProportions=(2, 2))
        ConRat = NarO / WideO

        if 0.80 < ConRat:
            panoseContrastValue = 2
        elif 0.65 < ConRat <= 0.80:
            panoseContrastValue = 3
        elif 0.48 < ConRat <= 0.65:
            panoseContrastValue = 4
        elif 0.30 < ConRat <= 0.48:
            panoseContrastValue = 5
        elif 0.20 < ConRat <= 0.30:
            panoseContrastValue = 6
        elif 0.15 < ConRat <= 0.20:
            panoseContrastValue = 7
        elif 0.08 < ConRat <= 0.15:
            panoseContrastValue = 8
        elif ConRat <= 0.08:
            panoseContrastValue = 9
        else:
            panoseContrastValue = 0
        return panoseContrastValue

    def getStrokeVariation(self):
        """
        `getStrokeVariation` currently cannot calculate stroke variation.

        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-No Variation</li>
        <li>3-Gradual/Diagonal</li>
        <li>4-Gradual/Transitional</li>
        <li>5-Gradual/Vertical</li>
        <li>6-Gradual/Horizontal</li>
        <li>7-Rapid/Vertical</li>
        <li>8-Rapid/Horizontal</li>
        <li>9-Instant/Vertical</li>
        <li>10-Instant/Horizontal</li>
        </ul>

        """
        return 0

    def getArmStyle(self):
        """
        `getArmStyle` currently cannot calculate arm style.
        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-Straight Arms/Horizontal</li>
        <li>3-Straight Arms/Wedge</li>
        <li>4-Straight Arms/Vertical</li>
        <li>5-Straight Arms/Single Serif</li>
        <li>6-Straight Arms/Double Serif</li>
        <li>7-Non-Straight/Horizontal</li>
        <li>8-Non-Straight/Wedge</li>
        <li>9-Non-Straight/Vertical</li>
        <li>10-Non-Straight/Single Serif</li>
        <li>11-Non-Straight/Double Serif</li>
        </ul>

        """
        return 0

    def getLetterform(self):
        """
        `getLetterform` can only currently only sets letteform to 2 for Roman and 9 for Italic.
        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-Normal/Contact</li>
        <li>3-Normal/Weighted</li>
        <li>4-Normal/Boxed</li>
        <li>5-Normal/Flattened</li>
        <li>6-Normal/Rounded</li>
        <li>7-Normal/Off Center</li>
        <li>8-Normal/Square</li>
        <li>9-Oblique/Contact</li>
        <li>10-Oblique/Weighted</li>
        <li>11-Oblique/Boxed</li>
        <li>12-Oblique/Flattened</li>
        <li>13-Oblique/Rounded</li>
        <li>14-Oblique/Off Center</li>
        <li>15-Oblique/Square</li>
        </ul>

        """
        f = self.f
        if f.info.italicAngle == 0:
            panoseLetterform = 2
        else:
            panoseLetterform = 9
        return panoseLetterform

    def getMidline(self):
        """
        `getMidline` currently cannot set midline.
        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-Standard/Trimmed</li>
        <li>3-Standard/Pointed</li>
        <li>4-Standard/Serifed</li>
        <li>5-High/Trimmed</li>
        <li>6-High/Pointed</li>
        <li>7-High/Serifed</li>
        <li>8-Constant/Trimmed</li>
        <li>9-Constant/Pointed</li>
        <li>10-Constant/Serifed</li>
        <li>11-Low/Trimmed</li>
        <li>12-Low/Pointed</li>
        <li>13-Low/Serifed</li>
        </ul>

        """
        return 0

    def getXHeight(self):
        """
        `getXHeight` gets the xHeight value.
        <ul>
        <li>0-Any</li>
        <li>1-No Fit</li>
        <li>2-Constant/Small</li>
        <li>3-Constant/Standard</li>
        <li>4-Constant/Large</li>
        <li>5-Ducking/Small</li>
        <li>6-Ducking/Standard</li>
        <li>7-Ducking/Large</li>
        </ul>

        """
        f = self.f
        if not 'x' in f or not 'A' in f or not 'H' in f:
            return 0
        XTall = f['x'].box[3] - f['x'].box[1]
        AAcTall = f['A'].box[3] - f['A'].box[1]
        CapH = f['H'].box[3]
        DuckRat = AAcTall / CapH
        XRat = XTall / CapH

        if DuckRat <= .93:
            ducking = True
        else:
            ducking = False

        if XRat < 0.50:
            size = 'small'
        elif 0.50 < XRat < 0.66:
            size = 'medium'
        elif 0.66 < XRat:
            size = 'large'
        else:
            size = None

        if not ducking and size == 'small':
            panoseXHeight = 2
        elif not ducking and size == 'medium':
            panoseXHeight = 3
        elif not ducking and size == 'large':
            panoseXHeight = 4
        elif ducking and size == 'small':
            panoseXHeight = 5
        elif ducking and size == 'medium':
            panoseXHeight = 6
        elif ducking and size == 'large':
            panoseXHeight = 7
        else:
            panoseXHeight = 0

        return panoseXHeight

    def get(self):
        """
        `get` returns a tuple of all panose values that can be passed to `f.info.openTypeOS2Panose`.
        """
        f = self.f
        return (
                       self.getFamilyKind(),       # 1
                       self.getSerifValue(),       # 2
                       self.getWeightValue(),      # 3
                       self.getWidthValue(),       # 4
                       self.getContrastValue(),    # 5
                       self.getStrokeVariation(),  # 6
                       self.getArmStyle(),         # 7
                       self.getLetterform(),       # 8
                       self.getMidline(),          # 9
                       self.getXHeight(),          # 10
                       )

    def set(self):
        """`set` sets the panose value in the font."""
        f = self.f
        f.info.openTypeOS2Panose = self.get()

class FBPanose:
    """`FBPanose` is a panose-setter that sets the panose the FB way, meaning everything to zero, except for monospacedness and style.`"""

    def __init__(self, f):
        self.f = f

    def getFamilyKind(self):
        return 0
    def getSerifValue(self):
        return 0
    def getWeightValue(self):
        return 0
    def getWidthValue(self):
        # if all of ASCII is the same width as the 'zero' glyph, it is monospaced.
        # allows two exceptions, just in case of a minor error
        f = self.f
        m = getCharacterMapping(f) # f may not be a RF Wrapper font. Used general method instead.
        proportionalCount = 0
        totalCount = 0
        try:
            width = f[m.get(48)[0]].width
        except:
            width = 500
        for u in range(32, 128):
            gnames = m.get(u)
            if gnames:
                totalCount += 1
                gname = gnames[0]
                g = f[gname]
                if g.width != width:
                    proportionalCount += 1
                    if proportionalCount > 2:
                        break
        if not totalCount or ( proportionalCount / float(totalCount) ) > .01:
            return 0
        else:
            return 9



    def getContrastValue(self):
        return 0
    def getStrokeVariation(self):
        return 0
    def getArmStyle(self):
        return 0
    def getLetterform(self):
        f = self.f
        if f.info.italicAngle == 0:
            return 2
        else:
            return 9

    def getMidline(self):
        return 0
    def getXHeight(self):
        return 0

    def get(self):
        """
        `get` returns a tuple of all panose values that can be passed to `f.info.openTypeOS2Panose`.
        """
        f = self.f
        return (
                       self.getFamilyKind(),       # 1
                       self.getSerifValue(),       # 2
                       self.getWeightValue(),      # 3
                       self.getWidthValue(),       # 4
                       self.getContrastValue(),    # 5
                       self.getStrokeVariation(),  # 6
                       self.getArmStyle(),         # 7
                       self.getLetterform(),       # 8
                       self.getMidline(),          # 9
                       self.getXHeight(),          # 10
                       )

    def set(self):
        """`set` sets the panose value in the font."""
        f = self.f
        f.info.openTypeOS2Panose = self.get()


if __name__ == "__main__":
    f = CurrentFont()

    print(DesktopFontInfoTX.getPanose(f.info))
