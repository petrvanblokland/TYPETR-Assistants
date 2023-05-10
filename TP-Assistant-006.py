# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
#     Version 004
# ..............................................................................
#
#     TYPETR Assistant
#
#     A fast and flexible collection of helpers for type projects.
#
import importlib

import drawBot

# https://typesupply.github.io/merz/objects/path.html#path-properties-path
from merz import MerzView, MerzPen
from mojo.UI import OpenGlyphWindow
from mojo.events import postEvent

import assistantLib
from assistantLib import baseAssistant
from assistantLib import helpers # Includes ufo name helpers, getFont() and global openFonts dictionary.
from assistantLib import tp_previewOverlay
from assistantLib import tp_glyphBrowser
from assistantLib.tp_glyphBrowser import GlyphBrowser
from assistantLib.tp_glyphBrowser import GlyphBrowserController
from assistantLib import tp_previewDesignspace
from assistantLib.tp_previewDesignspace import PreviewDesignspace
from assistantLib.tp_previewDesignspace import PreviewDesignspaceController

importlib.reload(assistantLib)
importlib.reload(assistantLib.baseAssistant)
importlib.reload(assistantLib.helpers)
importlib.reload(assistantLib.tp_previewDesignspace)
importlib.reload(assistantLib.tp_previewOverlay)
importlib.reload(assistantLib.tp_glyphBrowser)

from assistantLib.baseAssistant import EVENT_DO_OPEN_EDITWINDOW
from assistantLib.tp_previewDesignspace import PreviewDesignspace, PreviewDesignspaceController
from assistantLib.tp_previewOverlay import PreviewOverlay, PreviewOverlayController
from assistantLib.tp_glyphBrowser import GlyphBrowser, GlyphBrowserController

from assistantLib.helpers import *

