# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     nakedwrapper.py
#
class NakedWrapper(object):
    """Simple wrapper to call RoboFont methods that assume a RoboFont wrapper, where we only
    have the defcon glyph available."""
    def __init__(self, glyph):
        self._nakedGlyph = glyph
        
    def naked(self):
        return self._nakedGlyph
    
