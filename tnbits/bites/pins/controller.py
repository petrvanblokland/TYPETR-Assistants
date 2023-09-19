# -*- coding: UTF-8 -*- # -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    controller.py
#
import traceback
from AppKit import NSColor, NSGraphicsContext
from Quartz import CGContextSetTextMatrix, CGAffineTransformIdentity

from tnbits.model import model
from tnbits.model.storage.otfstorage import OTFStorage
from tnbits.base.constants.tool import *
from tnbits.base.constants.colors import *
from tnbits.base.controller import BaseController
from tnbits.canvas.canvas import Canvas
from tnbits.canvas.kit import CanvasKit
from tnbits.canvas.pin import Pin
from tnbits.canvas.slider import Slider
from tnbits.canvas.glyphlabel import CTGlyphLabel, FTGlyphLabel
from tnbits.canvas.eventhandler import CanvasEventHandler
from tnbits.toolbox.mathematics import Mathematics
from tnbits.bites.pins.menu import Menu
from tnbits.bites.pins.status import Status
from tnbits.bites.pins.constants import *
from tnbits.variations.constants import *
from tnbits.variations.varfontdesignspace import *
from tnbits.variations.varmath import *

FONTTOOLS = 'FontTools'
CORETEXT = 'CoreText'
TOP = BUTTON_HEIGHT + 2*PADDING
BOTTOM = 30
PADDING = 28

