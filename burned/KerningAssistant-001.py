# -*- coding: UTF-8 -*-
#
#    Kerning Assistant for RoboFont4
#    It works on the current font.
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

import sys
import os
import codecs
import vanilla
import merz
import weakref
import importlib
from random import choice
from copy import copy
from math import *
from AppKit import *
import drawBot

from mojo.events import extractNSEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

from fontTools.misc.transform import Transform

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/', '../TYPETR-Segoe-UI/')
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

# Importing Similarity for grouping & spacing
import cosineSimilarity
# Importing KernNet for AI assistent kerning
#import torch
#from assistantLib.kernnet.predictKernNetModel import predict_kern_value

import assistantLib
importlib.reload(assistantLib)
import assistantLib.kerningSamples
importlib.reload(assistantLib.kerningSamples)
import assistantLib.kerningSamples.ulcwords
importlib.reload(assistantLib.kerningSamples.ulcwords)
import assistantLib.tp_kerningManager
importlib.reload(assistantLib.tp_kerningManager)

from assistantLib.kerningSamples.ulcwords import ULCWORDS
from assistantLib.tp_kerningManager import KerningManager



ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]
FUNCTION_KEYS = (
    'Uu', # Decrement left margin
    'Ii', # Increment left margin
    'Oo', # Decrement right margin
    'Pp', # Increment right margin
    'Nn', # Increment left kerning
    'Mm', # Decrement left kerning
    '.<', # Decrement right kerning
    ',>', # Increment right kerning
)

VERBOSE = False
VERBOSE2 = False

KERNING_SAMPLE_SELECT_LIB = 'TYPETR-Presti-Assistant-KerningSampleIndex'
KERNING_SAMPLE_X = 'TYPETR-Presti-Assistant-KerningSampleX'

GROUPGLYPH_COLOR = (0, 0, 0.6, 1)
GLYPHGLYPH_COLOR = (0, 0.4, 0, 1)

# Initial template string. The /? gets replaced by the unicode of the current glyph.
# Replace /??W by random word

SAMPLES = (
    # Force to capitals [clig] trigger
    ' /?A/?B/?C/?D/?E/?F/?G/?H/?I/?J/?K/?L/?M/?N/?O/?P/?Q/?R/?S/?T/?U/?V/?W/?X/?Y/?Z/?',
    ' /?a/?b/?c/?d/?e/?f/?g/?h/?i/?j/?k/?l/?m/?n/?o/?p/?q/?r/?s/?t/?u/?v/?w/?x/?y/?z/?',
    ' A/? B/? C/? D/? E/? F/? G/? H/? I/? J/? K/? L/? M/? N/? O/? P/? Q/? R/? S/? T/? U/? V/? W/? X/? Y/? Z/?',
    ' a/? b/? c/? d/? e/? f/? g/? h/? i/? j/? k/? l/? m/? n/? o/? p/? q/? r/? s/? t/? u/? v/? w/? x/? y/? z/?',
    ' I/?~T1~B1 I/?~mlu1~mru1 I/?~mld1~mrd1 I/?~tlu1~tru1 I/?~tld1~trd1 I/?~bld1~brd1 I/?~blu1~bru1 I/?io/?on/?n Hamburgefons/?tiv H/?HAMBURG/?RGER',

    '/??d /??W /??K /?I/?IO/?H/?i/?io/?on/?n ',
    '/??d /??K /??W /?I/?IO/?H/?i/?io/?on/?n ',
    '/??d I/?IO/?H/?i/?io/?on/?n /?/??W/?Hamburgefonstiv',
    '/??d I/?IO/?H/?i/?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',

    ' /?~T1~B1 /?~mlu1~mru1 /?~mld1~mrd1 /?~tlu1~tru1 /?~tld1~trd1 /?~bld1~brd1 /?~blu1~bru1 /?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    ' /?~T2~B2 /?~mlu2~mru2 /?~mld2~mrd2 /?~tlu2~tru2 /?~tld2~trd2 /?~bld2~brd2 /?~blu2~bru2 /?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    ' /?~T3~B3 /?~mlu3~mru3 /?~mld3~mrd3 /?~tlu3~tru3 /?~tld3~trd3 /?~bld3~brd3 /?~blu3~bru3 /?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    ' /?~T4~B4 /?~mlu4~mru4 /?~mld4~mrd4 /?~tlu4~tru4 /?~tld4~trd4 /?~bld4~brd4 /?~blu4~bru4 /?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    ' /?~T5~B5 /?~mlu5~mru5 /?~mld5~mrd5 /?~tlu5~tru5 /?~tld5~trd5 /?~bld5~brd5 /?~blu5~bru5 /?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    ' /?~T1~B1 I/?~mlu1~mru1IO/?~tlu1~tru1H/?~bld1~brd1i/?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    ' /?~tlu1~tru1~mlu1~mru1~bld1~brd1~T1~B1 I/?IO/?H/?i/?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    'I/?IO/?H/?i/?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?RGER',
    '0/?1/?2/?3/?4/?5/?6/?7/?8/?9/?0/?H/?HO/?O/?n/?o/?Hamburg',
    '0/?/0 1/?/0 2/?/0 3/?/0 4/?/0 5/?/0 6/?/0 7/?/0 8/?/0 9/?/0 0//?0 1//?0 2//?0 3//?0 4//?0 5//?0 6//?0 7//?0 8//?0 9//?0 Hamburg',
    'A/?AH/?HO/?OV/?Va/?ai/?io/?ov/?v',
    'A/?Æ/?B/?C/?D/?E/?F/?G/?H/?I/?J/?K/?L/?M/?N/?O/?Ø/?Œ/?P/?Q/?R/?S/?T/?U/?V/?W/?X/?Y/?Z/?',
    'A/?Á/?Ä/?Æ/?B/?C/?Ç/?D/?E/?É/?F/?G/?H/?I/?J/?K/?L/?M/?N/?O/?Ø/?Œ/?P/?Q/?R/?S/?T/?U/?V/?W/?X/?Y/?Z/?',
    'I/?IO/?H/?i/?io/?on/?n Hamburgefons/?tiv/?HAMBURG/?',
    'a/?æ/?b/?c/?d/?e/?f/?g/?h/?i/?j/?k/?l/?m/?n/?o/?ø/?œ/?p/?q/?r/?s/?t/?u/?v/?w/?x/?y/?z/?',
    'f/?fiflftfnfmfufhfkflfbffifflfafàfáfâfãfäfåfāfăfąfǻfæfǽfefèféfêfëfēfĕfėfęfěfufùfúfûfüfũfūfŭfůfűfofòfófôfõföfōfŏfőføfǿfifìfífîfïfĩfīfĭfįfĳ/? Hamburgefons',
    'point. points de suspension… point-virgule; deux-points: point d’exclamation! apostrophe’ virgule, {accolades} (parenthèses) <chevrons> [crochets] «guillemets» ou “hey” ou ‘ho’ ou “ha„ ou ‘hé‚ ou ‹hi› barre oblique/ slash/ barre oblique inversée\\ barre verticale| verticale brisée¦ point médian· point d’interrogation? ¡espagnol! ¿espagnol? trait d’union- tiret n dash– ou m dash— -–—',
    'ďaďáďkďmďnďoďsďtďuďžđďiďjď!ľ?ľ!ľiľjť?ť!ťiťj',
    """A'A"A‘A“A 7.7 F.OF.TF.UF.VF.YF.“F.’ P.OP.TP.UP.VP.YP.“P.’ T.OT.T.UT.VT.YT.“T.’ U.OU.TU.UU.VU.YU.“U.’ V.V.OV.TV.UV.YV.“V.’ Y.OY.TY.UY.VY.YY.“Y.’  """,
    'l.’nn.” “nn,” “nn”. “nn”, r.” v.” w.” y.” F.” P.” T.” V.” W.” Y.”',
    'loďka ďábelska ďatlov ďábel objížďka buďto  Nunatuĸavut',
    'břeťa cenťák žesťový řiťka opúšťať hradišťský tchaj-ťi šťuka dvanásťročný',
    'ď.ď,ď:ď;ď?ď!ď”ď“ď™ď®ď)ď}ď]ť.ť,ť;ť:ť?ť!ť”ť“ť™ť®ť)ť}ť]ľ.ľ,ľ:ľ;ľ?ľ!ľ”ľ“ľ™ľ®ľ)ľ}ľ]',
    'ïlïbïkïl"ī"/ī/\\ī\\(ī)[ī]{ī}ïlïbïkïl"ï"/ï/\\ï\\(ï)[ï]{ï}fífìfîfïfīffĩfíffìffîffïffīffĩfþ',
    'fît(French), fìsica(Corsican), fīča(Latvian), ffïon(Welsh)',
    'L‌̧l‌̧M̧ajelm̧N‌̧n‌̧O̧o̧ĀāN̄n̄ŌōŪūĄąĄ́ą́ĘęĘ́ę́ĮįĮ́į́ǪǫǪ́ǫ́G̃g̃',
    'hradišťský tchaj-ťi šťuka aukščiausiųjų',
)    

