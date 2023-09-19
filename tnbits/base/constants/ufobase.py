# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     ufobase.py
#
def f2f(s): # Floq name to field name
    return s.replace('ID','_id')

"""
Shared parameters with web server environment.
"""
TABLE_ITEM = 'item' # Main tree item with library records.
TABLE_ADDRESS = 'address' # Users and roles.
TABLE_NOTE = 'note' # Table with "yellow" notes about items.
TABLE_PROJECT = 'project' # Tree table with information about a project.
TABLE_ASSOCIATION = 'association' # Associative binding between items.
TABLE_LOG = 'log' # Logging of everything that happens in the database.

# P A R A M

PARAM_POSTITEM = 'postItem' # Generic url parameter for uploading a single item
PARAM_AJAX = 'ajax'

PARAM_ITEMS = 'items' # Answer a (sliced) list of all items.
PARAM_MAGICKEY = 'm' # Magic key to be added to id number.
PARAM_ORDER = 'order'
PARAM_FIELD = 'field'
PARAM_USER = 'user'
PARAM_JSON = 'json' # Storage of the main block, e.g. the font data in a POST.

# POST parameters.

PARAM_INSERTLIBRARY = 'insertLibrary'
PARAM_INSERTSERIES = 'insertSeries'
PARAM_INSERTSTYLE = 'insertStyle'
PARAM_UPDATESTYLE = 'updateStyle'
PARAM_UPLOADSTYLE = 'uploadStyle' # Upload the font item and glyph items.
PARAM_UPLOADSTYLEINFO = 'uploadStyleInfo'
PARAM_DELETESTYLE = 'deleteStyle'
PARAM_DESTROYSTYLE = 'destroyStyle' # Really remove the items from the database.

# GET parameters.

PARAM_GETLOGIN = 'getLogin'
#PARAM_GETSTYLESTATE = 'getStyleState'
PARAM_GETROOT = 'getRoot' # Answer the single root record
PARAM_GETFOUNDRYLIST = 'getFoundryList'
PARAM_GETLIBRARYLIST = 'getLibraryList'
PARAM_GETSERIESLIST = 'getSeriesList'
PARAM_GETFAMILYLIST = 'getFamilyList' # Answer a list of all families.
PARAM_GETSTYLELIST = 'getStyleList' # Answer the list with available styles.
PARAM_GETGLYPHLIST = 'getGlyphList'
#PARAM_GETITEMS = 'getItems' # Answer a (sliced) list of all items.
PARAM_GETGLYPHBYNAME = 'getGlyphByName'                 # Answer the glyph item, indicated by name and parent_id
PARAM_GETTYPES = 'getTypes' # Answer all records from the common root that is one of the indicated types.
#PARAM_GETSTYLESBYFAMILYID = 'getStylesByFamilyID' # Answer the styles of the given family ids
PARAM_GETBYNAME = 'getByName'

PARAM_START = 'start' # Answer the start indexof a slice
PARAM_SLICE = 'slice' # Answer the slice size

PARAM_GETTYPES = 'getTypes'
PARAM_GETBYID = 'getByID'
PARAM_GETBYPARENTID = 'getByParentID'
PARAM_GETBYNAME = 'getByName' # Answer the item which name exactly matches the name.
#PARAM_GETLIKE = 'getLike' # Answer the set of items that includes the name pattern.

# Auxiliary GET parameters.

PARAM_TYPE = 'type'
PARAM_PARENTID = 'parent_id' # Parent id of an item.
PARAM_PARENTOFNAME = 'parentofname'
PARAM_PARENTOFID = 'parentofid'
PARAM_ROOTOFNAME = 'rootofname'
PARAM_ROOTOFID = 'rootofid'
PARAM_GLYPH = 'glyph'
PARAM_USER = 'user'
PARAM_PASSWORD = 'password' # Encrypted password in the URL by TX.encryptPassword().
PARAM_NAME = 'name'
PARAM_LIKE = 'like'
PARAM_GETSTYLESTATE = 'getstylestate'

