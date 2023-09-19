# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    subset2.py
#
import os, shutil, copy
from tnbits.objects.truetypefont import TrueTypeFont, TTFCompiler
from tnbits.proofing.webproof.exportproof import Proof

DEBUG = True
DOSUBSET = True
REPORT2FILE = True
EXITFATAL = False

GENERATE_SOURCE_PROOF = False
GENERATE_TARGET_PROOF = True
SAVE_OT_SPECIMEN_PAGE_SOURCE = False
# Make true, to generate the (complete) output, with patched EOT OS/2 values.
# Copy the generated EOT into to delivery that is generated with this parameter set to False.
RUN_EOT_OS2_PATCHES = False

from glyphsets import GLYPHSETS

class SegoeFont(TrueTypeFont):
    # Inherit the TrueTypeFont, to redefine the creation of certain tables.

    def TTFCompilerClass(self):
        # Allow inheriting classes from TrueTypeFont define their own compiler class.
        # E.g. to define alternative handling of certain tables, such as the copy of
        # of OS/2 values in Segoe, instead of recalculating them.
        return SegoeCompiler

class SubsetProof(Proof):
    SHOW_SIZES = False
    SHOW_KERNING = True

class SegoeCompiler(TTFCompiler):
    pass

class Subsetter(object):
    def __init__(self):
        self._report = None

    def openReport(self, name=None):
        if self._report is None:
            try:
                os.makedirs(self.REPORTPATH)
            except OSError: # Skip if it already exists.
                pass
            self._report = open(self.REPORTPATH + '/' + (name or '~Report.txt'), 'w')

    def closeReport(self):
        if self._report is not None:
            self._report.close()
            self._report = None

    def report(self, s):
        print(s)
        if self._report is None:
            print(s)
        else:
            self._report.write(s + '\n')

    def reportLine(self):
        self.report('-'*80)

    def buildProof(self, paths):
        SubsetProof.buildPaths(paths)


