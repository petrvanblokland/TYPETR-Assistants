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
#    actions.py
#

from vanilla import  Button
from tnbits.bites.proof.constants import *

BUTTON_WIDTH = 120

class Actions(object):

    def __init__(self, controller, mode):
        """Action buttons at below the list."""
        # TODO: add buttons to group, assign group to window in controller.
        self.controller = controller
        self.mode = mode
        self.build()

    def getWindow(self):
        # TODO: should be added to group view, remove this.
        return self.controller.tool.w

    def build(self):

        # TODO: should be added to group view, remove this.
        window = self.getWindow()

        n = 1
        x0 = -BUTTON_WIDTH - 4
        x = n * x0
        y = -20
        window.run = Button((x, y, BUTTON_WIDTH, 16),
                                'Run', sizeStyle='small',
                                callback=self.runCallback)
        # Will be enabled by styleList selection.
        window.run.enable(False)
        n += 1

        # TODO: switch to isinstance() when (base)tool doesn't import mojo.
        #if isinstance(tool, BaseTool):
        if self.mode == 'tool':
            x = n * x0
            # Open selected styles (only in RoboFont).
            window.openStyle = Button((x, y, BUTTON_WIDTH, 16), 'Open styles',
                                sizeStyle='small', callback=self.openStyleCallback)
            window.openStyle.enable(False) # Will be enabled by styleList selection
            n += 1

        x = n * x0
        window.openFamily = Button((x, y, BUTTON_WIDTH, 16), 'Open family',
                            sizeStyle='small', callback=self.openFamilyCallback)

    def runCallback(self, sender):
        self.controller.run()

    def openStyleCallback(self, sender):
        self.controller.openStyle()

    def openFamilyCallback(self, sender):
        self.controller.openFamily()
