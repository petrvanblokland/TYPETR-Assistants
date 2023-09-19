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
#    masters.py
#
from vanilla import Group
from tnbits.base.constants.tool import *
from tnbits.base.transformer import *
from tnbits.base.dialogs.styleselectiondialog import StyleSelectionDialog
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell
from tnbits.qualityassurance.variations import *

W = 5*UNIT + PADDING

class Masters(object):
    """Implements GUI for the design space masters."""

    def __init__(self, parent, pos=(0, 0, -0, -0),
            cellChangedCallback=None):
        """Builds the masters spreadsheet."""
        self.parent = parent
        self.dialog = None
        self.identifierKey = None
        self.descriptions = None
        self.view = Group(pos)
        self.setSpreadsheet()

    # Get.

    # TODO: share in base class.
    def getView(self):
        return self.view

    def getDesignSpace(self):
        return self.getController().getDesignSpace()

    def getFamily(self):
        return self.getController().getFamily()

    def getController(self):
        return self.parent.controller

    def get(self):
        """Returns spreadsheet data."""
        return self.spreadsheet.get()

    def getDescriptions(self):
        """Sets headers and data structure."""
        descriptions = []
        d = dict(title='Master', key='master', width=400, editable=False, isAxis=False)
        descriptions.append(d)
        d = dict(title='Neutral', key='neutral', editable=False, isAxis=False)
        descriptions.append(d)
        ds = self.getDesignSpace()

        if ds:
            for axisTag, axis in ds.getAxes().items():
                d = dict(title=axis['name'], key=axisTag, editable=True, isAxis=True)
                descriptions.append(d)

        return descriptions

    def getSelection(self):
        """Returns spreadsheet selection."""
        return self.spreadsheet.getSelection()

    def getSelectedKeys(self):
        """Returns style keys for all selected rows."""
        # TODO: move to shared  styles sheet class.
        styleKeys = []
        ys = self.spreadsheet.getSelectionYs()

        for y in ys:
            styleKey = self.getStyleKeyByY(y)
            styleKeys.append(styleKey)

        return styleKeys

    def getStyleKeyByCell(self, cell):
        # TODO: move to shared  styles sheet class.
        _, y = cell.identifier
        return self.getStyleKeyByY(y)

    def getStyleKeyByY(self, y):
        # TODO: move to shared  styles sheet class.
        x = self.spreadsheet.getColumnIndex(self.identifierKey)
        cell = self.spreadsheet[(x, y)]
        styleName = cell.value
        family = self.getFamily()
        return (family.familyID, styleName)

    def getData(self, formats=None):
        """Gets styles as items to fill the list. Looks if a master is
        available and skips unwanted file types."""
        data = []
        ds = self.getDesignSpace()
        family = self.getFamily()

        if ds is None:
            return data

        # Default formats.
        if formats is None:
            formats = ['ufo', 'ttf', 'otf', 'woff']

        ids = family.getStyleIDs()
        y = 0

        for styleId in ids:
            if not isAFormatOf(styleId, formats):
                continue

            styleKey = family.familyID, styleId
            isMaster = ds.isMaster(styleKey)

            if not isMaster:
                continue

            x = 0
            c0 = Cell(identifier=(x, y), value=styleId)
            l = [c0]
            x += 1

            if styleKey[1] == ds.origin:
                value = u'•'
            else:
                value = ''

            c1 = Cell(identifier=(x, y), value=value)
            l.append(c1)
            x += 1

            # FIXME: should be sorted.
            for axisTag, axis in ds.getAxes().items():
                enabled = axis['enabled']
                value = ds.getStyleInterpolationAxis(styleKey, axisTag)
                l.append(Cell(identifier=(x, y), value=value, enabled=enabled))
                x += 1

            data.append(l)
            y += 1

        return data

    def getMenuItems(self):
        return [
                dict(title='Open', callback='openCallback:'),
                dict(title='Add', callback='addCallback:'),
                dict(title='Neutral', callback='neutralCallback:'),
                dict(title='Compare', callback='compareCallback:'),
                dict(title='Fix', callback='fixCallback:'),
                dict(title='Remove', callback='removeCallback:'),
            ]

    # Set.

    def setSpreadsheet(self):
        self.descriptions = self.getDescriptions()
        self.identifierKey = self.descriptions[0]['key']
        data = self.getData()
        self.spreadsheet = Spreadsheet(self, descriptions=self.descriptions,
                data=data, cellChangedCallback=self.cellChangedCallback,
                doubleClickCallback=self.doubleClickCallback,
                menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    def neutralCallback_(self, menuItem):
        cellID = self.spreadsheet.currentCell
        cell = self.spreadsheet[cellID]
        styleKey = self.getStyleKeyByCell(cell)
        ds = self.getDesignSpace()
        ds.asOrigin(styleKey)
        ds.save()
        self.update()

    # Delete and reset.

    def deleteSpreadsheet(self):
        del self.view.spreadsheet

    def update(self):
        """
        TODO: reload spreadsheet contents without deleting.
        """
        self.deleteSpreadsheet()
        self.setSpreadsheet()
        self.parent.prompt.setLines()

    # Callbacks.

    def doubleClickCallback(self, cell):
        x, y = cell

        if x == 0:
            styleKeys = self.getSelectedKeys()
            self.getController().openStyle(styleKeys)
        else:
            self.spreadsheet.openEditCell(cell)

    def addCallback_(self, menuItem):
        ds = self.getDesignSpace()
        family = self.getFamily()

        if self.dialog is None:
            self.dialog = StyleSelectionDialog(self, family,
                    ds, self.addMaster)
        else:
            # TODO: Bring to front.
            pass

    def addMaster(self, selection):
        self.dialog = None
        ds = self.getDesignSpace()

        if selection:
            for styleKey in selection:
                ds.asMaster(styleKey)
            self.update()
            ds.save()

    def openCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        self.getController().openStyle(styleKeys)

    def compareCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        stylesDict = self.getController().getStylesDict(styleKeys)
        messages = compareMasters(stylesDict)
        messages = self.compareAxes(styleKeys, messages)
        self.parent.updatePrompt(messages)

    def getAxesList(self):
        axesList = []

        for d in self.descriptions:
            if d['isAxis'] is True:
                axesList.append(d['key'])

        return axesList

    def compareAxes(self, styleKeys, messages):
        ds = self.getDesignSpace()

        for styleKey in styleKeys:
            base = True
            for axisTag, axis in ds.getAxes().items():
                value = ds.getStyleInterpolationAxis(styleKey, axisTag)

                if value != 0:
                    base = False
                    continue

            if base:
                messages.append('%s is base' % styleKey[1])

        return messages

    def fixCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        stylesDict = self.getController().getStylesDict(styleKeys)
        messages = fixMasters(stylesDict)
        self.parent.updatePrompt(messages)

    def removeCallback_(self, menuItem):
        ds = self.getDesignSpace()
        styleKeys = self.getSelectedKeys()

        for styleKey in styleKeys:
            ds.notMaster(styleKey)

        ds.save()
        self.update()

    def cellChangedCallback(self, cell):
        styleKey = self.getStyleKeyByCell(cell)
        cellX, _ = cell.identifier
        key = self.descriptions[cellX]['key']
        value = int(cell.value)
        ds = self.getDesignSpace()
        ds.setStyleInterpolationAxis(styleKey, key, value)
        ds.save()
