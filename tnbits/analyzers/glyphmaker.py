# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     glyphmaker.py
#

import math
import weakref

from lib.tools.extremePoints import extremePoints

from tnbits.constants import Constants
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.model.objects.glyph import getPointContexts
from tnbits.model.objects.style import nakedStyle

class GlyphMaker(object):
    """The GlyphMaker is capable of modifying glyph in an intelligent way, using information from
    the StyleAnalyzer and GlyphAnalyzer. Not all of these modification are 100% right, so the
    main usage of the scaler is in meme calls, where the result can be finalized by the designer.
    Since the modifications are incrementally destructive to the glyph outline, the original is copied
    into a layer first."""
    C = Constants

    def __init__(self, parent, name):
        """The GlyphScaler modifies the defcon glyph, using parameter from the GlyphAnalyzer and
        StyleAnalyzer."""
        self.parent = nakedStyle(parent)
        self.name = name

    def __repr__(self):
        glyph = self.glyph
        return '[%s of "%s"]' % (self.__class__.__name__, glyph.name)

    @classmethod
    def common(cls, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        returns intersection point if it exists. Otherwise (None, None) is answered.
        http://en.wikipedia.org/wiki/Line-line_intersection
        """
        d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if d != 0:
            m1 = (x1*y2-y1*x2)
            m2 = (x3*y4-y3*x4)
            return (m1*(x3-x4) - m2*(x1-x2)) / d, (m1*(y3-y4) - m2*(y1-y2)) / d
        return None, None

    # self.parent    Weakref to the parent (font) analyzer

    def _get_parent(self):
        return self._parent()
    def _set_parent(self, analyzer):
        # Set the weakref to the parent (font) analyzer
        self._parent = weakref.ref(analyzer)
    parent = property(_get_parent, _set_parent)

    # self.glyph
    def _get_glyph(self):
        style = self.parent
        if style is not None and self.name in style:
            return style[self.name]
        return None
    glyph = property(_get_glyph)

    def setStem(self, value):
        """Set the stem width to value and interpolated the untouched points accordingly."""
        if self.parent is None or not self.name in self.parent:
            return
        ga = analyzerManager.getGlyphAnalyzer(self.parent[self.name])
        print(ga, value)

    @classmethod
    def italicizedPoint(cls, x, y, angle):
        #math.tan(-angle*math.pi/180)*y, y
        return x - math.tan(math.radians(angle))*y, y

    @classmethod
    def italicize(cls, glyph, angle, adjustCurves=True):
        """Perform an intelligent italicize on the glyph. First, store the points that are round
        horizontal extremes. Then slant all points over the given angle. Calculate the curvePalet-ratio
        of all 4 offCurve in their horizontal/vertical directions. Move the round extremes in the
        direction of the new slanted direction of the extreme. The amount is a guess, hack depending
        on the angle value. Could be improved. Then adjust the position of the neighbor offCurves,
        by forcing the x value identical to the moved round onCurve point. Then adjust the 4 offCuves
        to the same original curvePalet-ratio.
        This method is a "reasonable" ok solution of italicizing, but it still needs a bit of manual
        adjustment. There is room for improvement.
        The transformation matrix of components is not touched (unlike an overall skew in RoboFont,
        because the baseGlyphs are already italicized."""
        # http://66.147.242.192/~operinan/2/2.3.4a/2.3.4.34.curves.htm

        # Magic number to compensate for the movement of the off-curve points.
        # Made for angle of 8°. Likely not working for other angles. Needs more intelligent calculation in the future.
        # Compensation is "ok", as starting point for italics to be adjusted manually.
        magicNumber = 0.94

        pointContexts = getPointContexts(glyph, 3)
        specialPCs = [] # (pc, rx1, ry1, rx2, ry2)
        # Check on the points that need special attention later. We need to do
        # that before italicizing, otherwise it is harder to detect verticals.
        if adjustCurves:
            for pc in pointContexts:
                # On vertical round extreme we need to compensate
                if pc[3].segmentType is not None \
                    and pc[2].segmentType is None and pc[1].segmentType is None \
                    and pc[4].segmentType is None and pc[5].segmentType is None \
                    and pc[3].smooth and pc[4].x == pc[3].x == pc[2].x:
                        # This is a curve extreme that needs special attention.
                        # Calculate the curvePalette ratios before the slanting and store them with the pc.
                        intersection1 = cls.common(pc[3].x, pc[3].y, pc[4].x, pc[4].y, pc[5].x, pc[5].y, pc[6].x, pc[6].y)
                        intersection2 = cls.common(pc[3].x, pc[3].y, pc[2].x, pc[2].y, pc[1].x, pc[1].y, pc[0].x, pc[0].y)
                        if not None in intersection1 and not None in intersection2:
                            # Calculate the ratio of distance between the onCurve->offCurve and onCurve->intersection
                            rx1 = float(pc[5].x - pc[6].x) / (intersection1[0] - pc[6].x)
                            ry1 = float(pc[4].y - pc[3].y) / (intersection1[1] - pc[3].y)
                            rx2 = float(pc[1].x - pc[0].x) / (intersection2[0] - pc[0].x)
                            ry2 = float(pc[2].y - pc[3].y) / (intersection2[1] - pc[3].y)
                            #rx1 = ry1 = rx2 = ry2 = 0
                            specialPCs.append((pc, rx1, ry1, rx2, ry2))

        # Now italicize all point positions.
        for pc in pointContexts:
            pc[3].x, _ = cls.italicizedPoint(pc[3].x, pc[3].y, angle)

        # Italicize the anchors
        for anchor in glyph.anchors:
            anchor.x, _ = cls.italicizedPoint(anchor.x, anchor.y, angle)

        # Insert extreme points in slanted curve
        #extremePoints(glyph, getContours(glyph), roundCoordinates=True)

        if adjustCurves:
            # Horizontal extreme curve points move, but also their neighbor off-curves. This makes the
            # extremes into slanted extremes. Now we can move the x-position off-curves equal to the on-curve.
            # but then we need to compensate the position of the on-curve and the length of the off-curves
            # to make the best fit. This compensation is the crux, magic calculation.
            # Now we need to move the special PC's and their neighbor off-curves.
            for pc, rx1, ry1, rx2, ry2 in specialPCs:
                p0 = pc[0]
                p1 = pc[1] # Off-curve, just to be moved in x for length
                p2 = pc[2] # Previous off-curve, moves to p3.x and y for compensation.
                p3 = pc[3] # Special on-curve with round extreme, to be moved for compensation.
                p4 = pc[4] # Next off-curve, moves to p3.x and y for compensation
                p5 = pc[5] # Off-curve, just to be moved in x for length.
                p6 = pc[6]
                # First understand the direction. Otherwise swap.
                if (p3.x > p4.x and p3.y > p4.y and p6.x < p3.x) or \
                    (p3.x < p4.x and p3.y < p4.y and p6.x > p3.x):
                    p0, p1, p2, p4, p5, p6 = p6, p5, p4, p2, p1, p0
                # Calculate the movement of the center onCurve point.
                if angle:
                    dx = (p4.x - p3.x)/(-angle/2)
                    dy = (p4.y - p3.y)/(-angle/2)
                else:
                    dx = dy = 0
                # Move the main onCurve point to position where it can have verticals
                p3.x = p3.x + dx
                p3.y = p3.y + dy
                # Align the horizontal offCurve position to the x of the on-curve point.
                p2.x = p4.x = p3.x
                # Calculate the slanted intersections
                intersection1 = cls.common(p3.x, p3.y, p4.x, p4.y, p5.x, p5.y, p6.x, p6.y)
                intersection2 = cls.common(p3.x, p3.y, p2.x, p2.y, p1.x, p1.y, p0.x, p0.y)
                if not None in intersection1 and not None in intersection2:
                    # And calculate the positions of the offCurves on the same ratio as the un-slanted offCurve points had,
                    # corrected by a percentage (magicNumber) of what the on curve moved from its original position.
                    # Made for angle of 8°. Likely not working for other angles. Needs more intelligent calculation in the future.
                    # Compensation is "ok", as starting point for italics to be adjusted manually.
                    p5.x = p6.x + rx1 * (intersection1[0] - p6.x)
                    p4.y = p3.y + magicNumber*ry1 * (intersection1[1] - p3.y)
                    p1.x = p0.x + rx2 * (intersection2[0] - p0.x)
                    p2.y = p3.y + magicNumber*ry2 * (intersection2[1] - p3.y)

if __name__ == '__main__':
    g = CurrentGlyph()
    if g is not None:
        f = g.getParent()
        name = g.name
        if not name+'.copy' in f:
            f[name+'.copy'] = g
        f[name] = f[name+'.copy']
        gm = GlyphMaker(f, g.name)
        gm.italicize(-7)
