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


class BaseAssistant:
    """Share functions and class variables for both Assistant and AssistantController"""

    # Must be redefined by inheriting assistant classes where to find the main UFO master files
    UFO_PATH = 'ufo/' # Standard place for UFO files
    UFO_PATHS = None 

    # If there's masterData available, then this should be redefined as dictionaty by inheriting Assistant classes
    MASTER_DATA = None 

    # Names of methods to call for initializeing and updating Merz. 
    # To be defined by inheriting classes. 
    INIT_MERZ_METHODS = []
    UPDATE_MERZ_METHODS = []
    SET_GLYPH_METHODS = [] # Methods to be called when the EditorWindow selected a new current glyph 
    MOUSE_MOVE_METHODS = []
    MOUSE_DOWN_METHODS = []
    # Controller methods
    BUILD_UI_METHODS = []
        
    def build(self):
        
        self.mouseClickPoint = None
        self.mouseDraggedPoint = None

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
            print(f'### Cannot find UFO {fullPath}')
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
    
    def path2UfoPath(self, path):
        return path.split('/')[-1]

    def getMasterData(self, f):
        """Answer the MasterData instance for this font, containing meta-information about the entire font."""
        ufoName = self.path2UfoPath(f.path)
        if self.MASTER_DATA is not None and ufoName in self.MASTER_DATA:
            return self.MASTER_DATA[ufoName]
        # Otherwise just answer a default MasterData for f
        print(f'### Cannot find MasterData for {ufoName}')
        return MasterData(f)

    def getGlyphData(self, f, gName):
        """Answer the GlyphData instance for this glyph, containing meta-information."""
        gd = GlyphData(f, gName)
        return gd 

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



class Assistant(BaseAssistant, Subscriber):

    # Editor window drawing parameters
    SPACE_MARKER_R = 16 # Radius of spacing markers at the baseline
    POINT_MARKER_R = 6 # Radius of point markers
    
    controller = None
    
    #    B U I L D I N G
    
    def build(self):
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
        # To be redefined by inheriting assistant classes, so they can define 
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
    
    #def glyphEditorGlyphDidChange(self, info) # Better no use this one, as it also is triggered on lib changes.
    #   The editor selected another glyph. Update the visible Merz elements for the new glyph."""
        
    def glyphEditorGlyphDidChangeContours(self, info):
        """The editor did change contours"""
        #print("""The editor did change contours""", info['glyph'])
        self.updateMerz(info)
        
    def glyphEditorGlyphDidChangeComponents(self, info):
        """The editor change components"""
        #print("""The editor did change components""", info['glyph'])
        self.updateMerz(info)
        
    def glyphEditorDidSetGlyph(self, info):
        """Called when the GlyphEditor selects a new glyph"""
        #print("""The editor did set glyph""", info['glyph'])
        g = info['glyph']
        cg = CurrentFont()
        if g == cg:
            for setGlyphMethodName in self.SET_GLYPH_METHODS: 
                getattr(self, setGlyphMethodName)(g)
        self.updateMerz(info)
        
    def glyphEditorDidMouseDown(self, info):
        g = info['glyph']
        self.mouseClickPoint = p = info['locationInGlyph']
        for mouseDownMethodName in self.MOUSE_DOWN_METHODS:
            getattr(self, mouseDownMethodName)(g, p.x, p.y)
    
    def glyphEditorDidMouseUp(self, info):
        # Reset terminal stuff
        self.mouseClickPoint = None
        self.mouseDraggedPoint = None
    
    def glyphEditorDidMouseMove(self, info):
        g = info['glyph']
        p = info['locationInGlyph']
        for mouseMoveMethodName in self.MOUSE_MOVE_METHODS:
            getattr(self, mouseMoveMethodName)(g, p.x, p.y)
    
    def glyphEditorDidMouseDrag(self, info):
        self.mouseDraggedPoint = info['locationInGlyph']

    def started(self):
        pass
            
    def destroy(self):
        self.foregroundContainer.clearSublayers()

    def getController(self):
        """Answer the controller. We need this method to be compatible in case of controller.getController()"""
        return self.controller

    def updateMerz(self, info):
        """Update the Merz objects for all activated Merz components"""
        if self.isUpdating:
            return
        self.isUpdating = True
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
        
        f = CurrentFont()
        f.lib[self.LIB_KEY] = {}

        # Can't do these as class variable, since they may depend on inheritied self.W, self.H, self.COLS, etc.        
        self.CW = (self.W - (self.COLS + 1) * self.M)/self.COLS
        self.C0 = self.M
        self.C1 = self.C0 + self.CW + self.M
        self.C2 = self.C1 + self.CW + self.M

        y = self.M
        self.w = self.WINDOW_CLASS((self.W, self.H), self.NAME, minSize=(self.W, self.H))
        y = self.buildUI(y) # y goes down, depending how much the UI components need
        self.w.open()
                
    def buildUI(self, y):
        """Default user interface controllers. The selection of controls by an inheriting
        assistant class also defines the available functions."""
        for buildUIMethodName in self.BUILD_UI_METHODS:
            y = getattr(self, buildUIMethodName)(y)
        return y

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

