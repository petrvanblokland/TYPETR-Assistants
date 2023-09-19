# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

import os
from tnbits.toolbox.fontparts.fontinfo import FontInfoTX
from tnbits.toolbox.file import File
from tnbits.constants import Constants as C
import string


class Series:

    def __init__(self, styles):
        self.styles = styles

    def getStyles(self):
        return self._styles

    def setStyles(self, value):
        self._styles = value

    styles = property(getStyles, setStyles)

    def getAxes(self):
        axes = set()
        for style in self.styles:
            for axis in style.getAxisInfo().keys():
                axes.add(axis)
        return tuple(axes)

    def getNamesForAxis(self, axisName):
        values = set()
        for style in self.styles:
            axisInfo = style.getAxisInfo()
            if axisName in axisInfo:
                values.add(axisInfo.get(axisName))
            else:
                values.add(SeriesTX.getAxisDefault(axisName))
        return tuple(values)


class Style:

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    name = property(getName, setName)

    def getAxisInfo(self):
        return SeriesTX.getStyleInfo(self.name)

    def __repr__(self):
        return '<%s: %s>' %('BaseStyle', self.name)

class StyleForFont(Style):
    pass

class SeriesTX:

    @classmethod
    def getAxisDefault(cls, axis):
        for name, value in C.STYLENAME_PREFERRED_VALUES.get(axis):
            if isinstance(value, float):
                return name

    @classmethod
    def XXgetStyleInfo(cls, style):
        return FontInfoTX.getStyleInfo(style)

    @classmethod
    def getStyleInfo(cls, style):
        styleMap = {}
        style = style.replace('-', ' ')
        for axis,spectrum in C.STYLENAME_PREFERRED_VALUES.items():
            for word, _ in sorted(spectrum, key=lambda s: len(s[0])*-1): # word, score
                if word and word in style:
                    styleMap[axis] = word
                    style = style.replace(word, '')
                    style = style.replace('  ', '')
        if style and style != ' ':
            styleMap['tags'] = style.strip().split(' ')
        return styleMap

    @classmethod
    def getNumericStyleInfo(cls, style):
        styleInfo = cls.getStyleInfo(style)
        numericStyleInfo = dict()
        for attr, value in styleInfo.items():
            if attr != 'tags':
                num = cls.styleName2Numeric(value, attr)
                default = C.STYLENAME_DEFAULT_VALUES.get(attr)
                if num != default:
                    numericStyleInfo[attr] = num
        if 'tags' in styleInfo:
            if 'Roman' in styleInfo.get('tags'):
                styleInfo['tags'].pop(styleInfo['tags'].index('Roman'))
            if styleInfo['tags']:
                numericStyleInfo['tags'] = styleInfo.get('tags')
        return numericStyleInfo


    @classmethod
    def getNameForSorting(cls, name, attributeOrder=None):
        if not attributeOrder:
            attributeOrder = C.STYLENAME_DEFAULT_ORDER
        defaults = C.STYLENAME_DEFAULT_VALUES
        styleInfo = cls.getStyleInfo(name)
        sortingList = []
        for attribute in attributeOrder:
            if attribute in styleInfo:
                sortingList.append(cls.styleName2Numeric(styleInfo[attribute], attribute))
            else:
                sortingList.append(defaults.get(attribute))
        sortingList.append(name)
        return tuple(sortingList)

    @classmethod
    def styleName2Numeric(cls, name, attribute):
        values = C.STYLENAME_PREFERRED_VALUES.get(attribute)
        for findName, numeric in values:
            if findName == name:
                return numeric
        return None

    @classmethod
    def getSortedNames(cls, names):
        toSort = []
        for name in names:
            toSort.append(cls.getNameForSorting(name))
        toSort.sort()
        return [x[-1] for x in toSort]

    @classmethod
    def getPrimary(cls, names):
        """
        This is a godawful way to get the primary style from.
        """
        if names:
            names = cls.getSortedNames(names)
            for name in names:
                series, style = FontInfoTX.getSeriesAndStyle(name)
                numericStyleInfo = cls.getNumericStyleInfo(style)
                if len(numericStyleInfo) == 0:
                    return name
            passedAttrs = []
            order = C.STYLENAME_DEFAULT_ORDER[:]
            for attr in order:
                for name in names:
                    series, style = FontInfoTX.getSeriesAndStyle(name)
                    numericStyleInfo = cls.getNumericStyleInfo(style)
                    for passedAttr in passedAttrs:
                        if passedAttr in numericStyleInfo:
                            del numericStyleInfo[passedAttr]
                    if len(numericStyleInfo) == 0:
                        return name
                    else:
                        if 'tags' in numericStyleInfo:
                            del numericStyleInfo['tags']
                passedAttrs.append(attr)
            return names[0]

if __name__ == "__main__":

    styles = [Style('Condensed Regular'), Style('Display Italic')]
    s = Series(styles)
    print(s.styles)

if __name__ == "__main__2":
    basePath = u"/Users/david/Documents/FB/Masters/TypeNetwork"
    #dirPath = basePath
    #if 1 == 1:
    dirs = os.listdir(basePath)
    for dir in dirs:
        dirPath = os.path.join(basePath, dir)
        if os.path.isdir(dirPath):
            paths = File.collect(dirPath)
            pathsToNames = {}
            names = []
            for path in paths:
                name = '-'.join(FontInfoTX.getSeriesAndStyleFromFileName(path))
                pathsToNames[path] = name
                names.append(name)
            print(dir, SeriesTX.getPrimary(names) or "### " + dir)

