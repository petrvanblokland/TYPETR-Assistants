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
from AppKit import NSURL
from vanilla import Group, PathControl
from tnbits.bites.assembly.constants import *
from tnbits.base.constants.tool import *

class Status(object):

    def __init__(self, controller):
        """Buttons above styles list."""
        self.controller = controller
        x = PADDING
        y = PADDING
        w = BUTTON_WIDTH
        h = BUTTON_HEIGHT
        s = 'small'
        self.view = Group((0, -3*UNIT, -0, 3*UNIT))
        # TODO: width in units.
        #self.view.designSpaceLabel = TextBox((x, y, 500, 16), 'Design Space: ', sizeStyle=s)
        w = -PADDING - BUTTON_WIDTH
        # Names will be set when a family is loaded.
        self.view.designSpacePath = PathControl((x, y, w, h), None, callback=None, sizeStyle='small')

    def getView(self):
        return self.view

    def set(self, designSpace):
        if designSpace:
            f = designSpace.getXMLPath()
            url = NSURL.fileURLWithPath_(f)
            self.view.designSpacePath._nsObject.setURL_(url)
