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

from typelib.toolset import interpolateGlyph, openFont, copyLayer, scaleGlyph

import scriptsLib

importlib.reload(scriptsLib)

W, H = 600, 600
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C2 = C1 + CW + M
VT = 150 # Vertical tab from bottom

WindowClass = vanilla.Window
#WindowClass = vanilla.FloatingWindow

openFonts = {} # Keep track of the open fonts (even when they are open in the background)

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
    
def getMaster(path, showInterface):
    global openFonts
    # Check if the master is already open, by RoboFont or by self
    for f in AllFonts():
        if f.path.endswith(path):
            #print('... Selecting open font', path)
            return f

    root = getCurrentDirectory(CurrentFont())
    rootPath = root + path
    
    if rootPath in openFonts:
        return openFonts[rootPath]
    # Not open yet, open it in the background and cache the master
    
    print('... Opening hidden font', root+path)
    # In case "showUI" error here, then start venv
    f = OpenFont(rootPath, showInterface=showInterface)
    if f is None:
        print('### Cannot open font', rootPath)
        return None
    openFonts[rootPath] = f
    return f

assistant = None # Little cheat, to make the assistant available from the window

class BaseTypolator:
    
    def __init__(self):
        
        y = M
        self.w = WindowClass((W, H), self.__class__.__name__, minSize=(W, H))

        self.w.filterPatternLabel1 = vanilla.TextBox((M, y, CW/2, 24), 'Filter 1')
        self.w.filterPatternLabel2 = vanilla.TextBox((M+CW/2, y, CW/2, 24), 'Filter 2')
        self.w.referenceUfo = vanilla.TextBox((C1, y, CW, 24), 'Reference UFO')
        #self.w.filterItalicUfo = vanilla.HorizontalRadioGroup((C2, y, CW, 24), ('Roman', 'Italic'), callback=self.updateUfoListCallback)
        #self.w.filterItalicUfo.set(0)
        y += L
        self.w.filterPattern1 = vanilla.EditText((M, y, CW/2, 24), callback=self.filterNamesCallback)
        self.w.filterPattern2 = vanilla.EditText((M+CW/2, y, CW/2, 24), callback=self.filterNamesCallback)

        refNames = []
        for f in AllFonts(): # Use open fonts as seed to find the folders. 
            refNames.append(getUfoName(f))
        self.w.referenceSelection = vanilla.PopUpButton((C1, y, CW*2, 24), items=sorted(refNames), callback=self.updateUfoListCallback)
        
        y += L*1.2
        self.w.glyphNames = vanilla.List((M, y, CW, -VT), items=[])
        self.w.ufoNames = vanilla.List((M+M+CW, y, CW+M+CW, -VT), items=[])
        y = -VT
        self.w.openGlyphWindow = vanilla.CheckBox((C2, y, CW, 24), 'Open GlyphEditor', value=True, sizeStyle='small')
        y += L
        self.w.updateUfoList = vanilla.Button((C1, y, CW, 32), 'Update UFO list', callback=self.updateUfoListCallback)
        self.w.checkInterpolation = vanilla.Button((C2, y, CW, 32), 'Check/Fix', callback=self.checkInterpolationCallback)
        y += L*1.2
        self.w.saveCloseAll = vanilla.Button((C1, y, CW, 32), 'Save/Close all', callback=self.saveCloseAllCallback)
    
        self.glyphgNames = []
        self.updateUfoListCallback()
        self.w.open()

    def filterNamesCallback(self, sender=None):
        glyphNames = []
        filterPattern1 = self.w.filterPattern1.get()
        filterPattern2 = self.w.filterPattern2.get()
        for glyphName in sorted(self.glyphNames):
            if filterPattern1 and filterPattern1[0] == '=' and filterPattern1[1:] == glyphName:
                glyphNames.append(glyphName)                
            elif (not filterPattern1 or filterPattern1 in glyphName) and (not filterPattern2 or filterPattern2 in glyphName):
                glyphNames.append(glyphName)
        self.w.glyphNames.set(glyphNames)
        
    def updateUfoListCallback(self, sender=None):
        """Update the list of UFOs that are in the same folder as the fonts that are currently open.
        Open them in the background if not already open."""
        self.glyphNames = set()
        ufoNames = []

        refName = self.w.referenceSelection.getItem()
        if refName is None:
            return
        ref = openFont(refName)
        
        if not ref.path in openFonts: # This may be a newly opened font. Check to be sure, add to openFonts otherwise
            openFonts[ref.path] = ref
        dirPath = getUfoDirPath(ref)
        for fileName in os.listdir(dirPath):
            if not fileName.endswith('.ufo'):
                continue
            ufoPath = dirPath + fileName
            select = bool('Italic' in refName) == bool('Italic' in fileName)
            if select:
                ufoNames.append(fileName)
                ufo = OpenFont(ufoPath, False)
                if ufoPath not in openFonts:
                    openFonts[ufoPath] = ufo
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
        
    def checkInterpolationCallback(self, sender):
        ref = None
        refName = self.w.referenceSelection.getItem()
        if refName is None:
            return
        ref = openFont(refName)
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
            f = openFont(dirPath + ufoName)
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
                    if self.w.openGlyphWindow.get() and foundError:
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
         
    def update(self, sender):
        pass
        
if __name__ == '__main__':
    BaseTypolator()

  