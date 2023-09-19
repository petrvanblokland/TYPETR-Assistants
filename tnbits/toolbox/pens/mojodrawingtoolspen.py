# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
from mojo.drawingTools import newPath, moveTo, lineTo, curveTo, closePath, drawPath
from fontTools.pens.basePen import BasePen

from fontTools.pens.transformPen import TransformPen

class MojoDrawingToolsPen(BasePen):

    def __init__(self, g, f, offset=(0, 0), scale=(1, 1)):
        BasePen.__init__(self, f.keys())
        self.g = g
        self.f = f
        self.offset = offset
        self.scale = scale
        newPath()

    def moveTo(self, pt):
        x, y = pt
        moveTo((x * self.scale[0] + self.offset[0], y * self.scale[1] + self.offset[1]))

    def lineTo(self, pt):
        x, y = pt
        lineTo((x * self.scale[0] + self.offset[0], y * self.scale[1] + self.offset[1]))

    def curveTo(self, pt1, pt2, pt3):
        h1x, h1y = pt1
        h2x, h2y = pt2
        x, y = pt3
        curveTo((h1x * self.scale[0] + self.offset[0], h1y * self.scale[1] + self.offset[1]), (h2x * self.scale[0] + self.offset[0], h2y * self.scale[1] + self.offset[1]), (x * self.scale[0] + self.offset[0], y * self.scale[1] + self.offset[1]))

    def qCurveTo(self, pt1, pt2, pt3):
        pass

    def closePath(self):
        closePath()

    def endPath(self):
        closePath()

    def draw(self):
        drawPath()

    def addComponent(self, baseName, transformation):
        try:
            glyph = self.f[baseName]
            tPen = TransformPen(self, transformation)
            glyph.draw(tPen)
        except:
            pass
