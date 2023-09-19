# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#


class GroupsTX:
    """GroupsTX contains class methods to manage the references within groups.
    Groups can be provided as a RGroups object or as a regular dictionary."""

    # left groups are keys, right groups are values.

    # Default kern prefixes when automatically generating group name from glyph
    # name.
    KERN_PREFIX_L = '@MMK_L_' 
    KERN_PREFIX_R = '@MMK_R_' 

    PUBLIC_KERN1_PREFIX = 'public.kern1'
    PUBLIC_KERN2_PREFIX = 'public.kern2'

    KERN_GROUP_PREFIXES = {
        KERN_PREFIX_L: KERN_PREFIX_R,
        PUBLIC_KERN1_PREFIX: PUBLIC_KERN2_PREFIX,
        '@'+PUBLIC_KERN1_PREFIX: '@'+PUBLIC_KERN2_PREFIX,
        # Happens with automatic conversion by RoboFont2
        PUBLIC_KERN1_PREFIX+'.'+KERN_PREFIX_L: PUBLIC_KERN2_PREFIX+'.'+KERN_PREFIX_R, 
        '@KERN_LEFT_': '@KERN_RIGHT_',
    }

    SPACE_PREFIX_L = '@SPC_L_'
    SPACE_PREFIX_R = '@SPC_R_'
    SPACE_GROUP_PREFIXES = {SPACE_PREFIX_L: SPACE_PREFIX_R}

    # IDENTITY.

    @classmethod
    def copy(cls, source, dest=None):
        groups = {}
        for groupName, groupGlyphs in source.items():
            groups[groupName] = groupGlyphs[:]
        if dest:
            dest.update(groups)
        else:
            return groups


    @classmethod
    def isGroup(cls, name):
        """Given a name, `isGroup` determines whether it is a group (based on @
        prefix)."""
        if name[0] == '@':
            return True
        else:
            return False

    @classmethod
    def isKernGroup(cls, groupName):
        """Given a name, `isKernGroup` determines whether it is a kerning group
        (based on @MMK or @public.kern prefix)."""
        if groupName is not None:
            kernGroupPrefixes = list(cls.KERN_GROUP_PREFIXES.keys()) + \
                    list(cls.KERN_GROUP_PREFIXES.values())
            for prefix in kernGroupPrefixes:
                if groupName.startswith(prefix):
                    return True
        return False

    @classmethod
    def isLeftKernGroup(cls, groupName):
        """Given a name, `isLeftKernGroup` determines whether it is a left side
        kerning group."""
        if groupName is not None:
            kernGroupPrefixes = cls.KERN_GROUP_PREFIXES.keys()
            for prefix in kernGroupPrefixes:
                if groupName.startswith(prefix):
                    return True
        return False

    @classmethod
    def isRightKernGroup(cls, groupName):
        """Given a name, `isRightKernGroup` determines whether it is a right
        side kerning group."""
        if groupName is not None:
            kernGroupPrefixes = cls.KERN_GROUP_PREFIXES.values()
            for prefix in kernGroupPrefixes:
                if groupName.startswith(prefix):
                    return True
        return False

    @classmethod
    def getOppositeKernGroup(cls, groupName):
        """Given a group name, `getOppositeKernGroup` gets the name of the
        equivalent group on the other side. (if left, get right. if right, get
        left)."""
        if groupName is not None:
            opp = None
            for kernPrefixLeft, kernPrefixRight in cls.KERN_GROUP_PREFIXES.items():
                if groupName[0:len(kernPrefixLeft)] == kernPrefixLeft:
                    opp = kernPrefixRight + groupName[len(kernPrefixLeft):]
                elif groupName[0:len(kernPrefixRight)] == kernPrefixRight:
                    opp = kernPrefixLeft + groupName[len(kernPrefixRight):]
        return opp

    # SPACE GROUPS.

    @classmethod
    def isSpaceGroup(cls, groupName):
        """Given a name, `isKernGroup` determines whether it is a spacing group
        (based on @SPC or @public.kern prefix)."""
        if groupName is not None:
            spaceGroupPrefixes = cls.SPACE_GROUP_PREFIXES.keys() + \
                    cls.SPACE_GROUP_PREFIXES.values()
            for prefix in spaceGroupPrefixes:
                if groupName.startswith(prefix):
                    return True
        return False

    @classmethod
    def isLeftSpaceGroup(cls, groupName):
        """Given a name, `isLeftSpaceGroup` determines whether it is a left
        side spacing group."""
        if groupName is not None:
            spaceGroupPrefixes = cls.SPACE_GROUP_PREFIXES.keys()
            for prefix in spaceGroupPrefixes:
                if groupName.startswith(prefix):
                    return True
        return False

    @classmethod
    def isRightSpaceGroup(cls, groupName):
        """Given a name, `isRightKernGroup` determines whether it is a right
        side spacing group."""
        if groupName is not None:
            spaceGroupPrefixes = cls.SPACE_GROUP_PREFIXES.values()
            for prefix in spaceGroupPrefixes:
                if groupName.startswith(prefix):
                    return True
        return False

    @classmethod
    def cleanSpaceGroups(cls, groups):
        """For export, all space groups should be removed from the font."""
        spaceGroupPrefixes = cls.SPACE_GROUP_PREFIXES.keys() + \
                cls.SPACE_GROUP_PREFIXES.values()
        for groupName in groups.keys():
            for spaceGroupPrefix in spaceGroupPrefixes:
                if groupName.startswith(spaceGroupPrefix):
                    del groups[groupName]
                    break

    # REFERENCES.

    @classmethod
    def getGroupsForGlyph(cls, groups, glyphName):
        """`getGroupsForGlyph` gets the groups for which _glyphName_ is a
        member."""
        results = []
        for groupName, groupGlyphs in groups.items():
            if glyphName in groupGlyphs:
                results.append(groupName)
        return results

    @classmethod
    def clean(cls, groups, glyphs=None, font=None, collapse=True, sort=True,
            removeKeyGlyphMarker=True, checkGlyphsInMultipleKernGroups=True):
        """`clean` removes references to glyphs that do not exist in
        _glyphs_."""
        # if we are not given an explicit glyph list, get it from the font
        if glyphs is None:
            glyphs = font.keys()
        ###
        if checkGlyphsInMultipleKernGroups:
            errors = cls.checkGlyphsInMultipleKernGroups(groups)
            if errors:
                print('Glyphs in Multiple Kern Groups Error', errors)
                #return None
        for groupName, groupGlyphs in groups.items():
            newGroupGlyphs = []
            for groupGlyph in groupGlyphs:
                if removeKeyGlyphMarker:
                    if len(groupGlyph) > 0 and groupGlyph[-1] == "'":
                        groupGlyph = groupGlyph[:-1]
                if groupGlyph in glyphs:
                    newGroupGlyphs.append(groupGlyph)
            if newGroupGlyphs:
                if sort:
                    newGroupGlyphs.sort()
                groups[groupName] = newGroupGlyphs
            elif collapse:
                    del groups[groupName]
            else:
                groups[groupName] = []
        return groups

    @classmethod
    def cleanSingleGlyphGroups(cls, groups, kerning):
        """Removes all groups that only include a single glyph. If there is a
        kerning pair using the group, then replace the pair by the direct glyph
        name. If there are no glyphs in the group, then remove it anyway."""
        # Build replacement dictionary.
        obsoleteGroups = {} 

        for groupName, group in groups.items():
            # No reference, just remove it from the groups.
            if len(group) == 0: 
                # No need to search in kerning.
                del groups[groupName] 
            elif len(group) == 1:
                obsoleteGroups[groupName] = group[0]

        for (n1, n2), v in kerning.items():
            name1 = n1
            name2 = n2
            if n1 in obsoleteGroups:
                name1 = obsoleteGroups[n1]
            if n2 in obsoleteGroups:
                name2 = obsoleteGroups[n2]
            if name1 != n1 or name2 != n2: 
                # It changed, add value under new pair and remove original pair
                del kerning[(n1, n2)]
                # Now only overwrite if the pair does not already exist and if
                # the value is different (to avoid unnecessary making the style
                # dirty.
                if not (name1, name2) in kerning and kerning[(name1, name2)] != v:
                    kerning[(name1, name2)] = v

    @classmethod
    def checkGlyphsInMultipleKernGroups(cls, groups={}):
        """Checks to see if there are any glyphs in multiple kern groups."""
        errors = []
        leftGroups = cls.getLeftKernGroups(groups)
        leftGlyphs = []

        for groupName, groupGlyphs in leftGroups.items():
            for groupGlyph in groupGlyphs:
                if groupGlyph not in leftGlyphs:
                    leftGlyphs.append(groupGlyph)
                else:
                    errors.append((groupName, groupGlyph))

        rightGroups = cls.getRightKernGroups(groups)
        rightGlyphs = []

        for groupName, groupGlyphs in rightGroups.items():
            for groupGlyph in groupGlyphs:
                if groupGlyph not in rightGlyphs:
                    rightGlyphs.append(groupGlyph)
                else:
                    errors.append((groupName, groupGlyph))
        return errors

    @classmethod
    def renameReference(cls, sourceName, destName, groups):
        """Renames all references of a glyph _sourceName_ to _destName_."""
        for groupName, groupGlyphs in groups.items():
            groupGlyphs = list(groupGlyphs)
            if sourceName in groupGlyphs:
                for x, groupGlyph in enumerate(groupGlyphs):
                    if groupGlyph == sourceName:
                        groupGlyphs[x] = destName
                groups[groupName] = groupGlyphs
        return groups

    @classmethod
    def duplicateReference(cls, sourceName, destName, groups):
        """Creates a copy of all references to glyph _sourceName_ for
        _destName_."""
        for groupName, groupGlyphs in groups.items():
            if sourceName in groupGlyphs:
                newGroupGlyphs = []
                for groupGlyph in groupGlyphs:
                    if groupGlyph not in newGroupGlyphs:
                        newGroupGlyphs.append(groupGlyph)
                    if groupGlyph == sourceName and destName not in newGroupGlyphs:
                        newGroupGlyphs.append(destName)
                groups[groupName] = newGroupGlyphs
        return groups

    @classmethod
    def removeReference(cls, gName, groups, collapse=True):
        """Removes all references to a glyph, and collapses
        empty groups."""
        for groupName, groupGlyphs in groups.items():
            if gName in groupGlyphs:
                newGroupGlyphs = []
                for groupGlyph in groupGlyphs:
                    if gName != groupGlyph:
                        newGroupGlyphs.append(groupGlyph)
                if newGroupGlyphs != []:
                    groups[groupName] = newGroupGlyphs
                elif collapse:
                    del groups[groupName]
                else:
                    groups[groupName] = []
        return groups

    @classmethod
    def swapReferences(cls, sourceName, destName, groups, tempSuffix =
            '____________________'):
        """Swaps the positions of two references in all groups. This is
        accomplished by a series of renames."""
        cls.renameReference(sourceName, sourceName+tempSuffix, groups)
        cls.renameReference(destName, sourceName, groups)
        cls.renameReference(sourceName+tempSuffix, destName, groups)

    # KERNING GROUPS

    @classmethod
    def getKernGroups(cls, groups):
        """Returns only kerning groups."""
        kernGroups = {}
        for groupName, groupGlyphs in groups.items():
            if cls.isKernGroup(groupName):
                kernGroups[groupName] = groupGlyphs
        return kernGroups

    @classmethod
    def getLeftKernGroups(cls, groups):
        """Returns only left side kerning groups."""
        leftGroups = {}
        for groupName, groupGlyphs in groups.items():
            if cls.isLeftKernGroup(groupName):
                leftGroups[groupName] = groupGlyphs
        return leftGroups

    @classmethod
    def getRightKernGroups(cls, groups={}):
        """Returns only right side kerning groups."""
        rightGroups = {}
        for groupName, groupGlyphs in groups.items():
            if cls.isRightKernGroup(groupName):
                #if (gName and gName in groupGlyphs) or not gName:
                rightGroups[groupName] = groupGlyphs
        return rightGroups

    @classmethod
    def getKernGroupsForGlyph(cls, gName, groups={}):
        """Returns a left group and right group that
        contain a given glyph."""
        leftGroup = None
        rightGroup = None
        for groupName, groupGlyphs in groups.items():
            if cls.isLeftKernGroup(groupName) and gName in groupGlyphs and leftGroup is None:
                leftGroup = groupName
            elif cls.isRightKernGroup(groupName) and gName in groupGlyphs and rightGroup is None:
                rightGroup = groupName
            if leftGroup is not None and rightGroup is not None:
                break
        return leftGroup, rightGroup

    @classmethod
    def getLeftKernGroupForGlyph(cls, gName, groups={}):
        """Returns only the left side group that contain a given glyph."""
        return cls.getKernGroupsForGlyph(gName, groups)[0]

    @classmethod
    def getRightKernGroupForGlyph(cls, gName, groups={}):
        """Returns only the rigth side group that contain a given glyph."""
        return cls.getKernGroupsForGlyph(gName, groups)[1]

    @classmethod
    def getXKernGroups(cls, groups):
        """Answers the x-ref of kern groups, key is glyphName, value is list of
        group names."""
        leftGroups = {}
        rightGroups = {}

        for groupName, groupGlyphs in groups.items():
            if cls.isLeftKernGroup(groupName):
                for glyphName in groupGlyphs:
                    if not glyphName in leftGroups:
                        # Make a list, just in case. It is an MMK error to have
                        # multiple here.
                        leftGroups[glyphName] = [] 
                    leftGroups[glyphName].append(groupName)
            elif cls.isRightKernGroup(groupName):
                for glyphName in groupGlyphs:
                    if not glyphName in rightGroups:
                        # Make a list, just in case. It is an MMK error to have
                        # multiple here.
                        rightGroups[glyphName] = [] 
                    rightGroups[glyphName].append(groupName)

        return leftGroups, rightGroups

    @classmethod
    def getXSpaceGroups(cls, groups):
        """Answers the x-ref of kern groups, key is glyphName, value is list of
        group names."""
        leftGroups = {}
        rightGroups = {}

        for groupName, groupGlyphs in groups.items():
            if cls.isLeftSpaceGroup(groupName):
                for glyphName in groupGlyphs:
                    if not glyphName in leftGroups:
                        # Make a list, just in case. It is an MMK error to have
                        # multiple here.
                        leftGroups[glyphName] = [] 
                    leftGroups[glyphName].append(groupName)
            elif cls.isRightSpaceGroup(groupName):
                for glyphName in groupGlyphs:
                    if not glyphName in rightGroups:
                        # Make a list, just in case. It is an MMK error to have
                        # multiple here.
                        rightGroups[glyphName] = [] 
                    rightGroups[glyphName].append(groupName)
        return leftGroups, rightGroups

    @classmethod
    def getXLeftKernGroups(cls, groups):
        """Returns only left side x-ref kerning groups."""
        self.getXKernGroups(group)[0]

    @classmethod
    def getXRightKernGroups(cls, groups={}):
        """Returns only right side x-ref kerning groups."""
        self.getXKernGroups(group)[1]


    @classmethod
    def getAliases(cls, gnames=[], groups={}):
        """Gets all possible names for a list of glyph names. For each glyph
        name, it looks for any group names that could also be used to affect
        the kerning for that glyph."""
        if not isinstance(gnames, list):
            gnames = [gnames]
        allNames = []
        for gName in gnames:
            allNames.append(gName)
            left, right = cls.getKernGroupsForGlyph(gName, groups)
            if left and left not in allNames:
                allNames.append(left)
            if right and right not in allNames:
                allNames.append(right)
        return allNames

    @classmethod
    def getUnusedGroups(cls, pairs, groups):
        """Returns only groups that were not referenced in _pairs_."""
        usedNames = []
        for pair, value in pairs.items():
            left, right = pair
            if cls.isKernGroup(left) and left not in usedNames:
                usedNames.append(left)
            if cls.isKernGroup(right) and right not in usedNames:
                usedNames.append(right)
        unusedGroups = {}
        for groupName, groupGlyphs in groups.items():
            if cls.isKernGroup(groupName) and groupName not in usedNames:
                unusedGroups[groupName] = groupGlyphs
        return unusedGroups

    @classmethod
    def asFeatures(cls, groups, lineBreak='\r'):
        """Writes a group dictionary as feature definition language."""
        lines = []
        linebreak = '\n'
        groupNames = groups.keys()
        groupNames.sort()
        for groupName in groupNames:
            groupGlyphs = groups[groupName]
            if groupGlyphs:
                t = "@%s = [%s];" %(groupName, " ".join(groupGlyphs))
                t.replace("'")
                lines.append(t)
        return linebreak.join(lines)

if __name__ == "__main__":
    from mojo.roboFont import CurrentFont
    print(GroupsTX.clean(CurrentFont().groups, ['a', 'b', 'c']))
