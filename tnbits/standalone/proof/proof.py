# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Proofing appication.
#    Copyright (c) 2016+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    app.py
#
from vanilla import Window
from tnbits.base.preferences import Preferences
from tnbits.bites.proof.controller import Controller
from tnbits.base.app import App
from tnbits.base.model import *

class Proof(App):
    u"""Implements a standalone application version of the Type Network
    proofing tool."""

    NAME = 'Proof'
    windowSize = (1000, 900)

    def __init__(self):
        super(Proof, self).__init__()
        self.w = Window(self.windowSize, minSize=(1, 1), closable=True)
        self.preferences = Preferences(self.NAME, standAlone=True)
        self.controller = Controller(self, mode='app')
        self.openWindow()
        family = openFamily(self)
        self.controller.setFamily(family)

    def savePreferences(self):
        print('ProofApp.savePreferences(): to be implemented')

    def open(self):
        family = openFamily(self)
        self.controller.setFamily(family)

    def close(self):
        self.controller.closeFamily()
