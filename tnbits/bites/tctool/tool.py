# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N   T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tool.py
#

from vanilla import Window
from tnbits.base.tool import Tool
from tnbits.base.preferences import Preferences
from tnbits.base.constants.tool import *
from tnbits.base.windows import setBackgroundColor
from tnbits.bites.tctool.controller import Controller

class TextCenterTool(Tool):
    """Interactive kerning and spacing editor."""

    OBSERVERS = (
        ('mouseUp', EVENT_MOUSEUP),
        ('keyUp', EVENT_KEYUP),
        ('viewDidChangeGlyph', EVENT_VIEWDIDCHANGEGLYPH),
        #('fontDidOpen', EVENT_FONTDIDOPEN),
        #('fontIsClosing', EVENT_FONTWILLCLOSE),
        #('featuresChanged', EVENT_FEATURESCHANGED),
    )

    TOOLID = 'tnTextCenter'
    NAME = 'TextCenter'
    VERSION = '3.0'
    DEFAULTKEY = "com.typenetwork.tc"
    CATEGORY = CATEGORY_GENERALIZE
    VIEWWIDTH = 1000
    VIEWHEIGHT = 900
    VIEWX = 50
    VIEWY = 50
    VIEWMINSIZE = (600, 400)
    VIEWMAXSIZE = (4000, 4000)
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)
    USEFLOATINGWINDOW = False
    FAMILYPREFERENCES = True


    # TODO: not needed?
    PREFERENCE_MODEL = dict(
        metricsColor=dict(label=u'Metrics color', sort=10, type=PREFTYPE_COLOR,
            default=(0.6, 0.6, 0.6, 1)),
        labelColor=dict(label=u'Labels color', sort=20, type=PREFTYPE_COLOR,
            default=(0.1, 0.1, 0.1, 1)),
        textColor=dict(label=u'Text color', sort=30, type=PREFTYPE_COLOR,
            default=(0, 0, 0, 1)),
        selectedGlyphColor=dict(label=u'Hover glyph color', sort=50,
            type=PREFTYPE_COLOR, default=(0.8, 0, 0, 1)),
        nonExistingGlyphColor=dict(label=u'Non-existing glyph color', sort=60,
            type=PREFTYPE_COLOR, default=(0, 0.8, 0, 1)),
        canvasColor=dict(label=u'Canvas color', sort=70, type=PREFTYPE_COLOR,
            default=(1, 1, 1, 1)),

        # Window.
        useFloatingWindow=dict(label=u'Tool as floating window', sort=400,
            type=PREFTYPE_BOOL, default=USEFLOATINGWINDOW),
        windowPosSize=dict(label=u'Window size', sort=410, type=PREFTYPE_RECT,
            default=(VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)),
    )

    ControllerClass = Controller

    '''
    def fontDidOpen(self, event):
        rfont = event['font']
        self.controller.updateRFont(rfont)
    '''

    '''
    def featuresChanged(self, event):
        print('Event: featuresChanged() %s' % event)
    '''

    def viewDidChangeGlyph(self, event):
        self.controller.viewDidChangeGlyph(event['glyph'])

    def close(self, sender):
        self.controller.close()
        super().close(sender)
