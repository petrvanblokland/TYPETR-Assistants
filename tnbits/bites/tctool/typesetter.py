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
#    typesetter.py
#

import math

from fontTools.misc.transform import Transform
from AppKit import (NSCommandKeyMask, NSShiftKeyMask, NSAlternateKeyMask,
        NSUpArrowFunctionKey, NSDownArrowFunctionKey, NSLeftArrowFunctionKey,
        NSRightArrowFunctionKey, NSColor, NSBackspaceCharacter,
        NSDeleteFunctionKey, NSDeleteCharacter, NSBezierPath, NSPointInRect,
        NSGraphicsContext, NSAffineTransform, NSMakeRect, NSMakePoint,
        NSFontAttributeName, NSFont, NSForegroundColorAttributeName,
        NSAttributedString, NSControlKeyMask, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey, NSTimer)
from datetime import datetime, timedelta
import traceback
from random import random

from tnbits.base.constants.colors import *
from tnbits.base.constants.tool import *
from tnbits.base.expandtext import expandText
from tnbits.base.groups import (getGroupKerning, isLocked, toggleLock,
        getGroupBaseGlyphName, changeSpacing, changeKerning, equalizeSpacing)
from tnbits.base.samples import SAMPLE_TAGS, RE_GLYPHNAMES, compileText, getGlyphName
from tnbits.base.tools import getLog, setLog
from tnbits.toolbox.character import CharacterTX
from tnbits.canvas.canvas import Canvas
from tnbits.canvas.kit import CanvasKit
from tnbits.canvas.eventhandler import CanvasEventHandler
from tnbits.bites.tctool.constants import *
from tnbits.bites.tctool.cache import Cache
from tnbits.bites.tctool.menu import Menu
from tnbits.bites.tctool.searchbox import SearchBox

def between(y0, y1, y2):
    if y0 > y1 and y0 < y2:
        return True
    return False

