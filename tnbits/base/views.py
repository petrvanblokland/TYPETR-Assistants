# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    views.py
#
from vanilla import HorizontalLine, Box, TextBox
from tnbits.base.text import *
from tnbits.base.constants.colors import *
from tnbits.base.constants.tool import *

def addTitle(view, pos, label, inverse=False):
    """Adds an attributed title with an underline to a view."""
    x, y, w, h = pos
    nsString = getAttributedTitle(label.title())
    setattr(view, label + 'Title', TextBox(pos, nsString))

    if not inverse:
        y += h

    addHR(view, (x, y, w, 1), label, UILightBlue)

    if inverse:
        y -= PADDING
    else:
        y += PADDING

    return y

def addHR(view, pos, label, color):
    hl = HorizontalLine(pos)
    box = hl.getNSBox()
    box.setBoxType_(4)
    box.setBorderColor_(color)
    setattr(view, label + 'Line', hl)

def addBox(view, pos, label, color, borderColor=None):
    hlb = Box(pos)
    box = hlb.getNSBox()
    box.setBoxType_(4)
    box.setFillColor_(color)
    box.setBorderColor_(borderColor)
    setattr(view, label + 'OuterLine', hlb)
