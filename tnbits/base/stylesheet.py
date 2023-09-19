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

from tnbits.base.view import View
from vanilla import Group
from tnbits.spreadsheet.cell import Cell
from tnbits.spreadsheet.spreadsheet import Spreadsheet

class StyleSheet(View):
    """Shared functions for view that contain a styles spreadsheet."""

    def __init__(self, controller, pos=(0, 0, -0, -0)):
        super(StyleSheet, self).__init__()
        self.controller = controller
        self.descriptions = None
        self.view = Group(pos)

    def __len__(self):
        return len(self.spreadsheet)

    def set(self, searchString=None):
        """Sets the spreadsheet data. See also update()."""
        self.descriptions = self.getDescriptions()
        data = self.getData(searchString=searchString)
        self.identifierKey = self.descriptions[0]['key']
        self.spreadsheet = Spreadsheet(self, descriptions=self.descriptions,
                data=data, cellChangedCallback=self.cellChangedCallback,
                singleClickCallback=self.singleClickCallback,
                doubleClickCallback=self.doubleClickCallback,
                orderCallback=self.orderCallback,
                menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    def update(self, searchString=None):
        """"""
        data = self.getData(searchString=searchString)
        self.view.spreadsheet.set(data)

    def getController(self):
        return self.controller

    def getData(self, formats=None, searchString=None):
        """Puts style data in a list of spreadsheet cells."""
        data = []
        family = self.getFamily()
        y = 0

        if family is None:
            return data

        IDs = family.getStyleIDs()
        ds = self.getDesignSpace()

        for styleID in IDs:
            if searchString and not searchString.lower() in styleID.lower():
                continue

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

            v2 = None
            isOpen = family.styleIsOpen(styleKey)
            if isOpen:
                v = '+'
                style = family.getStyle(styleKey)
                dirty = style.naked().dirty
                if dirty:
                    v2 = '+'

            else:
                v = '-'

            l.append(Cell(identifier=(x, y), value=v))
            x += 1
            l.append(Cell(identifier=(x, y), value=v2))
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

        d = dict(title='Open', key='open', width=40,
                editable=False, isAxis=False)
        descriptions.append(d)
        d = dict(title='Dirty', key='dirty', width=40,
                editable=False, isAxis=False)
        descriptions.append(d)

        ds = self.getDesignSpace()

        if ds:
            for axisTag, axis in ds.getAxes().items():
                d = dict(title=axis['name'], key=axisTag, editable=True, isAxis=True)
                descriptions.append(d)

        return descriptions

    # Selections, keys and IDs.

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

    def getSelectedIDs(self):
        styleIDs = []

        for cellID in self.getSelection():
            styleID = self.getStyleID(cellID)
            styleIDs.append(styleID)

        return styleIDs

    # def getAllKeys(self):

    def getAllIDs(self):
        styleIDs = []

        for cellID in self.spreadsheet.getColumnIDs(0):
            styleID = self.getStyleID(cellID)
            styleIDs.append(styleID)

        return styleIDs

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

    def orderCallback(self, order):
        styleIDs = []

        for i in order:
            cellID = (0, i)
            styleID = self.getStyleID(cellID)
            styleIDs.append(styleID)

        family = self.getFamily()
        family.setStyleIDs(styleIDs)
        self.update()
