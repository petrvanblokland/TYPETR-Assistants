# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    hinting.py
#

# Location of hint tables. Don't changes as several
# decompilers and factories assume that the information is there.
# Use the HintLib class to read/write data in the font.
FONTLIB_ROBOHINT = 'com.robofont.fbhint'

# Storage in font.lib[FONTLIB_ROBOHINT]
HINTLIB_PROGRAMS = 'programs'

# Measurement
AXISUNIT = 1

# Default showing depth of stacks
SHOWSTACKSIZE = 3

# Font lib keys
LIB_DATA = 'data'
LIB_ORIGINALS = 'originals'
LIB_GLYPHNAME = 'glyphname'
LIB_SOURCE = 'source'

# TT table names
TABLE_CVT_ = 'cvt '
TABLE_PREP = 'prep'
TABLE_FPGM = 'fpgm'
TABLE_GLYF = 'glyf'
TABLE_GASP = 'gasp'
TABLE_MAXP = 'maxp'
TABLE_OS2 = 'OS/2'

TABLE_CVT_DICT = TABLE_CVT_ + '.dict'

CVT = 'cvt' # CVT label without the space
FLOQ = 'floq' # Identifier of the FloqEditor

# WingEditor name
WINGS = 'wings'
WINGCOMMAND = 'wingcommand'
FLIGHT = 'flight'
ANALYZER = 'analyzer'

# FloqMeme/Wing field names
WINGFIELD_FLOQMEMES = 'floqMemes'
WINGFIELD_CVT = 'cvt'
CVTVALUE_ID = 'id'
CVT_TYPES = [] # TODO: Need to be filled.

ROBOHINT_PASTEBOARDTYPE = 'roboHintPasteBoardType'

# Lib storage paths
# The Winglabel list is automatically derived from the existing winglets.
# Cache paths, for internatl wing caching in self._cacheLib
CACHEPATH_CVT = 'cvt'
CACHEPATH_PREP = 'prep'
CACHEPATH_FPGM = 'fpgm'
CACHEPATH_WINGSET = 'wingset'
CACHEPATH_WINGCOMMANDS = 'wingcommands'

# Lib source paths
LIBPATH_CVT_JSON = CACHEPATH_CVT + '_json'
LIBPATH_PREP_SRC = CACHEPATH_PREP + '_src'
LIBPATH_FPGM_SRC = CACHEPATH_FPGM + '_src'
LIBPATH_WINGSET_JSON = CACHEPATH_WINGSET + '_json'
LIBPATH_WINGCOMMANDS_JSON = CACHEPATH_WINGCOMMANDS + '_json'

JSONTYPES = (dict, list, tuple, str, int, float)

PIXELTYPE_ANTIALIASING = 0
#PIXELTYPE_BLACKWHITE = 1
PIXELTYPE_GRAY = 1
PIXELTYPE_RGB = 2
PIXELTYPE_GBR = 3
PIXELTYPES_SUBPIXEL = (PIXELTYPE_GRAY, PIXELTYPE_RGB, PIXELTYPE_GBR)

WINGCOMMAND_ANTIALIASING = 'aa' # Also used in names of generated font files.
WINGCOMMAND_CLEARTYPE = 'ct'
WINGCOMMAND_BLACKNWHITE = 'bw'
WINGCOMMAND_SPACEPRESERVE = 'sp'
WINGCOMMAND_LABELS = { WINGCOMMAND_ANTIALIASING: 'Anti-aliasing',
                       WINGCOMMAND_CLEARTYPE: 'Cleartype',
                       WINGCOMMAND_BLACKNWHITE: 'Black & white',
                       WINGCOMMAND_SPACEPRESERVE: 'Space constraint',
                    }
WINGCOMMANDIDS = ( WINGCOMMAND_ANTIALIASING, WINGCOMMAND_CLEARTYPE,
                   WINGCOMMAND_BLACKNWHITE, WINGCOMMAND_SPACEPRESERVE)

WINGCOMMAND_DEFAULT = WINGCOMMAND_ANTIALIASING


# Pattern to recognize the hint label in RoboFont Point labels.
# This should never change, since otherwise the labels in existing
# fonts can no longer be found (or write a translation first)
UNIQUEID_PATTERN = '*'
UNIQUEID_SPACE = 10000000 # Add to the index of a space point to make a unique id

# Default ranges for the PPEM selector
PPEM_RANGEMIN = 2
PPEM_RANGEMAX = 48
PPEM_RANGE = range(PPEM_RANGEMIN, PPEM_RANGEMAX+1)
PPEM_RANGESTR = []
for ppem in PPEM_RANGE:
    PPEM_RANGESTR.append(str(ppem))
PPEM_DEFAULT = 16

PPEM_MIN = 10 # Min and max PPEM to apply autohints on
PPEM_MAX = 20

# Tool values
VALUE_POINTRADIUS = 8 # Radius of a winglabel point and selection area

LEFTMARGIN = 'leftmargin'
RIGHTMARGIN = 'rightmargin'
ASCENDER = 'ascender'
DESCENDER = 'descender'
CAPHEIGHT = 'capheight'

# FloqMeme types
FLOQMEME_UNDEFINED = 0
FLOQMEME_STEM = 100 # X direction
FLOQMEME_ROUNDSTEM = 101
FLOQMEME_WHITE = 110
FLOQMEME_MARGIN = 120
FLOQMEME_BAR = 200 # Y direction
FLOQMEME_ROUNDBAR = 201
FLOQMEME_ASCENDER = 210
FLOQMEME_DESCENDER = 220
FLOQMEME_XHEIGHT = 230
FLOQMEME_CAPHEIGHT = 240
FLOQMEME_OVERSHOOT = 250
FLOQMEME_DIAGONAL = 300
FLOQMEME_SERIF = 400

FLOQMEMES = set((
    FLOQMEME_UNDEFINED, FLOQMEME_STEM, FLOQMEME_ROUNDSTEM, FLOQMEME_WHITE, FLOQMEME_MARGIN,
    FLOQMEME_BAR, FLOQMEME_ROUNDBAR, FLOQMEME_ASCENDER, FLOQMEME_DESCENDER, FLOQMEME_XHEIGHT,
    FLOQMEME_CAPHEIGHT, FLOQMEME_OVERSHOOT, FLOQMEME_DIAGONAL, FLOQMEME_SERIF))

FLOQMEME_LABELS = { # Names of floq type in UI
    FLOQMEME_UNDEFINED: '???',
    FLOQMEME_STEM: 'Stem', # X direction
    FLOQMEME_ROUNDSTEM: 'RStem',
    FLOQMEME_WHITE: 'White',
    FLOQMEME_MARGIN: 'Margin',
    FLOQMEME_BAR: 'Bar', # Y direction
    FLOQMEME_ROUNDBAR: 'RBar',
    FLOQMEME_ASCENDER: 'Ascender',
    FLOQMEME_DESCENDER: 'Descender',
    FLOQMEME_XHEIGHT: 'xHeight',
    FLOQMEME_CAPHEIGHT: 'capHeight',
    FLOQMEME_OVERSHOOT: 'Overshoot',
    FLOQMEME_DIAGONAL: 'Diagonal',
    FLOQMEME_SERIF: 'Serif',
}
# Type of line terminals implemented by tnbits.drawing.lines.
TERMINAL_SQUARE = 'smallSquare'
TERMINAL_LARGECIRCLE = 'largeCircle'


# FLOQ Field names, inherits from Winglet attributes
FLOQMEME_NAME = 'name'
FLOQMEME_ID = 'id'  # Cvt id is editable, different from winglet unique id
FLOQMEME_AXIS = 'axis'
FLOQMEME_TYPE = 'type'
FLOQMEME_VALUE = 'value'
FLOQMEME_PARENT = 'parent'
FLOQMEME_POINT = 'point'
FLOQMEME_GLYPH = 'glyph'
FLOQMEME_DEFAULTGLYPH = 'defaultglyph'
FLOQMEME_DEFAULTHOOK = 'defaulthook' # Function name where to initialize the default FLOQ winglabel
FLOQMEME_INFO = 'info'

