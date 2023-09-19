# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   glyph.py
#

import time
import traceback
from defcon.objects.glyph import Glyph as DefconGlyph

from tnbits.model.toolbox.undo.undomanager import UndoManager
from tnbits.model.toolbox.pens.pointcollector import drawPointsFromPack
from tnbits.toolbox.transformer import TX

from fontTools.pens.cocoaPen import CocoaPen  # XXX should not be here, see below
from fontTools.pens.boundsPen import BoundsPen

#TODO: move global functions to module __init__.

# -----------------------------------------------------------------------------
#   G L Y P H

def naked(obj):
    """Returns the wrapped (base) glyph object, else returns object itself."""
    if hasattr(obj, 'naked'):
        return obj.naked()
    return obj

nakedGlyph = naked

# -----------------------------------------------------------------------------
#   S P A C I N G

SPACEENVELOP = 'tnTools.spacingEnvelop'

def getEnvelop(glyph):
    """Answers the spacing envelop (list of (x, y) describing the polygon of
    straight lined around the glyph. Default is a list of the 4 corner points
    of the (origin, width) and vertical bounding box. If the envelop does not
    exist or there is only 1 or 2 points, always create the default box."""
    if not SPACEENVELOP in glyph.lib or len(glyph.lib[SPACEENVELOP]) < 3:
        x, y, w, h = boundingBox(glyph)
        glyph.lib[SPACEENVELOP] = [[min(0, x), y], [min(0, x), y+h], [max(x+w, glyph.width), y+h], [max(x+w, glyph.width), y]] # All lists, so they can be modified.
    return glyph.lib[SPACEENVELOP]

def setEnvelop(glyph, envelop):
    glyph.lib[SPACEENVELOP] = envelop

def _overlappingEnvelops(envelop1, envelop2, offset):
    from lib.tools import bezierTools  # TODO doesn't work outside of RoboFont

    for i, p12 in enumerate(envelop1):
        p11 = envelop1[i-1]
        for j, (x22, y22) in enumerate(envelop2):
            x21, y21 = envelop2[j-1]
            r = bezierTools.intersectLineLine(p11, p12, (x21+offset, y21), (x22+offset, y22))
            if r.status == "Intersection":
                return True # There is overlap, we can stop.
    return False

def kerningByEnvelop(glyph1, glyph2):
    """Answer the kerning value based on the touching of the envelops of
    glyph1 and glyphs2."""
    envelop1 = getEnvelop(glyph1)
    envelop2 = getEnvelop(glyph2)
    # Find an x offset, where envelop1 + (offset, 0) does not have overlapping lines with envelop2
    offset = glyph1.width/2 # Safe place to start iteration?
    while (offset < 1000 and _overlappingEnvelops(envelop1, envelop2, offset)):
        offset += 5 # Todo: Make bigger steps and iterate backwards.
    return -glyph1.width + offset # Convert to kerning value


# -----------------------------------------------------------------------------
#   O U T L I N E

def setStartPoint(glyph, pid):
    """Set the start point of contours[cIndex] to the point pid (cIndex, pIndex).
    Answer if the start point transformation was successful."""
    contour = nakedGlyph(glyph)[pid[0]]
    if 0 <= pid[1] < len(contour) and contour[pid[1]].segmentType is not None:
        contour.setStartPoint(pid[1])
        return True # Success
    return False

def getPointContext(glyph, pid, size=1):
    """Answers the slice of points pid (cIndex, pIndex) in context around the
    indexed point."""
    context = []
    contour = getContours(glyph)[pid[0]]
    nPoints = len(contour)
    # TODO: For speed, can we make this in to a real slice, instead of loop?
    for i in range(pid[1]-size, pid[1]+size+1):
        context.append(contour[i % nPoints])
    return context

def isOnCurve(point):
    """Answer if the point p is on-curve or off-curve."""
    return point.segmentType is not None

def isQuadraticContour(contour):
    """Answer that this contour is Quadratic if there is at
    least one quadratic segment."""
    for segment in contour:
        if hasattr(segment, 'type') and segment.type == 'qcurve':
            return True
        return False

def isQuadratic(glyph):
    """Answer if the glyph has quadratic curves. The first point found in the
    list of points that has a segment type of either "qcurve" or "curve"
    decides the choice. This value is cached in the glyph as glyph.segmentType.
    If there are no curve points, then the glyph is cubic "curve" by
    default."""
    glyph = nakedGlyph(glyph)
    if not hasattr(glyph, 'segmentType'):
        glyph.segmentType = 'curve' # By default
        for p in getPoints(glyph):
            if p.segmentType in ('qcurve', 'curve'):
                glyph.segmentType = p.segmentType
                break
    return glyph.segmentType == 'qcurve'

def isCubic(glyph):
    """Answer the negated value of self.isQuadratic."""
    return not isQuadratic(glyph)

def getPointByPid(glyph, pid):
    """Answer the point instance that relates to pid (cIndex, pIndex)"""
    return getContours()[pid[0]][pid[1]]

def getPrevPid(glyph, pid, prev=1):
    """Answer the previous point id on index *prev from pid. If the requested
    index runs lower than 0, start from the top of the contour index."""
    cIndex, pIndex = pid
    pIndex -= prev
    if pIndex < 0:
        contour = getContours(glyph)[cIndex]
        pIndex += len(contour)
    return cIndex, pIndex

def getNextPid(glyph, pid, next=1):
    """Answer the previous point id on index *next from pid. If the requested
    index runs higher than the number of points in the contours, start from at
    index 0 of the contour index."""
    cIndex, pIndex = pid
    pIndex += next
    contour = getContours(glyph)[cIndex]
    if pIndex >= len(contour):
        pIndex -= len(contour)
    return cIndex, pIndex

def getStartPoints(glyph):
    """Answer a list with all start points of the contours. Answer an empty
    list if the glyph has no contours."""
    return [contour[0] for contour in nakedGlyph(glyph) if contour]

def getPoints(glyph):
    points = []
    for contour in nakedGlyph(glyph):
        for p in contour:
            points.append(p)
    return points

def getPointContexts(glyph, size=1):
    """Answer all point contexts of the glyph with a window of size (default
    is 1)."""
    pointContexts = []
    for cIndex, contour in enumerate(nakedGlyph(glyph)):
        for pIndex, p in enumerate(contour):
            pointContexts.append(getPointContext(glyph, (cIndex, pIndex), size))
    return pointContexts

