# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   baseAssistant.py
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
from assistantLib.assistantParts.data import MasterData

import assistantLib.assistantParts.spacingKerning.kerningManager
importlib.reload(assistantLib.assistantParts.spacingKerning.kerningManager)
from assistantLib.assistantParts.spacingKerning.kerningManager import KerningManager

import assistantLib.toolbox.glyphAnalyzer
importlib.reload(assistantLib.toolbox.glyphAnalyzer)
from assistantLib.toolbox.glyphAnalyzer import GlyphAnalyzer

from assistantLib.assistantParts.glyphsets.anchorData import AD

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

FAR = 100000 # Put drawing stuff outside the window

# Some global storage, that can be reached from Controllers as well as Subscribers

GLOBAL_BG_FONTS = {} # Global storage. Key is fullPath, value is RFont without showing interface
GLOBAL_GLYPH_ANALYZERS = {} # Key is font path, value is dictionary of GlyphAnalyzer instances 
GLOBAL_KERNING_MANAGERS = {} # Key is font path, value is the related KerningManager instance.

class BaseAssistant:
    """Share functions and class variables for both Assistant and AssistantController.
    - Personalized marker colors for visited glyphs in the FontWindow
    - Personalized dictionary for function keys
    """

    BUILD_VERSION = 0 # Build version number. To be redefined by inheriting assistant classes.

    # Select the color by user
    VISITED_MARKERS = [
        #('/Users/petr/Desktop/TYPETR-git', (40/255, 120/255, 255/255, 0.6), keys), # "Final" marker Blue (Petr))    
        ('/Users/petr/Desktop/TYPETR-git', (50/255, 70/255, 230/255, 0.8), {'§':'§'}), # "Final" marker Blue (Petr))    
        ('/Users/edwarddzulaj/Documents', (92/255, 149/255, 190/255, 1), {}), # Edward
        ('/Users/graemeswank/Documents', (255/255, 83/255, 73/255, 1), {}),
        ('/Users/graeme/Documents', (255/255, 83/255, 73/255, 1), {}),
        ('/Users/caterinasantullo/Desktop', (226/255, 69/255, 0/255, 1), {}),
        ('/Users/til/Documents', (0.9, 0.75, 1.0, 1.0), {'g':'z'}),
        ('/Users/anna/Downloads', (57/255, 163/255, 160/255, 1), {}),
        ('/Users/annakhorash/Documents/GitHub', (57/255, 163/255, 160/255, 1), {}),
        ('/Users/lenalepommelet/Documents', (138/255, 43/255,  226/255, 1), {}),
        ('/Users/Marte/Documents', (255/255, 222/255,  0/255, .8), {}),
        ('/Users/iv/Documents/', (0/255, 130/255,  100/255, 1), {}),
    ]
    
    # Key translations from personalized key strokes are handled by the BaseAssistant.glyphEditorDidKeyDown
    TRANSLATE_KEYS = {} # Key strokes can be redefined as <org>:<local> if defined as dict(b='B', B=None, g='G', q='#')
    
    VISITED_MARKER = None
    for path, color, keys in VISITED_MARKERS:
        if __file__.startswith(path):
            VISITED_MARKER = color
            print(f'User color for {path}, {color}')
            TRANSLATE_KEYS = keys
            break
    if VISITED_MARKER is None:
        VISITED_MARKER = (1, 1, 1, 1) # Clear to white

    # Make these keys available for parts by class constant.
    UP_ARROW_FUNCTION_KEY = NSUpArrowFunctionKey
    DOWN_ARROW_FUNCTION_KEY = NSDownArrowFunctionKey
    LEFT_ARROW_FUNCTION_KEY = NSLeftArrowFunctionKey
    RIGHT_ARROW_FUNCTION_KEY = NSRightArrowFunctionKey
    PAGE_UP_FUNCTION_KEY = NSPageUpFunctionKey
    PAGE_DOWN_FUNCTION_KEY = NSPageDownFunctionKey
    PAGE_HOME_FUNCTION_KEY = NSHomeFunctionKey
    PAGE_END_FUNCTION_KEY = NSEndFunctionKey

    # If arrow keys are used, then always update the glyph.
    ARROW_KEYS = [UP_ARROW_FUNCTION_KEY, DOWN_ARROW_FUNCTION_KEY,
            LEFT_ARROW_FUNCTION_KEY, RIGHT_ARROW_FUNCTION_KEY, PAGE_UP_FUNCTION_KEY,
            PAGE_DOWN_FUNCTION_KEY, PAGE_HOME_FUNCTION_KEY, PAGE_END_FUNCTION_KEY]

    # Must be redefined by inheriting assistant classes where to find the main UFO master files
    UFO_PATH = 'ufo/' # Standard place for UFO files
    UFO_PATHS = None 

    # If there's masterData available, then this should be redefined as dictionaty by inheriting Assistant classes
    MASTER_DATA = None 

    # Names of methods to call for initializeing and updating Merz. 
    # To be defined by inheriting classes. 
    INIT_MERZ_METHODS = []
    UPDATE_METHODS = [] # Something changed to the glyph. Check if something else needs to be done
    UPDATE_MERZ_METHODS = []
    SET_GLYPH_METHODS = [] # Methods to be called when the EditorWindow selected a new current glyph 
    MOUSE_MOVE_METHODS = []
    MOUSE_DRAG_METHODS = []
    MOUSE_UP_METHODS = []
    MOUSE_DOWN_METHODS = []
    CLOSING_WINDOW_METHODS = [] # Methods for parts to subscribe on the event that the main assistant window is about to close.
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

    # Point types
    POINTTYPE_BEZIER = 'curve'
    POINTTYPE_QUADRATIC = 'qcurve'
    POINTTYPE_OFFCURVE = 'offcurve'

    # Attaching layer functions to layer names.
    EDIT_LAYER = 'foreground' # Name of the main layer to edit. Could be on background, such as Upgrade Neon
    BACKGROUND_LAYER = 'background'
    PRESENTATION_LAYER = 'background'

    #   E V E N T S

    def registerKeyStroke(self, c, methodName):
        """Let parts register the keyStroke-methodName combination that they want to listen to.
        Answer the actual personalized key, depending if it's redefined in self.TRANSLATE_KEYS."""
        c = self.TRANSLATE_KEYS.get(c, c)
        if not c in self.KEY_STROKE_METHODS:
            self.KEY_STROKE_METHODS[c] = set()
        self.KEY_STROKE_METHODS[c].add(methodName)
        return c # Answer the personalize key that this method got registered to.

    def fixAllOfTheseGlyphsKey(self, g, c, event):
        """Force check/fix on the glyphs with the same name in all open fonts."""
        for f in self.getAllOpenFonts():
            if g.name in f:
                f[g.name].changed() # Force check/fix on the glyphs with the same name in all open fonts.

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
    bgFonts = GLOBAL_BG_FONTS # Key is fullPath, value is RFont without showing interface

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
        if filePath is None:
            return None

        fullPath = self.path2FullPath(filePath) # Make sure it's a full path, in case filePath is relative.

        assert fullPath is not None and os.path.exists(fullPath), (f'### Cannot find {fullPath}')

        for f in self.getAllOpenFonts(): # Otherwise search if it already open
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
        if f is not None:
            ufoName = self.path2UfoName(f.path)
            if self.MASTER_DATA is not None and ufoName in self.MASTER_DATA:
                return self.MASTER_DATA[ufoName]
            # Otherwise just answer a default MasterData for f
            print(f'### Cannot find MasterData for {ufoName}')
            return MasterData(f)
        return None

    def getGlyphData(self, g):
        """Answer the GlyphData instance for this glyph, containing meta-information. It's either derives from g.lib
        or constructed from guessed information."""
        if g is not None:  
            md = self.getMasterData(g.font)
            if md is not None:
                gd = md.glyphSet.get(g.name)
                if gd is not None:
                    return gd
            print(f'### Cannot find GlyphData for {g.name}')
        return None

    #   A N A L Y Z E R S

    # The overhead difference between resetting a GlyphAnalyzer is so small that we as well just create
    # a new one, instead of caching it. If something changes in the glyph, then just create a new instance.

    def getGlyphAnalyzer(self, g):
        """Answer the glyph analzyer for /g."""
        return GlyphAnalyzer(g) # /g is not stored in the analyzer instance.

    #   S P A C I N G  &  K E R N I N G

    SIM_CLIP = 300 # Default range to look "into" glyph sides for 1000 em. Will be corrected for actual f.info.unitsPerEm
    kerningManagers = GLOBAL_KERNING_MANAGERS # Key is font path, value is the related KerningManager instance.

    def getKerningManager(self, f):
        if not f.path in self.kerningManagers:
            md = self.getMasterData(f)
            simClip = self.SIM_CLIP * f.info.unitsPerEm / 1000 # Correct for other em-squares.
            self.kerningManagers[f.path] = KerningManager(f, md, simClip=simClip)
        return self.kerningManagers[f.path]

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

    #   F O N T

    def getCurrentFont(self):
        """Answer the current font. By default this the result of CurrentFont(), but it can be altered by
        inheriting assistant classes to force another current font selection."""
        return CurrentFont()
    
    def getAllOpenFonts(self):
        """Answer a list with all current open fonts. By default this is the result of AllFonts(), but it can be altered by
        inheriting assistant classes to fore another set of font selection."""
        return AllFonts()

    def getAllUfoFonts(self):
        """Answer a list with all fonts in the current ufo/ if they are defined in the master data. If the font
        is not open, then open it on the background."""
        ufos = []
        f = self.getCurrentFont()  
        parentPath = self.filePath2ParentPath(f.path)                        
        for ufoPath in enumerate(self.getUfoPaths(parentPath)):
            ufo = self.getFont(ufoPath)
            if ufo is not None:
                ufos.append(ufo)
        return ufos

    def openGlyphWindow(self, g, newWindow=False):
        """Open this glyph in a RoboFont glyph window, if it is not open of if newWindow is set to True.
        Otherwise open the glyph in the window of the current glyph.
        """
        if g is not None:
            OpenGlyphWindow(g, newWindow=newWindow)

    def isEqualFont(self, f1, f2):
        """Answer the boolean flag if f1 and f2 are the same font. Point to the same path is also True."""
        if f1 is None or f2 is None:
            return False
        if f1 is f2 or f1 == f2:
            return True
        if f1.path == f2.path:
            return True
        return False

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
        #if srcFont.path == dstFont.path:
        #    assert glyphName != dstGlyphName, (f'### copyGlyph: Either srcFont {srcFont} != dstFont {dstFont} or /{glyphName} != dstGlyphName /{dstGlyphName} should be defined.')
        #srcGlyph = srcFont[glyphName]
        print(f'... Copy /{glyphName} to /{dstGlyphName}')
        dstFont[dstGlyphName] = srcFont[glyphName]
        #dstFont.insertGlyph(srcGlyph, name=dstGlyphName)
        return dstFont[dstGlyphName]

    def getCurrentGlyph(self, layerName=EDIT_LAYER):
        """Answer the current glyph. By default this the result of CurrentGlyph, but it can be altered by
        inheriting assistant classes to force the current glyph as another layer (e.g. as in Responder and Upgrade Neon,
        where the "background" layer is return as working area. Answer None if there is no current glyph selected."""
        g = CurrentGlyph()
        if g is None:
            return None
        return g.getLayer(layerName)

    def isCurrentGlyph(self, g):
        """Answers te boolean flag if the g is the current glyph."""
        cg = self.getCurrentGlyph()
        if g is None or cg is None:
            return False
        return g.name == cg.name and g.font.path == cg.font.path

    def doesInterpolate(self, g, fix=True, verbose=False):
        """Answer the boolean flag if this glyphs interpolates with the md.m0 master. Note that this is quick check,
        mostly on the amount of points for each contour."""
        f = g.font
        md = self.getMasterData(f)
        gd = self.getGlyphData(g)
        ref = self.getFont(md.m0)
        changed = False
        if ref is not None and g.name in ref:
            refG = ref[g.name]
            # Test components
            if len(refG.components) != len(g.components):
                if verbose:
                    print(f'### {md.name} /{g.name} Incompatible amount of components {len(g.components)} -- {len(refG.components)}')
                return False
            # We no longer do this from the reference glyph per 2025-03-28
            # Component module will take care of this, using the GlyphData of the glyph instead.
            # for cIndex, refComponent in enumerate(refG.components):
            #     component = g.components[cIndex]
            #     if component.baseGlyph != refComponent.baseGlyph:
            #         if verbose:
            #             print(f'### {md.name} /{g.name} Incompatible baseGlyph in component {cIndex} /{component.baseGlyph} -- /{refComponent.baseGlyph}')
            #         if fix: # We can do this simple fix here, if allowed
            #             print('SAASASASSASSAASAS', component.baseGlyph, refComponent.baseGlyph)
            #             component.baseGlyph = refComponent.baseGlyph
            #             changed = True
            #         else:
            #             return False
            # Test contours
            if len(refG.contours) != len(g.contours):
                if verbose:
                    print(f'### {md.name} /{g.name} Incompatible amount of contours {len(g.contours)} -- {len(refG.contours)})')
                return False
            for cIndex, refContour in enumerate(refG.contours):
                contour = g.contours[cIndex]
                points = contour.points
                refPoints = refContour.points
                if len(refPoints) != len(points):
                    if verbose:
                        print(f'### {md.name} /{g.name} Incompatible amount of points in contour {cIndex} {len(points)} -- {len(refPoints)})')
                    return False
                for pIndex, refP in enumerate(refPoints):
                    p = points[pIndex]
                    if refP.type != p.type:
                        if verbose:
                            print(f'### {md.name} /{g.name} Incompatible amount points type in contour {cIndex} #{pIndex} {p.type} -- {refP.type})')
                        return False
        
        if changed: # Fixed something, the report
            g.changed()
        return True

    def getBaseGlyph(self, g):
        """If g has a base glyph component, then answer the base glyph. Otherwise answer None."""
        gd = self.getGlyphData(g)
        if gd is not None and gd.base and gd.base in g.font:
            return g.font[gd.base]
        return None

    def getBaseGlyphOffset(self, g):
        """If the offset of the component is needed, then use this method. It answers the base glyph and a tuple for the transformation offset."""
        gd = self.getGlyphData(g)
        if gd is not None and gd.base and gd.base in g.font:
            for component in g.components:
                if gd.base == component.baseGlyph:
                     return g.font[gd.base], component.transformation[-2:]
        return None, (0, 0)

    def scaleGlyph(self, g, sx, sy=None):
        if sy is None:
            sy = sx
        for component in g.components:
            t = list(component.transformation)
            t[-2] = int(round(t[-2] * sx))
            t[-1] = int(round(t[-1] * sy))
            component.transformation = t
        for contour in g.contours:
            for p in contour.points:
                p.x = int(round(p.x * sx))
                p.y = int(round(p.y * sy))
        for anchor in g.anchors:
            anchor.x = int(round(anchor.x * sx))
            anchor.y = int(round(anchor.y * sy))
        g.width = int(round(g.width * sx))


    def offsetGlyph(self, g, dx=0, dy=0):
        for component in g.components:
            t = list(component.transformation)
            t[-2] = int(round(t[-2] + dx))
            t[-1] = int(round(t[-1] + dy))
            component.transformation = t
        for contour in g.contours:
            for p in contour.points:
                p.x = int(round(p.x + dx))
                p.y = int(round(p.y + dy))
        for anchor in g.anchors:
            anchor.x = int(round(anchor.x + dx))
            anchor.y = int(round(anchor.y + dy))

    def resetComponentPositions(self, g):
        for component in g.components:
            t = list(component.transformation)
            t[-2] = 0
            t[-1] = 0
            component.transformation = t

    def roundGlyph(self, g):
        for contour in g.contours:
            for point in contour.points:
                point.x = int(round(point.x))
                point.y = int(round(point.y))
        for component in g.components:
            t = list(component.transformation)
            t[-2] = int(round(t[-2]))
            t[-1] = int(round(t[-1]))
            component.transformation = t
        for anchor in g.anchors:
            anchor.x = int(round(anchor.x))
            anchor.y = int(round(anchor.y))
        g.width = int(round(g.width))

    #   A N C H O R S

    def getAnchorsDict(self, g):
        """Answer a dictionary with the anchors of g by their name."""
        anchors = {}
        for a in g.anchors:
            anchors[a.name] = a
        return anchors

    def getAnchorNames(self, g):
        """Answer a sorted list of anchor names in the glyph."""
        anchors = []
        for a in g.anchors:
            anchors.append(a.name)
        return sorted(anchors)

    def getAnchors(self, g):
        """Answer the selected anchors. If no anchors are selected, then answer a list with all anchors."""
        anchors = []
        for anchor in g.anchors:
            if anchor.selected:
                anchors.append(anchor)
        if anchors:
            return anchors # Just answer the selected anchor
        return g.anchors # Nothing selected, answer them all
        
    def getAccentAnchor(self, g, accentName):
        """Answer the named anchor, if it exits and if it an accent. Answer None otherwise."""
        if accentName in AD.ACCENT_DATA:
            return getAnchor(g, AD.ACCENT_DATA[accentName]) 
        return None

    def getBaseAnchor(self, g, accentName):
        """Answer the counterpart connected anchor of accentName, if it exits. Answer None otherwise."""
        if accentName in AD.ACCENT_DATA:
            anchorName = AD.ACCENT_DATA[accentName] 
            return getAnchor(g, AD.CONNECTED_ANCHORS[anchorName])
        return None
    
    def getCorrespondingAnchor(self, g, anchorName):
        """Answer the corresponding anchor in g if it exists. Answer None otherwise."""
        return self.getAnchor(g, AD.CONNECTED_ANCHORS.get(anchorName))
    
    def getAnchor(self, g, anchorName):
        """Answer the named anchor, if it exits. Answer None otherwise."""
        if g is not None:
            for anchor in g.anchors:
                if anchor.name == anchorName:
                    return anchor
        return None

    #   P O I N T S

    def distance(self, px1, py1, px2, py2):
        return sqrt((px1 - px2)**2 + (py1 - py2)**2)

    def hasSelectedPoints(self, g):
        """Answer the boolean flag if there is one or more points selected. E.g. italicize is using this
        to decide if the skew/rotate should be applied to the whole glyph (in case there is nothing or all selected).
        If there is a partial selection, then only skew/rotate the selected points."""
        for contour in g.contours:
            for p in contour.points:
                if p.selected:
                    return True
        return False

    def italicX(self, g, x, y, baseY=None):
        """Answer the italic x value on position e, depending on the italic angle of the font.
        If baseY is defined, then first project x on the baseline."""
        if y is None:
            return x
        if baseY is not None:
            x = self.italicX(g, x, -baseY)
        return x + int(round(tan(radians(-(g.font.info.italicAngle or 0))) * y))

    def isQuadratic(self, g):
        for contour in g.contours:
            for p in contour.points:
                if p.type == self.POINTTYPE_QUADRATIC:
                    return True
        return False

    def isBezier(self, g):
        for contour in g.contours:
            for p in contour.points:
                if p.type == self.POINTTYPE_BEZIER:
                    return True
        return False

    def isCurved(self, g):
        """Answer the boolean flag if this glyph has off-curve points"""
        for contour in g.contours:
            for p in contour.points:
                if p.type == self.POINTTYPE_OFFCURVE:
                    return True
        return False

    def getXBounds(self, g, y1, y2=None):
        """Answer points that are in the bounding box."""
        if y2 is None:
            y2 = y1
        p1 = p2 = None
        for contour in g.contours:
            for p in contour.points:
                if y1 <= p.y and p.y <= y2:
                    if p1 is None:
                        p1 = p
                    if p2 is None:
                        p2 = p
                    if p.x < p1.x:
                        p1 = p
                    if p.x > p2.x:
                        p2 = p
        return p1, p2