class Typesetter():
    """Typesetting canvas. Displays the sample text and provides an interface
    to set kerning and spacing values for groups."""

    def __init__(self, controller):
        self.controller = controller
        self.setGlobals()
        self.cache = Cache(controller)
        self.canvas = Canvas((0, 0, -0, -0), delegate=self,
                canvasSize=(self.width, self.height), acceptsMouseMoved=True,
                hasHorizontalScroller=True, hasVerticalScroller=True,
                autohidesScrollers=False, backgroundColor=None,
                drawsBackground=True, flipped=True)
        self.kit = CanvasKit()
        self.eventHandler = CanvasEventHandler(self.canvas)
        self.setSearchBox()

    def setGlobals(self):
        self._tStart = []
        self._tEnd = []
        self._pageOrder = []
        self._pages = []
        self._stringLabels = {}
        self._doUpdateOnMouseUp = False
        self._lastKey = ''
        self._sampleCache = {}
        self._bounds = None

        # Page width and height, in pixels. Update to actual values after a
        # typeset().
        self.width = 1000
        self.height = 1000
        self.sampleIndex = 0
        self.pageIndex = 0
        self.lastClick = None
        self.timer = None
        self.running = False
        self.stepX = 0
        self.characters = ''
        # Keydown reaction interval.
        self.interval = 0.2
        # Timer polling interval every 100 ms.
        self.timerInterval = 0.01

    def __len__(self):
        return len(self._pages)

    def getCanvasView(self):
        return self.canvas.getCanvasView()

    # Transformations.

    def _transform(self, transform):
        t = NSAffineTransform.alloc().init()
        t.setTransformStruct_(transform[:])
        t.concat()

    def scale(self, x=1, y=None):
        if y is None:
            y = x
        t = Transform().scale(x, y)
        self._transform(t)

    def translate(self, x, y, flip=True):
        """Moves to x, y and optionally turns upside down."""
        affineTransform = NSAffineTransform.transform()
        affineTransform.translateXBy_yBy_(x, y)

        if flip:
            affineTransform.scaleXBy_yBy_(1, -1)
            affineTransform.concat()

    # Timing.

    def moreThanInterval(self):
        """Checks if time passed since last event is larger than keydown
        reaction interval."""
        if self.lastClick is None:
            return True
        now = datetime.now()
        dt = now - self.lastClick
        sec = timedelta(seconds=self.interval)
        return dt > sec

    def setTimer(self):
        """Sets a new polling timer with a fixed interval that is shorter than
        the keydown reaction interval."""
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(self.timerInterval, self, 'timerDoneHandler:', None, False)

    def timerDoneHandler_(self, timer):
        """Update groups if time after last click is larger than the interval.
        Else set a new timer."""
        self.timer = None

        if self.moreThanInterval():
            #self.doGroups(characters, self.stepX)
            self.doGroups()
            self.update(typesetVisible=True)
        else:
            self.setTimer()

    # Search.

    def setSearchBox(self):
        """Editable cell to be moved to a cell position on enter."""
        self.canvas.searchBox = SearchBox((100, 100, 300, 20), "",
                callback=self.searchCallback)
        self.canvas.searchBox.searchBoxEnded = self.closeSearchBox
        self.canvas.searchBox.show(False)
        self.searchBoxIsVisible = False

    def searchCallback(self, sender):
        glyphName = str(sender.get())

        if glyphName.strip() != '':
            self.search(glyphName)

    def search(self, glyphName):
        """Matches the first glyph name on the page."""
        found = self.findGlyph(glyphName)

        if not found:
            # TODO: statusbar feedback.
            print('%s not found' % glyphName)

    def findGlyph(self, glyphName):
        for y, line in self.cache.getLines().items():

            for x, textItem in line.items():
                if textItem.name == glyphName:
                    self.setSelected(textItem)
                    self.scrollTo(textItem)
                    visible = self.cache.isVisible(textItem.yIndex)
                    self.update(typesetVisible=visible)
                    return True

        return False

    def closeSearchBox(self):
        """Processes cell contents after search, makes the spreadsheet canvas
        become first responder again."""
        # FIXME: current cell disappears after search.
        # FIXME: check if searched text is a float.
        self.canvas.searchBox.show(False)
        self.searchBoxIsVisible = False
        view = self.getCanvasView()
        view.window().makeFirstResponder_(view)
        value = self.canvas.searchBox.get()

    def openSearchBox(self):
        """Opens a TextField search box."""
        self.canvas.searchBox.setPosSize((100, 100, 300, 30))
        #self.canvas.searchBox.set('bla')
        self.canvas.searchBox.show(True)
        self.canvas.searchBox.getNSTextField().becomeFirstResponder()
        self.searchBoxIsVisible = True

    def refresh(self):
        self.setPage(self.pageIndex)

    # Get.

    def getStyle(self):
        return self.controller.style

    def getNSView(self):
        return self.canvas.getNSView()

    def getEditMode(self):
        return self.controller._editMode

    def setHover(self, mouse):
        """Finds the glyph that we are currently hovering over. Updates the
        position of the red rectangle. Disables the hover glyph if the mouse is
        not inside any glyph area.

        TODO: update canvas based on previous position again.

        """
        style = self.getStyle()
        lines = self.cache.getLines()

        if style is None or lines is None:
            return

        mouseX, mouseY = mouse
        textScale = self.controller.getTextScale()
        yIndex = self.getScaledValueToIndex(mouseY)

        if not yIndex is None:
            line = lines.get(yIndex)

            if line:
                for _, textItem in sorted(line.items()):
                    x = textItem.x
                    width = textItem.width
                    x2 = x + width

                    if x * textScale <= mouseX <= x2 * textScale:
                        # Still the same.
                        if self.cache.isHoverItem(textItem):
                            return
                        else:
                            self.cache.setHoverIndex(textItem)
                            self.canvas.update()
                            return

        self.resetHover()

    def getStepSize(self, event):
        """Square the distance for >= 4, until larger than stepX * 10, then
        truncate."""
        modifiers = event.modifierFlags()
        commandDown = modifiers & NSCommandKeyMask
        shiftDown = modifiers & NSShiftKeyMask
        optionDown = modifiers & NSAlternateKeyMask
        stepX = self.controller._stepSize

        if shiftDown:
            if stepX >= 4:
                # 4 --> 16, 6 --> 36, 8 --> 64, 10 --> 100, 20 --> 200
                stepX = min(stepX * stepX, stepX * 10)
            else:
                # For small steps, multiply by 5.
                # 1 --> 5, 2 --> 10, 3 --> 15
                stepX = stepX * 5

        #TODO : make this work
        #if optionDown:
        #    stepX = 1

        return stepX

    def getFeatureGlyphNames(self, glyphNames):
        """Expands features if feature controller and featureCompiler are
        installed.

        TODO: finish implementation.
        """
        stylePath = self.getStyle().path

        if stylePath in self.controller._featureCompilers and \
                stylePath in self.controller._featureViewers:
            featureViewer = self.controller._featureViewers[stylePath]
            featureCompiler = self.controller._featureCompilers[stylePath]
            #featureSettings = dict(case='Unchanged', script='latn', language='dflt',
            #    gsub=dict(ss07=False, ss04=True, smcp=False, frac=True))
            return featureCompiler.getCompiledGlyphNames(featureViewer.get(), glyphNames)

    def getPageName(self, page):
        # First 20 characters of first word. Replace escaped slash.
        i = 0
        name = ''
        for c in page:
            if i == 20:
                break

            char = CharacterTX.glyphName2Char(c)

            if char is None:
                print('Can\'t look up name for %s, type is %s' % (c, type(c)))
                continue

            name += char
            i += 1

        return name

    def getPageNames(self):
        return self._pageOrder

    def getUIText(self):
        page = self._pages[self.pageIndex]
        text = ''

        for c in page:
            text += '/' + c

        return text

    def getIndexToScaledValue(self, yIndex, baseLine=True):
        """Converts index to scaled pixel coordinate, origin is at the top. If
        baseLine is True, adds (negative) descender value."""
        upem = self.controller.getUpem()
        lineHeight = self.controller.getLineHeight()
        textScale = self.controller.getTextScale()
        y = yIndex * lineHeight + M / textScale + upem

        if baseLine:
            descender = self.controller.getDescender()
            return y + descender
        else:
            return y

    def getScaledValueToIndex(self, y):
        """Converts scaled pixel coordinate to index. If baseLine is True,
        subtracts (negative) descender value first."""
        upem = self.controller.getUpem()
        lineHeight = self.controller.getLineHeight()
        textScale = self.controller.getTextScale()
        y = y / textScale
        m = M / textScale

        if y < m:
            return 0

        return int((y - m) / lineHeight)

    def getControlsHeight(self):
        gutter0, _, buttonWidth = self.getControlSizes()
        if self.controller.hasOverlayRelated():
            lines = 4
        else:
            lines = 3

        return lines * (buttonWidth + gutter0)

    def getNSString(self, textType, label, size, color):
        # Test on cached string label.
        # FIXME: caches different sizes, colors under same key.
        key = textType + label
        nsString = self._stringLabels.get(key)

        if nsString is None:
            # Prepare the text attributes.
            attributes = {
                NSFontAttributeName : NSFont.boldSystemFontOfSize_(size),
                NSForegroundColorAttributeName : color
            }
            nsString = NSAttributedString.alloc().initWithString_attributes_(label , attributes)
            self._stringLabels[key] = nsString

        return nsString

    def getControlSizes(self):
        """Calculates sizes for control interface."""
        textScale = self.controller.getTextScale()
        gutter0 = 3 / textScale
        gutter1 = gutter0 / 2
        buttonWidth = LABEL_SIZE * 1.4 / textScale
        return gutter0, gutter1, buttonWidth

    def getGlyphLabel(self, textItem, glyph, glyphName):
        label = glyphName

        if glyph.unicode:
            label = '%s | #%04X' % (label, glyph.unicode)

        if self.controller._showNumbers:

            label = '%s: %s' % (textItem.getIdentifier(), label)

        return label

    def getView(self):
        """Returns the view, which in this case is the canvas."""
        return self.canvas

    def getUITextColor(self, opaque=False):
        colorScheme = self.controller.getColorScheme()

        if colorScheme == REGULAR:
            if not opaque:
                return blackColor
            else:
                return opaqueBlackColor
        elif colorScheme == DIA:
            if not opaque:
                return whiteColor
            else:
                return opaqueWhiteColor
        elif colorScheme == COLOR:
            if not opaque:
                return UIGrey
            else:
                return UIOpaqueGrey

    def getRegularBox(self, x, y, w, h):
        # TODO: merge with slanted, pass tangent parameter.
        return NSBezierPath.bezierPathWithRect_(((x, y), (w, h)))

    def getSlantedBox(self, x, y, w, h):
        # TODO: merge with regular, pass tangent parameter.
        path = NSBezierPath.bezierPath()
        t = self.controller.getTangent()
        y1 = y + h
        path.moveToPoint_((x + y * t, y))
        path.lineToPoint_((x + y1 * t, y1))
        path.lineToPoint_((x + y1 * t + w, y1))
        path.lineToPoint_((x + y * t + w, y))
        path.lineToPoint_((x + y * t, y))
        return path

    # Set.

    def setPage(self, i, update=True):
        self.pageIndex = i

        if update:
            self.update()

    def setSample(self, index, pageIndex=0, update=True):
        """Calculates the new expanded feature text source. Updates the canvas
        and calculate the flow of text lines."""
        sampleName = SAMPLENAMES[index]
        sample = SAMPLES[index]

        if isinstance(sample, (tuple, list)):
            # Already a list of glyph names.
            t = ' '.join(sample)
        elif sample in SAMPLE_TAGS:
            # Dynamically expanded glyph set using the expandText() function
            # from tnbits.base.
            groups = self.controller.getGroups()
            t = expandText(self.getStyle(), sample, groups)
        else:
            # Already a valid sample.
            t = sample

        self.setPages(t, pageIndex)
        self.sampleIndex = index
        if update:
            self.update()

    def setPages(self, t, pageIndex=0):
        """Splits up glyph set into separate pages depending on number of
        glyphs per apge. Uses compileText() from tnbits.base. Keeps track of
        page indices and order."""
        self._pageOrder = []
        self._pages = []
        glyphNames = compileText(t)
        pages = self.splitPages(glyphNames)

        # FIXME: start and end glyphs are added to page names.
        for i, page in enumerate(pages):
            name = self.getPageName(page)
            self._pageOrder.append(name)
            self._pages.append(page)

        assert pageIndex < len(self._pages)
        self.pageIndex = pageIndex

    def getNumberOfPages(self):
        return len(self._pages)

    def getPageNumber(self):
        return self.pageIndex

    # Reset.

    def reset(self):
        self.resetLabels()
        self.resetHover()

    def resetLabels(self):
        """Clears cache of string labels."""
        self._stringLabels = {}

    def resetHover(self):
        """Deselects hover item. Updates entire visible canvas are for now."""
        if self.cache.resetHover():
            self.canvas.update()

    # Drawing.

    def draw(self, rect):
        """Main routine that is called after canvas update(). Inside try-except
        statement to prevent crashing during a draw operation when an error
        occurs."""

        try:
            self.drawBackground(rect)
            self.drawGrid()
            self.drawMargins()
            self.drawLines()

            if self.controller.family is None:
                return

            self.drawAllKerningValues()
            self.drawControls()
            self.drawHover()
            self.drawNumbers()
            self.drawMeasures()
        except:
            print(traceback.format_exc())

    def drawLines(self):
        if self.canvas.getCanvasView().resizing:
            self.typeset()

        bounds = self.canvas.getClipBounds()

        # Recalculates values for entire page if only the visible lines
        # have been updated and bounds have changed, i.e. the page has been
        # scrolled (entire reflow needed due to different spacing /
        # kerning) or resized (line width has changed).
        if self.cache.isDirty() and bounds != self._bounds:
            self.cache.clearVisible()
            self.typeset()
            self.cache.setDirty(False)

        # Check if there is something to draw.
        if self.getStyle() is None:
            return

        elif not self.cache.hasLines():
            return

        lines = self.cache.getLines()


        # Draws all the visible glyph lines.
        for yIndex, line in sorted(lines.items()):
            if self.yIndexIsVisible(yIndex):
                self.drawGlyphLine(yIndex, line)

    def drawBackground(self, rect):
        """Draws the background color."""
        colorScheme = self.controller.getColorScheme()

        if colorScheme == REGULAR:
            WHITECOLOR.set()
        elif colorScheme == DIA:
            BLACKCOLOR.set()
        elif colorScheme == COLOR:
            UILightBlue.set()

        path = NSBezierPath.bezierPathWithRect_(rect)
        path.fill()

    def drawGlyphLine(self, yIndex, line):
        """Draws a single line of glyphs for yIndex."""
        for x, textItem in line.items():
            width = textItem.width

            glyphName = textItem.name

            if textItem.missing:
                self.drawMissing(x, yIndex, glyphName, width)
            elif glyphName in self.getStyle():
                glyph = self.getStyle()[glyphName]
                self.drawGroupMargins(x, yIndex, glyphName, width)

                if self.controller._showMarkColors and glyph.markColor:
                    self.drawMarkColor(glyph.markColor, x, yIndex, width)

                self.drawGroups(x, yIndex, glyphName, width)
                self.drawGlyph(x, yIndex, glyphName, glyph, width)
                self.drawComponents(x, yIndex, glyphName, glyph)
                self.drawAnchors(x, yIndex, glyphName, glyph)

            if self.controller._showMetrics:
                self.drawMetrics(x, yIndex, width)

    def drawMarkColor(self, markColor, x0, yIndex, width):
        """Shows mark colors as set in RoboFont."""
        if not self.yIndexIsVisible(yIndex):
            return

        NSGraphicsContext.saveGraphicsState()
        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        descender = self.controller.getDescender()
        y0 = self.getIndexToScaledValue(yIndex, baseLine=False) - upem
        self.scale(textScale)
        self.translate(x0, y0)
        r, g, b, a = markColor
        h = upem * 0.05
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)


        t = self.controller.getTangent()

        if t == 0:
            self.kit.drawRectangle(0, -h, width, h, fillColor=color, strokeColor=None)

        else:
            color.set()
            x0 = t * (upem + descender)
            path = self.getSlantedBox(x0, 0, width, -h)
            path.fill()

        NSGraphicsContext.restoreGraphicsState()

    def drawGroups(self, x0, yIndex, glyphName, width):
        """Shows an orange triangle for all glyphs in left group and a blue one
        for right."""
        # TODO: calculate from baseline to get correct slant offset.
        if not self.controller._showGroupGlyphs:
            return
        if not self.yIndexIsVisible(yIndex):
            return

        t = self.controller.getTangent()
        NSGraphicsContext.saveGraphicsState()
        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        descender = self.controller.getDescender()
        y0 = self.getIndexToScaledValue(yIndex)
        self.scale(textScale)
        self.translate(x0, y0)
        style = self.getStyle()
        sq = upem * 0.05
        l = self.controller.getSelectedGroup()
        r = self.controller.getSelectedGroup(left=False)
        y = upem + descender - sq
        w = sq
        h = sq

        if l:
            if glyphName in l:
                x = 0

                self.kit.drawGroupMarker(x, y, w, h, t,
                        fillColor=orangeColor, strokeColor=None)
        if r:

            if glyphName in r:
                x = width - sq

                self.kit.drawGroupMarker(x, y, w, h, t,
                        fillColor=cyanColor, strokeColor=None, left=False)

        NSGraphicsContext.restoreGraphicsState()

    def drawGroupMargins(self, x0, yIndex, glyphName, width):
        """Shows a red border in case of group margin mismatch for left and
        right."""
        if not self.controller._compareGroupMargins:
            return
        if not self.yIndexIsVisible(yIndex):
            return

        NSGraphicsContext.saveGraphicsState()
        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        descender = self.controller.getDescender()
        t = self.controller.getTangent()
        y0 = self.getIndexToScaledValue(yIndex, baseLine=False)
        self.scale(textScale)
        self.translate(x0, y0)
        leftName = self.controller.getSelectedGroupName()
        l = self.controller.getSelectedGroup()
        rightName = self.controller.getSelectedGroupName(left=False)
        r = self.controller.getSelectedGroup(left=False)
        c1 = opaquePurpleColor
        c2 = opaqueRedColor

        # TODO: separate function that does either left or right.
        if l:
            if glyphName in l:
                leftBaseName = getGroupBaseGlyphName(leftName)
                if leftBaseName == glyphName:
                    c = c1
                else:
                    c = c2

                if glyphName in self.controller._leftMismatches:
                    if t == 0:
                        self.kit.drawRectangle(0, 0, width / 20, upem,
                                fillColor=c, strokeColor=None)
                    else:
                        c.set()
                        x0 = descender * t
                        path = self.getSlantedBox(x0, 0, width / 20, upem)
                        path.fill()

        if r:
            if glyphName in r:
                rightBaseName = getGroupBaseGlyphName(rightName)
                if rightBaseName == glyphName:
                    c = c1
                else:
                    c = c2

                if glyphName in self.controller._rightMismatches:
                    if t == 0:
                        w = width / 20
                        x = width - w
                        self.kit.drawRectangle(x, 0, w, upem, fillColor=c,
                                strokeColor=None)
                    else:
                        c.set()
                        w = width / 20
                        x0 = width + descender * t - w
                        path = self.getSlantedBox(x0, 0, w, upem)
                        path.fill()

        NSGraphicsContext.restoreGraphicsState()

    def drawNumbers(self):
        # TODO: draw white in case of dia.
        if not self.controller._showNumbers:
            return

        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        color = self.getUITextColor()
        lines = self.cache.getLines()

        for yIndex in sorted(lines.keys()):
            if self.yIndexIsVisible(yIndex):
                x = M / 2
                y = (self.getIndexToScaledValue(yIndex) - upem / 2) * textScale
                self.kit.drawText(str(yIndex), x, y, color=color)

        x = self.width - M
        y = self.height - M
        t = '%s / %s' % (self.pageIndex + 1, len(self))
        self.kit.drawText(t, x, y, color=color, align='right')

    def drawMeasures(self, unit='px'):
        # TODO: draw white in case of dia.
        # TODO: make italic.
        # TODO: add units.
        if not self.controller._showMeasures:
            return

        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        color = magentaColor
        lines = self.cache.getLines()

        for yIndex in sorted(lines.keys()):
            x = M / 2
            y = (self.getIndexToScaledValue(yIndex)) * textScale
            y = round(y, 1)
            self.kit.drawText('y=%s%s' % (y, unit), x, y - 20, color=color, padding=0)
            self.kit.drawCircle(x-2, y-2, 4, 4, fillColor=color)
            line = lines[yIndex]

            y0 = (self.getIndexToScaledValue(yIndex, baseLine=False)) * textScale
            y0 = round(y0, 1)
            self.kit.drawText('y=%s%s' % (y0, unit), x, y0 - 20, color=color, padding=0)
            self.kit.drawCircle(x-2, y0-2, 4, 4, fillColor=color)

            upem = self.controller.getUpem() * textScale
            y1 = y0 - upem
            y1 = round(y1, 1)
            self.kit.drawText('y=%s%s' % (y1, unit), x, y1 - 20, color=color, padding=0)
            self.kit.drawCircle(x-2, y1-2, 4, 4, fillColor=color)

            for x in line:
                x = x * textScale
                x = round(x, 1)
                self.kit.drawText('x=%s%s' % (x, unit), x, y, color=color, padding=0)
                self.kit.drawCircle(x-2, y-2, 4, 4, fillColor=color)

        # Bottom left corner.
        x = M
        y = self.height - M
        self.kit.drawText('y=%s%s' % (y, unit), x, y - 20, color=color, padding=0)
        self.kit.drawCircle(x-2, y-2, 4, 4, fillColor=color)

    def drawGlyph(self, x, yIndex, glyphName, glyph, width):
        """Draws the glyph from the glyph representation (it may have changed
        by the editor, so we don't want to keep it in the textItem."""
        textScale = self.controller.getTextScale()
        y = self.getIndexToScaledValue(yIndex)

        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        self.translate(x, y)

        if self.controller.hasOverlayRelated():
            relatedStyle = self.controller.relatedStyle
            color = self.getUITextColor(opaque=True)
            color.set()

            if glyphName in relatedStyle:
                relatedGlyph = relatedStyle[glyphName]
                path = relatedGlyph.getRepresentation("defconAppKit.NSBezierPath")
                path.setLineWidth_(self.controller._strokeWidth / textScale)
                path.stroke()
        else:
            color = self.getUITextColor()
            color.set()

        path = glyph.getRepresentation("defconAppKit.NSBezierPath")
        path.fill()

        NSGraphicsContext.restoreGraphicsState()
        return glyph

    def drawComponents(self, x, yIndex, glyphName, glyph):
        """Draws component boxes."""
        if not self.controller._showComponents:
            return

        textScale = self.controller.getTextScale()
        y = self.getIndexToScaledValue(yIndex)

        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        self.translate(x, y)
        strokeWidth = self.controller._strokeWidth / textScale

        if glyph.components:
            for c in glyph.components:
                if not c.bounds:
                    continue

                xMin, yMin, xMax, yMax = c.bounds
                self.kit.drawRectangle(xMin, yMin, xMax - xMin, yMax - yMin,
                        fillColor=None, strokeColor=orangeColor,
                        width=strokeWidth)

        NSGraphicsContext.restoreGraphicsState()

    def drawAnchors(self, x, yIndex, glyphName, glyph):
        """Draws component boxes."""
        if not self.controller._showAnchors:
            return

        textScale = self.controller.getTextScale()
        y = self.getIndexToScaledValue(yIndex)

        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        self.translate(x, y)
        strokeWidth = self.controller._strokeWidth / textScale
        style = self.getStyle()

        if glyph.components:
            for c in glyph.components:
                if not c.transformation:
                    continue

                _, _, _, _, x, y = c.transformation

                baseGlyph = style[c.baseGlyph]
                xMin1, _, yMin1, _ = baseGlyph.bounds

                for anchor in baseGlyph.anchors:
                    x0 = anchor.x
                    y0 = anchor.y
                    name = anchor.name
                    d = 10
                    d1 = 20
                    c = orangeColor
                    self.kit.drawCircle(x0 - d/2, y0 - d/2, d, d,
                            fillColor=c)
                    self.kit.drawCircle(x0 + x - d1/2, y0 + y - d1/2, d1, d1,
                            strokeColor=c)
                    offset = 10
                    self.drawTextLabel('?', name, x0 + offset, y0 + offset, c,
                            'center')
                    self.kit.drawLine((x0, y0), (x0 + x, y0 + y), color=c, width=1)

        NSGraphicsContext.restoreGraphicsState()

    def drawMissing(self, x, yIndex, glyphName, width):
        """If the glyph does not exists, show colored rectangle + example of
        glyph.

        FIXME: error in width calculation.

        """
        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        descender = self.controller.getDescender()
        cName = CharacterTX.glyphName2Char(glyphName)
        fSize = upem / 2
        LIGHTBLUECOLOR.set()
        indent = 0.5 / textScale
        x0 = indent
        y0 = descender + indent
        w = width - 2 * indent
        h = upem - 2 * indent

        attributes = {
            NSFontAttributeName: NSFont.systemFontOfSize_(fSize),
            NSForegroundColorAttributeName: LIGHTGREYCOLOR
        }

        if not cName:
            cName = glyphName
            fSize = 100

        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        y = self.getIndexToScaledValue(yIndex)
        self.translate(x, y)

        t = self.controller.getTangent()

        if t == 0:
            path = self.getRegularBox(x0, y0, w, h)
        else:
            path = self.getSlantedBox(x0, y0, w, h)

        path.fill()

        nsString = NSAttributedString.alloc().initWithString_attributes_(cName,
                attributes)
        nameWidth, nameHeight = nsString.size()
        x = width / 2 - nameWidth / 2
        y = -600
        self.translate(0, 0)

        nsString.drawInRect_(NSMakeRect(x, y, nameWidth, nameHeight))
        NSGraphicsContext.restoreGraphicsState()

    def drawMetrics(self, x, yIndex, width):
        NSGraphicsContext.saveGraphicsState()
        style = self.getStyle()
        descender = self.controller.getDescender()
        upem = self.controller.getUpem()
        textScale = self.controller.getTextScale()
        self.scale(textScale)
        y = self.getIndexToScaledValue(yIndex)
        #self.drawTextLabel('?', '%s, %s' % (x, y), x, y+descender, blackColor, 'left')
        self.translate(x, y)
        t = self.controller.getTangent()

        # Bounding box.

        if t == 0:
            # Straight box if regular.
            path = self.getRegularBox(0, descender, width, upem)
        else:
            # Slanted box if italic.
            path = self.getSlantedBox(0, descender, width, upem)

        colorScheme = self.controller.getColorScheme()

        if colorScheme in (REGULAR, DIA):
            METRICSBGCOLOR.set()
        elif colorScheme == COLOR:
            blueColor.set()

        path.setLineWidth_(0.5 / textScale)
        path.stroke()

        # Base line.
        path = NSBezierPath.bezierPath()
        path.setLineWidth_(0.5 / textScale)
        path.moveToPoint_((0, 0))
        path.lineToPoint_((width, 0))
        path.stroke()
        NSGraphicsContext.restoreGraphicsState()

    def drawMissingMarker(self, textItem):
        """Draws a marker for a missing glyph. Fills area below the selected
        glyph to show that it is selected but unknown. Only shows the missing
        glyphs if the side checkbox is selected."""
        upem = self.controller.getUpem()
        descender = self.controller.getDescender()
        glyphName = textItem.name
        w = textItem.width
        h = self.getControlsHeight()
        t = self.controller.getTangent()
        textScale = self.controller.getTextScale()
        ty = self.getIndexToScaledValue(textItem.yIndex)
        gutter0, gutter1, buttonWidth = self.getControlSizes()
        metricsW = max(w + 2 * buttonWidth + 3 * gutter0, 5 * buttonWidth + 6 * gutter0)
        x = w / 2
        y = metricsW
        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        self.translate(textItem.x, ty)
        y = descender - h
        MISSINGGLYPHMARKERCOLOR.set()

        if t == 0:
            path = self.getRegularBox(0, y, w, h)
        else:
            path = self.getSlantedBox(0, y, w, h)

        path.fill()

        x = w / 2
        y = -gutter0

        self.drawTextLabel('?', '%s (missing)' % glyphName, x, y, BLACKCOLOR,
                'center')

        NSGraphicsContext.restoreGraphicsState()

    def drawControlsBackground(self, x, y, w, h):
        """Draws gray rectangle under metrics data and keys. Size and position
        depends on spacing or kerning. Horizontally skewed to match descender
        position in case style is italic."""
        descender = self.controller.getDescender()
        h0 = descender
        h1 = descender - h
        t = self.controller.getTangent()

        if t != 0:
            #  Draws slanted box in case of an italic style.
            '''
            path = NSBezierPath.bezierPath()
            path.moveToPoint_((t * h1 - XX, h1))
            path.lineToPoint_((t * h0 - XX, h0))
            path.lineToPoint_((t * h0 + w + 2 * XX, h0))
            path.lineToPoint_((t * h1 + w + 2 * XX, h1))
            path.lineToPoint_((t * h1 - XX, h1))
            '''
            path = self.getSlantedBox(x - XX, h1, y + 2 * XX, h)
        else:
            #  Draws straight box in case of a regular style.
            path = self.getRegularBox(x - XX, h1, y + 2 * XX, h)

        if self.controller.isSpacing():
            SPACINGBGCOLOR.set()
        elif self.controller.isKerning():
            KERNINGBGCOLOR.set()

        path.fill()

    def drawSpacingControls(self, textItem):
        """Spacing controls..."""
        descender = self.controller.getDescender()
        textScale = self.controller.getTextScale()
        t = self.controller.getTangent()
        glyphName = textItem.name
        glyph = self.getStyle()[glyphName]
        glyphLabel = self.getGlyphLabel(textItem, glyph, glyphName)
        leftMargin, rightMargin, w = self.controller.getMargins(glyphName)
        leading = self.controller.getLeading()
        gutter0, gutter1, buttonWidth = self.getControlSizes()
        ty = self.getIndexToScaledValue(textItem.yIndex)

        # Make sure the 5 buttons fit on the width. Move box horizontally to
        # descender position in case style is italic.
        #w = int(round(glyph.width))
        h = self.getControlsHeight()
        metricsW = max(w + 2 * buttonWidth + 3 * gutter0, 5 * buttonWidth + 6 * gutter0)
        px = w / 2 - metricsW / 2
        pw = metricsW

        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        self.translate(textItem.x, ty)

        self.drawControlsBackground(px, pw, w, h)
        y = descender
        self.drawSpaceMargins(y, leftMargin, rightMargin, w)
        y -= buttonWidth

        if self.controller.hasOverlayRelated():
            lmr, rmr, wr = self.controller.getMargins(glyphName, related=True)
            # FIXME: w should be related width.
            self.drawSpaceMargins(y, lmr, rmr, wr)
            y -= buttonWidth

        self.drawSpaceButtons(y, w, leftMargin)
        y -= buttonWidth + gutter0

        # FIXME: Should be centered.
        #x = t * (descender - 3 * buttonWidth + 2 * gutter0)
        xLabel = w / 2
        self.drawTextLabel('/', glyphLabel, xLabel, y, BLACKCOLOR,
                'center')

        # Draw lock if the glyph anchor updating is locked.
        if isLocked(glyph):
            self.drawLock()

        NSGraphicsContext.restoreGraphicsState()

    def drawSpaceButtons(self, y, w, leftMargin):
        """Spacing keys, make sure there is space for the buttons in the
        middle. If there are no margins (for example in a space), just show
        the O/P pair. Shifts horizontally to match descender position in case
        style is italic."""
        gutter0, gutter1, buttonWidth = self.getControlSizes()
        descender = self.controller.getDescender()
        t = self.controller.getTangent()
        #y = descender - buttonWidth

        if leftMargin is None:
            self.drawKeyButton(w / 2 - gutter1 + t * y, y, buttonWidth,
                    'O', LABEL_SIZE, 'left')
            self.drawKeyButton(w / 2 + gutter1 + t * y, y, buttonWidth,
                    'P', LABEL_SIZE, 'right')
        else:
            xl = min(w / 2 - 1.5 * (LABEL_SIZE + gutter1), 0)
            xm = w / 2
            xr = max(w / 2 + 1.5 * (LABEL_SIZE + gutter1), w)

            # Draw the buttons.
            self.drawKeyButton(xl - gutter1 + t * y, y, buttonWidth, 'U',
                    LABEL_SIZE, 'left')
            self.drawKeyButton(xl + gutter1 + t * y, y, buttonWidth, 'I',
                    LABEL_SIZE, 'right')

            self.drawKeyButton(xm + t * y, y, buttonWidth, '=',
                    LABEL_SIZE, 'center')

            self.drawKeyButton(xr - gutter1 + t * y, y, buttonWidth, 'O',
                    LABEL_SIZE, 'left')
            self.drawKeyButton(xr + gutter1 + t * y, y, buttonWidth, 'P',
                    LABEL_SIZE, 'right')

    def drawSpaceMargins(self, y0, leftMargin, rightMargin, w):
        # TODO: simplify.
        gutter0, gutter1, buttonWidth = self.getControlSizes()
        t = self.controller.getTangent()

        # Draw margins if they exist.
        if leftMargin is not None:
            if leftMargin < 0:
                c = REDCOLOR
                xx = leftMargin - gutter0
            else:
                c = DARKBLUECOLOR
                xx = -gutter0

            c.set()
            # Shift horizontally to match y0 position in case style
            # is italic.

            y00 = y0 - buttonWidth

            if t == 0:
                # kit.drawRectangle
                path = self.getRegularBox(0, y00, leftMargin, buttonWidth)

            else:
                path = self.getSlantedBox(0, y00, leftMargin, buttonWidth)

            path.fill()

            # Shift horizontally to match y0 position in case style is
            # italic.
            xLabel = xx + t * y0
            yLabel = y0
            self.drawTextLabel('sb', str(leftMargin), xLabel, yLabel,
                    c, 'left')

        # Width
        # Shift horizontally to match descender position in case style is
        # italic.
        xLabel = w / 2 + t * y0
        yLabel = y0
        self.drawTextLabel('sb', str(w), xLabel, yLabel,
                BLACKCOLOR, 'center')

        if rightMargin is not None:
            if rightMargin < 0:
                c = REDCOLOR
                xx = w - rightMargin + gutter0
            else:
                c = DARKBLUECOLOR
                xx = w + gutter0

            c.set()

            # Shift horizontally to match y0 position in case style
            # is italic.
            x0 = w - rightMargin
            y00 = y0 - buttonWidth

            if t == 0:
                path = self.getRegularBox(x0, y00, rightMargin, buttonWidth)
            else:
                path = self.getSlantedBox(x0, y00, rightMargin, buttonWidth)

            path.fill()

            # Shift horizontally to match y0 position in case style
            # is italic.
            xLabel = xx + t * y0
            yLabel = y0
            self.drawTextLabel('sb', str(rightMargin), xLabel, yLabel,
                    c, 'right')

    def drawControls(self):
        """Control buttons below selected glyph."""
        textItem = self.cache.getSelectedItem()

        if not textItem:
            return

        style = self.getStyle()
        glyphName = textItem.name
        upem = self.controller.getUpem()
        descender = self.controller.getDescender()
        leading = self.controller.getLeading()

        if not self.controller.exists(glyphName):
            self.drawMissingMarker(textItem)
        elif self.controller.isSpacing():
            self.drawSpacingControls(textItem)
        elif self.controller.isKerning():
            self.drawKerningControls(textItem)

    def drawHover(self):
        """Draws mouse hover red rectangle. Draw slanted if style is italic."""
        textItem = self.cache.getHoverItem()

        if textItem is None:
            return

        style = self.getStyle()
        descender = self.controller.getDescender()
        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        leading = self.controller.getLeading()
        width = textItem.width or 0
        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)

        # Start a next line, not at origin.
        y = self.getIndexToScaledValue(textItem.yIndex)
        self.translate(textItem.x, y)
        t = self.controller.getTangent()

        # Draw slanted box if italic.
        if t == 0:
            path = self.getRegularBox(0, descender, width, upem)
        else:
            path = self.getSlantedBox(0, descender, width, upem)

        NSColor.redColor().set()
        path.setLineWidth_(1 / textScale)
        path.stroke()
        NSGraphicsContext.restoreGraphicsState()

    def drawMargins(self):
        if not self.controller._showMargins:
            return

        self.kit.drawRectangle(M, M, self.width - 2*M, self.height - 2*M,
                fillColor=None, strokeColor=cyanColor)

    def drawGrid(self):
        if not self.controller._showGrid:
            return

        ppem = self.controller.getPpem()
        textScale = self.controller.getTextScale()
        xRect, yRect, wRect, hRect = self.canvas.getScrollRectangle()
        w = 0.5

        x0 = M
        x1 = self.width - M

        y = M
        i = 0

        while y < self.height - M:
            y = M + i * ppem / 10
            self.kit.drawLine((x0, y), (x1, y), color=cyanColor, width=w)
            i += 1

            if y > yRect + hRect:
                break

        y0 = M
        y1 = self.height - M
        x = M
        i = 0

        while x < self.width - M:
            x = M + i * ppem / 10
            self.kit.drawLine((x, y0), (x, y1), color=cyanColor, width=w)
            i += 1

            if x > xRect + wRect:
                break

    def drawAllKerningValues(self):
        """Draws the kerning values for all glyphs except selected, which is
        already drawn by the kerning controls."""
        if not self.controller._showMarkers or not self.controller.isKerning():
            return

        upem = self.controller.getUpem()
        leading = self.controller.getLeading()
        textScale = self.controller.getTextScale()
        lines = self.cache.getLines()

        for yIndex, line in sorted(lines.items()):
            if self.yIndexIsVisible(yIndex):
                for textItem in line.values():
                    selectedTextItem = self.cache.getSelectedItem()

                    if textItem != selectedTextItem:
                        y = self.getIndexToScaledValue(yIndex)
                        NSGraphicsContext.saveGraphicsState()
                        self.scale(textScale)
                        self.translate(textItem.x, y)
                        self.drawKerningValue(textItem)
                        NSGraphicsContext.restoreGraphicsState()

    def drawKerningValue(self, textItem, doBlack=False):
        """Draws kerning labels. Only show if zero if doBlack is True.
        Negative kerning is red, positive kerning is green. Show the value. On
        left positive, on right is negative values. Same color as the kerning
        value bar."""
        if not textItem:
            return

        textScale = self.controller.getTextScale()
        descender = self.controller.getDescender()
        gutter, _, buttonWidth = self.getControlSizes()
        k = textItem.kerning
        t = self.controller.getTangent()
        y0 = descender - buttonWidth

        if k and k < 0:
            REDCOLOR.set()
            if t == 0:
                path = self.getRegularBox(0, y0, abs(k), buttonWidth)
            else:
                path = self.getSlantedBox(0, y0, abs(k), buttonWidth)

            path.fill()

            self.drawTextLabel('-k', '%d' % k, -gutter, descender, REDCOLOR,
                    'left')

        elif k and k > 0:
            DARKGREENCOLOR.set()
            if t == 0:
                path = self.getRegularBox(-k, y0, k, buttonWidth)

            else:
                path = self.getSlantedBox(-k, y0, k, buttonWidth)

            path.fill()
            self.drawTextLabel('+k', '+%d' % k, k + gutter, descender,
                    DARKGREENCOLOR, 'right')
        else:
            if doBlack:
                BLACKCOLOR.set()
                if t == 0:
                    path = self.getRegularBox(0, descender - buttonWidth, 1 / textScale, buttonWidth)
                else:
                    path = self.getSlantedBox(0, y0, 1 / textScale, buttonWidth)

                path.fill()
                self.drawTextLabel('k', '%d' % k, gutter, descender,
                        BLACKCOLOR, 'right')

    def drawKerningControls(self, textItem):
        """Draws the info marker below a kerning pair."""
        descender = self.controller.getDescender()
        glyphName = textItem.name
        glyph = self.getStyle()[glyphName]
        leading = self.controller.getLeading()
        textScale = self.controller.getTextScale()
        gutter0, gutter1, buttonWidth = self.getControlSizes()
        ty = self.getIndexToScaledValue(textItem.yIndex)
        glyphLabel = self.getGlyphLabel(textItem, glyph, glyphName)
        labelValueWidth = -LABEL_SIZE * len(glyphLabel)
        h = self.getControlsHeight()
        w = int(round(glyph.width))
        xl = min(-buttonWidth - 1.5 * gutter0, labelValueWidth)
        xw = max(w + 2 * buttonWidth + 3 * gutter0, labelValueWidth)
        previousTextItem = self.cache.getPrevious()

        if previousTextItem:
            previousGlyphName = previousTextItem.name
        else:
            previousGlyphName = 'None'

        textLabel = '%s-%s' % (previousGlyphName, glyphName)
        xLabel = w / 2
        yLabel = descender - 3 * buttonWidth + 3 * gutter0

        NSGraphicsContext.saveGraphicsState()
        self.scale(textScale)
        self.translate(textItem.x, ty)
        self.drawControlsBackground(xl, xw, w, h)
        self.drawKerningValue(textItem, doBlack=True)
        self.drawKerningButtons()
        self.drawTextLabel('/', textLabel, xLabel, yLabel,
                BLACKCOLOR, 'center')
        NSGraphicsContext.restoreGraphicsState()

    def drawKerningButtons(self):
        descender = self.controller.getDescender()
        gutter0, gutter1, buttonWidth = self.getControlSizes()
        y = descender - buttonWidth + gutter0
        self.drawKeyButton(-gutter1, y, buttonWidth, 'H', LABEL_SIZE, 'left')
        self.drawKeyButton(gutter1, y, buttonWidth, 'J', LABEL_SIZE, 'right')

    def drawSpacing(self, style, glyph, glyphName, width):
        """If the spacing of the glyph is different from the rest of it's
        group, then draw the markers on the other glyphs in the group.

        TODO: to be implemented?

        """
        pass

    def drawKeyButton(self, x, y, w, key, size, align):
        """Draws the icon of a key-button. Checks against the last / current
        key string to know if the key should be drawn white on black."""
        textScale = self.controller.getTextScale()
        NSGraphicsContext.saveGraphicsState()
        size = size / textScale
        self.translate(0, 0)

        if key in self._lastKey:
            c = WHITECOLOR
            bg = BLACKCOLOR
            ks = 'pushedKey' + key
        else:
            c = BLACKCOLOR
            bg = WHITECOLOR
            ks = 'key' + key

        nsString = self._stringLabels.get(ks) # Test on cached string label

        if nsString is None:
            # Prepare the text attributes.
            # TODO: make global.
            attributes = {NSFontAttributeName: NSFont.boldSystemFontOfSize_(size),
                NSForegroundColorAttributeName: c}
            self._stringLabels[ks] = nsString = NSAttributedString.alloc().initWithString_attributes_(key , attributes)

        width, height = nsString.size()

        if align == 'left':
            x -= w / 2
        elif align == 'center':
            pass
        elif align == 'right':
            x += w / 2

        path = self.getRegularBox(x - w / 2, -y + w / 2, w, w)
        bg.set()
        path.fill()
        c.set()
        path.setLineWidth_(0.5 / textScale)
        path.stroke()
        r = NSMakeRect(x - width / 2, -y + w / 10 + height / 2, width, height)
        nsString.drawInRect_(r)
        NSGraphicsContext.restoreGraphicsState()

    def drawTextLabel(self, textType, label, x, y, color, align):
        """Generic method to draw text labels in the UI.

        TODO: move to canvas kit.
        """
        textScale = self.controller.getTextScale()
        size = LABEL_SIZE / textScale
        nsString = self.getNSString(textType, label, size, color)
        textScale = self.controller.getTextScale()
        NSGraphicsContext.saveGraphicsState()
        self.translate(0, 0)
        width, height = nsString.size()

        if align == 'left':
            x -= width
        elif align == 'center':
            x -= width / 2

        nsString.drawInRect_(NSMakeRect(x, -y + height / 3, width, height))
        NSGraphicsContext.restoreGraphicsState()

    def drawLock(self):
        # TODO: move path building somewhere else.
        NSGraphicsContext.saveGraphicsState()
        self.scale(5)
        y = -90
        x = -100
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((x+6, y+18))
        path.lineToPoint_((x+6, y+20))

        # On, Off, Off
        path.curveToPoint_controlPoint1_controlPoint2_((x+12, y+28),
                (x+6, y+25), (x+8, y+28))
        path.curveToPoint_controlPoint1_controlPoint2_((x+18, y+20),
                (x+16, y+28), (x+18, y+25))
        path.lineToPoint_((x+18, y+18))
        path.closePath()
        path.moveToPoint_((x+0, y+0))
        path.curveToPoint_controlPoint1_controlPoint2_((x+24, y+0),
                (x+8, y-1), (x+16, y-1))
        path.lineToPoint_((x+24, y+18))
        path.lineToPoint_((x+22, y+18))
        path.lineToPoint_((x+22, y+20))
        path.curveToPoint_controlPoint1_controlPoint2_((x+12, y+32),
                (x+22, y+27), (x+18, y+32))
        path.curveToPoint_controlPoint1_controlPoint2_((x+2, y+20),
                (x+6, y+32), (x+2, y+27))
        path.lineToPoint_((x+2, y+18))
        path.lineToPoint_((x+0, y+18))
        path.closePath()
        LOCKMARKERCOLOR.set()
        path.fill()
        NSGraphicsContext.restoreGraphicsState()

    # Visible parts inside scroll rectangle.

    def yIndexIsVisible(self, yIndex, entirely=False):
        """Checks if a line index is inside the visible scrollView area. Origin
        is at the top of the page."""
        textScale = self.controller.getTextScale()
        upem = self.controller.getUpem()
        _, y, _, h = self.canvas.getScrollRectangle()

        topY = self.getIndexToScaledValue(yIndex, baseLine=False) * textScale
        bottomY = (self.getIndexToScaledValue(yIndex, baseLine=False) - upem) * textScale

        if topY < y:
            return False
        elif bottomY > y + h:
            return False

        return True

    def getVisibleLinesIndices(self):
        """Determines which line numbers are currently visible."""
        textScale = self.controller.getTextScale()
        lineHeight = self.controller.getLineHeight() * textScale
        upem = self.controller.getUpem() * textScale
        _, y0, _, h0 = self.canvas.getScrollRectangle()
        margin = M
        rectangleTop = y0
        rectangleBottom = y0 + h0
        indices = []

        yTop = margin
        yBottom = margin + upem
        yLine = yTop + lineHeight
        i = 0

        while yLine < self.height - margin:

            if between(yTop, rectangleTop, rectangleBottom) or \
                    between(yBottom, rectangleTop, rectangleBottom):
                indices.append(i)

            i += 1
            yTop = yLine
            yBottom = yTop + upem
            yLine = yTop + lineHeight

        return indices


    # Typesetting.

    def typeset(self):
        """Typesets the glyphNames based on self.glyphNames() to fit on page of
        *width*, with a certain font size and leading. The glyph position of
        each glyph is calculate, taking the kerning into account, and stored in
        the cache.

        In case there are no lines to display or in case the window size
        changed, recalculates the text flow. Answer the new window size
        tuple."""
        style = self.getStyle()

        if style is None:
            return

        nsview = self.canvas.getNSView()
        self.width, _ = self.canvas.getClipView().getSize()
        textScale = self.controller.getTextScale()
        leading = self.controller.getLeading()
        width = self.width / textScale
        margin = M / textScale
        upem = self.controller.getUpem()
        glyphNames = self._pages[self.pageIndex]
        glyphNames = self.addStartEndGlyphs(glyphNames)
        groups = self.controller.getGroups()
        showKerning = self.controller._showKerning
        showRepeat = self.controller._showRepeat
        showMissing = self.controller._showMissingGlyphs
        showEmpty = self.controller._showEmptyGlyphs

        # Creates the TextItem lines in the cache.
        yIndex = self.cache.initLines(glyphNames, groups, width, margin,
                showKerning=showKerning, showRepeat=showRepeat,
                showMissing=showMissing, showEmpty=showEmpty)

        # Calculates the vertical position of the line last rendered so we can
        # adjust the canvas height.
        h = self.getIndexToScaledValue(yIndex, baseLine=False) * textScale
        ch = self.getControlsHeight() * textScale
        self.height =  h + ch + M # */ textScale?
        self.canvas.getCanvasView().setSize(self.width, self.height)

    def typesetVisibleLines(self):
        """Only typesets the glyphs inside current viewport. Use typeset()
        after a scroll event."""
        style = self.getStyle()

        if style is None:
            return

        showKerning = self.controller._showKerning
        showRepeat = self.controller._showRepeat
        showMissing = self.controller._showMissingGlyphs
        showEmpty = self.controller._showEmptyGlyphs
        groups = self.controller.getGroups()

        lineIndices = self.getVisibleLinesIndices()
        self.cache.updateLines(groups, lineIndices,
                showKerning=showKerning, showRepeat=showRepeat,
                showMissing=showMissing, showEmpty=showEmpty)

    def addStartEndGlyphs(self, glyphNames):
        new = []

        for n in glyphNames:
            new += self._tStart
            new.append(n)
            new += self._tEnd

        return new

    def findAndReplace(self, tStart, tEnd, expandedText):
        replacementPairs = [('\\n', '\n')]

        for p0, p1 in replacementPairs:
            tStart = tStart.replace(p0, p1)
            tEnd = tEnd.replace(p0, p1)
            expandedText = expandedText.replace(p0, p1)

        return tStart, tEnd, expandedText

    def splitPages(self, glyphNames):
        """The number of glyphNames may have grown too long. If so, split into
        pages and show them in the page popup. Maximum number of glyphs is set
        in the side menu."""
        maxGlyphs = min(self.controller._maxGlyphs, NUMBER_OF_GLYPHS_MAX)
        pages = []

        while glyphNames:
            pages.append(glyphNames[:maxGlyphs])
            glyphNames = glyphNames[maxGlyphs:]

        return pages

    # Update.

    def update(self, typesetVisible=False, typeset=True):
        """Typesets sample page and redraws canvas. Tells controller to update
        spacing / kerning values for selected groups.

        Flow is calculated in self.typeset(), should be recalculated on spacing
        and kerning changes. The typesetVisible option only updates the lines
        inside the canvas viewport. Also sets _dirty to indicate the rest of the
        lines need to be updated on a scroll or resize.
        """

        try:
            if typesetVisible:
                # Typeset visible lines only.
                self.typesetVisibleLines()
                self.cache.setDirty(True)
                self._bounds = self.canvas.getClipBounds()
            elif typeset:
                self.typeset()
                self.cache.clearVisible()
                self.cache.setDirty(False)

            self.canvas.update()
            #self.controller.setGroupsInfo()
            log = getLog()
            log.set()
        except:
            print(traceback.format_exc())

    def updateStartGlyphs(self, tStart):
        glyphNames = []
        tStart = tStart.replace('\\n', '\n')
        startGlyphs = RE_GLYPHNAMES.findall(tStart)

        for t in startGlyphs:
            glyphName = getGlyphName(t)
            glyphNames.append(glyphName)

        self._tStart = glyphNames
        self.update()

    def updateEndGlyphs(self, tEnd):
        glyphNames = []
        tEnd = tEnd.replace('\\n', '\n')
        endGlyphs = RE_GLYPHNAMES.findall(tEnd)

        for t in endGlyphs:
            glyphName = getGlyphName(t)
            glyphNames.append(glyphName)

        self._tEnd = glyphNames
        self.update()

    def updateMaxGlyphs(self):
        # TODO: set to last page index?
        self.setSample(self.sampleIndex, 0)
        self.controller.updatePageNames()

    def updatePage(self, text):
        glyphNames = compileText(text)
        self._pages[self.pageIndex] = glyphNames
        self.update()

    def toggleLockAnchor(self):
        item = self.cache.getSelectedItem()

        if not item:
            return

        style = self.getStyle()

        if item is not None and style is not None and item.name in style:
            glyph = style[item.name]
            toggleLock(glyph)

    # Menu.

    def menu(self, event):
        menu = Menu(self)
        menu.open(event)

    # Callbacks.

    def addToGroupCallback_(self, menuItem):
        selectedTextItem = self.cache.getSelectedItem()

        if selectedTextItem:
            self.controller.addToGroup(selectedTextItem.name)

    def newGroupCallback_(self, menuItem):
        pass

    def addToDesignSpaceCallback_(self, menuItem):
        self.controller.addToDesignSpace()

    def removeFromDesignSpaceCallback_(self, menuItem):
        self.controller.removeFromDesignSpace()

    def saveStyleCallback_(self, menuItem):
        self.controller.save()

    def editStyleCallback_(self, menuItem):
        self.controller.editStyle()

    def editGlyphCallback_(self, menuItem):
        selectedTextItem = self.cache.getSelectedItem()
        if selectedTextItem:
            self.controller.editGlyph(selectedTextItem.name)

    def defaultGroupsCallback_(self, menuItem):
        self.controller.defaultGroups()

    def setTabWidthsCallback_(self, menuItem):
        self.controller.setTabWidths()

    def openFamilyCallback_(self, menuItem):
        self.controller.openFamily()

    def closeFamilyCallback_(self, menuItem):
        self.controller.closeFamily()

    def setFwidWidthsCallback_(self, menuItem):
        self.controller.setFwidWidths()

    def setHwidWidthsCallback_(self, menuItem):
        self.controller.setHwidWidths()

    def setCmbWidthsCallback_(self, menuItem):
        self.controller.setCmbWidths()

    def fixGroupsCallback_(self, menuItem):
        self.controller.fixGroups()

    # Mouse events.

    def getMouseFromEvent(self, event):
        """Answers the current mouse position."""
        mouse = self.canvas.getMouse(event)
        return NSMakePoint(mouse.x, mouse.y)

    def outsideScrollRectangle(self, mouse):
        mouseX, mouseY = mouse
        x, y, w, h = self.canvas.getScrollRectangle()

        if mouseX < x or mouseY < y or mouseX > x + w or mouseY > y + h:
            return True

        return False

    def mouseMoved(self, event):
        mouse = self.eventHandler.getMouse(event)

        if mouse and not self.outsideScrollRectangle(mouse):
            self.setHover(mouse)
        else:
            self.resetHover()

    def mouseDown(self, event):
        """Selects glyph after a single click. Opens the glyph after a double
        click."""
        mouse = self.eventHandler.mouseDown(event)
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask
        optionDown = modifiers & NSAlternateKeyMask

        if not self.cache.getHoverItem():
            return

        self.setSelected(self.cache.getHoverItem())
        selectedTextItem = self.cache.getSelectedItem()
        self.scrollTo(selectedTextItem)

        if optionDown:
            # If the clicked glyph (option/alt key) is not the current
            # glyph, then added this glyph (and all the glyphs in its
            # group) to the group of the current glyph. Don't change the
            # selection of the current glyph.
            # TODO
            pass
        elif shiftDown:
            # TODO
            pass
        elif event.clickCount() == 2:
            # Double click opens the selected glyph in the editor.
            selectedTextItem = self.cache.getSelectedItem()
            self.controller.editGlyph(selectedTextItem.name)
        else:
            try:
                # Regular selection by click. Sets the current hover glyph as
                # selected glyph.
                x = selectedTextItem.x
                yIndex = selectedTextItem.yIndex
                w = selectedTextItem.width
                # Stores middle of the selected glyph in scaled (x, y) tuple (not the
                # mouse position).
                self.update(typeset=False)
            except:
                print(traceback.format_exc())

    def mouseDragged(self, event):
        """
        TODO: Debug?
        """
        #mouse = self.eventHandler.mouseDragged(event)
        pass

    def mouseUp(self, event):
        pass
        '''
        mouse = self.eventHandler.mouseUp(event)

        # Dragging may have changed parts. Now update all.
        if self._doUpdateOnMouseUp:
            self._doUpdateOnMouseUp = False
            self.update()
        '''

    def keyDown(self, event):
        modifiers = event.modifierFlags()
        commandDown = modifiers & NSCommandKeyMask

        characters = event.characters()
        style = self.getStyle()
        self._lastKey = ''

        if characters in KEY_EQUALSPACING:
            self.doEqualize()
            self.update(typesetVisible=True)
        elif characters in GROUP_KEYS:
            stepX = self.getStepSize(event)
            self.handleGroups(characters, stepX)
            self.typeset()
            self.followSelected()
        elif characters in EDIT_KEYS:
            self.handleEdit(characters, commandDown)
            self.update(typesetVisible=True)
        elif characters in ARROW_KEYS:
            self.handleArrows(event, characters)
            self.update(typesetVisible=True)
        elif characters in FLAG_KEYS:
            self.handleFlags(characters)
            self.update(typesetVisible=True)
        elif characters in ZOOM_KEYS:
            self.handleZoom(characters)
            self.update(typesetVisible=True)
        elif characters in LEADING_KEYS:
            self.handleLeading(characters)
            self.update(typesetVisible=True)
        elif characters in OPEN_KEYS:
            self.handleOpen(commandDown)
            self.update(typesetVisible=True)
        elif characters in KEY_LOCKANCHOR:
            self.toggleLockAnchor()
            self.update(typesetVisible=True)
        elif characters in KEY_FIND:
            self.openSearchBox()
            self.update(typesetVisible=True)

        self.cache.resetHover()

    def handleGroups(self, characters, stepX):
        selectedTextItem = self.cache.getSelectedItem()

        if selectedTextItem is None or selectedTextItem.missing:
            return

        if not self.timer:
            self.setTimer()

        # TODO: consider step orientation.
        self.stepX += stepX
        self.characters = characters

        # Last click time.
        self.lastClick = datetime.now()

    def doEqualize(self):
        style = self.getStyle()
        selectedTextItem = self.cache.getSelectedItem()
        glyphName = selectedTextItem.name
        groups = self.controller.getGroups()
        round2Step = self.controller._doRound
        spacingMode = self.controller.isSpacing()

        if spacingMode:
            changedGlyphs = equalizeSpacing(style, glyphName, groups,
                    round2Step=round2Step)
            self._lastKey = KEY_EQUALSPACING

        setLog()
        self.controller.compareSelectedGroupMargins()

    def doGroups(self):
        changedGlyphs = None
        spacingMode = self.controller.isSpacing()
        kerningMode = self.controller.isKerning()
        style = self.getStyle()
        groups = self.controller.getGroups()
        selectedTextItem = self.cache.getSelectedItem()
        glyphName = selectedTextItem.name
        round2Step = self.controller._doRound

        if spacingMode:
            if self.characters in KEY_LEFTDEC:
                changedGlyphs = changeSpacing(style, glyphName,
                        -self.stepX, LEFT, groups, round2Step=round2Step)
                self._lastKey = KEY_LEFTDEC
            elif self.characters in KEY_LEFTINC:
                changedGlyphs = changeSpacing(style, glyphName,
                        self.stepX, LEFT, groups, round2Step=round2Step)
                self._lastKey = KEY_LEFTINC
            elif self.characters in KEY_RIGHTDEC:
                changedGlyphs = changeSpacing(style, glyphName,
                        -self.stepX, RIGHT, groups, round2Step=round2Step)
                self._lastKey = KEY_RIGHTDEC
            elif self.characters in KEY_RIGHTINC:
                changedGlyphs = changeSpacing(style, glyphName,
                        self.stepX, RIGHT, groups, round2Step=round2Step)
                self._lastKey = KEY_RIGHTINC
        elif kerningMode:
            previousTextItem = self.cache.getPrevious()

            if previousTextItem:
                previousGlyphName = previousTextItem.name

                if self.characters in KEY_KERNDEC:
                    changedGlyphs = changeKerning(style, previousGlyphName,
                            glyphName, -self.stepX, groups, round2Step=round2Step)
                    self._lastKey = KEY_KERNDEC
                elif self.characters in KEY_KERNINC:
                    changedGlyphs = changeKerning(style, previousGlyphName,
                            glyphName, self.stepX, groups, round2Step=round2Step)
                    self._lastKey = KEY_KERNINC

        setLog()
        self.controller.compareSelectedGroupMargins()
        self.stepX = 0
        self.characters = ''
        self.timer = None

    def handleEdit(self, characters, commandDown):
        view = self.controller.side.getView()

        if characters in KEY_EDITKERNING: # 'kK'
            self.controller.setEditMode(EDIT_MODES[KERNING])
            view.editMode.set(self.getEditMode())
        elif characters in KEY_EDITSPACING: # 'sS'
            if commandDown:
                self.controller.save()
            else:
                self.controller.setEditMode(EDIT_MODES[SPACING])
                view.editMode.set(self.getEditMode())

    def handleFlags(self, characters):
        view = self.controller.side.getView()

        if characters in KEY_SHOWMISSING:
            self.controller._showMissingGlyphs = not view.showMissingGlyph.get()
            view.showMissingGlyph.set(self.controller._showMissingGlyphs)

        elif characters in KEY_SHOWMARKERS:
            self.controller._showMarkers = not self.controller._showMarkers
            view.showMarkers.set(self.controller._showMarkers)

        elif characters in KEY_SHOWKERNING:
            self.controller._showKerning = not view.showKerning.get()
            view.showKerning.set(self.controller._showKerning)

        elif characters in KEY_SHOWMETRICS:
            self.controller._showMetrics = not view.showMetrics.get()
            view.showMetrics.set(self.controller._showMetrics)

    def handleZoom(self, characters):
        # FIXME
        if characters in self.KEY_ZOOMIN:
            if shiftDown:
                self.setZoom(10)
            else:
                self.setZoom(2)
        elif characters in self.KEY_ZOOMOUT:
            if shiftDown:
                self.setZoom(-10)
            else:
                self.setZoom(-2)

    def handleLeading(self, characters):
        # TODO
        pass

    def handleOpen(self, commandDown):
        """Space, return or enter key open selected glyph in EditorWindow."""

        if commandDown:
            self.controller.editStyle()
        else:
            selectedTextItem = self.cache.getSelectedItem()
            self.controller.editGlyph(selectedTextItem.name)

    def handleArrows(self, event, characters):
        """Implements arrow key behavior."""
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask
        controlDown = modifiers & NSControlKeyMask
        selectedTextItem = self.cache.getSelectedItem()

        if not selectedTextItem:
            return

        previousIndex = selectedTextItem.yIndex

        if characters in NSHomeFunctionKey or \
                characters == NSUpArrowFunctionKey and \
                shiftDown and controlDown:
            self.scrollToFirst()
        elif characters in NSEndFunctionKey or \
                characters == NSDownArrowFunctionKey and \
                shiftDown and controlDown:
            self.scrollToLast()
        elif characters == NSUpArrowFunctionKey:
            dx = 1

            if shiftDown:
                dx = 10

            self.moveSelectionUp(dx)
        elif characters == NSDownArrowFunctionKey:
            dx = 1

            if shiftDown:
                dx = 10

            self.moveSelectionDown(dx)
        elif characters == NSLeftArrowFunctionKey:
            dx = 1

            if shiftDown:
                dx = 10

            self.moveSelectionLeft(dx)
        elif characters == NSRightArrowFunctionKey:
            dx = 1

            if shiftDown:
                dx = 10

            self.moveSelectionRight(dx)
        elif characters == NSPageUpFunctionKey:
            self.moveSelectionUp(10)
        elif characters == NSPageDownFunctionKey:
            self.moveSelectionDown(10)

        self.follow(previousIndex)

    # Scrolling.

    def scrollTo(self, textItem):
        """Keeps the selected item inside the viewport."""
        if not self.controller._showFollow:
            return

        textScale = self.controller.getTextScale()
        scrollRect = self.canvas.getScrollRectangle()
        _, ry, _, rh = scrollRect
        lineHeight = self.controller.getLineHeight() * textScale
        y0 = (textItem.yIndex - 1) * lineHeight
        y1 = (textItem.yIndex + 1) * lineHeight

        if y1 > ry + rh or y0 < ry:
            self.scroll()

    def scroll(self, doBuffer=False):
        """Scrolls to new position if outside viewport."""
        leading = self.controller.getLeading()
        em = self.controller.getUpem()
        textScale = self.controller.getTextScale()
        selectedTextItem = self.cache.getSelectedItem()

        if selectedTextItem is None:
            return

        x = 0
        h = leading * em * textScale
        i = selectedTextItem.yIndex

        if doBuffer:
            # One-line buffer.
            if i > 0:
                i -= 1

        y = i * h
        h = h * 1.5
        w = 10

        self.canvas.scroll(x, y, w, h)

    def scrollToFirst(self):
        firstItem = self.cache.getFirst()
        self.setSelected(firstItem)
        self.scrollTo(firstItem)

    def scrollToLast(self):
        lastItem = self.cache.getLast()
        self.setSelected(lastItem)
        self.scrollTo(lastItem)

    # Follow.

    def follow(self, previousIndex):
        if not self.controller._showFollow:
            return

        selectedTextItem = self.cache.getSelectedItem()

        if not selectedTextItem:
            return

        newIndex = selectedTextItem.yIndex

        if previousIndex < newIndex:
            self.scroll()
        elif previousIndex > newIndex:
            self.scroll(doBuffer=True)

    def followSelected(self):
        selectedTextItem = self.cache.getSelectedItem()
        self.scrollTo(selectedTextItem)

    # Selection.

    def setSelected(self, textItem):
        self.cache.setSelectedIndex(textItem)
        self.controller.setSelected(textItem)

    def moveSelectionUp(self, dy):
        """Vertical move, find the previous line."""
        textItem = self.cache.getAbove(dy)
        self.setSelected(textItem)

    def moveSelectionDown(self, dy):
        """Vertical move, find the next line."""
        textItem = self.cache.getBelow(dy)
        self.setSelected(textItem)

    def moveSelectionLeft(self, dx):
        """Horizontal move, gets the previous glyph."""
        textItem = self.cache.getPrevious(dx, previousPage=True)
        self.setSelected(textItem)

    def moveSelectionRight(self, dx):
        """Horizontal move, gets the next glyph."""
        textItem = self.cache.getNext(dx, nextPage=True)
        self.setSelected(textItem)
