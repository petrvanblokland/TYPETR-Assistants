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
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell
from tnbits.bites.spreadsheet.constants import *

W = 5*UNIT + PADDING

class StyleSheet(View):

    def __init__(self, controller, pos=(0, 0, -0, -0), cellChangedCallback=None):
        self.controller = controller
        self.cellChangedCallback = cellChangedCallback
        self.descriptions = None
        self.view = Group(pos)
        self.setSpreadsheet()

    def getController(self):
        return self.controller

    def setSpreadsheet(self):
        self.descriptions = self.getDescriptions()
        self.identifierKey = self.descriptions[0]['key']
        data = self.getData()
        self.spreadsheet = Spreadsheet(self, descriptions=self.descriptions,
                data=data, cellChangedCallback=self.cellChangedCallback,
                singleClickCallback=self.singleClickCallback,
                doubleClickCallback=self.doubleClickCallback,
                menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    def getMenuItems(self):
        l =  [
                dict(title='Extract', callback='extractCallback:'),
                dict(title='Open', callback='openCallback:'),
            ]

        return l

    def getData(self, formats=None):
        """
        """
        data = []
        family = self.getFamily()
        y = 0

        if family is None:
            return data

        ids = family.getStyleIDs()
        ds = self.getDesignSpace()

        for styleId in ids:
            styleKey = family.familyID, styleId

            if ds:
                # Checks if the style is a master in the current design space.
                isMaster = ds.isMaster(styleKey)

                if not isMaster:
                    continue

            x = 0
            c0 = Cell(identifier=(x, y), value=styleId)
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

        for cellID in self.getSelection():
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

    def openCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        self.getController().openStyle(styleKeys)

    def addCallback(self, cell):
        styleKey = self.getStyleKey(cell)
        controller = self.getController()
        controller.openAddDialog(styleKey)

    def removeCallback(self, cell):
        styleID = self.getStyleID(cell)
        family = self.getFamily()
        styleKey = (family.familyID, styleID)
        controller = self.getController()
        controller.removeFromDesignSpace(styleKey)

    def update(self):
        """
        TODO: reload spreadsheet contents without deleting.
        """
        self.deleteSpreadsheet()
        self.setSpreadsheet()

    def deleteSpreadsheet(self):
        del self.view.spreadsheet

    def extractCallback_(self, menuItem):
        controller = self.getController()
        styleKeys = self.getSelectedKeys()

        for styleKey in styleKeys:
            controller.extract(styleKey=styleKey)

    def singleClickCallback(self, cellID):
        controller = self.getController()
        styleKey = self.getStyleKey(cellID)
        controller.setStyle(styleKey)

    def doubleClickCallback(self, cellID):
        controller = self.getController()
        styleKey = self.getStyleKey(cellID)
        controller.extract(styleKey=styleKey)
