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
#    overlay.py
#

import traceback
from drawBot import saveImage, newDrawing, pdfImage
from tnbits.base.samples import *
from tnbits.model.objects.style import Style
from tnbits.model.storage.otfstorage import OTFStorage
from tnbits.proofing.base import Base
from tnbits.proofing.tx import *
from tnbits.vanillas.dialogs.warningdialog import WarningDialog

class Overlay(Base):
    """Overlays outlines of two or more fonts."""

    name = "Overlay"
    colors = (
        (0.75, 0, 0), (0, 0.75, 0), (0, 0, 0.75), (0.75, 0.75, 0), (0.75, 0, 0.75),
        (0, 0.75, 0.75), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (0.5, 0.5, 0),
        (0.5, 0, 0.5), (0, 0.5, 0.5), (0.25, 0, 0.75), (0, 0.25, 0.75),
        (0.75, 0, 0.25), (0.25, 0.25, 0.75), (0.25, 0.75, 0.25), (0.75, 0.25, 0.25),
    )

    def build(self, styleKeys, sampleName, sample):
        """Draws each glyph of the selected styles as outline overlay for the
        selected glyph set."""
        # Get all glyphs and render the styles.
        self.sampleName = sampleName

        if len(styleKeys) < 2:
            dialog = WarningDialog()
            dialog.openWarningDialog('Please select at least two styles.')
            return

        if self._fontSize == 'Other...':
            sizes = self.getCustomFontSizes()

            if sizes:
                for size in sizes:
                    path, pdf = self.draw(styleKeys, sample, size)
                    self.paths.append(path)
                    self.pdfs.append(pdf)

        else:
            path, pdf = self.draw(styleKeys, sample, self._fontSize)
            self.paths.append(path)
            self.pdfs.append(pdf)

        return self.paths

    def getColors(self, styleKeys):
        colors = {}

        for colorIndex, styleKey in enumerate(styleKeys):
            if colorIndex >= len(self.colors):
                colorIndex = 0
            colors[styleKey] = self.colors[colorIndex]

        return colors

    def draw(self, styleKeys, sample, size):
        sizeString = 'Size: %dpt' % size
        #locationString = self.getLocationString(style)
        styles = {}
        sizes = {}
        isNewPage = False
        self.tool.progressTicks(len(styleKeys))

        for styleKey in styleKeys:
            self.tool.progressUpdate(text='Opening style %s' % styleKey[1])
            styles[styleKey] = self.controller.getStyle(styleKey)
            sizes[styleKey] = size

        # Takes sorting of first style.
        _, style0 = list(styles.items())[0]
        flatKernings = self.getFlatKernings(styleKeys)
        maxAscenderHeight = self.getMaxAscenderHeight(styles, size)
        glyphNames = compileText(sample)
        glyphNames = self.getSortedGlyphNames(style0, glyphNames)
        self.maxUpem = self.getMaxUpem(styles)
        overlayGlyphs = self.getOverlayGlyphs(styles, sample, glyphNames)
        colors = self.getColors(styleKeys)
        lineHeight = size * self._leading
        w = self.width - 2 * self.margin
        h = self.height - 2 * self.margin
        glyphSets = getGlyphPageSets(glyphNames, styles, sizes, w, h,
                flatKernings, lineHeight)
        _showNames = self._showNames

        newDrawing()
        # FIXME: combined location string for all styles.
        self.drawNewPage(styleKeys, colors=colors, sizeString=sizeString,
                locationString=None)
        self.tool.progressTicks(len(glyphSets))

        for n, glyphSet in enumerate(glyphSets):
            self.tool.progressUpdate(text='GlyphSet %d' % n)

            for layerIndex, styleKey in enumerate(styleKeys):
                style = styles[styleKey]
                dy = maxAscenderHeight * self._leading

                if style == style0 and _showNames:
                    self._showNames = True
                else:
                    self._showNames = False

                kwargs = dict(
                        dy=dy,
                        size=size,
                        glyphNames=glyphSet,
                        doNewPage=False, fillColor=None,
                        strokeColor=colors[styleKey],
                        overlayGlyphs=overlayGlyphs, align=self._align,
                        layerIndex=layerIndex)

                # FIXME: should we overlay kern values? Or remove option?
                # if so calculate during getOverlayWidths() pass.
                '''
                if self._withKerning:
                    kwargs['flatKerning'] = flatKernings[styleKey]
                '''

                _ = self.drawGlyphs(style, **kwargs)

            if self._doOnePage:
                break

            self._showNames = _showNames

            # New page after each glyph set except the last.
            if n != len(glyphSets) - 1:
                pageNumber = n + 2
                self.drawNewPage(styleKeys, pageNumber, colors=colors,
                        locationString=None)

        path = self.getPath(styleKeys, size=size)
        saveImage(path)
        pdf = pdfImage()
        return path, pdf

    def getMaxAscenderHeight(self, styles, size):
        maxAscenderHeight = 0

        for style in styles.values():
            ascenderHeight = getAscenderHeight(style, size, style.info.unitsPerEm)
            if ascenderHeight > maxAscenderHeight:
                maxAscenderHeight = ascenderHeight

        return maxAscenderHeight

    def getMaxUpem(self, styles):
        upem = None

        for style in styles.values():
            if upem is None:
                upem = style.info.unitsPerEm
            else:
                if style.info.unitsPerEm > upem:
                    upem = style.info.unitsPerEm

        assert not upem is None
        return upem

    def getOverlayGlyphs(self, styles, sample, glyphNames):
        """Compares glyphs in styles, only adds glyphs that are in all the
        selected styles and compares maximum width.

        TODO: integrate with styles by line getGlyphLineSets()?
        """
        overlayGlyphs = {}

        for glyphName in glyphNames:
            maxWidth = 0
            missing = False

            for styleKey, style in styles.items():
                upem = style.info.unitsPerEm

                if glyphName not in style:
                    missing = True
                else:
                    if isinstance(style, Style) and \
                            isinstance(style.storage, OTFStorage) and \
                            style.storage.isVar():
                        try:
                            glyphWidth = style.getVarWidth(glyphName)
                        except Exception as e:
                            print(traceback.format_exc())
                            glyph = style[glyphName]
                            glyphWidth = glyph.width
                            #print('%s  %d' % (glyphName, glyphWidth))
                    else:
                        glyph = style[glyphName]
                        glyphWidth = glyph.width


                    #if glyphName == 'H':
                    #    print('%s: %d' % (styleKey[1], glyphWidth))

                    glyphWidth = glyphWidth * upem / self.maxUpem

                    #if glyphName == 'H':
                    #    print('%s: %d' % (styleKey[1], glyphWidth))


                    if glyphWidth > maxWidth:
                        maxWidth = glyphWidth

            if not missing:
                overlayGlyphs[glyphName] = maxWidth

        return overlayGlyphs
