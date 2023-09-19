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
#    dropdowndialog.py
#

from vanilla import Window, TextBox, Button, ComboBox

class DropDownDialog(object):
    """
    Drop down selection dialog.
    """

    def __init__(self, parent, title, values, callback, width=250, height=150):
        """
        parent: window calling up the dialog
        title: dialog title
        values: list of values to be passed to the drop down (ComboBox).
        callback: parent function to be called after selection.
        """
        self.parent = parent
        self.title = title
        self.values = values
        self.callback = callback
        self.width = width
        self.height = height

    def open(self, msg):
        dialogSize = (self.width, self.height)
        self.window = Window(dialogSize, self.title, minSize=dialogSize,
                maxSize=dialogSize)
        self.window.message = TextBox((20, 20, self.width-40, 30), msg)
        self.window.selectReference = ComboBox((20, 50, self.width-40, 30), self.values, callback=self.confirmSelectionCallback)
        self.window.selectReference.set('--')
        self.window.cancel = Button((self.width-90, 100, 60, 20), "Cancel",
                callback=self.close)
        self.window.open()

    def confirmSelectionCallback(self, sender):
        selected = sender.get()
        self.callback(selected)
        self.close(sender)

    def close(self, sender):
        if self.window is not None:
            self.window.close()
