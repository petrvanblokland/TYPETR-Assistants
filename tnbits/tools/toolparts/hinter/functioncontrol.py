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
#    functioncontrol.py
#

from vanilla import Group, PopUpButton, CheckBoxListCell
from AppKit import NSView, NSBezierPath, NSColor
from tnbits.vanillas.lists.listcell import *
from tnbits.vanillas.lists.tnlist import List

class FunctionControl(Group):
    """Shows functions that have been compiled from the font program (FPGM)."""

    functions = []
    function = []
    isInsideCall = False

    C0 = 2
    C1 = 304
    C2 = 456

    def __init__(self, posSize, delegate):
        super(FunctionControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        self.functionsBox = PopUpButton((self.C0, 2, 150, 30),
                                self.functions,
                                callback=self.functionsCallback)

        descriptions = [
            dict(title="", key="break", width=20, cell=CheckBoxListCell()),
            dict(title="index", key="index", width=40),
            dict(title="value", key="value")
        ]

        self.functionList = List((self.C0, 30, -0, -0), self.function,
            columnDescriptions=descriptions,
            doubleClickCallback=self.doubleClickCallback,
            selectionCallback=self.functionCallback)

    def update(self, functionId=None, functionStepIndex=None):
        if self.delegate.simulator.hasFunctions():
            ids = self.delegate.simulator.getFunctionIds()
            self.functions = map(str, ids)
            self.functionsBox.setItems(self.functions)

            if functionId is None:
                functionIndex = 0
                functionId = int(self.functions[0])
            else:
                functionIndex = self.functions.index(str(functionId))

            self.setFunction(functionId)
            self.functionsBox.set(functionIndex)

            if not functionId is None and not functionStepIndex is None:
                s = [functionStepIndex]
            else:
                s = []

            self.functionList.setSelection(s)

    def setFunction(self, functionId):
        """
        Gets the functions instructions from the graphics state and shows them
        in an enumerated list.
        """
        function = self.delegate.simulator.gstate.functions[functionId]
        data = []

        for i, value in enumerate(function.asList()):
            data.append({'index': str(i), 'value': str(value)})

        self.functionList.set(data)

    def functionsCallback(self, sender):
        """
        """
        i = sender.get()
        functionId = int(self.functions[i])
        self.delegate.functionId = functionId
        self.setFunction(functionId)

    def functionCallback(self, sender):
        sel = sender.getSelection()

        if len(sel) > 0:
            i = sender.getSelection()[-1]

            if not self.function is None and i < len(self.function):
                print(self.function[i])

    def doubleClickCallback(self, sender):
        """
        Steps to the selected point in the list.
        """
        sel = sender.getSelection()
        l = len(sel)

        if self.isInsideCall is True and l > 0:
            i = sel[-1]
            self.delegate.runPrep(topLevelIndex=i)