class SegoeSubsetter(Subsetter):

    ROOT = '/FontDevelopment/_TTF/SegoeWorkSpace'
    #SOURCES = ROOT + '/Sources'
    SOURCES = ROOT + '/Sources2'
    SRCPATH = SOURCES + '/SegoeUI-%s%s-All.ttf'
    FALLBACKPATH = SRCPATH % ('Fallback', '') # Copy from here if a required glyph (such as .notdef') is not in the source font.
    MODELS = ROOT + '/Models'
    MODELPATH = MODELS + '/%s/SegoeUI-%s%s-%s.ttf'
    TARGETS = ROOT + '/Targets'
    if RUN_EOT_OS2_PATCHES:
        TARGETS = TARGETS+'-EOT-PATCH'
    TARGETPATH = TARGETS + '/SegoeUI-%s%s-%s.ttf'
    REPORTPATH = TARGETS + '/~Reports'

    # Thai needs another source file
    THAI_SRCPATH = SOURCES + '/SegoeUI-%s%s-Thai.ttf'

    #TARGET_SCRIPTS = ('Arabic', 'Cyrillic', 'East European', 'Greek', 'Hebrew', 'Thai', 'Vietnamese', 'West European')
    #TARGET_SCRIPTS = ('Cyrillic', 'East European', 'Greek', 'Hebrew', 'Thai', 'Vietnamese', 'West European')
    #TARGET_SCRIPTS = ('Arabic', 'Cyrillic', 'Kazakh', 'East European', 'Greek', 'Hebrew', 'Thai', 'Vietnamese', 'West European')
    #TARGET_SCRIPTS = ('Cyrillic', 'West European')
    #TARGET_SCRIPTS = ('West European',)
    #TARGET_SCRIPTS = ('Vietnamese',)
    #TARGET_SCRIPTS = ('Greek',)
    TARGET_SCRIPTS = ('Hebrew',)
    #TARGET_SCRIPTS = ('Vietnamese','Hebrew', 'Arabic')
    #TARGET_SCRIPTS = ('Thai',)
    #TARGET_SCRIPTS = ('Arabic',)
    #TARGET_SCRIPTS = ('Cyrillic',)

    TARGET_WEIGHTS = ('Regular', 'Bold', 'Light', 'SemiBold', 'SemiLight')
    #TARGET_WEIGHTS = ('Regular', 'Bold', 'SemiBold', 'SemiLight') # Problems with the light
    TARGET_WEIGHTS = ('Light',)
    #TARGET_WEIGHTS = ('SemiLight',)
    #TARGET_WEIGHTS = ('Bold', )
    #TARGET_WEIGHTS = ('Regular', )

    TARGET_STYLES = ('', '-Italic')
    #TARGET_STYLES = ('-Italic',)
    TARGET_STYLES = ('',)

    # Languages per script

    SCRIPTLANGUAGES = {
        'Arabic': {
            'DFLT': ('*',),
            'arab': ('ARA', 'MLY', 'MOR', 'SND', 'URD'),
            'cyrl': ('dflt',),
            'grek': ('dflt',),
            'hebr': ('dflt',), # In model Regular, SemiLight. Not in model Bold, Light, Semibold,
            'latn': ('dflt', 'TRK'),
        },
        'Cyrillic': {
            'DFLT': ('*',),
            'cyrl': ('dflt', 'MKD', 'SRB'), # 'MKD', 'SRB' in model Bold-Italic
            'latn': ('dflt', 'TRK'),
        },
        'East European': {
            'DFLT': ('*',),
            'latn': ('dflt', 'TRK'),
        },
        'Greek': {
            'DFLT': ('*',),
            'grek': ('dflt',),
            'latn': ('dflt', 'TRK'),
        },
        'Hebrew': {
            'DFLT': ('*',),
            'hebr': ('dflt',), # Not in model Bold, Semibold
            #'latn': ('dflt', 'TRK'),
        },
        'Thai': {
            'DFLT': ('*',),
            'thai': ('dflt'),
        },
        'Vietnamese': {
            'DFLT': ('*',),
            'latn': ('dflt', 'TRK'),
        },
        'West European': {
            'DFLT': ('*',),
            'latn': ('dflt', 'TRK'),
        },
    }
    # G L Y P H names
    GLYPH_NULL = '.null'
    GLYPH_NOTDEF = '.notdef'
    #GLYPH_FRACTION = 'fraction' # Make sure that the light GSUB does not collapse
    REQUIREDGLYPHS = (GLYPH_NULL, GLYPH_NOTDEF) #, GLYPH_FRACTION)

    def fatal(self, s):
        print(s)
        raise 'Fatal error'

    def doSubset(self, script):
        # Answer if the target font should be subset
        return DOSUBSET

    def buildProof(self, path):
        base, fileAndExt = os.path.split(path)
        proofBase = os.path.join(base, 'proof')
        try:
            os.makedirs(proofBase)
        except:
            pass # Exists, ignore
        outputPath = os.path.join(proofBase, fileAndExt.replace('.ttf', '.html'))
        webFontBase = os.path.join(proofBase, 'fonts')
        try:
            os.makedirs(webFontBase)
        except:
            pass # Exists, ignore
        print('... Build proof', webFontBase)
        Proof.simpleBuild(path, outputPath, webFontBase)

    def subsetAll(self):
        if REPORT2FILE:
            self.openReport()
        for weight in self.TARGET_WEIGHTS:
            for style in self.TARGET_STYLES:
                self.subsetWeightStyle(weight, style)
        # Build the proof
        if GENERATE_TARGET_PROOF:
            for fileName in os.listdir(self.TARGETS):
                if fileName.endswith(".ttf"):
                    path = self.TARGETS + '/' + fileName
                    self.buildProof(path)

    def compareFileSizes(self):
        self.openReport('~CompareSizes.txt')
        modelTotal = 0
        targetTotal = 0
        totalFonts = 0
        for dirName in os.listdir(self.MODELS):
            modelDir = self.MODELS + '/' + dirName
            targetDir = self.TARGETS + '/' + '/'.join(dirName.split('/')[1:])
            if os.path.isdir(modelDir):
                for fileName in os.listdir(modelDir):
                    if fileName.endswith('ttf') and os.path.exists(targetDir + '/' + fileName):
                        totalFonts += 1
                        modelSize = os.path.getsize(modelDir + '/' + fileName)
                        modelTotal += modelSize
                        targetSize = os.path.getsize(targetDir + '/' + fileName)
                        targetTotal += targetSize
                        reduction = int(round((1-1.0*targetSize/modelSize)*100))
                        modelSize = int(modelSize/1000)
                        targetSize = int(targetSize/1000)
                        if reduction < 0:
                            label = '++++++ %3d%% Larger ' % -reduction
                        elif reduction == 0:
                            label = '            Equal  '
                        else:
                            label = '------ %3d%% Smaller' % reduction
                        line = '%s %s Model %dk Target %dk' % (label, fileName, modelSize, targetSize)
                        print(line)
                        self.report(line)

        if modelTotal:
            line = '\nTotal number of fonts %d, Total %0.2f%% saved' % (totalFonts, (1-float(targetTotal)/modelTotal)*100)
            print(line)
            self.report(line)
        self.closeReport()


    def subsetWeightStyle(self, weight, style):
        fallbackFont = SegoeFont(self.FALLBACKPATH) # Copy requested missing glyphs from here
        orgSourcePath = self.SRCPATH % (weight, style)
        if GENERATE_SOURCE_PROOF:
            self.buildProof(orgSourcePath)
        for script in self.TARGET_SCRIPTS:
            scriptName = script.replace(' ', '')
            # Model fonts are only used for existence check (to know which target font to generate,
            # as not all combinations of scriptNane+weight+style are needed in the target set),
            # and for some preset OS/2 values that need to be maintained.
            # Note that currently the rest of the information in the model fonts is too unreliable to use.
            modelPath = self.MODELPATH % (scriptName, weight, style, scriptName)
            if os.path.exists(modelPath): # Test if we need this target font.
                modelFont = SegoeFont(modelPath)
                if scriptName == 'Thai': # Thai has special separate source.
                    srcPath = self.THAI_SRCPATH % (weight, style)
                else:
                    srcPath = orgSourcePath
                targetPath = self.TARGETPATH % (weight, style, scriptName)
                # Make sure that the path exists
                try:
                    os.makedirs('/'.join(targetPath.split('/')[:-1]))
                except OSError:
                    pass # It exists, ignore.

                print('Subsetting from source', srcPath)

                # Make a copy of the source path to the target path
                shutil.copy(srcPath, targetPath)
                print('...... Target', targetPath)
                targetFont = SegoeFont(targetPath)
                # Get the glyphset for this script
                glyphset = self.getGlyphset(script) # Key is unicode, value is unicode glyph name
                # Excecute the actual subsetting of the targetFont
                self.subsetFont(targetFont, modelFont, fallbackFont, weight, style, script, glyphset)

    def getGlyphset(self, script):
        # Get the glyphset name for this script
        return GLYPHSETS[script.replace(' ', '')]

    def copyGlyph(self, fallbackFont, targetFont, name=None, unicodeValue=None, srcName=None):
        # Copy the glyph from the fallbackFont to the targetFont.
        # If the unicode attribute is defined, then find the glyph in the fallbackFont by unicode.
        # Otherwise find it by name. If the srcName attribute is defined, then copy from there
        # to name in the targetFont.
        glyph = fallbackGlyph = None
        if unicodeValue is not None:
            fallbackGlyph = fallbackFont.glyphByUnicode(unicodeValue)
            if fallbackGlyph is None:
                self.report('?????? Warning: Requested unicode glyph "%04X" missing in source font and fallback font.' % unicodeValue)
            else:
                name = fallbackGlyph.name
                if srcName is None:
                    srcName = name
                self.report('?????? Warning: Substituting missing unicode glyph "%04X" by fallback font glyph "%04X"' % (unicodeValue, unicodeValue))
        elif name is not None:
            if srcName is None:
                srcName = name
            if srcName in fallbackFont:
                self.report('?????? Warning: Substituting missing glyph "%s" from fallback font glyph "%s"' % (name, srcName))
                fallbackGlyph = fallbackFont[srcName]
            else:
                self.fatal('###### Error: required glyph "%s" does not exist in fallback font' % name)
        else:
            raise ValueError
        if fallbackGlyph is not None:
            targetFont[name] = glyph = copy.copy(fallbackGlyph)
            targetFont.hmtx.metrics[name] = fallbackFont.hmtx.metrics[srcName]
            if not name in targetFont.glyphOrder:
                targetFont.glyphOrder = [name] + targetFont.glyphOrder
        return glyph

    def addTargetGlyphName(self, glyphNameSet, glyphUnicodeSet, glyphName, fallbackFont, font):
        # Expand the glyphNameSet with the all the (nested) names in the components
        # of the glyphs in the set. Since glyphNameSet is a Set instance, it does
        # not matter if the same glyph name gets added multiple times.
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
                    # Can be, if the glyph was copied from a fallback font, and the components not yet.
                    componentGlyph = self.copyGlyph(fallbackFont, font, name=componentGlyphName)
                if componentGlyph is not None:
                    glyphNameSet.add(componentGlyphName)
                    if componentGlyph.unicode:
                        glyphUnicodeSet.add(componentGlyph.unicode)
                else:
                    self.report('[addTargetGlyphName] Could not find component "%s" in fallback font.' % componentGlyphName)
        return glyph

    def subsetGSUB(self, weight, style, script, targetFont, targetGlyphNames, modelFont):
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
        targetGSUB = targetFont.gsub
        if SAVE_OT_SPECIMEN_PAGE_SOURCE:
            targetGSUB.saveSpecimenPage(targetFont, targetFont.path+'.Source')
        # Just to show how incomplete these are.
        modelGSUB = modelFont.gsub
        modelGSUB.saveSpecimenPage(modelFont, targetFont.path+'.Model')
        # Do the actual deletion of the unwanted scripts.
        self.deleteScripts(targetGSUB, self.SCRIPTLANGUAGES[script].keys())
        # Now we have a GSUB that only contains the same script names as the requested glyph list has,
        # where we are sure that all glyphs in the GSUB/GPOS exist in the source/target font.
        # Next thing is to delete all languages (and features) that don't exist in the model font.
        self.deleteUnusedLanguages(targetGSUB, self.SCRIPTLANGUAGES[script])
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
        """
        key = '%s-%s' % (weight, script) # No italic exceptions
        removeGlyphs = REMOVEGLYPHS.get(key)
        if removeGlyphs is not None:
            for glyphName in removeGlyphs:
                if glyphName in targetGlyphNames:
                    targetGlyphNames.remove(glyphName)
                targetGSUB.deleteGlyph(glyphName)
        """
        for glyphName in set(targetGSUB.getInputGlyphNames()):
            # Delete input glyphs only if it is not in the targetGlyphNames and it has a unicode
            """
            if glyphName == 'afii57664':
                print('afii57664' in targetGlyphNames)
                print(targetFont[glyphName], targetFont[glyphName].unicode)
                pass
            if glyphName == 'glyph03911':
                print('glyph03911' in targetGlyphNames)
                print(targetFont[glyphName], targetFont[glyphName].unicode)
                pass
            """
            if targetFont[glyphName] is not None and targetFont[glyphName].unicode and not glyphName in targetGlyphNames:
                # The GSUB input is using a glyph that does not exist in the target list. This is caused
                # by bad GSUB (when it does not exist in the source font at all) or it can be
                # used by glyphs that will be removed by the subsetting, remove the glyphName
                # from the GSUB, anywhere in the lookups where it is used. Since that can be very deep,
                # we let the lookups do the work themselves. Since many of the coverate.glyphs lists
                # will become empty, we'll clean up the emptied lookups later, by cutting the live wires
                # to them.
                targetGSUB.deleteInputGlyph(glyphName)

        # Now the input glyphs are cleaned, we have to add the remaining output glyphs to the target list.
        # Clean up the targetGSUB for all lookups that no longer have input glyphs,
        # to release all hard links to removed state instances. All lookups with just dead weakrefs
        # will drop out.
        targetGSUB.cleanUp() # Delete lookups with empty inputs

        # So far we only cleaned the input glyphs with a unicode. But we also can have the situation where the input
        # glyph does not have a unicode. In that case its existence depends on the usage on the output or
        # as part of a composite.

        for chn in targetGSUB.getInputGlyphNames():
            if not targetFont[chn].unicode:
                print(2432343434, chn)

        #
        # Now GSUB only contains the glyphs that are really available in the target font.
        # And targetGlyphNames contains all the glyph names that should be in the target font (so far)
        #

    def subsetGPOS(self, weight, style, script, targetFont, targetGlyphNames, modelFont):
        #
        # G P O S
        #
        # Then we do almost the same with GPOS as we did with GSUB. Delete the scripts that we don't need.
        targetGPOS = targetFont.gpos
        #modelGPOS = modelFont.gpos
        if DEBUG:
        #    self.dumpGPOS(self.REPORTPATH + '/DEBUG-GPOS.xml', targetGPOS) # Use to compare unchanged XML output
        #    self.report('[GPOS] Model scripts%s' % modelGPOS.scripts.keys())
            self.report('[GPOS] Source/target scripts%s' % targetGPOS.scripts.keys())
        if self.doSubset(script):
            self.deleteScripts(targetGPOS, self.SCRIPTLANGUAGES[script].keys())
        if DEBUG:
            self.report('[GPOS] Target scripts after subset %s' % targetGPOS.scripts.keys())
        # GPOS is different from GSUB, that is will not add new/extra glyphs to the set.
        # So we will match the glyphs in GPOS not to exceed the required glyphs that we already got.
        # Is that good reasoning?
        # Next thing is to delete all languages and features that don't exist in the model font.
        # Bottom up, delete the features that are not in the model font, before deleting the unused languages.
        #self.deleteUnusedFeatures(targetGPOS)
        self.deleteUnusedLanguages(targetGPOS, self.SCRIPTLANGUAGES[script])
        # Get the set with names of glyphs in the source/target GPOS that have a unicode.
        if self.doSubset(script):
            # All remaining glyphs in the GPOS should be in the requiredGlyphNames name list.
            for glyphName in targetGPOS.getGlyphNames():
                if not isinstance(glyphName, str):
                    self.error() # Was an error, test to be sure, otherwise glyph are deleted.
                if not glyphName in targetGlyphNames:
                    # If not existing in the source/target font, delete it from the lookups.
                    targetGPOS.deleteGlyph(glyphName)
            # Finally clean up the targetGPOS, to release all hard links to removed state instances.
            targetGPOS.cleanUp()

            for chn in targetGPOS.getInputGlyphNames():
                if not targetFont[chn].unicode:
                    print(112211222, chn)
