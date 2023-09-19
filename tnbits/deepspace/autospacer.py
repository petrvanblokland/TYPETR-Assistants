# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#            autospacer.py
#

from mojo.tools import IntersectGlyphWithLine, intersection
from lib.tools.bezierTools import curveConverter

from tnbits.contributions.typemytype.outliner import OutlinePen
from tnbits.model.objects.glyph import boundingBox, nakedGlyph

# Open Source
# https://github.com/ninastoessinger/Touche
from tnbits.contributions.touche.touche import Touche


class AutoSpacer(object):

    STEP = 8

    def __init__(self, regionFactor=0.01):
        self.regionFactor = regionFactor # % of emSize

    def calculate(self, glyph, offset):

        pen = OutlinePen(glyph.font,
                            offset=offset,
                            connection='round',
                            cap='round',
                            mitterLimit=None,
                            closeOpenPaths=True)
        glyph.draw(pen)

        pen.drawSettings(drawOriginal=False, drawInner=True, drawOuter=False)
        return pen

    def makeRegion(self, glyph, width, srcLayer):
        nakedGlyph(glyph).copyLayerToLayers(srcLayer, 'AutoKernRegion')
        layerGlyph = glyph.getLayer('AutoKernRegion')
        #layerGlyph.removeOverlap()
        regionGlyph = glyph.getLayer('AutoKern')
        regionGlyph.clear()
        outline = self.calculate(layerGlyph, width)
        outline.drawPoints(regionGlyph.getPointPen())
        #regionGlyph.removeOverlap()
        #regionGlyph.round()
        # Region is always Bezier
        naked = regionGlyph.naked()
        if curveConverter.isQuadratic(naked):
            curveConverter.quadratic2bezier(naked)
        return regionGlyph

    def getSpaceGlyph(self, glyph):
        return glyph.getLayer('AutoSpace')

    def autoKern(self, glyph1, glyph2, regionSize=None, k=0):
        style = glyph1.getParent()
        if regionSize is None:
            regionSize = int(round(self.regionFactor * style.info.unitsPerEm))
        self.makeRegion(glyph1, regionSize, 'foreground')
        #self.makeRegion(glyph2, regionSize, 'foreground')

        #t = Touche(style)
        #t.findTouchingPairs((glyph1.getLayer('AutoKern'), glyph2.getLayer('AutoKern')))
        #return t
        #return t.checkPair(glyph1.getLayer('AutoKern'), glyph2.getLayer('AutoKern'), k)

    def autoSpace(self, glyph, normVolume=None):
        """Guess an x-position at distance from the right side bearing, outside the bounding box,
        e.g. on the `max(width+value, boundings.right+value)`.
        """
        overSize = 10
        length = 0
        self.makeRegion(glyph, self.regionSize, 'foreground', 'AutoSpace')
        left, bottom, right, top = boundingBox(glyph)
        spaceGlyph = self.getSpaceGlyph(glyph)
        rLeft = int(left-self.regionSize-overSize)
        rRight = int(right+self.regionSize+overSize)
        rBottom = int(bottom-self.regionSize-overSize)
        rTop = int(top+self.regionSize+overSize)
        # Left side
        # Right side
        rmin = right
        rmax = rRight
        rwidth = (rmin + rmax)//2
        while True:
            slices = []
            maxL = 0
            for x in range(rmax, rmin, -4):
                slices.append(IntersectGlyphWithLine(spaceGlyph, ((x, rTop), (x, rBottom))))
            for edges in slices:
                if not edges:
                    continue
                for i in range(0, int(len(edges)/2), 2):
                    if i < len(edges)-1:
                        x1, y1 = edges[i]
                        x2, y2 = edges[i+1]
                        l2 = abs(y2 - y1) * (abs(rmax - rwidth))
                        maxL = max(maxL, l2)
                        length += l2
            if maxL:
                volume = length/maxL
                print('VVVVV', rmin, rwidth, rmax, volume, normVolume)
                if normVolume is None or abs(volume - normVolume) < 2:
                    break
                elif volume > normVolume:
                    rmin, rwidth = rwidth, int((rwidth + rmax)/2)
                    print('------>', rmin, rwidth, rmax)
                else:
                    rmax, rwidth = rwidth, int((rmin + rwidth)/2)
                    print('<------', rmin, rwidth, rmax)
            if normVolume is None or rmax - rmin < 4:
                break

        self.makeRegion(glyph, rwidth - right, 'foreground', 'AutoSpace')
        return rRight - rwidth, volume

