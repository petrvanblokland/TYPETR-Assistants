from fontTools.ttLib import newTable
from fontTools.ttLib.tables import otTables as ot
from fontTools.otlLib.builder import buildLookup, buildSingleSubstSubtable
from fontTools.varLib.models import normalizeValue
from tnbits.compilers.f5 import otlTools


def addConditionalSubstitutions(font, conditionalSubstitutions):
    """Add conditional substitutions to a Variable Font.

    The `conditionalSubstitutions` argument is a list of (Region, Substitutions)
    tuples.

    A Region is a list of Spaces. A Space is a dict mapping axisTags to
    (minValue, maxValue) tuples. Irrelevant axes may be omitted.
    A Space represents a 'rectangular' subset of an N-dimensional design space.
    A Region represents a more complex subset of an N-dimensional design space,
    namely the union of all the Spaces in the Region.
    For efficiency, Spaces within a Region should ideally not overlap, but
    functionality is not compromised if they do.

    A Substitution is a dict mapping source glyph names to substitute glyph names.

    Example:

        >>> f = TTFont(srcPath)
        >>> condSubst = [
        ...     # A list of (Region, Substitution) tuples.
        ...     ([{"wght": (0.5, 1.0)}], {"dollar": "dollar.rvrn"}),
        ...     ([{"wdth": (0.5, 1.0)}], {"cent": "cent.rvrn"}),
        ... ]
        >>> addConditionalSubstitutions(f, condSubst)
        >>> f.save(dstPath)
    """
    defaultSpace = {}
    axisMap = {}
    for axis in font["fvar"].axes:
        defaultSpace[axis.axisTag] = (axis.minValue, axis.maxValue)
        axisMap[axis.axisTag] = (axis.minValue, axis.defaultValue, axis.maxValue)

    # Since the FeatureVariations table will only ever match one rule at a time,
    # we will make new rules for all possible combinations of our input, so we
    # can indirectly support overlapping rules.
    explodedConditionalSubstitutions = []
    for permutation in getPermutations(len(conditionalSubstitutions)):
        regions = []
        lookups = []
        for index in permutation:
            regions.append(conditionalSubstitutions[index][0])
            lookups.append(conditionalSubstitutions[index][1])
        if not regions:
            continue
        intersection = regions[0]
        for region in regions[1:]:
            intersection = intersectRegions(intersection, region)
        for space in intersection:
            # Remove default values, so we don't generate redundant ConditionSets
            space = cleanupSpace(space, defaultSpace)
            if space:
                explodedConditionalSubstitutions.append((normalizeSpace(space, axisMap), lookups))

    addConditionalSubstitutionsRaw(font, explodedConditionalSubstitutions)


def getPermutations(numRules):
    """Given a number of rules, return a list of all combinations by index.
    The list is reverse-sorted by the number of indices, so we get the most
    specialized rules first."""
    bitNumbers = range(numRules)
    permutations = []
    for num in range(2 ** numRules):
        permutation = []
        for bitNum in bitNumbers:
            if num & (1 << bitNum):
                permutation.append(bitNum)
        permutations.append(permutation)
    # reverse sort by the number of indices
    permutations.sort(key=lambda x: len(x), reverse=True)
    return permutations


"""
Region and Space support

Terminology:

A 'Space' is a dict representing a "rectangular" bit of N-dimensional space.
The keys in the dict are axis tags, the values are (minValue, maxValue) tuples.
Missing dimensions (keys) are substituted by the default min and max values
from the corresponding axes.

A 'Region' is a list of Space dicts, representing the union of the Spaces,
therefore representing a more complex subset of design space.
"""

def intersectRegions(region1, region2):
    """Return the region intersecting `region1` and `region2`."""
    region = []
    for space1 in region1:
        for space2 in region2:
            space = intersectSpaces(space1, space2)
            if space is not None:
                region.append(space)
    return region


def intersectSpaces(space1, space2):
    """Return the space intersected by `space1` and `space2`, or None if there
    is no intersection."""
    space = {}
    space.update(space1)
    space.update(space2)
    for axisTag in set(space1) & set(space2):
        min1, max1 = space1[axisTag]
        min2, max2 = space2[axisTag]
        minimum = max(min1, min2)
        maximum = min(max1, max2)
        if not minimum < maximum:
            return None
        space[axisTag] = minimum, maximum
    return space


