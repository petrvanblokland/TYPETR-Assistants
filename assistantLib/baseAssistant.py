# -*- coding: UTF-8 -*-
#
#    BaseAssistant for RoboFont4
#    
#    Assistants inheriting from this base class, support a variety of functions,
#    which can be selected, depending on how relevant it is for a certain family.
#
#    Conversions triggered by selected or changed glyphs
#    - Draw on “background” layer, with converted outlines in the “foreground” layer.
#    -
#
#    Groups, spacing and kerning
#    - Showing the group(s) of current glyph
#    - Show editable line of related kerning pairs
#
#    Preview
#    - Left/right glyphs for showing spacing/kerning, interpolation check
#
#    Design process
#    - Color markers for individual designers after altering a glyph.
#
import sys
import os
import math
import codecs
import merz
import weakref
import importlib
from random import choice
from copy import copy

from vanilla import *
from math import *
from AppKit import *

from mojo.events import extractNSEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint, CurrentGlyph, CurrentFont
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.events import extractNSEvent

from fontTools.misc.transform import Transform

import assistantLib.assistantParts.data
importlib.reload(assistantLib.assistantParts.data)
from assistantLib.assistantParts.data import GlyphData, MasterData

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

FAR = 100000 # Put drawing stuff outside the window

ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]

class BaseAssistant:
    """Share functions and class variables for both Assistant and AssistantController.
    - Personalized marker colors for visited glyphs in the FontWindow
    - Personalized dictionary for function keys
    """

    # Select the color by user
    VISITED_MARKERS = [
        #('/Users/petr/Desktop/TYPETR-git', (40/255, 120/255, 255/255, 0.6), keys), # "Final" marker Blue (Petr))    
        ('/Users/petr/Desktop/TYPETR-git', (50/255, 70/255, 230/255, 0.8), {}), # "Final" marker Blue (Petr))    
        ('/Users/edwarddzulaj/Documents', (92/255, 149/255, 190/255, 1), {}), # Edward
        ('/Users/graemeswank/Documents', (255/255, 83/255, 73/255, 1), {}),
        ('/Users/graeme/Documents', (255/255, 83/255, 73/255, 1), {}),
        ('/Users/caterinasantullo/Desktop', (226/255, 69/255, 0/255, 1), {}),
        ('/Users/til/Documents', (0.9, 0.75, 1.0, 1.0), {}),
        ('/Users/anna/Downloads/Dropbox', (57/255, 163/255, 160/255, 1), {}),
        ('/Users/lenalepommelet/Documents', (138/255, 43/255,  226/255, 1), {})
    ]
    
    # Key translations from personalized key strokes are handled by the BaseAssistant.glyphEditorDidKeyDown
    TRANSLATE_KEYS = {} # Key strokes can be redefined if defined as dict(b='B', B=None, g='G', q='#')
    
    VISITED_MARKER = None
    for path, color, keys in VISITED_MARKERS:
        if __file__.startswith(path):
            VISITED_MARKER = color
            print('User color for',  path, color)
            TRANSLATE_KEYS = keys
            break
    if VISITED_MARKER is None:
        VISITED_MARKER = (1, 1, 1, 1) # Clear to white

    # Must be redefined by inheriting assistant classes where to find the main UFO master files
    UFO_PATH = 'ufo/' # Standard place for UFO files
    UFO_PATHS = None 

    # If there's masterData available, then this should be redefined as dictionaty by inheriting Assistant classes
    #MASTER_DATA = None 

    # Names of methods to call for initializeing and updating Merz. 
    # To be defined by inheriting classes. 
    INIT_MERZ_METHODS = []
    UPDATE_METHODS = [] # Something changed to the glyph. Check if something else needs to be done
    UPDATE_MERZ_METHODS = []
    SET_GLYPH_METHODS = [] # Methods to be called when the EditorWindow selected a new current glyph 
    MOUSE_MOVE_METHODS = []
    MOUSE_UP_METHODS = []
    MOUSE_DOWN_METHODS = []
    # Dictionary with key-method combinations where each part wants to subscribe on.
    # Each parts adds their key-method by self.registerKeyStroke(key, methodName).
    # The receiving method must be able to handle self.mePartMethodKey(g, c, event), where:
    # commandDown = event['commandDown']
    # shiftDown = event['shiftDown']
    # controlDown = event['controlDown']
    # optionDown = event['optionDown']
    # capLock = event['capLockDown']

    KEY_STROKE_METHODS = {}
    # Controller methods
    BUILD_UI_METHODS = []
    
    ITALIC_ANGLE = 0

    #   E V E N T S

    def registerKeyStroke(self, c, methodName):
        """Let parts register the keyStroke-methodName combination that they want to listen to."""
        if not c in self.KEY_STROKE_METHODS:
            self.KEY_STROKE_METHODS[c] = set()
        self.KEY_STROKE_METHODS[c].add(methodName)

    #   F I L E P A T H S

    def filePath2ParentPath(self, filePath):
        """Answer the parent path of filePath."""
        return '/'.join(filePath.split('/')[:-1]) + '/'
      
    def getUfoPaths(self, path):
        """Answer all ufo paths in the path directory. If the class variable UFO_PATHS 
        is defined by an inheriting assistant class, then these are returned."""
        ufoPaths = self.UFO_PATHS
        if ufoPaths is not None:
            return ufoPaths
        paths = []
        for fileName in os.listdir(path):
            if fileName.endswith('.ufo'):
                paths.append(path + fileName)
        return paths

    # Caching of open fonts without interface. Once a font get opened with a FontWindow,
    # it will be removed from this dictionary.          
    bgFonts = {} # Key is fullPath, value is RFont without showing interface

    def path2FullPath(self, path):
        """Using the class value PROJECT_PATH to construct the full path. If path is None,
        then we can't make a full path. Then just answer None."""
        if path is not None:
            if path.startswith('/'):
                return path
            fullDirPath = self.PROJECT_PATH
            if not fullDirPath.endswith('/'):
                fullDirPath = '/'.join(fullDirPath.split('/')[:-1]) + '/'
            return fullDirPath + path
        return None # Can't make a full path.

    def getFont(self, filePath, showInterface=False):
        """Answer the RFont if it is already open. Otherwise open it for read-only and store it into 
        the class variable self.bgFonts[filePath]"""
        fullPath = self.path2FullPath(filePath) # Make sure it's a full path, in case filePath is relative.

        if fullPath is None or not os.path.exists(fullPath):
            print(f'### getFont: Cannot find UFO {fullPath}')
            return None

        for f in AllFonts(): # Otherwise search if it already open
            if fullPath == f.path:
                if fullPath in self.bgFonts: # It was opened before, but now RoboFont has it open.
                    del self.bgFonts[fullPath]
                return f

        if showInterface:
            if fullPath in self.bgFonts: # It was opened before, but now RoboFont has it open.
                f = self.bgFonts[fullPath]
                f.openInterface()
                del self.bgFonts[fullPath]
            else:
                f = OpenFont(fullPath, showInterface=True) # Make sure it gets open
            return f
        
        if fullPath in self.bgFonts: # If it was already opened in the background, then just answer it
            return self.bgFonts[fullPath]
        
        # Otherwise just open it in the background and cache it
        f = OpenFont(fullPath, showInterface=False)
        self.bgFonts[fullPath] = f
        return f
    
    def path2UfoName(self, path):
        return path.split('/')[-1]

    #   D A T A

    def getMasterData(self, f):
        """Answer the MasterData instance for this font, containing meta-information about the entire font."""
        ufoName = self.path2UfoName(f.path)
        if self.MASTER_DATA is not None and ufoName in self.MASTER_DATA:
            return self.MASTER_DATA[ufoName]
        # Otherwise just answer a default MasterData for f
        print(f'### Cannot find MasterData for {ufoName}')
        return MasterData(f)

    def getGlyphData(self, f, gName):
        """Answer the GlyphData instance for this glyph, containing meta-information."""
        gd = GlyphData(f, gName)
        return gd 

    #   L I B

    LIB_KEY = 'com.typetr'

    def getLib(self, fOrG, key, defaultValue):
        if fOrG is None:
            return defaultValue
        if not self.LIB_KEY in fOrG.lib:
            fOrG.lib[self.LIB_KEY] = {}
        if not key in fOrG.lib[self.LIB_KEY]:
            self.setLib(fOrG, key, defaultValue)
        return fOrG.lib[self.LIB_KEY][key]

    def setLib(self, fOrG, key, value):
        if fOrG is not None:
            if self.LIB_KEY not in fOrG.lib:
                fOrG.lib[self.LIB_KEY] = {}
            fOrG.lib[self.LIB_KEY][key] = value

    #   G L Y P H

    def copyGlyph(self, srcFont, glyphName, dstFont=None, dstGlyphName=None, copyUnicode=True):
        """If dstFont is omitted, then the dstGlyphName (into the same font) should be defined.
        If dstGlyphName is omitted, then dstFont (same glyph into another font) should be defined.
        Note that this also overwrites/copies the anchors.
        """
        assert glyphName in srcFont, (f'### copyGlyph: Glyph /{glyphName} does not exist source font {srcFont.path}')
        if dstFont is None:
            dstFont = srcFont
        if dstGlyphName is None:
            dstGlyphName = glyphName
        assert srcFont != dstFont or glyphName != dstGlyphName, ('### copyGlyph: Either dstFont or dstGlyphName should be defined.')
        srcGlyph = srcFont[glyphName]
        dstFont.insertGlyph(srcGlyph, name=dstGlyphName)
        return dstFont[dstGlyphName]

    #   P O I N T S

    def distance(self, px1, py1, px2, py2):
        return math.sqrt((px1 - px2)**2 + (py1 - py2)**2)

