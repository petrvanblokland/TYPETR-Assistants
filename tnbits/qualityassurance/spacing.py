# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     spacing.py
#

from tnbits.qualityassurance.qamath import getOffset, getSortedGlyphNames
from tnbits.model.objects.glyph import boundingBox
from tnbits.qualityassurance.qamessage import addHeader, headerMessage

def accentedWidths(stylesDict, ignoredNames=[], ignoredSubstrings=[],
        zeroWidthUnicodes=[], **kwargs):
    """Width analysis of accents.

    # Get a list of base glyphs.

    if reorderComponents:
        clearComponents(g)

        for h, baseGlyph, offset, scale in componentList:
            o = offset=(offset[0] * -1, offset[1] * -1)
            g.appendComponent(baseGlyph=baseGlyph, o, scale=scale)

    TODO: divide into smaller routines."""
    defaultMatrix = (1, 0, 0, 1)
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        widthMessages = []
        offsetMessages = []
        matrixMessages = []
        spaceCenterString = ''

        for glyphName in style.keys():
            g = style[glyphName]
            error = False
            match = False

            if g.name in ignoredNames:
                continue

            for substring in ignoredSubstrings:
                if substring in g.name:
                    match = True
                    break

            if match is True:
                continue

            # Compares components.
            if g.components:
                componentList = []

                # First look for components and put them in a list.
                for c in g.components:
                    if not c.baseGlyph in style.keys():
                        msg = 'Missing base glyph %s' % c.baseGlyph
                        widthMessages.append((msg, 'error'))
                        error = True
                        break

                    base = style[c.baseGlyph]
                    box = boundingBox(base)
                    h = box[3] - box[1]
                    offset = getOffset(c)
                    matrix = c.transformation[:4]

                    if matrix != defaultMatrix:
                        msg = 'Non-default matrix in %s: (%d, %d, %d, %d)' % (c.baseGlyph, matrix[0], matrix[1], matrix[2], matrix[3])
                        matrixMessages.append((msg, 'error'))

                    t = (h, c.baseGlyph, offset)
                    componentList.append(t)

                if error:
                    # No baseglyph could be found, continue to the next
                    # component.
                    continue

                componentList.sort()
                componentList.reverse()
                mainBaseGlyph = componentList[0][1]
                offset = componentList[0][2]
                baseWidth = style[mainBaseGlyph].width

                # Checks for zero width on some accents, else compare with
                # width of base.
                if g.name.endswith('cmb') or g.name.endswith('comb'):

                    # cmb should always be zero.
                    if g.width != 0:
                        msg = '%s width is %d (baseWidth %s), not zero.' % (g.name, g.width, baseWidth)
                        widthMessages.append((msg, 'error'))
                elif str(g.unicode) in zeroWidthUnicodes:
                    if g.width != 0:
                        msg = 'Unicode %s width is %d (baseWidth %s), not zero.' % (g.unicode, g.width, baseWidth)
                        widthMessages.append((msg, 'error'))

                elif g.width != baseWidth:
                    msg = '%s, w=%d, base width is %d' % (g.name, g.width, baseWidth)
                    widthMessages.append((msg, 'error'))
                    spaceCenterString += '/space/' + mainBaseGlyph + '/' + g.name

                if offset != (0, 0):
                    msg = '%s, offset is (%d, %d)' % (g.name, offset[0], offset[1])
                    offsetMessages.append((msg, 'warning'))

        # Compares width of dottlessi to i, dotlessj to j.

        compares = [('dotlessi', 'i'), ('dotlessj', 'j')]

        for pair in compares:
            (i, j) = pair

            if i in style.keys() and j in style.keys():
                if style[i].width != style[j].width:
                    msg = '%s, w=%d, %s, w=%d' % (i, style[i].width, j, style[j].width)
                    widthMessages.append((msg, 'error'))
                    spaceCenterString += '/space/' + i + '/' + j

        if len(widthMessages) > 0:
            m.append('Widths')
            m.append(widthMessages)

        if len(offsetMessages) > 0:
            # FIXME: header should not be shown if warnings are suppressed.
            m.append('Offsets')
            m.append(offsetMessages)

        if len(matrixMessages) > 0:
            m.append('Transformations')
            m.append(matrixMessages)

        if len(spaceCenterString) > 0:
            m.append('Space Center')
            m.append([spaceCenterString])

        addHeader("Accented Widths", styleId, m, messages)

    return messages

