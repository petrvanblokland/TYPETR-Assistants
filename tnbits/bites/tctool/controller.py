# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    controller.py
#

import AppKit
import math
import traceback
from vanilla import TextEditor, Group, EditText, SplitView
from fontParts.world import RFont
from tnbits.base.constants.tool import *
from tnbits.base.controller import BaseController
from tnbits.base.handler import BitsHandler
from tnbits.base.scroll import ScrollGroup
from tnbits.base.toolbar import Toolbar
from tnbits.base.tools import (openTool, addLogger, getLog, showOutputWindow,
        setLog)
from tnbits.base.groups import (getMargin, getGroupBaseGlyphName,
        getSpaceOrKerningGroupNames, fixKerningGroups, setExtWidths)
from tnbits.bites.tctool.constants import *
from tnbits.bites.tctool.dialogs.savedialog import SaveDialog
from tnbits.bites.tctool.dialogs.adddialog import AddDialog
from tnbits.bites.tctool.dialogs.designspacedialog import DesignSpaceDialog
from tnbits.bites.tctool.groupswindow import GroupsWindow
from tnbits.bites.tctool.preferencemodel import preferenceModel
from tnbits.bites.tctool.side import Side
from tnbits.bites.tctool.typesetter import Typesetter
from tnbits.bites.tctool.textitem import TextItem
from tnbits.base.groups import (getSpaceOrKerningGroupNames, getKernGroupNames,
        makeRomanGroups)
from tnbits.model import model
from tnbits.model.objects.xgroups import XGroups
from tnbits.model.objects.style import isItalic
from tnbits.model.toolbox.kerning.groupkerning import (exportGroupsScript,
        exportKerningScript)
from tnbits.spreadsheet.cell import Cell
from tnbits.toolbox.transformer import TX

