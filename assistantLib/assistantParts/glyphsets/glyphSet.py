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

# Different sizes of standard glyph set
from assistantLib.assistantParts.glyphsets.Latin_A_set import (LATIN_A_SET_NAME, LATIN_A_SET, LATIN_A_SET_NAME_ITALIC, LATIN_A_SET_ITALIC) 
from assistantLib.assistantParts.glyphsets.Latin_S_set import (LATIN_S_SET_NAME, LATIN_S_SET, LATIN_S_SET_NAME_ITALIC, LATIN_S_SET_ITALIC, 
    SC_NAMES, 
    # SUPS_SINF_NAMES, Deprecated, these are in the GlyphSet tables now. 
    # NUMR_DNOM_NAMES, Deprecated
    TAB_NAMES, ONUM_NAMES)
from assistantLib.assistantParts.glyphsets.Latin_M_set import LATIN_M_SET_NAME, LATIN_M_SET, LATIN_M_SET_NAME_ITALIC, LATIN_M_SET_ITALIC
from assistantLib.assistantParts.glyphsets.Latin_L_set import LATIN_L_SET_NAME, LATIN_L_SET, LATIN_L_SET_NAME_ITALIC, LATIN_L_SET_ITALIC
from assistantLib.assistantParts.glyphsets.Latin_XL_set import LATIN_XL_SET_NAME, LATIN_XL_SET, LATIN_XL_SET_NAME_ITALIC, LATIN_XL_SET_ITALIC
from assistantLib.assistantParts.glyphsets.Cyrillic_set import CYRILLIC_SET_NAME, CYRILLIC_SET, CYRILLIC_SET_NAME_ITALIC, CYRILLIC_SET_ITALIC
# Deprecated
#from assistantLib.assistantParts.glyphsets.TYPETR_full_set import TYPETR_FULL_SET_NAME, TYPETR_FULL_SET

STANDARD_GLYPH_SETS = {
    LATIN_A_SET_NAME: LATIN_A_SET,
    LATIN_A_SET_NAME_ITALIC: LATIN_A_SET_ITALIC,
    LATIN_S_SET_NAME: LATIN_S_SET,
    LATIN_S_SET_NAME_ITALIC: LATIN_S_SET_ITALIC,
    LATIN_M_SET_NAME: LATIN_M_SET,
    LATIN_M_SET_NAME_ITALIC: LATIN_M_SET_ITALIC,
    LATIN_L_SET_NAME: LATIN_L_SET,
    LATIN_L_SET_NAME_ITALIC: LATIN_L_SET_ITALIC,
    LATIN_XL_SET_NAME: LATIN_XL_SET,
    LATIN_XL_SET_NAME_ITALIC: LATIN_XL_SET_ITALIC,
    #CYRILLIC_SET_NAME: CYRILLIC_SET, # Add this "manually" in the Assistant as: GS.appendGlyphSet(CYRILLIC_SET)
}

