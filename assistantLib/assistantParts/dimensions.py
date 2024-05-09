# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   dimensions.py
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

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.data import * # Import anchors names

MAX_LINES = 80
MAX_MEASURES = 50

class AssistantPartDimensions(BaseAssistantPart):
    """The Dimensions assistant part calculates relevant measures in the glyph and shows them on the side. 
    In the case of diagonals, it shows the distances inside diagonal stems.
    """
    DIMENSIONS_LINES_STROKE_WIDTH = 1
    DIMENSIONS_LINES_COLOR = (0, 0, 0, 0.5)
    DIMENSIONS_VALUE_COLOR = (0, 0, 0, 0.8)
    DIMENSIONS_LABEL_FONT = 'Verdana'
    DIMENSIONS_LABEL_SIZE = 12

    DIMENSIONS_DIAGONAL_MARKER_COLOR = (1, 1, 1, 0.25)
    DIMENSIONS_DIAGONAL_MARKER_ERROR_COLOR = (1, 1, 0, 0.4)

    DIMENSIONS_MARKER_R = 24 # Radius or marker circle behind diagonal labels
    STEM_TOLERANCE = 2 # Tolerance for stems to show as 

    def initMerzDimensions(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        self.dimensionsHorizontalBarLines = []
        self.dimensionsBarMeasures = []
        self.dimensionsBarMeasureValues = []
        self.dimensionsVerticalStemLines = []
        self.dimensionsStemMeasures = []
        self.dimensionsStemMeasureValues = []
        self.dimensionsDiagonalMeasureLine1 = [] # Lines left of diagonal marker
        self.dimensionsDiagonalMeasureLine2 = [] # Lines right of diagonal marker
        self.dimensionsDiagonalMeasureValues = []
        self.dimensionsDiagonalMeasureBackground = []

        for n in range(MAX_LINES):
            self.dimensionsHorizontalBarLines.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
        for n in range(MAX_MEASURES):
            self.dimensionsBarMeasures.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            self.dimensionsBarMeasureValues.append(container.appendTextLineSublayer(
                position=(0, 0),
                text='',
                fillColor=self.DIMENSIONS_VALUE_COLOR,
                horizontalAlignment="center",
                font=self.DIMENSIONS_LABEL_FONT,
                pointSize=self.DIMENSIONS_LABEL_SIZE,
                visible=False,
            ))

        for n in range(MAX_LINES):
            self.dimensionsVerticalStemLines.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
        for n in range(MAX_MEASURES):
            self.dimensionsStemMeasures.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            self.dimensionsStemMeasureValues.append(container.appendTextLineSublayer(
                position=(0, 0),
                text='',
                fillColor=self.DIMENSIONS_VALUE_COLOR,
                horizontalAlignment="center",
                font=self.DIMENSIONS_LABEL_FONT,
                pointSize=self.DIMENSIONS_LABEL_SIZE,
                visible=False,
            ))

        for n in range(MAX_MEASURES):
            # Left of marker circle
            self.dimensionsDiagonalMeasureLine1.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            # Right of marker circle
            self.dimensionsDiagonalMeasureLine2.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            self.dimensionsDiagonalMeasureBackground.append(container.appendOvalSublayer(
                position=(0, 0),
                size=(self.DIMENSIONS_MARKER_R*2, self.DIMENSIONS_MARKER_R*2),
                fillColor=self.DIMENSIONS_DIAGONAL_MARKER_COLOR,
                strokeColor=None,
                visible=False,
            ))
            self.dimensionsDiagonalMeasureValues.append(container.appendTextLineSublayer(
                position=(0, 0),
                text='',
                fillColor=self.DIMENSIONS_VALUE_COLOR,
                horizontalAlignment="center",
                font=self.DIMENSIONS_LABEL_FONT,
                pointSize=self.DIMENSIONS_LABEL_SIZE,
                visible=False,
            ))



    def updateMerzDimensions(self, info):
        changed = False
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed to the glyph
        return changed

    def updateDimensions(self, info):
        """If the checkbox is set, then show relevant measures of stem and bars."""
        changed = False
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed to the glyph
        self.updateGlyphDimensions(g)
        return changed

    def mouseMoveDimensions(self, g, x, y):
        pass 

    def mouseDownDimensions(self, g, x, y):
        pass 
        
    def mouseUpDimensions(self, g, x, y):
        pass 

    def setGlyphDimensions(self, g):
        """The editor selected another glyph."""
        self.updateGlyphDimensions(g)

    def updateGlyphDimensions(self, g):
        c = self.getController()
        dIndex = 0
        if c.w.showDimensions.get():
            ga = self.getGlyphAnalyzer(g)
            gd = self.getGlyphData(g)
            md = self.getMasterData(g.font)
            for dy, bars in sorted(ga.bars.items()):
                for bar in bars:
                    pass
                    #print('Bar', dy, bar)
            #print('@@@ updateGlyphDimensions Bars:', ga.diagonalBars)
            for dx, stems in sorted(ga.stems.items()):
                for stem in stems:
                    pass
                    #print('Stem', dx, stem)
            #print('@@@ updateGlyphDimensions Stems:', ga.diagonalStems)
            for dxy, diagonals in sorted(ga.diagonals.items()):
                for diagonal in diagonals:
                    pass
                    #print('Diagonal', dxy, diagonal)

            containerScale = self.dimensionsDiagonalMeasureBackground[dIndex].getContainer().getContainerScale()
            # TODO: Solve the scale of the marker circle
            r = self.DIMENSIONS_MARKER_R #* containerScale

            for dxy, p0, p1 in ga.dValues:
                dxy = int(round(dxy))
                if dxy == 0 or dxy > md.HStem * 1.5: # Probably not a diagonal stem, ignore.
                    continue

                dx = (p1.x - p0.x) * r / dxy
                dy = (p1.y - p0.y) * r / dxy

                x = p0.x + (p1.x - p0.x)/2
                y = p0.y + (p1.y - p0.y)/2

                # Left side of marker, make line not strike through the transparant marker.
                self.dimensionsDiagonalMeasureLine1[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureLine1[dIndex].setStartPoint((p0.x, p0.y))
                self.dimensionsDiagonalMeasureLine1[dIndex].setEndPoint((x - dx, y - dy))

                # Right size of marker
                self.dimensionsDiagonalMeasureLine2[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureLine2[dIndex].setStartPoint((x + dx, y + dy))
                self.dimensionsDiagonalMeasureLine2[dIndex].setEndPoint((p1.x, p1.y))

                if gd.isLower:
                    targetStem = md.nStem
                else:
                    targetStem = md.HStem

                if abs(dxy - targetStem) >= md.diagonalTolerance: # In case out of bounds, then use other marker color
                    markerColor = self.DIMENSIONS_DIAGONAL_MARKER_ERROR_COLOR
                else:
                    markerColor = self.DIMENSIONS_DIAGONAL_MARKER_COLOR

                self.dimensionsDiagonalMeasureBackground[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureBackground[dIndex].setSize((r*2, r*2))
                self.dimensionsDiagonalMeasureBackground[dIndex].setPosition((x - r, y - r))
                self.dimensionsDiagonalMeasureBackground[dIndex].setFillColor(markerColor)

                self.dimensionsDiagonalMeasureValues[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureValues[dIndex].setText(str(dxy))
                self.dimensionsDiagonalMeasureValues[dIndex].setPosition((x, y + self.DIMENSIONS_LABEL_SIZE + 2))

                dIndex += 1
                if dIndex >= MAX_MEASURES:
                    break

        else: # Not showing dimension merz objects
            pass

        for n in range(dIndex, MAX_MEASURES):
            self.dimensionsDiagonalMeasureLine1[n].setVisible(False)
            self.dimensionsDiagonalMeasureLine2[n].setVisible(False)
            self.dimensionsDiagonalMeasureValues[n].setVisible(False)
            self.dimensionsDiagonalMeasureBackground[n].setVisible(False)

    def buildDimensions(self, y):
        """Build the assistant UI for guidelines controls."""
        #personalKey = self.registerKeyStroke('±', 'makeGuidelines')

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.showDimensions = CheckBox((C1, y, CW, L), 'Show Dimensions', value=True, sizeStyle='small', callback=self.updateEditor)
        #c.w.makeGuidelines = Button((C2, y, CW, L), f'Make guides [{personalKey}]', callback=self.makeGuidesCallback)
        # Line color is crashing RF
        #c.w.guidelinesFooterLine = HorizontalLine((self.M, y+4, -self.M, 2))
        #c.w.guidelinesFooterLine.setBorderColor((0, 0, 0, 1))
        y += L + L/5
        c.w.dimensionsEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.dimensionsEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5

        return y
 
