# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     fontinfo.py
#

from tnbits.qualityassurance.qamessage import addHeader

def getFontInfoDict(style, attrs=None, **kwargs):
    """
    Tries to get all attribute values from font info, sets to None if fails.
    NOTE: doesn't find OS/2 values yet for TTF / OTF.
    """
    fontInfoDict = {}

    for attr in attrs:
        value = None

        try:
            value = getattr(style.info, attr)
        except Exception as e:
            print(e)

        fontInfoDict[attr] = value

    return fontInfoDict

def verticalMetrics(stylesDict, attrs=None, referenceId=None, **kwargs):
    """
    Gives a summary of embedded font info. Some analytics:

    * compares cap heights before doing font info and adds an error to
    message output for wrong cap heights,
    * looks if cap height is smaller than ascender,
    * looks if ascender plus descender equals units per em.
    """
    messages = []
    capHeightMatches = {}
    ascenderMatches = {}
    descenderMatches = {}
    referenceHeight = None

    # If there's a reference, i.e. there are multiple fonts, stores cap height,
    # ascender and descender for comparison in next loop.

    if referenceId:
        referenceStyle = stylesDict[referenceId]
        referenceHeight = referenceStyle.info.capHeight
        referenceAscender = referenceStyle.info.ascender
        referenceDescender = referenceStyle.info.descender

        for styleId, style in stylesDict.items():
            if styleId == referenceId:
                continue

            c = style.info.capHeight
            a = style.info.ascender
            d = style.info.descender

            if c != referenceHeight:
                capHeightMatches[styleId] = False
            else:
                capHeightMatches[styleId] = True

            if a != referenceAscender:
                ascenderMatches[styleId] = False
            else:
                ascenderMatches[styleId] = True

            if d != referenceDescender:
                descenderMatches[styleId] = False
            else:
                descenderMatches[styleId] = True

    # Compiles results for all styles.

    for styleId, style in stylesDict.items():
        m = []
        d = getFontInfoDict(style, attrs)
        ascDescSum = style.info.ascender - style.info.descender
        lineType = 'plaintext'

        # Note the difference:

        m.append('Family Name: %s' % d['familyName'])
        m.append('Style Name: %s' % d['styleName'])
        m.append('Style Map Family Name: %s' % d['styleMapFamilyName'])

        # Ascender matches reference.

        msg = 'Ascender: %s' % d['ascender']

        if styleId in ascenderMatches:
            if ascenderMatches[styleId] is False:
                msg += u' (🚫 ascender mismatch)'
                m.append((msg, 'error'))
            else:
                m.append(msg)
        else:
            # Is reference.
            m.append(msg)

        # Descender matches reference.

        msg = 'Descender: %s' % d['descender']

        if styleId in descenderMatches:
            if descenderMatches[styleId] is False:
                msg += u' (🚫 descender mismatch)'
                m.append((msg, 'error'))
            else:
                m.append(msg)
        else:
            # Is reference.
            m.append(msg)

        # Units per Em equals ascender plus descender.

        msg = 'Units Per Em: %s' % d['unitsPerEm']

        if ascDescSum == style.info.unitsPerEm:
            d['ascDescMatch'] = 'ok'
            msg +=  ' (asc / desc match)'
            m.append(msg)
        else:
            msg += u' (🚫 asc/desc mismatch)'
            m.append((msg, 'error'))

        # Cap height matches reference and smaller than ascender.

        msg = 'Cap Ht: %s' % d['capHeight']
        capError = False

        if styleId in capHeightMatches:
            if capHeightMatches[styleId] is False:
                capError = True
                msg += u' (🚫 height mismatch)'

        if style.info.capHeight < style.info.ascender:
            msg += ' (< asc)'
        else:
            msg += u' (🚫 greater than/equal to ascender)'
            capError = True

        if capError is True:
            m.append((msg, 'error'))
        else:
            m.append(msg)

        # Italic angle larger than zero if name containts 'It'.

        m.append('x-height: %s' % d['xHeight'])
        parts = styleId.split('-')

        if len(parts) > 1:
            if 'It' in parts[-1] and float(d['italicAngle']) >= 0.0:
                lineType = 'error'

        m.append(('Italic Angle: %s' % d['italicAngle'], lineType))
        m.append('Copyright: %s' % d['copyright'])
        addHeader("Vertical Metrics", styleId, m, messages)

    return messages

def checkOS2Values(stylesDict, attrs=None, **kwargs):
    """
    For now just reports all OS/2 fields in font info. See also #83.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m = []
        fontInfoDict = getFontInfoDict(style, attrs)

        for key, value in fontInfoDict.items():
            if 'OS2' in key:
                msg = '%s: %s' % (key, value)
                m.append(msg)

        addHeader("Check OS/2 Values", styleId, m, messages)

    return messages
