# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    appresource.py
#
from AppKit import NSApp

from preferences import Preferences

class AppResource(object):
    """Generic NSApp applications."""

    preferences = Preferences() # Read preference from local user directory
    
    @classmethod
    def getCurrentGlyphView(cls):
        return None
        doc = NSApp().currentDocument()
        if doc is None:
            return
        return doc.getCurrentGlyphEditorView()

