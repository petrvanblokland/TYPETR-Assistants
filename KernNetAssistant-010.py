# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright (c) 2023+ TYPETR | Petr van Blokland
#   Usage by MIT License
#
# ..............................................................................
#
#    KernNetAssistant-010.py
#
#    The KernNet Assistant support the following functions:
#    - Works on the CurrentFont()
#    - FontData analyser, finding and caching cross-references (such as unicode2GlyphName dictionary)
#    - Spacing by Similarity
#    - Auto-grouping per script type
#    - Kerning form trained KernNet AI
#    - Samples by script
#    - Settings are stored in font.lib and glyph.lib
#
#    More in details:
#    
#    Keyboard driven alterations of spacing and kerning.
#    Selection from multiple kerning samples
#    Generating sample line file for FontGoggles
#    Support for various open type feature sets
#    Support for glyph-glyph, group-glyph, glyph-group and group-group kerning
#    Find function by glyph name
#    Shows kerning groups for the current selected pairs
#    Show kerning line samples in the Editor Window
#    Alloes selection by clicking on the sample line.
#
#    Install Similarity from Mechanic and run it once, after RoboFont starts.
#    The initial window can be closed. This way the library "cosoneSimilarity"
#    becomes available for this Assistant.
#
#    No need to import KernNet for AI assistent kerning. That will be available as local webserver.
#
import sys
import importlib
from math import *
from AppKit import *

from vanilla import *
import drawBot

from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from assistantLib.kerningSamples.fontGoggles import FONT_GOGGLES_SAMPLES
from assistantLib.tp_kerningManager import KerningManager

# Decide on the type of window for the Assistant.
WindowClass = Window # Will hide behind other windows, if not needed.
#WindowClass = FloatingWindow # Is always available, but it can block the view of other windows if the Asistant window grows in size.

# Add paths to libs in sibling repositories. The assistantLib module contains generic code for Asistanta.s
PATHS = ['../TYPETR-Assistants/']
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

# Global parameters
W, H = 400, 600
WH = 300 # WH > 300 is used for (hidden) preferences
M = 20 
BW = 200 - 2*M # Button width
BH = 24 # Button height
FAR = 100000 # Put drawing stuff outside the window

# Kerning line parameters
KERN_LINE_SIZE = 32 # Number of glyphs on kerning line
KERN_SCALE = 0.15 #0.2

TAB_WIDTH = 1170 # Can be altered in a textbox, stored in font.lib

SYMMETRIC_GLYPHS = (# Valid to calibrate margins <--> kerning. Stored in font.lib. Can be altered in textbox. 
    'zero', 
    'A', 'H', 'I', 'M', 'N', 'O', 'T', 'U', 'V', 'W', 'X', 'Y', 
    'o', 's', 'x', 'v', 'w', 
)

ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]
        
FUNCTION_KEYS = (
    'Uu', # Decrement left margin
    'Ii', # Increment left margin
    'Oo', # Decrement right margin
    'Pp', # Increment right margin
    '=', # Set left and right pair kerning to self.predictedKerning. Clear "manualKerning" in font.lib
    'Nn', # Increment left kerning. Set "manualKerning" in font.lib
    'Mm', # Decrement left kerning. Set "manualKerning" in font.lib
    '.<', # Decrement right kerning. Set "manualKerning" in font.lib
    ',>', # Increment right kerning. Set "manualKerning" in font.lib
)

KERNING_SAMPLE_SELECT_LIB = 'TYPETR-KernNetAssistant-Index'
KERNING_SAMPLE_X = 'KerningAssistant-FG-Sample'

# Color indicating theh type of kerning
GROUPGROUP_COLOR = (0, 0, 0, 0.8) # Color for showing glyph outlines and sample text
GROUPGLYPH_COLOR = (0, 0, 0.6, 1) # Golor for Group-Glyph or Glyph-Group kerning
GLYPHGLYPH_COLOR = (0, 0.4, 0, 1) # Color for Glyph-Glyph kerning

