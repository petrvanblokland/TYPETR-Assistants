# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     qamath.py
#

from math import sqrt
import traceback

"""
Math functions to be used by quality assurance tools.
"""

def getSortedGlyphNames(style):
    """Where `style` is a DefCon font or DoodleFont.
    FIXME: incompatible with latest DefCon unicodeData.
    """
    keys = sorted(style.keys())

    try:
        ud = style.unicodeData
        l = ud.sortGlyphNames(keys)
    except Exception as e:
        print(traceback.format_exc())
        return keys

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

def lineIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
    div = det(xdiff, ydiff)

    if div == 0:
       return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def isBetween(a, c, b):
    return distance(a, c) + distance(c, b) == distance(a, b)

def getOffset(c):
    """
    Gets a tranformation from a DoodleComponent and calculates an offset tuple.
    """
    offsetX, offsetY = c.transformation[4], c.transformation[5]
    return (offsetX * -1, offsetY * -1)