# Link field names in Winglets
WINGFIELD_ID = 'id' # Id (label) of the link
WINGFIELD_TYPE = 'type' # Render type of the wing
WINGFIELD_CODE = 'code' # Storage of the source code line of a Winglet
WINGFIELD_LINENUMBER = 'linenumber' # Line number of the winglet.
WINGFIELD_PLUS = 'plus' # Dummy field in list as insert new line command
WINGFIELD_DRAG = 'drag' # Dummy field in list as drag area.
WINGFIELD_PARENT = 'parent' # Name (label) of source link object (point, link or cvt)
WINGFIELD_WINGORDER = 'wingorder' # WingCommand order of activated wings
WINGFIELD_WINGID = 'wingid' # Storage of the wing.id in WingCommand lists
WINGFIELD_EXPANDED = 'expanded'  # Storage flag if the wingcommand entry is expanded in the UI
WINGFIELD_CHILDREN = 'children'  # Use of UI items [x] on WingCommand list
WINGFIELD_ACTIVATE = 'activate'  # Item flag if the wing is active in a WingCommand
WINGFIELD_POINT = 'point' # Name (label) Label of reference point
WINGFIELD_UNIQUEID = 'uniqueID'  # Calculated Unique ID, e.g. parent.uniqueID + point.uniqueID
WINGFIELD_WINGLABEL = 'winglabel' # Id of the winglabel this wing refers to
WINGFIELD_AXIS = 'axis' # x or y
WINGFIELD_FLOQMEME = 'floqmeme'  # Name (label) of target link object (point, link or cvt)
WINGFIELD_FLOQ = 'floq' # Dict of FloqMeme (previously CvtDict with CvtValue) instances
WINGFIELD_WINGS = 'wings' # List of Wings in the Wingset instance
WINGFIELD_WINGSETS = 'wingsets' # Dictionary of references to used wingsets
WINGFIELD_NAME = 'name' # Name of the WingDict instance
WINGFIELD_COLOR = 'color'
WINGFIELD_PV = 'pv'  # Projection vector
WINGFIELD_FV = 'fv'  # Freedom vector
WINGFIELD_MNEMONIC = 'mnemonic' # Instruction name
WINGFIELD_METHOD = 'method' # Method produces a set of mnemonics to call, could be Python method
WINGFIELD_PARAMS = 'params' # Instruction params list
WINGFIELD_COMMENT = 'comment'
WINGFIELD_ERROR = 'error'
WINGFIELD_SELECTED = 'selected' # Indicator of the selected item
WINGFIELD_SIZE = 'size'
WINGFIELD_SRC = 'src' # Storage of wing sources
WINGFIELD_DIRTY = 'dirty' # If the source changed, but the wing is not recompiled.

WINGLETFIELDS = (WINGFIELD_AXIS, WINGFIELD_MNEMONIC, WINGFIELD_PARAMS)

# Link rounding
WINGROUNDING_GRID = 'grid'
WINGROUNDING_HALFGRID = 'halfgrid'
WINGROUNDING_ALIGN = 'align'
WINGROUNDING_ROUND = 'round'
WINGROUNDING_ROUNDUP = 'roundup'
WINGROUNDINGS = (WINGROUNDING_GRID, WINGROUNDING_HALFGRID, WINGROUNDING_ALIGN,
                                    WINGROUNDING_ROUND, WINGROUNDING_ROUNDUP)
# Link color
WINGCOLOR_BLACK = 'black'
WINGCOLOR_WHITE = 'white'
WINGCOLOR_GRAY = 'gray'
WINGCOLORS = (WINGCOLOR_BLACK, WINGCOLOR_WHITE, WINGCOLOR_GRAY)

# Wing rendering types
WINGTYPE_ANTIALIASING = 'aa'
WINGTYPE_BLACKWHITE = 'bw'
WINGTYPE_CLEARTYPE = 'ct'
WINGTYPES = (WINGTYPE_ANTIALIASING, WINGTYPE_BLACKWHITE, WINGTYPE_CLEARTYPE)

WINGAXIS_X = 'x'
WINGAXIS_Y = 'y'
WINGAXIS_D = 'd'
WINGAXIS = (WINGAXIS_X, WINGAXIS_Y, WINGAXIS_D)

# Abstract naming for PttBulder
# Point field names in UI list
POINTFIELD_ID = 'id'
POINTFIELD_X = WINGAXIS_X
POINTFIELD_Y = WINGAXIS_Y
POINTFIELD_CURVE = 'curve'
POINTFIELD_SMOOTH = 'smooth'
POINTFIELD_START = 'start'
POINTFIELD_UNIQUEID = 'uniqueID'
POINTFIELD_BASEGLYPH = 'baseglyph'
POINTFIELD_SCRIPT = 'script'
POINTFIELD_TOUCHX = 'tx'
POINTFIELD_TOUCHY = 'ty'
POINTFIELD_COMMENT = 'comment'
POINTFIELD_XPARENT = 'xparent'
POINTFIELD_YPARENT = 'yparent'

# ---------------------------------------------------------------------------------------------------------
#    M V C  E V E N T

EVENT_SELECTGLYPH = 'selectGlyph'
EVENT_UNSELECTGLYPH = 'unselectGlyph'
EVENT_SELECTLISTMODE = 'selectListMode' # Select list mode
EVENT_SELECTTEXTMODE = 'selectTextMode' # Select text mode
EVENT_CHANGEGLYPH = 'changeGlyph'

#    Maxp keys
MAXTWILIGHTPOINTS = 'maxTwilightPoints'
NUMGLYHPS = 'numGlyphs'
MAXSTACKELEMENTS = 'maxStackElements'
MAXCOMPONENTDEPTH = 'maxComponentDepth'
MAXSIZEOFINSTRUCTIONS = 'maxSizeOfInstructions'
MAXZONES = 'maxZones'
TABLETAG = 'tableTag'
MAXCOMPOSITEPOINTS = 'maxCompositePoints'
MAXCOMPONENTELEMENTS = 'maxComponentElements'
MAXSTORAGE = 'maxStorage'
MAXCONTOURS = 'maxContours'
MAXFUNCTIONSDEFS = 'maxFunctionDefs'
MAXCOMPOSITECONTOURS = 'maxCompositeContours'
MAXINSTRUCTIONDEFS = 'maxInstructionDefs'
TABLEVERSION = 'tableVersion'
MAXPOINTS = 'maxPoints'

# ---------------------------------------------------------------------------------------------------------
#   M A T C H I N G  A N A L Y Z E R - C V T  N A M E S

MATCHINGHEIGHTS = (
    ('capHeights', 'capHeight'),
    ('capHeightsOS', 'capHeightOS'),
    ('xHeights', 'xheight'),
    ('xHeightsOS', 'xHeightOS'),
    ('baselinesOS', 'baselineOS'), # No plain baseline, 0 is too generic
    ('ascenders', 'ascender'),
    ('ascendersOS', 'ascenderOS'),
    ('descenders', 'descender'),
    ('descendersOS', 'descenderOS'),
)

# ---------------------------------------------------------------------------------------------------------
#    H I N T I N G

# Possible values of round state
ROUND_HALFGRID = 'halfgrid'
ROUND_GRID = 'grid'
ROUND_DOUBLEGRID = 'doublegrid'
ROUND_DOWNTOGRID = 'downtogrid'
ROUND_UPTOGRID = 'uptogrid'
ROUND_OFF = 'off'
ROUND_NONE = 'none' # None standard, used to call the round method just for compensation
ROUND_SUPER = 'super'
ROUND_SUPER45 = 'super45'

# ---------------------------------------------------------------------------------------------------------
#    P O P / P U S H  T Y P E S

PARAMTYPE_BYTE = 'Byte'
PARAMTYPE_WORD = 'Word'
PARAMTYPE_LONG = 'Long'
PARAMTYPE_ULONG = 'Ulong'
PARAMTYPE_INTEGER = 'Integer'
PARAMTYPE_POINT = 'Point' # Long
PARAMTYPE_NPOINT = 'PointList' # List of one or more points
PARAMTYPE_FIXED = 'Fixed'
PARAMTYPE_INT16 = 'Int16'
PARAMTYPE_INT32 = 'Int32'
PARAMTYPE_USHORT32 = 'Ushort32'
PARAMTYPE_FLAG32 = 'Flag32' # Flags padded to 32 bits
PARAMTYPE_V_ = 'Value' # @@@ Check on type
PARAMTYPE_CVT = 'CvtName'

# ---------------------------------------------------------------------------------------------------------
#    L A B E L
LABEL_AXIS = 'XY'
LABEL_WING = 'Wing'
"""
LABEL_SAVE = 'Save'
LABEL_NEW = 'New'

LABEL_ID = 'Id'
LABEL_X = 'X'
LABEL_Y = 'Y'
LABEL_QCURVE = 'Q'
LABEL_VALUE = '123'
LABEL_GLYPH = 'Glyph'
LABEL_SMTH = '-o-'
LABEL_START = 'Start'
#LABEL_STARTMARKER = u'★'
#LABEL_TCHX = u'☝X'
#LABEL_TCHY = u'☝Y'
"""
LABEL_AXISX = u'→'
LABEL_AXISY = u'↑'
LABEL_AXISD = u'↖'
"""
LABEL_TYPE = u'Type'
LABEL_FRX = u'←X→'
LABEL_FRY = u'←Y→'
LABEL_LABEL = 'Label'
LABEL_COMMENT = 'Comment'
LABEL_ROUNDING = 'Rounding'
#LABEL_XPARENT = u'♒X'
#LABEL_YPARENT = u'♒Y'
LABEL_PARENT = u'P→'
LABEL_POINT = u'→P'
LABEL_NAME = 'Name'
LABEL_CODE = 'Code'
LABEL_LINENUMBER = ''
LABEL_PLUS = '+'
LABEL_VALUES = 'Values' # Label in the menu
"""
LABEL_UNTITLED = 'Untitled'
"""
LABEL_COMMENT_T = '# %s'
LABEL_SIZE_N = '#'
"""
LABEL_ERRORSEPARATOR = u' • '

LABEL_XSPRINGS = u'♒'
LABEL_AUTOHINT = 'Autohint'
LABEL_VTT = 'VTT'
#LABEL_YSPRINGS = u'Y' #u'⧙⧙' # ⌇'
#LABEL_DSPRINGS = u'D'