def getContourPoints(glyph):
    """Answer the list with all points of the glyph, organized as list of list
    of points, representing the contours."""
    contours = []
    for contour in nakedGlyph(glyph):
        c = []
        contours.append(c)
        for p in contour:
            c.append(p)
    return contours

def getContours(glyph):
    """Answer the list of contours for this glyph."""
    return nakedGlyph(glyph)._contours

def getContourPoints(contour):
    return list(contour)

def clearContours(glyph):
    glyph.clearContours()

def getBounds(glyph):
    if hasattr(glyph, 'angledBounds'):
        # DoodleGlyph.
        return glyph.angledBounds
    elif hasattr(glyph, 'bounds'):
        # ?.
        return glyph.bounds
    else:
        print('Can\'t find bounds for glyph %s' % glyph)

def isClockWise(pointsOrContour):
    """Answer the calculated clockwise flag of the contour, instead of the
    (possible wrong) contour.clockwise. isClockWise(pointList) is simple and
    fast.

    http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
    """
    p = None
    total = 0
    for index, nextP in enumerate(pointsOrContour):
        p = pointsOrContour[index-1] # Takes last point of list if index == 0 :)
        total += (nextP.x - p.x) * (nextP.y + p.y)
    return total > 0

def roundPoints(glyph):
    """Round all points in the glyph contours to integers."""
    for contour in getContours(glyph) or []:
        for p in contour:
            p.x = int(round(p.x))
            p.y = int(round(p.y))

def roundComponents(glyph):
    """Round the dx/dy transformation values of the components"""
    for component in getComponents(glyph) or []:
        t = list(component.transformation)
        t[4] = int(round(t[4]))
        t[5] = int(round(t[5]))
        component.transformation = t

class ReadOnlyPoint(object):

    def __init__(self, x, y, segmentType, smooth):
        self._x = x
        self._y = y
        self._segmentType = segmentType
        self._smooth = smooth

    def _get_x(self):
        return self._x
    def _set_x(self, value):
        raise ValueError('%s(%d, %d, %s, %s) is readonly. Cannot write attribute "x".' % (self.__class__.__name__, self.x, self.y, self.segmentType, self.smooth))
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self._y
    def _set_y(self, value):
        raise ValueError('%s(%d, %d, %s, %s) is readonly. Cannot write attribute "y".' % (self.__class__.__name__, self.x, self.y, self.segmentType, self.smooth))
    y = property(_get_y, _set_y)

    def _get_segmentType(self):
        return self._segmentType
    def _set_segmentType(self, value):
        raise ValueError('%s(%d, %d, %s, %s) is readonly. Cannot write attribute "segmentType".' % (self.__class__.__name__, self.x, self.y, self.segmentType, self.smooth))
    segmentType = property(_get_segmentType, _set_segmentType)

    def _get_smooth(self):
        return self._smooth
    def _set_smooth(self, value):
        raise ValueError('%s(%d, %d, %s, %s) is readonly. Cannot write attribute "segmentType".' % (self.__class__.__name__, self.x, self.y, self.segmentType, self.smooth))
    smooth = property(_get_smooth, _set_smooth)

def getComponentPoints(glyph):
        """Answer the list of points, as collected falling through component
        references."""

        style = glyph.font
        points = getPoints(glyph)
        for component in getComponents(glyph):
            dx, dy = component.transformation[-2:]
            if component.baseGlyph in style:
                for p in getComponentPoints(style[component.baseGlyph]):
                    if dx or dy:
                        p = ReadOnlyPoint(p.x+dx, p.y+dy, p.segmentType, p.smooth) # Make read-only point, to prevent that it is accidentally changed.
                    points.append(p)
        return points

def pointOnPath(glyph, point, padding):
    """Answer if the point is on the path of the glyph,
    measuring on a rectangle padding around the point."""
    path = glyph.getRepresentation('defconAppKit.NSBezierPath')
    oldLineWidth = path.lineWidth()
    path.setLineWidth_(padding)
    result = path.intersectsRect_(((point.x-padding, point.y-padding), (padding*2, padding*2)))
    path.setLineWidth_(oldLineWidth)
    return result

def contourIsOpen(contour):
    """Answer if the contour is open."""
    if contour:
        return contour[0].segmentType == 'move'
    return True # No points in the contour. Consider it to be open.

def closeContour(contour):
    """If the contour is open, then close it."""
    if contourIsOpen(contour):
        contour[0].segmentType = 'line'

# -----------------------------------------------------------------------------
#   C O M P O N E N T S

def hasComponents(glyph):
    """Answer if the glyph has component."""
    return len(nakedGlyph(glyph)._component) > 0


def getComponents(glyph):
    """Answer the list of components for this glyph."""
    glyph = nakedGlyph(glyph)
    if glyph is not None:
        if hasattr(glyph, '_components'):
            return glyph._components
        elif hasattr(glyph, 'components'):
            return glyph.components
    return None

def setComponents(glyph, components):
    """Set the components of the glyph to this list. Note that no further
    checking is done about the validity of the components in the list. It is
    assumed that they come from an earlier getComponents(glyph) or have a
    similar API. Then new components are created from there."""
    clearComponents(glyph)
    for component in components:
        addComponent(glyph, component.baseGlyph, component.transformation)

def baseComponent(glyph):
    """Answer the component where base name is the same as the base name part
    of glyph.name. Answer None if no such component exists. This component can
    be used to determine the margin of the base component glyph, e.g. as in
    Igrave."""
    glyph = nakedGlyph(glyph)
    for component in glyph._components:
        if glyph.name.startswith(component.baseGlyph):
            return component
    return None

def addComponent(glyph, baseName, transformation):
    """Add the baseName glyph as component to glyph, using the transformation
    tuple."""
    glyph.getPen().addComponent(baseName, transformation)

def clearComponents(glyph):
    """Clear all components from the glyph."""
    nakedGlyph(glyph)._components = []

def deleteComponent(glyph, component):
    """Delete the component instance from the glyph, it is part of the glyph
    compoonent list."""
    glyph = nakedGlyph(glyph)
    glyph.removeComponent(component)

def _leftxHeightMargin(glyph):
    x = glyph.width
    style = glyph.font
    xHeight = style.info.xHeight
    for contour in getContours(glyph):
        for point in contour:
            if 0 <= point.y <= xHeight:
                x = min(x, point.x)
    # TODO: Check on recursive component references.
    for component in getComponents(glyph):
        if component.baseGlyph in style:
            x = min(_leftxHeightMargin(style[component.baseGlyph]) + component.transformation[4], x)
    return x

# -----------------------------------------------------------------------------
#   R O B O F O N T

