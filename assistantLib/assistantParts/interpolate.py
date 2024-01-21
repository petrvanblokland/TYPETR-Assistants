# -*- coding: UTF-8 -*-

import sys
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR
from mojo.roboFont import CurrentFont

class AssistantPartInterpolate(BaseAssistantPart):
    """The Interpolate assistant part, checks on interpolation errors and
    interpolates glyphs is the UFO is defined as instance, instead of master.
    """
    def initMerzInterpolate(self, container):
        """Update any Merz objects that exist in the EditWindow"""
        self.registerKeyStroke('§', 'curvesB2QGlyphKey')

    def updateInterpolate(self, info):
        c = self.getController()
        g = info['glyph']
        if g is None:
            return
        md = self.getMasterData(g.font)
        c.w.InterpolateButton.enable(None not in (md.m1, md.m2))

    def buildInterpolate(self, y):
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = L/2
        c = self.getController()
        c.w.InterpolateButton = Button((C2, y, CW, L), 'Interpolate', callback=self.interpolateCallback)
        y += L + LL
        return y

    def curvesB2QGlyphKey(self, g, c, event):
        self.interpolateCallback(g)

    def interpolateCallback(self, sender=None):
        g = CurrentGlyph()
        if g is None:
            return
        md = self.getMasterData(g.font)
        if md.m1 is not None and md.m2 is not None:
            f1 = self.getFont(md.m1)
            f2 = self.getFont(md.m2)
            md1 = self.getMasterData(f1)
            md2 = self.getMasterData(f2)
            if g.name in f1 and g.name in f2:
                iFactor = (md.HStem - md1.HStem)/(md2.HStem - md1.HStem)
                self.interpolateGlyph(g, f1[g.name], f2[g.name], iFactor)
            else:
                print(f'### Glyph {g.name} does not exist in source fonts')

    def _interpolateValue(self, v1, v2, i, doRound=True):
        v = v1 + (v2 - v1)*i
        if doRound:
            v = int(round(v))
        return v
        
    def interpolateGlyph(self, g, gMaster1, gMaster2, ix, iy=None, doRound=True):
        if iy is None: 
            iy = ix
        f = g.font
        self.copyGlyph(gMaster1.font, g.name, f, g.name)
        g = f[g.name]
        g.width = self._interpolateValue(gMaster1.width, gMaster2.width, ix)
        g.unicode = gMaster1.unicode
        
        # Interpolate component positions
        for cIndex, component in enumerate(g.components):
            try:
                t = list(component.transformation)
                t1 = list(gMaster1.components[cIndex].transformation)
                t2 = list(gMaster2.components[cIndex].transformation)
                t[-2] = self._interpolateValue(t1[-2], t2[-2], ix, doRound) # Interpolate tx
                t[-1] = self._interpolateValue(t1[-1], t2[-1], iy, doRound) # Interpolate ty
                component.transformation = t
            except IndexError:
                print(f'### Error /{g.name} interpolating component {cIndex} transformation')

        # Interpolate all points, independent of their type.
        for cIndex, contour in enumerate(g.contours):
            for pIndex, p in enumerate(contour.points):
                try:
                    p1 = gMaster1.contours[cIndex].points[pIndex]
                    p2 = gMaster2.contours[cIndex].points[pIndex]
                    p.x = self._interpolateValue(p1.x, p2.x, ix, doRound)
                    p.y = self._interpolateValue(p1.y, p2.y, iy, doRound)
                except IndexError:
                    print(f'### Error /{g.name} interpolating contours {cIndex} point {pIndex} {(p.x, p.y)}')
                    break

        # Interpolate all anchor positions
        for aIndex, anchor in enumerate(g.anchors):
            try:
                a1 = gMaster1.anchors[aIndex]
                a2 = gMaster2.anchors[aIndex]
                anchor.x = self._interpolateValue(a1.x, a2.x, ix, doRound)
                anchor.y = self._interpolateValue(a1.y, a2.y, iy, doRound)
            except IndexError:
                print(f'### Error /{g.name} interpolating anchor {aIndex} {anchor.name} {(anchor.x, anchor.y)}')
        return g

