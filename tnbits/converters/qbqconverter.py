# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    qbqconverter.py
#

from tnbits.constants import Constants as C
from tnbits.objects.point import Point, SpacePoint
from tnbits.toolbox.transformer import TX
from tnbits.model.objects.glyph import getContours

DEBUG = False

class QBQConverter(object):
    """
    Quadratic <-> Bézier conversion.
    """

    FACTOR = 1.340   # This estimated value gives amazingly accurate conversion.
    FACTORS = {
        C.POINTTYPE_QUADRATIC:     1.0/FACTOR,
        C.POINTTYPE_BEZIER:     FACTOR
    }

    @classmethod
    def factorizeOffCurve(cls, onCurve, offCurve, factor, scale=1):
        dx = offCurve.x - onCurve.x
        dy = offCurve.y - onCurve.y
        offCurve.x = int(round((onCurve.x + dx * factor) * scale))
        offCurve.y = int(round((onCurve.y + dy * factor) * scale))
        if scale != 1:
            onCurve.x = int(round(onCurve.x * scale))
            onCurve.y = int(round(onCurve.y * scale))

    @classmethod
    def b2q(cls, x1, y1, x2, y2):
        return x1 + (x2 - x1)/cls.FACTOR, y1 + (y2 - y1)/cls.FACTOR

    @classmethod
    def q2b(cls, x1, y1, x2, y2):
        return x1 + (x2 - x1)*cls.FACTOR, y1 + (y2 - y1)*cls.FACTOR

    @classmethod
    def singleq2b(cls, x1, y1, x2, y2):
        return x1 + (x2 - x1)/2, y1 + (y2 - y1)/2

    @classmethod
    def factorizeSegment(cls, position, segment, fromType, toType, scale=1):
        if segment[-1].segmentType == fromType:
            f = cls.FACTORS[toType]
            if len(segment) == 2:
                # One BCP missing, interpret bcp connected to first point
                cls.factorizeOffCurve(position, segment[0], f, scale)

            elif len(segment) == 3:
                # 2 offCurve's defined. Move them
                cls.factorizeOffCurve(position, segment[0], f)
                cls.factorizeOffCurve(segment[2], segment[1], f, scale)
            segment[-1].segmentType = toType

    @classmethod
    def factorize(cls, glyph, fromType, toType, scale=1):
        u"""Factorize the length of the segment off-curves to the toType format."""
        for contour in getContours(glyph):
            segments = contour.segments
            position = segments[-1][-1] # Position of segment start
            for segment in contour.segments:
                cls.factorizeSegment(position, segment, fromType, toType, scale)
                position = segment[-1] # Set to start position of next segment

    @classmethod
    def bezier2Quadratic(cls, glyph, scale=1):
        cls.factorize(glyph, C.POINTTYPE_BEZIER, C.POINTTYPE_QUADRATIC, scale)

    @classmethod
    def quadratic2Bezier(cls, glyph, scale=1):
        cls.factorize(glyph, C.POINTTYPE_QUADRATIC, C.POINTTYPE_BEZIER, scale)

    @classmethod
    def getQuadratic2FBHintPoints(cls, glyph):
        """
        The `getQuadratic2FBHintPoints` method converts the glyph
        points into a point list. The original RoboFont points are enveloped by
        a `RfPoint` to give more freedom to add other information
        and also to become independent to changes in API of the RF points.<br/>

        Also add 4 phantom points at the end to indicate the margins and
        descender/ascender as used by the hinting programs as instances of
        FBHint points.<br/> Since the API of all point types is equal,
        application using this list don't have to know the difference.
        """
        if glyph is None:
            return []
        if DEBUG: print('[QBQConverter.getQuadratic2FBHintPoints]', glyph.name)

        if hasattr(glyph, '_object'):
            glyph = glyph._object
        font = glyph.font
        if cls.isBezier(glyph):
            cls.bezier2Quadratic(glyph)

        """
        for index, contour in enumerate(glyph._contours):
            # Freetype does not like it when the start point is not on-curve.
            # Shift the start point of the contour until the start point it on-curve
            # Since there is max 2 off-curves in a row, we only need to try twice
            if contour:
                if contour[0].segmentType is None:
                    contour = contour[1:] + [contour[0]]
                if contour[0].segmentType is None:
                    contour = contour[1:] + [contour[0]]
                assert contour[0].segmentType is not None
                glyph._contours[index] = contour
        """
        points = [] # FBHint Zone()
        index = 0 # In case there are no points, space point index starts at 0

        for contour in glyph._contours:
            for contourIndex, p in enumerate(contour):
                hp = Point(p, id=TX.index2PointId(index), start=contourIndex==0)
                points.append(hp)
                index += 1

        # Phantom points for spacing, descender and ascender.
        spacePointIndex = len(points)
        points.append(SpacePoint(cls.getSpacedUniqueID(1), 0, 0, C.POINTTYPE_SPACE, None, spacePointIndex))
        points.append(SpacePoint(cls.getSpacedUniqueID(2), glyph.width, 0, C.POINTTYPE_SPACE, None, spacePointIndex+1))
        # For MS Rasterizer 1.7 and higher
        points.append(SpacePoint(cls.getSpacedUniqueID(3), 0, font.info.ascender, C.POINTTYPE_SPACE, None, spacePointIndex+2))
        points.append(SpacePoint(cls.getSpacedUniqueID(4), 0, font.info.descender, C.POINTTYPE_SPACE, None, spacePointIndex+3))

        return points

    @classmethod
    def getSpacedUniqueID(cls, offset):
        return '*%s' % (C.UNIQUEID_SPACE+offset)

    @classmethod
    def getFBHintPoints2Glyph(cls, points, glyph):
        """
        Get the (modified) coordinates from the FBHint Point list and mode the
        glyph points. Note that the glyph is in the lead, so we don't need to
        skip the extra 2 (or 4?) spacing points at the end of the list. Then
        the phantom points are used to adjust the hinted spacing.
        """
        if hasattr(glyph, '_object'):
            glyph = glyph._object
        i = 0
        for contour in glyph._contours:
            for p in contour._points:
                fbhintpoint = points[i]
                p.x = fbhintpoint.x
                p.y = fbhintpoint.y
                p.selected = fbhintpoint.selected
                #p.name = p.name
                #p.label = point.label
                #p.script = point.script
                #p.comment = point.comment
                i += 1
        # 4 Phantom points for spacing.
        glyph.leftmargin = points[-4].x
        glyph.width = points[-3].x + 4 # Hack for now to cover up roundings
        # points[-2] defines ascender
        # points[-1] defines descender
        # Round ascender and descender
        #font.info.ascender = round(font.info.ascender / grid) * grid
        #font.info.descender = round((font.info.ascender - em) / grid) * grid

    @classmethod
    def isQuadratic(cls, glyph):
        #return bool(glyph.preferedSegmentType == C.POINTTYPE_QUADRATIC)
        #return glyph.hasSplinesCurves
        for contour in (glyph or []):
            for segment in contour.segments:
                for point in segment:
                    if segment[-1].type == C.POINTTYPE_QUADRATIC:
                        return True
        return False

    @classmethod
    def isBezier(cls, glyph):
        #return bool(glyph.preferedSegmentType == C.POINTTYPE_BEZIER)
        #return glyph.hasBezierCurves
        for contour in (glyph or []):
            for segment in contour.segments:
                for point in segment:
                    if segment[-1].type == C.POINTTYPE_BEZIER:
                        return True
        return False

    @classmethod
    def toggle(cls, glyph):
        if cls.isBezier(glyph):
            cls.bezier2Quadratic(glyph)
        elif cls.isQuadratic(glyph):
            cls.quadratic2Bezier(glyph)

    @classmethod
    def isRounded(cls, glyph):
        for contour in (glyph or []):
            for segment in contour:
                for p in segment:
                    if p.x != round(p.x) or p.y != round(p.y):
                        return False
        return True
