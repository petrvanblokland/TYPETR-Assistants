# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    pin.py
#
from tnbits.base.constants.colors import *
from tnbits.variations.varmath import *
from tnbits.canvas.widget import Widget

class Pin(Widget):
    """Pin widget to be used on a canvas."""
    #TODO: add snap.

    def __init__(self, controller, kit, identifier, point, angle, l, name=None, w=12,
            color=None, border=None, isSelected=False, ratio=None, headSize=8, threshold=150):
        self.identifier = identifier
        self.name = name or identifier
        self.point = point
        self.angle = angle
        self.l = l
        self.w = w
        self.color = color
        self.border = border
        self.ratio = ratio or 0.0
        self.headSize = headSize
        self.threshold = threshold
        self.color = color
        self.rangePoints = self.getPoints(ratio=0.0)
        super(Pin, self).__init__(controller, kit, isSelected=isSelected)

    def on(self, point):
        _, head = self.getPoints()
        x, y = head
        x1, y1 = point
        dx = x - x1
        dy = y - y1
        s = self.headSize

        if abs(dx) < (s / 2) and abs(dy) < (s / 2):
            return True

        return False

    def update(self, mouse):
        """Displacement distance divided by length."""
        x, y = mouse
        p0, p1 = self.rangePoints
        x0, y0 = p1
        d = Mathematics.distance(x0, y0, x, y)
        t = Mathematics.orthogonalPoint(mouse, p0, p1)

        if not t:
            return False

        px, py, distance = t

        if distance < self.threshold:
            self.ratio = d / self.l
            return True

        return False

    def setLength(self, l):
        self.l = l
        self.rangePoints = self.getPoints(ratio=0.0)

    def draw(self):
        """Draws the pin on the canvas."""
        self.kit.drawCircle(self.point[0] - 2, self.point[1] - 2, 4, 4, blackColor)
        p0, p1 = self.getPoints()
        self.kit.drawLine(p0, self.point, color=darkGrayColor)
        self.kit.drawLine(self.point, p1)
        self.drawPinHead(p1, self.headSize)
        self.drawTitle()

    def drawTitle(self, offset=5):
        p0, p1 = self.getPoints()
        x, y = p1
        msg = '%s = %s' % (self.name, '%.1f' % self.ratio)
        self.kit.drawText(msg, x + offset,  y + offset)

    def drawPinHead(self, point, size=8):
        x, y = point

        if self.isSelected:
            color = magentaColor
        else:
            color = cyanColor

        self.kit.drawCircle(x - size / 2, y - size / 2, size, size, color, blackColor)

    def getPoints(self, ratio=None):
        """Extreme points based on pin point, length, angle and ratio."""
        if ratio is None:
            ratio = self.ratio

        l0 = self.l * ratio
        l1 = self.l * (1 - ratio)
        x0, y0 = self.point
        dx, dy = angle2XY(self.angle, l0)
        p0 = (x0 - dx, y0 - dy)
        dx, dy = angle2XY(self.angle, l1)
        p1 = (x0 + dx, y0 + dy)
        return p0, p1
