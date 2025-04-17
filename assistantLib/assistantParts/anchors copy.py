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
#   - Otherwise check if there is a set of predefined vertical positions for each anchor type
#   - The assistant decides on an initial strategy, but then the user can alter that.
#   - If an anchor was dragged, this is stored in the glyph.lib, so it will not change by the assistant anymore.
#   - Unless that flag is cleared.
#
import sys, copy
from math import *
from vanilla import *

GGGG = 'Abreveacute'

try:
    from mojo.roboFont import AllFonts #
except ImportError: # In case not running inside RoboFont
    pass

VERBOSE = False
#
# Add paths to libs in sibling repositories
# It implices that the TYPETR-Assistants repository should live in the same directory as the project repositories.
# This way no installation of libraries is required. Easier to update for new versions.
#
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
        if gd is None:
            print(f'### No GlyphData found for /{g.name}')
        else:
            for a in g.anchors:
                for dName in AD.EXAMPLE_DIACRITICS.get(a.name, []):
                    if not gd.isLower and dName + '.uc' in g.font:
                        dName += '.uc' # Show capital diacritics version
                    if dName in g.font:
                        dg = g.font[dName]
                        dAnchor = self.getAnchor(dg, AD.CONNECTED_ANCHORS[a.name])
                        if dAnchor is not None:
                            diacriticsLayer = self.anchorsDiacriticsCloud[dIndex] # Get layer for this diacritics glyph
                            diacriticsPath = dg.getRepresentation("merz.CGPath") 
                            diacriticsLayer.setPath(diacriticsPath)
                            ax = a.x - dAnchor.x
                            ay = a.y - dAnchor.y
                            #print(dName, ax, ay, a.name, a.x, a.y, dAnchor.name, dAnchor.x, dAnchor.y)
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
        if c.w.autoAnchors.get(): # @@@ Hack to update all glyphs
            changed = self.checkFixAnchors(g)

        # Update the guessed positions, in case one of the X/Y positions depends on the current positions of an axis
        #self.updateGuessedAnchorPositions(g)

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
        c.w.checkFixAllMasterAnchors = CheckBox((C1, y, CW, L), 'Fix all open masters', value=True, sizeStyle='small')
        y += L + L/5
        # Line color is crashing RoboFont
        #y += L # Closing line for the part UI
        #c.w.anchorsLine = HorizontalLine((self.M, y+4, -self.M, 0))
        #y += 8

        # Sliders for manual overwriting of anchor positions. These values are glyph specific and get stored in glyph.lib
        c.w.anchorTopReset = Button((C0, y-5, CW, L), 'Reset Top', sizeStyle='small', callback=self.anchorsTopResetCallback)
        c.w.topAnchorXOffsetSlider = Slider((C1, y-5, CW, L), minValue=-self.MAX_OVERLAY_OFFSET_SLIDER, maxValue=self.MAX_OVERLAY_OFFSET_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateTopAnchorSliderCallback)
        c.w.topAnchorYOffsetSlider = Slider((C2, y-5, CW, L), minValue=-self.MAX_OVERLAY_OFFSET_SLIDER, maxValue=self.MAX_OVERLAY_OFFSET_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateTopAnchorSliderCallback)
        y += L
        c.w.anchorMiddleReset = Button((C0, y-5, CW, L), 'Reset Middle', sizeStyle='small', callback=self.anchorsMiddleResetCallback)
        c.w.middleAnchorXOffsetSlider = Slider((C1, y-5, CW, L), minValue=-self.MAX_OVERLAY_OFFSET_SLIDER, maxValue=self.MAX_OVERLAY_OFFSET_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateMiddleAnchorSliderCallback)
        c.w.middleAnchorYOffsetSlider = Slider((C2, y-5, CW, L), minValue=-self.MAX_OVERLAY_OFFSET_SLIDER, maxValue=self.MAX_OVERLAY_OFFSET_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateMiddleAnchorSliderCallback)
        y += L
        c.w.anchorBottomReset = Button((C0, y-5, CW, L), 'Reset Bottom', sizeStyle='small', callback=self.anchorsBottomResetCallback)
        c.w.bottomAnchorXOffsetSlider = Slider((C1, y-5, CW, L), minValue=-self.MAX_OVERLAY_OFFSET_SLIDER, maxValue=self.MAX_OVERLAY_OFFSET_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateBottomAnchorSliderCallback)
        c.w.bottomAnchorYOffsetSlider = Slider((C2, y-5, CW, L), minValue=-self.MAX_OVERLAY_OFFSET_SLIDER, maxValue=self.MAX_OVERLAY_OFFSET_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateBottomAnchorSliderCallback)
        y += L

        c.w.anchorEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.anchorEndLine2 = HorizontalLine((self.M, y, -self.M, 1)) # Double for slightly darker line
        #c.w.anchorEndLine.setBorderWidth(.5)
        y += L/5

        return y

    # Labels for (x, y) offset for anchors, stored in glyph.lib
    ANCHOR_TOP_OFFSET = 'anchorTopOffset'
    ANCHOR_MIDDLE_OFFSET = 'anchorMiddleOffset'
    ANCHOR_BOTTOM_OFFSET = 'anchorBottomOffset'
    MAX_OVERLAY_OFFSET_SLIDER = 200

    def anchorsTopResetCallback(self, sender):
        g = self.getCurrentGlyph()
        self.setLib(g, self.ANCHOR_TOP_OFFSET, (0, 0))
        c = self.getController()
        c.w.topAnchorXOffsetSlider.set(0)
        c.w.topAnchorYOffsetSlider.set(0)
        g.changed()

    def updateTopAnchorSliderCallback(self, sender):
        """Update the position of the anchors, with the setting of the offset sliders and store the value in glyph.lib"""
        g = self.getCurrentGlyph()
        x, y = self.getLib(g, self.ANCHOR_TOP_OFFSET, (0, 0))
        ox, oy = int(round(self.w.topAnchorXOffsetSlider.get())), int(round(self.w.topAnchorYOffsetSlider.get()))
        changed = False
        if x != ox:
            x = ox
            changed = True
        if y != oy:
            y = oy
            changed = True
        if changed:
            #print('Top', x, y, ox, oy)
            self.setLib(g, self.ANCHOR_TOP_OFFSET, (x, y))
            g.changed()

    def anchorsMiddleResetCallback(self, sender):
        g = self.getCurrentGlyph()
        self.setLib(g, self.ANCHOR_MIDDLE_OFFSET, (0, 0))
        c = self.getController()
        c.w.middleAnchorXOffsetSlider.set(0)
        c.w.middleAnchorYOffsetSlider.set(0)
        g.changed()

    def updateMiddleAnchorSliderCallback(self, sender):
        """Update the position of the anchors, with the setting of the offset sliders and store the value in glyph.lib"""
        g = self.getCurrentGlyph()
        x, y = self.getLib(g, self.ANCHOR_MIDDLE_OFFSET, (0, 0))
        ox, oy = int(round(self.w.middleAnchorXOffsetSlider.get())), int(round(self.w.middleAnchorYOffsetSlider.get()))
        changed = False
        if x != ox:
            x = ox
            changed = True
        if y != oy:
            y = oy
            changed = True
        if changed:
            #print('Middle', x, y, ox, oy)
            self.setLib(g, self.ANCHOR_MIDDLE_OFFSET, (x, y))
            g.changed()

    def anchorsBottomResetCallback(self, sender):
        g = self.getCurrentGlyph()
        self.setLib(g, self.ANCHOR_BOTTOM_OFFSET, (0, 0))
        c = self.getController()
        c.w.bottomAnchorXOffsetSlider.set(0)
        c.w.bottomAnchorYOffsetSlider.set(0)
        g.changed()
        
    def updateBottomAnchorSliderCallback(self, sender):
        """Update the position of the anchors, with the setting of the offset sliders and store the value in glyph.lib"""
        g = self.getCurrentGlyph()
        x, y = self.getLib(g, self.ANCHOR_BOTTOM_OFFSET, (0, 0))
        ox, oy = int(round(self.w.bottomAnchorXOffsetSlider.get())), int(round(self.w.bottomAnchorYOffsetSlider.get()))
        changed = False
        if x != ox:
            x = ox
            changed = True
        if y != oy:
            y = oy
            changed = True
        if changed:
            #print('Bottom', x, y, ox, oy)
            self.setLib(g, self.ANCHOR_BOTTOM_OFFSET, (x, y))
            g.changed()
        
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
        It is assumed there that the required anchors exist."""
        changed = False
        gd = self.getGlyphData(g)
        if gd is None:
            print(f'### checkFixAnchorPositions: Cannot find GlyphData for /{g.name}')
            return changed

        if gd.autoFixAnchorPositionX or gd.autoFixAnchorPositionY:
            for a in g.anchors:
                changed |= self.autoCheckFixAnchorPosition(g, gd, a)
            if changed:
                print(f'... Check-fix anchor positions of {g.name} in {g.font.path.split('/')[-1]}')
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
        print(f'... Check-fixing master {f.path.split('/')[-1]}')
        fontChanged = False
        if glyphNames is not None:
            if not isinstance(glyphNames, (list, tuple)):
                glyphNames = [glyphNames]
        else:
            glyphNames = sorted(f.keys())

        # First check on all glyphs without components.
        for gName in glyphNames:
            g = f[gName]
            if g.contours and not g.components:
                changed = self.checkFixAnchors(g)
                if changed:
                    g.changed()
                    fontChanged = True

        # Then check on glyphs with components.
        for gName in glyphNames:
            g = f[gName]
            if g.components and not g.contours:
                changed = self.checkFixAnchors(g)
                if changed:
                    g.changed()
                    fontChanged = True

        # Then check on hybrid glyphs with components and contours.
        for gName in glyphNames:
            g = f[gName]
            if g.contours and g.components:
                changed = self.checkFixAnchors(g)
                if changed:
                    fontChanged = True
                    g.changed()

        return fontChanged

    ANCHORS_LIB_KEY = 'anchorsLib'
    ANCHORS_DEFAULT_LIB = dict(
        anchorMethodX={}, # Key is anchor name, value is method name for guessing the position. Values can be None or missing.
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

        gd = self.getGlyphData(g)
        if gd is None:
            print(f'### mouseDownAnchors: Cannot find GlyphData for /{g.name}')
            return

        shiftDown = event['shiftDown']
        commandDown = event['commandDown']
        optionDown = event['optionDown']
        capLock = event['capLockDown']

        if False and shiftDown and optionDown and commandDown: # All anchors of all masters 
            # @@@@@@@@@ Disabled, could be checkbox choice.
            for a in g.anchors: # All anchors, not checking on nearness
                parentPath = self.filePath2ParentPath(g.font.path) 
                for pth in sorted(self.getUfoPaths(parentPath)): # Do all masters in the same way for this anchor
                    fullPath = self.path2FullPath(pth)
                    ff = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                    if g.name in ff:
                        gg = ff[g.name]
                        gg.prepareUndo()
                        self.checkFixRequiredAnchors(gg) # First make sure that they all exist.
                        for aa in gg.anchors:
                            if aa.name == a.name:
                                print(f'... autoCheckFixAnchorPosition: {pth} Anchor {a.name}')
                                self.autoCheckFixAnchorPosition(gg, gd, aa) # GlyphData is supposed to be equal for all glyphs in the family
                    
        elif shiftDown and commandDown: # All anchors of all masters with name of anchors near mouse click
            for a in g.anchors: # All anchors that are within reach
                if self.distance(a.x, a.y, x, y) < self.ANCHOR_SELECT_DISTANCE:
                    parentPath = self.filePath2ParentPath(g.font.path) 
                    for pth in sorted(self.getUfoPaths(parentPath)): # Do all masters in the same way for this anchor
                        fullPath = self.path2FullPath(pth)
                        ff = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                        if g.name in ff:
                            gg = ff[g.name]
                            gg.prepareUndo()
                            self.checkFixRequiredAnchors(gg) # First make sure that they all exist.
                            for aa in gg.anchors:
                                if aa.name == a.name:
                                    print(f'... autoCheckFixAnchorPosition: {pth} Anchor {a.name}')
                                    self.autoCheckFixAnchorPosition(gg, gd, aa) # GlyphData is supposed to be equal for all glyphs in the family
                            gg.changed()
                    
        elif shiftDown and optionDown: # Only do a single anchor in the current glyph if click is within range.
            self.checkFixRequiredAnchors(g) # First make sure that they all exist.
            for a in g.anchors:
                if self.distance(a.x, a.y, x, y) < self.ANCHOR_SELECT_DISTANCE:
                    self.autoCheckFixAnchorPosition(g, gd, a)
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
                        gSrc = self._getAnchorTypeGlyph(gg) # Get the glyph that is model for the anchor types, if defined in glyphData.anchorGlyphSrc, otherwise use /g itself.
                        # We can't use (ax, ay) here, because it's specific for the current glyph. 
                        # Calculating them for all glyphs separate for all open fonts is a bit expensive, but it's only done on mouse click. Let's see.
                        a = self.getAnchor(gg, anchorName)
                        if a is None:
                            print(f'### Missing anchor "{anchorName} in /{g.name} in {f.path.split("/")[-1]}')
                        # Get the guessed position of this anchor type. Possibly from the glyphData.anchorGlyphSrc if defined. Otherwise from the gg glyph itself.
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
        if g.name == GGGG:
            print('checkFixAnchors', g, id(g.font))
        return self.setGlyphAnchors(g)

        changed = False
        changed |= self.checkFixRequiredAnchors(g) # First make sure that they all exist.
        changed |= self.checkFixAnchorPositions(g) # Fix anchor position depending on the selected method.
        changed |= self.checkFixRomanItalicAnchors(g)
        return changed

    def checkFixRequiredAnchors(self, g):
        """Check/fix the required anchors if they don't all exist or if there are too many."""
        changed = False
        gd = self.getGlyphData(g)
        if gd is None:
            print(f'### checkFixRequiredAnchors: Cannot find GlyphData for /{g.name}')
            return False

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

    def setGlyphAnchors(self, g, loop=True):
        """Called when the EditWindow selected a new glyph. Try to find previous anchor info in g.lib,
        about mode by which the current anchors are set and if they were manually moved."""
        if g.name == GGGG:
            print('setGlyphAnchors', g, g.font.path.split('/')[-1], id(g.font))
        if loop:
            for gg in g.font:
                f = self.getCurrentFont()
                self.setGlyphAnchors(f[gg.name], False)

        changed = self.checkFixRequiredAnchors(g) # First make sure that they all exist.
        gd = self.getGlyphData(g)
        if gd is None:
            print(f'### setGlyphAnchors: Cannot find GlyphData for /{g.name}')

        elif gd.autoFixAnchorPositionX or gd.autoFixAnchorPositionY:
            c = self.getController()

            for a in g.anchors:
                # Set the offset sliders from the current values in glyph.lib
                if a.name == AD.TOP_:
                    ox, oy = self.getLib(g, self.ANCHOR_TOP_OFFSET, (0, 0))
                    c.w.topAnchorXOffsetSlider.set(ox)
                    c.w.topAnchorYOffsetSlider.set(oy)
                elif a.name == AD.MIDDLE_:
                    ox, oy = self.getLib(g, self.ANCHOR_MIDDLE_OFFSET, (0, 0))
                    c.w.middleAnchorXOffsetSlider.set(ox)
                    c.w.middleAnchorYOffsetSlider.set(oy)
                elif a.name == AD.BOTTOM_:
                    ox, oy = self.getLib(g, self.ANCHOR_BOTTOM_OFFSET, (0, 0))
                    c.w.bottomAnchorXOffsetSlider.set(ox)
                    c.w.bottomAnchorYOffsetSlider.set(oy)

                changed |= self.autoCheckFixAnchorPosition(g, gd, a)
        return changed

    def _getAnchorTypeGlyph(self, g):
        """Answer the glyph that is model for the anchors of g. If glyphData.anchorGlyphSrc is defined then use that glyph,
        e.g. as defined for /Uhorn using the anchor type positions of /U. Otherwise answer g as model."""
        assert g is not None
        gd = self.getGlyphData(g)
        if gd is None:
            print(f'### setGlyphAnchors: Cannot find GlyphData for /{g.name}')

        elif gd.anchorGlyphSrc is not None: # There is a src glyph other than /g to copy guessed anchor positions from
            if gd.anchorGlyphSrc in g.font: # Does the reference exist?
                return g.font[gd.anchorGlyphSrc]
            # Print the error if the referenced glyph cannot be found
            print(f'### Cannot find anchorGlyphSrc /{gd.anchorGlyphSrc} for /{g.name}') 

        return g # By default use this glyph as its own source to guess possible anchor positions from

    #   A N C H O R  P O S I T I O N  C O N S T R U C T I O N S

    def autoCheckFixAnchorPosition(self, g, gd, a):
        if g.name == GGGG:
            print('@@@ autoCheckFixAnchorPosition', g.name, g.font.path.split('/')[-1], id(g.font))

        changed = False

        ax = ay = None
        if a.name == AD.TOP_:
            ax, ay = self.constructAnchorTOP_XY(g, gd, a)

        elif a.name == AD._TOP:
            ax, ay = self.constructAnchor_TOPXY(g, gd, a)

        elif a.name == AD.MIDDLE_:
            ax, ay = self.constructAnchorMIDDLE_XY(g, gd, a)

        elif a.name == AD._MIDDLE:
            ax, ay = self.constructAnchor_MIDDLEXY(g, gd, a)
        
        elif a.name == AD.BOTTOM_: # Try to guess bottom position
            ax, ay = self.constructAnchorBOTTOM_XY(g, gd, a)
        
        elif a.name == AD._BOTTOM:
            ax, ay = self.constructAnchor_BOTTOMXY(g, gd, a)

        elif a.name == AD.OGONEK_: # Try to guess bottom position
            ax, ay = self.constructAnchorOGONEK_XY(g, gd, a)

        elif a.name == AD.TOPLEFT_: # Try to guess topleft position only for capitals
            ax, ay = self.constructAnchorTOPLEFT_XY(g, gd, a)

        if ax is not None:
            ax = int(round(ax))
            if ax != a.x:
                print(f'... Fix /{g.name} anchor {a.name}.x {ax} --> {a.x} sc={gd.isSc} lower={gd.isLower} in {g.font.path.split('/')[-1]}')
                print('ddd', g)
                #zzz = ddd
                a.x = ax
                changed = True
        if ay is not None:
            ay = int(round(ay))
            if ay != a.y:
                print(f'... Fix /{g.name} anchor {a.name}.y {ay} --> {a.y} sc={gd.isSc} lower={gd.isLower} in {g.font.path.split('/')[-1]}')
                print('ddd', g)
                #fff = ddd
                a.y = ay
                changed = True
        return changed

    # Deprecated, let's rewrite this one.
    def XXXconstructAnchorTOP_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the TOP_ anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        """
        md = self.getMasterData(g.font)

        offsetX, offsetY = self.getLib(g, self.ANCHOR_TOP_OFFSET, (0, 0))

        ax = ay = None
        baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base, just copy the vertical and hotizontal anchor positions, with the component offset

        # TOP_ Construct vertical position
        if gd.autoFixAnchorPositionY:
            if gd.anchorTopY is not None:
                if gd.anchorTopY in g.font: # In case it is an existing glyph name, then take the vertical position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorTopY], a.name)
                    if aa is not None:
                        ay = aa.y

                elif gd.isSc and 'H.sc' in g.font:
                    # Make sure to set the H.sc vertical top anchor position as model for all other .sc
                    scAnchor = self.getAnchor(g.font['H.sc'], a.name)
                    if scAnchor:
                        ay = scAnchor.y + dy

                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ay
                    # Available: 
                    ay = getattr(self, 'constructAnchor'+gd.anchorTopY)(g, gd, a.name, a.x, ay or a.y) # @@@ Various methods still to be implemented

            if ay is None: # Still None, no construction glyph or method defined, then try to figure out from this glyph shape
                # Trying to guess vertical from anchor in base glyph + its offset
                if gd.hasDiacritics: 
                    # This is a glyph, probably with diacritics. If these are on top, then the anchor position needs
                    # to be lifted to accommodate the higher bounding box. Since there are accents, we can safely
                    # assume that the base glyph is also defined. So let's start there.
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ay = baseAnchor.y + dy # Vertical position of the base anchor + component offset.
                        if g.bounds is not None: # Probably bounding box extended from diacritics
                            if gd.isLower: # Default position below xHeight or capHeight
                                ay = g.bounds[3] + md.xHeightDiacriticsAnchorOffsetY # Likely to ba a negative number
                            elif gd.isSc:
                                ay = g.bounds[3] + md.scHeightDiacriticsAnchorOffsetY # Likely to ba a negative number                                
                            else:
                                ay = g.bounds[3] + md.capHeightDiacriticsAnchorOffsetY # Likely to ba a negative number
                
                elif gd.isSc and 'H.sc' in g.font:
                    # Make sure to set the H.sc vertical top anchor position as model for all other .sc
                    scAnchor = self.getAnchor(g.font['H.sc'], a.name)
                    if scAnchor:
                        ay = scAnchor.y + dy

                elif baseGlyph is not None:
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ay = baseAnchor.y + dy # Vertical position of the base anchor + component offset.
                
                if ay is None: # No base component, get the height from xHeight or capHeight
                    if gd.isLower: # Default position below xHeight or capHeight
                        ay = md.xHeight + md.xHeightAnchorOffsetY # Likely to ba a negative number
                    elif gs.isSc:
                        ay = md.scHeight + md.scAnchorOffsetY # Likely to ba a negative number
                    else:
                        ay = md.capHeight + md.capHeightAnchorOffsetY # Likely to ba a negative number
                
                # In case the a.y now is below the bounding box, then lift the anchor to fit the top of the bounding box
                if gd.isLower: # Default position below xHeight or capHeight
                    if g.bounds is not None and md.baseDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                        ay = g.bounds[3] + md.boxTopAnchorOffsetY
                elif gd.isSc:
                    if g.bounds is not None and md.baseDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                        ay = g.bounds[3] + md.boxTopAnchorOffsetY                    
                else: 
                    if g.bounds is not None and md.capDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                        ay = g.bounds[3] + md.boxTopAnchorOffsetY

        # TOP_ Construct horizontal position
        if gd.autoFixAnchorPositionX:
            if gd.anchorTopX is not None:
                if gd.anchorTopX in g.font: # In case it is an existing glyph name, then take the horizontal position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorTopX], a.name)
                    if aa is not None:
                        ax = aa.x
                    # Then add the offset of the referring component
                    for component in g.components:
                        if component.baseGlyph == gd.anchorTopX:
                            ax += component.transformation[-2]
                            
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ax
                    # Available: 
                    # Constructor methods are supposed to answer italic x-position
                    ax = getattr(self, 'constructAnchor' + gd.anchorTopX)(g, gd, a.name, a.x, ay or a.y) # Use new ay here. Various methods still to be implemented

            # Hack, this should become an optioncal construction method
            elif g.name == 'J': # Special case, can't use the width. Find the top-left most corner point
                p1, p2 = self.getXBounds(g, y1=g.font.info.capHeight)
                ax = self.italicX(g, p1.x + (p2.x - p1.x)/2, ay, baseY=g.font.info.capHeight) # Half stem of /J

            elif ay is not None: # No construction glyph or method name defined, then try to figure out from the glyph shape
                # Try to guess horizontal from anchor in base glyph + its offset
                if baseGlyph is not None: # In case there is a base
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)
                else: # Center on width by default, otherwise use the gd.anchorTopX="Bounds" method
                    ax = self.italicX(g, g.width/2, ay)

        if ax is not None:
            ax += offsetX
        if ay is not None:
            ay += offsetY + md.topAnchorYSelectionOffset # Add topAnchorYSelectionOffset as extra offset below height for better manual selection of the anchor
        
        return ax, ay

    def XXXXXconstructAnchorTOP_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the TOP_ anchor for g, based on available rules and shape. 
        The x and/or y can be None in case not a valid value could be constructed. 
        In that case the position needs to be set manually in the editor.

        Order of rules for Y
        * if gd.anchorTypeY is pointing to an existing glyph, then copy the Y position of the equivalent anchor

        """
        VERBOSE = True

        md = self.getMasterData(g.font)
        gd.fixBaseAnchors = True

        # In case there is a manually adjusted offset in the g.lib, then add it to the automatic result.
        offsetX, offsetY = self.getLib(g, self.ANCHOR_TOP_OFFSET, (0, 0))

        # Start with a black anchor positions. If they remain None, then we could not construct a value
        ax = ay = None
        # In case there is a base, just copy the vertical and horizontal anchor positions, with the component offset
        baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) 
        if gd.fixBaseAnchors and baseGlyph is not None:
            # Make sure that this is recursively fixed
            self.constructAnchorTOP_XY(baseGlyph, self.getGlyphData(baseGlyph), a)

        # TOP_ Construct vertical position
        if gd.autoFixAnchorPositionY: # Only if the auto-fix flag is on.
            if VERBOSE:
                print(f'[00] /{g.name} {gd.anchorTopY} {g.bounds} {gd.isLower} {gd.isSc}')
            if gd.anchorTopY is not None: 
                # In case it is an existing glyph name, then take the vertical position from the corresponding anchor
                if gd.anchorTopY in g.font: 
                    aa = self.getAnchor(g.font[gd.anchorTopY], a.name)
                    if aa is not None:
                        ay = aa.y

                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ay
                    methodName = 'constructAnchor' + gd.anchorTopY
                    if hasattr(self, methodName):
                        # Available: 
                        ay = getattr(self, methodName)(g, gd, a.name, a.x, ay or a.y) # @@@ Various methods still to be implemented
                    elif VERBOSE:
                        print(f'### (constructAnchorTOP_XY) Warning: Unknown gd.anchorTopY={gd.anchorTopY} for /{g.name}')

            if ay is None: # Still None, no construction glyph or method defined, then try to figure out from this glyph shape
                # Trying to guess vertical from anchor in base glyph + its offset
                if gd.hasDiacritics: # Just test on diacritic components, not for the base glyph
                    # This is a glyph, probably with diacritics. If these are on top, then the anchor position needs
                    # to be lifted to accommodate the higher bounding box. Since there are accents, we can safely
                    # assume that the base glyph is also defined. So let's start there.
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ay = baseAnchor.y + dy # Vertical position of the base anchor + component offset.
                        if g.bounds is not None: # Probably bounding box extended from diacritics
                            if gd.isLower: # Default position below xHeight or capHeight
                                offsetFromBounds = -30#md.xHeightDiacriticsAnchorOffsetY # Likely to ba a negative number
                            elif gd.isSc:
                                offsetFromBounds = -30 #md.scHeightDiacriticsAnchorOffsetY # Likely to ba a negative number                                
                            else:
                                offsetFromBounds = -48 #md.capHeightDiacriticsAnchorOffsetY # Likely to ba a negative number
                            if VERBOSE:
                                print(f'[10] /{g.name} {offsetFromBounds} {ay} {gd.isLower} {gd.isSc}')
                            ay = g.bounds[3] + offsetFromBounds
                
                # elif gd.isSc and 'H.sc' in g.font:
                #     # Make sure to set the H.sc vertical top anchor position as model for all other .sc
                #     scAnchor = self.getAnchor(g.font['H.sc'], a.name)
                #     if scAnchor:
                #         ay = scAnchor.y + dy

                # There is a baseGlyph and not accents: then do a plain copy from the baseGlyph anchor position
                elif baseGlyph is not None:
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if VERBOSE:
                        print(f'[20] /{g.name} baseGlyph:/{baseGlyph.name} baseAnchor.y {baseAnchor.y}')
                    if baseAnchor is not None:
                        ay = baseAnchor.y + dy # Vertical position of the base anchor + component offset.
                
                if ay is None: # No base component, get the height from xHeight or capHeight
                    if gd.isLower: # Default position below xHeight or capHeight
                        ay = md.xHeight + md.xHeightAnchorOffsetY # Likely to ba a negative number
                    elif gd.isSc:
                        ay = md.scHeight + md.scAnchorOffsetY # Likely to ba a negative number
                    else:
                        ay = md.capHeight + md.capHeightAnchorOffsetY # Likely to ba a negative number
                    if VERBOSE:
                        print(f'[30] /{g.name} ay={ay}')
                
                # # In case the a.y now is below the bounding box, then lift the anchor to fit the top of the bounding box
                # if gd.isLower: # Default position below xHeight or capHeight
                #     if g.bounds is not None and md.baseDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                #         ay = g.bounds[3] + md.boxTopAnchorOffsetY
                # elif gd.isSc:
                #     if g.bounds is not None and md.baseDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                #         ay = g.bounds[3] + md.boxTopAnchorOffsetY                    
                # else: 
                #     if g.bounds is not None and md.capDiacriticsTop < g.bounds[3]: # Probably bounding box extended from diacritics
                #         ay = g.bounds[3] + md.boxTopAnchorOffsetY

        # TOP_ Construct horizontal position
        if gd.autoFixAnchorPositionX:
            if gd.anchorTopX is not None:
                if gd.anchorTopX in g.font: # In case it is an existing glyph name, then take the horizontal position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorTopX], a.name)
                    if aa is not None:
                        ax = aa.x
                    # Then add the offset of the referring component
                    for component in g.components:
                        if component.baseGlyph == gd.anchorTopX:
                            ax += component.transformation[-2]
                            
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ax
                    # Available: 
                    # Constructor methods are supposed to answer italic x-position
                    ax = getattr(self, 'constructAnchor' + gd.anchorTopX)(g, gd, a.name, a.x, ay or a.y) # Use new ay here. Various methods still to be implemented

            # Hack, this should become an optioncal construction method
            elif g.name == 'J': # Special case, can't use the width. Find the top-left most corner point
                p1, p2 = self.getXBounds(g, y1=g.font.info.capHeight)
                ax = self.italicX(g, p1.x + (p2.x - p1.x)/2, ay, baseY=g.font.info.capHeight) # Half stem of /J

            elif ay is not None: # No construction glyph or method name defined, then try to figure out from the glyph shape
                # Try to guess horizontal from anchor in base glyph + its offset
                if baseGlyph is not None: # In case there is a base
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)
                else: # Center on width by default, otherwise use the gd.anchorTopX="Bounds" method
                    ax = self.italicX(g, g.width/2, ay)

        if ax is not None:
            ax += offsetX
        if ay is not None:
            ay += offsetY # Add topAnchorYSelectionOffset as extra offset below height for better manual selection of the anchor
        
        return ax, ay

    def XXXconstructAnchor_TOPXY(self, g, gd, a):
        """Answer the constructed (x, y) position of the _TOP anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        md = self.getMasterData(g.font)
        ax = ay = None
        # In case the a.y now is above the bounding box, then lift the anchor to fit the top of the bounding box

        if gd.autoFixAnchorPositionY:
            if g.bounds is not None: # In case of stacked diacritics, take the box position above
                yy = g.bounds[3] + 36
            else:
                yy = 0
            if gd.isLower:
                ay = max(yy, g.font.info.xHeight) + md.xHeightAnchorOffsetY # Likely to ba a negative number. All dicritics are positioned on x-height
            else:
                ay = max(yy, g.font.info.capHeight) + md.capHeightAnchorOffsetY # Likely to ba a negative number. All dicritics are positioned on x-height
        if gd.autoFixAnchorPositionX and ay is not None:
            ax = self.italicX(g, 0, ay) # All glyph that contain _top are supposed to have width = 0
        
        return ax, ay

    def constructAnchorTOP_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the TOP_ anchor for g, based on available rules and shape. 
        The x and/or y can be None in case not a valid value could be constructed. 
        In that case the position needs to be set manually in the editor.

        Order of rules for Y
        * if gd.anchorTypeY is pointing to an existing glyph, then copy the Y position of the equivalent anchor

        """
        VERBOSE = True

        md = self.getMasterData(g.font)
        gd.fixBaseAnchors = True

        # In case there is a manually adjusted offset in the g.lib, then add it to the automatic result.
        offsetX, offsetY = self.getLib(g, self.ANCHOR_TOP_OFFSET, (0, 0))

        # Start with a black anchor positions. If they remain None, then we could not construct a value
        ax = ay = baseAnchor = None

        # In case there is a base, just copy the vertical and horizontal anchor positions, with the component offset
        baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) 
        if gd.fixBaseAnchors and baseGlyph is not None:
            # Make sure that this is recursively fixed
            self.constructAnchorTOP_XY(baseGlyph, self.getGlyphData(baseGlyph), a)

        if baseGlyph is not None:
            baseAnchor = self.getAnchor(baseGlyph, a.name)

        # TOP_ Construct vertical position
        if gd.autoFixAnchorPositionY: # Only if the auto-fix flag is on.

            # There is a baseGlyph and not accents: then do a plain copy from the baseGlyph anchor position
            if ay is None and baseAnchor is not None:
                ay = baseAnchor.y + dy # Vertical position of the base anchor + component offset.

            if ay is None: # Still None, no construction glyph or method defined, then try to figure out from this glyph shape
                # Trying to guess vertical from anchor in base glyph + its offset
                if gd.hasDiacritics: # Just test on diacritic components, not for the base glyph
                    # This is a glyph, probably with diacritics. If these are on top, then the anchor position needs
                    # to be lifted to accommodate the higher bounding box. Since there are accents, we can safely
                    # assume that the base glyph is also defined. So let's start there.
                    if g.bounds is not None: # In case of stacked diacritics, take the box position above
                        yy = g.bounds[3] + md.boxTopAnchorOffsetY
                    else:
                        yy = 0
                    if gd.isLower:
                        ay = max(yy, g.font.info.xHeight + md.xHeightAnchorOffsetY) # Likely to ba a negative number. All dicritics are positioned on x-height
                    elif gd.isSc:
                        ay = max(yy, md.scHeight + md.xHeightAnchorOffsetY) # Likely to ba a negative number. All dicritics are positioned on x-height
                    else:
                        ay = max(yy, g.font.info.capHeight + md.capHeightAnchorOffsetY) # Likely to ba a negative number. All dicritics are positioned on x-height

            if ay is None: # No base component, and still None. Get the height from xHeight or capHeight
                # Calculate position, in case the top-bound exceeds the normal xHeight/capHeight position.
                # This happens with ascenders and diacritics
                # Example glyphs for this method: /dieresiscmb, /A
                if g.bounds is not None: # In case of stacked diacritics, take the box position above
                    yy = g.bounds[3] + md.boxTopAnchorOffsetY
                else:
                    yy = 0
                if gd.isLower:
                    ay = max(yy, g.font.info.xHeight + md.xHeightAnchorOffsetY) # Likely to ba a negative number. All dicritics are positioned on x-height
                elif gd.isSc:
                    ay = max(yy, md.scHeight + md.xHeightAnchorOffsetY) # Likely to ba a negative number. All dicritics are positioned on x-height
                else:
                    ay = max(yy, g.font.info.capHeight + md.capHeightAnchorOffsetY) # Likely to ba a negative number. All dicritics are positioned on x-height

            if ay is not None:
                ay += offsetY 

        if gd.autoFixAnchorPositionX: # Only if the auto-fix flag is on.

            if gd.anchorTopX is not None:
                # In case it is an existing glyph name, then take the horizontal position from the corresponding anchor
                # This is used to position the anchor on top of round glyphs that are not symmetric, e.g. /C and /a
                if isinstance(gd.anchorTopX, (int, float)):
                    ax = self.italicX(g, gd.anchorTopX, ay or 0)

                elif gd.anchorTopX in g.font: 
                    aa = self.getAnchor(g.font[gd.anchorTopX], a.name)
                    if aa is not None:
                        ax = aa.x
                    # Then add the offset of the referring component
                    #for component in g.components:
                    #    if component.baseGlyph == gd.anchorTopX:
                    #        ax += component.transformation[-2]
                        
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ax
                    # Available: 
                    # Constructor methods are supposed to answer italic x-position
                    ax = getattr(self, 'constructAnchor' + gd.anchorTopX)(g, gd, a.name, a.x, ay or a.y) # Use new ay here. Various methods still to be implemented

            if ax is None and ay is not None: # No construction glyph or method name defined, then try to figure out from the glyph shape
                # Try to guess horizontal from anchor in base glyph + its offset
                if baseAnchor is not None:
                    ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)
                else: # Center on width by default, otherwise use the gd.anchorTopX="Bounds" method
                    ax = self.italicX(g, g.width/2, ay)

            if ax is not None:
                ax += offsetX

        return ax, ay

    def constructAnchor_TOPXY(self, g, gd, a):
        """Answer the constructed (x, y) position of the _TOP anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        md = self.getMasterData(g.font)
        ax = ay = None
        # In case the a.y now is above the bounding box, then lift the anchor to fit the top of the bounding box
        if gd.autoFixAnchorPositionY:
            yy = 0
            if gd.isLower:
                ay = max(yy, g.font.info.xHeight) + md.xHeightAnchorOffsetY # Likely to ba a negative number. All dicritics are positioned on x-height
            else:
                ay = max(yy, g.font.info.capHeight) + md.capHeightAnchorOffsetY # Likely to ba a negative number. All dicritics are positioned on x-height
        if gd.autoFixAnchorPositionX and ay is not None:
            ax = self.italicX(g, 0, ay) # All glyph that contain _top are supposed to have width = 0

        return ax, ay

    def constructAnchorMIDDLE_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the MIDDLE_ anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        md = self.getMasterData(g.font)
        ax = g.width/2
        if gd.isSc:
            ay = md.scHeight/2
        elif gd.isLower:
            ay = md.xHeight/2
        else:
            ay = md.capHeight/2

        # In case there is a manually adjusted offset in the g.lib, then add it to the automatic result.
        offsetX, offsetY = self.getLib(g, self.ANCHOR_MIDDLE_OFFSET, (0, 0))

        # MIDDLE_ Construct vertical position
        if gd.autoFixAnchorPositionY:
            if gd.anchorMiddleY is not None:
                if gd.anchorMiddleY in g.font: # In case it is an existing glyph name, then take the vertical position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorMiddleY], a.name)
                    if aa is not None:
                        ay = aa.y
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ay
                    # Available: 
                    ay = getattr(self, 'constructAnchor' + gd.anchorMiddleY)(g, gd, a.name, a.x, ay or a.y) # @@@ Various methods still to be implemented

            else: # No construction glyph or method defined, then try to figure out from this glyph shape
                # Trying to guess vertical
                if gd.isSc:
                    md = self.getMasterData(g.font)
                    ay = md.scHeight/2
                elif gd.isLower: # Default position below xHeight or capHeight
                    ay = md.xHeight/2
                else:
                    ay = md.capHeight/2

        # TOP_ Construct horizontal position
        if gd.autoFixAnchorPositionX:
            if gd.anchorMiddleX is not None:
                if gd.anchorMiddleX in g.font: # In case it is an existing glyph name, then take the vertical position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorMiddleX], a.name)
                    if aa is not None:
                        ax = aa.x
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ay
                    # Available: 
                    # Constructor methods are supposed to answer italic x-position
                    ax = getattr(self, 'constructAnchor' + gd.anchorMiddleX)(g, gd, a.name, a.x, ay or a.y) # Use new ay here. Various methods still to be implemented

            # Hack, this should become an optioncal construction method
            elif g.name == 'J': # Special case, can't use the width. Find the top-left most corner point
                p1, p2 = self.getXBounds(g, y1=g.font.info.capHeight)
                ax = self.italicX(g, p1.x + (p2.x - p1.x)/2, ay, baseY=g.font.info.capHeight) # Half stem of /J

            else: # No construction glyph or method name defined, then try to figure out from the glyph shape
                # Try to guess horizontal
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base 
                if baseGlyph is not None:
                    #rint(baseGlyph.name, dx, dy)
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ax = baseAnchor.x + dx
                else: # Center on width by default
                    ax = self.italicX(g, g.width/2, ay)

        if ax is not None:
            ax += offsetX
        if ay is not None:
            ay += offsetY

        return ax, ay

    def constructAnchor_MIDDLEXY(self, g, gd, a):
        """Answer the constructed (x, y) position of the _MIDDLE anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        md = self.getMasterData(g.font)
        ax = ay = None
        if gd.autoFixAnchorPositionY:
            if gd.isLower: # Default position below xHeight or capHeight
                   ay = md.xHeight/2
            elif gd.isSc:
                ay = md.scHeight/2
            else:
                ay = md.capHeight/2

        if gd.autoFixAnchorPositionX:
            ax = self.italicX(g, 0, ay) # All glyph that contain _middle are supposed to have width = 0

        return ax, ay

    def constructAnchorBOTTOM_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the BOTTOM_ anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        """
        ax = ay = None
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)

        offsetX, offsetY = self.getLib(g, self.ANCHOR_BOTTOM_OFFSET, (0, 0))

        baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base, just copy the vertical and hotizontal anchor positions, with the component offset

        # BOTTOM_ Construct vertical position
        if gd.autoFixAnchorPositionY:
            if gd.anchorBottomY is not None:
                if gd.anchorBottomY in g.font: # In case it is an existing glyph name, then take the vertical position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorBottomY], a.name)
                    if aa is not None:
                        ay = aa.y
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ay
                    ay = getattr(self, 'constructAnchor' + gd.anchorBottomY)(g, gd, a.name, a.x, ay or a.y) # @@@ Various methods still to be implemented

            else: # No glyph or construction method defined, then try to figure out from this glyph shape
                # Trying to guess vertical
                # Default position below xHeight or capHeight
                ay = md.baselineAnchorOffsetY
                # In case the a.y now is above the bounding box, then lift the anchor to fit the top of the bounding box
                if g.bounds is not None and md.baseDiacriticsBottom > g.bounds[1]:
                    ay = g.bounds[1] + md.boxBottomAnchorOffsetY

        # BOTTOM_ Construct horizontal position
        if gd.autoFixAnchorPositionX:
            if gd.anchorBottomX is not None:
                if gd.anchorBottomX in g.font: # In case it is an existing glyph name, then take the vertical position from the corresponding anchor
                    aa = self.getAnchor(g.font[gd.anchorBottomX], a.name)
                    if aa is not None:
                        ax = aa.x
                else: # If not an existing glyph name, then we can assume it is a valid method name that will calculate the ay
                    # Constructor methods are supposed to answer italic x-position
                    ax = getattr(self, 'constructAnchor' + gd.anchorBottomX)(g, gd, a.name, a.x, ay or a.y) # Use new ay here. Various methods still to be implemented

            # Hack, this should become an optioncal construction method
            elif g.name == 'R' and ay is not None: # Special case, can't use the width. Find the top-left most corner point
                p1, p2 = self.getXBounds(g, y1=0)
                if p1 is not None and p2 is not None:
                    ax = self.italicX(g, p1.x + (p2.x - p1.x)/2, ay or 0) # Half stem of /J

            elif ay is not None: # No construction glyph or method name defined, then try to figure out from the glyph shape
                # BOTTOM_ Construct horizontal position
                if baseGlyph is not None:
                    baseAnchor = self.getAnchor(baseGlyph, a.name)
                    if baseAnchor is not None:
                        ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)
                else: # Center in width by default
                    ax = self.italicX(g, g.width/2, ay)

        if ax is not None:
            ax += offsetX
        if ay is not None:
            ay += offsetY

        return ax, ay

    def constructAnchor_BOTTOMXY(self, g, gd, a):
        """Answer the constructed (x, y) position of the BOTTOM_ anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        md = self.getMasterData(g.font)
        ax = ay = None
        if gd.autoFixAnchorPositionY:
            ay = md.baselineAnchorOffsetY
        if gd.autoFixAnchorPositionX:
            ax = self.italicX(g, 0, ay) # All glyph that contain _bottom are supposed to have width = 0

        return ax, ay

    def constructAnchorOGONEK_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the OGONEK_ anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        ax = ay = None
        md = self.getMasterData(g.font)
        gd = self.getGlyphData(g)
        # If there is a base, then take the horizontal position of the ogonek
        if gd.autoFixAnchorPositionY:
            if gd.base:
                # In case there is a base, just copy the vertical and hotizontal anchor positions, with the component offset
                baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) 
                baseAnchor = self.getAnchor(baseGlyph, a.name)
                if baseAnchor is not None:
                    ax = baseAnchor.x + dx
                    ay = baseAnchor.y + dy
        if gd.autoFixAnchorPositionX:
            if ax is None:
                # Trying to guess vertical
                ay = md.ogonekAnchorOffsetY
                ax = None # Otherwise the horizontal position is always manual

        return ax, ay

    def constructAnchorTOPLEFT_XY(self, g, gd, a):
        """Answer the constructed (x, y) position of the TOPLEFT_ anchor for g, based on available rules and shape. The x and/or y can be None 
        in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
        @@@ No methods here yet.
        """
        # Trying to guess vertical
        ax = ay = None

        if gd.autoFixAnchorPositionY:
            ay = g.font.info.capHeight # Likely to ba a negative number

        # Try to guess horizontal
        if gd.autoFixAnchorPositionX:
            baseGlyph, (dx, dy) = self.getBaseGlyphOffset(g) # In case there is a base 
            if baseGlyph is not None:
                baseAnchor = self.getAnchor(baseGlyph, a.name)
                if baseAnchor is not None:
                    ax = baseAnchor.x + self.italicX(g, dx, ay - baseAnchor.y)

            # @@@ Hack to correct topleft anchor on specific glyph shapes
            elif g.name == 'A': # Special case, can't use the left margin. Find the top-left most corner point
                bounds = self.getXBounds(g, y1=g.font.info.capHeight) # Test if there are bounds, not if topleft is not supported
                if bounds[0] is not None:
                    ax = bounds[0].x * 3/4

            elif g.name in ('O', 'Ohm'): # Special case, can't use the left margin. Find the top-left most corner point
                ax = self.italicX(g, g.angledLeftMargin, ay) # Right aligned on margin

            else: # Center in width by default
                ax = self.italicX(g, g.angledLeftMargin/2, ay) # Right aligned, halfway left margin

        return ax, ay

    #def constructAnchor_TOPLEFTXY(self, g, a):
    #    """Answer the constructed (x, y) position of the _TOPLEFT anchor for g, based on available rules and shape. The x and/or y can be None 
    #    in case not valid value could be constructed. In that case the position needs to be set manually in the editor.
    #    @@@ No methods here yet.
    #    """
    #    # Trying to guess vertical
    #    ay = g.font.info.capHeight # Likely to ba a negative number
    #    ax = self.italicX(g, 0, ay) # Right aligned, halfway left margin
    #
    #    return ax, ay

    #   A N C H O R  P O S I T I O N  C O N S T R U C T O R S

    def constructAnchorBoundsX2(self, g, gd, a, ax, ay):
        """Constructor method for half bounds width. Because of italic shapes, we cannot use g.bounds here. Use angled margins instead."""
        #print('... Anchor position by constructAnchorBoundsX2')
        ml = g.angledLeftMargin
        mr = g.angledRightMargin
        if not None in (ml, mr):
            return self.italicX(g, ml + (g.width - ml - mr)/2, ay) # Construct methods are supposed to answer italicized x-positions
        return g.width/2 # Cannot find margins, so just answer width/2

    def constructAnchorTopX(self, g, gd, a, ax, ay):
        """Answer the X position of the highest point(s). If there is not point (e.g. just contours), then answer the middle of the bounaries."""
        xx = []
        y = None
        for contour in g.contours:
            for p in contour.points:
                if p.type == 'offcurve':
                    continue
                if y is None or y == p.y:
                    y = p.y
                    xx.append(p.x)
                elif y < p.y:
                    y = p.y
                    xx = [p.x]
        if xx:
            return int(round(sum(xx)/len(xx)))
        # Could not find an x, e.g. because of only components. Then use the bounding box width/2 instead.
        return self.constructAnchorBoundsX2(g, gd, a, ax, ay)

    def constructAnchorTopY(self, g, gd, a, ax, ay):
        """Answer the anchor TopX measured against the bounding box.""" 
        md = self.getMasterData(g.font)
        if gd.isUpper:
            if g.bounds is not None and ay < g.bounds[3] + md.capHeightAnchorOffsetY: # Probably bounding box extended from diacritics
                ay = g.bounds[3] + md.capHeightAnchorOffsetY
        # Test on small caps too here.
        else:
            if g.bounds is not None and ay < g.bounds[3] + md.xHeightAnchorOffsetY: # Probably bounding box extended from diacritics
                ay = g.bounds[3] + md.xHeightAnchorOffsetY
        return ay

    def constructAnchorMiddleX(self, g, gd, a, ax, ay):
        """Answer the X position of as average of TopX and BottomX. If there is not point (e.g. just contours), then answer the middle of the boundaries."""
        return (self.constructAnchorTopX(g, gd, a, ax, ay) + self.constructAnchorBottomX(g, gd, a, ax, ay))/2

    def constructAnchorBottomX(self, g, gd, a, ax, ay):
        """Answer the X position of the lowest point(s). If there is no point (e.g. just contours), then answer the middle of the boundaries."""
        xx = []
        y = None
        for contour in g.contours:
            for p in contour.points:
                if p.type == 'offcurve':
                    continue
                if y is None or y == p.y:
                    y = p.y
                    xx.append(p.x)
                elif y > p.y:
                    y = p.y
                    xx = [p.x]
        if xx: # In case it was defined
            return int(round(sum(xx)/len(xx)))
        # Could not find an x, e.g. because of only components. Then use the bounding box width/2 instead.
        return self.constructAnchorBoundsX2(g, gd, a, ax, ay)

    def constructAnchorBaselineY(self, g, gd, a, ax, ay):
        """Answer the Y position on baseline."""
        md = self.getMasterData(g.font)
        ay = md.baselineAnchorOffsetY
        return ay

    #   M E R Z  A N C H O R  P O S I T I O N S

    def XXXupdateGuessedAnchorPositions(self, g):
        """Reset the guessed anchor positions for this glyph, e.g. after the glyphEditor set another glyph, or if spacing or bounding box changed.
        This method is not changing any position of the anchors it self."""
        return 

        c = self.getController()
        self.guessedAnchorPositions = {}
        # Get the glyph that is model for the anchor types, if defined in glyphData.anchorGlyphSrc, otherwise use /g itself.
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

    '''

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
    '''

    #   K E Y S

    def anchorsGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']

        # If checkbox is set, then check/fix the anchors in glyphs of the current master.

        if c.lower() == c: # Just the current glyph as [a] key
            pass # Nothing for now on [a]
        else: # All glyphs in all open masters as [A] key
            if g.name == GGGG:
                print(g, self.getCurrentGlyph(), id(g.font), id(self.getCurrentGlyph().font))
            f = self.getCurrentGlyph().font # @@@ Hack
            for gg in f:
                #self.checkFixAllAnchors(g.font)
                self.setGlyphAnchors(gg)

    def anchorsCenterOnWidth(self, g, c, event):
        """If there are anchors selected, then center them on the width. If no anchors are selected,
        the center all on width."""
        changed = False
        for a in self.getAnchors(g): # Answers selected anchors or all
            if not a.name in AD.CENTERING_ANCHORS: # Does this anchor center?
                continue # Otherwise ignore
            x = int(round(g.width/2 + a.y * tan(radians(-(g.font.info.italicAngle or 0)))))
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
        if gd is None:
            print(f'### checkFixRomanItalicAnchors: Cannot find GlyphData for /{g.name}')
            return False

        src = self.getFont(md.romanItalicUFOPath)
        if src is not None and g.name in src:
            srcG = src[g.name]
            anchors = self.getAnchorsDict(g) # Get a dictionary of anchors
            srcAnchors = self.getAnchorsDict(srcG)
            for aName, srcA in srcAnchors.items():
                x = int(round(srcA.x + srcA.y * tan(radians(-(f.info.italicAngle or 0)))))
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


