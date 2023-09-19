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
#     varmath.py
#

#NOTE: normalized minimum values sometimes -1 now?
# using fontTools.varLib.models normalizeLocation()

from math import pi, sin, cos
from tnbits.toolbox.mathematics import Mathematics

def getDefaultAxisRatio(axisTag, axesDict):
    # DEPRECATED?
    v = axesDict[axisTag]
    minValue, defaultValue, maxValue = v
    return values2ratio(minValue, defaultValue, maxValue)

def getDefaultLocation(axesDict):
    """Returns a dictionary that contains all axes set to a normalized default
    values."""
    d = {}

    if axesDict is None:
        return

    for axisTag, values in axesDict.items():
        minValue, defaultValue, maxValue = values
        d[axisTag] = defaultValue

    return d

def angle2XY(angle, r):
    """Calculates the XY position for a given angle (degrees) and r relative
    to the origin."""
    return cos(angle / 180.0 * pi) * r, sin(angle / 180.0 * pi) * r

def values2percentage(minValue, value, maxValue):
    # DEPRECATED?
    return (value - minValue) / ((maxValue - minValue) / 100.0)

def values2ratio(minValue, value, maxValue):
    # DEPRECATED?
    return (value - minValue) / (maxValue - minValue)

def distributedAngles(d):
    """Calculates initial axis distribution over variation circle."""
    angles = {}
    a = 0

    for axis in d.keys():
        angles[axis] = a
        a += 360.0 / len(d)

    return angles
