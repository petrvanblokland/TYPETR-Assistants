# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     accordionview.py
#

from AppKit import NSApp, NSArray, NSAttributedString, NSBezierPath, NSButton, \
    NSClipView, NSColor, NSCursor, NSDisclosureBezelStyle, NSFont, \
    NSFontAttributeName, NSForegroundColorAttributeName, NSGradient, \
    NSMakeRect, NSNoBorder, NSObject, NSPointInRect, NSPushOnPushOffButton, \
    NSRectFill, NSView, NSViewMaxYMargin, NSViewMinYMargin, NSViewWidthSizable, \
    NSSmallControlSize
from vanilla import Group, ScrollView
from tnbits.base import future

class TNResizerView(NSView):
    """
    """

    def initWithFrame_(self, frame):
        self = super(TNResizerView, self).initWithFrame_(frame)
        self.canDrag = False
        return self

    def drawRect_(self, rect):
        if self.isCollapsed():
            (x, y), (w, h) = self.frame()

            l = 30

            path = NSBezierPath.bezierPath()

            x = round(w/2. - l/2.)
            y = round(h/2.) +.5

            path.moveToPoint_((x, y))
            path.lineToPoint_((x + l, y))

            NSColor.grayColor().set()
            path.stroke()

    def isCollapsed(self):
        return not self.superview().collapsed

    def mouseDown_(self, event):
        self.canDrag = False
        if self.isCollapsed():
            self.canDrag = True
            self.window().disableCursorRects()

            #view = self.getFocusView()
            #self.window().makeFirstResponder_(view)

    def mouseDragged_(self, event):
        if self.canDrag:
            superview = self.superview()
            if superview:
                height = superview.frame().size.height
                superview.adjustSize(height + event.deltaY())

    def mouseUp_(self, event):
        self.canDrag = False
        self.window().enableCursorRects()

    def acceptsFirstResponder(self):
        return True

    def mouseEntered_(self, event):
        if not self.isCollapsed():
            return
        if not self.canDrag:
            NSCursor.resizeUpDownCursor().push()

    def mouseExited_(self, event):
        if not self.canDrag:
            NSCursor.arrowCursor().set()

    def viewDidMoveToWindow(self):
        b = self.bounds()
        self.addTrackingRect_owner_userData_assumeInside_(b, self, None, True)

