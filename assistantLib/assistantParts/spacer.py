# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   spacer.py
#
#   TODO
#   - Auto sim spacing
#   - Sample line or buttons line for alternative spacing masters
#   - Kerning line
#   - Spacing and kerning keys
#   - Set Similarity zones
#
import sys
from math import *
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR
from assistantLib.assistantParts.data import * # Import anchors names

class KerningLineGlyphPosition:
    """Element that holds position and name of glyphs in the spacer/kerning line. This makes it easier 
    for mouseover to detect clicks on the line"""
    def __init__(self, name, x, y, w, h, k):
        self.name = name # Glyph name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.k = k # Kerning with previoud glyph

class AssistantPartSpacer(BaseAssistantPart):
    """The Spacer assistant part handles all margins and widths that can be automated.
    It makes guesses based on the names of glyphs, existing components, values in the MasterData
    and Erik van Blokland's Similarity.
    The assistant part gives feedback about where the automated values came from, so it's easier to debug.
    """

    KERN_LINE_SIZE = 40 # Number of glyphs on kerning line
    KERN_SCALE = 0.12 #0.2 Scaler for glyphs on kerning line

    SPACER_FIXED_WIDTH_MARKER_COLOR = 0.5, 0.5, 0.5, 0.5
    SPACER_FIXED_MARGIN_MARKER_COLOR = 0.8, 0.2, 0.4, 0.7
    SPACER_LABEL_SIZE = 18
    SPACER_MARKER_R = 22 # Radius of space marker

    def initMerzSpacer(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""

        #    K E R N I N G  L I N E
    
        self.spacerGlyphPositions = [] # Tuples (x, y, w, h, k, glyphName) Adjusted by the line lenght, to center on current glyph.width/2

        self.kerningLine = [] # List of kerned/spaced glyph image layers, also buttons
        self.kerningLineValues = [] # List of kerning value layers
        self.kerningLineNames = [] # List of glyph name layers
        self.kerningLineBoxes = [] # List of kerned glyph em-boxes
        self.kerningSelectedGlyph = None # Name of the glyph selected by the kerning editor
        
        for gIndex in range(self.KERN_LINE_SIZE):
            # Previewing current glyphs on left/right side.        
            im = self.backgroundContainer.appendPathSublayer(
                name='kernedGlyph-%d' % gIndex,
                position=(FAR, 0),
                fillColor=(0, 0, 0, 1),
            )
            im.addScaleTransformation(self.KERN_SCALE)
            self.kerningLine.append(im)
            
            kerningLineValue = self.backgroundContainer.appendTextLineSublayer(
                name='kernedValue-%d' % gIndex,
                position=(FAR, 0),
                text='xxx\nxxx',
                font='Courier',
                pointSize=16,
                fillColor=(0, 0, 0, 1), # Can be red (negative kerning) or green (positive kerning)
            )
            kerningLineValue.addScaleTransformation(self.KERN_SCALE)
            kerningLineValue.setHorizontalAlignment('center')
            self.kerningLineValues.append(kerningLineValue)

            kerningLineBox = self.backgroundContainer.appendRectangleSublayer(
                name='kernedBox-%d' % gIndex,
                position=(FAR, 0),
                size=(1, 1),
                fillColor=None,
                strokeColor=(0, 0, 0, 0.5),
                strokeWidth=1,
            )
            kerningLineBox.addScaleTransformation(self.KERN_SCALE)
            self.kerningLineBoxes.append(kerningLineBox)

            kerningLineName = self.backgroundContainer.appendTextLineSublayer(
                name='kernedName-%d' % gIndex,
                position=(FAR, 0),
                text='xxx\nxxx',
                font='Courier',
                pointSize=12,
                fillColor=(0.6, 0.6, 0.6, 1),
            )
            kerningLineName.addScaleTransformation(self.KERN_SCALE)
            self.kerningLineNames.append(kerningLineName)

        self.kerningSelectedGlyphMarker = self.backgroundContainer.appendRectangleSublayer(
            name='kerningSelectedGlyphMarker',
            position=(FAR, 0),
            size=(1, 20),
            fillColor=(1, 0, 0, 1),
            strokeColor=None,
            strokeWidth=1,
        )
        self.kerningSelectedGlyphMarker.addScaleTransformation(self.KERN_SCALE)

        self.kerning1Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning1Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning1Value.setHorizontalAlignment('center')
        self.kerning2Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning2Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning2Value.setHorizontalAlignment('center')

        self.kerningCursorBox = self.backgroundContainer.appendTextLineSublayer(
            name="kerningCursorBox",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=14,
            fillColor=(0.6, 0.6, 0.6, 1),
        )


        #   S P A C I N G  M A R K E R S

        self.fixedSpaceMarkerLeft = container.appendOvalSublayer(name="spaceMarkerLeft",
            position=(-self.SPACER_MARKER_R, -self.SPACER_MARKER_R),
            size=(self.SPACER_MARKER_R*2, self.SPACER_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.leftSpaceSourceLabel = container.appendTextLineSublayer(name="leftSpaceSourceLabel",
            position=(FAR, -self.SPACER_MARKER_R*2),
            text='LSB',
            font='Courier',
            pointSize=self.SPACER_LABEL_SIZE,
            fillColor=(0, 0, 0, 1),
        )
        self.leftSpaceSourceLabel.setHorizontalAlignment('center')
        
        self.fixedSpaceMarkerRight = container.appendOvalSublayer(name="spaceMarkerRight",
            position=(1000-self.SPACER_MARKER_R, -self.SPACER_MARKER_R),
            size=(self.SPACER_MARKER_R*2, self.SPACER_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.rightSpaceSourceLabel = container.appendTextLineSublayer(name="rightSpaceSourceLabel",
            position=(FAR, -self.SPACER_MARKER_R*2),
            text='RSB',
            font='Courier',
            pointSize=self.SPACER_LABEL_SIZE,
            fillColor=(0, 0, 0, 1),
        )
        self.rightSpaceSourceLabel.setHorizontalAlignment('center')

    def updateMerzSpacer(self, info):
        """Update the spacing/kerning sample line"""
        c = self.getController()
        if c.w.showSpacingSampleLine.get():
            g = info['glyph']
            self.updateMerzSpacerKerningLine(g)

    def updateMerzSpacerKerningLine(self, g):
        """Update the spacing/kerning/sample line for the current glyphs and its settings."""
        f = g.font

        x = 0 # Adjusted from the previous line calculation
        y = (f.info.descender - 300)/self.KERN_SCALE
        k = 0 # For now
        h = f.info.unitsPerEm

        km = self.getKerningManager(g.font)
        sample = km.getSpacingSample(g, len(self.kerningLine)) # Get a spacing sample for the right amount of glyphs

        # We need to do this in 2 runs, unfortunately, to center the line by its total width.
        for gIndex, kerningGlyphLayer in enumerate(self.kerningLine): # List of kerned glyph images
            spaceG = f[sample[gIndex]]
            kerningGlyphLayer.setFillColor((0, 0, 0, 1))
            kerningGlyphLayer.setPath(spaceG.getRepresentation("merz.CGPath"))
            self.spacerGlyphPositions.append(KerningLineGlyphPosition(g.name, x, y, spaceG.width, h, k))
            x += spaceG.width + k

        x = g.width/2 - x/2 + y * tan(radians(-f.info.italicAngle or 0))
        for gIndex, kerningGlyphLayer in enumerate(self.kerningLine):
            kerningGlyphLayer.setPosition((self.spacerGlyphPositions[gIndex].x + x, y))

    """
            kerningSrc = None
                            
            xLeft = int(c.w.kerningLeftX.get())      
            xo = x = xLeft/self.KERN_SCALE # Get left position of kerning samples
            y1 = 1.75*f.info.descender/self.KERN_SCALE # Glyph image position
            y3 = y1 + f.info.descender # Box position
            y2 = y3 - 100 # Kerning value position
            y4 = -150 # Position of current kerning values
            y6 = -250 # Position of kerning-cursor box

            start = kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            stop = start + self.KERN_LINE_SIZE
            prevName = None
            for gIndex, kerningGlyphLayer in enumerate(self.kerningLine): # List of kerned glyph images
                gName = km.sample[start + gIndex]
                if gName is not None and gName in f:
                    gKern = f[gName]
                    if gIndex == kerningSelectedIndex:
                        self.kerningSelectedGlyphMarker.setPosition((x + k, y2-100))
                        self.kerningSelectedGlyphMarker.setSize((gKern.width, 100))

                        if self.controller.w.showKerningFilled.get():
                            self.kernGlyphImage.setPath(gKern.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage.setPosition((0, 0))
                        else:
                            self.kernGlyphImage.setPosition((FAR, 0))
                        self.kernGlyphImage.setFillColor((0, 0, 0, 1))
                                            
                        if prevName is not None: # Kerning glyph on left side of current glyph

                            prev = f[prevName]
                            k, groupK, kerningType = km.getKerning(prevName, gKern.name) # Get the kerning from the groups of these glyphs
                            kSrcString = ''
                            self.kernGlyphImage1.setPath(prev.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage1.setPosition((-prev.width - k, 0))
                            if gName != g.name: # Other current glyph than selected in kerning line
                                #print(gName, prev.name, g.name)
                                gray = 0.4
                                self.kernGlyphImage2.setFillColor((gray, gray, gray, 0.7)) # Just show as light gray
                                self.kernGlyphImage.setFillColor((gray, gray, gray, 0.7)) # Just show as light gray
                                self.kernGlyphImage1.setFillColor((gray, gray, gray, 0.7)) # Just show as light gray
                            elif kerningType in (1, 2) and k != groupK: # Show that we are kerning group<-->glyph
                                if self.controller.w.showKerningLeftFilled.get():
                                    self.kernGlyphImage1.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage1.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage1.setFillColor(None)
                                    self.kernGlyphImage1.setStrokeColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GROUPGLYPH_COLOR)

                            elif kerningType == 3 and k != groupK: # Show that we are in kerning glyph<-->glyph
                                if self.controller.w.showKerningLeftFilled.get():
                                    self.kernGlyphImage1.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage1.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage1.setFillColor(None)
                                    self.kernGlyphImage1.setStrokeColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GLYPHGLYPH_COLOR)

                            elif self.controller.w.showKerningFilled.get():
                                self.kernGlyphImage1.setFillColor((0, 0, 0, 1))
                                self.kernGlyphImage1.setStrokeColor(None)

                            else:
                                self.kernGlyphImage1.setFillColor(None)
                                self.kernGlyphImage1.setStrokeColor(None)
                                
                            if kerningType in (1, 2):
                                self.kerning1Value.setFillColor(GROUPGLYPH_COLOR)
                            elif kerningType == 3:
                                self.kerning1Value.setFillColor(GLYPHGLYPH_COLOR)
                            elif k < 0:
                                self.kerning1Value.setFillColor((1, 0, 0, 1))
                            elif k > 0:
                                self.kerning1Value.setFillColor((0, 0.5, 0, 1))
                            else:
                                self.kerning1Value.setFillColor((0.6, 0.6, 0.6, 1))
                            self.kerning1Value.setPosition((-k, y4))
                            #if k != self.predictedKerning1:
                            #    predicted = f'\n({self.predictedKerning1})'
                            #else:
                            #    predicted = '' 
                            #if k != groupK: 
                            #    self.kerning1Value.setText('%d:G%d%s%s' % (k, groupK, kSrcString, predicted))
                            #else:
                            #    self.kerning1Value.setText('%d%s%s' % (k, kSrcString, predicted))
                            if k != groupK: 
                                self.kerning1Value.setText('%d:G%d%s' % (k, groupK, kSrcString))
                            else:
                                self.kerning1Value.setText('%d%s' % (k, kSrcString))
                                
                    elif gIndex == kerningSelectedIndex + 1: # Kerning glyph on right side of current glyph
                        if prevName is not None:  
                            prev = f[prevName]
                            k, groupK, kerningType = km.getKerning(prevName, gKern.name) # Get the kerning from the groups of these glyphs
                            kSrcString = ''
                            self.kernGlyphImage2.setPath(gKern.getRepresentation("merz.CGPath"))
                            self.kernGlyphImage2.setPosition((prev.width + k, 0))
                            if gName != g.name: # Other current glyph than selected in kerning line
                                gray = 0.4
                                self.kernGlyphImage2.setFillColor((gray, gray, gray, 0.7)) # Just show as light gray
                                self.kernGlyphImage.setFillColor((gray, gray, gray, 0.7)) # Just show as light gray
                                self.kernGlyphImage1.setFillColor((gray, gray, gray, 0.7)) # Just show as light gray
                            elif kerningType in (1, 2) and k != groupK: # Show that we are kerning group<-->glyph
                                if self.controller.w.showKerningRightFilled.get():
                                    self.kernGlyphImage2.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage2.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage2.setFillColor(None)
                                    self.kernGlyphImage2.setStrokeColor(GROUPGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GROUPGLYPH_COLOR)

                            elif kerningType == 3 and k != groupK: # Show that we are in kerning glyph<-->glyph
                                if self.controller.w.showKerningRightFilled.get():
                                    self.kernGlyphImage2.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage2.setStrokeColor(None)
                                    self.kernGlyphImage.setFillColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setStrokeColor(None)
                                else:
                                    self.kernGlyphImage2.setFillColor(None)
                                    self.kernGlyphImage2.setStrokeColor(GLYPHGLYPH_COLOR)
                                    self.kernGlyphImage.setFillColor(None)
                                    self.kernGlyphImage.setStrokeColor(GLYPHGLYPH_COLOR)

                            elif self.controller.w.showKerningFilled.get():
                                self.kernGlyphImage2.setFillColor((0, 0, 0, 1))
                                self.kernGlyphImage2.setStrokeColor(None)

                            else:
                                self.kernGlyphImage1.setFillColor(None)
                                self.kernGlyphImage1.setStrokeColor(None)
                                
                            if kerningType in (1,2):
                                self.kerning2Value.setFillColor(GROUPGLYPH_COLOR)
                            elif kerningType == 3:
                                self.kerning2Value.setFillColor(GLYPHGLYPH_COLOR)
                            elif k < 0:
                                self.kerning2Value.setFillColor((1, 0, 0, 1))
                            elif k > 0:
                                self.kerning2Value.setFillColor((0, 0.5, 0, 1))
                            else:
                                self.kerning2Value.setFillColor((0.6, 0.6, 0.6, 1))
                            self.kerning2Value.setPosition((prev.width + k, y4))
                            if k != self.predictedKerning2:
                                predicted = f'\n({self.predictedKerning2})'
                            else:
                                predicted = '' 
                            if k != groupK:        
                                self.kerning2Value.setText('%d:G%d%s%s' % (k, groupK, kSrcString, predicted))
                            else:
                                self.kerning2Value.setText('%d%s%s' % (k, kSrcString, predicted))

                    k = 0
                    if prevName is not None:
                        k, groupK, kerningType = km.getKerning(prevName, gName) # Get the kerning from the groups of these glyphs
                        if kerningType is not None:
                            kSrc = 0
                            kSrcString = ''
                            klv = self.kerningLineValues[gIndex] # List of kerning value layers
                            if k or kSrc:
                                klv.setPosition((x, y2))
                                if k != groupK:
                                    klv.setText('%d:G%d%s' % (k, groupK, kSrcString))
                                else:
                                    klv.setText('%d%s' % (k, kSrcString))
                                if kerningType in (1, 2) and k != groupK: # Other than group<-->group                            
                                    klv.setFillColor(GROUPGLYPH_COLOR)
                                elif kerningType == 3 and k != groupK: # Other than group<-->group                            
                                    klv.setFillColor(GLYPHGLYPH_COLOR)
                                elif k < 0:
                                    klv.setFillColor((1, 0, 0, 1))
                                elif k > 0:
                                    klv.setFillColor((0, 0.5, 0, 1))
                                else:
                                    klv.setFillColor((0.6, 0.6, 0.6, 1))
                            else:
                                klv.setPosition((FAR, y2))

                    kerningGlyphLayer.setFillColor((0, 0, 0, 1))
                    kerningGlyphLayer.setPath(gKern.getRepresentation("merz.CGPath"))
                    kerningGlyphLayer.setPosition((x + k, y1))
        
                    klb = self.kerningLineBoxes[gIndex]
                    if self.controller.w.showKerningBox.get():
                        klb.setPosition((x + k, y3))
                        klb.setSize((gKern.width, f.info.unitsPerEm))
                    else:
                        klb.setPosition((FAR, y3))
                        
                    x += gKern.width + k
                    prevName = gName
                    
            kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
            s = '%d/%d Pairs %d' % (kerningCursor/self.KERN_LINE_SIZE, len(km.sample)/self.KERN_LINE_SIZE, len(f.kerning))
            self.kerningCursorBox.setText(s)
            self.kerningCursorBox.setPosition((xLeft, 40)) # y6
        else:
            for kerningLine in self.kerningLine:
                kerningLine.setPosition((FAR, 0))
            for kerningLineValue in self.kerningLineValues:
                kerningLineValue.setPosition((FAR, 0))
            for kerningLineBox in self.kerningLineBoxes:
                kerningLineBox.setPosition((FAR, 0))
            self.kerningCursorBox.setPosition((FAR, 0))
            self.kernGlyphImage1.setPosition((FAR, 0))
            self.kernGlyphImage2.setPosition((FAR, 0))
            self.kerning1Value.setPosition((FAR, 0))
            self.kernGlyphImage.setPosition((FAR, 0))
            self.kerning2Value.setPosition((FAR, 0))

        kerningSelectedIndex = int(self.KERN_LINE_SIZE/2)
        kerningCursor = int(round(self.controller.w.kerningSampleSelectSlider.get()))
        self.kernGlyph1 = km.sample[kerningCursor + kerningSelectedIndex - 1]
        self.kernGlyph2 = km.sample[kerningCursor + kerningSelectedIndex + 1]

        # Update the groups lists for the new current glyph
        self.group1TextLeftLayer.setText('\n'.join(sorted(km.glyphName2Group1.get(self.kernGlyph1, []))))
        self.group2TextLeftLayer.setText('\n'.join(sorted(km.glyphName2Group2.get(g.name, []))))
        self.group1TextRightLayer.setText('\n'.join(sorted(km.glyphName2Group1.get(g.name, []))))
        self.group2TextRightLayer.setText('\n'.join(sorted(km.glyphName2Group2.get(self.kernGlyph2, []))))

        if self.controller.w.showKerningLists.get():
            self.group1TextLeftLayer.setPosition((-g.width-2*self.groupTextLayer_colW, 0))
            self.group2TextLeftLayer.setPosition((-g.width-self.groupTextLayer_colW, 0))
            self.group1TextRightLayer.setPosition((g.width*2+self.groupTextLayer_colW, 0)) # Some extra on the right, in case of italics
            self.group2TextRightLayer.setPosition((g.width*2+2*self.groupTextLayer_colW, 0))
        else:
            self.group1TextLeftLayer.setPosition((FAR, 0))
            self.group2TextLeftLayer.setPosition((FAR, 0))
            self.group1TextRightLayer.setPosition((FAR, 0))
            self.group2TextRightLayer.setPosition((FAR, 0))
        """

    def updateSpacer(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width.
        Answer the boolean flag if something was changed to the glyph."""
        changed = False
        g = info['glyph']
        if g is None:
            return changed # Nothing changed.
        
        changed |= self.checkFixGlyphLeftMargin(g)
        changed |= self.checkFixGlyphRightMargin(g)
        changed |= self.checkFixGlyphWidth(g)
        
        return changed

    KEY_CENTER_GLYPH = '='
    KEY_INC_RIGHT_MARGIN_CAP = 'P'
    KEY_INC_RIGHT_MARGIN = 'p'
    KEY_DEC_RIGHT_MARGIN_CAP = 'O'
    KEY_DEC_RIGHT_MARGIN = 'o'
    KEY_INC_LEFT_MARGIN_CAP = 'I'
    KEY_INC_LEFT_MARGIN = 'i'
    KEY_DEC_LEFT_MARGIN_CAP = 'U'
    KEY_DEC_LEFT_MARGIN = 'u'

    def buildSpacer(self, y):
        """Build the assistant UI for anchor controls."""
        personalKey_eq = self.registerKeyStroke(self.KEY_CENTER_GLYPH, 'spacerCenterGlyph')

        personalKey_U = self.registerKeyStroke(self.KEY_DEC_LEFT_MARGIN_CAP, 'spacerDecLeftMarginCap')
        personalKey_u = self.registerKeyStroke(self.KEY_DEC_LEFT_MARGIN, 'spacerDecLeftMargin')
        personalKey_I = self.registerKeyStroke(self.KEY_INC_LEFT_MARGIN_CAP, 'spacerIncLeftMarginCap')
        personalKey_i = self.registerKeyStroke(self.KEY_INC_LEFT_MARGIN, 'spacerIncLeftMargin')

        personalKey_O = self.registerKeyStroke(self.KEY_DEC_RIGHT_MARGIN_CAP, 'spacerDecRightMarginCap')
        personalKey_o = self.registerKeyStroke(self.KEY_DEC_RIGHT_MARGIN, 'spacerDecRightMargin')
        personalKey_P = self.registerKeyStroke(self.KEY_INC_RIGHT_MARGIN_CAP, 'spacerIncRightMarginCap')
        personalKey_p = self.registerKeyStroke(self.KEY_INC_RIGHT_MARGIN, 'spacerIncRightMargin')

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
        c.w.simSpace = CheckBox((C0, y, CW, L), 'Similar space', value=False, sizeStyle='small')
        c.w.autoSpace = CheckBox((C1, y, CW, L), 'Auto space', value=True, sizeStyle='small')
        c.w.centerGlyphButton = Button((C2, y, CW, L), 'Center width [%s]' % personalKey_eq, callback=self.spacerCenterGlyphCallback)
        y += L
        c.w.splitSimScripts = CheckBox((C0, y, CW, L), 'Split Sim scripts', value=True, sizeStyle='small')
        c.w.showSpacingSampleLine = CheckBox((C1, y, CW, L), 'Show sample line', value=True, sizeStyle='small')
        
        c.w.decLeftMarginButton = Button((C2, y, CW/4, L), '<[%s]' % personalKey_u, callback=self.spacerDecLeftMarginCallback)
        c.w.incLeftMarginButton = Button((C2+CW/4, y, CW/4, L), '[%s]>' % personalKey_i, callback=self.spacerIncLeftMarginCallback)
        c.w.decRightMarginButton = Button((C2+2*CW/4, y, CW/4, L), '<[%s]' % personalKey_o, callback=self.spacerDecRightMarginCallback)
        c.w.incRightMarginButton = Button((C2+3*CW/4, y, CW/4, L), '[%s]>' % personalKey_p, callback=self.spacerIncRightMarginCallback)
        y += L + LL

        return y

    #   S P A C I N G | K E R N I N G  K E Y S

    def spacerDecLeftMarginCallback(self, sender):
        self._adjustLeftMargin(g, -1)
        g.changed()

    def spacerIncLeftMarginCallback(self, sender):
        self._adjustLeftMargin(g, 1)
        g.changed()

    def spacerDecRightMarginCallback(self, sender):
        self._adjustRightMargin(g, -1)
        g.changed()

    def spacerIncRightMarginCallback(self, sender):
        self._adjustRightMargin(g, 1)
        g.changed()


    def spacerDecLeftMarginCap(self, g, c, event):
        self._adjustLeftMargin(g, -5)
        g.changed()

    def spacerDecLeftMargin(self, g, c, event):
        self._adjustLeftMargin(g, -1)
        g.changed()

    def spacerIncLeftMarginCap(self, g, c, event):
        self._adjustLeftMargin(g, 5)
        g.changed()

    def spacerIncLeftMargin(self, g, c, event):
        self._adjustLeftMargin(g, 1)
        g.changed()

    def spacerDecRightMarginCap(self, g, c, event):
        self._adjustRightMargin(g, -5)
        g.changed()

    def spacerDecRightMargin(self, g, c, event):
        self._adjustRightMargin(g, -1)
        g.changed()

    def spacerIncRightMarginCap(self, g, c, event):
        self._adjustRightMargin(g, 5)
        g.changed()

    def spacerIncRightMargin(self, g, c, event):
        self._adjustRightMargin(g, 1)
        g.changed()

    #    A D J U S T  S P A C I N G

    SPACING_UNIT = 4

    def _adjustLeftMargin(self, g, value): # This moved to TYPETR-Assistants/KerningAssistant-005.py
        if self.isUpdating:
            return
        f = g.font        
        g.angledLeftMargin = int(round(g.angledLeftMargin/self.SPACING_UNIT) + value) * self.SPACING_UNIT
                          
    def _adjustRightMargin(self, g, value): # This moved to TYPETR-Assistants/KerningAssistant-005.py
        if self.isUpdating:
            return
        f = g.font
        g.angledRightMargin = int(round(g.angledRightMargin/self.SPACING_UNIT) + value) * self.SPACING_UNIT

    """
        #    K E R N I N G

        elif characters in '.>': # Increment right kerning
            if shiftDown:
                self._adjustRightKerning(g, 5) # 20
            else:
                self._adjustRightKerning(g, 1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in ',<': # Decrement right kerning
            if shiftDown:
                self._adjustRightKerning(g, -5) # 20
            else:
                self._adjustRightKerning(g, -1) # 4
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Mm': # Decrement left kerning
            if shiftDown:
                self._adjustLeftKerning(g, -5) # 20
            else:
                self._adjustLeftKerning(g, -1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        
        elif characters in 'Nn': # Increment left kerning
            if shiftDown:
                self._adjustLeftKerning(g, 5) # 20
            else:
                self._adjustLeftKerning(g, 1) # 4           
            changed |= self.checkSpacingDependencies(g) # Update the spacing consistency for all glyphs in the kerning line
        """

    #   G U E S S  S P A C I N G  &  K E R N I N G

    def _fixGlyphWidth(self, g, width):
        if g.width != width:
            print(f'... Fix glyph width: Set /{g.name} width from {g.width} to {width}')
            g.width = width
            return True
        return False

    def _fixGlyphLeftMargin(self, g, lm):
        if abs(g.angledLeftMargin - lm) >= 1:
            print(f'... Fix left margin: Set /{g.name} from {g.angledLeftMargin} to {lm}')
            g.angledLeftMargin = lm
            return True
        return False

    def _fixGlyphRightMargin(self, g, rm):
        if abs(g.angledRightMargin - rm) >= 1:
            print(f'... Fix left margin: Set /{g.name} from {g.angledRightMargin} to {rm}')
            g.angledRightMargin = rm
            return True
        return False

    def checkFixGlyphWidth(self, g, km=None):
        """Use the KerningManager for the current font to determine the best width for this glyph.
        Check if this glyph should have its width altered. If it has components, then fix those first.
        If something changed, then answer True. 
        """
        changed = False
        if km is None:
            km = self.getKerningManager(g.font)

        label = ''
        color = 0, 0, 0, 0
    
        width = km.getWidth(g)
        if width is not None:
            changed = self._fixGlyphWidth(g, width)
            label = 'Width=%d' % g.width
            color = self.SPACER_FIXED_WIDTH_MARKER_COLOR

        self.fixedSpaceMarkerRight.setPosition((g.width - self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setPosition((g.width, -self.SPACER_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setText(label)

        return changed

    def checkFixGlyphLeftMargin(self, g, km=None):
        """Use the KerningManager for the current font to determine the best left margin for this glyph.
        Check if this glyph should have its left margin altered. If it has components, then fix those first.
        If something changed, then answer True. 
        """
        c = self.getController()
        changed = False
        if km is None:
            km = self.getKerningManager(g.font)

        label = ''
        color = 0, 0, 0, 0

        if c.w.simSpace.get():
            km.simSameCategory = km.simSameScript = not c.w.splitSimScripts.get()
            similar2 = km.getSimilarMargins2(g)
            print('Similar left', similar2)

        lm = km.getLeftMargin(g)
        if lm is not None:
            changed = self._fixGlyphLeftMargin(g, lm)
            label = 'Left=%d' % g.width
            color = self.SPACER_FIXED_MARGIN_MARKER_COLOR

        self.fixedSpaceMarkerLeft.setPosition((-self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setPosition((0, -self.SPACER_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setText(label)

        return changed

    def checkFixGlyphRightMargin(self, g, km=None):
        """Use the KerningManager for the current font to determine the best roght margin for this glyph. 
        Check if this glyph should have its right margin altered. If it has components, then fix those first.
        If something changed, then answer True. 
        """
        c = self.getController()
        changed = False
        km = self.getKerningManager(g.font)

        label = ''
        color = 0, 0, 0, 0

        if c.w.simSpace.get():
            km.simSameCategory = km.simSameScript = not c.w.splitSimScripts.get()
            similar1 = km.getSimilarMargins1(g)
            print('Similar right', similar1)
        
        rm = km.getRightMargin(g)
        if rm is not None:
            changed = self._fixGlyphRightMargin(g, rm)
            label = 'Right=%d' % g.width
            color = self.SPACER_FIXED_MARGIN_MARKER_COLOR

        self.fixedSpaceMarkerLeft.setPosition((-self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setPosition((0, -self.SPACER_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setText(label)

        ##### FOR NOW
        # Add rightmargin stuff here

        return changed
    
    def spacerCenterGlyphCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            if self.spacerCenterGlyhph(g):
                g.changed()

    def spacerCenterGlyph(self, g, c, event):     
        """Snap the selected points of the current glyph onto points that are within range on the background glyph."""
        changed = False
        lm = g.angledLeftMargin
        rm = g.angledRightMargin
        w = g.width
        if lm is not None:
            g.angledLeftMargin = (lm + rm)/2
            g.width = w
            changed = True

        return changed
