
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     glyphset.py
#
import operator
from tnbits.qualityassurance.qamessage import addHeader, headerMessage

def count(stylesDict, referenceId=None, **kwargs):
    """Counts number of glyphs for each font -- in order to select a Reference
    font designers often need to get a peek at which selected styles have the
    most glyphs. Ordered high to low."""
    messages = []
    m = []
    d = {}

    for styleId, style in stylesDict.items():
        d[styleId] = len(style)

    sortedByLength = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    for t in sortedByLength:
        m.append('%s: %d glyphs' % t)

    addHeader("Count", None, m, messages)
    return messages

def unicodes(stylesDict, **kwargs):
    messages = []

    for styleId, style in stylesDict.items():
        values = []
        duplicates = []

        for glyphName in style.keys():
            glyph = style[glyphName]
            if glyph.unicode:
                u = glyph.unicode

                if u not in values:
                    values.append(u)
                else:
                    duplicates.append(u)

        for glyphName in sorted(style.keys()):
            glyph = style[glyphName]

            if glyph.unicode:
                u = glyph.unicode
                msg = '%s, %s' % (str(hex(u)), str(chr(u)))
                msg = ' + %s = %s' % (glyphName, msg)

                if u in duplicates:
                    msg = ('%s (duplicate)' % msg, 'error')
                else:
                    msg = (msg, 'plaintext')
            else:
                msg = (' - %s' % glyphName, 'warning')

            msg = ('%s\n' % msg[0], msg[1])
            messages.append(msg)

            if len(glyph.unicodes) > 0:
                refs = []
                error = False

                for u in glyph.unicodes:
                    refs.append(str(hex(u)))
                    if u != glyph.unicode and u in values:
                        error = True

                msg = '   > [%s]\n' % ', '.join(refs)

                if error:
                    msg = (msg, 'error')

                messages.append(msg)

    return messages

def compare(stylesDict, referenceId=None, **kwargs):
    """Compares all character sets from a batch of fonts and reports the
    differences. If there is a Current Font open, then this will be used as the
    Master reference; otherwise, a separate dialog will ask to have a Master
    reference selected. Results are printed to the Output window, and saved to
    a text file if one is specified. The format of the glyph lists in the
    result can be adjusted with the pythonList variable.  """
    messages = []

    if len(stylesDict) <= 1 or referenceId is None:
        m = []
        msg = ('Please select more than one style.', 'warning')
        m.append(msg)
        addHeader("Compare", None, m, messages)
        return messages

    referenceStyle = stylesDict[referenceId]
    referenceSet = set(referenceStyle.keys())

    if len(stylesDict) == 1:
        return []

    for styleId, style in stylesDict.items():
        # Skip the reference font.
        if styleId == referenceId:
            continue

        msg = 'Compare %s (%d glyphs)' % (styleId, len(style))
        messages.append(headerMessage(msg, 3))
        intro = 'Reference style = %s (%d glyphs)\n\n' % (referenceId, len(referenceStyle))
        messages.append(intro)
        m = []
        glyphSet = set(style.keys())

        # Gets the differences both ways.
        missingSet = list(referenceSet.difference(glyphSet))
        additionalSet = list(glyphSet.difference(referenceSet))

        if len(missingSet) > 0:
            missingList = list(sorted(missingSet))
            msg = 'Missing glyphs: %s' % ', '.join(missingList)
            m.append((msg, 'error'))

        if len(additionalSet) > 0:
            additionalList = list(sorted(additionalSet))
            msg = 'Additional glyphs: %s' % ', '.join(additionalList)
            m.append((msg, 'error'))

        if len(missingSet) == 0 and len(additionalSet) == 0:
            m.append(['same'])

        messages.append(m)

    #addHeader("Compare", None, m, messages, intro=intro)
    return messages
