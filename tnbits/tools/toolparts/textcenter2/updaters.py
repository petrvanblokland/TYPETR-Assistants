# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    updaters.py
#

import math
from AppKit import NSMakeRect
from tnbits.toolbox.transformer import TX
from tnbits.toolbox.fontparts.groups import GroupsTX
from tnbits.model.toolbox.kerning.groupkerning import getAllGlyphGroups
from tnbits.model.objects.style import setDirty
from tnbits.model.objects.glyph import getComponents
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.tools.toolparts.accentbuilder.instructions import INSTRUCTIONS, BASES_COMPOSITES
import traceback

class Updaters:

    # Make new versions including small caps as keys
    # Including smallcap variants.
    BASES = {}

    # Including smallcap variants.
    BASES_SC_COMPOSITES = {}
    INSTRUCTIONS_SC = {}

    for glyphName, instruction in INSTRUCTIONS.items():
        items = instruction.split("+")

        # Copy plain instruction
        INSTRUCTIONS_SC[glyphName] = instruction

        # Keep glyphName --> base glyph
        BASES[glyphName] = base = items[0]

        if base[0].upper() == base[0] and glyphName[0].upper() == glyphName[0]:
            base_sc = base + '.sc'
            glyphName_sc = glyphName+'.sc'
            INSTRUCTIONS_SC[glyphName_sc] = base_sc + '+' + '+'.join(items[1:])
            BASES[glyphName_sc] = base_sc

    for base, composites in BASES_COMPOSITES.items():
       BASES_SC_COMPOSITES[base] = composites
       if base[0].upper() == base[0]:
           base_sc = base + '.sc'
           BASES_SC_COMPOSITES[base_sc] = composites_sc = set()
           for composite in composites:
               composites_sc.add(composite + '.sc')

    # U P D A T E R S

    def updateWindowTitle(self, info):
        view = self.getView()
        view.setTitle(self.getWindowTitle())

    def updateStyleList(self, info):
        view = self.getView()
        view.styleSelection.setItems(sorted(self.getUniqueFileNames().keys()))

    def updateToggleLockAnchor(self, info):
        item = self._selectedTextItem
        style = self.getStyle()
        if item is not None and style is not None and item.name in style:
            glyph = style[item.name]
            glyph.lib[self.EXTKEY_LOCK] = not glyph.lib.get(self.EXTKEY_LOCK)


    # U P D A T E  M A R G I N S

    def _getCompositeGlyphs(self, g):
        """Search though the style of g to find all composite glyphs that have
        components that that refer to g as base."""
        compositeGlyphs = []
        style = g.getParent()
        for compositeGlyphName in self.BASES_SC_COMPOSITES.get(g.name, []):
            if compositeGlyphName in style:
                compositeGlyph = style[compositeGlyphName]

                # In case locked by TextCenter or AccentBuilder, then skip.
                if not compositeGlyph.lib.get(self.EXTKEY_LOCK):
                    compositeGlyphs.append(compositeGlyph)

        return compositeGlyphs

    def _setLeftMargin(self, g, margin=None):
        """Set the left margin of g. If g has a base glyph and components, then
        take that as margin reference. Otherwise just use margin. Don't update
        the glyph, just answer if it changed."""
        components = getComponents(g)
        baseGlyphName = self.BASES.get(g.name)

        if baseGlyphName == g.name or not components:
            if margin is not None and margin != round(g.angledLeftMargin):
                g.angledLeftMargin = margin
                return True
        offset = None
        #  There is a defined baseGlyphName for this glyph. Find the base
        #  component.
        if baseGlyphName != g.name:
            for component in components:
                if component.baseGlyph == baseGlyphName:
                    offset = component.transformation[4]
                    break

        # Did not find or no baseGlyphName defined?
        if not offset:
            for component in components:
                if g.name.startswith(component.baseGlyph):
                    offset = component.transformation[4]
                    break
        if offset:
            # Make the whole glyph shift by that offset difference.
            g.angledLeftMargin -= offset
            return True
        return False

    def _setRightMargin(self, g, margin=None):
        """Set the right margin of g. If g has a base glyph and components,
        then take that as margin reference. Otherwise just use margin. Don't
        update the glyph, just answer if it changed."""
        components = getComponents(g)
        baseGlyphName = self.BASES.get(g.name)

        if baseGlyphName == g.name or not components:
            if margin is not None:
                g.angledRightMargin = margin
                return True

        # If there is a defined baseGlyphName for this glyph. Find the base
        # component.
        style = g.getParent()
        if baseGlyphName != g.name:
            for component in components:
                if component.baseGlyph == baseGlyphName and baseGlyphName in style:
                    baseGlyph = g.getParent()[baseGlyphName]
                    w = component.transformation[4] + style[baseGlyphName].width
                    if w != g.width:
                        g.width = w
                        return True
                    return False

        # Otherwise try some automatich matching between component reference
        # names and available glyphs with that name.
        for component in components:
            if g.name.startswith(component.baseGlyph) and component.baseGlyph in style:
                w = component.transformation[4] + style[component.baseGlyph].width
                if w != g.width:
                    g.width = w
                    return True
                return False
        return False

    def _findComponent(self, g, componentName):
        """Find the component that has base (split by ".") component name."""
        for component in getComponents(g):
            if component.baseGlyph.split('.')[0] == componentName:
                return component
        return None

    def _findAnchor(self, g, anchorName):
        for anchor in g.anchors:
            if anchor.name == anchorName:
                return anchor
        return None

    def fixAnchorComponents(self, g):
        """Similar to the accentBuilder too: fix the accent transformation
        positions of all accent glyphs that refer to g and are not locked. Also
        fix mistakes in the position of anchor and width of accent cmb glyphs
        if found.

        In order to avoid warnings on glyph with different accent components
        than expected (e.g. as often in ogonek composites, lock the glyph by
        the [tT] command in TextCenter."""
        # Names of glyphs that changed by fixes.
        glyphsChanged = set()
        style = g.getParent()

        # Find glyphs refering to this glyph
        italicOffsetFactor = math.tan(math.radians(-style.info.italicAngle))
        compositeGlyphs = self._getCompositeGlyphs(g)

        # The anchors g may have effect on these glyphs. Check the components.
        for compositeGlyph in compositeGlyphs:
            instructions = self.INSTRUCTIONS_SC.get(compositeGlyph.name)

            if instructions is None:
                print('### [Warning] Cannot find accent instructions for "%s".' % (compositeGlyph.name))
                continue
            accentName, anchorName = instructions.split('+')[1].split('@')
            if not accentName in style:
                print('### [Warning] Accent "%s" does not exist in style.' % accentName)
                continue

            # Find the component and fix the position from it from the base
            # anchor position and the accent anchor position.
            accentComponent = self._findComponent(compositeGlyph, accentName)
            if accentComponent is None:
                print('### [Warning] Accent component "%s" does not exist in glyph "%s".' % (accentName, compositeGlyph.name))
                continue

            # Get the accent glyph and do some testing and fixing.
            accentName = accentComponent.baseGlyph # Now get the real accent name, as it may be gravecmb.uc instead of the standard gravecmb
            accentGlyph = style[accentName]
            if accentGlyph.width:
                print('### [Warning] Accent "%s" width is %d (not zero): Fixed.' % (accentName, accentGlyph.width))
                accentGlyph.width = 0
                glyphsChanged.add(accentName)
            accentAnchor = self._findAnchor(accentGlyph, '_'+anchorName)
            dx = round(italicOffsetFactor * accentAnchor.y)
            if accentAnchor.x != dx:
                print('### [Warning] Accent "%s" anchor.x is %d (not zero): Fixed.' % (accentName, accentAnchor.x) )
                accentAnchor.x = dx
                glyphsChanged.add(accentName)

            # Find the base anchor
            baseAnchor = self._findAnchor(g, anchorName)
            if baseAnchor is None:
                print('### [Warning] Anchor "%s" in base glyph "%s" does not exist.' % (anchorName, g.name))
                continue

            # Now we can fix the offset position of the accent, depending on
            # the angle of the style.
            transformation = list(accentComponent.transformation)
            dy = baseAnchor.y - accentAnchor.y
            dx = round(baseAnchor.x - italicOffsetFactor * baseAnchor.y)

            if transformation[-2] != dx or transformation[-1] != dy:
                print('Fixing position of accent "%s" in glyph "%s" to (%d,%d) by anchor "%s" position from base glyph "%s".' % (accentName, compositeGlyph.name, baseAnchor.x, baseAnchor.y, anchorName, g.name))
                transformation[-2] = dx # Ignore position of accentAnchor.x as it is supposed to be 0
                transformation[-1] = dy
                accentComponent.transformation = transformation
                glyphsChanged.add(compositeGlyph.name)

        self.setChanged(style, glyphsChanged)

    def setChanged(self, style, glyphsChanged):
        for changedGlyphName in glyphsChanged:
            print('changing %s' % changedGlyphName)
            style[changedGlyphName].changed()

    def updateMarginGroups(self, info):
        """Check on validity of groups and kerning. Apply all margins to the glyphs in groups from their base glyph."""
        style = self.getStyle()
        if style is None:
            return
        changedGlyphs = set()
        self.initXGroups(style, force=True) # Make sure that the groups are updated.

        # Also check validity of kerning  group references.
        for (name1, name2), value in style.kerning.items():
            if (name1.startswith('public.kern1') or name1.startswith('@MMK_L')) and not name1 in style.groups:
                print('### [Warning] Deleting kerning. Group "%s" in (%s,%s)-->%s does not exist.' % (name1, name1, name2, value))
                del style.kerning[(name1, name2)]
            if (name1.startswith('public.kern2') or name2.startswith('@MMK_R')) and not name2 in style.groups:
                print('### [Warning] Deleting kerning. Group "%s" in (%s,%s)-->%s does not exist.' % (name2, name1, name2, value))
                del style.kerning[(name1, name2)]

        # Check if there are duplicate names in groups of the same side.
        leftKernGroup = {}
        rightKernGroup = {}
        leftSpaceGroup = {}
        rightSpaceGroup = {}

        for gName, group in style.groups.items():
            if gName.startswith('public.kern1') or gName.startswith('@MMK_L'):
                for cName in group:
                    if not cName in style:
                        print('### [Warning] Glyph "%s" in left group %s" does not exist in style.' % (cName, gName))
                    elif cName in leftKernGroup:
                        print('### [Warning] Duplicate glyph "%s" in left groups "%s" and "%s".' % (cName, leftKernGroup[cName], gName))
                    else:
                        leftKernGroup[cName] = gName

            elif gName.startswith('public.kern2') or gName.startswith('@MMK_R'):
                for cName in group:
                    if not cName in style:
                        print('### [Warning] Glyph "%s" in right group %s" does not exist in style.' % (cName, gName))
                    elif cName in rightKernGroup:
                        print('### [Warning] Duplicate glyph "%s" in right groups "%s" and "%s".' % (cName, rightKernGroup[cName], gName))
                    else:
                        rightKernGroup[cName] = gName

            elif gName.startswith('@SPC_L'):
                for cName in group:
                    if not cName in style:
                        print('### [Warning] Glyph "%s" in left group %s" does not exist in style.' % (cName, gName))
                    elif cName in leftSpaceGroup:
                        print('### [Warning] Duplicate glyph "%s" in left @SPC groups "%s" and "%s".' % (cName, leftSpaceGroup[cName], gName))
                    else:
                        leftSpaceGroup[cName] = gName

            elif gName.startswith('@SPC_R'):
                for cName in group:
                    if not cName in style:
                        print('### [Warning] Glyph "%s" in right group %s" does not exist in style.' % (cName, gName))
                    elif cName in rightSpaceGroup:
                        print('### [Warning] Duplicate glyph "%s" in right @SPC groups "%s" and "%s".' % (cName, rightSpaceGroup[cName], gName))
                    else:
                        rightSpaceGroup[cName] = gName

        # Scan through spacing groups and kerning groups, find base glyph and
        # apply margins to the rest of the group.

        leftBaseDone = {}
        for gName, group in style.groups.items():
            if not '@SPC_R' in gName: # Do only left spacing groups
                continue

            # Calculate base glyph from group name @SPC_R_o_sinf --> o.sinf
            baseGlyphName = self._groupName2BaseGlyph(gName)
            if not baseGlyphName in group:
                print('### [Warning] Base glyph "%s" is not part of its right group "%s"-->%s".' % (baseGlyphName, gName, group))
                continue

            if baseGlyphName in leftBaseDone:
                print('### [Warning] Duplicate base glyph "%s" in space groups "%s" and "%s".' % (baseGlyphName, gName, leftBaseDone[baseGlyphName]))
                continue

            baseGlyph = style[baseGlyphName]
            lm = baseGlyph.angledLeftMargin # @SPC_R is on right, so left margin
            for cName in group:
                if cName in style:
                    g = style[cName]
                    if self._setLeftMargin(g, lm):
                        changedGlyphs.add(cName)
            leftBaseDone[baseGlyphName] = gName

        for gName, group in style.groups.items():
            if not '@MMK_R' in gName: # Do only left kerning groups
                continue
            baseGlyphName = self._groupName2BaseGlyph(gName) # Calculate base glyph from group name @SPC_R_o_sinf --> o.sinf
            if baseGlyphName in leftBaseDone: # Already done by space group, skip
                continue
            if not baseGlyphName in group:
                print('### [Warning] Base glyph "%s" is not part of its left group "%s"-->"%s".' % (baseGlyphName, gName, group))
                continue
            baseGlyph = style[baseGlyphName]
            lm = baseGlyph.angledLeftMargin # @SPC_R is on right, so left margin
            for cName in group:
                if cName in style:
                    g = style[cName]
                    if self._setLeftMargin(g, lm):
                        changedGlyphs.add(cName)
            leftBaseDone[baseGlyphName] = gName


        rightBaseDone = {} # Remember the base glyphs we did.
        for gName, group in style.groups.items():
            if not '@SPC_L' in gName: # Do only left spacing groups
                continue
            baseGlyphName = self._groupName2BaseGlyph(gName) # Calculate base glyph from group name @SPC_L_o_sinf --> o.sinf
            if not baseGlyphName in group:
                print('### [Warning] Base glyph "%s" is not part of its left group "%s"-->"%s".' % (baseGlyphName, gName, group))
                continue
            if baseGlyphName in rightBaseDone:
                print('### [Warning] Duplicate base glyph "%s" in space groups "%s" and "%s".' % (baseGlyphName, gName, rightBaseDone[baseGlyphName]))
                continue
            baseGlyph = style[baseGlyphName]
            rm = baseGlyph.angledRightMargin # @SPC_L is on left, so right margin
            for cName in group:
                if cName in style:
                    g = style[cName]
                    if self._setRightMargin(g, rm):
                        changedGlyphs.add(cName)
            rightBaseDone[baseGlyphName] = gName

        for gName, group in style.groups.items():
            if not '@MMK_L' in gName: # Do only left spacing groups
                continue
            baseGlyphName = self._groupName2BaseGlyph(gName) # Calculate base glyph from group name @SPC_L_o_sinf --> o.sinf
            if baseGlyphName in rightBaseDone: # Already done by space group, skip
                continue
            if not baseGlyphName in group:
                print('### [Warning] Base glyph "%s" is not part of its left group "%s"-->"%s".' % (baseGlyphName, gName, group))
                continue
            baseGlyph = style[baseGlyphName]
            rm = baseGlyph.angledRightMargin # @SPC_L is on left, so right margin
            for cName in group:
                if cName in style:
                    g = style[cName]
                    if self._setRightMargin(g, rm):
                        changedGlyphs.append(cName)
            rightBaseDone[baseGlyphName] = gName

        self.setChanged(style, changedGlyphs)

    def updateAccents(self, info):
        """Update the accent positions of the current selected glyph."""
        style = self.getStyle()

    def updateStyleAccents(self, info):
        """Update the accent position of all glyphs in the style."""
        style = self.getStyle()
        changedGlyphs = set()
        for baseGlyphName, compositeGlyphNames in self.BASES_SC_COMPOSITES.items():
            if not baseGlyphName in style:
                continue
            baseGlyph = style[baseGlyphName]
            for compositeGlyphName in compositeGlyphNames:
                if not compositeGlyphName in style:
                    continue
                compositeGlyph = style[compositeGlyphName]
                if not compositeGlyph.lib.get(self.EXTKEY_LOCK):
                    if self._setLeftMargin(compositeGlyph, baseGlyph.angledLeftMargin):
                        changedGlyphs.add(compositeGlyph.name)
                    if self._setRightMargin(compositeGlyph, baseGlyph.angledRightMargin):
                        changedGlyphs.add(compositeGlyph.name)
            self.fixAnchorComponents(baseGlyph) # Checking inside if accent glyphs are locked

        self.setChanged(style, changedGlyphs)

    def setScale(self, increment=0):
        """Set the scale factor to the ppem value. The scaling depends on the
        unitsPerEm of the selected style."""
        style = self.getStyle()
        if style is not None:
            view = self.getView()
            ppem = max(self.PPEM_MIN, min(self.PPEM_MAX, (TX.asIntOrNone(view.ppem.get()) or self.PPEM_DEFAULT) + increment))
            self._scale = 1.0*ppem/style.info.unitsPerEm
            if increment:
                view.ppem.set(str(ppem))
            self._stringLabels = {} # Reset the cached labels, because their size compensates the drawing scale
            self.resetLines() # Force update of lines and glyph positions

    def getScale(self):
        style = self.getStyle()

        if style is not None and not self._scale: # Needs initialize
            view = self.getView()
            ppem = max(self.PPEM_MIN, min(self.PPEM_MAX, (TX.asIntOrNone(view.ppem.get()) or self.PPEM_DEFAULT)))
            self._scale = 1.0*ppem/style.info.unitsPerEm
        return self._scale or 1

    def updateText(self, info):
        """Update the full screen, assuming that the line caching is already
        defined and up to date. Show values in controls that depend on the
        current selection of glyph(s)."""

        # TODO: Optimize, only update if the selection changed.
        #if self._editSpacing:
        #    self.selectProfiles(True, True)
        #elif self._editKerning:
        #    self.updateKerningGroups()

        if self.w is not None:
            self.w.canvas.update()

    def updateTextHeight(self, info):
        """In case the leading changed, we don't need reflow. Just adjust the
        height of the canvas."""
        if not self.lines:
            self.typesetPage()
        else:
            style = self.getStyle()
            view = self.getView()
            w, h = view.canvas.getNSView().superview().frame().size
            self._oldSize = w, h
            canvasHeight = (len(self.lines)+2) * self.getLeading() * style.info.unitsPerEm * self.getScale()
            self.w.canvas.getNSView().setFrame_(NSMakeRect(0, 0, w, canvasHeight))

    def updateLine(self, info):
        """Recalculate the x positions of the current line from widths and
        kerning, to save calculating the entire page reflow and constructing
        new glyph items. Better to reuse them as much as possible."""
        style = self.getStyle() # Get the style for kerning, which may have been changed.

        if style is None: # No open fonts, clear the canvas.
            return

        emSize = style.info.unitsPerEm # Some extra space around update rectangle for safety.

        if self.lines is None: # Make sure that we have an initialized flow of lines.
            self.typesetPage()

        # Find the line indices to update.
        if info is not None:
            if not isinstance(info, (tuple, list)):
                info = [info]

            # Special request to update these line indices, e.g. when running
            # over page boundaries with the cursor.
            yIndices = info

        elif self._selectedTextItem is not None and \
                self._selectedTextItem.yIndex in range(len(self.lines)): # Check if the line still exists.
            yIndices = [self._selectedTextItem.yIndex] # Otherwise just update the current line index.
        else:
            yIndices = [] # Could not find this line, ignore.

        # Do update rect for each line separate.
        for yIndex in yIndices:
            line = self.lines[yIndex]
            newLine = {}
            newX = None
            maxX = 0
            prevName = None # Keep the prevs for kerning with the next glyph.
            prevWidth = None

            for x, textItem in sorted(line.items()):
                if newX is None:
                    newX = textItem.x # First glyph is positioned as smallest x key.
                    prevWidth = textItem.width
                else:
                    name = textItem.name
                    # Get from group kerning or direct kerning, if groups are missing.
                    kv = self.getGroupKerning(style, textItem.prev, name) or 0 # None on case of missing.
                    textItem.kerning = kv # Set the kerning in the item.
                    newX += prevWidth + kv # And move the cursor by width and kerning.

                    if name is not None and name in style:
                        prevWidth = style[name].width
                    else:
                        prevWidth = style.info.unitsPerEm / 2 # In case glyph does not exist, make default of em/2

                    textItem.x = newX
                    textItem.width = prevWidth
                    maxX = newX + prevWidth # Remember the largest x, so we can calculate the rectangle for fast update.
                # Save the new spaced glyph item.
                newLine[newX] = textItem
            # Save the new spaced glyph line.
            self.lines[yIndex] = newLine

        if yIndices:
            # Update the display of the range of updated lines by estimated
            # rectangle around the changed lines including space for controls,
            # accents, etc. For now, update all, does not seem to be noticable
            # difference in speed.
            minYIndex = max(min(yIndices)-4, 0)
            maxYIndex = min(max(yIndices)+4, len(self.lines)+4)
            scale = self.getScale()
            scaledLeading = self.getLeading() * style.info.unitsPerEm * scale
            self.updateRect((0, minYIndex * scaledLeading, (maxX + emSize) * scale, (maxYIndex - minYIndex) * scaledLeading))

    def updateLines(self, updateInfo):
        if self.lines is not None:
            info = list(self.lines.keys())
        else:
            info = None # Update all lines

        try:
            self.updateLine(info)
        except:
            print(traceback.format_exc())

    def updateKerningGroups(self, info):
        """Update group popup and group glyph listings, depending on current
        selected glyph."""
        self._updating = True # Avoid calling the update for setting checkboxes.
        view = self.getView()
        style = self.getStyle()

        glyphName, selectedTextItem = self.getSelectedGlyphTextItem()
        if not selectedTextItem:
            return
        prevName = selectedTextItem.prev

        groupNamesMR = [] # Left list, group name is @MMK_L_C, combining right margins
        groupNamesML = [] # Right list, group name is @MMK_R_O, combining left margins

        if style is not None and glyphName is not None and glyphName in style and prevName:
            groupNameML, _ = self.getGroupNamesOfGlyph(style, prevName)
            _, groupNameMR = self.getGroupNamesOfGlyph(style, glyphName)

            self.groupKerningCount.set('Groups: %d | Kerning pairs: %d' % (len(style.groups), len(style.kerning)))

            self.groupKerningMR.set('%s --> %d <-- %s' % (prevName, selectedTextItem.kerning, glyphName))
            self.groupKerningNameMR.set(groupNameMR or 'No group')
            self.groupKerningML.set('')
            self.groupKerningNameML.set(groupNameML or 'No group')

            # For now, just clear this field, instead of showing the kerning of
            # the same pair in the related style.
            # TODO: Get this to work.
            self.relatedGroupSpacingML.set('')
            self.relatedGroupSpacingMR.set('')

            # In case of overwriting single pair over their groups. This
            # depends on the availability of kerning pairs with one or both of
            # the single glyph names. Also if there is no group available for
            # one of the glyphs, then the checkbox is set, but disabled for
            # changing.

            #self.singleGlyphKerningMR.enable(groupNameML is not None and groupNameML in style.groups)
            #self.singleGlyphKerningMR.setTitle('%s [%s]' % (selectedTextItem.prev, self.CHAR_SINGLEGLYPHKERNLEFT))
            #self.singleGlyphKerningMR.set((prevName or '', glyphName or groupNameML or '') in style.kerning)
            #self.singleGlyphKerningML.enable(groupNameMR is not None and groupNameMR in style.groups)
            #self.singleGlyphKerningML.setTitle('%s [%s]' % (glyphName, self.CHAR_SINGLEGLYPHKERNRIGHT))
            #self.singleGlyphKerningML.set((prevName or groupNameMR or '', glyphName or '') in style.kerning)

            # Left group is list on the left
            # Right group is list on the right.
            if groupNameML is not None and groupNameML in style.groups:
                groupNamesML = sorted(set(style.groups[groupNameML])) # Remove any duplicates from the list and reorder.
            if groupNameMR is not None and groupNameMR in style.groups:
                groupNamesMR = sorted(set(style.groups[groupNameMR])) # Remove any duplicates from the list and reorder.

            # Fill the lists with new items, reversed because spacing is mirrorred to kerning
            self.leftSpaceGroupGlyphList.set('\n'.join(groupNamesML))
            # Select the glyph in the lists
            #if glyphName in groupNamesML:
            #    self.leftSpaceGroupGlyphList.setSelection([groupNamesML.index(glyphName)])

            # Fill the lists with new items.
            self.rightSpaceGroupGlyphList.set('\n'.join(groupNamesMR))
            # Select the glyph in the lists
            #if glyphName in groupNamesMR:
            #    self.rightSpaceGroupGlyphList.setSelection([groupNamesMR.index(glyphName)])

        else:
            # Glyphs don't exist.
            if style is not None and prevName is not None and prevName in style:
                prevNameLabel = prevName
            else:
                prevNameLabel = '(%s)' % prevName
            self.groupKerningMR.set('') # Same as field self.groupSpacingML
            self.groupKerningNameMR.set(prevNameLabel) # Same as field self.groupSpacingNameML

            if style is not None and glyphName is not None and glyphName in style:
                glyphNameLabel = glyphName
            else:
                glyphNameLabel = '(%s)' % glyphName
            self.groupKerningML.set('') # Same as field self.groupSpacingMR
            self.groupKerningNameML.set(glyphNameLabel) # Same as field self.groupSpacingNameMR

        #self._setGroupButtonStatus(glyphName, leftGlyphNames, rightGlyphNames)
        self._updating = False

    def getSelectedGlyphTextItem(self):
        """Answer the (glyphName, selectedTextItem) of the current selection.
        In case nothing is selected, answer (None, None)."""
        if self._selectedTextItem: # Get index in list of this selected item
            selectedTextItem = self._selectedTextItem
            return selectedTextItem.name, selectedTextItem
        return None, None

    def _getRelatedStyle(self):
        """Try to guess if there is a related style to the current style that
        has useful values to show. E.g. as is the case with Roman-Italic."""
        style = self.getStyle()
        if style is not None and style.path:
            if 'Italic' in style.path:
                relatedStylePath = style.path.replace('_Italic.ufo', '.ufo') # @@@ Hack for now.
            else:
                relatedStylePath = style.path.replace('.ufo', '_Italic.ufo')
            return self.getPath2Style(relatedStylePath)
        return None

    def updateSpaceGroups(self, info):
        """Update group popup and group glyph listings, depending on current
        selected glyph."""
        view = self.getView()
        style = self.getStyle()
        glyphName, selectedTextItem = self.getSelectedGlyphTextItem()

        # Left list, group name is @SPC_R_ or @MMK_R_, combining left margins.
        groupNamesML = []
        # Right list, group name is @SPC_L_ or @MMK_L_, combining right margins.
        groupNamesMR = []

        if style is not None and glyphName is not None and glyphName in style:
            glyph = style[glyphName]
            ga = analyzerManager.getGlyphAnalyzer(glyph) # We need this to get/set the margin by base glyph
            self.groupKerningCount.set('Groups: %d | Kerning pairs: %d' % (len(style.groups), len(style.kerning)))
            groupNameML, groupNameMR = self.getGroupNamesOfGlyph(style, glyphName)
            spaceGroupNameML, spaceGroupNameMR = self.getSpaceGroupNamesOfGlyph(style, glyphName)
            nameML = spaceGroupNameML or groupNameML # Existence of a @SPC_ group overwrites the kerning group.
            nameMR = spaceGroupNameMR or groupNameMR

            # If this glyph get margin from a base glyph that is in the same group, then use that margin.
            self.groupSpacingML.set('%d <-- %s' % (round(ga.leftBaseMargin or 0), glyphName))
            self.groupSpacingNameML.set(nameML or 'No group')
            self.groupSpacingMR.set('%s --> %d' % (glyphName, round(ga.rightBaseMargin or 0)))
            self.groupSpacingNameMR.set(nameMR or 'No group')

            # If there is a related Roman-Italic style, then show the corresponding margin values here.
            relatedStyle = self._getRelatedStyle()
            if relatedStyle is not None and glyphName in relatedStyle:
                relatedGlyph = relatedStyle[glyphName]
                rga = analyzerManager.getGlyphAnalyzer(relatedGlyph) # We need teh analyzer for the base margins.
                label = {True: 'Roman', False: 'Italic'}['Italic' in style.info.styleName]
                self.relatedGroupSpacingML.set('(%d Related %s)' % (round(rga.leftBaseMargin or 0), label))
                self.relatedGroupSpacingMR.set('(%d Related %s)' % (round(rga.rightBaseMargin or 0), label))

            # Show space groups first, if they existing, overwriting the usage
            # kerning groups. This way space groups can have different content
            # (and deleted on production of the fonts), and used with the
            # spacing of the base glyph, hiding the kerning groups.

            # Left group is list on the right
            # Right group is list on the left.
            if nameML is not None and nameML in style.groups:
                groupNamesML = sorted(set(style.groups[nameML])) # Remove any duplicates from the list and reorder.

            if nameMR is not None and nameMR in style.groups:
                groupNamesMR = sorted(set(style.groups[nameMR])) # Remove any duplicates from the list and reorder.

            # Fill the lists with new items.
            self.leftSpaceGroupGlyphList.set('\n'.join(groupNamesML))
            # Select the glyph in the lists
            #if glyphName in groupNamesML:
            #    self.leftSpaceGroupGlyphList.setSelection([groupNamesML.index(glyphName)])

            # Fill the lists with new items.
            self.rightSpaceGroupGlyphList.set('\n'.join(groupNamesMR))
            # Select the glyph in the lists
            #if glyphName in groupNamesMR:
            #    self.rightSpaceGroupGlyphList.setSelection([groupNamesMR.index(glyphName)])

        else:
            if style is not None and glyphName is not None and glyphName in style:
                glyphNameLabel = glyphName
            else:
                glyphNameLabel = '(%s)' % glyphName

            self.groupSpacingML.set('') # Same field as self.groupKerningMR
            self.groupSpacingNameML.set(glyphNameLabel) # Same field as self.groupKerningNameMR
            self.groupSpacingMR.set('') # Same field as self.groupKerningML
            self.groupSpacingNameMR.set('') # Same field as self.groupKerningNameML
            # Clear related style fields.
            self.relatedGroupSpacingML.set('')
            self.relatedGroupSpacingMR.set('')

        # In case of overwriting single pair over their groups, only in kerning mode.
        #self.singleGlyphKerningMR.enable(False)
        #self.singleGlyphKerningMR.setTitle(glyphName)
        #self.singleGlyphKerningMR.set(False)
        #self.singleGlyphKerningML.enable(False)
        #self.singleGlyphKerningML.setTitle(glyphName)
        #self.singleGlyphKerningML.set(False)
        #self._setGroupButtonStatus(glyphName, leftGlyphNames, rightGlyphNames)
