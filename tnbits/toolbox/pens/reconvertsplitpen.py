# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from fontTools.ufoLib.pointPen import AbstractPointPen, SegmentToPointPen

try:
    from lib.tools.bezierTools import intersectRayRay
except:  # Remove in later RoboFont version, when this renaming has been done.
    from lib.tools.bezierTools import instersectRayRay
    intersectRayRay = instersectRayRay

from compositor import Font

class TestPen(AbstractPointPen):

    def __init__(self):
        self.data = []

    def beginPath(self):
        self.data.append("beginPath")

    def endPath(self):
        self.data.append("endpath")

    def addPoint(self, d, segmentType=None, smooth=False, name=None, **kwargs):
        x, y = d
        self.data.append("point: %s, %s segmentType: %s" % (x, y, segmentType))

    def addComponent(self, baseGlyphName, transformation):
        self.data.append("baseGlyph: %s transformation: %s" % (baseGlyphName, transformation))


class ReconvertSplinePointPen(AbstractPointPen):

    def __init__(self, outPointPen):
        self.outPointPen = outPointPen

    def beginPath(self):
        self.points = []

    def endPath(self):
        points = []

        for i, data in enumerate(self.points):
            if data["name"] and "inserted" in data["name"]:
                if data["segmentType"] is None:
                    # There are two situations to recognize.
                    # If the inserted point is an off-curve, then it originally came from
                    # on-off-on, so the we must use the neighbor off-curve to calculate the
                    # intersection and the take that as new off-curve.
                    # In the situation that the inserted point is an on-curve, it originally
                    # came from on-off-off-off-off-on (we hope, could there have been more
                    # off-curves in the sequence?). Then restore by ignoring the on-curve
                    # and changing the length of the off-curves.
                    prevOnCurvePoint = self.points[i - 1]
                    nextOffCurvePoint = self.points[(i + 1) % len(self.points)]
                    nextOnCurvePoint = self.points[(i + 2) % len(self.points)]

                    result = intersectRayRay(prevOnCurvePoint["pt"], data["pt"], nextOffCurvePoint["pt"], nextOnCurvePoint["pt"])
                    if result.points:
                        p = result.points[0]
                        nextOffCurvePoint["pt"] = int(round(p.x)), int(round(p.y))

                continue
            points.append(data)

        self.outPointPen.beginPath()
        for data in points:
            self.outPointPen.addPoint(data["pt"],
                                      data["segmentType"],
                                      data["smooth"],
                                      data["name"],
                                      **data["kwargs"])
        self.outPointPen.endPath()

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        data = dict(pt=pt, segmentType=segmentType, smooth=smooth, name=name, kwargs=kwargs)
        self.points.append(data)

    def addComponent(self, baseGlyphName, transformation):
        self.outPointPen.addComponent(baseGlyphName, transformation)

if __file__ == 'main':
    from mojo.roboFont import CurrentGlyph
    g = CurrentGlyph()
    print(g)
    testPen = TestPen()
    pen = ReconvertSplinePointPen(testPen)
    g.drawPoints(pen)
    source = Font(g.getParent().lib["com.typemytype.robofont.binarySource"])
    sourceG = source[g.name]
    sourceTestPen = TestPen()
    sourceG.draw(SegmentToPointPen(sourceTestPen))
    print(testPen.data == sourceTestPen.data)
    print("\n".join(testPen.data))
    print
    print("\n".join(sourceTestPen.data))
