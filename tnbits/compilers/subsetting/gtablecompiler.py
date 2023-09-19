# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     gtablecompiler.py
#
from io import StringIO
from copy import copy
from fontTools.ttLib import newTable
#Original import: from fontTools.ttLib.xmlImport import importXML
from tnbits.toolbox.parsers.xmlImport import importXML
from tnbits.compilers.subsetting.states import Script, Language, Feature, Lookup
from tnbits.compilers.subsetting.groupset import GroupSet
from tnbits.compilers.subsetting.featureconstants import FC

class GTableBaseCompiler(object):

    def __init__(self):
        self._output = None
        self.indent = 0

    # X M L  W R I T E R

    def newOutput(self):
        if self._output is not None:
            self._output.close()
        self._output = StringIO.StringIO()
        self.indent = 0

    def write(self, s):
        self._output.write(s)

    def getOutput(self):
        if self._output is None:
            return None
        src = self._output.getvalue()
        self._output.close()
        self._output = None
        return src

    def writeXmlHeader(self):
        self.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')

    def tagOpen(self, name, index=None, Format=None, glyph=None, value=None):
        self.write('\t'*self.indent + '<' + name)
        if index is not None:
            self.write(' index="%s"' % index)
        if Format is not None:
            self.write(' Format="%s"' % Format)
        if glyph is not None:
            self.write(' glyph="%s"' % glyph)
        if value is not None:
            self.write(' value="%s"' % value)
        self.write('>\n')
        self.indent += 1

    def tagClose(self, name):
        self.indent -= 1
        self.write('\t'*self.indent + '</' + name + '>\n')

    def tagOpenClose(self, name, index=None, value=None, in_=None, out_=None, glyph=None, components=None,
            xyValue=None, class_=None):
        self.write('\t'*self.indent + '<' + name)
        if index is not None:
            self.write(' index="%s"' % index)
        if value is not None:
            self.write(' value="%s"' % value)
        if in_ is not None:
            self.write(' in="%s"' % in_)
        if out_ is not None:
            self.write(' out="%s"' % out_)
        if components is not None:
            self.write(' components="%s"' % components)
        if glyph is not None:
            self.write(' glyph="%s"' % glyph)
        if xyValue is not None:
            if xyValue.XPlacement is not None:
                self.write(' XPlacement="%d"' % xyValue.XPlacement)
            if xyValue.XAdvance is not None:
                self.write(' XAdvance="%d"' % xyValue.XAdvance)
            if xyValue.YPlacement is not None:
                self.write(' YPlacement="%d"' % xyValue.YPlacement)
            if xyValue.YAdvance is not None:
                self.write(' YAdvance="%d"' % xyValue.YAdvance)
        if class_ is not None:
            self.write(' class="%s"' % class_)
        self.write('/>\n')

    def compile2Table(self, g, ttFont):
        # Compile the "g" State to the FontTools table instance.
        xml = self.compile2XML(g)
        #return table_G_P_O_S_(self.TABLE_TAG).fromXML((self.TABLE_TAG, [], xml), ttFont)
        #pathToXML = tempfile.mkstemp()[1]
        pathToXML = '/Users/petr/Desktop/PATH_%s_2XML.xml' % g.__class__.__name__
        # Write the XML to a tmp file.
        f = open(pathToXML, "w")
        f.write(xml)
        f.close()

        ttFont[self.TABLE_TAG] = newTable(self.TABLE_TAG)
        importXML(ttFont.ttfont, pathToXML) # Pass real FontTools font there
        # Comment next line to keep the XML output visible as file for debugging.
        #os.remove(pathToXML)
        return ttFont[self.TABLE_TAG]

    def tagRoot(self):
        self.tagOpen(self.TABLE_TAG)

    def _tagRoot(self):
        self.tagClose(self.TABLE_TAG)

    def tagVersion(self, version='1.0'):
        self.tagOpenClose('Version', value=version)

    def tagScriptList(self):
        self.tagOpen('ScriptList')

    def _tagScriptList(self):
        self.tagClose('ScriptList')

    def tagScriptRecord(self, index):
        self.tagOpen('ScriptRecord', index=index)

    def _tagScriptRecord(self):
        self.tagClose('ScriptRecord')

    def tagScriptTag(self, tag):
        self.tagOpenClose('ScriptTag', value=tag)

    def tagScript(self):
        self.tagOpen('Script')

    def _tagScript(self):
        self.tagClose('Script')

    def tagDefaultLangSys(self):
        self.tagOpen('DefaultLangSys')

    def _tagDefaultLangSys(self):
        self.tagClose('DefaultLangSys')

    def tagReqFeatureIndex(self, value):
        self.tagOpenClose('ReqFeatureIndex', value=value)

    def tagComment(self, s):
        self.write('\t'*self.indent + '<!-- ' + s + ' -->\n')

    def tagFeatureIndex(self, index, value):
        self.tagOpenClose('FeatureIndex', index=index, value=value)

    def tagLangSysRecord(self, index):
        self.tagOpen('LangSysRecord', index=index)

    def _tagLangSysRecord(self):
        self.tagClose('LangSysRecord')

    def tagLangSysTag(self, tag):
        self.tagOpenClose('LangSysTag', value=tag)

    def tagLangSys(self):
        self.tagOpen('LangSys')

    def _tagLangSys(self):
        self.tagClose('LangSys')

    def tagFeatureList(self):
        self.tagOpen('FeatureList')

    def _tagFeatureList(self):
        self.tagClose('FeatureList')

    def tagFeatureRecord(self, index):
        self.tagOpen('FeatureRecord', index=index)

    def _tagFeatureRecord(self):
        self.tagClose('FeatureRecord')

    def tagFeatureTag(self, tag):
        self.tagOpenClose('FeatureTag', value=tag)

    def tagFeature(self):
        self.tagOpen('Feature')

    def _tagFeature(self):
        self.tagClose('Feature')

    def tagLookupListIndex(self, index, value):
        self.tagOpenClose('LookupListIndex', index=index, value=value)

    def tagLookupList(self):
        self.tagOpen('LookupList')

    def _tagLookupList(self):
        self.tagClose('LookupList')

    def tagLookup(self, index):
        self.tagOpen('Lookup', index=index)

    def _tagLookup(self):
        self.tagClose('Lookup')

    def tagLookupType(self, value):
        self.tagOpenClose('LookupType', value=value)

    def tagLookupFlag(self, value):
        self.tagOpenClose('LookupFlag', value=value)

    def tagExtensionSubst(self, index, format):
        self.tagOpen('ExtensionSubst', index=index, Format=format)

    def _tagExtensionSubst(self):
        self.tagClose('ExtensionSubst')

    def tagExtensionPos(self, index, format):
        # Index can be None, if called by an extension lookup
        self.tagOpen('ExtensionPos', index=index, Format=format)

    def _tagExtensionPos(self):
        self.tagClose('ExtensionPos')

    def tagExtensionLookupType(self, value):
        self.tagOpenClose('ExtensionLookupType', value=value)

    def tagSingleSubst(self, index, format):
        # Index can be None, of called by an extension lookup.
        self.tagOpen('SingleSubst', index=index, Format=format)

    def _tagSingleSubst(self):
        self.tagClose('SingleSubst')

    def tagSubstitution(self, src, dst):
        self.tagOpenClose('Substitution', in_=src, out_=dst)

    def tagChainContextSubst(self, format):
        self.tagOpen('ChainContextSubst', Format=format)

    def _tagChainContextSubst(self):
        self.tagClose('ChainContextSubst')

    def tagInputCoverage(self, index, format):
        self.tagOpen('InputCoverage', index=index, Format=format)

    def _tagInputCoverage(self):
        self.tagClose('InputCoverage')

    def tagGlyph(self, glyphName):
        self.tagOpenClose('Glyph', value=glyphName)

    def tagBacktrackCoverage(self, index, format):
        self.tagOpen('BacktrackCoverage', index=index, Format=format)

    def _tagBacktrackCoverage(self):
        self.tagClose('BacktrackCoverage')

    def tagLookAheadCoverage(self, index, format):
        self.tagOpen('LookAheadCoverage', index=index, Format=format)

    def _tagLookAheadCoverage(self):
        self.tagClose('LookAheadCoverage')

    def tagLigatureSubst(self, index, format):
        # index can be None if called by an extension lookup.
        self.tagOpen('LigatureSubst', index=index, Format=format)

    def _tagLigatureSubst(self):
        self.tagClose('LigatureSubst')

    def tagLigatureSet(self, glyph):
        self.tagOpen('LigatureSet', glyph=glyph)

    def _tagLigatureSet(self):
        self.tagClose('LigatureSet')

    def tagLigature(self, components, glyph):
        self.tagOpenClose('Ligature', components=components, glyph=glyph)

    def tagMultipleSubst(self, index, format):
        # index can be None if called by an extension lookup.
        self.tagOpen('MultipleSubst', index=index, Format=format)

    def _tagMultipleSubst(self):
        self.tagClose('MultipleSubst')

    def tagCoverage(self, format):
        self.tagOpen('Coverage', Format=format)

    def _tagCoverage(self):
        self.tagClose('Coverage')

    def tagSequence(self, index):
        self.tagOpen('Sequence', index=index)

    def _tagSequence(self):
        self.tagClose('Sequence')

    def tagSubstitute(self, index, value):
        self.tagOpenClose('Substitute', index=index, value=value)

    def tagAlternateSubst(self, index, format):
        self.tagOpen('AlternateSubst', index=index, Format=format)

    def _tagAlternateSubst(self):
        self.tagClose('AlternateSubst')

    def tagAlternateSet(self, glyph):
        self.tagOpen('AlternateSet', glyph=glyph)

    def _tagAlternateSet(self):
        self.tagClose('AlternateSet')

    def tagAlternate(self, glyph):
        self.tagOpenClose('Alternate', glyph=glyph)

    def tagSubstLookupRecord(self, index):
        self.tagOpen('SubstLookupRecord', index=index)

    def _tagSubstLookupRecord(self):
        self.tagClose('SubstLookupRecord')

    def tagSequenceIndex(self, value):
        self.tagOpenClose('SequenceIndex', value=value)

    def tagPairPos(self, index, format):
        # Index can be None, if called by an extension lookup
        self.tagOpen('PairPos', index=index, Format=format)

    def _tagPairPos(self):
        self.tagClose('PairPos')

    def tagMarkBasePos(self, index, format):
        # Index can be None, if called by an extension lookup
        self.tagOpen('MarkBasePos', index=index, Format=format)

    def _tagMarkBasePos(self):
        self.tagClose('MarkBasePos')

    def tagMarkCoverage(self, format):
        self.tagOpen('MarkCoverage', Format=format)

    def _tagMarkCoverage(self):
        self.tagClose('MarkCoverage')

    def tagBaseCoverage(self, format):
        self.tagOpen('BaseCoverage', Format=format)

    def _tagBaseCoverage(self):
        self.tagClose('BaseCoverage')

    def tagMarkArray(self):
        self.tagOpen('MarkArray')

    def _tagMarkArray(self):
        self.tagClose('MarkArray')

    def tagBaseArray(self):
        self.tagOpen('BaseArray')

    def _tagBaseArray(self):
        self.tagClose('BaseArray')

    def tagMarkRecord(self, index):
        self.tagOpen('MarkRecord', index=index)

    def _tagMarkRecord(self):
        self.tagClose('MarkRecord')

    def tagClass(self, value):
        self.tagOpenClose('Class', value=value)

    def tagMarkAnchor(self, format):
        self.tagOpen('MarkAnchor', Format=format)

    def _tagMarkAnchor(self):
        self.tagClose('MarkAnchor')

    def tagXCoordinate(self, value):
        self.tagOpenClose('XCoordinate', value=value)

    def tagYCoordinate(self, value):
        self.tagOpenClose('YCoordinate', value=value)

    def tagBaseRecord(self, index):
        self.tagOpen('BaseRecord', index=index)

    def _tagBaseRecord(self):
        self.tagClose('BaseRecord')

    def tagBaseAnchor(self, index, format):
        self.tagOpen('BaseAnchor', index=index, Format=format)

    def _tagBaseAnchor(self):
        self.tagClose('BaseAnchor')

    def tagSinglePos(self, index, format):
        # Index can be None, if called by an extension lookup
        self.tagOpen('SinglePos', index=index, Format=format)

    def _tagSinglePos(self):
        self.tagClose('SinglePos')

    def tagValue(self, xyValue, id=None):
        if xyValue.XPlacement is not None or xyValue.XAdvance is not None or xyValue.YPlacement is not None or xyValue.YAdvance is not None:
            self.tagOpenClose('Value%s' % (id or ''), xyValue=xyValue)

    def tagValueFormat(self, format, id=None):
        self.tagOpenClose('ValueFormat%s' % (id or ''), value=format)

    def tagMarkLigPos(self, format):
        self.tagOpen('MarkLigPos', Format=format)

    def _tagMarkLigPos(self):
        self.tagClose('MarkLigPos')

    def tagLigatureCoverage(self, format):
        self.tagOpen('LigatureCoverage', Format=format)

    def _tagLigatureCoverage(self):
        self.tagClose('LigatureCoverage')

    def tagLigatureArray(self):
        self.tagOpen('LigatureArray')

    def _tagLigatureArray(self):
        self.tagClose('LigatureArray')

    def tagLigatureAttach(self, index):
        self.tagOpen('LigatureAttach', index=index)

    def _tagLigatureAttach(self):
        self.tagClose('LigatureAttach')

    def tagComponentRecord(self, index):
        self.tagOpen('ComponentRecord', index=index)

    def _tagComponentRecord(self):
        self.tagClose('ComponentRecord')

    def tagLigatureAnchor(self, index, format):
        self.tagOpen('LigatureAnchor', index=index, Format=format)

    def _tagLigatureAnchor(self):
        self.tagClose('LigatureAnchor')

    def tagPairSet(self, index):
        self.tagOpen('PairSet', index=index)

    def _tagPairSet(self):
        self.tagClose('PairSet')

    def tagPairValueRecord(self, index):
        self.tagOpen('PairValueRecord', index=index)

    def _tagPairValueRecord(self):
        self.tagClose('PairValueRecord')

    def tagSecondGlyph(self, value):
        self.tagOpenClose('SecondGlyph', value=value)

    def tagGlyphClassDef(self, format):
        self.tagOpen('GlyphClassDef', Format=format)

    def _tagGlyphClassDef(self):
        self.tagClose('GlyphClassDef')

    def tagClassDef(self, glyphName, classDef):
        self.tagOpenClose('ClassDef', glyph=glyphName, class_=classDef)

    def tagCaretList(self):
        raise 'tobeimplemented'

    def _tagCarentList(self):
        raise 'tobeimplemented'

    def tagMarkAttachClassDef(self, format):
        self.tagOpen('MarkAttachClassDef', Format=format)

    def _tagMarkAttachClassDef(self):
        self.tagClose('MarkAttachClassDef')

    def tagClassDefN(self, format, id):
        self.tagOpen('ClassDef%d' % id, Format=format)

    def _tagClassDefN(self, id):
        self.tagClose('ClassDef%d' % id)

    def tagClassNRecord(self, index, id):
        self.tagOpen('Class%dRecord' % id, index=index)

    def _tagClassNRecord(self, id):
        self.tagClose('Class%dRecord' % id)

    def tagMarkMarkPos(self, index, format):
        self.tagOpen('MarkMarkPos', index=index, Format=format)

    def _tagMarkMarkPos(self):
        self.tagClose('MarkMarkPos')

    def tagMarkNCoverage(self, format, id):
        self.tagOpen('Mark%dCoverage' % id, Format=format)

    def _tagMarkNCoverage(self, id):
        self.tagClose('Mark%dCoverage' % id)

    def tagMarkNArray(self, id):
        self.tagOpen('Mark%dArray' % id)

    def _tagMarkNArray(self, id):
        self.tagClose('Mark%dArray' % id)

    def tagMark2Record(self, index):
        self.tagOpen('Mark2Record', index=index)

    def _tagMark2Record(self):
        self.tagClose('Mark2Record')

    def tagMark2Anchor(self, index, format):
        self.tagOpen('Mark2Anchor', index=index, Format=format)

    def _tagMark2Anchor(self):
        self.tagClose('Mark2Anchor')

    def tagPosLookupRecord(self, index):
        self.tagOpen('PosLookupRecord', index=index)

    def _tagPosLookupRecord(self):
        self.tagClose('PosLookupRecord')

    def tagChainContextPos(self, index, format):
        self.tagOpen('ChainContextPos', index=index, Format=format)

    def _tagChainContextPos(self):
        self.tagClose('ChainContextPos')

    def tagXDeviceTable(self):
        self.tagOpen('XDeviceTable')

    def _tagXDeviceTable(self):
        self.tagClose('XDeviceTable')

    def tagStartSize(self, startSize):
        self.tagOpenClose('StartSize', value=startSize)

    def tagEndSize(self, endSize):
        self.tagOpenClose('EndSize', value=endSize)

    def tagDeltaFormat(self, deltaFormat):
        self.tagOpenClose('DeltaFormat', value=deltaFormat)

    def tagDeltaValue(self, deltaValue):
        self.tagOpenClose('DeltaValue', value=deltaValue)

