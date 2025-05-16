# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................

from copy import deepcopy

if __name__ == '__main__': # Used for doc tests to find assistantLib
    import os, sys
    PATH = '/'.join(__file__.split('/')[:-4]) # Relative path to this respository that holds AssistantLib
    if not PATH in sys.path:
        sys.path.append(PATH)

from assistantLib.assistantParts.glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_ etc.

CYRILLIC_SET_NAME = 'Cyrillic'
CYRILLIC_SET_NAME_ITALIC = 'Cyrillic Italic'

# The "c" attribtes are redundant, if the @uni or @hex are defined, but they offer easy searching in the source by char.

CYRILLIC_SET = {

    #   A

   'A_cy': GD(name='A_cy', uni=0x0410, hex='0410', c='А', l='A', r='A', base='A', anchors=['top', 'middle', 'bottom'], gid=661),
   'Abreve_cy': GD(name='Abreve_cy', uni=0x04D0, hex='04D0', c='Ӑ', l='A', r='A', base='A', accents=['brevecmb_cy.uc'], anchors=['top', 'middle', 'bottom'], gid=853),
   'Adieresis_cy': GD(name='Adieresis_cy', uni=0x04D2, hex='04D2', c='Ӓ', l='A', r='A', base='A', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=855),
   'Aie_cy': GD(name='Aie_cy', uni=0x04D4, hex='04D4', c='Ӕ', l='AE', r='E', base='AE', anchors=['top', 'middle', 'bottom'], gid=857),

    #   B

   'Be_cy': GD(name='Be_cy', uni=0x0411, hex='0411', c='Б', l='H', gid=662),

    #   C

   'Che_cy': GD(name='Che_cy', uni=0x0427, hex='0427', c='Ч', r='H', anchors=['top'], gid=684),
   'Cheabkhasian_cy': GD(name='Cheabkhasian_cy', uni=0x04BC, hex='04BC', c='Ҽ', l='o', r='O', gid=833),
   'Chedescender_cy': GD(name='Chedescender_cy', uni=0x04B6, hex='04B6', c='Ҷ', l='Che_cy', r='Tse_cy', gid=827),
   'Chedescenderabkhasian_cy': GD(name='Chedescenderabkhasian_cy', uni=0x04BE, hex='04BE', c='Ҿ', l='Cheabkhasian_cy', r='Cheabkhasian_cy', base='Cheabkhasian_cy', gid=835),
   #'Chedescenderabkhasian_cy.component': GD(name='Chedescenderabkhasian_cy.component', gid=1599),
   'Chedieresis_cy': GD(name='Chedieresis_cy', uni=0x04F4, hex='04F4', c='Ӵ', l='Che_cy', r='H', base='Che_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=889),
   'Chekhakassian_cy': GD(name='Chekhakassian_cy', uni=0x04CB, hex='04CB', c='Ӌ', l='Che_cy', r='H', gid=848),
   'Cheverticalstroke_cy': GD(name='Cheverticalstroke_cy', uni=0x04B8, hex='04B8', c='Ҹ', l='Che_cy', r='H', base='Che_cy', anchors=['top'], gid=829),

    #   D

   'De_cy': GD(name='De_cy', uni=0x0414, hex='0414', c='Д', l='off', r='Tse_cy', gid=665),
   'De_cy.loclBGR': GD(name='De_cy.loclBGR'), 

   'Dje_cy': GD(name='Dje_cy', uni=0x0402, hex='0402', c='Ђ', l='T', gid=647),
   'Dze_cy': GD(name='Dze_cy', uni=0x0405, hex='0405', c='Ѕ', l='S', r='S', base='S', anchors=['top', 'middle', 'bottom'], gid=650),
   'Dzhe_cy': GD(name='Dzhe_cy', uni=0x040F, hex='040F', c='Џ', l='H', r='H', gid=660),

    #   E

   'E_cy': GD(name='E_cy', uni=0x0404, hex='0404', c='Є', l='O', r='C', gid=649),
   'Edieresis_cy': GD(name='Edieresis_cy', uni=0x04EC, hex='04EC', c='Ӭ', l='Ereversed_cy', r='O', anchorTopX='Ereversed_cy', anchorTopY='TopY', base='Ereversed_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=881),
   'Ef_cy': GD(name='Ef_cy', uni=0x0424, hex='0424', c='Ф', l='O', l2r='Ef_cy', gid=681),
   #'Eiotified_cy': GD(name='Eiotified_cy', uni=0x0464, hex='0464', c='Ѥ', l='H', r='C', gid=745),
   'El_cy': GD(name='El_cy', uni=0x041B, hex='041B', c='Л', r='H', gid=672),
   'El_cy.loclBGR': GD(name='El_cy.loclBGR', l='A', r='A', base='Lambda'),
   'Eltail_cy': GD(name='Eltail_cy', uni=0x04C5, hex='04C5', c='Ӆ', l='El_cy', r='Iishorttail_cy', base='El_cy', anchorTopY='El_cy', accents=['tail.component_cy.case'], gid=842),
   'Em_cy': GD(name='Em_cy', uni=0x041C, hex='041C', c='М', l='H', r='H', base='M', anchors=['top', 'middle', 'bottom'], gid=673),
   'Emtail_cy': GD(name='Emtail_cy', uni=0x04CD, hex='04CD', c='Ӎ', l='H', r='Iishorttail_cy', base='M', anchorBottomY='M', accents=['tail.component_cy.case'], anchors=['top', 'middle', 'bottom'], gid=850),
   'En_cy': GD(name='En_cy', uni=0x041D, hex='041D', c='Н', l='H', r='H', base='H', anchors=['top', 'middle', 'bottom'], gid=674),
   'Endescender_cy': GD(name='Endescender_cy', uni=0x04A2, hex='04A2', c='Ң', l='H', r='Tse_cy', gid=807),
   'Enghe_cy': GD(name='Enghe_cy', uni=0x04A4, hex='04A4', c='Ҥ', l='H', r='Ge_cy', gid=809),
   'Enhook_cy': GD(name='Enhook_cy', uni=0x04C7, hex='04C7', c='Ӈ', l='H', r='J', gid=844),
   'Entail_cy': GD(name='Entail_cy', uni=0x04C9, hex='04C9', c='Ӊ', l='H', r='Iishorttail_cy', base='H', anchorBottomY='H', accents=['tail.component_cy.case'], anchors=['top', 'middle', 'bottom'], gid=846),
   'Er_cy': GD(name='Er_cy', uni=0x0420, hex='0420', c='Р', l='H', r='P', base='P', anchors=['top', 'middle', 'bottom'], gid=677),
   'Ereversed_cy': GD(name='Ereversed_cy', uni=0x042D, hex='042D', c='Э', r='O', anchorTopX='TopX', anchorTopY='TopY', anchors=['top'], gid=690),
   'Ertick_cy': GD(name='Ertick_cy', uni=0x048E, hex='048E', c='Ҏ', l='H', r='P', base='P', gid=787),
   'Es_cy': GD(name='Es_cy', uni=0x0421, hex='0421', c='С', l='C', r='C', base='C', anchors=['top', 'middle', 'bottom'], gid=678),
   'Esdescender_cy': GD(name='Esdescender_cy', uni=0x04AA, hex='04AA', c='Ҫ', l='O', r='C', base='C', gid=815),

    #   F

   #'Fita_cy': GD(name='Fita_cy', uni=0x0472, hex='0472', c='Ѳ', l='O', r='O', base='Obarred_cy', gid=759),

    #   G

   'Ge_cy': GD(name='Ge_cy', uni=0x0413, hex='0413', c='Г', l='H', base='Gamma', anchors=['top'], gid=664),
   'Gedescender_cy': GD(name='Gedescender_cy', uni=0x04F6, hex='04F6', c='Ӷ', l='H', r='Ge_cy', gid=891),
   'Ghemiddlehook_cy': GD(name='Ghemiddlehook_cy', uni=0x0494, hex='0494', c='Ҕ', l='H', r='o', gid=793),
   'Ghestroke_cy': GD(name='Ghestroke_cy', uni=0x0492, hex='0492', c='Ғ', l='Eth', r='Ge_cy', base='Ge_cy', gid=791),
   'Gheupturn_cy': GD(name='Gheupturn_cy', uni=0x0490, hex='0490', c='Ґ', l='H', r='Ge_cy', gid=789),
   'Gje_cy': GD(name='Gje_cy', uni=0x0403, hex='0403', c='Ѓ', l='H', r='Ge_cy', base='Ge_cy', accents=['acutecmb.uc'], anchors=['top'], gid=648),
   'Gehookstroke_cy': GD(name='Gehookstroke_cy', uni=0x04FA, hex='04FA', c='Ӻ', l='H', r='Ge_cy', anchors=['top'], gid=648),

    #   H

   'Ha_cy': GD(name='Ha_cy', uni=0x0425, hex='0425', c='Х', l='X', r='X', base='X', anchors=['top', 'middle', 'bottom'], gid=682),
   'Haabkhasian_cy': GD(name='Haabkhasian_cy', uni=0x04A8, hex='04A8', c='Ҩ', l='o', r='c', gid=813),
   'Hadescender_cy': GD(name='Hadescender_cy', uni=0x04B2, hex='04B2', c='Ҳ', l='X', r='Kadescender_cy', gid=823),
   'Hahook_cy': GD(name='Hahook_cy', uni=0x04FC, hex='04FC', c='Ӽ', l='X', r='X', gid=897),
   'Hardsign_cy': GD(name='Hardsign_cy', uni=0x042A, hex='042A', c='Ъ', l='T', r='Softsign_cy', gid=687),
   'Hastroke_cy': GD(name='Hastroke_cy', uni=0x04FE, hex='04FE', c='Ӿ', l='X', r='X', base='X', gid=899),

    #   I

   'I_cy': GD(name='I_cy', uni=0x0406, hex='0406', l='I', r='I', base='I', anchors=['top', 'middle', 'bottom'], gid=651),
   'Ia_cy': GD(name='Ia_cy', uni=0x042F, hex='042F', c='Я', r='H', gid=692),
   'Idieresis_cy': GD(name='Idieresis_cy', uni=0x04E4, hex='04E4', c='Ӥ', bl='H', r='H', base='Ii_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=873),
   'Ie_cy': GD(name='Ie_cy', uni=0x0415, hex='0415', c='Е', bl='H', r='E', base='E', anchors=['top', 'middle', 'bottom'], gid=666),
   'Iebreve_cy': GD(name='Iebreve_cy', uni=0x04D6, hex='04D6', c='Ӗ', l='E', r='E', base='E', accents=['brevecmb_cy.uc'], anchors=['top', 'middle', 'bottom'], gid=859),
   'Iegrave_cy': GD(name='Iegrave_cy', uni=0x0400, hex='0400', c='Ѐ', l='E', r='E', base='E', accents=['gravecmb.uc'], anchors=['top', 'middle', 'bottom'], gid=645),
   'Ii_cy': GD(name='Ii_cy', uni=0x0418, hex='0418', c='И', l='H', r='H', anchors=['top'], gid=669),
   'Iigrave_cy': GD(name='Iigrave_cy', uni=0x040D, hex='040D', c='Ѝ', bl='H', r='H', base='Ii_cy', accents=['gravecmb.uc'], anchors=['top'], gid=658),
   'Iishort_cy': GD(name='Iishort_cy', uni=0x0419, hex='0419', c='Й', bl='H', r='H', base='Ii_cy', accents=['brevecmb_cy.uc'], anchors=['top'], gid=670),
   'Iishorttail_cy': GD(name='Iishorttail_cy', uni=0x048A, hex='048A', c='Ҋ', bl='H', r='off', base='Iishort_cy', accents=['tail.component_cy.case'], gid=783),
   'Imacron_cy': GD(name='Imacron_cy', uni=0x04E2, hex='04E2', c='Ӣ', l='H', r='H', base='Ii_cy', accents=['macroncmb.uc'], anchors=['top'], gid=871),
   'Io_cy': GD(name='Io_cy', uni=0x0401, hex='0401', c='Ё', l='E', r='E', base='E', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=646),
   'Iu_cy': GD(name='Iu_cy', uni=0x042E, hex='042E', c='Ю', l='H', r='O', gid=691),
   #'Izhitsa_cy': GD(name='Izhitsa_cy', uni=0x0474, hex='0474', c='Ѵ', l='V', r='V', anchors=['top'], gid=761),
   #'Izhitsadblgrave_cy': GD(name='Izhitsadblgrave_cy', uni=0x0476, hex='0476', c='Ѷ', l='V', r='Izhitsa_cy', base='Izhitsa_cy', accents=['dblgravecmb.uc'], anchors=['top'], gid=763),

    #   J

   'Je_cy': GD(name='Je_cy', uni=0x0408, hex='0408', c='Ј', w='J', bl='J', base='J', anchors=['top', 'middle', 'bottom'], gid=653),

    #   K

   'Ka_cy': GD(name='Ka_cy', uni=0x041A, hex='041A', c='К', l='H', r='K', base='K', anchors=['top', 'middle', 'bottom'], gid=671),
   'Kabashkir_cy': GD(name='Kabashkir_cy', uni=0x04A0, hex='04A0', c='Ҡ', l='T', r='K', gid=805),
   'Kadescender_cy': GD(name='Kadescender_cy', uni=0x049A, hex='049A', c='Қ', l='H', r='Zhedescender_cy', gid=799),
   'Kahook_cy': GD(name='Kahook_cy', uni=0x04C3, hex='04C3', c='Ӄ', l='H', gid=840),
   'Kastroke_cy': GD(name='Kastroke_cy', uni=0x049E, hex='049E', c='Ҟ', l='Eth', r='K', gid=803),
   'Kaverticalstroke_cy': GD(name='Kaverticalstroke_cy', uni=0x049C, hex='049C', c='Ҝ', l='H', r='K', gid=801),
   'Kje_cy': GD(name='Kje_cy', uni=0x040C, hex='040C', c='Ќ', l='H', r='K', base='K', accents=['acutecmb.uc'], anchors=['top', 'middle', 'bottom'], gid=657),
   #'Koppa_cy': GD(name='Koppa_cy', uni=0x0480, hex='0480', c='Ҁ', l='O', r='C', gid=773),
   #'Ksi_cy': GD(name='Ksi_cy', uni=0x046E, hex='046E', c='Ѯ', r='Ze_cy', gid=755),

    #   L

   'Lje_cy': GD(name='Lje_cy', uni=0x0409, hex='0409', c='Љ', l='El_cy', r='Softsign_cy', gid=654),

    #   M

    #   N

   'Nje_cy': GD(name='Nje_cy', uni=0x040A, hex='040A', c='Њ', l='H', r='Softsign_cy', gid=655),

    #   O

   'O_cy': GD(name='O_cy', uni=0x041E, hex='041E', c='О', l='O', r='O', base='O', anchors=['top', 'middle', 'bottom'], gid=675),
   'Obarred_cy': GD(name='Obarred_cy', uni=0x04E8, hex='04E8', c='Ө', l='O', r='O', base='O', anchors=['top'], gid=877),
   'Obarreddieresis_cy': GD(name='Obarreddieresis_cy', uni=0x04EA, hex='04EA', c='Ӫ', l='O', r='O', base='Obarred_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=879),
   'Odieresis_cy': GD(name='Odieresis_cy', uni=0x04E6, hex='04E6', c='Ӧ', l='O', r='O', base='O', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=875),
   #'Omega_cy': GD(name='Omega_cy', uni=0x0460, hex='0460', c='Ѡ', l='O', r='O', anchors=['top'], gid=741),

    #   P

   'Palochka_cy': GD(name='Palochka_cy', uni=0x04C0, hex='04C0', c='Ӏ', l='I', r='I', base='I', anchors=['top', 'middle', 'bottom'], gid=837),
   'Pe_cy': GD(name='Pe_cy', uni=0x041F, hex='041F', c='П', l='H', r='H', base='Pi', gid=676),
   'Pedescender_cy': GD(name='Pedescender_cy', uni=0x0524, hex='0524', c='Ԥ', l='H', r='Tse_cy', gid=901),
   #'Pedescender_cy.component': GD(name='Pedescender_cy.component', w=0, gid=1605),
   'Pemiddlehook_cy': GD(name='Pemiddlehook_cy', uni=0x04A6, hex='04A6', c='Ҧ', l='H', r='o', gid=811),
   #'Psi_cy': GD(name='Psi_cy', uni=0x0470, hex='0470', c='Ѱ', l='V', r='U', base='Psi', gid=757),

    #   Q

    #   R

    #   S

   'Schwa_cy': GD(name='Schwa_cy', uni=0x04D8, hex='04D8', c='Ә', r='O', base='Schwa', anchors=['top'], gid=861),
   'Schwadieresis_cy': GD(name='Schwadieresis_cy', uni=0x04DA, hex='04DA', c='Ӛ', l='Schwa_cy', r='O', base='Schwa', accents=['dieresiscmb.uc'], anchors=['top'], gid=863),
   'Semisoftsign_cy': GD(name='Semisoftsign_cy', uni=0x048C, hex='048C', c='Ҍ', r='Softsign_cy', base='Softsign_cy', gid=785),
   'Sha_cy': GD(name='Sha_cy', uni=0x0428, hex='0428', c='Ш', l='H', r='H', gid=685),
   'Shcha_cy': GD(name='Shcha_cy', uni=0x0429, hex='0429', c='Щ', l='H', r='Tse_cy', gid=686),
   #'Shei-coptic': GD(name='Shei-coptic', uni=0x03E2, hex='03E2', l='H', r='H', c='Ϣ', gid=615),
   'Shha_cy': GD(name='Shha_cy', uni=0x04BA, hex='04BA', c='Һ', l='H', r='n', gid=831),
   'Softsign_cy': GD(name='Softsign_cy', uni=0x042C, hex='042C', c='Ь', l='H', r='O', gid=689),

    #   T

   'Te_cy': GD(name='Te_cy', uni=0x0422, hex='0422', c='Т', l='T', r='T', base='T', anchors=['top', 'middle', 'bottom'], gid=679),
   'Tedescender_cy': GD(name='Tedescender_cy', uni=0x04AC, hex='04AC', c='Ҭ', l='T', r='T', gid=817),
   'Tetse_cy': GD(name='Tetse_cy', uni=0x04B4, hex='04B4', c='Ҵ', l='T', r='Tse_cy', gid=825),
   'Tse_cy': GD(name='Tse_cy', uni=0x0426, hex='0426', c='Ц', l='H', r='off', gid=683),
   'Tshe_cy': GD(name='Tshe_cy', uni=0x040B, hex='040B', c='Ћ', l='T', r='n', gid=656),

    #   U

   'U_cy': GD(name='U_cy', uni=0x0423, hex='0423', c='У', l2r='U_cy', anchors=['top'], gid=680),
   'Udieresis_cy': GD(name='Udieresis_cy', uni=0x04F0, hex='04F0', c='Ӱ', l='U_cy', r='U_cy', base='U_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=885),
   'Uhungarumlaut_cy': GD(name='Uhungarumlaut_cy', uni=0x04F2, hex='04F2', c='Ӳ', l='U_cy', r='U_cy', base='U_cy', accents=['hungarumlautcmb.uc'], anchors=['top'], gid=887),
   #'Uk_cy': GD(name='Uk_cy', uni=0x0478, hex='0478', c='Ѹ', l='O', r='y', base='O', accents=['y'], gid=765),
   'Umacron_cy': GD(name='Umacron_cy', uni=0x04EE, hex='04EE', c='Ӯ', l='U_cy', r='U_cy', base='U_cy', accents=['macroncmb.uc'], anchors=['top'], gid=883),
   'Ushort_cy': GD(name='Ushort_cy', uni=0x040E, hex='040E', c='Ў', l='U_cy', r='U_cy', base='U_cy', accents=['brevecmb_cy.uc'], anchors=['top'], gid=659),
   'Ustrait_cy': GD(name='Ustrait_cy', uni=0x04AE, hex='04AE', c='Ү', l='Y', r='Y', base='Y', anchors=['top', 'middle', 'bottom'], gid=819),
   'Ustraitstroke_cy': GD(name='Ustraitstroke_cy', uni=0x04B0, hex='04B0', c='Ұ', l='Y', r='Y', base='Y', gid=821),

    #   V

   'Ve_cy': GD(name='Ve_cy', uni=0x0412, hex='0412', c='В', l='B', r='B', base='B', anchors=['top', 'middle', 'bottom'], gid=663),

    #   W

    #   X

    #   Y

   #'Yat_cy': GD(name='Yat_cy', uni=0x0462, hex='0462', c='Ѣ', r='Softsign_cy',base='Softsign_cy', gid=743),
   'Yeru_cy': GD(name='Yeru_cy', uni=0x042B, hex='042B', c='Ы', l='H', r='H', anchors=['top'], gid=688),
   'Yerudieresis_cy': GD(name='Yerudieresis_cy', uni=0x04F8, hex='04F8', c='Ӹ', l='H', r='H', base='Yeru_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=893),
   'Yi_cy': GD(name='Yi_cy', uni=0x0407, hex='0407', c='Ї', bl='I', w='I', base='I', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=652),
   #'Yusbig_cy': GD(name='Yusbig_cy', uni=0x046A, hex='046A', c='Ѫ', l2r='Yusbig_cy', gid=751),
   #'Yusbigiotified_cy': GD(name='Yusbigiotified_cy', uni=0x046C, hex='046C', c='Ѭ', l='H', r='Yusbig_cy', gid=753),
   #'Yuslittle_cy': GD(name='Yuslittle_cy', uni=0x0466, hex='0466', c='Ѧ', l='A', r='A', gid=747),
   #'Yuslittleiotified_cy': GD(name='Yuslittleiotified_cy', uni=0x0468, hex='0468', c='Ѩ', l='H', r='A', gid=749),

    #   Z

   'Ze_cy': GD(name='Ze_cy', uni=0x0417, hex='0417', c='З', r='B', anchors=['top'], gid=668),
   'Zedescender_cy': GD(name='Zedescender_cy', uni=0x0498, hex='0498', c='Ҙ', l='Ze_cy', r='B', base='Ze_cy', gid=797),
   'Zedieresis_cy': GD(name='Zedieresis_cy', uni=0x04DE, hex='04DE', c='Ӟ', l='Ze_cy', r='B', base='Ze_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=867),
   'Zhe_cy': GD(name='Zhe_cy', uni=0x0416, hex='0416', c='Ж', r2l='Ka_cy', anchors=['top'], gid=667),
   'Zhebreve_cy': GD(name='Zhebreve_cy', uni=0x04C1, hex='04C1', c='Ӂ', l='Zhe_cy', r='Zhe_cy', base='Zhe_cy', accents=['brevecmb_cy.uc'], anchors=['top'], gid=838),
   'Zhedescender_cy': GD(name='Zhedescender_cy', uni=0x0496, hex='0496', c='Җ', l='Zhe_cy', r='Shcha_cy', gid=795),
   'Zhedieresis_cy': GD(name='Zhedieresis_cy', uni=0x04DC, hex='04DC', c='Ӝ', l='Zhe_cy', r='Zhe_cy', base='Zhe_cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=865),

    #   a

   'a_cy': GD(name='a_cy', uni=0x0430, hex='0430', c='а', bl='a', w='a', base='a', isLower=True, anchors=['top', 'middle', 'bottom'], gid=693),
   'abreve_cy': GD(name='abreve_cy', uni=0x04D1, hex='04D1', c='ӑ', bl='a', w='a', base='a', accents=['brevecmb_cy'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=854),
   'adieresis_cy': GD(name='adieresis_cy', uni=0x04D3, hex='04D3', c='ӓ', l='a', r='a', base='a', accents=['dieresiscmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=856),
   'aie_cy': GD(name='aie_cy', uni=0x04D5, hex='04D5', c='ӕ', bl='a', r='e', base='ae', isLower=True, anchors=['top', 'middle', 'bottom'], gid=858),

    #   b

   'be_cy': GD(name='be_cy', uni=0x0431, hex='0431', c='б', l='O', r='o', isLower=False, gid=694), # Behaves as capital
   'be_cy.loclSRB': GD(name='be_cy.loclSRB', l='o', r='o', isLower=True),

    #   c

   'che_cy': GD(name='che_cy', uni=0x0447, hex='0447', c='ч', r='en_cy', isLower=True, anchors=['top'], gid=716),
   'che_cy.loclBGR': GD(name='che_cy.loclBGR', l='che_cy', isLower=True),   
   'cheabkhasian_cy': GD(name='cheabkhasian_cy', uni=0x04BD, hex='04BD', c='ҽ', l='o', r='e', isLower=True, gid=834),
   'chedescender_cy': GD(name='chedescender_cy', uni=0x04B7, hex='04B7', c='ҷ', l='che_cy', r='tse_cy', isLower=True, gid=828),
   'chedescenderabkhasian_cy': GD(name='chedescenderabkhasian_cy', uni=0x04BF, hex='04BF', c='ҿ', l='cheabkhasian_cy', r='e', base='cheabkhasian_cy', isLower=True, gid=836),
   #'chedescenderabkhasian_cy.component': GD(name='chedescenderabkhasian_cy.component', w=0, isLower=True, gid=1628),
   'chedieresis_cy': GD(name='chedieresis_cy', uni=0x04F5, hex='04F5', c='ӵ', l='che_cy', r='en_cy', base='che_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=890),
   'chekhakassian_cy': GD(name='chekhakassian_cy', uni=0x04CC, hex='04CC', c='ӌ', l='che_cy', r='en_cy', isLower=True, gid=849),
   'cheverticalstroke_cy': GD(name='cheverticalstroke_cy', uni=0x04B9, hex='04B9', c='ҹ', l='che_cy', r='en_cy', isLower=True, anchors=['top'], gid=830),

    #   d

   #'dasiapneumatacmb_cy': GD(name='dasiapneumatacmb_cy', uni=0x0485, hex='0485', c='҅', w=0, isLower=True, anchors=['top', '_top'], gid=778),
   'de_cy': GD(name='de_cy', uni=0x0434, hex='0434', c='д', r='o', isLower=True, gid=697, anchors=['top', 'middle', 'bottom']), # Italic variant has different shape.
   'de_cy.loclBGR': GD(name='de_cy.loclBGR', isLower=True),
   'dje_cy': GD(name='dje_cy', uni=0x0452, hex='0452', c='ђ', l='hbar', isLower=True, gid=727),
   'dze_cy': GD(name='dze_cy', uni=0x0455, hex='0455', c='ѕ', l='s', r='s', base='s', isLower=True, anchors=['top', 'middle', 'bottom'], gid=730),
   'dzhe_cy': GD(name='dzhe_cy', uni=0x045F, hex='045F', c='џ', l='en_cy', r='en_cy', isLower=True, gid=740),

    #   e

   'e_cy': GD(name='e_cy', uni=0x0454, hex='0454', c='є', l='o', r='c', isLower=True, gid=729),
   'edieresis_cy': GD(name='edieresis_cy', uni=0x04ED, hex='04ED', c='ӭ', anchorTopX='TopX', l='ereversed_cy', r='o', base='ereversed_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=882),
   'ef_cy': GD(name='ef_cy', uni=0x0444, hex='0444', c='ф', l2r='ef_cy', isLower=True, gid=713),
   #'eiotified_cy': GD(name='eiotified_cy', uni=0x0465, hex='0465', c='ѥ', l='en_cy', r='c', isLower=True, gid=746),
   'el_cy': GD(name='el_cy', uni=0x043B, hex='043B', c='л', r='en_cy', isLower=True, gid=704),
   'el_cy.loclBGR': GD(name='el_cy.loclBGR', isLower=True),
   'eltail_cy': GD(name='eltail_cy', uni=0x04C6, hex='04C6', c='ӆ', l='el_cy', r='iishorttail_cy', base='el_cy', accents=['tail.component_cy'], isLower=True, gid=843),
   'em_cy': GD(name='em_cy', uni=0x043C, hex='043C', c='м', l='en_cy', r='en_cy', isLower=True, gid=705),
   'emtail_cy': GD(name='emtail_cy', uni=0x04CE, hex='04CE', c='ӎ', l='en_cy', r='iishorttail_cy', base='em_cy', accents=['tail.component_cy'], isLower=True, gid=851),
   'en_cy': GD(name='en_cy', uni=0x043D, hex='043D', c='н', l='off', l2r='en_cy', isLower=True, gid=706),
   'en_cy.loclBGR': GD(name='en_cy.loclBGR', isLower=True),
   'endescender_cy': GD(name='endescender_cy', uni=0x04A3, hex='04A3', c='ң', l='en_cy', r='tse_cy', isLower=True, gid=808),
   'enghe_cy': GD(name='enghe_cy', uni=0x04A5, hex='04A5', c='ҥ', l='en_cy', r='ge_cy', isLower=True, gid=810),
   'enhook_cy': GD(name='enhook_cy', uni=0x04C8, hex='04C8', c='ӈ', l='en_cy', r='j', isLower=True, gid=845),
   'entail_cy': GD(name='entail_cy', uni=0x04CA, hex='04CA', c='ӊ', l='en_cy', r='iishorttail_cy', base='en_cy', accents=['tail.component_cy'], isLower=True, gid=847),
   'er_cy': GD(name='er_cy', uni=0x0440, hex='0440', c='р', l='p', r='p', base='p', isLower=True, anchors=['top', 'middle', 'bottom'], gid=709),
   'ereversed_cy': GD(name='ereversed_cy', uni=0x044D, hex='044D', c='э', r='o', anchorTopX='TopX', isLower=True, anchors=['top'], gid=722),
   'ertick_cy': GD(name='ertick_cy', uni=0x048F, hex='048F', c='ҏ', l='p', w='p', base='p', isLower=True, anchors=['top', 'middle', 'bottom'], gid=788),
   'es_cy': GD(name='es_cy', uni=0x0441, hex='0441', c='с', l='c', r='c', base='c', isLower=True, anchors=['top', 'middle', 'bottom'], gid=710),
   'esdescender_cy': GD(name='esdescender_cy', uni=0x04AB, hex='04AB', c='ҫ', l='o', r='c', base='c', isLower=True, gid=816),

    #   f

   #'fita_cy': GD(name='fita_cy', uni=0x0473, hex='0473', c='ѳ', l='o', r='o', base='obarred_cy', isLower=True, gid=760),

    #   g

   'ge_cy': GD(name='ge_cy', uni=0x0433, hex='0433', c='г', l2r='s', r2l='s', isLower=True, anchors=['top', 'middle', 'bottom'], gid=696),
   'ge_cy.loclBGR': GD(name='ge_cy.loclBGR', isLower=True),
   'gedescender_cy': GD(name='gedescender_cy', uni=0x04F7, hex='04F7', c='ӷ', l='en_cy', r='ge_cy', isLower=True, gid=892),
   'ghemiddlehook_cy': GD(name='ghemiddlehook_cy', uni=0x0495, hex='0495', c='ҕ', l='en_cy', r='o', isLower=True, gid=794),
   'ghestroke_cy': GD(name='ghestroke_cy', uni=0x0493, hex='0493', c='ғ',  r='ge_cy', base='ge_cy', isLower=True, gid=792),
   'gheupturn_cy': GD(name='gheupturn_cy', uni=0x0491, hex='0491', c='ґ', l='en_cy', r='ge_cy', isLower=True, gid=790),
   'gje_cy': GD(name='gje_cy', uni=0x0453, hex='0453', c='ѓ', base='ge_cy', accents=['acutecmb'], isLower=True, anchors=['top'], gid=728),
   'gehookstroke_cy': GD(name='gehookstroke_cy', uni=0x04FB, hex='04FB', c='ӻ', r='ge_cy', isLower=True, anchors=['top']),

    #   h

   'ha_cy': GD(name='ha_cy', uni=0x0445, hex='0445', c='х', l='x', r='x', base='x', isLower=True, anchors=['top', 'middle', 'bottom'], gid=714),
   'haabkhasian_cy': GD(name='haabkhasian_cy', uni=0x04A9, hex='04A9', c='ҩ', l='o', r='c', isLower=True, gid=814),
   'hadescender_cy': GD(name='hadescender_cy', uni=0x04B3, hex='04B3', c='ҳ', l='x', r='kadescender_cy', isLower=True, gid=824),
   'hahook_cy': GD(name='hahook_cy', uni=0x04FD, hex='04FD', c='ӽ', l='x', r='x', isLower=True, gid=898),
   'hardsign_cy': GD(name='hardsign_cy', uni=0x044A, hex='044A', c='ъ', l='te_cy', r='softsign_cy', isLower=True, gid=719),
   'hardsign_cy.loclBGR': GD(name='hardsign_cy.loclBGR', l='hardsign_cy', r='hardsign_cy', isLower=True), 
   'hastroke_cy': GD(name='hastroke_cy', uni=0x04FF, hex='04FF', c='ӿ', l='x', r='x', base='x', isLower=True, gid=900),

    #   i
    
   'i_cy': GD(name='i_cy', uni=0x0456, hex='0456', c='і', l='i', w='idotless', base='i', anchorBottomX='BottomX', anchorMiddleX='TopX', anchorTopX='TopX', isLower=True, anchors=['top', 'middle', 'bottom'], gid=731),
   'ia_cy': GD(name='ia_cy', uni=0x044F, hex='044F', c='я', r='en_cy', isLower=True, gid=724),
   'idieresis_cy': GD(name='idieresis_cy', uni=0x04E5, hex='04E5', c='ӥ', base='ii_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=874),
   'ie_cy': GD(name='ie_cy', uni=0x0435, hex='0435', c='е', l='o', w='e', base='e', isLower=True, anchors=['top', 'middle', 'bottom'], gid=698),
   'iebreve_cy': GD(name='iebreve_cy', uni=0x04D7, hex='04D7', c='ӗ', l='e', w='e', base='e', accents=['brevecmb_cy'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=860),
   'iegrave_cy': GD(name='iegrave_cy', uni=0x0450, hex='0450', c='ѐ', bl='o', w='e', base='e', accents=['gravecmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=725),
   'ii_cy': GD(name='ii_cy', uni=0x0438, hex='0438', c='и', l='en_cy', r='en_cy', bl='u', isLower=True, anchors=['top'], gid=701),
   'ii_cy.loclBGR': GD(name='ii_cy.loclBGR', base='u', isLower=True, anchors=['top']),
   'iigrave_cy': GD(name='iigrave_cy', uni=0x045D, hex='045D', c='ѝ', l='en_cy', r='en_cy', base='ii_cy', accents=['gravecmb'], isLower=True, anchors=['top'], gid=738),
   'iishort_cy': GD(name='iishort_cy', uni=0x0439, hex='0439', c='й', l='en_cy', r='en_cy', base='ii_cy', accents=['brevecmb_cy'], isLower=True, anchors=['top'], gid=702),
   'iishort_cy.loclBGR': GD(name='iishort_cy.loclBGR', base='u', accents=['brevecmb_cy'], isLower=True, anchors=['top']),
   'iishorttail_cy': GD(name='iishorttail_cy', uni=0x048B, hex='048B', c='ҋ', l='en_cy', base='iishort_cy', accents=['tail.component_cy'], isLower=True, anchors=['top'], gid=784),
   'imacron_cy': GD(name='imacron_cy', uni=0x04E3, hex='04E3', c='ӣ', l='en_cy', r='en_cy', base='ii_cy', accents=['macroncmb'], isLower=True, anchors=['top'], gid=872),
   'io_cy': GD(name='io_cy', uni=0x0451, hex='0451', c='ё', l='o', r='e', base='e', accents=['dieresiscmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=726),
   'iu_cy': GD(name='iu_cy', uni=0x044E, hex='044E', c='ю', l='en_cy', r='o', isLower=True, gid=723),
   'iu_cy.loclBGR': GD(name='iu_cy.loclBGR', l='l', r='o', isLower=True),
   #'izhitsa_cy': GD(name='izhitsa_cy', uni=0x0475, hex='0475', c='ѵ', l='v', isLower=True, anchors=['top'], gid=762),
   #'izhitsadblgrave_cy': GD(name='izhitsadblgrave_cy', uni=0x0477, hex='0477', c='ѷ', bl='v', w='izhitsa_cy', base='izhitsa_cy', accents=['dblgravecmb'], isLower=True, anchors=['top'], gid=764),

    #   j

   'je_cy': GD(name='je_cy', uni=0x0458, hex='0458', c='ј', l='j', r='j', base='j', isLower=True, anchors=['middle', 'bottom'], gid=733),

    #   k

   'ka_cy': GD(name='ka_cy', uni=0x043A, hex='043A', c='к', l='en_cy', r='k', isLower=True, anchors=['top'], gid=703),
   'ka_cy.loclBGR': GD(name='ka_cy.loclBGR', base='k', isLower=True),
   'kabashkir_cy': GD(name='kabashkir_cy', uni=0x04A1, hex='04A1', c='ҡ', l='te_cy', r='k', isLower=True, gid=806),
   'kadescender_cy': GD(name='kadescender_cy', uni=0x049B, hex='049B', c='қ', l='en_cy', r='zhedescender_cy', isLower=True, gid=800),
   'kahook_cy': GD(name='kahook_cy', uni=0x04C4, hex='04C4', c='ӄ', l='en_cy', isLower=True, gid=841),
   'kastroke_cy': GD(name='kastroke_cy', uni=0x049F, hex='049F', c='ҟ', r='k', l='hyphen', isLower=True, gid=804),
   'kaverticalstroke_cy': GD(name='kaverticalstroke_cy', uni=0x049D, hex='049D', c='ҝ', l='en_cy', r='k', isLower=True, gid=802),
   'kje_cy': GD(name='kje_cy', uni=0x045C, hex='045C', c='ќ', l='en_cy', r='k', base='ka_cy', accents=['acutecmb'], isLower=True, anchors=['top'], gid=737),
   #'koppa_cy': GD(name='koppa_cy', uni=0x0481, hex='0481', c='ҁ', l='o', r='c', isLower=True, gid=774),
   #'ksi_cy': GD(name='ksi_cy', uni=0x046F, hex='046F', c='ѯ', r='ze_cy', isLower=True, gid=756),

    #   l
   'lje_cy': GD(name='lje_cy', uni=0x0459, hex='0459', c='љ', l='el_cy', r='softsign_cy', gid=654),

    #   m

    #   n

   'nje_cy': GD(name='nje_cy', uni=0x045A, hex='045A', c='њ', l='en_cy', r='softsign_cy', isLower=True, gid=735),
   'numero': GD(name='numero', uni=0x2116, hex='2116', c='№', l='N', base='N', isLower=True),

    #   o

   'o_cy': GD(name='o_cy', uni=0x043E, hex='043E', c='о', l2r='o', base='o', isLower=True, anchors=['top', 'middle', 'bottom'], gid=707),
   'obarred_cy': GD(name='obarred_cy', uni=0x04E9, hex='04E9', c='ө', l='o', r='o', base='o', isLower=True, anchors=['top'], gid=878),
   'obarreddieresis_cy': GD(name='obarreddieresis_cy', uni=0x04EB, hex='04EB', c='ӫ', l='o', r='o', base='obarred_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=880),
   'odieresis_cy': GD(name='odieresis_cy', uni=0x04E7, hex='04E7', c='ӧ', bl='o', w='o', base='o', accents=['dieresiscmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=876),
   #'omega_cy': GD(name='omega_cy', uni=0x0461, hex='0461', c='ѡ', l='off', l2r='omega_cy', isLower=True, anchors=['top'], gid=742),

    #   p

   #'palatalizationcmb_cy': GD(name='palatalizationcmb_cy', uni=0x0484, hex='0484', c='҄', w=0, isLower=True, anchors=['top', '_top'], gid=777),
   'palochka_cy': GD(name='palochka_cy', uni=0x04CF, hex='04CF', c='ӏ', l='h', l2r='h', isLower=True, anchors=['top', 'middle', 'bottom'], gid=852),
   'pe_cy': GD(name='pe_cy', uni=0x043F, hex='043F', c='п', l='en-cu', r='en_cy', isLower=True, gid=708),
   'pe_cy.loclBGR': GD(name='pe_cy.loclBGR', l='n', r='n', base='n', isLower=True),
   'pedescender_cy': GD(name='pedescender_cy', uni=0x0525, hex='0525', c='ԥ', l='en_cy', r='tse_cy', isLower=True, gid=902),
   #'pedescender_cy.component': GD(name='pedescender_cy.component', w=0, isLower=True, gid=1681),
   'pemiddlehook_cy': GD(name='pemiddlehook_cy', uni=0x04A7, hex='04A7', c='ҧ', l='en_cy', r='o', isLower=True, gid=812),
   #'psi_cy': GD(name='psi_cy', uni=0x0471, hex='0471', c='ѱ', r='n', base='psi',isLower=True, gid=758),
   #'psilipneumatacmb_cy': GD(name='psilipneumatacmb_cy', uni=0x0486, hex='0486', c='҆', w=0, base='psili', isLower=True, anchors=['top', '_top'], gid=779),

    #   q

    #   r

    #   s

   'schwa_cy': GD(name='schwa_cy', uni=0x04D9, hex='04D9', c='ә', r='o', isLower=True, anchors=['top'], gid=862),
   'schwadieresis_cy': GD(name='schwadieresis_cy', uni=0x04DB, hex='04DB', c='ӛ', l='schwa_cy', r='o', base='schwa_cy', accents=['dieresiscmb'], isLower=True, gid=864),
   'semisoftsign_cy': GD(name='semisoftsign_cy', uni=0x048D, hex='048D', c='ҍ', r='softsign_cy', srcName='softsign_cy', isLower=True, gid=786),
   'sha_cy': GD(name='sha_cy', uni=0x0448, hex='0448', c='ш', l='en_cy', r='en_cy', isLower=True, gid=717),
   'sha_cy.loclBGR': GD(name='sha_cy.loclBGR', l='u', r='u', isLower=True), 
   'shcha_cy': GD(name='shcha_cy', uni=0x0449, hex='0449', c='щ', l='en_cy', r='tse_cy', isLower=True, gid=718),
   'shcha_cy.loclBGR': GD(name='shcha_cy.loclBGR', l='u', r='tse_cy', isLower=True),
   'shha_cy': GD(name='shha_cy', uni=0x04BB, hex='04BB', c='һ', l='h', r='h', base='h', isLower=True, anchors=['top', 'middle', 'bottom'], gid=832),
   'softsign_cy': GD(name='softsign_cy', uni=0x044C, hex='044C', c='ь', l='en_cy', isLower=True, gid=721),
   'softsign_cy.loclBGR': GD(name='softsign_cy.loclBGR', l='u', r='softsign_cy', isLower=True),

    #   t

   'te_cy': GD(name='te_cy', uni=0x0442, hex='0442', c='т', l2r='te_cy', isLower=True, gid=711),
   'te_cy.loclBGR': GD(name='te_cy.loclBGR', l='m', r='m', base='m', isLower=True),
   'tedescender_cy': GD(name='tedescender_cy', uni=0x04AD, hex='04AD', c='ҭ', l='te_cy', r='te_cy', isLower=True, gid=818),
   'tetse_cy': GD(name='tetse_cy', uni=0x04B5, hex='04B5', c='ҵ', l='te_cy', r='tse_cy', isLower=True, gid=826),
   #'thousand_cy': GD(name='thousand_cy', uni=0x0482, hex='0482', c='҂', isLower=True, gid=775),
   #'titlocmb_cy': GD(name='titlocmb_cy', uni=0x0483, hex='0483', c='҃', w=0, isLower=True, anchors=['top', '_top'], gid=776),
   'tse_cy': GD(name='tse_cy', uni=0x0446, hex='0446', c='ц', l='en_cy', anchors=['top'], isLower=True, gid=715),
   'tse_cy.loclBGR': GD(name='tse_cy.loclBGR', l='u', r='tse_cy', isLower=True),
   'tshe_cy': GD(name='tshe_cy', uni=0x045B, hex='045B', c='ћ', l='hbar', r='hbar', base='h', isLower=True, gid=736),

    'tail.component_cy.case': GD(name='tail.component_cy.case', w=0, isLower=False),
    'tail.component_cy.case.sc': GD(name='tail.component_cy.case.sc', w=0, isLower=False),
    'tail.component_cy': GD(name='tail.component_cy', w=0, isLower=True),

    #   u

   'u_cy': GD(name='u_cy', uni=0x0443, hex='0443', c='у', l='y', r='y', base='y', isLower=True, anchors=['top', 'middle', 'bottom'], gid=712),
   'udieresis_cy': GD(name='udieresis_cy', uni=0x04F1, hex='04F1', c='ӱ', l='y', r='y', base='y', accents=['dieresiscmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=886),
   'uhungarumlaut_cy': GD(name='uhungarumlaut_cy', uni=0x04F3, hex='04F3', c='ӳ', l='y', w='y', base='y', accents=['hungarumlautcmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=888),
   #'uk_cy': GD(name='uk_cy', uni=0x0479, hex='0479', c='ѹ', l='o', r='y', base='o', accents=['y'], isLower=True, gid=766),
   'umacron_cy': GD(name='umacron_cy', uni=0x04EF, hex='04EF', c='ӯ', l='y', r='y', base='y', accents=['macroncmb'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=884),
   'ushort_cy': GD(name='ushort_cy', uni=0x045E, hex='045E', c='ў', l='y', r='y', base='y', accents=['brevecmb_cy'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=739),
   'ustrait_cy': GD(name='ustrait_cy', uni=0x04AF, hex='04AF', c='ү', l='v', l2r='ustrait_cy', isLower=True, gid=820),
   'ustraitstroke_cy': GD(name='ustraitstroke_cy', uni=0x04B1, hex='04B1', c='ұ', l='ustrait_cy', r='ustrait_cy', base='ustrait_cy', isLower=True, gid=822),

    #   v

   've_cy': GD(name='ve_cy', uni=0x0432, hex='0432', c='в', l='n', r='three', isLower=True, gid=695),
   've_cy.loclBGR': GD(name='ve_cy.loclBGR', l='n', r='three', isLower=True),

    #   w

    #   x

    #   y

   #'yat_cy': GD(name='yat_cy', uni=0x0463, hex='0463', c='ѣ', r='softsign_cy', isLower=True, gid=744),
   'yeru_cy': GD(name='yeru_cy', uni=0x044B, hex='044B', c='ы', l='en_cy', r='en_cy', isLower=True, anchors=['top'], gid=720),
   'yerudieresis_cy': GD(name='yerudieresis_cy', uni=0x04F9, hex='04F9', c='ӹ', l='en_cy', r='en_cy', base='yeru_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=894),
   'yi_cy': GD(name='yi_cy', uni=0x0457, hex='0457', c='ї', w='idotless', bl='idotless', base='idotless', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=732),
   #'yusbig_cy': GD(name='yusbig_cy', uni=0x046B, hex='046B', c='ѫ', l2r='yusbig_cy', isLower=True, gid=752),
   #'yusbigiotified_cy': GD(name='yusbigiotified_cy', uni=0x046D, hex='046D', c='ѭ', l='en_cy', r='yusbig_cy', isLower=True, gid=754),
   #'yuslittle_cy': GD(name='yuslittle_cy', uni=0x0467, hex='0467', c='ѧ', l2r='yuslittle_cy', isLower=True, gid=748),
   #'yuslittleiotified_cy': GD(name='yuslittleiotified_cy', uni=0x0469, hex='0469', c='ѩ', l='en_cy', r='yuslittle_cy', isLower=True, gid=750),

    #   z

    'ze_cy': GD(name='ze_cy', uni=0x0437, hex='0437', c='з', r='ve_cy', isLower=True, anchors=['top'], gid=700),
    'ze_cy.loclBGR': GD(name='ze_cy.loclBGR', isLower=True),
    'zedescender_cy': GD(name='zedescender_cy', uni=0x0499, hex='0499', c='ҙ', l='ze_cy', r='ve_cy', base='ze_cy', isLower=True, gid=798),
    'zedieresis_cy': GD(name='zedieresis_cy', uni=0x04DF, hex='04DF', c='ӟ', l='ze_cy', r='ve_cy', base='ze_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=868),
    'zhe_cy': GD(name='zhe_cy', uni=0x0436, hex='0436', c='ж', r='k', isLower=True, anchors=['top'], gid=699),
    'zhe_cy.loclBGR': GD(name='zhe_cy.loclBGR', l ='zhe_cy', r='zhe_cy', isLower=True),
    'zhebreve_cy': GD(name='zhebreve_cy', uni=0x04C2, hex='04C2', c='ӂ', l='zhe_cy', r='zhe_cy', base='zhe_cy', accents=['brevecmb_cy'], isLower=True, anchors=['top'], gid=839),
    'zhedescender_cy': GD(name='zhedescender_cy', uni=0x0497, hex='0497', c='җ', l='zhe_cy', isLower=True, gid=796),
    'zhedieresis_cy': GD(name='zhedieresis_cy', uni=0x04DD, hex='04DD', c='ӝ', l='zhe_cy', r='zhe_cy', base='zhe_cy', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=866),
  
    'breve_cy': GD(name='breve_cy', base='brevecmb_cy', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, ),
    'brevecmb_cy': GD(name='breve_cy', w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='brevecmb', isLower=True, anchors=['_top', 'top'], ),
    'brevecmb_cy.uc': GD(name='breve_cy.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=False, srcName='brevecmb.uc', anchors=['_top', 'top'], ),

}

CYRILLIC_SET_ITALIC = CSI = deepcopy(CYRILLIC_SET)

# Exceptions to the Cyrillic Italic set go here.
CSI['te_cy'] = GD(name='te_cy', uni=0x0442, hex='0442', c='т', l='m', r='m', base='m', isLower=True, gid=711)
CSI['tedescender_cy'] = GD(name='tedescender_cy', uni=0x04AD, hex='04AD', c='ҭ', l='m', r='m', base='m', isLower=True, gid=711)
CSI['tetse_cy'] = GD(name='tetse_cy', uni=0x04B5, hex='04B5', c='ҵ', l='u', r='tse_cy', base='tse_cy', accents=['macroncmb'], isLower=True, gid=826)
CSI['pe_cy'] = GD(name='pe_cy', uni=0x043F, hex='043F', c='п', l='n', r='n', base='n', isLower=True, gid=708)
CSI['ii_cy'] = GD(name='ii_cy', uni=0x0438, hex='0438', c='и', l='u', r='u', base='u', isLower=True, anchors=['top'], gid=701)
CSI['dzhe_cy'] = GD(name='dzhe_cy', uni=0x045F, hex='045F', c='џ', l='en_cy', r='en_cy', base='u', isLower=True, gid=740)
CSI['de_cy.loclBGR'] = GD(name='de_cy.loclBGR', base='g', isLower=True)
CSI['ghestroke_cy'] = GD(name='ghestroke_cy', uni=0x0493, hex='0493', c='ғ', isLower=True, gid=792)
CSI['pedescender_cy'] = GD(name='pedescender_cy', uni=0x0525, hex='0525', c='ԥ', l='en_cy', r='tse_cy', base='n', isLower=True, gid=902)


# Remove these glyphs from the Cyrillic italic set, because the glyphs are the identical to the defailt glyphs
for gName in [
    'ge_cy.loclBGR', 'ii_cy.loclBGR', 'iishort_cy.loclBGR', 'en_cy.loclBGR', 'tse_cy.loclBGR', 
    'che_cy.loclBGR', 'sha_cy.loclBGR', 'shcha_cy.loclBGR', 'hardsign_cy.loclBGR', 'softsign_cy.loclBGR']:
    if gName in CYRILLIC_SET_ITALIC:
        del CYRILLIC_SET_ITALIC[gName]


