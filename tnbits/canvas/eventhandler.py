#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     eventhandler.py
#

from AppKit import NSShiftKeyMask, NSShiftKeyMask, NSAlternateKeyMask, NSCommandKeyMask
import traceback

class CanvasEventHandler(object):
    """Handles keyboard and mouse events and keeps track of positions and
    interaction areas such as bounds.

    self.bounds: current bounds, while dragging; area will be updated, then bounds are
                 copied to upBounds to update previously selected area.
    self.prevBounds: stores previous bounds values.
    self.upBounds: updated on mouse up or key down.
    """

    # Bounds.

    bounds = None
    upBounds = None
    prevBounds = None

    # Mice.

    downMouse = None
    dragMouse = None
    upMouse = None
    prevMouse = None

    def __init__(self, canvas):
        self.canvas = canvas

    def handleShiftDownBounds(self, event):
        """ On shift-down, if possible, copies previously stored bounds to
        current. Else clears all and loads previous Mouse into bounds."""
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask

        if not shiftDown:
            #self.clearSelected()
            pass
        else:
            if self.prevBounds is None:
                self.setBounds(self.getMouse(event))
            else:
                self.bounds = self.getDefaultBounds()
                self.copyBounds(self.prevBounds, self.bounds)

    # Mouse.

    def getMouseFromEvent(self, event):
        """Answer the current mouse position."""
        try:
            mouse = self.canvas.getMouse(event)
            return (mouse.x, mouse.y)
        except Exception as e:
            print(traceback.format_exc())

    def getMouse(self, event):
        """Holding down option restricts the mouse to straight lines."""
        x, y = self.getMouseFromEvent(event)
        modifiers = event.modifierFlags()
        optionDown = modifiers & NSAlternateKeyMask

        if optionDown and not self.prevMouse is None:
            x0, y0 = self.prevMouse
            dx = abs(x - x0)
            dy = abs(y - y0)
            if dx > dy:
                y = y0
            else:
                x = x0

        return (x, y)

    def mouseDown(self, event):
        self.downMouse = self.getMouse(event)
        self.dragMouse = None
        self.upMouse = None
        return self.downMouse

    def mouseDragged(self, event):
        self.dragMouse = self.getMouse(event)
        return self.dragMouse

    def mouseUp(self, event):
        self.dragMouse = None
        self.downMouse = None
        self.prevMouse = self.dragMouse or self.downMouse
        self.upMouse = self.getMouse(event)
        return self.upMouse

    def getMousePosition(self):
        if self.dragMouse:
            return self.dragMouse
        elif self.downMouse:
            return self.downMouse

    def isDragged(self):
        return self.draggedMouse is not None
