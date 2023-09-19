# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    family.py
#

import os
import os.path
import traceback
import logging
import datetime

from tnbits.base.constants.sorting import *
from tnbits.base.constants.tool import ANY
from tnbits.model.storage.basestorage import getStorage
from tnbits.model.objects.designspace import DesignSpace
from tnbits.model.objects.style import (nakedStyle, getStyleKey, isItalic,
        getRomanStyleKey, getItalicStyleKey)
from tnbits.toolbox.transformer import TX

logger = logging.getLogger(__name__)

class Family(object):
    """The *Family* binds a set of related style instances and design spaces,
    inside a folder of font files. All metadata is stored in the .fam file.

    TODO: add open / close notifications.

    >>> from tnTestFonts import getFontPath
    >>> name = "Condor-Bold.ufo"
    >>> path = getFontPath(name)
    >>> familyName = TX.path2FamilyName(path)
    >>> familyName
    'Condor'
    >>> styleID = TX.path2FileName(path)
    >>> styleID # Unique identifier of the style inside the family folder.
    'Condor-Bold.ufo'
    >>> familyDir = TX.path2FamilyDir(path)
    >>> family = Family(familyName, familyDir + '/Condor.fam')
    >>> len(family.storage.getStyleIDs())
    2
    >>> roman = family['Roman']
    >>> roman.asInstance(styleID) # Define this style as instance
    >>> roman.isMaster(styleID), roman.isInstance(styleID)
    (False, True)
    >>> roman.asMaster(styleID) # Define this style as master
    >>> roman.isMaster(styleID), roman.isInstance(styleID)
    (True, False)
    >>> roman.addAxis('Weight', 'wght', 0, 1000)
    >>> roman.addAxis('Width', 'wdth', 0, 1000)
    >>> roman.setStyleInterpolationAxis(styleID, 'Weight', 200)
    >>> roman.interpolations # Answer the full dict of style-axis-value relations
    {'Condor-Bold.ufo': {'Weight': 200}}
    >>> roman.interpolations[styleID]
    {'Weight': 200}
    >>> roman.interpolations[styleID]['Weight']
    200
    >>> roman.generate()
    {}
    >>> family.save()

    Format of family.json
    {
      "sortedStyleIDs": [],
      "lib": {},
      "designSpaces": {
        "Italic": {
          "axes": {},
          "instances": [
            "Promise-Medium_Italic.ufo"
          ],
          "interpolations": {
            "Promise-BoldCompressed_Italic.ufo": {},
            "Promise-Bold_Italic.ufo": {},
            "Promise-Medium_Italic.ufo": {},
            "Promise-UltraLightCompressed_Italic.ufo": {},
            "Promise-UltraLight_Italic.ufo": {}
          },
          "landingPatterns": {},
          "locked": [],
          "masters": [
            "Promise-BoldCompressed_Italic.ufo",
            "Promise-UltraLightCompressed_Italic.ufo",
            "Promise-UltraLight_Italic.ufo",
            "Promise-Bold_Italic.ufo"
          ],
          "name": "Italic",
          "sortedAxes": []
        },
        "Roman": {
            ...
        }
    }

    See also designspace.py.
    """

    def __init__(self, name, familyID, useRoboFont=True, hasPreferences=False):
        assert familyID
        self.name = name

        # Unique path of the family.fam file, while it is open.
        # familyID can be a path of a database identifier.
        self.familyID = familyID
        self.useRoboFont = useRoboFont
        self.hasPreferences = hasPreferences
        self.storage = getStorage(familyID)

        # Caching of styles once they are read from the storage.
        # Key is styleKey tuple.
        self.styles = {}
        self.lastModified = {}

        # Get info pack from data storage.
        pack = self.storage.getPack()

        # Initialize the internal DesignSpace instances.
        self.designSpaces = {}
        designSpacesPack = pack[self.storage.PACKKEY_DESIGNSPACES]

        for cName, cPack in designSpacesPack.items():
            self.designSpaces[cName] = DesignSpace(cName, cPack, self)

        # Checks if design spaces are defined, else creates the default.
        for name in self.storage.DEFAULT_DESIGNSPACES:
            if not name in self.designSpaces:
                self.designSpaces[name] = DesignSpace(name, {}, self)

        self.preferences = pack[self.storage.PACKKEY_PREFERENCES]
        self.save()
        self.dirty = False


    def __getitem__(self, cName):
        if cName == ANY:
            return

        return self.designSpaces[cName]

    def __contains__(self, cName):
        return cName in self.designSpaces

    def __len__(self):
        """Answers the number of design spaces."""
        return len(self.designSpaces)

    def keys(self):
        return self.designSpaces.keys()

    def __iter__(self):
        return iter(self.designSpaces)

    def __repr__(self):
        return '[%s name:%s]' % (self.__class__.__name__, self.name)

    def _get_dirty(self):
        return self._dirty

    def _set_dirty(self, value):
        self._dirty = value

    dirty = property(_get_dirty, _set_dirty)

    def isDirty(self):
        return self.dirty

    def save(self, path=None):
        """Saves the family to a <familyName>.json file in the current folder.
        If self.storage.path is None, then path must be defined as valid
        <familyName>.json path. Save all the styles in this family if they are
        open. Makes sure that if path is defined, it can only save in the same
        directory as the original. (otherwise we need to copy the fonts
        too?)"""
        # Get the verified pack from storage.
        pack = self.storage.getPack()

        # Creates a new design space dictionary for converted DesignSpace
        # instances output.
        designSpacesPack = {}

        for cName, designSpace in self.designSpaces.items():
            # Add converted DesignSpace instances.
            designSpacesPack[cName] = designSpace.getPack()

        preferencesPack = {}

        for toolName, preferences in self.preferences.items():
            preferencesPack[toolName] = preferences

        # Store converted designSpaces.
        pack[self.storage.PACKKEY_DESIGNSPACES] = designSpacesPack
        pack[self.storage.PACKKEY_PREFERENCES] = preferencesPack

        # Set pack and let verification run.
        self.storage.setPack(pack)
        self.storage.save(path)
        self.dirty = False
        logger.info('Saved %s' % self.name)

    # Style management.

    def saveStyles(self):
        """Saves the styles that are currently open."""
        for style in self.styles.values():
            style.save()

    def getStyle(self, styleKey):
        """Answers the cached style. If it is not open yet, then reads it from
        the storage first. Note that it is possible to open and cache a style
        (in the same folder as the family file) that is neither a master nor
        instance in one of the design spaces."""
        self.validateStyleKey(styleKey)
        updated = self.updateRFonts()

        # Creates a new style object if it doesn't exist yet.
        if not styleKey in updated and not styleKey in self.styles:
            self.openStyle(styleKey)

        return self.styles[styleKey]

    def openStyle(self, styleKey):
        path = TX.path2FamilyDir(styleKey[0]) + '/' + styleKey[1]
        self.styles[styleKey] = self.storage.getStyle(path, useRoboFont=self.useRoboFont)
        self.setLastModified(styleKey, path)

    def setLastModified(self, styleKey, path):
        mod_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        self.lastModified[styleKey] = mod_timestamp

    def getRelatedStyleKey(self, styleKey):
        if isItalic(styleKey):
            styleKey = getRomanStyleKey(styleKey)
        else:
            styleKey = getItalicStyleKey(styleKey)
        return styleKey

    def getRelatedStyle(self, style):
        """Try to guess if there is a related style to the current style that
        has useful values to show. E.g. as is the case with Roman-Italic."""
        # TODO: load font if not in fam yet.
        styleKey = getStyleKey(style)
        relatedStyleKey = self.getRelatedStyleKey(styleKey)

        if relatedStyleKey in self.styles:
                return self.styles[relatedStyleKey]
        else:
            path = TX.path2FamilyDir(relatedStyleKey[0]) + '/' + relatedStyleKey[1]

            if os.path.exists(path):
                return self.getStyle(relatedStyleKey)

    def updateRFonts(self):
        """Checks if the family still holds the same naked fonts compared to
        the ones currently loaded in RoboFont; it can happen that RoboFont
        closed a font and then reopens it, which causes the font to be loaded
        as a different naked instance than the one contained in the family.
        After calling the update, the styles in the family and enclosed design
        spaces will be changed to refer to the RoboFont styles (the other way
        around is not possible)."""
        updated = []

        if self.useRoboFont:
            # Does a quick scan to make sure that we still refer to the same
            # styles as RoboFont.
            from mojo.roboFont import AllFonts

            # Checks if this font is in the same directory as self but not opened
            # yet in the family.
            for rFont in AllFonts():
                if not self.checkRFont(rFont):
                    continue

                rfFamDir = TX.path2FamilyDir(rFont.path)
                famDir = TX.path2FamilyDir(self.familyID)

                # Same folder, same family.
                if rFont.path is not None and rfFamDir == famDir:
                    styleKey = self.updateRFont(rFont)
                    updated.append(styleKey)
        else:
            zero = datetime.timedelta(0)

            for styleKey in self.styles:
                style = self.styles[styleKey]
                lastModified = self.lastModified[styleKey]
                mod_timestamp_new = datetime.datetime.fromtimestamp(os.path.getmtime(style.path))
                td = lastModified - mod_timestamp_new

                if td != zero:
                    logger.info('Reloading %s' % styleKey[-1])
                    self.openStyle(styleKey)
                    updated.append(styleKey)

        return updated

    def updateRFont(self, rFont):
        """Updates reference to a single RFont after opening it in RoboFont.
        Returns an empty list if not in RoboFont."""
        if not self.useRoboFont:
            return

        styleKey = TX.path2StyleKey(rFont.path)

        if not styleKey in self.styles:
            self.styles[styleKey] = rFont
            self.setLastModified(styleKey, rFont.path)
            logger.info('family.updateRFont(): added RoboFont style %s' % rFont.path)
        elif self.styles[styleKey] != rFont:
            style = self.styles[styleKey]

            # Save the smartLibs tree or else it will disappear without
            # original style.
            if hasattr(style, '_tnSmartLibs'):
                #if not hasattr(rFont, '_tnSmartLibs'):
                setattr(rFont,'_tnSmartLibs', style._tnSmartLibs)
                #rfStyle._tnSmartLibs = style._tnSmartLibs

            self.styles[styleKey] = rFont
            self.setLastModified(styleKey, rFont.path)
            logger.info('family.updateRFont(): updated %s' % rFont.path)

        return styleKey

    def checkRFont(self, rfStyle):
        assert rfStyle is not None

        if not hasattr(rfStyle, 'path'):
            # FIXME: Happens with TTF / OTF, maybe use something other than path?
            msg = '* family.checkRFont(): no path for %s (skipping)' % rfStyle
            logger.error(msg)
            return False

        if rfStyle.path is None:
            # Ignore, can be new untitled font.
            return False

        return True

    def validateStyleKey(self, styleKey):
        """Test the format validity of the styleKey. For normal styles it has
        format ('familyPath', 'styleName'), but e.g. for the virtual dragging
        font in Interpolator it can have format ('', styleID), as long as the
        resulting tuple is unique."""
        try:
            assert isinstance(styleKey, (list, tuple))
        except AssertionError as e:
            logger.error('* family.validateStyleKey(): error -- not a list or tuple', styleKey)
            return False

        try:
            assert len(styleKey) == 2
        except AssertionError as e:
            logger.error('!!! Length not 2', styleKey)
            return False

        try:
            assert styleKey[0].endswith('.fam')
        except AssertionError as e:
            logger.error('!!! family identifier not a .fam file', styleKey)
            return False

        return True

    def styleIsOpen(self, styleKey):
        """Answers if the styleKey is already open in memory. This method can be
        used to avoid time consuming opening during drag or to open a progress
        window."""
        self.validateStyleKey(styleKey)
        return styleKey in self.styles

    def pushStyle(self, style):
        """In case RoboFont opened the same style (but different instance)
        than we already have open, this method will put this new style on the
        position. The method typically is called in a FONTWILLOPEN call
        back."""
        styleKey = getStyleKey(style)

        # It's already open, make sure to save and remove the old one from
        # storage.
        if styleKey in self.styles:
            self.styles[styleKey].save() # Save and close the old style.

        self.styles[styleKey] = nakedStyle(style) # Set the new style instance.
        #self.lastModified[styleKey] = os.stat(style.path)
        self.dirty = True

    def addStyle(self, style):
        """The application may have create a new font file that is not in the
        family yet. Checks if the style is in the same directory as the style,
        and then adds it to the family. Ignores if the style is already open.
        This makes this method different from self.pushStyle."""
        styleKey = getStyleKey(style)
        self.addStyleKey(styleKey)
        # Answers the styleKey for convenience of the caller.
        return styleKey

    def removeStyle(self, style):
        styleKey = getStyleKey(style)
        del self.styles[styleKey]
        del self.lastModified[styleKey]
        logger.info('Removed %s, %s' % styleKey)

    def addStyleKey(self, styleKey):
        """Add the styleKey if not already there. Answers the stykeKey for
        convenience of the caller."""
        if not styleKey in self.styles:
            style = self.getStyle(styleKey)

            if style is not None:
                # Set the new style instance.
                self.styles[styleKey] = nakedStyle(style)
                #self.lastModified[styleKey] = os.stat(style.path)
                self.dirty = True

        return styleKey

    def getStyles(self):
        """Answers all open styles."""
        return self.styles

    def getStyleKeys(self):
        """Answers the list with key tuples if format (familyPath, fileName) in
        the stored order. A styleID is the styleKey[1] part, defined by the
        UFO file name of the style. We don't want to store the family path in
        the family.fam file, so only the styleID is stored."""
        styleKeys = []
        for styleID in self.getStyleIDs():
            styleKey = self.familyID, styleID
            self.validateStyleKey(styleKey)
            styleKeys.append(styleKey)
        return styleKeys

    def setStyleKeys(self, styleKeys):
        """Save the styleID order in family storage. A styleID is the
        styleKey[1] part, defined by the UFO file name of the style. We don't
        want to store the family path in the family.fam file, so only the
        styleID is stored."""
        styleIDs = []
        for _, styleID in styleKeys:
            styleIDs.append(styleID)
        self.setStyleIDs(styleIDs)

    def getDecoratedStyleNames(self):
        """Answers the list of style names in the order of self.getStyleIDs().
        Derived from the TX.path2StyleName(styleID) path.
        Adds a marker if the style is a master."""
        decoratedStyleNames = []
        for styleID in self.getStyleIDs():
            decoratedName = TX.path2FileName(styleID).replace('_',' ').replace('.ufo','')
            if self.isMaster(styleID):
                decoratedName += ' [M]'
            decoratedStyleNames.append(decoratedName)
        return decoratedStyleNames

    def getStyleNames(self):
        """Answers the list of style names in the order of self.getStyleIDs().
        Derived from the path name, not from style.info.styleName for speed (we
        don't want to open all font files to make this list."""
        styleNames = []
        for styleID in self.getStyleIDs():
            styleNames.append(TX.path2StyleName(styleID))
        return styleNames

    def getStyleIDs(self):
        """Answers the updated ordered list of all family fileNames in this
        family folder, checking the actual font files against the
        self.storage.sortedStyleIDs list. These fonts are not necessarily
        opened in one of the design spaces (yet) or previously part of any
        relation with the family. It's just a list of any styleID that can be
        found in the scope of the family folder or database. The order is
        derived from alphabetic sorted or what is stored as sorted list through
        self.setStyleIDs()"""
        return self.storage.getStyleIDs()

    def getStyleKeyIndex(self, styleKey):
        """Gets the index `i` from the style keys order of the style key
        exists."""
        for i, key in enumerate(self.getStyleKeys()):
            if styleKey == key:
                return i

    def setStyleIDs(self, styleIDs):
        """Stores the ordered list of file names for this family. The list will
        be checked against validity with the real styles upon retrieval. The
        list is stored in the pack. It is used to maintain the right order of
        styleIDs, which is answered by self.getStyleIDs(), e.g. as draggable
        list in the Builder style list.

        styleIDs has format:

            [(familyPath, 'Profile-Bold.ufo'), (familyPath, 'Profile-Medium.ufo')]

        fileNames has format:

            ('Profile-Bold.ufo', 'Profile-Medium')

        so it can be stored in the family.fam storage JSON.
        """
        self.storage.setSortedStyleIDs(styleIDs)
        #TODO: send notification to tools that need to know about styles order.
        self.dirty = True

    def newStyle(self, styleType='ufo', showUI=False):
        """Create a new style. Default is UFO. Setting the showUI flag to True
        opens a RoboFont font window."""
        style = None

        if styleType == 'ufo':
            from mojo.roboFont import NewFont
            style = nakedStyle(NewFont(showUI=showUI))
            style.setParent(self)
            style.info.familyName = self.name
            style.info.styleName = 'NoStyle'
            self.pushStyle(style)
        else:
            raise TypeError('[Family.newStyle] Cannot create style of type "%s"' % styleType)

        return style

    def makeTempStyleKey(self, styleType='ufo', styleName='TempStyle', descender=None):
        """Makes a temporary style (for internal use in a tool), that will not
        be part of the Master / Instance list and will not ask for saving on
        closing the application or tool. Answers the style key. The styleName
        argument defines the style.info.styleName of the new tmp font, so it
        can be identified by the caller."""
        tmpStyle = self.newStyle(styleType=styleType)
        # Identifier for temp styles.
        tmpStyle.info.styleName = styleName

        if descender is not None:
            # Optionally syncs baseline with other family styles.
            tmpStyle.info.descender = descender

        return getStyleKey(tmpStyle)

    # Design spaces.

    def getDesignSpace(self, name):
        """Answers the named design space. Answers None if it does not
        exist."""
        return self.designSpaces.get(name)

    def getDesignSpacesOfStyle(self, styleKey):
        """Answers the design spaces that use styleKey as master or instance."""
        designSpaces = []
        for c in self.designSpaces.values():
            if c.hasStyle(styleKey):
                designSpaces.append(c)
        return designSpaces

    def getMasterKeysOfStyle(self, styleKey):
        """Answers the total set of master keys that have an interpolation
        relation through any of the family design spaces."""
        masterKeys = set()
        for c in self.designSpaces.values():
            if not c.hasStyle(styleKey):
                continue
            masterKeys = masterKeys.union(set(c.masters))
        return masterKeys

    def getMasterKeys(self):
        """Answers the set of all style keys that are used as Master"""
        masterKeys = set()
        for styleKey in self.getStyleKeys():
            for c in self.designSpaces.values():
                if c.isMaster(styleKey):
                    masterKeys.add(styleKey)
                    continue
        return masterKeys

    def getInstanceKeys(self):
        """Answers the set of all style keys that are used as Instance"""
        instanceKeys = set()
        for styleKey in self.getStyleKeys():
            for c in self.designSpaces.values():
                if c.isInstance(styleKey):
                    instanceKeys.add(styleKey)
                    continue
        return instanceKeys

    def getDesignSpacesOfInstance(self, styleKey):
        """Answers the design spaces that use styleKey as instance."""
        designSpaces = []
        for designSpace in self.designSpaces.values():
            if designSpace.isInstance(styleKey):
                designSpaces.append(designSpace)
        return designSpaces

    def getDesignSpacesOfMaster(self, styleKey):
        """Answers the design spaces that use styleKey as master."""
        designSpaces = []
        for designSpace in self.designSpaces.values():
            if designSpace.isMaster(styleKey):
                designSpaces.append(designSpace)
        return designSpaces

    def isMaster(self, styleID):
        """Answers if the font indicated by styleID is master
        in one of the design spaces."""
        for designSpace in self.designSpaces.values():
            if designSpace.isMaster(styleID):
                return True
        return False

    def isInstance(self, styleID):
        """Answers if the font indicated by styleID is
        instance in one of the design spaces."""
        for designSpace in self.designSpaces.values():
            if designSpace.isInstance(styleID):
                return True
        return False

    def getPath(self):
        p = self.familyID
        p = '/'.join(p.split('/')[:-1])
        return p

    def addDesignSpace(self, name):
        assert self.getDesignSpace(name) is None
        self.designSpaces[name] = DesignSpace(name, {}, self)
        logger.info('Added %s to %s' % (name, self.name))
        self.save()

    def removeDesignSpace(self, name):
        if name in self.designSpaces:
            self.designSpaces.pop(name)
            logger.warning('Removed %s from %s' % (name, self.name))

        self.save()

    def getSortedDesignSpaceNames(self):
        designSpaces = []
        keys = self.keys()

        if 'Roman' in keys:
            designSpaces.append('Roman')
        if 'Italic' in keys:
            designSpaces.append('Italic')

        for k in keys:
            if k != 'Roman' and k != 'Italic':
                designSpaces.append(k)

        return designSpaces

    def getFirstName(self):
        l = self.getSortedDesignSpaceNames()

        if len(l) > 0:
            return l[0]

    # Sorting.

    def sort(self, verbose=False):
        """For now sorts weights and widths.
        TODO: make recursive and add optical size, slope, serif."""
        d = {}

        for styleID in self.getStyleIDs():
            # Get descriptors from substring after the hyphen.
            name = '.'.join(styleID.split('.')[:-1])
            description = name.split('-')[-1]
            parts = description.split('_')

            # Add the styleID to the dictionary.
            self.getWeight(styleID, parts, d)

        if verbose:
            for key, value in d.items():
                logger.info(key)
                for k, v in value.items():
                    logger.info('\t%s: %s' % (k, v))

        styleIDs = self.sortCollected(d, verbose=verbose)
        self.setStyleIDs(styleIDs)
        self.save()

    def compareWeight(self, part):
        """See if part equals one of the weight qualifiers."""
        for weight in SORTWEIGHTSORDER:
            synonyms = SORTWEIGHTS[weight]
            part = part.lower()

            # TODO: also check for substrings.
            # TODO: use difflib to find close matches..
            if part == weight or part in synonyms:
                return True, weight

        return False, None

    def getWeight(self, styleID, parts, d):
        """Adds styleID to the dictionary based on weight, width to be
        determined."""
        for i, part in enumerate(parts):
            match, weight = self.compareWeight(part)

            if match is True:

                # Backtracks 'extra' qualifier that has a space between
                # according to list order.
                # TODO: untested
                if weight in ('light', 'bold', 'black'):
                    if i > 0 and parts[i-1].lower() == 'extra':
                        weight = 'extra' + weight

                # Add to dictionary if not already there.
                if weight not in d:
                    d[weight] = {}

                parts.remove(part)
                self.getWidth(styleID, weight, parts, d)
                return

        # No match.
        if 'None' not in d:
            d['None'] = {}

        # Finally, get the ones without a detected weight.
        self.getWidth(styleID, 'None', parts, d)
        return

    def compareWidth(self, part):
        """See if part equals one of the width qualifiers."""
        for width in SORTWIDTHSORDER:
            synonyms = SORTWIDTHS[width]
            part = part.lower()

            # TODO: also check for substrings.
            # TODO: use difflib to find close matches..
            if part == width or part in synonyms:
                return True, width

        return False, None

    def getWidth(self, styleID, weight, parts, d):
        """
        """
        for i, part in enumerate(parts):
            match, width = self.compareWidth(part)

            if match is True:
                # Backtracks 'extra' qualifier that has a space between
                # according to list order.
                # TODO: untested
                if width in ('compressed', 'condensed'):
                    if i > 0 and parts[i-1].lower() == 'extra':
                        width = 'extra' + width

                if width not in d[weight]:
                    d[weight][width] = []
                d[weight][width].append(styleID)

                parts.remove(part)
                return

        # No match.
        if 'None' not in d[weight]:
            d[weight]['None'] = []

        d[weight]['None'].append(styleID)
        return

    def sortCollected(self, d, verbose=False):
        """
        Sorts weight first, then width.
        """
        order = []
        unsorted = []

        for weight in SORTWEIGHTSORDER:
            if weight in d:
                for width in SORTWIDTHSORDER:
                    if width in d[weight]:
                        styleIDs = d[weight][width]

                        # For now sort same widths alphabetically.
                        # TODO: sort by slope, optical size, (sans) serif.
                        order.extend(sorted(styleIDs))

        return order

    # Preferences.

    def setPreference(self, toolName, key, value):
        """Adds the value and optionally key to the preferences dictionary for
        the tool."""
        if not toolName in self.preferences:
            self.preferences[toolName] = {}

        self.preferences[toolName][key] = value
        #self.save()

    def getPreference(self, toolName, key, default=None, forceDefault=False):
        """Gets the preference value if it exists, else returns the default."""
        if forceDefault:
            return default
        elif not toolName in self.preferences:
            return default
        elif not key in self.preferences[toolName]:
            return default

        return self.preferences[toolName][key]
