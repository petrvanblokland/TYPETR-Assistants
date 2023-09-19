# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    tool.py
#

# Measures for layouts.

UNIT = 10
GUTTER = UNIT
COLUMN = 8 * UNIT
BUTTON_WIDTH = COLUMN
BIGBUTTON_WIDTH = 12*UNIT

# NOTE: Button height should correspond to 'regular', 'small' or 'mini'
# sizeStyle.
BUTTON_HEIGHT = 2 * UNIT
BUTTON_HEIGHT_REGULAR = BUTTON_HEIGHT
BUTTON_HEIGHT_SMALL = 17
BUTTON_HEIGHT_MINI = 14
PADDING = UNIT / 2
MENU = 3 * UNIT
SIDE = 20 * UNIT

C1 = 0 # Column 1
C2 = C1 + COLUMN + GUTTER # Column 2
C3 = C2 + COLUMN + GUTTER # Column 3
C4 = C3 + COLUMN + GUTTER # Column 4

# Leading between components

L = 2*UNIT
LL = 2*L
LLL = 3*L
LLLL = 4*L
LLLLL = 5*L

S = 'small'
MAXINT = 100000000
HUNITS = 64.0 # Multiplication factor for fixed vector values

FALSEVALUES = ('', 0, '0', 'f', 'F', 'none', 'None', 'NONE', 'false', 'False',
        'FALSE', 'n', 'N', 'no', 'No', 'NO', None, False)

PLUSMIN = [{'title': "+", 'width': 2*UNIT,}, {'title': "-", 'width': 2*UNIT}]
NONE = 'None'
ANY = 'Any'

# ---------------------------------------------------------------------------------------------------------
#    U S E R  I N T E R F A C E

# Module interface markers
MARK_CURRENT = u'➤'
MARK_OPENED = u'O'

# Generic boolean list label
POINTMARKER_TRUE = u'✓'
POINTMARKER_FALSE = u'✗'
POINTMARKER_EMPTY = ''

# Labels
LABEL_STATUS = 'Status'
LABEL_PATH = 'Path'
LABEL_FID = 'fid' # FLoq id. Can be path or record id.
LABEL_NAME = 'Name'
LABEL_IMAGE = 'Image'
LABEL_CHR = 'Chr'
LABEL_VALUE = 'Value'
LABEL_ID = 'ID'
LABEL_COMMENT = 'Comment'
LABEL_CONTENT = 'Content'
LABEL_MODIFIED = 'X'
LABEL_USER = 'user'
LABEL_PPEM = 'Em' # Units per em
LABEL_ASCENDER = 'Asc'
LABEL_CAPHEIGHT = 'Hght'
LABEL_XHEIGHT = 'xHght'
LABEL_DESCENDER = 'Desc'

# Tab styles (from Vanilla)
TABSTYLE_MINI = 'mini'
TABSTYLE_SMALL = 'small'
TABSTYLE_REGULAR = 'regular'

# Predefined styles for various components
STYLE_ERRORSIZE = TABSTYLE_SMALL
STYLE_POPUPSIZE = TABSTYLE_MINI
STYLE_RADIOSIZE = TABSTYLE_SMALL
STYLE_BUTTONSIZE = TABSTYLE_MINI
STYLE_BIGBUTTONSIZE = TABSTYLE_REGULAR
STYLE_LABELSIZE = TABSTYLE_SMALL
STYLE_TEXTBOXSIZE = TABSTYLE_SMALL
STYLE_PROGRAMSIZE = TABSTYLE_SMALL
STYLE_SLIDERSIZE = TABSTYLE_MINI
STYLE_CHECKBOXSIZE = TABSTYLE_SMALL
STYLE_CHECKBOXSIZEMINI = TABSTYLE_MINI

MENUHEIGHT = 0

# Tool values
VALUE_POINTRADIUS = 8 # Radius of a winglabel point and selection area

# ---------------------------------------------------------------------------------------------------------
# C A T E G O R I E S

CATEGORY_LAB = 'Lab'
CATEGORY_DEVELOPMENT = 'Development'
CATEGORY_MANAGE = 'Manage'
CATEGORY_DESIGN = 'Design'
CATEGORY_ANALYZE = 'Analyze'
CATEGORY_GENERALIZE = 'Generalize'
CATEGORY_PRODUCTIZE = 'Productize'
CATEGORY_PUBLICIZE = 'Publicize'
CATEGORY_MONETIZE = 'Monetize'

