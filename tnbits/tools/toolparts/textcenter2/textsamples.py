# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    textsamples.py
#
import re
from tnbits.tools.constantsparts.smartsets import ULCWORDS, ULCWORDS_PAGE, USCWORDS_PAGE, LOREM_IPSUM_PAGE, SPACING, EXTENDED_KERNING, \
    CONTEXT_KERNING, JILL_KERNING, DUTCH_TEXT_PAGE, FRACTIONS, SURNAMES, SS_ASCII, SUPERIORS_PAGE, \
    CYRILLIC_SLAVIC_TEXT, CYRILLIC_NONSLAVIC_TEXT, CYRILLIC_KERNING, getUnicodeNames

# TODO: Get these from general smart set description.

KERNINGCLASSES = dict(
    Cap='ABCDEFGHIJKLMNOPQRSTUVWXYZ/AE/OE/Oslash',
    Sc='/A.sc/B.sc/C.sc/D.sc/E.sc/F.sc/G.sc/H.sc/I.sc/J.sc/K.sc/L.sc/M.sc/N.sc/O.sc/P.sc/Q.sc/R.sc/S.sc/T.sc/U.sc/V.sc/W.sc/X.sc/Y.sc/Z.sc/AE.sc/OE.sc/Oslash.sc',
    Lc='abcdefghijklmnopqrstuvwxyz/ae/oe/oslash',
    Figs='1234567890',
    Punc=':;.,//'
)
IJij_COMBINATIONS = """/A/I/A/Iacute/A/Igrave/A/Imacron/A/Itilde/A/Ibreve/A/Iogonek/A/Icircumflex/A/Idieresis/A/Idotaccent/A/J/A/Jcircumflex/B/I/B/Iacute/B/Igrave/B/Imacron/B/Itilde/B/Ibreve/B/Iogonek/B/Icircumflex/B/Idieresis/B/Idotaccent/B/J/B/Jcircumflex/C/I/C/Iacute/C/Igrave/C/Imacron/C/Itilde/C/Ibreve/C/Iogonek/C/Icircumflex/C/Idieresis/C/Idotaccent/C/J/C/Jcircumflex/D/I/D/Iacute/D/Igrave/D/Imacron/D/Itilde/D/Ibreve/D/Iogonek/D/Icircumflex/D/Idieresis/D/Idotaccent/D/J/D/Jcircumflex/E/I/E/Iacute/E/Igrave/E/Imacron/E/Itilde/E/Ibreve/E/Iogonek/E/Icircumflex/E/Idieresis/E/Idotaccent/E/J/E/Jcircumflex/F/I/F/Iacute/F/Igrave/F/Imacron/F/Itilde/F/Ibreve/F/Iogonek/F/Icircumflex/F/Idieresis/F/Idotaccent/F/J/F/Jcircumflex/G/I/G/Iacute/G/Igrave/G/Imacron/G/Itilde/G/Ibreve/G/Iogonek/G/Icircumflex/G/Idieresis/G/Idotaccent/G/J/G/Jcircumflex/H/I/H/Iacute/H/Igrave/H/Imacron/H/Itilde/H/Ibreve/H/Iogonek/H/Icircumflex/H/Idieresis/H/Idotaccent/H/J/H/Jcircumflex/I/I/I/Iacute/I/Igrave/I/Imacron/I/Itilde/I/Ibreve/I/Iogonek/I/Icircumflex/I/Idieresis/I/Idotaccent/I/J/I/Jcircumflex/J/I/J/Iacute/J/Igrave/J/Imacron/J/Itilde/J/Ibreve/J/Iogonek/J/Icircumflex/J/Idieresis/J/Idotaccent/J/Jcircumflex/K/I/K/Iacute/K/Igrave/K/Imacron/K/Itilde/K/Ibreve/K/Iogonek/K/Icircumflex/K/Idieresis/K/Idotaccent/K/J/K/Jcircumflex/L/I/L/Iacute/L/Igrave/L/Imacron/L/Itilde/L/Ibreve/L/Iogonek/L/Icircumflex/L/Idieresis/L/Idotaccent/L/J/L/Jcircumflex/M/I/M/Iacute/M/Igrave/M/Imacron/M/Itilde/M/Ibreve/M/Iogonek/M/Icircumflex/M/Idieresis/M/Idotaccent/M/J/M/Jcircumflex/N/I/N/Iacute/N/Igrave/N/Imacron/N/Itilde/N/Ibreve/N/Iogonek/N/Icircumflex/N/Idieresis/N/Idotaccent/N/J/N/Jcircumflex/O/I/O/Iacute/O/Igrave/O/Imacron/O/Itilde/O/Ibreve/O/Iogonek/O/Icircumflex/O/Idieresis/O/Idotaccent/O/J/O/Jcircumflex/P/I/P/Iacute/P/Igrave/P/Imacron/P/Itilde/P/Ibreve/P/Iogonek/P/Icircumflex/P/Idieresis/P/Idotaccent/P/J/P/Jcircumflex/Q/I/Q/Iacute/Q/Igrave/Q/Imacron/Q/Itilde/Q/Ibreve/Q/Iogonek/Q/Icircumflex/Q/Idieresis/Q/Idotaccent/Q/J/Q/Jcircumflex/R/I/R/Iacute/R/Igrave/R/Imacron/R/Itilde/R/Ibreve/R/Iogonek/R/Icircumflex/R/Idieresis/R/Idotaccent/R/J/R/Jcircumflex/S/I/S/Iacute/S/Igrave/S/Imacron/S/Itilde/S/Ibreve/S/Iogonek/S/Icircumflex/S/Idieresis/S/Idotaccent/S/J/S/Jcircumflex/T/I/T/Iacute/T/Igrave/T/Imacron/T/Itilde/T/Ibreve/T/Iogonek/T/Icircumflex/T/Idieresis/T/Idotaccent/T/J/T/Jcircumflex/U/I/U/Iacute/U/Igrave/U/Imacron/U/Itilde/U/Ibreve/U/Iogonek/U/Icircumflex/U/Idieresis/U/Idotaccent/U/J/U/Jcircumflex/V/I/V/Iacute/V/Igrave/V/Imacron/V/Itilde/V/Ibreve/V/Iogonek/V/Icircumflex/V/Idieresis/V/Idotaccent/V/J/V/Jcircumflex/W/I/W/Iacute/W/Igrave/W/Imacron/W/Itilde/W/Ibreve/W/Iogonek/W/Icircumflex/W/Idieresis/W/Idotaccent/W/J/W/Jcircumflex/X/I/X/Iacute/X/Igrave/X/Imacron/X/Itilde/X/Ibreve/X/Iogonek/X/Icircumflex/X/Idieresis/X/Idotaccent/X/J/X/Jcircumflex/Y/I/Y/Iacute/Y/Igrave/Y/Imacron/Y/Itilde/Y/Ibreve/Y/Iogonek/Y/Icircumflex/Y/Idieresis/Y/Idotaccent/Y/J/Y/Jcircumflex/Z/I/Z/Iacute/Z/Igrave/Z/Imacron/Z/Itilde/Z/Ibreve/Z/Iogonek/Z/Icircumflex/Z/Idieresis/Z/Idotaccent/Z/J/Z/Jcircumflex/A/i/A/iacute/A/igrave/A/imacron/A/itilde/A/ibreve/A/iogonek/A/icircumflex/A/idieresis/A/idotaccent/A/j/A/jcircumflex/B/i/B/iacute/B/igrave/B/imacron/B/itilde/B/ibreve/B/iogonek/B/icircumflex/B/idieresis/B/idotaccent/B/j/B/jcircumflex/C/i/C/iacute/C/igrave/C/imacron/C/itilde/C/ibreve/C/iogonek/C/icircumflex/C/idieresis/C/idotaccent/C/j/C/jcircumflex/D/i/D/iacute/D/igrave/D/imacron/D/itilde/D/ibreve/D/iogonek/D/icircumflex/D/idieresis/D/idotaccent/D/j/D/jcircumflex/E/i/E/iacute/E/igrave/E/imacron/E/itilde/E/ibreve/E/iogonek/E/icircumflex/E/idieresis/E/idotaccent/E/j/E/jcircumflex/F/i/F/iacute/F/igrave/F/imacron/F/itilde/F/ibreve/F/iogonek/F/icircumflex/F/idieresis/F/idotaccent/F/j/F/jcircumflex/G/i/G/iacute/G/igrave/G/imacron/G/itilde/G/ibreve/G/iogonek/G/icircumflex/G/idieresis/G/idotaccent/G/j/G/jcircumflex/H/i/H/iacute/H/igrave/H/imacron/H/itilde/H/ibreve/H/iogonek/H/icircumflex/H/idieresis/H/idotaccent/H/j/H/jcircumflex/I/i/I/iacute/I/igrave/I/imacron/I/itilde/I/ibreve/I/iogonek/I/icircumflex/I/idieresis/I/idotaccent/I/j/I/jcircumflex/J/i/J/iacute/J/igrave/J/imacron/J/itilde/J/ibreve/J/iogonek/J/icircumflex/J/idieresis/J/idotaccent/J/j/J/jcircumflex/K/i/K/iacute/K/igrave/K/imacron/K/itilde/K/ibreve/K/iogonek/K/icircumflex/K/idieresis/K/idotaccent/K/j/K/jcircumflex/L/i/L/iacute/L/igrave/L/imacron/L/itilde/L/ibreve/L/iogonek/L/icircumflex/L/idieresis/L/idotaccent/L/j/L/jcircumflex/M/i/M/iacute/M/igrave/M/imacron/M/itilde/M/ibreve/M/iogonek/M/icircumflex/M/idieresis/M/idotaccent/M/j/M/jcircumflex/N/i/N/iacute/N/igrave/N/imacron/N/itilde/N/ibreve/N/iogonek/N/icircumflex/N/idieresis/N/idotaccent/N/j/N/jcircumflex/O/i/O/iacute/O/igrave/O/imacron/O/itilde/O/ibreve/O/iogonek/O/icircumflex/O/idieresis/O/idotaccent/O/j/O/jcircumflex/P/i/P/iacute/P/igrave/P/imacron/P/itilde/P/ibreve/P/iogonek/P/icircumflex/P/idieresis/P/idotaccent/P/j/P/jcircumflex/Q/i/Q/iacute/Q/igrave/Q/imacron/Q/itilde/Q/ibreve/Q/iogonek/Q/icircumflex/Q/idieresis/Q/idotaccent/Q/j/Q/jcircumflex/R/i/R/iacute/R/igrave/R/imacron/R/itilde/R/ibreve/R/iogonek/R/icircumflex/R/idieresis/R/idotaccent/R/j/R/jcircumflex/S/i/S/iacute/S/igrave/S/imacron/S/itilde/S/ibreve/S/iogonek/S/icircumflex/S/idieresis/S/idotaccent/S/j/S/jcircumflex/T/i/T/iacute/T/igrave/T/imacron/T/itilde/T/ibreve/T/iogonek/T/icircumflex/T/idieresis/T/idotaccent/T/j/T/jcircumflex/U/i/U/iacute/U/igrave/U/imacron/U/itilde/U/ibreve/U/iogonek/U/icircumflex/U/idieresis/U/idotaccent/U/j/U/jcircumflex/V/i/V/iacute/V/igrave/V/imacron/V/itilde/V/ibreve/V/iogonek/V/icircumflex/V/idieresis/V/idotaccent/V/j/V/jcircumflex/W/i/W/iacute/W/igrave/W/imacron/W/itilde/W/ibreve/W/iogonek/W/icircumflex/W/idieresis/W/idotaccent/W/j/W/jcircumflex/X/i/X/iacute/X/igrave/X/imacron/X/itilde/X/ibreve/X/iogonek/X/icircumflex/X/idieresis/X/idotaccent/X/j/X/jcircumflex/Y/i/Y/iacute/Y/igrave/Y/imacron/Y/itilde/Y/ibreve/Y/iogonek/Y/icircumflex/Y/idieresis/Y/idotaccent/Y/j/Y/jcircumflex/Z/i/Z/iacute/Z/igrave/Z/imacron/Z/itilde/Z/ibreve/Z/iogonek/Z/icircumflex/Z/idieresis/Z/idotaccent/Z/j/Z/jcircumflex/a/i/a/iacute/a/igrave/a/imacron/a/itilde/a/ibreve/a/iogonek/a/icircumflex/a/idieresis/a/idotaccent/a/j/a/jcircumflex/b/i/b/iacute/b/igrave/b/imacron/b/itilde/b/ibreve/b/iogonek/b/icircumflex/b/idieresis/b/idotaccent/b/j/b/jcircumflex/c/i/c/iacute/c/igrave/c/imacron/c/itilde/c/ibreve/c/iogonek/c/icircumflex/c/idieresis/c/idotaccent/c/j/c/jcircumflex/d/i/d/iacute/d/igrave/d/imacron/d/itilde/d/ibreve/d/iogonek/d/icircumflex/d/idieresis/d/idotaccent/d/j/d/jcircumflex/e/i/e/iacute/e/igrave/e/imacron/e/itilde/e/ibreve/e/iogonek/e/icircumflex/e/idieresis/e/idotaccent/e/j/e/jcircumflex/f/i/f/iacute/f/igrave/f/imacron/f/itilde/f/ibreve/f/iogonek/f/icircumflex/f/idieresis/f/idotaccent/f/j/f/jcircumflex/g/i/g/iacute/g/igrave/g/imacron/g/itilde/g/ibreve/g/iogonek/g/icircumflex/g/idieresis/g/idotaccent/g/j/g/jcircumflex/h/i/h/iacute/h/igrave/h/imacron/h/itilde/h/ibreve/h/iogonek/h/icircumflex/h/idieresis/h/idotaccent/h/j/h/jcircumflex/i/i/i/iacute/i/igrave/i/imacron/i/itilde/i/ibreve/i/iogonek/i/icircumflex/i/idieresis/i/idotaccent/i/j/i/jcircumflex/j/i/j/iacute/j/igrave/j/imacron/j/itilde/j/ibreve/j/iogonek/j/icircumflex/j/idieresis/j/idotaccent/j/j/j/jcircumflex/k/i/k/iacute/k/igrave/k/imacron/k/itilde/k/ibreve/k/iogonek/k/icircumflex/k/idieresis/k/idotaccent/k/j/k/jcircumflex/l/i/l/iacute/l/igrave/l/imacron/l/itilde/l/ibreve/l/iogonek/l/icircumflex/l/idieresis/l/idotaccent/l/j/l/jcircumflex/m/i/m/iacute/m/igrave/m/imacron/m/itilde/m/ibreve/m/iogonek/m/icircumflex/m/idieresis/m/idotaccent/m/j/m/jcircumflex/n/i/n/iacute/n/igrave/n/imacron/n/itilde/n/ibreve/n/iogonek/n/icircumflex/n/idieresis/n/idotaccent/n/j/n/jcircumflex/o/i/o/iacute/o/igrave/o/imacron/o/itilde/o/ibreve/o/iogonek/o/icircumflex/o/idieresis/o/idotaccent/o/j/o/jcircumflex/p/i/p/iacute/p/igrave/p/imacron/p/itilde/p/ibreve/p/iogonek/p/icircumflex/p/idieresis/p/idotaccent/p/j/p/jcircumflex/q/i/q/iacute/q/igrave/q/imacron/q/itilde/q/ibreve/q/iogonek/q/icircumflex/q/idieresis/q/idotaccent/q/j/q/jcircumflex/r/i/r/iacute/r/igrave/r/imacron/r/itilde/r/ibreve/r/iogonek/r/icircumflex/r/idieresis/r/idotaccent/r/j/r/jcircumflex/s/i/s/iacute/s/igrave/s/imacron/s/itilde/s/ibreve/s/iogonek/s/icircumflex/s/idieresis/s/idotaccent/s/j/s/jcircumflex/t/i/t/iacute/t/igrave/t/imacron/t/itilde/t/ibreve/t/iogonek/t/icircumflex/t/idieresis/t/idotaccent/t/j/t/jcircumflex/u/i/u/iacute/u/igrave/u/imacron/u/itilde/u/ibreve/u/iogonek/u/icircumflex/u/idieresis/u/idotaccent/u/j/u/jcircumflex/v/i/v/iacute/v/igrave/v/imacron/v/itilde/v/ibreve/v/iogonek/v/icircumflex/v/idieresis/v/idotaccent/v/j/v/jcircumflex/w/i/w/iacute/w/igrave/w/imacron/w/itilde/w/ibreve/w/iogonek/w/icircumflex/w/idieresis/w/idotaccent/w/j/w/jcircumflex/x/i/x/iacute/x/igrave/x/imacron/x/itilde/x/ibreve/x/iogonek/x/icircumflex/x/idieresis/x/idotaccent/x/j/x/jcircumflex/y/i/y/iacute/y/igrave/y/imacron/y/itilde/y/ibreve/y/iogonek/y/icircumflex/y/idieresis/y/idotaccent/y/j/y/jcircumflex/z/i/z/iacute/z/igrave/z/imacron/z/itilde/z/ibreve/z/iogonek/z/icircumflex/z/idieresis/z/idotaccent/z/j/z/jcircumflex"""

