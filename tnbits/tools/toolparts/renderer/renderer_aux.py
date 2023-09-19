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
#    aux.py
#

from tnbits.vanillas.listcell import SmallTextListCell

class Aux(object):
    """
    Auxilliary functions for the GUI, getters & setters.
    """

    def setGlobals(self):
        self.renderTraceback = None
        self.warningDialog = None
        self._minFontSize = self.getPreference('minFontSize') or self.MINFONTSIZE_DEFAULT
        self._maxFontSize = self.getPreference('maxFontSize') or self.MAXFONTSIZE_DEFAULT

    def getStyleItems(self):
        """
        Gets styles as items to fill the list.
        """
        styleItems = []
        for styleKey in self.family.getStyleKeys():
            styleName = styleKey[1]

            if self.isTruetypeOpentype(styleName): # For now only TTF and OTF, filters UFO's out.
                d = dict(styleKey=styleKey, styleName=styleName)
                styleItems.append(d)
            else:
                # TODO: add to reporter.
                print('This tool currently only supports TrueType and OpenType files (couldn\'t load %s)' % styleName)

        return styleItems

    def isTruetypeOpentype(self, styleName):
        if styleName.lower().endswith('.ttf') or styleName.lower().endswith('.otf'):
            return True

        return False

    def setFamily(self, family):
        self.family = family
        items = self.getStyleItems()
        window = self.getView()
        window.styleList.set(items)
        self.w.setTitle(family.name)

    def getSelectedStyleKeys(self):
        """
        Returns (familyPath, filename) pairs in a list.
        TODO: could be shared with other tools such as proof.
        """
        view = self.getView()
        selections = view.styleList.getSelection() # Always need a selection to come here.
        styleKeys = [] # Format (familyPath, fileName)

        for selection in selections:
            selectedItem = view.styleList[selection]
            styleKeys.append(selectedItem['styleKey'])

        return styleKeys

    def getFontSizes(self):
        fontSizes = []

        for fontSize in self.FONTSIZES:
            if isinstance(fontSize, int):
                fontSizes.append(str(fontSize))
            else:
                fontSizes.append(fontSize)

        return fontSizes

    def getMinFontSize(self, minSize=False):

        try:
            return '%d' % self._minFontSize
        except:
            return self._minFontSize

    def getMaxFontSize(self, maxSize=False):

        try:
            return '%d' % self._maxFontSize
        except:
            return self._maxFontSize

    def getStyleListDescriptor(self):
        """
        Style list descriptors, sets headers and data structure.
        """
        return [
            # Also styleKey is added for selection reference, not displayed.
            dict(title='File name', key='styleName', width=250,
                cell=SmallTextListCell(editable=False), editable=False),
            # 'magic' kludgy column so we'll get edit callbacks even though
            # none of our columns are editable
            dict(title="", key="dummy", width=200, editable=True),
        ]

