# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    ttxcompiler.py
#
#from lib.fontObjects.doodleFontCompiler.ttfCompiler import TTFCompilerSettings as CS
from tnbits.compilers.ttfcompilersettings import TTFCompilerSettings as CS

from tnbits.toolbox.transformer import TX
from tnbits.toolbox.dimensions.floqs.value.floqmeme import FloqMeme
#from tnbits.model.hinting.compiler.wingcompiler import WingCompiler

class TTXCompiler(object):

    @classmethod
    def compileToBinary(cls, font):
        """
        Fill all font.lib values so they can be used by the RoboFont font compiler.
        This class method gets call by RoboFont on writing a binary font through
        subscription by addObserver(cls, "fontWillGenerateCallback", "fontWillGenerate")
        """
        fontLib = font.lib
        # OS/2

        # gasp
        gasp = fontLib.get(CS.fbHintGaspLibKey + '.dict')
        if gasp is None:
            gasp = {'8': 2, '16': 1, '65535': 3}
        fontLib[CS.fbHintGaspLibKey] = gasp # For now, just copy the dict

        # maxp
        maxp = fontLib.get(CS.fbHintMaxp, {})
        """
        fbHintMaxp = "com.robofont.fbhint.maxp" # base name
        fbHintMaxpMaxZonesLibKey = "com.robofont.fbhint.maxp.maxZones" # int
        fbHintMaxpMaxTwilightPointsLibKey = "com.robofont.fbhint.maxp.maxTwilightPoints" # int
        fbHintMaxpMaxStorageLibKey = "com.robofont.fbhint.maxp.maxStorage" # int
        fbHintMaxpMaxFunctionDefsLibKey = "com.robofont.fbhint.maxp.maxFunctionDefs" # int
        fbHintMaxpMaxInstructionDefsLibKey = "com.robofont.fbhint.maxp.maxInstructionDefs" # int
        fbHintMaxpMaxStackElementsLibKey = "com.robofont.fbhint.maxp.maxStackElements" # int
        fbHintMaxpMaxSizeOfInstructionsLibKey = "com.robofont.fbhint.maxp.maxSizeOfInstructions" # int
        fbHintMaxpMaxComponentElementsLibKey = "com.robofont.fbhint.maxp.maxComponentElements" # int

        maxComponentDepth (4874664960)    int: 0
        maxComponentElements (4874652080)    int: 0
        maxCompositeContours (4874651952)    int: 0
        maxCompositePoints (4874664624)    int: 0
        maxContours (4874656624)    int: 5
        maxFunctionDefs (4874664736)    int: 22
        maxInstructionDefs (4874664792)    int: 0
        maxPoints (4874656576)    int: 70
        maxSizeOfInstructions (4874652016)    int: 408
        maxStackElements (4874664848)    int: 256
        maxStorage (4874657056)    int: 2
        maxTwilightPoints (4874664568)    int: 1
        maxZones (4874656816)    int: 2
        numGlyphs (4874656336)    int: 226
        tableTag (4711703344)    str: maxp
        tableVersion (4874664232)    int: 65536
        """

        if maxp is not None:
            for maxpKey in (
                CS.fbHintMaxpMaxZonesLibKey, CS.fbHintMaxpMaxTwilightPointsLibKey,
                CS.fbHintMaxpMaxStorageLibKey, CS.fbHintMaxpMaxFunctionDefsLibKey,
                CS.fbHintMaxpMaxInstructionDefsLibKey, CS.fbHintMaxpMaxStackElementsLibKey,
                CS.fbHintMaxpMaxSizeOfInstructionsLibKey, CS.fbHintMaxpMaxComponentElementsLibKey
            ):
                #    maxpKey: "com.robofont.fbhint.maxp.maxZones" # int
                #    fbHintKey: "maxZones" # int
                fbHintKey = maxpKey.split('.')[-1]
                if maxpKey in fontLib:
                    del fontLib[maxpKey]
                if fbHintKey in maxp:
                    fontLib[maxpKey] = maxp[fbHintKey]

        # CVT
        cvtDict = fontLib.get(CS.fbHintCvtLibKey + '.dict', {})
        if cvtDict is not None:
            # Make sure that there is at least one value here, to have it written as table.
            if not cvtDict:
                cvtDict[0] = 0 #FloqMeme()
            # Convert the string keys of the CVT to a dict with integer keys,
            # because TTX requires that and get the values from the CVT FloqMeme instances
            cvtDict = TX.stringKeyDict2IntKeyDict(cvtDict)
            cvts = []
            cvtKeys = cvtDict.keys()
            # Make a range until the maximum id of CVT and fill in the blanks
            for index in range(max(cvtKeys)+1): # Don't forget to include the last one
                # The storage is now as dict, make this into a list where the holes are filled by zero's
                #cvts.append(cvtDict.get(index, 0).get('value', 0)) # To be replaced by CVT FloqMeme instance.
                cvts.append(cvtDict.get(index, 0)) # To be replaced by CVT FloqMeme instance.
            fontLib[CS.fbHintCvtLibKey] = cvts

        # Hint programs, make them compile to assembly
        #WingCompiler.compileData(font, 'fpgm')
        #WingCompiler.compileData(font, 'prep')
        #for glyph in font:
        #    WingCompiler.compileData(glyph, 'glyf')

