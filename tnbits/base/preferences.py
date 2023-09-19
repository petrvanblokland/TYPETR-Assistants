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
#    preferences.py
#

import os, os.path
from AppKit import NSMutableDictionary, NSSearchPathForDirectoriesInDomains, \
        NSApplicationSupportDirectory, NSUserDomainMask, NSUserDefaults
from tnbits.base.c import *
from tnbits.base.screens import Screens
from tnbits.base.preferencemodels import *

class Preferences(object):
    """Interface for tool preferences. Saves to:

        /Users/michiel/Library/Application Support/RoboFont/plugins/preferences.plist

    if inside RoboFont or to for example:

        /Users/michiel/Library/Application Support/Proof/plugins/preferences.plist

    when running as an independent application.
    """

    def __init__(self, toolName, standAlone=False, tool=None, defaultPos=None,
            useFloatingWindow=False):
        # One preferences set per name.
        # TODO: use TOOLID as identifier to distinguish between family windows
        # of the same tool.
        self.toolName = toolName
        self.tool = tool
        self.path = None
        self._extensionDefaults = None
        self.standAlone = standAlone

        if self.standAlone:
            self.setPreferencesPath()

        self.defaultPos = defaultPos
        self.useFloatingWindow = useFloatingWindow
        self.model = getModel(toolName, defaultPos)
        self.screens = Screens(self, defaultPos)

    def extensionDefaults(self):
        """Reads from current dictionary, from file or return empty dictionary
        if file doesn't exist."""
        if self._extensionDefaults is None:
            self._extensionDefaults = NSMutableDictionary.dictionaryWithContentsOfFile_(self.path)

        if self._extensionDefaults is None:
            self._extensionDefaults = NSMutableDictionary.dictionary()

        return self._extensionDefaults

    # Get.

    def getExtensionDefault(self, key, fallback=None):
        """Gets an default value for a key, with a fallback if the key is not
        present in the defaults."""
        if self.standAlone:
            defaults = self.extensionDefaults()
            return defaults.get(key, fallback)
        else:
            from mojo.extensions import getExtensionDefault as mojoGetExtensionDefault
            return mojoGetExtensionDefault(key, fallback)

    def getPreferenceId(self):
        """Answers the toolId as preference ID. Can be *None* if the
        class did not define it."""
        return 'tnTools.' + self.toolName

    def getPreference(self, key, default=None, forceDefault=False):
        """The *getPreference* method answers the preference value for the
        *moduleID* and *key* as set in the application preferences. If the
        value cannot be found then *default* is answered. The default value is
        not stored in the preferences."""
        value = None
        preferenceId = self.getPreferenceId()
        k = ("%s.%s" % (preferenceId, key)).replace(' ', '_')

        if not forceDefault:
            value = self.getExtensionDefault(k)

        if value is None:
            value = self.getPreferenceModelValue(key)

        # Tests if we really got a value, then save it in RoboFont default
        # storage. If it was default, make sure it is saved.
        if value is not None:
            self.setExtensionDefault(k, value)

        # If still None then force default.
        if value is None:
            value = default

        return value

    def getPreferenceModel(self, name):
        """Answers the dictionary as stored under *name* from the class
        dictionary *self.model*.
        Answers *None* if the entry cannot be found. If the tool doesn't
        redefined this dictionary, then the default model of the BaseTool class
        is used."""
        return self.model.get(name)

    def getPreferenceModelValue(self, name, default=None):
        """In case the value does not have a given default, try to get the
        value from the preferences model. If the model does not know the entry,
        then answer *default*."""
        model = self.getPreferenceModel(name)

        if model is not None: # Test on None, default can be 0, which we want to keep.
            return model.get('default')

        return default

    # Set.

    def setPreferencesPath(self):
        """Creates a preferences file for a stand alone application if it
        doesn't exist yet."""
        paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,
                    NSUserDomainMask, True)
        supportPath = os.path.join(paths[0], self.toolName)

        if not os.path.exists(supportPath):
            os.mkdir(supportPath)

        defaultsFromFile = NSUserDefaults.standardUserDefaults()
        key = "extensionsDir"
        defaultValue = os.path.join(supportPath, "plugins")
        pluginPath = defaultsFromFile.get(key, defaultValue)

        if not os.path.exists(pluginPath):
            os.mkdir(pluginPath)

        f = "preferences.plist"
        self.path = os.path.join(pluginPath, f)

    def setExtensionDefault(self, key, value):
        """Sets a default value for a key."""
        if self.standAlone:
            defaults = self.extensionDefaults()
            defaults[key] = value
        else:
            from mojo.extensions import setExtensionDefault as mojoSetExtensionDefault
            mojoSetExtensionDefault(key, value)

    def setPreference(self, key, value):
        """The *setPreference* method sets the preference *key* to *value* for
        the defined *moduleID*."""
        preferenceId = self.getPreferenceId()
        k = ("%s.%s" % (preferenceId, key)).replace(' ', '_')
        self.setExtensionDefault(k, value)

    def writePreferences(self):
        """Writes the defaults dictionary to file in the Application Support
        folders."""
        if self.standAlone:
            defaults = self.extensionDefaults()
            defaults.writeToFile_atomically_(self.path, True)
