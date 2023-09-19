# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    bezierpathfactory.py
#
from fontTools.pens.cocoaPen import CocoaPen

def NSBezierPathFactory(glyph, font):
    pen = CocoaPen(font)
    glyph.draw(pen)
    return pen.path
