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

FORCE_GROUP1 = {}
FORCE_GROUP2 = {}

PUBLIC_KERN1 = 'public.kern1.'
PUBLIC_KERN2 = 'public.kern2.'

SC = 'sc'
UC1 = 'uc1'
UC2 = 'uc2'

LT1 = 'lt1'
LT2 = 'lt2'
LT1_SC = SC + LT1
LT2_SC = SC + LT2

CY1 = 'cy1'
CY2 = 'cy2'
CY1_SC = SC + CY1
CY2_SC = SC + CY2

GR1 = 'gr1'
GR2 = 'gr2'
GR1_SC = SC + GR1
GR2_SC = SC + GR2

ASC1 = 'asc1'
ASC2 = 'asc2'

FIG1 = 'fig1'
FIG2 = 'fig2'
FIG1_SC = SC + FIG1
FIG2_SC = SC + FIG2

SUPS1 = 'superior1'
SUPS2 = 'superior2'
SINF1 = 'inferior1'
SINF2 = 'inferior2'
DNOM1 = 'dnom1'
DNOM2 = 'dnom2'
NUMR1 = 'numr1'
NUMR2 = 'numr2'
DNOM1 = 'dnom1'
DNOM2 = 'dnom2'
ONUM1 = 'onum1'
ONUM2 = 'onum2'

NOK = 'nok' # No kerning necessary (leave out of sample)

GROUP_NAME_PARTS = {
    LT1:    (PUBLIC_KERN1, '_lt'), 
    LT2:    (PUBLIC_KERN2, '_lt'),
    LT1_SC: (PUBLIC_KERN1, '_sc_lt'),
    LT2_SC: (PUBLIC_KERN2, '_sc_lt'),

    CY1: (PUBLIC_KERN1, '_cy'), 
    CY2: (PUBLIC_KERN2, '_cy'),
    CY1_SC: (PUBLIC_KERN1, '_sc_cy'),
    CY2_SC: (PUBLIC_KERN2, '_sc_cy'),

    GR1: (PUBLIC_KERN1, '_gr'), 
    GR2: (PUBLIC_KERN2, '_gr'),
    GR1_SC: (PUBLIC_KERN1, '_sc_gr'),
    GR2_SC: (PUBLIC_KERN2, '_sc_gr'),

    ASC1: (PUBLIC_KERN1, '_asc'), 
    ASC2: (PUBLIC_KERN2, '_asc'),

    FIG1: (PUBLIC_KERN1, '_fig'), 
    FIG2: (PUBLIC_KERN2, '_fig'),

    UC1: (PUBLIC_KERN1, '_uc'), 
    UC2: (PUBLIC_KERN2, '_uc'),

    SUPS1: (PUBLIC_KERN1, '_superior'), 
    SUPS2: (PUBLIC_KERN2, '_superior'),
    SINF1: (PUBLIC_KERN1, '_inferior'), 
    SINF2: (PUBLIC_KERN2, '_inferior'),
    NUMR1: (PUBLIC_KERN1, '_numr'), 
    NUMR2: (PUBLIC_KERN2, '_numr'),
    DNOM1: (PUBLIC_KERN1, '_dnom'), 
    DNOM2: (PUBLIC_KERN2, '_dnom'),
    ONUM1: (PUBLIC_KERN1, '_onum'), 
    ONUM2: (PUBLIC_KERN2, '_onum'),
}
BASE_SCRIPTS1 = (
    LT1, LT1_SC, 
    CY1, CY1_SC, 
    GR1, GR1_SC, 
    ASC1, 
    FIG1, FIG1_SC, 
    SUPS1, SINF1, NUMR1, DNOM1, ONUM1)
