# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    pagelayout.py
#

from copy import copy
from AppKit import NSMakeRect
from tnbits.tools.toolparts.textcenter2.textsamples import (RE_GLYPHNAMES,
        ALL_GLYPHS_TAG, ALL_BASE_GLYPHS_TAG, CAPS_ON_ALL_BASE_GLYPHS_TAG,
        LC_ON_ALL_BASE_GLYPHS_TAG, SMALL_CAPS_TAG, SORTED_KERNING_TAG,
        CUSTOM_TEXT, FIGURE_SETS)
from tnbits.model.toolbox.kerning.groupkerning import getAllGlyphGroups

# Counting all characters of glyph names, not glyphs.
MAX_PAGE_SIZE = 25000

class TextItem:
    """Holds glyph info in the text cache lines."""

    def __init__(self, **kwargs):
        for name, arg in kwargs.items():
            setattr(self, name, arg)

class PageLayout(object):

    def selectSamplePage(self, index, subIndex, updatePages=False):
        view = self.getView()

        sampleText = self.PROOFPAGES[index]
        if sampleText is None: # Divider is selected, take next one.
            index += 1
            view.selectSampleText.set(index)
            sampleText = self.PROOFPAGES[index]

        # If there are multiple pages in the sample, then select the first and
        # fill/enable the view.selectPage popup.

        # There are sub pages in the selected sample.
        if isinstance(sampleText, (tuple, list)):
            pages = []

            for page in sampleText:
                # First 20 characters of first word. Replace escaped slash.
                pages.append(page.split(' ')[0][:20].replace('//','/'))

            if updatePages:
                view.selectPage.setItems(pages)
                # Show the sample-->page selector popup.
                view.selectPage.show(True)
                # Show the popup label.
                view.selectPageLabel.show(True)

            sampleText = sampleText[subIndex]
            view.selectPage.set(subIndex)

        else:
            if updatePages:
                # No paging in this sample, clear the page selector popup.
                view.selectPage.setItems([])
                # Show the sample---> page selector popup.
                view.selectPage.show(False)
                # Hide the popup label.
                view.selectPageLabel.show(False)

        view.rawText.set(sampleText)

        # Clear selections.
        self._lastKey = ''
        # Calculate the new expanded feature text source.
        self.expandFeatureText()
        # Update the canvas and set calculate the flow of text lines.
        self.resetLines()
        self.typesetPage()

        # Set selection to first item of first line if there are calculated
        # lines.
        if self.lines:
            try:
                line = self.lines[0]
                x = min(line.keys())
                item = line[x]
            except (KeyError, IndexError):
                item = None
        else:
            item = None # No source or lines available

        self._selectedTextItem = self._hoverTextItem = item

        # Update the page.
        self.requestUpdate(self.UPDATE_TEXT)
        self.update()

    def expandFeatureText(self):
        """
        """
        view = self.getView()
        t = view.rawText.get()

        # Expand wild cards, such as ALL_GLYPHS.
        if ALL_GLYPHS_TAG in t:
            # Dynamically expand with the sorted glyph set of the current
            # style.
            glyphNames = self._getAllGlyphNames()
            t = t.replace(ALL_GLYPHS_TAG, '/'+'/'.join(glyphNames))

        elif ALL_BASE_GLYPHS_TAG in t:
            # Dynamically expand with all sorted glyphs that don't have an
            # extension. The extension should be address by feature selection
            # and by groups.
            glyphNames = self._getAllBaseGlyphNames()
            t = t.replace(ALL_BASE_GLYPHS_TAG, '/'+'/'.join(glyphNames))

        elif CAPS_ON_ALL_BASE_GLYPHS_TAG in t:
            # Dynamically expand with all sorted glyphs that don't have an
            # extension. The extension should be address by feature selection
            # and by groups.
            glyphNames = self._getCapsXAllBaseGlyphNames()
            t = t.replace(CAPS_ON_ALL_BASE_GLYPHS_TAG, '/'+'/'.join(glyphNames))

        elif LC_ON_ALL_BASE_GLYPHS_TAG in t:
            # Dynamically expand with all sorted glyphs that don't have an
            # extension. The extension should be address by feature selection
            # and by groups.
            glyphNames = self._getLowercaseXAllBaseGlyphNames()
            t = t.replace(LC_ON_ALL_BASE_GLYPHS_TAG, '/'+'/'.join(glyphNames))

        elif SMALL_CAPS_TAG in t:
            # Dynamically expand with the sorted list of smallcaps in the
            # current style.
            smallCaps = []
            for glyphName in self._getAllGlyphNames():
                if '.sc' in glyphName:
                    smallCaps.append(glyphName)
            t = t.replace(SMALL_CAPS_TAG, '/'+'/'.join(smallCaps))

        elif FIGURE_SETS in t:
            style = self.getStyle()
            figureSetString = []
            figureSets = {} # Key is type of extension
            for glyphName in self._getAllGlyphNames():
                nameParts = glyphName.split('.')
                figureName = nameParts[0]
                if not figureName in TN_FIGURES + TN_PRIMARY:
                    continue
                if len(nameParts) > 1:
                    extension = '.'.join(nameParts[1:])
                else:
                    extension = ''
                if not extension in figureSets:
                    figureSets[extension] = set()
                figureSets[extension].add(glyphName)
            """
            for extension, figureSet in sorted(figureSets.items()):
                for
            for figure2 in TN_FIGURES + TN_PRIMARY:
                for figure1 in TN_FIGURES:
                    figureSetString.append('/%s/%s' % (figure1, figure2))
            """
        elif SORTED_KERNING_TAG in t:
            style = self.getStyle()
            kerningSample = []
            k = {}
            kerning = style.kerning

            for nameL, nameR in kerning.keys():
                # Test if there are still group names in the kerning. Then get
                # the value from the We expanded, so we can skip them.
                kerning = self.getGroupKerning(style, nameL, nameR) or 0 # None on case of missing.
                if not kerning:
                    continue

                if not kerning in k:
                    k[kerning] = []

                if nameL in style: # Direct glyph name
                    namesL = [nameL]
                elif nameL in style.groups:
                    namesL = style.groups[nameL]
                else:
                    namesL = []

                if nameR in style: # Direct glyph name
                    namesR = [nameR]
                elif nameR in style.groups:
                    namesR = style.groups[nameR]
                else:
                    namesR = []

                for n1 in namesL:
                    for n2 in namesR:
                        k[kerning].append('/space/%s/%s' % (n1, n2))

            for _, pairs in sorted(k.items()): # Negative values first
                kerningSample += sorted(pairs)

            t = t.replace(SORTED_KERNING_TAG, ''.join(kerningSample))

        '''
        Now the text of `t` may have grown too long. If so, split into pages
        and show them in the page popup (if not already filled by source
        pages. This means that the page split only works if there are not
        other pages, e.g. if the user does a paste. Counting the length of `t`
        is not accurate, since they all are glyph names, but it's a good
        guess that we don't want text pages to be longer than 25000 to do goo
        scrolling.
        '''

        if len(t) > MAX_PAGE_SIZE:
            pages = self._splitTextToPages(t)
            print('LENGTH', len(t))
            for index, page in enumerate(pages):
                print('LENGTH OF EXPANDED TEXT', index, len(page))
            #t = pages[0] # TODO: Bring this under the pages menu.
        self._expandedText = t

    def _splitTextToPages(self, t):
        # Split too-long custom text into pages.
        # TODO: Needs to be finished to place under the pages popup.
        glyphNames = t.split('/')
        chunk = int(MAX_PAGE_SIZE / 5) # Roughly "average" glyphName length.
        self._customTextPages = []
        while glyphNames:
            self._customTextPages.append('/'.join(glyphNames[:chunk]))
            glyphNames = glyphNames[chunk:]
        return self._customTextPages

    def typesetPage(self):
        """In case there are no lines to display or in case the window size
        changed, recalc the text flow. Answer the new window size tuple for
        convenience of the caller."""
        view = self.getView()
        w, h = view.canvas.getNSView().superview().frame().size

        # The window changed size or no lines / glyphs cache yet, or lines were
        # reset.
        if (w, h) != self._oldSize or not self.lines:

            #try:
            canvasHeight = self.typeset(w/self.getScale()) or 100
            #except Exception as e:
            #    print('Error typesetting page:', e)
            #    canvasHeight = h

            self._oldSize = w, h
            # Adjust canvas to follow the scrollview width and the y position
            # for height should happen only when view is resized... with
            # viewDidEndLiveResize
            self.w.canvas.getNSView().setFrame_(NSMakeRect(0, 0, w, canvasHeight))

        return w, h

    def typeset(self, w):
        """Typeset the glyphNames as result of self.glyphNames() into a floq
        that fits on page width *w*, with the given font size and leading. The
        glyph position of each glyph is calculate (also taking the kerning into
        account) and stored in a self.lines[yIndex][xPosition] dictionary that
        holds values of the positioned glyph: @exists, @name, @prev, @width,
        @kerning, @glyph and @path. If the glyph does not exist in the font, a
        special type of glyph dictionary is created to show the screen update
        to draw a missing box + glyph name at that position. An itemIndex is
        maintained, independent of line-layout, so we can restore the new item
        that corresponds with the current selected item. If there currently is
        a selection, it will be replaced by the new item."""
        style = self.getStyle()

        if style is None:
            return
        #leftGroups = FontTX.getXLeftKerningGroupsforGlyphs(style.groups)
        #rightGroups = FontTX.getXRightKerningGroupsforGlyphs(style.groups)

        emSize = style.info.unitsPerEm
        #kerningDict = style.kerning
        #kerningDictPairs = set(kerningDict.keys())
        textScale = self.getScale()
        margin = self.M/textScale
        x = margin
        glyphIndex = 0
        prevGlyphName = None

        # Index of a line in the dictionary of all lines.
        yIndex = 0

        # Index of all items, so we can find the selected item, even after line
        # reflow.
        itemIndex = 0

        if self._selectedTextItem is not None:
            # If there is a current selection, then remember the itemIndex.
            selectedItemIndex = self._selectedTextItem.itemIndex
        else:
            selectedItemIndex = None # No selection to restore.

        glyphNames = self.compiledText()

        # Expanding features if there is a feature controller and
        # featureCompiler installed.
        stylePath = self.getStylePath()

        if stylePath in self._featureCompilers and stylePath in self._featureViewers:
            featureViewer = self._featureViewers[stylePath]
            featureCompiler = self._featureCompilers[stylePath]

            #featureSettings = dict(case='Unchanged', script='latn', language='dflt',
            #    gsub=dict(ss07=False, ss04=True, smcp=False, frac=True))
            glyphNames = featureCompiler.getCompiledGlyphNames(featureViewer.get(), glyphNames)

        # Initialize the line cache.
        self.lines = {}

        for glyphName in glyphNames:
            nextGlyphName = None
            kerning = 0
            if glyphName in ('\r', '\n'): # Newline?
                yIndex += 1
                x = margin
                glyphIndex = 0
                prevGlyphName = None
                continue

            elif not glyphName in style: # Glyph does not exist, mark special case for display
                # Make new line entry if not there yet.
                if not self._showMissingGlyphs:
                    continue # Ignore missing glyphs in text.
                exists = False
                width = emSize/2 # Placeholder width
            else:
                # Get glyph, width and kerning
                exists = True
                glyph = style[glyphName]
                # Make sure not to create negative width.
                width = glyph.width

                # Show kerning?
                if self._showKerning and prevGlyphName is not None:
                    # Get from group kerning or direct kerning, if groups are missing.
                    kerning = self.getGroupKerning(style, prevGlyphName, glyphName) or 0 # None on case of missing.
                x += kerning

            skipSpace = False
            if x + width+margin > w: # Newline needed?
                x = margin
                """
                if self.lines:
                    # Get last item of the current line, so we can copy as first on the next line.
                    lastItem = self.lines[yIndex][max(self.lines[yIndex].keys())]
                else:
                    lastItem = None
                """
                yIndex += 1
                glyphIndex = 0
                prevGlyphName = None #lastItem.name
                skipSpace = True # No spaces at start of the line.

                if 0 and self.lines and self.lines[yIndex-1]:
                    lastItem = self.lines[yIndex-1][sorted(self.lines[yIndex-1].keys())[-1]]
                    # Copy text item from end of previous line (if it exists) and use that item as first
                    # item on the next line. This way we don't loose the kerning combiation in the deisplay
                    # on th eline break. Make new line entry, if not there yet.
                    self.lines[yIndex] = {
                        x: TextItem(x=x, yIndex=yIndex, itemIndex=itemIndex, exists=lastItem.exists,
                            name=lastItem.name, prev=lastItem.prev, next=lastItem.next,
                            width=lastItem.width, kerning=lastItem.kerning, glyphIndex=lastItem.glyphIndex,
                        )
                    }
                    itemIndex += 1
                    x += lastItem.width + lastItem.kerning
                else:
                    self.lines[yIndex] = {}

            elif not yIndex in self.lines:
                # Make new line entry, if not there yet.
                self.lines[yIndex] = {}

            line = self.lines[yIndex]

            if not (skipSpace and glyphName in ('space',)):

                if glyphIndex < len(glyphNames)-1:
                    nextGlyphName = glyphNames[glyphIndex+1]

                # Add the glyph dict at the horizontal position. Note that if
                # there are multiple glyphs on the same position (e.g. glyphs
                # have width = 0 then only the first one will show. As hack
                # we'll move by one unit.
                while x in line:
                    x += 1

                # Now we are sure that the glyph x entry does not exist yet.
                line[x] = TextItem(x=x, yIndex=yIndex, itemIndex=itemIndex,
                    exists=exists, name=glyphName, prev=prevGlyphName, next=nextGlyphName,
                    width=width, kerning=kerning, glyphIndex=glyphIndex,
                )

                # If there is a selection to restore, then check if this is the one.
                if selectedItemIndex == itemIndex:
                    self._selectedTextItem = line[x]
                    self._hoverTextItem = None # Make sure that there is no old item left over from the previous zoom.

                # Save this glyph name and set index to next position
                prevGlyphName = glyphName
                x += width
                glyphIndex += 1
                itemIndex += 1

        # Answers the vertical position of the line last rendered so the caller
        # can adjust the view port height. Uses `yIndex + 2` to add a bit of
        # margin at the end of the page.
        return (yIndex + 2) * self.getLeading() * style.info.unitsPerEm * textScale
