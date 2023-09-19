# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.constants import Constants
from tnbits.toolbox.fontparts.groups import GroupsTX
from tnbits.toolbox.mathematics import M
from fontTools.ttLib import newTable
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0

class KerningTX(object):
    """Contains class methods that manage the references within kerning."""

    C = Constants

    @classmethod
    def renameReference(cls, sourceName, destName, kerning, keepOriginal=False,
            DEBUG=False):
        """Renames a reference to a group or glyph in all pairs."""
        for pair, value in kerning.items():
            l, r = pair
            if l == sourceName or r == sourceName:
                if not keepOriginal:
                    # delete original pair
                    try:
                        del kerning[pair]
                    except:
                        kerning.remove(pair)
                # add new pair
                if l == sourceName:
                    l = destName
                if r == sourceName:
                    r = destName
                if DEBUG: print('NEW PAIR', (l, r), value)
                kerning[(l, r)] = value
        return kerning

    @classmethod
    def renameReferenceForLeftPairs(cls, sourceName, destName, kerning,
            keepOriginal=False, DEBUG=False):
        """Renames a reference to a group or glyph in all pairs.
        """
        for pair, value in kerning.items():
            l, r = pair
            if l == sourceName:
                if not keepOriginal:
                    # delete original pair.
                    try:
                        del kerning[pair]
                    except:
                        kerning.remove(pair)
                # add new pair.
                if DEBUG: print('NEW PAIR', (destName, r), value)
                kerning[(destName, r)] = value
        return kerning

    @classmethod
    def renameReferenceForRightPairs(cls, sourceName, destName, kerning,
            keepOriginal=False, DEBUG=False):
        """Renames a reference to a group or glyph in all pairs."""
        for pair, value in kerning.items():
            l, r = pair
            if r == sourceName:
                if not keepOriginal:
                    # delete original pair.
                    try:
                        del kerning[pair]
                    except:
                        kerning.remove(pair)
                # add new pair
                if DEBUG: print('NEW PAIR', (l, destName), value)
                kerning[(l, destName)] = value
        return kerning


    @classmethod
    def removeReference(cls, gName, kerning, collapse=True):
        """Removes a reference to a group or glyph in all pairs."""
        # remove from kerning
        for pair, value in kerning.items():
            l, r = pair
            if l == gName or r == gName:
                try:
                    del kerning[pair]
                except:
                    kerning.remove(pair)
        return kerning

    @classmethod
    def duplicateReference(cls, sourceName, destName, kerning, DEBUG=False):
        """Finds all pairs with _sourceName_, creates a duplicate of them with
        _destName_."""
        cls.renameReference(sourceName, destName, kerning, keepOriginal=True, DEBUG=DEBUG)

    @classmethod
    def swapReferences(cls, sourceName, destName, kerning, tempSuffix =
            '____________________'):
        """Swaps the positions of two references in all pairs. This is
        accomplished by a series of renames."""
        cls.renameReference(sourceName, sourceName+tempSuffix, kerning)
        cls.renameReference(destName, sourceName, kerning)
        cls.renameReference(sourceName+tempSuffix, destName, kerning)

    @classmethod
    def clean(cls, pairs=None, groups=None, glyphNames=None, font=None,
            verbose=False):
        """Gets rid of pairs that reference glyphs or groups that don't exist
        in the given font or list of glyph names."""
        # if no specific groups are given, get them from the font.
        if groups is None:
            groups = font.groups

        # if no specific glyphs are given, get them from the font.
        if glyphNames is None:
            glyphNames = font.keys()

        for pair, value in pairs.items():
            removePair = False
            l, r = pair
            if not l in glyphNames and not l in groups:
                removePair = True
            if not r in glyphNames and not r in groups:
                removePair = True
            if removePair:
                if verbose:
                    print('\tremoving', pair, value)
                try:
                    del pairs[pair]
                except:
                    pairs.remove(pair)
        return pairs

    # GET KERN VALUE.

    @classmethod
    def getValue(cls, pair, pairs={}, groups={}):
        """Returns the actual kerning value that will be displayed in the font,
        as determined by all glyph2glyph, glyph2group, group2glyph, and
        group2group pairs."""
         # define groups
        l, r = pair
        leftGroup = GroupsTX.getLeftKernGroupForGlyph(l, groups)
        rightGroup = GroupsTX.getRightKernGroupForGlyph(r, groups)
        # check pair
        if (l, r) in pairs:
            return pairs[(l, r)]
        # check group to glyph
        elif leftGroup and (leftGroup, r) in pairs:
            return pairs[(leftGroup, r)]
        elif rightGroup and (l, rightGroup) in pairs:
            return pairs[(l, rightGroup)]
        # check group to group
        elif leftGroup and rightGroup and (leftGroup, rightGroup) in pairs:
            return pairs[(leftGroup, rightGroup)]
        else:
            return 0

    @classmethod
    def getValuePair(cls, pair, pairs={}, groups={}):
        """Returns the actual kerning pair that will dictate the value in the
        font, as determined by all glyph2glyph, glyph2group, group2glyph, and
        group2group pairs."""
         # define groups
        l, r = pair
        leftGroup = GroupsTX.getLeftKernGroupForGlyph(l, groups)
        rightGroup = GroupsTX.getRightKernGroupForGlyph(r, groups)
        # check pair
        if (l, r) in pairs:
            return (l, r)
        # check group to glyph
        elif leftGroup and (leftGroup, r) in pairs:
            return (leftGroup, r)
        elif rightGroup and (l, rightGroup) in pairs:
            return (l, rightGroup)
        # check group to group
        elif leftGroup and rightGroup and (leftGroup, rightGroup) in pairs:
            return (leftGroup, rightGroup)
        else:
            return None

    # GET PAIRS BY TYPE.

    @classmethod
    def getGroupPairs(cls, pairs={}, groups={}):
        """Returns all pairs that involve a group."""
        groupPairs = {}
        for pair, value in pairs.items():
            left, right = pair
            if left in groups:
                groupPairs[pair] = value
            if right in groups:
                groupPairs[pair] = value
        return groupPairs

    # get kerning pairs and exceptions.

    @classmethod
    def getGrouplessPairs(cls, pairs={}, groups={}):
        """Returns all pairs that don't involve a group."""
        grouplessPairs = {}
        for pair, value in pairs.items():
            left, right = pair
            if not left in groups and not right in groups:
                grouplessPairs[pair] = value
        return grouplessPairs

    @classmethod
    def getPairsByType(cls, pairs={}, groups={}):
        """Returns a tuple with all pairs divided into four groups:

        - [0] Pairs with left and right group kerns
        - [1] Pairs with left group kerns
        - [2] Pairs with right group kerns
        - [3] Pairs with no group kern

        - Test type division.
        >>> getPairsByType({('@MMK_L_A', '@MMK_R_A'): 25,('@MMK_L_A', 'B'): 25, ('B', '@MMK_R_A'): 25,('A', 'B'): 25,}, {'@MMK_L_A': ['A', 'Aacute'],'@MMK_R_A': ['A', 'Aacute']})
        ({('@MMK_L_A', '@MMK_R_A'): 25}, {('@MMK_L_A', 'B'): 25}, {('B', '@MMK_R_A'): 25}, {('A', 'B'): 25})

        """
        group2group = {}
        group2glyph = {}
        glyph2group = {}
        glyph2glyph = {}
        for pair, value in pairs.items():
            left, right = pair
            if left in groups and right in groups:
                group2group[(left, right)] = value
            elif left in groups:
                group2glyph[(left, right)] = value
            elif right in groups:
                glyph2group[(left, right)] = value
            else:
                glyph2glyph[(left, right)] = value
        return (group2group, group2glyph, glyph2group, glyph2glyph)

    @classmethod
    def getPairsAndExceptionsByType(cls, pairs={}, groups={}):
        """Returns a tuple with all pairs divided into five groups:

        - [0] Pairs with group to group kerns
        - [1] Pairs with group-glyph or glyph-group kerns
        - [2] Exceptions with group-glyph or glyph-group kerns
        - [3] Pairs with no group kerns
        - [4] Exceptions with no group kerns.

        """
        group2group = {}
        group2glyph = {}
        glyph2glyph = {}
        group2glyphExceptions = {}
        glyph2glyphExceptions = {}
        # begin sorting
        for pair, value in pairs.items():
            left, right = pair
            if left in groups and right in groups:
                group2group[(left, right)] = value

            elif left in groups:
                rightGroup = GroupsTX.getRightKernGroupForGlyph(right, groups)
                if (left, rightGroup) in pairs:
                    group2glyphExceptions[(left, right)] = value
                else:
                    group2glyph[(left, right)] = value
            elif right in groups:
                leftGroup = GroupsTX.getLeftKernGroupForGlyph(left, groups)
                if (leftGroup, right) in pairs:
                    group2glyphExceptions[(left, right)] = value
                else:
                    group2glyph[(left, right)] = value
            else:
                leftGroup = GroupsTX.getLeftKernGroupForGlyph(left, groups)
                rightGroup = GroupsTX.getRightKernGroupForGlyph(right, groups)
                if (leftGroup, rightGroup) in pairs or (leftGroup, right) in pairs or (left, rightGroup) in pairs:
                    glyph2glyphExceptions[(left, right)] = value
                else:
                    glyph2glyph[(left, right)] = value
        return (group2group, group2glyph, group2glyphExceptions, glyph2glyph, glyph2glyphExceptions)

    @classmethod
    def getSeparatedPairs(cls, pairs, groups):
        """Parses _pairs_ and returns a monster tuple with the following
        collections:

        - [0] glyph-glyph
        - [1] glyph-glyph exceptions
        - [2] glyph-group exceptions
        - [3] group-glyph exceptions
        - [4] glyph-group
        - [5] group-glyph
        - [6] group-group

        (patterned after ufo2fdk.kernFeatureWriter method of the same name)

        """
        ## Separate the pairs
        glyph2Glyph = {}
        glyph2GlyphExceptions = {}
        glyph2Group = {}
        glyph2GroupExceptions = {}
        group2Glyph = {}
        group2GlyphExceptions = {}
        group2Group = {}

        for (left, right), value in pairs.items():
            if left in groups and right in groups:
                group2Group[left, right] = value
            elif left in groups:
                group2Glyph[left, right] = value
            elif right in groups:
                glyph2Group[left, right] = value
            else:
                glyph2Glyph[left, right] = value

        # Split out exceptions
        # glyph to glyph exceptions
        for (left, right), value in glyph2Glyph.items():
            if cls.isException((left, right), pairs, groups):
                glyph2GlyphExceptions[left, right] = value
                del glyph2Glyph[left, right]
        # glyph to group exceptions
        for (left, right), value in glyph2Group.items():
            if cls.isException((left, right), pairs, groups):
                glyph2GroupExceptions[left, right] = value
                del glyph2Group[left, right]
        # group to glyph exceptions
        for (left, right), value in group2Glyph.items():
            if cls.isException((left, right), pairs, groups):
                group2GlyphExceptions[left, right] = value
                del group2Glyph[left, right]
        ## Return the results
        return glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group

    @classmethod
    def getPairsGroup2Group(cls, pairs, groups):
        """Returns a dict of all group-group pairs."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        return group2Group

    @classmethod
    def getPairsGroup2Glyph(cls, pairs, groups, excludeExceptions=False):
        """Returns a dict of all group-glyph pairs.  If
        _excludeExceptions=True_ then only pairs that are not exceptions will
        be returned."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        if not excludeExceptions:
            group2Glyph.update(group2GlyphExceptions)
        return group2Glyph

    @classmethod
    def getPairsGlyph2Group(cls, pairs, groups, excludeExceptions=False):
        """Returns a dict of all glyph-group pairs. If _excludeExceptions=True_
        then only pairs that are not exceptions will be returned.  """
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        if not excludeExceptions:
            glyph2Group.update(glyph2GroupExceptions)
        return glyph2Group

    @classmethod
    def getPairsGroupAndGlyph(cls, pairs, groups, excludeExceptions=False):
        """Returns a dict of all pairs that involve a group and a glyph in
        either combination.  If _excludeExceptions=True_ then only pairs that
        are not exceptions will be returned."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        groupAndGlyph = group2Glyph
        groupAndGlyph.update(glyph2Group)
        if not excludeExceptions:
            groupGlyph.update(group2GlyphExceptions)
            groupGlyph.update(glyph2GroupExceptions)
        return groupAndGlyph

    @classmethod
    def getPairsGlyph2Glyph(cls, pairs, groups, excludeExceptions=False):
        """Returns a dict of all glyph-glyph pairs.  If
        _excludeExceptions=True_ then only pairs that are not exceptions will
        be returned."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        if not excludeExceptions:
            glyph2Glyph.update(glyph2GlyphExceptions)
        return glyph2Glyph

    @classmethod
    def getExceptionsGroup2Glyph(cls, pairs, groups):
        """Returns a dict of all class-kerning exceptions comprised of
        group-glyph pairs."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        return group2GlyphExceptions

    @classmethod
    def getExceptionsGlyph2Group(cls, pairs, groups):
        """Returns a dict of all class-kerning exceptions comprised of
        glyph-group pairs."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        return glyph2GroupExceptions

    @classmethod
    def getExceptionsGroupAndGlyph(cls, pairs, groups):
        """Returns a dict of all class-kerning exception pairs that involve a
        group and a glyph in either combination."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        groupAndGlyphExceptions = group2GlyphExceptions
        groupAndGlyphExceptions.update(glyph2GroupExceptions)
        return groupAndGlyphExceptions

    @classmethod
    def getExceptionsGlyph2Glyph(cls, pairs, groups):
        """Returns a dict of all class-kerning exceptions comprised of
        glyph-to-glyph pairs."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        return glyph2GlyphExceptions

    @classmethod
    def getExceptions(cls, pairs, groups):
        """Returns a dict of all class-kerning exception pairs -- glyph-glyph,
        glyph-group, and group-glyph."""
        glyph2Glyph, glyph2GlyphExceptions, glyph2GroupExceptions, group2GlyphExceptions, glyph2Group, group2Glyph, group2Group = cls.getSeparatedPairs(pairs, groups)
        exceptions = group2GlyphExceptions
        exceptions.update(glyph2GroupExceptions)
        exceptions.update(glyph2GlyphExceptions)
        return exceptions

    # PAIR TRANSFORMATIONS

    @classmethod
    def getPairParent(cls, target, pairs={}, groups={}):
        """Given an exception, returns the parent pair for the target pair. If
        the target has no parent, `getPairParent` returns the target pair."""
        left, right = target
        leftTop = left
        rightTop = right
        # get left group
        if left in groups:
            leftTop = left
        else:
            leftTop = GroupsTX.getLeftKernGroupForGlyph(left, groups)
        # get right group
        if right in groups:
            rightTop = right
        else:
            rightTop = GroupsTX.getRightKernGroupForGlyph(right, groups)

        if (leftTop, rightTop) in pairs:
            return (leftTop, rightTop)
        elif (left, rightTop) in pairs:
            return (left, rightTop)
        elif (leftTop, right) in pairs:
            return (leftTop, right)
        else:
            return (left, right)

    @classmethod
    def getPairExceptions(cls, target, pairs={}, groups={}):
        """Given a target pair (presumably one with a group), returns any
        existing exceptions that could modify that pair.

        - Test 2 groups
        >>> getPairExceptions(('@MMK_L_A', '@MMK_L_B'), {('@MMK_L_A', '@MMK_L_B'): -25, ('A', 'B'): -25}, groups={'@MMK_L_A': ['A', 'Aacute'], '@MMK_L_B': ['B']})
        {('A', 'B'): -25}

        """

        left, right = target
        exceptions = {}
        if left in groups and right in groups:
            for leftGlyph in groups[left]:
                gotException = False
                for rightGlyph in groups[right]:
                    if (leftGlyph, rightGlyph) in pairs:
                        exceptions[(leftGlyph, rightGlyph)] = pairs[(leftGlyph, rightGlyph)]
                        gotException = True
                    # get group to glyph exceptions
                    if not gotException and (left, rightGlyph) in pairs:
                        exceptions[(left, rightGlyph)] = pairs[(left, rightGlyph)]
                    if not gotException and (leftGlyph, right) in pairs:
                        exceptions[(leftGlyph, right)] = pairs[(leftGlyph, right)]
        elif left in groups:
            for leftGlyph in groups[left]:
                if (leftGlyph, right) in pairs:
                    exceptions[(leftGlyph, right)] = pairs[(leftGlyph, right)]
        elif right in groups:
            for rightGlyph in groups[right]:
                if (left, rightGlyph) in pairs:
                    exceptions[(left, rightGlyph)] = pairs[(left, rightGlyph)]
        return exceptions

    @classmethod
    def isException(cls, target, pairs={}, groups={}):
        """Returns True if the target pair is an exception, False if it is
        not."""
        if cls.getPairParent(target, pairs, groups) == target:
            return False
        else:
            return True

    @classmethod
    def isExceptionForPair(cls, exception, pair, pairs={}, groups={}):
        """Returns True if the given _exception_ an exception for a given
        _pair_, False if it is not."""
        if cls.getPairParent(exception, pairs, groups) == pair:
            return True
        else:
            return False

    @classmethod
    def getRedundantExceptions(cls, pairs={}, groups={}):
        """Gets exceptions that have the same value as their group parent.
        Gets exceptions that have the same value as their group parent.

        - Test group to group
        >>> getRedundantExceptions({('@MMK_L_A', '@MMK_L_B'): -25, ('A', 'B'): -25}, {'@MMK_L_A': ['A', 'Aacute'], '@MMK_L_B': ['B']})
        {('A', 'B'): -25}
        >>> getRedundantExceptions({('@MMK_L_A', 'B'): -25, ('A', 'B'): -25}, {'@MMK_L_A': ['A', 'Aacute'], '@MMK_L_B': ['B']})
        {('A', 'B'): -25}
        """
        redundant = {}
        for pair, value in pairs.items():
            exceptionPairs = cls.getPairExceptions(pair, pairs, groups)
            for exceptionPair, exceptionValue in exceptionPairs.items():
                if exceptionValue == value:
                    redundant[exceptionPair] = exceptionValue
        return redundant

    # SEARCH

    @classmethod
    def searchRightPairs(cls, names, pairs={}, groups={}, includeExceptions=True):
        """Gets all right kerns with a given name or list of names."""
        if isinstance(names, str):
            names = [names]
        result = {}
        for pair, value in pairs.items():
            left, right = pair
            if right in names:
                result[pair] = value
        if includeExceptions:
            for pair, value in pairs.items():
                if pair not in result:
                    parent = cls.getPairParent(pair, pairs, groups)
                    if parent in result.keys():
                        result[pair] = value
        return result

    @classmethod
    def searchLeftPairs(cls, names, pairs={}, groups={}, includeExceptions=True):
        """Gets all left kerns with a given name or list of names."""
        if isinstance(names, str):
            names = [names]
        result = {}
        for pair, value in pairs.items():
            left, right = pair
            if left in names:
                result[pair] = value
        if includeExceptions:
            for pair, value in pairs.items():
                if pair not in result:
                    parent = cls.getPairParent(pair, pairs, groups)
                    if parent in result.keys():
                        result[pair] = value
        return result

    @classmethod
    def searchPairs(cls, names, pairs={}, groups={}, includeExceptions=True):
        """Gets all kerns with a given name or list of names."""
        if isinstance(names, str):
            names = [names]
        result = {}
        for pair, value in pairs.items():
            left, right = pair
            if left in names or right in names:
                result[pair] = value
        if includeExceptions:
            for pair, value in pairs.items():
                if pair not in result:
                    #print('ppg', pair, pairs, groups)
                    parent = cls.getPairParent(pair, pairs, groups)
                    if parent in result.keys():
                        result[pair] = value
        return result

    # Flatten

    @classmethod
    def getFlattenedPairs(cls, pairs={}, groups={}):
        """Expands the groups and returns a much larger dictionary of flattened
        pairs.


        - Test flattening.
        >>> flattenKerns(pairs={('@MMK_L_A', '@MMK_R_A'): 25, ('Aacute', 'A'): 30}, groups={'@MMK_L_A': ['A', 'Aacute'], '@MMK_R_A': ['A', 'Aacute']})
        {('Aacute', 'Aacute'): 25, ('A', 'A'): 25, ('Aacute', 'A'): 30, ('A', 'Aacute'): 25}
        """
        newPairs = {}
        noGroups = {}

        # Sorts by right first to put classes ahead of individual glyphs. Then
        # sorts by left, leaving right in previous order; to ensure that class
        # exceptions get flattened correctly.
        sortedPairs = sorted(pairs.items(), key=lambda item: item[0][1])
        sortedPairs = sorted(sortedPairs)

        for pair, value in sortedPairs:
            left, right = pair

            # Both are groups.
            if left in groups and right in groups:
                for leftGlyph in groups[left]:
                    for rightGlyph in groups[right]:
                        newPairs[(leftGlyph, rightGlyph)] = value

            # Only left is a group.
            elif left in groups and not right in groups:
                for glyph in groups[left]:
                    newPairs[(glyph, right)] = value

            # Only right is a group.
            elif right in groups and not left in groups:
                for glyph in groups[right]:
                    newPairs[(left, glyph)] = value

            # No groups.
            else:
                noGroups[(left, right)] = value
                #newPairs[pair] = value

        # redundant? ^
        for pair, value in noGroups.items():
            newPairs[pair] = value

        return newPairs


    #ACTIONS

    @classmethod
    def round(cls, pairs={}, multiple=1, removeEmpty=True, verbose=False):
        """Rounds all _pairs_ to the nearest _multiple_, and remove pairs that
        zero out."""
        removeCount = 0
        newPairs = {}
        for pair, value in pairs.items():
            if pairs[pair] == 0 and removeEmpty:
                removeCount +=1
            else:
                newPairs[pair] = int(round(value / float(multiple))) * multiple
        if verbose:
            print('\t', removeCount, 'pairs were removed during rounding.')
        return newPairs

    @classmethod
    def scale(cls, pairs={}, multiplier=1):
        """Scales all _pairs_ by a _multiplier_."""
        for pair, value in pairs.items():
            pairs[pair] = int(value * multiplier)
        return pairs

    @classmethod
    def threshold(cls, pairs={}, minValue=1, maxValue=None, verbose=False):
        """Removes all _pairs_ below a certain _minValue_ in units."""
        removeCount = 0
        newPairs = {}
        for pair, value in pairs.items():
            add = True
            if minValue is not None and abs(value) < minValue:
                add = False
                removeCount += 1
            if maxValue is not None and abs(value) > maxValue:
                add = False
                removeCount += 1
            if add:
                newPairs[pair] = value                            
        if verbose:
            print('\t', removeCount, 'pairs were removed.')
        return pairs

    @classmethod
    def interpolate(cls, k1={}, k2={}, groups={}, value=0, round=1, testPair=None):
        """Interpolates class-based kerning. It is loosely based on the script
        that Cyrus dreamed about that one time. It only makes sense to me
        sometimes, but it combines class kerns, exceptions, and postscript
        (class-independent kerns)."""
        k1 = k1.copy()
        k2 = k2.copy()
        groups = groups.copy()

        # for each pole, split the pairs up into types
        group2group1, group2glyph1, group2glyphExceptions1, glyph2glyph1, glyph2glyphExceptions1 = cls.getPairsAndExceptionsByType(k1, groups)
        group2group2, group2glyph2, group2glyphExceptions2, glyph2glyph2, glyph2glyphExceptions2 = cls.getPairsAndExceptionsByType(k2, groups)

        # get every single pair that appears in either pole
        allPairs = set(list(k1.keys())+list(k2.keys()))

        # begin to assemble the segments
        group2group = {}
        group2glyph = {}
        group2glyphExceptions = {}
        glyph2glyph = {}
        glyph2glyphExceptions = {}
        newGroup2glyphExceptions = {}
        newGlyph2glyphExceptions = {}
        mixed = {}

        # there has got to be a more efficient way to do this
        # loop through all pairs, figure out the type, and interpolate accordingly
        for pair in allPairs:
            l, r = pair
            # CONSISTENT PAIRS
            # if both are group-to-group, interpolate the group-to-group values
            if pair in group2group1 and pair in group2group2:
                group2group[pair] = M.interpolate(group2group1[pair], group2group2[pair], value)
            # if both are group-to-glyph, interpolate the group-to-glyph values
            elif pair in group2glyph1 and pair in group2glyph2:
                group2glyph[pair] = M.interpolate(group2glyph1[pair], group2glyph2[pair], value)
                if pair == testPair:
                    print(pair, 'group-to-glyph', group2glyph[pair])
            # if both are glyph-to-glyph, interpolate the glyph-to-glyph values
            elif pair in glyph2glyph1 and pair in glyph2glyph2:
                glyph2glyph[pair] = M.interpolate(glyph2glyph1[pair], glyph2glyph2[pair], value)
                if pair == testPair:
                    print(pair, 'glyph-to-glyph', glyph2glyph[pair])
            # CONSISTENT EXCEPTIONS
            # if both are group to glyph exceptions, interpolate the exception values
            elif pair in group2glyphExceptions1 and pair in group2glyphExceptions2:
                group2glyphExceptions[pair] = M.interpolate(group2glyphExceptions1[pair], group2glyphExceptions2[pair], value)
                if pair == testPair:
                    print(pair, 'glyph-to-glyph exceptions, consistent', group2glyphExceptions[pair])
            # if both are glyph to glyph exceptions, interpolate the exception values
            elif pair in glyph2glyphExceptions1 and pair in glyph2glyphExceptions2:
                glyph2glyphExceptions[pair] = M.interpolate(glyph2glyphExceptions1[pair], glyph2glyphExceptions2[pair], value)
                if pair == testPair:
                    print(pair, 'glyph-to-glyph exceptions, consistent', glyph2glyphExceptions[pair])
            # INCONSISTENT EXCEPTIONS
            # if one pole has a pair and another pole does not, interpolate the pair with the other pole's apparent values
            elif pair in k1 and pair not in k2:
                mixed[pair] = M.interpolate(k1[pair], cls.getValue(pair, k2, groups), value)
                if pair == testPair:
                    print(pair, 'mixed exceptions (not k2), inconsistent', mixed[pair])
            elif pair not in k1 and pair in k2:
                mixed[pair] = M.interpolate(cls.getValue(pair, k1, groups), k2[pair], value)

                if pair == testPair:
                    print(pair, 'mixed exceptions (not k1), inconsistent', mixed[pair])

            # if one is an exception and the other one isn't, kern them anyway!
            elif pair in k1 and pair in k2:
                mixed[pair] = M.interpolate(cls.getValue(pair, k1, groups), cls.getValue(pair, k2, groups), value)
                if pair == testPair:
                    print(pair, 'mixed exceptions (both), inconsistent', mixed[pair])

            else:
                print('WARNING: could not kern pair', pair)
                print('\tgroup2group', pair in group2group1, pair in group2group2)
                print('\tgroup2glyph', pair in group2glyph1, pair in group2glyph2)
                print('\tgroup2glyphExceptions', pair in group2glyphExceptions1, pair in group2glyphExceptions2)
                print('\tglyph2glyph', pair in glyph2glyph1, pair in glyph2glyph2)
                print('\tglyph2glyphExceptions', pair in glyph2glyphExceptions1, pair in glyph2glyphExceptions2)

        # assemble the different parts
        newKerns = {}
        newKerns.update(group2group)
        newKerns.update(group2glyph)
        newKerns.update(group2glyphExceptions)
        newKerns.update(glyph2glyph)
        newKerns.update(glyph2glyphExceptions)
        newKerns.update(newGroup2glyphExceptions)
        newKerns.update(newGlyph2glyphExceptions)
        newKerns.update(mixed)

        # round
        if round:
            newKerns = cls.round(newKerns, round)

        return newKerns

    @classmethod
    def setTTFontKernTableFormat0(cls, ttfont, pairs):
        ttfont['kern'] = newTable('kern')
        ttfont['kern'].kernTables = []
        ttfont['kern'].version = 0
        zero = KernTable_format_0()
        zero.version = 0
        zero.coverage = 1
        zero.kernTable = pairs
        ttfont['kern'].kernTables.append(zero)


