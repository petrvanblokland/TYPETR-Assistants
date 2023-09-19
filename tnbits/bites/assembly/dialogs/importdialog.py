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
#    importdialog.py
#
from AppKit import NSLineBreakByTruncatingMiddle
from vanilla import TextBox, Button, PopUpButton, Sheet
from vanilla.dialogs import getFile
from tnbits.base.constants.tool import *
from tnbits.base.transformer import *

class ImportDialog(object):
    """Dialog to import a design space."""


    def __init__(self, controller, callback, width=200, height=100):
        """Shows a pop up with existing design space names and a getFile
        button to open a design space file.

        controller: window calling up the dialog
        callback: controller function to be called after selection.
        """
        self.controller = controller
        self.title = 'Import a design space to family %s' % self.controller.family.name
        self.callback = callback
        self.width = width
        self.height = height
        self.path = None
        dialogSize = (self.width, self.height)
        self.window = Sheet(dialogSize, controller.tool.getWindow())

        x = PADDING
        y = PADDING
        w = self.width - 2*PADDING
        h = BUTTON_HEIGHT
        names = self.controller.family.getSortedDesignSpaceNames()
        self.designSpaceName = names[0]
        self.window.selectDesignSpace = PopUpButton((x, y, w, h),
                names,
                sizeStyle=S, callback=self.setDesignSpace)
        y += h
        self.window.selectSampleFile = Button((x, y, w, h), 'Select Designspace File',
                sizeStyle=S, callback=self.getPathCallback)
        y += h
        l = self.window.pathLabel = TextBox((x, y, w, h), '')
        l.getNSTextField().setLineBreakMode_(NSLineBreakByTruncatingMiddle)
        pos = (-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.cancel = Button(pos, "Cancel", callback=self.close)
        pos = (2*-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.okay = Button(pos, "Okay", callback=self.okay)
        self.window.okay.getNSButton().setEnabled_(False)
        self.window.open()

    # Callbacks.

    def getFamily(self):
        return self.controller.family

    def okay(self, sender):
        self.callback(self.designSpaceName, self.path)
        self.closeWindow()

    def close(self, sender):
        self.callback(None, None)
        self.closeWindow()

    def closeWindow(self):
        if self.window is not None:
            self.window.close()

    def getPathCallback(self, sender):
        msg = 'Please select a designspace file...'
        paths = getFile(messageText=msg,
                        title=msg,
                        allowsMultipleSelection=False,
                        fileTypes=('designspace',))

        if paths is not None:
            self.path = paths[0]
            self.window.pathLabel.set(self.path)
        self.checkOkay()

    # Set.

    def setDesignSpace(self, sender):
        i = int(sender.get())
        family = self.getFamily()
        self.designSpaceName = family.getSortedDesignSpaceNames()[i]
        self.checkOkay()

    def checkOkay(self):
        if not self.designSpaceName is None and not self.path is None:
            self.window.okay.getNSButton().setEnabled_(True)
        else:
            self.window.okay.getNSButton().setEnabled_(False)
