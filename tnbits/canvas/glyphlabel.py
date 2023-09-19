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
#    glyphlabel.py
#

from AppKit import NSAttributedString, NSGraphicsContext
from CoreText import kCTFontNameAttribute, kCTFontAttributeName, \
        CTFontDescriptorCreateWithAttributes, \
        CTFontDescriptorCreateCopyWithVariation, \
        CTFontCreateWithFontDescriptor, CTLineCreateWithAttributedString, \
        CGContextSetTextPosition, CTLineDraw
from tnbits.canvas.bezierpath import CanvasBezierPath
from tnbits.canvas.widget import Widget
from tnbits.base.constants.colors import *

M = [1, 0, 0, 1, 0, 0]

def tagToInt(tag):
    assert len(tag) == 4
    i = 0

    for c in tag:
        i <<= 8
        i |= ord(c)

    return i

class GlyphLabel(Widget):
    """Base class."""

    def __init__(self, controller, kit, glyphName, fontSize, point, r, location,
            backgroundColor, labelSize='regular'):
        self.glyphName = glyphName
        self.point = point
        self.setFontSize(fontSize)
        self.location = location
        self.backgroundColor = backgroundColor
        self.labelSize = labelSize
        super(GlyphLabel, self).__init__(controller, kit)

    def setFontSize(self, fontSize):
        self.fontSize = fontSize
        self.r = fontSize * 1.33

    def setPoint(self, point):
        self.point = point

    def setGlyph(self, glyphName):
        self.glyphName = glyphName

class FTGlyphLabel(GlyphLabel):
    """Glyph widget to be used on a canvas. FontTools based."""

    def __init__(self, controller, kit, glyphName, glyphSet, upem, fontSize,
            location, point, r=None, backgroundColor=None, labelSize='regular'):
        self.glyphSet = glyphSet
        self.upem = upem
        super(FTGlyphLabel, self).__init__(controller, kit, glyphName, fontSize, point,
                r, location, backgroundColor, labelSize=labelSize)

    def draw(self):
        self.drawBackground()
        self.drawGlyph()

    def drawBackground(self, factor=1.2):
        """Draws a circle background behind the glyph."""
        mx, my = self.point
        x = mx - 0.5 * self.fontSize * factor
        y = my - 0.5 * self.fontSize * factor
        w = self.fontSize * factor
        h = self.fontSize * factor
        self.kit.drawCircle(x, y, w, h, fillColor=self.backgroundColor)

    def drawGlyph(self):
        """Draws the glyph in a BezierPath and displays it."""
        x, y = self.point
        self.glyphSet.setLocation(self.location) # Not needed?
        g = self.glyphSet[self.glyphName]
        scale = self.fontSize / float(self.upem)
        path = CanvasBezierPath(glyphSet=self.glyphSet)
        g.draw(path)
        path.scale(scale)
        x0, y0, x1, y1 = path.bounds()
        w = x1 - x0
        h = y1 - y0
        path.translate(x - w / 2, y - h / 2)
        blackColor.set()
        path._path.fill()

class CTGlyphLabel(GlyphLabel):
    """Glyph widget to be used on a canvas. CoreText based."""

    def __init__(self, controller, kit, glyphName, fontName, fontSize,
            location, point, r=None, backgroundColor=None, labelSize='regular'):
        self.fontName = fontName
        super(CTGlyphLabel, self).__init__(controller, kit, glyphName, fontSize, point,
                r, location, backgroundColor, labelSize=labelSize)

    def getDefaultDescriptor(self):
        attrs = {kCTFontNameAttribute: self.fontName}
        return CTFontDescriptorCreateWithAttributes(attrs)

    def getVarFont(self):
        descriptor = self.getDefaultDescriptor()

        # Updates descriptor with location values.
        for tag, value in self.location.items():
            descriptor = CTFontDescriptorCreateCopyWithVariation(descriptor,
                    tagToInt(tag), value)

        return CTFontCreateWithFontDescriptor(descriptor, self.fontSize, M)

    def setLocation(self):
        pass

    def draw(self):
        self.drawBackground()
        self.drawGlyph()

    def drawGlyph(self):
        context = NSGraphicsContext.currentContext().graphicsPort()
        font = self.getVarFont()
        attrs = {kCTFontAttributeName: font}
        s = NSAttributedString.alloc().initWithString_attributes_(self.glyphName, attrs)
        line = CTLineCreateWithAttributedString(s)
        x, y = self.point

        # TODO: Approx. position, use advance for actual glyph size.
        CGContextSetTextPosition(context, x - self.fontSize / 3, y - self.fontSize / 3)
        CTLineDraw(line, context)

    def drawBackground(self, factor=1.2):
        """Draws a circle background behind the glyph."""
        mx, my = self.point
        x = mx - 0.5 * self.fontSize * factor
        y = my - 0.5 * self.fontSize * factor
        w = self.fontSize * factor
        h = self.fontSize * factor
        self.kit.drawCircle(x, y, w, h, fillColor=self.backgroundColor)
