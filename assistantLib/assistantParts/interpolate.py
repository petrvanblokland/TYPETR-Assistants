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
#@@@ Make interpolation method independent, so it can be used in scripts
#from assistantLib.toolbox.interpolate import interpolateGlyph

#importlib.reload(assistantLib.assistantParts.outliner)
from assistantLib.assistantParts.outliner import calculateOutline, OL_BUTT, OL_SQUARE

class AssistantPartInterpolate(BaseAssistantPart):
    """The Interpolate assistant part, checks on interpolation errors and
    interpolates glyphs is the UFO is defined as instance, instead of master.
    """

    COLORSET = [
        # Sequence of interpolation color lines.
        (1, 0, 0, 1),
        (0.75, 0.25, 0, 1),
        (0.5, 0.5, 0, 1),
        (0.25, 0.75, 0, 1),
        (0, 1, 0, 1),
        (0, 0.75, 0.25, 1),
        (0, 0.5, 0.5, 1),
        (0, 0.25, 0.75, 1),
        (0, 0, 1, 1),
        (0.25, 0, 0.75, 1),
        (0.5, 0, 0.5, 1),
        (0.75, 0, 0.25, 1),
    ]
    INTERPOLATION_MAX_POINT_MARKERS = 100 # Max amount of points for interpolation error lines.
    INTERPOLATION_ERROR_COLOR = (0, 0.2, 0.6, 1)
    INTERPOLATION_LINE_MARKERS_COLORS = COLORSET * int((INTERPOLATION_MAX_POINT_MARKERS + len(COLORSET)) / len(COLORSET))

    def initMerzInterpolate(self, container):
        """Update any Merz objects that exist in the EditWindow"""
        # Interpolation lines
        # Triggered by w.interpolationPathOverlay
        self.interpolationPath = container.appendPathSublayer(
            position=(0, 0),
            fillColor=None,
            strokeColor=self.INTERPOLATION_ERROR_COLOR,
            strokeWidth=1,
            visible=False,
        )
        self.interpolationLineMarkers = []
        for pIndex in range(self.INTERPOLATION_MAX_POINT_MARKERS): # Max number of points to display in a glyph from the background glyph layer
            self.interpolationLineMarkers.append(container.appendPathSublayer(name=f"interpolationError{pIndex:03d}",
                fillColor=None,
                strokeColor=self.INTERPOLATION_LINE_MARKERS_COLORS[-pIndex],
                strokeWidth=1,
                visible=False,
            ))


    def setGlyphInterpolation(self, g):
        """Setup the glyph.lib-->isLower flag if it not already exists, copied from the GlyphData.isLower.
        If the flag already exists, this will overwrite the value in the GlyphData table.
        This is a bit of hack (allowing the flag to be changed in the assistant interface). Eventually this
        value should go back into GlyphData table for each glyph.
        """
        c = self.getController()
        gd = self.getGlyphData(g)
        if gd is not None: # Only if there is glyphData for this glyph:
            isLower = self.getLib(g, 'glyphIsLower', gd.isLower) # Just make sure it exists, using the flag in GlyphData.isLower as default
        else:
            isLower = False
        c.w.glyphIsLower.set(isLower)

    def updateInterpolate(self, info):
        changed = False
        c = self.getController()
        if c is None: # Assistant window may just have been closed.
            return False
        g = info['glyph']
        g = self.getCurrentGlyph()
        if g is None:
            return False # Nothing changed to the glyph

        md = self.getMasterData(g.font)
        c.w.interpolateButton.enable(None not in (md.m1, md.m2))
                        
        ref = self.getFont(md.m0)
        D = 300
        epIndex = 0 # Index of interpolation error lines

        # Show the interpolation reference glyph on the right side of the current glyph
        if g.name in ref:
            refG = ref[g.name]
            self.interpolationPath.setPath(refG.getRepresentation("merz.CGPath"))
            self.interpolationPath.setPosition((g.width*2, 0))
            self.interpolationPath.setVisible(True)

            points = []
            for contour in refG.contours:
                points += contour.points
            refPoints = []
            for contour in g.contours:
                refPoints += contour.points

            for n in range(min(self.MAX_POINT_MARKERS, len(points), len(refPoints))):
                #print(points[n].x, points[n].y, refPoints[n].x + g.width*2, refPoints[n].y)
                p0 = points[n]
                p1 = refPoints[n]
                if p0.type != p1.type:
                    self.interpolationLineMarkers[epIndex].setVisible(True)
                    self.interpolationLineMarkers[epIndex].setStrokeColor(self.INTERPOLATION_LINE_MARKERS_COLORS[epIndex])
                    pen = self.interpolationLineMarkers[epIndex].getPen()
                    px0, py0 = p0.x + g.width*2, p0.y
                    px1, py1 = p1.x, p1.y
                    pen.moveTo((px0, py0))
                    #pen.lineTo((refPoints[n].x + g.width*2, refPoints[n].y+300))
                    pen.curveTo(
                        (px0 + (px1 - px0)/2, py0 + (py1 - py0)/2 + D),
                        (px0 + (px1 - px0)/2, py0 + (py1 - py0)/2 - D),
                        (px1, py1)
                    )
                    pen.curveTo(
                        (px0 + (px1 - px0)/2, py0 + (py1 - py0)/2 - D),
                        (px0 + (px1 - px0)/2, py0 + (py1 - py0)/2 + D),
                        (px0, py0)
                    )
                    pen.closePath()
                    epIndex += 1
        else:
            self.familyOverviewInterpolationPath.setVisible(False)


        # Hide the remaining interpolation lines.
        for n in range(epIndex, len(self.interpolationLineMarkers)):
            self.interpolationLineMarkers[n].setVisible(False)


        return changed

    KEY_INTERPOLATE = '§'

    def buildInterpolate(self, y):
        personalKey = self.registerKeyStroke(self.KEY_INTERPOLATE, 'interpolateGlyphKey')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = L/2
        c = self.getController()
        c.w.glyphIsLower = CheckBox((C0, y, CW, L), 'Glyph is lowercase', value=False, sizeStyle='small', callback=self.glyphIsLowerCallback) # Stored in glyph.lib, overwrites the GlyphData.isLower flag.
        c.w.interpolateAllSelectedGlyphs = CheckBox((C1, y, CW, L), 'Interpolate selected', value=False, sizeStyle='small')
        c.w.interpolateButton = Button((C2, y, CW, L), f'Interpolate [{personalKey}]', callback=self.interpolateGlyphCallback)
        y += L
        c.w.showInterpolationLines = CheckBox((C0, y, CW, L), f'Show interpolation lines', callback=self.showInterpolationLinesCallback, sizeStyle='small')
        y += L
        c.w.decomposeCopiedInterpolatedGlyph = CheckBox((C0, y, CW, L), 'Decompose copy', value=False, sizeStyle='small')
        c.w.copyFromRomanButton = Button((C1, y, CW, L), 'Copy from Roman', callback=self.copyFromRomanCallback)
        c.w.copyFromSourceButton = Button((C2, y, CW, L), 'Copy from source', callback=self.copyFromSourceCallback)
        y += L + L/5
        c.w.interpolateEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.interpolateEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5
        return y

    def glyphIsLowerCallback(self, sender):
        """Set the isLower flag for this glyph in all masters."""
        g = self.getCurrentGlyph()
        for f in self.getAllFonts():
            if g.name in f:
                gg = f[g.name]
                self.setLib(gg, 'glyphIsLower', sender.get()) # Just make sure it exists, using the flag in GlyphData.isLower as default

    def showInterpolationLinesCallback(self, sender):
        """Toggle the checkbox flag to show/hide interpolation lined"""
        print('sdaasadsdsdas')
        g = self.getCurrentGlyph()
        if g is not None:
            g.changed()

    def interpolateGlyphKey(self, g, c, event):
        gName = g.name
        f = g.font
        if 0 and 'superior' in gName: # @@@@
            f[gName] = f[gName.replace('superior', '')]
        g.prepareUndo()
        print(f'... Interpolate glyph /{gName}')
        changed = self.interpolateGlyph(g)
        if changed:
            f[gName].changed()

    def interpolateGlyphCallback(self, sender):
        c = self.getController()
        g = self.getCurrentGlyph()
        if g is not None:
            g.prepareUndo()
            if c.w.interpolateAllSelectedGlyphs.get():
                for gg in g.font:
                    if gg.selected:
                        print(f'... Interpolate selected /{gg.name}')
                        changed = self.interpolateGlyph(gg)
                        if changed:
                            gg.changed()
            else: # Just do the current glyphs
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
                g.prepareUndo()
                if c.w.decomposeCopiedInterpolatedGlyph.get():
                    rf[g.name].decompose() # Make sure not to save this one.
                f[g.name] = rf[g.name]
                f[g.name].changed()

    def copyFromSourceCallback(self, sender=None):
        """Copy the glyph from roman to alter it manually, instead of interpolating or italicizing."""
        c = self.getController()
        g = self.getCurrentGlyph()
        if g is None:
            return
        f = g.font
        md = self.getMasterData(f)
        if md.srcUFOPath is not None:
            rf = self.getFont(md.srcUFOPath)
            g.prepareUndo()
            if g.name in rf:
                f[g.name] = rf[g.name]
                f[g.name].changed()

    def interpolateGlyph(self, g):
        """Interpolate the g from the settings in MasterData. This could be a plain interpolation, or it can be scalerpolation if
        glyph.lib-->isLower and if the xHeight of the interpolation sources is different from the xHeight of the current target glyph.
        If the glyph is "mod", then use the md.modStem values instead."""
        f = g.font
        md = self.getMasterData(f)
        gd = self.getGlyphData(g)
        iScale = iFactor = None
        changed = False

        g.prepareUndo()

        if md.m1 is None:
            f1 = f
        else:
            f1 = self.getFont(md.m1)
        if md.m2 is None:
            f2 = f
        else:
            f2 = self.getFont(md.m2)

        md1 = self.getMasterData(f1)
        md2 = self.getMasterData(f2)

        if g.name in f1 and g.name in f2:
            if 'mod' in g.name: # Use gd.isMod instead?
                iFactor = (md.modStem - md1.modStem)/(md2.modStem - md1.modStem)
            else:
                iFactor = (md.HStem - md1.HStem)/(md2.HStem - md1.HStem)
        else:
            print(f'### Glyph {g.name} does not exist in source fonts')
            iFactor = None

        isLower = self.getLib(g, 'glyphIsLower', gd.isLower) # In case it does not exists, using the flag in GlyphData.isLower as default

        # Change to glyphData.height, so scalerpolation will also work for small caps.
        if g.name.endswith('.sc'):
            iScaleY = (md.scHeight - 1.5*md.scOutline) / f.info.capHeight # Also correct for increased height from outline
            iScaleX = iScaleY * md.scWidthFactor
            gName = g.name
            srcName = gName.replace('.sc', '')
            tmpName = 'TMP'
            tmpG = self.copyGlyph(f, srcName, f, tmpName, copyUnicode=False)
            tmpG.unicode = None # Avoid conflicts in FontGoggles
            g = self.copyGlyph(f, srcName, f, gName, copyUnicode=False)
            print(f'... Scalerpolating /{gName} from /{tmpName} + /{srcName} scOutline={md.scOutline} iScale={(iScaleX, iScaleY)} scFactor={(md.scIFactorX, md.scIFactorY)}')
            self.interpolateByFactor(g, tmpG, f2[srcName], ix=md.scIFactorX, iy=md.scIFactorY, doCopy=False, copyUnicode=False)
            calculateOutline(g, thickness=md.scOutline, corner=OL_SQUARE, cap=OL_SQUARE, drawOuter=False)
            self.offsetGlyph(g, dx=0, dy=md.scOutline)
            self.scaleGlyph(g, iScaleX, iScaleY)
            g.removeOverlap()
            g.angledLeftMargin = tmpG.angledLeftMargin  # * iScaleX
            g.angledRightMargin = tmpG.angledRightMargin    # * iScaleX
            #f.removeGlyph(tmpName)
            changed = True

        elif g.name.endswith('superior'):
            iScaleY = (md.superiorHeight - 2*md.superiorOutline) / f.info.xHeight # Also correct for increased height from outline
            iScaleX = iScaleY * md.superiorWidthFactor
            gName = g.name
            srcName = gName.replace('superior', '')
            tmpName = 'TMP'
            tmpG = self.copyGlyph(f, srcName, f, tmpName, copyUnicode=False)
            tmpG.unicode = None # Avoid conflicts in FontGoggles
            g = self.copyGlyph(f, srcName, f, gName, copyUnicode=False)
            print(f'... Scalerpolating /{gName} from /{tmpName} + /{srcName} scOutline={md.scOutline} iScale={(iScaleX, iScaleY)} scFactor={(md.scIFactorX, md.scIFactorY)}')
            self.interpolateByFactor(g, tmpG, f2[srcName], ix=md.superiorIFactorX, iy=md.superiorIFactorY, doCopy=False, copyUnicode=False)
            calculateOutline(g, thickness=md.superiorOutline, corner=OL_SQUARE, cap=OL_SQUARE, drawOuter=False)
            self.offsetGlyph(g, dx=0, dy=md.supsBaseline + md.superiorOutline)
            self.scaleGlyph(g, iScaleX, iScaleY)
            g.removeOverlap()
            g.angledLeftMargin = tmpG.angledLeftMargin # * iScaleX
            g.angledRightMargin = tmpG.angledRightMargin # * iScaleX
            #f.removeGlyph(tmpName)
            changed = True

        elif g.name.endswith('inferior'):
            # Assume that the superior component is already there.
            self.resetComponentPositions(g)
            self.offsetGlyph(g, dx=0, dy=-md.supsBaseline + md.sinfBaseline)

        elif isLower and f1.info.xHeight != f.info.xHeight: # Test if scalerpolation on the xHeight is needed?
            iScale = f.info.xHeight / f1.info.xHeight # Now the stems get thicker. Compensate that in the interpolation factor
            iFactor /= iScale 
            print(iScale, iFactor)
        
            # Now we can just interpolate between the masters, where the factor is defined by their ratio of the three H-stems 
            if iScale in (None, 1) and iFactor is not None:
                #print('cdsadsads interpolate', g.name, iFactor)
                changed = self.interpolateByFactor(g, f1[g.name], f2[g.name], iFactor)

            # If we're doing scalerpolation for xHeight, they
            elif iScale not in (None, 1):
                #print('cdsadsads scale', g.name, iScale)
                self.scaleGlyph(g, iScale)
                if iFactor is not None:
                    self.interpolateByFactor(g, f1[g.name], f2[g.name], iFactor)
                changed = True

        else: # Just do plain interpolation, e.g. between capitals
            if iFactor is not None:
                self.interpolateByFactor(g, f1[g.name], f2[g.name], iFactor)

        return changed

    def _interpolateValue(self, v1, v2, i, doRound=True):
        v = v1 + (v2 - v1)*i
        if doRound:
            v = int(round(v))
        return v
        
    def interpolateByFactor(self, g, gMaster1, gMaster2, ix, iy=None, doRound=True, doCopy=True, copyUnicode=True):
        if iy is None: 
            iy = ix
        f = g.font
        if doCopy:
            g = self.copyGlyph(gMaster1.font, g.name, f, g.name)
        #g = f[g.name]
        g.width = self._interpolateValue(gMaster1.width, gMaster2.width, ix)
        if copyUnicode:
            g.unicode = gMaster1.unicode
        
        print(f'... Interpolate /{gMaster1.name} + /{gMaster2.name} to /{g.name} by {ix}')

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

