# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     gposcompiler.py
#
#     http://www.microsoft.com/typography/otspec/gpos.htm
#
from copy import copy
from tnbits.compilers.subsetting.states import LookupSub, ChainLookup, \
    GPOSState, Coverage, Value, PairPos, Pair, PairValue,\
    ClassGroup, ClassDef, Anchor
from tnbits.compilers.subsetting.gtablecompiler import GTableCompiler

def tobedeveloped():
    print('TO BE DEVELOPED')
    exit()

class LookupSub1(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 1

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        return len(self.coverage.glyphs) > 0

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        return set(self.coverage.glyphs)

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    def deleteGlyph(self, glyphName):
        while glyphName in self.coverage.glyphs:
            if self.format == 1:
                del self.coverage.glyphs[self.coverage.glyphs.index(glyphName)]
            elif self.format == 2:
                glyphIndex = self.coverage.glyphs.index(glyphName)
                del self.coverage.glyphs[glyphIndex]
                del self.values[glyphIndex]
            else:
                self.error()

    def getFeatureTalk(self, tag, groupSet, indent):
        pass

    def glyphUsage(self, glyphName):
        lookupNames = set(self.getGlyphNames())
        if glyphName in lookupNames:
            return 'LookupSub1=(%s)' % self.value.glyphUsage(glyphName)
        return ''

class LookupSub2(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 2

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        keepIt = False
        if self.format == 1:
            keepCoverage = self.pairPos.coverage.keepIt()
            if len(self.pairPos.pairSet) > 0: # There should be at least one pairSet
                keepIt = True
        elif self.format == 2:
            keepCoverage = self.classGroup.coverage.keepIt()
            if self.classGroup.classDef1.classDefs or self.classGroup.classDef2.classDefs:
                keepIt = True
        else:
            self.error()
        return keepCoverage and keepIt

    def getGlyphNames(self):
        # Answer the list of all glyph names in the lookup. Search format dependent.
        if self.format == 1:
            glyphNames = self.pairPos.coverage.glyphs[:]
            for pair in self.pairPos.pairSet:
                for value in pair.values:
                    glyphNames.append(value.secondGlyph)
        elif self.format == 2:
            glyphNames = self.classGroup.coverage.glyphs[:]
            for glyphName in self.classGroup.classDef1.classDefs.keys():
                glyphNames.append(glyphName)
            for glyphName in self.classGroup.classDef2.classDefs.keys():
                glyphNames.append(glyphName)
        return glyphNames

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    def deleteGlyph(self, glyphName):
        if self.format == 1:
            while glyphName in self.pairPos.coverage.glyphs:
                index = self.pairPos.coverage.glyphs.index(glyphName)
                del self.pairPos.coverage.glyphs[index]
                del self.pairPos.pairSet[index]
            for pairSet in self.pairPos.pairSet:
                pairSet.values = [pairValue for pairValue in pairSet.values if glyphName != pairValue.secondGlyph]
        elif self.format == 2:
            if glyphName in self.classGroup.classDef1.classDefs:
                del self.classGroup.classDef1.classDefs[glyphName]
            if glyphName in self.classGroup.classDef2.classDefs:
                del self.classGroup.classDef2.classDefs[glyphName]
            while glyphName in self.classGroup.coverage.glyphs:
                glyphIndex = self.classGroup.coverage.glyphs.index(glyphName)
                del self.classGroup.coverage.glyphs[glyphIndex]
        else:
            self.error()
    def getFeatureTalk(self, tag, groupSet, indent):
        pass

    def glyphUsage(self, glyphName):
        glyphNames = self.getGlyphNames()
        if glyphName in glyphNames:
            index = glyphNames.index(glyphName)
            if index < len(glyphNames):
                return 'LookupSub2=(%s)' % glyphNames[index]#.glyphUsage(glyphName)
        return ''

class LookupSub3(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 3

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        tobedeveloped

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        tobedeveloped

    def hasGlyph(self, glyphName):
        tobedeveloped

    def deleteGlyph(self, glyphName):
        tobedeveloped

    def getFeatureTalk(self, tag, groupSet, indent):
        tobedeveloped

    def glyphUsage(self, glyphName):
        return 'LookupSub3'

class LookupSub4(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 4

    def keepIt(self):
        # If no more glyphs in self.single, then no reason to keep this lookup.
        # @@@ Can one of them be empty? For now we assume that both need to be filled in order to keep the lookup.
        return (len(self.baseCoverage.glyphs) * len(self.markCoverage.glyphs)) > 0

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        return set(self.baseCoverage.glyphs).union(set(self.markCoverage.glyphs))

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    def deleteGlyph(self, glyphName):
        while glyphName in self.baseCoverage.glyphs:
            index = self.baseCoverage.glyphs.index(glyphName)
            del self.baseCoverage.glyphs[index]
            del self.baseAnchors[index]
        while glyphName in self.markCoverage.glyphs:
            index = self.markCoverage.glyphs.index(glyphName)
            del self.markCoverage.glyphs[index]
            del self.markAnchors[index]
    def getFeatureTalk(self, tag, groupSet, indent):
        pass

    def glyphUsage(self, glyphName):
        baseValues = []
        markValues = []
        baseCoverageGlyphs = self.baseCoverage.glyphs
        markCoverageGlyphs = self.markCoverage.glyphs
        if glyphName in baseCoverageGlyphs:
            index = baseCoverageGlyphs.index(glyphName)
            if index < len(self.baseAnchors):
                for anchor in self.baseAnchors[index]:
                    baseValues.append(anchor.glyphUsage(glyphName))

        baseValues = ','.join(baseValues)
        if baseValues or markCoverageGlyphs:
            return 'LookupSub4=(base:%s mark:%s)' % (baseValues, ','.join(markCoverageGlyphs))
        return ''

class LookupSub5(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 5

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        # @@@ Can one of them be empty? For now we assume that both need to be filled in order to keep the lookup.
        return self.ligatureCoverage.keepIt() and self.markCoverage.keepIt()

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        return set(self.ligatureCoverage.glyphs).union(set(self.markCoverage.glyphs))

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    def deleteGlyph(self, glyphName):
        while glyphName in self.ligatureCoverage.glyphs:
            index = self.ligatureCoverage.glyphs.index(glyphName)
            del self.ligatureCoverage.glyphs[index]
            del self.ligatures[index]
        while glyphName in self.markCoverage.glyphs:
            index = self.markCoverage.glyphs.index(glyphName)
            del self.markCoverage.glyphs[index]
            del self.marks[index]

    def getFeatureTalk(self, tag, groupSet, indent):
        pass

    def glyphUsage(self, glyphName):
        ligatureValues = []
        markValue = ''
        ligatureGlyphs = self.ligatureCoverage.glyphs
        markGlyphs = self.markCoverage.glyphs
        if glyphName in ligatureGlyphs:
            index = ligatureGlyphs.index(glyphName)
            if index < len(self.ligatures):
                for anchorSet in self.ligatures[index]:
                    for anchor in anchorSet:
                        ligatureValues.append(anchor.glyphUsage(glyphName))
        if glyphName in markGlyphs:
            index = markGlyphs.index(glyphName)
            if index < len(self.marks):
                markValue = self.marks[index].glyphUsage(glyphName)
        ligatureValues = ' '.join(ligatureValues)
        if ligatureValues or markValue:
            return 'LookupSub5=(ligature:%s mark:%s)' % (ligatureValues, markValue)
        return ''

class LookupSub6(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 6

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        # @@@ Can one of them be empty? For now we assume that both need to be filled in order to keep the lookup.
        return self.mark1Coverage.keepIt() and self.mark2Coverage.keepIt()

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        return set(self.mark1Coverage.glyphs).union(set(self.mark2Coverage.glyphs))

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    def deleteGlyph(self, glyphName):
        if glyphName in self.mark1Coverage.glyphs:
            del self.mark1Coverage.glyphs[self.mark1Coverage.glyphs.index(glyphName)]
        if glyphName in self.mark2Coverage.glyphs:
            del self.mark2Coverage.glyphs[self.mark2Coverage.glyphs.index(glyphName)]

    def getFeatureTalk(self, tag, groupSet, indent):
        tobedeveloped

    def glyphUsage(self, glyphName):
        mark1Value = mark2Value = ''
        mark1Glyphs = self.mark1Coverage.glyphs
        mark2Glyphs = self.mark2Coverage.glyphs
        if glyphName in mark1Glyphs:
            index = mark1Glyphs.index(glyphName)
            if index < len(self.marks1):
                mark1Value = '%s(%s)->%s' % (glyphName, self.marks1[index].glyphUsage(glyphName), ','.join(mark2Glyphs))
        if glyphName in mark2Glyphs:
            index = mark2Glyphs.index(glyphName)
            if index < len(self.marks2):
                values = []
                for anchor in self.marks2[index]:
                    values.append(anchor.glyphUsage(glyphName))
                mark2Value = '%s(%s)->%s' % (glyphName, ' '.join(values), ','.join(mark1Glyphs))
        if mark1Value or mark2Value:
            return 'LookupSub6=(mark1:%s,mark2:%s)' % (mark1Value, mark2Value)
        return ''

class LookupSub7(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 7

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        self.tobedeveloped()

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        self.tobedeveloped()

    def hasGlyph(self, glyphName):
        self.tobedeveloped()

    def deleteGlyph(self, glyphName):
        self.tobedeveloped()

    def getFeatureTalk(self, tag, groupSet, indent):
        self.tobedeveloped()

    def glyphUsage(self, glyphName):
        return 'LookupSub7'

class LookupSub8(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 8

    # self.pos

    def _get_pos(self):
        # API to self._pos attribute. We need this to dynamically omit the chainLookups that
        # became obsolete (referring to a dead lookup), which present themselves as None in the chainLookup.lookup.
        # Beware that the answered list is constructed. Is it not the real self._pos.
        # For changes, the entire list needs to be replaced by self.pos = newPos
        if not hasattr(self, '_pos'):
            self._pos = []
        pos = []
        for chainLookup in self._pos:
            if chainLookup.lookup is not None: # Is it still valid, then answer it
                pos.append(chainLookup)
        return tuple(pos) # Make read-only, just to be sure called won't make changes.

    def _set_pos(self, pos):
        # API to self._pos attribute
        self._pos = []
        for chainLookup in pos:
            self.addPos(chainLookup)

    pos = property(_get_pos, _set_pos)

    def addPos(self, chainLookup):
        assert isinstance(chainLookup, ChainLookup)
        self._pos.append(chainLookup)

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        # There should at least be one inputCoverage with at least one glyph
        # and there should at least be a glyph in the backtrackCoverage or
        # lookaheadCoverage.
        inputKeepIt = False
        for coverage in self.inputCoverage:
            if coverage.keepIt():
                inputKeepIt = True
                break
        backtrackKeepIt = False
        for coverage in self.backtrackCoverage:
            if coverage.keepIt():
                backtrackKeepIt = True
                break
        lookAheadKeepIt = False
        for coverage in self.lookAheadCoverage:
            if coverage.keepIt():
                lookAheadKeepIt = True
                break
        # Check if there is at least one lookup referencing to self that needs to be kept
        # @@@ There is currently no check on circle referencing lookups. Is that allowed?
        # @@@ Or is it likely to happen? Is it a way to crash render engines?
        referencedKeepIt = True # In case there is no lookup reference.
        pos = self.pos
        if pos:
            referencedKeepIt = False
            for chainLookup in pos:
                if chainLookup.lookup is not None and chainLookup.keepIt():
                    referencedKeepIt = True
                    break
        return inputKeepIt and (backtrackKeepIt or lookAheadKeepIt or referencedKeepIt)

    def getGlyphNames(self):
        # Answer the set of all glyph names in the lookup.
        glyphNames = set()
        for coverage in self.backtrackCoverage:
            glyphNames = glyphNames.union(set(coverage.glyphs))
        for coverage in self.inputCoverage:
            glyphNames = glyphNames.union(set(coverage.glyphs))
        for coverage in self.lookAheadCoverage:
            glyphNames = glyphNames.union(set(coverage.glyphs))
        # Just to be sure we get them all, add the glyphs of any referenced lookup too
        for pos in self.pos:
            if pos.lookup is not None: # There is an existing referefnced lookup on the other side
                glyphNames = glyphNames.union(set(pos.lookup.getGlyphNames()))
        return glyphNames

    def hasGlyph(self, glyphName):
        return glyphName in self.getGlyphNames()

    def deleteGlyph(self, glyphName):
        for coverage in self.backtrackCoverage:
            if glyphName in coverage.glyphs:
                del coverage.glyphs[coverage.glyphs.index(glyphName)]
        for coverage in self.inputCoverage:
            if glyphName in coverage.glyphs:
                del coverage.glyphs[coverage.glyphs.index(glyphName)]
        for coverage in self.lookAheadCoverage:
            if glyphName in coverage.glyphs:
                del coverage.glyphs[coverage.glyphs.index(glyphName)]
        for pos in self.pos: # These must be all valid lookups.
            pos.lookup.deleteGlyph(glyphName)

    def getFeatureTalk(self, tag, groupSet, indent):
        self.tobedeveloped()

    def attachIndexReferencedLookup(self, parent, lookups):
        # If this is a lookup type 8 and 9, then there may be substitution
        # references to other lookups. Fill them in with the real
        # links if they are present.
        # As now there is a direct link, the index numbers become obsolete.
        # Editing the lookups may cause them to have different index
        # numbers on output.
        # Perform directly on the chainLookups in self._pos, we don't want
        # a filtered list here.
        for pos in self._pos:
            pos.lookup = lookups[pos.lookupIndex] # Set as weakref in the pos chainLookup
            pos.lookup.attachReferencingLookup(parent) # Attach in reverse direction too for the parent of self

    def updateLookupIndices(self, lookups):
        # If the lookups are added or deleted, then the current index numbers
        # of referenced lookups may no longer be valid. Use the current lookup
        # (if there is an existing reference) to get it's index in the lookup
        # table, and store it in the index field.
        for pos in self.pos:
            assert pos.lookup in lookups # Just to make sure that the lookup is there.
            pos.index = lookups.index(pos.lookup) # Store index of the referenced lookup

    def glyphUsage(self, glyphName):
        usages = []
        for chainLookup in self.pos:
            usages.append(chainLookup.glyphUsage(glyphName))
        if usages:
            return 'LookupSub8=(%s)' % ' '.join(usages)
        return ''

class LookupSub9(LookupSub):
    # Inheriting lookups for each type, so we can intelligent for each type.
    type = 9

    def keepIt(self):
        # If not more glyphs in self.single, then no reason to keep this lookup.
        return self.extension.keepIt()

    def getGlyphNames(self):
        # Answer the set of all glyph names in the self.extSubTable.
        return self.extension.getGlyphNames()

    def hasGlyph(self, glyphName):
        self.extension.hasGlyph(glyphName)

    def deleteGlyph(self, glyphName):
        # Delete the glyph names glyphName anywhere it exists in self.extSubTable
        self.extension.deleteGlyph(glyphName)

    def getFeatureTalk(self, tag, groupSet, indent):
        return self.extension.getFeatureTalk(tag, groupSet, indent)

    def attachIndexReferencedLookup(self, parent, lookups):
        # If this is a lookup type 8 and 9, then there may be substitution
        # references to other lookups. Fill them in with the real
        # links if they are present. For other types this call is ignored.
        # The call is ignored by the other lookup types.
        self.extension.attachIndexReferencedLookup(parent, lookups)

    def updateLookupIndices(self, lookups):
        self.extension.updateLookupIndices(lookups)

    def glyphUsage(self, glyphName):
        return self.extension.glyphUsage(glyphName)

class GPOSCompiler(GTableCompiler):

    TABLE_TAG = 'GPOS'

    def newState(self):
        return GPOSState()

    def _decompileLookupSub1(self, gLookupSub, gTable):
        # Single Adjustment Positioning Subtablex
        # A single adjustment positioning subtable (SinglePos) is used to adjust the position
        # of a single glyph, such as a subscript or superscript. In addition, a SinglePos subtable
        # is commonly used to implement lookup data for contextual positioning.
        # A SinglePos subtable will have one of two formats: one that applies the same adjustment to a
        # series of glyphs, or one that applies a different adjustment for each unique glyph.
        lookupSub = LookupSub1()
        lookupSub.valueFormat = gLookupSub.ValueFormat
        lookupSub.format = gLookupSub.Format
        lookupSub.coverage = Coverage(copy(gLookupSub.Coverage.glyphs), gLookupSub.Coverage.Format)
        if lookupSub.format == 1:
            gValue = gLookupSub.Value
            lookupSub.value = Value(gValue, lookupSub.valueFormat)
        else: # lookup.format == 2
            lookupSub.values = values = []
            for gValue in gLookupSub.Value:
                lookupSub.values.append(Value(gValue, lookupSub.valueFormat))
        return lookupSub

    def _decompileLookupSub2(self, gLookupSub, gTable):
        # Pair Adjustment Positioning Subtable
        # A pair adjustment positioning subtable (PairPos) is used to adjust the positions of two glyphs
        # in relation to one another-for instance, to specify kerning data for pairs of glyphs.
        # Compared to a typical kerning table, however, a PairPos subtable offers more flexiblity
        # and precise control over glyph positioning. The PairPos subtable can adjust each glyph
        # in a pair independently in both the X and Y directions, and it can explicitly describe
        # the particular type of adjustment applied to each glyph. In addition, a PairPos subtable
        # can use Device tables to subtly adjust glyph positions at each font size and device resolution.
        # PairPos subtables can be either of two formats: one that identifies glyphs individually by
        # index (Format 1), or one that identifies glyphs by class (Format 2).
        lookupSub = LookupSub2()
        lookupSub.format = gLookupSub.Format
        if lookupSub.format == 1:
            lookupSub.pairPos = pairPos = PairPos(gLookupSub.LookupType, gLookupSub.Format)
            pairPos.valueFormat1 = gLookupSub.ValueFormat1
            pairPos.valueFormat2 = gLookupSub.ValueFormat2
            pairPos.coverage = Coverage(copy(gLookupSub.Coverage.glyphs), gLookupSub.Coverage.Format)
            pairPos.pairSet = pairSet = []
            for gTablePair in gLookupSub.PairSet:
                pair = Pair()
                pairSet.append(pair)
                pair.values = []
                for gTablePairValue in gTablePair.PairValueRecord:
                    pairValue = PairValue(gTablePairValue.SecondGlyph, gTablePairValue.Value1, gTablePairValue.Value2)
                    pair.values.append(pairValue)

        elif lookupSub.format == 2:
            lookupSub.classGroup = classGroup = ClassGroup(gLookupSub.LookupType, gLookupSub.Format)
            classGroup.valueFormat1 = gLookupSub.ValueFormat1
            classGroup.valueFormat2 = gLookupSub.ValueFormat2
            classGroup.coverage = Coverage(copy(gLookupSub.Coverage.glyphs), gLookupSub.Coverage.Format)
            classGroup.class1Records = class1Records = []
            for gClass1Rec in gLookupSub.Class1Record:
                class2Records = []
                class1Records.append(class2Records)
                for gClass2Rec in gClass1Rec.Class2Record:
                    classValue1 = Value(gClass2Rec.Value1, gLookupSub.ValueFormat1)
                    classValue2 = Value(gClass2Rec.Value2, gLookupSub.ValueFormat2)
                    class2Records.append((classValue1, classValue2))
            classGroup.classDef1 = ClassDef(gLookupSub.ClassDef1.Format)
            classGroup.classDef1.classDefs = copy(gLookupSub.ClassDef1.classDefs) # Copy glyph dictionary
            classGroup.classDef2 = ClassDef(gLookupSub.ClassDef2.Format)
            classGroup.classDef2.classDefs = copy(gLookupSub.ClassDef2.classDefs) # Copy glyph dictionary
        else:
            self.error()
        return lookupSub

    def _decompileLookupSub3(self, gLookupSub, gTable):
        # Cursive Attachment Positioning Subtable
        # Some cursive fonts are designed so that adjacent glyphs join when rendered with their default
        # positioning. However, if positioning adjustments are needed to join the glyphs, a cursive
        # attachment positioning (CursivePos) subtable can describe how to connect the glyphs by aligning
        # two anchor points: the designated exit point of a glyph, and the designated entry point of the
        # following glyph.
        lookupSub = LookupSub3()
        lookupSub.format = gLookupSub.Format
        self.tobedeveloped()
        return lookupSub

    def _decompileLookupSub4(self, gLookupSub, gTable):
        # MarkToBase Attachment Positioning Subtable
        # The MarkToBase attachment (MarkBasePos) subtable is used to position combining mark glyphs
        # with respect to base glyphs. For example, the Arabic, Hebrew, and Thai scripts combine
        # vowels, diacritical marks, and tone marks with base glyphs.
        # In the MarkBasePos subtable, every mark glyph has an anchor point and is associated with a
        # class of marks. Each base glyph then defines an anchor point for each class of marks it uses.
        lookupSub = LookupSub4()
        lookupSub.format = gLookupSub.Format
        lookupSub.baseAnchors = anchors = []
        for baseRec in gLookupSub.BaseArray.BaseRecord:
            baseAnchors = []
            anchors.append(baseAnchors)
            for anchorRec in baseRec.BaseAnchor:
                try:
                    baseAnchors.append(Anchor(anchorRec.XCoordinate, anchorRec.YCoordinate, anchorRec.Format))
                except:
                    print('Skipping invalid anchor')

        lookupSub.baseCoverage = Coverage(copy(gLookupSub.BaseCoverage.glyphs), gLookupSub.BaseCoverage.Format)

        lookupSub.markAnchors = anchors = []
        for markRec in gLookupSub.MarkArray.MarkRecord:
            anchors.append(Anchor(markRec.MarkAnchor.XCoordinate, markRec.MarkAnchor.YCoordinate, markRec.MarkAnchor.Format, markRec.Class))
        lookupSub.markCoverage = Coverage(copy(gLookupSub.MarkCoverage.glyphs), gLookupSub.MarkCoverage.Format)
        return lookupSub

    def _decompileLookupSub5(self, gLookupSub, gTable):
        # MarkToLigature Attachment Positioning Subtable
        # The MarkToLigature attachment (MarkLigPos) subtable is used to position combining mark
        # glyphs with respect to ligature base glyphs. With MarkToBase attachment, described previously,
        # a single base glyph defines an attachment point for each class of marks. In contrast,
        # MarkToLigature attachment describes ligature glyphs composed of several components that
        # can each define an attachment point for each class of marks.
        lookupSub = LookupSub5()
        lookupSub.format = gLookupSub.Format
        lookupSub.ligatures = ligatures = []
        for ligatureAttach in gLookupSub.LigatureArray.LigatureAttach:
            components = []
            ligatures.append(components)
            for componentRec in ligatureAttach.ComponentRecord:
                anchors = []
                components.append(anchors)
                for ligatureAnchorRec in componentRec.LigatureAnchor:
                    anchor = Anchor(ligatureAnchorRec.XCoordinate, ligatureAnchorRec.YCoordinate, ligatureAnchorRec.Format)
                    anchors.append(anchor)
        lookupSub.ligatureCoverage = Coverage(copy(gLookupSub.LigatureCoverage.glyphs), gLookupSub.LigatureCoverage.Format)
        lookupSub.marks = marks = []
        for markRec in gLookupSub.MarkArray.MarkRecord:
            anchor = Anchor(markRec.MarkAnchor.XCoordinate, markRec.MarkAnchor.YCoordinate, markRec.MarkAnchor.Format, markRec.Class)
            marks.append(anchor)
        lookupSub.markCoverage = Coverage(copy(gLookupSub.MarkCoverage.glyphs), gLookupSub.MarkCoverage.Format)
        return lookupSub

    def _decompileLookupSub6(self, gLookupSub, gTable):
        # MarkToMark Attachment Positioning Subtable
        # The MarkToMark attachment (MarkMarkPos) subtable is identical in form to the MarkToBase
        # attachment subtable, although its function is different. MarkToMark attachment defines
        # the position of one mark relative to another mark as when, for example, positioning
        # tone marks with respect to vowel diacritical marks in Vietnamese.
        lookupSub = LookupSub6()
        lookupSub.format = gLookupSub.Format
        lookupSub.marks1 = marks = []
        for markAnchor in gLookupSub.Mark1Array.MarkRecord:
            marks.append(Anchor(markAnchor.MarkAnchor.XCoordinate, markAnchor.MarkAnchor.YCoordinate, markAnchor.MarkAnchor.Format, markAnchor.Class))
        lookupSub.mark1Coverage = Coverage(copy(gLookupSub.Mark1Coverage.glyphs), gLookupSub.Mark1Coverage.Format)
        lookupSub.marks2 = marks = []
        for markRecs in gLookupSub.Mark2Array.Mark2Record:
            mark2Anchors = []
            marks.append(mark2Anchors)
            for mark2Rec in markRecs.Mark2Anchor:
                if mark2Rec.Format == 1:
                    mark2Anchors.append(Anchor(mark2Rec.XCoordinate, mark2Rec.YCoordinate, mark2Rec.Format))
                elif mark2Rec.Format == 2:
                    self.tobedeveloped()
                elif mark2Rec.Format == 3:
                    anchor = Anchor(mark2Rec.XCoordinate, mark2Rec.YCoordinate, mark2Rec.Format)
                    anchor.deltaFormat = mark2Rec.XDeviceTable.DeltaFormat
                    anchor.deltaValue = mark2Rec.XDeviceTable.DeltaValue
                    anchor.startSize = mark2Rec.XDeviceTable.StartSize
                    anchor.endSize = mark2Rec.XDeviceTable.EndSize
                    mark2Anchors.append(anchor)
                else:
                    self.tobedeveloped()
        lookupSub.mark2Coverage = Coverage(copy(gLookupSub.Mark2Coverage.glyphs), gLookupSub.Mark2Coverage.Format)
        return lookupSub

    def _decompileLookupSub7(self, gLookupSub, gTable):
        # Contextual Positioning Subtables
        # A Contextual Positioning (ContextPos) subtable defines the most powerful type of glyph
        # positioning lookup. It describes glyph positioning in context so a text-processing
        # client can adjust the position of one or more glyphs within a certain pattern of glyphs.
        # Each subtable describes one or more “input” glyph sequences and one or more positioning
        # operations to be performed on that sequence.
        lookupSub = LookupSub7()
        lookupSub.format = gLookupSub.Format
        self.tobedeveloped()
        return lookupSub

    def _decompileLookupSub8(self, gLookupSub, gTable):
        # LookupType 8: Chaining Contextual Positioning Subtable
        # A Chaining Contextual Positioning subtable(ChainContextPos)describes glyph positioning
        # in context with an ability to look back and/or look ahead in the sequence of glyphs.
        # The design of the Chaining Contextual Positioning subtable is parallel to that of
        # the Contextual Positioning subtable, including the availability of three formats.
        lookupSub = LookupSub8()
        lookupSub.format = gLookupSub.Format

        lookupSub.backtrackCoverage = []
        for backtrackCoverage in gLookupSub.BacktrackCoverage:
            lookupSub.backtrackCoverage.append(Coverage(copy(backtrackCoverage.glyphs), backtrackCoverage.Format))
        lookupSub.inputCoverage = []
        for inputCoverage in gLookupSub.InputCoverage:
            lookupSub.inputCoverage.append(Coverage(copy(inputCoverage.glyphs), inputCoverage.Format))
        lookupSub.lookAheadCoverage = []
        for lookAheadCoverage in gLookupSub.LookAheadCoverage:
            lookupSub.lookAheadCoverage.append(Coverage(copy(lookAheadCoverage.glyphs), lookAheadCoverage.Format))
        lookupSub.pos = []
        for posLookupRecord in gLookupSub.PosLookupRecord:
            # Just store index for now.
            # Later make a direct link to this record in one direction and a weakref on the other direction
            posLookup = ChainLookup(posLookupRecord.LookupListIndex, posLookupRecord.SequenceIndex)
            lookupSub.addPos(posLookup) # Add this way, as lookupSub.pos is read only due to weakref conversion.
        return lookupSub

    def _decompileLookupSub9(self, gLookupSub, gTable):
        # Extension Positioning
        # This lookup provides a mechanism whereby any other lookup type's subtables are stored
        # at a 32-bit offset location in the 'GPOS' table. This is needed if the total size of the
        # subtables exceeds the 16-bit limits of the various other offsets in the 'GPOS' table.
        # In this specification, the subtable stored at the 32-bit offset location is termed
        # the “extension” subtable.
        lookupSub = LookupSub9()
        lookupSub.format = gLookupSub.Format
        lookupSub.extensionLookupType = gLookupSub.ExtensionLookupType
        # Dispatch the lookup type on 2nd level.
        hook = '_decompileLookupSub%d' % gLookupSub.ExtSubTable.LookupType
        lookupSub.extension = getattr(self, hook)(gLookupSub.ExtSubTable, gTable)
        return lookupSub

    #    C O M P I L E  2  T T X / X M L

    def compileLookups2XML(self, gpos):
        # Compile the lookups to TTX/XML
        self.tagLookupList()
        for lookupIndex, lookup in enumerate(gpos.lookups):
            if lookupIndex != lookup.orgIndex:
                self.tagComment('OriginalIndex=%d' % lookup.orgIndex)
            self.tagLookup(lookupIndex)
            self.tagLookupType(lookup.type)
            self.tagLookupFlag(lookup.flag)
            self.tagComment('SubTableCount=%s' % len(lookup.subs))
            for subIndex, lookupSub in enumerate(lookup.subs):
                hook = '_compileLookupSub%d' % lookup.type
                getattr(self, hook)(lookupSub, gpos, subIndex)
            self._tagLookup()
        self._tagLookupList()

    def _compileLookupSub1(self, lookupSub, gposLookups, index=None):
        self.tagSinglePos(index=index, format=lookupSub.format)
        self.tagCoverage(lookupSub.coverage.format)
        for glyphName in lookupSub.coverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagCoverage()
        self.tagValueFormat(lookupSub.valueFormat)
        if lookupSub.format == 1:
            self.tagValue(lookupSub.value)
        else: # lookup.format == 2
            for value in lookupSub.values:
                self.tagValue(value)
        self._tagSinglePos()

    def _compileLookupSub2(self, lookupSub, gposLookups, index=None):
        self.tagPairPos(index=index, format=lookupSub.format)
        if lookupSub.format == 1:
            self.tagCoverage(lookupSub.pairPos.coverage.format)
            for glyphName in lookupSub.pairPos.coverage.glyphs:
                self.tagGlyph(glyphName)
            self._tagCoverage()
            self.tagValueFormat(lookupSub.pairPos.valueFormat1, 1)
            self.tagValueFormat(lookupSub.pairPos.valueFormat2, 2)
            self.tagComment('PairSetCount=%d' % len(lookupSub.pairPos.pairSet))
            for pairSetIndex, pairSet in enumerate(lookupSub.pairPos.pairSet):
                self.tagPairSet(pairSetIndex)
                self.tagComment('PairValueCount=%s' % len(pairSet.values))
                for valueIndex, pairValueRecord in enumerate(pairSet.values):
                    self.tagPairValueRecord(valueIndex)
                    self.tagSecondGlyph(pairValueRecord.secondGlyph)
                    self.tagValue(pairValueRecord.value1, 1)
                    self.tagValue(pairValueRecord.value2, 2)
                    self._tagPairValueRecord()
                self._tagPairSet()
        else: # lookupformat == 2
            self.tagCoverage(lookupSub.classGroup.coverage.format)
            for glyphName in lookupSub.classGroup.coverage.glyphs:
                self.tagGlyph(glyphName)
            self._tagCoverage()
            self.tagValueFormat(lookupSub.classGroup.valueFormat1, 1)
            self.tagValueFormat(lookupSub.classGroup.valueFormat2, 2)
            self.tagClassDefN(lookupSub.classGroup.classDef1.format, 1)
            for glyphName, classDef in lookupSub.classGroup.classDef1.classDefs.items():
                self.tagClassDef(glyphName=glyphName, classDef=classDef)
            self._tagClassDefN(1)
            self.tagClassDefN(lookupSub.classGroup.classDef2.format, 2)
            for glyphName, classDef in lookupSub.classGroup.classDef2.classDefs.items():
                self.tagClassDef(glyphName=glyphName, classDef=classDef)
            self._tagClassDefN(2)
            self.tagComment('Class1Count=%d' % len(lookupSub.classGroup.class1Records))
            for index1, class2Records in enumerate(lookupSub.classGroup.class1Records):
                self.tagComment('Class2Count=%d' % len(class2Records))
                self.tagClassNRecord(index1, 1)
                for index2, (value1, value2) in enumerate(class2Records):
                    self.tagClassNRecord(index2, 2)
                    self.tagValue(value1, 1)
                    self.tagValue(value2, 2)
                    self._tagClassNRecord(2)
                self._tagClassNRecord(1)
        self._tagPairPos()

    def _compileLookupSub3(self, lookup, gposLookups, index=None):
        self.tagPairPos(index=index, format=lookup.format)
        self.tobedeveloped()
        #self.write('<!-- XXXXX 3 XXXXXX -->\n')
        self._tagPairPos()

    def _compileLookupSub4(self, lookupSub, gposLookups, index=None):
        self.tagMarkBasePos(index=index, format=lookupSub.format)
        self.tagMarkCoverage(lookupSub.markCoverage.format)
        for glyphName in lookupSub.markCoverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagMarkCoverage()
        self.tagBaseCoverage(lookupSub.baseCoverage.format)
        for glyphName in lookupSub.baseCoverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagBaseCoverage()
        self.tagMarkArray()
        self.tagComment('MarkCount=%d' % len(lookupSub.markAnchors))
        for markIndex, markAnchor in enumerate(lookupSub.markAnchors):
            self.tagMarkRecord(markIndex)
            self.tagClass(markAnchor.class_)
            self.tagMarkAnchor(markAnchor.format)
            self.tagXCoordinate(markAnchor.x)
            self.tagYCoordinate(markAnchor.y)
            self._tagMarkAnchor()
            self._tagMarkRecord()
        self._tagMarkArray()
        self.tagBaseArray()
        self.tagComment('BaseCount=%d' % len(lookupSub.markAnchors))
        for baseIndex, baseRecord in enumerate(lookupSub.baseAnchors):
            self.tagBaseRecord(baseIndex)
            for anchorIndex, baseAnchor in enumerate(baseRecord):
                self.tagBaseAnchor(anchorIndex, baseAnchor.format)
                self.tagXCoordinate(baseAnchor.x)
                self.tagYCoordinate(baseAnchor.y)
                self._tagBaseAnchor()
            self._tagBaseRecord()
        self._tagBaseArray()
        self._tagMarkBasePos()

    def _compileLookupSub5(self, lookupSub, gposLookups, index=None):
        self.tagMarkLigPos(lookupSub.format)
        self.tagMarkCoverage(lookupSub.markCoverage.format)
        for glyphName in lookupSub.markCoverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagMarkCoverage()
        self.tagLigatureCoverage(lookupSub.ligatureCoverage.format)
        for glyphName in lookupSub.ligatureCoverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagLigatureCoverage()
        self.tagMarkArray()
        self.tagComment('MarkCount=%d' % len(lookupSub.marks))
        for index, mark in enumerate(lookupSub.marks):
            self.tagMarkRecord(index)
            self.tagClass(mark.class_)
            self.tagMarkAnchor(mark.format)
            self.tagXCoordinate(mark.x)
            self.tagYCoordinate(mark.y)
            self._tagMarkAnchor()
            self._tagMarkRecord()
        self._tagMarkArray()
        self.tagLigatureArray()
        self.tagComment('LigatureCount=%d' % len(lookupSub.ligatures))
        for ligatureIndex, ligature in enumerate(lookupSub.ligatures):
            self.tagLigatureAttach(ligatureIndex)
            self.tagComment('ComponentCount=%d' % len(ligature))
            for componentIndex, anchors in enumerate(ligature):
                self.tagComponentRecord(componentIndex)
                for anchorIndex, anchor in enumerate(anchors):
                    self.tagLigatureAnchor(anchorIndex, anchor.format)
                    self.tagXCoordinate(anchor.x)
                    self.tagYCoordinate(anchor.y)
                    self._tagLigatureAnchor()
                self._tagComponentRecord()
            self._tagLigatureAttach()
        self._tagLigatureArray()
        self._tagMarkLigPos()

    def _compileLookupSub6(self, lookupSub, gposLookups, index=None):
        self.tagMarkMarkPos(index=index, format=lookupSub.format)
        self.tagMarkNCoverage(lookupSub.mark1Coverage.format, 1)
        for glyphName in lookupSub.mark1Coverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagMarkNCoverage(1)
        self.tagMarkNCoverage(lookupSub.mark2Coverage.format, 2)
        for glyphName in lookupSub.mark2Coverage.glyphs:
            self.tagGlyph(glyphName)
        self._tagMarkNCoverage(2)
        self.tagComment('ClassCount=%d' % 1) # ??????
        self.tagMarkNArray(1)
        self.tagComment('MarkCount=%d' % len(lookupSub.marks1))
        for index, anchor in enumerate(lookupSub.marks1):
            self.tagMarkRecord(index)
            self.tagClass(anchor.class_)
            self.tagMarkAnchor(anchor.format)
            if anchor.format == 1:
                self.tagXCoordinate(anchor.x)
                self.tagYCoordinate(anchor.y)
            elif anchor.format == 2:
                tobedeveloped()
            elif anchor.format == 3:
                self.tagXCoordinate(anchor.x)
                self.tagYCoordinate(anchor.y)
            else:
                tobedeveloped()
            self._tagMarkAnchor()
            self._tagMarkRecord()
        self._tagMarkNArray(1)
        self.tagComment('Mark2Count=%d' % len(lookupSub.marks2))
        self.tagMarkNArray(2)
        for index, markRecords in enumerate(lookupSub.marks2):
            self.tagMark2Record(index)
            for _, anchor in enumerate(markRecords): # anchorIndex, anchor
                self.tagMark2Anchor(index=index, format=anchor.format)
                if anchor.format == 1:
                    self.tagXCoordinate(anchor.x)
                    self.tagYCoordinate(anchor.y)
                elif anchor.format == 2:
                    tobedeveloped()
                elif anchor.format == 3:
                    self.tagXCoordinate(anchor.x)
                    self.tagYCoordinate(anchor.y)
                    self.tagXDeviceTable()
                    self.tagStartSize(anchor.startSize)
                    self.tagEndSize(anchor.endSize)
                    self.tagDeltaFormat(anchor.deltaFormat)
                    self.tagDeltaValue(anchor.deltaValue)
                    self._tagXDeviceTable()
                else:
                    tobedeveloped()
                self._tagMark2Anchor()
            self._tagMark2Record()
        self._tagMarkNArray(2)
        self._tagMarkMarkPos()

    def _compileLookupSub7(self, lookupSub, gposLookups, index=None):
        self.tobedeveloped()
        #self.write('<!-- XXXXX 7 XXXXXX -->\n')

    def _compileLookupSub8(self, lookupSub, gposLookups, index=None):
        self.tagChainContextPos(index=index, format=lookupSub.format)
        self.tagComment('BacktrackGlyphCount=%d' % len(lookupSub.backtrackCoverage))
        for coverageIndex, coverage in enumerate(lookupSub.backtrackCoverage):
            self.tagBacktrackCoverage(index=coverageIndex, format=coverage.format)
            for glyphName in coverage.glyphs:
                self.tagGlyph(glyphName)
            self._tagBacktrackCoverage()
        self.tagComment('InputGlyphCount=%d' % len(lookupSub.inputCoverage))
        for coverageIndex, coverage in enumerate(lookupSub.inputCoverage):
            self.tagInputCoverage(index=coverageIndex, format=coverage.format)
            for glyphName in coverage.glyphs:
                self.tagGlyph(glyphName)
            self._tagInputCoverage()
        self.tagComment('LookAheadGlyphCount=%d' % len(lookupSub.lookAheadCoverage))
        for coverageIndex, coverage in enumerate(lookupSub.lookAheadCoverage):
            self.tagLookAheadCoverage(index=coverageIndex, format=coverage.format)
            for glyphName in coverage.glyphs:
                self.tagGlyph(glyphName)
            self._tagLookAheadCoverage()
        self.tagComment('PosCount=%d' % len(lookupSub.pos))
        for posIndex, posLookup in enumerate(lookupSub.pos):
            self.tagPosLookupRecord(posIndex)
            self.tagSequenceIndex(posLookup.sequenceIndex)
            if posLookup.lookup is not None:
                lookupIndex = gposLookups.getIndexOfLookup(posLookup.lookup)
                if posLookup.lookup.orgIndex != lookupIndex:
                    self.tagComment('OriginalIndex=%d' % posLookup.lookup.orgIndex)
                self.tagLookupListIndex(None, lookupIndex)
            else:
                self.tagComment('###### Error with lookup?')
            self._tagPosLookupRecord()
        self._tagChainContextPos()

    def _compileLookupSub9(self, lookupSub, gposLookups, index):
        # Export the LookupSub9
        extension = lookupSub.extension
        self.tagExtensionPos(index=index, format=lookupSub.format)
        self.tagExtensionLookupType(extension.type)
        hook = '_compileLookupSub%d' % extension.type
        getattr(self, hook)(extension, gposLookups)
        self._tagExtensionPos()

