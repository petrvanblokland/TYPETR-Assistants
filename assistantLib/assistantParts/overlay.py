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
    
    def initMerzOverlay(self, container):    
        # Previewing current glyphs on left/right side.        
        self.previewGlyphLeft = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=(0, 0, 0, 0.6),
        )
        self.previewGlyphOverlay = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=(0, 0, 0, 0.6),
        )
        self.previewGlyphRight = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=(0, 0, 0, 0.6),
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
                strokeColor=(0, 0.5, 0.5, 1),
                strokeWidth=1,
            ))

    def updateMerzOverlay(self, info):
        c = self.getController()
        if c is None:
            return
        g = info['glyph']
        if g is None:
            return
        f = g.font
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
        if overlayName == '/?':
            overlayName = g.name
        
        pIndex = 0
        if overlayName and overlayName in f:
            gOverlay = f[overlayName].getLayer('forground')
            glyphPathOverlay = gOverlay.getRepresentation("merz.CGPath") 
            self.previewGlyphOverlay.setPath(glyphPathOverlay)
            if c.w.overlayAlignment.get() == 0:
                x = 0 # Left aligned 
            elif c.w.overlayAlignment.get() == 1:
                x = (g.width - gOverlay.width)/2
            else:
                x = g.width - gOverlay.width
            self.previewGlyphOverlay.setPosition((x, 0))
            if c.w.fillOverlay.get():
                self.previewGlyphOverlay.setFillColor((0.7, 0.7, 0.7, 0.5))
            else:
                self.previewGlyphOverlay.setFillColor(None)
            # Move point markers to this glyph, as much of the list as we need. 
            for contour in gOverlay.contours:
                for p in contour.points:
                    #print(pIndex, len(self.previewPointMarkers))
                    #self.previewPointMarkers[pIndex].setPosition((x+p.x-POINT_MARKER_R, p.y-POINT_MARKER_R)) 
                    pIndex += 1
        else:
            self.previewGlyphOverlay.setPosition((FAR, 0))            

        # Then hide the rest of the point markers
        for n in range(pIndex, len(self.previewPointMarkers)):
            self.previewPointMarkers[n].setPosition((FAR, 0)) 
            
    #    O V E R L A Y
    
    def buildOverlay(self, y):
        """Build the overlay UI controls"""
        # Calculate the column positions
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        c = self.getController()
        c.w.previewGlyphLeft = CheckBox((C0, y, CW, L), 'Preview Left', value=True, callback=self.updateEditor)
        c.w.previewGlyphRight = CheckBox((C2, y, CW, L), 'Preview Right', value=True, callback=self.updateEditor)
        y += L
        c.w.previewGlyphLeftName = EditText((C0, y, CW, L), callback=self.updateEditor)
        c.w.overlayGlyphName = EditText((C1, y, CW, L), callback=self.updateEditor)
        c.w.previewGlyphRightName = EditText((C2, y, CW, L), callback=self.updateEditor)
        y += L
        c.w.overlayAlignment = RadioGroup((C1, y, CW, L), ('L', 'C', 'R'), isVertical=False, sizeStyle='small', callback=self.updateEditor)
        c.w.overlayAlignment.set(0)
        c.w.fillOverlay = CheckBox((C0, y, CW, L), 'Fill overlay', value=False, sizeStyle='small', callback=self.updateEditor)
        y += L * 1.5
        return y
