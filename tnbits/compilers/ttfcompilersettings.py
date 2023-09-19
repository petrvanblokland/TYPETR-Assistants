# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    ttfcompilersettings.py
#
#    Copied from RoboFont

class TTFCompilerSettings(object):

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
    fbHintOS2LibKey = "com.robofont.fbhint.OS/2" # dict

    # cvt
    fbHintCvtLibKey = "com.robofont.fbhint.cvt " # list, note the space in the name for compatibility

    # fpgm
    fbHintFpgmLibKey = "com.robofont.fbhint.fpgm" # list of assembly code

    # prep
    fbHintPrepLibKey = "com.robofont.fbhint.prep" # list of assembly code

    # gasp
    fbHintGaspLibKey = "com.robofont.fbhint.gasp" # dict of int ranges {8: 2, 16: 1, 65535: 3}

    # GPOS
    fbHintGPOSLibKey = "com.robofont.fbhint.GPOS.xml" # TTX-XML decompile
    
    # GSUB
    fbHintGSUBLibKey = "com.robofont.fbhint.GSUB.xml" # TTX-XML decompile
