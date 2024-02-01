# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   glyphSet.py
#
from copy import deepcopy

class GlyphSet:
    """GlyphSet behaves like a dictionary of GlyphData instances.

    >>> from glyphData import *
    >>> glyphs = {\
        'A': GD(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', comment='A Uppercase Alphabet, Latin', gid=35),\
        'Aacute': GD(l='A', r='A', uni=193, c='Á', name='Aacute', srcName='Aacute', hex='00c1', base='A', accents=['acute'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER', gid=130),\
        }
    >>> gs = GlyphSet(glyphs)
    >>> gs
    <GlyphSet 2 glyphs>
    >>> gs['A']
    <GlyphData A>
    >>> gs['B']
    >>> gd = gs['Aacute']
    >>> gd.base
    'A'
    >>> gd.accents
    ['acute']
    >>> gd.comment
    'Á A WITH ACUTE, LATIN CAPITAL LETTER'
    """

    # For doc-testing only. Redefine in inheriting classes.
    GLYPH_DATA = {}

    def __init__(self, glyphData=None):
        self.name = self.__class__.__name__
        if glyphData is None:
            glyphData = self.GLYPH_DATA
        self.glyphs = deepcopy(glyphData) # Deep copy the data, in case it's altered in the instance.

    def __repr__(self):
        return(f'<{self.__class__.__name__} {len(self.glyphs)} glyphs>')

    def __getitem__(self, gName):
        return self.glyphs.get(gName, None)

    def get(self, gName, default=None):
        return self.glyphs.get(gName, default) 

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])



