# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    buildgroups.py
#
#    D E P R E C A T E D
#    Use groupkerning instead.


from tnbits.model.objects.style import nakedStyle
from tnbits.errors.floqerror import FloqError

def sortValues(d):
    for k, v in d.items():
        d[k] = tuple(sorted(v))

def explodeKerning(kerning, groups):
    """Explode class kerning into 'flat' kerning.

    NOTE: make sure class kerning comes first. Sorting may be enough, as @
    comes before letters and glyph names cannot start with a digit.
    FIXME: should work recursively.
    """
    flatKerning = {}
    groupsUsed = set()
    groupsNotUsed = set()
    exceptions = set()
    groupNames = set(groups.keys()) # Fast searchable set of all group names.
    kerning = sorted(kerning.items())

    for (a, b), value in kerning:
        if isAGroup(a):
            # Check if this group really exists, otherwise ignore.
            if not a in groupNames:
                continue

            groupsUsed.add(a)
            aGlyphs = groups[a]
        else:
            aGlyphs = [a]

        if isAGroup(b):
            # Check if this group really exists, otherwise ignore.
            if not b in groupNames:
                continue

            groupsUsed.add(b)
            bGlyphs = groups[b]
        else:
            bGlyphs = [b]

        for a in aGlyphs:
            for b in bGlyphs:
                pair = a, b

                # Pair already exists.
                if pair in flatKerning:
                    if pair not in exceptions:
                        exceptions.add(pair)
                    else:
                        msg = 'Found a duplicate glyph pair (%s,  %s).' % (a, b)
                        print(msg)
                else:
                    flatKerning[pair] = value

    for g in groupNames:
        if not g in groupsUsed:
            groupsNotUsed.add(g)

    return flatKerning, groupsUsed, groupsNotUsed, exceptions

def isAGroup(name):
    if name.startswith('@') or name.startswith('public.kern'):
        return True
    return False

def makeProfiles(kerning):
    """
    NOTE: kerning must be flat!
    """
    firstProfiles = {}
    secondProfiles = {}

    for (first, second), value in kerning.items():
        if first not in firstProfiles:
            firstProfiles[first] = set()
        firstProfiles[first].add((second, value))   # (oppositeGlyph, kernValue)
        if second not in secondProfiles:
            secondProfiles[second] = set()
        secondProfiles[second].add((first, value))  # (oppositeGlyph, kernValue)

    sortValues(firstProfiles)
    sortValues(secondProfiles)
    return firstProfiles, secondProfiles

def makeGroupsFromProfiles(d):
    groups = {}
    for k, v in d.items():
        if v not in groups:
            groups[v] = []
        groups[v].append(k)
    sortValues(groups)
    return groups

def _getGlyphs2Groups(style, groupNames, glyphNames, groupName, glyphs2Groups):
    """glyphs2Groups is supposed to be dictionary {glyphName: [groupName, ...], ...}"""
    if groupName in groupNames:
        group = style.groups[groupName]
        for name in group:
            if name in glyphNames:  # Name must be a glyphName
                if not name in glyphs2Groups:  # Entry does not exist yet. add emptyt list
                    glyphs2Groups[name] = []
                glyphs2Groups[name].append(groupName)
            elif name.startswith('@'):  # Group in group, do recursive call, trying deeper.
                _getGlyphs2Groups(style, groupNames, glyphNames, name, glyphs2Groups)
            else:
                raise KeyError('Glyph "%s" does not exist.' % name)
    else:
        raise KeyError('Group "%s" does not exist.' % groupName)

def _initGlyphs2Groups(style):
    """Answer the dictionary that holds the reverse reference of group-->glyph. Answer dictionary {glyphName: [groupName, ...], ...}"""
    glyphs2Groups = {}
    groupNames = set(style.groups.keys())
    glyphNames = set(style.keys())
    for groupName in style.groups.keys():
        if groupName.startswith('@'):
            _getGlyphs2Groups(style, groupNames, glyphNames, groupName, glyphs2Groups)
    return glyphs2Groups

def getGlyphs2Groups(style):
    style = nakedStyle(style)
    if not hasattr(style, '_glyphs2Groups'):
        style._glyphs2Groups = _initGlyphs2Groups(style)
    return style._glyphs2Groups

def setKerning(style, name1, name2, value):
    """Test if name1 or name2 is part of a group. Then set the value for the group instead.
    If the cache dictionary does not exist in the style, then create it."""
    glyphs2Groups = getGlyphs2Groups(style)
    pair = glyphs2Groups.get(name1, name1), glyphs2Groups.get(name2, name2)
    style.kerning[pair] = value

def getKerning(style, name1, name2):
    glyphs2Groups = getGlyphs2Groups(style)
    pair = glyphs2Groups.get(name1, name1), glyphs2Groups.get(name2, name2)
    return style.kerning.get(pair)