# ---------------------------------------------------------------------------------------------------------
#    F B H I N T

# Index for machine compensations in 1/64th of pixel
COMPENSATION_GRAY = 0
COMPENSATION_1 = 1 # Used??
COMPENSATION_BLACK = 2
COMPENSATION_WHITE = 3
COMPENSATIONS_DEFAULT = {COMPENSATION_GRAY: 0, COMPENSATION_1: 0, COMPENSATION_BLACK: 0, COMPENSATION_WHITE: 0}

# Contants attribute values
#POINTTYPE_OFFCURVE = None # Values of point types as they come from RoboFont
#POINTTYPE_QUADRATIC = u'qcurve'
#POINTTYPE_BEZIER = u'curve'
#POINTTYPE_LINE = u'line'
#POINTTYPE_SPACE = u'space'
#POINTTYPE_CURVES = (POINTTYPE_QUADRATIC, POINTTYPE_BEZIER)
#POINTTYPES = ( POINTTYPE_OFFCURVE, POINTTYPE_QUADRATIC,
#                                    POINTTYPE_BEZIER, POINTTYPE_LINE,
#                                    POINTTYPE_SPACE)

POINTMARKER_ONCURVE = u'•'
POINTMARKER_OFFCURVE = u'o'
POINTMARKER_LINE = u'^'
POINTMARKER_SPACE = u'-'

# Alternative names for point in hints point reference, used as "index"
# The parser also checks on the name without @. This is corrected then in reformat.
POINTNAME_ORIGIN = '@origin'     # Origin point (left side bearing)
POINTNAME_WIDTH = '@width' # Width point (right side bearing)
POINTNAME_TOP = '@top' # Y maximum extreme, with lowest X in case of multiple equal values
POINTNAME_BOTTOM = '@bottom' # Y minimum extreme, with lowest X in case of multiple equal values
POINTNAME_LEFT = '@left' # X minimum extreme, with lowest Y in case of multiple equal values
POINTNAME_RIGHT = '@right' # X maximum extreme, with lowest Y in case of multiple equal values

# Start point marker
POINTTYPE_START = True
POINTTYPE_NOTSTART = False

# Zones
ZONE0 = 0
ZONE1 = 1

# Index of param value/flags of MIRP and MDRP
MxRP_i_RP2P = 0
MxRP_i_KEEPDISTANCE = 1
MxRP_i_ROUNDDISTANCE = 2
MxRP_i_COLOR = 3

# Index of param value/flags in IUP
IUP_i_direction = 0

# Possible values of round state
ROUND_HALFGRID = 'halfgrid'
ROUND_GRID = 'grid'
ROUND_DOUBLEGRID = 'doublegrid'
ROUND_DOWNTOGRID = 'downtogrid'
ROUND_UPTOGRID = 'uptogrid'
ROUND_OFF = 'off'
ROUND_NONE = 'none'  # None standard, used to call the round method just for compensation
ROUND_SUPER = 'super'
ROUND_SUPER45 = 'super45'

# Chars in a mnemonic name that are worth searching for
MNEMONICNAMECHARS = 'abcdefghijklmnopqrstuvwxyz1234567890<>'
PARAMSOURCECHARS = '1234567890-. '

# ---------------------------------------------------------------------------------------------------------
#    C V T  D E F I N E S  F R O M  V T T

HUNITS = 64.0 # Multiplication factor for fixed vetcor values

_OS = '_os'    # Indicator that this is a FloqMeme with overshoot

X = WINGAXIS_X # FloqMeme axis direction identifier
Y = WINGAXIS_Y
D = WINGAXIS_D # Diagonal
XY = 'xy' # FloqMeme item label identifier
AXIS_DEFAULT = Y
TITLE_AXISX = '(%s)' % X # Title pattern of a wing axis
TITLE_AXISY = '(%s)' % Y
TITLE_AXISD = '(%s)' % D
AXIS2LABEL = { X: LABEL_AXISX, Y: LABEL_AXISY, D: LABEL_AXISD }

# Note that the Floq identifiers are compatible with what otherwise
# the default names in the CVT table are defined by.
FLOQ_FLATCAPITALS = 'H I B D E F J K L M N P R T U V W X Y Z'
FLOQ_LCHEIGHTS = 'b d h k l'
FLOQ_LCHEIGHTS_OS = 'f'
FLOQ_CAPITALS_TOP_OS = 'C G O Q'
FLOQ_CAPITALS_BOTTOM_OS = 'C G O Q'

FLOQ_ascHeight = 'ascHeight'
FLOQ_ascHeight_OS = FLOQ_ascHeight + _OS
FLOQ_capHeight = 'capHeight'
FLOQ_capHeight_OS = FLOQ_capHeight + _OS
FLOQ_figHeight = 'figHeight'
FLOQ_figHeight_OS = FLOQ_figHeight + _OS
FLOQ_xHeight = 'xHeight'
FLOQ_xHeight_OS = FLOQ_xHeight + _OS
FLOQ_capBaseline = 'capBaseline'
FLOQ_capBaseline_OS = FLOQ_capBaseline + _OS
FLOQ_baseline = 'baseline' # Lower case baseline
FLOQ_baseline_OS = FLOQ_baseline + _OS # Lower case overshoot baseline
FLOQ_figBaseHeight = 'figBaseHeight'
FLOQ_figBaseHeight_OS = FLOQ_figBaseHeight + _OS
FLOQ_desc = 'desc'
FLOQ_desc_OS = FLOQ_desc + _OS
FLOQ_parenTop = 'parenTop'
FLOQ_parenTop_OS = FLOQ_parenTop + _OS
FLOQ_parenBottom = 'parenBottom'
FLOQ_parenBottom_OS = FLOQ_parenBottom + _OS
FLOQ_aoBottom = 'aoBottom'
FLOQ_aoBottom_OS = FLOQ_aoBottom + _OS
FLOQ_aoTop = 'aoTop'
FLOQ_aoTop_OS = FLOQ_aoTop + _OS
FLOQ_supBottom = 'supBottom'
FLOQ_supBottom_OS = FLOQ_supBottom + _OS
FLOQ_supTop = 'supTop'
FLOQ_supTop_OS = FLOQ_supTop + _OS
RESERVED_BY_VTT_T = 'RESERVED_BY_VTT%03d'
CUSTOM_FLOQ_T = 'CUSTOM FLOQ%03d' # Previously custom CVT value
FLOQ_ascSerifHeight = 'ascSerifHeight'
FLOQ_capSerifHeight = 'capSerifHeight'
FLOQ_figSerifHeight = 'figSerifHeight'
FLOQ_serifHeight = 'xSerifHeight' # Lowercase serif height
FLOQ_capBaseSerifHeight = 'capBaseSerifHeight'
FLOQ_baseSerifHeight = 'baseSerifHeight' # Lowercase base serif height
FLOQ_figBaseSerifHeight = 'figBaseSerifHeight'
FLOQ_descSerifHeight = 'descSerifHeight'
FLOQ_italicRun = 'italicRun'
FLOQ_stem = 'stem'
FLOQ_stemAlt = 'stemAlt'
FLOQ_stemXAbove = 'stemXAbove'
FLOQ_stemYAbove = 'stemYAbove'
FLOQ_thinnestStem = 'thinnestStem'
FLOQ_stemRound = 'stemRound'
FLOQ_stemRoundAlt = 'stemRoundAlt'
FLOQ_thinStem = 'thinStem'
FLOQ_thinStemAlt = 'thinStemAlt'
FLOQ_thinStemRound = 'thinStemRound'
FLOQ_thinStemRoundAlt = 'thinStemRoundAlt'
FLOQ_thinStemBarDiagonal = 'thinStemBarDiagonal'
FLOQ_thinStemBarDiagonalAlt = 'thinStemBarDiagonalAlt'
FLOQ_serifShort = 'serifShort'
FLOQ_serifLong = 'serifLong'
FLOQ_serifHeight = 'serifHeight'
FLOQ_capStem = 'capStem'
FLOQ_capStemAlt = 'capStemAlt'
FLOQ_capStemRound = 'capStemRound'
FLOQ_capStemRoundAlt = 'capStemRoundAlt'
FLOQ_capThinStem = 'capThinStem'
FLOQ_capThinStemAlt = 'capThinStemAlt'
FLOQ_capThinStemRound = 'capThinStemRound'
FLOQ_capThinStemRoundAlt = 'capThinStemRoundAlt'
FLOQ_capDiagonal = 'capDiagonal'
FLOQ_capDiagonalAlt = 'capDiagonalAlt'
FLOQ_capSerifShort = 'capSerifShort'
FLOQ_capSerifLong = 'capSerifLong'
FLOQ_capSerifHeight = 'capSerifHeight'

FLOQ_ijDotDist = 'ijDotDist'
FLOQ_ijDotStem = 'ijDotStem'
FLOQ_ijDotWhiteSpace = 'ijDotWhiteSpace'

FLOQ_capLsb = 'capLsb'
FLOQ_capRsb = 'capRsb'
FLOQ_capLsbRound = 'capLsbRound'
FLOQ_capRsbRound = 'capRsbRound'
FLOQ_capLsbDiag = 'capLsbDiag'
FLOQ_capRsbDiag = 'capRsbDiag'
FLOQ_capLsbFigRound = 'capLsbFigRound'
FLOQ_capRsbFigRound = 'capRsbFigRound'

