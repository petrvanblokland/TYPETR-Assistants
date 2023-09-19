# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     iconview.py
#
from AppKit import NSView, NSMakeRect, NSColor, NSRectFill
from tnbits.base import future

class IconNSView(NSView):

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, dimensions, path=None, color=None, backgroundColor=None):
        w, h = dimensions
        self.setFrame_(NSMakeRect(0, 0, w, h))
        self._path = path
        if color is None:
            color = NSColor.blackColor()
        self._color = color
        if backgroundColor is None:
            backgroundColor = NSColor.whiteColor()
        self._backgroundColor = backgroundColor
        self._bezelStyle = None
        self._drawsBackground = True
        self._s = 'a'

    def setTextColor_(self, color):
        self._color = color

    def getTextColor(self):
        return self._color

    def setBezelStyle_(self, bezelStyle):
        self._bezelStyle = bezelStyle

    def getBezelStyle(self):
        return self._bezelStyle

    @future.python_method
    def setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor

    def getBackgroundColor(self):
        return self._backgroundColor

    @future.python_method
    def setDrawsBackground(self, flag):
        self._drawsBackground = flag

    def drawsBackground(self):
        return self._drawsBackground

    def setUpFieldEditorAttributes_(self, attributes):
        pass

    def setWantsNotificationForMarkedText_(self, flag):
        pass

    def setPlaceholderString_(self, s):
        pass

    def placeholderString(self):
        return ''

    def setPlaceholderAttributedString_(self, s):
        self._s = s

    def placeholderAttributedString(self):
        return self._s

    def allowedInputSourceLocales(self):
        return True

    def setAllowedInputSourceLocales_(self, flag):
        pass

    def drawRect_(self, rect):
        if self._drawsBackground:
            self._backgroundColor.set()
            NSRectFill(rect)
        if self._path is not None:
            self._color.set()
            self._path.fill()
