# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     screens.py
#
from AppKit import NSScreen, NSWindow
from tnbits.base.c import *

class ScreenConfiguration(object):
    """Class methods for (dual) screen measurements and data."""

    @classmethod
    def screens(cls):
        return NSScreen.screens()

    @classmethod
    def frames(cls):
        frames = []
        for screen in cls.screens():
            (x, y), (w, h) = screen.frame()
            frames.append((x, y, w, h))
        return frames

    @classmethod
    def getScreenId(cls, screen):
        return screen.deviceDescription()['NSScreenNumber']

    @classmethod
    def getWindowScreenId(cls, window):
        """Gets the screen ID from the Vanilla window."""
        if isinstance(window, NSWindow):
            return cls.getScreenId(window.screen())
        else:
            return cls.getScreenId(window._window.screen())

    @classmethod
    def getMainScreenId(cls):
        return cls.getScreenId(cls.getMainScreen())

    @classmethod
    def getScreen(cls, screenId):
        """Answers the screen defined by *screenId*. If the screen can not be
        found, then answer the main screen."""
        for screen in cls.screens():
            if screenId == screen.deviceDescription()['NSScreenNumber']:
                return screen
        return cls.getMainScreen()

    @classmethod
    def sizes(cls):
        sizes = []
        for _, _, w, h in sorted(cls.frames()):
            sizes.append((w, h))
        return sizes

    @classmethod
    def sizesById(cls):
        """Answers the dictionary with screen ids as keys and sizes as
        value."""
        sizes = {}
        for screen in cls.screens():
            (x, y), (w, h) = screen.frame()
            sizes[cls.getScreenId(screen)] = x, y, w, h
        return sizes

    @classmethod
    def getId(cls):
        """Answers a unique Id for this number and size of screens, so we can
        use that as key for the position of the windows. We'll only look at the
        screen ids, not they relative positions, so the configuration gets
        recognized, even if the relative position of the windows changed in the
        meantime."""
        ids = []
        for screen in cls.screens():
            ids.append('%d' % cls.getScreenId(screen))
        return '+'.join(ids)

    @classmethod
    def getMainScreen(cls):
        """Answers the main `Screen` instance, positioned at `(0,0)`."""
        for screen in cls.screens():
            (x, y), (_, _) = screen.frame()
            if x == 0 and y == 0:
                return screen
        return None

class Screens(object):
    """Provides access to screen configuration and window size functions."""

    def __init__(self, preferences, defaultPos, window=None):
        self.preferences = preferences
        self.defaultPos = defaultPos
        self.window = window

    def applyWindowPosSize(self):
        """Applies the current position and size to the window tool. This can
        happen between category switches."""
        screen, posSize = self.getWindowScreenPosSize()
        self.setWindowPosSize(posSize)

    def getWindowPosSizeKey(self, configurationId):
        """Answers the unique key for this tool window and for the current
        configuration of screens."""
        # TODO: Make multi-screen positioning to work properly, as there still
        # seem to be some issues there.  Build the key from current
        # configuration and the selected Badger category If no Badger context
        # is available, then store the posSize in "single" mode (self.CATEGORY
        # answers None).
        return '%s-%s' % (PREF_WINDOWPOSSIZE, configurationId)

    def getWindowScreenPosSize(self, posSize=None):
        """Answers the window position from the stored preference for the
        current screen configuration and selected category if it exists,
        otherwise takes the attributes as default."""
        # Get the unique preference key for this tool window and this screen configuration
        configuration = ScreenConfiguration()
        configurationId = configuration.getId() # Apply only for the current screen configuration.
        key = self.getWindowPosSizeKey(configurationId)

        if posSize is None:
            # Default window size, if not supplied. Get from the tool preference.
           posSize = self.preferences.getPreferenceModelValue(PREF_WINDOWPOSSIZE)

        if self.window: # If there already is a window, get the screen it is on.
            screenId = configuration.getWindowScreenId(self.window.getNSWindow())
        else: # Otherwise we'll assume it is to be placed on the main screen.
            # @@@ This wrong, as there may already be a position on another
            # screen from the previous session.
            screenId = configuration.getMainScreenId()

        # This default posSize gets overwritten if a value is already stored in
        # RF preferences under this key (= screen configuration and Badger
        # category.
        screenId, posSize = self.preferences.getPreference(key, default=(screenId, posSize))

        # Still None, this may be a new tool, set to the tool class default
        # values.
        if posSize is None:
            posSize = self.preferences.defaultPos

        # Answers screen and the position on the screen.
        return configuration.getScreen(screenId), posSize

    def setWindowPosSize(self, posSize=None, screen=None, window=None):
        """Saves the current window screen, position and size in the user
        preferences for the current configuration of the screen(s)."""
        # Get the unique preference key for this tool window and this screen
        # configuration
        configuration = ScreenConfiguration()
        configurationId = configuration.getId() # Apply only for the current screen configuration.
        key = self.getWindowPosSizeKey(configurationId)

        if screen is not None:
            screenId = configuration.getScreenId(screen)
        elif window is not None:
            screenId = configuration.getWindowScreenId(window)
        else:
            screenId = configuration.getMainScreenId()

        if window is None: # Working on another window than our own.
            window = self.window

        if window:
            if posSize is None:
                posSize = window.getPosSize()
            else: # Otherwise adjust the window to the new position.
                window.setPosSize(posSize)

        if posSize is None:
            # Make old default measures first. Then match against what is in
            # default preference of the tool.
            posSize = self.defaultPos
            posSize = self.preferences.getPreferenceModelValue(PREF_WINDOWPOSSIZE, default=posSize)
        self.preferences.setPreference(key, (screenId, posSize))

    def toolWindowMoved(self, window):
        """Tool window moved. Store the current posSize in the preferences."""
        self.setWindowPosSize(window=window)

    def toolWindowResized(self, window):
        """Tool window resized. Store the current posSize in the
        preferences."""
        self.setWindowPosSize(window=window)

if __name__ == '__main__':
    sc = ScreenConfiguration()

    for screen in sc.screens():
        print(screen)
        print(sc.getScreenId(screen))
        print(screen.deviceDescription())

    print(sc.frames())
    print(sc.sizes())
    print(sc.getId())