FLOQ_lsb = 'lsb'
FLOQ_rsb = 'rsb'
FLOQ_lsbRound = 'lsbRound'
FLOQ_rsbRound = 'rsbRound'
FLOQ_lsbDiag = 'lsbDiag'
FLOQ_rsbDiag = 'rsbDiag'

FLOQ_figureStem = 'figureStem'
FLOQ_figureStemAlt = 'figureStemAlt'
FLOQ_figureStemRound = 'figureStemRound'
FLOQ_figureStemRoundAlt = 'figureStemRoundAlt'
FLOQ_figureBar = 'figureBar'
FLOQ_figureBarAlt = 'figureBarAlt'
FLOQ_figureBarRound = 'figureBarRound'
FLOQ_figureBarRoundAlt = 'figureBarRoundAlt'
FLOQ_figureDiagonal = 'figureDiagonal'
FLOQ_figureDiagonalAlt = 'figureDiagonalAlt'
FLOQ_figureSerifShort = 'figureSerifShort'
FLOQ_figureSerifLong = 'figureSerifLong'
FLOQ_figureSerifHeight = 'figureSerifHeight'

FLOQ_otherStem = 'otherStem'
FLOQ_otherStemAlt = 'otherStemAlt'
FLOQ_otherStemRound = 'otherStemRound'
FLOQ_otherStemRoundAlt = 'otherStemRoundAlt'
FLOQ_otherBar = 'otherBar'
FLOQ_otherBarAlt = 'otherBarAlt'
FLOQ_otherBarRound = 'otherBarRound'
FLOQ_otherBarRoundAlt = 'otherBarRoundAlt'
FLOQ_otherDiagonal = 'otherDiagonal'
FLOQ_otherDiagonalAlt = 'otherDiagonalAlt'
FLOQ_otherSerifShort = 'otherSerifShort'
FLOQ_otherSerifLong = 'otherSerifLong'
FLOQ_otherSerifHeight = 'otherSerifHeight'

FLOQ_accentBaseline = 'accentBaseline'
FLOQ_accentStem = 'accentStem'
FLOQ_accentStemRound = 'accentStemRound'
FLOQ_accentBar = 'accentBar'
FLOQ_accentBarRound = 'accentBarRound'
FLOQ_accentGraveDistance = 'accentGraveDistance'
FLOQ_accentDieresisRound = 'accentDieresisRound'
FLOQ_fStem = 'fStem'
FLOQ_fBar = 'fBar'
FLOQ_fCounter = 'fCounter'

FLOQ_semicolonDist = 'semicolonDist'
FLOQ_parenDist = 'parenDist'
FLOQ_bracketDist = 'bracketDist'
FLOQ_braceDist = 'braceDist'
FLOQ_semicolonVDist = 'semicolonVDist'
FLOQ_parenVDist = 'parenVDist'
FLOQ_bracketVDist = 'bracketVDist'
FLOQ_braceVDist = 'braceVDist'
FLOQ_endashDist = 'endashDist'
FLOQ_daggerStem = 'daggerStem'
FLOQ_daggerBar = 'daggerBar'
FLOQ_daggerThinBar = 'daggerThinBar'

# OTHER_superiorS
FLOQ_supStem = 'supStem'
FLOQ_supStemRound = 'supStemRound'
FLOQ_supBar = 'supBar'
FLOQ_supBarRound = 'subBarRound'
FLOQ_plusStem = 'plusStem'
FLOQ_plusBar = 'plusBar'
FLOQ_plusBaseline = 'plusBaseline'
FLOQ_plusThinBar = 'plusThinBar'
FLOQ_minusBar = 'minusBar'
FLOQ_minusThinBar = 'minusThinBar'
FLOQ_percentXCounter = 'percentXCounter'
FLOQ_percentYCounter = 'percentYCounter'

FLOQ_capVRun = 'capVRun'
FLOQ_capVStem = 'capVStem'
FLOQ_capARun = 'capARun'
FLOQ_capMRun = 'capMRun'
FLOQ_capWRun1 = 'capWRun1'
FLOQ_capWRun2 = 'capWRun2'
FLOQ_capXRun = 'capXRun'
FLOQ_capYRun = 'capYRun'
FLOQ_circRun = 'circRun'
FLOQ_vRun = 'vRun'
FLOQ_wRun1 = 'wRun1'
FLOQ_xRun = 'xRun'
FLOQ_wRun2 = 'wRun2'
FLOQ_capHItalicRun = 'capHItalicRun'
FLOQ_nItalicRun = 'nItalicRun'
FLOQ_hItalicRun = 'hItalicRun'

FLOQ_serif = 'serif'
FLOQ_capSerif = 'capSerif'

FLOQ_unknown = 'unknown'

WINGLABEL_ARROW = '>'
WINGLABEL_PATTERN = '%s'+WINGLABEL_ARROW+'%s'    # Scripting macro for reference to WINGLABEL

#    User defines Floq identifers (compatible to CVT) start at 159
FLOQ_MINUSERID = 159
FLOQ_UNKNOWN = 250
FLOQ_CUSTOMINDEXSTART = 300 # Start for the first index of custom CVT entries

# Generic CVT types are use to search for matching CVT values, depending on the context of the glyph
# and the position and direction of the points involved. Matching CVT names need to with one
# of these patterns or with the pattern + '_os'
#FLOQ_stem = 'stem'         # stems, bars, etc. (black)
#FLOQ_height = 'height'         # xHeight, capHeight, ascender, descender and other vertical distances (gray)
#FLOQ_side = 'side'         # left and right sidebearings (white)
#FLOQ_counter = 'counter'         # counters (white)
#FLOQ_aperture = 'aperture'     # white space the needs to be kept open (white)
#FLOQ_run = 'run'             # horizontal run of a diagonal (gray)
#FLOQ_length = 'width'         # length between two points (connected?), e.g. serif length (black)
#FLOQ_nothing = 'nothing'
#
# Types of generic CVT type with their resulting value to be checked on.
#FLOQ_TYPES = (FLOQ_stem, FLOQ_height, FLOQ_side, FLOQ_counter, FLOQ_aperture, FLOQ_run, FLOQ_length, FLOQ_nothing)

