# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     memeparser.py
#
#    http://www.dabeaz.com/ply/ply.html#ply_nn6
#
#===========================================================================
# indicates comment until the end of the line (same as in Python)
# + is adding two glyphs as component.
# @top @center @bottom reference to anchor points, there can be more name, @xheight, @ascender (to make the difference between accents on bowl or ascender with "d"
# /glyphname (same as in SpaceCenter) to make difference between keywords and glyph names
# /glyphname.width (attribute of a glyph)
# comma: component separator
# X: Y: D: projections/directions
# = is an action or contextual retrieval of value
# single names, e.g. verticalCounter, serif and rectangle: drawing entities
# 
# Agrave
# /A + @top /gravecomb # Add A and gravecomb glyph, using the top anchor
# 
# D
# X: /H.lsb, /H.stem, >/O.counter & H<, /O.stem, /O.rsb
# Y: /H.alignments, /H.bar, verticalCounter, /H.bar
# Pressure: width.condensed /O.rsb
# 
# I
# X: /H.lsb, /H.stem[0], /H.rsb
# Y: /H.alignments
# 
# ndash
# X: /hyphen.lsb, rectangle.width=fill, width=em/2
# Y: /hyphen.bottom, rectangle.height=/H.bar
# 
# parenright
# X: /parenleft.rsb, /parentleft=fliph, /parentleft.lsb
# Y: /parenleft.alignments
# 
# m
# X: /n.lsb, /n.stemp[0], /n.counter, /n.stem[1], /n.counter, /n.stem[1]. /n.rsb
# Y: /n.alignments
# 
# one
# X: center /H.stem[0] center, width=em/2
# Y: /H alignments, serif.bottom, rectangle, serif.topLeft
#
#    ssb = straight side bearing
#    -n = miniumum
#    (…) = body
#    sstem = straight stem
#    sbasealign = square baseline alignment,
#    xht = x height alignment
#    rs = round stem
#
#    Script: Latin
#        Class: Sans
#            Subsclass: Humanist
#                Glyph Class: Lowercase
#                    Size Master: 12pts
#    G: /n;
#    X: ssb1!1 (sstem!1 counter {ssb1 ssb2} sstem!1), ssb2!0;
#    Y: sbasealign.sstem sbasealign.sstem xht!3, xht.overshoot rstem!1
#
#    G: /o;
#    X: rsb!1 (rstem!1 counter rstem!1) rsb!0;
#    Y: basealign.undershoot rstem!1 xht!3 xht.overlap rstem!1
#
#    G: /p;
#    X: ssb!1 (sstem!1, counter {/o} rstem!1) rsb!0;
#    Y: sdescentalign basealign undershoot rstem!1 xht!3, xht.overlap rstem!1
#
#    G: Adieresis {/A /dieresis@top};
#    X: A.lsb!1 A.rsb!0
#
#    G: /n;
#    X: /n.ssb!1 (sstem!1, counter {ssb ssb} sstem!1) /n.ssb!0
# 
#===========================================================================

import sys
sys.path.insert(0,"../..")

class BaseMemeTool(object):
    TYPE = 'type'
    TYPE_MEME = 'meme'
    TYPE_EXPRESSION = 'expression'
    TYPE_GLYPH = 'glyph'
    TYPE_GROUP = 'group'
    TYPE_ASPECT = 'aspect'
    TYPE_PARAMETER = 'parameter'
    TYPE_MINUS = 'minus'
    TYPE_ANCHOR = 'anchor'
    TYPE_POSITION = 'position'

    ATTR_TYPE = 'type'
    ATTR_NAME = 'name'
    ATTR_SELECTOR = 'selector'
    ATTR_CONSTRUCTOR = 'constructor'
    ATTR_POSITION = 'position'
    ATTR_ATTRIBUTES = 'attributes'
    ATTR_ASPECTS = 'aspects'
    ATTR_DIMENSIONS = 'dimensions'
    ATTR_PIXEL = 'pixel'
    ATTR_ASPECTS = 'aspects'
    ATTR_EXPRESSION = 'e'
    ATTR_EXPRESSION1 = 'e1'
    ATTR_EXPRESSION2 = 'e2'
    ATTR_OPERATOR = 'operator'