def getTabularGlyphs(style):
    """
    """
    suffixes = ('.tab', '.tf', '.tosf', '.ton', '.tin', '_tab', '.tnum', '.tonum')
    tabularGlyphs = []

    # First look for tabular figures.
    for glyphName in style.keys():
        g = style[glyphName]

        for suffix in suffixes:
            if suffix in g.name:
                tabularGlyphs.append(g.name)
                break

    return tabularGlyphs

def getTabularWidth(style, tabularGlyphs):
    """Determines the width to compare tabular glyphs to. Takes the glyph
    names found by getTabularGlyphs() as an argument."""
    message = None
    found = False
    g = None

    for glyphName in tabularGlyphs:
        if glyphName.startswith('zero.'):
            g = style[glyphName]
            found = True
            break

    if not found:
        for glyphName in style.keys():
            if glyphName.startswith('zero.t'):
                g = style[glyphName]
                found = True
                break

    if found:
        w = int(g.width)
    else:
        w = 650
        message = ('zero.tab not in font, setting source width to 650pt', 'warning')

    return w, message

def tabularWidths(stylesDict, **kwargs):
    """If present, compares widths of tabular figures againts zero.tab."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        tabularGlyphs = getTabularGlyphs(style)

        if len(tabularGlyphs) == 0:
            m.append('No glyphs with suffix denoting tabular figures.')
        else:
            tabularWidth, msg = getTabularWidth(style, tabularGlyphs)

            if msg is not None:
                m.append(msg)

            msg = 'Source width is %d, %d tabular glyphs' % (tabularWidth, len(tabularGlyphs))
            m.append((msg, 'highlight'))
            errors = []

            for gname in tabularGlyphs:
                g = style[gname]

                if round(g.width) != tabularWidth and round(g.width) != round(tabularWidth / 2):
                    msg = 'different width for %s: %d' % (g.name, g.width)
                    errors.append((msg, 'error'))

            m.append(errors)

        addHeader("Tabular Widths", styleId, m, messages)

    return messages

def compareTabularWidths(stylesDict, referenceId=None, **kwargs):
    """Compares widths of tabular glyphs across styles."""
    messages = []

    if len(stylesDict) <= 1 or referenceId is None:
        msg = ('Please select more than one style.', 'warning')
        m = []
        m.append(msg)
        addHeader("Compare Tabular Widths", None, m, messages)
        return messages

    referenceStyle = stylesDict[referenceId]
    referenceSet = set(referenceStyle.keys())
    referenceTabularGlyphs = getTabularGlyphs(referenceStyle)
    tabularWidths = {}
    tabularGlyphsDict = {}
    msg = 'Compare Tabular Widths %s (%s reference tabular glyphs)' % (referenceId, len(referenceTabularGlyphs))
    messages.append(headerMessage(msg, 3))
    m = []

    # List tabularWidth.

    for styleId, style in stylesDict.items():
        tabularGlyphs = getTabularGlyphs(style)
        tabularWidth, _ = getTabularWidth(style, tabularGlyphs)

        if not tabularWidth in tabularWidths:
            tabularWidths[tabularWidth] = []

        # Store values for faster lookup during second loop.
        tabularWidths[tabularWidth].append(styleId)
        tabularGlyphsDict[styleId] = tabularGlyphs


    for w in sorted(tabularWidths.keys()):
        m.append('%d: %s' % (w, ', '.join(tabularWidths[w])))

    messages.append(m)

    for styleId, style in stylesDict.items():
        # Skip the reference font.
        if styleId == referenceId:
            continue

        tabularGlyphs = tabularGlyphsDict[styleId]
        msg = 'Compare Tabular Widths %s (%d tabular glyphs)' % (styleId, len(tabularGlyphs))
        messages.append(headerMessage(msg, 3))
        mismatch = []
        missing = []
        m = []

        for glyphName in referenceTabularGlyphs:
            if glyphName in tabularGlyphs:
                rg = referenceStyle[glyphName]
                g = style[glyphName]

                if rg.width != g.width:
                    mismatch.append((glyphName, g.width, rg.width))
            else:
                missing.append(glyphName)

        if len(mismatch) > 0:
            msg = 'Mismatches:'

            for mm in mismatch:
                msg += ' %s: %d (ref: %d)' % mm

            m.append((msg, 'error'))

        if len(missing) > 0:
            msg = 'Missing: %s' % ', '.join(missing)
            m.append((msg, 'error'))

        if len(mismatch) == 0 and len(missing) == 0:
            m.append('same')

        messages.append(m)

    return messages

def controlSidebearings(stylesDict, attrs=None, **kwargs):
    """Checks sidebearings for control glyphs passed throught glyphNames.
    Returns a summary as a list of messages.

    NOTE: this is just a report for human interpretation, we don't look for
    errors or warnings here."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        for gname in attrs:
            if gname not in style.keys():
                msg = 'Glyph %s not in font' % gname
            else:
                g = style[gname]
                lineType = 'plaintext'

                if g.leftMargin is None or g.rightMargin is None:
                    msg = 'Missing margin in %s' % gname
                else:
                    msg = '%s: (%s, %s)' % (gname, g.leftMargin, g.rightMargin)

            m.append(msg)

        addHeader("Control Sidebearings", styleId, m, messages)

    return messages