class TNListViewItem(NSView):
    """
    """

    def __new__(cls, *arg, **kwargs):
        return cls.alloc().init()

    def __init__(self, labelName, vanillaView, maxSize, minSize, height, collapsed=True, canResize=True, headerHeight=20, resizerHeight=10):
        self.labelName = labelName
        self.group = Group((0, headerHeight, 100, maxSize))
        self.group.view = vanillaView

        if not canResize:
            resizerHeight = 0

        self.maxSize = maxSize + headerHeight + resizerHeight
        self.minSize = minSize + headerHeight + resizerHeight
        self.collapsed = collapsed
        self.headerHeight = headerHeight
        self.resizerHeight = resizerHeight
        h = self.headerHeight

        if not self.collapsed:
            h = self.maxSize

        self.setFrame_(NSMakeRect(0, height, 0, h))
        mask = 0
        mask |= NSViewWidthSizable
        self.setAutoresizingMask_(mask)
        self.addSubview_(self.group._nsObject)
        self.disclosureButton = NSButton.alloc().initWithFrame_(NSMakeRect(0, h-self.headerHeight, 20, self.headerHeight))
        mask = 0
        mask |= NSViewMinYMargin
        self.disclosureButton.setAutoresizingMask_(mask)
        self.disclosureButton.setTitle_("")
        self.disclosureButton.setBezelStyle_(NSDisclosureBezelStyle)
        self.disclosureButton.setButtonType_(NSPushOnPushOffButton)
        self.disclosureButton.setState_(not self.collapsed)
        self.addSubview_(self.disclosureButton)

        if canResize:
            self.resizer = TNResizerView.alloc().initWithFrame_(NSMakeRect(0, 0, 0, self.resizerHeight))
            mask = 0
            mask |= NSViewWidthSizable
            self.resizer.setAutoresizingMask_(mask)
            self.addSubview_(self.resizer)

    def setVanillaGroupWidth(self):
        frameWidth, frameHeight = self.frame()[1]
        x, y, w, h = self.group.getPosSize()
        self.group.setPosSize((x, y, frameWidth, h))

    def viewDidMoveToWindow(self):
        self.setVanillaGroupWidth()
        self._recurseThroughSubviews(self.group.getNSView())

    @future.python_method
    def _recurseThroughSubviews(self, view):
        if hasattr(view, "documentView"):
            view = view.documentView()

        if hasattr(view, "vanillaWrapper"):
            vanillaWrapper = view.vanillaWrapper()
            if vanillaWrapper is not None:
                posSize = vanillaWrapper.getPosSize()
                vanillaWrapper.setPosSize(posSize)
                for subview in view.subviews():
                    self._recurseThroughSubviews(subview)

    def hitTest_(self, point):
        r = self.frame()
        r.size.height = self.headerHeight

        if NSPointInRect(point, r):
            return self

        return super(TNListViewItem, self).hitTest_(point)

    def toggle(self):
        (x, y), (w, h) = self.frame()

        if h != self.headerHeight and h != self.maxSize:
            return

        self.disclosureButton.performClick_(self)
        diff = self.maxSize - self.headerHeight
        superview = self.superview()
        superview.setResizingMaskInSubViewWithView_(self)

        if self.collapsed:
            r = NSMakeRect(x, y, w, self.maxSize)
        else:
            diff *= -1
            r = NSMakeRect(x, y, w, self.headerHeight)

        if superview.animate():
            self.animator().setFrame_(r)
        else:
            self.setFrame_(r)

        (x, y), (w, h) = superview.frame()

        if superview.animate():
            superview.animator().setFrame_(NSMakeRect(x, y, w, h+diff))
        else:
            superview.setFrame_(NSMakeRect(x, y, w, h+diff))

        self.collapsed = not self.collapsed

        if not self.collapsed and hasattr(self.group.view, "reload"):
            self.group.view.reload()

        # TODO: store user defaults.
        #setDefault("InspectorWindow%s" %self.labelName, self.collapsed)

    @future.python_method
    def adjustSize(self, newMaxSize):
        if newMaxSize < self.minSize:
            newMaxSize = self.minSize

        diff = newMaxSize - self.maxSize
        self.maxSize = newMaxSize
        superview = self.superview()
        superview.setResizingMaskInSubViewWithView_(self)
        (x, y), (w, h) = self.frame()
        self.setFrame_(NSMakeRect(x, y, w, self.maxSize))
        (x, y), (w, h) = superview.frame()
        superview.setFrame_(NSMakeRect(x, y, w, h+diff))
        frameWidth, frameHeight = self.frame()[1]
        x, y, w, h = self.group.getPosSize()
        self.group.setPosSize((x, y, frameWidth, self.maxSize- self.headerHeight - self.resizerHeight))


    def mouseDown_(self, event):
        if event.clickCount() > 1:
            return

        point = self.convertPoint_fromView_(event.locationInWindow(), None)
        width, height = self.frame().size
        r = NSMakeRect(0, height-self.headerHeight, width, self.headerHeight)

        if NSPointInRect(point, r):
            self.toggle()
            #view = self.getFocusView()
            #self.window().makeFirstResponder_(view)

    def drawRect_(self, rect):
        if self.inLiveResize():
            self.setVanillaGroupWidth()

        NSColor.windowBackgroundColor().set()
        NSRectFill(rect)
        self.drawLabel_(rect)

    def labelAttributes(self):
        return {
            NSFontAttributeName : NSFont.systemFontOfSize_(11),
            NSForegroundColorAttributeName : NSColor.blackColor(),
        }

    def drawLabel_(self, rect):
        width, height = self.frame().size
        r = NSMakeRect(0, height-self.headerHeight, width, self.headerHeight)
        g = NSGradient.alloc().initWithColors_([NSColor.whiteColor(), NSColor.colorWithCalibratedWhite_alpha_(.85, 1), NSColor.whiteColor()])
        g.drawInRect_angle_(r, 90)
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((0, height-self.headerHeight+.5))
        path.lineToPoint_((width, height-self.headerHeight+.5))

        if not self.collapsed:
            path.moveToPoint_((0, .5))
            path.lineToPoint_((width, .5))

        NSColor.grayColor().set()
        path.stroke()
        text = NSAttributedString.alloc().initWithString_attributes_(self.labelName, self.labelAttributes())
        x = 20
        sw, sh = text.size()
        y = height-self.headerHeight + (self.headerHeight - sh) / 2.
        text.drawAtPoint_((x, y))

