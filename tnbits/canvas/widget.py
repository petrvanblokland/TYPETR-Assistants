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
#    widget.py
#

class Widget(object):
    """Base class for all widgets"""

    def __init__(self, controller, kit, isSelected=False):
        self.controller = controller
        self.kit = kit
        self.isSelected = isSelected
        kit.add(self)

    def draw(self):
        raise NotImplementedError

    def select(self):
        self.isSelected = True
        self.kit.select(self)

    def deselect(self):
        self.isSelected = False
        self.kit.deselect(self)

