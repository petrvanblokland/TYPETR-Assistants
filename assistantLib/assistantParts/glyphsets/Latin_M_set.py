# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_M_set.py
#    https://github.com/koeberlin/Latin-Character-Sets
#
#    From https://github.com/koeberlin/Latin-Character-Sets/blob/main/README.md:
#
#    Latin S
#    There’s nothing extended about what’s most often referred to as Latin Extended. 
#    Latin S is a new approach to a handy base character set that doesn’t take much more effort, 
#    but has a rather big impact on language support.
#
#    Here’s a closer look at it: Designing Latin S
#    Compared to the common practice, it 
#       • requires ≈80 additional glyphs (most of which are composites of existing glyphs though, such as Ẽǒʼ).
#       • supports about 100 extra languages3, such as Azerbaijani (37M speakers), Ga (8.5M), 
#         Paraguayan Guaraní (6.5M), Hausa (40M), Igbo (27M), Lingála (15M), Úmbúndú (9.5M), Yorùbá (40M) …
#       • serves about 200,000,000 additional speakers
#    Btw, it includes the Pan-Nigerian alphabet and therefore does support the languages of the seventh 
#    most populous country in the world! 💯
#
#    Latin M
#    Latin M is mainly about stacking accents for Vietnamese (76M speakers). 
#    And while you’re at it, you might want to add support for Pinyin and the romanization of 
#    Semitic languages and Sanskrit.
#
#    Requires 144 additional glyphs (≈90% composites of existing glyphs)
#
#    Latin S + Latin M
#    AÁĂǍÂÄẠÀĀĄÅÃÆBḄƁCĆČÇĈĊDÐĎĐḌƊEÉĔĚÊËĖẸÈĒĘƐƎẼFGĞĜĢĠḠǦHĦĤḦḤIÍĬǏÎÏİỊÌĪĮƗĨJĴKĶƘLĹĽĻŁMNŃŇŅṄṆƝÑŊ
#    OÓŎǑÔÖỌÒŐŌƆØÕŒPṖÞQRŔŘŖSŚŠŞŜȘṢẞƏTŤŢȚUÚŬǓÛÜỤÙŰŪŲŮŨVɅWẂŴẄẀXẌYÝŶŸỲƳỸȲZŹŽŻẒaáăǎâäạàāąåãæbḅɓcć
#    čçĉċdðďđḍɗeéĕěêëėẹèēęɛẽǝəfgğĝģġḡǧhħĥḧḥiıíĭǐîïịìīįɨĩjȷĵkķƙlĺľļłmnńňņṅṇɲñŋoóŏǒôöọòőōɔøõœpṗ
#    þqrŕřŗsśšşŝșṣßtťţțuúŭǔûüụùűūųůũvʌwẃŵẅẁxẍyýŷÿỳƴỹȳzźžżẓ₵₡₲₺₼₦₹ ̈ ̇ ̀ ́ ̋ ̂ ̌ ̆ ̊ ̃ ̄ ̒ ̣ ̦ ̧ ̨ʼʻ ̵
#    ẮẶẰẲẴẤẬẦẨẪẢǢḎẾỆỀỂỄẺḪḨỈḲḴḶḸḺṀṂṈỐỘỒỔỖỎƠỚỢỜỞỠṘṚṜṞṬṮǗǙǛǕỦƯỨỰỪỬỮẈẎỴỶẔ
#    ắặằẳẵấậầẩẫảǣḏếệềểễẻḫḩẖỉḳḵḷḹḻṁṃṉốộồổỗỏơớợờởỡṙṛṝṟṭṯǘǚǜǖủưứựừửữẉẏỵỷẕ₫
#
#    See README.md for list of supported languages and recommendations for the OpenType code.
#
#    This is an example of a glyphset definition, derived from another one.
#    Don't forget to make a deepcopy first, before altering anything.
#
from copy import deepcopy

if __name__ == '__main__': # Used for doc tests to find assistantLib
    import os, sys
    PATH = '/'.join(__file__.split('/')[:-4]) # Relative path to this respository that holds AssistantLib
    if not PATH in sys.path:
        sys.path.append(PATH)

from assistantLib.assistantParts.glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_ etc.
from assistantLib.assistantParts.glyphsets.Latin_S_set import (
    LATIN_S_SET_LANGUAGES, LATIN_S_SET, LATIN_S_SET_ITALIC)

LATIN_M_SET_NAME = 'Latin M'
LATIN_M_SET_NAME_ITALIC = 'Latin M Italic'

LATIN_M_SET_LANGUAGES = (
    'Asturian', 'Falam Chin', 'Hakha Chin', 'Madurese', 'Mezquital Otomi', 'Mizo', 
    'Secoya', 'Siona', 'Totontepec Mixe', 'Vietnamese',
) 

# The "c" attributes are redundant, if the @uni or @hex are defined, but they offer easy searching in the source by char.

LATIN_M_SET = deepcopy(LATIN_S_SET)
LATIN_M_SET_ITALIC = deepcopy(LATIN_S_SET_ITALIC)