ALL_GLYPHS_TAG = '#ALLGLYPHS#' # Contextual of selected styles, will be calculated.
ALL_BASE_GLYPHS_TAG = '#ALLBASEGLYPHS#' # Contextual of selected styles, all glyphs without "." extension, will be calculated.
CAPS_ON_ALL_BASE_GLYPHS_TAG = '#CAPSXALLBASEGLYPHS#' # Contextual of selected styles, all caps x all glyphs without "." extension, will be calculated.
LC_ON_ALL_BASE_GLYPHS_TAG = '#LCXALLBASEGLYPHS#' # Contextual of selected styles, all lowercase x all glyphs without "." extension, will be calculated.
SORTED_KERNING_TAG = '#SORTEDKERNING#' # All kerning pairs sorted by value
SMALL_CAPS_TAG = '#SMALLCAPS#' # All small caps
CUSTOM_TEXT = '#CUSTOMTEXT#' # Pasted or altered text sample, divided into pages if longer than 25k characters.
FIGURE_SETS = '#FIGURESETS#' # Dynamic sets of feature figure sets.

RE_GLYPHNAMES = re.compile("/(/)|/([a-zA-Z0-9._]*)[\s]?|([^/])")

PAGES = (
    ('A-Z a-z .sc Figures', KERNINGCLASSES['Cap'] + '\n' + KERNINGCLASSES['Lc'] + '\n' + KERNINGCLASSES['Sc'] + '\n' + KERNINGCLASSES['Figs'] + '\n' + KERNINGCLASSES['Punc']),
    ('Cap-lc words', ULCWORDS_PAGE), # ULCWORDS for split pages.
    ('Cap-smallcaps words', USCWORDS_PAGE), # USCWORDS for split pages.
    ('Hamburgerfonstiv', """HAMBURGEFONSTIV\nHamburgefonstiv\nH/A.sc/M.sc/B.sc/U.sc/R.sc/G.sc/E.sc/F.sc/O.sc/N.sc/S.sc/T.sc/I.sc/V.sc"""),
    ('All glyphs in the style', ALL_GLYPHS_TAG),
    ('All glyphs w/h extension', ALL_BASE_GLYPHS_TAG),
    ('Caps on all glyphs w/h extension', CAPS_ON_ALL_BASE_GLYPHS_TAG),
    ('Lowercase on all glyphs w/h extension', LC_ON_ALL_BASE_GLYPHS_TAG),
    ('All smallcaps in the style', SMALL_CAPS_TAG),
    ('Lorem ipsum', LOREM_IPSUM_PAGE), # LOREM_IPSUM_TEXT for split pages.
    ('Spacing', SPACING),
    ('Extended kerning', EXTENDED_KERNING),
    ('Contextual kerning', CONTEXT_KERNING),
    ('Jills kerning', JILL_KERNING),
    ('Sorted kerning', SORTED_KERNING_TAG),
    ('IJij combinations', IJij_COMBINATIONS),
    ('Figures', KERNINGCLASSES['Figs']),
    ('Surnames', SURNAMES),
    ('Dutch', DUTCH_TEXT_PAGE), # DUTCH_TEXT_PAGE for split pages.
    ('Fractions', FRACTIONS),
    ('Figure sets', FIGURE_SETS),
    ('Superiors & Inferiors', SUPERIORS_PAGE),
    ('Cyrillic Slavic text', CYRILLIC_SLAVIC_TEXT),
    ('Cyrillic Non Slavic text', CYRILLIC_NONSLAVIC_TEXT),
    ('Cyrillic kerning', CYRILLIC_KERNING),
    ('ASCII', SS_ASCII),
    ('Latin 1', '/'.join(getUnicodeNames('Latin 1'))),
    ('Latin TN Extended', '/'.join(getUnicodeNames('Latin FB Extended'))),
    ('OGL', '/'.join(getUnicodeNames('OGL'))),
    ('MS WGL4', '/'.join(getUnicodeNames('WGL'))),
    ('Mac OS Roman', '/'.join(getUnicodeNames('Mac Roman'))),
    ('-- Custom --', CUSTOM_TEXT) # TODO: Make this working together with self._
)
