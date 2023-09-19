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
#    preview.py
#
import traceback
from AppKit import NSColor, NSGraphicsContext
from Quartz import CGContextSetTextMatrix, CGAffineTransformIdentity

import os.path
from fontTools.ttLib import TTFont
from vanilla import Group
from tnbits.base.constants.colors import *
from tnbits.canvas.canvas import Canvas
from tnbits.canvas.kit import CanvasKit
from tnbits.canvas.glyphlabel import FTGlyphLabel
from tnbits.canvas.eventhandler import CanvasEventHandler
from tnbits.variations.constants import *
from tnbits.variations.varfontdesignspace import *
from tnbits.variations.varmath import *

class Preview(object):

    ttfont = None
    glyphName = None

    def __init__(self, parent, pos=(0, 0, -0, -0), w=1000, h=1000):
        self.parent = parent
        self.view = Group(pos)
        self.kit = CanvasKit()
        self.canvas = Canvas((0, 0, -0, -0), delegate=self, canvasSize=(w, h),
                acceptsMouseMoved=False, liveResize=False, flipped=False,
                backgroundColor=NSColor.whiteColor())
        self.view.canvas = self.canvas
        self.eventHandler = CanvasEventHandler(self.canvas)
        self.locations = []

    def loadStyle(self, path):
        self.kit.clear()
        self.locations = []
        if not os.path.exists(path):
            return

        self.ttfont = TTFont(path)
        #self.upem = self.style.info.unitsPerEm
        self.upem = 1000
        glyphNames = self.ttfont.getGlyphOrder()
        self.glyphSet = TTVarFontGlyphSet(self.ttfont)
        self.glyphName = glyphNames[1]
        self.setGlyph()

    def setGlyph(self):
        axes = self.glyphSet._axes
        size = 100
        r = size + 20
        x0 = r / 2
        y = r

        # Neutral.
        location = self.getLocation(axes)
        self.locations.append((location, x0 - r / 4, r / 2 - 20, 'neutral'))
        p = (x0, y)
        label = FTGlyphLabel(self, self.kit, self.glyphName, self.glyphSet,
                self.upem, size, location, p, backgroundColor=None)

        for axisTag in axes.keys():
            i = 1

            for v in ('min', 'halfway', 'max'):
                location = self.getLocation(axes, axisTag, v)
                x = x0 + i*r
                self.locations.append((location, x - r / 4, y - r / 2 - 20, '%s %s' % (axisTag, v)))
                p = (x, y)
                label = FTGlyphLabel(self, self.kit, self.glyphName,
                        self.glyphSet, self.upem, size, location, p,
                        backgroundColor=None)
                i += 1

            y += r + 20

    def getLocation(self, axes, axisTag=None, value='default'):
        """Returns a dictionary that contains all axes set to default values.
        """
        d = {}

        if axes is None:
            return

        for key, values in axes.items():
            minValue, defaultValue, maxValue = values
            if key == axisTag:

                if value == 'min':
                    d[key] = minValue
                elif value == 'max':
                    d[key] = maxValue
                elif value =='default':
                    d[key] = defaultValue
                elif value =='halfway':
                    d[key] = (maxValue + minValue) / 2
            else:
                d[key] = defaultValue

        return d

    def drawLocations(self):
        for t in self.locations:
            location, x, y, label = t
            self.drawLocation(location, x, y, label)

    def drawLocation(self, location, x, y, label):
        fs = 9
        leading = 11
        self.kit.drawText(label, x, y, fontSize=fs)
        y -= leading
        s = []
        for key, value in location.items():
            s.append('%s: %s' % (key[0], str(value)))

        s = ', '.join(s)
        self.kit.drawText(s, x, y, fontSize=fs)

    def getView(self):
        return self.view

    def draw(self, rect):
        """Gets graphics context and transforms, translates and scales text
        matrix."""
        context = NSGraphicsContext.currentContext().graphicsPort()
        CGContextSetTextMatrix(context, CGAffineTransformIdentity);

        try:
            self.drawSliders()
            self.drawLabels()
            self.drawLocations()
        except Exception as e:
            print(traceback.format_exc())

    def drawLabels(self):
        for label in self.kit.labels:
            label.draw()

    def drawSliders(self):
        for slider in self.kit.sliders:
            slider.draw()

    # TODO: share in base class.

    def getDesignSpace(self):
        return self.getController().getDesignSpace()

    def getFamily(self):
        return self.getController().family

    def getController(self):
        return self.parent.controller

    def update(self):
        ds = self.getDesignSpace()

        if ds:
            p = ds.getVarPath()
            self.loadStyle(p)
            self.canvas.update()
