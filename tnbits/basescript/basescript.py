# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  T O O L S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    basescript.py
#

from mojo.roboFont import CurrentGlyph
from tnbits.constants import Constants

class BaseScript(object): #StyleBits, GlyphBits, object):
    """The BaseTool class combines functionality for all tools that want to be found
    by the fbProject."""
    C = Constants # Access to constants through self.C, allowing changes by inheriting classes.

    SCRIPTID = None # To be redefined by the inheriting tool class
    NAME = None # To be redefined by the inheriting class
    # To be redefined by inheriting classes. [(eventName, callbackName),...]

    def __init__(self):
        self.name = self.NAME or 'Untitled Script'

    @classmethod
    def getId(cls):
        """Unique script id. Must be refined by inheriting class. Otherwise None,
        to prevent base tool classes to add themselves. Used e.g. to save
        preferences."""
        return cls.SCRIPTID

    def do(self):
        print('### Redefine the self.do method for inheriting script classes.')

    def getGlyph(self):
        """Answers standard CurrentGlyph"""
        return CurrentGlyph()

    getCurrentGlyph = getGlyph
