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

def upperFirst(s):
    return s[0].upper() + s[1:]

def getFlagName(category, functionName):
    if category is not None:
        return '_' + category + 'Do' + upperFirst(functionName)
    else:
        return '_do' + upperFirst(functionName)

