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
#    stylesheet.py
#

from vanilla import Group
from tnbits.base.constants.tool import *
from tnbits.base.view import View
#from tnbits.base.stylesheet import StyleSheet
from tnbits.bites.spreadsheet.constants import *
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell

W = 5*UNIT + PADDING

class StyleSheet(View):
# TODO: inherit from base.
#class ProofStyleSheet(StyleSheet):

    def __init__(self, controller, pos=(0, 0, -0, -0), cellChangedCallback=None):
        self.controller = controller
        self.cellChangedCallback = cellChangedCallback
        self.descriptions = None
        self.view = Group(pos)
        self.set()

    def update(self):
        """Updates stylesheet data."""
        data = self.getData()
        self.spreadsheet.set(data)

    def getController(self):
        return self.controller

    def set(self):
        self.descriptions = self.getDescriptions()
        self.identifierKey = self.descriptions[0]['key']
        data = self.getData()
        self.spreadsheet = Spreadsheet(self, descriptions=self.descriptions,
                data=data, cellChangedCallback=self.cellChangedCallback,
                singleClickCallback=self.singleClickCallback,
                doubleClickCallback=self.doubleClickCallback,
                orderCallback=self.orderCallback,
                menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    def sortCallback_(self, menuItem):
        self.controller.sortFamilyCallback(None)

    def getMenuItems(self):
        l =  [
                dict(title='Proof', callback='proofCallback:'),
                dict(title='Sort', callback='sortCallback:'),
                dict(title='Open Family', callback='openFamilyCallback:'),
                dict(title='Close Family', callback='closeFamilyCallback:'),
                #dict(title='Add to Design Space', callback=self.addCallback),
            ]

        if self.controller.getMode() == 'tool':
            d = dict(title='Edit', callback='editCallback:')
            l.append(d)

        ds = self.getDesignSpace()

        if not ds is None:
            d = dict(title='Remove from Design Space', callback="removeCallback:")
            l.append(d)

        return l

    def getData(self, formats=None):
        """Returns cell data for styles in the family."""
        data = []
        family = self.getFamily()
        y = 0

        if family is None:
            return data

        ids = family.getStyleIDs()
        ds = self.getDesignSpace()

        for styleID in ids:
            styleKey = family.familyID, styleID

            if ds:
                # Checks if the style is a master in the current design space.
                isMaster = ds.isMaster(styleKey)

                if not isMaster:
                    continue

            x = 0
            c0 = Cell(identifier=(x, y), value=styleID)
            l = [c0]
            x += 1

            if ds:
                for axisTag, axis in ds.getAxes().items():
                    enabled = axis['enabled']
                    value = ds.getStyleInterpolationAxis(styleKey, axisTag)
                    l.append(Cell(identifier=(x, y), value=value, enabled=enabled))
                    x += 1

            data.append(l)

            y += 1
        return data

    def getDescriptions(self):
        """Sets headers and data structure."""
        descriptions = []
        d = dict(title='Style', key='name', width=400,
                editable=False, isAxis=False)
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
        family = self.getFamily()
        styleKeys = []
        s = self.getSelection()

        for cellID in sorted(s):
            styleKey = self.getStyleKey(cellID)
            styleKeys.append(styleKey)

        return styleKeys

    def getStyleKey(self, cellID):
        styleID = self.getStyleID(cellID)
        family = self.getFamily()
        return (family.familyID, styleID)

    def getStyleID(self, cellID):
        """Gets the style ID stored in the cell value"""
        x, y = cellID
        cellID = (0, y)
        cell = self.spreadsheet[cellID]
        return cell.value

    def editCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        self.getController().editStyleKeys(styleKeys)

    def addCallback_(self, menuItem):
        cell = self.spreadsheet.currentCell
        styleKey = self.getStyleKey(cell)
        controller = self.getController()
        controller.openAddDialog(styleKey)

    def removeCallback_(self, menuItem):
        cell = self.spreadsheet.currentCell
        styleID = self.getStyleID(cell)
        family = self.getFamily()
        styleKey = (family.familyID, styleID)
        controller = self.getController()
        controller.removeFromDesignSpace(styleKey)

    # Callbacks.

    def proofCallback_(self, menuItem):
        controller = self.getController()
        controller.proof()

    def singleClickCallback(self, cellID):
        controller = self.getController()
        styleKey = self.getStyleKey(cellID)
        controller.setStyle(styleKey)

    def doubleClickCallback(self, cellID):
        controller = self.getController()
        controller.proof()

    def openFamilyCallback_(self, menuItem):
        controller = self.getController()
        controller.openFamily()

    def closeFamilyCallback_(self, menuItem):
        controller = self.getController()
        controller.closeFamily()

    def orderCallback(self, order):
        styleIDs = []

        for i in order:
            cellID = (0, i)
            styleID = self.getStyleID(cellID)
            styleIDs.append(styleID)

        family = self.getFamily()
        family.setStyleIDs(styleIDs)
        self.update()
