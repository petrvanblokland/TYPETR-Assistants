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
from vanilla import Sheet, TextBox, Button, PopUpButton
from tnbits.base.constants.tool import *
from tnbits.base.expandtext  import _getAllGlyphNames

class AddDialog(object):
    """Dialog asking which glyph to add to a group."""

    def __init__(self, controller, groupName, callback, width=200, height=100):
        self.controller = controller
        self.groupName = groupName
        self.title = 'Add Glyph'
        self.callback = callback
        self.width = 2 * BUTTON_WIDTH + 3 * PADDING
        self.height = height
        self.selectedGlyphName = None
        self.glyphNames = _getAllGlyphNames(controller.style)
        dialogSize = (self.width, self.height)
        self.window = Sheet(dialogSize, self.controller.groupsWindow.getWindow(),
                minSize=dialogSize, maxSize=dialogSize)
        x = PADDING
        y = PADDING
        w = self.width - 2*PADDING
        h = BUTTON_HEIGHT
        self.window.addLabel = TextBox((x, y, w, h), 'Select a Glyph')
        y += h
        self.window.popUp = PopUpButton((x, y, w, h), self.glyphNames,
                sizeStyle='small', callback=self.selectGlyphCallback)

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

    def selectGlyphCallback(self, sender):
        i = sender.get()
        self.selectedGlyphName = self.glyphNames[i]

    def save(self, sender):
        self.callback(self.groupName, self.selectedGlyphName)
        self.closeWindow()

    def cancel(self, sender):
        self.callback(None, None)
        self.closeWindow()

    def closeWindow(self):
        if self.window is not None:
            self.window.close()