# ULCWORDS has list of words

W, H = 400, 500
M = 32
SPACE_MARKER_R = 16
POINT_MARKER_R = 6
FAR = 100000 # Put drawing stuff outside the window
KERN_LINE_SIZE = 32 # Number of glyphs on kerning line
KERN_SCALE = 0.15 #0.2

INTERPOLATION_ERROR_MARKER = (1, 0, 0, 1)
NO_MARKER = (1, 1, 1, 1)
#VISITED_MARKER = (0, 0.5, 0.5, 0.5)
if __file__.startswith('/Users/petr/Desktop/TYPETR-git'):
    VISITED_MARKER = 40/255, 120/255, 255/255, 1 # "Final" marker Blue (for others)
    print('Using Petr color')
else:
    VISITED_MARKER = 92/255, 149/255, 190/255, 1 # "Final" marker (for Petr)
    print('Using Tilmann/Graeme color')

#KERNING = KERNING_START + KERNING # Basic set, as used for Segoe, without feature glyphs
#KERNING = KERNING_START + KERNING_SIMPLE # Relatively small samplt with only one glyph per group
#KerningSample = KERNING
# Total number of kerning lines in this sample
KerningNumLines = KERNING_NUM_LINES = int(round(KERN_LINE_SIZE / KERN_LINE_SIZE))

WindowClass = vanilla.Window
#WindowClass = vanilla.FloatingWindow
            
kerningAssistant = None # Little cheat, to make the assistant available from the window

