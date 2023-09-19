# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     point.py
#
from tnbits.constants import Constants

class Point(object):

    __slots__ = ('x', 'y', 'type', 'index', 'selected', 'smooth', 'labels', 'id', 'name', 'start', 'touchedX', 'touchedY', 'orgX', 'orgY')

    C = Constants

    def __init__(self, x, y, type=None, smooth=False, labels=None, id=None, name=None, start=False):
        self.x = self.orgX = x # Remember original position in case touched by adapter or hint..
        self.y = self.orgY = y
        if type is self.C.POINTTYPE_OFFCURVE: # Replace "offCurve" by None
            type = self.C.POINTTYPE_NONECURVE
        self.type = type
        self.smooth = smooth or False
        self.labels = labels
        if id is None and labels:
            for label in labels:
                if label.startswith('*'):
                    id = label
                    break
        self.id = id
        self.name = name or id
        self.start = start
        self.touchedX = self.touchedY = False
        self.selected = False
        self.index = None

    def __repr__(self):
        s = 'P(x:%s,y:%s,type:%s,smooth:%s' % (self.x, self.y, self.type, self.smooth)
        if self.labels:
            s += ',labels:%s' % len(self.labels)
        if self.id is not None:
            s += ',id:%s' % self.id
        if self.name is not None:
            s += ',name:%s' % self.name
        if self.start:
            s += ',start:True'
        s += ')'
        return s

    TYPE2INT = {'offCurve': None, 'line': 1, 'curve': 2, 'qcurve': 3}
    INT2TYPE = {1: 'line', 2: 'curve', 3: 'qcurve'}

    @classmethod
    def type2IntOrNone(cls, type):
        """Convert the point type string to an integer. Off-curves are @None@."""
        return cls.TYPE2INT.get(type)

    @classmethod
    def intOrNone2Type(cls, type):
        """Convert the point type code to string. Off-curves are @None@."""
        return cls.INT2TYPE.get(type)

    def asDict(self):
        """Answer the dict instance of @self@ that can be stored under pList or JSON.
        Omit values that are @None@."""
        d = dict(x=self.x, y=self.y)
        type = self.type2IntOrNone(self.type)
        if type: # Ignore if None
            d['type'] = type
        if self.smooth:
            d['smooth'] = True
        if self.labels:
            d['labels'] = self.labels
        if self.name and self.name != self.id:
            d['name'] = self.name
        if self.id:
            d['id'] = self.id
        if self.start:
            d['start'] = True
        return d

    @classmethod
    def fromDict(cls, d):
        return cls(d['x'], d['y'], cls.intOrNone2Type(d.get('type')), d.get('smooth', False), d.get('labels', []),
            d.get('id', ''), d.get('name', ''), d.get('start', False))

    def isSpace(self):
        return False

    def touchX(self):
        self.touchedX = True

    def touchY(self):
        self.touchedY = True

    def shiftBy(self, dx, dy=None):
        """Make point shift relative over (dx, dy). If dy is not defined,
        then the first attribute is supposed to be (dx, dy)"""
        if dy is None:
            dx, dy = dx
        self.shiftTo(self.x + dx, self.y + dy)

    move = shiftBy

    def shiftTo(self, x, y=None):
        """Set absolute position to (x, y). If y is not defined,
        then the first attribute is supposed to be (x, y)"""
        if y is None:
            x, y = x
        self.x = x
        self.y = y

    def getShifted(self):
        return self.x - self.orgX, self.y - self.orgY

    # self.rx       Rounded x value

    def _get_rx(self):
        return round(self.x)

    rx = property(_get_rx)

    # self.ry       Rounded y value

    def _get_ry(self):
        return round(self.y)

    ry = property(_get_ry)

    def isOffCurve(self):
        return self.type in self.C.POINTTYPE_OFFCURVES

    def isQCurve(self):
        return self.type == self.C.POINTTYPE_QUADRATIC

    def isCurve(self):
        return self.type == self.C.POINTTYPE_BEZIER

class SpacePoint(Point):
    """
    The *SpacePoint* class implements point-compatible instances
    that are not part of the glyph outline, but are needed for hinting,
    such as the 4 phantom spacing points at the end of the point list.
    
    """
    def __init__(self, uniqueID, x=None, y=None, type=None, start=False, index=None, labels=None, script=None,
            name=None, selected=False, smooth=False):
        # points.append(SpacePoint(cls.getSpacedUniqueID(1), 0, 0, self.C.POINTTYPE_SPACE, None, spacePointIndex))
        # points.append(SpacePoint(cls.getSpacedUniqueID(2), glyph.width, 0, self.C.POINTTYPE_SPACE, None, spacePointIndex+1))
        # For MS Rasterizer 1.7 and higher
        # points.append(SpacePoint(cls.getSpacedUniqueID(3), 0, font.info.ascender, self.C.POINTTYPE_SPACE, None, spacePointIndex+2))
        # points.append(SpacePoint(cls.getSpacedUniqueID(4), 0, font.info.descender, self.C.POINTTYPE_SPACE, None, spacepointinde+3))
        # The start parameter is True, if this point is the start of a contour
        self.x = self.orgx = x
        self.y = self.orgy = y
        self.uniqueID = str(uniqueID)  # Make sure it is a string, it may come from a calculation.
        self.type = type or self.C.POINTTYPE_QUADRATIC  # On curve or off curve
        self.selected = selected
        self.smooth = smooth
        self.index = index or 0  # Optional index of point
        self.script = script or ''
        self.name = name or self.uniqueID
        self.start = start
        self.touchedX = False
        self.touchedY = False

        # No need to store this in glyph.lib, SpacePoint instances are not part of the contour
        # Make an empty WingLabel just for compatibility reasons of attributes.
        # self.winglabel = WingLabel(uniqueID)

    def isSpace(self):
        return True

    def isOnCurve(self):
        return False