class TNListClipView(NSClipView):
    """
    """

    def adjustVanillaObjects(self):
        if self.documentView() == None:
            return

        self.documentView().setVanillaGroupWidth()

    def viewBoundsChanged_(self, notification):
        super(TNListClipView, self).viewBoundsChanged_(notification)
        self.adjustVanillaObjects()

    def viewFrameChanged_(self, notification):
        super(TNListClipView, self).viewFrameChanged_(notification)
        self.adjustVanillaObjects()

class TNListView(NSView):
    """
    """

    headerHeight = 18
    resizerHeight = 6
    minSize = 50
    maxSize = 100

    listViewItemClass = TNListViewItem

    def init(self):
        self = super(TNListView, self).init()
        self._animate = True
        return self

    def initWithViewDescriptions_(self, viewDescriptions):
        self = self.init()
        self.setViewDescriptions_(viewDescriptions)
        return self

    def setViewDescriptions_(self, viewDescriptions):
        for subview in list(self.subviews()):
            subview.removeFromSuperviewWithoutNeedingDisplay()

        views = list()
        height = 0

        for description in viewDescriptions:
            label = description["label"]
            vanillaObject = description["view"]
            maxSize = description.get("size", self.maxSize)
            minSize = description.get("minSize", self.minSize)
            collapsed = description.get("collapsed", True)
            canResize = description.get("canResize", True)
            view = self.listViewItemClass(label, vanillaObject, maxSize, minSize=minSize, height=height, collapsed=collapsed, headerHeight=self.headerHeight, resizerHeight=self.resizerHeight, canResize=canResize)

            height += self.headerHeight

            if not collapsed:
                height += maxSize

                if canResize:
                    height += self.resizerHeight

            views.append(view)

        self.setFrame_(NSMakeRect(0, 0, 0, height))
        mask = 0
        mask |= NSViewWidthSizable
        self.setAutoresizingMask_(mask)
        self.setSubviews_(NSArray.arrayWithArray_(views))

        return self

    def setAnimate_(self, value):
        self._animate = value

    def animate(self):
        return self._animate

    def isFlipped(self):
        return True

    def setResizingMaskInSubViewWithView_(self, view):
        subviews = self.subviews()

        if view not in subviews:
            return

        index = subviews.indexOfObject_(view) + 1

        for subview in subviews[:index]:
            mask = 0
            mask |= NSViewWidthSizable
            mask |= NSViewMaxYMargin
            subview.setAutoresizingMask_(mask)

        for subview in subviews[index:]:
            mask = 0
            mask |= NSViewWidthSizable
            mask |= NSViewMinYMargin
            subview.setAutoresizingMask_(mask)

    def setVanillaGroupWidth(self):
        for view in self.subviews():
            view.setVanillaGroupWidth()

class AccordionView(ScrollView):
    """View that expands and collapses multiple subviews."""

    listViewClass = TNListView

    def __init__(self, posSize, descriptions,
            backgroundColor=NSColor.colorWithCalibratedWhite_alpha_(.6, 1.0),
            animate=True):
        self.listView = self.listViewClass.alloc().initWithViewDescriptions_(descriptions)
        self.listView.setAnimate_(animate)
        super(AccordionView, self).__init__(posSize, self.listView,
                autohidesScrollers=False, hasHorizontalScroller=False,
                backgroundColor=backgroundColor,
                clipView=TNListClipView.alloc().init())
        self.getNSScrollView().setDrawsBackground_(True)
        self.getNSScrollView().setBorderType_(NSNoBorder)
        self.getNSScrollView().verticalScroller().setControlSize_(NSSmallControlSize)
        #self.focusView = focusView

    #def getFocusView(self):
    #    return self.focusView
