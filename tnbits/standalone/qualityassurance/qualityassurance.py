# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Quality Assurance appication.
#    Copyright (c) 2016+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    qualityassurance.py
#
from vanilla import Window
from tnbits.base.preferences import Preferences
from tnbits.bites.qatool.controller import Controller
from tnbits.base.app import App
from tnbits.base.model import *

class QualityAssurance(App):
    u"""Implements the standalone application version of the Type Network
    quality assurance tool."""

    windowSize = (1000, 900)
    NAME = u'Quality Assurance'

    def __init__(self):
        super(QualityAssurance, self).__init__()
        self.w = Window(self.windowSize, minSize=(1, 1), closable=True)
        self.preferences = Preferences(self.NAME, standAlone=True)
        self.controller = Controller(self, mode='app')
        self.openWindow()
        family = openFamily(self)
        self.controller.setFamily(family)