class KerningAssistant(Subscriber):

    debug = True
    
    controller = None
    
    #    B U I L D I N G
    
    def build(self):
        global kerningAssistant
        kerningAssistant = self

        self.kerningManagers = {} # Key is f.path, value is KerningManager instance. Will be initialized by self.getKerningSample(f)  
        self.kerningSample = None
        f = CurrentFont()
        if f is not None:
            self.getKerningManager(f) # Initialize self.kerningSample
                  
        self.capLock = False # Used for creating glyph/group or group/glyph or glyph/glyph kerning (showing in blue and green)
        
        self.isUpdating = False
        self.fixingAnchors = False
        
        # Store selected glyphs for (kern1, kern2) if the preview char changed value
        #self.previewKern1 = self.previewKern2 = None

        self.mouseClickPoint = None
        self.mouseDraggedPoint = None
        
        # Currently dragging this terminal
        self.selectedTerminal = None
        self.terminals = [] # Updated but self.draw with the terminal-data found

        self._dValues = None # Caching diagonal values from Dimensioneer glyph analyzer.
                
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

        self.kernGlyph1 = None # Name of glyph on left side, if kerning is on
        self.kernGlyph2 = None # Name of glyph on right side, if kerning is on
        self.groupTextLayer_colW = colW = 400 
        colH = 750
        # Showing the left and groups of the current glyp
        self.group1TextLeftLayer = container.appendTextBoxSublayer(name="group1Left",
            position=(FAR, 0), # Will be changed to width of current glyph
            backgroundColor=(1, 1, 1, 0.5),
            text='Group1-Left',
            size=(colW, colH),
            font='Courier',
            pointSize=14,
            lineHeight=18,
            fillColor=(0, 0, 0, 1),
        )
        self.group2TextLeftLayer = container.appendTextBoxSublayer(name="group2Left",
            position=(FAR, 0), # Will be changed to width of current glyph
            backgroundColor=(1, 1, 1, 0.5),
            text='Group2-Left',
            size=(colW, colH),
            font='Courier',
            pointSize=14,
            lineHeight=18,
            fillColor=(0, 0, 0, 1),
        )
        self.group1TextRightLayer = container.appendTextBoxSublayer(name="group1Right",
            position=(FAR, 0), # Will be changed to width of current glyph
            backgroundColor=(1, 1, 1, 0.5),
            text='Group1-Right',
            size=(colW, colH),
            font='Courier',
            pointSize=14,
            lineHeight=18,
            fillColor=(0, 0, 0, 1),
        )
        self.group2TextRightLayer = container.appendTextBoxSublayer(name="group2Right",
            position=(FAR, 0), # Will be changed to width of current glyph
            backgroundColor=(1, 1, 1, 0.5),
            text='Group2-Right',
            size=(colW, colH),
            font='Courier',
            pointSize=14,
            lineHeight=18,
            fillColor=(0, 0, 0, 1),
        )

        self.fixedSpaceMarkerLeft = container.appendOvalSublayer(name="spaceMarkerLeft",
            position=(-SPACE_MARKER_R, -SPACE_MARKER_R),
            size=(SPACE_MARKER_R*2, SPACE_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.leftSpaceSourceLabel = container.appendTextLineSublayer(name="leftSpaceSourceLabel",
            position=(FAR, -SPACE_MARKER_R*1.5),
            text='LSB',
            font='Courier',
            pointSize=14,
            fillColor=(0, 0, 0, 1),
        )
        self.leftSpaceSourceLabel.setHorizontalAlignment('center')
        
        self.fixedSpaceMarkerRight = container.appendOvalSublayer(name="spaceMarkerRight",
            position=(1000-SPACE_MARKER_R, -SPACE_MARKER_R),
            size=(SPACE_MARKER_R*2, SPACE_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.rightSpaceSourceLabel = container.appendTextLineSublayer(name="rightSpaceSourceLabel",
            position=(1000, -SPACE_MARKER_R*1.5),
            text='RSB',
            font='Courier',
            pointSize=14,
            fillColor=(0, 0, 0, 1),
        )
        self.rightSpaceSourceLabel.setHorizontalAlignment('center')
                  
        # Kerning
        
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
            name="kerning1Value",
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
        self.kernGlyphImage1 = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage1',
            position=(FAR, 0),
            fillColor=(0, 0, 0, 1),
        )
        self.kernGlyphImage = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage',
            position=(FAR, 0),
            fillColor=(0, 0, 0, 1),
        )
        self.kernGlyphImage2 = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage2',
            position=(FAR, 0),
            fillColor=(0, 0, 0, 1),
        )

        
        #    E V E N T S
        
    def started(self):
        self.sampleText = None # Initialize sample text storage for FontGoggles file.
        self.randomWord = choice(ULCWORDS)
        #print("subscription started")
        #self.controller.addInfo("subscription started")        
    
    def destroy(self):
        #print("stop subscription")
        self.foregroundContainer.clearSublayers()
        #self.controller.addInfo("stop subscription")
    
    def predictKerning(self, gName1, gName2):
        f = CurrentFont()            
        imageName = 'test.png'
        kernImagePath = '/'.join(__file__.split('/')[:-1]) + '/assistantLib/kernnet/_imagePredict/' + imageName
        W = H = 32
        R = 12
        R2 = 2*R
        scale = H/f.info.unitsPerEm
        y = -f.info.descender 

        drawBot.newDrawing()
        drawBot.newPage(W, H)
        drawBot.fill(0)
        
        drawBot.scale(scale)
        drawBot.save()

        g1 = f[gName1]
        path1 = g1.getRepresentation("defconAppKit.NSBezierPath")
        drawBot.translate(W/2/scale-g1.width, y)
        drawBot.drawPath(path1)
        drawBot.restore()        

        g2 = f[gName2]
        path2 = g2.getRepresentation("defconAppKit.NSBezierPath")
        drawBot.translate(W/2/scale, y)
        drawBot.drawPath(path2)

        drawBot.saveImage(kernImagePath)
        
        import urllib.request
        page = urllib.request.urlopen('http://localhost:8080/' + imageName)
        
        CALIBRATE = 0
        
        return int(str(page.read())[2:-1]) + CALIBRATE     
                                
    def glyphEditorDidSetGlyph(self, info):
        #self.backgroundContainer.clearSublayers()
        #self.foregroundContainer.clearSublayers()
        g = info["glyph"]
        if g is None:
            self.controller.w.setTitle('Kerning Assistant')
            return
        f = g.font
        if VERBOSE:
            print('--- glyphEditorDidSetGlyph', g.name)
        
        # Unselect points to avoid moving them on kerning-cursor keys
        if 0:
            for contour in g.contours:
                for p in contour.points:
                    p.selected = False
            for component in g.components:
                component.selected = False

        # Set controller groups names for current glyph
        km = self.getKerningManager(f)
        sample = km.sample
        cursor = int(round(self.controller.w.kerningSampleSelectSlider.get())) + 16
        gName1 = km.sample[cursor-1]
        gName2 = km.sample[cursor+1]

        k1 = k2 = 0
        k1 = self.predictKerning(gName1, g.name)
        k2 = self.predictKerning(g.name, gName2)
        print((gName1, g.name), k1, (g.name, gName2), k2)
        

        simGroups2 = km.getSimilarGroups2(g)
        simGroups1 = km.getSimilarGroups1(g)
        self.controller.w.groupNameList2.set(sorted(simGroups2.keys()))
        self.controller.w.groupNameList1.set(sorted(simGroups1.keys()))

        # Left side of glyph
        groupName2 = km.glyphName2GroupName2.get(g.name)
        if groupName2 is not None:
            label2 = f'{groupName2} ({len(f.groups[groupName2])})'
        else:
            label2 = '---'
        self.controller.w.groupName2.set(label2) # Left side of the current glyph                

        # Right side of glyph
        groupName1 = km.glyphName2GroupName1.get(g.name)
        if groupName1 is not None:
            label1 = f'{groupName1} ({len(f.groups[groupName1])})'
        else:
            label1 = '---'
        self.controller.w.groupName1.set(label1) # Right side of the current glyph

        self.controller.w.setTitle(f'Kerning Assistant /{g.name}')

        self.updateGlyph(g)
        #self.glyphEditorGlyphDidChange(info)
        #self.glyphEditorGlyphDidChangeInfo(info)
        #self.glyphEditorGlyphDidChangeOutline(info)
        #self.glyphEditorGlyphDidChangeComponents(info)
        #self.glyphEditorGlyphDidChangeAnchors(info)
        #self.glyphEditorGlyphDidChangeGuidelines(info)
        #self.glyphEditorGlyphDidChangeImage(info)
        #self.glyphEditorGlyphDidChangeMetrics(info)
        #self.glyphEditorGlyphDidChangeContours(info)

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
        updatePreview = False
                             
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
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
            
        elif characters in 'Oo': # Decrement right margin
            if shiftDown:
                self._adjustRightMargin(g, -5)
            else:
                self._adjustRightMargin(g, -1)
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
        
        elif characters in 'Ii': # Increment left margin
            if shiftDown:
                self._adjustLeftMargin(g, 5)
            else:
                self._adjustLeftMargin(g, 1)            
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
        
        elif characters in 'Uu': # Decrement left margin
            if shiftDown:
                self._adjustLeftMargin(g, -5)
            else:
                self._adjustLeftMargin(g, -1)            
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True

        # Adjust kerning

        elif characters in '.>': # Increment right kerning
            if shiftDown:
                self._adjustRightKerning(g, 5) # 20
            else:
                self._adjustRightKerning(g, 1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
        
        elif characters in ',<': # Decrement right kerning
            if shiftDown:
                self._adjustRightKerning(g, -5) # 20
            else:
                self._adjustRightKerning(g, -1) # 4
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
        
        elif characters in 'Mm': # Decrement left kerning
            if shiftDown:
                self._adjustLeftKerning(g, -5) # 20
            else:
                self._adjustLeftKerning(g, -1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
        
        elif characters in 'Nn': # Increment left kerning
            if shiftDown:
                self._adjustLeftKerning(g, 5) # 20
            else:
                self._adjustLeftKerning(g, 1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True

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
            updatePreview = True
                 
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
            updatePreview = True
        
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
            #self.saveKerningCursor()
            updatePreview = True
        
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
            #self.saveKerningCursor()
            updatePreview = True
        
        if changed:
            if VERBOSE:
                print('... Update', g.name)
            self.updateGlyph(g)
        if updatePreview:
            #print('Preview key down', g.name)
            self.updatePreview(g)

    def saveKerningCursor(self):
        f = CurrentFont() # Only save the current kerning cursor in the curren font
        kerningSampleIndex = self.controller.w.kerningSampleSelectSlider.get()
        if f.lib.get(KERNING_SAMPLE_SELECT_LIB) != kerningSampleIndex:
            #print('... Saving kerning select index %d (%d) in f.lib[%s]=%d for %s' % (kerningSampleIndex, kerningSampleIndex/KERN_LINE_SIZE, KERNING_SAMPLE_SELECT_LIB, kerningSampleIndex, f.path.split('/')[-1]))
            f.lib[KERNING_SAMPLE_SELECT_LIB] = kerningSampleIndex
            f.lib[KERNING_SAMPLE_X] = self.controller.w.kerningLeftX.get()

    def glyphEditorDidMouseDown(self, info):
        #event = extractNSEvent(info['NSEvent'])
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorDidMouseDown', g.name)
        
        g.prepareUndo()
        self.selectedTerminal = None
        self.mouseClickPoint = p = info['locationInGlyph']
        for terminal in self.terminals:
            ox, oy = terminal['anchor']
            if ox-5 <= p.x <= ox+5 and oy-5 <= p.y <= oy+5:
                self.selectedTerminal = terminal
                break
        # Check on anchors
        #if self.controller.w.fixAnchors.get() and gd.fixAnchors:
        #    self.fixAnchors(g)
            
        #self.showFrozen(g)
        #self.showItalicRoman(g)
        #print('... Mouse down', info['locationInGlyph'], info['NSEvent'])
    
    def glyphEditorDidMouseUp(self, info):
        # Reset terminal stuff
        if VERBOSE:
            print('--- glyphEditorDidMouseDown', info['glyph'].name)
        self.selectedTerminal = None
        self.mouseClickPoint = None
        self.mouseDraggedPoint = None
        #print('... Mouse up', info['locationInGlyph'], info['NSEvent'])
    
    def glyphEditorDidMouseMove(self, info):
        pass
        #print('... Mouse move', info['locationInGlyph'], info['NSEvent'])
    
    def glyphEditorDidMouseDrag(self, info):
        g = info['glyph']
        #if VERBOSE:
        #    print('--- glyphEditorDidMouseDrag-RETURN', g.name)
     
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChange', g.name)

    def glyphEditorGlyphDidChangeInfo(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeInfo', g.name)
             
    def glyphEditorGlyphDidChangeOutline(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeOutline', g.name)
        self.updateGlyph(g)
            
    def glyphEditorGlyphDidChangeContours(self, info):
        """Event also calls glyphEditorGlyphDidChangeOutline"""
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeContours', g.name)        
        self.updateGlyph(g)
             
    def glyphEditorGlyphDidChangeComponents(self, info):
        """Event also calls glyphEditorGlyphDidChangeOutline"""
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeComponents', g.name)
        self.updateGlyph(g)
             
    def glyphEditorGlyphDidChangeAnchors(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeAnchors', g.name)
        self.updateGlyph(g)

    #def glyphEditorGlyphDidChangeSelection(self, info):
    #    g = info['glyph']
    #    if g is None:
    #        return
    #    #if VERBOSE:
    #    print('--- glyphEditorGlyphDidChangeSelection', g.name)
 
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
                
    #    S P A C I N G
    
    def _adjustLeftMargin(self, g, value):
        if self.isUpdating:
            return
        f = g.font
        unit = 4
        gd = getGlyphData(f, g.name)
        marginSrcName = gd.leftSpaceSourceLabel
        if not gd.fixedLeft:
            #self.isUpdating = True
            g.angledLeftMargin = int(round(g.angledLeftMargin/unit) + value) * unit
            #self.isUpdating = False
                        
    def _adjustRightMargin(self, g, value):
        if self.isUpdating:
            return
        f = g.font
        unit = 4
        gd = getGlyphData(f, g.name)
        marginSrcName = gd.rightSpaceSourceLabel
        if not gd.fixedRight:
            #self.isUpdating = True
            g.angledRightMargin = int(round(g.angledRightMargin/unit) + value) * unit
            #self.isUpdating = False

    def _adjustLeftKerning(self, g, value):
        """    
            3 = glyph<-->glyph # Not used
            2 = group<-->glyph
            1 = glyph<-->group
            0 or None = group<-->group
        """
        f = g.font
        km = self.getKerningManager(f)
        unit = 4
        if self.kernGlyph1 is None:
            return
        k, groupK, kerningType = km.getKerning(self.kernGlyph1, g.name)
        k = int(round(k/unit))*unit + value * unit
        if not kerningType and self.capLock:
            kerningType = 2 # group<-->glyph
        elif kerningType == 2 and self.capLock:
            kerningType = 3 # glyph<-->glyph 
        km.setKerning(self.kernGlyph1, g.name, k, kerningType)
                                        
    def _adjustRightKerning(self, g, value):
        """    
            3 = glyph<-->glyph # Not used
            2 = group<-->glyph
            1 = glyph<-->group
            0 or None = group<-->group
        """
        f = g.font
        km = self.getKerningManager(f)
        unit = 4
        if self.kernGlyph2 is None:
            return
        k, groupK, kerningType = km.getKerning(g.name, self.kernGlyph2)
        k = int(round(k/unit))*unit + value * unit
        if not kerningType and self.capLock:
            kerningType = 1 # glyph<-->group
        elif kerningType == 1 and self.capLock:
            kerningType = 3 # glyph<-->glyph
        km.setKerning(g.name, self.kernGlyph2, k, kerningType)

            
    def updateGlyph(self, g):
        """Figure out what needs to be done with this of glyph.
        """
        if VERBOSE2:
            print('@@@ updateGlyph', g.name)
        
        if self.controller is None: # In case no longer available
            return
        if self.isUpdating:
            return
        self.isUpdating = True
        
        #print('Preview updateGlyph', g.name)
        self.updatePreview(g)
        
        self.isUpdating = False
                         
    def updateSampleText(self, md):
        """
        current Sample == sampleText != popup:  Popup changed
        current Sample != sampleText != popup:  Sample text change manually
            
        """
        g = CurrentGlyph()
        if VERBOSE2:
            print('@@@ updateSampleText', g.name)
        
        if g is not None: # FontGoggles can only show characters with unicode. Stylistic sets will show alternatives.
            if g.name.startswith('.'):
                return
            baseName = g.name.split('.')[0]
            f = g.font
            if baseName in f:
                g = f[baseName]
                gd = getGlyphData(f, g.name)
                if gd is not None and gd.c:
                    font = g.font # Get the font to know where to write the file
                    # Get the path of the current font and calculate the output file path local to it.
                    path = '/'.join(font.path.split('/')[:-1]) + '/' + SAMPLE_FILE_NAME
                    currentCursor = int(round(self.controller.w.kerningSampleSelectSlider.get())) # Show number of sample cursor in line
                    kerningSample = self.getKerningSample(f)
                    kSample = ''
                    for gName in kerningSample[currentCursor:int(currentCursor + KERN_LINE_SIZE)]:
                        gds = getGlyphData(f, gName)
                        if gds is not None:
                            c = gds.c
                            if '.sc' in gName:
                                gName = gName.replace('.sc', '')
                                kSample += (getGlyphData(f, gName).c or '').lower()
                            else:
                                gName = gName.replace('.uc', '')
                                kSample += getGlyphData(f, gName).c or ''
                        else:
                            print('### Cannot find glyph data for', gName)
                    
                    ggSsample = self.controller.w.sampleText.get().replace('/??d', str(int(currentCursor/KERN_LINE_SIZE))).replace('/??K', kSample).replace('/??W', self.randomWord).replace('/?', gd.c) # Get the sample and replace pattern /?
                    if self.sampleText != ggSsample:
                        self.sampleText = ggSsample
                        #print('... Write FontGoggles sample', path, sample)
                        f = codecs.open(path, 'w', encoding='utf-8') # Open file, for unicode/UTF-8
                        f.write(ggSsample) 
                        f.close()

    #    F I N D
    
    def findKerningSample(self, kerningGlyph1, kerningGlyph2=''):
        prev = None
        f = CurrentFont()
        km = kerningAssistant.getKerningManager(f)
        # Find the pair in the kerning sample and set the cursor there. 
        if kerningGlyph1 not in f: # Typed char instead of glyph name?
            kerningGlyph1 = km.uni2glyphName.get(kerningGlyph1)

        if kerningGlyph2 and kerningGlyph2 not in f: # Typed char instead of glyph name?
            kerningGlyph2 = km.uni2glyphName.get(kerningGlyph1)
        
        if kerningGlyph2:
            print(f'... Searching for /{kerningGlyph1}, /{kerningGlyph2}' % (kerningGlyph1, kerningGlyph2))  
        else:
            print(f'... Searching for /{kerningGlyph1}')  
        #print('### %s' % getKerningSample(f))              
        found = False
        for gIndex, gName in enumerate(km.sample):
            if prev is not None:
                if gIndex > 10 and kerningGlyph1 in (prev, '') and kerningGlyph2 in (gName, ''):
                    self.controller.w.kerningSampleSelectSlider.setMaxValue(len(km.sample))
                    self.controller.w.kerningSampleSelectSlider.set(gIndex - 11) # Updating will be done from here
                    self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d' % (int(round((gIndex-11)/KERN_LINE_SIZE)), len(km.sample)/KERN_LINE_SIZE))
                    found = True
                    break
            prev = gName
        if not found: # Try again with just the first glyph
            for gIndex, gName in enumerate(km.sample):
                if gIndex > 10 and gName == kerningGlyph1:
                    self.controller.w.kerningSampleSelectSlider.setMaxValue(len(km.sample))
                    self.controller.w.kerningSampleSelectSlider.set(gIndex - 11) # Updating will be done from here
                    self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d' % (int(round((gIndex-11)/KERN_LINE_SIZE)), len(km.sample)/KERN_LINE_SIZE))
                    found = True
                    break
        if not found:
            print('### Kerning main pair not found (%s, %s)' % (kerningGlyph1, kerningGlyph2))
        else:
            g = CurrentGlyph()
            if g is not None:
                self.updatePreview(g)
                                                   
    def kerningSampleSelect(self):
        g = CurrentGlyph()
        if g is not None:
            km = kerningAssistant.getKerningManager(g.font)
            self.controller.w.kerningSampleSelectSlider.setMaxValue(len(km.sample))
            self.controller.w.kerningSampleSelectLabel.set('Kerning sample %d/%d' % (self.controller.w.kerningSampleSelectSlider.get(), len(km.sample)/KERN_LINE_SIZE))
            self.updatePreview(g)
            
    #    U P D A T E
                       
    def updatePreview(self, g):

        if self.controller is None: # In case no longer available
            return
                
        f = g.font

        km = self.getKerningManager(f)            

        kerningSelectedIndex = int(KERN_LINE_SIZE/2)
        # Update the kerning line
        if self.controller.w.showKerning.get():
            # Check if the right glyph is selected
            kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            #print('@@@', kerningSample[kerningCursor:kerningCursor+KERN_LINE_SIZE])
            selectedGlyph = km.sample[kerningCursor + kerningSelectedIndex]
            if g.name != selectedGlyph and self.kerningSelectedGlyph != selectedGlyph:
                self.kerningSelectedGlyph = selectedGlyph
                if selectedGlyph in f:
                    OpenGlyphWindow(glyph=f[selectedGlyph], newWindow=False)
                return # Will be called again with the new selected glyph

         # Update the kerning line
        if self.controller.w.showKerning.get():
            
            kerningSrc = None
                            
            xLeft = int(self.controller.w.kerningLeftX.get())      
            xo = x = xLeft/KERN_SCALE # Get left position of kerning samples
            y1 = 1.75*f.info.descender/KERN_SCALE # Glyph image position
            y3 = y1 + f.info.descender # Box position
            y2 = y3 - 100 # Kerning value position
            y4 = -150 # Position of current kerning values
            y6 = -250 # Position of kerning-cursor box

            start = kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            stop = start + KERN_LINE_SIZE
            prevName = None
            for gIndex, kerningGlyphLayer in enumerate(self.kerningLine): # List of kerned glyph images
                gName = km.sample[start + gIndex]
                if gName is not None and gName in f:
                    gKern = f[gName]
                    if gIndex == kerningSelectedIndex:
                        self.kerningSelectedGlyphMarker.setPosition((x + k, y2-100))
                        self.kerningSelectedGlyphMarker.setSize((gKern.width, 100))

                        if self.controller.w.showKerningFilled.get():
                            self.kernGlyphImage.setPath(gKern.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage.setPosition((0, 0))
                        else:
                            self.kernGlyphImage.setPosition((FAR, 0))
                        self.kernGlyphImage.setFillColor((0, 0, 0, 1))
                                            
                        if prevName is not None: # Kerning glyph on left side of current glyph

                            prev = f[prevName]
                            k, groupK, kerningType = km.getKerning(prevName, gKern.name) # Get the kerning from the groups of these glyphs
                            kSrcString = ''
                            self.kernGlyphImage1.setPath(prev.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage1.setPosition((-prev.width - k, 0))
                            if kerningType in (1, 2) and k != groupK: # Show that we are kerning group<-->glyph
                                self.kernGlyphImage1.setFillColor(GROUPGLYPH_COLOR)
                                self.kernGlyphImage.setFillColor(GROUPGLYPH_COLOR)
                            elif kerningType == 3 and k != groupK: # Show that we are in kerning glyph<-->glyph
                                self.kernGlyphImage1.setFillColor(GLYPHGLYPH_COLOR)
                                self.kernGlyphImage.setFillColor(GLYPHGLYPH_COLOR)
                            else:
                                self.kernGlyphImage1.setFillColor((0, 0, 0, 1))
                            if kerningType in (1, 2):
                                self.kerning1Value.setFillColor(GROUPGLYPH_COLOR)
                            elif kerningType == 3:
                                self.kerning1Value.setFillColor(GLYPHGLYPH_COLOR)
                            elif k < 0:
                                self.kerning1Value.setFillColor((1, 0, 0, 1))
                            elif k > 0:
                                self.kerning1Value.setFillColor((0, 0.5, 0, 1))
                            else:
                                self.kerning1Value.setFillColor((0.6, 0.6, 0.6, 1))
                            self.kerning1Value.setPosition((-k, y4))
                            if k != groupK: 
                                self.kerning1Value.setText('%d:G%d%s' % (k, groupK, kSrcString))
                            else:
                                self.kerning1Value.setText('%d%s' % (k, kSrcString))
                                
                    elif gIndex == kerningSelectedIndex + 1: # Kerning glyph on right side of current glyph
                        if prevName is not None:  
                            prev = f[prevName]
                            k, groupK, kerningType = km.getKerning(prevName, gKern.name) # Get the kerning from the groups of these glyphs
                            kSrcString = ''
                            self.kernGlyphImage2.setPath(gKern.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage2.setPosition((prev.width + k, 0))
                            if kerningType in (1, 2) and k != groupK: # Show that we are kerning glyph<-->group
                                self.kernGlyphImage2.setFillColor(GROUPGLYPH_COLOR)
                                self.kernGlyphImage.setFillColor(GROUPGLYPH_COLOR)
                            elif kerningType == 3 and k != groupK: # Show that we are kerning glyph<-->group
                                self.kernGlyphImage2.setFillColor(GLYPHGLYPH_COLOR)
                                self.kernGlyphImage.setFillColor(GLYPHGLYPH_COLOR)
                            else:
                                self.kernGlyphImage2.setFillColor((0, 0, 0, 1))
                            if kerningType in (1,2):
                                self.kerning2Value.setFillColor(GROUPGLYPH_COLOR)
                            elif kerningType == 3:
                                self.kerning2Value.setFillColor(GLYPHGLYPH_COLOR)
                            elif k < 0:
                                self.kerning2Value.setFillColor((1, 0, 0, 1))
                            elif k > 0:
                                self.kerning2Value.setFillColor((0, 0.5, 0, 1))
                            else:
                                self.kerning2Value.setFillColor((0.6, 0.6, 0.6, 1))
                            self.kerning2Value.setPosition((prev.width + k, y4))
                            if k != groupK:        
                                self.kerning2Value.setText('%d:G%d%s' % (k, groupK, kSrcString))
                            else:
                                self.kerning2Value.setText('%d%s' % (k, kSrcString))

                    k = 0
                    if prevName is not None:
                        k, groupK, kerningType = km.getKerning(prevName, gName) # Get the kerning from the groups of these glyphs
                        if kerningType is not None:
                            kSrc = 0
                            kSrcString = ''
                            klv = self.kerningLineValues[gIndex] # List of kerning value layers
                            if k or kSrc:
                                klv.setPosition((x, y2))
                                if k != groupK:
                                    klv.setText('%d:G%d%s' % (k, groupK, kSrcString))
                                else:
                                    klv.setText('%d%s' % (k, kSrcString))
                                if kerningType in (1, 2) and k != groupK: # Other than group<-->group                            
                                    klv.setFillColor(GROUPGLYPH_COLOR)
                                elif kerningType == 3 and k != groupK: # Other than group<-->group                            
                                    klv.setFillColor(GLYPHGLYPH_COLOR)
                                elif k < 0:
                                    klv.setFillColor((1, 0, 0, 1))
                                elif k > 0:
                                    klv.setFillColor((0, 0.5, 0, 1))
                                else:
                                    klv.setFillColor((0.6, 0.6, 0.6, 1))
                            else:
                                klv.setPosition((FAR, y2))

                    kerningGlyphLayer.setFillColor((0, 0, 0, 1))
                    kerningGlyphLayer.setPath(gKern.getRepresentation("merz.CGPath"))
                    kerningGlyphLayer.setPosition((x + k, y1))
        
                    klb = self.kerningLineBoxes[gIndex]
                    if self.controller.w.showKerningBox.get():
                        klb.setPosition((x + k, y3))
                        klb.setSize((gKern.width, f.info.unitsPerEm))
                    else:
                        klb.setPosition((FAR, y3))
                        
                    x += gKern.width + k
                    prevName = gName
                    
            kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            s = '%d/%d Pairs %d' % (kerningCursor/KERN_LINE_SIZE, len(km.sample)/KERN_LINE_SIZE, len(f.kerning))
            self.kerningCursorBox.setText(s)
            self.kerningCursorBox.setPosition((xLeft, 40)) # y6
        else:
            for kerningLine in self.kerningLine:
                kerningLine.setPosition((FAR, 0))
            for kerningLineValue in self.kerningLineValues:
                kerningLineValue.setPosition((FAR, 0))
            for kerningLineBox in self.kerningLineBoxes:
                kerningLineBox.setPosition((FAR, 0))
            self.kerningCursorBox.setPosition((FAR, 0))
            self.kernGlyphImage1.setPosition((FAR, 0))
            self.kernGlyphImage2.setPosition((FAR, 0))
            self.kerning1Value.setPosition((FAR, 0))
            self.kernGlyphImage.setPosition((FAR, 0))
            self.kerning2Value.setPosition((FAR, 0))

        kerningSelectedIndex = int(KERN_LINE_SIZE/2)
        kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
        self.kernGlyph1 = km.sample[kerningCursor + kerningSelectedIndex - 1]
        self.kernGlyph2 = km.sample[kerningCursor + kerningSelectedIndex + 1]

        # Update the groups lists for the new current glyph
        self.group1TextLeftLayer.setText('\n'.join(sorted(km.glyphName2Group1.get(self.kernGlyph1, []))))
        self.group2TextRightLayer.setText('\n'.join(sorted(km.glyphName2Group2.get(self.kernGlyph2, []))))
        self.group2TextLeftLayer.setText('\n'.join(sorted(km.glyphName2Group1.get(g.name, []))))
        self.group1TextRightLayer.setText('\n'.join(sorted(km.glyphName2Group2.get(g.name, []))))

        if self.controller.w.showKerningLists.get():
            self.group1TextLeftLayer.setPosition((-g.width-2*self.groupTextLayer_colW, 0))
            self.group2TextRightLayer.setPosition((g.width*2+self.groupTextLayer_colW, 0))
            self.group2TextLeftLayer.setPosition((-g.width-self.groupTextLayer_colW, 0))
            self.group1TextRightLayer.setPosition((g.width*2, 0))
        else:
            self.group1TextLeftLayer.setPosition((FAR, 0))
            self.group2TextRightLayer.setPosition((FAR, 0))
            self.group2TextLeftLayer.setPosition((FAR, 0))
            self.group1TextRightLayer.setPosition((FAR, 0))
            
    def guessBasedLeftMargin(self, f, md, g, gd, base, l):
        if l == 'CENTER':
            return l
        if isinstance(l, str):
            l = f[l].angledLeftMargin
        elif l is None:
            if base is not None: # If l is not defined and there is a base, then use that margin instead
                baseGlyph = f[base] # Get the base glyph
                baseGd = getGlyphData(f, g.name)
                self.checkSpacing(f, md, baseGlyph, baseGd) # Make sure the base itself is rightly spaced
                l = baseGlyph.angledLeftMargin # Now we take the left margin of the base.
        # else l must already be a number or None

        if l is not None and base: # Answer the margin from the perspective of the base component, if defined 
            for component in g.components:
                if component.baseGlyph == base: # This is the base component, get the transformation
                    baseGlyph = f[base]
                    baseLeft = baseGlyph.angledLeftMargin
                    l -= component.transformation[-2] + baseLeft + tan(radians(f.info.italicAngle)) * component.transformation[-1]
                    l = g.angledLeftMargin + l
        
        # Number or 'CENTER'            
        return l
       
    def guessBasedRightMargin(self, f, md, g, gd, base, r):
        if isinstance(r, str):
            r = f[r].angledRightMargin
        elif r is None:
            if base is not None: # If l is not defined, and there is a base, use that margin instead
                baseGlyph = f[base] # Get the base glyph
                baseGd = getGlyphData(f, g.name)
                self.checkSpacing(f, md, baseGlyph, baseGd) # Make sure the base itself is rightly spaced
                r = baseGlyph.angledRightMargin # Now we take the left margin of the base.
        # else r must already be a number or None
        if r is not None and base: # Answer the margin from the perspective of the base component, if defined 
            for component in g.components:
                if component.baseGlyph == base: # This is the base component, get the transformation
                    baseGlyph = f[base]
                    r = baseGlyph.angledRightMargin
                    
        return r   
            
    def checkSpacingDependencies(self, g):
        """Check the spacing dependencies of the current selected kerning line"""
        changed = False
        """ Skip for now, we'll do margin-guessing in context of similarities, instead of using GLYPH_DATA, 
        as that table may not always be available or filled out.
        f = g.font
        md = getMasterData(f)
        glyph2SpacingChildren = getGlyph2SpacingChildren(f)
        for gChildName in glyph2SpacingChildren.get(g.name, []):
            gChild = f[gChildName]
            gd = getGlyphData(f, gChildName)
            changed |= self.checkSpacing(f, md, gChild, gd, setMarkers=False)
        """
        return changed
        
    def checkSpacing(self, f, md, g, gd, done=None, setMarkers=True):
        """Check the spacing, draw markers and overwrite the spacing from the source if it is different."""
        if VERBOSE2:
            print('@@@ Check spacing', g.name)
        
        if gd is None:
            print('### Cannot find glyphData for /%s' % g.name)
            return False
            
        if done is None:
            done = set()
        if g.name in done:
            return False

        base, l, r, w, il, ir, iw, ml, mr, l2r, r2l, il2r, ir2l = (
            gd.base,
            gd.l, gd.r, gd.w, gd.il, gd.ir, gd.iw, gd.ml, gd.mr, 
            gd.l2r, gd.r2l, gd.il2r, gd.ir2l)

        changed = False
        
        gLabel = ''
        gDisplay = None
        
        # @@@ Disable the auto-copy of margins from Display masters per 2022-02-12 (Build 015) 
        # @@@ Enable on 2023-03-05
        # @@@ Disable on 2023-09-21 after TN/Adobe delivery
        if 0 and md.displaySrc is not None: # Copy from equivalent margin of Display master            
            fd = getMaster(md.displaySrc)
            if g.name not in fd:
                print('### Missing glyph /%s in %s' % (g.name, md.displaySrc))
                return False
            gDisplay = fd[g.name]
            if gDisplay.width and not g.components:
                if l is None and ml is None and il is None and r2l is None and gDisplay.leftMargin is not None:
                    l = int(round(gDisplay.angledLeftMargin + gd.smallTrackLeft))
                    gLabel = 'Copy left from display /%s' % g.name
                if r is None and mr is None and ir is None and w is None and iw is None and l2r is None and gDisplay.rightMargin is not None:
                    r = int(round(gDisplay.angledRightMargin + gd.smallTrackRight))
                    gLabel += 'Copy right from display /%s' % g.name
                        
        if self.controller.w.checkFixSpacing.get() and not md.fixedSpacing: # This font has automatic spacing? If fixed, then ignore any requested change
            # Interpret which kind of spacing is requested
            # Interpret left specification. Translate the requested left margin l
            # into what the margin should be to keep the base at its original positions.

            if ml is not None:
                l = self.guessBasedLeftMargin(f, md, g, gd, None, ml) # Overwrite the base margin, just look at full glyph margin           
            elif l is not None:
                l = self.guessBasedLeftMargin(f, md, g, gd, base, l) # Use margin of the base
            if mr is not None:
                r = self.guessBasedRightMargin(f, md, g, gd, None, mr) # Overwrite the base margin, just look at full glyph margin
            elif r is not None:
                r = self.guessBasedRightMargin(f, md, g, gd, base, r) # Use margin of the base

            # Interpret width specification
            if w == TAB:
                w = md.tab # md.metrics[TAB] @ Dofferent for Condensed and Extended
            elif w == ACCENT_WIDTH:
                w = md.accentWidth #metrics[ACCENT_WIDTH] Different for Condensed and Extended
            elif w == EM:
                w = md.em #.metrics[EM]
            elif w == EM2:
                w = md.em/2
            elif w == MATH_WIDTH:
                w = md.mathWidth
            elif isinstance(w, str):
                w = f[w].width  
            elif w is None and base is not None and mr is None:
                baseGlyph = f[base]
                baseGd = getGlyphData(f, g.name)
                changed |= self.checkSpacing(f, md, baseGlyph, baseGd, done)  # Make sure the base itself is rightly spaced
                if VERBOSE4 and changed:
                    print('###222 Set width', changed)
                if g.name in done:
                    return changed
                #w = baseGlyph.width    
 
            # else w must be a number
            # Interpret mirrored margins
            if r2l:
                l = f[r2l].angledRightMargin    
            if l2r:
                r = f[l2r].angledLeftMargin  
            
            D = 1 # Difference when to change (due to rounding of italic coordinates)
            if g.angledLeftMargin is None and w is not None: # No contours, just set width
                g.width = w
                changed = True
                if VERBOSE4 and changed:
                    print('###333 Set width', changed)
            elif w is not None:
                if r is None:
                    # Just set the width
                    g.width = w
                    changed = True
                    if VERBOSE4 and changed:
                        print('###444 Set width', changed)
                elif l == 'CENTER':
                    alm = g.angledLeftMargin
                    if alm is not None:
                        if abs(g.width - w) > 0.5:
                            g.width = w
                            changed = True
                            if VERBOSE4 and changed:
                                print('###555 Set width', changed)
                        centered = (alm + g.angledRightMargin) / 2
                        if abs(centered - alm) > D:
                            print('... Center /%s left margin (%d --> %d) and width (%d --> %d)' % (g.name, alm, centered, w, g.width))
                            g.angledLeftMargin = centered
                            g.width = w # Set again, in case of rounding error
                            changed = True
                            if VERBOSE4 and changed:
                                print('###666 Set width', changed)
                    l = r = None # Notify that we already did draw. If w and l defined, then ignore r
            
                elif l is not None:
                    alm = g.angledLeftMargin
                    if alm is not None and (abs(alm - l) > D or abs(g.width - w) > D):
                        print('... %s Set /%s left margin (%d --> %d) and width (%d --> %d)' % (gLabel, g.name, alm, l, w, g.width))
                        g.angledLeftMargin = l
                        g.width = w
                        changed = True
                        if VERBOSE4 and changed:
                            print('###777 Set width', changed)
                    l = r = None # Notify that we already did draw. If w and l defined, then ignore r

                elif r is not None: # Either l or r can be set, if w is defined.
                    arm = g.angledRightMargin
                    if arm is not None and (abs(arm - r) > D or abs(g.width - w) > D):
                        print('... %s Set /%s right margin (%d --> %d) and width (%d --> %d)' % (gLabel, g.name, arm, r, w, g.width))
                        g.width = w # First set the width
                        arm = g.angledRightMargin
                        g.angledLeftMargin -= arm - r # Then move the glyph by difference on right side
                        g.width = w # Set actual width to overwrite roundings.
                        changed = True
                        if VERBOSE4 and changed:
                            print('###888 Set width', changed)
                    r = l = None # Notify that we already did draw

                elif w is not None and abs(g.width - w) > D: # No l or r defined, just set the width.
                    print('... %s Set /%s width (%d --> %d)' % (gLabel, g.name, w, g.width))
                    g.width = w
                    changed = True
                    if VERBOSE4 and changed:
                        print('###999 Set width', changed)
   
            if l is not None and isinstance(l, (float, int)):  # Value defined but not drawn yet?
                alm = g.angledLeftMargin
                #print('## L ##', g.name, r, l, alm)
                if alm is not None and abs(alm - l) > D:
                    print('... %s Set /%s left margin (%d --> %d)' % (gLabel, g.name, l, alm))
                    g.angledLeftMargin = l
                    changed = True
                    if VERBOSE4 and changed:
                        print('###000 Set angledLeftMargin', changed)

            if r is not None and isinstance(r, (float, int)): # Value defined but not drawn yet?
                arm = g.angledRightMargin
                #print('## R ##', g.name, r, l, arm)
                if arm is not None and abs(arm - r) > D:
                    print('... %s Set /%s right margin (%d --> %d)' % (gLabel, g.name, r, arm))
                    g.angledRightMargin = r
                    changed = True
                    if VERBOSE4 and changed:
                        print('###000 Set angledRightMargin', changed)
        
        # @@@@@ Move to self.updatePreview() ?            
        if setMarkers:
            # Set the drawing of spacing markers, depending if there are spacing sources for this glyph
            self.fixedSpaceMarkerRight.setPosition((g.width-SPACE_MARKER_R, -SPACE_MARKER_R))
            self.leftSpaceSourceLabel.setPosition((0, -SPACE_MARKER_R*1.5))
            self.rightSpaceSourceLabel.setPosition((g.width, -SPACE_MARKER_R*1.5))

            leftSpaceSourceLabel = gd.leftSpaceSourceLabel
            if md.fixedSpacing:
                c = 0.2, 0, 0.5, 0.25
                label = 'Fixed'
            elif leftSpaceSourceLabel:
                c = 1, 0, 0, 1
                label = leftSpaceSourceLabel
            elif gDisplay is not None:
                c = 1, 1, 0, 1
                label = 'Display %s: %d+%d' % (gDisplay.name, gDisplay.angledLeftMargin, gd.smallTrackLeft)
            else:
                c = 0, 0, 0, 0
                label = ''
            self.fixedSpaceMarkerLeft.setStrokeColor(c)
            self.leftSpaceSourceLabel.setText(label)

            rightSpaceSourceLabel = gd.rightSpaceSourceLabel
            if md.fixedSpacing:
                c = 0.2, 0, 0.5, 0.25
                label = 'Fixed'
            elif rightSpaceSourceLabel:
                c = 1, 0, 0, 1
                label = rightSpaceSourceLabel
            elif gDisplay is not None:
                c = 1, 1, 0, 1
                label = 'Display %s: %d+%d' % (gDisplay.name, gDisplay.angledRightMargin, gd.smallTrackRight)
            else:
                c = 0, 0, 0, 0
                label = ''
            self.fixedSpaceMarkerRight.setStrokeColor(c)
            self.rightSpaceSourceLabel.setText(label)
        
        done.add(g.name) # Recursively remember that we did this one
        
        return changed
        
    def updateMetricsText(self, md):
        # Update the metric text for this
        pass
        s = 'H stem: %s\nH thin: %s\nO stem: %s\nO thin: %s\nU thin: %s\nV thin: %s\nHsc stem: %s\nHsc thin: %s\nOsc stem: %s\nOsc thin: %s\nn stem: %s\no stem: %s\no thin: %s' % (
            md.HStem, md.HThin, md.OStem, md.OThin, md.UThin, md.VThin, md.HscStem, md.HscThin, md.OscStem, md.OscThin, md.nStem, md.oStem, md.oThin) 
        self.metricsTextLayer.setText(s)
        #print('... MetricsText', self.metricsTextLayer.getText())

        
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
C2 = C1 + CW + M

class KerningAssistantController(WindowController):
        
    assistantGlyphEditorSubscriberClass = KerningAssistant
    
    NAME = 'Kerning Assistant'
    
    def build(self):        

        f = CurrentFont()
        if f is None:
            kerningSampleIndex = 0
            kerningSampleX = -1000
        else:
            kerningSampleIndex = f.lib.get(KERNING_SAMPLE_SELECT_LIB, 0)
            kerningSampleX = f.lib.get(KERNING_SAMPLE_X, -1000)
            print('... Reading kerning select index in f.lib[%s]=%d for %s' % (KERNING_SAMPLE_SELECT_LIB, kerningSampleIndex, f.path.split('/')[-1]))

        y = M
        self.w = WindowClass((W, H), self.NAME, minSize=(W, H))

        self.w.showKerning = vanilla.CheckBox((C0, y, CW, L), 'Show kerning', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningBox = vanilla.CheckBox((C1, y, CW, L), 'Show kerning box', value=False, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningFilled = vanilla.CheckBox((C2, y, CW, L), 'Show kerning filled', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L
        self.w.showKerningLists = vanilla.CheckBox((C0, y, CW, L), 'Show kerning lists', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.keysOverview = vanilla.TextBox((C1, y, 2*CW, 36), 'Navigate: alt + arrows, alt + shift + arrows\nKern: [n][m] [comma][period]', sizeStyle="small")
        y += 24
        self.w.kerningSampleTextLabel = vanilla.TextBox((C0, y, -M, 24), 'Find kerning pair', sizeStyle="small")
        y += 18
        self.w.kerningGlyph1 = vanilla.EditText((C0, y, CW, L)) # Use  kerning find button to go there.
        self.w.kerningGlyph2 = vanilla.EditText((C1, y, CW, L))
        self.w.findKerning = vanilla.Button((C2, y, CW, L), 'Find pair', callback=self.findKerningSampleCallback)
        y += 32
        self.w.kerningLeftXLabel = vanilla.TextBox((C0, y, -M, 24), 'Kerning sample X', sizeStyle="small")
        self.w.kerningSampleSelectLabel = vanilla.TextBox((C1, y, -M, 24), 'Kerning sample 0/0 lines', sizeStyle="small") # Range value will be updated
        y += 12
        self.w.kerningLeftX = vanilla.Slider((C0, y, CW, 24), minValue=-4000, maxValue=2500, value=kerningSampleX, continuous=True, callback=self.updateEditor)
        self.w.kerningSampleSelectSlider = vanilla.Slider((C1, y, CW*2+M, 24), minValue=0, maxValue=486, value=kerningSampleIndex, continuous=True, callback=self.kerningSampleSelectSliderCallback)
        y += 32
        self.w.automaticGroups = vanilla.CheckBox((C0, y, CW, L), 'Automatic groups', value=True, sizeStyle='small')
        y += L
        self.w.groupName2Label = vanilla.TextBox((C0, y, CW, 24), 'Group 2 (left side)', sizeStyle="small")
        self.w.groupName1Label = vanilla.TextBox((C15, y, CW, 24), 'Group 1 (right side)', sizeStyle="small")
        y += 18 
        # Group names of current glyph
        self.w.groupName2 = vanilla.TextBox((C0, y, CW*1.5, 24), '---', sizeStyle="small")
        self.w.groupName1 = vanilla.TextBox((C15, y, CW*1.5, 24), '---', sizeStyle="small")
        y += 18
        # List of alternative group (or single glyphs without a group) according to Similarity
        self.w.groupNameList2 = vanilla.List((C0, y, CW*1.5, 90), [], selectionCallback=self.groupNameListSelectCallback2, doubleClickCallback=self.groupNameListDblClickCallback2)
        self.w.groupNameList1 = vanilla.List((C15, y, CW*1.5, 90), [], selectionCallback=self.groupNameListSelectCallback1, doubleClickCallback=self.groupNameListDblClickCallback1)
        y += 100
        # Label for glyph list of current group selection
        self.w.groupGlyphs2Label = vanilla.TextBox((C0, y, CW, 24), 'Glyphs of ---', sizeStyle="small")
        self.w.groupGlyphs1Label = vanilla.TextBox((C15, y, CW, 24), 'Glyphs of ---', sizeStyle="small")
        y += 18
        # List of glyphs of current group selection.
        # Double click opens the EditorWindow on that glyph.
        self.w.groupNameGlyphList2 = vanilla.List((C0, y, CW*1.5, 130), [], doubleClickCallback=self.groupNameGlyphListDblClickCallback)
        self.w.groupNameGlyphList1 = vanilla.List((C15, y, CW*1.5, 130), [], doubleClickCallback=self.groupNameGlyphListDblClickCallback)
        y += 130
        # Text box to enter an alternative sample text. /? is replaced by the current glyph unicode
        self.w.sampleTextLabel = vanilla.TextBox((C0, y, -M, 24), 'Sample text in FontGoggles', sizeStyle="small")
        y += 18
        self.w.sampleText = vanilla.EditText((C0, y, -M, 24), SAMPLES[0], callback=self.updateEditor)
        y += L
        self.w.sampleTextSelect = vanilla.PopUpButton((C0, y, -M, 32), SAMPLES,
            callback=self.sampleTextSelectCallback, sizeStyle='small')

        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None
        
    def groupNameListSelectCallback2(self, sender):
        f = CurrentFont()
        glyphNames = []
        label = 'Glyphs of ---'
        if f is not None:
            for index in sender.getSelection():
                groupName = sender[index]
                if groupName in f.groups:
                    glyphNames = f.groups[groupName]
                    label = f'Glyphs of {groupName}'
                    break
                    
        self.w.groupGlyphs2Label.set(label)
        self.w.groupNameGlyphList2.set(glyphNames)
        
    def groupNameListSelectCallback1(self, sender):
        f = CurrentFont()
        glyphNames = []
        label = 'Glyphs of ---'
        if f is not None:
            for index in sender.getSelection():
                groupName = sender[index]
                if groupName in f.groups:
                    glyphNames = f.groups[groupName]
                    label = f'Glyphs of {groupName}'
                    break
        self.w.groupGlyphs2Label.set(label)
        self.w.groupNameGlyphList1.set(glyphNames)
 
    def groupNameListDblClickCallback2(self, sender):
        g = CurrentGlyph()
        km = kerningAssistant.getKerningManager(g.font)
        km.addGlyph2Group2(g, sender[sender.getSelection()[0]])
        
    def groupNameListDblClickCallback1(self, sender):
        g = CurrentGlyph()
        km = kerningAssistant.getKerningManager(g.font)
        km.addGlyph2Group1(g, sender[sender.getSelection()[0]])
               
    def groupNameGlyphListDblClickCallback(self, sender):        
        f = CurrentFont()
        if f is not None:
            for index in sender.getSelection():
                glyphName = sender[index]
                OpenGlyphWindow(glyph=f[glyphName], newWindow=False)
                break
            
    def findKerningSampleCallback(self, sender):
        kerningAssistant.findKerningSample(self.w.kerningGlyph1.get(), self.w.kerningGlyph2.get())
    
    def kerningSampleSelectSliderCallback(self, sender):
        kerningAssistant.kerningSampleSelect()
            
    def updateEditor(self, sender):
        # Force updating of the current EditorWindow. Is there a better way to do this directly?
        g = CurrentGlyph()
        if g is not None:
            g.changed()
            
    def fixKerning(self, f):
        """Copy all kerning from Display if f is a Small master"""
        xxx
        md = getMasterData(f)
        # @@@ Disable copy of kerning from Display masters per 1/12/2022 (Build 015)
        if 0 and md.displaySrc is not None: # Copy from equivalent margin of Display master            
            fd = getMaster(md.displaySrc)
            f.kerning.clear()
            print('... Copy %d kerning pairs from %s to %s' % (len(fd.kerning), md.displaySrc, md.name))
            for pair, k in fd.kerning.items():
                f.kerning[pair] = k
                                                  
    def sampleTextSelectCallback(self, sender):
        # This will makek the self.w.sampleText call the self.updateEditor
        self.w.sampleText.set(sender.getItem())
        self.updateEditor(sender)
 
                  
if __name__ == '__main__':
    OpenWindow(KerningAssistantController)

  