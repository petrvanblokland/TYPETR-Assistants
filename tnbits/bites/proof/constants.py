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
#    constants.py
#
#    Static globals used by the proof tool.
from tnbits.base.views import *
from tnbits.base.samples import SAMPLES as TEXTSAMPLES

# Glyph sets and other standard sample page content. 
# FIXME: move to tnbits.base.samples.
SAMPLES = []

# Construct small set from glyph names. None means all glyphs.
SAMPLENAMES = []

for name, t in TEXTSAMPLES:
    SAMPLENAMES.append(name)
    SAMPLES.append(t)

PAPERORDER = ['A4', 'A3', 'A2', 'A1', '8"x11"', '11"x17"']
PAPERSIZES = {
        # Name:  (width, height, margin)
        'A4': (595, 824, 32),
        'A3': (824, 1195, 48),
        'A2': (1195, 1648, 64),
        'A1': (1648, 2390, 96),
        '8"x11"': (8*72, 11*72, 32),
        '11"x17"': (11*72, 17*72, 48),
    }


a = ['L', 'C', 'R']
ALIGNMENT_VALUES = []

for v in a:
    ALIGNMENT_VALUES.append(getAttributedString(v))

LEADINGS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2,
            2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
LEADING_DEFAULT = 1.2
FONTSIZE_PROGRESSION_DEFAULT = 10
FONTSIZE_DEFAULT = 36

FONTSIZES = ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
        '16', '17', '18', '20', '22', '24', '26', '28', '30', '32', '36', '48',
        '56', '64', '72', '80', '96', '128', '144', '160', '192', '256', '288',
        '320', '364']

TEMPLATES = {
    'PageWide': 'Page Wide',
    'TextProgression': 'Text Progression',
    'KerningMap': 'Kerning Map',
    'Overlay': 'Overlay',
    'AllMetrics': 'All Metrics',
    'StylesPerLine': 'Styles per line',
    #'HTML': 'HyperText Markup Language (HTML)',
    #'ReadingEdge': 'Reading Edge',
    #'Kerning pair matrix', # TODO: Needs better position and scale of the pairs drawing.
    #'Interpolation per glyph',
    #'Arranged',
    #'Book',
    #'Magazine',
    #'Newspaper',
}

TEMPLATES_ORDER = ('PageWide', 'TextProgression', 'StylesPerLine', 'Overlay',
        'AllMetrics', 'KerningMap')
TEMPLATES_NAMES_ORDER = []

for t in TEMPLATES_ORDER:
    TEMPLATES_NAMES_ORDER.append(TEMPLATES[t])
