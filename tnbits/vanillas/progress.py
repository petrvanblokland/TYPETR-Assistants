# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     progress.py
#
import vanilla
from defconAppKit.windows.progressWindow import ProgressWindow

class Progress(ProgressWindow):
    """The `Progress` class is a redefine of the Vanilla `ProgressWindow` to
    have a text and title line in the window. All other calls are identical, so
    a code writing to a progress window will change the text, not the title."""
    def __init__(self, title=None, text=None, tickCount=None, parentWindow=None):
        if parentWindow is None:
            self.w = vanilla.Window((250, 72), closable=False,
                    miniaturizable=False, textured=False)
        else:
            self.w = vanilla.Sheet((250, 72), parentWindow)

        if tickCount is None:
            isIndeterminate = True
            tickCount = 0
        else:
            isIndeterminate = False

        self.w.progress = vanilla.ProgressBar((15, 15, -15, 10),
                maxValue=tickCount, isIndeterminate=isIndeterminate,
                sizeStyle="small")

        self.w.title = vanilla.TextBox((15, 32, -15, 14), title or '',
                sizeStyle="mini")
        self.w.text = vanilla.TextBox((15, 48, -15, 14), text or '',
                sizeStyle="small")
        self.w.progress.start()
        self.w.center()
        self.setUpBaseWindowBehavior()
        self.w.open()

    def set(self, text=None, title=None):
        if title is not None:
            self.w.title.set(title)
            self.w.title._nsObject.display()
        if text is not None:
            self.w.text.set(text)
            self.w.text._nsObject.display()

    def update(self, text=None, title=None):
        '''Text is first, to be compatible with ProgressWindow call.'''
        self.w.progress.increment()
        self.set(text, title)
