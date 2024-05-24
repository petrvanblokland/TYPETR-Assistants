# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   overlay.py
#
import sys
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart

class AssistantPartOverlay(BaseAssistantPart):

    #    O V E R L A Y

    MAX_POINT_MARKERS = 150 # Should be enough to show most glyphs
    
    OVERLAY_FILL_LEFT_COLOR = 0, 0, 0, 0.6
    OVERLAY_FILL_COLOR = 0, 0, 0, 0.6
    OVERLAY_FILL_RIGHT_COLOR = 0, 0, 0, 0.6

    OVERLAY_STROKE_POINTMARKERS_COLOR = 0, 0.5, 0.5, 1

    OVERLAY_FILL_SRC_COLOR = 0, 0.2, 0.8, 0.4
    OVERLAY_STROKE_SOME_UFO_COLOR = 0, 0.8, 0.2, 0.6
    OVERLAY_FILL_SRC_COLOR = 0, 0, 0, 0.6
    OVERLAY_FILL_KERNING_COLOR = 0, 0.5, 0, 0.6
    OVERLAY_STROKE_ROMANITALIC_COLOR = 1, 0, 0, 0.7

    POINT_MARKER_R = 7

    def initMerzOverlay(self, container):    
        # Previewing current glyphs on left/right side. 
        # Triggered by w.previewGlyphLeft, w.previewGlyphOverlay and w.previewGlyphRight       

        self.previewGlyphLeft = container.appendPathSublayer(
            position=(0, 0),
            fillColor=self.OVERLAY_FILL_LEFT_COLOR,
            visible=False,
        )
        self.previewGlyphOverlay = container.appendPathSublayer(
            position=(0, 0),
            fillColor=self.OVERLAY_FILL_COLOR,
            visible=False,
        )
        self.previewGlyphRight = container.appendPathSublayer(
            position=(0, 0),
            fillColor=self.OVERLAY_FILL_RIGHT_COLOR,
            visible=False,
        )
        self.previewPointMarkers = []
        for pIndex in range(self.MAX_POINT_MARKERS): # Max number of points to display in a glyph
            self.previewPointMarkers.append(container.appendSymbolSublayer(name=f"point{pIndex:03d}",
                position=(0, 0),
                imageSettings=dict(
                    name="rectangle",
                    size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                    fillColor=None,
                    strokeColor=(0, 0.5, 0, 1),
                    strokeWidth=1,
                ),
                visible=False,
            ))
        self.backgroundPointMarkers = []
        for pIndex in range(self.MAX_POINT_MARKERS): # Max number of points to display in a glyph from the background glyph layer
            self.backgroundPointMarkers.append(container.appendRectangleSublayer(name=f"bgPoint{pIndex:03d}",
                position=(0, 0),
                size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                fillColor=None,
                strokeColor=self.OVERLAY_STROKE_POINTMARKERS_COLOR,
                strokeWidth=1,
                visible=False,
            ))
        # Triggered by w.srcUFOPathOverlay
        self.srcUFOPathOverlay = container.appendPathSublayer(
            position=(0, 0),
            fillColor=self.OVERLAY_FILL_SRC_COLOR,
                visible=False,
        )
        # Triggered by w.someUFOPathOverlay
        self.someUFOPathOverlay = container.appendPathSublayer(
            position=(0, 0),
            fillColor=None,
            strokeColor=self.OVERLAY_STROKE_SOME_UFO_COLOR,
            strokeWidth=1,
            visible=False,
        )
        # Triggered by w.orgUFOPathOverlay
        self.orgUFOPathOverlay = container.appendPathSublayer(
            position=(0, 0),
            fillColor=self.OVERLAY_FILL_SRC_COLOR,
            visible=False,
        )
        # Triggered by w.kerningSrcPathOverlay
        self.kerningSrcPathOverlay = container.appendPathSublayer(
            position=(0, 0),
            fillColor=self.OVERLAY_FILL_KERNING_COLOR,
            visible=False,
        )
        # Triggered by w.romanItalicUFOPathOverlay
        self.romanItalicUFOPathOverlay = container.appendPathSublayer(
            position=(0, 0),
            fillColor=None,
            strokeColor=self.OVERLAY_STROKE_ROMANITALIC_COLOR,
            strokeWidth=1,
            visible=False,
        )

    def updateMerzOverlay(self, info):
        c = self.getController()
        if c is None:
            return
        g = info['glyph']
        if g is None:
            return
        f = g.font
        md = self.getMasterData(f)
        km = self.getKerningManager(f)

        gLeft = gRight = fg = g.getLayer('foreground')
        # Show filled preview of the glyph on left/right side
        glyphPathLeft = glyphPathRight = glyphPath = fg.getRepresentation("merz.CGPath")
        leftName = c.w.previewGlyphLeftName.get()
        if leftName and leftName in f:
            gLeft = f[leftName].getLayer('foreground')
            k, groupK, kerningType = km.getKerning(gLeft.name, g.name) # Supply glyph names here, not the glyphs
            x = min(-gLeft.width, gLeft.angledLeftMargin-500) - k # Subtract: needs to move right
            glyphPathLeft = gLeft.getRepresentation("merz.CGPath") 
            self.previewGlyphLeft.setPath(glyphPathLeft)
            self.previewGlyphLeft.setPosition((x, 0)) # Make sure not to overlap on zero-width
            self.previewGlyphLeft.setVisible(True)

        elif c.w.previewGlyphLeft.get():
            k, groupK, kerningType = km.getKerning(g.name, g.name)
            x = min(-g.width, g.angledLeftMargin-500) - k # Subtract: needs to move right
            self.previewGlyphLeft.setPath(glyphPath)
            self.previewGlyphLeft.setPosition((x, 0)) # Make sure not to overlap on zero-width
            self.previewGlyphLeft.setVisible(True)

        else:
            self.previewGlyphLeft.setVisible(False)

        rightName = c.w.previewGlyphRightName.get()
        if rightName and rightName in f:
            gRight = f[rightName].getLayer('foreground')
            k, groupK, kerningType = km.getKerning(g.name, gRight.name)
            x = max(g.width, -g.angledRightMargin+500) + k # Add, with negative kerning moves to the left
            glyphPathRight = gRight.getRepresentation("merz.CGPath") 
            self.previewGlyphRight.setPath(glyphPathRight)
            self.previewGlyphRight.setPosition((x, 0)) # Make sure not to overlap on zero-width
            self.previewGlyphRight.setVisible(True)
        
        elif c.w.previewGlyphRight.get():
            k, groupK, kerningType = km.getKerning(g.name, g.name)
            x = max(g.width, -g.angledRightMargin+500) + k # Add, with negative kerning moves to the left
            self.previewGlyphRight.setPath(glyphPath)
            self.previewGlyphRight.setPosition((x, 0)) # Make sure not to overlap on zero-width
            self.previewGlyphRight.setVisible(True)
        
        else:
            self.previewGlyphRight.setVisible(False)

        overlayName = c.w.overlayGlyphName.get()
        if overlayName == '/?' or not overlayName:
            overlayName = g.name
        
        pIndex = 0
        if overlayName and overlayName in f:
            gOverlay = f[overlayName].getLayer('foreground')
            glyphPathOverlay = gOverlay.getRepresentation("merz.CGPath") 
            self.previewGlyphOverlay.setPath(glyphPathOverlay)
 
            x = c.w.overlayPositionSlider.get() / self.MAX_OVERLAY_SLIDER * (g.width - gOverlay.width)
            self.previewGlyphOverlay.setPosition((x, 0))
            self.previewGlyphOverlay.setVisible(True)
            
            if c.w.previewGlyphOverlay.get():
                self.previewGlyphOverlay.setFillColor(self.OVERLAY_FILL_COLOR)
            else:
                self.previewGlyphOverlay.setFillColor(None)
            
            if c.w.previewPointsOverlay.get():
                # Move point markers to this glyph, as much of the list as we need. 
                for contour in gOverlay.contours:
                    for p in contour.points:
                        if pIndex < len(self.previewPointMarkers): # Test if there is no overflow.
                            #print(pIndex, len(self.previewPointMarkers))
                            self.previewPointMarkers[pIndex].setPosition((x+p.x, p.y))
                            self.previewPointMarkers[pIndex].setVisible(True)
                            pIndex += 1
        else:
            self.previewGlyphOverlay.setVisible(False)

        # Then hide the rest of the point markers
        for n in range(pIndex, len(self.previewPointMarkers)):
            self.previewPointMarkers[n].setVisible(False)

        # If there is not an path md defined for each type of overlay, then disable their checkboxes.
        drawn = False
        if md.srcUFOPath is not None and c.w.srcUFOPathOverlay.get():
            of = self.getFont(md.srcUFOPath)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.srcUFOPathOverlay.setPath(glyphPath)
                self.srcUFOPathOverlay.setPosition((0, 0)) 
                self.srcUFOPathOverlay.setVisible(True)
                drawn = True
        if not drawn:
            self.srcUFOPathOverlay.setVisible(False)

        drawn = False
        if md.someUFOPath is not None and c.w.someUFOPathOverlay.get():
            of = self.getFont(md.someUFOPath)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.someUFOPathOverlay.setPath(glyphPath)
                self.someUFOPathOverlay.setPosition((0, 0)) 
                self.someUFOPathOverlay.setVisible(True)
                drawn = True
        if not drawn:
            self.someUFOPathOverlay.setVisible(False)

        drawn = False
        if md.orgUFOPath is not None and c.w.orgUFOPathOverlay.get():
            of = self.getFont(md.orgUFOPath)
            #print('ffdfdf', md.orgUFOPath, of)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                print('dadasaddagfdgfdgf', og.name)
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.orgUFOPathOverlay.setPath(glyphPath)
                self.orgUFOPathOverlay.setPosition((0, 0)) 
                self.orgUFOPathOverlay.setVisible(True)
                drawn = True
        if not drawn:
            self.orgUFOPathOverlay.setVisible(False) 

        drawn = False
        if md.romanItalicUFOPath is not None and c.w.romanItalicUFOPathOverlay.get():
            of = self.getFont(md.romanItalicUFOPath)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.romanItalicUFOPathOverlay.setPath(glyphPath)
                self.romanItalicUFOPathOverlay.setPosition((0, 0)) 
                self.romanItalicUFOPathOverlay.setVisible(True)
                drawn = True
        if not drawn:
            self.romanItalicUFOPathOverlay.setVisible(False) 

    def overlaySnap2Overlay(self, g, c, event):     
        """Snap the selected points of the current glyph onto points that are within range on the background glyph."""
        self.snapSelectionToNearestPoint(g)

    def overlaySnap2OverlayCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.snapSelectionToNearestPoint(g)

    def snapSelectionToNearestPoint(self, g):
        c = self.getController()
        f = g.font

        overlayText = c.w.overlayGlyphName.get()
        snapped = False

        for gName in overlayText.split('/'):
            #print('---', gName, f.path)
            gName = gName.strip()
            if gName and f is not None and gName in f:
                og = f[gName] # Use current font as overlay
                offsetX = c.w.overlayPositionSlider.get() / self.MAX_OVERLAY_SLIDER * (g.width - og.width)
                snapped = snapped or self.snapGlyphPoints(g, og, offsetX)
        
        if snapped:
            g.changed()

    def snapGlyphPoints(self, g, srcGlyph, offsetX=0):
        g.prepareUndo()
        snapped = False
        for contour in g.contours:
            offCurves = []
            used = set()
            points = contour.points
            for pIndex, p in enumerate(points): # First do on-curves + offcurves
                if p.selected and p.type != 'offcurve':
                    distance = None
                    nearestX = nearestY = None 
                    for gContour in srcGlyph.contours:
                        for gp in gContour.points:
                            gpx = gp.x + offsetX
                            gpy = gp.y
                            if (gpx, gpy)in used:
                                continue
                            if gp.type != 'offcurve':
                                d = self.distance(p.x, p.y, gpx, gpy)
                                if distance is None or d < distance:
                                    nearestX = gpx
                                    nearestY = gpy
                                    distance = d
                    if nearestX is not None:
                        dx = nearestX - p.x
                        dy = nearestY - p.y
                        p.x = int(round(nearestX))
                        p.y = int(round(nearestY))
                        used.add((p.x, p.y))
                        p_1 = points[pIndex-1]

                        # Move neighbour offcurves relative to p
                        if p_1.type == 'offcurve':
                            p_1.x = int(round(p_1.x + dx))
                            p_1.y = int(round(p_1.y + dy))
                            offCurves.append(p_1)
                        if pIndex < len(contour.points)-1:
                            p1 = points[pIndex+1]
                            if p1.type == 'offcurve':
                                p1.x = int(round(p1.x + dx))
                                p1.y = int(round(p1.y + dy))
                                offCurves.append(p1)
                        else:
                            p1 = points[0]
                            if p1.type == 'offcurve':
                                p1.x = int(round(p1.x + dx))
                                p1.y = int(round(p1.y + dy))
                                offCurves.append(p1)
                        snapped = True

            for p in points: # Then do off-curves after, if selected or previously moved
                if p.selected and p.type == 'offcurve' or p in offCurves:
                    distance = None
                    nearestX = nearestY = None 
                    for gContour in srcGlyph.contours:
                        for gp in gContour.points:
                            gpx = gp.x + offsetX
                            gpy = gp.y
                            if (gpx, gpy) in used:
                                continue
                            if gp.type == 'offcurve':
                                d = self.distance(p.x, p.y, gpx, gpy)
                                if distance is None or d < distance:
                                    nearestX = gpx
                                    nearestY = gpy
                                    distance = d
                    if nearestX is not None:
                        p.x = int(round(nearestX))
                        p.y = int(round(nearestY))
                        used.add((p.x, p.y))
                        snapped = True
        return snapped

    #    O V E R L A Y
    
    MAX_OVERLAY_SLIDER = 2048

    def buildOverlay(self, y):
        """Build the overlay UI controls. Give control to show the following masters (if defined in the masterData)
        5 types of overlay. They checkboxes are disabled if the current glyph master data does not have one of
        the paths defined.

        md.srcPath              "Original" master of this font, used as source to copy from
        md.displaySrcPath       Show this outline on the background
        md.orgPath              "Original" master of this font for overlay reference
        md.romanItalicPath      Roman <---> Italic master reference
        md.kerningSrcPath       Used as kerning reference.

        """
        personalKey = self.registerKeyStroke('g', 'overlaySnap2Overlay')

        # Calculate the column positions
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.previewGlyphLeft = CheckBox((C0, y, CW, L), 'Preview Left', value=True, callback=self.updateEditor)
        c.w.previewGlyphOverlay = CheckBox((C1, y, CW, L), 'Fill', value=True, callback=self.updateEditor)
        c.w.previewPointsOverlay = CheckBox((C1 + CW/2, y, CW, L), 'Points', value=False, callback=self.updateEditor)
        c.w.previewGlyphRight = CheckBox((C2, y, CW, L), 'Preview Right', value=True, callback=self.updateEditor)
        y += L
        c.w.previewGlyphLeftName = EditText((C0, y, CW, L), callback=self.updateEditor)
        c.w.overlayGlyphName = EditText((C1, y, CW, L), callback=self.updateEditor)
        c.w.previewGlyphRightName = EditText((C2, y, CW, L), callback=self.updateEditor)
        y += L
        c.w.overlayAlignment = RadioGroup((C1, y, CW, L), ('L', 'C', 'R'), isVertical=False, sizeStyle='small', callback=self.updateOverlayPositionCallback)
        c.w.overlayAlignment.set(0)
        y += L
        c.w.overlayPositionSlider = Slider((C1, y, CW, L), minValue=0, maxValue=self.MAX_OVERLAY_SLIDER, value=0, 
            sizeStyle='small', continuous=True, callback=self.updateOverlayPositionSliderCallback)
        y += L
        c.w.srcUFOPathOverlay = CheckBox((C0, y, CW, L), 'Source UFO overlay', value=True, sizeStyle='small', callback=self.updateEditor)
        c.w.someUFOPathOverlay = CheckBox((C1, y, CW, L), 'Some UFO overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        c.w.orgUFOPathOverlay = CheckBox((C2, y, CW, L), 'Original UFO overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        y += L
        c.w.kerningSrcUFOPathOverlay = CheckBox((C0, y, CW, L), 'Kerning overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        c.w.romanItalicUFOPathOverlay = CheckBox((C1, y, CW, L), 'Roman/italic', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L
        c.w.snapOnBackgroundButton = Button((C2, y, CW, L), f'Snap on BG [{personalKey}]', callback=self.overlaySnap2OverlayCallback)
        y += L + L/5
        c.w.overlayEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.overlayEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5
        return y

    def updateOverlayPositionCallback(self, sender):
        position = self.w.overlayAlignment.get()
        self.w.overlayPositionSlider.set(position/2*self.MAX_OVERLAY_SLIDER)
        self.updateEditor(sender)

    def updateOverlayPositionSliderCallback(self, sender):
        position = int(round(self.w.overlayPositionSlider.get()))
        if position == 0:
            align = 0
        elif position == self.MAX_OVERLAY_SLIDER/2:
            align = 1
        elif position == self.MAX_OVERLAY_SLIDER:
            align = 2
        else:
            align = 1
        self.w.overlayAlignment.set(align)
        self.updateEditor(sender)

