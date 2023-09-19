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
#    status.py
#
from vanilla import Group, TextBox
from tnbits.base.constants.tool import *
from tnbits.base.constants.colors import *

class Status(object):

    def __init__(self, controller):
        self.controller = controller
        self.view = Group((0, -3*UNIT, -0, 3*UNIT))
        nsView = self.view.getNSView()
        nsView.setWantsLayer_(True)
        nsView.layer().setBackgroundColor_(greyColor)
        self.view.info = TextBox((UNIT, UNIT / 2, -0, -0), '')

    def set(self, msg):
        self.view.info.set(msg)

    def getView(self):
        return self.view
