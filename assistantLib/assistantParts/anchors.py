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

    Most generic/basic anchor methods are support by self (inheriting from BaseAssistant) 
    """

    def initMerzAnchors(self, container):
        """Initialize the Merz object for this assistant part.
        Note that the diacritics-cloud object are supported by the contours part.
        """
        self.anchorsDiacriticsCloud = [] # Storage of diacritics images
        for dIndex in range(self.MAX_DIACRITICS_CLOUD): # Max number of diacritics in a glyph. @@@ If too low, some diacritics don't show
            self.anchorsDiacriticsCloud.append(self.backgroundContainer.appendPathSublayer(
                name='diacritics-%d' % dIndex,
                position=(FAR, 0),
                fillColor=(0, 0, 0.5, 0.2),
            ))

    def updateMerzAnchors(self, info):
        """Update the diacritics cloud, depending on the existing anchors"""
        changed = False
        g = info['glyph']
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        dIndex = 0 # Index into showing diacritics Merz layers
        assert gd is not None # Otherwise the glyph data does not exist.
        for a in g.anchors:
            for dName in AD.EXAMPLE_DIACRITICS.get(a.name, []):
                if dName in g.font:
                    dg = g.font[dName]
                    dAnchor = self.getAnchor(dg, AD.CONNECTED_ANCHORS[a.name])
                    if dAnchor is not None:
                        diacriticsLayer = self.anchorsDiacriticsCloud[dIndex] # Get layer for this diacritics glyph
                        diacriticsPath = dg.getRepresentation("merz.CGPath") 
                        diacriticsLayer.setPath(diacriticsPath)
                        ax = a.x - dAnchor.x
                        ay = a.y - dAnchor.y
                        diacriticsLayer.setPosition((ax, ay))
                        dIndex += 1

        for n in range(dIndex, len(self.anchorsDiacriticsCloud)):
            self.anchorsDiacriticsCloud[n].setPosition((FAR, 0))
        
    def updateAnchors(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width."""
        changed = False
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed to the glyph
        if c.w.autoAnchors.get():
            changed |= self.checkFixAnchors(g)
        return changed

    def buildAnchors(self, y):
        """Register key stroke [a] to sync anchor positions"""
        personalKey = self.registerKeyStroke('a', 'anchorsGlyphKey')

        """Build the assistant UI for anchor controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c.w.autoAnchors = CheckBox((C0, y, CW, L), 'Auto anchors', value=True, sizeStyle='small')
        c.w.copyRomanAnchors = CheckBox((C1, y, CW, L), 'Copy roman-->italic', value=True, sizeStyle='small')
        c.w.fixAnchorsButton = Button((C2, y, CW, L), 'Fix anchors [%s]' % personalKey, callback=self.anchorsCallback)
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8
        y += L

        return y

    def anchorsCallback(self, sender):
        g = self.getCurrentGlyph()
        if self.checkFixAnchors(g):
            g.changed() # Force update. UpdateItalize will then rebuild the glyph.

    def anchorsGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']
        
        if self.checkFixAnchors(g):
            g.changed()

    def checkFixAnchors(self, g):
        changed = False
        changed |= self.checkFixZeroWidthAnchorPosition(g)
        changed |= self.checkFixRomanItalicAnchors(g)
        return changed

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
            anchors = self.getAnchorsDict(g) # Get a dictionary of anchors
            srcAnchors = self.getAnchorsDict(srcG)
            for aName, srcA in srcAnchors.items():
                x = int(round(srcA.x + srcA.y * tan(radians(-f.info.italicAngle or 0))))
                y = int(round(srcA.y))
                if not aName in anchors:
                    g.appendAnchor(position=(x, srcA.y), anchor=srcA)
                    print(f'... Add anchor "{aName}" to /{g.name} at ({x}, {y})')
                    changed = True
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
        Note that will be other checking/fixing done too, so the filter should be exclusive.
        Answer the boolean flag if something changed to the glyph."""
        changed = False
        if g.width == 0:
            for a in g.anchors:
                ix = self.italicX(g, 0, a.y)
                if abs(ix - a.x) >= 1: # Not in position, move it
                    print(f'... Move /{g.name} anchor {a.name} from {a.x} to {ix}')
                    a.x = ix
                    changed = True
                    break
        return changed

