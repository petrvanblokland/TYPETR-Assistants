# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   makeglyphset.py
#
import sys
from math import *
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.data import * # Import anchors names

from assistantLib.assistantParts.glyphsets.Latin_S_set import LATIN_S_SET_NAME, LATIN_S_SET
from assistantLib.assistantParts.glyphsets.Latin_M_set import LATIN_M_SET_NAME, LATIN_M_SET
from assistantLib.assistantParts.glyphsets.Latin_L_set import LATIN_L_SET_NAME, LATIN_L_SET
from assistantLib.assistantParts.glyphsets.Latin_XL_set import LATIN_XL_SET_NAME, LATIN_XL_SET

class AssistantPartGlyphsets(BaseAssistantPart):
    """The Glyphsets assistant part handles all the choice of available glyph sets and commands that bring the current font up to date.
    """

    def buildGlyphsets(self, y):
        """Build the assistant UI for guidelines controls."""
        personalKey = self.registerKeyStroke('±', 'makeGuidelines')

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.makeGlyphSetAllFonts = CheckBox((C1, y, CW, L), f'All fonts', value=False)
        c.w.makeGlyphset = Button((C2, y, CW, L), f'Fix glyphset', callback=self.fixGlyphsetsCallback)
        y += L + L/5
        c.w.makeGlyphsetEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.makeGlyphsetEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5

        return y

    def fixGlyphsetsCallback(self, sender):
        """Make the missing glyphs"""
        if self.w.makeGlyphSetAllFonts.get():
            fonts = self.getAllOpenFonts()
        else:
            fonts = [self.getCurrentFont()]
        for f in fonts:
            md = self.getMasterData(f)
            gs = md.glyphSet
            for gName, gd in gs.items():
                # Check if all glyphs in the defined GlyphSet do exist in the font. Otherwise, create the glyph
                if not gName in f:
                    print(f'... Make new glyph {gName} in {f.path.split("/")[-1]}')
                    f.newGlyph(gName)
            for g in f:
                if g.name not in gs.glyphs:
                    print(f'### Glyph /{g.name} is in font, but not in glyphset {gs.name}')
            #print(gs)