class GlyphSet:
    """GlyphSet behaves like a dictionary of GlyphData instances.
    GlyphData instances are records that keep information about each individual glyph.

    >>> from glyphData import *
    >>> from anchorData import AD
    >>> from Latin_S_set import LATIN_S_SET_NAME
    >>> glyphs = {}
    >>> glyphs['A'] = GD(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', anchors=(AD.TOP_, AD.MIDDLE_, AD.BOTTOM_), comment='A Uppercase Alphabet, Latin', gid=35)
    >>> glyphs['Aacute'] = GD(l='A', r='A', uni=193, c='Á', name='Aacute', srcName='Aacute', hex='00c1', anchors=(AD.TOP_, AD.MIDDLE_, AD.BOTTOM_),  base='A', accents=['acutecmb'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER', gid=130)
    >>> gs = GlyphSet(glyphData=glyphs) # Simple one
    >>> gs
    <GlyphSet 2 glyphs>
    >>> gs = GlyphSet(name=LATIN_S_SET_NAME, sc=True, sinf=True, tab=True)
    >>> gs.saveGlyphSetSource() # Save Python source of the glyphset into _export/Exported_GlyphSet.py
    >>> gd = gs['A']
    >>> gd
    <GlyphData A>
    >>> sorted(gd.anchors)
    ['bottom', 'middle', 'ogonek', 'tonos', 'top']
    >>> gs['B']
    <GlyphData B>
    >>> gd = gs['Aacute']
    >>> gd.c
    'Á'
    >>> gd.base
    'A'
    >>> gd.accents
    ['acutecmb']
    >>> gd.componentNames
    ['A', 'acutecmb']
    >>> gd.comment
    'Á A WITH ACUTE, LATIN CAPITAL LETTER'
    >>> #sorted(gs.glyphs.keys())
    >>> gd = gs['A.sc']
    >>> gd.name
    'A.sc'
    >>> gd = gs['one.tab']
    >>> gd.name
    'one.tab'
    >>> gd.w
    'zero.tab'
    >>> gd = gs['one.sinf']
    >>> gd.name
    'one.sinf'
    >>> gd.l, gd.r
    ('zero.sinf', 'zero.sinf')

    """

    # For doc-testing only. Redefine in inheriting classes.
    GLYPH_DATA = {} # Key is glyph name, value is GlyphData instance

    def __init__(self, name=None, glyphData=None, sc=False, superior=False, tab=False, onum=False, alt=False, verbose=False):
        """Answer the request type of glyphset. 
        """
        self.name = name
        self.verbose = verbose # Some additional remarks on exceptions and errors

        self.hasSc = sc
        self.hasSuperior = superior
        self.hasTab = tab
        self.hasOnum = onum
        self.hasAlt = alt

        if name in STANDARD_GLYPH_SETS:
            glyphData  = STANDARD_GLYPH_SETS[name]
        elif glyphData is None:
            glyphData = self.GLYPH_DATA # Redefined by inheriting class
        self.glyphs = deepcopy(glyphData) # Deep copy the data, in case it's altered by the instance.

        if sc:
            self._appendSmallCaps()

        if tab:
            self._appendTab()

        # Deprecated, these are hard-coded in the "S" glyphset table now
        #if superior:
        #    self._appendSuperiorInferior()
        #    self._appendDnomNumrSupsSinf()

        if onum: # Lowercase (oldstyle) figures
            self._appendOnum()

        self.unicode2GlyphName = {} # Key is unicode, value is glyph name
        self.anchor2GlyphNames = {} # Key is names of anchors. Value if a list of glyph names that implement the anchor.
        self.anchor2DiacriticNames = {} # Key is names of anchors, Value is a list of diacritics that support the anchor placement.
        self.diacritic2GlyphNames = {} # Key is name of a diacritic. Value is a list of glyph names that use the diacritic as component

        for gName, gd in sorted(self.glyphs.items()):

            if gd.uni:
                #assert gd.uni not in UNICODE2GLYPH, ("Unicode %04x already defined for /%s" % (gd.uni, gName))
                self.unicode2GlyphName[gd.uni] = gd.name
            # Make the dict of disacritics --> List of glyphs that use them
            for componentName in gd.componentNames:
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

    def _appendSmallCaps(self):
        """Append small caps for every glyphs in SC_NAMES."""
        ext = '.sc'
        for gName in SC_NAMES:
            if gName in self.glyphs:
                gNameSc = gName + ext
                if gNameSc in self.glyphs: # Only if it does not already exist
                    if self.verbose:
                        print(f'### _appendSmallCaps: GlyphData /{gNameSc} already exists')
                else:
                    self.glyphs[gNameSc] = gd = deepcopy(self.glyphs[gName])
                    gd.name = gNameSc
                    gd.uni = gd.hex = gd.c = None
                    if gd.l in SC_NAMES:
                        gd.l += ext
                    if gd.r in SC_NAMES:
                        gd.r += ext
                    if gd.l2r in SC_NAMES:
                        gd.l2r += ext
                    if gd.r2l in SC_NAMES:
                        gd.r2l += ext
                    if gd.w in SC_NAMES: 
                        gd.w += ext
                    # Do anchors, slip exception for smallcaps tonos
                    anchorNames = []
                    for anchorName in gd.anchors:
                        if not (anchorName == 'topleft' and gd.isSc):
                            anchorNames.append(anchorName)
                    gd.anchors = anchorNames 
                    # Do accent alteration in another loop, since not all .sc may have been created yet.
                    # Also there is a problem for Cyrillic added before the Greek, since Gamma.sc does not exist yet.
                    gd.srcName = gName
                    gd.isLower = False
                    gd.overshoot = gd.CAT_SC_OVERSHOOT

        for gName in SC_NAMES: # Scmall cap component and anchor conversions
            if gName in self.glyphs:
                gNameSc = gName + ext
                gd = self.glyphs[gNameSc] # We know here that is already must exist
                if gd.base is not None and gd.base + ext in self.glyphs:
                    gd.base = (gd.base + ext).replace('.uc', '')

                # Also convert these references, e.g. for /Ohorn glyphs
                if gd.anchorTopX is not None and gd.anchorTopX + ext in self.glyphs:
                    gd.anchorTopX += ext
                if gd.anchorTopY is not None and gd.anchorTopY + ext in self.glyphs:
                    gd.anchorTopY += ext

                accents = []
                for accent in gd.accents:
                    if accent + ext in self.glyphs:
                        accents.append(accent + ext)
                    else:
                        accents.append(accent)
                gd.accents = []
                for accent in accents: # Make a copy, because we're going to change the .uc to lowercase diacritics
                    # /tail.component-cy.case replaced to /tail.component-cy 
                    gd.accents.append(accent.replace('.uc', ''))

    def _appendTab(self):
        tabExt = '.tab'
        for gName in TAB_NAMES:
            if gName in self.glyphs:
                gNameTab = gName + tabExt
                if gNameTab not in self.glyphs: # Only if it does not exist already
                    self.glyphs[gNameTab] = gd = deepcopy(self.glyphs[gName])
                    gd.name = gNameTab
                    gd.uni = gd.hex = gd.c = None
                    gd.l = gd.CAT_CENTER
                    gd.w = gd.CAT_TAB_WIDTH
                    gd.base = gName # Assuming that the tab as component of the main glyph. # Otherwise make the BG manually
                #else:
                #    print(f'### _appendTab: GlyphData /{gNameTab} already exists')

    def _appendSuperiorInferior(self):
        for ext in ('superior', 'inferior'):
            for gName in SUPS_SINF_NAMES:
                if gName in self.glyphs:
                    gNameExt = gName + ext
                    if gNameExt not in self.glyphs: # Only if it does not exist already
                        self.glyphs[gNameExt] = gd = deepcopy(self.glyphs[gName])
                        gd.name = gNameExt
                        gd.uni = gd.hex = gd.c = None
                        gd.isLower = False
                        gd.overshoot = gd.CAT_SUPERIOR_OVERSHOOT
                        if ext != 'superior':
                            gd.l = gd.r = 'zerosuperior'
                            gd.base = gName + 'superior'
                        else:
                            gd.base = None
                    #else:
                    #    print(f'### _appendSuperiorInferiorDnomNumr: GlyphData /{gNameExt} already exists')

    def _appendDnomNumrSupsSinf(self):
        for ext in ('.dnom', '.numr', '.sups', '.sinf'):
            for gName in NUMR_DNOM_NAMES:
                if gName in self.glyphs:
                    gNameExt = gName + ext
                    if gNameExt not in self.glyphs: # Only if it does not exist already
                        self.glyphs[gNameExt] = gd = deepcopy(self.glyphs[gName])
                        gd.name = gNameExt
                        gd.uni = gd.hex = gd.c = None
                        gd.isLower = False
                        gd.overshoot = gd.CAT_SUPERIOR_OVERSHOOT
                        gd.l = gd.r = 'zerosuperior'
                        gd.base = gName + 'superior'
                    #else:
                    #    print(f'### _appendSuperiorInferiorDnomNumr: GlyphData /{gNameExt} already exists')


    def _appendOnum(self):
        tabExt = '.onum'
        for gName in ONUM_NAMES:
            if gName in self.glyphs:
                gNameExt = gName + tabExt
                if gNameExt in self.glyphs: # Only if it does not exist already
                    if self.verbose:
                        print(f'### _appendOnum: GlyphData /{gNameExt} already exists')
                else:
                    self.glyphs[gNameExt] = gd = deepcopy(self.glyphs[gName])
                    gd.name = gNameExt
                    gd.uni = gd.hex = gd.c = None
                    if '.tab' not in gName:
                        gd.l = gd.r = gName
                    elif gd.base is not None:
                        gd.base = gName.replace('.tab', '.onum')

    def appendGlyphSet(self, gs):
        for gdName, gd in gs.items():
            self.glyphs[gdName] = deepcopy(gd)
        # Make sure to add the derivatives, such as .sc and .tab
        if self.hasSc:
            self._appendSmallCaps()      
        # Deprecated, these are hard-coded in the "S" table now      
        #if self.hasSuperior:
        #    self._appendSuperiorInferior()
        #    self._appendDnomNumrSupsSinf()
        if self.hasTab:
            self._appendTab()
        if self.hasOnum: # Lowercase (oldstyle) figures
            self._appendOnum()

    def __repr__(self):
        return(f'<{self.__class__.__name__} {len(self.glyphs)} glyphs>')

    def __getitem__(self, gName):
        return self.glyphs.get(gName, None)

    def __setitem__(self, gName, gd):
        self.glyphs[gName] = gd

    def keys(self):
        return self.glyphs.keys()

    def values(self):
        return self.glyphs.values()

    def items(self):
        return self.glyphs.items()

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

        #print(f'... Exported glyphs {filePath}')
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


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])



