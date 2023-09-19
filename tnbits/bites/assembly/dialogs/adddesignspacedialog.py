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
from vanilla import Sheet, TextBox, Button, EditText
from tnbits.base.constants.tool import *

class AddDesignSpaceDialog(object):
    """Dialog to add a design space."""


    def __init__(self, controller, family, callback, width=200, height=100):
        self.controller = controller
        self.family = family
        self.title = 'Add a design space to family %s' % family.name
        self.callback = callback
        self.width = width
        self.height = height
        self.name = None
        dialogSize = (self.width, self.height)
        self.window = Sheet(dialogSize, self.controller.tool.getWindow(),
                minSize=dialogSize, maxSize=dialogSize)
        x = PADDING
        y = PADDING
        w = self.width - 2*PADDING
        h = BUTTON_HEIGHT
        self.window.addLabel = TextBox((x, y, w, h), 'Please enter a name')
        y += h
        self.window.addEntry = EditText((x, y, w, h), '', callback=self.edit)
        pos = (-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.cancel = Button(pos, "Cancel", callback=self.close)
        pos = (2*-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.okay = Button(pos, "Okay", callback=self.okay)
        self.window.okay.getNSButton().setEnabled_(False)
        self.window.open()

    # Callbacks.

    def okay(self, sender):
        self.callback(self.name)
        self.closeWindow()

    def close(self, sender):
        self.callback(None)
        self.closeWindow()

    def closeWindow(self):
        if self.window is not None:
            self.window.close()

    def edit(self, sender):
        self.name = sender.get()
        self.checkOkay()

    def checkOkay(self):
        if not self.name in self.family:
            self.window.okay.getNSButton().setEnabled_(True)
        else:
            self.window.okay.getNSButton().setEnabled_(False)
