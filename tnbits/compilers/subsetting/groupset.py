# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     groupset.py
#
class GroupSet(object):
    # The Group set holds/creates groups of glyphs set, under a unique name.
    def __init__(self):
        self.groups = {} # Name is key, group list is value
        self.revGroups = {} # Reverse: group list is key, name is value

    def __setitem__(self, name, glyphList):
        self.groups[name] = glyphList
        self.revGroups[tuple(glyphList)] = name

    def __getitem__(self, name):
        return self.groups.get(name)

    def items(self):
        return self.groups.items()

    def hasGroup(self, glyphList):
        return self.getNameOfGlyphs(glyphList) is not None

    def getNameOfGlyphs(self, glyphList):
        return self.revGroups.get(tuple(glyphList))

    def getUniqueGroupName(self, tag):
        # Calculate a unique group name, that is not in the groups keys yet.
        count = 0
        found = False
        while not found:
            uniqueName = '%s%d' % (tag, count)
            if not uniqueName in self.groups:
                found = True
            count += 1
        return uniqueName

    def aggregate(self, tag, glyphList):
        # If the glyphList has only one name, then answer the name without
        # adding it the group set.
        # If there are multiple names, then look if it already is part of the glyphset.
        # Then answer the name of that group. If the glyphList does not exist yet,
        # create a new unique name, based on the tag, store the glyphList under
        # that name and answer the new name.
        if len(glyphList) > 1:
            srcName = self.getNameOfGlyphs(glyphList)
            if srcName is None:
                srcName = self.getUniqueGroupName(tag)
                self[srcName] = glyphList
            srcOutput = '@' + srcName # Show the group name
        else:
            srcOutput = glyphList[0] # Show the name instead of group if only 1
        return srcOutput

