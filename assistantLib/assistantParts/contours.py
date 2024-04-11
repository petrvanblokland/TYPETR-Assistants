# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   contours.py
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
from assistantLib.assistantParts.glyphsets.anchorData import AD


class AssistantPartContours(BaseAssistantPart):
    """Set startpoint and other contour functions
    """

    def initMerzContours(self, container):
        """Initialize the Merz instances for this assistant part.""" 

    def updateContours(self, info):
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed
        return self.checkFixContours(g)

    def checkFixContours(self, g):
        changed = False
        # ...
        return changed

    def buildContours(self, y):
        personalKey_e = self.registerKeyStroke('e', 'contoursSetStartPoint')
        personalKey_E = self.registerKeyStroke('E', 'contoursSetAllStartPoints')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.setStartPointButton = Button((C2, y, CW, L), f'Set start [{personalKey_E}{personalKey_e}]', callback=self.contoursSetStartPointCallback)
        y += L + L/5
        c.w.contoursEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.contoursEndLine2 = HorizontalLine((self.M, y, -self.M, 1)) # Double for slightly darker line
        y += L/5

        return y

    #    C O N T O U R S

    def contoursSetStartPointCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.contoursSetStartPoint(g)

    def contoursSetAllStartPoints(self, g, c=None, event=None):
        for f in self.getAllFonts():
            if g.name in f:
                self.contoursSetStartPoint(f[g.name])

    def contoursSetStartPoint(self, g, c=None, event=None):
        """Set the start point to the selected points on [e]. Auto select the point on [E] key."""
        changed = False
        doSelect = True
        doAuto = c is None or c != c.upper() # Auto select if lowercase of key was used
        selectedContours = []
        autoContours = []
        openContours = []

        g.prepareUndo()
        for cIndex, contour in enumerate(g.contours):
            selected = auto = x = y = None
            points = contour.points
            numPoints = len(points)
            if contour.open: # Just select between the start and end point
                openContours.append((cIndex, contour))
            else:
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

        if openContours:
            for cIndex, contour in openContours:
                p0 = contour.points[0]
                p1 = contour.points[-1]
                if p0.y > p1.y or (p0.y == p1.y and p0.x > p1.x):
                    print(f'... Altering startpoint of open contour {cIndex}')
                    contour.reverse()
                    changed = True

        if doAuto: # Find the best match, ignoring any selections
            #print('... %s: Auto start for %d contours' % (glyph.name, len(autoContours)))
            for pIndex, contour in autoContours:
                if pIndex:
                    # Make x show same as angled value in EditorWindow
                    x = contour.points[pIndex].x - int(round((tan(radians(-g.font.info.italicAngle or 0)) * contour.points[pIndex].y)))
                    print(f'... Altering startpoint to {(x, contour.points[pIndex].y)}')
                    contour.naked().setStartPoint(pIndex)
                    changed = True

        elif doSelect and selectedContours: # Uppercase key stroke: only do the selected points
            #print('... %s: Set start for %d contours' % (glyph.name, len(selectedContours)))
            for pIndex, contour in selectedContours:
                contour.naked().setStartPoint(pIndex)
                changed = True

        if changed:
            g.changed()

