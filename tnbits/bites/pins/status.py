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
#    status.py
#

from vanilla import Group

class Status(object):
    """Visual feedback of current status."""

    def __init__(self, pos, controller):
        self.pos = pos
        self.controller = controller
        self.s = Group((0, 0, -0, -0))
        controller.tool.w.status = self.s
        self.build()

    def build(self):
        pass
