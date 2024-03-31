# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   neon.py
#
#   BaseAssistant part for Neon tubes.
#   Simplified version of Outliner part, we only need tube thicknes and minimal distance defined.
#
import sys
from math import *
from vanilla import *
from AppKit import *

from fontTools.pens.basePen import BasePen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.pointPen import ReverseContourPointPen, AbstractPointPen, PointToSegmentPen
from mojo.UI import UpdateCurrentGlyphView
#from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
from mojo.roboFont import OpenWindow, CurrentGlyph # Used in Outliner
from defcon import Glyph

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart

def roundFloat(f):
    error = 1000000.
    return round(f*error)/error

def checkSmooth( firstAngle, lastAngle):
    if  firstAngle == None or lastAngle == None:
        return True
    error = 4
    firstAngle = degrees(firstAngle)
    lastAngle = degrees(lastAngle)

    if int(firstAngle) + error >= int(lastAngle) >= int(firstAngle) - error:
        return True
    return False

def checkInnerOuter(firstAngle, lastAngle):
    if  firstAngle == None or lastAngle == None:
        return True
    dirAngle = degrees(firstAngle) - degrees(lastAngle)

    if dirAngle > 180:
        dirAngle = 180 - dirAngle
    elif dirAngle < -180:
        dirAngle= -180 - dirAngle

    if dirAngle > 0:
        return True

    if dirAngle <= 0:
        return False

def interSect(seg1, seg2):
    seg1s, seg1e = seg1
    seg2s, seg2e = seg2
    denom = (seg2e.y - seg2s.y)*(seg1e.x - seg1s.x) - (seg2e.x - seg2s.x)*(seg1e.y - seg1s.y)
    if roundFloat(denom) == 0:
        return None
    uanum = (seg2e.x - seg2s.x)*(seg1s.y - seg2s.y) - (seg2e.y - seg2s.y)*(seg1s.x - seg2s.x)
    ubnum = (seg1e.x - seg1s.x)*(seg1s.y - seg2s.y) - (seg1e.y - seg1s.y)*(seg1s.x - seg2s.x)
    ua = uanum/denom
    ub = ubnum/denom
    x = seg1s.x + ua*(seg1e.x - seg1s.x)
    y = seg1s.y + ua*(seg1e.y - seg1s.y)
    return MathPoint(x, y)

def pointOnACurve(p1, p2, p3, p4, value):
    (x1, y1), (cx1, cy1), (cx2, cy2), (x2, y2) = p1, p2, p3, p4
    dx = x1
    cx = (cx1 - dx) * 3.0
    bx = (cx2 - cx1) * 3.0 - cx
    ax = x2 - dx - cx - bx
    dy = y1
    cy = (cy1 - dy) * 3.0
    by = (cy2 - cy1) * 3.0 - cy
    ay = y2 - dy - cy - by
    mx = ax*(value)**3 + bx*(value)**2 + cx*(value) + dx
    my = ay*(value)**3 + by*(value)**2 + cy*(value) + dy
    return MathPoint(mx, my)
        
class MathPoint:

    def __init__(self, x, y=None):
        if y is None:
            x, y = x
        self.x = x
        self.y = y

    def __repr__(self): #### print(p)
        return "<MathPoint x:%s y:%s>" %(self.x, self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def __iter__(self):
        for value in [self.x, self.y]:
            yield value

    def __add__(self, p): # p+ p
        if not isinstance(p, self.__class__):
            return self.__class__(self.x + p, self.y + p)
        return self.__class__(self.x + p.x, self.y + p.y)

    def __sub__(self, p): #p - p
        if not isinstance(p, self.__class__):
            return self.__class__(self.x - p, self.y - p)
        return self.__class__(self.x - p.x, self.y - p.y)

    def __mul__(self, p): ## p * p
        if not isinstance(p, self.__class__):
            return self.__class__(self.x * p, self.y * p)
        return self.__class__(self.x * p.x, self.y * p.y)

    def __div__(self, p):
        if not isinstance(p, self.__class__):
            return self.__class__(self.x / p, self.y / p)
        return self.__class__(self.x / p.x, self.y / p.y)

    def __eq__(self, p): ## if p == p
        if not isinstance(p,self.__class__):
            return False
        return roundFloat(self.x) == roundFloat(p.x) and roundFloat(self.y) == roundFloat(p.y)

    def __ne__(self, p): ## if p != p
        return not self.__eq__(p)

    def copy(self):
        return self.__class__(self.x, self.y)

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)

    def distance(self, p):
        return sqrt((p.x - self.x)**2 + (p.y - self.y)**2)

    def angle(self, other, add=90):
        #### returns the angle of a Line in radians
        b = other.x - self.x
        a = other.y - self.y
        c = sqrt(a**2 + b**2)
        if c == 0:
            return None
        if add is None:
            return b/c
        cosAngle = degrees(acos(b/c))
        sinAngle = degrees(asin(a/c))
        if sinAngle < 0:
            cosAngle = 360 - cosAngle
        return radians(cosAngle + add)

