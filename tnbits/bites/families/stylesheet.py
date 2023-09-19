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
from tnbits.base.tools import setLog
from tnbits.base.stylesheet import StyleSheet
from tnbits.bites.spreadsheet.constants import *

class FamStyleSheet(StyleSheet):

    def __init__(self, controller, pos=(0, 0, -0, -0), cellChangedCallback=None):
        super(FamStyleSheet, self).__init__(controller, pos)
        self.cellChangedCallback = cellChangedCallback

    def getMenuItems(self):
        l = [
                dict(title='Edit', callback='editCallback:'),
                dict(title='Save', callback='saveCallback:'),
                dict(title='Close', callback='closeCallback:'),
                dict(title='Refresh', callback='refreshCallback:'),
                ]
        return l

    def editCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        self.getController().editStyleKeys(styleKeys)
        self.update()
        setLog()

    def refreshCallback_(self, menuItem):
        self.update()

    def closeCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        self.getController().closeStyleKeys(styleKeys)
        self.update()

    def saveCallback_(self, menuItem):
        styleKeys = self.getSelectedKeys()
        self.getController().saveStyleKeys(styleKeys)
        self.update()
        setLog()

    def addCallback_(self, menuItem):
        pass

    def removeCallback_(self, menuItem):
        pass

    def sortCallback_(self, menuItem):
        pass

    def singleClickCallback(self, cellID):
        pass

    def doubleClickCallback(self, cellID):
        pass
