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
#    tools.py
#

from vanilla import Window
from tnbits.base.preferences import Preferences

class Tools(object):

    VIEWX = 50
    VIEWY = 50
    VIEWHEIGHT = 500
    VIEWWIDTH = 100
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)
    VIEWMINSIZE = (VIEWWIDTH, VIEWHEIGHT)
    VIEWMAXSIZE = (VIEWWIDTH, VIEWHEIGHT)
    TOOLID = 'tnExampleTools'
    NAME = '...'

    def __init__(self, controller):
        self.preferences = Preferences(self.TOOLID, defaultPos=self.DEFAULTPOS,
                useFloatingWindow=False)
        screen, posSize = self.preferences.screens.getWindowScreenPosSize()
        self.controller = controller
        self.w = window = Window(title=self.NAME, posSize=posSize,
                screen=screen, minSize=self.VIEWMINSIZE,
                maxSize=self.VIEWMAXSIZE)

        self.w.open()
