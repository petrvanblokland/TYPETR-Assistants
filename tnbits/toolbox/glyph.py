# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.toolbox.glyphparts.glyphname import GlyphNameTX
from tnbits.toolbox.glyphparts.component import ComponentTX
from tnbits.toolbox.mathematics import M

class GlyphTX:
    name = GlyphNameTX
    component = ComponentTX
    #char = CharacterTX

    @classmethod
    def setSelection(cls, glyph, selection):
        pass

    @classmethod
    def removeDuplicateBCPs(cls, glyph, DEBUG=False):
        """
        `removeDuplicateBCPs` removes duplicate. Be
        """
        originalSelection = glyph.selection
        glyph.deselect()
        for contour in glyph:
            anchorCoords = [bPoint.anchor for bPoint in contour.bPoints]
            for point in contour.points:
                if point.type == 'offCurve' and (point.x, point.y) in anchorCoords:
                    point.selected = True
                    if DEBUG:
                        print('\tremoving', point, 'from', glyph.name)
        glyph._object.selection.deleteSelectionFromGlyph()
        cls.setSelection(glyph, originalSelection)

    @classmethod
    def getSelectedBox(cls, g):
        hasSelection = False
        if g is not None:
            xmin = 9999999999
            xmax = -9999999999
            ymin = 9999999999
            ymax = -9999999999
            for p in g.selection:
                hasSelection = True
                if p.x < xmin:
                    xmin = p.x
                if p.x > xmax:
                    xmax = p.x
                if p.y < ymin:
                    ymin = p.y
                if p.y > ymax:
                    ymax = p.y
            for c in g.components:
                if c.selected and c.box:
                    hasSelection = True
                    cxmin, cymin, cxmax, cymax = c.box
                    if cxmin < xmin:
                        xmin = cxmin
                    if cxmax > xmax:
                        xmax = cxmax
                    if cymin < ymin:
                        ymin = cymin
                    if cymax > ymax:
                        ymax = cymax
        if hasSelection:
            return xmin, ymin, xmax, ymax
        elif g.box:
            return g.box

    @classmethod
    def centerBoxVertically(cls, g, upperMargin=None):
        if upperMargin is None:
            upperMargin = g.getParent().info.capHeight
        boxHeight = g.box[3] - g.box[1]
        margins = upperMargin - boxHeight
        bottomMargin = margins/2.0
        offset = bottomMargin - g.box[1]
        g.move((0, offset))

    @classmethod
    def centerBoxHorizontally(cls, g, width=None):
        if width is None:
            width = g.width
        boxWidth = g.box[2] - g.box[0]
        g.leftMargin = (width - boxWidth) / 2.0
        g.width = width

    @classmethod
    def setWidth(cls, g, newWidth=0, proportionalMargins=False, makeChanges=True, doComponents=False):
        """
        Modify the advance width of a glyph.
        """
        if g.box:
            boxWidth = g.box[2] - g.box[0]
            marginWidth = g.width - boxWidth
            newMarginWidth = newWidth - boxWidth

            if proportionalMargins:
                # add or subtract width proportionally to the existing margins
                try:
                    leftRatio = g.leftMargin/marginWidth
                except ZeroDivisionError:
                    # if there are zero margins on either side, we'll just call the glyph centered in its set width
                    leftRatio = .5
                newLeft = int(leftRatio*(newMarginWidth))
            else:
                # add or subtract equally from both sides
                widthDiff = newWidth - g.width
                newLeft = g.leftMargin + widthDiff/2
            # get the right sidebearing
            #newRight = newMarginWidth - newLeft
            if makeChanges:
                #leftShift = g.leftMargin - newLeft
                g.leftMargin = newLeft
                g.width = newWidth
                #for c in g.components:
                #    c.offset = (c.offset[0]-leftShift/2.0, c.offset[1])
            return (g.leftMargin, g.rightMargin)
        else:
            if makeChanges:
                g.width = newWidth
            return (g.leftMargin, g.rightMargin)

    #######################
    ###### checks ###########
    #######################

    @classmethod
    def getOpenContours(cls, g):
        openContours = []
        for c in g:
            if c.open:
                openContours.append(c)
        return openContours

    @classmethod
    def getDoublePoints(cls, g):
        doublePoints = []
        for c in g:
            processedCoordinates = []
            for p in c.points:
                coords = (p.x, p.y)
                if coords not in processedCoordinates:
                    points = cls.getPointsByCoordinate(coords, c, 1)
                    if len(points) > 1:
                        doublePoints.append(coords)
        return coords

    @classmethod
    def getPointsByCoordinate(cls, coord, c, wiggle=0):
        matches = []
        if isinstance(wiggle, (int, float)):
            wiggle = wiggle, wiggle
        for p in c.points:
            if coord[0]-wiggle[0] < p.x < coord[0]+wiggle[0] and coord[1]-wiggle[1] < p.y < coord[1]+wiggle[1]:
                matches.append(p)
        return matches


    @classmethod
    def removeDoublePoints(cls, g):
        """
        This won't remove double oncurve points. Something is happening where it thinks it is selecting an offcurve to delete but it is really selecting an oncurve.
        """
        cls.deselectAll(g)
        for c in g:
            processedCoordinates = []
            for p in c.points:
                coords = (p.x, p.y)
                if coords not in processedCoordinates:
                    points = cls.getPointsByCoordinate(coords, c, 1)
                    if len(points) > 1:
                        keeper = None
                        for point in points:
                            if keeper is None and p.type != 'offCurve':
                                keeper = point
                            elif p.type == 'offCurve':
                                p.selected = True
                    processedCoordinates.append(coords)
        g.naked().selection.deleteSelectionFromGlyph(deleteComponents=False, deleteAnchors=False)


    @classmethod
    def getDoubleComponents(cls, g):
        doubleComponents = []
        existing = []
        for c in g.components:
            check = c.baseGlyph, c.offset, c.scale
            if check in existing:
                doubleComponents.append(c)
            existing.append(check)

    @classmethod
    def deselectAll(cls, g):
        for c in g:
            for p in c.points:
                p.selected = False

    @classmethod
    def checkPointSmoothness(cls, g, slopeMargin=2, DEBUG=True):
        """
        Returns recommended points to smooth, points to unsmooth, and points that are colinear.
        """
        colinearPoints = []
        pointsToSmooth = []
        pointsToUnsmooth = []
        for c in g:
            if len(c) > 1:
                for i, p in enumerate(c.points):
                    # check only oncurve points
                    if p.type != "offCurve":
                        if i+1 < len(c.points):
                            nextPoint = c.points[i+1]
                        elif not c.open:
                            nextPoint = c.points[0]
                        else:
                            # if this last of an open contour, continue
                            continue
                        if i > 0:
                            previousPoint = c.points[i-1]
                        elif not c.open:
                            previousPoint  = c.points[-1]
                        else:
                            # if this first of an open contour, continue
                            continue
                        # get differences between the incoming and outgoing bcp slopes
                        # also calculate reverse slope, to account for vertical or near vertical
                        slopeDiff = None
                        reverseSlopeDiff = None
                        previousSlope = M.getSlope(previousPoint.x, previousPoint.y, p.x, p.y)
                        nextSlope = M.getSlope(p.x, p.y, nextPoint.x, nextPoint.y)
                        reversePreviousSlope = M.getSlope(previousPoint.y, previousPoint.x, p.y, p.x)
                        reverseNextSlope = M.getSlope(p.y, p.x, nextPoint.y, nextPoint.x)
                        if previousSlope is not None and nextSlope is not None:
                            slopeDiff = abs(previousSlope - nextSlope)
                        if reversePreviousSlope is not None and reverseNextSlope is not None:
                            reverseSlopeDiff = abs(reversePreviousSlope - reverseNextSlope)
                        # slopemargin is the allowable smooth tolerance
                        if (slopeDiff is not None and slopeDiff <  slopeMargin) or (reverseSlopeDiff is not None and reverseSlopeDiff <  slopeMargin):
                            smooth = True
                        else:
                            smooth = False
                        # if the previous and next are both offcurves, we have found a colinear point
                        if previousPoint.type != 'offCurve' and nextPoint.type != 'offCurve':
                            colinearPoints.append(p)
                        elif p.smooth != smooth:
                            if smooth:
                                pointsToSmooth.append(p)
                            else:
                                pointsToUnsmooth.append(p)
        return pointsToSmooth, pointsToUnsmooth, colinearPoints

    @classmethod
    def autoPointSmoothness(cls, g, slopeMargin=2, DEBUG=False):
        pointsToSmooth, pointsToUnsmooth, colinearPoints = cls.checkPointSmoothness(g)
        cls.deselectAll(g)
        if DEBUG:
            print(g.name)
            print('\t: points to smooth:', pointsToSmooth)
            print('\t: points to unsmooth:', pointsToUnsmooth)
        for p in pointsToSmooth+pointsToUnsmooth:
            p.selected = True
        g.naked().selection.toggleSmoothness()

    @classmethod
    def hasAnchor(cls, anchorName, g):
        for a in g.anchors:
            if a.name == anchorName:
                return True
        return False

    @classmethod
    def getAnchor(cls, name, g):
        for a in g.anchors:
            if a.name == name:
                return a

    @classmethod
    def cleanMissingComponentReferences(cls, f):
        for g in f:
            for c in g.components:
                if not c.baseGlyph in f:
                    print('removing', c.baseGlyph, 'from', g.name)
                    g.removeComponent(c)

if __name__ == "__main__":
    from mojo.roboFont import CurrentGlyph
    glyph = CurrentGlyph()
    GlyphTX.setWidth(glyph, 700)