def cleanupSpace(space, defaultSpace):
    """Return a sparse copy of `space`, without redundant (default) values."""
    return {tag: limit for tag, limit in space.items() if limit != defaultSpace[tag]}


def normalizeSpace(space, axisMap):
    """Convert the min/max values in the `space` dict to normalized
    design space values."""
    space = {tag: (normalizeValue(minValue, axisMap[tag]), normalizeValue(maxValue, axisMap[tag]))
                for tag, (minValue, maxValue) in space.items()}
    return space


#
# Low level implementation
#

def addConditionalSubstitutionsRaw(font, conditionalSubstitutions):
    """Low level implementation of addConditionalSubstitutions that directly
    models the possibilities of the FeatureVariations table."""

    #
    # assert there are no 'kern' and 'rvrn' features
    # make dummy 'kern' and 'rvrn' features with no lookups
    # sort features, get 'kern' and 'rvrn' feature indices
    # make lookups
    # add feature variations
    #

    if "GSUB" not in font:
        font["GSUB"] = buildGSUB()

    gsub = font["GSUB"].table

    if gsub.Version < 0x00010001:
        gsub.Version = 0x00010001  # allow gsub.FeatureVariations

    gsub.FeatureVariations = None  # delete any existing FeatureVariations

    for feature in gsub.FeatureList.FeatureRecord:
        assert feature.FeatureTag != 'kern'
        assert feature.FeatureTag != 'rvrn'

    kernFeature = buildFeatureRecord('kern', [])
    rvrnFeature = buildFeatureRecord('rvrn', [])
    gsub.FeatureList.FeatureRecord.append(kernFeature)
    gsub.FeatureList.FeatureRecord.append(rvrnFeature)

    otlTools.sortFeatureList(gsub)
    kernFeatureIndex = gsub.FeatureList.FeatureRecord.index(kernFeature)
    rvrnFeatureIndex = gsub.FeatureList.FeatureRecord.index(rvrnFeature)

    for scriptRecord in gsub.ScriptList.ScriptRecord:
        for langSys in [scriptRecord.Script.DefaultLangSys] + scriptRecord.Script.LangSysRecord:
            langSys.FeatureIndex.extend([kernFeatureIndex, rvrnFeatureIndex])

    # setup lookups

    # turn substitution dicts into tuples of tuples, so they can be hashed
    conditionalSubstitutions, allSubstitutions = makeSubstitutionsHashable(conditionalSubstitutions)

    lookupMap = buildSubstitutionLookups(gsub, allSubstitutions)

    axisIndices = {axis.axisTag: axisIndex for axisIndex, axis in enumerate(font["fvar"].axes)}

    featureVariationRecords = []
    for conditionSet, substitutions in conditionalSubstitutions:
        conditionTable = []
        for axisTag, (minValue, maxValue) in sorted(conditionSet.items()):
            assert minValue < maxValue
            ct = buildConditionTable(axisIndices[axisTag], minValue, maxValue)
            conditionTable.append(ct)

        lookupIndices = [lookupMap[subst] for subst in substitutions]
        ftsr1 = buildFeatureTableSubstitutionRecord(kernFeatureIndex, lookupIndices)
        ftsr2 = buildFeatureTableSubstitutionRecord(rvrnFeatureIndex, lookupIndices)
        featureVariationRecords.append(buildFeatureVariationRecord(conditionTable, [ftsr1, ftsr2]))

    gsub.FeatureVariations = buildFeatureVariations(featureVariationRecords)


#
# Building GSUB/FeatureVariations internals
#

def buildGSUB():
    """Build a GSUB table from scratch."""
    fontTable = newTable("GSUB")
    gsub = fontTable.table = ot.GSUB()
    gsub.Version = 0x00010001  # allow gsub.FeatureVariations

    gsub.ScriptList = ot.ScriptList()
    gsub.ScriptList.ScriptRecord = []
    gsub.FeatureList = ot.FeatureList()
    gsub.FeatureList.FeatureRecord = []
    gsub.LookupList = ot.LookupList()
    gsub.LookupList.Lookup = []

    srec = ot.ScriptRecord()
    srec.ScriptTag = 'DFLT'
    srec.Script = ot.Script()
    srec.Script.DefaultLangSys = None
    srec.Script.LangSysRecord = []

    langrec = ot.LangSysRecord()
    langrec.LangSys = ot.LangSys()
    langrec.LangSys.ReqFeatureIndex = 0xFFFF
    langrec.LangSys.FeatureIndex = [0]
    srec.Script.DefaultLangSys = langrec.LangSys

    gsub.ScriptList.ScriptRecord.append(srec)
    gsub.FeatureVariations = None

    return fontTable


