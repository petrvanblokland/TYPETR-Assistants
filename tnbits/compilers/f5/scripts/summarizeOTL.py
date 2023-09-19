# -*- coding: utf8 -*-


from fontTools.ttLib import TTFont


def summarizeScripts(scripts):
    print("number of scripts:", len(scripts))
    for script in scripts:
        print(script.ScriptTag)
        print("-   DFLT",)
        print(hex(script.Script.DefaultLangSys.ReqFeatureIndex),)
        print(script.Script.DefaultLangSys.FeatureIndex  #', 'LookupOrder', 'ReqFeatureIndex)
        for langSysRec in script.Script.LangSysRecord:
            print("   ", langSysRec.LangSysTag,)
            print(hex(langSysRec.LangSys.ReqFeatureIndex),)
            print(langSysRec.LangSys.FeatureIndex)
    print

def summarizeFeatures(features):
    allLookups = set()
    print("number of features:", len(features))
    for index, feature in enumerate(features):
        print(index, feature.FeatureTag, feature.Feature.LookupListIndex)
        allLookups |= set(feature.Feature.LookupListIndex)
    print
    print("number of lookups directly used by features:", len(allLookups))
    print

def summarizeLookups(lookups):
    print("number of lookups:", len(lookups))
    allTypes = set()
    for index, lookup in enumerate(lookups):
        print("%s LookupType: %s, LookupFlag: %s" % (index, lookup.LookupType, lookup.LookupFlag))
        for subTable in lookup.SubTable:
            lookupName = subTable.__class__.__name__
            allTypes.add("%sFormat%s" % (lookupName, subTable.Format))
            print("    %s, Format: %s, LookUpType: %s" % (lookupName, subTable.Format, subTable.LookupType))
            if lookupName in ["ExtensionSubst", "ExtensionPos"]:
                subTable = subTable.ExtSubTable
                lookupName = subTable.__class__.__name__
                allTypes.add("%sFormat%s" % (lookupName, subTable.Format))
                print("    --- %s, Format: %s, LookUpType: %s" % (lookupName, subTable.Format, subTable.LookupType))

    print
    print("LookupTypes used:", ", ".join(sorted(allTypes)))
    print

def summarizeOTL(path):
    font = TTFont(path)
    for tag in ["GPOS", "GSUB"]:
        print("*" * 80)
        print("    ", tag, path)
        print("*" * 80)
        print
        try:
            table = font[tag].table
        except KeyError:
            print("No %s table found" % tag)
        else:
            summarizeScripts(table.ScriptList.ScriptRecord)
            summarizeFeatures(table.FeatureList.FeatureRecord)
            summarizeLookups(table.LookupList.Lookup)
        print


if __name__ == "__main__":
    import sys, os
    if sys.argv[1:]:
        paths = sys.argv[1:]
    else:
        from tnTestFonts import getAllFontPaths
        paths = getAllFontPaths("ttf", "otf")
    for path in paths:
        summarizeOTL(path)
