# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   packdefinitions.py
#
def _formatType(tp):
    if tp is None or tp is type(None):
        return "None"
    else:
        return tp.__name__


def checkPack(pack, definitions):
    """Check a pack against its definition. Return a list of error strings.

        >>> pack = dict(familyName="TestFont", compatibleFullName="TestFont", copyright="Mine.",
        ...             styleName="Bold",
        ...             license="Yes.", trademark="TM", familyClass=0, manufacturerName="FBI",
        ...             os2Selection={}, panose={})
        >>> checkPack(pack, IDENTIFIERS)
        []
        >>> pack = dict(familyName="TestFont", compatibleFullName="TestFont", copyright="Mine.",
        ...             styleName="Bold",
        ...             license="Yes.", trademark="TM", familyClass=0, manufacturerName="FBI",
        ...             os2Selection={})
        >>> checkPack(pack, IDENTIFIERS)
        ["Missing required field: 'panose'"]
        >>> pack = dict(familyName=0, compatibleFullName="TestFont", copyright="Mine.",
        ...             styleName="Bold",
        ...             license="Yes.", trademark="TM", familyClass=0, manufacturerName="FBI",
        ...             os2Selection={}, panose={})
        >>> checkPack(pack, IDENTIFIERS)
        ["Type mismatch for 'familyName'; expected str, got int"]
        >>> pack = dict(familyName="TestFont", compatibleFullName="TestFont", copyright="Mine.",
        ...             styleName="Bold",
        ...             license="Yes.", trademark="TM", familyClass=0, manufacturerName="FBI",
        ...             os2Selection={}, panose={}, manufacturerUrl=123)
        >>> checkPack(pack, IDENTIFIERS)
        ["Type mismatch for 'manufacturerUrl'; expected str or None, got int"]
        >>> pack = dict(familyName="TestFont", compatibleFullName="TestFont", copyright="Mine.",
        ...             styleName="Bold",
        ...             license="Yes.", trademark="TM", familyClass=0, manufacturerName="FBI",
        ...             os2Selection={}, panose={}, doesNotExist=123)
        >>> checkPack(pack, IDENTIFIERS)
        ["Found undefined field: 'doesNotExist'"]
        >>> pack = dict(familyName=123, compatibleFullName="TestFont", copyright="Mine.",
        ...             styleName="Bold",
        ...             license="Yes.", trademark="TM", familyClass=0, manufacturerName="FBI",
        ...             os2Selection={})
        >>> checkPack(pack, IDENTIFIERS)
        ["Type mismatch for 'familyName'; expected str, got int", "Missing required field: 'panose'"]
    """
    errors = []
    for key in sorted(definitions):
        types = definitions[key]
        if key not in pack:
            if None not in types:
                # it's a required field
                errors.append("Missing required field: %r" % key)
        else:
            value = pack[key]
            typeOk = True
            for tp in types:
                if tp is None:
                    if value is None:
                        break
                elif isinstance(value, tp):
                    break
            else:
                typeOk = False
            if not typeOk:
                foundTypeName = _formatType(type(value))
                typeNames = [_formatType(tp) for tp in types]
                typeNames = " or ".join(typeNames)
                errors.append("Type mismatch for %r; expected %s, got %s" % (key, typeNames, foundTypeName))
    for key in sorted(pack):
        if key not in definitions:
            errors.append("Found undefined field: %r" % key)
    return errors


os2SelectionFields = [
    "italic",
    "underscore",
    "negative",
    "outlines",
    "strikeout",
    "bold",
    "regular",
    "useTypoMetrics",
    "wws",
    "oblique",
]


