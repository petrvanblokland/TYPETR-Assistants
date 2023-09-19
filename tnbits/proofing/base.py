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
#    base.py
#

from __future__ import division

import os, re
import datetime
import traceback

from drawBot import (newPage, drawPath, translate, scale, fill, stroke, rect,
        line, text, fontSize, strokeWidth, rotate, textSize, image, textBox)

from AppKit import (NSMakeRect, NSImage, NSAffineTransform,
        NSTIFFCompressionNone, NSCompositeCopy, NSImageHintInterpolation,
        NSImageInterpolationNone)

from fontTools.pens.cocoaPen import CocoaPen

from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.base.robofont.defaults import doodleLibIdentifier, getDefault
from tnbits.base.expandtext import expandText
from tnbits.base.samples import *
from tnbits.errors.floqerror import FloqError
from tnbits.groups import *
from tnbits.model.objects.style import getStyleKey
from tnbits.model.toolbox.kerning.buildgroups import explodeKerning
from tnbits.model.objects.style import Style
from tnbits.model.objects.xgroups import XGroups
from tnbits.model.storage.ufostorage import UFOStorage
from tnbits.model.storage.otfstorage import OTFStorage
from tnbits.proofing.tx import *
from tnbits.toolbox.character import CharacterTX
from tnbits.toolbox.fontparts.unicode import UnicodeTX
DEBUG = False

