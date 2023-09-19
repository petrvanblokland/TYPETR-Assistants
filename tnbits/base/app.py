# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    app.py
#

from tnbits.base.base import Base

class App(Base):
    """Functions shared by all stand alone applications.

    NOTE: parallel functions to Tool, except RoboFont events and observers. All
    shared functionality should go into the shared Base class.

    TODO: add all Tool  functions, put all shared functions in Base.
    """
    RF = False

    def __init__(self):
        super(App, self).__init__()

    def openWindow(self):
        self.w.open()

    def terminate(self):
        self.savePreferences()

    def windowCloseCallback(self, sender):
        self.closeWindow(sender)

        '''
        if self.w is not None:
            self.w.unbind('move', self.isMoved)
            self.w.unbind('resize', self.isResized)
        '''

        self.w = None
        self.terminate()

    def setFamily(self, family):
        pass

    def open(self):
        print('open something')

    def close(self):
        print('close something')

    def save(self):
        print('save something')

    def saveAs(self):
        print('save something as...')

    def terminate(self):
        pass

    def new(self):
        print('something new')

    # Edit.

    def cut(self):
        print('cut something')

    def copy(self):
        print('copy something')

    def paste(self):
        print('paste something')

    def delete(self):
        print('delete something')

    def undo(self):
        print('undo something')

    def redo(self):
        print('redo something')
