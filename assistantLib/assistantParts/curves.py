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

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart

FACTOR = 1.340   # This estimated value gives amazingly accurate conversion.

class AssistantPartCurves(BaseAssistantPart):
    """The Curves assistant part converts between Quadratics and Bezier.
    """
    def initMerzCurves(self, container):
        pass

    def updateCurves(self, info):
        c = self.getController()
        if c is None: # Window could just have been closed.
            return False
            
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
        return False # Nothing changed to the glyph
        
    def buildCurves(self, y):

        personalKey_q = self.registerKeyStroke('q', 'curvesB2QGlyphKey')
        personalKey_b = self.registerKeyStroke('b', 'curvesQ2BGlyphKey')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.Q2BButton = Button((C1, y, CW, L), f'Q --> B [{personalKey_b}]', callback=self.Q2BCallback)
        c.w.B2QButton = Button((C2, y, CW, L), f'B --> Q [{personalKey_q}]', callback=self.B2QCallback)
        y += L + L/5
        c.w.curvesEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.curvesEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5

        return y

    #    Q U A D R A T I C --> B E Z I E R

    def Q2BCallback(self, sender):
        """Callback from button"""
        g = self.getCurrentGlyph()
        if g is not None:
            self.curvesConvert(g, self.POINTTYPE_QUADRATIC, self.POINTTYPE_BEZIER, FACTOR)

    def curvesQ2BGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']
        
        self.curvesConvert(g, self.POINTTYPE_QUADRATIC, self.POINTTYPE_BEZIER, FACTOR)

    #    B E Z I E R --> Q U A D R A T I C
        
    def B2QCallback(self, sender):
        """Callback from button"""
        g = self.getCurrentGlyph()
        if g is not None:
            self.curvesConvert(g, self.POINTTYPE_BEZIER, self.POINTTYPE_QUADRATIC, 1/FACTOR)

    def curvesB2QGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']

        self.curvesConvert(g, self.POINTTYPE_BEZIER, self.POINTTYPE_QUADRATIC, 1/FACTOR)

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
                    if p_1.type == self.POINTTYPE_OFFCURVE:
                        self.factorizeOffCurve(p_0, p_1, factor)
                    if p_2.type == self.POINTTYPE_OFFCURVE:
                        self.factorizeOffCurve(p_3, p_2, factor)
            for p in contour.points:
                p.selected = False
        g.changed()

