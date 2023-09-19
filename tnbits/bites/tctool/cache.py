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
#    cache.py
#

from tnbits.bites.tctool.textitem import TextItem
from tnbits.base.groups import getGroupKerning

class Cache():
    """Typesetter cache that stores currently loaded glyphs for a single page. Keeps
    track and updates lines depending on viewport size."""

    def __init__(self, controller):
        self.controller = controller
        self._allLines = None
        self._visibleLines = None
        self._lastYIndex = None
        self._dirty = False
        self._selectedIndex = None
        self._hoverIndex = None
        self._width = None
        self._margin = None

    def __len__(self):
        """Returns the index of the last item plus one."""
        i = 0
        line = self.getLastLine()
        textItem = self.getLastItem(line)
        return textItem.index + 1

    def getStyle(self):
        return self.controller.style

    def getLastLine(self):
        """Returns the last line on the page, be it visible or not."""
        lastLine = None
        keys = sorted(self._allLines.keys())
        lastKey = keys[-1]

        if self._visibleLines is not None:
            # checks if last line visible lines > last line all lines.
            visibleKeys = sorted(self._visibleLines.keys())
            lastVisibleKey = visibleKeys[-1]

            if lastVisibleKey > lastKey:
                return self._visibleLines[lastVisibleKey]


        if self._visibleLines is not None and lastKey in self._visibleLines:
            # Last key in visible lines.
            lastLine = self._visibleLines[lastKey]
        else:
            # last line after visible lines.
            lastLine = self._allLines[lastKey]

        return lastLine

    def getLastItem(self, line):
        sortedX = sorted(line.keys())
        lastX = sortedX[-1]
        return line[lastX]

    # Lines.

    def numberOfLines(self):
        # TODO: optionally add visible lines if they extend beyond all lines?
        return len(self._allLines)

    def initLines(self, glyphNames, groups, width, margin, showKerning=True,
            showRepeat=False, showMissing=False, showEmpty=False):
        """"Initializes the

            self._allLines[yIndex][xPosition]

        dictionary that holds glyphs as TextItems for a single page.

        If the glyph does not exist in the font, glyph dictionary is created to
        draw a missing box + glyph name at that position.

        """
        style = self.getStyle()
        self._width = width
        self._margin = margin
        w = 0
        x = margin
        prevGlyphName = None
        prevWidth = 0
        prevKerning = 0
        self._allLines = {}
        index = 0 # Keeps track of all glyphs.
        sampleIndex = 0 # Keeps track of glyphs in the original sample.
        yIndex = 0 # Keeps track of line index.
        selectedIndex = self.getSelectedIndex()

        # Builds up TextItems from glyph names.
        # TODO: break up loop into smaller parts.
        for glyphName in glyphNames:
            kerning = 0
            missing = False

            if not self.controller.exists(glyphName):
                #if not glyphName in style:
                # Glyph does not exist, optionally skip it.
                if not showMissing:
                    continue

                missing = True
                w = 700

            else:
                # Gets glyph, width and kerning.
                glyph = style[glyphName]

                if not showEmpty:
                    if self.isEmpty(glyph):
                        continue

                w = glyph.width

                if showKerning and prevGlyphName is not None:
                    kerning = getGroupKerning(style, prevGlyphName, glyphName,
                            groups)

                x += kerning


            if x + w + margin > width:
                # Newline needed.
                x = margin
                yIndex += 1

                if showRepeat:
                    # Repeats the last glyph of the previous line, No previous
                    # glyph, current is previous glyph with stored previous
                    # kerning, next is the current glyph.
                    d = dict(x=x, index=index, sampleIndex=sampleIndex-1, yIndex=yIndex,
                            name=prevGlyphName, width=prevWidth, isRepeat=True,
                            missing=missing, kerning=prevKerning)
                    ti = TextItem(**d)
                    line = {}
                    line[x] = ti
                    self._allLines[yIndex] = line
                    x += prevWidth
                    index += 1

                    if showKerning:
                        kerning = getGroupKerning(style, prevGlyphName,
                                glyphName, groups)
                        x += kerning

                else:
                    prevGlyphName = None
                    self._allLines[yIndex] = {}

            elif not yIndex in self._allLines:
                # Make new line entry, if it doesn't exist.
                self._allLines[yIndex] = {}

            line = self._allLines[yIndex]

            # Adds the item to the line dictionary at the `x`-position.
            # Because `x` is key we cannot have identical values, or else
            # previous items will be overwritten. As a hack we move it by
            # one unit until the keyname is not taken.
            while x in line:
                x += 1

            # Makes a new TextItem.
            d = dict(x=x, index=index, sampleIndex=sampleIndex, yIndex=yIndex,
                    name=glyphName, width=w, kerning=kerning, missing=missing,
                    isRepeat=False)
            ti = TextItem(**d)
            line[x] = ti

            # If there is a selection to restore, then check if this is the one
            # so we can keep track of it even when TextItems are switched.
            #if selectedIndex and selectedIndex == index:
            #    self.setSelectedIndex(line[x])

            # Save this glyph name, width and kerning value and set index to
            # next position.
            prevGlyphName = glyphName
            prevWidth = w
            prevKerning = kerning
            x += w
            index += 1
            sampleIndex += 1

        return yIndex

    def updateLines(self, groups, lineIndices, showKerning=True,
            showRepeat=False, showMissing=False, showEmpty=False):
        """Updates the lines inside the typesetter viewport. Gets starting
        index from which to draw and consecutive text items that need to be
        typset again. Then rebuilds the lines that are currently visible."""
        # TODO: check if y-index range changed.
        # TODO: also update missing, empty.
        style = self.getStyle()
        currentYIndex = lineIndices[0]
        items = self.getTextItems(lineIndices)
        previous = None
        x = self._margin
        self._visibleLines = {}
        line = {}
        selectedIndex = self.getSelectedIndex()

        for textItem in items:
            # First one.
            if previous is None:
                index = textItem.index
                line[x] = textItem
            else:
                if previous.missing or textItem.missing or not showKerning:
                    # No kerning.
                    kerningValue = 0
                    w = textItem.width
                else:
                    # Kerning.
                    kerningValue = getGroupKerning(style, previous.name,
                            textItem.name, groups)
                    glyph = style[textItem.name]
                    w = glyph.width

                if x + previous.width + w + self._margin > self._width:
                    # New line.
                    x = self._margin
                    self._visibleLines[currentYIndex] = line
                    currentYIndex += 1
                    line = {}

                    if showRepeat:
                        d = dict(x=x, index=index, sampleIndex=textItem.sampleIndex-1,
                                yIndex=currentYIndex, name=previous.name,
                                width=previous.width, isRepeat=True,
                                missing=previous.missing,
                                kerning=previous.kerning,)

                        ti = TextItem(**d)
                        line[x] = ti
                        x += previous.width
                        index += 1

                        if showKerning:
                            kerning = getGroupKerning(style, previous.name,
                                    textItem.name, groups)
                            x += kerning
                else:
                    x += previous.width + kerningValue

                # Adds the item to the line dictionary at the `x`-position.
                # Because `x` is key we cannot have identical values, or else
                # previous items will be overwritten. As a hack it is moved by
                # one unit.
                while x in line:
                    x += 1

                # Updates textItem values. Updates the `x`-value for the
                # TextItem object and uses it as the dictionary key.
                # TODO: make a copy?
                # Note: maybe better to deepcopy?
                textItem.kerning = kerningValue
                textItem.width = w
                textItem.index = index
                textItem.yIndex = currentYIndex
                textItem.x = x
                line[x] = textItem

                # Updates reference to selected object.
                if not textItem.isRepeat and selectedIndex and \
                        selectedIndex == textItem.index:
                    self.setSelectedIndex(textItem)

            previous = textItem
            index += 1

        # Adds the last line.
        if len(line):
            self._visibleLines[currentYIndex] = line

    def isEmpty(self, glyph):

        # Get the DoodleGlyph.
        if hasattr(glyph, 'naked'):
            glyph = glyph.naked()

        if len(glyph) == 0 and len(glyph.components) == 0:
            return True

        return False

    def getLines(self):
        """Either returns visible lines or all lines."""
        if self._visibleLines:
            lines = self._visibleLines
        else:
            lines = self._allLines

        return lines

    def hasLines(self):
        return self._visibleLines or self._allLines

    def resetHover(self):
        if self._hoverIndex:
            self._hoverIndex = None
            return True
        return False

    def isHoverItem(self, textItem):
        if textItem.index == self._hoverIndex:
            return True
        return False

    def hasVisibleLines(self):
        return self._visibleLines is not None

    def clearVisible(self):
        self._visibleLines = None

    def isDirty(self):
        return self._dirty

    def setDirty(self, dirty):
        self._dirty = dirty

    def getLine(self, yIndex):
        """Tries to get line from visible line cache, else gets it from all
        lines."""
        if self._visibleLines and yIndex in self._visibleLines:
            line = self._visibleLines[yIndex]
        else:
            line = self._allLines[yIndex]

        return line

    def isVisible(self, index):
        if not self._visibleLines:
            return False

        lines = sorted(self._visibleLines)

        i0 = lines[0]
        line0 = self._visibleLines[i0]
        ii0 = sorted(line0)[0]
        ti0 = line0[ii0]
        index0 = ti0.index

        i1 = lines[-1]
        line1 = self._visibleLines[i1]
        ii1 = sorted(line1)[-1]
        ti1 = line1[ii1]
        index1 = ti1.index

        if index0 <= index and index <= index1:
            return True

        return False

    def selectFirst(self):
        """Set selection to first item of first line if there are calculated
        lines."""
        lines = self.getLines()

        if len(lines) > 0:
            line = lines[0]
            x = min(line.keys())
            item = line[x]
            self.setSelectedIndex(item)

    # Text Items.

    def setSelectedIndex(self, textItem):
        """If repeated glyph is selected, original text item from sample is selected."""
        if textItem.isRepeat:
            textItem = self.getTextItem(sampleIndex=textItem.sampleIndex)

        self._selectedIndex = textItem.index

    def setHoverIndex(self, textItem):
        if textItem.isRepeat:
            textItem = self.getTextItem(sampleIndex=textItem.sampleIndex)

        self._hoverIndex = textItem.index

    def getFirst(self):
        firstY = sorted(self._allLines.keys())[0]
        firstLine = self._allLines[firstY]
        sortedX = sorted(firstLine.keys())
        firstX = sortedX[0]
        firstItem = firstLine[firstX]
        return firstItem

    def getLast(self):
        lastY = sorted(self._allLines.keys())[-1]
        lastLine = self._allLines[lastY]
        return self.getLastItem(lastLine)

    def getSelectedItem(self):
        """Checks if selected index is in the visible line cache, else gets the
        item  from all lines."""
        if self._selectedIndex is not None:
            textItem = self.getTextItem(self._selectedIndex)
            return textItem

    def getSelectedIndex(self):
        """If there is a current selection, remember the original item
        index."""
        selectedIndex = None
        selectedTextItem = self.getSelectedItem()

        if selectedTextItem is not None:
            selectedIndex = selectedTextItem.index

        return selectedIndex

    def getHoverItem(self):
        if self._hoverIndex is not None:
            textItem = self.getTextItem(self._hoverIndex)
            return textItem

    def getTextItem(self, index=None, sampleIndex=None):
        if index is None and sampleIndex is None:
            return
        elif index is not None and sampleIndex is not None:
            # TODO: raise error
            print('cant pass both index and sampleIndex')

        if index is not None:
            i = index
        elif sampleIndex is not None:
            i = sampleIndex


        # TODO: also for sampleIndex?
        if self.isVisible(i):
            lines = self._visibleLines
        else:
            lines = self._allLines

        for yIndex in sorted(lines.keys()):
            line = lines[yIndex]

            for _, textItem in sorted(line.items()):
                if index is not None:
                    if textItem.index == index:
                        return textItem
                elif sampleIndex is not None:
                    if textItem.sampleIndex == sampleIndex:
                        return textItem

    def getTextItems(self, lineIndices):
        """Puts text items in a row. Items are taken from relevant line cache.
        Repeated glyphs are removed so they can be derived from line ends
        again. Auxiliary function to typesetVisibleLines()."""
        items = []

        for yIndex in lineIndices:
            #if not yIndex in self._allLines:
            #    break

            line = self._allLines[yIndex]

            for _, textItem in sorted(line.items()):
                if textItem.isRepeat:
                    continue
                items.append(textItem)

        return items

    def getAbove(self, dy=1):
        # TODO: compare middles.
        textItem = self.getSelectedItem()
        i = textItem.yIndex - dy

        if i < 0:
            self.controller.previousPage()
            i = self.numberOfLines() - 1

        line = self.getLine(i)
        textItemAbove = None
        sortedX = sorted(line.keys())

        for x in sortedX:
            newItem = line[x]

            if x + newItem.width >= textItem.x:
                textItemAbove = newItem
                break

        if line and textItemAbove is None:
            x = sortedX[-1]
            textItemAbove = line[x]

        return textItemAbove

    def getBelow(self, dy=1):
        # TODO: compare middles.
        textItem = self.getSelectedItem()
        i = textItem.yIndex + dy

        if i >= self.numberOfLines():
            self.controller.nextPage()
            i = 0

        line = self.getLine(i)

        # Now search that line below for the glyph that matches the
        # clicked x-position.
        textItemBelow = None
        sortedX = sorted(line.keys())

        for x in sortedX:
            newItem = line[x]

            if x + newItem.width >= textItem.x:
                textItemBelow = newItem
                break

        if line and textItemBelow is None:
            x = sortedX[-1]
            textItemBelow = line[x]

        return textItemBelow

    def getPrevious(self, dx=1, textItem=None, previousPage=False):
        """Get the glyph on the left, previous line or previous page."""
        if self._selectedIndex is None:
            return

        if textItem is None:
            textItem = self.getSelectedItem()

        j = textItem.index - dx

        # FIXME: also check if page length smaller than dx.
        if textItem.index == 0:
            if previousPage:
                # Page before - rest of the offset.
                self.controller.previousPage()
                j = len(self) - 1
            else:
                return

        return self.getTextItem(j)

    def getNext(self, dx=1, textItem=None, repeat=False, nextPage=False):
        """Get the glyph on the right, next line or next page."""
        if self._selectedIndex is None:
            return

        if textItem is None:
            textItem = self.getSelectedItem()

        i = textItem.index + dx

        # FIXME: also check if page length smaller than dx.
        if i > len(self) - 1:
            if nextPage:
                # Page after + rest of the offset.
                i -= len(self)
                self.controller.nextPage()
            else:
                return

        textItem = self.getTextItem(i)

        if textItem.isRepeat and repeat is False:
            return self.getNext(textItem=textItem)

        return textItem
