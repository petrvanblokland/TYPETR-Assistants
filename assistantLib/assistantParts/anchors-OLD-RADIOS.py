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

from mojo.roboFont import AllFonts

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
    MAX_GUESSED_ANCHORS = 50
    ANCHOR_LABEL_FONT = 'Verdana'
    ANCHOR_LABEL_SIZE = 12
    GUESSED_ANCHOR_MARKER_R = 8
    GUESSED_ANCHOR_POSITION_COLOR = 0, 0.5, 0, 1 # Color of marker outlines
    GUESSED_ANCHOR_POSITION_COLOR2 = 0, 0.25, 0, 1 # Color of labels

    def initMerzAnchors(self, container):
        """Initialize the Merz object for this assistant part.
        Note that the diacritics-cloud object are supported by the contours part.
        """
        self.guessedAnchorPositions = {} # Calculated if editor windows set glyph. Key is (x, y), value is (anchpr, methodNameX, methodNamey)

        self.anchorsDiacriticsCloud = [] # Storage of diacritics images
        for dIndex in range(self.MAX_DIACRITICS_CLOUD): # Max number of diacritics in a glyph. @@@ If too low, some diacritics don't show
            self.anchorsDiacriticsCloud.append(self.backgroundContainer.appendPathSublayer(
                name='diacritics-%d' % dIndex,
                position=(0, 0),
                fillColor=(0, 0, 0.5, 0.2),
                visible=False,
            ))
        self.guessedAnchorPositions1 = [] # Storage of guessed anchor positions and their labels, showing as two concentric circles
        self.guessedAnchorPositions2 = [] 
        self.guessedAnchorLabels = []
        for aIndex in range(self.MAX_GUESSED_ANCHORS): # Max number of guessed anchor positions to show
            self.guessedAnchorPositions1.append(container.appendOvalSublayer(name='guessedAnchorPosition1%d' % aIndex,
                position=(0, 0),
                size=(self.GUESSED_ANCHOR_MARKER_R*2, self.GUESSED_ANCHOR_MARKER_R*2),
                fillColor=(0.1, 0.8, 0.7, 0.25),
                strokeColor=self.GUESSED_ANCHOR_POSITION_COLOR,
                strokeWidth=1,
                visible=False,
            ))
            self.guessedAnchorPositions2.append(container.appendOvalSublayer(name='guessedAnchorPosition2%d' % aIndex,
                position=(0, 0),
                size=(self.GUESSED_ANCHOR_MARKER_R*4, self.GUESSED_ANCHOR_MARKER_R*4),
                fillColor=(0.1, 0.4, 0.35, 0.25),
                strokeColor=self.GUESSED_ANCHOR_POSITION_COLOR,
                strokeWidth=1,
                visible=False,
            ))
            self.guessedAnchorLabels.append(container.appendTextBoxSublayer(name='guessedAnchorLabel%d' % aIndex,
                position=(0, 0),
                size=(400, 100),
                font=self.ANCHOR_LABEL_FONT,
                pointSize=self.ANCHOR_LABEL_SIZE,
                fillColor=self.GUESSED_ANCHOR_POSITION_COLOR2,
                alignment='center',
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
        if c is None: # In case the window is closed
            return False

        g = info['glyph']
        if g is None:
            return False # Nothing changed to the glyph
        if c.w.autoAnchors.get():
            changed |= self.checkFixAnchors(g)

        # Update the guessed positions, in case one of the X/Y positions depends on the current positions of an axis
        self.updateGuessedAnchorPositions(g)

        return changed

    def buildAnchors(self, y):
        """Register key stroke [a] to sync anchor positions"""
        personalKey_A = self.registerKeyStroke('A', 'anchorsGlyphKey') # Check/fix all glyphs in the current font
        personalKey_a = self.registerKeyStroke('a', 'anchorsGlyphKey')
        personalKey_exclam = self.registerKeyStroke('!', 'anchorsCenterOnWidth')

        """Build the assistant UI for anchor controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        # @@@ THIS WILL GO TO A SEPARATE WINDOW WITH MORE SPACE FOR CHOICES
        c.w.autoAnchors = CheckBox((C0, y, CW, L), 'Auto anchors', value=True, sizeStyle='small')
        c.w.copyRomanAnchors = CheckBox((C1, y, CW, L), 'Copy roman-->italic', value=True, sizeStyle='small')
        c.w.fixAnchorsButton = Button((C2, y, CW, L), f'Fix anchors [{personalKey_A}{personalKey_a}]', callback=self.anchorsCallback)
        y += L
        # Radios to select the type of anchor mode for the current glyph, in this order.
        # So if there are no components, then the horizontal position of boundingbox/2 is used.
        c.w.anchorXModes = RadioGroup((C0, y, 3*CW, L), ('X-Base', 'X-Box/2', 'X-Rom/Ita', 'X-Width/2', 'X-Manual'), isVertical=False, sizeStyle='small', callback=self.anchorXModesCallback)
        c.w.anchorXModes.set(0)
        y += L
        c.w.anchorYModes = RadioGroup((C0, y, 3*CW*4/5, L), ('Y-Diacritics', 'Y-Base', 'Y-Metrics', 'Y-Manual'), isVertical=False, sizeStyle='small', callback=self.anchorYModesCallback)
        c.w.anchorYModes.set(0)
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8
        y += L

        return y

    def closingAnchors(self):
        """Called when the main assistant window is about to close. We can close our anchors window here."""
        c = self.getController()
        #c.anchorsWindow.close()

    def anchorsCallback(self, sender):
        changed = False
        g = self.getCurrentGlyph()
        changed |= self.checkFixAnchors(g) # Create missing anchors and check X and Y position of anchors
        if changed:
            g.changed() # Force update. UpdateAnchors will then check and update.

    def anchorXModesCallback(self, sender):
        """Save the x-mode selection in the name glyph for all open fonts."""
        changed = False
        g = self.getCurrentGlyph()
        for f in AllFonts(): # Keep them compatible for the same glyph in all fonts
            if g.name not in f:
                continue
            gg = f[g.name]
            self.getLib(gg, 'Anchors', {})['Xmode'] = sender.get()
            changed |= self._fixGlyphAnchorsX(gg)
            if changed:
                gg.changed()

    def anchorYModesCallback(self, sender):
        """Save the y-mode selection in the name glyph for all open fonts."""
        changed = False
        g = self.getCurrentGlyph()
        for f in AllFonts(): # Keep them compatible for the same glyph in all fonts
            if g.name not in f:
                continue
            gg= f[g.name]
            self.getLib(gg, 'Anchors', {})['Ymode'] = sender.get()
            changed |= self._fixGlyphAnchorsY(gg)
            if changed:
                gg.changed()

    def checkFixAnchorsXPosition(self, g):
        """Check/fix the x-position of the anchors named in AD.CENTERING_ANCHORS. It is assumed there that all anchors exist."""
        return self._fixGlyphAnchorsX(g)

    def _fixGlyphAnchorsX(self, g):
        """In sequence (or as defined by the mode in radio-buttons) trying to find the x-position of anchors:
        'X-Base', 'X-Box/2', 'X-Rom/Ita', 'X-Width/2', 'X-Manual'
        """
        changed = False
        gd = self.getGlyphData(g)
        xMode = self.getLib(g, 'Anchors', {}).get('Xmode')
        if xMode is None: # Lib was not complete, reinitialize. Maybe make this more generic later.
            self.setLib(g, 'Anchors', copy.copy(self.ANCHORS_DEFAULT_LIB_KEY))
            xMode = self.getLib(g, 'Anchors', {}).get('Xmode')

        for a in g.anchors:

            """Check on the (horizontal) position of anchors for glyphs with zero with.
            Make sure that the implementation of the anchors in assistants is done after checking the spacing.
            Note that will be other checking/fixing done too, so the filter should be exclusive.
            Answer the boolean flag if something changed to the glyph."""
            if g.width == 0:
                ix = self.italicX(g, 0, a.y)
                if abs(ix - a.x) >= 1: # Not in position, move it
                    print(f'... Move /{g.name} anchor.x {a.name} from {a.x} to {ix}')
                    a.x = ix # Only change x position for this.
                    changed = True
                continue

            if a.name not in AD.CENTERING_ANCHORS: 
                # Only for these. Anchors do diacritics like /ogonekcomb and /tonoscomb need positions manually in x.
                continue

            if xMode == 0: # X-Base: If there is a base glyph, then set the x-position identical, shifted by the base offset.
                #print(xMode, 'X-Base', a.name)
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g)
                if baseGlyph is not None:
                    ba = self.getAnchor(baseGlyph, a.name)
                    if ba is not None:
                        changed = self._setAnchorXY(g, a, ba.x + dx, ba.y + dy, italicize=False) # Anchors from base are already italicized.
                    continue

            if xMode <= 1: # X-Box/2
                #print(xMode, 'X-Box/2', a.name)
                x1 = g.angledLeftMargin
                x2 = g.width - g.angledRightMargin
                changed = self._setAnchorX(g, a, x1 + (x2 - x1)/2)
                continue

            if xMode <= 2: # X-Rom/Ita
                #print(xMode, 'X-Rom/Ita', a.name)
                changed = self.checkFixRomanItalicAnchors(g, doX=True) # Check positions, not if the anchors exist.
                continue

            if xMode <= 3: # X-Width/2
                #print(xMode, 'X-Width/2', a.name)
                changed = self._setAnchorX(g, a, g.width/2)
                continue

            if xMode <= 4: # X-Manual
                #print(xMode, 'X-Manual', a.name)
                changed = False
                continue

        return changed

    def checkFixAnchorsYPosition(self, g):
        """Check/fix the y-position of the anchors named in AD.CENTERING_ANCHORS. It is assumed there that all anchors exist."""
        return self._fixGlyphAnchorsY(g)

    def _fixGlyphAnchorsY(self, g):
        """Fix the anchors X-position if it is different from where it should be according to the current mode.
        In sequence (or as defined by the mode in radio-buttons) trying to find the x-position of anchors:
        'Y-Base', 'Y-Metrics', 'Y-Manual'
        
        Strategies: 
        - If there are vertical metrics rules defined for each type of anchor, for the base or this type of glyph, then apply them.
        - If there is a base, then take the y position of the base anchors
        - If the vertical positions are too much inside the vertical bounds of the diacritics, then move up/down
        """
        changed = False
        f = g.font
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)
        yMode = self.getLib(g, 'Anchors', {}).get('Ymode')
        if yMode is None: # Lib was not complete, reinitialize. Maybe make this more generic later.
            self.setLib(g, 'Anchors', copy.copy(self.ANCHORS_DEFAULT_LIB_KEY))
            yMode = self.getLib(g, 'Anchors', {}).get('Ymode')

        for a in g.anchors:

            # H A C K S

            if a.name == AD._TOP and a.y < 100:
                a.y = f.info.xHeight - 16
                changed = True

            # Y - S C E N A R I O S

            if yMode == 0: # Y-Base
                #print(yMode, 'Y-Base', a.name')
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g)
                if baseGlyph is not None:
                    ba = self.getAnchor(baseGlyph, a.name)
                    if ba is not None:
                        changed = self._setAnchorXY(g, a, ba.x + dx, ba.y + dy, italicize=False) # Anchors from base are already italicized.
                continue

            if yMode in (0, 1): # Y-Diacritics or Y-Metrics
                #print(yMode, 'Y-Diacritics or Y-Metrics', a.name')

                done = None
                y = None
                # First guess, if there is a base, the use that as a start. Then scan through all the components, find their 
                # anchors and adjust the min/max y position of the anchor accordingly.
                if a.name == AD.TOP_:

                    hasDiacritics = False
                    overshoot = md.getAnchorOvershoot(g.name)
                    y = md.getHeight(g.name) - overshoot # This is what the masterData guess is, from info in the glyphSet parameters.
                    # First check if the bounding box of this glyph exceeds a certain height above the standard y
                    if g.bounds is not None and g.bounds[3] > y + 4 * overshoot:
                        y = g.bounds[3]

                    # Then check on the transformed vertical position of the anchors in the components
                    for component in g.components: # Now we're going to look at the glyph itself.
                        if component.baseGlyph not in f: # Checking, just to be sure
                            print(f'### _fixGlyphAnchorsY: Cannot find component glyph /{component.baseGlyph} in /{g.name}')
                            continue
                        
                        if not component.baseGlyph in AD.ACCENT_DATA: # Not an accent component, ignore.
                            continue
                        
                        hasDiacritics = True
                        tx, ty = component.transformation[-2:] # Get the transformation for this components, as offset for its anchor position
                        cg = f[component.baseGlyph]
                        ca = self.getAnchor(cg, a.name) # Get the equivalent anchor of the diacritics glyph
                        if ca is not None:
                            #print(f'### _fixGlyphAnchorsY: Cannot find anchor {a.name} in diacritics component {component.baseGlyph} in /{g.name}')
                            y = max(y, ca.y + ty) # Move the anchor up if there is extra space needed for the diacritics.

                    if gd.isUpper:
                        y -= 62 # Extra lower for capitals. @@@ TODO Make this into a more generic rule, independent from unitsPerEm  
                    elif hasDiacritics or g.name in AD.ACCENT_DATA:
                        y -= 140 # Closer together for stacking diacritics. @@@ TODO Make this into a more generic rule, independent from unitsPerEm

                elif a.name == AD.MIDDLE_:
                    y = md.getHeight2(g.name) # Just set to half-height.

                elif a.name == AD.BOTTOM_:

                    overshoot = md.getAnchorOvershoot(g.name)
                    y = md.getBaseline(g.name) + overshoot # This is what the masterData guess is, from info in the glyphSet parameters.
                    # First check if the bounding box of this glyph exceeds a certain height above the standard y
                    if g.bounds is not None and g.bounds[1] < y - 4 * overshoot:
                        y = g.bounds[1]

                    # Then check on the transformed vertical position of the anchors in the components
                    for component in g.components: # Now we're going to look at the glyph itself.
                        if component.baseGlyph not in f: # Checking, just to be sure
                            print(f'### _fixGlyphAnchorsY: Cannot find component glyph /{component.baseGlyph} in /{g.name}')
                            continue
                        
                        if not component.baseGlyph in AD.ACCENT_DATA: # Not an accent component, ignore.
                            continue
                        
                        tx, ty = component.transformation[-2:] # Get the transformation for this components, as offset for its anchor position
                        cg = f[component.baseGlyph]
                        ca = self.getAnchor(cg, a.name) # Get the equivalent anchor of the diacritics glyph
                        if ca is not None:
                            y = max(y, ca.y + ty) # Move the anchor down if there is extra space needed for the diacritics.

                    if g.name in AD.ACCENT_DATA:
                        y += 100 # Closer together for stacking diacritics. @@@ TODO Make this into a more generic rule, independent from unitsPerEm

                if y is not None:
                    changed |= self._setAnchorY(g, a, y) # Move the anchor to its new y position, also adjusting the x-position accordingly
                continue

            elif yMode == 2: # Y-Manual
                #print(yMode, 'Y-Manual', a.name')
                pass
        
        return changed

    def _setAnchorX(self, g, a, x, italicize=True):
        """Set the x-value of the anchor. If the italicize flag is on, then correct the x value by the italic angle in height.
        If the difference is smaller than 1 unit, the don't change anything. Otherwise print a message about the changed value.
        Answer the boolean flag if something did change.
        """
        changed = False
        if italicize:
            ax = int(round(self.italicX(g, x, a.y)))
        else:
            ax = x
        if abs(ax - a.x) >= 1: # Too different, correct it
            print(f'... Set /{g.name} anchor {a.name}.x from {int(round(a.x))} to {ax}')
            a.x = ax
            changed = True
        return changed

    def _setAnchorY(self, g, a, y, italicize=True):
        """Set the y-value of the anchor. If the italicize flag is on, then correct the x value by the relative change in height.
        If the difference is smaller than 1 unit, the don't change anything. Otherwise print a message about the changed value.
        Answer the boolean flag if something did change.
        """
        changed = False
        dy = y - a.y # Get relative y-position, so we know how much to move x too.
        if abs(dy) >= 1: # Too different, correct it
            print(f'... Set /{g.name} anchor {a.name}.y from {int(round(a.y))} to {y}')
            if italicize:
                a.x += int(round(self.italicX(g, 0, dy)))
            a.y = y
            changed = True
        return changed

    def _setAnchorXY(self, g, a, x, y, italicize=True):
        changed = False
        if italicize:
            ax = int(round(self.italicX(g, x, y)))
        else:
            ax = x
        if abs(ax - a.x) >= 1 or abs(y - a.y) >= 1:
            print(f'... Set /{g.name} anchor {a.name} from {(int(round(a.x)), int(round(a.y)))} to {(int(round(ax)), int(round(y)))}')
            a.x = ax
            a.y = y
            changed = True
        return changed

        #   E V E N T S

    def checkFixAllAnchors(self, f, glyphNames=None):
        """Check/fix all anchors in all glyphs of the font. if glyphNames is defined (single glyph name of list of glyph names),
        then only check on these glyphs instead of the whole font.
        First check on all glyphs that have no components. Then check on the glyphs that do have component, to avoid shifts in based glyphs.
        """
        fontChanged = False
        if glyphNames is None:
            if not isinstance(glyphNames, (list, tuple)):
                glyphNames = [glyphNames]
        else:
            glyphNames = sorted(f.keys())

        # First check on all glyphs without components.
        for gName in glyphNames:
            g = f[gName]
            if g.components:
                continue
            changed = self.checkFixAnchors(g)
            if changed:
                fontChanged = True
                g.changed()

        # Then check on glyphs with components.
        for gName in glyphNames:
            g = f[gName]
            if not g.components:
                continue
            changed = self.checkFixAnchors(g)
            if changed:
                fontChanged = True
                g.changed()

        return fontChanged

    def mouseMoveAnchors(self, g, x, y):
        """Update the guessed anchor positions, as they may be partially dependent on the anchors, if they are dragged."""
        self.updateGuessedAnchorPositions(g)

    def mouseDownAnchors(self, g, x, y):
        """There was a mouse down. Check if it was near a guessed anchor position."""
        print(x, y)
        for (ax, ay), (a, mx, my) in self.guessedAnchorPositions.items():
            if (ax - self.GUESSED_ANCHOR_MARKER_R <= x <= ax + self.GUESSED_ANCHOR_MARKER_R) and (ax - self.GUESSED_ANCHOR_MARKER_R <= x <= ax + self.GUESSED_ANCHOR_MARKER_R):
                if a.x != ax and a.y != ay:
                    a.x = ax
                    a.y = ay
                    print(f'... Set anchor {a.name} of /{g.name} to ({ax}, {ay}) by ({mx}, {my})')
                    break

    def checkFixAnchors(self, g):
        """Check and fix the anchors of g. First try to determine if the right number of anchors exists. There are
        2 ways (based on legacy data) to find the anchors that this glyph needs: as defined in the glyphData if named 
        anchors are part of the tables. But GlyphData already includes GLYPH_ANCHORS if no anchor attribute is defined.
        So, looking into G;lyphData is enough."""
        changed = False
        changed |= self.checkFixRequiredAnchors(g) # First make sure that they all exist.
        changed |= self.checkFixAnchorsXPosition(g) # Fix anchor X before adjusting Y position.
        changed |= self.checkFixAnchorsYPosition(g)
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
        requiredAnchorNames = gd.anchors  
        anchorNames = self.getAnchorNames(g)
        if requiredAnchorNames != anchorNames:
            # Remove obsolete anchors
            for a in g.anchors[:]: # Make a copy of the list, as it may be altered
                if a.name not in requiredAnchorNames:  
                    print(f'... Remove obsolete anchor "{a.name}" in /{g.name}')
                    g.removeAnchor(a)
                    changed = True

            # Add missing anchors
            for aName in requiredAnchorNames:
                if aName not in anchorNames:
                    print(f'... Add missing anchor "{aName}" in /{g.name}')
                    g.appendAnchor(name=aName, position=(0, 0)) # Just put at origin, position will be set in later checks.
                    changed = True 

            # Check on duplicate anchors
            done = [] # Remember which are already done, to detect duplicate anchors
            for a in g.anchors[:]: # Make a copy of the list, as it may be altered
                if a.name in done:
                    print(f'... Remove duplicate anchor "{a.name}" in /{g.name}')
                    g.removeAnchor(a)
                done.append(a.name)

        return changed

    def setGlyphAnchors(self, g):
        """Called when the EditWindow selected a new glyph. Try to  find previous anchor info in g.lib,
        about mode by which the current anchors are set and if they were manually moved."""
        self.updateGuessedAnchorPositions(g)

    def updateGuessedAnchorPositions(self, g):
        """Reset the guessed anchor positions for th is glyph."""
        self.guessedAnchorPositions = {}
        aIndex = 0
        for anchor in g.anchors:
            x, y = anchor.x, anchor.y

            for methodNameY in AD.AUTO_PLACED_ANCHORS_Y.get(anchor.name, []):
                if hasattr(self, methodNameY):
                    guessedY = getattr(self, methodNameY)(g, anchor)
                    if guessedY is None:
                        #print(f'### Could not guess Y-position by {methodNameY}')
                        continue
                    y = guessedY
                else:
                    print(f'### Missing {self.__class__.__name__}.{methodNameY}')
                    continue

                for methodNameX in AD.AUTO_PLACED_ANCHORS_X.get(anchor.name, []):
                    if hasattr(self, methodNameX):
                        guessedX = getattr(self, methodNameX)(g, anchor)
                        if guessedX is None:
                            #print(f'### Could not guess X-position by {methodNameX}')
                            continue
                        x = self.italicX(g, guessedX, y)
                    else:
                        print(f'### Missing {self.__class__.__name__}.{methodNameX}')
                        continue
        
                    x = int(round(x))
                    y = int(round(y))
                    if (x, y) in self.guessedAnchorPositions:
                        continue # Avoid double permuated labels)

                    if aIndex >= len(self.guessedAnchorPositions1): # Maybe there are too many guessed anchor positions to show. Skip the rest:
                        continue 

                    self.guessedAnchorPositions1[aIndex].setPosition((x - self.GUESSED_ANCHOR_MARKER_R, y - self.GUESSED_ANCHOR_MARKER_R))
                    self.guessedAnchorPositions1[aIndex].setVisible(True)
                    self.guessedAnchorPositions2[aIndex].setPosition((x - 2*self.GUESSED_ANCHOR_MARKER_R, y - 2*self.GUESSED_ANCHOR_MARKER_R))
                    self.guessedAnchorPositions2[aIndex].setVisible(True)
                    self.guessedAnchorLabels[aIndex].setText(f'@{anchor.name}\n{methodNameX.replace('guessAnchor', '')}: {x}\n{methodNameY.replace('guessAnchor', '')}: {y}')
                    tw, th = self.guessedAnchorLabels[aIndex].getSize()
                    #self.guessedAnchorLabels[aIndex].setPosition((x + self.GUESSED_ANCHOR_MARKER_R, y - 2*self.GUESSED_ANCHOR_MARKER_R - th/2))
                    self.guessedAnchorLabels[aIndex].setPosition((x, y - 2*self.GUESSED_ANCHOR_MARKER_R - th))
                    self.guessedAnchorLabels[aIndex].setVisible(True)
                    aIndex += 1
                    self.guessedAnchorPositions[(x, y)] = anchor, methodNameX, methodNameY

        for n in range(aIndex, len(self.guessedAnchorPositions1)):
            self.guessedAnchorPositions1[n].setVisible(False)
            self.guessedAnchorPositions2[n].setVisible(False)
            self.guessedAnchorLabels[n].setVisible(False)

    #   G U E S S I N G  A N C H O R  P O S I T I O N S

    # AUTO_PLACED_ANCHORS_Y = { # List of anchors that are responsive to auto-placement, with method names for their suggested positions.
    #     TOP_: ('guessAnchorBaseY', 'guessAnchorHeight', 'guessAnchorBoxTop', 'guessAnchorAscenderTop'),
    #     _TOP: ('guessAnchorBaseY', 'guessAnchorHeight', 'guessAnchorBoxTop', 'guessAnchorAscenderTop'),
    #     MIDDLE_: ('guessAnchorBaseY', 'guessAnchorMiddleY'),
    #     _MIDDLE: ('guessAnchorBaseY', 'guessAnchorMiddleY'),
    #     BOTTOM_: ('guessAnchorBaseY', 'guessAnchorBaseline', 'guessAnchorBoxBottom', 'guessAnchorDescenderBottom'), 
    #     _BOTTOM: ('guessAnchorBaseY', 'guessAnchorBaseline', 'guessAnchorBoxBottom', 'guessAnchorDescenderBottom'),
    #     DOT_: ('guessAnchorBaseY', 'guessAnchorMiddleY'),
    #     _DOT: ('guessAnchorBaseY', 'guessAnchorMiddleY'),
    #     VERT_: ('guessAnchorCapheight', 'guessAnchorAscender'),
    #     _VERT: ('guessAnchorCapheight', 'guessAnchorAscender'),
    #     TONOS_: ('guessAnchorCapheight', 'guessAnchorTonosY'),
    #     _TONOS: ('guessAnchorCapheight', 'guessAnchorTonosY'),
    #     OGONEK_: ('guessAnchorBaseY', 'guessAnchorBaseline', 'guessAnchorBoxBottom', 'guessAnchorOgonekY'), 
    #     _OGONEK: ('guessAnchorBaseY', 'guessAnchorBaseline', 'guessAnchorBoxBottom', 'guessAnchorOgonekY'),
    # }
    # AUTO_PLACED_ANCHORS_X = { # List of anchors that are responsive to auto-placement, with method names for their suggested positions.
    #     TOP_: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
    #     _TOP: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
    #     MIDDLE_: ('guessAnchorBaseX', 'guessAnchorMiddleX'),
    #     _MIDDLE: ('guessAnchorBaseX', 'guessAnchorMiddleX'),
    #     BOTTOM_: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
    #     _BOTTOM: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
    # }

    #   X

    def guessAnchorMiddleX(self, g, a):
        return g.width/2
        
    def guessAnchorBaseX(self, g, a):
        base = self.getBaseGlyph(g)
        if base is not None:
            baseAnchor = self.getAnchor(g, a.name)
            if baseAnchor is not None:
                return baseAnchor.x
        return None
        
    def guessAnchorCenterWidth(self, g, a):
        return g.width/2

    def guessAnchorCenterBox(self, g, a):
        """Answer the non-italized guess position of the anchor"""
        lm = g.angledLeftMargin
        rm = g.angledRightMargin
        if lm is not None:
            return lm + (g.width - rm - lm)/2
        return g.width/2
        
    #   Y

    def guessAnchorHeight(self, g, a):
        """Get the height of the anchor, from xHeight or capHeight."""
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        if gd.isLower:
            return md.getHeight(g.name) + md.xHeightAnchorOffsetY # Probably negative offset, so we can add.
        return md.getHeight(g.name) + md.capHeightAnchorOffsetY # Probably negative offset, so we can add.

    def guessAnchorBaseY(self, g, a):
        """Get the height of the anchor in the base glyph, if there is any. 
        This used to copy the vertical anchor position of the base."""
        base = self.getBaseGlyph(g)
        if base is not None:
            baseAnchor = self.getAnchor(g, a.name)
            if baseAnchor is not None:
                return baseAnchor.y
        return None

        #self.descenderAnchorOffsetY = descenderAnchorOffsetY
        #self.baselineAnchorOffsetY = baselineAnchorOffsetY
        #self.xHeightAnchorOffsetY = xHeightAnchorOffsetY
        #self.capHeightAnchorOffsetY = capHeightAnchorOffsetY # Optional vertical offset of cap-anhors or lower capital diacritics.
        #self.ascenderAnchorOffsetY = ascenderAnchorOffsetY

    def guessAnchorAscenderTop(self, g, a):
        """Get the height of the anchor from ascender."""
        md = self.getMasterData(g.font)
        return g.font.info.ascender + md.ascenderAnchorOffsetY # Probably negative value, so just add.

    def guessAnchorCapheight(self, g, a):
        """Get the height of the anchor, from capHeight."""
        md = self.getMasterData(g.font)
        return g.font.info.capHeight + md.capHeightAnchorOffsetY # Correct vertical position for lower diacritics.

    def guessAnchorBaseline(self, g, a):
        """Get the height of the anchor at baseline."""
        md = self.getMasterData(g.font)
        return md.baselineAnchorOffsetY # Probabyl positive value, moving the anchor up by the offset.

    def guessAnchorBoxTop(self, g, a):
        """Get the height of the anchor, from xHeight or capHeight."""
        md = self.getMasterData(g.font)
        return g.bounds[3] + md.boxTopAnchorOffsetY # Probably negative offset, so we can add.

    def guessAnchorMiddleY(self, g, a):
        md = self.getMasterData(g.font)
        h = md.getHeight(g.name)
        if h is None:
            return g.font.info.capHeight/2
        return h/2
        
    def guessAnchorBoxBottom(self, g, a):
        """Get the height of the anchor from xHeight or capHeight."""
        md = self.getMasterData(g.font)
        return g.bounds[1] + md.boxBottomAnchorOffsetY 

    def guessAnchorDescenderBottom(self, g, a):
        """Get the height of the anchor from descender position."""
        md = self.getMasterData(g.font)
        return g.font.info.descender + md.descenderAnchorOffsetY

    """
    # Table below is used as reference. It's defined in glyphSets/anchorData.py
    #
    AUTO_PLACED_ANCHORS_Y = { # List of anchors that are responsive to auto-placement, with method names for their suggested positions.
        TOP_: ('guessAnchorHeight', 'guessAnchorBaseY', 'guessAnchorBoxTop'),
        _TOP: ('guessAnchorHeight', 'guessAnchorBaseY'),
        MIDDLE_: ('guessAnchorMiddleY', 'guessAnchorBaseY'),
        _MIDDLE: ('guessAnchorMiddleY', 'guessAnchorBaseY'),
        BOTTOM_: ('guessAnchorBaseline', 'guessAnchorBaseY', 'guessAnchorBoxBottom'), 
        _BOTTOM: ('guessAnchorBaseline', 'guessAnchorBaseY'),
        DOT_: ('guessAnchorMiddleY', 'guessAnchorBaseY'),
        _DOT: ('guessAnchorMiddleY', 'guessAnchorBaseY'),
        VERT_: ('guessAnchorCapheight',),
        _VERT: ('guessAnchorCapheight',),
        TONOS_: ('guessAnchorCapheight',),
        _TONOS: ('guessAnchorCapheight',),
        OGONEK_: ('guessAnchorBaseline', 'guessAnchorBaseY', 'guessAnchorBoxBottom'), 
        _OGONEK: ('guessAnchorBaseline', 'guessAnchorBaseY'),
    }
    AUTO_PLACED_ANCHORS_X = { # List of anchors that are responsive to auto-placement, with method names for their suggested positions.
        TOP_: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
        _TOP: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
        MIDDLE_: ('guessAnchorMiddleX', 'guessAnchorBaseX'),
        _MIDDLE: ('guessAnchorMiddleX', 'guessAnchorBaseX'),
        BOTTOM_: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
        _BOTTOM: ('guessAnchorBaseX', 'guessAnchorCenterWidth', 'guessAnchorCenterBox'),
    }
    """
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
        """If there is a base glyph, then check if the anchors in the counterpart roman or italic glyph has the same position for the current font.
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
                if aName in anchors: # Only check on the existing anchors, don't make new ones, since roman and italic may not be compatible.
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

