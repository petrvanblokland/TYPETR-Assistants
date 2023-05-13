# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR points.py
#
#    Basic point transformation tools
#
import math

def intersectionPoint(x1, y1, x2, y2, x3, y3, x4, y4, doRound=False):
    """
    returns intersection point if it exists. Otherwise (None, None) is answered.
    http://en.wikipedia.org/wiki/Line-line_intersection


    >>> intersectionPoint(-100, 0, 100, 0, 0, -100, 0, 100, True) 
    (0, 0)
    >>> intersectionPoint(0, 0, 200, 0, 0, -100, 200, 100, True) 
    (100, 0)
    >>> intersectionPoint(-100, -100, 100, 100, -100, 0, 100, 0, True) 
    (0, 0)
    >>> intersectionPoint(-100, 50, 100, -50, -100, 0, 100, 0, True) 
    (0, 0)
    
    """
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if d != 0:
        m1 = (x1 * y2 - y1 * x2)
        m2 = (x3 * y4 - y3 * x4)
        x, y = (m1 * (x3 - x4) - m2 * (x1 - x2)) / d, ( m1 * (y3 - y4) - m2 * (y1 - y2)) / d
        if doRound:
            x = int(round(x))
            y = int(round(y))
    else: 
        x = y = None # No intersection point
    return x, y

def isBetween(a,b,c):
    """Answers the boolean flag if b is between @a and @c inclusive.
    
    >>> isBetween(10, 20, 30)
    True
    >>> isBetween(5, 4, 3)
    True
    >>> isBetween(5, 5, 5)
    True
    >>> isBetween(100, 99, 200)
    False
    """
    return bool(min(a, c) <= b and b <= max(a, c))
    
def orthogonalPoint(x1, y1, x2, y2, doRound=False):
    """Answers the line that goes orthogonal through the middle point between
    (@x1, @y1) and (@x2, @y2).
    
    >>> orthogonalPoint(0, 0, 200, 0, True)
    (100, 0, 100, -200)
    
    """
    mx, my = (x1 + x2)/2, (y1 + y2)/2
    if doRound:
        mx = int(round(mx))
        my = int(round(my))
    return mx, my, mx + (y2 - y1), my + (x1 - x2)

def determinant(v1, v2):
    """Answer the determinant of the line.
    
    >>> determinant(Vector(0, 0), Vector(200, 0))
    0
    >>> determinant(Vector(0, 0), Vector(0, 200))
    0
    
    """
    return v1.x * v2.y - v1.y * v2.x

#   B A S E  V E C T O R

class BaseVector:

    def __init__(self, xy=0, y=0):
        if isinstance(xy, (tuple, list)):
            self.x, self.y = xy
        else:
            self.x, self.y = xy, y

    def asPoint(self):
        """
        >>> Vector(100, 200).asPoint()
        (100, 200)
        """
        return self.x, self.y

    def __add__(self, v):
        """ vector + v --> vector
        
        >>> Vector(100, 100) + 50
        Vector(150, 150)
        >>> Vector(100, 100) + (20, 30)
        Vector(120, 130)
        >>> Vector(100, 100) + Vector(20, 30)
        Vector(120, 130)
        
        """
        if isinstance(v, (list, tuple)):
            x = self.x + v[0]
            y = self.y + v[1]
        elif isinstance(v, (int, float)):
            x = self.x + v
            y = self.y + v
        else: # Assume that v is a Vector
            assert isinstance(v, Vector)
            x = self.x + v.x
            y = self.y + v.y
        return self.__class__(x, y)

    def __sub__(self, v):
        """ vector - vector --> vector
        
        >>> Vector(100, 100) - 50
        Vector(50, 50)
        >>> Vector(100, 100) - (20, 30)
        Vector(80, 70)
        >>> Vector(100, 100) - Vector(20, 30)
        Vector(80, 70)
        
        """
        if isinstance(v, (list, tuple)):
            x = self.x - v[0]
            y = self.y - v[1]
        elif isinstance(v, (int, float)):
            x = self.x - v
            y = self.y - v
        else: # Assume that v is a Vector
            assert isinstance(v, Vector)
            x = self.x - v.x
            y = self.y - v.y
        return self.__class__(x, y)

    def __neg__(self):
        """ -vector --> vector 
        
        >>> -Vector(100, 100)
        Vector(-100, -100)
        
        """
        x = -self.x
        y = -self.y
        return self.__class__(x, y)

    def __mul__(self, v):
        """ vector * value --> vector"""
        x = self.x * v
        y = self.y * v
        return self.__class__(x, y)

    def __div__(self, v):
        """ vector / value --> vector """
        x = self.x / v
        y = self.y / v
        return self.__class__(x, y)

    def __len__(self):
        """ len(vector) 
        
        >>> len(Vector(100, 0))
        100
        >>> len(Vector(100, 100))
        141
        """
        return int(round(self.length))
        
    def _get_length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    length = property(_get_length)
    
    def setPoint(self, p):
        """ vector.fromPoint(p) 
        
        >>> v = Vector(100, 100)
        >>> v.setPoint((20, 30))
        >>> v
        Vector(20, 30)
        
        """
        self.x, self.y = p

    def normal(self):
        """
        Anwer the vector of self with length 1.
        
        >>> n = Vector(100, 100).normal()
        >>> '(%0.2f, %0.2f)' % (n.x, n.y)
        '(0.71, 0.71)'
        
        """
        l = self.length
        return self.__class__(self.x / l , self.y / l)

    def ortho(self):
        """Answer the orthogonal vector of self."""
        return self.__class__(-self.y, self.x)

    def _get_angle(self):
        if self.vector[1] != 0:
            rd = 180 / math.pi
            h = self.x
            v = self.y
            a = math.atan( h/v ) * rd
            q = self.quadrant()
            if q == 1:
                return a
            elif q == 2:
                return 180 + a
            elif q == 3:
                return 270 - a
            else:
                return 360 - a
        else:
            return 90
    angle = property(_get_angle)
    
