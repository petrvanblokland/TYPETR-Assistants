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

class AssistantPartOverlay(BaseAssistantPart):

    #    O V E R L A Y

    MAX_POINT_MARKERS = 100
    
    OVERLAY_FILL_LEFT_COLOR = 0, 0, 0, 0.6
    OVERLAY_FILL_COLOR = 0, 0, 0, 0.6
    OVERLAY_FILL_RIGHT_COLOR = 0, 0, 0, 0.6

    OVERLAY_STROKE_POINTMARKERS_COLOR = 0, 0.5, 0.5, 1

    OVERLAY_FILL_SRC_COLOR = 0, 0.2, 0.8, 0.4
    OVERLAY_STROKE_SOME_UFO_COLOR = 0, 0.8, 0.2, 0.6
    OVERLAY_FILL_SRC_COLOR = 0, 0, 0, 0.6
    OVERLAY_FILL_KERNING_COLOR = 0, 0.5, 0, 0.6
    OVERLAY_STROKE_ROMANITALIC_COLOR = 1, 0, 0, 0.7

    POINT_MARKER_R = 8

    def initMerzOverlay(self, container):    
        # Previewing current glyphs on left/right side. 
        # Triggered by w.previewGlyphLeft, w.previewGlyphOverlay and w.previewGlyphRight       

        self.registerKeyStroke('g', 'overlaySnap2Overlay')

        self.previewGlyphLeft = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=self.OVERLAY_FILL_LEFT_COLOR,
        )
        self.previewGlyphOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=self.OVERLAY_FILL_COLOR,
        )
        self.previewGlyphRight = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=self.OVERLAY_FILL_RIGHT_COLOR,
        )
        self.previewPointMarkers = []
        for pIndex in range(self.MAX_POINT_MARKERS): # Max number of points to display in a glyph
            self.previewPointMarkers.append(container.appendRectangleSublayer(name="point%03d" % pIndex,
                position=(FAR, 0),
                size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                fillColor=None,
                strokeColor=(0, 0.5, 0, 1),
                strokeWidth=1,
            ))
        self.backgroundPointMarkers = []
        for pIndex in range(self.MAX_POINT_MARKERS): # Max number of points to display in a glyph from the background glyph layer
            self.backgroundPointMarkers.append(container.appendRectangleSublayer(name="bgPoint%03d" % pIndex,
                position=(FAR, 0),
                size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                fillColor=None,
                strokeColor=self.OVERLAY_STROKE_POINTMARKERS_COLOR,
                strokeWidth=1,
            ))
        # Triggered by w.srcUFOPathOverlay
        self.srcUFOPathOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=self.OVERLAY_FILL_SRC_COLOR,
        )
        # Triggered by w.someUFOPathOverlay
        self.someUFOPathOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=None,
            strokeColor=self.OVERLAY_STROKE_SOME_UFO_COLOR,
            strokeWidth=1,
        )
        # Triggered by w.orgUFOPathOverlay
        self.orgUFOPathOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=self.OVERLAY_FILL_SRC_COLOR,
        )
        # Triggered by w.kerningSrcPathOverlay
        self.kerningSrcPathOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=self.OVERLAY_FILL_KERNING_COLOR,
        )
        # Triggered by w.romanItalicUFOPathOverlay
        self.romanItalicUFOPathOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=None,
            strokeColor=self.OVERLAY_STROKE_ROMANITALIC_COLOR,
            strokeWidth=1,
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

        gLeft = gRight = fg = g.getLayer('foreground')
        # Show filled preview of the glyph on left/right side
        glyphPathLeft = glyphPathRight = glyphPath = fg.getRepresentation("merz.CGPath")
        leftName = c.w.previewGlyphLeftName.get()
        if leftName and leftName in f:
            gLeft = f[leftName].getLayer('foreground')
            glyphPathLeft = gLeft.getRepresentation("merz.CGPath") 
            self.previewGlyphLeft.setPath(glyphPathLeft)
            self.previewGlyphLeft.setPosition((-gLeft.width, 0))

        elif c.w.previewGlyphLeft.get():
            self.previewGlyphLeft.setPath(glyphPath)
            self.previewGlyphLeft.setPosition((-g.width, 0))

        else:
            self.previewGlyphLeft.setPosition((FAR, 0)) # Far, far away

        rightName = c.w.previewGlyphRightName.get()
        if rightName and rightName in f:
            gRight = f[rightName].getLayer('foreground')
            glyphPathRight = gRight.getRepresentation("merz.CGPath") 
            self.previewGlyphRight.setPath(glyphPathRight)
            self.previewGlyphRight.setPosition((g.width, 0))
        
        elif c.w.previewGlyphRight.get():
            self.previewGlyphRight.setPath(glyphPath)
            self.previewGlyphRight.setPosition((g.width, 0))
        
        else:
            self.previewGlyphRight.setPosition((FAR, 0))

        overlayName = c.w.overlayGlyphName.get()
        if overlayName == '/?' or not overlayName:
            overlayName = g.name
        
        pIndex = 0
        if overlayName and overlayName in f:
            gOverlay = f[overlayName].getLayer('foreground')
            glyphPathOverlay = gOverlay.getRepresentation("merz.CGPath") 
            self.previewGlyphOverlay.setPath(glyphPathOverlay)
            
            if c.w.overlayAlignment.get() == 0:
                x = 0 # Left aligned 
            elif c.w.overlayAlignment.get() == 1:
                x = (g.width - gOverlay.width)/2
            else:
                x = g.width - gOverlay.width
            self.previewGlyphOverlay.setPosition((x, 0))
            
            if c.w.previewGlyphOverlay.get():
                self.previewGlyphOverlay.setFillColor(self.OVERLAY_FILL_COLOR)
            else:
                self.previewGlyphOverlay.setFillColor(None)
            
            if c.w.previewPointsOverlay.get():
                # Move point markers to this glyph, as much of the list as we need. 
                for contour in gOverlay.contours:
                    for p in contour.points:
                        #print(pIndex, len(self.previewPointMarkers))
                        self.previewPointMarkers[pIndex].setPosition((x+p.x-self.POINT_MARKER_R, p.y-self.POINT_MARKER_R)) 
                        pIndex += 1
        else:
            self.previewGlyphOverlay.setPosition((FAR, 0))            

        # Then hide the rest of the point markers
        for n in range(pIndex, len(self.previewPointMarkers)):
            self.previewPointMarkers[n].setPosition((FAR, 0)) 

        # If there is not an path md defined for each type of overlay, then disable their checkboxes.
        drawn = False
        if md.srcUFOPath is not None and c.w.srcUFOPathOverlay.get():
            of = self.getFont(md.srcUFOPath)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.srcUFOPathOverlay.setPath(glyphPath)
                self.srcUFOPathOverlay.setPosition((0, 0)) 
                drawn = True
        if not drawn:
            self.srcUFOPathOverlay.setPosition((FAR, 0)) 

        drawn = False
        if md.someUFOPath is not None and c.w.someUFOPathOverlay.get():
            of = self.getFont(md.someUFOPath)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.someUFOPathOverlay.setPath(glyphPath)
                self.someUFOPathOverlay.setPosition((0, 0)) 
                drawn = True
        if not drawn:
            self.someUFOPathOverlay.setPosition((FAR, 0)) 

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
                drawn = True
        if not drawn:
            self.orgUFOPathOverlay.setPosition((FAR, 0)) 

        drawn = False
        if md.romanItalicUFOPath is not None and c.w.romanItalicUFOPathOverlay.get():
            of = self.getFont(md.romanItalicUFOPath)
            if of is not None and g.name in of:
                og = of[g.name] # The overlay glyph
                glyphPath = og.getRepresentation("merz.CGPath") 
                self.romanItalicUFOPathOverlay.setPath(glyphPath)
                self.romanItalicUFOPathOverlay.setPosition((0, 0)) 
                drawn = True
        if not drawn:
            self.romanItalicUFOPathOverlay.setPosition((FAR, 0)) 

            
    #    O V E R L A Y
    
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
        c.w.overlayAlignment = RadioGroup((C1, y, CW, L), ('L', 'C', 'R'), isVertical=False, sizeStyle='small', callback=self.updateEditor)
        c.w.overlayAlignment.set(0)
        y += L
        c.w.srcUFOPathOverlay = CheckBox((C0, y, CW, L), 'Source UFO overlay', value=True, sizeStyle='small', callback=self.updateEditor)
        c.w.someUFOPathOverlay = CheckBox((C1, y, CW, L), 'Some UFO overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        c.w.orgUFOPathOverlay = CheckBox((C2, y, CW, L), 'Original UFO overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        y += L
        c.w.kerningSrcUFOPathOverlay = CheckBox((C0, y, CW, L), 'Kerning overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        c.w.romanItalicUFOPathOverlay = CheckBox((C1, y, CW, L), 'Roman/italic', value=False, sizeStyle='small', callback=self.updateEditor)
        y += L * 1.5
        return y
