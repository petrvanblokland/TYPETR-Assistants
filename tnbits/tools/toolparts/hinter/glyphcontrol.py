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
#    glyphcontrol.py
#


from vanilla import Group, CheckBoxListCell
from AppKit import NSView, NSBezierPath, NSColor
from tnbits.vanillas.lists.listcell import *
from tnbits.vanillas.lists.tnlist import List

class GlyphControl(Group):
    """Wraps the Glyph view."""

    glyphOpcodes = []

    def __init__(self, posSize, delegate):
        super(GlyphControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)

        descriptions = [
            dict(title="", key="break", width=20, cell=CheckBoxListCell()),
            dict(title="index", key="index", width=40),
            dict(title="value", key="value")
        ]

        self.glyph = List((0, 0, -0, -0), self.glyphOpcodes,
                    columnDescriptions=descriptions,
                    selectionCallback=self.selectionCallback,
                    doubleClickCallback=self.doubleClickCallback,
                    allowsMultipleSelection=False)

    def update(self, selected=None):
        self.updateGlyph()
        self.glyph.set(self.glyphOpcodes)

        if selected is None:
            selection = []
        else:
            selection = [selected]

        self.glyph.setSelection(selection)

    def updateGlyph(self):
        if self.delegate.simulator.glyph is None:
            return

        instructions = self.delegate.simulator.glyph.asList()
        self.glyphOpcodes = []

        for i, value in enumerate(instructions):
            self.glyphOpcodes.append({'index': str(i), 'value': str(value)})

    def doubleClickCallback(self, sender):
        """
        Steps to the selected point in the list.
        """
        sel = sender.getSelection()
        l = len(sel)

        if l > 0:
            i = sel[-1]

            if not self.glyphOpcodes is [] and i < len(self.glyphOpcodes):
                # Run with explicit index.
                self.delegate.mode = 'glyph'

                try:
                    self.delegate.simulator.setGlyph(self.delegate.glyph, self.delegate.size)
                    self.delegate.simulator.runFpgm()
                    self.delegate.simulator.runPrep()
                    self.delegate.runGlyph(stepIndex=i)
                    self.updateGlyph()
                    self.glyph.set(self.glyphOpcodes)
                except Exception as e:
                    print(e)

    def selectionCallback(self, sender):
        pass
