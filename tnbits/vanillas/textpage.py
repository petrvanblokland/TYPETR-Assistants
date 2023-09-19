# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     textpage.py
#

import weakref
from mouse import Mouse
from eventview import EventView
from AppKit import NSFontAttributeName, NSFont, NSColor
from AppKit import NSForegroundColorAttributeName, NSCommandKeyMask, NSShiftKeyMask
from AppKit import NSBezierPath, NSString, NSAttributedString, NSMakeRect
from mojo.drawingTools import rect, fill

from vanilla import VanillaBaseObject

class TextPage(VanillaBaseObject):

    defaultTextAttributes = {NSFontAttributeName: NSFont.fontWithName_size_("Verdana", 12),
                             NSForegroundColorAttributeName: NSColor.blackColor()}

    def __init__(self, posSize, parent, model=None):
        """The `Spreadsheet` defines the generic behavior of a spread sheet.
        The _cols_ can be an integer, indicating the number of columns, or it
        can be a list of names for all columns. The same applies to the _rows_
        attribute."""
        self._posSize = posSize
        self.model = model # Weakref to style/family model
        self.parent = parent # Weakref to implementing tool
        self._mouse = None
        _, _, self._width, self._height = posSize

        # Set view.
        self._nsObject = view = EventView.alloc().init()
        view.setFrame_(((0, 0), (self._width, self._height)))
        self.clearMouse()

    #   self.model

    def _get_model(self):
        return self._model()

    def _set_model(self, model):
        if model is None:
            self._model = None
        else:
            self._model = weakref.ref(model)

    model = property(_get_model, _set_model)

    #   self.parent

    def _get_parent(self):
        return self._parent()

    def _set_parent(self, parent):
        self._parent = weakref.ref(parent)

    parent = property(_get_parent, _set_parent)

    def getPreference(self, name):
        """Answer the preference value of *name* as defined by the implementing parent tool."""
        return self.parent.getPreference(name, forceDefault=True)

    def getView(self):
        return self._nsObject

    def getWindowSize(self):
        w, h = self._nsObject.bounds()[1]
        return w, h

    def getWindowWidth(self):
        w, _ = self._nsObject.bounds()[1]
        return w

    def getWindowHeight(self):
        _, h = self._nsObject.bounds()[1]
        return h

    def getWindowPosSize(self):
        x, y = self._nsObject.bounds()[0]
        return x, y, 100, 100

    #   E V E N T S

    def mouseDown(self, event):
        self._mouse.p = event.locationInWindow()
        self._mouse.modifiers = modifiers = event.modifierFlags()
        self._mouse.dragging = False

        if modifiers & NSCommandKeyMask:
            # Cmd-key, toggle current position.
            pass
        elif modifiers & NSShiftKeyMask:
            pass
        else:
            # Otherwise clear selection and set the current position.
            self.clearSelection()

        self.update()

    def mouseUp(self, event):
        """
        Shows edit cell with contents.
        """
        self._mouse.dragging = False
        self.update()

    def mouseDragged(self, event):
        self._mouse.dragging = True
        p = event.locationInWindow()
        xy = self.mouse2Cell(p.x, p.y)
        self.marqueeSelect(xy)
        self.update()

    def keyDown(self, event):
        self._colNames
        print('keyDown', event)

    def keyUp(self, event):
        print('keyUp', event)

    def clearMouse(self):
        self._mouse = Mouse()

    #   D R A W

    def update(self):
        self._nsObject.display()

    def draw(self, rect):
        """
        Renders the cells that fall inside rectangle.
        """
        self.drawCanvas(rect)
        self.drawText(rect)

    def setColor(self, c):
        self.setRGBA(c[0], c[1], c[2], c[3])

    def setRGBA(self, r, g, b, a):
        NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a).set()

    def fillRect(self, x, y, w, h):
        box = NSMakeRect(x, y, w, h)
        path = NSBezierPath.bezierPathWithRect_(box)
        path.fill()

    def drawCanvas(self, r):
        """Initialize the canvas with the defined background color."""
        self.setColor(self.getPreference('backgroundColor'))
        self.fillRect(10, 10, 300, 400)

    def drawText(self, r):
        """Draw the sample text for this model family in the give rectangle."""
        print('#@#@', r)
