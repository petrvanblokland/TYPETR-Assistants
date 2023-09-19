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

import os, os.path
from tnbits.base.constants.tool import *
from tnbits.base.static import *
from tnbits.base.console import Console
from tnbits.base.controller import BaseController
from tnbits.base.toolbar import Toolbar
from tnbits.base.handler import BitsHandler
from tnbits.base.tools import *
from tnbits.bites.extractor.stylesheet import StyleSheet
import extractor
from defcon import Font as DefConFont
import AppKit
from vanilla import SplitView

class Controller(BaseController):
    """"""

    parametersClosed = False

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        self.style = None
        self.styleKey = None
        self.loadPreferences()
        items = self.getToolbarItems()
        self.toolbar = Toolbar(self, items=items)
        self.console = Console(self)
        self.styleSheet = StyleSheet(self)
        c = dict(identifier="console", view=self.console.getView())
        s = dict(identifier="styleSheet", view=self.styleSheet.getView())
        sv = SplitView((0, 0, -0, -0), [s, c])
        self.tool.set('splitView', sv)
        #self.status = Status(self)
        #self.tool.set('status', self.status.getView())
        h = BitsHandler(self.console)
        addLogger('tnbits', h)

    def setFamily(self, family):
        self.family = family
        self.setTitle(family)
        self.update()

    def loadPreferences(self):
        pass

    def getToolbarItems(self):
        items = [
            {"itemIdentifier": "extract",
             "label": "Extract",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameAdvanced,
             "callback": self.extractCallback},
            {"itemIdentifier": "openFamily",
             "label": "Open Family",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameFolderSmart,
             "callback": self.openFamilyCallback}
        ]

        if self.mode == 'tool':
            items.append(
                {"itemIdentifier": "openStyle",
                 "label": "Open Style",
                 "imagePath": None,
                 "imageNamed": AppKit.NSImageNameFontPanel,
                 "callback": self.openStyleCallback})
        return items

    def update(self):
        self.styleSheet.update()

    def setStyle(self, styleKey):
        self.styleKey = styleKey
        self.style = self.family.getStyle(styleKey)

    def extract(self, styleKey=None):
        if styleKey is None:
            styleKey = self.styleKey

        if styleKey is None:
            return

        # TODO: check if not UFO. Maybe even before raising menu.
        style = self.family.getStyle(styleKey)
        path = style.path
        parts = path.split('.')

        if parts[-1].lower() == 'ufo':
            msg = '> %s is already a UFO.\n' % path
            self.console.message((msg, 'warning'))
        else:
            ufoPath = '.'.join(parts[:-1]) + '.ufo'

            if os.path.exists(ufoPath):
                msg = '> UFO %s already exists.\n' % ufoPath
                self.console.message((msg, 'warning'))
            else:
                ufo = DefConFont()
                extractor.extractUFO(path, ufo)
                ufo.save(ufoPath)
                self.console.message('> Extracted %s to %s.\n' % (path, ufoPath))

    # Callbacks.

    def openStyleCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()
        self.openStyle(styleKeys)

    def extractCallback(self, sender):
        self.console.clearLines()
        styleKeys = self.styleSheet.getSelectedKeys()

        for styleKey in styleKeys:
            self.extract(styleKey=styleKey)

        self.console.setLines()
        self.update()

    def openFamilyCallback(self, sender):
        self.openFamily()
