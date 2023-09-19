# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     groupskerning.py
#
#     MM compatible functions. Used by TextCenterMM
#

import os
from tnbits.toolbox.transformer import TX
from tnbits.toolbox.fontparts.groups import GroupsTX

#   G R O U P S

def getGlyphGroups(style, glyphName):
    """Answers the tuples of group names that glyph is part of. Note that this
    is a relative slow scanning method, therefore the calling application is
    responsible for caching the reversed relation."""
    groups = []
    for groupName, group in style.groups.items():
        if glyphName in group:
            groups.append(groupName)
    return groups

def getAllGlyphGroups(style):
    """Answers the dictionary of all glyph-->(leftGroup, rightGroup)
    references.  This is the reversed dictionary of the existing style.groups
    dictionary."""
    groups = {}
    for glyph in style:
        groups[glyph.name] = [None, None]
    for groupName, group in style.groups.items():
        for glyphName in group:
            if not glyphName in groups:
                continue
            if GroupsTX.isLeftKernGroup(groupName):
                groups[glyphName][0] = groupName
            elif GroupsTX.isRightKernGroup(groupName):
                groups[glyphName][1] = groupName
    return groups

def setGroupBase(style, groupName, baseName):
    """Sets the base of the group by renaming it and and references to it in
    all kerning pairs using this group name. Convention is MM group names
    @MMK_(LR)_(baseName), where baseName has any "." replaced into "_"."""
    if GroupsTX.isLeftKernGroup(groupName):
        newGroupName = GroupsTX.KERN_PREFIX_L + baseName
    elif GroupsTX.isRightKernGroup(groupName):
        newGroupName = GroupsTX.KERN_PREFIX_R + baseName
    renameGroup(style, groupName, newGroupName)

def renameGroup(style, oldName, newName):
    groups = style.groups
    assert not newName in groups
    kerning = style.kerning
    if oldName in groups and oldName != newName:
        # Rename the group entry.
        groups[newName] = groups[oldName]
        del groups[oldName]
        # Rename any reference of the group in other groups.
        for gName, group in groups.items():
            group = set(group)  # Remove any accidental duplicates.
            if oldName in group:
                group.remove(oldName)
                group.add(newName)
            groups[gName] = sorted(group)
        # Rename the kerning pair references.
        for pair in kerning.keys():
            if oldName == pair[0] and oldName == pair[1]:
                kerning[(newName, newName)] = kerning[pair]
                del kerning[pair]
            elif oldName == pair[0]:
                kerning[(newName, pair[1])] = kerning[pair]
                del kerning[pair]
            elif oldName == pair[1]:
                kerning[(pair[0], newName)] = kerning[pair]
                del kerning[pair]

def cleanGroups(style, removeDuplicates=True):
    """Remove all glyph references in the groups that don't exist in the style.
    Remove all group references that don't exist. Answer the set with deleted
    (reason, groupName, glyphName) tuples."""
    groups = style.groups
    groupNames = set(groups.keys())
    leftUsedNames = set()
    rightUsedNames = set()
    deleted = set()
    for groupName, group in groups.items():
        groupSet = set(group)  # Remove any accidental duplicates.
        isLeft = GroupsTX.isLeftKernGroup(groupName)
        isRight = GroupsTX.isRightKernGroup(groupName)
        changed = False
        for name in group:
            if removeDuplicates and isLeft and name in leftUsedNames:
                # print("Remove left duplicate", name, 'from', groupName)
                deleted.add(('Duplicate', groupName, name))
                groupSet.remove(name)
                changed = True
            elif removeDuplicates and isRight and name in rightUsedNames:
                # print("Remove right duplicate", name, 'from', groupName)
                deleted.add(('Duplicate', groupName, name))
                groupSet.remove(name)
                leftUsedNames.add(name)
                changed = True
            elif not name in style and not name in groupNames:
                # print("Remove missing style glyph", name, 'from', groupName)
                deleted.add(('Missing', groupName, name))
                groupSet.remove(name)
                rightUsedNames.add(name)
                changed = True

        if changed:
            if groupSet:  # Still names there?
                groups[groupName] = sorted(groupSet)
            else:
                del groups[groupName]
    return deleted

