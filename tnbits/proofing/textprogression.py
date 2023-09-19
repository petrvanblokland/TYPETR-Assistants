# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    textprogression.py
#

from drawBot import saveImage, newDrawing, pdfImage
from tnbits.vanillas.dialogs.warningdialog import WarningDialog
from tnbits.proofing.base import Base
from tnbits.proofing.tx import *

class TextProgression(Base):
    """Draws the selected glyph set as a text progression."""

    name = "Text Progression"

    def build(self, styleKeys, sampleName, sample):
        """Draw the selected glyph set in a page wide column."""
        self.sampleName = sampleName

        if len(styleKeys) < 1:
            dialog = WarningDialog()
            dialog.openWarningDialog('Please select at least one style.')
            return

        if self._fontSizeProgression <= self._fontSize:
            sizes = range(self._fontSizeProgression, self._fontSize+1)
        else:
            sizes = range(self._fontSizeProgression, self._fontSize-1, -1)

        self.tool.progressTicks(len(styleKeys) * len(sizes))

        for styleKey in styleKeys:
            path, pdf = self.draw(sample, styleKey, sizes)
            self.paths.append(path)
            self.pdfs.append(pdf)

        return self.paths

    def getSizeString(self, sizes):
        sizeString = ''
        pointSizes = []

        for size in sizes:
            pointSize = '%dpt' % size
            pointSizes.append(pointSize)

        if self._fontSize == 'Other...':
            sizeString = 'Sizes: %s' % ', '.join(pointSizes)
        else:
            sizeString = 'Sizes: %s-%s' % (pointSizes[0], pointSizes[-1])

        return sizeString

    def draw(self, sample, styleKey, sizes):
        """Draws the textProgression template for a single style."""
        # TODO: guestimate number of pages and reset / update ticks.
        #self.tool.progressTicks(n)

        style = self.family.getStyle(styleKey)
        flatKernings = self.getFlatKernings([styleKey])
        upem = style.info.unitsPerEm
        styleKeys = [styleKey]
        newDrawing()
        sizeString=self.getSizeString(sizes)
        locationString = self.getLocationString(style)
        self.drawNewPage(styleKeys, pageNumber=1, sizeString=sizeString, locationString=locationString)
        isNewPage = True
        dy = 0
        proofHeight = 0
        pageNumber = 1

        for i, size in enumerate(sizes):
            self.tool.progressUpdate(title='Proofing textProgression',
                    text='%s | %dpt' % (styleKey[1], size))

            ascenderHeight = getAscenderHeight(style, size, upem)

            '''
            Before we start making the proof for a new font size:
            * calculate starting point based on previous proof height,
            * recalculate delta-y when we're on a new page.
            '''
            if isNewPage == True:
                dy = proofHeight + ascenderHeight * self._leading
                isNewPage = False
            else:
                dy += proofHeight + ascenderHeight * self._leading

            kwargs = dict(sample=sample, dy=dy, size=size,
                    flatKerning=flatKernings[styleKey], showSize=True,
                    pageNumber=pageNumber, sizeString=sizeString)

            # Passes glyphs to DrawBot.
            results = self.drawGlyphs(style, **kwargs)
            isNewPage = results['isNewPage']
            proofHeight = results['proofHeight']
            pageNumber = results['pageNumber']

        sizeString = '%d-%d' % (min(sizes), max(sizes))
        path = self.getPath(styleKeys,
                sizeString=sizeString)
        self.tool.progressUpdate(title='Saving to %s' % path)
        saveImage(path)
        pdf = pdfImage()
        return path, pdf
