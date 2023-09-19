# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    samples.py
#

import re
from tnbits.toolbox.character import CharacterTX
from tnbits.base.constants.samples import (BASEGLYPHS, ULCWORDS_PAGE,
        USCWORDS_PAGE, LOREM_IPSUM_PAGE, SPACING, EXTENDED_KERNING,
        IJij_COMBINATIONS, CONTEXT_KERNING, JILLS_KERNING, DUTCH_TEXT_PAGE,
        FRACTIONS, SURNAMES, SS_ASCII, SUPERIORS_PAGE, CYRILLIC_SLAVIC_TEXT,
        TN_FIGURES, TN_PRIMARY, CYRILLIC_NONSLAVIC_TEXT, CYRILLIC_KERNING_TEXT,
        CYRILLIC_KERNING, GREEK_KERNING, QUICK_BROWN_FOX_TEXT, SPACE_SAMPLES,
        TYPETR_RESPONDER, TYPETR_RESPONDER_CONNECTORS, getUnicodeNames)

SELECTED_SAMPLE = '#FILE#'

# TODO: Get these from general smart set description.
HKPX = 'Hkpxfblzhpgjyz'
HHDH = 'HHDHOHODOOnnOoo nnpnonopoo'

# Tags for contextual lookup of sample glyphs, will be calculated for;
# - all glyphs,
# - all glyphs without "." extension,
# - all caps × all glyphs without "." extension,
# - all lowercase × all glyphs without "." extension,
# - all small caps,
# - dynamic sets of feature figure sets,
# - all kerning pairs sorted by value,
# - dynamic sets of all superior and inferiors.
ALL_GLYPHS_TAG = '#ALLGLYPHS#'
ALL_BASE_GLYPHS_TAG = '#ALLBASEGLYPHS#'
CAPS_ON_ALL_BASE_GLYPHS_TAG = '#CAPSXALLBASEGLYPHS#'
LC_ON_ALL_BASE_GLYPHS_TAG = '#LCXALLBASEGLYPHS#'
SMALL_CAPS_TAG = '#SMALLCAPS#'
FIGURE_SETS = '#FIGURESETS#'
SORTED_KERNING_TAG = '#SORTEDKERNING#'
SUPS_SINF_NUMR_DNOM_SETS = '#SUPSSINFNUMRDNOMSETS#'
SUPS_SINF = '#SUPSSINF#'

SAMPLE_TAGS = (ALL_GLYPHS_TAG, ALL_BASE_GLYPHS_TAG, CAPS_ON_ALL_BASE_GLYPHS_TAG,
        LC_ON_ALL_BASE_GLYPHS_TAG, SMALL_CAPS_TAG, SUPS_SINF_NUMR_DNOM_SETS,
        FIGURE_SETS, SORTED_KERNING_TAG)

# Pasted or altered text sample, divided into pages if longer than 25k
# characters.
# TODO: equals selected sample?
CUSTOM_TEXT = '#CUSTOMTEXT#'
#('-- Custom --', CUSTOM_TEXT) # TODO: Make this working together with self._

RE_GLYPHNAMES = re.compile("/(/)|/([a-zA-Z0-9._]*)[\s]?|([^/])")

caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ/AE/OE/Oslash'
smallcaps = '/A.sc/B.sc/C.sc/D.sc/E.sc/F.sc/G.sc/H.sc/I.sc/J.sc/K.sc/L.sc/M.sc/N.sc/O.sc/P.sc/Q.sc/R.sc/S.sc/T.sc/U.sc/V.sc/W.sc/X.sc/Y.sc/Z.sc/AE.sc/OE.sc/Oslash.sc'
lowercase = 'abcdefghijklmnopqrstuvwxyz/ae/oe/oslash'
figures = '1234567890'
punctuation = ':;.,//'

KERNINGCLASSES = dict(
    Cap=caps,
    Sc=smallcaps,
    Lc=lowercase,
    Figs=figures,
    Punc=punctuation
)

kc = ''.join([KERNINGCLASSES['Cap'], '\n', KERNINGCLASSES['Lc'], '\n',
    KERNINGCLASSES['Sc'], '\n', KERNINGCLASSES['Figs'], '\n',
    KERNINGCLASSES['Punc']])

HFT =  "HAMBURGEFONSTIV\nHamburgefonstiv\nH/A.sc/M.sc/B.sc/U.sc/R.sc/G.sc/E.sc/F.sc/O.sc/N.sc/S.sc/T.sc/I.sc/V.sc "
HFT += "Pchnąć w tę łódź jeża lub osiem skrzyń fig. Żywioł, jaźń, Świerk."
HFT += "Flygande bäckasiner söka strax hwila på mjuka tuvor."
HFT += "βρεγμένοι ξυλουργοί πίνουν ψηφιακό ζύθο χωρίς δισταγμό"
HFT += "В чащах юга жил был цитрус...—да, но фальшивый экземпляр!"

