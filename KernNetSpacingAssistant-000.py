# -*- coding: UTF-8 -*-
#
#    Template to build Assistants
#    It works on the current font.
#
# 
import sys
import importlib
from math import *
import urllib.request
from AppKit import *

from vanilla import *
import drawBot

from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.events import extractNSEvent

import assistantLib
importlib.reload(assistantLib)

# Decide on the type of window for the Assistant.
#WindowClass = Window # Will hide behind other windows, if not needed.
WindowClass = FloatingWindow # Is always available, but it can block the view of other windows if the Asistant window grows in size.

# Add paths to libs in sibling repositories. The assistantLib module contains generic code for Asistanta.s
PATHS = ['../TYPETR-Assistants/']
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

# Add paths to libs in sibling repositories
PATHS = ['../TYPETR-Assistants/']
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

import assistantLib
importlib.reload(assistantLib)
import assistantLib.kerningSamples
importlib.reload(assistantLib.kerningSamples)
import assistantLib.kerningSamples.ulcwords
importlib.reload(assistantLib.kerningSamples.ulcwords)
import assistantLib.tp_kerningManager
importlib.reload(assistantLib.tp_kerningManager)

from assistantLib.kerningSamples.ulcwords import ULCWORDS
from assistantLib.tp_kerningManager import KerningManager, SPACING_TYPES_LEFT, SPACING_TYPES_RIGHT

VERBOSE = False

W, H = 400, 300
M = 20
BW = 200 - 2*M # Button width
BH = 24 # Button height
FAR = 100000 # Put drawing stuff outside the window
MAX_DIACRITICS = 150

KERN_GLYPH_COLOR = (0, 0, 0, 0.7)

ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]

VISITED_MARKER = (15/256, 180/256, 240/256, 1)

CALIBRATOR = 'H' # Calibrator glyph, that is used on both sides to get standard kerning and spacing.
SYMMETRIC_GLYPHS = (# Valid to calibrate 
    'period', 'quotesingle', 'slash', 'fraction', 'clickdental', 'clicklateral', 
    'Hsmall', 
    'zero', 
    'A', 'H', 'I', 'O', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    'o', 's', 'x', 'v', 'w', 'z', )

class FontData:
    def __init__(self, f):
        """Build X-ref data from the from. Don't store the font itself, as it may be close by the calling application."""
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

assistant = None # Little cheat, to make the assistant available from the window
            
