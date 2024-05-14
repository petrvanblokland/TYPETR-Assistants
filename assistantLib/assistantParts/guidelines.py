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

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.data import * # Import anchors names

class AssistantPartGuidelines(BaseAssistantPart):
    """The Guidelines assistant part handles all guideline positions. If there is a guidelines definition defined
    in the masterData, then take these values. Otherwise do some guessing from the current font.
    """

    def initMerzGuidelines(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        pass

    def updateGuidelines(self, info):
        """If the checkbox is set, then automatic build guidelines if another glyph is selected."""
        changed = False
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed to the glyph
        if c.w.automakeGuidelines.get():
            changed |= self.checkFixGuidelines() # Always make them when glyph is selected. 
        return changed

    def buildGuidelines(self, y):
        """Build the assistant UI for guidelines controls."""
        personalKey = self.registerKeyStroke('±', 'makeGuidelines')

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.automakeGuidelines = CheckBox((C1, y, CW, L), 'Auto make', value=True, sizeStyle='small', callback=self.updateEditor)
        c.w.makeGuidelines = Button((C2, y, CW, L), f'Make guides [{personalKey}]', callback=self.makeGuidesCallback)
        # Line color is crashing RF
        #y += L # Closing line for the part UI
        #c.w.guidelinesFooterLine = HorizontalLine((self.M, y+4, -self.M, 2))
        #c.w.guidelinesFooterLine.setBorderColor((0, 0, 0, 1))
        #y += 8
        y += L + L/5
        c.w.guidelinesEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.guidelinesEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5

        return y

    def makeGuidesCallback(self, sender):
        """Make the guidelines for the current glyph. Same as [±] keys."""
        self.checkFixGuidelines(forced=True)

    def makeAllGuidelines(self, f):
        for g in f:
            self.makeGuidelines(self, g)
            
    def makeGuidelines(self, g, c, event):
        self.checkFixGuidelines(forced=True)

    def checkFixGuidelines(self, forced=False):
        """Build the guide lines from the definition in masterData, based on real values and categories. 
        Also try to guess which glyphs need which guidelines based on patterns in glyph names.
        """
        changed = False
        g = self.getCurrentGlyph()
        if g is None:
            return False # Nothing changed
        f = g.font
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)

        # Guideline label position angled for italics
        tg = tan(radians(-f.info.italicAngle or 0))

        overshoot = md.getOvershoot(g.name) # Get the right kind of overshoot for this glyph cetegory
        baseline = md.getBaseline(g.name)
        height = md.getHeight(g.name)
        middle = md.getHeight2(g.name) # Height for this glyph / 2
        
        xHeight = f.info.xHeight
        capHeight = f.info.capHeight

        x = -550 # Label position on the left
        xo = -300 # Label position for overshoot values

        guidelines = []
        if baseline: 
            guidelines.append((x + tg * baseline, baseline, 0, f'Baseline {baseline}'))
            guidelines.append((xo + tg * (baseline - overshoot), baseline - overshoot, 0, f"{baseline - overshoot} ({overshoot})"))
        else: # Don't overwrite y == 0 position
            guidelines.append((xo + tg * (baseline - overshoot), baseline - overshoot, 0, f"({overshoot})"))            
        guidelines.append((xo + tg * (height + overshoot), height + overshoot, 0, f"{height + overshoot} ({overshoot})"))
        if height not in (capHeight, xHeight):
            guidelines.append((x + tg * height, height, 0, f'Height {height}'))
        guidelines.append((x + tg * middle, middle, 0, f'Middle {middle}'))

        # Always a guideline on font xHeight and capHeight.
        guidelines.append((x + tg * xHeight, xHeight, 0, f'xHeight {xHeight}'))
        guidelines.append((x + tg * capHeight, capHeight, 0, f'capHeight {capHeight}'))


        if gd.isLower or 'comb' in g.name:
            if md.baseDiacriticsTop is not None: # Baseline of top diacritics
                guidelines.append((xo + tg * md.baseDiacriticsTop, md.baseDiacriticsTop, 0, f'Bottom of top diacritics ({md.baseDiacriticsTop})'))
                self.setLib(f, 'baseDiacriticsTop', md.baseDiacriticsTop) # Save value, so an independent proofing script can find it.
        else:
            if md.capDiacriticsTop is not None: # Baseline of top diacritics
                guidelines.append((xo + tg * md.capDiacriticsTop, md.capDiacriticsTop, 0, f'Bottom of top diacritics ({md.capDiacriticsTop})'))
                self.setLib(f, 'capDiacriticsTop', md.capDiacriticsTop) # Save value, so an independent proofing script can find it.

        if md.baseDiacriticsBottom is not None:
            guidelines.append((xo + tg * md.baseDiacriticsBottom, md.baseDiacriticsBottom, 0, f'Top of bottom diacritics ({md.baseDiacriticsBottom})'))
            self.setLib(f, 'baseDiacriticsBottom', md.baseDiacriticsBottom) # Save value, so an independent proofing script can find it.

        if gd is None:
            print(f'### Cannot find /{g.name} in GlyphData {md.glyphSet.__class__.__name__}')

        elif gd.isLower:
            guidelines.append((xo + tg * (md.ascender + overshoot), md.ascender + overshoot, 0, f"{md.ascender + overshoot} ({overshoot})"))
            guidelines.append((x + tg * md.ascender, md.ascender, 0, f'Ascender {md.ascender}'))
            guidelines.append((xo + tg * (md.descender - overshoot), md.descender - overshoot, 0, f'{md.descender - overshoot} ({overshoot})'))
            guidelines.append((x + tg * md.descender, md.descender, 0, f'Descender {md.descender}'))

        if md.stemOvershoot is not None: # Font is using single stem overshoots, e.g. with rounded stems as in Upgrade Neon
            guidelines.append((xo + tg * (height + md.stemOvershoot), height + md.stemOvershoot, 0, f"{height + md.stemOvershoot} ({md.stemOvershoot})"))
            guidelines.append((xo + tg * (baseline - md.stemOvershoot), baseline - md.stemOvershoot, 0, f"{baseline - md.stemOvershoot} ({md.stemOvershoot})"))

        if forced or len(g.guidelines) != len(guidelines):
            # Amounts are different, too complex to compare. Just rebuild all guidelines.
            changed = True
            g.clearGuidelines()
            for x, y, angle, name in guidelines:
                g.appendGuideline((x, y), angle, name=name)
        else: # The amount of guidelines match, check if the position and names are stil the same.
            for gIndex, guideline in enumerate(g.guidelines):
                x, y, angle, name = guidelines[gIndex]
                if guideline.x != x or guideline.y != y or guideline.name != name:
                    print('... Set guide', x, y, name)
                    guideline.x = x
                    guideline.y = y
                    guideline.name = name
                    guideline.changed() # Handle the update for just the guideline.

        return changed

