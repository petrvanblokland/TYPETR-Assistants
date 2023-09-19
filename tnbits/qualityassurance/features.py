# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     features.py
#
from tnbits.qualityassurance.qamessage import addHeader

def missingGroupNames(stylesDict, **kwargs):
    """
    Checks if glyphs in groups  exist in the font.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []

        if not hasattr(style, 'groups'):
            msg = 'No groups in style'
            m.append((msg, 'error'))
            continue

        for groupName in style.groups.keys():
            for name in style.groups[groupName]:
                if not name in style:
                    msg = 'Glyph %s in Group %s does not exist' % (name, groupName)
                    m.append((msg, 'error'))

        addHeader("Missing Group Names", styleId, m, messages)

    return messages

def reportSuffixes(stylesDict, **kwargs):
    """
    Collects all suffixes.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        suffixes = []

        for glyphName in style.keys():
            g = style[glyphName]

            if '.' in g.name:
                suffix = g.name.split('.')[-1]
                suffix = '.' + suffix

                if suffix not in suffixes:
                    suffixes.append(suffix)

        if len(suffixes) > 0:
            suffixes.sort()
            m.append('Found suffixes:')
            m.append(suffixes)

        addHeader("Report Suffixes", styleId, m, messages)

    return messages
