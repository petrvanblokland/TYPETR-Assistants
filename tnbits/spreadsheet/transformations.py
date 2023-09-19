# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    transformations.py
#
#    Common mouse & point conversions.

from AppKit import NSMakePoint, NSPoint

def event2MousePoint(view, event):
    # TODO: reuse.
    mouse = event.locationInWindow()
    return mouse2Point(view, mouse)

def mouse2Point(view, mouse):
    # TODO: reuse.
    """Transform the mouse position to an NSPoint."""
    return view.convertPoint_fromView_(mouse, None)

def point2Mouse(view, p):
    # TODO: reuse.
    """Transform the unscaled p to mouse position."""
    return view.convertPoint_toView_(p, None)

def scalePoint(p, scale):
    return NSPoint(p.x * scale, p.y * scale)

def scaledPoint2Cell(sp, cellXToScaledX, sy, scale):
    """Transform the scaled point to cellID (cellX, cellY) tuple."""
    return scaledX2CellX(sp.x, cellXToScaledX), scaledY2CellY(sp.y, sy, scale)

def scaledX2CellX(sx, cellXToScaledX):
    cellX = None

    for ix, value in sorted(cellXToScaledX.items()):
        if sx > value:
            cellX = ix
        else:
            break

    return cellX

def scaledY2CellY(sy, scale, origin_y, leading, numberOfRows):
    """Converts the cellY to scaled Y position. Clips the resulting index
    between (0, numberOfRows - 1)."""
    if sy < origin_y:
        return 0

    cellY = int((sy - origin_y) / (leading * scale))

    if 0 <= cellY < numberOfRows:
        return cellY
    elif cellY >= numberOfRows:
        if numberOfRows > 0:
            return numberOfRows - 1
        else:
            return 0

def cellY2ScaledY(iy, scale, origin_y, leading):
    """Converts row cellY index to scaled y-value."""
    if iy is not None:
        return origin_y + (iy * leading * scale)

def cellX2ScaledX(ix, scale, origin_x, leading):
    """Converts row cellY index to scaled y-value."""
    if ix is not None:
        return origin_x + (ix * leading * scale)