class SegoePreviewDesignspaceController(PreviewDesignspaceController):

    VERBOSE = False
    UFO_PATH = '_ufo/'
    VF_PATH = '_vf/SegoeUI_wght5-opsz3-vf-213.ttf'
    VF_REF_PATH = '_vf/SegoeUI-VF.ttf'
    
    MASTER_LOCATIONS = {
        # (opsz, wght): ufoName
        (36, 900): 'Segoe_UI_Display-Black_MA420.ufo',        (36, 700): 'Segoe_UI_Display-Bold_MA323.ufo',        (36, 400): 'Segoe_UI_Display-Regular_MA168.ufo',        (36, 300): 'Segoe_UI_Display-Light_MA98.ufo',        (36, 100): 'Segoe_UI_Display-Hairline_MA32.ufo',        (10.5, 900): 'Segoe_UI_Text-Black_MA420.ufo',        (10.5, 700): 'Segoe_UI_Text-Bold_MA323.ufo',        (10.5, 400): 'Segoe_UI_Text-Regular_MA168.ufo',        (10.5, 300): 'Segoe_UI_Text-Light_MA98.ufo',
        (10.5, 100): 'Segoe_UI_Text-Hairline_MA62.ufo',        (5, 900): 'Segoe_UI_Small-Black_MA410.ufo',        (5, 700): 'Segoe_UI_Small-Bold_MA300.ufo',        (5, 400): 'Segoe_UI_Small-Regular_MA200.ufo',        (5, 300): 'Segoe_UI_Small-Light_MA160.ufo',        (5, 100): 'Segoe_UI_Small-Hairline_MA97.ufo',    }
    W = 600 # Width of designspace canvas window
    H = 800
    M = ML = MR = MT = 16 # Margin and gutter
    
    # Determine the dimensions of the grid
    WGHTS = set() # All unique weights in the design space
    OPSZS = set() # All unique optical sizes in the design space
    CELLS = {} # Store X-ref of location --> ufoName
    for (opsz, wght), ufoName in MASTER_LOCATIONS.items():
        WGHTS.add(wght)
        OPSZS.add(opsz)
        CELLS[(opsz, wght)] = ufoName
    WGHTS = sorted(WGHTS)
    OPSZS = sorted(OPSZS)
    ROWS = len(WGHTS)
    COLS = len(OPSZS)
    
    CW = (W - 2 * M)/COLS
    CH = (H - 2 * M)/ROWS
    
    GLYPH_COLOR = (0, 0, 0, 1)
    REF_COLOR = (1, 0, 0, 1)

    FONTSIZE = CH * 0.9
    MB = 0
    
    #    E V E N T
    
    def mouseDown(self, view, event):
        x = event.locationInWindow().x
        y = event.locationInWindow().y
        # Try to locate the cell of this mouse click.
        xIndex = max(0, min(len(self.OPSZS), round((x - self.M - self.CW/2) / self.CW)))
        yIndex = max(0, min(len(self.WGHTS), round((-y + self.H + self.M  - self.MB) / self.CH - 1)))
        opsz = self.OPSZS[xIndex]
        wght = self.WGHTS[yIndex]
        # Now open the EditorWindow for this font on this glyph
        ufoName = self.MASTER_LOCATIONS[(opsz, wght)]
        info = dict(x=x, y=y, xIndex=xIndex, yIndex=yIndex, location=(opsz, wght), ufoName=ufoName)

        if self. VERBOSE:
            print('--- SegoePreviewDesignspaceController.mouseDown', xIndex, yIndex, opsz, wght, ufoName)
        postEvent(EVENT_DO_OPEN_EDITWINDOW, info=info)

    #    U P D A T E
    
    def updateCellLayer(self, gName, location, layers, fontPath):
        #print('... updateCellLayer', location)
        opsz, wght = location
        
        pen = MerzPen()         
        p = drawBot.BezierPath()
        fs = drawBot.FormattedString('', font=fontPath, fontSize=self.FONTSIZE, fill=0, align='center', fontVariations=dict(opsz=opsz, wght=wght))
        fs.appendGlyph(gName)
        p.text(fs)
        p.drawToPen(pen)
        if location in layers:
            layers[location].setPath(pen.path)

    def updateCellUfoLayer(self, gName, location, layers):
        #print('... updateCellLayer', location)
        opsz, wght = location        

        ufoName = self.MASTER_LOCATIONS[location]
        f = getFont(self.UFO_PATH + ufoName)

        # Get index of these location values in the axes range.        
        xIndex = self.OPSZS.index(opsz)
        yIndex = self.WGHTS.index(wght)
        
        g = f[gName]

        scale = self.FONTSIZE/f.info.unitsPerEm
        
        # Calculate the (x, y) position of the cell for this location
        x = self.M + xIndex * self.CW + self.CW/2 - g.width/2*scale # Centered
        y = self.H + self.M - (yIndex+1) * self.CH - self.MB

        path=f[gName].getRepresentation('merz.CGPath')
        layers[location].setPath(path)   
        layers[location].setPosition((x/scale, y/scale))     
        
    def updateCell(self, gName, location):
        """There are some options to build the cell. Either use self.VF_REF_PATH and self.VF_PATH to draw
        via drawBot.FormattedString or use ufoName to use the current UFO glyph directly to generate the path."""        
        self.updateCellLayer(gName, location, self.refLayers, self.VF_REF_PATH)
        #self.updateCellLayer(gName, location, self.glyphLayers, self.VF_PATH)
        self.updateCellUfoLayer(gName, location, self.glyphLayers)
                         
    def glyphEditorDidSetGlyph(self, info):
        """There is a new glyph set. Respond to this even by replacing all cell paths by the new glyph."""
        if self.VERBOSE:
            print('--- SegoePreviewDesignspaceController.glyphEditorDidSetGlyph /%s' % info['glyph'].name)
        g = info['glyph']
        if g is not None:
            for location, ufoName in self.MASTER_LOCATIONS.items():
                self.updateCell(g.name, location)
    
    #    B U I L D
    
    def buildCellLayer(self, gName, location, layers, fontPath, color):
        """Build the cell layer for this location."""
        opsz, wght = location        

        # Get index of these location values in the axes range.        
        xIndex = self.OPSZS.index(opsz)
        yIndex = self.WGHTS.index(wght)
        
        # Calculate the (x, y) position of the cell for this location
        x = self.M + xIndex * self.CW + self.CW/2
        y = self.H + self.M - (yIndex+1) * self.CH - self.MB
        
        # Create the Merz layer, append it to the container and store it in the layers dictionary
        container = self.w.view.getMerzContainer()
        layers[location] = layer = container.appendPathSublayer(
            position=(x, y),
            size=(self.CW, self.CH),
            fillColor=None,
            strokeColor=color, # Used the outline color for the type of layer.
            strokeWidth=0.5,
        )
        # Create a MerzPen to write the FormattedString into, that contains the glyph shape instance from the VF
        pen = MerzPen()
        p = drawBot.BezierPath()
        fs = drawBot.FormattedString('', font=fontPath, fontSize=self.FONTSIZE, fill=0, align='center', fontVariations=dict(opsz=opsz, wght=wght))
        fs.appendGlyph(gName)
        p.text(fs)
        p.drawToPen(pen)
        layer.setPath(pen.path) # Set the layer path to this new MerzPen result.

    def buildCellUfoLayer(self, gName, location, layers, color):
        """Build the cell layer for this location, using the UFO font --> glyph path."""
        opsz, wght = location        

        ufoName = self.MASTER_LOCATIONS[location]
        f = getFont(self.UFO_PATH + ufoName)

        # Get index of these location values in the axes range.        
        xIndex = self.OPSZS.index(opsz)
        yIndex = self.WGHTS.index(wght)
        
        g = f[gName]

        scale = self.FONTSIZE/f.info.unitsPerEm
        
        # Calculate the (x, y) position of the cell for this location
        x = self.M + xIndex * self.CW + self.CW/2 - g.width/2*scale # Centered
        y = self.H + self.M - (yIndex+1) * self.CH - self.MB

        # Create the Merz layer, append it to the container and store it in the layers dictionary
        container = self.w.view.getMerzContainer()
        layers[location] = layer = container.appendPathSublayer(
            position=(x/scale, y/scale),
            path=g.getRepresentation('merz.CGPath'),
            size=(self.CW, self.CH),
            fillColor=None,
            strokeColor=color, # Used the outline color for the type of layer.
            strokeWidth=0.5,
        )
        layer.addScaleTransformation(scale, 'glyphScale')
        
    def buildCell(self, gName, location):
        """There are some options to build the cell. Either use self.VF_REF_PATH and self.VF_PATH to draw
        via drawBot.FormattedString or use ufoName to use the current UFO glyph directly to generate the path."""        
        self.buildCellLayer(gName, location, self.refLayers, self.VF_REF_PATH, self.REF_COLOR)
        #self.buildCellLayer(gName, location, self.glyphLayers, self.VF_PATH, self.GLYPH_COLOR)
        self.buildCellUfoLayer(gName, location, self.glyphLayers, self.GLYPH_COLOR)

    def buildUI(self):
        self.lastMouseGrid = None # Save the last mouse grid click
        self.lastMouse = None # Actual position of last mouse click
        self.lastMouseDrag = None # Actual position of last mouse drag
        self.selectedDragPoints = None # Storage of selected points, while dragging

        self.w.view = MerzView((0, 0, 0, 0),
            backgroundColor=(1, 1, 1, 1),
            delegate=self
        )
        self.glyphLayers = {} # Storage of Merzlayers for master glyph paths
        self.refLayers = {} # Storage of Merz layers for reference VF instance pathts

        g = CurrentGlyph()
        if g is not None:
            for location in self.MASTER_LOCATIONS.keys():
                self.buildCell(g.name, location)
                    
if __name__ == '__main__':
    #OpenWindow(PreviewOverlayController)
    #OpenWindow(GlyphBrowserController)
    OpenWindow(SegoePreviewDesignspaceController)
    
    
  
  