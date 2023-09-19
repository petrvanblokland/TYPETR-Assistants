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
from tnbits.base.controller import BaseController
from tnbits.base.scroll import ScrollGroup
from tnbits.base.tools import *
from tnbits.base.static import *
from tnbits.base.preferences import Preferences
from tnbits.base.preferencemodels import *
from tnbits.bites.switchboard.board import Board
from os.path import exists

class Controller(BaseController):
    """"""

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        root = getRoot()
        toolNames = findTools(root)
        prefTools = getPrefTools()
        self.prefOrder = []
        self.preferencesDict = {}

        # Mojo-only prefs.
        for toolName in prefTools['BaseTool']:
            preferences = Preferences(toolName, standAlone=False)
            self.preferencesDict[toolName] = preferences
            self.prefOrder.append(toolName)

        for toolName in prefTools['Tool']:
            preferences = Preferences(toolName)
            self.preferencesDict[toolName] = preferences
            self.prefOrder.append(toolName)

        self.board = Board(self, self.preferencesDict)
        nsview = self.board.getNSView()
        self.tool.set('scroller', ScrollGroup(nsview, (0, 0, -0, -0)))

    def setFamily(self, family):
        pass
