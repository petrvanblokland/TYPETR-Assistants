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
#    slider.py
#
from AppKit import NSBezierPath
from tnbits.base.constants.colors import *
from tnbits.canvas.widget import Widget
from tnbits.toolbox.mathematics import Mathematics

class Slider(Widget):
    """Slider widget to be used on a canvas."""

    def __init__(self, controller, kit, identifier, p0, p1, w=12, name=None,
            color=grayColor, borderColor=blackColor, isSelected=False, pct=50,
            flipped=False, r=4, minValue=0, maxValue=100, defaultValue=None,
            updateCallback=None):
        super(Slider, self).__init__(controller, kit)
        # TODO: switch to normalized instead of percentage.
        self.identifier = identifier
        self.name = name or identifier
        self.p0 = p0
        self.p1 = p1
        x0, y0 = p0
        x1, y1 = p1
        self.l = Mathematics.distance(x0, y0, x1, y1)
        self.w = w
        self.threshold = 2*w # Minimal pixel distance.
        self.snap = 2.5
        self.color = color
        self.borderColor = borderColor
        self.isSelected = isSelected
        self.pct = pct
        self.flipped = flipped
        self.r = r
        self.minValue = minValue
        self.defaultValue = defaultValue
        self.maxValue = maxValue
        self.updateCallback = updateCallback
        if not defaultValue is None:
            defaultPct = self.getPct(defaultValue)
            self.set(defaultPct)

    def getValue(self):
        diff = self.maxValue - self.minValue
        return self.minValue + self.pct / 100. * diff

    def getPct(self, value):
        assert value >= self.minValue
        assert value <= self.maxValue
        diff = self.maxValue - self.minValue
        onepct = diff / 100.
        return (value - self.minValue) / onepct

    # Drawing.

    def draw(self):
        self.drawPath(self.w + 2, blackColor)
        self.drawPath(self.w)
        self.drawButton()
        self.drawTitle()
        self.drawValue()

    def drawValue(self):
        x, y = self.p1
        x += 40

    def drawTitle(self):
        x, y = self.p1
        value = self.getValue()
        msg = '%s = %s' % (self.name, '%.1f' % value)
        x += 15
        if self.flipped:
            y += (self.w + 2) / 2
        self.kit.drawText(msg, x,  y - self.w)

    def drawPath(self, w, color=lightGrayColor):
        path = NSBezierPath.bezierPath()
        path.moveToPoint_(self.p0)
        path.lineToPoint_(self.p1)
        color.set()
        path.setLineWidth_(w)
        path.stroke()
        x, y = self.p0
        self.kit.drawCircle(x - w/2, y - w/2, w, w, fillColor=color)
        x, y = self.p1
        self.kit.drawCircle(x - w/2, y - w/2, w, w, fillColor=color)

    def getCoordinates(self, pct):
        x0, y0 = self.p0
        x1, y1 = self.p1
        x = x0 + (x1 - x0) * pct / 100
        y = y0 + (y1 - y0) * pct / 100
        return x, y

    def drawButton(self, r=4):
        """
        """
        if not self.defaultValue is None:
            pct = self.getPct(self.defaultValue)
            x, y = self.getCoordinates(pct)
            self.kit.drawCircle(x - r, y - r, 2*r, 2*r, fillColor=greyColor)

        if self.isSelected:
            color = magentaColor
        else:
            color = cyanColor

        x, y = self.getCoordinates(self.pct)
        self.kit.drawCircle(x - r, y - r, 2*r, 2*r, strokeColor=blackColor,
                fillColor=color)

    def on(self, point):
        distances = {}
        projectedPoints = {}

        t = Mathematics.orthogonalPoint(point, self.p0, self.p1)

        if t:
            x, y, distance = t
            if distance < self.threshold:
                return True

        return False

    def update(self, mouse):
        """Calculates distances from mouse to slider and sets percentage if
        within range."""
        if self.on(mouse):
            x, y = mouse
            x0, y0 = self.p0
            l0 = Mathematics.distance(x0, y0, x, y)
            pct = l0 / (self.l / 100)
            self.set(pct)
            self.updateCallback(self.pct)

    def set(self, pct, snap=True):
        pct = round(pct, 2)

        if pct <= self.snap:
            pct = 0
        elif abs(100 - pct) <= self.snap:
            pct = 100

        if not self.defaultValue is None:
            defaultPct = self.getPct(self.defaultValue)
            if abs(defaultPct - pct) <= self.snap / 2:
                pct = defaultPct

        self.pct = pct
