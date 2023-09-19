# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tool.py
#
from vanilla import Window
from tnbits.base.c import CATEGORY_MANAGE
from tnbits.base.constants.tool import *
from tnbits.base.preferences import Preferences
from tnbits.base.tool import Tool
from tnbits.base.windows import setBackgroundColor
from tnbits.bites.families.controller import Controller

class FamiliesTool(Tool):
    """A tool to manage font families."""

    # Tool globals, override Tool values.
    TOOLID = 'tnFamilies'
    NAME = u'Families'
    DEFAULTKEY = "com.typenetwork.families"
    VERSION = 1.0
    CATEGORY = CATEGORY_MANAGE
    VIEWX = 60
    VIEWY = 80
    VIEWWIDTH = 400 # Take default tool width
    VIEWHEIGHT = 300
    VIEWMINSIZE = (200, 150)
    VIEWMAXSIZE = (1200, 800)
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)
    OBSERVERS = (
        #('fontDidOpen', EVENT_FONTDIDOPEN),
        #('fontIsClosing', EVENT_FONTWILLCLOSE),
        #('fontChanged', EVENT_CURRENTFONTCHANGED),
        #('glyphChanged', EVENT_CURRENTGLYPHCHANGED),
        ('mouseUp', EVENT_MOUSEUP),
        ('keyUp', EVENT_KEYUP),
        ('fontSaved', EVENT_FONTDIDSAVE),
        #('viewDidChangeGlyph', EVENT_VIEWDIDCHANGEGLYPH),
        #('featuresChanged', EVENT_FEATURESCHANGED),
    )

    ControllerClass = Controller
