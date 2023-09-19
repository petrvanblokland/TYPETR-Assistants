# -*- coding: UTF-8 -*- # -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    actions.py
#

from vanilla import Group, Button
from tnbits.bites.qatool.constants import *
from tnbits.base.constants.tool import *

class Actions(object):
    """
    TODO: merge with console.
    """

    def __init__(self, controller, mode):
        """Action buttons below split view."""
        self.controller = controller
        self.mode = mode
        self.view = Group((SIDE, -24, -0, -0))
        padding = 4
        buttonWidth = 80
        dx = -buttonWidth - padding
        x = dx
        y = 4

        self.view.clearConsole = Button((x, y, buttonWidth, 16), 'Clear',
                sizeStyle='mini', callback=controller.clearCallback)
        x += dx
        self.view.saveConsole = Button((x, y, buttonWidth, 16), 'Save',
                sizeStyle='mini', callback=controller.saveCallback)

        self.setEnabled(False)

    def setEnabled(self, value):
        self.view.clearConsole.enable(value)
        self.view.saveConsole.enable(value)

    def getView(self):
        return self.view

