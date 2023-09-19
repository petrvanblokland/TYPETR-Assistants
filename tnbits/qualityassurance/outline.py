# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     outline.py
#

from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.qualityassurance.qamath import getSortedGlyphNames, lineIntersection, isBetween
from tnbits.qualityassurance.qamessage import addHeader, getHeader, headerMessage
from tnbits.qualityassurance.bezierpoint import BezierPoint
from tnbits.model.objects.glyph import boundingBox, contourIsOpen

def verticalSizeReport(stylesDict, capGlyphs=None, descGlyphs=None, referenceId=None, **kwargs):
    """Compares control glyph vertical sizes to cap height and descender
    values."""
    messages = []

    for styleId, style in stylesDict.items():
        h = getHeader("Vertical Size Report", styleId)
        messages.append(headerMessage(h, 3))
        sa = analyzerManager.getStyleAnalyzer(style=style)
        capHeight = style.info.capHeight
        m = []

        if capHeight is None:
            m.append(('No cap height', 'error'))
        else:
            m.append('Cap height value is %d' % capHeight)
            mm = []

            for glyphName in capGlyphs:
                ga = sa[glyphName]
                bb = ga.boundingBox
                h = bb[-1]

                if h is None:
                    msg = ('No bounding box height', 'error')
                else:
                    diff = capHeight - h
                    msg = '%s: %d (diff = %d)' % (glyphName, h, diff)
                    if diff < 0:
                        msg = (msg, 'highlight')

                mm.append(msg)

            m.append(mm)

        desc = style.info.descender

        if desc is None:
            m.append(('No descender', 'error'))
        else:
            m.append('Descender value is %d' % desc)
            mm = []

            for glyphName in descGlyphs:
                ga = sa[glyphName]
                bb = ga.boundingBox
                l = bb[1]

                if l is None:
                    msg = ('No bounding box lower', 'error')
                else:
                    msg = '%s: %d (diff = %d)' % (glyphName, l, l - desc)

                mm.append(msg)

            m.append(mm)

        messages.append(m)

    return messages

def findOpenContours(stylesDict, **kwargs):
    """
    Finds open contours in style glyphs.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for glyphName in style.keys():
            g = style[glyphName]
            isOpen = False

            for ci, c in enumerate(g):
                if styleId.endswith('.ufo'):
                    if c.open:
                        isOpen = True
                else:
                    if contourIsOpen(c):
                        isOpen = True

                if isOpen:
                    msg = '%s has open contour %s' % (g.name, ci)
                    m.append((msg, 'error'))

        addHeader("Find Open Contours", styleId, m, messages)

    return messages

def compareContourOrder(stylesDict, **kwargs):
    """Compares contour lengths of same glyphs in different fonts to check if they are different."""
    messages = []
    d = {}

    for styleId, style in stylesDict.items():
        for glyphName in style.keys():
            glyph = style[glyphName]

            if glyphName not in d.keys():
                d[glyphName] = {}

            for i, c in enumerate(glyph):
                if i not in d[glyphName]:
                    d[glyphName][i] = len(c)
                else:
                    if len(c) != d[glyphName][i]:
                        msg = 'Contour mismatch for %s in %s, lenght is %d, should be %d\n' % (glyphName, styleId, len(c), d[glyphName][i])
                        messages.append((msg, 'error'))

    #addHeader("Compare Contour order", styleId, m, messages)
    return messages


def findMissingComponents(stylesDict, fix=False, **kwargs):
    """
    Removes missing components in a style. Returns a summary as a list
    of messages.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for glyphName in style.keys():
            g = style[glyphName]
            for c in g.components:
                if not c.baseGlyph in style:
                    m = []
                    msg = 'Missing component in glyph %s: %s' % (g.name, c.baseGlyph)
                    m.append((msg, 'error'))
                    # TODO: optionally repair, see #187.
                    #g.removeComponent(c)

        addHeader("Find Missing Components", styleId, m, messages)

    return messages

def controlOvershoots(stylesDict, **kwargs):
    """
    Checks if there are overshoots in the style.  Returns a summary as
    a list of messages.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for gname in ['O', 'o']:
            if gname.lower() == gname:
                heightCompare = style.info.xHeight
            else:
                heightCompare = style.info.capHeight

            g = style[gname]
            box = boundingBox(g)
            msg = '%s %s %s' % (gname, box[1], box[3] - heightCompare)
            m.append(msg)

        addHeader("Control Overshoots", styleId, m, messages)

    return messages

def crossingHandles(stylesDict, **kwargs):
    """
    Checks if Bézier handles cross eachother.

    Uses a BezierPoint class similar to bPoint in RoboFabWrapper so it
    doesn't depend on NSDocument and can be used separately from the GUI
    for the standalone application.

    FIXME: adapt to new signature.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        #glyphOrder = getSortedGlyphNames(style)

        #for glyphName in glyphOrder:
        for glyphName in style.keys():
            #if glyphName in style:
            g = style[glyphName]

            for c in g:
                bezierPoints = []

                if hasattr(c, 'naked'):
                    c = c.naked()

                if c.onCurvePoints:
                    for point in c.onCurvePoints:
                        bezierPoint = BezierPoint(obj=point, contour=c)
                        bezierPoints.append(bezierPoint)

                if len(bezierPoints) > 0:
                    previousAnchor = bezierPoints[-1].anchor
                    previousBCP = bezierPoints[-1].anchor[0] + bezierPoints[-1].bcpOut[0], bezierPoints[-1].anchor[1] + bezierPoints[-1].bcpOut[1]

                    for b in bezierPoints:
                        anchor = b.anchor
                        bcp = b.anchor[0] + b.bcpIn[0], b.anchor[1] + b.bcpIn[1]
                        result = lineIntersection((previousAnchor, previousBCP), (anchor, bcp))

                        if result and isBetween(previousAnchor, result, previousBCP) and isBetween(anchor, result, bcp):
                            msg = 'handles crossing for %s %s (index is %d)' % (glyphName, result, b.getIndex())
                            m.append((msg, 'error'))

                        previousAnchor = anchor
                        previousBCP = b.anchor[0] + b.bcpOut[0], b.anchor[1] + b.bcpOut[1]

        addHeader("Crossing Handles", styleId, m, messages)

    return messages

def findDuplicateComponents(stylesDict, fix=False, **kwargs):
    """
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for glyphName in style.keys():
            g = style[glyphName]
            componentList = []

            for c in g.components:
                #offset = qamath.getOffset(c)
                t = (c.baseGlyph, c.transformation)

                if t in componentList:
                    msg = 'Found duplicate %s: %s' % (g.name, t)
                    m.append((msg, 'error'))
                    '''
                    if fix:
                        g.removeComponent(c)
                        g.mark = 120
                    '''
                else:
                    componentList.append(t)

            '''
            if fix:
                g.clearComponents()

                for baseGlyph, offset, scale in componentList:
                    g.appendComponent(baseGlyph, offset, scale)
            '''
        addHeader("Find Duplicate Components", styleId, m, messages)

    return messages
