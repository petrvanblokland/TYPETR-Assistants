# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   anchors.py
#
#   Strategies for anchor placements
#   - Type and amount of anchors are defined by the anchors list in the GlyphSet/GlyphData
#   - Or by the anchors of base glyphs
#   - Or by the anchors in the roman/italic companion masters
#   - Anchors that refer to a base, get their (relative) horizontal (slanted) positions from it.
#   - Vertical position too, unless there are already diacritics lower and/or higher, then the vertical position is adjusted to fit the glyph bounding box.
#   - Otherwise check if there is a set of predefined vertical position for each anchor type
#   - The assistant decides on an initial strategy, but then the user can alter that.
#   - If an anchor was dragged, this is stored in the glyph.lib, so it will not change by the assistant anymore.
#   - Unless that flag is cleared.
#
import sys, copy
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
from assistantLib.assistantParts.glyphsets.anchorData import AD

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
                position=(0, 0),
                fillColor=(0, 0, 0.5, 0.2),
                visible=False,
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
                        diacriticsLayer.setVisible(True)
                        dIndex += 1

        for n in range(dIndex, len(self.anchorsDiacriticsCloud)):
            self.anchorsDiacriticsCloud[n].setVisible(False)
        
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
        personalKey_A = self.registerKeyStroke('A', 'anchorsGlyphKey') # Check/fix all glyphs in the current font
        personalKey_a = self.registerKeyStroke('a', 'anchorsGlyphKey')
        personalKey_exclam = self.registerKeyStroke('!', 'anchorsCenterOnWidth')

        """Build the assistant UI for anchor controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c.w.autoAnchors = CheckBox((C0, y, CW, L), 'Auto anchors', value=True, sizeStyle='small')
        c.w.copyRomanAnchors = CheckBox((C1, y, CW, L), 'Copy roman-->italic', value=True, sizeStyle='small')
        c.w.fixAnchorsButton = Button((C2, y, CW, L), 'Fix anchors [%s]' % personalKey_a, callback=self.anchorsCallback)
        y += L
        # Radios to select the type of anchor mode for the current glyph, in this order.
        # So if there are no components, then the horizontal position of boundingbox/2 is used.
        c.w.anchorXModes = RadioGroup((C0, y, 3*CW, L), ('X-Base', 'X-Box/2', 'X-Rom/Ita', 'X-Width/2', 'X-Manual'), isVertical=False, sizeStyle='small', callback=self.anchorXModesCallback)
        c.w.anchorXModes.set(0)
        y += L
        c.w.anchorYModes = RadioGroup((C0, y, 3*CW, L), ('Y-Base', 'Y-Box/2', 'Y-Rom/Ita', 'Y-Width/2', 'Y-Manual'), isVertical=False, sizeStyle='small', callback=self.anchorYModesCallback)
        c.w.anchorYModes.set(0)
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8
        y += L

        return y

    def anchorsCallback(self, sender):
        g = self.getCurrentGlyph()
        if self.checkFixAnchors(g): # Create missing anchors and check X and Y position of anchors
            g.changed() # Force update. UpdateAnchors will then check and update.

    def anchorXModesCallback(self, sender):
        g = self.getCurrentGlyph()
        self._fixGlyphAnchorsX(g)

    def anchorYModesCallback(self, sender):
        g = self.getCurrentGlyph()
        self._fixGlyphAnchorsY(g)

    def _fixGlyphAnchorsX(self, g):
        changed = False
        done = False
        gd = self.getGlyphData(g)
        d = self.getLib(g, 'Anchors', {})['Xmode'] = sender.get()
        for a in g.anchors:
            if not a.name in AD.CENTERING_ANCHORS:
                continue
            if d == 0: # X-Base: If there is a base glyph, then set the x-position identical, shifted by the base offset.
                print('X-Base')
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g)
                if baseGlyph is not None:
                    ba = self.getAnchor(baseGlyph, a.name)
                    if ba is not None:
                        changed = self._setAnchorX(g, a, ba.x + dx)
                        done = True

            if not done and d == 1: # X-Box/2
                print('X-Box/2')
                bounds = g.bounds
                if bounds is not None:
                    x1, _, x2, _ = bounds
                    changed = self._setAnchorsX(g, x1 + (x2 - x1)/2)
                    done = True

            if not done and d == 2: # X-Rom/Ita
                print('X-Rom/Ita')
                changed = self.checkFixRomanItalicAnchors(g, doX=True)
                done = True

            if not done and d == 3: # X-Width/2
                print('X-Width/2')
                changed = self._setAnchorsX(g, g.width/2)
                done = True

            if not done: # d == 4: # X-Manual
                print('X-Manual')
                changed = False

            if changed:
                g.changed()

    def _fixGlyphAnchorsY(self, g):
        """Fix the anchors X-position if it is different from where it should be according to the current mode."""
        return False

        d = self.getLib(g, 'Anchors', {})['Ymode'] = sender.get()
        if d == 0: # Y-Base
            print('Y-Base')
        
        elif d == 1: # Y-Box/2
            print('Y-Box/2')
            bounds = g.bounds
            if bounds is not None:
                _, y1, _, y2 = bounds
                for a in g.anchors:
                    if not a.name in AD.CENTERING_ANCHORS:
                        continue
                    changed |= self._setAnchorsY(g, y1 + (y2 - y1)/2)
        
        elif d == 2: # Y-Rom/Ita
            print('Y-Rom/Ita')
            changed = self.checkFixRomanItalicAnchors(g, doY=True)
            done = True

        elif d == 3: # Y-Width/2
            print('Y-Width/2')
        
        else: # d == 4: # Y-Manual
            print('Y-Manual')
        
        if changed:
            g.changed()

    def _setAnchorX(self, g, a, x):
        changed = False
        ax = int(round(self.italicX(g, x, a.y)))
        if abs(ax - a.x) >= 1: # Too different, correct it
            print(f'... Set anchor {a.name}.x from {a.x:0.2f} to {ax}')
            a.x = ax
            changed = True
        return changed

    def _setAnchorsY(self, g, y):
        changed = False
        return changed

    #   E V E N T S

    def checkFixAnchors(self, g):
        """Check and fix the anchors of g. First try to determine if the right number of anchors exists. There are
        2 ways (based on legacy data) to find the anchors that this glyph needs: as defined in the glyphData if named 
        anchors are part of the tables. But GlyphData already includes GLYPH_ANCHORS if no anchor attribute is defined.
        So, looking into G;lyphData is enough."""
        changed = False
        changed |= self.checkFixRequiredAnchors(g) # First make sure that they all exist.
        changed |= self.checkFixZeroWidthAnchorPosition(g)
        changed |= self.checkFixRomanItalicAnchors(g)
        return changed

    ANCHORS_DEFAULT_LIB_KEY = dict(
        Xmode=0, # Default anchors for X from base glyph, if it exists
        Ymode=0, # Default anchors for Y from base glyph, if it exists
    )

    def checkFixRequiredAnchors(self, g):
        """Check/fix the required anchors if they don't all exist or if there are too many."""
        changed = False
        gd = self.getGlyphData(g)
        done = [] # Remember which are already done, to detect duplicate anchors
        requiredAnchorNames = gd.anchors  
        anchorNames = self.getAnchorNames(g)
        if requiredAnchorNames != anchorNames:
            for a in g.anchors[:]: # Make a copy of the list, as it may be altered
                if a.name in done: # Detact duplicate anchors
                    print(f'... Remove duplucate anchor "{a.name}" in /{g.name}')
                    g.removeAnchor(a)
                    changed = True
                elif a.name not in requiredAnchorNames:  
                    print(f'... Remove obsolete anchor "{a.name}" in /{g.name}')
                    g.removeAnchor(a)
                    changed = True
                else:
                    done.append(a.name)

            for aName in requiredAnchorNames:
                if aName not in anchorNames:
                    print(f'... Add missing anchor "{aName}" in /{g.name}')
                    g.appendAnchor(name=aName, position=(0, 0)) # Just put at origin, position will be set in later checks.
                    changed = True        
        return changed

    def setGlyphAnchors(self, g):
        """Called when the EditWindow selected a new glyph. Try to  find previous anchor info in g.lib,
        about mode by which the current anchors are set and if they were manually moved."""
        c = self.getController()
        d = self.getLib(g, 'Anchors', copy.deepcopy(self.ANCHORS_DEFAULT_LIB_KEY))
        c.w.anchorXModes.set(d.get('Xmode', 0))
        c.w.anchorYModes.set(d.get('Ymode', 0))
        #print('... setGlyphAnchors', g.name, d)

    #   K E Y S

    def anchorsGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']
        if c.lower() == c: # Just the current glyph
            glyphs = [g]
        else:
            glyphs = g.font
        for gg in glyphs:
            if self.checkFixAnchors(gg):
                gg.changed()

    def anchorsCenterOnWidth(self, g, c, event):
        """If there are anchors selected, then center them on the width. If no anchors are selected,
        the center all on width."""
        changed = False
        for a in self.getAnchors(g): # Answers selected anchors or all
            if not a.name in AD.CENTERING_ANCHORS: # Does this anchor center?
                continue # Otherwise ignore
            x = int(round(g.width/2 + a.y * tan(radians(-g.font.info.italicAngle or 0))))
            y = int(round(a.y))
            if abs(a.x - x) > 1 or abs(a.y - y) > 1:
                print(f'... Centering anchor “{a.name} of /{g.name}')
                a.x = x
                a.y = y
                changed = True
        if changed:
            g.changed()

    def checkFixRomanItalicAnchors(self, g, doX=False, doY=False):
        """If there is a base glyph, then Check if the anchors in the counterpart roman or italic glyph is the same as for the current font.
        If not, then add the missing anchor and position it on slanted position.
        Note that will be other checking/fixing done too, so the filter should be exclusive."""
        changed = False
        f = g.font
        md = self.getMasterData(f)
        gd = self.getGlyphData(g)
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
                        if doX:
                            a.x = x
                            print(f'... Fix anchor.x "{aName}" of /{g.name} to ({x}, {y})')
                            changed = True
                        if doY:
                            a.y = y
                            print(f'... Fix anchor.y "{aName}" of /{g.name} to ({x}, {y})')
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
                    a.x = ix # Only change x position for this.
                    changed = True
                    break
        return changed

