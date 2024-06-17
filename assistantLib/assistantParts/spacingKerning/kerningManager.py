# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   kerningManager.py
#
import os, sys
import weakref
import urllib

import drawBot as db # Used to generate KernNet sample kerning image test.png

# We use Letterrors' Similarity to find matching groups
# Install cosineSimilarity extensions via Mechanic 2
# But here we import it as separate source in assistantLib.
import assistantLib.similarity.cosineSimilarity
from assistantLib.similarity.cosineSimilarity import cosineSimilarity, SimilarGlyphsKey

from assistantLib.kerningSamples import SAMPLES, CYRILLIC_KERNING, GREEK_KERNING
# Seed relation between glyphs as start for similarity groups
from assistantLib.assistantParts.glyphsets.groupBaseGlyphs import *

# Defines types of spacing dependencies
SPACING_TYPES_LEFT = ('', 'l', 'ml', 'r2l')
SPACING_TYPES_RIGHT = ('', 'r', 'mr', 'l2r', 'w')
SPACING_KEYS = ('typeRight', 'right', 'typeLeft', 'left')

# Preselect sample script. This should become an option in KerningManager selection
#MAIN_SAMPLES = CYRILLIC_KERNING
#MAIN_SAMPLES = GREEK_KERNING
MAIN_SAMPLES = SAMPLES

TAB_WIDTH = 650 # Default tab width, change for em != 1000

class Q2B:
    """In order to do glyph.removeOverlap outside RoboFont, we can only have Bezier points.
    KerningManager.kernedDistance is using a method where remove overlap is necessary.
    The class may be brought outside this source. 
    """
    # Point types
    POINTTYPE_BEZIER = 'curve'
    POINTTYPE_QUADRATIC = 'qcurve'
    POINTTYPE_OFFCURVE = 'offcurve'

    FACTOR = 1.340   # This estimated value gives amazingly accurate conversion.

    def curvesQ2B(self, g):
        self.curvesConvert(g, self.POINTTYPE_QUADRATIC, self.POINTTYPE_BEZIER, self.FACTOR)

    def factorizeOffCurve(self, onCurve, offCurve, factor):
        dx = offCurve.x - onCurve.x
        dy = offCurve.y - onCurve.y
        offCurve.x = int(round(onCurve.x + dx * factor))
        offCurve.y = int(round(onCurve.y + dy * factor))

    def curvesConvert(self, g, fromType, toType, factor):
        # Make sure to unselect all points
        for contour in g.contours:
            points = contour.points
            for n in range(len(points)):
                p_0, p_1, p_2, p_3 = points[n], points[n-1], points[n-2], points[n-3]
                if p_0.type == fromType:
                    p_0.type = toType
                    if p_1.type == self.POINTTYPE_OFFCURVE:
                        self.factorizeOffCurve(p_0, p_1, factor)
                    if p_2.type == self.POINTTYPE_OFFCURVE:
                        self.factorizeOffCurve(p_3, p_2, factor)

q2b = Q2B()

class GroupKerningStatistics:
    def __init__(self, f):
        self.path = f.path
        self.totalGroups = len(f.groups)
        self.totalKerning = len(f.kerning)
        self.groupGroupKerning = 0
        self.groupGlyphKerning = 0
        self.glyphGroupKerning = 0
        self.glyphGlyphKerning = 0

        # Kerning statistics
        self.missingKernedGroups1 = set()
        self.missingKernedGlyph1 = set()
        self.missingKernedGroups2 = set()
        self.missingKernedGlyph2 = set()

        self.negativeKerning = 0
        self.zeroKerning = 0
        self.positiveKerning = 0

        # Group statistics
        self.missingGroupName1 = {}
        self.missingGroupName2 = {}
        self.badGroupNames = set()

        # Test if all kerning is either a valid group name or an existing glyph
        for (name1, name2), k in f.kerning.items():

            if name1 in f.groups and name2 in f.groups:
                self.groupGroupKerning += 1
            elif name1 in f.groups and name2 in f.keys():
                self.groupGlyphKerning += 1
            elif name1 in f.keys() and name2 in f.groups:
                self.glyphGroupKerning += 1
            elif name1 in f.keys() and name2 in f.keys():
                self.glyphGlyphKerning += 1

            if name1.startswith(PUBLIC_KERN1) and name1 not in self.f.groups:
                self.missingKernedGroups1.add((name1, name2))
            elif name1 not in f.keys():
                self.missingKernedGlyph1.add(name1)
            
            if name2.startswith(PUBLIC_KERN2) and name2 not in self.f.groups:
                self.missingKernedGroups2.add((name1, name2))
            elif name2 not in f.keys():
                self.missingKernedGlyph2.add(name1)

            if k < 0:
                self.negativeKerning += 1
            elif k > 0:
                self.positiveKerning += 1
            else:
                self.zeroKerning += 1

        hasGroup1 = set()
        hasGroup2 = set()

        for groupName, group in f.groups.items():
            for gName in group:

                if groupName.startswith(PUBLIC_KERN1):
                    if gName not in self.f.keys():
                        if gName not in self.missingGroupName1:
                            self.missingGroupName1[gName] = []
                        self.missingGroupName1.append(gName)

                    if gName in hasGroup1:
                        if gName not in self.multipleGroups1:
                            self.multipleGroups1[gName] = []
                        self.multipleGroups1[gName].append(groupName)

                    hasGroup1.add(gName)

                elif groupName.startswith(PUBLIC_KERN2):
                    if gName not in self.f.keys():
                        if gName not in self.missingGroupName2:
                            self.missingGroupName2[gName] = []
                        self.missingGroupName2.append(gName)

                    if gName in hasGroup2:
                        if gName not in self.multipleGroups2:
                            self.multipleGroups2[gName] = []
                        self.multipleGroups2[gName].append(groupName)
            
                    hasGroup1.add(gName)

                else:
                    self.badGroupNames.add(groupName)
    
    def __repr__(self):
        return f"""
--- Group-Kerning statistics of {f.path.split('/')[-1]}
    • Groups: {self.totalGroups}
    • Kerning: {self.totalKerning}
    • Group-Group kerning: {self.groupGroupKerning}

    • Missing kerned groups1: {len(self.missingKernedGroups1)} {self.missingKernedGroups1}
    • Missing kerned glyphs1: {len(self.missingKernedGlyph1)} {self.missingKernedGlyph1}
    • Missing kerned groups2: {len(self.missingKernedGroups2)} {self.missingKernedGroups2}
    • Missing kerned glyphs2: {len(self.missingKernedGlyph2)} {self.missingKernedGlyph2}

    • Negative kerning: {self.negativeKerning}
    • Zero kerning: {self.zeroKerning}
    • Positive kerning: {self.positiveKerning}

    
    """


