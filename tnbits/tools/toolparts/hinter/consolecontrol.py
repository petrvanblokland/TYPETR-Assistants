# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010 buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    consolecontrol.py
#

from vanilla import Group, TextBox, Button, CheckBox, PopUpButton, TextEditor
from AppKit import NSView, NSBezierPath, NSColor
import string, os

from fontTools.ttLib import TTFont

class ConsoleControl(Group):
    """Wraps the Console view."""

    C0 = 4

    def __init__(self, posSize, delegate):
        super(ConsoleControl, self).__init__(posSize)
        self.delegate = delegate
        self._setupView(NSView, posSize)
        self.console = TextEditor((self.C0, 0, -0, -0), '', callback=self.consoleCallback)
        textView = self.console.getNSTextView()
        textView.setBackgroundColor_(NSColor.blackColor())
        textView.setTextColor_(NSColor.whiteColor())

    def update(self, msg):
        self.setConsole(msg)
        view = self.getNSView()
        view.setNeedsDisplay_(True)

    def consoleCallback(self, sender):
        pass

    def setConsole(self, msg):
        self.console.set(msg)
