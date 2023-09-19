# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    transformer.py
#

def isAFormatOf(styleId, formats):
    for f in formats:
        if isFormat(styleId, f):
            return True

    return False

def isFormat(styleId, f):
    """Looks if extension is of format f."""
    if styleId.lower().endswith('.%s' % f):
        return True

def isUFO(styleId):
    """Looks at the extension to see if this is a UFO."""
    # DEPRECATED.
    if styleId.lower().endswith('.ufo'):
        return True

    return False

def isAcceptedBinary(styleId):
    # DEPRECATED.
    """Looks at the extension to see if binary format is supported."""
    if styleId.lower().endswith('.ttf'):
        return True
    elif styleId.lower().endswith('.otf'):
        return True
    elif styleId.lower().endswith('.woff'):
        return True

    return False

