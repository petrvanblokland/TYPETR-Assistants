# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Extractor appication.
#    Copyright (c) 2016+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    Extractor.py
#
from vanilla import Window
from tnbits.base.preferences import Preferences
from tnbits.bites.extractor.controller import Controller
from tnbits.base.app import App
from tnbits.base.model import *

class Extractor(App):
    u"""Implements the standalone application version of the Type Network
    extractor tool."""

    windowSize = (1000, 900)
    NAME = u'Bakery'

    def __init__(self):
        super(Extractor, self).__init__()
        self.w = Window(self.windowSize, minSize=(1, 1), closable=True)
        self.preferences = Preferences(self.NAME, standAlone=True)
        self.controller = Controller(self, mode='app')
        self.openWindow()
        family = openFamily(self)
        self.controller.setFamily(family)