def updateGlyph(glyph):
    """If the parent style of glyph is an open RoboFont font, then broadcast
    the update."""
    # TODO: Should be part of tool, not global glyph function.
    from mojo.roboFont import AllFonts
    style = glyph.font
    if hasattr(style, 'naked'):
        style = style.naked()
    for font in AllFonts():
        if font.naked() is style:
            if glyph.name in font:
                font[glyph.name].update()
            break

# -----------------------------------------------------------------------------
#   A V A T A R S

def getAvatarGlyphs(glyph):
    """Answer the dictionary of avatar glyphs that have a valid axis+value
    name."""
    glyph = nakedGlyph(glyph) # Make sure it's naked.
    avatarGlyphs = {}
    if hasattr(glyph, 'layers'):
        for layerName in glyph.layers.keys():
            layerGlyph = glyph.layers[layerName]
            if not layerGlyph._contours and not layerGlyph._components:
                continue
            nameParts = layerName.split('.')
            if len(nameParts) == 2 and nameParts[0].startswith('@'):
                layerName = nameParts[0][1:]
                layerValue = TX.asInt(nameParts[1])
                if layerValue is not None:
                    avatarGlyphs[(layerName, layerValue)] = layerGlyph
    return avatarGlyphs

# -----------------------------------------------------------------------------
#   S P A C I N G

def syncDotlessSpacing(glyph, targetGlyph=None):
    """If there is a "dotless"+glyph.name in the style, then make sure that
    the margins and widths are idential. Sync otherwise. The function will try
    to match the all contours with points below xHeight. and adjust the
    position of dotless glyph accordingly if the margins are different. There
    is no other generic way, other than making the dotlessi/dotlessj be the
    source of the side bearings, which is not what users would expect for i and
    j construction."""
    style = glyph.font
    if style is None: # In situations like glyph layers?
        return
    dotlessName = "dotless"+glyph.name
    # Only if not defined and if it exists.
    if targetGlyph is None: # Just looking for sync between glyph and the "dotless..." connections, if there are any.
        # This is generic for dotlessi, dotlessj and others.
        if dotlessName in style:
            targetGlyph = style[dotlessName]

            changed = False
            # Find minimal x below xHeight
            x = _leftxHeightMargin(glyph)
            targetX = _leftxHeightMargin(targetGlyph)
            # If they are different, move the dotless glyph accordingly.
            if x != targetX:
                targetGlyph.leftMargin += x - targetX
                changed = True
            if targetGlyph.width != glyph.width:
                targetGlyph.width = glyph.width
                changed = True
            if changed:
                targetGlyph.update()

    else: # For a given target glyph, we need to check if there is a base glyph component inside.
        # Remove transformation from the component referring to the base glyph
        # This has to be done before position if the accent elements can be done.
        changed = False
        for component in getComponents(targetGlyph):
            if component.baseGlyph in (glyph.name, dotlessName):
                t = list(component.transformation)
                t[4] = t[5] = 0
                component.transformation = t
                changed = True
                break
        # Now copy the width
        if targetGlyph.width != glyph.width:
            targetGlyph.width = glyph.width
            changed = True

        if changed:
            targetGlyph.update()

def clearLayers(glyph):
    nakedGlyph(glyph).layers = {}

# -----------------------------------------------------------------------------
#   A N C H O R S

def getAnchor(glyph, name):
    """Answer the anchor with the name. Answer the None if the anchor cannot
    be found."""
    for anchor in glyph.anchors:
        if anchor.name == name:
            return anchor
    return None

def getAnchors(glyph):
    """Answer the list of anchors of the glyph."""
    return glyph.anchors

def addAnchor(glyph, name, t):
    """Add a new anchor to the glyph. Don't add if the anchor already exists.
    Answer the new anchor, for convenience of the caller."""
    x, y = t
    anchor = getAnchor(glyph, name)
    if anchor is None:
        glyph = nakedGlyph(glyph)
        anchor = glyph.anchorClass()
        anchor.name = name
        anchor.x = x
        anchor.y = y
        glyph.appendAnchor(anchor)
    else: # Otherwise just set the new position. Make sure not to set if value is equal, to avoid unnecessary trigger of dirty flag.
        if anchor.x != x:
            anchor.x = x
        if anchor.y != y:
            anchor.y = y
    return anchor

def deleteAnchor(glyph, name):
    anchor = getAnchor(glyph, name)
    if anchor is not None:
        glyph.removeAnchor(anchor)

def clearAnchors(glyph):
    glyph.clearAnchors()

# -----------------------------------------------------------------------------
#   M A R G I N S

def boundingBox(glyph):
    """Calculate the bounding box of glyph. We cannot use glyph.box, as it
    seems not to update right while dragging. Note that the result of this
    function is not chached, so it is a relative expensive call. For repeating
    retrievals of the bounding box, it is advised to use the GlyphAnalyzer
    instead."""
    glyph = nakedGlyph(glyph)
    x1 = y1 = 10000000
    x2 = y2 = -x1
    for contour in glyph:
        for point in contour:
            x1 = min(x1, point.x)
            x2 = max(x2, point.x)
            y1 = min(y1, point.y)
            y2 = max(y2, point.y)
    return x1, y1, x2-x1, y2-y1

'''
Answer the left margin of the base component From the baseGlyph we again take
the leftComponentMargin as the component also may be built from components.
Note that we must assume that there is no circle reference possible.
'''

def getLeftBaseComponentMargin(glyph):
    """Answer the left margin of the component that has the base name of
    glyph. E.g. if the glyph name is "Agrave", then the (shifted) left margin
    is answered of the component that has base name "A". If there is no such
    component, then answer the regular glyph.leftMargin. If the italic angle
    is of the style is not 0, then use italic margins."""
    style = glyph.font
    margin = glyph.angledLeftMargin
    component = baseComponent(glyph) # Find the component that has glyph name as start of self.name
    if component is not None and component.baseGlyph in style:
        baseGlyph = style[component.baseGlyph]
        if baseGlyph is not None:
            # Now we found the base component, take its left margin and add the horizontal transformation shift
            _, _, _, _, dx, _ = component.transformation
            margin = baseGlyph.angledLeftMargin + dx
    return margin

