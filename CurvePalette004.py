# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................

import math
from copy import copy
from merz import MerzView
from vanilla import Window, PopUpButton, CheckBox, Button
from AppKit import *

from mojo.events import extractNSEvent
from mojo.roboFont import OpenWindow
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

W = H = 300
ML = MR = 8
MT = 24
MB = 72
BUTTON_HEIGHT = 24
POPUP_HEIGHT = 24
POPUP_WIDTH = 40
 
GRID_LINE = 0.25
GRID_COLOR = (0.25, 0.25, 0.25, 1)
DIAGONAL_COLOR = (0.85, 0.85, 0.85, 1)
BEST_CIRCLE_CELL_COLOR = (0.15, 0.15, 0.15, 1)
BEST_CIRCLE_FILL_COLOR = (1, 1, 1, 0.5)
MARQUEE_COLOR = (0, 0, 0, 0.15)
POINT_SIZE = 8
INVISIBLE_BUTTON_COLOR = (1, 0, 0, 0.5)
# Point-tension colors
POINT_FILL_COLOR = (1, 1, 0, 1)
POINT_STROKE_COLOR = (0, 0, 0, 1)
# Cell colors
ALL_SELECTED_COLOR = (1, 0, 0, 0.85)
PART_SELECTED_COLOR = (0, 0, 1, 0.85)
UNSELECTED_COLOR = (0, 0.5, 0, 0.85)

MAX_CELLS = 80 # More?
MAX_POINTS = 80 # More?
# Min and max range of the grid. Make sure that the values cannot overlap.
MIN_RANGE = range(60, 19, -5) # (60, 55, 50, 45, 40, 35, 30, 25, 20)
MAX_RANGE = range(100, 65-1, -5) # (100, 95, 90, 85, 80, 75, 70, 65)
# Limit the choice of possible grid sizes. 
GRID_SIZES = range(12, 33) # 12 - 32 grid sizes
GRID_SIZE = 18 # Default number of cells in the grid. Value is stored in the font.lib and self.preferences

PREFERENCES_LIB = 'TYPETR.CurvePalette' # Key for storage in font.lib
DEFAULT_PREFERENCES = dict(minRange=30, maxRange=100, gridSize=GRID_SIZE)

curvePaletteController = None # Little cheat, to make the assistant available from the window. How to do this otherwise?

