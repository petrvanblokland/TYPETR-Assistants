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

from tnbits.base.constants.tool import *
from tnbits.base.stylesheet import StyleSheet
from tnbits.bites.spreadsheet.constants import *

W = 5*UNIT + PADDING

class QAStyleSheet(StyleSheet):

    def __init__(self, controller, pos=(0, 0, -0, -0), cellChangedCallback=None):
        super(QAStyleSheet, self).__init__(controller, pos)
        self.cellChangedCallback = cellChangedCallback

    def getMenuItems(self):
        l =  [
                dict(title='QA', callback='qaCallback:'),
                dict(title='Set Reference', callback='setReferenceCallback:'),
                dict(title='Sort', callback='sortCallback:'),
                #dict(title='Add to Design Space', callback=self.addCallback),
            ]

        if self.controller.getMode() == 'tool':
            d = dict(title='Edit', callback='editCallback:')
            l.append(d)

        #ds = self.getDesignSpace()

        #if not ds is None: d = dict(title='Remove from Design Space', callback="removeCallback:")
        #    l.append(d)

        return l

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

    def qaCallback_(self, menuItem):
        controller = self.getController()
        controller.qualityAssuranceCallback(None)

    def setReferenceCallback_(self, menuItem):
        controller = self.getController()
        IDs = self.getSelectedIDs()

        if len(IDs):
            controller.setReferenceID(IDs[0])

    def sortCallback_(self, menuItem):
        self.controller.sortFamilyCallback(None)

    def singleClickCallback(self, cellID):
        pass
        #controller = self.getController()
        #styleKey = self.getStyleKey(cellID)
        #controller.setStyle(styleKey)

    def doubleClickCallback(self, cellID):
        controller = self.getController()
        controller.qualityAssuranceCallback(None)
