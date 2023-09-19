# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    gsubcompiler.py
#
#    http://partners.adobe.com/public/developer/opentype/index_table_formats1.html
#
from copy import copy

from tnbits.compilers.subsetting.states import LookupSub, ChainLookup, Coverage, GSUBState, Ligature, Chain
from tnbits.compilers.subsetting.gtablecompiler import GTableCompiler

def tobedeveloped():
    print('TO BE DEVELOPED')
    exit()

class LookupSub1(LookupSub):
    """Inheriting lookups for each type, so we can define intelligence for each type.
    Replace  one glyph with one glyph.

    inputGlyph --> outputGlyph

    Input: self.single.keys()
    Output: self.single.values()
    """
    """
    Example TTX:
    <ExtensionSubst index="0" Format="1">
      <ExtensionLookupType value="1"/>
      <SingleSubst Format="2">
        <Substitution in="uni060C" out="uni060C.MLY.SND"/>
        <Substitution in="uni061B" out="uni061B.MLY.SND"/>
        <Substitution in="uni064C" out="uni064C.MLY"/>
        <Substitution in="uni064C0651" out="uni064C0651.MLY"/>
      </SingleSubst>
    </ExtensionSubst>
    """
    type = 1

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        return len(self.single) > 0

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        glyphNames = []
        # Collect all glyph names used by this feature
        for key, glyphs in self.single.items():
            glyphNames.append(key)
            # Just test on the type, as the FontTools tables seems to ignore the format?
            if not isinstance(glyphs, (list, tuple)):
                glyphs = [glyphs] # glyphs is a single name
            for glyph in glyphs:
                glyphNames.append(glyph)
        return glyphNames

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        return set(self.single.keys())

    def hasGlyph(self, glyphName):
        found = False
        for glyphs in self.single.values():
            if glyphName in glyphs:
                found = True
                break
        return found

    def deleteGlyph(self, glyphName):
        """Delete the glyphName from self.single. If self.single[glyphName]
        exists, and it is a single glyph name value, then delete the whole entry.
        If the self.single[glyphName] is a tuple/list of the output set, then remove the glyphName
        from the output list. If the list became empty, then remove the whole entry."""
        self.deleteInputGlyph(glyphName)
        self.deleteOutputGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        # For the remaining glyphs, test if glyphName is one of the values.
        if glyphName == 'afii57664':
            pass
        for key, glyphOrGlyphs in self.single.items():
            # Just test on the type, as the FontTools tables seems to ignore the format?
            if isinstance(glyphOrGlyphs, (list, tuple)):
                if glyphName in glyphOrGlyphs:
                    del self.single[key][self.single[key].index(glyphName)]
                if not self.single[key]: # Glyphs list became empty, remove the whole entry
                    del self.single[key]
            elif glyphOrGlyphs == glyphName: # glyphsOrGlyph is a single name, delete the whole entry
                del self.single[key]

    def deleteInputGlyph(self, glyphName):
        U"""Delete the input glyphName input entry, if it exists. The values are untouched.
        Deletion is simple and straightforward, as the input-output glyphs are connected in the dictionary.
        Deleting the key also deletes the value glyph name."""
        if glyphName == 'afii57664':
            pass
        if glyphName in self.single:
            del self.single[glyphName]

    def getFeatureTalk(self, tag, groupSet, indent):
        ft = ['%s# Lookup 1\n' % (indent*'\t')]
        # Collect the groups in this single conversion
        srcs = []
        dsts = []
        for src, dst in sorted(self.single.items()):
            srcs.append(src)
            dsts.append(dst)
        # Aggregate group
        srcId = groupSet.aggregate(tag, srcs)
        dstId = groupSet.aggregate(tag, dsts)
        ft.append('\tsub %s by %s\n' % (srcId, dstId))
        return ''.join(ft)

    def glyphUsage(self, glyphName):
        return 'LookupSub1'