def addGroup(style, groupName, group=None):
    if group is None:
        group = []
    if not groupName in style.groups.keys():
        style.groups[groupName] = group
    else:
        orgGroup = style.groups[groupName]
        for glyphName in group:
            if not glyphName in oldGroup:
                orgGroup.append(glyphName)
        style.groups[groupName] = orgGroup

def removeGroup(style, groupName):
    glyphs2Groups = getGlyphs2Groups(style)
    if groupName in style.groups.keys():
        for glyphName in style.groups[groupName]:
            group = glyph2Groups[glyphName]
            del group[group.index(groupName)]
            if len(group):
                del glyphs2Groups[glyphName]
        del style.groups[groupName]
    else:
        raise KeyError('Group "%s" does not exist.' % groupName)

def addGlyph2Group(style, glyphName, groupName):
    glyphs2Groups = getGlyphs2Groups(style)
    if not glyphName in glyphs2Groups:
        glyphs2Groups[glyphName] = [groupName]
    elif not groupName in glyphs2Groups[glyphName]:
        glyphs2Groups[glyphName].append(groupName)
    group = style.groups[groupName]
    if not glyphName in group:
        group.append(glyphName)
    else:
        raise KeyError('Glyph "%s" already exists in the group.' % glyphName)

def removeGlyphFromGroups(style, glyphName):
    glyphs2Groups = getGlyphs2Groups(style)
    for groupName in glyphs2Groups[glyphName]:
        # Remove backeard references
        group = style.groups[groupName]
        if glyphName in group:
            del group[group.index(glyphName)]
            style.groups[groupName] = group
    del glyphs2Groups[glyphName]

def makeGroupNames(groups, prefix):
    """Make group names from a prefix and the first glyph name in the group.
    or the sole glyph name itself if there is only one."""
    byName = {}
    byGroup = {}
    for group in groups:
        if len(group) == 1:
            name = group[0]
        else:
            name = prefix + group[0]
            byName[name] = group
        byGroup[group] = name
    return byName, byGroup

def buildStyleGroupKerning(style, verbose=False):

    flatKerning, usedGroupNames, groupsNotUsed, exceptions = explodeKerning(style.kerning, style.groups)

    if verbose:
        print("original number of kern pairs (with classes):", len(style.kerning))
        print("original number of groups used:", len(usedGroupNames))
        print("original number of exceptions:", len(exceptions))

    firstProfiles, secondProfiles = makeProfiles(flatKerning)

    if verbose:
        print
        print("--profiles--")
        print("number of first glyphs:", len(firstProfiles))
        print("number of unique first profiles:", len(set(firstProfiles.values())))
        print("number of second glyphs:", len(secondProfiles))
        print("number of unique second profiles:", len(set(secondProfiles.values())))
        print

    firstGroupsByValues = makeGroupsFromProfiles(firstProfiles)
    secondGroupsByValues = makeGroupsFromProfiles(secondProfiles)

    firstGroups = firstGroupsByValues.values()
    secondGroups = secondGroupsByValues.values()

    # print(firstGroupsByValues)

    firstByName, firstByGroup = makeGroupNames(firstGroups, "@KERN_FIRST_")
    secondByName, secondByGroup = makeGroupNames(secondGroups, "@KERN_SECOND_")

    newKerning = {}
    for fg in firstGroups:
        for sg in secondGroups:
            testPair = fg[0], sg[0]
            if testPair in flatKerning:
                value = flatKerning[testPair]
                newKerning[firstByGroup[fg], secondByGroup[sg]] = value
                # for f in fg:
                #     for s in sg:
                #         testPair = f, s
                #         if testPair in flatKerning:
                #             assert flatKerning[testPair] == value
                #         else:
                #             assert 0
            # else:
            #     for f in fg:
            #         for s in sg:
            #             testPair = f, s
            #             if testPair in flatKerning:
            #                 assert 0



    allGroups = {}
    allGroups.update(firstByName)
    allGroups.update(secondByName)

    if verbose:
        print("new number of kern pairs (with classes):", len(newKerning))
        print("new number of groups used:", len(allGroups))
        print("- number of 'first' groups:", len(firstByName))
        print("- number of 'second' groups:", len(secondByName))

    newFlatKerning, newUsedGroupNames, groupsNotUsed, newExceptions = explodeKerning(newKerning, allGroups)
    assert len(newUsedGroupNames) == len(allGroups)
    if verbose:
        print("new number of exceptions:", len(newExceptions))

        print("=====")

        print("amount of flat kerning, before, after:", len(newFlatKerning), len(flatKerning))

        missing = set(flatKerning) - set(newFlatKerning)
        if missing:
            print("missing:", len(missing))
            print(sorted(missing)[:20])
        else:
            print("new same as old:", flatKerning == newFlatKerning)