class Controller(BaseController):
    """Controls behavior and logic of various variation pin circle parts."""
    # TODO: normalize axis values.
    # TODO: cache glyph labels and dont's update on drag.

    fontSize = SIZES[-2]
    varType = None
    ttfont = None
    ctfont = None
    glyphSet = None
    styleName = None
    glyphName = None
    style = None
    upem = None
    pos = None
    currentAxisTag = None
    uiLocation = {}
    sliderPoints = {}
    angles = {}
    axesDict = {}
    axesTags = {}
    pinLength = None

    def __init__(self, tool, preferencesManager):
        self.tool = tool
        self.preferencesManager = preferencesManager
        self.family = None # To be initialized on opening.
        m = self.fontSize
        self.previewSize = self.fontSize * 2
        self.width = tool.VIEWWIDTH
        self.height = tool.VIEWHEIGHT
        self.setSizes()
        self.kit = CanvasKit()
        self.setPinLength()
        self.updateGlyph = True
        self.build()

    def setSizes(self):
        x = 0
        y = 0
        h = self.height - TOP - BOTTOM - PADDING
        w = self.width - PADDING
        self.mx = x + w / 2
        self.my = y + h / 2
        self.pos = (x, y, w, h)
        s = min(w, h)
        self.cw = int(s * 0.5)
        self.ch = int(s * 0.5)
        self.cx = self.mx - int(self.cw  / 2)
        self.cy = self.my - int(self.ch  / 2)
        #self.pos = (m, m, self.width - m, self.height - m) # Should be canvas size?
        #self.mx, self.my = self.getMiddle()

    def build(self):
        x, y, w, h = self.pos
        size = (w, h)
        self.menu = Menu((x, y, -0, TOP), self)
        y += TOP
        self.canvas = self.tool.w.canvas = Canvas((x, y, -0, -BOTTOM),
                delegate=self, canvasSize=size, flipped=False,
                backgroundColor=NSColor.whiteColor())
        self.eventHandler = CanvasEventHandler(self.canvas)
        self.status = Status((x, -BOTTOM, -0, BOTTOM), self)

    def loadFirstStyle(self):
        """Gets the first style key from the family and tries to load it."""
        try:
            styleKey = self.family.getStyleKeys()[0]
            self.loadFontToolsStyle(styleKey)
            self.update()
        except Exception as e:
            print(traceback.format_exc())

    def updateFontSize(self, fontSize):
        self.fontSize = fontSize
        self.previewSize = self.fontSize * 2
        self.setPinLength()
        self.setLabelSizes()
        for axisTag, angle in self.angles.items():
            size = self.fontSize / 4
            p = self.getPinPoint(angle, self.cw / 2 + self.pinLength + size * 1.33)
            self.objects[axisTag]['label'].setPoint(p)
        self.update()

    def setPinLength(self):
        self.pinLength = l = (self.cw - self.previewSize * 1.2) / 2

        for pin in self.kit.pins:
            pin.setLength(l)

    def setLabelSizes(self):
        for label in self.kit.labels:
            if label.labelSize == 'large':
                label.setFontSize(self.previewSize)


    # Family & styles.

    def setFamily(self, family):
        self.family = family
        names = self.family.getStyleNames()
        self.menu.setStyleNames(names)

    def reset(self):
        self.style = None
        self.upem = None
        self.ttfont = None
        self.glyphSet = None
        self.glyphname = None

    def loadFontToolsStyle(self, styleKey):
        """Loads a new style and calculates the initial spokes positions and
        default variations location."""
        self.varType = FONTTOOLS
        self.reset()
        style = model.getStyle(styleKey)

        if not hasattr(style, 'storage') or not isinstance(style.storage, OTFStorage):
            return

        self.style = style
        self.upem = self.style.info.unitsPerEm
        self.ttfont = self.style.storage._font # TODO: use Floq Model functions.
        self.glyphSet = TTVarFontGlyphSet(self.ttfont) # TODO: just use style
        glyphNames = sorted(list(self.style.keys()))
        # FIXME: might crash.
        self.glyphName = glyphNames[1]
        self.menu.setGlyphNames(self.glyphName, glyphNames)
        self.setAxes()
        self.kit.clear()
        self.setDefaults()
        self.buildSliders()

    def loadCoreTextStyle(self, fontName):
        self.varType = CORETEXT
        self.ctfont = fontName
        self.setAxes()
        self.kit.clear()
        self.setDefaults()
        self.buildSliders()
        self.update()

    def buildSliders(self):
        x, y, w, h = self.pos
        m = 20
        boxWidth = 150
        p0 = (m, h - m)
        p1 = (m + boxWidth, h - m)
        Slider(self, self.kit, 'size', p0, p1, minValue=40, defaultValue=100, maxValue=120,
                updateCallback=self.sizeCallback)

    # Callbacks.

    def sizeCallback(self, pct):
        minValue = 40
        maxValue = 120
        fontSize = minValue + int((pct / 100) * (maxValue - minValue))
        self.updateFontSize(fontSize)

    def previewFactorCallback(self, value):
        pass

    # Var.

    def setAxes(self, coretext=False):
        """Sets contents of axes values, names, angles and spokes."""
        if self.varType == FONTTOOLS:
            d = self.glyphSet._axes
        elif self.varType == CORETEXT:
            print('to be implemented')
            '''
            d = {}

            # TODO: size, location not needed for axis info.
            font = getFont(self.ctfont, size=self.fontSize, location=self.uiLocation)
            axes = getAxisInfo(font)

            for axis in axes:
                d[axis['tag']] = (axis['minValue'], axis['default'], axis['maxValue'])
            '''

        self.axesDict = d
        self.axesTags = self.axesDict.keys()

    def setGlyph(self, glyphName):
        self.glyphName = glyphName

        for label in self.kit.labels:
            label.setGlyph(glyphName)

    def setDefaults(self):
        """Sets or restores default variation location and sets sliders to
        corresponding positions."""

        self.uiLocation = getDefaultLocation(self.axesDict, normalize=False)
        self.angles = distributedAngles(self.axesDict)
        self.objects = {} # TODO: axis object containing pin and label.

        for axisTag, angle in self.angles.items():
            self.objects[axisTag] = {}
            p = self.getPinPoint(angle)
            ratio = getDefaultAxisRatio(axisTag, self.axesDict)
            pin = Pin(self, self.kit, axisTag, p, angle, self.pinLength, ratio=ratio, name=axisTag)
            self.objects[axisTag]['pin'] = Pin

            size = self.fontSize / 4
            p = self.getPinPoint(angle, self.cw / 2 + self.pinLength + size * 1.33)
            x, y = p
            _, _, maxValue = self.axesDict[axisTag]
            location = {axisTag: maxValue}

            if self.varType == CORETEXT:
                label = CTGlyphLabel(self, self.kit, self.glyphName,
                        self.ctfont, 25, location, p,
                        backgroundColor=yellowColor)
            elif self.varType == FONTTOOLS:
                label = FTGlyphLabel(self, self.kit, self.glyphName,
                        self.glyphSet, self.upem, 25, location, p,
                        backgroundColor=yellowColor)

            self.objects[axisTag]['label'] = label

        p = (self.mx, self.my)

        if self.varType == CORETEXT:
            CTGlyphLabel(self, self.kit, self.glyphName, self.ctfont, self.previewSize,
                    self.uiLocation, p, backgroundColor=whiteColor, labelSize='large')
        elif self.varType == FONTTOOLS:
            FTGlyphLabel(self, self.kit, self.glyphName, self.glyphSet,
                    self.upem, self.previewSize, self.uiLocation, p,
                    backgroundColor=whiteColor, labelSize='large')

    def updateUILocation(self, axisTag, ratio):
        """Calculates axis values by percentage and stores them in
        uiLocation."""
        minValue, defaultValue, maxValue = self.axesDict[axisTag]
        v = minValue + (ratio * (maxValue - minValue))
        self.uiLocation[axisTag] = v

    # Mouse.

    def mouseDown(self, event):
        """Checks if a pin is selected."""
        mouse = self.eventHandler.mouseDown(event)
        self.kit.clearSelected()

        for o in self.kit.objects:
            if isinstance(o, Pin):
                if o.on(mouse):
                    o.select()
            elif isinstance(o, Slider):
                if o.on(mouse):
                    o.select()
                    o.update(mouse)

        self.update()

    def mouseDragged(self, event):
        """Checks if a pin is selected and drags within range.
        """
        mouse = self.eventHandler.mouseDragged(event)

        for o in self.kit.objects:
            if isinstance(o, Pin):
                if not o.isSelected:
                    continue

                if o.update(mouse):
                    self.updateUILocation(o.identifier, o.ratio)

            elif isinstance(o, Slider):
                if not o.isSelected:
                    continue

                o.update(mouse)

        self.update(updateGlyph=False)

    def mouseUp(self, event):
        """Resets pins."""
        mouse = self.eventHandler.mouseUp(event)

        for pin in self.kit.pins:
            pin.isSelected = False

        self.update()

    # Drawing.

    def draw(self, rect):
        """Gets graphics context and transforms, translates and scales text
        matrix."""
        context = NSGraphicsContext.currentContext().graphicsPort()
        CGContextSetTextMatrix(context, CGAffineTransformIdentity);

        if not self.style:
            return

        try:
            self.drawBackground()
            self.drawSliders()
            self.drawPins()
            self.drawLabels()
        except Exception as e:
            print(traceback.format_exc())

    def drawBackground(self):
        self.kit.drawCircle(self.cx, self.cy, self.cw, self.ch,
                fillColor=lightGrayColor)

    def drawPins(self):
        for pin in self.kit.pins:
            pin.draw()

    def drawSliders(self):
        for slider in self.kit.sliders:
            slider.draw()

    def drawLabels(self):
        for label in self.kit.labels:
            label.draw()

    def update(self, updateGlyph=False):
        self.updateGlyph = updateGlyph
        self.tool.w.canvas.update()

    # Some calculations.

    def getPinPoint(self, angle, r=None):
        if r is None:
            r = self.cw / 2

        x, y = angle2XY(angle, r)
        p = (self.mx + x, self.my + y)
        return p

    def getMiddle(self):
        x, y, w, h = self.pos
        mx = x + w / 2
        my = y + h / 2
        return int(mx), int(my)

