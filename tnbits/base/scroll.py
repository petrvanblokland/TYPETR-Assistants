# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    scroll.py
#
from AppKit import NSClipView
from vanilla import Group, ScrollView
from tnbits.base.constants.colors import *

class ScrollGroup(Group):
    """Wraps a group in a scroll view."""

    def __init__(self, view, posSize, hasHorizontalScroller=True,
            hasVerticalScroller=True, autohidesScrollers=True, w=-0, h=-0):
        super(ScrollGroup, self).__init__(posSize)
        clipView = ScrollClipView(self)
        self.scrollView = ScrollView((0, 0, w, h), view,
                hasHorizontalScroller=hasHorizontalScroller,
                hasVerticalScroller=hasVerticalScroller,
                autohidesScrollers=autohidesScrollers, clipView=clipView, backgroundColor=UIGrey)

    def getView(self):
        """Returns the wrapped scroll view."""
        return self.scrollView

class ScrollClipView(NSClipView):
    """Wraps an NSClipView to determine bounds and tell if frame has changed
    (scrolled)."""

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, parent):
        self.parent = parent

    '''
    def viewBoundsChanged_(self, notification):
        super(ScrollClipView, self).viewBoundsChanged_(notification)

    def viewFrameChanged_(self, notification):
        super(ScrollClipView, self).viewFrameChanged_(notification)
        #self.centerDocument()
    '''