BASE_SCRIPTS2 = (
    LT2, LT2_SC, 
    CY2, CY2_SC, 
    GR2, GR2_SC, 
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
    (LT1_SC, LT2_SC),
    (LT1, LT1_SC),
    (LT1, UC2),
    (UC1, LT2),

    (ASC1, ASC2),
    (ASC1, LT2),
    (ASC1, LT2_SC),
    (LT1, ASC2),
    (LT1_SC, ASC2),

    (FIG1, FIG2),
    (FIG1, LT2),
    (LT1, FIG2),
    
    (SUPS1, SUPS2),
    (SINF1, SINF2),
    (LT1, SUPS2),
    (LT1, SINF2),
    (SUPS1, LT2),
    (SINF1, LT2),
    
    (NUMR1, NUMR2),
    (LT1, NUMR2),
    (LT1, DNOM2),
    (NUMR1, LT2),
    (DNOM1, LT2),
    
    (ONUM1, ONUM2),
    (ONUM1, LT2),
    (LT1, ONUM2),

    # Cyrillic
    (CY1, CY2),
    (CY1_SC, CY2_SC),
    (CY1, CY1_SC),

    #(ASC1, ASC2),
    (ASC1, CY2),
    (ASC1, CY2_SC),
    (CY1, ASC2),
    (CY1_SC, ASC2),

    #(FIG1, FIG2),
    (FIG1, CY2),
    (CY1, FIG2),
    
    #(SUPS1, SUPS2),
    #(SINF1, SINF2),
    (CY1, SUPS2),
    (CY1, SINF2),
    (SUPS1, CY2),
    (SINF1, CY2),
    
    #(NUMR1, NUMR2),
    (CY1, NUMR2),
    (CY1, DNOM2),
    (NUMR1, CY2),
    (DNOM1, CY2),
    
    #(ONUM1, ONUM2),
    (ONUM1, CY2),
    (CY1, ONUM2),

    # Greek
    (GR1, GR2),
    (GR1_SC, GR2_SC),
    (GR1, GR1_SC),

    #(ASC1, ASC2),
    (ASC1, GR2),
    (ASC1, GR2_SC),
    (GR1, ASC2),
    (GR1_SC, ASC2),

    #(FIG1, FIG2),
    (FIG1, GR2),
    (GR1, FIG2),
    
    #(SUPS1, SUPS2),
    #(SINF1, SINF2),
    (GR1, SUPS2),
    (GR1, SINF2),
    (SUPS1, GR2),
    (SINF1, GR2),
    
    #(NUMR1, NUMR2),
    (GR1, NUMR2),
    (GR1, DNOM2),
    (NUMR1, GR2),
    (DNOM1, GR2),
    
    #(ONUM1, ONUM2),
    (ONUM1, GR2),
    (GR1, ONUM2),

)


GROUP_IGNORE = ('tnum', 'cmb', 'comb', 'mod', 'component',) # Always ignore glyphs that include these patterns

