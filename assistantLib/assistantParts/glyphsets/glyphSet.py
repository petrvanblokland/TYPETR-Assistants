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

from assistantLib.assistantParts.glyphsets.glyphData import *
from assistantLib.assistantParts.glyphsets.anchorData import AD 

class GlyphSet:
    """GlyphSet behaves like a dictionary of GlyphData instances.
    GlyphData instances are records that keep information about each individual glyph.

    >>> from glyphData import *
    >>> from anchorData import AD
    >>> glyphs = {}
    >>> glyphs['A'] = GD(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', anchors=(AD.TOP_, AD.MIDDLE_, AD.BOTTOM_), comment='A Uppercase Alphabet, Latin', gid=35)
    >>> glyphs['Aacute'] = GD(l='A', r='A', uni=193, c='Á', name='Aacute', srcName='Aacute', hex='00c1', anchors=(AD.TOP_, AD.MIDDLE_, AD.BOTTOM_),  base='A', accents=['acutecmb'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER', gid=130)
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

        self.unicode2GlyphName = {} # Key is unicode, value is glyph name
        self.anchor2GlyphNames = {} # Key is names of anchors. Value if a list of glyph names that implement the anchor.
        self.anchor2DiacriticNames = {} # Key is names of anchors, Value is a list of diacritics that support the anchor placement.
        self.diacritic2GlyphNames = {} # Key is name of a diacritic. Value is a list of glyph names that use the diacritic as component

        for gName, gd in sorted(self.glyphs.items()):
            if gd.uni:
                #assert gd.uni not in UNICODE2GLYPH, ("Unicode %04x already defined for /%s" % (gd.uni, gName))
                self.unicode2GlyphName[gd.uni] = gd.name
            # Make the dict of disacritics --> List of glyphs that use them
            for componentName in gd.components:
                gdc = self.glyphs.get(componentName)
                if gdc is not None and gdc.isDiacritic:
                    if not gdc.name in self.diacritic2GlyphNames:
                        self.diacritic2GlyphNames[gdc.name] = []
                    self.diacritic2GlyphNames[gdc.name].append(gd.name)

            gdBase = None
            if gd.base is not None: # If there is a base defined, take the x-ref base reference.
                gdBase = gd.base
                gd.composites.add(gName)

            if gd.anchors is not None:
                for anchorName in gd.anchors:
                    if not anchorName in self.anchor2GlyphNames:
                        self.anchor2GlyphNames[anchorName] = []
                    self.anchor2GlyphNames[anchorName].append(gName)
                    if not anchorName in self.anchor2DiacriticNames:
                        self.anchor2DiacriticNames[anchorName] = []
                    self.anchor2DiacriticNames[anchorName].append(gName)

    def __repr__(self):
        return(f'<{self.__class__.__name__} {len(self.glyphs)} glyphs>')

    def __getitem__(self, gName):
        return self.glyphs.get(gName, None)

    def getAnchorGlyphNames(self, anchorName):
        """Answer the list of glyphs that have this anchor"""
        return self.anchor2GlyphNames.get(anchorName)

    def getAnchorDiacriticNames(self, anchorName):
        """Answer the list of diacritic glyph names that have this anchor"""
        return self.anchor2DiacriticNames.get(anchorName)

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
                anchors.append(AD.TOP_)                   
            if g.name in MIDDLE_ANCHORS:
                anchors.append(AD.MIDDLE_)                   
            if g.name in BOTTOM_ANCHORS:
                anchors.append(AD.BOTTOM_)                   
            if g.name in OGONEK_ANCHORS:
                anchors.append(AD.OGONEK_)                   
            if g.name in DOT_ANCHORS:
                anchors.append(AD.DOT_)                   
            if g.name in TONOS_ANCHORS:
                anchors.append(AD.TONOS_)                   
            if g.name in VERT_ANCHORS:
                anchors.append(AD.VERT_)                   
        
            if g.name in _TOP_ANCHORS:
                anchors.append(AD._TOP)                   
            if g.name in _MIDDLE_ANCHORS:
                anchors.append(AD._MIDDLE)                   
            if g.name in _BOTTOM_ANCHORS:
                anchors.append(AD._BOTTOM)                   
            if g.name in _OGONEK_ANCHORS:
                anchors.append(AD._OGONEK)                   
            if g.name in _DOT_ANCHORS:
                anchors.append(AD._DOT)                   
            if g.name in _TONOS_ANCHORS:
                anchors.append(AD._TONOS)                   
            if g.name in _VERT_ANCHORS:
                anchors.append(AD._VERT)                   
        
            gs.anchors = anchors

    def get(self, gName, default=None):
        return self.glyphs.get(gName, default) 

    def keys(self):
        return self.glyphs.keys()

    def fromFont(self, f):
        """If a new project starts, and there is no standard glyph set available, this method
        creates the glyphData records based on the contents of @f"""
        for gName in sorted(f.keys()):
            g = f[gName]
            base = None
            accents = []
            if g.components:
                base = g.components[0].baseGlyph
                if len(g.components) > 1:
                    for component in g.components[1:]:
                        accents.append(component.baseGlyph)
            anchors = []
            for a in g.anchors:
                anchors.append(a.name)
            self.glyphs[gName] = GlyphData(name=gName, uni=g.unicode, base=base, accents=accents,
                anchors=anchors,
            )
        
    def saveGlyphSetSource(self, filePath=None):
        """Write Python code source for the current self.GLYPH_DATA table."""
        if filePath is None:
            fileName = f'Exported_{self.__class__.__name__}.py'
            dirPath = '/'.join(__file__.split('/')[:-1]) + '/_export/' # Get the directory path that this script is in.
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            filePath = dirPath + fileName

        print(f'... Exported glyphs {filePath}')
        out = codecs.open(filePath, 'w', encoding='utf8')
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
""" % (self.__class__.__name__, filePath))
        initial = None
        for gName, gd in sorted(self.glyphs.items()):
            if initial != gName[0]:
                initial = gName[0]
                out.write(f'\n        #   {initial}\n')
            out.write(gd.asSourceLine())
        out.write('}\n')
        out.close()



