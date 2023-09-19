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

from tnbits.base.constants.tool import *
from tnbits.base.static import *
from tnbits.base.console import Console
from tnbits.base.controller import BaseController
from tnbits.base.toolbar import Toolbar
from tnbits.base.handler import BitsHandler
from tnbits.model.toolbox.kerning.buildgroups import explodeKerning
from tnbits.base.tools import *
from tnbits.bites.kerning.stylesheet import StyleSheet
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
        addLogger('ROBOFONT', h)
        addLogger('tnbits', h)

    def setFamily(self, family):
        self.family = family
        self.setTitle(family)
        self.update()

    def loadPreferences(self):
        pass

    def getToolbarItems(self):
        items = [
            {"itemIdentifier": "kerns",
             "label": "Kerns",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameAdvanced,
             "callback": self.kernsCallback},
            {"itemIdentifier": "groups",
             "label": "Groups",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameAdvanced,
             "callback": self.groupsCallback},
            {"itemIdentifier": "explode",
             "label": "Explode",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameAdvanced,
             "callback": self.explodeCallback},
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

    def kerns(self, styleKey=None):
        self.console.clearLines()
        if styleKey is None:
            styleKey = self.styleKey

        if styleKey is None:
            return

        style = self.family.getStyle(styleKey)

        if hasattr(style, 'kerning'):
            self.console.message('Kernings: %d\n' % len(style.kerning))
            for k, v in style.kerning.items():
                self.console.message('%s: %s\n' % (k, v))
            self.console.setLines()

    def groups(self, styleKey=None):
        self.console.clearLines()
        if styleKey is None:
            styleKey = self.styleKey

        if styleKey is None:
            return

        style = self.family.getStyle(styleKey)
        if hasattr(style, 'groups'):
            self.console.message('Groups: %d\n' % len(style.groups))
            for k, v in style.groups.items():
                self.console.message('%s: %s\n' % (k, v))
            self.console.setLines()

    def explode(self, styleKey=None):
        self.console.clearLines()
        if styleKey is None:
            styleKey = self.styleKey

        if styleKey is None:
            return

        style = self.family.getStyle(styleKey)

        if hasattr(style, 'kerning') and hasattr(style, 'groups'):
            flatKerning, groupsUsed, groupsNotUsed, exceptions = explodeKerning(style.kerning, style.groups)
            self.console.message('> Kerns: %d\n' % len(style.kerning))
            self.console.message('> Groups: %d\n' % len(style.groups))
            self.console.message('> Exploded: %d\n' % len(flatKerning))
            self.console.message('> Groups Used: %d\n' % len(groupsUsed))
            self.console.message('> Groups not Used: %d\n' % len(groupsNotUsed))
            self.console.message('> Exceptions: %d\n' % len(exceptions))

            for k, v in flatKerning.items():
                self.console.message('%s: %s\n' % (k, v))

            self.console.message('\nGroups used:\n')

            for n in groupsUsed:
                self.console.message('%s\n' % n)

            self.console.message('\nGroups not used:\n')

            for n in groupsNotUsed:
                self.console.message('%s\n' % n)

            self.console.message('\nExceptions:\n')

            for e in exceptions:
                self.console.message('%s\n' % e)

            self.console.setLines()


    # Callbacks.

    def openStyleCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()
        self.editStyleKeys(styleKeys)

    def kernsCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()

        for styleKey in styleKeys:
            self.kerns(styleKey=styleKey)

    def groupsCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()

        for styleKey in styleKeys:
            self.groups(styleKey=styleKey)

    def explodeCallback(self, sender):
        styleKeys = self.styleSheet.getSelectedKeys()

        for styleKey in styleKeys:
            self.explode(styleKey=styleKey)

    def openFamilyCallback(self, sender):
        self.openFamily()