class CleanPointPen(AbstractPointPen):

    def __init__(self, pointPen):
        self.pointPen = pointPen
        self.currentContour = None

    def processContour(self):
        pointPen = self.pointPen
        contour = self.currentContour

        index = 0
        prevAngle = None
        toRemove = []
        for data in contour:
            if data["segmentType"] in ["line", "move"]:
                prevPoint = contour[index-1]
                if prevPoint["segmentType"] in ["line", "move"]:
                    angle = MathPoint(data["point"]).angle(MathPoint(prevPoint["point"]))
                    if prevAngle is not None and angle is not None and roundFloat(prevAngle) == roundFloat(angle):
                        toRemove.append(prevPoint)
                    prevAngle = angle
                else:
                    prevAngle = None
            else:
                prevAngle = None
            index += 1

        for data in toRemove:
            contour.remove(data)

        pointPen.beginPath()
        for data in contour:
            pointPen.addPoint(data["point"], **data)
        pointPen.endPath()

    def beginPath(self):
        assert self.currentContour is None
        self.currentContour = []
        self.onCurve = []

    def endPath(self):
        assert self.currentContour is not None
        self.processContour()
        self.currentContour = None

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        data = dict(point=pt, segmentType=segmentType, smooth=smooth, name=name)
        data.update(kwargs)
        self.currentContour.append(data)

    def addComponent(self, gName, transform):
        assert self.currentContour is None
        self.pointPen.addComponent(gName, transform)