PARAM_VERIFY = 'verify'
PARAM_FORMCMD = 'formcmd'
PARAM_PAGESLICE = 'pageslice'
PARAM_PAGESTART = 'pagestart'
PARAM_PAGELEFT = 'pageleft'
PARAM_PAGERIGHT = 'pageright'
PARAM_PAGEEND = 'pageend'
PARAM_SELECTITEM = 'selectitem'
PARAM_SELECTIONTYPE = 'selectiontype'
PARAM_BATCH = 'batch' # Holding the name of the batch process to be executed.

# For a complete set of fields see
#
# /XierpaDev/Applications/TypeNetworkLibrary/src/typenetworklibrary/_py/models.py.
#
# Fields used as attributes in floqs must have camelCase to be compatible with
# standard fields in RoboFont.

FLOQ_ID = 'id'
FLOQ_WIDTHVALUE = 'widthValue'
FLOQ_WEIGHTVALUE = 'weightValue'
FLOQ_ANGLEVALUE = 'angleValue'
FLOQ_SIZEVALUE = 'sizeValue'
FLOQ_GRADEVALUE = 'gradeValue'
FLOQ_LEFTMARGIN = 'leftMargin'
FLOQ_RIGHTMARGIN = 'rightMargin'
FLOQ_WIDTH = 'width'
FLOQ_STEM = 'stem'
FLOQ_EM = 'em'
FLOQ_DESCENDER = 'descender'
FLOQ_ASCENDER = 'ascender'
FLOQ_BASELINE = 'baseline'
FLOQ_XHEIGHT = 'xHeight'
FLOQ_CAPHEIGHT = 'capHeight'
FLOQ_MODIFICATIONDATETIME = 'modificationDateTime'
FLOQ_MODIFICATIONUSERID = 'modificationUserID'
FLOQ_CREATIONDATETIME = 'creationDateTime'
FLOQ_CREATIONUSERID = 'creationUserID'
FLOQ_OPTIMALMINSIZE = 'optimalMinSize'
FLOQ_OPTIMALSIZE = 'optimalSize'
FLOQ_OPTIMALMAXSIZE = 'optimalMaxSize'
FLOQ_STATUS = 'status'
FLOQ_TYPE = 'type'
FLOQ_NAME = 'name'
FLOQ_IDNAME = 'idName'
FLOQ_ROOTID = 'rootID'
FLOQ_PARENTID = 'parentID'
FLOQ_VERSION = 'version'
FLOQ_FLOQMEMES = 'floqMemes'
FLOQ_UFO = 'ufo'
FLOQ_INFO = 'info'
FLOQ_FEATURES = 'features'
FLOQ_CHARACTERMAPPING = 'characterMapping'
FLOQ_GROUPS = 'groups'
FLOQ_KERNING = 'kerning'
FLOQ_LIB = 'lib'
FLOQ_UNICODES = 'unicodes'
FLOQ_DELETED = 'deleted'
FLOQ_FILTER = 'filter'
FLOQ_CHILDREN = 'children'
FLOQ_USERID = 'userid'

# Some queries don't need the full item set as default, so the query/url can
# defined the fields. FLOQS_ITEMBASE list below is always included.
FLOQS_ITEMBASE = [
    FLOQ_NAME, FLOQ_IDNAME, FLOQ_ID, FLOQ_ROOTID, FLOQ_TYPE, FLOQ_DELETED,
    FLOQ_MODIFICATIONDATETIME, FLOQ_PARENTID, FLOQ_VERSION, FLOQ_STATUS,
]

# The basic set of item fields includes the main values, but not the large lists.
FLOQS_ITEMSMALL = FLOQS_ITEMBASE + [
    FLOQ_FLOQMEMES, # Dictionary that contains FloqMeme instances by key.
    FLOQ_UFO, # For glyphs this contains the glyph UFO XML
    FLOQ_INFO, # Read style.info too, so we can "repair" the search fields on style level
]

