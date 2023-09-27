# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    Dimensioneer.py
#
#   TODO: Add overshoot, as it was in original Dimensioneer.
#

from math import sqrt
import traceback

import vanilla
from AppKit import (NSBezierPath, NSColor, NSFontAttributeName, NSFont,
        NSForegroundColorAttributeName, NSAttributedString, NSMakeRect, NSGraphicsContext)
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.model.objects.glyph import getComponents
from tnbits.tools.basetool import BaseTool
from tnbits.toolbox.transformer import TX
from tnbits.vanillas.preferencesgroup import PreferencesGroup

FAR = 10000

SPACE_MARKER_R = 16
POINT_MARKER_R = 6
FAR = 100000 # Put drawing stuff outside the window
KERN_LINE_SIZE = 32 # Number of glyphs on kerning line
KERN_SCALE = 0.15 #0.2

W, H = 400, 600
VIEWMINSIZE = VIEWMAXSIZE = (W, H)
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C2 = C1 + CW + M

WindowClass = vanilla.Window

#from mojo.events import addObserver
'''
from mojo.drawingTools import (rect, closePath, drawPath, newPath, moveTo,
        lineTo, oval, fontSize, translate, rotate, text, fill, curveTo, stroke,
        strokeWidth)
'''


class Dimensioneer(Subscriber, WindowController):
    """The tool *Dimensioneer* shows dimensions, proportions and relations in
    the editor window."""
    C = BaseTool.C

    TOOLID = 'tnDimensioneer'
    NAME = 'Dimensioneer'
    CATEGORY = C.CATEGORY_DESIGN
    USEFLOATINGWINDOW = False
    VIEWX = VIEWY = 100
    VIEWHEIGHT = 500
    VIEWWIDTH = BaseTool.VIEWWIDTH / 2
    VIEWMINSIZE = VIEWWIDTH, VIEWHEIGHT
    VIEWMAXSIZE = VIEWWIDTH, 1000

    TOOLOBSERVERS = (
        ('currentGlyphChanged', C.EVENT_CURRENTGLYPHCHANGED),
        ('viewChangedGlyph', C.EVENT_VIEWDIDCHANGEGLYPH),
        ('drawInactive', C.EVENT_DRAWINACTIVE),
        ('draw', C.EVENT_DRAW),
    )

    """Dimensioneer doesn't have a window on it's own. Use the DisplayItems
    tools to set the preferences. Label in RF preferences. Sort key is to
    define the automatic ordering of groups of parameters. Drawing switches."""
    PREFERENCE_MODEL = dict(
        drawInactiveWindows=dict(label=u'Draw inactive windows', sort=5,
            type=C.PREFTYPE_BOOL, default=True),
        drawSelectedPoints=dict(label=u'Draw selected points', sort=8,
            type=C.PREFTYPE_BOOL, default=True),
        drawXDimensions=dict(label=u'Draw X dimensions', sort=10,
            type=C.PREFTYPE_BOOL, default=True),
        drawYDimensions=dict(label=u'Draw Y dimensions', sort=20,
            type=C.PREFTYPE_BOOL, default=True),
        drawOvershoots=dict(label=u'Draw Y overhoots', sort=25,
            type=C.PREFTYPE_BOOL, default=True),
        drawComponentTransform=dict(label=u'Draw component transform', sort=30,
            type=C.PREFTYPE_BOOL, default=True), # Use stem color for the lines
        drawDiagonals=dict(label=u'Draw diagonal dimensions', sort=36,
            type=C.PREFTYPE_BOOL, default=True),
        diagonalColor=dict(label=u'Diagonal color', sort=40,
            type=C.PREFTYPE_COLOR, default=(.4, .4, .8, .8)),
        drawComponentDimensions=dict(label=u'Draw component dimensions',
            sort=50, type=C.PREFTYPE_BOOL, default=True),
        gridColor=dict(label=u'Grid color', sort=70, type=C.PREFTYPE_COLOR,
            default=(.2, .2, .2, .8)),
        stemColor=dict(label=u'Stem color', sort=72, type=C.PREFTYPE_COLOR,
            default=(.2, .2, .2, .8)),
        maxStems=dict(label=u'Max showing stems', sort=80, type=C.PREFTYPE_INT,
            default=40),
        maxBars=dict(label=u'Max showing bars', sort=80, type=C.PREFTYPE_INT,
            default=20),
        metricsColor=dict(label=u'Metrics color', sort=90,
            type=C.PREFTYPE_COLOR, default=(.2, .2, .8, .8)),
        counterColor=dict(label=u'Counter color', sort=100,
            type=C.PREFTYPE_COLOR, default=(.8, .2, .2, .8)),
        endWidth=dict(label=u'Line end width', sort=200, type=C.PREFTYPE_INT,
            default=3), # Marker size on dimension line endings.
        strokeWidthValue=dict(label=u'Line thickness', sort=210,
            type=C.PREFTYPE_INT, default=0.5), # Line thickness
        textSize=dict(label=u'Text size', sort=230, type=C.PREFTYPE_INT,
            default=9), # Text size of value labels,
    )

    def started(self):
        self.sampleText = None # Initialize sample text storage for FontGoggles file.
        self.randomWord = choice(ULCWORDS)
        #print("subscription started")
        #self.controller.addInfo("subscription started")        
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.__class__)
    
    def destroy(self):
        #print("stop subscription")
        self.foregroundContainer.clearSublayers()
        #self.controller.addInfo("stop subscription")
        unregisterGlyphEditorSubscriber(self.__class__)
        self.assistantGlyphEditorSubscriberClass.controller = None
                            
    def populateView(self):
        x = y = 4
        #view = self.getView()
                
        # TODO: scroller.
        #pGroup = PreferencesGroup(self, (10, 10, -10, -10), self.preferenceChanged)
        #view.preferences = pGroup.group

    def preferenceChanged(self, sender):
        """One of the preferences changed. Get the all values of the current
        group and store them into the RoboFont preference area.  Checks if the
        tool is valid. Runs through the preference model, and gets the values
        from the group UI controls. Then stores the (new) values in the
        RoboFont preference area."""
        group = self.getView().preferences

        for name, preference in self.PREFERENCE_MODEL.items():
            pType = preference['type']

            if pType == self.C.PREFTYPE_COLOR:
                color = getattr(group, 'tControl0_%s' % name).get()
                r = color.redComponent()
                g = color.greenComponent()
                b = color.blueComponent()
                a = color.alphaComponent()
                self.setPreference(name, (r, g, b, a))

            elif pType == self.C.PREFTYPE_BOOL:
                widget = getattr(group, 'tControl0_%s' % name)
                value = widget.get()
                self.setPreference(name, value)
                #setattr(self, name, value)
            elif pType == self.C.PREFTYPE_INT:
                value = TX.asIntOrNone(getattr(group, 'tControl0_%s' % name).get())

                if value is not None:
                    self.setPreference(name, value)

            elif pType == self.C.PREFTYPE_RECT:
                rect = list(self.getPreference(name, (0, 0, 0, 0)))

                for n in range(4): # 4 input boxes for x, y, w, h.
                    value = TX.asIntOrNone(getattr(group, 'tControl%d_%s' % (n, name)).get())

                    if value is not None:
                        rect[n] = value

                self.setPreference(name, rect)
            elif pType == self.C.PREFTYPE_SIZE:
                size = list(self.getPreference(name, (0, 0)))

                for n in range(2): # 2 input boxes for w, h.
                    value = TX.asIntOrNone(getattr(group, 'tControl%d_%s' % (n, name)).get())

                    if value is not None:
                        rect[n] = value
                self.setPreference(name, size)

        # TODO: use setattr instead.
        self.setPreferences()
        self.update()

    def getCurrentGlyph(self):
        return CurrentGlyph()
        
    def getGlyph(self):
        glyph = self.getCurrentGlyph()

        if glyph is not None:
            self.glyph = glyph
            self.ga = analyzerManager.getGlyphAnalyzer(glyph)
            self.ga.reset()
            self.resetCache()

    def setGA(self, glyph):
            self.ga = analyzerManager.getGlyphAnalyzer(glyph)
            self.ga.reset()

    def resetCache(self):
        self._dValues = None # Caching storage for glyph values
        self._strings = {}

    def build(self):
        """Dimensioneer doesn't have a window of it's own. Use the
        DisplayItems tools to set the preferences."""

        self.resetCache()
        self.glyph = None
        self.scale = 1.0
        self.ga = None

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
        #self.backgroundContainer.appendTextLineSublayer
        #self.backgroundContainer.appendRectangleSublayer
        #self.backgroundContainer.appendPathSublayer
        #self.backgroundContainer.appendLineSublayer
        self.diagonalLayers = []
        for n in range(50):
            self.diagonalLayers.append(container.appendLineSublayer(
                startPoint=(FAR, 0),
                endPoint=(FAR+10, 0),
                strokeColor=(0, 0, 0, 0),
                strokeWidth=0.5
            ))

        self.setPreferences()
        #screen, posSize = self.getWindowScreenPosSize()
        posSize = (50, 50, 400, 400)
        self.w = WindowClass(posSize=posSize, title='Dimensioneer-M', 
            minSize=VIEWMINSIZE, maxSize=VIEWMAXSIZE)
        self.populateView()

        self.w.open()
        
        # Set bindings of window events and open window.
        #self.openWindow()
        self.resetAnalyzer()
        self.getGlyph()
        self.updateGlyph()

    def getPreference(self, key):
        return self.PREFERENCE_MODEL[key]
        
    def setPreferences(self):
        # TODO: preferences as booleans instead of PyObjC longs.
        self._drawInactiveWindows = self.getPreference('drawInactiveWindows')
        self._drawSelectedPoints = self.getPreference('drawSelectedPoints')
        self._drawX = self.getPreference('drawXDimensions')
        self._drawY = self.getPreference('drawYDimensions')
        self._drawD = self.getPreference('drawDiagonals')
        self._drawOvershoots = self.getPreference('drawOvershoots')
        self._drawComponentTransform = self.getPreference('drawComponentTransform')
        self._drawComponentDimensions = self.getPreference('drawComponentDimensions')
        self._gridColor = self.getPreference('gridColor')
        self._maxStems = min(max(TX.asInt(self.getPreference('maxStems')) or 2, 40), 100) # Between 2 and 100
        self._maxBars = min(max(TX.asInt(self.getPreference('maxBars')) or 2, 40), 100)
        self._stemColor = self.getPreference('stemColor')
        self._metricsColor = self.getPreference('metricsColor')
        self._counterColor = self.getPreference('counterColor')
        self._RGBdiagonalColor = self.getPreference('diagonalColor')
        self._endWidth = self.getPreference('endWidth')
        self._strokeWidthValue = self.getPreference('strokeWidthValue')
        self._textSize = self.getPreference('textSize')
        #self.updateGlyph()

    def resetAnalyzer(self):
        self.resetCache()

    def updateGlyph(self):
        # Calculate and display the dimensions of the current glyph.
        self.resetCache()
        self.getGlyph()
        self.drawDimensions()

    def viewChangedGlyph(self, info):
        self.resetCache()
        self.drawDimensions()

    def glyphChanged(self, info):
        """Rest the glyph analyzer if there is a current glyph."""
        self.getGlyph()

    YLINE = 16
    # Fitting 3 digits of y-coordinate.
    XLINE = 22

    def drawInactive(self, event):
        """Always draw, even if inactive"""
        if self._drawInactiveWindows:
            self.draw(event)

    def update(self):
        # TODO: update request to RF canvas.
        if self.glyph:
            self.glyph.update()

    def draw(self, event):
        """Drawing event on mouse and dragging."""
        if event['glyph'] != self.glyph:
            self.resetCache()
            self.glyph = event['glyph']
            self.setGA(self.glyph)
            self.calcDValues()
        else:
            self.ga.reset()
        if event['scale'] != self.scale:
            self.scale = event['scale']

        self.drawDimensions()

    def drawDimensions(self):
        if self.glyph is None or self.ga is None:
            return

        self.drawComponentTransform()
        self.drawStemLines()
        self.drawBarLines()
        self.drawOvershootLines()
        self.drawDiagonals()

    def drawComponentTransform(self):
        """Draw the transformation of the component, if @dx@ or @dy@ are not
        *0*."""

        if not self._drawComponentTransform:
            return

        # Stroke width is assumed to be set.
        # Only if there are components in the glyph
        for component in (getComponents(self.ga.glyph) or []):

            # Draw arrow line from original middle of bounding box to new
            # middle. Label is the transformation.
            # Or component.baseName ???
            if component.baseGlyph in self.ga.parent.style:
                # Get component glyph analyzer
                cga = self.ga.parent[component.baseGlyph]
                bounds = cga.boundings

                if not None in bounds:
                    x0, y0, x1, y1 = bounds
                    # Just to dx/dy transformation now. Show others.
                    tx1, ty1, tx2, ty2, dx, dy = component.transformation
                    # Also show other transformations here as a warning that
                    # these are not supported.
                    # Not just test on 0 and float, value can be None for some
                    # reason.
                    dx = int(round(dx or 0))
                    dy = int(round(dy or 0))

                    # Don't show vector if no transformation.
                    if dx or dy:
                        # Show sublabel is skew / rotate / flip is different
                        # from [1,0,0,1]
                        if tx1 != 1 or ty1 != 0 or tx2 != 0 or ty2 != 1:
                            subLabel = '[%s %s %s %s]' % (tx1, ty1, tx2, ty2)
                        else:
                            subLabel = None

                        color = self._stemColor
                        #color = self._RGBdiagonalColor
                        color.set()
                        path = NSBezierPath.bezierPath()
                        path.moveToPoint_((x0, y0))
                        path.lineToPoint_((x0 + dx, y0 + dy))
                        path.setLineWidth_(0.4 * self.scale)
                        path.stroke()

                        # TODO: show tranform string.
                        #self.drawNumberText(color, distance, pp0.x, pp0.y)

                        '''
                        Line.draw(x0, y0, x0 + dx, y0 + dy,
                                self._RGBdiagonalColor, self.scale,
                                drawTerminals=self.C.TERMINAL_SQUARE,
                                drawLabel=True, xyLabel=True,
                                subLabel=subLabel, terminalWidth=self._endWidth,
                            strokeWidthValue=self._strokeWidthValue,
                            textSize=self._textSize)
                        '''

    def _hasSpace(self, p, value, values):
        for p1, value1 in values:
            if p + value > p1 and p < p1 + value1:
                return False
        return True

    def drawStemLines(self):
        """Key is y, value is set of (x1, x2) for iterations to test for free
        space and if value is already drawn."""

        if not self._drawX:
            return

        positions = {}
        # Harvest unique grid lines to be drawn. Key is x, value is smallest y.
        grid = {}

        # Draw left and right margins.
        self.drawMargins(positions, grid)

        # Draw the all types of stems and counters as found by the analyzer.
        if self._drawComponentDimensions:
            # Including dimensions of all components deep.
            stemsCounters = self.ga.allStemsCountersComponents
        else:
            stemsCounters = self.ga.allStemsCounters

        index = 0

        # Place smallest stem/counter values first.
        for value, stems in sorted(stemsCounters.items()):
            index += len(stems)
            if index > self._maxStems:
                # Threshold for max amount of stems to show, starting with
                # smallest.
                break
            self.drawStemsCounters(value, stems, positions, grid)

        # Draw the horizontal measures of the bounding box.
        self.drawBoundsX(positions, grid)

        # Draw the collected unique grid lines.
        # TODO: Make vertical position of the line equal to the max y-value +
        # overshoot, instead of fixed y2.
        y2 = 2000 * self.scale
        path = NSBezierPath.bezierPath()
        skip = (0, self.ga.width)
        self._gridColor.set()

        for x, y in grid.items():
            # Skip special lines as side bearings.
            if x in skip:
                continue

            path.moveToPoint_((x, y))
            path.lineToPoint_((x, y2))

        path.setLineWidth_(0.4 * self.scale)
        path.stroke()

    def drawMargins(self, positions, grid):
        """Draw the margins at free line positions"""
        leftMargin = self.ga.leftMargin
        leftBaseMargin = self.ga.leftBaseMargin
        rightMargin = self.ga.rightMargin
        rightBaseMargin = self.ga.rightBaseMargin
        width = self.ga.width

        if not None in (leftMargin, rightMargin):
            values = [
                (min(0, leftMargin), abs(leftMargin)),
                (min(width, width - rightMargin), abs(rightMargin))
            ]

            # In case of overhanging accents, etc. add base margin.
            if leftMargin != leftBaseMargin:
                values.append((min(0, leftBaseMargin), abs(leftBaseMargin)))

            # In case of overhanging accents, etc. add base margin.
            if rightMargin != rightBaseMargin:
                values.append((min(width, width - rightBaseMargin), abs(rightBaseMargin)))

            # Draw the metrics lines.
            for x, value in sorted(values):
                self.drawPositionedHLine(x, value, positions, grid, self._gridColor)

    def drawBoundsX(self, positions, grid):
        """Draw the horizontal bounding box and half size."""
        x1, _, x2, _ = self.ga.boundings

        # Only if there is a bounding box.
        if x1 is not None:
            w = x2 - x1
            w2 = w / 2

            for x, w in ((x1, w2), (x1+w2, w2), (x1, w)):
                self.drawPositionedHLine(x, w, positions, grid, self._gridColor)

    def drawStemsCounters(self, value, stemsCounters, positions, grid):
        """Draw the stem or counter. Color is dependent on the type."""
        colors = {False: self._stemColor, True: self._counterColor}

        for stemOrCounter in stemsCounters:
            # Position of stem or counter, including component offset.
            x, _ = stemOrCounter.x
            color = colors[stemOrCounter.isWhite()]
            self.drawPositionedHLine(x, value, positions, grid, color)

    def drawPositionedHLine(self, x, value, positions, grid, color):
        """Draw the line at x with lentgth value, on a vertical position where
        there is still fit.  If not fitting, take the next line and mark the
        occupied position in positions. Also keep the grid position for x and
        y, so the caller knows where to draw the grid lines."""

        # Largest y first, scan from top to bottom to find space.
        sortedY = sorted(positions.keys(), reverse=True)
        y = None

        for sy in sortedY:
            k = x, value
            # Identical already done, ignore.
            if k in positions[sy]:
                return

            # Is there space on this y line?
            if self._hasSpace(x, value, positions[sy]):
                self.drawHLine(value, x, sy, grid, color)
                positions[sy].add((x, value))
                return

        # Could not find space in y, add new line if we have valid sortedY or
        # there is a bounding box.
        if not sortedY and self.ga.minY is not None:
            y = min(0, self.ga.minY) - 2 * self.YLINE * self.scale
        elif sortedY:
            y = min(sortedY) - self.YLINE * self.scale

        # Did we find a valid y?
        if y is not None:
            positions[y] = set([(x, value)])
            self.drawHLine(value, x, y, grid, color)

    def drawHLine(self, value, x, y, grid, color):
        x1 = x + value
        y1 = y - self.YLINE * self.scale / 2
        # size of arrow head.
        D = self._textSize * self.scale / 3
        D2 = D * 2

        color.set()
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((x, y))
        path.lineToPoint_((x1, y))

        # Save all grid positions for later drawing, to avoid double lines.
        grid[x] = min(grid.get(x, 0), y1)
        grid[x1] = min(grid.get(x1, 0), y1)

        # Arrow head
        path.moveToPoint_((x + D2, y + D))
        path.lineToPoint_((x, y))
        path.lineToPoint_((x + D2, y - D))

        path.moveToPoint_((x1 - D2, y + D))
        path.lineToPoint_((x1, y))
        path.lineToPoint_((x1 - D2, y - D))

        path.setLineWidth_(0.4 * self.scale)
        path.stroke()

        self.drawNumberText(color, value, x+(x1-x)/2, y)

    def drawNumberText(self, color, value, x, y):
        attributeStyleName = {
            NSFontAttributeName : NSFont.systemFontOfSize_(self._textSize * self.scale),
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

    def drawOvershootLines(self):
        if not self._drawOvershoots:
            return

        overshoots = self.ga.parent.overshoots
        glyphName = self.ga.name
        path = NSBezierPath.bezierPath()
        w = self.ga.width
        values = None

        # This is a capital, show capital overshoots.
        if glyphName[0].upper() == glyphName[0]:
            if 'O' in overshoots:
                values = overshoots['O']
        elif '.sc' in glyphName:
            if 'O.sc' in overshoots:
                values = overshoots['O.sc']
        else:
            if 'o' in overshoots:
                values = overshoots['o']

        if values is not None:
            for y, value in values:
                path.moveToPoint_((0, y + value))
                path.lineToPoint_((w, y + value))

            NSColor.redColor().set()
            path.setLineWidth_(0.4 * self.scale)
            path.stroke()

    def drawBarLines(self):
        """Key is y, value is set of (x1, x2) for iterations to test for free
        space and if value is already drawn."""
        if not self._drawY:
            return

        positions = {}

        # Harvest unique grid lines to be drawn. Key is y, value is longest x.
        grid = {}

        if self._drawComponentDimensions:
            # Including dimensions of all components deep.
            barsCounters = self.ga.allBarsCountersComponents
        else:
            barsCounters = self.ga.allBarsCounters

        index = 0

        # Place smallest stem values first
        for value, bars in sorted(barsCounters.items()):
            index += len(bars)
            if index > self._maxBars:
                # Threshold for max amount of bars to show, starting with
                # smallest.
                break
            self.drawBarsCounters(value, bars, positions, grid)

        # Draw the collected grid lines.
        x2 = self.ga.width
        path = NSBezierPath.bezierPath()
        self._gridColor.set()

        for y, x in grid.items():
            path.moveToPoint_((x, y))
            path.lineToPoint_((x2, y))

        path.setLineWidth_(0.4*self.scale)
        path.stroke()

    def drawBarsCounters(self, value, barsCounters, positions, grid):
        """Draw the stem or counter. Color is dependent on the type."""
        colors = {False: self._stemColor, True: self._counterColor}

        for barOrCounter in barsCounters:
            # Position of bar or counter, including component offset.
            y, _ = barOrCounter.y
            color = colors[barOrCounter.isWhite()]
            self.drawPositionedVLine(y, value, positions, grid, color)

    def drawPositionedVLine(self, y, value, positions, grid, color):
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
            x = min(0, self.ga.minX) - 2 * self.XLINE * self.scale
        elif sortedX:
            x = min(sortedX) - self.XLINE * self.scale

        # Did we find a valid x?
        if x is not None:
            positions[x] = set([(y, value)])
            self.drawVLine(value, x, y, grid, color)

    def drawVLine(self, value, x, y, grid, color):
        y1 = y+value
        x1 = x - self.XLINE * self.scale / 2
        # size of arrow head.
        D = self._textSize * self.scale / 3
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

    #   D I A G O N A L S

    def calcDValues(self):
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

    def drawDiagonals(self):
        """Draw the diagonal stems."""
        if not self._drawD:
            return

        color = self._stemColor
        #color = self._RGBdiagonalColor

        if self._dValues is None:
            self.calcDValues()

        # Stroke width is assumed to be set in self._dValues.
        for lIndex, (distance, pp0, pp1) in enumerate(self._dValues):
            # Take real instance, instead of calculating between pp0 and pp1,
            # because of rounding errors.
            if distance > 0:
                layer = self.diagonalLayers[lIndex]
                layer.setStartPoint((pp0.x, pp0.y))
                layer.setEndPoint((pp0.x, pp0.y))
                self.drawNumberText(color, distance, pp0.x+(pp1.x-pp0.x)/2, pp0.y+(pp1.y-pp0.y)/2)
        for n in range(lIndex, len(self.diagonalLayers)):
            self.diagonalLayers[n].setStartPoint((FAR, 0))
            self.diagonalLayers[n].setEndPoint((FAR, 10))

if __name__ == '__main__':
    OpenWindow(Dimensioneer)
