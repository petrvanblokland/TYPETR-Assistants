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

    MAX_DIACRITICS_CLOUD = 40

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
        c.w.anchorYModes = RadioGroup((C0, y, 3*CW, L), ('Y-Metrics', 'Y-Base', 'Y-Manual'), isVertical=False, sizeStyle='small', callback=self.anchorYModesCallback)
        c.w.anchorYModes.set(0)
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8
        y += L

        return y

    def anchorsCallback(self, sender):
        changed = False
        g = self.getCurrentGlyph()
        changed |= self.checkFixAnchors(g) # Create missing anchors and check X and Y position of anchors
        if changed:
            g.changed() # Force update. UpdateAnchors will then check and update.

    def anchorXModesCallback(self, sender):
        changed = False
        g = self.getCurrentGlyph()
        self.getLib(g, 'Anchors', {})['Xmode'] = sender.get()
        changed |= self._fixGlyphAnchorsX(g)
        if changed:
            g.changed()

    def anchorYModesCallback(self, sender):
        changed = False
        g = self.getCurrentGlyph()
        self.getLib(g, 'Anchors', {})['Ymode'] = sender.get()
        changed |= self._fixGlyphAnchorsY(g)
        if changed:
            g.changed()

    def checkFixAnchorsXPosition(self, g):
        """Check/fix the x-position of the anchors named in AD.CENTERING_ANCHORS. It is assumed there that all anchors exist."""
        return self._fixGlyphAnchorsX(g)

    def _fixGlyphAnchorsX(self, g):
        """In sequence (or as defined by the mode in radio-buttons) trying to find the x-position of anchors:
        'X-Base', 'X-Box/2', 'X-Rom/Ita', 'X-Width/2', 'X-Manual'
        """
        changed = done = False
        gd = self.getGlyphData(g)
        xMode = self.getLib(g, 'Anchors', {})['Xmode']
        for a in g.anchors:
            if a.name not in AD.CENTERING_ANCHORS: # Only for these. Diacritics like /ogonekcomb and /tonoscomb need positions manually in x.
                continue

            if xMode == 0: # X-Base: If there is a base glyph, then set the x-position identical, shifted by the base offset.
                #print(xMode, 'X-Base', a.name)
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g)
                if baseGlyph is not None:
                    ba = self.getAnchor(baseGlyph, a.name)
                    if ba is not None:
                        changed = self._setAnchorX(g, a, ba.x + dx)
                        done = True

            if not done and xMode <= 1: # X-Box/2
                #print(xMode, 'X-Box/2', a.name)
                bounds = g.bounds
                if bounds is not None:
                    x1, _, x2, _ = bounds
                    changed = self._setAnchorX(g, a, x1 + (x2 - x1)/2)
                    done = True

            if not done and xMode <= 2: # X-Rom/Ita
                #print(xMode, 'X-Rom/Ita', a.name)
                changed = self.checkFixRomanItalicAnchors(g, doX=True)
                done = True

            if not done and xMode <= 3: # X-Width/2
                #print(xMode, 'X-Width/2', a.name)
                changed = self._setAnchorX(g, a, g.width/2)
                done = True

            if not done and xMode <= 4: # X-Manual
                #print(xMode, 'X-Manual', a.name)
                changed = False

        return changed

    def checkFixAnchorsYPosition(self, g):
        """Check/fix the y-position of the anchors named in AD.CENTERING_ANCHORS. It is assumed there that all anchors exist."""
        return self._fixGlyphAnchorsY(g)

    def _fixGlyphAnchorsY(self, g):
        """Fix the anchors X-position if it is different from where it should be according to the current mode.
        Strategies: 
        - If there are vertical metrics rules defined for each type of anchor, for the base or this type of glyph, then apply them.
        - If there is a base, then take the y position of the base anchors
        - If the vertical positions are too much inside the vertical bounds of the diacritics, then move up/down
        """
        changed = done = False
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)
        yMode = self.getLib(g, 'Anchors', {})['Ymode']
        for a in g.anchors:
            y = None
            # First guess, if there is a base, the use that as a start.
            if a.name == AD.TOP_:
                y = md.getHeight(g.name) - md.getAnchorOvershoot(g.name)    
            elif a.name == AD.MIDDLE_:
                y = md.getHeight2(g.name)
            elif a.name == AD.BOTTOM_:
                y = md.getBaseline(g.name) + md.getAnchorOvershoot(g.name)
            if y is not None:
                changed |= self._setAnchorY(g, a, y) 

            if 0 and yMode == 0: # Y-Base: If there is a base glyph, then set the x-position identical, shifted by the base offset.
                #print(yMode, 'Y-Base', a.name)
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g)
                if baseGlyph is not None:
                    ba = self.getAnchor(baseGlyph, a.name)
                    if ba is not None:
                        changed = self._setAnchorX(g, a, ba.x + dx)
                        done = True

            if not done and yMode <= 1: # Y-Metrics
                #print(yMode, 'Y-Metrics', a.name')
                pass

        return changed

    def _setAnchorX(self, g, a, x):
        changed = False
        ax = int(round(self.italicX(g, x, a.y)))
        if abs(ax - a.x) >= 1: # Too different, correct it
            print(f'... Set anchor {a.name}.x from {int(round(a.x))} to {ax}')
            a.x = ax
            changed = True
        return changed

    def _setAnchorY(self, g, a, y):
        changed = False
        if abs(y - a.y) >= 1: # Too different, correct it
            print(f'... Set anchor {a.name}.y from {int(round(a.y))} to {y}')
            a.y = y
            changed = True
        return changed

    #   E V E N T S

    def checkFixAnchors(self, g):
        """Check and fix the anchors of g. First try to determine if the right number of anchors exists. There are
        2 ways (based on legacy data) to find the anchors that this glyph needs: as defined in the glyphData if named 
        anchors are part of the tables. But GlyphData already includes GLYPH_ANCHORS if no anchor attribute is defined.
        So, looking into G;lyphData is enough."""
        changed = False
        changed |= self.checkFixRequiredAnchors(g) # First make sure that they all exist.
        changed |= self.checkFixAnchorsYPosition(g) # Fix Y before X for italics
        changed |= self.checkFixAnchorsXPosition(g)
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

