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

class AssistantPartGlyphsets(BaseAssistantPart):
    """The Glyphsets assistant part handles all the choice of available glyph sets and commands that bring the current font up to date.
    """

    def buildGlyphsets(self, y):
        """Build the assistant UI for guidelines controls."""
        personalKey = self.registerKeyStroke('±', 'makeGuidelines')

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.makeGlyphset = Button((C2, y, CW, L), f'Make glyphset', callback=self.makeGlyphsetsCallback)
        y += L + L/5
        c.w.makeGlyphsetEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.makeGlyphsetEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5

        return y

    def makeGlyphsetsCallback(self, sender):
        """Make the missing glyphs"""
        f = self.getCurrentFont()
        

