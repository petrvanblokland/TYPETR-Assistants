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

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

FAR = 100000 # Put drawing stuff outside the window

class MasterData:
    """Storing additional data about masters, without storing the actual RFont instance. 
    The font can be retrieves by baseAssistant.getMaster(self.path)
    """
    def __init__(self, f, srcPath=None, orgPath=None, romanItalicPath=None,
            kerningSrcPath=None, displaySrcPath=None,
            m0=None, m1=None, m2=None, sm1=None, sm2=None, dsPosition=None,
            tripletData1=None, tripletData2=None, featurePath=None, 
            glyphData=None, metrics=None,
            HStem=None, HThin=None, OStem=None, OThin=None,
            HscStem=None, HscThin=None, OscStem=None, OscThin=None,
            nStem=None, oStem=None, oThin=None, UThin=None, VThin=None, eThin=None,
        ):
        self.path = f.path
        self.italicSkew = f.info.italicAngle
        self.rotation = radians(f.info.italicAngle) 
        self.isItalic = bool(f.info.italicAngle)
        # Referencing related masters by relative path
        self.srcPath = srcPath # "Original" master of this font, copy from here
        self.orgPath = orgPath # "Original" master of this font
        self.romanItalicPath = romanItalicPath # Roman <---> Italic master reference
        self.kerningSrcPath = kerningSrcPath 
        self.displaySrcPath = displaySrcPath # Show this outline on the background
        # Interpolation & design space
        self.interpolationFactor = 0.5
        self.m0 = m0 # Regular origin
        self.m1 = m1 # Direct interpolation master in "min" side
        self.m2 = m2 # Direct interpolation master on "max" side
        self.sm1 = sm1
        self.sm2 = sm2, # Scalerpolate masters for condensed and extended making. 
        self.dsPosition = dsPosition # Design space position (matching .designspace) to calculate triplet kerning
        self.tripletData1 = tripletData1
        self.tripletData2 = tripletData2, # Compatible triplet sets of (name1, name2, name3, kerning) tuples for interpolation.
        self.featurePath = featurePath
        # Glyphs
        if glyphData is None:
            glyphData = {}
        self.glyphData = glyphData
        if metrics is None:
            metrics = {}
        self.metrics = metrics 
        self.HStem = HStem
        self.HThin = HThin
        self.OStem = OStem
        self.OThin = OThin
        self.HscStem = HscStem
        self.HscThin = HscStem
        self.OscStem = OscStem
        self.OscThin = OscThin
        self.nStem = nStem
        self.oStem = oStem
        self.oThin = oThin
        self.UThin = UThin
        self.VThin = VThin
        self.eThin = eThin
        # Info
        self.ttfPath=None
        self.ttfPath=None, platformID=None, platEncID=None, langID=None, 
        unitsPerEm=UNITS_PER_EM,
        copyright=COPYRIGHT, uniqueID=None, trademark=TRADEMARK, lowestRecPPEM=LOWEST_PPEM,
        familyName=None, styleName=None,
        fullName=None, version=None, versionMajor=VERSION_MAJOR, versionMinor=VERSION_MINOR,
        postscriptName=None, preferredFamily=None, preferredSubFamily=None,
        openTypeOS2WinAscent=OS2_WIN_ASCENT, openTypeOS2WinDescent=OS2_WIN_DESCENT,
        openTypeOS2Type=[2, 8], # fsType, TN standard
        vendorURL=VENDOR_URL, manufacturerURL=MANUFACTURER_URL, manufacturer=MANUFACTURER,
        designerURL=DESIGNER_URL, designer=DESIGNER, 
        eulaURL=EULA_URL, eulaDescription=EULA_DESCRIPTION,
        underlinePosition=None, underlineThickness=UNDERLINE_THICKNESS

class GlyphData:
    def __init__(self, f, gName):
        self.name = gName

class BaseAssistant:
    """Share functions and class variables for both Assistant and AssistantController"""

    UFO_PATHS = None # Must be redefined by inheriting assistant classes

    # Names of methods to call for initializeing and updating Merz. 
    # To be defined by inheriting classes. 
    INIT_MERZ_METHODS = []
    UPDATE_MERZ_METHODS = []
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
                
    fonts = {}
    def getFont(self, filePath):
        """Answer the RFont if it is already open. Otherwise open it for read-only and store it into 
        the class variable self.fonts[filePath]"""
        for f in AllFonts():
            if filePath == f.path:
                if filePath in self.fonts: # It was opened before, but not RoboFont has it open.
                    del self.fonts[filePath]
                return f
        
        if filePath in self.fonts:
            return self.fonts[filePath]
            
        if os.path.exists(filePath):
            f = OpenFont(filePath, showInterface=False)
            self.fonts[filePath] = f
            return f
        return None
    
    def getMasterData(self, f):
        """Answer the MasterData instance for this font, containing meta-information about the entire font."""
        md = MasterData(f)
        return md 

    def getGlyphData(self, f, gName):
        """Answer the GlyphData instance for this glyph, containing meta-information."""
        gd = GlyphData(f, gName)
        return gd 

class Assistant(BaseAssistant, Subscriber):

    # Editor window drawing parameters
    SPACE_MARKER_R = 16 # Radius of spacing markers at the baseline
    POINT_MARKER_R = 6 # Radius of point markers
    
    controller = None
    
    #    B U I L D I N G
    
    def build(self):
        glyphEditor = self.getGlyphEditor()
        self.isUpdating = False

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
    
    def glyphEditorGlyphDidChange(self, info):
        self.updateMerz(info)
        
    def glyphEditorDidSetGlyph(self, info):
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


