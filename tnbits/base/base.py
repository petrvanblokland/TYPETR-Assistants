# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    base.py
#

import logging
from vanilla.vanillaWindows import Window
from defconAppKit.windows.baseWindow import BaseWindowController

from tnbits.vanillas.progress import Progress
from tnbits.base.preferences import Preferences
from tnbits.base.notificationcenter import NotificationCenter

class Base(BaseWindowController):
    """Controls a Vanilla window in the context of the Type Network development
    environment. Superclass to

    * Tool for usage withing RoboFont context and
    * App for usage as a stand alone application.

    """

    # Preferences are stored in the family or tool.
    FAMILYPREFERENCES = False

    def __init__(self):
        self.windowClass = self.getWindowClass()
        self.name = self.NAME or 'Untitled Tool'
        self.w = None
        self._progress = None
        self.dialogs = {}
        self.notificationCenter = NotificationCenter(self)
        self.logger = logging.getLogger(__name__)

        if not self.FAMILYPREFERENCES:
            self.preferences = Preferences(self.NAME, defaultPos=self.DEFAULTPOS)

    # Vanilla / window.

    def openWindow(self):
        """
        Should open a Vanilla window and maybe create some bindings.

        For Example:

        self.window.open()
        """
        raise NotImplementedError

    def closeWindow(self, sender):
        BaseWindowController.windowCloseCallback(self, sender)

    def getWindow(self):
        return self.w

    getView = getWindow

    def getPosSize(self):
        return self.w.getPosSize()

    def setTitle(self, family=None, styleName=None):
        """Composes window title from tool name and family name."""
        t = self.getTitle(family, styleName=styleName)
        self.w.setTitle(t)

    def getTitle(self, family, styleName=None):
        """Returns window title that displays family name and number of
        styles."""
        if styleName:
            return '%s - %s' % (styleName, self.NAME)
        elif family:
            return '%s - %s' % (family.name, self.NAME)
        else:
            return self.NAME

    def getWindowClass(self):
        """Answers the class for the tool windows, depending on the settings
        of the preference."""
        # TODO: use isinstance on self?
        #if self.preferences.getPreference(PREF_FLOATINGWINDOW):
        #    return FloatingWindow
        return Window

    def set(self, name, vanillaObject):
        # TODO: check if object inherits from vanilla base.
        setattr(self.w, name, vanillaObject)

    def get(self, name):
        return getattr(self.w, name)

    # Progress.

    def progressOpen(self, title='', text='', ticks=None, inside=True):
        """Opens the progress window. If ticks is None or omitted, then show
        the progress bar as animated setIndeterminate. Ticks is the amount of
        predicted items that need to be processed."""
        if not self._progress:
            if inside:
                parent = self.getWindow()
            else:
                # Forces progress window to be separate floating window.
                parent = None

            self._progress = Progress(title=title, text=text, tickCount=ticks,
                    parentWindow=parent)
        else:
            self.progressTicks(ticks)
            self.progressSet(title, text)

    def progressTicks(self, ticks):
        """Updates the number of items still to be processed."""
        if self._progress is not None:
            self._progress.setTickCount(ticks)

    def progressUpdate(self, text=None, title=None):
        """Increment the current tick, making the process bar to click to the
        next relative position."""
        if self._progress is not None:
            self._progress.update(title=title, text=text)

    def progressClose(self):
        if self._progress is not None:
            self._progress.close()
            self._progress = None

    def progressTitle(self, title):
        self.progressSet(title=title, text=None)

    def progressText(self, text):
        self.progressSet(title=None, text=text)

    def progressSet(self, title=None, text=None):
        if self._progress is not None:
            self._progress.set(title=title, text=text)

    def getProgress(self):
        """The `getProgress` method answers the current ProgressWindow
        instance, allowing other tools to update the progressBar."""
        return self._progress

    # Preferences.

    def setPreference(self, key, value):
        if self.FAMILYPREFERENCES:
            self.controller.family.setPreference(self.name, key, value)
        else:
            self.preferences.setPreference(key, value)

    def getPreferences(self):
        if not self.FAMILYPREFERENCES:
            return self.preferences

    def writePreferences(self, *args, **kwargs):
        if not self.FAMILYPREFERENCES:
            self.preferences.writePreferences()
        else:
            self.controller.family.save()

    def getPreference(self, key, default=None, forceDefault=False):
        if self.FAMILYPREFERENCES:
            return self.controller.family.getPreference(self.name, key, default, forceDefault)
        else:
            return self.preferences.getPreference(key, default, forceDefault)

    def getDefaultPreference(self, controller, key, default=None):
        """Gets default preference if doesn't exist yet."""
        value = self.getPreference(key)

        if value is None:
            print('No preference value found for %s, defaulting to %s!' % (key, default))
            value = default
            self.setPreference(key, value)

        return value

        #setattr(controller, param, p)

    def setDefaultPreference(self, controller, param, value=True):
        """Sets preference to default if not found. This is better than testing
        with an or statement, because a True default value will always
        succeed.

        DEPRECATED: use getDefaultPreference and set attr in controller.
        """
        p = self.getPreference(param)

        if p is None:
            print('No preference value found for %s, defaulting to %s!' % (param, value))
            p = value
            self.setPreference(param, p)

        setattr(controller, param, p)

    def preferencesChanged(self):
        """To be redefined by tools that want to cache preferences.
        """
        if hasattr(self, 'controller'):
            self.controller.preferencesChanged()


    # Window bindings.

    def bind(self):
        self.w.bind('move', self.isMoved)
        self.w.bind('resize', self.isResized)

    def unbind(self):
        if self.w is not None:
            self.w.unbind('move', self.isMoved)
            self.w.unbind('resize', self.isResized)

    def isMoved(self, window):
        # TODO: do only after move is finished.
        if not self.FAMILYPREFERENCES:
            self.preferences.screens.toolWindowMoved(window)

    def isResized(self, window):
        # TODO: do only after resize is finished.
        if not self.FAMILYPREFERENCES:
            self.preferences.screens.toolWindowResized(window)

    # Dialogs.

    def addDialog(self, name, dialog):
        assert not name in self.dialogs
        self.dialogs[name] = dialog

    def removeDialog(self, name):
        if name in self.dialogs:
            self.dialogs.pop(name)
