# -*- coding: UTF-8 -*-
#
#    TYPETR-Polator
#
#    A faster and more flexible version of Prepolator functionality
#

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

from mojo.events import extractNSEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

from fontTools.misc.transform import Transform

from typelib.toolset import interpolateGlyph, copyLayer, scaleGlyph

import scriptsLib

importlib.reload(scriptsLib)

W, H = 500, 450
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/2
CW2 = (CW-M)/2
C0 = M
C1 = C0 + CW + M
VT = 120 # Vertical tab from bottom

WindowClass = vanilla.Window
#WindowClass = vanilla.FloatingWindow

def getUfoName(f):
    """Answer the file name of this font. Answer None if there is no path."""
    if f.path is not None: # Untitled fonts don't have a path
        return f.path.split('/')[-1] # Answet the ufo file name
    return None

def getUfoDirPath(f):
    """Answer the directory path that this UFO is in."""
    if f.path is not None:
        return '/'.join(f.path.split('/')[:-1]) + '/'
    return None
    
def getCurrentDirectory(f):
    """Answer the path of this font."""
    if f.path is None:
        return None
    return '/'.join(f.path.split('/')[:-1]) + '/'

openFonts = {} # Keep track of the open fonts (even when they are open in the background)
    
def getMaster(path, showInterface=False):
    """If there is an open font with @path, then answer it.
    """
    global openFonts
    # Check if the master is already open, by RoboFont. Then answer it.
    for f in AllFonts():
        if f.path == path:
            #print('... Selecting open font', path)
            return f
    # If the font is open without interface, then it must be in the global openFonts dictionary. 
    # This avoids the opening of hidden fonts more than once.   
    if path in openFonts and not showInterface:
        return openFonts[path]
        
    # Not open yet, open it in the background and cache the master    
    print('... Opening hidden font', path)
    # In case "showUI" error here, then start venv, because using the old FontParts
    f = OpenFont(path, showInterface=showInterface) # Open in RoboFont
    if f is None:
        print('### Cannot open font', path)
        return None
    openFonts[path] = f # Store with full path name as key
    return f

assistant = None # Little cheat, to make the assistant available from the window

class Typolator(Subscriber):

    controller = None

    def build(self):
        global curvePaletteController
        curvePaletteController = self

        glyphEditor = self.getGlyphEditor()

    def started(self):
        pass
            
    def destroy(self):
        pass

    def glyphEditorDidSetGlyph(self, info):
        # Pass this on to the window controller. How to do this better?
        self.controller.glyphEditorDidSetGlyph(info)

    def glyphEditorDidMouseUp(self, info):
        # Pass this on to the window controller. How to do this better?
        self.controller.glyphEditorDidMouseUp(info)

    def glyphEditorDidMouseDrag(self, info):
        # Pass this on to the window controller. How to do this better?
        self.controller.glyphEditorDidMouseDrag(info)

    def glyphEditorGlyphDidChangeSelection(self, info):
        # Pass this on to the window controller. How to do this better?
        self.controller.glyphEditorGlyphDidChangeSelection(info)

    def fontDocumentDidOpen(self, info):
        self.controller.updateRefPopup()
        self.controller.updateUfoListCallback()
        
    def fontDocumentDidClose(self, info):
        self.controller.updateRefPopup()
        self.controller.updateUfoListCallback()
        
