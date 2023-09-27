# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
# Generic system imports
import os, sys

from math import sqrt

# @@@@ REMOVE LATER
from AppKit import (
        NSBezierPath, NSColor, NSFontAttributeName, NSFont,
        NSForegroundColorAttributeName, NSAttributedString, NSMakeRect, 
        NSGraphicsContext)

# Import of resources available in RoboFont
from vanilla import (Window, FloatingWindow, TextBox, HorizontalRadioGroup, EditText, 
    PopUpButton, List, CheckBox, RadioGroup, Button)
import merz
from mojo.subscriber import Subscriber, WindowController, registerRoboFontSubscriber
from mojo.roboFont import AllFonts, OpenFont, CurrentFont
from mojo.UI import OpenGlyphWindow
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

from tnbits.analyzers.analyzermanager import analyzerManager

# Add the local assistantLib library to the RoboFont sys paths if it does not already exist.
# This ways we can just start this script without the need to install it into RoboFont.
# Maybe not entirely user friendly (the script is running from the source, instead of making
# it available from a menu), but the iterative concept of helpers and assistants make them
# closer to be viewed as source.
# The PATH can also be used to access other resources in this repository.
PATH = '/'.join(__file__.split('/')[:-1]) + '/' # Get the directory path that this script is in.
if not PATH in sys.path: # Is it not already defined in RoboFont
    sys.path.append(PATH) # Then add it.
import assistantLib # Now we can import local helper/assistant stuff 

# Define the GlyphBrowser class, inheriting from Subsriber (which responds to RoboFont events)
# and WindowController (which knows how to deal with the user interface).
# In principle these could be two separate classes (GlyphBrowserSubscriber and GlyphBrowserController)
# but in simple helper applications like this it’s also good to combine the functions.

MAX_BARS = MAX_STEMS = 40
LABEL_SIZE = 14
LINE_MARKER_SIZE = 8
NUM_LAYER_ELEMENTS = 50 # Max number of layer elements
TEXT_SIZE = 12

YLINE = 16
# Fitting 3 digits of y-coordinate.
XLINE = 22

STEM_COLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.2, 0.2, 0.2, 0.8)
COUNTER_COLOR = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.7, 0.2, 0.2, 0.8)

