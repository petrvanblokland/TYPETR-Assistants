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
#    spreadsheetview.py
#

from vanilla import Group
from tnbits.base.view import View
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell

class SpreadsheetView(View):

    def __init__(self, parent, pos=(0, 0, -0, -0)):
        self.parent = parent
        self.view = Group(pos)
        posSize = (0, 20, -0, -0)
        descriptions = self.getDescriptions()
        self.leftGroupName = None
        self.rightGroupName = None
        self.spreadsheet = Spreadsheet(self, descriptions=descriptions,
                    posSize=posSize, data=[], cellChangedCallback=None,
                    doubleClickCallback=self.doubleClickCallback,
                    menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    # Get.

    def getMenuItems(self):
        return [
                dict(title='Add', callback='addCallback:'),
                dict(title='Remove', callback='removeCallback:'),
                dict(title='Edit', callback='editCallback:'),
                dict(title='Set as Text', callback='setTextCallback:'),
        ]

    def getDescriptions(self, leftGroupName='kern1', rightGroupName='kern2'):
        """Sets headers and data structure."""
        descriptions = []

        for h in (leftGroupName, rightGroupName):
            d = dict(title=h, key=h.lower(), width=200, editable=False)
            descriptions.append(d)

        return descriptions

    # Set.

    def setData(self,  data):
        leftGroupName, rightGroupName, d = data
        self.leftGroupName = leftGroupName
        self.rightGroupName = rightGroupName
        descriptions = self.getDescriptions(leftGroupName, rightGroupName)
        del self.view.spreadsheet
        posSize = (0, 0, -0, -0)
        self.spreadsheet = Spreadsheet(self, descriptions=descriptions,
                    posSize=posSize, data=d, cellChangedCallback=None,
                    doubleClickCallback=self.doubleClickCallback,
                    menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    # Callbacks.

    def doubleClickCallback(self, cellID):
        if cellID[0] == 0:
            self.parent.clicked(left=True)
        elif cellID[0] == 1:
            self.parent.clicked(left=False)

    def getCurrentGroupName(self):
        cellID = self.spreadsheet.currentCell
        x, _ = cellID
        if x == 0:
            groupName = self.leftGroupName
        elif x == 1:
            groupName = self.rightGroupName
        return groupName

    def getCurrentGlyphName(self):
        groupName = self.getCurrentGroupName()
        cellID = self.spreadsheet.currentCell
        cell = self.spreadsheet[cellID]
        return cell.value

    def editCallback_(self, menuItem):
        cellID = self.spreadsheet.currentCell
        self.doubleClickCallback(cellID)

    def setTextCallback_(self, menuItem):
        s = self.spreadsheet.getSelection()
        glyphNames = []

        if len(s) == 1:
            x = s[0][0]
            print(x)
            col = self.spreadsheet.getColumnIDs(x)
        else:
            col = s

        for cellID in col:
            cell = self.spreadsheet[cellID]
            glyphName = cell.value

            if not glyphName in glyphNames:
                glyphNames.append(glyphName)

        text = '/' + '/'.join(glyphNames)
        self.parent.controller.setSpreadsheetText(text)
        self.parent.controller.update()

    def addCallback_(self, menuItem):
        groupName = self.getCurrentGroupName()
        self.parent.controller.openAddDialog(groupName)

    def removeCallback_(self, menuItem):
        groupName = self.getCurrentGroupName()
        glyphName = self.getCurrentGlyphName()
        self.parent.controller.removeGlyphFromGroup(groupName, glyphName)
