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
        c = self.getController()
        g = info['glyph']
        if g is None:
            return
        if c.w.automakeGuidelines.get():
            self.makeGuidelines() # Always make them when glyph is selected. 

    def buildGuidelines(self, y):
        """Build the assistant UI for guidelines controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.makeGuidelines = Button((C0, y, CW, L), 'Make guides', callback=self.makeGuidesCallback)
        c.w.automakeGuidelines = CheckBox((C1, y, CW, L), 'Auto make', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L + LL

        return y

    def makeGuidesCallback(self, sender):
        """Make the guidelines for the current glyph. Same as [±] keys."""
        self.makeGuidelines()

    def makeGuidelines(self):
        """Build the guide lines from the definition in masterData, based on real values and categories. 
        Also try to guess which glyphs need which guidelines based on patterns in glyph names.
        """

        g = self.currentGlyph()
        if g is None:
            return
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)

        # Guideline label position angled for italics
        tg = tan(radians(-g.font.info.italicAngle or 0))

        g.clearGuidelines()
        overshoot = md.getOvershoot(g.name) # Get the right kind of overshoot for this glyph cetegory
        baseline = md.getBaseline(g.name)
        height = md.getHeight(g.name)
        middle = md.getMiddleHeight(g.name)
        
        x = -300 # Label position on the left
        xo = -50 # Label position for overshoot values

        if baseline: 
            g.appendGuideline((x + tg * baseline, baseline), 0, name='Baseline %d' % baseline)
            g.appendGuideline((xo + tg * (baseline - overshoot), baseline - overshoot), 0, name='%d (%d)' % (baseline - overshoot, overshoot))
        else: # Don't overwrite y == 0 position
            g.appendGuideline((xo + tg * (baseline - overshoot), baseline - overshoot), 0, name='(%d)' % overshoot)            
        g.appendGuideline((xo + tg * (height + overshoot), height + overshoot), 0, name='%d (%d)' % (height + overshoot, overshoot))
        g.appendGuideline((x + tg * height, height), 0, name='Height %d' % height)
        g.appendGuideline((x + tg * middle, middle), 0, name='Middle %d' % middle)

        if gd.isLower:
            g.appendGuideline((xo + tg * (md.ascender + overshoot), md.ascender + overshoot), 0, name='%d (%d)' % (md.ascender + overshoot, overshoot))
            g.appendGuideline((x + tg * md.ascender, md.ascender), 0, name='Ascender %d' % md.ascender)
            g.appendGuideline((xo + tg * (md.descender - overshoot), md.descender - overshoot), 0, name='%d (%d)' % (md.descender - overshoot, overshoot))
            g.appendGuideline((x + tg * md.descender, md.descender), 0, name='Descender %d' % md.descender)

