from StringIO import StringIO


def _kernSorter(pair):
    isClass1 = isClass2 = False
    g1, g2 = pair
    if g1[0] == "@":
        isClass1 = True
        g1 = g1[1:]
    if g2[0] == "@":
        isClass2 = True
        g2 = g2[1:]
    return (not isClass1, not isClass2, g1, g2)


def writeKernFeature(kerning, groups):
    """
        >>> kerning = {("T", "o"): 10, ("T", "H"): 20}
        >>> print(writeKernFeature(kerning, {})).strip()
        feature kern {
          pos T H 20;
          pos T o 10;
        } kern;
        >>> groups = {"@A": ["A", "B"]}
        >>> kerning = {("T", "o"): 10, ("A", "H"): 20, ("@A", "o"): 5, ("@Z", "@Y"): -10, ("T", "@G"): 4}
        >>> print(writeKernFeature(kerning, groups)).strip()
        @A = [A B];
        <BLANKLINE>
        feature kern {
          pos @Z @Y -10;
          pos @A o 5;
          pos T @G 4;
          pos A H 20;
          pos T o 10;
        } kern;
    """
    ff = StringIO()
    if groups:
        for groupName in sorted(groups):
            assert groupName[0] == "@"
            ff.write("%s = [%s];\n" % (groupName, " ".join(groups[groupName])))
        ff.write("\n")
    ff.write("feature kern {\n")
    for g1, g2 in sorted(kerning, key=_kernSorter):
        value = kerning[g1, g2]
        ff.write("  pos %s %s %s;\n" % (g1, g2, value))
    ff.write("} kern;\n\n")
    return ff.getvalue()


def _sortValues(d):
    for k, v in d.items():
        d[k] = tuple(sorted(v))


def _makeProfiles(kerning):
    # kerning must be flat!
    profiles1 = {}
    profiles2 = {}
    for (first, second), value in kerning.items():
        if first not in profiles1:
            profiles1[first] = set()
        profiles1[first].add((second, value))   # (oppositeGlyph, kernValue)
        if second not in profiles2:
            profiles2[second] = set()
        profiles2[second].add((first, value))  # (oppositeGlyph, kernValue)
    _sortValues(profiles1)
    _sortValues(profiles2)
    return profiles1, profiles2


def _makeGroupsFromProfiles(profiles):
    groups = {}
    for k, v in profiles.items():
        if v not in groups:
            groups[v] = set()
        assert k not in groups[v]
        groups[v].add(k)
    _sortValues(groups)
    return sorted(groups.values())


def _makeGroupNames(groups, prefix):
    """Make group names from a prefix and the first glyph name in the group.
    or the sole glyph name itself if there is only one."""
    byName = {}
    byGroup = {}
    for group in groups:
        if len(group) == 1:
            name = group[0]
        else:
            name = prefix + group[0]
            byName[name] = group
        byGroup[group] = name
    return byName, byGroup


def _makeNewKerningFromProfiles(profiles1, profiles2, flatKerning, prefix1, prefix2):
    groups1 = _makeGroupsFromProfiles(profiles1)
    groups2 = _makeGroupsFromProfiles(profiles2)

    byName1, byGroup1 = _makeGroupNames(groups1, prefix1)
    byName2, byGroup2 = _makeGroupNames(groups2, prefix2)

    newKerning = {}
    for g1 in groups1:
        for g2 in groups2:
            testPair = g1[0], g2[0]
            if testPair in flatKerning:
                value = flatKerning[testPair]
                pair = byGroup1[g1], byGroup2[g2]
                if pair in newKerning:
                    assert newKerning[pair] == value
                else:
                    newKerning[pair] = value

    return newKerning, byName1, byName2


def regroupKerning(flatKerning, prefix1="@FIRST_", prefix2="@SECOND_"):
    profiles1, profiles2 = _makeProfiles(flatKerning)
    newKerning, groups1, groups2 = _makeNewKerningFromProfiles(profiles1, profiles2, flatKerning, prefix1, prefix2)
    groups = {}
    groups.update(groups1)
    groups.update(groups2)
    assert len(groups) == len(groups1) + len(groups2)
    return newKerning, groups


def _getKerningFromPairPosFormat1(subTable):
    assert subTable.ValueFormat1 in (0, 4)
    assert subTable.ValueFormat2 == 0

    kerning = {}
    for firstGlyph, pairSet in zip(subTable.Coverage.glyphs, subTable.PairSet):
        for pvr in pairSet.PairValueRecord:
            if pvr.Value1 is not None:
                kerning[firstGlyph, pvr.SecondGlyph] = pvr.Value1.XAdvance
            else:
                kerning[firstGlyph, pvr.SecondGlyph] = 0
    return kerning


