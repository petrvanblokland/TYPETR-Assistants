# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   groupBaseGlyphs.py
#

# Glyphs that are used as base for groups. Scripts only kern within the script (and "all") to the other side.
# The "all" also kern to each other, on the other side. There is no kerning allowed between the scripts.
# 
# Since we now format the group names so that they include the base glyph in the name, we can extract 
# the base glyph name and the script name with kerningManager.groupName2baseGlyphScript(groupName) --> (baseGlyph, scriptName)
#

FORCE_GROUP1 = {}
FORCE_GROUP2 = {}

PUBLIC_KERN1 = 'public.kern1.'
PUBLIC_KERN2 = 'public.kern2.'

SC = 'sc'
UC1 = 'uc1'
UC2 = 'uc2'

LT1 = 'lt1'
LT2 = 'lt2'
SC_LT1 = SC + LT1
SC_LT2 = SC + LT2

CY1 = 'cy1'
CY2 = 'cy2'
SC_CY1 = SC + CY1
SC_CY2 = SC + CY2

GR1 = 'gr1'
GR2 = 'gr2'
SC_GR1 = SC + GR1
SC_GR2 = SC + GR2

ASC1 = 'asc1'
ASC2 = 'asc2'

FIG1 = 'fig1'
FIG2 = 'fig2'
SC_FIG1 = SC + FIG1
SC_FIG2 = SC + FIG2

SUPS1 = 'sups1' # Superior figures
SUPS2 = 'sups2'
SINF1 = 'sinf1' # Inferior figures
SINF2 = 'sinf2'
TSUPS1= 'tsups1' # Latin text superiors
TSUPS2= 'tsups2'
TSINF1= 'tsinf1' # Latin text inferiors
TSINF2= 'tsinf2'

DNOM1 = 'dnom1'
DNOM2 = 'dnom2'
NUMR1 = 'numr1'
NUMR2 = 'numr2'
DNOM1 = 'dnom1'
DNOM2 = 'dnom2'
ONUM1 = 'onum1'
ONUM2 = 'onum2'

NOK1 = 'nok1' # No kerning necessary (leave out of sample)
NOK2 = 'nok2'

XXX_GROUP_NAME_PARTS = {
    LT1:    (PUBLIC_KERN1, '_lt'), 
    LT2:    (PUBLIC_KERN2, '_lt'),
    SC_LT1: (PUBLIC_KERN1, '_sc_lt'),
    SC_LT2: (PUBLIC_KERN2, '_sc_lt'),

    CY1: (PUBLIC_KERN1, '_cy'), 
    CY2: (PUBLIC_KERN2, '_cy'),
    SC_CY1: (PUBLIC_KERN1, '_sc_cy'),
    SC_CY2: (PUBLIC_KERN2, '_sc_cy'),

    GR1: (PUBLIC_KERN1, '_gr'), 
    GR2: (PUBLIC_KERN2, '_gr'),
    SC_GR1: (PUBLIC_KERN1, '_sc_gr'),
    SC_GR2: (PUBLIC_KERN2, '_sc_gr'),

    ASC1: (PUBLIC_KERN1, '_asc'), 
    ASC2: (PUBLIC_KERN2, '_asc'),

    FIG1: (PUBLIC_KERN1, '_fig'), 
    FIG2: (PUBLIC_KERN2, '_fig'),

    UC1: (PUBLIC_KERN1, '_uc'), 
    UC2: (PUBLIC_KERN2, '_uc'),

    SUPS1: (PUBLIC_KERN1, '_sups'), 
    SUPS2: (PUBLIC_KERN2, '_sups'),
    SINF1: (PUBLIC_KERN1, '_sinf'), 
    SINF2: (PUBLIC_KERN2, '_sinf'),
    NUMR1: (PUBLIC_KERN1, '_numr'), 
    NUMR2: (PUBLIC_KERN2, '_numr'),
    DNOM1: (PUBLIC_KERN1, '_dnom'), 
    DNOM2: (PUBLIC_KERN2, '_dnom'),
    ONUM1: (PUBLIC_KERN1, '_onum'), 
    ONUM2: (PUBLIC_KERN2, '_onum'),
}
XXX_BASE_SCRIPTS1 = (
    LT1, SC_LT1, 
    CY1, SC_CY1, 
    GR1, SC_GR1, 
    ASC1, 
    FIG1, SC_FIG1, 
    SUPS1, SINF1, NUMR1, DNOM1, ONUM1)
XXX_BASE_SCRIPTS2 = (
    LT2, SC_LT2, 
    CY2, SC_CY2, 
    GR2, SC_GR2, 
    ASC2, 
    FIG2, 
    SUPS2, SINF2, NUMR2, DNOM2, ONUM2)

# Defining all script <--> script combinations in the kerning table.
# Also this table is used to generate at least one placeholder kerning pair,
# to ensure that the [kern] lookup gets generated. Otherwise building the VF
# complains for incompatible amounts of [kern] lookups.
# In general this gets solved automatically if all kerning exists, but during 
# development not all kerning may have been filled in.

KERN_GROUPS = (
    # Latin
    (LT1, LT2),
    (LT1, SC_LT1),
    (SC_LT1, SC_LT2),

    (LT1, ASC2),
    (SC_LT1, ASC2),
    (ASC1, ASC2),

    (LT1, FIG2),
    (FIG1, FIG2),
    
    (LT1, SUPS2),
    (LT1, TSUPS2),
    (LT1, SINF2),
    (LT1, TSINF2),
    
    (LT1, NUMR2),
    (LT1, DNOM2),
    (NUMR1, NUMR2),
    
    (LT1, ONUM1),
    (ONUM1, ONUM2),

    # Cyrillic
    (CY1, CY2),
    (CY1, SC_CY1),
    (SC_CY1, SC_CY2),

    (CY1, ASC2),
    (SC_CY1, ASC2),

    (CY1, FIG2),
    (FIG1, CY2),
    
    (CY1, SUPS2),
    (CY1, SINF2),
    
    (CY1, NUMR2),
    (CY1, DNOM2),

    # Greek
    (GR1, GR2),
    (GR1, SC_GR1),
    (SC_GR1, SC_GR2),

    (GR1, ASC2),
    (SC_GR1, ASC2),

    (GR1, FIG2),
    
    (GR1, SUPS2),
    (GR1, SINF2),
    
    (GR1, NUMR2),
    (GR1, DNOM2),    
    (GR1, ONUM2),

)


GROUP_IGNORE = ('tnum', 'cmb', 'comb', 'mod', 'component',) # Always ignore glyphs that include these patterns

