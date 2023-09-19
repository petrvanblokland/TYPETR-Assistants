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
#    family.py
#

import os

from vanilla.dialogs import getFileOrFolder, putFile
from tnbits.model import model

class Family(object):
    """Functions needed when a tool operates on all styles in a family folder.

    DEPRECATED. Use static functions in familymanager.
    """

    @classmethod
    def _findFamilyFile(cls, folderPath):
        """Answers the path of the first family file in folderPath. Answer None
        if no family file can be found."""
        for fileName in sorted(os.listdir(folderPath)):
            if fileName.endswith('.fam'):
                return folderPath + '/' + fileName
        return None

    @classmethod
    def openFamily(cls):
        """
        From Proof tool. Should probably read files recursively.
        """
        msg = 'Select a folder, a family.fam or a font with family name.'
        selection = getFileOrFolder(messageText=msg, title='Open family',
            allowsMultipleSelection=False)

        if selection is not None and len(selection) == 1: # Selection was made, no cancel.
            path = selection[0] # Get the selected path.

            if os.path.isdir(path) and not path.lower().endswith('.ufo'):
                '''
                A folder was selected, look for any UFO's inside. We need to
                check on the name too because os.path.isdir sees a UFO
                package as a folder. This means that folders containing UFO's
                should _never_ have a ".ufo" extension.
                '''
                familyPath = cls._findFamilyFile(path)

                # No family file found here, ask for family name to write the
                # family file.
                if familyPath is None:
                    path = putFile(title='Create a new family file by its family name.',
                        messageText='This directory is not (yet) a family folder.',
                        fileName='FAMILY', canCreateDirectories=False, fileTypes=('fam',))
                else:
                    path = familyPath # There was a family file in the folder.

            # A file was selected or created. This can be a UFO or a .fam.
            # Either way we can detect the family name.
            if path:
                if model.isFamilyOpen(path):
                    family = model.getFamily(path)
                else:
                    # Must be a valid path to an unopened family. Get the
                    # family instance, indicated by path. Create untitled, if
                    # no <family>.fam there.
                    family = model.openFamily(path=path)

                cls.open(family)

    @classmethod
    def closeFamily(cls):
        """
        TODO: close / reopen files in list.
        """
        pass