def explodeKerning(kerning, groups):
    """Explode class kerning into 'flat' kerning."""
    flatKerning = {}
    usedGroupNames = set()
    exceptions = set()
    groupNames = set(groups.keys()) # Fast searchable set of all group names.

    # XXX make sure class kerning comes first. Sorting may be enough, as @
    # comes before letters and glyph names cannot start with a digit.
    # BUG: This exploding should work recursively.
    kerning = sorted(kerning.items())

    for (a, b), value in kerning:
        if a[0] == "@":
            # Check if this group really exists, otherwise ignore.
            if not a in groupNames:
                continue
            usedGroupNames.add(a)
            aGlyphs = groups[a]
        else:
            aGlyphs = [a]

        if b[0] == "@":
            # Check if this group really exists, otherwise ignore.
            if not b in groupNames:
                continue
            usedGroupNames.add(b)
            bGlyphs = groups[b]
        else:
            bGlyphs = [b]

        for a in aGlyphs:
            for b in bGlyphs:
                testPair = a, b
                if testPair in flatKerning:
                    assert testPair not in exceptions
                    exceptions.add(testPair)
                    # print("====", testPair, flatKerning[testPair], value)
                flatKerning[testPair] = value

    return flatKerning, usedGroupNames, exceptions


if __name__ == "__main__":
    from mojo.roboFont import CurrentFont
    f = CurrentFont()
    k = f.kerning.asDict()
    print(len(k))
    t = KerningTX.threshold(k, 100)
    print(len(t))
    print(t.values())
    #import doctest
    #doctest.testmod()

    #groups = {'@MMK_L_A': ['A', 'Aacute'], '@MMK_R_A': ['A', 'Aacute']}
    #pairs = {('@MMK_L_A', '@MMK_R_A'): 25, ('Aacute', 'Aacute'): 125, ('@MMK_L_A', 'Aacute'): 350}

    #otherPairs = {('@MMK_L_A', 'v'): -25, ('v', '@MMK_R_A'): -550}

    #k = Kern(pairs, groups)
    #k.removeNames(['Aacute'])
