# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   tp_kerningSamples.py
#
import os, sys
import weakref

# We use Letterrors' Similarity to find matching groups
# Install cosineSimilarity extensions via Mechanic 2
# But here we import it as separate source in assistantLib.
import assistantLib.similarity.cosineSimilarity
from assistantLib.similarity.cosineSimilarity import cosineSimilarity, SimilarGlyphsKey
from assistantLib.kerningSamples import SAMPLES, CYRILLIC_KERNING, GREEK_KERNING

# Defines types of spacing dependencies
SPACING_TYPES_LEFT = ('', 'l', 'ml', 'r2l')
SPACING_TYPES_RIGHT = ('', 'r', 'mr', 'l2r', 'w')
SPACING_KEYS = ('typeRight', 'right', 'typeLeft', 'left')

# Preselect sample script. This should become an option in KerningManager selection
#MAIN_SAMPLES = CYRILLIC_KERNING
#MAIN_SAMPLES = GREEK_KERNING
MAIN_SAMPLES = SAMPLES

class KerningManager:
    """Generic kerning manager"""

    def __init__(self, f, features=None, 
            sample=None, sampleCAPS=None, sampleC2SC=None,
            simT=0.90, simSameCategory=True, simSameScript=True, simClip=300, simZones=None,
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
        self.similar2Base1 = {}
        self.similar2Base2 = {}

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
            sample, sampleCAPS, sampleC2SC = self._initSamples() 
        self.sample = sample
        self.sampleC2SC = sampleC2SC
        self.sampleCAPS = sampleCAPS


    def _get_f(self):
        return self._f
        #return self._f()
    def _set_f(self, f):
        self._f = f
        #self._f = weakref.ref(f)
    f = property(_get_f, _set_f)

    #   G R O U P S

    def addGlyph2Group1(self, g, groupName):
        """Add glyph g to groupName. if g already exists in another "kern1" group,
        then remove it there. If that group gets empty, then remove it from g.font.groups"""
        currentGroup = self.glyphName2GroupName1.get(g.name)
        if currentGroup != groupName: # Only if there is something to change
            if currentGroup is not None: # Glyph is part of another "kern1" group, remove it there.
                # Remove the glyph from the curren group
                group = set(g.font.groups[currentGroup])
                group.remove(g.name)
                if not len(group): # Group became empty, delete it.
                    del g.font.groups[currentGroup]
                else:
                    g.font.groups[currentGroup] = sorted(group) # Otherwise save the cleaned group.
                self.glyphName2GroupName1[g.name] = currentGroup
                self.glyphName2Group1[g.name] = sorted(group)

            # Save the glyph under the new groupName
            if groupName in g.font.groups:
                dstGroup = list(g.font.groups[groupName])
            else:
                dstGroup = [] # Group does not exist, create a new one
            dstGroup.append(g.name)
            g.font.groups[groupName] = sorted(dstGroup)
            #print('==== Current group', currentGroup, group)
        
    def addGlyph2Group2(self, g, groupName):
        """Add glyph g to groupName. if g already exists in another "kern2" group,
        then remove it there. If that group gets empty, then remove it from g.font.groups"""
        currentGroup = self.glyphName2GroupName2.get(g.name)
        if currentGroup != groupName: # Only if there is something to change
            if currentGroup is not None: # Glyph is part of another "kern1" group, remove it there.
                # Remove the glyph from the curren group
                group = set(g.font.groups[currentGroup])
                group.remove(g.name)
                if not len(group): # Group became empty, delete it.
                    del g.font.groups[currentGroup]
                else:
                    g.font.groups[currentGroup] = sorted(group) # Otherwise save the cleaned group.
                self.glyphName2GroupName2[g.name] = currentGroup
                self.glyphName2Group2[g.name] = sorted(group)

            # Save the glyph under the new groupName
            if groupName in g.font.groups:
                dstGroup = list(g.font.groups[groupName])
            else:
                dstGroup = [] # Group does not exist, create a new one
            dstGroup.append(g.name)
            g.font.groups[groupName] = sorted(dstGroup)
            #print('==== Current group', currentGroup, group)
    
    #   S P A C I N G  B Y  G R O U P S

    #   Spacing by groups, answers the base glyph for the group of g (left or right side). 
    def getLeftMarginGroupBaseGlyph(self, g):
        """Answer the angled left margin source glyph, according to the base glyph of group2"""
        groupName = self.glyphName2GroupName2.get(g.name)
        if groupName is None:
            return None
        baseGlyphName = groupName.replace('public.kern2.', '')
        if baseGlyphName.endswith('_lt'):
            baseGlyphName = baseGlyphName.replace('_lt', '')
        elif baseGlyphName.endswith('_lt'):
            baseGlyphName = baseGlyphName.replace('_cy', '')
        elif baseGlyphName.endswith('_lt'):
            baseGlyphName = baseGlyphName.replace('_gr', '')
        if baseGlyphName not in self.f:
            print(f'### /{baseGlyphName} not in font.')
            return None
        return self.f[baseGlyphName]
        
    def getRightMarginGroupBaseGlyph(self, g):
        """Answer the angled right margin source glyph, according to the base glyph of group1"""
        groupName = self.glyphName2GroupName1.get(g.name)
        if groupName is None:
            return None
        baseGlyphName = groupName.replace('public.kern1.', '')
        if baseGlyphName.endswith('_lt'):
            baseGlyphName = baseGlyphName.replace('_lt', '')
        elif baseGlyphName.endswith('_lt'):
            baseGlyphName = baseGlyphName.replace('_cy', '')
        elif baseGlyphName.endswith('_lt'):
            baseGlyphName = baseGlyphName.replace('_gr', '')
        if baseGlyphName not in self.f:
            print(f'### /{baseGlyphName} not in font')
            return None
        return self.f[baseGlyphName]
        
    #   S P A C I N G  D E P E N D E N C I E S

    #   This is a different approach from similarity of groups. Sometimes margins need to be forced,
    #   even if the shapes are not similar, such as inferior --> superior. Also copying from side to side
    #   (l2r and r2l) or copy/set a fixed width cannot be defined by the standard similarity check.
    #   And groups only work inside their own script. In order to copy margins such as /A --> /A-cy
    #   this approach is more flexible. 
    #   The spacing dependencies are stored as dictionary:
    #   f['A-cy'].lib[KEY] = dict(typeLeft='l', left='A', typeRight='r', right='A')
    #   The left and/or right dependencies can be omitted. They can be altered in the editor. 
    #   Omitted dependencies make the glyph "base" for other dependencies. 

    KEY = 'com.typetr.KerningAssistant.spacingDependencies' # Dictionary for left/right dependencies and spacing types

    def getSpacingDependencyLib(self, g):
        """Answer the g.lib dictionary that defines the left/right spacing dependencies.""" 
        if self.KEY not in g.lib: # Initialize if it does not exist
            g.lib[self.KEY] = {}
        d = g.lib.get(self.KEY) # Should have format dict(typeLeft='l', left='H', typeRight='r', right='A')
        for key, value in d.items():
            if not key in SPACING_KEYS:
                del d[key]
        # Do some valication on the dictionary, otherwise the g.lib may raise an error.
        if d.get('typeLeft') not in SPACING_TYPES_LEFT: # Not a valid value, reset
            d['typeLeft'] = ''
        if d.get('typeRight') not in SPACING_TYPES_RIGHT: # Not a valid value, reset
            d['typeRight'] = ''
        #print('GET', d)
        return d

    def setSpacingDependencyLib(self, g, d):
        """Store the g.lib dictionary that defines the left/right spacing dependencies.""" 
        for key, value in d.items():
            if not key in SPACING_KEYS:
                del d[key]
        # Do some valication on the dictionary, otherwise the g.lib may raise an error.
        if d.get('typeLeft') not in SPACING_TYPES_LEFT: # Not a valid value, reset
            d['typeLeft'] = ''
        if d.get('typeRight') not in SPACING_TYPES_RIGHT: # Not a valid value, reset
            d['typeRight'] = ''
        #print('SET', d)
        g.lib[self.KEY] = d # Should have format dict(typeLeft='l', left='H', typeRight='r', right='A')

    def getLeftSpaceDependencyLabel(self, g):
        """Answer the left label as used in the EditorWindow that shows the margin dependency of the glyph.
        If the label is empty, it means that there is no dependency. The glyph is "base" for other glyphs."""
        labels = dict(l='Base Left:%s', ml='Left:%s', r2l='R-->L:%s')
        d = self.getSpacingDependencyLib(g)
        if 'typeLeft' in d and 'left' in d:
            return labels.get(d.get('typeLeft'), '%s') % d.get('left', '')
        return ''

    def getRightSpaceDependencyLabel(self, g):
        """Answer the right label as used in the EditorWindow that shows the margin dependency of the glyph.
        If the label is empty, it means that there is no dependency. The glyph is "base" for other glyphs."""
        labels = dict(r='Base Right:%s', mr='Right:%s', l2r='L-->R:%s', w='Width:%s')
        d = self.getSpacingDependencyLib(g)
        if 'typeRight' in d and 'right' in d:
            return labels.get(d.get('typeRight'), '%s') % d.get('right', '')
        return ''
    
    def getSpacingDependencyLeft(self, g):
        d = self.getSpacingDependencyLib(g)
        return d.get('typeLeft'), d.get('left')

    def getSpacingDependencyRight(self, g):
        d = self.getSpacingDependencyLib(g)
        return d.get('typeRight'), d.get('right')

    def getLeftMargin(self, g, visited=None):
        """Answer the recursive value for angled left margin dependency of this glyph.
        Note that this is the value that the glyph is supposed to have based, on its defined dependency.
        The value is not the angled left margin that is has now.""" 
        if visited is None:
            visited = [] # Remember the glyphs we referenced, in case there's a circular chain.
        lm = None # Default value, we could not determine the left margin.
        spacingType, value = self.getSpacingDependencyLeft(g)
        if isinstance(value, (int, float)):
            lm = value # It's an actual value, we're done.
        elif isinstance(value, str):
            if value in visited: # Did we already got here?
                print(f'### getSpacingDependencyLeft: Circular reference for /{g.name} with {visited}')
                return None # Error, probably a circular reference. Backout
            visited.append(g.name) # Remember that we were here.
            if spacingType == 'l': # Use the left margin of the base component (assumed to be the first component)
                if g.components: # Only if there are any components
                    component = g.components[0]
                    if component.baseGlyph in g.font:
                        baseG = g.font[component.baseGlyph]
                        blm = self.getLeftMargin(baseG, visited) # Recursively get the left margin from the base
                        if blm is not None:
                            lm = component.transformation[-2] - blm # Add it to the current position of the base component
                # Otherwise just let the method return the angled left margin of g
            elif spacingType == 'ml': # Answer the plain left margin of the referenced glyph     
                if value in g.font: # Is it a glyph reference?
                    refG = g.font[value]
                    lm = self.getLeftMargin(refG, visited)
            elif spacingType == 'r2l': # Right to left copy of reference glyph
                if value in g.font: # Is it a glyph reference?
                    refG = g.font[value]
                    lm = self.getRightMargin(refG)
        return lm

    def getRightMargin(self, g, visited=None):
        """Answer the recursive value for angled right margin dependency of this glyph.
        Note that this is the value that the glyph is supposed to have based, on its defined dependency.
        The value is not the angled left margin that is has now.""" 
        if visited is None:
            visited = [] # Remember the glyphs we referenced, in case there's a circular chain.
        rm = None # Default value, we could not determine the right margin.
        spacingType, value = self.getSpacingDependencyRight(g)
        if isinstance(value, (int, float)):
            rm = value # It's an actual value, we're done.
        elif isinstance(value, str):
            if value in visited: # Did we already got here?
                print(f'### getSpacingDependencyLeft: Circular reference for /{g.name} with {visited}')
                return None # Error, probably a circular reference. Backout
            visited.append(g.name) # Remember that we were here.
            if spacingType == 'w': # Answer the plain width of the referenced glyph     
                if value in g.font: # Is it a glyph reference?
                    refG = g.font[value]
                    # Setting the width, but we are supposed to answer the right margin.
                    # So we'll calculate the difference of widths and translate that into right margin
                    rm = g.angledRightMargin + refG.width - g.width
            elif spacingType == 'r': # Use the right margin of the base component (assumed to be the first component)
                if g.components: # Only if there are any components
                    component = g.components[0]
                    if component.baseGlyph in g.font:
                        baseG = g.font[component.baseGlyph]
                        brm = self.getRightMargin(baseG, visited) # Recursively get the left margin from the base
                        if brm is not None:
                            rm = component.transformation[-2] - brm # Add it to the current position of the base component
                # Otherwise just let the method return the angled left margin of g
            elif spacingType == 'mr': # Answer the plain left margin of the referenced glyph     
                if value in g.font: # Is it a glyph reference?
                    refG = g.font[value]
                    rm = self.getRightMargin(refG, visited)
            elif spacingType == 'l2r': # Left to right to copy of reference glyph
                if value in g.font: # Is it a glyph reference?
                    refG = g.font[value]
                    rm = self.getLeftMargin(refG)
        return rm

    #   S I M I L A R I T Y

    # Glyph names that are used as base for the seeds for the similarity checks
    # This means that all other glyphs in the set are within the tolerance range of these base glyphs.
    # These are the only ones that need to be spaced.

    BASE1 = [ # Base glyphs on left side, similar to right margin 
        'A', 'H', 'O', 'X', 'n', 'o',  # Overall base glyphs

        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        
        'period',
        
        'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

        'Iegrave-cy', 'Io-cy', 'Dje-cy', 'Gje-cy', 'E-cy', 'Dze-cy', 'I-cy', 'Yi-cy', 'Je-cy', 'Lje-cy', 'Nje-cy', 'Tshe-cy', 'Kje-cy', 'Iigrave-cy', 'Ushort-cy', 'Dzhe-cy', 
        'A-cy', 'Be-cy', 'Ve-cy', 'Ge-cy', 'De-cy', 'Ie-cy', 'Zhe-cy', 'Ze-cy', 'Ii-cy', 'Iishort-cy', 'Ka-cy', 'El-cy', 'Em-cy', 'En-cy', 'O-cy', 'Pe-cy', 'Er-cy', 'Es-cy', 
        'Te-cy', 'U-cy', 'Ef-cy', 'Ha-cy', 'Tse-cy', 'Che-cy', 'Sha-cy', 'Shcha-cy', 'Hardsign-cy', 'Yeru-cy', 'Softsign-cy', 'Ereversed-cy', 'Iu-cy', 'Ia-cy', 
        
        'a-cy', 'be-cy', 've-cy', 'ge-cy', 'de-cy', 'ie-cy', 'zhe-cy', 'ze-cy', 'ii-cy', 'iishort-cy', 'ka-cy', 'el-cy', 'em-cy', 'en-cy', 'o-cy', 'pe-cy', 'er-cy', 
        'es-cy', 'te-cy', 'u-cy', 'ef-cy', 'ha-cy', 'tse-cy', 'che-cy', 'sha-cy', 'shcha-cy', 'hardsign-cy', 'yeru-cy', 'softsign-cy', 'ereversed-cy', 'iu-cy', 
        'ia-cy', 'iegrave-cy', 'io-cy', 'dje-cy', 'gje-cy', 'e-cy', 'dze-cy', 'i-cy', 'yi-cy', 'je-cy', 'lje-cy', 'nje-cy', 'tshe-cy', 'kje-cy', 'iigrave-cy', 
        'ushort-cy', 'dzhe-cy', 'Omega-cy', 'omega-cy', 'Yat-cy', 'yat-cy', 'Eiotified-cy', 'eiotified-cy', 'Yuslittle-cy', 'yuslittle-cy', 'Yuslittleiotified-cy', 
        'yuslittleiotified-cy', 'Yusbig-cy', 'yusbig-cy', 'Yusbigiotified-cy', 'yusbigiotified-cy', 'Ksi-cy', 'ksi-cy',

        'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',    
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigmafinal', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
    ]
    BASE2 = [ # Base glyphs on right side, similar on left margin 
        'H', 'O', 'X', 'n', 'o', # Overall base glyphs

        'zero', 
        #'one', 
        'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        
        'period',

        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

        'Iegrave-cy', 'Io-cy', 'Dje-cy', 'Gje-cy', 'E-cy', 'Dze-cy', 'I-cy', 'Yi-cy', 'Je-cy', 'Lje-cy', 'Nje-cy', 'Tshe-cy', 'Kje-cy', 'Iigrave-cy', 'Ushort-cy', 'Dzhe-cy', 
        'A-cy', 'Be-cy', 'Ve-cy', 'Ge-cy', 'De-cy', 'Ie-cy', 'Zhe-cy', 'Ze-cy', 'Ii-cy', 'Iishort-cy', 'Ka-cy', 'El-cy', 'Em-cy', 'En-cy', 'O-cy', 'Pe-cy', 'Er-cy', 'Es-cy', 
        'Te-cy', 'U-cy', 'Ef-cy', 'Ha-cy', 'Tse-cy', 'Che-cy', 'Sha-cy', 'Shcha-cy', 'Hardsign-cy', 'Yeru-cy', 'Softsign-cy', 'Ereversed-cy', 'Iu-cy', 'Ia-cy', 
        
        'a-cy', 'be-cy', 've-cy', 'ge-cy', 'de-cy', 'ie-cy', 'zhe-cy', 'ze-cy', 'ii-cy', 'iishort-cy', 'ka-cy', 'el-cy', 'em-cy', 'en-cy', 'o-cy', 'pe-cy', 'er-cy', 
        'es-cy', 'te-cy', 'u-cy', 'ef-cy', 'ha-cy', 'tse-cy', 'che-cy', 'sha-cy', 'shcha-cy', 'hardsign-cy', 'yeru-cy', 'softsign-cy', 'ereversed-cy', 'iu-cy', 
        'ia-cy', 'iegrave-cy', 'io-cy', 'dje-cy', 'gje-cy', 'e-cy', 'dze-cy', 'i-cy', 'yi-cy', 'je-cy', 'lje-cy', 'nje-cy', 'tshe-cy', 'kje-cy', 'iigrave-cy', 
        'ushort-cy', 'dzhe-cy', 'Omega-cy', 'omega-cy', 'Yat-cy', 'yat-cy', 'Eiotified-cy', 'eiotified-cy', 'Yuslittle-cy', 'yuslittle-cy', 'Yuslittleiotified-cy', 
        'yuslittleiotified-cy', 'Yusbig-cy', 'yusbig-cy', 'Yusbigiotified-cy', 'yusbigiotified-cy', 'Ksi-cy', 'ksi-cy',

        'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',    
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigmafinal', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
    ]

    """Answer the sorted list of glyph names that are in self.BASE2 (similar on left side) while not similar to one 
    of the other base glyphs. Also add the glyphs that don't fit in any of the similar groups, because these should 
    have been base glyph.
    Keep track of the glyphs that we examined, since the way similarity works, glyphs can be similar to multiple base
    glyphs, while those base glyphs are not similar to each other when they fall outside the range."""

    def _findSimilarBaseNames2(self, baseName, similarBaseNames, examinedNames):
        if baseName in examinedNames:
            return
        if baseName in self.f:
            g = self.f[baseName]
            for similarName in self.getSimilarNames2(g):
                if similarName not in examinedNames:
                    if similarName in examinedNames:
                        continue
                    if baseName not in similarBaseNames:
                        similarBaseNames[baseName] = set()
                        examinedNames.add(baseName)
                    similarBaseNames[baseName].add(similarName)
                    self.similare2Base2[similarName] = baseName
        # If the baseName was not covered here, then add it as similarBaseName
        if baseName not in similarBaseNames:
            similarBaseNames[baseName] = set()
            examinedNames.add(baseName)
            self.similare2Base2[baseName] = baseName # Base of itself

    def getSimilarBaseNames2(self):
        """Answer the sorted list of glyph names that are in self.BASE2 while not similar to one of the other base glyphs.
        Also add the glyphs that don't fit in any of the similar groups, because these should have been base glyph."""
        similarBaseNames = {}
        examinedNames = set()
        for baseName in self.BASE2:
            self._findSimilarBaseNames2(baseName, similarBaseNames, examinedNames)
        # Now run again to make all glyphs into base that were not similar to one of the other glyphs
        for g in self.f:
            self._findSimilarBaseNames2(g.name, similarBaseNames, examinedNames)
        return similarBaseNames

    def _findSimilarBaseNames1(self, baseName, similarBaseNames, examinedNames):
        if baseName in examinedNames:
            return
        if baseName in self.f:
            g = self.f[baseName]
            for similarName in self.getSimilarNames1(g):
                if similarName not in examinedNames:
                    if similarName in examinedNames:
                        continue
                    if baseName not in similarBaseNames:
                        similarBaseNames[baseName] = set()
                        examinedNames.add(baseName)
                    similarBaseNames[baseName].add(similarName)
                    self.similare2Base1[similarName] = baseName
        # If the baseName was not covered here, then add it as similarBaseName
        if baseName not in similarBaseNames:
            similarBaseNames[baseName] = set()
            examinedNames.add(baseName)
            self.similare2Base1[baseName] = baseName # Base of itself

    def getSimilarBaseNames1(self):
        """Answer the sorted list of glyph names that are in self.BASE1 while not similar to one of the other base glyphs.
        Also add the glyphs that don't fit in any of the similar groups, because these should have been base glyph."""
        similarBaseNames = {}
        examinedNames = set()
        for baseName in self.BASE1:
            self._findSimilarBaseNames1(baseName, similarBaseNames, examinedNames)
        # Now run again to make all glyphs into base that were not similar to one of the other glyphs
        for g in self.f:
            self._findSimilarBaseNames1(g.name, similarBaseNames, examinedNames)
        return similarBaseNames

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

    def getSimilarNames1(self, g):
        """Answer a simple list of similar glyphs to g."""
        simNames = [g.name]
        for confidence, simGroup in self.getSimilar1(g).items():
            simNames += simGroup
        return sorted(set(simNames))

    def getSimilarGroupsNames1(self, g):
        """Answer a sorted list of group names that are similar to g."""
        simGroups = set()
        for confidence, simGroup in self.getSimilar1(g).items():
            for gName in simGroup:
                groupName = self.glyphName2GroupName1.get(gName) # If a group exists for this glyph
                if groupName is not None:
                    simGroups.add(groupName)
        return sorted(simGroups)

    def getSimilarGroups1(self, g):
        """Answer a dict for each found group with a list of tuples (glyph names, confidence %, isCurrent flag) 
        that are similar to g, including the group that glyph g is already in. 
        If there is more than one group, either g should change or groups should be merged."""
        simGroups = {} # Key is group name, value is list of tuple (group, confidence, isCurrent)
        for confidence, simGroup in self.getSimilar1(g).items():
            for gName in simGroup:
                groupName = self.glyphName2GroupName1.get(gName) # If a group exists for this glyph
                if groupName is None:
                    if self.automaticGroups: # Create missing group?
                        groupName = f'public.kern1.{gName}'
                        self.f.groups[groupName] = [gName]
                        self.glyphName2GroupName1[gName] = groupName
                        if self.verbose:
                            print(f'... Add group {groupName}')
                    else: # Otherwise for now, use a pseudo group name "(glyphName)"
                        groupName = f'({gName})'

                if groupName not in simGroups:
                    simGroups[groupName] = []
                simGroups[groupName].append((gName, confidence, bool(gName == g.name)))

        return simGroups

    def getSimilarNames2(self, g):
        """Answer a simple list of similar glyphs to g."""
        simNames = [g.name]
        for confidence, simGroup in self.getSimilar2(g).items():
            simNames += simGroup
        return sorted(set(simNames))
        
    def getSimilarGroupsNames2(self, g):
        """Answer a list of group names that are similar to g."""
        simGroups = set()
        for confidence, simGroup in self.getSimilar2(g).items():
            for gName in simGroup:
                groupName = self.glyphName2GroupName2.get(gName) # If a group exists for this glyph
                if groupName is not None:
                    simGroups.add(groupName)
        return sorted(simGroups)

    def getSimilarGroups2(self, g):
        """Answer a dict for each found group with a list of tuples (glyph names, confidence %, isCurrent flag) 
        that are similar to g, including the group that glyph g is already in. 
        If there is more than one group, either g should change or groups should be merged."""
        simGroups = {} # Key is group name, value is list of tuple (group, confidence, isCurrent)
        for confidence, simGroup in self.getSimilar2(g).items():
            for gName in simGroup:
                groupName = self.glyphName2GroupName2.get(gName) # If a group exists for this glyph
                if groupName is None:
                    if self.automaticGroups: # Create missing group?
                        groupName = f'public.kern2.{gName}'
                        self.f.groups[groupName] = [gName]
                        self.glyphName2GroupName2[gName] = groupName
                        if self.verbose:
                            print(f'... Add group {groupName}')
                    else: # Otherwise for now, use a pseudo group name "(glyphName)"
                        groupName = f'({gName})'

                if groupName not in simGroups:
                    simGroups[groupName] = []
                simGroups[groupName].append((gName, confidence, bool(gName == g.name)))

        return simGroups

    #   S A M P L E

    def _initSamples(self):
        """Answer lists of glyph names for the MAIN_SAMPLES. If a lower case glyph exists as small cap then add it to sampleCAPS.
        If a capital exists as small cap, then add it to the sampleC2SC. """
        #pre = ['Ereversedcyrillic.alt1', 'Euro.tab', 'Khacyrillic.cm1', 'Sigma.alt2', 'a.ct2', 'approxequal', 'approxequal.lc', 'approxequal.tab', 'approxequal.tab.uc', 'approxequal.uc', 'backslash.tab', 'bitcoin.tab', 'braceleft.tab', 'braceright.tab', 'bracketleft.tab', 'bracketright.tab', 'cent.tab', 'colon.tab', 'comma.tab', 'degree.tab', 'divide.tab', 'divide.tab.uc', 'dollar.tab', 'eight.tab', 'eight.tab_lc', 'eight.tab_sc', 'endash.tab', 'endash.tab.uc', 'equal', 'equal.lc', 'equal.tab', 'equal.tab.uc', 'equal.uc', 'five.tab', 'five.tab_lc', 'five.tab_sc', 'florin.tab', 'four.tab', 'four.tab_lc', 'four.tab_sc', 'greater', 'greater.lc', 'greater.tab', 'greater.tab.uc', 'greater.uc', 'greaterequal', 'greaterequal.lc', 'greaterequal.tab', 'greaterequal.tab.uc', 'greaterequal.uc', 'less', 'less.lc', 'less.tab', 'less.tab.uc', 'less.uc', 'lessequal', 'lessequal.lc', 'lessequal.tab', 'lessequal.tab.uc', 'lessequal.uc', 'minus', 'minus.lc', 'minus.tab', 'minus.tab.uc', 'minus.uc', 'minute.tab', 'multiply', 'multiply.lc', 'multiply.tab', 'multiply.tab.uc', 'multiply.uc', 'nine.tab', 'nine.tab_lc', 'nine.tab_sc', 'notequal', 'notequal.lc', 'notequal.tab', 'notequal.tab.uc', 'notequal.uc', 'numbersign.tab', 'numbersign.tab.uc', 'one.tab', 'one.tab_lc', 'one.tab_sc', 'parenleft.tab', 'parenright.tab', 'percent.tab', 'period.tab', 'perthousand.tab', 'plus', 'plus.lc', 'plus.tab', 'plus.tab.uc', 'plus.uc', 'plusminus', 'plusminus.lc', 'plusminus.tab', 'plusminus.tab.uc', 'plusminus.uc', 'second.tab', 'semicolon.tab', 'seven.tab', 'seven.tab_lc', 'seven.tab_sc', 'six.tab', 'six.tab_lc', 'six.tab_sc', 'slash.tab', 'space.tab', 'space.tab_em', 'space.tab_en', 'space.tab_thin', 'sterling.tab', 'three.tab', 'three.tab_lc', 'three.tab_sc', 'two.tab', 'two.tab_lc', 'two.tab_sc', 'yen.tab', 'zero.tab', 'zero.tab_lc', 'zero.tab_lc_salt_slash', 'zero.tab_salt_slash', 'zero.tab_sc']
        #pre = ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 
        #    'Euro.lc', 'approxequal.lc', 'bitcoin.lc', 'degree.lc', 'divide.lc', 'dollar.lc', 'eight.lc', 'equal.lc', 'five.lc', 'florin.lc', 'four.lc', 'greater.lc', 'greaterequal.lc', 'guillemotleft.lc', 'guillemotright.lc', 'guilsinglleft.lc', 'guilsinglright.lc', 'less.lc', 'lessequal.lc', 'logicalnot.lc', 'minus.lc', 'minute.lc', 'multiply.lc', 'nine.lc', 'notequal.lc', 'numbersign.lc', 'one.lc', 'ordfeminine.lc', 'ordmasculine.lc', 'paragraph.lc', 'percent.lc', 'perthousand.lc', 'plus.lc', 'plusminus.lc', 'second.lc', 'section.lc', 'seven.lc', 'six.lc', 'sterling.lc', 'three.lc', 'two.lc', 'yen.lc', 'zero.lc', 'zero.lc_salt_slash']

        #pre = ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'Euro.tab', 'approxequal.tab', 'approxequal.tab.uc', 'backslash.tab', 'bitcoin.tab', 'braceleft.tab', 'braceright.tab', 'bracketleft.tab', 'bracketright.tab', 'cent.tab', 'colon.tab', 'comma.tab', 'degree.tab', 'divide.tab', 'divide.tab.uc', 'dollar.tab', 'eight.tab', 'eight.tab_lc', 'eight.tab_sc', 'endash.tab', 'endash.tab.uc', 'equal.tab', 'equal.tab.uc', 'five.tab', 'five.tab_lc', 'five.tab_sc', 'florin.tab', 'four.tab', 'four.tab_lc', 'four.tab_sc', 'greater.tab', 'greater.tab.uc', 'greaterequal.tab', 'greaterequal.tab.uc', 'less.tab', 'less.tab.uc', 'lessequal.tab', 'lessequal.tab.uc', 'minus.tab', 'minus.tab.uc', 'minute.tab', 'multiply.tab', 'multiply.tab.uc', 'nine.tab', 'nine.tab_lc', 'nine.tab_sc', 'notequal.tab', 'notequal.tab.uc', 'numbersign.tab', 'numbersign.tab.uc', 'one.tab', 'one.tab_lc', 'one.tab_sc', 'parenleft.tab', 'parenright.tab', 'percent.tab', 'period.tab', 'perthousand.tab', 'plus.tab', 'plus.tab.uc', 'plusminus.tab', 'plusminus.tab.uc', 'second.tab', 'semicolon.tab', 'seven.tab', 'seven.tab_lc', 'seven.tab_sc', 'six.tab', 'six.tab_lc', 'six.tab_sc', 'slash.tab', 'space.tab', 'space.tab_em', 'space.tab_en', 'space.tab_thin', 'sterling.tab', 'three.tab', 'three.tab_lc', 'three.tab_sc', 'two.tab', 'two.tab_lc', 'two.tab_sc', 'yen.tab', 'zero.tab', 'zero.tab_lc', 'zero.tab_lc_salt_slash', 'zero.tab_salt_slash', 'zero.tab_sc']
        pre = ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'alpha', 'iota', 'Theta', 'Omegatonos', 'Omega', 'Etatonos', 'iotadieresis',
             'alpha.cm0', 'iota.cm0', 'alpha.ct0', 'iota.ct0', 'Theta', 
             'alpha.cm1', 'iota.cm1', 'alpha.ct1', 'iota.ct1', 'Theta', 
             'alpha.cm2', 'iota.cm2', 'alpha.ct2', 'iota.ct2', 'Theta', 
             'alpha', 'gamma', 'alpha', 'zeta', 'alpha', 'eta', 'alpha', 'kappa', 'alpha', 'mu', 'alpha', 'nu', 'alpha', 'xi', 'alpha', 'pi', 'alpha', 'tau', 
             'alpha', 'phi', 'alpha', 'chi', 'alpha', 'psi', 'alpha', 'omega', 

             'alpha.cm0', 'gamma', 'alpha.cm0', 'zeta', 'alpha.cm0', 'eta', 'alpha.cm0', 'kappa', 'alpha.cm0', 'mu', 'alpha.cm0', 'nu', 'alpha.cm0', 'xi', 'alpha.cm0', 'pi', 'alpha.cm0', 'tau', 
             'alpha.cm1', 'gamma', 'alpha.cm1', 'zeta', 'alpha.cm1', 'eta', 'alpha.cm1', 'kappa', 'alpha.cm1', 'mu', 'alpha.cm1', 'nu', 'alpha.cm1', 'xi', 'alpha.cm1', 'pi', 'alpha.cm1', 'tau', 
             'alpha.cm2', 'gamma', 'alpha.cm2', 'zeta', 'alpha.cm2', 'eta', 'alpha.cm2', 'kappa', 'alpha.cm2', 'mu', 'alpha.cm2', 'nu', 'alpha.cm2', 'xi', 'alpha.cm2', 'pi', 'alpha.cm2', 'tau', 
             'alpha.cm0', 'phi', 'alpha.cm0', 'chi', 'alpha.cm0', 'psi', 'alpha.cm0', 'omega', 
             'alpha.cm1', 'phi', 'alpha.cm1', 'chi', 'alpha.cm1', 'psi', 'alpha.cm1', 'omega', 
             'alpha.cm2', 'phi', 'alpha.cm2', 'chi', 'alpha.cm2', 'psi', 'alpha.cm2', 'omega', 
             'alpha.ct0', 'gamma', 'alpha.ct0', 'zeta', 'alpha.ct0', 'eta', 'alpha.ct0', 'kappa', 'alpha.ct0', 'mu', 'alpha.ct0', 'nu', 'alpha.ct0', 'xi', 'alpha.ct0', 'pi', 'alpha.ct0', 'tau', 
             'alpha.ct1', 'gamma', 'alpha.ct1', 'zeta', 'alpha.ct1', 'eta', 'alpha.ct1', 'kappa', 'alpha.ct1', 'mu', 'alpha.ct1', 'nu', 'alpha.ct1', 'xi', 'alpha.ct1', 'pi', 'alpha.ct1', 'tau', 
             'alpha.ct2', 'gamma', 'alpha.ct2', 'zeta', 'alpha.ct2', 'eta', 'alpha.ct2', 'kappa', 'alpha.ct2', 'mu', 'alpha.ct2', 'nu', 'alpha.ct2', 'xi', 'alpha.ct2', 'pi', 'alpha.ct2', 'tau', 
             'alpha.ct0', 'phi', 'alpha.ct0', 'chi', 'alpha.ct0', 'psi', 'alpha.ct0', 'omega', 
             'alpha.ct1', 'phi', 'alpha.ct1', 'chi', 'alpha.ct1', 'psi', 'alpha.ct1', 'omega', 
             'alpha.ct2', 'phi', 'alpha.ct2', 'chi', 'alpha.ct2', 'psi', 'alpha.ct2', 'omega', 
             'beta.cm0', 'gamma', 'beta.cm0', 'iota', 'beta.cm0', 'upsilon', 'beta.cm0', 'omega',
             'beta.cm1', 'gamma', 'beta.cm1', 'iota', 'beta.cm1', 'upsilon', 'beta.cm1', 'omega',
             'beta.cm2', 'gamma', 'beta.cm2', 'iota', 'beta.cm2', 'upsilon', 'beta.cm2', 'omega',
             'beta.ct0', 'gamma', 'beta.ct0', 'iota', 'beta.ct0', 'upsilon', 'beta.ct0', 'omega',
             'beta.ct1', 'gamma', 'beta.ct1', 'iota', 'beta.ct1', 'upsilon', 'beta.ct1', 'omega',
             'beta.ct2', 'gamma', 'beta.ct2', 'iota', 'beta.ct2', 'upsilon', 'beta.ct2', 'omega',
             'gamma.cm0', 'gamma.cm0', 'gamma.cm0', 'kappa.cm0', 'gamma.cm0', 'iota', 'gamma.cm0', 'mu', 'gamma.cm0', 'nu', 'gamma.cm0', 'omicron', 'gamma.cm0', 'upsilon', 'gamma.cm0', 'chi', 'gamma.cm0', 'omega',
             'gamma.cm1', 'gamma.cm1', 'gamma.cm1', 'kappa.cm1', 'gamma.cm1', 'iota', 'gamma.cm1', 'mu', 'gamma.cm1', 'nu', 'gamma.cm1', 'omicron', 'gamma.cm1', 'upsilon', 'gamma.cm1', 'chi', 'gamma.cm1', 'omega',
             'gamma.cm2', 'gamma.cm2', 'gamma.cm2', 'kappa.cm2', 'gamma.cm2', 'iota', 'gamma.cm2', 'mu', 'gamma.cm2', 'nu', 'gamma.cm2', 'omicron', 'gamma.cm2', 'upsilon', 'gamma.cm2', 'chi', 'gamma.cm2', 'omega',
             'gamma.ct0', 'gamma.ct0', 'gamma.ct0', 'kappa.ct0', 'gamma.ct0', 'iota', 'gamma.ct0', 'mu', 'gamma.ct0', 'nu', 'gamma.ct0', 'omicron', 'gamma.ct0', 'upsilon', 'gamma.ct0', 'chi', 'gamma.ct0', 'omega',
             'gamma.ct1', 'gamma.ct1', 'gamma.ct1', 'kappa.ct1', 'gamma.ct1', 'iota', 'gamma.ct1', 'mu', 'gamma.ct1', 'nu', 'gamma.ct1', 'omicron', 'gamma.ct1', 'upsilon', 'gamma.ct1', 'chi', 'gamma.ct1', 'omega',
             'gamma.ct2', 'gamma.ct2', 'gamma.ct2', 'kappa.ct2', 'gamma.ct2', 'iota', 'gamma.ct2', 'mu', 'gamma.ct2', 'nu', 'gamma.ct2', 'omicron', 'gamma.ct2', 'upsilon', 'gamma.ct2', 'chi', 'gamma.ct2', 'omega',
             'delta.cm0', 'alpha', 'delta.cm0', 'delta', 'delta.cm0', 'iota',
             'delta.cm1', 'alpha', 'delta.cm1', 'delta', 'delta.cm1', 'iota',
             'delta.cm2', 'alpha', 'delta.cm2', 'delta', 'delta.cm2', 'iota',
             'delta.ct0', 'alpha', 'delta.ct0', 'delta', 'delta.cm0', 'iota',
             'delta.ct1', 'alpha', 'delta.ct1', 'delta', 'delta.cm1', 'iota',
             'delta.ct2', 'alpha', 'delta.ct2', 'delta', 'delta.cm2', 'iota',
              'epsilon.cm0', 'alpha', 'epsilon.cm0', 'beta', 'epsilon.cm0', 'gamma', 'epsilon.cm0', 'eta', 'epsilon.cm0', 'kappa', 'epsilon.cm0', 'mu', 'epsilon.cm0', 'nu', 'epsilon.cm0', 'xi', 'epsilon.cm0', 'pi', 
              'epsilon.cm1', 'alpha', 'epsilon.cm1', 'beta', 'epsilon.cm1', 'gamma', 'epsilon.cm1', 'eta', 'epsilon.cm1', 'kappa', 'epsilon.cm1', 'mu', 'epsilon.cm1', 'nu', 'epsilon.cm1', 'xi', 'epsilon.cm1', 'pi', 
              'epsilon.cm2', 'alpha', 'epsilon.cm2', 'beta', 'epsilon.cm2', 'gamma', 'epsilon.cm2', 'eta', 'epsilon.cm2', 'kappa', 'epsilon.cm2', 'mu', 'epsilon.cm2', 'nu', 'epsilon.cm2', 'xi', 'epsilon.cm2', 'pi', 
              'epsilon.cm0', 'rho', 'epsilon.cm0', 'sigma', 'epsilon.cm0', 'tau', 'epsilon.cm0', 'upsilon', 'epsilon.cm0', 'chi', 'epsilon.cm0', 'omega',
              'epsilon.cm1', 'rho', 'epsilon.cm1', 'sigma', 'epsilon.cm1', 'tau', 'epsilon.cm1', 'upsilon', 'epsilon.cm1', 'chi', 'epsilon.cm1', 'omega',
              'epsilon.cm2', 'rho', 'epsilon.cm2', 'sigma', 'epsilon.cm2', 'tau', 'epsilon.cm2', 'upsilon', 'epsilon.cm2', 'chi', 'epsilon.cm2', 'omega',
              'epsilon.ct0', 'alpha', 'epsilon.ct0', 'beta', 'epsilon.ct0', 'gamma', 'epsilon.ct0', 'eta', 'epsilon.ct0', 'kappa', 'epsilon.ct0', 'mu', 'epsilon.ct0', 'nu', 'epsilon.ct0', 'xi', 'epsilon.ct0', 'pi', 
              'epsilon.ct1', 'alpha', 'epsilon.ct1', 'beta', 'epsilon.ct1', 'gamma', 'epsilon.ct1', 'eta', 'epsilon.ct1', 'kappa', 'epsilon.ct1', 'mu', 'epsilon.ct1', 'nu', 'epsilon.ct1', 'xi', 'epsilon.ct1', 'pi', 
              'epsilon.ct2', 'alpha', 'epsilon.ct2', 'beta', 'epsilon.ct2', 'gamma', 'epsilon.ct2', 'eta', 'epsilon.ct2', 'kappa', 'epsilon.ct2', 'mu', 'epsilon.ct2', 'nu', 'epsilon.ct2', 'xi', 'epsilon.ct2', 'pi', 
              'epsilon.ct0', 'rho', 'epsilon.ct0', 'sigma', 'epsilon.ct0', 'tau', 'epsilon.ct0', 'upsilon', 'epsilon.ct0', 'chi', 'epsilon.ct0', 'omega',
              'epsilon.ct1', 'rho', 'epsilon.ct1', 'sigma', 'epsilon.ct1', 'tau', 'epsilon.ct1', 'upsilon', 'epsilon.ct1', 'chi', 'epsilon.ct1', 'omega',
              'epsilon.ct2', 'rho', 'epsilon.ct2', 'sigma', 'epsilon.ct2', 'tau', 'epsilon.ct2', 'upsilon', 'epsilon.ct2', 'chi', 'epsilon.ct2', 'omega',
              'zeta.cm0', 'epsilon',
              'zeta.cm1', 'epsilon',
              'zeta.cm2', 'epsilon',
              'zeta.ct0', 'epsilon',
              'zeta.ct1', 'epsilon',
              'zeta.ct2', 'epsilon',
              'eta.cm0', 'gamma', 'eta.cm0', 'zeta', 'eta.cm0', 'nu', 'eta.cm0', 'omicron', 'eta.cm0', 'pi', 'eta.cm0', 'sigma', 'eta.cm0', 'tau', 'eta.cm0', 'upsilon', 'eta.cm0', 'chi', 'eta.cm0', 'psi', 'eta.cm0', 'omega',
              'eta.cm1', 'gamma', 'eta.cm1', 'zeta', 'eta.cm1', 'nu', 'eta.cm1', 'omicron', 'eta.cm1', 'pi', 'eta.cm1', 'sigma', 'eta.cm1', 'tau', 'eta.cm1', 'upsilon', 'eta.cm1', 'chi', 'eta.cm1', 'psi', 'eta.cm1', 'omega',
              'eta.cm2', 'gamma', 'eta.cm2', 'zeta', 'eta.cm2', 'nu', 'eta.cm2', 'omicron', 'eta.cm2', 'pi', 'eta.cm2', 'sigma', 'eta.cm2', 'tau', 'eta.cm2', 'upsilon', 'eta.cm2', 'chi', 'eta.cm2', 'psi', 'eta.cm2', 'omega',
              'eta.ct0', 'gamma', 'eta.ct0', 'zeta', 'eta.ct0', 'nu', 'eta.ct0', 'omicron', 'eta.ct0', 'pi', 'eta.ct0', 'sigma', 'eta.ct0', 'tau', 'eta.ct0', 'upsilon', 'eta.ct0', 'chi', 'eta.ct0', 'psi', 'eta.ct0', 'omega',
              'eta.ct1', 'gamma', 'eta.ct1', 'zeta', 'eta.ct1', 'nu', 'eta.ct1', 'omicron', 'eta.ct1', 'pi', 'eta.ct1', 'sigma', 'eta.ct1', 'tau', 'eta.ct1', 'upsilon', 'eta.ct1', 'chi', 'eta.ct1', 'psi', 'eta.ct1', 'omega',
              'eta.ct2', 'gamma', 'eta.ct2', 'zeta', 'eta.ct2', 'nu', 'eta.ct2', 'omicron', 'eta.ct2', 'pi', 'eta.ct2', 'sigma', 'eta.ct2', 'tau', 'eta.ct2', 'upsilon', 'eta.ct2', 'chi', 'eta.ct2', 'psi', 'eta.ct2', 'omega',
              'eta.cm0', 'lambda',
              'eta.cm1', 'lambda',
              'eta.cm2', 'lambda',
              'eta.ct0', 'lambda',
              'eta.ct1', 'lambda',
              'eta.ct2', 'lambda',
              'theta.cm0', 'alpha', 'theta.cm0', 'eta', 'theta.cm0', 'iota', 'theta.cm0', 'kappa', 'theta.cm0', 'mu', 'theta.cm0', 'nu', 'theta.cm0', 'upsilon', 'theta.cm0', 'omega',
              'theta.cm1', 'alpha', 'theta.cm1', 'eta', 'theta.cm1', 'iota', 'theta.cm1', 'kappa', 'theta.cm1', 'mu', 'theta.cm1', 'nu', 'theta.cm1', 'upsilon', 'theta.cm1', 'omega',
              'theta.cm2', 'alpha', 'theta.cm2', 'eta', 'theta.cm2', 'iota', 'theta.cm2', 'kappa', 'theta.cm2', 'mu', 'theta.cm2', 'nu', 'theta.cm2', 'upsilon', 'theta.cm2', 'omega',
              'theta.ct0', 'alpha', 'theta.ct0', 'eta', 'theta.ct0', 'iota', 'theta.ct0', 'kappa', 'theta.ct0', 'mu', 'theta.ct0', 'nu', 'theta.ct0', 'upsilon', 'theta.ct0', 'omega',
              'theta.ct1', 'alpha', 'theta.ct1', 'eta', 'theta.ct1', 'iota', 'theta.ct1', 'kappa', 'theta.ct1', 'mu', 'theta.ct1', 'nu', 'theta.ct1', 'upsilon', 'theta.ct1', 'omega',
              'theta.ct2', 'alpha', 'theta.ct2', 'eta', 'theta.ct2', 'iota', 'theta.ct2', 'kappa', 'theta.ct2', 'mu', 'theta.ct2', 'nu', 'theta.ct2', 'upsilon', 'theta.ct2', 'omega',
              'theta.cm0', 'lambda',
              'theta.cm1', 'lambda',
              'theta.cm2', 'lambda',
              'theta.ct0', 'lambda',
              'theta.ct1', 'lambda',
              'theta.ct2', 'lambda',
              'iota.cm0', 'alpha', 'iota.cm0', 'gamma', 'iota.cm0', 'delta', 'iota.cm0', 'zeta', 'iota.cm0', 'eta', 'iota.cm0', 'kappa', 'iota.cm0', 'nu', 'iota.cm0', 'omicron', 'iota.cm0', 'pi', 'iota.cm0', 'rho', 'iota.cm0', 'sigma', 'iota.cm0', 'tau', 'iota.cm0', 'upsilon', 'iota.cm0', 'chi',  'iota.cm0', 'psi', 'iota.cm0', 'omega',
              'iota.cm1', 'alpha', 'iota.cm1', 'gamma', 'iota.cm1', 'delta', 'iota.cm1', 'zeta', 'iota.cm1', 'eta', 'iota.cm1', 'kappa', 'iota.cm1', 'nu', 'iota.cm1', 'omicron', 'iota.cm1', 'pi', 'iota.cm1', 'rho', 'iota.cm1', 'sigma', 'iota.cm1', 'tau', 'iota.cm1', 'upsilon', 'iota.cm1', 'chi',  'iota.cm1', 'psi', 'iota.cm1', 'omega',
              'iota.cm2', 'alpha', 'iota.cm2', 'gamma', 'iota.cm2', 'delta', 'iota.cm2', 'zeta', 'iota.cm2', 'eta', 'iota.cm2', 'kappa', 'iota.cm2', 'nu', 'iota.cm2', 'omicron', 'iota.cm2', 'pi', 'iota.cm2', 'rho', 'iota.cm2', 'sigma', 'iota.cm2', 'tau', 'iota.cm2', 'upsilon', 'iota.cm2', 'chi',  'iota.cm2', 'psi', 'iota.cm2', 'omega',
              'iota.ct0', 'alpha', 'iota.ct0', 'gamma', 'iota.ct0', 'delta', 'iota.ct0', 'zeta', 'iota.ct0', 'eta', 'iota.ct0', 'kappa', 'iota.ct0', 'nu', 'iota.ct0', 'omicron', 'iota.ct0', 'pi', 'iota.ct0', 'rho', 'iota.ct0', 'sigma', 'iota.ct0', 'tau', 'iota.ct0', 'upsilon', 'iota.ct0', 'chi',  'iota.ct0', 'psi', 'iota.ct0', 'omega',
              'iota.ct1', 'alpha', 'iota.ct1', 'gamma', 'iota.ct1', 'delta', 'iota.ct1', 'zeta', 'iota.ct1', 'eta', 'iota.ct1', 'kappa', 'iota.ct1', 'nu', 'iota.ct1', 'omicron', 'iota.ct1', 'pi', 'iota.ct1', 'rho', 'iota.ct1', 'sigma', 'iota.ct1', 'tau', 'iota.ct1', 'upsilon', 'iota.ct1', 'chi',  'iota.ct1', 'psi', 'iota.ct1', 'omega',
              'iota.ct2', 'alpha', 'iota.ct2', 'gamma', 'iota.ct2', 'delta', 'iota.ct2', 'zeta', 'iota.ct2', 'eta', 'iota.ct2', 'kappa', 'iota.ct2', 'nu', 'iota.ct2', 'omicron', 'iota.ct2', 'pi', 'iota.ct2', 'rho', 'iota.ct2', 'sigma', 'iota.ct2', 'tau', 'iota.ct2', 'upsilon', 'iota.ct2', 'chi',  'iota.ct2', 'psi', 'iota.ct2', 'omega',
              'kappa.cm0', 'zeta', 'kappa.cm0', 'eta', 'kappa.cm0', 'kappa', 'kappa.cm0', 'mu', 'kappa.cm0', 'nu', 'kappa.cm0', 'pi', 'kappa.cm0', 'rho', 'kappa.cm0', 'tau', 'kappa.cm0', 'upsilon', 'kappa.cm0', 'chi',
              'kappa.cm1', 'zeta', 'kappa.cm1', 'eta', 'kappa.cm1', 'kappa', 'kappa.cm1', 'mu', 'kappa.cm1', 'nu', 'kappa.cm1', 'pi', 'kappa.cm1', 'rho', 'kappa.cm1', 'tau', 'kappa.cm1', 'upsilon', 'kappa.cm1', 'chi',
              'kappa.cm2', 'zeta', 'kappa.cm2', 'eta', 'kappa.cm2', 'kappa', 'kappa.cm2', 'mu', 'kappa.cm2', 'nu', 'kappa.cm2', 'pi', 'kappa.cm2', 'rho', 'kappa.cm2', 'tau', 'kappa.cm2', 'upsilon', 'kappa.cm2', 'chi',
              'kappa.ct0', 'zeta', 'kappa.ct0', 'eta', 'kappa.ct0', 'kappa', 'kappa.ct0', 'mu', 'kappa.ct0', 'nu', 'kappa.ct0', 'pi', 'kappa.ct0', 'rho', 'kappa.ct0', 'tau', 'kappa.ct0', 'upsilon', 'kappa.ct0', 'chi',
              'kappa.ct1', 'zeta', 'kappa.ct1', 'eta', 'kappa.ct1', 'kappa', 'kappa.ct1', 'mu', 'kappa.ct1', 'nu', 'kappa.ct1', 'pi', 'kappa.ct1', 'rho', 'kappa.ct1', 'tau', 'kappa.ct1', 'upsilon', 'kappa.ct1', 'chi',
              'kappa.ct2', 'zeta', 'kappa.ct2', 'eta', 'kappa.ct2', 'kappa', 'kappa.ct2', 'mu', 'kappa.ct2', 'nu', 'kappa.ct2', 'pi', 'kappa.ct2', 'rho', 'kappa.ct2', 'tau', 'kappa.ct2', 'upsilon', 'kappa.ct2', 'chi',
              'kappa.cm0', 'lambda',
              'kappa.cm1', 'lambda',
              'kappa.cm2', 'lambda',
              'kappa.ct0', 'lambda',
              'kappa.ct1', 'lambda',
              'kappa.ct2', 'lambda',
              'lambda.cm0', 'alpha', 'lambda.cm0', 'gamma', 'lambda.cm0', 'delta', 'lambda.cm0', 'zeta', 'lambda.cm0', 'omicron', 'lambda.cm0', 'pi', 'iota.cm0', 'rho', 'lambda.cm0', 'tau', 'lambda.cm0', 'upsilon', 'lambda.cm0', 'phi', 'lambda.cm0', 'chi',  'lambda.cm0', 'omega',
              'lambda.cm1', 'alpha', 'lambda.cm1', 'gamma', 'lambda.cm1', 'delta', 'lambda.cm1', 'zeta', 'lambda.cm1', 'omicron', 'lambda.cm1', 'pi', 'iota.cm1', 'rho', 'lambda.cm1', 'tau', 'lambda.cm1', 'upsilon', 'lambda.cm1', 'phi', 'lambda.cm1', 'chi',  'lambda.cm1', 'omega',
              'lambda.cm2', 'alpha', 'lambda.cm2', 'gamma', 'lambda.cm2', 'delta', 'lambda.cm2', 'zeta', 'lambda.cm2', 'omicron', 'lambda.cm2', 'pi', 'iota.cm2', 'rho', 'lambda.cm2', 'tau', 'lambda.cm2', 'upsilon', 'lambda.cm2', 'phi', 'lambda.cm2', 'chi',  'lambda.cm2', 'omega',
              'lambda.ct0', 'alpha', 'lambda.ct0', 'gamma', 'lambda.ct0', 'delta', 'lambda.ct0', 'zeta', 'lambda.ct0', 'omicron', 'lambda.ct0', 'pi', 'iota.ct0', 'rho', 'lambda.ct0', 'tau', 'lambda.ct0', 'upsilon', 'lambda.ct0', 'phi', 'lambda.ct0', 'chi',  'lambda.ct0', 'omega',
              'lambda.ct1', 'alpha', 'lambda.ct1', 'gamma', 'lambda.ct1', 'delta', 'lambda.ct1', 'zeta', 'lambda.ct1', 'omicron', 'lambda.ct1', 'pi', 'iota.ct1', 'rho', 'lambda.ct1', 'tau', 'lambda.ct1', 'upsilon', 'lambda.ct1', 'phi', 'lambda.ct1', 'chi',  'lambda.ct1', 'omega',
              'lambda.ct2', 'alpha', 'lambda.ct2', 'gamma', 'lambda.ct2', 'delta', 'lambda.ct2', 'zeta', 'lambda.ct2', 'omicron', 'lambda.ct2', 'pi', 'iota.ct2', 'rho', 'lambda.ct2', 'tau', 'lambda.ct2', 'upsilon', 'lambda.ct2', 'phi', 'lambda.ct2', 'chi',  'lambda.ct2', 'omega',
              'mu.cm0', 'alpha', 'mu.cm0', 'delta', 'mu.cm0', 'epsilon', 'mu.cm0', 'eta', 'mu.cm0', 'mu', 'mu.cm0', 'nu', 'mu.cm0', 'omicron', 'mu.cm0', 'pi', 'mu.cm0', 'rho', 'mu.cm0', 'sigma', 'mu.cm0', 'tau', 'mu.cm0', 'upsilon', 'mu.cm0', 'chi', 'mu.cm0', 'psi', 'mu.cm0', 'omega',
              'mu.cm1', 'alpha', 'mu.cm1', 'delta', 'mu.cm1', 'epsilon', 'mu.cm1', 'eta', 'mu.cm1', 'mu', 'mu.cm1', 'nu', 'mu.cm1', 'omicron', 'mu.cm1', 'pi', 'mu.cm1', 'rho', 'mu.cm1', 'sigma', 'mu.cm1', 'tau', 'mu.cm1', 'upsilon', 'mu.cm1', 'chi', 'mu.cm1', 'psi', 'mu.cm1', 'omega',
              'mu.cm2', 'alpha', 'mu.cm2', 'delta', 'mu.cm2', 'epsilon', 'mu.cm2', 'eta', 'mu.cm2', 'mu', 'mu.cm2', 'nu', 'mu.cm2', 'omicron', 'mu.cm2', 'pi', 'mu.cm2', 'rho', 'mu.cm2', 'sigma', 'mu.cm2', 'tau', 'mu.cm2', 'upsilon', 'mu.cm2', 'chi', 'mu.cm2', 'psi', 'mu.cm2', 'omega',
              'mu.ct0', 'alpha', 'mu.ct0', 'delta', 'mu.ct0', 'epsilon', 'mu.ct0', 'eta', 'mu.ct0', 'mu', 'mu.ct0', 'nu', 'mu.ct0', 'omicron', 'mu.ct0', 'pi', 'mu.ct0', 'rho', 'mu.ct0', 'sigma', 'mu.ct0', 'tau', 'mu.ct0', 'upsilon', 'mu.ct0', 'chi', 'mu.ct0', 'psi', 'mu.ct0', 'omega',
              'mu.ct1', 'alpha', 'mu.ct1', 'delta', 'mu.ct1', 'epsilon', 'mu.ct1', 'eta', 'mu.ct1', 'mu', 'mu.ct1', 'nu', 'mu.ct1', 'omicron', 'mu.ct1', 'pi', 'mu.ct1', 'rho', 'mu.ct1', 'sigma', 'mu.ct1', 'tau', 'mu.ct1', 'upsilon', 'mu.ct1', 'chi', 'mu.ct1', 'psi', 'mu.ct1', 'omega',
              'mu.ct2', 'alpha', 'mu.ct2', 'delta', 'mu.ct2', 'epsilon', 'mu.ct2', 'eta', 'mu.ct2', 'mu', 'mu.ct2', 'nu', 'mu.ct2', 'omicron', 'mu.ct2', 'pi', 'mu.ct2', 'rho', 'mu.ct2', 'sigma', 'mu.ct2', 'tau', 'mu.ct2', 'upsilon', 'mu.ct2', 'chi', 'mu.ct2', 'psi', 'mu.ct2', 'omega',
            'mu.cm0', 'lambda', 'mu.cm0', 'lambda',
            'mu.cm1', 'lambda', 'mu.cm1', 'lambda',
            'mu.cm2', 'lambda', 'mu.cm2', 'lambda',
            'nu.cm0', 'gamma', 'nu.cm0', 'eta', 'nu.cm0', 'iota', 'nu.cm0', 'kappa', 'nu.cm0', 'mu', 'nu.cm0', 'nu', 'nu.cm0', 'omicron', 'nu.cm0', 'pi', 'nu.cm0', 'rho', 'nu.cm0', 'sigma', 'nu.cm0', 'tau', 'nu.cm0', 'upsilon', 'nu.cm0', 'chi', 'nu.cm0', 'psi', 'nu.cm0', 'omega',
            'nu.cm1', 'gamma', 'nu.cm1', 'eta', 'nu.cm1', 'iota', 'nu.cm1', 'kappa', 'nu.cm1', 'mu', 'nu.cm1', 'nu', 'nu.cm1', 'omicron', 'nu.cm1', 'pi', 'nu.cm1', 'rho', 'nu.cm1', 'sigma', 'nu.cm1', 'tau', 'nu.cm1', 'upsilon', 'nu.cm1', 'chi', 'nu.cm1', 'psi', 'nu.cm1', 'omega',
            'nu.cm2', 'gamma', 'nu.cm2', 'eta', 'nu.cm2', 'iota', 'nu.cm2', 'kappa', 'nu.cm2', 'mu', 'nu.cm2', 'nu', 'nu.cm2', 'omicron', 'nu.cm2', 'pi', 'nu.cm2', 'rho', 'nu.cm2', 'sigma', 'nu.cm2', 'tau', 'nu.cm2', 'upsilon', 'nu.cm2', 'chi', 'nu.cm2', 'psi', 'nu.cm2', 'omega',

            'nu.ct0', 'gamma', 'nu.ct0', 'eta', 'nu.ct0', 'iota', 'nu.ct0', 'kappa', 'nu.ct0', 'mu', 'nu.ct0', 'nu', 'nu.ct0', 'omicron', 'nu.ct0', 'pi', 'nu.ct0', 'rho', 'nu.ct0', 'sigma', 'nu.ct0', 'tau', 'nu.ct0', 'upsilon', 'nu.ct0', 'chi', 'nu.ct0', 'psi', 'nu.ct0', 'omega',
            'nu.ct1', 'gamma', 'nu.ct1', 'eta', 'nu.ct1', 'iota', 'nu.ct1', 'kappa', 'nu.ct1', 'mu', 'nu.ct1', 'nu', 'nu.ct1', 'omicron', 'nu.ct1', 'pi', 'nu.ct1', 'rho', 'nu.ct1', 'sigma', 'nu.ct1', 'tau', 'nu.ct1', 'upsilon', 'nu.ct1', 'chi', 'nu.ct1', 'psi', 'nu.ct1', 'omega',
            'nu.ct2', 'gamma', 'nu.ct2', 'eta', 'nu.ct2', 'iota', 'nu.ct2', 'kappa', 'nu.ct2', 'mu', 'nu.ct2', 'nu', 'nu.ct2', 'omicron', 'nu.ct2', 'pi', 'nu.ct2', 'rho', 'nu.ct2', 'sigma', 'nu.ct2', 'tau', 'nu.ct2', 'upsilon', 'nu.ct2', 'chi', 'nu.ct2', 'psi', 'nu.ct2', 'omega',

            'nu.cm0', 'lambda', 'nu.ct0', 'lambda',
            'nu.cm1', 'lambda', 'nu.ct1', 'lambda',
            'nu.cm2', 'lambda', 'nu.ct2', 'lambda',

            'xi.cm0', 'alpha', 'xi.cm0', 'beta', 'xi.cm0', 'gamma', 'xi.cm0', 'epsilon', 'xi.cm0', 'zeta', 'xi.cm0', 'eta', 'xi.cm0', 'theta', 'xi.cm0', 'kappa', 'xi.cm0', 'nu', 'xi.cm0', 'pi', 'xi.cm0', 'omicron', 'xi.cm0', 'rho', 'xi.cm0', 'sigma', 'xi.cm0', 'tau', 'xi.cm0', 'chi', 'xi.cm0', 'omega',
            'xi.cm1', 'alpha', 'xi.cm1', 'beta', 'xi.cm1', 'gamma', 'xi.cm1', 'epsilon', 'xi.cm1', 'zeta', 'xi.cm1', 'eta', 'xi.cm1', 'theta', 'xi.cm1', 'kappa', 'xi.cm1', 'nu', 'xi.cm1', 'pi', 'xi.cm1', 'omicron', 'xi.cm1', 'rho', 'xi.cm1', 'sigma', 'xi.cm1', 'tau', 'xi.cm1', 'chi', 'xi.cm1', 'omega',
            'xi.cm2', 'alpha', 'xi.cm2', 'beta', 'xi.cm2', 'gamma', 'xi.cm2', 'epsilon', 'xi.cm2', 'zeta', 'xi.cm2', 'eta', 'xi.cm2', 'theta', 'xi.cm2', 'kappa', 'xi.cm2', 'nu', 'xi.cm2', 'pi', 'xi.cm2', 'omicron', 'xi.cm2', 'rho', 'xi.cm2', 'sigma', 'xi.cm2', 'tau', 'xi.cm2', 'chi', 'xi.cm2', 'omega',

            'xi.ct0', 'alpha', 'xi.ct0', 'beta', 'xi.ct0', 'gamma', 'xi.ct0', 'epsilon', 'xi.ct0', 'zeta', 'xi.ct0', 'eta', 'xi.ct0', 'theta', 'xi.ct0', 'kappa', 'xi.ct0', 'nu', 'xi.ct0', 'pi', 'xi.ct0', 'omicron', 'xi.ct0', 'rho', 'xi.ct0', 'sigma', 'xi.ct0', 'tau', 'xi.ct0', 'chi', 'xi.ct0', 'omega',
            'xi.ct1', 'alpha', 'xi.ct1', 'beta', 'xi.ct1', 'gamma', 'xi.ct1', 'epsilon', 'xi.ct1', 'zeta', 'xi.ct1', 'eta', 'xi.ct1', 'theta', 'xi.ct1', 'kappa', 'xi.ct1', 'nu', 'xi.ct1', 'pi', 'xi.ct1', 'omicron', 'xi.ct1', 'rho', 'xi.ct1', 'sigma', 'xi.ct1', 'tau', 'xi.ct1', 'chi', 'xi.ct1', 'omega',
            'xi.ct2', 'alpha', 'xi.ct2', 'beta', 'xi.ct2', 'gamma', 'xi.ct2', 'epsilon', 'xi.ct2', 'zeta', 'xi.ct2', 'eta', 'xi.ct2', 'theta', 'xi.ct2', 'kappa', 'xi.ct2', 'nu', 'xi.ct2', 'pi', 'xi.ct2', 'omicron', 'xi.ct2', 'rho', 'xi.ct2', 'sigma', 'xi.ct2', 'tau', 'xi.ct2', 'chi', 'xi.ct2', 'omega',

            'omicron.cm0', 'alpha', 'omicron.cm0', 'gamma', 'omicron.cm0', 'iota', 'omicron.cm0', 'mu', 'omicron.cm0', 'pi', 'omicron.cm0', 'rho', 'omicron.cm0', 'sigma', 'omicron.cm0', 'tau', 'omicron.cm0', 'chi', 'omicron.cm0', 'omega',
            'omicron.cm1', 'alpha', 'omicron.cm1', 'gamma', 'omicron.cm1', 'iota', 'omicron.cm1', 'mu', 'omicron.cm1', 'pi', 'omicron.cm1', 'rho', 'omicron.cm1', 'sigma', 'omicron.cm1', 'tau', 'omicron.cm1', 'chi', 'omicron.cm1', 'omega',
            'omicron.cm2', 'alpha', 'omicron.cm2', 'gamma', 'omicron.cm2', 'iota', 'omicron.cm2', 'mu', 'omicron.cm2', 'pi', 'omicron.cm2', 'rho', 'omicron.cm2', 'sigma', 'omicron.cm2', 'tau', 'omicron.cm2', 'chi', 'omicron.cm2', 'omega',

            'omicron.ct0', 'alpha', 'omicron.ct0', 'gamma', 'omicron.ct0', 'iota', 'omicron.ct0', 'mu', 'omicron.ct0', 'pi', 'omicron.ct0', 'rho', 'omicron.ct0', 'sigma', 'omicron.ct0', 'tau', 'omicron.ct0', 'chi', 'omicron.ct0', 'omega',
            'omicron.ct1', 'alpha', 'omicron.ct1', 'gamma', 'omicron.ct1', 'iota', 'omicron.ct1', 'mu', 'omicron.ct1', 'pi', 'omicron.ct1', 'rho', 'omicron.ct1', 'sigma', 'omicron.ct1', 'tau', 'omicron.ct1', 'chi', 'omicron.ct1', 'omega',
            'omicron.ct2', 'alpha', 'omicron.ct2', 'gamma', 'omicron.ct2', 'iota', 'omicron.ct2', 'mu', 'omicron.ct2', 'pi', 'omicron.ct2', 'rho', 'omicron.ct2', 'sigma', 'omicron.ct2', 'tau', 'omicron.ct2', 'chi', 'omicron.ct2', 'omega',

             'omicron.cm0', 'epsilon', 'omicron.ct0', 'epsilon', 
             'omicron.cm1', 'epsilon', 'omicron.ct1', 'epsilon', 
             'omicron.cm2', 'epsilon', 'omicron.ct2', 'epsilon', 

             'pi.cm0', 'alpha', 'pi.cm0', 'beta', 'pi.cm0', 'gamma', 'pi.cm0', 'epsilon', 'pi.cm0', 'zeta', 'pi.cm0', 'eta', 'pi.cm0', 'xi', 'pi.cm0', 'pi', 'pi.cm0', 'rho', 'pi.cm0', 'sigma', 'pi.cm0', 'tau', 'pi.cm0', 'omega',
             'pi.cm1', 'alpha', 'pi.cm1', 'beta', 'pi.cm1', 'gamma', 'pi.cm1', 'epsilon', 'pi.cm1', 'zeta', 'pi.cm1', 'eta', 'pi.cm1', 'xi', 'pi.cm1', 'pi', 'pi.cm1', 'rho', 'pi.cm1', 'sigma', 'pi.cm1', 'tau', 'pi.cm1', 'omega',
             'pi.cm2', 'alpha', 'pi.cm2', 'beta', 'pi.cm2', 'gamma', 'pi.cm2', 'epsilon', 'pi.cm2', 'zeta', 'pi.cm2', 'eta', 'pi.cm2', 'xi', 'pi.cm2', 'pi', 'pi.cm2', 'rho', 'pi.cm2', 'sigma', 'pi.cm2', 'tau', 'pi.cm2', 'omega',

             'pi.ct0', 'alpha', 'pi.ct0', 'beta', 'pi.ct0', 'gamma', 'pi.ct0', 'epsilon', 'pi.ct0', 'zeta', 'pi.ct0', 'eta', 'pi.ct0', 'xi', 'pi.ct0', 'pi', 'pi.ct0', 'rho', 'pi.ct0', 'sigma', 'pi.ct0', 'tau', 'pi.ct0', 'omega',
             'pi.ct0', 'alpha', 'pi.ct0', 'beta', 'pi.ct0', 'gamma', 'pi.ct0', 'epsilon', 'pi.ct0', 'zeta', 'pi.ct0', 'eta', 'pi.ct0', 'xi', 'pi.ct0', 'pi', 'pi.ct0', 'rho', 'pi.ct0', 'sigma', 'pi.ct0', 'tau', 'pi.ct0', 'omega',
             'pi.ct0', 'alpha', 'pi.ct0', 'beta', 'pi.ct0', 'gamma', 'pi.ct0', 'epsilon', 'pi.ct0', 'zeta', 'pi.ct0', 'eta', 'pi.ct0', 'xi', 'pi.ct0', 'pi', 'pi.ct0', 'rho', 'pi.ct0', 'sigma', 'pi.ct0', 'tau', 'pi.ct0', 'omega',

              'pi.cm0', 'lambda', 'pi.ct0', 'lambda', 
              'pi.cm1', 'lambda', 'pi.ct1', 'lambda', 
              'pi.cm2', 'lambda', 'pi.ct2', 'lambda', 

            'rho.cm0', 'alpha', 'rho.cm0', 'beta', 'rho.cm0', 'gamma', 'rho.cm0', 'epsilon', 'rho.cm0', 'zeta', 'rho.cm0', 'eta', 'rho.cm0', 'theta', 'rho.cm0', 'iota', 'rho.cm0', 'kappa', 'rho.cm0', 'mu', 'rho.cm0', 'nu', 'rho.cm0', 'xi', 'rho.cm0', 'omicron', 'rho.cm0', 'pi', 'rho.cm0', 'rho', 'rho.cm0', 'sigma', 'rho.cm0', 'tau', 'rho.cm0', 'upsilon', 'rho.cm0', 'phi', 'rho.cm0', 'chi', 'rho.cm0', 'omega',
            'rho.cm1', 'alpha', 'rho.cm1', 'beta', 'rho.cm1', 'gamma', 'rho.cm1', 'epsilon', 'rho.cm1', 'zeta', 'rho.cm1', 'eta', 'rho.cm1', 'theta', 'rho.cm1', 'iota', 'rho.cm1', 'kappa', 'rho.cm1', 'mu', 'rho.cm1', 'nu', 'rho.cm1', 'xi', 'rho.cm1', 'omicron', 'rho.cm1', 'pi', 'rho.cm1', 'rho', 'rho.cm1', 'sigma', 'rho.cm1', 'tau', 'rho.cm1', 'upsilon', 'rho.cm1', 'phi', 'rho.cm1', 'chi', 'rho.cm1', 'omega',
            'rho.cm2', 'alpha', 'rho.cm2', 'beta', 'rho.cm2', 'gamma', 'rho.cm2', 'epsilon', 'rho.cm2', 'zeta', 'rho.cm2', 'eta', 'rho.cm2', 'theta', 'rho.cm2', 'iota', 'rho.cm2', 'kappa', 'rho.cm2', 'mu', 'rho.cm2', 'nu', 'rho.cm2', 'xi', 'rho.cm2', 'omicron', 'rho.cm2', 'pi', 'rho.cm2', 'rho', 'rho.cm2', 'sigma', 'rho.cm2', 'tau', 'rho.cm2', 'upsilon', 'rho.cm2', 'phi', 'rho.cm2', 'chi', 'rho.cm2', 'omega',

            'rho.ct0', 'alpha', 'rho.ct0', 'beta', 'rho.ct0', 'gamma', 'rho.ct0', 'epsilon', 'rho.ct0', 'zeta', 'rho.ct0', 'eta', 'rho.ct0', 'theta', 'rho.ct0', 'iota', 'rho.ct0', 'kappa', 'rho.ct0', 'mu', 'rho.ct0', 'nu', 'rho.ct0', 'xi', 'rho.ct0', 'omicron', 'rho.ct0', 'pi', 'rho.ct0', 'rho', 'rho.ct0', 'sigma', 'rho.ct0', 'tau', 'rho.ct0', 'upsilon', 'rho.ct0', 'phi', 'rho.ct0', 'chi', 'rho.ct0', 'omega',
            'rho.ct1', 'alpha', 'rho.ct1', 'beta', 'rho.ct1', 'gamma', 'rho.ct1', 'epsilon', 'rho.ct1', 'zeta', 'rho.ct1', 'eta', 'rho.ct1', 'theta', 'rho.ct1', 'iota', 'rho.ct1', 'kappa', 'rho.ct1', 'mu', 'rho.ct1', 'nu', 'rho.ct1', 'xi', 'rho.ct1', 'omicron', 'rho.ct1', 'pi', 'rho.ct1', 'rho', 'rho.ct1', 'sigma', 'rho.ct1', 'tau', 'rho.ct1', 'upsilon', 'rho.ct1', 'phi', 'rho.ct1', 'chi', 'rho.ct1', 'omega',
            'rho.ct2', 'alpha', 'rho.ct2', 'beta', 'rho.ct2', 'gamma', 'rho.ct2', 'epsilon', 'rho.ct2', 'zeta', 'rho.ct2', 'eta', 'rho.ct2', 'theta', 'rho.ct2', 'iota', 'rho.ct2', 'kappa', 'rho.ct2', 'mu', 'rho.ct2', 'nu', 'rho.ct2', 'xi', 'rho.ct2', 'omicron', 'rho.ct2', 'pi', 'rho.ct2', 'rho', 'rho.ct2', 'sigma', 'rho.ct2', 'tau', 'rho.ct2', 'upsilon', 'rho.ct2', 'phi', 'rho.ct2', 'chi', 'rho.ct2', 'omega',

             'sigma.cm0', 'alpha', 'sigma.cm0', 'gamma', 'sigma.cm0', 'zeta', 'sigma.cm0', 'eta', 'sigma.cm0', 'iota', 'sigma.cm0', 'kappa', 'sigma.cm0', 'mu', 'sigma.cm0', 'nu', 'sigma.cm0', 'omicron', 'sigma.cm0', 'pi', 'sigma.cm0', 'rho', 'sigma.cm0', 'sigma', 'sigma.cm0', 'tau', 'sigma.cm0', 'upsilon', 'sigma.cm0', 'chi', 'sigma.cm0', 'omega',
             'sigma.cm1', 'alpha', 'sigma.cm1', 'gamma', 'sigma.cm1', 'zeta', 'sigma.cm1', 'eta', 'sigma.cm1', 'iota', 'sigma.cm1', 'kappa', 'sigma.cm1', 'mu', 'sigma.cm1', 'nu', 'sigma.cm1', 'omicron', 'sigma.cm1', 'pi', 'sigma.cm1', 'rho', 'sigma.cm1', 'sigma', 'sigma.cm1', 'tau', 'sigma.cm1', 'upsilon', 'sigma.cm1', 'chi', 'sigma.cm1', 'omega',
             'sigma.cm2', 'alpha', 'sigma.cm2', 'gamma', 'sigma.cm2', 'zeta', 'sigma.cm2', 'eta', 'sigma.cm2', 'iota', 'sigma.cm2', 'kappa', 'sigma.cm2', 'mu', 'sigma.cm2', 'nu', 'sigma.cm2', 'omicron', 'sigma.cm2', 'pi', 'sigma.cm2', 'rho', 'sigma.cm2', 'sigma', 'sigma.cm2', 'tau', 'sigma.cm2', 'upsilon', 'sigma.cm2', 'chi', 'sigma.cm2', 'omega',

             'sigma.ct0', 'alpha', 'sigma.ct0', 'gamma', 'sigma.ct0', 'zeta', 'sigma.ct0', 'eta', 'sigma.ct0', 'iota', 'sigma.ct0', 'kappa', 'sigma.ct0', 'mu', 'sigma.ct0', 'nu', 'sigma.ct0', 'omicron', 'sigma.ct0', 'pi', 'sigma.ct0', 'rho', 'sigma.ct0', 'sigma', 'sigma.ct0', 'tau', 'sigma.ct0', 'upsilon', 'sigma.ct0', 'chi', 'sigma.ct0', 'omega',
             'sigma.ct1', 'alpha', 'sigma.ct1', 'gamma', 'sigma.ct1', 'zeta', 'sigma.ct1', 'eta', 'sigma.ct1', 'iota', 'sigma.ct1', 'kappa', 'sigma.ct1', 'mu', 'sigma.ct1', 'nu', 'sigma.ct1', 'omicron', 'sigma.ct1', 'pi', 'sigma.ct1', 'rho', 'sigma.ct1', 'sigma', 'sigma.ct1', 'tau', 'sigma.ct1', 'upsilon', 'sigma.ct1', 'chi', 'sigma.ct1', 'omega',
             'sigma.ct2', 'alpha', 'sigma.ct2', 'gamma', 'sigma.ct2', 'zeta', 'sigma.ct2', 'eta', 'sigma.ct2', 'iota', 'sigma.ct2', 'kappa', 'sigma.ct2', 'mu', 'sigma.ct2', 'nu', 'sigma.ct2', 'omicron', 'sigma.ct2', 'pi', 'sigma.ct2', 'rho', 'sigma.ct2', 'sigma', 'sigma.ct2', 'tau', 'sigma.ct2', 'upsilon', 'sigma.ct2', 'chi', 'sigma.ct2', 'omega',

             'sigma.cm0', 'lambda', 'sigma.ct0', 'lambda', 
             'sigma.cm1', 'lambda', 'sigma.ct1', 'lambda', 
             'sigma.cm2', 'lambda', 'sigma.ct2', 'lambda', 

              'tau.cm0', 'alpha', 'tau.cm0', 'gamma', 'tau.cm0', 'delta', 'tau.cm0', 'epsilon', 'tau.cm0', 'zeta', 'tau.cm0', 'eta', 'tau.cm0', 'iota', 'tau.cm0', 'kappa', 'tau.cm0', 'mu', 'tau.cm0', 'xi', 'tau.cm0', 'omicron', 'tau.cm0', 'pi', 'tau.cm0', 'rho', 'tau.cm0', 'sigma', 'sigma.cm0', 'tau', 'sigma.cm0', 'phi', 'tau.cm0', 'chi', 'tau.cm0', 'omega',
              'tau.cm1', 'alpha', 'tau.cm1', 'gamma', 'tau.cm1', 'delta', 'tau.cm1', 'epsilon', 'tau.cm1', 'zeta', 'tau.cm1', 'eta', 'tau.cm1', 'iota', 'tau.cm1', 'kappa', 'tau.cm1', 'mu', 'tau.cm1', 'xi', 'tau.cm1', 'omicron', 'tau.cm1', 'pi', 'tau.cm1', 'rho', 'tau.cm1', 'sigma', 'sigma.cm1', 'tau', 'sigma.cm1', 'phi', 'tau.cm1', 'chi', 'tau.cm1', 'omega',
              'tau.cm2', 'alpha', 'tau.cm2', 'gamma', 'tau.cm2', 'delta', 'tau.cm2', 'epsilon', 'tau.cm2', 'zeta', 'tau.cm2', 'eta', 'tau.cm2', 'iota', 'tau.cm2', 'kappa', 'tau.cm2', 'mu', 'tau.cm2', 'xi', 'tau.cm2', 'omicron', 'tau.cm2', 'pi', 'tau.cm2', 'rho', 'tau.cm2', 'sigma', 'sigma.cm2', 'tau', 'sigma.cm2', 'phi', 'tau.cm2', 'chi', 'tau.cm2', 'omega',

              'tau.ct0', 'alpha', 'tau.ct0', 'gamma', 'tau.ct0', 'delta', 'tau.ct0', 'epsilon', 'tau.ct0', 'zeta', 'tau.ct0', 'eta', 'tau.ct0', 'iota', 'tau.ct0', 'kappa', 'tau.ct0', 'mu', 'tau.ct0', 'xi', 'tau.ct0', 'omicron', 'tau.ct0', 'pi', 'tau.ct0', 'rho', 'tau.ct0', 'sigma', 'sigma.ct0', 'tau', 'sigma.ct0', 'phi', 'tau.ct0', 'chi', 'tau.ct0', 'omega',
              'tau.ct1', 'alpha', 'tau.ct1', 'gamma', 'tau.ct1', 'delta', 'tau.ct1', 'epsilon', 'tau.ct1', 'zeta', 'tau.ct1', 'eta', 'tau.ct1', 'iota', 'tau.ct1', 'kappa', 'tau.ct1', 'mu', 'tau.ct1', 'xi', 'tau.ct1', 'omicron', 'tau.ct1', 'pi', 'tau.ct1', 'rho', 'tau.ct1', 'sigma', 'sigma.ct1', 'tau', 'sigma.ct1', 'phi', 'tau.ct1', 'chi', 'tau.ct1', 'omega',
              'tau.ct2', 'alpha', 'tau.ct2', 'gamma', 'tau.ct2', 'delta', 'tau.ct2', 'epsilon', 'tau.ct2', 'zeta', 'tau.ct2', 'eta', 'tau.ct2', 'iota', 'tau.ct2', 'kappa', 'tau.ct2', 'mu', 'tau.ct2', 'xi', 'tau.ct2', 'omicron', 'tau.ct2', 'pi', 'tau.ct2', 'rho', 'tau.ct2', 'sigma', 'sigma.ct2', 'tau', 'sigma.ct2', 'phi', 'tau.ct2', 'chi', 'tau.ct2', 'omega',

             'tau.cm0', 'lambda','tau.ct0', 'lambda', 
             'tau.cm1', 'lambda','tau.ct1', 'lambda', 
             'tau.cm2', 'lambda','tau.ct2', 'lambda', 

             'upsilon.cm0', 'alpha', 'upsilon.cm0', 'delta', 'upsilon.cm0', 'lambda', 'upsilon.cm0', 'omicron', 'upsilon.cm0', 'rho', 'upsilon.cm0', 'phi',
             'upsilon.cm1', 'alpha', 'upsilon.cm1', 'delta', 'upsilon.cm1', 'lambda', 'upsilon.cm1', 'omicron', 'upsilon.cm1', 'rho', 'upsilon.cm1', 'phi',
             'upsilon.cm2', 'alpha', 'upsilon.cm2', 'delta', 'upsilon.cm2', 'lambda', 'upsilon.cm2', 'omicron', 'upsilon.cm2', 'rho', 'upsilon.cm2', 'phi',

             'upsilon.ct0', 'alpha', 'upsilon.ct0', 'delta', 'upsilon.ct0', 'lambda', 'upsilon.ct0', 'omicron', 'upsilon.ct0', 'rho', 'upsilon.ct0', 'phi',
             'upsilon.ct1', 'alpha', 'upsilon.ct1', 'delta', 'upsilon.ct1', 'lambda', 'upsilon.ct1', 'omicron', 'upsilon.ct1', 'rho', 'upsilon.ct1', 'phi',
             'upsilon.ct2', 'alpha', 'upsilon.ct2', 'delta', 'upsilon.ct2', 'lambda', 'upsilon.ct2', 'omicron', 'upsilon.ct2', 'rho', 'upsilon.ct2', 'phi',

              'phi.cm0', 'alpha', 'phi.cm0', 'delta', 'phi.cm0', 'lambda', 'phi.cm0', 'omicron', 'phi.cm0', 'rho', 'phi.cm0', 'phi', 
              'phi.cm1', 'alpha', 'phi.cm1', 'delta', 'phi.cm1', 'lambda', 'phi.cm1', 'omicron', 'phi.cm1', 'rho', 'phi.cm1', 'phi', 
              'phi.cm2', 'alpha', 'phi.cm2', 'delta', 'phi.cm2', 'lambda', 'phi.cm2', 'omicron', 'phi.cm2', 'rho', 'phi.cm2', 'phi', 

              'phi.ct0', 'alpha', 'phi.ct0', 'delta', 'phi.ct0', 'lambda', 'phi.ct0', 'omicron', 'phi.ct0', 'rho', 'phi.ct0', 'phi', 
              'phi.ct1', 'alpha', 'phi.ct1', 'delta', 'phi.ct1', 'lambda', 'phi.ct1', 'omicron', 'phi.ct1', 'rho', 'phi.ct1', 'phi', 
              'phi.ct2', 'alpha', 'phi.ct2', 'delta', 'phi.ct2', 'lambda', 'phi.ct2', 'omicron', 'phi.ct2', 'rho', 'phi.ct2', 'phi', 

              'chi.cm0', 'theta', 'chi.ct0', 'theta', 
              'chi.cm1', 'theta', 'chi.ct1', 'theta', 
              'chi.cm2', 'theta', 'chi.ct2', 'theta', 

              'psi.cm0', 'delta', 'psi.ct0', 'delta', 
              'psi.cm1', 'delta', 'psi.ct1', 'delta', 
              'psi.cm2', 'delta', 'psi.ct2', 'delta', 

              'psi.cm0', 'epsilon', 'psi.cm0', 'lambda',
              'psi.cm1', 'epsilon', 'psi.cm1', 'lambda',
              'psi.cm2', 'epsilon', 'psi.cm2', 'lambda',

              'psi.ct0', 'epsilon', 'psi.ct0', 'lambda',
              'psi.ct1', 'epsilon', 'psi.ct1', 'lambda',
              'psi.ct2', 'epsilon', 'psi.ct2', 'lambda',

              'omega.cm0', 'delta', 'omega.cm0', 'epsilon', 'omega.cm0', 'zeta', 'omega.cm0', 'theta', 'omega.cm0', 'phi',
              'omega.cm1', 'delta', 'omega.cm1', 'epsilon', 'omega.cm1', 'zeta', 'omega.cm1', 'theta', 'omega.cm1', 'phi',
              'omega.cm2', 'delta', 'omega.cm2', 'epsilon', 'omega.cm2', 'zeta', 'omega.cm2', 'theta', 'omega.cm2', 'phi',

              'omega.ct0', 'delta', 'omega.ct0', 'epsilon', 'omega.ct0', 'zeta', 'omega.ct0', 'theta', 'omega.ct0', 'phi',
              'omega.ct1', 'delta', 'omega.ct1', 'epsilon', 'omega.ct1', 'zeta', 'omega.ct1', 'theta', 'omega.ct1', 'phi',
              'omega.ct2', 'delta', 'omega.ct2', 'epsilon', 'omega.ct2', 'zeta', 'omega.ct2', 'theta', 'omega.ct2', 'phi',

              'omega.cm0', 'lambda', 'omega.cm0', 'xi', 
              'omega.cm1', 'lambda', 'omega.cm1', 'xi', 
              'omega.cm2', 'lambda', 'omega.cm2', 'xi', 

              'omega.ct0', 'lambda', 'omega.ct0', 'xi', 
              'omega.ct1', 'lambda', 'omega.ct1', 'xi', 
              'omega.ct2', 'lambda', 'omega.ct2', 'xi', 
             ]
        sample = pre #[] # List of glyph names
        sampleCAPS = []
        sampleC2SC = []
        for c in MAIN_SAMPLES:
            gName = self.chr2glyphName.get(c)
            if gName is not None:
                sample.append(gName)

                # Lowercase to small caps, keep the capitals
                capsExceptions = dict(oe='OE.sc', ae='AE.sc', aeacute='AEacute.sc', ij='IJ.sc', germandbls='germandbls.sc') # Cannot be solved by simple name conversion
                capsName = gName[0].upper() + gName[1:] + '.sc'
                if gName in capsExceptions: # /oe --> /OE.sc
                    sampleCAPS.append(capsExceptions[gName])
                elif gName[0].upper() == gName[0]: # /Agrave --> /Agrave
                    sampleCAPS.append(gName)
                elif gName[0].upper() != gName[0] and capsName in self.f: # /agrave --> /Agrave.sc
                    sampleCAPS.append(capsName)
                else: # /period --> /period
                    sampleCAPS.append(gName) 

                # Capitals to smallcaps, then also lowercase to small caps
                capsExceptions = dict(OE='OE.sc', AE='AE.sc', AEacute='AEacute.sc', IJ='IJ.sc', Germandbls='germandbls.sc') # Cannot be solved by simple name conversion
                if gName[0].upper() == gName[0] and gName + '.sc' in self.f: # It's a capital, does the small caps exist?
                    sampleC2SC.append(gName + '.sc')
                else:
                    capsName = gName[0].upper() + gName[1:] + '.sc'
                    if gName in capsExceptions:
                        sampleC2SC.append(capsExceptions[gName])
                    elif capsName in self.f:
                        sampleC2SC.append(capsName)
                    elif gName + '.sc' in self.f:
                        sampleC2SC.append(gName + '.sc')
                    else:
                        sampleC2SC.append(gName)

        return sample, sampleCAPS, sampleC2SC

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