class LookupSub2(LookupSub):
    """Inheriting lookups for each type, so we can intelligent for each type.
    A Multiple Substitution (MultipleSubst) subtable replaces a single glyph with more than one glyph,
    as when multiple glyphs replace a single ligature. The subtable has a single format: MultipleSubstFormat1.
    The subtable specifies a format identifier (SubstFormat), an offset to a Coverage table that defines the
    input glyph indices, a count of offsets in the Sequence array (SequenceCount), and an array of offsets
    to Sequence tables that define the output glyph indices (Sequence). The Sequence table offsets are
    ordered by the Coverage Index of the input glyphs.
    For each input glyph listed in the Coverage table, a Sequence table defines the output glyphs. Each Sequence
    table contains a count of the glyphs in the output glyph sequence (GlyphCount) and an array of output glyph
    indices (Substitute).

    inputGlyph --> [outputGlyph, outputGlyph, ...]

    Input: Sequence
    Output: Coverage
    """
    type = 2

    def keepIt(self):
        # Still glyphs defined, then keep this lookup.
        return bool(self.coverage.glyphs and self.sequences)

    def deleteGlyph(self, glyphName):
        if glyphName == 'afii57664':
            pass
        self.deleteInputGlyph(glyphName)
        self.deleteOutputGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        if self.format == 1:
            while glyphName in self.coverage.glyphs:
                del self.coverage.glyphs[self.coverage.glyphs.index(glyphName)]
        elif self.format == 2:
            while glyphName in self.coverage.glyphs:
                del self.coverage.glyphs[self.coverage.glyphs.index(glyphName)]
        else: # Unknown format
            self.error()

    def deleteInputGlyph(self, glyphName):
        if glyphName == 'afii57664':
            pass
        if self.format == 1:
            sequences = []
            for sequence in self.sequences:
                while glyphName in sequence:
                    del sequence[sequence.index(glyphName)]
                if sequence: # Still not empty?
                    sequences.append(sequence)
            self.sequences = sequences
        elif self.format == 2:
            sequences = []
            for sequence in self.sequences:
                while glyphName in sequence:
                    del sequence[sequence.index(glyphName)]
                if sequence: # Still not empty?
                    sequences.append(sequence)
            self.sequences = sequences
        else: # Unknown format
            self.error()

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        glyphNames = self.coverage.glyphs[:]
        for sequence in self.sequences:
            for glyphName in sequence:
                glyphNames.append(glyphName)
        return glyphNames

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        glyphNames = []
        for sequence in self.sequences:
            for glyphName in sequence:
                glyphNames.append(glyphName)
        return glyphNames

    def getFeatureTalk(self, tag, groupsset, indent):
        ft = ['%s# Lookup 2\n' % (indent*'\t')]
        return ''.join(ft)

    def glyphUsage(self, glyphName):
        return 'LookupSub2'

class LookupSub3(LookupSub):
    """Inheriting lookups for each type, so we can intelligent for each type."""
    type = 3

    def keepIt(self):
        tobedeveloped

    def deleteGlyph(self, glyphName):
        self.deleteInputGlyph(glyphName)
        self.deleteOutputGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        tobedeveloped

    def deleteInputGlyph(self, glyphName):
        tobedeveloped

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        tobedeveloped

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        tobedeveloped

    def getFeatureTalk(self, tag, groupSet, indent):
        ft = ['%s# Lookup 3\n' % (indent*'\t')]
        return ''.join(ft)

    def glyphUsage(self, glyphName):
        return 'LookupSub3'

