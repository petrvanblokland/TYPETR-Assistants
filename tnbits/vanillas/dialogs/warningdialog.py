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
#    warningdialog.py
#

from vanilla import Window, TextBox, Button

class WarningDialog(object):
    """
    Adds a warning message dialog to a tool.
    """

    def openWarningDialog(self, message):
        dialogSize = (250, 150)
        self.warningDialog = Window(dialogSize, "Warning", minSize=dialogSize,
                maxSize=dialogSize)
        self.warningDialog.message = TextBox((20, 60, 210, 30), message)
        self.warningDialog.okay = Button((160, 100, 60, 20), "Okay",
                callback=self.closeWarningDialog)
        self.warningDialog.open()

    def closeWarningDialog(self, sender):
        if self.warningDialog is not None:
            self.warningDialog.close()
