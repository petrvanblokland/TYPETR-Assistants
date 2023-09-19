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
#    savedialog.py
#
from vanilla import Sheet, TextBox, Button, EditText
from tnbits.base.constants.tool import *

class SaveDialog(object):
    """Dialog asking to save the edited font."""


    def __init__(self, controller, callback, width=200, height=100):
        self.controller = controller
        self.title = 'Confirm Save'
        self.callback = callback
        self.width = 2 * BUTTON_WIDTH + 3 * PADDING
        self.height = height
        self.name = None
        dialogSize = (self.width, self.height)
        self.window = Sheet(dialogSize, self.controller.tool.getWindow(),
                minSize=dialogSize, maxSize=dialogSize)
        x = PADDING
        y = PADDING
        w = self.width - 2*PADDING
        h = BUTTON_HEIGHT
        self.window.addLabel = TextBox((x, y, w, h), 'Save font?')
        y += h

        x = -BUTTON_WIDTH - PADDING
        y = -3 * UNIT
        w = BUTTON_WIDTH
        h = 2 * UNIT
        pos = (x, y, w, h)
        self.window.cancel = Button(pos, "Cancel", callback=self.cancel)


        x -= BUTTON_WIDTH + PADDING
        pos = (x, y, w, h)
        self.window.save = Button(pos, "Okay", callback=self.save)
        self.window.open()

    # Callbacks.

    def save(self, sender):
        self.callback(True)
        self.closeWindow()

    def cancel(self, sender):
        self.callback(False)
        self.closeWindow()

    def closeWindow(self):
        if self.window is not None:
            self.window.close()