class Dimensioneer(Subscriber):
    """The SimpleAssistant is a demo class to show how events work between inside the 
        Assistant as well as from the EditorWindow. 
    """
    controller = None

    scale = 1
    
    def build(self):
        self._dValues = None # Caching diagonal values from glyph analyzer.

        glyphEditor = self.getGlyphEditor()

        # Add Merz drawing layers
        self.foregroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )
        #https://typesupply.github.io/merz/objects/textBox.html#merz.objects.text.TextBox.setHorizontalAlignment
        
        #self.backgroundContainer.appendTextLineSublayer
        #self.backgroundContainer.appendRectangleSublayer
        #self.backgroundContainer.appendPathSublayer
        #self.backgroundContainer.appendLineSublayer
        self.diagonalLayers = []
        self.diagonalLayerLabels = []
        
        self.horizontalGridLayers = []
        self.horizontalLayers = []
        self.horizontalLabelLayers = []
        
        self.verticalGridLayers = []
        self.verticalLayers = []
        self.verticalLabelLayers = []
        
        lineColor = (0, 0, 0.8, 0.7)
        textColor = (0, 0, 0, 1)
        pointSymbol = dict(name='oval', size=(12, 12), fillColor=None, strokeColor=lineColor, strokeWidth=0.7)
        arrowSymbol = dict(name='oval', size=(8, 8), fillColor=None, strokeColor=lineColor, strokeWidth=0.7)
        
        for n in range(NUM_LAYER_ELEMENTS):
            
            # Diagonal measures
            
            self.diagonalLayers.append(self.backgroundContainer.appendLineSublayer(name='Diagonal%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=lineColor,
                strokeWidth=0.5,
                startSymbol=pointSymbol,
                endSymbol=pointSymbol,
            ))
            self.diagonalLayerLabels.append(self.backgroundContainer.appendTextLineSublayer(name='DiagonalLabel%d' % n,
                position=(FAR, 0),
                text='',
                horizontalAlignment='center',
                verticalAlignment="center",
                font='Courier Bold',
                pointSize=LABEL_SIZE,
                fillColor=textColor,
                applyTransformation=False,
            ))
            
            # Vertical measures
            
            # Horizontal grid lines
            self.verticalGridLayers.append(self.backgroundContainer.appendLineSublayer(name='VerticalGrid%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=lineColor,
                strokeWidth=0.5,
            ))
            self.verticalLayers.append(self.backgroundContainer.appendLineSublayer(name='Vertical%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=lineColor,
                strokeWidth=0.5,
                startSymbol=arrowSymbol,
                endSymbol=arrowSymbol,
            ))
            self.verticalLabelLayers.append(self.backgroundContainer.appendTextLineSublayer(name='VerticalLabel%d' % n,
                position=(FAR, 0),
                text='',
                horizontalAlignment='center',
                verticalAlignment="center",
                font='Courier-Bold',
                pointSize=LABEL_SIZE,
                fillColor=textColor,
                applyTransformation=False,
            ))
                 
            # Horizontal measures
            
            # Vertical grid lines
            self.horizontalGridLayers.append(self.backgroundContainer.appendLineSublayer(name='HorizontalGrid%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=lineColor,
                strokeWidth=0.5,
            ))
            self.horizontalLayers.append(self.backgroundContainer.appendLineSublayer(name='Horizontal%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=lineColor,
                strokeWidth=0.5,
                startSymbol=arrowSymbol,
                endSymbol=arrowSymbol,
            ))
            self.horizontalLabelLayers.append(self.backgroundContainer.appendTextLineSublayer(name='HorizontalLabel%d' % n,
                position=(FAR, 0),
                text='',
                horizontalAlignment='center',
                verticalAlignment="center",
                font='Courier-Bold',
                pointSize=LABEL_SIZE,
                fillColor=textColor,
                applyTransformation=False,
            ))


    def started(self):
        pass

    def destroy(self):
        pass
                
    #   C A L L B A C K S
                    
    def update(self):
        self.updateDiagonals()
        self.updateBarLines()
        self.updateStemLines()
                     
    #   B A R  L I N E S

    def _overlapsY(self, y, d, usedBars):
        for uy, ud in usedBars:
            if y < uy + ud and y + d > uy: 
                return True
        return False
        
    def updateBarLines(self):

        if self.controller.w.showComponentDimensions.get():
            # Including dimensions of all components deep.
            barsCounters = self.ga.allBarsCountersComponents
        else:
            barsCounters = self.ga.allBarsCounters
        
        # Harvest unique grid lines to be drawn. Key is y, value is longest x.
        positions = set() # x1
        usedBars = set() # (x1, x2) tuples to test if we already had one.
        
        lIndex = gIndex = 0
        
        if self.controller.w.showVerticalMeasures.get():        
            w = self.ga.glyph.width
            x = min(0, self.ga.glyph.bounds[0]) - 32
            col = 24
                
            # Arrange the layout of grid lines, so they don't overlap.    
            # Place smallest stem values first
            for value, bars in sorted(barsCounters.items()):
                for bar in bars:
                    y = bar.y[0]
                    d = bar.size
                    if (y, d) in usedBars:
                        continue
                    
                    if self._overlapsY(y, d, usedBars):
                        x -= col
                    self.verticalLayers[lIndex].setStartPoint((x, y))
                    self.verticalLayers[lIndex].setEndPoint((x, y + d))
                    self.verticalLabelLayers[lIndex].setPosition((x, y+d/2))
                    self.verticalLabelLayers[lIndex].setText(str(int(round(d))))
                    lIndex += 1

                    usedBars.add((y, d))                
                    positions.add(y)
                    positions.add(y + d)

            for y in positions:
                self.verticalGridLayers[gIndex].setStartPoint((w, y))
                self.verticalGridLayers[gIndex].setEndPoint((x, y))
                gIndex += 1
        
        # Move remaining lines and arrows heads out or sight
        for n in range(lIndex, len(self.verticalLayers)):
            self.verticalLayers[n].setStartPoint((FAR, 0))
            self.verticalLayers[n].setEndPoint((FAR, 1))
            self.verticalLabelLayers[n].setPosition((FAR, 0))
        for n in range(gIndex, len(self.verticalGridLayers)):
            self.verticalGridLayers[n].setStartPoint((FAR, 0))
            self.verticalGridLayers[n].setEndPoint((FAR, 1))

    #   S T E M  L I N E S

    def _overlapsX(self, x, d, usedStems):
        for ux, ud in usedStems:
            if x < ux + ud and x + d > ux: 
                return True
        return False
        
    def updateStemLines(self):
        """Key is y, value is set of (x1, x2) for iterations to test for free
        space and if value is already drawn."""

        if self.controller.w.showComponentDimensions.get():
            # Including dimensions of all components deep.
            stemsCounters = self.ga.allStemsCountersComponents
        else:
            stemsCounters = self.ga.allStemsCounters
        
        # Harvest unique grid lines to be drawn. Key is y, value is longest x.
        positions = set() # x1
        usedStems = set() # (x1, x2) tuples to test if we already had one.
        
        lIndex = gIndex = 0

        if self.controller.w.showHorizontalMeasures.get():        
            y = self.ga.glyph.bounds[1] - 48
            leading = 16
                
            # Arrange the layout of grid lines, so they don't overlap.    
            # Place smallest stem values first
            for value, stems in sorted(stemsCounters.items()):
                for stem in stems:
                    x = stem.x[0]
                    d = stem.size
                    if (x, d) in usedStems:
                        continue
                    
                    if self._overlapsX(x, d, usedStems):
                        y -= leading
                    self.horizontalLayers[lIndex].setStartPoint((x, y))
                    self.horizontalLayers[lIndex].setEndPoint((x + d, y))
                    self.horizontalLabelLayers[lIndex].setPosition((x + d/2, y+5))
                    self.horizontalLabelLayers[lIndex].setText(str(d))
                    lIndex += 1

                    usedStems.add((x, d))                
                    positions.add(x)
                    positions.add(x + d)

            ascender = self.ga.glyph.font.info.ascender
            for x in positions:
                self.horizontalGridLayers[gIndex].setStartPoint((x, ascender))
                self.horizontalGridLayers[gIndex].setEndPoint((x, y - 16))
                gIndex += 1
        
        # Move remaining lines and arrows heads out or sight
        for n in range(lIndex, len(self.horizontalLayers)):
            self.horizontalLayers[n].setStartPoint((FAR, 0))
            self.horizontalLayers[n].setEndPoint((FAR, 1))
            self.horizontalLabelLayers[n].setPosition((FAR, 0))
        for n in range(gIndex, len(self.horizontalGridLayers)):
            self.horizontalGridLayers[n].setStartPoint((FAR, 0))
            self.horizontalGridLayers[n].setEndPoint((FAR, 1))
            
    #   D I A G O N A L S
    
    def calcDiagonalValues(self):
        # Initialize cache of the diagonals, even if empty.
        d = self._dValues = []

        # Get diagonals found by the analyzer diagonalStems, distance is
        # calculated.
        for diagonalStems in self.ga.diagonalStems.values():
            for diagonalStem in diagonalStems:
                
                for pp0, pp1 in diagonalStem.perpendicularLines:
                    if not None in (pp0, pp1):
                        distance = sqrt((pp1.x - pp0.x)**2 + (pp1.y - pp0.y)**2)
                        d.append((distance, pp0, pp1))

    def updateTextLabel(self, layer, value, x, y):
        if int(round(value)) == value:
            sValue = '%d' % value
        else:
            # Floats get one decimal.
            sValue = '%0.1f' % value
        layer.setText(sValue)
        layer.setPosition((x, y))

    def updateDiagonals(self):
        """Draw the diagonal stems."""

        if self._dValues is None:
            self.calcDiagonalValues()
        
        # Stroke width is assumed to be set in self._dValues.
        lIndex = 0
        if self.controller.w.showDiagonalLines.get():
            for distance, pp0, pp1 in self._dValues:
                # Take real instance, instead of calculating between pp0 and pp1,
                # because of rounding errors.
                if distance > 0:
                    layer = self.diagonalLayers[lIndex]
                    layer.setStartPoint((pp0.x, pp0.y))
                    layer.setEndPoint((pp1.x, pp1.y))
                    self.updateTextLabel(self.diagonalLayerLabels[lIndex], distance, pp0.x+(pp1.x-pp0.x)/2, pp0.y+(pp1.y-pp0.y)/2)
                    lIndex += 1
        for n in range(lIndex, len(self.diagonalLayers)):
            self.diagonalLayers[n].setStartPoint((FAR, 0))
            self.diagonalLayers[n].setEndPoint((FAR, 1))
            self.diagonalLayerLabels[n].setPosition((FAR, 0))

       
    #   E V E N T S

    def glyphEditorDidSetGlyph(self, info):
        g = info['glyph']
        if g is None:
            print('### Dimensioneer (glyphEditorDidSetGlyph) No open editor')
            return # No open editor
        #print(f'(glyphEditorDidSetGlyph) /{g.name}')

        self.ga = analyzerManager.getGlyphAnalyzer(g)
        self._dValues = None # Force recalculation        
        self.update()

    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        if g is None:
            print('### Dimensioneer (glyphEditorGlyphDidChange) No open editor')
            return # No open editor
        #print(f'(glyphEditorGlyphDidChange) /{g.name}')

        self._dValues = None # Force recalculation
        self.update()
    
    def fontDocumentWindowDidOpen(self, info):
        self.filterNamesCallback()
        
    def fontDocumentDidClose(self, info):
        #self.update()
        pass