def groupsScript(style):
    """Answers the Python source that defines all current groups in the style.

    from tnbits.analyzers.analyzermanager import analyzerManager
    f = CurrentFont()
    print(groupsScript(f))
    """
    LINE = '#' + '-' * 30
    script = [
        '# -*- coding: UTF-8 -*-', LINE, '#    Groups of %s' % (style.path or 'Untitled'), LINE, '',
        'def g(groups, name, group):', '    groups[name] = sorted(set(group))', '', '',
        'def makeGroups(f):', '    groups = f.groups', '    groups.clear()', '',
    ]
    side = None
    groups = style.groups
    for groupName in sorted(groups.keys()):
        if side is None and GroupsTX.isLeftKernGroup(groupName):
            script.append('    ' + LINE)
            script.append('    #    L E F T = Right margin')
            script.append('    ' + LINE)
            side = 'LEFT'
        elif side is 'LEFT' and GroupsTX.isRightKernGroup(groupName):
            script.append('    ' + LINE)
            script.append('    #    R I G H T = Left margin')
            script.append('    ' + LINE)
            side = 'RIGHT'
        group = groups[groupName]
        script.append("    g(groups, '%s', %s)" % (groupName, repr(sorted(group))))
    # In case run as single file, add call for CurrentFont.
    script.append("\nif __name__ == '__main__':\n\tf = CurrentFont()\n\tmakeGroups(f)\n")
    return '\n'.join(script)

def exportGroupsScript(style):
    """Exports the groups script to a standard file. Uses the style name to
    create a path, where all spaces and hyphens in the name are replaced by
    underscores. This way the exported group can be imported by other scripts,
    e.g. in case the groups need to be applied on a whole family."""
    assert style.path is not None

    script = groupsScript(style)
    filePath = TX.path2FileName(style.path).replace(' ','_').replace('-','_').replace('.ufo','_Groups.py')
    scriptsPath = TX.path2ScriptsDir(style.path)

    try:
        os.makedirs(scriptsPath)
    except OSError:
        pass

    groupsPath = scriptsPath + '/' + filePath
    groupsFile = open(groupsPath, 'w')
    groupsFile.write(script)
    groupsFile.close()
    print('Written group script as', groupsPath)

#   K E R N I N G

def cleanKerning(style):
    """Cleans the kerning from all values that are 0, non-existing glyphs or
    non-existing groups. Answers the set with deleted (name1, name2, value)
    tuples."""
    deleted = set()
    groupNames = set(style.groups.keys())
    for (name1, name2), value in style.kerning.items():
        if (name1 in style or name1 in groupNames) and (name2 in style or name2 in groupNames) and value:
            continue
        # print('Remove non-existing pair', name1, name2, value)
        deleted.add((name1, name2, value))
        del style.kerning[(name1, name2, value)]
    return deleted

def kerningScript(style, U=1):
    """Answers the Python source that defines all current kerning in the style.

    from tnbits.analyzers.analyzermanager import analyzerManager
    f = CurrentFont()
    print(kerningScript(f) # Default unit = 1)
    """
    LINE = '#' + '-' * 30
    script = [
        '# -*- coding: UTF-8 -*-', LINE, '#\tKerning of %s' % (style.path or 'Untitled'), LINE, '',
        'def k(kerning, n1, n2, value):', '\tkerning[(n1, n2)] = value', '', '',
        'def makeKerning(f, U=%d):' % U, '\tk = f.kerning', ''
    ]
    kerning = style.kerning

    for pair in sorted(kerning.keys()):
        left, right = pair
        comment = ""
        if left.startswith('@') and not left in style.groups:
            script.append("\t# Left group %s does not exist" % left)
            comment = "# "
        if right.startswith('@') and not right in style.groups:
            script.append("\t# Right group %s does not exist" % right)
            comment = "# "
        value = kerning[pair]
        script.append("\t%sk[%s] = %d*U" % (comment, tuple(pair), int(round(value / U))))

    # In case run as single file, add call for CurrentFont.
    script.append("\nif __name__ == '__main__':\n\tf = CurrentFont()\n\tmakeKerning(f)\n")
    return '\n'.join(script)

def exportKerningScript(style):
    """Export the kerning script in a standard place. """
    assert style.path is not None
    script = kerningScript(style)
    filePath = TX.path2FileName(style.path).replace(' ','_').replace('-','_').replace('.ufo','_Kerning.py')
    scriptsPath = TX.path2ScriptsDir(style.path)

    try:
        os.makedirs(scriptsPath)
    except OSError:
        pass

    kerningPath = scriptsPath + '/' + filePath
    kerningFile = open(kerningPath, 'w')
    kerningFile.write(script)
    kerningFile.close()
    print('Written kerning script as', kerningPath)