class KernNetSpacingAssistant(Subscriber):

    def build(self):
        global assistant
        assistant = self

        self.isUpdating = False

        self.kerningManagers = {} # Key is f.path, value is KerningManager instance. Will be initialized by self.getKerningSample(f)  
        self.kerningSample = None
        f = CurrentFont()
        if f is not None:
            self.getKerningManager(f) # Initialize self.kerningSample
        
        self.fontDatas = {} # Key is font path, value is FontData instance that holds mined X-ref data on the font.

        glyphEditor = self.getGlyphEditor()
        
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

        #self.glyphEditorGlyphDidChange(info)
        #self.glyphEditorGlyphDidChangeInfo(info)
        #self.glyphEditorGlyphDidChangeOutline(info)
        #self.glyphEditorGlyphDidChangeComponents(info)
        #self.glyphEditorGlyphDidChangeAnchors(info)
        #self.glyphEditorGlyphDidChangeGuidelines(info)
        #self.glyphEditorGlyphDidChangeImage(info)
        #self.glyphEditorGlyphDidChangeMetrics(info)
        #self.glyphEditorGlyphDidChangeContours(info)

    def getFontData(self, f):
        """Answer the cached FontData instance. If it does not exist, create it and let it in mine X-refs from the @f. """
        if not f.path in self.fontDatas:
            self.fontDatas[f.path] = FontData(f)
        return self.fontDatas[f.path]
    
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        self.update(g)
           
    def glyphEditorDidSetGlyph(self, info):
        g = info['glyph']
        #fd = self.getFontData(g.font)
        #print(g.name, fd.components)
        #print('-----', fd.glyphAnchors)
        #print('-----', fd.unicodes)
        if g.markColor != VISITED_MARKER: # NO_MARKER
            g.markColor = VISITED_MARKER

        self.update(g)

    def glyphEditorDidKeyDown(self, info):
        g = info['glyph']
        if VERBOSE:
            print('--- glyphEditorDidKeyDown', g.name) 
                
        event = extractNSEvent(info['NSEvent'])
        characters = event['keyDown']
        #print(event.keys())
        #print(characters)
        
        commandDown = event['commandDown']
        shiftDown = event['shiftDown']
        controlDown = event['controlDown']
        optionDown = event['optionDown']
        self.capLock = event['capLockDown']

        changed = False

        if characters in 'Ee': # Calibration of symmwrix glyphs
            if g.name not in SYMMETRIC_GLYPHS: # Don't do asymmetric glyph this way
                return
            self.calibrate(g) # Update the spacing consistency for all glyphs in left/right kerning = 0.
            changed = True
                                         
        if characters in 'Dd': # Autospace by KernNet
            self.space(g) # Update the spacing consistency for all glyphs in the kerning line
            changed = True
                                         
        #elif characters in 'Hh': # Toggle show frozen
        #    self.controller.w.showFrozenUfo.set(not self.controller.w.showFrozenUfo.get())
        #    self.lastFrozen = None
        #    changed = True
            
        #print('... Key down', info['locationInGlyph'], info['NSEvent'].characters)
        if characters in 'Pp': # Increment right margin
            if shiftDown:
                self._adjustRightMargin(g, 5)
            else:
                self._adjustRightMargin(g, 1)            
            changed = True #|= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            
        elif characters in 'Oo': # Decrement right margin
            if shiftDown:
                self._adjustRightMargin(g, -5)
            else:
                self._adjustRightMargin(g, -1)
            changed = True # |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Ii': # Increment left margin
            if shiftDown:
                self._adjustLeftMargin(g, 5)
            else:
                self._adjustLeftMargin(g, 1)            
            changed = True # |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Uu': # Decrement left margin
            if shiftDown:
                self._adjustLeftMargin(g, -5)
            else:
                self._adjustLeftMargin(g, -1)            
            changed = True # |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line

        # Adjust to predicted kerning
        
        #elif characters == ';': # Set left pair to predicted kerning
        #    self._adjustLeftKerning(g, newK=self.predictedKerning1)
        #    changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        #    updatePreview = True
        
        #elif characters == "'": # Set right pair to predicted kerning
        #    self._adjustRightKerning(g, newK=self.predictedKerning2)
        #    changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        #    updatePreview = True
            
        # Adjust kerning

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
            if VERBOSE:
                print('... Update', g.name)
            self.update(g)

    #    S P A C I N G
    
    def _adjustLeftMargin(self, g, value):
        if self.isUpdating:
            return
        km = self.getKerningManager(g.font)
        unit = 4
        lm = km.getLeftMargin(g) # Margin from dependency
        g1 = km.getLeftMarginGroupBaseGlyph(g) # Margin from group
        # Only if no dependency and no group or g is a group base, then we can alter the margin
        if lm is None and (g1 is None or g1.name == g.name): 
            g.angledleftMargin = int(round(g.angledLeftMargin/unit) + value) * unit
                        
    def _adjustRightMargin(self, g, value):
        if self.isUpdating:
            return
        km = self.getKerningManager(g.font)
        unit = 4
        rm = km.getRightMargin(g) # Margin from dependency
        g2 = km.getRightMarginGroupBaseGlyph(g) # Margin from group
        # Only if no dependency and no group or g is a group base, then we can alter the margin
        if rm is None and (g2 is None or g2.name == g.name): 
            g.angledRightMargin = int(round(g.angledRightMargin/unit) + value) * unit
            
    #    K E R N I N G

    def getKerningManager(self, f):
        if f.path:
            if f.path not in self.kerningManagers:
                self.kerningManagers[f.path] = KerningManager(f, sample=self.kerningSample) #  First sample will be initialzed, others will be copied
            km = self.kerningManagers[f.path]
            self.kerningSample = km.sample
            return km
        return None
        
    def getKerningSample(self, f):
        km = self.getKerningManager(f)
        if km is not None:
            return km.sample
        return ''

    def autoKernAll(self):
        f = CurrentFont()
        km = self.getKerningManager(f)
        km.setKerning('H', 'H', 0)
        for gIndex, gName2 in enumerate(km.sample):
            gName1 = km.sample[gIndex-1]
            k = self.predictKerning(gName1, gName2)
            print(gName1, gName2, k)
            #if gIndex > 20:
            #    break

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
        unit = 4
        if self.kernGlyph1 is None:
            return
        k, groupK, kerningType = km.getKerning(self.kernGlyph1, g.name)
        if newK is not None:
            k = newK # Set this value, probably predicted.
        else: # Adjust relative by rounded value
            k = int(round(k/unit))*unit + value * unit
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
            k = int(round(k/unit))*unit + value * unit
        if not kerningType and self.capLock:
            kerningType = 1 # glyph<-->group
        elif kerningType == 1 and self.capLock:
            kerningType = 3 # glyph<-->glyph
        km.setKerning(g.name, self.kernGlyph2, k, kerningType)


    #    E V E N T
                        
    def update(self, g):
        f = g.font
        self.controller.w.currentGlyph.set(g.name)

        #self.space(g)
        gName1 = self.controller.w.kerningGlyph1.get()
        gName2 = self.controller.w.kerningGlyph2.get()
        if gName1 is not None and gName1 in f and gName2 is not None and gName2 in f:
            k1, k2 = self.predictKerning(gName1, g, gName2)
        
            self.controller.w.kerningGlyph1_mr.set('R'+str(round(f[gName1].angledRightMargin)))
            self.controller.w.kerningGlyph1_k.set('K'+str(round(k1)))
            self.controller.w.currentGlyph_ml.set('L'+str(round(g.angledLeftMargin)))
            self.controller.w.currentGlyph_mr.set('R'+str(round(g.angledRightMargin)))
            self.controller.w.kerningGlyph2_k.set('K'+str(round(k2)))
            self.controller.w.kerningGlyph2_ml.set('L'+str(round(f[gName2].angledLeftMargin)))

        # Enabling buttons
        self.controller.w.calibrateButton.enable(g.name in SYMMETRIC_GLYPHS)

    def calibrate(self, g, margin=500):
        """Calibrate the margins, starting at lm=0 and rm=0, then increase, until the k reaches a local minimum.
        The glyph is supposed to be sumetrics, as the predicted kerning is dived by 2 to get the margins."""
        prevK = 10000 # Start with extreme large.
        if margin is not None:
            g.angledRightMargin = g.angledLeftMargin = margin    
        for m in range(50): # Number of 
            margin = g.angledRightMargin = g.angledLeftMargin
            k1, k2 = self.predictKerning(CALIBRATOR, g, CALIBRATOR, step=1)
            #print('DDDD', margin, k1, k2, prevK)
            g.angledLeftMargin = g.angledRightMargin = margin + k1/2
            if abs(k1) <= 1: #or abs(k1) == abs(prevK):
                break
            prevK = k1
        g.changed()

    #    S P A C I N G  B Y  K E R N N E T
    
    def space(self, g, margin=200, step=1):
        """Try to guess what the margins for @h should be, based on the Similarity groups and on /H/H kerning == 0."""
        H = g.font['H']
        g.angledLeftMargin = g.angledRightMargin = 50 # Start with neuitral value
        
        for n in range(5): # Do some iterations
            k1, k2 = self.predictKerning(CALIBRATOR, g, CALIBRATOR, step=step)
            print(k1, k2)
            g.angledLeftMargin += k1 # Correct the margins by the amount of predicted kerning it would need.
            g.angledRightMargin += k2
            if g.angledLeftMargin <= 0 or g.angledRightMargin <= 0:
                break
            if abs(k1) <= 2 and abs(k2) <= 2:
                break
        g.changed()

    #    K E R N N E T
             
    def predictKerning(self, gName1, g, gName2, step=None):
        k1 = k2 = 0
        f = g.font
        if gName1 and gName1 in f:
            g1 = f[gName1]
            k1 = self.getKernNetKerning(g1, g, step=step)
            self.kernGlyphImage1.setPath(g1.getRepresentation("merz.CGPath"))
            self.kernGlyphImage1.setPosition((-g1.width - k1, 0))
        else:
            self.kernGlyphImage1.setPosition((FAR, 0))
                        
        self.kernGlyphImage.setPath(g.getRepresentation("merz.CGPath"))
        self.kernGlyphImage.setPosition((0, 0))

        if gName2 and gName2 in f:
            g2 = f[gName2]
            k2 = self.getKernNetKerning(g, g2, step=step)
            self.kernGlyphImage2.setPath(g2.getRepresentation("merz.CGPath"))
            self.kernGlyphImage2.setPosition((g.width + k1, 0))
        else:
            self.kernGlyphImage2.setPosition((FAR, 0))

        y4 = -150 # Position of current kerning values

        if k1 < 0:
            kernColor = 1, 0, 0, 1
        if k1 > 0:
            kernColor = 0, 0.5, 0, 1
        else:
            kernColor = 0.6, 0.6, 0.6, 1
        self.kerning1Value.setFillColor(kernColor)
        self.kerning1Value.setPosition((k1, y4))
        self.kerning1Value.setText(f'{k1}')
            
        if k2 < 0:
            kernColor = 1, 0, 0, 1
        if k2 > 0:
            kernColor = 0, 0.5, 0, 1
        else:
            kernColor = 0.6, 0.6, 0.6, 1
        self.kerning2Value.setFillColor(kernColor)
        self.kerning2Value.setPosition((g.width + k2, y4))        
        self.kerning2Value.setText(f'{k2}')
        
        return k1, k2
        
    #FACTOR = 0.8
    #FACTOR = 1.4
    UNIT = 2
    
    def getKernNetKerning(self, g1, g2, step=None):
        """Gernerate the kerning test image.
        Answer the KernNet predicted kerning for @g1 amd @g2. This assumes the KernNet server to be running on localhost:8080"""
        if step is None:
            step = self.UNIT
        f = g1.font
        imageName = 'test.png'
        kernImagePath = '/'.join(__file__.split('/')[:-1]) + '/assistantLib/kernnet6/_imagePredict/' + imageName
        iw = ih = 32
        scale = ih/f.info.unitsPerEm
        y = -f.info.descender 

        if 'Italic' in f.path:
            italicOffset = -50 # Calibrate HH shows in the middle
        else:
            italicOffset = 0
            
        im1 = g1.getRepresentation("defconAppKit.NSBezierPath")
        im2 = g2.getRepresentation("defconAppKit.NSBezierPath")
        s = iw / g1.font.info.unitsPerEm
        y = -g1.font.info.descender

        #if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
        drawBot.newDrawing()
        drawBot.newPage(iw, ih)
        
        #drawBot.fill(1, 0, 0, 1)
        #drawBot.rect(0, 0, iw, ih)
        drawBot.fill(0)
        drawBot.scale(s, s)
        drawBot.save()
        drawBot.translate(iw/s/2 - g1.width + italicOffset, y)
        drawBot.drawPath(im1)
        drawBot.restore()
        drawBot.save()
        drawBot.translate(iw/s/2 + italicOffset, y)
        drawBot.drawPath(im2)
        drawBot.restore()
        
        # If flag is set, clip space above capHeight and below baseline
        if self.controller.w.cropKernImage.get():
            drawBot.fill(1, 0, 0, 1)
            drawBot.rect(0, f.info.capHeight+600, iw/s, ih/s)
            drawBot.fill(0, 0, 1, 1)
            drawBot.rect(0, -ih/s, iw/s, ih/s-300)
            
        drawBot.saveImage(kernImagePath)

        page = urllib.request.urlopen(f'http://localhost:8080/{g1.name}/{g2.name}/{imageName}')
        
        # Returns value is glyphName1/glyphName2/predictedKerningValue
        # The glyph names are returned to check validity of the kerning value.
        # Since the call is ansynchronic to the server, we may get the answer here from a previous query.
        parts = str(page.read())[2:-1].split('/')
        if not len(parts) == 3 or parts[0] != g1.name or parts[1] != g2.name:
            print('### Predicted kerning query not value', parts)
            return None
        try:
            factor = float(self.controller.w.factor.get())
        except ValueError:
            factor = 1
            
        k = float(parts[-1])
        #print(k, k - abs(factor * k), abs(factor * k), int(round(k * f.info.unitsPerEm/1000/step))*step)
        k = k * factor
        
        # Calculate the rouned-truncated value of the floating         
        ki = int(round(k * f.info.unitsPerEm/1000/step))*step # Scale the kerning value to our Em-size.  
        if abs(ki) <= step:
            ki = 0 # Apply threshold for very small kerning values
        print(f'... Predicted kerning {g1.name} -- {g2.name} k={k} kk={ki}')
            
        return ki
        
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
C2 = C1 + CW + M