def setLeftBaseComponentMargin(glyph, margin):
    """Set the left margin of the component that has the base name of glyph.
    E.g. if the glyph name is "Agrave", then the (shifted) left margin is set
    for the component that has base name "A". If there is no such component,
    then the regular glyph.leftMargin is set. If the italic angle is of the
    style is not 0, then use italic margins."""
    component = baseComponent(glyph) # Find the component that has glyph name as start of self.name
    style = glyph.font
    if component is None: # No component, just set in the normal way
        glyph.angledLeftMargin = margin
    elif component.baseGlyph in style: # Set the left margin to the relative difference with the base glyph
        baseGlyph = style[component.baseGlyph]
        if baseGlyph is None: # Referencing base component could not be found, just set in the normal way.
            glyph.leftMargin = margin
        else: # Found the glyph, set relative to current margin and shifted base component
            _, _, _, _, dx, _ = component.transformation
            glyph.angledLeftMargin = margin - (baseGlyph.angledLeftMargin + dx - glyph.angledLeftMargin)

def getRightBaseComponentMargin(glyph):
    """Answer the right margin of the component that has the base name of
    glyph. E.g. if the glyph name is "Agrave", then the (shifted) right margin
    is answered of the component that has base name "A". If there is no such
    component, then answer the regular glyph.rightMargin. If the italic angle
    is of the style is not 0, then use italic margins."""
    style = glyph.font
    margin = glyph.angledRightMargin
    component = baseComponent(glyph) # Find the component that has glyph name as start of self.name
    style = glyph.font
    if component is not None and component.baseGlyph in style:
        baseGlyph = style[component.baseGlyph]
        if baseGlyph is not None:
            # Now we found the base component, take its left margin and add the horizontal transformation shift
            _, _, _, _, dx, _ = component.transformation
            margin = glyph.width - (baseGlyph.width - baseGlyph.angledRightMargin + dx)
    return margin

def setRightBaseComponentMargin(glyph, margin):
    """Set the right margin of the component that has the base name of glyph.
    E.g. if the glyph name is "Agrave", then the (shifted) right margin is set
    for the component that has base name "A". If there is no such component,
    then the regular glyph.rightMargin is set. If the italic angle is of the
    style is not 0, then use italic margins."""
    component = baseComponent(glyph) # Find the component that has glyph name as start of self.name
    style = glyph.font
    if component is None: # No component, just set in the normal way
        glyph.angledRightMargin = margin
    elif component.baseGlyph in style: # Set the left margin to the relative difference with the base glyph
        baseGlyph = style[component.baseGlyph]
        if baseGlyph is None: # Referencing base component could not be found, just set in the normal way.
            glyph.angledRightMargin = margin
        else: # Found the glyph, set relative to current margin and shifted base component
            _, _, _, _, dx, _ = component.transformation
            glyph.width = margin + baseGlyph.width - baseGlyph.angledRightMargin + dx

def leftComponentMargins(glyph):
    """Answer a dictionary of the left margins of all components, including
    their component offset with format {componentBaseName: [123, 234], ...}.
    Because it is possible that there are multiple references of the same
    component, the value of the dictionary is a set of margins."""
    glyph = nakedGlyph(glyph)
    leftMargins = {}
    style = glyph.font
    for component in glyph._components:
        baseName = component.baseGlyph
        # Get the component glyph if it exists in the style. Otherwise ignore.
        if baseName in style:
            componentGlyph = style[baseName]
            # Round transformation dx.
            dx = int(round(component.transformation[4]))
            # Make entry on baseName if it doesn't exist yet.
            if not baseName in leftMargins:
                leftMargins[baseName] = set()
            leftMargins[baseName].add(dx + componentGlyph.leftMargin) # Only one level deep. Non-recursive.
    return leftMargins

def rightComponentMargins(glyph):
    """Answer a dictionary of the right margins of all components, including
    their component offset with format {componentBaseName: [123, 234], ...}.
    Because it is possible that there are multiple references of the same
    component, the value of the dictionary is a set of margins."""
    glyph = nakedGlyph(glyph)
    rightMargins = {}
    style = glyph.font
    for component in glyph._components:
        baseName = component.baseGlyph
        # Get the component glyph if it exists in the style. Otherwise ignore.
        if baseName in style:
            componentGlyph = style[baseName]
            # Round transformation dx.
            dx = int(round(component.transformation[4]))
            # Make entry on baseName if it doesn't exist yet.
            if not baseName in rightMargins:
                rightMargins[baseName] = set()
            componentRightSize = dx + componentGlyph.width - componentGlyph.rightMargin
            rightMargins[baseName].add(glyph.width - componentRightSize) # Only one level deep. Non-recursive.
    return rightMargins

def swapContours(glyph, index1, index2):
    """Swap the order of the contours."""
    glyph = nakedGlyph(glyph)
    glyph._contours[index1], glyph._contours[index2] = glyph._contours[index2], glyph._contours[index1]

def setAutoStartPoints(glyph):
    """Find the automatic position of the origins and adjust the contours.
    Calculate automatic start points for all characters & contours in the font.
    Preferred position of the start point is at the most bottom-left of the
    Contour For each contour on the glyph, the function looks for the lowest
    point first. If it detects more than one (like the bottom of most H's) it
    takes the most left point. When adjusting a font for interpolation it is
    likely that the masters have a similar construction. This works fine in
    most cases, but of course it is not completely waterproof. Answer the
    boolean flag if something was changed."""
    changed = False
    for contour in glyph:
        i = 0
        x = y = 10000000 # Very far away top-right
        for index, point in enumerate(contour):
            if point.segmentType is not None:
                # Any smaller y or the smallest x for a known y.
                if point.y < y or (point.y == y and point.x < x):
                    i = index
                    x = point.x
                    y = point.y
                    # Did it change?
                    if i > 0:
                        changed = True
        if i > 0:
            contour.setStartPoint(i)
    return changed

def getComponentBaseOrder(glyph):
    """Answer the dictionary with component info as {baseGlyph: [index1, ...],
    ...}, where the index is the order of components. This way it is easy to
    compare the component structure between two glyphs."""
    componentBases = {}
    style = glyph.font
    for cIndex, component in enumerate(getComponents(glyph)):
        if not component.baseGlyph in componentBases:
            componentBases[component.baseGlyph] = []
        componentBases[component.baseGlyph].append(cIndex)
    return componentBases

def isClockWise(contour):
    """Answer Contour direction. Simple and fast.

    http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
    """
    total = 0
    for index, point in enumerate(contour):
        p = contour[index-1] # Takes last point of list if index == 0 :)
        total += (point.x - p.x) * (point.y + p.y)
    return total > 0

#   Undo handling for glyphs

