# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     location.py
#
DEBUG = False
import weakref
from AppKit import NSPoint
from tnbits.toolbox.transformer import TX
from tnbits.constants import Constants
from tnbits.toolbox.glyphparts.intersect import pointOnLine, pointOnACurve
from tnbits.analyzers.elements.pointcontext import PointContext

class Location(object):
    # In the constructor points can be real points or an id referencing to a point.
    # They get transformed upon query from the floq or glyph/analyzer

    C = Constants

    POINTCONTEXTCLASS = PointContext

    D_P0 = 'p0'
    D_P1 = 'p1'
    D_P2 = 'p2'
    D_P3 = 'p3'
    D_FV = 'fv' # Key to floqMeme expression
    D_AV = 'av' # Key to analyzer value

    def __repr__(self):
        return '<Loc p0=%s p1=%s p2=%s p3=%s -- i=%s>' % (self.p0, self.p1, self.p2, self.p3, self.interpolation)

    def __init__(self):
        raise ValueError("Use specific subclassed Location constructors instead.")

    def isPointClass(self, p):
        """Answer if the point has an *x* and *y* attributes."""
        return hasattr(p, 'x') and hasattr(p, 'y')

    @classmethod
    def fromDict(cls, glyph, d):
        # Dispatcher for Location type constructors.
        if d is None:
            return None
        if cls.D_P0 in d or cls.D_P3 in d:
            return PointLocation.fromDict(glyph, d)
        #if cls.D_FV in d:
        #    return FloqLocation.fromDict(glyph, d)
        #if cls.D_AV in d:
        #    return AnalyzerLocation.fromDict(glyph, d)
        # Bad location data.
        return None

    # self.glyph

    def _get_glyph(self):
        return self._glyph()

    def _set_glyph(self, glyph):
        self._glyph = weakref.ref(glyph)

    glyph = property(_get_glyph, _set_glyph)

    # self.x, self.y

    def _get_x(self):
        if self.point is not None:
            return self.point.x
        return None

    def _get_y(self):
        if self.point is not None:
            return self.point.y
        return None

    x = property(_get_x)
    y = property(_get_y)

    def getPointByUniqueID(self, pointOrId):
        """Answer the point instance that is indicated by pointOrId identifier."""
        from tnbits.model.objects.glyph import getContours
        if isinstance(pointOrId, str):
            glyph = self.glyph
            if glyph is not None:
                # PointOrId is id string, convert to point if possible
                for contour in getContours(glyph):
                    for p in contour:
                        puid = TX.naked(p).uniqueID
                        if puid == pointOrId:
                            return p
            return None # Could not find it.
        # Just pass it on it must already be a real point
        return pointOrId

    def getPointContextByUniqueID(self, pointOrId):
        """Answer the point context that is indicated by the pointOrId identifier."""
        from tnbits.model.objects.glyph import getContours

        if not isinstance(pointOrId, str):
            pointOrId = pointOrId.name
        glyph = self.glyph
        if glyph is not None:
            # PointOrId is id string, convert to point if possible
            for cIndex, contour in enumerate(getContours(glyph)):
                for pIndex, point in enumerate(contour):
                    puid = TX.naked(point).uniqueID
                    if puid == pointOrId: # Did we find this point
                        # Get previous and next point contexts
                        prev1 = pIndex - 1 # Automatic running over to -1 index
                        prev2 = pIndex - 2 # Automatic running over to -2 index
                        prev3 = pIndex - 3 # Automatic running over to -3 index
                        next1 = pIndex + 1
                        if next1 >= len(contour):
                            next1 = 0
                        next2 = next1 + 1
                        if next2 >= len(contour):
                            next2 = 0
                        next3 = next2 + 1
                        if next3 >= len(contour):
                            next3 = 0
                        return self.POINTCONTEXTCLASS(contour[prev3], contour[prev2], contour[prev1], point, contour[next1], contour[next2],
                              contour[next3], pIndex, cIndex, contour.clockwise)

        return None # Could not find it.

    def getUniqueIDFromPoint(self, point):
        # Answer the id of the point. We have to do some guessing what kind of point this is.
        if isinstance(point, NSPoint): # Has not id, make one from the coordinates
            return '%s,%s' % (point.x, point.y)
        point = TX.naked(point) # Make sure that we have the real point, if it is a wrapper
        if not hasattr(point, 'uniqueID'): # Still has no uniqueID, make one from the coordinate.
            return '%s,%s' % (point.x, point.y)
        return point.uniqueID

    def getAnalyzer(self):
        """Get the analyzer from self.glyph (if it is available)"""
        if self.glyph is not None:
            from tnbits.analyzers.analyzermanager import analyzerManager
            return analyzerManager.getGlyphAnalyzer(self.glyph)
        return None

    def isPointLocation(self):
        return False

    def isVertical(self):
        return False

    isHorizontal = isVertical

