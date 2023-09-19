# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    debug.py
#

import traceback
from random import random
from AppKit import NSColor, NSBezierPath

def drawUpdateRect(rect):
    """Draws a randomly colored rectangle to show where the screen is
    updated. For debugging purposes."""
    if rect is not None:
        try:
            C = 0.85
            R = 1 - C
            r = C+random() * R
            g = C+random() * R
            b = C+random() * R
            NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, 1).set()
            path = NSBezierPath.bezierPathWithRect_(rect)
            path.fill()
            NSColor.redColor().set()
            path.stroke()
        except Exception as e:
            print(traceback.format_exc())
