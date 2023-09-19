# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010 buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    prepcontrol.py
#

from vanilla import Group, CheckBoxListCell

from AppKit import NSView, NSBezierPath, NSColor
#from tnbits.vanillas.lists.listcell import *
from tnbits.vanillas.lists.tnlist import List

class PrepControl(Group):
    """Wraps the Prep view."""

    prepOpcodes = []

    def __init__(self, posSize, delegate):
        super(PrepControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)

        descriptions = [
            dict(title="", key="break", width=50, cell=CheckBoxListCell()),
            dict(title="index", key="index", width=50),
            dict(title="value", key="value")
        ]

        self.prep = List((0, 0, -0, -0), self.prepOpcodes,
                    columnDescriptions=descriptions,
                    selectionCallback=self.selectionCallback,
                    editCallback=self.editCallback,
                    doubleClickCallback=self.doubleClickCallback,
                    allowsMultipleSelection=False)

        print(self.prep.getNSTableView())

    def mouseDown_(self, event):
        print('controller', event)

    def update(self, selected=None):
        self.updatePrep()
        self.prep.set(self.prepOpcodes)

        if selected is None:
            selected = []
        else:
            selected = [selected]

        self.prep.setSelection(selected)

    def updatePrep(self):
        prep = self.delegate.simulator.prep

        if not prep is None:
            instructions = prep.asList()
            self.prepOpcodes = []

            for i, value in enumerate(instructions):
                self.prepOpcodes.append({'index': str(i), 'value': str(value)})

    def doubleClickCallback(self, sender):
        """
        Steps to the selected point in the list.
        """
        sel = sender.getSelection()
        l = len(sel)

        if l > 0:
            i = sel[-1]

            if not self.prepOpcodes is [] and i < len(self.prepOpcodes):
                # Run with explicit index.
                self.delegate.mode = 'prep'
                self.delegate.runPrep(stepIndex=i)

    def editCallback(self, sender):
        sel = sender.getSelection()

        if sel:
            item = sender[sel[0]]
            if 'break' in item:
                print(item['break'])

    def selectionCallback(self, sender):
        pass