def prepareUndo(glyph, message, pack=None):
    """If the glyph can handle prepareUndo, then transfer the request.
    Otherwise we have to create an UndoManager in the glyph if it does not
    exists (as in raw RoboFont glyphs)."""
    if hasattr(glyph, 'prepareUndo'):
        glyph.prepareUndo(message)
        return
    if not hasattr(glyph, 'undoManager'):
        glyph.undoManager = UndoManager()
    glyph.undoManager.prepareUndo(message, pack)

def performUndo(glyph):
    """If the glyph can handle performUndo, then transfer the request.
    Otherwise we have to create an UndoManager in the glyph if it does not
    exists (as in raw RoboFont glyphs)."""
    if hasattr(glyph, 'performUndo'):
        glyph.performUndo()
        return
    if not hasattr(glyph, 'undoManager'):
        glyph.undoManager = UndoManager()
    glyph.undoManager.performUndo()

def undo(glyph):
    """If the glyph can handle undo, then transfer the request. Otherwise we
    have to create an UndoManager in the glyph if it does not exists (as in raw
    RoboFont glyphs)."""
    if 'Doodle' in nakedGlyph(glyph).__class__.__name__:
        from lib.doodleUndo import glyphUndoManagersForGlyphs
        for um in glyphUndoManagersForGlyphs([glyph]):
            um.undo()
    else:
        if not hasattr(glyph, 'undoManager'):
            glyph.undoManager = UndoManager()
        glyph.undoManager.undo()

def redo(glyph):
    """If the glyph can handle redo, then transfer the request. Otherwise we
    have to create an UndoManager in the glyph if it does not exists (as in raw
    RoboFont glyphs)."""
    if 'Doodle' in nakedGlyph(glyph).__class__.__name__:
        from lib.doodleUndo import glyphUndoManagersForGlyphs
        for um in glyphUndoManagersForGlyphs([glyph]):
            um.redo()
    else:
        if not hasattr(glyph, 'undoManager'):
            glyph.undoManager = UndoManager()
        glyph.undoManager.redo()

# -----------------------------------------------------------------------------
#   D I M E N S I O N S
#   (Formerly known as FloqModel values)

DIMENSIONS_KEY = 'tnTools.dimensions'

def getDimensions(glyph):
    if not DIMENSIONS_KEY in glyph.lib:
        self.clearDimensions() # Initialize empty dimensions dictionary
    return glyph.lib[DIMENSIONS_KEY]

def clearDimensions(glyph):
    """Create empty variations lib dictionary for storing deltas."""
    glyph.lib[DIMENSIONS_KEY] = dict(stems={}, bars={}, diagonals={}, blueBars={})

# -----------------------------------------------------------------------------
#   V A R I A T I O N S

VARIATION_DELTALIB_KEY = 'tnTools.variationDeltas'
DELTA_WIDTH_ANCHOR = 'deltaWidth' # Name of the anchor that defines the delta width
POINT_ID_PREFIX = 'Pt'
COMPONENT_ID_PREFIX = 'Co'
# deltaWidth y-offset for better grab (less likely to overlap with glyph outline)
ANCHOR_Y_OFFSET = -32

def getDeltasLib(glyph):
    """Answers the style.lib dictionary with all DeltaLocations dicts.
    Gets the deltalibs in the glyph, if they exist. Otherwise initializes an
    empty dictionary. Format of the data:
    glyph.lib[VARIATION_DELTALIBS_KEY] = { # deltasLib
        <deltaLocationName>: { # deltas
            deltaWidth: 100,
            deltasXY: {<pointId>: (20, 30), ...}
        }
        ...
    }
    """
    if not VARIATION_DELTALIB_KEY in glyph.lib:
        # Key is unique DeltaLocation name, value is DeltaLocation dict.
        glyph.lib[VARIATION_DELTALIB_KEY] = {}
    return glyph.lib[VARIATION_DELTALIB_KEY]

def deleteDeltas(glyph, name):
    deltasLib = getDeltasLib[name]
    assert name in deltasLib
    del deltasLib[name]

def getDeltaPointId(p):
    """Answer a unique point ID, based on time, current index and position"""
    labels = p.labels
    for dpid in labels:
        if dpid.startswith(POINT_ID_PREFIX):
            return dpid
    dpid = '%s%X%X' % (POINT_ID_PREFIX, time.time()*100, id(p))
    labels.append(dpid)
    p.labels = labels
    return dpid

def getComponentId(component, index):
    """For now, just keep use the index as unique number; we cannot store
    something in the component. Although we make a recognizable difference
    between point ID's and component ID's, in TrueType it is not legal to mix
    outlines and component references."""
    return '%s%d' % (COMPONENT_ID_PREFIX, index)

#   Deltas

def getDeltas(glyph, name):
    """Answer the deltas for this location. {'deltaWidth':100,
    'deltasXY':{...}} The deltasXY dictionary has pointId or comppnentId as
    keys and (dx, dy) delta tuple as value.  Answer an empty deltas dictionary,
    if the deltaLocation name does not exist."""
    deltasLib = getDeltasLib(glyph)
    if not name in deltasLib:
        deltasLib[name] = dict(deltaWidth=0, deltasXY={}) # Initializes deltas
    return deltasLib[name] # Answer {'deltaWidth', 100, deltasXY:{...}}

def setDeltas(glyph, name, deltas):
    """Set the points/components deltas for this location. The deltas
    dictionary must have format point/component ID's as key and (dx,dy) delta
    tuple as value."""
    assert 'deltaWidth' in deltas and 'deltasXY' in deltas
    deltasLib = getDeltasLib(glyph)
    deltasLib[name] = deltas

#   deltaWidth

def getDeltaWidth(neutralGlyph, name):
    """Answer the deltaWidth of deltaLocation name. This is the difference with
    neutralGlyph.width. Answer 0 if for some reason the delta width does not
    exist for name."""
    return getDeltas(name)['deltaWidth']

def setDeltaWidth(neutralGlyph, name, deltaWidth):
    """Store the delta width under deltaLocation name. Note that this
    deltaWidth already is the difference with neutral.width."""
    getDeltas(name)['deltaWidth'] = deltaWidth

#   deltasXY

def getDeltasXY(neutralGlyph, name):
    """Answer the deltaWidth of deltaLocation name. This is the difference with
    neutralGlyph.width. Answer 0 if for some reason the delta width does not
    exist for name."""
    return getDeltas(name)['deltasXY']

def setDeltasXY(neutralGlyph, name, deltasXY):
    """Store the delta width under deltaLocation name. Note that this
    deltaWidth already is the difference with neutral.width."""
    getDeltas(name)['deltasXY'] = deltasXY

