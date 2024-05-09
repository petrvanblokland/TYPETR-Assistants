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
    MAX_GUESSED_ANCHORS = 30 # Probably not needing more than this amount of choices inside one glyph.
    
    ANCHOR_LABEL_FONT = 'Verdana'
    ANCHOR_LABEL_SIZE = 12
    GUESSED_ANCHOR_MARKER_R = 12
    SELECTED_ANCHOR_POSITION_COLOR = 1, 0.2, 0, 1 # Color of marker outlines if anchor is at selected guessed position
    #GUESSED_ANCHOR_POSITION_COLOR = 0, 0.5, 0, 1 # Color of marker outlines
    #GUESSED_ANCHOR_POSITION_COLOR_FILL = 0.1, 0.8, 0.7, 0.25
    #GUESSED_ANCHOR_POSITION_COLOR2 = 0, 0.25, 0, 1 # Color of labels
    #GUESSED_ANCHOR_POSITION_COLOR2_FILL = 0.1, 0.4, 0.35, 0.25

    def initMerzAnchors(self, container):
        """Initialize the Merz object for this assistant part.
        Note that the diacritics-cloud object are supported by the contours part.
        """
        self.guessedAnchorPosition = {} # Calculated if editor windows set glyph. Key is (x, y), value is (anchorName, methodNameX, methodNamey)

        self.anchorsDiacriticsCloud = [] # Storage of diacritics images
        for dIndex in range(self.MAX_DIACRITICS_CLOUD): # Max number of diacritics in a glyph. @@@ If too low, some diacritics don't show
            self.anchorsDiacriticsCloud.append(self.backgroundContainer.appendPathSublayer(
                name=f'diacritics-{dIndex}',
                position=(0, 0),
                fillColor=(0, 0, 0.5, 0.2),
                visible=False,
            ))
        self.guessedAnchorPositionsMarkers = [] # Storage of guessed anchor positions and their labels, showing as two concentric circles
        self.guessedAnchorLabels = []
        for aIndex in range(self.MAX_GUESSED_ANCHORS): # Max number of guessed anchor positions to show
            self.guessedAnchorPositionsMarkers.append(container.appendOvalSublayer(name=f'guessedAnchorPosition1{aIndex}',
                position=(0, 0),
                size=(self.GUESSED_ANCHOR_MARKER_R*2, self.GUESSED_ANCHOR_MARKER_R*2),
                fillColor=None,
                strokeColor=None, # Will be set to the color of the anchor type
                strokeWidth=2,
                visible=False,
            ))
            self.guessedAnchorLabels.append(container.appendTextBoxSublayer(name=f'guessedAnchorLabel{aIndex}',
                position=(0, 0),
                size=(400, 100),
                font=self.ANCHOR_LABEL_FONT,
                pointSize=self.ANCHOR_LABEL_SIZE,
                fillColor=None, # Will be set to the color of the anchor type
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

        c.w.autoAnchors = CheckBox((C0, y, CW, L), 'Auto anchors', value=True, sizeStyle='small')
        c.w.copyRomanAnchors = CheckBox((C1, y, CW, L), 'Copy roman-->italic', value=True, sizeStyle='small')
        c.w.fixAnchorsButton = Button((C2, y, CW, L), f'Fix anchors [{personalKey_A}{personalKey_a}]', callback=self.anchorsCallback)
        y += L
        c.w.showGuessedNames = CheckBox((C0, y, CW, L), 'Show guessed names', value=False, sizeStyle='small') # Show names+info of guessed positions.
        y += L + L/5
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8
        c.w.anchorEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.anchorEndLine2 = HorizontalLine((self.M, y, -self.M, 1)) # Double for slightly darker line
        #c.w.anchorEndLine.setBorderWidth(.5)
        y += L/5

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

    def XXXanchorXModesCallback(self, sender):
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

    def XXXanchorYModesCallback(self, sender):
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

    def XXXcheckFixAnchorsXPosition(self, g):
        """Check/fix the x-position of the anchors named in AD.CENTERING_ANCHORS. It is assumed there that all anchors exist."""
        return self._fixGlyphAnchorsX(g)

    def XXX_fixGlyphAnchorsX(self, g):
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

    def checkFixAnchorPositions(self, g):
        """Check/fix the y-position of the anchors named in AD.CENTERING_ANCHORS, according to which guessMethod names are defined in glyph.lib. 
        It is assumed there that required anchors exist."""
        changed = False#
        #return self._fixGlyphAnchorsY(g)
        #print(f'... Check-fix anchor positions of {g.name}')
        return changed

    def XXXcheckFixAnchorsYPosition(self, g):
        """Check/fix the y-position of the anchors named in AD.CENTERING_ANCHORS. It is assumed there that all anchors exist."""
        return self._fixGlyphAnchorsY(g)

    def XXX_fixGlyphAnchorsY(self, g):
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

    def XXX_setAnchorX(self, g, a, x, italicize=True):
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

    def XXX_setAnchorY(self, g, a, y, italicize=True):
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
        """Set the anchor position of it it different from (x, y)."""
        changed = False
        if italicize:
            ax = int(round(self.italicX(g, x, y)))
        else:
            ax = x
        if abs(ax - a.x) >= 1 or abs(y - a.y) >= 1:
            print(f'... Set /{g.name} anchor {a.name} from {(int(round(a.x)), int(round(a.y)))} to {(int(round(ax)), int(round(y)))})')
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

    ANCHORS_LIB_KEY = 'anchorsLib'
    ANCHORS_DEFAULT_LIB = dict(
        anchorMethodX={}, # Key is anchor name, value is method name for geussing the position. Values can be None or missing.
        anchorMethodY={},
    )

    def _getAnchorsGlyphLib(self, g):
        """Answer the anchor glyph lib as stored in glyph.lib. If it is not initialized then use a copy of self.ANCHORS_DEFAULT_LIB_KEY.
        If the content is not rightly formatted, then repair it. """
        anchorsGlyphLib = self.getLib(g, self.ANCHORS_LIB_KEY, copy.deepcopy(self.ANCHORS_DEFAULT_LIB))
        if not isinstance(anchorsGlyphLib, dict):
            anchorsGlyphLib = self.setLib(g, self.ANCHORS_LIB_KEY, copy.deepcopy(self.ANCHORS_DEFAULT_LIB))
        # Repair in case the lib is damage or has legacy initialization
        if not 'anchorMethodX' in anchorsGlyphLib or not isinstance(anchorsGlyphLib['anchorMethodX'], dict):
            anchorsGlyphLib['anchorMethodX'] = {}
        if not 'anchorMethodX' in anchorsGlyphLib or not isinstance(anchorsGlyphLib['anchorMethodY'], dict):
            anchorsGlyphLib['anchorMethodY'] = {}
        return anchorsGlyphLib

    def _getGuessMethodAnchorNames(self, g, anchorName):
        anchorGlyphLib = self._getAnchorsGlyphLib(g)
        return anchorsGlyphLib['anchorMethodX'].get(anchorName), anchorsGlyphLib['anchorMethodY'].get(anchorName)

    def _setGuessMethodAnchorNames(self, g, anchorName, methodNameX, methodNameY):
        """Store the methocNameX and methodNameY in glyph lib under the anchor name."""
        anchorsGlyphLib = self._getAnchorsGlyphLib(g)
        anchorsGlyphLib['anchorMethodX'][anchorName] = methodNameX
        anchorsGlyphLib['anchorMethodY'][anchorName] = methodNameY

    def mouseMoveAnchors(self, g, x, y):
        """Update the guessed anchor positions, as they may be partially dependent on the anchors, if they are dragged."""
        self.updateGuessedAnchorPositions(g)

    def mouseDownAnchors(self, g, x, y):
        """There was a mouse down. Check if it was near a guessed anchor position. If so, then store the guessed method name in the glyph.lib if not already there.
        Then store the method names in all family masters and checkSet the anchor position to that guessed value"""
        changed = False
        for (ax, ay), (anchorName, mx, my) in self.guessedAnchorPositions.items():
            if (ax - self.GUESSED_ANCHOR_MARKER_R/2 <= x <= ax + self.GUESSED_ANCHOR_MARKER_R/2) and (ay - self.GUESSED_ANCHOR_MARKER_R/2 <= y <= ay + self.GUESSED_ANCHOR_MARKER_R/2):
                # Set the guessed method name in this glyph for all open fonts.

                parentPath = self.filePath2ParentPath(g.font.path)
                for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
                    fullPath = self.path2FullPath(pth)
                    f = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                    if g.name in f:
                        gg = f[g.name]
                        gSrc = self._getAnchorTypeGlyph(gg) # Get the glyph that is model for the anchor types, if defined in glyphData.anchorTypeGlyphSrc, otherwise use /g itself.
                        # We can't use (ax, ay) here, because it's specific for the current glyph. 
                        # Calculating them for all glyphs separate for all open fonts is a bit expensive, but it's only done on mouse click. Let's see.
                        a = self.getAnchor(gg, anchorName)
                        if a is None:
                            print(f'### Missing anchor "{anchorName} in /{g.name} in {f.path.split("/")[-1]}')
                        # Get the guessed position of this anchor type. Possibly from the glyphData.anchorTypeGlyphSrc if defined. Otherwise from the gg glyph itself.
                        guessedY = getattr(self, my)(gSrc, a.name)
                        guessedX = self.italicX(gSrc, getattr(self, mx)(gSrc, a.name) or a.x, guessedY or a.y)
                        # Apply this guessed values from the selected anchor type onto the anchor positions of /gg
                        changed = self._setAnchorXY(gg, a, guessedX, guessedY, italicize=False) 
                        if changed:
                            gg.changed()

    def checkFixAnchors(self, g):
        """Check and fix the anchors of g. First try to determine if the right number of anchors exists. There are
        2 ways (based on legacy data) to find the anchors that this glyph needs: as defined in the glyphData if named 
        anchors are part of the tables. But GlyphData already includes GLYPH_ANCHORS if no anchor attribute is defined.
        So, looking into G;lyphData is enough."""
        changed = False
        changed |= self.checkFixRequiredAnchors(g) # First make sure that they all exist.
        changed |= self.checkFixAnchorPositions(g) # Fix anchor position depending on the selected method.
        changed |= self.checkFixRomanItalicAnchors(g)
        return changed

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

    def _getAnchorTypeGlyph(self, g):
        """Answer the glyph that is model for the anchorTypes of g. If glyphData.anchorTypeGlyphSrc is defined then use that glyph,
        e.g. as defined for /Uhorn using the anchor type positions of /U. Otherwise answer g as model."""
        assert g is not None
        gd = self.getGlyphData(g)
        if gd.anchorTypeGlyphSrc is not None: # There is a src glyph other than /g to copy guessed anchor positions from
            if gd.anchorTypeGlyphSrc in g.font: # Does the reference exist?
                return g.font[gd.anchorTypeGlyphSrc]
            # Print the error if the referenced glyph cannot be found
            print(f'### Cannot find anchorTypeGlyphSrc /{gd.anchorTypeGlyphSrc} for /{g.name}') 
        return g # By default use this glyph as its own source to guess possible anchor positions from

    def updateGuessedAnchorPositions(self, g):
        """Reset the guessed anchor positions for this glyph, e.g. after the glyphEditor set another glyph, or if spacing or bounding box changed.
        This method is not changing any position of the anchors it self."""
        c = self.getController()
        self.guessedAnchorPositions = {}
        gSrc = self._getAnchorTypeGlyph(g) # Get the glyph that is model for the anchor types, if defined in glyphData.anchorTypeGlyphSrc, otherwise use /g itself.
        aIndex = 0
        showNames = c.w.showGuessedNames.get()
        for anchor in gSrc.anchors: # Using the anchors here just as template to know which anchors belong in this glyph.
            if anchor.name not in AD.AUTO_PLACED_ANCHORS:
                continue # This type of anchor does not have guessing methods implemented

            #if anchor.name != 'top':
            #    continue

            for methodNameX, methodNameY in AD.AUTO_PLACED_ANCHORS[anchor.name]:
                if not hasattr(self, methodNameX):
                    print(f'### Missing anchor guessing method {methodNameX}')
                    continue
                if not hasattr(self, methodNameY):
                    print(f'### Missing anchor guessing method {methodNameY}')
                    continue
                x = getattr(self, methodNameX)(gSrc, anchor.name)
                y = getattr(self, methodNameY)(gSrc, anchor.name)
        
                if y is None: # If the guessing function answers None, then take the current position of the anchor
                    y = anchor.y
                if x is None: 
                    x = self.italicX(gSrc, anchor.x, y - anchor.y)
                else:
                    x = self.italicX(gSrc, x, y)


                if (x, y) in self.guessedAnchorPositions:
                    continue # Avoid double permutated labels)

                if aIndex >= len(self.guessedAnchorPositionsMarkers): # Maybe there are too many guessed anchor positions to show. Skip the rest:
                    continue 

                self.guessedAnchorPositionsMarkers[aIndex].setPosition((x - self.GUESSED_ANCHOR_MARKER_R, y - self.GUESSED_ANCHOR_MARKER_R))
                self.guessedAnchorPositionsMarkers[aIndex].setStrokeColor(AD.GUESS_ANCHOR_COLORS[anchor.name])
                self.guessedAnchorPositionsMarkers[aIndex].setVisible(True)

                self.guessedAnchorLabels[aIndex].setText(f'@{anchor.name}\n{methodNameX.replace("guessAnchor", "")}: {x}\n{methodNameY.replace("guessAnchor", "")}: {y}')
                tw, th = self.guessedAnchorLabels[aIndex].getSize()
                #self.guessedAnchorLabels[aIndex].setPosition((x + self.GUESSED_ANCHOR_MARKER_R, y - 2*self.GUESSED_ANCHOR_MARKER_R - th/2))
                self.guessedAnchorLabels[aIndex].setPosition((x, y - 2*self.GUESSED_ANCHOR_MARKER_R - th))
                self.guessedAnchorLabels[aIndex].setFillColor(AD.GUESS_ANCHOR_COLORS[anchor.name])
                self.guessedAnchorLabels[aIndex].setVisible(showNames) # SHowing depends on [x] Show guessed names
                aIndex += 1
                self.guessedAnchorPositions[(x, y)] = anchor.name, methodNameX, methodNameY

        for n in range(aIndex, len(self.guessedAnchorPositionsMarkers)):
            self.guessedAnchorPositionsMarkers[n].setVisible(False)
            self.guessedAnchorLabels[n].setVisible(False)

    #   G U E S S I N G  A N C H O R  P O S I T I O N S

    #   X

    def guessAnchorMiddleX(self, g, anchorName):
        return g.width/2
        
    def guessAnchorBaseX(self, g, anchorName):
        base = self.getBaseGlyph(g)
        if base is not None:
            baseAnchor = self.getAnchor(g, anchorName)
            if baseAnchor is not None:
                return baseAnchor.x
        return None
        
    def guessAnchorCenterWidth(self, g, anchorName):
        return g.width/2

    def guessAnchorBoxCenterX(self, g, anchorName):
        """Answer the non-italized guess position of the anchor"""
        lm = g.angledLeftMargin
        rm = g.angledRightMargin
        if lm is not None:
            return lm + (g.width - rm - lm)/2
        return g.width/2

    def guessAnchorOgonekX(self, g, anchorName):
        """Dummy method, as the horizontal position of the ogonek is hard to guess. 
        Answering None makes the current (manual) position of a.x be used as best guess.
        This method can be redefined by inheriting assistant classes if projects have a better guessing method."""
        return None

    def guessAnchorDotX(self, g, anchorName):
        """Dummy method, as the horizontal position of the dot is hard to guess. 
        Answering None makes the current (manual) position of a.x be used as best guess.
        This method can be redefined by inheriting assistant classes if projects have a better guessing method."""
        return None

    def guessAnchorVertX(self, g, anchorName):
        """Dummy method, as the horizontal position of the vert anchor is hard to guess. 
        Answering None makes the current (manual) position of a.x be used as best guess.
        This method can be redefined by inheriting assistant classes if projects have a better guessing method."""
        return None

    def guessAnchorX(self, g, anchorName):
        """Answering None makes the current (manual) position of a.x be used as best guess.
        This method can be redefined by inheriting assistant classes if projects have a better guessing method."""
        return None

    #   Y

    def guessAnchorHeight(self, g, anchorName):
        """Get the height of the anchor, from xHeight or capHeight."""
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        if gd.isLower:
            return md.getHeight(g.name) + md.xHeightAnchorOffsetY # Probably negative offset, so we can add.
        return int(round(md.getHeight(g.name) + md.capHeightAnchorOffsetY)) # Probably negative offset, so we can add.

    def guessAnchorBaseY(self, g, anchorName):
        """Get the height of the anchor in the base glyph, if there is any. 
        This used to copy the vertical anchor position of the base."""
        base = self.getBaseGlyph(g)
        if base is not None:
            baseAnchor = self.getAnchor(g, anchorName)
            if baseAnchor is not None:
                return int(round(baseAnchor.y))
        return None

    def guessAnchorAscender(self, g, anchorName):
        """Get the height of the anchor from ascender."""
        md = self.getMasterData(g.font)
        return g.font.info.ascender + md.ascenderAnchorOffsetY # Probably negative value, so just add.

    def guessAnchorCapheight(self, g, anchorName):
        """Get the height of the anchor, from capHeight."""
        md = self.getMasterData(g.font)
        return g.font.info.capHeight + md.capHeightAnchorOffsetY # Correct vertical position for lower diacritics.

    def guessAnchorBaseline(self, g, anchorName):
        """Get the height of the anchor at baseline."""
        md = self.getMasterData(g.font)
        return md.baselineAnchorOffsetY # Probabyl positive value, moving the anchor up by the offset.

    def guessAnchorBoxTop(self, g, anchorName):
        """Get the height of the anchor, from xHeight or capHeight."""
        md = self.getMasterData(g.font)
        return int(round(g.bounds[3])) + md.boxTopAnchorOffsetY # Probably negative offset, so we can add.

    def guessAnchorMiddleY(self, g, anchorName):
        md = self.getMasterData(g.font)
        h = md.getHeight(g.name)
        if h is None:
            return g.font.info.capHeight/2
        return int(round(h/2))

    def guessAnchorBoxBottom(self, g, anchorName):
        """Get the height of the anchor from xHeight or capHeight."""
        md = self.getMasterData(g.font)
        return int(round(g.bounds[1] + md.boxBottomAnchorOffsetY)) 

    def guessAnchorDescender(self, g, anchorName):
        """Get the height of the anchor from descender position."""
        md = self.getMasterData(g.font)
        return g.font.info.descender + md.descenderAnchorOffsetY

    def guessAnchorOgonekY(self, g, anchorName):
        """Answer the vertical guessed ogonek position for this anchor"""
        md = self.getMasterData(g.font)
        return md.ogonekAnchorOffsetY # Probably positive value, moving the anchor up by the offset.

    def guessAnchorVertY(self, g, anchorName):
        """Get the height of the anchor, from capHeight."""
        md = self.getMasterData(g.font)
        return g.font.info.capHeight + md.baselineAnchorOffsetY # Re=use this value, same construction above capHeight. Correct vertical position for lower diacritics.

    def guessAnchorVertAscenderY(self, g, anchorName):
        """Get the height of the anchor, from capHeight."""
        md = self.getMasterData(g.font)
        return g.font.info.ascender + md.baselineAnchorOffsetY # Re=use this value, same construction above capHeight. Correct vertical position for lower diacritics.

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


