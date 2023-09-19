# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   undomanager.py
#
from tnbits.toolbox.storage.stack import Stack

class UndoManager(object):
    """The UndoManager handle the undo push/pop for the changes to a single glyph."""
    def __init__(self):
        self._undo = Stack()
        self._redo = Stack()
        self.pending = None # Storage of pack between prepareUndo and performUndo

    def prepareUndo(self, message, pack):
        self.pending = message, pack

    def performUndo(self):
        assert self.pending is not None
        self._undo.push(self.pending)
        self.pending = None

    def undo(self):
        messagePack = self._undo.pop()
        if messagePack is not None:
            _, pack = messagePack # message, pack
            self._redo.push(messagePack)
            return pack
        return None

    def redo(self):
        messagePack = self._redo.pop()
        if messagePack is not None:
            _, pack = messagePack # message, pack
            self._undo.push(messagePack)
            return pack
        return None

