# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    subset.py
#
import os, shutil, copy


DEBUG = False
DOSUBSET = True
REPORT2FILE = True
EXITFATAL = False

GENERATE_SOURCE_PROOF = False
GENERATE_TARGET_PROOF = True
# Make true, to generate the (complete) output, with patched EOT OS/2 values.
# Copy the generated EOT into to delivery that is generated with this parameter set to False.
RUN_EOT_OS2_PATCHES = False

from tnbits.objects.truetypefont import TrueTypeFont, TTFCompiler
from tnbits.proofing.webproof.exportproof import Proof

from glyphsets import GLYPHSETS

class SegoeFont(TrueTypeFont):
    # Inherit the TrueTypeFont, to redefine the creation of certain tables.

    def TTFCompilerClass(self):
        # Allow inheriting classes from TrueTypeFont define their own compiler class.
        # E.g. to define alternative handling of certain tables, such as the copy of
        # of OS/2 values in Segoe, instead of recalculating them.
        return SegoeCompiler

class SegoeCompiler(TTFCompiler):

    def setupTable_OS2(self):
        """
        Make the OS/2 table. Redefining from complete OS/2 rebuild in TTFCompiler,
        since Segoe needs the model values restored, instead of calculating new values.
        """
        self.otf["OS/2"] = self.ufo.os2

class SubsetProof(Proof):
    SHOW_SIZES = False
    SHOW_KERNING = True

class SubSetter(object):

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
        if self._report is None:
            print(s)
        else:
            self._report.write(s + '\n')

    def reportLine(self):
        self.report('-'*80)

    def buildProof(self, paths):
        SubsetProof.buildPaths(paths)

