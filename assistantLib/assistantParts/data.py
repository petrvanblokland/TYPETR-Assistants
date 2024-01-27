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

# Master data default values
UNITS_PER_EM = 1000
COPYRIGHT = ""
TRADEMARK = ""
LOWEST_PPEM = 5

DEFAULT_TAB_WIDTH = 650
DEFAULT_OVERSHOOT = 12

VERSION_MAJOR = 1
VERSION_MINOR = 0

UFO_PATH = 'ufo/'

class MasterData:
    """Storing additional data about masters, without storing the actual RFont instance. 
    The font can be retrieves by baseAssistant.getMaster(self.path)
    """
    def __init__(self, name=None, ufoPath=UFO_PATH, 
            srcUFOPath=None, someUFOPath=None, orgUFOPath=None, kerningSrcUFOPath=None, romanItalicUFOPath=None, 
            italicAngle=0, italicSkew=None, italicRotation=None, isItalic=False,
            thickness=10, distance=16, # Used for Neon tubes
            m0=None, m1=None, m2=None, sm1=None, sm2=None, dsPosition=None,
            tripletData1=None, tripletData2=None, featurePath=None, 
            glyphData=None, 
            # Vertical metrics
            baseline=0, overshoot=None, capOvershoot=None, scOvershoot=None, supsOvershoot=None,
            xHeight=None, capHeight=None, scHeight=None, supsHeight=None,
            diacriticsTop=None, capDiacriticsTop=None, scDiacriticsTop=None, # Baseline of top diacritics
            diacticicsBottom=None, # Top of bottom diacritis
            numrBaseline=None, supsBaseline=None, sinfBaseline=None, dnomBaseline=None,
            middlexHeight=None, middleCapHeight=None,
            # Horizontal metrics
            HStem=None, HThin=None, OStem=None, OThin=None,
            HscStem=None, HscThin=None, OscStem=None, OscThin=None,
            nStem=None, oStem=None, oThin=None, UThin=None, VThin=None, eThin=None,
            tabWidth=DEFAULT_TAB_WIDTH,
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
        self.ufoPath = ufoPath # Ufo file path = self.ufoPath + self.name
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
        self.overshoot = overshoot # For generic use /O. Also used by the Neon for the size of the inner gap circle marker
        
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
        
        self.tabWidth = tabWidth

        # Glyphs
        if glyphData is None:
            glyphData = {}
        self.glyphData = glyphData
        
        # Vertical metrics. Do some guessing for missing values. 
        # This may not be matching the current font, as we don't have it available as open RFont here.

        if baseline is None:
            baseline = 0
        self.baseline = baseline

        if overshoot is None: # Generic overshoot, specifically for lower case
            overshoot = self.DEFAULT_OVERSHOOT
        self.overshoot = overshoot
        if capOvershoot is None: # Overshoot for capitals
            capOvershoot = overshoot
        self.capOvershoot = capOvershoot
        if scOvershoot is None: # Overshoot for smallcaps, mod, etc.
            scOvershoot = overshoot
        self.scOvershoot = scOvershoot
        if supsOvershoot is None: # Overshoot for sups, numr, sinf and dnom
            supsOvershoot = overshoot
        self.supsOvershoot = supsOvershoot

        if unitsPerEm is None:
            unitsPerEm = DEFAILT_UNITS_PER_EM
        self.unitsPerEm = unitsPerEm
        if ascender is None:
            ascender = DEFAULT_ASCENDER
        self.ascender = ascender
        if descender is None:
            descender = DEFAULT_DESCENDER
        self.descender = descender
        if xHeight is None:
            xHeight = DEFAULT_XHEIGHT
        self.xHeight = xHeight
        if capHeight is None:
            capHeight = DEFAULT_CAPHEIGHT
        self.capHeight = capHeight
        if scHeight is None:
            scHeight = xHeight * 1.1
        self.scHeight = scHeight
        if middlexHeight is None:
            middlexHeight = xHeight/2,
        self.middlexHeight = middlexHeight        
        if middleCapHeight is None:
            middleCapHeight = capHeight/2
        self.middleCapHeight = middleCapHeight

        if diacriticsTop is None: # Baseline of top diacritics
            diacriticsTop = xheight * 1.2
        self.diacriticsTop = diacriticsTop
        if capDiacriticsTop is None:
            capDiacriticsTop = capHeight * 1.1
        self.capDiacriticsTop = capDiacriticsTop
        if diacriticsBottom is None: # Top of bottom diacritis
            diacriticsBottom = -4 * overshoot
        self.diacriticsBottom = diacriticsBottom

        if supsHeight is None:
            supsHeight = xHeight * 2/3
        self.supsHeight = supsHeight
        if supsBaseline is None:
            supsBaseline = xHeight
        self.supsBaseline =supsBaseline
        if numrBaseline is None: 
            numrBaseline = ascender - supsHeight  
        self.numrBaseline = numrBaseline
        if dnomBaseline is None: 
            dnomBaseline = baseline  
        self.dnomBaseline = dnomBaseline
        if sinfBaseline is None: 
            sinfBaseline = descender  
        self.sinfBaseline = sinfBaseline

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

MD = MasterData