# Now GPOS only contains the glyphs that are really available in the target font.
        # And targetGlyphNames contains all the glyph names that should be in the target font (so far)

    def subsetGDEF(self, weight, style, script, targetFont, targetGlyphNames, modelFont):
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
        if self.doSubset(script):
            targetGDEF = targetFont.gdef
            if self.doSubset(script):
                deleteCount = 0
                for glyphName in sorted(targetGDEF.getGlyphNames()):
                    if not glyphName in targetGlyphNames:
                        # If not existing in the source/target font, delete it from the lookups.
                        targetGDEF.deleteGlyph(glyphName)
                        deleteCount += 1
                self.report('[GDEF] Deleted %s source/target glyphs.' % deleteCount)

    def subsetCMAP(self, weight, style, script, targetFont, targetGlyphNames, modelFont):
        #
        # C M A P
        #
        targetCmap = targetFont.cmap
        for table in targetCmap.tables:
            for unicodeValue, glyphName in table.cmap.items():
                if not glyphName in targetGlyphNames:
                    del table.cmap[unicodeValue]

    def subsetKERN(self, weight, style, script, targetFont, targetGlyphNames, modelFont):
        #
        # K E R N
        #
        # Cleanup the kern table for all glyph pairs that have one or two not in finalGlyphNames.
        # Because it is simple with no references, we do that directly on the FontTools table object.
        kernTables = targetFont.kern.kernTables
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
        targetFont.kern.kernTables = newKernTables
        self.report('[kern] Deleted %s kerning pairs.' % deleteCount)
        self.report('[kern] Remaining %s kerning pairs.' % kernCount)

    def subsetGlyphs(self, weight, style, script, targetFont, targetGlyphNames, modelFont):
        #
        # F I N A L L Y  D E L E T E  U N W A N T E D  G L Y P H S
        #
        # Now we have the final list of glyphs for the target font. Remove all the others.
        if self.doSubset(script):
            for glyphName in sorted(targetFont.keys()):
                if not glyphName in targetFont:
                    print('### Warning DOSUBSET: Expected glyph "%s" does not exist in the target font.' % glyphName)
                if not glyphName in targetGlyphNames:
                    del targetFont[glyphName]

    def deleteScripts(self, targetGTable, requiredScriptNames):
        # Delete the scripts in targetGTable that are not in requiredScriptNames
        # Note that later in the subsetting process, if features and lookups are cleaned,
        # we also need to check if the required scripts did become empty too.
        # In that case they are removed too.
        for script in targetGTable.scripts.keys():
            if not script in requiredScriptNames:
                if DEBUG:
                    self.report('\tDeleting source script(%s)' % script)
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

    def subsetFont(self, targetFont, modelFont, fallbackFont, weight, style, script, glyphset):
        # So, we are going to subset the targetFont here, which is a fresh clean copy of the source font.
        # This means that all glyphs and all GSUB/GPOS/GDEF language subtables are available, we just have to check the
        # minimum set that is needed according to the glyphset and then delete the rest in the target font.
        # The modelFont holds the set of scripts and glyphs that are supposed to go into the target.
        # There are some resources for the new set of glyphs that need to match:
        #    - All glyphs with a unicode identical to the one the model font, need to go into the targetFont
        #    - All glyphs that are (recursively) referred as component in this resulting glyph set should be added too.
        #    - Delete all scripts and features and lookups from the target font that have no reference to any of
        #        the final target glyph set
        #    - Delete all glyphs in the target font that are not in the target list.
        # The model font is only used to copy some preset OS/2 values from.
        #
        # C O M P A R E  G L Y P H S E T S
        #
        # Collect all the glyphs in the target font that need to be kept (we will be
        # deleting the glyphs from a full copy of the source font). This includes
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
        for unicodeValue in sorted(glyphset.keys()):
            glyph = targetFont.glyphByUnicode(unicodeValue)
            if glyph is None:
                # If the unicode is currently not in the target font, then copy it from the fallback font.
                glyph = self.copyGlyph(fallbackFont, targetFont, unicodeValue=unicodeValue)
            if glyph is not None:
                # There is a matching glyph, now add it to the target list, and also add the (recursively nested)
                # name(s) of any component glyph that it contains. It is important to do it right away, or else
                # the subsetting needs to be done in several passes. Any time a component glyph gets added
                # to the list, this also can have effect on the lookups to be kept.
                glyph = self.addTargetGlyphName(targetGlyphNames, targetGlyphUnicodes, glyph.name, fallbackFont, targetFont)
            else:
                print('### Warning: Font does not contain expected unicode glyph "%04X"' % unicodeValue)
        # Add the required glyphs that are not part of the standard glyphset
        for glyphName in self.REQUIREDGLYPHS:
            targetGlyphNames.add(glyphName)
            if not glyphName in targetFont:
                glyph = self.copyGlyph(fallbackFont, targetFont, name=glyphName)
                if glyph is None: # If not in the fallback font, then copy from .notdef
                    glyph = self.copyGlyph(fallbackFont, targetFont, name=glyphName, srcName=self.GLYPH_NOTDEF)
                if glyph is not None and glyph.unicode:
                    targetGlyphUnicodes.add(glyph.unicode)

        if self.doSubset(script):
            #
            # G S U B
            #
            self.subsetGSUB(weight, style, script, targetFont, targetGlyphNames, modelFont)
            #
            # G P O S
            #
            self.subsetGPOS(weight, style, script, targetFont, targetGlyphNames, modelFont)
            #
            # G D E F
            #
            self.subsetGDEF(weight, style, script, targetFont, targetGlyphNames, modelFont)
            #
            # C M A P
            #
            self.subsetCMAP(weight, style, script, targetFont, targetGlyphNames, modelFont)
            #
            # K E R N
            #
            self.subsetKERN(weight, style, script, targetFont, targetGlyphNames, modelFont)
            #
            # O T H E R  T A B L E S
            #
            # We don't have to delete the rest of unwanted tables from the target font,
            # because the SegoeFont.save() will create another new TTFont and only
            # copy/create the tables that that are needed in the output. This means
            # that all unwanted tables in the current targetFont will not be copied.
            # @@@ We could think of a mechanism to select which tables get copied or not
            # (such as the [kern] table) to make it general and optional.
            #
            # Cleanup again, as some of the script or languages mat have become empty now.
            targetFont.gsub.cleanUp()
            targetFont.gpos.cleanUp()

            for script in targetFont.gsub.scripts.values():
                for language in script.languages.values():
                    for feature in language.features:
                        for lookup in feature.lookups:
                            for keepGlyphName in lookup.getGlyphNames():
                                if 'afii57664' in lookup.getGlyphNames():
                                    print('432234', lookup.keepIt())
                                    lookup.deleteGlyph('afii57664')
                                print('ADDING GLYPH', keepGlyphName)
                                glyph = targetFont[keepGlyphName]
                                self.addTargetGlyphName(targetGlyphNames, targetGlyphUnicodes, glyph.name, fallbackFont, targetFont)

            # Now the input glyphs are cleaned, we have to add the remaining output glyphs to the target list.
            # Clean up the targetGSUB for all lookups that no longer have input glyphs,
            # to release all hard links to removed state instances. All lookups with just dead weakrefs
            # will drop out.
            # Cleanup again, as some of the script or languages mat have become empty now.
            #targetFont.gsub.cleanUp()
            #targetFont.gpos.cleanUp()
            #
            # Check and show what the difference is between the collected targetGlyphNames and
            # the original request for unicode glyphs.
            #
            # Now GSUB and GPOS only contains the glyphs that are really available in the target font.
            # And targetGlyphNames contains all the glyph names that should be in the target font (so far)
            #
            self.subsetGlyphs(weight, style, script, targetFont, targetGlyphNames, modelFont)

            targetFont.gsub.saveSpecimenPage(targetFont, targetFont.path+'.Target')
            """
            for index, lookup in enumerate(targetFont.gsub.lookups):
                print(index, lookup.getInputGlyphNames(), lookup.getGlyphNames())

            print('=====', len(targetFont.gsub.lookups))
            print('=====', len(targetFont.gsub.getGlyphNames()))
            print('=====', len(targetFont.gpos.lookups))
            print('=====', len(targetFont.gpos.getGlyphNames()))
            print('=====', len(targetGlyphNames))
            # See which glyphs still remain in the GSUB
            for index, lookup in enumerate(targetFont.gsub.lookups):
                if 'uni0670' in lookup.getGlyphNames():
                    for feature in lookup.features:
                        print('====', feature)
                    print('All', index, lookup, lookup.getGlyphNames())
                    print('Input', index, lookup, lookup.getInputGlyphNames())
            print('@#@@@', 'uni0670' in targetGlyphNames)
            """
        #
        # Save the font created target font.
        #
        targetFont.save()
        print('...... Done saving')

subsetter = SegoeSubsetter()
subsetter.subsetAll()
subsetter.compareFileSizes()