class GTableCompiler(GTableBaseCompiler):

    #    D E C O M P I L E

    def decompile(self, gTable):
        # Decompile the fonttools gTable (GPOS or GSUB) into a construct of dict, list and State instances.
        # The result of the decompile is a State instance "gsub", that holds gsub.scripts
        # for the separate decompiled scripts.
        # The gsub.errors is a list of found error and warnings.
        # Note that there is no checking against available glyphs in the font and other
        # consistency checks. This just builds the State-based data structure.
        # Once that is available it can be used for testing, checking, manipulation and compiling.
        # This means that glyphs are referenced by name, not being represented (yet) by the
        # actual shared glyph object.
        # Storage of classes, as they are found
        self.classes = {} # Storage of classes as we can derive them from recognizing the patterns
        self.classNameIndex = 0 # Unique counter used for creating unique class names.
        # Storage of the gsub state under construction, which will be answered when the decompile is completed.
        g = self.newState()
        # Harvest the scripts & references
        self.harvestScripts(gTable, g)
        # Harvest the features, keep them in order
        self.harvestFeatures(gTable, g)
        # Harvest the actual lookups. Keep them in order.
        self.harvestLookups(gTable, g)
        # Now we decompiled the scripts, features and lookups, we can build the feature
        # list that knows which language and script is referencing to it. The scripts
        # and lookups will be appended to the features with a direct reference.
        # Then in reverse the features and lookups are added as weakref in the script
        # and lookup instances, to allow direct access and to avoid hard circle references.
        # Note that on compiling, we can no longer use the existing index numbers,
        # since the content of the features may have changed. So there we need to
        # lookup the actual index of the lookup and the feature in the list as it is.
        # @@@ Later: Add error reports if the indices are not matching the available data set.
        g.attachIndexedReferences()
        # Now run through the features to see if we can recognize glyph sequences
        # that can be replace by @class references.
        """
        for feature in gsub.features:
            tag = feature.tag # In case creating class names, use the current tag as name base.
            # The coverage areas are the most likely to find patterns of glyph names
            feature.backtrackCoverage = feature.backtrackCoverage, tag
            feature.inputCoverage = feature.inputCoverage, tag
            feature.lookAheadCoverage = feature.lookAheadCoverage, tag
        """
        return g

    def fatal(self, s):
        self.tagComment(s)
        print(s)
        raise 'fatal'

    def harvestScripts(self, gTable, g):
        # Harvest the scripts & references
        for scriptRecord in gTable.table.ScriptList.ScriptRecord:
            # script.defaults will be filled on 2nd decompile phase with feature instances.
            script = g.addScript(scriptRecord.ScriptTag, Script(scriptRecord.ScriptTag))
            # Add default as a language with name 'dflt' if DefaultLangSys exists
            if scriptRecord.Script.DefaultLangSys is not None:
                language = script.addLanguage('dflt', Language('dflt',
                    copy(scriptRecord.Script.DefaultLangSys.FeatureIndex),
                    scriptRecord.Script.DefaultLangSys.LookupOrder,
                    scriptRecord.Script.DefaultLangSys.ReqFeatureIndex,
                    script
                ))
                g.addLanguage(language) # Keep link to prevent deletion because of network weakrefs

            # LangSysRecord
            for langSysRecord in scriptRecord.Script.LangSysRecord:
                # language.features will be filled on 2nd decompile phase.
                language = script.addLanguage(langSysRecord.LangSysTag, Language(
                    langSysRecord.LangSysTag,
                    copy(langSysRecord.LangSys.FeatureIndex),
                    langSysRecord.LangSys.LookupOrder,
                    langSysRecord.LangSys.ReqFeatureIndex,
                    script
                ))
                g.addLanguage(language) # Keep link to prevent deletion because of network weakrefs

    def harvestFeatures(self, gTable, g):
        # Harvest the features, keep them in order
        # Just store the indices to the lookups, the real links will be made
        # in the 2nd phase of the decompile
        g.features = features = []
        for index, featureRecord in enumerate(gTable.table.FeatureList.FeatureRecord):
            feature = Feature(
                featureRecord.FeatureTag,
                featureRecord.Feature.FeatureParams,
                featureRecord.Feature.LookupListIndex
            )
            features.append(feature)

    def harvestLookups(self, gTable, g):
        g.lookups = lookups = []
        # The lookups list is really a list, since the script-->features-->lookups are indexed references.
        # and the order matters in the feature program.
        for lookupIndex, gLookupRecord in enumerate(gTable.table.LookupList.Lookup):
            # LookupType GSUB
            #    1         Single      Replace one glyph with one glyph
            #    2         Multiple    Replace one glyph with more than one glyph
            #    3         Alternate   Replace one glyph with one of many glyphs
            #    4         Ligature    Replace multiple glyphs with one glyph
            #    5         Context     Replace one or more glyphs in context
            #    6         Reserved    For future use
            #    7         Parent      Parent-Subset lookup for large index volumes
            # Dispatch the calls of the lookup types over implemented methods
            #
            # The lookupRecord is on the level of lookupFlag, lookupType and Subtable.
            # This could imply both the call for an extension parent (type 7 in GSUB
            # or type 9 in GPOS) or a direct call for a lookup type. On both situations
            # the lookupRecord should have compatible levels.
            #
            lookup = Lookup(gLookupRecord.LookupType, gLookupRecord.LookupFlag) # Contains list of LookupSub instances
            lookup.orgIndex = lookupIndex # For debugging, keep the original index of the lookup
            for gSub in gLookupRecord.SubTable:
                hook = '_decompileLookupSub%d' % gSub.LookupType
                lookup.subs.append(getattr(self, hook)(gSub, gTable))
            lookups.append(lookup)

    #     C O M P I L E  2  F E A T U R E  T A L K

    def compile2FeatureTalk(self, g):
        # Compile the "g" State to FeatureTalk source, with the aim that it stays the
        # same for compile/decompile to between the source and the objects
        self._groups = GroupSet() # Groups of combined glyph names. Key is list, value is name.
        self.newOutput() # Reset output stream
        # First do all lookups, so we aggregate the groups of glyphs by name.
        for tag, lookups in sorted(g.getUniqueLookups().items()): # Get dictionary of unique lookup with feature.tag as key
            # Do all referencing features have the same tag?
            self.write('feature %s { # %s\n' % (tag, FC.FEA_COMMENTS.get(tag, '')))
            for lookup in lookups:
                self.write(lookup.getFeatureTalk(tag, self._groups))
            self.write('} %s;\n\n' % tag)
        body = self.getOutput()
        # We have the body, but the definition of the agregated groups should be written in at the start of the file.
        # So we make another output before returning.
        self.newOutput() # Reset output stream
        self.write('# \n')
        # languagesystems
        self.write('# LANGUAGE SYSTEMS\n')
        for scriptName, script in g.scripts.items():
            for languageName, language in script.languages.items():
                self.write('languagesystem %s %s\n' % (scriptName, languageName))
            self.write('\n')
        # Write the groups
        for name, glyphs in sorted(self._groups.items()):
            self.write('@%s = [%s];\n' % (name, ' '.join(glyphs)))
        self.write('\n\n')
        # Write the body
        self.write(body)
        return self.getOutput()

    #     C O M P I L E  2  T T X / X M L

    def compile2XML(self, g):
        # Compile the "g" State to the FontTools XML, so we can use that to compile to fonttools objects.
        self.newOutput() # Reset output stream
        self.writeXmlHeader()
        self.write('<ttFont sfntVersion="OTTO" ttLibVersion="2.2">\n')
        self.tagRoot()
        self.tagVersion('1.0')
        # S C R I P T L I S T
        self.compileScripts2XML(g)
        # F E A T U R E  L I S T
        self.compileFeatures2XML(g)
        # L O O K U P  L I S T
        self.compileLookups2XML(g)
        self._tagRoot()
        self.write('</ttFont>\n')
        return self.getOutput()

    def compileScripts2XML(self, g):
        # Compile the gTable instance to TTX/XML
        self.tagScriptList()
        self.tagComment('ScriptCount=%s' % len(g.scripts))
        for index, scriptTag in enumerate(sorted(g.scripts.keys())):
            script = g.scripts[scriptTag]
            self.tagScriptRecord(index)
            self.tagScriptTag(script.tag)
            self.tagScript()
            # Handle the default, if it exists in the table.
            default = script.getDefault()
            # Run through the default lookups of the features to see which is connected to this script,
            # so from that we know the index in the feature list. Also collect them all before output,
            # because we need the total amount for the FeatureCount comment.
            featureIndicesOfScript = []
            if default is not None:
                self.tagDefaultLangSys()
                self.tagReqFeatureIndex(default.reqFeatureIndex) # For now, what does it do? Need to recalculate?
                for feature in default.features:
                    featureIndicesOfScript.append(g.features.index(feature))
                self.tagComment('FeatureCount=%d' % len(featureIndicesOfScript))
                for index, value in enumerate(featureIndicesOfScript):
                    self.tagFeatureIndex(index, value)
                self._tagDefaultLangSys()
            # LangSysRecord
            index = 0 # Separate count, to ignore the default
            self.tagComment('LangSysCount=%d' % (len(script.languages)-1)) # Ignore the default
            for languageTag, language in sorted(script.languages.items()):
                if languageTag == 'dflt':
                    continue # Skip the default in the main language list, we already did that.
                self.tagLangSysRecord(index)
                self.tagLangSysTag(languageTag)
                self.tagLangSys()
                self.tagReqFeatureIndex(language.reqFeatureIndex)
                featureIndicesOfLanguage = []
                for feature in language.features:
                    featureIndicesOfLanguage.append(g.features.index(feature))
                self.tagComment('FeatureCount=%d' % len(featureIndicesOfLanguage))
                for featureIndex, value in enumerate(featureIndicesOfLanguage):
                    self.tagFeatureIndex(featureIndex, value)
                self._tagLangSys()
                self._tagLangSysRecord()
                index += 1
            self._tagScript()
            self._tagScriptRecord()
        self._tagScriptList()

    def compileFeatures2XML(self, g):
        # Compile the GTable to FontTools XML source.
        self.tagFeatureList()
        self.tagComment('FeatureCount=%d' % len(g.features))
        for index, feature in enumerate(g.features):
            self.tagFeatureRecord(index)
            self.tagFeatureTag(feature.tag)
            self.tagFeature()
            self.tagComment('LookupCount=%d' % len(feature.lookups))
            for index, lookup in enumerate(feature.lookups):
                if lookup is not None:
                    self.tagLookupListIndex(index, g.lookups.index(lookup)) # Lookup is now the real lookup instance
            self._tagFeature()
            self._tagFeatureRecord()
        self._tagFeatureList()

