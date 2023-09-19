# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     filtertags.py
#
# Filter and other field tags

class FilterTags:

    # 0-999 Types of item records
    """
    TYPE_LIBRARY = 100
    TYPE_SERIES = 200
    TYPE_FAMILY = 300
    TYPE_GAGGLE = 350 # Sets of styles for a specific purpose/group/usage 
    TYPE_STYLE = TYPE_FONT = 400 # Although "Font" is deprecated as name
    TYPE_GLYPH = 500
    TYPE_LAYER = 600
    """
    # Item Type (used in FIELD_ITEMTYPE field)
    # Identical to XierpaDev constants
    ITEMTYPE_SITE = 10001
    ITEMTYPE_MAGAZINE = 10002
    ITEMTYPE_ARTICLE = 10003
    ITEMTYPE_PAGE = 10004
    ITEMTYPE_IMAGEREF = 10005  # X-reference between article and image
    ITEMTYPE_IMAGE = 10006
    ITEMTYPE_BLOG = 10007
    ITEMTYPE_AD = 10008
    ITEMTYPE_COVERREF = 10009
    ITEMTYPE_404 = 10010
    ITEMTYPE_PERSON = 10014
    ITEMTYPE_GAGGLE = 10018

    # Types of items in the database, related to the UFO tree.
    # Root<--Foundry<--Library<--Series<--Family<--Gaggle<--Font/Style<--Glyph<--Floq
    ITEMTYPE_ROOT = 10013
    ITEMTYPE_FOUNDRY = 10015
    ITEMTYPE_LIBRARY = 10016
    ITEMTYPE_SERIES = 10017  
    ITEMTYPE_FAMILY = 10011  
    ITEMTYPE_FONT = ITEMTYPE_STYLE = 10012  
    ITEMTYPE_GLYPH = 10019

    ITEMTYPE_DEFAULT = ITEMTYPE_FOUNDRY
    
    ITEM_TYPESET = (ITEMTYPE_ROOT, ITEMTYPE_FOUNDRY, ITEMTYPE_LIBRARY, ITEMTYPE_SERIES, 
    	ITEMTYPE_FAMILY, ITEMTYPE_GAGGLE, ITEMTYPE_STYLE, ITEMTYPE_GLYPH)

    # 1000-9999 Categories of type
    CATEGORY_SANS = 1000
    CATEGORY_SERIF = 1100
    CATEGORY_SLAB = 1200
    CATEGORY_SCRIPT = 1300
    CATEGORY_DECORATIVE = 1400

    CATEGORIES = (CATEGORY_SANS, CATEGORY_SERIF, CATEGORY_SLAB, CATEGORY_SCRIPT, CATEGORY_DECORATIVE)

    # 2000-2999 widths of type
    WIDTH_ULTRANARROW = 2000
    WIDTH_EXTRANARROW = 2100
    WIDTH_NARROW = 2200
    WIDTH_NORMAL = 2300
    WIDTH_WIDE = 2400
    WIDTH_EXTRAWIDE = 2500
    WIDTH_ULTRAWIDE = 2600

    WIDTHS = (WIDTH_EXTRANARROW, WIDTH_NARROW, WIDTH_NORMAL, WIDTH_WIDE, WIDTH_EXTRAWIDE)
    # 3000-4999 Weights of type
    WEIGHT_ULTRALIGHT = 3000
    WEIGHT_EXTRALIGHT = 3100
    WEIGHT_LIGHT = 3200
    WEIGHT_NORMAL = 3300
    WEIGHT_BOOK = 3400
    WEIGHT_MEDIUM = 3500
    WEIGHT_SEMIBOLD = 3600
    WEIGHT_BOLD = 3700
    WEIGHT_EXTRABOLD = 3800
    WEIGHT_EXTRABOLD = 3900
    WEIGHT_BLACK = 4000

    WEIGHTS = (
        WEIGHT_ULTRALIGHT, WEIGHT_EXTRALIGHT, WEIGHT_LIGHT, WEIGHT_NORMAL, WEIGHT_BOOK,
        WEIGHT_MEDIUM, WEIGHT_SEMIBOLD, WEIGHT_BOLD, WEIGHT_EXTRABOLD, WEIGHT_EXTRABOLD,
        WEIGHT_BLACK
    )

    # 5000-5999 Usage of type
    USAGE_MAGAZINE = 5000
    USAGE_NEWSPAPER = 5100
    USAGE_SCREENTEXT = 5200
    USAGE_BRANDING = 5300

    USAGES = (USAGE_MAGAZINE, USAGE_NEWSPAPER, USAGE_SCREENTEXT, USAGE_BRANDING)

    # 6000-6999 Intended size of type
    INTENDEDSIZE_EXTRALARGE = 6000
    INTENDEDSIZE_LARGE = 6100
    INTENDEDSIZE_MEDIUM = 6200
    INTENDEDSIZE_SMALL = 6300
    INTENDEDSIZE_EXTRASMALL = 6400

    INTENDEDSIZES = (INTENDEDSIZE_EXTRALARGE, INTENDEDSIZE_LARGE, INTENDEDSIZE_MEDIUM,
        INTENDEDSIZE_SMALL, INTENDEDSIZE_EXTRASMALL
    )
    # 7000-7999 Cases of type
    CASES_MULTICASE = 7100
    CASES_UNICASE = 7200

    CASES = (CASES_MULTICASE, CASES_UNICASE)

        # Language ( English, Spanish, French, German, Swedish, ...)
        # Hinting (XY-BW, XY-GS+CL, Y-CT, Minimal/Auto, ...)
        # Hintingtype (FBHint, Dhint-PT, Dhint-MT, Auto-MTFastPass, Auto-FS, Auto-TTFAutohint, Auto-AdobeFDK, Auto-FL, ...)
        # Character support (asoc Latin, Extended Latin, Greek, Cyrillic, ...)
        # Function (Display, Headline, Subhead, Body, Captions, Agate, ...)
        # Mood (Contemporary, Classical, Delicate, Sturdy, Formal, Casual, Feminine, Masculine, High-tech
        #         Organic, Conservative/Conventional, Expressive/Quirky, Neutral)
        # Availability (Private/Custom, Requested, Print, Web, Apps, E-books, Free?, ...)
        # Foundry

    # The item.filter fields is a text list of these numbers as string
    # with a prefix to mark the unique filter flag, e.g. F1400
    # Then the fast indexed searching/selecting can be done on this unique pattern.
    ITEM_FILTERSET = CATEGORIES + WIDTHS + WEIGHTS + USAGES + INTENDEDSIZES + CASES

    # Possible Status items in of item.status field
    STATUS_MERGE2DELETE = 1150

    STATUS_LABELS = {
        STATUS_MERGE2DELETE: 'Merge+delete'
    }
F = FilterTags
