# -*- coding: UTF-8 -*-

"""
from AppKit import *
from defconAppKit.windows.baseWindow import BaseWindowController
from lib.tools.bezierTools import curveConverter, roundValue
from mojo.glyphPreview import GlyphPreview
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import fill, stroke, strokeWidth, oval, rect, line, fontSize, text, drawPath, save, restore, translate
from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
from fontTools.pens.cocoaPen import CocoaPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.pointPen import ReverseContourPointPen
from defcon import Glyph
from math import sqrt, cos, sin, acos, asin, atan2, degrees, radians, tan, pi
from typelib.toolset import openFont
from typelib.typetr.upgrade_neon import anchors, glyphset, fixspacing
from typelib.typetr.upgrade_neon.draw import drawFixAccentCloud

import importlib
import typelib
import typelib.typetr.upgrade_neon
import typelib.typetr.upgrade_neon.fixspacing
import typelib.toolset.glyph

importlib.reload(typelib)
importlib.reload(typelib.typetr.upgrade_neon)
importlib.reload(typelib.typetr.upgrade_neon.fixspacing)
from typelib.typetr.upgrade_neon.fixspacing import fixWidth, BASE1, BASE2
importlib.reload(typelib.toolset)
importlib.reload(typelib.toolset.glyph)


DO_REMOVE_OBSOLETE_GLYPHS = True
DO_CLEAR_ALL_ANCHORS = True # WARNING: This clears the position of all anchors in the font first.
ENABLE_FIXING_ANCHORS = False

"""
import sys
from math import *
from vanilla import *
from AppKit import *

