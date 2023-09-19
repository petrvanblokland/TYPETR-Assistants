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
#    model.py
#

import os
from vanilla.dialogs import getFileOrFolder, putFile
from tnbits.model import model
from tnbits.base.app import App
from tnbits.toolbox.transformer import TX
from tnbits.base.constants.tool import ALLOWED_EXTENSIONS

"""GUI functions to open a family."""

def findFamilyFile(folderPath):
    """Answers the path of the first family file in folderPath. Answers `None`
    if no family file can be found."""
    for fileName in sorted(os.listdir(folderPath)):
        if fileName.endswith('.fam'):
            return folderPath + '/' + fileName
    return None

def getFamilyID(folderPath):
    # TODO: normalize names first.
    for fileName in sorted(os.listdir(folderPath)):
        ext = TX.extensionOf(fileName)

        if ext in ALLOWED_EXTENSIONS:
            path = folderPath + '/' + fileName
            styleKey = TX.path2StyleKey(path)
            return styleKey[0]

def openFamily(parent=None):
    """
    TODO: read files recursively.
    TODO: more flexible approach to opening a family, see #505.
    """
    useRoboFont = True

    if isinstance(parent, App):
        useRoboFont = False

    msg = 'Select a folder, a family.fam or a font with family name.'
    selection = getFileOrFolder(messageText=msg, title='Open family',
        allowsMultipleSelection=False)

    if selection is not None and len(selection) == 1:
        path = selection[0]
        selectedPath = path
        familyPath = None

        """
        Makes sure a .fam file is found if it exists. If a folder was selected,
        we need to check on the name too because os.path.isdir sees a UFO
        package as a folder. Else we scan the containing folder for .fam files.

        NOTE: This means that folders containing UFO's should _never_ have
        a ".ufo" extension.
        TODO: detect multiple .fam files.
        """

        if os.path.isdir(path) and not path.lower().endswith('.ufo'):
            parentPath = path
            familyPath = findFamilyFile(path)
        else:
            parts = path.split('/')
            parentPath = '/'.join(parts[:-1])
            familyPath = findFamilyFile(parentPath)

        if familyPath is None:
            familyID = getFamilyID(parentPath)

            if familyID is None:
                return

            familyName = TX.path2FamilyName(familyID)
            family = model.loadFamily(familyName, familyID, useRoboFont=useRoboFont)

            #familyPath = putFile(title="Create a new family file by it's family name.",
            #    messageText='This is not a family folder, please give it a name:',
            #    fileName='FAMILYNAME.fam', canCreateDirectories=False, fileTypes=('fam',))

        else:
            # A file was selected or created. This can be a .ufo, .ttf, .orf,
            # .designspace or a .fam. Either way we can detect the family
            # name.
            if model.isFamilyOpen(familyPath):
                family = model.getFamily(familyPath)
            else:
                # Must be a valid path to an unopened family. Get the
                # family instance, indicated by path. Create untitled, if
                # no <family>.fam there.
                family = model.openFamily(familyPath=familyPath, selectedPath=selectedPath, useRoboFont=useRoboFont)

        return family

def closeFamily():
    """
    TODO: close / reopen files in list.
    """
    pass
