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
#    allmetrics.py
#
from random import random

from drawBot import newPage, saveImage, newDrawing, stroke, fill, strokeWidth, \
                    line, fontSize, text, textSize, pdfImage
from tnbits.vanillas.dialogs.warningdialog import WarningDialog
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.proofing.base import Base
from tnbits.proofing.tx import *

class AllMetrics(Base):
    """
    Shows metrics provided by the style analyzer.
    TODO: shorter line width to prevent overlaping metadata texts.
    """

    name = "All Metrics"

    def __init__(self, **kwargs):
        kwargs['doOneLine'] = True
        super(AllMetrics, self).__init__(**kwargs)

    def build(self, styleKeys, sampleName, sample):
        """Show basic metrics glyph set with metrics lines. This can be used
        with any selection of sample, but just one line will be shown."""
        self.sampleName = sampleName

        if len(styleKeys) < 1:
            dialog = WarningDialog()
            dialog.openWarningDialog('Please select at least one style.')
            return

        for styleKey in styleKeys:
            if self._fontSize == 'Other...':
                sizes = self.getCustomFontSizes()

                if sizes:
                    for size in sizes:
                        path = self.draw(styleKey, sample, size)
                        self.paths.append(path)
            else:
                path, pdf = self.draw(styleKey, sample, self._fontSize)
                self.paths.append(path)
                self.pdfs.append(pdf)

        return self.paths

    def draw(self, styleKey, sample, size):
        style = self.controller.getStyle(styleKey)
        sizeString = 'Size: %dpt' % size
        locationString = self.getLocationString(style)
        flatKernings = self.getFlatKernings([styleKey])

        newDrawing()
        newPage(self.width, self.height)
        self.drawDebug()
        self.drawHeader([styleKey])
        self.drawFooter(sizeString=sizeString, locationString=locationString)
        self.tool.progressUpdate(title='Proofing metrics', text='Opening %s' % styleKey[1])
        dy = size * self._leading
        sa = analyzerManager.getStyleAnalyzer(style=style) # We need it to guess smallcap height.

        # Draw the glyphs.

        kwargs = dict(sample=sample, dy=dy, size=size,
                flatKerning=flatKernings[styleKey])

        # Draw first line of glyphs.
        results = self.drawGlyphs(style, **kwargs)
        y0 = self.margin + dy #- getDescenderHeight(style, size)
        self.drawMetricsLabels(y0, style, sa, size)
        path = self.getPath([styleKey], size=size)
        saveImage(path)
        pdf = pdfImage()
        return path, pdf

    def drawMetricsLabels(self, y0, style, sa, size):
        w, h, margin = self.getPaperSize()
        x0 = margin
        x1 = w - margin
        fontSize(4)
        labels = (
                ('asc %d', style.info.ascender),
                ('cap %d ', style.info.capHeight),
                ('x %d ', style.info.xHeight),
                ('scap %d ', sa.scapHeight),
                ('base %d ', 0),
                ('desc %d ', style.info.descender))

        w = 0

        # FIXME: better font and position.
        # Add metrics lines.
        for label, y1 in labels:
            stroke(None)
            fill(0)
            y1 *= size / float(style.info.unitsPerEm)
            y = h - (y0 - y1)
            label1 = label % y1
            width1, _ = textSize(label1)
            w += width1
            text(label1, x1 - w, y)

            # Lines.
            strokeWidth(0.25)
            stroke(random(), random(), random())
            fill(None)
            line((x0, y), (x1, y))
