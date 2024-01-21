# -*- coding: UTF-8 -*-
#
#    qbqconverter.py
#

#from tnbits.constants import Constants as C
#from tnbits.objects.point import Point, SpacePoint
#from tnbits.toolbox.transformer import TX
#from tnbits.model.objects.glyph import getContours

DEBUG = False

"""
Quadratic <-> Bézier conversion.
"""

POINTTYPE_BEZIER = 'curve'
POINTTYPE_QUADRATIC = 'qcurve'

FACTOR = 1.340   # This estimated value gives amazingly accurate conversion.
FACTORS = {
    POINTTYPE_QUADRATIC: 1.0/FACTOR,
    POINTTYPE_BEZIER: FACTOR
}

def factorizeOffCurve(onCurve, offCurve, factor, scale=1):
    dx = offCurve.x - onCurve.x
    dy = offCurve.y - onCurve.y
    offCurve.x = int(round((onCurve.x + dx * factor) * scale))
    offCurve.y = int(round((onCurve.y + dy * factor) * scale))
    if scale != 1:
        onCurve.x = int(round(onCurve.x * scale))
        onCurve.y = int(round(onCurve.y * scale))

#def b2q(x1, y1, x2, y2):
#    return x1 + (x2 - x1)/FACTOR, y1 + (y2 - y1)/FACTOR

#def q2b(x1, y1, x2, y2):
#    return x1 + (x2 - x1)*FACTOR, y1 + (y2 - y1)*FACTOR

#def singleq2b(x1, y1, x2, y2):
#    return x1 + (x2 - x1)/2, y1 + (y2 - y1)/2

def factorizeSegment(position, segment, fromType, toType, scale=1):
    if segment[-1].type == fromType:
        f = FACTORS[toType]
        if len(segment) == 2:
            # One BCP missing, interpret bcp connected to first point
            factorizeOffCurve(position, segment[0], f, scale)
            segment[-1].type = toType

        elif len(segment) == 3:
            # 2 offCurve's defined. Move them
            factorizeOffCurve(position, segment[0], f)
            factorizeOffCurve(segment[2], segment[1], f, scale)
            segment[-1].type = toType
            segment[-2].type = toType

def factorize(g, fromType, toType, scale=1):
    u"""Factorize the length of the segment off-curves to the toType format."""
    for contour in g.contours:
        segments = contour.segments
        position = segments[-1][-1] # Position of segment start
        for segment in segments:
            factorizeSegment(position, segment, fromType, toType, scale)
            position = segment[-1] # Set to start position of next segment

def bezier2Quadratic(g, scale=1):
    factorize(g, POINTTYPE_BEZIER, POINTTYPE_QUADRATIC, scale)

def quadratic2Bezier(g, scale=1):
    factorize(g, POINTTYPE_QUADRATIC, POINTTYPE_BEZIER, scale)

def isQuadratic(g):
    for contour in g.contours:
        for p in contour.points:
            if p.type == POINTTYPE_QUADRATIC:
                return True
    return False

def isBezier(glyph):
    for contour in g.contours:
        for p in contour.points:
            if p.type == POINTTYPE_BEZIER:
                return True
    return False

def isRounded(g):
    for contour in g.contours:
        for p in contour.points:
            if p.x != round(p.x) or p.y != round(p.y):
                return False
    return True
