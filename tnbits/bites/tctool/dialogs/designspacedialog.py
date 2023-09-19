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
#    adddesignspacedialog.py
#
from vanilla import Sheet, TextBox, Button,  PopUpButton
from tnbits.base.constants.tool import *

class DesignSpaceDialog(object):
    """Dialog to add a design space."""


    def __init__(self, controller, callback, width=200, height=100):
        self.controller = controller
        self.title = 'Select a design space'
        self.callback = callback
        self.width = width
        self.height = height
        self.designSpaceName = None
        dialogSize = (self.width, self.height)
        self.window = Sheet(dialogSize, self.controller.tool.getWindow(),
                minSize=dialogSize, maxSize=dialogSize)

        s = 'small'
        x = PADDING
        y = PADDING
        w = self.width - 2*PADDING
        h = BUTTON_HEIGHT

        self.names = controller.family.getSortedDesignSpaceNames()
        pos = (x, y, w, h)
        self.window.designSpaceSelection = PopUpButton(pos, self.names, sizeStyle=s,
                callback=self.selectionCallback)
        h += BUTTON_HEIGHT + PADDING

        pos = (-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.cancel = Button(pos, "Cancel", callback=self.close)

        pos = (2*-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.okay = Button(pos, "Okay", callback=self.okay)
        self.window.okay.getNSButton().setEnabled_(False)
        self.window.open()

    # Callbacks.

    def selectionCallback(self, sender):
        i = sender.get()
        self.designSpaceName = self.names[i]
        self.window.okay.getNSButton().setEnabled_(True)

    def okay(self, sender):
        self.callback(self.designSpaceName)
        self.closeWindow()

    def close(self, sender):
        self.callback(None)
        self.closeWindow()

    def closeWindow(self):
        if self.window is not None:
            self.window.close()

    def designSpaceCallback(self, sender):
        self.designSpaceName = sender.get()
        self.checkOkay()

    def checkOkay(self):
        if not self.name in self.family:
            self.window.okay.getNSButton().setEnabled_(True)
        else:
            self.window.okay.getNSButton().setEnabled_(False)
