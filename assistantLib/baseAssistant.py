# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR baseAssistant.py
#
#    The BaseAssistantSubscriber provides both an example template as base class for writing Assistant tools,
#    with specific knowledge about a typedesign project.
#

import os
import AppKit

# Import the main entry into RoboFont subscriber and window controller classes and functions.
from mojo.subscriber import (Subscriber, WindowController, 
    registerGlyphEditorSubscriber, disableSubscriberEvents, getRegisteredSubscriberEvents,
    unregisterGlyphEditorSubscriber, registerSubscriberEvent)
from mojo.events import postEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RFont, RGlyph, RPoint, CurrentGlyph, CurrentFont

# Get the vanilla controls that are used in the UI window
from vanilla import (Window, FloatingWindow, TextBox, EditText, PopUpButton, RadioGroup, 
    CheckBox, Slider, List, Button, HorizontalRadioGroup)

# Unique key to identify Assistant events coming from helpers.
DEFAULT_KEY = 'com.typetr.Assistant'

# PreviewDesignspace events
EVENT_DO_OPEN_EDITWINDOW = f"{DEFAULT_KEY}.doOpenEditWindow"
EVENT_SAVE_ALL = f"{DEFAULT_KEY}.saveAll"

class BaseAssistantSubscriber(Subscriber):
    """This class interacts with the glyphs and UFO’s through events. It also holds
    the Merz objects that are drawn in the EditorWindow that belongs to this Assistant subscriber.
    Each EditorWindow gets its own Assistant, so there is not confusion about what the current
    glyph is. 
    All Assistant-Subscriber instances talk to the same AssistantController, sharing the window
    of controls, following up on events. 
    """
    debug = True
    controller = None
    VERBOSE = False # Set to True for debugging the tool

    FAR = 100000 # Move Merz objects here to get them out of view.
   
    def build(self):
        # Build the Assistant subscriber object
        if self.VERBOSE:
            print('--- build')

        self.windowControllers = []

        # Get the GlyphEditor that relates to self.
        glyphEditor = self.getGlyphEditor()

        self.foregroundContainer = glyphEditor.extensionContainer(
            identifier="com.typetr.%s.foreground" % self.__class__.__name__,
            location="foreground",
            clear=True
        )
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.typetr.%s.background" % self.__class__.__name__,
            location="background",
            clear=True
        )

        """Register the events for this subscriber. The methodName is the method self.method responds to."""
        registerSubscriberEvent(
            subscriberEventName=EVENT_DO_OPEN_EDITWINDOW,
            methodName="doOpenEditWindow",
            lowLevelEventNames=[EVENT_DO_OPEN_EDITWINDOW],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_SAVE_ALL,
            methodName="saveAll",
            lowLevelEventNames=[EVENT_SAVE_ALL],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        self.buildAssistant() # Build specifics of inheriting assistant classes.

    def buildAssistant(self):
        """Build the rest of the Assistant subscriber, such as adding all Merz drawing object,
        in case the inheriting class wants to draw in the related EditorWindow.
        To be redefined by inheriting Assistant-Subscriber classes.
        Default behavior is to do nothing.
        """
        print('### BaseAssistantSubscriber.buildAssistant should be redefined by the inheriting Assistant class.')

    def destroy(self):
        """This is called if the glyphEditor is about to get closed. 
        All containers are released there and so it the event binding."""
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(DEFAULT_KEY, location='background')
        container.clearSublayers()

    #   G L Y P H

    def getGlyph(self):
        """Answer the glyph in the GlyphEditor that relates to this subscriber. This answer a DoodleGlyph"""
        glyphEditor = self.getGlyphEditor()
        #print(glyphEditor.getGlyph().__class__.__name__)
        #print(CurrentGlyph().__class__.__name__)
        return glyphEditor.getGlyph()

    def getCurrentGlyph(self):
        return CurrentGlyph()

    def getCurrentFont(self):
        return CurrentFont()

    #   E V E N T S

    def doOpenEditWindow(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.doOpenEditWindow {info['lowLevelEvents'][0]['info']['ufoName']}")

    def glyphEditorDidSetGlyph(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.glyphEditorDidSetGlyph {info['glyph'].name}")

    def glyphEditorDidMouseUp(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.glyphEditorDidMouseUp {info['glyph'].name}")

    def glyphEditorDidMouseDrag(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.glyphEditorDidMouseDrag {info['glyph'].name}")

    def glyphEditorGlyphDidChangeSelection(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.glyphEditorGlyphDidChangeSelection {info['glyph'].name}")

    def currentFontDidSetFont(self):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.currentFontDidSetFont")
        
    def fontDocumentDidOpen(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.fontDocumentDidOpen {info['font'].path}")
        
    def fontDocumentDidClose(self, info):
        if self.VERBOSE:
            print(f"--- {self.__class__.__name__}.fontDocumentDidClose")

    def saveAll(self, info):
        # Save all open fonts and all fonts that are in the global openFonts dictionary.
        print(f'--- {self.__class__.__name__}.saveAll')
        for f in AllFonts():
            f.save()
        for ufoPath, f in openFonts.items():
            f.save()

class BaseAssistantController(WindowController):
    """Define the base class the creates the UI window for the assistant tool.
    Inheriting controller classes can define required functions by setting class flags to True.

    This class mostly just defines the window, controls and interactions, calling events
    for the Assistant-Subscriber to perform tasks on glyphs and UFO’s.

    Helpers are generic tools that can perform a series of tasks. They know how to build their
    part of the interface. They instruct the Assistant on which events the want to respond
    and they know how to perform theirs tasks on glyph, current UFO or all UFOs.
    Helpers can draw in the EditorWindow through Merz objects. And they can construct their
    own window or canvas.
    The selection and order of the helpers defines their top-down order in the Assistant window.
    """
    WINDOW_CLASS = Window # Or FloatingWindow
    subscriberClass = BaseAssistantSubscriber
    debug = True
    VERBOSE = False

    TITLE = 'Assistant'

    X = Y = 50 # Position of the window, should eventually come from preference storage.
    W, H = 400, 600 # Width and height of controller window
    MINW, MINH, MAXW, MAXH = W, H, 3 * W, 3 * H # Min/max size of the window
    M = 8 # Margin and gutter
    L = 20 # Line height between controls
    LL = 32 # Line height between functions
    BH = 32 # Button height
    TBH = 24 # Text box height
    LH = 24 # Label height
    POBH = 24 # Popup button height
    CW = (W - 4 * M) / 3 # Column width
    CW2 = 2 * CW + M # Column width
    C0 = M # X position of column 0
    C1 = C0 + CW + M # X position of column 1
    C2 = C1 + CW + M # X position of column 2
    
    TITLE = subscriberClass.__name__ # Default is class subscriber class name
    
    def build(self):
        self.fonts = {}
        self.w = self.WINDOW_CLASS((self.X, self.Y, self.W, self.H), self.TITLE, 
            minSize=(self.MINW, self.MINH), maxSize=(self.MAXW, self.MAXH))
        self.buildUI()
        self.w.open()

    def buildUI(self):
        """For inheriting classes to define the building of the user interface."""
        pass
        
    def started(self):
        self.subscriberClass.controller = self
        registerGlyphEditorSubscriber(self.subscriberClass)

    def destroy(self):
        unregisterGlyphEditorSubscriber(self.subscriberClass)
        self.subscriberClass.controller = None

    #   F O N T

