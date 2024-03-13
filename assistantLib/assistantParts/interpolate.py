# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   interpolate.py
#
import sys
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from mojo.roboFont import OpenFont, AllFonts, RGlyph, RPoint
from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart

class AssistantPartInterpolate(BaseAssistantPart):
    """The Interpolate assistant part, checks on interpolation errors and
    interpolates glyphs is the UFO is defined as instance, instead of master.
    """
    def initMerzInterpolate(self, container):
        """Update any Merz objects that exist in the EditWindow"""

    def updateInterpolate(self, info):
        changed = False
        c = self.getController()
        if c is None: # Assistant window may just have been closed.
            return False
        g = info['glyph']
        if g is None:
            return False # Nothing changed to the glyph
        md = self.getMasterData(g.font)
        c.w.interpolateButton.enable(None not in (md.m1, md.m2))
        return changed

    KEY_INTERPOLATE = '§'

    def buildInterpolate(self, y):
        personalKey = self.registerKeyStroke(self.KEY_INTERPOLATE, 'interpolateGlyphKey')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = L/2
        c = self.getController()
        c.w.decomposeCopiedInterpolatedGlyph = CheckBox((C0, y, CW, L), 'Decompose copy', value=False, sizeStyle='small')
        c.w.copyFromRomanButton = Button((C1, y, CW, L), 'Copy from Roman', callback=self.copyFromRomanCallback)
        c.w.interpolateButton = Button((C2, y, CW, L), 'Interpolate [%s]' % personalKey, callback=self.interpolateGlyphCallback)
        y += L + LL
        return y

    def interpolateGlyphKey(self, g, c, event):
        changed = self.interpolateGlyph(g)
        if changed:
            g.changed()

    def interpolateGlyphCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            changed = self.interpolateGlyph(g)
            if changed:
                g.changed()

    def copyFromRomanCallback(self, sender=None):
        """Copy the glyph from roman to alter it manually, instead of interpolating or italicizing."""
        c = self.getController()
        g = self.getCurrentGlyph()
        if g is None:
            return
        f = g.font
        md = self.getMasterData(f)
        if md.romanItalicUFOPath is not None:
            rf = self.getFont(md.romanItalicUFOPath)
            if g.name in rf:
                if c.w.decomposeCopiedInterpolatedGlyph.get():
                    rf[g.name].decompose() # Make sure not to save this one.
                f[g.name] = rf[g.name]
                f[g.name].changed()

    def interpolateGlyph(self, g):
        """Interpolate the g from the settings in MasterData. This could be a plain interpolation, or it can be scalerpolation if
        glyph.isLower and if the xHeight of the interpolation sources is different from the xHeight of the current target glyph."""
        f = g.font
        md = self.getMasterData(f)
        gd = self.getGlyphData(g)
        iScale = iFactor = None
        changed = False

        if md.m1 is not None and md.m2 is not None:
            f1 = self.getFont(md.m1)
            f2 = self.getFont(md.m2)
            md1 = self.getMasterData(f1)
            md2 = self.getMasterData(f2)

            if g.name in f1 and g.name in f2:
                iFactor = (md.HStem - md1.HStem)/(md2.HStem - md1.HStem)
            else:
                print(f'### Glyph {g.name} does not exist in source fonts')
                iFactor = None

            # @@@ Change later to glyphData.height, so scalerpolation will also work for small caps.
            if gd.isLower and f1.info.xHeight != f.info.xHeight: # Test if scalerpolation on the xHeight is needed?
                iScale = f.info.xHeight / f1.info.xHeight # Now the stems get thicker. Compensate that in the interpolation factor
                iFactor /= iScale 
                print(iScale, iFactor)
            
            # Now we can just interpolate between the masters, where the factor is defined by their ratio of the three H-stems 
            if iFactor is not None:
                print('cdsadsads interpolate', g.name, iFactor)
                changed = self.interpolateByFactor(g, f1[g.name], f2[g.name], iFactor)

            # If we're doing scalerpolation for xHeight, they
            if iScale not in (None, 1):
                print('cdsadsads scale', g.name, iScale)
                self.scaleGlyph(g, iScale)
                changed = True

        return changed

    def _interpolateValue(self, v1, v2, i, doRound=True):
        v = v1 + (v2 - v1)*i
        if doRound:
            v = int(round(v))
        return v
        
    def interpolateByFactor(self, g, gMaster1, gMaster2, ix, iy=None, doRound=True):
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
                t1 = gMaster1.components[cIndex].transformation
                t2 = gMaster2.components[cIndex].transformation
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

