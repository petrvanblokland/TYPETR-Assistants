# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   features.py
#

import re
import os
from tnbits.toolbox.file import File
from tnbits.toolbox.glyph import GlyphTX
#from tnbits.contributions.fbFeaTools.parser import parseFeatures
#from tnbits.contributions.fbFeaTools.writers.parseWriter import ParseFeatureWriter
#from tnbits.contributions.fbFeaTools.writers.fdkSyntaxWriter import FDKSyntaxFeatureWriter
#from tnbits.contributions.fbFeaTools.writers.subsetWriter import SubsetFeatureWriter
#from tnbits.contributions.fbFeaTools.writers.gsubMapWriter import GSUBMapWriter

class FeaturesTX:
    """FeaturesTX contains basic tools for accessing and modifying features as plain text.
    """
    # PLAINTEXT

    @classmethod
    def checkFeaType(cls, features):
        """
        `checkFeaType` is used to check whether the _features_ argument passed is the features object or a text string. It returns a tuple with features as text string and _feaType_ indicating whether the original was an object or text type.
        """
        try:
            feaText = features.text
            feaType = 'object'
        except:
            feaText = features
            feaType = 'text'
        return (feaText, feaType)

    @classmethod
    def getFeature(cls, name, features):
        """
        `getFeature` uses regular expressions to return the feature block text of _name_ from _features_.
        """
        feaText, feaType = cls.checkFeaType(features) # so that we can accept a feature object or text string; or do we want assume features as text?
        rSearchTerm = re.compile("feature %s {.*?} %s;" %(name, name), re.DOTALL)
        feaBlock = re.search(rSearchTerm, feaText)
        if feaBlock:
            return feaBlock.group()
        else:
            return None

    @classmethod
    def replaceFeature(cls, findName, replace, features, DEBUG=False):
        """
        `replaceFeature` uses regular expressions to replace the feature block text of _findName_ with _replace_ in _features_.
        """
        # Test for feature object or text string
        feaText, feaType = cls.checkFeaType(features) # Do we care about accepting either feature object or text, or do we want to require that features be provided as text?
        rSearchTerm = re.compile("feature %s {.*?} %s;" %(findName, findName), re.DOTALL)
        newFeaText, rNum = re.subn(rSearchTerm, replace, feaText)
        if DEBUG:
            print('Found', rNum, 'features to replace.')
        # Pass back the same type of object as provided
        if feaType == 'object':
            features.text = newFeaText
        else:
            features = newFeaText
        return features

    @classmethod
    def removeFeature(cls, findName, features):
        """
        `removeFeature` uses regular expressions to remove the feature block text of _findName_ from _features_.
        """
        return cls.replaceFeature(findName=findName, replace='', features=features)

    @classmethod
    def getClass(cls, name, features):
        """
        `getClass` uses regular expressions to return the class definition of _name_ (with or without @ token) from _features_.
        """
        feaText, feaType = cls.checkFeaType(features) # so that we can accept a feature object or text string; or do we want assume features as text?
        if '@' in name:
            name = name.replace('@', '') # so we can accept and process a class name with or without the @; or should we just assume/require @ token to be provided in the argument?
        rSearchTerm = re.compile(r"@%s ?= ?\[.*?\];" %(name), re.DOTALL) # Do we need/want dotall mode?
        classDef = re.search(rSearchTerm, feaText)
        if classDef:
            return classDef.group()
        else:
            return None

    #============

    @classmethod
    def renameReference(cls, sourceName, destName, features):
        """
        `renameReference` renames all references of a glyph _sourceName_ to _destName_ in _features_. _Features_ may be provided as f.features object or as text.
        """
        # Test for feature object or text string
        feaText, feaType = cls.checkFeaType(features)
        sourceName = sourceName.replace('.', '\.') # probably a good idea to escape any periods in source glyph name, just in case
        rSearchTerm = re.compile(r'(^%s|(?<!feature )(?<!lookup )(?<!} )(?<=[\s\[])%s)(?=[;\s\]\'])' %(sourceName, sourceName), re.M) # using PERL non-capturing, positional assertions to delimit whole references and to ignore feature block & lookup name tags
        replaceTerm = r'%s' %(destName)
        feaText = re.sub(rSearchTerm, replaceTerm, feaText)
        # Pass back the same type of object as provided
        if feaType == 'object':
            features.text = feaText
        else:
            features = feaText
        return features

    @classmethod
    def getClassReferences(cls, featureBlock):
        """
        `getClassReferences` returns a list of any named classes referenced in _featureBlock_.
        """
        rSearchTerm = re.compile(r'@.+?(?=[;\s\]\'])')
        classRefs = set(re.findall(rSearchTerm, featureBlock)) # use set to eliminate duplicate references from findall
        return classRefs
        # Is it okay to return the raw set, or better to iterate the set back into plain list?

    @classmethod
    def remapGlyphsInClasses(cls, remap, classList, features):
        """
        `remapGlyphsInClasses` renames glyphs according to a _remap_ dictionary, targeting only class definitions named in _classList_ within _features_. _Features_ may be provided as f.features object or as text.
        """
        # Test for feature object
        feaText, feaType = cls.checkFeaType(features)
        # Make sure classList is list
        if isinstance(classList, str):
            classList = [classList]
        # Get each target class definition, derive new class def and replace in feature text
        for className in classList:
            classDef = cls.getClass(className, feaText)
            if classDef == None:
                print("Warning:", className, "class was not present in features")
                continue
            newClassDef = classDef
            for source, dest in remap.items():
                newClassDef = cls.renameReference(source, dest, newClassDef)
            if newClassDef != classDef:
                feaText = feaText.replace(classDef, newClassDef)
        # Pass back the same type of object as provided
        if feaType == 'object':
            features.text = feaText
        else:
            features = feaText
        return features

    @classmethod
    def remapGlyphsInFeatures(cls, remap, featureList, features):
        """`remapGlyphsInFeatures` renames glyphs according to a _remap_
        dictionary, targeting only feature blocks named in _featureList_ within
        _features_. _Features_ may be provided as f.features object or as
        text."""
        # Test for feature object
        feaText, feaType = cls.checkFeaType(features)
        # Make sure featureList is list
        if isinstance(featureList, str):
            featureList = [featureList]
        # Get each target feature block, collect any referenced classes, derive new feature block and replace in feature text
        classList = []
        for feaName in featureList:
            feaBlock = cls.getFeature(feaName, feaText)
            if feaBlock == None:
                print("Warning", feaName, "feature was not present in features")
                continue
            feaClasses = cls.getClassReferences(feaBlock)
            if len(feaClasses) > 0:
                classList.extend(feaClasses)
            newFeaBlock = feaBlock
            for source, dest in remap.items():
                newFeaBlock = cls.renameReference(source, dest, newFeaBlock)
            if newFeaBlock != feaBlock:
                feaText = feaText.replace(feaBlock, newFeaBlock)
        # Replace in any referenced classes
        if len(classList) > 0:
            classList = set(classList) # eliminate duplicate references across multiple fea blocks
            feaText = cls.remapGlyphsInClasses(remap, classList, feaText)
        # Pass back the same type of object as provided
        if feaType == 'object':
            features.text = feaText
        else:
            features = feaText
        return features

    @classmethod
    def swapGlyphsInFeatures(cls, swapMap, featureList, features):
        tempMap = {}
        swapBackMap = {}
        for gname, newName in swapMap.items():
            temp = GlyphTX.name.appendSuffixElement(gname, 'XXXXXXXXXXXXXXXXXXXX')
            tempMap[newName] = temp
            swapBackMap[temp] = gname
        features = cls.remapGlyphsInFeatures(tempMap, featureList, features)
        features = cls.remapGlyphsInFeatures(swapMap, featureList, features)
        features = cls.remapGlyphsInFeatures(swapBackMap, featureList, features)
        return features


    @classmethod
    def getFeatureTags(cls, features):
        """
        `getFeatureTags` will return a list of all feature tags used in a fea file.
        """
        feaText, feaType = cls.checkFeaType(features)
        rSearchTerm = re.compile("feature (....) {")
        feaTags = re.findall(rSearchTerm, feaText)
        return feaTags

    @classmethod
    def getGSUBMapping(cls, features):
        """
        `getGSBUMapping` parses FDK-syntax feature text and returns a dictionary keyed by feature tag and a second dictionary mapping {target: replacement} for each GSUB feature.
        """
        writer = GSUBMapWriter()
        parseFeatures(writer, features)
        gsubMap = writer.getMap()
        return gsubMap

    @classmethod
    def getGSUBMapForFeature(cls, featag, features):
        """
        `getGSBUBMapForFeature` parses FDK-syntax feature text and returns a {replacement: target} dictionary for the provided feature tag. If the feature file does not contain the provided tag or if the feature does not contain any parsed gsub types, the return will be an empty dict. There may still be some anomalies in format of returned target for gsub 4 (ligature) and gsub 6 (contextual).
        """
        gsubMap = cls.getGSUBMapping(features)
        return gsubMap.get(featag, {})


    @classmethod
    def subset(cls, removeList, features):
        """

        """
        writer = SubsetFeatureWriter(removeList)
        parseFeatures(writer, features)
        subsettedFeatures = writer.write()
        return subsettedFeatures

    #============

    @classmethod
    def parse(cls, features):
        """
        `parse` uses `fbfeaTools` to parse features into statements.
        """
        writer = ParseFeatureWriter()
        parseFeatures(writer, features)
        parsedData = writer.getData()
        return parsedData

    @classmethod
    def unparse(cls, parsedData):
        """
        `unparse` converts data in the format received from the `parse` method back into FDK feature syntax.
        """
        writer = FDKSyntaxFeatureWriter()
        cls.unParseFeatures(writer, parsedData)
        features = writer.write()
        return features

    @classmethod
    def unParseFeatures(cls, writer, parsedData):
        for token, obj in parsedData:
            if token == "class":
                name, contents = obj
                writer.classDefinition(name, contents)
            if token == "language system":
                scriptTag, languageTag = obj
                writer.languageSystem(scriptTag, languageTag)
            if token == "script":
                writer.script(obj)
            if token == "language":
                languageTag, includeDefault = obj
                writer.language(languageTag, includeDefault)
            if token == "feature":
                name, featureBlock = obj
                featureWriter = writer.feature(name)
                cls.unParseFeatures(featureWriter, featureBlock)
            if token == "lookup":
                name, lookupBlock = obj
                lookupWriter = writer.lookup(name)
                cls.unParseFeatures(lookupWriter, lookupBlock)
            if token == "gsub type 1":
                target, replacement = obj
                writer.gsubType1(target, replacement)
            if token == "gsub type 3":
                target, replacement = obj
                writer.gsubType3(target, replacement)
            if token == "gsub type 4":
                target, replacement = obj
                writer.gsubType4(target, replacement)
            if token == "gsub type 6":
                precedingContext, target, trailingContext, replacement = obj
                writer.gsubType6(precedingContext, target, trailingContext, replacement)
            if token == "gpos type 1":
                target, value = obj
                writer.gposType1(target, value)
            if token == "gpos type 2":
                target, value = obj
                writer.gposType2(target, value)
            if token == "lookup flag":
                rightToLeft, ignoreBaseGlyphs, ignoreLigatures, ignoreMarks = obj
                writer.lookupFlag(rightToLeft, ignoreBaseGlyphs, ignoreLigatures, ignoreMarks)
            if token == "lookup reference":
                writer.lookupReference(obj)
            if token == "feature reference":
                writer.featureReference(obj)
            if token == "table":
                name, data = obj
                writer.table(name, data)
            if token == "subtable break":
                writer.subtableBreak()
            if token == "include":
                writer.include(obj)

    #============

    @classmethod
    def parseKern(cls, kernFeature=''):
        """
        `parseKern` uses `fbfeaTools` to parse a plaintext {kern} feature into dicts of pairs and groups.
        """
        pairs = {}
        groups = {}
        enumPairs = {}
        data = cls.parse(kernFeature)
        feature = data[0][1][1]
        if 1 == 1:
            for item in feature:
                tokenType, tokenContent = item
                if tokenType == 'class':
                    groupName, groupList = tokenContent
                    groups[groupName] = groupList
                elif tokenType == 'gpos type 2':
                    pair, value = tokenContent
                    left, right = pair
                    if isinstance(left, list):
                        newLeft = cls.findGroup(left, groups)
                    else:
                        newLeft = left
                    if isinstance(right, list):
                        newRight = cls.findGroup(right, groups)
                    else:
                        newRight = right
                    if newLeft and newRight:
                        pairs[(newLeft, newRight)] = int(round(value, 1))
                    else:
                        value = int(round(value, 1))
                        if isinstance(left, list):
                            for l in left:
                                if isinstance(right, list):
                                    for r in right:
                                        enumPairs[(l, r)] = value
                                else:
                                    enumPairs[(l, right)] = value
                        else:
                            if isinstance(right, list):
                                for r in right:
                                    enumPairs[(left, r)] = value
                            else:
                                enumPairs[(left, right)] = value
        pairs.update(enumPairs)
        return pairs, groups

    @classmethod
    def findGroup(cls, gnames, groups={}):
        for groupName, groupGlyphs in groups.items():
            if set(gnames) == set(groupGlyphs):
                return groupName


    @classmethod
    def getKernFeatureFromKerning(cls, f):
        from ufo2fdk.kernFeatureWriter import KernFeatureWriter
        k = KernFeatureWriter(f)
        return k.write()

    @classmethod
    def getFlattened(cls, fea, sourcePath=''):
        basePath = os.path.split(sourcePath)[0]
        searchTerm = re.compile(r'include ?\(([^>]*?)\);') #KL Edit 130115
        includes = re.findall(searchTerm, fea)
        for include in includes:

            path = os.path.join(basePath, include)
            if os.path.exists(path):
                featuresToAdd = File.read(path)
                fea, count = re.subn(searchTerm, featuresToAdd, fea, count=1)
            else:
                print('Error. Could not find %s' %path)
                fea, count = re.subn(searchTerm, 'FAILED INCLUDE %s' %include, fea)
        return fea

if __name__ == "__main__":
    f = CurrentFont()
    print(FeaturesTX.getFlattened(f.features.text, f.path))

if __name__ == "__main__2":
    from mojo.roboFont import CurrentFont
    f = CurrentFont()
    # Testing
    #parsedData = FeaturesTX.parse(f.features.text)
    #features = FeaturesTX.unparse(parsedData)

    feaText = FeaturesTX.getFlattened(f.features.text, f.path)
    removeList = []
    features = FeaturesTX.subset(removeList, feaText)

    print(features)