class PointLocation(Location):
    def __init__(self, glyph, p0=None, p1=None, p2=None, p3=None, interpolation=None):
        # Store floq (as weakref), so point ids can be converted to real points
        self.glyph = glyph # Keep as weakref
        self._p0 = self._p1 = self._p2 = self._p3 = None
        # If there is only one point defined, make sure it is stored as p3
        if p0 is not None and p1 is None and p2 is None and p3 is None:
            p3, p0 = p0, p3
        # Store the points, if it is an id, then store the real point
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3 # this is the main point!
        # Initialize the interpolations as an int number between 0 and 1000. Default is 1000 (= 1.0)
        if interpolation is None:
            interpolation = 1000
        assert isinstance(interpolation, int) and 0 <= interpolation <= 1000
        self.interpolation = interpolation # Stored as rounded curve/line interpolation value int(t*1000)

    # P0

    def _get_p0(self):
        return self._p0
    def _set_p0(self, pointOrId):
        self._p0 = self.getPointByUniqueID(pointOrId)
    p0 = property(_get_p0, _set_p0)

    # P1

    def _get_p1(self):
        return self._p1
    def _set_p1(self, pointOrId):
        self._p1 = self.getPointByUniqueID(pointOrId)
    p1 = property(_get_p1, _set_p1)

    # P2

    def _get_p2(self):
        return self._p2
    def _set_p2(self, pointOrId):
        self._p2 = self.getPointByUniqueID(pointOrId)
    p2 = property(_get_p2, _set_p2)

    # P3

    def _get_p3(self):
        return self._p3
    def _set_p3(self, pointOrId):
        self._p3 = self.getPointByUniqueID(pointOrId)
    p3 = property(_get_p3, _set_p3)

    def __eq__(self, locationOrPoint):
        # Test if the locationOrPoint has the same x, y values as self.
        if self is locationOrPoint:
            return True
        p0 = self.point # Calculation the point of self location
        if isinstance(locationOrPoint, Location):
            p1 = locationOrPoint.point
        elif not locationOrPoint.__class__.__name__ in self.C.POINTTYPES:
            p1 = None
        return p0 is not None and p1 is not None and p0.x == p1.x and p0.y == p1.y

    def keepIt(self):
        # Keep this location if there is at least one of (p1, p3) defined.
        return self.p0 is not None or self.p3 is not None

    def isVertical(self):
        return (self.p0 is not None and self.p3 is not None and self.p0.x == self.p3.x) or \
            (self.p0 is not None and self.p1 is not None and self.p0.x == self.p1.x)

    def isHorizontal(self):
        return (self.p0 is not None and self.p3 is not None and self.p0.y == self.p3.y) or \
            (self.p0 is not None and self.p1 is not None and self.p0.y == self.p1.y)

    # self.point

    def _get_point(self):
        if self.p0 is None:
            return self.p3
        elif self.p1 is None and self.p2 is None:
            return pointOnLine(self.p0, self.p3, self.interpolation/1000.0)
        else:
            return pointOnACurve(self.p0, self.p1, self.p2, self.p3, self.interpolation/1000.0)
    point = property(_get_point)

    # self.pointContext

    def _get_pointContext(self):
        return self.getPointContextByUniqueID(self.p0 or self.p3)
    pointContext = property(_get_pointContext)

    def isPointLocation(self):
        return True

    def isPoint(self):
        return self.p0 is None

    def isLine(self):
        return self.p0 is not None

    def isCurve(self):
        return self.p1 is not None

    @classmethod
    def fromDict(cls, glyph, d):
        interpolation = d.get('interpolation', 1000) # == 1.0
        p0 = d.get(cls.D_P0)
        p3 = d.get(cls.D_P3)
        if p0 is None and p3 is None:
            return None
        if p3 is None: # Single point location? Keep P3 as the main point.
            p3 = p0
            p0 = None
        return cls(glyph, p0, None, None, p3, interpolation)

    def asDict(self):
        d = dict(interpolation=self.interpolation)
        if self.p0 is not None:
            d[self.D_P0] = self.getUniqueIDFromPoint(self.p0)
        if self.p1 is not None:
            d[self.D_P1] = self.getUniqueIDFromPoint(self.p1)
        if self.p2 is not None:
            d[self.D_P2] = self.getUniqueIDFromPoint(self.p2)
        if self.p3 is not None:
            d[self.D_P3] = self.getUniqueIDFromPoint(self.p3)
        return d