def makeSubstitutionsHashable(conditionalSubstitutions):
    """Turn all the substitution dictionaries in sorted tuples of tuples so
    they are hashable, to detect duplicates so we don't write out redundant
    data."""
    allSubstitutions = set()
    condSubst = []
    for conditionSet, substitutionMaps in conditionalSubstitutions:
        substitutions = []
        for substitutionMap in substitutionMaps:
            subst = tuple(sorted(substitutionMap.items()))
            substitutions.append(subst)
            allSubstitutions.add(subst)
        condSubst.append((conditionSet, substitutions))
    return condSubst, sorted(allSubstitutions)


def buildSubstitutionLookups(gsub, allSubstitutions):
    """Build the lookups for the glyph substitutions, return a dict mapping
    the substitution to lookup indices."""
    firstIndex = len(gsub.LookupList.Lookup)
    lookupMap = {}
    for i, substitutionMap in enumerate(allSubstitutions):
        lookupMap[substitutionMap] = i + firstIndex

    for subst in allSubstitutions:
        substMap = dict(subst)
        lookup = buildLookup([buildSingleSubstSubtable(substMap)])
        gsub.LookupList.Lookup.append(lookup)
        assert gsub.LookupList.Lookup[lookupMap[subst]] is lookup
    return lookupMap


def buildFeatureVariations(featureVariationRecords):
    """Build the FeatureVariations subtable."""
    fv = ot.FeatureVariations()
    fv.Version = 0x00010000
    fv.FeatureVariationRecord = featureVariationRecords
    return fv

def buildFeatureRecord(featureTag, lookupListIndices):
    """Build a FeatureRecord."""
    fr = ot.FeatureRecord()
    fr.FeatureTag = featureTag
    fr.Feature = ot.Feature()
    fr.Feature.LookupListIndex = lookupListIndices
    return fr

def buildFeatureVariationRecord(conditionTable, substitutionRecords):
    """Build a FeatureVariationRecord."""
    fvr = ot.FeatureVariationRecord()
    fvr.ConditionSet = ot.ConditionSet()
    fvr.ConditionSet.ConditionTable = conditionTable
    fvr.FeatureTableSubstitution = ot.FeatureTableSubstitution()
    fvr.FeatureTableSubstitution.Version = 0x00010001
    fvr.FeatureTableSubstitution.SubstitutionRecord = substitutionRecords
    return fvr

def buildFeatureTableSubstitutionRecord(featureIndex, lookupListIndices):
    """Build a FeatureTableSubstitutionRecord."""
    ftsr = ot.FeatureTableSubstitutionRecord()
    ftsr.FeatureIndex = featureIndex
    ftsr.Feature = ot.Feature()
    ftsr.Feature.LookupListIndex = lookupListIndices
    return ftsr

def buildConditionTable(axisIndex, filterRangeMinValue, filterRangeMaxValue):
    """Build a ConditionTable."""
    ct = ot.ConditionTable()
    ct.Format = 1
    ct.AxisIndex = axisIndex
    ct.FilterRangeMinValue = filterRangeMinValue
    ct.FilterRangeMaxValue = filterRangeMaxValue
    return ct


if __name__ == "__main__":
    from fontTools.ttLib import TTFont

    srcPath = "AgencyFB-VF-N-4-edited.ttf"
    dstPath = "AgencyVarRebuilt2.ttf"

    f = TTFont(srcPath)
    dollarSubst = {"dollar": "dollar.rvrn"}
    condSubst = [
        ([("wght", 0.5, 1.0)], dollarSubst),
        ([("wdth", -1.0, -0.5), ("wght", -0.5, 1.0)], dollarSubst),
    ]
    addConditionalSubstitutions(f, condSubst)

    f.save(dstPath)
    f = TTFont(dstPath)
    f.saveXML(dstPath + ".ttx", tables=["GSUB"])