class KernNetSpacingAssistantController(WindowController):

    assistantGlyphEditorSubscriberClass = KernNetSpacingAssistant
    
    NAME = 'KernNet Assistant'

    def build(self):        

        f = CurrentFont()
        
        tbw = 5 * M
        
        y = M
        self.w = WindowClass((450, 50, W, H), self.NAME, minSize=(W, H))

        self.w.kerningGlyph1 = EditText((C0, y, CW, L), callback=self.updateKerningCallback) # Use  kerning find button to go there.
        self.w.currentGlyph = TextBox((C1, y, CW, L), '')
        self.w.kerningGlyph2 = EditText((C2, y, CW, L), callback=self.updateKerningCallback)
        self.w.kerningGlyph1.set('H')
        self.w.kerningGlyph2.set('H')

        y += L
        self.w.kerningGlyph1_mr = TextBox((C1-1.5*tbw, y, tbw, L), '0')
        self.w.kerningGlyph1_k = TextBox((C1-tbw/2, y, tbw, L), '0')
        self.w.currentGlyph_ml = TextBox((C1+tbw/2, y, tbw, L), '0')
        self.w.currentGlyph_mr = TextBox((C2-1.5*tbw, y, tbw, L), '0')
        self.w.kerningGlyph2_k = TextBox((C2-tbw/2, y, tbw, L), '0')
        self.w.kerningGlyph2_ml = TextBox((C2+tbw/2, y, tbw, L), '0')
        
        y += 2*L
        self.w.factor = EditText((C0, y, CW, L), callback=self.updateKerningCallback) # Use  kerning find button to go there.
        self.w.factor.set('1.4')

        self.w.cropKernImage = CheckBox((C2, y, CW, L), 'Crop kern image', value=True, callback=self.updateKerningCallback)
        
        y = H - M - BH
        self.w.calibrateButton = Button((M, y, CW, BH), 'Calibrate', callback=self.calibrateButtonCallback)
        self.w.spaceButton = Button((C1, y, CW, BH), 'Space', callback=self.spaceButtonCallback)
        
        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None
                           
    def updateKerningCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            g.changed()
            
    def calibrateButtonCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            assistant.calibrate(g)
            
    def spaceButtonCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            assistant.space(g)
            
if __name__ == '__main__':
    OpenWindow(KernNetSpacingAssistantController)
