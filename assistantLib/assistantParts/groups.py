# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   groups.py
#
import sys
from math import *
from vanilla import *
import importlib

# Add paths to libs in sibling repositories
#PATHS = ('../TYPETR-Assistants/',)
#for path in PATHS:
#    if not path in sys.path:
#        print('@@@ Append to sys.path', path)
#        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.glyphsets.anchorData import AD


class AssistantPartGroups(BaseAssistantPart):
    """Fix show and fix groups
    """

    GROUPS_LIST_FONT = 'Verdana'
    GROUPS_LIST_SIZE = 10
    GROUPS_LIST_NAME_SIZE = 24
    GROUPS_LIST_COLOR = (0.3, 0.3, 0.3, 1)

    def initMerzGroups(self, container):
        """Initialize the Merz instances for this assistant part.""" 
        self.groupsListLeftName = container.appendTextLineSublayer(
                name='groupsListLeftName',
                position=(0, 0),
                text='',
                font=self.GROUPS_LIST_FONT,
                pointSize=self.GROUPS_LIST_NAME_SIZE,
                fillColor=self.GROUPS_LIST_COLOR,
                visible=True,
            )
        self.groupsListLeft = container.appendTextLineSublayer(
                name='groupsListLeft',
                position=(0, 0),
                text='',
                font=self.GROUPS_LIST_FONT,
                pointSize=self.GROUPS_LIST_SIZE,
                fillColor=self.GROUPS_LIST_COLOR,
                visible=True,
            )

        self.groupsListRightName = container.appendTextLineSublayer(
                name='groupsListRightName',
                position=(0, 0),
                text='',
                font=self.GROUPS_LIST_FONT,
                pointSize=self.GROUPS_LIST_NAME_SIZE,
                fillColor=self.GROUPS_LIST_COLOR,
                visible=True,
            )
        self.groupsListRight = container.appendTextLineSublayer(
                name='groupsListRight',
                position=(0, 0),
                text='',
                font=self.GROUPS_LIST_FONT,
                pointSize=self.GROUPS_LIST_SIZE,
                fillColor=self.GROUPS_LIST_COLOR,
                visible=True,
            )

    def updateMerzGroups(self, info):
        pass

    def updateGroups(self, info):
        c = self.getController()
        g = info['glyph']
        km = self.getKerningManager(g.font)
        group2 = km.glyphName2Group2.get(g.name, [])
        groupName2 = km.glyphName2GroupName2.get(g.name, '(No group)')
        group1 = km.glyphName2Group1.get(g.name, [])
        groupName1 = km.glyphName2GroupName1.get(g.name, '(No group)')
        
        x = -g.width * 1.5
        y = g.font.info.ascender
        self.groupsListLeftName.setText(groupName2)
        self.groupsListLeftName.setPosition((x, y))        
        self.groupsListLeft.setText('\n'.join(group2))
        self.groupsListLeft.setPosition((x, y - 3*self.GROUPS_LIST_NAME_SIZE))

        x = g.width * 2.5
        self.groupsListRightName.setText(groupName1)
        self.groupsListRightName.setPosition((x, y))        
        self.groupsListRight.setText('\n'.join(group1))
        self.groupsListRight.setPosition((x, y - 3*self.GROUPS_LIST_NAME_SIZE))
        return False

    def checkFixGroups(self, g):
        changed = False
        #changed |= self.checkFixComponentsExist(g)
        #changed |= self.checkFixComponentsPosition(g)
        return changed

    def buildGroups(self, y):
        #personalKey_c = self.registerKeyStroke('C', 'componentFixAllKey')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.showGroups = CheckBox((C0, y, CW, L), 'Show groups', value=True, sizeStyle='small')
        c.w.fixLeftGroup = Button((C1, y, CW, L), f'Fix left group', callback=self.fixLeftGroupCallback)
        c.w.fixRightGroup = Button((C2, y, CW, L), f'Fix right group', callback=self.fixRightGroupCallback)
        y += L + 10
        c.w.initializeGroups = Button((C2, y, CW, L), f'Init groups', callback=self.initializeGroupsCallback) # @@@ D A N G E R
        y += L + 10
        c.w.groupsEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.groupsEndLine2 = HorizontalLine((self.M, y, -self.M, 1))
        y += L/5

        return y

    def initializeGroupsCallback(self, sender):
        f = self.getCurrentFont()
        if f is not None:
            km = self.getKerningManager(f)
            km.initializeGroups()
            self.updateEditor

    def fixLeftGroupCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.fixLeftGroup(g)
            self.updateEditor

    def fixLeftGroup(self, g):
        """Check if the groups of gd.groupSrcUFOPath are consistent with what km.similar2(g) suggests.
        If not the same, then fix the group. Then make sure that the current font has the same
        definition of the group."""
        md = self.getMasterData(g.font)
        # First make sure that the gd.groupSrcUFOPath group is good.
        src = self.getFont(md.groupSrcUFOPath)
        assert src is not None
        srcG = src[g.name]

        # Get kerning manager of the source font
        km = self.getKerningManager(srcG.font)

        baseGroupGlyphName = km.getBaseGroupGlyphName2(g)
        print(baseGroupGlyphName)
        return 

        srcGroup2 = km.glyphName2Group2.get(srcG.name, [])
        srcGroupName2 = km.getSimilarBaseGroupName2(srcG)
        srcSimNames2 = sorted(km.getSimilarNames2(srcG))
        # Do not try to set the group directly, because it may need to be removed from other groups first.
        # The kerning manager can figure this out. The km.setGroup answers the flag if something changed.
        if km.setGroup2(src, srcGroupName2, srcSimNames2):
            src.changed()

        # Do not try to set the group directly, because it may need to be removed from other groups first.
        # The kerning manager can figure this out. The km.setGroup answers the flag if something changed.
        if km.setGroup2(g.font, srcGroupName2, srcSimNames2):
            src.changed()
    
    def fixRightGroupCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.fixRightGroup(g)
            self.updateEditor

    def fixRightGroup(self, g):
        """Check if the groups of gd.groupSrcUFOPath are consistent with what km.similar1(g) suggests.
        If not the same, then fix the group. Then make sure that the current font has the same
        definition of the group."""
        md = self.getMasterData(g.font)
        # First make sure that the gd.groupSrcUFOPath group is good.
        src = self.getFont(md.groupSrcUFOPath)
        assert src is not None
        srcG = src[g.name]

        # Get kerning manager of the source font
        km = self.getKerningManager(srcG.font)

        baseGroupGlyphName = km.getBaseGroupGlyphName1(g)
        print(baseGroupGlyphName)
        return 

        srcGroup1 = km.glyphName2Group1.get(srcG.name, [])
        srcGroupName1 = km.getSimilarBaseGroupName1(srcG)
        srcSimNames1 = sorted(km.getSimilarNames1(srcG))
        # Do not try to set the group directly, because it may need to be removed from other groups first.
        # The kerning manager can figure this out. The km.setGroup answers the flag if something changed.
        if km.setGroup1(src, srcGroupName1, srcSimNames1):
            src.changed()

        # Do not try to set the group directly, because it may need to be removed from other groups first.
        # The kerning manager can figure this out. The km.setGroup answers the flag if something changed.
        if km.setGroup1(g.font, srcGroupName1, srcSimNames1):
            src.changed()

