# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    meme.py
#
from tnbits.toolbox.storage.adict import ADict
from memetalk2dict import MemeTalk2Dict # Get the cached parser instance.
from dict2memetalk import dict2MemeTalk # Get the cached parser instance.

# TODO: See Frederik GlyphConstruction syntax. adieresis = a + dieresis@center,top
# Get position from guidelines too.

class Meme(object):
    """
    The Meme class is a wrapper around a ADict meme instance, as generated
    by the Meme compilers.
    A typical MemeTalk has the syntax:

    g: /A;
    a: @top { X: center Y top+em/10 }:

    g: /Adieresis {/A, /dieresis@top};

    g: /p;
    x: ssb1=1, (sstem=1, counter[1] {ssb[0], /o}, rstem=1), rsb2=0;
    y: sdescentalign, basealign.undershoot, rstem=1, xht=3, xht.overlap, rstem=1


        >>> memeSource_A = '''g: /A;a: @top {y: top + em // 10; x: center} @bottom {y: baseline; x: center}'''
        >>> memeSource_Adieresis = '''g: /Adieresis {/A /dieresis@top};
        ...         x: ssb[0]!1 (sstem!1 counter[0] {ssb[0] ssb[1]} sstem!1) rsb[2]!0;
        ...         y: sbaseline.sstem sbasealign.sstem xht!3 xht.overshoot rstem!1'''

        >>> meme = Meme.fromMemeTalk(memeSource_A)
        >>> meme.anchors[0].dimensions.x
        <NoneList:[{'type': 'aspect', 'name': 'center'}]>
        >>> meme.anchors[0].dimensions.y[0].operator
        '+'
        >>> meme = Meme.fromMemeTalk(memeSource_Adieresis)
        >>> meme.name
        'Adieresis'
        >>> meme.baseGlyph
        'A'
        >>> meme.constructor[1].position
        'top'
    """

    def __init__(self, d):
        assert isinstance(d, (dict, ADict))
        if isinstance(d, dict):
            d = ADict(d)
        self.d = d

    def __repr__(self):
        return '%s' % self.__class__.__name__

    @classmethod
    def fromMemeTalk(cls, memeTalk):
        d = MemeTalk2Dict.compile(memeTalk)
        if d is not None:
            return Meme(d)
        return None

    #   self.name

    def _get_name(self):
        """
            >>> memeSource_A = '''g: /A;a: @top {y: top + em // 10; x: center} @bottom {y: baseline; x: center}'''
            >>> meme = Meme.fromMemeTalk(memeSource_A)
            >>> meme.name
            'A'
        """
        g = self.d.g
        if g is not None and isinstance(g[0], (dict, ADict)):
            return g[0].name
        return None

    name = property(_get_name)

    #   self.constructor

    def _get_constructor(self):
        """Answer the G:constructor of the meme dict."""
        g = self.d.g
        if g is not None and isinstance(g[0], (dict, ADict)):
            return g[0].constructor
        return None

    constructor = property(_get_constructor)

    #   self.baseGlyph      Answer the base glyph name. None if there is not constructor

    def _get_baseGlyph(self):
        """Answer the base glyph of the constructor. Answer None if it does not exist.
            >>> memeSource_Adieresis = '''g: /Adieresis {/A /dieresis@top};
            ...         x: ssb[0]!1 (sstem!1 counter[0] {ssb[0] ssb[1]} sstem!1) rsb[2]!0;
            ...         y: sbaseline.sstem sbasealign.sstem xht!3 xht.overshoot rstem!1'''

            >>> meme = Meme.fromMemeTalk(memeSource_Adieresis)
            >>> meme.baseGlyph
            'A'
        """
        constructor = self.constructor
        if constructor is not None:
            for glyphConstructor in constructor:
                if glyphConstructor.position is None: # No anchor, this must be the base glyph in the constructor.
                    return glyphConstructor.name
        return None

    baseGlyph = property(_get_baseGlyph)

    #   self.anchoredGlyphs     Answer the list of anchored glyph names.

    def _get_anchoredGlyphs(self):
        """Answer the dictionary of all anchored glyph names with their anchor name.
        Answer an empty dictionary if there is are no anchor glyphs found in the constructor or if
        there is no constructor. Note that this only works properly if there never will be two
        glyphs on the same anchor. Does that ever happen?"""
        anchoredGlyphNames = {}
        constructor = self.constructor
        if constructor is not None:
            for glyphConstructor in constructor:
                if glyphConstructor.position is not None: # Test if this glyph has an anchor defined.
                    anchoredGlyphNames[glyphConstructor.position] = glyphConstructor.name
        return anchoredGlyphNames

    anchoredGlyphs = property(_get_anchoredGlyphs)

    #   self.anchors

    def _get_anchors(self):
        """Answer the dictionary of anchors for this meme. Answer None of no anchors are defined."""
        a = self.d.a
        if a is not None:
            return a
        return None

    anchors = property(_get_anchors)

    #   self.memeTalk       Answer the memeTalk source from the content of self.d

    def _get_memeTalk(self):
        return dict2MemeTalk.compile(self.d)

    memeTalk = property(_get_memeTalk)

