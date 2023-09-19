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
#    adddialog.py
#
from vanilla import Button, PopUpButton, Sheet
from tnbits.base.constants.tool import *
from tnbits.base.transformer import *

class AddDialog(object):
    """Dialog to add a style to a design space."""


    def __init__(self, controller, styleKey, callback, width=200, height=100):
        """
        controller: window calling up the dialog
        callback: controller function to be called after selection.
        """
        self.controller = controller
        self.styleKey = styleKey
        self.callback = callback
        self.width = width
        self.height = height
        dialogSize = (self.width, self.height)
        self.title = '%s -- add a style to a design space' % self.controller.family.name
        self.window = Sheet(dialogSize, controller.tool.getWindow())

        x = PADDING
        y = PADDING
        w = self.width - 2*PADDING
        h = BUTTON_HEIGHT

        self.names = self.getNames()
        self.designSpaceName = self.names[0]
        self.window.selectDesignSpace = PopUpButton((x, y, w, h), self.names,
                sizeStyle=S, callback=self.setDesignSpace)
        y += h
        pos = (-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.cancel = Button(pos, "Cancel", callback=self.close)
        pos = (2*-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.okay = Button(pos, "Okay", callback=self.okay)
        #self.window.okay.getNSButton().setEnabled_(False)
        self.window.open()

    def getNames(self):
        names = []
        allNames = self.controller.family.getSortedDesignSpaceNames()

        for n in allNames:
            ds = self.controller.family[n]
            if ds.isMaster(self.styleKey):
                continue
            names.append(n)

        return names

    def getFamily(self):
        return self.controller.family

    # Callbacks.

    def okay(self, sender):
        self.callback(self.designSpaceName, self.styleKey)
        self.closeWindow()

    def close(self, sender):
        self.callback(None, None)
        self.closeWindow()

    def closeWindow(self):
        if self.window is not None:
            self.window.close()

    # Set.

    def setDesignSpace(self, sender):
        i = int(sender.get())
        family = self.getFamily()
        self.designSpaceName = self.names[i]
        self.checkOkay()

    def checkOkay(self):
        if not self.designSpaceName is None:
            self.window.okay.getNSButton().setEnabled_(True)
        else:
            self.window.okay.getNSButton().setEnabled_(False)
