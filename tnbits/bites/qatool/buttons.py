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
#    buttons.py
#
from vanilla import Group, Button, TextBox, PopUpButton
from tnbits.base.constants.tool import *
from tnbits.bites.qatool.constants import *

class Buttons(object):

    def __init__(self, controller):
        """Buttons above styles list."""
        self.controller = controller
        self.view = Group((2*SIDE, 0, -0, 24))
        padding = 4
        buttonWidth = 100
        x = padding
        y = padding
        self.view.referenceLabel = TextBox((x, y, 300, 16),
                self.controller.getReferenceLabel(), sizeStyle='small')
        x = -buttonWidth - padding
        self.view.designSpaces = PopUpButton((x, y, buttonWidth, 16), [],
            sizeStyle='small', callback=self.controller.designSpaceCallback)

    def getView(self):
        return self.view
