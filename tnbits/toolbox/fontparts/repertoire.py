# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.toolbox.fontparts.groups import GroupsTX
from tnbits.toolbox.fontparts.kerning import KerningTX
from tnbits.toolbox.glyph import GlyphTX
from tnbits.constants import Constants as C
from tnbits.base.future import chr

class RepertoireTX:
    """
    `RepertoireTX` contains methods for transforming the repertoire of glyphs. Methods usually take a font.
    """

    @classmethod
    def getGlyphOrder(cls, f):
        if f.has_attr('glyphOrder'):
            return f.glyphOrder
        elif 'org.robofab.glyphOrder' in f.lib:
            # FIXME: should this reference fontParts instead?
            return f.lib['org.robofab.glyphOrder']
        return []

    @classmethod
    def getGlyphNamesInOrder(cls, f):
        glyphOrder = cls.getGlyphOrder(f)
        return f.glyphOrder + sorted(set(glyphOrder) - set(f.keys()))

    @classmethod
    def getComposites(cls, f, limitTo=None):
        """

            `getComposites` returns all composite glyphs from a given font. _LimitTo_ is an opitional list which will limit results to composites of only the listed glyphs.

        """
        composites = []
        for g in f:
            if g.components:
                if limitTo:
                    for c in g.components:
                        if c.baseGlyph in limitTo:
                            composites.append(g)
                else:
                    composites.append(g)
        return composites

    @classmethod
    def getSameWidth(cls, target, f):
        """

            `getSameWidth` returns all glyphs with the same width as the _target_ glyph, including target itself.

        """
        results = []
        targetWidth = target.width
        for g in f:
            if g.width == targetWidth:
                results.append(g)
        return results

    @classmethod
    def getSameBbox(cls, target, f):
        """

            `getSameBbox` returns all glyphs with the same bounding box as the _target_ glyph, including the target itself.

        """
        targetBox = target.box
        results = []
        for g in f:
            if g.box == targetBox:
                results.append(g)
        return results

    @classmethod
    def getSameMark(cls, target, f):
        """

            `getSameMark` returns all glyphs with the same color mark as the _target_ glyph, including the target itself.

        """
        targetMark = target.mark
        results = []
        for g in f:
            if g.mark == targetMark:
                results.append(g)
        return results

    @classmethod
    def getModified(cls, f):
        """

            `getModified` returns all glyphs which contains modifications that are not yet saved.

        """
        results = []
        for g in f:
            if g.naked().modified == 1:
                results.append(g)
        return results

    @classmethod
    def getInverse(cls, glyphList):
        """

            `getInverse` returns a list of all glyphs in a font that were not in the given list.

        """
        ''' # Where does "f" come from?
        inverse = []
        for g in f:
            if g not in glyphList:
                inverse.append(g)
        return g
        '''

    @classmethod
    def sortBy(cls, glyphs, glyphOrder):
        glyphNames = cls.getNames(glyphs)
        glyphOrder = cls.getNames(glyphOrder)
        sorted = []
        for sortGlyph in glyphOrder:
            if sortGlyph in glyphNames:
                sorted.append(sortGlyph)
        for glyphName in glyphNames:
            if glyphName not in sortGlyph:
                sorted.append(glyphName)
        return sorted

    @classmethod
    def getGlyphs(cls, gnames=None, f=None, sort=True):
        """

            `getGlyphs` returns a list of all glyphs that exist from a list of gyph names.

        """
        if gnames is None:
            return f.values()
        existing = []
        for gname in gnames:
            try:
                if gname in f:
                    existing.append(f[gname])
            except:
                if gname.name:
                    existing.append(gname)
        if sort:
            existing = cls.sortBy(existing, f.glyphOrder)
        return existing

    @classmethod
    def getNames(cls, glyphs):
        """

            Given a list of glyphs, `getNames` returns a list of corresponding glyph names.

        """
        try:
            return [g.name for g in glyphs]
        except:
            return glyphs

    @classmethod
    def select(cls, f, selection):
        """

            `select` selects a list of glyphs in a font.

        """
        f.selection = [g.name for g in cls.getGlyphs(selection, f)]

    ###############
    # COMPONENT REFERENCES
    ###############

    @classmethod
    def renameComponentReference(cls, sourceName, destName, f):
        """

            `renameComponentReference` changes the baseGlyph of all components with _sourceName_ to _destName_.

        """
        for g in f:
            for c in g.components:
                if c.baseGlyph == sourceName:
                    c.baseGlyph = destName

    @classmethod
    def decomposeComponentReference(cls, gName, f):
        """

            `decomposeComponentReference` decomposes all components whose baseGlyph is the given glyph name, thereby removing all component references to the glyph.

        """
        for g in f:
            for c in g.components:
                if c.baseGlyph == gName:
                    c.decompose()

    @classmethod
    def removeComponentReference(cls, gName, f):
        """

            `removeComponentReference` removes all components with a given base glyph name.

        """
        for g in f:
            for c in g.components:
                if c.baseGlyph == gName:
                    c.removeComponent(c)

    @classmethod
    def removeGlyphAndReferences(cls, gName, f):
        """

            `removeGlyphAndReferences` safely removes a glyph from a font, by making sure component, group, and kerning references to that glyph are also removed. Features coming soon?

        """
        if gName in f:
            # decompose components
            cls.decomposeComponentReference(gName, f)
            # remove group references
            GroupsTX.removeReference(gName, f.groups)
            # remove kerning references
            KerningTX.removeReference(gName, f.kerning)
            # remove from features
            #
            #
            #
            # remove from glyph order
            #
            #
            #
            # remove glyph
            f.removeGlyph(gName)

    @classmethod
    def renameGlyphAndReferences(cls, sourceName, destName, f):
        """

            `renameGlyphAndReferences` safely renames a glyph in a font, by making sure component, group, and kerning references to that glyph are also renamed. Features coming soon?

        """
        if sourceName in f:
            # decompose components
            cls.renameComponentReference(sourceName, destName, f)
            # remove group references
            newGroups = GroupsTX.renameReference(sourceName, destName, f.groups)
            # remove kerning references
            newKerning = KerningTX.renameReference(sourceName, destName, f.kerning)
            # rename in features
            #
            #
            #
            # rename in glyph order
            #
            #
            #
            # rename glyph
            f[sourceName].name = destName


    @classmethod
    def duplicateGlyphAndReferences(cls, sourceName, destName, f, asComponent=True):
        """

            `duplicateGlyphAndReferences` safely renames a glyph in a font, by making sure component, group, and kerning references to that glyph are also renamed. Features coming soon?

        """
        if sourceName in f:
            # decompose components
            #cls.renameComponentReference(sourceName, destName, f)
            # remove group references
            newGroups = GroupsTX.duplicateReference(sourceName, destName, f.groups)
            # remove kerning references
            newKerning = KerningTX.duplicateReference(sourceName, destName, f.kerning)
            g = f.newGlyph(destName)
            g.width = f[sourceName].width
            g.appendComponent(sourceName)
            if not asComponent:
                g.decompose()




    @classmethod
    def getSupportedLanguagesList(cls, f, useImportantSpecialChars=False, returnMissing=False):
        """
        Get a list of supported languages for a font.
        """
        specialChars = C.SPECIAL_CHARS_BY_LANGUAGE_REQUIRED
        # if we are also counting "important" special chars, mix them in
        if useImportantSpecialChars:
            importantChars = C.SPECIAL_CHARS_BY_LANGUAGE_IMPORTANT
            for lang, chars in importantChars.items():
                if lang in specialChars:
                    specialChars[lang] += chars
                else:
                    specialChars[lang] = chars
        # loop through known langauges and look for special chars
        supportedLangs = []
        missing = {}
        for lang, chars in specialChars.items():
            missingFromLang = []
            support = True
            for char in chars:
                try:
                    if not char in f.naked().unicodeData:
                        support = False
                        missingFromLang.append(char)
                except:
                        support = False
                        missingFromLang.append(char)
            if support:
                supportedLangs.append(lang)
            else:
                missing[lang] = missingFromLang

        if returnMissing:
            return supportedLangs, missing
        else:
            return supportedLangs

    @classmethod
    def getSupportedLanguages(cls, f, useImportantSpecialChars=False, returnMissing=False):
        # get supported languages
        languageList = cls.getSupportedLanguagesList(f, useImportantSpecialChars=False, returnMissing=False)
        languageNameList = []
        # convert list of opentype language tags to a list of language names
        for lang in languageList:
            if lang in C.OPENTYPE_LANGUAGE_TAGS:
                languageNameList.append(C.OPENTYPE_LANGUAGE_TAGS[lang])
        languageNameList.sort()
        return languageNameList


    @classmethod
    def swapGlyphs(cls, f, glyphMap):
        for gname, newName in glyphMap.items():
            temp = GlyphTX.name.appendSuffixElement(gname, 'XXXXXXXXXXXXXXXXXXXX')
            cls.renameGlyphAndReferences(newName, temp, f)
            cls.renameGlyphAndReferences(gname, newName, f)
            cls.renameGlyphAndReferences(temp, gname, f)

    @classmethod
    def swapGlyphsBySuffix(cls, f, suffix1, suffix2):
        glyphMap = {}
        mapDict = {suffix1: suffix2}
        for gname in f.keys():
            if GlyphTX.name.hasSuffixElement(gname, suffix1):
                newGname = GlyphTX.name.replaceSuffixElement(gname, mapDict)
                if newGname in f:
                    glyphMap[gname] = newGname
        cls.swapGlyphs(f, glyphMap)