def _getKerningFromPairPosFormat2(subTable):
    assert subTable.ValueFormat1 in (0, 4)
    assert subTable.ValueFormat2 == 0

    allGlyphs = set(subTable.Coverage.glyphs)
    classDef1 = dict(subTable.ClassDef1.classDefs)
    for gn in allGlyphs - set(classDef1):
        classDef1[gn] = 0
    classDef2 = dict(subTable.ClassDef2.classDefs)

    kerning = {}
    for firstGlyph, class1 in classDef1.items():
        for secondGlyph, class2 in classDef2.items():
            valueRecord = subTable.Class1Record[class1].Class2Record[class2].Value1
            if valueRecord is not None:
                value = valueRecord.XAdvance
                kerning[firstGlyph, secondGlyph] = value
            else:
                assert subTable.ValueFormat1 == 0
                # XXXX According to getKerningPairsFromOTF.py we need to ignore subTable.ValueFormat1 == 0
                # But then: what does such a subtable accomplish at all?
                #kerning[firstGlyph, secondGlyph] = 0
    if subTable.ValueFormat1 == 0:
        # See above, this makes no sense to me.
        assert len(kerning) == 0
    return kerning


def getFeatureLookupIndices(gpos, featureTag):
    lookupIndices = []
    for feature in gpos.FeatureList.FeatureRecord:
        if feature.FeatureTag == featureTag:
            if lookupIndices:
                assert lookupIndices == sorted(feature.Feature.LookupListIndex)
            else:
                lookupIndices = sorted(feature.Feature.LookupListIndex)
    return lookupIndices


def _getKernTables(gpos):
    lookupIndices = getFeatureLookupIndices(gpos, "kern")
    kernTables = []
    for li in lookupIndices:
        lookup = gpos.LookupList.Lookup[li]
        assert lookup.LookupType in (2, 9)
        for subTable in lookup.SubTable:
            if subTable.LookupType == 9:
                # ExtensionLookup
                assert subTable.ExtensionLookupType == 2
                subTable = subTable.ExtSubTable
            assert subTable.LookupType == 2
            if subTable.Format == 1:
                kernTables.append(_getKerningFromPairPosFormat1(subTable))
            elif subTable.Format == 2:
                kernTables.append(_getKerningFromPairPosFormat2(subTable))
            else:
                assert 0
    return kernTables


def getKerningFromGPOS(gpos, clearZeros=True):
    kerning = {}
    for kernTable in reversed(_getKernTables(gpos)):
        kerning.update(kernTable)
    if clearZeros:
        kerning = filterZeroKerning(kerning)
    return kerning


def interpolateKerning(kerning1, kerning2, factor):
    """
        >>> interpolateKerning({}, {}, 0.5)
        {}
        >>> interpolateKerning({("T", "o"): 10}, {}, 0.5)
        {('T', 'o'): 5.0}
        >>> interpolateKerning({}, {("T", "o"): 10}, 0.5)
        {('T', 'o'): 5.0}
        >>> interpolateKerning({("T", "o"): 10}, {("T", "o"): 20}, 0.5)
        {('T', 'o'): 15.0}
        >>> interpolateKerning({("T", "o"): 10}, {("T", "o"): 20}, 0.0)
        {('T', 'o'): 10.0}
        >>> interpolateKerning({("T", "o"): 10}, {("T", "o"): 20}, 1.0)
        {('T', 'o'): 20.0}
    """
    interpolatedKerning = {}
    for pair in sorted(set(kerning1) | set(kerning2)):
        val1 = kerning1.get(pair, 0)
        val2 = kerning2.get(pair, 0)
        interpolatedKerning[pair] = val1 + factor * (val2 - val1)
    return interpolatedKerning


def scaleKerning(kerning, scaleFactor):
    """
        >>> scaleKerning({("T", "o"): 10}, 2.0)
        {('T', 'o'): 20.0}
    """
    return {pair: scaleFactor * kerning[pair] for pair in kerning}


def roundKerning(kerning):
    """
        >>> roundKerning(scaleKerning({("T", "o"): 10}, 2.234))
        {('T', 'o'): 22}
    """
    return {pair: int(round(kerning[pair])) for pair in kerning}


def filterZeroKerning(kerning):
    """
        >>> filterZeroKerning({("T", "o"): 10, ("T", "H"): 0})
        {('T', 'o'): 10}
    """
    return {pair: kerning[pair] for pair in kerning if kerning[pair] != 0}


def subsetKerning(kerning, glyphNames):
    """
        >>> subsetKerning({("T", "o"): 10, ("T", "H"): 20}, {"T", "H"})
        {('T', 'H'): 20}
        >>> subsetKerning({("T", "o"): 10, ("T", "H"): 20}, {"T", "o", "H"})
        {('T', 'o'): 10, ('T', 'H'): 20}
        >>> subsetKerning({("T", "o"): 10, ("T", "H"): 20}, {"T", "o"})
        {('T', 'o'): 10}
        >>> subsetKerning({("T", "o"): 10, ("T", "H"): 20}, {"H", "o"})
        {}
    """
    return {pair: kerning[pair] for pair in kerning if pair[0] in glyphNames and pair[1] in glyphNames}


#
# other GPOS tools
#

_valueRecordAttrs = ["XPlacement", "YPlacement", "XAdvance", "YAdvance"]

