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
#    draw.py
#

class Draw(object):

    def drawFreetypePoints(self, fc, pen):
        outline = fc.getOutline()
        start, end = 0, 0

        # Splits up contours.
        for i in range(len(outline.contours)):
            # For each contour, get a circular points list.
            end = outline.contours[i]
            points = outline.points[start:end+1]
            points.append(points[0])

            # Tags?
            tags = outline.tags[start:end+1]
            tags.append(tags[0])

            # Splits up segments.
            segments = [[points[0],],]

            # Compiles segments.
            for j in range(1, len(points) ):
                segments[-1].append(points[j])

                if tags[j] & (1 << 0) and j < (len(points)-1):
                    segments.append([points[j],])

            # Walks through segments.
            pen.moveTo(segments[0][0])

            for segment in segments:
                self.drawSegment(segment, pen)

            pen.closePath()

            start = end + 1

    def drawSegment(self, segment, pen):
        """
        Passes each segment to the pen. After the last segment pen.closePath()
        should be called to flush the contour (i.e. actually draw it).
        """
        if len(segment) == 2:
            pen.lineTo(segment[-1])
        elif len(segment) == 3:
            pen.curveTo(segment[0], segment[1], segment[2])
        else:
            pen.qCurveTo(*segment)
