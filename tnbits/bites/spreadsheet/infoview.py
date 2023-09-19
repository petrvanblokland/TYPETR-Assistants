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
#    infoview.py
#

from tnbits.base.console import Console

class InfoView(object):

    def __init__(self, controller, pos=(0, 0, -0, -0)):
        """Shows information and metrics for selected design space / style /
        glyph."""
        self.controller = controller
        self.info = Console(self)
        self.view = self.info.getView()

    def getView(self):
        return self.view

    def savePreferences(self, sender):
        pass

    def message(self, msg):
        self.info.message(msg)

    def setLines(self):
        self.info.setLines()

    def clearLines(self):
        self.info.clearLines()
