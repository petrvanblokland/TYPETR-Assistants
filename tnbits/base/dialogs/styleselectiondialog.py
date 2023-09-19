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
#    styleselectiondialog.py
#

from vanilla import Window, Button, List
from tnbits.base.constants.tool import *
from tnbits.base.transformer import *

class StyleSelectionDialog(object):
    """Dialog to select styles from the family as masters or instances."""

    def __init__(self, controller, family, designSpace, callback, width=800, height=600):
        """Shows a list of available styles to be selected as a master or
        instance in the family.

        controller: window calling up the dialog.
        family: the font family.
        designSpace: selected design space for the family.
        callback: controller function to be called after selection.
        """
        self.controller = controller
        self.family = family
        self.designSpace = designSpace
        self.title = 'Free styles in family %s' % family.name
        self.callback = callback
        self.width = width
        self.height = height
        self.numberOfItems = 0
        dialogSize = (self.width, self.height)
        self.window = Window(dialogSize, self.title, minSize=dialogSize,
                maxSize=dialogSize)
        pos = (0, 0, -0, -4*UNIT)
        descriptions = self.getDescriptions()
        self.l = List(pos, [],
            doubleClickCallback=self.okay,
            drawFocusRing=False,
            enableDelete=False,
            allowsMultipleSelection=True,
            allowsEmptySelection=True,
            showColumnTitles=True,
            columnDescriptions=descriptions,
            rowHeight=18,
        )
        self.window.l = self.l
        pos = (-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.cancel = Button(pos, "Cancel", callback=self.close)
        pos = (2*-BUTTON_WIDTH-PADDING, -3*UNIT, BUTTON_WIDTH, 2*UNIT)
        self.window.okay = Button(pos, "Okay", callback=self.okay)
        self.setItems()
        self.window.open()

    # Callbacks.

    def okay(self, sender):
        selected = self.getSelectedKeys()
        self.closeWindow()
        self.callback(selected)

    def close(self, sender):
        self.closeWindow()
        self.callback(None)

    def closeWindow(self):
        if self.window is not None:
            self.window.close()

    # Set.

    def setItems(self, formats=None):
        if formats is None:
            formats = ['ufo']
        """Gets family styles as items and loads them into the list."""
        items = self.getItems(formats=formats)
        self.l.set(items)
        self.numberOfItems = len(items)

    # Get.

    def getSelectedKeys(self):
        """Returns style keys in a list."""
        styleKeys = [] # Format (familyPath, fileName)
        selections = self.l.getSelection() # Always need a selection to come here.

        for selection in selections:
            selectedItem = self.l[selection]
            styleKeys.append(selectedItem['styleKey'])

        return styleKeys

    def getSelection(self):
        """Returns Vanilla list selection."""
        return self.l.getSelection()

    def getDescriptions(self):
        """Sets headers and data structure."""
        descriptions = []
        d = dict(title='File', key='styleName', width=200, editable=False)
        descriptions.append(d)
        return descriptions

    def getItems(self, formats=None):
        """Gets styles as items to fill the list. Filters file types. Doesn't
        show masters and instances."""
        if formats is None:
            formats = ['ufo']
        items = []
        ids = self.family.getStyleIDs()

        for styleId in ids:
            if not isAFormatOf(styleId, formats):
                continue

            styleKey = self.family.familyID, styleId
            d = dict(styleKey=styleKey, styleName=styleKey[1])
            isMaster = self.designSpace.isMaster(styleKey)
            isInstance = self.designSpace.isInstance(styleKey)

            if isMaster or isInstance:
                continue

            items.append(d)

        return items