class SegoeSubsetter(SubSetter):

    # If True, charset files are generated, no subsetting is done.
    MAKEGLYPHSETFILES = False

    ROOT = '/FontDevelopment/_TTF/SegoeWorkSpace'
    SOURCES = ROOT + '/Sources'
    SRCPATH = SOURCES + '/SegoeUI-%s%s-All.ttf'
    FALLBACKPATH = SRCPATH % ('Regular', '') # Copy from here if a required glyph (such as .notdef') is not in the source font.
    MODELS = ROOT + '/Models'
    MODELPATH = MODELS + '/%s/SegoeUI-%s%s-%s.ttf'
    TARGETS = ROOT + '/Targets'
    if RUN_EOT_OS2_PATCHES:
        TARGETS = TARGETS+'-EOT-PATCH'
    TARGETPATH = TARGETS + '/SegoeUI-%s%s-%s.ttf'
    REPORTPATH = TARGETS + '/~Reports'

    # Thai needs another source file
    THAI_SRCPATH = SOURCES + '/SegoeUI-%s%s-Thai.ttf'

    TARGET_SCRIPTS = ('Arabic', 'Cyrillic', 'East European', 'Greek', 'Hebrew', 'Thai', 'Vietnamese', 'West European')
    #TARGET_SCRIPTS = ('Arabic', 'Cyrillic', 'Kazakh', 'East European', 'Greek', 'Hebrew', 'Thai', 'Vietnamese', 'West European')
    #TARGET_SCRIPTS = ('Cyrillic', 'West European')
    #TARGET_SCRIPTS = ('West European',)
    #TARGET_SCRIPTS = ('Vietnamese',)
    TARGET_SCRIPTS = ('Hebrew',)
    #TARGET_SCRIPTS = ('Vietnamese','Hebrew', 'Arabic')
    #TARGET_SCRIPTS = ('Thai',)
    #TARGET_SCRIPTS = ('Arabic',)
    #TARGET_SCRIPTS = ('Cyrillic',)

    TARGET_WEIGHTS = ('Regular', 'Bold', 'Light', 'SemiBold', 'SemiLight')
    #TARGET_WEIGHTS = ('Regular', 'Bold', 'SemiBold', 'SemiLight') # Problems with the light
    TARGET_WEIGHTS = ('Light',)
    #TARGET_WEIGHTS = ('Bold', )
    #TARGET_WEIGHTS = ('Regular', )

    TARGET_STYLES = ('', '-Italic')
    #TARGET_STYLES = ('-Italic',)
    TARGET_STYLES = ('',)

    # Languages per script

    SCRIPTLANGUAGES = {
        'Arabic': {
            'dflt': 'arab',
            'arab': ('ARA', 'MLY', 'MOR', 'SND', 'URD'),
            'cyrl': ('dflt',),
            'grek': ('dflt',),
            'hebr': ('dflt',), # In model Regular, SemiLight. Not in model Bold, Light, Semibold,
            'latn': ('dflt', 'TRK'),
        },
        'Cyrillic': {
            'dflt': 'cyrl',
            'cyrl': ('dflt', 'MKD', 'SRB'), # 'MKD', 'SRB' in model Bold-Italic
            'latn': ('dflt', 'TRK'),
        },
        'East European': {
            'dflt': 'latn',
            'latn': ('dflt', 'TRK'),
        },
        'Greek': {
            'dflt': 'grek',
            'grek': ('dflt',),
            'latn': ('dflt', 'TRK'),
        },
        'Hebrew': {
            'dflt': 'hebr',
            'hebr': ('dflt',), # Not in model Bold, Semibold
            'latn': ('dflt', 'TRK'),
        },
        'Thai': {
            'dflt': 'thai',
            'thai': ('dflt'),
        },
        'Vietnamese': {
            'dflt': 'latn',
            'latn': ('dflt', 'TRK'),
        },
        'West European': {
            'dflt': 'latn',
            'latn': ('dflt', 'TRK'),
        },
    }

    # G L Y P H names
    GLYPH_NULL = '.null'
    GLYPH_NOTDEF = '.notdef'
    GLYPH_FRACTION = 'fraction' # Make sure that the light GSUB does not collapse
    REQUIREDGLYPHS = (GLYPH_NULL, GLYPH_NOTDEF, GLYPH_FRACTION)

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
        self.closeReport()
        # Build the proof
        if GENERATE_TARGET_PROOF:
            for file in os.listdir(self.TARGETS):
                if file.endswith(".ttf"):
                    path = self.TARGETS + '/' + file
                    self.buildProof(path)

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
                print('-'*80)
                print('Subsetting from source', srcPath)
                self.reportLine()
                self.report('Subsetting from source %s' % srcPath)
                self.reportLine()
                self.report('\n......\nSubsetting from model path %s\n......\n' % modelPath)
                # Make a copy of the source path to the target path
                shutil.copy(srcPath, targetPath)
                print('...... Target', targetPath)
                targetFont = SegoeFont(targetPath)
                # Get the glyphset for this script
                glyphset = self.getGlyphset(script) # Key is unicode, value is unicode glyph name
                # Excecute the actual subsetting of the targetFont
                self.subsetFont(targetFont, modelFont, fallbackFont, weight, style, script, glyphset)

    def fatal(self, s):
        self.report(s)
        print(s)
        if EXITFATAL:
            exit()

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
                self.report('?????? Warning: Substituting missing unicode glyph "%04X" by fallback font glyph "%04X"' % (unicodeValue, unicodeValue))
        elif name is not None:
            if (srcName or name) in fallbackFont:
                self.report('?????? Warning: Substituting missing glyph "%s" from fallback font glyph "%s"' % (name, srcName or name))
                fallbackGlyph = fallbackFont[srcName or name]
            else:
                self.fatal('###### Error: required glyph "%s" does not exist in fallback font' % name)
        else:
            raise ValueError
        if fallbackGlyph is not None:
            targetFont[name] = glyph = copy.copy(fallbackGlyph)
            if not name in targetFont.glyphOrder:
                targetFont.glyphOrder = [name] + targetFont.glyphOrder
        return glyph

    def getGlyphset(self, script):
        # Get the glyphset name for this script
        return GLYPHSETS[script.replace(' ', '')]

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
                self.fatal('###### Font does not contain expected unicode glyph "%04X"' % unicodeValue)
        # Add the required glyphs that are not part of the standard glyphset
        for glyphName in self.REQUIREDGLYPHS:
            targetGlyphNames.add(glyphName)
            if not glyphName in targetFont:
                glyph = self.copyGlyph(fallbackFont, targetFont, name=glyphName)
                if glyph is None: # If not in the fallback font, then copy from .notdef
                    glyph = self.copyGlyph(fallbackFont, targetFont, name=glyphName, srcName=self.GLYPH_NOTDEF)
                if glyph is not None and glyph.unicode:
                    targetGlyphUnicodes.add(glyph.unicode)
        # At this point the target list is not supposed to change anymore, as the GSUB and GPOS and GDEF will
        # shrink to fit in side the projected target glyph set.
        if self.doSubset(script) and DEBUG:
            print('1 Target', len(targetGlyphNames), 'glyphs. Model glyphset with unicode', len(glyphset.keys()), 'glyphs.')
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
        if self.doSubset(script):
            targetGSUB = targetFont.gsub
            print(1, 'Lookups', len(targetGSUB.lookups))
            targetGSUB.saveSpecimenPage(targetFont, targetFont.path+'.Source')
            # Just to show how incomplete these are.
            modelGSUB = modelFont.gsub
            modelGSUB.saveSpecimenPage(modelFont, targetFont.path+'.Model')
            if DEBUG:
                self.dumpGSUB(self.REPORTPATH + '/DEBUG-GSUB.xml', targetGSUB) # Use to compare unchanged XML output
                self.report('[GSUB] Source/target scripts%s' % targetGSUB.scripts.keys())
                #self.report('[GSUB] Model scripts%s' % modelGSUB.scripts.keys())

            # Do the actual deletion of the unwanted scripts.
            self.deleteScripts(targetGSUB, self.SCRIPTLANGUAGES[script].keys())
            print(2, 'Lookups', len(targetGSUB.lookups))

            self.report('[GSUB] Target scripts after subset %s' % (targetGSUB.scripts.keys(),))
            # Now we have a GSUB that only contains the same script names as the requested glyph list has,
            # where we are sure that all glyphs in the GSUB/GPOS exist in the source/target font.
            # Next thing is to delete all languages (and features) that don't exist in the model font.
            self.deleteUnusedLanguages(targetGSUB, self.SCRIPTLANGUAGES[script])
            print(3, 'Lookups', len(targetGSUB.lookups))
            # Next is to clean all GSUB lookups, where the input glyph is not in the target list.
            # After that is cleaned, the remaining glyphs in the GSUB, are supposed to extend the
            # target glyph list, because these are the substituted glyphs that may not have a unicode.
            # Also add these glyphs to the target list.
            # Note that we have to do the GSUB first (before GPOS and GDEF), in order to complete the
            # list of glyphs that we need in the target.
            # Make sure just to test on the input glyph names of the GSUB and later add all glyphs
            # of GSUB again to the targetGlyphNames, as there may be output glyphs that we don't
            # know yet.
            for glyphName in targetGSUB.getInputGlyphNames():
                # Delete input glyphs only if is in the targetGlyphNames and it has a unicode
                if not glyphName in targetGlyphNames and\
                    targetFont[glyphName] is not None and targetFont[glyphName].unicode:
                    # The GSUB input is using a glyph that does not exist in the target list. This is caused
                    # by bad GSUB (when it does not exist in the source font at all) or it can be
                    # used by glyphs that will be removed by the subsetting, remove the glyphName
                    # from the GSUB, anywhere in the lookups where it is used. Since that can be very deep,
                    # we let the lookups do the work themselves. Since many of the coverate.glyphs lists
                    # will become empty, we'll clean up the emptied lookups later, by cutting the live wires
                    # to them.
                    targetGSUB.deleteInputGlyph(glyphName)
                    print(4, 'Lookups', len(targetGSUB.lookups))
            # Now the input glyphs are cleaned, we have to add the remaining output glyphs to the target list.
            # Clean up the targetGSUB for all lookups that no longer have input glyphs,
            # to release all hard links to removed state instances.
            targetGSUB.cleanUp() # Delete lookups with empty inputs
            print(5, 'Lookups', len(targetGSUB.lookups))
            print('5-1', 'Lookup input glyphs', len( targetGSUB.getInputGlyphNames()), targetGSUB.getInputGlyphNames())
            print('5-2', 'Lookup all glyphs', len(targetGSUB.getGlyphNames()), targetGSUB.getGlyphNames())
            # Now run again, to add the remaining output glyphs to the target list, if not already there.
            # Make sure that, if adding a missing output glyph, also add any component inside that glyph.
            print(1, 'uni0620.fina' in targetGlyphNames)
            for glyphName in targetGSUB.getGlyphNames():
                if not glyphName in targetGlyphNames:
                    glyph = self.addTargetGlyphName(targetGlyphNames, targetGlyphUnicodes, glyphName, fallbackFont, targetFont)
            print(2, 'uni0620.fina' in targetGlyphNames)
            print(6, 'Lookups', len(targetGSUB.lookups))
            print('2-2', targetGlyphUnicodes)
            print('2-3', glyphset)
            targetGSUB.saveSpecimenPage(targetFont, targetFont.path+'.Target')
            print(7, 'Lookups', len(targetGSUB.lookups))

        if self.doSubset(script): # Reporting on life/dead of GSUB lookups, features and languages
            # Reporting status on glyphset
            print(333, 'uniFEF7 in', 'uniFEF7' in targetGlyphNames, 'uniFEF7' in  targetGSUB.getGlyphNames())
            print('2 Target', len(targetGlyphNames), 'glyphs. Model glyphset with unicode', len(glyphset.keys()), 'glyphs.')
            # Test if really all glyphs where removed from the GSUB that are not in the target.
            for glyphName in targetGSUB.getGlyphNames():
                if not glyphName in targetGlyphNames:
                    self.fatal('###### Fatal error: Glyph "%s" still in GSUB, is not in the font.' % targetGSUB.findLookupsUsingGlyph(glyphName))
        #
        # Now GSUB only contains the glyphs that are really available in the target font.
        # And targetGlyphNames contains all the glyph names that should be in the target font (so far)
        #
        # G P O S
        #
        # Then we do almost the same with GPOS as we did with GSUB. Delete the scripts that we don't need.
        print(3, 'uni0620.fina' in targetGlyphNames)
        if self.doSubset(script):
            targetGPOS = targetFont.gpos
            modelGPOS = modelFont.gpos
            if DEBUG:
                self.dumpGPOS(self.REPORTPATH + '/DEBUG-GPOS.xml', targetGPOS) # Use to compare unchanged XML output
                self.report('[GPOS] Model scripts%s' % modelGPOS.scripts.keys())
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
            # Now GPOS only contains the glyphs that are really available in the target font.
            # And targetGlyphNames contains all the glyph names that should be in the target font (so far)
            print('3 Target', len(targetGlyphNames), 'glyphs. Model glyphset with unicode', len(glyphset.keys()), 'glyphs.')
        print(4, 'uni0620.fina' in targetGlyphNames)
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
        print(5, 'uni0620.fina' in targetGlyphNames)
        #
        # C M A P
        #
        targetCmap = targetFont.cmap
        for table in targetCmap.tables:
            for unicodeValue, glyphName in table.cmap.items():
                if not glyphName in targetGlyphNames:
                    del table.cmap[unicodeValue]
        print(6, 'uni0620.fina' in targetGlyphNames)
        #
        # K E R N
        #
        # Cleanup the kern table for all glyph pairs that have one or two not in finalGlyphNames.
        # Because it is simple with no references, we do that directly on the FontTools table object.
        if self.doSubset(script):
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
        print(7, 'uni0620.fina' in targetGlyphNames)
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
        # F I N A L L Y  D E L E T E  U N W A N T E D  G L Y P H S
        #
        # Now we have the final list of glyphs for the target font. Remove all the others.
        print(8, 'uni0620.fina' in targetGlyphNames)
        if self.doSubset(script):
            for glyphName in sorted(targetFont.keys()):
                if not glyphName in targetFont:
                    print('### Warning DOSUBSET: Expected glyph "%s" does not exist in the target font.' % glyphName)
                if not glyphName in targetGlyphNames:
                    del targetFont[glyphName]
        print(9, 'uni0620.fina' in targetGlyphNames)
        print(10, 'uni0620.fina' in targetFont.keys())
        #
        # C L E A N  G L Y P H  O R D E R
        #
        # Then adjust the glyph order list to the latest content of the font.
        if self.doSubset(script):
            glyphOrder = []
            for glyphName in targetFont.glyphOrder:
                if glyphName in targetFont:
                    glyphOrder.append(glyphName)
            targetFont.glyphOrder = glyphOrder
        print(11, 'uni0620.fina' in glyphOrder)
        print(11, 'uni0620.fina' in targetGlyphNames)
        print(12, 'uni0620.fina' in targetFont.keys())
        print(targetFont.keys())
        #
        # O S / 2
        #
        # Copy the OS/2 values for the targetFont from the modelFont that are influenced by the glyph range.
        # Or the ones that need to be identical for legacy reaons.
        if self.doSubset(script):
            targetOS2 = targetFont.os2
            modelOS2 = modelFont.os2
            if self.doSubset(script):
                for fieldName in ('xAvgCharWidth', 'sFamilyClass', 'usMaxContex',
                        'sTypoAscender', 'sTypoDescender', 'sTypoLineGap', 'usWinAscent', 'usWinDescent',
                        'ulCodePageRange1', 'ulCodePageRange2',
                        'ulUnicodeRange1', 'ulUnicodeRange2',
                        'ulUnicodeRange3', 'ulUnicodeRange4'
                    ):
                    setattr(targetOS2, fieldName, getattr(modelOS2, fieldName))

        # Michelle Perham: With Windows, we ship the following OS/2 values:
        # Segoe UI Light  300
        # Segoe UI Semilight  350
        # Segoe UI Regular  400
        # Segoe UI Semibold  600
        # Segoe UI Bold 700
        #
        # We used these values for the first set of web fonts we created. Because increments of 50 are illegal in CSS,
        # we encountered issues in Firefox with the Semilight. So we switched to the following:
        # Segoe UI Light 200
        # Segoe UI Semilight 300
        # Segoe UI Regular 400
        # Segoe UI Semibold 600
        # Segoe UI Bold 700
        #
        # We thought this was fine, but we recently got a report of problems on Windows XP with the newer Semilight EOTs
        # (the old ones work fine and the developer claims the weight is the problem). So we’d like to go back to the original
        # values just for the EOTs, but keep the new values for the other file formats. Does that sound reasonable?

        # If this run is patching EOT-OS/2 weight values, then alter the value according to the current weight.
        if self.doSubset(script) and RUN_EOT_OS2_PATCHES:
            if weight == 'SemiLight':
                targetOS2.usWeightClass = 350
            elif weight == 'Light':
                targetOS2.usWeightClass = 300
        #
        # H M T X
        #
        # Delete all HTMX entries that are not in the required glyph set.
        # Then make sure that all glyphs in the glyphset are set in the HTMX
        targetHmtx = targetFont.hmtx
        # Values for HHEA table, need to be consistent with values in HTMX
        minLeftSideBearing = 10000000 # Collect for HHEA table
        minRightSideBearing = 10000000 # Collect for HHEA table
        advanceWidthMax = 0 # Collect for HHEA table
        xMaxExtent = 0 # Collect for HHEA table
        maxComponentElements = 0 # Collect for maxp table
        #maxSizeOfInstructions = 0 # Collect for maxp table
        # If subsetting, delete the glyphs that we don't want.
        if self.doSubset(script):
            for glyphName in targetHmtx.metrics.keys():
                if not glyphName in targetGlyphNames:
                    del targetHmtx.metrics[glyphName]
        # Calculate the metrics for the remaining glyphs
        # Add the glyphs that are in the target set and yet in the table.
        # This happens e.g. for the required glyphs that came from the fallback font.
        # We write all the existing values in the table, just to be sure anyway.
        for glyphName in targetGlyphNames:
            glyph = targetFont[glyphName]
            targetHmtx.metrics[glyph.name] = (glyph.width, glyph.leftMargin)
            # Collect HHEA metrics, only for glyphs with contours.
            if glyph.points or glyph.components:
                minLeftSideBearing = min(glyph.leftMargin, minLeftSideBearing)
                minRightSideBearing = min(glyph.rightMargin, minRightSideBearing) # Min(aw - lsb - (xMax - xMin))
                advanceWidthMax = max(glyph.width, advanceWidthMax)
                xMaxExtent = max(glyph.rightMargin, xMaxExtent) # Max(lsb + (xMax - xMin)).
            maxComponentElements = max(len(glyph.components), maxComponentElements)
        #
        # H H E A
        #
        # Copy values from the model font HHEA table to the target, to make
        # sure we preserve the vertical metrics from the model.
        if self.doSubset(script):
            targetHhea = targetFont.hhea
            modelHhea = modelFont.hhea
            # Set the calculated advanceWidthMax, minLeftSideBearing, minRightSideBearing, numberOfHMetrics, xMaxExtent
            # from the current set of glyphs as collected in the HTMX loop
            targetHhea.minLeftSideBearing = minLeftSideBearing
            targetHhea.minRightSideBearing = minRightSideBearing
            targetHhea.advanceWidthMax = advanceWidthMax
            targetHhea.numberOfHMetrics = len(targetHmtx.metrics)
            targetHhea.xMaxExtent = xMaxExtent
            # Copy the other HHEA values from the model font to the target font.
            for attrName in ('lineGap', 'ascent', 'caretOffset', 'caretSlopeRise', 'caretSlopeRun', 'descent', 'metricDataFormat'):
                setattr(targetHhea, attrName, getattr(modelHhea, attrName))
        #
        # M A X P
        #
        # Set the calculated the max number of glyph instructions maxSizeOfInstructions
        # the maxComponent elements, derived from the scanning in the HMTX table
        if self.doSubset(script):
            modelMaxp = modelFont.maxp
            targetMaxp = targetFont.maxp
            # @@@ There probably are more values to recalculate here.
            targetMaxp.maxComponentElements = maxComponentElements # Gathered in the HTMX glyph scan.
            targetMaxp.maxSizeOfInstructions = modelMaxp.maxSizeOfInstructions
        #
        # C H E C K I N G  O N  T H E  R E S U L T
        #
        # The number of target lookups should be the same as in the target font
        if self.doSubset(script) and DEBUG:
            self.report('[GSUB]')
            self.report('\tgsub.lookups: Model %d Target %d' % (len(modelGSUB.lookups), len(targetGSUB.lookups)))
            self.report('\tgsub.scripts: Model %d Target %d' % (len(modelGSUB.scripts), len(targetGSUB.scripts)))
            self.report('\tgsub.features: Model %d Target %d' % (len(modelGSUB.features), len(targetGSUB.features)))
            # Check if GSUB is "clean", which means that all of the glyphs in GSUB now should be in the font
            for glyphName in targetGSUB.getGlyphNames():
                if not glyphName in targetFont:
                    self.fatal('###### [GSUB] Glyph name in GSUB "%s" does not exist in the target font' % glyphName)

            self.dumpGSUB(self.REPORTPATH + '/DEBUG-GSUB.SUBSET.xml', targetGSUB) # Use to compare unchanged XML output

            self.report('[GPOS]')
            self.report('\tgpos.lookups: Model %d Target %d' % (len(modelGPOS.lookups), len(targetGPOS.lookups)))
            self.report('\tgpos.scripts: Model %d Target %d' % (len(modelGPOS.scripts), len(targetGPOS.scripts)))
            self.report('\tgpos.features: Model %d Target %d' % (len(modelGPOS.features), len(targetGPOS.features)))
            # Check if GPOS is "clean", which means that all of the glyphs in GPOS now should be in the font
            for glyphName in targetGPOS.getGlyphNames():
                if not glyphName in targetFont:
                    self.fatal('###### [GPOS] Glyph name in GPOS "%s" does not exist in the target font' % glyphName)
            self.dumpGPOS(self.REPORTPATH + '/DEBUG-GPOS.SUBSET.xml', targetGPOS) # Use to compare unchanged XML output

            self.report('[GDEF]')
            self.report('\tgpos.lookups: Model %d Target %d' % (len(modelGPOS.lookups), len(targetGPOS.lookups)))
            # Check if GDEF is "clean", which means that all of the glyphs in GDEF now should be in the font
            for glyphName in targetGDEF.getGlyphNames():
                if not glyphName in targetFont:
                    self.fatal('###### [GDEF] Glyph name in GDEF "%s" does not exist in the target font' % glyphName)
            self.dumpGDEF(self.REPORTPATH + '/DEBUG-GDEF.SUBSET.xml', targetGDEF) # Use to compare unchanged XML output

            self.report('[glyf]')
            self.report('\tModel font glyphs %d' % len(modelFont.keys()))
            self.report('\tModel font glyphs with unicode %d' % len(modelFont.keysWithUnicode()))
            self.report('\tTarget font glyphs %d' % len(targetFont.keys()))
            self.report('\tTarget font glyphs with unicode %d' % len(targetFont.keysWithUnicode()))
        #
        # D E B U G
        #
        # Dump the table XML in separate files, so they can be compared with the source and model files.
        #if DEBUG:
        #    self.dumpGSUB(self.REPORTPATH + '/testDecompileGSUB.%s.%s%s.xml' % (script, weight, style), targetGSUB)
        #    self.dumpGPOS(self.REPORTPATH + '/testDecompileGPOS.%s.%s%s.xml' % (script, weight, style), targetGPOS)
        #    self.dumpGDEF(self.REPORTPATH + '/testDecompileGDEF.%s.%s%s.xml' % (script, weight, style), targetGDEF)
        #
        # G L Y P H S E T
        #
        # Check if the required unicodes are still in the target font.
        if self.doSubset(script):
            for unicodeValue in glyphset.keys():
                if targetFont.glyphByUnicode(unicodeValue) is None:
                    self.fatal('###### Required unicode "%04X" does not exist in final target font.' % unicodeValue)
            # Double check if glyphorder is (still) consistent with the glyph set
            for glyphName in targetFont.glyphOrder:
                if not glyphName in targetFont.glyphs:
                    self.fatal("""###### Required glyphOrder "%s" does not exist in final font.glyphs""" % glyphName)
        """
        # @@@ For now, compare the unicode entry points of the model, so we can check them
        # @@@ against the unicodes of the final target font.
        # @@@ Compare the final unicode set of the target with the model.
        targetUnicodes = sorted(targetFont.unicodes)
        modelUnicodes = sorted(modelFont.unicodes)
        if targetUnicodes != modelUnicodes:
            for unicodeValue in targetUnicodes:
                if not unicodeValue in modelUnicodes:
                    glyph = targetFont.glyphByUnicode(unicodeValue)
                    if glyph is None:
                        print('###### Cannot find glyph "%s" in target font.' % unicodeValue)
                    elif glyph.name in modelFont:
                        print('###### Model "%s" has no unicode.' % glyph.name)
                    else:
                        print('###### Unicode "%s" is in target and not in model.' % unicodeValue)

            for unicodeValue in modelUnicodes:
                if not unicodeValue in targetUnicodes:
                    glyph = modelFont.glyphByUnicode(unicodeValue)
                    if glyph is None:
                        print('###### Cannot find glyph "%s" in model font.' % unicodeValue)
                    elif glyph.name in targetFont:
                        print('###### Target "%s" has no unicode.' % glyph.name)
                    else:
                        print('###### Unicode "%s" is in model and not in target.' % unicodeValue)
        """
        # O U T P U T
        #
        # Save the modified subset targetFont as TTF format.
        #if DEBUG:
        print(12, 'uni0620.fina' in targetFont.keys())
        print(13, len(targetGlyphNames))
        print(len(targetFont), len(targetFont.glyphs.keys()))
        print(targetFont.keys())
        print(targetFont.glyphs.keys())
        targetFont.save()
        #else:
        #    try:
        #       targetFont.save()
        #    except (KeyError, AssertionError):
        #        errorMessage = '###### Error compiling the font %s %s %s' % (script, weight, style)
        #        self.report(errorMessage)
        #        print(errorMessage)

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

    def deleteScripts(self, targetGTable, requiredScriptNames):
        # Delete the scripts in targetGTable that are not in requiredScriptNames
        for script in targetGTable.scripts.keys():
            if not script in requiredScriptNames:
                if DEBUG:
                    self.report('\tDeleting source script(%s)' % script)
                targetGTable.deleteScript(script)

    def deleteUnusedFeatures(self, targetGTable):
        # OLD: Get all the different feature names in the model font and delete all features
        # OLD: in the target font that are not in the model font. Report the deletion.
        # NEW: Since we cannot trust the model font, we have to check for the required
        # glyphs if they are used in the features. And add the result of that feature
        # to the requires set of glyphs.
        # Question is what happens with the features and lookups that were referenced by
        # the deleted languages. This needs to be checked by the keepIt() of the feature
        # and lookup instances.


        # OLD: assuming that the model font is right, which is not.
        # OLD: so we really have to check for the glyphs if they are used by the features.
        """
        deletedFeatures = set()
        modelFeatureNames = set()
        for feature in modelGTable.features:
            modelFeatureNames.add(feature.tag)
        cleanedFeatures = []
        for feature in targetGTable.features:
            if feature.tag in modelFeatureNames and feature.hasAliveParent():
                cleanedFeatures.append(feature)
            else:
                deletedFeatures.add(feature.tag)
                #self.report('\tDeleting feature "%s" KeepIt=%s hasAliveParent=%s glyphs=%s' % (feature.tag, feature.keepIt(), feature.hasAliveParent(), sorted(feature.getGlyphNames())))
        targetGTable.features = cleanedFeatures
        self.report('\tDeleting feature(s) "%s" which are not in the model font.' % ', '.join(sorted(deletedFeatures)))
        """

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
            if language.script is not None and language.tag in modelLanguageNames:
                cleanedLanguages.append(language)
            else:
                deletedLanguages.add(language.tag)
                #self.report('\tDeleting language "%s" KeepIt=%s script=%s glyphs=%s' % (language.tag, language.keepIt(), language.script, sorted(language.getGlyphNames())))
        targetGTable.languages = cleanedLanguages
        self.report('\tDeleting language(s) "%s" that are not part of the language script.' % ', '.join(sorted(deletedLanguages)))

    def findMatchingGlyphs(self, glyphName, modelFont, sourceFont):
        # If the modelFont does not have glyphName, then answer None
        # If there is a matching unicode, then this if preferred above any name or outline matching.
        # Find the matching glyphName for the modelFont in the sourceFont.
        # Otherwise answer None if no match can be found
        # To be answered if we find a matching glyph
        matchingGlyphNames = set()
        if not glyphName in modelFont:
            return matchingGlyphNames
        # Get the glyph from the model
        modelGlyph = modelFont[glyphName]
        # Compare by unicode
        if modelGlyph.unicode is not None:
            matchingGlyph = sourceFont.glyphByUnicode(modelGlyph.unicode)
            if matchingGlyph is not None:
                # We found a matching unicode. That overwrites all other matching
                # such as name or outline.
                matchingGlyphNames.add(matchingGlyph.name)
                return matchingGlyphNames
        # Compare by glyph name
        if glyphName in sourceFont:
            # It is a direct find by glyph name, matching between both fonts
            matchingGlyphNames.add(glyphName)
            return matchingGlyphNames

        # No direct unicode or name matching.
        # Find the matching glyphName as in modelFont in sourceFont by point/component match
        for sourceName in sourceFont.keys():
            sourceGlyph = sourceFont[sourceName]
            # Compare looks for width, component count, point count and matching coordincates.
            # So it much really be identical. Fails if one or more of the values if different.
            # If not equal, the "reason" contains the error/warning string why the glyphs
            # of the two fonts are not considered to be equal.
            isEqual, _ = modelGlyph.compare(sourceGlyph) # isEqual, reason
            if isEqual:
                matchingGlyphNames.add(sourceName)
                # We found it.
                # But we cannot return here, when found one, as there can be duplicate outlines
                # in the font that all have their own component reference.
        if not matchingGlyphNames:
            self.report('###### Model glyph "%s" does not have a matching equivalent in the target font.' % glyphName)
        else:
            self.report('?????? Warning: Found matching glyph with different name(s): Model[%s] --> Target[%s]' % (glyphName, ', '.join(matchingGlyphNames)))
        return matchingGlyphNames

    def dumpGSUB(self, path, gsub):
        from tnbits.compilers.subsetting.gsubcompiler import GSUBCompiler
        gc = GSUBCompiler()

        #f = open('/GSUBmodel.%s.%s%s.json' % (script, weight, style), 'wb')
        #f.write(modelGSUB.asJson())
        #f.close()

        #f = open('/GSUBtarget.%s.%s%s.json' % (script, weight, style), 'wb')
        #f.write(targetGSUB.asJson())
        #f.close()

        #f = open('/testDecompileGSUB.fea', 'wb')
        #f.write(gc.compile2FeatureTalk(targetGSUB))
        #f.close()

        f = open(path, 'wb')
        gsubXML = gc.compile2XML(gsub)
        f.write(gsubXML)
        f.close()

    def dumpGPOS(self, path, gpos):
        from tnbits.compilers.subsetting.gposcompiler import GPOSCompiler
        gc = GPOSCompiler()

        #f = open('/GPOSmodel.%s.%s%s.json' % (script, weight, style), 'wb')
        #f.write(modelGPOS.asJson())
        #f.close()

        #f = open('/GPOStarget.%s.%s%s.json' % (script, weight, style), 'wb')
        #f.write(targetGPOS.asJson())
        #f.close()

        #f = open('/testDecompileGPOS.fea', 'wb')
        #f.write(gc.compile2FeatureTalk(targetGPOS))
        #f.close()

        f = open(path, 'wb')
        gposXML = gc.compile2XML(gpos)
        f.write(gposXML)
        f.close()

    def dumpGDEF(self, path, gdef):
        from tnbits.compilers.subsetting.gdefcompiler import GDEFCompiler
        gc = GDEFCompiler()

        f = open(path, 'wb')
        gdefXML = gc.compile2XML(gdef)
        f.write(gdefXML)
        f.close()

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

subsetter = SegoeSubsetter()
subsetter.subsetAll()
subsetter.compareFileSizes()
