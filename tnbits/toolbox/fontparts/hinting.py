# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.ttLib import TTFont, newTable
from tnbits.constants import Constants as C
from tnbits.toolbox.transformer import TX

class BaseHintManager:
    # glyf table
    fbHintGlyphAssemblyLibKey = "com.robofont.fbhint.assembly" # list of assembly code
    # maxp
    fbHintMaxp = "com.robofont.fbhint.maxp" # base name
    fbHintMaxpMaxZonesLibKey = "com.robofont.fbhint.maxp.maxZones" # int
    fbHintMaxpMaxTwilightPointsLibKey = "com.robofont.fbhint.maxp.maxTwilightPoints" # int
    fbHintMaxpMaxStorageLibKey = "com.robofont.fbhint.maxp.maxStorage" # int
    fbHintMaxpMaxFunctionDefsLibKey = "com.robofont.fbhint.maxp.maxFunctionDefs" # int
    fbHintMaxpMaxInstructionDefsLibKey = "com.robofont.fbhint.maxp.maxInstructionDefs" # int
    fbHintMaxpMaxStackElementsLibKey = "com.robofont.fbhint.maxp.maxStackElements" # int
    fbHintMaxpMaxSizeOfInstructionsLibKey = "com.robofont.fbhint.maxp.maxSizeOfInstructions" # int
    fbHintMaxpMaxComponentElementsLibKey = "com.robofont.fbhint.maxp.maxComponentElements" # int
    # OS/2
    fbHintOS2LibKey = "com.robofont.fbhint.OS/2 " # dict
    # cvt
    fbHintCvtLibKey = "com.robofont.fbhint.cvt " # list, note the space in the name for compatibility
    # fpgm
    fbHintFpgmLibKey = "com.robofont.fbhint.fpgm" # list of assembly code
    # prep
    fbHintPrepLibKey = "com.robofont.fbhint.prep" # list of assembly code
    # gasp
    fbHintGaspLibKey = "com.robofont.fbhint.gasp" # dict of int ranges {8: 2, 16: 1, 65535: 3}


