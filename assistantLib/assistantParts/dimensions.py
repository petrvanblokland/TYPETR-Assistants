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
#PATHS = ('../TYPETR-Assistants/',)
#for path in PATHS:
#    if not path in sys.path:
#        print('@@@ Append to sys.path', path)
#        sys.path.append(path)

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
    DIMENSIONS_VALUE_COLOR = (0, 0, 0, 1)
    DIMENSIONS_LABEL_FONT = 'Verdana'
    DIMENSIONS_LABEL_SIZE = 12

    DIMENSIONS_BAR_MARKER_COLOR = (1, 1, 1, 1)
    DIMENSIONS_BAR_MARKER_ERROR_COLOR = (1, 1, 0.8, 0.8)

    DIMENSIONS_STEM_MARKER_COLOR = (1, 1, 1, 1)
    DIMENSIONS_STEM_MARKER_ERROR_COLOR = (1, 1, 0.8, 0.8)

    DIMENSIONS_DIAGONAL_MARKER_COLOR = (1, 1, 1, 0.25)
    DIMENSIONS_DIAGONAL_MARKER_ERROR_COLOR = (1, 1, 0, 0.4)

    DIMENSIONS_MARKER_R = 22 # Radius or marker circle behind diagonal labels
    STEM_TOLERANCE = 2 # Tolerance for stems to show as 

    def initMerzDimensions(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        self.dimensionsBarMeasureLines1 = [] # Lines left of stem marker
        self.dimensionsBarMeasureLines2 = [] # Lines right of stem marker
        self.dimensionsBarMeasureValues = []
        self.dimensionsBarMeasureBackgrounds = []

        self.dimensionsStemMeasureLines1 = [] # Lines left of stem marker
        self.dimensionsStemMeasureLines2 = [] # Lines right of stem marker
        self.dimensionsStemMeasureValues = []
        self.dimensionsStemMeasureBackgrounds = []

        self.dimensionsDiagonalMeasureLines1 = [] # Lines left of diagonal marker
        self.dimensionsDiagonalMeasureLines2 = [] # Lines right of diagonal marker
        self.dimensionsDiagonalMeasureValues = []
        self.dimensionsDiagonalMeasureBackgrounds = []

        for n in range(MAX_MEASURES):
            self.dimensionsBarMeasureLines1.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            # Right of marker circle
            self.dimensionsBarMeasureLines2.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            self.dimensionsBarMeasureBackgrounds.append(container.appendOvalSublayer(
                position=(0, 0),
                size=(self.DIMENSIONS_MARKER_R*2, self.DIMENSIONS_MARKER_R*2),
                fillColor=self.DIMENSIONS_BAR_MARKER_COLOR,
                strokeColor=None,
                visible=False,
            ))
            self.dimensionsBarMeasureValues.append(container.appendTextLineSublayer(
                position=(0, 0),
                text='',
                fillColor=self.DIMENSIONS_VALUE_COLOR,
                horizontalAlignment="center",
                font=self.DIMENSIONS_LABEL_FONT,
                pointSize=self.DIMENSIONS_LABEL_SIZE+3,
                visible=False,
            ))

            self.dimensionsStemMeasureLines1.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            # Right of marker circle
            self.dimensionsStemMeasureLines2.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            self.dimensionsStemMeasureBackgrounds.append(container.appendOvalSublayer(
                position=(0, 0),
                size=(self.DIMENSIONS_MARKER_R*2, self.DIMENSIONS_MARKER_R*2),
                fillColor=self.DIMENSIONS_STEM_MARKER_COLOR,
                strokeColor=None,
                visible=False,
            ))
            self.dimensionsStemMeasureValues.append(container.appendTextLineSublayer(
                position=(0, 0),
                text='',
                fillColor=self.DIMENSIONS_VALUE_COLOR,
                horizontalAlignment="center",
                font=self.DIMENSIONS_LABEL_FONT,
                pointSize=self.DIMENSIONS_LABEL_SIZE+3,
                visible=False,
            ))

        for n in range(MAX_MEASURES):
            # Left of marker circle
            self.dimensionsDiagonalMeasureLines1.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            # Right of marker circle
            self.dimensionsDiagonalMeasureLines2.append(container.appendLineSublayer(
                startPoint=(0, 0),
                endPoint=(0, 0),
                strokeWidth=self.DIMENSIONS_LINES_STROKE_WIDTH,
                strokeColor=self.DIMENSIONS_LINES_COLOR,
                visible=False,
            ))
            self.dimensionsDiagonalMeasureBackgrounds.append(container.appendOvalSublayer(
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

    def mouseMoveDimensions(self, g, x, y, event):
        pass 

    def mouseDownDimensions(self, g, x, y, event):
        pass 
        
    def mouseUpDimensions(self, g, x, y, event):
        pass 

    def setGlyphDimensions(self, g):
        """The editor selected another glyph."""
        self.updateGlyphDimensions(g)

    def updateGlyphDimensions(self, g):
        c = self.getController()
        dIndex = 0
        sIndex = 0 # Index of used Stem Merz layers
        bIndex = 0

        if c.w.showDimensions.get():
            ga = self.getGlyphAnalyzer(g)
            gd = self.getGlyphData(g)
            md = self.getMasterData(g.font)

            containerScale = self.dimensionsDiagonalMeasureBackgrounds[dIndex].getContainer().getContainerScale()
            # TODO: Solve the scale of the marker circle
            r = self.DIMENSIONS_MARKER_R #* containerScale

            barsDone = set()
            for sy, bars in sorted(ga.bars.items()):
                for bar in bars:
                    if bar.height == 0 or bar.height > md.HThin * 1.5: # Probably not a diagonal stem, ignore.
                        continue

                    dx = (bar.h2.x - bar.h1.x) * r / bar.height
                    dy = (bar.h2.y - bar.h1.y) * r / bar.height

                    x = bar.h1.x + (bar.h2.x - bar.h1.x)/2
                    y = bar.h1.y + (bar.h2.y - bar.h1.y)/2

                    if (bar.h1.x, bar.h1.y) in barsDone or (bar.h2.x, bar.h2.y) in barsDone:
                        continue
                    barsDone.add((bar.h1.x, bar.h2.y))
                    barsDone.add((bar.h2.x, bar.h1.y))

                    # Left side of marker, make line not strike through the transparant marker.
                    self.dimensionsBarMeasureLines1[sIndex].setVisible(True)
                    self.dimensionsBarMeasureLines1[sIndex].setStartPoint((bar.h1.x, bar.h1.y))
                    self.dimensionsBarMeasureLines1[sIndex].setEndPoint((x - dx, y - dy))

                    # Right size of marker
                    self.dimensionsBarMeasureLines2[sIndex].setVisible(True)
                    self.dimensionsBarMeasureLines2[sIndex].setStartPoint((x + dx, y + dy))
                    self.dimensionsBarMeasureLines2[sIndex].setEndPoint((bar.h2.x, bar.h2.y))

                    if gd.isLower:
                        targetBar = md.oThin
                    else:
                        targetBar = md.HThin

                    if abs(bar.height - targetBar) >= md.diagonalTolerance: # In case out of bounds, then use other marker color
                        markerColor = self.DIMENSIONS_BAR_MARKER_ERROR_COLOR
                    else:
                        markerColor = self.DIMENSIONS_BAR_MARKER_COLOR

                    self.dimensionsBarMeasureBackgrounds[sIndex].setVisible(True)
                    self.dimensionsBarMeasureBackgrounds[sIndex].setSize((r*2, r*2))
                    self.dimensionsBarMeasureBackgrounds[sIndex].setPosition((x - r, y - r))
                    self.dimensionsBarMeasureBackgrounds[sIndex].setFillColor(markerColor)

                    self.dimensionsBarMeasureValues[dIndex].setVisible(True)
                    self.dimensionsBarMeasureValues[dIndex].setText(str(int(round(bar.height))))
                    self.dimensionsBarMeasureValues[dIndex].setPosition((x, y + self.DIMENSIONS_LABEL_SIZE + 2))

                    bIndex += 1

            #print('@@@ updateGlyphDimensions Bars:', ga.diagonalBars)
            stemsDone = set()
            for sx, stems in sorted(ga.stems.items()):
                for stem in stems:
                    if stem.width == 0 or stem.width > md.HStem * 1.5: # Probably not a diagonal stem, ignore.
                        continue

                    dx = (stem.v2.x - stem.v1.x) * r / stem.width
                    dy = (stem.v2.y - stem.v1.y) * r / stem.width

                    x = stem.v1.x + (stem.v2.x - stem.v1.x)/2
                    y = stem.v1.y + (stem.v2.y - stem.v1.y)/2

                    if (stem.v1.x, stem.v1.y) in stemsDone or (stem.v2.x, stem.v2.y) in stemsDone:
                        continue
                    stemsDone.add((stem.v1.x, stem.v1.y))
                    stemsDone.add((stem.v2.x, stem.v2.y))

                    # Left side of marker, make line not strike through the transparant marker.
                    self.dimensionsStemMeasureLines1[sIndex].setVisible(True)
                    self.dimensionsStemMeasureLines1[sIndex].setStartPoint((stem.v1.x, stem.v1.y))
                    self.dimensionsStemMeasureLines1[sIndex].setEndPoint((x - dx, y - dy))

                    # Right size of marker
                    self.dimensionsStemMeasureLines2[sIndex].setVisible(True)
                    self.dimensionsStemMeasureLines2[sIndex].setStartPoint((x + dx, y + dy))
                    self.dimensionsStemMeasureLines2[sIndex].setEndPoint((stem.v2.x, stem.v2.y))

                    if gd.isLower:
                        targetStem = md.nStem
                    else:
                        targetStem = md.HStem

                    if abs(stem.width - targetStem) >= md.diagonalTolerance: # In case out of bounds, then use other marker color
                        markerColor = self.DIMENSIONS_STEM_MARKER_ERROR_COLOR
                    else:
                        markerColor = self.DIMENSIONS_STEM_MARKER_COLOR

                    self.dimensionsStemMeasureBackgrounds[sIndex].setVisible(True)
                    self.dimensionsStemMeasureBackgrounds[sIndex].setSize((r*2, r*2))
                    self.dimensionsStemMeasureBackgrounds[sIndex].setPosition((x - r, y - r))
                    self.dimensionsStemMeasureBackgrounds[sIndex].setFillColor(markerColor)

                    self.dimensionsStemMeasureValues[dIndex].setVisible(True)
                    self.dimensionsStemMeasureValues[dIndex].setText(str(int(round(stem.width))))
                    self.dimensionsStemMeasureValues[dIndex].setPosition((x, y + self.DIMENSIONS_LABEL_SIZE + 2))

                    sIndex += 1

            # Show diagonal measures that are within the range of stems. If they are outside the ma.diagonalTolerance range,
            # then show them as a different color.
            for dxy, p0, p1 in ga.dValues:
                dxy = int(round(dxy))
                if dxy == 0 or dxy > md.HStem * 1.5: # Probably not a diagonal stem, ignore.
                    continue

                dx = (p1.x - p0.x) * r / dxy
                dy = (p1.y - p0.y) * r / dxy

                x = p0.x + (p1.x - p0.x)/2
                y = p0.y + (p1.y - p0.y)/2

                # Left side of marker, make line not strike through the transparant marker.
                self.dimensionsDiagonalMeasureLines1[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureLines1[dIndex].setStartPoint((p0.x, p0.y))
                self.dimensionsDiagonalMeasureLines1[dIndex].setEndPoint((x - dx, y - dy))

                # Right size of marker
                self.dimensionsDiagonalMeasureLines2[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureLines2[dIndex].setStartPoint((x + dx, y + dy))
                self.dimensionsDiagonalMeasureLines2[dIndex].setEndPoint((p1.x, p1.y))

                if gd.isLower:
                    targetStem = md.nStem
                else:
                    targetStem = md.HStem

                if abs(dxy - targetStem) >= md.diagonalTolerance: # In case out of bounds, then use other marker color
                    markerColor = self.DIMENSIONS_DIAGONAL_MARKER_ERROR_COLOR
                else:
                    markerColor = self.DIMENSIONS_DIAGONAL_MARKER_COLOR

                self.dimensionsDiagonalMeasureBackgrounds[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureBackgrounds[dIndex].setSize((r*2, r*2))
                self.dimensionsDiagonalMeasureBackgrounds[dIndex].setPosition((x - r, y - r))
                self.dimensionsDiagonalMeasureBackgrounds[dIndex].setFillColor(markerColor)

                self.dimensionsDiagonalMeasureValues[dIndex].setVisible(True)
                self.dimensionsDiagonalMeasureValues[dIndex].setText(str(dxy))
                self.dimensionsDiagonalMeasureValues[dIndex].setPosition((x, y + self.DIMENSIONS_LABEL_SIZE + 2))

                dIndex += 1
                if dIndex >= MAX_MEASURES:
                    break

        else: # Not showing dimension merz objects
            pass

        for n in range(dIndex, MAX_MEASURES):
            self.dimensionsDiagonalMeasureLines1[n].setVisible(False)
            self.dimensionsDiagonalMeasureLines2[n].setVisible(False)
            self.dimensionsDiagonalMeasureValues[n].setVisible(False)
            self.dimensionsDiagonalMeasureBackgrounds[n].setVisible(False)

        for n in range(sIndex, MAX_MEASURES):
            self.dimensionsStemMeasureLines1[n].setVisible(False)
            self.dimensionsStemMeasureLines2[n].setVisible(False)
            self.dimensionsStemMeasureValues[n].setVisible(False)
            self.dimensionsStemMeasureBackgrounds[n].setVisible(False)

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
 
