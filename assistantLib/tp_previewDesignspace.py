# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR tp_previewOverlay.py
#

from vanilla import TextBox, EditText, CheckBox, RadioGroup, Slider
from merz import MerzView

# Import the main entry into RoboFont subscriber and window controller classes and functions.
from mojo.subscriber import (Subscriber, WindowController, 
    registerGlyphEditorSubscriber, disableSubscriberEvents, getRegisteredSubscriberEvents,
    unregisterGlyphEditorSubscriber, registerSubscriberEvent)
from mojo.events import postEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint, CurrentFont

from assistantLib.baseAssistant import BaseAssistant, BaseAssistantController, DEFAULT_KEY
from assistantLib.helpers import *

# PreviewDesignspace events
EVENT_PREVIEW_DESIGNSPACE_CHANGED = f"{DEFAULT_KEY}.previewDesignspaceChanged"

class PreviewDesignspace(BaseAssistant):

    VERBOSE = False
    
    def buildAssistant(self):
        """This instance is part of the BaseAssistantController.helpers list, which defines 
        how the Assistant window is building together.
        Build the rest PreviewDesignspace assistant by adding Merz objects into the @subscriber.
        The subscriber should be stored in the helper, since there can be many subscribers 
        for one controller. 
        """
        if self.VERBOSE:
            print('--- PreviewDesignspace.buildAssistant')
        
        """Register the events for this subscriber. The methodName is the method self.method responds to."""
        registerSubscriberEvent(
            subscriberEventName=EVENT_PREVIEW_DESIGNSPACE_CHANGED,
            methodName="previewOverlayDidChange",
            lowLevelEventNames=[EVENT_PREVIEW_DESIGNSPACE_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )

    def glyphEditorDidSetGlyph(self, info):
        if self.VERBOSE:
            print('--- PreviewDesignspace.glyphEditorDidSetGlyph /%s' % info['glyph'].name)
        self.controller.glyphEditorDidSetGlyph(info)

    def glyphEditorDidMouseUp(self, info):
        # Pass this on to the window controller. How to do this better?
        print('--- PreviewDesignspace. glyphEditorDidMouseUp')

    def glyphEditorDidMouseDrag(self, info):
        # Pass this on to the window controller. How to do this better?
        print('--- PreviewDesignspace. glyphEditorDidMouseDrag')

    def doOpenEditWindow(self, info):
        ufoPath = info['lowLevelEvents'][0]['info']['ufoName']
        dirPath = getUfoDirPath(CurrentFont())
        f = getFont(dirPath + ufoPath)
        if self.controller.showInterface.get():
            f.openInterface()
        g = info['lowLevelEvents'][0]['glyph']
        if g.name in f:
            OpenGlyphWindow(f[g.name])

class PreviewDesignspaceController(BaseAssistantController):

    subscriberClass = PreviewDesignspace

    # Left/right position of the slider
    
    TITLE = 'Preview Designspace'
    MASTER_LOCATIONS = {} # Define by inheriting class

    debug = True

    W = 600 # Width of designspace canvas window
    H = 600
    M = ML = MR = MT = 8 # Margin and gutter
    MB = 16

    def acceptsFirstResponder(self, sender):
        # necessary for accepting mouse events
        return True

    def acceptsMouseDown(self, sender):
        # necessary for tracking mouse down
        return True

    def mouseDown(self, view, event):
        print('--- mouseDown', view, event)

    def buildUI(self):
        """This needs to become a more generalized version. For now see the specific: 
        SegoePreviewDesignspaceController instead.
        """
        self.lastMouseGrid = None # Save the last mouse grid click
        self.lastMouse = None # Actual position of last mouse click
        self.lastMouseDrag = None # Actual position of last mouse drag
        self.selectedDragPoints = None # Storage of selected points, while dragging

        self.w.view = MerzView(
            (self.ML, self.MT, -self.MR, -self.MB),
            backgroundColor=(1, 1, 1, 1),
            delegate=self
        )
