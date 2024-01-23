# -*- coding: UTF-8 -*-

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

class AssistantPartSpacer(BaseAssistantPart):
    """The Spacer assistant part handles all margins and widths that can be automated.
    It makes guesses based on the names of glyphs, existing components, values in the MasterData
    and Erik van Blokland's Similarity.
    The assistant part gives feedback about where the automated values came from, so it's easier to debug.
    """

    # List with names of glyphs that need zero with. To be redefined by inheriting assistant classes.
    # If redefined, that turns of automated guessing which glyph have zero width.
    SPACER_ZERO_WIDTH = None
    SPACER_ZERO_WIDTH_PATTERNS = ('.component',)
    SPACER_ZERO_WIDTH_END_PATTERNS = ('cmb', 'comb')

    def initMerzSpacer(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        self.registerKeyStroke('=', 'spacerCenterGlyph')

    def updateSpacer(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width."""
        g = info['glyph']
        if g is None:
            return
        changed = False

        changed |= self.checkFixZeroWidth(g)
        if changed:
            g.changed()

    def buildSpacer(self, y):
        """Build the assistant UI for anchor controls."""
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        self.w.autoSpace = CheckBox((C0, y, CW, L), 'Auto space', value=True, sizeStyle='small')
        y += L + LL

        return y

    #   G U E S S  W I D T H S

    def _fixGlyphWidth(self, g, width):
        if g.width != width:
            print(f'... Fix glyph width: Set /{g.name} width from {g.width} to {width}')
            g.width = width
            return True
        return False

    def checkFixZeroWidth(self, g):
        """Check if this glyph should have zero width. If it has width then fix it and answer True."""
        if self.SPACER_ZERO_WIDTH is not None: # Predefined list by inheriting assistant class
            if g.name in self.SPACER_ZERO_WIDTH:
                return self._fixGlyphWidth(g, 0)
        # Nothing defined, try to guess based on name
        for pattern in self.SPACER_ZERO_WIDTH_END_PATTERNS:
            if g.name.endswith(pattern):
                return self._fixGlyphWidth(g, 0)
        for pattern in self.SPACER_ZERO_WIDTH_PATTERNS:
            if pattern in g.name:
                return self._fixGlyphWidth(g, 0)

        return False

    def spacerCenterGlyph(self, g, c, event):     
        """Snap the selected points of the current glyph onto points that are within range on the background glyph."""
        lm = g.angledLeftMargin
        rm = g.angledRightMargin
        w = g.width
        if lm is not None:
            g.angledLeftMargin = (lm + rm)/2
            g.width = w
            g.changed()
            