#   Glyph --> Deltas

def glyph2Deltas(neutralGlyph, deltaGlyph):
    """Answer a dictionary of deltas (difference in (x, y), where the key is a
    unique point id. Note that it is not allowed in TrueTupe to have both
    contours and components together, for the sake of the design process we'll
    allow both here. The Variation font export needs to expand the component,
    taking over its deltas into point deltas."""

    deltasXY = {}
    deltas = dict(deltaWidth=0, deltasXY=deltasXY)
    neutralGlyph = nakedGlyph(neutralGlyph)
    deltaGlyph = nakedGlyph(deltaGlyph)

    # Handle the delta points.
    neutralPoints = getPoints(neutralGlyph)
    deltaPoints = getPoints(deltaGlyph)

    if len(deltaPoints) != len(neutralPoints): # Only when matching amount of points.
        print('### Not matching points for neutral %s (%d) and %s (%d)' % (neutralGlyph.name, len(neutralPoints), deltaGlyph.font.info.styleName, len(deltaPoints)))
    else:
        for pIndex, np in enumerate(neutralPoints):
            dpid = getDeltaPointId(np)
            dp = deltaPoints[pIndex]
            dx = dp.x-np.x
            dy = dp.y-np.y
            if dx or dy:
                deltasXY[dpid] = dx, dy

    # Handle the delta compoonets
    neutralComponents = getComponents(neutralGlyph)
    deltaComponents = getComponents(deltaGlyph)
    if len(deltaComponents) != len(neutralComponents): # Only when matching amount of components
        print('### Not matching components for neutral', neutralGlyph.name, 'and', deltaGlyph.getParent().info.styleName)
    else:
        for cIndex, nc in enumerate(neutralComponents):
            dcip = getComponentId(deltaGlyph, cIndex)
            dc = deltaComponents[cIndex]
            dx = dc.transformation[-2] - nc.transformation[-2]
            dy = dc.transformation[-1] - nc.transformation[-1]
            if dx or dy:
                deltasXY[dcip] = dx, dy

    # If there is deltawWidth anchor, then use x-position to calculate delta
    # width. Deltawidth is initialized to 0, if there is no deltaWidth anchor.
    # It the responsibility of the caller to create the anchor by calling
    # setDeltaWidthAnchor()
    deltaWidthAnchor = getAnchor(deltaGlyph, DELTA_WIDTH_ANCHOR)
    if deltaWidthAnchor is not None: # Otherwise ignore, it is already 0
        deltas['deltaWidth'] = deltaWidthAnchor.x - neutralGlyph.width # Store the delta difference.

    return deltas

def makeDeltaWidthAnchor(neutralGlyph, deltaGlyph, deltaWidth=None):
    """Set the deltaWidth in the deltaGlyph and make sure that the deltaWidth
    anchor exists. If deltaWidth is None, then the angledRightMargin of
    neutralGlyph is used to copy to deltaGlyph. If it already exists, only
    alter the position of the anchor, if the position is different from what it
    should be. We do this check to avoid unnecessary setting of the glyph dirty
    flag."""
    deltaWidthAnchor = getAnchor(deltaGlyph, DELTA_WIDTH_ANCHOR)
    if deltaWidthAnchor is None: # Otherwise create the anchor
        if deltaWidth is None:
            if neutralGlyph.bounds is None or deltaGlyph.bounds is None:
                deltaWidth = 0
            else: # Difference in right max of outline.
                deltaWidth = deltaGlyph.bounds[2] - neutralGlyph.bounds[2]
        addAnchor(deltaGlyph, DELTA_WIDTH_ANCHOR, (neutralGlyph.width + (deltaWidth or 0), ANCHOR_Y_OFFSET)) # y-offset for better grab.
    elif deltaWidth is not None:
        if deltaWidthAnchor.x != neutralGlyph.width + (deltaWidth or 0) or deltaWidthAnchor.y != ANCHOR_Y_OFFSET:
            # Only update if changing to avoid setting deltaGlyph dirty flag.
            deltaWidthAnchor.x = neutralGlyph.width + (deltaWidth or 0)
            deltaWidthAnchor.y = ANCHOR_Y_OFFSET

def clearDeltaGlyph(neutralGlyph):
    """Clear deltaGlyph in layer, in case the number of contours, points or
    components changed."""
    deltaGlyph = neutralGlyph.getLayer(LAYER_NAME)
    deltaGlyph.clear()

def deltas2Glyph(neutralGlyph, deltas, deltaGlyph):
    """Expand the neutralGlyph by the set of deltas on points and component
    positions. If the deltaGlyph does not exist as layer LAYER_NAME, create
    the layer and copy the glyph from the neutralGlyph forground.

    Note that it is not allowed in TrueType to have both contours and
    components together -- for the sake of the design process we'll allow both
    here. The Variation font export needs to expand the component, taking over
    it's deltas into point deltas."""

    deltasXY = deltas.get('deltasXY', {}) # Make data format robust to format mistakes.
    deltaWidth = deltas.get('deltaWidth', 0)

    # If the delta glyph does not exist as layer, create it, copy from neutral
    # forground.
    neutralGlyph = nakedGlyph(neutralGlyph)
    deltaGlyph = nakedGlyph(deltaGlyph)

    neutralPoints = getPoints(neutralGlyph)
    neutralComponents = getComponents(neutralGlyph)

    deltaPoints = getPoints(deltaGlyph)
    deltaComponents = getComponents(deltaGlyph)

    if len(neutralPoints) != len(deltaPoints) or len(neutralComponents) != len(deltaComponents):
        # Nothing there yet or not compatible points/components, draw the new
        # neutral glyph there.
        deltaGlyph.clear()
        neutralGlyph.draw(deltaGlyph.getPen())
        if len(deltaGlyph) >= 4:
            for n in range(4): # We got 4 extra points, remove them for now.
                deltaGlyph.removeContour(deltaGlyph[-1])
        # Get new points and components
        deltaPoints = getPoints(deltaGlyph)
        deltaComponents = getComponents(deltaGlyph)

    # Run through the neutral points and adjust the position of the deltaGlyph
    # points if there is a delta pairs with that ID.
    for pIndex, np in enumerate(neutralPoints):
        dipd = getDeltaPointId(np)
        dp = deltaPoints[pIndex]
        dx, dy = deltasXY.get(dipd, (0, 0))
        dpx = np.x + dx
        dpy = np.y + dy
        if dpx != dp.x or dpy != dp.y: # Only update  if changing, to avoid setting deltaGlyph dirty flag.
            dp.x = dpx
            dp.y = dpy

    # Handle components with deltas
    for cIndex, nc in enumerate(neutralComponents):
        dcip = getComponentId(deltaGlyph, cIndex)
        if dcip in deltasXY:
            dc = deltaComponents[cIndex]
            dx, dy = deltas.get(dcip, (0, 0))
            neutralT = list(nc.transformation)
            deltaT = list(dc.transformation)
            tx = neutralT[-2] + dx
            ty = neutralT[-1] + dy
            if tx != deltaT[-2] or ty != deltaT[-1]: # Only update if changing to avoid setting deltaGlyph dirty flag.
                deltaT[-2] = tx
                deltaT[-1] = ty
                deltaGlyph.transformation = deltaT

    # Set the deltaWidth anchor to position. Create the anchor if it does not
    # exist. If there is deltwWidth anchor, then use x-position to calculate
    # delta width.
    makeDeltaWidthAnchor(neutralGlyph, deltaGlyph, deltaWidth)