class Base(object):
    """Base class for a template, which contains all the general drawing functions to be
    used for proofing."""

    # Font size of header and footer line.
    HEADER_FONTSIZE = 8
    HEADER_LEADING = 1.2
    MONTHS = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    DEFAULTFILL = 0.5
    infoSize = 2

    # Init.

    def __init__(self, controller=None, tool=None, family=None, fontSize=None,
            fontSizeProgression=None, customFontSize=None, leading=None,
            withKerning=None, withAutoFit=None, showGlyphSpace=None,
            showKernValues=None, showMarginValues=None, showNames=None,
            showErrors=None, doOnePage=None, align=0, pageAlign=0,
            showMissing=None, styleKeys=None, sortGlyphs=None, paperSize=None,
            repeatLastGlyph=None, doOneLine=False, doNewlines=False,
            compileText=False, **kwargs):
        self.controller = controller
        self.tool = tool
        self.family = family
        self._fontSize = fontSize
        self._fontSizeProgression = fontSizeProgression
        self._customFontSize = customFontSize
        self._leading = leading
        self._withKerning = withKerning
        self._showGlyphSpace = showGlyphSpace
        self._showKernValues = showKernValues
        self._showMarginValues = showMarginValues
        self._showNames = showNames
        self._showErrors = showErrors
        self._showMissing = showMissing
        self._sortGlyphs = sortGlyphs
        self._doOnePage = doOnePage
        self._doOneLine = doOneLine
        self._doNewlines = doNewlines
        self._repeatLastGlyph = repeatLastGlyph
        self._align = align
        self._pageAlign = pageAlign
        self._withAutoFit = withAutoFit
        self._compileText = compileText

        self.warningDialog = None
        self.glyphNames = None
        self.size = None
        self.margin = None
        self.scale = None
        self.lineHeight = None
        self.descender = None
        self.ascender = None
        self.capHeight = None
        self.labelSize = None
        self.paths = []
        self.pdfs = []
        self.paperSize = paperSize
        self.infoLeading = self.getInfoLeading()
        self.otfWarning = False
        self.defaultGlyphWidth = 500
        self.maxUpem = None
        self.upem = None
        w, h, margin = self.getPaperSize()
        self.width = w
        self.height = h
        self.margin = margin
        self.isVariableFont = False
        self.errors = []
        self.cache = {}
        self.widthsCache = {}
        self.currentStyle = None
        self.xgroups = {}

    def build(self, styleKeys, *args, **kwargs):
        raise NotImplementedError

    # Get.

    def getMissingGlyphWidth(self, glyphName, maxWidths=None):
        if maxWidths and glyphName in maxWidths:
            return maxWidths[glyphName] / self.scale
        else:
            return self.defaultGlyphWidth

    def isVar(self, style):
        if not isinstance(style, Style):
            return False
        elif not isinstance(style.storage, OTFStorage):
            return False
        elif not style.storage.isVar():
            return False

        return True

    def getLocationString(self, style):
        if not self.isVar(style):
            return

        s = []
        for k, v in style.rawLocation.items():
            s.append('%s %0.1f' % (k, v))

        return '; '.join(s)

    def getGlyphAndWidth(self, glyphName, overlayGlyphs=None, maxWidths=None):
        """Gets the glyph and its width. If it is present in overlayGlyphs then
        we return that value to make overlaying glyphs align."""
        overlay = False
        width = None
        missing = False

        if not glyphName in self.style:
            primary = UnicodeTX.primaryUnicodeForGlyphName(glyphName)
            unicodeData = UnicodeTX.getUnicodeData(self.style)
            if isinstance(primary, list):
                print('warning: primary is a list: %s' % primary)
                primary = primary[0]

            try:
                if primary in unicodeData:
                    unicodes = unicodeData[primary]
                    for uc in unicodes:
                        if uc in self.style:
                            glyphName = uc
                            break
            except:
                print(traceback.format_exc())
                print(primary)
                print(unicodeData)

        if not glyphName in self.style or glyphName == '.notdef' or \
                self.style[glyphName] is None:
            glyph = None
            width = self.getMissingGlyphWidth(glyphName, maxWidths=maxWidths)
        else:
            glyph = self.style[glyphName]

            # TODO: what about overlaying var fonts?
            if overlayGlyphs is None:
                if self.isVariableFont:
                    width = self.getVarWidth(glyphName)
                else:
                    width = glyph.width
            else:
                # Gets the width from overlayGlyphs.
                if glyphName in overlayGlyphs:
                    overlay = True
                    width = overlayGlyphs[glyphName]
                else:
                    glyph = None
                    width = self.getMissingGlyphWidth(glyphName, maxWidths=maxWidths)

        return glyph, glyphName, width, overlay

    def getVarWidth(self, glyphName):
        if not glyphName in self.widthsCache:
            width = self.style.getVarWidth(glyphName)
            self.widthsCache[glyphName] = width
        else:
            width = self.widthsCache[glyphName]

        return width

    def getGlyphCoord(self, x, y, glyphWidth, proofHeight, showSize, doNewLine):
        #  End of line.
        newLine = False
        w = self.width - 2 * self.margin

        if (x + glyphWidth * self.scale) > self.margin + w:
            newLine = True

            if doNewLine:
                # Break and continue new line at 0.
                # Back to original indent.
                x = self.margin

                # Extra indent for text progression template.
                if showSize:
                    x += self.margin

                y += self.lineHeight
                proofHeight += self.lineHeight

        return x, y, proofHeight, newLine

    def getKerning(self, x, prevGlyph, glyph, flatKerning):
        kerning = 0

        if self._withKerning and x > 0 and prevGlyph is not None and glyph is not None:
            pair = prevGlyph.name, glyph.name

            # TODO: in case of overlay take largest kerning value.
            if flatKerning is not None and pair in flatKerning:
                kerning = int(round(flatKerning[pair]))
                x += kerning * self.scale

        return x, kerning

    def setGroups(self):
        """Make sure that the x-ref xGroups are initialized for this style. If
        force is True, then always recalculate the x-ref dictionary.

        TODO: update when groups have been edited in RoboFont.
        """
        if self.style.path in self.xgroups:
            return

        xgroups = XGroups(self.style)
        self.xgroups[self.style.path] = xgroups

    def getNewPageCoord(self, y, doNewPage, pageNumber, proofHeight,
            sizeString=None, drawNew=True):
        """Checks if height plus one line is exceeding margin, if so makes new
        page."""
        isNewPage = False
        h = self.height - 2 * self.margin
        if y + self.descender > self.margin + h:
            if doNewPage and not self._doOnePage:
                # Set function variables.
                pageNumber += 1
                isNewPage = True
                y = self.margin + (self.ascender * self._leading)
                proofHeight = self.ascender * self._leading
                styleKeys = [getStyleKey(self.style)]
                if drawNew:
                    self.drawNewPage(styleKeys, pageNumber=pageNumber, sizeString=sizeString)

        return pageNumber, y, isNewPage, proofHeight


    def getNewPage(self, y, doNewPage, pageNumber, isNewPage,
            proofHeight, sizeString=None, drawNew=True):
        """Checks if height plus one line is exceeding margin, if so makes new
        page."""
        h = self.height - 2 * self.margin
        if y + self.descender > self.margin + h:
            if doNewPage and not self._doOnePage:
                # Set function variables.
                pageNumber += 1
                isNewPage = True
                y = self.margin + (self.ascender * self._leading)
                proofHeight = self.ascender * self._leading
                styleKeys = [getStyleKey(self.style)]
                if drawNew:
                    self.drawNewPage(styleKeys, pageNumber=pageNumber, sizeString=sizeString)

        return pageNumber, y, isNewPage, proofHeight

    def getLastLine(self, isNewPage, proofHeight, y, isLast, forceDraw,
            pageNumber):
        """Checks if last line fits exactly, else handles overflow to next
        page."""
        h = self.height - 2 * self.margin

        # Last line (fits exactly, else should already be handled in draw()).
        if y + self.descender == self.margin + h:
            if not isLast and not forceDraw:
                isNewPage = True
                proofHeight = 0
                pageNumber += 1

                # New page in DrawBot.
                newPage(self.width, self.height)
                self.drawDebug()
                self.drawHeader([getStyleKey(self.style)], pageNumber=pageNumber)
                self.drawFooter()
        else:
            proofHeight += self.descender

        return isNewPage, proofHeight, pageNumber

    # Update.

    def clearCache(self):
        self.cache = {}
        self.widthsCache = {}

    def update(self, glyphNames, style, size):
        """Updates values that will change between each proof run."""
        self.currentStyle = style
        # TODO: check style and location before clearing self.cache.
        self.clearCache()
        self.isVariableFont = self.isVar(self.style)
        self.glyphNames = self.getSortedGlyphNames(style, glyphNames)
        self.size = size
        self.labelSize = size / 2

        from tnbits.proofing.overlay import Overlay

        if isinstance(self, Overlay):
            self.upem = self.maxUpem
        else:
            self.upem = style.info.unitsPerEm

        self.scale = getScale(size, self.upem)
        self.lineHeight = getLineHeight(size, self._leading)
        self.descender = getDescenderHeight(style, size, self.upem)
        self.ascender = getAscenderHeight(style, size, self.upem)
        self.capHeight = getCapHeight(style, size, self.upem)

    def sampleToGlyphNames(self, sample):
        glyphNames = []

        if self.sampleName == SELECTED_SAMPLE:
            if self._compileText:
                glyphNames = compileText(sample)
            else:
                for s in sample:
                    if s == '\n':
                        glyphNames.append(s)
                    else:
                        # TODO: already glyphName after compileText?
                        glyphName = CharacterTX.char2GlyphName(s)
                        glyphNames.append(glyphName)
        else:
            if sample in SAMPLE_TAGS:
                self.setGroups()
                xgroups = self.xgroups[self.style.path]
                sample = expandText(self.style, sample, xgroups)
            try:
                glyphNames = compileText(sample)
            except Exception as e:
                print('Sample in wrong format;')
                print(sample)

        return glyphNames

    # Draw.

    def drawGlyphs(self, style, sample=None, dx=0, dy=0, glyphNames=None,
            size=None, maxWidths=None, flatKerning=None, fillColor=0,
            strokeColor=None, doNewLine=True, doNewPage=True, showSize=False,
            showStyleName=False, overlayGlyphs=None, pageNumber=1,
            align='left', isLast=False, forceDraw=False, sizeString=None,
            showNames=True, layerIndex=0, iteration=0):
        """Main function that draws the glyphs on the page. Either goes to the
        next page or stops if the margin of the drawing area is reached.

        - doNewLine: breaks line when running outside proof rectangle.
        - showSize: point size prefix for text progression template.
        - showStyleName: style name under first line.
        - doNewPage: enables multiple pages.
        - overlayGlyphs: Set of widest glyphs in case of overlay, to calculate
          position.
        - forceDraw: make sure all glyphs are written on the same page,
          regardless of margin bounds overflow.
        - doBitmap: TODO

        TODO: replace with getGlyphCoords() / drawGlyph().
        TODO: merge doNewPage with global doOnePage, logically similar.
        """
        assert sample or glyphNames
        isNewPage = False
        proofHeight = 0
        prevGlyph = None
        glyphIndex = None
        self.style = style

        if not glyphNames:
            glyphNames = self.sampleToGlyphNames(sample)

        self.update(glyphNames, style, size)

        # Start drawing at margin plus offset.
        y = self.margin + dy
        x = self.margin + dx
        self.drawDebugLine(y)

        # Extra margin for point sizes.
        if showSize:
            x += self.margin

        # Main loop.
        for glyphIndex, glyphName in enumerate(self.glyphNames):
            glyph, glyphName, glyphWidth, overlay = self.getGlyphAndWidth(glyphName,
                    overlayGlyphs, maxWidths=maxWidths)

            # Start of line.
            if x == 0 and glyphName == 'space':
                continue

            if glyphName == '\n':
                if self._doNewlines:
                    x = self.margin + dx
                    y += self.lineHeight
                continue

            # FIXME: kerning should be calculated before newline.
            x, y, proofHeight, newLine = self.getGlyphCoord(x, y, glyphWidth, proofHeight,
                    showSize, doNewLine)

            if newLine and self._doOneLine:
                break

            x, kerning = self.getKerning(x, prevGlyph, glyph, flatKerning)
            pageNumber, y, isNewPage, proofHeight = self.getNewPage(y,
                    doNewPage, pageNumber, isNewPage, proofHeight,
                    sizeString=sizeString)
            self.drawLineStart(glyphIndex, showSize, showStyleName, y)

            # Repeats last glyph on new line; new first glyph so kerning value
            # is always zero.
            if newLine and self._repeatLastGlyph:
                x = self.drawGlyph(prevGlyph, prevGlyphName, prevGlyphWidth, x,
                        y, size, overlay=overlay, align=align, kerning=0,
                        strokeColor=strokeColor, fillColor=fillColor,
                        layerIndex=layerIndex)
                x += kerning * self.scale

            # Break for a single page.
            h = self.height - 2 * self.margin

            if y + self.descender > self.margin + h:
                # FIXME: should break one glyph earlier.
                if self._doOnePage:
                    break
                if (not doNewPage and not forceDraw):
                    break

            x = self.drawGlyph(glyph, glyphName, glyphWidth, x, y, size,
                    overlay=overlay, align=align, kerning=kerning,
                    strokeColor=strokeColor, fillColor=fillColor,
                    layerIndex=layerIndex)

            # Store current values for next loop.
            prevGlyph = glyph
            prevGlyphName = glyphName
            prevGlyphWidth = glyphWidth

        isNewPage, proofHeight, pageNumber = self.getLastLine(isNewPage,
                proofHeight, y, isLast, forceDraw, pageNumber)

        results = {'isNewPage': isNewPage, 'proofHeight': proofHeight,
                'pageNumber': pageNumber}
        return results

    def getGlyphCoords(self, style, sample=None, dx=0, dy=0, glyphNames=None,
            size=None, maxWidths=None, flatKerning=None, fillColor=0,
            strokeColor=None, doNewLine=True, doNewPage=True, showSize=False,
            showStyleName=False, overlayGlyphs=None, pageNumber=1,
            align='left', isLast=False, forceDraw=False, sizeString=None,
            showNames=True, layerIndex=0):
        """
        FIXME: in case of onePage,  should stop one glyph earlier.
        """
        self.style = style
        assert sample or glyphNames
        isNewPage = False
        proofHeight = 0
        prevGlyph = None
        glyphIndex = None
        coords = []
        page = []
        line = []

        if not glyphNames:
            glyphNames = self.sampleToGlyphNames(sample)

        self.update(glyphNames, style, size)

        # Start drawing at margin plus offset.
        y = self.margin + dy
        x0 = self.margin + dx
        x = x0

        #if showSize:
        #    x += self.margin

        for glyphIndex, glyphName in enumerate(self.glyphNames):
            glyph, glyphName, glyphWidth, overlay = self.getGlyphAndWidth(glyphName,
                    overlayGlyphs, maxWidths=maxWidths)

            # Start of line.
            if x == x0 and glyphName == 'space':
                continue

            # Forced new line.
            if glyphName == '\n':
                if self._doNewlines:
                    x = x0
                    y += self.lineHeight
                    page.append(line)
                    line = []
                continue

            x, y, proofHeight, newLine = self.getGlyphCoord(x, y, glyphWidth,
                    proofHeight, showSize, doNewLine)

            if newLine:
                page.append(line)
                line = []

                if self._doOneLine:
                    break

            x, kerning = self.getKerning(x, prevGlyph, glyph, flatKerning)

            pageNumber, y, isNewPage, proofHeight = self.getNewPageCoord(y,
                    doNewPage, pageNumber, proofHeight,
                    sizeString=sizeString, drawNew=False)

            if isNewPage:
                if len(line):
                    page.append(line)

                coords.append(page)
                page = []
                line = []
            line.append([glyph, glyphName, x, y, glyphWidth, kerning])

            # Break for a single page.
            h = self.height - 2 * self.margin

            if y + self.descender > self.margin + h:
                if self._doOnePage: break
                if (not doNewPage and not forceDraw):
                    break

            if overlay:
                scale = getScale(size, self.maxUpem)
                x += glyphWidth * scale
            else:
                x += glyphWidth * self.scale

            # Store current values for next loop.
            prevGlyph = glyph
            prevGlyphName = glyphName
            prevGlyphWidth = glyphWidth

        if len(line):
            page.append(line)

        if len(page):
            coords.append(page)

        isNewPage, proofHeight, pageNumber = self.getLastLine(isNewPage,
                proofHeight, y, isLast, forceDraw, pageNumber)

        results = {'isNewPage': isNewPage, 'proofHeight': proofHeight,
                'pageNumber': pageNumber}
        return coords, results

    # Glyph drawing.

    def drawGlyph(self, glyph, glyphName, glyphWidth, x, y, size, kerning=0,
            strokeColor=None, fillColor=0, layerIndex=0, overlay=False,
            align=None):
        """Draws the glyph outline and optional extra information around it
        such as kerning value(s), name, glyph space box."""
        w = scaledWidth(glyphWidth, self.scale)

        if overlay:
            x0 = getXOverlay(x, align, glyphWidth, glyph, self.scale)
        else:
            x0 = x

        h = self.size

        if glyph is None:
            self.drawGlyphMissing(glyphName, x0, y, w, h, layerIndex=layerIndex, color=strokeColor)
        else:
            # TODO: calculate max h in case of overlay so info texts have same
            # offset.
            self.drawOutline(glyph, glyphName, x0, y, fillColor, strokeColor)
            self.drawMargin(glyph, x0, y, w, layerIndex, strokeColor)
            self.drawKerning(glyph, x0, y, kerning)
            gsw = scaledWidth(glyph.width, self.scale)
            self.drawGlyphSpace(x0, y, gsw, h, strokeColor)

        self.drawGlyphName(glyphName, glyphWidth, x0, y)

        # Adds width to `x`-value for next glyph and store this glyph as `previous`
        # for later reference.
        if overlay:
            scale = getScale(size, self.maxUpem)
            x += glyphWidth * scale
        else:
            x += glyphWidth * self.scale

        return x

    def drawOutline(self, glyph, glyphName, x, y, fillColor=None,
            strokeColor=None, strokeW=2):
        """Flips the canvas and draws the glyph itself with the Cocoa pen."""
        # TODO: cache outlines.
        _, h, _ = self.getPaperSize()
        x0 = x
        y0 = h - y
        translate(x0, y0)
        scale(self.scale)

        if strokeColor is None:
            stroke(None)
        else:
            r, g, b = strokeColor
            stroke(r, g, b)
            strokeWidth(strokeW)

        if fillColor in (0, None):
            # (0, 0, 0) gives Cocoa error?
            fill(fillColor)
        else:
            r, g, b = fillColor
            fill(r, g, b)

        pen = CocoaPen(self.style)
        isVarGlyph = False

        if self.isVariableFont:
            try:
                if not glyphName in self.cache:
                    path = self.style.getVarOutline(glyphName)
                    self.cache[glyphName] = path
                else:
                    path = self.cache[glyphName]

                drawPath(path)
                isVarGlyph = True
            except Exception as e:
                print('%s Error with variable glyph' % glyphName)
                print(traceback.format_exc())
                # Falling back to non-var outline.

        if isVarGlyph is False:
            try:
                glyph.draw(pen)
                drawPath(pen.path)
            except Exception as e:
                msg = 'proofing.base.drawGlyphOutline(): error drawing glyph %s\n' % glyphName
                msg += traceback.format_exc()
                self.errors.append(msg)
                print(msg)

        scale(1/(self.scale))
        translate(-x0, -y0)

    def drawMargin(self, glyph, x, y, width, layerIndex, color, padding=1):
        """Draws left and right margin values underneath the glyph."""
        dy = 0
        if not self._showMarginValues:
            return

        if not color:
            color = (0.5, 0.5, 0.5)

        if glyph.leftMargin and glyph.rightMargin:
            stroke(None)
            r, g, b = color
            fill(r, g, b)
            size = 2
            lm = str(int(round(glyph.leftMargin)))
            rm = str(int(round(glyph.rightMargin)))
            fontSize(self.infoSize)
            wrm, _ = textSize(rm)
            dy += layerIndex * self.infoLeading
            y = y + (self.descender + dy + self.infoLeading)
            xLeft = x + padding
            xRight = x + width - wrm - padding
            self.drawInfoText(lm, xLeft, y)
            self.drawInfoText(rm, xRight, y)
            fill(1)

    def drawKerning(self, glyph, x, y, kerning, dx=0, dy=0):
        """Show kerning value if not 0."""
        k = None

        if not self._showKernValues:
            return

        if kerning == 0:
            return
        elif kerning < 0:
            fill(1, 0, 0)
            k = '%d' % kerning
        elif kerning > 0:
            fill(0, 0.5, 0)
            k = '+%d' % kerning

        stroke(None)
        size = 2
        textHeight = size * 1.2
        yText = y + (self.descender + dy + textHeight + self.infoLeading)
        w, h = textSize(k)
        xLeft = x
        self.drawInfoText(k, xLeft, yText, size)
        fill(1)

    def drawPoints(self, glyph):
        pass
        #for cIndex, contour in enumerate(glyph.contours):
        #for point in contour.points:
        #    print(point)

    def getTruncatedText(self, message, maxWidth, size, offset=15, maxLoops=10):
        """Tests if text fits inside maximum width, else truncates characters
        until it does. Maximum number of loops is used for cutoff to prevent
        infinite recursion."""
        fontSize(size)
        textWidth, _ = textSize(message)
        sw, _ = textSize('...')
        n = 0

        if textWidth > (maxWidth - 2 * offset) * self.scale:
            while textWidth + sw > (maxWidth - 2*offset) * self.scale:
                n += 1
                message = message[:-1]
                textWidth, _ = textSize(message)
                if n > maxLoops:
                    break

            message = message + '...'
            textWidth, _ = textSize(message)

        return message, textWidth

    def drawGlyphName(self, glyphName, glyphWidth, x, y, dx=0, dy=0,
            color='black', offset=15):
        """Draws the glyph name.
        TODO: keep track of overlap.
        """
        if not self._showNames:
            return

        size = 2
        glyphName, textWidth = self.getTruncatedText(glyphName, glyphWidth, size)
        stroke(None)
        if color == 'black':
            fill(0.5)
        elif color == 'red':
            fill(1, 0, 0)
        tw = textWidth / 2
        gw = glyphWidth * self.scale / 2
        x = x + dx - tw + gw
        y = y + self.descender + dy + self.infoLeading
        self.drawInfoText(glyphName, x, y, size)

    def getGlyphNameWidth(self, glyphName):
        """Returns width of glyph name label."""
        fontSize(self.labelSize)
        textWidth, _ = textSize(glyphName)
        return textWidth / self.scale

    def drawGlyphMissing(self, glyphName, x, y, wBox, hBox, layerIndex=0, color=None):
        """Draws glyph name when contours are missing."""
        if not self._showMissing:
            return

        size = 2
        offset = 15
        glyphName, _ = self.getTruncatedText(glyphName, hBox / self.scale, size, offset=offset)

        if color is None:
            fill(0.5)
        else:
            r, g, b = color
            fill(r, g, b)

        stroke(None)
        x0 = x + wBox / 2 + size * layerIndex
        y0 = self.height - y - self.descender + offset * self.scale
        rotate(90)
        position = (y0, -x0)
        text(glyphName, position)
        rotate(-90)

        if DEBUG:
            stroke(1, 0, 0)
            strokeWidth(0.3)
            fill(None)
            x0 = x
            y0 = self.height - y - self.descender
            x1 = x0 + wBox
            y1 = y0 + self.size
            line(x0, y0, x1, y1)
            line(x0, y1, x1, y0)
            stroke(None)

    def drawGlyphSpace(self, x, y, w, h, strokeColor=None):
        """Draws glyph space as a box outline around the glyph. Always
        calculates box dimensions."""
        if self._showGlyphSpace:
            y += self.descender
            y = self.height - y
            fill(None)

            if strokeColor is None:
                stroke(0.5)
            else:
                r, g, b = strokeColor
                stroke(r, g, b)

            strokeWidth(0.3)
            rect(x, y, w, h)

    # Lines.

    def drawLineStart(self, glyphIndex, showSize, showStyleName, y):
        """Optional indented point size and style name."""
        if glyphIndex != 0:
            return

        if showSize:
            # Draws font size (i.e. in case of text progression
            # template).
            fill(0.5)
            self.drawInfoText('%d pt' %  self.size, self.margin, y, size=6)
            fill(1)

        if showStyleName:
            fill(0.5)
            styleName = getStyleKey(self.style)[1]
            self.drawInfoText(styleName, self.margin, y + self.descender + 7.5, size=7)
            fill(1)

    # Pages.

    def drawNewPage(self, styleKeys, pageNumber=1, colors=None,
            sizeString=None, locationString=None):
        """Wrapper for DrawBot newPage(), adds debug features, header and
        footer."""
        self.tool.progressUpdate(text='Drawing page %d' % pageNumber)
        newPage(self.width, self.height)
        self.drawDebug()
        self.drawHeader(styleKeys, pageNumber=pageNumber, colors=colors)
        self.drawFooter(sizeString=sizeString, locationString=locationString)

    def drawHeader(self, styleKeys, pageNumber=1, colors=None):
        """Proof information at top."""
        w, h, margin = self.getPaperSize()
        y0 = h - margin + 2
        stroke(None)
        fill(self.DEFAULTFILL)
        fontSize(self.HEADER_FONTSIZE)
        t = 'Proof: %s (%s) | Family: %s | ' % (self.name, self.getPaperName(),
                self.family.name)
        position = (margin, y0)
        text(t, position)
        textWidth, _ = textSize(t)
        width = margin + textWidth

        if styleKeys:
            if len(styleKeys) > 1:
                t = 'Styles: '
            else:
                t = 'Style: '

            position = (width, y0)
            text(t, position)
            textWidth, _ = textSize(t)
            width += textWidth

            for styleKey in styleKeys:
                styleName = styleKey[1]

                if colors:
                    r, g, b = colors[styleKey]
                    fill(r, g, b)
                else:
                    fill(self.DEFAULTFILL)

                t = styleName + ' '
                position = (width, y0)
                text(t, position)
                textWidth, _ = textSize(t)
                width += textWidth

        fill(self.DEFAULTFILL)

        if self.sampleName is not None:
            t = '| Sample: %s' % self.sampleName
            position = (width, y0)
            text(t, position)

        # Page number.
        pageNumber = '%d' % pageNumber
        textWidth, _ = textSize(pageNumber)
        position = (w - margin - textWidth, y0)
        text(pageNumber, position)

    def drawFooter(self, sizeString=None, locationString=None):
        _, _, margin = self.getPaperSize()
        now = datetime.datetime.now()
        t = ['%s, %s %s' % (now.year, self.MONTHS[now.month-1], now.day)]
        t.append('%02d:%02d:%02d' % (now.hour, now.minute, now.second))

        if sizeString is not None:
            t.append(sizeString)

        if not self.name in ('Kerning Map'):
            t.append('Leading: %0.1fem' % self._leading)

        if locationString:
            t.append(locationString)

        stroke(None)
        fill(self.DEFAULTFILL)
        position = (margin, margin - self.HEADER_FONTSIZE * self.HEADER_LEADING)
        text(' | '.join(t), position)
        #fill(0)

    def drawInfoText(self, t, x, y, size=None):
        """Draw line of info text (e.g. a label) at this position."""
        if not size:
            size = self.infoSize

        fontSize(size)
        position = (x, self.height - y)
        text(t, position)

    # Errors & debugging.

    def drawDebug(self):
        if not DEBUG:
            return

        w, h, margin = self.getPaperSize()
        fill(None)
        stroke(1, 0, 0)
        strokeWidth(0.5)
        rect(margin, margin, w - 2*margin, h - 2*margin)
        fill(0, 0, 0)
        stroke(None)

    def drawDebugLine(self, y, r=0, g=0, b=0, size=7, message=None):
        if not DEBUG:
            return

        w, h, margin = self.getPaperSize()
        fill(None)
        strokeWidth(0.1)
        stroke(r, g, b)
        line((margin, h - y), (w - margin, h - y))
        fill(0, 0, 0)
        stroke(None)
        fontSize(size)
        t = 'y = %d' % y
        position = (w - margin, h - y)
        text(t, position)
        if message is not None:
            position = (w - margin, h - y - 9)
            text(message, position)

    # Auxilliary getters.

    def getCustomFontSizes(self):
        """
        Parses font sizes from custom font size entry box.
        """
        fontSizes = []
        parts = self._customFontSize.split(',')

        for part in parts:
            try:
                if '.' in part:
                        part = float(part)
                size = int(part)

                if size > 0:
                    fontSizes.append(size)
            except:
                print('Cannot parse %s' % part)

        return fontSizes

    def getInfoLeading(self):
        leading = 1.0

        if self._showNames:
            return 2 * leading
        elif self._showMarginValues:
            return 2 * leading
        else:
            return 0

    # Sorting.

    def getSortedGlyphNames(self, style, glyphNames):
        """Converts the RoboFont sorting order to a list of glyph names.

        Bypassing defCon sorting seems to work, looks like RoboFont always
        returns a presorted 'ascending' list."""
        sortDescriptors = self.getSortDescriptors(style)

        if sortDescriptors is None:
            return glyphNames

        sortDescriptor = sortDescriptors[0] # Always just one?
        sortedGlyphNames = []

        if isinstance(style, Style):
            # TTF's and OTF's are encapsulated in a style.
            if isinstance(style.storage,  UFOStorage):
                glyphOrder = sortDescriptor['ascending'] # Always 'ascending'?
            elif isinstance(style.storage,  OTFStorage):
                return sorted(glyphNames)
        else:
            try:
                # Maybe running as a tool, might be a DoodleFont. We don't
                # want to import mojo so just do trial and error.
                glyphOrder = self.getGlyphOrder(style, sortDescriptors)
            except:
                # Running as an application, UFO's are DefCon fonts.
                glyphOrder = sortDescriptor['ascending'] # Always 'ascending'?

        for glyphName in glyphOrder:
            if glyphName in glyphNames:
                sortedGlyphNames.append(glyphName)

        return sortedGlyphNames

    def getGlyphOrder(self, style, sortDescriptors, allowTemplateGlyphs=True):
        """Function adapted from RoboFont font overview.

        NOTE: deprecated -- accessing sortDescriptor dictionary directly."""
        glyphNames = style.unicodeData.sortGlyphNames(style.keys(),
                sortDescriptors=sortDescriptors)

        if not allowTemplateGlyphs:
            glyphNames = self.ignoreTemplateGlyphs(style, glyphNames)

        return glyphNames

    def getSortDescriptors(self, style):
        """Reads out user defined RoboFont glyph sorting order if set, or else
        the default RoboFont sorting order."""
        sortDescriptors = None

        if self._sortGlyphs:
            sortDescriptors = getDefault("sortDescriptors")
            glyphOrder = style.lib.get("public.glyphOrder")

            if glyphOrder is None:
                sortDescriptors = style.lib.get("%s.sort" %
                        doodleLibIdentifier, sortDescriptors)
            else:
                sortDescriptors = [dict(type="glyphList", ascending=glyphOrder)]

        return sortDescriptors

    # Bitmap.

    def getGlyphBitmap(self, glyph):
        """Based on RoboFont bitmap representation. Returns a bitmap rendering
        of a glyph at a certain scale. TODO: double check if pixel sizes
        correspond to font sizes.
        """
        from tnbits.base.robofont.defaults import getDefaultColor

        path = glyph.getRepresentation("defconAppKit.NSBezierPath").copy()
        scale = self.scale / 2 # Divided by 2 for retina?

        if path.isEmpty():
            return

        (px, py), (pw, ph) =  path.bounds()
        if pw == 0 or ph == 0:
            return

        at = NSAffineTransform.transform()
        at.scaleXBy_yBy_(scale, scale)

        # Translate to make sure area outside glyph space is drawn.
        at.translateXBy_yBy_(-px, -py)
        path.transformUsingAffineTransform_(at)

        # Draw first to render entire image?
        path.moveToPoint_((0, 0))
        path.lineToPoint_((px, py))
        bitmap = NSImage.alloc().initWithSize_((pw * scale, ph * scale))
        bitmap.lockFocus()
        color = getDefaultColor("glyphViewBitmapColor")
        color.set()
        path.fill()
        bitmap.unlockFocus()
        return bitmap, (px, py)

    # Paper.

    def getPaperSize(self):
        """Gets size, considers portrait / landscape orientation."""
        return self.paperSize[1]

    def getPaperName(self):
        """Gets size, considers portrait / landscape orientation."""
        return self.paperSize[0]

    # Kerning.

    def getFlatKernings(self, styleKeys):
        """Puts flat kerning in a dictionary for each style."""
        flatKernings = {}

        for styleKey in styleKeys:
            style = self.family.getStyle(styleKey)
            assert style.kerning is not None

            if not hasattr(style, 'groups'):
                print('No groups in %s' % str(style))
                # TODO: add to errors.
                continue

            flatKerning = None

            try:
                flatKerning, groupsUsed, groupsNotUsed, exceptions = explodeKerning(style.kerning, style.groups)
            except FloqError as e:
                print(traceback.format_exc())

            # TODO: add to groups not used to errors.
            # TODO: add exceptions to errors.

            flatKernings[styleKey] = flatKerning

        return flatKernings

    def splitKerningPairs(self, expandedKernings):
        """Splits kerning pairs into sorted sets of left and right glyph
        names."""
        left = set()
        right = set()

        if not expandedKernings is None:
            for styleKey in expandedKernings.keys():
                pairs = expandedKernings[styleKey].keys()
                left.update([l for l, _ in pairs])
                right.update([r for _, r in pairs])

            left = sorted(left, reverse=True)
            right = sorted(right)

        return left, right

    def ignoreTemplateGlyphs(self, style, glyphNames):
        return [glyphName for glyphName in glyphNames if not style[glyphName].template]

    def getPath(self, styleKeys, size=None, sizeString=None):
        """Normalized output file name for all the templates."""
        proofPath = self.getOutputPath()
        styleNames = []

        for styleKey in styleKeys:
            n = styleKey[1]
            n = n.replace(self.family.name, '')
            n = n.replace('.ufo', '')
            n = n.replace('-', '')
            n = n.replace('_', '')
            n = n.replace(' ', '')
            styleNames.append(n)

        if not sizeString:
            sizeString = '%dpt' % size

        templateName = self.name.replace(' ', '_')
        fileName = '%s-%s-%s' % (self.family.name, sizeString, templateName)

        if self.sampleName:
            sampleName = self.sampleName.replace(' ', '_')
            fileName += '-%s' % sampleName

        path = '%s/%s' % (proofPath, fileName)
        ext = '.pdf'
        i = 1

        # TODO: what do we do when we reach 99?
        while i < 100 and os.path.exists(path + ext):
            if i != 1:
                path = path[:-3]

            path = path + '.%02d' % i
            i += 1

        return path + ext

    def getOutputPath(self):
        """Calculates the path for the proofs of the given style. Create the
        directory if is doesn't exist."""
        familyName = self.family.name or 'unknown'
        proofFolder = 'proof-%s' % familyName
        proofPath = '/'.join(self.family.familyID.split('/')[:-1]) + '/%s' % proofFolder

        if not os.path.exists(proofPath):
            os.makedirs(proofPath)

        return proofPath

    def checkGlyph(self, glyph):
        """Checks if there are any problems with this glyph. Append detected
        errors."""
        ga = analyzerManager.getGlyphAnalyzer(glyph)
        return ga.validate()

    # Errors & debug.

    def printKerning(self, kerning):
        """Verbose output of kerning samples.
        NOTE: Only for debugging, very slow for big fonts."""
        for pair, value in kerning.items():
            print(pair, value)

    def verboseStyle(self, style, sample):
        s = ''
        i = 0
        s += '%s\n' % type(style)

        for g in compiledText(sample):
            s += '%s, %s, %s\n' % (g, type(g), style[g])
            i += 1
            if i >= 30:
                break

        print(s)

