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
#    programcontrol.py
#

from vanilla import Group, TextEditor
from AppKit import NSView, NSBezierPath, NSColor

class ProgramControl(Group):
    """Wraps the Hinter view."""

    def __init__(self, posSize, delegate):
        super(ProgramControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        self.program = TextEditor((0, 0, -0, -0), '', callback=self.programCallback)
        self.update()

    def update(self, mode='fpgm'):
        if mode == 'fpgm':
            if not self.delegate.simulator.fpgm is None:
                self.program.set(self.delegate.simulator.fpgm.dump())
        elif mode == 'prep':
            if not self.delegate.simulator.prep is None:
                self.program.set(self.delegate.simulator.prep.dump())

        view = self.getNSView()
        view.setNeedsDisplay_(True)

    def programCallback(self, sender):
        pass
