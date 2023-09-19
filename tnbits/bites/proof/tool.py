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
from tnbits.base.preferences import Preferences
from tnbits.base.tool import Tool
from tnbits.base.windows import setBackgroundColor
from tnbits.base.constants.tool import CATEGORY_ANALYZE
from tnbits.bites.proof.controller import Controller

class ProofTool(Tool):
    """A tool to proof font families."""

    # Tool globals, override Tool values.
    TOOLID = 'tnProof'
    NAME = u'Proof'
    DEFAULTKEY = "com.typenetwork.proof"
    VERSION = 1.0
    CATEGORY = CATEGORY_ANALYZE
    VIEWX = 60
    VIEWY = 80
    VIEWWIDTH = 800 # Take default tool width
    VIEWHEIGHT = 600
    VIEWMINSIZE = (600, 400)
    VIEWMAXSIZE = (1200, 1000)
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)
    ControllerClass = Controller
