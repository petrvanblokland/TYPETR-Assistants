# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   interpolate.py
#

def interpolateGlyph(g, md, gd, isLower):
    """Interpolate the g from the settings in MasterData. This could be a plain interpolation, or it can be scalerpolation if
    glyph.lib-->isLower and if the xHeight of the interpolation sources is different from the xHeight of the current target glyph."""
    f = g.font
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
        if isLower and f1.info.xHeight != f.info.xHeight: # Test if scalerpolation on the xHeight is needed?
            iScale = f.info.xHeight / f1.info.xHeight # Now the stems get thicker. Compensate that in the interpolation factor
            iFactor /= iScale 
            print(iScale, iFactor)
        
        # Now we can just interpolate between the masters, where the factor is defined by their ratio of the three H-stems 
        if iFactor is not None:
            #print('cdsadsads interpolate', g.name, iFactor)
            changed = self.interpolateByFactor(g, f1[g.name], f2[g.name], iFactor)

        # If we're doing scalerpolation for xHeight, they
        if iScale not in (None, 1):
            #print('cdsadsads scale', g.name, iScale)
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

