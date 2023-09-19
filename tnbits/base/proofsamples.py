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
#    samples.py
#
#    Wraps the sample set values so they can be used in a GUI.
#    Static version of toolparts/glyphsets.py.

# DEPRECATED.
# See new sample.py
# NOTE: Merged with TCTool


'''
from tnbits.tools.constantsparts.smartsets import (ULCWORDS, USCWORDS,
        CONTEXT_KERNING, SPACING, EXTENDED_KERNING, CYRILLIC_SLAVIC_TEXT,
        CYRILLIC_NONSLAVIC_TEXT, CYRILLIC_KERNING_TEXT,
        CYRILLIC_KERNING, GREEK_KERNING, JILL_KERNING,
        LOREM_IPSUM_TEXT, BASEGLYPHS, SPACE_SAMPLES, DUTCH_TEXT, FRACTIONS,
        QUICK_BROWN_FOX_TEXT)
from tnbits.toolbox.character import CharacterTX
import re

HKPX = 'Hkpxfblzhpgjyz'
HHDH = 'HHDHOHODOOnnOoo nnpnonopoo'
ULCWORDS = ' '.join(ULCWORDS) # Make string from pages.

USCWORDS_NAME = 'UC-smallcap words'
USCWORDS = ' '.join(USCWORDS) # Make string from pages.
SPACING = ' '.join(SPACING)
EXTENDED_KERNING = ' '.join(EXTENDED_KERNING)
JILL_KERNING = ''.join(JILL_KERNING)
LOREM_IPSUM_TEXT = '\n'.join(LOREM_IPSUM_TEXT)
DUTCH_TEXT = '\n'.join(DUTCH_TEXT)
FRACTIONS_NAME = 'Fractions 1-100'
FRACTIONS = ' '.join(FRACTIONS)
ALL_GLYPHS_NAME = 'All glyphs in the style'
ALL_GLYPHS = '#ALLGLYPHS#' # Contextual of selected styles, will be calculated.
ALL_CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SELECTED_SAMPLE = '#FILE#'
SPACE_MASTERS_NAME = 'Space masters'
SPACE_MASTERS_TEXT = []

for tt in SPACE_SAMPLES:
    SPACE_MASTERS_TEXT.append('/'.join(tt))

SPACE_MASTERS_TEXT = '\n'.join(SPACE_MASTERS_TEXT)

# Split into set and titles, to keep the order in the popup.
GLYPH_SOURCES = (
    ('Basic Latin', BASEGLYPHS),
    (HKPX, HKPX),
    (HHDH, HHDH),
    ('UC-lc words', ULCWORDS),
    (USCWORDS_NAME, USCWORDS),
    ('Spacing', SPACING),
    ('Extended kerning', EXTENDED_KERNING),
    ('Contextual kerning', CONTEXT_KERNING),
    ("Jill's kerning", JILL_KERNING),
    (FRACTIONS_NAME, FRACTIONS),
    (ALL_GLYPHS_NAME, ALL_GLYPHS),
    ('Lorem ipsum', LOREM_IPSUM_TEXT),
    ('Quick brown fox', QUICK_BROWN_FOX_TEXT),
    (SPACE_MASTERS_NAME, SPACE_MASTERS_TEXT),
    ('Dutch text', DUTCH_TEXT),
    ('All Caps', ALL_CAPS),
    ('Greek kerning', GREEK_KERNING),
    ('Cyrillic kerning', CYRILLIC_KERNING),
    ('Cyrillic Slavic text', CYRILLIC_SLAVIC_TEXT),
    ('Cyrillic Non Slavic text', CYRILLIC_NONSLAVIC_TEXT),
    ('Cyrillic kerning text', CYRILLIC_KERNING_TEXT),
    ('Selected sample', SELECTED_SAMPLE), # Trigger to read the text from the
                                      # indicated sample file path.
)

GLYPHSETS = {}
GLYPHSET_TITLES = []

# Flips title and source and adds titles to a list.
for title, source in GLYPH_SOURCES:
    GLYPHSETS[title] = source
    GLYPHSET_TITLES.append(title)

RE_GLYPHNAMES = re.compile("/(/)|/([a-zA-Z0-9._]*)[\s]?|([^/])")

def compiledText(t, sorting=None, verbose=False):
    """Answers the list of glyph names of the text to draw, including
    start and end glyphs. Doesn't check if the glyph exists in the font.

    Filters all names starting with slashes.


    TODO: take care of sorting here.
    FIXME: splits .notdef into separate glyphs.

    """
    glyphNames = []

    try:
        for c1, c2, c3 in RE_GLYPHNAMES.findall(t):
            if verbose:
                print('c1: %s' % c1)
                print('c2: %s' % c2)
                print('c3: %s' % c3)

            if c3 and c3 in '\n\r':
                glyphNames.append(c3)
            elif c2:
                glyphNames.append(c2)
            elif c1 or c3:
                glyphName = CharacterTX.char2GlyphName(c1 or c3)
                glyphNames.append(glyphName)
    except TypeError as e:
        print('Type error in compiledText()', t, e)

    return glyphNames
'''
