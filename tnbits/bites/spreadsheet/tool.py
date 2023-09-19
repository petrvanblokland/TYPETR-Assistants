# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    Spreadsheet.py
#


from vanilla import Window
from tnbits.base.preferences import Preferences
from tnbits.base.constants.tool import CATEGORY_ANALYZE
from tnbits.base.tool import Tool
from tnbits.base.windows import *
from tnbits.bites.spreadsheet.controller import Controller


class SpreadsheetTool(Tool):
    """Spreadsheet that connects floqmodel, analyzers and designspace."""
    TOOLID = 'tnSpreadsheet'
    NAME = 'Spreadsheet'
    CATEGORY = CATEGORY_ANALYZE
    VIEWX = 50
    VIEWY = 50
    VIEWHEIGHT = 800
    VIEWWIDTH = 1200
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)
    VIEWMINSIZE = (600, 400)
    VIEWMAXSIZE = (4000, 4000)

    def build(self):
        """Builds spread sheet tool."""
        self.preferences = Preferences(self.NAME, defaultPos=self.DEFAULTPOS,
                useFloatingWindow=False)
        screen, posSize = self.preferences.screens.getWindowScreenPosSize()
        self.w = window = Window(posSize=posSize, title=self.NAME,
                screen=screen, minSize=self.VIEWMINSIZE,
                maxSize=self.VIEWMAXSIZE)
        setBackgroundColor(self.w)
        self.controller = Controller(self)
        self.openWindow()

    def setFamily(self, family):
        self.controller.setFamily(family)

