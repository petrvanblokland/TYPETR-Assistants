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
#    controller.py
#

import traceback
from vanilla import PopUpButton, SplitView
from tnbits.base.controller import BaseController
from tnbits.base.constants.tool import *
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.bites.spreadsheet.familyview import FamilyView
from tnbits.bites.spreadsheet.infoview import InfoView
from tnbits.bites.spreadsheet.constants import *
from tnbits.bites.spreadsheet.dialogs.adddialog import AddDialog

class Controller(BaseController):
    """Implements internal logic between various parts of the spreadsheet."""

    style = None
    sa = None
    styleKey = None
    glyph = None
    glyphName = None
    ga = None

    def __init__(self, tool, mode='tool'):
        """Adds the spreadsheet to a view and loads some font data."""
        super(Controller, self).__init__(tool, mode)
        self.presetName = PRESETS_ORDER[0]
        self.designSpaces = PopUpButton((PADDING, PADDING, BUTTON_WIDTH, BUTTON_HEIGHT),
            [], sizeStyle='small', callback=self.designSpaceCallback)
        self.glyphSets = PopUpButton((2*PADDING + BUTTON_WIDTH, PADDING,
            BUTTON_WIDTH, BUTTON_HEIGHT), PRESETS_ORDER, sizeStyle='small',
            callback=self.glyphSetCallback)
        self.familyView = FamilyView(self)
        self.infoView = InfoView(self)
        f = dict(identifier="styleSheet", view=self.familyView.getView())
        i = dict(identifier="infoView", view=self.infoView.getView())
        self.splitView = SplitView((0, MENU, -0, -0), [f, i], isVertical=False)
        self.tool.set('designSpaces', self.designSpaces)
        self.tool.set('glyphSets', self.glyphSets)
        self.tool.set('splitView', self.splitView)
        self.addDialog = None

    def reset(self):
        self.style = None
        self.sa = None
        self.styleKey = None
        self.glyph = None
        self.glyphName = None
        self.ga = None

    def getView(self):
        return self.splitView

    def openAddDialog(self, styleKey):
        if self.addDialog is None:
            self.addDialog = AddDialog(self, styleKey, self.addToDesignSpace)

    def addToDesignSpace(self, designSpaceName, styleKey):
        self.addDialog = None

        for name in self.family:
            ds = self.family[name]

            if name == designSpaceName:
                ds.asMaster(styleKey)
                print('adding master %s to %s' % (styleKey[1], name))
                ds.save()
            else:
                if ds.isMaster(styleKey):
                    print('removing master %s from %s' % (styleKey[1], name))
                    ds.notMaster(styleKey)
                    ds.save()

        self.familyView.update()

    def removeFromDesignSpace(self, styleKey):
        ds = self.getDesignSpace()
        print('removing master %s from %s' % (styleKey[1], ds.name))
        ds.notMaster(styleKey)
        ds.save()
        self.familyView.update()

    def setFamily(self, family):
        self.family = family
        self.setTitle(family)
        #name = self.family.getFirstName()
        name = ANY
        self.setDesignSpace(name)
        names = self.getDesignSpaceNames()
        self.designSpaces.setItems(names)
        i = names.index(name)
        self.designSpaces.set(i)
        self.familyView.update()

    def setStyle(self, styleKey):
        self.style = self.getStyle(styleKey)
        self.styleKey = styleKey
        self.sa = analyzerManager.getStyleAnalyzer(style=self.style)
        self.familyView.glyphSheet.update()
        self.update()

    def getGlyph(self, glyphName):
        assert not self.style is None
        glyph = self.style[glyphName]
        #print(glyph)
        #print(type(glyph))
        # FIXME: should be a tnbits model glyph.

        try:
            ga = analyzerManager.getGlyphAnalyzer(glyph, parent=self.style)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            ga = None

        self.glyphName = glyphName
        self.glyph = glyph
        self.ga = ga
        return glyph, ga

    def update(self, updateGlyph=False):
        """Updates information after selection has changed."""
        self.infoView.clearLines()

        if self.styleKey and self.style and self.sa:
            msg = ' > style name: %s\n' % self.styleKey[1]
            self.infoView.message(msg)

            if updateGlyph and self.glyph and self.glyphName and self.ga:
                msg = ' > glyph name: %s\n' % self.glyphName
                self.infoView.message(msg)

                for key, value in self.ga.__dict__.items():
                    msg = ' > %s: %s\n' % (key, value)
                    self.infoView.message(msg)

            self.infoView.setLines()

    def designSpaceCallback(self, sender):
        i = sender.get()
        names = self.getDesignSpaceNames()
        name = names[i]
        self.setDesignSpace(name)
        self.familyView.styleSheet.update()

    def glyphSetCallback(self, sender):
        i = sender.get()
        self.presetName = PRESETS_ORDER[i]
        self.familyView.update(styles=False)
