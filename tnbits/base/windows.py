# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    windows.py
#
from vanilla import Window
from tnbits.base.constants.colors import *

def setBackgroundColor(window):
    assert isinstance(window, Window)
    window.getNSWindow().setBackgroundColor_(UIBlue)