class Assistant(BaseAssistant, Subscriber):

    # Editor window drawing parameters
    SPACE_MARKER_R = 16 # Radius of spacing markers at the baseline
    POINT_MARKER_R = 6 # Radius of point markers
    
    controller = None
    
    #    B U I L D I N G
    
    def build(self):
        self.mouseClickPoint = None
        self.mouseDraggedPoint = None

        glyphEditor = self.getGlyphEditor()
        self.isUpdating = 0

        assert glyphEditor is not None
        
        self.foregroundContainer = container = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        
        self.backgroundContainer = bgContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )
        # self.INIT_MERZ_METHODS is to be redefined by inheriting assistant classes, so they can define 
        # their own set of components and UI."""
        for initMerzMethodName in self.INIT_MERZ_METHODS:
            getattr(self, initMerzMethodName)(container)
                
    # E V E N T S

    # Types of events to subscribe to
    #self.glyphEditorGlyphDidChange(info)
    #self.glyphEditorGlyphDidChangeInfo(info)
    #self.glyphEditorGlyphDidChangeOutline(info)
    #self.glyphEditorGlyphDidChangeComponents(info)
    #self.glyphEditorGlyphDidChangeAnchors(info)
    #self.glyphEditorGlyphDidChangeGuidelines(info)
    #self.glyphEditorGlyphDidChangeImage(info)
    #self.glyphEditorGlyphDidChangeMetrics(info)
    #self.glyphEditorGlyphDidChangeContours(info)
    #self.glyphEditorDidMouseDown(info)
    #self.glyphEditorDidMouseUp(info)
    #self.glyphEditorDidMouseDrag(info)
    #self.glyphEditorDidKeyDown(info):

    
    #def glyphEditorGlyphDidChange(self, info) # Better not use this one, as it also is triggered on lib changes.
    #   The editor selected another glyph. Update the visible Merz elements for the new glyph."""
        
    def glyphEditorGlyphDidChangeContours(self, info):
        """The editor did change contours"""
        #print("""The editor did change contours""", info['glyph'])
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)
        
    def glyphEditorGlyphDidChangeComponents(self, info):
        """The editor change components"""
        #print("""The editor did change components""", info['glyph'])
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)
        
    def glyphEditorDidSetGlyph(self, info):
        """Called when the GlyphEditor selects a new glyph"""
        #print("""The editor did set glyph""", info['glyph'])
        g = info['glyph']
        cg = CurrentFont()
        if g == cg:
            for setGlyphMethodName in self.SET_GLYPH_METHODS: 
                getattr(self, setGlyphMethodName)(g)
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)
        
    def glyphEditorDidMouseDown(self, info):
        g = info['glyph']
        g.prepareUndo()
        self.mouseClickPoint = p = info['locationInGlyph']
        for mouseDownMethodName in self.MOUSE_DOWN_METHODS:
            getattr(self, mouseDownMethodName)(g, p.x, p.y)
        self.updateMerz(info)
    
    def glyphEditorDidMouseUp(self, info):
        # Reset terminal stuff
        self.mouseClickPoint = None
        self.mouseDraggedPoint = None
        for mouseDownMethodName in self.MOUSE_UP_METHODS:
            getattr(self, mouseDownMethodName)(g, p.x, p.y)
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)

    def glyphEditorDidMouseMove(self, info):
        g = info['glyph']
        p = info['locationInGlyph']
        for mouseMoveMethodName in self.MOUSE_MOVE_METHODS:
            getattr(self, mouseMoveMethodName)(g, p.x, p.y)
    
    def glyphEditorDidMouseDrag(self, info):
        self.mouseDraggedPoint = info['locationInGlyph']

    def glyphEditorDidKeyDown(self, info):
        # User specific key strokes to be added here

        g = info['glyph']
        cg = CurrentGlyph()
        if g.font.path != cg.font.path:
            # Not the current glyph, ignore the key stroke
            return

        gd = self.getGlyphData(g.font, g.name)
         
        event = extractNSEvent(info['NSEvent'])
        cc = event['keyDown']
       
        #commandDown = event['commandDown']
        #shiftDown = event['shiftDown']
        #controlDown = event['controlDown']
        #optionDown = event['optionDown']
        #self.capLock = event['capLockDown']

        changed = False

        """Translate the user key stroke to application key stroke. Of the user based TRANSLATE_KEYS
        is None, then answer None, indicating the assistant should ingnore this key."""
        c = self.TRANSLATE_KEYS.get(cc, cc) # Answer c if not define in the dictionary.
        if c is not None and c in self.KEY_STROKE_METHODS: # Otherwise skip the key stroke
            for keyStrokeMethodName in self.KEY_STROKE_METHODS[c]:
                print(f'... [{c}] {keyStrokeMethodName} {g.name} {g.font.path}')
                getattr(self, keyStrokeMethodName)(g, c, event)

    def started(self):
        pass
            
    def destroy(self):
        self.foregroundContainer.clearSublayers()

    def getController(self):
        """Answer the controller. We need this method to be compatible in case of controller.getController()"""
        return self.controller

    def update(self, info):
        """The glyph changed. Check is something else needs to be done."""
        if self.isUpdating:
            return
        self.isUpdating = True
        # Let the parts do updating work too, in case that is necessary
        for updateMethod in self.UPDATE_METHODS:
            getattr(self, updateMethod)(info)
        self.isUpdating = False

    def updateMerz(self, info):
        """Update the Merz objects for all activated Merz components"""
        if self.isUpdating:
            return
        self.isUpdating = True

        g = info['glyph']
        if g is None:
            return
        fg = g.getLayer('foreground')
        if fg.markColor != self.VISITED_MARKER: # NO_MARKER or different marker
            fg.markColor = self.VISITED_MARKER # Change to the marker color of this user

        # Update Merz elements, in case things changed to the shapes
        for updateMerzMethodName in self.UPDATE_MERZ_METHODS:
            getattr(self, updateMerzMethodName)(info)
        self.isUpdating = False

