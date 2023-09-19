# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     character.py
#

import unicodedata

from tnbits.toolbox.transformer import TX
from tnbits.toolbox.glyph import GlyphTX
from tnbits.toolbox.fontparts.unicode import UnicodeTX
from tnbits.constants import Constants as C
from tnbits.base.future import chr

class AbstractCharacterTX:

    @classmethod
    def char2AbstractGlyphName(cls, char): #x
        gname = UnicodeTX.glyphNameForUnicode(ord(char))

        if gname:
            return gname
        else:
            return GlyphTX.name.getUnicodeName([ord(char)])

    @classmethod
    def char2StrictGlyphName(cls, char): #x
        gname = UnicodeTX.strictGlyphNameForUnicode(ord(char))

        if gname:
            return gname
        else:
            # Should not be necessary as this fallback is part of UnicodeTX
            # method.
            return GlyphTX.name.getUnicodeName([ord(char)])

    @classmethod
    def char2AllAbstractGlyphNames(cls, char): #x
        return UnicodeTX.allGlyphNamesForUnicode(ord(char))

    @classmethod
    def glyphName2AbstractChar(cls, glyphName, breakDown=False):
        if not breakDown:
            unicode = UnicodeTX.primaryUnicodeForGlyphName(glyphName)
            if isinstance(unicode, int):
                return chr(unicode)

        characterComponents = []

        for baseName in GlyphTX.name.getBaseNameElements(glyphName):
            unicodeSequence = GlyphTX.name.getUnicodeSequence(baseName)

            if unicodeSequence:
                characterComponents += [chr(u) for u in unicodeSequence]
            else:
                u = UnicodeTX.primaryUnicodeForGlyphName(baseName)
                if u:
                    characterComponents.append(chr(u))

        if characterComponents:
            return ''.join(characterComponents)
        else:
            return None

    @classmethod
    def glyphName2AbstractPseudoChar(cls, glyphName, breakDown=False):
        abstractChar = cls.glyphName2AbstractChar(glyphName, breakDown=breakDown)

        if abstractChar:
            return abstractChar
        else:
            baseName = GlyphTX.name.getBaseName(glyphName)
            return cls.glyphName2AbstractChar(baseName, breakDown=breakDown)

    @classmethod
    def getDecomposition(cls, char):
        """Decomposition."""
        charDec = ord(char)
        decompString = unicodedata.decomposition(char)

        if decompString:
            decompHex = decompString.split(' ')
            decomp = [TX.hex2dec(i) for i in decompHex]
            overrides = {
                290: {807: 806}, # u'Ģ': {u'̦': u'̧'}
                291: {807: 786}, # gcommaccent
                310: {807: 806}, # u'Ķ': {u'̦': u'̧'}
                311: {807: 806}, # u'ķ': {u'̦': u'̧'}
                315: {807: 806}, # u'Ļ': {u'̦': u'̧'}
                316: {807: 806}, # u'ļ': {u'̦': u'̧'}
                325: {807: 806}, # u'Ņ': {u'̦': u'̧'}
                326: {807: 806}, # u'ņ': {u'̦': u'̧'}
                342: {807: 806}, # u'Ŗ': {u'̦': u'̧'}
                343: {807: 806}, # u'ŗ': {u'̦': u'̧'}
                536: {807: 806}, # u'Ș': {u'̦': u'̧'}
                537: {807: 806}, # u'ș': {u'̦': u'̧'}
                538: {807: 806}, # u'Ț': {u'̦': u'̧'}
                539: {807: 806}, # u'ț': {u'̦': u'̧'}
                319: {183: 775}, # Ldot : {periodcentered: dotaccentcmb}
                320: {183: 775} # ldot
                }

            for x, u in enumerate(decomp):
                if charDec in overrides and u in overrides[charDec]:
                    decomp[x] = overrides[charDec][u]

            charList = []

            for d in decomp:
                if isinstance(d, int):
                    charList.append(chr(d))

            return charList
        return None