class TTFontHintManager(BaseHintManager):
    """
    For managing hints in a fontTools TTFont.
    """

    @classmethod
    def getMAXP(cls, font):
        if C.TABLE_MAXP in font:
            return font[C.TABLE_MAXP].__dict__
        return {}

    @classmethod
    def setMAXP(cls, font, values):
        font["maxp"] = maxp = newTable("maxp")
        maxp.tableVersion = 0x10000
        maxp.maxZones = values.get(cls.fbHintMaxpMaxZonesLibKey.split('.')[-1], 1)
        maxp.maxTwilightPoints = values.get(cls.fbHintMaxpMaxTwilightPointsLibKey.split('.')[-1], 0)
        maxp.maxStorage = values.get(cls.fbHintMaxpMaxStorageLibKey.split('.')[-1], 0)
        maxp.maxFunctionDefs = values.get(cls.fbHintMaxpMaxFunctionDefsLibKey.split('.')[-1], 0)
        maxp.maxInstructionDefs = values.get(cls.fbHintMaxpMaxInstructionDefsLibKey.split('.')[-1], 0)
        maxp.maxStackElements = values.get(cls.fbHintMaxpMaxStackElementsLibKey.split('.')[-1], 512)
        maxp.maxSizeOfInstructions = values.get(cls.fbHintMaxpMaxSizeOfInstructionsLibKey.split('.')[-1], 1023)
        maxp.maxComponentElements = values.get(cls.fbHintMaxpMaxComponentElementsLibKey.split('.')[-1], 0)

    @classmethod
    def delMAXP(cls, font):
        if C.TABLE_MAXP in font:
            del font[C.TABLE_MAXP]

    @classmethod
    def getCVT_(cls, font):
        if C.TABLE_CVT_ in font:
            return list(font[C.TABLE_CVT_].values)
        return []

    @classmethod
    def setCVT_(cls, font, cvtValues):
        # ufocvt needs to be a continues list of values with 0 at the missing slots.
        if cvtValues is not None:
            import array
            font['cvt '] = cvt = newTable('cvt ')
            #@@@ Bug in table__c_v_t: cvt.values is not defined yet
            cvt.values = array.array("h")
            ## for key, value in ufocvt:
            ##    cvt[key] = value
            ## this means you can not have a list that jumps from 0 1 2 15 16 17
            ## from the fontTools code I assume that this is the case, so this must be possible
            ## array.array allows empty slots and fills it with '0'
            ## I think it should be stored in the ufo lib as a dict not a list. I could be wrong
            [cvt.values.append(value) for value in cvtValues]

    @classmethod
    def delCVT_(cls, font):
        if C.TABLE_CVT_ in font:
            del font[C.TABLE_CVT_]

    @classmethod
    def getFPGM(cls, font):
        if C.TABLE_FPGM in font:
            return font[C.TABLE_FPGM].program.getAssembly()
        return []

    @classmethod
    def setFPGM(cls, font, value):
        if value is not None:
            font[C.TABLE_FPGM] = fpgm = newTable(C.TABLE_FPGM)
            fpgm.program = Program()
            fpgm.program.fromAssembly(value)

    @classmethod
    def delFPGM(cls, font):
        if C.TABLE_FPGM in font:
            del font[C.TABLE_FPGM]

    @classmethod
    def getPREP(cls, font):
        if C.TABLE_PREP in font:
            return font[C.TABLE_PREP].program.getAssembly()
        return []

    @classmethod
    def setPREP(cls, font, value):
            font[C.TABLE_PREP] = fpgm = newTable(C.TABLE_PREP)
            fpgm.program = Program()
            fpgm.program.fromAssembly(value)

    @classmethod
    def delPREP(cls, font):
        if C.TABLE_PREP in font:
            del font[C.TABLE_PREP]

    @classmethod
    def getGASP(cls, font):
        if C.TABLE_GASP in font:
            origGasp = font[C.TABLE_GASP].gaspRange
            gasp = {}
            for key, value in origGasp.items():
                gasp[str(key)] = value
            return gasp
        return {}

    @classmethod
    def setGASP(cls, font, values):
        if values is not None:
            # Make sure that the values are ok.
            ufogaspints = {}
            for key, value in values.items():
                ufogaspints[int(key)] = int(value)  # Key as int(65535) gives error.
            cls.otf[C.TABLE_GASP] = gasp = newTable(C.TABLE_GASP)
            gasp.gaspRange = ufogaspints

    @classmethod
    def delGASP(cls, font):
        if C.TABLE_GASP in font:
            del font[C.TABLE_GASP]

    @classmethod
    def getGLYFAssembly(cls, glyph=None):
        if hasattr(glyph, 'program'):
            return glyph.program.getAssembly()
        return []

    @classmethod
    def setGLYFAssembly(cls, glyph, value):
        glyph.program.fromAssembly(value)

    @classmethod
    def delGLYFAssembly(cls, glyph):
        if hasattr(glyph, 'program'):
            glyph.program = Program()
            glyph.program.fromAssembly([])

    @classmethod
    def getAllGLYFAssembly(cls, font):
        glyfMap = {}
        if C.TABLE_GLYF in font:
            for gname, glyph in font[C.TABLE_GLYF].glyphs.items():
                glyfMap[gname] = cls.getGLYFAssembly(glyph)
        return glyfMap

    @classmethod
    def setAllGLYFAssembly(cls, font, value):
        if C.TABLE_GLYF in font:
            for gname, glyph in font[C.TABLE_GLYF].glyphs.items():
                cls.setGLYFAssembly(glyph, value.get(gname) or [])

    @classmethod
    def delAllGLYFAssembly(cls, font):
        if C.TABLE_GLYF in font:
            for gname, glyph in font[C.TABLE_GLYF].glyphs.items():
                font[gname] = cls.delGLYFAssembly(glyph)

