# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    keysandmouse.py
#


from AppKit import NSCommandKeyMask, NSShiftKeyMask, NSAlternateKeyMask, NSUpArrowFunctionKey,\
    NSDownArrowFunctionKey, NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSColor,\
    NSBackspaceCharacter, NSDeleteFunctionKey, NSDeleteCharacter, NSBezierPath,\
    NSPointInRect, NSGraphicsContext, NSAffineTransform, NSMakeRect, NSMakePoint, \
    NSFontAttributeName, NSFont, NSForegroundColorAttributeName, NSAttributedString, \
    NSControlKeyMask

from tnbits.analyzers.analyzermanager import analyzerManager

class KeysAndMouse:
    """Event-driven functions for key and mouse handling."""

    def getMouseFromEvent(self, event):
        """Answer the current mouse position."""
        view = self.getView()
        if view is not None:
            mouse = view.canvas.getNSView().convertPoint_fromView_(event.locationInWindow(), None)
            return NSMakePoint(mouse.x, mouse.y)
        return None

    def mouseMoved(self, event):
        self._mouse = self.getMouseFromEvent(event)
        if self._mouse is not None:
            # Find the glyph location for this mouse positions
            self.findHoveredGlyph()

    def mouseDown(self, event):
        """The user clicked on one of the glyphs. Select it for a single
        click, and set the horizontal/vertical coordinate as reference for
        cursor operations on the selection. Open the glyph on double click."""
        self._mouseDown = self.getMouseFromEvent(event)
        modifiers = event.modifierFlags()
        shiftDown = modifiers & NSShiftKeyMask
        optionDown = modifiers & NSAlternateKeyMask
        self._lastKey = '' # Clear last key indicator flag.

        if self._hoverTextItem is not None:
            self._selectedTextItem = self._hoverTextItem

            if optionDown:
                # If the clicked glyph (option/alt key) is not the current
                # glyph, then added this glyph (and all the glyphs in its
                # group) to the group of the current glyph. Don't change the
                # selection of the current glyph.
                pass
            elif shiftDown:
                pass
            elif event.clickCount() == 2:  # Double click, open the selected glyph in the editor.
                self.openGlyphWindow()
            else: # Simple selection by click. Set the current hover glyph as selected glyph.
                x = self._selectedTextItem.x
                yIndex = self._selectedTextItem.yIndex
                w = self._selectedTextItem.width
                # Store middle of selected glyph in scaled x/y (not mouse
                # position)
                self._selectedPoint = x + w/2, yIndex

                # Handle necessary updates.
                if self._editMode == 'spacing':
                    self.requestUpdate(self.UPDATE_SPACEGROUPS)
                elif self._editMode == 'kerning':
                    self.requestUpdate(self.UPDATE_KERNINGGROUPS)

                self.requestUpdate(self.UPDATE_LINE) # Update only the current line.
                self.update()

    def mouseDragged(self, event):
        """
        TODO: Debug?
        """
        return
        # @@@@
        """
        self._mouseDragged = self.getMouseFromEvent(event)
        if self._mouseDown is None:
            return # Something happened, there is no mouseDown position stored. Ignore.
        if self._selectedTextItem is not None:
            style = self.getStyle()
            (x, yIndex), currentGlyph = self._selectedTextItem
            line = self.lines.get(yIndex) # It may no longer exist, due to update mismatch.
            if line is not None:
                for cx, glyphItem in sorted(line.items()):
                    prevName = glyphItem.prev
                    if x == cx and prevName is not None:
                        pair = prevName, glyphItem.name
                        k = int(round(self._mouseDragged.x - self._mouseDown.x))
                        kerningDict = self.getKerningDict(style) # Allow automatic group/kerning expansion
                        if pair in kerningDict:
                            oldK = kerningDict[pair]
                        else:
                            oldK = 0
                        if k != oldK:
                            glyphItem.kerning = k
                            style.kerning[pair] = int(round(k or 0))
                            # Avoid typesetting of the whole page, we only adjust the positions
                            # of the glyph items in the rest of the current line.
                            del line[cx]
                            newX = int(round(self._mouseDragged.x/self._scale))
                            glyphItems.x = newX
                            line[newX] = glyphItem
                            self._selectedTextItem = glyphItem
                            self.update()
                        self._doUpdateOnMouseUp = True
                        break
        """

    def mouseUp(self, event):
        self._mouse = self.getMouseFromEvent(event)
        self._mouseDown = None
        self._mouseDragged = None
        if self._doUpdateOnMouseUp: # Dragging may have changed parts. Now update all.
            self._doUpdateOnMouseUp = False
            self.resetLines()
            self.requestUpdate(self.UPDATE_TEXT)
            self.update()

    def keyDown(self, event):
        view = self.getView()
        # get the characters
        characters = event.characters()
        modifiers = event.modifierFlags()
        commandDown = modifiers & NSCommandKeyMask # Check on standard menu short cuts
        shiftDown = modifiers & NSShiftKeyMask
        optionDown = modifiers & NSAlternateKeyMask
        #controlDown = modifiers & NSControlKeyMask
        self._lastKey = ''

        spacingMode = self._editMode == 'spacing'
        kerningMode = self._editMode == 'kerning'

        style = self.getStyle()
        emStep = int(round(style.info.unitsPerEm/1000))
        stepX = self._cursorIncrement # 10 * emStep # Factor step corrected for emSize. 1000 = 1, 2028 = 2
        if shiftDown:
            # TODO: This should be in the preference?
            # Square the distance for >= 4, until larger than stepX * 10, then truncate.
            if stepX >= 4:
                stepX = min(stepX * stepX, stepX * 10) # 4 --> 16, 6 --> 36, 8 --> 64, 10 --> 100, 20 --> 200
            else: # For small steps, multiply by 5.
                stepX = stepX * 5 # 1 --> 5, 2 --> 10, 3 --> 15
        #TODO : make this work
        #if optionDown:
        #    stepX = 1

        changed = False
        changedLine = False
        update = False

        if characters in self.CHAR_LEFTDEC:
            if spacingMode:
                # Only in spacing mode, avoid accidental change when in kerning
                # mode.
                changedLine = self.changeSpacing(self._selectedTextItem, -stepX, 0, True)
                self._moveStatus = self.CHAR_LEFTDEC, stepX
                self._lastKey = self.CHAR_LEFTDEC # Keep the typed key group, so we can adjust the display key feedback.

        elif characters in self.CHAR_LEFTINC:
            if spacingMode: # Only in spacing mode, avoid accidental change when in kerning mode.
                changedLine = self.changeSpacing(self._selectedTextItem, stepX, 0, True)
                self._moveStatus = self.CHAR_LEFTINC, stepX
                self._lastKey = self.CHAR_LEFTINC # Keep the typed key group, so we can adjust the display key feedback.

        elif characters in self.CHAR_RIGHTDEC:
            if spacingMode: # Only in spacing mode, avoid accidental change when in kerning mode.
                changedLine = self.changeSpacing(self._selectedTextItem, -stepX, 0, False)
                self._moveStatus = self.CHAR_RIGHTDEC, stepX
                self._lastKey = self.CHAR_RIGHTDEC # Keep the typed key group, so we can adjust the display key feedback.

        elif characters in self.CHAR_RIGHTINC:
            if spacingMode: # Only in spacing mode, avoid accidental change when in kerning mode.
                changedLine = self.changeSpacing(self._selectedTextItem, stepX, 0, False)
                self._moveStatus = self.CHAR_RIGHTINC, stepX
                self._lastKey = self.CHAR_RIGHTINC # Keep the typed key group, so we can adjust the display key feedback.

        elif characters in self.CHAR_KERNDEC:
            # Decrement kerning by 5 or 1 (shift)
            if kerningMode: # Only in kerning mode, avoid accidental change when in spacing mode.
                changedLine = self.changeKerning(self._selectedTextItem, -stepX, 0)
                self._moveStatus = self.CHAR_KERNDEC, stepX
                self._lastKey = self.CHAR_KERNDEC # Keep the typed key group, so we can adjust the display key feedback.

        elif characters in self.CHAR_KERNINC:
            # Increment kerning by 5 or 1 (shift)
            if kerningMode: # Only in kerning mode, avoid accidental change when in spacing mode.
                changedLine = self.changeKerning(self._selectedTextItem, stepX, 0)
                self._moveStatus = self.CHAR_KERNINC, stepX
                self._lastKey = self.CHAR_KERNINC # Keep the typed key group, so we can adjust the display key feedback.

        elif characters in self.CHAR_ZOOMIN:
            if shiftDown:
                self.setZoom(10)
            else:
                self.setZoom(2)
            self.resetLines() # Force update of lines and glyph item positions
            update = True

        elif characters in self.CHAR_ZOOMOUT:
            if shiftDown:
                self.setZoom(-10)
            else:
                self.setZoom(-2)
            self.resetLines() # Force update of lines and glyph item positions
            update = True

        elif characters in self.CHAR_LEADINGINC:
            if commandDown: # cmd-C = Copy selected glyph
                self.copyToPasteBoard()
            else:
                if shiftDown:
                    self.changeLeading(10)
                else:
                    self.changeLeading(1)
                # No need to reflow text, vertical position of lines is by index not by y-position.
                # But we need to recalculate the height of the canvas.
                self.requestUpdate(self.UPDATE_TEXTHEIGHT)
                update = True

        elif characters in self.CHAR_LEADINGDEC:
            if commandDown: # cmd-V = Paste from paste board onto selected glyph.
                self.pasteFromPasteBoard()
            else:
                if shiftDown:
                    self.changeLeading(-10)
                else:
                    self.changeLeading(-1)
                # No need to reflow text, vertical position of lines is by index not by y-position.
                # But we need to recalculate the height of the canvas.
                self.requestUpdate(self.UPDATE_TEXTHEIGHT)
                update = True

        elif 0 and characters in self.CHAR_SINGLEGLYPHKERNLEFT: # '1'
            # Toggle force left of kerning pair under glyph name instead of group.
            # Ignore update, as that will be done by the callback of the checkbox toggle.
            self.singleGlyphKerningMR.toggle()
            # Now do the callback, as the CheckBox change by script does not do that.
            self.singleGlyphKerningCallback()
            update = False

        elif 0 and characters in self.CHAR_SINGLEGLYPHKERNRIGHT: # '2'
            # Toggle force left of kerning pair under glyph name instead of group.
            # Ignore update, as that will be done by the callback of the checkbox toggle.
            self.singleGlyphKerningML.toggle()
            # Now do the callback, as the CheckBox change by script does not do that.
            self.singleGlyphKerningCallback()
            update = False #

        #elif characters in (self.CHAR_REMOVERIGHT, self.CHAR_ADDRIGHT, self.CHAR_CREATERIGHT, self.CHAR_REMOVELEFT, self.CHAR_ADDLEFT, self.CHAR_CREATELEFT):
            # Group Editor events
            #    CHAR_CREATERIGHT = '1' # Create a new right group with the current glyph
            #    CHAR_ADDRIGHT = '2' # Add the cyurent glyph to the right space group
            #    CHAR_REMOVERIGHT = '3' # Remove the current glyph from the right space group
            #    CHAR_CREATELEFT = '5' # Create a new left group with the current glyph
            #    CHAR_ADDLEFT = '6' # Add the cyrrent glyph to the left space group
            #    CHAR_REMOVELEFT = '7' # Remove the current glyph from the left space group
            #
            # This is a GroupEditor event. Send it along.
            # No need, to update. That may come back from the editor in an update notification call.
            #
        #    self.groupEditorCallback(setStyle=False) # Make sure it is open. No need to update the style there.
        #    if self._groupEditor is not None and self._groupEditor() is not None: # Still alive?
        #        event = dict(type=characters, glyphName=self._selectedTextItem.name)
        #        self._groupEditor().event(event)

        elif characters in self.CHAR_SHOWMISSING:
            self._showMissingGlyphs = not view.showMissingGlyph.get()
            view.showMissingGlyph.set(self._showMissingGlyphs)
            self.resetLines() # Force update of lines and glyph item positions
            update = True # Update whole screen

        elif characters in self.CHAR_SHOWMARKERS:
            self._showMarkers = not self._showMarkers
            view.showMarkers.set(self._showMarkers)
            update = True # Update whole screen

        elif characters in self.CHAR_SHOWKERNING:
            self._showKerning = not view.showKerning.get()
            view.showKerning.set(self._showKerning)
            self.resetLines() # Force update of lines and glyph items positions
            update = True # Update whole screen

        elif characters in self.CHAR_METRICS:
            self._showMetrics = not view.showMetrics.get()
            view.showMetrics.set(self._showMetrics)
            update = True # Update whole screen

        elif characters in self.CHAR_EDITKERNING: # 'kK'
            # Toggle the behavior of the various cursor key (option/cmd/shift)
            # to affect spacing or kerning.  Set to edit spacing flag to False,
            # if it is on. Can be both off, but not both on.
            self._editMode = 'kerning'
            view.editMode.set(1)
            self.requestUpdate((self.UPDATE_KERNINGGROUPS, self.UPDATE_LINES))
            update = True # Update whole screen to hide spacing marker and show kerning marker

        elif characters in self.CHAR_EDITSPACING: # 'sS'
            # Toggle the behavior of the various cursor key (option/cmd/shift)
            # to affect spacing or kerning.  Set to edit kerning flag to False,
            # if it is on. Can be both off, but not both on. If menu shortcut
            # cmd-S is pressed, then save the font without changing spacing
            # mode.
            if commandDown:
                style = self.getStyle()
                if style is not None:
                    self.saveRoboFont(style) # Make sure to save the RF wrapper font if it exists. Otherwise the naked cache.
            else:
                self._editMode = 'spacing'
                view.editMode.set(0)
                self.requestUpdate((self.UPDATE_SPACEGROUPS, self.UPDATE_LINES))
                update = True # Update whole screen to hide kerning marker and show spacing marker.

        elif ord(characters) == self.CHAR_PREVPROOF or characters in (self.CHAR_PREVPROOF_K + self.CHAR_PREVPAGE_K):
            if optionDown or characters in self.CHAR_PREVPROOF_K:
                selection = view.selectSampleText.get()
                subSelection = view.selectPage.get() - 1
                if subSelection < 0:
                    subSelection = len(view.selectPage.getItems())-1
                view.selectPage.set(subSelection)
                self.selectSamplePage(selection, subSelection, False)
            else:
                selection = view.selectSampleText.get() - 1
                subSelection = 0
                if selection < 0:
                    selection = len(view.selectSampleText.getItems())-1
                if self.PROOFPAGES[selection] is None: # Divider is selected, take next one.
                    selection -= 1
                view.selectSampleText.set(selection)
                self.selectSamplePage(selection, subSelection, True)

        elif ord(characters) == self.CHAR_NEXTPROOF or characters in (self.CHAR_NEXTPROOF_K + self.CHAR_NEXTPAGE_K):
            if optionDown or characters in self.CHAR_NEXTPAGE_K:
                selection = view.selectSampleText.get()
                subSelection = view.selectPage.get() + 1
                if subSelection == len(view.selectPage.getItems()):
                    subSelection = 0
                view.selectPage.set(subSelection)
                self.selectSamplePage(selection, subSelection, False)
            else:
                selection = view.selectSampleText.get() + 1
                subSelection = 0
                if selection == len(view.selectSampleText.getItems()):
                    selection = 0
                if self.PROOFPAGES[selection] is None: # Divider is selected, take next one.
                    selection += 1
                view.selectSampleText.set(selection)
                self.selectSamplePage(selection, subSelection, True)

        elif characters == NSUpArrowFunctionKey:
            # Plain up cursor key behavior is to select the glyph item above
            # which is closest to the current x-position. Check if the cursor
            # runs out of the viewport, then scroll one line up.
            changedLine = self.changeSelection(self._selectedTextItem, 0, -1) # Select one line up (unless it is the first line)

            # Check if we are now at the bottom of the page (scrolling through
            # the top). Then we have to update the whole page.
            maxYIndex = len(self.lines)-1

            if changedLine and self._selectedTextItem.yIndex == maxYIndex:
                self.requestUpdate(self.UPDATE_LINE, (0, maxYIndex)) # Update first and last line of the text.
            # Scroll to new position if outside viewport.
            h = self.getLeading() * style.info.unitsPerEm * self._scale
            y = self._selectedTextItem.yIndex * h
            view.canvas.getNSView().scrollRectToVisible_(((0, y), (10, 1.5*h)))
            self._moveStatus = None

        elif characters == NSDownArrowFunctionKey:
            # Plain down cursor key behavior is to select the glyph item below
            # which is closest to the current x-position. Check if the cursor
            # runs out of the viewport, then scroll one line down.
            changedLine = self.changeSelection(self._selectedTextItem, 0, 1) # Select one line down (unless it is the last line)

            # Check if we are now at the top of the page (scrolling through the
            # bottom). Then we have to update the whole page.
            if changedLine and self._selectedTextItem.yIndex == 0:
                self.requestUpdate(self.UPDATE_LINE, (0, len(self.lines)-1)) # Update first and last line of the text.

            # Scroll to new position if outside viewport.
            h = self.getLeading() * style.info.unitsPerEm*self._scale
            y = self._selectedTextItem.yIndex
            view.canvas.getNSView().scrollRectToVisible_(((0, y*h), (10, 1.5*h)))
            self._moveStatus = None

        elif characters == NSLeftArrowFunctionKey:
            # Plain left cursor key behavior is to select the glyph item on the left.
            # Wrap back to the end of the previous line, if the current glyph item is the
            # first on the line.
            changedLine = self.changeSelection(self._selectedTextItem, -1, 0)
            self._moveStatus = None

        elif characters == NSRightArrowFunctionKey:
            # Plain right cursor key behavior is to select the glyph item on the right.
            # Wrap forward to the start of the next line, if the current glyph is the
            # last on the line.
            changedLine = self.changeSelection(self._selectedTextItem, 1, 0)
            self._moveStatus = None

        elif characters in self.CHAR_RECALCMARGINS:
            # Recalculate all margins, according to groups and which glyphs are the base of a group.
            self.requestUpdate((self.UPDATE_MARGINS,))
            self.initXGroups(style, force=True)
            if spacingMode:
                changed = True
                self.requestUpdate((self.UPDATE_MARGINS, self.UPDATE_SPACEGROUPS, self.UPDATE_LINES)) # Update the space groups.
            elif kerningMode:
                # Update the kerning list and the item content, as values may have changed.
                changed = True
                self.requestUpdate((self.UPDATE_MARGINS, self.UPDATE_KERNINGGROUPS, self.UPDATE_LINES))

        elif characters in self.CHAR_REFLOW:
            '''
            Reflow the text lines. This should not exist, because the text is
            automatically reflowed of the window size changes. There are
            situation where just a single line spacing is changed (for reasons
            of update efficiency) and the user want to be sure that the page is
            showing the real spacing/kerning. Force reset of the group
            reversed-references.
            '''
            self.initXGroups(style, force=True)
            if spacingMode:
                changed = True
                self.requestUpdate((self.UPDATE_SPACEGROUPS, self.UPDATE_LINES)) # Update the space groups.
            elif kerningMode:
                # Update the kerning list and the item content, as values may have changed.
                changed = True
                self.requestUpdate((self.UPDATE_KERNINGGROUPS, self.UPDATE_LINES))

        elif characters in ' \n\r':
            # Space or enter keys will open an edit window.
            # Return opens the current selected glyph in an edit window,
            # identical to double click.
            # Open glyph in EditorWindow on hitting space or return or enter
            # key.
            if commandDown:
                self.openFontWindow()
            else:
                self.openGlyphWindow()

        elif characters in self.CHAR_LOCKANCHOR:
            """Toggle the lock flag in glyph.lib (compatible to AccentBuilder
            tool) to activate/prevent recalculate of accent positions,
            according to matching anchors."""
            self.requestUpdate((self.UPDATE_TOGGLELOCKANCHOR, self.UPDATE_LINE))
            changed = True

        elif characters in self.CHAR_UPDATEACCENT:
            """Synchronize all margins and accent positions of unlocked accent
            glyphs from the position and margins of their base glyphs.
            Lowercase "y" only adjusts for the current glyph. Captital "Y"
            adjusts for all glyphs in the current style."""
            if shiftDown:
                self.requestUpdate((self.UPDATE_ACCENTSTYLEPOSITIONS, self.UPDATE_LINES))
            else:
                self.requestUpdate((self.UPDATE_ACCENTPOSITIONS, self.UPDATE_LINES))
            changed = True

        else: # For debugging key input
            print('Unknown command', characters)

        if changedLine: # Just update width runs of the lines without reflow.
            self._hoverTextItem = None # Disable hover rectangle to be shown on selection change by cursor.
            # Just update the positions of the current selected textItem line.
            if spacingMode:
                # Update the space groups.
                self.requestUpdate((self.UPDATE_SPACEGROUPS, self.UPDATE_LINE))
            elif kerningMode:
                # Update the kerning list and the item content, as values may have changed.
                self.requestUpdate((self.UPDATE_KERNINGGROUPS, self.UPDATE_LINE))
        elif changed:
            # Change all?
            self._hoverTextItem = None # Disable hover rectangle to be shown on selection change by cursor.
            self.resetLines() # Force all text to reflow.
            self.requestUpdate(self.UPDATE_TEXT)
        elif update:
            self._hoverTextItem = None # Disable hover rectangle to be shown on selection change by cursor.
            self.requestUpdate(self.UPDATE_TEXT)

        self.update()

        #if changed:
        #    parent.performUndo()
