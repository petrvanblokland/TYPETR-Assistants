# -*- coding: UTF-8 -*-

import sys
from math import *
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from fontTools.misc.transform import Transform
from mojo.roboFont import OpenWindow, CurrentGlyph, CurrentFont, OpenFont, AllFonts, RGlyph, RPoint

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

class AssistantPartItalicize(BaseAssistantPart):
    """The Italicize assistant part italicizes the current glyph in RoboFont.
    """

    def initMerzItalicize(self, container):
        """Register key stroke cap-I. [i] is reserved for the spacing part"""
        self.registerKeyStroke('I', 'italicizeGlyphKey')

    def updateItalicize(self, info):
        g = info['glyph']
        if g.components or g.contours: # Not empty, do nothing
            return
        # Glyph is empty (by italicizeCallback or manually by user
        self.italicizeGlyph(g)

    def buildItalicize(self, y):
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        self.w.addItalicizedComponents = CheckBox((C0, y, CW, L), 'Add components', value=True, sizeStyle='small')
        self.w.skipItalicizedComponents = CheckBox((C1, y, CW, L), 'Skip components', value=True, sizeStyle='small')
        self.w.addItalicizedExtremes = CheckBox((C0, y+LL, CW, L), 'Add extremes', value=True, sizeStyle='small')
        self.w.skewRotate = CheckBox((C1, y+LL, CW, L), 'Skew & rotate', value=False, sizeStyle='small')

        self.w.italicizeButton = Button((C2, y+LL/2, CW, L), 'Italicize', callback=self.italicizeCallback)
        y += L + LL

        return y

    def italicizeCallback(self, sender):
        g = CurrentGlyph()
        g.clear() 
        g.changed() # Force update. UpdateItalize will then rebuild the glyph.

    def italicizeGlyphKey(self, g, c, event):
        """Callback for registered event on key stroke"""

        # Current we don't need any of these modifiers
        # commandDown = event['commandDown']
        # shiftDown = event['shiftDown']
        # controlDown = event['controlDown']
        # optionDown = event['optionDown']
        # capLock = event['capLockDown']
        
        self.italicizeGlyph(g)

    # Function mostly copied from the Slanter extension
    def italicizeGlyph(self, g):
        f = g.font
        md = self.getMasterData(f)
        gd = self.getGlyphData(f, g.name)
        gName = g.name
        c = self.getController()

        if not md.isItalic:
            print(f'### Glyph {md.name}/{g.name} is not italic.')
            return

        g.prepareUndo()

        addComponents = c.w.addItalicizedComponents.get()
        skipComponents = c.w.skipItalicizedComponents.get()
        addExtremes = c.w.addItalicizedExtremes.get()

        srcF = self.getFont(md.romanItalicUFOPath)
        if srcF is None:
            print(f'### Cannot find italic source {md.romanItalicUFOPath}.')
            return
        if gName not in srcF:
            print(f'### Italic source glyph {gName} does not exist.')
            return

        srcG = srcF[gName]

        # Glyphs like /O better use skew+rotate to italicize, just look at the checkbox, not at the GLYPH_DATA flags.
        # self.isCurved is inherited from the italicize Assistant part
        print('4322423', c.w.skewRotate.get(), self.isCurved(srcG))
        if c.w.skewRotate.get() and self.isCurved(srcG): 
            print(f'... Using Skew ({md.italicSkew}) & Rotate ({md.italicRotation})')
            skew = radians(-md.italicSkew)
            rotation = radians(md.italicRotation)
        else:
            skew = radians(-md.italicAngle)
            rotation = 0

        print(f'... Italicize: Skew {skew } & Rotate {rotation}', )    
        
        f[gName] = srcG # Copy from roman
        dstG = f[gName]
        
        if not addComponents:
            for component in dstG.components:
                pointPen = DecomposePointPen(srcG.layer, dest.getPointPen(), component.transformation)
                component.drawPoints(pointPen)
                dest.removeComponent(component)

        for contour in list(dstG.contours):
            if contour.open:
                dstG.removeContour(contour)

        if skew == 0 and rotation == 0:
            return

        for contour in dstG:
            for bPoint in contour.bPoints:
                bcpIn = bPoint.bcpIn
                bcpOut = bPoint.bcpOut
                if bcpIn == (0, 0):
                    continue
                if bcpOut == (0, 0):
                    continue
                if bcpIn[0] == bcpOut[0] and bcpIn[1] != bcpOut[1]:
                    bPoint.anchorLabels = ["extremePoint"]
                if rotation and bcpIn[0] != bcpOut[0] and bcpIn[1] == bcpOut[1]:
                    bPoint.anchorLabels = ["extremePoint"]

        cx, cy = 0, 0
        box = srcG.bounds
        if box:
            cx = box[0] + (box[2] - box[0]) * .5
            cy = box[1] + (box[3] - box[1]) * .5

        t = Transform()
        t = t.skew(skew)
        t = t.translate(cx, cy).rotate(rotation).translate(-cx, -cy)

        if not skipComponents:
            dstG.transformBy(tuple(t))
        else:
            for contour in dstG.contours:
                contour.transformBy(tuple(t))

            # this seems to work !!!
            for component in dstG.components:
                # get component center
                _box = srcG.layer[component.baseGlyph].bounds
                if not _box:
                    continue
                _cx = _box[0] + (_box[2] - _box[0]) * .5
                _cy = _box[1] + (_box[3] - _box[1]) * .5
                # calculate origin in relation to base glyph
                dx = cx - _cx
                dy = cy - _cy
                # create transformation matrix
                tt = Transform()
                tt = tt.skew(skew)
                tt = tt.translate(dx, dy).rotate(rotation).translate(-dx, -dy)
                # apply transformation matrix to component offset
                P = RPoint()
                P.position = component.offset
                P.transformBy(tuple(tt))
                # set component offset position
                component.offset = P.position

        for anchor in dstG.anchors:
            anchor.x += int(round(tan(radians(skew or 0)) * anchor.y)) # Correct for italic angle offset in x

        # check if "add extremes" is set to True
        if gd.addItalicExtremePoints and addExtremes:
            self.addExtremePoints(dstG, doSelect=True)

        dstG.round()
        dstG.angledLeftMargin = srcG.angledLeftMargin
        dstG.angledRightMargin = srcG.angledRightMargin
        
        dstG.copyToLayer('background', dstG)
        #dstG.removeSelection()
        dstG.changed()

    def addExtremePoints(self, g, doSelect=False):
        g.extremePoints(round=0)
        for contour in g:
            for point in contour.points:
                if "extremePoint" in point.labels:
                    point.selected = doSelect
                    point.smooth = True
                else:
                    point.selected = doSelect
       
 