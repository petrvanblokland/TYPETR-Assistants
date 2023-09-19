# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    glyphs.py
#


GLYPHNAME_SUFFIXORDER = ['numr', 'dnom', 'uc', 'lc', 'sc', 'smcp', 'nc', 'pc',
        'tab', 'tnum', 'thin', 'em', 'en', 'prop', 'pnum', 'onum', 'lnum',
        'sups', 'sinf', 'ordn', 'subs', 'isol', 'init', 'medi', 'fina', 'alt',
        'salt', 'calt', 'swsh', 'unic', 'long', 'short', 'n', 'nw', 'w', 's',
        'se', 'e', 'ne']

GLYPHNAME_ALLOWEDCHARS = ['.', '_'] + [chr(gName) for gName in range(48,58)] + [chr(gName) for gName in range(65,91)] + [chr(gName) for gName in range(97,123)]
GLYPHNAME_NOTFIRSTCHARS = ['.'] + [chr(gName) for gName in range(48,58)]