DEFAULT_FLOQ_SOURCE = {
    # Name                        Id    Axis Default            FLOQ type        DefaultGet        Comment
    FLOQ_ascHeight:                (0,   Y,    'h',              'height',        'maxY',        """Cvt #0 is the “ascHeight” and is obtain by measuring the height of the lowercase b, d, h, k, and l."""),
    FLOQ_ascHeight_OS:             (1,   Y,    'f',              'height',        'maxY',        """Cvt #1 is the overshoot amount for the ascenders. This maybe the lowercase 'f' height if the height is actually taller than the other ascenders."""),
    FLOQ_capHeight:                (2,   Y,    'H',              'height',        'maxY',        """Cvt #2 “capHeight” is measured from the baseline to the visual top of the uppercase 'flat' glyphs. Examples are: B, D, E, F, H, I, J, K, L, M, N, P, R, T, U, V, W, X, Y, and Z. The value should be the point where hinting will originate from. Similar to the baseline. This may not be the value at the top most of the glyph."""),
    FLOQ_capHeight_OS:             (3,   Y,    'O',              'height',        'maxY',        """Cvt #3 is the top overshoot of the uppercase round glyphs. This value is calculated by using the most common or average value from the uppercase round glyphs (ex: C, G, O, and Q.) Measured from the baseline to the top of the glyph. Subtracting the value by Cvt #2."""),
    FLOQ_figHeight:                (4,   Y,    'five',            'height',        'maxY',        """Cvt #4 “figHeight” is the value from the baseline to the top of the flat figure glyphs. (ex: 5,7)."""),
    FLOQ_figHeight_OS:             (5,   Y,    'two',            'height',        'maxY',        """Cvt #5 is the figure top overshoot value."""),
    FLOQ_xHeight:                  (6,   Y,    'x',            'height',        'maxY',        """Cvt #6 “xHeight” is the lowercase flat top value. Similar to the capHeight, this is not necessarily the top of the lowercase x, but the visual top of the lowercase flat glyphs."""),
    FLOQ_xHeight_OS:               (7,   Y,    'o',            'height',        'maxY',        """Cvt #7 is the lowercase top overshoot value."""),
    FLOQ_capBaseline:              (8,   Y,    'H',            'height',        'minY',        """Cvt #8 “capBaseline” this value is usually zero."""),
    FLOQ_capBaseline_OS:           (9,   Y,    'O',            'height',        'minY',        """Cvt #9 this is the bottom uppercase overshoot. This value is usually negative and the same absolute value as Cvt #3."""),
    FLOQ_baseline:                 (10,  Y,    'n',            'height',        'minY',        """Cvt #10 “baseline” this value is usually zero."""),
    FLOQ_baseline_OS:              (11,  Y,    'o',            'height',        'minY',        """Cvt #11 is the bottom lowercase overshoot. This value is usually negative and the same absolute value as Cvt #7."""),
    FLOQ_figBaseHeight:            (12,  Y,    'one',            'height',        'minY',        """Cvt #12 “figBaseHeight” this value is usually zero."""),
    FLOQ_figBaseHeight_OS:         (13,  Y,    'six',            'height',        'minY',        """Cvt #13 is the bottom figure overshoot. This value is usually negative and the same absolute value as Cvt #5."""),
    FLOQ_desc:                     (14,  Y,    'p',            'height',        'minY',        """Cvt #14 “desc” this value is the flat descender value often measured from the lowercase p and q. The lowercase g and j may or may not be the same."""),
    FLOQ_desc_OS:                  (15,  Y,    'g',            'height',        'minY',        """Cvt #15 is the descender overshoot value. Used if the round descenders (g or j) are lower than the flat descenders."""),
    FLOQ_parenTop:                 (16,  Y,    'parenleft',    'height',        'maxY',        """Cvt #16 “parenTop” is the top parenthesis, brackets, and braces. These glyphs are generally aligned to the lowercase ascender value. This value is often the same as Cvt #0."""),
    FLOQ_parenTop_OS:              (17,  Y,    'parenleft',    'height',        'maxY',        """Cvt #17 could be used for a design where the one of the pairs of brackets or braces overshoots the parenthesis height. Commonly this value is left as zero."""),
    FLOQ_parenBottom:              (18,  Y,    'parenleft',    'height',        'minY',        """Cvt #18 “parenBottom” this is the bottom of the parenthesis. The value is negative and often the same as Cvt #14."""),
    FLOQ_parenBottom_OS:           (19,  Y,    'parenleft',    'height',        'minY',        """Cvt #19 is the overshoot for the parenthesis. If an overshoot is used this value is negative."""),
    FLOQ_aoBottom:                 (20,  Y,    'onesuperior',    'height',        'minY',        """Cvt #20 “aoBottom” this value is for the 'a', 'o' ordinals and is often the same as Cvt #24."""),
    FLOQ_aoBottom_OS:              (21,  Y,    'threesuperior','height',        'minY',        """Cvt #21 this is the ordinal's overshoot amount and usually the same as Cvt# 25."""),
    FLOQ_aoTop:                    (22,  Y,    'onesuperior',    'height',        'maxY',        """Cvt #22 “aoTop” this value is for the 'a', 'o' ordinals and is often the same as Cvt #26."""),
    FLOQ_aoTop_OS:                 (23,  Y,    'threesuperior','height',        'maxY',        """Cvt #23 this is the ordinal's overshoot amount and usually the same as Cvt# 27."""),
    FLOQ_supBottom:                (24,  Y,    'onesuperior',    'height',        'minY',        """Cvt #24 “supBottom” this is the bottom of the flat superiors (superior one or two.)."""),
    FLOQ_supBottom_OS:             (25,  Y,    'threesuperior','height',        'minY',        """Cvt #25 is the round overshoot value of the superior three."""),
    FLOQ_supTop:                   (26,  Y,    'fivesuperior',    'height',        'maxY',        """Cvt #26 “supTop” this is the flat top of the superior numerals. In a full set of superiors the value is the top of the superior 5 and 7.)."""),
    FLOQ_supTop_OS:                (27,  Y,    'threesuperior','height',        'maxY',        """Cvt #27 (Y) superior top overshoot value."""),
    FLOQ_ascSerifHeight:           (28,  Y,    'l',            'height',        'notdef',    """Cvt #28 (Y) Ascender serif height."""),
    FLOQ_capSerifHeight:           (29,  Y,    'H',            'height',        'notdef',    """Cvt #29 (Y) Capital serif height."""),
    FLOQ_figSerifHeight:           (30,  Y,    'one',            'height',        'notdef',    """Cvt #30 (Y) Figure serif height."""),
    FLOQ_serifHeight:              (31,  Y,    'n',            'height',        'notdef',    """Cvt #31 (Y) Lowercase serif height."""),
    FLOQ_capBaseSerifHeight:       (32,  Y,    'H',            'height',        'notdef',    """Cvt #32 (Y) Capital base serif height."""),
    FLOQ_baseSerifHeight:          (33,  Y,    'n',            'height',        'notdef',    """Cvt #33 (Y) Lowercase base serif height."""),
    FLOQ_figBaseSerifHeight:       (34,  Y,    'one',            'height',        'notdef',    """Cvt #34 (Y) Figure base serif height."""),
    FLOQ_descSerifHeight:          (35,  Y,    'p',            'height',        'notdef',    """Cvt #35 (Y) Descender serif height."""),
    FLOQ_italicRun:                (36,  X,    'I',            'run',            'notdef',    """Cvt #36 (X) italicRun is used by a high level function for italic strokes. In upright fonts this value is '0'. Later when we measure the italic fonts I will explain how this is measured. In italic fonts this value is the horizontal distance from the left extreme of an uppercase stroke to the uppercase flat height. In mathematics, this distance is the 'run', hence the comment '# italicRun.' The uppercase flat height would be mathematically called the 'rise'."""),

      # Compiler Internals Temps &amp; SideBearing Control:  */
    # FLOQ# 40..64 USED BY THE VTT COMPILER DO NOT USE or REMOVE
    #
    #  40:    0
    #  41:    0
    #  42:    0
    #  43:    0 lsb TEMP
    #  44:    0 rsb TEMP
    #  45:    0
    #  46:    0
    #  47:    0
    #  48:    0
    #  49:    0
    #  50:    0
    #  51:    0 lsb DELTA
    #  52:    0 rsb DELTA
    #  53:    0
    #  54:    0
    #
      #    c_cvtNorm[] dump (in nc_FillCvtEpilogue) */
      #
    #   55:    0
    #   56:    0
    #   57:    0
    #   58:    0
    #   59:    0
    #   60:    0
    #   61:    0
    #   62:    0
    #   63:    0
    #   64:    0

    FLOQ_thinnestStem:            (65,X,    'i',            'stem',            'stem',        """Thinnest stem (Y) to keep all stems at one pixel."""),
    FLOQ_stemXAbove:                (66,X,    'n',            'stem',            'stem',        """The most major (X) stem usually the lowercase (X) straight stem value. Controlling (X) direction above one pixel size."""),
    FLOQ_stemYAbove:                (67,Y,    'n',            'stem',            'rbar',        """The most major (Y) stem often the same as Cvt 65. Controlling (Y) direction above one pixel size."""),

    # UPPERCASE
    FLOQ_capStem:                (68,X,    'H',            'stem',            'stem',        """Cvt #68 (X) Capital straight stem width."""),
    FLOQ_capStemAlt:                (69,X,    'H',            'stem',            'stem',        """Cvt #69 (X) Capital straight stem width alternate."""),
    FLOQ_capStemRound:            (70,X,    'O',            'stem',            'rstem',    """Cvt #70 (X) Capital round stem width."""),
    FLOQ_capStemRoundAlt:        (71,X,    'O',            'stem',            'rstem',    """Cvt #71 (X) Capital round stem width alternate."""),
    FLOQ_capThinStem:            (72,Y,    'H',            'stem',            'bar',        """Cvt #72 (Y) Capital straight horizontal thin stem ."""),
    FLOQ_capThinStemAlt:            (73,Y,    'H',            'stem',            'bar',        """Cvt #73 (Y) Capital straight horizontal thin stem alternate."""),
    FLOQ_capThinStemRound:        (74,Y,    'O',            'stem',            'rbar',        """Cvt #74 (Y) Capital thin round."""),
    FLOQ_capThinStemRoundAlt:    (75,Y,    'O',            'stem',            'rbar',        """Cvt #75 (Y) Capital thin round alternate."""),
    FLOQ_capDiagonal:            (76,D,    'X',            'run',            'run',        """Cvt #76 (D) Capital diagonal."""),
    FLOQ_capDiagonalAlt:            (77,D,    'X',            'run',            'run',        """Cvt #77 (D) Capital diagonal alternate."""),
    FLOQ_capSerifShort:            (78,X,    'H',            'width',        'notdef',    """Cvt #78 (X) Capital serif short."""),
    FLOQ_capSerifLong:            (79,X,    'H',            'width',        'notdef',    """Cvt #79 (X) Capital serif long."""),
    FLOQ_capSerifHeight:            (80,Y,    'H',            'height',        'notdef',    """Cvt #80 (Y) Capital serif height."""),

    # LOWERCASE
    FLOQ_stem:                     (81,X,    'n',            'stem',            'stem',        """Cvt #81 (X) Lowercase straight."""),
    FLOQ_stemAlt:                 (82,X,    'n',            'stem',            'stem',        """Cvt #82 (X) Lowercase straight alternate."""),
    FLOQ_stemRound:                 (83,X,    'o',            'stem',            'rstem',    """Cvt #83 (X) Lowercase round."""),
    FLOQ_stemRoundAlt:             (84,X,    'o',            'stem',            'rstem',    """Cvt #84 (X) Lowercase round alternate."""),
    FLOQ_thinStem:                 (85,Y,    'z',            'stem',            'bar',        """Cvt #85 (Y) Lowercase thin stem (bar) straight."""),
    FLOQ_thinStemAlt:             (86,Y,    'z',            'stem',            'bar',        """Cvt #86 (Y) Lowercase thin stem (bar) straight alternate."""),
    FLOQ_thinStemRound:             (87,Y,    'o',            'stem',            'rbar',        """Cvt #87 (Y) Lowercase thin stem (bar) round."""),
    FLOQ_thinStemRoundAlt:         (88,Y,    'o',            'stem',            'rbar',        """Cvt #88 (Y) Lowercase thin stem (bar) round alternate."""),
    FLOQ_thinStemBarDiagonal:     (89,D,    'x',            'run',            'run',        """Cvt #89 (D) Lowercase thin stem (bar) diagonal."""),
    FLOQ_thinStemBarDiagonalAlt: (90,D,    'x',            'run',            'run',        """Cvt #90 (D) Lowercase thin stem (bar) diagonal alternate."""),
    FLOQ_serifShort:             (91,X,    'n',            'width',        'notdef',    """Cvt #91 (X) Lowercase serif short."""),
    FLOQ_serifLong:                 (92,X,    'n',            'width',        'notdef',    """Cvt #92 (X) Lowercase serif long."""),
    FLOQ_serifHeight:             (93,Y,    'n',            'height',        'notdef',    """Cvt #93 (Y) Lowercase serif height."""),
    FLOQ_ijDotDist:                (94,X,    'i',            'stem',            'notdef',    """Cvt #94 (X) Lowercase i,j dot distance."""),
    FLOQ_ijDotStem:                 (95,Y,    'i',            'stem',            'notdef',    """Cvt #95 (Y) Lowercase i,j dot distance."""),
    FLOQ_ijDotWhiteSpace:         (96,Y,    'i',            'apperture',    'notdef',    """Cvt #96 (Y) Lowercase i,j dot white space."""),

    #    FIGURE
    FLOQ_figureStem:                (97,X,    'one',            'stem',            'stem',        """Cvt #97 (X) Figure straight."""),
    FLOQ_figureStemAlt:            (98,X,    'one',            'stem',            'stem',        """Cvt #98 (X) Figure straight alternate."""),
    FLOQ_figureStemRound:        (99,X,    'six',            'stem',            'rstem',    """Cvt #99 (X) Figure round."""),
    FLOQ_figureStemRoundAlt:        (199,X,    'six',            'stem',            'rstem',    """Cvt #100 (X) Figure round alternate."""),
    FLOQ_figureBar:                (101,Y,    'seven',        'stem',            'bar',        """Cvt #101 (Y) Figure straight."""),
    FLOQ_figureBarAlt:            (102,Y,    'seven',        'stem',            'bar',        """Cvt #102 (Y) Figure straight alternate."""),
    FLOQ_figureBarRound:            (103,Y,    'six',            'stem',            'rbar',        """Cvt #103 (Y) Figure round."""),
    FLOQ_figureBarRoundAlt:        (104,Y,    'six',            'stem',            'rbar',        """Cvt #104 (Y) Figure round alternate."""),
    FLOQ_figureDiagonal:            (105,D,    'seven',        'run',            'run',        """Cvt #105 (D) Figure diagonal."""),
    FLOQ_figureDiagonalAlt:        (106,D,    'seven',        'run',            'run',        """Cvt #106 (D) Figure diagonal alternate."""),
    FLOQ_figureSerifShort:        (107,X,    'one',            'width',        'notdef',    """Cvt #107 (X) Figure serif short."""),
    FLOQ_figureSerifLong:        (108,X,    'one',            'width',        'notdef',    """Cvt #108 (X) Figure serif long."""),
    FLOQ_figureSerifHeight:        (109,Y,    'one',            'height',        'notdef',    """Cvt #109 (Y) Figure serif height."""),

    # OTHER
    FLOQ_otherStem:                (110,X,    'n',            'stem',            'stem',        """Cvt #110  (X) Other straight."""),
    FLOQ_otherStemAlt:            (111,X,    'n',            'stem',            'stem',        """Cvt #111  (X) Other straight alternate."""),
    FLOQ_otherStemRound:            (112,X,    'o',            'stem',            'rstem',    """Cvt #112  (X) Other round."""),
    FLOQ_otherStemRoundAlt:        (113,X,    'o',            'stem',            'rstem',    """Cvt #113  (X) Other round alternate."""),
    FLOQ_otherBar:                (114,Y,    'n',            'stem',            'bar',        """Cvt #114  (Y) Other straight."""),
    FLOQ_otherBarAlt:            (115,Y,    'n',            'stem',            'bar',        """Cvt #115  (Y) Other straight alternate."""),
    FLOQ_otherBarRound:            (116,Y,    'o',            'stem',            'rbar',        """Cvt #116  (Y) Other round."""),
    FLOQ_otherBarRoundAlt:        (117,Y,    'o',            'stem',            'rbar',        """Cvt #117  (Y) Other round alternate."""),
    FLOQ_otherDiagonal:            (118,D,    'x',            'run',            'run',        """Cvt #118  (D) Other diagonal."""),
    FLOQ_otherDiagonalAlt:        (119,D,    'x',            'run',            'run',        """Cvt #119  (D) Other diagonal alternate."""),
    FLOQ_otherSerifShort:        (120,X,    'n',            'width',        'notdef',    """Cvt #120  (X) Other serif short."""),
    FLOQ_otherSerifLong:            (121,X,    'n',            'width',        'notdef',    """Cvt #121  (X) Other serif long."""),
    FLOQ_otherSerifHeight:        (122,Y,    'n',            'height',        'notdef',    """Cvt #122  (Y) Other serif height."""),

    #    OTHER_PUNCUATION
    FLOQ_semicolonDist:            (123,X,    'semicolon',    'stem',            'rstem',    """Cvt #123 (X) semicolon horizontal dot distance."""),
    FLOQ_parenDist:                (124,X,    'parenleft',    'stem',            'rstem',    """Cvt #124 (X) parens distance."""),
    FLOQ_bracketDist:            (125,X,    'bracketleft',    'stem',            'stem',        """Cvt #125 (X) brackets distance."""),
    FLOQ_braceDist:                (126,X,    'braceleft',    'stem',            'stem',        """Cvt #126 (X) braces distance."""),
    FLOQ_semicolonVDist:            (127,Y,    'semicolon',    'stem',            'stem',        """Cvt #127 (Y) semicolon vertical dot distance."""),
    FLOQ_parenVDist:                (128,Y,    'parenleft',    'stem',            'stem',        """Cvt #128 (Y) parens distance."""),
    FLOQ_bracketVDist:            (129,Y,    'bracketleft',    'stem',            'stem',        """Cvt #129 (Y) brackets distance."""),
    FLOQ_braceVDist:                (130,Y,    'braceleft',    'stem',            'stem',        """Cvt #139 (Y) braces distance."""),
    FLOQ_endashDist:                (131,Y,    'endash',        'stem',            'bar',        """Cvt #131 (Y) en/em dash distance."""),
    FLOQ_daggerStem:                (132,X,    'dagger',        'stem',            'stem',        """Cvt #132 (X) dagger straight stem."""),
    FLOQ_daggerBar:                (133,X,    'dagger',        'stem',            'bar',        """Cvt #133 (X) dagger bar length."""),
    FLOQ_daggerThinBar:            (134,Y,    'dagger',        'stem',            'stem',        """Cvt #134 (Y) dagger thin bar (thickness)."""),

    # OTHER_superiorS
    FLOQ_supStem:                (135,X,    'superiorone',    'stem',            'stem',        """Cvt #135 (X) superior straight stem."""),
    FLOQ_supStemRound:            (136,X,    'superiorzero',    'stem',            'rstem',    """Cvt #136 (X) superior round stem."""),
    FLOQ_supBar:                    (137,Y,    'superiorone',    'stem',            'bar',        """Cvt #137 (Y) superior straight."""),
    FLOQ_supBarRound:            (138,Y,    'superiorzero',    'stem',            'rbar',        """Cvt #138 (Y) superior round."""),
    FLOQ_percentXCounter:        (139,X,    'percent',        'counter',        'notdef',    """Cvt #139 (X) percent counter."""),
    FLOQ_percentYCounter:        (140,Y,    'percent',        'counter',        'notdef',    """Cvt #140 (Y) percent counter."""),

    # OTHER_MATH
    FLOQ_plusStem:                (141,X,    'plus',            'stem',            'stem',        """Cvt #141 (X) plus straight stem."""),
    FLOQ_plusBar:                (142,X,    'plus',            'stem',            'stem',        """Cvt #142 (X) plus bar length."""),
    FLOQ_plusBaseline:            (143,Y,    'plus',            'height',        'minY',        """Cvt #143 (Y) plus baseline."""),
    FLOQ_plusThinBar:            (144,Y,    'plus',            'stem',            'bar',        """Cvt #144 (X) plus thin bar (thickness)."""),
    FLOQ_minusBar:                (145,X,    'minus',        'stem',            'bar',        """Cvt #145 (X) minus bar length."""),
    FLOQ_minusThinBar:            (146,Y,    'minus',        'stem',            'bar',        """Cvt #146 (Y) minus bar straight stem."""),

    # OTHER_DIACRITICS
    FLOQ_accentBaseline:            (147,Y,    'acute',        'height',        'minY',        """Cvt #147 (Y) accent baseline."""),
    FLOQ_accentStem:                (148,X,    'acute',        'stem',            'stem',        """Cvt #148 (X) accent straight."""),
    FLOQ_accentStemRound:        (149,X,    'acute',        'stem',            'rstem',    """Cvt #149 (X) accent round."""),
    FLOQ_accentBar:                (150,Y,    'acute',        'stem',            'bar',        """Cvt #150 (Y) accent straight."""),
    FLOQ_accentBarRound:            (151,Y,    'acute',        'stem',            'rbar',        """Cvt #151 (Y) accent round."""),
    FLOQ_accentGraveDistance:    (152,Y,    'acute',        'stem',            'stem',        """Cvt #152 (Y) acute_grave distance."""),
    FLOQ_accentDieresisRound:    (153,X,    'dieresis',        'stem',            'rstem',    """Cvt #153 (X) dieresis round."""),
    FLOQ_fStem:                    (154,X,    'f',            'stem',            'stem',        """Cvt #154 (X) BOLLƒ distance."""),
    FLOQ_fBar:                    (155,Y,    'f',            'stem',            'stem',        """Cvt #155 (Y) BOLLƒ distance."""),
    FLOQ_fCounter:                (156,Y,    'f',            'counter',        'notdef',    """Cvt #156 (Y) BOLLƒ_counter."""),

    # First Available FLOQ Index =  157 (Compatible to default CVT Table)
    # INSERT less common or glyph specific cvts here

    'floq157':                    (157,X,    'n',            '',                'notdef',    """Cvt #157 other."""),

    FLOQ_capLsb:                    (160,X,    'H',            'side',            'minX',        """Cvt #160 (X) H Left sidebearing."""),
    FLOQ_capRsb:                    (161,X,    'H',            'side',            'rsb',        """Cvt #161 (X) H Right sidebearing."""),
    FLOQ_capLsbRound:            (163,X,    'O',            'side',            'minX',        """Cvt #163 (X) O Left sidebearing."""),
    FLOQ_capRsbRound:            (164,X,    'O',            'side',            'rsb',        """Cvt #164 (X) O Right sidebearing."""),
    FLOQ_capLsbDiag:                (165,X,    'V',            'side',            'minX',        """Cvt #165 (X) V Left sidebearing."""),
    FLOQ_capRsbDiag:                (166,X,    'V',            'side',            'rsb',        """Cvt #166 (X) V Right sidebearing."""),
    FLOQ_capLsbFigRound:         (167,X,    'zero',            'side',            'minX',        """Cvt #167 (X) 0 Right sidebearing."""),
    FLOQ_capRsbFigRound:            (168,X,    'zero',            'side',            'rsb',        """Cvt #168 (X) 0 Left sidebearing."""),

    FLOQ_lsb:                    (170,X,    'n',            'side',            'minX',        """Cvt #170 (X) n Left sidebearing."""),
    FLOQ_rsb:                    (171,X,    'n',            'side',            'rsb',        """Cvt #171 (X) n Right sidebearing."""),
    FLOQ_lsbRound:                (173,X,    'o',            'side',            'minX',        """Cvt #173 (X) o Left sidebearing."""),
    FLOQ_rsbRound:                (174,X,    'o',            'side',            'rsb',        """Cvt #174 (X) o Right sidebearing."""),
    FLOQ_lsbDiag:                (175,X,    'v',            'side',            'minX',        """Cvt #175 (X) v Left sidebearing."""),
    FLOQ_rsbDiag:                (176,X,    'v',            'side',            'rsb',        """Cvt #176 (X) v Right sidebearing."""),

    FLOQ_capVRun:                (177,D,    'V',            'run',            'run',        """Cvt #177 V run."""),
    FLOQ_capVStem:                (178,D,    'V',            'stem',            'diagonal',    """Cvt #178 V stem."""),
    FLOQ_capARun:                (179,D,    'A',            'run',            'run',        """Cvt #179 A run."""),
    FLOQ_capMRun:                (180,D,    'M',            'run',            'run',        """Cvt #180 M run."""),
    FLOQ_capWRun1:                (181,D,    'W',            'run',            'run',        """Cvt #181 W run 1."""),
    FLOQ_capWRun2:                (182,D,    'W',            'run',            'run',        """Cvt #182 W run 2."""),
    FLOQ_capXRun:                (183,D,    'X',            'run',            'run',        """Cvt #183 X run."""),
    FLOQ_capYRun:                (184,D,    'Y',            'run',            'run',        """Cvt #184 Y run."""),
    FLOQ_circRun:                (185,D,    'circ',            'run',            'rstem',    """Cvt #185 circ run."""),
    FLOQ_vRun:                    (186,D,    'v',            'run',            'run',        """Cvt #186 v run."""),
    FLOQ_wRun1:                    (187,D,    'w',            'run',            'run',        """Cvt #187 w run 1."""),
    FLOQ_xRun:                    (188,D,    'x',            'run',            'run',        """Cvt #188 x run."""),
    FLOQ_wRun2:                    (189,D,    'w',            'run',            'run',        """Cvt #189 w run 2."""),
    FLOQ_capHItalicRun:            (200,D,    'H',            'run',            'notdef',    """Cvt #200 H italic run."""),
    FLOQ_nItalicRun:                (201,D,    'n',            'run',            'notdef',    """Cvt #201 n italic run."""),
    FLOQ_hItalicRun:                (202,D,    'h',            'run',            'notdef',    """Cvt #202 h italic run."""),

    FLOQ_serif:                    (220,D,    'n',            'run',            'notdef',    """Cvt #220 (D) Serif diagonal indicator."""),
    FLOQ_capSerif:                (221,D,    'H',            'run',            'notdef',    """Cvt #221 (D) Cap serif diagonal indicator."""),

    FLOQ_unknown:                (FLOQ_UNKNOWN, '', '',    '',                'notdef',    """Floq #9999 Unknown Floq reference"""),

}
# Construct the various Floq entries.
# Note that due to the requirements of plist saving (the CVT table is inside
# the font.lib, the id's are converted to strings.
DEFAULT_FLOQ = {}
DEFAULT_USED_FLOQ = {}
DEFAULT_FLOQBYNAME = {}
DEFAULT_NAMEBYID = {}

