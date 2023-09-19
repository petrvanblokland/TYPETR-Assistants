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
#    stackcontrol.py
#

from vanilla import Group, List
from AppKit import NSView, NSBezierPath, NSColor

class StackControl(Group):
    """Wraps the Stack view."""

    stack = []

    def __init__(self, posSize, delegate):
        super(StackControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        descriptions = [{"title": "index"}, {"title": "value"}]
        self.stackList = List((0, 0, -0, -0), self.stack, columnDescriptions=descriptions, selectionCallback=self.stackCallback)

        self.update()

    def update(self, gstate=None):
        view = self.getNSView()
        self.stack = []

        if not gstate is None and not gstate.stack is None:

            for n in range(len(gstate.stack)):
                self.stack.append({'index': str(n), 'value': str(gstate.stack.peek(n))})
        else:
            self.stack = []

        self.stackList.set(self.stack)

    def stackCallback(self, sender):
        pass