"""

Generic Identification

* :attr:`~defcon.Info.familyName`
* :attr:`~defcon.Info.styleName`
* :attr:`~defcon.Info.styleMapFamilyName`
* :attr:`~defcon.Info.styleMapStyleName`
* :attr:`~defcon.Info.versionMajor`
* :attr:`~defcon.Info.versionMinor`
* :attr:`~defcon.Info.year`

Generic Legal
"""""""""""""

* :attr:`~defcon.Info.copyright`
* :attr:`~defcon.Info.trademark`

Generic Dimensions
""""""""""""""""""

* :attr:`~defcon.Info.unitsPerEm`
* :attr:`~defcon.Info.descender`
* :attr:`~defcon.Info.xHeight`
* :attr:`~defcon.Info.capHeight`
* :attr:`~defcon.Info.ascender`
* :attr:`~defcon.Info.italicAngle`

Generic Miscellaneous

* :attr:`~defcon.Info.note`

OpenType head Table
"""""""""""""""""""

* :attr:`~defcon.Info.openTypeHeadCreated`
* :attr:`~defcon.Info.openTypeHeadLowestRecPPEM`
* :attr:`~defcon.Info.openTypeHeadFlags`

OpenType hhea Table
"""""""""""""""""""

* :attr:`~defcon.Info.openTypeHheaAscender`
* :attr:`~defcon.Info.openTypeHheaDescender`
* :attr:`~defcon.Info.openTypeHheaLineGap`
* :attr:`~defcon.Info.openTypeHheaCaretSlopeRise`
* :attr:`~defcon.Info.openTypeHheaCaretSlopeRun`
* :attr:`~defcon.Info.openTypeHheaCaretOffset`

OpenType name Table
"""""""""""""""""""

* :attr:`~defcon.Info.openTypeNameDesigner`
* :attr:`~defcon.Info.openTypeNameDesignerURL`
* :attr:`~defcon.Info.openTypeNameManufacturer`
* :attr:`~defcon.Info.openTypeNameManufacturerURL`
* :attr:`~defcon.Info.openTypeNameLicense`
* :attr:`~defcon.Info.openTypeNameLicenseURL`
* :attr:`~defcon.Info.openTypeNameVersion`
* :attr:`~defcon.Info.openTypeNameUniqueID`
* :attr:`~defcon.Info.openTypeNameDescription`
* :attr:`~defcon.Info.openTypeNamePreferredFamilyName`
* :attr:`~defcon.Info.openTypeNamePreferredSubfamilyName`
* :attr:`~defcon.Info.openTypeNameCompatibleFullName`
* :attr:`~defcon.Info.openTypeNameSampleText`
* :attr:`~defcon.Info.openTypeNameWWSFamilyName`
* :attr:`~defcon.Info.openTypeNameWWSSubfamilyName`


OpenType OS/2 Table

* :attr:`~defcon.Info.openTypeOS2WidthClass`
* :attr:`~defcon.Info.openTypeOS2WeightClass`
* :attr:`~defcon.Info.openTypeOS2Selection`
* :attr:`~defcon.Info.openTypeOS2VendorID`
* :attr:`~defcon.Info.openTypeOS2Panose`
* :attr:`~defcon.Info.openTypeOS2FamilyClass`
* :attr:`~defcon.Info.openTypeOS2UnicodeRanges`
* :attr:`~defcon.Info.openTypeOS2CodePageRanges`
* :attr:`~defcon.Info.openTypeOS2TypoAscender`
* :attr:`~defcon.Info.openTypeOS2TypoDescender`
* :attr:`~defcon.Info.openTypeOS2TypoLineGap`
* :attr:`~defcon.Info.openTypeOS2WinAscent`
* :attr:`~defcon.Info.openTypeOS2WinDescent`
* :attr:`~defcon.Info.openTypeOS2Type`
* :attr:`~defcon.Info.openTypeOS2SubscriptXSize`
* :attr:`~defcon.Info.openTypeOS2SubscriptYSize`
* :attr:`~defcon.Info.openTypeOS2SubscriptXOffset`
* :attr:`~defcon.Info.openTypeOS2SubscriptYOffset`
* :attr:`~defcon.Info.openTypeOS2SuperscriptXSize`
* :attr:`~defcon.Info.openTypeOS2SuperscriptYSize`
* :attr:`~defcon.Info.openTypeOS2SuperscriptXOffset`
* :attr:`~defcon.Info.openTypeOS2SuperscriptYOffset`
* :attr:`~defcon.Info.openTypeOS2StrikeoutSize`
* :attr:`~defcon.Info.openTypeOS2StrikeoutPosition`
* :attr:`~defcon.Info.openTypeVheaVertTypoAscender`
* :attr:`~defcon.Info.openTypeVheaVertTypoDescender`
* :attr:`~defcon.Info.openTypeVheaVertTypoLineGap`
* :attr:`~defcon.Info.openTypeVheaCaretSlopeRise`
* :attr:`~defcon.Info.openTypeVheaCaretSlopeRun`
* :attr:`~defcon.Info.openTypeVheaCaretOffset`

Postscript

* :attr:`~defcon.Info.postscriptFontName`
* :attr:`~defcon.Info.postscriptFullName`
* :attr:`~defcon.Info.postscriptSlantAngle`
* :attr:`~defcon.Info.postscriptUniqueID`
* :attr:`~defcon.Info.postscriptUnderlineThickness`
* :attr:`~defcon.Info.postscriptUnderlinePosition`
* :attr:`~defcon.Info.postscriptIsFixedPitch`
* :attr:`~defcon.Info.postscriptBlueValues`
* :attr:`~defcon.Info.postscriptOtherBlues`
* :attr:`~defcon.Info.postscriptFamilyBlues`
* :attr:`~defcon.Info.postscriptFamilyOtherBlues`
* :attr:`~defcon.Info.postscriptStemSnapH`
* :attr:`~defcon.Info.postscriptStemSnapV`
* :attr:`~defcon.Info.postscriptBlueFuzz`
* :attr:`~defcon.Info.postscriptBlueShift`
* :attr:`~defcon.Info.postscriptBlueScale`
* :attr:`~defcon.Info.postscriptForceBold`
* :attr:`~defcon.Info.postscriptDefaultWidthX`
* :attr:`~defcon.Info.postscriptNominalWidthX`
* :attr:`~defcon.Info.postscriptWeightName`
* :attr:`~defcon.Info.postscriptDefaultCharacter`
* :attr:`~defcon.Info.postscriptWindowsCharacterSet`

Macintosh FOND Resource

* :attr:`~defcon.Info.macintoshFONDFamilyID`
* :attr:`~defcon.Info.macintoshFONDName`
"""

