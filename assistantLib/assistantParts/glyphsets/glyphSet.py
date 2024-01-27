# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   glyphSet.py
#
from copy import deepcopy

from glyphData import GD

class GlyphSet:
    """GlyphSet behaves like a dictionary of GlyphData instances.

    >>> gs = GlyphSet()
    >>> gs
    <GlyphSet 15 glyph>
    >>> gs['A']
    <GlyphData A>
    >>> gs['B']
    None
    """

    # For doc-testing only. Redefine in inheriting classes.
    GLYPH_DATA = {
        '.notdef': GD(uni=None, c=None, gid=0, name='.notdef', srcName='.notdef', hex=None),
        '.null': GD(uni=0, unicodes=(0, 13), c=None, gid=1, name='.null', srcName='.null', hex='0000'),
        'A': GD(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', comment='A Uppercase Alphabet, Latin', gid=35),
        'A-cy': GD(l='A', r='A', uni=1040, c='А', name='A-cy', srcName='A-cy', hex='0410', base='A', gid=661),
        'AE': GD(l='A', r='E', uni=198, c='Æ', name='AE', srcName='AE', hex='00c6', comment='Æ ligature ae, latin capital', gid=135),
        'AEacute': GD(l='A', r='E', uni=508, c='Ǽ', name='AEacute', srcName='AEacute', hex='01fc', base='AE', accents=['acute'], comment='Ǽ LATIN CAPITAL LETTER AE WITH ACUTE', gid=445),
        'AEmacron': GD(l='A', r='E', uni=482, c='Ǣ', name='AEmacron', srcName='uni01E2', hex='01e2', base='AE', accents=['macron'], gid=419),
        'Aacute': GD(l='A', r='A', uni=193, c='Á', name='Aacute', srcName='Aacute', hex='00c1', base='A', accents=['acute'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER', gid=130),
        'Abreve': GD(l='A', r='A', uni=258, c='Ă', name='Abreve', srcName='Abreve', hex='0102', base='A', accents=['breve'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE', gid=195),
        'Abreve-cy': GD(l='A', r='A', uni=1232, c='Ӑ', name='Abreve-cy', srcName='Abreve-cy', hex='04d0', base='A', accents=['brevecomb.component'], gid=853),
        'Abreve.component': GD(uni=None, c=None, w=0, name='Abreve.component', srcName='Abreve.component', hex=None, gid=1594),
        'Abreve.component1': GD(uni=None, c=None, w=0, name='Abreve.component1', srcName='Abreve.component1', hex=None, gid=1595),
        'Abreve.component2': GD(uni=None, c=None, w=0, name='Abreve.component2', srcName='Abreve.component2', hex=None, gid=1596),
        'Abreve.component3': GD(uni=None, c=None, w=0, name='Abreve.component3', srcName='Abreve.component3', hex=None, gid=1597),
        'Abreveacute': GD(l='A', r='A', uni=7854, c='Ắ', name='Abreveacute', srcName='Abreveacute', hex='1eae', base='A', accents=['Abreve.component'], comment='Ắ LATIN CAPITAL LETTER A WITH BREVE AND ACUTE', gid=1097),
    }
    def __init__(self):
        self.glyphs = deepcopy(self.GLYPH_DATA) # Deep copy the data, in case it's altered in the instance.

    def __repr__(self):
        return(f'<{self.__class__.__name__} {len(self.glyphs)} glyph>')

    def __getitem__(self, gName):
        return self.glyphs.get(gName) 

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])



