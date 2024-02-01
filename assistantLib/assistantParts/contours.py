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

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR


class AssistantPartContours(BaseAssistantPart):
    """Set startpoint and other contour functions
    """
    def initMerzContours(self, container):
        pass

    def updateContours(self, info):
        c = self.getController()
        g = info['glyph']

    def buildContours(self, y):

        personalKey_E = self.registerKeyStroke('E', 'curvesSetStartPoint') # Choose selected point as start point
        personalKey_e = self.registerKeyStroke('e', 'curvesSetStartPoint') # Auto selection of start points on best match

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.setStartPointButton = Button((C2, y, CW, L), 'Set start [%s]' % personalKey_e, callback=self.curvesSetStartPointCallback)
        y += L

        return y

    #    C O N T O U R S

    def curvesSetStartPointCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.curvesSetStartPoint(g)

    def curvesSetStartPoint(self, g, c=None, event=None):
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
                print('Open contour', cIndex)
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

