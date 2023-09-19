# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    draw.py
#


import traceback
import math
from mojo.drawingTools import scale, save, restore
from random import random
from fontTools.pens.cocoaPen import CocoaPen

from AppKit import (NSCommandKeyMask, NSShiftKeyMask, NSAlternateKeyMask,
        NSUpArrowFunctionKey, NSDownArrowFunctionKey, NSLeftArrowFunctionKey,
        NSRightArrowFunctionKey, NSColor, NSBackspaceCharacter,
        NSDeleteFunctionKey, NSDeleteCharacter, NSBezierPath, NSPointInRect,
        NSGraphicsContext, NSAffineTransform, NSMakeRect, NSMakePoint,
        NSFontAttributeName, NSFont, NSForegroundColorAttributeName,
        NSAttributedString, NSControlKeyMask)

from tnbits.toolbox.character import CharacterTX
from tnbits.analyzers.analyzermanager import analyzerManager

SHOWDRAWTILES = False # Draw debug screen update tiles.

class Draw:

    def draw(self, rect):
        """There was an update call on the canvas view. Redraw the lines of
        the text in the TextCenter canvas window."""
        style = self.getStyle()

        if style is None:
            return

        if SHOWDRAWTILES:
            r = 0.85 + random() * 0.2
            g = 0.85 + random() * 0.2
            b = 0.85 + random() * 0.2
            NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, 1).set()
            path = NSBezierPath.bezierPathWithRect_(rect)
            path.fill()
        else:
            # Fill the canvas area white
            self._canvasColor.set()
            path = NSBezierPath.bezierPathWithRect_(rect)
            path.fill()

        # Typeset the page if it is empty or if the size of the window changed.
        w, h = self.typesetPage()

        try:
            # Now we can be sure that there must be self.lines to draw.
            self.drawText(style, w, h, rect)
        except Exception as e:
            print(traceback.format_exc())

    def drawMissing(self, glyphName, descender, width, emSize):
        """Shows rectangle when a glyph is missing."""
        self._nonExistingGlyphColor.set()
        textScale = self.getScale()
        indent = 0.5/textScale

        path = NSBezierPath.bezierPathWithRect_(((indent, descender+indent), (width-2*indent, emSize-2*indent)))
        path.fill()

        cName = CharacterTX.glyphName2Char(glyphName)
        fSize = emSize/2 # Scale with zoom factor.

        if not cName:
            cName = glyphName
            fSize = 100

        NSGraphicsContext.saveGraphicsState()
        glyphTransform = NSAffineTransform.transform()
        glyphTransform.scaleXBy_yBy_(1, -1)
        glyphTransform.concat()

        # Prepares the text attributes.
        attributes = {
            NSFontAttributeName : NSFont.systemFontOfSize_(fSize),
            NSForegroundColorAttributeName : self._nonExistingGlyphLabelColor
        }

        nsString = NSAttributedString.alloc().initWithString_attributes_(cName , attributes)
        nameWidth, nameHeight = nsString.size()
        nsString.drawInRect_(NSMakeRect(width/2-nameWidth/2, -600, nameWidth, nameHeight))
        NSGraphicsContext.restoreGraphicsState()

    def drawText(self, style, w, h, rect):
        """Main routine.
        TODO: break into smaller parts.
        """
        if not self.lines: # Check if there is something to draw. The back out.
            return

        emSize = style.info.unitsPerEm
        descender = style.info.descender
        lineHeight = emSize * self.getLeading()
        textScale = self.getScale()

        (rx, ry), (rw, rh) = rect # Scale the rect to canvas.
        rx /= textScale
        ry /= textScale
        rw /= textScale
        rh /= textScale

        # Draw all lines of glyphs and metrics.
        for yIndex, line in sorted(self.lines.items()):
            y = yIndex * lineHeight

            # Check if line is outside the clip rectangle.
            if y + 2 * emSize < ry or ry + rh < y - emSize:
                continue

            # flip glyph drawing
            # https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/CocoaDrawingGuide/Transforms/Transforms.html#//apple_ref/doc/uid/TP40003290-CH204-BCIHDAIJ
            # save
            for x, textItem in line.items(): # No need to be sorted.
                width = textItem.width

                if x+width < rx or rx + rw < x: # Check if we'll be drawing outside the clip rect.
                    continue

                NSGraphicsContext.saveGraphicsState()
                scale(textScale)
                flipTransform = NSAffineTransform.transform()
                flipTransform.translateXBy_yBy_(x, y+emSize)
                flipTransform.scaleXBy_yBy_(1, -1)
                flipTransform.concat()

                glyph = None
                glyphName = textItem.name

                 # If the glyph does not exists, show colored rect + example of glyph.
                if not textItem.exists:
                    self.drawMissing(glyphName, descender, width, emSize)
                    glyph = None
                elif glyphName in style:
                    # Glyph exists, draw the main glyph directly from
                    # the glyph representation (it may have changed by the
                    # editor, so we don't want to keep it in the textItem.
                    glyph = style[glyphName]
                    self._textColor.set()
                    glyph.getRepresentation("defconAppKit.NSBezierPath").fill()

                if self._showMetrics:
                    self.drawMetrics(style, width, emSize, descender)

                if self._showMarkers and glyph is not None: # Only if UI checkbox is set.
                    if self._editMode == 'spacing':
                        self.drawSpacing(style, glyph, glyphName, width)
                    elif self._editMode == 'kerning':
                        self.drawKerning(textItem, descender)

                NSGraphicsContext.restoreGraphicsState()

        self.drawMarkers(style, self._selectedTextItem)
        self.drawHover(style, descender, lineHeight, emSize)

    def drawMetrics(self, style, width, emSize, descender):
        # Bounding box
        textScale = self.getScale()

        if style.info.italicAngle: # Draw slanted box if italic.
            dy = math.tan(-style.info.italicAngle * math.pi/180)
            path = NSBezierPath.bezierPath()
            path.moveToPoint_((descender*dy, descender))
            path.lineToPoint_(((emSize+descender)*dy, emSize+descender))
            path.lineToPoint_(((emSize+descender)*dy+width, emSize+descender))
            path.lineToPoint_((descender*dy+width, descender))
            path.lineToPoint_((descender*dy, descender))
        else:
            path = NSBezierPath.bezierPathWithRect_(((0, descender), (width, emSize)))

        self._metricsColor.set()
        path.setLineWidth_(0.5/textScale)
        path.stroke()

        # Draw base line
        path = NSBezierPath.bezierPath()
        path.setLineWidth_(0.5/textScale)
        path.moveToPoint_((0, 0))
        path.lineToPoint_((width, 0))
        path.stroke()

    def drawSpacing(self, style, glyph, glyphName, width):
        """If the spacing of the glyph is different from the rest of it's
        group, then draw the markers on the other glyphs in the group."""

        # FIXME
        return
        textScale = self.getScale()
        # If the glyph is a base in it's profile or if the margin is different
        # from its profile base, then draw the marker
        if self.leftProfile is not None and self.leftProfile.baseName in style:
            labelSize = self.LABEL_SIZE
            ww = labelSize * 2 / textScale # Profile marker size

            if self.leftProfile.baseName == glyphName:
                self.BASEMARKERCOLOR.set()
                NSBezierPath.bezierPathWithOvalInRect_(((0, style.info.ascender+ww/2), (ww, ww))).fill()
                self.drawTextLabel('base', 'L', ww/2, style.info.ascender+ww*3/2, labelSize, self.WHITECOLOR, 'center')
                path = NSBezierPath.bezierPath()
                path.setLineWidth_(1/textScale)
                path.moveToPoint_((0, style.info.ascender+ww))
                path.lineToPoint_((0, style.info.ascender-ww))
                path.stroke()
            elif glyphName in self.leftProfile.group and glyphName in style and self.leftProfile.baseName in style and \
                    round(style[self.leftProfile.baseName].leftMargin) != round(glyph.leftMargin):
                path = NSBezierPath.bezierPathWithOvalInRect_(((0, style.info.ascender+ww/2), (ww, ww)))
                path.setLineWidth_(1/textScale)
                self.WHITECOLOR.set()
                path.fill()
                self.REDCOLOR.set()
                path.stroke()
                self.drawTextLabel('lsb', str(int(round(style[self.leftProfile.baseName].leftMargin))), ww/2, style.info.ascender+ww*3/2, labelSize, self.REDCOLOR, 'center')
                path = NSBezierPath.bezierPath()
                path.setLineWidth_(1/textScale)
                path.moveToPoint_((0, style.info.ascender+ww))
                path.lineToPoint_((0, style.info.ascender-ww))
                path.stroke()

        if self.rightProfile is not None and self.rightProfile.baseName:
            labelSize = self.LABEL_SIZE
            ww = labelSize*2/textScale # Profile marker size

            if self.rightProfile.baseName == glyphName:
                self.BASEMARKERCOLOR.set()
                NSBezierPath.bezierPathWithOvalInRect_(((width-ww, style.info.ascender+ww/2), (ww, ww))).fill()
                self.drawTextLabel('base', 'R', width-ww/2, style.info.ascender+ww*3/2, labelSize, self.WHITECOLOR, 'center')
                path = NSBezierPath.bezierPath()
                path.setLineWidth_(1/textScale)
                path.moveToPoint_((width, style.info.ascender+ww))
                path.lineToPoint_((width, style.info.ascender-ww))
                path.stroke()
            elif glyphName in self.rightProfile.group and glyphName in style and self.rightProfile.baseName in style and \
                    round(style[self.rightProfile.baseName].rightMargin) != round(glyph.rightMargin):
                path = NSBezierPath.bezierPathWithOvalInRect_(((width-ww, style.info.ascender+ww/2), (ww, ww)))
                path.setLineWidth_(1/textScale)
                self.WHITECOLOR.set()
                path.fill()
                self.REDCOLOR.set()
                path.stroke()
                self.drawTextLabel('rsb', str(int(round(style[self.rightProfile.baseName].rightMargin))), width-ww/2, style.info.ascender+ww*3/2, labelSize, self.REDCOLOR, 'center')
                path = NSBezierPath.bezierPath()
                path.setLineWidth_(1/textScale)
                path.moveToPoint_((width, style.info.ascender+ww))
                path.lineToPoint_((width, style.info.ascender-ww))
                path.stroke()

    def drawKerning(self, textItem, descender):
        """Draws kerning labels."""
        textScale = self.getScale()
        ls = self.LABEL_SIZE
        lg = 3/textScale # Label gutter
        bw = ls*1.4/textScale # Width/height of the button.

        if self._selectedTextItem is None:
            return
        elif textItem is None:
            return
        elif self._selectedTextItem.x == textItem.x and self._selectedTextItem.yIndex == textItem.yIndex:
            # Don't draw twice.
            return

        k = textItem.kerning # Kerning value

        if k:
            # Only show if not zero. Negative kerning is red, positive kerning
            # is green. Show the value. On left positive, on right is negative
            # values. Same color as the kerning value bar.
            valueString = '%d' % k

            if k < 0:
                self.REDCOLOR.set()
                path = NSBezierPath.bezierPathWithRect_(((0, descender-bw), (abs(k), bw)))
                path.fill()
                self.drawTextLabel('-k', valueString, -lg, descender, self.LABEL_SIZE, self.REDCOLOR, 'left')
            else:
                self.DARKGREENCOLOR.set()
                path = NSBezierPath.bezierPathWithRect_(((-k, descender-bw), (k, bw)))
                path.fill()
                self.drawTextLabel('+k', '+'+valueString, k+lg, descender, self.LABEL_SIZE, self.DARKGREENCOLOR, 'right')


    def drawHover(self, style, descender, lineHeight, emSize):
        """
        Draws mouse hover red rectangle. Draw slanted if style is italic.
        """
        if self._hoverTextItem:
            textScale = self.getScale()
            textItem = self._hoverTextItem
            width = textItem.width or 0
            NSGraphicsContext.saveGraphicsState()
            scale(textScale)
            flipTransform = NSAffineTransform.transform()
            flipTransform.translateXBy_yBy_(textItem.x, textItem.yIndex * lineHeight + emSize)
            flipTransform.scaleXBy_yBy_(1, -1)
            flipTransform.concat()
            if style.info.italicAngle: # Draw slanted box if italic.
                dy = math.tan(-style.info.italicAngle * math.pi/180)
                path = NSBezierPath.bezierPath()
                path.moveToPoint_((descender*dy, descender))
                path.lineToPoint_(((emSize+descender)*dy, emSize+descender))
                path.lineToPoint_(((emSize+descender)*dy+width, emSize+descender))
                path.lineToPoint_((descender*dy+width, descender))
                path.lineToPoint_((descender*dy, descender))
            else:
                path = NSBezierPath.bezierPathWithRect_(((0, descender), (width, emSize)))
            NSColor.redColor().set()
            path.setLineWidth_(1 / textScale)
            path.stroke()
            # restore
            NSGraphicsContext.restoreGraphicsState()

    def drawKeyButton(self, x, y, w, key, size, align):
        """Draw the icon of a key-button on the defined position. Check against
        the last / current key string to know if the key should be drawing as
        white on black."""
        textScale = self.getScale()
        NSGraphicsContext.saveGraphicsState()
        size = size/textScale
        flipTransform = NSAffineTransform.transform()
        flipTransform.scaleXBy_yBy_(1, -1)
        flipTransform.concat()

        if key in self._lastKey:
            c = self.WHITECOLOR
            bg = self.BLACKCOLOR
            ks = 'pushedKey'+key
        else:
            c = self.BLACKCOLOR
            bg = self.WHITECOLOR
            ks = 'key'+key

        nsString = self._stringLabels.get(ks) # Test on cached string label

        if nsString is None:
            # Prepare the text attributes.
            attributes = {
                NSFontAttributeName : NSFont.boldSystemFontOfSize_(size),
                NSForegroundColorAttributeName : c
            }
            self._stringLabels[ks] = nsString = NSAttributedString.alloc().initWithString_attributes_(key , attributes)
        width, height = nsString.size()
        if align == 'left':
            x -= w/2
        elif align == 'center':
            pass
        elif align == 'right':
            x += w/2
        path = NSBezierPath.bezierPathWithRect_(((x-w/2, -y+w/2), (w, w)))
        bg.set()
        path.fill()
        c.set()
        path.setLineWidth_(0.5/textScale)
        path.stroke()
        nsString.drawInRect_(NSMakeRect(x-width/2, -y+w/10+height/2, width, height))
        NSGraphicsContext.restoreGraphicsState()

    def drawTextLabel(self, type, label, x, y, size, color, align):
        """Generic method to draw text labels in the UI."""
        textScale = self.getScale()
        NSGraphicsContext.saveGraphicsState()
        size = size/textScale
        nsString = self._stringLabels.get(type+label) # Test on cached string label
        flipTransform = NSAffineTransform.transform()
        flipTransform.scaleXBy_yBy_(1, -1)
        flipTransform.concat()
        if nsString is None:
            # Prepare the text attributes.
            attributes = {
                NSFontAttributeName : NSFont.boldSystemFontOfSize_(size),
                NSForegroundColorAttributeName : color
            }
            self._stringLabels[type+label] = nsString = NSAttributedString.alloc().initWithString_attributes_(label , attributes)
        width, height = nsString.size()
        if align == 'left':
            x -= width
        elif align == 'center':
            x -= width/2
        nsString.drawInRect_(NSMakeRect(x, -y+height/3, width, height))
        NSGraphicsContext.restoreGraphicsState()

    def drawLock(self):
        # Always make sure to call restoreGraphicsState before leaving method!
        NSGraphicsContext.saveGraphicsState()
        scale(5)
        y = -90
        x = -100
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((x+6, y+18))
        path.lineToPoint_((x+6, y+20))
        path.curveToPoint_controlPoint1_controlPoint2_((x+12, y+28), (x+6, y+25), (x+8, y+28)) # On, Off, Off
        path.curveToPoint_controlPoint1_controlPoint2_((x+18, y+20), (x+16, y+28), (x+18, y+25))
        path.lineToPoint_((x+18, y+18))
        path.closePath()
        path.moveToPoint_((x+0, y+0))
        path.curveToPoint_controlPoint1_controlPoint2_((x+24, y+0), (x+8, y-1), (x+16, y-1))
        path.lineToPoint_((x+24, y+18))
        path.lineToPoint_((x+22, y+18))
        path.lineToPoint_((x+22, y+20))
        path.curveToPoint_controlPoint1_controlPoint2_((x+12, y+32), (x+22, y+27), (x+18, y+32))
        path.curveToPoint_controlPoint1_controlPoint2_((x+2, y+20), (x+6, y+32), (x+2, y+27))
        path.lineToPoint_((x+2, y+18))
        path.lineToPoint_((x+0, y+18))
        path.closePath()
        self.LOCKMARKERCOLOR.set()
        path.fill()
        NSGraphicsContext.restoreGraphicsState()

    def drawMarkers(self, style,  textItem):
        """Draws the measurement markers for the selected glyph. If the glyph
        is selected, then show the marker stuff We cannot draw that in the main
        loop, because we want to draw over all neighboring glyphs, e.g. over
        the line below."""
        if self._selectedTextItem is None:
            return

        emSize = style.info.unitsPerEm
        descender = style.info.descender
        leading = self.getLeading()
        textScale = self.getScale()

        ls = self.LABEL_SIZE
        lg = 3/textScale # Label gutter
        lg2 = lg/2
        bw = ls*1.4/textScale # Width/height of the button.

        ty = textItem.yIndex * emSize * leading + emSize  # Start a next line, not at origin)

        NSGraphicsContext.saveGraphicsState() # Always make sure to call restoreGraphicsState before leaving method!
        scale(textScale)
        flipTransform = NSAffineTransform.transform()
        flipTransform.translateXBy_yBy_(textItem.x, ty)
        flipTransform.scaleXBy_yBy_(1, -1)
        flipTransform.concat()

        glyphName = textItem.name

        # If italic style, move whole box to fit horizontal position of the slanted bounding box
        # and draw slanted margin lines.
        if style.info.italicAngle: # Draw slanted box if italic. dy is horizontal factor of vertical position.
            dy = math.tan(-style.info.italicAngle * math.pi/180)
        else:
            dy = 0

        if not glyphName in style:
            # Double check if the glyph still exists. Otherwise just draw a
            # marker that it is selected.  Color area below the selected glyph
            # to show that it is selected but unknown.  Only show the missing
            # glyphs if the UI checkbox is selected, should be selected by the
            # typesetter.
            w = textItem.width
            if dy: # In case italic style, draw slanted missing box marker.
                path = NSBezierPath.bezierPath()
                path.moveToPoint_((descender*dy, descender))
                path.lineToPoint_(((emSize+descender)*dy, emSize+descender))
                path.lineToPoint_(((emSize+descender)*dy+w, emSize+descender))
                path.lineToPoint_((descender*dy+w, descender))
                path.lineToPoint_((descender*dy, descender))
            else:
                path = NSBezierPath.bezierPathWithRect_(((0, descender-emSize/3), (w, emSize/3)))
            self.MISSINGGLYPHMARKERCOLOR.set()
            path.fill()
            self.drawTextLabel('?', glyphName, w/2, descender/2-100, ls, self.DARKBLUECOLOR, 'center')
            self.drawTextLabel('?', '(Not in style)', w/2, descender/2-200, ls, self.DARKBLUECOLOR, 'center')

        elif self._editMode == 'spacing':

            glyph = style[glyphName]
            ga = analyzerManager.getGlyphAnalyzer(glyph)

            if glyph.unicode:
                label = '%s | #%04X' % (glyphName, glyph.unicode)
            else:
                label = glyphName

            # Find metric for this glyph. To show the values, and also to
            # determine the minimal size of the label area in order to make all
            # buttons fit.
            lm = ga.leftBaseMargin

            if lm is not None: # If None, there is no outline or component, e.g. as in space.
                lm = int(round(lm))

            w = int(round(glyph.width))

            # Height of colored marker rectangle with space for bars, buttons
            # and glyph name.
            h = 3*bw+3*lg
            rm = ga.rightBaseMargin
            if rm is not None:
                rm = int(round(rm))

            # Make sure the 5 buttons fit on the width.
            metricsW = max(w+2*bw+3*lg, 5*bw+6*lg)

            # Move box horizontally to descender position in case style is
            # italic.
            px = w/2-metricsW/2
            pw = metricsW

            # Draw metrics gray rectangle to hold metrics data. Size and
            # position depends on spacing or kerning.  Gray area below the
            # selected glyph to show metric values and keys. Shift horizontally
            # to match descender position in case style is italic.
            XX = 300

            if dy: # In case italic style, draw slanted box for marker.
                path = NSBezierPath.bezierPath()
                path.moveToPoint_((dy*(descender-h)-XX, descender-h))
                path.lineToPoint_((dy*descender-XX, descender))
                path.lineToPoint_((dy*descender+w+2*XX, descender))
                path.lineToPoint_((dy*(descender-h)+w+2*XX, descender-h))
                path.lineToPoint_((dy*(descender-h)-XX, descender-h))
            else:
                path = NSBezierPath.bezierPathWithRect_(((px+dy*(descender-h)-XX, descender-h), (pw+2*XX, h)))
            self.SPACINGBGCOLOR.set()
            path.fill()

            # Draw margins if they exist
            if lm is not None:
                if lm < 0:
                    c = self.REDCOLOR
                    xx = lm-lg
                else:
                    c = self.DARKBLUECOLOR
                    xx = -lg

                c.set()
                # Shift horizontally to match descender position in case style is italic.
                path = NSBezierPath.bezierPathWithRect_(((dy*(descender-bw), descender-bw), (lm, bw)))
                path.fill()
                # Shift horizontally to match descender position in case style is italic.
                self.drawTextLabel('sb', str(lm), xx+dy*descender, descender, ls, c, 'left')

            if rm is not None:
                if rm < 0:
                    c = self.REDCOLOR
                    xx = w-rm+lg
                else:
                    c = self.DARKBLUECOLOR
                    xx = w+lg
                c.set()
                # Shift horizontally to match descender position in case style is italic.
                path = NSBezierPath.bezierPathWithRect_(((w-rm+dy*(descender-bw), descender-bw), (rm, bw)))
                path.fill()
                # Shift horizontally to match descender position in case style is italic.
                self.drawTextLabel('sb', str(rm), xx+dy*descender, descender, ls, c, 'right')

            # Width
            # Shift horizontally to match descender position in case style is italic.
            self.drawTextLabel('sb', str(w), w/2+dy*descender, descender, ls, self.DARKBLUECOLOR, 'center')

            # Spacing keys, make sure there is space for the buttons in the middle
            y = descender - bw

            if lm is None: # If there are no margin (as in a space), just show the O/P pair
                # Shift horizontally to match descender position in case style is italic.
                self.drawKeyButton(w/2-lg2+dy*y, y, bw, 'O', ls, 'left')
                self.drawKeyButton(w/2+lg2+dy*y, y, bw, 'P', ls, 'right')
            else:
                xl = min(w/2-1.5*(ls+lg), 0)
                xr = max(w/2+1.5*(ls+lg), w)
                # Draw the buttons.
                self.drawKeyButton(xl-lg2+dy*y, y, bw, 'U', ls, 'left')
                self.drawKeyButton(xl+lg2+dy*y, y, bw, 'I', ls, 'right')
                self.drawKeyButton(xr-lg2+dy*y, y, bw, 'O', ls, 'left')
                self.drawKeyButton(xr+lg2+dy*y, y, bw, 'P', ls, 'right')

            self.drawTextLabel('/', label, dy*(descender-3*bw+2*lg), descender-3*bw+2*lg, ls, self.BLACKCOLOR, 'right' )

            # Draw lock if the glyph anchor updating is locked.
            if glyph.lib.get(self.EXTKEY_LOCK):
                self.drawLock()

        elif self._editMode == 'kerning':
            # Draw the info marker below a kerning pair.
            glyph = style[glyphName]
            if glyph.unicode:
                label = '%s | #%04X' % (glyphName, glyph.unicode)
            else:
                label = glyphName

            # Kerning
            k = textItem.kerning or 0 # Kerning value
            label = '%d' % k

            labelValueWidth = -ls*len(label)
            xl = min(-bw-1.5*lg, labelValueWidth)
            y = descender-bw
            h = 3*bw+3*lg # Height of colored marker rectangle
            w = int(round(glyph.width))
            xw = max(3*bw+4*lg, labelValueWidth)

            # Gray area below the selected glyph to show metric values and keys
            XX = 300

            if style.info.italicAngle: # Draw slanted box if italic.
                dy = math.tan(-style.info.italicAngle * math.pi/180)
                path = NSBezierPath.bezierPath()
                path.moveToPoint_((dy*(descender-h)-XX, descender-h))
                path.lineToPoint_((dy*descender-XX, descender))
                path.lineToPoint_((dy*descender+w+2*XX, descender))
                path.lineToPoint_((dy*(descender-h)+w+2*XX, descender-h))
                path.lineToPoint_((dy*(descender-h)-XX, descender-h))
            else:
                path = NSBezierPath.bezierPathWithRect_(((xl-XX, descender-h), (xw+2*XX, h)))

            self.KERNINGBGCOLOR.set()
            path.fill()

            if k < 0:
                self.REDCOLOR.set()
                path = NSBezierPath.bezierPathWithRect_(((0, descender-bw), (abs(k), bw)))
                path.fill()
                self.drawTextLabel('-k', label, -lg, descender, ls, self.REDCOLOR, 'left')
            elif k > 0:
                self.DARKGREENCOLOR.set()
                path = NSBezierPath.bezierPathWithRect_(((-k, descender-bw), (k, bw)))
                path.fill()
                self.drawTextLabel('+k', '+'+label, k+lg, descender, ls, self.DARKGREENCOLOR, 'right')
            else:
                self.BLACKCOLOR.set()
                path = NSBezierPath.bezierPathWithRect_(((0, descender-bw), (1/textScale, bw)))
                path.fill()
                self.drawTextLabel('k', label, lg, descender, ls, self.BLACKCOLOR, 'right')

            # Kerning keys
            self.drawKeyButton(-lg2, y, bw, 'H', ls, 'left')
            self.drawKeyButton(lg2, y, bw, 'J', ls, 'right')
            self.drawTextLabel('/', '%s-%s' % (textItem.prev, glyphName), w/2, descender-3*bw+2*lg, ls, self.BLACKCOLOR, 'center' )

        NSGraphicsContext.restoreGraphicsState()

    def drawProfiles(self, event):
        """Draw the profiles in the editor window."""
        if self._drawGaussProfiles:
            glyph = event.get('glyph')
            if glyph is None:
                return
            style = glyph.font
            scaleValue = event['scale']

            # In case drawing the left and right profile of the current glyph
            if glyph is not None:
                self.drawGaussProfiles(glyph, scaleValue)

    def drawGaussProfiles(self, glyph, scaleValue):
        """Draw gauss profiles on sides of the glyph of what we have as types
        and ranges."""
        sa = analyzerManager.getStyleAnalyzer(style=self.getStyle())
        pg = sa.profileGroups
        ga = sa[glyph.name]
        boundings = ga.boundings
        if boundings is not None:
            l, t, r, b = boundings
            profile = pg.add('left', glyph.name, 'xHeight')
            step = profile.step # Step is identical for all profiles. Only need to get it once.
            for index, level in enumerate(profile.gauss):
                level = 1-level/1000
                path = NSBezierPath.bezierPathWithRect_(((profile.x-step/2, step*index), (step/2-1, step-1)))
                NSColor.colorWithCalibratedRed_green_blue_alpha_(level, level, level, 1).set()
                path.setLineWidth_(0.5*scaleValue)
                path.fill()
            NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 1).set()
            NSBezierPath.bezierPathWithRect_(((profile.x-step/2, profile.minY+step/2), (2, profile.maxY-profile.minY))).fill()

            profile = pg.add('left', glyph.name, 'ascender')
            for index, level in enumerate(profile.gauss):
                level = 1-level/1000
                path = NSBezierPath.bezierPathWithRect_(((profile.x-step, step*index), (step/2-1, step-1)))
                NSColor.colorWithCalibratedRed_green_blue_alpha_(level, level, level, 1).set()
                path.setLineWidth_(0.5*scaleValue)
                path.fill()
            NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 1).set()
            NSBezierPath.bezierPathWithRect_(((profile.x-step, profile.minY+step/2), (2, profile.maxY-profile.minY))).fill()

            profile = pg.add('right', glyph.name, 'xHeight')
            for index, level in enumerate(profile.gauss):
                level = 1-level/1000
                path = NSBezierPath.bezierPathWithRect_(((profile.x+2, step*index), (step/2-1, step-1)))
                NSColor.colorWithCalibratedRed_green_blue_alpha_(level, level, level, 1).set()
                path.setLineWidth_(0.5*scaleValue)
                path.fill()
            NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 1).set()
            NSBezierPath.bezierPathWithRect_(((profile.x+step/2, profile.minY+step/2), (2, profile.maxY-profile.minY))).fill()

            profile = pg.add('right', glyph.name, 'ascender')
            for index, level in enumerate(profile.gauss):
                level = 1-level/1000
                path = NSBezierPath.bezierPathWithRect_(((profile.x+2+step/2, step*index), (step/2-1, step-1)))
                NSColor.colorWithCalibratedRed_green_blue_alpha_(level, level, level, 1).set()
                path.setLineWidth_(0.5*scaleValue)
                path.fill()
            NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 1).set()
            NSBezierPath.bezierPathWithRect_(((profile.x+step, profile.minY+step/2), (2, profile.maxY-profile.minY))).fill()
