# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   pointcollector.py
#
from fontTools.ufoLib.pointPen import AbstractPointPen

CURVETYPES = {"curve": "cubic", "qcurve": "quadratic"}
SEGMENTTYPES = {v: k for k, v in CURVETYPES.items()}  # the reverse of CURVETYPES


class PointCollector(AbstractPointPen):

    def __init__(self):
        self.currentContour = None
        self.curveType = None
        self.contours = []
        self.components = []
        self.anchors = []

    def beginPath(self, identifier=None, **kwargs):
        self.currentContour = {"isClosed": True}
        args = []
        if identifier is not None:
            self.currentContour["identifier"] = identifier
        self.currentContour.update(kwargs)
        self.currentContour["points"] = []
        self.contours.append(self.currentContour)

    def endPath(self):
        assert self.currentContour is not None
        self.currentContour = None

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
        assert self.currentContour is not None
        point = dict(x=pt[0], y=pt[1])
        if segmentType is not None:
            if segmentType in ("curve", "qcurve"):
                # XXX assert we're not mixing curve types
                self.curveType = CURVETYPES.get(segmentType, segmentType)
            elif segmentType == "move":
                self.currentContour["isClosed"] = False
            point["onCurve"] = True
        if smooth:
            point["smooth"] = smooth
        if name is not None:
            point["name"] = name
        if identifier is not None:
            point["identifier"] = identifier
        point.update(kwargs)
        self.currentContour["points"].append(point)

    def addComponent(self, baseGlyphName, transformation, identifier=None, **kwargs):
        """Add the componenet to self. The transformation is a tuple of (xScale, xyScale, yxScale, yScale,
        xOffset, yOffset)."""
        assert self.currentContour is None
        component = dict(baseGlyphName=baseGlyphName, transformation=tuple(transformation))

        if identifier is not None:
            component["identifier"] = identifier
        component.update(kwargs)
        self.components.append(component)

    def filterAnchors(self):
        """Filter the anchors from the contours. Anchors are defined as contours with one point,
        where the point has a defined name."""
        contours = []
        for contour in self.contours:
            points = contour["points"]
            if len(points) == 1 and points[0].get("name") is not None:
                self.anchors.append(points[0])
            else:
                contours.append(contour)
        self.contours = contours


# This is the reverse of the PointCollector
def drawPointsFromPack(glyphPack, pointPen):
    """Draw the contours and components from the pack onto a PointPen."""
    curveType = glyphPack["curveType"]
    segmentType = SEGMENTTYPES.get(curveType, "curve")
    for contour in glyphPack.get("contours", []):
        isClosed = contour["isClosed"]
        pointPen.beginPath()
        for point in contour["points"]:
            pt = point["x"], point["y"]
            if point.get("onCurve", False):
                segTp = segmentType
            else:
                segTp = None
            # addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs)
            pointPen.addPoint(pt, segmentType=segTp, smooth=point.get("smooth", False),
                    name=point.get("name"), identifier=point.get("identifier"))
        pointPen.endPath()
    for anchor in glyphPack.get("anchors", []):
        raise NotImplementedError
    for component in glyphPack.get("components", []):
        # addComponent(self, baseGlyphName, transformation)
        pointPen.addComponent(component["baseGlyphName"], component["transformation"])
               # Petr: No identifier attribute in the component: identifier=component.get("identifier"))