maxid = 0
for key, (id, axis, defaultglyph, type, defaulthook, info) in DEFAULT_FLOQ_SOURCE.items():
    d = dict(id=id, name=key, axis=axis, defaultglyph=defaultglyph, type=type, defaulthook=defaulthook,
        locked=0, value=0, point='', parent='', glyph=defaultglyph, script='', comment='', info=info)
    # To be found as key and as key.lower()
    DEFAULT_FLOQBYNAME[key] = DEFAULT_FLOQBYNAME[key.lower()] = DEFAULT_USED_FLOQ[id] = DEFAULT_FLOQ[id] = d
    DEFAULT_NAMEBYID[id] = key
    maxid = max(maxid, id)
for id in range(0, maxid):
    if not id in DEFAULT_FLOQ:
        if id < FLOQ_CUSTOMINDEXSTART:
            info = RESERVED_BY_VTT_T % id
        else:
            info = CUSTOM_FLOQ_T % id
        DEFAULT_FLOQBYNAME[RESERVED_BY_VTT_T % id] = DEFAULT_FLOQ[id] = dict(id=id,
            name='cvt%d' % id, axis=AXIS_DEFAULT, defaultglyph='', type='', defaulthook='', locked=1, point='',
            parent='', glyph='', script='',  comment='', info=info)

