# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   familyOverview.py
#
import sys
from vanilla import *
from math import *

from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint
from mojo.UI import OpenGlyphWindow, CurrentGlyphWindow, getGlyphViewDisplaySettings, setGlyphViewDisplaySettings

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart

class AssistantPartFamilyOverview(BaseAssistantPart):

    #    O V E R L A Y

    MAX_FAMILY_OVERVIEW = 50
    FAMILY_OVERVIEW_SCALE = 0.12 # Relates to spacer.KERN_SCALE

    MAX_FAMILY_START_POINTS = 100 # Masters * max number of contours
    FAMILY_OVERVIEW_START_POINT_SIZE = 10/FAMILY_OVERVIEW_SCALE
    FAMILY_OVERVIEW_START_POINT_COLOR = 0.9, 0.2, 0.6, 0.8

    MAX_FAMILY_ANCHORS = MAX_FAMILY_START_POINTS * 3 # Geussing the max amount of anchors to show
    FAMILY_OVERVIEW_ANCHOR_SIZE = 16/FAMILY_OVERVIEW_SCALE
    FAMILY_OVERVIEW_ANCHOR_COLOR = 0.1, 0.3, 0.8, 0.8

    FAMILY_DEFAULT_FILL_COLOR = 0, 0, 0, 1
    FAMILY_HOVER_FILL_COLOR = 1, 0, 0, 1
    FAMILY_INTERPOLATION_ERROR_FILL_COLOR = 0.3, 0.2, 1, 1 # Error color of interpolation is not compatible
    FAMILY_LABEL_FONT = 'Verdana'
    FAMILY_LABEL_SIZE = 12
    FAMILY_LABEL_SPACING = 0.5 # Factor to unitsPerEm distance between the styles, leave space for the style names

    def initMerzFamilyOverview(self, container):    
        """Previewing current glyph for all master styles, with the style name of each master"""       

        self.familyOverviewGlyphs = []
        self.familyOverviewStyleName = []
        for ufoIndex in range(self.MAX_FAMILY_OVERVIEW): # Max number glyphs in family overview
            subLayer = container.appendPathSublayer(name=f"familyOverview{ufoIndex:03d}",
                position=(0, 0),
                fillColor=(0, 0, 0, 1),
                strokeColor=None,
                visible=False,
            )
            subLayer.addScaleTransformation(self.FAMILY_OVERVIEW_SCALE)
            self.familyOverviewGlyphs.append(subLayer)            

            subLayer = container.appendTextLineSublayer(name=f"familyOverviewStyleName{ufoIndex:03d}",
                position=(0, 0),
                text='',
                font=self.FAMILY_LABEL_FONT,
                pointSize=self.FAMILY_LABEL_SIZE,
                fillColor=self.FAMILY_DEFAULT_FILL_COLOR, # Can be set to FAMILY_INTERPOLATION_ERROR_FILL_COLOR
                visible=False,
            )
            subLayer.addScaleTransformation(self.FAMILY_OVERVIEW_SCALE)            
            subLayer.setHorizontalAlignment('center')
            self.familyOverviewStyleName.append(subLayer)
        
        self.familyOverviewStartPoints = []
        for spIndex in range(self.MAX_FAMILY_START_POINTS): # Max amount of start points to show
            subLayer = container.appendOvalSublayer(name=f"familyOverviewStartPoint{spIndex:03d}",
                position=(0, 0),
                size=(self.FAMILY_OVERVIEW_START_POINT_SIZE, self.FAMILY_OVERVIEW_START_POINT_SIZE),
                fillColor=self.FAMILY_OVERVIEW_START_POINT_COLOR,
                visible=False,
            )
            subLayer.addScaleTransformation(self.FAMILY_OVERVIEW_SCALE)
            self.familyOverviewStartPoints.append(subLayer)            
        
        self.familyOverviewAnchors = []
        for spIndex in range(self.MAX_FAMILY_ANCHORS): # Max amount of start points to show
            subLayer = container.appendOvalSublayer(name=f"familyOverviewAnchors{spIndex:03d}",
                position=(0, 0),
                size=(self.FAMILY_OVERVIEW_ANCHOR_SIZE, self.FAMILY_OVERVIEW_ANCHOR_SIZE),
                fillColor=self.FAMILY_OVERVIEW_ANCHOR_COLOR,
                visible=False,
            )
            subLayer.addScaleTransformation(self.FAMILY_OVERVIEW_SCALE)
            self.familyOverviewAnchors.append(subLayer)            
        
    def updateMerzFamilyOverview(self, info):
        """Position the overview Merz elements on x = 0 and y = g.font.info.unitsPerEm""" 
        c = self.getController()
        g = info['glyph']
        if g is None:
            return
        nIndex = spIndex = 0
        if g is not None and c.w.showFamilyOverview.get():
            f = g.font
            y = f.info.unitsPerEm / self.FAMILY_OVERVIEW_SCALE

            parentPath = self.filePath2ParentPath(f.path)
            spIndex = 0 # Index of start point Merz 
            aIndex = 0 # Index of anchor point Merz

            startPos, totalFamilyOverviewSingleWidth = self.getStartPointAndSingleWidthFamilyOverview(g)
                        
            for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
                if fIndex < len(self.familyOverviewGlyphs):
                    ufo = self.getFont(pth)
                    if ufo is not None and g.name in ufo:
                        ufoG = ufo[g.name] # Show the foreground layer.
                        if not self.isCurrentGlyph(ufoG) or not c.w.showFamilyInterpolation.get() or self.doesInterpolate(ufoG):
                            fillColor = self.FAMILY_DEFAULT_FILL_COLOR
                        else:
                            fillColor = self.FAMILY_INTERPOLATION_ERROR_FILL_COLOR
                        x = startPos + totalFamilyOverviewSingleWidth*nIndex
                        glyphPath = ufoG.getRepresentation("merz.CGPath")
                        #print('Updating family glyph path', pth, g.name)
                        self.familyOverviewGlyphs[fIndex].setPath(glyphPath)
                        self.familyOverviewGlyphs[fIndex].setPosition((x, y))
                        self.familyOverviewGlyphs[fIndex].setFillColor(fillColor)
                        self.familyOverviewGlyphs[fIndex].setVisible(True)
                        self.familyOverviewStyleName[fIndex].setText(ufo.info.styleName)
                        self.familyOverviewStyleName[fIndex].setPosition((x+ufoG.width/2, y+ufo.info.descender))
                        self.familyOverviewStyleName[fIndex].setVisible(True)

                        nIndex += 1
                        # Position start points
                        for contour in ufoG.contours:
                            p = contour.points[0]
                            pos = x + p.x - self.FAMILY_OVERVIEW_START_POINT_SIZE/2, y + p.y - self.FAMILY_OVERVIEW_START_POINT_SIZE/2
                            self.familyOverviewStartPoints[spIndex].setPosition(pos)
                            self.familyOverviewStartPoints[spIndex].setVisible(True)
                            spIndex += 1

                        for a in ufoG.anchors:
                            pos = x + a.x - self.FAMILY_OVERVIEW_ANCHOR_SIZE/2, y + a.y - self.FAMILY_OVERVIEW_ANCHOR_SIZE/2
                            self.familyOverviewAnchors[aIndex].setPosition(pos)
                            self.familyOverviewAnchors[aIndex].setVisible(True)
                            aIndex += 1

        for n in range(nIndex, len(self.familyOverviewGlyphs)):
            self.familyOverviewGlyphs[n].setVisible(False)
            self.familyOverviewStyleName[n].setVisible(False)
        for n in range(spIndex, len(self.familyOverviewStartPoints)):
            self.familyOverviewStartPoints[n].setVisible(False)
        for n in range(aIndex, len(self.familyOverviewAnchors)):
            self.familyOverviewAnchors[n].setVisible(False)

    def mouseMoveFamilyOverview(self, g, x, y, event):
        """Set the hoover color for the current selected glyph"""
        if g is None:
            return
        c = self.getController()
        currentFont = g.font
        y1 = currentFont.info.unitsPerEm
        y2 = y1 + currentFont.info.unitsPerEm * self.FAMILY_OVERVIEW_SCALE
        parentPath = self.filePath2ParentPath(currentFont.path)
        
        startPos, totalFamilyOverviewSingleWidth = self.getStartPointAndSingleWidthFamilyOverview(g)
        x1 = (startPos - totalFamilyOverviewSingleWidth/2) * self.FAMILY_OVERVIEW_SCALE
        
        for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
            fullPath = self.path2FullPath(pth)
            if fIndex < len(self.familyOverviewGlyphs):
                ufo = self.getFont(fullPath)
                if ufo is not None and g.name in ufo:
                    ufoG = ufo[g.name]
                    x2 = x1 + totalFamilyOverviewSingleWidth * self.FAMILY_OVERVIEW_SCALE
                    if y1 <= y <= y2 and x1 <= x <= x2:
                        fillColor = self.FAMILY_HOVER_FILL_COLOR
                    elif not self.isCurrentGlyph(ufoG) or not c.w.showFamilyInterpolation.get() or self.doesInterpolate(ufoG):
                        fillColor = self.FAMILY_DEFAULT_FILL_COLOR
                    else:
                        fillColor = self.FAMILY_INTERPOLATION_ERROR_FILL_COLOR
                    self.familyOverviewGlyphs[fIndex].setFillColor(fillColor)
                    x1 = x2
                    
    def mouseDownFamilyOverview(self, g, x, y, event):
        """Open Editor window on clicked glyph"""
        if g is None:
            return
        currentFont = g.font
        y1 = currentFont.info.unitsPerEm
        y2 = y1 + currentFont.info.unitsPerEm * self.FAMILY_OVERVIEW_SCALE
        startPos, totalFamilyOverviewSingleWidth = self.getStartPointAndSingleWidthFamilyOverview(g)
        x1 = (startPos - totalFamilyOverviewSingleWidth/2) * self.FAMILY_OVERVIEW_SCALE
        parentPath = self.filePath2ParentPath(currentFont.path)
        for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
            fullPath = self.path2FullPath(pth)
            if fIndex < len(self.familyOverviewGlyphs):
                ufo = self.getFont(fullPath, showInterface=currentFont.path == fullPath) # Make sure RoboFont opens the current font.
                if ufo is not None and g.name in ufo:
                    ufoG = ufo[g.name]
                    x2 = x1 + totalFamilyOverviewSingleWidth * self.FAMILY_OVERVIEW_SCALE
                    if y1 <= y <= y2 and x1 <= x <= x2:
                        if currentFont.path != ufo.path:
                            rr = self.getGlyphWindowPosSize()
                            if rr is not None:
                                currentLayerName = g.layer.name
                                p, s, settings, viewFrame, viewScale = rr
                                self.setGlyphWindowPosSize(ufoG, p, s, settings=settings, viewFrame=viewFrame, viewScale=viewScale, layerName=currentLayerName)
                        return 
                    x1 = x2
            
    def getStartPointAndSingleWidthFamilyOverview(self, g):
        """Find the starting point and width per glyph for the family overview"""
        f = g.font
        y = f.info.unitsPerEm / self.FAMILY_OVERVIEW_SCALE
        parentPath = self.filePath2ParentPath(f.path)
        totalFamilyOverviewWidth = 0
        for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
            if fIndex < len(self.familyOverviewGlyphs):
                ufo = self.getFont(pth)
                if ufo is not None and g.name in ufo:
                    ufoG = ufo[g.name]
                    totalFamilyOverviewWidth += max(f.info.unitsPerEm/2, ufoG.width + f.info.unitsPerEm * self.FAMILY_LABEL_SPACING)

        totalFamilyOverviewSingleWidth = totalFamilyOverviewWidth/len(self.getUfoPaths(parentPath))
        italicOffset = y * tan(radians(-g.font.info.italicAngle or 0))
        startPos = (g.width/self.FAMILY_OVERVIEW_SCALE - totalFamilyOverviewWidth)/2 + italicOffset
        return startPos, totalFamilyOverviewSingleWidth

    def getGlyphWindowPosSize(self):
        w = CurrentGlyphWindow()
        if w is None:
            return
        x,y, width, height = w.window().getPosSize()
        settings = getGlyphViewDisplaySettings()
        view = w.getGlyphView()
        viewFrame = view.visibleRect()
        viewScale = w.getGlyphViewScale()
        return (x, y), (width, height), settings, viewFrame, viewScale

    def setGlyphWindowPosSize(self, glyph, pos, size, animate=False, settings=None, viewFrame=None, viewScale=None, layerName=None):
        OpenGlyphWindow(glyph=glyph, newWindow=False)
        w = CurrentGlyphWindow()
        view = w.getGlyphView()
        w.window().setPosSize((pos[0], pos[1], size[0], size[1]), animate=animate)
        if viewScale is not None:
            w.setGlyphViewScale(viewScale)
        if viewFrame is not None:
            view.scrollRectToVisible_(viewFrame)
        if settings is not None:
            setGlyphViewDisplaySettings(settings)
        if layerName is not None:
            w.setLayer(layerName, toToolbar=True)
                    
    #    O V E R L A Y
    
    def buildFamilyOverview(self, y):
        """Build the overlay stuff: Merz components and """
        self.registerKeyStroke('}', 'familyOverviewNextGlyph')
        self.registerKeyStroke('{', 'familyOverviewPrevGlyph')

        # Calculate the column positions
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        self.w.showFamilyOverview = CheckBox((C0, y, CW, L), 'Show family overview', value=True, sizeStyle='small', callback=self.updateEditor)
        self.w.showFamilyInterpolation = CheckBox((C1, y, CW, L), 'Show interpolation test', value=True, sizeStyle='small', callback=self.updateEditor)
        y += L + L/5
        self.w.familyOverviewEndLine = HorizontalLine((self.M, y, -self.M, 1))
        self.w.familyOverviewEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5
        return y

    #   G L Y P H  S E L E C T I O N

    def familyOverviewNextGlyph(self, g, c, event):
        """Open the EditorWindow on the next glyph in the list"""
        currentFont = g.font
        parentPath = self.filePath2ParentPath(currentFont.path)
        ufoPaths = self.getUfoPaths(parentPath)
        for fIndex in range(len(ufoPaths)):
            pth_1, pth = ufoPaths[fIndex-1], ufoPaths[fIndex]
            fullPath_1 = self.path2FullPath(pth_1)
            fullPath = self.path2FullPath(pth)
            if fullPath_1 == currentFont.path:
                nextUfo = self.getFont(fullPath, showInterface=True) # Make sure RoboFont opens the current font.
                if g.name in nextUfo:
                    nextG = nextUfo[g.name]
                    rr = self.getGlyphWindowPosSize()
                    if rr is not None:
                        currentLayerName = g.layer.name
                        p, s, settings, viewFrame, viewScale = rr
                        self.setGlyphWindowPosSize(nextG, p, s, settings=settings, viewFrame=viewFrame, viewScale=viewScale, layerName=currentLayerName)


    def familyOverviewPrevGlyph(self, g, c, event):
        """Open the EditorWindow on the previous glyph in the list"""
        currentFont = g.font
        parentPath = self.filePath2ParentPath(currentFont.path)
        ufoPaths = self.getUfoPaths(parentPath)
        for fIndex in range(len(ufoPaths)):
            pth_1, pth = ufoPaths[fIndex-1], ufoPaths[fIndex]
            fullPath_1 = self.path2FullPath(pth_1)
            fullPath = self.path2FullPath(pth)
            if fullPath == currentFont.path:
                prevUfo = self.getFont(fullPath_1, showInterface=True) # Make sure RoboFont opens the current font.
                if g.name in prevUfo:
                    prevG = prevUfo[g.name]
                    rr = self.getGlyphWindowPosSize()
                    if rr is not None:
                        currentLayerName = g.layer.name
                        p, s, settings, viewFrame, viewScale = rr
                        self.setGlyphWindowPosSize(prevG, p, s, settings=settings, viewFrame=viewFrame, viewScale=viewScale, layerName=currentLayerName)



