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
#    log.py
#

from vanilla import Window
from tnbits.base.console import Console

class Log():
    """Window that showss all TN log messages."""

    def __init__(self, maxLines=30):
        self.console = Console(self, addDateTime=False, showFlags=False)
        self._isOpen = False
        self.maxLines = maxLines

    # Window.

    def open(self):
        """Sets up a new window and adds the console."""
        self.w = Window((400, 300), "TN Log", closable=True,
                minSize=(400, 300), maxSize=(1200, 800))
        self.w.console = self.console.getView()
        self.bind()
        self.w.open()
        self._isOpen = True
        self.set()

    def show(self):
        if self._isOpen is False:
            self.open()

        self.w.show()

    def closeCallback(self, sender):
        """Close callback after pressing close button in the title bar."""
        self.terminate()

    def close(self):
        """Callable close function."""
        self.w.close()
        self.terminate()

    def terminate(self):
        """Finalizes window close."""
        self._isOpen = False
        self.unbind()
        self.w = None

    def bind(self):
        self.w.bind('close', self.closeCallback)

    def unbind(self):
        if self.w is not None:
            self.w.unbind('close', self.closeCallback)

    # Console.

    def set(self):
        if self._isOpen:
            self.console.setLines(numberOfLines=self.maxLines)

    def message(self, msg):
        self.console.message(msg)
