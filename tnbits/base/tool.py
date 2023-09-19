# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tool.py
#
#   Forks the BaseTool, starting a new version without multiple inheritance or
#   RoboFont dependencies.

from vanilla import Window
from tnbits.base.c import *
from tnbits.base.base import Base
from tnbits.base.static import *
from tnbits.base.tools import *
from tnbits.base.windows import setBackgroundColor

class Tool(Base):
    """A tool inside the RoboFont scripting context. Provides preferences,
    screen and window management. Can be connected to RoboFont callbacks
    through observers. Mostly doesn't know about floq model or font tech; that
    information goes inside the controllers. Stand alone versions of the tools
    should inherit from the App class, which has a shared Base class.

    TODO: Vanilla related code should be moved to Base class.
    """

    # Default global values. Override in inheriting class.

    TOOLID = None
    NAME = None
    CATEGORY = None
    VIEWX = VIEWY = 50
    VIEWWIDTH = 800
    VIEWHEIGHT = 600
    VIEWMINSIZE = (VIEWWIDTH / 2, VIEWHEIGHT / 2)
    VIEWMAXSIZE = (VIEWWIDTH * 2, VIEWHEIGHT * 2)

    # Allowing multiple windows of the same tool.
    ALLOWMULTIPLE = False

    # RoboFont or stand alone tool.
    RF = True

    # See tnbits.base.constants for a full list of events.
    OBSERVERS = (
        #('_fontDidOpen', EVENT_FONTDIDOPEN),
        #('_fontDidClose', EVENT_FONTDIDCLOSE),
        #('_currentGlyphChanged', EVENT_CURRENTGLYPHCHANGED),
        ('mouseUp', EVENT_MOUSEUP),
        ('keyUp', EVENT_KEYUP),
        ('fontSaved', EVENT_FONTDIDSAVE),
    )

    def __init__(self):
        super(Tool, self).__init__()
        self._active = True

    def build(self):
        """Builds the tool. Can be redefined in the inheriting class."""

        if hasattr(self, 'preferences'):
            screen, posSize = self.preferences.screens.getWindowScreenPosSize()
            self.w = Window(posSize=posSize, title=self.NAME, screen=screen,
                    minSize=self.VIEWMINSIZE, maxSize=self.VIEWMAXSIZE)
        else:
            # TODO: restore screen and posSize using family preferences.
            # DEFAULT possize?
            posSize = (0, 0, self.VIEWWIDTH, self.VIEWHEIGHT)
            self.w = Window(posSize=posSize, title=self.NAME, minSize=self.VIEWMINSIZE,
                    maxSize=self.VIEWMAXSIZE)

        setBackgroundColor(self.w)
        self.controller = self.ControllerClass(self)
        self.openWindow()

    # Family.

    def setFamily(self, family):
        """Sets a family when tool is opened."""
        if hasattr(self, 'controller'):
            self.controller.setFamily(family)

    # Etc.

    def getID(self):
        """Unique tool ID. Must be refined by inheriting class. Otherwise
        None, to prevent base tool classes to add themselves."""
        return self.TOOLID

    def isActive(self):
        """Answers if the tool is currently active and has an open window."""
        return self._active and self.isOpen()

    def activate(self, active=True):
        self._active = active

    def exists(self):
        # TODO: Restore for Badger.
        pass

    # Window.

    def openWindow(self):
        """Creates DefCon window bindings, store the position in tool
        preferences. Opens window and marks that the tool is active."""
        self.setUpBaseWindowBehavior()
        self.bind()
        self.addObservers()
        self.w.open()
        self.activate()

    def getWindowToFront(self):
        """Bring the window of this tool to front."""
        # TODO: move to Base class?
        self.w.show()

    def isOpen(self):
        """Answers if the tool has an open window."""
        return self.w is not None

    def hide(self):
        """Hides the window(s) of the tools if they exist."""
        if self.isActive():
            self.w.hide()

        self.activate(False)

    def show(self):
        """Show the window(s) of the tool. If there are no open window yet,
        then call *self.build* to open the window."""
        if not self.isActive():
            self.build()
        else:
            self.w.show()

        self.activate()

    # Callbacks.

    def windowCloseCallback(self, sender):
        if hasattr(self, 'controller'):
            self.controller.preferencesChanged()
            self.controller.close()
        self.close(sender)

    def close(self, sender):
        self.closeWindow(sender)
        self.unbind()
        self.w = None
        self.activate(False)
        self.terminate()

    # Notifications.

    '''
    RoboFont notifications can be observed by the tool by connecting the event
    to a function by adding a (function, event_name) tuple to the OBSERVERS
    global:

    @('glyphChanged', EVENT_CURRENTGLYPHCHANGED),@

    Both OBSERVERS and notified functions should be redefined by the inheriting
    tool subclass.

    OBSERVERS = (
        ('fontDidOpen', EVENT_FONTDIDOPEN),
        ('fontIsClosing', EVENT_FONTWILLCLOSE),
        ('fontChanged', EVENT_CURRENTFONTCHANGED),
        ('glyphChanged', EVENT_CURRENTGLYPHCHANGED),
        ('mouseUp', EVENT_MOUSEUP),
        ('fontSaved', EVENT_FONTDIDSAVE),
        ('viewDidChangeGlyph', EVENT_VIEWDIDCHANGEGLYPH),
        ('featuresChanged', EVENT_FEATURESCHANGED),
    )
    '''

    def glyphChanged(self, event):
        raise NotImplementedError

    def mouseUp(self, event):
        if hasattr(self, 'controller'):
            self.controller.update()

    def keyUp(self, event):
        if hasattr(self, 'controller'):
            self.controller.update()

    def fontSaved(self, event):
        if hasattr(self, 'controller'):
            self.controller.update()

    # Observers.

    def addObservers(self):
        self.notificationCenter.addObservers()

    def removeObservers(self):
        self.notificationCenter.removeObservers()

    def getObservers(self):
        return self.OBSERVERS

    # Deletion.

    def __del__(self):
        """Make sure all observers are released and the window is closed by
        calling @self.terminate()@."""
        self.terminate()

    def terminate(self):
        """Gets called by the project manager, if the tool is deleted. To be
        redefined by inheriting classes. The default behavior is to close the
        window, if it exists."""
        # Still exists in the tools? Delete self from the tools set.
        self.removeObservers()
        self.writePreferences()
        removeTool(self)

        if self.w is not None: # Make sure it is closed.
            self.w.close()
            self.w = None # Avoid duplicate closing on termination

        # TODO: restore observers.
        """Gets called if the tool sets the tool observer
        @('currentGlyphChanged', EVENT_CURRENTGLYPHCHANGED),@

        DO NOT REDEFINE IN INHERITING CLASS, or otherwise add the line below to
        remove/add the glyph observers."""
        # By default an observer for "glyphChanged" is added, which is called if
        # the outline or the width of the glyph was changed in the editor.
        #self.setCurrentGlyphObserver(event['glyph'])


    # Updates.

    """Code  that handles the request for an update (e.g.  vanilla fills,
    redraws, etc.).

    Callbacks that are part of an event (e.g. setting a list content which
    causes the update callback for that list be called), should only set the
    request, not actually execute the update."""

    def registerUpdaters(self, registeredUpdates):
        """Register the list of update request name and the methods to be
        called.  registeredUpdates has format [('updateList', 'updateList'),
        ...]"""
        # Make dictionary for fast access.
        self._registeredUpdateMethods = {}
        # Keep the defined order.
        self._registeredUpdateIds = []

        for updateName, updateMethodName in registeredUpdates:
            assert hasattr(self, updateMethodName), 'Missing method name "%s"' % updateMethodName
            self._registeredUpdateMethods[updateName] = getattr(self, updateMethodName)
            self._registeredUpdateIds.append(updateName)

        self.clearPendingUpdates()

    def clearPendingUpdates(self):
        # Request ID's, connected to optional data to distract the rect from.
        self._pendingUpdateData = {}
        self._pendingUpdates = []

        # We can reset, because we know that we started the update.
        self._updating = False

    def requestUpdate(self, names, updateInfo=None):
        """Add the name-type of update to be added to the pending list. Names
        can be a single update name or a list/tuple with update names. If we
        are already in updating mode, no more requests can be added.  They will
        be ignored. This happens if updating callbacks are happening during the
        execution of the pending updates. It's "too late" to add new ones. Call
        update first before new requests will be stored.  In case info is
        defined, request an update of the rect defined by the data. This can be
        a rectangle, but also the glyph/name the changed, so the calling
        application needs to figure out later how to distract the rect from
        this data.

        The optional updateInfo can contain the rectangle that must be
        updated."""
        if self._updating:
            return

        if not isinstance(names, (tuple, list)):
            names = [names]

        for name in names:
            assert name in self._registeredUpdateIds, 'Unregistered method name "%s"' % name

            # Make sure the request is only added once to the pending update
            # list. Just add once, ignore other requests with the same name.
            if not name in self._pendingUpdateData:
                # Can be None if the update doesn't not need info for update
                # rect.
                self._pendingUpdateData[name] = updateInfo

                # Collect update names, so we can find the ordered methods
                # while updating.
                self._pendingUpdates.append(name)

    def update(self):
        """Run through the aggregated update requests, execute the methods in
        the order of registered methods."""
        from time import time

        # If already in updating mode, then ignore.
        if not self._updating:
            # Run through the list of pending updater names.
            for name in self._pendingUpdates:
                # If there is any info supplied to determine the update rect,
                # then pass it on.
                info = self._pendingUpdateData[name]

                # Execute the method with the intended data as resource for the
                # calling tools to decide on which part to update.  Info can be
                # None if the request was made without additional info.
                if name in self._registeredUpdateMethods:
                    self._registeredUpdateMethods[name](info)
                else:
                    print('### [Error] TRYING TO UPDATE', name, info, 'Missing updater method.')
            # We updated, now clear the pending list for next set of requests.
            # Also clears the self._updating flag.
            self.clearPendingUpdates()
