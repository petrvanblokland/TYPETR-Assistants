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
#    glyphsets.py
#


import re
from tnbits.tools.constantsparts.smartsets import ULCWORDS, USCWORDS, CONTEXT_KERNING, SPACING, \
                                        EXTENDED_KERNING, CYRILLIC_SLAVIC_TEXT, \
                                        CYRILLIC_NONSLAVIC_TEXT, CYRILLIC_KERNING, \
                                        JILL_KERNING, LOREM_IPSUM_TEXT, BASEGLYPHS, \
                                        SPACE_SAMPLES, DUTCH_TEXT, FRACTIONS

from tnbits.model import model
from tnbits.toolbox.character import CharacterTX
RE_GLYPHNAMES = re.compile("/(/)|/([a-zA-Z0-9._]*)[\s]?|([^/])")
# TODO: deprecated, switch to global tnbits.base.samples.

class GlyphSets(object):
    """
    Wraps the smart set values so they can be used in a GUI.
    """

    ULCWORDS = ' '.join(ULCWORDS) # Make string from pages.
    USCWORDS = ' '.join(USCWORDS) # Make string from pages.
    HKPX = 'Hkpxfblzhpgjyz'
    SPACING = ' '.join(SPACING)
    EXTENDED_KERNING = ' '.join(EXTENDED_KERNING)
    JILL_KERNING = ''.join(JILL_KERNING)
    LOREM_IPSUM_TEXT = '\n'.join(LOREM_IPSUM_TEXT)
    DUTCH_TEXT = '\n'.join(DUTCH_TEXT)
    CYRILLIC_SLAVIC_TEXT = '\n\n'.join(CYRILLIC_SLAVIC_TEXT)
    CYRILLIC_NONSLAVIC_TEXT = '\n\n'.join(CYRILLIC_NONSLAVIC_TEXT)
    CYRILLIC_KERNING = '\n\n'.join(CYRILLIC_KERNING)
    FRACTIONS = ' '.join(FRACTIONS)
    ALL_GLYPHS = '#ALLGLYPHS#' # Contextual of selected styles, will be calculated.
    SAMPLE_FILE = '#FILE#' # Trigger to read from the specified sample file path

    SPACE_MASTERS_TEXT = []

    for tt in SPACE_SAMPLES:
        SPACE_MASTERS_TEXT.append('/'.join(tt))

    SPACE_MASTERS_TEXT = '\n'.join(SPACE_MASTERS_TEXT)

    # Split into set and titles, to keep the order in the popup.
    GLYPH_SOURCES = (
        ('Basic Latin', BASEGLYPHS),
        ('Hkpxfblzhpgjyz', HKPX),
        ('UC-lc words', ULCWORDS),
        ('UC-smallcap words', USCWORDS),
        ('Spacing', SPACING),
        ('Extended kerning', EXTENDED_KERNING),
        ('Contextual kerning', CONTEXT_KERNING),
        (u"Jill's kerningbla", JILL_KERNING),
        ('Fractions 1-100', FRACTIONS),
        ('All glyphs in the style', ALL_GLYPHS),
        ('Lorem ipsum', LOREM_IPSUM_TEXT),
        ('Space masters', SPACE_MASTERS_TEXT),
        ('Dutch text', DUTCH_TEXT),
        ('Cyrillic Slavic text', CYRILLIC_SLAVIC_TEXT),
        ('Cyrillic Non Slavic text', CYRILLIC_NONSLAVIC_TEXT),
        ('Cyrillic kerning', CYRILLIC_KERNING),
        ('Selected sample', SAMPLE_FILE), # Trigger to read the text from the
                                          # indicated sample file path.
        #'Englist text': TYPENETWORK_MANIFEST,
    )

    GLYPHSETS = {}
    GLYPHSET_TITLES = []

    # Flattens sources into a dictionary and adds titles to a list.
    for title, source in GLYPH_SOURCES:
        GLYPHSETS[title] = source
        GLYPHSET_TITLES.append(title)

    NO_SAMPLE_FILE_SELECTED = 'No sample file selected'

    def getContent(self, styleKeys, view):
        """Returns one of the defined sample sets or a custom sample file."""
        contentName = view.selectContent.getItem()
        content = self.GLYPHSETS[contentName or 'Basic Latin']

        if content == self.SAMPLE_FILE:
            # If there is no sample text path, ask for a file first.
            if not self._sampleTextPath:
                self.selectSampleTextCallback()

            if self._sampleTextPath:
                content = self.readFile(self._sampleTextPath)
        elif content == self.ALL_GLYPHS:
            content = set()

            for styleKey in styleKeys:
                content = content.union(set(model.getStyle(styleKey).keys()))
            content = '/'.join(sorted(content))

        return contentName, content

    def compiledText(self, t):
        """Answers the list of glyph names of the text to draw, including
        start and end glyphs. Doesn't check if the glyph exists in the font."""
        glyphNames = []

        try:
            for c1, c2, c3 in RE_GLYPHNAMES.findall(t):
                if c3 and c3 in '\n\r':
                    glyphNames.append(c3)
                elif c2:
                    glyphNames.append(c2)
                elif c1 or c3:
                    glyphName = CharacterTX.char2GlyphName(c1 or c3)
                    glyphNames.append(glyphName)
        except TypeError:
            print('Type error in compiledText()', t)

        return glyphNames
