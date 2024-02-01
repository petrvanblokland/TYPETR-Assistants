# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   curves.py
#
import sys
from math import *
from vanilla import *
import importlib

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

FACTOR = 1.340   # This estimated value gives amazingly accurate conversion.

class AssistantPartCurves(BaseAssistantPart):
    """The Curves assistant part converts between Quadratics and Bezier.
    """
    def initMerzCurves(self, container):
        pass

    def updateCurves(self, info):
        c = self.getController()
        g = info['glyph']
        q2bEnable = b2qEnable = False
        if g is not None:
            if self.isQuadratic(g):
                q2bEnable = True
                b2qEnable = False
            elif self.isBezier(g):
                q2bEnable = False
                b2qEnable = True
        c.w.Q2BButton.enable(q2bEnable)
        c.w.B2QButton.enable(b2qEnable)

    def buildCurves(self, y):

        personalKey_q = self.registerKeyStroke('q', 'curvesB2QGlyphKey')
        personalKey_b = self.registerKeyStroke('b', 'curvesQ2BGlyphKey')
        personalKey_E = self.registerKeyStroke('E', 'curvesSetStartPoint') # Choose selected point as start point
        personalKey_e = self.registerKeyStroke('e', 'curvesSetStartPoint') # Auto selection of start points on best match

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
        c = self.getController()
        c.w.setStartPointButton = Button((C0, y, CW, L), 'Set start [%s]' % personalKey_e, callback=self.curvesSetStartPointCallback)
        c.w.Q2BButton = Button((C1, y, CW, L), 'Q --> B [%s]' % personalKey_b, callback=self.Q2BCallback)
        c.w.B2QButton = Button((C2, y, CW, L), 'B --> Q [%s]' % personalKey_q, callback=self.B2QCallback)
        y += L + LL

        return y

    #    Q U A D R A T I C --> B E Z I E R

    def Q2BCallback(self, sender):
        """Callback from button"""
        g = self.currentGlyph()
        if g is not None:
            self.curvesConvert(g, POINTTYPE_QUADRATIC, POINTTYPE_BEZIER, FACTOR)

    def curvesQ2BGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']
        
        self.curvesConvert(g, POINTTYPE_QUADRATIC, POINTTYPE_BEZIER, FACTOR)

    #    B E Z I E R --> Q U A D R A T I C
        
    def B2QCallback(self, sender):
        """Callback from button"""
        g = self.currentGlyph()
        if g is not None:
            self.curvesConvert(g, POINTTYPE_BEZIER, POINTTYPE_QUADRATIC, 1/FACTOR)

    def curvesB2QGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']

        self.curvesConvert(g, POINTTYPE_BEZIER, POINTTYPE_QUADRATIC, 1/FACTOR)

    def factorizeOffCurve(self, onCurve, offCurve, factor):
        dx = offCurve.x - onCurve.x
        dy = offCurve.y - onCurve.y
        offCurve.x = int(round(onCurve.x + dx * factor))
        offCurve.y = int(round(onCurve.y + dy * factor))

    def curvesConvert(self, g, fromType, toType, factor):
        # Make sure to unselect all points
        for contour in g.contours:
            points = contour.points
            for n in range(len(points)):
                p_0, p_1, p_2, p_3 = points[n], points[n-1], points[n-2], points[n-3]
                if p_0.type == fromType:
                    p_0.type = toType
                    if p_1.type == POINTTYPE_OFFCURVE:
                        self.factorizeOffCurve(p_0, p_1, factor)
                    if p_2.type == POINTTYPE_OFFCURVE:
                        self.factorizeOffCurve(p_3, p_2, factor)
            for p in contour.points:
                p.selected = False
        g.changed()

    #    C O N T O U R S

    def curvesSetStartPointCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.curvesSetStartPoint(g)

    def curvesSetStartPoint(self, g, c=None, event=None):
        """Set the start point to the selected points on [e]. Auto select the point on [E] key."""
        doSelect = True
        doAuto = c != c.upper() # Auto select if lowercase of key was used:
        selectedContours = []
        autoContours = []
        g.prepareUndo()
        for contour in g.contours:
            selected = auto = x = y = None
            points = contour.points
            numPoints = len(points)
            for pIndex, point in enumerate(points):
                if point.type == 'offcurve':
                    continue
                if point.selected:
                    selected = pIndex
                if auto is None or x is None or y is None or point.y < y or (point.y == y and point.x < x):
                    auto = pIndex
                    x = point.x
                    y = point.y
            if selected:
                selectedContours.append((selected, contour))
            if auto:
                autoContours.append((auto, contour))
    
        if doAuto: # Find the best match, ignoring any selections
            changed = False
            #print('... %s: Auto start for %d contours' % (glyph.name, len(autoContours)))
            for pIndex, contour in autoContours:
                if pIndex:
                    # Make x show same as angled value in EditorWindow
                    x = contour.points[pIndex].x - int(round((tan(radians(-g.font.info.italicAngle or 0)) * contour.points[pIndex].y)))
                    print(f'... Altering startpoint to {(x, contour.points[pIndex].y)}')
                    contour.naked().setStartPoint(pIndex)
                    changed = True
            if changed:
                g.changed()
        elif doSelect and selectedContours: # Uppercase key stroke: only do the selected points
            #print('... %s: Set start for %d contours' % (glyph.name, len(selectedContours)))
            for pIndex, contour in selectedContours:
                contour.naked().setStartPoint(pIndex)
            g.changed()

