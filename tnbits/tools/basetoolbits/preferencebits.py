# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    preferencebits.py
#
from time import time

try:
    from mojo.extensions import getExtensionDefault, setExtensionDefault
except:
    print('preferencesbits.py (DEPRECATED): not in RoboFont, stand alone mode.')

from tnbits.model import model

class Track(object):
    def __init__(self):
        self.start = self.count = self.total = self.end = self.max = self.average = 0

class PreferenceBits(object):

    @classmethod
    def getPreferenceId(cls):
        """Answers the toolId as preference ID. Can be *None* if the
        class did not define it."""
        return 'tnTools.' + cls.getId()

    def hasPreference(self, name):
        """Answer if the RoboFont preference storage contains the name."""
        return getExtensionDefault(name, None) is not None

    def getPreference(self, name, default=None, forceDefault=False):
        """The *getPreference* method answers the preference value for the
        *moduleID* and *key* as set in the application preferences. If the
        value cannot be found then *default* is answered. The default value is
        not stored in the preferences."""
        value = None
        preferenceId = self.getPreferenceId()
        if preferenceId is not None:
            k = ("%s.%s" % (preferenceId, name)).replace(' ', '_')
            value = None
            if not forceDefault:
                value = getExtensionDefault(k)
            # If not in RF preferences yet, get it from the PREFERENCES_MODEL of the tool
            # Try to get the preference as defined by the tool. This is used in the initialization
            # phase, when the tools doesn't have a stored user preference setting yet."""
            if value is None:
                value = self.getPreferenceModelValue(name)
            # Test if we really got a value, then save it in RoboFont default storage.
            if value is not None: # and value == default:
                setExtensionDefault(k, value) # If it was default, make sure it is saved.
        if value is None: # Still None, they force default.
            value = default
        return value

    def setPreference(self, name, value):
        """
        The *setPreference* method sets the preference *key* to *value*
        for the defined *moduleID*. The *value* is answered for convenience of the
        caller.
        """
        preferenceId = self.getPreferenceId()
        if preferenceId is not None:
            k = ("%s.%s" % (preferenceId, name)).replace(' ', '_')
            setExtensionDefault(k, value)
        return value

    def _initializeLibPreference(self, lib, name, default=None):
        """Make sure that the named tool lib dictionary exists in the font.lib or glyph.lib"""
        toolId = self.getId()
        if not toolId in lib:
            lib[toolId] = {}
        if default is not None and not name in lib[toolId]:
            if default is None:
                # Try to initialize from the preference model.
                default = self.getPreferenceModelValue(name, '')
            lib[toolId][name] = default

    #   Using the tool preferences, as defined in the self.PREFERENCE_MODEL dictionary.
    #   This is also used to automatically create central tool preferences editor in DisplayItems.

    def getPreferenceModel(self, name):
        """Answer the dictionary as stored under *name* from the class dictionary *self.PREFERENCE_MODEL*.
        Answer *None* if the entry cannot be found. If the tool doesn't redefined this dictionary,
        then the default model of the BaseTool class is used."""
        return self.PREFERENCE_MODEL.get(name)

    def getPreferenceModelValue(self, name, default=None):
        """In case the value does not have a given default, try to get the value from the
        preferences model. If the model does not know the entry, then answer *default*."""
        model = self.getPreferenceModel(name)
        if model is not None: # Test on None, default can be 0, which we want to keep.
            return model.get('default')
        return default

    def getStylePreference(self, name, default=None, styleKey=None):
        """Answer the named preference in the current font if it exists. If it does not exist,
        then set the default and answer the default. If there is no current font, answer None."""
        if styleKey is not None:
            style = model.getStyle(styleKey)
        else:
            style = self.getCurrentStyle()
        if style is not None:
            self._initializeLibPreference(style.lib, name, default or '')
            toolId = self.getId()
            return style.lib[toolId][name]
        return default

    def setStylePreference(self, name, value, styleKey=None):
        """Set the named preference in the current font if it exists. Answer the value for
        convenience of the caller. If there is no current font, then answer None."""
        if styleKey is not None:
            style = model.getStyle(styleKey)
        else:
            style = self.getCurrentStyle()
        if style is not None:
            self._initializeLibPreference(style.lib, name)
            toolId = self.getId()
            style.lib[toolId][name] = value
        return value

    def getGlyphPreference(self, glyphName, name, default=None, styleKey=None):
        """Answer the named preference in the current glyph if it exists. If it does not exist,
        then set the default and answer the default. If there is no current glyph, answer None."""
        if styleKey is not None:
            style = model.getStyle(styleKey)
        else:
            style = self.getCurrentStyle()
        if style is not None and glyphName in style:
            glyph = style[glyphName]
            if default is None: # Allow for empty list or dictionary.
                default = {}
            self._initializeLibPreference(glyph.lib, name, default)
            toolId = self.getId()
            return glyph.lib[toolId][name]
        return default

    def setGlyphPreference(self, glyphName, name, value, styleKey=None):
        """Set the named preference in the current font if it exists. Answer the value for
        convenience of the caller. If there is no current font, then answer None"""
        if styleKey is not None:
            style = model.getStyle(styleKey)
        else:
            style = self.getCurrentStyle()
        if style is not None and glyphName in style:
            glyph = style[glyphName]
            self._initializeLibPreference(glyph.lib, name)
            toolId = self.getId()
            glyph.lib[toolId][name] = value
        return value

    #   W I N D O W  S I Z I N G

    def applyWindowPosSize(self):
        """Apply the current preference to the window tool. This can happen between
        category switches by the Project tool."""
        screen, posSize = self.getWindowScreenPosSize()
        self.setWindowPosSize(posSize)

    def getWindowPosSizeKey(self, configurationId):
        """Answer the unique key for this tool window and for the current configuration of screens."""
        # TODO: Make multi-screen positioning to work properly, as there still seem to be some issues there.
        # Build the key from current configuration and the selected Badger category
        # If no Badger context is available, then store the posSize in "single" mode (self.category answers None).
        return '%s-%s-%s' % (self.C.PREF_WINDOWPOSSIZE, configurationId, self.category or 'single')

    def getWindowScreenPosSize(self, posSize=None):
        """Answers the window position from the stored preference for the
        current screen configuration and selected category if it exists,
        otherwise takes the attributes as default."""
        # Get the unique preference key for this tool window and this screen configuration
        configuration = self.screenConfiguration()
        configurationId = configuration.getId() # Apply only for the current screen configuration.
        key = self.getWindowPosSizeKey(configurationId)

        if posSize is None:
            # Default window size, if not supplied. Get from the tool preference.
           posSize = self.getPreferenceModelValue(self.C.PREF_WINDOWPOSSIZE)

        if self.w: # If there already is a window, get the screen it is on.
            screenId = configuration.getWindowScreenId(self.w.getNSWindow())
        else: # Otherwise we'll assume it is to be placed on the main screen.
            # @@@ This wrong, as there may already be a position on another screen from the previous session.
            screenId = configuration.getMainScreenId()

        # This default posSize get overwritten if there is a value already stored in RF preferences
        # under this key (= screen configuration and Badger category.
        screenId, posSize = self.getPreference(key, default=(screenId, posSize))

        # Still None, this may be a new tool, set to the tool class default values.
        if posSize is None:
            posSize = self.VIEWX, self.VIEWY, self.VIEWWIDTH, self.VIEWHEIGHT

        return configuration.getScreen(screenId), posSize # Answer screen and the position on the screen

    def setWindowPosSize(self, posSize=None, screen=None, window=None):
        """Saves the current window screen, position and size in the user
        preferences for the current configuration of the screen(s)."""
        # Get the unique preference key for this tool window and this screen configuration
        configuration = self.screenConfiguration()
        configurationId = configuration.getId() # Apply only for the current screen configuration.
        key = self.getWindowPosSizeKey(configurationId)
        if screen is not None:
            screenId = configuration.getScreenId(screen)
        else:
            screenId = configuration.getMainScreenId()

        if window is None: # Working on another window than our own.
            window = self.w

        if window:
            if posSize is None:
                posSize = window.getPosSize()
            else: # Otherwise adjust the window to the new position.
                window.setPosSize(posSize)

        if posSize is None:
            # Make old default measures first. Then match against what is in default preference of the tool.
            posSize = self.VIEWX, self.VIEWY, self.VIEWWIDTH, self.VIEWHEIGHT
            posSize = self.getPreferenceModelValue(self.C.PREF_WINDOWPOSSIZE, default=posSize)

        self.setPreference(key, (screenId, posSize))

    def toolWindowMoved(self, window):
        """Tool window moved. Store the current posSize in the preferences."""
        self.setWindowPosSize()

    def toolWindowResized(self, window):
        """Tool window resized. Store the current posSize in the preferences."""
        self.setWindowPosSize()

    #   E V E N T  T R A C K I N G

    def _getTracking(self, name):
        if name is None:
            name = self.TOOLID
        if not hasattr(self, '_tracking'):
            self._tracking = {}
        if not name in self._tracking:
            self._tracking[name] = Track()
        return self._tracking[name]

    def trackEventStart(self, name=None):
        """Call this to start execution of an event, e.g. to time the total amount of time spend inside a drawing
        event. This way a tool can figure out how much interaction time it is draining. If the optional name is not
        defined, they use self.TOOLID instead."""
        tracking = self._getTracking(name)
        tracking.start = time()

    def trackEventEnd(self, name=None):
        """Finalize the tracking registration for this event call, initiated by calling self.trackEventStart()."""
        tracking = self._getTracking(name)
        tracking.end = e = time()
        d = e - tracking.start
        tracking.count += 1
        tracking.total += d
        tracking.average = tracking.total / tracking.count
        tracking.max = max(tracking.max, d)

    def getEventTracking(self, name=None):
        """Answer the event track record for this name. If the optional name is not defined, then use self.TOOLID instead."""
        return self._getTracking(name)
