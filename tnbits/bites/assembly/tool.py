# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    Variation Bakery
#
import os

from vanilla import Window
from tnbits.base.constants.tool import CATEGORY_DEVELOPMENT
from tnbits.base.model import *
from tnbits.base.tools import *
from tnbits.base.tool import Tool
from tnbits.base.preferences import Preferences
from tnbits.base.windows import setBackgroundColor
from tnbits.bites.assembly.controller import Controller

class AssemblyTool(Tool):
    """Tool to assemble (variation) fonts using FontMake."""

    TOOLID = 'tnAssembly'
    NAME = u'Assembly'
    DEFAULTKEY = "com.typenetwork.assembly"
    CATEGORY = CATEGORY_DEVELOPMENT
    VIEWWIDTH = 1000
    VIEWHEIGHT = 900
    VIEWX = 50
    VIEWY = 50
    VIEWMINSIZE = (600, 400)
    VIEWMAXSIZE = (4000, 4000)
    DEFAULTPOS = (VIEWX, VIEWY, VIEWWIDTH, VIEWHEIGHT)
    ControllerClass = Controller
