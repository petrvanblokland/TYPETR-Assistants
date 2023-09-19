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

import os, traceback, codecs, sys
import AppKit
from vanilla import Window, SplitView
from tnbits.base.controller import BaseController
from tnbits.base.model import *
from tnbits.base.tools import *
from tnbits.base.console import Console
from tnbits.base.handler import BitsHandler
from tnbits.base.toolbar import Toolbar
from tnbits.base.constants.tool import *
from tnbits.base.scroll import ScrollGroup
from tnbits.base.samples import *
from tnbits.bites.families.stylesheet import FamStyleSheet

W = 150

class Controller(BaseController):
    """Implements internal logic between different parts of family tool."""

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        self.build()

    def build(self):
        self.toolbar = Toolbar(self, items=self.getToolbarItems())
        self.styleSheet = FamStyleSheet(self, pos=(W, 0, -0, -0))
        self.tool.set('styleSheet', self.styleSheet.getView())
        showLog()
        showOutputWindow()

    def write(self, inputText):
        log = getLog()
        log.console.message(inputText)
        log.set()

    def close(self):
        pass

    def setFamily(self, family):
        self.family = family
        self.family.updateRFonts()
        self.setTitle(family)
        self.styleSheet.set()
        setLog()

    def update(self):
        self.styleSheet.update()

    # Get.

    def getToolbarItems(self):
        items = [
            {"itemIdentifier": "pr",
             "label": "Proof",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameFolderSmart,
             "callback": self.proofCallback},
            {"itemIdentifier": "qa",
             "label": "Quality Assurance",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameFolderSmart,
             "callback": self.qualityAssuranceCallback},
            {"itemIdentifier": "tc",
             "label": "Text Center",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameFolderSmart,
             "callback": self.textCenterCallback},
            {"itemIdentifier": "ss",
             "label": "Spreadsheet",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameFolderSmart,
             "callback": self.spreadsheetCallback},
            {"itemIdentifier": "as",
             "label": "Assembly",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameFolderSmart,
             "callback": self.assemblyCallback},
        ]

        return items

    # Callbacks.

    def proofCallback(self, sender):
        from tnbits.bites.proof.tool import ProofTool
        openTool(ProofTool, self.family)

    def qualityAssuranceCallback(self, sender):
        from tnbits.bites.qatool.tool import QualityAssuranceTool
        openTool(QualityAssuranceTool, self.family)

    def textCenterCallback(self, sender):
        from tnbits.bites.tctool.tool import TextCenterTool
        openTool(TextCenterTool, self.family)

    def spreadsheetCallback(self, sender):
        from tnbits.bites.spreadsheet.tool import SpreadsheetTool
        openTool(SpreadsheetTool, self.family)

    def assemblyCallback(self, sender):
        from tnbits.bites.assembly.tool import AssemblyTool
        openTool(AssemblyTool, self.family)
