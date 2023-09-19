from AppKit import NSView, NSMakeRect, NSColor, NSRectFill
from mojo.drawingTools import save, restore

class CanvasView(NSView):

    def initWithSize_delegate_(cls, size, delegate):
        self = cls.init()
        w, h = size
        self.setFrame_(NSMakeRect(0, 0, w, h))
        self.setDelegate_(delegate)
        return self

    def setDelegate_(self, delegate):
        self._delegate = delegate

    def delegate(self):
        return self._delegate

    def sendDelegateAction_event_(self, method, event):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)(event)
        return None

    def sendDelegateAction_fallback_(self, method, fallback=None):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)()
        return fallback

    def acceptsMouseMoved(self):
        return self.sendDelegateAction_fallback_("acceptsMouseMoved", False)

    def acceptsFirstResponder(self):
        return self.sendDelegateAction_fallback_("acceptsFirstResponder", True)

    def becomeFirstResponder(self):
        if self.acceptsMouseMoved():
            self.window().setAcceptsMouseMovedEvents_(True)
        return self.sendDelegateAction_fallback_("becomeFirstResponder", True)

    def resignFirstResponder(self):
        if self.acceptsMouseMoved():
            window = self.window()
            if window:
                window.setAcceptsMouseMovedEvents_(False)
        return self.sendDelegateAction_fallback_("resignFirstResponder", True)

    def mouseDown_(self, event):
        self.sendDelegateAction_event_("mouseDown", event)

    def mouseMoved_(self, event):
        self.sendDelegateAction_event_("mouseMoved", event)

    def drawRect_(self, rect):
        if self.sendDelegateAction_fallback_("shouldDrawBackground", True):
            NSColor.whiteColor().set()
            NSRectFill(rect)
            NSColor.blackColor().set()
        save()
        self.sendDelegateAction_fallback_("draw")
        restore()

    def update(self):
        self.setNeedsDisplay_(True)