LIB_KEY = 'TYPETR-KernNetAssistant' # Key to store application settings in the font.lib and glyph.lib

def getLib(f_or_g):
    """Get the dictionary of flags that is stored in f.lib or g.lib"""
    if not LIB_KEY in f_or_g.lib:
        f_or_g.lib[LIB_KEY] = {}
    return f_or_g.lib[LIB_KEY]

class FontData:
    def __init__(self, f):
        """Build X-ref data from the from. Don't store the font itself, as it may be close by the calling application.
        Building a FontData takes a bit of time, so it’s best to cache it."""
        self.path = f.path
        # Fins all glyphs that use this glyph as component
        self.base = {} # Key is glyphName. Value is list of component.baseGlyph names
        # Find all diacritics and match them with the referring glyphs.
        self.diacritics = {} # Key is diacritics name. Value is list of glyph names that use this diacritic as component.
        # All glyphs that are in the same cloud of diacritics (affected by the position of the same anchor)
        self.diacriticsCloud = {} # Key is glyhName
        # All glyphs usage of anchors
        self.glyphAnchors = {} # Key is glyphName, Value is dict of ancbhor.name --> (x, y).
        self.anchors = {} # Key is anchor name. Value is list of glyphs that use this anchor
        # Unicode --> Glyph name
        self.unicodes = {} # Key is unicode (if it exists). Value is glyph name.
        for g in f:
            self.base[g.name] = [] # These glyphs have components refering to g.
            if g.name.endswith('cmb') or g.name.endswith('comb'):
                if g.unicode and g.name not in self.diacritics: # Only for real floating diacritics that have a unicode
                    self.diacritics[g.name] = []
        for g in f:
            self.base[g.name] = bb = []
            for component in g.components:
                bb.append(component.baseGlyph)
                if component.baseGlyph in self.diacritics: # Only for real diacritics (that have a unicode)
                    self.diacritics[component.baseGlyph].append(g.name)
                    
            # glyphName --> dict of anchors
            self.glyphAnchors[g.name] = aa = {}
            for a in g.anchors:
                aa[a.name] = a.x, a.y
                # anchorName --> List of glyph that are using it
                if a.name not in self.anchors:
                    self.anchors[a.name] = []
                self.anchors[a.name].append(g.name)
            if g.unicode:
                self.unicodes[g.unicode] = g.name
            
                    
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.path.split("/")[-1]}>'

kerningAssistant = None # Little hack, to make the assistant available from the window

