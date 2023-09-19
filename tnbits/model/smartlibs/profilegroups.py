# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    profilegroups.py
#

from tnbits.model.smartlibs.smartlibbase import SmartLibBase
from tnbits.model import model
from tnbits.tools.constantsparts.smartsets import SPACE_CATEGORIES # Only make profile groups if glyph are same category

class Profile(object):
    """
    """

    RADIUS = 100
    GRID = 10
    NORMALIZE = 1000 # Multiplication factor of gauss levels, to store the sequence in integers.
    STEPS = 32 # Number of levels per em
    #KERNELS = {RADIUS/GRID: getKernel(RADIUS/GRID)} # Initialize default kernel.

    def __init__(self, styleKey, sideName, glyphName, rangeName, gauss=None, group=None, ignore=None, baseName=None):
        self.styleKey = styleKey
        self.sideName = sideName
        self.glyphName = glyphName
        # Name of the glyph that is source for the side spacing of glyphName. Same as glyphName is not defined.
        self.baseName = baseName or glyphName
        self.rangeName = rangeName
        self.gauss = gauss
        if group is None:
            group = set([glyphName])
        self.group = group
        if ignore is None:
            ignore = set()
        self.ignore = ignore
        # Default attributes
        self.grid = self.GRID
        self.radius = self.RADIUS
        self.normalize = self.NORMALIZE
        self._step = None # Property will be calculated on usage.
        self.minX = self.maxX = self.minY = self.maxY = None # Filled by self.calculateGauss

    def __repr__(self):
        return 'Profile(%s, base=%s, side=%s range=%s, gauss=%s, group=%s)' % (self.glyphName, self.baseName, self.sideName,
            self.rangeName, self.gauss, self.group)

    def clear(self):
        self._gauss = None

    def _get_gauss(self):
        if self._gauss is None:
            self._gauss = self.calculateGauss()
        return self._gauss
    def _set_gauss(self, values):
        # Set the gauss sequence, can be list or None.
        assert values is None or isinstance(values, (tuple, list))
        self._gauss = values
    gauss = property(_get_gauss, _set_gauss)

    def _get_step(self):
        if self._step is None:
            from tnbits.analyzers.analyzermanager import analyzerManager
            sa = analyzerManager.getStyleAnalyzer(styleKey=self.styleKey)
            self._step = sa.unitsPerEm / self.STEPS
        return self._step
    def _set_step(self, step):
        self._step = step
    step = property(_get_step, _set_step)

    def _getKernel(self):
        pass
        '''
        kernelKey = self.radius/self.grid
        if not kernelKey in self.KERNELS:
            self.KERNELS[kernelKey] = getKernel(kernelKey)
        return self.KERNELS[kernelKey]
        '''

    def calculateGauss(self):
        """Calculate the photons in each pixel on position self.x between the
        vertical range (self.y0, self.y1). Truncate the descender to a whole number of
        steps, to we get exactly to the baseline. Use the glyph related to this
        profile. Since we use styleKey and glyphName, this is always the latest version
        of the glyph, as know by the model/family/style storage. This
        guarantees consistency inside RoboFont, better than keeping a weakref to the
        style or glyph. Answer None if the style or glyph does not exist."""
        from tnbits.analyzers.analyzermanager import analyzerManager
        sa = analyzerManager.getStyleAnalyzer(styleKey=self.styleKey)
        if not self.glyphName in sa:
            return
        ga = sa[self.glyphName]
        # Get vertical range, scan in order of most frequent queries.
        if self.rangeName == 'xHeight':
            y0 = 0
            y1 = sa.xHeight + self.step
        elif self.rangeName == 'ascender':
            y0 = 0
            y1 = sa.ascender + self.step
        elif self.rangeName == 'capHeight':
            y0 = 0
            y1 = sa.capHeight + self.step
        elif self.rangeName == 'scapHeight':
            y0 = 0
            y1 = sa.scapHeight + self.step
        elif self.rangeName == 'descender':
            y0 = sa.descender - self.step
            y1 = 0

        box = ga.getVacuumeBox(minY=y0, maxY=y1)
        if box is None: # Not contours or components in the glyph.
            return
        x0, _, x1, _ = box
        if self.sideName == 'left':
            x = x0
        else:
            x = x1
        minY = y1 # Will be adjusted to the smallest y where the level is not zero.
        maxY = y0 # Will be adjusted to the largest y where the level is not zero.
        nsPathObject = ga.glyphPath
        kernel = self._getKernel() # Get cached kernel or create one for the current radius/grid measure.
        levels = []
        step = self.step # Initialize property if not yet used.
        for y in range(int(y0/step)*step, int(y1/step)*step, step):
            level = 0
            for pos, val in kernel.items():
                if nsPathObject.containsPoint_((x+pos[0]*self.GRID, y+pos[1]*self.GRID)):
                    level += int(round(val * self.normalize)) # Normalize on 1000x and round to integer.
            levels.append(level)
            if level: # If there is any light level on this y, then adjust the min/max
                minY = min(minY, y)
                maxY = max(maxY, y)
        self.x = x
        self.minX = x0
        self.maxX = x1
        self.minY = minY # Calculate Y-values where there was actually something non-white.
        self.maxY = maxY
        return levels

    def _get_average(self):
        """Answer the average level for all levels that are not zero."""
        sum = 0
        cnt = 0
        for level in self.gauss: # Get calculated sequence of gauss values.
            if level:
                sum += level
            cnt += 1 # Just calculate average for gauss values != 0
        if cnt:
            return sum/cnt
        return 0
    average = property(_get_average)

    def compare(self, profile, tolerance=40):
        """Compare the profiles. The tolerance indicates the max difference
        per level before the comparison aborts. It is assumed that the number of scan
        lines of self is equal to the number of the profile, otherwise the
        range compare is ignored. If the answer dictionary is empty, there is
        no range where these profiles are similar."""
        allEmpty = True

        # Only compare with identical number of levels, otherwise ignore profile height.
        if len(profile.gauss) == len(self.gauss):
            for index, level1 in enumerate(profile.gauss):
                level2 = self.gauss[index]

                if level1 or level2: # Avoid comparing empty with empty
                    allEmpty = False

                if tolerance < abs(level2 - level1): # If difference larger than tolerance, abort
                    return False

        return not allEmpty

