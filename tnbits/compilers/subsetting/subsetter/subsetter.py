# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    subsetter.py
#

import copy
import shutil
from tnbits.objects.truetypefont import TrueTypeFont
from tnbits.compilers.subsetting.subsetter.glyphsets import SCRIPTLANGUAGES

class Subsetter(object):

    GLYPH_SPACE = ('space', 0x20) # Must be defined in the font. Used as source for required missing glyphs.
    #GLYPH_NULL = ('.null', None) # Name, unicode
    GLYPH_NOTDEF = ('.notdef', None)
    REQUIREDGLYPHS = (GLYPH_NOTDEF, GLYPH_SPACE)

    def subsetFontPath(self, sourcePath, targetPath, glyphset, script):
        # Copy the source font to the target font. Then we only need to clean it up.
        shutil.copy(sourcePath, targetPath)
        # Copy the source font to the target font.
        font = TrueTypeFont(targetPath)
        self.subsetFont(font, glyphset, script)

    def error(self, s):
        print('### ERROR', s)

    def report(self, s):
        print('... Report:', s)

    def addTargetGlyphName(self, glyphNameSet, glyphUnicodeSet, glyphName, font):
        """Expand the glyphNameSet with the all the (nested) names in the components
        of the glyphs in the set. Since glyphNameSet is a Set instance, it does
        not matter if the same glyph name gets added multiple times."""
        glyph = None
        if glyphName in font:
            glyph = font[glyphName]
            glyphNameSet.add(glyphName)
            if glyph.unicode:
                glyphUnicodeSet.add(glyph.unicode)
            # Check if there are any component in this glyph that are not part of the font yet.
            for componentGlyphName in font[glyphName].getComponentNames():
                componentGlyph = font[componentGlyphName]
                if componentGlyph is None:
                    self.error('Referred component glyph "%s" by "%s" is missing from the font' % (componentGlyphName, glyphName))
                else:
                    glyphNameSet.add(componentGlyphName)
                    if componentGlyph.unicode:
                        glyphUnicodeSet.add(componentGlyph.unicode)
        return glyph

    def subsetGSUB(self, script, font, targetGlyphNames):
        #
        # G S U B
        #
        # If we get here, we can assume that we know all the requered glyphs with a unicode, expanded
        # to the possible non-unicode glyphs that are used as component.
        # Additionally we have to make an additional check in the GSUB result glyph set, to see what
        # extra glyphs need to be kept in the output, because they
        # used as substituted glyph. And then again, these can contain component that also need to be
        # check for existence.
        # Next is to clean up the GSUB by deleting all scripts-feature-lookups that are not in the script set of the model font.
        targetGSUB = font.gsub
        if targetGSUB is None:
            self.report('[GSUB] Warning: No GSUB table in the font.')
        else:
            # Do the actual deletion of the unwanted scripts.
            self.deleteScripts(targetGSUB, SCRIPTLANGUAGES[script].keys())
            # Now we have a GSUB that only contains the same script names as the requested glyph list has,
            # where we are sure that all glyphs in the GSUB/GPOS exist in the source/target font.
            # Next thing is to delete all languages (and features) that don't exist in the model font.
            self.deleteUnusedLanguages(targetGSUB, SCRIPTLANGUAGES[script])
            # Next is to clean all GSUB lookups, where the input glyph is not in the target list.
            # After that is cleaned, the remaining glyphs in the GSUB, are supposed to extend the
            # target glyph list, because these are the substituted glyphs that may not have a unicode.
            # Also add these glyphs to the target list.
            # Note that we have to do the GSUB first (before GPOS and GDEF), in order to complete the
            # list of glyphs that we need in the target.
            # Make sure just to test on the input glyph names of the GSUB and later add all glyphs
            # of GSUB again to the targetGlyphNames, as there may be output glyphs that we don't
            # know yet.

            # Delete addition glyphs, as define in the REMOVEGLYPHS table,
            # specific for weight-script
            for glyphName in set(targetGSUB.getInputGlyphNames()):
                # Delete input glyphs only if it is not in the targetGlyphNames and it has a unicode
                if font[glyphName] is not None and font[glyphName].unicode and not glyphName in targetGlyphNames:
                    # The GSUB input is using a glyph that does not exist in the target list. This is caused
                    # by bad GSUB (when it does not exist in the source font at all) or it can be
                    # used by glyphs that will be removed by the subsetting, remove the glyphName
                    # from the GSUB, anywhere in the lookups where it is used. Since that can be very deep,
                    # we let the lookups do the work themselves. Since many of the coverate.glyphs lists
                    # will become empty, we'll clean up the emptied lookups later, by cutting the live wires
                    # to them.
                    targetGSUB.deleteInputGlyph(glyphName)
                    targetGSUB.deleteOutputGlyph(glyphName)
            # So far we only cleaned the input glyphs with a unicode. But we also can have the situation where the input
            # glyph does not have a unicode. In that case its existence depends on the usage on the output or as part of a composite.
            targetGSUB.cleanUp() # Delete lookups with empty inputs
            # Now the input glyphs are cleaned, we have to add the remaining output glyphs to the target list.
            # Clean up the targetGSUB for all lookups that no longer have input glyphs,
            # to release all hard links to removed state instances. All lookups with just dead weakrefs
            # will drop out.
            #targetGSUB.cleanUp() # Delete lookups with empty inputs
            #
            # Now GSUB only contains the glyphs that are really available in the target font.
            # And targetGlyphNames contains all the glyph names that should be in the target font (so far)
            #

    def subsetGPOS(self, script, font, targetGlyphNames):
        #
        # G P O S
        #
        # Then we do almost the same with GPOS as we did with GSUB. Delete the scripts that we don't need.
        targetGPOS = font.gpos
        if targetGPOS is None:
            self.report('[GPOS] Warning: No GPOS table in the font.')
        else:
            #modelGPOS = modelFont.gpos
            self.deleteScripts(targetGPOS, SCRIPTLANGUAGES[script].keys())
            # GPOS is different from GSUB, that is will not add new/extra glyphs to the set.
            # So we will match the glyphs in GPOS not to exceed the required glyphs that we already got.
            # Is that good reasoning?
            # Next thing is to delete all languages and features that don't exist in the model font.
            # Bottom up, delete the features that are not in the model font, before deleting the unused languages.
            #self.deleteUnusedFeatures(targetGPOS)
            self.deleteUnusedLanguages(targetGPOS, SCRIPTLANGUAGES[script])
            # Get the set with names of glyphs in the source/target GPOS that have a unicode.
            # All remaining glyphs in the GPOS should be in the requiredGlyphNames name list.
            for glyphName in targetGPOS.getGlyphNames():
                if not isinstance(glyphName, str):
                    self.error() # Was an error, test to be sure, otherwise glyph are deleted.
                if not glyphName in targetGlyphNames:
                    # If not existing in the source/target font, delete it from the lookups.
                    targetGPOS.deleteGlyph(glyphName)
            # Finally clean up the targetGPOS, to release all hard links to removed state instances.
            #targetGPOS.cleanUp()
            # Now GPOS only contains the glyphs that are really available in the target font.
            # And targetGlyphNames contains all the glyph names that should be in the target font (so far)

    def subsetGDEF(self, script, font, targetGlyphNames):
        #
        # S U B S E T  G L Y P H S
        #
        # Now we have a clean GPOS/GSUB. All glyphs we need in the subset is a union of the sets below:
        # - All glyphs referred to by the cleaned GPOS as they exist in the target font glyph set.
        # - All glyphs referred to by the cleaned GSUB as they exist in the target font glyph set.
        # - All target glyphs with unicode that have a match in the model font with a unicode
        # - All components glyphs from the glyphs in the union of the above sets.
        # If the GSUB was cleaned enough, all of gsubGlyphNames should be in targetGlyphNames
        #if DEBUG:
        #    self.report('Total gsubGlyphNames %d' % len(targetGSUB.getGlyphNames()))
        #    self.report('Total gposGlyphNames %d' % len(targetGPOS.getGlyphNames()))
        #    self.report('Total targetGlyphNames %d' % len(targetGlyphNames))
        #
        # G D E F
        #
        # Only keep the glyphs in GDEF that are really in the output font.
        # We have to do this, before deleting the glyphs from the font, or else FontTools give an error.
        targetGDEF = font.gdef
        if targetGDEF is None:
            self.report('[GDEF] Warning: No GDEF table in the font.')
        else:
            deleteCount = 0
            for glyphName in sorted(targetGDEF.getGlyphNames()):
                if not glyphName in targetGlyphNames:
                    # If not existing in the source/target font, delete it from the lookups.
                    targetGDEF.deleteGlyph(glyphName)
                    deleteCount += 1
            self.report('[GDEF] Deleted %s source/target glyphs.' % deleteCount)

    def subsetCMAP(self, script, font, targetGlyphNames):
        #
        # C M A P
        #
        targetCmap = font.cmap
        for table in targetCmap.tables:
            for unicodeValue, glyphName in table.cmap.items():
                if not glyphName in targetGlyphNames:
                    del table.cmap[unicodeValue]

    def subsetKERN(self, script, font, targetGlyphNames):
        #
        # K E R N
        #
        # Cleanup the kern table for all glyph pairs that have one or two not in finalGlyphNames.
        # Because it is simple with no references, we do that directly on the FontTools table object.
        kern = font.kern
        if kern is None:
            self.report('[kern] Warning: No kern table in the font.')
        else:
            kernTables = kern.kernTables
            kernCount = 0
            deleteCount = 0
            newKernTables = []
            for kernRecord in kernTables:
                for glyphName1, glyphName2 in kernRecord.kernTable.keys():
                    if not glyphName1 in targetGlyphNames or not glyphName2 in targetGlyphNames:
                        del kernRecord.kernTable[(glyphName1, glyphName2)]
                        deleteCount += 1
                    else:
                        kernCount += 1
                # If finally the kern subtable did not become empty, then add it again to the new set or subtables.
                if kernRecord.kernTable:
                    newKernTables.append(kernRecord)
            kern.kernTables = newKernTables
            self.report('[kern] Deleted %s kerning pairs.' % deleteCount)
            self.report('[kern] Remaining %s kerning pairs.' % kernCount)

    def subsetGlyphs(self, script, font, targetGlyphNames):
        #
        # F I N A L L Y  D E L E T E  U N W A N T E D  G L Y P H S
        #
        # Now we have the final list of glyphs for the target font. Remove all the others.
        for glyphName in sorted(font.keys()):
            if not glyphName in font:
                print('### Warning DOSUBSET: Expected glyph "%s" does not exist in the target font.' % glyphName)
            if not glyphName in targetGlyphNames:
                del font[glyphName]

    def deleteScripts(self, targetGTable, requiredScriptNames):
        # Delete the scripts in targetGTable that are not in requiredScriptNames
        # Note that later in the subsetting process, if features and lookups are cleaned,
        # we also need to check if the required scripts did become empty too.
        # In that case they are removed too.
        for script in targetGTable.scripts.keys():
            if not script in requiredScriptNames:
                targetGTable.deleteScript(script)

    def deleteUnusedLanguages(self, targetGTable, modelLanguageNames):
        # Delete all the languages from the targetGTable.languages list that either
        # have a reference to a dead script or which name is not in modelLanguageNames.
        # @@@ Special care needs to be taken to the dflt language.
        # Question is what happens with the features and lookups that were referenced by
        # the deleted languages. This needs to be checked by the keepIt() of the feature
        # and lookup instances.
        deletedLanguages = set()
        cleanedLanguages = []
        for language in targetGTable.languages:
            # Always add DFLT if is exists.
            if language.script is not None and language.script.tag == 'DFLT':
                cleanedLanguages.append(language)
            elif language.script is not None and \
                language.script.tag in modelLanguageNames.keys() and \
                language.tag in modelLanguageNames[language.script.tag]:
                cleanedLanguages.append(language)
            else:
                deletedLanguages.add(language.tag)
                #self.report('\tDeleting language "%s" KeepIt=%s script=%s glyphs=%s' % (language.tag, language.keepIt(), language.script, sorted(language.getGlyphNames())))
        targetGTable.languages = cleanedLanguages
        self.report('\tDeleting language(s) "%s" that are not part of the language script.' % ', '.join(sorted(deletedLanguages)))

    def copyGlyph(self, font, name=None, unicodeValue=None, srcName=None):
        # Copy the glyph from the fallbackFont to the targetFont.
        # If the unicode attribute is defined, then find the glyph in the fallbackFont by unicode.
        # Otherwise find it by name. If the srcName attribute is defined, then copy from there
        # to name in the targetFont.
        glyph = srcGlyph = None
        if unicodeValue is not None:
            srcGlyph = font.glyphByUnicode(unicodeValue)
        elif srcName is not None or name is not None:
            srcGlyph = font[srcName or name]
        else:
            raise ValueError
        if srcGlyph is not None:
            font[name] = glyph = copy.copy(srcGlyph)
            if not name in font.glyphOrder:
                font.glyphOrder = [name] + font.glyphOrder
        return glyph


    def subsetFont(self, font, glyphset, script):
        # So, we are going to subset this font here, which is a fresh clean copy of the source font.
        # This means that all glyphs and all GSUB/GPOS/GDEF language subtables are available, we just have to check the
        # minimum set that is needed according to the glyphset and the request scripts and then delete the rest in the font.
        # There are some resources for the new set of glyphs that need to match:
        #    - All glyphs with a unicode or name identical to the one the glyphset, need to go into the font.
        #        The glyphset can be a dictionary {unicode: name} or a list of glyph names.
        #    - All glyphs that are (recursively) referred as component in this resulting glyph set should be added too.
        #        The list of requested glyphs is build as expansion of the glyph list.
        #        Add all glyphs that expand from the original glyphset that fit the requested scripts.
        #    - Delete all scripts and features and lookups from the target font that have no reference to any of
        #        the final target glyph set
        #    - Delete all glyphs in the target font that are in the final list of request glyphs.
        #
        # C O M P A R E  G L Y P H S E T S
        #
        # Collect all the glyphs in the target font that need to be kept (we will
        # delete the glyphs from a full copy of the source font). This includes
        # all the glyphs matching the requested set of unicodes, and also the glyphs that
        # are referred to by components. Later the GPOS and GSUB alternates will be added
        # to the list, if they are found to be necessary in the remaining feature lookups.
        # This list must be done by names (although the internal naming of the font
        # glyphs don't have value outside the font), because not all glyphs have a unicode.
        #
        # Storage of the final target glyph set of names, unicode + non-unicode
        targetGlyphNames = set()
        # Collect the unicode entry points
        targetGlyphUnicodes = set()
        # Check for all required unicodes if they exists. Otherwise copy from the fallback font.
        # Get the unicodes from the glyphset and make sure they are all in the target font.
        # Otherwise copy the glyph from the fallback font.

        # In case the glyphset is a {unicode: glyphName} dictionary
        if isinstance(glyphset, dict):
            for unicodeValue in sorted(glyphset.keys()):
                glyph = font.glyphByUnicode(unicodeValue)
                if glyph is None:
                    self.error('Required glyph with unicode "%s" is missing from the font' % unicodeValue)
                else:
                    # There is a matching glyph, now add it to the target list, and also add the (recursively nested)
                    # name(s) of any component glyph that it contains. It is important to do it right away, or else
                    # the subsetting needs to be done in several passes. Any time a component glyph gets added
                    # to the list, this also can have effect on the lookups to be kept.
                    self.addTargetGlyphName(targetGlyphNames, targetGlyphUnicodes, glyph.name, font)

        else: # glyphset must be a list of glyph names.
            for glyphName in glyphset:
                if not glyphName in font:
                    self.error('Required glyph "%s" is missing from the font' % glyphName)
                else:
                    # There is a matching glyph, now add it to the target list, and also add the (recursively nested)
                    # name(s) of any component glyph that it contains. It is important to do it right away, or else
                    # the subsetting needs to be done in several passes. Any time a component glyph gets added
                    # to the list, this also can have effect on the lookups to be kept.
                    self.addTargetGlyphName(targetGlyphNames, targetGlyphUnicodes, glyphName, font)

        # Add the required glyphs that are not part of the standard glyphset
        for glyphName, glyphUnicode in self.REQUIREDGLYPHS:
            targetGlyphNames.add(glyphName)
            if not glyphName in font:
                glyph = self.copyGlyph(font, name=glyphName, srcName=self.GLYPH_SPACE[0]) # Space must be there!
                if glyph is not None and glyphUnicode is not None:
                    targetGlyphUnicodes.add(glyphUnicode)

        # Now targetGlyphNames contains all the glyphs that we need in the subset that have unicode or are
        # expanded component glyphs of the unicode glyphs. In principle this list should be enough as input
        # selection of GPOS, GSUB and GDEF, but in practice it happens that also non-unicode glyphs can
        # be on the input side. This can be valid, in case they are also used as output glyph somewhere
        # or if they are a component in one of the output glyphs.
        #
        # G S U B
        #
        self.subsetGSUB(script, font, targetGlyphNames)
        #
        # G P O S
        #
        self.subsetGPOS(script, font, targetGlyphNames)
        #
        # G D E F
        #
        self.subsetGDEF(script, font, targetGlyphNames)
        #
        # C M A P
        #
        self.subsetCMAP(script, font, targetGlyphNames)
        #
        # K E R N
        #
        self.subsetKERN(script, font, targetGlyphNames)
        #
        # O T H E R  T A B L E S
        #
        # We don't have to delete the rest of unwanted tables from the target font,
        # because the SegoeFont.save() will create another new TTFont and only
        # copy/create the tables that that are needed in the output. This means
        # that all unwanted tables in the current font will not be copied.
        # @@@ We could think of a mechanism to select which tables get copied or not
        # (such as the [kern] table) to make it general and optional.
        #
        # Cleanup again, as some of the script or languages mat have become empty now.
        font.gsub.cleanUp()
        font.gpos.cleanUp()

        for script in font.gsub.scripts.values():
            for language in script.languages.values():
                for feature in language.features:
                    for lookup in feature.lookups:
                        for keepGlyphName in lookup.getGlyphNames():
                            glyph = font[keepGlyphName]
                            self.addTargetGlyphName(targetGlyphNames, targetGlyphUnicodes, glyph.name, font)

        # Now the input glyphs are cleaned, we have to add the remaining output glyphs to the target list.
        # Clean up the targetGSUB for all lookups that no longer have input glyphs,
        # to release all hard links to removed state instances. All lookups with just dead weakrefs
        # will drop out.
        # Cleanup again, as some of the script or languages mat have become empty now.
        #font.gsub.cleanUp()
        #font.gpos.cleanUp()
        #
        # Check and show what the difference is between the collected targetGlyphNames and
        # the original request for unicode glyphs.
        #
        # Now GSUB and GPOS only contains the glyphs that are really available in the target font.
        # And targetGlyphNames contains all the glyph names that should be in the target font (so far)
        #
        self.subsetGlyphs(script, font, targetGlyphNames)

        #
        # Save the font created target font.
        #
        font.save()
        print('...... Done saving')


