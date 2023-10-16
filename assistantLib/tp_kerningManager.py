# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   tp_kerningSamples.py
#
import weakref

# We use Letterrors' Similarity to find matching groups
# Install cosineSimilarity extensions via Mechanic 2
import cosineSimilarity
from cosineSimilarity import cosineSimilarity, SimilarGlyphsKey

from assistantLib.kerningSamples import SAMPLES 

class KerningManager:
    """Generic kerning manager"""

    def __init__(self, f, features=None, sample=None, simT=0.95, 
            simSameCategory=True, simSameScript=True, simClip=300, simZones=None,
            automaticGroups=True, verbose=True):
        assert f is not None
        self.f = f # Stored as weakref property
        if features is None:
            features = {}
        self.features = features # Dictionary of open type features to show in the samples

        self.verbose = verbose

        # Similarity parameters
        self.simT = simT # the confidence threshold. Only show results > simT
        self.simSameCategory = simSameCategory # only show glyphs in the same unicode category
        self.simSameScript = simSameScript # only show glyphs in the same unicode script
        self.simClip = simClip # clip is how deep the profile should be, measured from the margin inward.
        # zones are pairs of y values of the areas we specifically want to compare.
        # useful if you want to exclude certain bands.
        # this is an example, your values might be different:
        #zones = []
        #zones.append((f.info.xHeight, f.info.unitsPerEm+f.info.descender))
        #zones.append((0, f.info.xHeight))
        #zones.append((f.info.descender, 0))
        #zones = tuple(zones)    # make sure the zones are a tuple
        #zones = None            # or make zones None to scane the full height
        self.simZones = simZones

        # X-ref unicode and names
        self.uni2glyphName = {}
        self.chr2glyphName = {}
        for g in f:
            if g.unicode:
                self.uni2glyphName[g.unicode] = g.name
                self.chr2glyphName[chr(g.unicode)] = g.name

        self.automaticGroups = automaticGroups # Generated new groups for glyphs that don't belong.

        # Do some caching on groups
        self.glyphName2GroupName1 = {}
        self.glyphName2Group1 = {}
        self.glyphName2GroupName2 = {}
        self.glyphName2Group2 = {}
        for groupName, group in f.groups.items():
            if 'kern1' in groupName:
                for glyphName in group:
                    self.glyphName2GroupName1[glyphName] = groupName
                    self.glyphName2Group1[glyphName] = group
            elif 'kern2' in groupName:
                for glyphName in group:
                    self.glyphName2GroupName2[glyphName] = groupName
                    self.glyphName2Group2[glyphName] = group

        if sample is None: # Allows to define the sample, avoiding multiple generators if a whole family is open.
            sample = self._initSample() 
        self.sample = sample

    def _get_f(self):
        return self._f
        #return self._f()
    def _set_f(self, f):
        self._f = f
        #self._f = weakref.ref(f)
    f = property(_get_f, _set_f)

    #   G R O U P S

    def addGlyph2Group1(self, g, groupName):
        print(g.name, groupName)
        
    def addGlyph2Group2(self, g, groupName):
        print(g.name, groupName)
        
    #   S I M I L A R I T Y

    def getSimilar1(self, g):
        """Answer the similar representation from the glyph with SimilarGlyphsKey"""
        return self._getSimilar(g, 'right')

    def getSimilar2(self, g):
        """Answer the similar representation from the glyph with SimilarGlyphsKey"""
        return self._getSimilar(g, 'left')

    def _getSimilar(self, g, side):
        return g.getRepresentation(SimilarGlyphsKey,
            threshold=self.simT, 
            sameUnicodeClass=self.simSameCategory,
            sameUnicodeScript=self.simSameScript,
            zones=self.simZones,
            side=side,
            clip=self.simClip
        )
    def getSimilarGroups1(self, g):
        """Answer a list of group names that are similar to g, including the group that g is already in.
        If there is more than one group, either g should change or the groups should be merged."""
        simGroups = {}
        for confidence, simGroup in self.getSimilar1(g).items():
            for gName in simGroup:
                groupName = self.glyphName2GroupName1.get(gName)
                if groupName is not None:
                    simGroups[groupName] = self.f.groups[groupName]
                elif self.automaticGroups:
                    groupName = f'public.kern1.{gName}'
                    group = [gName]
                    simGroups[groupName] = self.f.groups[groupName] = group
                    self.glyphName2GroupName1[gName] = groupName
                    if self.verbose:
                        print(f'... Add group {groupName} {group}')
                else:
                    simGroups[f'({gName})'] = [gName]
        return simGroups

    def getSimilarGroups2(self, g):
        """Answer a list of group names that are similar to g, including the group that g is already in.
        If there is more than one group, either g should change or the groups should be merged."""
        simGroups = {}
        for confidence, simGroup in self.getSimilar2(g).items():
            for gName in simGroup:
                groupName = self.glyphName2GroupName2.get(gName)
                if groupName is not None:
                    simGroups[groupName] = self.f.groups[groupName]
                elif self.automaticGroups:
                    groupName = f'public.kern2.{gName}'
                    group = [gName]
                    simGroups[groupName] = self.f.groups[groupName] = group
                    self.glyphName2GroupName2[gName] = groupName
                    if self.verbose:
                        print(f'... Add group {groupName} {group}')
                else:
                    simGroups[f'({gName})'] = [gName]
        return simGroups

    #   S P A C I N G

    def getLeftMarginSrc(self, g):
        """Answer the angled left margin source glyph, according to the base glyph of group2"""
        groupName = self.glyphName2GroupName2.get(g.name)
        if groupName is None:
            return None
        baseGlyphName = groupName.replace('public.kern2.', '')
        assert baseGlyphName in self.f
        return self.f[baseGlyphName]
        
    def getRightMarginSrc(self, g):
        """Answer the angled right margin source glyph, according to the base glyph of group1"""
        groupName = self.glyphName2GroupName1.get(g.name)
        if groupName is None:
            return None
        baseGlyphName = groupName.replace('public.kern1.', '')
        assert baseGlyphName in self.f
        return self.f[baseGlyphName]
        
    #   S A M P L E

    def _initSample(self):
        sample = [] # List of glyph names
        for c in SAMPLES:
            gName = self.chr2glyphName.get(c)
            if gName is not None:
                sample.append(gName)

        return sample

        """
            assert self.f() is not None
            SPECIMEN_RF = KerningSample()
            SPECIMEN_RF.append(KL(PRE))
            #SPECIMEN_PDF.append(KL(ALICE_TEXT))
            #SPECIMEN_PDF.append(KL(DIACRITICS))
            SPECIMEN_RF.append(KL(CAPS))
            SPECIMEN_RF.append(KL(LC))
            SPECIMEN_RF.append(KL(names=LIGATURE_ACCENTS))

            for chars in (LC_CHARS, CAP_CHARS):
                for char1 in 'JR':
                    for char2 in chars:
                        SPECIMEN_RF.append(KL(char1))
                        SPECIMEN_RF.append(KL(char2))
                        SPECIMEN_RF.append(KL(char1, aalt=True))
                        SPECIMEN_RF.append(KL(char2))

            #SPECIMEN_RF.append(KL(LC_ACCENTS))
            SPECIMEN_RF.append(KL(LC_PUNCTUATIONS))
            SPECIMEN_RF.append(KL(CAPS_LC))
            #SPECIMEN_RF.append(KL(CAPS_LC_ACCENTS))
            SPECIMEN_RF.append(KL(CAPS_PUNCTUATIONS))
            SPECIMEN_RF.append(KL(FIGURES))
            SPECIMEN_RF.append(KL(FIGURES, onum=True))
            SPECIMEN_RF.append(KL(FIGURES, tnum=True))
            SPECIMEN_RF.expandFractions(FIGURES_FRACTIONS)
            #SPECIMEN_RF.append(KL(LCWORDS_PAGE))
            #SPECIMEN_RF.append(KL(FIGURE_WORDS))
            # Small caps
            SPECIMEN_RF.append(KL(PRE, smcp=True))
            SPECIMEN_RF.append(KL(LC, smcp=True))
            SPECIMEN_RF.append(KL(LC_ACCENTS, smcp=True))
            SPECIMEN_RF.append(KL(LC_PUNCTUATIONS, smcp=True))

            for char1 in 'JR':
                for char2 in CAP_CHARS:
                    SPECIMEN_RF.append(KL(char1))
                    SPECIMEN_RF.append(KL(char2))
            for char1 in 'JR':
                for char2 in CAP_CHARS:
                    SPECIMEN_RF.append(KL(char1, aalt=True))
                    SPECIMEN_RF.append(KL(char2))
            for char1 in 'JR':
                for char2 in CAP_CHARS:
                    SPECIMEN_RF.append(KL(char1, aalt=True))
                    SPECIMEN_RF.append(KL(char2, c2sc=True))

            SPECIMEN_RF.append(KL(CAPS, c2sc=True))
            SPECIMEN_RF.append(KL(CAPS_LC, smcp=True))
            #SPECIMEN_RF.append(KL(CAPS_LC_ACCENTS, smcp=True))
            #SPECIMEN_RF.append(KL(CAPS_ACCENTS, smcp=True))
            SPECIMEN_RF.append(KL(CAPS_PUNCTUATIONS, c2sc=True))
            SPECIMEN_RF.append(KL(FIGURES, smcp=True))
            SPECIMEN_RF.append(KL(FIGURES, c2sc=True))
            SPECIMEN_RF.append(KL(LCWORDS_PAGE, smcp=True))
            SPECIMEN_RF.append(KL(FIGURE_WORDS, smcp=True))

            KERNING_RF_SAMPLES = KERNING_RF_SAMPLES_ITALIC = SPECIMEN_RF.getNames()
        """

    def expandFractions(self, s):
        for c1 in s:
            for c2 in s:
                self.append(KL('0'+c1, numr=True))
                self.append(KL('⁄'))
                self.append(KL(c2+'0', dnom=True))


    def getNames(self):
        names = []
        for kl in self.kerningLines:
            names += kl.getNames(self.glyphData, self.uni2GlyphData)
        return names

    def get(self):
        s = []
        for kl in self.kerningLines:
            s += kl.s
        return ''.join(s)

    def getKerning(self, gName1, gName2):
        """Answer the kerning between gName1 and gName2.
        If there is a glyph<-->glyph kerning, then answer that.
        If there is a group<-->glyph or glyph<-->group kerning, then answer that.
        Otherwise answer the group<-->group kerning if it exists.
        Otherwise answer None. 

        3 = glyph<-->glyph
        2 = group<-->glyph
        1 = glyph<-->group
        0 or None = group<-->group
        """ 
        assert self.f is not None
        groupName1 = self.glyphName2GroupName1.get(gName1)
        groupName2 = self.glyphName2GroupName2.get(gName2)
        if None in (groupName1, groupName2):
            return 0, 0, None

        groupK = self.f.kerning.get((groupName1, groupName2), 0) # Get the default group-group kerning for this pair
        if (gName1, gName2) in self.f.kerning: # Test on glyph<-->glyph kerning first
            k = self.f.kerning[(gName1, gName2)]
            pair = (gName1, gName2)
            kerningType = 3
        elif (groupName1, gName2) in self.f.kerning: # Test on group<-->glyph kerning
            k = self.f.kerning[(groupName1, gName2)]
            pair = groupName1, gName2
            kerningType = 2
        elif (gName1, groupName2) in self.f.kerning: # Test on glyph<-->group kerning
            k = self.f.kerning[gName1, groupName2]
            pair = (gName1, groupName2)
            kerningType = 1
        else: # Must be group<-->group kerning
            k = groupK
            pair = groupName1, groupName2
            kerningType = 0
        if k == groupK and kerningType: # Special kerning type is no longer needed
            del self.f.kerning[pair]
            kerningType = 0
        # Otherwise it must be group<-->group kerning or not existing
        return k, groupK, kerningType     
              
    def setKerning(self, gName1, gName2, k, kerningType=None):
        """Set the kerning between gName1 and gName2 or their groups, depending on the kerningType
        3 = glyph<-->glyph
        2 = group<-->glyph
        1 = glyph<-->group
        0 or None = group<-->group
        """
        assert self.f is not None
        assert kerningType in (None, 0, 1, 2, 3)
        if not kerningType:
            if gName1 not in self.glyphName2GroupName1:
                print(f'Glyph1 /{gName1} not in group1')
                if gName2 not in self.glyphName2GroupName2:
                    kerningType = 3 # glyph<-->glyph
                else:
                    kerningType = 1 # glyph<-->group
            if gName2 not in self.glyphName2GroupName2:
                print(f'Glyph2 /{gName2} not in group2')
                if gName1 not in self.glyphName2GroupName1:
                    kerningType = 3 # glyph<-->glyph
                else:
                    kerningType = 2 # group<-->glyph

        if not kerningType: # Can be 0 or None
            pair = self.glyphName2GroupName1[gName1], self.glyphName2GroupName2[gName2] # Test against this default
        elif kerningType == 1:
            pair = gName1, self.glyphName2GroupName2[gName2]
        elif kerningType == 2:
            pair = self.glyphName2GroupName1[gName1], gName2
        else: # kerningType == 3 glyph<-->glyph kerning
            pair = gName1, gName2
            
        #if kerningType and k == getKerning(gName1, gName2, 0)[0]: # Get kerning of group<-->group
        #    del self.f.kerning[pair] # If identical to group, then remove kerningType pair
        #elif k == 0 and pair in self.f.kerning:
        if k in (0, None) and pair in self.f.kerning: # Delete this existing pair that now gets value 0
            print('... Delete kerning %s' % str(pair))
            del self.f.kerning[pair]
        elif k: # If kerningType in (1, 2, 3) then kerning can be 0 to correct the group kerning
            print('... Set kerning %s to %d' % (pair, k))
            self.f.kerning[pair] = k



