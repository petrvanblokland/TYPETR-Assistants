# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     qamessage.py
#


"""
Functions for message formatting.
"""

def addHeader(functionName, styleId, m, messages, intro=None):
    """
    Adds a header message with style ID in it and pastes it before the
    messages list.
    """
    if len(m) > 0:
        h = getHeader(functionName, styleId)
        messages.append(headerMessage(h, 3))

        if intro is not None:
            messages.append(intro + '\n\n')

        messages.append(m)
    else:
        h = getHeader(functionName, styleId)
        messages.append(headerMessage(h, 3))
        messages.append('OKAY\n')

def getTitle(name):
    h = name[0].upper()

    for i, c in enumerate(name[1:]):
        if c.isupper():
            if not name[i].isupper():
                h += ' ' + c
            else:
                h += c
        else:
            h += c

    return h

def getHeader(functionId, styleId=None):
    h = getTitle(functionId)
    if styleId is not None:
        h = h + ' ' + styleId

    return h

def headerMessage( msg, level=1):
    """
    Formats header messages by adding markdown hash levels.
    """
    r = '\n'
    msg = '%s%s %s%s%s' % (r, level * '#', msg, r, r)
    return (msg, 'header')

def printKernsAndGroups(style):
    """For verbose kerns and groups. NOTE: very slow."""
    print(len(style.kerning))

    for pair in style.kerning.keys():
        print(pair, style.kerning[pair])

    print(len(style.groups))

    for group in style.groups.keys():
        print(group, style.groups[group])

