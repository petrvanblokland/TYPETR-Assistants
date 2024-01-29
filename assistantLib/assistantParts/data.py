# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   data.py
#
#   Main recent data, used by build.py
#
#   Most common anchor names
#   Anchors with an initial underscore belong in diacritics.
#   In the diacritics cloud and in engines such as Harfbuzz, the anchors are matche with their counter parts
#   on glyph to get their position on top or below.
#   Stacking diacritics can have both, to allow other diacritics floating on top.
#

try:
    from assistantLib.assistantParts.glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_, CAT_CAP_OVERSHOOT, etc.
    from assistantLib.assistantParts.glyphsets.glyphSet import GlyphSet
except ModuleNotFoundError:
    from glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_, CAT_CAP_OVERSHOOT, etc.
    from glyphsets.glyphSet import GlyphSet

_TOP = '_top'
TOP_ = 'top'
_BOTTOM = '_bottom'
BOTTOM_ = 'bottom'
_RING = '_ring'
RING_ = 'ring'
_OGONEK = '_ogonek'
OGONEK_ = 'ogonek'
_VERT = '_vert'
VERT_ = 'vert'
_DOT = '_dot'
DOT_ = 'dot'
_TILDE = '_tilde'
TILDE_ = 'tilde'
_TONOS = '_tonos'
TONOS_ = 'tonos'
_HORN = '_horn'
HORN_ = 'horn'
_MIDDLE = '_middle'
MIDDLE_ = 'middle'

CONNECTED_ANCHORS = {
    _TOP: TOP_,
    _BOTTOM: BOTTOM_,
    _RING: RING_,
    _OGONEK: OGONEK_,
    _VERT: VERT_,
    _DOT: DOT_,
    _TILDE: TILDE_,
    _TONOS: TONOS_, # Also anchor of the other -uc accents
    _HORN: HORN_,
    _MIDDLE: MIDDLE_,
}

