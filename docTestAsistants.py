# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   docTestAssistants.py
#
import sys

from fontParts.fontshell.font import RFont

from assistantLib import *
from assistantLib.assistantParts import *
from assistantLib.assistantParts.glyphsets import *

from assistantLib.assistantParts.glyphsets.anchorData import *
from assistantLib.assistantParts.glyphsets.glyphData import *
from assistantLib.assistantParts.glyphsets.glyphSet import *
from assistantLib.assistantParts.glyphsets.MS_WGL4_segoe import *
from assistantLib.assistantParts.glyphsets.TYPETR_UpgradeNeon_set import *

from assistantLib.assistantParts.data import MasterData
from assistantLib.assistantParts.spacingKerning.kerningManager import KerningManager

SEGOEUI_DISPLAY_REGULAR_ITALIC = 'Segoe_UI_Display-Regular_Italic_MA168.ufo'
ufoName = SEGOEUI_DISPLAY_REGULAR_ITALIC
ufoPath = '../TYPETR-Segoe-UI-Italic/ufo/' + ufoName
f = RFont(ufoPath)

# Test GlyphSet
from assistantLib.assistantParts.glyphsets.TYPETR_full_set import TYPETR_GlyphSet 
#glyphSet = TYPETR_GlyphSet()
glyphSet = MS_GlyphSet()
md = MasterData(name=ufoName, glyphSet=glyphSet)

gs = md.glyphSet
gd = gs['kstroke']

g = f[gd.name]
km = KerningManager(f, md)
print(km.getLeftMarginByGlyphSetReference(g))

g = f['H']
print(km.getLeftMarginByGlyphSetReference(g))
print(km.getRightMarginByGlyphSetReference(g))