# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.constants import Constants as C
from tnbits.toolbox.transformer import TX
from tnbits.base.future import chr

############################################################
############################################################
############################################################
############################################################
#  G L Y P H   N A M E
############################################################
############################################################
############################################################
############################################################

class GlyphNameTX:
    """
    `GlyphNameTX</ code> is a mini-transformer that handles some of the common glyph name manipulations. A
    glyph can be split into baseName and suffix parts. Each of these parts can be split into elements:
    _baseNameElement1_baseNameElement2.suffixElement1_suffixElement2_.
    """
    ELEMENT_DELIMITER = '_'
    NAME_DELIMITER = '.'

    ##########
    # STRING

    @classmethod
    def splitElements(cls, name, delimiter=ELEMENT_DELIMITER):
        """
        `splitElements` splits a name into a list of underscore-delimited elements.
        """
        elementList = []
        if name:
            if isinstance(name, list):
                elementList = name
            else:
                elementList = name.split(delimiter)
        return elementList

    @classmethod
    def joinElements(cls, elements, delimiter=ELEMENT_DELIMITER):
        """
        `joinElements` joins a name from a list of underscore-delimited elements.
        """
        elementString = ''
        if elements:
            if isinstance(elements, str):
                elementString = elements
            elif isinstance(elements, list):
                elementString = delimiter.join(elements)
        return elementString

    @classmethod
    def appendElement(cls, elementList, elements, avoidDuplicates=True):
        """
        `appendElement` adds a new element to a list of elements, avoiding duplicates, and returns the
        new list.
        """
        if elementList is None:
            elementList = []
        if isinstance(elementList, str):
            elementList = [elementList]
        if avoidDuplicates:
            for s in elementList:
                if not s or s in elements:
                    elementList.remove(s)
        return elements + elementList

    @classmethod
    def removeElement(cls, elementList, elements):
        """
        `removeElement` removes an element from a list of elements, and returns the new list.
        """
        if isinstance(elementList, str):
            elementList = [elementList]
        newElements = []
        for s in elements:
            if s not in elementList:
                newElements.append(s)
        return newElements

    @classmethod
    def replaceElement(cls, elements, mapDict):
        """
        `replaceElement` replaces elements according to _mapDict_.
        """
        newElements = []
        for s in elements:
            if s in mapDict:
                newElements.append(mapDict[s])
            else:
                newElements.append(s)
        return newElements

    ##############################
    ##############################
    ##############################

    @classmethod
    def split(cls, name, delimiter=NAME_DELIMITER):
        """
        `split` splits a given name into base name and suffix strings.
        """

        baseName = None
        suffix = None
        nameElements = name.split(delimiter)
        if len(nameElements) > 0:
            baseName = nameElements[0]
            if len(nameElements) > 1:
                suffix = delimiter.join(nameElements[1:])
            else:
                suffix = None
        return baseName, suffix

    @classmethod
    def join(cls, baseNameElements, suffixElements, delimiter=NAME_DELIMITER):
        """
        `join` returns a new name from a given baseName and suffix. This accepts strings or element
        lists.
        """

        if not isinstance(baseNameElements, list):
            baseNameElements = [baseNameElements]
        if not isinstance(suffixElements, list):
            suffixElements = [suffixElements]
        baseNameString = cls.joinElements(baseNameElements)
        suffixString = cls.joinElements(suffixElements)
        gName = baseNameString
        if suffixString:
            gName += delimiter + suffixString
        return gName

    @classmethod
    def splitIntoElements(cls, name, delimiter=NAME_DELIMITER, elementDelimiter=ELEMENT_DELIMITER):
        """
        `splitIntoElements` splits a given name into base name and suffix lists.
        """
        baseName, suffix = cls.split(name, delimiter=delimiter)
        return cls.splitElements(baseName, delimiter=elementDelimiter), cls.splitElements(suffix, delimiter=elementDelimiter)

    @classmethod
    def getBaseName(cls, name):
        """
        `getBaseName` returns the give name's base name as a string.
        """
        return cls.split(name)[0]

    @classmethod
    def getSuffix(cls, name):
        """
        `getSuffix` returns the give name's suffix as a string.
        """
        return cls.split(name)[1]

    @classmethod
    def getBaseNameElements(cls, name):
        """
        `getBaseNameELements` returns the give name's base name as a list of elements.
        """
        return cls.splitIntoElements(name)[0]

    @classmethod
    def getSuffixElements(cls, name):
        """
        `getSuffixElements` returns the give name's suffix as a list of elements.
        """
        return cls.splitIntoElements(name)[1]

    ##########################################
    ##########################################

    @classmethod
    def appendSuffixElement(cls, name, suffixList, avoidDuplicates=True):
        """
        `appendSuffixElement` returns a new name with new suffix elements added.
        """
        if not isinstance(suffixList, list):
            suffixList = [suffixList]
        elements = cls.getSuffixElements(name) or []
        newElements = cls.appendElement(suffixList, elements, avoidDuplicates=avoidDuplicates)
        return cls.join(cls.getBaseName(name), newElements)

    @classmethod
    def removeSuffixElement(cls, name, suffixList):
        """
        `appendSuffixElement` returns a new name with new suffix elements removed.
        """
        if not isinstance(suffixList, list):
            suffixList = [suffixList]
        elements = cls.getSuffixElements(name) or []
        newElements = cls.removeElement(suffixList, elements)
        return cls.join(cls.getBaseName(name), newElements)

    @classmethod
    def replaceSuffixElement(cls, name, mapDict):
        """
        `appendSuffixElement` returns a new name with new suffix elements replaced according to
        _mapDict_.
        """
        elements = cls.getSuffixElements(name) or []
        newElements = cls.replaceElement(elements, mapDict)
        return cls.join(cls.getBaseName(name), newElements)

    @classmethod
    def appendBaseNameElement(cls, name, baseNameList, avoidDuplicates=False):
        """
        `appendSuffixElement` returns a new name with new base name elements added.
        """
        if not isinstance(baseNameList, list):
            baseNameList = [baseNameList]
        elements = cls.getBaseNameElements(name) or []
        newElements = cls.appendElement(baseNameList, elements, avoidDuplicates=avoidDuplicates)
        return cls.join(newElements, cls.getSuffix(name))

    @classmethod
    def removeBaseNameElement(cls, name, baseNameList):
        """
        `appendSuffixElement` returns a new name with new base name elements removed.
        """
        if not isinstance(baseNameList, list):
            baseNameList = [baseNameList]
        elements = cls.getBaseNameElements(name) or []
        newElements = cls.removeElement(baseNameList, elements)
        return cls.join(newElements, cls.getSuffix(name))

    @classmethod
    def replaceBaseNameElement(cls, name, mapDict):
        """
        `appendSuffixElement` returns a new name with new base name elements replaced according to
        _mapDict_.
        """
        elements = cls.getBaseNameElements(name) or []
        newElements = cls.replaceElement(elements, mapDict)
        return cls.join(newElements, cls.getSuffix(name))

    @classmethod
    def hasSuffix(cls, name, searchFor=None):
        """
        `hasSuffix` returns True if a given glyph name has any suffix. Optionally, a specific suffix may
        be provided, and it will return True if the suffixes match.
        """
        suffix = cls.getSuffix(name)
        if searchFor is None:
            if suffix:
                return True
            else:
                return False
        else:
            return suffix == searchFor

    @classmethod
    def hasSuffixElement(cls, name, searchFor=None):
        """
        `hasSuffix` returns True if a given glyph name has any suffix elements. Optionally, a specific
        suffix element may be provided, and it will return True if the suffix contains that element.
        """
        if searchFor is None:
            if cls.getSuffixElements(name):
                return True
            else:
                return False
        if not isinstance(searchFor, list):
            searchFor = [searchFor]
        searchForSet = set(searchFor)
        suffixElements = cls.getSuffixElements(name)
        suffixSet = set(suffixElements)
        return searchForSet <= suffixSet


    @classmethod
    def orderSuffixElements(cls, suffixElements):
        """
        `orderSuffixElements` puts suffixes into a predetermined order, appending the rest in the order
        in which they were given.
        """
        suffixList = suffixElements[:]
        newSuffixList = []
        for s in C.GLYPHNAME_SUFFIXORDER:
            if s in suffixList:
                newSuffixList.append(s)
                index = suffixList.index(s)
                del suffixList[index]
        for extraSuffix in suffixList:
            newSuffixList.append(extraSuffix)
        return newSuffixList

    @classmethod
    def reorderSuffix(cls, name):
        """
        `reorderSuffix` returns a new name with the suffixes shuffled.
        """
        baseNameElements, suffixElements = cls.splitIntoElements(name)
        suffixElements = cls.orderSuffixElements(suffixElements)
        return cls.join(baseNameElements, suffixElements)

    @classmethod
    def isHexDigit(cls, name):
        """
        `isHexDigit` returns True if the given name matches a hexadecimal unicode value.
        """
        for n in name:
            if n not in C.HEXADECIMALDIGITS:
                return False
        return True

    @classmethod
    def splitFourDigitUnicodeSequence(cls, l):
        """
        `splitFourDigitUnicodeSequence` helps process unicode values.
        """
        return [l[i:i + 4] for i in range(0, len(l), 4)]



    @classmethod
    def getUnicodeName(cls, unicodes=[]):
        """
        `getUnicodeName` takes a list of unicodes, and returns a 'uni' or 'u' prefixed name. For use
        when no Adobe Glyph List name exists.
        """
        if isinstance(unicodes, int):
            unicodes = [unicodes]
        hexUnicodes = TX.readUnicodes(unicodes)
        prefix = 'uni'
        for hexUnicode in hexUnicodes:
            if TX.hex2dec(hexUnicode) >= 65535:
                if len(unicodes) == 1:
                    prefix = 'u'
        if hexUnicodes:
            return prefix + ''.join(hexUnicodes)
        else:
            return None

    @classmethod
    def getUnicodeSequence(cls, name, VERBOSE=False):
        """
        `getUnicodeSequence` gets a unicode sequence from a unicode name, following the rules.
        <blockquote>If the component is of the form "uni" (U+0075 U+006E U+0069) followed by a sequence of uppercase
        hexadecimal digits (0 .. 9, A .. F, i.e. U+0030 .. U+0039, U+0041 .. U+0046), the length of that sequence is a
        multiple of four, and each group of four digits represents a number in the set {0x0000 .. 0xD7FF, 0xE000 ..
        0xFFFF}, then interpret each such number as a Unicode scalar value and map the component to the string made of
        those scalar values. Note that the range and digit length restrictions mean that the "uni" prefix can be used
        only with Unicode values from the Basic Multilingual Plane (BMP).</blockquote>

        <blockquote>Otherwise, if the component is of the form "u" (U+0075) followed by a sequence of four to six
        uppercase hexadecimal digits {0 .. 9, A .. F} (U+0030 .. U+0039, U+0041 .. U+0046), and those digits represent a
        number in {0x0000 .. 0xD7FF, 0xE000 .. 0x10FFFF}, then interpret this number as a Unicode scalar value and map
        the component to the string made of this scalar value.</blockquote>
        """
        unicodeList = None
        if VERBOSE: print('isUnicodeName, %s' % name)
        if len(name) > 3 and name[:3] == 'uni':
            unicodeSequence = name[3:]
            if len(unicodeSequence) / 4 == int(len(unicodeSequence) / 4):
                unicodeList = cls.splitFourDigitUnicodeSequence(unicodeSequence)
                for unicodeHex in unicodeList:
                    if not cls.isHexDigit(unicodeHex):
                        return None
        elif len(name) > 1 and name[0] == 'u':
            unicodeSequence = name[1:]
            if len(unicodeSequence) >= 4 and len(unicodeSequence) <= 6 and cls.isHexDigit(unicodeSequence):
                if unicodeSequence:
                    unicodeList = [unicodeSequence]
                else:
                    unicodeList = unicodeSequence
        decUnicodeList = []
        if unicodeList:
            for u in unicodeList:
                try:
                    decUnicodeList.append(TX.hex2dec(u))
                except:
                    decUnicodeList.append(u)
            return decUnicodeList
        else:
            return unicodeList


    ##########
    # Adobe glyph name rules
    ##########

    @classmethod
    def validate(cls, name, f=None, VERBOSE=False):
        """
        `validate` tests all requirements for a glyph name. See also the
        <a href="http://www.adobe.com/devnet/opentype/archives/glyph.html">Adobe Glyph Naming convention</a>.
        """
        isValid = True
        # check name length and character requirements

        if len(name) > 31:
            isValid = False
            if VERBOSE: print("\tLength '%s' is greater than 31 chars." % len(name))
        if len(name) < 1:
            isValid = False
            if VERBOSE: print("\tLength '%s' is less than 1 chars." % len(name))

        for x, s in enumerate(name):
            if s not in C.GLYPHNAME_ALLOWEDCHARS:
                isValid = False
                if VERBOSE: print("\tCharacter %s is not a valid character. Must be 0-9 A-Z a-z . _" % s)
            if x == 0 and s in C.GLYPHNAME_NOTFIRSTCHARS and name != '.notdef':
                isValid = False
                if VERBOSE: print("\tCharacter cannot begin with number or period, except for .notdef.")

        # look for base names
        for baseName in cls.getBaseNameElements(name):
            unicodeSequence = cls.getUnicodeSequence(baseName)
            # make sure Unicode exist.
            if unicodeSequence:
                for unicodeValue in unicodeSequence:
                    if f and not cls.writeUnicode(unicodeValue) in f.getCharacterMapping():
                        isValid = False
                        if VERBOSE: print('\tUnicode value %s does not exist in font.' % unicodeValue)
            else:
                if not baseName in C.ADOBEGLYPHLIST:
                    isValid = False
                    if VERBOSE: print("\tBaseName '%s' not in Adobe Glyph List." % baseName)
        return isValid

    @classmethod
    def getCharacterComponents(cls, name):
        """
        `getCharacterComponents` gets the components of the glyph name.
        """
        characterComponents = []
        for baseName in cls.getBaseNameElements(name):
            unicodeSequence = cls.getUnicodeSequence(baseName)
            if unicodeSequence:
                characterComponents.append(unicodeSequence)
            else:
                if baseName in C.ADOBEGLYPHLIST:
                    characterComponents.append(C.ADOBEGLYPHLIST[baseName])
                # else:
                    # characterComponents.append('')
        return characterComponents

    @classmethod
    def getCharacterString(cls, name):
        """
        `getCharacterString` gets the character mapping of the glyph name as a string.
        """
        components = cls.getCharacterComponents(name)
        characterString = u''
        for c in components:
            if isinstance(c, list):
                for l in c:
                    characterString += chr(l)
            else:
                characterString += chr(c)
        return characterString

    @classmethod
    def getClosestExistingName(cls, name, f):
        """
        Given a font, `getClosestExistingName` finds closest name that exists in the font. This removes
        the last suffix, one by one, until a name is found, meaning order is important here. For example, say we have
        a font with two glyphs: ['A', 'A.sc']. If the glyph name is 'A.sc_scrap', the closest glyph is 'A.sc'. If the
        glyph name is 'A.scrap_sc', with standardizeSuffixOrder=False, the closest glyph is 'A'.
        """
        if name in f:
            return name
        else:
            baseNameElements, suffixElements = cls.splitIntoElements(name)
            if suffixElements:
                newSuffixElements = suffixElements[:-1]
                newName = cls.join(baseNameElements, newSuffixElements)
                return cls.getClosestExistingName(newName, f)
            else:
                return None

    @classmethod
    def getSuffixElementsAfter(cls, name, s):
        """
        `getSuffixElementsAfter` gets all suffix elements that follow a given element.
        """
        suffixElements = cls.getSuffixElements(name)
        if s in suffixElements:
            i = suffixElements.index(s)
            return suffixElements[i + 1:]
        return []

    @classmethod
    def getUniqueName(cls, name, f, rootName=None, index=1):
        """
        Given a font, `getUniqueName` takes _name_ and adds suffixes until it is unique.
        """
        if not rootName:
            rootName = name
        if name in f:
            gn = cls.appendSuffixElement(rootName, str(index))
            return cls.getUniqueName(name=gn, f=f, rootName=rootName, index=index + 1)
        else:
            return name