class LookupSub4(LookupSub):
    """Inheriting lookups for each type, so we can intelligent for each type.
    A Ligature Substitution (LigatureSubst) subtable identifies ligature substitutions where a single
    glyph replaces multiple glyphs. One LigatureSubst subtable can specify any number of ligature substitutions.
    The subtable uses a single format: LigatureSubstFormat1. It contains a format identifier
    (SubstFormat), a Coverage table offset (Coverage), a count of the ligature sets defined in this
    table (LigSetCount), and an array of offsets to LigatureSet tables (LigatureSet). The Coverage
    table specifies only the index of the first glyph component of each ligature set.
    """
    """
    Example TTX:
    <ExtensionSubst index="0" Format="1">
      <ExtensionLookupType value="4"/>
      <LigatureSubst Format="1">
        <LigatureSet glyph="uni0651">
          <Ligature components="uni064E" glyph="uni064E0651"/>
          <Ligature components="uni064F" glyph="uni064F0651"/>
          <Ligature components="uni064C" glyph="uni064C0651"/>
          <Ligature components="uni064B" glyph="uni064B0651"/>
          <Ligature components="uni064C.MLY" glyph="uni064C0651.MLY"/>
          <Ligature components="uni0670" glyph="uni06510670"/>
        </LigatureSet>
        <LigatureSet glyph="uni0654">
          <Ligature components="uni064C" glyph="uni0654064C"/>
          <Ligature components="uni064E" glyph="uni0654064E"/>
          <Ligature components="uni064F" glyph="uni0654064F"/>
          <Ligature components="uni064B" glyph="uni06540651"/>
          <Ligature components="uni0652" glyph="uni06540652"/>
        </LigatureSet>
        <LigatureSet glyph="uni0655">
          <Ligature components="uni064D" glyph="uni0655064D"/>
          <Ligature components="uni0650" glyph="uni06550650"/>
        </LigatureSet>
      </LigatureSubst>
    </ExtensionSubst>
    """
    type = 4

    def keepIt(self):
        # If one or more of the ligatures needs to be kept, then this lookup needs to be kept.
        keepIt = False
        for ligatureList in self.ligatures.values():
            for ligature in ligatureList:
                if ligature.keepIt():
                    keepIt = True
                    break
            if keepIt:
                break
        return keepIt

    def deleteGlyph(self, glyphName):
        self.deleteInputGlyph(glyphName)
        self.deleteOutputGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        if glyphName == 'afii57664':
            pass
        for _, ligatures in self.ligatures.items(): # key, ligatures
            for ligature in ligatures:
                if glyphName in ligature.components:
                    del ligature.components[ligature.components.index(glyphName)]
                if ligature.lig == glyphName:
                    ligature.lig = None
                    ligature.glyphName = None # Flag not to keep this Ligature instance.

    def deleteInputGlyph(self, glyphName):
        # Delete the ligature that has glyphName as input glyph.
        # @@@ For now we just answer the set with ligature keys.
        # @@@ Do we need to add more? Are other glyphs also interpreted as input?
        if glyphName == 'afii57664':
            pass
        if glyphName in self.ligatures:
            del self.ligatures[glyphName]

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        glyphNames = []
        for key, ligatures in self.ligatures.items():
            glyphNames.append(key)
            for ligature in ligatures:
                glyphNames.append(ligature.glyph)
                if ligature.lig is not None:
                    glyphNames.append(ligature.lig)
                for component in ligature.components:
                    glyphNames.append(component)
        return glyphNames

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        # @@@ For now we just answer the set with ligature keys.
        # @@@ Do we need to add more? Are other glyphs also interpreted as input?
        return set(self.ligatures.keys())

    def getFeatureTalk(self, tag, groupSet, indent):
        ft = ['%s# Lookup 4\n' % (indent*'\t')]
        return ''.join(ft)

    def glyphUsage(self, glyphName):
        return 'LookupSub4'

