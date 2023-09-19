from fontTools.ttLib.tables.otTables import SingleSubst, Lookup, FeatureRecord, Feature
from tnbits.compilers.f5 import otlTools


def addSingleSubstFeature(gsubTable, mapping, featureTag):  # XXX args needed to specify where to insert the feature
    if hasattr(gsubTable, "table"):
        gsubTable = gsubTable.table
    assert mapping, "empty substitution"

    for feature in gsubTable.FeatureList.FeatureRecord:
        if feature.FeatureTag == featureTag:
            # Theoretically we could merge the new feature with the existing
            # one. For now, it's probably best to just complain loudly.
            raise ValueError("%s feature already defined" % featureTag)

    lookup = buildSingleSubstLookup(mapping)
    lookupIndex = 0
    insertLookup(gsubTable, lookupIndex, lookup)
    featureRec = buildFeatureRecord(gsubTable, featureTag, lookupIndex)
    featureIndex = appendFeatureRecord(gsubTable, featureRec)
    addFeatureToScripts(gsubTable, featureIndex)

    # Lastly, sort the feature list by feature tag
    otlTools.sortFeatureList(gsubTable)


def buildSingleSubstLookup(mapping):
    # first, create the subtable, the actual lookup
    subTable = SingleSubst()
    subTable.mapping = mapping

    # create the lookup and add the subtable to it
    lookup = Lookup()
    lookup.LookupType = 1
    lookup.LookupFlag = 0
    lookup.SubTable = [subTable]
    lookup.SubTableCount = len(lookup.SubTable)  # FontTools requires this here
    return lookup


def insertLookup(gsubTable, atIndex, lookup):
    if atIndex < 0:
        atIndex %= len(gsubTable.LookupList.Lookup)
    else:
        atIndex = min(atIndex, len(gsubTable.LookupList.Lookup))

    lookupRemap = dict(zip(
        range(len(gsubTable.LookupList.Lookup)),
        range(0, atIndex) + range(atIndex + 1, len(gsubTable.LookupList.Lookup) + 1)
    ))
    assert len(lookupRemap) == len(gsubTable.LookupList.Lookup)
    #assert atIndex not in set(lookupRemap.values())  # XXX
    otlTools.remapLookups(gsubTable, lookupRemap)
    gsubTable.LookupList.Lookup.insert(atIndex, lookup)
    gsubTable.LookupList.LookupCount = len(gsubTable.LookupList.Lookup)  # FontTools requires this here


def buildFeatureRecord(gsubTable, featureTag, lookupIndex):
    # Set up the feature and feature record
    feature = Feature()
    feature.FeatureParams = None
    feature.LookupListIndex = [lookupIndex]
    featureRec = FeatureRecord()
    featureRec.FeatureTag = featureTag
    featureRec.Feature = feature
    return featureRec


def appendFeatureRecord(gsubTable, featureRec):
    featureIndex = len(gsubTable.FeatureList.FeatureRecord)
    gsubTable.FeatureList.FeatureRecord.append(featureRec)
    return featureIndex


def addFeatureToScripts(gsubTable, featureIndex):
    # Just add it to all the FeatureIndex lists we can find
    # XXX this will need to be more specific and more flexible
    for script in gsubTable.ScriptList.ScriptRecord:
        script.Script.DefaultLangSys.FeatureIndex.append(featureIndex)
        for langSysRec in script.Script.LangSysRecord:
            langSysRec.LangSys.FeatureIndex.append(featureIndex)