DEFAULT_FLOQORDEREDNAMES = sorted(DEFAULT_FLOQBYNAME)

# ---------------------------------------------------------------------------------------------------------
#    I N S T R U C T I O N S

# Pushing data onto the interpreter stack
PUSH = 'PUSH'   # Pseudo code, automatic converted into the right push mnemonics
NPUSHB = 'NPUSHB'
NPUSHW = 'NPUSHW'

PUSHB = 'PUSHB' # Equivalent to PUSHB_1
PUSHB_1 = 'PUSHB_1'
PUSHB_2 = 'PUSHB_2'
PUSHB_3 = 'PUSHB_3'
PUSHB_4 = 'PUSHB_4'
PUSHB_5 = 'PUSHB_5'
PUSHB_6 = 'PUSHB_6'
PUSHB_7 = 'PUSHB_7'
PUSHB_8 = 'PUSHB_8'

PUSHW = 'PUSHW' # Equivalent to PUSHW_1
PUSHW_1 = 'PUSHW_1'
PUSHW_2 = 'PUSHW_2'
PUSHW_3 = 'PUSHW_3'
PUSHW_4 = 'PUSHW_4'
PUSHW_5 = 'PUSHW_5'
PUSHW_6 = 'PUSHW_6'
PUSHW_7 = 'PUSHW_7'
PUSHW_8 = 'PUSHW_8'

# Managing the Storage Area
RS = 'RS'
WS = 'WS'

# Managing the Control Value Table
WCVTP = 'WCVTP'
WCVTF = 'WCVTF'
RCVT = 'RCVT'

