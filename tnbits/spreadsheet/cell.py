# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    cell.py
#

import weakref
from vanilla import EditText
from vanilla.vanillaBase import VanillaCallbackWrapper
from tnbits.toolbox.transformer import TX

class Cell(object):

    def __init__(self, value=None, identifier=None, enabled=True):
        self.value = value
        self.identifier = identifier
        self.enabled = enabled

    def __repr__(self):
        return '[%s, %s]' % (self.identifier, self.asString())

    def asString(self):
        if self.value is None:
            return ""
        return TX.asString(self.value)

class EditCell(EditText):
    """Edit box of the selected cell. The box is hidden or moved to the
    position of the selected cell. Also the size to the selected column width
    is adusted."""

    def _setCallback(self, callback):
        if callback is not None:
            self._target = EditCellDelegate(callback)
            self._target._continuous = self._continuous
            self._nsObject.setDelegate_(self._target)
            self._target.parent = weakref.ref(self)

class EditCellDelegate(VanillaCallbackWrapper):
    """The EditCellDelegate is used by the edit box, when in selection entry
    mode."""
    _continuous = True

    def controlTextDidChange_(self, notification):
        if self._continuous:
            self.action_(notification.object())

    def controlTextShouldBeginEditing_(self, notification):
        if self._continuous:
            self.action_(notification.object())

    def controlTextDidBeginEditing_(self, notification):
        if self._continuous:
            self.action_(notification.object())

    def controlTextShouldEndEditing_(self, notification):
        if self._continuous:
            self.action_(notification.object())

    def controlTextDidEndEditing_(self, notification):
        if self._continuous:
            self.action_(notification.object())
            parent = self.parent()

            if parent is not None:
                parent.editCellEnded()
