# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   anchors.py
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

class AssistantPartAnchors(BaseAssistantPart):
    """The Anchors assistant part handles all creation and placement of anchors.
    Also it supports the display of the diacritics clouds and it positions diacitics of related
    base glyphs if their position does not sychronize with the position of their anchors.
    """

    def initMerzAnchors(self, container):
        pass

    def updateAnchors(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width."""
        c = self.getController()
        g = info['glyph']
        if g is None:
            return
        if c.w.autoAnchors.get():
            self.checkFixAnchors(g)

    def buildAnchors(self, y):
        """Register key stroke [a] to sync anchor positions"""
        personalKey = self.registerKeyStroke('a', 'anchorsGlyphKey')

        """Build the assistant UI for anchor controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c.w.fixAnchorsButton = Button((C0, y, CW, L), 'Fix anchors [%s]' % personalKey, callback=self.anchorsCallback)
        c.w.autoAnchors = CheckBox((C1, y, CW, L), 'Auto anchors', value=True, sizeStyle='small')
        c.w.copyRomanAnchors = CheckBox((C2, y, CW, L), 'Copy roman-->italic', value=True, sizeStyle='small')
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8
        y += L
        
        return y

    def anchorsCallback(self, sender):
        g = self.getCurrentGlyph()
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

    def checkFixAnchors(self, g):
        changed = False
        changed |= self.checkFixZeroWidthAnchorPosition(g)
        changed |= self.checkFixRomanItalicAnchors(g)
        changed |= self.checkFixComponents(g)
        changed |= self.checkFixComponentPositions(g)
        if changed:
            g.changed()

    def checkFixRomanItalicAnchors(self, g):
        """Check if the anchors in the counterpart roman or italic glyph is the same as for the current font.
        If not, then add the missing anchor and position it on slanted position.
        Note that will be other checking/fixing done too, so the filter should be exclusive."""
        changed = False
        f = g.font
        md = self.getMasterData(f)
        src = self.getFont(md.romanItalicUFOPath)
        if g.name in src:
            srcG = src[g.name]
            anchors = self.getAnchors(g) # Get a dictionary of anchors
            srcAnchors = self.getAnchors(srcG)
            for aName, srcA in srcAnchors.items():
                x = int(round(srcA.x + srcA.y * tan(radians(-f.info.italicAngle or 0))))
                y = int(round(srcA.y))
                if not aName in anchors:
                    g.appendAnchor(position=(x, srcA.y), anchor=srcA)
                    changed = True
                    print(f'... Add anchor "{aName}" to /{g.name} at ({x}, {y})')
                else:
                    a = anchors[aName]
                    if abs(a.x - x) >= 1 or abs(a.y - y) >= 1:
                        a.x = x
                        a.y = y
                        print(f'... Fix anchor "{aName}" of /{g.name} to ({x}, {y})')
                        changed = True
        return changed

    def checkFixZeroWidthAnchorPosition(self, g):
        """Check on the (horizontal) position of anchors for glyphs with zero with.
        Make sure that the implementation of the anchors in assistants is done after checking the spacing.
        Note that will be other checking/fixing done too, so the filter should be exclusive."""
        if g.width == 0:
            for a in g.anchors:
                ix = self.italicX(g, 0, a.y)
                if abs(ix - a.x) >= 1: # Not in position, move it
                    print(f'... Move /{g.name} anchor {a.name} from {a.x} to {ix}')
                    a.x = ix
                    return True
        return False # Did not change

    def checkFixComponents(self, g):
        """Check the existence of gd.base and gd.accent component. Create them when necessary.
        And delete components that are not defined in the GlyphData.
        These are the checks:
        1 There are components but there should be none
        2 There are no components but there should be one or more
        3 The number of existing components is larger than it should be
        4 The number of existing components is smaller than it should be
        5 The number of components it right,  but their baseGlyph names are wrong
        6 The number and names of existing components are just right
         """
        changed = False
        md = self.getMasterData(g.font)
        gd = md.glyphset.get(g.name)
        if gd is None:
            print(f'### checkFixComponents: Glyph /{g.name} does not exist in glyphset {gd.__class__.__name__}')
            if g.components:
                if gd.base and gd.base != g.components[0].baseGlyph:
                    g.components[0].baseGlyph = gd.base
                    print(f'... Set base component of /{g.name} to ')
        return changed

    def checkFixComponentPositions(self, g):
        """For all components check if they are in place. If the base component has an anchor
        and there are diacritic components that have the matching achor, then move the diacritics
        so the positions of the anchors match up."""
        if not g.components: # This must be a base glyph, check for drawing the diacritics cloud of glyphs that have g as base.
            pass
        else:
            for component in g.components:
                pass

        return False