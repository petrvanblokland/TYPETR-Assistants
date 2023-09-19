#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    g.py
#

import re
from tnbits.constants import Constants

class Globals(object):
    C = Constants

    i = 0
    VERBOSE = 'verbose'
    RULER = '-' * 80
    DOTRULER = '.' * 80
    TAB = '\t'

    # Separate the tokens into (<VTTmnemonic>, <comment>, <number>, <partOfFree>)
    SRC2TOKEN = re.compile(r'[,\s]*([A-Za-z][A-Za-z0123]*\[[A-Za-z0-9\<\>\s]*\])|(/\*.*?\*/)|([0-9\-]+[,\s]*)|([a-z]+[a-z0-9]*)[,\s]*', re.DOTALL)
    STRIPCOMMENT = re.compile('/\*(.*)\*/', re.DOTALL)

    test1 = '''
        NPUSHB[ ]  /* 13 values pushed */ 34 0 71 0 7 20 20 5 29 2 7 13 40
        SVTCA[0]
        SRP0[ ]
        MDRP[00100]
        SHP[0]
        MIRP[00100]
        SHP[0]
        SVTCA[1]
        SHP[1]
        MDAP[1]
        SHP[1]
        SHP[1]
        SROUND[]
        MDAP[1]
        SHP[1]
        IUP[0]
        IUP[1]
        '''

    test2 = '''
        PUSHB[] 12 32 34 45 56
        CALL[]
        SVTCA[1]
        SVTCA[0]
        MDRP[01001] /* Both formats allowed */
        MDRP[m>rBl]
        PUSHB[] 23 34 45 56
        LOOPCALL[]
        PUSHB[] 56 67 78
        LOOPCALL[]
        '''

