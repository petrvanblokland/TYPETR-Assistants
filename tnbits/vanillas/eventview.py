# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     eventview.py
#

import weakref
from AppKit import NSView

class EventView(NSView):

    def isFlipped(self):
        return True

    def isOpaque(self):
        return False

    def getModel(self):
        if hasattr(self, '_model'):
            return self._model()
        return None

    def setModel(self, model):
        self._model = weakref.ref(model)

    def handleEvent(self, name, event):
        model = self.getModel()
        if model is not None and hasattr(model, name):
            getattr(model, name)(event)

    #    M O U S E  E V E N T S

    def mouseDown_(self, event):
        self.handleEvent('mouseDown', event)

    def mouseDragged_(self, event):
        self.handleEvent('mouseDragged', event)

    def mouseUp_(self, event):
        self.handleEvent('mouseUp', event)

    def mouseMoved_(self, event):
        self.handleEvent('mouseMoved', event)

    def mouseEntered_(self, event):
        self.handleEvent('mouseEntered', event)

    def mouseExited_(self, event):
        self.handleEvent('mouseExited', event)

    def rightMouseDown_(self, event):
        self.handleEvent('rightMouseDown', event)

    def rightMouseDragged_(self, event):
        self.handleEvent('rightMouseDragged', event)

    def rightMouseUp_(self, event):
        self.handleEvent('rightMouseUp', event)

    def otherMouseDown_(self, event):
        self.handleEvent('otherMouseDown', event)

    def otherMouseDragged_(self, event):
        self.handleEvent('otherMouseDragged', event)

    def otherMouseUp_(self, event):
        self.handleEvent('otherMouseUp', event)

    #   K E Y

    def keyDown_(self, event):
        self.handleEvent('keyDown', event)

    def keyUp_(self, event):
        self.handleEvent('keyUp', event)

    #   D R A W I N G

    def drawRect_(self, rect):
        model = self.getModel()
        if model is not None:
            model.draw(rect)

    #  S C R O L L I N G

    def scrollPoint_(self, point):
        print(point)

