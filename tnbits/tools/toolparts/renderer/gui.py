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
#    gui.py
#

from vanilla import List, Button, PopUpButton, CheckBox, TextBox, \
    HorizontalLine, Group, EditText, TextEditor, RadioGroup

from tnbits.toolbox.transformer import TX

class GUI(object):

    line = 20
    indent = 80

    def buildSide(self, window):
        self.buildFontParameters(window, 4, 4)

    def buildList(self, window, yb):
        """
        Builds the font list.
        """
        window.styleList = List((self.LEFTCOLUMN, 4, -4, -4), [],
            #selectionCallback=self.styleListCallback,
            doubleClickCallback=self.renderCallback,
            #editCallback=self.editStyleListCallback,
            #dragSettings=dragSettings,
            allowsSorting=True, # Set to True if the column sorting bug is solved.
            drawFocusRing=False,
            enableDelete=False,
            allowsMultipleSelection=True,
            allowsEmptySelection=True,
            drawHorizontalLines=True,
            showColumnTitles=True,
            columnDescriptions=self.getStyleListDescriptor(),
            rowHeight=18,
        )

    def buildFontParameters(self, window, x, y):
        """Sets font size and leading."""
        # Main font size.
        fontSizes = self.getFontSizes()

        y += self.line
        window.selectMinFontSizeLabel = TextBox((x, y+2, self.indent, 16), 'Min font size',
                                    sizeStyle='small')

        window.selectMinFontSize = PopUpButton((x+self.indent, y, self.LEFTCOLUMN-8-self.indent, 16),
                                fontSizes, sizeStyle='small',
                                callback=self.savePreferencesCallback)

        size = self.getMinFontSize()
        window.selectMinFontSize.set(fontSizes.index(size))

        y += self.line*1.5
        window.selectMaxFontSizeLabel = TextBox((x, y+2, self.indent, 16), 'Max font size',
                                    sizeStyle='small')

        window.selectMaxFontSize = PopUpButton((x+self.indent, y, self.LEFTCOLUMN-8-self.indent, 16),
                                fontSizes, sizeStyle='small',
                                callback=self.savePreferencesCallback)

        size = self.getMaxFontSize()
        window.selectMaxFontSize.set(fontSizes.index(size))

        y += self.line*1.5
        window.scaledEm = RadioGroup((x, y+2, self.LEFTCOLUMN-8, 3*self.line), ('Fixed Em of style', 'Fixed Em 1024 (64 x 16)', 'Scaled Em (64 x pt)'),
            callback=self.savePreferencesCallback)
        window.scaledEm.set(self.getPreference('scaledEm', 2))
        y += 3*self.line
        window.roundWidthUp = CheckBox((x, y+2, self.LEFTCOLUMN-8, 32), 'Round width up', callback=self.savePreferencesCallback, value=self.getPreference('roundWidthUp', True))
        y += self.line*1.5
        window.exportTTF = CheckBox((x, y+2, self.LEFTCOLUMN-8, 32), 'Export TTF', callback=self.savePreferencesCallback, value=self.getPreference('exportTTF', True))
        return y