# Manage the Gaphics State
SVTCA_X = 'SVTCA_X'
SVTCA_Y = 'SVTCA_Y'
SPVTCA_X = 'SPVTCA_X'
SPVTCA_Y = 'SPVTCA_Y'
SFVTCA_X = 'SFVTCA_X'
SFVTCA_Y = 'SFVTCA_Y'
SPVTL_r = 'SPVTL_r'
SPVTL_R = 'SPVTL_R'
SFVTL_r = 'SFVTL_r'
SFVTL_R = 'SFVTL_R'
SFVTPV = 'SFVTPV'
SDPVTL_r = 'SDPVTL_r'
SDPVTL_R = 'SDPVTL_R'
SPVFS = 'SPVFS'
SFVFS = 'SFVFS'
GPV = 'GPV'
GFV = 'GFV'
SRP0 = 'SRP0'
SRP1 = 'SRP1'
SRP2 = 'SRP2'
SZP0 = 'SZP0'
SZP1 = 'SZP1'
SZP2 = 'SZP2'
SZPS = 'SZPS'
RTHG = 'RTHG'
RTG = 'RTG'
RTDG = 'RTDG'
RDTG = 'RDTG'
RUTG = 'RUTG'
ROFF = 'ROFF'
SROUND = 'SROUND'
S45ROUND = 'S45ROUND'
SLOOP = 'SLOOP'
SMD = 'SMD'
INSTCTRL = 'INSTCTRL'
SCANCTRL = 'SCANCTRL'
SCANTYPE = 'SCANTYPE'
SCVTCI = 'SCVTCI'
SSWCI = 'SSWCI'
SSW = 'SSW'
FLIPON = 'FLIPON'
FLIPOFF = 'FLIPOFF'
AA = 'AA'
SANGW = 'SANGW'
SDB = 'SDB'
SDS = 'SDS'

# Reading and writing data
GC_curp = 'GC_curp'
GC_orgp = 'GC_orgp'
SCFS = 'SCFS'
MD_grid = 'MD_grid'
MD_org = 'MD_org'
MPPEM = 'MPPEM'
MPS = 'MPS'

# Managing outlines
FLIPPT = 'FLIPPT'
FLIPRGEON = 'FLIPRGEON'
FLIPRGEOFF = 'FLIPRGEOFF'
SHP_0 = 'SHP_0'
SHP_1 = 'SHP_1'
SHC_0 = 'SHC_0'
SHC_1 = 'SHC_1'
SHZ_0 = 'SHZ_0'
SHZ_1 = 'SHZ_1'
SHPIX = 'SHPIX'
MSIRP_m = 'MSIRP_m'
MSIRP_M = 'MSIRP_M'
MDAP_r = 'MDAP_r'
MDAP_R = 'MDAP_R'
MIAP_r = 'MIAP_r'
MIAP_R = 'MIAP_R'
MDRP_m_lt_r_Gray = 'MDRP_m_lt_r_Gray'
MDRP_M_lt_r_Gray = 'MDRP_M_lt_r_Gray'
MDRP_m_gt_r_Gray = 'MDRP_m_gt_r_Gray'
MDRP_M_gt_r_Gray = 'MDRP_M_gt_r_Gray'
MDRP_m_lt_R_Gray = 'MDRP_m_lt_R_Gray'
MDRP_M_lt_R_Gray = 'MDRP_M_lt_R_Gray'
MDRP_m_gt_R_Gray = 'MDRP_m_gt_R_Gray'
MDRP_M_gt_R_Gray = 'MDRP_M_gt_R_Gray'
MDRP_m_lt_r_Black = 'MDRP_m_lt_r_Black'
MDRP_M_lt_r_Black = 'MDRP_M_lt_r_Black'
MDRP_m_gt_r_Black = 'MDRP_m_gt_r_Black'
MDRP_M_gt_r_Black = 'MDRP_M_gt_r_Black'
MDRP_m_lt_R_Black = 'MDRP_m_lt_R_Black'
MDRP_M_lt_R_Black = 'MDRP_M_lt_R_Black'
MDRP_m_gt_R_Black = 'MDRP_m_gt_R_Black'
MDRP_M_gt_R_Black = 'MDRP_M_gt_R_Black'
MDRP_m_lt_r_White = 'MDRP_m_lt_r_White'
MDRP_M_lt_r_White = 'MDRP_M_lt_r_White'
MDRP_m_gt_r_White = 'MDRP_m_gt_r_White'
MDRP_M_gt_r_White = 'MDRP_M_gt_r_White'
MDRP_m_lt_R_White = 'MDRP_m_lt_R_White'
MDRP_M_lt_R_White = 'MDRP_M_lt_R_White'
MDRP_m_gt_R_White = 'MDRP_m_gt_R_White'
MDRP_M_gt_R_White = 'MDRP_M_gt_R_White'

MIRP_m_lt_r_Gray = 'MIRP_m_lt_r_Gray'
MIRP_M_lt_r_Gray = 'MIRP_M_lt_r_Gray'
MIRP_m_gt_r_Gray = 'MIRP_m_gt_r_Gray'
MIRP_M_gt_r_Gray = 'MIRP_M_gt_r_Gray'
MIRP_m_lt_R_Gray = 'MIRP_m_lt_R_Gray'
MIRP_M_lt_R_Gray = 'MIRP_M_lt_R_Gray'
MIRP_m_gt_R_Gray = 'MIRP_m_gt_R_Gray'
MIRP_M_gt_R_Gray = 'MIRP_M_gt_R_Gray'
MIRP_m_lt_r_Black = 'MIRP_m_lt_r_Black'
MIRP_M_lt_r_Black = 'MIRP_M_lt_r_Black'
MIRP_m_gt_r_Black = 'MIRP_m_gt_r_Black'
MIRP_M_gt_r_Black = 'MIRP_M_gt_r_Black'
MIRP_m_lt_R_Black = 'MIRP_m_lt_R_Black'
MIRP_M_lt_R_Black = 'MIRP_M_lt_R_Black'
MIRP_m_gt_R_Black = 'MIRP_m_gt_R_Black'
MIRP_M_gt_R_Black = 'MIRP_M_gt_R_Black'
MIRP_m_lt_r_White = 'MIRP_m_lt_r_White'
MIRP_M_lt_r_White = 'MIRP_M_lt_r_White'
MIRP_m_gt_r_White = 'MIRP_m_gt_r_White'
MIRP_M_gt_r_White = 'MIRP_M_gt_r_White'
MIRP_m_lt_R_White = 'MIRP_m_lt_R_White'
MIRP_M_lt_R_White = 'MIRP_M_lt_R_White'
MIRP_m_gt_R_White = 'MIRP_m_gt_R_White'
MIRP_M_gt_R_White = 'MIRP_M_gt_R_White'

ALIGNRP = 'ALIGNRP'
ISECT = 'ISECT'
ALIGNPTS = 'ALIGNPTS'
IP = 'IP'
UTP = 'UTP'
IUP_Y = 'IUP_Y'
IUP_X = 'IUP_X'

# Exceptions
DELTAP1 = 'DELTAP_1'
DELTAP2 = 'DELTAP_2'
DELTAP3 = 'DELTAP_3'
DELTAC1 = 'DELTAC_4'
DELTAC2 = 'DELTAC_5'
DELTAC3 = 'DELTAC_6'

# Managing the stack
DUP = 'DUP'
POP = 'POP'
CLEAR = 'CLEAR'
SWAP = 'SWAP'
DEPTH = 'DEPTH'
CINDEX = 'CINDEX'
MINDEX = 'MINDEX'
ROLL = 'ROLL'

# Flow control
IF = 'IF'
ELSE = 'ELSE'
EIF = 'EIF'
JROT = 'JROT'
JMPR = 'JMPR'
JROF = 'JROF'

# Logical instructions
LT = 'LT'
LTEQ = 'LTEQ'
GT = 'GT'
GTEQ = 'GTEQ'
EQ = 'EQ'
NEQ = 'NEQ'
ODD = 'ODD'
EVEN = 'EVEN'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'

# Arithmetic and math instructions
ADD = 'ADD'
SUB = 'SUB'
DIV = 'DIV'
MUL = 'MUL'
ABS = 'ABS'
NEG = 'NEG'
FLOOR = 'FLOOR'
CEILING = 'CEILING'
MAX = 'MAX'
MIN = 'MIN'

# Compensating for machine characteristics
ROUND_gray = 'ROUND_gray'
ROUND_black = 'ROUND_black'
ROUND_white = 'ROUND_white'
NROUND_gray = 'NROUND_gray'
NROUND_black = 'NROUND_black'
NROUND_white = 'NROUND_white'

# Defining and using functions and instructions
FDEF = 'FDEF'
ENDF = 'ENDF'
CALL = 'CALL'
LOOPCALL = 'LOOPCALL'
IDEF = 'IDEF'
DEBUG = 'DEBUG'
GETINFO = 'GETINFO'

# Unknown or error from UI (not part of standard mnemonic set)
UNKNOWN = 'UNKNOWN'
EMPTY = 'EMPTY'

# VTTR Talk
VTT_BEGIN = '#BEGIN'
VTT_END = '#END'
VTT_PUSH = '#PUSH'
VTT_PUSHON = '#PUSHON'
VTT_PUSHOFF = '#PUSHOFF'
VTT_MSIRP_m = 'MSIRP_m'

