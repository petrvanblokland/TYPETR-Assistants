from __future__ import division
import math
import traceback
from AppKit import NSActionCell, NSApp, NSAlternateKeyMask, NSFlagsChanged
from fontTools.pens.cocoaPen import CocoaPen
from mojo.drawingTools import *
from tnbits.vanillas.classnameincrementer import ClassNameIncrementer


def insetRect(rect, inset):
    (x, y), (w, h) = rect
    x += inset
    y += inset
    w -= inset * 2
    h -= inset * 2
    return (x, y), (w, h)


class VarGlyphCell(NSActionCell):

    __metaclass__ = ClassNameIncrementer

    rectInset = -1
    glyphMargin = 8

    @classmethod
    def prefersTrackingUntilMouseUp(cls):
        return True

    def drawInteriorWithFrame_inView_(self, frame, view):
        try:
            self._draw(frame)
        except:
            traceback.print_exc()

    def getPosition(self, frame, t):
        (x, y), (w, h) = insetRect(frame, self.rectInset)
        offset = h / 2
        length = w - h
        xPos = x + offset + t * length
        yPos = y + h/2
        return xPos, yPos

    def _draw(self, frame):
        if self.representedObject() is None:
            # happens when reordering columns :(
            return
        axisValue = self.representedObject().wrappedObject()
        nVal = axisValue.normalizedValue
        (x, y), (w, h) = insetRect(frame, self.rectInset)
        fill(1, 0.95)
        rect(x, y, w, h)

        if w < h:
            # we're too narrow, doesn't make sense to display at all
            return

        values = []
        values.append((axisValue.axis.minValue, 0.75))
        if axisValue.axis.defaultValue not in (axisValue.axis.minValue, axisValue.axis.maxValue):
            values.append((axisValue.axis.defaultValue, 0.75))
        values.append((axisValue.axis.maxValue, 0.75))
        values.append((axisValue.value, 0))

        for val, gray in values:
            xPos, yPos = self.getPosition(frame, axisValue.axis.normalizeValue(val))
            path, (cx, cy), size = axisValue.getOutline(val, CocoaPen)
            path = path.path
            save()
            translate(xPos, yPos)
            scale((h - 2 * self.glyphMargin) / size)
            scale(1, -1)
            translate(-cx, -cy)
            fill(gray)
            drawPath(path)
            restore()

    def trackMouse_inRect_ofView_untilMouseUp_(self, event, rect, view, flag):
        self._trackedRect = rect
        self._didDrag = False
        return super(VarGlyphCell, self).trackMouse_inRect_ofView_untilMouseUp_(event, rect, view, flag)

    def startTrackingAt_inView_(self, pt, view):
        axisValue = self.representedObject().wrappedObject()
        vx, vy = self.getPosition(self._trackedRect, axisValue.normalizedValue)
        mx, my = pt
        distance = math.hypot(vy - my, vx - mx)
        h = self._trackedRect.size.height
        if distance < (h - self.glyphMargin) / 2 or NSApp.currentEvent().modifierFlags() & NSAlternateKeyMask:
            # If we're more or less clicking *on* the black glyph, let's not move until we're dragged.
            # Likewise, if alt is pressed, so we don't get a glitch when the user alt-clicks to go
            # back to the default value.
            return True
        else:
            return self._doTracking(pt, pt, view)

    def continueTracking_at_inView_(self, prevPt, pt, view):
        self._didDrag = True
        return self._doTracking(prevPt, pt, view)

    def _doTracking(self, prevPt, pt, view):
        if NSApp.currentEvent().type() == NSFlagsChanged:
            # pt is bogus
            return True
        (x, y), (w, h) = insetRect(self._trackedRect, self.rectInset)
        axisValueWrapper = self.representedObject()

        val = (pt[0] - (x + h/2)) / (w - h)
        axisValueWrapper.setValue_forKey_(val, "normalizedValue")  # trigger bindings
        self.setObjectValue_(axisValueWrapper.wrappedObject().value)

        return True

    def stopTracking_at_inView_mouseIsUp_(self, a, pt, view, flag):
        if not self._didDrag:
            if NSApp.currentEvent().modifierFlags() & NSAlternateKeyMask:
                axisValueWrapper = self.representedObject()
                axisValue = axisValueWrapper.wrappedObject()
                axisValueWrapper.setValue_forKey_(axisValue.axis.defaultValue, "value")  # trigger bindings
                self.setObjectValue_(axisValueWrapper.wrappedObject().value)
        self._didDrag = False
