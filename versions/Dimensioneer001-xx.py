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
from AppKit import (NSBezierPath, NSColor, NSFontAttributeName, NSFont,
        NSForegroundColorAttributeName, NSAttributedString, NSMakeRect, NSGraphicsContext)

# Import of resources available in RoboFont
from vanilla import (Window, FloatingWindow, TextBox, HorizontalRadioGroup, EditText, PopUpButton, 
    List, CheckBox, RadioGroup, Button)
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

MAX_BARS = 40
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
        self.horizontalLayers = []
        self.horizontalMarkerLeftLayers = []
        self.horizontalMarkerRightLayers = []
        self.horizontalLayerLabels = []
        self.verticalLayers = []
        self.verticalMarkerTopLayers = []
        self.verticalMarkerBottomLayers = []
        self.verticalLayerLabels = []

        for n in range(NUM_LAYER_ELEMENTS):
            
            # Diagonal lines
            
            self.diagonalLayers.append(self.backgroundContainer.appendLineSublayer(name='Diagonal%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5
            ))
            self.diagonalLayerLabels.append(self.backgroundContainer.appendTextLineSublayer(name='DiagonalLabel%d' % n,
                position=(FAR, 0),
                text='',
                horizontalAlignment='center',
                font='Courier',
                pointSize=LABEL_SIZE,
                fillColor=(0, 0, 0, 1),
            ))
            
            # Horizontal lines
            
            self.horizontalLayers.append(self.backgroundContainer.appendLineSublayer(name='Horizontal%d' % n,
                startPoint=(100, 0),
                endPoint=(200, 301),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5,
            ))
            self.horizontalMarkerLeftLayers.append(self.backgroundContainer.appendOvalSublayer(name='HorizontalMarkerLeftLabel%d' % n,
                position=(FAR, 0),
                size=(LINE_MARKER_SIZE, LINE_MARKER_SIZE),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5,
                fillColor=None,
            ))
            self.horizontalMarkerRightLayers.append(self.backgroundContainer.appendOvalSublayer(name='HorizontalMarkerRightLabel%d' % n,
                position=(FAR, 0),
                size=(LINE_MARKER_SIZE, LINE_MARKER_SIZE),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5,
                fillColor=None,
            ))
            self.horizontalLayerLabels.append(self.backgroundContainer.appendTextLineSublayer(name='HorizontalLabel%d' % n,
                position=(FAR, 0),
                text='',
                horizontalAlignment='center',
                font='Courier',
                pointSize=LABEL_SIZE,
                fillColor=(0, 0, 0, 1),
            ))
            
            # Vertical lines
            
            self.verticalLayers.append(self.backgroundContainer.appendLineSublayer(name='Vertical%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 1),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5
            ))
            self.verticalMarkerTopLayers.append(self.backgroundContainer.appendOvalSublayer(name='VerticalMarkerTopLabel%d' % n,
                position=(FAR, 0),
                size=(LINE_MARKER_SIZE, LINE_MARKER_SIZE),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5,
                fillColor=None,
            ))
            self.verticalMarkerBottomLayers.append(self.backgroundContainer.appendOvalSublayer(name='VerticalMarkerBottomLabel%d' % n,
                position=(FAR, 0),
                size=(LINE_MARKER_SIZE, LINE_MARKER_SIZE),
                strokeColor=(0, 0, 0, 1),
                strokeWidth=0.5,
                fillColor=None,
            ))
            self.verticalLayerLabels.append(self.backgroundContainer.appendTextLineSublayer(name='VerticalLabel%d' % n,
                position=(FAR, 0),
                text='',
                horizontalAlignment='center',
                font='Courier',
                pointSize=LABEL_SIZE,
                fillColor=(0, 0, 0, 1),
            ))
                
    def started(self):
        pass

    def destroy(self):
        pass
                
    #   C A L L B A C K S
                    
    def update(self):
        self.updateDiagonals()
        #self.updateBarLines()
    
    #   B A R  L I N E S

    def updateBarLines(self):
        """Key is y, value is set of (x1, x2) for iterations to test for free
        space and if value is already drawn."""

        positions = {}

        # Harvest unique grid lines to be drawn. Key is y, value is longest x.
        grid = {}

        if self.controller.w.showComponentDimensions.get():
            # Including dimensions of all components deep.
            barsCounters = self.ga.allBarsCountersComponents
        else:
            barsCounters = self.ga.allBarsCounters

        index = 0

        # Place smallest stem values first
        for value, bars in sorted(barsCounters.items()):
            index += len(bars)
            if index > MAX_BARS:
                # Threshold for max amount of bars to show, starting with
                # smallest.
                break
            self.updateBarsCounters(value, bars, positions, grid)

        # Draw the collected grid lines.
        x2 = self.ga.width
        path = NSBezierPath.bezierPath()
        #self._gridColor.set()

        for y, x in grid.items():
            path.moveToPoint_((x, y))
            path.lineToPoint_((x2, y))

        path.setLineWidth_(0.4)
        path.stroke()

    def updateBarsCounters(self, value, barsCounters, positions, grid):
        """Draw the stem or counter. Color is dependent on the type."""
        colors = {False: STEM_COLOR, True: COUNTER_COLOR}

        for barOrCounter in barsCounters:
            # Position of bar or counter, including component offset.
            y, _ = barOrCounter.y
            color = colors[barOrCounter.isWhite()]
            self.updatePositionedVLine(y, value, positions, grid, color)

    def updatePositionedVLine(self, y, value, positions, grid, color):
        """Draw the line at x with length value, on a horizontal position where
        there is still fit.  If not fitting, take the next column to the left
        and mark the occupied position in positions. Also keep the grid
        position for x and y, so the caller knows where to draw the grid
        lines."""
        # Largest x first, scan from top to bottom to find space.
        sortedX = sorted(positions.keys(), reverse=True)
        x = None
        for sx in sortedX:
            k = y, value

            # Identical already done, ignore.
            if k in positions[sx]:
                return

            # Is there space on this y line?
            if self._hasSpace(y, value, positions[sx]):
                self.drawVLine(value, sx, y, grid, color)
                positions[sx].add((y, value))
                return

        # Could not find space in x, add new column if we have valid sortedX or
        # there is a bounding box.
        if not sortedX and self.ga.minX is not None:
            x = min(0, self.ga.minX) - 2 * XLINE * self.scale
        elif sortedX:
            x = min(sortedX) - XLINE * self.scale

        # Did we find a valid x?
        if x is not None:
            positions[x] = set([(y, value)])
            self.drawVLine(value, x, y, grid, color)

    def drawVLine(self, value, x, y, grid, color):
        y1 = y+value
        x1 = x - XLINE * self.scale / 2
        # size of arrow head.
        D = TEXT_SIZE * self.scale / 3
        D2 = D*2

        color.set()
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((x, y))
        path.lineToPoint_((x, y1))

        # Save all grid positions for later drawing, to avoid double lines.
        grid[y] = min(grid.get(y, 0), x1)
        grid[y1] = min(grid.get(y1, 0), x1)

        # Arrow head
        path.moveToPoint_((x - D, y + D2))
        path.lineToPoint_((x, y))
        path.lineToPoint_((x + D, y + D2))

        path.moveToPoint_((x - D, y1- D2))
        path.lineToPoint_((x, y1))
        path.lineToPoint_((x + D, y1 - D2))

        path.setLineWidth_(0.4 * self.scale)
        path.stroke()
        self.drawNumberText(color, value, x, y+(y1-y)/2)

    def drawNumberText(self, color, value, x, y):
        attributeStyleName = {
            NSFontAttributeName : NSFont.systemFontOfSize_(TEXT_SIZE * self.scale),
            NSForegroundColorAttributeName : color
        }

        if int(round(value)) == value:
            sValue = '%d' % value
        else:
            # Floats get one decimal.
            sValue = '%0.1f' % value

        # Double space to position.
        nsString = NSAttributedString.alloc().initWithString_attributes_(sValue, attributeStyleName)
        width, height = nsString.size()
        nsString.drawInRect_(NSMakeRect(x - width / 2, y - height/2, width, height))
          
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
                    self.updateTextLabel(self.diagonalLayerLabels[lIndex], distance, pp0.x+(pp1.x-pp0.x)/2, pp0.y+(pp1.y-pp0.y)/2 + LABEL_SIZE)
                    lIndex += 1
        for n in range(lIndex, len(self.diagonalLayers)):
            self.diagonalLayers[n].setStartPoint((FAR, 0))
            self.diagonalLayers[n].setEndPoint((FAR, 1))
            self.diagonalLayerLabels[n].setPosition((FAR, 0))

       
    #   E V E N T S

    def glyphEditorDidSetGlyph(self, info):
        if not info['glyph']:
            return # No opeb editor
        g = info['glyph']
        print('(glyphEditorDidSetGlyph)', g.name)

        self.ga = analyzerManager.getGlyphAnalyzer(g)
        self._dValues = None # Force recalculation
        
        self.update()

    def glyphEditorGlyphDidChange(self, info):
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
        self.w.showHorizonalLines = CheckBox((C0, y + M, CW2, L), 'Show vertical measures', 
            value=True, sizeStyle='small', callback=self.update)
        y += L
        self.w.showVerticalLines = CheckBox((C0, y + M, CW2, L), 'Show horizontal measures', 
            value=True, sizeStyle='small', callback=self.update)
        y += L
        self.w.showComponentDimensions = CheckBox((C0, y + M, CW2, L), 'Show component positions', 
            value=True, sizeStyle='small', callback=self.update)
        y += L
        self.w.showDiagonalLines = CheckBox((C0, y + M, CW2, L), 'Show diagonals', 
            value=True, sizeStyle='small', callback=self.update)

        self.w.open()

    def update(self):
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

