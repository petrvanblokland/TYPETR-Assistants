# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    eventhandler.py

from AppKit import NSApplication, NSLeftMouseDragged, NSRightMouseDragged, \
    NSLeftMouseUp, NSRightMouseUp, NSShiftKeyMask, NSAlternateKeyMask, \
    NSCommandKeyMask, NSUpArrowFunctionKey, NSDownArrowFunctionKey, \
    NSLeftArrowFunctionKey, NSRightArrowFunctionKey

class EventHandler(object):
    """Takes care of mouse and keyboard events."""

    def isShiftKeyEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        return modifiers & NSShiftKeyMask

    def isOptionKeyEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        #commandDown = modifiers & NSCommandKeyMask
        return modifiers & NSAlternateKeyMask

    def isCommandKeyEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        return  modifiers & NSCommandKeyMask

    def isDoubleClickEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        return event.clickCount() == 2

    def isMouseDownEvent(self):
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        return not event.type() in (NSLeftMouseUp, NSRightMouseUp)

    def isMouseDraggedEvent(self):
        """Answers if the mouse is currently dragging. If there is no event,
        then answer False."""
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        if event is None:
            return False
        return event.type() in (NSLeftMouseDragged, NSRightMouseDragged)

    def isCursorKeyEvent(self):
        """Answers if the current event was a cursor key. This way tools can
        decide not to update; when a change is minor calls will be too
        frequent, for example when dragging cursor keys. Answers false if
        option+shift is down."""
        app = NSApplication.sharedApplication()
        event = app.currentEvent()
        modifiers = event.modifierFlags()
        #return not modifiers & NSShiftKeyMask and \
        return not modifiers & NSShiftKeyMask and \
            event.keyCode in (NSUpArrowFunctionKey, NSDownArrowFunctionKey,NSLeftArrowFunctionKey,NSRightArrowFunctionKey)
