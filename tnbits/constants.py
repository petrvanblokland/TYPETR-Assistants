# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     constants.py
#

from tnbits.tools.constantsparts.config.userconfig import Config
from tnbits.tools.constantsparts.errors import Errors
from tnbits.tools.constantsparts.tool import Tool
from tnbits.tools.constantsparts.codepages import CodePages
from tnbits.tools.constantsparts.cmap import CMap
from tnbits.tools.constantsparts.contours import Contours
from tnbits.tools.constantsparts.database import Database
from tnbits.tools.constantsparts.fontinfo import FontInfo
from tnbits.tools.constantsparts.glyphs import Glyphs
from tnbits.tools.constantsparts.opentype import OpenType
from tnbits.tools.constantsparts.unicodes import Unicodes
from tnbits.tools.constantsparts.hinting import Hinting
from tnbits.tools.constantsparts.path import Path
from tnbits.tools.constantsparts.ufobase import UfoBase
from tnbits.tools.constantsparts.languagesupport import LanguageSupport
from tnbits.tools.constantsparts.stylename import StyleNames
from tnbits.tools.constantsparts.floqconstants import FloqConstants
from tnbits.tools.constantsparts.burofont import BuroFont
from tnbits.tools.constantsparts.landingpattern import LandingPattern


# TODO: move to tools.

class Constants(Config, Unicodes, Hinting, FontInfo, Glyphs, OpenType,
        Contours, CMap, Tool, CodePages, Path, UfoBase, LanguageSupport,
        StyleNames, FloqConstants, BuroFont, LandingPattern, Database, Errors,
        object):

    floqLibKey = 'com.typenetwork.floq'
