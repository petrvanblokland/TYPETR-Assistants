# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    preferences.py
#
import os
import plistlib
from tnbits.toolbox.storage.state import State

class Preferences(State):

    PATH = '~/.BuroFontPreferences.plist'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value
        self.read(os.path.expanduser(self.PATH))
        self.windows = {}

    def read(self, path):
        if os.path.exists(path):
            d = plistlib.readPlist(path)
            for key, value in d.items():
                self[key] = value

    def save(self):
        d = {}
        for key, value in self.items():
            if isinstance(value, (int, float, str, tuple, list, dict)):
                d[key] = value
        plistlib.writePlist(d, os.path.expanduser(self.PATH))

