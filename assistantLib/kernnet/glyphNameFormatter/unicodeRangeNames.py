# -*- coding: UTF-8 -*-
from __future__ import print_function
from glyphNameFormatter.data import unicodeRangeNames

import rangeProcessors
reload(rangeProcessors)


unicodePlaneNames = {
    (0x00000,   0x0FFFF): (u"Basic Multilingual Plane", ),
    (0x10000,   0x1FFFF): (u"Supplementary Multilingual Plane", ),
    (0x20000,   0x2FFFF): (u"Supplementary Ideographic Plane"),
    (0x30000,   0xDFFFF): (u"Plane 3 - 13, unassigned", ),
    (0xE0000,   0xEFFFF): (u"Supplement­ary Special-purpose Plane", ),
    (0xF0000,   0x10FFFF): (u"Supplement­ary Private Use Area", ),
}


def getRangeName(value):
    for a, b in unicodeRangeNames.keys():
        if a <= value <= b:
            return unicodeRangeNames[(a, b)]
    return None


def getRangeAndName(value):
    for a, b in unicodeRangeNames.keys():
        if a <= value <= b:
            return (a, b), unicodeRangeNames[(a, b)]
    return None, None


def getRangeByName(rangeName):
    for r, name in unicodeRangeNames.items():
        if rangeName == name:
            return r
    return None


def getAllRangeNames():
    names = []
    ranges = unicodeRangeNames.keys()
    ranges.sort()
    for r in ranges:
        names.append(unicodeRangeNames[r])
    return names


def getPlaneName(value):
    for a, b in unicodePlaneNames.keys():
        if a <= value <= b:
            return unicodePlaneNames[(a, b)][0]
    return None


def getAllPlaneNames():
    names = []
    k = unicodePlaneNames.keys()
    k.sort()
    for r in k:
        names.append(unicodePlaneNames[r])
    return names


def rangeNameToModuleName(rangeName):
    return rangeName.lower().replace(" ", "_").replace("-", "_")


def getRangeProcessor(value):
    name = getRangeName(value)
    if name is None:
        return None
    return getRangeProcessorByRangeName(name)


def getRangeProcessorByRangeName(rangeName):
    import importlib
    moduleName = rangeNameToModuleName(rangeName)
    module = None
    try:
        module = importlib.import_module('glyphNameFormatter.rangeProcessors.%s' % moduleName)
    except ImportError:
        # return the default
        module = rangeProcessors
    try:
        return getattr(module, "process")
    except AttributeError:
        print(moduleName)
        return None
