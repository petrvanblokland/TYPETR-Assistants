# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     bezierpoint.py
#

class BezierPoint(object):
    """
    A Decorator around a Bézier point triple that takes a single DefCon point.
    Derived from RobofabWrapperBPoint in RoboFont, minus the GUI functions.
    """

    def __init__(self, obj=None, contour=None):
        if obj is not None:
            self._anchor = obj

        self._contour = contour

    def getParent(self):
        """
        Returns the contour contour.
        """
        return self._contour

    def __del__(self):
        del self._anchor

    def getIndex(self):
        c = self.getParent()
        index = c.index(self._anchor)
        return index

    def _getNextPoint(self):
        c = self.getParent()
        index = c.index(self._anchor)
        return c[(index + 1) % len(c)]

    def _getPrevPoint(self):
        c = self.getParent()
        index = c.index(self._anchor)
        return c[index - 1]

    def _caculateSmoothness(self):
        previousPoint = self._getPrevPoint()
        nextPoint = self._getNextPoint()

        if previousPoint.segmentType is not None and nextPoint.segmentType is not None:
            # all line segments
            self._anchor.smooth = False
        else:
            error = 1
            angle1 = bezierTools.calculateAngle((self._anchor.x,
                self._anchor.y), (previousPoint.x, previousPoint.y))
            angle2 = bezierTools.calculateAngle((nextPoint.x, nextPoint.y),
                    (self._anchor.x, self._anchor.y))
            # calculate error based on the length of the bcp...
            self._anchor.smooth = abs(angle1 - angle2) < error

    def _get_anchor(self):
        return self._anchor.x, self._anchor.y

    def _set_anchor(self, t):
        x, y = t
        self._anchor.x = x
        self._anchor.y = y

    anchor = property(_get_anchor, _set_anchor, doc="The anchor point of the bPoint.")

    def _get_bcpIn(self):
        prevPoint = self._getPrevPoint()
        contourIsOpen = self._anchor.segmentType == "move"

        if not contourIsOpen and prevPoint.segmentType is None:
            return prevPoint.x - self._anchor.x, prevPoint.y - self._anchor.y

        return (0, 0)

    def _set_bcpIn(self, t):
        x, y = t
        if self._anchor.segmentType == "move":
            raise RoboFontError("Cannot add bpc in to the first point in a contour")

        prevPoint = self._getPrevPoint()

        if prevPoint.segmentType is not None:
            contour = self.getParent()
            onCurvePoints = contour.onCurvePoints
            onCurveIndex = onCurvePoints.index(self._anchor)
            prevOnCurvePoint = onCurvePoints[onCurveIndex - 1]
            index = contour.index(self._anchor)
            p1 = contour._pointClass((prevOnCurvePoint.x, prevOnCurvePoint.y))
            p2 = contour._pointClass((self._anchor.x, self._anchor.y))
            contour._points.insert(index, p2)
            contour._points.insert(index, p1)
            self._anchor.segmentType = "curve"
            prevPoint = p2

        prevPoint.x = x + self._anchor.x
        prevPoint.y = y + self._anchor.y
        self._caculateSmoothness()

    bcpIn = property(_get_bcpIn, _set_bcpIn, doc="The in coming bcp of the bPoint.")

    def _get_bcpOut(self):
        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is None:
            return nextPoint.x - self._anchor.x, nextPoint.y - self._anchor.y

        return (0, 0)

    def _set_bcpOut(self, t):
        x, y = t
        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is not None:
            contour = self.getParent()
            onCurvePoints = contour.onCurvePoints
            onCurveIndex = onCurvePoints.index(self._anchor)
            nextOnCurvePoint = onCurvePoints[(onCurveIndex + 1) % len(onCurvePoints)]
            index = contour.index(nextOnCurvePoint)
            p1 = contour._pointClass((self._anchor.x, self._anchor.y))
            p2 = contour._pointClass((nextOnCurvePoint.x, nextOnCurvePoint.y))
            contour._points.insert(index, p2)
            contour._points.insert(index, p1)
            nextOnCurvePoint.segmentType = "curve"
            nextPoint = p1

        nextPoint.x = x + self._anchor.x
        nextPoint.y = y + self._anchor.y
        self._caculateSmoothness()

    bcpOut = property(_get_bcpOut, _set_bcpOut, doc="The in outgoing bcp of the bPoint.")

    # labels

    def _get_anchorLabels(self):
        return self._anchor.labels

    def _set_anchorLabels(self, value):
        setLabelForDefconPoint(self._anchor, value)

    anchorLabels = property(_get_anchorLabels, _set_anchorLabels, doc="Labels for the anchor point.")

    # names

    def _get_anchorName(self):
        return self._anchor.name

    def _set_anchorName(self, value):
        self._anchor.name = value

    anchorName = property(_get_anchorName, _set_anchorName, doc="Name for the anchor point.")

    def _get_bcpInName(self):
        prevPoint = self._getPrevPoint()

        if prevPoint.segmentType is None:
            return prevPoint.name

        return ""

    def _set_bcpInName(self, value):
        prevPoint = self._getPrevPoint()

        if prevPoint.segmentType is None:
            prevPoint.name = value

    bcpInName = property(_get_bcpInName, _set_bcpInName, doc="Name for the in coming bcp point.")

    def _get_bcpOutName(self):
        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is None:
            return nextPoint.name

        return ""

    def _set_bcpOutName(self, value):
        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is None:
            nextPoint.name = value

    bcpOutName = property(_get_bcpOutName, _set_bcpOutName, doc="Name for the out going bcp point.")

    def round(self):
        """
        Round the bPoint.
        """
        self._anchor.x, self._anchor.y = roundPt((self._anchor.x, self._anchor.y))
        prevPoint = self._getPrevPoint()

        if prevPoint.segmentType is None:
            prevPoint.x, prevPoint.y = roundPt((prevPoint.x, prevPoint.y))

        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is None:
            nextPoint.x, nextPoint.y = roundPt((nextPoint.x, nextPoint.y))

    def move(self, t):
        """
        Move the bPoint by (x, y)
        """
        x, y = t
        self._anchor.move((x, y))
        prevPoint = self._getPrevPoint()

        if prevPoint.segmentType is None:
            prevPoint.move((x, y))

        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is None:
            nextPoint.move((x, y))

    def _get_segmentType(self):
        t = "corner"
        bcpIn = self.bcpIn

        if bcpIn == (0, 0):
            return t

        bcpOut = self.bcpOut

        if bcpOut == (0, 0):
            return t

        if self._anchor.segmentType and self._anchor.smooth:
            t = "curve"

        return t

    def _set_segmentType(self, pointType):
        raise NotImplementedError

    segmentType = property(_get_segmentType, _set_segmentType, doc="curve type of the bPoint")

    type = segmentType

    def transform(self, matrix):
        """
        Transform the bPoint by a transform matrix.
        """
        self._anchor.x, self._anchor.y = matrix.transformPoint((self._anchor.x, self._anchor.y))
        prevPoint = self._getPrevPoint()

        if prevPoint.segmentType is None:
            prevPoint.x, prevPoint.y = matrix.transformPoint((prevPoint.x, prevPoint.y))

        nextPoint = self._getNextPoint()

        if nextPoint.segmentType is None:
            nextPoint.x, nextPoint.y = matrix.transformPoint((nextPoint.x, nextPoint.y))

    def scale(self, factor, center=(0, 0)):
        """
        Scale the bPoint by an (x, y) a round an optionally center point (x, y).
        """
        if isinstance(factor, tuple):
            x, y = factor
        else:
            x = y = factor

        rT = Identity.translate(center[0], center[1])
        rT = rT.scale(x, y)
        rT = rT.translate(-center[0], -center[1])
        self.transform(rT)
