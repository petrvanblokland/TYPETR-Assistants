# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     floqmeme.py
#

import weakref
import math
from AppKit import NSPoint

from tnbits.toolbox.transformer import TX
from tnbits.toolbox.mathematics import M
from tnbits.toolbox.dimensions.parser.floqparser import FloqParser
from floqstate import FloqState
from location import Location, PointLocation

DEBUG = False

class FloqMeme(FloqState):

    FM_LOC0 = 'loc0'
    FM_LOC1 = 'loc1'
    FM_TYPE = 'type'
    FM_NAME = 'name'
    FM_FLOQ = 'floq'
    FM_VALUE = 'value'
    VALID_KEYS = (FM_LOC0, FM_LOC1, FM_TYPE)

    def __init__(self, glyph, type, value):
        self.glyph = glyph # Store as weakref
        self.type = type
        self.value = value # Can be string, dict of 2 locations, etc.

    def asLibValue(self):
        """Create an object from self that can be stored in *font.lib* and *glyph.lib*.
        If the floq value is *None*, then just answer it.
        If value is string or number, then just answer the value without conversion."""
        value = self.value
        if value is None:
            libValue = None # Mark not to store it in lib.
        elif isinstance(value, (str, int, float)):
            libValue = value
        else: # Need to convert this value into a type that can be stored in lib.
            libValue = TX.asDict(value)
            libValue[self.FM_FLOQ] = self.glyph.name or ''
            libValue[self.FM_TYPE] = self.type or ''
        return libValue

    @classmethod
    def fromLib(cls, glyph, d):
        """Rebuild FloqMeme instance from the lib dictionary. If not consistent data, then answer *None*."""
        value = None
        if cls.FM_LOC0 in d and cls.FM_LOC1 in d:
            loc0 = Location.fromDict(glyph, d[cls.FM_LOC0])
            loc1 = Location.fromDict(glyph, d[cls.FM_LOC1])
            if loc0 is not None and loc1 is not None:
                value = dict(loc0=loc0, loc1=loc1)
        else:
            value = d.get(cls.FM_VALUE)
        if value is not None:
            return cls(glyph, d.get(cls.FM_TYPE), value)
        return None

    def setLocations(self, loc0, loc1):
        assert isinstance(loc0, Location) and isinstance(loc1, Location)
        self.value = dict(loc0=loc0, loc1=loc1)

    def __repr__(self):
        return '<%s.%s.%s>' % (self.__class__.__name__, self.type, self._value or 'NoValue')

    def isSnappable(self):
        # To avoid circular reference, floqMemes that have one or two sides
        # if interpolating on another floqMeme, cannot be snapped by other floqMemes.
        # FloqMemes to other FloqMemes and Analyzer Values are therefore not snappable.
        return self.loc0 is not None and self.loc1 is not None and\
            self.loc0.isPointLocation() and self.loc1.isPointLocation()

    def interpolate(self, interpolation):
        """Answers an temporary interpolated *PointLocation* instance between loc0 and loc1,
        where 0 <= interpolation <= 1000"""
        if self.loc is not None:
            interpolation /= 1000.0
            point0 = self.loc0.point
            point1 = self.loc1.point
            if point0 is not None and point1 is not None:
                p = NSPoint(M.interpolate(point0.x, point1.x, interpolation), M.interpolate(point0.y, point1.y, interpolation))
                return PointLocation(self.glyph, p3=p)
        return None

    # self.glyph

    def _get_glyph(self):
        if self._glyph is not None:
            return self._glyph()
        return None
    def _set_glyph(self, glyph):
        # Do some shallow testing, if this is a Floq kind of thing.
        self._glyph = weakref.ref(glyph)
    floq = property(_get_glyph, _set_glyph)

    # self.value

    def _get_value(self):
        # Render the value to answer
        # h.lsb
        # em*0.12
        # *h.lsb
        # *h.w
        result = None
        value = self._value
        if isinstance(value, str):
            # In case it is a string, try to parse it as expression.
            value = value.strip()
            if value == 'None':
                value = None
            elif value.startswith('='): # Is this an expression?
                print('FloqMeme instantiating FloqParser')
                parser = FloqParser(self.glyph, self.type)
                value = parser.run(value[1:])
        return value

    def _set_value(self, value):
        """Set the value. This can be a simple value or a (string) expression.
        """
        if value is None:
            value = 'none'
        if not isinstance(value, (int, float, dict, tuple, list, str)):
            pass
        self._value = value

    value = property(_get_value, _set_value)

    # self.raw

    def _get_raw(self):
        return self._value

    raw = property(_get_raw, _set_value) # _set_value and _set_raw are identical

    # self.loc0

    def _get_loc0(self):
        if isinstance(self.value, dict) and self.FM_LOC0 in self.value:
            return self.value[self.FM_LOC0]
        return None

    def _set_loc0(self, loc0):
        if not isinstance(self.value, dict):
            self.value = {}
        self.value[self.FM_LOC0] = loc0

    loc0 = property(_get_loc0, _set_loc0)

    # self.loc1

    def _get_loc1(self):
        if isinstance(self.value, dict) and self.FM_LOC1 in self.value:
            return self.value[self.FM_LOC1]
        return None

    def _set_loc1(self, loc1):
        if not isinstance(self.value, dict):
            self.value = {}
        self.value[self.FM_LOC1] = loc1

    loc1 = property(_get_loc1, _set_loc1)

    # self.loc

    def _get_loc(self):
        if isinstance(self.value, dict):
            loc0 = self.value.get(self.FM_LOC0)
            loc1 = self.value.get(self.FM_LOC1)
            if loc0 is not None and loc1 is not None:
                return loc0, loc1
        return None

    def _set_loc(self, loc):
        assert isinstance(loc, (tuple, list)) and len(loc) == 2
        self.value[self.FM_LOC0], self.value[self.FM_LOC1]

    loc = property(_get_loc, _set_loc)

    # self.length   Answer the distance between the two location points, if loc0 and loc1 exist.
    #               Otherwise answer None

    def _get_length(self):
        if self.loc0 is not None and self.loc1 is not None:
            p0 = self.loc0.point
            p1 = self.loc1.point
            dx = p1.x - p0.x
            dy = p1.y - p0.y
            return math.sqrt(dx*dx + dy*dy)
        return None

    length = property(_get_length)

    # self.width    Answer the distance in X direction between the two location points.

    def _get_width(self):
        if self.loc0 is not None and self.loc1 is not None:
            p0 = self.loc0.point
            p1 = self.loc1.point
            return abs(p0.x - p1.x)

    width = property(_get_width)

    # self.height   Answer the distance in Y direction between the two location points

    def _get_height(self):
        if self.loc0 is not None and self.loc1 is not None:
            p0 = self.loc0.point
            p1 = self.loc1.point
            return abs(p0.y - p1.y)

    height = property(_get_height)

    # self.middle   Answer the middle point between the two interpolated locations

    def _get_middle(self):
        if self.loc0 is not None and self.loc1 is not None:
            p0 = self.loc0.point
            p1 = self.loc1.point
        return NSPoint(p0.x + (p1.x - p0.x)/2, p0.y + (p1.y - p0.y)/2)

    middle = property(_get_middle)

    def get(self, default=None):
        # Answer the unprocessed source of the variable (e.g. to be used in storage).
        result = self._value
        if result is None:
            result = self.loc or None
        if result is None:
            result = default
        return result

    def set(self, value=None, loc=None):
        # Set one of the three value types. Only one should be defined.
        self.value = value # Can be fixed number or expression
        self.loc = loc # Location
