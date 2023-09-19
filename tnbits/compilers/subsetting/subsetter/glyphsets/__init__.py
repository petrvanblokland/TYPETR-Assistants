# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
from tnbits.compilers.subsetting.subsetter.glyphsets import glyphsetArabic, glyphsetCyrillic, glyphsetEastEuropean, \
    glyphsetGreek, glyphsetHebrew, glyphsetKazakh, glyphsetThai, glyphsetVietnamese, glyphsetWestEuropean,\
    glyphsetAsciiPlus, glyphsetLatin1, glyphsetLatinExtended

MS_ARABIC = 'MS Arabic'
MS_CYRILLIC = 'MS Cyrillic'
MS_EASTEUROPEAN = 'MS E-Europe'
MS_GREEK = 'MS Greek'
MS_HEBREW = 'MS Hebrew'
MS_KAZAKH = 'MS Kazakh'
MS_THAI = 'MS Thai'
MS_VIETNAMESE = 'MS Vietnamese'
MS_WESTEUROPEAN = 'MS W-Europe'
FB_ASCIIPLUS = 'FB AsciiPlus'
FB_LATIN1 = 'FB Latin1'
FB_LATINEXTENDED = 'FB LatinExt'

GLYPHSETS = {
    MS_ARABIC: glyphsetArabic.glyphset,
    MS_CYRILLIC: glyphsetCyrillic.glyphset,
    MS_EASTEUROPEAN: glyphsetEastEuropean.glyphset,
    MS_GREEK: glyphsetGreek.glyphset,
    MS_HEBREW: glyphsetHebrew.glyphset,
    MS_KAZAKH: glyphsetKazakh.glyphset,
    MS_THAI: glyphsetThai.glyphset,
    MS_VIETNAMESE: glyphsetVietnamese.glyphset,
    MS_WESTEUROPEAN: glyphsetWestEuropean.glyphset,
    # FB sets
    FB_ASCIIPLUS: glyphsetAsciiPlus.glyphlist, # List for now, not a dictionary
    FB_LATIN1: glyphsetLatin1.glyphlist, # List for now, not a dictionary
    FB_LATINEXTENDED: glyphsetLatinExtended.glyphlist, # List for now, not a dictionary
}
SCRIPTLANGUAGES = {
    MS_ARABIC: {
        'DFLT': ('*',),
        'arab': ('ARA', 'MLY', 'MOR', 'SND', 'URD'),
        'cyrl': ('dflt',), 
        'grek': ('dflt',),
        'hebr': ('dflt',), # In model Regular, SemiLight. Not in model Bold, Light, Semibold, 
        'latn': ('dflt', 'TRK'),
    },
    MS_CYRILLIC: {
        'DFLT': ('*',),
        'cyrl': ('dflt', 'MKD', 'SRB'), # 'MKD', 'SRB' in model Bold-Italic
        'latn': ('dflt', 'TRK'),
    },
    MS_EASTEUROPEAN: {
        'DFLT': ('*',),
        'latn': ('dflt', 'TRK'),
    },
    MS_GREEK: {
        'DFLT': ('*',),
        'grek': ('dflt',),
        'latn': ('dflt', 'TRK'),
    },
    MS_HEBREW: {
        'DFLT': ('*',),
        'hebr': ('dflt',), # Not in model Bold, Semibold
        #'latn': ('dflt', 'TRK'),
    },
    MS_THAI: {
        'DFLT': ('*',),
        'thai': ('dflt'),
    },
    MS_VIETNAMESE: {
        'DFLT': ('*',),
        'latn': ('dflt', 'TRK'),
    },
    MS_WESTEUROPEAN: {
        'DFLT': ('*',),
        'latn': ('dflt', 'TRK'),
    },
    FB_ASCIIPLUS: {
        'DFLT': ('*',),
        'latn': ('dflt', 'TRK'),
    },
    FB_LATIN1: {
        'DFLT': ('*',),
        'latn': ('dflt', 'TRK'),
    },
    FB_LATINEXTENDED: {
        'DFLT': ('*',),
        'latn': ('dflt', 'TRK'),
    },
}
