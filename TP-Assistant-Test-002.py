# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
#     Version 002
# ..............................................................................
#
#     TYPETR Assistant
#
#     A fast and flexible version collections of helpers for type projects.
#

from vanilla import (Window, FloatingWindow, TextBox, EditText, PopUpButton, RadioGroup, List, Button)
from mojo.subscriber import Subscriber, WindowController, getRegisteredSubscriberEvents
from mojo.subscriber import registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.roboFont import OpenWindow
from mojo.events import postEvent

W, H = 500, 450
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/2
CW2 = (CW-M)/2
C0 = M
C1 = C0 + CW + M
VT = 120 # Vertical tab from bottom
FAR = 100000 # Move stuff out of view

WindowClass = Window
#WindowClass = FloatingWindow
#!/usr/bin/env python3

DEFAULT_KEY = 'com.developerName.SomeTool'


class TypolatorController(WindowController):
    """The Controller does not really do anything, beside providing an interface window to the Typolator assistant.
    
    """

    subscriberClass = Typolator

    debug = True
    thickness = 5

    def build(self):
        self.w = FloatingWindow((200, 40), "Tool")
        self.w.slider = Slider((10, 10, -30, 23),
                               minValue=0,
                               value=self.thickness,
                               maxValue=25,
                               stopOnTickMarks=True,
                               tickMarkCount=6,
                               continuous=False,
                               callback=self.sliderCallback)
        self.w.textBox = TextBox((-25, 10, 30, 17), f"{self.thickness:.0f}")
        self.w.open()

    def started(self):
        Tool.controller = self
        registerGlyphEditorSubscriber(Tool)

    def destroy(self):
        unregisterGlyphEditorSubscriber(Tool)
        Tool.controller = None

    def sliderCallback(self, sender):
        self.thickness = sender.get()
        self.w.textBox.set(f"{self.thickness:.0f}")
        postEvent(f"{DEFAULT_KEY}.changed")


class Tool(Subscriber):
    """
    Tool can only ask for information to the palette

    """

    debug = True
    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(identifier=DEFAULT_KEY,
                                                   location='background',
                                                   clear=True)
        self.path = container.appendPathSublayer(
            fillColor=(0, 0, 0, 0),
            strokeColor=(1, 0, 0, 1),
            strokeWidth=self.controller.thickness if self.controller else 0,
        )
        glyph = self.getGlyphEditor().getGlyph()
        self.path.setPath(glyph.getRepresentation("merz.CGPath"))

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(DEFAULT_KEY, location='background')
        container.clearSublayers()

    def glyphEditorGlyphDidChangeOutline(self, info):
        self.path.setPath(info['glyph'].getRepresentation("merz.CGPath"))

    def paletteDidChange(self, info):
        self.path.setStrokeWidth(self.controller.thickness)


# -- Instructions -- #
if __name__ == '__main__':
    eventName = f"{DEFAULT_KEY}.changed"

    # we register the subscriber event only if necessary
    if eventName not in getRegisteredSubscriberEvents():
        registerSubscriberEvent(
            subscriberEventName=eventName,
            methodName="paletteDidChange",
            lowLevelEventNames=[eventName],
            dispatcher="roboFont",
            documentation="Send when the tool palette did change parameters.",
            delay=0,
            debug=True
        )
    OpenWindow(ToolPalette)