EMPTY = None

INFODICT = dict(
    # Superset of font.info, name table, OS/2 table, etc.
    # TODO: Copy names identical from RoboFont.info instead of cleaned names.

    familyName                  =  (str,),       # Family name must be filled.
    styleName                   =  (str,),       # Style name must be filled.
    # postscriptFullName ??
    compatibleFullName          =  (str, EMPTY), # openTypeNameCompatibleFullName
    manufacturerName            =  (str, EMPTY), # openTypeNameManufacturer
    manufacturerUrl             =  (str, EMPTY), # openTypeNameManufacturerURL
    vendorID                    =  (str, EMPTY), # openTypeOS2VendorID
    designerName                =  (str, EMPTY), # openTypeNameDesigner
    designerUrl                 =  (str, EMPTY), # openTypeNameDesignerURL
    copyright                   =  (str, EMPTY),
    note                        =  (str, EMPTY),
    trademark                   =  (str, EMPTY),
    license                     =  (str, EMPTY), # openTypeNameLicense
    licenseUrl                  =  (str, EMPTY), # openTypeNameLicenseURL
    description                 =  (str, EMPTY), # openTypeNameDescription
    sampleText                  =  (str, EMPTY), # openTypeNameSampleText
#    created                     =  (str, int,),  # openTypeHeadCreated
#    modified                    =  (str, int,),
    panose                      =  (dict,),             # openTypeOS2Panose'
    familyClass                 =  (int,),              # openTypeOS2FamilyClass
    os2Selection                =  (dict,),             # openTypeOS2Selection

    unitsPerEm                  =  (int,),
    xHeight                     =  (int,),
    ascender                    =  (int,),
    descender                   =  (int,),              # descent, openTypeHheaDescender
    winAscender                 =  (int,),              # openTypeOS2WinAscent or idential to ascender
    winDescender                =  (int,),              # openTypeOS2WinDescent or identical to descender
    typoAscender                =  (int,),              # openTypeOS2TypoAscender or identical to ascender
    typoDescender               =  (int,),              # openTypeOS2TypoDescender or identical to descender
    capHeight                   =  (int,),
    minPPEM                     =  (int,),              # openTypeHeadLowestRecPPEM
    lineGap                     =  (int,),              # openTypeHheaLineGap
    typoLineGap                 =  (int,),              # openTypeOS2TypoLineGap or identical to lineGap
    italicAngle                 =  (float, int,),       # postscriptSlantAngle,
    underlinePosition           =  (int,),              # postscriptUnderlinePosition
    underlineThickness          =  (int,),              # postscriptUnderlineThickness
    isFixedPitch                =  (int, bool),         # postscriptIsFixedPitch
    horizontalCaretOffset       =  (int,),              # openTypeHheaCaretOffset
    horizontalCaretSlopeRise    =  (int,),              # openTypeHheaCaretSlopeRise
    horizontalCaretSlopeRun     =  (int,),              # openTypeHheaCaretSlopeRun
    verticalCaretOffset         =  (int, EMPTY),        # openTypeVheaCaretOffset
    verticalCaretSlopeRise      =  (int, EMPTY),        # openTypeVheaCaretSlopeRise
    verticalCaretSlopeRun       =  (int, EMPTY),        # openTypeVheaCaretSlopeRun
    subscriptXOffset            =  (int,),              # openTypeOS2SubscriptXOffset
    subscriptXSize              =  (int,),              # openTypeOS2SubscriptXSize
    subscriptYOffset            =  (int,),              # openTypeOS2SubscriptYOffset
    subscriptYSize              =  (int,),              # openTypeOS2SubscriptYSize
    superscriptXOffset          =  (int,),              # openTypeOS2SuperscriptXOffset
    superscriptXSize            =  (int,),              # openTypeOS2SuperscriptXSize
    superscriptYOffset          =  (int,),              # openTypeOS2SuperscriptYOffset
    superscriptYSize            =  (int,),              # openTypeOS2SuperscriptYSize
    strikeoutSize               =  (int,),              # openTypeOS2StrikeoutSize
    strikeoutPosition           =  (int,),              # openTypeOS2StrikeoutPosition
    widthClass                  =  (int,),              # openTypeOS2WidthClass
    weightClass                 =  (int,),              # openTypeOS2WeightClass
    averageWidth                =  (int,),              # avgCharWidth  XXX calculated value, analyzers?

    # These are mostly (but not all) TT-specific and will be calculated upon compile.
    # Question is if they should be stored.

    maxComponentDepth           =  (int,),
    maxComponentElements        =  (int,),
    maxCompositeContours        =  (int,),
    maxCompositePoints          =  (int,),
    maxContours                 =  (int,),
    maxFunctionDefs             =  (int,),
    maxInstructionDefs          =  (int,),
    maxPoints                   =  (int,),
    maxSizeOfInstructions       =  (int,),
    maxStackElements            =  (int,),
    maxStorage                  =  (int,),
    maxTwilightPoints           =  (int,),
    maxZones                    =  (int,),
    maxX                        =  (int,),
    maxY                        =  (int,),
    minX                        =  (int,),
    minY                        =  (int,),
    numGlyphs                   =  (int,),
    # GASP
    gaspRange                   =  (dict,),
    # HHEA
    advanceWidthMax             =  (int,),
    minLeftSideBearing          =  (int,),
    minRightSideBearing         =  (int,),
    maxExtent                   =  (int,),
    # OS/2
    maxContext                  =  (int,),
)

