# -*- coding: UTF-8 -*-
#
#   Main recent data, used by build.py
#
UNITS_PER_EM = 1000
COPYRIGHT = ""
TRADEMARK = ""
LOWEST_PPEM = 5

VERSION_MAJOR = 1
VERSION_MINOR = 0

UFO_PATH = 'ufo/'

class MasterData:
    """Storing additional data about masters, without storing the actual RFont instance. 
    The font can be retrieves by baseAssistant.getMaster(self.path)
    """
    def __init__(self, name=None, ufoPath=UFO_PATH, srcPath=None, orgPath=None, romanItalicPath=None,
            italicAngle=0, rotation=0, 
            kerningSrcPath=None, displaySrcPath=None,
            m0=None, m1=None, m2=None, sm1=None, sm2=None, dsPosition=None,
            tripletData1=None, tripletData2=None, featurePath=None, 
            glyphData=None, metrics=None,
            HStem=None, HThin=None, OStem=None, OThin=None,
            HscStem=None, HscThin=None, OscStem=None, OscThin=None,
            nStem=None, oStem=None, oThin=None, UThin=None, VThin=None, eThin=None,
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

        self.italicSkew = italicAngle
        self.rotation = rotation 
        self.isItalic = bool(italicAngle)
        # Referencing related masters by relative path, handled by the overlay assistant part
        self.srcPath = srcPath # "Original" master of this font, copy from here
        self.displaySrcPath = displaySrcPath # Show this outline on the background
        self.orgPath = orgPath # "Original" master of this font for overlay reference
        self.romanItalicPath = romanItalicPath # Roman <---> Italic master reference
        self.kerningSrcPath = kerningSrcPath # Used as kerning reference.
        # Interpolation & design space
        self.interpolationFactor = 0.5
        self.m0 = m0 # Regular origin
        self.m1 = m1 # Direct interpolation master in "min" side
        self.m2 = m2 # Direct interpolation master on "max" side
        self.sm1 = sm1
        self.sm2 = sm2, # Scalerpolate masters for condensed and extended making. 
        self.dsPosition = dsPosition # Design space position (matching .designspace) to calculate triplet kerning
        self.tripletData1 = tripletData1
        self.tripletData2 = tripletData2, # Compatible triplet sets of (name1, name2, name3, kerning) tuples for interpolation.
        self.featurePath = featurePath
        # Glyphs
        if glyphData is None:
            glyphData = {}
        self.glyphData = glyphData
        if metrics is None:
            metrics = {}
        self.metrics = metrics 
        self.HStem = HStem
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

class GlyphData:
    def __init__(self, f, gName, uni=None):
        self.name = gName
        if gName in f:
            g = f[gName]
            self.uni = g.unicode
        else:
            self.uni = uni 

GD = GlyphData