class ProfileGroups(SmartLibBase):
    """Keep the dictionary of all glyph profile groups for the specified side as choice of ('left', 'right').
    This can be extended later for vertical spacing classes. Note that it is up to the caller to check consistency
    of the space classes dictionary, e.g. that base glyphName cannot exist in one of the other classes.
    And on base name change, the classes should be checked, because another class with the same base may have been
    overwritten.
    The profile groups are created by side comparison with Erik's Gauss "photon-counting". In combination with
    permutated comparison, this is relative expensive method, so we'll cache the glyph groups that are the result of it.
    Note that due to the convenience of storing the groups as one dictionary in the style.lib, it is possible that
    a glyph name not longer exists in the style. The caller should test on this. The Builder tool provides a
    function to clean the groups of glyphs that are added to or removed from the style.
    The caller can make direct changes to the answered dictionaries, which then are automatically saved with
    the style.lib.
    For storage in the lib the gauss sequence is only saved once for the whole profile group. Potentiall this creates
    a small rounding error between the stored sequence and the actual sequence per glyph, but that does not seem to
    be a problem. The profiles get expanded on the individual glyph Profile instances, and any change to the outline
    will make the gauss values to be recalculated.

    The base glyph name reference in Profiles is used to copy the side from, e.g. with [=] key instruction in TextCenter.
    """
    # Format: style.lib['_tnSmartLibs']['tnProfileGroups'] = {
    #   'profiles': (
    #       {side:'left', range:'xHeight', base:'n', gauss:(0,12,23,43,55,67,45,33,21,5),
    #           group:(('m','n', ...), ignore:((ignoreNames, ...), ...),
    #       (side:'left', range:'capHeight', base:'O', gauss:(0,12,23,43,55,67,45,67,78,89,67,78,33,21,5),
    #           group:(('O','C','Q', ...), ignore:((ignoreNames, ...), ...),
    #    ),
    #   'mirrors': (
    #       ('leftright', (('x', 'k'), ...), ...),
    #   ),
    # }
    # Then the internal self.d will expand to the structure
    #
    # self.d = {
    #   'left': {
    #       'm': {'xHeight': Profile('m', base='n', gauss=(0,12,23,43,55,67,45,33,21,5),
    #           group: referencedGroup(('m', 'n', ...)), ignore: set(), ... },
    #       'n': {'xHeight': Profile('n', base='n', gauss=(0,12,23,43,55,67,45,33,21,5),
    #           group: referencedGroup(('m', 'n', ...)), ignore: set(), ... },
    #       'O': {'capHeight': Profile('O', base='O', gauss=(0,12,23,43,55,67,45,67,78,89,67,78,33,21,5),
    #           group: referencedGroup(('O','C','Q', ...)), ignore: set(), ...},
    #       'C': {'capHeight': Profile('C', base='O', gauss=(0,12,23,43,55,67,45,67,78,89,67,78,33,21,5),
    #           group: referencedGroup(('O','C','Q', ...)), ignore: set(), ...},
    #       'Q': {'capHeight': Profile('Q', base='O', gauss=(0,12,23,43,55,67,45,67,78,89,67,78,33,21,5),
    #           group: referencedGroup(('O','C','Q', ...)), ignore: set(), ...},
    #   },
    #   'right': {
    #       ...
    #   }
    # }
    # self.groups = [set(('m', 'n', ...)), set(('O','C','Q', ...))]

    PROFILE_CLASS = Profile

    TNTOOLS = 'tnTools'
    TNPROFILEGROUPS = 'tnProfileGroups'
    TNSIDES = ('left', 'right')
    TNPROFILERANGES = ('descender', 'xHeight', 'scapHeight', 'capHeight', 'ascender')

    @classmethod
    def getId(cls):
        return cls.TNPROFILEGROUPS

    def fromDict(self, rootD):
        """Redefine the default behavior of SmartLibBase. Convert the raw d from style.lib into the internal
        smartLib dictionary that we need. Create entries for all glyphs in a group, and replace the groups of
        glyph names by sets. Note that it is important that glyph references keep pointing to the same sets."""
        newD = {} # Reference glyphs names in groups.
        profiles = rootD.get('profiles')
        if isinstance(profiles, (list, tuple)): # List of profile data.
            for profileData in profiles:
                validData = False
                # TODO: This test can be removed later. Now only to solve development compatibilities with earlier data sets.
                if isinstance(profileData, (list, tuple)) and len(profiles) == 4:
                    sideName, rangeName, gauss, group = profiles
                    baseName = None
                    validData = True
                elif isinstance(profileData, dict):
                    sideName = profileData.get('side')
                    rangeName = profileData.get('range')
                    gauss = profileData.get('gauss')
                    group = profileData.get('group', [])
                    ignore = profileData.get('ignore', [])
                    baseName = profileData.get('base') # Name of base glyph for this spacing group.
                    validData = True
                if validData: # and False: Set to False if profile groups should not be read for debugging.
                    group = set(group) # Convert the list to a set to remove duplicates and making faster testing.
                    ignore = set(ignore)
                    for refName in group: # Build cross reference for each glyph in the group.
                        d = self.getDictByPath(newD, (sideName, refName), True)
                        d[rangeName] = self.PROFILE_CLASS(self.styleKey, sideName, refName, rangeName, gauss, group, ignore, baseName)
                        # Validate the ignore set. If in both sets, then remove from the ignore set.
                        # We don't can about an ignored glyph be part of another profile group. The user may want to
                        # force the glyph staying out of this group, even if the profile value suggests that is is part.
                        if refName in ignore:
                            ignore.remove(refName)

        return newD # Answer a copy of d, where each group of glyph names is replaced by a set.

    def keys(self):
        return self.d.keys()

    def getLeft(self):
        return self.d['left']

    def getRight(self):
        return self.d['right']

    def asDict(self):
        """Redefine the default behavior of SmartLibBase.asDict(). Convert the internal smartLib data into
        the dictionary that can be stored in style.lib."""
        groups = []
        exported = [] # Keep track of what we already did
        dCopy = dict(profiles=groups)
        for sideName, glyphs in self.d.items():
            for glyphName, ranges in glyphs.items():
                for rangeName, profile in ranges.items():
                    if not profile.group in exported:
                        # Convert the set to list and take the first as key.
                        # If there is any overlap between the ignore and group sets, validation be solved when reading by fromDict.
                        groups.append(dict(side=sideName, range=rangeName, gauss=profile.gauss or [],
                            ignore=sorted(profile.ignore or []),
                            group=sorted(profile.group or []), base=profile.baseName))
                        exported.append(profile.group)
        return dCopy

    def clear(self):
        """Clear the cached self.d."""
        self.d = {}

    def cleanUp(self):
        """Perform clean up and validation on the consistency of the profile group."""
        print('Clean up profile group.')
        for side in ('left', 'right'):
            toRemove = []
            for cname in self.d[side].keys():
                for ytype in self.d[side][cname]:
                    profile = self.d[side][cname][ytype]
                    # XREFs?
                    for gname in profile.group:
                        # Check if there is a cross reference.
                        #if not gname in pg.d[side]:
                        #   print('gname has no profile', ytype, side, gname)
                        #elif not ytype in pg.d[side][gname]:
                        #    print('No type', ytype, side, cname, '-->', gname, 'no', ytype)
                        if not cname in self.d[side][gname][ytype].group:
                            print('No XREF', ytype, side, gname, '-->', cname)
                            toRemove.append((gname, profile.group))
            for glyphName, group in toRemove:
                group.remove(glyphName)
                print('Removed', side, ytype, cname, '-->', gname, 'group',  group)

    def getDictByPath(self, d, paths, create=False):
        """Answer the style lib dictionary, indicated by paths. If the create flag is True, then create the path.
        Otherwise answer None if it does not exist. Answer None if style is None.
        Not that it is up to the caller to check for consistency inside the answered dictionary. Other than the standard
        Python classes is not allowed."""
        for path in paths:
            if path is None:
                break
            if not path in d:
                if create:
                    d[path] = {}
                else:
                    return None
            d = d[path]
        return d

    def getProfile(self, sideName, glyphName, rangeName, baseName=None, create=False):
        """Answer the Profile instance for this side, glyph and range. If the create flag is True, then
        create a new profile if it does not exist and also store it in cache for later use. Otherwise answer None."""
        glyphD = self.getDictByPath(self.d, (sideName, glyphName), create=create)
        if glyphD is not None:
            if rangeName in glyphD:
                return glyphD[rangeName]
            if create:
                group = set([glyphName])
                profile = glyphD[rangeName] = self.PROFILE_CLASS(self.styleKey, sideName, glyphName, rangeName, group=group, baseName=baseName)
                return profile
        return None

    def getRange(self, sideName, glyphName, rangeName):
        return self.getDictByPath(self.d, (sideName, glyphName, rangeName))

    def getGlyph(self, sideName, glyphName):
        return self.getDictByPath(self.d, (sideName, glyphName))

    def getSide(self, sideName):
        """Answer the dictionary with glyphs."""
        return self.getDictByPath(self.d, (sideName,))

    def getMatchingKerningProfiles(self, glyphName1, glyphName2):
        """Answer the tuple of 2 profiles that are most relevant in the kerning pair (glyphName1, glyphName2).
        Decide which range is best fitting and answers the profiles if they exist for that range. Otherwise
        create one or both of the profiles and store then in cache.
        The aim is that e.g. /A, /Aring - /e, /egrave may share the same profiles, where /T - /e and
        /T - /egrave often are different.
        Another challenge is that /A and /R share the same cap profile, but for /A/V and /R/V the profile
        should be different. But in practice this my be an exception that so much depends on the design,
        that the user will split the group manually in the TextCenter interface.
        """
        for rangeName in self.TNPROFILERANGES:
            r = self.getRange('right', glyphName1, rangeName)
            if r is not None:
                levels = r.calculateGauss()
        for rangeName in self.TNPROFILERANGES:
            r = self.getRange('left', glyphName2, rangeName)
            if r is not None:
                levels = r.calculateGauss()

    def getRangeGroups(self, sideName, rangeName):
        """Answer the list of unique groups for the give side and range. Note that the is created, not cached."""
        groups = []
        glyphs = self.getDictByPath(self.d, (sideName,))
        if glyphs is not None:
            for glyph in glyphs.values():
                if rangeName in glyph:
                    group = glyph[rangeName]
                    if not group in groups:
                        groups.append(glyph[rangeName])
        return groups

    def getSortedLeftGroup(self, glyphName, rangeName):
        return sorted(self.getGroup('left', glyphName, rangeName))

    def getSortedRightGroup(self, glyphName, rangeName):
        return sorted(self.getGroup('right', glyphName, rangeName))

    def _joiningSpaceCategory(self, glyphName1, glyphName2):
        """Answer the boolean if glyphName1 and glyphName2 can join in the same space group, because they belong to
        the same space category."""
        for category in SPACE_CATEGORIES.values():
            if glyphName1 in category and glyphName2 in category:
                return True
        return False

    def add(self, sideName, glyphName, rangeName, baseName=None, create=True, force=False):
        """Add glyphName to the profile groups of baseName. If glyphName already exists in another group,
        then remove it there, and change the existing cross reference to the new group. Also remove the
        profile for side/glyph/range if it exists.
        Compare the profile.gauss with the existing profiles. If there is a close match by profile1.compare(profile2)
        than cross reference the groups. If there is no matching other profile, then store it as a separate group.
        Answer the profile as convenience for the caller.
        Default behavior is to skip ignored glyph names. The force attribute value overwrites this."""
        #if glyphName is not None and self.getDictByPath(self.d, (sideName, glyphName, rangeName)) is not None:
        #    self.remove(sideName, glyphName, rangeName)
        # Make a profile for this glyph.
        # If ignoring this name for this glyph name, then continue
        profile = self.getProfile(sideName, glyphName, rangeName, baseName, create=create)
        # If ignoring this name for this glyph name, then continue
        if profile is not None:
            searchedGlyphs = set()
            existingGlyphs = self.getDictByPath(self.d, (sideName,))
            found = False
            for existingGlyphName, rangeProfiles in existingGlyphs.items():
                # Check if existingGlyphName and glyphName are of the same space category, otherwise they
                # cannot join the same group.
                if self._joiningSpaceCategory(existingGlyphName, glyphName) and not existingGlyphName in searchedGlyphs \
                        and rangeName in rangeProfiles and not glyphName in profile.ignore:
                    existingProfile = rangeProfiles[rangeName]
                    if profile.compare(existingProfile):
                        profile.baseName = existingProfile.baseName # Copy the base name, if it is already defined.
                        group = profile.group = existingProfile.group
                        if force or not glyphName in profile.ignore:
                            group.add(glyphName)
                        found = True
                    searchedGlyphs = searchedGlyphs.union(existingProfile.group)
            if not found:
                if not glyphName in existingGlyphs:
                    existingGlyphs[glyphName] = {}
                existingGlyphs[glyphName][rangeName] = profile
        return profile

    def addLeft(self, baseName, rangeName, create=True):
        self.add('left', baseName, rangeName, create=create)

    def addRight(self, baseName, rangeName, create=True):
        self.add('right', baseName, rangeName, create=create)

    def reprofile(self, profile):
        """Delete profile and try to redistribute all profile.group glyphs into existing profiles."""
        group = sorted(profile.group) # Sort and make sure to have a copy, since the remove is adjusting the set.
        for glyphName in group:
            self.remove(profile.sideName, glyphName)
        # Now try to add this glyph to an existing profile, without creating a new one.
        for glyphName in group:
            for rangeName in self.TNPROFILERANGES:
                self.add(profile.sideName, glyphName, rangeName, create=False)

    def remove(self, sideName, glyphName, rangeName=None, ignore=True):
        """Remove the glyphName from the profile group for the defined side. If no rangeName is defined,
        remove the glyph reference from all ranges."""
        glyphD = self.getDictByPath(self.d, (sideName, glyphName))
        if glyphD is not None: # GlyphD is a dictionary of ranges with a profile as value
            if rangeName is None:
                rangeNames = glyphD.keys()
            else:
                rangeNames = [rangeName]
            for rangeName in rangeNames:
                if rangeName in glyphD: # Remove the profile for this side/glyph/range if it exists.
                    profile = glyphD[rangeName]
                    if glyphName in profile.group:
                        profile.group.remove(glyphName)
                        if ignore:
                            profile.ignore.add(glyphName)
                    del glyphD[rangeName]
            if not glyphD: # All ranged removed, then remove the glyph profile from the side.
                side = self.getDictByPath(self.d, (sideName,))
                del side[glyphName]

    def removeLeft(self, glyphName, rangeName=None, ignore=True):
        self.remove('left', glyphName, rangeName, ignore)

    def removeRight(self, glyphName, rangeName=None, ignore=True):
        self.remove('right', glyphName, rangeName, ignore)

    def setBaseName(self, sideName, glyphName, rangeName, baseName):
        """Set the base of the glyphName to baseName, if the profile exists in self. Ignore if it does
        not exist. Answer the boolean setting was successful."""
        profile = self.getProfile(sideName, glyphName, rangeName, create=False)
        if profile is not None:
            profile.baseName = baseName
            return True
        return False

if __file__ == '__main__':
    from tnbits.model.smartlibs.profilegroups import ProfileGroups

    f = CurrentFont()
    pg = ProfileGroups.getLib(f)
    pg.add('left', 'H', 'capHeight')
    print(1, pg)
    pg.addLeft('H', 'capHeight', 'L')
    print(2, pg)
    pg.addLeft('O', 'capHeight', 'Q')
    print(3, pg)
    pg.remove('left', 'Q', 'capHeight')
    print(4, pg)
    print(5, 'capHeight groups', pg.getRangeGroups('left', 'capHeight'))
    pg.save()
    # Show data structure present in the naked style._tnSmartLibs
    print(f.naked()._tnSmartLibs[ProfileGroups.getId()].d)
    # Show data structure present in the style.lib
    print(f.lib['_tnSmartLibs']['tnProfileGroups'])
