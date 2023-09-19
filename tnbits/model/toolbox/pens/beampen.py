# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     beampen.py
#
from fontTools.pens.basePen import BasePen
from fontTools.pens.cocoaPen import CocoaPen
from fontTools.misc.bezierTools import splitLine, splitCubic

try:
    from lib.tools import bezierTools
except:
    bezierTools = None  # delay error so more things can work outside of RF

class ZZBeamPen(BasePen):

    def __init__(self, glyphSet, glyph, beam, canHaveComponent=True, italicAngle=0):
        BasePen.__init__(self, glyphSet)
        self._glyph = glyph
        self._canHaveComponent = canHaveComponent
        self._italicAngle = italicAngle

class BeamPen(BasePen):
    def __init__(self, glyphSet, glyph, beam, canHaveComponent=True, italicAngle=0):
        BasePen.__init__(self, glyphSet)
        self._glyph = glyph
        self._canHaveComponent = canHaveComponent
        self._italicAngle = italicAngle

        self.beamStart, self.beamEnd = beam

        self.firstPoint = None
        self.intersects = []
        self.intersectsX = []
        self.intersectsY = []
        self.sliceData = []

        self._contourIndex = -1
        self._segmentIndex = -1

        self._leftMarginIntersects = []
        self._rightMarginIntersects = []
        self._fontMetricsIntersects = []

    def _convertPoint(self, p):
        x = bezierTools.roundFloat(p.x, 100.)
        y = bezierTools.roundFloat(p.y, 100.)
        return x, y

    def addPoint(self, p, t):
        self._addPoint(bezierTools.SimplePoint(p), t)

    def _addPoint(self, p, t):
        x, y = self._convertPoint(p)
        self.intersects.append((x, y))
        self.intersectsX.append(x)
        self.intersectsY.append(y)

        self.sliceData.append(dict(contourIndex=self._contourIndex,
                                        segmentIndex=self._segmentIndex,
                                        t=t,
                                        x=x,
                                        y=y,
                                        point=p))

    def addIntersection(self, r):
        if r.status == "Intersection":
            for index, p in enumerate(r.points):
                self._addPoint(p, r.t[index])


    marginMax = 10000

    def _get_rightMarginIntersection(self):
        if self._rightMarginIntersects:
            return self._rightMarginIntersects

        w = self._glyph.width

        bottom = bezierTools.angledPoint((w, -self.marginMax), self._italicAngle)
        top = bezierTools.angledPoint(((w, self.marginMax)), self._italicAngle)
        r = bezierTools.intersectLineLine(bottom, top, self.beamStart, self.beamEnd)
        if r.status == "Intersection":
            for p in r.points:
                self._rightMarginIntersects.append(self._convertPoint(p))

        return self._rightMarginIntersects

    rightMarginIntersection = property(_get_rightMarginIntersection)

    def _get_lefMarginIntersection(self):
        self._leftMarginIntersects = []

        left = self._glyph.UILeftMargin

        bottom = bezierTools.angledPoint((left, -self.marginMax), self._italicAngle)
        top = bezierTools.angledPoint(((left, self.marginMax)), self._italicAngle)

        r = bezierTools.intersectLineLine(bottom, top, self.beamStart, self.beamEnd)
        if r.status == "Intersection":
            for p in r.points:
                self._leftMarginIntersects.append(self._convertPoint(p))

        return self._leftMarginIntersects

    lefMarginIntersection = property(_get_lefMarginIntersection)

    def _get_fontMetricsIntersections(self):
        if self._fontMetricsIntersects:
            return self._fontMetricsIntersects

        self._fontMetricsIntersects = []
        font = self._glyph.font
        if font is not None:

            baseLine = 0
            xHeight = font.info.xHeight
            capHeight = font.info.capHeight
            ascender = font.info.ascender
            descender = font.info.descender

            for value in [baseLine, xHeight, capHeight, ascender, descender]:
                r = bezierTools.intersectLineLine((-self.marginMax, value), (self.marginMax, value), self.beamStart, self.beamEnd)
                if r.status == "Intersection":
                    for p in r.points:
                        self._fontMetricsIntersects.append(self._convertPoint(p))

        return self._fontMetricsIntersects

    fontMetricsIntersections = property(_get_fontMetricsIntersections)

    def _moveTo(self, point):
        self._contourIndex += 1
        self._segmentIndex = -1
        self.firstPoint = point

    def _lineTo(self, point):
        self._segmentIndex += 1

        if self._getCurrentPoint() in [self.beamStart, self.beamEnd]:
            self.addPoint(self._getCurrentPoint(), 0)
        if point in [self.beamStart, self.beamEnd]:
            self.addPoint(point, 1)

        l = bezierTools.intersectLineLine(self._getCurrentPoint(), point, self.beamStart, self.beamEnd)
        self.addIntersection(l)

    def _curveToOne(self, bcp1, bcp2, point):
        self._segmentIndex += 1

        if self._getCurrentPoint() in [self.beamStart, self.beamEnd]:
            self.addPoint(self._getCurrentPoint(), 0)
        if point in [self.beamStart, self.beamEnd]:
            self.addPoint(point, 1)

        if bezierTools.isPointOnLine(self._getCurrentPoint(), (self.beamStart, self.beamEnd)):
            self.addPoint(self._getCurrentPoint(), 0)
        if bezierTools.isPointOnLine(point, (self.beamStart, self.beamEnd)):
            self.addPoint(point, 1)

        l = bezierTools.intersectCubicLine(self._getCurrentPoint(), bcp1, bcp2, point, self.beamStart, self.beamEnd)
        self.addIntersection(l)

    def qCurveTo(self, *points):
        ### this should always have a length of 3!!! so basically this is the same as 2 beziers
        if len(points) != 3:
            raise RoboFontError("Should have 3 points!!")

        points = bezierTools.curveConverter.convertSegment(self._getCurrentPoint(), points, "curve")
        self.curveTo(*points)

    def _closePath(self):
        if self.firstPoint is not self. _getCurrentPoint():
            self._lineTo(self.firstPoint)
        self.firstPoint = None

    def addComponent(self, *args, **kwargs):
        if self._canHaveComponent:
            BasePen.addComponent(self,  *args, **kwargs)

    def sliceGlyph(self, roundValue=False):
        if not self.sliceData:
            return

        self._glyph.disableNotifications()
        self._glyph.selection.resetSelection()

        oldPointData = set()
        for contour in self._glyph:
            for point in contour:
                oldPointData.add((point.x, point.y))

        slicedContours = dict()

        for value in self.sliceData:
            ci = value.get("contourIndex")
            si = value.get("segmentIndex")
            point = value.get("point")
            t = value.get("t")
            contour = self._glyph[ci]

            if contour not in slicedContours:
                slicedContours[contour] = dict()

            if si not in slicedContours[contour]:
                slicedContours[contour][si] = list()

            slicedContours[contour][si].append(point)

        _contourIntersetionPoints = dict()

        hasOpenContours = False
        for contour, segments in slicedContours.items():
            if contour.open:
                hasOpenContours = True
            _points = set(contour.onCurvePoints)

            for segmentIndex in sorted(segments.keys(), reverse=True):
                points = segments[segmentIndex]
                ts = list()
                for point in points:
                    t = contour.insertPointAtPointInSegment(point, segmentIndex, roundValue, doSplit=False)
                    if t is not None:
                        ts.append(t)

                for t in sorted(ts, reverse=True):
                    if contour[0].segmentType == "move":
                        segmentIndex += 1
                    contour.splitAndInsertPointAtSegmentAndT(segmentIndex, t)


            if roundValue:
                for p in contour._points:
                    p.x = round(p.x)
                    p.y = round(p.y)
                #self.dirty = True

            ip = set(contour.onCurvePoints) - _points
            _contourIntersetionPoints[contour] = ip

        if not hasOpenContours and len(self.intersects) == 2 and len(_contourIntersetionPoints) <= 2:
            pen = CocoaPen(self._glyph.font)
            for contour in slicedContours:
                contour.draw(pen)

            if not (pen.path.containsPoint_(self.beamStart) or pen.path.containsPoint_(self.beamEnd)):
                for contour, intersectionPoints in _contourIntersetionPoints.items():
                    for p in intersectionPoints:
                        p.smooth = False

                newContours = []
                if len(_contourIntersetionPoints) == 1:
                    for contour, intersectionPoints in _contourIntersetionPoints.items():
                        points = sorted(intersectionPoints, cmp=lambda p1, p2: cmp((p1.x, p1.y), (p2.x, p2.y)))
                        ranges = list()

                        ip1 = points[0]
                        ip2 = points[1]

                        index1 = contour._points.index(ip1)
                        index2 = contour._points.index(ip2)

                        if index1 < index2:
                            oi = index1
                            index1 = index2
                            index2 = oi

                            op = ip1
                            ip1 = ip2
                            ip2 = op

                        newContours.append(contour._points[index2:index1] + [ip1])
                        newContours[-1][0] = self._glyph.pointClass((newContours[-1][0].x, newContours[-1][0].y), "line")

                        newContours.append(contour._points[:index2] + [ip2] + contour._points[index1:])
                        newContours[-1][index2+1] = self._glyph.pointClass((newContours[-1][index2+1].x, newContours[-1][index2+1].y), "line")

                elif len(_contourIntersetionPoints) == 2:
                    contour1 = _contourIntersetionPoints.keys()[0]
                    contour2 = _contourIntersetionPoints.keys()[1]
                    if bezierTools.boundsInBounds(contour1.bounds, contour2.bounds) or bezierTools.boundsInBounds(contour2.bounds, contour1.bounds):

                        newContours.append([])
                        for contour, intersectionPoints in _contourIntersetionPoints.items():
                            intersectionPoints = list(intersectionPoints)
                            intersectionPoint = intersectionPoints[0]
                            index = contour._points.index(intersectionPoint)
                            nw = contour._points[index:] + contour._points[:index] + [intersectionPoint]
                            nw[0] = self._glyph.pointClass((nw[0].x, nw[0].y), "line")

                            newContours[-1] += nw

                if newContours:
                    for contour in slicedContours:
                        self._glyph.removeContour(contour)


                    for c in newContours:
                        contour = self._glyph.contourClass(self._glyph.pointClass)
                        self._glyph.appendContour(contour)

                        contour._points = [self._glyph.pointClass((p.x, p.y), segmentType=p.segmentType, smooth=p.smooth, name=p.name) for p in c]

                        contour._destroyBoundsCache()
                        contour._clockwiseCache = None


        for contour in self._glyph:
            for point in contour:
                if not point.segmentType:
                    continue
                if (point.x, point.y) not in oldPointData:
                    self._glyph.selection.addPoint(point, contour=contour)

        self._glyph.enableNotifications()
        self._glyph._destroyBoundsCache()
        self._glyph.dirty = True