SPACE_MARKER_R = 24
POINT_MARKER_R = 6
FAR = 100000 # Put drawing stuff outside the window
KERN_LINE_SIZE = 20 # Number of glyphs on kerning line
KERN_SCALE = 0.15 #0.2

# Layout paratemers. Not using Ezui right now, just layout math.
X = Y = 50 # Position of the window, should eventually come from RF preference storage.
W, H = 400, 300 # Width and height of controller window, should eventually come from RF preference storage.
MINW, MINH, MAXW, MAXH = W, H, 3 * W, 3 * H # Min/max size of the window
M = 12 # Margin and gutter
L = 20 # Line height between controls
LL = 32 # Line height between functions
BH = 32 # Button height
TBH = 24 # Text box height
LH = 24 # Label height
POBH = 24 # Popup button height
CW = (W - 4 * M) / 3 # Column width
CW2 = 2 * CW + M # Column width
C0 = M # X position of column 0
C1 = C0 + CW + M # X position of column 1
C2 = C1 + CW + M # X position of column 2
BROWSER_BOTTOM = -36 # Save room at the bottom of the lists to add buttons.
                            
class DimensioneerController(WindowController):
        
    assistantGlyphEditorSubscriberClass = Dimensioneer

    WINDOW_CLASS = Window # FloatingWindow or Window
    TITLE = 'Dimensioneer'
    
    def build(self):        

        self.w = self.WINDOW_CLASS((X, Y, W, H), self.TITLE, 
            minSize=(MINW, MINH), maxSize=(MAXW, MAXH))

        y = L
        self.w.showHorizontalMeasures = CheckBox((C0, y + M, CW2, L), 'Show vertical measures', 
            value=True, sizeStyle='small', callback=self.update)
        y += L
        self.w.showVerticalMeasures = CheckBox((C0, y + M, CW2, L), 'Show horizontal measures', 
            value=True, sizeStyle='small', callback=self.update)
        y += L
        self.w.showComponentDimensions = CheckBox((C0, y + M, CW2, L), 'Show component positions', 
            value=True, sizeStyle='small', callback=self.update)
        y += L
        self.w.showDiagonalLines = CheckBox((C0, y + M, CW2, L), 'Show diagonals', 
            value=True, sizeStyle='small', callback=self.update)

        self.w.open()

    def update(self, sender=None):
        g = CurrentGlyph()
        if g is not None:
            g.changed()
            
    def started(self):
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None
                                        
if __name__ == '__main__':
    OpenWindow(DimensioneerController)