class LookupSub5(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 5

    def keepIt(self):
        tobedeveloped

    def deleteGlyph(self, glyphName):
        self.deleteOutputGlyph(glyphName)
        self.deleteInputGlyph(glyphName)

    def deleteOutputGyph(self, glyphName):
        tobedeveloped

    def deleteInputGlyph(self, glyphName):
        tobedeveloped

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        tobedeveloped

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        tobedeveloped

    def getFeatureTalk(self, tag, groupSet, indent):
        ft = ['%s# Lookup 5\n' % (indent*'\t')]
        return ''.join(ft)

    def glyphUsage(self, glyphName):
        return 'LookupSub5'

class LookupSub6(LookupSub):
    """Inheriting lookups for each type, so we can intelligent for each type."""
    type = 6

    def keepIt(self):
        referencedKeepIt = keepIt = False
        for chain in self.chains:
            if chain.keepIt():
                keepIt = True
                break
        if keepIt:
            # Check if there is at least one lookup referencing to self that needs to be kept
            # @@@ There is currently no check on circle referencing lookups. Is that allowed?
            # @@@ Or is it likely to happen? Is it a way to crash render engines?
            for lookup in self.referencingLookups:
                if lookup.keepIt():
                    referencedKeepIt = True
                    break
        return keepIt
        #return referencedKeepIt and keepIt

    def deleteGlyph(self, glyphName):
        for chain in self.chains:
            chain.deleteGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        for chain in self.chains:
            chain.deleteOutputGlyph(glyphName)

    def deleteInputGlyph(self, glyphName):
        for chain in self.chains:
            chain.deleteInputGlyph(glyphName)

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        glyphNames = []
        if self.format == 1:
            tobedeveloped()
        elif self.format == 2:
            tobedeveloped()
        elif self.format == 3:
            for chain in self.chains:
                for backtrackCoverage in chain.backtrackCoverage:
                    for glyph in backtrackCoverage.glyphs:
                        glyphNames.append(glyph)
                for inputCoverage in chain.inputCoverage:
                    for glyph in inputCoverage.glyphs:
                        glyphNames.append(glyph)
                for lookAheadCoverage in chain.lookAheadCoverage:
                    for glyph in lookAheadCoverage.glyphs:
                        glyphNames.append(glyph)
        else:
            self.error()
        return glyphNames

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        glyphSet = set()
        if self.format == 1:
            tobedeveloped
        elif self.format == 2:
            tobedeveloped
        elif self.format == 3:
            for chain in self.chains:
                for inputCoverage in chain.inputCoverage:
                    glyphSet = glyphSet.union(set(inputCoverage.glyphs))
        else:
            self.error()
        return glyphSet

    def getFeatureTalk(self, tag, groupSet, indent):
        # sub f' @calt_f_i by f.calt_nokern;
        # sub f' @calt_f_asc by f.calt_nokern;
        ft = ['%s# Lookup 6\n' % (indent*'\t')]
        for chain in self.chains:
            # Aggregate groups
            backtrackIds = []
            for glyphList in chain.backtrackCoverage.glyphs:
                backtrackIds.append(groupSet.aggregate(tag, glyphList))
            inputIds = []
            for glyphList in chain.inputCoverage.glyphs:
                inputIds.append(groupSet.aggregate(tag, glyphList))
            lookAheadIds = []
            for glyphList in chain.lookAheadCoverage.glyphs:
                lookAheadIds.append(groupSet.aggregate(tag, glyphList))
            # Output the ids
            for index in range(len(inputIds)):
                backtrackId = lookAheadId = ''
                if backtrackIds:
                    backtrackId = backtrackIds[index] + ' '
                if lookAheadIds:
                    lookAheadId = ' ' + lookAheadIds[index]
                ft.append("\tsub %s%s'%s by %s\n" % (backtrackId, inputIds[0], lookAheadId, 'XXX'))
        return ''.join(ft)

    def attachIndexReferencedLookup(self, parent, lookups):
        # If this is a lookup type 6 and 7, then there may be substitution
        # references to other lookups. Fill them in with the real
        # links if they are present.
        # As now there is a direct link, the index numbers become obsolete.
        # Editing the lookups may cause them to have different index
        # numbers on output.
        for chain in self.chains:
            for chainLookup in chain.lookups:
                chainLookup.lookup = lookups[chainLookup.lookupIndex]
                chainLookup.lookup.attachReferencingLookup(parent) # Attach in reverse direction too for the parent of self

    def updateLookupIndices(self, lookups):
        # If the lookups are added or deleted, then the current index numbers
        # of referenced lookups may no longer be valid. Use the current lookup
        # (if there is an existing reference) to get it's index in the lookup
        # table, and store it in the index field.
        for chain in self.chains:
            for chainLookup in chain.lookup:
                if chainLookup.lookup is not None:
                    assert chainLookup.lookup in lookups
                    chainLookup.index = lookups.index(chainLookup.lookup) # Store index of the referenced lookup

    def glyphUsage(self, glyphName):
        return 'LookupSub6'
        #usages = []
        #for chain in self.chains:
        #    usages.append(chain.glyphUsage(glyphName))
        #return '\n'.join(usages)

class LookupSub7(LookupSub):
    """Inheriting lookups for each type, so we can intelligent for each type.
    This lookup provides a mechanism whereby any other lookup type's subtables are stored at
    a 32-bit offset location in the 'GSUB' table. This is needed if the total size of the
    subtables exceeds the 16-bit limits of the various other offsets in the 'GSUB' table.
    In this specification, the subtable stored at the 32-bit offset location is termed the
    "extension" subtable.
    """
    """
    Example TTX:
    <LookupType value="7"/>
    <LookupFlag value="1"/>
    <!-- SubTableCount=1 -->
    <ExtensionSubst index="0" Format="1">
      <ExtensionLookupType value="1"/>
        ...
        ...
      <SingleSubst Format="2">
        <Substitution in="uni060C" out="uni060C.MLY.SND"/>
        <Substitution in="uni061B" out="uni061B.MLY.SND"/>
        <Substitution in="uni064C" out="uni064C.MLY"/>
        <Substitution in="uni064C0651" out="uni064C0651.MLY"/>
      </SingleSubst>
        ...
        ...
    </ExtensionSubst>
    """
    type = 7

    def keepIt(self):
        return self.extension.keepIt()

    def deleteGlyph(self, glyphName):
        self.extension.deleteGlyph(glyphName)

    def deleteOutputGlyph(self, glyphName):
        self.extension.deleteOutputGlyph(glyphName)

    def deleteInputGlyph(self, glyphName):
        self.extension.deleteInputGlyph(glyphName)

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        return self.extension.getGlyphNames()

    def getInputGlyphNames(self):
        # Answer the set of all input glyph names in the lookup.
        return self.extension.getInputGlyphNames()

    def getFeatureTalk(self, tag, groupSet, indent):
        return self.extension.getFeatureTalk(tag, groupSet, indent)

    def attachIndexReferencedLookup(self, parent, lookups):
        # If this is a lookup type 6 and 7, then there may be substitution
        # references to other lookups. Fill them in with the real
        # links if they are present. For other types this call is ignored.
        # The call is ignored for the other lookup types.
        self.extension.attachIndexReferencedLookup(parent, lookups)

    def updateLookupIndices(self, lookups):
        self.extension.updateLookupIndices(lookups)

    def glyphUsage(self, glyphName):
        return self.extension.glyphUsage(glyphName)

class GSUBCompiler(GTableCompiler):
    # The GSUBCompiler compiles/decompiles the fonttools instance (ttFont['GSUB']) into
    # a State instance with contained states, lists, dicts, which then is answered.

    TABLE_TAG = 'GSUB'

    def newState(self):
        return GSUBState()

    #    L O O K U P  F O R M A T S

    def _decompileLookupSub1(self, gLookupSub, gTable):
        # Single substitution (SingleSubst) subtables tell a client to replace a single glyph with another glyph.
        # The subtables can be either of two formats. Both formats require two distinct sets of glyph indices:
        # one that defines input glyphs (specified in the Coverage table), and one that defines the output glyphs.
        # Format 1 requires less space than Format 2, but it is less flexible.
        # Defines lookup.single mapping dictionary
        # Actual output format will be decided on, depending on the amount of single mappings.
        lookupSub = LookupSub1() # lookup.type is class value
        lookupSub.format = gLookupSub.Format # Just storing to keep the original value
        # Dictionary of glyph-->glyph substitutions, same for both formats.
        lookupSub.single = copy(gLookupSub.mapping)
        return lookupSub

    def _decompileLookupSub2(self, gLookupSub, gTable):
        # A Multiple Substitution (MultipleSubst) subtable replaces a single glyph with more
        # than one glyph, as when multiple glyphs replace a single ligature. The subtable has
        # a single format: MultipleSubstFormat1. The subtable specifies a format identifier
        # (SubstFormat), an offset to a Coverage table that defines the input glyph indices,
        # a count of offsets in the Sequence array (SequenceCount), and an array of offsets to
        # Sequence tables that define the output glyph indices (Sequence). The Sequence table
        # offsets are ordered by the Coverage Index of the input glyphs.
        # For each input glyph listed in the Coverage table, a Sequence table defines the output
        # glyphs. Each Sequence table contains a count of the glyphs in the output glyph sequence
        # (GlyphCount) and an array of output glyph indices (Substitute).
        # Note: The order of the output glyph indices depends on the writing direction of the
        # text. For text written left to right, the left-most glyph will be first glyph in the
        # sequence. Conversely, for text written right to left, the right-most glyph will be first.
        # The use of multiple substitution for deletion of an input glyph is prohibited.
        # GlyphCount should always be greater than 0.
        lookupSub = LookupSub2() # lookup.type is class value
        lookupSub.format = gLookupSub.Format # Just storing to keep the original value
        if lookupSub.format == 1:
            lookupSub.coverage = Coverage(gLookupSub.Coverage.glyphs[:], gLookupSub.Coverage.Format)
            lookupSub.sequences = []
            for sequence in gLookupSub.Sequence:
                lookupSub.sequences.append(copy(sequence.Substitute))
        else: # Unknown format, only 1 format for lookup 2
            self.error()
        return lookupSub

    def _decompileLookupSub3(self, gLookupSub, gTable):
        # An Alternate Substitution (AlternateSubst) subtable identifies any number of aesthetic
        # alternatives from which a user can choose a glyph variant to replace the input glyph.
        # For example, if a font contains four variants of the ampersand symbol, the cmap table
        # will specify the index of one of the four glyphs as the default glyph index, and an
        # AlternateSubst subtable will list the indices of the other three glyphs as alternatives.
        # A text-processing client would then have the option of replacing the default glyph with
        # any of the three alternatives.
        # The subtable has one format: AlternateSubstFormat1. The subtable contains a format
        # identifier (SubstFormat), an offset to a Coverage table containing the indices of glyphs
        # with alternative forms (Coverage), a count of offsets to AlternateSet tables (AlternateSetCount),
        # and an array of offsets to AlternateSet tables (AlternateSet).
        # For each glyph, an AlternateSet subtable contains a count of the alternative glyphs
        # (GlyphCount) and an array of their glyph indices (Alternate). Because all the glyphs
        # are functionally equivalent, they can be in any order in the array.
        lookupSub = LookupSub3() # lookup.type is class value
        lookupSub.format = gLookupSub.Format # Just storing to keep the original value
        if lookupSub.format == 1:
            lookupSub.alternates = copy(gLookupSub.alternates) # Dictionary glyph: alternateGlyphs
        else: # Unknown format, only 1 format for lookup 3
            self.error()
        return lookupSub

    def _decompileLookupSub4(self, gLookupSub, gTable):
        # A Ligature Substitution (LigatureSubst) subtable identifies ligature substitutions
        # where a single glyph replaces multiple glyphs. One LigatureSubst subtable can specify
        # any number of ligature substitutions.
        # The subtable uses a single format: LigatureSubstFormat1. It contains a format identifier
        # (SubstFormat), a Coverage table offset (Coverage), a count of the ligature sets defined
        # in this table (LigSetCount), and an array of offsets to LigatureSet tables (LigatureSet).
        # The Coverage table specifies only the index of the first glyph component of each ligature set.
        lookupSub = LookupSub4() # lookup.type is class value
        lookupSub.format = gLookupSub.Format # Just storing to keep the original value
        if lookupSub.format == 1:
            lookupSub.ligatures = ligatures = {}
            for glyphName, tableLigatures in gLookupSub.ligatures.items():
                ligatures[glyphName] = ligatureSet = []
                for tableLigature in tableLigatures:
                    ligatureSet.append(Ligature(
                        glyphName,
                        tableLigature.LigGlyph,
                        copy(tableLigature.Component)
                    ))
        else: # Unknown format, only 1 format for lookup 4
            self.error()
        return lookupSub

    def _decompileLookupSub5(self, gLookupSub, gTable):
        # A Contextual Substitution (ContextSubst) subtable defines the most powerful type of
        # glyph substitution lookup: it describes glyph substitutions in context that replace
        # one or more glyphs within a certain pattern of glyphs.
        # ContextSubst subtables can be any of three formats that define a context in terms of
        # a specific sequence of glyphs, glyph classes, or glyph sets. Each format can describe
        # one or more input glyph sequences and one or more substitutions for each sequence.
        # All three formats of ContextSubst subtables specify substitution data in a SubstLookupRecord.
        lookupSub = LookupSub5()
        tobedeveloped()
        return lookupSub

    def _decompileLookupSub6(self, gLookupSub, gTable):
        # A Chaining Contextual Substitution subtable (ChainContextSubst) describes glyph substitutions
        # in context with an ability to look back and/or look ahead in the sequence of glyphs.
        # The design of the Chaining Contextual Substitution subtable is parallel to that of the
        # Contextual Substitution subtable, including the availability of three formats for handling
        # sequences of glyphs, glyph classes, or glyph sets. Each format can describe one or more backtrack,
        # input, and lookahead sequences and one or more substitutions for each sequence.
        # Actual output format will be decided on content of the lookup.
        lookupSub = LookupSub6()
        lookupSub.format = gLookupSub.Format # Just storing the original format.
        lookupSub.chains = []
        if lookupSub.format == 1:
            tobedeveloped()
        elif lookupSub.format == 2:
            tobedeveloped()
        elif lookupSub.format == 3:
            chain = Chain()
            chain.format = gLookupSub.Format
            lookupSub.chains.append(chain)
            chain.backtrackCoverage = []
            for backtrackCoverage in gLookupSub.BacktrackCoverage:
                chain.backtrackCoverage.append(Coverage(copy(backtrackCoverage.glyphs), backtrackCoverage.Format))
            chain.inputCoverage = []
            for inputCoverage in gLookupSub.InputCoverage:
                chain.inputCoverage.append(Coverage(copy(inputCoverage.glyphs), inputCoverage.Format))
            chain.lookAheadCoverage = []
            for lookAheadCoverage in gLookupSub.LookAheadCoverage:
                chain.lookAheadCoverage.append(Coverage(copy(lookAheadCoverage.glyphs), lookAheadCoverage.Format))
            chain.lookups = []
            for lookupRecord in gLookupSub.SubstLookupRecord:
                # Just store index for now.
                # Later make a direct link to this record in one direction and a weakref on the other direction
                chainLookup = ChainLookup(lookupRecord.LookupListIndex, lookupRecord.SequenceIndex)
                chain.lookups.append(chainLookup)
        else: # Unknown format
            self.error()
        return lookupSub

    def _decompileLookupSub7(self, gLookupSub, gTable):
        # Indirect level of subtable. lookup.type is defined as class value
        lookupSub = LookupSub7()
        lookupSub.format = gLookupSub.Format
        lookupSub.extensionLookupType = gLookupSub.ExtensionLookupType
        # Dispatch the lookup type on 2nd level.
        hook = '_decompileLookupSub%d' % gLookupSub.ExtSubTable.LookupType
        lookupSub.extension = getattr(self, hook)(gLookupSub.ExtSubTable, gTable)
        return lookupSub

    #  C L A S S  S U B S T I T U T I O N

    def _glyphList2Code(self, glyphList, tag):
        className = self._guessClassName(glyphList, tag)
        if className is not None:
            return '@%s' % className
        return ' '.join(glyphList)

    #    C O M P I L E  2 F E A T U R E  T A L K

    #    C O M P I L E  2  T T X / X M L

    def compileLookups2XML(self, gsub):
        # Compile the lookups to TTX/XML. Bootstrap the output of the tree.
        self.tagLookupList()
        self.tagComment('LookupCount=%d' % len(gsub.lookups))
        for lookupIndex, lookup in enumerate(gsub.lookups):
            if lookupIndex != lookup.orgIndex:
                self.tagComment('OriginalIndex=%d' % lookup.orgIndex)
            self.tagLookup(lookupIndex)
            self.tagLookupType(lookup.type)
            self.tagLookupFlag(lookup.flag)
            self.tagComment('SubTableCount=%s' % len(lookup.subs))
            for subIndex, lookupSub in enumerate(lookup.subs):
                hook = '_compileLookupSub%d' % lookup.type
                getattr(self, hook)(lookupSub, gsub, subIndex)
            self._tagLookup()
        self._tagLookupList()

    def _compileLookupSub1(self, lookupSub, gTable, index=None):
        # Export the LookupSub1. Index can be None if called by the extension parent.
        self.tagSingleSubst(index=index, format=lookupSub.format)
        for src, substition in sorted(lookupSub.single.items()):
            self.tagSubstitution(src, substition)
        self._tagSingleSubst()

    def _compileLookupSub2(self, lookupSub, gTable, index=None):
        # Export the LookupSub2. Index can be None if called by the extension parent.
        self.tagMultipleSubst(index=index, format=lookupSub.format)
        #self.tagLookupFlag(value=parent.flag)
        self.tagCoverage(lookupSub.coverage.format)
        for glyphName in lookupSub.coverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagCoverage()
        self.tagComment('SequenceCount=%d' % len([lookupSub.sequences]))
        for sequenceIndex, sequence in enumerate(lookupSub.sequences):
            self.tagSequence(sequenceIndex)
            self.tagComment('GlyphCount=%d' % len(sequence))
            for glyphIndex, glyphName in enumerate(sequence):
                self.tagSubstitute(index=glyphIndex, value=glyphName)
            self._tagSequence()
        self._tagMultipleSubst()

    def _compileLookupSub3(self, lookupSub, gTable, index=None):
        # Export the LookupSub3. Index can be None if called by the extension parent.
        for alternateIndex, (baseName, alternates) in enumerate(sorted(lookupSub.alternates.items())):
            self.tagAlternateSubst(alternateIndex, 1) # Try format 1 first
            self.tagAlternateSet(glyph=baseName)
            for glyphName in alternates:
                self.tagAlternate(glyph=glyphName)
            self._tagAlternateSet()
            self._tagAlternateSubst()

    def _compileLookupSub4(self, lookupSub, gTable, index=None):
        # Export the LookupSub4. Index can be None if called by the extension parent.
        self.tagLigatureSubst(index=index, format=lookupSub.format)
        for glyphName, ligatures in sorted(lookupSub.ligatures.items()):
            self.tagLigatureSet(glyph=glyphName)
            for ligature in ligatures:
                if ligature.components and ligature.lig: # Should have been cleaned up, but just to be sure.
                    self.tagLigature(components=','.join(ligature.components), glyph=ligature.lig)
            self._tagLigatureSet()
        self._tagLigatureSubst()

    def _compileLookupSub5(self, lookupSub, gTable, index=None):
        # Export the LookupSub5. Index can be None if called by the extension parent.
        tobedeveloped()

    def _compileLookupSub6(self, lookupSub, gTable, index=None):
        # Export the LookupSub6. Index can be None if called by the extension parent.
        for chain in lookupSub.chains:
            self.tagChainContextSubst(chain.format)
            self.tagComment('BacktrackGlyphCount=%d' % len(chain.backtrackCoverage))
            for backtrackCoverageIndex, coverage in enumerate(chain.backtrackCoverage):
                if coverage.glyphs:
                    self.tagBacktrackCoverage(backtrackCoverageIndex, coverage.format)
                    for glyphName in coverage.glyphs:
                        self.tagGlyph(glyphName)
                    self._tagBacktrackCoverage()
            self.tagComment('InputGlyphCount=%d' % len(chain.inputCoverage))
            for inputCoverageIndex, coverage in enumerate(chain.inputCoverage):
                if coverage.glyphs:
                    self.tagInputCoverage(inputCoverageIndex, coverage.format)
                    for glyphName in coverage.glyphs:
                        self.tagGlyph(glyphName)
                    self._tagInputCoverage()
            self.tagComment('LookAheadGlyphCount=%s' % len(chain.lookAheadCoverage))
            for lookAheadCoverageIndex, coverage in enumerate(chain.lookAheadCoverage):
                if coverage.glyphs:
                    self.tagLookAheadCoverage(lookAheadCoverageIndex, coverage.format)
                    for glyphName in coverage.glyphs:
                        self.tagGlyph(glyphName)
                    self._tagLookAheadCoverage()
            self.tagComment('SubstCount=%d' % len(chain.lookups))
            if chain.lookups:
                for chainLookupIndex, chainLookup in enumerate(chain.lookups):
                    self.tagSubstLookupRecord(chainLookupIndex)
                    self.tagSequenceIndex(chainLookup.sequenceIndex)
                    if chainLookup.lookup is None:
                        self.tagComment('XXXXXXXXXXXXXXXXXXXXXXXX')
                        #self.fatal('###### Error: chainLookup.lookup of lookup %s is None' %  chainLookup.lookup.orgIndex)
                    elif not chainLookup.lookup in gTable.lookups:
                        self.fatal('###### Error: no chainLookup.lookup in gTable.lookups of ')
                    else: # chainLookup.lookup.orgIndex != chainLookup.lookupIndex:
                        self.tagComment('OriginalIndex=%d' % chainLookup.lookup.orgIndex)
                        self.tagLookupListIndex(None, gTable.lookups.index(chainLookup.lookup)) # Get the new lookup indexindex in output
                    self._tagSubstLookupRecord()
            self._tagChainContextSubst()

    def _compileLookupSub7(self, lookupSub, gTable, index):
        # Export the LookupSub7
        extension = lookupSub.extension
        self.tagExtensionSubst(index=index, format=lookupSub.format)
        self.tagExtensionLookupType(extension.type)
        hook = '_compileLookupSub%d' % extension.type
        getattr(self, hook)(extension, gTable) # No index in output of extension lookupSub
        self._tagExtensionSubst()

    #    F E A T U R E  T A L K

    def compile2FeatureScript(self, gsub):
        self.newOutput()
        for feature in gsub.features:
            self._feature2Output(feature)
        return self.getOutput()
