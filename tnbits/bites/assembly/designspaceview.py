# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits #    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    designspaceview.py
#

import sys
import fontmake
import ufo2ft
import defcon
import fontTools.ufoLib
import cu2qu
from tnbits.base.console import Console
from tnbits.bites.assembly.axes import Axes
from tnbits.bites.assembly.masters import Masters
from tnbits.bites.assembly.preview import Preview
from tnbits.base.constants.tool import *
from vanilla import SplitView

class DesignSpaceView(object):
    """
    """

    _doVerbose = True
    _doSuppressWarnings = False

    def __init__(self, controller, pos=(0, 0, -0, -0)):
        # Design space split view.
        self.doShowNumbers = True # TODO: make a console feature.
        self.controller = controller
        self.axes = Axes(self)
        self.masters = Masters(self)
        self.preview = Preview(self)
        a = dict(identifier="axes", view=self.axes.getView())
        m = dict(identifier="masters", view=self.masters.getView())
        p = dict(identifier="preview", view=self.preview.getView())
        #instances = dict(identifier="instances", view=self.instances.getView())
        self.listSplitView = SplitView((0, 0, -0, -0), [a, m, p],
                isVertical=False)

        # Consoles.

        self.prompt = Console(self)
        self.xmlView = Console(self)
        p = dict(identifier="prompt", view=self.prompt.getView())
        x = dict(identifier="xml", view=self.xmlView.getView())
        self.promptSplitView = SplitView((0, 0, -0, -0), [p, x],
                isVertical=False)

        # Main splitview.

        l = dict(identifier="listSplitView", view=self.listSplitView)
        c = dict(identifier="consolesSplitView", view=self.promptSplitView)
        self.view = SplitView((SIDE + 2*UNIT, 0, -0, -3*UNIT), [l, c])

    def getView(self):
        return self.view

    def updateMasters(self):
        self.masters.update()
        self.prompt.setLines()
        #self.instances.resetList()

    def updatePrompt(self, messages):
        self.prompt.clearLines()

        for m in messages:
            self.prompt.message(m)

        self.prompt.setLines()

    def savePreferences(self, sender):
        pass

    def update(self):
        self.masters.update()
        self.axes.update()
        self.preview.update()
        self.prompt.setLines()

    def show(self, doShow=True):
        hidden = not doShow
        self.view.getNSSplitView().setHidden_(hidden)

    def resize(self, width, height):
        self.view.resize(width, height)

    def move(self, x, y):
        self.view.move(x, y)

    def getDesignSpace(self):
        return self.controller.getDesignSpace()

    def clear(self):
        self.prompt.clearLines()
        self.xmlView.clearLines()

    def showNumbers(self):
        if self.doShowNumbers:
            self.doShowNumbers = False
        elif not self.doShowNumbers:
            self.doShowNumbers = True

        self.updateXml()

    def scanLibraries(self):
        """Checks relevant library paths and versions."""
        self.prompt.message('> Python version: %s\n' % sys.version)
        v = fontmake.__version__
        self.prompt.message('> fontmake version: %s\n' % v)
        p = fontmake.__path__[0]
        self.prompt.message('> fontmake path: %s\n' % p)
        v = ufo2ft.__version__
        self.prompt.message('> ufo2ft version: %s\n' % v)
        p = ufo2ft.__path__[0]
        self.prompt.message('> ufo2ft path: %s\n' % p)
        v = cu2qu.__version__
        self.prompt.message('> cu2qu version: %s\n' % v)
        p = cu2qu.__path__[0]
        self.prompt.message('> cu2qu path: %s\n' % p)

        try:
            v = defcon.__version__
            self.prompt.message('> defcon version: %s\n' % v)
        except:
            v = 'no version info, need >= 0.3.4'
            self.prompt.message(('> defcon version: %s\n' % v, 'error'))

        p = defcon.__path__[0]
        self.prompt.message('> defcon path: %s\n' % p)
        v = fontTools.ufoLib.__version__
        self.prompt.message('> ufoLib version: %s\n' % v)
        p = fontTools.ufoLib.__path__[0]
        self.prompt.message('> ufoLib path: %s\n' % p)
        self.prompt.setLines()

    # Load.

    def updateXml(self):
        """Shows design space XML in console.
        TODO: parse for errors and report.
        """
        self.xmlView.clearLines()

        try:
            self.updateXmlFile()
        except:
            self.doMissingFileMessage()

    def updateXmlFile(self):
        """Opens XML file and shows it in console."""
        # TODO: connect to design space XML.
        ds = self.getDesignSpace()
        lines = ds.getXMLFromFile()
        l = len(str(len(lines)))
        formatter = '{:>%s}' % l

        for n, line in enumerate(lines):
            number = formatter.format(n)
            if self.doShowNumbers:
                self.xmlView.message('%s %s' % (number, line))
            else:
                self.xmlView.message('%s' % line)

        self.xmlView.setLines()

    # Message.

    def doMissingFileMessage(self):
        ds = self.getDesignSpace()
        familyName = self.controller.family.name

        if not ds:
            return

        msg = 'No file for design space %s, %s' % (familyName, ds.name)
        self.xmlView.message((msg, 'error'))
        self.xmlView.setLines()

    # Callbacks.

    def saveClearCallback(self, console, clear):
        pass
