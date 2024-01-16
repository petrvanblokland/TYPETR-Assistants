# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR tp_q2b2q.py
#

from vanilla import TextBox, EditText, CheckBox, RadioGroup, Slider

# Import the main entry into RoboFont subscriber and window controller classes and functions.
from mojo.subscriber import (Subscriber, WindowController, 
    registerGlyphEditorSubscriber, disableSubscriberEvents, getRegisteredSubscriberEvents,
    unregisterGlyphEditorSubscriber, registerSubscriberEvent)
from mojo.events import postEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint

from .baseAssistant import BaseAssistant

class Q2B2Q(BaseAssistant):

    # Q2B2Q events
    EVENT_Q2B = f"{DEFAULT_KEY}.Q2B"
    EVENT_B2Q = f"{DEFAULT_KEY}.B2Q"