LATINTNEXTENDED = '/' + '/'.join(getUnicodeNames('Latin FB Extended'))
LATIN1 = '/' + '/'.join(getUnicodeNames('Latin 1'))
OGL = '/' + '/'.join(getUnicodeNames('OGL'))
MACOS = '/' + '/'.join(getUnicodeNames('Mac Roman'))
MSWGL = '/' + '/'.join(getUnicodeNames('WGL'))
ASCII = '/' + '/'.join(SS_ASCII)

# TODO: Check
SPACE_MASTERS_NAME = 'Space masters'
SPACE_MASTERS_TEXT = []

for tt in SPACE_SAMPLES:
    SPACE_MASTERS_TEXT.append('/'.join(tt))

SPACE_MASTERS_TEXT = '\n'.join(SPACE_MASTERS_TEXT)

ULCWORDS_NAME = 'Cap-lowercase words'
USCWORDS_NAME = 'Cap-smallcaps words'
FRACTIONS_NAME = 'Fractions 1-100'
ALL_GLYPHS_NAME = 'All glyphs in the style'

SAMPLES = (
    ('Basic Latin', BASEGLYPHS),
    (HKPX, HKPX),
    (HHDH, HHDH),
    ('Hamburgefonstiv', HFT),
    ('A-Z a-z .sc Figures', kc),
    (ULCWORDS_NAME, ULCWORDS_PAGE), # ULCWORDS for split pages.
    (USCWORDS_NAME, USCWORDS_PAGE), # USCWORDS for split pages.
    (ALL_GLYPHS_NAME, ALL_GLYPHS_TAG),
    ('All glyphs with extension', ALL_BASE_GLYPHS_TAG),
    ('Caps on all glyphs with extension', CAPS_ON_ALL_BASE_GLYPHS_TAG),
    ('Lowercase on all glyphs with extension', LC_ON_ALL_BASE_GLYPHS_TAG),
    ('All smallcaps in the style', SMALL_CAPS_TAG),
    ('Lorem ipsum', LOREM_IPSUM_PAGE), # LOREM_IPSUM_TEXT for split pages.
    ('Spacing', SPACING),
    (SPACE_MASTERS_NAME, SPACE_MASTERS_TEXT),
    ('Extended kerning', EXTENDED_KERNING),
    ('Contextual kerning', CONTEXT_KERNING),
    ('Jills kerning', JILLS_KERNING),
    ('Sorted kerning', SORTED_KERNING_TAG),
    ('IJij combinations', IJij_COMBINATIONS),
    ('Figures', KERNINGCLASSES['Figs']),
    ('Surnames', SURNAMES),
    ('Dutch', DUTCH_TEXT_PAGE), # DUTCH_TEXT_PAGE for split pages.
    ('Quick brown fox', QUICK_BROWN_FOX_TEXT),
    (FRACTIONS_NAME, FRACTIONS),
    #('Figure sets', FIGURE_SETS),
    ('Superiors & Inferiors', SUPERIORS_PAGE),
    ('Greek kerning', GREEK_KERNING),
    ('Cyrillic kerning', CYRILLIC_KERNING),
    ('Cyrillic kerning text', CYRILLIC_KERNING_TEXT),
    ('Cyrillic Slavic text', CYRILLIC_SLAVIC_TEXT),
    ('Cyrillic Non Slavic text', CYRILLIC_NONSLAVIC_TEXT),
    ('ASCII', ASCII),
    ('Latin 1', LATIN1),
    ('Latin TN Extended', LATINTNEXTENDED),
    ('OGL', OGL),
    ('MS WGL4', MSWGL),
    ('Mac OS Roman', MACOS),
    ('Selected sample', SELECTED_SAMPLE),
    ('TYPETR Responder', TYPETR_RESPONDER),
    ('TYPETR Connectors', TYPETR_RESPONDER_CONNECTORS),
)

def char2GlyphName(u):
    """Translates the name into glyphName. Keeps control of white space so we
    can respond to line endings."""
    if u in ('\n', '\r', '\t'):
        return u

    return CharacterTX.char2GlyphName(u)

def getGlyphName(t):
    c1, c2, c3 = t
    if c2:
        return c2
    elif c1 or c3:
        glyphName = char2GlyphName(c1 or c3)

        try:
            assert glyphName is not None
        except:
            print('No name found for %s, %s' % (c1, c3))

        return glyphName

def compileText(page):
    """Converts glyphs to glyph names.

    NOTE: no checking is done if the glyph actually exists in the font."""
    glyphNames = []

    # Regular expression to divide page by slashes to derive glyph names (?).
    textGlyphs = RE_GLYPHNAMES.findall(page)

    for i, t in enumerate(textGlyphs):
        # Filters single slashes.
        if t == ('', '', ''):
            continue

        glyphName = getGlyphName(t)
        if glyphName == '.notdef':
            continue
        try:
            assert not glyphName is None
        except:
            print('Bad glyph number %d' % i)

            if isinstance(t, str):
                print('could not convert glyph %s' % t)
            elif isinstance(t, tuple):
                print('is a tuple, please check text sample: %s' % str(t))
            else:
                print('could not convert glyph of type %s' % type(t))

            continue

        glyphNames.append(glyphName)
    return glyphNames


print(LATINTNEXTENDED)
