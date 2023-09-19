
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    constants.py
#

from AppKit import (NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSColor,
        NSBackspaceCharacter, NSDeleteFunctionKey, NSDeleteCharacter,
        NSPageUpFunctionKey, NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey)
from tnbits.tools.basetool import BaseTool
from tnbits.base.future import chr
from tnbits.base.constants.tool import *
from tnbits.base.constants.groups import LEFT, RIGHT
from tnbits.base.samples import SAMPLES as TEXTSAMPLES
from tnbits.bites.tctool.keys import *

# TODO: move colors to tnbits.base.
# Color indicator for kerning.
REDCOLOR = NSColor.redColor()

# Key indicator.
BLACKCOLOR = NSColor.blackColor()

# Key indicator.
WHITECOLOR = NSColor.whiteColor()

# Other colors.
LIGHTBLUECOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.5, 0.6, 0.8, 0.8)
LIGHTGREYCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 0.8)
DARKGREENCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0.5, 0, 1)
DARKBLUECOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0.7, 1)
BASEMARKERCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.3, 0.3, 0.3, 0.9)
METRICSBGCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.7, 0.7, 0.7, 0.7)
SPACINGBGCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.8, 0.8, 0.9, 0.9)
KERNINGBGCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.9, 0.8, 0.8, 0.9)
MISSINGGLYPHMARKERCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.5, 0.6, 0.9, 0.8)
LOCKMARKERCOLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 1)

XX = 300
MARGIN = 4

# Order fits radio buttons in GUI.
KERNING = 'kerning'
SPACING = 'spacing'
EDIT_MODES = {SPACING: 0, KERNING: 1}

DEFAULT_KERN1 = 'kern1'
DEFAULT_KERN2 = 'kern2'

REGULAR = 'regular'
DIA = 'dia'
COLOR = 'color'

COLORSCHEMES = {0: REGULAR, 1: DIA, 2: COLOR}

# Maximum number of glyphs per page.
MAX_GLYPHS = 1000

# Default width for .tab glyphs.
TAB_WIDTH = 650
STROKE_WIDTH = 1
KEY_INTERVAL = 0.2

# 5 seconds for UI-mode elements to show.
DISPLAY_TIME  = 5

LEADING_KEYS = KEY_LEADINGINC + KEY_LEADINGDEC
EDIT_KEYS = KEY_EDITKERNING + KEY_EDITSPACING
ZOOM_KEYS = KEY_ZOOMIN + KEY_ZOOMOUT
GROUP_KEYS = KEY_LEFTDEC + KEY_LEFTINC + KEY_RIGHTDEC + KEY_RIGHTINC + \
        KEY_KERNDEC + KEY_KERNINC
FLAG_KEYS = KEY_SHOWMARKERS + KEY_SHOWKERNING + KEY_SHOWMISSING + \
    KEY_SHOWMETRICS
OPEN_KEYS = KEY_SPACE + KEY_NEWLINE + KEY_RETURN
ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]

DELETE_KEYS = [NSBackspaceCharacter, NSDeleteFunctionKey, NSDeleteCharacter,
        chr(0x007F),]

PPEM_MIN = 80
PPEM_MAX = 400
PPEM_DEFAULT = 100
LEADING_DEFAULT = 110
NUMBER_OF_GLYPHS_MAX = 1000

# Page margin in the canvas.
M = 36

LABEL_EXISTS = u'•'
LABEL_CHR = 'Ch'
LABEL_NAME = 'Name'
LABEL_HEX = '#'

RIGHTARROW = u'→'

# Minimal width of metrics info area.
METRICSW = 300

# Height of metrics info area.
METRICSH = 180

# Point size of metrics value labels.
LABEL_SIZE = 11
KEY_SIZE = 12

# Glyph sets and other standard sample page content.
# FIXME: move to tnbits.base.samples.
SAMPLES = []

# Construct small set from glyph names. None means all glyphs.
SAMPLENAMES = []

for name, t in TEXTSAMPLES:
    SAMPLENAMES.append(name)
    SAMPLES.append(t)

# TODO: check if all of these are still in use.
# Update action name,   method name.
#(UPDATE_MARGINS, 'updateMarginGroups'), # TODO?
#(UPDATE_ACCENTSTYLEPOSITIONS, 'updateStyleAccents'), # TODO?
# Update the margins of all glyphs from groups and base glyph in the groups.
UPDATE_MARGINS = 'margins'
# Update entire style for accent positions.
UPDATE_ACCENTSTYLEPOSITIONS = 'updateStyleAccentsFromBase'

'''
# Batch tasks
T_SPACING = 'Spacing'
T_KERNING = 'Kerning'
T_EXPORT = 'Export'

TASKS = (
    T_SPACING, T_KERNING, T_EXPORT
)
'''
