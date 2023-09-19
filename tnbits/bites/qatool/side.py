# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    side.py
#
from AppKit import NSClipView
from vanilla import CheckBox, Group, SegmentedButton
from tnbits.base.samples import *
from tnbits.base.constants.colors import *
from tnbits.base.constants.tool import *
from tnbits.base.text import *
from tnbits.base.views import *
from tnbits.bites.qatool.constants import *
from tnbits.bites.qatool.transformer import *
from vanilla import Group, ScrollView
from tnbits.qualityassurance.qamessage import getTitle
from tnbits.base.view import View

COLWIDTH = 2*SIDE - 3*PADDING
INDENT = 80
COMBOWIDTH = COLWIDTH - INDENT
LINE = BUTTON_HEIGHT
MAXLINES = 12
H = MAXLINES * LINE

class Side(View):
    """Adds buttons to a group view. Group view itself is embedded in a scroll
    view."""

    def __init__(self, controller):
        """Adds all available QA functions to the view, grouped by
        category."""
        self.controller = controller
        self.groups = {}
        self.currentGroupName = None
        pos = (0, 0, 2*SIDE - 2*PADDING, H)
        self.view = Group(pos)
        nsView = self.getNSView()
        nsView.setFlipped_(True)
        self.build()

    # Views.

    def getController(self):
        return self.controller

    def getView(self):
        return self.view

    def getNSView(self):
        return self.view.getNSView()

    def getGroup(self, category):
        groupName = self.getGroupName(category)
        return self.groups[groupName]

    # Build.

    def selectGroupCallback(self, sender):
        i = sender.get()
        category = categoryOrder[i]
        self.currentGroupName = self.getGroupName(category)

        for n, g in self.groups.items():
            if n == self.currentGroupName:
                self.show(g)
            else:
                self.hide(g)

    def build(self):
        """Assembles QA function checkboxes."""
        padding = 8
        x = padding
        y = -padding - LINE
        items = []

        for category in categoryOrder:
            title = getTitle(category)
            items.append(dict(title=title))
        self.view.sb = SegmentedButton((x, y, -10, 20), items,
                callback=self.selectGroupCallback, sizeStyle='mini')

        y = -H - 2*LINE
        W = 2*SIDE + 2*PADDING
        hidden = False

        for category in categoryOrder:
            group = self.buildGroup(category, x, y, W, H, hidden=hidden)
            groupName = self.getGroupName(category)
            self.groups[groupName] = group
            setattr(self.view, groupName, group)
            hidden = True

    def buildGroup(self, category, x, y, w, h, hidden=True):
        group = Group((x, y, w, h))
        label = category + 'Label'

        y1 = 0

        for function in allFunctions[category]:
            flagName = getFlagName(category, function)
            title = getTitle(function)
            flag = getattr(self.controller, flagName)
            t = getAttributedString(title)

            setattr(group, flagName, CheckBox((20, y1, 2*SIDE-8, 16),
                    t, sizeStyle='small', value=flag,
                    callback=self.controller.savePreferences))

            y1 += LINE

        group.getNSView().setHidden_(hidden)
        return group

    def hide(self, g):
        g.getNSView().setHidden_(True)

    def show(self, g):
        g.getNSView().setHidden_(False)

    def getGroupName(self, category):
        return '%sGroupView' % category

    # Update.

    def update(self):
        controller = self.getController()
        tool = controller.getTool()
        preferences = tool.getPreferences()

        for key, value in preferences.model.items():
            view = None
            t = value['type']

            if hasattr(self.view, key):
                view = self.view

            if view:
                attr = getattr(view, key)
                if t == PREFTYPE_BOOL:
                    v = preferences.getPreference(key)
                    attr.set(v)

class MyClipView(NSClipView):
    """Wraps an NSClipView to determine bounds and tell if frame has changed
    (scrolled)."""

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, parent):
        self.parent = parent

    '''
    def viewBoundsChanged_(self, notification):
        super(MyClipView, self).viewBoundsChanged_(notification)

    def viewFrameChanged_(self, notification):
        super(MyClipView, self).viewFrameChanged_(notification)
        #self.centerDocument()
    '''