from fontTools.pens.basePen import BasePen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.pointPen import ReverseContourPointPen, AbstractPointPen, PointToSegmentPen
from mojo.UI import UpdateCurrentGlyphView
#from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
from mojo.UI import UpdateCurrentGlyphView
from mojo.roboFont import OpenWindow, CurrentGlyph, CurrentFont
from defcon import Glyph

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

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

    def initMerzNeon(self, container):    
        pass
    
    def setGlyphNeon(self, g):
        """Gets called when the EditorWindow selected a new glyph. Update the control values
        for the Neon part from font.lib."""
        c = self.getController()
        f = g.font
        thickness = self.getLib(f, self.LIB_THICKNESS, self.DEFAULT_THICKNESS)
        c.w.thickness.set(thickness)
        c.w.thicknessText.set(str(thickness))
        print('setGlyphNeon: Set thickness', thickness)
        """
        contrast = int(c.w.contrast.get())
        self.setLib(f, self.LIB_CONTRAST, contrast)
        contrastAngle = int(c.w.contrastAngle.get())
        self.setLib(f, self.LIB_CONTRAST_ANGLE, contrastAngle)
        keepBounds = c.w.keepBounds.get()
        self.setLib(f, self.LIB_KEEP_BOUNDS, keepBounds)
        preserveComponents = bool(c.w.preserveComponents.get())
        self.setLib(f, self.LIB_PRESERVE_COMPONENTS, preserveComponents)

        miterLimit = int(c.w.miterLimit.get())
        if c.w.connectmiterLimit.get():
            miterLimit = thickness
            c.w.miterLimit.set(miterLimit)
        self.setLib(f, self.LIB_CONNECT_MITER_LIMIT, c.w.connectmiterLimit)
        self.setLib(f, self.LIB_MITER_LIMIT, miterLimit)

        corner = c.w.corner.getItems()[c.w.corner.get()]
        self.setLib(f, self.LIB_CORNER, corner )

        closeOpenPath = c.w.useCap.get()
        self.setLib(f, self.LIB_CLOSE_OPEN_PATH, closeOpenPath)

        cap = c.w.cap.getItems()[c.w.cap.get()]
        self.setLib(f, self.LIB_CAP, cap )

        drawOriginal = c.w.drawOriginal.get()
        self.setLib(f, self.LIB_DRAW_ORIGINAL, drawOriginal)

        drawInner = c.w.drawInner.get()
        self.setLib(f, self.LIB_DRAW_INNER, drawInner)

        drawOuter = c.w.drawOuter.get()
        self.setLib(f, self.LIB_DRAW_OUTER, drawOuter)
        
        c.w.thicknessText.set("%i" % thickness)
        c.w.contrastText.set("%i" % contrast)
        c.w.contrastAngleText.set("%i" % contrastAngle)
        c.w.miterLimitText.set("%i" % miterLimit)
        """
    def updateMerzNeon(self, info):
        g = info['glyph']
        if g.layer.name == 'foreground':
            return
        f = CurrentFont()

        if g is not None and f is not None and g.font.path == f.path:
            #print('updateMerzNeon', g.name)
            self.updateOutline(g)

    def calculate(self, g, preserveComponents=True):
        c = self.getController()
        if c is None:
            return

        thickness = c.w.thickness.get()
        contrast = c.w.contrast.get()
        contrastAngle = c.w.contrastAngle.get()
        keepBounds = c.w.keepBounds.get()
        
        if c.w.connectmiterLimit.get():
            miterLimit = None
        else:
            miterLimit = c.w.miterLimit.get()

        corner = c.w.corner.getItems()[c.w.corner.get()]
        cap = c.w.cap.getItems()[c.w.cap.get()]

        closeOpenPaths = c.w.useCap.get()

        drawOriginal = c.w.drawOriginal.get()
        drawInner = c.w.drawInner.get()
        drawOuter = c.w.drawOuter.get()

        pen = OutlinePen(g.getParent(),
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
        if keepBounds:
            if g.bounds and result.bounds:
                minx1, miny1, maxx1, maxy1 = g.bounds
                minx2, miny2, maxx2, maxy2 = result.bounds

                h1 = maxy1 - miny1

                w2 = maxx2 - minx2
                h2 = maxy2 - miny2

                s = h1 / h2

                center = minx2 + w2 * .5, miny2 + h2 *.5

                dummy = RGlyph(result)
                dummy.scale((s, s), center)

        return result

    def updateOutline(self, g):
        self.expandedPoints = {}
        bgG = g.getLayer('background')
        fgG = g.getLayer('foreground')
        f = g.font
        
        outline = self.calculate(bgG.naked())
        # Only update for current glyph selection
        if bgG.contours or bgG.components : # Clear only of there is content
            for component in bgG.components:
                if component.baseGlyph in f:
                    self.updateOutline(f[component.baseGlyph])
            fgG.clear()
            pen = fgG.naked().getPen()
            outline.draw(pen)

    DEFAULT_THICKNESS = 10
    DEFAULT_CONTRAST = 0
    DEFAULT_CONTRAST_ANGLE = 0
    DEFAULT_CONNECT_MITER_LIMIT = True
    DEFAULT_MITER_LIMIT = 10
    DEFAULT_PRESERVE_COMPONENTS = True
    DEFAULT_CLOSE_OPEN_PATH = True
    DEFAULT_CORNER = 'Round'
    DEFAULT_CAP = 'Round'
    DEFAULT_KEEP_BOUNDS = False

    # font.lib[self.LIB_KEY][...] keys for this part
    LIB_THICKNESS = 'neon.thickness'
    LIB_CONTRAST = 'neon.contrast'
    LIB_CONTRAST_ANGLE = 'neon.contrastAngle'
    LIB_KEEP_BOUNDS = 'neon.keepBounds'
    LIB_PRESERVE_COMPONENTS = 'neon.preserveComponents'
    LIB_CONNECT_MITER_LIMIT = 'neon.connectMiterLimit'
    LIB_MITER_LIMIT = 'neon.miterLimit'
    LIB_CORNER = 'neon.corner'
    LIB_CLOSE_OPEN_PATH = 'closeOpenPath'
    LIB_CAP = 'neon.cap'
    LIB_KEEP_BOUNDS = 'neon.keepBounds'
    LIB_DRAW_ORIGINAL = 'neon.drawOriginal'
    LIB_DRAW_INNER = 'neon.drawInner'
    LIB_DRAW_OUTER = 'neon.drawOuter'
    LIB_FILL = 'neon.fill'
    LIB_STROKE = 'neon.stroke'
    LIB_COLOR = 'neon.color'
    LIB_PREVIEW = 'neon.preview'

    def buildNeon(self, y):
        """Build the Neon stuff: Merz components and """
        # Calculate the column positions
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        f = CurrentFont()

        w = self.W
        h = 700
        middle = 135
        textMiddle = middle - 27
        y += 10
        self.w._thickness = TextBox((0, y-3, textMiddle, 17), 'Thickness:', alignment="right")

        thicknessValue = self.getLib(f, self.LIB_THICKNESS, self.DEFAULT_THICKNESS)

        self.w.thickness = Slider((middle, y, -50, 15),
                                 minValue=1,
                                 maxValue=200,
                                 callback=self.parametersChanged,
                                 value=thicknessValue)
        self.w.thicknessText = EditText((-40, y, -10, 17), thicknessValue,
                                       callback=self.parametersTextChanged,
                                       sizeStyle="small")
        y += 33
        self.w._contrast = TextBox((0, y-3, textMiddle, 17), 'Contrast:', alignment="right")

        contrastValue = self.getLib(f, self.LIB_CONTRAST, self.DEFAULT_CONTRAST)

        self.w.contrast = Slider((middle, y, -50, 15),
                                 minValue=0,
                                 maxValue=200,
                                 callback=self.parametersChanged,
                                 value=contrastValue)
        self.w.contrastText = EditText((-40, y, -10, 17), contrastValue,
                                       callback=self.parametersTextChanged,
                                       sizeStyle="small")
        y += 33
        self.w._contrastAngle = TextBox((0, y-3, textMiddle, 17), 'Contrast Angle:', alignment="right")

        contrastAngleValue = self.getLib(f, self.LIB_CONTRAST_ANGLE, self.DEFAULT_CONTRAST_ANGLE)

        self.w.contrastAngle = Slider((middle, y-10, 30, 30),
                                 minValue=0,
                                 maxValue=360,
                                 callback=self.contrastAngleCallback,
                                 value=contrastAngleValue)
        self.w.contrastAngle.getNSSlider().cell().setSliderType_(NSCircularSlider)
        self.w.contrastAngleText = EditText((-40, y, -10, 17), contrastAngleValue,
                                       callback=self.parametersTextChanged,
                                       sizeStyle="small")

        y += 33
        
        self.w._pointPen= TextBox((0, y-3, textMiddle, 17), 'Point Label:', alignment="right")

        self.w.pointPen = Slider((middle, y, -50, 15),
                                    minValue=50,
                                    maxValue=110,
                                    callback=self.pointPenChanged,
                                    value=100)
        self.w.pointPenText = EditText((-40, y, -10, 17), 100,
                                          callback=self.pointPenTextChanged,
                                          sizeStyle="small")
        y += 24
        x = 8
        BX = 40
        # Buttons with predefined values for PointPen labels
        for bIndex, buttonValue in enumerate((50, 55, 60, 65, 70, 72, 75, 76, 78, 80, 82, 84, 85, 86, 88, 90, 92, 94, 96, 98, 100)):
            button = Button((x, y, BX, 24), str(buttonValue), self.setPointPenByValue)
            button.value = buttonValue
            setattr(self.w, 'pointPenButton%d' % bIndex, button)
            if bIndex in (6, 13):
                x = 8
                y += 24
            else:
                x += BX+2
        
        # Buttons with predefined right margins
        mry = y + 130
        x = 8
        BX = 55
        for bIndex, rm in enumerate([-65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125, -130, -135, -140, -145, -150, -165, -170, -175, -180, -185, -190, -195, -200]):
            button = Button((x, mry, BX, 24), str(rm), self.setRightMarginByValue)
            button.value = rm
            setattr(self.w, 'rightMarginButton%d' % rm, button)
            if bIndex % 2:
                x = 8
                mry += 24
            else:
                x += BX+2            
        y += 33

        self.w._miterLimit = TextBox((0, y-3, textMiddle, 17), 'MiterLimit:', alignment="right")

        connectmiterLimitValue = self.getLib(f, self.LIB_CONNECT_MITER_LIMIT, self.DEFAULT_CONNECT_MITER_LIMIT)

        self.w.connectmiterLimit = CheckBox((middle-22, y-3, 20, 17), "",
                                             callback=self.connectmiterLimit,
                                             value=connectmiterLimitValue)

        miterLimitValue = self.getLib(f, self.LIB_MITER_LIMIT, self.DEFAULT_MITER_LIMIT)

        self.w.miterLimit = Slider((middle, y, -50, 15),
                                    minValue=1,
                                    maxValue=200,
                                    callback=self.parametersChanged,
                                    value=miterLimitValue)
        self.w.miterLimitText = EditText((-40, y, -10, 17), miterLimitValue,
                                          callback=self.parametersTextChanged,
                                          sizeStyle="small")

        self.w.miterLimit.enable(not connectmiterLimitValue)
        self.w.miterLimitText.enable(not connectmiterLimitValue)

        y += 30

        cornerAndCap = ["Square", "Round", "Butt"]

        self.w._corner = TextBox((0, y, textMiddle, 17), 'Corner:', alignment="right")
        self.w.corner = PopUpButton((middle-2, y-2, -48, 22), cornerAndCap, callback=self.parametersTextChanged)
        self.w.corner.set(1)

        y += 30

        self.w._cap = TextBox((0, y, textMiddle, 17), 'Cap:', alignment="right")
        useCapValue = self.getLib(f, self.LIB_CLOSE_OPEN_PATH, self.DEFAULT_CLOSE_OPEN_PATH)
        self.w.useCap = CheckBox((middle-22, y, 20, 17), "",
                                             callback=self.useCapCallback,
                                             value=useCapValue)
        self.w.cap = PopUpButton((middle-2, y-2, -48, 22), cornerAndCap, callback=self.parametersTextChanged)
        self.w.cap.enable(useCapValue)
        self.w.cap.set(1)

        cornerValue = self.getLib(f, self.LIB_CORNER, self.DEFAULT_CORNER)
        if cornerValue in cornerAndCap:
            self.w.corner.set(cornerAndCap.index(cornerValue))

        capValue = self.getLib(f, self.LIB_CAP, self.DEFAULT_CAP)
        if capValue in cornerAndCap:
            self.w.cap.set(cornerAndCap.index(capValue))

        y += 33

        self.w.keepBounds = CheckBox((middle-3, y, middle, 22), "Keep Bounds",
                                   value=self.getLib(f, self.LIB_KEEP_BOUNDS, self.DEFAULT_KEEP_BOUNDS),
                                   callback=self.parametersTextChanged)
        y += 30
        self.w.drawOriginal = CheckBox((middle-3, y, middle, 22), "Draw Source",
                                   value=self.getLib(f, self.LIB_DRAW_ORIGINAL, False),
                                   callback=self.parametersTextChanged)
        y += 30
        self.w.drawInner = CheckBox((middle-3, y, middle, 22), "Draw Inner",
                                   value=self.getLib(f, self.LIB_DRAW_INNER, True),
                                   callback=self.parametersTextChanged)
        y += 30
        self.w.drawOuter = CheckBox((middle-3, y, middle, 22), "Draw Outer",
                                   value=self.getLib(f, self.LIB_DRAW_OUTER, True),
                                   callback=self.parametersTextChanged)

        y += 35
        self.w.preview = CheckBox((middle-3, y, middle, 22), "Preview",
                               value=self.getLib(f, self.LIB_PREVIEW, False),
                               callback=self.previewCallback)
        y += 30
        self.w.fill = CheckBox((middle-3+10, y, middle, 22), "Fill",
                               value=self.getLib(f, self.LIB_FILL, False),
                               callback=self.fillCallback, sizeStyle="small")
        y += 25
        self.w.stroke = CheckBox((middle-3+10, y, middle, 22), "Stroke",
                               value=self.getLib(f, self.LIB_STROKE, True),
                               callback=self.strokeCallback, sizeStyle="small")

        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 1, 1, .8)

        self.w.color = ColorWell(((middle-5)*1.7, y-33, -10, 60),
                                 color=color,
                                 callback=self.colorCallback)

        self.w.preserveComponents = CheckBox((10, -25, -10, 22), "Preserve Components", sizeStyle="small",
                                value=self.getLib(f, self.LIB_PRESERVE_COMPONENTS, self.DEFAULT_PRESERVE_COMPONENTS),
                                callback=self.parametersTextChanged)

        self.previewCallback(self.w.preview)

        return y

    def parametersChanged(self, sender=None, g=None):
        c = self.getController()
        g = CurrentGlyph()
        if g is None:
            return
        f = g.font
        thickness = int(c.w.thickness.get())
        self.setLib(f, self.LIB_THICKNESS, thickness)
        contrast = int(c.w.contrast.get())
        self.setLib(f, self.LIB_CONTRAST, contrast)
        contrastAngle = int(c.w.contrastAngle.get())
        self.setLib(f, self.LIB_CONTRAST_ANGLE, contrastAngle)
        keepBounds = c.w.keepBounds.get()
        self.setLib(f, self.LIB_KEEP_BOUNDS, keepBounds)
        preserveComponents = bool(c.w.preserveComponents.get())
        self.setLib(f, self.LIB_PRESERVE_COMPONENTS, preserveComponents)

        miterLimit = int(c.w.miterLimit.get())
        if c.w.connectmiterLimit.get():
            miterLimit = thickness
            c.w.miterLimit.set(miterLimit)
        self.setLib(f, self.LIB_CONNECT_MITER_LIMIT, c.w.connectmiterLimit)
        self.setLib(f, self.LIB_MITER_LIMIT, miterLimit)

        corner = c.w.corner.getItems()[c.w.corner.get()]
        self.setLib(f, self.LIB_CORNER, corner )

        closeOpenPath = c.w.useCap.get()
        self.setLib(f, self.LIB_CLOSE_OPEN_PATH, closeOpenPath)

        cap = c.w.cap.getItems()[c.w.cap.get()]
        self.setLib(f, self.LIB_CAP, cap )

        drawOriginal = c.w.drawOriginal.get()
        self.setLib(f, self.LIB_DRAW_ORIGINAL, drawOriginal)

        drawInner = c.w.drawInner.get()
        self.setLib(f, self.LIB_DRAW_INNER, drawInner)

        drawOuter = c.w.drawOuter.get()
        self.setLib(f, self.LIB_DRAW_OUTER, drawOuter)
        
        c.w.thicknessText.set("%i" % thickness)
        c.w.contrastText.set("%i" % contrast)
        c.w.contrastAngleText.set("%i" % contrastAngle)
        c.w.miterLimitText.set("%i" % miterLimit)

        g.getLayer('background').changed() # Make sure to update from the background

    def parametersTextChanged(self, sender):
        c = self.getController()
        value = sender.get()
        try:
            value = int(float(value))
        except ValueError:
            value = 10
            sender.set(value)

        thickness = int(c.w.thicknessText.get())
        c.w.thickness.set(thickness)
        contrast = int(c.w.contrastText.get())
        c.w.contrast.set(contrast)
        contrastAngle = int(c.w.contrastAngleText.get())
        c.w.contrastAngle.set(contrastAngle)
        c.parametersChanged(sender)

    def contrastAngleCallback(self, sender):
        if NSEvent.modifierFlags() & NSShiftKeyMask:
            value = sender.get()
            value = roundValue(value, 45)
            sender.set(value)
        self.parametersChanged(sender)

    def pointPenChanged(self, sender):
        c = self.getController()
        changed = False
        value = int(round(sender.get()))
        c.w.pointPenText.set(value)
        g = CurrentGlyph()
        if g is not None:
            for contour in g:
                for p in contour.points:
                    if p.selected:
                        if value == 100:
                            p.labels = [] # On default, clear label
                        else:
                            p.labels = ['F%d' % value]
                        changed = True
        if changed:
            self.updateView()
        
    def pointPenTextChanged(self, sender):
        c = self.getController()
        changed = False
        try:
            value = int(sender.get())
            c.w.pointPen.set(value)
            g = CurrentGlyph()
            if g is not None:
                for contour in g:
                    for p in contour.points:
                        if p.selected:
                            p.labels = ['F%d' % value]
                            changed = True
        except ValueError:
            pass
        if changed:
            self.updateView()

    def setPointPenByValue(self, sender):
        c = self.getController()
        c.w.pointPen.set(sender.value)
        c.w.pointPenText.set(sender.value)
        g = CurrentGlyph()
        if g is not None:
            for contour in g:
                for p in contour.points:
                    if p.selected:
                        if sender.value == 100:
                            p.labels = []
                        else:
                            p.labels = ['F%d' % sender.value]
                        changed = True
        self.updateView()

    def setRightMarginByValue(self, sender):
        g = CurrentGlyph()
        if g is not None:
            g.angledRightMargin = sender.value

    def connectmiterLimit(self, sender):
        c = self.getController()
        f = CurrentFont()
        self.setLib(f, self.LIB_CONNECT_MITER_LIMIT, sender.get())
        value = not sender.get()
        c.w.miterLimit.enable(value)
        c.w.miterLimitText.enable(value)
        self.parametersChanged(sender)

    def useCapCallback(self, sender):
        c = self.getController()
        f = CurrentFont()
        value = sender.get()
        self.setLib(f, self.LIB_CLOSE_OPEN_PATH, value)
        c.w.cap.enable(value)
        self.parametersChanged(sender)

    def previewCallback(self, sender):
        c = self.getController()
        f = CurrentFont()
        value = sender.get()
        c.w.fill.enable(value)
        c.w.stroke.enable(value)
        c.w.color.enable(value)
        self.setLib(f, self.LIB_CLOSE_OPEN_PATH, value)
        self.updateView()

    def fillCallback(self, sender):
        f = CurrentFont()
        self.setLib(f, self.LIB_FILL, sender.get()),
        self.updateView()

    def strokeCallback(self, sender):
        f = CurrentFont()
        self.setLib(f, self.LIB_STROKE, sender.get()),
        self.updateView()

    def colorCallback(self, sender):
        f = CurrentFont()
        self.setLib(f, self.LIB_COLOR, sender.get())
        self.updateView()

    def updateView(self, sender=None):
        UpdateCurrentGlyphView()

