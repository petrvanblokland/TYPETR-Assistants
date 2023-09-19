# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    gui.py
#
from AppKit import NSColor
from lib.UI.inspector import AccordionView
from vanilla import (CheckBox, EditText, TextEditor, TextBox, List,
        PopUpButton, Button, Group, RadioGroup)
from tnbits.vanillas.flippedcanvas import FlippedCanvas

class GroupList(List):
    pass

class GUI:

    def populateView(self):
        """Fills the tool window with widgets."""
        view = self.getView()

        # List width.
        W = 300

        # Width of start / end text entries.
        TW = W/2
        TH = 72
        M = 2
        y = M
        x = M

        # Top.

        view.styleSelectionLabel = TextBox((x, y, W-100-M, 16),
                'Select family style', sizeStyle='small')
        view.styleSelection = PopUpButton((x, y+14, W-M, 20), [],
                sizeStyle='small', callback=self.styleSelectionCallback)

        # Selection of available SmartSets.
        view.selectSampleTextLabel = TextBox((x, y+34, W-100-M, 16),
                'Select sample <->', sizeStyle='small')
        view.selectSampleText = PopUpButton((x, y+48, W-100-M, 18),
                self.PROOFPAGENAMES, sizeStyle='small',
                callback=self.selectSampleTextCallback)
        view.selectSampleText.set(self.getPreference('selectedSampleText', 0))

        view.selectPageLabel = TextBox((x+W-100, y+34, 100-M, 16), u'Page ≤-≥',
                sizeStyle='small')
        view.selectPage = PopUpButton((x+W-100, y+48, 100-M, 18), [],
                sizeStyle='small', callback=self.selectPageCallback)

        view.startControlGlyphs = EditText((x+W, y, TW, TH), '',
                sizeStyle='small', callback=self.controlGlyphsCallback,
                continuous=False)
        page = self.PROOFPAGES[0]

        if isinstance(page, (list, tuple)):
            page = page[0]

        view.rawText = TextEditor((x+W+M+TW, y, -TW-2*M, TH), page,
                callback=self.rawTextCallback)
        view.endControlGlyphs = EditText((-TW-M, y, -M, TH), '',
                sizeStyle='small', continuous=False,
            callback=self.controlGlyphsCallback)

        xx = x+W+M
        y += TH+M

        #view.showGroups = CheckBox((4, y, 120, 18), 'Show groups [g]', value=self._showGroupLists,
        #    sizeStyle='small', callback=self.showGroupsCallback)

        view.ppem = EditText((xx, y, 32, 20), str(self.PPEM_DEFAULT),
                continuous=False, sizeStyle='small',
                callback=self.ppemCallback)

        view.ppemLabel = TextBox((xx+32, y+2, 64, 20), 'ppem [zx]', sizeStyle='small')

        # Will calculate self._scale from ppem and unitsPerEm.
        self.setScale()
        xx += 92+M

        view.leading = EditText((xx, y, 32, 20), str(self.LEADING_DEFAULT), continuous=False,
            sizeStyle='small', callback=self.leadingCallback)
        view.leadingLabel = TextBox((xx+32, y+2, 80, 20), '% leading [cv]', sizeStyle='small')
        xx += 110+M

        # Set cursor increment from preference.
        self._cursorIncrement = int(self.getPreference('cursorIncrement', 4))
        view.cursorIncrement = EditText((xx, y, 32, 20), str(self._cursorIncrement), continuous=False,
            sizeStyle='small', callback=self.cursorIncrementCallback)
        view.cursorIncrementLabel = TextBox((xx+32, y+2, 80, 20), 'cursor', sizeStyle='small')
        xx += 72+M
        view.editMode = RadioGroup((xx, y, 210, 18), ('Edit spacing [s]', 'Edit kerning [k]'), isVertical=False,
            sizeStyle='small', callback=self.editModeCallback)
        view.editMode.set({False:0, True:1}[self._editMode == 'kerning'])
        xx += 220+M
        view.showKerning = CheckBox((xx, y, 110, 18), 'Show kerning [q]', value=self._showKerning,
            sizeStyle='small', callback=self.showKerningCallback)
        xx += 110+M
        view.showMarkers = CheckBox((xx, y, 110, 18), 'Show markers [w]', value=self._showMarkers,
            sizeStyle='small', callback=self.showMarkersCallback)
        xx += 110+M
        view.showMetrics = CheckBox((xx, y, 110, 18), 'Show metrics [m]', value=self._showMetrics,
            sizeStyle='small', callback=self.showMetricsCallback)
        xx += 110+M
        view.showMissingGlyph = CheckBox((xx, y, 110, 18), 'Missing [?]', value=self._showMissingGlyphs,
            sizeStyle='small', callback=self.showMissingGlyphsCallback)

        y += 22 + M

        # Dictionary of feature viewers is initialized at style selection. Bit
        # of hack, save the position for later use, when viewers are created
        # here.
        self._featureViewerPosition = (W, y)

        # Text page canvas
        # Canvas with actual text rending.
        self.w.canvas = FlippedCanvas((W+2*M+150, y, -M, -24-2*M),
            delegate=self,
            canvasSize=(800, 600),
            acceptsMouseMoved=True,
            hasHorizontalScroller=True,
            hasVerticalScroller=True,
            autohidesScrollers=False,
            backgroundColor=None,
            drawsBackground=False
        )

        view.groupEditor = Button((-300-4*M, -24-M, 100-M, 24), 'Group editor',
                callback=self.groupEditorCallback, sizeStyle='small')
        view.saveSources = Button((-200-2*M, -24-M, 100-M, 24), 'Export scripts',
                callback=self.saveScriptsCallback, sizeStyle='small')
        view.saveStyle = Button((-100, -24-M, -M, 24), 'Save style',
                callback=self.saveStyleCallback, sizeStyle='small')

        # Spacing groups
        # Groups are set from style.groups names in the current style.

        view.groupSpace = g = Group((0, y, W, -M))
        yy = 0
        self.groupKerningCount = g.groupCount = TextBox((x, yy, W, 16),
                'Groups: 0 | Kerning pairs:', sizeStyle='regular')

        yy += 24
        self.groupSpacingML = g.groupSpacingML = self.groupKerningMR = TextBox((x, yy, W, 16), 'Left margin:', sizeStyle='regular') # Double width, also contains kerning
        self.groupSpacingMR = g.groupSpacingMR = self.groupKerningML = TextBox((W/2+2, yy, W/2+10, 16), 'Right margin:', sizeStyle='regular')

        # Reserve some space here for alternative values, such as the same
        # margins in italic (hack until we have a better solution).

        yy += 18
        # Double width, also contains kerning.
        self.relatedGroupSpacingML = g.relatedGroupSpacingML = TextBox((x, yy, W, 16), '', sizeStyle='regular')
        self.relatedGroupSpacingMR = g.relatedGroupSpacingMR = TextBox((W/2+2, yy, W/2+10, 16), '', sizeStyle='regular')

        # Default order and naming is for "spacing" mode. For Kerning these are
        # reversed as second reference.
        yy += 18
        self.groupSpacingNameML = g.groupSpacingNameML = self.groupKerningNameMR = TextBox((x, yy, W/2+10, 16), '', sizeStyle='small')
        self.groupSpacingNameMR = g.groupSPacingNameMR = self.groupKerningNameML = TextBox((W/2+2, yy, W/2+10, 16), '', sizeStyle='small')

        #yy += 18
        # Only enabled for kerning.
        #self.singleGlyphKerningMR = g.singleGlyphKerningMR = CheckBox((x, yy, W/2+10, 20), '', callback=self.singleGlyphKerningCallback)
        #self.singleGlyphKerningML = g.singleGlyphKerningML = CheckBox((W/2+2, yy, W/2+10, 20), '', callback=self.singleGlyphKerningCallback)

        yy += 22

        # Right space group is on the left side
        self.rightSpaceGroupGlyphList = g.rightSpaceGroupGlyphList = TextBox((4, yy, W/2-2, -0))
        """
        self.rightSpaceGroupGlyphList = g.rightSpaceGroupGlyphList = List((4, yy, W/2-2, -0), [],
            drawVerticalLines=True, drawHorizontalLines=True, enableDelete=True,
            #editCallback=self.rightSpacingListEditCallback, # In case values are changed manually.
            doubleClickCallback=self.rightSpaceListDoubleClickCallback,
            selectionCallback=self.rightSpaceListSelectionCallback,
            #columnDescriptions=self.getKerningListDescriptor(),
            rowHeight=16) #self.getPreference('sampleSize')*1.4 # Accommodating the sampleSize from the tool preferences.
        """
        # Left space group list is on the right side
        self.leftSpaceGroupGlyphList = g.leftSpaceGroupGlyphList = TextBox((W/2+2, yy, -4, -0))
        """
        self.leftSpaceGroupGlyphList = g.leftSpaceGroupGlyphList = List((W/2+2, yy, -4, -0), [],
            drawVerticalLines=True, drawHorizontalLines=True, enableDelete=True,
            #editCallback=self.leftSpacingListEditCallback, # In case values are changed manually.
            doubleClickCallback=self.leftSpaceListDoubleClickCallback,
            selectionCallback=self.leftSpaceListSelectionCallback,
            #columnDescriptions=self.getKerningListDescriptor(),
            rowHeight=16) #self.getPreference('sampleSize')*1.4 # Accommodating the sampleSize from the tool preferences.
        """
        #view.groupSpace.show(self._showGroupLists)

        # Set page selection from preference sample
        self.selectSampleTextCallback(view.selectSampleText)

        self.requestUpdate((self.UPDATE_STYLELIST, self.UPDATE_TEXT,
            self.UPDATE_SPACEGROUPS, self.UPDATE_KERNINGGROUPS,
            self.UPDATE_WINDOWTITLE))
        self.update()
