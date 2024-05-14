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
#   - Anchors that refer to a base, get their (relative) horizontal (slanted) positions from it, with the base component offset.
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

    ANCHOR_SELECT_DISTANCE = 48 # Within radius of this, an anchor gets selected by option-shift-click

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

        # Make sure to check/fix the current glyph
        if c.w.autoAnchors.get():
            changed |= self.checkFixAnchors(g)

        # Update the guessed positions, in case one of the X/Y positions depends on the current positions of an axis
        self.updateGuessedAnchorPositions(g)

        return changed

    def buildAnchors(self, y):
        """Register key stroke [a] to sync anchor positions"""
        personalKey_A = self.registerKeyStroke('A', 'anchorsGlyphKey') # Check/fix all glyphs in the current font and/or all masters
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
        c.w.checkFixAllMasterAnchors = CheckBox((C1, y, CW, L), 'Fix all masters', value=True, sizeStyle='small')
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

    def checkFixAnchorPositions(self, g):
        """Check/fix the y-position of the anchors named in AD.CENTERING_ANCHORS, according to which guessMethod names are defined in glyph.lib. 
        It is assumed there that required anchors exist."""
        changed = False#
        #return self._fixGlyphAnchorsY(g)
        #print(f'... Check-fix anchor positions of {g.name}')
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

    def mouseMoveAnchors(self, g, x, y, event):
        """Update the guessed anchor positions, as they may be partially dependent on the anchors, if they are dragged."""
        #self.autoCheckFixAnchorPositions(g)
        #self.updateGuessedAnchorPositions(g)
        pass

    def mouseDownAnchors(self, g, x, y, event):
        """There was a mouse down. Check if it was near a guessed anchor position. If so, then store the guessed method name in the glyph.lib if not already there.
        Then store the method names in all family masters and checkSet the anchor position to that guessed value"""
        #controlDown = event['controlDown'] # Cannot use control-key, as it pops up a RoboFont menu
        shiftDown = event['shiftDown']
        commandDown = event['commandDown']
        optionDown = event['optionDown']
        capLock = event['capLockDown']

        if shiftDown and optionDown and commandDown: # All anchors of all masters
            for a in g.anchors: # All anchrs that are within reach
                parentPath = self.filePath2ParentPath(g.font.path) 
                for pth in sorted(self.getUfoPaths(parentPath)): # Do all masters in the same way for this anchor
                    fullPath = self.path2FullPath(pth)
                    ff = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                    if g.name in ff:
                        gg = ff[g.name]
                        gg.prepareUndo()
                        for aa in gg.anchors:
                            if aa.name == a.name:
                                print(f'... autoCheckFixAnchorPosition: {pth} Anchor {a.name}')
                                self.autoCheckFixAnchorPosition(gg, aa)
                    
        elif shiftDown and commandDown: # All anchors of all masters
            for a in g.anchors: # All anchrs that are within reach
                if self.distance(a.x, a.y, x, y) < self.ANCHOR_SELECT_DISTANCE:
                    parentPath = self.filePath2ParentPath(g.font.path) 
                    for pth in sorted(self.getUfoPaths(parentPath)): # Do all masters in the same way for this anchor
                        fullPath = self.path2FullPath(pth)
                        ff = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                        if g.name in ff:
                            gg = ff[g.name]
                            gg.prepareUndo()
                            for aa in gg.anchors:
                                if aa.name == a.name:
                                    print(f'... autoCheckFixAnchorPosition: {pth} Anchor {a.name}')
                                    self.autoCheckFixAnchorPosition(gg, aa)
                    
        elif shiftDown and optionDown: # Only do a single anchor in the current glyph if click is within range.
            for a in g.anchors:
                if self.distance(a.x, a.y, x, y) < self.ANCHOR_SELECT_DISTANCE:
                    self.autoCheckFixAnchorPosition(g, a)
        return

    def ZZZZZ(self):
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
                        self.checkFixAnchors(gg) # Make sure the right amount of anchors exists.
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

    def autoCheckFixAnchorPosition(self, g, a):
        changed = False
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)

        ax = ay = None
        if a.name == AD.TOP_:
            # Trying to guess vertical
            baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base, just copy the vertical anchor position 
            if baseGlyph is not None:
                baseAnchor = self.getAnchor(baseGlyph, a.name)
                if baseAnchor is not None:
                    ay = baseAnchor.y + dy # Vertical position of the base anchor + component offset.
            if ay is None: # No base component, get the height from xHeight or capHeight
                if gd.isLower: # Default position below xHeight or capHeight
                    ay = g.font.info.xHeight + md.xHeightAnchorOffsetY # Likely to ba a negative number
                else:
                    ay = g.font.info.capHeight + md.capHeightAnchorOffsetY # Likely to ba a negative number
            # In case the a.y now is below the bounding box, then lift the anchor to fit the top of the bounding box
            #print(g.bounds, a.x, a.y, ax, ay, h, g.bounds[3], md.baseOvershoot, g.bounds[3] + 2*md.baseOvershoot, h < g.bounds[3] + 2*md.baseOvershoot)
            if gd.isLower: # Default position below xHeight or capHeight
                if md.baseDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                    ay = g.bounds[3] + md.boxTopAnchorOffsetY
            else:
                if md.capDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                    ay = g.bounds[3] + md.boxTopAnchorOffsetY

            # Try to guess horizontal
            if baseGlyph is not None: # In case there is a base
                baseAnchor = self.getAnchor(baseGlyph, a.name)
                if baseAnchor is not None:
                    ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)
            else: # Center on width by default
                ax = self.italicX(g, g.width/2, ay)

        elif a.name == AD._TOP:
            ay = g.font.info.xHeight + md.xHeightAnchorOffsetY # Likely to ba a negative number
            ax = self.italicX(g, 0, ay) # All glyph that contain _top are supposed to have width = 0

        elif a.name == AD.MIDDLE_:
            # Trying to guess vertical
            if gd.isLower: # Default position below xHeight or capHeight
                ay = g.font.info.xHeight/2
            else:
                ay = g.font.info.capHeight/2
            # Try to guess horizontal
            baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base 
            if baseGlyph is not None:
                print(baseGlyph.name, dx, dy)
                baseAnchor = self.getAnchor(baseGlyph, a.name)
                if baseAnchor is not None:
                    ax = baseAnchor.x + dx
            else: # Center on width by default
                ax = self.italicX(g, g.width/2, ay)

        elif a.name == AD._MIDDLE:
            ay = g.font.info.xHeight/2
            ax = self.italicX(g, 0, ay) # All glyph that contain _top are supposed to have width = 0
        
        elif a.name == AD.BOTTOM_: # Try to guess bottom position
            # Trying to guess vertical
            # Default position below xHeight or capHeight
            ay = md.baseOvershoot
            # In case the a.y now is above the bounding box, then lift the anchor to fit the top of the bounding box
            if ay < g.bounds[1] - 2*md.baseOvershoot:
                ay = g.bounds[1]

            # Try to guess horizontal
            baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base 
            if baseGlyph is not None:
                baseAnchor = self.getAnchor(baseGlyph, a.name)
                if baseAnchor is not None:
                    ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)
            else: # Center in width by default
                ax = self.italicX(g, g.width/2, ay)
        
        elif a.name == AD._BOTTOM:
            ay = md.baseOvershoot
            ax = self.italicX(g, 0, ay) # All glyph that contain _bottom are supposed to have width = 0

        elif a.name == AD.OGONEK_: # Try to guess bottom position
            # Trying to guess vertical
            ay = md.ogonekAnchorOffsetY

        elif a.name == AD.TONOS_: # Try to guess tonos position only for capitals
            # Trying to guess vertical
            ay = g.font.info.capHeight # Likely to ba a negative number
            ax = self.italicX(g, g.angledLeftMargin/2, ay) # Right aligned, halfway left margin

        elif a.name == AD._TONOS: # Try to guess _tonos position
            # Trying to guess vertical
            ay = g.font.info.capHeight # Likely to ba a negative number
            ax = self.italicX(g, 0, ay) # Right aligned, halfway left margin

        if ax is not None and ax != a.x:
            a.x = ax
            changed = True
        if ay is not None and ay != a.y:
            a.y = ay
            changed = True
        return changed

    def updateGuessedAnchorPositions(self, g):
        """Reset the guessed anchor positions for this glyph, e.g. after the glyphEditor set another glyph, or if spacing or bounding box changed.
        This method is not changing any position of the anchors it self."""
        c = self.getController()
        self.guessedAnchorPositions = {}
        # Get the glyph that is model for the anchor types, if defined in glyphData.anchorTypeGlyphSrc, otherwise use /g itself.
        gSrc = self._getAnchorTypeGlyph(g) 
        aIndex = 0
        showNames = c.w.showGuessedNames.get()
        for anchor in gSrc.anchors: # Using the anchors here just as template to know which anchors belong in this glyph.
            continue # @@@@@@

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
        
    def guessAnchorZeroWidthX(self, g, anchorName):
        if g.width == 0:
            return 0
        return None
        
    def guessAnchorBaseX(self, g, anchorName):
        base, (dx, dy) = self.getBaseGlyphOffset(g)
        if base is not None:
            baseAnchor = self.getAnchor(g, anchorName)
            if baseAnchor is not None:
                return baseAnchor.x + dx
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

    def guessAnchorTonosX(self, g, anchorName):
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
        base, (dx, dy) = self.getBaseGlyphOffset(g)
        if base is not None:
            baseAnchor = self.getAnchor(g, anchorName)
            if baseAnchor is not None:
                return int(round(baseAnchor.y + dy))
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

        # If checkbox is set, then check/fix the anchors in all masters.
        if self.getController().w.checkFixAllMasterAnchors.get():
            fonts = []
            parentPath = self.filePath2ParentPath(g.font.path)
            for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
                fullPath = self.path2FullPath(pth)
                f = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                fonts.append(f)
        else:
            fonts = [g.font]

        for f in fonts:
            if g.name in f:
                if c.lower() == c: # Just the current glyph
                    glyphs = [f[g.name]]
                else:
                    glyphs = f
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


