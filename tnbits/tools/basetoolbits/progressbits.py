# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    progressbits.py
#
from tnbits.vanillas.progress import Progress

class ProgressBits(object):
    """Bits and pieces for the base tool. All needed to handle fonts and styles."""

    def progressOpen(self, title='', text='', ticks=None, inside=True):
        """Opens the progress window. If ticks is None or omitted, then show
        the progress bar as animated setIndeterminate. Ticks is the amount of
        predicted items that need to be processed.
        """
        if self._progress is None:
            if inside:
                window = self.getWindow()
            else:
                # Forces progress window to be separate floating window.
                window = None
            self._progress = Progress(title=title, text=text, tickCount=ticks,
                    parentWindow=window)
        else:
            self.progressTicks(ticks)
            self.progressSet(title, text)

    def progressUpdate(self, text=None, title=None):
        """Increment the current tick, making the process bar to click to the
        next relative position."""
        if self._progress is not None:
            self._progress.update(title=title, text=text)

    def progressClose(self):
        if self._progress is not None:
            self._progress.close()
            self._progress = None

    def progressTicks(self, ticks):
        """Allows to redefine the amount of items still to be processed."""
        if self._progress is not None:
            self._progress.setTickCount(ticks)

    def progressTitle(self, title):
        self.progressSet(title=title, text=None)

    def progressText(self, text):
        self.progressSet(title=None, text=text)

    def progressSet(self, title=None, text=None):
        if self._progress is not None:
            self._progress.set(title=title, text=text)

    def getProgress(self):
        """
        The `getProgress` method answers the ProgressWindow
        instance, to allow other (parts of) applications to update the
        progressBar.
        """
        return self._progress

