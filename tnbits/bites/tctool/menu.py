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
#    menu.py
#

from tnbits.vanillas.contextmenu import ContextMenu
from tnbits.bites.tctool.constants import *

class Menu():
    """Wraps a context menu on top of the typesetter canvas."""

    def __init__(self, typesetter):
        self.typesetter = typesetter
        menuItems = self.getMenuItems()
        self.contextMenu = ContextMenu(menuItems, typesetter.getNSView(), typesetter)

    def open(self, event):
        self.contextMenu.open(event)

    def getMenuItems(self):
        enabled = True
        menuItems = []
        selectedTextItem = self.typesetter.controller.getSelected()

        if not selectedTextItem or selectedTextItem.missing:
            enabled = False

        d = {"Save": "saveStyleCallback:",
            "Edit Style": "editStyleCallback:",
            "Edit Glyph": "editGlyphCallback:",}

        for t, c in d.items():
            item = dict(title=t, callback=c)
            if t == "Edit Glyph":
                item['enabled'] = enabled

                if enabled:
                    t = "Edit Glyph ‘%s’" % selectedTextItem.name
                    item['title'] = t

            menuItems.append(item)

        self.addFamilyMenu(menuItems)
        self.addWidthsMenu(menuItems)
        self.addGroupsMenu(menuItems)
        self.addDesignSpaceMenu(menuItems)

        return menuItems

    def addItems(self, title, menuItems, d):
        subMenuItems = []

        for t, c in d.items():
            item = dict(title=t, callback=c)
            subMenuItems.append(item)

        menuItems.append(dict(title=title, items=subMenuItems))

    def addFamilyMenu(self, menuItems):
        d = {
            "Open...": "openFamilyCallback:",
            "Close ": "closeFamilyCallback:",
        }

        self.addItems('Family', menuItems, d)

    def addWidthsMenu(self, menuItems):
        subMenuItems = []
        d = {
            "Set .tab Widths": "setTabWidthsCallback:",
            "Set .fwid widths ": "setFwidWidthsCallback:",
            "Set .hwid widths ": "setHwidWidthsCallback:",
            "Set .cmb widths ": "setCmbWidthsCallback:",
        }

        for t, c in d.items():
            item = dict(title=t, callback=c)
            subMenuItems.append(item)

        menuItems.append(dict(title='Widths', items=subMenuItems))

    def addGroupsMenu(self, menuItems):
        subMenuItems = []
        mode = self.typesetter.getEditMode()

        d = {"Add To...": "addToGroupCallback:",
            "New...": "newGroupCallback:",
            "Default": "defaultGroupsCallback:",
            "Fix": "fixGroupsCallback:"}

        for t, c in d.items():
            item = dict(title=t, callback=c)
            subMenuItems.append(item)

        menuItems.append(dict(title='Groups', items=subMenuItems))

    def addDesignSpaceMenu(self, menuItems):
        subMenuItems = []
        d = {"Add to...": "addToDesignSpaceCallback:",
            "Remove from...": "removeFromDesignSpaceCallback:",}

        for t, c in d.items():
            item = dict(title=t, callback=c)
            subMenuItems.append(item)

        menuItems.append(dict(title='Design Space', items=subMenuItems))
