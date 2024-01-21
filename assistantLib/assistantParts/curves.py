# -*- coding: UTF-8 -*-

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

from mojo.roboFont import CurrentGlyph

import assistantLib.toolbox.qbqconverter
importlib.reload(assistantLib.toolbox.qbqconverter)
from assistantLib.toolbox.qbqconverter import *
from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

POINTTYPE_BEZIER = 'curve'
POINTTYPE_QUADRATIC = 'qcurve'
POINTTYPE_OFFCURVE = 'offcurve'

FACTOR = 1.340   # This estimated value gives amazingly accurate conversion.

class AssistantPartCurves(BaseAssistantPart):
    """The Curves assistant part converts between Quadratics and Bezier.
    """
    def initMerzCurves(self, container):
        self.registerKeyStroke('q', 'curvesB2QGlyphKey')
        self.registerKeyStroke('b', 'curvesQ2BGlyphKey')

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
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
        c = self.getController()
        c.w.Q2BButton = Button((C1, y, CW, L), 'Q --> B', callback=self.Q2BCallback)
        c.w.B2QButton = Button((C2, y, CW, L), 'B --> Q', callback=self.B2QCallback)
        y += L + LL

        return y

    #    Q U A D R A T I C --> B E Z I E R

    def Q2BCallback(self, sender):
        """Callback from button"""
        g = CurrentGlyph()
        if g is not None:
            self.curvesConvert(g, POINTTYPE_QUADRATIC, POINTTYPE_BEZIER, FACTOR)

    def curvesB2QGlyphKey(self, g, c, event):
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
        g = CurrentGlyph()
        if g is not None:
            self.curvesConvert(g, POINTTYPE_BEZIER, POINTTYPE_QUADRATIC, 1/FACTOR)

    def curvesQ2BGlyphKey(self, g, c, event):
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

    def isQuadratic(self, g):
        for contour in g.contours:
            for p in contour.points:
                if p.type == POINTTYPE_QUADRATIC:
                    return True
        return False

    def isBezier(self, g):
        for contour in g.contours:
            for p in contour.points:
                if p.type == POINTTYPE_BEZIER:
                    return True
        return False

