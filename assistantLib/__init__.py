# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR assistantLib/
#
#    The assistantLib/ holds the functions and classes to construct 
#    project-specific Helper and Assistant tools.
#    Some functions are rewrites of functions that already exist in RoboFont or as
#    method in RGlyph and RFont classes.
#

#    G L Y P H

def copyGlyph(srcFont, glyphName, dstFont=None, dstGlyphName=None):
    """Copy the @glyphName glyph from @srcFont to @dstFont.
    If @dstFont is omitted, then the @dstGlyphName (into the same font) should be defined.
    If @dstGlyphName is omitted, then @dstFont (same glyph into another font) should be defined
    different from @srcFont.
    Note that this function also overwrites/copies the anchors.
    An error is raised if @glyphName does not exist in @srcFont.
    """
    assert glyphName in srcFont, ('### Glyph "%s" does not exist source font "%s"' % (glyphName, srcFont.path))
    if dstFont is None:
        dstFont = srcFont
    if dstGlyphName is None:
        dstGlyphName = glyphName
    assert srcFont != dstFont or glyphName != dstGlyphName, ('### Either dstFont or dstGlyphName should be defined.')
    srcGlyph = srcFont[glyphName]
    dstFont.insertGlyph(srcGlyph, name=dstGlyphName)
    return dstFont[dstGlyphName]

def copyLayer(glyph, srcLayer, dstLayer):
    srcLayerGlyph = glyph.getLayer(srcLayer)
    dstLayerGlyph = glyph.newLayer(dstLayer)
    dstLayerGlyph.clear()
    pen = dstLayerGlyph.getPen()
    srcLayerGlyph.draw(pen)
    dstLayerGlyph.width = srcLayerGlyph.width

def removeLayer(glyph, layer):
    if layer != 'public.default':
        glyph.removeLayer(layer)

def scaleGlyph(g, sx, sy=None):
    if sy is None:
        sy = sx
    for component in g.components:
        t = list(component.transformation)
        t[-2] = int(round(t[-2] * sx))
        t[-1] = int(round(t[-1] * sy))
        component.transformation = t
    for contour in g.contours:
        for p in contour.points:
            p.x = int(round(p.x * sx))
            p.y = int(round(p.y * sy))
    for anchor in g.anchors:
        anchor.x = int(round(anchor.x * sx))
        anchor.y = int(round(anchor.y * sy))
    g.width = int(round(g.width * sx))


def offsetGlyph(g, dx=0, dy=0):
    for component in g.components:
        t = list(component.transformation)
        t[-2] = int(round(t[-2] + dx))
        t[-1] = int(round(t[-1] + dy))
        component.transformation = t
    for contour in g.contours:
        for p in contour.points:
            p.x = int(round(p.x + dx))
            p.y = int(round(p.y + dy))
    for anchor in g.anchors:
        anchor.x = int(round(anchor.x + dx))
        anchor.y = int(round(anchor.y + dy))

def roundGlyph(g):
    for contour in g.contours:
        for point in contour.points:
            point.x = int(round(point.x))
            point.y = int(round(point.y))
    for component in g.components:
        t = list(component.transformation)
        t[-2] = int(round(t[-2]))
        t[-1] = int(round(t[-1]))
        component.transformation = t
    for anchor in g.anchors:
        anchor.x = int(round(anchor.x))
        anchor.y = int(round(anchor.y))
    g.width = int(round(g.width))

#    I N T E R P O L A T I O N 

def _interpolateValue(v1, v2, i, doRound=True):
    v = v1 + (v2 - v1)*i
    if doRound:
        v = int(round(v))
    return v

def interpolateGlyphByFactor(g, gMaster1, gMaster2, ix, iy=None, doWidth=True, doUnicode=True, doRound=True):
    """Interpolate glyph @g from master glyphs @gMaster1 and @gMasters2 by the factor @ix
    between 0 and 1. A negative value and a value > 1 does extrapolate.
    If @iy is defined, then the interpolation is disproportional in x and y direction.
    The @doWidth flag by default will also interpolate the width. Otherwise the width of @gNaster1 is used.
    If the @doUnicode flag is set, the target glyph @g inherits the unicode from @gMaster1.
    Otherwise the original unicode is maintained.
    """
    if iy is None: 
        iy = ix
    f = g.font
    unicodeOrg = g.unicode # Keep it, in case the unicode is maintained.
    copyGlyph(gMaster1.font, g.name, f, g.name)
    g = f[g.name]
    if interpolateWidth:
        g.width = _interpolateValue(ix, gMaster1.width, gMaster2.width)
    if doUnicode:
        g.unicode = gMaster1.unicode
    else:
        g.unicode = unicodeOrg
    # Interpolate component positions
    for cIndex, component in enumerate(g.components):
        try:
            t = list(component.transformation)
            t1 = list(gMaster1.components[cIndex].transformation)
            t2 = list(gMaster2.components[cIndex].transformation)
            t[-2] = _interpolateValue(t1[-2], t2[-2], ix, doRound) # Interpolate tx
            t[-1] = _interpolateValue(t1[-1], t2[-1], iy, doRound) # Interpolate ty
            component.transformation = t
        except IndexError:
            print('### Error "%s" interpolating component %d transformation' % (g.name, cIndex))

    # Interpolate all points, independent of their type.
    for cIndex, contour in enumerate(g.contours):
        for pIndex, p in enumerate(contour.points):
            try:
                p1 = gMaster1.contours[cIndex].points[pIndex]
                p2 = gMaster2.contours[cIndex].points[pIndex]
                p.x = _interpolateValue(p1.x, p2.x, ix, doRound)
                p.y = _interpolateValue(p1.y, p2.y, iy, doRound)
            except IndexError:
                print('### Error "%s" interpolating contours %d point %d (%d,%d)' % (g.name, cIndex, pIndex, p.x, p.y))
                break

    # Interpolate all anchor positions
    for aIndex, anchor in enumerate(g.anchors):
        try:
            a1 = gMaster1.anchors[aIndex]
            a2 = gMaster2.anchors[aIndex]
            anchor.x = _interpolateValue(a1.x, a2.x, ix, doRound)
            anchor.y = _interpolateValue(a1.x, a2.y, iy, doRound)
        except IndexError:
            print('### Error "%s" interpolating anchor %d %s (%d,%d)' % (g.name, aIndex, anchor.name, anchor.x, anchor.y))
    return g
