# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     drop.py
#

from AppKit import NSView, NSFilenamesPboardType, NSDragOperationNone, NSDragOperationCopy
from vanilla import Group

class DropNSView(NSView):

    def init(self):
        self = super(DropNSView, self).init()
        # # register for file dropping
        self.registerForDraggedTypes_([NSFilenamesPboardType])
        self._dropCallback = None
        return self

    def setDropCallback_(self, callback):
        self._dropCallback = callback

    def draggingEntered_(self, sender):
        source = sender.draggingSource()
        if source == self:
            return NSDragOperationNone
        return NSDragOperationCopy

    def draggingUpdated_(self, sender):
        source = sender.draggingSource()
        if source == self:
            return NSDragOperationNone
        return NSDragOperationCopy

    def draggingExited_(self, sender):
        return None

    def prepareForDragOperation_(self, sender):
        source = sender.draggingSource()
        if source == self:
            return NSDragOperationNone
        pb = sender.draggingPasteboard()
        files = pb.propertyListForType_(NSFilenamesPboardType)
        return self._proposeDrop(files, testing=True)

    def performDragOperation_(self, sender):
        source = sender.draggingSource()
        if source == self:
            return NSDragOperationNone
        pb = sender.draggingPasteboard()
        files = pb.propertyListForType_(NSFilenamesPboardType)
        return self._proposeDrop(files, testing=False)

    def _proposeDrop(self, files, testing):
        if self._dropCallback is None:
            return False
        return self._dropCallback(files, testing)

class Drop(Group):

    nsViewClass = DropNSView

    def __init__(self, posSize, dropCallback=None):
        super(Drop, self).__init__(posSize)
        self._nsObject.setDropCallback_(dropCallback)

