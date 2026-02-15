# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_AZ_set.py
#    Smallest A-Za-z for initial or final kerning testing
##
#    Latin “Ascii” (Smallest set accorting to Monotype)
#    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
#
from copy import deepcopy

if __name__ == '__main__': # Used for doc tests to find assistantLib
    import os, sys
    PATH = '/'.join(__file__.split('/')[:-4]) # Relative path to this respository that holds AssistantLib
    if not PATH in sys.path:
        sys.path.append(PATH)

from assistantLib.assistantParts.glyphsets.glyphData import *
from assistantLib.assistantParts.glyphsets.anchorData import AD

# Values to be implemented by MasterData for each master
#MIN_MARGIN = 24
#EM_WIDTH = 1000
#EN_WIDTH = int(EM_WIDTH/2)
#SPACE_WIDTH = int(EM_WIDTH/5)
#FIGURE_WIDTH = 650 # 1265 for Segoe UI 2048-EM
#ACCENT_WIDTH = FIGURE_WIDTH/2
#FRACTION_WIDTH = FIGURE_WIDTH/4
#HAIR_WIDTH = int(EM_WIDTH/8)
#MOD_MIN = 48 # Constant margin for some superior and unferiot glyphs

LATIN_AZ_SET_NAME = 'Latin AZ'
LATIN_AZ_SET_NAME_ITALIC = 'Latin AZ Italic'

