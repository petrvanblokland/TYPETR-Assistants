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
#    Install Similarity from Mechanic and run it once, after RoboFont starts.
#    The initial window can be closed. This way the library "cosoneSimilarity"
#    becomes available for this Assistant.
#
#    No need to import KernNet for AI assistent kerning. That will be available as local webserver.
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

ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]
FUNCTION_KEYS = (
    'Uu', # Decrement left margin
    'Ii', # Increment left margin
    'Oo', # Decrement right margin
    'Pp', # Increment right margin
    ';', # Set left pair kerning to self.predictedKerning1
    "'", # Set right pair kerning to self.predictedKerning2
    'Nn', # Increment left kerning
    'Mm', # Decrement left kerning
    '.<', # Decrement right kerning
    ',>', # Increment right kerning
)

VERBOSE = False
VERBOSE2 = False

KERNING_SAMPLE_SELECT_LIB = 'TYPETR-Presti-Assistant-KerningSampleIndex'
KERNING_SAMPLE_X = 'KerningAssistant-GG-Sample'

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

W, H = 460, 640
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
        
        self.predictedKerning1 = '-'
        self.predictedKerning2 = '-'
        
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
        self.groupTextLayer_colW = colW = 500 
        colH = f.info.capHeight
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
        
        # The KerningManagers is just doing margins according the available glyph.lib dependecies 
        # and to the groups.
        
        self.fixedSpaceMarkerLeft = container.appendOvalSublayer(name="spaceMarkerLeft",
            position=(-SPACE_MARKER_R, -SPACE_MARKER_R),
            size=(SPACE_MARKER_R*2, SPACE_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.leftSpaceSourceLabel = container.appendTextLineSublayer(name="leftSpaceSourceLabel",
            position=(FAR, -SPACE_MARKER_R*2),
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
            position=(FAR, -SPACE_MARKER_R*2),
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
        self.similarGlyphImage1 = self.backgroundContainer.appendPathSublayer(
            name='similarGlyphImage1',
            position=(0, 0),
            fillColor=(0.5, 0.5, 0.5, 0.2),
            strokeColor=(1, 0, 0, 1),
            strokeWidth=1,
        )
        self.similarGlyphImage2 = self.backgroundContainer.appendPathSublayer(
            name='similarGlyphImage2',
            position=(0, 0),
            fillColor=(0.5, 0.5, 0.5, 0.2),
            strokeColor=(1, 0, 0, 1),
            strokeWidth=1,
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
        
        # For some reason, predicted kerning seems to be best when subrachting this amount
        # Value is for 1000 EM.
        CALIBRATE = 1 #.4 #-36 
        ss = str(page.read())
        #print('Predicted kerning', ss, len(ss), int(ss[2:-1]))
        #print('===', int(str(page.read())[2:-1]))
        k = float(ss[2:-1])
        #k = round(int(str(page.read())[2:-1]) * f.info.unitsPerEm/1000) + CALIBRATE     
        kk = int(round(k * CALIBRATE/4))*4
        print('Predicted kerning', gName1, gName2, k, kk)
        if abs(kk) <= 4:
            kk = 0 # Apply threshold for very small kerning values
            
        return kk
                            
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

        # Get the kerning  manager instance for this glyph
        km = self.getKerningManager(f)
                
        # Set spacing dependency parameters from glyph.lib
        d = km.getSpacingDependencyLib(g)
    
        # Set dependency UI labels according to the selected values    
        typeLeft = d.get('typeLeft')
        left = d.get('left', '')
        self.controller.w.spacingTypeLeft.setItem(typeLeft) 
        if left and left in f:
            self.controller.w.spacingLeft.set(left)
            if typeLeft == 'l': # Left margin of base component, if it exists.
                label = f'Left from base /{left}'
            elif typeLeft == 'ml':  # Left margin of whole glyph         
                label = f'Left from /{left}'
            elif typeLeft == 'r2l':           
                label = f'Right-->Left /{left}'
            else:
                label = 'Left'
            self.controller.w.spacingLeftLabel.set(label)                  
        else:
            self.controller.w.spacingLeft.set('') 
            self.controller.w.spacingLeftLabel.set('Left')

        typeRight = d.get('typeRight', '-')
        right = d.get('right', '')
        self.controller.w.spacingTypeRight.setItem(typeRight) 
        if right and right in f:
            self.controller.w.spacingRight.set(right)
            if typeRight == 'r': # Right margin of base component, if it exists.
                label = f'Right from base /{right}'
            elif typeRight == 'mr': # Right margin of whole glyph          
                label = f'Right from /{right}'
            elif typeLeft == 'l2r':          
                label = f'Left-->Right /{right}'
            else:
                label = 'Right'
            self.controller.w.spacingRightLabel.set(label)                  
        else:
            self.controller.w.spacingRight.set('') 
            self.controller.w.spacingRightLabel.set('Right')
            
        # Set controller groups names for current glyph
        sample = km.sample
        cursor = int(round(self.controller.w.kerningSampleSelectSlider.get())) + 16
        gName1 = km.sample[cursor-1]
        gName2 = km.sample[cursor+1]

        self.predictedKerning1 = self.predictKerning(gName1, g.name)
        self.predictedKerning2 = self.predictKerning(g.name, gName2)
        #print((gName1, g.name), k1, (g.name, gName2), k2)
        
        # Lists with similar groups
        simGroups2 = km.getSimilarGroupsNames2(g) #[] # List of group names
        self.controller.w.groupNameList2.set(simGroups2)
        if simGroups2:
            self.controller.w.groupNameList2.setSelection([0])
            self.controller.groupNameListSelectCallback2()
            
        simGroups1 = km.getSimilarGroupsNames1(g) #[] # List of group names
        self.controller.w.groupNameList1.set(simGroups1)
        if simGroups1:
            self.controller.w.groupNameList1.setSelection([0])
            self.controller.groupNameListSelectCallback1()

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
        self.updatePreview(g)
        
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

        # Adjust to predicted kerning
        
        elif characters == ';': # Set left pair to predicted kerning
            self._adjustLeftKerning(g, newK=self.predictedKerning1)
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
            updatePreview = True
        
        elif characters == "'": # Set right pair to predicted kerning
            self._adjustRightKerning(g, newK=self.predictedKerning2)
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
            print('Preview key down', g.name)
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
        self.updatePreview(g)
    
    def glyphEditorDidMouseUp(self, info):
        # Reset terminal stuff
        g = info['glyph']
        if VERBOSE:
            print('--- glyphEditorDidMouseDown', g.name)
        self.selectedTerminal = None
        self.mouseClickPoint = None
        self.mouseDraggedPoint = None
        #print('... Mouse up', info['locationInGlyph'], info['NSEvent'])
        self.updatePreview(g)
    
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
        self.updatePreview(g)

    def glyphEditorGlyphDidChangeInfo(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeInfo', g.name)
        self.updatePreview(g)
             
    def glyphEditorGlyphDidChangeOutline(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeOutline', g.name)
        self.updateGlyph(g)
        self.updatePreview(g)
            
    def glyphEditorGlyphDidChangeContours(self, info):
        """Event also calls glyphEditorGlyphDidChangeOutline"""
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeContours', g.name)        
        self.updateGlyph(g)
        self.updatePreview(g)
             
    def glyphEditorGlyphDidChangeComponents(self, info):
        """Event also calls glyphEditorGlyphDidChangeOutline"""
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeComponents', g.name)
        self.updateGlyph(g)
        self.updatePreview(g)
             
    def glyphEditorGlyphDidChangeAnchors(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeAnchors', g.name)
        self.updateGlyph(g)
        self.updatePreview(g)

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


    #    U P D A T I N G
                
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
        
        # Things that change the glyph should go here.
                
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
            print(f'... Searching for /{kerningGlyph1}, /{kerningGlyph2}')  
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
                
        self.updateKerningLine(g)
        self.updateSpaceMarkers(g)
        
    def updateSpaceMarkers(self, g):
        km = self.getKerningManager(g.font)

        print('updateSpaceMarkers', g.name)
        # Set the drawing of spacing markers, if there are spacing dependecies for this glyph
        self.fixedSpaceMarkerRight.setPosition((g.width-SPACE_MARKER_R, -SPACE_MARKER_R))
        self.leftSpaceSourceLabel.setPosition((0, -SPACE_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setPosition((g.width, -SPACE_MARKER_R*1.5))

        leftSpaceSourceLabel = km.getLeftSpaceDependencyLabel(g)
        if leftSpaceSourceLabel:
            c = 1, 0, 0, 1
            label = leftSpaceSourceLabel
        else:
            c = 0, 0, 0, 0
            label = ''
        self.fixedSpaceMarkerLeft.setStrokeColor(c)
        self.leftSpaceSourceLabel.setText(label)

        rightSpaceSourceLabel = km.getRightSpaceDependencyLabel(g)
        if rightSpaceSourceLabel:
            c = 1, 0, 0, 1
            label = rightSpaceSourceLabel
        else:
            c = 0, 0, 0, 0
            label = ''
        self.fixedSpaceMarkerRight.setStrokeColor(c)
        self.rightSpaceSourceLabel.setText(label)
        
    def updateKerningLine(self, g):
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
                                if self.controller.w.showKerningLeftFilled.get():
                                    self.kernGlyphImage1.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage1.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage1.setFillColor(None)
                                    self.kernGlyphImage1.setStrokeColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GROUPGLYPH_COLOR)

                            elif kerningType == 3 and k != groupK: # Show that we are in kerning glyph<-->glyph
                                if self.controller.w.showKerningLeftFilled.get():
                                    self.kernGlyphImage1.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage1.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage1.setFillColor(None)
                                    self.kernGlyphImage1.setStrokeColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GLYPHGLYPH_COLOR)

                            elif self.controller.w.showKerningFilled.get():
                                self.kernGlyphImage1.setFillColor((0, 0, 0, 1))
                                self.kernGlyphImage1.setStrokeColor(None)

                            else:
                                self.kernGlyphImage1.setFillColor(None)
                                self.kernGlyphImage1.setStrokeColor(None)
                                
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
                            if k != self.predictedKerning1:
                                predicted = f'\n({self.predictedKerning1})'
                            else:
                                predicted = '' 
                            if k != groupK: 
                                self.kerning1Value.setText('%d:G%d%s%s' % (k, groupK, kSrcString, predicted))
                            else:
                                self.kerning1Value.setText('%d%s%s' % (k, kSrcString, predicted))
                                
                    elif gIndex == kerningSelectedIndex + 1: # Kerning glyph on right side of current glyph
                        if prevName is not None:  
                            prev = f[prevName]
                            k, groupK, kerningType = km.getKerning(prevName, gKern.name) # Get the kerning from the groups of these glyphs
                            kSrcString = ''
                            self.kernGlyphImage2.setPath(gKern.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage2.setPosition((prev.width + k, 0))
                            if kerningType in (1, 2) and k != groupK: # Show that we are kerning group<-->glyph
                                if self.controller.w.showKerningRightFilled.get():
                                    self.kernGlyphImage2.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage2.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage2.setFillColor(None)
                                    self.kernGlyphImage2.setStrokeColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GROUPGLYPH_COLOR)

                            elif kerningType == 3 and k != groupK: # Show that we are in kerning glyph<-->glyph
                                if self.controller.w.showKerningRightFilled.get():
                                    self.kernGlyphImage2.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage2.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage2.setFillColor(None)
                                    self.kernGlyphImage2.setStrokeColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GLYPHGLYPH_COLOR)

                            elif self.controller.w.showKerningFilled.get():
                                self.kernGlyphImage2.setFillColor((0, 0, 0, 1))
                                self.kernGlyphImage2.setStrokeColor(None)

                            else:
                                self.kernGlyphImage1.setFillColor(None)
                                self.kernGlyphImage1.setStrokeColor(None)
                                
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
                            if k != self.predictedKerning2:
                                predicted = f'\n({self.predictedKerning2})'
                            else:
                                predicted = '' 
                            if k != groupK:        
                                self.kerning2Value.setText('%d:G%d%s%s' % (k, groupK, kSrcString, predicted))
                            else:
                                self.kerning2Value.setText('%d%s%s' % (k, kSrcString, predicted))

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
        self.group2TextLeftLayer.setText('\n'.join(sorted(km.glyphName2Group2.get(g.name, []))))
        self.group1TextRightLayer.setText('\n'.join(sorted(km.glyphName2Group1.get(g.name, []))))
        self.group2TextRightLayer.setText('\n'.join(sorted(km.glyphName2Group2.get(self.kernGlyph2, []))))

        if self.controller.w.showKerningLists.get():
            self.group1TextLeftLayer.setPosition((-g.width-2*self.groupTextLayer_colW, 0))
            self.group2TextLeftLayer.setPosition((-g.width-self.groupTextLayer_colW, 0))
            self.group1TextRightLayer.setPosition((g.width*2+self.groupTextLayer_colW, 0)) # Some extra on the right, in case of italics
            self.group2TextRightLayer.setPosition((g.width*2+2*self.groupTextLayer_colW, 0))
        else:
            self.group1TextLeftLayer.setPosition((FAR, 0))
            self.group2TextLeftLayer.setPosition((FAR, 0))
            self.group1TextRightLayer.setPosition((FAR, 0))
            self.group2TextRightLayer.setPosition((FAR, 0))
                        
    def checkSpacingDependencies(self, g):
        """Check the spacing dependencies of the current selected kerning line.
        The KerningManagers is just doing margins according dependencies and groups.
        This way no GLYPH_DATA is necessary. 
        """
        changed = False
        f = g.font
        km = self.getKerningManager(f)
        
        # Priority to dependencies that may be defined in g.lib[km.KEY]
        # Otherwise try to find the group2 (left) base
        lm = km.getLeftMargin(g) 
        if lm is not None:
            explain = f'... Set left margin of /{g.name} to {int(round(lm))} from dependency {km.getLeftSpaceDependencyLabel(g)}'
        else: # No dependency defined, try glyph group
            g2 = km.getLeftMarginGroupBaseGlyph(g) # Get the left margin source glyph, according to group2 of g
            if g2 is not None:
                lm = g2.angledLeftMargin
                explain = f'... Set left margin of /{g.name} to {int(round(lm))} from group {km.glyphName2GroupName2[g.name]}'

        if lm is not None and abs(g.angledLeftMargin - lm) >= 1: # Defined and it changed?
            print(explain)
            g.angledLeftMargin = lm
            changed = True

        # Priority to dependencies that may be defined in g.lib[km.KEY]
        # Otherwise try to find the group1 (right) base
        rm = km.getRightMargin(g) 
        if rm is not None:
            explain = f'... Set right margin of /{g.name} to {int(round(rm))} from dependency {km.getRightSpaceDependencyLabel(g)}'
        else: # No dependency defined, try glyph group
            g1 = km.getRightMarginGroupBaseGlyph(g) # Get the right margin source glyph, according to group1 of g
            if g1 is not None:
                rm = g1.angledRightMargin
                explain = f'... Set right margin of /{g.name} to {int(round(rm))} from group {km.glyphName2GroupName1[g.name]}'

        if rm is not None and abs(g.angledRightMargin - rm) >= 1: # Defined and it changed?
            print(explain)
            g.angledRightMargin = rm
            changed = True

        return changed
                        
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

        self.w.showKerningLeftFilled = vanilla.CheckBox((C0, y, CW, L), 'Show left filled', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningFilled = vanilla.CheckBox((C1, y, CW, L), 'Show kerning filled', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningRightFilled = vanilla.CheckBox((C2, y, CW, L), 'Show right filled', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L
        self.w.showKerning = vanilla.CheckBox((C0, y, CW, L), 'Show kerning', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showKerningBox = vanilla.CheckBox((C1, y, CW, L), 'Show kerning box', value=False, sizeStyle='small', callback=self.updateEditor)
        y += L
        self.w.showKerningLists = vanilla.CheckBox((C0, y, CW, L), 'Show kerning lists', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.keysOverview = vanilla.TextBox((C1, y, 2*CW, 36), 'Navigate: alt + arrows, alt + shift + arrows\nKern: [n][m] [comma][period]', sizeStyle="small")
        y += 24
        self.w.kerningSampleTextLabel = vanilla.TextBox((C0, y, -M, 24), 'Find kerning pair', sizeStyle="small")
        y += 24
        self.w.kerningGlyph1 = vanilla.EditText((C0, y, CW, L)) # Use  kerning find button to go there.
        self.w.kerningGlyph2 = vanilla.EditText((C1, y, CW, L))
        self.w.findKerning = vanilla.Button((C2, y, CW, L), 'Find pair', callback=self.findKerningSampleCallback)
        y += 32
        self.w.kerningLeftXLabel = vanilla.TextBox((C0, y, -M, 24), 'Kerning sample X', sizeStyle="small")
        self.w.kerningSampleSelectLabel = vanilla.TextBox((C1, y, -M, 24), 'Kerning sample 0/0 lines', sizeStyle="small") # Range value will be updated
        y += 12
        self.w.kerningLeftX = vanilla.Slider((C0, y, CW, 24), minValue=-4000, maxValue=2500, value=kerningSampleX, continuous=True, callback=self.updateEditor)
        self.w.kerningSampleSelectSlider = vanilla.Slider((C1, y, CW*2+M, 24), minValue=0, maxValue=486, value=kerningSampleIndex, continuous=True, callback=self.kerningSampleSelectSliderCallback)
        y += 24            
        self.w.autoKernAll = vanilla.Button((C1, y, CW, L), 'Auto kern all', callback=self.autoKernAllCallback)
        y += 24            
        popWidth = 60
        self.w.spacingTypeLeftLabel = vanilla.TextBox((C0, y, CW, 24), 'Type', sizeStyle="small")
        self.w.spacingLeftLabel = vanilla.TextBox((C0+popWidth, y, CW*1.5-popWidth, 24), 'Left', sizeStyle="small")
        self.w.spacingTypeRightLabel = vanilla.TextBox((C15, y, CW, 24), 'Type', sizeStyle="small")
        self.w.spacingRightLabel = vanilla.TextBox((C15+popWidth, y, CW*1.5-popWidth, 24), 'Right', sizeStyle="small")
        y += 18            
        self.w.spacingTypeLeft = vanilla.PopUpButton((C0, y, popWidth, L), SPACING_TYPES_LEFT, callback=self.setSpacingLibCallback) 
        self.w.spacingLeft = vanilla.EditText((C0+popWidth, y, CW*1.5-popWidth, L), callback=self.setSpacingLibCallback) 
        self.w.spacingTypeRight = vanilla.PopUpButton((C15, y, popWidth, L), SPACING_TYPES_RIGHT, callback=self.setSpacingLibCallback) 
        self.w.spacingRight = vanilla.EditText((C15+popWidth, y, CW*1.5-popWidth, L), callback=self.setSpacingLibCallback) 
        y += 32
        self.w.showSimilarGlyphs2 = vanilla.CheckBox((C0, y, CW, L), 'Show similar2', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.automaticGroups = vanilla.CheckBox((C1, y, CW, L), 'Automatic groups', value=True, sizeStyle='small')
        self.w.showSimilarGlyphs1 = vanilla.CheckBox((C2, y, CW, L), 'Show similar1', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L
        self.w.groupName2Label = vanilla.TextBox((C0, y, CW, 24), 'Group 2 (left side)', sizeStyle="small")
        self.w.groupName1Label = vanilla.TextBox((C15, y, CW, 24), 'Group 1 (right side)', sizeStyle="small")
        y += 18 
        # Group names of current glyph
        self.w.groupName2 = vanilla.TextBox((C0, y, CW*1.5, 24), '---', sizeStyle="small")
        self.w.groupName1 = vanilla.TextBox((C15, y, CW*1.5, 24), '---', sizeStyle="small")
        y += 18
        # List of alternative group (or single glyphs without a group) according to Similarity
        self.w.groupNameList2 = vanilla.List((C0, y, CW*1.5, 90), [], 
            selectionCallback=self.groupNameListSelectCallback2, doubleClickCallback=self.groupNameListDblClickCallback2)
        self.w.groupNameList1 = vanilla.List((C15, y, CW*1.5, 90), [], 
            selectionCallback=self.groupNameListSelectCallback1, doubleClickCallback=self.groupNameListDblClickCallback1)
        y += 100
        # Label for glyph list of current group selection
        self.w.groupGlyphs2Label = vanilla.TextBox((C0, y, CW*1.5, 24), 'Glyphs of ---', sizeStyle="small")
        self.w.groupGlyphs1Label = vanilla.TextBox((C15, y, CW*1.5, 24), 'Glyphs of ---', sizeStyle="small")
        y += 18
        # List of glyphs of current group selection.
        # Double click opens the EditorWindow on that glyph.
        self.w.groupNameGlyphList2 = vanilla.List((C0, y, CW*1.5, 130), [], 
            columnDescriptions=[dict(title='•', width=12), dict(title='Name'), dict(title='%', width=48)], 
            selectionCallback=self.groupNameGlyphListCallback2, doubleClickCallback=self.groupNameGlyphListDblClickCallback)
        self.w.groupNameGlyphList1 = vanilla.List((C15, y, CW*1.5, 130), [], 
            columnDescriptions=[dict(title='•', width=12), dict(title='Name'), dict(title='%', width=48)],
            selectionCallback=self.groupNameGlyphListCallback1, doubleClickCallback=self.groupNameGlyphListDblClickCallback)
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

    def groupNameListSelectCallback2(self, sender=None):
        g = CurrentGlyph()
        if g is None:
            return
        km = kerningAssistant.getKerningManager(g.font)
        glyphNames = []
        selectedGroup = None
        label = 'Glyphs of ---'

        for index in self.w.groupNameList2.getSelection():
            selectedGroupName = self.w.groupNameList2[index]
            if selectedGroupName in g.font.groups:
                label = f'Glyphs of {selectedGroupName}'
                similarGroups = km.getSimilarGroups2(g)
                selectedGroup = similarGroups.get(selectedGroupName)
                break
        self.w.groupGlyphs2Label.set(label)
        
        if selectedGroup is None:
            self.w.groupNameGlyphList2.set([])
        else:
            rows = []        
            for gName, confidence, isCurrent in selectedGroup:
                rows.append({'•':{True:'•', False:''}[isCurrent], 'Name':gName, '%':'%0.3f' % confidence})
            self.w.groupNameGlyphList2.set(rows)
            
    def groupNameListSelectCallback1(self, sender=None):
        g = CurrentGlyph()
        if g is None:
            return
        km = kerningAssistant.getKerningManager(g.font)
        glyphNames = []
        selectedGroup = None
        label = 'Glyphs of ---'

        for index in self.w.groupNameList1.getSelection():
            selectedGroupName = self.w.groupNameList1[index]
            if selectedGroupName in g.font.groups:
                label = f'Glyphs of {selectedGroupName}'
                similarGroups = km.getSimilarGroups1(g)
                selectedGroup = similarGroups.get(selectedGroupName)
                break
        self.w.groupGlyphs1Label.set(label)
        
        if selectedGroup is None:
            self.w.groupNameGlyphList1.set([])
        else:
            rows = []        
            for gName, confidence, isCurrent in selectedGroup:
                rows.append({'•':{True:'•', False:''}[isCurrent], 'Name':gName, '%':'%0.3f' % confidence})
            self.w.groupNameGlyphList1.set(rows)
 
    def groupNameListDblClickCallback2(self, sender):
        g = CurrentGlyph()
        km = kerningAssistant.getKerningManager(g.font)
        km.addGlyph2Group2(g, sender[sender.getSelection()[0]['Name']])
        
    def groupNameListDblClickCallback1(self, sender):
        g = CurrentGlyph()
        km = kerningAssistant.getKerningManager(g.font)
        km.addGlyph2Group1(g, sender[sender.getSelection()[0]['Name']])
               
    def groupNameGlyphListCallback1(self, sender=None):
        """Selected a glyph, show it as overlay in the EditorWindow"""
        g = CurrentGlyph()
        selection = self.w.groupNameGlyphList1.getSelection()
        if self.w.showSimilarGlyphs1.get() and g is not None and selection:
            similarGlyphName = self.w.groupNameGlyphList1[selection[0]]
            simG = g.font[similarGlyphName['Name']]
            kerningAssistant.similarGlyphImage1.setPath(simG.getRepresentation("merz.CGPath"))
            kerningAssistant.similarGlyphImage1.setPosition((g.width - simG.width, 0)) # Right aligned.
        else:
            kerningAssistant.similarGlyphImage1.setPosition((FAR, 0))                
        
    def groupNameGlyphListCallback2(self, sender=None):
        """Selected a glyph, show it as overlay in the EditorWindow"""
        g = CurrentGlyph()
        selection = self.w.groupNameGlyphList2.getSelection()
        if self.w.showSimilarGlyphs2.get() and g is not None and selection:
            similarGlyphName = self.w.groupNameGlyphList2[selection[0]]
            simG = g.font[similarGlyphName['Name']]
            kerningAssistant.similarGlyphImage2.setPath(simG.getRepresentation("merz.CGPath"))
            kerningAssistant.similarGlyphImage2.setPosition((0, 0)) # Right aligned.
        else:
            kerningAssistant.similarGlyphImage2.setPosition((FAR, 0))                
                
    def groupNameGlyphListDblClickCallback(self, sender):        
        f = CurrentFont()
        if f is not None:
            for index in sender.getSelection():
                glyphName = sender[index]['Name']
                OpenGlyphWindow(glyph=f[glyphName], newWindow=False)
                break
            
    def findKerningSampleCallback(self, sender):
        kerningAssistant.findKerningSample(self.w.kerningGlyph1.get(), self.w.kerningGlyph2.get())

    def autoKernAllCallback(self, sender):
        kerningAssistant.autoKernAll()
            
    def kerningSampleSelectSliderCallback(self, sender):
        kerningAssistant.kerningSampleSelect()
        
    def setSpacingLibCallback(self, sender):
        """Set the spacing dependecies for the current glyph.
        The spacing dependencies are stored as dictionary:
        f['A-cy'].lib[KEY] = dict(typeLeft='l', left='A', typeRight='r', right='A')
        The left and/or right dependencies can be omitted. They can be altered in the editor. 
        Omitted dependencies make the glyph "base" for other dependencies. 
        """
        g = CurrentGlyph()
        km = kerningAssistant.getKerningManager(g.font)
        d = {}
        typeLeft = self.w.spacingTypeLeft.getItem()
        left = self.w.spacingLeft.get()
        if typeLeft not in ('', '-'): # Otherwise just omit typeLeft
            d['typeLeft'] = typeLeft
        if left and left in g.font: 
            d['left'] = left
            self.w.spacingLeftLabel.set(f'Left from /{left}')
        else:
            d['left'] = ''
            self.w.spacingLeftLabel.set(f'Left')

        typeRight = self.w.spacingTypeRight.getItem()
        right = self.w.spacingRight.get()
        if typeRight not in ('', '-'): # Otherwise just omit typeRight
            d['typeRight'] = typeRight
        if right and right in g.font: 
            d['right'] = right
            self.w.spacingRightLabel.set(f'Right from /{right}')
        else:
            d['right'] = ''
            self.w.spacingLeftLabel.set(f'Right')

        km.setSpacingDependencyLib(g, d) # Set the g.lib[km.KEY] dictionary that hold the
        g.changed()
        
    def updateEditor(self, sender):
        # Force updating of the current EditorWindow. Is there a better way to do this directly?
        g = CurrentGlyph()
        self.groupNameGlyphListCallback1()
        self.groupNameGlyphListCallback2()
        if g is not None:
            g.changed()
                                                              
    def sampleTextSelectCallback(self, sender):
        # This will makek the self.w.sampleText call the self.updateEditor
        self.w.sampleText.set(sender.getItem())
        self.updateEditor(sender)
 
                  
if __name__ == '__main__':
    OpenWindow(KerningAssistantController)

  