CATEGORIES = (CATEGORY_MANAGE, CATEGORY_DESIGN, CATEGORY_ANALYZE,
        CATEGORY_GENERALIZE, CATEGORY_PRODUCTIZE, CATEGORY_PUBLICIZE,
        CATEGORY_MONETIZE)

# ---------------------------------------------------------------------------------------------------------
# L A B E L S

LABEL_OPENFONT = 'Open Font'
LABEL_SELECTAFONT = 'Select a font:'

# ---------------------------------------------------------------------------------------------------------
#    P R E F E R E N C E S

PREF_PATHLIST = 'pathList'
PREF_SELECTEDTOOLS = 'selectedTools'
PREF_FLOATINGWINDOW = 'useFloatingWindow' # Ordering key for window type boolean
PREF_WINDOWPOSSIZE = 'windowPosSize' # Standard sorting preference key and label of window positions

# Types of preference values. Used in PREFERENCE_MODEL, so auto UI can be generated
# and they can be stored in a central place in RoboFont, related to the tool ID.
PREFTYPE_BOOL = 'bool'
PREFTYPE_INT = 'int'
PREFTYPE_FLOAT = 'float'
PREFTYPE_RECT = 'rect'
PREFTYPE_COLOR = 'color'
PREFTYPE_SIZE = 'size'
PREFTYPE_LABEL = 'label'
PREFTYPE_RADIO = 'radio'
PREFTYPE_LIST = 'list' # Generate popup, single value choice.

# ---------------------------------------------------------------------------------------------------------
#    E X T E N S I O N S

EXTENSION_UFO = 'ufo'
EXTENSION_TTF = 'ttf'
EXTENSION_OTF = 'otf'
EXTENSION_WOFF = 'woff'
EXTENSION_EOT = 'eot'
EXTENSION_TTX = 'ttx'
EXTENSION_SVG = 'svg'
ALLOWED_EXTENSIONS = (EXTENSION_UFO, EXTENSION_TTF, EXTENSION_EOT,
        EXTENSION_OTF, EXTENSION_WOFF, EXTENSION_TTX, EXTENSION_SVG)
EXTENSION_FAM = 'fam'
EXTENSION_DESIGNSPACE = 'designspace'

# ---------------------------------------------------------------------------------------------------------
#    F O R M A T S

FORMATS = [EXTENSION_OTF, EXTENSION_TTF]

# ---------------------------------------------------------------------------------------------------------
#    L A Y E R S

LAYER_FOREGROUND = 'foreground'
LAYER_BACKGROUND = 'background'
LAYER_ROBOHINT = 'fbhint'
LAYER_FREETYPE = 'freetype'
LAYER_NOVERLAP = 'noverlap' # Copy from foreground with overlap removed.
LAYER_INTERPOLATE = 'fbinterpolate'

# ---------------------------------------------------------------------------------------------------------
#    E V E N T  N A M E S  F R O M  R O B O F O N T  W I N D O W
#
#    See: http://doodletrac.typemytype.com/browser/doodle/trunk/lib/eventTools/baseEventTool.py
#    http://code.typesupply.com/browser/packages/defcon/trunk/Lib/defcon/objects/glyph.py#L48

EVENT_MOUSEUP = 'mouseUp'
EVENT_MOUSEDOWN = 'mouseDown'
EVENT_MOUSEMOVED = 'mouseMoved'
EVENT_MOUSEDRAGGED = 'mouseDragged'
EVENT_RIGHTMOUSEDOWN = 'rightMouseDown'
EVENT_RIGHTMOUSEDRAGGED = 'rightMouseDragged'
EVENT_KEYDOWN = 'keyDown'
EVENT_KEYUP = 'keyUp'
EVENT_MODIFIERSCHANGED = 'modifiersChanged'
EVENT_SELECTALL = 'selectAll'
EVENT_DIDUNDO = 'didUndo'
EVENT_COPY = 'copy'
EVENT_COPYASCOMPONENT = 'copyAsComponent'
EVENT_CUT = 'cut'
EVENT_DELETE = 'delete'
EVENT_PASTE = 'paste'

