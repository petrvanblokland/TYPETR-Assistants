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
#    text.py
#
from AppKit import NSFontAttributeName, NSFont, NSForegroundColorAttributeName, \
    NSAttributedString
from tnbits.base.constants.colors import *
from tnbits.base.constants.tool import *

attributesStrings = {
    NSFontAttributeName: NSFont.systemFontOfSize_(11),
    NSForegroundColorAttributeName: whiteColor
}

attributesTitles = {
    NSFontAttributeName: NSFont.boldSystemFontOfSize_(11),
    NSForegroundColorAttributeName: UILightBlue
}

def getSystemFont(style, fontSize):
    # System fonts.
    if style == 'regular':
        return NSFont.systemFontOfSize_(fontSize)
    elif style == 'bold':
        return NSFont.boldSystemFontOfSize_(fontSize)

def getAttributedTitle(title):
    attrs = attributesTitles
    return NSAttributedString.alloc().initWithString_attributes_(title, attrs)

def getAttributedString(title):
    attrs = attributesStrings
    return NSAttributedString.alloc().initWithString_attributes_(title, attrs)

def listFonts():
    pass