def common(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    returns intersection point if it exists. Otherwise (None, None) is answered.
    http://en.wikipedia.org/wiki/Line-line_intersection
    """
    d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if d != 0:
        m1 = (x1*y2-y1*x2)
        m2 = (x3*y4-y3*x4)
        return (m1*(x3-x4) - m2*(x1-x2)) / d, (m1*(y3-y4) - m2*(y1-y2)) / d
    return None, None

def inbetween(a,b,c):
    if ((a>=b and b>=c) or (a<=b and b<=c)):
        return 1
    return 0

def orthogonal(x1, y1, x2, y2):
    """Answers the line that goes orthogonal through the middle point."""
    mx, my = (x1 + x2)/2, (y1 + y2)/2
    return mx, my, mx + (y2 - y1), my + (x1 - x2)

def determinant(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

    # ---------------------------------------------------------------------------------------------------------
    #   B A S E  C L A S S E S

class BaseVector:

    def __init__(self, xy=0, y=0):
        if isinstance(xy, (tuple, list)):
            x, y = xy
        self.vector = x, y

    def as_pt(self):
        return self.vector

    def __add__(self, other):
        """ vector + vector """
        x = self.vector[0] + other.vector[0]
        y = self.vector[1] + other.vector[1]
        return self.__class__(x, y)

    def __sub__(self, other):
        """ vector - vector """
        x = self.vector[0] - other.vector[0]
        y = self.vector[1] - other.vector[1]
        return self.__class__(x, y)

    def __neg__(self):
        """ -vector """
        x = -self.vector[0]
        y = -self.vector[1]
        return self.__class__(x, y)

    def __mul__(self, other):
        """ vector * vector """
        x = self.vector[0] * other
        y = self.vector[1] * other
        return self.__class__(x, y)

    def __div__(self, other):
        """ vector / 2 """
        x = self.vector[0] / other
        y = self.vector[1] / other
        return self.__class__(x, y)

    def __getitem__(self, key):
        """ vector['x']
        vector['y'] """
        return self.vector[key]

    def __setitem__(self, key, value):
        self.vector[key] = value

    def _length(self):
        """ len(vector) """
        x2 = self.vector[0] * self.vector[0]
        y2 = self.vector[1] * self.vector[1]
        return math.sqrt(x2 + y2)

    def fromPoint(self, p):
        """ vector.fromPoint(p) """
        self.vector[0] = p[0]
        self.vector[1] = p[1]

    def normal(self):
        """
        XXX this makes no sense.... the normal vector is the same as self, but with length 1
        perpendicular vector
        """
        l = self.length()
        return self.__class__(-self.vector[1] / l , self.vector[0] / l)

    def ortho(self):
        """Answer the orthogonal vector of self."""
        x, y = self.vector
        return self.__class__(-y, x)

    def angle(self):
        if self.vector[1] != 0:
            rd = 180 / math.pi
            h = self.vector[0]
            v = self.vector[1]
            a = math.atan( h/v ) * rd
            q = self.quadrant()
            if q == 1:
                return a
            elif q == 2:
                return 180 + a
            elif q == 3:
                return 270 - a
            else:
                return 360 - a
        else:
            return 90

class IntVector(BaseVector):

    def __init__(self, xy=0, y=0):
        if isinstance(xy, (tuple, list)):
            x, y = xy
        self.vector = (int(x), int(y))

    def __repr__(self):
        return 'IntVector: %s' % self.vector

    def as_Vector(self):
        return Vector(self.vector[0], self.vector[1])

    def length(self):
        return int(round(self._length))

class Vector(BaseVector):

    def __init__(self, xy=0, y=0):
        if isinstance(xy, (tuple, list)):
            xy, y = xy
        self.vector = (float(xy), float(y))

    def __repr__(self):
        return 'Vector: %s' % self.vector

    def as_IntVector(self):
        return IntVector(self.vector[0], self.vector[1])

    def length(self):
        return self._length()

    def quadrant(self):
        h = self.vector[0]
        v = self.vector[1]
        #q = 1
        if h < 0:
            if v >= 0:  return 2
            else:     return 3
        else:
            if v < 0:   return 4
        return 1

class Line:

    def __init__(self, d = Vector(), p = Vector() ):
        if isinstance(d, (tuple, list)):
            if isinstance(d[0], int) and isinstance(d[1], int):
                d = IntVector( d )
            else:
                d = Vector( d )
        if isinstance(p, (tuple, list)):
            if isinstance(p[0], int) and isinstance(p[1], int):
                p = IntVector( p )
            else:
                p = Vector( p )
        self.dv = d # direction vector
        self.pv = p # place vector
        self.segment = (Vector(), Vector() )

    def makeLine(self, a = Vector(), b = Vector()):
        """
        Makes line line that runs through a and b.
        """
        self.dv = b - a
        self.pv = a
        self.segment = (a, b)

    def orthogonal( self ):
        """
        Makes a line that runs orthogonal to self and through pv.
        """
        return Line( (self.dv[1], -self.dv[0]), self.pv )

    def near(self, x = None, y = None):

        if x == None or y == None:
            print("   x == None or y == None")
            return 0

        # test if aPt in inside bounding box of segment
        a1 = self.segment[0].vector[0]
        a2 = self.segment[0].vector[1]
        b1 = self.segment[1].vector[0]
        b2 = self.segment[1].vector[1]
        a1b1 = inbetween(a1, x, b1)
        a2b2 = inbetween(a2, y, b2)

        if a1b1 and a2b2:
            return 1
        else:
            return 0

    def has_intersect(self, other):
        d = determinant(self.dv, other.dv)
        if d == 0:
            return 0
        if determinant(self.dv, other.dv) != 0:
            return 1
        else:
            return 0

    def intersect(self, other):
        if determinant(self.dv, other.dv) != 0:
            return common(  self.dv.vector[0], self.dv.vector[1], self.pv.vector[0], self.pv.vector[1], \
                        other.dv.vector[0], other.dv.vector[1], other.pv.vector[0], other.pv.vector[1])
        return None

    def angle(self):
        return self.dv.angle()

    def has_point(self, x, y):
        # werkt niet
        mu = round(x / (self.dv[0] + self.pv[0]), 2)
        nu = round(y / (self.dv[1] + self.pv[1]), 2)
        if mu == nu:
            return 1
        else:
            return 0

    def __repr__(self):
        return "Line: direction " + str(self.dv) + " place " + str(self.pv) + " segment = " + str(self.segment)

class CurvePalette(Subscriber):

    controller = None

    def build(self):
        global curvePaletteController
        curvePaletteController = self

        glyphEditor = self.getGlyphEditor()

    def started(self):
        pass
            
    def destroy(self):
        pass

    def glyphEditorDidKeyDown(self, info):
        event = extractNSEvent(info['NSEvent'])
        characters = event['keyDown']
        
        commandDown = event['commandDown']
        shiftDown = event['shiftDown']
        controlDown = event['controlDown']
        optionDown = event['optionDown']
        self.capLock = event['capLockDown']

        if characters in 'Hh':
            # As if "Circle - (8, 8) was hit for [h]. Caps [H] gives less stress (7, 7)"
            self.controller.glyphEditorSelectedDefaultCurve(characters == 'H')
            
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
        
class CurvePaletteController(WindowController):

    glyphEditorSubscriberClass = CurvePalette

    debug = True

    def build(self):
        self.lastMouseGrid = None # Save the last mouse grid click
        self.lastMouse = None # Actual position of last mouse click
        self.lastMouseDrag = None # Actual position of last mouse drag
        self.selectedDragPoints = None # Storage of selected points, while dragging

        self.w = FloatingWindow((W + ML + MR, H + MT + MB), "Curve Palette")
        self.w.view = MerzView(
            (ML, MT, -MR, -MB),
            backgroundColor=(1, 1, 1, 1),
            delegate=self
        )
        # See of there is a font open that we can get preference values from.
        self.preferences = self.getPreferences(CurrentFont())
        maxGridSize = max(GRID_SIZES)
        cw = self.getCellWidth()
        
        container = self.w.view.getMerzContainer()
        self.gridDiagonals = []
        for x in range(maxGridSize):
            y = x
            self.gridDiagonals.append(container.appendRectangleSublayer(
               position=(x * cw, y * cw),
               size=(cw, cw),
               fillColor=DIAGONAL_COLOR,
            ))
            
        self.gridLinesVertical = []
        for x in range(maxGridSize):
            self.gridLinesVertical.append(container.appendLineSublayer(
               startPoint=(x * cw, 0),
               endPoint=(x * cw, H),
               strokeWidth=GRID_LINE,
               strokeColor=GRID_COLOR,
            ))
            
        self.gridLinesHorizontal = []
        for y in range(maxGridSize):
            self.gridLinesHorizontal.append(container.appendLineSublayer(
               startPoint=(0, y * cw),
               endPoint=(W, y * cw),
               strokeWidth=GRID_LINE,
               strokeColor=GRID_COLOR,
            ))
            
        self.cellRects = []
        for n in range(MAX_CELLS): # Color markers on the grid
            # Square cell markers, indicating the rounded value/button
            self.cellRects.append(container.appendRectangleSublayer(
                position=(0, 0),
                visible=False,
                size=(cw, cw),
                fillColor=INVISIBLE_BUTTON_COLOR,
            ))
        self.cellPoints = []
        for n in range(MAX_POINTS):
            self.cellPoints.append(container.appendOvalSublayer(
                position=(0, 0),
                visible=False,
                size=(POINT_SIZE, POINT_SIZE),
                fillColor=POINT_FILL_COLOR,
                strokeWidth=1,
                strokeColor=POINT_STROKE_COLOR,
            ))
        self.bestCircleCell = container.appendOvalSublayer( # Showing the cell with the best approximation of a circle
                position=(0, 0),
                visible=False,
                size=(cw, cw),
                fillColor=BEST_CIRCLE_FILL_COLOR,
                strokeColor=BEST_CIRCLE_CELL_COLOR,
                strokeWidth=2,
            )    
        self.bestSuperCircleCell = container.appendOvalSublayer( # Showing the cell with the best approximation of a circle with different algorithm
                position=(0, 0),
                visible=False,
                size=(cw, cw),
                fillColor=BEST_CIRCLE_FILL_COLOR,
                strokeColor=BEST_CIRCLE_CELL_COLOR,
                strokeWidth=2,
            )    
        self.selectionMarquee = container.appendRectangleSublayer(
                position=(0, 0),
                visible=False,
                size=(cw, cw),
                strokeColor=None,
                fillColor=MARQUEE_COLOR,
            )    
        self.w.rMinPopup = PopUpButton((ML, H + POPUP_HEIGHT, POPUP_WIDTH, POPUP_HEIGHT),
                              [str(v) for v in MIN_RANGE],
                              callback=self.updateGridCallback,
                              sizeStyle='mini')
        self.w.rMinPopup.setItem(str(self.preferences['minRange']))
        self.w.rMaxPopup = PopUpButton((-MR - POPUP_WIDTH, 0, POPUP_WIDTH, POPUP_HEIGHT),
                              [str(v) for v in MAX_RANGE],
                              callback=self.updateGridCallback,
                              sizeStyle='mini')
        self.w.rMaxPopup.setItem(str(self.preferences['maxRange']))
        self.w.gridSizePopup = PopUpButton((ML + W/2 - POPUP_WIDTH/2, 0, POPUP_WIDTH, POPUP_HEIGHT),
                              [str(v) for v in GRID_SIZES],
                              callback=self.updateGridCallback,
                              sizeStyle='mini')
        self.w.gridSizePopup.setItem(str(self.preferences['gridSize']))
        
        y = W + POPUP_HEIGHT + MT
        
        self.w.showPointsCheckBox = CheckBox((ML, y, W/3, POPUP_HEIGHT), 'Show points', value=False, 
            callback=self.updateUI, sizeStyle='small')
        #self.w.makeCircleButton = Button((W/2, y, W/3, BUTTON_HEIGHT), 'Make circle', callback=self.makeCircleCallback)
        
        self.w.open()

    def makeCircleCallback(self, sender):
        """Make the current selection of points into circle curves"""
        
    def getCellWidth(self):
        """Answer the width of a cell with the current preference settings."""
        return W / self.preferences['gridSize']
        
    def getPreferences(self, f=None):
        if f is None:
            f = CurrentFont()
        if f is None: # No open font, answer the default settings
            return copy(DEFAULT_PREFERENCES) # Make sure not to alter the default original
        if PREFERENCES_LIB not in f.lib:
            f.lib[PREFERENCES_LIB] = copy(DEFAULT_PREFERENCES)
        return f.lib[PREFERENCES_LIB]
        
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
        self.glyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.glyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        container = self.w.view.getMerzContainer()
        container.clearSublayers()
        unregisterGlyphEditorSubscriber(self.glyphEditorSubscriberClass)
        self.glyphEditorSubscriberClass.controller = None

    def getMousePosition(self, event):
        x, y = event.locationInWindow()
        return x - ML, y - MB

    def glyphEditorSelectedDefaultCurve(self, lessStress=False):
        """Key stroke inditing "Circle - (2, 2)" location hit."""
        if lessStress:
            self.updateCurves(7, 7)
        else:
            self.updateCurves(8, 8)
        self.glyphChanged()
        
    def getMouseCellPosition(self, event):
        x, y = self.getMousePosition(event)
        cw = self.getCellWidth()
        print('Cell =', int(x / cw), int(y / cw) )
        return int(x / cw), int(y / cw)
                     
    def mouseDown(self, view, event):
        self.lastMouse = self.lastMouseDrag = self.getMousePosition(event)
        cx, cy = self.getMouseCellPosition(event)        
        self.lastMouseGrid = cx, cy
        modifiers = event.modifierFlags()
        alternateDown = modifiers & NSAlternateKeyMask
        if alternateDown:
            self.unselectPoints()
        else:
            self.updateCurves(cx, cy)
            self.glyphChanged()

    def mouseDragged(self, view, event):
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask
        alternateDown = modifiers & NSAlternateKeyMask
        if alternateDown:
            if self.selectedDragPoints is None: # Not selected yet
                g = self.getCurrentGlyph()
                if g is not None:
                    _, _, self.selectedDragPoints = self.getSelectedCurvePoints(g)
            x, y = self.getMousePosition(event)
            if (x, y) != self.lastMouseDrag:
                self.selectionMarquee.setPosition((
                    min(self.lastMouse[0], self.lastMouseDrag[0]), 
                    min(self.lastMouse[1], self.lastMouseDrag[1])
                ))
                self.selectionMarquee.setSize((
                    self.lastMouseDrag[0] - self.lastMouse[0], 
                    self.lastMouseDrag[1] - self.lastMouse[1]
                ))
                self.lastMouseDrag = (x, y)
        #else:
        #    cx, cy = self.getMouseCellPosition(event)
        #    if (cx, cy) != self.lastMouseGrid:
        #        self.lastMouseGrid = cx, cy
        #        self.updateCurves(cx, cy)
        #        self.glyphChanged()

    def mouseUp(self, view, event):
        #print(self.lastMouseDrag, self.selectedDragPoints)
        if self.lastMouseDrag is not None and self.selectedDragPoints is not None:
            # Finishing drag: select the points in the marquee
            marqueeX1 = min(self.lastMouseDrag[0], self.lastMouse[0])
            marqueeY1 = min(self.lastMouseDrag[1], self.lastMouse[1])
            marqueeX2 = max(self.lastMouseDrag[0], self.lastMouse[0])
            marqueeY2 = max(self.lastMouseDrag[1], self.lastMouse[1])

            rMin = self.preferences['minRange']/100
            rMax = self.preferences['maxRange']/100
            r = rMax - rMin

            modifiers = event.modifierFlags()
            shiftDown = modifiers & NSShiftKeyMask
            #alternateDown = modifiers & NSAlternateKeyMask
            #commandDown = modifiers & NSCommandKeyMask
            #controlDown = modifiers & NSControlKeyMask
            for segmentTensions in self.selectedDragPoints.values():
                for points, tx, ty in segmentTensions: 
                    x = (tx - rMin) / r * W - POINT_SIZE/2
                    y = (ty - rMin) / r * H - POINT_SIZE/2
                    for p in (points[0], points[-1]):
                        if marqueeX1 <= x <= marqueeX2 and marqueeY1 <= y <= marqueeY2:
                            if shiftDown:
                                p.selected = not p.selected
                            else:
                                p.selected = True
                        elif not shiftDown:
                            p.selected = False

        self.lastMouseDrag = self.selectedDragPoints = None # No longer marquee operating
        self.selectionMarquee.setPosition((0, 0))
        self.selectionMarquee.setVisible(False)

    def glyphEditorDidSetGlyph(self, info):
        # Passed this on from the subscriber. How to do this better?
        g = info['glyph']
        #print('### glyphEditorDidSetGlyph')
        self.update(g)

    def glyphEditorDidMouseDrag(self, info):
        # Passed this on from the subscriber. How to do this better?
        g = info['glyph']
        self.update(g)

    def glyphEditorDidMouseDown(self, info):
        # Passed this on from the subscriber. How to do this better?
        g = info['glyph']
        self.update(g)

    def glyphEditorDidMouseUp(self, info):
        # Passed this on from the subscriber. How to do this better?
        g = info['glyph']
        self.update(g)

    def glyphEditorGlyphDidChangeSelection(self, info):
        # Passed this on from the subscriber. How to do this better?
        g = info['glyph']
        self.update(g)

    #   C U R V E S
    
    def updateCurves(self, cx, cy):
        g = self.getCurrentGlyph()
        if g is not None:
            selected, _, _ = self.getSelectedCurvePoints(g)
            # Reverse direction of the y-axis.
            # Double short BCP is bottom-left and double long BCP is top-right
            g.prepareUndo()
            self.adjustPoints(g, cx, cy) # Does not update the glyph yet.

    def adjustPoints(self, g, vx, vy):
        # ----------------------------------------------------------------------------------
        #   Adjust the position of the BCP's from the selected points.
        #   Note that BCP's are only touched if they they have a different position from
        #   their curve points.
        #   If doSelect is True, then just select the points that fit the intended value.
        #...................................................................................

        rMin = self.preferences['minRange']/100
        rMax = self.preferences['maxRange']/100
        cw = self.getCellWidth()
        # Get the interpolation values from the dialog for the two quadrants
        vx = rMin + vx * cw * (rMax - rMin) / W
        vy = rMin + vy * cw * (rMax - rMin) / H
        smoothPoints = [] # Keep the index of smooth points, to set their status back.
        for contour in g:
            points = list(contour.points)
            if points: # Any points here?
                if len(points) < 4:
                    continue
                points2 = points + points # Double, so we can run over he edge.
            
                for index in range(len(points)):
                    p0, p1, p2, p3 = points2[index:index+4]
                    #nextnextp = self.nextp(bPoints, index + 1)
                    #prevp = self.prevp(bPoints, index)
                    if p1.type != 'offcurve' or p2.type != 'offcurve': # Not a curve
                        continue
                    if not p0.selected or not p3.selected:
                        continue
                    if p0.smooth: # Remember the smoothness, to put it back. It may disable in the process
                        smoothPoints.append(p0)
                    if p3.type in ('qcurve', 'curve'): # Double check if quadratic curve or Bezier      
                        self.adjustBCP(p0, p1, p2, p3, vx, vy)
                    else:
                        print('Unknown curve type', p3.type)
                        
        for p in smoothPoints:
            p.smooth = True

    def adjustBCP( self, p0, p1, p2, p3, svx, svy):
        """Adjust the BCP lengths of the point to the intended vector length.
        If doSelect is True, then just select the points that (closely) fit the new length.
        In that case the position of the BCP points is not changed.
        """
        intersection = Line( (p1.x, p1.y), (p0.x, p0.y) ).intersect( Line( (p2.x, p2.y), (p3.x, p3.y) ))
        if intersection is not None:
            ix, iy = intersection
            if ix is not None and iy is not None:

                p1.x = int(round(p0.x + svx * (ix - p0.x)))
                p1.y = int(round(p0.y + svy * (iy - p0.y)))
                p2.x = int(round(p3.x + svx * (ix - p3.x)))
                p2.y = int(round(p3.y + svy * (iy - p3.y)))


    #   G R I D  M A R K E R S
    
    def _getRelativeVectorLength(self, p1, p2, p3):
        """

           |-------------|--------|-----------|------------------|---------|----------|
           0%             t1       p1          p2                 p3        t2        100%

        Calculate the relative length of p1-->p2 in relation to p3, scale the percentage.
        Also take the t1 and t2 slider values into account, which define the cropped grid 
        in relation to 0-100%
        """
        p1x, p1y = p1
        p2x, p2y = p2
        p3x, p3y = p3
        v1 = Vector(p2x - p1x, p2y - p1y)
        v2 = Vector(p3x - p1x, p3y - p1y)
        #return (t2 - t1) / v2.length() * v1.length()
        v2Length = v2.length()
        if v2Length == 0:
            return None
        return v1.length() / v2Length

    def getCurveTension(self, p1, bcp1, bcp2, p2):
        # Figure out where the intersection of the BCP's is, relative to p1
        ix = iy = None
        x = y = presetx = presety = None
        intersection = Line( p1, bcp1).intersect( Line( p2, bcp2)  )
        if intersection is not None:
            ix, iy = intersection
        
        if ix is not None and iy is not None:
            
            presetx = self._getRelativeVectorLength(p1, bcp1, intersection)
            presety = self._getRelativeVectorLength(p2, bcp2, intersection)

            if presetx is not None and presety is not None:

                # As we know the intersection of the off-curve vectors now, we can calculate the percentage
                # of the onCurve-offCurve vectors. Taking the values of the sliders, this leads to a
                # x/y coordinates that will be used to highlite the buttons.
                rMin = self.preferences['minRange']/100
                rMax = self.preferences['maxRange']/100

                # For now set button from the rounded preset value that we have.
                # Later this will change in an interface on the editor window with
                # gridded area that shows that range/area of the selection without rounding.
                # The mouse then can snap to a x/y position and the curves can show live
                # when the mouse is moved over the palette.
                rDiff = rMax - rMin
                if rDiff: # Test on division by 0:
                    paletSize = self.preferences['gridSize']
                    x = max(0, min(paletSize, int(((presetx - rMin) * paletSize)/rDiff)))
                    y = max(0, min(paletSize, int(((presety - rMin) * paletSize)/rDiff)))
        return x, y, presetx, presety
         
    #   P O I N T S

    def unselectPoints(self, g=None):
        if g is None:
            g = self.getCurrentGlyph()
        if g is not None:
            for contour in g.contours:
                for p in contour.points:
                    p.selected = False
                    
    def getSelectedCurvePoints(self, g):
        """Answer a tuple of 3 dictionaries of points that are selected/unselected in the glyph.
        """
        selected = {}
        unselected = {}
        allCurvePoints = {} # Combination of selected and unselected
        for contour in g:
            points = contour.points
            if len(points) < 4:
                continue
            for pIndex in range(len(contour.points)):
                p_2 = points[pIndex - 3]
                p_1 = points[pIndex - 2]
                p = points[pIndex - 1]
                p1 = points[pIndex]
                segment = p_2, p_1, p, p1
                if p_1.type == 'offcurve' and p.type == 'offcurve':
                    cx, cy, tx, ty = self.getCurveTension((p_2.x, p_2.y), (p_1.x, p_1.y), (p.x, p.y), (p1.x, p1.y))
                    d = segment, tx, ty # Store all for later use, showing actual tension scatter per point
                    if p_2.selected or p_1.selected or p.selected or p1.selected:
                        if not (cx, cy) in selected:
                            selected[(cx, cy)] = [d]
                        else:
                            selected[(cx, cy)].append(d)
                    else:
                        if not (cx, cy) in unselected:
                            unselected[(cx, cy)] = [d]
                        else:
                            unselected[(cx, cy)].append(d)
                    # Also collect them all in points
                    if not (cx, cy) in allCurvePoints: 
                        allCurvePoints[(cx, cy)] = [d]
                    else:
                        allCurvePoints[(cx, cy)].append(d)
                        
        return selected, unselected, allCurvePoints

    #    U P D A T E  W I N D O W
    
    def getCurrentGlyph(self):
        return CurrentGlyph()
    
    def glyphChanged(self):
        g = self.getCurrentGlyph()
        if g is not None:
            g.changed()
                
    def updateGridCallback(self, sender=None):
        self.preferences['minRange'] = int(self.w.rMinPopup.getItem())
        self.preferences['maxRange'] = int(self.w.rMaxPopup.getItem())
        self.preferences['gridSize'] = int(self.w.gridSizePopup.getItem())
        f = CurrentFont()
        if f is not None:
            f.lib[PREFERENCES_LIB] = self.preferences
        self.updateGrid()
                
    def updateGrid(self):
        """One of the grid preferences got changed. Update the positions of the gridlines
        and the size of the selection boxes."""
        cw = self.getCellWidth()
        for x, line in enumerate(self.gridLinesVertical):
            px = x * cw
            line.setVisible(x < self.preferences['gridSize'])
            line.setStartPoint((px, 0))
            line.setEndPoint((px, H))
        
        for y, line in enumerate(self.gridLinesHorizontal):
            py = y * cw
            line.setVisible(y < self.preferences['gridSize'])
            line.setStartPoint((0, py))
            line.setEndPoint((W, py))

        for xy, gridDiagonal in enumerate(self.gridDiagonals):
            p = xy * cw
            line.setVisible(xy < self.preferences['gridSize'])
            gridDiagonal.setPosition((p, p))
            gridDiagonal.setSize((cw, cw))
            
        for cellRect in self.cellRects:
            cellRect.setSize((cw, cw))
                        
        for cellPoint in self.cellPoints:
            cellPoint.setSize((POINT_SIZE, POINT_SIZE))
        
        g = self.getCurrentGlyph()    
        if g is not None:
            self.update(g)

    def updateUI(self, sender):
        g = self.getCurrentGlyph()    
        if g is not None:
            self.update(g)
        
    def update(self, g):
        #self.getTensions(g)
        selected, unselected, _ = self.getSelectedCurvePoints(g)
        cellIndex = pointIndex = 0
        cw = self.getCellWidth()
        rMin = self.preferences['minRange']/100
        rMax = self.preferences['maxRange']/100
        r = rMax - rMin
        for points, c in (selected, ALL_SELECTED_COLOR), (unselected, UNSELECTED_COLOR):
            for (cx, cy), tensions in points.items():
                if None in (cx, cy):
                    continue
                cell = self.cellRects[cellIndex]
                cell.setPosition((cx * cw, cy * cw))
                if (cx, cy) in selected and (cx, cy) in unselected:
                    c = PART_SELECTED_COLOR
                cell.setFillColor(c)
                cell.setVisible(True)
                cellIndex += 1
                
                originX = originY = cw/2 - POINT_SIZE/2
                topX = topY = W - cw/2 - POINT_SIZE/2
                if self.w.showPointsCheckBox.get():
                    for segment, tx, ty in tensions:
                        tensionPoint = self.cellPoints[pointIndex]
                        tensionPoint.setPosition((((tx - rMin) / r * W - POINT_SIZE/2, (ty - rMin) / r * H - POINT_SIZE/2)))
                        if segment[0].selected:
                            w = 3
                        else:
                            w = 1
                        tensionPoint.setStrokeWidth(w)
                        tensionPoint.setVisible(True)
                        pointIndex += 1

        for n in range(cellIndex, len(self.cellRects)):
            self.cellRects[n].setVisible(False)
                    
        for n in range(pointIndex, len(self.cellPoints)):
            self.cellPoints[n].setVisible(False)

        # Set the position of the best circles marker
        c = ((4/3) * (math.tan(math.pi/8)) - rMin) / r # 0.5522847498 or more common approximation 4/3 * (math.sqrt(2) - 1)
        self.bestCircleCell.setPosition((c * W, c * H))
        self.bestCircleCell.setSize((cw*1.5, cw*1.5))
        self.bestCircleCell.setVisible(True)
        # Both formulas seem to be equally accurate
        #c = ((4/3) * (math.sqrt(2) - 1) - rMin) / r # More common approximation 4/3 * (math.sqrt(2) - 1)
        #self.bestSuperCircleCell.setPosition((c * W, c * H))
        #self.bestSuperCircleCell.setSize((cw*1.5, cw*1.5))
        #self.bestSuperCircleCell.setVisible(True)
                    
if __name__ == '__main__':
    OpenWindow(CurvePaletteController)
