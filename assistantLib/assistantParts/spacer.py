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

from mojo.UI import OpenGlyphWindow

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.data import * # Import anchors names

class KerningLineGlyphPosition:
    """Element that holds position and name of glyphs in the spacer/kerning line. This makes it easier 
    for mouseover to detect clicks on the line"""
    def __init__(self, glyph, x, y, w, h, k, fillColor):
        self.glyph = glyph # RGlyph object 
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.k = k # Kerning with previoud glyph
        self.fillColor = fillColor

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

    SPACER_LABEL_FONT = 'Verdana'
    SPACER_LABEL_SIZE = 10

    SPACER_FILL_COLOR = 0.2, 0.2, 0.2, 1 # Default color
    SPACER_SELECTED_COLOR = 0.2, 0.2, 0.5, 1 # Current glyph
    SPACER_HOVER_COLOR = 1, 0, 0, 1 # Mouse goes over the element
    SPACER_LINE_BOX_COLOR = 0, 0, 0, 0.5 # Stroke color of space box

    def initMerzSpacer(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""

        #    K E R N I N G  L I N E
    
        self.spacerGlyphPositions = [] # Tuples (x, y, w, h, k, glyphName) Adjusted by the line lenght, to center on current glyph.width/2

        self.kerningLine = [] # List of kerned/spaced glyph image layers, also buttons
        self.kerningLineValues = [] # List of kerning value layers
        self.kerningLineNames = [] # List of glyph name layers
        self.kerningLineBoxes = [] # List of kerned glyph em-boxes
        self.kerningSelectedGlyph = None # Name of the glyph selected by the kerning editor

        # White rectangle as background of spacer/kerning line
        self.spacerWhiteBackground = container.appendRectangleSublayer(name="spacesWhiteBackground",
            position=(0, 0),
            size=(1, 1),
            fillColor=(1, 1, 1, 1),
            visible=False,
        )
        self.spacerWhiteBackground.addScaleTransformation(self.KERN_SCALE)
        
        # Glyphs cells on the spacer/kerning line

        for gIndex in range(self.KERN_LINE_SIZE):
            # Previewing current glyphs on left/right side.        
            im = container.appendPathSublayer(
                name='kernedGlyph-%d' % gIndex,
                position=(0, 0),
                fillColor=self.SPACER_FILL_COLOR,
                visible=False,
            )
            im.addScaleTransformation(self.KERN_SCALE)
            self.kerningLine.append(im)
            
            kerningLineValue = container.appendTextLineSublayer(
                name='kernedValue-%d' % gIndex,
                position=(0, 0),
                text='xxx\nxxx',
                font=self.SPACER_LABEL_FONT,
                pointSize=self.SPACER_LABEL_SIZE,
                fillColor=self.SPACER_FILL_COLOR, # Can be red (negative kerning) or green (positive kerning)
                visible=False,
            )
            kerningLineValue.addScaleTransformation(self.KERN_SCALE)
            kerningLineValue.setHorizontalAlignment('center')
            self.kerningLineValues.append(kerningLineValue)

            kerningLineBox = container.appendRectangleSublayer(
                name='kernedBox-%d' % gIndex,
                position=(0, 0),
                size=(1, 1),
                fillColor=None,
                strokeColor=self.SPACER_LINE_BOX_COLOR,
                strokeWidth=1,
                visible=False,
            )
            kerningLineBox.addScaleTransformation(self.KERN_SCALE)
            self.kerningLineBoxes.append(kerningLineBox)

            kerningLineName = container.appendTextLineSublayer(
                name='kernedName-%d' % gIndex,
                position=(0, 0),
                text='xxx\nxxx',
                font=self.SPACER_LABEL_FONT,
                pointSize=self.SPACER_LABEL_SIZE,
                fillColor=self.SPACER_FILL_COLOR, # Default line glyph color
                visible=False,
            )
            kerningLineName.addScaleTransformation(self.KERN_SCALE)
            kerningLineName.setHorizontalAlignment('center')
            self.kerningLineNames.append(kerningLineName)

        self.kerningSelectedGlyphMarker = container.appendRectangleSublayer(
            name='kerningSelectedGlyphMarker',
            position=(0, 0),
            size=(1, 20),
            fillColor=(1, 0, 0, 1),
            strokeColor=None,
            strokeWidth=1,
            visible=False,
        )
        self.kerningSelectedGlyphMarker.addScaleTransformation(self.KERN_SCALE)

        self.kerning1Value = container.appendTextLineSublayer(
            name="kerning1Value",
            position=(0, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
            visible=False,
        )
        self.kerning1Value.setHorizontalAlignment('center')
        self.kerning2Value = container.appendTextLineSublayer(
            name="kerning2Value",
            position=(0, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
            visible=False,
        )
        self.kerning2Value.setHorizontalAlignment('center')

        self.kerningCursorBox = container.appendTextLineSublayer(
            name="kerningCursorBox",
            position=(0, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=14,
            fillColor=(0.6, 0.6, 0.6, 1),
            visible=False,
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
            position=(0, -self.SPACER_MARKER_R*2),
            text='LSB',
            font='Courier',
            pointSize=self.SPACER_LABEL_SIZE,
            fillColor=(0, 0, 0, 1),
            visible=False,
        )
        self.leftSpaceSourceLabel.setHorizontalAlignment('center')
        
        self.fixedSpaceMarkerRight = container.appendOvalSublayer(name="spaceMarkerRight",
            position=(1000-self.SPACER_MARKER_R, -self.SPACER_MARKER_R),
            size=(self.SPACER_MARKER_R*2, self.SPACER_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
            visible=False,
        )
        self.rightSpaceSourceLabel = container.appendTextLineSublayer(name="rightSpaceSourceLabel",
            position=(0, -self.SPACER_MARKER_R*2),
            text='RSB',
            font='Courier',
            pointSize=self.SPACER_LABEL_SIZE,
            fillColor=(0, 0, 0, 1),
            visible=False,
        )
        self.rightSpaceSourceLabel.setHorizontalAlignment('center')

    def updateMerzSpacer(self, info):
        """Update the spacing/kerning sample line"""
        c = self.getController()
        g = info['glyph']
        if g is None:
            return 
        if c.w.showSpacingSampleLine.get():
            self.updateMerzSpacerKerningLine(g)
        else:
            self.hideMerzSpacerKerningLine()
            g.changed()

    def hideMerzSpacerKerningLine(self):
        for kerningGlyphLayer in self.kerningLine:
            kerningGlyphLayer.setVisible(False)
        for kerningNameLayer in self.kerningLineNames:
            kerningNameLayer.setVisible(False)
        self.spacerWhiteBackground.setVisible(False)

    def updateMerzSpacerKerningLine(self, g):
        """Update the spacing/kerning/sample line for the current glyphs and its settings."""
        c = self.getController()
        f = g.font

        h = f.info.unitsPerEm
        m = h/5 # Margin around white rectangle.
        x = 0 # Adjusted from the previous line calculation
        y = (f.info.descender - 1.5*m)/self.KERN_SCALE
        k = 0 # For now

        visible = c.w.showSpacingSampleLine.get()

        km = self.getKerningManager(g.font)
        sampleContext = c.w.spacerMode.get()
        # 0    Glyphset
        # 1    According to similarity
        # 2    Byt group mode context
        # 3    By spacing mode context
        # 4    By kerning mode context
        # Get a spacing sample for the right amount of glyphs for the selected context
        sample = km.getSpacingSample(g, context=sampleContext, length=len(self.kerningLine)) 

        self.spacerGlyphPositions = [] # Reset the list of KerningLineGlyphPosition instances.

        # We need to do this in 2 runs unfortunately, constructing the list of spacerGlyphPositions first,
        # in order to center the line by its total width.
        for gIndex, kerningGlyphLayer in enumerate(self.kerningLine): # List of kerned glyph images
            spaceG = f[sample[gIndex]]
            if g.name == spaceG.name:
                color = self.SPACER_SELECTED_COLOR
            else:
                color = self.SPACER_FILL_COLOR
            self.spacerGlyphPositions.append(KerningLineGlyphPosition(spaceG, x, y, spaceG.width, h, k, color))
            x += spaceG.width + k

        gpFirst = self.spacerGlyphPositions[0]
        gpLast = self.spacerGlyphPositions[-1]

        offsetX = g.width/2/self.KERN_SCALE - (gpLast.x - gpFirst.x)/2 + y * tan(radians(-f.info.italicAngle or 0))

        self.spacerWhiteBackground.setPosition((gpFirst.x + offsetX - 2*m, y + f.info.descender - m))
        self.spacerWhiteBackground.setSize((gpLast.x - gpFirst.x + gpLast.w + 4*m, h + 2*m))
        self.spacerWhiteBackground.setVisible(True)

        for gIndex, kerningGlyphLayer in enumerate(self.kerningLine):
            gp = self.spacerGlyphPositions[gIndex]
            
            if self.mouseMovePoint is not None and gp.x <= self.mouseMovePoint.x/self.KERN_SCALE <= gp.x + gp.y:
                color = self.SPACER_HOVER_COLOR
            else:
                color = gp.fillColor 
            kerningGlyphLayer.setFillColor(color)
            kerningGlyphLayer.setPath(gp.glyph.getRepresentation("merz.CGPath"))
            kerningGlyphLayer.setPosition((gp.x + offsetX, y))
            kerningGlyphLayer.setVisible(visible)

            kerningNameLayer = self.kerningLineNames[gIndex]
            kerningNameLayer.setFillColor(color)
            kerningNameLayer.setText(gp.glyph.name)
            kerningNameLayer.setPosition((gp.x + offsetX + gp.w/2, y + f.info.descender))
            kerningNameLayer.setVisible(False) # Will be shown on mouse over hover

    def mouseMoveSpacer(self, g, x, y):
        """Set the hoover color for the current selected glyph"""
        if g is None or not self.spacerGlyphPositions or self.mouseMovePoint is None:
            return

        gpFirst = self.spacerGlyphPositions[0]
        gpLast = self.spacerGlyphPositions[-1]
        offsetX = g.width/2/self.KERN_SCALE - (gpLast.x - gpFirst.x)/2# + y * tan(radians(-g.font.info.italicAngle or 0))

        sx = x/self.KERN_SCALE - offsetX
        sy = y/self.KERN_SCALE

        for gIndex, gp in enumerate(self.spacerGlyphPositions):
            #print(gp.x, sx, gp.x + gp.w)
            if gp.x <= sx <= gp.x + gp.w and gp.y - gp.h <= sy <= gp.y + gp.h:
                color = self.SPACER_HOVER_COLOR
                visible = True
            elif gp.glyph.name == g.name:
                color = self.SPACER_SELECTED_COLOR
                visible = False
            else:
                color = self.SPACER_FILL_COLOR
                visible = False
            self.kerningLineNames[gIndex].setFillColor(color)
            self.kerningLine[gIndex].setFillColor(color)
            self.kerningLineNames[gIndex].setVisible(visible)
        return
                    
    def mouseDownSpacer(self, g, x, y):
        """Open Editor window on clicked glyph"""
        if g is None or not self.spacerGlyphPositions or self.mouseMovePoint is None:
            return

        gpFirst = self.spacerGlyphPositions[0]
        gpLast = self.spacerGlyphPositions[-1]
        offsetX = g.width/2/self.KERN_SCALE - (gpLast.x - gpFirst.x)/2# + y * tan(radians(-g.font.info.italicAngle or 0))

        sx = x/self.KERN_SCALE - offsetX
        sy = y/self.KERN_SCALE

        for gIndex, gp in enumerate(self.spacerGlyphPositions):
            #print(gp.x, sx, gp.x + gp.w)
            if gp.x <= sx <= gp.x + gp.w and gp.y - gp.h <= sy <= gp.y + gp.h:
                OpenGlyphWindow(glyph=gp.glyph, newWindow=False)
                break
        return

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

    KEY_INC_KERN2_CAP = '>'
    KEY_INC_KERN2 = '.'
    KEY_DEC_KERN2_CAP = '<'
    KEY_DEC_KERN2 = ','
    KEY_INC_KERN1_CAP = 'M'
    KEY_INC_KERN1 = 'm'
    KEY_DEC_KERN1_CAP = 'N'
    KEY_DEC_KERN1 = 'n'

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

        personalKey_larger = self.registerKeyStroke(self.KEY_INC_KERN2_CAP, 'spacerDecKern2Cap')
        personalKey_period = self.registerKeyStroke(self.KEY_INC_KERN2, 'spacerDecKern2')
        personalKey_smaller = self.registerKeyStroke(self.KEY_DEC_KERN2_CAP, 'spacerIncKern2Cap')
        personalKey_comma = self.registerKeyStroke(self.KEY_DEC_KERN2, 'spacerIncKern2')

        personalKey_M = self.registerKeyStroke(self.KEY_INC_KERN1_CAP, 'spacerDecKern1Cap')
        personalKey_m = self.registerKeyStroke(self.KEY_INC_KERN1, 'spacerDecKern1')
        personalKey_N = self.registerKeyStroke(self.KEY_DEC_KERN1_CAP, 'spacerIncKern1Cap')
        personalKey_n = self.registerKeyStroke(self.KEY_DEC_KERN1, 'spacerIncKern1')

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
        y += L
        c.w.spacerMode = RadioGroup((C0, y, 2*CW, L), ('Glyphs', 'Similar', 'Group', 'Space', 'Kern'), isVertical=False, sizeStyle='small', callback=self.updateEditor)
        c.w.spacerMode.set(3)
        #c.w.decKern2Button = Button((C2, y, CW/4, L), '<[%s]' % personalKey_m, callback=self.spacerDecKern2Callback)
        #c.w.incKern2Button = Button((C2+CW/4, y, CW/4, L), '[%s]>' % personalKey_n, callback=self.spacerIncKern2Callback)
        #c.w.decKern1Button = Button((C2+2*CW/4, y, CW/4, L), '<[%s]' % personalKey_period, callback=self.spacerDecKern1Callback)
        #c.w.incKern1Button = Button((C2+3*CW/4, y, CW/4, L), '[%s]>' % personalKey_comma, callback=self.spacerIncKern1Callback)
        y += L + LL

        return y

    #   S P A C I N G  K E Y S

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

    #   K E R N I N G  K E Y S

    def spacerDecKern2Callback(self, sender):
        self._adjustLeftMargin(g, -1)
        g.changed()

    def spacerIncKern2Callback(self, sender):
        self._adjustLeftMargin(g, 1)
        g.changed()

    def spacerDecKern1Callback(self, sender):
        self._adjustRightMargin(g, -1)
        g.changed()

    def spacerIncKern1Callback(self, sender):
        self._adjustRightMargin(g, 1)
        g.changed()


    def spacerDecKern2Cap(self, g, c, event):
        self._adjustLeftMargin(g, -5)
        g.changed()

    def spacerDecKern2(self, g, c, event):
        self._adjustLeftMargin(g, -1)
        g.changed()

    def spacerIncKern2Cap(self, g, c, event):
        self._adjustLeftMargin(g, 5)
        g.changed()

    def spacerIncKern2(self, g, c, event):
        self._adjustLeftMargin(g, 1)
        g.changed()

    def spacerDecKern1Cap(self, g, c, event):
        self._adjustRightMargin(g, -5)
        g.changed()

    def spacerDecKern1(self, g, c, event):
        self._adjustRightMargin(g, -1)
        g.changed()

    def spacerIncKern1Cap(self, g, c, event):
        self._adjustRightMargin(g, 5)
        g.changed()

    def spacerIncKern1(self, g, c, event):
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
