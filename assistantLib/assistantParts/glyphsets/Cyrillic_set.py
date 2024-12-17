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

# The "c" attribtes are redundant, if the @uni or @hex are defined, but they offer easy searching in the source by char.

CYRILLIC_SET = {

    #   A

   'A-cy': GD(name='A-cy', uni=0x0410, hex='0410', c='А', l='A', r='A', base='A', anchors=['top', 'middle', 'bottom'], gid=661),
   'Abreve-cy': GD(name='Abreve-cy', uni=0x04D0, hex='04D0', c='Ӑ', l='A', r='A', base='A', accents=['brevecmb-cy.uc'], anchors=['top', 'middle', 'bottom'], gid=853),
   'Adieresis-cy': GD(name='Adieresis-cy', uni=0x04D2, hex='04D2', c='Ӓ', l='A', r='A', base='A', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=855),
   'Aie-cy': GD(name='Aie-cy', uni=0x04D4, hex='04D4', c='Ӕ', l='AE', r='E', base='AE', anchors=['top', 'middle', 'bottom'], gid=857),

    #   B

   'Be-cy': GD(name='Be-cy', uni=0x0411, hex='0411', c='Б', l='H', gid=662),

    #   C

   'Che-cy': GD(name='Che-cy', uni=0x0427, hex='0427', c='Ч', r='H', anchors=['top'], gid=684),
   'Cheabkhasian-cy': GD(name='Cheabkhasian-cy', uni=0x04BC, hex='04BC', c='Ҽ', l='o', r='O', gid=833),
   'Chedescender-cy': GD(name='Chedescender-cy', uni=0x04B6, hex='04B6', c='Ҷ', l='Che-cy', r='Tse-cy', gid=827),
   'Chedescenderabkhasian-cy': GD(name='Chedescenderabkhasian-cy', uni=0x04BE, hex='04BE', c='Ҿ', l='Cheabkhasian-cy', r='Cheabkhasian-cy', base='Cheabkhasian-cy', accents=['Chedescenderabkhasian-cy.component'], gid=835),
   'Chedescenderabkhasian-cy.component': GD(name='Chedescenderabkhasian-cy.component', gid=1599),
   'Chedieresis-cy': GD(name='Chedieresis-cy', uni=0x04F4, hex='04F4', c='Ӵ', l='Che-cy', r='H', base='Che-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=889),
   'Chekhakassian-cy': GD(name='Chekhakassian-cy', uni=0x04CB, hex='04CB', c='Ӌ', l='Che-cy', r='H', gid=848),
   'Cheverticalstroke-cy': GD(name='Cheverticalstroke-cy', uni=0x04B8, hex='04B8', c='Ҹ', l='Che-cy', r='H', base='Che-cy', anchors=['top'], gid=829),

    #   D

   'De-cy': GD(name='De-cy', uni=0x0414, hex='0414', c='Д', l='off', r='Tse-cy', gid=665),
   'Dje-cy': GD(name='Dje-cy', uni=0x0402, hex='0402', c='Ђ', l='T', gid=647),
   'Dze-cy': GD(name='Dze-cy', uni=0x0405, hex='0405', c='Ѕ', l='S', r='S', base='S', anchors=['top', 'middle', 'bottom'], gid=650),
   'Dzhe-cy': GD(name='Dzhe-cy', uni=0x040F, hex='040F', c='Џ', l='H', r='H', gid=660),

    #   E

   'E-cy': GD(name='E-cy', uni=0x0404, hex='0404', c='Є', l='O', r='C', gid=649),
   'Edieresis-cy': GD(name='Edieresis-cy', uni=0x04EC, hex='04EC', c='Ӭ', l='Ereversed-cy', r='O', base='Ereversed-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=881),
   'Ef-cy': GD(name='Ef-cy', uni=0x0424, hex='0424', c='Ф', l2r='Ef-cy', gid=681),
   'Eiotified-cy': GD(name='Eiotified-cy', uni=0x0464, hex='0464', c='Ѥ', l='H', r='C', gid=745),
   'El-cy': GD(name='El-cy', uni=0x041B, hex='041B', c='Л', r='H', gid=672),
   'Eltail-cy': GD(name='Eltail-cy', uni=0x04C5, hex='04C5', c='Ӆ', l='El-cy', r='Iishorttail-cy', base='El-cy', anchorTopY='El-cy', accents=['tail.component'], gid=842),
   'Em-cy': GD(name='Em-cy', uni=0x041C, hex='041C', c='М', l='H', r='H', base='M', anchors=['top', 'middle', 'bottom'], gid=673),
   'Emtail-cy': GD(name='Emtail-cy', uni=0x04CD, hex='04CD', c='Ӎ', l='H', r='Iishorttail-cy', base='M', anchorBottomY='M', accents=['tail.component'], anchors=['top', 'middle', 'bottom'], gid=850),
   'En-cy': GD(name='En-cy', uni=0x041D, hex='041D', c='Н', l='H', r='H', base='H', anchors=['top', 'middle', 'bottom'], gid=674),
   'Endescender-cy': GD(name='Endescender-cy', uni=0x04A2, hex='04A2', c='Ң', l='H', r='Tse-cy', gid=807),
   'Enghe-cy': GD(name='Enghe-cy', uni=0x04A4, hex='04A4', c='Ҥ', l='H', r='Ge-cy', gid=809),
   'Enhook-cy': GD(name='Enhook-cy', uni=0x04C7, hex='04C7', c='Ӈ', l='H', r='J', gid=844),
   'Entail-cy': GD(name='Entail-cy', uni=0x04C9, hex='04C9', c='Ӊ', l='H', r='Iishorttail-cy', base='H', anchorBottomY='H', accents=['tail.component'], anchors=['top', 'middle', 'bottom'], gid=846),
   'Er-cy': GD(name='Er-cy', uni=0x0420, hex='0420', c='Р', l='H', r='P', base='P', anchors=['top', 'middle', 'bottom'], gid=677),
   'Ereversed-cy': GD(name='Ereversed-cy', uni=0x042D, hex='042D', c='Э', r='O', anchors=['top'], gid=690),
   'Ertick-cy': GD(name='Ertick-cy', uni=0x048E, hex='048E', c='Ҏ', l='H', r='P', base='Er-cy', gid=787),
   'Es-cy': GD(name='Es-cy', uni=0x0421, hex='0421', c='С', l='C', r='C', base='C', anchors=['top', 'middle', 'bottom'], gid=678),
   'Esdescender-cy': GD(name='Esdescender-cy', uni=0x04AA, hex='04AA', c='Ҫ', l='O', r='C', gid=815),

    #   F

   'Fita-cy': GD(name='Fita-cy', uni=0x0472, hex='0472', c='Ѳ', l='O', r='O', gid=759),

    #   G

   'Ge-cy': GD(name='Ge-cy', uni=0x0413, hex='0413', c='Г', l='H', base='Gamma', anchors=['top'], gid=664),
   'Gedescender-cy': GD(name='Gedescender-cy', uni=0x04F6, hex='04F6', c='Ӷ', l='H', r='Ge-cy', gid=891),
   'Gestrokehook-cy': GD(name='Gestrokehook-cy', uni=0x04FA, hex='04FA', c='Ӻ', r='Ge-cy', base='Ghestroke-cy', accents=['Gestrokehook-cy.component'], gid=895),
   'Gestrokehook-cy.component': GD(name='Gestrokehook-cy.component', w=0, gid=1600),
   'Ghemiddlehook-cy': GD(name='Ghemiddlehook-cy', uni=0x0494, hex='0494', c='Ҕ', l='H', r='o', gid=793),
   'Ghestroke-cy': GD(name='Ghestroke-cy', uni=0x0492, hex='0492', c='Ғ', l='Eth', r='Ge-cy', gid=791),
   'Gheupturn-cy': GD(name='Gheupturn-cy', uni=0x0490, hex='0490', c='Ґ', l='H', r='Ge-cy', gid=789),
   'Gje-cy': GD(name='Gje-cy', uni=0x0403, hex='0403', c='Ѓ', l='H', r='Ge-cy', base='Ge-cy', accents=['acutecmb.uc'], anchors=['top'], gid=648),

    #   H

   'Ha-cy': GD(name='Ha-cy', uni=0x0425, hex='0425', c='Х', l='X', r='X', base='X', anchors=['top', 'middle', 'bottom'], gid=682),
   'Haabkhasian-cy': GD(name='Haabkhasian-cy', uni=0x04A8, hex='04A8', c='Ҩ', l='o', r='c', gid=813),
   'Hadescender-cy': GD(name='Hadescender-cy', uni=0x04B2, hex='04B2', c='Ҳ', l='X', r='Kadescender-cy', gid=823),
   'Hahook-cy': GD(name='Hahook-cy', uni=0x04FC, hex='04FC', c='Ӽ', l='X', r='X', gid=897),
   'Hardsign-cy': GD(name='Hardsign-cy', uni=0x042A, hex='042A', c='Ъ', l='T', r='Softsign-cy', gid=687),
   'Hastroke-cy': GD(name='Hastroke-cy', uni=0x04FE, hex='04FE', c='Ӿ', l='X', r='X', gid=899),

    #   I

   'I-cy': GD(name='I-cy', uni=0x0406, hex='0406', bl='I', br='I', base='I', anchors=['top', 'middle', 'bottom'], gid=651),
   'Ia-cy': GD(name='Ia-cy', uni=0x042F, hex='042F', c='Я', r='H', gid=692),
   'Idieresis-cy': GD(name='Idieresis-cy', uni=0x04E4, hex='04E4', c='Ӥ', bl='H', br='H', base='Ii-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=873),
   'Ie-cy': GD(name='Ie-cy', uni=0x0415, hex='0415', c='Е', bl='H', r='E', base='E', anchors=['top', 'middle', 'bottom'], gid=666),
   'Iebreve-cy': GD(name='Iebreve-cy', uni=0x04D6, hex='04D6', c='Ӗ', bl='E', br='E', base='E', accents=['brevecmb-cy.uc'], anchors=['top', 'middle', 'bottom'], gid=859),
   'Iegrave-cy': GD(name='Iegrave-cy', uni=0x0400, hex='0400', c='Ѐ', bl='E', br='E', base='E', accents=['gravecmb.uc'], anchors=['top', 'middle', 'bottom'], gid=645),
   'Ii-cy': GD(name='Ii-cy', uni=0x0418, hex='0418', c='И', l='H', r='H', anchors=['top'], gid=669),
   'Iigrave-cy': GD(name='Iigrave-cy', uni=0x040D, hex='040D', c='Ѝ', bl='H', br='H', base='Ii-cy', accents=['gravecmb.uc'], anchors=['top'], gid=658),
   'Iinvertedbreve': GD(name='Iinvertedbreve', uni=0x020A, hex='020A', c='Ȋ', w='I', bl='I', base='I', accents=['invertedbrevecmb'], anchors=['top', 'middle', 'bottom']),
   'Iishort-cy': GD(name='Iishort-cy', uni=0x0419, hex='0419', c='Й', bl='H', br='H', base='Ii-cy', accents=['brevecmb-cy.uc'], anchors=['top'], gid=670),
   'Iishorttail-cy': GD(name='Iishorttail-cy', uni=0x048A, hex='048A', c='Ҋ', bl='H', r='off', base='Iishort-cy', accents=['tail.component'], gid=783),
   'Imacron-cy': GD(name='Imacron-cy', uni=0x04E2, hex='04E2', c='Ӣ', l='H', r='H', base='Ii-cy', accents=['macroncmb.uc'], anchors=['top'], gid=871),
   'Io-cy': GD(name='Io-cy', uni=0x0401, hex='0401', c='Ё', l='E', r='E', base='E', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=646),
   'Iu-cy': GD(name='Iu-cy', uni=0x042E, hex='042E', c='Ю', l='H', r='O', gid=691),
   'Izhitsa-cy': GD(name='Izhitsa-cy', uni=0x0474, hex='0474', c='Ѵ', l='V', r='V', anchorTopY='V', anchorTopX='V', anchors=['top'], gid=761),
   'Izhitsadblgrave-cy': GD(name='Izhitsadblgrave-cy', uni=0x0476, hex='0476', c='Ѷ', l='V', r='Izhitsa-cy', base='Izhitsa-cy', anchorTopX='V', accents=['dblgravecmb.uc'], anchors=['top'], gid=763),

    #   J

   'Je-cy': GD(name='Je-cy', uni=0x0408, hex='0408', c='Ј', w='J', bl='J', base='J', anchors=['top', 'middle', 'bottom'], gid=653),

    #   K

   'Ka-cy': GD(name='Ka-cy', uni=0x041A, hex='041A', c='К', l='H', r='K', base='K', anchors=['top', 'middle', 'bottom'], gid=671),
   'Kabashkir-cy': GD(name='Kabashkir-cy', uni=0x04A0, hex='04A0', c='Ҡ', l='T', r='K', gid=805),
   'Kadescender-cy': GD(name='Kadescender-cy', uni=0x049A, hex='049A', c='Қ', l='H', r='Zhedescender-cy', gid=799),
   'Kahook-cy': GD(name='Kahook-cy', uni=0x04C3, hex='04C3', c='Ӄ', l='H', gid=840),
   'Kastroke-cy': GD(name='Kastroke-cy', uni=0x049E, hex='049E', c='Ҟ', l='Eth', r='K', gid=803),
   'Kaverticalstroke-cy': GD(name='Kaverticalstroke-cy', uni=0x049C, hex='049C', c='Ҝ', l='H', r='K', gid=801),
   'Kje-cy': GD(name='Kje-cy', uni=0x040C, hex='040C', c='Ќ', l='H', r='K', base='K', accents=['acutecmb.uc'], anchors=['top', 'middle', 'bottom'], gid=657),
   'Koppa-cy': GD(name='Koppa-cy', uni=0x0480, hex='0480', c='Ҁ', l='O', r='C', gid=773),
   'Ksi-cy': GD(name='Ksi-cy', uni=0x046E, hex='046E', c='Ѯ', r='Ze-cy', gid=755),

    #   L

   'Lje-cy': GD(name='Lje-cy', uni=0x0409, hex='0409', c='Љ', l='El-cy', r='Softsign-cy', gid=654),

    #   M

    #   N

   'Nje-cy': GD(name='Nje-cy', uni=0x040A, hex='040A', c='Њ', l='H', r='Softsign-cy', gid=655),

    #   O

   'O-cy': GD(name='O-cy', uni=0x041E, hex='041E', c='О', l='O', r='O', base='O', anchors=['top', 'middle', 'bottom'], gid=675),
   'Obarred-cy': GD(name='Obarred-cy', uni=0x04E8, hex='04E8', c='Ө', l='O', r='O', anchors=['top'], anchorTopX='TopX', gid=877),
   'Obarreddieresis-cy': GD(name='Obarreddieresis-cy', uni=0x04EA, hex='04EA', c='Ӫ', l='O', r='O', base='Obarred-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=879),
   'Odieresis-cy': GD(name='Odieresis-cy', uni=0x04E6, hex='04E6', c='Ӧ', l='O', r='O', base='O', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=875),
   'Omega-cy': GD(name='Omega-cy', uni=0x0460, hex='0460', c='Ѡ', l='V', r='V', anchors=['top'], gid=741),

    #   P

   'Palochka-cy': GD(name='Palochka-cy', uni=0x04C0, hex='04C0', c='Ӏ', l='I', r='I', base='I', anchors=['top', 'middle', 'bottom'], gid=837),
   'Pe-cy': GD(name='Pe-cy', uni=0x041F, hex='041F', c='П', l='H', r='H', gid=676),
   'Pedescender-cy': GD(name='Pedescender-cy', uni=0x0524, hex='0524', c='Ԥ', l='H', r='Tse-cy', gid=901),
   'Pedescender-cy.component': GD(name='Pedescender-cy.component', w=0, gid=1605),
   'Pemiddlehook-cy': GD(name='Pemiddlehook-cy', uni=0x04A6, hex='04A6', c='Ҧ', l='H', r='o', gid=811),
   'Psi-cy': GD(name='Psi-cy', uni=0x0470, hex='0470', c='Ѱ', l='V', r='U', gid=757),

    #   Q

    #   R

    #   S

   'Schwa-cy': GD(name='Schwa-cy', uni=0x04D8, hex='04D8', c='Ә', r='O', base='Schwa', anchors=['top'], gid=861),
   'Schwadieresis-cy': GD(name='Schwadieresis-cy', uni=0x04DA, hex='04DA', c='Ӛ', l='Schwa-cy', r='O', base='Schwa', accents=['dieresiscmb.uc'], anchors=['top'], gid=863),
   'Semisoftsign-cy': GD(name='Semisoftsign-cy', uni=0x048C, hex='048C', c='Ҍ', r='Softsign-cy', gid=785),
   'Sha-cy': GD(name='Sha-cy', uni=0x0428, hex='0428', c='Ш', l='H', r='H', gid=685),
   'Shcha-cy': GD(name='Shcha-cy', uni=0x0429, hex='0429', c='Щ', l='H', r='Tse-cy', gid=686),
   'Shei-coptic': GD(name='Shei-coptic', uni=0x03E2, hex='03E2', l='H', r='H', c='Ϣ', gid=615),
   'Shha-cy': GD(name='Shha-cy', uni=0x04BA, hex='04BA', c='Һ', l='H', r='n', gid=831),
   'Softsign-cy': GD(name='Softsign-cy', uni=0x042C, hex='042C', c='Ь', l='H', r='O', gid=689),

    #   T

   'Te-cy': GD(name='Te-cy', uni=0x0422, hex='0422', c='Т', l='T', r='T', base='T', anchors=['top', 'middle', 'bottom'], gid=679),
   'Tedescender-cy': GD(name='Tedescender-cy', uni=0x04AC, hex='04AC', c='Ҭ', l='T', r='T', gid=817),
   'Tetse-cy': GD(name='Tetse-cy', uni=0x04B4, hex='04B4', c='Ҵ', l='T', r='Tse-cy', gid=825),
   'Tse-cy': GD(name='Tse-cy', uni=0x0426, hex='0426', c='Ц', l='H', r='off', gid=683),
   'Tshe-cy': GD(name='Tshe-cy', uni=0x040B, hex='040B', c='Ћ', l='T', r='n', gid=656),

    #   U

   'U-cy': GD(name='U-cy', uni=0x0423, hex='0423', c='У', l2r='U-cy', anchors=['top'], gid=680),
   'Udieresis-cy': GD(name='Udieresis-cy', uni=0x04F0, hex='04F0', c='Ӱ', l='U-cy', r='U-cy', base='U-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=885),
   'Uhungarumlaut-cy': GD(name='Uhungarumlaut-cy', uni=0x04F2, hex='04F2', c='Ӳ', l='U-cy', r='U-cy', base='U-cy', accents=['hungarumlautcmb.uc'], anchors=['top'], gid=887),
   'Uk-cy': GD(name='Uk-cy', uni=0x0478, hex='0478', c='Ѹ', l='O', r='izhitsa-cy', gid=765),
   'Umacron-cy': GD(name='Umacron-cy', uni=0x04EE, hex='04EE', c='Ӯ', l='U-cy', r='U-cy', base='U-cy', accents=['macroncmb.uc'], anchors=['top'], gid=883),
   'Ushort-cy': GD(name='Ushort-cy', uni=0x040E, hex='040E', c='Ў', l='U-cy', r='U-cy', base='U-cy', accents=['brevecmb-cy.uc'], anchors=['top'], gid=659),
   'Ustrait-cy': GD(name='Ustrait-cy', uni=0x04AE, hex='04AE', c='Ү', l='Y', r='Y', base='Y', anchors=['top', 'middle', 'bottom'], gid=819),
   'Ustraitstroke-cy': GD(name='Ustraitstroke-cy', uni=0x04B0, hex='04B0', c='Ұ', l='Y', r='Y', gid=821),

    #   V

   'Ve-cy': GD(name='Ve-cy', uni=0x0412, hex='0412', c='В', l='B', r='B', base='B', anchors=['top', 'middle', 'bottom'], gid=663),

    #   W

    #   X

    #   Y

   'Yat-cy': GD(name='Yat-cy', uni=0x0462, hex='0462', c='Ѣ', r='Softsign-cy', gid=743),
   'Yeru-cy': GD(name='Yeru-cy', uni=0x042B, hex='042B', c='Ы', l='H', r='H', anchors=['top'], gid=688),
   'Yerudieresis-cy': GD(name='Yerudieresis-cy', uni=0x04F8, hex='04F8', c='Ӹ', l='H', r='H', base='Yeru-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=893),
   'Yi-cy': GD(name='Yi-cy', uni=0x0407, hex='0407', c='Ї', bl='I', w='I', base='I', accents=['dieresiscmb.uc'], anchors=['top', 'middle', 'bottom'], gid=652),
   'Yusbig-cy': GD(name='Yusbig-cy', uni=0x046A, hex='046A', c='Ѫ', l2r='Yusbig-cy', gid=751),
   'Yusbigiotified-cy': GD(name='Yusbigiotified-cy', uni=0x046C, hex='046C', c='Ѭ', l='H', r='Yusbig-cy', gid=753),
   'Yuslittle-cy': GD(name='Yuslittle-cy', uni=0x0466, hex='0466', c='Ѧ', l='A', r='A', gid=747),
   'Yuslittleiotified-cy': GD(name='Yuslittleiotified-cy', uni=0x0468, hex='0468', c='Ѩ', l='H', r='A', gid=749),

    #   Z

   'Ze-cy': GD(name='Ze-cy', uni=0x0417, hex='0417', c='З', r='B', anchors=['top'], gid=668),
   'Zedescender-cy': GD(name='Zedescender-cy', uni=0x0498, hex='0498', c='Ҙ', l='Ze-cy', r='B', gid=797),
   'Zedieresis-cy': GD(name='Zedieresis-cy', uni=0x04DE, hex='04DE', c='Ӟ', l='Ze-cy', r='B', base='Ze-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=867),
   'Zhe-cy': GD(name='Zhe-cy', uni=0x0416, hex='0416', c='Ж', r2l='Ka-cy', anchors=['top'], gid=667),
   'Zhebreve-cy': GD(name='Zhebreve-cy', uni=0x04C1, hex='04C1', c='Ӂ', l='Zhe-cy', r='Zhe-cy', base='Zhe-cy', accents=['brevecmb-cy.uc'], anchors=['top'], gid=838),
   'Zhedescender-cy': GD(name='Zhedescender-cy', uni=0x0496, hex='0496', c='Җ', l='Zhe-cy', r='Shcha-cy', gid=795),
   'Zhedieresis-cy': GD(name='Zhedieresis-cy', uni=0x04DC, hex='04DC', c='Ӝ', l='Zhe-cy', r='Zhe-cy', base='Zhe-cy', accents=['dieresiscmb.uc'], anchors=['top'], gid=865),

    #   a

   'a-cy': GD(name='a-cy', uni=0x0430, hex='0430', c='а', bl='a', w='a', base='a', isLower=True, anchors=['top', 'middle', 'bottom'], gid=693),
   'abreve-cy': GD(name='abreve-cy', uni=0x04D1, hex='04D1', c='ӑ', bl='a', w='a', base='a', accents=['brevecmb-cy'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=854),
   'adieresis-cy': GD(name='adieresis-cy', uni=0x04D3, hex='04D3', c='ӓ', bl='a', r='a', w='a', base='a', accents=['dieresiscmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=856),
   'aie-cy': GD(name='aie-cy', uni=0x04D5, hex='04D5', c='ӕ', bl='a', r='e', base='ae', isLower=True, anchors=['top', 'middle', 'bottom'], gid=858),

    #   b

   'be-cy': GD(name='be-cy', uni=0x0431, hex='0431', c='б', l='O', r='o', isLower=False, gid=694), # Behaves as capital
   'be-cy.loclSRB': GD(name='be-cy.loclSRB', l='be-cy', r='be-cy', isLower=True),

    #   c

   'che-cy': GD(name='che-cy', uni=0x0447, hex='0447', c='ч', r='en-cy', isLower=True, anchors=['top'], gid=716),
   'cheabkhasian-cy': GD(name='cheabkhasian-cy', uni=0x04BD, hex='04BD', c='ҽ', l='omod', r='e', isLower=True, gid=834),
   'chedescender-cy': GD(name='chedescender-cy', uni=0x04B7, hex='04B7', c='ҷ', l='che-cy', r='tse-cy', isLower=True, gid=828),
   'chedescenderabkhasian-cy': GD(name='chedescenderabkhasian-cy', uni=0x04BF, hex='04BF', c='ҿ', l='cheabkhasian-cy', r='e', base='cheabkhasian-cy', accents=['chedescenderabkhasian-cy.component'], isLower=True, gid=836),
   'chedescenderabkhasian-cy.component': GD(name='chedescenderabkhasian-cy.component', w=0, isLower=True, gid=1628),
   'chedieresis-cy': GD(name='chedieresis-cy', uni=0x04F5, hex='04F5', c='ӵ', l='che-cy', r='en-cy', base='che-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=890),
   'chekhakassian-cy': GD(name='chekhakassian-cy', uni=0x04CC, hex='04CC', c='ӌ', l='che-cy', r='en-cy', isLower=True, gid=849),
   'cheverticalstroke-cy': GD(name='cheverticalstroke-cy', uni=0x04B9, hex='04B9', c='ҹ', l='che-cy', r='en-cy', base='che-cy', isLower=True, anchors=['top'], gid=830),

    #   d

   'dasiapneumatacmb-cy': GD(name='dasiapneumatacmb-cy', uni=0x0485, hex='0485', c='҅', w=0, base='dasia', isLower=True, anchors=['top', '_top'], gid=778),
   'de-cy': GD(name='de-cy', uni=0x0434, hex='0434', c='д', r='o', isLower=True, gid=697, anchors=['top', 'middle', 'bottom']), # Italic variant has different shape.
   'de-cy.loclSRB': GD(name='de-cy.loclSRB', base='g', isLower=True, anchors=['top', 'middle', 'bottom']),
   'dje-cy': GD(name='dje-cy', uni=0x0452, hex='0452', c='ђ', l='hbar', isLower=True, gid=727),
   'dze-cy': GD(name='dze-cy', uni=0x0455, hex='0455', c='ѕ', l='s', r='s', base='s', isLower=True, anchors=['top', 'middle', 'bottom'], gid=730),
   'dzhe-cy': GD(name='dzhe-cy', uni=0x045F, hex='045F', c='џ', l='en-cy', r='en-cy', isLower=True, gid=740),

    #   e

   'e-cy': GD(name='e-cy', uni=0x0454, hex='0454', c='є', l='o', r='c', isLower=True, gid=729),
   'edieresis-cy': GD(name='edieresis-cy', uni=0x04ED, hex='04ED', c='ӭ', l='ereversed-cy', r='o', base='ereversed-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=882),
   'ef-cy': GD(name='ef-cy', uni=0x0444, hex='0444', c='ф', l2r='ef-cy', isLower=True, gid=713),
   'eiotified-cy': GD(name='eiotified-cy', uni=0x0465, hex='0465', c='ѥ', l='en-cy', r='c', isLower=True, gid=746),
   'el-cy': GD(name='el-cy', uni=0x043B, hex='043B', c='л', r='en-cy', isLower=True, gid=704),
   'eltail-cy': GD(name='eltail-cy', uni=0x04C6, hex='04C6', c='ӆ', l='el-cy', r='iishorttail-cy', base='el-cy', accents=['tail.component'], isLower=True, gid=843),
   'em-cy': GD(name='em-cy', uni=0x043C, hex='043C', c='м', l='en-cy', r='en-cy', isLower=True, gid=705),
   'emtail-cy': GD(name='emtail-cy', uni=0x04CE, hex='04CE', c='ӎ', l='en-cy', r='iishorttail-cy', base='em-cy', accents=['tail.component'], isLower=True, gid=851),
   'en-cy': GD(name='en-cy', uni=0x043D, hex='043D', c='н', l='off', l2r='en-cy', isLower=True, gid=706),
   'endescender-cy': GD(name='endescender-cy', uni=0x04A3, hex='04A3', c='ң', l='en-cy', r='tse-cy', isLower=True, gid=808),
   'enghe-cy': GD(name='enghe-cy', uni=0x04A5, hex='04A5', c='ҥ', l='en-cy', r='ge-cy', isLower=True, gid=810),
   'enhook-cy': GD(name='enhook-cy', uni=0x04C8, hex='04C8', c='ӈ', l='en-cy', r='j', isLower=True, gid=845),
   'entail-cy': GD(name='entail-cy', uni=0x04CA, hex='04CA', c='ӊ', l='en-cy', r='iishorttail-cy', base='en-cy', accents=['tail.component'], isLower=True, gid=847),
   'er-cy': GD(name='er-cy', uni=0x0440, hex='0440', c='р', l='p', r='p', base='p', isLower=True, anchors=['top', 'middle', 'bottom'], gid=709),
   'ereversed-cy': GD(name='ereversed-cy', uni=0x044D, hex='044D', c='э', r='o', isLower=True, anchors=['top'], gid=722),
   'ertick-cy': GD(name='ertick-cy', uni=0x048F, hex='048F', c='ҏ', l='p', w='p', base='p', isLower=True, anchors=['top', 'middle', 'bottom'], gid=788),
   'es-cy': GD(name='es-cy', uni=0x0441, hex='0441', c='с', l='c', r='c', base='c', isLower=True, anchors=['top', 'middle', 'bottom'], gid=710),
   'esdescender-cy': GD(name='esdescender-cy', uni=0x04AB, hex='04AB', c='ҫ', l='o', r='c', isLower=True, gid=816),

    #   f

   'fita-cy': GD(name='fita-cy', uni=0x0473, hex='0473', c='ѳ', l='o', r='o', isLower=True, gid=760),

    #   g

   'ge-cy': GD(name='ge-cy', uni=0x0433, hex='0433', c='г', l2r='s', r2l='s', isLower=True, anchors=['top', 'middle', 'bottom'], gid=696),
   'ge-cy.loclSRB': GD(name='ge-cy.loclSRB', l='imacron', r='imacron', base='imacron', isLower=True),
   'gedescender-cy': GD(name='gedescender-cy', uni=0x04F7, hex='04F7', c='ӷ', l='en-cy', r='ge-cy', isLower=True, gid=892),
   'gestrokehook-cy': GD(name='gestrokehook-cy', uni=0x04FB, hex='04FB', c='ӻ', r='ge-cy', base='ghestroke-cy', accents=['Gestrokehook-cy.component'], isLower=True, gid=896),
   'ghemiddlehook-cy': GD(name='ghemiddlehook-cy', uni=0x0495, hex='0495', c='ҕ', l='en-cy', r='o', isLower=True, gid=794),
   'ghestroke-cy': GD(name='ghestroke-cy', uni=0x0493, hex='0493', c='ғ', l='hyphen', r='ge-cy', isLower=True, gid=792),
   'gheupturn-cy': GD(name='gheupturn-cy', uni=0x0491, hex='0491', c='ґ', l='en-cy', r='ge-cy', isLower=True, gid=790),
   'gje-cy': GD(name='gje-cy', uni=0x0453, hex='0453', c='ѓ', base='ge-cy', accents=['acutecmb.uc'], isLower=True, anchors=['top'], gid=728),

    #   h

   'ha-cy': GD(name='ha-cy', uni=0x0445, hex='0445', c='х', l='x', r='x', base='x', isLower=True, anchors=['top', 'middle', 'bottom'], gid=714),
   'haabkhasian-cy': GD(name='haabkhasian-cy', uni=0x04A9, hex='04A9', c='ҩ', l='o', r='c', isLower=True, gid=814),
   'hadescender-cy': GD(name='hadescender-cy', uni=0x04B3, hex='04B3', c='ҳ', l='x', r='kadescender-cy', isLower=True, gid=824),
   'hahook-cy': GD(name='hahook-cy', uni=0x04FD, hex='04FD', c='ӽ', l='x', r='x', isLower=True, gid=898),
   'hardsign-cy': GD(name='hardsign-cy', uni=0x044A, hex='044A', c='ъ', l='te-cy', r='softsign-cy', isLower=True, gid=719),
   'hardsigncmb-cy': GD(name='hardsigncmb-cy', uni=0xA678, hex='A678', c='ꙸ', w=0, l='off', isLower=True, anchors=['_top'], gid=1579),
   'hastroke-cy': GD(name='hastroke-cy', uni=0x04FF, hex='04FF', c='ӿ', l='x', r='x', isLower=True, gid=900),

    #   i

   'i-cy': GD(name='i-cy', uni=0x0456, hex='0456', c='і', l='i', w='idotless', base='i', anchorBottomX='BottomX', anchorMiddleX='TopX', anchorTopX='TopX', isLower=True, anchors=['top', 'middle', 'bottom'], gid=731),
   'ia-cy': GD(name='ia-cy', uni=0x044F, hex='044F', c='я', r='en-cy', isLower=True, gid=724),
   'idieresis-cy': GD(name='idieresis-cy', uni=0x04E5, hex='04E5', c='ӥ', base='ii-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=874),
   'ie-cy': GD(name='ie-cy', uni=0x0435, hex='0435', c='е', l='o', w='e', base='e', isLower=True, anchors=['top', 'middle', 'bottom'], gid=698),
   'iebreve-cy': GD(name='iebreve-cy', uni=0x04D7, hex='04D7', c='ӗ', l='e', w='e', base='e', accents=['brevecmb-cy'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=860),
   'iegrave-cy': GD(name='iegrave-cy', uni=0x0450, hex='0450', c='ѐ', bl='o', w='e', base='e', accents=['gravecmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=725),
   'ii-cy': GD(name='ii-cy', uni=0x0438, hex='0438', c='и', l='en-cy', r='en-cy', bl='u', isLower=True, anchors=['top'], gid=701),
   'iigrave-cy': GD(name='iigrave-cy', uni=0x045D, hex='045D', c='ѝ', l='en-cy', r='en-cy', base='ii-cy', accents=['gravecmb.uc'], isLower=True, anchors=['top'], gid=738),
   'iishort-cy': GD(name='iishort-cy', uni=0x0439, hex='0439', c='й', l='en-cy', r='en-cy', base='ii-cy', accents=['brevecmb-cy'], isLower=True, anchors=['top'], gid=702),
   'iishorttail-cy': GD(name='iishorttail-cy', uni=0x048B, hex='048B', c='ҋ', l='en-cy', base='iishort-cy', accents=['tail.component'], isLower=True, anchors=['top'], gid=784),
   'imacron-cy': GD(name='imacron-cy', uni=0x04E3, hex='04E3', c='ӣ', l='en-cy', r='en-cy', base='ii-cy', accents=['macroncmb.uc'], isLower=True, anchors=['top'], gid=872),
   'io-cy': GD(name='io-cy', uni=0x0451, hex='0451', c='ё', l='o', r='e', base='e', accents=['dieresiscmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=726),
   'iu-cy': GD(name='iu-cy', uni=0x044E, hex='044E', c='ю', l='en-cy', r='o', isLower=True, gid=723),
   'izhitsa-cy': GD(name='izhitsa-cy', uni=0x0475, hex='0475', c='ѵ', l='v', isLower=True, anchorTopY='v', anchorTopX='v', anchors=['top'], gid=762),
   'izhitsadblgrave-cy': GD(name='izhitsadblgrave-cy', uni=0x0477, hex='0477', c='ѷ', bl='v', w='izhitsa-cy', base='izhitsa-cy', accents=['dblgravecmb.uc'], isLower=True, anchors=['top'], gid=764),

    #   j

   'je-cy': GD(name='je-cy', uni=0x0458, hex='0458', c='ј', l='j', r='j', base='j', isLower=True, anchors=['middle', 'bottom'], gid=733),

    #   k

   'ka-cy': GD(name='ka-cy', uni=0x043A, hex='043A', c='к', l='en-cy', r='k', base='kgreenlandic', isLower=True, anchors=['top'], gid=703),
   'kabashkir-cy': GD(name='kabashkir-cy', uni=0x04A1, hex='04A1', c='ҡ', l='te-cy', r='k', isLower=True, gid=806),
   'kadescender-cy': GD(name='kadescender-cy', uni=0x049B, hex='049B', c='қ', l='en-cy', r='zhedescender-cy', isLower=True, gid=800),
   'kahook-cy': GD(name='kahook-cy', uni=0x04C4, hex='04C4', c='ӄ', l='en-cy', isLower=True, gid=841),
   'kastroke-cy': GD(name='kastroke-cy', uni=0x049F, hex='049F', c='ҟ', r='k', l='hyphen', isLower=True, gid=804),
   'kaverticalstroke-cy': GD(name='kaverticalstroke-cy', uni=0x049D, hex='049D', c='ҝ', l='en-cy', r='k', isLower=True, gid=802),
   'kje-cy': GD(name='kje-cy', uni=0x045C, hex='045C', c='ќ', l='en-cy', r='k', base='kgreenlandic', accents=['acutecmb.uc'], isLower=True, anchors=['top'], gid=737),
   'koppa-cy': GD(name='koppa-cy', uni=0x0481, hex='0481', c='ҁ', l='o', r='c', isLower=True, gid=774),
   'ksi-cy': GD(name='ksi-cy', uni=0x046F, hex='046F', c='ѯ', r='ze-cy', isLower=True, gid=756),

    #   l

    #   m

    #   n

   'nje-cy': GD(name='nje-cy', uni=0x045A, hex='045A', c='њ', l='en-cy', r='softsign-cy', isLower=True, gid=735),

    #   o

   'o-cy': GD(name='o-cy', uni=0x043E, hex='043E', c='о', l2r='o', base='o', isLower=True, anchors=['top', 'middle', 'bottom'], gid=707),
   'obarred-cy': GD(name='obarred-cy', uni=0x04E9, hex='04E9', c='ө', l='o', r='o', isLower=True, anchors=['top'], gid=878),
   'obarreddieresis-cy': GD(name='obarreddieresis-cy', uni=0x04EB, hex='04EB', c='ӫ', l='o', r='o', base='obarred-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=880),
   'odieresis-cy': GD(name='odieresis-cy', uni=0x04E7, hex='04E7', c='ӧ', bl='o', w='o', base='o', accents=['dieresiscmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=876),
   'omega-cy': GD(name='omega-cy', uni=0x0461, hex='0461', c='ѡ', l='off', l2r='omega-cy', isLower=True, anchors=['top'], gid=742),

    #   p

   'palatalizationcmb-cy': GD(name='palatalizationcmb-cy', uni=0x0484, hex='0484', c='҄', w=0, isLower=True, anchors=['top', '_top'], gid=777),
   'palochka-cy': GD(name='palochka-cy', uni=0x04CF, hex='04CF', c='ӏ', l='h', l2r='h', isLower=True, anchors=['top', 'middle', 'bottom'], gid=852),
   'pe-cy': GD(name='pe-cy', uni=0x043F, hex='043F', c='п', l='p', r='o', isLower=True, gid=708),
   'pe-cy.loclSRB': GD(name='pe-cy.loclSRB', base='umacron', isLower=True),
   'pedescender-cy': GD(name='pedescender-cy', uni=0x0525, hex='0525', c='ԥ', l='en-cy', r='tse-cy', isLower=True, gid=902),
   'pedescender-cy.component': GD(name='pedescender-cy.component', w=0, isLower=True, gid=1681),
   'pemiddlehook-cy': GD(name='pemiddlehook-cy', uni=0x04A7, hex='04A7', c='ҧ', l='en-cy', r='o', isLower=True, gid=812),
   'psi-cy': GD(name='psi-cy', uni=0x0471, hex='0471', c='ѱ', r='n', isLower=True, gid=758),
   'psilipneumatacmb-cy': GD(name='psilipneumatacmb-cy', uni=0x0486, hex='0486', c='҆', w=0, base='psili', isLower=True, anchors=['top', '_top'], gid=779),

    #   q

    #   r

    #   s

   'schwa-cy': GD(name='schwa-cy', uni=0x04D9, hex='04D9', c='ә', r='o', base='schwa', isLower=True, anchors=['top'], gid=862),
   'schwadieresis-cy': GD(name='schwadieresis-cy', uni=0x04DB, hex='04DB', c='ӛ', l='schwa-cy', r='o', base='schwa-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=864),
   'semisoftsign-cy': GD(name='semisoftsign-cy', uni=0x048D, hex='048D', c='ҍ', r='softsign-cy', isLower=True, gid=786),
   'sha-cy': GD(name='sha-cy', uni=0x0448, hex='0448', c='ш', l='en-cy', r='en-cy', isLower=True, gid=717),
   'shcha-cy': GD(name='shcha-cy', uni=0x0449, hex='0449', c='щ', l='en-cy', r='tse-cy', isLower=True, gid=718),
   'shha-cy': GD(name='shha-cy', uni=0x04BB, hex='04BB', c='һ', l='h', r='h', base='h', isLower=True, anchors=['top', 'middle', 'bottom'], gid=832),
   'softsign-cy': GD(name='softsign-cy', uni=0x044C, hex='044C', c='ь', l='en-cy', isLower=True, gid=721),
   'softsigncmb-cy': GD(name='softsigncmb-cy', uni=0xA67A, hex='A67A', c='ꙺ', w=0, l='off', isLower=True, anchors=['_top'], gid=1580),

    #   t

   'te-cy': GD(name='te-cy', uni=0x0442, hex='0442', c='т', l2r='te-cy', isLower=True, gid=711),
   'te-cy.loclSRB': GD(name='te-cy.loclSRB', base='sha-cy', accents=['macroncmb.uc'], isLower=True),
   'tedescender-cy': GD(name='tedescender-cy', uni=0x04AD, hex='04AD', c='ҭ', l='te-cy', r='te-cy', isLower=True, gid=818),
   'tetse-cy': GD(name='tetse-cy', uni=0x04B5, hex='04B5', c='ҵ', l='te-cy', r='tse-cy', isLower=True, gid=826),
   'thousand-cy': GD(name='thousand-cy', uni=0x0482, hex='0482', c='҂', isLower=True, gid=775),
   'titlocmb-cy': GD(name='titlocmb-cy', uni=0x0483, hex='0483', c='҃', w=0, isLower=True, anchors=['top', '_top'], gid=776),
   'tse-cy': GD(name='tse-cy', uni=0x0446, hex='0446', c='ц', l='en-cy', isLower=True, gid=715),
   'tshe-cy': GD(name='tshe-cy', uni=0x045B, hex='045B', c='ћ', l='hbar', r='hbar', isLower=True, gid=736),

    #   u

   'u-cy': GD(name='u-cy', uni=0x0443, hex='0443', c='у', l='y', r='y', base='y', isLower=True, anchors=['top', 'middle', 'bottom'], gid=712),
   'udieresis-cy': GD(name='udieresis-cy', uni=0x04F1, hex='04F1', c='ӱ', l='y', r='y', base='y', accents=['dieresiscmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=886),
   'uhungarumlaut-cy': GD(name='uhungarumlaut-cy', uni=0x04F3, hex='04F3', c='ӳ', l='y', w='y', base='y', accents=['hungarumlautcmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=888),
   'uk-cy': GD(name='uk-cy', uni=0x0479, hex='0479', c='ѹ', l='o', r='izhitsa-cy', isLower=True, gid=766),
   'umacron-cy': GD(name='umacron-cy', uni=0x04EF, hex='04EF', c='ӯ', l='y', r='y', base='y', accents=['macroncmb.uc'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=884),
   'ushort-cy': GD(name='ushort-cy', uni=0x045E, hex='045E', c='ў', l='y', r='y', base='y', accents=['brevecmb-cy'], isLower=True, anchors=['top', 'middle', 'bottom'], gid=739),
   'ustrait-cy': GD(name='ustrait-cy', uni=0x04AF, hex='04AF', c='ү', l='v', l2r='ustrait-cy', isLower=True, gid=820),
   'ustraitstroke-cy': GD(name='ustraitstroke-cy', uni=0x04B1, hex='04B1', c='ұ', l='ustrait-cy', r='ustrait-cy', isLower=True, gid=822),

    #   v

   've-cy': GD(name='ve-cy', uni=0x0432, hex='0432', c='в', l='n', isLower=True, gid=695),

    #   w

    #   x

    #   y

   'yat-cy': GD(name='yat-cy', uni=0x0463, hex='0463', c='ѣ', r='softsign-cy', isLower=True, gid=744),
   'yeru-cy': GD(name='yeru-cy', uni=0x044B, hex='044B', c='ы', l='en-cy', r='en-cy', isLower=True, anchors=['top'], gid=720),
   'yerudieresis-cy': GD(name='yerudieresis-cy', uni=0x04F9, hex='04F9', c='ӹ', l='en-cy', r='en-cy', base='yeru-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=894),
   'yi-cy': GD(name='yi-cy', uni=0x0457, hex='0457', c='ї', w='idotless', bl='idotless', base='idotless', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=732),
   'yusbig-cy': GD(name='yusbig-cy', uni=0x046B, hex='046B', c='ѫ', l2r='yusbig-cy', isLower=True, gid=752),
   'yusbigiotified-cy': GD(name='yusbigiotified-cy', uni=0x046D, hex='046D', c='ѭ', l='en-cy', r='yusbig-cy', isLower=True, gid=754),
   'yuslittle-cy': GD(name='yuslittle-cy', uni=0x0467, hex='0467', c='ѧ', l2r='yuslittle-cy', isLower=True, gid=748),
   'yuslittleiotified-cy': GD(name='yuslittleiotified-cy', uni=0x0469, hex='0469', c='ѩ', l='en-cy', r='yuslittle-cy', isLower=True, gid=750),

    #   z

   'ze-cy': GD(name='ze-cy', uni=0x0437, hex='0437', c='з', r='ve-cy', isLower=True, anchors=['top'], gid=700),
   'zedescender-cy': GD(name='zedescender-cy', uni=0x0499, hex='0499', c='ҙ', l='ze-cy', r='ve-cy', isLower=True, gid=798),
   'zedieresis-cy': GD(name='zedieresis-cy', uni=0x04DF, hex='04DF', c='ӟ', l='ze-cy', r='ve-cy', base='ze-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=868),
   'zhe-cy': GD(name='zhe-cy', uni=0x0436, hex='0436', c='ж', r='k', isLower=True, anchors=['top'], gid=699),
   'zhebreve-cy': GD(name='zhebreve-cy', uni=0x04C2, hex='04C2', c='ӂ', l='zhe-cy', r='zhe-cy', base='zhe-cy', accents=['brevecmb-cy'], isLower=True, anchors=['top'], gid=839),
   'zhedescender-cy': GD(name='zhedescender-cy', uni=0x0497, hex='0497', c='җ', l='zhe-cy', isLower=True, gid=796),
   'zhedieresis-cy': GD(name='zhedieresis-cy', uni=0x04DD, hex='04DD', c='ӝ', l='zhe-cy', r='zhe-cy', base='zhe-cy', accents=['dieresiscmb.uc'], isLower=True, anchors=['top'], gid=866),
}