def saveGlyphAsDeltas(neutralGlyph, deltaGlyph, deltaLocationName):
    """Standard function to store the deltaGlyph as pack of delta values in
    neutralGlyph.lib, using the location dictionary as key). Raise an error if
    the glyphs are not point compatible. If there already exist a delta
    representation under location, then overwite without warning (acting like a
    dictionary). """
    deltas = glyph2Deltas(neutralGlyph, deltaGlyph)
    setDeltas(neutralGlyph, deltaLocationName, deltas)
    return deltas

def readLayerGlyphFromDeltas(neutralGlyph, deltaGlyph, deltaLocName):
    # Get the glyph delta's library
    deltas = getDeltas(neutralGlyph, deltaLocName)
    deltas2Glyph(neutralGlyph, deltas, deltaGlyph)

def clearDeltas(neutralGlyph):
    """Create empty variations lib dictionary for storing deltas."""
    neutralGlyph.lib[VARIATION_DELTALIB_KEY] = {}

# -----------------------------------------------------------------------------
#   G L Y P H

class Glyph(DefconGlyph):
    """Common interface for UFO and OpenType glyphs.

        glyph.font

        Representations
        defconAppKit.NSBezierPath

        >>> from tnbits.model.objects.style import Style
        >>> from tnTestFonts import getFontPath
        >>> styleName = "CusterRE-RegularS2.ttf"
        >>> path = getFontPath(styleName)
        >>> style = Style(path)
        >>> 'aaa' in style.storage.getGlyphNames() # Otherwise KeyError for non-existing glyph
        False
        >>> style.storage.readGlyphPack('a')['curveType']
        'quadratic'
        >>> glyph = style['a']
        >>> glyph.width
        320
        >>> glyph.bounds
        (28, -6, 315, 295)
        >>> glyph.unicodes
        [97]
        >>> #from tnbits.analyzers.analyzermanager import analyzerManager
        >>> #getGlyphAnalyzer

    """
    """
        >>> glyph.name
        'a'
        >>> len(glyph._contours)

    """

    def __init__(self, glyphName, glyphPack=None, parent=None):
        DefconGlyph.__init__(self)
        self.width = 500  # XXX default?
        self.name = glyphName
        self.deselectAll() # Point index (contourIndex, pointIndex)
        # TODO Make Undo work
        # self.undoManager = UndoManager()
        if glyphPack is not None:
            self.unpackGlyph(glyphPack)

        try:
            self.setParent(parent)
        except Exception as e:
            # Newer versions of DefCon already take care of parent internally.
            pass

    def unpackGlyph(self, glyphPack):
        self.width = glyphPack.get("width", self.width)
        #self.curveType = glyphPack.get("curveType", 'cubic')
        self.curveType = glyphPack.get("curveType", 'quadratic')
        glyphPack['curveType'] = self.curveType
        pointPen = self.getPointPen()
        drawPointsFromPack(glyphPack, pointPen)
        self.unicodes = glyphPack.get("unicodes", [])

    def _get_parent(self):
        return self.getParent()
    parent = property(_get_parent)

    def packGlyph(self):
        contours = []
        for contour in self.contours:
            contours.append(contour.packContour())
        components = []
        for component in self.components:
            components.append(component.packComponent())

        return dict(
            glyphName=self.name,
            width=self.width,
            curveType=self.curveType,
            contours=contours,
            components=components,
            unicodes=self.unicodes,
        )

    def deselectAll(self):
        self.selectedPoints = set()
        self.selectedComponents = set()

    def selectAll(self):
        """Select all points of the glyph, including the off-curve points."""
        for cIndex, contour in enumerate(self.contours):
            for point in contour.points:
                self.selectPoint((cIndex, point.index))
        for componentIndex, component in enumerate(self.components):
            self.selectComponent(componentIndex)

    def selectPoint(self, pid):
        """Add the point index pid (contourIndex, pointIndex) to the set of
        selected points."""
        self.selectedPoints.add(pid)
        # In case the storage supports the selection of point, notify.
        # FIXME: where is storage selectPoint()?
        self.parent.storage.selectPoint(self.name, pid, True)

    def deselectPoint(self, pid):
        """If the point index pid (pid (contourIndex, pointIndex) is in the
        set of selected points, then remove it."""
        if pid in self.selectedPoints:
            self.selectedPoints.remove(pid)
        # In case the storage supports the selection of point, notify.
        self.parent.storage.selectPoint(self.name, pid, False)

    def getSelectedContours(self):
        """In case the storage supports the selection of contours and
        individual points, answer the list of selected contours. Otherwise
        answer an empty list."""
        return self.parent.storage.getSelectedContourIndices(self.name)

    def setCurrentPoint(self, pid=None):
        """Set the (cIndex, pIndex) of the current point. If omitted or None,
        then there is no current point selected."""
        self.currentPoint = pid

    def setCurrentSegment(self, pids=None):
        """Set the (pid1, pid2) of the current segment. If omitted or NOne,
        then there is no current segment selected."""
        self.currentSegment = pids

    def selectSegment(self, pid1, pid2):
        self.selectPoint(pid1)
        self.selectPoint(pid2)

    def unSelectSegment(self, pid1, pid2):
        self.unSelectPoint(pid1)
        self.unSelectPoint(pid2)

    def selectContour(self, cIndex):
        for p in self.contours[cIndex]:
            self.selectPoint((cIndex, p.index))

    def unselectContour(self, cIndex):
        for p in self.contour[cIndex]:
            self.deselectPoint((cIndex, p.index))

    def selectComponent(self, componentIndex):
        self.selectedComponents.add(componentIndex)

    def deselectComponent(self, componentIndex):
        if componentIndex in self.selectedComponents:
            self.selectedComponents.remove(componentIndex)

    def setCurrentComponent(self, componentIndex=None):
        self.currentComponent = componentIndex

    def invalidateRepresentations(self):
        self._representations = {}

    def getRepresentation(self, name, *args, **kwargs):
        """Get the named representation. Check if the storage is capable (as
        in RoboFont the most used representations are already there in cache),
        otherwise check if the glyph has it cached. If that fails try to
        create a new representation with that name."""
        # TODO: Need to solve this to make compatible with RoboFont. Change to
        # global function instead?
        rep = None

        # First check if the storage is capable to deliver.
        if self.parent is not None:
            rep = self.parent.storage.getRepresentation(self.name, name)

        if rep is None:
            rep = self._representations.get(name)

        if rep is None: # Otherwise the glyph should be able to create.
            rep = _glyphRepresentationFactories[name](self, *args, **kwargs)
            self._representations[name] = rep

        return rep

    def prepareUndo(self, message):
        #self.undoManager.prepareUndo(message, self.packGlyph())
        pass

    def performUndo(self):
        #self.undoManager.performUndo()
        pass

    def undo(self):
        pack = self.undoManager.undo()
        if pack is not None:
            self.unpackGlyph(pack)
            self.invalidateRepresentations()

    def redo(self):
        pack = self.undoManager.redo()
        if pack is not None:
            self.unpackGlyph(pack)
            self.invalidateRepresentations()

    def deleteSelection(self):
        """Delete all points that are selected. If this causes contours to
        become empty, then also delete the contours from the glyph. Note to
        delete in the right order, otherwise the selected pid's get invalid."""
        for cIndex, contour in enumerate(self.contours):
            points = []
            for point in contour.points:
                if not (cIndex, point.index) in self.selectedPoints:
                    points.append(point)
            contour.points = points
        self.deleteEmptyContours() # Check if there are empty contours.
        self.deselectAll() # Make sure that the selected indices don't refer to deleted points.
        self.setCurrentPoint() # Deselect the current point.

    def deleteEmptyContours(self):
        """Delete all contours from the glyph that have no points."""
        contours = []
        for contour in self.contours:
            if contour.points:
                contours.append(contour)
        self.contours = contours # Replace old list by new list.
        self.invalidateRepresentations()

    def getPoints(self):
        # TODO: if there's a "points" representation, it should be accessed through the
        # dynamic "points" attribute, and this method should go.
        return self.points

    def roundPoints(self):
        pass

    def getGlyphPath(self):
        return self.nsBezierPath

    def getGlyphOrgPath(self):
        """Answer the glyph path, based on (p.orgX, p.orgY), normally the
        status before any dragging started."""
        return self.nsBezierOrgPath

    def update(self):
        self.invalidateRepresentations()

    def updateFromAdapter(self):
        """Data in the storage change, due to an external action. Update the
        glyph data from the storage."""
        glyphPack = self.parent.storage.readGlyphPack(self.name)
        if glyphPack is not None:
            self.unpackGlyph(glyphPack)

    #   I N T E R S E C T I O N S

    def getIntersectionsWithLine(self, x1, x2, y1, y2, canHaveComponent=False, addSideBearings=False):
        """Intersect a glyph with a line. Returning a list of
        intersections."""
        intersects = self.getRepresentation("intersections", beam=((x1, y1), (x2, y2)), canHaveComponent=canHaveComponent)
        if addSideBearings:
            return intersects.lefMarginIntersection + intersects.intersects + intersects.rightMarginIntersection
        return intersects.intersects

    #   R E P R E S E N T A T I O N S

    def getGlyphPath(self):
        return self.nsBezierPath