def getNegativeSidebearingsIgnore(gname, attrs):
    """Checks if glyph should be ignored by negativeSidebearings()."""
    ignore = False
    gnl = gname.lower()

    # substrings.

    for attr in attrs:
        # Tuple passes exception substrings.
        if isinstance(attr, tuple):
            substring, exceptions = attr

            if substring in gnl:
                found = False

                for exception in exceptions:
                    if exception in gnl:
                        found = True
                        break

                if not found:
                    ignore = True

                break

        # Strings, no exceptions.
        elif isinstance(attr, str):
            if attr in gnl:
                ignore = True
                break

    # Ends / starts with.

    if gnl.endswith('cmb') or gnl.startswith('uni') or gnl.startswith('afii'):
        ignore = True

    return ignore

def negativeSidebearings(stylesDict, attrs=None, **kwargs):
    """Checks if sidebearings are negative for given glyph names.
    Returns a summary as a list of messages."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for glyphName in style.keys():
            ignore = getNegativeSidebearingsIgnore(glyphName, attrs)

            if ignore:
                continue

            g = style[glyphName]

            if g.leftMargin and g.leftMargin < 0:
                msg = '%s %s, %s' % (glyphName, g.leftMargin, g.rightMargin)
                m.append(msg)

            if g.rightMargin and g.rightMargin < 0:
                msg = '%s %s, %s' % (glyphName, g.leftMargin, g.rightMargin)
                m.append(msg)

        m = sorted(m)

        addHeader("Negative Sidebearings", styleId, m, messages)

    return messages

def symmetricalSidebearings(stylesDict, attrs=None, **kwargs):
    """Looks if left and right sidebearings are equal for given glyph names.
    Filters if the difference is two points or larger. i.e. more than 1 units.

    Returns a summary as a list of messages."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for gname in attrs:
            if gname not in style.keys():
                msg = 'Glyph %s not in font' % gname
            else:
                g = style[gname]
                error = False

                if g.leftMargin is None or g.rightMargin is None:
                    msg = 'Missing margin in %s' % gname
                    error = True
                else:
                    msg = '%s: (%s, %s)' % (gname, g.leftMargin, g.rightMargin)

                    if abs(g.leftMargin - g.rightMargin) > 1:
                        error = True

                if error is True:
                    lineType = 'error'
                else:
                    lineType='warning'

                m.append((msg, lineType))

        addHeader("Symmetrical Sidebearings", styleId, m, messages)

    return messages

def spacingGroups(stylesDict, attrs=None, **kwargs):
    """Compares sidebearings for given glyph names. Returns a summary as a
    list of messages."""
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        for target, left, right in attrs:
            if target in style.keys() and left in style.keys() and right in style.keys():
                t = style[target]
                l = style[left]
                r = style[right]
                msgLeft = None
                msgRight = None

                if t.leftMargin != l.leftMargin:
                    msgLeft = ' %s (%s, %s)' % (left, t.leftMargin, l.leftMargin)

                if t.rightMargin != r.rightMargin:
                    msgRight = ' %s (%s, %s)' % (right, r.rightMargin, t.rightMargin)

                if msgLeft is not None or msgRight is not None:
                    msg = '%s (%s, %s)' % (target, t.leftMargin, t.rightMargin)

                    if msgLeft:
                        msg += msgLeft
                    if msgRight:
                        msg += msgRight

                    m.append((msg, 'error'))
            else:
                msg = 'unable to process %s' % target
                m.append((msg, 'warning'))

        addHeader("Spacing Groups", styleId, m, messages)

    return messages