EVENT_BINARYFONTWILLOPEN = 'binaryFontWillOpen'
EVENT_FONTWILLGENERATE = 'fontWillGenerate'
EVENT_FONTDIDGENERATE = 'fontDidGenerate'
EVENT_FONTWILLSAVE = 'fontWillSave'
EVENT_FONTDIDSAVE = 'fontDidSave'
EVENT_FONTWILLOPEN = 'fontWillOpen'
EVENT_FONTDIDOPEN = 'fontDidOpen'
EVENT_FONTWILLCLOSE = 'fontWillClose'
EVENT_FONTDIDCLOSE = 'fontDidClose'
EVENT_FONTBECAMECURRENT = 'fontBecameCurrent'
EVENT_FONTREFRAINCURRENT = 'fontRefrainCurrent'
EVENT_FONTRESIGNCURRENT = 'fontResignCurrent'

EVENT_GLYPHWINDOWWILLCLOSE = 'glyphWindowWillClose'
EVENT_TOGGLETRANSFORMMODE = 'toggleTransformMode'
EVENT_VIEWDIDCHANGEGLYPH = 'viewDidChangeGlyph'
EVENT_CURRENTGLYPHCHANGED = 'currentGlyphChanged'
EVENT_CURRENTFONTCHANGED = 'currentFontChanged'
EVENT_FEATURESCHANGED = 'Features.Changed'
EVENT_DRAWBACKGROUND = 'drawBackground'
EVENT_DRAW = 'draw'
EVENT_DRAWINACTIVE = 'drawInactive'
EVENT_DRAWSPACECENTER = 'spaceCenterDraw'
EVENT_CLOSE = 'close'
EVENT_BECOMEACTIVE = 'becomeActive'
EVENT_BECOMEINACTIVE = 'becomeInactive'

# DefCon events.
EVENT_FONTCHANGED = 'Font.Changed'
EVENT_GLYPHSETCHANGED = 'Font.GlyphSetChanged'
EVENT_GLYPHCHANGED = 'Glyph.Changed' # Posted when the *dirty* attribute is set.
EVENT_GLYPHWIDTHCHANGED = 'Glyph.WidthChanged' # DoodleFont notification
EVENT_GLYPHSELECTIONCHANGED = 'Glyph.selectionChanged' # DoodleFont nofitication
EVENT_GLYPHNAMECHANGED = 'Glyph.NameChanged' # Posted after the *reloadGlyphs* method has been called.
EVENT_GLYPHUNICODESCHANGED = 'Glyph.UnicodesChanged' # Posted after the *reloadGlyphs* method has been called.
EVENT_INFOCHANGED = 'Info.Changed'
EVENT_LIBCHANGED = 'Lib.Changed'
EVENT_GLYPHZOOMVIEWSHOWITEMSCHANGED = 'doodle.glyphZoomViewShowItemsDidChange'

# Use in combination with self.setUpObeserverCallBacks
# to register the callback if there is a method with
# name 'observer' + eventName
ALLEVENTS = (
    EVENT_MOUSEDOWN,
    EVENT_RIGHTMOUSEDOWN,
    EVENT_MOUSEDRAGGED,
    EVENT_RIGHTMOUSEDRAGGED,
    EVENT_MOUSEMOVED,
    EVENT_MOUSEUP,
    EVENT_KEYDOWN,
    EVENT_KEYUP,
    EVENT_MODIFIERSCHANGED,
    EVENT_SELECTALL,
    EVENT_COPY,
    EVENT_COPYASCOMPONENT,
    EVENT_CUT,
    EVENT_DELETE,
    EVENT_PASTE,
    EVENT_TOGGLETRANSFORMMODE,
    EVENT_VIEWDIDCHANGEGLYPH,
    EVENT_DRAWBACKGROUND,
    EVENT_DRAW,
    EVENT_BECOMEACTIVE,
    EVENT_BECOMEINACTIVE,

    EVENT_FONTCHANGED,
    EVENT_GLYPHSETCHANGED,
    EVENT_GLYPHCHANGED,
    EVENT_GLYPHNAMECHANGED,
    EVENT_GLYPHUNICODESCHANGED,
    EVENT_INFOCHANGED,
    EVENT_LIBCHANGED,
)
EVENT_OBSERVERPREFIX = 'observer'

# ---------------------------------------------------------------------------------------------------------
#    M A N U A L

TEMPLATE_MANUAL = 'index.html'
PATH_FONTANALYZER = 'fontAnalyzer.html'