class LATERFloqLocation(Location):
    def __init__(self, glyph, floqMeme, interpolation=1000):
        # Set the floqMeme. This initially can be a string (name of the floqMeme),
        # later to be replace by the referenced FloqMeme instance. We use a property
        # here for storage, so we can test if the real floqMeme still exists. Otherwise
        # a None is answered as value.
        self.glyph = glyph # Keep as weakref
        self.floqMeme = floqMeme # If this is a string, it must the id for a floqMeme instanced. Will be replaced later by the real instance.
        self.interpolation = interpolation # Rounded curve/line interpolation value int(t*1000)

    def __eq__(self, locationOrFloqMeme):
        # Equal if the self.floqMeme is same as locationOrFloqMeme.floqMeme or locationOrFloqMeme
        from floqmeme import FloqMeme
        fv = self.floqMeme
        return fv is not None and (\
            (isinstance(locationOrFloqMeme, self.__class__) and fv == locationOrFloqMeme.floqMeme and fv.interpolation == self.interpolation) or\
            (isinstance(locationOrFloqMeme, FloqMeme) and fv == locationOrFloqMeme)
        )

    def _set_floqMeme(self, floqMeme):
        if isinstance(floqMeme, str):
            self._floqMeme = floqMeme # Store as name for now
        else:
            from floqmeme import FloqMeme
            assert isinstance(floqMeme, FloqMeme)
            self._floqMeme = weakref.ref(floqMeme) # Store weakref link to FloqMeme instance

    def _get_floqMeme(self):
        if isinstance(self._floqMeme, str):
            return self._floqMeme
        return self._floqMeme()

    floqMeme = property(_get_floqMeme, _set_floqMeme)

    def isLine(self):
        # Floq lines are always straight
        return True

    def keepIt(self):
        from floqmeme import FloqMeme
        return isinstance(self.floqMeme, (str, FloqMeme))

    def _get_point(self):
        if self.floqMeme:
            return self.floqMeme.interpolate(self.interpolation)
        return NSPoint(0, 0)

    point = property(_get_point)

    @classmethod
    def fromDict(cls, floq, d):
        return cls(floq, floqMeme=d.get(cls.D_FV))

    def asDict(self):
        d = dict(interpolation=self.interpolation)
        d[self.D_FV] = self.floqMeme.uniqueID;
        return d

class LATERAnalyzerLocation(Location):
    def __init__(self, glyph, analyzerValue):
        self.glyph = glyph # Set weakref of glyph
        self.analyzerValue = analyzerValue # If this is a string, it will be used as analyzer reference key.

    def _get_point(self):
        analyzer = self.getAnalyzer()
        if analyzer is not None:
            return analyzer.getPointByNamedValue(self.analyzerValue)
        return NSPoint(0, 0)

    point = property(_get_point)

    @classmethod
    def fromDict(cls, floq, d):
        return cls(floq, analyzeValue=d.get(cls.D_AV))

    def asDict(self):
        # Just store the name of the analyzer reference.
        d = {}
        if self.analyzerValue is not None:
            d[self.D_AV] = self.analyzerValue
        return d


class XXXFloqMemeSet(object):

    def __init__(self):
        self._values = {} # key:FloqMeme, so we can easily see which keys are floqMemes.

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, floqMeme):
        setattr(self, key, floqMeme)

    def __getattr__(self, key):
        if key in self._values:
            return self._values[key]
        return self.__dict__.get(key) # Always answer None for non-existing attributes.

    def __setattr__(self, key, value):
        from floqmeme import FloqMeme
        if isinstance(value, FloqMeme):
            self._values[key] = value
        else:
            self.__dict__[key] = value

    def __contains__(self, key):
        return key in self._values

    def keys(self):
        return self._values.keys()

    def values(self):
        return self._values.values()

    def items(self):
        return self._values.items()