class IntVector(BaseVector):

    def _get_x(self):
        return int(self._x)
    def _set_x(self, x):
        self._x = int(x)
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return int(self._y)
    def _set_y(self, y):
        self._y = int(y)
    y = property(_get_y, _set_y)
    
    def asIntVector(self):
        return self
        
    def __repr__(self):
        """
        
        >>> IntVector(100, 200)
        IntVector(100, 200)
        
        """
        return f'IntVector({self.x}, {self.y})'

    def asVector(self):
        return Vector(self.x, self.y)

class Vector(BaseVector):

    def __repr__(self):
        """
        >>> Vector(100, 100)
        Vector(100, 100)
        """
        return f'Vector({self.x}, {self.y})'

    def asIntVector(self):
        """
        >>> Vector(100.0, 100.0).asIntVector()
        IntVector(100, 100)
        >>> IntVector(100.0, 100.0).asIntVector()
        IntVector(100, 100)
        
        """
        return IntVector(self.x, self.y)

    def quadrant(self):
        h = self.vector.x
        v = self.vector.y
        #q = 1
        if h < 0:
            if v >= 0:  return 2
            else:     return 3
        else:
            if v < 0:   return 4
        return 1

class Line:

    def __init__(self, d=Vector(), p=Vector() ):
        if isinstance(d, (tuple, list)):
            if isinstance(d[0], int) and isinstance(d[1], int):
                d = IntVector(d)
            else:
                d = Vector(d)
        if isinstance(p, (tuple, list)):
            if isinstance(p[0], int) and isinstance(p[1], int):
                p = IntVector(p)
            else:
                p = Vector(p)
        self.dv = d # direction vector
        self.pv = p # place vector
        self.segment = Vector(), Vector()

    def makeLine(self, a=Vector(), b=Vector()):
        """
        Makes line line that runs through a and b.
        """
        self.dv = b - a
        self.pv = a
        self.segment = a, b

    def orthogonal(self):
        """
        Makes a line that runs orthogonal to self and through pv.
        """
        return Line( (self.dv[1], -self.dv[0]), self.pv )

    def near(self, x=None, y=None):

        if x is None or y is None:
            print("   x == None or y == None")
            return 0

        # test if aPt in inside bounding box of segment
        a1 = self.segment[0].x
        a2 = self.segment[0].y
        b1 = self.segment[1].x
        b2 = self.segment[1].y
        a1b1 = inbetween(a1, x, b1)
        a2b2 = inbetween(a2, y, b2)

        if a1b1 and a2b2:
            return True
        return False

    def hasIntersect(self, other):
        d = determinant(self.dv, other.dv)
        if d == 0:
            return False
        if determinant(self.dv, other.dv) != 0:
            return True
        return False

    def intersect(self, other):
        if determinant(self.dv, other.dv) != 0:
            return common(  self.dv.vector.x, self.dv.vector.y, self.pv.vector.x, self.pv.vector.y,
                        other.dv.vector.x, other.dv.vector.y, other.pv.vector.x, other.pv.vector.y)
        return None

    def angle(self):
        return self.dv.angle()

    def has_point(self, x, y):
        # werkt niet
        mu = round(x / (self.dv.x + self.pv.x), 2)
        nu = round(y / (self.dv.y + self.pv.y), 2)
        if mu == nu:
            return 1
        else:
            return 0

    def __repr__(self):
        return "Line: direction " + str(self.dv) + " place " + str(self.pv) + " segment = " + str(self.segment)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