class MyValueRecord(object):

    """
        >>> MyValueRecord([0, 0, 0, 0])
        <0 0 0 0>
        >>> MyValueRecord([0, 0, 0, 0]).asTuple()
        (0, 0, 0, 0)
        >>> MyValueRecord([0, 1, 0, 0]) * 2
        <0 2 0 0>
        >>> MyValueRecord([0, 1.2, 0, 4.0]) * 2
        <0 2.4 0 8.0>
        >>> 2 * MyValueRecord([0, 1.2, 0, 4.0])
        <0 2.4 0 8.0>
        >>> (MyValueRecord([0, 1.2, 0, 4.0]) * 2).round()
        <0 2 0 8>
        >>> MyValueRecord([100, 0, 20, -30]) + MyValueRecord([10, 10, 10, 10])
        <110 10 30 -20>
        >>> MyValueRecord([100, 0, 20, -30]) - MyValueRecord([10, 10, 10, 10])
        <90 -10 10 -40>
        >>> MyValueRecord([10, 10, 10, 10]) - MyValueRecord([100, 0, 20, -30])
        <-90 10 -10 40>
    """

    def __init__(self, valueRecord):
        if isinstance(valueRecord, (tuple, list)):
            for index, attrName in enumerate(_valueRecordAttrs):
                setattr(self, attrName, valueRecord[index])
        else:
            for attrName in _valueRecordAttrs:
                setattr(self, attrName, getattr(valueRecord, attrName, 0))

    def asTuple(self):
        return tuple(getattr(self, attrName) for attrName in _valueRecordAttrs)

    def __repr__(self):
        return "<%s %s %s %s>" % self.asTuple()

    def __mul__(self, factor):
        return MyValueRecord(tuple(v * factor for v in self.asTuple()))
    __rmul__ = __mul__

    def __add__(self, other):
        return MyValueRecord(tuple(s + o for s, o in zip(self.asTuple(), other.asTuple())))
    __radd__ = __add__

    def __sub__(self, other):
        return MyValueRecord(tuple(s - o for s, o in zip(self.asTuple(), other.asTuple())))

    def __rsub__(self, other):
        return MyValueRecord(tuple(o - s for s, o in zip(self.asTuple(), other.asTuple())))

    def round(self):
        return MyValueRecord(tuple(int(round(v)) for v in self.asTuple()))


def writeSinglePosFeature(lookupMap, featureTag):
    ff = StringIO()
    ff.write("feature %s {\n" % featureTag)
    for gn in sorted(lookupMap):
        ff.write("  position %s %s;\n" % (gn, lookupMap[gn]))
    ff.write("} %s;\n\n" % featureTag)
    return ff.getvalue()


def getSinglePosFromGPOS(gpos, featureTag):
    lookupIndices = getFeatureLookupIndices(gpos, featureTag)
    lookupType = None
    lookupMap = {}
    for lookupIndex in lookupIndices:
        lookup = gpos.LookupList.Lookup[lookupIndex]
        if lookupType is None:
            lookupType = lookup.LookupType
        else:
            assert lookupType == lookup.LookupType
        for subTable in lookup.SubTable:
            if subTable.Format == 1:
                for gn in subTable.Coverage.glyphs:
                    lookupMap[gn] = MyValueRecord(subTable.Value)
            elif subTable.Format == 2:
                assert len(subTable.Coverage.glyphs) == len(subTable.Value)
                for gn, value in zip(subTable.Coverage.glyphs, subTable.Value):
                    assert gn not in lookupMap
                    lookupMap[gn] = MyValueRecord(value)
            else:
                assert 0
    return lookupMap


def interpolateSinglePos(singlePos1, singlePos2, factor):
    interpolatedSinglePos = {}
    zeroValue = MyValueRecord((0, 0, 0, 0))
    for glyphName in sorted(set(singlePos1) | set(singlePos2)):
        val1 = singlePos1.get(glyphName, zeroValue)
        val2 = singlePos2.get(glyphName, zeroValue)
        interpolatedSinglePos[glyphName] = val1 + factor * (val2 - val1)
    return interpolatedSinglePos


def scaleSinglePos(singlePos, scaleFactor):
    return {glyphName: scaleFactor * singlePos[glyphName] for glyphName in singlePos}


def roundSinglePos(singlePos):
    return {glyphName: singlePos[glyphName].round() for glyphName in singlePos}


def filterZeroSinglePos(singlePos):
    return {glyphName: singlePos[glyphName] for glyphName in singlePos if singlePos[glyphName].asTuple() != (0, 0, 0, 0)}


def subsetSinglePos(singlePos, glyphNames):
    return {glyphName: singlePos[glyphName] for glyphName in singlePos if glyphName in glyphNames}


def _runDocTests():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    import sys
    from fontTools.ttLib import TTFont

    for path in sys.argv[1:]:
        print("dumping kerning for %r" % path)
        f = TTFont(path)
        kerning = getKerningFromGPOS(f['GPOS'].table)
        for g1, g2 in sorted(kerning):
            print(g1, g2, kerning[g1, g2])
        print

        for featureTag in ["halt", "palt", "vhal", "vpal"]:
            singlePos = getSinglePosFromGPOS(f['GPOS'].table, featureTag)
            if singlePos:
                print(writeSinglePosFeature(singlePos, featureTag))
    else:
        _runDocTests()
