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
#    kit.py
#

from AppKit import NSMakeRect, NSColor, NSBezierPath, \
        NSForegroundColorAttributeName, NSFontAttributeName, NSFont, \
        NSAttributedString
from tnbits.base.constants.colors import *
from tnbits.canvas.bezierpath import CanvasBezierPath
from tnbits.canvas.pin import Pin
from tnbits.canvas.slider import Slider
from tnbits.canvas.glyphlabel import GlyphLabel

class CanvasKit(object):
    """Provides reusable functions to draw graphics on a canvas. Companion to
    tnbits.canvas but also can be used on other self-drawing NSViews."""

    def __init__(self):
        # Cache.
        self.objects = []
        self.attributedStrings = {}
        self.labelPositions = {}
        self.selected = []

    def resetStrings(self):
        self.attributedStrings = {}

    def add(self, o):
        """Stores all existing objects in a list."""
        self.objects.append(o)

    def select(self, o):
        self.selected.append(o)

    def deselect(self, o):
        self.selected.remove(o)

    def clearSelected(self):
        for o in self.selected:
            o.deselect()

    def _get_sliders(self):
        sliders = []

        for o in self.objects:
            if isinstance(o, Slider):
                sliders.append(o)

        return sliders

    sliders = property(_get_sliders)

    def _get_pins(self):
        pins = []

        for o in self.objects:
            if isinstance(o, Pin):
                pins.append(o)

        return pins

    pins = property(_get_pins)

    def _get_labels(self):
        labels = []

        for o in self.objects:
            if isinstance(o, GlyphLabel):
                labels.append(o)

        return labels

    labels = property(_get_labels)

    def clear(self):
        self.objects = []

    def drawCircle(self, x, y, w, h, fillColor=None, strokeColor=None, strokeWidth=None):
        """Draws a circular path."""
        rect = NSMakeRect(x, y, w, h)
        path = NSBezierPath.bezierPathWithOvalInRect_(rect)

        if fillColor:
            fillColor.set()
            path.fill()

        if strokeColor:
            strokeColor.set()
            path.stroke()

    def drawLine(self, p0, p1, color=blackColor, width=0.5):
        path = NSBezierPath.bezierPath()
        if width:
            path.setLineWidth_(width)
        path.moveToPoint_(p0)
        path.lineToPoint_(p1)
        color.set()
        path.stroke()
        return path

    def drawRectangle(self, x, y, w, h, fillColor=whiteColor,
            strokeColor=lightGreyColor, width=0.5):
        # FIXME: width should be strokeWidth.
        rect = NSMakeRect(x, y, w, h)
        path = NSBezierPath.bezierPathWithRect_(rect)

        if fillColor:
            fillColor.set()
            path.fill()

        if width:
            path.setLineWidth_(width)

        if strokeColor:
            strokeColor.set()
            path.stroke()

    def drawGroupMarker(self, x, y, w, h, t=0, fillColor=yellowColor,
            strokeColor=None, width=0.5, left=True):

        y1 = y + h
        dx = y * t
        dx1 = y1 * t

        if left:
            p0 = (x + dx, y)
        else:
            p0 = (x + dx + w, y)

        p1 = (x + dx1, y1)
        p2 = (x + dx1 + w, y1)

        path = NSBezierPath.bezierPath()
        path.moveToPoint_(p0)
        path.lineToPoint_(p1)
        path.lineToPoint_(p2)

        if fillColor:
            fillColor.set()
            path.fill()

        path.setLineWidth_(w)

        if strokeColor:
            strokeColor.set()
            path.stroke()

    # Slider.
    # TODO: use Slider class.

    def drawSlider(self, p0, p1, w=12, color=None,
        # DEPRECATED: implemented in Slider class.
            border=None, isCurrent=False, defaultPct=None, r=4):
        if isCurrent:
            self.drawSliderPath(p0, p1, w + 2, cyanColor)
        elif border:
            self.drawSliderPath(p0, p1, w + 2, border)

        self.drawSliderPath(p0, p1, w, color)

        if defaultPct:
            x0, y0 = p0
            x1, y1 = p1
            x = x0 + (x1 - x0) * defaultPct / 100
            y = y0 + (y1 - y0) * defaultPct / 100
            self.drawCircle(x - r, y - r, 2*r, 2*r, fillColor=darkGrayColor)

    def drawSliderPath(self, p0, p1, w, color):
        path = NSBezierPath.bezierPath()
        path.moveToPoint_(p0)
        path.lineToPoint_(p1)
        color.set()
        path.setLineWidth_(w)
        path.stroke()
        x, y = p0
        self.drawCircle(x - w/2, y - w/2, w, w, fillColor=color)
        x, y = p1
        self.drawCircle(x - w/2, y - w/2, w, w, fillColor=color)

    def drawSliderButton(self, x, y, r=4, color=None):
        self.drawCircle(x - r + 1, y - r - 1, 2*r, 2*r, strokeColor=darkGrayColor)
        self.drawCircle(x - r, y - r, 2*r, 2*r, fillColor=whiteColor, strokeColor=lightGrayColor)

        if color:
            self.drawCircle(x - r/ 2, y - r /2, r, r, fillColor=color, strokeColor=lightGrayColor)

    # Glyph Var Preview.
    # TODO: move to separate class, add callbacks etc.
    # Store bounds, width, height, etc.

    def drawGlyphVariation(self, mx, my, glyphSet, glyphName, fontSize, upem,
            location, background=True, backgroundColor=None):
        """Draws the variation of a glyph."""
        if background:
            self.drawGlyphBackground(mx, my, fontSize, backgroundColor=backgroundColor)

        glyphSet.setLocation(location)
        g = glyphSet[glyphName]
        scale = fontSize / float(upem)
        self.drawGlyphPath(glyphSet, g, mx, my, location, scale=scale, fillColor=blackColor)

    def drawGlyphBackground(self, mx, my, fontSize, factor=1.2,
            backgroundColor=whiteColor):
        """Draws a circle background behind the glyph."""
        x = mx - 0.5 * fontSize * factor
        y = my - 0.5 * fontSize * factor
        w = fontSize * factor
        h = fontSize * factor
        self.drawCircle(x, y, w, h, fillColor=backgroundColor)

    def drawGlyphPath(self, glyphSet, g, x, y, location=None, scale=0.1, fillColor=None):
        """Draws the glyph in a BezierPath and displays it."""
        path = CanvasBezierPath(glyphSet=glyphSet)
        g.draw(path)
        path.scale(scale)
        x0, y0, x1, y1 = path.bounds()
        w = x1 - x0
        h = y1 - y0
        path.translate(x - w / 2, y - h / 2)
        fillColor.set()
        path._path.fill()

    def drawText(self, text, x, y, fontSize=11, color=None, padding=4, align='left'):
        if color is None:
            color = blackColor

        # Caching.
        if not text in self.attributedStrings:
            attributes = {
                NSForegroundColorAttributeName: color,
                NSFontAttributeName: NSFont.systemFontOfSize_(fontSize)
            }
            self.attributedStrings[text] = NSAttributedString.alloc().initWithString_attributes_(text, attributes)

        s = self.attributedStrings[text]
        width, height = s.size()
        x0 = x - padding
        y0 = y - padding
        w = width + 2 * padding
        h = height + 2 * padding

        if align == 'center':
            x0 -= w / 2
        elif align == 'right':
            x0 -= w

        rect0 = ((x0, y0), (w, h))

        '''
        # Shift to find an open spot.
        while self.labelIntersects(rect0) and i < 10:
            x0, y0 = self.getLabelCoordinates(rect0)
            rect0 = (x0, y0, w, h)
            i += 1
        self.labelPositions.append(rect0)
        '''

        s.drawInRect_(rect0)