class CharacterTX(AbstractCharacterTX):

    @classmethod
    def char2GlyphName(cls, char, f=None): #x
        if f is not None:
            unicodeData = UnicodeTX.getUnicodeData(f)
            gname = unicodeData.glyphNameForUnicode(ord(char))

            # Instead of gname in f:, which only works on wrappers, not on
            # naked fonts.
            try:
                return f[gname].name
            except KeyError:
                return None
        else:
            return cls.char2AbstractGlyphName(char)

    @classmethod
    def char2Glyph(cls, char, f): #x
        gname = cls.char2GlyphName(char, f)
        if gname:
            return f[gname]

    @classmethod
    def char2DefaultGlyph(cls, char, f): #x
        u = ord(char)
        charMap = f.getCharacterMapping()
        if u in charMap:
            gname = charMap[u][0]
            return f[gname]

    @classmethod
    def glyphName2Char(cls, glyphName, f=None): #
        if f is not None:
            unicodeData = UnicodeTX.getUnicodeData(f)
            u = unicodeData.unicodeForGlyphName(glyphName)
            if u is not None:
                return chr(u)
        else:
            return cls.glyphName2AbstractChar(glyphName)

    @classmethod
    def glyph2Char(cls, glyph): #x
        f = glyph.font
        return cls.glyphName2Char(glyph.name, f)

    @classmethod
    def glyph2DefaultChar(cls, g): #x
        if g.unicodes:
            return chr(g.unicodes[0])

    @classmethod
    def glyphName2PseudoChar(cls, gname, f=None): #x
        if f is not None:
            unicodeData = UnicodeTX.getUnicodeData(f)
            char = unicodeData.pseudoUnicodeForGlyphName(gname)
            if char:
                return chr(char)
        else:
            return cls.glyphName2AbstractPseudoChar(gname)

    @classmethod
    def glyph2PseudoChar(cls, g, f=None): #x
        if f is None:
            f = g.getParent()

        return cls.glyphName2PseudoChar(g.name, f)

    @classmethod
    def char2DecompositionNames(cls, char):
        """Given a character, get a list of primary glyph names that form up
        the composition."""
        baseNames = []
        for c in char:
            decomposition = cls.getDecomposition(c)
            if decomposition:
                for d in decomposition:
                    gname = cls.char2GlyphName(d)
                    baseNames.append(gname)
            else:
                gname = cls.char2GlyphName(c)
                baseNames.append(gname)
        return baseNames

    @classmethod
    def glyph2Decomposition(cls, g):
        """Given a character, get a list of glyph names that form up the
        composition."""
        f = g.getParent()
        suffixElements = GlyphTX.name.getSuffixElements(g.name)
        baseName = GlyphTX.name.getBaseName(g.name)

        if baseName in f:
            char = cls.glyph2Char(f[baseName])
        else:
            char = cls.glyphName2Char(baseName)

        if char is not None:
            if len(char) == 1:
                baseNames = cls.char2DecompositionNames(char)
            else:
                baseNames = []
                for c in char:
                    baseNames += cls.char2DecompositionNames(c)

            glyphs = []

            for baseName in baseNames:
                suffixedName = GlyphTX.name.appendSuffixElement(baseName, suffixElements)
                g = f[GlyphTX.name.getClosestExistingName(suffixedName, f)]
                glyphs.append(g)
            return glyphs
        return []

    @classmethod
    def pseudoChar2Glyphs(cls, char, f):
        results = []

        for g in f:
            if cls.glyph2PseudoChar(g) == char:
                results.append(g)

        return results



if __name__ == "__main__":
    print('afii61352', CharacterTX.glyphName2Char('afii61352'))
    print('afii61352', CharacterTX.glyphName2Char('numero'))

    import unicodedata

    def roundTrip(char):
        print('-----')
        print(ord(char), unicodedata.name(char))
        gname = CharacterTX.char2GlyphName(char)
        print(gname)
        newChar = CharacterTX.glyphName2Char(gname)
        print(ord(newChar), unicodedata.name(newChar))
        print(CharacterTX.char2GlyphName(newChar))

    roundTrip(chr(699))
    roundTrip(chr(8216))