# Latin M unicodes
#
#    0x01a0, 0x01a1, 0x01af, 0x01b0, 0x01d5, 0x01d6, 0x01d7, 0x01d8, 0x01d9, 0x01da, 0x01db, 0x01dc, 0x01e2, 0x01e3, 
#    0x02be, 0x02bf, 0x0309, 0x031b, 0x032e, 0x0331, 0x1e0e, 0x1e0f, 0x1e28, 0x1e29, 0x1e2a, 0x1e2b, 0x1e32, 0x1e33, 
#    0x1e34, 0x1e35, 0x1e36, 0x1e37, 0x1e38, 0x1e39, 0x1e3a, 0x1e3b, 0x1e40, 0x1e41, 0x1e42, 0x1e43, 0x1e48, 0x1e49, 
#    0x1e58, 0x1e59, 0x1e5a, 0x1e5b, 0x1e5c, 0x1e5d, 0x1e5e, 0x1e5f, 0x1e6c, 0x1e6d, 0x1e6e, 0x1e6f, 0x1e88, 0x1e89, 
#    0x1e8e, 0x1e8f, 0x1e94, 0x1e95, 0x1e96, 0x1ea2, 0x1ea3, 0x1ea4, 0x1ea5, 0x1ea6, 0x1ea7, 0x1ea8, 0x1ea9, 0x1eaa, 
#    0x1eab, 0x1eac, 0x1ead, 0x1eae, 0x1eaf, 0x1eb0, 0x1eb1, 0x1eb2, 0x1eb3, 0x1eb4, 0x1eb5, 0x1eb6, 0x1eb7, 0x1eba, 
#    0x1ebb, 0x1ebe, 0x1ebf, 0x1ec0, 0x1ec1, 0x1ec2, 0x1ec3, 0x1ec4, 0x1ec5, 0x1ec6, 0x1ec7, 0x1ec8, 0x1ec9, 0x1ece, 
#    0x1ecf, 0x1ed0, 0x1ed1, 0x1ed2, 0x1ed3, 0x1ed4, 0x1ed5, 0x1ed6, 0x1ed7, 0x1ed8, 0x1ed9, 0x1eda, 0x1edb, 0x1edc, 
#    0x1edd, 0x1ede, 0x1edf, 0x1ee0, 0x1ee1, 0x1ee2, 0x1ee3, 0x1ee6, 0x1ee7, 0x1ee8, 0x1ee9, 0x1eea, 0x1eeb, 0x1eec, 
#    0x1eed, 0x1eee, 0x1eef, 0x1ef0, 0x1ef1, 0x1ef4, 0x1ef5, 0x1ef6, 0x1ef7, 0x20ab
#

