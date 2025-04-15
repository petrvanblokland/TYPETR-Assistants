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
import importlib

from assistantLib.assistantParts.glyphsets.glyphData import * 
from assistantLib.assistantParts.glyphsets.glyphSet import GlyphSet
import assistantLib.assistantParts.glyphsets.anchorData
importlib.reload(assistantLib.assistantParts.glyphsets.anchorData)
from assistantLib.assistantParts.glyphsets.anchorData import AD
from assistantLib.assistantParts.glyphsets.Latin_L_set import LATIN_L_SET

class MasterData:
    """Storing additional data about masters, without storing the actual RFont instance. 
    The font can be retrieves by baseAssistant.getMaster(self.path)

    >>> # Doctesting is done via more global docTestAssistants.py

    """
    # Master data default values
    UNITS_PER_EM = 1000
    COPYRIGHT = ""
    TRADEMARK = ""
    LOWEST_PPEM = 5

    BASELINE = 0
    BASE_OVERSHOOT = 12
    STEM_OVERSHOOT = 0 # Used for small  dovershoot if single stems, e.g. in rounded terminals such as Upgrade Neon
    ASCENDER = 750
    DESCENDER = -250
    XHEIGHT = 500
    CAPHEIGHT = 750
    
    VERSION_MAJOR = 1
    VERSION_MINOR = 0

    UFO_PATH = 'ufo/'

    def __init__(self, name=None, ufoPath=None, 
            srcUFOPath=None, someUFOPath=None, orgUFOPath=None, 
            groupSrcUFOPath=None, # Optioncal copy groups from here, otherwise use orgUFOPath
            kerningSrcUFOPath=None, # Optional copy kerning from here, otherwise use orgUFOPath
            romanItalicUFOPath=None, # Path of corresponding master for roman <--> italic
            spacingSrcUFOPath=None, # If defined, used as spacing reference, overwriting all spacing rules. Goes with spacingOffset
            spacingOffset=0, # Value to add to margins of self.spacingSrcUFOPath (if defined)
            italicAngle=0, italicSkew=None, italicRotation=None, isItalic=False,
            dsPosition=None,
            m0=None, # Origin of the design space
            m1=None, m2=None, # Used for interpolating spacing, outlines, anchor positions, component positions
            m3=None, # Rsource for interpolation "Copy" button"
            sm1=None, sm2=None, # Scalerpolate masters for condensed and extended making
            osm1=None, osm2=None, # Previous and next master on the same optical size level
            tripletData1=None, tripletData2=None, featurePath=None, 
            # GlyphSet instance, describing the glyph set and GlyphData characteristics. This attribute must be defined
            glyphSet=None, 
            # Spacing category rules
            spaceWidth=None,
            emWidth=None,
            emWidth2=None,
            enWidth=None,
            hairWidth=None,
            accentWidth=None,
            tabWidth=None,
            figureWidth=None,
            mathWidth=None,
            fractionWidth=None,
            # Margins
            centerWidth=None,
            minMargin=None,
            modMinMargin=None,
            # Vertical metrics
            unitsPerEm=UNITS_PER_EM, 
            baseline=0, stemOvershoot=STEM_OVERSHOOT, baseOvershoot=None, capOvershoot=None, 
                scOvershoot=None, onumOvershoot=None, superiorOvershoot=None,
                diacriticsOvershoot=None,
            ascender=None, descender=None,
            xHeight=None, capHeight=None, scHeight=None, onumHeight=None, 
            superiorHeight=None, superiorCapHeight=None, superiorAscender=None, superiorDescender=None,
            modHeight=None,
            numrBaseline=None, supsBaseline=None, sinfBaseline=None, dnomBaseline=None, modBaseline=None,
            middlexHeight=None, middleCapHeight=None,
            
            # Vertical anchor offsets to avoid collission with baseline, guidelines, etc. in mouse selection
            #topAnchorYSelectionOffset=0, bottomAnchorYSelectionOffset=0, # Offset placement of top/bottom anchors, for better manual selection
            #capStackedDiacriticsVKerning=None, # Offset for stacked diacritics on capitals
            #stackedDiacriticsVKerning=None, # Offset for stacked diacritics
            baseDiacriticsTop=None, capDiacriticsTop=None, scDiacriticsTop=None, # Baseline of top diacritics
            baseDiacriticsBottom=None, # Top of bottom diacritis
            ascenderAnchorOffsetY= -AD.ANCHOR_ASCENDER_OFFSET,
            boxTopAnchorOffsetY= -AD.ANCHOR_BOXTOP_OFFSET,
            capHeightAnchorOffsetY= -AD.ANCHOR_CAP_OFFSET, # Optional vertical offset of cap-anchors or lower capital diacritics.
            xHeightAnchorOffsetY= -AD.ANCHOR_OFFSET, 
            baselineAnchorOffsetY=AD.ANCHOR_OFFSET,
            ogonekAnchorOffsetY=AD.ANCHOR_OGONEK_OFFSET,
            boxBottomAnchorOffsetY= AD.ANCHOR_BOXBOTTOM_OFFSET,
            descenderAnchorOffsetY=AD.ANCHOR_DESCENDER_OFFSET,
            
            # Horizontal metrics
            diagonalTolerance=0, # ± Tolerance for italic diagonals to be marked as off-limit
            HStem=None, HThin=None, OStem=None, OThin=None,
            HscStem=None, HscThin=None, OscStem=None, OscThin=None,
            nStem=None, oStem=None, oThin=None, UThin=None, VThin=None, eThin=None,
            modStem=None, # Used for special factor to interpolate/extrapolate "mod" glyphs, e.g. extrapolating Black from Regular + Bold
            thickness=10, distance=16, # Used for Neon tubes, can be overwritten from GlyphData.thickness
            iFactor=None, 
            superiorIFactorX=None, superiorIFactorY=None, scIFactor=None,
            superiorOutline=None, # Used for scalarpolation of superiors
            superiorWidthFactor=1, # Additional horizontal scaling factor of superiors.
            scIFactorX=None, scIFactorY=None, 
            scOutline=None, # Used for scalarpolations of .sc
            scWidthFactor=1, # Additional horizontal scaling factor of .sc
            # Table stuff
            ttfPath=None, platformID=None, platEncID=None, langID=None, 
            copyright=COPYRIGHT, uniqueID=None, trademark=TRADEMARK, 
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
        if name is None:
            name = 'Untitled'
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

        # Used by Neon for tube thickness and minimal tube distance. Overwritten if GlyphData.thickness is not None
        self.thickness = thickness
        self.distance = distance
        
        # Referencing related masters by relative path, handled by the overlay assistant part
        self.srcUFOPath = srcUFOPath # "Original" master of this font, copy from here
        self.someUFOPath = someUFOPath # Show this outline on the background
        self.orgUFOPath = orgUFOPath # "Original" master of this font for overlay reference
        self.romanItalicUFOPath = romanItalicUFOPath # Roman <---> Italic master reference
        self.groupSrcUFOPath = groupSrcUFOPath or orgUFOPath # Used as groups reference to copy from
        self.kerningSrcUFOPath = kerningSrcUFOPath or orgUFOPath # Used as kerning reference.
        self.spacingSrcUFOPath = spacingSrcUFOPath # If defined, used as spacing reference, overwriting all spacing rules. Goes with spacingOffset
        self.spacingOffset = spacingOffset # Value to add to margins of self.spacingSrcUFOPath (if defined)


        # Standard interpolation factors (e.g. for scalarpolations). This overwrites the corrections directly derived from comparing the stems.
        if iFactor is None:
            iFactor = 0.5
        self.iFactor = iFactor or 0.5

        if superiorIFactorX is None:
            superiorIFactorX = 0.3
        self.superiorIFactorX = superiorIFactorX
        if superiorIFactorY is None:
            superiorIFactorY = self.superiorIFactorX
        self.superiorIFactorY = superiorIFactorY
        
        self.superiorWidthFactor = superiorWidthFactor

        if superiorOutline is None:
            superiorOutline = 16
        self.superiorOutline=superiorOutline

        if scIFactorX is None:
            scIFactorX = 0.3
        self.scIFactorX = scIFactorX
        if scIFactorY is None:
            scIFactorY = self.scIFactorX
        self.scIFactorY = scIFactorY
        
        self.scWidthFactor = scWidthFactor

        if scOutline is None:
            scOutline = 16
        self.scOutline=scOutline


        # Interpolation & design space
        self.m0 = m0 # Regular origin
        self.m1 = m1 # Direct interpolation master in "min" side
        self.m2 = m2 # Direct interpolation master on "max" side
        self.sm1 = sm1 # Scalerpolate masters for condensed and extended making.
        self.sm2 = sm2
        self.osm1 = osm1 # If defined, lighter master on same optical size level
        self.osm2 = osm2 # If defined, bolder master on same optical size level

        # Design space position (matching .designspace) to calculate triplet kerning.
        # This can be different from HStem (with m1, m2) interpolation.
        self.dsPosition = dsPosition 
        self.tripletData1 = tripletData1
        self.tripletData2 = tripletData2 # Compatible triplet sets of (name1, name2, name3, kerning) tuples for interpolation.
        self.featurePath = featurePath

        # Glyphs
        if glyphSet is None: # Print warning and use a standard glyphset
            print('### Glyphset undefined, using default.')
            glyphSet = LATIN_L_SET
        #assert glyphSet is not None, (f'### Glyphset {glyphSet} should be defined')
        self.glyphSet = glyphSet
        
        # Vertical metrics. Do some guessing for missing values. 
        # This may not be matching the current font, as we don't have it available as open RFont here.

        #self.capStackedDiacriticsVKerning = capStackedDiacriticsVKerning or 0 # Optional offset for stacked diacritics on capitals
        #self.stackedDiacriticsVKerning = stackedDiacriticsVKerning or 0 # Optional offset for stacked diacritics
        #self.topAnchorYSelectionOffset = topAnchorYSelectionOffset # Offset placement of top anchors below heigjt, for better manual selection
        #self.bottomAnchorYSelectionOffset = bottomAnchorYSelectionOffset # Offset placement of bottom aobve baseline, for better manual selection

        if baseOvershoot is None: # Generic overshoot value, specifically for lower case
            baseOvershoot = self.BASE_OVERSHOOT
        self.baseOvershoot = baseOvershoot
        if stemOvershoot is None:
            stemOvershoot = self.STEM_OVERSHOOT
        self.stemOvershoot = stemOvershoot
        if capOvershoot is None: # Overshoot value for capitals
            capOvershoot = baseOvershoot
        self.capOvershoot = capOvershoot
        if scOvershoot is None: # Overshoot value for smallcaps, mod, etc.
            scOvershoot = baseOvershoot
        self.scOvershoot = scOvershoot
        if onumOvershoot is None: # Overshoot value for old-style figures. Defaults to scOvershoot
            onumOvershoot = scOvershoot
        self.onumOvershoot = onumOvershoot
        if superiorOvershoot is None: # Overshoot value for superior, inferior, .sups, .numr, .sinf and .dnom
            superiorOvershoot = baseOvershoot
        self.superiorOvershoot = superiorOvershoot
        if diacriticsOvershoot is None:
            diacriticsOvershoot = superiorOvershoot
        self.diacriticsOvershoot = diacriticsOvershoot
        
        self.cat2Overshoot = { # Category --> overshoot
            GD.CAT_OVERSHOOT: baseOvershoot,
            GD.CAT_CAP_OVERSHOOT: capOvershoot,
            GD.CAT_SUPERIOR_OVERSHOOT: superiorOvershoot,
            GD.CAT_SC_OVERSHOOT: scOvershoot,
            GD.CAT_ONUM_OVERSHOOT: onumOvershoot,
            GD.CAT_DIACRITICS_OVERSHOOT: diacriticsOvershoot,
        }

        # Vertical anchor offsets
        self.ascenderAnchorOffsetY = ascenderAnchorOffsetY
        self.boxTopAnchorOffsetY = boxTopAnchorOffsetY
        self.capHeightAnchorOffsetY = capHeightAnchorOffsetY # Optional vertical offset of cap-anhors or lower capital diacritics.
        self.xHeightAnchorOffsetY = xHeightAnchorOffsetY
        self.baselineAnchorOffsetY = baselineAnchorOffsetY
        self.ogonekAnchorOffsetY = ogonekAnchorOffsetY
        self.boxBottomAnchorOffsetY = boxBottomAnchorOffsetY
        self.descenderAnchorOffsetY = descenderAnchorOffsetY
        
        # Vertical metrics
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
        if onumHeight is None:
            onumHeight = scHeight # Default old-style figures same height as small caps
        self.onumHeight = onumHeight
        if superiorHeight is None:
            superiorHeight = xHeight * 2/3
        self.superiorHeight = superiorHeight
        if superiorCapHeight is None:
            superiorCapHeight = capHeight * 2/3
        self.superiorCapHeight = superiorCapHeight
        if superiorAscender is None:
            superiorAscender = ascender * 2/3
        self.superiorAscender = superiorAscender
        if superiorDescender is None:
            superiorDescender = descender * 2/3
        self.superiorDescender = superiorDescender
        self.modHeight = modHeight or self.superiorHeight

        if middlexHeight is None:
            middlexHeight = xHeight/2,
        self.middlexHeight = middlexHeight        
        if middleCapHeight is None:
            middleCapHeight = capHeight/2
        self.middleCapHeight = middleCapHeight

        self.cat2Height = { # Category --> height
            GD.CAT_XHEIGHT: xHeight,
            GD.CAT_CAP_HEIGHT: capHeight,
            GD.CAT_SC_HEIGHT: scHeight,
            GD.CAT_ONUM_HEIGHT: onumHeight,
            GD.CAT_SUPERIOR_HEIGHT: superiorHeight, # Height of .sups, .sinf, .numr, .dnom and mod
        }

        if baseDiacriticsTop is None: # Baseline of top diacritics
            baseDiacriticsTop = int(round(xHeight * 1.2))
        self.baseDiacriticsTop = baseDiacriticsTop
        if capDiacriticsTop is None:
            capDiacriticsTop = int(round(capHeight * 1.1))
        self.capDiacriticsTop = capDiacriticsTop
        self.scDiacriticsTop = scDiacriticsTop
        if baseDiacriticsBottom is None: # Top of bottom diacritis
            baseDiacriticsBottom = int(round(-4 * baseOvershoot))
        self.baseDiacriticsBottom = baseDiacriticsBottom

        if baseline is None:
            baseline = self.BASELINE
        self.baseline = baseline # Main baseline, default is 0
        if modBaseline is None:
            modBaseline = xHeight
        self.modBaseline = modBaseline # Mod baseline, default is xHeight
        if supsBaseline is None:
            supsBaseline = xHeight
        if sinfBaseline is None: 
            sinfBaseline = descender  
        self.sinfBaseline = sinfBaseline # Inferior (sinf) baseline, default is descender

        self.supsBaseline = supsBaseline # Superior (sups) baseline, default is xHeight
        if numrBaseline is None: 
            numrBaseline = ascender - superiorHeight  
        self.numrBaseline = numrBaseline # Numr baseline (for fractions), default is moved down by height from ascender
        if dnomBaseline is None: 
            dnomBaseline = baseline  
        self.dnomBaseline = dnomBaseline # Dnom baseline (for fractions), default is 0

        self.cat2Baseline = {
            GD.CAT_BASELINE: baseline,
            GD.CAT_MOD_BASELINE: modBaseline,
            GD.CAT_NUMR_BASELINE: numrBaseline,
            GD.CAT_SINF_BASELINE: sinfBaseline,
            GD.CAT_SUPS_BASELINE: supsBaseline,
            GD.CAT_DNOM_BASELINE: dnomBaseline ,
        }

        # Spacing

        if emWidth is None:
            emWidth = unitsPerEm
        self.emWidth = emWidth
        if emWidth2 is None:
            emWidth2 = int(round(unitsPerEm/2))
        self.emWidth2 = emWidth2
        if enWidth is None:
            enWidth = enWidth
        self.enWidth = enWidth
        if accentWidth is None:
            accentWidth = int(round(unitsPerEm/5))
        self.accentWidth = accentWidth
        if figureWidth is None:
            figureWidth = int(round(unitsPerEm * 0.65))
        self.figureWidth = figureWidth
        if mathWidth is None:
            mathWidth = figureWidth
        self.mathWidth = mathWidth
        if fractionWidth is None:
            fractionWidth = int(round(unitsPerEm/10))
        self.fractionWidth = fractionWidth
        if tabWidth is None:
            tabWidth = figureWidth
        self.tabWidth = tabWidth
        if hairWidth is None:
            hairWidth = int(round(unitsPerEm/24))
        self.hairWidth = hairWidth

        # Margin
        if minMargin is None:
            minMargin = int(round(unitsPerEm/10))
        self.minMargin = minMargin 
        if modMinMargin is None:
            modMinMargin = int(round(unitsPerEm/12))
        self.modMinMargin = modMinMargin 

        self.cat2Width = {
            GD.CAT_ACCENT_WIDTH: accentWidth,
            GD.CAT_TAB_WIDTH: tabWidth,
            GD.CAT_MATH_WIDTH: mathWidth,
            GD.CAT_FIGURE_WIDTH: figureWidth,
            GD.CAT_FRACTION_WIDTH: fractionWidth,
            GD.CAT_EM_WIDTH: emWidth,
            GD.CAT_EM_WIDTH2: emWidth2, # Half emWidth
            GD.CAT_EN_WIDTH: enWidth,
            GD.CAT_SPACE_WIDTH: spaceWidth, # Word space
            GD.CAT_HAIR_WIDTH: hairWidth,
            # Margin
            GD.CAT_MIN_MARGIN: minMargin,
            GD.CAT_MOD_MIN_MARGIN: modMinMargin,
        }
        
        # Horizontal metrics
        self.diagonalTolerance = diagonalTolerance # ± Tolerance for italic diagonals to be marked as off-limit
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
        self.modStem = modStem

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

    def isNumber(self, v):
        return isinstance(v, (int, float))

    def getOvershoot(self, gName):
        """Answer the overshoot for this glyph based on the settings of the related GlyphData and otherwise guessing on its name."""
        gd = self.glyphSet.get(gName)
        if gd is None:
            print(f'### getOvershoot: Unknown glyph /{gName} in glyphSet of {self.name}')
            return self.baseOvershoot
        # If there is a category defined in the glyphData for this glyph, then answer the referenced category value.
        if gd.overshoot in self.cat2Overshoot:
            return self.cat2Overshoot[gd.overshoot]
        if isinstance(gd.overshoot, (int, float)): 
            return gd.overshoot

        # Not defined in the GlyphSet/GlyphData for this glyph. We need to do some quessing, based on the name.
        if gd.isOnum: # Old-style figures
            return self.cat2Overshoot[GD.CAT_ONUM_OVERSHOOT]
        if gd.isSuperior or gd.isNumr or gd.isInferior or gd.isDnom or gd.isMod: # One of sups, sinf, dnom, numr, mod in the name
            return self.cat2Overshoot[GD.CAT_SUPERIOR_OVERSHOOT]
        if gd.isSc: # One of .sc, small in the name
            return self.cat2Overshoot[GD.CAT_SC_OVERSHOOT]
        if gd.isUpper: # All glyph that start with initial cap
            return self.cat2Overshoot[GD.CAT_CAP_OVERSHOOT]
        # Otherwise answer the default overshoot. 
        return self.baseOvershoot

    def getBaseline(self, gName):
        """Answer the baseline position for this glyph based on the settings of the related GlyphData and otherwise guessing on its name."""
        gd = self.glyphSet.get(gName)
        if gd is None:
            print(f'### getBaseline: Unknown glyph /{gName} in glyphSet of {self.name}')
            return self.BASELINE
        if gd.baseline is None: # Nothing defined in the glyph, use the default
            return self.BASELINE
        if isinstance(gd.baseline, (int, float)): 
            return gd.baseline
        # If there is a category defined in the glyphData for this glyph, then answer the referenced category value.
        if gd.baseline in self.cat2Baseline:
            return self.cat2Baseline[gd.baseline]
        # Not defined in the GlyphSet/GlyphData for this glyph. We need to do some quessing, based on the type of glyph or its name.
        if gd.isSuperior:
            return self.supsBaseline
        if gd.isInferior:
            return self.sinfBaseline
        if gd.isNumr:
            return self.numrBaseline
        if gd.isDnom:
            return self.dnomBaseline
        if gd.isMod:
            return self.modBaseline
        return self.BASELINE

    def getHeight(self, gName):
        """Answer the height for this glyph based on the settings of the related GlyphData and otherwise guessing on its name."""
        gd = self.glyphSet.get(gName)
        if gd is None:
            print(f'### getHeight: Unknown glyph /{gName} in glyphSet of {self.name}')
            return self.capHeight
        # Old-style figures
        if gName.endswith('.onum') or gd.isOnum:
            return self.onumHeight
        # Smallcaps
        if gName.endswith('.sc') or gd.isSc:
            return self.scHeight
        # Normal height
        if gd.height is None: # Nothing defined in the glyph, use the default
            if gd.isLower:
                return self.xHeight
            return self.capHeight
        if isinstance(gd.height, (int, float)): 
            return gd.height
        # If there is a category defined in the glyphData for this glyph, then answer the referenced category value.
        # Not defined in the GlyphSet/GlyphData for this glyph. We need to do some quessing, based on the type of glyph or its name.
        if gd.isMod or gd.isSuperior or gd.isNumr or gd.isInferior or gd.isDnom:
            return self.superiorHeight
        if gd.isLower:
            return self.xHeight
        return self.capHeight

    def getHeight2(self, gName):
        """Answer the rounded half of height."""
        return int(round(self.getHeight(gName)/2))
    
    def getAnchorOvershoot(self, gName):
        """Answer the standard overshoot of anchors (to make sure they don't overlap with outline points)"""
        return 16 # for now

MD = MasterData



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])




