# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Spreadsheet appication.
#    Copyright (c) 2016+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    Spreadsheet.py
#
from vanilla import Window
from tnbits.base.preferences import Preferences
from tnbits.bites.spreadsheet.controller import Controller
from tnbits.base.app import App
from tnbits.base.model import *

class Spreadsheet(App):
    u"""Implements the standalone application version of the Type Network
    bakery tool."""

    NAME = u'Spreadsheet'
    windowSize = (1000, 900)

    def __init__(self):
        super(Spreadsheet, self).__init__()
        self.w = Window(self.windowSize, minSize=(1, 1), closable=True)
        self.preferences = Preferences(self.NAME, standAlone=True)
        self.controller = Controller(self, mode='app')
        self.openWindow()
        family = openFamily(self)
        self.controller.setFamily(family)