class KernNetAssistant(Subscriber):

    SPACING_UNIT = 4
    KERNING_UNIT = 4
    
    def build(self):
        global kerningAssistant
        kerningAssistant = self


        self.kerningSample = None
        self.kerningManagers = {} # Key is f.path, value is KerningManager instance. Will be initialized by self.getKerningSample(f)  

        f = CurrentFont()
        if f is not None: # If there is a current font, then initialize the KerningManager now.
            self.getKerningManager(f) # Initialize self.kerningSample

        self.fontDatas = {} # Key is font path, value is FontData instance that holds mined X-ref data on the font.

        self.initMerz() # Initialize the Merz objects that this Assistant needs to display in the EditorWindow

    def initMerz(self):
        glyphEditor = self.getGlyphEditor()
        if glyphEditor is None:
            return
        
        self.foregroundContainer = container = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )
        
        #    K E R N I N G
        
        self.kernGlyphImage1 = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage1',
            position=(FAR, 0),
            fillColor=KERN_GLYPH_COLOR, # Opaque diacritics cloud
        )
        self.kernGlyphImage = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage',
            position=(FAR, 0),
            fillColor=KERN_GLYPH_COLOR, # Sets to light gray if not equal to current glyph.
        )
        self.kernGlyphImage2 = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage2',
            position=(FAR, 0),
            fillColor=KERN_GLYPH_COLOR, # Opaque diacritics cloud
        )
        self.kerning1Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning1Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning1Value.setHorizontalAlignment('center')
        
        self.kerning2Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning2Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning2Value.setHorizontalAlignment('center')

        self.leftMarginValue = self.backgroundContainer.appendTextLineSublayer(
            name="leftMarginValue",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.rightMarginValue = self.backgroundContainer.appendTextLineSublayer(
            name="rightMarginValue",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        
        #    K E R N I N G  L I N E
    
        self.kerningLine = [] # List of kerned glyph image layers
        self.kerningLineValues = [] # List of kerning value layers
        self.kerningLineBoxes = [] # List of kerned glyph em-boxes
        self.kerningSelectedGlyph = None # Name of the glyph selected by the kerning editor
        
        for gIndex in range(KERN_LINE_SIZE):
            # Previewing current glyphs on left/right side.        
            im = self.backgroundContainer.appendPathSublayer(
                name='kernedGlyph-%d' % gIndex,
                position=(FAR, 0),
                fillColor=(0, 0, 0, 1),
            )
            im.addScaleTransformation(KERN_SCALE)
            self.kerningLine.append(im)
            
            kerningLineValue = self.backgroundContainer.appendTextLineSublayer(
                name='kernedValue-%d' % gIndex,
                position=(FAR, 0),
                text='xxx\nxxx',
                font='Courier',
                pointSize=16,
                fillColor=(0, 0, 0, 1), # Can be red (negative kerning) or green (positive kerning)
            )
            kerningLineValue.addScaleTransformation(KERN_SCALE)
            kerningLineValue.setHorizontalAlignment('center')
            self.kerningLineValues.append(kerningLineValue)

            kerningLineBox = self.backgroundContainer.appendRectangleSublayer(
                name='kernedBox-%d' % gIndex,
                position=(FAR, 0),
                size=(1, 1),
                fillColor=None,
                strokeColor=(0, 0, 0, 0.5),
                strokeWidth=1,
            )
            kerningLineBox.addScaleTransformation(KERN_SCALE)
            self.kerningLineBoxes.append(kerningLineBox)

        self.kerningSelectedGlyphMarker = self.backgroundContainer.appendRectangleSublayer(
            name='kerningSelectedGlyphMarker',
            position=(FAR, 0),
            size=(1, 20),
            fillColor=(1, 0, 0, 1),
            strokeColor=None,
            strokeWidth=1,
        )
        self.kerningSelectedGlyphMarker.addScaleTransformation(KERN_SCALE)

        self.kerning1Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning1Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning1Value.setHorizontalAlignment('center')
        self.kerning2Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning2Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning2Value.setHorizontalAlignment('center')

        self.kerningCursorBox = self.backgroundContainer.appendTextLineSublayer(
            name="kerningCursorBox",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=14,
            fillColor=(0.6, 0.6, 0.6, 1),
        )

    def getFontData(self, f):
        """Answer the cached FontData instance. If it does not exist, create it and let it in construct X-refs from the @f. """
        if not f.path in self.fontDatas:
            self.fontDatas[f.path] = FontData(f) # Store the cobstructed data. This does not include the font itself.
        return self.fontDatas[f.path]

    #    E V E N T S
        
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
           
    def glyphEditorDidSetGlyph(self, info):
        g = info['glyph']
        self.update(g)

    def glyphEditorDidKeyDown(self, info):

        g = info['glyph']
        gd = getGlyphData(g.font, g.name)
         
        event = extractNSEvent(info['NSEvent'])
        characters = event['keyDown']
       
        commandDown = event['commandDown']
        shiftDown = event['shiftDown']
        controlDown = event['controlDown']
        optionDown = event['optionDown']
        self.capLock = event['capLockDown']

        if characters in '=':
            self.setKernNetKerning(g)
            changed = True

        #    G U I D E S
        
        elif characters in '§':
            self.setGlyphGuides(g)
            changed = True

        #     S P A C I N G

        # Support is now in KernNet Assitant
        elif characters in 'Pp': # Increment right margin
            if shiftDown:
                self._adjustRightMargin(g, 5)
            else:
                self._adjustRightMargin(g, 1)            
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
            
        elif characters in 'Oo': # Decrement right margin
            if shiftDown:
                self._adjustRightMargin(g, -5)
            else:
                self._adjustRightMargin(g, -1)
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Ii': # Increment left margin
            if shiftDown:
                self._adjustLeftMargin(g, 5)
            else:
                self._adjustLeftMargin(g, 1)            
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Uu': # Decrement left margin
            if shiftDown:
                self._adjustLeftMargin(g, -5)
            else:
                self._adjustLeftMargin(g, -1)            
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line

        #    K E R N I N G

        elif characters in '.>': # Increment right kerning
            if shiftDown:
                self._adjustRightKerning(g, 5) # 20
            else:
                self._adjustRightKerning(g, 1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in ',<': # Decrement right kerning
            if shiftDown:
                self._adjustRightKerning(g, -5) # 20
            else:
                self._adjustRightKerning(g, -1) # 4
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Mm': # Decrement left kerning
            if shiftDown:
                self._adjustLeftKerning(g, -5) # 20
            else:
                self._adjustLeftKerning(g, -1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Nn': # Increment left kerning
            if shiftDown:
                self._adjustLeftKerning(g, 5) # 20
            else:
                self._adjustLeftKerning(g, 1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line

        #    K E R N I N G  L I N E
        
        elif optionDown and characters == NSUpArrowFunctionKey:
            kerningSample = self.getKerningSample(g.font)
            currentCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            if shiftDown:
                cursor = max(0, currentCursor - 8*KERN_LINE_SIZE)
            else:
                cursor = max(0, currentCursor - KERN_LINE_SIZE)
            self.controller.w.kerningSampleSelectSlider.set(cursor)
            self.controller.w.kerningSampleSelectSlider.setMaxValue(len(kerningSample))
            self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d lines' % (int(round(cursor/KERN_LINE_SIZE)), len(kerningSample)/KERN_LINE_SIZE))
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            self.randomWord = choice(ULCWORDS) # Random word changed on up/down cursor
            self.saveKerningCursor()
                 
        elif optionDown and characters == NSDownArrowFunctionKey:
            kerningSample = self.getKerningSample(g.font)
            currentCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            if shiftDown:
                cursor = min(len(kerningSample)- KERN_LINE_SIZE, currentCursor + 8*KERN_LINE_SIZE)
            else:
                cursor = min(len(kerningSample)- KERN_LINE_SIZE, currentCursor + KERN_LINE_SIZE)
            self.controller.w.kerningSampleSelectSlider.set(cursor) 
            self.controller.w.kerningSampleSelectSlider.setMaxValue(len(kerningSample))
            self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d lines' % (int(round(cursor/KERN_LINE_SIZE)), len(kerningSample)/KERN_LINE_SIZE))
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            self.randomWord = choice(ULCWORDS) # Random word changed on up/down cursor
            self.saveKerningCursor()
        
        elif optionDown and characters == NSLeftArrowFunctionKey:
            kerningSample = self.getKerningSample(g.font)
            currentCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            if shiftDown:
                cursor = max(0, currentCursor - 8)
                self.randomWord = choice(ULCWORDS) # Random word changed on left-shift cursor
            else:
                cursor = max(0, currentCursor - 1)
            self.controller.w.kerningSampleSelectSlider.set(cursor)
            self.controller.w.kerningSampleSelectSlider.setMaxValue(len(kerningSample))
            self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d lines' % (int(round(cursor/KERN_LINE_SIZE)), len(kerningSample)/KERN_LINE_SIZE))
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif optionDown and characters == NSRightArrowFunctionKey:
            kerningSample = self.getKerningSample(g.font)
            currentCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            if shiftDown:
                cursor = min(len(kerningSample) - KERN_LINE_SIZE, currentCursor + 8)
                self.randomWord = choice(ULCWORDS) # Random word changed onright-shift cursor
            else:
                cursor = min(len(kerningSample) - KERN_LINE_SIZE, currentCursor + 1)
            self.controller.w.kerningSampleSelectSlider.set(cursor)
            self.controller.w.kerningSampleSelectSlider.setMaxValue(len(kerningSample))
            self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d lines' % (int(round(cursor/KERN_LINE_SIZE)), len(kerningSample)/KERN_LINE_SIZE))
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line

        if changed:
            g.changed()

    #    A D J U S T  S P A C I N G

    def _adjustLeftMargin(self, g, value): # This moved to TYPETR-Assistants/KerningAssistant-005.py
        if self.isUpdating:
            return
        f = g.font
        
        gd = getGlyphData(f, g.name)
        marginSrcName = gd.leftSpaceSourceLabel
        if not gd.fixedLeft:
            g.angledLeftMargin = int(round(g.angledLeftMargin/self.SPACING_UNIT) + SPACING_UNIT) * self.SPACING_UNIT
                          
    def _adjustRightMargin(self, g, value): # This moved to TYPETR-Assistants/KerningAssistant-005.py
        if self.isUpdating:
            return
        f = g.font
        unit = 4
        gd = getGlyphData(f, g.name)
        marginSrcName = gd.rightSpaceSourceLabel
        if not gd.fixedRight:
            g.angledRightMargin = int(round(g.angledRightMargin/self.SPACING_UNIT) + value) * self.SPACING_UNIT

    #    A D J U S T  K E R N I N G
    
    def getKerningManager(self, f):
        if f.path:
            if f.path not in self.kerningManagers:
                self.kerningManagers[f.path] = KerningManager(f, sample=self.kerningSample, simT=0.95 ,simSameCategory=False, simSameScript=False, simClip=150) #  First sample will be initialzed, others will be copied
            km = self.kerningManagers[f.path]
            self.kerningSample = km.sample
            return km
        return None

    def _adjustLeftKerning(self, g, value=None, newK=None):
        """ 
        Two ways of usage:
        • value is relative adjustment
        • newK is setting new kerning value.
           
            3 = glyph<-->glyph # Not used
            2 = group<-->glyph
            1 = glyph<-->group
            0 or None = group<-->group
        """
        assert value is not None or newK is not None
        f = g.font
        km = self.getKerningManager(f)
        if self.kernGlyph1 is None:
            return
        k, groupK, kerningType = km.getKerning(self.kernGlyph1, g.name)
        if newK is not None:
            k = newK # Set this value, probably predicted.
        else: # Adjust relative by rounded value
            k = int(round(k/self.KERNING_UNIT))*self.KERNING_UNIT + value * self.KERNING_UNIT
        if not kerningType and self.capLock:
            kerningType = 2 # group<-->glyph
        elif kerningType == 2 and self.capLock:
            kerningType = 3 # glyph<-->glyph 
        km.setKerning(self.kernGlyph1, g.name, k, kerningType)
    
    def _adjustRightKerning(self, g, value=None, newK=None):
        """    
        Two ways of usage:
        • value is relative adjustment
        • newK is setting new kerning value.

            3 = glyph<-->glyph # Not used
            2 = group<-->glyph
            1 = glyph<-->group
            0 or None = group<-->group
        """
        assert value is not None or newK is not None
        f = g.font
        km = self.getKerningManager(f)
        unit = 4
        if self.kernGlyph2 is None:
            return
        k, groupK, kerningType = km.getKerning(g.name, self.kernGlyph2)
        if newK is not None:
            k = newK # Set this value, probably predicted.
        else: # Adjust relative by rounded value
            k = int(round(k/self.KERNING_UNIT))*self.KERNING_UNIT + value * self.KERNING_UNIT
        if not kerningType and self.capLock:
            kerningType = 1 # glyph<-->group
        elif kerningType == 1 and self.capLock:
            kerningType = 3 # glyph<-->glyph
        km.setKerning(g.name, self.kernGlyph2, k, kerningType)

    #    U P D A T I N G 
    
    def update(self, g):
        """Update visuals of the font, setting the attributes of Merz objects."""

# Window measurements
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
C2 = C1 + CW + M
       
class KernNetAssistantController(WindowController):

    assistantGlyphEditorSubscriberClass = KernNetAssistant

    NAME = 'KernNet Kerning Assistant'
    
    def build(self):        

        f = CurrentFont()
        if f is not None: # If there is a current font, then initialize the KerningManager now.
            fLib = getLib(f)
            kerningSampleIndex = fLib.get(KERNING_SAMPLE_SELECT_LIB, 0)
            kerningSampleX = fLib.get(KERNING_SAMPLE_X, -1000)
            print('... Reading kerning select index in f.lib[%s]=%d for %s' % (KERNING_SAMPLE_SELECT_LIB, kerningSampleIndex, f.path.split('/')[-1]))    
        else:
            kerningSampleIndex = 0
            kerningSampleX = -1000

        y = M
        self.w = WindowClass((W, WH), self.NAME, minSize=(W, WH), maxSize=(W, H))

        self.w.showKerningLeftFilled = CheckBox((C0, y, CW, L), 'Show left filled', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningFilled = CheckBox((C1, y, CW, L), 'Show kerning filled', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningRightFilled = CheckBox((C2, y, CW, L), 'Show right filled', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L
        self.w.showKerning = CheckBox((C0, y, CW, L), 'Show kerning', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningBox = CheckBox((C1, y, CW, L), 'Show kerning box', value=False, sizeStyle='small', callback=self.updateEditor)
        y += L
        self.w.showKerningLists = CheckBox((C0, y, CW, L), 'Show kerning lists', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.keysOverview = TextBox((C1, y, 2*CW, 36), 'Navigate: alt + arrows, alt + shift + arrows\nKern: [n][m] [comma][period]', sizeStyle="small")
        y += 24
        self.w.kerningSampleTextLabel = TextBox((C0, y, -M, 24), 'Find kerning pair', sizeStyle="small")
        y += 24
        self.w.kerningGlyph1 = EditText((C0, y, CW, L)) # Use  kerning find button to go there.
        self.w.kerningGlyph2 = EditText((C1, y, CW, L))
        self.w.findKerning = Button((C2, y, CW, L), 'Find pair', callback=self.findKerningSampleCallback)
        y += 32
        self.w.kerningLeftXLabel =  TextBox((C0, y, -M, 24), 'Kerning sample X', sizeStyle="small")
        self.w.kerningSampleSelectLabel =  TextBox((C1, y, -M, 24), 'Kerning sample 0/0 lines', sizeStyle="small") # Range value will be updated
        y += 12
        self.w.kerningLeftX =  Slider((C0, y, CW, 24), minValue=-4000, maxValue=2500, value=kerningSampleX, continuous=True, callback=self.updateEditor)
        self.w.kerningSampleSelectSlider =  Slider((C1, y, CW*2+M, 24), minValue=0, maxValue=486, value=kerningSampleIndex, continuous=True, callback=self.kerningSampleSelectSliderCallback)

        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None

    #    C A L L B A C K S

    def findKerningSampleCallback(self, sender):
        kerningAssistant.findKerningSample(self.w.kerningGlyph1.get(), self.w.kerningGlyph2.get())

    def kerningSampleSelectSliderCallback(self, sender):
        #kerningAssistant.kerningSampleSelect()
        pass
        
    def updateEditor(self, sender):
        # Force updating of the current EditorWindow. Is there a better way to do this directly?
        g = CurrentGlyph()
        #self.groupNameGlyphListCallback1()
        #self.groupNameGlyphListCallback2()
        if g is not None:
            g.changed()
                           
if __name__ == '__main__':
    OpenWindow(KernNetAssistantController)

