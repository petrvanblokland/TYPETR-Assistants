# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    outlineinformationfactory.py
#
import math

from fontTools.ufoLib.pointPen import AbstractPointPen

#from defcon.pens.clockwiseTestPointPen import ClockwiseTestPointPen

# ----------
# point data
# ----------

class OutlineInformationPen(AbstractPointPen):
    """
    Pen for drawing glyph outline points.
    """

    def __init__(self, glyphSet):
        """
        """
        self.glyphSet = glyphSet
        self._rawPointData = []
        self._rawComponentData = []
        self._bezierHandleData = []

    def getData(self):
        """
        """
        data = dict(startPoints=[],
            onCurvePoints=[],
            offCurvePoints=[],
            bezierHandles=[],
            anchors=[],
            labels=[],
            components=self._rawComponentData,
            rawData=self._rawPointData)

        for contour in self._rawPointData:
            # anchor (an anchor must have a name)
            contourLength = len(contour)
            if contourLength == 1:
                anchor = contour[0]
                if anchor["name"]:
                    data["anchors"].append(anchor)
                    continue
            # points
            # clocwisePen = ClockwiseTestPointPen()
            # for point in contour:
            #     clocwisePen.addPoint(point["point"], segmentType=point["segmentType"])
            # clockwise = clocwisePen.getIsClockwise()
            clockwise = False

            haveFirst = False
            for pointIndex, point in enumerate(contour):
                if point["segmentType"] is None:
                    data["offCurvePoints"].append(point)
                    # look for handles
                    back = contour[pointIndex - 1]

                    forward = contour[(pointIndex + 1) % contourLength]
                    if back["segmentType"] in ("qcurve", "curve", "line", "move", "tangent"):
                        p1 = back["point"]
                        p2 = point["point"]
                        if p1 != p2:
                            data["bezierHandles"].append((p1, p2))

                    elif forward["segmentType"] in ("qcurve", "curve", "line", "move", "tangent"):
                        p1 = forward["point"]
                        p2 = point["point"]
                        if p1 != p2:
                            data["bezierHandles"].append((p1, p2))
                else:

                    # atch first point.
                    if not haveFirst:
                        haveFirst = True
                        nextOn = None
                        for nextPoint in contour[pointIndex:] + contour[:pointIndex]:
                            #if nextPoint["segmentType"] is None:
                            #    continue
                            if nextPoint["point"] == point["point"]:
                                continue
                            nextOn = nextPoint
                            break
                        angle = None
                        if nextOn:
                            x1, y1 = point["point"]
                            x2, y2 = nextOn["point"]
                            xDiff = x2 - x1
                            yDiff = y2 - y1
                            angle = round(math.atan2(yDiff, xDiff) * 180 / math.pi, 3)

                        #data["startPoints"].append((point["point"], angle, point["segmentType"] == "move", clockwise))
                        data["startPoints"].append((point["point"], angle, point["segmentType"] == "move"))#, clockwise))

                    nextPoint = contour[(pointIndex+1) % contourLength]
                    prevPoint = contour[pointIndex - 1]

                    if nextPoint["segmentType"] is None and prevPoint["segmentType"] is not None:
                        point["segmentType"] = "tangent"

                    elif nextPoint["segmentType"] is not None and prevPoint["segmentType"] is None:
                        point["segmentType"] = "tangent"

                    data["onCurvePoints"].append(point)

                    '''
                    if nextPoint["segmentType"] == None:
                        point["segmentType"] = "curve" # @@@ We have to solve this to know if qcurve


                    if point["smooth"]:
                        x1, y1 = contour[pointIndex - 1 ]["point"]
                        x2, y2 = point["point"]
                        xDiff = x2 - x1
                        yDiff = y2 - y1
                        angle = round(math.atan2(yDiff, xDiff) * 180 / math.pi, 3)
                        point["smoothAngle"] = angle
                    '''

                if point["name"] is not None:
                    data["labels"].append((point["point"], point["name"]))
        return data

    def beginPath(self):
        self._rawPointData.append([])

    def endPath(self):
        pass

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        d = dict(point=pt, segmentType=segmentType, smooth=smooth, name=name)
        self._rawPointData[-1].append(d)

    def addComponent(self, baseGlyphName, transformation):
        """
        TODO: to be completed.
        """
        NSLog('add component %s' % baseGlyphName)

        '''
        firstPoint = None

        if self.glyphSet[baseGlyphName]:
            c = self.glyphSet[baseGlyphName][0]
            if c._points:
                firstPoint = c._points[0]

        d = dict(baseGlyphName=baseGlyphName, transformation=transformation, firstPoint=(firstPoint.x, firstPoint.y))
        '''

        self._rawComponentData.append((baseGlyphName, transformation))


def OutlineInformationFactory(glyph, font):
    """
    Gets a pen and draws the glyph points with it.
    """
    pen = OutlineInformationPen(font)
    glyph.drawPoints(pen)
    return pen.getData()
