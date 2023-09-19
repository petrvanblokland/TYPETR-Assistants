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
#    menu.py
#

from vanilla import ComboBox, Button, Group
from tnbits.bites.pins.constants import *
from tnbits.toolbox.transformer import TX
import CoreText, AppKit

def getFont(fontName, size=200, location=None):
    attributes = {CoreText.kCTFontNameAttribute: fontName}
    descriptor = CoreText.CTFontDescriptorCreateWithAttributes(attributes);

    if location:
        for tag, value in location.items():
            descriptor = CoreText.CTFontDescriptorCreateCopyWithVariation(descriptor, tagToInt(tag), value)
    return CoreText.CTFontCreateWithFontDescriptor(descriptor, size, [1, 0, 0, 1, 0, 0])

def getVarFontList():
    allVarFonts = []
    varFonts = []
    baseFonts = set()

    for fontName in AppKit.NSFontManager.sharedFontManager().availableFonts():
        font = getFont(fontName, size=10)
        rawAxisInfo = CoreText.CTFontCopyVariationAxes(font)

        if rawAxisInfo:
            allVarFonts.append(fontName)

    for fontName in allVarFonts:
        if "_" not in fontName:
            baseFonts.add(fontName)

    for fontName in allVarFonts:
        if "_" not in fontName or fontName.split("_")[0] not in baseFonts:
            varFonts.append(fontName)

    return varFonts

class Menu(object):
    """Wraps a set of menu buttons in a group."""

    def __init__(self, pos, controller):
        self.pos = pos
        self.controller = controller
        self.m = Group((0, 0, -0, -0))
        controller.tool.w.menu = self.m
        self.coreTextFonts = getVarFontList()
        self.build()

    def build(self):
        w = 150
        h = 20
        x = 4
        y = 4
        p = 4

        self.m.stylesBox = ComboBox((x, y, w, h), [], callback=self.stylesBoxCallback)
        x += w + p
        self.m.glyphsBox = ComboBox((x, y, w, h), [], callback=self.glyphsBoxCallback)
        x += w + p
        self.m.sizeBox = ComboBox((x, y, w, h), SIZES, callback=self.sizeBoxCallback)
        self.m.sizeBox.set(self.controller.fontSize)
        x += w + p
        self.m.coreTextBox = ComboBox((x, y, w, h), self.coreTextFonts,
                callback=self.coreTextBoxCallback)
        x += w + p
        self.m.defaultsButton = Button((x, y, w, h), 'defaults', callback=self.defaultsCallback)

    def setStyleNames(self, names):
        self.m.stylesBox.setItems(names)
        self.m.stylesBox.set(names[0])

    def setGlyphNames(self, currentGlyphName, glyphNames):
        self.m.glyphsBox.setItems(glyphNames)
        self.m.glyphsBox.set(currentGlyphName)

    def stylesBoxCallback(self, sender):
        self.controller.styleName = sender.get()

        for styleKey in self.controller.family.getStyleKeys():
            styleId = styleKey[1]
            styleName = TX.path2StyleName(styleId)

            if self.controller.styleName == styleName:
                self.controller.loadFontToolsStyle(styleKey)
                self.controller.update()

    def glyphsBoxCallback(self, sender):
        self.controller.setGlyph(sender.get())
        self.controller.update()

    def sizeBoxCallback(self, sender):
        size = int(sender.get())
        self.controller.updateFontSize(size)

    def defaultsCallback(self, sender):
        self.controller.setDefaults()
        self.controller.update()

    def coreTextBoxCallback(self, sender):
        fontName = sender.get()
        self.controller.loadCoreTextStyle(fontName)
