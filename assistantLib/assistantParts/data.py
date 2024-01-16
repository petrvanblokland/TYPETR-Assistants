# -*- coding: UTF-8 -*-
#
#   Main recent data, used by build.py
#
class MasterData:
    """Storing additional data about masters, without storing the actual RFont instance. 
    The font can be retrieves by baseAssistant.getMaster(self.path)
    """
    def __init__(self, f, srcPath=None, orgPath=None, romanItalicPath=None,
            kerningSrcPath=None, displaySrcPath=None,
            m0=None, m1=None, m2=None, sm1=None, sm2=None, dsPosition=None,
            tripletData1=None, tripletData2=None, featurePath=None, 
            glyphData=None, metrics=None,
            HStem=None, HThin=None, OStem=None, OThin=None,
            HscStem=None, HscThin=None, OscStem=None, OscThin=None,
            nStem=None, oStem=None, oThin=None, UThin=None, VThin=None, eThin=None,
                    self.ttfPath=None
        self.platformID=None, platEncID=None, langID=None, 
        unitsPerEm=UNITS_PER_EM,
        copyright=COPYRIGHT, uniqueID=None, trademark=TRADEMARK, lowestRecPPEM=LOWEST_PPEM,
        familyName=None, styleName=None,
        fullName=None, version=None, versionMajor=VERSION_MAJOR, versionMinor=VERSION_MINOR,
        postscriptName=None, preferredFamily=None, preferredSubFamily=None,
        openTypeOS2WinAscent=OS2_WIN_ASCENT, openTypeOS2WinDescent=OS2_WIN_DESCENT,
        openTypeOS2Type=[2, 8], # fsType, TN standard
        vendorURL=VENDOR_URL, manufacturerURL=MANUFACTURER_URL, manufacturer=MANUFACTURER,
        designerURL=DESIGNER_URL, designer=DESIGNER, 
        eulaURL=EULA_URL, eulaDescription=EULA_DESCRIPTION,
        underlinePosition=None, underlineThickness=UNDERLINE_THICKNESS

        ):
        self.path = f.path
        self.italicSkew = f.info.italicAngle
        self.rotation = radians(f.info.italicAngle) 
        self.isItalic = bool(f.info.italicAngle)
        # Referencing related masters by relative path
        self.srcPath = srcPath # "Original" master of this font, copy from here
        self.orgPath = orgPath # "Original" master of this font
        self.romanItalicPath = romanItalicPath # Roman <---> Italic master reference
        self.kerningSrcPath = kerningSrcPath 
        self.displaySrcPath = displaySrcPath # Show this outline on the background
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
        self.ttfPath=None
        self.platformID=None, platEncID=None, langID=None, 
        unitsPerEm=UNITS_PER_EM,
        copyright=COPYRIGHT, uniqueID=None, trademark=TRADEMARK, lowestRecPPEM=LOWEST_PPEM,
        familyName=None, styleName=None,
        fullName=None, version=None, versionMajor=VERSION_MAJOR, versionMinor=VERSION_MINOR,
        postscriptName=None, preferredFamily=None, preferredSubFamily=None,
        openTypeOS2WinAscent=OS2_WIN_ASCENT, openTypeOS2WinDescent=OS2_WIN_DESCENT,
        openTypeOS2Type=[2, 8], # fsType, TN standard
        vendorURL=VENDOR_URL, manufacturerURL=MANUFACTURER_URL, manufacturer=MANUFACTURER,
        designerURL=DESIGNER_URL, designer=DESIGNER, 
        eulaURL=EULA_URL, eulaDescription=EULA_DESCRIPTION,
        underlinePosition=None, underlineThickness=UNDERLINE_THICKNESS

class GlyphData:
    def __init__(self, f, gName):
        self.name = gName
