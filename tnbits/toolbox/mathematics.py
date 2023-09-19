# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     mathematics.py
#

import math
import operator
import functools
from tnbits.constants import Constants as C

class FT(int):
    def __repr__(self):
        return 'FT: %d (%0.2f)' % (self, self/C.HUNITS)

    str = __repr__

class Mathematics(object):
    @classmethod
    def lucasRange(cls, a, z, n, minN=None, maxN=None):
        """Answers the range stem widths for interpolation, according to
        Lucas’ formula.

        http://www.lucasfonts.com/about/interpolation-theory/
        a = minStem
        z = maxStem
        n = number of interpolated stems, including the two masters
        minN = optional minimum value if normalizing, e.g. 0-1000
        maxN = optional maximum value if normalizing

        print(Mathematics.lucasRange(32, 212, 8))
        [32, 42, 55, 72, 94, 124, 162, 212]

        print(Mathematics.lucasRange(32, 212, 8, 0, 1000))
        [0, 55, 127, 222, 346, 508, 721, 1000]

        print(Mathematics.lucasRange(32, 212, 8, 100, 200))
        [100, 106, 113, 122, 135, 151, 172, 200]
        """

        n = n - 2  # Correct for two masters
        i = []
        for x in range(n + 2):
            v = (a ** (n + 1 - x) * z ** x) ** (1 / (n + 1))
            if not None in (minN, maxN):
                v = (v - a) * (maxN - minN) / (z - a) + minN
            i.append(int(round(v)))
        return i

    @classmethod
    def intersection(cls, x1, y1, x2, y2, x3, y3, x4, y4):
        """Returns intersection point if it exists. Otherwise (None, None) is
        answered. Different from the RoboFont intersection tool, we intersect
        on infinite line lengths. See also:

        http://en.wikipedia.org/wiki/Line-line_intersection
        """
        d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if d != 0:
            m1 = (x1*y2-y1*x2)
            m2 = (x3*y4-y3*x4)
            return (m1*(x3-x4) - m2*(x1-x2)) / d, (m1*(y3-y4) - m2*(y1-y2)) / d
        return None, None

    @classmethod
    def isBetween(cls, x1, y1, x2, y2, px, py):
        """Checks if point is on line between line endpoints. Uses epsilon
        margin for float values, can be substituted by zero for integer
        values."""
        epsilon = 1e-6
        crossproduct = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
        if abs(crossproduct) > epsilon: return False   # (or != 0 if using integers)

        dotproduct = (px - x1) * (x2 - x1) + (py - y1)*(y2 - y1)
        if dotproduct < 0 : return False

        squaredlengthba = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
        if dotproduct > squaredlengthba: return False

        return True

    @classmethod
    def squareDistance(cls, x1, y1, x2, y2):
        """Answers the square of the distance for relative comparison and to
        save the time of the `sqrt`."""
        tx, ty = x2-x1, y2-y1
        return tx*tx + ty*ty

    @classmethod
    def distance(cls, x1, y1, x2, y2):
        """Answers the distance between the points."""
        return math.sqrt(cls.squareDistance(x1, y1, x2, y2))

    @classmethod
    def orthogonalPoint(cls, point, l0, l1):
        """Checks if point is orthogonal to line _and_ orthogonal point is
        between line end points. Returns orthogonal point coordinates and
        distance from original point."""
        px, py = point
        x0, y0 = l0
        x1, y1 = l1
        x, y = cls.pointProjectedOnLine(x0, y0, x1, y1, px, py)

        if cls.isBetween(x0, y0, x1, y1, x, y):
            distance = cls.distance(px, py, x, y)
            return (x, y, distance)

    @classmethod
    def point2Line(cls, x1, y1, x2, y2, px, py):
        """Answers the distance from point _(px, py)_ to line _((x1,
        y1), (x2, y2))_."""
        x, y = cls.pointProjectedOnLine(x1, y1, x2, y2, px, py)
        tx, ty = px-x, py-y # Vector p1->p2
        return math.sqrt(tx*tx + ty*ty) # Length of p1->p2

    @classmethod
    def dotProduct(cls, v1, v2):
        return functools.reduce(operator.add, map(operator.mul, v1, v2))

    @classmethod
    def pointProjectedOnLine(cls, x1, y1, x2, y2, px, py):
        """Answers the projected point `(px, py)` on line `((x1, y1), (x2, y2))`.
        Answers `(x1, y1)` if there is not distance between the two points of the line."""
        # Line vector.
        tx, ty = float(x2 - x1), float(y2 - y1)
        v1 = (tx, ty)

        # Vector from line start to point.
        t1x, t1y = float(px - x1), float(py - y1)
        v2 = (t1x, t1y)

        # Square length of line to normalize.
        dd = tx*tx + ty*ty

        if dd == 0:
            return x1, y1

        dot = cls.dotProduct(v1, v2)
        return  x1 + (dot * tx) / dd, y1 + (dot * ty) / dd

    @classmethod
    def insideCircle(cls, dx, dy, r):
        assert r > 0

        if abs(dx) + abs(dy) <= r:
            return True
        if abs(dx) > r:
            return False
        if abs(dy) > r:
            return False
        if dx**2 + dy**2 <= r**2:
            return True

        return False

    @classmethod
    def test(cls, condition, error):
        if not condition:
            print('###', error)

    @classmethod
    def ft2Float(cls, v):
        if isinstance(v, FT):
            v = v / C.HUNITS
        return v

    @classmethod
    def ft2Int(cls, v):
        return int(round(cls.ft2Float(v)))

    @classmethod
    def value2Ft(cls, v):
        if not isinstance(v, FT):
            v = FT(v * C.HUNITS)
        return v

    @classmethod
    def values2Ft(cls, vs):
        fts = []
        for v in vs:
            fts.append(cls.value2Ft(v))
        return fts

    @classmethod
    def ftMax(cls, v1, v2):
        return FT(max(v1, v2))

    @classmethod
    def ftMin(cls, v1, v2):
        return FT(min(v1, v2))

    @classmethod
    def ftPadFloor(cls, ft, n):
        cls.test(isinstance(ft, FT), '[ftPadFloor] Not FT (%s, %s)' % (ft, n))
        return FT(ft & ~(n-1))

    @classmethod
    def ftPadRound(cls, ft, n):
        cls.test(isinstance(ft, FT), '[ftPadRound] Not FT (%s, %s)' % (ft, n))
        return cls.ftPadFloor(FT(ft + (n//2)), n )

    @classmethod
    def ftPadCeil(cls, ft, n):
        cls.test(isinstance(ft, FT), '[ftPadCeil] Not FT (%s, %s)' % (ft, n))
        return cls.ftPadFloor(FT(ft + (n-1)), n)

    @classmethod
    def ftPixFloor(cls, ft):
        cls.test(isinstance(ft, FT), '[ftPixFloor] Not FT (%s)' % ft)
        return FT(ft & ~63)

    @classmethod
    def ftPixRound(cls, ft):
        cls.test(isinstance(ft, FT), '[ftPixRound] Not FT (%s)' % ft)
        return cls.ftPixFloor(FT(ft + 32))

    @classmethod
    def ftPixCeil(cls, ft):
        cls.test(isinstance(ft, FT), '[ftPixCeil] Not FT (%s)' % ft)
        return cls.ftPixFloor(FT(ft + 63))

    @classmethod
    def isOdd(cls, v):
        return v%2 != 0

    @classmethod
    def isEven(cls, v):
        return v%2 == 0

    @classmethod
    def ftScalexy(cls, x, y, gstate):
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        scale = gstate.scale
        return FT(x * scale.x), FT(y * scale.y)

    @classmethod
    def scalexy(cls, x, y, gstate):
        scale = gstate.scale
        return x * scale.x, y * scale.y

    @classmethod
    def ftScalexyByVector(cls, x, y, v):
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        return FT(x * v.x), FT(y * v.y)

    @classmethod
    def scalexyByVector(cls, x, y, v):
        return x * v.x, y * v.y

    @classmethod
    def ftScaled(cls, d, v, gstate):
        d = cls.value2Ft(d)
        x, y = cls.scalexy(d, d, gstate)
        return FT(x * v.x + y * v.y)

    @classmethod
    def ftVectorLength(cls, x, y):
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        return FT(math.sqrt(x*x + y*y))

    @classmethod
    def vectorLength(cls, x, y):
        return math.sqrt(x*x + y*y)

    @classmethod
    def normalizedVector(cls, x, y, length=1):
        """

        Normalize the vector @(x,y). The _length_ defines
        the length of the normalized vector, default is @1@.
        ###    Freetype XXX: UNDOCUMENTED! It seems that it is possible to try   */
        ###    to normalize the vector (0,0).  Return immediately. */

        """
        if y == 0:
            return math.copysign(length, x), 0
        w = cls.vectorLength(x, y)
        if w == 0:
            return None
        return 1.0 * x * length / w, 1.0 * y * length / w

    @classmethod
    def normalize(cls, x, y, length=1):
        if y == 0:
            return length, 0
        w = cls.vectorLength(x, y)
        if w == 0:
            return None
        return 1.0 * x * length / w

    @classmethod
    def ftAxisDirection(cls, axis, p1, p2):
        assert axis in (C.X, C.Y, C.D, '')
        if axis in (C.X, C.D): # Diagonal run show dx in CVT
            v = FT(p2.ftx - p1.ftx)
        elif axis == C.Y:
            v = FT(p2.fty - p1.fty)
        else:
            v = FT(0)
        return v

    @classmethod
    def axisDirection(cls, axis, p1, p2):
        return cls.ft2Float(cls.ftAxisDirection(axis, p1, p2))

    @classmethod
    def ftPointDistance(cls, p1, p2):
        dx = p2.ftx - p1.ftx
        dy = p2.fty - p1.fty
        return FT(cls.sqrt(dx*dx + dy*dy))

    @classmethod
    def pointDistance(cls, p1, p2):
        return cls.ft2Float(cls.ftPointDistance(p1, p2))

    # Projection measuring

    @classmethod
    def ftProjectionMeasure(cls, x, y, gstate):
        """
        The @projectionMeasure@ method answers the measured x,y distance
        by the projection vector pixel size float vector (not in hUnits).
        """
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        v = gstate.projectionVector # Vector are unified, so no FT measure

        if v is None:
            return None

        return FT(x * v.x + y * v.y)

    @classmethod
    def ftDualProjectionMeasure(cls, x, y, gstate):
        """
        The @dualProjectionMeasure@ method answers the measure original
        unmoved x,y distance by the dual projection vector in pixel size float vector
        (not in hUnits).
        """
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        v = gstate.dualProjectionVector # Vector are unified, so no FT measure
        if v is None:
            return None
        return FT(x * v.x + y * v.y)

    # Freedom conversion.

    '''
    def xxxfreedom_xy2d(cls, x, y, gstate):
        pv = gstate.feedomVector
        return x * pv.x + y * pv.y
    '''
    @classmethod
    def ftFreedom_d2xy(cls, d, gstate):
        d = cls.value2Ft(d)
        v = gstate.freedomVector # Vector are unified, so no FT measure
        if v is None:
            return None
        return FT(d * v.x), FT(d * v.y)

    @classmethod
    def ftFreedom_xy2v(cls, x, y, gstate):
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        d = cls.vectorLength(x, y)
        return cls.ftFreedom_d2xy(d, gstate)

    @classmethod
    def ftFreeMoveTo(cls, x, y, d, gstate):
        # xu, yu, du have 64u value
        x = cls.value2Ft(x)
        y = cls.value2Ft(y)
        d = cls.value2Ft(d)
        xy = cls.ftFreedom_d2xy(d, gstate)
        if xy is None:
            return xy
        dx, dy = xy
        return FT(x + dx), FT(y + dy)

    @classmethod
    def freeMoveTo(cls, x, y, d, gstate):
        # Answer (x,y) as rounded int
        x, y = cls.ftFreeMoveTo(x, y, d, gstate)
        return cls.ft2Int(x), cls.ft2Int(y)

    # Touching the point

    @classmethod
    def touchPxy(cls, p):
        p.touchX()
        p.touchY()

    @classmethod
    def touchP(cls, p, gstate):
        fv = gstate.freedomVector
        if fv.x:
            p.touchX()
        if fv.y:
            p.touchY()

    # Rounding

    @classmethod
    def ftMulDiv(cls, a, b, c):
        a = cls.value2Ft(a)
        b = cls.value2Ft(b)
        c = cls.value2Ft(c)
        if c == 0:
            return FT(C.MAXINT)
        return FT(a * b / c)

    @classmethod
    def ftRoundD(cls, d, gstate, compensationIndex=None, roundState=None):
        # Do the rounding type, as methods defined in M.ROUNDERS
        d = cls.value2Ft(d)
        #scalex = gstate.getPixelSize() #gstate.scale.x
        scalex = gstate.em / gstate.scale.x
        scaledd = FT(d / scalex)
        compensation = FT(gstate.getCompensation(compensationIndex)) # In 1/64th

        if roundState is None:
            roundState = gstate.roundState

        rounded = getattr(cls, cls.ROUNDERS[roundState])(scaledd, gstate, compensation)
        return FT(rounded * scalex)

    @classmethod
    def ftRoundP(cls, p, gstate, compensationIndex=None):
        if gstate.freedomVector.isX():
            p.ftx = cls.roundD(p.ftx, gstate, compensationIndex)
        elif gstate.freedomVector.isY():
            p.fty = cls.roundD(p.fty, gstate, compensationIndex)
        # @@@@ Other vector directions here

    @classmethod
    def ftRound2Grid(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        if distance >= 0:
            v = FT(compensation + distance + 32)
            if distance and v > 0:
                v = FT(v & ~63) # FT_F26Dot6 round
            else:
                v = FT(0)
        else:
            v = FT(-cls.ftPixRound(FT(compensation - distance)))
            if v > 0:
                v = FT(0)
        return v

    @classmethod
    def ftRound2HalfGrid(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        if distance >= 0:
            v = cls.ftPixFloor(FT(distance + compensation)) + 32
            if distance and v < 0:
                v = FT(0)
        else:
            v = FT(-(cls.ftPixFloor(FT(compensation - distance)) + 32))
            if v > 0:
                v = FT(0)
        return v

    @classmethod
    def ftRound2DoubleGrid(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        if distance >= 0:
            v = distance + compensation + 16
            if distance and v > 0:
                v = FT(v & 31)
            else:
                v = FT(0)
        else:
            v = FT(-cls.ftPadRound(FT(compensation - distance), 32))
            if v > 0:
                v = 0
        return v

    @classmethod
    def ftRoundUp2Grid(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        if distance >= 0:
            v = distance + compensation + 63
            if distance and v > 0:
                v = FT(v & ~63)
            else:
                v = 0
        else:
            v = FT(-cls.ftPixCeil(compensation - distance))
            if v > 0:
                v = FT(0)
        return v

    @classmethod
    def ftRoundDown2Grid(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        if distance >= 0:
            v = compensation + distance
            if distance and v > 0:
                v = FT(v & ~63)
            else:
                v = FT(0)
        else:
            v = FT(-((compensation - distance) & 64))
            if v > 0:
                v = FT(0)
        return v

    @classmethod
    def ftRoundNone(cls, distance, gstate, compensation):
        # distance and compensation are in real pixels size here, not 1/64th
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        if distance >= 0:
            v = FT(distance + compensation)
            if distance and v < 0:
                v = FT(0)
        else:
            v = FT(distance - compensation)
            if v > 0:
                v = FT(0)
        return v

    ftRoundOff = ftRoundNone

    @classmethod
    def ftRoundSuper(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        roundperiod, roundPhase, roundthreshold = cls.values2Ft(gstate.sRoundState)
        if distance >= 0:
            v = FT(distance - roundPhase + roundthreshold + compensation) & -roundperiod
            if distance and v < 0:
                v = FT(0)
            v = FT(v + roundPhase)
        else:
            v = FT(-((roundthreshold - roundPhase - distance + compensation) & -roundperiod))
            if v > 0:
                v = FT(v - roundPhase)
        return v

    @classmethod
    def ftRoundSuper45(cls, distance, gstate, compensation):
        distance = cls.value2Ft(distance)
        compensation = cls.value2Ft(compensation)
        roundperiod, roundPhase, roundthreshold = cls.values2Ft(gstate.sRoundState)
        if distance >= 0:
            v = FT(((distance - roundPhase + roundthreshold + compensation) // roundperiod) * roundperiod)
            if distance and v < 0:
                v = FT(0)
            v = FT(v + roundPhase)
        else:
            v = FT(-((roundthreshold - roundPhase - distance + compensation) / roundperiod) * roundperiod)
            if v > 0:
                v = FT(v - roundPhase)
        return v

    ROUNDERS = {
        C.ROUND_HALFGRID:        'ftRound2HalfGrid',
        C.ROUND_GRID:            'ftRound2Grid',
        C.ROUND_DOUBLEGRID:        'ftRound2DoubleGrid',
        C.ROUND_DOWNTOGRID:        'ftRoundDown2Grid',
        C.ROUND_UPTOGRID:        'ftRoundUp2Grid',
        C.ROUND_SUPER:            'ftRoundSuper',
        C.ROUND_SUPER45:        'ftRoundSuper45',
        C.ROUND_NONE:            'ftRoundNone',
        C.ROUND_OFF:            'ftRoundOff',
    }
    '''
    @classmethod
    def xxxxrecalcAxis(cls, gstate):
        fv = gstate.freedomVector
        pv = gstate.projectionVector
        if fv.x ==  cls.AXISUNIT:
            gstate.FdotP = fv.x * LONGAXIS
        elif fv.y == cls.AXISUNIT:
            gstate.FdotP = fv.y * LONGAXIS
        else:
            gstate.FdotP = pv.x * fv.x * 4 + pv.y * fv.y * 4

        #    at small sizes, F_dot_P can become too small, resulting   */
        #    in overflows and `spikes' in a number of glyphs like `w'. */
        #if ( FT_ABS( CUR.F_dot_P ) < 0x4000000L )
        #    CUR.F_dot_P = 0x40000000L;

        gstate.currentRatio = 0        # Reset, to be recalculated on usage

    @classmethod
    def xxxxgetCurrentRatio(cls, gstate):
        """

        Returns the current aspect ratio scaling factor depending on the
        projection vector's state and device resolutions.
        Returns the aspect ratio as float, always <= 1.0 .

        """
        if not gstate.currentRatio:
            ratio = gstate.metrics.ratio
            if gstate.projectionVector.y == 0:
                gstate.currentRatio = ratio.x
            elif gstate.projectionVector.x == 0:
                gstate.currentRatio = ratio.y
            else:
                x = cls.mulDiv(gstate.projectionVector.x * ratio.x / AXISUNIT)
                y = cls.mulDiv(gstate.projectionVector.y * ratio.y / AXISUNIT)
                gstate.currentRatio = cls.vectorLength((x, y))
        return gstate.currentRatio
    '''

    ##################
    # ITALIC OFFSETS
    ##################

    @classmethod
    def getItalicOffset(cls, yoffset, italicAngle):
        '''
        Given a y offset and an italic angle, calculate the x offset.
        '''
        from math import radians, tan
        ritalicAngle = radians(italicAngle)
        xoffset = int(round(tan(ritalicAngle) * yoffset))
        return xoffset*-1

    @classmethod
    def getItalicCoordinates(cls, coords, italicAngle):
        """
        Given (x, y) coords and an italic angle, get new coordinates accounting for italic offset.
        """
        x, y = coords
        x += cls.getItalicOffset(y, italicAngle)
        return x, y

    #####################
    # INTERPOLATION
    #####################

    @classmethod
    def interpolate(cls, s1, s2, value):
        return s1 + (s2-s1) * value

    @classmethod
    def getInterpolatedValue(cls, s1, s2, target):
        if s2 != s1:
            return float(target-s1) / float(s2-s1)
        else:
            return 0

    @classmethod
    def getSlope(cls, x1, y1, x2, y2):
        xoffset = abs(x2 - x1)

        yoffset = abs(y2 - y1)

        if xoffset != 0:
            a = math.atan(yoffset/float(xoffset))

            return math.degrees(a)
        else:
            return None

M = Mathematics

if __name__ == "__main__":
    print(M.normalize(1, 0))
    print(M.normalize(1, 0.1))
    print(M.normalize(1000, 500))
    print(M.normalize(0, 1))
    print(M.normalize(0.1, 1))
    print(M.normalize(1,2, 10))