class TypolatorController(WindowController):

    subscriberClass = Typolator

    debug = True

    def build(self):
            
        y = M
        self.w = WindowClass((W, H), 'Typolator', minSize=(W, H))

        self.w.filterPatternLabelStart = vanilla.TextBox((M, y, CW/3, 24), 'Starts')
        self.w.filterPatternLabelHas = vanilla.TextBox((M+CW/3, y, CW/3, 24), 'Has')
        self.w.filterPatternLabelEnd = vanilla.TextBox((M+2*CW/3, y, CW/3, 24), 'Ends')
        self.w.referenceUfo = vanilla.TextBox((C1, y, CW, 24), 'Reference UFO')
        #self.w.filterItalicUfo = vanilla.HorizontalRadioGroup((C2, y, CW, 24), ('Roman', 'Italic'), callback=self.updateUfoListCallback)
        #self.w.filterItalicUfo.set(0)
        y += L
        self.w.filterPatternStart = vanilla.EditText((M, y, CW/3, 24), continuous=True, callback=self.filterNamesCallback)
        self.w.filterPatternHas = vanilla.EditText((M+CW/3, y, CW/3, 24), continuous=True, callback=self.filterNamesCallback)
        self.w.filterPatternEnd = vanilla.EditText((M+2*CW/3, y, CW/3, 24), continuous=True, callback=self.filterNamesCallback)

        # List of currently open fonts, that can be used as reference.
        self.w.referenceSelection = vanilla.PopUpButton((C1, y, CW, 24), [], callback=self.updateUfoListCallback)
        
        y += L*1.2
        self.w.glyphNames = vanilla.List((M, y, CW, -VT), items=[], doubleClickCallback=self.dblClickGlyphNamesCallback)
        self.w.ufoNames = vanilla.List((M+M+CW, y, CW, -VT), items=[], doubleClickCallback=self.dblClickUfoNamesCallback)
        y = -VT
        self.w.selectOpenDblClick = vanilla.RadioGroup((C1, y, CW, L), ('Open GlyphEditor', 'Open FontWindow'), isVertical=False, sizeStyle='small')
        self.w.selectOpenDblClick.set(0)
        y += L
        #self.w.checkInterpolation = vanilla.Button((C1, y, CW, 32), 'Check/Fix', callback=self.checkInterpolationCallback)
        #y += L*1.1
        self.w.saveAll = vanilla.Button((C1, y, CW2, 32), 'Save all', callback=self.saveAllCallback)
        self.w.saveCloseAll = vanilla.Button((C1 + CW2 + M, y, CW2, 32), 'Save/Close all', callback=self.saveCloseAllCallback)
    
        self.glyphgNames = []
        self.updateRefPopup() 
        self.updateUfoListCallback()
        self.w.open()

    def acceptsFirstResponder(self, sender):
        # necessary for accepting mouse events
        return True

    def acceptsMouseDrag(self, sender):
        # necessary for tracking mouse movement
        return True

    def acceptsMouseDown(self, sender):
        # necessary for tracking mouse down
        return True

    def started(self):
        #print("started")
        self.subscriberClass.controller = self
        registerGlyphEditorSubscriber(self.subscriberClass)

    def destroy(self):
        #print("windowClose")
        #container = self.w.view.getMerzContainer()
        #container.clearSublayers()
        #unregisterGlyphEditorSubscriber(self.subscriberClass)
        #self.subscriberClass.controller = None
        pass

    def glyphEditorDidSetGlyph(self, info):
        # Pass this on to the window controller. How to do this better?
        pass
        
    def glyphEditorDidMouseUp(self, info):
        # Pass this on to the window controller. How to do this better?
        pass

    def glyphEditorDidMouseDrag(self, info):
        # Pass this on to the window controller. How to do this better?
        pass

    def glyphEditorGlyphDidChangeSelection(self, info):
        # Pass this on to the window controller. How to do this better?
        pass

    def filterNamesCallback(self, sender=None):
        filteredGlyphNames = []
        filterPatternStart = self.w.filterPatternStart.get().strip()
        filterPatternHas = self.w.filterPatternHas.get().strip()
        filterPatternEnd = self.w.filterPatternEnd.get().strip()
        # Search for component patterns
        componentPatternStart = componentPatternHas = componentPatternEnd = None
        if '@' in filterPatternStart:
            componentPatternStart = filterPatternStart.split('@')[1]
            filterPatternStart = filterPatternStart.split('@')[0]
        if '@' in filterPatternHas:
            filterPatternHas = filterPatternHas.split('@')[1]
            filterPatternHas = filterPatternHas.split('@')[0] # In there is a combined pattern A@
        if '@' in filterPatternEnd:
            componentPatternEnd = filterPatternEnd.split('@')[1]
            filterPatternEnd = filterPatternEnd.split('@')[0]

        f = CurrentFont()
        for glyphName in sorted(self.glyphNames):
            selected = None
            if ((not filterPatternStart or glyphName.startswith(filterPatternStart)) and
                (not filterPatternHas or filterPatternHas in glyphName) and
                (not filterPatternEnd or glyphName.endswith(filterPatternEnd))):
                selected = glyphName
            # Test on component filter too
            if f is not None and selected is not None and selected in f and (
                componentPatternStart is not None or componentPatternHas is not None or componentPatternEnd):
                selectedByComponent = None
                for component in f[selected].components:
                    if componentPatternStart is not None and component.baseGlyph.startswith(componentPatternStart):
                        selectedByComponent = selected
                        break
                    if componentPatternHas is not None and componentPatternHas in component.baseGlyph:
                        selectedByComponent = selected
                        break
                    if componentPatternEnd is not None and component.baseGlyph.endswith(componentPatternEnd):
                        selectedByComponent = selected
                        break
                selected = selectedByComponent # Not this one.
            if selected is not None:
                filteredGlyphNames.append(selected)
                

        self.w.glyphNames.set(sorted(filteredGlyphNames))

    def dblClickUfoNamesCallback(self, sender):
        ref = self.getReferenceFont()
        if ref is None:
            return
        dirPath = getUfoDirPath(ref)

        ufoSelected = sender.getSelection()
        for ufoIndex in ufoSelected:

            ufoPath = dirPath + sender[ufoIndex]
            getMaster(ufoPath, showInterface=True)
                
    def dblClickGlyphNamesCallback(self, sender):
        """Double click on one of the glyphs. Open the glyph editor on the selectyed UFO and otherwise
        on the current font"""
        selected = sender.getSelection()
        for index in selected:
            glyphName = sender[index]
            ufoSelection = self.w.ufoNames.getSelection()
            f = None
            if ufoSelection:
                ref = self.getReferenceFont()
                if ref is not None:
                    dirPath = getUfoDirPath(ref) # Get the directory of the reference.
                    f = getMaster(dirPath + self.w.ufoNames[ufoSelection[0]])
            else:
                f = CurrentFont()
            if f is not None:
                g = f[glyphName]
                if self.w.selectOpenDblClick.get() == 0:
                    OpenGlyphWindow(g) # Open the editor window on the selected glyph name.
                else:
                    for fontWindow in AllFontWindows():
                        if fontWindow._font == f.naked():
                            fontWindow.window().show()
                    
    def updateRefPopup(self):
        refNames = []
        for f in AllFonts(): # Use open fonts as seed to find the folders. 
            refNames.append(getUfoName(f))
        self.w.referenceSelection.setItems(refNames)
              
    def updateUfoListCallback(self, sender=None):
        """Update the list of UFOs that are in the same folder as the fonts that are currently open.
        Open them in the background if not already open."""
        self.glyphNames = set()
        ufoNames = []

        ref = self.getReferenceFont()
        if ref is None:
            return

        dirPath = getUfoDirPath(ref)
        refName = getUfoName(ref)
        
        for fileName in os.listdir(dirPath):
            if not fileName.endswith('.ufo'):
                continue
            ufoPath = dirPath + fileName
            select = bool('Italic' in refName) == bool('Italic' in fileName)
            if select:
                ufoNames.append(fileName)
                ufo = getMaster(ufoPath, False)
                self.glyphNames = self.glyphNames.union(set(ufo.keys()))
                    
        self.w.ufoNames.set(sorted(ufoNames))
        self.filterNamesCallback()

    def checkInterpolationCompatibility(self, g, gRef, errors):
        foudError = False
        
        if len(g.anchors) != len(gRef.anchors):
            errors.append('### Anchors (%d) in /%s not equal to reference (%d)' % (len(g.anchors), g.name, len(gRef.anchors)))
            foudError = True
        
        if len(g.components) != len(gRef.components):
            errors.append('### Components (%d) in /%s not equal to reference (%d)' % (len(g.components), g.name, len(gRef.components)))
            foudError = True
        
        if len(g.contours) != len(gRef.contours):
            errors.append('### Components (%d) in /%s not equal to reference (%d)' % (len(g.contours), g.name, len(gRef.contours)))
            foudError = True
        else:
            for cIndex, contour in enumerate(g.contours):
                contourRef = gRef.contours[cIndex]
                if len(contour.points) != len(contourRef.points):
                    errors.append('### Contour[%s].points (%d) in /%s not equal to reference (%d)' % (cIndex, len(contour.points), g.name, len(contourRef.points)))
                    foudError = True
        return foudError
    
    def getReferenceFont(self):
        ref = None
        refName = self.w.referenceSelection.getItem()
        if refName is None:
            return None
        # Find the reference font
        for f in AllFonts():
            if getUfoName(f) == refName:
                return f
        return None
            
    def checkInterpolationCallback(self, sender):
        ref = self.getReferenceFont()
        if ref is None:
            return
        dirPath = getUfoDirPath(ref)
                
        # Collect selected names from the UFO name list
        selectedUfoNames = []
        for row in self.w.ufoNames.getSelection():
            selectedUfoNames.append(self.w.ufoNames[row])
        if not selectedUfoNames: # Nothing selected, then use the whole list.
            selectedUfoNames = self.w.ufoNames.get()

        done = False
        totalErrors = 0
        for ufoName in selectedUfoNames:
            errors = []
            f = getMaster(dirPath + ufoName)
            # Now we have a reference, compare the list of filtered glyph names.
            print('... Checking interpolation of %s' % ufoName)
            for glyphName in self.w.glyphNames: # Just test for the filtered set
                if glyphName not in ref:
                    print('### Missing glyph /%s in reference %s' % (glyphName, getUfoName(f)))
                    continue                    
                gRef = ref[glyphName]
                if glyphName not in f:
                    print('### Missing glyph /%s in %s' % (glyphName, getUfoName(f)))
                else:
                    g = f[glyphName]
                    foundError = self.checkInterpolationCompatibility(g, gRef, errors)
                    if self.w.selectOpenDblClick.get() == 0 and foundError:
                        OpenGlyphWindow(g)
                        done = True
                if done:
                    break
            if errors:
                print('\n'.join(errors))  
                totalErrors += len(errors)               
            if done:
                break  
        print('Done checking interpolation (Total errors: %d)' % totalErrors)
                                                  
    def saveCloseAllCallback(self, sender):
        # Save and close all open fonts
        for f in AllFonts():
            f.save()
            f.close()
         
    def saveAllCallback(self, sender):
        # Save and close all open fonts
        for f in AllFonts():
            f.save()
         
    def update(self, sender):
        pass
        
if __name__ == '__main__':
    OpenWindow(TypolatorController)

  