# TODO: This needs to be adapted to defcon representations.
_glyphRepresentationFactories = {}

def addGlyphRepresentationFactory(name, factory):
    _glyphRepresentationFactories[name] = factory

def nsBezierPathFactory(glyph):
    # TODO this should move to a module that is allowed to import Cocoa things
    pen = CocoaPen(glyph.parent)
    glyph.draw(pen)
    return pen.path

def nsBezierOrgPathFactory(glyph):
    pen = CocoaPen(glyph.parent)
    glyph.draw(pen, drawOrg=True)
    return pen.path

def boundsFactory(glyph):
    pen = BoundsPen(glyph.parent)

    try:
        glyph.draw(pen)
    except Exception as e:
        print('%s for %s (%s)' %(e, glyph.name, type(glyph)))
        print(traceback.format_exc())

    return pen.bounds

def pointsFactory(glyph):
    points = []
    for contour in glyph.contours:
        points += contour.points
    return points

def intersectionsFactory(glyph, beam, canHaveComponent=False):
    # glyphSet, glyph, beam, canHaveComponent=True, italicAngle=0):
    from tnbits.model.toolbox.pens.beampen import BeamPen
    pen = BeamPen(glyph.parent, glyph, beam, canHaveComponent)
    glyph.draw(pen)
    return pen

import math
def italicizedPoint(x, y, angle):
    #math.tan(-angle*math.pi/180)*y, y
    return x - math.tan(math.radians(angle))*y, y

# Beziér paths.
addGlyphRepresentationFactory("defconAppKit.NSBezierPath", nsBezierPathFactory) # Compatible to RoboFont glyph path.
addGlyphRepresentationFactory("nsBezierPath", nsBezierPathFactory)  # XXX move to a module that does GUI stuff
addGlyphRepresentationFactory("nsBezierOrgPath", nsBezierOrgPathFactory)  # XXX move to a module that does GUI stuff

# Bounds.
addGlyphRepresentationFactory("bounds", boundsFactory)
addGlyphRepresentationFactory("defcon.glyph.bounds", boundsFactory)

# TODO: these should probably move to the module that needs them:
addGlyphRepresentationFactory("intersections", intersectionsFactory) # doodle.Beam
addGlyphRepresentationFactory("points", pointsFactory)

def _docTests():
    r"""
        >>> g = Glyph("a")
        >>> g.width
        500
        >>> g.nsBezierPath.elementCount()
        0
        >>> print(g.bounds)
        None
        >>> g.bounds = 12
        Traceback (most recent call last):
            ...
        AttributeError: can't set attribute
        >>> g.lalala = 12
        >>> g.lalala
        12
        >>> g.unicodes
        []
        >>> g.unicode = 97
        >>> g.unicode
        97
        >>> g.unicodes
        [97]
    """

def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
