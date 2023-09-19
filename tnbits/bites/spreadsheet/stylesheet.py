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
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.base.constants.tool import *
from tnbits.base.view import View
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell
from tnbits.bites.spreadsheet.constants import *

W = 5 * UNIT + PADDING

class StyleSheet(View):

    def __init__(self, parent, pos=(0, 0, -0, -0), cellChangedCallback=None):
        self.parent = parent
        self.cellChangedCallback = cellChangedCallback
        self.descriptions = None
        self.view = Group(pos)
        self.setSpreadsheet()

    def getController(self):
        return self.parent.controller

    def setSpreadsheet(self):
        self.descriptions = self.getDescriptions()
        self.identifierKey = self.descriptions[0]['key']
        data = self.getData()
        self.spreadsheet = Spreadsheet(self, descriptions=self.descriptions,
                data=data, cellChangedCallback=self.cellChangedCallback,
                doubleClickCallback=self.doubleClickCallback,
                menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    def getMenuItems(self):
        l =  [
                dict(title='Scan', callback='scanCallback:'),
                dict(title='Open', callback='openCallback:', shortcut='O'),
                dict(title='Add to Design Space', callback='addCallback:',
                    shortcut='A'),
            ]
        ds = self.getDesignSpace()

        if not ds is None:
            d = dict(title='Remove from Design Space',
                    callback='removeCallback:', shortcut='R')
            l.append(d)

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
            style = self.getStyle(styleKey)
            #print(type(style))
            sa = analyzerManager.getStyleAnalyzer(styleKey)

            if ds:
                # Checks if the style is a master in the current design space.
                isMaster = ds.isMaster(styleKey)

                if not isMaster:
                    continue

            '''
            else:
                # Checks if the style is not in any of the existing design
                # spaces.
                isMaster = False

                for designSpaceName in family:
                    ads = family[designSpaceName]

                    if ads.isMaster(styleKey):
                        isMaster = True
                        break

                if isMaster:
                    continue
            '''

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

            #d = getFontInfoDict(style, attrs)

            for header in STYLES_HEADERS:
                if header == 'Units Per Em':
                    value = style.info.unitsPerEm
                elif header == 'Ascender':
                    value = style.info.ascender
                elif header == 'Descender':
                    value = style.info.ascender
                elif header == 'Descender':
                    value = style.info.ascender
                elif header == 'Cap Height':
                    value = style.info.capHeight
                elif header == 'X Height':
                    value = style.info.xHeight
                elif header == 'X Height':
                    value = style.info.xHeight
                elif header == 'Italic Angle':
                    value = style.info.italicAngle
                elif header == 'Smallcap Height':
                    value = sa.scapHeight
                elif header == 'Glyphs':
                    value = len(style)
                else:
                    value = None

                l.append(Cell(identifier=(x, y), value=value))
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

        for header in STYLES_HEADERS:
            d = dict(title=header, key=header, editable=True, isAxis=True)
            descriptions.append(d)

        return descriptions

    def getStyleID(self, cell):
        """Gets the style ID stored in the cell value"""
        x, y = cell.identifier
        cellID = (0, y)
        cell = self.spreadsheet[cellID]
        return cell.value

    def getStyleKey(self, cell):
        styleID = self.getStyleID(cell)
        family = self.getFamily()
        return (family.familyID, styleID)

    def openCallback_(self, menuItem):
        cellID = self.spreadsheet.currentCell
        cell = self.spreadsheet[cellID]
        styleKey = self.getStyleKey(cell)
        self.getController().openStyle([styleKey])

    def addCallback_(self, menuItem):
        cellID = self.spreadsheet.currentCell
        cell = self.spreadsheet[cellID]
        styleKey = self.getStyleKey(cell)
        controller = self.getController()
        controller.openAddDialog(styleKey)

    def removeCallback_(self, menuItem):
        cellID = self.spreadsheet.currentCell
        cell = self.spreadsheet[cellID]
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

    def scanCallback_(self, menuItem):
        cellID = self.spreadsheet.currentCell
        self.doubleClickCallback(cellID)

    def doubleClickCallback(self, cellID):
        x, y = cellID
        cell = self.spreadsheet[(0, y)]
        name = cell.value
        family = self.getFamily()
        styleKey = (family.familyID, name)
        controller = self.getController()
        controller.reset()
        cellID = self.spreadsheet.currentCell
        controller.setStyle(styleKey)
