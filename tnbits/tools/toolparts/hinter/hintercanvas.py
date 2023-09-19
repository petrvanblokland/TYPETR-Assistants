# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Wayfinding appication.
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.mijksenaar.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    hintercanvas.py
#

from AppKit import NSView, NSColor, NSMakeRect, NSRectFill, NSSize
from vanilla import Group, ScrollView

class HinterCanvasNSView(NSView):
    """
    Inherits from a normal NSView, enables all delegate, first responder, mouse
    / key event and menu functionality.
    """

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, d, delegate, acceptsMouseMoved):
        w, h = d
        self.setFrame_(NSMakeRect(0, 0, w, h))
        self.setDelegate_(delegate)
        self.setAcceptsMouseMoved_(acceptsMouseMoved)

    def setDelegate_(self, delegate):
        self._delegate = delegate

    def delegate(self):
        return self._delegate

    def setAcceptsMouseMoved_(self, value):
        self._acceptsMouseMoved = value

    def acceptsMouseMoved(self):
        return True
        #return self._acceptsMouseMoved

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
        self.delegate().draw(rect)

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

    #   M E N U

    def undo_(self, event):
        self.sendDelegateAction_event_("undo", event)

    def redo_(self, event):
        self.sendDelegateAction_event_("redo", event)

    def cut_(self, event):
        self.sendDelegateAction_event_("cut", event)

    def copy_(self, event):
        self.sendDelegateAction_event_("copy", event)

    def paste_(self, event):
        self.sendDelegateAction_event_("paste", event)

    def copyAsComponent_(self, event):
        self.sendDelegateAction_event_("copyAsComponent", event)

    def delete_(self, event):
        self.sendDelegateAction_event_("delete", event)

    def selectAll_(self, event):
        self.sendDelegateAction_event_("selectAll", event)

    def selectAllAlternate_(self, event):
        self.sendDelegateAction_event_("selectAllAlternate", event)

    def selectAllControl_(self, event):
        self.sendDelegateAction_event_("selectAllControl", event)

    #   E V E N T

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
            super(HinterCanvasNSView, self).rightMouseDown_(event)

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

class HinterCanvas(Group):
    """
    Wraps an HinterCanvasNSView in a ScrollView. Tells which part of the canvas to redraw.

    HinterCanvas(posSize,
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
        - mouseMoved(event) (only when acceptsMouseMoved is set True)
        - rightMouseDown(event)
        - rightMouseDragged(event)
        - rightMouseUp(event)
        - keyDown(event)
        - keyUp(event)
        - flagChanged(event)

    Example:

    from vanilla import Window

    class ExampleWindow:

        def __init__(self):
            self.w = Window((400, 400), minSize=(200, 200))
            self.w.canvas = HinterCanvas((0, 0, -0, -0), delegate=self)
            self.w.open()

        def draw(self):
            rect(10, 10, 100, 100)

    ExampleWindow()
    """

    def __init__(self, posSize, delegate=None, canvasSize=(150, 150),
                acceptsMouseMoved=False, hasHorizontalScroller=True, hasVerticalScroller=True,
                autohidesScrollers=False, backgroundColor=None, drawsBackground=True, width=4000, height=4000):
        super(HinterCanvas, self).__init__(posSize)
        if backgroundColor is None:
            backgroundColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 1)
        self._view = HinterCanvasNSView(canvasSize, delegate, acceptsMouseMoved=acceptsMouseMoved)
        self.scrollView = ScrollView((0, 0, -0, -0), self._view, backgroundColor=backgroundColor,
                                    hasHorizontalScroller=hasHorizontalScroller,
                                hasVerticalScroller=hasVerticalScroller, autohidesScrollers=autohidesScrollers,
                                drawsBackground=drawsBackground)

        self.width = width
        self.height = height

    def update(self):
        """
        Updates entire drawing board.
        """
        self._view.setNeedsDisplay_(True)

    def hide(self):
        """
        """
        self.getNSView().setHidden_(True)

    def show(self):
        """
        """
        self.getNSView().setHidden_(False)

    def zoom(self, z):
        self.getNSSubView().scaleUnitSquareToSize_((z, z))
        self.width = z * self.width
        self.height = z * self.height
        newSize = NSSize(self.width, self.height)
        self.getNSSubView().setFrameSize_(newSize)

    def updateRect(self, rect):
        """
        Updates only a certain rectangular area of drawing board.
        """
        x, y, w, h = rect
        #self._view.setNeedsDisplayInRect_(((x, y), (w, h)))
        #self._view.setNeedsDisplay_(False)

    def getNSSubView(self):
        return self._view
