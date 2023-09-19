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
#    instances.py
#

from AppKit import NSDragOperationMove
from vanilla import List, Group, TextBox, SegmentedButton
from tnbits.base.constants.tool import *
from tnbits.base.dialogs.styleselectiondialog import StyleSelectionDialog
from tnbits.base.transformer import *

W = 5*UNIT + PADDING

class Instances(object):
    """Implements GUI for the design space instances."""

    def __init__(self, controller, family, designSpace, pos=(0, 0, -0, -0),
            doubleClickCallback=None, selectionCallback=None,
            editCallback=None):
        """Builds the style list."""
        self.controller = controller
        self.family = family
        self.designSpace = designSpace
        self.numberOfItems = 0
        self.dialog = None
        self.view = Group(pos)
        self.view.title = TextBox((PADDING, PADDING, W, 2*UNIT), 'instances',
                sizeStyle='small')
        self.view.addRemoveButton = SegmentedButton((PADDING, PADDING + 2*UNIT, W, 2*UNIT),
                segmentDescriptions=PLUSMIN, selectionStyle="momentary",
                callback=self.addRemove)
        self.setList(doubleClickCallback=doubleClickCallback,
                selectionCallback=selectionCallback, editCallback=editCallback)

    # Get.

    def getDragSettings(self):
        return dict(type="myInternalDragQAType", callback=None)

    def getSelfDropSettings(self):
        return dict(type="myInternalDragQAType",
                callback=self.dropRearrange,
                operation=NSDragOperationMove)

    def getList(self):
        """Returns Vanilla list object."""
        return self.l

    def getView(self):
        return self.view

    def get(self):
        """Returns Vanilla list contents."""
        return self.l.get()

    def getSelection(self):
        """Returns Vanilla list selection."""
        return self.l.getSelection()

    def getDescriptions(self):
        """Sets headers and data structure."""
        # TODO: generate descriptor based on actual axis names.
        descriptions = []
        d = dict(title='File', key='styleName', width=200, editable=False)
        descriptions.append(d)

        for axisTag, axis in self.designSpace.getAxes().items():
            d = dict(title=axis['name'], key=axisTag, width=200, editable=True)
            descriptions.append(d)

        return descriptions

    def getSortedItems(self):
        """Answers the list of style items, sorted by their current order in
        the view."""
        arrayController = self.l._arrayController
        unsortedArray = arrayController.content()
        sortDescriptors = arrayController.sortDescriptors()

        if sortDescriptors:
            # Sorting has been done. therefore, unsorting needs to be done.
            unsortedArray = unsortedArray.sortedArrayUsingDescriptors_(sortDescriptors)

        return unsortedArray

    def getSelectedKeys(self):
        """Returns (familyPath, filename) pairs in a list."""
        styleKeys = []
        selections = self.l.getSelection()

        for selection in selections:
            selectedItem = self.l[selection]
            styleKeys.append(selectedItem['styleKey'])

        return styleKeys

    def getAllIds(self):
        """Answers ID's of all the styles in the list."""
        styleIDs = []
        styleKeys = self.getAllKeys()

        for key in styleKeys:
            styleIDs.append(key[1])

        return styleIDs

    def getAllKeys(self):
        """Answers all styleKeys in the list. NOTE: does this give the
        same results as self.family.getStyleKeys()?"""
        styleKeys = []
        designSpace = self.controller.getDesignSpace()
        items = self.getItems(self.controller.family, designSpace)

        for i in items:
            styleKeys.append(i['styleKey'])

        return styleKeys

    def getItems(self, formats=None):
        """Gets styles as items to fill the list. Looks if a master is
        available and skips unwanted file types."""
        items = []

        # Default formats.
        if formats is None:
            formats = ['ufo', 'ttf', 'otf', 'woff']

        ids = self.family.getStyleIDs()

        for styleID in ids:
            if not isAFormatOf(styleID, formats):
                continue

            styleKey = self.family.familyID, styleID
            d = dict(styleKey=styleKey, styleName=styleKey[1])
            isInstance = self.designSpace.isInstance(styleKey)

            if not isInstance:
                continue

            for axisTag, axis in self.designSpace.getAxes().items():
                value = self.designSpace.getStyleInterpolationAxis(styleKey, axisTag)
                d[axis['name']] = value

            items.append(d)

        return items

    # List.

    def setList(self, doubleClickCallback=None, selectionCallback=None,
            editCallback=None):
        pos = (W, 0, -0, -0)
        dragSettings = self.getDragSettings()
        selfDropSettings = self.getSelfDropSettings()
        descriptions = self.getDescriptions()

        self.l = List(pos, [],
            doubleClickCallback=doubleClickCallback,
            selectionCallback=selectionCallback,
            editCallback=editCallback,
            dragSettings=dragSettings,
            #allowsSorting=True, # Set to True if the column sorting bug is solved.
            drawFocusRing=False,
            enableDelete=False,
            allowsMultipleSelection=True,
            allowsEmptySelection=True,
            #drawHorizontalLines=True,
            showColumnTitles=True,
            selfDropSettings=selfDropSettings,
            columnDescriptions=descriptions,
            rowHeight=18,
        )
        self.view.l = self.l
        self.setItems(formats=['ufo'])

    def setItems(self, formats=None):
        """Gets family styles as items and loads them into the list."""
        items = self.getItems(formats=formats)
        self.l.set(items)
        self.numberOfItems = len(items)

    def deleteList(self):
        del self.view.l

    def resetList(self):
        self.deleteList()
        self.setList()

    # Callbacks.

    def addRemove(self, sender):
        if sender.get() == 0:
            if self.dialog is None:
                self.dialog = StyleSelectionDialog(self, self.family,
                        self.designSpace, self.addInstance)
            else:
                # Bring to front.
                pass
        elif sender.get() == 1:
            # TODO: hook up to dialog.
            selection = self.getSelectedKeys()

            for styleKey in selection:
                self.designSpace.notInstance(styleKey)
                self.setItems()
            self.designSpace.save()

    def addInstance(self, selection):
        self.dialog = None

        if selection:
            for styleKey in selection:
                self.designSpace.asInstance(styleKey)
            self.setItems()
            self.designSpace.save()

    def editCallback(self, sender):
        """Order of the list changed, update the sort order in the current
        constellation.

        DEPRECATED.
        TODO: implement actual editable cells.
        """
        sortedKeys = []

        for item in self.getSortedItems():
            sortedKeys.append(item['styleKey'])

        self.controller.family.setStyleKeys(sortedKeys)
        self.controller.family.save()

    def dropRearrange(self, sender, dropInfo):
        """A drag/drop was performed on one or more elements of the style
        list. Rebuilds the ordered list of styleIDs and saves the new ordered
        list in the family.storage."""
        dropped = not dropInfo["isProposal"]

        if dropped:
            # Resets the sort descriptors because they are no longer
            # automatically sorted. TODO: does this still hold after
            # a new autosort?
            arrayController = sender._arrayController
            arrayController.setSortDescriptors_(())

            rowIndex = dropInfo["rowIndex"]
            movedItems = dropInfo['data']
            newKeyOrder = []

            for index, styleItem in enumerate(self.l):
                # This is the dropping index, insert the moved items here.
                if rowIndex == index:
                    for movedItem in movedItems:
                        # Keep StyleKey to update family style ordering.
                        newKeyOrder.append(movedItem['styleKey'])

                skipItem = False # Test if our current item is part of the moving pack.

                for movedItem in movedItems:
                    if styleItem['styleKey'] == movedItem['styleKey']:
                        skipItem = True
                        break

                # If this styleID is not moved, then continue to copy the list
                # in original order.
                if not skipItem:
                    # Keep StyleKey to update family style ordering.
                    newKeyOrder.append(styleItem['styleKey'])

            # Make sure to save the altered order into the .fam file.
            self.controller.setFamilyOrder(newKeyOrder)

        return True
