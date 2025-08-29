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
        gName = g.name
        f = g.font
        c = self.getController()
        if c.w.autoCopyContourFromSrc.get():
            g = self.getCurrentGlyph()
            gd = self.getGlyphData(g)
            if gd is not None and gd.srcName:
                if gd.srcName not in f:
                    print(f'### Source glyph /{gd.srcName} for /{gName} does not exist')
                else:
                    srcG = f[gd.srcName]
                    if not g.contours and not g.components:
                        f[gName] = srcG
                        f[gName].decompose()
                        changed = True
        return changed

    def buildContours(self, y):
        personalKey_e = self.registerKeyStroke('e', 'contoursSetStartPoint')
        personalKey_E = self.registerKeyStroke('E', 'contoursSetAllStartPoints')
        personalKey_plusminus = self.registerKeyStroke('±', 'contoursAddCorners')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.autoCopyContourFromSrc = CheckBox((C0, y, CW, L), f'Auto copy from source', value=True)
        c.w.setStartPointForAllGlyphs = CheckBox((C1, y, CW, L), f'All glyphs', value=False)
        c.w.setStartPointButton = Button((C2, y, CW, L), f'Set start [{personalKey_E}{personalKey_e}]', callback=self.contoursSetStartPointCallback)
        y += L + L/5
        c.w.contoursEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.contoursEndLine2 = HorizontalLine((self.M, y, -self.M, 1)) # Double for slightly darker line
        y += L/5

        return y

    #    C O N T O U R S

    def contoursSetStartPointCallback(self, sender):
        g = self.getCurrentGlyph()
        c = self.getController()
        if c.w.setStartPointForAllGlyphs.get():
            glyphs = self.getCurrentFont()
        elif g is not None:
            glyphs = [g]
        else:
            glyphs = []
        for g in glyphs:
            self.contoursSetStartPoint(g)

    def contoursSetAllStartPoints(self, g, c=None, event=None):
        for f in self.getAllOpenFonts():
            if g.name in f:
                self.contoursSetStartPoint(f[g.name])

    def contoursAddCorners(self, g, c=None, even=None):
        g.prepareUndo("Insert corners")

        contours = []
        for contour in g.contours:
            c = []
            contours.append(c)
            for p in contour.points:
                c.append((round(p.x), round(p.y), p.type, p.smooth))

        if 'Hairline' in g.font.path:
            t = 1
        else:
            t = 4
            
        g.clearContours()
        pen = g.getPen()
        for contour in contours:
            offCurve1 = None
            offCurve2 = None
            prevCurvex = prevCurvey = None
            for pIndex in range(len(contour)):
                p_1x, p_1y, _, _ = contour[pIndex-2]
                p0x, p0y, type, smooth = contour[pIndex-1]
                p1x, p1y, _, _ = contour[pIndex]

                print(pIndex, offCurve1, offCurve2, (p0x, p0y), prevCurvex, prevCurvey)
                
                if pIndex == 0:
                     pen.moveTo((p0x, p0y))
                elif type == 'line':
                    if p_1x == p0x and p_1y > p0y and p0y == p1y and p0x < p1x:
                        # Bottom up left
                        pen.lineTo((p0x, p0y + t))
                        pen.lineTo((p0x + t, p0y))
                    elif p_1x > p0x and p_1y == p0y and p0y > p1y and p0x == p1x:
                        # Top down left
                        print(pIndex)
                        pen.lineTo((p0x + t, p0y))
                        pen.lineTo((p0x, p0y - t))
                    elif p_1x == p0x and p_1y < p0y and p1x < p0x and p1y == p0y:
                        # Top down right
                        pen.lineTo((p0x, p0y - t))
                        pen.lineTo((p0x - t, p0y))
                    elif p_1x < p0x and p_1y == p0y and p0x == p1x and p0y < p1y:
                        # Bottom up right
                        pen.lineTo((p0x - t, p0y))
                        pen.lineTo((p0x, p0y + t))
                    else:
                        pen.lineTo((p0x, p0y))
                    
                elif type == 'offcurve':
                    if offCurve1 is None:
                        offCurve1 = (p0x, p0y)
                        prevCurvex = p_1x
                        prevCurvey = p_1y
                    elif offCurve2 is None:
                        offCurve2 = (p0x, p0y)
                    
                elif type == 'curve':
                    if abs(prevCurvex - p0x) <= 4 and abs(prevCurvey - p0y) <= 4:
                        pen.lineTo((prevCurvex, prevCurvey))
                        pen.lineTo((p0x, p0y))
                    else:
                        if offCurve1 is None:
                            continue
                        if offCurve2 is None:
                            continue
                        pen.curveTo(offCurve1, offCurve2, (p0x, p0y))
                    offCurve1 = offCurve2 = prevCurvex = prevCurvey = None
                
            pen.closePath()
            

        self.contoursSetStartPoint(g) # Always reset start points
        g.changed()

    def fixDirections(self, g):
        if 'O' in g.font:
            refG = g.font['O'] # Use this glyph as reference to check on the type of curves.
            g.correctDirection(trueType=not self.isBezier(refG))

    def contoursSetStartPoint(self, g, c=None, event=None):
        """Set the start point to the selected points on [e]. Auto select the point on [E] key.
        If the [x] Do all fonts is checked, then do all fonts,"""
        changed = False
        doSelect = True
        doAuto = c is None or c != c.upper() # Auto select if lowercase of key was used
        selectedContours = []
        autoContours = []
        openContours = []

        g.prepareUndo()

        # Correct the directions of the glyph to PostScript standard.
        # Direction is counter-clockwise, the arrow is on the black area.
        self.fixDirections(g)

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
                    x = contour.points[pIndex].x - int(round((tan(radians(-(g.font.info.italicAngle or 0))) * contour.points[pIndex].y)))
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

