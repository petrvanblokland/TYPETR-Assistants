# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     glyphBuilder.py
#
from tnbits.builders.memes.wgl4 import Memes

class GlyphBuilder(object):

    def __init__(self, memes=None):
        if memes is None:
            memes = Memes()
        self.memes = memes

    def hasScript(self, glyphName):
        hook = 'meme_'+glyphName
        return hasattr(self.memes, hook)

    def build(self, style, glyphName):
        hook = 'meme_'+glyphName
        if hasattr(self.memes, hook):
            if not glyphName in style:
                style.newGlyph(glyphName)
            glyph = style[glyphName]
            getattr(self.memes, hook)(glyph, glyph.getPen())
            return True
        return False

