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
#    controller.py
#

from tnbits.base.controller import BaseController
from tnbits.model.objects.glyph import getContours, getComponents
from tnbits.bites.examplesheet.constants import *
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell

class Controller(BaseController):
    """Implements internal logic between various parts of the Sheet."""

    def __init__(self, tool, mode='tool'):
        """Adds the spreadsheet to a view and loads some font data."""

        self.i = 0
        self.tool = tool
        self.mode = mode
        view = self.tool.getWindow()
        view.spreadsheet = Spreadsheet(self, (0, 0, -5, -5),
                self.getGlyphDescriptor(), data=self.getTestData(),
                cellChangedCallback=self.cellChangedCallback,
                doubleClickCallback=self.doubleClickCallback,
                singleClickCallback=self.singleClickCallback,
                minScale=0.25,
                maxScale=2, menuItems=self.getMenuItems())

        self.loadData()
        #self.tools = Tools(self)

    def defaultCallback_(self, menuItem):
        print('default callback')
        print(menuItem)

    def setFamily(self, family):
        pass

    def getGlyphDescriptor(self):
        """Descriptors for glyph header."""
        return [
            dict(title="Glyph Name", width=150, key="name", editable=False),
            dict(title="Unicode", width=80, key="unicode", format="%04X"),
            dict(title="Width", width=80, key="width"),
            dict(title="LSB", width=80, key="leftMargin"),
            dict(title="RSB", width=80, key="rightMargin"),
            dict(title="Contours", width=80, key='contours', editable=False), # , method=self.getContours
            dict(title="Components", width=80, key='components', editable=False), # , method=self.getComponents
        ]

    def getMenuItems(self):
        #return [dict(title="Default", callback="defaultCallback:", shortcut="M")]
        return [dict(title='Open', callback='openGlyphCallback:', shortcut='O'),
                dict(title='Insert After', callback='insertGlyphCallback:', shortcut='I'),
                dict(title='Delete', callback='deleteGlyphCallback:', shortcut='d')
                ]

    def getTestData(self):
        """Gets glyphs from style including attributes."""
        glyphDescriptor = self.getGlyphDescriptor()
        data = []
        l = 13
        i0 = self.i * l
        i1 = (self.i + 1) * l

        if i1 > len(glyphData):
            i1 = len(glyphData) + 1
            self.i = 0
        else:
            self.i += 1


        subset = glyphData[i0:i1]

        for cellY, values in enumerate(subset):
            line = []
            glyphname = values[0]

            for cellX, value in enumerate(values):
                cell = Cell(value)
                cell.glyphName = glyphname
                cell.identifier = cellX, cellY
                line.append(cell)
            data.append(line)

        return data

    def loadData(self):
        """Updates the spreadsheet view."""
        view = self.tool.getWindow()
        view.spreadsheet.set(self.getTestData())

    # Callbacks.

    def cellChangedCallback(self, cell):
        """Callback for cell update."""
        print('callback for cell %s' % str(cell))

    def doubleClickCallback(self, cell):
        print('doubleClickCallback() for cell %s' % str(cell))

    def singleClickCallback(self, cell):
        print('singleClickCallback() for cell %s' % str(cell))
        self.loadData()

    def openGlyphCallback_(self, value):
        print('openGlyphCallback() on %s' % value)

    def deleteGlyphCallback_(self, value):
        print('deleteGlyphCallback() on %s' % value)

    def insertGlyphCallback_(self, value):
        print('insertGlyphCallback() on %s' % value)

    # Attribute / property getters.

    def getContours(self, glyph):
        return len(getContours(glyph))

    def getComponents(self, glyph):
        return len(getComponents(glyph))
