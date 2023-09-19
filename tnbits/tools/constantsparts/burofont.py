# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    burofont.py
#

class BuroFont:
    FALSEVALUES = ('', 0, '0', 'f', 'F', 'none', 'None', 'NONE', 'false', 'False', 'FALSE', 'n', 'N', 'no', 'No', 'NO',
                   None, False)

    MAXINT = 100000000

    # F I L E  &  A D A P T E R  T Y P E S

    SQL = 'sql'
    UFO = 'ufo'
    TTF = 'ttf'
    OTF = 'otf'
    GLIF = 'glif' # Extension of Ufo/glif file
    TTX = 'ttx'
    PFB = 'pfb'
    PFA = 'pfa'
    WOFF = 'woff'
    SVG = 'svg'
    FONTFILE_TYPES = (UFO, OTF, TTF, TTX, PFA, PFB, WOFF)

    # P O I N T

    #P_MOVE = 'move'
    #P_LINE = 'line'
    #P_QCURVE = 'qcurve'
    #P_CURVE = 'curve'
    #P_OFFCURVE = 'offCurve' # Can also be None?
    #P_CURVES = (P_CURVE, P_QCURVE)

    # F L O Q

    ROOTID = 'Root' # Fid of the main root floq
    #LIBRARY_FONTBUREAU = 'TypeNetwork.db'

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

    # L A B E L S

    LABEL_OPENFONT = 'Open Font'
    LABEL_SELECTAFONT = 'Selecte a font:'

    # T R U E T Y P E  T A B L E  N A M E S

    #FIXME: similar fields in hinting module.
    HEAD = 'head'
    MAXP = 'maxp'
    CMAP = 'cmap'
    GLYF = 'glyf'
    GSUB = 'GSUB'
    GPOS = 'GPOS'
    GDEF = 'GDEF'
    GASP = 'gasp'
    HMTX = 'hmtx'
    HHEA = 'hhea'
    LOCA = 'loca'
    KERN = 'kern'
    NAME = 'name'
    FPGM = 'fpgm'
    PREP = 'prep'
    OS2 = 'OS/2'
    CFF = 'CFF '
    POST = 'post'

    # C O N T O U R

    C_CW = 'CW' # Contour clockwise direction
    C_CCW = 'CCW' # Contour counter-clockwise direction

    '''
    L = 8 # UI units
    L2 = L+L
    L3 = L2+L

    # V A N I L L A

    VANILLA_MINI = 'mini'

    # L A Y E R S

    LAYER_FOREGROUND = 'Foreground'
    LAYER_BACKGROUND = 'Background'

    # I N F O

    UNITSPEREM = 'unitsPerEm'
    XHEIGHT = 'xHeight'
    CAPHEIGHT = 'capHeight'
    ASCENDER = 'ascender'
    DESCENDER = 'descender'

    '''
