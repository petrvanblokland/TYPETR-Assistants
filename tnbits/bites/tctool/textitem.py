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
#    textitem.py
#

class TextItem:
    """Holds glyph info in the text cache lines."""

    def __init__(self, x=None, index=None, sampleIndex=None, yIndex=None,
            name=None, width=None, kerning=None, missing=None, isRepeat=False,
            glyphIndex=None):
        self.x = x
        self.yIndex = yIndex
        self.index = index
        self.sampleIndex = sampleIndex
        self.name = name
        self.width = width
        self.kerning = kerning
        self.missing = missing
        self.isRepeat = isRepeat


    # TODO: Deep copy.

    def __repr__(self):
        return '<TextItem #%s=\'%s\' (%s, %s)>' % (self.getIdentifier(), self.name, self.x, self.yIndex)

    def getIdentifier(self):
        if self.isRepeat:
            return 'Rsi%d/i%d' % (self.sampleIndex, self.index)
        else:
            return 'si%d/i%d' % (self.sampleIndex, self.index)