class UFOHintManager(BaseHintManager):
    """
    For managing hints in a UFO.
    """

    @classmethod
    def getMAXP(cls, font):
        maxp = dict()
        maxp['maxZones'] = font.lib.get(cls.fbHintMaxpMaxZonesLibKey)
        maxp['maxTwilightPoints'] = font.lib.get(cls.fbHintMaxpMaxTwilightPointsLibKey)
        maxp['maxStorage'] = font.lib.get(cls.fbHintMaxpMaxStorageLibKey)
        maxp['maxFunctionDefs'] = font.lib.get(cls.fbHintMaxpMaxFunctionDefsLibKey)
        maxp['maxInstructionDefs'] = font.lib.get(cls.fbHintMaxpMaxInstructionDefsLibKey)
        maxp['maxStackElements'] = font.lib.get(cls.fbHintMaxpMaxStackElementsLibKey)
        maxp['maxSizeOfInstructions'] = font.lib.get(cls.fbHintMaxpMaxSizeOfInstructionsLibKey)
        maxp['maxComponentElements'] = font.lib.get(cls.fbHintMaxpMaxComponentElementsLibKey)
        return maxp

    @classmethod
    def setMAXP(cls, font, values):
        maxp = values
        font.lib[cls.fbHintMaxpMaxZonesLibKey] = maxp.get('maxZones')
        font.lib[cls.fbHintMaxpMaxTwilightPointsLibKey] = maxp.get('maxTwilightPoints')
        font.lib[cls.fbHintMaxpMaxStorageLibKey] = maxp.get('maxStorage')
        font.lib[cls.fbHintMaxpMaxFunctionDefsLibKey] = maxp.get('maxFunctionDefs')
        font.lib[cls.fbHintMaxpMaxInstructionDefsLibKey] = maxp.get('maxInstructionDefs')
        font.lib[cls.fbHintMaxpMaxStackElementsLibKey] = maxp.get('maxStackElements')
        font.lib[cls.fbHintMaxpMaxSizeOfInstructionsLibKey] = maxp.get('maxSizeOfInstructions')
        font.lib[cls.fbHintMaxpMaxComponentElementsLibKey] = maxp.get('maxComponentElements')

    @classmethod
    def delMAXP(cls, font):
        if cls.fbHintMaxpMaxZonesLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxZonesLibKey]
        if cls.fbHintMaxpMaxTwilightPointsLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxTwilightPointsLibKey]
        if cls.fbHintMaxpMaxStorageLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxStorageLibKey]
        if cls.fbHintMaxpMaxFunctionDefsLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxFunctionDefsLibKey]
        if cls.fbHintMaxpMaxInstructionDefsLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxInstructionDefsLibKey]
        if cls.fbHintMaxpMaxStackElementsLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxStackElementsLibKey]
        if cls.fbHintMaxpMaxSizeOfInstructionsLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxSizeOfInstructionsLibKey]
        if cls.fbHintMaxpMaxComponentElementsLibKey in font.lib:
            del font.lib[cls.fbHintMaxpMaxComponentElementsLibKey]

    @classmethod
    def getCVT_(cls, font):
        return font.lib.get(cls.fbHintCvtLibKey)

    @classmethod
    def setCVT_(cls, font, value):
        font.lib[cls.fbHintCvtLibKey] = value

    @classmethod
    def delCVT_(cls, font):
        if cls.fbHintCvt in font.lib:
            del font.lib[cls.fbHintCvt]

    @classmethod
    def getFPGM(cls, font):
        return font.lib.get(cls.fbHintFpgmLibKey)

    @classmethod
    def setFPGM(cls, font, value):
        font.lib[cls.fbHintFpgmLibKey] = value

    @classmethod
    def delFPGM(cls, font):
        if cls.fbHintFpgmLibKey in font.lib:
            del font.lib[cls.fbHintFpgmLibKey]

    @classmethod
    def getPREP(cls, font):
        return font.lib.get(cls.fbHintPrepLibKey)

    @classmethod
    def setPREP(cls, font, value):
        font.lib[cls.fbHintPrepLibKey] = value

    @classmethod
    def delPREP(cls, font):
        if cls.fbHintPrepLibKey in font.lib:
            del font.lib[cls.fbHintPrepLibKey]

    @classmethod
    def getGASP(cls, font):
        origGasp = font.lib.get(cls.fbHintGaspLibKey)
        gasp = {}
        if origGasp:
            for key, value in origGasp.items():
                gasp[int(key)] = value
            return gasp
        else:
            return origGasp

    @classmethod
    def setGASP(cls, font, value={}):
        origGasp = value
        gasp = {}
        if origGasp:
            for key, v in origGasp.items():
                gasp[str(key)] = v
        font.lib[cls.fbHintGaspLibKey] = gasp

    @classmethod
    def delGASP(cls, font):
        if cls.fbHintGaspLibKey in font.lib:
            del font.lib[cls.fbHintGaspLibKey]

    @classmethod
    def getGLYFAssembly(cls, glyph):
        return glyph.lib.get(cls.fbHintGlyphAssemblyLibKey)

    @classmethod
    def setGLYFAssembly(cls, glyph, value):
        glyph.lib[cls.fbHintGlyphAssemblyLibKey] = value

    @classmethod
    def delGLYFAssembly(cls, glyph):
        if cls.fbHintGlyphAssemblyLibKey in glyph.lib:
            del glyph.lib[cls.fbHintGlyphAssemblyLibKey]

    @classmethod
    def getAllGLYFAssembly(cls, font):
        glyfMap = {}
        for glyph in font:
            glyfMap[glyph.name] = cls.getGLYFAssembly(glyph)
        return glyfMap

    @classmethod
    def setAllGLYFAssembly(cls, font, glyfMap={}):
        for gname, assembly in glyfMap.items():
            if gname in font:
                font[gname].lib[cls.fbHintGlyphAssemblyLibKey] = assembly

    @classmethod
    def delAllGLYFAssembly(cls, font):
        for glyph in font:
            if cls.fbHintGlyphAssemblyLibKey in glyph.lib:
                del glyph.lib[cls.fbHintGlyphAssemblyLibKey]

