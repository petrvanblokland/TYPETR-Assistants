# -*- coding: UTF-8 -*-

import sys
from vanilla import *

from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint, CurrentGlyph, CurrentFont
from mojo.UI import OpenGlyphWindow, CurrentGlyphWindow, getGlyphViewDisplaySettings, setGlyphViewDisplaySettings

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

class AssistantPartFamilyOverview(BaseAssistantPart):

    #    O V E R L A Y

    MAX_FAMILY_OVERVIEW = 50
    FAMILY_OVERVIEW_SCALE = 0.15
    LABEL_FONT = 'Verdana'
    LABEL_SIZE = 12
    LABEL_SPACING = 400 # Distance between the styles

    def initMerzFamilyOverview(self, container):    
        # Previewing current glyphs on left/right side, with the style name of each master        
        self.familyOverviewGlyphs = []
        self.familyOverviewStyleName = []
        for ufoIndex in range(self.MAX_FAMILY_OVERVIEW): # Max number glyphs in family overview
            subLayer = container.appendPathSublayer(name="familyOverview%03d" % ufoIndex,
                position=(FAR, 0),
                fillColor=(0, 0, 0, 1),
                strokeColor=None,
            )
            subLayer.addScaleTransformation(self.FAMILY_OVERVIEW_SCALE)
            self.familyOverviewGlyphs.append(subLayer)            

            subLayer = container.appendTextLineSublayer(name="familyOverviewStyleName%03d" % ufoIndex,
                position=(FAR, 0),
                text='',
                font=self.LABEL_FONT,
                pointSize=self.LABEL_SIZE,
                fillColor=(0, 0, 0, 1),
            )
            subLayer.addScaleTransformation(self.FAMILY_OVERVIEW_SCALE)
            subLayer.setHorizontalAlignment('center')
            self.familyOverviewStyleName.append(subLayer)
        
    def updateMerzFamilyOverview(self, info):
        g = info['glyph']
        nIndex = 0
        print('Updating', g.name)
        if g is not None and self.controller.w.showFamilyOverview.get():
            f = g.font
            x = 0
            y = f.info.unitsPerEm / self.FAMILY_OVERVIEW_SCALE
            parentPath = self.filePath2ParentPath(f.path)
            for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
                if fIndex < len(self.familyOverviewGlyphs):
                    ufo = self.getFont(pth)
                    if ufo is not None and g.name in ufo:
                        ufoG = ufo[g.name]
                        glyphPath = ufoG.getRepresentation("merz.CGPath")
                        self.familyOverviewGlyphs[fIndex].setPath(glyphPath)
                        self.familyOverviewGlyphs[fIndex].setPosition((x, y))
                        self.familyOverviewStyleName[fIndex].setText(ufo.info.styleName)
                        self.familyOverviewStyleName[fIndex].setPosition((x+ufoG.width/2, y+ufo.info.descender))
                        x += max(f.info.unitsPerEm/2, ufoG.width + self.LABEL_SPACING) # Add a wordspace between the styles
                        nIndex += 1
        for n in range(nIndex, len(self.familyOverviewGlyphs)):
            self.familyOverviewGlyphs[n].setPosition((FAR, 0))
            self.familyOverviewStyleName[n].setPosition((FAR, 0))
        
    def mouseMoveFamilyOverview(self, g, x, y):
        """Set the hoover color for the current selected glyph"""
        currentFont = g.font
        y1 = currentFont.info.unitsPerEm
        y2 = y1 + currentFont.info.unitsPerEm * self.FAMILY_OVERVIEW_SCALE
        x1 = 0
        parentPath = self.filePath2ParentPath(currentFont.path)
        for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
            if fIndex < len(self.familyOverviewGlyphs):
                ufo = self.getFont(pth)
                if ufo is not None and g.name in ufo:
                    ufoG = ufo[g.name]
                    x2 = x1 + max(ufo.info.unitsPerEm/2, ufoG.width + self.LABEL_SPACING) * self.FAMILY_OVERVIEW_SCALE
                    if y1 <= y <= y2 and x1 <= x <= x2:
                        c = 1, 0, 0, 1
                    else:
                        c = 0, 0, 0, 0.8
                    self.familyOverviewGlyphs[fIndex].setFillColor(c)
                    x1 = x2
                    
    def mouseDownFamilyOverview(self, g, x, y):
        """Open Editor window on clicked glyph"""
        currentFont = g.font
        y1 = currentFont.info.unitsPerEm
        y2 = y1 + currentFont.info.unitsPerEm * self.FAMILY_OVERVIEW_SCALE
        x1 = 0
        parentPath = self.filePath2ParentPath(currentFont.path)
        for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
            if fIndex < len(self.familyOverviewGlyphs):
                ufo = self.getFont(pth)
                if ufo is not None and g.name in ufo:
                    ufoG = ufo[g.name]
                    x2 = x1 + max(ufo.info.unitsPerEm/2, ufoG.width + self.LABEL_SPACING) * self.FAMILY_OVERVIEW_SCALE
                    if y1 <= y <= y2 and x1 <= x <= x2:
                        if currentFont.path != ufo.path:
                            rr = self.getGlyphWindowPosSize()
                            if rr is not None:
                                currentLayerName = g.layer.name
                                p, s, settings, viewFrame, viewScale = rr
                                self.setGlyphWindowPosSize(ufoG, p, s, settings=settings, viewFrame=viewFrame, viewScale=viewScale, layerName=currentLayerName)
                        return 
                    x1 = x2

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
        # Calculate the column positions
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        self.w.showFamilyOverview = CheckBox((C0, y, CW, L), 'Show family overview', value=True, callback=self.updateEditor)
        y += L
        return y