class AssistantController(BaseAssistant, WindowController):

    # Default constants, to be overwritten by inheriting classes
    W, H = 250, 250 # Width and height of the main window
    M = 8 # Margins and gutter of the main window UI
    L = 22 # Distance between UI controls
    COLS = 3 # Number of columns on the UI window
            
    # Editor window drawin parameters for kerning
    KERN_LINE_SIZE = 32 # Number of glyphs on kerning line
    KERN_SCALE = 0.15 # Calibration factor for AI kerning
        
    assistantGlyphEditorSubscriberClass = BaseAssistant

    # Inheriting class can overwrite this default class variable to alter type of window 
    #WINDOW_CLASS = vanilla.Window
    WINDOW_CLASS = FloatingWindow
        
    NAME = 'Base Assistant'

    def build(self):
        """Build the controller window."""
        
        # Reference to the redefined MASTER_DATA and PROJECT_PATH from the main Assistant class
        self.MASTER_DATA = self.assistantGlyphEditorSubscriberClass.MASTER_DATA
        self.PROJECT_PATH = self.assistantGlyphEditorSubscriberClass.PROJECT_PATH

        f = CurrentFont()
        f.lib[self.LIB_KEY] = {}

        # Can't do these as class variable, since they may depend on inheritied self.W, self.H, self.COLS, etc.        
        self.CW = (self.W - (self.COLS + 1) * self.M)/self.COLS
        self.C0 = self.M
        self.C1 = self.C0 + self.CW + self.M
        self.C2 = self.C1 + self.CW + self.M

        y = self.M
        self.w = self.WINDOW_CLASS((self.W, self.H), self.NAME, minSize=(self.W, self.H))
        self.buildUI(y) # y goes down, depending how much the UI components need
        self.w.open()
                
    def buildUI(self, y):
        """Default user interface controllers. The selection of controls by an inheriting
        assistant class also defines the available functions."""
        for buildUIMethodName in self.BUILD_UI_METHODS:
            y = getattr(self, buildUIMethodName)(y)
        self.w.saveAllButton = Button((self.C2, -self.L-self.M, self.CW, self.L), 'Save all', callback=self.saveAllCallback)

    def saveAllCallback(self, sender):
        for f in AllFonts():
            print(f'... Save {f.path}')
            f.save()

    def updateEditor(self, sender):
        g = CurrentGlyph()
        if g is not None:
            g.changed()
                  
    # Handle subscriptions to the EditorWindow events
    
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None

    def getController(self):
        """Answer the controller. We need this method to be compatible in case of controller.getController()"""
        return self