class Controller(BaseController):
    """Implements internal logic between various parts of the TC tool.

    TODO: implement features.
    TODO: variable (& compatible groups...)
    TODO: variable designspace interface
    TODO: stepY?
    TODO: unit testing
    TODO: proof like templates (overlay, styles per line)
    TODO: Exclude filtered glyph names, certain extensions.
    """

    def __init__(self, tool, mode='tool'):
        super(Controller, self).__init__(tool, mode)
        self._groupEditor = None
        self._selectedTextItem = None
        self._selectedLeftGroupName = None
        self._selectedRightGroupName = None
        self._selectedLeftGroup = None
        self._selectedRightGroup = None
        self._leftMismatches = []
        self._rightMismatches = []

        # TODO: margin caching.
        self._currentGroupMarginValues = {}

        # Values derived from self.style:
        self._textScale = None
        self._descender = None
        self._ascender = None
        self._tangent = None
        self._upem = None

        # - Dictionary of cache feature compilers. Key is style.path, value is
        # FeatureCompiler.
        # FIXME
        # - Dictionary of feature viewers. Key is style.path, value is
        # OpenTypeControlsView.
        # FIXME
        self._featureCompilers = {}
        self._featureViewers = {}
        self.xgroups = {}
        self._recentPages = {}

        # Start up the tool with default values. This is before the family is
        # loaded.
        for k, v in preferenceModel.items():
            default = v['default']
            setattr(self, k, default)

        self.build()

    def build(self):
        self.toolbar = Toolbar(self, items=self.getToolbarItems())

        # Side.
        self.side = Side(self)
        nsview = self.side.getNSView()
        self.tool.set('side', ScrollGroup(nsview, (0, 0, SIDE, -0)))

        # Top.
        top =  Group((0, 0, -0, -0))
        TW = 100
        self.startControlGlyphs = EditText((0, 0, TW, -0), '',
                sizeStyle='small', callback=self.startGlyphsCallback,
                continuous=False)

        # FIXME: load from preferences.
        self.rawText = TextEditor((TW, 0, -TW, -0), SAMPLES[0],
                callback=self.rawTextCallback)

        self.endControlGlyphs = EditText((-TW, 0, 0, -0), '',
                sizeStyle='small', continuous=False,
                callback=self.endGlyphsCallback)

        top.startControlGlyphs = self.startControlGlyphs
        top.rawText = self.rawText
        top.endControlGlyphs = self.endControlGlyphs

        # Typesetter.
        self.typesetter = Typesetter(self)

        # Split views.
        pane0 = dict(identifier="top", view=top, size=150)
        pane1 = dict(identifier="typesetter", view=self.typesetter.getView())
        splitView = SplitView((SIDE, 0, -0, -0), [pane0, pane1], isVertical=False)
        self.tool.set('splitView', splitView)

        # Groups.
        self.groupsWindow = GroupsWindow(self)
        self.groupsWindow.open()

    # Groups.

    def setGroups(self):
        """Make sure that the x-ref xGroups are initialized for this style. If
        force is True, then always recalculate the x-ref dictionary.

        TODO: update when groups have been edited in RoboFont.
        """
        if self.style.path in self.xgroups:
            return

        xgroups = XGroups(self.style)
        self.xgroups[self.style.path] = xgroups

    def clearGroups(self, style):
        if style and style.path in self.xgroups:
            del self.xgroups[style.path]

    # Get.

    def getMargins(self, glyphName, related=False):
        """Finds metric for this glyph to show the values, and also to
        determine the minimal size of the label area in order to make all
        buttons fit.

        TODO: use angled margins for italic styles.

        """
        if related:
            style = self.relatedStyle
        else:
            style = self.style


        italic = isItalic(self.styleKey)
        glyph = style[glyphName]
        w = glyph.width
        leftMargin = getMargin(glyph, LEFT, italic=italic)
        rightMargin = getMargin(glyph, RIGHT, italic=italic)
        return leftMargin, rightMargin, w

    def getToolbarItems(self):
        items = [
            {"itemIdentifier": "showGroups",
             "label": "Groups",
             "imagePath": None,
             "imageNamed": "toolbarGroups",
             "callback": self.showGroupsWindow},
            {"itemIdentifier": "showLog",
             "label": "Log",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameBookmarksTemplate,
             "callback": self.showLogCallback},
            {"itemIdentifier": "showOutput",
             "label": "Output",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameBookmarksTemplate,
             "callback": self.showOutputCallback},
            {"itemIdentifier": "previousPage",
             "label": "Previous",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameGoLeftTemplate,
             "callback": self.previousPageCallback},
            {"itemIdentifier": "nextPage",
             "label": "Next",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameGoRightTemplate,
             "callback": self.nextPageCallback},
            {"itemIdentifier": "search",
             "label": "Search",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameRevealFreestandingTemplate,
             "callback": self.searchCallback},
            {"itemIdentifier": "refresh",
             "label": "Refresh",
             "imagePath": None,
             "imageNamed": AppKit.NSImageNameRefreshFreestandingTemplate,
             "callback": self.refreshCallback},
        ]

        return items

    def getRecentPage(self, i):
        if i in self._recentPages:
            return self._recentPages[i]
        return 0

    def getLastPage(self):
        return self.typesetter.getNumberOfPages() - 1

    def getSelected(self):
        return self.typesetter.cache.getSelectedItem()

    def getEditMode(self):
        return self._editMode

    def getSelectedGroup(self, left=True):
        if left:
            return self._selectedLeftGroup
        else:
            return self._selectedRightGroup

    def getSelectedGroupName(self, left=True):
        if left:
            return self._selectedLeftGroupName
        else:
            return self._selectedRightGroupName

    def getGroups(self):
        if self.style.path in self.xgroups:
            return self.xgroups[self.style.path]
        return None

    # Set.

    def setStyle(self, styleKey):
        self.reset()
        self.style = self.getStyle(styleKey)
        self.styleKey = styleKey
        self.setGroups()
        self.relatedStyle = self.getRelatedStyle()
        self.setSample(self._sample, page=self._page)
        name = self.styleKey[-1]
        self.tool.setTitle(styleName=name)
        self.groupsWindow.setTitle(name)

    def getRelatedStyle(self):
        return self.family.getRelatedStyle(self.style)

    def setTabWidths(self):
        setExtWidths(self.style, self._tabWidth, 'tab')
        self.update()

    def setFwidWidths(self):
        fwid = self.getUpem()
        setExtWidths(self.style, fwid, 'fwid')
        self.update()

    def setHwidWidths(self):
        hwid = int(self.getUpem() / 2)
        setExtWidths(self.style, hwid, 'hwid')
        self.update()

    def setCmbWidths(self):
        setExtWidths(self.style, 0, 'cmb')
        self.update()

    def setSelected(self, textItem):
        if not textItem.missing:
            self.setSelectedGroups()

    def setEditMode(self, editMode):
        self.controller._editMode = editMode
        self.setSelectedGroups()

    def setSelectedGroups(self):
        selectedTextItem = self.getSelected()

        if not selectedTextItem:
            return

        if self.isSpacing():
            glyphName = selectedTextItem.name
            groups = self.getGroups()
            l, r = getSpaceOrKerningGroupNames(self.style, glyphName, groups)
        else:
            glyphName = selectedTextItem.name
            previousItem = self.typesetter.cache.getPrevious(textItem=selectedTextItem)
            prevName = selectedTextItem.name
            groups = self.getGroups()
            l, _ = getKernGroupNames(self.style, glyphName, groups)
            _, r = getKernGroupNames(self.style, prevName, groups)

        if l and l in self.style.groups:
            self._selectedLeftGroupName = l
            self._selectedLeftGroup = self.style.groups[l]
        if r and r in self.style.groups:
            self._selectedRightGroupName = r
            self._selectedRightGroup = self.style.groups[r]

        self.compareSelectedGroupMargins()

    def setGroupGlyphs(self, groupName, glyphNames):
        glyphNames = list(set(glyphNames))
        glyphNames.sort()

        if None in glyphNames:
            glyphNames.remove(None)

        for glyphName in glyphNames:
            if not glyphName in self.style.keys():
                self.logger.warning('glyph name %s not in style' % glyphName)

        self.style.groups[groupName] = glyphNames
        self.clearGroups(self.style)
        self.setGroups()
        self.setGroupsInfo()
        self.typesetter.update()
        return glyphNames

    def setFamily(self, family):
        """Initializes selected family at startup based on folder contents."""
        self.family = family
        self.setPreferences()
        styleKey = model.getSelectedStyleKey()
        self.setStyle(styleKey)
        # TODO: change to names later.
        self.setDesignSpace(ANY)
        self.updateSide()
        self.update()

    def setStyleByID(self, styleID):
        styleKeys = list(self.family.getStyleKeys())

        for styleKey in styleKeys:
            if styleKey[1] == styleID:
                self.setStyle(styleKey)

    def getStyleIDs(self):
        assert self.family
        return self.family.getStyleIDs()

    def setSample(self, sampleIndex, page=0):
        """Sets all sample related values after a selection from side."""
        self.typesetter.setSample(sampleIndex, update=False)
        self.typesetter.setPage(page, update=False)
        self._sample = sampleIndex

        '''
        last = self.getLastPage()

        if page > last:
            page = last

        '''
        self._page = page
        self.tool.setPreference('_sample', sampleIndex)
        self.tool.setPreference('_page', page)
        text = self.typesetter.getUIText()
        self.setText(text)
        self.typesetter.update()
        self._recentPages[sampleIndex] = page
        return page

    def setPage(self, i):
        self.typesetter.setPage(i)
        last = self.getLastPage()

        if i > last:
            i = last

        self.tool.setPreference('_page', i)
        text = self.typesetter.getUIText()
        self.setText(text)
        self._recentPages[self._sample] = i

    def setText(self, text):
        self.rawText.set(text)

    def setSpreadsheetText(self, text):
        self.setText(text)
        self.typesetter.setPages(text)
        self.typesetter.update()

    def resetGlyph(self):
        if not self.glyph is None:
            #self.glyph.removeObserver(self, "_glyphChangedTC")
            self.glyph = None

    def setGlyph(self, glyph):
        # FIXME: naming conflict with mojo GlyphPreview.
        self.resetGlyph()
        #glyph.addObserver(self, "_glyphChangedTC", "Glyph.Changed")
        self.glyph = glyph

    def setChanged(self, changedGlyphs):

        if self._steps == self._numSteps:
            if isinstance(self.style, RFont):
                for glyphName in changedGlyphs:
                    try:
                        glyph = self.style[name]
                        glyph.changed()
                    except:
                        self.logger.warning('Cannot find %s' % glyphName)

            self._steps = 0

        else:
            self._steps += 1

    def setGroupsInfo(self):
        textItem = self.getSelected()

        if not textItem:
            return

        if self.style and textItem and textItem.name and textItem.name in self.style:
            msg1 = ''
            msg2 = ''
            msg3 = ''

            if self._editMode == EDIT_MODES[KERNING]:
                msg1 = 'Groups: %d' % len(self.style.groups)
                msg2 = 'Kernings: %d' % len(self.style.kerning)
                previousItem = self.typesetter.cache.getPrevious(textItem=textItem)
                msg3 = '%s --> %d <-- %s' % (previousItem.name, textItem.kerning, textItem.name)
            elif self._editMode == EDIT_MODES[SPACING]:
                glyph = self.style[textItem.name]
                left = str(getMargin(glyph, LEFT))
                right = str(getMargin(glyph, RIGHT))
                msg1 = 'Groups: %d' % len(self.style.groups)
                msg2 = 'Kernings: %d' % len(self.style.kerning)
                msg3 = '%s <-- %s --> %s' % (left, textItem.name, right)

            self.groupsWindow.setInfo(msg1, msg2, msg3)

        data = self.getData(textItem)
        spreadsheetView = self.groupsWindow.getSpreadsheetView()
        spreadsheetView.setData(data)

    def _glyphChangedTC(self, notification):
        self.logger.info('%s changed' % self.glyph.name)

    # Show.

    def showGroupsWindow(self, sender):
        self.groupsWindow.show()

    def showLogCallback(self, sender):
        log = getLog()
        log.show()

    def showOutputCallback(self, sender):
        showOutputWindow()

    # Previous / next.

    def previousPageCallback(self, sender):
        self.previousPage()

    def previousPage(self):
        i = self.typesetter.getPageNumber()
        last = self.getLastPage()

        if i == 0:
            j = last
        else:
            j = i - 1

        if i != j:
            self.side.view.selectPage.set(j)
            self.setSample(self._sample, j)

    def nextPageCallback(self, sender):
        self.nextPage()

    def nextPage(self):
        i = self.typesetter.getPageNumber()
        last = self.getLastPage()

        if i == last:
            j = 0
        else:
            j = i + 1

        if i != j:
            self.setSample(self._sample, j)
            self.side.view.selectPage.set(j)

    # Reset.

    def reset(self):
        self._selectedTextItem = None
        self._selectedLeftGroupName = None
        self._selectedRightGroupName = None
        self._selectedLeftGroup = None
        self._selectedRightGroup = None
        self._leftMismatches = []
        self._rightMismatches = []
        self._currentGroupMarginValues = {}
        self._textScale = None
        self._descender = None
        self._tangent = None
        self._upem = None
        self.style = None
        self.styleKey = None
        self.resetGlyph()

    # Compare; TODO: move to QA.

    def compareSelectedGroupMargins(self):
        if not self._compareGroupMargins:
            self._leftMismatches = []
            self._rightMismatches = []
            return

        if self._selectedLeftGroup:
            self._leftMismatches = self.compareMargins()

        if self._selectedRightGroup:
            self._rightMismatches = self.compareMargins(left=False)

    def compareMargins(self, left=True):
        groupName = self.getSelectedGroupName(left=left)
        group = self.getSelectedGroup(left=left)
        baseName = getGroupBaseGlyphName(groupName)
        mismatches = []

        if baseName in self.style:
            baseGlyph = self.style[baseName]

            if left:
                margin = getMargin(baseGlyph, LEFT)
            else:
                margin = getMargin(baseGlyph, RIGHT)

            for glyphName in group:
                #if not glyphName in self._currentGroupMarginValues:
                #self._currentGroupMarginValues[groupName] = {}
                if not glyphName in self.style:
                    continue

                glyph = self.style[glyphName]

                if left:
                    value = getMargin(glyph, LEFT)
                else:
                    value = getMargin(glyph, RIGHT)

                if value != margin:
                    mismatches.append(glyphName)

            if len(mismatches) > 0:
                mismatches.append(baseName)

        return mismatches

    # Boolean.

    def isSpacing(self):
        return self.getEditMode() == EDIT_MODES[SPACING]

    def isKerning(self):
        return self.getEditMode() == EDIT_MODES[KERNING]

    def hasOverlayRelated(self):
        if self._overlayRelated and self.relatedStyle:
            return True

        return False

    def exists(self, glyphName):
        try:
            if glyphName in self.style:
                return True
            return False
        except:
            print(traceback.format_exc())
            return False

    # Groups.

    def removeGlyphFromGroup(self, groupName, glyphName):
        if groupName and glyphName:
            glyphNames = removeGlyphFromGroup(groupName, glyphName, self.style)
            self.setGroupGlyphs(groupName, glyphNames)

    def addToGroup(self, glyphName):
        # See issue #641.
        mode = self.getEditMode()
        # TODO: open dialog.

    def newGroup(self):
        # See issue #641.
        mode = self.getEditMode()
        # TODO: open dialog.

    def defaultGroups(self):
        # TODO: roman vs. italic.
        makeRomanGroups(self.style)
        self.clearGroups(self.style)
        self.setGroups()
        self.setGroupsInfo()

    def fixGroups(self):
        # See issue #639, #588.
        # TODO: open dialog.
        mode = self.getEditMode()

        if self.isSpacing():
            self.logger.info('Fixing spacing groups...')
            fixed = fixSpacingGroups(self.style)
            for f in fixed:
                msg = 'glyph ‘%s’ not in group %s' % f
                self.logger.warning(msg)
        elif self.isKerning():
            self.logger.info('Fixing kerning groups...')
            fixKerningGroups(self.style)
        self.setGroups()
        self.setGroupsInfo()
        setLog()

    # Dialogs.

    def openAddDialog(self, groupName):
        dialog = AddDialog(self, groupName, self.confirmAdd)
        self.tool.addDialog('add', dialog)

    def confirmAdd(self, groupName, glyphName):
        self.tool.removeDialog('add')

        if groupName and glyphName:
            glyphNames = self.style.groups[groupName]
            glyphNames.append(glyphName)
            self.setGroupGlyphs(groupName, glyphNames)

    # UI.

    def close(self):
        if self.family.isDirty():
            # TODO: open save dialog.
            pass
        if self.groupsWindow:
            self.groupsWindow.close()

    # Callbacks.

    def searchCallback(self, sender):
        # TODO: toggle on / off.
        self.typesetter.openSearchBox()

    def refreshCallback(self, sender):
        self.setSample(self._sample, self.typesetter.pageIndex)

    def proofCallback(self, sender):
        from tnbits.bites.proof.tool import ProofTool
        openTool(ProofTool, self.family)

    def qualityAssuranceCallback(self, sender):
        from tnbits.bites.qatool.tool import QualityAssuranceTool
        openTool(QualityAssuranceTool, self.family)

    def openFamilyCallback(self, sender):
        self.openFamily()

    def editStyleCallback(self, sender):
        # TODO: Ask to save before opening, else TC changes will be reverted.
        self.editStyle()
        setLog()

    def editGlyphCallback(self, sender):
        if IN_ROBOFONT is False:
            return

        selectedTextItem = self.getSelected()

        if not selectedTextItem:
            return

        if isinstance(self.selectedTextItem, TextItem):
            glyphName = self.selectedTextItem.name
            self.editGlyph(glyphName)

    def startGlyphsCallback(self, sender):
        """Updates the control glyphs."""
        tStart = sender.get()
        self.typesetter.updateStartGlyphs(tStart)

    def endGlyphsCallback(self, sender):
        """Updates the control glyphs."""
        tEnd = sender.get()
        self.typesetter.updateEndGlyphs(tEnd)

    def closeFamilyCallback(self, sender):
        self.closeFamily()

    def closeFamily(self):
        self.reset()
        model.closeFamily(self.family)
        self.family = None
        self.clearGroups(self.style)
        self.typesetter.reset()
        self.update()

    def rawTextCallback(self, sender):
        """Callback for the raw text input field. Expands the features of the
        raw text into the display text. Split the text into pages if too
        long."""
        text = sender.get()
        self.typesetter.updatePage(text)

    def openFamilyCallback(self, sender):
        self.openFamily()

    def setPreferences(self):
        """Initializes preferences variables for a family."""
        # TODO: remove parameter name underscores, add them during setattr().

        for key, v in preferenceModel.items():
            default = v['default']
            value = self.tool.getDefaultPreference(self, key, default=default)

            setattr(self, key, value)

    def viewDidChangeGlyph(self, glyph):
        self.setGlyph(glyph)

    # Groups sheet.

    def getData(self, textItem):
        style = self.style

        if style is None or textItem is None:
            return (DEFAULT_KERN1, DEFAULT_KERN2, [])

        if self._editMode == EDIT_MODES[KERNING]:
            return self.getKernData(style, textItem)
        elif self._editMode == EDIT_MODES[SPACING]:
            return self.getSpacingData(style, textItem)

    def getKernData(self, style, textItem):
        groups = self.getGroups()
        previousItem = self.typesetter.cache.getPrevious(textItem=textItem)
        l, _ = getKernGroupNames(style, previousItem.name, groups)
        _, r = getKernGroupNames(style, textItem.name, groups)
        return self.getGroupData(style, l, r)

    def getSpacingData(self, style, textItem):
        groups = self.getGroups()
        l, r = getSpaceOrKerningGroupNames(style, textItem.name, groups)
        return self.getGroupData(style, l, r)

    def getGroupData(self, style, groupNameML, groupNameMR):
        data = []
        y = 0
        title1 = 'No group'
        title2 = 'No group'
        sortedGroupNamesML = []
        sortedGroupNamesMR = []

        # Remove any duplicates from the list and reorder.
        # Fill the lists with new items, reversed because spacing is
        # mirrorred to kerning.

        if groupNameML is not None and groupNameML in style.groups:
            title1 = groupNameML
            sortedGroupNamesML = sorted(set(style.groups[groupNameML]))

        if groupNameMR is not None and groupNameMR in style.groups:
            title2 = groupNameMR
            sortedGroupNamesMR = sorted(set(style.groups[groupNameMR]))


        ll = len(sortedGroupNamesML)
        lr = len(sortedGroupNamesMR)

        l = max(ll, lr)

        for i in range(l):
            x = 0
            msg = ''
            if i < ll:
                msg = sortedGroupNamesML[i]

            cell = Cell(identifier=(x, y), value=msg)
            row = [cell]
            x = 1
            msg = ''

            if i < lr:
                msg = sortedGroupNamesMR[i]

            cell = Cell(identifier=(x, y), value=msg)
            row.append(cell)
            data.append(row)
            y += 1

        return (title1, title2, data)

    def openCallback(self, cell):
        styleKey = self.getStyleKey(cell)
        self.getController().openStyle([styleKey])

    # Family & style.

    def getPageNames(self):
        return self.typesetter.getPageNames()

    def updatePageNames(self):
        self.side.updatePageNames()

    def save(self):
        if self.style:
            rFont = self.getRFont(self.style.path)

            if rFont:
                rFont.save()
                self.logger.info('Saved RFont %s' % rFont.path)
            else:
                self.style.save()
                self.logger.info('Saved Style %s' % self.style.path)

            setLog()

    def addToDesignSpace(self):
        dialog = DesignSpaceDialog(self, self.confirmAddToDesignSpace)
        self.tool.addDialog('designSpace', dialog)

    def removeFromDesignSpace(self):
        dialog = DesignSpaceDialog(self, self.confirmRemoveFromDesignSpace)
        self.tool.addDialog('designSpace', dialog)

    def confirmAddToDesignSpace(self, name):
        self.tool.removeDialog('designSpace')

    def confirmRemoveFromDesignSpace(self, name):
        self.tool.removeDialog('designSpace')

    # Scale.

    def getPpem(self):
        """Pixels per Em as set by the text entry."""
        return self._ppem

    def getUpem(self):
        """Units per Em derived from the style."""
        # TODO: make property
        if self.style is not None and not self._upem:
            # Needs initialization.
            self._upem = self.style.info.unitsPerEm

        return self._upem

    def getTangent(self):
        """Angle derived from the style."""
        if self.style is not None and not self._tangent:
            if self.style.info.italicAngle:
                self._tangent = math.tan(-self.style.info.italicAngle * math.pi / 180)
            else:
                self._tangent = 0

        return self._tangent

    def getDescender(self):
        """Descender derived from the style."""
        # TODO: make property
        # TODO: QA -- make sure asc + desc == upem.
        if self.style is not None and not self._descender:
            # Needs initialization.
            self._descender = self.style.info.descender

        return self._descender

    def getAscender(self):
        """Descender derived from the style."""
        # TODO: make property
        # TODO: QA -- make sure asc + desc == upem.
        if self.style is not None and not self._ascender:
            # Needs initialization.
            self._ascender = self.style.info.ascender

        return self._ascender

    def getLineHeight(self):
        """Maximum height (i.e. Em size) of font multiplied by leading."""
        return self.getUpem() * self.getLeading()

    def setTextScale(self, ppem):
        """Sets the scale factor to the ppem value. The scaling depends on the
        unitsPerEm of the selected style."""
        if self.style is not None:
            ppem = int(ppem)
            ppem = min(PPEM_MAX, (ppem or PPEM_DEFAULT))
            ppem = max(PPEM_MIN, ppem)
            self._ppem = ppem
            self.tool.setPreference('_ppem', self._ppem)
            self._textScale = self._ppem / self.getUpem()

            # Resets the cached labels because their size compensates the
            # drawing scale.
            self.typesetter.resetLabels()
            self.update()

    def getTextScale(self):
        """Pixels per Em divided by units per Em."""
        # TODO: make property
        if self.style is not None and not self._textScale:
            # Needs initialization.
            ppem = self.getPpem()
            self.setTextScale(ppem)

        return self._textScale

    # Leading.

    def setLeading(self, leading):
        """Converts leading percentage to a decimal float number;

            100% == 1.0

        TODO: typesetter doesn't need to reflow text, just adjust height.
        """
        self._leading = TX.asFloat(leading, 100) / 100
        self.tool.setPreference('_leading', self._leading)
        self.update()

    def getLeading(self):
        return self._leading

    # Edit Mode.

    def setEditMode(self, editMode):
        self._editMode = editMode
        self.tool.setPreference('_editMode', self._editMode)
        self.update()

    def setColorScheme(self, colorScheme):
        self._colorScheme = colorScheme
        self.tool.setPreference('_colorScheme', self._colorScheme)
        self.typesetter.kit.resetStrings()
        self.typesetter.update()

    def getColorScheme(self):
        return COLORSCHEMES[self._colorScheme]

    # Flags.

    def setShowKerning(self, showKerning):
        self._showKerning = showKerning
        self.tool.setPreference('_showKerning', self._showKerning)
        self.update()

    def setShowMarkers(self, showMarkers):
        self._showMarkers = showMarkers
        self.tool.setPreference('_showMarkers', self._showMarkers)
        self.update()

    def setShowMissingGlyphs(self, showMissingGlyphs):
        self._showMissingGlyphs = showMissingGlyphs
        self.tool.setPreference('_showMissingGlyphs', self._showMissingGlyphs)
        self.update()

    def setShowEmptyGlyphs(self, showEmptyGlyphs):
        self._showEmptyGlyphs = showEmptyGlyphs
        self.tool.setPreference('_showEmptyGlyphs', self._showEmptyGlyphs)
        self.update()

    def setShowFollow(self, showFollow):
        self._showFollow = showFollow
        self.tool.setPreference('_showFollow', self._showFollow)
        self.typesetter.followSelected()
        self.update()

    def setShowRepeat(self, showRepeat):
        self._showRepeat = showRepeat
        self.tool.setPreference('_showRepeat', self._showRepeat)
        self.update()

    def setDoRound(self, doRound):
        self._doRound = doRound
        self.tool.setPreference('_doRound', self._doRound)
        self.update()

    def setOverlayRelated(self, overlayRelated):
        self._overlayRelated = overlayRelated
        self.tool.setPreference('_overlayRelated', self._overlayRelated)
        self.update()

    def setShowMargins(self, showMargins):
        self._showMargins = showMargins
        self.tool.setPreference('_showMargins', self._showMargins)
        self.update()

    def setShowNumbers(self, showNumbers):
        self._showNumbers = showNumbers
        self.tool.setPreference('_showNumbers', self._showNumbers)
        self.update()

    def setShowGrid(self, showGrid):
        self._showGrid = showGrid
        self.tool.setPreference('_showGrid', self._showGrid)
        self.update()

    def setShowComponents(self, showComponents):
        self._showComponents = showComponents
        self.tool.setPreference('_showComponents', self._showComponents)
        self.update()

    def setShowAnchors(self, showAnchors):
        self._showAnchors = showAnchors
        self.tool.setPreference('_showAnchors', self._showAnchors)
        self.update()

    def setShowMeasures(self, showMeasures):
        self._showMeasures = showMeasures
        self.tool.setPreference('_showMeasures', self._showMeasures)
        self.update()

    def setShowMarkColors(self, showMarkColors):
        self._showMarkColors = showMarkColors
        self.tool.setPreference('_showMarkColors', self._showMarkColors)
        self.update()

    def setShowGroupGlyphs(self, showGroupGlyphs):
        self._showGroupGlyphs = showGroupGlyphs
        self.tool.setPreference('_showGroupGlyphs', self._showGroupGlyphs)
        self.update()

    def setCompareGroupMargins(self, compareGroupMargins):
        self._compareGroupMargins = compareGroupMargins
        self.tool.setPreference('_compareGroupMargins', self._compareGroupMargins)
        self.update()

    def setShowMetrics(self, showMetrics):
        self._showMetrics = showMetrics
        self.tool.setPreference('_showMetrics', self._showMetrics)
        self.update()

    def setStepSize(self, stepSize):
        self._stepSize = TX.asIntOrNone(stepSize) or 4
        self.tool.setPreference('_stepSize', TX.asInt(self._stepSize))

    def setMaxGlyphs(self, maxGlyphs):
        self._maxGlyphs = TX.asIntOrNone(maxGlyphs) or MAX_GLYPHS
        self.typesetter.updateMaxGlyphs()
        text = self.typesetter.getUIText()
        self.setText(text)
        self.tool.setPreference('_maxGlyphs', self._maxGlyphs)

    def setTabWidth(self, tabWidth):
        self._tabWidth = TX.asIntOrNone(tabWidth) or TAB_WIDTH
        self.tool.setPreference('_tabWidth', self._tabWidth)

    def setStrokeWidth(self, strokeWidth):
        self._strokeWidth = TX.asFloatOrNone(strokeWidth) or STROKE_WIDTH
        self.tool.setPreference('_strokeWidth', self._strokeWidth)

    def setKeyInterval(self, keyInterval):
        keyInterval = float(keyInterval) / 1000.0
        keyInterval = TX.asFloatOrNone(keyInterval) or KEY_INTERVAL
        if keyInterval < 0.05 or keyInterval > 1:
            keyInterval = KEY_INTERVAL
            self.side.view.keyInterval.set(int(keyInterval * 1000))
        self._keyInterval = keyInterval
        self.tool.setPreference('_keyInterval', self._keyInterval)
        self.typesetter.interval = keyInterval

    # Update.

    def update(self):
        self.compareSelectedGroupMargins()
        self.typesetter.update()
        setLog()

    def updateSide(self):
        self.side.updateStyle()
        self.side.updateDesignSpaces()
        self.side.updateValues()
        self.side.updateSample()

    # Export.

    def exportScripts(self):
        exportGroupsScript(self.style)
        exportKerningScript(self.style)
