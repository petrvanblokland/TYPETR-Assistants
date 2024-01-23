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

class AssistantPartAnchors(BaseAssistantPart):
    """The Anchors assistant part handles all creation and placement of anchors.
    Also it supports the display of the diacritics clouds and it positions diacitics of related
    base glyphs if their position does not sychronize with the position of their anchors.
    """

    def initMerzAnchors(self, container):
        """Register key stroke [a] to sync anchor positions"""
        self.registerKeyStroke('a', 'anchorsGlyphKey')

    def updateAnchors(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width."""
        g = info['glyph']
        if g is None:
            return
        changed = False

        changed |= self.checkFixZeroWidthAnchorPosition(g)
        if changed:
            g.changed()

    def buildAnchors(self, y):
        """Build the assistant UI for anchor controls."""
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        self.w.autoAnchors = CheckBox((C0, y, CW, L), 'Auto anchors', value=True, sizeStyle='small')
        y += L

        return y

    def anchorsCallback(self, sender):
        g = self.currentGlyph()
        #g.clear() 
        g.changed() # Force update. UpdateItalize will then rebuild the glyph.

    def anchorsGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']
        
        print('... anchorsGlyphKey')
        #self.italicizeGlyph(g)

    def checkFixZeroWidthAnchorPosition(self, g):
        """Check on the (horizontal) position of anchors for glyphs with zero with.
        Make sure that the implementation of the anchors in assistants is done after checking the spacing."""
        if g.width == 0:
            for a in g.anchors:
                ix = self.italicX(g, 0, a.y)
                if abs(ix - a.x) >= 1: # Not in position, move it
                    print(f'... Move /{g.name} anchor {a.name} from {a.x} to {ix}')
                    a.x = ix
                    return True
        return False # Did not change

