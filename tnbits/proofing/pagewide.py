#-*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    pagewide.py
#

from drawBot import newPage, saveImage, newDrawing, pdfImage, oval, fill, rect, stroke
from tnbits.vanillas.dialogs.warningdialog import WarningDialog
from tnbits.proofing.base import Base
from tnbits.proofing.tx import *

class PageWide(Base):
    """Draws the selected glyph set page wide."""

    name = "Page Wide"

    def build(self, styleKeys, sampleName, sample):
        """Builds a page for each size."""
        self.sampleName = sampleName

        if len(styleKeys) < 1:
            dialog = WarningDialog()
            dialog.openWarningDialog('Please select at least one style.')
            return

        for styleKey in styleKeys:
            style = self.family.getStyle(styleKey)
            title = 'Proofing style for glyph set %s' % sampleName
            self.tool.progressUpdate(title=title, text=styleKey[1])
            path = ''

            if self._fontSize == 'Other...':
                sizes = self.getCustomFontSizes()

                if sizes:
                    path, pdf = self.draw(styleKey, sample, sizes)
            else:
                path, pdf = self.draw(styleKey, sample, [self._fontSize])

            self.paths.append(path)
            self.pdfs.append(pdf)

        return self.paths

    def getAligned(self, scale, coords):
        if self._pageAlign == 0:
            return coords

        paperWidth, _, margin = self.getPaperSize()
        lineWidth = paperWidth - 2 * margin

        lineWidth = int(lineWidth / scale)
        widths = []
        alignedCoords = []

        for page in coords:
            alignedPage = []

            for line in page:
                alignedLine = []
                width = 0

                # Calculates total line width, ignoring kerning of last
                # glyph.
                for i, info in enumerate(line):
                    _, _, _, _, w, k = info

                    if i != len(line):
                        width += w + k
                    else:
                        width += w

                if self._pageAlign == 1:
                    dx = (lineWidth - width) / 2 * scale
                elif self._pageAlign == 2:
                    dx = (lineWidth - width) * scale

                for info in line:
                    x = info[2]
                    info[2] = x + dx
                    alignedLine.append(info)
                alignedPage.append(alignedLine)

            alignedCoords.append(alignedPage)

        return alignedCoords

    def draw(self, styleKey, sample, sizes, continuous=True):
        """Builds pages for a single style."""
        style = self.controller.getStyle(styleKey)
        flatKerning = None

        if self._withKerning:
            flatKernings = self.getFlatKernings([styleKey])
            flatKerning = flatKernings[styleKey]

        newDrawing()
        sizeString, sizeStringFile = self.getSizeString(sizes)
        locationString = self.getLocationString(style)
        styleKeys = [styleKey]
        isNewPage = True
        proofHeight = 0
        pageNumber = 1
        upem = style.info.unitsPerEm

        for i, size in enumerate(sizes):
            '''
            Before we start making the proof for a new font size:
            * calculate starting point based on previous proof height,
            * recalculate y0 when we're on a new page.
            '''
            ascenderHeight = getAscenderHeight(style, size, upem)

            if isNewPage == True:
                dy = proofHeight + ascenderHeight * self._leading
                isNewPage = False
            else:
                dy += proofHeight + ascenderHeight * self._leading

            kwargs = dict(sample=sample, dy=dy, size=size,
                    flatKerning=flatKerning, pageNumber=pageNumber)

            coords, results = self.getGlyphCoords(style, **kwargs)
            scale = getScale(size, style.info.unitsPerEm)
            alignedCoords = self.getAligned(scale, coords)
            self.drawPages(alignedCoords, styleKeys, size, sizeString=sizeString,
                    locationString=locationString)

        path = self.getPath(styleKeys, sizeString=sizeStringFile)
        saveImage(path)
        pdf = pdfImage()
        return path, pdf

    def drawPages(self, alignedCoords, styleKeys, size, sizeString=None,
            locationString=None):

            for i, page in enumerate(alignedCoords):
                newPage(self.width, self.height)
                self.drawDebug()
                self.drawHeader(styleKeys)

                for line in page:
                    for info in line:
                        glyph, glyphName, x, y, w, _ = info
                        self.drawGlyph(glyph, glyphName, w, x, y, size,
                                fillColor=(0, 0, 0), strokeColor=None)

                self.drawFooter(sizeString=sizeString, locationString=locationString)

    def getSizeString(self, sizes):
        sizeString = ''
        sizeStringFile = ''

        if len(sizes) > 1:
            pointSizes = []
            for size in sizes:
                pointSize = '%dpt' % size
                pointSizes.append(pointSize)

            sizeString = 'Sizes: %s' % ', '.join(pointSizes)
            sizeStringFile = '-'.join(pointSizes)
        else:
            sizeString = 'Size: %spt' % sizes[0]
            sizeStringFile = '%spt' % sizes[0]

        return sizeString, sizeStringFile
