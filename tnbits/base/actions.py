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

from vanilla import Button, Group

class Actions(object):

    def __init__(self, controller, window, mode='tool', pos=None):
        """Action buttons below split view.
        """
        padding = 4
        buttonWidth = 80
        dx = -buttonWidth - padding
        x = dx
        y = -20
        self.mode = mode

        if pos is None:
            self.pos = (0, 0, -0, -0)
        else:
            self.pos = pos

        self.view = Group(self.pos)

        if self.mode == 'tool':
            # Open selected styles in RoboFont. Only if part of tool.
            self.view.openStyle = Button((x, y, buttonWidth, 16), 'Open Style',
                                sizeStyle='small', callback=self.openStyleCallback)
            self.view.openStyle.enable(False) # Will be enabled by styleList selection
            x += dx

        self.view.openFamily = Button((x, y, buttonWidth, 16), 'Open Family',
                            sizeStyle='small', callback=self.openFamilyCallback)
        x += dx
        self.view.clearReporter = Button((x, y, buttonWidth, 16), 'Clear',
                            sizeStyle='small', callback=controller.reporter.clearCallback)
        self.view.clearReporter.enable(False)
        x += dx
        self.view.saveReporter = Button((x, y, buttonWidth, 16), 'Save',
                            sizeStyle='small', callback=controller.reporter.saveCallback)
        self.view.saveReporter.enable(False)

    def getView(self):
        """Returns top view object (is a group)."""
        return self.view

