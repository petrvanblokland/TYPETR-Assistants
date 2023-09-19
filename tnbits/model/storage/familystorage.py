# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    familystorage.py
#
import os
import json
import traceback
import logging

from tnbits.toolbox.transformer import TX
from tnbits.model.storage.basestorage import BaseStorage
from tnbits.model.objects.style import Style, getStyleKey, nakedStyle
from defcon.objects.font import Font

logger = logging.getLogger(__name__)

class FamilyStorage(BaseStorage):
    """The FamilyStorage holds a set of styles together. The default type of
    family storage does not keep the structure. But other inheriting classes
    can define behavior to read/write from plist file or database record.

    >>> from tnTestFonts import getFontPath
    >>> name = "Condor-Bold.ufo"
    >>> path = getFontPath(name)
    >>> familyPath = TX.path2FamilyDir(path)
    >>> storage = FamilyStorage(familyPath)
    >>> styleID = name
    >>> pack = storage.getPack()
    >>> pack['myData'] = 123
    >>> storage.setPack(pack)
    >>> pack['designSpaces'].keys()
    ['Roman', 'Italic']
    >>> style = storage.getStyle(styleID) # In case of docTest answers path, not style.
    >>> style.endswith('ufo')
    True

    """
    AID = 'FB_FAM' # Unique storage ID for this class.
    DEFAULT_DESIGNSPACES = ('Roman', 'Italic')
    PACKKEY_SORTEDSTYLEIDS = 'sortedStyleIDs'
    PACKKEY_DESIGNSPACES = 'designSpaces'
    PACKKEY_PREFERENCES = 'preferences'
    PACKKEY_LIB = 'lib'

    def __init__(self, path):
        if not path.endswith('.fam'):
            path += '.fam'

        self.path = path
        # Read the pack if possible.
        success = False

        if os.path.exists(self.path) and not os.path.isdir(self.path):
            f = open(self.path, 'rb')
            s = f.read()
            f.close()

            try:
                self.pack = json.loads(s) #cjson.decode(s)
                success = True
            except ValueError:
                os.system('cp "%s" "%s.BAD"' % (path, path))
                logger.error('Could not read damaged family file %s' % path)
                logger.error('Copied this bad fam file to %s.BAD' % path)
                logger.error('to avoid it will be overwritten by the first save of the new empty family.')

        # Otherwise create a new pack with default design space data to be
        # saved later as <family>.fam
        if not success:
            self.pack = {}

        # Verify the pack format and adjust where needed.
        self.verifyPack()

    def verifyPack(self):
        """Verify the pack format for consistency. We can assume that the
        self.pack already exists, but it may be empty."""
        # If pack is not a dict, then overwrite data with empty dict. We cannot
        # save unknown pack data format.
        if not isinstance(self.pack, dict):
            self.pack = {}

        if not self.PACKKEY_DESIGNSPACES in self.pack:
            self.pack[self.PACKKEY_DESIGNSPACES] = {}

        # Make sure the default design spaces are there.
        designSpaces = self.pack[self.PACKKEY_DESIGNSPACES]

        for cName in self.DEFAULT_DESIGNSPACES:
            if not cName in designSpaces:
                designSpaces[cName] = {} # Create empty design space data

        # Initialize sorted styleIDs list.
        if not self.PACKKEY_SORTEDSTYLEIDS in self.pack:
            self.pack[self.PACKKEY_SORTEDSTYLEIDS] = []

        # Initialize the generic family.lib
        if not self.PACKKEY_LIB in self.pack:
            self.pack[self.PACKKEY_LIB] = []

        # Initialize the generic family.lib
        if not self.PACKKEY_LIB in self.pack:
            self.pack[self.PACKKEY_LIB] = []

        # Initialize the generic family.lib
        if not self.PACKKEY_PREFERENCES in self.pack:
            self.pack[self.PACKKEY_PREFERENCES] = {}

    def getPack(self):
        """Verify the pack and then answer it. Check if there is at least the
        default design space data."""
        self.verifyPack()
        return self.pack

    def setPack(self, pack):
        """Set the pack and verify the consistancy."""
        self.pack = pack
        self.verifyPack()

    def save(self, path=None):
        """Write the pack to the <family.name>.fam file."""
        if path is None:
            path = self.path
        assert path is not None
        f = open(path, 'w')
        d = json.dumps(self.pack, indent=2, sort_keys=True)
        f.write(d)
        f.close()

    def _get_dirPath(self):
        return TX.path2FamilyDir(self.path)

    dirPath = property(_get_dirPath)


    # Styles.

    def getStyle(self, path, useRoboFont=True):
        """Make a Style instance from path and add it to self.styles with key
        style.id."""
        style = None
        openFontPaths = {}
        fileName = path.split('/')[-1]

        # TODO: make sure extensionOf doesn't interpret 'ufo' and 'ttf'
        # folders as extensions, maybe even check if folder.
        extension = None

        if '.' in fileName:
            extension = TX.extensionOf(fileName).lower()

        if extension is None:
            return

        if extension == 'ufo':

                if useRoboFont:
                    # NOTE: RoboFont embedded fontParts seems to have a diffent signature now,
                    # using mojo OpenFont instead for now.
                    from mojo.roboFont import OpenFont
                    style = OpenFont(path, showInterface=False)
                    msg = 'familyStorage.getStyle(): opened %s with mojo OpenFont' % path
                    logger.info(msg)
                else:
                    from fontParts.world import OpenFont
                    style = OpenFont(path, showInterface=False)
                    msg = 'familyStorage.getStyle(): opened %s with fontParts OpenFont' % path
                    logger.info(msg)


        # Returns style for OpenType fonts outside RoboFont.
        if style is None and os.path.exists(path):
            try:
                style = Style(path)
                logger.info('familyStorage.getStyle(): opened Style %s', path)
            except Exception as e:
                logger.error('Error opening Style %s' % path)
                logger.error(e)
                logger.error(traceback.format_exc())

        if style is None:
            raise TypeError('familyStorage.getStyle(): can\'t make Style %s' % path)

        return style

    def getStyleIDs(self, filter=None):
        """Answer the ordered list of styleIDs stored in self.styleIDsOrder
        (from file name). To make sure that the list is consistent with the
        current set of styles in the family and to maintain the current
        order, it is cross-references against the result of self.getStyleIDs().
        If styles no longer exist, they are removed from the ordered list. If
        there are new styles they are added at the end of the ordered list."""
        styleIDs = []

        if filter is None:
            filter = 'ufo', 'ttf', 'otf'

        familyDir = TX.path2FamilyDir(self.path)

        for fileName in os.listdir(familyDir):
            if fileName.startswith('.'):
                continue

            # TODO: make sure extensionOf doesn't interpret 'ufo' and 'ttf'
            # folders as extensions, maybe even check if folder.
            extension = None

            fileName = fileName.split('/')[-1]

            if '.' in fileName:
                extension = TX.extensionOf(fileName).lower()

            if extension in filter:
                styleIDs.append(fileName)

        # Now cross-check against the ordered list in the pack.
        self.verifyPack()
        sortedStyleIDs = self.pack[self.PACKKEY_SORTEDSTYLEIDS]

        if not sortedStyleIDs:
            # Get styleIDs from the storage and order alphabetically.
            self.pack[self.PACKKEY_SORTEDSTYLEIDS] = sortedStyleIDs = sorted(styleIDs)
        else:
            checkedStyleIDs = []

            # Otherwise check the existence of the ordered styleIDs against the
            # styles in storage.
            for styleID in sortedStyleIDs:
                if styleID in styleIDs:
                    checkedStyleIDs.append(styleID)

            # Check if there are styles not yet in the ordered list. Add them at the end.
            for styleID in styleIDs:
                if not styleID in sortedStyleIDs:
                    checkedStyleIDs.append(styleID)
            self.pack[self.PACKKEY_SORTEDSTYLEIDS] = sortedStyleIDs = checkedStyleIDs

        return sortedStyleIDs # Answer the checked ordered list.

    def setSortedStyleIDs(self, sortedStyleIDs):
        """Store the sortedStyleIDs in the pack. The validity of the list
        (checked against available styles) is tested on retrieval by
        self.getStyleIDs()."""
        self.pack[self.PACKKEY_SORTEDSTYLEIDS] = sortedStyleIDs
        self.verifyPack()

    # Preferences.

def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
