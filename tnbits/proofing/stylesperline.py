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
#    stylesperline.py
#

from drawBot import newPage, saveImage, newDrawing, pdfImage
from tnbits.vanillas.dialogs.warningdialog import WarningDialog
from tnbits.proofing.tx import *
from tnbits.base.samples import *
from tnbits.proofing.base import Base

class StylesPerLine(Base):
    """
    Displays each style on a single line.
    """

    name = "Styles per Line"

    def build(self, styleKeys, sampleName, sample):
        """Draws each glyph of the selected styles as outline overlay for the
        selected glyph set."""
        dy = None
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

    def draw(self, styleKeys, sample, size):
        """Builds pages with each style on a line."""
        x0 = self.margin
        dy = 0
        i = 0 # Determines page breaks within glyph sets.
        styles = {}
        flatKernings = {}
        isNewPage = True
        proofHeight = 0
        pageNumber = 1
        distributedHeight = None
        sizes = {}
        numberOfStyles = None
        sizeString = 'Size: %dpt' % size
        flatKernings = None

        if self._withKerning:
            flatKernings = self.getFlatKernings(styleKeys)

        if len(styleKeys) < 2:
            return

        # Collect styles and kerning.
        for styleKey in styleKeys:
            styles[styleKey] = self.family.getStyle(styleKey)

        # Take sorting of first style.
        _, style0 = list(styles.items())[0]
        glyphNames = compileText(sample)
        glyphNames = self.getSortedGlyphNames(style0, glyphNames)

        if self._withAutoFit:
            distributedHeight, numberOfStyles = self.getDistributedHeight(size,
                    styleKeys, styles, self.height - 2 * self.margin)
            sizes = self.getDistributedSizes(styleKeys, styles,
                    distributedHeight)
            glyphSets, maxWidths = getGlyphLineSets(glyphNames, styles, sizes,
                    self.width - 2*self.margin, flatKernings)
        else:
            for styleKey in styleKeys:
                sizes[styleKey] = size


            w = self.width - 2*self.margin
            glyphSets, maxWidths = getGlyphLineSets(glyphNames, styles, sizes,
                    w, flatKernings)

        newDrawing()
        newPage(self.width, self.height)
        self.drawDebug()
        self.drawHeader(styleKeys)
        # FIXME: find out combined location string?
        self.drawFooter(sizeString=sizeString, locationString=None)

        for glyphSet in glyphSets:
            isLast = False

            if glyphSet == glyphSets[-1]:
                isLast = True

            for styleKey in styleKeys:
                i += 1
                style = styles[styleKey]
                upem = style.info.unitsPerEm
                ascenderHeight = getAscenderHeight(style, size, upem)
                locationString = self.getLocationString(style)

                '''
                Before we start making the new proof part, we need to calculate
                offset based on previous proof height (dy).
                '''
                if self._withAutoFit:
                    # Evenly distribute lines over page.
                    s = sizes[styleKey]

                    if isNewPage == True:
                        dy = distributedHeight - getDescenderHeight(style, s, upem)
                        isNewPage = False
                    else:
                        dy += distributedHeight
                else:
                    # Continuous flow, recalculate baseline and add previous height.
                    s = size

                    if isNewPage == True:
                        dy = proofHeight + (ascenderHeight * self._leading)
                        isNewPage = False
                    else:
                        dy += proofHeight + (ascenderHeight * self._leading)

                self.drawDebugLine(self.margin + dy, r=1, message="line %d" % i)

                kwargs = dict(dy=dy, size=s, glyphNames=glyphSet,
                        maxWidths=maxWidths, pageNumber=pageNumber,
                        showStyleName=True)

                if self._withKerning:
                    kwargs['flatKerning'] = flatKernings[styleKey]

                if self._withAutoFit:
                    # Handles new pages here, not in drawGlyphs().
                    kwargs['doNewPage'] = False
                    # Make sure all lines are drawn on the same page, hacky
                    # solution for overflow calculation rounding inaccuracies.
                    # FIXME: get rid of forceDraw at some point.
                    kwargs['forceDraw'] = True
                else:
                    kwargs['isLast'] = isLast

                results = self.drawGlyphs(style, **kwargs)
                isNewPage = results['isNewPage']
                proofHeight = results['proofHeight']
                pageNumber = results['pageNumber']

                if self._withAutoFit:
                    l = len(styleKeys)
                    if numberOfStyles < l and \
                            i % numberOfStyles == 0 and \
                            not styleKey == styleKeys[-1]:
                        # Forces new page within glyphset. Exact distribution
                        # so zero overflow of previous proof part.
                        isNewPage = True
                        pageNumber += 1
                        i = 0

                        self.drawNewPage(styleKeys, pageNumber)

            if self._withAutoFit and not isLast and not isNewPage:
                # Forces new page after glyphset.
                isNewPage = True
                pageNumber += 1
                i = 0
                self.drawNewPage(styleKeys, pageNumber)

        path = self.getPath(styleKeys, size=size)
        saveImage(path)
        pdf = pdfImage()
        return path, pdf

    # Getters.

    def getMaxHeight(self, size, styleKeys, styles):
        """Finds out which style is the highest."""
        heights = []

        for styleKey in styleKeys:
            style = styles[styleKey]
            upem = style.info.unitsPerEm
            ascenderHeight = getAscenderHeight(style, size, upem)
            descenderHeight = getDescenderHeight(style, size, upem)
            minimumLeading = 1.2
            height = (ascenderHeight + descenderHeight) * minimumLeading
            heights.append(height)

        maxHeight = max(heights)
        return maxHeight

    def getDistributedHeight(self, size, styleKeys, styles, height):
        """Divides the page into even parts for multiple styles on a page."""
        numberOfStyles = len(styles.items())
        h = float(height) - 8 # Minus the leading for the bottom row style name.
        distributedHeight = h / numberOfStyles
        maxHeight = self.getMaxHeight(size, styleKeys, styles)

        while maxHeight > distributedHeight and numberOfStyles > 1:
            numberOfStyles -= 1
            distributedHeight = h / numberOfStyles

        return distributedHeight, numberOfStyles

    def getDistributedSizes(self, styleKeys, styles, distributedHeight):
        """Calculates style size based on distributed height."""
        sizes = {}

        for styleKey in styleKeys:
            style = styles[styleKey]
            leading = 1.2
            pageStyleHeight = distributedHeight / leading # pixels?
            styleHeight = style.info.ascender - style.info.descender # points?
            ratio = styleHeight / float(style.info.unitsPerEm)
            sizes[styleKey] = pageStyleHeight / ratio

        return sizes
