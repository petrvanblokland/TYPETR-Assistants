# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010 buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    graphicsstatecontrol.py
#
import math
from vanilla import Group
from AppKit import NSView, NSFont, NSColor, NSFontAttributeName, \
    NSForegroundColorAttributeName, NSBezierPath, NSAttributedString
from tnbits.constants import Constants as C
from tnbits.toolbox.transformer import TX
from tnbits.base import future

class GraphicsStateView(NSView):
    """View that draws the GraphicsState values."""

    C0 = 2
    C1 = 152
    C2 = 304
    C3 = 456
    C4 = 700
    LINE = 12
    GUTTER = LINE
    RADIUS = 36
    MT = 4

    gstate = None

    def drawRect_(self, rect):
        width, height = self.frame()[1]
        y = height - 34
        attr = {NSFontAttributeName : NSFont.systemFontOfSize_(12), NSForegroundColorAttributeName : NSColor.blackColor()}

        if self.gstate is not None:

            # Column 0.
            self.showReferencePoints(self.C0, attr)
            self.showZonePointers(self.C0, 6, attr)
            self.showLevel(self.C0, 11, attr)
            #self.showFunctions(self.C0, 5, attr)

            # Column 1.

            # Column 2.
            self.showRoundState(attr)
            self.showMinimumDistance(attr)
            self.showCutIns(attr)

            # Column 3.
            self.showSloop(self.C3, 1, attr)
            self.showSkip(self.C3, 2, attr)
            self.showFlip(self.C3, 3, attr)
            self.showInhibit(self.C3, 4, attr)

            # Column 4 (circles).
            w = (self.RADIUS + self.GUTTER)
            self.showStateCircle((self.C4, y), self.gstate.projectionVector, 'Projection', self.RADIUS)
            self.showStateCircle((self.C4 + w, y), self.gstate.freedomVector, 'Freedom', self.RADIUS)
            self.showStateCircle((self.C4 + 2*w, y), self.gstate.dualProjectionVector, 'Diagonal', self.RADIUS)

    @future.python_method
    def setGState(self, gstate):
        """Load the viewer with the current gstate. This determines if anything is displayed."""
        self.gstate = gstate

    @future.python_method
    def showStateCircle(self, position, vector, label='', size=10):
        """
        position x, y
        vector: some vector
        size: radius
        """
        x, y = position
        radius = 0.5*size
        path = NSBezierPath.bezierPathWithOvalInRect_(((x-radius*2, y-radius), (size, size)))
        NSColor.whiteColor().set()
        path.fill()
        path.setLineWidth_(1)
        NSColor.blackColor().set()
        path.stroke()

        if vector is not None:
            angle = math.atan2(vector.x, vector.y)
            path = NSBezierPath.alloc().init()
            path.moveToPoint_((x-radius,y))
            path.lineToPoint_((x-radius+math.sin(angle)*radius,y+math.cos(angle)*radius))
            path.setLineWidth_(1)
            path.stroke()

        if label:
            attributes = {
                NSFontAttributeName : NSFont.systemFontOfSize_(9),
                NSForegroundColorAttributeName : NSColor.darkGrayColor()
            }

            text = NSAttributedString.alloc().initWithString_attributes_(label, attributes)
            text.drawAtPoint_((x-36, y+22))

    @future.python_method
    def showReferencePoints(self, col, attr):
        _, height = self.frame()[1]
        text = NSAttributedString.alloc().initWithString_attributes_('Reference Points', attr)
        pos = (col, height - 12 - self.MT)
        text.drawAtPoint_(pos)

        rp0 = self.gstate.referencePoint0
        self.showReferencePoint(rp0, 0, col, attr)
        rp1 = self.gstate.referencePoint1
        self.showReferencePoint(rp1, 1, col, attr)
        rp2 = self.gstate.referencePoint2
        self.showReferencePoint(rp2, 2, col, attr)

    @future.python_method
    def showReferencePoint(self, rp, index, col, attr):
        _, height = self.frame()[1]

        if rp is None:
            rpLabel = u'–'
        else:
            rpLabel = '%d' % rp

        t = 'RP%d: %s' % (index, rpLabel)
        text = NSAttributedString.alloc().initWithString_attributes_(t, attr)
        pos = (col, height - 12 * (index + 2) - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showZonePointers(self, col, line, attr):
        zpts = self.gstate.zonePointers
        zones = self.gstate.zones
        _, height = self.frame()[1]
        text = NSAttributedString.alloc().initWithString_attributes_('Zones', attr)
        pos = (col, height - line*self.LINE - self.MT)
        text.drawAtPoint_(pos)
        line += 1

        for index, zone in enumerate(zpts):
            if zone is zones[C.ZONE0]:
                label = 'Zone 0 (Glyph, %d Points)' % len(zone)
            elif zone is zones[C.ZONE1]:
                label = 'Zone 1 (Twilight, %d Points)' % len(zone)
            else:
                label = u'Error: non-existing zone!'

            t = 'Zone pointer %d: %s' % (index, label)
            text = NSAttributedString.alloc().initWithString_attributes_(t, attr)
            pos = (col, height - line*self.LINE - self.MT)
            text.drawAtPoint_(pos)
            line += 1

    @future.python_method
    def showLevel(self, col, line, attributes):
        _, height = self.frame()[1]
        l = 'Conditional Level: %d' % self.gstate.conditionalLevel
        text = NSAttributedString.alloc().initWithString_attributes_(l, attributes)
        pos = (col, height - line * self.LINE - self.MT)
        text.drawAtPoint_(pos)
        l = 'Function Level: %d' % self.gstate.functionLevel
        text = NSAttributedString.alloc().initWithString_attributes_(l, attributes)
        pos = (col, height - (line + 1) * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showFunctions(self, col, line, attributes):
        _, height = self.frame()[1]
        t = '#functions: %d' % len(self.gstate.functions)
        text = NSAttributedString.alloc().initWithString_attributes_(t, attributes)
        pos = (col, height - line * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showSkip(self, col, line, attributes):
        text = NSAttributedString.alloc().initWithString_attributes_('Skip: (%s) %s' % (2, self.gstate.isSkip()) , attributes)
        _, height = self.frame()[1]
        pos = (col, height - line * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showSloop(self, col, line, attributes):
        text = NSAttributedString.alloc().initWithString_attributes_('Loop: %s' % self.gstate.loop , attributes)
        _, height = self.frame()[1]
        pos = (col, height - line * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showMinimumDistance(self, attributes):
        mindistance = self.gstate.minimumDistance
        if mindistance:
            mindistance = '%du' % mindistance
        text = NSAttributedString.alloc().initWithString_attributes_('Min Dist: %s' % (mindistance or u'–'), attributes)
        _, height = self.frame()[1]
        pos = (self.C2, height - 2 * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showCutIns(self, attributes):
        cvtcutin = self.gstate.cvtCutIn

        if cvtcutin:
            cvtcutin = '%du' % cvtcutin

        text = NSAttributedString.alloc().initWithString_attributes_('Cvt Cut In: %s' % (cvtcutin or u'–'), attributes)
        _, height = self.frame()[1]
        pos = (self.C2, height - self.LINE - self.MT)
        text.drawAtPoint_(pos)
        singlewidthcutin = self.gstate.singleWidthCutIn

        if not singlewidthcutin is None:
            singlewidthcutin = '%du' % singlewidthcutin

        text = NSAttributedString.alloc().initWithString_attributes_('SW Cut In: %s' % (singlewidthcutin or u'–'), attributes)
        pos = (self.C2, 2 * self.LINE)
        text.drawAtPoint_(pos)
        singlewidthvalue = self.gstate.singleWidthValue

        if not singlewidthvalue is None:
            singlewidthvalue = '%du' % singlewidthvalue

        text = NSAttributedString.alloc().initWithString_attributes_('SW Value: %s' % (singlewidthvalue or u'–'), attributes)
        pos = (self.C2, 3 * self.LINE)
        text.drawAtPoint_(pos)

    @future.python_method
    def showRoundState(self, attributes):
        roundstate = self.gstate.roundState
        text = NSAttributedString.alloc().initWithString_attributes_('Round %s' % (roundstate or u'–'), attributes)
        _, height = self.frame()[1]
        pos = (self.C2, height - 4 * self.LINE - self.MT)
        text.drawAtPoint_(pos)
        roundPeriod, roundPhase, roundThreshold = self.gstate.sRoundState

        if not roundPeriod is None:
            roundPeriod = '%0.3f' % roundPeriod

        if not roundPhase is None:
            roundPhase = '%0.3f' % roundPhase

        if not roundThreshold is None:
            roundThreshold = '%0.3f' % roundThreshold

        text = NSAttributedString.alloc().initWithString_attributes_('SR period: %s' % (roundPeriod or u'–'), attributes)
        pos = (self.C2, height - 5 * self.LINE - self.MT)
        text.drawAtPoint_(pos)
        text = NSAttributedString.alloc().initWithString_attributes_('SR phase: %s' % (roundPhase or u'–'), attributes)
        pos = (self.C2, height - 6 * self.LINE - self.MT)
        text.drawAtPoint_(pos)
        text = NSAttributedString.alloc().initWithString_attributes_('SR threshold: %s' % (roundThreshold or u'–'), attributes)
        pos = (self.C2, height - 7 * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showFlip(self, col, line, attributes):
        flip = self.gstate.autoFlip

        if flip:
            flip = 'on'
        else:
            flip = 'off'

        text = NSAttributedString.alloc().initWithString_attributes_('Auto Flip: %s' % flip, attributes)
        _, height = self.frame()[1]
        pos = (col, height - line * self.LINE - self.MT)
        text.drawAtPoint_(pos)

    @future.python_method
    def showInhibit(self, col, line, attributes):
        igf = self.gstate.inhibitGridFitting

        if igf:
            igf = 'on'
        else:
            igf = 'off'

        text = NSAttributedString.alloc().initWithString_attributes_('Inhibit Grid Fitting: %s' % igf, attributes)
        _, height = self.frame()[1]
        pos = (col, height - line * self.LINE - self.MT)
        text.drawAtPoint_(pos)

class GraphicsStateControl(Group):
    """ This is the vanilla wrapper of the Graphics State view."""

    def __init__(self, posSize, delegate):
        self.delegate = delegate
        super(GraphicsStateControl, self).__init__(posSize)
        self._setupView(GraphicsStateView, posSize)
        view = self.getNSView()

    def update(self, gstate=None):
        view = self.getNSView()

        if not gstate is None:
            view.setGState(gstate)

        view.setNeedsDisplay_(True)
