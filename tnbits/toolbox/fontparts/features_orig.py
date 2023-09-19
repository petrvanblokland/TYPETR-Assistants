# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

import re
import os
from tnbits.toolbox.file import File

try:
    from feaTools.test import TestFeatureWriter, parseFeatures
except:
    print('Warning: missing feaTools.')

class FeaturesTX:
    """
    `FeaturesTX` contains basic tools for accessing and modifying features as plain text.
    """
    # PLAINTEXT

    @classmethod
    def get(cls, name='', features=''):
        """
        `get` uses regular expressions to return the feature text of _name_ from _features_.
        """
        rSearchTerm = re.compile("feature %s {.*?} %s;" %(name, name), re.DOTALL)
        newFeatureText = re.search(rSearchTerm, features)
        if newFeatureText:
            return newFeatureText.group()
        else:
            return None

    @classmethod
    def replace(cls, findName='', replace='', features='', DEBUG=False):
        """`replace` uses regular expressions to replace the feature text of
        _name_ with _replace_."""
        rSearchTerm = re.compile("feature %s {.*?} %s;" %(findName, findName), re.DOTALL)
        rNewFeatureText, rNum = re.subn(rSearchTerm, replace, features,  re.MULTILINE)
        if DEBUG:
            print('Found', rNum, 'features to replace.')
        return rNewFeatureText

    @classmethod
    def remove(cls, findName='', features=''):
        """`remove` uses regular expressions to replace the feature text of
        _name_ with _replace_."""
        return cls.replace(findName=findName, replace='', features=features)

    @classmethod
    def parse(cls, features=''):
        """
        `parse` uses `feaTools` to parse features into statements.
        """
        writer = TestFeatureWriter()
        parseFeatures(writer, features)
        parsedData =  writer.getData()
        return parsedData

    @classmethod
    def parseKern(cls, kernFeature=''):
        """
        `parseKern` uses `feaTools` to parse a plaintext {kern} feature into dicts of pairs and groups.
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
        searchTerm = re.compile(r'include \(([^>]*?)\);')
        includes = re.findall(searchTerm, fea)
        for include in includes:
            path = os.path.join(basePath, include)
            if os.path.exists(path):
                featuresToAdd = File.read(path)
                fea, count = re.subn(searchTerm, featuresToAdd, fea)
            else:
                print('Error. Could not find %s' %path)
                fea, count = re.subn(searchTerm, 'FAILED INCLUDE %s' %include, fea)
        return fea

if __name__ == "__main__":
    from mojo.roboFont import CurrentFont
    f = CurrentFont()
    print(f)
    print(FeaturesTX.getFlattened(f.features.text, os.path.split(f.path)[0]))