# The "c" attributes are redundant, if the @uni or @hex are defined, but they are offer easy searching in the source by char.
LATIN_A_SET = GDS = {

    '.notdef': GD(name='.notdef'),
    '.null': GD(name='.null', uni=0x0000, hex='0000'),
    'space': GD(name='space', uni=0x0020, hex='0020', w=GD.CAT_SPACE_WIDTH, c=' ', isLower=False, comment='  Symbols, ASCII Punctuation and'),

    'A': GD(name='A', uni=0x0041, hex='0041', c='A', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='A Uppercase Alphabet, Latin'),
    'B': GD(name='B', uni=0x0042, hex='0042', c='B', l='H', anchors=['bottom', 'middle', 'top'], comment='B LATIN CAPITAL LETTER B'),
    'C': GD(name='C', uni=0x0043, hex='0043', c='C', l='O', anchors=['bottom', 'dot', 'middle', 'top'], comment='C LATIN CAPITAL LETTER C'),
    'D': GD(name='D', uni=0x0044, hex='0044', c='D', l='H', r='O', anchors=['bottom', 'middle', 'top'], comment='D'),
    'E': GD(name='E', uni=0x0045, hex='0045', c='E', l='H', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='E'),
    'F': GD(name='F', uni=0x0046, hex='0046', c='F', l='H', anchors=['bottom', 'middle', 'top'], comment='F'),
    'G': GD(name='G', uni=0x0047, hex='0047', c='G', l='O', anchors=['bottom', 'middle', 'top'], comment='G'),
    'H': GD(name='H', uni=0x0048, hex='0048', c='H', l2r='self', anchors=['bottom', 'middle', 'top', 'topleft'], comment='H'),
    'I': GD(name='I', uni=0x0049, hex='0049', c='I', l='H', r='H', srcName='H', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='I'),
    'J': GD(name='J', uni=0x004A, hex='004A', c='J', anchors=['bottom', 'middle', 'top'], comment='J'),
    'K': GD(name='K', uni=0x004B, hex='004B', c='K', l='H', anchors=['bottom', 'middle', 'top'], comment='K'),
    'L': GD(name='L', uni=0x004C, hex='004C', c='L', l='H', anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='L'),
    'M': GD(name='M', uni=0x004D, hex='004D', c='M', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='M'),
    'N': GD(name='N', uni=0x004E, hex='004E', c='N', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='N'),
    'O': GD(name='O', uni=0x004F, hex='004F', c='O', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='O'),
    'P': GD(name='P', uni=0x0050, hex='0050', c='P', l='H', anchors=['bottom', 'middle', 'top', 'topleft'], comment='P'),
    'Q': GD(name='Q', uni=0x0051, hex='0051', c='Q', l='O', w='O', anchors=['bottom', 'middle', 'top'], comment='Q'),
    'R': GD(name='R', uni=0x0052, hex='0052', c='R', bl='H', anchors=['bottom', 'middle', 'top'], comment='R'),
    'S': GD(name='S', uni=0x0053, hex='0053', c='S', l2r='self', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='S'),
    'T': GD(name='T', uni=0x0054, hex='0054', c='T', l2r='self', anchors=['bottom', 'middle', 'top'], comment='T'),
    'U': GD(name='U', uni=0x0055, hex='0055', c='U', l='off', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='U'),
    'V': GD(name='V', uni=0x0056, hex='0056', c='V', l='A', r='A', anchors=['bottom', 'middle', 'top'], comment='V'),
    'W': GD(name='W', uni=0x0057, hex='0057', c='W', l='V', r='V', anchors=['bottom', 'middle', 'top'], comment='W'),
    'X': GD(name='X', uni=0x0058, hex='0058', c='X', l2r='self', anchors=['bottom', 'middle', 'top'], comment='X'),
    'Y': GD(name='Y', uni=0x0059, hex='0059', c='Y', l2r='self', anchors=['bottom', 'middle', 'top', 'topleft'], comment='Y'),
    'Z': GD(name='Z', uni=0x005A, hex='005A', c='Z', l2r='self', anchors=['bottom', 'middle', 'top'], comment='Z'),
    'a': GD(name='a', uni=0x0061, hex='0061', c='a', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='a Small Letters, Latin'),
    'b': GD(name='b', uni=0x0062, hex='0062', c='b', l='off', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='b'),
    'c': GD(name='c', uni=0x0063, hex='0063', c='c', isLower=True, anchors=['bottom', 'dot', 'middle', 'top'], comment='c'),
    'd': GD(name='d', uni=0x0064, hex='0064', c='d', isLower=True, anchors=['bottom', 'middle', 'top', 'vert'], comment='d'),
    'e': GD(name='e', uni=0x0065, hex='0065', c='e', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='e'),
    'f': GD(name='f', uni=0x0066, hex='0066', c='f', l='t', rightMin='-100', isLower=True, anchors=['bottom', 'middle', 'top'], comment='f'),
    'g': GD(name='g', uni=0x0067, hex='0067', c='g', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g'),
    'h': GD(name='h', uni=0x0068, hex='0068', c='h', isLower=True, anchors=['bottom', 'dot', 'middle', 'top'], comment='h'),
    'i': GD(name='i', uni=0x0069, hex='0069', c='i', l='n', r='idotless', base='idotless', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='i'),
    'j': GD(name='j', uni=0x006A, hex='006A', c='j', l='off', r='off', isLower=True, anchors=['bottom', 'middle'], comment='j'),
    'k': GD(name='k', uni=0x006B, hex='006B', c='k', l='h', r='x', isLower=True, anchors=['bottom', 'middle', 'top'], comment='k'),
    'l': GD(name='l', uni=0x006C, hex='006C', c='l', l='h', r='idotless', isLower=True, anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='l'),
    'm': GD(name='m', uni=0x006D, hex='006D', c='m', l='n', r='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='m'),
    'n': GD(name='n', uni=0x006E, hex='006E', c='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='n'),
    'o': GD(name='o', uni=0x006F, hex='006F', c='o', l2r='self', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='o'),
    'p': GD(name='p', uni=0x0070, hex='0070', c='p', l='n', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='p'),
    'q': GD(name='q', uni=0x0071, hex='0071', c='q', l='o', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='q'),
    'r': GD(name='r', uni=0x0072, hex='0072', c='r', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='r'),
    's': GD(name='s', uni=0x0073, hex='0073', c='s', l='off', l2r='self', isLower=True, useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='s'),
    't': GD(name='t', uni=0x0074, hex='0074', c='t', l='off', r='off', isLower=True, anchors=['bottom', 'middle', 'top', 'vert'], comment='t'),
    'u': GD(name='u', uni=0x0075, hex='0075', c='u', l2r='n', r2l='n', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='u'),
    'v': GD(name='v', uni=0x0076, hex='0076', c='v', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='v LATIN SMALL LETTER V'),
    'w': GD(name='w', uni=0x0077, hex='0077', c='w', l='v', r='v', isLower=True, anchors=['bottom', 'middle', 'top'], comment='w LATIN SMALL LETTER W'),
    'x': GD(name='x', uni=0x0078, hex='0078', c='x', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='x LATIN SMALL LETTER X'),
    'y': GD(name='y', uni=0x0079, hex='0079', c='y', l='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='y LATIN SMALL LETTER Y'),
    'z': GD(name='z', uni=0x007A, hex='007A', c='z', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='z LATIN SMALL LETTER Z')
}

# Make exceptions for Italic glyphs and spacing rules
LATIN_AZ_SET_ITALIC = GDSI = deepcopy(LATIN_AZ_SET)

if __name__ == '__main__':
    for gName, gd in GDS.items():
        #print('---', gd)
        if gd.base and gd.base not in GDS:
            print('##### Missing base', gName, gd.base)
        for aName in gd.accents:
            if aName not in GDS:
                print('#### Missing accent', gName, aName)

    for gName, gd in GDS.items():
        if len(gd.accents) >= 2:
            print(gName, gd.accents)

    chars = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789¹²³ªº
        %$€¥£¢&*@#|áâàäåãæçéêèëíîìïıñóôòöõøœšßúûùüýÿžÂÀÄÅÃÆÇÉÊÈËÍÎÌÏÑÓÔÒÖÕØŒŠÛÙÜÝŸ
        ,:;-–—•.…“‘’‘ ‚ “”„‹›«»/\\?!¿¡()[]{}©®§+×=_°
    """
    names = []
    for gName, gd in GDS.items():
        if gd.uni and chr(gd.uni) in chars:
            names.append(gd.asSourceLine())

    #print(''.join(names))