class Assistant(BaseAssistant, Subscriber):

    # Editor window drawing parameters
    SPACE_MARKER_R = 16 # Radius of spacing markers at the baseline
    POINT_MARKER_R = 6 # Radius of point markers
    
    controller = None
    
    #    B U I L D I N G
    
    def build(self):
        self.mouseClickPoint = None
        self.mouseDragPoint = None
        self.mouseMovePoint = None
        
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
    
    #   G L Y P H  E V E N T S

    def glyphEditorGlyphDidChangeMetrics(self, info):
        """The editor did change width"""
        #print("""The editor did change width""", info['glyph'])
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)
        
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
        cg = CurrentGlyph()
        if g == cg: # Handle subscribed methods of assistant parts, for current glyph only.
            for setGlyphMethodName in self.SET_GLYPH_METHODS: 
                getattr(self, setGlyphMethodName)(g)
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)
    
    #   M O U S E  E V E N T S

    def glyphEditorDidMouseDown(self, info):
        g = info['glyph']
        g.prepareUndo()

        event = extractNSEvent(info['NSEvent'])
        #commandDown = event['commandDown']
        #shiftDown = event['shiftDown']
        #controlDown = event['controlDown']
        #optionDown = event['optionDown']
        #capLock = event['capLockDown']

        self.mouseClickPoint = p = info['locationInGlyph']
        for mouseDownMethodName in self.MOUSE_DOWN_METHODS:
            getattr(self, mouseDownMethodName)(g, p.x, p.y, event)
        self.updateMerz(info)
    
    def glyphEditorDidMouseMove(self, info):
        g = info['glyph']
        
        event = extractNSEvent(info['NSEvent'])
        #commandDown = event['commandDown']
        #shiftDown = event['shiftDown']
        #controlDown = event['controlDown']
        #optionDown = event['optionDown']
        #capLock = event['capLockDown']

        # Save for assistant parts to use on an update, so they don't need their own even call.
        self.mouseMovePoint = p = info['locationInGlyph'] # Constantly keep track where the mouse is
        for mouseMoveMethodName in self.MOUSE_MOVE_METHODS: # In case the update is more urgent than a normal update call,
            getattr(self, mouseMoveMethodName)(g, p.x, p.y, event) # The assistant parts should implement and subscribe this method.
    
    def glyphEditorDidMouseDrag(self, info):
        g = info['glyph']
       
        event = extractNSEvent(info['NSEvent'])
        #commandDown = event['commandDown']
        #shiftDown = event['shiftDown']
        #controlDown = event['controlDown']
        #optionDown = event['optionDown']
        #capLock = event['capLockDown']

        self.mouseDragPoint = p = info['locationInGlyph']
        for mouseDragMethodName in self.MOUSE_DRAG_METHODS: # In case the update is more urgent than a normal update call,
            getattr(self, mouseDragMethodName)(g, p.x, p.y, event) # The assistant parts should implement and subscribe this method.

    def glyphEditorDidMouseUp(self, info):
        # Reset mouse moving stuff
        self.mouseClickPoint = None
        self.mouseDragPoint = None
        g = info['glyph']
       
        event = extractNSEvent(info['NSEvent'])
        #commandDown = event['commandDown']
        #shiftDown = event['shiftDown']
        #controlDown = event['controlDown']
        #optionDown = event['optionDown']
        #capLock = event['capLockDown']

        for mouseUpMethodName in self.MOUSE_UP_METHODS:
            getattr(self, mouseUpMethodName)(g, p.x, p.y, event)
        self.update(info) # Check if something else needs to be updated
        self.updateMerz(info)

    #   K E Y  E V E N T S

    def glyphEditorDidKeyDown(self, info):
        # User specific key strokes to be added here

        g = info['glyph']
        cg = self.getCurrentGlyph()
        if g.font.path != cg.font.path:
            # Not the current glyph, ignore the key stroke
            return

        gd = self.getGlyphData(g)
         
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
                print(f'... {keyStrokeMethodName} [{c}] {g.name} {g.font.path.split("/")[-1]}')
                getattr(self, keyStrokeMethodName)(g, c, event)
                changed = True

        elif c in self.ARROW_KEYS: # Always update the glyph if arrow keys are used.
            changed = True

        if changed:
            g.changed()

    def started(self):
        pass
            
    def destroy(self):
        self.foregroundContainer.clearSublayers()

    def getController(self):
        """Answer the controller. We need this method to be compatible in case of controller.getController()"""
        return self.controller

    def update(self, info):
        """The glyph changed. Check is something else needs to be done."""
        changed = False
        if self.isUpdating:
            return
        self.isUpdating = True
        # Let the parts do updating work too, in case that is necessary
        for updateMethod in self.UPDATE_METHODS:
            changed |= getattr(self, updateMethod)(info)
        if changed:
            info['glyph'].changed()
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
    KERN_LINE_LENGTH = 32 # Number of glyphs on kerning line
    KERN_SCALE = 0.15 # Calibration factor for AI kerning
    
    SHOW_PART_TITLES = True # Can be set to inheriting class to not show part titles below the separation lines.

    assistantGlyphEditorSubscriberClass = BaseAssistant

    # Inheriting class can overwrite this default class variable to alter type of window 
    #WINDOW_CLASS = Window
    WINDOW_CLASS = FloatingWindow
        
    NAME = 'Base Assistant'

    def build(self):
        """Build the controller window."""
        
        # Reference to the redefined MASTER_DATA and PROJECT_PATH from the main Assistant class
        self.MASTER_DATA = self.assistantGlyphEditorSubscriberClass.MASTER_DATA
        self.PROJECT_PATH = self.assistantGlyphEditorSubscriberClass.PROJECT_PATH

        f = self.getCurrentFont()
        assert f is not None, ('### Open a UFO before starting the assistant')
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
        c = self.getController()

        personalKey_f = self.registerKeyStroke('f', 'fixAllOfTheseGlyphsKey') # Check/fix the current glyph in all open fonts.

        for buildUIMethodName in self.BUILD_UI_METHODS:
            if self.SHOW_PART_TITLES:
                # Show title of the part over the line above
                y += 3
                setattr(self.w, 'partTitle-' + buildUIMethodName, TextBox((self.M, y-8, self.CW, 12), buildUIMethodName.replace('build', ''), sizeStyle='mini'))
                y += 1
            # Let the part build its UI and it returns the amount of vertical space it needed as new y
            y = getattr(self, buildUIMethodName)(y)

        # Some default buttons that every assistant window should have
        y = -2*self.L-self.M
        c.w.fixAllButton = Button((self.C0, y, self.CW, self.L), f'Fix all [{personalKey_f}]', callback=self.fixAllOpenFontsCallback)
        c.w.checkFixGlyphsetButton = Button((self.C1, y, self.CW, self.L), 'Fix glyphset', callback=self.checkFixGlyphSetCallback)
        c.w.saveAllButton = Button((self.C2, y, self.CW, self.L), 'Save all', callback=self.saveAllCallback)
        y += self.L
        c.w.fixAllSafety = CheckBox((self.C0, y, self.CW, self.L), 'Fix all safety', value=False, sizeStyle='small')
        c.w.fixGlyphSetSafety = CheckBox((self.C1, y, self.CW, self.L), 'Fix glyphset safety', value=False, sizeStyle='small')

    def fixAllOpenFontsCallback(self, sender):
        """This button will call automatic fixes on all open fonts that are available. And it will try to auto-fix as much as possible.
        Since not all parts may be loaded in the current assembly of the assistant, we need to check if certain functions are availalbe.

        * Check fix glyphset, based on contents of md.glyphSet. Add missing glyphs and remove obsolete glyphs
        """
        c = self.getController()
        if not c.w.fixAllSafety.get(): # Safe checkbox should be set for safety
            print(f'### Check [x] Fix all to enable this button.')
            return 
                   
        for f in [CurrentFont()]: #AllFonts(): #self.getAllOpenFonts():
            changed = False
            print(f'... Fixing all of {f.path.split("/")[-1]}')
            changed |= self.checkFixGlyphSet(f) # First check if all glyphs are there. Create missing, delete obsolete.
            #changed |= self.fixInterpolations(f) # Fix contours where auto-interpolation is possible.
            changed |= self.componentFixAll(f) # Fix components
            changed |= self.checkFixAllAnchors(f) # Fix anchors in all glyphs
            #hanged |= self.reportSpacing(f, doFix=True)
            # Fix groups
            # Fix kerning
            # Fix guidelines
            # Fix name tables
            # Fix vertical metrics
            if changed:
                f.changed()
                f.save()
        
        print('Done')

    def saveAllCallback(self, sender):
        for f in self.getAllOpenFonts():
            print(f'... Save {f.path}')
            f.save()

    def checkFixGlyphSetCallback(self, sender):
        """Check/fix the glyphset according to the defined MasterData.glyphSet records."""
        c = self.getController()
        if c.w.fixGlyphSetSafety.get(): # Safe checkbox should be set for safety
            f = self.getCurrentFont()
            self.checkFixGlyphSet(f)
        else:
            print(f'### Check [x] Fix glyphset to enable this button.')

    def checkFixGlyphSet(self, f):
        """Check/fix the glyphset according to the defined MasterData.glyphSet records."""
        changed = False
        c = self.getController()
        md = self.getMasterData(f)
        # Find missing glyphs
        for gName, gd in sorted(md.glyphSet.items()):
            if not gName in f:
                if c.w.fixGlyphSetSafety.get():
                    print(f'... checkFixGlyphSet: Create missing glyph /{gName}')
                    f.newGlyph(gName)
                    changed = True
                else:
                    print(f'### checkFixGlyphSet: Missing glyph /{gName}')
            if gd.uni and f[gName].unicode != gd.uni:
                print(f'... checkFixGlyphSet: Set /{gName}.unicode {hex(gd.uni or 0)} --> {hex(f[gName].unicode or 0)}')
                f[gName].unicode = gd.uni

        # Find obsolete glyphs to delete
        for gName in sorted(f.keys()):
            if gName not in md.glyphSet.keys():
                if c.w.fixGlyphSetSafety.get():
                    print(f'... checkFixGlyphSet: Delete obsolete glyph /{gName}')
                    del f[gName]
                    changed = True
                else:
                    print(f'### checkFixGlyphSet: Obsolete glyph /{gName}')
        return changed

    def updateEditor(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            g.changed()
                  
    # Handle subscriptions to the EditorWindow events
    
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        # Allow parts to close their own stuff (e.g. closing subwindows) before the main assistant window closes
        for methodName in self.CLOSING_WINDOW_METHODS:
            getattr(self, methodName)()
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None

    def getController(self):
        """Answer the controller. We need this method to be compatible in case of controller.getController()"""
        return self


