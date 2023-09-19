# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   familymanager.py
#
import traceback
import logging
from tnbits.toolbox.transformer import TX
from tnbits.model.objects.family import Family
from tnbits.model.objects.style import getStyleKey
from tnbits.base.constants.tool import (ALLOWED_EXTENSIONS, EXTENSION_FAM,
        EXTENSION_DESIGNSPACE)

logger = logging.getLogger(__name__)

class Model(object):
    """The *Model* instance is a singleton that stores families, design space
    and style data."""

    def __init__(self):
        """
        >>> model.reset() # Reset all data, so we can run clean doc tests.
        >>> model
        [Model families:0]
        >>> #   F A M I L Y
        >>> from tnTestFonts import getFontPath
        >>> name = "Condor-Bold.ufo"
        >>> path = getFontPath(name)
        >>> family = model.openFamily(path=path)
        >>> model
        [Model families:1]
        >>> family is model[family.familyID]
        True
        >>> '/Condor' in model.keys()[0]
        True
        >>> model.isFamilyOpen(family.familyID)
        True
        >>> family
        [Family name:Condor]
        >>> family.keys()
        ['Roman', 'Italic']
        >>> family.getStyleKeys()
        ['Condor-Bold.ufo', 'Condor-Regular.ufo']

        """
        self.reset()

        # Keeps track of styles that are being edited in RoboFont.
        self.rfOpenStyles = {}
        self.selectedKey = None
        self.currentFamily = None

    def __getitem__(self, name):
        return self.families[name]

    def __setitem__(self, name, family):
        self.families[name] = family

    def __contains__(self, name):
        return name in self.families

    def keys(self):
        return self.families.keys()

    def __iter__(self):
        return iter(self.families)

    def __len__(self):
        return len(self.families)

    def __repr__(self):
        return '[%s families:%d]' % (self.__class__.__name__, len(self))

    def openFamily(self, familyPath=None, selectedPath=None, styleKey=None,
            useRoboFont=True, hasPreferences=False):
        """Opens the family at path and derives the familyName from it. The
        path can be of a style or other file. There are several options:

        - If path is a directory or path is None, then ask the user for a
          folder / familyname.
        - If path is a font, then check if there is a family.json file with
          that name. Otherwise create it.
        - If path is a family file, then just open it.


        Typical formats of styleKey:
        (familyID, familyName)

        FamilyID will be expanded by the transformer to full path name from
        current directory:
        ('../Promise.fam', 'Promise-Bold')

        Absolute path:
        ('/FontDevelopment/Promise/2015-12-27/Promise.fam', 'Promise')
As Result of id(style), where style is an unsaved font:
        ('', 1232434556)
        """
        familyID = None
        assert familyPath is not None or styleKey is not None

        if familyPath:
            fileName = TX.path2FileName(familyPath)
            ext = TX.extensionOf(fileName)
            assert ext == EXTENSION_FAM
            familyID = TX.path2FamilyPath(familyPath)
            familyName = TX.path2FamilyName(familyPath)
        elif styleKey:
            familyID = styleKey[0]
            familyName = TX.path2FamilyName(familyID)

        if self.isFamilyOpen(familyID):
            family = self.getFamily(familyID)
        else:
            family = self.loadFamily(familyName, familyID,
                    useRoboFont=useRoboFont, hasPreferences=hasPreferences)

        if selectedPath:
            fileName = TX.path2FileName(selectedPath)
            ext = TX.extensionOf(fileName)

            # FIXME: look for existing .fam file.
            if ext in ALLOWED_EXTENSIONS:
                self.selectedKey = (familyID, fileName)

        return family

    def reset(self):
        """Reset all internal data. Used if the singleton is created. And also
        used by doc tests, so the are guaranteed to start with a fresh data
        set."""
        self.families = {}

    def updateStyles(self):
        """Do a quick check if the model still holds the same naked fonts and
        RoboFont has open. It can happen that RoboFont closed a font and then
        reopened. Which causes the font to be open as different naked instance
        that the model has. Calling the update, the styles in the model and
        enclosed constellations will be changed to refer to the RoboFont styles
        (because it does not work the other way around)."""
        for family in self.families.values():
            family.updateStyles()

    def loadFamily(self, familyName, familyID, useRoboFont=True, hasPreferences=False):
        """Adds a new family, styles aren't loaded yet."""
        assert familyName
        assert familyID
        logging.info('* model.loadFamily(): loading family, ID is %s' % familyID)
        family = Family(familyName, familyID, useRoboFont=useRoboFont,
                    hasPreferences=hasPreferences)
        self.families[familyID] = family
        self.currentFamily = family
        return family

    def closeFamily(self, family):
        print('To be implemented')

    def getSelectedStyleKey(self):
        if self.selectedKey:
            return self.selectedKey

        if self.currentFamily:
            styleKeys = list(self.currentFamily.getStyleKeys())

            if len(styleKeys):
                return styleKeys[0]

    def getFamily(self, familyID):
        """Answers the family related to familyID, which must be a path to an
        existing family.fam file."""
        return self[familyID]

    def isFamilyOpen(self, familyID):
        """Answers if a family with this name or path is already open."""
        return familyID in self

    def getStyleKey(self, style):
        """Answers the styleKey of style, which is a tuple of (familyPath,
        styleId). Open the family/style if the styleKey does not exist in the
        manager."""
        #self.openFamily(style.path) # Open the family if possible, otherwise ignore.
        return getStyleKey(style)

    def getStyle(self, styleKey):
        """Answers the style tuple from the styleKey of format (familyID,
        fileName). If there is no family with that familyID, then open it
        first."""
        family = self.openFamily(styleKey[0])

        if family is not None:
            # Answers the style with this styleKey if it exists, otherwise
            # answers None.
            return family.getStyle(styleKey)

        # Not possible to open the family with this familyID; The caller should
        # try to find it.
        return None

    def getStyleFromPath(self, path):
        familyPath = TX.path2FamilyPath(path)
        family = self.openFamily(familyPath)
        return family.getStyle(path)

    def getMasterKeysOfStyle(self, styleKey):
        """Answers the total set of master keys that have an interpolation
        relation through any of the family constellations."""
        family = self.openFamily(styleKey[0])
        return family.getMasterKeysOfStyle(styleKey)

    def getDesignSpacesOfStyle(self, styleKey):
        """Answers the total set of design spaces that have an interpolation
        relation in any of the families."""
        family = self.openFamily(styleKey[0])
        return family.getDesignSpacesOfStyle(styleKey)

    def fontDidOpen(self, sender):
        """Keeps track of fonts being edited in RoboFont, receives a
        notification."""
        rfStyle = sender['font']
        rfTool = sender['tool']
        self.rfOpenStyles[rfTool] = rfStyle

    def fontDidClose(self, sender):
        """Receives a notification when RoboFont editing window closes. Finds
        family using font path and schedules it to be reloaded directly from
        the file."""
        rfTool = sender['tool']
        rfStyle = self.rfOpenStyles[rfTool]
        path = rfStyle.path
        # FIXME: TTF / OTF fonts as RF Wrapper don't have a path.
        family = self.openFamily(path)
        family.removeClosedFont(path)

    def isDirty(self):
        for family in self.families.items():
            if family.dirty:
                return True

# Singleton object that keeps families stored, equivalent to RoboFont
# Document.
model = Model()

def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
