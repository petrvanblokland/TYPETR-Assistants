# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#         component.py
#
class Component:

    def __init__(self, baseName, dx, dy, xScale=None, xyScale=None, yxScale=None, yScale=None):
        """Component is not given a glyph or parent. The caller should get the right reference,
        using @self.baseName@. This way there is no confusion which type object the component
        is answering (*FLoq*, *Analyzer* or *Adapter*) and it is better possible to check on
        referenced glyphs that don't exist."""
        self.baseName = baseName
        self.dx = dx
        self.dy = dy
        self.xScale = xScale
        self.yScale = yScale
        self.xyScale = xyScale
        self.yxScale = yxScale

    def __repr__(self):
        s = 'Component(glyph:%s dx:%s dy:%s' % (self.baseName, self.dx, self.dy)
        if self.xScale is not None:
            s += ' xScale:%s' % self.xScale
        if self.yScale is not None:
            s += ' yScale:%s' % self.yScale
        if self.xyScale is not None:
            s += ' xyScale:%s' % self.xyScale
        if self.yxScale is not None:
            s += ' yxScale:%s' % self.yxScale
        s += ')'
        return s

    def asDict(self):
        """Answer the dict instance of @self@ that can be stored under pList or JSON.
        Omit values that are @None@ or @0@."""
        d = dict(base=self.baseName)
        if self.dx:
            d['dx'] = self.dx
        if self.dy:
            d['dy'] = self.dy
        if self.xScale:
            d['xScale'] = self.xScale
        if self.yScale:
            d['yScale'] = self.yScale
        if self.xyScale:
            d['xyScale'] = self.xyScale
        if self.yxScale:
            d['yxScale'] = self.yxScale
        return d

    @classmethod
    def fromDict(cls, d):
        return cls(d['baseName'], d.get('dx', 0), d.get('dy', 0), d.get('xScale'), d.get('xyScale'),
            d.get('yxScale'), d.get('yScale'))

    # self.transformation       Answer the defcon component alike transformation tuple.

    def _get_transformation(self):
        return self.xScale, self.xyScale, self.yxScale, self.yScale, self.dx, self.dy

    transformation = property(_get_transformation)

    # self.position

    def _get_position(self):
        return self.dx, self.dy

    def _set_position(self, xy):
        self.dx, self.dy = xy

    position = property(_get_position, _set_position)