"""

    # Pack: features
    # Includes TTF.GSUB
    PACK_FEATURES:dict(
        packType=(str,),
        features=(dict, EMPTY),
    ),
    # Pack: kerning
    # Includes TTF.KERN, TTF.GPOS
    PACK_POSITIONS:dict(
        packType=(str,),
        kernings=(list, tuple, EMPTY), # List of [kern] dictionaries
        positions=(dict, EMPTY),
    ),
    # Pack: hints
    # Includes TTF.FPGM, TTF.PREP OR OTF.CFF blue values.
    PACK_HINTS:dict(
        packType=(str,),
        fpgm=(str, None), # Optional source of fpgm
        prep=(str, None), # Optional source of prep
    ),
    # Pack: glyphs
    # Includes TTF.GLYF, TTF.CMAP
    PACK_GLYPHS:dict(
        packType=(str,),
        cmaps=(tuple, list), # List of cmaps. Should at least contain one cmap list.
        codePageRanges=(tuple, list), # ulCodePageRange1, ulCodePageRange2
        unicodeRanges=(tuple, list), # ulUnicodeRange1, ulUnicodeRange2, ulUnicodeRange3, ulUnicodeRange4
        breakChar=(int,), # os_2Table table usBreakChar
        defaultChar=(int,), # os_2Table table usDefaultChar
        floqMemes=(dict,), # Meme descriptions per glyph. Key is the glyph unicode name.
    ),
    # Pack: adapters
    # Data specific for an adapter. Key is Adapter.AID. Includes UFO.lib, UFO.xml
    PACK_ADAPTERS:dict(
        packType=(str,),
        sourceAdapterAid=(str,),
        ttf=(dict(
            os_2Selection=(dict,), # openTypeOS2Selection
        )),
        ufo=(dict(

        )),
    ),
})

"""


def _runDocTests():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _runDocTests()
