# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   glyphSet.py
#
from copy import deepcopy
import codecs
import os

try:
    from assistantLib.assistantParts.glyphsets.glyphData import *
    from assistantLib.assistantParts.glyphsets.glyphSet_anchors import (_TOP, _BOTTOM, _RING, _MIDDLE, _OGONEK, _VERT, _DOT, _TILDE, _TONOS, _HORN, _MIDDLE,
        _TOP_ANCHORS, _MIDDLE_ANCHORS, _BOTTOM_ANCHORS, _OGONEK_ANCHORS, _DOT_ANCHORS, _TONOS_ANCHORS, _VERT_ANCHORS) 
except ModuleNotFoundError:
    from glyphData import *
    from glyphSet_anchors import (_TOP, _BOTTOM, _RING, _MIDDLE, _OGONEK, _VERT, _DOT, _TILDE, _TONOS, _HORN, _MIDDLE,
        _TOP_ANCHORS, _MIDDLE_ANCHORS, _BOTTOM_ANCHORS, _OGONEK_ANCHORS, _DOT_ANCHORS, _TONOS_ANCHORS, _VERT_ANCHORS) 

class GlyphSet:
    """GlyphSet behaves like a dictionary of GlyphData instances.

    >>> from glyphData import *
    >>> from glyphSet_anchors import *
    >>> glyphs = {}
    >>> glyphs['A'] = GD(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', anchors=(TOP_, MIDDLE_, BOTTOM_), comment='A Uppercase Alphabet, Latin', gid=35)
    >>> glyphs['Aacute'] = GD(l='A', r='A', uni=193, c='Á', name='Aacute', srcName='Aacute', hex='00c1', anchors=(TOP_, MIDDLE_, BOTTOM_),  base='A', accents=['acutecmb'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER', gid=130)
    >>> gs = GlyphSet(glyphs)
    >>> gs
    <GlyphSet 2 glyphs>
    >>> gs.saveGlyphSetSource() # Save Python source of the glyphset into _export/Exported_GlyphSet.py
    >>> gd = gs['A']
    >>> gd
    <GlyphData A>
    >>> gd.anchors
    ('top', 'middle', 'bottom')
    >>> gs['B']
    >>> gd = gs['Aacute']
    >>> gd.c
    'Á'
    >>> gd.base
    'A'
    >>> gd.accents
    ['acutecmb']
    >>> gd.components
    ['A', 'acutecmb']
    >>> gd.comment
    'Á A WITH ACUTE, LATIN CAPITAL LETTER'

    """

    # For doc-testing only. Redefine in inheriting classes.
    GLYPH_DATA = {} # Key is glyph name, value is GlyphData instance

    def __init__(self, glyphData=None):
        if glyphData is None:
            glyphData = self.GLYPH_DATA # Redefined by inheriting class
        self.glyphs = deepcopy(glyphData) # Deep copy the data, in case it's altered by the instance.

        self._unicode2GlyphName = {} # Key is unicode, value is glyph name
        self._anchors = set() # Names of anchors 
        for gName, gd in sorted(self.glyphs.items()):
            if gd.uni:
                #assert gd.uni not in UNICODE2GLYPH, ("Unicode %04x already defined for /%s" % (gd.uni, gName))
                self._unicode2GlyphName[gd.uni] = gd.name
        
            gdBase = None
            if gd.base is not None: # If there is a base defined, take the x-ref base reference.
                gdBase = gd.base
                gd.composites.add(gName)
            '''
            for accentName in gd.accents: # It's an accent, x-ref this glyph to accents
                if accentName in ACCENT_DATA:
                    ad = ACCENT_DATA[accentName]
                    ad['composites'].add(gName)
                    accentAnchor = ad['anchor']
                    if gdBase is not None:  
                        gdBase.anchors.add(CONNECTED_ANCHORS[accentAnchor])
                    gdAccent = gds[accentName]
                    gdAccent.anchors.add(accentAnchor)
            '''

    def __repr__(self):
        return(f'<{self.__class__.__name__} {len(self.glyphs)} glyphs>')

    def __getitem__(self, gName):
        return self.glyphs.get(gName, None)

    def checkFixFromFont(self, f):
        """Check the validity of unicode, components, achors, etc."""
        for gName in sorted(f.keys()):
            g = f[gName]
            if not g.name in self.glyphs:
                print(f'### Missing glyph /{g.name}')
                self.glyphs[g.name] = GlyphData(name=g.name)
            gs = self.glyphs[g.name]
            for cIndex, component in enumerate(g.components):
                if cIndex == 0:
                    if gs.base != component.baseGlyph:
                        print(f'### /{g.name} has wrong base glyph /{component.baseGlyph} in component {cIndex}, should be /{gs.base}?')

                elif not component.baseGlyph in gs.accents:
                    print(f'### /{g.name} has wrong accent glyph /{component.baseGlyph} in component {cIndex}, should one of /{gs.accents}?')
            anchors = []
            if g.name in TOP_ANCHORS:
                anchors.append(TOP_)                   
            if g.name in MIDDLE_ANCHORS:
                anchors.append(MIDDLE_)                   
            if g.name in BOTTOM_ANCHORS:
                anchors.append(BOTTOM_)                   
            if g.name in OGONEK_ANCHORS:
                anchors.append(OGONEK_)                   
            if g.name in DOT_ANCHORS:
                anchors.append(DOT_)                   
            if g.name in TONOS_ANCHORS:
                anchors.append(TONOS_)                   
            if g.name in VERT_ANCHORS:
                anchors.append(VERT_)                   
        
            if g.name in _TOP_ANCHORS:
                anchors.append(_TOP)                   
            if g.name in _MIDDLE_ANCHORS:
                anchors.append(_MIDDLE)                   
            if g.name in _BOTTOM_ANCHORS:
                anchors.append(_BOTTOM)                   
            if g.name in _OGONEK_ANCHORS:
                anchors.append(_OGONEK)                   
            if g.name in _DOT_ANCHORS:
                anchors.append(_DOT)                   
            if g.name in _TONOS_ANCHORS:
                anchors.append(_TONOS)                   
            if g.name in _VERT_ANCHORS:
                anchors.append(_VERT)                   
        
            gs.anchors = anchors

    def get(self, gName, default=None):
        return self.glyphs.get(gName, default) 

    def keys(self):
        return self.glyphs.keys()

    def unicode2GlyphName(self, uni):
        return self._unicode2GlyphName.get(uni)

    def saveGlyphSetSource(self):
        """Write Python code source for the current self.GLYPH_DATA table."""
        fileName = 'Exported_' + self.__class__.__name__ + '.py'
        filePath = '/'.join(__file__.split('/')[:-1]) + '/_export/' # Get the directory path that this script is in.
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        out = codecs.open(filePath + fileName, 'w', encoding='utf8')
        out.write("""# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#     Auto-generated by %s
#     %s
#
try:
    from assistantLib.assistantParts.glyphsets.glyphData import *
except ModuleNotFoundError:
    from glyphData import *

GLYPH_DATA = {
""" % (self.__class__.__name__, fileName))
        initial = None
        for gName, gd in sorted(self.glyphs.items()):
            if initial != gName[0]:
                initial = gName[0]
                out.write(f'\n        #   {initial}\n\n')
            out.write(gd.asSourceLine())
        out.write('}\n')
        out.close()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])