# This table is now available as kerningManager.groupBaseGlyphs.
#GROUP_BASE_GLYPHS = {
#==== Proforma_Pro-Regular_MA76.ufo
#Groups: 982 Kerning: 1786, Proforma_Pro-Regular_MA76.ufo
#cy1': {'Pemiddlehook_cy', 'Ha_cy.sc', 'enhook_cy', 'Hahook_cy', 'Ha_cy', 'Er_cy.sc', 'ustrait_cy', 'Ef_cy', 'E_cy.sc', 'Dzeabkh_cy.sc', 'Dze_cy.sc', 'che_cy', 'Enhook_cy.sc', 'Shha_cy.sc', 'ge_cy.loclBGR', 'Dzeabkh_cy', 'Hahook_cy.sc', 'Kahook_cy.sc', 'hahook_cy', 'aie_cy', 'Cheabkhasian_cy.sc', 'De_cy.loclBGR.sc', 'Te_cy.sc', 'e_cy', 'Be_cy.sc', 'Ve_cy', 'Che_cy', 'yi_cy', 'dje_cy', 'Enhook_cy', 'ka_cy', 'pe_cy.loclBGR', 'dzeabkh_cy', 'hardsign_cy.loclBGR', 'Enghe_cy', 'enghe_cy', 'ze_cy', 'Aie_cy.sc', 'Pemiddlehook_cy.sc', 'Che_cy.sc', 'hardsign_cy', 'u_cy', 'Haabkhasian_cy', 'E_cy', 've_cy.loclBGR', 'be_cy.loclSRB', 'Er_cy', 'U_cy.sc', 'Ka_cy', 'Ef_cy.sc', 'ha_cy', 'de_cy.loclBGR', 'Dje_cy.sc', 'dze_cy', 'Hardsign_cy.sc', 'Yi_cy.sc', 'U_cy', 'A_cy.sc', 'be_cy', 'Ustrait_cy.sc', 'palochka_cy', 'el_cy.loclBGR', 'Haabkhasian_cy.sc', 'Shha_cy', 'Ustrait_cy', 'Enghe_cy.sc', 'De_cy.loclBGR', 'haabkhasian_cy', 've_cy', 'A_cy', 'kahook_cy', 'Kahook_cy', 'Dze_cy', 'Chedescender_cy', 'Ka_cy.sc', 'che_cy.loclBGR', 'ghemiddlehook_cy', 'Edieresis_cy', 'Hardsign_cy', 'chedescender_cy', 'er_cy', 'Cheabkhasian_cy', 'Chedescender_cy.sc', 'Dje_cy', 'Aie_cy', 'Be_cy', 'a_cy', 'Ve_cy.sc', 'Edieresis_cy.sc', 'Te_cy'}, 'lt1': {'F.sc', 'Eng', 'Yinferior', 'A', 'P', 'Alpha_latin', 'bsuperior', 'numero', 'Ldot.sc', 'Uinferior', 'Asuperior', 'C', 'Germandbls', 'd', 'f', 'eopen', 'usuperior', 'Thorn.sc', 'G.sc', 'Tsuperior', 'Rsuperior', 'Usuperior', 'k', 'Jsuperior', 'mturned', 'Ldot', 'Eng.sc', 'qsuperior', 'isuperior', 'P.sc', 'ezhreversed', 'Ezh.sc', 'Ohorn', 'Ainferior', 'tinferior', 'Khook.sc', 'cinferior', 'AE', 'ksuperior', 'Hinferior', 'gsuperior', 'Dz', 'Lj', 'gamma_latin', 'Fsuperior', 'g', 'whook', 'Chi_latin', 'Aturned', 'ainferior', 'U.sc', 'Ezhreversed.sc', 'Vinferior', 'Jcrossedtail', 'R', 'ustroke', 'dhook', 'AE.sc', 'Nlongrightleg', 'h', 'hsuperior', 'y', 'r', 'Dinferior', 'ldot', 'R.sc', 'Jcrossedtail.sc', 'Csuperior', 'asuperior', 'zinferior', 'Qhooktail', 'D.sc', 'F', 'Khook', 'fsuperior', 'ae', 'Lcaron.sc', 'DZ.sc', 'idotless', 'Gscript', 'Thorn', 't', 'Linferior', 'finferior', 'vturned', 'hinferior', 'eng', 'Hsuperior', 'Ezhreversed', 'fi', 'T.sc', 'jinferior', 'kinferior', 'ohorn', 'Zsuperior', 'dtail', 'Whook', 'Chi_latin.sc', 'Y', 'tcaron', 'chook', 'Ninferior', 'Pinferior', 'egraveinferior', 'qinferior', 'rinferior', 'T', 'W', 'C.sc', 'G', 'tsuperior', 'ginferior', 'Ginferior', 'v', 'zsuperior', 'Ereversed.sc', 'dsuperior', 'yturned', 'Einferior', 'Jinferior', 'Lsuperior', 'vsuperior', 'Tinferior', 'Gsuperior', 'Nsuperior', 'Esuperior', 'hturned', 'ezh', 'Cinferior', 'DZ', 'uinferior', 'Ghook', 'esh', 'Sinferior', 'idotlesshorn', 'dcaron', 'B', 'Ereversed', 'Ssuperior', 'jcrossedtail', 'Eopen.sc', 'Kinferior', 'dinferior', 'W.sc', 'S', 'jsuperior', 'Ysuperior', 'J.base.sc', 'Vsuperior', 'B.sc', 'Dsuperior', 'Germandbls.sc', 'Whook.sc', 'Eopen', 'Ezh', 'Uhorn', 'vinferior', 'lbar', 'U', 'eshreversedloop', 'Y.sc', 'Uhorn.sc', 'iinferior', 'A.sc', 'csuperior', 'L', 'Psuperior', 'chi_latin', 'a', 'Bsuperior', 'V.sc', 'iota_latin', 'rsuperior', 'b', 'egravesuperior', 'Zinferior', 'sinferior', 'Finferior', 'c', 'Ohm', 'Chook', 'J.base', 'Creversed', 'binferior', 'ssuperior', 'Ohorn.sc', 'Binferior', 'L.sc', 'Lcaron', 'Rinferior', 'Ksuperior'}, 'sc_cy1': {'De_cy.loclBGR.sc', 'Te_cy.sc', 'Be_cy.sc', 'Ha_cy.sc', 'U_cy.sc', 'Ef_cy.sc', 'Dje_cy.sc', 'Er_cy.sc', 'Ka_cy.sc', 'Hardsign_cy.sc', 'Yi_cy.sc', 'A_cy.sc', 'Ustrait_cy.sc', 'Haabkhasian_cy.sc', 'Chedescender_cy.sc', 'E_cy.sc', 'Dzeabkh_cy.sc', 'Dze_cy.sc', 'Enghe_cy.sc', 'Enhook_cy.sc', 'Aie_cy.sc', 'Shha_cy.sc', 'Hahook_cy.sc', 'Pemiddlehook_cy.sc', 'Kahook_cy.sc', 'Ve_cy.sc', 'Che_cy.sc', 'Edieresis_cy.sc', 'Cheabkhasian_cy.sc'}, 'sc_lt1': {'F.sc', 'J.base.sc', 'B.sc', 'AE.sc', 'Germandbls.sc', 'Whook.sc', 'Ldot.sc', 'C.sc', 'R.sc', 'Jcrossedtail.sc', 'Ereversed.sc', 'Thorn.sc', 'G.sc', 'D.sc', 'Y.sc', 'Uhorn.sc', 'Lcaron.sc', 'A.sc', 'Eng.sc', 'DZ.sc', 'V.sc', 'P.sc', 'Ezh.sc', 'Khook.sc', 'T.sc', 'Eopen.sc', 'W.sc', 'Ohorn.sc', 'L.sc', 'Chi_latin.sc', 'U.sc', 'Ezhreversed.sc'}, 'gr1': {'eta', 'tau', 'Rho.sc', 'Psi.sc', 'kaiSymbol', 'Epsilon', 'KaiSymbol.sc', 'Omicron', 'Beta', 'delta', 'Gamma.sc', 'xi', 'nu', 'sigma', 'Beta.sc', 'Psi', 'iota', 'Nu', 'Upsilon', 'Eta.sc', 'Eta', 'Zeta', 'lambda', 'zeta', 'Nu.sc', 'KaiSymbol', 'Zeta.sc', 'iotadieresis', 'lowernumeral_greek', 'theta', 'Phi.sc', 'Rho', 'Upsilon.sc', 'numeral_greek', 'Omicron.sc', 'Omega.sc', 'epsilon', 'sigmafinal', 'Omega', 'beta', 'Sigmafinal.sc', 'Phi', 'chi', 'alpha', 'gamma', 'Epsilon.sc', 'Gamma', 'pi', 'Alpha', 'Chi.sc', 'Chi'}, 'sc1': {'nine.sc', 'three.sc', 'zero.sc', 'one.sc', 'seven.sc', 'six.sc', 'Alpha.sc', 'eight.sc', 'five.sc', 'four.sc', 'two.sc'}, 'sc_gr1': {'Omicron.sc', 'Omega.sc', 'Gamma.sc', 'Nu.sc', 'Psi.sc', 'Rho.sc', 'Sigmafinal.sc', 'Beta.sc', 'Zeta.sc', 'Epsilon.sc', 'KaiSymbol.sc', 'Chi.sc', 'Phi.sc', 'Eta.sc', 'Upsilon.sc'}, 'asc1': {'braceright.sc', 'braceright', 'exclamdown', 'bracketleft', 'bullet', 'degree.sc', 'partialdiff', 'slash', 'clickretroflex', 'Esh', 'exclamdown.sc', 'space', 'bracketright.sc', 'horizontalbar', 'percent', 'quotedblright', 'copyright', 'emdash', 'asterisk', 'guillemotright', 'radical', 'backslash', 'questiondown', 'apple', 'at', 'dotaccent', 'bracketright', 'braceleft', 'parenright', 'Glottalstop', 'sterling', 'florin', 'tilde', 'bar', 'Saltillo', 'glottalstopsmall', 'bracketleft.sc', 'exclam.sc', 'parenleft', 'parenleft.sc', 'question.sc', 'questiondown.sc', 'underscore', 'yen', 'cent', 'backslash.sc', 'guillemotleft', 'comma', 'quotedblleft', 'section.sc', 'section', 'asciicircum', 'glottalstopreversed', 'quotedblrightreversed', 'parenright.sc', 'ampersand.sc', 'anoteleia', 'dollar', 'arrowNE', 'periodcentered', 'trademark', 'braceleft.sc', 'asciitilde', 'ordfeminine', 'slash.sc', 'ampersand', 'degree', 'currency', 'newsheqel', 'colon'}, 'uc1': {'periodcentered.uc', 'emdash.uc', 'questiondown.uc', 'bullet.uc', 'exclamdown.uc', 'guillemotright.uc', 'guillemotleft.uc'}, 'superior1': {'eurosuperior', 'sevensuperior', 'sterlingsuperior', 'onesuperior', 'eightsuperior', 'colonsuperior', 'quotedblleftsuperior', 'centsuperior'}, 'inferior1': {'commainferior', 'eightinferior', 'seveninferior', 'oneinferior'}, 'fig1': {'six', 'zero', 'one', 'eight', 'fraction', 'seven', 'nine', 'two', 'five', 'three', 'four'}, 'onum1': {'seven.onum', 'eight.onum', 'nine.onum', 'six.onum', 'two.onum', 'zero.onum', 'five.onum', 'three.onum', 'one.onum', 'four.onum'}, 'dnom1': {'oneseventh', 'one.dnom', 'eight.dnom'}, 'numr1': {'eight.numr', 'seven.numr', 'one.numr'}, 'lt2': {'Dafrican.sc', 'Yinferior', 'A', 'Alpha_latin', 'henghook', 'bsuperior', 'Uinferior', 'Asuperior', 'usuperior', 'eturned', 'eopen', 'f', 'Dafrican', 'Hturned.sc', 'Tsuperior', 'xsuperior', 'Usuperior', 'Jsuperior', 'p', 'Bhook', 'isuperior', 'Hturned', 'oopen', 'ezhreversed', 'Ezh.sc', 'Ainferior', 'tinferior', 'rhook', 'AE', 'Oopen.sc', 'Xinferior', 'gamma_latin', 'g', 'Chi_latin', 'Aturned', 'ainferior', 'U.sc', 'Ezhreversed.sc', 'Vinferior', 'Jcrossedtail', 'ustroke', 'AE.sc', 'h', 'hsuperior', 'yinferior', 'Yogh', 'Rtail', 's', 'Jcrossedtail.sc', 'Csuperior', 'asuperior', 'zinferior', 'Z.sc', 'idotless', 'jdotless', 't', 'vturned', 'hinferior', 'ysuperior', 'eng', 'Ezhreversed', 'T.sc', 'jinferior', 'msuperior', 'Zsuperior', 'aturned', 'Chi_latin.sc', 'Y', 'Iotaafrican', 'j', 'T', 'W', 'C.sc', 'tsuperior', 'minferior', 'v', 'zsuperior', 'Ereversed.sc', 'yturned', 'Jinferior', 'bhook', 'vsuperior', 'Tinferior', 'uinferior', 'ezh', 'Cinferior', 'Sinferior', 'B', 'Ereversed', 'Ssuperior', 'x', 'jcrossedtail', 'Eopen.sc', 'Bhook.sc', 'W.sc', 'S', 'jsuperior', 'Ysuperior', 'J.base.sc', 'Vsuperior', 'B.sc', 'Fhook', 'Rtail.sc', 'alpha_latin', 'Oopen', 'Eopen', 'liraTurkish', 'i', 'Ezh', 'Xsuperior', 'vinferior', 'lbar', 'U', 'Y.sc', 'iinferior', 'lbelt', 'A.sc', 'Z', 'chi_latin', 'a', 'Bsuperior', 'V.sc', 'iota_latin', 'b', 'xinferior', 'Zinferior', 'Fstroke', 'sinferior', 'Fhook.sc', 'beta_latin', 'Ohm', 'J.base', 'Creversed', 'binferior', 'ssuperior', 'Binferior', 'S.sc', 'Fstroke.sc', 'z'}, 'sc_lt2': {'J.base.sc', 'Dafrican.sc', 'B.sc', 'AE.sc', 'Rtail.sc', 'C.sc', 'Jcrossedtail.sc', 'Ereversed.sc', 'Hturned.sc', 'Y.sc', 'A.sc', 'Z.sc', 'V.sc', 'Ezh.sc', 'Fhook.sc', 'Oopen.sc', 'T.sc', 'Eopen.sc', 'Bhook.sc', 'W.sc', 'Chi_latin.sc', 'S.sc', 'Fstroke.sc', 'U.sc', 'Ezhreversed.sc'}, 'cy2': {'E_cy', 'A_cy', 'De_cy.loclBGR.sc', 've_cy.loclBGR', 'edieresis_cy', 'ii_cy.loclBGR', 'Be_cy.sc', 'Ha_cy.sc', 'de_cy', 'be_cy.loclSRB', 'U_cy.sc', 'ia_cy', 'El_cy.sc', 'gehookstroke_cy', 'Ef_cy.sc', 'Dze_cy', 'Che_cy', 'Ia_cy', 'Ha_cy', 'Dje_cy.sc', 'Gehookstroke_cy.sc', 'ha_cy', 'ze_cy.loclBGR', 'dze_cy', 'Yi_cy.sc', 'yi_cy', 'U_cy', 'A_cy.sc', 'be_cy', 'Ustrait_cy.sc', 'dje_cy', 'schwa_cy', 'ustrait_cy', 'De_cy.sc', 'el_cy.loclBGR', 'Cheabkhasian_cy', 'er_cy', 'Dje_cy', 'zhe_cy', 'Schwa_cy.sc', 'dzhe_cy', 'dzeabkh_cy', 'Ef_cy', 'E_cy.sc', 'El_cy', 'cheabkhasian_cy', 'Aie_cy', 'De_cy', 'Be_cy', 'Zhe_cy', 'a_cy', 'Ustrait_cy', 'Dzeabkh_cy.sc', 'Dze_cy.sc', 'che_cy', 'Aie_cy.sc', 'el_cy', 'Dzeabkh_cy', 'ge_cy.loclBGR', 'Schwa_cy', 'Che_cy.sc', 'hardsign_cy', 'Ia_cy.sc', 'Zhe_cy.sc', 'Gehookstroke_cy', 'De_cy.loclBGR', 'Cheabkhasian_cy.sc', 'u_cy'}, 'sc_cy2': {'De_cy.loclBGR.sc', 'Be_cy.sc', 'Ha_cy.sc', 'U_cy.sc', 'El_cy.sc', 'Ef_cy.sc', 'Dje_cy.sc', 'Gehookstroke_cy.sc', 'Yi_cy.sc', 'A_cy.sc', 'Ustrait_cy.sc', 'De_cy.sc', 'Schwa_cy.sc', 'E_cy.sc', 'Dzeabkh_cy.sc', 'Dze_cy.sc', 'Aie_cy.sc', 'Che_cy.sc', 'Ia_cy.sc', 'Zhe_cy.sc', 'Cheabkhasian_cy.sc'}, 'gr2': {'eta', 'tau', 'kaiSymbol', 'rho', 'Omicron', 'Beta', 'delta', 'xi', 'nu', 'Upsilontonos', 'Psi', 'iota', 'Tau', 'Upsilon', 'Zeta', 'lambda', 'zeta', 'upsilon', 'phi', 'lowernumeral_greek', 'theta', 'numeral_greek', 'Alphatonos', 'Epsilontonos', 'Xi', 'epsilon', 'Omega', 'psi', 'beta', 'Phi', 'chi', 'alpha', 'gamma', 'pi', 'omega', 'Alpha', 'Sigma', 'Chi'}, 'sc2': {'nine.sc', 'Omegatonos.sc', 'Xi.sc', 'Psi.sc', 'Chi.sc', 'six.sc', 'Sigma.sc', 'zero.sc', 'three.sc', 'Alphatonos.sc', 'Tau.sc', 'Beta.sc', 'Upsilontonos.sc', 'five.sc', 'Etatonos.sc', 'parenleft.sc', 'one.sc', 'seven.sc', 'Zeta.sc', 'Phi.sc', 'Upsilon.sc', 'parenright.sc', 'four.sc', 'Omega.sc', 'Sigmafinal.sc', 'slash.sc', 'Alpha.sc', 'eight.sc', 'two.sc'}, 'asc2': {'braceright.sc', 'braceright', 'exclamdown', 'rupeeIndian', 'bracketleft', 'Euro', 'bullet', 'degree.sc', 'partialdiff', 'Napostrophe.sc', 'slash', 'clickretroflex', 'Esh', 'exclamdown.sc', 'space', 'bracketright.sc', 'horizontalbar', 'circumflex', 'percent', 'copyright', 'emdash', 'numbersign', 'asterisk', 'guillemotright', 'radical', 'backslash', 'questiondown', 'apple', 'at', 'Glottalstop', 'bracketright', 'braceleft', 'parenright', 'sterling', 'florin', 'bar', 'Saltillo', 'glottalstopsmall', 'bracketleft.sc', 'exclam.sc', 'parenleft', 'question.sc', 'questiondown.sc', 'underscore', 'ruble', 'cent', 'backslash.sc', 'yen', 'guillemotleft', 'comma', 'quotedblleft', 'section.sc', 'section', 'asciicircum', 'numbersign.sc', 'glottalstopreversed', 'quotedblrightreversed', 'ampersand.sc', 'anoteleia', 'dollar', 'arrowNE', 'periodcentered', 'trademark', 'paragraph', 'braceleft.sc', 'asciitilde', 'ordfeminine', 'ampersand', 'degree', 'currency', 'newsheqel', 'colon', 'creversed'}, 'uc2': {'periodcentered.uc', 'arrowNE.uc', 'emdash.uc', 'questiondown.uc', 'bullet.uc', 'exclamdown.uc', 'guillemotright.uc', 'guillemotleft.uc'}, 'inferior2': {'commainferior', 'finferior', 'oneinferior', 'fourinferior', 'cinferior', 'ginferior', 'eightinferior'}, 'superior2': {'gsuperior', 'eurosuperior', 'fsuperior', 'foursuperior', 'onesuperior', 'eightsuperior', 'colonsuperior', 'csuperior'}, 'fig2': {'six', 'zero', 'one', 'eight', 'fraction', 'seven', 'nine', 'two', 'five', 'three', 'four'}, 'onum2': {'seven.onum', 'eight.onum', 'nine.onum', 'six.onum', 'two.onum', 'zero.onum', 'five.onum', 'three.onum', 'one.onum', 'four.onum'}, 'dnom2': {'four.dnom', 'one.dnom', 'eight.dnom'}, 'numr2': {'eight.numr', 'four.numr', 'one.numr'},
#}