def makeSpecimenPdf(glyphData, UNI2GLYPH_DATA):
    specimen = KerningSample(GLYPH_DATA,)
    specimen.append(KL(PRE))
    specimen.append(KL(ALICE_TEXT))
    specimen.append(KL(DIACRITICS))
    specimen.append(KL(LC))
    specimen.append(KL(CAPS))

    for chars in (LC_CHARS, CAP_CHARS):
        for char1 in 'JR':
            for char2 in chars:
                specimen.append(KL(char1))
                specimen.append(KL(char2))
                specimen.append(KL(char1, aalt=True))
                specimen.append(KL(char2))

    specimen.append(KL('JR', aalt=True))
    specimen.append(KL(LC_ACCENTS))
    specimen.append(KL(LC_PUNCTUATIONS))
    specimen.append(KL(CAPS_LC))
    specimen.append(KL(CAPS_LC_ACCENTS))
    specimen.append(KL(CAPS_PUNCTUATIONS))
    specimen.append(KL(FIGURES))
    specimen.append(KL(FIGURES, onum=True))
    specimen.append(KL(FIGURES, tnum=True))
    specimen.expandFractions(FIGURES_FRACTIONS)
    specimen.append(KL(LCWORDS_PAGE))
    specimen.append(KL(FIGURE_WORDS))
    # Small caps
    specimen.append(KL(PRE, smcp=True))
    specimen.append(KL(LC, smcp=True))
    specimen.append(KL(LC_ACCENTS, smcp=True))
    specimen.append(KL(LC_PUNCTUATIONS, smcp=True))

    for char1 in 'JR':
        for char2 in CAP_CHARS:
            specimen.append(KL(char1))
            specimen.append(KL(char2))
    for char1 in 'JR':
        for char2 in CAP_CHARS:
            specimen.append(KL(char1, aalt=True))
            specimen.append(KL(char2))
    for char1 in 'JR':
        for char2 in CAP_CHARS:
            specimen.append(KL(char1, aalt=True))
            specimen.append(KL(char2, c2sc=True))

    specimen.append(KL(CAPS, c2sc=True))
    specimen.append(KL(CAPS_LC, smcp=True))
    specimen.append(KL(CAPS_LC_ACCENTS, smcp=True))
    specimen.append(KL(CAPS_ACCENTS, smcp=True))
    specimen.append(KL(CAPS_PUNCTUATIONS, smcp=True))
    specimen.append(KL(FIGURES, smcp=True))
    specimen.append(KL(FIGURES, c2sc=True))
    specimen.append(KL(LCWORDS_PAGE, smcp=True))
    specimen.append(KL(FIGURE_WORDS, smcp=True))
    return specimen