class OutlinePen(BasePen):

    pointClass = MathPoint
    magicCurve = 0.5522847498

    def __init__(self, glyphSet, offset=10, contrast=0, contrastAngle=0, 
        connection="square", cap="round", miterLimit=None, closeOpenPaths=True, 
        preserveComponents=True, expandedPoints=None):
        BasePen.__init__(self, glyphSet)

        self.offset = abs(offset)
        self.contrast = abs(contrast)
        self.contrastAngle = contrastAngle
        # Local adjustments of the offset/contrast/contrasAngle
        # Key is (x, y) of ref point, value is ContrastPen instance 
        if expandedPoints is None:
            expandedPoints = {}
        self.expandedPoints = expandedPoints
        self.ignoreContour = False
        
        self._inputmiterLimit = miterLimit
        if miterLimit is None:
            miterLimit = self.offset * 2
        self.miterLimit = abs(miterLimit)

        self.closeOpenPaths = closeOpenPaths
        
        self.glyph = CurrentGlyph()
        self.points = {}
        for contour in self.glyph.contours:
            for point in contour.points:
                self.points[(point.x, point.y)] = point
                
        self.connectionCallback = getattr(self, "connection%s" % (connection.title()))
        self.capCallback = getattr(self, "cap%s" % (cap.title()))

        self.originalGlyph = Glyph()
        self.originalPen = self.originalGlyph.getPen()

        self.outerGlyph = Glyph()
        self.outerPen = self.outerGlyph.getPen()
        self.outerCurrentPoint = None
        self.outerFirstPoint = None
        self.outerPrevPoint = None

        self.innerGlyph = Glyph()
        self.innerPen = self.innerGlyph.getPen()
        self.innerCurrentPoint = None
        self.innerFirstPoint = None
        self.innerPrevPoint = None

        self.prevPoint = None
        self.firstPoint = None
        self.firstAngle = None
        self.prevAngle = None

        self.shouldHandleMove = True

        self.preserveComponents = preserveComponents
        self.components = []

        self.drawSettings()

    def getOffset(self, thickFactor=1):
        return self.offset * thickFactor
        
    def getThickFactor(self, x, y):
        p = self.points.get((x, y))
        if p is not None:
            for label in p.labels:
                if label.startswith('F'):
                    return float(label[1:])/100    
        return 1

    def _moveTo(self, p):
        x, y = p
        self.thickFactor = self.getThickFactor(x, y)
        
        if self.getOffset() == 0:
            self.outerPen.moveTo((x, y))
            self.innerPen.moveTo((x, y))
            return
        self.originalPen.moveTo((x, y))

        p = self.pointClass(x, y)
        self.prevPoint = p
        self.firstPoint = p
        self.shouldHandleMove = True
                            
    def _lineTo(self, p):
        x, y = p

        self.thickFactor = self.getThickFactor(x, y)

        if self.getOffset() == 0:
            self.outerPen.lineTo((x, y))
            self.innerPen.lineTo((x, y))
            return
        self.originalPen.lineTo((x, y))

        currentPoint = self.pointClass(x, y)
        if currentPoint == self.prevPoint:
            return
        
        self.currentAngle = self.prevPoint.angle(currentPoint)
        thickness = self.getThickness(self.currentAngle, self.thickFactor)
        self.innerCurrentPoint = self.prevPoint - self.pointClass(cos(self.currentAngle), sin(self.currentAngle)) * thickness 
        self.outerCurrentPoint = self.prevPoint + self.pointClass(cos(self.currentAngle), sin(self.currentAngle)) * thickness 

        self.addExpandedPoint(self.prevPoint, (self.innerCurrentPoint, self.outerCurrentPoint))

        self.thickFactor = self.getThickFactor(x, y)

        if self.shouldHandleMove:
            self.shouldHandleMove = False

            self.innerPen.moveTo(self.innerCurrentPoint)
            self.innerFirstPoint = self.innerCurrentPoint

            self.outerPen.moveTo(self.outerCurrentPoint)
            self.outerFirstPoint = self.outerCurrentPoint

            self.firstAngle = self.currentAngle
            
            self.addExpandedPoint(self.prevPoint, (self.innerFirstPoint, self.outerFirstPoint))
        
        else:
            self.buildConnection()


        self.innerCurrentPoint = currentPoint - self.pointClass(cos(self.currentAngle), sin(self.currentAngle)) * thickness 
        self.innerPen.lineTo(self.innerCurrentPoint)
        self.innerPrevPoint = self.innerCurrentPoint

        self.outerCurrentPoint = currentPoint + self.pointClass(cos(self.currentAngle), sin(self.currentAngle)) * thickness 
        self.outerPen.lineTo(self.outerCurrentPoint)
        self.outerPrevPoint = self.outerCurrentPoint

        self.prevPoint = currentPoint
        self.prevAngle = self.currentAngle

        self.addExpandedPoint(currentPoint, (self.innerCurrentPoint, self.outerCurrentPoint))


    def _curveToOne(self, p1, p2, p3):

        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3

        if self.getOffset() == 0:
            self.outerPen.curveTo((x1, y1), (x2, y2), (x3, y3))
            self.innerPen.curveTo((x1, y1), (x2, y2), (x3, y3))
            return
        self.originalPen.curveTo((x1, y1), (x2, y2), (x3, y3))

        p1 = self.pointClass(x1, y1)
        p2 = self.pointClass(x2, y2)
        p3 = self.pointClass(x3, y3)

        if p1 == self.prevPoint:
            p1 = pointOnACurve(self.prevPoint, p1, p2, p3, 0.01)
        if p2 == p3:
            p2 = pointOnACurve(self.prevPoint, p1, p2, p3, 0.99)

        a1 = self.prevPoint.angle(p1)
        a2 = p2.angle(p3)

        assert a1 is not None and a2 is not None
        
        self.currentAngle = a1
        thickness1 = self.getThickness(a1, self.thickFactor)
        thickness2 = self.getThickness(a2, self.thickFactor)

        a1bis = self.prevPoint.angle(p1, 0)
        a2bis = p3.angle(p2, 0)
        intersectPoint = interSect((self. prevPoint, self.prevPoint + self.pointClass(cos(a1), sin(a1)) * 100),
                                   (p3, p3 + self.pointClass(cos(a2), sin(a2)) * 100))

        self.innerCurrentPoint = self.prevPoint - self.pointClass(cos(a1), sin(a1)) * thickness1
        self.outerCurrentPoint = self.prevPoint + self.pointClass(cos(a1), sin(a1)) * thickness1

        self.thickFactor = self.getThickFactor(x3, y3)

        self.addExpandedPoint(self.prevPoint, (self.innerCurrentPoint, self.outerCurrentPoint))

        if self.shouldHandleMove:
            self.shouldHandleMove = False

            self.innerPen.moveTo(self.innerCurrentPoint)
            self.innerFirstPoint = self.innerPrevPoint = self.innerCurrentPoint

            self.outerPen.moveTo(self.outerCurrentPoint)
            self.outerFirstPoint = self.outerPrevPoint = self.outerCurrentPoint

            self.addExpandedPoint(self.prevPoint, (self.innerFirstPoint, self.outerFirstPoint))

            self.firstAngle = a1
        else:
            self.buildConnection()
            
        h1 = None
        if intersectPoint is not None:
            h1 = interSect((self.innerCurrentPoint, self.innerCurrentPoint + self.pointClass(cos(a1bis), sin(a1bis)) * thickness1),  (intersectPoint, p1))
        if h1 is None:
            h1 = p1 - self.pointClass(cos(a1), sin(a1)) * thickness1 

        self.innerCurrentPoint = p3 - self.pointClass(cos(a2), sin(a2)) * thickness2

        h2 = None
        if intersectPoint is not None:
            h2 = interSect((self.innerCurrentPoint, self.innerCurrentPoint + self.pointClass(cos(a2bis), sin(a2bis)) * thickness2), (intersectPoint, p2))
        if h2 is None:
            h2 = p2 - self.pointClass(cos(a1), sin(a1)) * thickness1

        self.innerPen.curveTo(h1, h2, self.innerCurrentPoint)
        self.innerPrevPoint = self.innerCurrentPoint

        ########
        h1 = None
        if intersectPoint is not None:
            h1 = interSect((self.outerCurrentPoint, self.outerCurrentPoint + self.pointClass(cos(a1bis), sin(a1bis)) * thickness1), (intersectPoint, p1))
        if h1 is None:
            h1 = p1 + self.pointClass(cos(a1), sin(a1)) * thickness1

        self.outerCurrentPoint = p3 + self.pointClass(cos(a2), sin(a2)) * thickness2

        h2 = None
        if intersectPoint is not None:
            h2 = interSect((self.outerCurrentPoint, self.outerCurrentPoint + self.pointClass(cos(a2bis), sin(a2bis)) * thickness2), (intersectPoint, p2))
        if h2 is None:
            h2 = p2 + self.pointClass(cos(a1), sin(a1)) * thickness1
        self.outerPen.curveTo(h1, h2, self.outerCurrentPoint)
        self.outerPrevPoint = self.outerCurrentPoint

        self.prevPoint = p3
        self.currentAngle = a2
        self.prevAngle = a2

        self.addExpandedPoint((x3, y3), (self.innerCurrentPoint, self.outerCurrentPoint))
        
    def _closePath(self):

        if self.ignoreContour:
            return
        if self.shouldHandleMove:
            return
        if self.getOffset() == 0:
            self.outerPen.closePath()
            self.innerPen.closePath()
            return

        if not self.prevPoint == self.firstPoint:
            self._lineTo(self.firstPoint)

        self.originalPen.closePath()

        self.innerPrevPoint = self.innerCurrentPoint
        self.innerCurrentPoint = self.innerFirstPoint

        self.outerPrevPoint = self.outerCurrentPoint
        self.outerCurrentPoint = self.outerFirstPoint

        self.prevAngle = self.currentAngle
        self.currentAngle = self.firstAngle

        self.buildConnection(close=True)

        self.innerPen.closePath()
        self.outerPen.closePath()

    def _endPath(self):
        
        if self.ignoreContour:
            self.ignoreContour = False
            return
        if self.shouldHandleMove:
            return

        self.originalPen.endPath()
        self.innerPen.endPath()
        self.outerPen.endPath()

        if self.closeOpenPaths:

            innerContour = self.innerGlyph[-1]
            outerContour = self.outerGlyph[-1]

            innerContour.reverse()

            innerContour[0].segmentType = "line"
            outerContour[0].segmentType = "line"

            self.buildCap(outerContour, innerContour)

            for point in innerContour:
                outerContour.addPoint((point.x, point.y), segmentType=point.segmentType, smooth=point.smooth)

            self.innerGlyph.removeContour(innerContour)

    def addComponent(self, glyphName, transform):
        if self.preserveComponents:
            self.components.append((glyphName, transform))
        else:
            BasePen.addComponent(self, glyphName, transform)

    def addExpandedPoint(self, srcP, dstPts):
        ixy = int(srcP[0]), int(srcP[1])
        if not ixy in self.expandedPoints:
            self.expandedPoints[ixy] = []
        self.expandedPoints[ixy] += list(dstPts)

    ## thickness

    def getThickness(self, angle, thickFactor=1):
        a2 = angle + pi * .5
        f = abs(sin(a2 + radians(self.contrastAngle)))
        f = f ** 5
        return self.getOffset(thickFactor) + self.contrast * f

    ## connections

    def buildConnection(self, close=False):
        if not checkSmooth(self.prevAngle, self.currentAngle):
            if checkInnerOuter(self.prevAngle, self.currentAngle):
                self.connectionCallback(self.outerPrevPoint, self.outerCurrentPoint, self.outerPen, close)
                self.connectionInnerCorner(self.innerPrevPoint, self.innerCurrentPoint, self.innerPen, close)
            else:
                self.connectionCallback(self.innerPrevPoint, self.innerCurrentPoint, self.innerPen, close)
                self.connectionInnerCorner(self.outerPrevPoint, self.outerCurrentPoint, self.outerPen, close)


    def connectionSquare(self, first, last, pen, close):
        angle_1 = radians(degrees(self.prevAngle)+90)
        angle_2 = radians(degrees(self.currentAngle)+90)

        tempFirst = first - self.pointClass(cos(angle_1), sin(angle_1)) * self.miterLimit
        tempLast = last + self.pointClass(cos(angle_2), sin(angle_2)) * self.miterLimit

        newPoint = interSect((first, tempFirst), (last, tempLast))

        if newPoint is not None:

            if self._inputmiterLimit is not None and roundFloat(newPoint.distance(first)) > self._inputmiterLimit:
                pen.lineTo(tempFirst)
                pen.lineTo(tempLast)
            else:
                pen.lineTo(newPoint)

        if not close:
            pen.lineTo(last)

    def connectionRound(self, first, last, pen, close):
        angle_1 = radians(degrees(self.prevAngle)+90)
        angle_2 = radians(degrees(self.currentAngle)+90)

        tempFirst = first - self.pointClass(cos(angle_1), sin(angle_1)) * self.miterLimit
        tempLast = last + self.pointClass(cos(angle_2), sin(angle_2)) * self.miterLimit

        newPoint = interSect((first, tempFirst), (last, tempLast))
        if newPoint is None:
            pen.lineTo(last)
            return
        distance1 = newPoint.distance(first)
        distance2 = newPoint.distance(last)
        if roundFloat(distance1) > self.miterLimit + self.contrast:
            distance1 = self.miterLimit + tempFirst.distance(tempLast) * .7
        if roundFloat(distance2) > self.miterLimit + self.contrast:
            distance2 = self.miterLimit + tempFirst.distance(tempLast) * .7

        distance1 *= self.magicCurve
        distance2 *= self.magicCurve

        bcp1 = first - self.pointClass(cos(angle_1), sin(angle_1)) * distance1 #* self.thickFactor
        bcp2 = last + self.pointClass(cos(angle_2), sin(angle_2)) * distance2 #* self.thickFactor
        pen.curveTo(bcp1, bcp2, last)
        
    def connectionButt(self, first, last, pen, close):
        if not close:
            pen.lineTo(last)

    def connectionInnerCorner(self,  first, last, pen, close):
        if not close:
            pen.lineTo(last)


    ## caps

    def buildCap(self, firstContour, lastContour):
        first = firstContour[-1]
        last = lastContour[0]
        first = self.pointClass(first.x, first.y)
        last = self.pointClass(last.x, last.y)

        self.capCallback(firstContour, lastContour, first, last, self.prevAngle)

        first = lastContour[-1]
        last = firstContour[0]
        first = self.pointClass(first.x, first.y)
        last = self.pointClass(last.x, last.y)

        angle = radians(degrees(self.firstAngle)+180)
        self.capCallback(lastContour, firstContour, first, last, angle)


    def capButt(self, firstContour, lastContour, first, last, angle):
        ## not nothing
        pass

    def capRound(self, firstContour, lastContour, first, last, angle):
        hookedAngle = radians(degrees(angle)+90)

        offset = self.getOffset(self.thickFactor)
        
        p1 = first - self.pointClass(cos(hookedAngle), sin(hookedAngle)) * offset
        p2 = last - self.pointClass(cos(hookedAngle), sin(hookedAngle)) * offset

        oncurve = p1 + (p2-p1)*.5
        
        h1 = first - self.pointClass(cos(hookedAngle), sin(hookedAngle)) * offset * self.magicCurve
        h2 = oncurve + self.pointClass(cos(angle), sin(angle)) * offset * self.magicCurve

        firstContour[-1].smooth = True

        firstContour.addPoint((h1.x, h1.y))
        firstContour.addPoint((h2.x, h2.y))
        firstContour.addPoint((oncurve.x, oncurve.y), smooth=True, segmentType="curve")

        h1 = oncurve - self.pointClass(cos(angle), sin(angle)) * offset * self.magicCurve
        h2 = last - self.pointClass(cos(hookedAngle), sin(hookedAngle)) * offset * self.magicCurve

        firstContour.addPoint((h1.x, h1.y))
        firstContour.addPoint((h2.x, h2.y))

        lastContour[0].segmentType = "curve"
        lastContour[0].smooth = True

    def capSquare(self, firstContour, lastContour, first, last, angle):
        angle = radians(degrees(angle)+90)

        firstContour[-1].smooth = True
        lastContour[0].smooth = True

        p1 = first - self.pointClass(cos(angle), sin(angle)) * self.offset
        firstContour.addPoint((p1.x, p1.y), smooth=False, segmentType="line")

        p2 = last - self.pointClass(cos(angle), sin(angle)) * self.offset
        firstContour.addPoint((p2.x, p2.y), smooth=False, segmentType="line")


    def drawSettings(self, drawOriginal=False, drawInner=False, drawOuter=True):
        self.drawOriginal = drawOriginal
        self.drawInner = drawInner
        self.drawOuter = drawOuter

    def drawPoints(self, pointPen):
        if self.drawInner:
            reversePen = ReverseContourPointPen(pointPen)
            self.innerGlyph.drawPoints(CleanPointPen(reversePen))
        if self.drawOuter:
            self.outerGlyph.drawPoints(CleanPointPen(pointPen))

        if self.drawOriginal:
            if self.drawOuter:
                pointPen = ReverseContourPointPen(pointPen)
            self.originalGlyph.drawPoints(CleanPointPen(pointPen))

        for glyphName, transform in self.components:
            pointPen.addComponent(glyphName, transform)

    def draw(self, pen):
        pointPen = PointToSegmentPen(pen)
        self.drawPoints(pointPen)

    def getGlyph(self):
        glyph = Glyph()
        pointPen = glyph.getPointPen()
        self.drawPoints(pointPen)
        return glyph

