# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.base.constants.filtertags import F

class FloqConstants:
    LIB_FLOQMEMES = 'floqMemesDict' # Old, can be removed if tnbits.toolbox.dimensions is removed.
    LIB_FLOQMEMELIB = 'floqMemeLib' # font.lib dictionary of glyph meme descriptions.
    # Newer version, writes memes as list instead of dictionary
    LIB_FLOQMEMESLIST = 'tnTools.floqMemesList'

    # E X P A N D I N G

    # Root
    EXPAND_ALL = 'all' # Indicate that nothing needs to be expanded here.
    # Style
    EXPAND_META = 'meta'
    EXPAND_LIB = 'lib'
    EXPAND_CHILDREN = 'children'
    EXPAND_FEATURES = 'features'
    EXPAND_INFO = 'info'
    EXPAND_KERNING = 'kerning'
    # Glyph
    EXPAND_WIDTH = 'width'
    EXPAND_CONTOURS = 'contours'
    EXPAND_UNICODES = 'unicodes'
    EXPAND_COMPONENTS = 'components'
    EXPAND_ANCHORS = 'anchors'
    EXPAND_BOUNDINGBOX = 'boundingBox'
    EXPAND_GROUPS = 'groups'
    EXPAND_HINTS = 'hints'

    # Named levels in the floq hierarchy.
    FLOQ_LABELS = {
        F.ITEMTYPE_ROOT: 'Root',
        F.ITEMTYPE_FOUNDRY: 'Foundries',
        F.ITEMTYPE_LIBRARY: 'Libraries',
        F.ITEMTYPE_SERIES: 'Series',
        F.ITEMTYPE_FAMILY: 'Families',
        F.ITEMTYPE_STYLE: 'Styles', # Chart, selected floq value(s) glyph=x and style=y (open fonts of current family)
        F.ITEMTYPE_GLYPH: 'Glyphs', # Chart, floq values=x and glyph=y (for current font)
    }
    FLOQ_LEVELS = []
    for level in (F.ITEMTYPE_ROOT, F.ITEMTYPE_FOUNDRY, F.ITEMTYPE_LIBRARY, F.ITEMTYPE_SERIES,
                  F.ITEMTYPE_FAMILY, F.ITEMTYPE_STYLE, F.ITEMTYPE_GLYPH):
        FLOQ_LEVELS.append((level, FLOQ_LABELS[level]))

    TYPE2FLOQ = {
        F.ITEMTYPE_ROOT: 'RootFloq',
        F.ITEMTYPE_FOUNDRY: 'FoundryFloq',
        F.ITEMTYPE_LIBRARY: 'LibraryFloq',
        F.ITEMTYPE_SERIES: 'SeriesFloq',
        F.ITEMTYPE_FAMILY: 'FamilyFloq',
        F.ITEMTYPE_STYLE: 'StyleFloq',
        F.ITEMTYPE_GLYPH: 'GlyphFloq',
    }
    FLOQ2TYPE = {}
    for name, className in TYPE2FLOQ.items():
        FLOQ2TYPE[className] = name

    FLOQ_PARENTLEVELS = { # Named levels of level parents
        F.ITEMTYPE_ROOT: None,
        F.ITEMTYPE_FOUNDRY: F.ITEMTYPE_ROOT,
        F.ITEMTYPE_LIBRARY: F.ITEMTYPE_FOUNDRY,
        F.ITEMTYPE_SERIES: F.ITEMTYPE_FOUNDRY,
        F.ITEMTYPE_FAMILY: F.ITEMTYPE_SERIES,
        F.ITEMTYPE_STYLE: F.ITEMTYPE_SERIES,
        F.ITEMTYPE_GLYPH: F.ITEMTYPE_STYLE,
    }
    FLOQ_CHILDLEVELS = { # Named levels of level children
        F.ITEMTYPE_ROOT: F.ITEMTYPE_FOUNDRY,
        F.ITEMTYPE_FOUNDRY: F.ITEMTYPE_LIBRARY,
        F.ITEMTYPE_LIBRARY: F.ITEMTYPE_SERIES,
        F.ITEMTYPE_SERIES: F.ITEMTYPE_FAMILY,
        F.ITEMTYPE_FAMILY: F.ITEMTYPE_STYLE,
        F.ITEMTYPE_STYLE: F.ITEMTYPE_SERIES,
        F.ITEMTYPE_GLYPH: None,
    }
    # Classes that are supported to glue a floq (or analyzer) onto.
    # Don't allow 'DoodleGlyph' and 'DoodleFont' here, make sure to use the wrappers.

    SUPPORTED_FONTGLYPH_CLASSES = ('FBfabWrapperGlyph', 'FBfabWrapperFont', 'DoodleGlyph', 'DoodleFont')

    STYLEATTRIBUTES = (
        'widthvalue',
        'sizevalue',
    )
    GLYPHATTRIBUTES = (
        'leftmargin',
        'width',
        'rightmargin'
    )

