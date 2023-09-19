# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
from tnbits.toolbox.glyph import GlyphTX
from tnbits.toolbox.character import CharacterTX
from tnbits.toolbox.fontparts.unicode import UnicodeTX
import unicodedata
from tnbits.base.future import chr

class GlyphElement:
    def __init__(self, chars=None, feas=None, name=None):
        # Don't use chars=[] in attributes, since these are mutable objects.
        # They can be modified on class level this way. Better to test the way below.
        if chars is None:
            chars = []
        if feas is None:
            feas = []
        self.setChars(list(chars))
        self.setFeas(feas)
        if name:
            self.setName(name)

    def setChars(self, chars):
        self.chars = chars or []

    def setFeas(self, feas):
        self.feas = feas or []

    def setName(self, name):
        self.name = name

    def getChars(self):
        return self.chars

    def getFeas(self):
        return self.feas

    def getName(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return self.autoName()

    def hasChar(self, char):
        if char in self.getChars():
            return True
        else:
            return False

    def hasFea(self, fea):
        if fea in self.getFea():
            return True
        else:
            return False

    def hasName(self, name):
        if self.getName() == name:
            return True
        else:
            return False

    def getGlyphsForChars(self, f):
        glyphs = []
        theseUnicodes = [ord(char) for char in self.getChars()]
        for g in f:
            nameChars = list(GlyphTX.name.getCharacterString(g.name))
            if nameChars == self.getChars():
                glyphs.append(g)
            elif set(g.unicodes).issuperset(set(theseUnicodes)):
                glyphs.append(g)
                for g in f:
                    if GlyphTX.name.getBaseName(g.name) == g.name:
                        glyphs.append(g)
        return glyphs

    def getGlyph(self, f):
        charGlyphs = self.getGlyphsForChars(f)
        feas = self.getFeas()
        for charGlyph in charGlyphs:
            suffixElements = GlyphTX.name.getSuffixElements(charGlyph.name)
            if suffixElements == feas:
                return charGlyph

    def getUnicodeCategory(self):
        chars = self.getChars()
        if chars:
            firstChar = self.getChars()[0]
            return unicodedata.category(firstChar)

    def isUnicodeCategory(self, category):
        if self.getUnicodeCategory()[:len(category)] == category:
            return True
        else:
            return False

    def copy(self):
        return GlyphElement(self.getChars()[:], self.getFeas()[:])

    def autoName(self):
        baseNames = [CharacterTX.char2GlyphName(char) for char in self.getChars()]
        suffixes = [fea for fea in self.getFeas()]
        try:
            return GlyphTX.name.join(baseNames, suffixes)
        except:
            return 'NUL'

    def __repr__(self):
        return '*' + self.getName() + '*'

class GlyphCollection(list):

    def allChars(self):
        chars = []
        for item in self:
            chars.append(u''.join(item.getChars()))
        return chars

    def allFeas(self):
        feas = []
        for item in self:
            for fea in item.getFeas():
                if fea not in feas:
                    feas.append(fea)
        return feas

    def getCategory(self, category):
        result = GlyphCollection()
        for item in self:
            if item.isUnicodeCategory(category):
                result.append(item.copy())
        return result

    def getInFont(self, f):
        result = GlyphCollection()
        for item in self:
            if item.getGlyph(f) is not None:
                result.append(item.copy())
        return result

    def getNotInFont(self, f, omitControls=True):
        result = GlyphCollection()
        for item in self:
            if omitControls and item.getUnicodeCategory() == 'Cc':
                continue
            if item.getGlyph(f) is None:
                result.append(item.copy())
        return result

    def getChar(self, char):
        result = GlyphCollection()
        for item in self:
            if item.hasChar(char):
                result.append(item.copy())
        return result

    def getName(self, name):
        result = GlyphCollection()
        for item in self:
            if item.getName() == name:
                result.append(item.copy())
        return result

    def getSorted(self):
        toSort = []
        for item in self:
            char = item.getChars()[0]
            toSort.append((ord(char), item))
        toSort.sort()
        return GlyphCollection([item for char, item in toSort])

    def getFea(self, fea):
        result = GlyphCollection()
        for item in self:
            if item.hasFea(fea):
                result.append(item.copy())
        return result

    def appendFea(self, fea):
        for item in self:
            feas = item.getFeas()
            feas.append(fea)
            item.setFeas(feas)

    def allNames(self):
        gnames = []
        for item in self:
            gnames.append(item.getName())
        return gnames

    def select(self,
               characterInclude=[],
               characterExclude=[],
               unicodeRangeInclude=[],
               unicodeRangeExclude=[],
               categoryInclude=[],
               categoryExclude=[],
               feaInclude=[],
               feaExclude=[]
               ):
        result = GlyphCollection()
        for item in self:
            include = False
            if characterInclude:
                for char in characterInclude:
                    if char in item.getChars():
                        include = True
            if categoryInclude:
                for category in categoryInclude:
                    if category == item.getUnicodeCategory():
                        include = True
            if feaInclude:
                if feaInclude is True:
                    if item.getFeas():
                        include = True
                else:
                    for fea in feaInclude:
                        if fea in item.getFeas():
                            include = True
            exclude = False
            if characterExclude:
                for char in characterExclude:
                    if char in item.getChars():
                        exclude = True
            if categoryExclude:
                for category in categoryExclude:
                    if category == item.getUnicodeCategory():
                        exclude = True
            if feaExclude:
                if feaExclude is True:
                    if item.getFeas():
                        exclude = True
                else:
                    for fea in feaExclude:
                        if fea in item.getFeas():
                            exclude = True
                        elif fea == None and not item.getFeas():
                            exclude = True

            if include and not exclude:
                result.append(item.copy())
        return result

    def derive(self,
               addFeas=[],
               removeFeas=[],
               characterInclude=[],
               characterExclude=[],
               categoryInclude=[],
               categoryExclude=[],
               unicodeRangeInclude=[],
               unicodeRangeExclude=[],
               feaInclude=[],
               feaExclude=[]
               ):
        selection = self.select(characterInclude, characterExclude, categoryInclude, categoryExclude, unicodeRangeInclude, unicodeRangeExclude, feaInclude, feaExclude)

        for item in selection:
            feas = item.getFeas()
            for addFea in addFeas:
                if addFea not in feas:
                    feas.append(addFea)
            for removeFea in removeFeas:
                if removeFea in feas:
                    feas.pop(removeFea)
        return selection

    def getNamesToElements(self):
        namesToElements = {}
        for i in self:
            namesToElements[i.getName()] = i
        return namesToElements

    def sort(self, type="cannedDesign", allowPseudoUnicode=True):
        from mojo.roboFont import RFont
        try:
            temp = RFont(showUI=False)
        except:
            temp = RFont()
        for gname in self.allNames():
            temp.newGlyph(gname)
        u = UnicodeTX.getUnicodeData(temp)
        sortOrder = u.sortGlyphNames(self.allNames(), sortDescriptors=[dict(type=type, allowPseudoUnicode=allowPseudoUnicode)])
        namesToElements = self.getNamesToElements()
        gc = GlyphCollection()
        for gname in sortOrder:
            gc.append(namesToElements[gname])
        return gc


class CollectionTX:

    FALSE_CATEGORY_UC = [u'Ω', u'Δ', u'Ω']
    FALSE_CATEGORY_LC = [u'ª', u'µ', u'º', u'ƒ', u'μ', u'π']

    @classmethod
    def makeFromChars(cls, chars):
        result = GlyphCollection()
        for char in chars:
            if isinstance(char, int):
                char = chr(char)
            r = GlyphElement([char])
            result.append(r)
        return result

    @classmethod
    def makeFromGlyphNames(cls, gnames):
        result = GlyphCollection()
        for gname in gnames:
            baseNames = GlyphTX.name.getBaseNameElements(gname)
            chars = []
            for baseName in baseNames:
                char = CharacterTX.glyphName2Char(baseName)
                if char is not None:
                    chars.append(char)

            feas = GlyphTX.name.getSuffixElements(gname)
            r = GlyphElement(chars, feas)
            result.append(r)
        return result

if __name__ == "__main__":
    from mojo.roboFont import CurrentFont
    f = CurrentFont()

    # SET INPUT CODEPAGE

    collection = CollectionTX.makeFromGlyphNames(f.keys())
    # collection = GlyphSelectTX.makeGlyphCollection(C.CODEPAGE_LATIN_1)

    # sc = collection.derive(addFeas=['xx'], categoryInclude=['Lu'], characterExclude=CollectionTX.FALSE_CATEGORY_UC, feaExclude=True)

    c = collection.select(characterInclude=[chr(x) for x in range(0, 128)], feaInclude=[], feaExclude=[])
    c = c.sort()
    print(c)
