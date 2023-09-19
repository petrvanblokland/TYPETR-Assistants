# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    utils.py
#


def getCharacterMapping(style):
    """Create a dictionary of unicode -> [glyphname, ...] mappings. Note that
    this dict is created each time this method is called, which can make it
    expensive for larger fonts. All glyphs are loaded. Note that one glyph can
    have multiple unicode values, and a unicode value can have multiple glyphs
    pointing to it. This method exists inside a RF Wrapper style, but not
    inside a naked style. That is why we implement is here for general
    usage."""
    map = {}

    for glyph in style:
        for u in glyph.unicodes:
            if not u in map:
                map[u] = []
            map[u].append(glyph.name)

    return map
