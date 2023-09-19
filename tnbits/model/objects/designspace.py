# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    designspace.py
#
#    D E P R E C A T E D
#    To be merged with dsmodel.DesignSpace


import os, re
import weakref
from tnbits.model.objects.style import Style, verifyStyleKey, getStyleKey
from tnbits.toolbox.transformer import TX
from tnbits.errors.designspaceerror import DesignSpaceError
import logging
logger = logging.getLogger(__name__)

try:
    from fontTools.designspaceLib import DesignSpaceDocument
except:
    import fontTools
    print('Can\'t find FontTools designspaceLib, version is %s' % fontTools.__version__)

class DesignSpace(object):
    """
    Internal format of design spaces dictionary
    self.designSpaces = {
        'Roman': { # Design space level "Roman"
            'instances': [<styleID1>, <styleID2>, ...],
            'masters': [<styleID3>, <styleID4>, ...],
            'locked': [<styleID1>, <styleID2>, ...],
            'disabled': [styleID2>, <styleID4>, ...],
            'axes': {
                'Weight': {enabled: True, 'minValue': 0, 'maxValue': 1000},
                'Width': {enabled: True, 'minValue': 0, 'maxValue': 1000),
                'Size': {enabled: False, 'minValue': 8, 'maxValue': 24),
                ...
            }
            'sortedAxes': ['Width', 'Weight', 'Size', ...], # Preferred order, independent if axis is enabled.
            'interpolation': {
                <styleID1>: {'Weight': 200, 'Width': 400', 'Size': 10, ...},
                <styleID2>: {'Weight': 100, 'Width': 0', ...},
                ...
            },
        }
        'Italic': { # Design space level "Italic"
            ...
        }
    }

    Implements design space to be used to generate variation fonts.
    >>> from tnTestFonts import getFontPath
    >>> from tnbits.model.objects.family import Family
    >>> name = "Condor-Bold.ufo"
    >>> path = getFontPath(name)
    >>> familyName = TX.path2FamilyName(path)
    >>> familyName
    'Condor'
    >>> styleKey = TX.path2StyleKey(path)
    >>> styleKey # Unique identifier of the style inside the family folder.
    'Condor-Bold.ufo'
    >>> familyDir = TX.path2FamilyDir(path)
    >>> family = Family(familyName, familyDir + '/Condor.fam')
    >>> len(family.storage.getStyleKeys())
    2
    >>> style = family.getStyle(styleKey)
    >>> style
    >>> roman = family['Roman']
    >>> roman.asMaster(styleKey) # Define this style as master
    >>> roman.addAxis('Weight', 'wght', 0, 1000)
    >>> roman.getAvatarGlyphName('dollar', {'weight': 500})

    TODO: connect to logger.
    TODO: axis as separate class?
    """

    def __init__(self, name, cPack, parent):
        """Make the Constellation instance."""
        self.name = name
        self.parent = parent
        self.setPack(cPack)

        # Key: base glyph name.
        # Value: accumulated set of related avatar names from all masters.
        self._avatarNames = {}

    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None
    def _set_parent(self, parent):
        self._parent = weakref.ref(parent)
    parent = property(_get_parent, _set_parent)

    def _get_styles(self):
        return self.parent.getStyles()
    styles = property(_get_styles)

    def __repr__(self):
        return '[%s family:%s name:%s]' % (self.__class__.__name__,
                self.parent.name, self.name)

    def __getitem__(self, styleKey):
        assert verifyStyleKey(styleKey) # Check that we get a valid styleKey here.
        return self.parent.getStyle(styleKey)

    def __contains__(self, styleKey):
        assert verifyStyleKey(styleKey)
        return styleKey in self.styles

    def keys(self):
        return self.styles.keys()

    def __iter__(self):
        return iter(self.styles)

    '''
    def __len__(self):
        """Answers the number of styles in this design space."""
        return len(self.styles)
    '''

    def _get_familyID(self):
        """Used for constructing global styleKey from local styleID."""
        return self.parent.familyID

    familyID = property(_get_familyID)

    #   C O N V E R T E R S

    def _styleIDs2StyleKeys(self, styleIDs):
        """Converts the list of StyleIDs (single fileNames) to a list of
        styleKeys, tuples of (familyID, styleID)."""
        styleKeys = []
        for styleID in styleIDs:
            styleKeys.append((self.familyID, styleID))
        return styleKeys

    def _styleKeys2styleID(self, styleKeys):
        """Converts the list of styleKeys, tuples of (familyID, styleID), to
        styleIDs."""
        styleIDs = []
        for styleKey in styleKeys:
            styleIDs.append(styleKey[1])
        return styleIDs

    def _interpolationIds2InterpolationKeys(self, interpolationIds):
        """Converts the dictionary with interpolation styleIDs into a
        dictionary with styleKey as key."""
        interpolationKeys = {}
        for styleID, axes in interpolationIds.items():
            interpolationKeys[(self.familyID, styleID)] = axes
        return interpolationKeys

    def _interpolationKeys2InterpolationIds(self, interpolationKeys):
        """Converts the dictionary with interpolation styleKeys into a
        dictionary with styleID as key."""
        interpolationIds = {}
        for styleKey, axes in interpolationKeys.items():
            interpolationIds[styleKey[1]] = axes
        return interpolationIds

    #   P A C K S

    def clear(self):
        """Resets all constellation values. Mostly used when building a
        constellation by script."""
        self.origin = None
        self.masters = []
        self.instances = []
        self.locked = []
        self.disabled = []
        self.axes = {}
        self.sortedAxes = []
        self.interpolations = {}
        self.landingPatterns = {}

    def setPack(self, cPack):
        """Unpack into self attributes. If the entry does not exist in the
        pack, then make a default value. In case cPack is an empty dictionary,
        fill all attributes by default values.

        Example pack dictionary:

        ```
        {u'origin': None,
        u'masters': [u'Upgrade-Black.ufo', u'Upgrade-UltraThin_Italic.ufo',
            u'Upgrade-UltraBlack.ufo', u'Upgrade-Middle.ufo', u'Upgrade-Light.ufo'],
        u'interpolations':
            {u'Upgrade-Book.ufo': {u'Weight': 42},
            u'Upgrade-Middle.ufo': {u'Width': 0, u'Weight': 140, u'Size': 8},
            u'Upgrade-Light.ufo': {u'Width': 0, u'Weight': 32, u'Size': 8},
            u'Upgrade-Black.ufo': {u'Width': 0, u'Weight': 212, u'Size': 8},
            u'Upgrade-Thin.ttf': {},
            u'Upgrade-UltraThin_Italic.ufo': {u'Width': 0, u'Weight': 8, u'Size': 8},
            u'Upgrade-UltraBlack.ufo': {u'Width': u'', u'Weight': 276, u'Size': u''}},
        u'locked': [],
        u'name': u'Roman',
        u'axes': {
            u'Width': {u'minValue': 0, u'defaultValue': 0, u'enabled': False,
            u'maxValue': 1000, u'name': u'Width'},
            u'Weight': {u'minValue': 8, u'defaultValue': 8, u'enabled': True,
            u'maxValue': 276, u'name': u'Weight'},
            u'Size': {u'minValue': 8, u'defaultValue': 8, u'enabled': False,
            u'maxValue': 72, u'name': u'Size'}},
        u'disabled': [],
        u'instances': [u'Upgrade-Book.ufo', u'Upgrade-Thin.ttf'],
        u'sortedAxes': [u'Weight', u'Width', u'Size'],
        u'landingPatterns': {}}
        ```

        Example of an empty italic design space dictionary:

        ```
        {u'origin': None,
        u'masters': [],
        u'interpolations': {},
        u'locked': [],
        u'name': u'Italic',
        u'axes': {},
        u'disabled': [],
        u'instances': [],
        u'sortedAxes': [],
        u'landingPatterns': {}}
        ```
        """
        # Style ID of origin.
        self.origin = cPack.get('origin', None)

        # List of style ids (= file name or unique record id)
        # Key in storage is simple styleID, not styleKey
        self.masters = self._styleIDs2StyleKeys(cPack.get('masters',[]))

        # List of style ids (= file name or unique record id)
        # Key in storage is simple styleID, not styleKey
        self.instances = self._styleIDs2StyleKeys(cPack.get('instances', []))

        # Set of style ids that are locked (can be masters and instances)
        # Key in storage is simple styleID, not styleKey. Set of style ids that
        # are disabeled (can be masters and instances)
        self.locked = set(self._styleIDs2StyleKeys(cPack.get('locked', [])))

        '''
        Key in storage is simple styleID, not styleKey.  Keep independent from
        master list, so masters can be turned off, without losing their value
        on the axis. Note that asking for axis names, may only answer the names
        that actually have an active master attached to that axis name. Create
        dictionary of {<tag>: dict(minValue=0, maxValue=1000, enabled=True,
        ...)}
        '''
        self.disabled = set(self._styleIDs2StyleKeys(cPack.get('disabled', [])))

        # Keep the list of sorted axis names for the application UI, because
        # the axis dictionary has no order.
        axes = cPack.get('axes', {})
        axes = self.fixAxes(axes)
        self.axes = axes
        self.sortedAxes = cPack.get('sortedAxes', [])

        # Keep styles related interpolation values per axis.
        self.interpolations = self._interpolationIds2InterpolationKeys(cPack.get('interpolations', {}))

        # Keep landing pattern parameters here.
        self.landingPatterns = cPack.get('landingPatterns', {})

    def getPack(self):
        return dict(
            name=self.name,
            origin=self.origin,
            masters=self._styleKeys2styleID(self.masters), # Simple lists of styleIDs, not styleKeys.
            instances=self._styleKeys2styleID(self.instances),
            locked=self._styleKeys2styleID(self.locked),
            disabled=self._styleKeys2styleID(self.disabled),
            axes=self.axes,
            sortedAxes=self.sortedAxes,
            interpolations=self._interpolationKeys2InterpolationIds(self.interpolations),
            landingPatterns=self.landingPatterns
        )

    def save(self):
        """Saves the family to a <familyName>.json file in the current folder.
        If self.storage.path is None, then path must be defined as valid
        <familyName>.json path. Saves all the styles in this family if they are
        open."""
        self.parent.save()

    #   A X E S

    def clearAxes(self):
        """Clears the axis. Note that we keep the interpolation values, to
        remember the order if new axes are created, or if an axis is recreated
        later."""
        self.axes = {}
        self.sortedAxes = []

    def fixAxes(self, axes):
        """Quick fix to copy minimum value to missing default value.
        TODO: remove at a certain point.
        """
        for tag, axis in axes.items():
            if not u'defaultValue' in axis:
                axis['defaultValue'] = axis['minValue']

            if 'axis' in axis.keys():
                axis['name'] = axis['axis']
                del axis['axis']

        return axes

    def getAxisArg(self, axis, p, **kwargs):
        """Checks if keyword arguments contain parameter, else takes original
        value from axis."""
        if not p in kwargs:
            value = axis[p]
        else:
            value = kwargs[p]

        return value

    def checkFloorCeiling(self, d):
        """Floor / ceiling for axis values."""
        minValue = d['minValue']
        defaultValue = d['defaultValue']
        maxValue = d['maxValue']

        if minValue > defaultValue:
            minValue = defaultValue
        if defaultValue > maxValue:
            defaultValue = maxValue
        if maxValue < minValue:
            maxValue = minValue
        if defaultValue < minValue:
            defaultValue = minValue

        d['minValue'] = minValue
        d['defaultValue'] = defaultValue
        d['maxValue'] = maxValue

        return d

    def setAxis(self, tag, **kwargs):
        """Gets axis by unique tag and updates values while checking floor /
        ceiling for values."""
        axis = self.getAxis(tag)
        d = {}

        for p in ['name', 'minValue', 'defaultValue', 'maxValue']:
            d[p] = self.getAxisArg(axis, p, **kwargs)

        d = self.checkFloorCeiling(d)

        for key, value in d.items():
            axis[key] = value

    def isAxisEnabled(self, tag):
        axis = self.getAxis(tag)
        return axis.get('enabled')

    def setAxisEnabled(self, tag, enabled):
        axis = self.getAxis(tag)
        if axis is not None:
            axis['enabled'] = enabled

    def getEnabledSortedAxes(self):
        """Answers the list of enabled axes in the order of self.sortedAxes."""
        axes = []

        for tag in self.sortedAxes:
            axis = self.axes.get(tag) # Make it robust, in case an axis is missing.

            if axis is not None and axis.get('enabled', False):
                axes.append(axis)

        return axes

    def getEnabledSortedAxisTags(self):
        """Answers the list of enabled axis names in the order of
        self.sortedAxes."""
        tags = []

        for tag in self.sortedAxes:
            axis = self.axes.get(tag) # Make it robust, in case an axis is missing.

            if axis is not None and axis.get('enabled', False):
                tags.append(tag)

        return tags

    def getAxis(self, tag):
        return self.axes[tag]

    def getAxisValue(self, tag, key):
        axis = self.getAxis(tag)
        return axis[key]

    def getAxisByName(self, name):
        axes = self.getAxes()

        for tag, axis in self.getAxes().items():
            if axis['name'] == name:
                return tag, axis

    def getAxes(self):
        """Answers the dictionary with axes, where the axis names are key."""
        return self.axes

    def getActiveAxes(self):
        """Answers the list with axes where the enabled flag is set, in order
        of self.sortedAxes."""
        activeAxes = []

        for tag in self.sortedAxes:
            axis = self.axes[tag]

            if axis['enabled']:
                activeAxes.append(axis)

        return activeAxes

    def getSortedAxes(self):
        """Answers the list with axes in order of self.sortedAxes."""
        activeAxes = []

        for tag in self.sortedAxes:
            activeAxes.append(self.axes[tag])

        return activeAxes

    def getAxisTags(self):
        """Answers a set of all unique axis tags that are in self.sortedAxes
        and self.axes, not matter if they are enabled or disabled."""
        tags = []

        for tag in self.sortedAxes:
            if tag in self.axes:
                tags.append(tag)

        return tags

    def getActiveAxisNames(self):
        """Answers the list with names of the active axes."""
        tags = []

        for tag in self.sortedAxes:

            if tag in self.axes and self.axes[tag]['enabled']:
                tags.append(tag)

        return tags

    def checkType(self, value):
        """Makes sure value is of correct type. TODO: move to a TX."""
        if value is None:
            return

        value = str(value)

        try:
            value = float(value)
            if value % 1 == 0:
                value = int(value)
        except:
            # It's a plain string.
            pass

        return value

    def addAxis(self, tag, name, minValue, maxValue, defaultValue=None, enabled=True):
        """Adds the axis to self, and add to the sortedAxes if it does not
        already exist. Also add it to the interpolations if it is not there
        already, with default value minValue."""
        minValue = self.checkType(minValue)
        defaultValue = self.checkType(defaultValue)
        maxValue = self.checkType(maxValue)

        if defaultValue is None:
            defaultValue = minValue

        # FIXME: Assert exists or open dialog before overwrite?
        if tag in self.axes:
            logger.error('Axis %s already exists in %s' % (tag, self.name))
            return

        self.axes[tag] = dict(name=name, minValue=minValue, maxValue=maxValue,
                defaultValue=defaultValue, enabled=enabled)

        tags = self.getAxisTags()

        # Not there yet, add it at the end of the sorted axis name
        # list.
        if not tag in tags:
            self.sortedAxes.append(tag)

        for interpolation in self.interpolations.values():
            if not tag in interpolation:
                interpolation[tag] = minValue

        logger.info('Added axis %s to %s' % (tag, self.name))

    def deleteAxis(self, tag):
        """Deletes the axis from the list of axis names, but keeps it in the
        style list. Note that the axis references are not delete from the
        styleKey interpolation, because we may want that information again,
        once an axis is restored."""
        if tag in self.axes:
            del self.axes[tag]
            logger.warning('Removed axis %s from %s' % (tag, self.name))

        # Delete all of these names from the list.
        while tag in self.sortedAxes:
            self.sortedAxes.remove(tag)

    def getAxisByIndex(self, index):
        """Answers the axis data, indicated by the index of self.sortedAxes.
        Answer None if the index is out of bounds."""
        if index < len(self.sortedAxes):
            return self.axes[self.sortedAxes[index]]

    def setAxisByIndex(self, index, axis):
        """Sets the axis indicated by the index of self.sortedAxis. The axis
        attribute needs to the same formatted object as available under
        self.axis[tag]."""
        if index < len(self.sortedAxes):
            self.axes[self.sortedAxes[index]] = axis

    #   I N S T A N C E S

    def makeStyle(self, styleKey):
        """Makes style take an instance or master and copies that into a
        style. After that several preparation are done, in order to export the font
        as file:
        - Copy
        - Swapping all avatar glyphs into their real glyph slots
        - Swapping all avatar glyhps special kerning pairs, if they exist.
        - Apply landing pattern
        - Validation
        """
        # TODO: Make this work
        pass

    #   A V A T A R

    AVATARAXISVALUESPLIT = re.compile('([a-zA-Z]+)([0-9]+)')

    def clearAvatarGlyphNameCache(self, glyphName):
        """Clear the avatar name cache for this glyph if it exists. Needs to
        be called if one of the masters changed added/deleted avatar glyphs with
        this base name."""
        if glyphName in self._avatarNames:
            del self._avatarNames[glyphName]

    def _getAvatarGlyphNames(self, glyphName):
        """Answers the cached avatar glyph names for glyphName. Scan the
        masters for avatar glyph names if the cache does not exist and cache
        the result."""
        if not glyphName in self._avatarNames:
            # Find all glyphs that have a matching name and their axis value.
            # And available in each master.
            self._avatarNames[glyphName] = set()
            for master in self.getMasters():
                for g in master:
                    # Find all glyphs that have a matching name and their axis
                    # value. And available in each master.
                    nameParts = g.name.split('.')
                    if glyphName == nameParts[0]:
                        self._avatarNames[glyphName].add(g.name)
        return self._avatarNames[glyphName]

    def getAvatarGlyphNames(self, glyphName, position):
        """Answers the avatar glyph name in the specified axes position,
        depending on what avatar glyphs are available in the constellation
        masters. Depending on the availability of avatar named glyphs, they
        play a role in interpolation between two masters.

        dollar # Runs from 0 and up
        dollar.weight600 # Runs from 600 and up. Glyph exists in Thin and Bold
        dollar.weight800 # Runs from 800 and up. Glyph exists in Thin and Bold
        Weight = 100 -> Normal interpolation
        Weight = 650 -> dollar.weight600 interpolation overrules normal interpolation
        Weight = 850 -> dollar.weight800 interpolation overrules 600+ interpolation.

        This method can figure out the order, so there is no need to add 2
        values as range to the name.  Keeping the axis+value in the glyph name,
        makes it not necessary to keep separate data in the family. Note that
        changing the transition position will then rename the glyphs.

        Just keeping the bottom value (main glyph value default to 0, to it is
        not in the name), makes it more flexible to add in others above and
        below. The relation is dynamic to which other glyphs are available in
        the Masters. If there is no valid avatar combinations in the relevant
        masters, given a set of axes, then the untranslated glyphName is
        answered. The caller can check if the names are equal, to decide if
        glyph swapping is needed, in case of interpolating instances are
        exported to fonts.

        Avatar-extension is behind the last ".", e.g. g.earless.weight600, as
        they can easily be truncated for their real glyph names in exporting
        instances."""
        # Make sure to take base name, in case we already got an avatar name
        # here. Initialize the found values, so the axis minValue is default.
        glyphName = glyphName.split('.')[0]

        for axisName, value in position.items():
            # TODO: Change to axis minValue

            # Key is interpolation value per axis. Value is (avatarName, axis,
            # [master,...])
            avatarValues = {0:[(axisName, 0, glyphName)]}

        # Position is dict of type {<axis1Name>: value, <axis2Name>: value}
        pAxisName = sorted(position.keys())[0] # TODO: Make this work for multiple axes

        for gName in self._getAvatarGlyphNames(glyphName):
            nameParts = gName.split('.')

            for axisName, value in self.AVATARAXISVALUESPLIT.findall(nameParts[-1]):
                if not axisName in position:
                    continue

                value = TX.asIntOrNone(value)

                if value is not None and axisName in position and value <= position[pAxisName]:
                    if not value in avatarValues:
                        avatarValues[value] = set()
                    avatarValues[value].add((axisName, value, gName))

        return sorted(avatarValues[max(avatarValues.keys())])

    def getAvatarValues(self, glyphName):
        """Answers the dictionary of avatar location, depending on the
        existence of avatar glyph names in the masters related to glyphName."""
        # Make sure to take base name, in case we already got an avatar name
        # here.
        glyphName = glyphName.split('.')[0]
        avatarAxisValues = {}

        if glyphName is not None:
            for gName in self._getAvatarGlyphNames(glyphName):
                nameParts = gName.split('.')
                for axisName, value in self.AVATARAXISVALUESPLIT.findall(nameParts[-1]):
                    value = TX.asIntOrNone(value)
                    if not axisName in avatarAxisValues:
                        avatarAxisValues[axisName] = {}
                    if not value in avatarAxisValues[axisName]:
                        avatarAxisValues[axisName][value] = set()
                    avatarAxisValues[axisName][value].add(gName)

        # Answers {'weight': set(['dollar.weigth800', ...]),...} if the
        # glyphName attribute is 'dollar'
        return avatarAxisValues

    #   L O C K E D

    def getLocked(self):
        """Answers the set with locked style keys."""
        lockedKeys = [] # List of styleKeys [(familyPath, fileName), ...]
        for lockedId in self.disabled:
            lockedKeys.append((self.familyID, lockedId))
        return lockedKeys

    def isLocked(self, styleKey):
        """Answers the locked status of the styleKey. Note that this style is
        not necessarily a master or instance, since we want to maintain the
        setting, even if the style if not master or instance."""
        return styleKey in self.locked

    def lock(self, styleKey):
        """Locks the styleKey. Note that this style is not necessarily a master
        or instance, since we want to maintain the setting, even if the style
        if not master or instance."""
        self.locked.add(styleKey)

    def unlock(self, styleKey):
        """Unlocks the styleKey. Note that this style is not necessarily a master
        or instance, since we want to maintain the setting, even if the style
        if not master or instance."""
        if styleKey in self.locked:
            self.locked.remove(styleKey)

    #   D I S A B L E D

    def getDisabled(self):
        """Answers the set with disabled style keys."""
        disabledKeys = []
        for disabledId in self.disabled:
            disabledKeys.append((self.familyID, disabledId))
        return disabledKeys

    def isDisabled(self, styleKey):
        """Answers the disabled status of the styleKey. Note that this style
        is not necessary a master or instance, since we want to maintain the
        setting, even if the style is not a master if instance."""
        return styleKey in self.disabled

    def disable(self, styleKey):
        """Disables the styleKey. Note that this style is not necessary a
        master or instance, since we want to maintain the setting, even if the
        style if not master or instance."""
        self.disabled.add(styleKey)

    def enable(self, styleKey):
        """Enables the styleKey. Note that this style is not necessary a master
        or instance, since we want to maintain the setting, even if the style
        if not master or instance."""
        if styleKey in self.disabled:
            self.disabled.remove(styleKey)

    #   I N T E R P O L A T I O N

    def getStyleInterpolations(self, styleKey):
        """Answers the axis:value dictionary of styleKey."""
        if not styleKey in self.interpolations:
            self.interpolations[styleKey] = {}
        return self.interpolations[styleKey]

    def getStyleInterpolationAxis(self, styleKey, tag, default=0):
        """Answers the interpolation value of styleKey-tag. Answers
        default if the interpolation value is not defined or if the style does
        not exist."""
        if not styleKey in self.interpolations:
            return default

        return self.interpolations[styleKey].get(tag, default)

    def setStyleNeutral(self, styleKey):
        pass

    def setStyleInterpolationAxis(self, styleKey, tag, value):
        """Sets the styleKey-axis to value. If the style does not exist, then
        create an entry."""
        if not styleKey in self.interpolations:
            self.interpolations[styleKey] = {}

        self.interpolations[styleKey][tag] = self.checkType(value)

        # Not there yet, add it at the end of the sorted axis name list.
        if not tag in self.sortedAxes:
            self.sortedAxes.append(tag)

    def getStyleInterpolationValueByAxisIndex(self, styleKey, index):
        """Answers the interpolation value of the axis, which is on index in
        the self.sortedAxes list. Answers an empty string if the index is out
        of bounds. Attribute can be styleKey."""
        if index < len(self.sortedAxes):
            return self.getStyleInterpolationAxis(styleKey, self.sortedAxes[index], '')
        return ''

    def setStyleInterpolationValueByAxisIndex(self, styleKey, index, value):
        """Sets the interpolation value of the axis, which is on index in the
        self.sortedAxes list. Ignore if the index is out of bounds. Attribute
        can be styleKey."""
        if index < len(self.sortedAxes):
            self.setStyleInterpolationAxis(styleKey, self.sortedAxes[index], value)

    #   O R I G I N

    def asOrigin(self, styleKey):
        """Adds the style as origin of the family."""
        self.asMaster(styleKey)
        self.origin = styleKey[1] # styleID

    def notOrigin(self, styleKey):
        """Removes the style as origin, master or instance."""
        self.notMaster(styleKey)
        self.notInstance(styleKey)
        if self.origin == styleKey[1]: # styleID
            self.origin = None

    #   M A S T E R S  &  I N S T A N C E S

    def asMaster(self, styleKey):
        """Add the style as master of the family."""
        assert verifyStyleKey(styleKey) and styleKey in self.parent.getStyleKeys()
        self.notInstance(styleKey) # Cannot be instance and master at the same time.

        if not styleKey in self.masters: # Make sure not to add duplicates.
            self.masters.append(styleKey)

            if not styleKey in self.interpolations:
                self.interpolations[styleKey] = {}

            logger.info('Added %s to %s'  % (styleKey[1], self.name))

    def asInstance(self, styleKey):
        """Add the style as instance of the family."""
        assert verifyStyleKey(styleKey) and styleKey in self.parent.getStyleKeys()
        self.notMaster(styleKey) # Cannot be instance and master at the same time.

        if not styleKey in self.instances: # Make sure not to add duplicates.
            self.instances.append(styleKey)
            if not styleKey in self.interpolations:
                self.interpolations[styleKey] = {} # Add empty axis, just to have an entry in there.

    def asIgnore(self, styleKey):
        """Remove the style as origin, master or instance."""
        self.notOrigin(styleKey) # Also calls self.notInstance and self.notMaster

    def notMaster(self, styleKey):
        """Releases the master styleKey or styleKey as part of the family."""
        while styleKey in self.masters:
            self.masters.remove(styleKey)
            logger.warning('Removed %s from %s'  % (styleKey[1], self.name))

    def notInstance(self, styleKey):
        """Releases the instance as part of the family."""
        while styleKey in self.instances:
            self.instances.remove(styleKey)

    def isMaster(self, styleKey):
        """Answers if the font indicated by styleKey is part
        of the constellation as master."""
        return styleKey in self.masters

    def isInstance(self, styleKey):
        """Answers if the font indicated by styleKey is part
        of the constellation as instance."""
        return styleKey in self.instances

    def hasStyle(self, styleKey):
        """Answers if the style styleKey is defined as either
        master or instance."""
        return self.isMaster(styleKey) or self.isInstance(styleKey)

    def getStyleKeys(self):
        """Answers the list of styleKeys for styles that are defined (masters
        and instances) in the order as stored in the family. Note that the
        styles may not yet be open at this point."""
        styleKeys = []
        designSpaceKeys = set(self.masters + self.instances)

        # Scan in stored family order.
        for styleKey in self.parent.getStyleKeys():
            # Only add when unique.
            if styleKey in designSpaceKeys and not styleKey in styleKeys:
                styleKeys.append(styleKey)
        return styleKeys

    def getMasterKeys(self):
        """Answers the list of masterKeys, constructed from the styleKey in
        self.masters, in the order as stored on the family storage."""
        masterKeys = []
        designSpaceKeys = set(self.masters)

        # Scan in stored family order.
        for styleKey in self.parent.getStyleKeys():
            # Only add when unique.
            if styleKey in designSpaceKeys and not styleKey in masterKeys:
                masterKeys.append(styleKey)
        return masterKeys

    def getInstanceKeys(self):
        """Answers the list of instanceKeys, constructed from the styleKeys in
        self.instances, in the order as stored on the family storage."""
        instanceKeys = []
        designSpaceKeys = set(self.instances)

        # Scan in stored family order. Only add when unique.
        for styleKey in self.parent.getStyleKeys():
            if styleKey in designSpaceKeys and not styleKey in instanceKeys:
                instanceKeys.append(styleKey)

        return instanceKeys

    def getMasters(self):
        """Answers the list with master instances in the order as stored in
        the family.storage. Opens the master styles if they are not open."""

        #FIXME: returns None.

        masters = []
        masterKeys = set() # Use to catch non-unique references.
        designSpaceKeys = set(self.masters)

        # Scan in stored family order. Make sure it is unique.
        for styleKey in self.parent.getStyleKeys():
            if styleKey in designSpaceKeys and not styleKey in masterKeys:
                masters.append(self.getStyle(styleKey))
                masterKeys.add(styleKey)

        return masters

    def getMasterIDs(self):
        masterIDs = []
        designSpaceKeys = set(self.masters)

        # Scan in stored family order. Only add when unique.
        for styleKey in self.parent.getStyleKeys():

            if styleKey in designSpaceKeys and not styleKey[1] in masterIDs:
                masterIDs.append(styleKey[1])

        return masterIDs

    def getInstances(self):
        """Answers the list with instances in the order as stored in the
        family.storage. Opens the instance styles if they are not open."""
        instances = []
        instanceKeys = set() # Use to catch non-unique references.
        designSpaceKeys = set(self.instances)

        # Scan in stored family order. Only add when unique.
        for styleKey in self.parent.getStyleKeys():
            if styleKey in designSpaceKeys and not styleKey in instanceKeys:
                instances.append(self.getStyle(styleKey))
                instanceKeys.add(styleKey)

        return instances

    def getInstanceIDs(self):
        print('To be implemented')

    def getStyle(self, styleKey):
        """Answers the style with styleKey, if it is a constellation master or
        instance. If the style is not open, let the parent family open the
        style first. Answers None if there is not style with that id."""
        if styleKey in self.parent.styles: # May not exist.
            return self[styleKey]
        return None


    # X M L   E X P O R T

    def getXMLName(self):
        """Design space XML file name based on family name."""
        return '%s-%s.designspace' % (self.parent.name, self.name)

    def getXMLPath(self, abbr=False):
        """Returns absolute or abbreviated path to design space XML file."""
        name = self.getXMLName()
        p = self.parent.getPath()

        if abbr:
            parts = p.split('/')
            if len(parts) > 2:
                return '../' + '/'.join(parts[-2:]) + '/' + name
            else:
                return p + '/' + name
        else:
            return p + '/' + name

    def writeToXML(self, masterKeys, instanceKeys=None, rules=None):
        """Writes design space XML file using the lxml library.."""
        try:
            from lxml import etree
        except:
            print('no lxml')
            return
        root = etree.Element('designspace', format='3')
        axes = etree.SubElement(root, 'axes')
        sources = etree.SubElement(root, 'sources')
        #instances = etree.SubElement('instances')
        #rules = etree.SubElement('rules')

        for tag, axis in self.getAxes().items():
            if not axis['enabled']:
                continue

            # Example of desired XML output:
            # <axis default="88" maximum="500" minimum="5" name="xopaque" tag="XOPQ">
            name = axis['name']
            minimum = axis['minValue']
            default = axis['defaultValue']
            maximum = axis['maxValue']
            axis = etree.Element('axis', default=str(default),
                    maximum=str(maximum), minimum=str(minimum), name=name,
                    tag=tag)
            label = etree.Element('labelname')
            XML = "{http://www.w3.org/XML/1998/namespace}"
            label.set(XML + 'lang', "en")
            label.text = name
            axis.append(label)
            axes.append(axis)

        for masterKey in masterKeys:
            _, masterName = masterKey
            master = self.parent.getStyle(masterKey)
            familyID, masterId = getStyleKey(master)
            masterPath = TX.path2FamilyDir(familyID) + '/' + masterId
            name = 'source_' + masterName.replace('.ufo', '') # + axis name + axis value

            try:
                assert not master.info.styleName is None
            except AssertionError:
                e = DesignSpaceError('master.info.styleName not set for %s' % masterId)
                raise(e)

            source = etree.Element('source', familyname=self.parent.name,
                    filename=masterName, name=name, stylename=master.info.styleName)
            location = etree.SubElement(source, 'location')

            for tag, axis in self.getAxes().items():
                if not axis['enabled']:
                    continue
                name = axis['name']
                value = str(self.getStyleInterpolationAxis(masterKey, tag))
                dimension = etree.SubElement(location, 'dimension', name=name, xvalue=value)

            if masterId == self.origin:
                info = etree.SubElement(source, 'info', copy='1')

            sources.append(source)

        # Writes to file.
        path = self.getXMLPath()
        f = open(path, 'wb')
        lines = etree.tostring(root, xml_declaration=True, encoding='utf-8',
                pretty_print=True)
        f.write(lines)
        f.close()

    def getXMLFromFile(self):
        """Reads XML lines from file. No parsing involved."""
        path = self.getXMLPath()
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def asDoc(self, designSpacePath, check=True):
        """Loads design space XML from file the MutatorMath way.
        See also self.doc.generate()
        """

        if designSpacePath is None:
            return

        doc = DesignSpaceDocument()
        doc.read(designSpacePath)

        if check:
            try:
                doc.check()
            except Exception as e:
                print('DesignSpace.asDoc(): invalid design space.')
                print(traceback.format_exc())
                raise(e)

        return doc

    # G E N E R A T E

    def generate(self, styleKeys=None, dirPath=None, progressBar=None):
        """Exports the styleKeys. Exports all styleKeys by default. The
        exporting is done based on the settings of the landing patterns of the
        styles and the family.

        DEPRECATED? Generating using FontMake.
        """
        report = {}

        if styleKeys is None:
            styleKeys = self.getStyleKeys()

        for styleKey in styleKeys:
            style = self.getStyle(styleKey)
            if style is None:
                continue
            if progressBar is not None:
                progressBar.set(title='Generating %s-%s' % (self.parent.name,
                    style.info.styleName))

            # Get the landing pattern for this style. The name of the landing
            # patterns is used as name for the sub folder that the generated
            # fonts are stored in.
            if not styleKey in self.landingPatterns:
                landingPatterns = None # Force use of default landing pattern
            else:
                landingPatterns = self.landingPatterns[styleKey[1]]
            self.generateStyleByLandingPattern(style, self.parent.name,
                    dirPath, landingPatterns, report, progressBar)

        return report

    @classmethod
    def generateStyleByLandingPattern(cls, style, familyName, dirPath=None,
            landingPatterns=None, report=None, progressBar=None):
        """DEPRECATED? Generating using FontMake."""
        if report is None:
            report = {}

        # In case not defined or empty, use default landing pattern.
        landingPatterns = landingPatterns or dict(default={})

        # For all formats/extensions in all landing patterns generate the
        # export font.
        for landingPatternName, landingPattern in landingPatterns.items():
            # Create export dictionary if it does not already exist. Use
            # optional dirPath if defined.
            if dirPath is None:
                dirPath = TX.path2FamilyDir(style.path)
            if not dirPath.endswith('/'):
                dirPath += '/'
            for extension in landingPattern.get('formats', ('otf', 'ttf')):
                # Create the export direction, if it does not already exist.
                lpPath = dirPath + 'export/' + landingPatternName + '/' + extension + '/'
                try:
                    os.makedirs(lpPath)
                except OSError:  # Path already exists, ignore.
                    pass

                # We don't know how valid the style name is. Do some testing
                # and tweaking here.
                styleName = style.info.styleName
                while styleName and styleName.startswith('-'):
                    styleName = styleName[1:]
                if not styleName:
                    styleName = 'Regular'

                # Now construct the path for the output font file.
                path = lpPath + familyName + '-' + styleName + '.' + extension

                # generate(self, path=None, format="otf", decompose=False,
                # checkOutlines=False, autohint=False, releaseMode=False,
                # glyphOrder=None, progressBar=None, useMacRoman=False):
                report[path] = style.generate(path, format=extension,
                    checkOutlines=landingPattern.get('checkOutlines', True),
                    autohint=landingPattern.get('autoHint', True),
                    releaseMode=landingPattern.get('releaseMode', True),
                    glyphOrder=landingPattern.get('glyphOrder', None),
                    progressBar=progressBar,
                    useMacRoman=landingPattern.get('useMacRoman', False)
                )
        for k, item in report.items():
            print('\n\n=== %s ===' % k)
            print(item)

    # Paths.

    def getVarPath(self):
        p = TX.path2FamilyDir(self.parent.familyID)
        n = self.parent.name
        return '%s/%s/%s-%s-VF.ttf' % (p, 'variable_ttf', n, self.name)