class AssistantPartNeon(BaseAssistantPart):
    #    N E O N

    NEON_STROKE_DISTANCE_MARKER_COLOR = 0.2, 0.1, 0.8, 1

    def initMerzNeon(self, container):    
        self.neonDistancePointMarkers = []
        self.neonOvershootPointMarkers = []
        for pIndex in range(self.MAX_POINT_MARKERS): # Max number of points to display in a glyph
            self.neonDistancePointMarkers.append(container.appendOvalSublayer(name="neonDistancePointMarker%03d" % pIndex,
                position=(0, 0),
                size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                fillColor=None,
                strokeColor=self.NEON_STROKE_DISTANCE_MARKER_COLOR,
                strokeWidth=1,
                visible=False,
            ))
            self.neonOvershootPointMarkers.append(container.appendOvalSublayer(name="neonOvershootPointMarker%03d" % pIndex,
                position=(0, 0),
                size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                fillColor=None,
                strokeColor=self.NEON_STROKE_DISTANCE_MARKER_COLOR,
                strokeWidth=1,
                visible=False,
            ))
    
    def updateMerzNeon(self, info):
        g = info['glyph']
        if g is None or g.layer.name == 'foreground':
            return
        f = g.font
        md = self.getMasterData(g.font)
        d = md.distance # Minimal distance between tubes
        stemRadius = md.thickness - md.stemOvershoot # Radius of the stem overshoot point marker
        currentFont = self.getCurrentFont()

        pIndex = 0
        if g is not None and currentFont is not None and currentFont.path == f.path:
            #print('updateMerzNeon', g.name)
            self.updateOutline(g)
            # Update the distance circle markers
            for contour in g.contours:
                for p in contour.points:
                    if p.type != 'offcurve':
                        self.neonDistancePointMarkers[pIndex].setSize((2*d, 2*d))
                        self.neonDistancePointMarkers[pIndex].setPosition((p.x-d, p.y-d))
                        self.neonDistancePointMarkers[pIndex].setVisible(True)
                        self.neonOvershootPointMarkers[pIndex].setSize((2*stemRadius, 2*stemRadius))
                        self.neonOvershootPointMarkers[pIndex].setPosition((p.x-stemRadius, p.y-stemRadius))
                        self.neonOvershootPointMarkers[pIndex].setVisible(True)
                        pIndex += 1
        for n in range(pIndex,len(self.neonDistancePointMarkers)):
            self.neonDistancePointMarkers[n].setVisible(False)
            self.neonOvershootPointMarkers[n].setVisible(False)

    def calculate(self, g, preserveComponents=True):
        c = self.getController()
        if c is None:
            return
        md = self.getMasterData(g.font)
        thickness = md.thickness

        contrast = 0
        contrastAngle = 0
        
        miterLimit = 14

        corner = 'Round'
        cap = 'Round'

        closeOpenPaths = True

        drawOriginal = False
        drawInner = True
        drawOuter = True

        pen = OutlinePen(g.font,
                            thickness,
                            contrast,
                            contrastAngle,
                            connection=corner,
                            cap=cap,
                            miterLimit=miterLimit,
                            closeOpenPaths=closeOpenPaths,
                            preserveComponents=preserveComponents,
                            expandedPoints=self.expandedPoints)
        g.draw(pen)

        pen.drawSettings(drawOriginal=drawOriginal,
                         drawInner=drawInner,
                         drawOuter=drawOuter)

        result = pen.getGlyph()
        return result

    def updateOutline(self, g):
        changed = False
        self.expandedPoints = {}
        bgG = g.getLayer('background')
        fgG = g.getLayer('foreground')
        f = g.font
        
        outline = self.calculate(bgG.naked())
        # Only update for current glyph selection
        if outline is not None and bgG.contours or bgG.components : # Clear only ff there is content
            for component in bgG.components:
                if component.baseGlyph in f:
                    self.updateOutline(f[component.baseGlyph])
            fgG.clear()
            pen = fgG.naked().getPen()
            outline.draw(pen)
            changed = True
        return changed

    def updateView(self, sender=None):
        UpdateCurrentGlyphView()