class KerningManager:
    """Generic kerning manager, the spacing WizzKid. It knows all about groups, spacing and kerning and it offers several strategies for it:
    by groups, by specification in the GlyphData, by Similarity and by KernNet-AI. It is up to the calling assistant to decide
    which strategy fits best to a certain design and to a certain phase in the design process.

    The KerningManager also is able to supply sample lists of glyphnames, that fit best to the current task (spacing or kerning)
    for a specific glyph.

    """

    def __init__(self, f, md, features=None, 
            #sample=None, sampleCAPS=None, sampleC2SC=None, # List of (kerning) glyph names
            simT=0.90, simSameUnicodeClass=True, simSameUnicodeRange=False, simSameUnicodeScript=True, simClip=300, simZones=None,
            automaticGroups=True, verbose=True,
            tabWidth=TAB_WIDTH, fixedLeftMarginPatterns=None, fixedRightMarginPatterns=None, fixedWidthPatterns=None,
            groupBaseGlyphs=None,
            ):
        """Calculate all values, patterns and similarity caching to guess margins for individual glyphs.
        For reasons of validity, the font itself is not stored in the spacer instance.
        The spacer can be initialize with a font later."""
        
        assert f is not None
        self.f = f # Stored as weakref property
        assert md is not None
        self.md = md # Contains the self.md.gs glyphset, useful for the KerningManager to have.
        if features is None:
            features = {}
        self.features = features # Dictionary of open type features to show in the samples

        self.verbose = verbose

        # Similarity parameters
        self.simT = simT # the confidence threshold. Only show results > simT
        self.simSameUnicodeClass = simSameUnicodeClass # only show glyphs in the same unicode category
        self.simSameUnicodeRange = simSameUnicodeRange
        self.simSameUnicodeScript = simSameUnicodeScript # only show glyphs in the same unicode script
        self.simClip = simClip # clip is how deep the profile should be, measured from the margin inward.
        # zones are pairs of y values of the areas we specifically want to compare.
        # useful if you want to exclude certain bands.
        # this is an example, your values might be different:
        #
        #if simZones is None:
        #    simZones = []
        #    simZones.append((f.info.xHeight, f.info.unitsPerEm+f.info.descender))
        #    simZones.append((0, f.info.xHeight))
        #    simZones.append((f.info.descender, 0))
        #    simZones = tuple(simZones)    # make sure the zones are a tuple
        # or 
        #    simZones = None            # or make zones None to scane the full height
        if simZones is None:
            simZones = []
            simZones.append((0, f.info.capHeight))
            simZones = tuple(simZones)
        self.simZones = simZones
        self.similar2Base1 = {}
        self.similar2Base2 = {}

        # X-ref unicode and names. Initialize attributes upon usage.
        self._uni2glyphName = None
        self._chr2glyphName = None

        self.automaticGroups = automaticGroups # Generated new groups for glyphs that don't belong.

        # Do some caching on groups. Initialize attributes upon usage
        self._glyphName2GroupName1 = None
        self._glyphName2Group1 = None
        self._glyphName2GroupName2 = None
        self._glyphName2Group2 = None

        # Dictionary with base glyphs for group1 and group2 per script
        # Required format: dict(
        #   lt1=(glyphName, ...), 
        #   lt2=(glyphName, ...), 
        #   cy1=(glyphName, ...), 
        #   cy2=(glyphName, ...), 
        #   gr1=(glyphName, ...), 
        #   gr2=(glyphName, ...)
        #   all1=(glyphName, ...), # Glyphs that kern with all scripts and with each other.
        #   all2=(glyphName, ...)
        # )
        if groupBaseGlyphs is None:
            groupBaseGlyphs = GROUP_BASE_GLYPHS # Use default
        self.groupBaseGlyphs = groupBaseGlyphs

        # Deprecated, now we have as dictionary of samples, initialized upon property request.
        #if not sample: # Not defined, then construct default
        #    sample = []
        #    for ch in SAMPLES:
        #        uni = ord(ch)
        #        gName = md.glyphSet.unicode2GlyphName.get(uni)
        #        if gName is not None:
        #            sample.append(gName)

        # Sample indices, remember different ones for different types of samples
        self._sampleGlyphSetIndex = 0
        self._sampleSimilarityIndex = 0
        self._sampleGroupIndex = 0
        self._sampleSpacingIndex = 0

        # Cashed sample for kerning. If None, it will be initialize upon usage.
        self._kerningSample = None
        self._sampleKerningIndex = 0 # Current index in the sample to show

        # Kerning filters
        self._kerningSampleFilter1 = None # Select sample kerning pairs in sample if None or if pattern is in the group base glyph name
        self._kerningSampleFilterValue = None # Select sample kerning pairs if value is None or within a range
        self._kerningSampleFilter2 = None # Select sample kerning pairs in sample if none or if pattern is in the group base glyph name

        self.tabWidth = tabWidth

        # @@@ Generic fixed spacing patterns. These are glyphset dependent, so their should go into the GlyphSet class. 

        # Does not seem to be in use anymore
        #if fixedLeftMarginPatterns is None:
        #    fixedLeftMarginPatterns = { # Key is right margin, value is list of glyph names
        #    186:  ('enclosingkeycapcomb',) # Margin of /H
        #}
        #self.fixedLeftMarginPatterns = fixedLeftMarginPatterns # Key is margin, value is list of glyph names
        #
        #if fixedRightMarginPatterns is None:
        #    fixedRightMarginPatterns = { # Key is right margin, value is list of glyph names
        #    186:  ('enclosingkeycapcomb',) # Margin of /H
        #}
        #self.fixedRightMarginPatterns = fixedRightMarginPatterns # Key is margin, value is list of glyph names

        if fixedWidthPatterns is None:
            # @@@ TODO: these are specific for Segoe, make these into tables of GlyphSet
            fixedWidthPatterns = { # Key is right margin, value is list of glyph names. Adding | vertical bar means that the patterns is at the end of the name.
            0: ('cmb|', 'comb|', 'comb-cy|', '-uc|', 'mod|', '.component', 'zerowidthspace', 'zerowidthjoiner', 
                'zerowidthnonjoiner', 'righttoleftmark', 'Otilde.component1', 'middledoublegraveaccentmod', 
                'perispomeni', 'cedillacomb.component', 'psili', 'dblgravecomb', 
                'dasiavaria-uc', 'ringhalfright', ), # "|" matches pattern on end of name"
            self.tabWidth: ('.tab|', '.tnum|')
        }
        self.fixedWidthPatterns = fixedWidthPatterns # Key is margin, value is list of glyph names

    def _get_f(self):
        return self._f
        #return self._f()
    def _set_f(self, f):
        self._f = f
        #self._f = weakref.ref(f)
    f = property(_get_f, _set_f)

    #   I N I T I A L I Z E  O N  U S A G E

    # Initialize time-consuming attributes upon usage
    def _initialize2glyphName(self):
        self._uni2glyphName = {}
        self._chr2glyphName = {}
        for g in self.f:
            if g.unicode:
                self._uni2glyphName[g.unicode] = g.name
                self._chr2glyphName[chr(g.unicode)] = g.name
    def _get_uni2glyphName(self):
        if self._uni2glyphName is None:
            self._initialize2glyphName() 
            return self.uni2glyphName 
    uni2glyphName = property(_get_uni2glyphName)      
    
    def _get_chr2glyphName(self):
        if self._chr2glyphName is None:
            self._initialize2glyphName() 
            return self._chr2glyphName 
    chr2glyphName = property(_get_chr2glyphName)      

    #   G R O U P  &  K E R N I N G  S T A T I S T I C S

    def getGroupKerningStatistics(self):
        """Answer statistics on groups and kerning for QA usage:
        - Is there any kerning that refers to non-existing groups
        - Is there any kerning that refers to non-existing glyphs
        - Amount of kerning pairs for each type (group-group, group-glyph, glyph-group, glyph-glyph)
        - Groups that have no kerning reference.
        - Glyph that have no kerning reference.
        """
        return GroupKerningStatistics(f)

    #   G R O U P S

    def _initializeGlyph2Group(self):
        """Initialize the glyph-->group dictionaries for the current font. As references only, no group storage."""
        self._glyphName2GroupName1 = {}
        self._glyphName2Group1 = {}
        self._glyphName2GroupName2 = {}
        self._glyphName2Group2 = {}

        for groupName, group in self.f.groups.items():
            if 'kern1' in groupName:
                for glyphName in group:
                    self._glyphName2GroupName1[glyphName] = groupName
                    self._glyphName2Group1[glyphName] = group
            elif 'kern2' in groupName:
                for glyphName in group:
                    self._glyphName2GroupName2[glyphName] = groupName
                    self._glyphName2Group2[glyphName] = group

    def _get_glyphName2GroupName1(self):
        if self._glyphName2GroupName1 is None:
            self._initializeGlyph2Group()
        return self._glyphName2GroupName1
    glyphName2GroupName1 = property(_get_glyphName2GroupName1)
    
    def _get_glyphName2Group1(self):
        if self._glyphName2Group1 is None:
            self._initializeGlyph2Group()
        return self._glyphName2Group1
    glyphName2Group1 = property(_get_glyphName2Group1)
    
    def _get_glyphName2GroupName2(self):
        if self._glyphName2GroupName2 is None:
            self._initializeGlyph2Group()
        return self._glyphName2GroupName2
    glyphName2GroupName2 = property(_get_glyphName2GroupName2)
    
    def _get_glyphName2Group2(self):
        if self._glyphName2Group2 is None:
            self._initializeGlyph2Group()
        return self._glyphName2Group2
    glyphName2Group2 = property(_get_glyphName2Group2)

    def getBaseGroupGlyphName1(self, g):
        """Answer the name of the base group glyph that g shares group 1 with.
        Getting the base group glyph name is sort of a hack: stripping the group name."""
        groupName1 = self.glyphName2GroupName1.get(g.name)
        if groupName1 is not None:
            gName = groupName1.replace(PUBLIC_KERN1, '') # Strip the PUBLIC_KERN1
            parts = gName.split('_')
            if parts[-1] in ('lt', 'cy', 'gr'): # Script extension, remove it
                gName = '_'.join(parts[:-1])
            return gName
        return None

    def getBaseGroupGlyphName2(self, g):
        """Answer the name of the base group glyph that g shares group 2 with.
        Getting the base group glyph name is sort of a hack: stripping the group name."""
        groupName2 = self.glyphName2GroupName2.get(g.name)
        if groupName2 is not None:
            gName = groupName1.replace(PUBLIC_KERN2, '') # Strip the PUBLIC_KERN2
            parts = gName.split('_')
            if parts[-1] in ('lt', 'cy', 'gr'): # Script extension, remove it
                gName = '_'.join(parts[:-1])
            return gName
        return None

    # Some methods to handle groups. Best not to do this directly on f.groups, so we can check consistency
    # e.g. removing the glyphs in the new group from other groups. And updating the glyphName2GroupName tables, etc.

    def _groupIgnore1(self, gName):
        for namePart in GROUP_IGNORE:
            if namePart in gName:
                return True
        return False

    def _groupIgnore2(self, gName):
        for namePart in GROUP_IGNORE:
            if namePart in gName:
                return True
        return False

    def initializeGroups(self, fixKerning=False):
        """This (dangerous) method does clear the self.f.groups and builds them according to what is in self.groupBaseGlyphs.
        If the fixKerning flag is set, then clean the kerning, removing all pairs with group names that no longer exist.
        Note that there may be base group glyphs that are so similar that they still should not have separate groups.
        """
        self.f.groups.clear() # Clear the current set of groups in this font
        # Then make groups for each of the glyphs in self.groupBaseGlyphs
        assert self.groupBaseGlyphs is not None # Make sure it is defined, if using this group inization process
        used1 = set() # Check that glyphs don't get in groups on their side more than once.
        used2 = set()
        noGroup1 = set()
        noGroup2 = set()
        baseGlyph2GroupName1 = {} # Key is base group glyph name, value is the groupName
        baseGlyph2GroupName2 = {} # Key is base group glyph name, value is the groupName
        # First make small groups for every base group glyph
        for scriptName, baseGlyphNames in self.groupBaseGlyphs.items(): # Script by script
            s1, s2 = GROUP_NAME_PARTS[scriptName] # Construct the group name for this script and this base group glyph name.
            for baseGlyphName in baseGlyphNames: # For each of the base group glyph names of this script.
                groupName = s1 + baseGlyphName + s2
                baseGroup = [baseGlyphName]

                if scriptName in BASE_SCRIPTS1:
                    used1.add(baseGlyphName)
                    baseGlyph2GroupName1[baseGlyphName] = groupName

                elif scriptName in BASE_SCRIPTS2:
                    used2.add(baseGlyphName)
                    baseGlyph2GroupName2[baseGlyphName] = groupName

                self.f.groups[groupName] = baseGroup # Initialize with just the base glyph in the group.                    
                print(f'... Initialize group "{s1 + baseGlyphName + s2}" to {str(baseGroup)}')

        # Then go through all glyphs, to see if they fit one of the created base glyph groups

        for g in self.f:
            if g.name not in used1 and not self._groupIgnore1(g.name):
                if g.name in FORCE_GROUP1:
                    simGroup1 = [FORCE_GROUP1[g.name]]
                    print(f'... Force {g.name} in group 1 {simGroup1}')
                else:
                    simGroup1 = sorted(self.getSimilarNames1(g))
                #print('==== 1 ==', 'O' in simGroup1, g.name, simGroup1)
                for simGlyphName1 in simGroup1:
                    # If a similar glyph to g exists in baseGlyph2GroupName1 then add it to that group
                    if simGlyphName1 in baseGlyph2GroupName1:
                        groupName1 = baseGlyph2GroupName1[simGlyphName1]
                        group1 = list(self.f.groups[groupName1])
                        group1.append(g.name)
                        self.f.groups[groupName1] = sorted(group1)
                        #print(f'... Add /{g.name} to group {str(groupName1)}')
                        used1.add(g.name)
                        break

                if not g.name in used1:
                    noGroup1.add(g.name)

            if g.name not in used2 and not self._groupIgnore2(g.name):            
                if g.name in FORCE_GROUP2:
                    simGroup2 = [FORCE_GROUP2[g.name]]
                    print(f'... Force {g.name} in group 2 {simGroup2}')
                else:
                    simGroup2 = sorted(self.getSimilarNames2(g))
                #print('==== 2 ==', 'O' in simGroup2, g.name, simGroup2)
                for simGlyphName2 in simGroup2:
                    # If a similar glyph to g exists in baseGlyph2GroupName2 then add it to that group
                    if simGlyphName2 in baseGlyph2GroupName2 or g.name in FORCE_GROUP2.get(simGlyphName2, []):
                        groupName2 = baseGlyph2GroupName2[simGlyphName2]
                        group2 = list(self.f.groups[groupName2])
                        group2.append(g.name)
                        self.f.groups[groupName2] = sorted(group2)
                        #print(f'... Add /{g.name} to group {str(groupName2)}')
                        used2.add(g.name)
                        break
                    
                if not g.name in used2:
                    noGroup2.add(g.name)

        if noGroup1:
            # If we get here, no base group was found for g
            print(f'... No groups1 ', noGroup1)

        if noGroup2:
            # If we get here, no base group was found for g
            print(f'... No groups2 ', noGroup2)

        self._initializeGlyph2Group()

        #for groupName, group in sorted(self.f.groups.items()):
        #    print(groupName, group)

        #print(f'{self.md.name} Groups: {len(self.f.groups)}')

        self.f.changed()

    def addGlyph2Group1(self, g, groupName):
        """Add glyph g to groupName. if g already exists in another "kern1" group,
        then remove it there. If that group gets empty, then remove it from g.font.groups"""
        assert groupName.startswith(PUBLIC_KERN1) # Check on right group naming
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
        assert groupName.startswith(PUBLIC_KERN2) # Check on right group naming
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

    def setGroup1(self, f, groupName, group):
        """Set f.groups[groupName] to group. We best can do this by this method instead of setting directly,
        so it can be checked if the glyphs in the group should first be removed from other "1" groups."""
        changed = False
        for gName in group:
            if gName in f:
                self.addGlyph2Group1(f[gName], groupName)
                changed = True
        # For now, force initialization
        self._initializeGlyph2Group()
        return changed

    def setGroup2(self, f, groupName, group):
        """Set f.groups[groupName] to group. We best can do this by this method instead of setting directly,
        so it can be checked if the glyphs in the group should first be removed from other "2" groups."""
        changed = False
        for gName in group:
            if gName in f:
                self.addGlyph2Group2(f[gName], groupName)
                changed = True
        # For now, force initialization
        self._initializeGlyph2Group()
        return changed
    
    #   S P A C I N G  B Y  G R O U P S

    #   Spacing by groups, answers the base glyph for the group of g (left or right side). 
    def getLeftMarginGroupBaseGlyph(self, g):
        """Answer the angled left margin source glyph, according to the base glyph of group2"""
        groupName = self.glyphName2GroupName2.get(g.name)
        if groupName is None:
            return None
        baseGlyphName = groupName.replace(PUBLIC_KERN2, '')
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
        baseGlyphName = groupName.replace(PUBLIC_KERN1, '')
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
        
    #   S P A C I N G  D E P E N D E N C I E S  B Y  G L Y P H  D A T A 

    #   This approach searched in glyph data if there are any references to source glyph for left an right margin

    def hasEqualLeftMargin(self, g, lm):
        """Answer the boolean flag if the left margin is different from the current g value,"""
        alm = g.angledLeftMargin
        if None in (alm, lm):
            return True # Undefined margins, as in /space, are not difference, by defintion.
        return abs(alm - lm) <= 1

    def hasEqualLeftBaseMargin(self, g, lm):
        """Answer the boolean flag if the left margin is different from the current g value,"""
        blm = self.getLeftMarginByGlyphSetReference(g)
        if None in (blm, lm):
            return True # Undefined margins, as in /space, are not difference, by defintion.
        return abs(blm - lm) <= 1

    def hasEqualRightMargin(self, g, rm):
        """Answer the boolean flag if the right margin is different from the current g value,"""
        arm = g.angledRightMargin
        if None in (arm, rm):
            return True # Undefined margins, as in /space, are not difference, by defintion.
        return abs(arm - rm) <= 1

    def hasEqualRightBaseMargin(self, g, rm):
        """Answer the boolean flag if the right margin is different from the current g value,"""
        arm = g.angledRightMargin
        if None in (arm, rm):
            return True # Undefined margins, as in /space, are not difference, by defintion.
        return abs(arm - rm) <= 1

    def hasLeftMarginReference(self, g):
        """Answer the boolean flag if the has a reference rule for the left margin."""
        gd = self.md.glyphSet.glyphs[g.name]
        return gd is not None and gd.leftSpaceSourceLabel is not None

    def hasRightMarginReference(self, g):
        """Answer the boolean flag if the has a reference rule for the right margin."""
        gd = self.md.glyphSet.glyphs[g.name]
        return gd is not None and gd.rightSpaceSourceLabel is not None

    def fixGlyphWidth(self, g, width, label=''):
        """Compare the rounded width to g.width. If it is different, then set the width."""
        width = int(round(width))
        if g.width != width:
            print(f'... Fix glyph width: Set /{g.name} width from {g.width} to {width} {label}')
            g.width = width
            return True
        return False

    def fixLeftMargin(self, g, lm, label=''):
        """If the left margin is different from the current g value, then change it. Label is optional information about why it changed."""
        if not self.hasEqualLeftMargin(g, lm):
            print(f'... Fix left margin: Set /{g.name} from {g.angledLeftMargin} to {lm} {label}')
            g.angledLeftMargin = lm
            return True
        return False

    def fixRightMargin(self, g, rm, label=''):
        """If the right margin is different from the current g value, then change it. Label is optional information about why is changed."""
        if not self.hasEqualRightMargin(g, rm):
            print(f'... Fix right margin: Set /{g.name} from {g.angledRightMargin} to {rm} {label}')
            g.angledRightMargin = rm
            return True
        return False

    def fixCenteredMargins(self, g, lable=''):
        """If the glyph is not centered on its current width then move it horizontally."""
        w = g.width
        lm = (g.angledLeftMargin + g.angledRightMargin)/2
        if not self.hasEqualLeftMargin(g, lm):
            g.angledLeftMargin = lm
            g.width = w # Restore the width to original.
            return True
        return False

    def fixLeftMarginByGlyphSetReference(self, g, useBase=True, doneLeft=None, doneRight=None):
        """If the angled left margin needs fixing, then set the value in the glyph. 
        Answer the boolean flag if something was changed."""
        changed = False
        if doneLeft is None:
            doneLeft = set()
        if g.name in doneLeft:
            print(f'### Circular reference in left margin for /{g.name}') # Check on possible circular references.
            return changed

        doneLeft.add(g.name)

        gd = self.md.glyphSet.get(g.name)
        if gd is None:
            return None # No entry in this glyphset for this glyph.

        # This sets the width, independent from later setting of the left margin.
        if gd.w == 0: 
            if isinstance(gd.w, (int, float)):
                w = gd.w
            else:
                assert gd.w in g.font, (f'### "gd.w={gd.w}" reference glyph for /{g.name} does not exist.') # Using "md.w" it should exist
                w = g.font[gd.w].width
            changed |= self.fixGlyphWidth(g, w, f'(w={gd.w})')

        # Try to figure out the rules for left margin in this glyph.
        if gd.l is not None: # Plain angled left margin
            if gd.l == 'off': # No automatic spacing, do manually
                return False
            elif gd.l == 'center': # Center the glyph on it's current defined width
                assert gd.w is not None, (f'gd.l=center also needs gd.w defined')
                changed |= self.fixGlyphWidth(g, gd.w, f"w={gd.w}")
                changed |= self.fixCenteredMargins(g, f"l='center'")
                return changed
            elif isinstance(gd.l, (int, float)): # It can be a value intead of a reference name
                lm = gd.l
            else:
                assert gd.l in g.font, (f'### "gd.l={gd.l}" reference glyph for /{g.name} does not exist.') # Using "md.l" it should exist
                lm = self.getLeftMarginByGlyphSetReference(g.font[gd.l], useBase, doneLeft, doneRight) # Get the left margin of the referenced glyph
            changed |= self.fixLeftMargin(g, lm, f'(l={gd.l})')
        
        elif gd.bl is not None: # Based left margin
            if isinstance(gd.bl, (int, float)): # Not entirely right, but we'll support values here too.
                lm = gd.bl
            else:
                assert gd.bl in g.font, (f'### "gd.bl={gd.bl}" reference glyph for /{g.name} does not exist.') # Using "md.bl" it should exist
                lm = self.getLeftMarginByGlyphSetReference(g.font[gd.bl], True, doneLeft, doneRight) # Get the left margin of the referenced glyph
            changed |= self.fixBasedLeftMargin(g, lm, f'(bl={gd.bl})')
        
        elif gd.r2l is not None: # Plain angled right margin to plain angled left margin
            assert gd.r2l in g.font, (f'### "gd.r2l={gd.r2l}" reference glyph for /{g.name} does not exist.') # Using "md.r2l" it should exist
            lm = self.getRightMarginByGlyphSetReference(g.font[gd.r2l], useBase, doneLeft, None) # Get the right margin of the referenced glyph
            changed |= self.fixLeftMargin(g, lm, f'(r2l={gd.r2l})')
        
        elif gd.br2l is not None: # Based right margin to plain angled left margin
            assert gd.br2l in g.font, (f'### "gd.br2l={gd.br2l}" reference glyph for /{g.name} does not exist.') # Using "bd.br2l" it should exist
            lm = self.getRightMarginByGlyphSetReference(g.font[gd.br2l], useBase, doneLeft, None) # Get the right margin of the referenced glyph
            changed |= self.fixLeftMargin(g, lm, f'(br2l={gd.br2l})')
        
        elif gd.r2bl is not None: # Plain angled right margin to based left margin
            assert gd.r2bl in g.font, (f'### "gd.r2bl={gd.r2bl}" reference glyph for /{g.name} does not exist.') # Using "md.r2bl" it should exist
            lm = self.getRightMarginByGlyphSetReference(g.font[gd.r2bl], useBase, doneLeft, None) # Get the right margin of the referenced glyph
            changed |= self.fixBasedLeftMargin(g, lm, f'(r2bl={gd.r2bl})')
        
        elif gd.br2bl is not None: # Based right margin to based left margin
            assert gd.br2bl in g.font, (f'### "gd.br2bl={gd.br2bl}" reference glyph for /{g.name} does not exist.') # Using "md.br2bl" it should exist
            lm = self.getRightMarginByGlyphSetReference(g.font[gd.br2bl], useBase, doneLeft, None) # Get the right margin of the referenced glyph
            changed |= self.fixBasedLeftMargin(g, lm, f'(br2bl={gd.br2bl})')
        
        # If there is a base in the glyphdata and no left margin reference, we go for that by default
        elif useBase and gd.base:
            assert gd.base in g.font, (f'### "gd.base={gd.base}" reference glyph for /{g.name} does not exist.') # Using "md.base" it should exist
            lm = self.getLeftMarginByGlyphSetReference(g.font[gd.base], useBase, doneLeft, None) # Get the left margin of the base glyph
            changed |= self.fixLeftMargin(g, lm, f'(base={gd.base})')
        return changed

    def fixRightMarginByGlyphSetReference(self, g, useBase=True, doneLeft=None, doneRight=None):
        """If the angled right margin needs fixing, then set the value in the glyph. 
        Answer the boolean flag if something was changed."""
        changed = False
        if doneRight is None:
            doneRight = set()
        if g.name in doneRight:
            print(f'### Circular reference in right margin for /{g.name}') # Check on possible circular references.
            return changed

        doneRight.add(g.name)

        gd = self.md.glyphSet.get(g.name)
        if gd is None:
            return None # No entry in this glyphset for this glyph.

        if gd.w is not None: # Just copy the width
            if isinstance(gd.w, (int, float)):
                w = gd.w
            else:
                assert gd.w in g.font, (f'### "gd.w={gd.w}" reference glyph for /{g.name} does not exist.') # Using "md.w" it should exist
                w = g.font[gd.w].width
            changed |= self.fixGlyphWidth(g, w, f'(w={gd.w})')

        elif gd.r is not None: # Plain angled right margin
            if gd.r == 'off': # No automatic spacing, do manually
                return False
            elif isinstance(gd.r, (int, float)): # It can be a value intead of a reference name
                rm = gd.r
            else:
                assert gd.r in g.font, (f'### "gd.r={gd.r}" reference glyph for /{g.name} does not exist.') # Using "md.r" it should exist
                rm = self.getRightMarginByGlyphSetReference(g.font[gd.r], useBase, doneLeft, doneRight) # Get the right margin of the referenced glyph
            changed |= self.fixRightMargin(g, rm, f'(r={gd.r})')
        
        elif gd.br is not None: # Based right margin
            if isinstance(gd.br, (int, float)): # Not entirely right, but we'll support values here too.
                rm = gd.br
            else:
                assert gd.br in g.font, (f'### "gd.br={gd.br}" reference glyph for /{g.name} does not exist.') # Using "md.br" it should exist
                rm = self.getRightMarginByGlyphSetReference(g.font[gd.br], True, doneLeft, doneRight) # Get the right margin of the referenced glyph
            changed |= self.fixBasedRightMargin(g, rm, f'(br={gd.br})')
        
        elif gd.l2r is not None: # Plain angled left margin to plain angled right margin
            assert gd.l2r in g.font, (f'### "gd.l2r={gd.l2r}" reference glyph for /{g.name} does not exist.') # Using "md.l2r" it should exist
            rm = self.getLeftMarginByGlyphSetReference(g.font[gd.l2r], useBase, doneLeft, None) # Get the left margin of the referenced glyph
            changed |= self.fixRightMargin(g, rm, f'(l2r={gd.l2r})')
        
        elif gd.bl2r is not None: # Based left margin to plain angled right margin
            assert gd.bl2r in g.font, (f'### "gd.bl2r={gd.bl2r}" reference glyph for /{g.name} does not exist.') # Using "bd.bl2r" it should exist
            rm = self.getLeftMarginByGlyphSetReference(g.font[gd.bl2r], useBase, doneLeft, None) # Get the left margin of the referenced glyph
            changed |= self.fixRightMargin(g, rm, f'(bl2r={gd.bl2r})')
        
        elif gd.l2br is not None: # Plain angled left margin to based right margin
            assert gd.l2br in g.font, (f'### "gd.l2br={gd.l2br}" reference glyph for /{g.name} does not exist.') # Using "md.l2br" it should exist
            rm = self.getLeftMarginByGlyphSetReference(g.font[gd.l2br], useBase, doneLeft, None) # Get the left margin of the referenced glyph
            changed |= self.fixBasedRightMargin(g, rm, f'(l2br={gd.l2br})')
        
        elif gd.bl2br is not None: # Based right margin to based left margin
            assert gd.bl2br in g.font, (f'### "gd.bl2br={gd.bl2br}" reference glyph for /{g.name} does not exist.') # Using "md.bl2br" it should exist
            rm = self.getLeftMarginByGlyphSetReference(g.font[gd.bl2br], useBase, doneLeft, None) # Get the left margin of the referenced glyph
            changed |= self.fixBasedRightMargin(g, rm, f'(bl2br={gd.bl2br})')
        
        # If there is a base in the glyphdata and no left margin reference, we go for that by default
        elif useBase and gd.base:
            assert gd.base in g.font, (f'### "gd.base={gd.base}" reference glyph for /{g.name} does not exist.') # Using "md.base" it should exist
            rm = self.getRightMarginByGlyphSetReference(g.font[gd.base], useBase, doneLeft, None) # Get the right margin of the base glyph
            changed |= self.fixRightMargin(g, rm, f'(base={gd.base})')
        return changed

    def getLeftMarginByGlyphSetReference(self, g, useBase=True, doneLeft=None, doneRight=None):
        """Answer the angled leftmargin, indicated by "l" reference in glyphdata. Answer None if there is no left reference.
        Test if there is a recursive reference """
        if doneLeft is None:
            doneLeft = set()
        if g.name in doneLeft:
            print(f'### Circular reference in left margin for /{g.name}') # Check on possible circular references.
            return g.angledLeftMargin

        doneLeft.add(g.name)

        gd = self.md.glyphSet.get(g.name)
        if gd is None:
            return None # No entry in this glyphset for this glyph.
        
        if gd.l is not None: # Plain angled left margin
            if gd.l == 'off':
                return g.angledLeftMargin # Nothing changed, adjust manually
            
            elif gd.l == 'center': # The margin is supposed to be centered.
                return (g.width - g.angledLeftMargin - g.angledRightMargin)/2

            elif isinstance(gd.l, (int, float)): # It can be a value intead of a reference name
                return gd.l
            
            assert gd.l in g.font, (f'### "gd.l={gd.l}" reference glyph for /{g.name} does not exist.') # Using "md.l" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.l], useBase, doneLeft, doneRight) # Get the left margin of the referenced glyph
        
        if gd.bl is not None: # Based left margin
            if isinstance(gd.bl, (int, float)): # Not entirely right, but we'll support values here too.
                return gd.bl
            assert gd.bl in g.font, (f'### "gd.bl={gd.bl}" reference glyph for /{g.name} does not exist.') # Using "md.bl" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.bl], True, doneLeft, doneRight) # Get the left margin of the referenced glyph
        
        if gd.r2l is not None: # Plain angled right margin to plain angled left margin
            assert gd.r2l in g.font, (f'### "gd.r2l={gd.r2l}" reference glyph for /{g.name} does not exist.') # Using "md.r2l" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.r2l], useBase, doneLeft, None) # Get the right margin of the referenced glyph
        
        if gd.br2l is not None: # Based right margin to plain angled left margin
            assert gd.br2l in g.font, (f'### "gd.br2l={gd.br2l}" reference glyph for /{g.name} does not exist.') # Using "bd.br2l" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.br2l], useBase, doneLeft, None) # Get the right margin of the referenced glyph
        
        if gd.r2bl is not None: # Plaing angled right margin to based left margin
            assert gd.r2bl in g.font, (f'### "gd.r2bl={gd.r2bl}" reference glyph for /{g.name} does not exist.') # Using "md.r2bl" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.r2bl], useBase, doneLeft, None) # Get the right margin of the referenced glyph
        
        if gd.br2bl is not None: # Based right margin to based left margin
            assert gd.br2bl in g.font, (f'### "gd.br2bl={gd.br2bl}" reference glyph for /{g.name} does not exist.') # Using "md.br2bl" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.br2bl], useBase, doneLeft, None) # Get the right margin of the referenced glyph
        
        # If there is a base in the glyphdata and no left margin reference, we go for that by default
        if useBase and gd.base:
            assert gd.base in g.font, (f'### "gd.base={gd.base}" reference glyph for /{g.name} does not exist.') # Using "md.base" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.base], useBase, doneLeft, doneRight)
        
        # End of reference sequence, just answer the left margin of this glyph
        if not hasattr(g, 'angledLeftMargin'):
            return g.leftMargin
        return g.angledLeftMargin

    def getRightMarginByGlyphSetReference(self, g, useBase=True, doneLeft=None, doneRight=None):
        """Answer the angled rightmargin, indicated by "r" reference in glyphdata. Answer None if there is no right reference.
        Test if there is a recursive reference """
        if doneRight is None:
            doneRight = set()
        if g.name in doneRight:
            print(f'### Circular reference in right margin for /{g.name}') # Check on possible circular references.
            return g.angledRightMargin

        doneRight.add(g.name)

        gd = self.md.glyphSet.get(g.name)
        if gd is None:
            return None # No entry in this glyphset for this glyph.
        
        if gd.r is not None:
            if gd.r == 'off':
                return g.angledRightMargin # Nothing changed, adjust manually
            elif isinstance(gd.r, (int, float)): # It can be a value instead of a reference name
                return gd.r
            assert gd.r in g.font, (f'### "gd.r={gd.r}" reference glyph for /{g.name} does not exist.') # Using "md.r" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.r], useBase, doneLeft, doneRight) # Get the right margin of the referenced glyph
        
        if gd.br is not None:
            if isinstance(gd.br, (int, float)): # Not entirely right, but we'll support values here too.
                return gd.br
            assert gd.br in g.font, (f'### "gd.br={gd.br}" reference glyph for /{g.name} does not exist.') # Using "md.br" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.br], True, doneLeft, doneRight) # Get the right margin of the referenced glyph
        
        if gd.l2r is not None:
            assert gd.l2r in g.font, (f'### "gd.l2r={gd.l2r}" reference glyph for /{g.name} does not exist.') # Using "md.l2r" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.l2r], useBase, None, doneRight) # Get the left margin of the referenced glyph
        
        if gd.l2br is not None: # Plain angled left margin to plain angled right margin
            assert gd.l2br in g.font, (f'### "gd.l2br={gd.l2br}" reference glyph for /{g.name} does not exist.') # Using "md.l2br" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.ml2r], useBase, None, doneRight) # Get the left margin of the referenced glyph
        
        if gd.bl2r is not None: # Based left margin to plain right margin 
            assert gd.bl2r in g.font, (f'### "gd.bl2r={gd.bl2r}" reference glyph for /{g.name} does not exist.') # Using "md.bl2r" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.bl2r], useBase, None, doneRight) # Get the left margin of the referenced glyph
        
        if gd.bl2br is not None:
            assert gd.bl2br in g.font, (f'### "gd.bl2br={gd.bl2br}" reference glyph for /{g.name} does not exist.') # Using "md.bl2br" it should exist
            return self.getLeftMarginByGlyphSetReference(g.font[gd.bl2br], useBase, None, doneRight) # Get the left margin of the referenced glyph
        
        # If there is a base in the glyphdata, we go for that.
        if useBase and gd.base:
            assert gd.base in g.font, (f'### "gd.base={gd.base}" reference glyph for /{g.name} does not exist.') # Using "md.base" it should exist
            return self.getRightMarginByGlyphSetReference(g.font[gd.base], True, doneLeft, doneRight)
        
        # End of reference sequence, just answer the left margin of this glyph
        if not hasattr(g, 'angledRightMargin'):
            return g.rightMargin
        return g.angledRightMargin

    #   B A S E  M A R G I N S

    def getComponentPosition(self, g, componentName):
        """Answer the (x, y) position of the named components. Answer None if the component does not exist."""
        for component in g.components:
            if component.baseGlyph == componentName:
                return component.transformation[-2:]
        return None

    def getBaseGlyph(self, g):
        """Answer the base glyph of g, if it is defined. Otherwise answer None."""
        assert g.name in self.md.glyphSet.glyphs
        gd = self.md.glyphSet.glyphs[g.name]
        if gd.base:
            assert gd.base in g.font
            return g.font[gd.base]
        return None

    def getBasedLeftMargin(self, g):
        """Answer the angled left margin of the base glyph component. Answer the g.angledLeftMargin if there is no base glyph component.
        If base or the base component are missing, a warning is printed."""
        base = self.getBaseGlyph(g)
        if base is not None:
            xy = self.getComponentPosition(g, base.name)
            if xy is not None:
                x, y, = xy
                return base.angledLeftMargin + x
        print(f'### getBasedLeftMargin: Cannot find base glyph or base component for /{g.name}')
        return g.angledLeftMargin

    def getBasedRightMargin(self, g):
        """Answer the angled right margin of the base glyph component. Answer the g.angledLeftMargin if there is no base glyph component.
        If base or the base component are missing, a warning is printed."""
        base = self.getBaseGlyph(g)
        if base is not None:
            xy = self.getComponentPosition(g, base.name)
            if xy is not None:
                x, y, = xy
                return base.angledRightMargin - x
        print(f'### getBasedRightMargin: Cannot find base glyph or base component for /{g.name}')
        return g.angledRightMargin

    def fixBasedLeftMargin(self, g, lm, label=''):
        """Set the left margin, relative to the current position of the base glyph component. If there is no base defined, then just set the left margin.
        Print a message and answer the True if the glyph margin was changed by a new value."""
        changed = False
        blm = self.getBasedLeftMargin(g)
        if abs(lm - blm) >= 1:
            print(f'Set based left margin of /{g.name} from {lm:0.2f} to {blm:0.2f} {label}')
            g.angledLeftMargin += lm - blm
            changed = True
        return changed

    def fixBasedRightMargin(self, g, rm, label=''):
        """Set the right margin, relative to the current position of the base glyph component. If there is no base defined, then just set the right margin.
        Print a message and answer the True if the glyph margin was changed by a new value."""
        changed = False
        brm = self.getBasedRightMargin(g)
        if abs(rm - brm) >= 1:
            print(f'Set based right margin of /{g.name} from {rm:0.2f} to {brm:0.2f} {label}')
            g.angledRightMargin += rm - brm
            changed = True
        return changed

    #   S P A C I N G  D E P E N D E N C I E S  B Y  G L Y P H  L I B

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

    #   M A R G I N S

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

    #   W I D T H

    def getWidth(self, g):
        """Try different strategies to find the width of the glyph:
        - Search by patterns.
        - Try groups
        - Similarity check
        """
        for width, patterns in self.fixedWidthPatterns.items(): # Predefined list by inheriting assistant class
            for pattern in patterns:
                if (pattern.endswith('|') and g.name.endswith(pattern[:-1])) or pattern in g.name:
                    print('ASSSAS', pattern, width, g.name)
                    return width
        # Could not find a valid width guess for this glyph.
        return None

    #   K E R N I N G

    def kernGroups(self, factor=1, calibrate=0, verbose=False):
        """This kerns all group pairs in KERN_GROUPS after clearing f.kerning first."""
        self.f.kerning.clear()
        for scriptName1, scriptName2 in KERN_GROUPS:
            print(f'... Kerning {scriptName1} - {scriptName2}')
            sLeft1, sRight1 = GROUP_NAME_PARTS[scriptName1] # Construct the group name for this script and this base group glyph name.
            sLeft2, sRight2 = GROUP_NAME_PARTS[scriptName2] # Construct the group name for this script and this base group glyph name.

            baseGlyphNames1 = self.groupBaseGlyphs[scriptName1]
            baseGlyphNames2 = self.groupBaseGlyphs[scriptName2]

            for baseGlyphName1 in baseGlyphNames1: # For each of the base group glyph names of this script.
                #if not baseGlyphName1 in ('V', 'A', 'T', 'period', 'n', 'o'):
                #    continue
                groupName1 = sLeft1 + baseGlyphName1 + sRight1
                for baseGlyphName2 in baseGlyphNames2: # For each of the base group glyph names of this script.
                    #if not baseGlyphName2 in ('V', 'A', 'T', 'period', 'n', 'o'):
                    #    continue
                    groupName2 = sLeft2 + baseGlyphName2 + sRight2
                    if baseGlyphName1 in self.f and baseGlyphName2 in self.f:
                        g1 = self.f[baseGlyphName1]
                        g2 = self.f[baseGlyphName2]
                        k = self.getKernNetKerning(g1, g2, step=None, factor=factor, calibrate=calibrate)
                        if abs(k) > 8:
                            if verbose:
                                print(f'... Set kerning ({groupName1}, {groupName2}) to {k}')
                            self.f.kerning[(groupName1, groupName2)] = k
                    else:
                        print(f'### Missing base glyphs for kerning ({baseGlyphName1}, {baseGlyphName2})')

        print(f'... Groups: {len(self.f.groups)} Kerning pairs {len(self.f.kerning)}')


    #   K E R N I N G  M E A S U R E

    def getTmpGlyph(self, g, tmpName):
        f = g.font
        if not tmpName in f:
            g.font.newGlyph(tmpName)
            tmp = f[tmpName]
        else:
            tmp = f[tmpName]
            tmp.clear()

        tmp.appendComponent(g.name)
        tmp.width = g.width
        tmp.decompose()
        q2b.curvesQ2B(tmp) # Remove overlap on quadratics does not work outside RoboFont
        tmp.removeOverlap()
        #tmp.removeOverlap() Just to be sure???
        return tmp

    def kernedDistance(self, g1, g2):
        """Answer the smallest distance that the kerned pair have to each other. Since there is not direct way to measure this,
        we need to use a time-expensive method: place them on kerned distance in a separate temporary glyph, decompse and remove overlap.
        If number of contours changes, then they are too close. Do a binary search for different distances until it falls within a range.
        Then we know how much the right glyph moved. 
        In order to make this happen we need to do a sequence of steps:
        - Copy g1 to /TMP1 glyph
        - Copy g2 to /TMP2 glyph
        - Decompose both
        - Convert to cubic, in case there are quadratic curves
        - Remove overlap in both temp glyphs. Now we have a reliable contour count in both.
        - Copy the glyph outlines of /TMP1 and /TMP2 to a combine TMP glyph, spaced by g1.width and (g1, g2) kerning.
        - Remove overlap. 
        Now if the amount of contours in /TMP changes, /TMP1 is too close and needs to move to the right (half the distance of last time)
        If the amount of contours in /TMP did not change, /TMP1 is too far out still. Move it to the left, half the distance of last time.
        Repeat the above until the moving distance gets below a certain threshold.
        """
        tmp1 = self.getTmpGlyph(g1, 'TMP1') # Could even be glyphs from another font than self.f 
        tmp2 = self.getTmpGlyph(g2, 'TMP2')
        k, groupK, kerningType = self.getKerning(g1.name, g2.name)
        step = -g1.width/2
        dist = newDist = g1.width + k
        # Make sure that the /TMP exists
        if 'TMP' not in self.f:
            g1.font.newGlyph('TMP')
        tmp = self.f['TMP']

        for n in range(0, 100): # Max number of iterations in the binary search
            #print(n, step)
            tmp.clear()
            tmp.appendComponent('TMP1')
            tmp.appendComponent('TMP2', offset=(newDist + step + k, 0))
            tmp.decompose()
            tmp.removeOverlap()
            if len(tmp.contours) == len(tmp1.contours) + len(tmp2.contours):
                # No overlap, go left
                #print('No overlap', dist, step, k, len(tmp.contours), len(tmp1.contours), len(tmp2.contours))
                if step > 0: 
                    step = -step * 0.5 # Reverse direction in slower speed
                # Otherwise step again with the same amount
            else:
                #print('Overlap', dist, step, k, len(tmp.contours), len(tmp1.contours), len(tmp2.contours))
                # Overlap, go right
                if step < 0:
                    step = -step * 0.5 # Reverse direction in slower speed
                # Otherwise step again with the same amount
 
            newDist += step # Keep new positiion

            if abs(step) < 4:
                break

        tmp.changed()
        return dist - newDist

    #   K E R N N E T  A I 

    KERNNET_UNIT = 4

    def getKernNetKerning(self, g1, g2, step=None, factor=1, calibrate=0):
        """Gernerate the kerning test image.
        Answer the KernNet predicted kerning for @g1 amd @g2. This assumes the KernNet server to be running on localhost:8080"""
        if step is None:
            step = self.KERNNET_UNIT
        f = g1.font
        imageName = 'test.png'
        tmpPath = '/tmp/com.typetr_imagePredict/'
        if not os.path.exists(tmpPath):
            os.makedirs(tmpPath, mode=0o777, exist_ok=False)
        kernImagePath = tmpPath + imageName
        iw = ih = 32
        scale = ih/f.info.unitsPerEm
        y = -f.info.descender 

        if 'Italic' in f.path:
            italicOffset = -50 # Calibrate HH shows in the middle
        else:
            italicOffset = 0
            
        im1 = g1.getRepresentation("defconAppKit.NSBezierPath")
        im2 = g2.getRepresentation("defconAppKit.NSBezierPath")
        s = iw / g1.font.info.unitsPerEm
        y = -g1.font.info.descender

        #if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
        db.newDrawing() # Calling the DrawBot libary
        db.newPage(iw, ih)
        
        #drawBot.fill(1, 0, 0, 1)
        #drawBot.rect(0, 0, iw, ih)
        db.fill(0)
        db.scale(s, s)
        db.save()
        db.translate(iw/s/2 - g1.width + italicOffset, y)
        db.drawPath(im1)
        db.restore()
        db.save()
        db.translate(iw/s/2 + italicOffset, y)
        db.drawPath(im2)
        db.restore()
        
        # If flag is set, clip space above capHeight and below baseline
        if 0 and self.controller.w.cropKernImage.get():
            db.fill(1, 0, 0, 1)
            db.rect(0, f.info.capHeight+600, iw/s, ih/s)
            db.fill(0, 0, 1, 1)
            db.rect(0, -ih/s, iw/s, ih/s-300)
            
        db.saveImage(kernImagePath)

        page = urllib.request.urlopen(f'http://localhost:8080/{g1.name}/{g2.name}/{imageName}')
        
        # Returned value is glyphName1/glyphName2/predictedKerningValue
        # The glyph names are returned to check validity of the kerning value.
        # Since the call is ansynchronic to the server, we still may get the answer here from a previous query.
        parts = str(page.read())[2:-1].split('/')
        if not len(parts) == 3 or parts[0] != g1.name or parts[1] != g2.name:
            print('### Predicted kerning query not value', parts)
            return None
            
        k = float(parts[-1]) # Extract the kerning from KernNet AI calculator
        k = (k + calibrate) * factor # Allows external calibrations for this pair
        
        # Calculate the rouned-truncated value of the floating         
        if abs(k) <= step:
            k = 0 # Apply threshold for very small kerning values
        ki = int(round(k * f.info.unitsPerEm/1000/step))*step # Scale the kerning value to our Em-size.  
        # print(f'... Predicted kerning {g1.name} -- {g2.name} k={k} kk={ki}')
            
        return ki


    #   S I M I L A R I T Y

    # Glyph names that are used as base for the seeds for the similarity checks
    # This means that all other glyphs in the set are within the tolerance range of these base glyphs.
    # These are the only ones that need to be spaced.
    # These lists are scanned in sequential order. If one of the glyphs existin in the similarity groups of the current glyphs,
    # the it is used a source for the sidebearing. 

    # @@@@@@ THIS OVERLAPS with the script-base groups on top of this file

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
        'Hdescender', 
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

    def getSimilarBaseName1(self, g):
        """Scan BASE1 in sequential order. If the glyph exits in self.similar1(g), then use it as source for the right margin.
        This avoid "inbreed" of similarity selections.
        If not found. The right side of g is too unique or there is not a base defined for it."""
        similar = set(self.getSimilarNames1(g))
        for gName in self.BASE1:
            if gName in similar:
                return gName
        return None # Not found. The right side of g is too unique or there is not a base defined for it.

    def getSimilarBaseGroupName1(self, g, baseName=None):
        """Answer the group name for left (1) that g is part of. If there no similar base name found,
        then use baseName. If that is not defined, then answer the group name constructed from g.name."""
        baseName1 = self.getSimilarBaseName2(g)
        if baseName1 is None:
            baseName1 = baseName
        if baseName1 is None:
            baseName1 = g.name
        return PUBLIC_KERN1 + baseName1
        
    def getSimilarBaseName2(self, g):
        """Scan BASE2 in sequential order. If the glyph exits in self.similar2(g), then use it as source for the right margin.
        This avoid "inbreed" of similarity selections.
        If not found. The right side of g is too unique or there is not a base defined for it."""
        similar = set(self.getSimilarNames2(g))
        for gName in self.BASE2:
            if gName in similar:
                return gName
        return None # Not found. The right side of g is too unique or there is not a base defined for it.

    def getSimilarBaseGroupName2(self, g, baseName=None):
        """Answer the group name for right (2) that g is part of. If there no similar base name found,
        then use baseName. If that is not defined, then answer the group name constructed from g.name."""
        baseName2 = self.getSimilarBaseName2(g)
        if baseName2 is None:
            baseName2 = baseName
        if baseName2 is None:
            baseName2 = g.name
        return PUBLIC_KERN2 + baseName2
               
    def getSimilar1(self, g):
        """Asnwer the dictionary of glyph names with similar shapes om the left side.
        Key is fraction of similarity, value is list of glyph names."""
        return self._getSimilar(g, 'right')

    def getSimilar2(self, g):
        """Asnwer the dictionary of glyph names with similar shapes om the left side.
        Key is fraction of similarity, value is list of glyph names."""
        return self._getSimilar(g, 'left')

    def _getSimilar(self, g, side):
        return g.getRepresentation(SimilarGlyphsKey,
            threshold=self.simT, 
            sameUnicodeClass=self.simSameUnicodeClass,
            sameUnicodeRange=self.simSameUnicodeRange,
            sameUnicodeScript=self.simSameUnicodeScript,
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

    def getSimilarMargins1(self, g):
        """Answer a dictionary of glyphs with similar right margins. Key is glyph name, value is angled right margin"""
        margins = {}
        f = g.font
        for gName in self.getSimilarNames1(g):
            margins[gName] = int(round(f[gName].angledRightMargin))
        return margins

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
                        groupName = PUBLIC_KERN1 + gName
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

    def getSimilarMargins2(self, g):
        """Answer a dictionary of glyphs with similar left margins. Key is glyph name, value if angled left margin"""
        margins = {}
        f = g.font
        for gName in self.getSimilarNames2(g):
            margins[gName] = int(round(f[gName].angledLeftMargin))
        return margins

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
                        groupName = PUBLIC_KERN2 + gName
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

    #   S A M P L E S

    def XXX_initSamples(self):
        """Answer lists of glyph names for the MAIN_SAMPLES. If a lower case glyph exists as small cap then add it to sampleCAPS.
        If a capital exists as small cap, then add it to the sampleC2SC. """
        sample = [] # List of glyph names
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

    SAMPLE_MODES = {
        0: 'getSpacingSample_GlyphSet',
        1: 'getSpacingSample_Similarity',
        2: 'getSpacingSample_Group',
        3: 'getSpacingSample_Spacing',
        4: 'getSpacingSample_GroupKerning',
    }

    def getSpacingSample(self, g, context=0, length=40, index=None, initialize=False):
        """Answer a single sample line of the defined length for the selected context.
        If the index in defined and the possible sample is larger than length, the slice the sample around the index.
        0    Glyphset
        1    According to similarity
        2    By group mode context
        3    By spacing mode context
        4    By group-kerning mode context

        The initialize flag forces the group-kerning to be initialized (or if it is still None)
        """
        return getattr(self, self.SAMPLE_MODES[context])(g, length, index=index, initialize=initialize)


    def getSpacingSample_GlyphSet(self, g, length, index=None, initialize=False):
        """Sample mode 0. Answer the sample, containing the full glyphset in the current RoboFont sorting, sorted by unicode.
        Always initialize, ignoring the flag. If index is not defined, then use self.sampleGlyphSetIndex. Otherwise set it to the new index."""
        if index is None:
            index = self.sampleGlyphSetIndex
        self.sampleGlyphSetIndex = index # Store this new index
        glyphNames = g.font.glyphOrder
        return glyphNames[index - int(length / 2) : max(len(glyphNames), index + int(length / 2))]

    def getSpacingSample_Similarity(self, g, length, index=None, initialize=False):
        """Sample mode 1. Answer the sample with glyphs matching the two similar sides of g.
        Always initialize, ignoring the flag. If index is not defined, then use self.sampleSimilarityIndex. Otherwise set it to the new index."""
        if index is None:
            index = self.sampleSimilarityIndex
        self.spacingSampleSimilarityIndex = index # Store this new index
        sample = []
        for perc, names in sorted(self.getSimilar2(g).items(), reverse=True):
            sample += names
        sample += ['hyphen', g.name, 'hyphen']
        for perc, names in sorted(self.getSimilar1(g).items(), reverse=True):
            sample += names
        return sample

    def getSpacingSample_Group(self, g, length, index=None, initialize=False):
        """Sample mode 2. Answer the sample, containing glyphs in the same groups as g.
        Always initialize, ignoring the flag. If index is not defined, then use self.sampleGroupIndex. Otherwise set it to the new index."""
        if index is None:
            index = self.sampleGroupIndex
        self.spacingSampleGroupIndex = index # Store this new index
        sample = ['B', g.name, 'B', g.name, 'O', g.name, 'O', 'H', g.name, 'H', g.name, 'H', g.name, 'H']
        while len(sample) < length:
            sample.append(g.name)
        return sample

    def getSpacingSample_Spacing(self, g, length, index=None, initialize=False):
        """Sample mode 3. Answer the sample, containing glyphs in the same spacing types as defined in the GlyphData.
        Always initialize, ignoring the flag. If index is not defined, then use self.sampleSpacingIndex. Otherwise set it to the new index."""
        if index is None:
            index = self.sampleSpacingIndex
        self.sampleSpacingIndex = index # Store this new index
        sample = [g.name, g.name, g.name, 'H', 'a', 'm', 'b', 'u', 'r', 'g', 'e', 'f', 'o', 'n', 't', 's', 't', 'i', 'v', 'I', 
            g.name, 'I', g.name, 'O', g.name, 'O', 'i', g.name, 'i', g.name, 'o', g.name, 'o']
        while len(sample) < length:
            sample.append(g.name)
        return sample

    def getSpacingSample_GroupKerning(self, g, length, index=None, initialize=False):
        """Build sample from permutating the groups. Now this depends on the hard coded lists of base glyphs per script. 
        This should become more generic, depending on the actual glyphset."""
        if index is None:
            index = self.sampleKerningIndex
        self.sampleKerningIndex = index # Store this new index
        if initialize:
            self._kerningSample = None # Force initiazation
        # Property will initialize the cached kerning sample if required, then slice it.
        return self.kerningSample[index - int(length / 2) : max(len(self.kerningSample), index + int(length / 2))]

    def _get_kerningSample(self):
        """Propery way to get the initialize cached kerning sample line.
        Initialize the kerning sample. There are various flavours possible for different stages in the process.
        For now we just initialize from the base glyphs of each group.
        """
        if self._kerningSample is None:
            # For now, in order to keep sync between the Assistant kerning lines and the proofing lines,
            # the initSample length needs to be a multiple of the line length 48
            initSample = [
                #'H', 'O', 'H', 'H', 'O', 'H', 'n', 'o', 'O', 'o', 'O', 'o', 'O',
                #'H', 'a', 'm', 'b', 'u', 'r', 'g', 'e', 'f', 'o', 'n', 't', 's', 't', 'i', 'v',
                #'H', 'a', 'm', 'b', 'u', 'r', 'g',
                #'H', 'A', 'M', 'B', 'U', 'R', 'G', 'E', 'F', 'O', 'N', 'T', 'S', 'T', 'I', 'V'
                ]
            exitSample = [
                'H', 'O', 'H', 'H', 'O', 'H', 'n', 'o', 'O', 'o', 'O', 'o', 'O',
                'H', 'a', 'm', 'b', 'u', 'r', 'g', 'e', 'f', 'o', 'n', 't', 's', 't', 'i', 'v',
                'H', 'a', 'm', 'b', 'u', 'r', 'g',
                'H', 'A', 'M', 'B', 'U', 'R', 'G', 'E', 'F', 'O', 'N', 'T', 'S', 'T', 'I', 'V'
                ]
            self._kerningSample = initSample.copy()
            for scriptName1, scriptName2 in KERN_GROUPS:
                pre1, ext1 = GROUP_NAME_PARTS[scriptName1]
                pre2, ext2 = GROUP_NAME_PARTS[scriptName2]
                baseGlyphs1 = sorted(GROUP_BASE_GLYPHS[scriptName1])
                baseGlyphs2 = sorted(GROUP_BASE_GLYPHS[scriptName2])
                for gName1 in baseGlyphs1:
                    if self._kerningSampleFilter1 is None or self._kerningSampleFilter1 == gName1:
                        for gName2 in baseGlyphs2:
                            if self._kerningSampleFilter2 is None or self._kerningSampleFilter2 == gName2:
                                self._kerningSample.append(gName1)
                                self._kerningSample.append(gName2)
            self._kerningSample += exitSample
        return self._kerningSample
    kerningSample = property(_get_kerningSample)

    def _get_sampleGlyphSetIndex(self):
        return self._sampleGlyphSetIndex
    def _set_sampleGlyphSetIndex(self, i):
        self._sampleGlyphSetIndex = min(max(i, 0), len(self._kerningSample))
    sampleGlyphSetIndex = property(_get_sampleGlyphSetIndex, _set_sampleGlyphSetIndex)
    
    def _get_sampleSimilarityIndex(self):
        return self._sampleSimilarityIndex
    def _set_sampleSimilarityIndex(self, i):
        self._sampleSimilarityIndex = min(max(i, 0), len(self._kerningSample))
    sampleSimilarityIndex = property(_get_sampleSimilarityIndex, _set_sampleSimilarityIndex)
    
    def _get_sampleGroupIndex(self):
        return self._sampleGroupIndex
    def _set_sampleGroupIndex(self, i):
        self._sampleGroupIndex = min(max(i, 0), len(self._kerningSample))
    sampleGroupIndex = property(_get_sampleGroupIndex, _set_sampleGroupIndex)
    
    def _get_sampleSpacingIndex(self):
        return self._sampleSpacingIndex
    def _set_sampleSpacingIndex(self, i):
        self._sampleSpacingIndex = min(max(i, 0), len(self._kerningSample))
    sampleSpacingIndex = property(_get_sampleSpacingIndex, _set_sampleSpacingIndex)
    
    def _get_sampleKerningIndex(self):
        return self._sampleKerningIndex
    def _set_sampleKerningIndex(self, i):
        self._sampleKerningIndex = min(max(i, 0), len(self._kerningSample))
    sampleKerningIndex = property(_get_sampleKerningIndex, _set_sampleKerningIndex)
    
    #   S A M P L E  F I L T E R S

    def _get_kerningSampleFilter1(self):
        return self._kerningSampleFilter1
    def _set_kerningSampleFilter1(self, s):
        self._kerningSampleFilter1 = s # Select kerning pairs in sample if None or if pattern is in the group base glyph name
        self._kerningSample = None # Force reset upon usage
    kerningSampleFilter1 = property(_get_kerningSampleFilter1, _set_kerningSampleFilter1)
    
    def _get_kerningFilterValue(self):
        return self._kerningFilterValue
    def _set_kerningFilterValue(self, k):
        self._kerningFilterValue = k # Select kerning pairs in sample if None or if pattern is in the group base glyph name
        self._kerningSample = None # Force reset upon usage
    kerningSampleValue = property(_get_kerningFilterValue, _set_kerningFilterValue)

    def _get_kerningSampleFilter2(self):
        return self._kerningSampleFilter2
    def _set_kerningSampleFilter2(self, s):
        self._kerningSampleFilter2 = s # Select kerning pairs in sample if None or if pattern is in the group base glyph name
        self._kerningSample = None # Force reset upon usage
    kerningSampleFilter2 = property(_get_kerningSampleFilter2, _set_kerningSampleFilter2)
    

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
        assert isinstance(gName1, str) and isinstance(gName2, str) # Common mistake to supply glyph here, instead of glyph names.

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
        """Set the kerning between gName1 and gName2 or their groups, depending on the kerningType.
        3 = glyph<-->glyph
        2 = group<-->glyph
        1 = glyph<-->group
        0 or None = group<-->group
        Answer the boolean if something changed.
        """
        assert self.f is not None
        assert kerningType in (None, 0, 1, 2, 3)
        changed = False
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
            changed = True
        elif k != self.f.kerning.get(pair): # If kerningType in (1, 2, 3) then kerning can be 0 to correct the group kerning
            print('... Set kerning %s to %d' % (pair, k))
            self.f.kerning[pair] = k
            changed = True

        return changed


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