class MasterData:
    """Storing additional data about masters, without storing the actual RFont instance. 
    The font can be retrieves by baseAssistant.getMaster(self.path)

    >>> from glyphsets.TYPETR_full_set import TYPETR_GlyphSet 
    >>> glyphSet = TYPETR_GlyphSet()
    >>> md = MasterData(glyphSet=glyphSet)

    """
    # Master data default values
    UNITS_PER_EM = 1000
    COPYRIGHT = ""
    TRADEMARK = ""
    LOWEST_PPEM = 5

    BASELINE = 0
    TAB_WIDTH = 650
    BASE_OVERSHOOT = 12
    ASCENDER = 750
    DESCENDER = -250
    XHEIGHT = 500
    CAPHEIGHT = 750

    VERSION_MAJOR = 1
    VERSION_MINOR = 0

    UFO_PATH = 'ufo/'

    def __init__(self, name=None, ufoPath=None, 
            srcUFOPath=None, someUFOPath=None, orgUFOPath=None, kerningSrcUFOPath=None, romanItalicUFOPath=None, 
            italicAngle=0, italicSkew=None, italicRotation=None, isItalic=False,
            thickness=10, distance=16, # Used for Neon tubes
            m0=None, m1=None, m2=None, sm1=None, sm2=None, dsPosition=None,
            tripletData1=None, tripletData2=None, featurePath=None, 
            # GlyphSet instance, descibing the glyph set and GlyphData characteristics. This attribute must be defined
            glyphSet=None, 
            # Vertical metrics
            baseline=0, baseOvershoot=None, capOvershoot=None, scOvershoot=None, supsOvershoot=None,
            ascender=None, descender=None,
            xHeight=None, capHeight=None, scHeight=None, supsHeight=None,
            baseDiacriticsTop=None, capDiacriticsTop=None, scDiacriticsTop=None, # Baseline of top diacritics
            baseDiacriticsBottom=None, # Top of bottom diacritis
            numrBaseline=None, supsBaseline=None, sinfBaseline=None, dnomBaseline=None, modBaseline=None,
            middlexHeight=None, middleCapHeight=None,
            # Horizontal metrics
            HStem=None, HThin=None, OStem=None, OThin=None,
            HscStem=None, HscThin=None, OscStem=None, OscThin=None,
            nStem=None, oStem=None, oThin=None, UThin=None, VThin=None, eThin=None,
            tabWidth=None,
            ttfPath=None, platformID=None, platEncID=None, langID=None, 
            unitsPerEm=UNITS_PER_EM, copyright=COPYRIGHT, uniqueID=None, trademark=TRADEMARK, 
            lowestRecPPEM=LOWEST_PPEM,
            familyName=None, styleName=None,
            fullName=None, version=None, versionMajor=VERSION_MAJOR, versionMinor=VERSION_MINOR,
            postscriptName=None, preferredFamily=None, preferredSubFamily=None,
            openTypeOS2WinAscent=None, openTypeOS2WinDescent=None,
            openTypeOS2Type=[2, 8], # fsType, TN standard
            vendorURL=None, manufacturerURL=None, manufacturer=None,
            designerURL=None, designer=None, 
            eulaURL=None, eulaDescription=None,
            underlinePosition=None, underlineThickness=None

        ):
        self.name = name
        self.ufoPath = ufoPath or self.UFO_PATH # Ufo file path = self.ufoPath + self.name
        self.familyName = familyName
        self.styleName = styleName

        # Angle, italic skew and rotation
        self.italicAngle = italicAngle or 0
        if italicSkew is None:
            italicSkew = italicAngle * 0.5 # Default, can be overwritten if needed.
        self.italicSkew = italicSkew # In case italicize is partical skew and rotation
        if italicRotation is None:
            italicRotation = italicAngle * 0.5
        self.italicRotation = italicRotation 
        self.isItalic = bool(italicAngle) or isItalic or 'Italic' in name

        # Used by Neon for tube thickness and minimal tube distance
        self.thickness = thickness
        self.distance = distance
        
        # Referencing related masters by relative path, handled by the overlay assistant part
        self.srcUFOPath = srcUFOPath # "Original" master of this font, copy from here
        self.someUFOPath = someUFOPath # Show this outline on the background
        self.orgUFOPath = orgUFOPath # "Original" master of this font for overlay reference
        self.romanItalicUFOPath = romanItalicUFOPath # Roman <---> Italic master reference
        self.kerningSrcUFOPath = kerningSrcUFOPath # Used as kerning reference.
        
        # Interpolation & design space
        self.interpolationFactor = 0.5
        self.m0 = m0 # Regular origin
        self.m1 = m1 # Direct interpolation master in "min" side
        self.m2 = m2 # Direct interpolation master on "max" side
        self.sm1 = sm1
        self.sm2 = sm2, # Scalerpolate masters for condensed and extended making. 
        
        # Design space position (matching .designspace) to calculate triplet kerning.
        # This can be different from HStem (with m1, m2) interpolation.
        self.dsPosition = dsPosition 
        self.tripletData1 = tripletData1
        self.tripletData2 = tripletData2, # Compatible triplet sets of (name1, name2, name3, kerning) tuples for interpolation.
        self.featurePath = featurePath
        
        if tabWidth is None:
            tabWidth = self.DEFAULT_TAB_WIDTH
        self.tabWidth = tabWidth

        # Glyphs
        assert glyphSet is not None
        self.glyphSet = glyphSet
        
        # Vertical metrics. Do some guessing for missing values. 
        # This may not be matching the current font, as we don't have it available as open RFont here.

        if baseOvershoot is None: # Generic overshoot value, specifically for lower case
            baseOvershoot = self.BASE_OVERSHOOT
        self.baseOvershoot = baseOvershoot
        if capOvershoot is None: # Overshoot value for capitals
            capOvershoot = baseOvershoot
        self.capOvershoot = capOvershoot
        if scOvershoot is None: # Overshoot value for smallcaps, mod, etc.
            scOvershoot = baseOvershoot
        self.scOvershoot = scOvershoot
        if supsOvershoot is None: # Overshoot value for sups, numr, sinf and dnom
            supsOvershoot = baseOvershoot
        self.supsOvershoot = supsOvershoot
        
        self.cat2Overshoot = { # Category --> overshoot
            CAT_OVERSHOOT: baseOvershoot,
            CAT_CAP_OVERSHOOT: capOvershoot,
            CAT_SUPS_OVERSHOOT: supsOvershoot,
            CAT_SC_OVERSHOOT: scOvershoot,
        }
        
        if unitsPerEm is None:
            unitsPerEm = self.UNITS_PER_EM
        self.unitsPerEm = unitsPerEm

        if ascender is None:
            ascender = self.ASCENDER
        self.ascender = ascender
        if descender is None:
            descender = self.DESCENDER
        self.descender = descender

        if xHeight is None:
            xHeight = self.XHEIGHT
        self.xHeight = xHeight
        if capHeight is None:
            capHeight = self.CAPHEIGHT
        self.capHeight = capHeight
        if scHeight is None:
            scHeight = xHeight
        self.scHeight = scHeight
        if supsHeight is None:
            supsHeight = xHeight * 2/3
        self.supsHeight = supsHeight

        if middlexHeight is None:
            middlexHeight = xHeight/2,
        self.middlexHeight = middlexHeight        
        if middleCapHeight is None:
            middleCapHeight = capHeight/2
        self.middleCapHeight = middleCapHeight

        self.cat2Height = { # Category --> height
            CAT_XHEIGHT: xHeight,
            CAT_CAP_HEIGHT: capHeight,
            CAT_SC_HEIGHT: scHeight,
            CAT_SUPS_HEIGHT: supsHeight, # Height of .sups, .sinf, .numr, .dnom and mod
        }

        if baseDiacriticsTop is None: # Baseline of top diacritics
            baseDiacriticsTop = xHeight * 1.2
        self.baseDiacriticsTop = baseDiacriticsTop
        if capDiacriticsTop is None:
            capDiacriticsTop = capHeight * 1.1
        self.capDiacriticsTop = capDiacriticsTop
        if baseDiacriticsBottom is None: # Top of bottom diacritis
            baseDiacriticsBottom = -4 * baseOvershoot
        self.baseDiacriticsBottom = baseDiacriticsBottom

        if baseline is None:
            baseline = self.BASELINE
        self.baseline = baseline
        if modBaseline is None:
            modBaseline = xHeight
        self.modBaseline = modBaseline
        if supsBaseline is None:
            supsBaseline = xHeight
        self.supsBaseline = supsBaseline
        if numrBaseline is None: 
            numrBaseline = ascender - supsHeight  
        self.numrBaseline = numrBaseline
        if dnomBaseline is None: 
            dnomBaseline = baseline  
        self.dnomBaseline = dnomBaseline
        if sinfBaseline is None: 
            sinfBaseline = descender  
        self.sinfBaseline = sinfBaseline

        self.cat2Baseline = {
            CAT_BASELINE: baseline,
            CAT_MOD_BASELINE: modBaseline,
            CAT_NUMR_BASELINE: numrBaseline,
            CAT_SINF_BASELINE: sinfBaseline,
            CAT_SUPS_BASELINE: supsBaseline,
            CAT_DNOM_BASELINE: dnomBaseline ,
        }

        # Horizontal metrics
        self.HStem = HStem # Used for m1->m2 interpolation
        self.HThin = HThin
        self.OStem = OStem
        self.OThin = OThin
        self.HscStem = HscStem
        self.HscThin = HscStem
        self.OscStem = OscStem
        self.OscThin = OscThin
        self.nStem = nStem
        self.oStem = oStem
        self.oThin = oThin
        self.UThin = UThin
        self.VThin = VThin
        self.eThin = eThin

        # Info
        self.ttfPath = ttfPath
        self.platformID = platformID
        self.platEncID = platEncID
        self.langID = platEncID, 
        self.unitsPerEm = unitsPerEm
        self.copyright = copyright
        self.uniqueID = uniqueID 
        self.trademark = trademark
        self.lowestRecPPEM = lowestRecPPEM

        self.fullName = fullName

        #version=None, versionMajor=VERSION_MAJOR, versionMinor=VERSION_MINOR,
        #postscriptName=None, preferredFamily=None, preferredSubFamily=None,
        #openTypeOS2WinAscent=OS2_WIN_ASCENT, openTypeOS2WinDescent=OS2_WIN_DESCENT,
        #openTypeOS2Type=[2, 8], # fsType, TN standard
        #vendorURL=VENDOR_URL, manufacturerURL=MANUFACTURER_URL, manufacturer=MANUFACTURER,
        #designerURL=DESIGNER_URL, designer=DESIGNER, 
        #eulaURL=EULA_URL, eulaDescription=EULA_DESCRIPTION,
        #underlinePosition=None, underlineThickness=UNDERLINE_THICKNESS

    def getOvershoot(self, gName):
        """Answer the overshoot for this glyph based on the settings of the related GlyphData and otherwise guessing on its name."""
        gd = self.glyphSet.get(gName)
        if gd is None:
            print(f'### getOvershoot: Unknown glyph /{gName} in glyphSet of {self.name}')
            return self.baseOvershoot
        if gd.overshoot is not None: # If there a hard coded value, then answer it
            return gd.overshoot
        # If there is a category defined in the glyphData for this glyph, then answer the referenced category value.
        if gd.catOvershoot is not None:
            return self.cat2Overshoot[gd.catOvershoot]
        # Not defined in the GlyphSet/GlyphData for this glyph. We need to do some quessing, based on the name.
        if gd.isUpper: # All glyph that start with initial cap
            return self.cat2Overshoot[CAT_CAP_OVERSHOOT]
        if gd.isMod: # One of sups, sinf, dnom, numr, mod in the name
            return self.cat2Overshoot[CAT_SUPS_OVERSHOOT]
        if gd.isSc: # One of .sc, small in the name
            return self.cat2Overshoot[CAT_SC_OVERSHOOT]
        # Otherwise answer the default overshoot. 
        return self.baseOvershoot

    def getBaseline(self, gName):
        """Answer the baseline position for this glyph based on the settings of the related GlyphData and otherwise guessing on its name."""
        gd = self.glyphSet.get(gName)
        if gd is None:
            print(f'### getBaseline: Unknown glyph /{gName} in glyphSet of {self.name}')
            return self.BASELINE
        if gd.baseline is not None: # If there a hard coded value, then answer it
            return gd.baseline
        # If there is a category defined in the glyphData for this glyph, then answer the referenced category value.
        if gd.catBaseline is not None:
            return self.cat2Baseline[gd.catBaseline]
        # Not defined in the GlyphSet/GlyphData for this glyph. We need to do some quessing, based on the type of glyph or its name.
        if gd.isMod:
            return self.modBaseline
        if gd.isSups:
            return self.supsBaseline
        if gd.isNumr:
            return self.numrBaseline
        if gd.isSinf:
            return self.sinfBaseline
        if gd.isDnom:
            return self.dnomBaseline
        return self.BASELINE

    def getHeight(self, gName):
        """Answer the height for this glyph based on the settings of the related GlyphData and otherwise guessing on its name."""
        gd = self.glyphSet.get(gName)
        if gd is None:
            print(f'### getHeight: Unknown glyph /{gName} in glyphSet of {self.name}')
            return self.capHeight
        if gd.height is not None: # If there a hard coded value, then answer it
            return gd.height
        # If there is a category defined in the glyphData for this glyph, then answer the referenced category value.
        # Smallcaps
        if gd.isSc:
            return self.cat2Height[gd.scHeight]
        # Not defined in the GlyphSet/GlyphData for this glyph. We need to do some quessing, based on the type of glyph or its name.
        if gd.isMod or gd.isSups or gd.isNumr or gd.isSinf or gd.isDnom:
            return self.supsHeight
        if gd.isLower:
            return self.xHeight
        return self.capHeight

    def getMiddleHeight(self, gName):
        """Answer the rounded half of height."""
        return int(round(self.getHeight(gName)/2))
        
MD = MasterData



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])




