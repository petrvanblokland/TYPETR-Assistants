#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     variationdesignspace.py
#
# FIXME: UFO design space? Should be moved to Floq Model.

from mutatorMath.ufo.document import DesignSpaceDocumentWriter, DesignSpaceDocumentReader
from defcon.objects.font import Font

import xml.etree.ElementTree as ET

class VariationDesignSpace(object):
    """
    TODO: What about masters? one master for each min, default, max values? one
    only? must also be default in other axes?
    TODO: Write some unit tests.
    TODO: Write a function to output all possible location extremes
    (instances?)
    TODO: Check Just's Axis object, also look at mutatorMath Location object
    and DesignSpace object.
    """

    def __init__(self):

        self.axes = []
        self.sources = []
        self.instances = []

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def _getDefaultLocation(self):
        defaultLocation = {}
        for axis in self.axes:
            defaultLocation[axis.tag] = axis.defaultValue
        return defaultLocation

    def _getDefaultSources(self):
        defaultLocation = self._getDefaultLocation()
        print('Default location', defaultLocation)
        defaultSources = [source for source in self.sources if defaultLocation == source.location]
        print(len(self.sources), self.sources[0])
        print(defaultSources)
        return defaultSources

    def _setDefaultSources(self):
        for source in self.sources:
            source.copyLib = False
            source.copyGroups = False
            source.copyInfo = False
            source.copyFeatures = False
        for source in self._getDefaultSources():
            source.copyLib = True
            source.copyGroups = True
            source.copyInfo = True
            source.copyFeatures = True

    def _updateSourceLocation(self): # TODO find better name
        axes = self.axes
        for source in self.sources:
            for axis in axes:
                if axis.tag not in source.location:
                    source.location[axis.tag] = axis.defaultValue

    def validateDesignSpace(self): # TODO where and when should this happen?
        assert self.axes, "No axis"
        axisTags = [axis.tag for axis in self.axes]
        assert len(axisTags) == len(set(axisTags)), "Axis tags not unique: %s" % axisTags
        assert self.sources, "No source"
        self._updateSourceLocation()
        defaultSources = self._getDefaultSources()
        assert defaultSources, "No default source: %s" % self._getDefaultLocation()
        if len(defaultSources) > 1:
            print("### Warning: More than one default source:")
            for defaultSource in defaultSources:
                print('\t', defaultSource.path)
        ###defaultSource = defaultSources[0]
        self._setDefaultSources()

    def _tag2NameLocation(self, location):
        loc = {}
        for tag, value in location.items():
            name = self.getAxisName(tag)
            if name:
                loc[name] = value
        return loc

    def getAxisName(self, tag):
        for axis in self.axes:
            if axis.tag == tag:
                return axis.name
        else:
            return None

    def getAxisMap(self):
        axisMap = {}
        for axis in self.axes:
            axisMap[axis.name] = (axis.tag, axis.name)
        return axisMap

    def writeDesignSpace(self, path):
        document = DesignSpaceDocumentWriter(path)

        """
        for axis in self.axes:
            document.addAxis(
                axis.tag,
                axis.name,
                axis.minValue,
                axis.maxValue,
                axis.defaultValue,
                warpMap=axis.warpMap
            ) # tag, name, minimum, maximum, default, warpMap=None
        """
                # We need to add labelNames here because addAxis doesn't
                # include it... need to use
                # https://github.com/LettError/designSpaceDocument
        for axisObject in self.axes:
            axisElement = ET.Element('axis')
            axisElement.attrib['tag'] = axisObject.tag
            axisElement.attrib['name'] = axisObject.name
            axisElement.attrib['minimum'] = str(axisObject.minValue)
            axisElement.attrib['maximum'] = str(axisObject.maxValue)
            axisElement.attrib['default'] = str(axisObject.defaultValue)
            for languageCode, labelName in axisObject.labelNames.items():
                languageElement = ET.Element('labelname')
                languageElement.attrib[u'xml:lang'] = languageCode
                languageElement.text = labelName
                axisElement.append(languageElement)
            if axisObject.warpMap:
                for inputValue, outputValue in axisObject.warpMap:
                    mapElement = ET.Element('map')
                    mapElement.attrib['input'] = str(inputValue)
                    mapElement.attrib['output'] = str(outputValue)
                    axisElement.append(mapElement)
            document.root.findall('.axes')[0].append(axisElement)

        for source in self.sources:
            location = self._tag2NameLocation(source.location)
            document.addSource(
                source.path,
                source.name,
                location,
                copyLib=source.copyLib,
                copyGroups=source.copyGroups,
                copyInfo=source.copyInfo,
                copyFeatures=source.copyFeatures,
                muteKerning=source.muteKerning,
                muteInfo=source.muteInfo,
                mutedGlyphNames=source.mutedGlyphNames,
                familyName=source.familyName,
                styleName=source.styleName
            )
        for instance in self.instances:
            location = self._tag2NameLocation(source.location)
            document.startInstance(
                name=instance.name,
                location=location,
                familyName=instance.familyName,
                styleName=instance.styleName,
                fileName=instance.fileName,
                postScriptFontName=instance.postScriptFontName,
                styleMapFamilyName=instance.styleMapFamilyName,
                styleMapStyleName=instance.styleMapStyleName,
            )
            #document.writeGlyph
            #document.writeInfo
            #document.writeKerning
            document.endInstance()
        document.save()

class Source(object):
    """
    Source
    * location is a dictionary of axisTag:value
    """
    def __init__(self, path, name, location):
        self.path = path
        self.name = name
        self.location = location

        self.copyLib = False
        self.copyGroups = False
        self.copyInfo = False
        self.copyFeatures = False
        self.muteKerning = False
        self.muteInfo = False
        self.mutedGlyphNames = False

        self._font = Font(path)
        # TODO assert wrong path?
        self.familyName = self._font.info.familyName
        self.styleName = self._font.info.styleName

    def getFont(self):
        return self._font

    def __repr__(self):
        return "<Source: %s>" % self.name

"""
fvar NamedInstance
coordinates = instance.location
name = instance.styleName
psname = instance.postScriptFontName
"""

class Instance(object):
    """
    Instance
    * location is a dictionary of axisTag:value
    """
    def __init__(self, postScriptFontName, styleName, location):
        self.name = None
        self.location = location
        self.familyName = None
        self.styleName = styleName
        self.fileName = None
        self.postScriptFontName = postScriptFontName
        self.styleMapFamilyName = None
        self.styleMapStyleName = None

    def __repr__(self):
        return "<Instance: %s>" % self.styleName

class Axis(object):
    """Axis"""

    def __init__(self, name, tag, minValue, defaultValue, maxValue,
            labelNames={}, warpMap=None):
        assert isinstance(name, str),  "Axis name must be a string"
        assert isinstance(tag, str),  "Axis '%s' tag must be a string" % name
        assert len(tag) == 4, "Axis '%s' tag must be a string of four ASCII characters" % name
        assert minValue <= defaultValue <= maxValue, "Axis '%s' defaultValue must be in range minValue maxValue" % name
        self.name = name
        self.tag = tag
        self.minValue = minValue
        self.defaultValue = defaultValue
        self.maxValue = maxValue
        self.labelNames = labelNames # e.g. labelNames[u'en'] = u"Weight"
        # TODO:
        # avar axis segment mapping
        # https://www.microsoft.com/typography/otspec/avar.htm
        self.warpMap = warpMap

    def __repr__(self):
        return "<Axis: %s [%s, %s, %s]>" % (self.name, self.minValue, self.defaultValue, self.maxValue)
