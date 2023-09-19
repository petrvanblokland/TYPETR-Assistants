# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#


class ComponentTX:

    @classmethod
    def sortByHeight(cls, g):
        f = g.getParent()
        componentsByHeight = []
        components = []
        for c in g.components:
            if c.baseGlyph in f:
                base = f[c.baseGlyph]
                baseName = base.name
                if base.box:
                    boxHeight = base.box[3] - base.box[1]
                    componentsByHeight.append((boxHeight, baseName, c.offset, c.scale))
        componentsByHeight.sort()
        componentsByHeight.reverse()
        g.clearComponents()
        for height, baseName, offset, scale in componentsByHeight:
            g.appendComponent(baseName, offset=offset, scale=scale)

    @classmethod
    def getTallestComponent(cls, g):
        cls.sortByHeight(g)
        if g.components:
            return g.getParent()[g.components[0].baseGlyph]

    @classmethod
    def getHighestLevelComponents(cls, g, componentList=None, contourList=None, offset=(0, 0), scale=(1, 1)):
        if componentList is None:
            componentList = []
        if contourList is None:
            contourList = []
        if not g.components:
            componentList.append((g.name, offset, scale))
        else:
            for c in g:
                contourList.append(c)
        for c in g.components:
            cls.getHighestLevelComponents(g.getParent()[c.baseGlyph], componentList, contourList, (c.offset[0] + offset[0], c.offset[1] + offset[1]), (c.scale[0] * scale[0], c.scale[1] * scale[1]), )
        return componentList, contourList

    @classmethod
    def flattenComponents(cls, g):
        componentList, contourList = cls.getHighestLevelComponents(g)
        g.clearComponents()
        g.clearContours()
        for baseGlyph, offset, scale in componentList:
            g.appendComponent(baseGlyph, offset, scale)
        for contour in contourList:
            g.appendContour(contour)

if __name__ == "__main__":
    from mojo.roboFont import CurrentGlyph
    print(ComponentTX.getHighestLevelComponents(CurrentGlyph()))