for GDS in (LATIN_M_SET, LATIN_M_SET_ITALIC):

    # A

    GDS['AEmacron'] = GD(name='AEmacron', uni=0x01E2, hex='01E2', c='Ǣ', l='A', r='E', base='AE', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top'], gid=419)
    GDS['Abreveacute'] = GD(name='Abreveacute', uni=0x1EAE, hex='1EAE', c='Ắ', l='A', r='A', base='A', accents=['breveacutecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1097, comment='Ắ LATIN CAPITAL LETTER A WITH BREVE AND ACUTE')
    GDS['Abrevedotbelow'] = GD(name='Abrevedotbelow', uni=0x1EB6, hex='1EB6', c='Ặ', l='A', r='A', base='Abreve', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1105, comment='Ặ LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW')
    GDS['Abrevegrave'] = GD(name='Abrevegrave', uni=0x1EB0, hex='1EB0', c='Ằ', l='A', r='A', base='A', accents=['brevegravecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1099, comment='Ằ LATIN CAPITAL LETTER A WITH BREVE AND GRAVE')
    GDS['Abrevehookabove'] = GD(name='Abrevehookabove', uni=0x1EB2, hex='1EB2', c='Ẳ', l='A', r='A', base='A', accents=['brevehookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1101, comment='Ẳ LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE')
    GDS['Abrevetilde'] = GD(name='Abrevetilde', uni=0x1EB4, hex='1EB4', c='Ẵ', l='A', r='A', base='A', accents=['brevetildecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1103, comment='Ẵ LATIN CAPITAL LETTER A WITH BREVE AND TILDE')
    GDS['Acircumflexacute'] = GD(name='Acircumflexacute', uni=0x1EA4, hex='1EA4', c='Ấ', l='A', w='A', base='A', accents=['circumflexacutecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1087, comment='Ấ LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE')
    GDS['Acircumflexdotbelow'] = GD(name='Acircumflexdotbelow', uni=0x1EAC, hex='1EAC', c='Ậ', l='A', r='A', base='Acircumflex', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1095, comment='Ậ LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND DOT BELOW')
    GDS['Acircumflexgrave'] = GD(name='Acircumflexgrave', uni=0x1EA6, hex='1EA6', c='Ầ', w='A', bl='A', base='A', accents=['circumflexgravecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1089, comment='Ầ LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE')
    GDS['Acircumflexhookabove'] = GD(name='Acircumflexhookabove', uni=0x1EA8, hex='1EA8', c='Ẩ', l='A', r='A', base='A', accents=['circumflexhookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1091, comment='Ẩ LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE')
    GDS['Acircumflextilde'] = GD(name='Acircumflextilde', uni=0x1EAA, hex='1EAA', c='Ẫ', l='A', r='A', base='A', accents=['circumflextildecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1093, comment='Ẫ LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE')
    GDS['Ahookabove'] = GD(name='Ahookabove', uni=0x1EA2, hex='1EA2', c='Ả', l='A', r='A', base='A', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1085, comment='Ả LATIN CAPITAL LETTER A WITH HOOK ABOVE')

    # D

    GDS['Dlinebelow'] = GD(name='Dlinebelow', uni=0x1E0E, hex='1E0E', c='Ḏ', base='D', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=937)

    # E

    GDS['Ecircumflexacute'] = GD(name='Ecircumflexacute', uni=0x1EBE, hex='1EBE', c='Ế', l='H', w='E', base='E', accents=['circumflexacutecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1113, comment='Ế LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE')
    GDS['Ecircumflexdotbelow'] = GD(name='Ecircumflexdotbelow', uni=0x1EC6, hex='1EC6', c='Ệ', w='E', bl='H', base='Ecircumflex', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1121, comment='Ệ LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW')
    GDS['Ecircumflexgrave'] = GD(name='Ecircumflexgrave', uni=0x1EC0, hex='1EC0', c='Ề', w='E', bl='E', base='E', accents=['circumflexgravecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1115, comment='Ề LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE')
    GDS['Ecircumflexhookabove'] = GD(name='Ecircumflexhookabove', uni=0x1EC2, hex='1EC2', c='Ể', w='E', bl='H', base='E', accents=['circumflexhookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1117, comment='Ể LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE')
    GDS['Ecircumflextilde'] = GD(name='Ecircumflextilde', uni=0x1EC4, hex='1EC4', c='Ễ', l='H', r='E', base='E', accents=['circumflextildecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1119, comment='Ễ LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE')
    GDS['Ehookabove'] = GD(name='Ehookabove', uni=0x1EBA, hex='1EBA', c='Ẻ', l='H', r='E', base='E', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1109, comment='Ẻ LATIN CAPITAL LETTER E WITH HOOK ABOVE')

    # H

    GDS['Hbrevebelow'] = GD(name='Hbrevebelow', uni=0x1E2A, hex='1E2A', c='Ḫ', l='H', r='H', base='H', accents=['brevebelowcmb'], anchors=['bottom', 'middle', 'top'], gid=965)
    GDS['Hcedilla'] = GD(name='Hcedilla', uni=0x1E28, hex='1E28', c='Ḩ', w='H', base='H', autoFixComponentPositions=False, accents=['cedillacmb'], fixAccents=False, anchors=['bottom', 'middle', 'top'], gid=963)

    # Separate, because it's sourcefor all other .sc
    GDS['H.sc'] = GD(name='H.sc', fixAccents=False, anchors=['bottom', 'middle', 'top'])

    # I

    GDS['Ihookabove'] = GD(name='Ihookabove', uni=0x1EC8, hex='1EC8', c='Ỉ', w='I', bl='I', base='I', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1123, comment='Ỉ LATIN CAPITAL LETTER I WITH HOOK ABOVE')

    # K

    GDS['Kdotbelow'] = GD(name='Kdotbelow', uni=0x1E32, hex='1E32', c='Ḳ', l='H', r='K', base='K', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=973)
    GDS['Klinebelow'] = GD(name='Klinebelow', uni=0x1E34, hex='1E34', c='Ḵ', l='H', r='K', base='K', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=975)

    # L

    GDS['Ldotbelow'] = GD(name='Ldotbelow', uni=0x1E36, hex='1E36', c='Ḷ', l='H', r='L', base='L', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=977)
    GDS['Ldotbelowmacron'] = GD(name='Ldotbelowmacron', uni=0x1E38, hex='1E38', c='Ḹ', l='H', r='L', base='Ldotbelow', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top'], gid=979)
    GDS['Llinebelow'] = GD(name='Llinebelow', uni=0x1E3A, hex='1E3A', c='Ḻ', l='H', r='L', base='L', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=981)

    # M

    GDS['Mdotaccent'] = GD(name='Mdotaccent', uni=0x1E40, hex='1E40', c='Ṁ', l='H', r='H', base='M', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], gid=987)
    GDS['Mdotbelow'] = GD(name='Mdotbelow', uni=0x1E42, hex='1E42', c='Ṃ', l='H', r='H', base='M', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=989)

    # N

    GDS['Nlinebelow'] = GD(name='Nlinebelow', uni=0x1E48, hex='1E48', c='Ṉ', l='H', r='H', base='N', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=995)

    # O

    GDS['Ocircumflexacute'] = GD(name='Ocircumflexacute', uni=0x1ED0, hex='1ED0', c='Ố', l='O', w='O', base='O', accents=['circumflexacutecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1131, comment='Ố LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE')
    GDS['Ocircumflexdotbelow'] = GD(name='Ocircumflexdotbelow', uni=0x1ED8, hex='1ED8', c='Ộ', l='O', r='O', base='Ocircumflex', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1139, comment='Ộ LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW')
    GDS['Ocircumflexgrave'] = GD(name='Ocircumflexgrave', uni=0x1ED2, hex='1ED2', c='Ồ', w='O', bl='O', base='O', accents=['circumflexgravecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1133, comment='Ồ LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE')
    GDS['Ocircumflexhookabove'] = GD(name='Ocircumflexhookabove', uni=0x1ED4, hex='1ED4', c='Ổ', l='O', w='O', base='O', accents=['circumflexhookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1135, comment='Ổ LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE')
    GDS['Ocircumflextilde'] = GD(name='Ocircumflextilde', uni=0x1ED6, hex='1ED6', c='Ỗ', l='O', r='O', base='O', accents=['circumflextildecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1137, comment='Ỗ LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE')
    GDS['Ohookabove'] = GD(name='Ohookabove', uni=0x1ECE, hex='1ECE', c='Ỏ', base='O', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1129, comment='Ỏ LATIN CAPITAL LETTER O WITH HOOK ABOVE')
    GDS['Ohorn'] = GD(name='Ohorn', uni=0x01A0, hex='01A0', c='Ơ', l='O', w='O', base='O', accents=['horncmb.uc'], autoFixComponentPositions=False, anchorTopX='O', anchorTopY='O', anchors=['bottom', 'middle', 'top'], gid=353, comment='Ơ')
    GDS['Ohornacute'] = GD(name='Ohornacute', uni=0x1EDA, hex='1EDA', c='Ớ', l='O', anchorTopY='O', anchorTopX='O', base='Ohorn', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1141, comment='Ớ LATIN CAPITAL LETTER O WITH HORN AND ACUTE')
    GDS['Ohorndotbelow'] = GD(name='Ohorndotbelow', uni=0x1EE2, hex='1EE2', c='Ợ', l='O', anchorTopY='O', anchorTopX='O', base='Ohorn', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1149, comment='Ợ LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW')
    GDS['Ohorngrave'] = GD(name='Ohorngrave', uni=0x1EDC, hex='1EDC', c='Ờ', l='O', anchorTopY='O', anchorTopX='O', base='Ohorn', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1143, comment='Ờ LATIN CAPITAL LETTER O WITH HORN AND GRAVE')
    GDS['Ohornhookabove'] = GD(name='Ohornhookabove', uni=0x1EDE, hex='1EDE', c='Ở', l='O', anchorTopY='O', anchorTopX='O', base='Ohorn', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1145, comment='Ở LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE')
    GDS['Ohorntilde'] = GD(name='Ohorntilde', uni=0x1EE0, hex='1EE0', c='Ỡ', l='O', anchorTopY='O', anchorTopX='O', base='Ohorn', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1147, comment='Ỡ LATIN CAPITAL LETTER O WITH HORN AND TILDE')
    # Assumes that the Greek /Omega exists. Otherwise overwrite the GlyphData with a real outline.
    GDS['Ohm'] = GD(name='Ohm', uni=0x2126, hex='2126', c='Ω', l='O', l2r='self', base='Omega', anchors=['top', 'bottom', 'topleft'])

    # R

    GDS['Rdotaccent'] = GD(name='Rdotaccent', uni=0x1E58, hex='1E58', c='Ṙ', l='H', r='R', base='R', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1011)
    GDS['Rdotbelow'] = GD(name='Rdotbelow', uni=0x1E5A, hex='1E5A', c='Ṛ', l='H', r='R', base='R', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1013)
    GDS['Rdotbelowmacron'] = GD(name='Rdotbelowmacron', uni=0x1E5C, hex='1E5C', c='Ṝ', l='H', r='R', base='Rdotbelow', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1015)
    GDS['Rlinebelow'] = GD(name='Rlinebelow', uni=0x1E5E, hex='1E5E', c='Ṟ', base='R', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1017)

    # T

    GDS['Tdotbelow'] = GD(name='Tdotbelow', uni=0x1E6C, hex='1E6C', c='Ṭ', l='T', r='T', base='T', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1031)
    GDS['Tlinebelow'] = GD(name='Tlinebelow', uni=0x1E6E, hex='1E6E', c='Ṯ', l='T', r='T', base='T', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1033)

    # U

    GDS['Udieresisacute'] = GD(name='Udieresisacute', uni=0x01D7, hex='01D7', c='Ǘ', l='U', r='U', base='U', accents=['dieresisacutecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=408)
    GDS['Udieresiscaron'] = GD(name='Udieresiscaron', uni=0x01D9, hex='01D9', c='Ǚ', l='U', r='U', base='U', accents=['dieresiscaroncmb.uc'], anchors=['bottom', 'middle', 'top'], gid=410)
    GDS['Udieresisgrave'] = GD(name='Udieresisgrave', uni=0x01DB, hex='01DB', c='Ǜ', l='U', r='U', base='U', accents=['dieresisgravecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=412)
    GDS['Udieresismacron'] = GD(name='Udieresismacron', uni=0x01D5, hex='01D5', c='Ǖ', l='U', r='U', base='U', accents=['dieresismacroncmb.uc'], anchors=['bottom', 'middle', 'top'], gid=406)
    GDS['Uhookabove'] = GD(name='Uhookabove', uni=0x1EE6, hex='1EE6', c='Ủ', l='U', r='U', base='U', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ủ LATIN CAPITAL LETTER U WITH HOOK ABOVE')
    GDS['Uhorn'] = GD(name='Uhorn', uni=0x01AF, hex='01AF', c='Ư', l='U', anchorTopY='U', anchorTopX='U', rightMin='minRight', autoFixComponentPositions=False, base='U', accents=['horncmb.uc'], anchors=['bottom', 'top'], gid=368, comment='Ư LATIN CAPITAL LETTER U WITH HORN')
    GDS['Uhornacute'] = GD(name='Uhornacute', uni=0x1EE8, hex='1EE8', c='Ứ', l='U', r='Uhorn', anchorTopY='U', anchorTopX='U', rightMin='minRight', base='Uhorn', accents=['acutecmb.uc'], anchors=['bottom', 'top'], gid=1155, comment='Ứ LATIN CAPITAL LETTER U WITH HORN AND ACUTE')
    GDS['Uhorndotbelow'] = GD(name='Uhorndotbelow', uni=0x1EF0, hex='1EF0', c='Ự', l='U', r='Uhorn', anchorTopX='U', anchorTopY='U', rightMin='minRight', base='Uhorn', accents=['dotbelowcmb'], anchors=['bottom', 'top'], gid=1163, comment='Ự LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW')
    GDS['Uhorngrave'] = GD(name='Uhorngrave', uni=0x1EEA, hex='1EEA', c='Ừ', l='U', r='Uhorn', anchorTopY='U', anchorTopX='U', rightMin='minRight', base='Uhorn', accents=['gravecmb.uc'], anchors=['bottom', 'top'], gid=1157, comment='Ừ LATIN CAPITAL LETTER U WITH HORN AND GRAVE')
    GDS['Uhornhookabove'] = GD(name='Uhornhookabove', uni=0x1EEC, hex='1EEC', c='Ử', l='U', r='Uhorn', anchorTopY='U', anchorTopX='U', rightMin='minRight', base='Uhorn', accents=['hookabovecmb.uc'], anchors=['bottom', 'top'], gid=1159, comment='Ử LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE')
    GDS['Uhorntilde'] = GD(name='Uhorntilde', uni=0x1EEE, hex='1EEE', c='Ữ', l='U', r='Uhorn', anchorTopY='U', anchorTopX='U', rightMin='minRight', base='Uhorn', accents=['tildecmb.uc'], anchors=['bottom', 'top'], gid=1161, comment='Ữ LATIN CAPITAL LETTER U WITH HORN AND TILDE')

    # W

    GDS['Wdotbelow'] = GD(name='Wdotbelow', uni=0x1E88, hex='1E88', c='Ẉ', l='W', r='W', base='W', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1059)

    # Y

    GDS['Ydotaccent'] = GD(name='Ydotaccent', uni=0x1E8E, hex='1E8E', c='Ẏ', l='Y', r='Y', base='Y', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1065)
    GDS['Ydotbelow'] = GD(name='Ydotbelow', uni=0x1EF4, hex='1EF4', c='Ỵ', l='Y', r='Y', base='Y', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1167, comment='Ỵ LATIN CAPITAL LETTER Y WITH DOT BELOW')
    GDS['Yhookabove'] = GD(name='Yhookabove', uni=0x1EF6, hex='1EF6', c='Ỷ', l='Y', r='Y', base='Y', accents=['hookabovecmb.uc'], anchors=['bottom', 'middle', 'top'], gid=1169, comment='Ỷ LATIN CAPITAL LETTER Y WITH HOOK ABOVE')

    # Z

    GDS['Zlinebelow'] = GD(name='Zlinebelow', uni=0x1E94, hex='1E94', c='Ẕ', l='Z', r='Z', base='Z', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'], gid=1071)

    # a

    GDS['abreveacute'] = GD(name='abreveacute', uni=0x1EAF, hex='1EAF', c='ắ', l='a', w='a', base='a', accents=['breveacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1098, comment='ắ LATIN SMALL LETTER A WITH BREVE AND ACUTE')
    GDS['abrevedotbelow'] = GD(name='abrevedotbelow', uni=0x1EB7, hex='1EB7', c='ặ', l='a', w='a', base='a', accents=['brevecmb', 'dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1106, comment='ặ LATIN SMALL LETTER A WITH BREVE AND DOT BELOW')
    GDS['abrevegrave'] = GD(name='abrevegrave', uni=0x1EB1, hex='1EB1', c='ằ', l='a', w='a', base='a', accents=['brevegravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1100, comment='ằ LATIN SMALL LETTER A WITH BREVE AND GRAVE')
    GDS['abrevehookabove'] = GD(name='abrevehookabove', uni=0x1EB3, hex='1EB3', c='ẳ', l='a', w='a', base='a', accents=['brevehookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1102, comment='ẳ LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE')
    GDS['abrevetilde'] = GD(name='abrevetilde', uni=0x1EB5, hex='1EB5', c='ẵ', l='a', w='a', base='a', accents=['brevetildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1104, comment='ẵ LATIN SMALL LETTER A WITH BREVE AND TILDE')
    GDS['acircumflexacute'] = GD(name='acircumflexacute', uni=0x1EA5, hex='1EA5', c='ấ', w='a', bl='a', base='a', accents=['circumflexacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1088, comment='ấ LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE')
    GDS['acircumflexdotbelow'] = GD(name='acircumflexdotbelow', uni=0x1EAD, hex='1EAD', c='ậ', w='a', bl='a', base='acircumflex', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1096, comment='ậ LATIN SMALL LETTER A WITH CIRCUMFLEX AND DOT BELOW')
    GDS['acircumflexgrave'] = GD(name='acircumflexgrave', uni=0x1EA7, hex='1EA7', c='ầ', w='a', bl='a', base='a', accents=['circumflexgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1090, comment='ầ LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE')
    GDS['acircumflexhookabove'] = GD(name='acircumflexhookabove', uni=0x1EA9, hex='1EA9', c='ẩ', w='a', bl='a', base='a', accents=['circumflexhookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1092, comment='ẩ LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE')
    GDS['acircumflextilde'] = GD(name='acircumflextilde', uni=0x1EAB, hex='1EAB', c='ẫ', w='a', bl='a', base='a', accents=['circumflextildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1094, comment='ẫ LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE')
    GDS['aemacron'] = GD(name='aemacron', uni=0x01E3, hex='01E3', c='ǣ', r='e', bl='a', base='ae', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=420)
    GDS['ahookabove'] = GD(name='ahookabove', uni=0x1EA3, hex='1EA3', c='ả', w='a', bl='a', base='a', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1086, comment='ả A WITH HOOK ABOVE, LATIN SMALL LETTER')

    # b

    # Should not exist as separate width glyph without unicode. Unicode of /brevebelowcmb is 032E
    #GDS['brevebelow'] = GD(name='brevebelow', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='brevebelowcmb', isLower=True, anchors=[], gid=1623)

    # d

    GDS['dlinebelow'] = GD(name='dlinebelow', uni=0x1E0F, hex='1E0F', c='ḏ', base='d', rightMin='-100', anchorTopX='TopX', anchorTopY='TopY', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=938)

    # e

    GDS['ecircumflexacute'] = GD(name='ecircumflexacute', uni=0x1EBF, hex='1EBF', c='ế', w='e', base='e', accents=['circumflexacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1114, comment='ế LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE')
    GDS['ecircumflexdotbelow'] = GD(name='ecircumflexdotbelow', uni=0x1EC7, hex='1EC7', c='ệ', w='e', base='ecircumflex', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1122, comment='ệ LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW')
    GDS['ecircumflexgrave'] = GD(name='ecircumflexgrave', uni=0x1EC1, hex='1EC1', c='ề', w='e', bl='e', base='e', accents=['circumflexgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1116, comment='ề LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE')
    GDS['ecircumflexhookabove'] = GD(name='ecircumflexhookabove', uni=0x1EC3, hex='1EC3', c='ể', w='e', base='e', accents=['circumflexhookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1118, comment='ể LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE')
    GDS['ecircumflextilde'] = GD(name='ecircumflextilde', uni=0x1EC5, hex='1EC5', c='ễ', w='e', base='e', accents=['circumflextildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1120, comment='ễ LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE')
    GDS['ehookabove'] = GD(name='ehookabove', uni=0x1EBB, hex='1EBB', c='ẻ', w='e', base='e', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1110, comment='ẻ E WITH HOOK ABOVE, LATIN SMALL LETTER')

    # h

    GDS['hbrevebelow'] = GD(name='hbrevebelow', uni=0x1E2B, hex='1E2B', c='ḫ', base='h', accents=['brevebelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=966)
    GDS['hcedilla'] = GD(name='hcedilla', uni=0x1E29, hex='1E29', c='ḩ', base='h', autoFixComponentPositions=False, accents=['cedillacmb'], isLower=True, fixAccents=False, anchors=['bottom', 'middle', 'top'], gid=964)
    GDS['hlinebelow'] = GD(name='hlinebelow', uni=0x1E96, hex='1E96', c='ẖ', base='h', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1073)
    # Just smallcaps for /hlinebelow, since there is no unicode for /Hlinebelow
    GDS['Hlinebelow.sc'] = GD(name='Hlinebelow.sc', base='H.sc', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])

    GDS['hookabovecmb'] = GD(name='hookabovecmb', uni=0x0309, hex='0309', c='̉', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top'], gid=495, comment='̉ HOOK ABOVE, COMBINING')

    # i

    GDS['ihookabove'] = GD(name='ihookabove', uni=0x1EC9, hex='1EC9', c='ỉ', w='idotless', bl='idotless', base='idotless', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1124, comment='ỉ I WITH HOOK ABOVE, LATIN SMALL LETTER')
    GDS['i.trk'] = GD(g2='i', g1='i', l='n', r='n', name='i.trk', isLower=True, comment='i.trk', base='idotless', accents=['dotaccentcmb'])

    # k

    GDS['kdotbelow'] = GD(name='kdotbelow', uni=0x1E33, hex='1E33', c='ḳ', base='k', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=974)
    GDS['klinebelow'] = GD(name='klinebelow', uni=0x1E35, hex='1E35', c='ḵ', base='k', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=976)

    # l

    GDS['ldotbelow'] = GD(name='ldotbelow', uni=0x1E37, hex='1E37', c='ḷ', w='l', bl='l', base='l', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=978)
    GDS['ldotbelowmacron'] = GD(name='ldotbelowmacron', uni=0x1E39, hex='1E39', c='ḹ', w='l', bl='l', base='l', accents=['macroncmb', 'dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=980)
    GDS['llinebelow'] = GD(name='llinebelow', uni=0x1E3B, hex='1E3B', c='ḻ', w='l', bl='l', base='l', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=982)

    # m

    GDS['macronbelowcmb'] = GD(name='macronbelowcmb', uni=0x0331, hex='0331', c='̱', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom'], comment='COMBINING MACRON BELOW')
    GDS['mdotaccent'] = GD(name='mdotaccent', uni=0x1E41, hex='1E41', c='ṁ', base='m', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=988)
    GDS['mdotbelow'] = GD(name='mdotbelow', uni=0x1E43, hex='1E43', c='ṃ', base='m', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=990)

    # n

    GDS['nlinebelow'] = GD(name='nlinebelow', uni=0x1E49, hex='1E49', c='ṉ', base='n', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=996)

    # o

    GDS['ocircumflexacute'] = GD(name='ocircumflexacute', uni=0x1ED1, hex='1ED1', c='ố', w='o', bl='o', base='o', accents=['circumflexacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1132, comment='ố LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE')
    GDS['ocircumflexdotbelow'] = GD(name='ocircumflexdotbelow', uni=0x1ED9, hex='1ED9', c='ộ', r='o', bl='o', base='o', accents=['circumflexcmb', 'dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1140, comment='ộ LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW')
    GDS['ocircumflexgrave'] = GD(name='ocircumflexgrave', uni=0x1ED3, hex='1ED3', c='ồ', w='o', bl='o', base='o', accents=['circumflexgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1134, comment='ồ LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE')
    GDS['ocircumflexhookabove'] = GD(name='ocircumflexhookabove', uni=0x1ED5, hex='1ED5', c='ổ', w='o', bl='o', base='o', accents=['circumflexhookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1136, comment='ổ LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE')
    GDS['ocircumflextilde'] = GD(name='ocircumflextilde', uni=0x1ED7, hex='1ED7', c='ỗ', w='o', bl='o', base='o', accents=['circumflextildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1138, comment='ỗ LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE')
    GDS['ohookabove'] = GD(name='ohookabove', uni=0x1ECF, hex='1ECF', c='ỏ', l='o', r='o', base='o', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1130, comment='ỏ O WITH HOOK ABOVE, LATIN SMALL LETTER')
    GDS['ohorn'] = GD(name='ohorn', uni=0x01A1, hex='01A1', c='ơ', l='o', r='o', anchorTopY='o', anchorTopX='o', isLower=True, autoFixComponentPositions=False, base='o', accents=['horncmb'], anchors=['bottom', 'top'], gid=354, comment='ơ O WITH HORN, LATIN SMALL LETTER')
    GDS['ohornacute'] = GD(name='ohornacute', uni=0x1EDB, hex='1EDB', c='ớ', rightMin='minRight', base='ohorn', accents=['acutecmb'], isLower=True, anchors=['bottom', 'top'], gid=1142, comment='ớ LATIN SMALL LETTER O WITH HORN AND ACUTE')
    GDS['ohorndotbelow'] = GD(name='ohorndotbelow', uni=0x1EE3, hex='1EE3', c='ợ', rightMin='minRight', base='ohorn', anchorTopY='o', anchorTopX='o', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'top'], gid=1150, comment='ợ LATIN SMALL LETTER O WITH HORN AND DOT BELOW')
    GDS['ohorngrave'] = GD(name='ohorngrave', uni=0x1EDD, hex='1EDD', c='ờ', rightMin='minRight', base='ohorn', accents=['gravecmb'], anchorTopY='o', anchorTopX='o', isLower=True, anchors=['bottom', 'top'], gid=1144, comment='ờ LATIN SMALL LETTER O WITH HORN AND GRAVE')
    GDS['ohornhookabove'] = GD(name='ohornhookabove', uni=0x1EDF, hex='1EDF', c='ở', rightMin='minRight', anchorTopY='o', anchorTopX='o', base='ohorn', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'top'], gid=1146, comment='ở LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE')
    GDS['ohorntilde'] = GD(name='ohorntilde', uni=0x1EE1, hex='1EE1', c='ỡ', rightMin='minRight', anchorTopY='o', anchorTopX='o', base='ohorn', accents=['tildecmb'], isLower=True, anchors=['bottom', 'top'], gid=1148, comment='ỡ LATIN SMALL LETTER O WITH HORN AND TILDE')

    # r

    GDS['rdotaccent'] = GD(name='rdotaccent', uni=0x1E59, hex='1E59', c='ṙ', l='r', r='r', rightMin='-100', base='r', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1012)
    GDS['rdotbelow'] = GD(name='rdotbelow', uni=0x1E5B, hex='1E5B', c='ṛ', w='r', rightMin='-100', base='r', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1014)
    GDS['rdotbelowmacron'] = GD(name='rdotbelowmacron', uni=0x1E5D, hex='1E5D', c='ṝ', w='r', bl='r', base='r', accents=['macroncmb', 'dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1016)
    GDS['ringhalfleft'] = GD(name='ringhalfleft', uni=0x02BF, hex='02BF', c='ʿ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, srcName='ringcmb', isLower=True, gid=473)
    GDS['ringhalfright'] = GD(name='ringhalfright', uni=0x02BE, hex='02BE', c='ʾ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='ringhalfrightcmb', isLower=True, gid=472)
    GDS['ringhalfrightcmb'] = GD(name='ringhalfrightcmb', l=GD.CAT_CENTER, w=0, isLower=True, anchors=['top', '_top'], gid=472)
    GDS['rlinebelow'] = GD(name='rlinebelow', uni=0x1E5F, hex='1E5F', c='ṟ', w='r', bl='r', base='r', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1018)
    GDS['ruble'] = GD(name='ruble', uni=0x20BD, hex='20BD', c='₽', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True, gid=1462)

    # t

    GDS['tdotbelow'] = GD(name='tdotbelow', uni=0x1E6D, hex='1E6D', c='ṭ', base='t', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1032)
    GDS['tlinebelow'] = GD(name='tlinebelow', uni=0x1E6F, hex='1E6F', c='ṯ', base='t', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1034)

    # u

    GDS['udieresisacute'] = GD(name='udieresisacute', uni=0x01D8, hex='01D8', c='ǘ', l='u', r='u', base='u', accents=['dieresisacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=409)
    GDS['udieresiscaron'] = GD(name='udieresiscaron', uni=0x01DA, hex='01DA', c='ǚ', l='u', r='u', base='u', accents=['dieresiscaroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=411)
    GDS['udieresisgrave'] = GD(name='udieresisgrave', uni=0x01DC, hex='01DC', c='ǜ', l='u', r='u', base='u', accents=['dieresisgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=413)
    GDS['udieresismacron'] = GD(name='udieresismacron', uni=0x01D6, hex='01D6', c='ǖ', l='u', r='u', base='u', accents=['dieresismacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=407)
    GDS['uhookabove'] = GD(name='uhookabove', uni=0x1EE7, hex='1EE7', c='ủ', l='u', r='u', base='u', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1154, comment='ủ U WITH HOOK ABOVE, LATIN SMALL LETTER')
    GDS['uhorn'] = GD(name='uhorn', uni=0x01B0, hex='01B0', c='ư', l='u', anchorTopY='u', anchorTopX='u', isLower=True, autoFixComponentPositions=False, srcName='u', anchors=['bottom', 'top'], gid=369, comment='ư U WITH HORN, LATIN SMALL LETTER. Best not to do the /horn as separate component.')
    GDS['uhornacute'] = GD(name='uhornacute', uni=0x1EE9, hex='1EE9', c='ứ', l='uhorn', r='uhorn', anchorTopY='u', anchorTopX='u', rightMin='minRight', base='uhorn', accents=['acutecmb'], isLower=True, anchors=['bottom', 'top'], gid=1156, comment='ứ LATIN SMALL LETTER U WITH HORN AND ACUTE')
    GDS['uhorndotbelow'] = GD(name='uhorndotbelow', uni=0x1EF1, hex='1EF1', c='ự', l='uhorn', r='uhorn', anchorTopY='u', anchorTopX='u', rightMin='minRight', base='uhorn', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'top'], gid=1164, comment='ự LATIN SMALL LETTER U WITH HORN AND DOT BELOW')
    GDS['uhorngrave'] = GD(name='uhorngrave', uni=0x1EEB, hex='1EEB', c='ừ', l='uhorn', r='uhorn', anchorTopY='u', anchorTopX='u', rightMin='minRight', base='uhorn', accents=['gravecmb'], isLower=True, anchors=['bottom', 'top'], gid=1158, comment='ừ LATIN SMALL LETTER U WITH HORN AND GRAVE')
    GDS['uhornhookabove'] = GD(name='uhornhookabove', uni=0x1EED, hex='1EED', c='ử', l='uhorn', r='uhorn', anchorTopY='u', anchorTopX='u', rightMin='minRight', base='uhorn', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'top'], gid=1160, comment='ử LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE')
    GDS['uhorntilde'] = GD(name='uhorntilde', uni=0x1EEF, hex='1EEF', c='ữ', w='uhorn', bl='uhorn', anchorTopY='u', anchorTopX='u', rightMin='minRight', base='uhorn', accents=['tildecmb'], isLower=True, anchors=['bottom', 'top'], gid=1162, comment='ữ LATIN SMALL LETTER U WITH HORN AND TILDE')

    # w

    GDS['wdotbelow'] = GD(name='wdotbelow', uni=0x1E89, hex='1E89', c='ẉ', l='w', r='w', base='w', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1060)

    # y

    GDS['ydotaccent'] = GD(name='ydotaccent', uni=0x1E8F, hex='1E8F', c='ẏ', l='y', r='y', base='y', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1066)
    GDS['ydotbelow'] = GD(name='ydotbelow', uni=0x1EF5, hex='1EF5', c='ỵ', l='y', r='y', base='y', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1168, comment='ỵ Y WITH DOT BELOW, LATIN SMALL LETTER')
    GDS['yhookabove'] = GD(name='yhookabove', uni=0x1EF7, hex='1EF7', c='ỷ', l='y', r='y', base='y', accents=['hookabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1170)

    # z

    GDS['zlinebelow'] = GD(name='zlinebelow', uni=0x1E95, hex='1E95', c='ẕ', base='z', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=1072)

    # Diacritics

    GDS['brevebelowcmb'] = GD(name='brevebelowcmb', uni=0x032E, hex='032E', c='̮', base='brevecmb', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, anchors=['bottom', '_bottom'])
    GDS['horncmb'] = GD(name='horncmb', uni=0x031B, hex='031B', c='̛', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['top', '_top'])
    GDS['horncmb.uc'] = GD(name='horncmb.uc', w=0, isLower=False, autoFixComponentPositions=False, autoFixMargins=False, srcName='horncmb') # No anchors

    # Arrows

    GDS['arrowright'] = GD(name='arrowright', uni=0x2192, hex='2192', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowleft'] = GD(name='arrowleft', uni=0x2190, hex='2190', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowup'] = GD(name='arrowup', uni=0x2191, hex='2191', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowdown'] = GD(name='arrowdown', uni=0x2193, hex='2193', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowleftright'] = GD(name='arrowleftright', uni=0x2194, hex='2194', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowupdown'] = GD(name='arrowupdown', uni=0x2195, hex='2195', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)    
    GDS['arrowSE'] = GD(name='arrowSE', uni=0x2198, hex='2198', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)  
    GDS['arrowNE'] = GD(name='arrowNE', uni=0x2197, hex='2197', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH) 
    GDS['arrowNW'] = GD(name='arrowNW', uni=0x2196, hex='2196', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH) 
    GDS['arrowSW'] = GD(name='arrowSW', uni=0x2199, hex='2199', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)     
    
    GDS['arrowright.uc'] = GD(name='arrowright.uc', base='arrowright', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowleft.uc'] = GD(name='arrowleft.uc', base='arrowleft', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowup.uc'] = GD(name='arrowup.uc', base='arrowup', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowdown.uc'] = GD(name='arrowdown.uc', base='arrowdown', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowleftright.uc'] = GD(name='arrowleftright.uc', base='arrowleftright', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)
    GDS['arrowupdown.uc'] = GD(name='arrowupdown.uc', base='arrowupdown', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)    
    GDS['arrowSE.uc'] = GD(name='arrowSE.uc', base='arrowSE', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)  
    GDS['arrowNE.uc'] = GD(name='arrowNE.uc', base='arrowNE', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH) 
    GDS['arrowNW.uc'] = GD(name='arrowNW.uc', base='arrowNW', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH) 
    GDS['arrowSW.uc'] = GD(name='arrowSW.uc', base='arrowSW', l=GD.CAT_CENTER, w=GD.CAT_ARROW_WIDTH)     
    

# Make exceptions here for Italic glyphs and spacing rules in LATIN_M_SET_ITALIC

GDSI = LATIN_M_SET_ITALIC

if __name__ == '__main__':
    for gName, gd in LATIN_M_SET.items():
        #print('---', gd)
        if gd.base and gd.base not in LATIN_M_SET:
            print('##### Missing base', gName, gd.base)
        for aName in gd.accents:
            if aName not in GDS:
                print('#### Missing accent', gName, aName)



