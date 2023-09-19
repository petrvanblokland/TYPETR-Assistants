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
#    axes.py
#

from vanilla import Group
from AppKit import NSNumberFormatter
from tnbits.base.constants.tool import *
from tnbits.bites.assembly.dialogs.axisdialog import AxisDialog
from tnbits.spreadsheet.cell import Cell
from tnbits.spreadsheet.spreadsheet import Spreadsheet

numberFormatter = NSNumberFormatter.alloc().init()
W = 5*UNIT + PADDING

class Axes(object):
    """Implements GUI for the design space axes."""

    def __init__(self, parent, pos=(0, 0, -0, -0)):
        self.parent = parent
        self.dialog = None
        self.descriptions = None
        self.identifierKey = None
        self.currentItems = []
        self.axesOrder = []
        self.view = Group(pos)
        self.setSpreadsheet()

    # Get.

    def get(self):
        """Returns spreadsheet contents."""
        return self.spreadsheet.get()

    def getMenuItems(self):
        return [dict(title='Add', callback="addCallback:"),
                dict(title='Remove', callback="removeCallback:"),
                dict(title='Enable / Disable', callback="enableDisableCallback:")
            ]

    def getView(self):
        return self.view

    def getController(self):
        return self.parent.controller

    def getDesignSpace(self):
        return self.getController().designSpace

    def getSelection(self):
        """Returns Vanilla list selection."""
        return self.spreadsheet.getSelection()

    def getSelectedAxesTags(self):
        """Returns style keys for all selected rows."""
        axesTags = []
        ys = self.spreadsheet.getSelectionYs()

        for y in ys:
            axisTag = self.getAxisTagByY(y)
            axesTags.append(axisTag)

        return axesTags

    def getAxisTagByCell(self, cell):
        _, y = cell.identifier
        return self.getAxisTagByY(y)

    def getAxisTagByY(self, y):
        x = self.spreadsheet.getColumnIndex(self.identifierKey)
        cell = self.spreadsheet[(x, y)]
        axisTag = cell.value
        return axisTag


    def getDescriptions(self):
        """Sets headers and data structure."""
        return [
            {'title': 'Tag', 'key':'axisTag', 'width':100, 'editable':False},
            {'title': 'Name', 'key':'name', 'width': 200, 'editable':True},
            {'title': 'Minimum', 'key':'minValue', 'width':100,
                'editable':True, 'formatter': numberFormatter},
            {'title': 'Default', 'key':'defaultValue', 'width':100,
                'editable':True, 'formatter': numberFormatter},
            {'title': 'Maximum', 'key':'maxValue', 'width':100,
                'editable':True, 'formatter': numberFormatter},
        ]

    def getData(self):
        """
        Example axes:

        {u'Width': {u'minValue': 0, u'enabled': False, u'maxValue': 1000,
        u'name': u'Width'},
        u'Weight': {u'minValue': 8, u'enabled': True, u'maxValue': 276,
        u'name': u'Weight'},
        u'Size': {u'minValue': 8, u'enabled': False, u'maxValue': 72, u'name':
        u'Size'}}

        """
        ds = self.getDesignSpace()
        data = []
        y = 0

        if ds is None:
            return data


        # TODO: use sortedAxes()
        for axisTag, values in ds.getAxes().items():
            enabled = values['enabled']
            x = 0
            l = [Cell(identifier=(x, y), value=axisTag, enabled=enabled)]
            x += 1
            l.append(Cell(identifier=(x, y), value=values['name'], enabled=enabled))
            x += 1
            l.append(Cell(identifier=(x, y), value=values['minValue'], enabled=enabled))
            x += 1
            l.append(Cell(identifier=(x, y), value=values['defaultValue'], enabled=enabled))
            x += 1
            l.append(Cell(identifier=(x, y), value=values['maxValue'], enabled=enabled))
            data.append(l)
            y += 1

        return data

    def getAxisTagByCell(self, cell):
        # TODO: adapt to moving columns.
        _, cellY = cell.identifier
        cell0 = self.spreadsheet[(0, cellY)]
        return cell0.value

    # Set.

    def setSpreadsheet(self):
        self.descriptions = self.getDescriptions()
        self.identifierKey = self.descriptions[0]['key']
        data = self.getData()
        self.spreadsheet = Spreadsheet(self, (0, 0, -0, -0),
                descriptions=self.descriptions, data=data,
                cellChangedCallback=self.cellChangedCallback, minScale=0.25,
                maxScale=2, menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    # Delete and reset.

    def deleteSpreadsheet(self):
        """Deletes the spreadsheet entirely."""
        del self.view.spreadsheet

    def update(self):
        """Deletes spreadsheet from view and builds a new on with current data.
        TODO: just clear and update descriptions and data.
        """
        self.deleteSpreadsheet()
        self.setSpreadsheet()

    # Callbacks.

    def cellChangedCallback(self, cell):
        ds = self.getDesignSpace()
        cellX, cellY = cell.identifier
        axisTag = self.getAxisTagByCell(cell)
        key = self.spreadsheet.getColumnKey(cellX)
        kwargs = {key: cell.value}
        ds.setAxis(axisTag, **kwargs)
        ds.save()
        cell.value = ds.getAxisValue(axisTag, key)
        self.update()

    def addCallback_(self, menuItem):
        # TODO: add to tool dialogs.
        #self.parent.tool.addDialog('axis', dialog)
        if self.dialog is None:
            self.dialog = AxisDialog(self, self.addAxis, self.cancelAddAxis)
        else:
            # TODO: Bring to front.
            pass

    def addAxis(self, values):
        ds = self.getDesignSpace()
        tag = values['tag']
        name = values['name']
        minValue = float(values['minValue'])
        defaultValue = float(values['defaultValue'])
        maxValue = float(values['maxValue'])
        ds.addAxis(tag, name, minValue, maxValue, defaultValue)
        ds.save()
        self.update()
        self.dialog = None
        self.parent.updateMasters()

    def enableDisableCallback_(self, menuItem):
        ds = self.getDesignSpace()
        axesTags = self.getSelectedAxesTags()

        for axisTag in axesTags:
            enabled = ds.isAxisEnabled(axisTag)
            if enabled:
                ds.setAxisEnabled(axisTag, False)
            else:
                ds.setAxisEnabled(axisTag, True)

        self.update()
        self.parent.updateMasters()


    def cancelAddAxis(self):
        self.dialog = None

    def removeCallback_(self, menuItem):
        ds = self.getDesignSpace()
        axesTags = self.getSelectedAxesTags()

        for axisTag in axesTags:
            ds.deleteAxis(axisTag)

        ds.save()
        self.update()
        self.parent.updateMasters()
