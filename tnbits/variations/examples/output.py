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
#     output.py
#
# FIXME: DEPRECATED?
from tnbits.toolbox.transformer import TX
from designSpaceDocument import DesignSpaceDocument, SourceDescriptor, \
    InstanceDescriptor, AxisDescriptor
from tnbits.model.objects.style import getAxes, getDeltaLocations


def writeDesignSpace(style):
    """Writes design space to file next to UFO."""
    familyVarName = familyName = style.info.familyName

    if not familyVarName.endswith('Var'):
        familyVarName += 'Var'

    familyPath = TX.path2FamilyDir(style.path)
    designSpacePath = '%s/%s.designspace' % (familyPath, familyVarName)
    axes = []

    for axisName, axis in getAxes(style).items():
        if axis['enabled']:
            axes.append(dict(minimum=axis['minValue'],
                maximum=axis['maxValue'], default=axis['defaultValue'],
                name=axis['tag'], tag=axis['tag'], map=[],
                labelNames=dict(en=axis['name'])))

    instances = []
    doc = DesignSpaceDocument()

    for deltaLocName, deltaLocation in getDeltaLocations(style).items():
        if not deltaLocation['axisLocations']:
            continue

        axisLocations = {}

        for tag, axisValue in deltaLocation['axisLocations'].items():
            axisLocations[tag] = axisValue['value']

        d = dict(location=axisLocations, styleName=deltaLocName,
                familyName=familyVarName)
        instances.append(d)
        fileName = '%s-%s.ufo' % (familyName, deltaLocName.replace(' ', '_'))
        s = SourceDescriptor()
        s.path = '%s/%s' % (familyPath, fileName)
        s.name = fileName

        # Copies the font.info from the neutral font.
        s.copyInfo = deltaLocation.get('neutral')
        s.location = axisLocations
        s.familyName = familyName
        s.styleName = deltaLocName
        doc.addSource(s)

    for instance in instances:
        i = InstanceDescriptor()
        i.location = instance["location"]
        i.familyName = instance["familyName"]
        i.styleName = instance["styleName"]
        doc.addInstance(i)

    for axis in axes:
        a = AxisDescriptor()
        a.minimum = axis["minimum"]
        a.maximum = axis["maximum"]
        a.default = axis["default"]
        a.name = axis["name"]
        a.tag = axis["tag"]

        for languageCode, labelName in axis["labelNames"].items():
                a.labelNames[languageCode] = labelName
        a.map = axis["map"]
        doc.addAxis(a)

    doc.write(designSpacePath)
    print('Saved file %s' % designSpacePath)
