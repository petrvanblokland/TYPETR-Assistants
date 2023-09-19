# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    searchcell.py
#

import weakref
from vanilla.vanillaBase import VanillaCallbackWrapper
from vanilla import EditText

class SearchBox(EditText):
    """Search box on top of a canvas. The box is hidden or moved to the
    position of the selected cell. Also the size to the selected column width
    is adusted."""

    def _setCallback(self, callback):
        if callback is not None:
            self._target = SearchBoxDelegate(callback)
            self._target._continuous = self._continuous
            self._nsObject.setDelegate_(self._target)
            self._target.parent = weakref.ref(self)

class SearchBoxDelegate(VanillaCallbackWrapper):
    """The SearchBoxDelegate is used by the search box, when in selection entry
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
                parent.searchBoxEnded()
