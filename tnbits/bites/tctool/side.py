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
#    side.py
#

from vanilla import (Group, TextBox, PopUpButton, EditText, RadioGroup,
        CheckBox, Button)
from tnbits.base.constants.tool import *
from tnbits.base.view import View
from tnbits.base.views import *
from tnbits.bites.tctool.constants import *
from tnbits.model import model

M = 10
LINE = 20
W = SIDE - 2*M
s = 'small'

class Side(View):
    """Adds all control buttons to a group view."""

    height = 45 * LINE

    def __init__(self, controller):
        self.controller = controller
        self.view = Group((0, 0, SIDE - 2*PADDING, self.height))
        nsView = self.view.getNSView()
        nsView.setFrame_(((0, 0), (SIDE - 2*PADDING, self.height)))
        nsView.setFlipped_(True)
        self.ids = None
        self.build()

    # MVC.

    def getController(self):
        return self.controller

    def getView(self):
        return self.view

    def getNSView(self):
        return self.view.getNSView()

    # Build interface.

    def build(self):
        x = M
        y = self.height - LINE
        y = self.buildDesignSpace(x, y)
        y = self.buildStyle(x, y)
        y = self.buildSample(x, y)
        y = self.buildMode(x, y)
        y = self.buildFlags(x, y)
        y = self.buildValues(x, y)
        y = self.buildColors(x, y)
        y = self.buildScripts(x, y)
        y = self.buildDebug(x, y)

    def buildDesignSpace(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Design Space', inverse=True)
        y -= LINE

        pos = (x, y, W-2*M, 16)
        self.view.designSpaces = PopUpButton(pos, [],
                sizeStyle='small', callback=self.designSpaceCallback)
        y -= LINE
        return y

    def buildStyle(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Style', inverse=True)
        y -= LINE

        pos = (x, y, W-2*M, LINE)
        self.view.styleSelection = PopUpButton(pos, [], sizeStyle=s,
                callback=self.styleSelectionCallback)
        y -= LINE
        return y

    def buildSample(self, x, y):
        """Selection of available glyph sets."""
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Sample', inverse=True)
        y -= LINE

        pos = (x, y, W-2*M, 18)
        self.view.selectSample = PopUpButton(pos, SAMPLENAMES,
                sizeStyle=s, callback=self.selectSampleCallback)
        y -= LINE

        self.view.selectPage = PopUpButton((x, y, W-2*M, 18), [],
                sizeStyle='small', callback=self.selectPageCallback)
        y -= LINE
        return y

    def buildMode(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Edit Mode', inverse=True)
        y -= LINE

        s0 = getAttributedString('Spacing [s]')
        s1 = getAttributedString('Kerning [k]')
        self.view.editMode = RadioGroup((x, y, W-2*M, 18), (s0, s1),
                isVertical=False, sizeStyle='small',
                callback=self.editModeCallback)
        y -= LINE
        return y

    def buildFlags(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Flags', inverse=True)
        y -= LINE

        s = getAttributedString('Kerning [q]')
        self.view.showKerning = CheckBox((x, y, 180, 18), s,
                sizeStyle='small', callback=self.showKerningCallback)
        y -= LINE

        s = getAttributedString('Kern markers [w]')
        self.view.showMarkers = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showMarkersCallback)
        y -= LINE

        s = getAttributedString('Glyph space [m]')
        self.view.showMetrics = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showMetricsCallback)
        y -= LINE

        s = getAttributedString('Missing [?]')
        self.view.showMissingGlyph = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showMissingGlyphsCallback)
        y -= LINE

        s = getAttributedString('Empty')
        self.view.showEmptyGlyph = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showEmptyGlyphsCallback)
        y -= LINE

        s = getAttributedString('Follow')
        self.view.showFollow = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showFollowCallback)
        y -= LINE

        s = getAttributedString('Repeat')
        self.view.showRepeat = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showRepeatCallback)
        y -= LINE

        s = getAttributedString('Mark Colors')
        self.view.showMarkColors = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showMarkColorsCallback)
        y -= LINE

        s = getAttributedString('Group Glyphs')
        self.view.showGroupGlyphs = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showGroupGlyphsCallback)
        y -= LINE

        s = getAttributedString('Compare Group Margins')
        self.view.compareGroupMargins = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.compareGroupMarginsCallback)
        y -= LINE

        s = getAttributedString('Round to Step Size')
        self.view.doRound = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.doRoundCallback)
        y -= LINE

        s = getAttributedString('Overlay Related')
        self.view.overlayRelated = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.overlayRelatedCallback)
        y -= LINE

        s = getAttributedString('Components')
        self.view.showComponents = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showComponentsCallback)
        y -= LINE

        s = getAttributedString('Anchors')
        self.view.showAnchors = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showAnchorsCallback)
        y -= LINE

        return y

    def buildDebug(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Debug', inverse=True)
        y -= LINE

        s = getAttributedString('Margins')
        self.view.showMargins = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showMarginsCallback)
        y -= LINE

        s = getAttributedString('Numbers')
        self.view.showNumbers = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showNumbersCallback)
        y -= LINE

        s = getAttributedString('Measures')
        self.view.showMeasures = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showMeasuresCallback)
        y -= LINE

        s = getAttributedString('Grid')
        self.view.showGrid = CheckBox((x, y, 180, 18), s,
                sizeStyle='small',
                callback=self.showGridCallback)
        y -= LINE


        return y

    def buildValues(self, x, y):
        """Builds value entry boxes."""
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Values', inverse=True)
        y -= LINE

        editWidth = 48
        editHeight = 20
        x1 = x + editWidth
        W1 = W - x1 - M

        pos = (x, y, editWidth, editHeight)
        self.view.ppem = EditText(pos, '',
                continuous=False, sizeStyle='small',
                callback=self.ppemCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('PPEM [zx]')
        self.view.ppemLabel = TextBox(pos, s, sizeStyle='small')
        y -= LINE

        pos = (x, y, editWidth, editHeight)
        self.view.leading = EditText(pos, '',
                continuous=False, sizeStyle='small',
                callback=self.leadingCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('% Leading [cv]')
        self.view.leadingLabel = TextBox(pos, s, sizeStyle='small')
        y -= LINE

        pos = (x, y, editWidth, editHeight)
        self.view.stepSize = EditText(pos, '',
                continuous=False, sizeStyle='small',
                callback=self.stepSizeCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('Step Size')
        self.view.stepSizeLabel = TextBox(pos, s,
                sizeStyle='small')
        y -= LINE

        pos = (x, y, editWidth, editHeight)
        self.view.maxGlyphs = EditText(pos, '',
                continuous=False,
                sizeStyle='small', callback=self.maxGlyphsCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('Glyphs per page')
        self.view.maxGlyphsLabel = TextBox(pos, s, sizeStyle='small')
        y -= LINE

        pos = (x, y, editWidth, editHeight)
        self.view.tabWidth = EditText(pos, '',
                continuous=False,
                sizeStyle='small', callback=self.tabWidthCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('Tab width')
        self.view.tabWidthLabel = TextBox(pos, s, sizeStyle='small')
        y -= LINE

        # Stroke width.

        pos = (x, y, editWidth, editHeight)
        self.view.strokeWidth = EditText(pos, '',
                continuous=False,
                sizeStyle='small', callback=self.strokeWidthCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('Stroke width')
        self.view.strokeWidthLabel = TextBox(pos, s, sizeStyle='small')
        y -= LINE

        # Key Interval.

        pos = (x, y, editWidth, editHeight)
        value = ''
        self.view.keyInterval = EditText(pos,
                '', continuous=False,
                sizeStyle='small', callback=self.keyIntervalCallback)

        pos = (x1, y - 3, W1, editHeight)
        s = getAttributedString('Key Interval (ms)')
        self.view.keyIntervalLabel = TextBox(pos, s, sizeStyle='small')
        y -= LINE

        return y

    def buildColors(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Color Scheme', inverse=True)
        y -= 3 * LINE
        s0 = getAttributedString('Regular')
        s1 = getAttributedString('Dia')
        s2 = getAttributedString('Color')
        self.view.colorScheme = RadioGroup((x, y, W-2*M, 18 * 3), (s0, s1, s2),
                sizeStyle='small', callback=self.colorSchemeCallback)


        y -= LINE
        return y

    def buildScripts(self, x, y):
        pos = (x, y, W-2*M, 16)
        y = addTitle(self.view, pos, 'Scripts', inverse=True)
        y -= LINE

        self.view.saveSources = Button((x, y, W-2*M, 18), 'Export',
                callback=self.exportScriptsCallback, sizeStyle='small')

        y -= LINE
        return y

    # Functions to update the contents of the side bar. These should be called
    # from the controller.

    def updateValues(self):
        """Updates the entry box and checkbox values."""
        # TODO: get names from preferences.
        v = self.getView()
        v.showKerning.set(self.controller._showKerning)
        v.selectSample.set(self.controller._sample)
        v.editMode.set(self.controller._editMode)
        v.showMarkers.set(self.controller._showMarkers)
        v.showMetrics.set(self.controller._showMetrics)
        v.showMissingGlyph.set(self.controller._showMissingGlyphs)
        v.showEmptyGlyph.set(self.controller._showEmptyGlyphs)
        v.showFollow.set(self.controller._showFollow)
        v.showRepeat.set(self.controller._showRepeat)
        v.showMarkColors.set(self.controller._showMarkColors)
        v.showGroupGlyphs.set(self.controller._showGroupGlyphs)
        v.compareGroupMargins.set(self.controller._compareGroupMargins)
        v.doRound.set(self.controller._doRound)
        v.overlayRelated.set(self.controller._overlayRelated)
        v.showMargins.set(self.controller._showMargins)
        v.showNumbers.set(self.controller._showNumbers)
        v.showComponents.set(self.controller._showComponents)
        v.showAnchors.set(self.controller._showAnchors)
        v.showMeasures.set(self.controller._showMeasures)
        v.showGrid.set(self.controller._showGrid)
        v.ppem.set(self.controller._ppem)
        v.leading.set(int(self.controller.getLeading() * 100))
        v.stepSize.set(self.controller._stepSize)
        v.maxGlyphs.set(self.controller._maxGlyphs)
        v.tabWidth.set(self.controller._tabWidth)
        v.strokeWidth.set(self.controller._strokeWidth)
        v.keyInterval.set(str((self.controller._keyInterval * 1000)))
        v.colorScheme.set(self.controller._colorScheme)


    def updateStyle(self):
        """Updates the list of styles and sets selection to the current style."""
        self.ids = self.controller.getStyleIDs()
        styleKey = model.getSelectedStyleKey()
        popup = self.view.styleSelection
        popup.setItems(self.ids)
        name = styleKey[1]
        i = self.ids.index(name)

        if isinstance(i, int):
            popup.set(i)

    def updateDesignSpaces(self):
        """Updates the list of design spaces and sets the seletion to the
        first design space.

        # TODO: remember selection.
        """
        view = self.getView()
        names = self.controller.getDesignSpaceNames()
        view.designSpaces.setItems(names)
        view.designSpaces.set(0)

    def updateSample(self):
        """Updates the sample selection, related pages and selected page."""
        v = self.getView()
        v.selectSample.set(self.controller._sample)
        self.updatePageNames()

    def updatePageNames(self):
        v = self.getView()
        names = self.controller.getPageNames()
        v.selectPage.setItems(names)
        v.selectPage.set(self.controller._page)

    # Calbacks.

    def styleSelectionCallback(self, sender):
        """Make the selected style current. Check if there is a feature
        controller, otherwise create one. Make the current featureViewer
        invisible and show the current featureViewer. Create on if it does not
        exist in cache."""
        view = self.getView()
        i = sender.get()
        styleID = self.ids[i]
        self.controller.setStyleByID(styleID)
        self.controller.update()

    def selectSampleCallback(self, sender):
        view = self.getView()
        i = view.selectSample.get()
        page = self.controller.getRecentPage(i)
        page = self.controller.setSample(i, page=page)
        pageNames = self.controller.getPageNames()
        view.selectPage.setItems(pageNames)
        view.selectPage.set(page)

    def selectPageCallback(self, sender):
        view = self.getView()
        i = view.selectPage.get()
        self.controller.setPage(i)

    def designSpaceCallback(self, sender):
        i = sender.get()
        names = self.controller.getDesignSpaceNames()
        name = names[i]
        self.controller.setDesignSpace(name)

        if name == ANY:
            self.ids = self.controller.family.getStyleIDs()
        else:
            self.ids = self.controller.designSpace.getMasterIDs()

        popup = self.view.styleSelection
        popup.setItems(self.ids)
        styleName = self.controller.styleKey[1]

        if styleName in self.ids:
            i = self.ids.index(styleName)

            if isinstance(i, int):
                popup.set(i)

    def ppemCallback(self, sender):
        ppem = sender.get()
        self.controller.setTextScale(ppem)

    def leadingCallback(self, sender):
        leading = sender.get()
        self.controller.setLeading(leading)

    def editModeCallback(self, sender):
        view = self.getView()
        editMode = view.editMode.get()
        self.controller.setEditMode(editMode)

    def showKerningCallback(self, sender):
        showKerning = sender.get()
        self.controller.setShowKerning(showKerning)

    def showMarkersCallback(self, sender):
        """Toggle showing of markers & values"""
        showMarkers = sender.get()
        self.controller.setShowMarkers(showMarkers)

    def showMissingGlyphsCallback(self, sender):
        showMissingGlyphs = sender.get()
        self.controller.setShowMissingGlyphs(showMissingGlyphs)

    def showEmptyGlyphsCallback(self, sender):
        showEmptyGlyphs = sender.get()
        self.controller.setShowEmptyGlyphs(showEmptyGlyphs)

    def showFollowCallback(self, sender):
        showFollow = sender.get()
        self.controller.setShowFollow(showFollow)

    def showRepeatCallback(self, sender):
        showRepeat = sender.get()
        self.controller.setShowRepeat(showRepeat)

    def showMarginsCallback(self, sender):
        showMargins = sender.get()
        self.controller.setShowMargins(showMargins)

    def doRoundCallback(self, sender):
        doRound = sender.get()
        self.controller.setDoRound(doRound)

    def overlayRelatedCallback(self, sender):
        overlayRelated = sender.get()
        self.controller.setOverlayRelated(overlayRelated)

    def showNumbersCallback(self, sender):
        showNumbers = sender.get()
        self.controller.setShowNumbers(showNumbers)

    def showGridCallback(self, sender):
        showGrid = sender.get()
        self.controller.setShowGrid(showGrid)

    def showComponentsCallback(self, sender):
        showComponents = sender.get()
        self.controller.setShowComponents(showComponents)

    def showAnchorsCallback(self, sender):
        showAnchors = sender.get()
        self.controller.setShowAnchors(showAnchors)

    def showMeasuresCallback(self, sender):
        showMeasures = sender.get()
        self.controller.setShowMeasures(showMeasures)

    def showMarkColorsCallback(self, sender):
        showMarkColors = sender.get()
        self.controller.setShowMarkColors(showMarkColors)

    def showGroupGlyphsCallback(self, sender):
        """Toggle showing of markers & values"""
        showGroupGlyphs = sender.get()
        self.controller.setShowGroupGlyphs(showGroupGlyphs)

    def compareGroupMarginsCallback(self, sender):
        """Toggle showing of markers & values"""
        compareGroupMargins = sender.get()
        self.controller.setCompareGroupMargins(compareGroupMargins)

    def showMetricsCallback(self, sender):
        showMetrics = sender.get()
        self.controller.setShowMetrics(showMetrics)

    def stepSizeCallback(self, sender):
        view = self.getView()
        stepSize = view.stepSize.get()
        self.controller.setStepSize(stepSize)

    def maxGlyphsCallback(self, sender):
        view = self.getView()
        maxGlyphs = view.maxGlyphs.get()
        self.controller.setMaxGlyphs(maxGlyphs)

    def tabWidthCallback(self, sender):
        view = self.getView()
        tabWidth = view.tabWidth.get()
        self.controller.setTabWidth(tabWidth)

    def strokeWidthCallback(self, sender):
        view = self.getView()
        strokeWidth = view.strokeWidth.get()
        self.controller.setStrokeWidth(strokeWidth)

    def keyIntervalCallback(self, sender):
        view = self.getView()
        keyInterval = view.keyInterval.get()
        self.controller.setKeyInterval(keyInterval)

    def colorSchemeCallback(self, sender):
        view = self.getView()
        colorScheme = view.colorScheme.get()
        self.controller.setColorScheme(colorScheme)

    def stepsCallback(self, sender):
        pass

    def exportScriptsCallback(self, sender):
        self.controller.exportScripts()