# Critical accents that go with their choice of alternative /f
LIGATURE_ACCENTS = (
    'f', 'a', 
    'f', 'aacute', 
    'f', 'aogonek', 
    'f', 'agrave', 
    'f', 'adieresis', 
    'f', 'aring', 
    'f', 'aringacute',
    'f', 'acircumflex', 
    'f', 'atilde', 
    'f', 'amacron', 
    'f', 'abreve', 
    
    'f', 'e', 
    'f', 'eacute', 
    'f', 'eogonek', 
    'f', 'egrave',  
    'f', 'edieresis', 
    'f', 'edotaccent', 
    'f', 'ecircumflex', 
    'f', 'emacron', 
    'f', 'ebreve', 
    'f', 'ecaron',
    
    'f', 'u', 
    'f', 'uacute', 
    'f', 'uhungarumlaut',
    'f', 'ugrave', 
    'f', 'udieresis', 
    'f', 'uring', 
    'f', 'ucircumflex', 
    'f', 'utilde', 
    'f', 'umacron', 
    'f', 'ubreve', 
    
    'f', 'o', 
    'f', 'oacute', 
    'f', 'oslash', 
    'f', 'ograve', 
    'f', 'odieresis', 
    'f', 'oslashacute',
    'f', 'ocircumflex', 
    'f', 'otilde', 
    'f', 'omacron', 
    'f', 'obreve', 
    'f', 'ohungarumlaut', 

    'f', 'idotless', 
    'f', 'i', 
    'f', 'ij',
    'f', 'iacute', 
    'f', 'igrave', 
    'f', 'idieresis', 
    'f', 'icircumflex', 
    'f', 'itilde', 
    'f', 'imacron', 
    'f', 'ibreve', 
    'f', 'iogonek', 
    
    'f', 'jdotless', 
    'f', 'j', 
    'f', 'jcircumflex', 

    'f', 'b', 
    'f', 'h', 
    'f', 'hbar', 
    'f', 'hcircumflex', 
    'f', 'hbar', 
    'f', 'k', 
    'f', 'kcommaaccent',

    'f', 'l', 
    'f', 'ldot', 'l', 
    'f', 'lslash', 
    'f', 'lacute', 
    'f', 'lcommaaccent', 
    'f', 'lcaron', 
    
    'f', 'thorn',  
    'f', 'germandbls',
    'f', 'f.small', 
    'f', 'f.ij', 
    'f', 'f.curly', 
    'f', 'f.overshoot', 
    'f', 'f.short', 
    'f', 'fi', 
    'f', 'fl', 
    
    'f', 't', 
    'f', 'tcedilla', 
    'f', 'tcaron', 
    'f', 'tcommaaccent', 
       
    'f', 'eth', 
    'f', 'tbar',  
    
    'f', 'r', 
    'f', 'rcaron',  
    
    'f', 's', 
    'f', 'scircumflex', 
    'f', 'scaron', 

    'f', 'z', 
    'f', 'zcaron', 

    'f', 'question',
    'f', 'exclam',
)

# RoboFont Assistant kerning samples