class HintingTX:

    @classmethod
    def remove(cls, f):
        # get extractor
        if isinstance(f, TTFont):
            deleter = TTFontHintManager
        else:
            deleter = UFOHintManager
        #deleter.delMAXP(f)
        deleter.delCVT_(f)
        deleter.delFPGM(f)
        deleter.delPREP(f)
        deleter.delGASP(f)
        #deleter.delAllGLYFAssembly(f)

    @classmethod
    def copy(cls, source, dest, DEBUG=False, clear=True):
        """
        readHints: Copies hinting from a TTF into a UFO lib. Source is a UFO or TTFont, For now, dest is a UFO.
        """
        # get extractor
        if isinstance(source, TTFont):
            extractor = TTFontHintManager
        else:
            extractor = UFOHintManager
        # get inserter
        if isinstance(source, TTFont):
            inserter = TTFontHintManager
        else:
            inserter = UFOHintManager
        # get and set
        inserter.setMAXP(dest, extractor.getMAXP(source))
        inserter.setCVT_(dest, extractor.getCVT_(source))
        inserter.setFPGM(dest, extractor.getFPGM(source))
        inserter.setPREP(dest, extractor.getPREP(source))
        inserter.setGASP(dest, extractor.getGASP(source))
        inserter.setAllGLYFAssembly(dest, extractor.getAllGLYFAssembly(source))

    @classmethod
    def ttfautohint(cls, path, dest=None):
        """
        Run ttfautohint
        """
        if not dest:
            dest = path
        TX.bash('ttfautohint "%s" "%s"' %(path, dest))

    #def copyOld(cls, source, dest, DEBUG=False, clear=True):
    #    # do font hints
    #    d = {}
    #    d[C.TABLE_MAXP] = extractor.getMAXP(source)    # Used as object with attribute values
    #    d[C.TABLE_CVT_] = extractor.getCVT_(source)
    #    d[C.TABLE_FPGM] = extractor.getFPGM(source)
    #    d[C.TABLE_PREP] = extractor.getPREP(source)
    #    d[C.TABLE_GASP] = extractor.getGASP(source)
    #    for key, value in d.items():
    #        libKey = str(C.FONTLIB_ROBOHINT+'.'+key)
    #        if value:
    #            dest.lib[libKey] = value
    #        elif libKey in dest.lib and clear:
    #            del dest.lib[libKey]
    #    # do glyph hints
    #    glyfMap = extractor.getAllGLYFAssembly(source)
    #    libKey = C.FONTLIB_ROBOHINT+'.assembly'
    #    for g in dest:
    #        if g.name in glyfMap:
    #            g.lib[libKey] = glyfMap[g.name]
    #        elif libKey in g.lib and clear:
    #            del g.lib[libKey]

if __name__ == "__main__":
    paths = [u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Black_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Bold_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Compressed_Black_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Compressed_Bold_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Compressed_Light_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Compressed_Thin_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Compressed_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Condensed_Black_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Condensed_Bold_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Condensed_Light_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Condensed_Thin_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Condensed_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Extended_Black_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Extended_Bold_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Extended_Light_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Extended_Thin_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Extended_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Light_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Regular_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Thin_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Wide_Black_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Wide_Bold_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Wide_Light_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Wide_Thin_WebTT.AH.ttf", u"/Users/david/Downloads/_Agency_FB_gaggle_WebTT_TTF_AH-2/_Agency_FB-Wide_WebTT.AH.ttf"]
    for path in paths:
        source = TTFont(path)
        HintingTX.remove(source)
        source.save(path.replace('_Agency_FB_gaggle_WebTT_TTF_AH-2', '_Agency_FB_gaggle_WebTT_TTF_AH-3'))
    print('done')
