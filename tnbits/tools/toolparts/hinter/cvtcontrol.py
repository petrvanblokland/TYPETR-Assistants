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
#    cvtcontrol.py
#

from vanilla import Group, List
from AppKit import NSView, NSBezierPath, NSColor

class CvtControl(Group):
    """Wraps the CVT view."""

    def __init__(self, posSize, delegate):
        super(CvtControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        data = []
        descriptions = [{"title": "index"}, {"title": "value"}]
        self.cvt = List((0, 0, -0, -0), data, columnDescriptions=descriptions, selectionCallback=self.cvtCallback)
        self.update()

    def update(self, gstate=None):

        if not gstate is None:
            data = []

            for i, value in enumerate(gstate.cvt):
                data.append({'index': str(i), 'value': str(value)})
            self.cvt.set(data)

    def cvtCallback(self, sender):
        pass
