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

import logging
from tnbits.base.constants.tool import *
from tnbits.base.model import *
from tnbits.base.tools import *
from tnbits.model import model

# FIXME: move to tool.
try:
    from mojo.roboFont import CurrentFont
    from mojo.UI import OpenGlyphWindow
except:
    logger = logging.getLogger(__name__)
    logger.info('Not in RoboFont')

class BaseController(object):
    """Bridge between a tool and the model."""
    # TODO: get rid of mode, use isinstance for diff Tool and App.

    def __init__(self, tool, mode='tool'):
        self.tool = tool
        self.mode = mode
        self.family = None
        self.style = None # Current style.
        self.styleKey = None
        self.glyph = None
        self.designSpace = None
        # TODO: not needed anymore?
        self.logger = logging.getLogger(__name__)

    # RoboFont.
    # FIXME: move to tool to keep standalone apps working.

    def editStyle(self, glyphName=None):
        #self.style.save()
        path = self.style.path
        rFont = self.getRFont(path)

        if rFont:
            msg = 'base controller: already open: %s' % path
            self.logger.info(msg)

        else:
            rFont = self.editRFont(path)
            msg = 'base controller: opened style %s in RoboFont' % rFont.path
            self.logger.info(msg)

        self.style = rFont

        if glyphName:
            self.openGlyph(rFont, glyphName)

    def editGlyph(self, glyphName):
        self.editStyle(glyphName=glyphName)

    def openGlyph(self, rFont, glyphName):
        glyph = rFont[glyphName]
        self.setGlyph(glyph)
        OpenGlyphWindow(self.glyph)

    # Tool.

    def getTool(self):
        return self.tool

    def preferencesChanged(self):
        """Updates interface values (checkboxes, textfields, etc...) if
        preferences have changed."""
        pass


    def getMode(self):
        return self.mode

    # Family.

    def openFamily(self):
        """Checks if family is new and if so, opens a new window in tool mode
        or loads it in the current window in application mode."""
        family = openFamily(self.tool)

        if self.mode == 'tool':
            # As tool, separate window for each family.
            openTool(type(self.tool), family)
        elif self.mode == 'app':
            # As application, same window.
            self.setFamily(family)

    def getFamily(self):
        return self.family

    def setFamily(self, family):
        raise NotImplementedError

    def setTitle(self, family):
        self.tool.setTitle(family)

    def setFamilyOrder(self, order):
        """Save the altered order into the .fam file.

        TODO: make independent of list.
        """
        self.family.setStyleKeys(order)
        self.family.save()
        designSpace = self.getDesignSpace()
        self.stylesList.setItems(self.family, designSpace)

    # Style.

    def getStyle(self, styleKey):
        # TODO: use model?
        return self.family.getStyle(styleKey)

    def getStyleKey(self, style):
        return model.getStyleKey(style)

    def getFileName(self, style):
        return style.path.split('/')[-1]

    def editStyleKeys(self, styleKeys, update=True):
        """Opens the selected styles in RoboFont. Note that this causes the
        naked font to change; therefore model will check for updates to
        replace the cache of open styles by the RoboFont naked style instance.
        """
        for styleKey in styleKeys:
            style = model.getStyle(styleKey)
            self.editRFont(style.path)

        '''
        if update:
            # Update the styles, replacing old naked of the fonts by the
            # RoboFont versions, before anything changes to the original.
            # Can be done manually with family.updateRFont combined with a
            # fontDidOpen event.
            model.updateStyles()
        '''

        return style

    def closeStyleKeys(self, styleKeys):
        for styleKey in styleKeys:
            # TODO
            pass

    def saveStyleKeys(self, styleKeys):
        for styleKey in styleKeys:
            style = self.getStyle(styleKey)
            style.save()
            self.logger.info('Saved %s' % style.path)

    def getRFont(self, path):
        # Checks for all fonts currently open in RoboFont comparing file names
        # with that of style.
        try:
            from mojo.roboFont import AllFonts
        except:
            self.logger.info('Not in RoboFont')
            return

        for rFont in AllFonts():
            if rFont.path == path:
                return rFont

    def editRFont(self, path):
        """Opens an RFont of the style in RoboFont."""
        try:
            from mojo.roboFont import OpenFont
        except:
            self.logger.info('Not in RoboFont')
            return

        rFont = self.getRFont(path)

        if rFont:
            self.logger.info('base controller editRFont(): already open %s' % path)
        else:
            rFont = OpenFont(path)
            self.family.updateRFont(rFont)
            self.logger.info('base controller editRFont(): OpenFont %s' % rFont.path)

        return rFont

    @classmethod
    def updateStyles(cls):
        """Update the open family/styles, to match the naked fonts with what
        is already open in the model. If RF has another naked style,
        then change the reference of the model to the RF naked font."""
        model.updateStyles()

    # Design Space.

    def setDesignSpace(self, name):
        if name is None or name is ANY:
            self.designSpace = None
        else:
            self.designSpace = self.family[name]

    def getDesignSpace(self):
        return self.designSpace

    def getDesignSpaceNames(self):
        u"""Gets design space names from family in right order and adds 'Any'
        before."""
        names = self.family.getSortedDesignSpaceNames()
        names.insert(0, ANY)
        return names
