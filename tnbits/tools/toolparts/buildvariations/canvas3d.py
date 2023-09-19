from __future__ import division
import traceback
import math
from AppKit import NSAlternateKeyMask
from mojo.canvas import CanvasGroup#, CanvasNSView
from tnbits.vanillas.flippedcanvas import FlippedCanvas
from mojo.drawingTools import *
transform = drawingTools._transform
from tnbits.tools.toolparts.buildvariations.transform3d import Transform3D
from tnbits.vanillas.classnameincrementer import ClassNameIncrementer


class Item3D(object):

    """This object represents one item drawn in the 3D canvas."""

    def __init__(self, point, path, center, size, fillColor=None):
        self.point = point
        self.path = path
        self.center = center
        self.size = size
        self.fillColor = fillColor
        self.transformedPoint = None

    def draw(self):
        save()
        cx, cy = self.center
        scale(1/self.size)
        translate(-cx, -cy)
        drawPath(self.path)
        restore()


class Canvas3DNSView(CanvasNSView):

    __metaclass__ = ClassNameIncrementer

    def scrollWheel_(self, event):
        self.sendDelegateAction_event_("scrollWheel", event)

    def magnifyWithEvent_(self, event):
        self.sendDelegateAction_event_("magnifyWithEvent", event)

    def rotateWithEvent_(self, event):
        self.sendDelegateAction_event_("rotateWithEvent", event)

    def swipeWithEvent_(self, event):
        self.sendDelegateAction_event_("swipeWithEvent", event)


class Canvas3D(CanvasGroup):

    nsViewClass = Canvas3DNSView

    backgroundColor = (0.9,)
    strokeColor = (1, 1)
    strokeWidth = 0.025
    fillColor = (0,)
    distortShapes = True
    doStroke = True

    def __init__(self, posSize, items, angleX=0, angleY=0):
        super(CanvasGroup, self).__init__(posSize)  # XXX use *CanvasGroup*, to work around mojo inheritance bug
        self.getNSView().setDelegate_(self)
        self.items = items
        self.angleX = angleX
        self.angleY = angleY
        self.individualZoom = 1.0
        self.totalZoom = 1.0
        self.affine = None
        self.updateItems()

    def set(self, items):
        self.items = items
        self.updateItems()
        self.update()

    def set3DGlyphs(self, onOff):
        self.distortShapes = onOff
        self.update()

    def setStroke(self, onOff):
        self.doStroke = onOff
        self.update()

    def mouseDown(self, event):
        point = self._nsObject.convertPoint_fromView_(event.locationInWindow(), None)
        # XXX

    def scrollWheel(self, event):
        scaleFactor = 0.5
        self.rotateEvent(scaleFactor * event.scrollingDeltaX(), scaleFactor * event.scrollingDeltaY())

    def mouseDragged(self, event):
        self.rotateEvent(event.deltaX(), event.deltaY())

    def rotateEvent(self, deltaX, deltaY):
        scaleFactor = 0.01
        self.angleX -= scaleFactor * deltaY
        maxVertocalRotate = 45
        self.angleX = min(self.angleX, math.radians(maxVertocalRotate))
        self.angleX = max(self.angleX, math.radians(-maxVertocalRotate))
        self.angleY -= scaleFactor * deltaX
        self.angleY = self.angleY % (2 * math.pi)
        self.updateItems()
        self.update()

    def magnifyWithEvent(self, event):
        if event.modifierFlags() & NSAlternateKeyMask:
            self.totalZoom += event.magnification()
            self.totalZoom = max(0.5, self.totalZoom)
            self.totalZoom = min(2, self.totalZoom)
        else:
            self.individualZoom += event.magnification()
            self.individualZoom = max(0.1, self.individualZoom)
            self.individualZoom = min(2, self.individualZoom)
        self.updateItems()
        self.update()

    def mouseUp(self, event):
        pass

    def draw(self):
        try:
            self._draw()
        except:
            traceback.print_exc()

    def updateItems(self):
        t = Transform3D()
        t = t.rotateX(self.angleX)
        t = t.rotateY(self.angleY)
        angle = self.angleY + math.radians(45)
        localT = t.rotateY(math.radians(-90) * (angle // math.radians(90)))
        self.affine = localT.getAffineTransform2D(2)
        for item in self.items:
            item.transformedPoint = t.transformPoint(item.point)
        self.items.sort(key=lambda item: item.transformedPoint[2])

    def _draw(self):
        (x, y), (w, h) = self._nsObject.bounds()

        size = min(w, h)

        lineJoin("round")
        fill(*self.backgroundColor)
        rect(x, y, w, h)
        translate(x + w/2, y + h/2)
        scale(0.5 * size * self.totalZoom)
        stroke(None)
        for item in self.items:
            x, y, z = item.transformedPoint
            save()
            translate(x, y)
            scale(0.3 * self.individualZoom)
            if self.distortShapes:
                transform(self.affine)
            if self.doStroke:
                stroke(*self.strokeColor)
                strokeWidth(item.size * self.strokeWidth / self.individualZoom)
                fill(None)
                item.draw()
                stroke(None)
            fill(*(item.fillColor or self.fillColor))
            item.draw()
            restore()
