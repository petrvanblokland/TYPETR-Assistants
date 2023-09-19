# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    sorting.py
#

# The preferred way to sort is first by weight, then by width, and then by
# slope. See also ticket #183.

SORTWEIGHTSORDER = ['ultrathin', 'thin', 'ultralight', 'extralight',
        'light', 'semilight', 'book', 'regular', 'medium', 'semibold', 'bold',
        'extrabold', 'black', 'extrablack', 'heavy', 'ultra', 'super', 'None']

# NOTE: Adding 'None' at the end as a fall-through option for sortFamily()
# / sortCollected().  This should be temporary, there's no such weight /
# width.
SORTWEIGHTS = {
        'ultrathin': ['hairline'],
        'thin': [],
        'ultralight': ['ultral', 'ultral'],
        'extralight': ['extral', 'extral', 'exl'],
        'light': ['lght'],
        'semilight': ['demil', 'demil', 'semil','semil'],
        'book': ['bk'],
        'regular': ['reg', 'roman', 'rom'],
        'medium': ['med', 'middle'],
        'semibold': ['demib', 'demib', 'semib','semib'],
        'bold': ['bld'],
        'extrabold': ['extrabo', 'extrabo'],
        'black': ['blk'],
        'extrablack': ['extrabl', 'extrabl', 'extbl', 'extbl'],
        'heavy': ['hvy'],
        'ultra': ['ult', 'ultrablack'],
        'super': ['sup'],
        'None': []
    }

SORTWIDTHSORDER = ['extracompressed', 'compressed', 'extracondensed',
        'condensed', 'None', 'extended']

SORTWIDTHS = {
            'extracompressed': [],
            'compressed': ['comp', 'cm'],
            'extracondensed': [],
            'condensed': ['cond', 'cn', 'narrow'],
            'wide': [],
            'None': [],
            'extended': ['exp', 'ext', 'extend']}

# TODO: also look at these:
SORTOPTICALSIZE = ['Sky', 'Post', 'Banner', 'Titl', 'Disp', 'Deck', 'Text',
        'RE', 'Micro']
SORTSLOPE = ['Italic', 'Ital',  'It', 'Oblique', 'Ob']
SORTSERIF = ['San', 'Ser']
