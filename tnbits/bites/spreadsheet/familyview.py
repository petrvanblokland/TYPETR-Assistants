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
#    familyview.py
#
from tnbits.base.constants.tool import *
from tnbits.bites.spreadsheet.stylesheet import StyleSheet
from tnbits.bites.spreadsheet.glyphsheet import GlyphSheet
from vanilla import SplitView

class FamilyView(object):
    """Shows design spaces, styles & glyphs in a column browser."""

    def __init__(self, controller, pos=(0, 0, -0, -0)):
        self.controller = controller
        self.styleSheet = StyleSheet(self)
        self.glyphSheet = GlyphSheet(self)
        s = dict(identifier="styleSheet", view=self.styleSheet.getView())
        g = dict(identifier="glyphSheet", view=self.glyphSheet.getView())
        self.view = SplitView((0, 0, -0, -0), [s, g])

    def update(self, styles=True, glyphs=True):
        if styles:
            self.styleSheet.update()

        if glyphs:
            self.glyphSheet.update()

    def savePreferences(self, sender):
        pass

    def getView(self):
        return self.view
