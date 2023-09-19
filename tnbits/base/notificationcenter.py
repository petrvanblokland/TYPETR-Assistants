# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    notificationcenter.py

import traceback
from tnbits.base.c import *
from tnbits.model import model
from mojo.events import addObserver, removeObserver

class NotificationCenter(object):
    """Default observers. Open and close callbacks are necessary for
    updateStyles() to work correctly. Optionally redefined by tool.
    Consists of tuples:

     (Callback, eventName)

    NOTE: callback name has to be different from event name."""

    def __init__(self, tool):
        self.tool = tool

    #   Events & notification observers.

    def style2Front(self, style):
        """Make _font_ the front window and set to current font."""
        style.document().getMainWindow().getNSWindow().makeKeyAndOrderFront_(None)

    def _fontDidClose(self, sender):
        model.fontDidClose(sender)

    def _fontDidOpen(self, sender):
        model.fontDidOpen(sender)

    def _fontDidSave(self, sender):
        pass

    # Observers.

    def getToolObservers(self):
        """Answer the observers to be installed for this tool."""
        return self.tool.getObservers()

    def addObservers(self):
        """The tool defines the observer it wants to have. Note that this is
        additional to the normal notifications, and observer is required to
        get notifications if the tool is not active."""
        for callbackName, eventName in self.getToolObservers():
            self.addObserver(self.tool, callbackName, eventName)

    def addObserver(self, model, callbackName, eventName):
        """Add the observer."""
        addObserver(model, callbackName, eventName)

    def removeObservers(self):
        """Remove all current observers for this tool."""
        for _, eventName in self.getToolObservers(): #  callbackName, eventName
            removeObserver(self, eventName)

    def setCurrentGlyphObserver(self, glyph=None):
        """This method is a construction to remove the "Glyph.Changed"
        and "Glyph.WidthChanged" observers from the current "self._glyph"
        (if it is set) and then set observers on the new current glyph
        (if it exists). If there is no current glyph, then @self._glyph"
        is set to @None@."""
        # TODO: This needs to be fixed in a more generalized way. Not store current glyph
        # TODO: and get it from the event?

        if not hasattr(self, '_glyph'):  # Make sure it exists
            self._glyph = None

        '''
        # FIXME: doesn't exist (yet) in floqmodel.
        if self._glyph is not None:
            self._glyph.removeObserver(self, "Glyph.Changed")
            self._glyph.removeObserver(self, "Glyph.WidthChanged")
        '''

        if glyph is None:
            glyph = self.getCurrentGlyph()

        self._glyph = glyph

        if self._glyph is not None:
            try:
                # FIXME: Observers are added multiple times.
                # catching error for now.
                self._glyph.addObserver(self, "glyphChanged", "Glyph.Changed")
                self._glyph.addObserver(self, "glyphChanged", "Glyph.WidthChanged")
            except:
                print('Error in NotificationCenter.setCurrentGlyphObserver():')
                print('Cannot add observer "Glyph.Changed"')
                print(traceback.format_exc())
