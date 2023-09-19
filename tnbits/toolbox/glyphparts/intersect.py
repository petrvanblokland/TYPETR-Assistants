# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
class SimplePoint(object):
    def __init__(self, pt):
        try:
            x = pt.x
            y = pt.y
        except:
            x, y = pt
        self.x = x
        self.y = y

    def __repr__(self):
        return "<SimplePoint x=%.2f, y=%.2f>" %(self.x, self.y)

def pointOnLine(p1, p2, value):
    p1 = SimplePoint(p1)
    p2 = SimplePoint(p2)
    return SimplePoint((p1.x + (p2.x-p1.x)*value, p1.y + (p2.y-p1.y)*value))

def pointOnACurve(p1, c1, c2, p2, value):
    p1 = SimplePoint(p1)
    c1 = SimplePoint(c1)
    c2 = SimplePoint(c2)
    p2 = SimplePoint(p2)
    dx = p1.x
    cx = (c1.x - dx) * 3.0
    bx = (c2.x - c1.x) * 3.0 - cx
    ax = p2.x - dx - cx - bx

    dy = p1.y
    cy = (c1.y - dy) * 3.0
    by = (c2.y - c1.y) * 3.0 - cy
    ay = p2.y - dy - cy - by

    mx = ax*(value)**3 + bx*(value)**2 + cx*(value) + dx
    my = ay*(value)**3 + by*(value)**2 + cy*(value) + dy

    return SimplePoint((mx, my))

def pointOnACurve(p1, c1, c2, p2, value):
    p1 = SimplePoint(p1)
    c1 = SimplePoint(c1)
    c2 = SimplePoint(c2)
    p2 = SimplePoint(p2)
    dx = p1.x
    cx = (c1.x - dx) * 3.0
    bx = (c2.x - c1.x) * 3.0 - cx
    ax = p2.x - dx - cx - bx

    dy = p1.y
    cy = (c1.y - dy) * 3.0
    by = (c2.y - c1.y) * 3.0 - cy
    ay = p2.y - dy - cy - by

    mx = ax*(value)**3 + bx*(value)**2 + cx*(value) + dx
    my = ay*(value)**3 + by*(value)**2 + cy*(value) + dy

    return SimplePoint((mx, my))


def IntersectGlyphWithLine(glyph, beam, canHaveComponent=False, addSideBearings=False):
    """
    Intersect a glyph with a line.
    Returning a list of intersections.

    >>> IntersectGlyphWithLine(myGlyph, ((100, 50), (800, 50)), canHaveComponent=True, addSideBearings=True)
    [(658.0, 50.0), (500.0, 50.0)]

    """

    nakedGlyph = glyph.naked()
    intersects = nakedGlyph.getRepresentation("doodle.Beam", beam=beam, canHaveComponent=canHaveComponent)

    if addSideBearings:
        return intersects.lefMarginIntersection + intersects.intersects + intersects.rightMarginIntersection
    else:
        return intersects.intersects
