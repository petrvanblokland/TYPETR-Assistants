# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    xgroups.py
#

from tnbits.toolbox.fontparts.groups import GroupsTX

class XGroups(object):
    """Caches reverse group mappings for a font; glyph to left groups, right
    groups, left spacing groups and right spacing groups.

    * [style.path][glyphName] --> leftGroupName
    * [style.path][glyphName] --> rightGroupName
    * spacing groups with @SPC_L_
    * spacing groups with @SPC_R_.
    """

    def __init__(self, style):
        self.style = style
        self._glyph2leftGroup = {}
        self._glyph2rightGroup = {}
        self._glyph2leftSpacingGroup = {}
        self._glyph2rightSpacingGroup = {}
        xKernGroups = GroupsTX.getXKernGroups(self.style.groups)
        xSpaceGroups = GroupsTX.getXSpaceGroups(self.style.groups)
        self._glyph2leftGroup, self._glyph2rightGroup = xKernGroups
        self._glyph2leftSpacingGroup, self._glyph2rightSpacingGroup = xSpaceGroups

    def getAllGroups(self):
        return self._glyph2leftGroup, self._glyph2rightGroup, \
                self._glyph2leftSpacingGroup, self._glyph2rightSpacingGroup

    def getKerningGroups(self):
        return self._glyph2leftGroup, self._glyph2rightGroup
    
    def getSpacingGroups(self):
        return self._glyph2leftSpacingGroup, self._glyph2rightSpacingGroup
