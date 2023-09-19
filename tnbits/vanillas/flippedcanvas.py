# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     flippedcanvas.py
#

from AppKit import NSView, NSColor, NSMakeRect, NSRectFill
from vanilla import Group, ScrollView

from mojo.drawingTools import save, restore

class FlippedCanvasNSView(NSView):
    # DEPRECATED; tnbits.canvas can be flipped.

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, d, delegate, acceptsMouseMoved):
        w, h = d
        self.setFrame_(NSMakeRect(0, 0, w, h))
        self.setDelegate_(delegate)
        self.setAcceptsMouseMoved_(acceptsMouseMoved)

    # flip coordinates to draw from top to bottom
    def isFlipped(self):
        return True

    def setDelegate_(self, delegate):
        self._delegate = delegate

    def delegate(self):
        return self._delegate

    def setAcceptsMouseMoved_(self, value):
        self._acceptsMouseMoved = value

    def acceptsMouseMoved(self):
        return self._acceptsMouseMoved

    def acceptsFirstResponder(self):
        return True

    def sendDelegateAction_(self, method):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)()
        return None

    def sendDelegateAction_event_(self, method, event):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)(event)
        return None

    def drawRect_(self, rect):
        #NSColor.whiteColor().set()
        #NSRectFill(rect)
        #NSColor.blackColor().set()
        save()
        self.delegate().draw(rect)
        restore()

    def becomeFirstResponder(self):
        if self._acceptsMouseMoved:
            self.window().setAcceptsMouseMovedEvents_(True)
        self.sendDelegateAction_("becomeFirstResponder")
        return True

    def resignFirstResponder(self):
        if self._acceptsMouseMoved:
            window = self.window()
            if window:
                window.setAcceptsMouseMovedEvents_(False)
        self.sendDelegateAction_("resignFirstResponder")
        return True

    def save_(self, event):
        self.sendDelegateAction_event_("save", event)

    def mouseDown_(self, event):
        self.sendDelegateAction_event_("mouseDown", event)

    def mouseDragged_(self, event):
        self.sendDelegateAction_event_("mouseDragged", event)

    def mouseUp_(self, event):
        self.sendDelegateAction_event_("mouseUp", event)

    def mouseMoved_(self, event):
        self.sendDelegateAction_event_("mouseMoved", event)

    def rightMouseDown_(self, event):
        result = self.sendDelegateAction_event_("rightMouseDown", event)
        if not result:
            super(FlippedCanvasNSView, self).rightMouseDown_(event)

    def rightMouseDragged_(self, event):
        self.sendDelegateAction_event_("rightMouseDragged", event)

    def rightMouseUp_(self, event):
        self.sendDelegateAction_event_("rightMouseUp", event)

    def keyDown_(self, event):
        self.sendDelegateAction_event_("keyDown", event)

    def keyUp_(self, event):
        self.sendDelegateAction_event_("keyUp", event)

    def flagsChanged_(self, event):
        self.sendDelegateAction_event_("flagsChanged", event)

    def menuForEvent_(self, event):
        print("menuForEvent_")
        return self.sendDelegateAction_("menu")

class FlippedCanvas(Group):
    """
    Canvas(posSize,
            delegate=None,
            canvasSize=(1000, 1000),
            acceptsMouseMoved=False,
            hasHorizontalScroller=True,
            hasVerticalScroller=True,
            autohidesScrollers=False,
            backgroundColor=None,
            drawsBackground=True)

    A view that sends all event to a given delegate.

    all events a delegate could have that can be used:
        - draw()
        - becomeFirstResponder(event)
        - resignFirstResponder(event)
        - mouseDown(event)
        - mouseDragged(event)
        - mouseUp(event)
        - mouseMoved(event) (only when accepsMouseMoved is set True)
        - rightMouseDown(event)
        - rightMouseDragged(event)
        - rightMouseUp(event)
        - keyDown(event)
        - keyUp(event)
        - flagChanged(event)

    Example:

    from mojo.canvas import Canvas
    from mojo.drawingTools import *
    from vanilla import Window

    class ExampleWindow:

        def __init__(self):
            self.w = Window((400, 400), minSize=(200, 200))
            self.w.canvas = Canvas((0, 0, -0, -0), delegate=self)
            self.w.open()

        def draw(self):
            rect(10, 10, 100, 100)

    ExampleWindow()
    """

    def __init__(self, posSize, delegate=None, canvasSize=(1000, 1000),
            acceptsMouseMoved=False, hasHorizontalScroller=True,
            hasVerticalScroller=True, autohidesScrollers=False,
            backgroundColor=None, drawsBackground=True):
        super(FlippedCanvas, self).__init__(posSize)
        if backgroundColor is None:
            backgroundColor = NSColor.grayColor()
        self._view = FlippedCanvasNSView(canvasSize, delegate, acceptsMouseMoved=acceptsMouseMoved)
        self.scrollView = ScrollView((0, 0, -0, -0), self._view, backgroundColor=backgroundColor,
                                    hasHorizontalScroller=hasHorizontalScroller, hasVerticalScroller=hasVerticalScroller,
                                    autohidesScrollers=autohidesScrollers, drawsBackground=drawsBackground)

    def update(self):
        self._view.setNeedsDisplay_(True)

    def updateRect(self, rect):
        x, y, w, h = rect
        self._view.setNeedsDisplayInRect_(((x, y), (w, h)))
        # Doesn't need self._view.setNeedsDisplay_(False)

    def getNSView(self):
        return self._view
