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

from mojo.roboFont import OpenWindow, CurrentGlyph, CurrentFont

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

class AssistantPartItalicize(BaseAssistantPart):
    """The Italicize assistant part italicizes the current glyph in RoboFont.
    """

    def initItalicize(self, container):
        pass

    def updateItalicize(self, info):
        pass

    def buildItalicize(self, y):
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        self.w.addItalicizedComponents = CheckBox((C1, y, CW, L), 'Add components', value=True, sizeStyle='small')
        self.w.skipItalicizedComponents = CheckBox((C1, y+LL, CW, L), 'Skip components', value=True, sizeStyle='small')
        self.w.addItalicizedExtremes = CheckBox((C1, y+2*LL, CW, L), 'Add extremes', value=True, sizeStyle='small')
        self.w.skewRotate = CheckBox((C1, y+3*LL, CW, L), 'Skew & rotate', value=False, sizeStyle='small')
        y += L

        self.w.italicizeButton = Button((C0, y, CW, L), 'Italicize', callback=self.italicizeCallback)
        y += L*1.5

        return y

    def italicizeCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            self.italicizeGlyph(g)
 
    # Function mostly copied from the Slanter extension
    def italicizeGlyph(self, g):
        f = g.font
        md = self.getMasterData(f)
        gd = self.getGlyphData(f, g.name)
        gName = g.name
        c = self.getController()

        g.prepareUndo()

        #if self.getController().w.skewRotate or gd.useSkewRotate: # Glyphs like /O better use skew+rotate to italicize   
        if controller.w.skewRotate.get(): # Glyphs like /O better use skew+rotate to italicize, just look at the checkbox, not at the GLYPH_DATA flags.
            skew = radians(md.italicSkew or -f.info.italicAngle)
            rotation = radians(md.italicRotation)
        else:
            skew = radians(-f.info.italicAngle)
            rotation = 0
        print(f'... Italicize: Skew {skew } & Rotate {rotation}', )    
        
        if not md.isItalic:
            return


        addComponents = c.w.addItalicizedComponents.get()
        skipComponents = c.w.skipItalicizedComponents.get()
        addExtremes = c.w.addItalicizedExtremes.get()

        if md.italicRomanUfo is None:
            md.italicRomanUfo = getMaster(md.italicRomanPath, showInterface=False)
            if md.italicRomanUfo is None:
                return
        src = md.italicRomanUfo[gName]
        
        f[gName] = src # Copy from roman
        dstG = f[gName]
        
        if not addComponents:
            for component in dstG.components:
                pointPen = DecomposePointPen(src.layer, dest.getPointPen(), component.transformation)
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
        box = src.bounds
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
                _box = src.layer[component.baseGlyph].bounds
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
        dstG.angledLeftMargin = src.angledLeftMargin
        dstG.angledRightMargin = src.angledRightMargin
        
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
       
 