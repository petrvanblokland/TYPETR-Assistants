# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   guidelines.py
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

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR
from assistantLib.assistantParts.data import * # Import anchors names

class AssistantPartGuidelines(BaseAssistantPart):
    """The Guidelines assistant part handles all guideline positions. If there is a guidelines definition defined
    in the masterData, then take these values. Otherwise do some guessing from the current font.
    """

    def initMerzGuidelines(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        self.registerKeyStroke('±', 'makeGuidelines')

    def updateGuidelines(self, info):
        """If the checkbox is set, then automatic build guidelines if another glyph is selected."""
        g = info['glyph']
        if g is None:
            return

    def buildGuidelines(self, y):
        """Build the assistant UI for guidelines controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.makeGuides = Button((C0, y, CW, L), 'Make guides', callback=self.makeGuidesCallback)
        y += L + LL

        return y

    def makeGuidesCallback(self, sender):
        """Make the guidelines for the current glyph. Same as [±] keys."""
        self.makeGuidelines()

    def makeGuidelines(self):
        """Build the guide lines from the definition in masterData. Also try to gues which glyphs need which guidelines.
        based on patters in glyph names.

        Defauls in MasterData:
        
        baseline = 0
        overshoot = self.DEFAULT_OVERSHOOT
        capOvershoot = overshoot
        scOvershoot = overshoot
        supsOvershoot = overshoot
        unitsPerEm = DEFAILT_UNITS_PER_EM
        ascender = DEFAULT_ASCENDER
        descender = DEFAULT_DESCENDER
        xHeight = DEFAULT_XHEIGHT
        capHeight = DEFAULT_CAPHEIGHT
        scHeight = xHeight * 1.1
        middlexHeight = xHeight/2,
        middleCapHeight = capHeight/2
        diacriticsTop = xheight * 1.2
        capDiacriticsTop = capHeight * 1.1
        diacriticsBottom = -4 * overshoot
        supsHeight = xHeight * 2/3
        supsBaseline = xHeight
        numrBaseline = ascender - supsHeight  
        dnomBaseline = baseline  
        sinfBaseline = descender  
        """

