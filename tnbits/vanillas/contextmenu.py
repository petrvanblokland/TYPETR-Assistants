# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     contextmenu.py
#

from AppKit import NSMenu, NSMenuItem

class ContextMenu():
    """Wrapper around NSMenu.

    TODO: add shortcuts.
    """

    def __init__(self, menuItems, view, target):
        self.view = view
        self.nsMenu = NSMenu.alloc().init()
        self.nsMenu.setAutoenablesItems_(False)

        for d in menuItems:
            self.addMenuItem(d, self.nsMenu, target)

    def addMenuItem(self, d, nsMenu, target):
        """Recursively builds an item from dictionary values and adds it to the
        menu."""

        t = d['title']

        if 'callback' in d:
            c = d['callback']
            menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(t, c, '')
            menuItem.setTarget_(target)

        elif 'items' in d:
            menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(t, '', '')
            nsSubMenu = NSMenu.alloc().init()
            nsSubMenu.setAutoenablesItems_(False)

            for d1 in d['items']:
                self.addMenuItem(d1, nsSubMenu, target)

            menuItem.setSubmenu_(nsSubMenu)

        if 'enabled' in d:
            menuItem.setEnabled_(d['enabled'])
        else:
            menuItem.setEnabled_(True)

        nsMenu.addItem_(menuItem)

    def open(self, event):
        NSMenu.popUpContextMenu_withEvent_forView_(self.nsMenu, event, self.view)

