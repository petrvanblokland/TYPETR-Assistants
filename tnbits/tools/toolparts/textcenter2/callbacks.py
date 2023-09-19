# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    callbacks.py
#
import weakref

from defconAppKit.controls.openTypeControlsView import OpenTypeControlsView

from tnbits.toolbox.transformer import TX
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.model.toolbox.kerning.groupkerning import exportGroupsScript, exportKerningScript
from tnbits.tools.toolparts.textcenter2.feacompiler import FeatureCompiler
from tnbits.tools.toolparts.textcenter2.groupeditor import GroupEditor

class Callbacks:
    """
    Callbacks for the text center tool.
    """

    def singleGlyphKerningCallback(self, sender=None):
        '''
        Changing status of left single glyph checkbox. Add / remove kerning
        pair and update status of kerning groups info labels Sender is ignored.
        This method can be called on [1] and [2] keystrokes too.
        '''
        view = self.getView()
        glyphName, selectedTextItem = self.getSelectedGlyphTextItem()
        prevName = selectedTextItem.prev
        kerning = selectedTextItem.kerning # Use the current kerning, in case preferred pair changes.

        leftGlyphNames = [] # Right list, group name is @MMK_L_O, combining right margins
        rightGlyphNames = [] # Left list, group name is @MMK_R_C, combining left margins
        style = self.getStyle()

        if glyphName in style and prevName in style:
            _, groupNameMR = self.getGroupNamesOfGlyph(style, prevName)
            groupNameML, _ = self.getGroupNamesOfGlyph(style, glyphName)

            if groupNameMR:
                # In case there is a group, use it.
                # This checkbox changed status, for left name of kerning pair.
                singleMR = self.singleGlyphKerningMR.get()
            else:
                # In case group is missing, default is to use single name kerning.
                singleMR = True

            if groupNameML: # In case there is a group, use it
                singleML = self.singleGlyphKerningML.get()
            else: # In case group is missing, default is to use single name kerning.
                singleML = True

            # There are 4 combinations that will define if there is a single glyph kerning exception overwriting the group.
            # (singleMR False-->True, singleML)
            # (singleMR True-->False, singleML)
            # (singleMR False-->True, singleML != groupNameML)
            # (singleMR True-->False, singleML != groupNameML)

            # Get the best guess kerning value with current status.
            k = 0
            if (groupNameMR, groupNameML) in style.kerning:
                k = style.kerning[(groupNameMR, groupNameML)]
            if (groupNameMR, glyphName) in style.kerning:
                k = style.kerning[(groupNameMR, glyphName)]
            if (prevName, groupNameML) in style.kerning:
                k = style.kerning[(prevName, groupNameML)]
            if (prevName, glyphName) in style.kerning:
                k = style.kerning[(prevName, glyphName)]

            # Additionally there is the status if a group was found for this glyph.
            if singleMR:
                if singleML: # Single glyph name on both sides. Make sure to remove group-glyph and prev-group if they exist.
                    if (groupNameMR, glyphName) in style.kerning:
                        del style.kerning[(groupNameMR, glyphName)]
                    if (prevName, groupNameML) in style.kerning:
                        del style.kerning[(prevName, groupNameML)]
                    style.kerning[(prevName, glyphName)] = k # Make pair, even if k == 0

                else:
                    if (prevName, glyphName) in style.kerning:
                        del style.kerning[(prevName, glyphName)]
                    if (groupNameMR, glyphName) in style.kerning:
                        del style.kerning[(groupNameMR, glyphName)]
                    style.kerning[(prevName, groupNameML)] = k # Make pair, even if k == 0

            else: # No single kerning, clean up.
                # Status changed to False, make sure to delete the single-single pair if is exists
                # and set the single-group pair if singleML is True
                if singleML: # Single glyph name on both sides. Make sure to remove group-glyph and prev-group if they exist.
                    if (prevName, groupNameML) in style.kerning:
                        del style.kerning[(prevName, groupNameML)]
                    if (prevName, glyphName) in style.kerning:
                        del style.kerning[(prevName, glyphName)]
                    style.kerning[(groupNameMR, glyphName)] = k # Make pair, even if k == 0

                else: # Just group-group, delete the others, don't touch the kerning value
                    if (groupNameMR, glyphName) in style.kerning:
                        del style.kerning[(groupNameMR, glyphName)]
                    if (prevName, groupNameML) in style.kerning:
                        del style.kerning[(prevName, groupNameML)]
                    if (prevName, glyphName) in style.kerning:
                        del style.kerning[(prevName, glyphName)]

            # Not need to update now, just setting checkbox and kerning pairs.
            # Later updates of kerning groups will show proper list and value.

    def resetLines(self):
        """Reset the dictionary of {y: {x: textItem, ...}, ...} line
        positions, to force resetting the text."""
        self.lines = None # Indicate to recalculate the flow of text in lines.

    def glyphLineViewControlsCallback(self, sender):
        # OT selection may have changed.
        self.resetLines() # Reflow a total text lines update, the entire style selection changed.
        self.requestUpdate((self.UPDATE_LINES, self.UPDATE_TEXT, self.UPDATE_SPACEGROUPS, self.UPDATE_KERNINGGROUPS, ))
        self.update()

    def styleSelectionCallback(self, sender):
        """Make the selected style current. Check if there is a feature
        controller, otherwise create one. Make the current featureViewer
        invisible and show the current featureViewer. Create on if it does not
        exist in cache."""
        view = self.getView()
        path = self.uniqueFileName2Path(sender.getItem())

        if path != self._stylePath:
            self._stylePath = path
            """
            prevStyle = self._style # Can be None
            self._style = style = self.family.getStyleKeys()[sender.get()]

            # Hide current
            if prevStyleKey in self._featureViewers:
                self._featureViewers[prevStyleKey].show(False)

            # Dictionary of cache feature compilers. Key is styleKey, value is FeatureCompiler
            if not styleKey in self._featureCompilers:

                W, y = self._featureViewerPosition # List width, created by self.populateView in gui.py

                self._featureCompilers[styleKey] = fc = FeatureCompiler(style)
                featureStyle = fc.getFeatureStyle()

                self._featureViewers[styleKey] = fv = OpenTypeControlsView((W, y, 150, 0), self.glyphLineViewControlsCallback)
                setattr(view, 'featureViewer_%s' % str(styleKey), fv)
                if featureStyle is not None:
                    fv.setFont(featureStyle)
            else: # Show the existing feature viewer.
                self._featureViewers[styleKey].show(True)
            """

            # If there is an open GroupEditor, update the style.
            if self._groupEditor is not None and self._groupEditor() is not None:
                self._groupEditor().setStyle(style)

            self.resetLines() # Reflow a total text lines update, the entire style selection changed.
            self.requestUpdate((self.UPDATE_LINES, self.UPDATE_SPACEGROUPS, self.UPDATE_KERNINGGROUPS, self.UPDATE_WINDOWTITLE))
            self.update()

    def selectSampleTextCallback(self, sender):
        """Get the selected sample text, indicated by the popup, clear the
        lines cache and update the canvas. Skip selection by 1, if a divider is
        selected."""
        view = self.getView()
        selection = view.selectSampleText.get()
        if self.PROOFPAGES[selection] is None: # Divider is selected, take next one.
            selection += 1
        self.selectSamplePage(selection, 0, updatePages=True)
        self.setPreference('selectedSampleText', view.selectSampleText.get())

    def selectPageCallback(self, sender):
        """If there is multiples pages in the selected sample text, then show
        the pages in this popup.  The content is set by the selection of
        self.selectSampleTextCallback."""
        view = self.getView()
        self.selectSamplePage(view.selectSampleText.get(), sender.get(), updatePages=False)

    def controlGlyphsCallback(self, sender=None):
        """Update the control glyphs, as they may have changed."""
        view = self.getView()
        self._tStart = view.startControlGlyphs.get().replace('\\n', '\n')
        self._tEnd = view.endControlGlyphs.get().replace('\\n', '\n')
        self.resetLines() # Force update of lines and glyphItem positions
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def cursorIncrementCallback(self, sender):
        """Cursor increment changed."""
        view = self.getView()
        self._cursorIncrement = TX.asIntOrNone(view.cursorIncrement.get()) or 4
        self.setPreference('cursorIncrement', TX.asInt(self._cursorIncrement)) # Store in preference as integer.

    def rawTextCallback(self, sender):
        """Callback for the raw text input field. Check if it is too long the
        the limit. Otherwise automatically split into multiple pages."""
        self.expandFeatureText() # Expand the features of the raw text into the display text. Split into pages if too long.
        self.resetLines() # Force update of lines and glyph positions
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def editModeCallback(self, sender):
        view = self.getView()
        self._editMode = self.EDIT_MODES[view.editMode.get()]
        self.setPreference('EditMode', self._editMode)
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def showKerningCallback(self, sender):
        self._showKerning = sender.get()
        self.setPreference('ShowKerning', self._showKerning)
        self.resetLines() # Force update of lines and glyph positions
        self.requestUpdate(self.UPDATE_TEXT, self.UPDATE_LINES)
        self.update()

    def showMissingGlyphsCallback(self, sender):
        self._showMissingGlyphs = sender.get()
        self.setPreference('ShowMissingGlyphs', self._showMissingGlyphs)
        self.resetLines() # Force update of lines and glyph positions
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def showMetricsCallback(self, sender):
        # No need to reflow. Just update the text draw.
        self._showMetrics = sender.get()
        self.setPreference('ShowMetrics', self._showMetrics)
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def showMarkersCallback(self, sender):
        """Toggle showing of markers & values"""
        self._showMarkers = sender.get()
        self.setPreference('ShowMarkers', self._showMarkers)
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def ppemCallback(self, sender):
        self.setScale() # Resets the lines
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def leadingCallback(self, sender):
        """Leading changed, redraw the lines. Since we store them as yIndex and
        not as y-position, the actual vertical position is calculated during
        the update draw."""
        self._leading = sender.get()
        self.setPreferences('Leading', self._leading)
        self.requestUpdate(self.UPDATE_TEXT) # No need to reflow, just redraw.
        self.update()

    def featuresChangedCallback(self, sender):
        self.featuresChanged()

    def saveScriptsCallback(self, sender):
        style = self.getStyle()
        exportGroupsScript(style)
        exportKerningScript(style)

    def saveStyleCallback(self, sender):
        style = self.getStyle()
        style.save()

    def groupEditorCallback(self, sender=None, setStyle=True):
        style = self.getStyle()
        if style is not None:
            if self._groupEditor is None or self._groupEditor() is None:
                self._groupEditor = weakref.ref(GroupEditor(style, self))
            else:
                self._groupEditor().setStyle(style)

    def notifyGroupChange(self):
        """Sent by the open GroupEditor, in case the content or naming of
        groups changed."""
        self.requestUpdate((self.UPDATE_SPACEGROUPS, self.UPDATE_KERNINGGROUPS))
        self.update()

    def leftSpaceListDoubleClickCallback(self, sender):
        """Doubleclick on the left space list. Open the glyph in RoboFont."""
        selection = sender.getSelection()
        if selection:
            glyphName = sender[selection[0]]
            self.openGlyphWindow(glyphName)

    def leftSpaceListSelectionCallback(self, sender):
        """Set the selection as /glyph in the endControlGlyphs (flipped order,
        so the left margin will appear on left)"""
        if self._updating:
            return
        view = self.getView()
        selectedGlyphs = ''
        for selection in sender.getSelection():
            selectedGlyphs += '/' + sender[selection]
        view.startControlGlyphs.set(selectedGlyphs)
        self.controlGlyphsCallback(None) # Update the lines

    def rightSpaceListDoubleClickCallback(self, sender):
        """Doubleclick on the right space list. Open the glyph in RoboFont."""
        selection = sender.getSelection()
        if selection:
            glyphName = sender[selection[0]]
            self.openGlyphWindow(glyphName)

    def rightSpaceListSelectionCallback(self, sender):
        """Set the selection as /glyph in the endControlGlyphs (flipped order,
        so the left margin will appear on left)"""
        if self._updating:
            return
        view = self.getView()
        selectedGlyphs = ''
        for selection in sender.getSelection():
            selectedGlyphs += '/' + sender[selection]
        view.endControlGlyphs.set(selectedGlyphs)
        self.controlGlyphsCallback(None) # Update the lines

    def leftSpaceGroupSelectCallback(self, sender):
        # Left space group selection changed.
        self.requestUpdate((self.UPDATE_SPACEGROUPS, self.UPDATE_KERNINGGROUPS))
        self.update()

    def rightSpaceGroupSelectCallback(self, sender):
        # Right space group selection changed.
        self.requestUpdate((self.UPDATE_SPACEGROUPS, self.UPDATE_KERNINGGROUPS))
        self.update()