# The extended set includes the large lists, such as kerning, info and lib.
FLOQS_ITEMEXTENDED = FLOQS_ITEMSMALL + [
    FLOQ_FEATURES, # read on extending
    FLOQ_LIB, # read on extending
    FLOQ_UNICODES, # read on extending
]

# The full read includes all search words. These are normally only used for
# writing as they are for searching in the database.
FLOQS_ITEMFULL = FLOQS_ITEMEXTENDED + [
    FLOQ_CREATIONDATETIME, FLOQ_CREATIONUSERID,
    FLOQ_MODIFICATIONUSERID,
    FLOQ_CHARACTERMAPPING, # read on extending
    FLOQ_GROUPS, # read on extending
    FLOQ_KERNING, # read on extending
    FLOQ_WIDTH, FLOQ_STEM, FLOQ_EM,
    FLOQ_LEFTMARGIN, FLOQ_RIGHTMARGIN, FLOQ_DESCENDER, FLOQ_ASCENDER,
    FLOQ_BASELINE, FLOQ_XHEIGHT, FLOQ_CAPHEIGHT, # Dimensions
    FLOQ_FILTER, FLOQ_WEIGHTVALUE, FLOQ_WIDTHVALUE, FLOQ_SIZEVALUE,
    FLOQ_ANGLEVALUE, FLOQ_GRADEVALUE,
    FLOQ_OPTIMALMINSIZE, FLOQ_OPTIMALSIZE, FLOQ_OPTIMALMAXSIZE,
]

FLOQS_ITEMBASE = set(FLOQS_ITEMBASE) # Allow fast searching for field name in the groups
FLOQS_ITEMSMALL = set(FLOQS_ITEMSMALL)
FLOQS_ITEMEXTENDED = set(FLOQS_ITEMEXTENDED)
FLOQS_ITEMFULL = set(FLOQS_ITEMFULL)
FLOQS_LEVELS = (FLOQS_ITEMBASE, FLOQS_ITEMSMALL, FLOQS_ITEMEXTENDED, FLOQS_ITEMFULL)

SCRIPTABLE_FLOQMEMES = set([
    FLOQ_WIDTH, FLOQ_STEM, FLOQ_EM,
    FLOQ_LEFTMARGIN, FLOQ_RIGHTMARGIN, FLOQ_DESCENDER, FLOQ_ASCENDER,
    FLOQ_BASELINE, FLOQ_XHEIGHT, FLOQ_CAPHEIGHT, # Dimensions
    FLOQ_WEIGHTVALUE, FLOQ_WIDTHVALUE, FLOQ_SIZEVALUE,
    FLOQ_ANGLEVALUE, FLOQ_GRADEVALUE,
    FLOQ_OPTIMALMINSIZE, FLOQ_OPTIMALSIZE, FLOQ_OPTIMALMAXSIZE
])

# Address: who-did-it table
FIELD_LOGIN = 'login'
FIELD_EMAIL = 'email'
FIELD_FIRSTNAME = 'firstName'
FIELD_MIDDLENAME = 'middleName'
FIELD_FAMILYNAME = 'familyName'
FIELD_ROLES = 'roles'
FIELD_PASSWORD = 'password'
FIELD_PREFERENCES = 'preferences'

# Note
FIELD_ITEM = 'item_id'
FIELD_NOTE = 'note'

# Binding
FIELD_SRC = 'src_id'
FIELD_DST = 'dst_id'
FIELD_STRENGTH = 'strength'
FIELD_BINDING = 'binding'

# Log (WhoDidId)
FIELD_USER = 'user'
FIELD_DESCRIPTION = 'description'
FIELD_VALUE = 'value'
FIELD_ACTIVITIES = 'activities' # Set of all activities that where performed in this log action

# Project
FIELD_CLIENTID = 'client_id'
FIELD_STATUS = FLOQ_STATUS
FIELD_CHILDREN = 'children'
FIELD_FILTER = 'filter'

# Status fields
JSON_GETRESULT = 'getresult'
JSON_POSTRESULT = 'postresult'
JSON_GETTYPE = 'gettype'
JSON_POSTTYPE = 'posttype'
