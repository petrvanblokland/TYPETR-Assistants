# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    groupeditor.py
#

import weakref
from vanilla import Window, EditText, Button, RadioGroup, List, TextBox, TextEditor
from tnbits.vanillas.listcell import SmallTextListCell, SmallRightAlignTextListCell
from tnbits.toolbox.fontparts.groups import GroupsTX

G = 8
M = G
W = 800
H = 700
MINH = 400
C = (W-2*M-3*G)/4
MIDDLE = 120
BOTTOM = -200
FIELD = 40

class GroupEditor(object):

    def getGroupNameDescriptor(self):
        return [
            dict(title="Name", key="name", cell=SmallTextListCell(editable=False), width=C-FIELD-G, editable=False),
            dict(title="Glyphs", key="glyphs", cell=SmallRightAlignTextListCell(editable=False), width=FIELD, editable=False),
        ]
    def getLeftMarginDescriptor(self):
        return [
            dict(title="Name", key="name", cell=SmallTextListCell(editable=False), width=C-FIELD-G, editable=False),
            dict(title="Left", key="value", cell=SmallRightAlignTextListCell(editable=False), width=FIELD, editable=False),
        ]
    def getRightMarginDescriptor(self):
        return [
            dict(title="Name", key="name", cell=SmallTextListCell(editable=True), width=C-FIELD-G, editable=True),
            dict(title="Right", key="value", cell=SmallRightAlignTextListCell(editable=False), width=FIELD, editable=False),
        ]

    def __init__(self, style, parent=None):

        self._style = style
        self.parent = parent

        y = M
        x = M

        self.w = w = Window((100, 200, W, H), self.getTitle(), minSize=(W, MINH), maxSize=(W, 2*H))
        w.center()

        w.group_ML_ListLabel = TextBox((M, y, C, 20), 'Group margin left', sizeStyle='small')
        w.group_ML_List = List((M, y+18, C, BOTTOM), [], selectionCallback=self.group_ML_ListSelectionCallback,
            enableDelete=False, columnDescriptions=self.getGroupNameDescriptor())

        w.glyph_ML_ListLabel = TextBox((M+C+G, y, C, 20), '<-- Glyphs Margin Left', sizeStyle='small')
        w.glyph_ML_List = List((M+C+G, y+18, C, BOTTOM), [], selectionCallback=self.glyph_ML_ListSelectionCallback,
            enableDelete=False, columnDescriptions=self.getLeftMarginDescriptor())

        w.group_MR_ListLabel = TextBox((M+2*(C+G), y, C, 20), 'Group Margin Right -->', sizeStyle='small')
        w.group_MR_List = List((M+2*(C+G), y+18, C, BOTTOM), [], selectionCallback=self.group_MR_ListSelectionCallback,
            enableDelete=False, editCallback=self.groupNamesListEditCallback,
            columnDescriptions=self.getGroupNameDescriptor())

        w.glyph_MR_ListLabel = TextBox((M+3*(C+G), y, C, 20), 'Glyphs Margin Right -->', sizeStyle='small')
        w.glyph_MR_List = List((M+3*(C+G), y+18, C, BOTTOM), [], selectionCallback=self.glyph_MR_ListSelectionCallback,
            enableDelete=False, columnDescriptions=self.getRightMarginDescriptor())

        y += BOTTOM

        w.deleteGroups_ML = Button((M, y, C, 20), 'Delete Group(s)', callback=self.deleteGroups_ML_Callback, sizeStyle='small')
        w.deleteGlyphs_ML = Button((M+C+G, y, C, 20), 'Delete Glyph(s)', callback=self.deleteGlyphs_ML_Callback, sizeStyle='small')

        w.deleteGroups_MR = Button((M+2*(C+G), y, C, 20), 'Delete Group(s)', callback=self.deleteGroups_MR_Callback, sizeStyle='small')
        w.deleteGlyphs_MR = Button((x+3*(C+G), y, C, 20), 'Delete Glyph(s)', callback=self.deleteGlyphs_MR_Callback, sizeStyle='small')

        y += 48
        w.groupName = EditText((x, y, W/2-G, 20), placeholder='New Group Name', continuous=True, callback=self.groupNameCallback, sizeStyle='small')
        w.glyphName = EditText((x+W/2, y, W/2-2*G, 20), placeholder='New Glyph Name', continuous=True, callback=self.glyphNameCallback, sizeStyle='small')

        y += 24
        w.makeNewGroup = Button((x, y, W/2-G, 20), 'Make new group', callback=self.makeNewGroupCallback, sizeStyle='small')
        w.addNewGlyph = Button((x+W/2, y, W/2-2*G, 20), 'Add new glyph', callback=self.addNewGlyphCallback, sizeStyle='small')
        w.cleanup = Button((x+W-G, y, W/2-2*G, 20), 'Clean up', callback=self.cleanupCallback, sizeStyle='small')

        y += 24
        w.reporter = TextEditor((x, y, -G, -G))
        # Created self._glyph2Groups dictionary. Key is glyphName, value is tuple [leftGroup, rightGroup]
        self.updateGlyph2Groups()
        self.updateGroupLists()

        self._updating = False

        self.updateButtons()
        self.w.open()

    def _get_parent(self):
        if self._parent is not None:
            if self._parent is None:
                return None
            return self._parent()
    def _set_parent(self, parent):
        if parent is None:
            self._parent = None
        else:
            self._parent = weakref.ref(parent)
    parent = property(_get_parent, _set_parent)

    def getTitle(self):
        return 'Groups | %s %s' % (self._style.info.familyName, self._style.info.styleName)

    def setStyle(self, style):
        self._style = style
        self.w.setTitle(self.getTitle())
        self.updateGlyph2Groups()
        self.updateGroupLists()
        self.updateGlyphList()
        self.updateButtons()

    def _getGroupName(self):
        return None

        if self.w.leftRightSelection.get():
            prefix = GroupsTX.KERN_PREFIX_L
        else:
            prefix = GroupsTX.KERN_PREFIX_R
        baseName = self.w.groupName.get()
        if baseName:
            return baseName
        return None

    # C A L L B A C K S

    def glyph_ML_ListSelectionCallback(self, sender):
        self.clearReport()
        self.updateGroup_ML_Lists()
        self.updateButtons()

    def glyph_MR_ListSelectionCallback(self, sender):
        self.clearReport()
        self.updateGroup_MR_Lists()
        self.updateButtons()

    # Delete groups

    def deleteGlyphs_ML_Callback(self, sender):
        self.clearReport()
        groupName = self._getSelectedGroup_ML_Name()
        if groupName in self._style.groups:
            group = set(self._style.groups[groupName])
            for selection in self.w.glyphNamesList.getSelection():
                glyphName = unDecorate(self.w.glyphNamesList[selection])
                if glyphName in group:
                    group.remove(glyphName)
                self.report('... Add glyph "%s" to group "%s' % (glyphName, groupName))
            self._style.groups[groupName] = sorted(group)
        self.updateGlyph2Groups()
        self.w.groupNamesList[self.w.groupNamesList.getSelection()[0]] =  '%s (%d)' % (groupName, len(group))
        self.updateGlyphList()
        self.updateButtons()
        self.notifyGroupChange()

    def deleteGlyphs_MR_Callback(self, sender):
        self.clearReport()
        groupName = self._getSelectedGroup_MR_Name()
        if groupName in self._style.groups:
            group = set(self._style.groups[groupName])
            for selection in self.w.glyphNamesList.getSelection():
                glyphName = unDecorate(self.w.glyphNamesList[selection])
                if glyphName in group:
                    group.remove(glyphName)
                self.report('... Add glyph "%s" to group "%s' % (glyphName, groupName))
            self._style.groups[groupName] = sorted(group)
        self.updateGlyph2Groups()
        self.w.groupNamesList[self.w.groupNamesList.getSelection()[0]] =  '%s (%d)' % (groupName, len(group))
        self.updateGlyphList()
        self.updateButtons()
        self.notifyGroupChange()

    def makeNewGroupCallback(self, sender):
        self.clearReport()
        groupName = self._getGroupName()
        if groupName is not None and not groupName in self._style.groups:
            self._style.groups[groupName] = []
            self.report('... Make new group "%s"' % groupName)
            self.updateGlyph2Groups()
            self.updateGroupLists()
            self.updateButtons()
            self.notifyGroupChange()

    def groupNamesListEditCallback(self, sender):
        self.clearReport()
        if self._updating:
            return
        selection = sender.getSelection()
        if selection:
            groupItems = self._getGroupItems() # Keep same order.
            newName = unDecorate(sender[selection[0]])
            if not newName in groupNames: # Make sure it does not exist
                oldName = unDecorate(groupNames[selection[0]]) # Must be the same index, undecorate
                if newName != oldName: # Rename the group.
                    self._style.groups[newName] = self._style.groups[oldName]
                    del self._style.groups[oldName]
                self.report('... Renamed group "%s" to group "%s' % (oldName, newName))
            self.updateGroupLists()
            self.updateButtons()

    def group_ML_ListSelectionCallback(self, sender):
        if self._updating:
            return
        self.clearReport()
        self.updateGlyph_ML_List()
        self.updateButtons()

    def group_MR_ListSelectionCallback(self, sender):
        if self._updating:
            return
        self.clearReport()
        self.updateGlyph_MR_List()
        self.updateButtons()

    def groupNameCallback(self, sender):
        self.updateButtons() # Update the status of the buttons

    def deleteGroups_ML_Callback(self, sender):
        self.clearReport()
        for selection in self.w.group_ML_List.getSelection():
            groupName = self.w.group_ML_List[selection]
            groupName = groupName.split(' ')[0] # Undecorate.
            if groupName in self._style.groups:
                del self._style.groups[groupName]
                self.report('... Deleted group "%s"' % groupName)
        self.updateGlyph2Groups()
        self.updateGroupLists()
        self.updateButtons()
        self.notifyGroupChange()

    def deleteGroups_MR_Callback(self, sender):
        self.clearReport()
        for selection in self.w.group_MR_List.getSelection():
            groupName = self.w.group_MR_List[selection]
            groupName = groupName.split(' ')[0] # Undecorate.
            if groupName in self._style.groups:
                del self._style.groups[groupName]
                self.report('... Deleted group "%s"' % groupName)
        self.updateGlyph2Groups()
        self.updateGroupLists()
        self.updateButtons()
        self.notifyGroupChange()


    def _getSelectedGroup_ML_Name(self):
        """Answer group name if there is a single selection. Otherwise answer
        None."""
        selection = self.w.group_ML_List.getSelection()
        if len(selection) == 1:
            return self.w.group_ML_List[selection[0]]['name']
        return None

    def _getSelectedGroup_MR_Name(self):
        """Answer group name if there is a single selection. Otherwise answer
        None."""
        selection = self.w.group_MR_List.getSelection()
        if len(selection) == 1:
            return self.w.group_MR_List[selection[0]]['name']
        return None

    def _getgroup_ML_Items(self):
        """Answer the sorted list of groups names, dependent on the left/right
        selection."""
        items = []
        for name in sorted(set(self._style.groups.keys())):
            if GroupsTX.isLeftKernGroup(name):
                items.append(dict(name=name, glyphs=str(len(self._style.groups[name]))))
        return items

    def _getgroup_MR_Items(self):
        """Answer the sorted list of groups names, dependent on the left/right
        selection."""
        items = []
        for name in sorted(set(self._style.groups.keys())):
            if GroupsTX.isRightKernGroup(name):
                items.append(dict(name=name, glyphs=str(len(self._style.groups[name]))))
        return items

    def glyphNameCallback(self, sender):
        self.updateButtons() # Check if there is non-existing valid glyph names

    def addNewGlyphCallback(self, sender):
        self.clearReport()
        groupName = self._getSelectedGroupName()
        if groupName is not None and groupName in self._style.groups:
            group = set(self._style.groups[groupName]) # Remove any duplicate glyph names.
            glyphNames = self.w.glyphName.get()
            for glyphName in glyphNames.replace('/', ' ').split(' '):
                if not glyphName:
                    continue
                group.add(glyphName)
                self.report('... Add glyph "%s" to group "%s"' % (glyphName, groupName))
            self._style.groups[groupName] = sorted(group)
            self.updateGlyph2Groups()
            self.w.groupNamesList[self.w.groupNamesList.getSelection()[0]] =  '%s (%d)' % (groupName, len(group))
            self.updateButtons()
            self.updateGlyphList()
            self.notifyGroupChange()

    def cleanupCallback(self, sender):
        """Clean up as much as possible."""
        for groupName, group in self._style.groups.items():
            # Remove all duplicates from the groups
            group = set(group)
            # Remove the glyhps that are not in the style.
            for glyphName in sorted(group):
                if not glyphName in self._style:
                    group.remove(glyphName)
            # Save the group as sorted list.
            self._style.groups[groupName] = sorted(group)
            self.updateGlyph2Groups()
            # If too many groups for a glyphName, then select the first one (may be wrong guess).
            for glyphName, groupSet in self._glyph2Groups.items():
                for gName in groupSet[0][1:]: # Clean left group, remove reference of all except first.
                    group = set(self._style.groups[gName])
                    if glyphName in group:
                        group.remove(glyphName)
                    self._style.groups[gName] = sorted(group)
                for gName in groupSet[1][1:]: # Clean right group, remove reference of all except first.
                    group = set(self._style.groups[gName])
                    if glyphName in group:
                        group.remove(glyphName)
                    self._style.groups[gName] = sorted(group)

        self.clearReport()
        self.updateGlyph2Groups()
        self.updateGroupLists()
        self.updateGlyphList()
        self.updateButtons()
        self.notifyGroupChange()

    # N O T I F I C A T I O N S

    # TODO: Notify parent if window is closing.

    def notifyGroupChange(self):
        """Set notification to parent, if weakref is not None."""
        parent = self.parent
        if parent is not None:
            parent.notifyGroupChange()

    def event(self, event):
        """Handle the event from the TextCenter, as defined in Constants."""
        #CHAR_CREATERIGHT = '1' # Create a new right group with the current glyph
        #CHAR_ADDRIGHT = '2' # Add the cyurent glyph to the right space group
        #CHAR_REMOVERIGHT = '3' # Remove the current glyph from the right space group
        #CHAR_CREATELEFT = '5' # Create a new left group with the current glyph
        #CHAR_ADDLEFT = '6' # Add the cyrrent glyph to the left space group
        #CHAR_REMOVELEFT = '7' # Remove the current glyph from the left space group
        eventType = event['type']
        glyphName = event['glyphName']
        if eventType == C.CHAR_CREATELEFT:
            print('Create left for', glyphName)
        elif eventType == C.CHAR_ADDLEFT:
            print('Add left', glyphName)
        elif eventType == C.CHAR_REMOVELEFT:
            print('Remove left', glyphName)
        elif eventType == C.CHAR_CREATERIGHT:
            print('Create left', glyphName)
        elif eventType == C.CHAR_ADDLEFT:
            print('Add left', glyphName)
        elif eventType == C.CHAR_REMOVELEFT:
            print('Remove left', glyphName)

    # U P D A T I N G

    def clearReport(self):
        self.w.reporter.set('')

    def report(self, reports):
        if reports:
            if isinstance(reports, (list, tuple)):
                reports = '\n'.join(reports)
            t = self.w.reporter.get()  + '\n' + reports
            self.w.reporter.set(t)

    def updateButtons(self):
        groupName = self._getGroupName()
        if groupName is not None and not groupName in self._style.groups:
            self.w.makeNewGroup.enable(True)
            self.w.makeNewGroup.setTitle('Make group ' + groupName)
        else:
            self.w.makeNewGroup.enable(False)
            self.w.makeNewGroup.setTitle('Make group')

        # Enable delete buttons
        groupSelection = self.w.group_ML_List.getSelection()
        self.w.deleteGroups_ML.enable(len(groupSelection))
        if len(groupSelection) > 1:
            label = 'Delete groups'
        else:
            label = 'Delete group'
        self.w.deleteGroups_ML.setTitle(label)

        groupSelection = self.w.group_MR_List.getSelection()
        self.w.deleteGroups_MR.enable(len(groupSelection))
        if len(groupSelection) > 1:
            label = 'Delete groups'
        else:
            label = 'Delete group'
        self.w.deleteGroups_MR.setTitle(label)

        glyphSelection = self.w.glyph_ML_List.getSelection()
        self.w.deleteGlyphs_ML.enable(len(glyphSelection))
        if len(glyphSelection) > 1:
            label = 'Delete glyphs'
        else:
            label = 'Delete glyph'
        self.w.deleteGlyphs_ML.setTitle(label)

        glyphSelection = self.w.glyph_MR_List.getSelection()
        self.w.deleteGlyphs_MR.enable(len(glyphSelection))
        if len(glyphSelection) > 1:
            label = 'Delete glyphs'
        else:
            label = 'Delete glyph'
        self.w.deleteGlyphs_MR.setTitle(label)

        """
        self.w.glyphNamesListLabel.enable(len(groupSelection) == 1)
        self.w.glyphNamesList.enable(len(groupSelection) == 1)


        selectedGroupName = self._getSelectedGroupName()
        self.w.glyphName.enable(selectedGroupName is not None)

        # Check on valid glyph input. Otherwise disable button.
        isValid = True
        groupName = self._getSelectedGroupName()
        if groupName is not None and groupName in self._style.groups:
            group = set(self._style.groups[groupName]) # Remove any duplicate glyph names.
            glyphNames = self.w.glyphName.get()
            for glyphName in glyphNames.replace('/', ' ').split(' '):
                if glyphName in group: # Already exist, disable the button
                    isValid = False
                    break
        self.w.addNewGlyph.enable(selectedGroupName is not None and isValid)
        """

    def updateGlyph2Groups(self):
        """Create glyph2Groups dictionary."""
        reports = []
        self._glyph2Groups_ML = d_ML = {}
        self._glyph2Groups_MR = d_MR = {}
        for groupName, group in self._style.groups.items():
            for glyphName in group:
                if GroupsTX.isLeftKernGroup(groupName):
                    if not glyphName in d_ML:
                        d_ML[glyphName] = []
                    d_ML[glyphName].append(groupName)
                    if len(d_ML[glyphName][0]) > 1:
                        reports.append('### Error glyph "%s" in multiple left groups %s' % (glyphName, d_ML[glyphName]))
                elif GroupsTX.isRightKernGroup(groupName):
                    if not glyphName in d_MR:
                        d_MR[glyphName] = []
                    d_MR[glyphName].append(groupName)
                    if len(d_MR[glyphName][0]) > 1:
                        reports.append('### Error glyph "%s" in multiple right groups %s' % (glyphName, d_MR[glyphName]))

        self.report(reports)

    def updateGroupLists(self):
        self.updateGroup_ML_Lists()
        self.updateGroup_MR_Lists()

    def updateGroup_ML_Lists(self):
        self._updating = True
        group_ML_Items = self._getgroup_ML_Items()
        self.w.group_ML_ListLabel.set('<-- Groups Margin Left (%s)' % len(group_ML_Items))
        self.w.group_ML_List.set(group_ML_Items) # Make decorated set
        self._updating = False

    def updateGroup_MR_Lists(self):
        self._updating = True
        group_MR_Items = self._getgroup_MR_Items()
        self.w.group_MR_ListLabel.set('Groups Margin Right (%s) -->' % len(group_MR_Items))
        self.w.group_MR_List.set(group_MR_Items) # Make decorated set
        self._updating = False

    def updateGlyph_ML_List(self):
        self._updating = True
        glyphItems = []
        groupName = self._getSelectedGroup_ML_Name()
        if groupName is not None:
            if groupName in self._style.groups:
                group = self._style.groups[groupName]
                for glyphName in group:
                    if not glyphName in self._style:
                        self.report('### Glyph "%s" does not exist in the style' % glyphName)
                        glyphItems.append(dict(name='(%s)' % glyphName, value='', glyphName=glyphName))
                        continue

                    if GroupsTX.isLeftKernGroup(groupName):
                        margin = str(int(self._style[glyphName].leftMargin))
                    else:
                        margin = ''
                    glyphItems.append(dict(name=glyphName, value=margin))

        self.w.glyph_ML_List.set(glyphItems)

    def updateGlyph_MR_List(self):
        self._updating = True
        glyphItems = []
        groupName = self._getSelectedGroup_MR_Name()
        if groupName is not None:
            if groupName in self._style.groups:
                group = self._style.groups[groupName]
                for glyphName in group:
                    if not glyphName in self._style:
                        self.report('### Glyph "%s" does not exist in the style' % glyphName)
                        glyphItems.append(dict(name='(%s)' % glyphName, value='', glyphName=glyphName))
                        continue

                    if GroupsTX.isRightKernGroup(groupName):
                        margin = str(int(self._style[glyphName].rightMargin))
                    else:
                        margin = ''
                    glyphItems.append(dict(name=glyphName, value=margin))

        self.w.glyph_MR_List.set(glyphItems)

# ----------------------------------------------------------------------------------
if __file__ == '__main__':
    f = CurrentFont()
    if f is not None:
        GroupEditor(f)
