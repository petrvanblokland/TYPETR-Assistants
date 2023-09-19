# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N   T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tool.py
#

from vanilla import Window
from tnbits.base.tool import Tool
from tnbits.base.preferences import Preferences
from tnbits.base.constants.tool import *
from tnbits.base.windows import setBackgroundColor
from tnbits.bites.qatool.controller import Controller

class QualityAssuranceTool(Tool):
    """Checks production fonts to see if they are complete and ready for
    publication."""

    TOOLID = 'tnQualityAssurance'
    NAME = 'QualityAssurance'
    DEFAULTKEY = "com.typenetwork.qa"
    CATEGORY = CATEGORY_DEVELOPMENT
    VIEWWIDTH = 1000
    VIEWHEIGHT = 900
    VIEWX = 50
    VIEWY = 50
    VIEWMINSIZE = (600, 400)
    VIEWMAXSIZE = (4000, 4000)
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)

    OBSERVERS = (
        ('mouseUp', EVENT_MOUSEUP),
        ('keyUp', EVENT_KEYUP),
        ('fontSaved', EVENT_FONTDIDSAVE),
    )

    def build(self):
        """Builds quality assurance tool."""
        self.preferences = Preferences(self.NAME, defaultPos=self.DEFAULTPOS)
        screen, posSize = self.preferences.screens.getWindowScreenPosSize()
        self.w = window = Window(posSize=posSize, title=self.NAME,
                screen=screen, minSize=self.VIEWMINSIZE,
                maxSize=self.VIEWMAXSIZE)
        self.controller = Controller(self)
        setBackgroundColor(self.w)
        self.openWindow()

    def setFamily(self, family):
        self.controller.setFamily(family)

    def preferencesChanged(self):
        self.controller.preferencesChanged()

    def mouseUp(self, event):
        self.controller.update()

    def keyUp(self, event):
        self.controller.update()

    def fontSaved(self, event):
        self.controller.update()
