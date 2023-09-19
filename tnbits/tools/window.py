# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     window.py
#

from vanilla.vanillaWindows import FloatingWindow, Window, _calcFrame
from vanilla.vanillaBase import _flipFrame

# DEPRECATED?

class FloatingScreenWindow(FloatingWindow):
    """
    Inherits from FloatingWindow to redefine some methods that give errors in vanilla plain
    windows, for parent-child windows that run off the screen.
    """
    pass

class ScreenWindow(Window):
    """Overwrite the screen position corrections of the standard Vanilla window."""
    pass
