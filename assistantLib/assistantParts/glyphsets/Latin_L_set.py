# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_L_set.py
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
#       • supports about 100 extra languages3, such as Azerbaijani (37M speakers) Ga (8.5M) 
#         Paraguayan Guaraní (6.5M) Hausa (40M) Igbo (27M) Lingála (15M) Úmbúndú (9.5M) Yorùbá (40M) …
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
#    Latin L
#    Latin L completes the support of all Latin-based languages on Hyperglot. 
#    I also added some legacy unicode characters like ŉ, ĸ and ǆ.
#
#    Latin S + Latin M + Latin L
#    AÁĂǍÂÄẠÀĀĄÅÃÆBḄƁCĆČÇĈĊDÐĎĐḌƊEÉĔĚÊËĖẸÈĒĘƐƎẼFGĞĜĢĠḠǦHĦĤḦḤIÍĬǏÎÏİỊÌĪĮƗĨJĴKĶƘLĹĽĻŁMNŃŇŅṄṆƝÑŊ
#    OÓŎǑÔÖỌÒŐŌƆØÕŒPṖÞQRŔŘŖSŚŠŞŜȘṢẞƏTŤŢȚUÚŬǓÛÜỤÙŰŪŲŮŨVɅWẂŴẄẀXẌYÝŶŸỲƳỸȲZŹŽŻẒaáăǎâäạàāąåãæbḅɓcć
#    čçĉċdðďđḍɗeéĕěêëėẹèēęɛẽǝəfgğĝģġḡǧhħĥḧḥiıíĭǐîïịìīįɨĩjȷĵkķƙlĺľļłmnńňņṅṇɲñŋoóŏǒôöọòőōɔøõœpṗ
#    þqrŕřŗsśšşŝșṣßtťţțuúŭǔûüụùűūųůũvʌwẃŵẅẁxẍyýŷÿỳƴỹȳzźžżẓ₵₡₲₺₼₦₹ ̈ ̇ ̀ ́ ̋ ̂ ̌ ̆ ̊ ̃ ̄ ̒ ̣ ̦ ̧ ̨ʼʻ ̵
#
#    ẮẶẰẲẴẤẬẦẨẪẢǢḎẾỆỀỂỄẺḪḨỈḲḴḶḸḺṀṂṈỐỘỒỔỖỎƠỚỢỜỞỠṘṚṜṞṬṮǗǙǛǕỦƯỨỰỪỬỮẈẎỴỶẔ
#    ắặằẳẵấậầẩẫảǣḏếệềểễẻḫḩẖỉḳḵḷḹḻṁṃṉốộồổỗỏơớợờởỡṙṛṝṟṭṯǘǚǜǖủưứựừửữẉẏỵỷẕ₫
#   
#    ȀǞȦǠȂⱭǺḀȺⱯǼḂꞴḆɃḈꞳƇȻǱǄƉḐḒḊǲǅȨḜḘȄȆḖḔƩɆḚƷǮƸꞘḞƑǴƓɁꞬǤȜȞḢꜦꞪꞍĲȈḮȊƖḬꞮꞲɈḰǨꝀǇȽꞭḼĿⱠⱢǈḾⱮƜǊṊǸǋȠƟȌȪȮȰ
#    ȎṒṐꞶǪǬǾṌṎȬȢṔƤⱣɊȐȒɌⱤṤꞋṦṠṨꞨŦṰȾṪƬƮɄṶȔṲȖṺƱṸṴꞸƔṾƲṼẆⱲẊɎẐƵΒΕΘΛΩ
#    ȁǟȧǡȃɑẚǻḁⱥɐǽḃꞵʘḇƀḉꭓƈↄȼȸḑḓḋɖǳǆȩḝḙȅȇḗḕʃƪɇḛʒǯƹꞙḟƒǵɣɠʔʕɂɡǥȝȟḣꜧɧɦɥȉḯȋĳɩḭɪǰʝɟʄɉḱǩꝁĸƛƚɬḽŀⱡɫǉḿɱɯŉṋ
#    ǹǌƞɵȍȫȯȱȏṓṑꞷǫǭǿṍṏȭȣṕɸƥᵽɋȹɤȑɽȓɍṥꞌṧṡṩꞩſẛŧṱⱦẗṫʧƭʈʉṷȕṳȗṻʊṹṵꞹṿʋṽẇⱳẘẋẙɏʎẑƶβεθλω
#    ǂǀǁǃₐₑʱʰⁱʲˡⁿₒʳₔˢʷₓˣʸₕₖₗₘₙₚₛᶿₜᵘᵛᶻˀˁʹˈ꞉ˮ˗꞊ ᷆ ᷅ ᷄ ̍ ̏ ̑ ̓ ̕ ̠ ̤ ̥ ̩ ̭ ̯ ̰ ̲ ͜ ͝ ͡ ᷊ ̴ ͘ˊˋ
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
from assistantLib.assistantParts.glyphsets.Latin_M_set import LATIN_M_SET

LATIN_L_SET_NAME = 'Latin L'

# The "c" attribtes are redundant, if the @uni or @hex atre defined, but they offer easy searching in the source by char.

LATIN_L_SET = GDS = deepcopy(LATIN_M_SET)

# Latin L unicodes
# Make this into these codes:
# GDS['aacute.alt'] = GD(name='aacute.alt', base='a.alt', accents=('acutecmb'))
#
#    0x0200, 0x01DE, 0x0226, 0x01E0, 0x0202, 0x2C6D, 0x01FA, 0x1E00, 0x023A, 0x2C6F, 0x01FC, 0x1E02, 0xA7B4, 0x1E06, 
#    0x0243, 0x1E08, 0xA7B3, 0x0187, 0x023B, 0x01F1, 0x01C4, 0x0189, 0x1E10, 0x1E12, 0x1E0A, 0x01F2, 0x01C5, 0x0228, 
#    0x1E1C, 0x1E18, 0x0204, 0x0206, 0x1E16, 0x1E14, 0x01A9, 0x0246, 0x1E1A, 0x01B7, 0x01EE, 0x01B8, 0xA798, 0x1E1E, 
#    0x0191, 0x01F4, 0x0193, 0x0241, 0xA7AC, 0x01E4, 0x021C, 0x021E, 0x1E22, 0xA726, 0xA7AA, 0xA78D, 0x0132, 0x0208, 
#    0x1E2E, 0x020A, 0x0196, 0x1E2C, 0xA7AE, 0xA7B2, 0x0248, 0x1E30, 0x01E8, 0xA740, 0x01C7, 0x023D, 0xA7AD, 0x1E3C, 
#    0x013F, 0x2C60, 0x2C62, 0x01C8, 0x1E3E, 0x2C6E, 0x019C, 0x01CA, 0x1E4A, 0x01F8, 0x01CB, 0x0220, 0x019F, 0x020C, 
#    0x022A, 0x022E, 0x0230, 0x020E, 0x1E52, 0x1E50, 0xA7B6, 0x01EA, 0x01EC, 0x01FE, 0x1E4C, 0x1E4E, 0x022C, 0x0222, 
#    0x1E54, 0x01A4, 0x2C63, 0x024A, 0x0210, 0x0212, 0x024C, 0x2C64, 0x1E64, 0xA78B, 0x1E66, 0x1E60, 0x1E68, 0xA7A8, 
#    0x0166, 0x1E70, 0x023E, 0x1E6A, 0x01AC, 0x01AE, 0x0244, 0x1E76, 0x0214, 0x1E72, 0x0216, 0x1E7A, 0x01B1, 0x1E78, 
#    0x1E74, 0xA7B8, 0x0194, 0x1E7E, 0x01B2, 0x1E7C, 0x1E86, 0x2C72, 0x1E8A, 0x024E, 0x1E90, 0x01B5, 0x0392, 0x0395, 
#    0x0398, 0x039B, 0x03A9, 0x0201, 0x01DF, 0x0227, 0x01E1, 0x0203, 0x0251, 0x1E9A, 0x01FB, 0x1E01, 0x2C65, 0x0250, 
#    0x01FD, 0x1E03, 0xA7B5, 0x0298, 0x1E07, 0x0180, 0x1E09, 0xAB53, 0x0188, 0x2184, 0x023C, 0x0238, 0x1E11, 0x1E13, 
#    0x1E0B, 0x0256, 0x01F3, 0x01C6, 0x0229, 0x1E1D, 0x1E19, 0x0205, 0x0207, 0x1E17, 0x1E15, 0x0283, 0x01AA, 0x0247, 
#    0x1E1B, 0x0292, 0x01EF, 0x01B9, 0xA799, 0x1E1F, 0x0192, 0x01F5, 0x0263, 0x0260, 0x0294, 0x0295, 0x0242, 0x0261, 
#    0x01E5, 0x021D, 0x021F, 0x1E23, 0xA727, 0x0267, 0x0266, 0x0265, 0x0209, 0x1E2F, 0x020B, 0x0133, 0x0269, 0x1E2D, 
#    0x026A, 0x01F0, 0x029D, 0x025F, 0x0284, 0x0249, 0x1E31, 0x01E9, 0xA741, 0x0138, 0x019B, 0x019A, 0x026C, 0x1E3D, 
#    0x0140, 0x2C61, 0x026B, 0x01C9, 0x1E3F, 0x0271, 0x026F, 0x0149, 0x1E4B, 0x01F9, 0x01CC, 0x019E, 0x0275, 0x020D, 
#    0x022B, 0x022F, 0x0231, 0x020F, 0x1E53, 0x1E51, 0xA7B7, 0x01EB, 0x01ED, 0x01FF, 0x1E4D, 0x1E4F, 0x022D, 0x0223, 
#    0x1E55, 0x0278, 0x01A5, 0x1D7D, 0x024B, 0x0239, 0x0264, 0x0211, 0x027D, 0x0213, 0x024D, 0x1E65, 0xA78C, 0x1E67, 
#    0x1E61, 0x1E69, 0xA7A9, 0x017F, 0x1E9B, 0x0167, 0x1E71, 0x2C66, 0x1E97, 0x1E6B, 0x02A7, 0x01AD, 0x0288, 0x0289, 
#    0x1E77, 0x0215, 0x1E73, 0x0217, 0x1E7B, 0x028A, 0x1E79, 0x1E75, 0xA7B9, 0x1E7F, 0x028B, 0x1E7D, 0x1E87, 0x2C73, 
#    0x1E98, 0x1E8B, 0x1E99, 0x024F, 0x028E, 0x1E91, 0x01B6, 0x03B2, 0x03B5, 0x03B8, 0x03BB, 0x03C9, 0x01C2, 0x01C0, 
#    0x01C1, 0x01C3, 0x2090, 0x2091, 0x02B1, 0x02B0, 0x2071, 0x02B2, 0x02E1, 0x207F, 0x2092, 0x02B3, 0x2094, 0x02E2, 
#    0x02B7, 0x2093, 0x02E3, 0x02B8, 0x2095, 0x2096, 0x2097, 0x2098, 0x2099, 0x209A, 0x209B, 0x1DBF, 0x209C, 0x1D58, 
#    0x1D5B, 0x1DBB, 0x02C0, 0x02C1, 0x02B9, 0x02C8, 0xA789, 0x02EE, 0x02D7, 0xA78A, 0x1DC7, 0x1DC6, 0x1DC5, 0x1DC4, 
#    0x030D, 0x030F, 0x0311, 0x0313, 0x0315, 0x0320, 0x0324, 0x0325, 0x0329, 0x032D, 0x032F, 0x0330, 0x0332, 0x035C, 
#    0x035D, 0x0361, 0x1DCA, 0x0334, 0x0358, 0x02CA, 0x02CB

GDS['Ustroke'] = GD(name='Ustroke', uni=0xA7B8, hex='A7B8', c='Ꞹ')
GDS['ustroke'] = GD(name='ustroke', uni=0xA7B9, hex='A7B9', c='ꞹ')

# A

GDS['AEacute'] = GD(name='AEacute', uni=0x01FC, hex='01FC', c='Ǽ', l='A', r='E', base='AE', accents=['acutecmb'], anchors=['bottom', 'middle', 'top'], gid=445, comment='Ǽ LATIN CAPITAL LETTER AE WITH ACUTE')
GDS['Adblgrave'] = GD(name='Adblgrave', uni=0x0200, hex='0200', c='Ȁ', l='A', r='A', base='A', accents=['dblgravecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Adieresismacron'] = GD(name='Adieresismacron', uni=0x01DE, hex='01DE', c='Ǟ', l='A', r='A', base='A', accents=['dieresismacroncmb'], srcName='uni01DE', anchors=['bottom', 'middle', 'top'], gid=415)
GDS['Adotaccent'] = GD(name='Adotaccent', uni=0x0226, hex='0226', c='Ȧ', l='A', r='A', base='A', accents=['dotaccentcmb'], srcName='uni0226', anchors=['bottom', 'middle', 'top'], gid=453)
GDS['Adotmacron'] = GD(name='Adotmacron', uni=0x01E0, hex='01E0', c='Ǡ', l='A', r='A', base='A', accents=['dotaccentmacroncmb'], srcName='uni01E0', anchors=['bottom', 'middle', 'top'], gid=417)
GDS['Ainvertedbreve'] = GD(name='Ainvertedbreve', uni=0x0202, hex='0202', c='Ȃ', l='A', r='A', base='A', accents=['invertedbrevecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Alpha-latin'] = GD(name='Alpha-latin', uni=0x2C6D, hex='2C6D', c='Ɑ', l='O', r='H')
GDS['Aringacute'] = GD(name='Aringacute', uni=0x01FA, hex='01FA', c='Ǻ', l='A', r='A', base='Aring', accents=['acutecmb'], anchors=['bottom', 'middle', 'ogonek', 'top'], gid=443, comment='Ǻ LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE')
GDS['Aringbelow'] = GD(name='Aringbelow', uni=0x1E00, hex='1E00', c='Ḁ', l='A', r='A', base='A', accents=['ringbelowcmb'], srcName='uni1E00', anchors=['bottom', 'middle', 'top'], gid=923)
GDS['Astroke'] = GD(name='Astroke', uni=0x023A, hex='023A', c='Ⱥ', l='A', w='A', base='A', accents=['strokecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Aturned'] = GD(name='Aturned', uni=0x2C6F, hex='2C6F', c='Ɐ', l2r='A', r2l='A', srcName='A')

# B

GDS['Bdotaccent'] = GD(name='Bdotaccent', uni=0x1E02, hex='1E02', c='Ḃ', l='H', r='B', base='B', accents=['dotaccentcmb'], srcName='uni1E02', anchors=['bottom', 'middle', 'top'], gid=925)
GDS['Beta'] = GD(name='Beta', uni=0x0392, hex='0392', c='Β', l='H', r='B', base='B', anchors=['bottom', 'middle', 'top'], gid=536)
GDS['Beta-latin'] = GD(name='Beta-latin', uni=0xA7B4, hex='A7B4', c='Ꞵ')
GDS['Blinebelow'] = GD(name='Blinebelow', uni=0x1E06, hex='1E06', c='Ḇ', l='H', r='B', base='B', accents=['macronbelowcmb'], srcName='uni1E06', anchors=['bottom', 'middle', 'top'], gid=929)
GDS['Bstroke'] = GD(name='Bstroke', uni=0x0243, hex='0243', c='Ƀ', l='Eth', base='B', anchors=['bottom', 'middle', 'top'])

# C

GDS['Ccedillaacute'] = GD(name='Ccedillaacute', uni=0x1E08, hex='1E08', c='Ḉ', l='O', r='C', base='C', accents=['cedillacmb', 'acutecmb'], srcName='uni1E08', anchors=['bottom', 'middle', 'top'], gid=931)
GDS['Chi-latin'] = GD(name='Chi-latin', uni=0xA7B3, hex='A7B3', c='Ꭓ', base='X', anchors=['bottom', 'middle', 'top'])
GDS['Chook'] = GD(name='Chook', uni=0x0187, hex='0187', c='Ƈ', l='O', srcName='uni0187', gid=328)
GDS['Cstroke'] = GD(name='Cstroke', uni=0x023B, hex='023B', c='Ȼ', l='C', r='C', base='C', accents=['strokecmb'], anchors=['bottom', 'middle', 'top'])

# D

GDS['DZ'] = GD(name='DZ', uni=0x01F1, hex='01F1', c='Ǳ', l='D', r='Z', base='D', accents=['Z'], srcName='uni01F1', gid=434)
GDS['DZcaron'] = GD(name='DZcaron', uni=0x01C4, hex='01C4', c='Ǆ', l='D', r='Z', base='D', accents=['Z', 'caroncmb'], srcName='uni01C4', fixAccents=False, gid=389)
GDS['Dafrican'] = GD(name='Dafrican', uni=0x0189, hex='0189', c='Ɖ', l='Eth', r='D', base='Eth', srcName='uni0189', gid=330, comment='Ɖ D, LATIN CAPITAL LETTER AFRICAN')
GDS['Dcedilla'] = GD(name='Dcedilla', uni=0x1E10, hex='1E10', c='Ḑ', l='D', r='D', base='D', accents=['cedillacmb'], srcName='uni1E10', anchors=['bottom', 'middle', 'top'], gid=939)
GDS['Dcircumflexbelow'] = GD(name='Dcircumflexbelow', uni=0x1E12, hex='1E12', c='Ḓ', l='D', r='D', base='D', accents=['circumflexbelowcmb'], srcName='uni1E12', anchors=['bottom', 'middle', 'top'], gid=941)
GDS['Ddotaccent'] = GD(name='Ddotaccent', uni=0x1E0A, hex='1E0A', c='Ḋ', l='D', r='D', base='D', accents=['dotaccentcmb'], srcName='uni1E0A', anchors=['bottom', 'middle', 'top'], gid=933)
GDS['Dz'] = GD(name='Dz', uni=0x01F2, hex='01F2', c='ǲ', l='D', r='z', base='D', accents=['z'], srcName='uni01F2', gid=435)
GDS['Dzcaron'] = GD(name='Dzcaron', uni=0x01C5, hex='01C5', c='ǅ', l='D', r='z', base='D', accents=['z', 'caroncmb'], srcName='uni01C5', fixAccents=False, gid=390)

# E

GDS['Ecedilla'] = GD(name='Ecedilla', uni=0x0228, hex='0228', c='Ȩ', base='E', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'])
GDS['Ecedillabreve'] = GD(name='Ecedillabreve', uni=0x1E1C, hex='1E1C', c='Ḝ', l='H', r='E', base='E', accents=['cedillacmb', 'brevecmb'], srcName='uni1E1C', anchors=['bottom', 'middle', 'top'], gid=951)
GDS['Ecircumflexbelow'] = GD(name='Ecircumflexbelow', uni=0x1E18, hex='1E18', c='Ḙ', l='H', w='E', base='E', accents=['circumflexbelowcmb'], srcName='uni1E18', anchors=['bottom', 'middle', 'top'], gid=947)
GDS['Edblgrave'] = GD(name='Edblgrave', uni=0x0204, hex='0204', c='Ȅ', bl='E', base='E', accents=['dblgravecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Einvertedbreve'] = GD(name='Einvertedbreve', uni=0x0206, hex='0206', c='Ȇ', base='E', accents=['invertedbrevecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Emacronacute'] = GD(name='Emacronacute', uni=0x1E16, hex='1E16', c='Ḗ', l='H', r='E', base='E', accents=['macronacutecmb'], srcName='uni1E16', anchors=['bottom', 'middle', 'top'], gid=945)
GDS['Emacrongrave'] = GD(name='Emacrongrave', uni=0x1E14, hex='1E14', c='Ḕ', l='H', r='E', base='E', accents=['macrongravecmb'], srcName='uni1E14', anchors=['bottom', 'middle', 'top'], gid=943)
GDS['Epsilon'] = GD(name='Epsilon', uni=0x0395, hex='0395', c='Ε', l='E', r='E', base='E', anchors=['bottom', 'middle', 'top'], gid=539)
GDS['Esh'] = GD(name='Esh', uni=0x01A9, hex='01A9', c='Ʃ', srcName='uni01A9', gid=362)
GDS['Estroke'] = GD(name='Estroke', uni=0x0246, hex='0246', c='Ɇ', base='E', accents=['slashlongcmb'], anchors=['bottom', 'middle', 'top'])
GDS['Etildebelow'] = GD(name='Etildebelow', uni=0x1E1A, hex='1E1A', c='Ḛ', base='E', accents=['tildebelowcmb'], srcName='uni1E1A', anchors=['bottom', 'middle', 'top'], gid=949)
GDS['Ezh'] = GD(name='Ezh', uni=0x01B7, hex='01B7', c='Ʒ', l='three', r='B', srcName='uni01B7', anchors=['top'], gid=376, comment='Ʒ EZH, LATIN CAPITAL LETTER')
GDS['Ezhcaron'] = GD(name='Ezhcaron', uni=0x01EE, hex='01EE', c='Ǯ', r='B', base='Ezh', accents=['caroncmb'], srcName='uni01EE', anchors=['top'], gid=431)
GDS['Ezhreversed'] = GD(name='Ezhreversed', uni=0x01B8, hex='01B8', c='Ƹ', r2l='B', srcName='uni01B8', gid=377)

# F

GDS['FStroke'] = GD(name='FStroke', uni=0xA798, hex='A798', c='Ꞙ', l='0', r='F')
GDS['Fdotaccent'] = GD(name='Fdotaccent', uni=0x1E1E, hex='1E1E', c='Ḟ', base='F', accents=['dotaccentcmb'], srcName='uni1E1E', anchors=['bottom', 'middle', 'top'], gid=953)
GDS['Fhook'] = GD(name='Fhook', uni=0x0191, hex='0191', c='Ƒ', l='J', r='F', srcName='uni0191', gid=338, comment='Ƒ LATIN CAPITAL LETTER F WITH HOOK')

# G

GDS['Gacute'] = GD(name='Gacute', uni=0x01F4, hex='01F4', c='Ǵ', l='G', r='G', base='G', accents=['acutecmb'], srcName='uni01F4', anchors=['bottom', 'middle', 'top'], gid=437)
GDS['Gammaafrican'] = GD(name='Gammaafrican', uni=0x0194, hex='0194', c='Ɣ', srcName='uni0194', gid=341, comment='Ɣ GAMMA, LATIN CAPITAL LETTER')
GDS['Ghook'] = GD(name='Ghook', uni=0x0193, hex='0193', c='Ɠ', l='G', w='G', srcName='uni0193', gid=340)
GDS['Glottalstop'] = GD(name='Glottalstop', uni=0x0241, hex='0241', c='Ɂ', l='question', r='question')
GDS['Gscript'] = GD(name='Gscript', uni=0xA7AC, hex='A7AC', c='Ɡ', l='O', r='H')
GDS['Gstroke'] = GD(name='Gstroke', uni=0x01E4, hex='01E4', c='Ǥ', l='G', r='G', srcName='uni01E4', gid=421)

# H

GDS['Hcaron'] = GD(name='Hcaron', uni=0x021E, hex='021E', c='Ȟ', base='H', accents=['caroncmb'], anchors=['bottom', 'middle', 'top'])
GDS['Hdotaccent'] = GD(name='Hdotaccent', uni=0x1E22, hex='1E22', c='Ḣ', l='H', r='H', base='H', accents=['dotaccentcmb'], srcName='uni1E22', anchors=['bottom', 'middle', 'top'], gid=957)
GDS['Heng'] = GD(name='Heng', uni=0xA726, hex='A726', c='Ꜧ')
GDS['Hhook'] = GD(name='Hhook', uni=0xA7AA, hex='A7AA', c='Ɦ')
GDS['Hturned'] = GD(name='Hturned', uni=0xA78D, hex='A78D', c='Ɥ', l='H')

# I

GDS['IJ'] = GD(name='IJ', uni=0x0132, hex='0132', c='Ĳ', l='I', r='J', base='I', accents=['J'], anchors=['bottom', 'middle', 'top'], gid=243, comment='Ĳ')
GDS['Idblgrave'] = GD(name='Idblgrave', uni=0x0208, hex='0208', c='Ȉ', w='I', bl='I', base='I', accents=['dblgravecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Idieresisacute'] = GD(name='Idieresisacute', uni=0x1E2E, hex='1E2E', c='Ḯ', w='I', bl='I', base='I', accents=['dieresisacutecmb'], srcName='uni1E2E', anchors=['bottom', 'middle', 'top'], gid=969)
GDS['Iinvertedbreve'] = GD(name='Iinvertedbreve', uni=0x020A, hex='020A', c='Ȋ', w='I', bl='I', base='I', accents=['invertedbrevecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Iotaafrican'] = GD(name='Iotaafrican', uni=0x0196, hex='0196', c='Ɩ', srcName='uni0196', gid=343)
GDS['Ismall'] = GD(name='Ismall', uni=0x026A, hex='026A', c='ɪ', l='hyphen', r='hyphen', srcName='uni026A', isSc=True, gid=463)
GDS['Itildebelow'] = GD(name='Itildebelow', uni=0x1E2C, hex='1E2C', c='Ḭ', w='I', bl='I', base='I', accents=['tildebelowcmb'], srcName='uni1E2C', anchors=['bottom', 'middle', 'top'], gid=967)

# J

GDS['Jcrossedtail'] = GD(name='Jcrossedtail', uni=0xA7B2, hex='A7B2', c='Ʝ', l='J', r='J')
GDS['Jstroke'] = GD(name='Jstroke', uni=0x0248, hex='0248', c='Ɉ', l='J', r='Eth', base='J', anchors=['bottom', 'middle', 'top'])

# K

GDS['Kacute'] = GD(name='Kacute', uni=0x1E30, hex='1E30', c='Ḱ', l='H', r='K', base='K', accents=['acutecmb'], srcName='uni1E30', anchors=['bottom', 'middle', 'top'], gid=971)
GDS['Kcaron'] = GD(name='Kcaron', uni=0x01E8, hex='01E8', c='Ǩ', l='H', r='K', base='K', accents=['caroncmb'], srcName='uni01E8', anchors=['bottom', 'middle', 'top'], gid=425)
GDS['Kstroke'] = GD(name='Kstroke', uni=0xA740, hex='A740', c='Ꝁ', l='Eth', r='K', base='K', anchors=['bottom', 'middle', 'top'])

# L

GDS['LJ'] = GD(name='LJ', uni=0x01C7, hex='01C7', c='Ǉ', l='H', r='J', base='L', accents=['J'], srcName='uni01C7', gid=392)
GDS['Lambda'] = GD(name='Lambda', uni=0x039B, hex='039B', c='Λ', l='A', r='A', gid=545, comment='Λ')
GDS['Lbar'] = GD(name='Lbar', uni=0x023D, hex='023D', c='Ƚ', l='Eth', base='L', anchors=['bottom', 'middle', 'top'])
GDS['Lbelt'] = GD(name='Lbelt', uni=0xA7AD, hex='A7AD', c='Ɬ', l='o', r='L')
GDS['Lcircumflexbelow'] = GD(name='Lcircumflexbelow', uni=0x1E3C, hex='1E3C', c='Ḽ', l='H', r='L', base='L', accents=['circumflexbelowcmb'], srcName='uni1E3C', anchors=['bottom', 'middle', 'top'], gid=983)
GDS['Ldot'] = GD(name='Ldot', uni=0x013F, hex='013F', c='Ŀ', l='H', r='L', base='L', accents=['dotmiddlecmb'], anchors=['bottom', 'middle', 'top'], gid=256, comment='Ŀ')
GDS['Ldoublebar'] = GD(name='Ldoublebar', uni=0x2C60, hex='2C60', c='Ⱡ', l='Eth', r='L', base='L', anchors=['bottom', 'middle', 'top'])
GDS['Lj'] = GD(name='Lj', uni=0x01C8, hex='01C8', c='ǈ', l='H', r='j', base='L', accents=['j'], srcName='uni01C8', gid=393)
GDS['Lmiddletilde'] = GD(name='Lmiddletilde', uni=0x2C62, hex='2C62', c='Ɫ', l='asciitilde', base='L', anchors=['bottom', 'middle', 'top'])

# M

GDS['Macute'] = GD(name='Macute', uni=0x1E3E, hex='1E3E', c='Ḿ', l='H', r='H', base='M', accents=['acutecmb'], srcName='uni1E3E', anchors=['bottom', 'middle', 'top'], gid=985)
GDS['Mhook'] = GD(name='Mhook', uni=0x2C6E, hex='2C6E', c='Ɱ', r='J')
GDS['Mturned'] = GD(name='Mturned', uni=0x019C, hex='019C', c='Ɯ', l='H', r='H', srcName='uni019C', gid=349)

# N

GDS['NJ'] = GD(name='NJ', uni=0x01CA, hex='01CA', c='Ǌ', l='H', r='J', base='N', accents=['J'], srcName='uni01CA', gid=395)
GDS['Ncircumflexbelow'] = GD(name='Ncircumflexbelow', uni=0x1E4A, hex='1E4A', c='Ṋ', l='H', r='H', base='N', accents=['circumflexbelowcmb'], srcName='uni1E4A', anchors=['bottom', 'middle', 'top'], gid=997)
GDS['Ngrave'] = GD(name='Ngrave', uni=0x01F8, hex='01F8', c='Ǹ', l='H', r='H', base='N', accents=['gravecmb'], srcName='uni01F8', anchors=['bottom', 'middle', 'top'], gid=441)
GDS['Nj'] = GD(name='Nj', uni=0x01CB, hex='01CB', c='ǋ', base='N', accents=['j'], srcName='uni01CB', gid=396)
GDS['Nlongrightleg'] = GD(name='Nlongrightleg', uni=0x0220, hex='0220', c='Ƞ', r='H')

# O

GDS['OU'] = GD(name='OU', uni=0x0222, hex='0222', c='Ȣ', l='o', r='o')
GDS['Ocenteredtilde'] = GD(name='Ocenteredtilde', uni=0x019F, hex='019F', c='Ɵ', l='O', r='O', srcName='uni019F', gid=352)
GDS['Odblgrave'] = GD(name='Odblgrave', uni=0x020C, hex='020C', c='Ȍ', bl='O', base='O', accents=['dblgravecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Odieresismacron'] = GD(name='Odieresismacron', uni=0x022A, hex='022A', c='Ȫ', base='O', accents=['dieresismacroncmb'], anchors=['bottom', 'middle', 'top'])
GDS['Odotaccent'] = GD(name='Odotaccent', uni=0x022E, hex='022E', c='Ȯ', base='O', accents=['dotaccentcmb'], anchors=['bottom', 'middle', 'top'])
GDS['Odotaccentmacron'] = GD(name='Odotaccentmacron', uni=0x0230, hex='0230', c='Ȱ', base='O', accents=['dotaccentmacroncmb'], anchors=['bottom', 'middle', 'top'])
GDS['Oinvertedbreve'] = GD(name='Oinvertedbreve', uni=0x020E, hex='020E', c='Ȏ', base='O', accents=['invertedbrevecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Omacronacute'] = GD(name='Omacronacute', uni=0x1E52, hex='1E52', c='Ṓ', l='O', r='O', base='O', accents=['macronacutecmb'], srcName='uni1E52', anchors=['bottom', 'middle', 'top'], gid=1005)
GDS['Omacrongrave'] = GD(name='Omacrongrave', uni=0x1E50, hex='1E50', c='Ṑ', l='O', r='O', base='O', accents=['macrongravecmb'], srcName='uni1E50', anchors=['bottom', 'middle', 'top'], gid=1003)
GDS['Omega'] = GD(name='Omega', uni=0x03A9, hex='03A9', c='Ω', anchors=['bottom', 'top'], gid=558)
GDS['Omega-latin'] = GD(name='Omega-latin', uni=0xA7B6, hex='A7B6', c='Ꞷ')
GDS['Oogonek'] = GD(name='Oogonek', uni=0x01EA, hex='01EA', c='Ǫ', l='O', r='O', base='O', accents=['ogonekcmb'], srcName='uni01EA', anchors=['bottom', 'middle', 'top'], gid=427)
GDS['Oogonekmacron'] = GD(name='Oogonekmacron', uni=0x01EC, hex='01EC', c='Ǭ', l='O', r='O', base='O', accents=['macroncmb', 'ogonekcmb'], srcName='uni01EC', anchors=['bottom', 'middle', 'top'], gid=429)
GDS['Oslashacute'] = GD(name='Oslashacute', uni=0x01FE, hex='01FE', c='Ǿ', l='Oslash', r='Oslash', base='Oslash', accents=['acutecmb'], anchors=['bottom', 'middle', 'top'], gid=447, comment='Ǿ')
GDS['Otildeacute'] = GD(name='Otildeacute', uni=0x1E4C, hex='1E4C', c='Ṍ', l='O', r='O', base='O', accents=['tildeacutecmb'], srcName='uni1E4C', anchors=['bottom', 'middle', 'top'], gid=999)
GDS['Otildedieresis'] = GD(name='Otildedieresis', uni=0x1E4E, hex='1E4E', c='Ṏ', l='O', r='O', base='O', accents=['tildedieresiscmb'], srcName='uni1E4E', anchors=['bottom', 'middle', 'top'], gid=1001)
GDS['Otildemacron'] = GD(name='Otildemacron', uni=0x022C, hex='022C', c='Ȭ', base='O', accents=['tildemacroncmb'], anchors=['bottom', 'middle', 'top'])

# P

GDS['Pacute'] = GD(name='Pacute', uni=0x1E54, hex='1E54', c='Ṕ', l='P', w='P', base='P', accents=['acutecmb'], srcName='uni1E54', anchors=['bottom', 'middle', 'top'], gid=1007)
GDS['Phook'] = GD(name='Phook', uni=0x01A4, hex='01A4', c='Ƥ', srcName='uni01A4', gid=357)
GDS['Pstroke'] = GD(name='Pstroke', uni=0x2C63, hex='2C63', c='Ᵽ', l='Eth', r='P', base='P', anchors=['bottom', 'middle', 'top'])

# Q

GDS['Qhooktail'] = GD(name='Qhooktail', uni=0x024A, hex='024A', c='Ɋ')

# R

GDS['Rdblgrave'] = GD(name='Rdblgrave', uni=0x0210, hex='0210', c='Ȑ', l='R', r='R', base='R', accents=['dblgravecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Rinvertedbreve'] = GD(name='Rinvertedbreve', uni=0x0212, hex='0212', c='Ȓ', base='R', accents=['invertedbrevecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Rstroke'] = GD(name='Rstroke', uni=0x024C, hex='024C', c='Ɍ', l='Eth', base='R', anchors=['bottom', 'middle', 'top'])
GDS['Rtail'] = GD(name='Rtail', uni=0x2C64, hex='2C64', c='Ɽ', l='H', r='R')

# S

GDS['Sacutedotaccent'] = GD(name='Sacutedotaccent', uni=0x1E64, hex='1E64', c='Ṥ', l='S', w='S', base='S', accents=['acutedotaccentcmb'], srcName='uni1E64', anchors=['bottom', 'middle', 'top'], gid=1023)
GDS['Saltillo'] = GD(name='Saltillo', uni=0xA78B, hex='A78B', c='Ꞌ', l='quotesingle', r='quotesingle')
GDS['Scarondotaccent'] = GD(name='Scarondotaccent', uni=0x1E66, hex='1E66', c='Ṧ', l='S', w='S', base='S', accents=['carondotaccentcmb'], srcName='uni1E66', anchors=['bottom', 'middle', 'top'], gid=1025)
GDS['Sdotaccent'] = GD(name='Sdotaccent', uni=0x1E60, hex='1E60', c='Ṡ', l='S', w='S', base='S', accents=['dotaccentcmb'], srcName='uni1E60', anchors=['bottom', 'middle', 'top'], gid=1019)
GDS['Sdotbelowdotaccent'] = GD(name='Sdotbelowdotaccent', uni=0x1E68, hex='1E68', c='Ṩ', l='S', w='S', base='S', accents=['dotaccentcmb', 'dotbelowcmb'], srcName='uni1E68', anchors=['bottom', 'middle', 'top'], gid=1027)
GDS['Sobliquestroke'] = GD(name='Sobliquestroke', uni=0xA7A8, hex='A7A8', c='Ꞩ', w='S', base='S', anchors=['bottom', 'middle', 'top'])

# T

GDS['Tbar'] = GD(name='Tbar', uni=0x0166, hex='0166', c='Ŧ', l='T', r='T', base='T', gid=295, comment='Ŧ')
GDS['Tcircumflexbelow'] = GD(name='Tcircumflexbelow', uni=0x1E70, hex='1E70', c='Ṱ', l='T', r='T', base='T', accents=['circumflexbelowcmb'], srcName='uni1E70', anchors=['bottom', 'middle', 'top'], gid=1035)
GDS['Tdiagonalstroke'] = GD(name='Tdiagonalstroke', uni=0x023E, hex='023E', c='Ⱦ', w='T', bl='T', base='T', accents=['diagonalstrokecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Tdotaccent'] = GD(name='Tdotaccent', uni=0x1E6A, hex='1E6A', c='Ṫ', l='T', r='T', base='T', accents=['dotaccentcmb'], srcName='uni1E6A', anchors=['bottom', 'middle', 'top'], gid=1029)
GDS['Theta'] = GD(name='Theta', uni=0x0398, hex='0398', c='Θ', l='O', r='O', gid=542)
GDS['Thook'] = GD(name='Thook', uni=0x01AC, hex='01AC', c='Ƭ', srcName='uni01AC', gid=365)
GDS['Tretroflexhook'] = GD(name='Tretroflexhook', uni=0x01AE, hex='01AE', c='Ʈ', l='T', w='T', srcName='uni01AE', gid=367)

# U

GDS['Ubar'] = GD(name='Ubar', uni=0x0244, hex='0244', c='Ʉ', l='Eth', l2r='Eth', base='U', anchors=['bottom', 'middle', 'top'])
GDS['Ucircumflexbelow'] = GD(name='Ucircumflexbelow', uni=0x1E76, hex='1E76', c='Ṷ', l='U', r='U', base='U', accents=['circumflexbelowcmb'], srcName='uni1E76', anchors=['bottom', 'middle', 'top'], gid=1041)
GDS['Udblgrave'] = GD(name='Udblgrave', uni=0x0214, hex='0214', c='Ȕ', base='U', accents=['dblgravecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Udieresisbelow'] = GD(name='Udieresisbelow', uni=0x1E72, hex='1E72', c='Ṳ', l='U', r='U', base='U', accents=['dieresisbelow'], srcName='uni1E72', anchors=['bottom', 'middle', 'top'], gid=1037)
GDS['Uinvertedbreve'] = GD(name='Uinvertedbreve', uni=0x0216, hex='0216', c='Ȗ', base='U', accents=['invertedbrevecmb'], anchors=['bottom', 'middle', 'top'])
GDS['Umacrondieresis'] = GD(name='Umacrondieresis', uni=0x1E7A, hex='1E7A', c='Ṻ', l='U', r='U', base='U', accents=['macrondieresiscmb'], srcName='uni1E7A', anchors=['bottom', 'middle', 'top'], gid=1045)
GDS['Upsilonafrican'] = GD(name='Upsilonafrican', uni=0x01B1, hex='01B1', c='Ʊ', l='Omega', r='Omega', srcName='uni01B1', gid=370)
GDS['Utildeacute'] = GD(name='Utildeacute', uni=0x1E78, hex='1E78', c='Ṹ', l='U', r='U', base='U', accents=['tildeacutecmb'], srcName='uni1E78', anchors=['bottom', 'middle', 'top'], gid=1043)
GDS['Utildebelow'] = GD(name='Utildebelow', uni=0x1E74, hex='1E74', c='Ṵ', l='U', r='U', base='U', accents=['tildebelowcmb'], srcName='uni1E74', anchors=['bottom', 'middle', 'top'], gid=1039)

# V 

GDS['Vdotbelow'] = GD(name='Vdotbelow', uni=0x1E7E, hex='1E7E', c='Ṿ', l='V', r='V', base='V', accents=['dotbelowcmb'], srcName='uni1E7E', anchors=['bottom', 'middle', 'top'], gid=1049)
GDS['Vhook'] = GD(name='Vhook', uni=0x01B2, hex='01B2', c='Ʋ', l='U', r='O', srcName='uni01B2', gid=371, comment='Ʋ v, latin capital letter script')
GDS['Vtilde'] = GD(name='Vtilde', uni=0x1E7C, hex='1E7C', c='Ṽ', l='V', r='V', base='V', accents=['tildecmb'], srcName='uni1E7C', anchors=['bottom', 'middle', 'top'], gid=1047)

# W

GDS['Wdotaccent'] = GD(name='Wdotaccent', uni=0x1E86, hex='1E86', c='Ẇ', l='W', r='W', base='W', accents=['dotaccentcmb'], srcName='uni1E86', anchors=['bottom', 'middle', 'top'], gid=1057)
GDS['Whook'] = GD(name='Whook', uni=0x2C72, hex='2C72', c='Ⱳ')

# X

GDS['Xdotaccent'] = GD(name='Xdotaccent', uni=0x1E8A, hex='1E8A', c='Ẋ', base='X', accents=['dotaccentcmb'], srcName='uni1E8A', anchors=['bottom', 'middle', 'top'], gid=1061)

# Y

GDS['Yogh'] = GD(name='Yogh', uni=0x021C, hex='021C', c='Ȝ', l='three', r='three')
GDS['Ystroke'] = GD(name='Ystroke', uni=0x024E, hex='024E', c='Ɏ', base='Y', anchors=['bottom', 'middle', 'top'])
GDS['Zcircumflex'] = GD(name='Zcircumflex', uni=0x1E90, hex='1E90', c='Ẑ', l='Z', r='Z', base='Z', accents=['circumflexcmb'], srcName='uni1E90', anchors=['bottom', 'middle', 'top'], gid=1067)
GDS['Zstroke'] = GD(name='Zstroke', uni=0x01B5, hex='01B5', c='Ƶ', l='Z', r='Z', srcName='uni01B5', gid=374)

# a

GDS['adblgrave'] = GD(name='adblgrave', uni=0x0201, hex='0201', c='ȁ', base='a', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['adieresismacron'] = GD(name='adieresismacron', uni=0x01DF, hex='01DF', c='ǟ', w='a', bl='a', base='a', accents=['dieresismacroncmb'], srcName='uni01DF', isLower=True, anchors=['bottom', 'middle', 'top'], gid=416)
GDS['adotaccent'] = GD(name='adotaccent', uni=0x0227, hex='0227', c='ȧ', w='a', bl='a', base='a', accents=['dotaccentcmb'], srcName='uni0227', isLower=True, anchors=['bottom', 'middle', 'top'], gid=454)
GDS['adotaccentmacron'] = GD(name='adotmacron', uni=0x01E1, hex='01E1', c='ǡ', w='a', bl='a', base='a', accents=['dotaccentmacroncmb'], srcName='uni01E1', isLower=True, anchors=['bottom', 'middle', 'top'], gid=418)
GDS['aeacute'] = GD(name='aeacute', uni=0x01FD, hex='01FD', c='ǽ', r='e', bl='a', base='ae', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=446, comment='ǽ')
GDS['ainvertedbreve'] = GD(name='ainvertedbreve', uni=0x0203, hex='0203', c='ȃ', base='a', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['alpha-latin'] = GD(name='alpha-latin', uni=0x0251, hex='0251', c='ɑ', srcName='uni0251', isLower=True, gid=456)
GDS['arighthalfring'] = GD(name='arighthalfring', uni=0x1E9A, hex='1E9A', c='ẚ', base='a', accents=['ringhalfright'], srcName='uni1E9A', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1077)
GDS['aringacute'] = GD(name='aringacute', uni=0x01FB, hex='01FB', c='ǻ', base='a', accents=['ringacutecmb'], isLower=True, fixAccents=False, anchors=['bottom', 'middle', 'top'], gid=444, comment='ǻ')
GDS['aringbelow'] = GD(name='aringbelow', uni=0x1E01, hex='1E01', c='ḁ', base='a', accents=['ringbelowcmb'], srcName='uni1E01', isLower=True, anchors=['bottom', 'middle', 'top'], gid=924)
GDS['astroke'] = GD(name='astroke', uni=0x2C65, hex='2C65', c='ⱥ', base='a', accents=['slashlongcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['aturned'] = GD(name='aturned', uni=0x0250, hex='0250', c='ɐ', l2r='a', r2l='a', isLower=True)

GDS['acutemacroncmb'] = GD(name='acutemacroncmb', uni=0x1DC7, hex='1DC7', c='᷇', w=0, isLower=True, anchors=['_top', 'top'])
GDS['acutemacroncmb.uc'] = GD(name='acutemacroncmb.uc', w=0, srcName='acutemacroncmb', isLower=True, anchors=['_top', 'top'])

GDS['asuperior'] = GD(name='asuperior', uni=0x1D43, hex='1D43', c='ᵃ', srcName='uni1D43', l='osuperior', r='nsuperior', isLower=False, isMod=True, gid=908)
GDS['ainferior'] = GD(name='ainferior', uni=0x2090, hex='2090', c='ₐ', l='asuperior', r='asuperior', base='asuperior', isLower=True)

# b

GDS['bdotaccent'] = GD(name='bdotaccent', uni=0x1E03, hex='1E03', c='ḃ', base='b', accents=['dotaccentcmb'], srcName='uni1E03', isLower=True, anchors=['bottom', 'middle', 'top'], gid=926)
GDS['beta'] = GD(name='beta', uni=0x03B2, hex='03B2', c='β', isLower=True, gid=567)
GDS['beta-latin'] = GD(name='beta-latin', uni=0xA7B5, hex='A7B5', c='ꞵ', base='beta', isLower=True)
GDS['bilabialclick'] = GD(name='bilabialclick', uni=0x0298, hex='0298', c='ʘ', l='zero', r='zero')
GDS['blinebelow'] = GD(name='blinebelow', uni=0x1E07, hex='1E07', c='ḇ', base='b', accents=['macronbelowcmb'], srcName='uni1E07', isLower=True, anchors=['bottom', 'middle', 'top'], gid=930)
GDS['bstroke'] = GD(name='bstroke', uni=0x0180, hex='0180', c='ƀ', l='hyphen', r='b', srcName='uni0180', isLower=True, gid=321)

GDS['breveinvertedbelowcmb'] = GD(name='breveinvertedbelowcmb', uni=0x032F, hex='032F', c='̯', w=0, base='invertedbrevecmb', isLower=True, anchors=['_bottom', 'bottom'])
GDS['breveinvertedcmb'] = GD(name='breveinvertedcmb', uni=0x0311, hex='0311', c='̑', w=0, isLower=True, anchors=['_top', 'top'], gid=500)
GDS['breveinvertedcmb.uc'] = GD(name='breveinvertedcmb.uc', w=0, base='breveinvertedcmb', isLower=True, anchors=['_top', 'top'], gid=500)
GDS['breveinverteddoublecmb'] = GD(name='breveinverteddoublecmb', uni=0x0361, hex='0361', c='͡', w=0, isLower=True, anchors=['_top', 'top'])
GDS['breveinverteddoublecmb.uc'] = GD(name='breveinverteddoublecmb.uc', w=0, isLower=True, anchors=['_top', 'top'])

GDS['bsuperior'] = GD(name='bsuperior', uni=0x1D47, hex='1D47', c='ᵇ', l='hsuperior', r='osuperior', isLower=False, isMod=True)
GDS['binferior'] = GD(name='binferior', l='hsuperior', r='osuperior', base='bsuperior', isLower=False, isMod=True)

# c

GDS['ccedillaacute'] = GD(name='ccedillaacute', uni=0x1E09, hex='1E09', c='ḉ', base='c', accents=['cedillacmb', 'acutecmb'], srcName='uni1E09', isLower=True, anchors=['bottom', 'middle', 'top'], gid=932)
GDS['chi-latin'] = GD(name='chi-latin', uni=0xAB53, hex='AB53', c='ꭓ', isLower=True, comment='Based on Greek /chi')
GDS['chook'] = GD(name='chook', uni=0x0188, hex='0188', c='ƈ', l='c', w='c', srcName='uni0188', isLower=True, gid=329)
GDS['clickalveolar'] = GD(name='clickalveolar', uni=0x01C2, hex='01C2', c='ǂ', srcName='uni01C2', isLower=True, gid=387)
GDS['clickdental'] = GD(name='clickdental', uni=0x01C0, hex='01C0', c='ǀ', l='bar', r='bar', base='bar', isLower=True, gid=385)
GDS['clicklateral'] = GD(name='clicklateral', uni=0x01C1, hex='01C1', c='ǁ', l='bar', r='bar', base='bar', accents=['bar'], srcName='uni01C1', isLower=True, gid=386)
GDS['clickretroflex'] = GD(name='clickretroflex', uni=0x01C3, hex='01C3', c='ǃ', base='exclam', srcName='uni01C3', isLower=True, gid=388)
GDS['cstroke'] = GD(name='cstroke', uni=0x023C, hex='023C', c='ȼ', base='c', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['creversed'] = GD(name='creversed', uni=0x2184, hex='2184', c='ↄ')

GDS['commaabovecmb'] = GD(name='commaabovecmb', uni=0x0313, hex='0313', c='̓', w=0, base='koronis', isLower=True, anchors=['_top', 'top'])
GDS['commaabovecmb.uc'] = GD(name='commaabovecmb.uc', w=0, srcName='commaabovecmb', isLower=True, anchors=['_top', 'top'])
GDS['commaaboverightcmb'] = GD(name='commaaboverightcmb', uni=0x0315, hex='0315', c='̕', w=0, base='psili', isLower=True, anchors=['_top', 'top'])
GDS['commaaboverightcmb.uc'] = GD(name='commaaboverightcmb.uc', w=0, srcName='commaaboverightcmb', isLower=True, anchors=['_top', 'top'])
GDS['circumflexbelowcmb'] = GD(name='circumflexbelowcmb', uni=0x032D, hex='032D', c='̭', w=0, base='circumflexcmb', isLower=True, anchors=['_bottom', 'bottom'])

GDS['csuperior'] = GD(name='csuperior', uni=0x1D9C, hex='1D9C', c='ᶜ', l='osuperior', isLower=False, isMod=True)
GDS['colonsuperior'] = GD(name='colonsuperior', uni=0xA789, hex='A789', c='꞉', l='period', r='period', isLower=True, isMod=True)

# d

GDS['dbdigraph'] = GD(name='dbdigraph', uni=0x0238, hex='0238', c='ȸ', l='d', r='b', isLower=True)
GDS['dcedilla'] = GD(name='dcedilla', uni=0x1E11, hex='1E11', c='ḑ', base='d', accents=['cedillacmb'], srcName='uni1E11', isLower=True, anchors=['bottom', 'middle', 'top'], gid=940)
GDS['dcircumflexbelow'] = GD(name='dcircumflexbelow', uni=0x1E13, hex='1E13', c='ḓ', base='d', accents=['circumflexbelowcmb'], srcName='uni1E13', isLower=True, anchors=['bottom', 'middle', 'top'], gid=942)
GDS['ddotaccent'] = GD(name='ddotaccent', uni=0x1E0B, hex='1E0B', c='ḋ', base='d', accents=['dotaccentcmb'], srcName='uni1E0B', isLower=True, anchors=['bottom', 'middle', 'top'], gid=934)
GDS['dieresisbelow'] = GD(name='dieresisbelow', uni=0x0324, hex='0324', c='̤', w=0, isLower=True, anchors=['_bottom', 'bottom'], gid=1634)
GDS['dtail'] = GD(name='dtail', uni=0x0256, hex='0256', c='ɖ', w='d', isLower=True, gid=459, comment='Glyph unicode 0256 is the lowercase letter "ɖ" in the International Phonetic Alphabet (IPA). It is used to represent a voiced retroflex plosive sound in various languages, including African languages such as Igbo, Yoruba, and Ewe. It is also used in some Native American languages such as Navajo and Tlingit. In linguistics, the IPA is commonly used to transcribe the sounds of human speech, and the glyph unicode 0256 helps to accurately represent this specific sound.')
GDS['dz'] = GD(name='dz', uni=0x01F3, hex='01F3', c='ǳ', l='d', r='z', base='d', accents=['z'], srcName='uni01F3', isLower=True, gid=436)
GDS['dzcaron'] = GD(name='dzcaron', uni=0x01C6, hex='01C6', c='ǆ', l='d', r='z', base='d', accents=['z', 'caroncmb'], srcName='uni01C6', isLower=True, gid=391)

GDS['dblgravecmb'] = GD(name='dblgravecmb', uni=0x030F, hex='030F', c='̏', w=0, isLower=True, anchors=['_top', 'top'], gid=499)
GDS['dblgravecmb.uc'] = GD(name='dblgravecmb.uc',w=0, srcName='dblgravecmb', isLower=True, anchors=['_top', 'top'], gid=499)
GDS['dotaboverightcmb'] = GD(name='dotaboverightcmb', uni=0x0358, hex='0358', c='͘', w=0, base='dotaccentcmb', isLower=True, anchors=['_top', 'top'])
GDS['dotaboverightcmb.uc'] = GD(name='dotaboverightcmb.uc', w=0, srcName='dotaboverightcmb', isLower=True, anchors=['_top', 'top'])
GDS['doublebrevebelowcmb'] = GD(name='doublebrevebelowcmb', uni=0x035C, hex='035C', c='͜', w=0, base='doublebrevecmb', isLower=True, anchors=['_bottom', 'bottom'])
GDS['doublebrevebelowcmb'] = GD(name='doublebrevebelowcmb', w=0, srcName='doublebrevebelowcmb', isLower=True, anchors=['_bottom', 'bottom'])
GDS['doublebrevecmb'] = GD(name='doublebrevecmb', uni=0x035D, hex='035D', c='͝', w=0, srcName='uni035D', isLower=True, anchors=['_top', 'top'])
GDS['doublebrevecmb.uc'] = GD(name='doublebrevecmb.uc', w=0, srcName='doublebrevecmb', isLower=True, anchors=['_top', 'top'])

GDS['dsuperior'] = GD(name='dsuperior', l='omod', r='lmod', srcName='uni1D49', isLower=False, isMod=True, gid=909)
GDS['dinferior'] = GD(name='dinferior', l='dsuperior', r='dsuperior', base='dsuperior', isLower=True)

GDS['dblquotesuperior'] = GD(name='dblquotesuperior', uni=0x02EE, hex='02EE', c='ˮ', base='quotedblright', isLower=True, isMod=True)

# e

GDS['ecedilla'] = GD(name='ecedilla', uni=0x0229, hex='0229', c='ȩ', base='e', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ecedillabreve'] = GD(name='ecedillabreve', uni=0x1E1D, hex='1E1D', c='ḝ', w='e', base='e', accents=['cedillacmb', 'brevecmb'], srcName='uni1E1D', isLower=True, anchors=['bottom', 'middle', 'top'], gid=952)
GDS['ecircumflexbelow'] = GD(name='ecircumflexbelow', uni=0x1E19, hex='1E19', c='ḙ', w='e', base='e', accents=['circumflexbelowcmb'], srcName='uni1E19', isLower=True, anchors=['bottom', 'middle', 'top'], gid=948)
GDS['edblgrave'] = GD(name='edblgrave', uni=0x0205, hex='0205', c='ȅ', w='e', bl='e', base='e', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['einvertedbreve'] = GD(name='einvertedbreve', uni=0x0207, hex='0207', c='ȇ', base='e', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['emacronacute'] = GD(name='emacronacute', uni=0x1E17, hex='1E17', c='ḗ', w='e', bl='e', base='e', accents=['macronacutecmb'], srcName='uni1E17', isLower=True, anchors=['bottom', 'middle', 'top'], gid=946)
GDS['emacrongrave'] = GD(name='emacrongrave', uni=0x1E15, hex='1E15', c='ḕ', bl='e', base='e', accents=['macrongravecmb'], srcName='uni1E15', isLower=True, anchors=['bottom', 'middle', 'top'], gid=944)
GDS['epsilon'] = GD(name='epsilon', uni=0x03B5, hex='03B5', c='ε', isLower=True, anchors=['top'], gid=570, comment='ε')
GDS['esh'] = GD(name='esh', uni=0x0283, hex='0283', c='ʃ', r='f', srcName='uni0283', isLower=True, gid=466)
GDS['eshreversedloop'] = GD(name='eshreversedloop', uni=0x01AA, hex='01AA', c='ƪ', r='l', srcName='uni01AA', isLower=True, gid=363)
GDS['estroke'] = GD(name='estroke', uni=0x0247, hex='0247', c='ɇ', base='e', accents=['slashlongcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['etildebelow'] = GD(name='etildebelow', uni=0x1E1B, hex='1E1B', c='ḛ', l='e', r='e', base='e', accents=['tildebelowcmb'], srcName='uni1E1B', isLower=True, anchors=['bottom', 'middle', 'top'], gid=950)
GDS['ezh'] = GD(name='ezh', uni=0x0292, hex='0292', c='ʒ', l='three', r='three', isLower=True, anchors=['top'], gid=468)
GDS['ezhcaron'] = GD(name='ezhcaron', uni=0x01EF, hex='01EF', c='ǯ', base='ezh', accents=['caroncmb'], srcName='uni01EF', isLower=True, anchors=['top'], gid=432)
GDS['ezhreversed'] = GD(name='ezhreversed', uni=0x01B9, hex='01B9', c='ƹ', l='o', l2r='three', srcName='uni01B9', isLower=True, gid=378)

GDS['esuperior'] = GD(name='esuperior', uni=0x1D49, hex='1D49', c='ᵉ', l='osuperior', r='osuperior', srcName='uni1D49', isLower=False, isMod=True, gid=909)
GDS['einferior'] = GD(name='einferior', uni=0x2091, hex='2091', c='ₑ', l='esuperior', r='esuperior', base='emod', isLower=True)
GDS['egravesuperior'] = GD(name='egravesuperior', l='esuperior', r='esuperior', srcName='esuperior', isLower=False, isMod=True, gid=909)
GDS['egraveinferior'] = GD(name='egraveinferior', l='egravesuperior', r='egravesuperior', base='egravesuperior', isLower=True)

# f

GDS['fStroke'] = GD(name='fStroke', uni=0xA799, hex='A799', c='ꞙ', base='f', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['fdotaccent'] = GD(name='fdotaccent', uni=0x1E1F, hex='1E1F', c='ḟ', rightMin='-100', base='f', accents=['dotaccentcmb'], srcName='uni1E1F', isLower=True, anchors=['bottom', 'middle', 'top'], gid=954)
GDS['florin'] = GD(name='florin', uni=0x0192, hex='0192', c='ƒ', w='zero.tnum', gid=339, comment='ƒ script f, latin small letter')
GDS['fourthtonechinese'] = GD(name='fourthtonechinese', uni=0x02CB, hex='02CB', c='ˋ', base='gravecmb', anchors=['top'])
GDS['firsttonechinese'] = GD(name='firsttonechinese', uni=0x02C9, hex='02C9', w=0, c='ˉ', isLower=True, anchors=['_top', 'top'])
GDS['fraction'] = GD(name='fraction', uni=0x2044, hex='2044', c='⁄', isLower=False, comment='⁄ solidus')


# g

GDS['gacute'] = GD(name='gacute', uni=0x01F5, hex='01F5', c='ǵ', base='g', accents=['acutecmb'], srcName='uni01F5', isLower=True, anchors=['bottom', 'middle', 'top'], gid=438)
GDS['gamma-latin'] = GD(name='gamma-latin', uni=0x0263, hex='0263', c='ɣ', isLower=True)
GDS['ghook'] = GD(name='ghook', uni=0x0260, hex='0260', c='ɠ', l='g', w='g', isLower=True)
GDS['glottalstop'] = GD(name='glottalstop', uni=0x0294, hex='0294', c='ʔ', isLower=True)
GDS['glottalstopreversed'] = GD(name='glottalstopreversed', uni=0x0295, hex='0295', c='ʕ', l2r='question', r2l='question')
GDS['glottalstopreversedmod'] = GD(name='glottalstopreversedmod', uni=0x02C1, hex='02C1', c='ˁ', srcName='uni02C1', isMod=True, gid=474)
GDS['glottalstopsmall'] = GD(name='glottalstopsmall', uni=0x0242, hex='0242', c='ɂ', l='question', r='question', isSc=True)
GDS['gravemacroncmb'] = GD(name='gravemacroncmb', uni=0x1DC5, hex='1DC5', c='᷅', w=0, base='firsttonechinese', accents=['gravecmb'], isLower=True, anchors=['_top', 'top'])
GDS['gsingle'] = GD(name='gsingle', uni=0x0261, hex='0261', c='ɡ', base='g', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['gstroke'] = GD(name='gstroke', uni=0x01E5, hex='01E5', c='ǥ', l='g', r='hyphen', srcName='uni01E5', isLower=True, gid=422)

GDS['gsuperior'] = GD(name='gsuperior', uni=0x1D4D, hex='1D4D', c='ᵍ', srcName='uni1D4D', l='osuperior', l2r='nsuperior', isLower=False, isMod=True, gid=911)
GDS['ginferior'] = GD(name='ginferior', l='gsuperior', r='gsuperior', base='gsuperior', isLower=True)

GDS['glottalstopmod'] = GD(name='glottalstopmod', uni=0x02C0, hex='02C0', c='ˀ', isMod=True)

# h

GDS['hcaron'] = GD(name='hcaron', uni=0x021F, hex='021F', c='ȟ', base='h', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['hdotaccent'] = GD(name='hdotaccent', uni=0x1E23, hex='1E23', c='ḣ', base='h', accents=['dotaccentcmb'], srcName='uni1E23', isLower=True, anchors=['bottom', 'middle', 'top'], gid=958)
GDS['heng'] = GD(name='heng', uni=0xA727, hex='A727', c='ꜧ', l='h', isLower=True)
GDS['henghook'] = GD(name='henghook', uni=0x0267, hex='0267', c='ɧ', l='h', r='h', isLower=True)
GDS['hhook'] = GD(name='hhook', uni=0x0266, hex='0266', c='ɦ', l='h', r='h', isLower=True)
GDS['hturned'] = GD(name='hturned', uni=0x0265, hex='0265', c='ɥ', isLower=True)

GDS['hsuperior'] = GD(name='hsuperior', uni=0x02B0, hex='02B0', c='ʰ', l='nsuperior', r='nsuperior', isMod=True)
GDS['hinferior'] = GD(name='hinferior', l='hinferior', r='hinferior', base='hsuperior', isLower=True)
GDS['hhooksuperior'] = GD(name='hhooksuperior', uni=0x02B1, hex='02B1', c='ʱ', l='nsuperior', r='nsuperior', isMod=True)
GDS['hhookinferior'] = GD(name='hhookinferior', base='hhookinferior', l='nsuperior', r='nsuperior', isMod=True)

# i

GDS['idblgrave'] = GD(name='idblgrave', uni=0x0209, hex='0209', c='ȉ', w='idotless', bl='idotless', base='idotless', accents=['dblgravecmb'], isLower=True, anchors=['top'])
GDS['idieresisacute'] = GD(name='idieresisacute', uni=0x1E2F, hex='1E2F', c='ḯ', w='idotless', bl='idotless', base='idotless', accents=['dieresisacutecmb'], srcName='uni1E2F', isLower=True, anchors=['bottom', 'middle', 'top'], gid=970)
GDS['iinvertedbreve'] = GD(name='iinvertedbreve', uni=0x020B, hex='020B', c='ȋ', w='idotless', bl='idotless', base='idotless', accents=['breveinvertedcmb'], isLower=True, anchors=['top'])
GDS['ij'] = GD(name='ij', uni=0x0133, hex='0133', c='ĳ', l='i', r='j', base='i', accents=['j'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=244, comment='ĳ SMALL LIGATURE IJ, LATIN')
GDS['iota-latin'] = GD(name='iota-latin', uni=0x0269, hex='0269', c='ɩ', isLower=True)
GDS['itildebelow'] = GD(name='itildebelow', uni=0x1E2D, hex='1E2D', c='ḭ', w='idotless', bl='i', base='i', accents=['tildebelowcmb'], srcName='uni1E2D', isLower=True, anchors=['bottom', 'middle', 'top'], gid=968)

GDS['isuperior'] = GD(name='isuperior', uni=0x2071, hex='2071', c='ⁱ', l2r='isuperior', isMod=True)
GDS['iinferior'] = GD(name='iinderior', l='isuperior', r='isuperior', base='isuperior', isMod=True)

# j

GDS['jcaron'] = GD(name='jcaron', uni=0x01F0, hex='01F0', c='ǰ', l='j', w='j', base='jdotless', accents=['caroncmb'], srcName='uni01F0', isLower=True, anchors=['bottom', 'middle', 'top'], gid=433)
GDS['jcrossedtail'] = GD(name='jcrossedtail', uni=0x029D, hex='029D', c='ʝ', rightMin='minRight', isLower=True)
GDS['jdotlessstroke'] = GD(name='jdotlessstroke', uni=0x025F, hex='025F', c='ɟ', l='jdotless', r='hyphen', isLower=True)
GDS['jdotlessstrokehook'] = GD(name='jdotlessstrokehook', uni=0x0284, hex='0284', c='ʄ', l='j', r='f', isLower=True)
GDS['jstroke'] = GD(name='jstroke', uni=0x0249, hex='0249', c='ɉ', l='j', r='hyphen', base='j', isLower=True, anchors=['bottom', 'middle'])

GDS['jsuperior'] = GD(name='jsuperior', uni=0x02B2, hex='02B2', c='ʲ', r='isuperior', isMod=True)
GDS['jinferior'] = GD(name='jsuperior', r='isuperior', base='jsuperior', isMod=True)

# k

GDS['kacute'] = GD(name='kacute', uni=0x1E31, hex='1E31', c='ḱ', base='k', accents=['acutecmb'], srcName='uni1E31', isLower=True, anchors=['bottom', 'middle', 'top'], gid=972)
GDS['kcaron'] = GD(name='kcaron', uni=0x01E9, hex='01E9', c='ǩ', base='k', accents=['caroncmb'], srcName='uni01E9', isLower=True, anchors=['bottom', 'middle', 'top'], gid=426)
GDS['kgreenlandic'] = GD(name='kgreenlandic', uni=0x0138, hex='0138', c='ĸ', isLower=True, anchors=['top'], gid=249, comment='ĸ LATIN SMALL LETTER KRA')
GDS['kstroke'] = GD(name='kstroke', uni=0xA741, hex='A741', c='ꝁ', l='hyphen', r='k', base='k', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['koronis'] = GD(name='koronis', uni=0x1FBD, hex='1FBD', c='᾽', w=0, isLower=True, anchors=['top'], gid=1347)

GDS['ksuperior'] = GD(name='ksuperior', uni=0x1D4F, hex='1D4F', c='ᵏ', l='hsuperior', srcName='uni1D4F', isLower=False, isMod=True, gid=912)
GDS['kinferior'] = GD(name='kinferior', uni=0x2096, hex='2096', c='ₖ', l='ksuperior', r='ksuperior', base='ksuperior')

# l

GDS['lambda'] = GD(name='lambda', uni=0x03BB, hex='03BB', c='λ', l='v', r='v', isLower=True, gid=576)
GDS['lambdastroke'] = GD(name='lambdastroke', uni=0x019B, hex='019B', c='ƛ', l='lambda', w='lambda', srcName='uni019B', isLower=True, gid=348)
GDS['lbar'] = GD(name='lbar', uni=0x019A, hex='019A', c='ƚ', l='t', r='t', srcName='uni019A', isLower=True, gid=347)
GDS['lbelt'] = GD(name='lbelt', uni=0x026C, hex='026C', c='ɬ', l='omod', r='hyphen', isLower=True)
GDS['lcircumflexbelow'] = GD(name='lcircumflexbelow', uni=0x1E3D, hex='1E3D', c='ḽ', w='l', bl='l', base='l', accents=['circumflexbelowcmb'], srcName='uni1E3D', isLower=True, anchors=['bottom', 'middle', 'top'], gid=984)
GDS['ldot'] = GD(name='ldot', uni=0x0140, hex='0140', c='ŀ', l='l', r='off', base='l', accents=['dotmiddlecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=257, comment='ŀ MIDDLE DOT, LATIN SMALL LETTER L WITH')
GDS['ldoublebar'] = GD(name='ldoublebar', uni=0x2C61, hex='2C61', c='ⱡ', l='hyphen', r='hyphen', isLower=True)
GDS['lj'] = GD(name='lj', uni=0x01C9, hex='01C9', c='ǉ', l='l', r='j', base='l', accents=['j'], srcName='uni01C9', isLower=True, gid=394)
GDS['lmiddletilde'] = GD(name='lmiddletilde', uni=0x026B, hex='026B', c='ɫ', l='asciitilde', r='asciitilde', isLower=True)
GDS['longs'] = GD(name='longs', uni=0x017F, hex='017F', c='ſ', w='f', r2l='j', isLower=True, fixAccents=False, anchors=['top'], gid=320, comment='ſ S, LATIN SMALL LETTER LONG')
GDS['longsdotaccent'] = GD(name='longsdotaccent', uni=0x1E9B, hex='1E9B', c='ẛ', w='longs', bl='longs', base='longs', accents=['dotaccentcmb'], srcName='uni1E9B', isLower=True, anchors=['top'], gid=1078)
GDS['lowlinecmb'] = GD(name='lowlinecmb', uni=0x0332, hex='0332', c='̲', w=0, isLower=True, anchors=['_bottom', 'bottom'])

GDS['lsuperior'] = GD(name='lsuperior', uni=0x02E1, hex='02E1', c='ˡ', l='Hsuperior', r='Hsuperior', isMod=True)
GDS['linferior'] = GD(name='linferior', uni=0x2097, hex='2097', c='ₗ', l='lsuperior', r='lsuperior', base='lsuperior', isLower=True)

# m

GDS['macronacutecmb'] = GD(name='macronacutecmb', uni=0x1DC4, hex='1DC4', c='᷄', w=0, base='firsttonechinese', accents=['acutecmb'], isLower=True, anchors=['_top', 'top'])
GDS['macrongravecmb'] = GD(name='macrongravecmb', uni=0x1DC6, hex='1DC6', c='᷆', w=0, isLower=True, anchors=['_top', 'top'])
GDS['macute'] = GD(name='macute', uni=0x1E3F, hex='1E3F', c='ḿ', base='m', accents=['acutecmb'], srcName='uni1E3F', isLower=True, anchors=['bottom', 'middle', 'top'], gid=986)
GDS['mhook'] = GD(name='mhook', uni=0x0271, hex='0271', c='ɱ', isLower=True)
GDS['minusmod'] = GD(name='minusmod', uni=0x02D7, hex='02D7', c='˗', l='48', r='48', srcName='uni02D7', isLower=True, isMod=True, gid=478)
GDS['mturned'] = GD(name='mturned', uni=0x026F, hex='026F', c='ɯ', isLower=True)

GDS['minusbelowcmb'] = GD(name='minusbelowcmb', uni=0x0320, hex='0320', c='̠', w=0, base='minusmod', isLower=True, anchors=['_bottom', 'bottom'])

GDS['msuperior'] = GD(name='msuperior', uni=0x1D50, hex='1D50', c='ᵐ', l='nsuperior', r='nsuperior', srcName='uni1D50', isLower=False, isMod=True)
GDS['minferior'] = GD(name='minferior', uni=0x2098, hex='2098', c='ₘ', l='minferior', r='minferior', base='minferior', isLower=True)
GDS['mu'] = GD(name='mu', uni=0x03BC, hex='03BC', c='μ', l='verticalbar', r='u', isLower=True, gid=577, comment='mu')

# n

GDS['napostrophe'] = GD(name='napostrophe', uni=0x0149, hex='0149', c='ŉ', base='n', accents=['quoterightcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=266, comment='ŉ')
GDS['ncircumflexbelow'] = GD(name='ncircumflexbelow', uni=0x1E4B, hex='1E4B', c='ṋ', base='n', accents=['circumflexbelowcmb'], srcName='uni1E4B', isLower=True, anchors=['bottom', 'middle', 'top'], gid=998)
GDS['ngrave'] = GD(name='ngrave', uni=0x01F9, hex='01F9', c='ǹ', w='n', bl='n', base='n', accents=['gravecmb'], srcName='uni01F9', isLower=True, anchors=['bottom', 'middle', 'top'], gid=442)
GDS['nj'] = GD(name='nj', uni=0x01CC, hex='01CC', c='ǌ', base='n', accents=['j'], srcName='uni01CC', isLower=True)
GDS['nlegrightlong'] = GD(name='nlegrightlong', uni=0x019E, hex='019E', c='ƞ', srcName='uni019E', isLower=True)

GDS['nsuperior'] = GD(name='nsuperior', uni=0x207F, hex='207F', c='ⁿ', isMod=True, gid=1432)
GDS['ninferior'] = GD(name='ninferior', uni=0x2099, hex='2099', c='ₙ', l='nsuperior', r='nsuperior', base='nsuperior')

# o

GDS['obarred'] = GD(name='obarred', uni=0x0275, hex='0275', c='ɵ', base='o', isLower=True, anchors=['top'], gid=464)
GDS['odblgrave'] = GD(name='odblgrave', uni=0x020D, hex='020D', c='ȍ', bl='o', base='o', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['odieresismacron'] = GD(name='odieresismacron', uni=0x022B, hex='022B', c='ȫ', w='o', bl='o', base='o', accents=['dieresismacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['odotaccent'] = GD(name='odotaccent', uni=0x022F, hex='022F', c='ȯ', w='o', bl='o', base='o', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['odotaccentmacron'] = GD(name='odotaccentmacron', uni=0x0231, hex='0231', c='ȱ', w='o', bl='o', base='o', accents=['dotaccentmacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['oinvertedbreve'] = GD(name='oinvertedbreve', uni=0x020F, hex='020F', c='ȏ', base='o', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['omacronacute'] = GD(name='omacronacute', uni=0x1E53, hex='1E53', c='ṓ', l='o', r='o', base='o', accents=['macronacutecmb'], srcName='uni1E53', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1006)
GDS['omacrongrave'] = GD(name='omacrongrave', uni=0x1E51, hex='1E51', c='ṑ', l='o', r='o', base='o', accents=['macrongravecmb'], srcName='uni1E51', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1004)
GDS['omega'] = GD(name='omega', uni=0x03C9, hex='03C9', c='ω', isLower=True, fixSpacing=False, anchors=['bottom', 'top'], gid=590, comment='ω')
GDS['omega-latin'] = GD(name='omega-latin', uni=0xA7B7, hex='A7B7', c='ꞷ', base='omega', isLower=True, anchors=['bottom', 'top'])
GDS['oogonek'] = GD(name='oogonek', uni=0x01EB, hex='01EB', c='ǫ', base='o', accents=['ogonekcmb'], srcName='uni01EB', isLower=True, anchors=['bottom', 'middle', 'top'], gid=428)
GDS['oogonekmacron'] = GD(name='oogonekmacron', uni=0x01ED, hex='01ED', c='ǭ', base='oogonek', accents=['macroncmb'], srcName='uni01ED', isLower=True, anchors=['top'], gid=430)
GDS['oslashacute'] = GD(name='oslashacute', uni=0x01FF, hex='01FF', c='ǿ', base='oslash', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=448, comment='ǿ')
GDS['otildeacute'] = GD(name='otildeacute', uni=0x1E4D, hex='1E4D', c='ṍ', base='o', accents=['tildeacutecmb'], srcName='uni1E4D', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1000)
GDS['otildedieresis'] = GD(name='otildedieresis', uni=0x1E4F, hex='1E4F', c='ṏ', base='o', accents=['tildedieresiscmb'], srcName='uni1E4F', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1002)
GDS['otildemacron'] = GD(name='otildemacron', uni=0x022D, hex='022D', c='ȭ', base='o', accents=['tildemacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ou'] = GD(name='ou', uni=0x0223, hex='0223', c='ȣ', l='o', r='o')

GDS['osuperior'] = GD(name='osuperior', uni=0x1D52, hex='1D52', c='ᵒ', srcName='uni1D52', isLower=False, l2r='osuperior', isMod=True)
GDS['oinferior'] = GD(name='oinferior', uni=0x2092, hex='2092', c='ₒ', l='osuperior', r='osuperior', base='osuperior', isLower=True)

# p

GDS['pacute'] = GD(name='pacute', uni=0x1E55, hex='1E55', c='ṕ', l='p', w='p', base='p', accents=['acutecmb'], srcName='uni1E55', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1008)
GDS['phi-latin'] = GD(name='phi-latin', uni=0x0278, hex='0278', c='ɸ', l='phi', r='phi', isLower=True)
GDS['phook'] = GD(name='phook', uni=0x01A5, hex='01A5', c='ƥ', l='p', r='p', srcName='uni01A5', isLower=True, gid=358)
GDS['primemod'] = GD(name='primemod', uni=0x02B9, hex='02B9', c='ʹ', base='quoteright', isMod=True)
GDS['pstroke'] = GD(name='pstroke', uni=0x1D7D, hex='1D7D', c='ᵽ', l='hyphen', r='hyphen', base='p', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['psili'] = GD(name='psili', uni=0x1FBF, hex='1FBF', c='᾿', w=0, isLower=True, anchors=['_top', 'top'], gid=1349)

GDS['psuperior'] = GD(name='psuperior', uni=0x1D56, hex='1D56', c='ᵖ', srcName='uni1D56', l='tsuperior', r='bsuperior', isLower=False, isMod=True)
GDS['pinferior'] = GD(name='pinferior', uni=0x209A, hex='209A', c='ₚ', l='psuperior', r='psuperior', base='psuperior')

# q

GDS['qhooktail'] = GD(name='qhooktail', uni=0x024B, hex='024B', c='ɋ', l='o', w='q', isLower=True)
GDS['qpdigraph'] = GD(name='qpdigraph', uni=0x0239, hex='0239', c='ȹ', l='q', r='p', isLower=True)

GDS['qsuperior'] = GD(name='qsuperior', l='oinferior', r='linferior', isMod=True)
GDS['qinferior'] = GD(name='qinferior', l='qsuperior', r='qsuperior', base='qsuperior', isMod=True)

# r

GDS['ramshorn'] = GD(name='ramshorn', uni=0x0264, hex='0264', c='ɤ', l='Y', r='Y', isLower=True)
GDS['rdblgrave'] = GD(name='rdblgrave', uni=0x0211, hex='0211', c='ȑ', w='r', bl='r', base='r', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['rhook'] = GD(name='rhook', uni=0x027D, hex='027D', c='ɽ', l='r', w='r', isLower=True)
GDS['ringbelowcmb'] = GD(name='ringbelowcmb', uni=0x0325, hex='0325', c='̥', l='center', w=0, base='ringcmb', isLower=True, anchors=['_bottom', 'bottom'], comment='COMBINING RING BELOW')
GDS['rinvertedbreve'] = GD(name='rinvertedbreve', uni=0x0213, hex='0213', c='ȓ', base='r', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['rstroke'] = GD(name='rstroke', uni=0x024D, hex='024D', c='ɍ', base='r', isLower=True, anchors=['bottom', 'middle', 'top'])

GDS['rsuperior'] = GD(name='rsuperior', uni=0x02B3, hex='02B3', c='ʳ', l='nsuperior', r='48', srcName='uni02B3', isMod=True)
GDS['rinferior'] = GD(name='rinferior', l='rinferior', r='rinferior', base='rinferior', isMod=True)

GDS['rbelowcmb'] = GD(name='rbelowcmb', uni=0x1DCA, hex='1DCA', c='᷊', w=0, base='rmod', anchors=['_bottom', 'bottom'])

# s

GDS['sacutedotaccent'] = GD(name='sacutedotaccent', uni=0x1E65, hex='1E65', c='ṥ', l='s', w='s', base='s', accents=['acutedotaccentcmb'], srcName='uni1E65', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1024)
GDS['saltillo'] = GD(name='saltillo', uni=0xA78C, hex='A78C', c='ꞌ', base='quotesingle', isLower=True)
GDS['scarondotaccent'] = GD(name='scarondotaccent', uni=0x1E67, hex='1E67', c='ṧ', l='s', r='s', base='s', accents=['carondotaccentcmb'], srcName='uni1E67', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1026)
GDS['sdotaccent'] = GD(name='sdotaccent', uni=0x1E61, hex='1E61', c='ṡ', l='s', r='s', base='s', accents=['dotaccentcmb'], srcName='uni1E61', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1020)
GDS['sdotbelowdotaccent'] = GD(name='sdotbelowdotaccent', uni=0x1E69, hex='1E69', c='ṩ', l='s', r='s', base='s', accents=['dotbelowcmb', 'dotaccentcmb'], srcName='uni1E69', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1028)
GDS['secondtonechinese'] = GD(name='secondtonechinese', uni=0x02CA, hex='02CA', c='ˊ', base='acutecmb', isLower=True, anchors=['top'])
GDS['shortequalmod'] = GD(name='shortequalmod', uni=0xA78A, hex='A78A', c='꞊', l='48', r='48', isLower=True, isMod=True)
GDS['sobliquestroke'] = GD(name='sobliquestroke', uni=0xA7A9, hex='A7A9', c='ꞩ', base='s', isLower=True, anchors=['bottom', 'middle', 'top'])

GDS['ssuperior'] = GD(name='ssuperior', uni=0x02E2, hex='02E2', c='ˢ', l2r='ssuperior', isMod=True)
GDS['sinferior'] = GD(name='sinferior', uni=0x209B, hex='209B', c='ₛ', l='ssuperior', r='ssuperior', base='ssuperior', isLower=True)
GDS['schwasuperior'] = GD(name='schwasuperior', uni=0x1D4A, hex='1D4A', c='ᵊ', l2r='esuperior', r2l='esuperior', srcName='uni1D4A', isLower=False, isMod=True)
GDS['schwainferior'] = GD(name='schwainferior', uni=0x2094, hex='2094', c='ₔ', l='schwasuperior', r='schwasuperior', base='schwasuperior', isLower=True)

# t

GDS['tbar'] = GD(name='tbar', uni=0x0167, hex='0167', c='ŧ', l='t', r='t', isLower=True, gid=296, comment='ŧ T WITH STROKE, LATIN SMALL LETTER')
GDS['tcircumflexbelow'] = GD(name='tcircumflexbelow', uni=0x1E71, hex='1E71', c='ṱ', base='t', accents=['circumflexbelowcmb'], srcName='uni1E71', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1036)
GDS['tdiagonalstroke'] = GD(name='tdiagonalstroke', uni=0x2C66, hex='2C66', c='ⱦ', w='t', bl='t', base='t', accents=['slashlongcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['tdieresis'] = GD(name='tdieresis', uni=0x1E97, hex='1E97', c='ẗ', w='t', bl='t', base='t', accents=['dieresiscmb'], srcName='uni1E97', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1074)
GDS['tdotaccent'] = GD(name='tdotaccent', uni=0x1E6B, hex='1E6B', c='ṫ', base='t', accents=['dotaccentcmb'], srcName='uni1E6B', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1030)
GDS['tesh'] = GD(name='tesh', uni=0x02A7, hex='02A7', c='ʧ', l='t', r='off', isLower=True)
GDS['theta'] = GD(name='theta', uni=0x03B8, hex='03B8', c='θ', gid=573)
GDS['thook'] = GD(name='thook', uni=0x01AD, hex='01AD', c='ƭ', l='t', w='t', srcName='uni01AD', isLower=True, gid=366)
GDS['tildebelowcmb'] = GD(name='tildebelow', uni=0x0330, hex='0330', c='̰', w=0, base='tildecmb', isLower=True, anchors=['_bottom', 'bottom'], gid=1706)
GDS['tildeoverlaycmb'] = GD(name='tildeoverlaycmb', uni=0x0334, hex='0334', c='̴', w=0, base='tildecmb', isLower=True, anchors=['_middle', 'middle'])
GDS['tretroflexhook'] = GD(name='tretroflexhook', uni=0x0288, hex='0288', c='ʈ', l='t', r='t', isLower=True)

GDS['tsuperior'] = GD(name='tsuperior', uni=0x0000, hex='0000', c='????', isLower=True, anchors=[])
GDS['tinferior'] = GD(name='tinferior', uni=0x209C, hex='209C', c='ₜ', l='tsuperior', r='tsuperior', base='tsuperior', isLower=True)

# u

GDS['ubar'] = GD(name='ubar', uni=0x0289, hex='0289', c='ʉ', l='hyphen', r='hyphen', base='u', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ucircumflexbelow'] = GD(name='ucircumflexbelow', uni=0x1E77, hex='1E77', c='ṷ', l='u', r='u', base='u', accents=['circumflexbelowcmb'], srcName='uni1E77', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1042)
GDS['udblgrave'] = GD(name='udblgrave', uni=0x0215, hex='0215', c='ȕ', w='u', bl='u', base='u', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['udieresisbelow'] = GD(name='udieresisbelow', uni=0x1E73, hex='1E73', c='ṳ', l='u', r='u', base='u', accents=['dieresisbelow'], srcName='uni1E73', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1038)
GDS['uinvertedbreve'] = GD(name='uinvertedbreve', uni=0x0217, hex='0217', c='ȗ', base='u', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['umacrondieresis'] = GD(name='umacrondieresis', uni=0x1E7B, hex='1E7B', c='ṻ', l='u', r='u', base='u', accents=['macrondieresiscmb'], srcName='uni1E7B', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1046)
GDS['uniA7AE'] = GD(name='uniA7AE', uni=0xA7AE, hex='A7AE', c='Ɪ', r='L', l2r='L', isLower=True)
GDS['upsilon-latin'] = GD(name='upsilon-latin', uni=0x028A, hex='028A', c='ʊ', l='o', r='o', srcName='uni028A', isLower=True, gid=467)
GDS['utildeacute'] = GD(name='utildeacute', uni=0x1E79, hex='1E79', c='ṹ', base='u', accents=['tildeacutecmb'], srcName='uni1E79', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1044)
GDS['utildebelow'] = GD(name='utildebelow', uni=0x1E75, hex='1E75', c='ṵ', base='u', accents=['tildebelowcmb'], srcName='uni1E75', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1040)

GDS['usuperior'] = GD(name='usuperior', uni=0x1D58, hex='1D58', c='ᵘ', l2r='nsuperior', r2l='nsuperior', srcName='uni1D58', isMod=True)
GDS['uinferior'] = GD(name='uinferior', l='usuperior', r='usuperior', base='usuperior', isMod=True)

# v

GDS['vdotbelow'] = GD(name='vdotbelow', uni=0x1E7F, hex='1E7F', c='ṿ', base='v', accents=['dotbelowcmb'], srcName='uni1E7F', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1050)
GDS['verticallineabovecmb'] = GD(name='verticallineabovecmb', uni=0x030D, hex='030D', c='̍', w=0, base='verticallinemod', isLower=True, anchors=['_top', 'top'])
GDS['verticallinebelowcmb'] = GD(name='verticallinebelowcmb', uni=0x0329, hex='0329', c='̩', w=0, base='verticallinemod', isLower=True, anchors=['_bottom', 'bottom'])
GDS['vhook'] = GD(name='vhook', uni=0x028B, hex='028B', c='ʋ', isLower=True)
GDS['vtilde'] = GD(name='vtilde', uni=0x1E7D, hex='1E7D', c='ṽ', l='v', r='v', base='v', accents=['tildecmb'], srcName='uni1E7D', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1048)

GDS['vsuperior'] = GD(name='vsuperior', uni=0x1D5B, hex='1D5B', c='ᵛ', l2r='vsuperior', srcName='uni1D5B', isMod=True, gid=918)
GDS['vinferior'] = GD(name='vinferior', l='vsuperior', r='vsuperior', base='vsuperior', isMod=True, gid=918)
GDS['verticallinesuperior'] = GD(name='verticallinesuperior', uni=0x02C8, hex='02C8', c='ˈ', w=0, isMod=True)
GDS['verticallineinferior'] = GD(name='verticallineinferior', w=0, isMod=True)

# w

GDS['wdotaccent'] = GD(name='wdotaccent', uni=0x1E87, hex='1E87', c='ẇ', l='w', r='w', base='w', accents=['dotaccentcmb'], srcName='uni1E87', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1058)
GDS['whook'] = GD(name='whook', uni=0x2C73, hex='2C73', c='ⱳ', isLower=True)
GDS['wring'] = GD(name='wring', uni=0x1E98, hex='1E98', c='ẘ', l='w', r='w', base='w', accents=['ringcmb'], srcName='uni1E98', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1075)

GDS['wsuperior'] = GD(name='wsuperior', uni=0x02B7, hex='02B7', c='ʷ', l='vmod', r='vmod', isMod=True)
GDS['winferior'] = GD(name='winferior', l='wsuperior', r='wsuperior', base='wsuperior', isMod=True)

# x

GDS['xdotaccent'] = GD(name='xdotaccent', uni=0x1E8B, hex='1E8B', c='ẋ', l='x', r='x', base='x', accents=['dotaccentcmb'], srcName='uni1E8B', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1062)

GDS['xsuperior'] = GD(name='xsuperior', uni=0x02E3, hex='02E3', c='ˣ', l2r='xsuperior', isMod=True)
GDS['xinferior'] = GD(name='xinferior', uni=0x2093, hex='2093', c='ₓ', l='xsuperior', r='xsuperior', base='xsuperior', isLower=True)

# y

GDS['yogh'] = GD(name='yogh', uni=0x021D, hex='021D', c='ȝ', l='three', r='three', isLower=True)
GDS['yring'] = GD(name='yring', uni=0x1E99, hex='1E99', c='ẙ', l='y', r='y', base='y', accents=['ringcmb'], srcName='uni1E99', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1076)
GDS['ystroke'] = GD(name='ystroke', uni=0x024F, hex='024F', c='ɏ', l='hyphen', r='hyphen', base='y', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['yturned'] = GD(name='yturned', uni=0x028E, hex='028E', c='ʎ', w='y', r2l='y', isLower=True)

GDS['ysuperior'] = GD(name='ysuperior', uni=0x02B8, hex='02B8', c='ʸ', isMod=True)
GDS['yinferior'] = GD(name='yinferior', l='ysuperior', r='ysuperior', base='ysuperior', isMod=True)

# z

GDS['zcircumflex'] = GD(name='zcircumflex', uni=0x1E91, hex='1E91', c='ẑ', l='z', r='z', base='z', accents=['circumflexcmb'], srcName='uni1E91', isLower=True, anchors=['bottom', 'middle', 'top'], gid=1068)
GDS['zstroke'] = GD(name='zstroke', uni=0x01B6, hex='01B6', c='ƶ', l='z', r='z', srcName='uni01B6', isLower=True, gid=375)

GDS['zsuperior'] = GD(name='zsuperior', uni=0x1DBB, hex='1DBB', c='ᶻ', l2r='zsuperior', isMod=True)
GDS['zinferior'] = GD(name='zinferior', l='zsuperior', r='zsuperior', base='zsuperior', isMod=True)

# Accents

GDS['dotaccentmacroncmb'] = GD(name='dotaccentmacroncmb', w=0, anchors=['top', '_top'])
GDS['tildedieresiscmb'] = GD(name='tildedieresiscmb', w=0, anchors=['top', '_top'])
GDS['tildeacutecmb'] = GD(name='tildeacutecmb', w=0, base='tildecmb', accents=['acutecmb'], anchors=['top', '_top'])
GDS['tildemacroncmb'] = GD(name='tildemacroncmb', w=0, base='tildecmb', accents=['macroncmb'], anchors=['top', '_top'])
GDS['tildemacroncmb'] = GD(name='tildemacroncmb', w=0, base='tildecmb', accents=['macroncmb'], anchors=['top', '_top'])
GDS['tildebelowcmb'] = GD(name='tildebelowcmb', w=0, base='tildecmb', anchors=['bottom', '_bottom'])
GDS['macrondieresiscmb'] = GD(name='macrondieresiscmb', w=0, base='macroncmb', accents=['dieresiscmb'], anchors=['top', '_top'])
GDS['macrondieresiscmb'] = GD(name='macrondieresiscmb', w=0, base='macroncmb', accents=['dieresiscmb'], anchors=['top', '_top'])
GDS['acutedotaccentcmb'] = GD(name='acutedotaccentcmb', w=0, base='acutecmb', accents=['dotaccentcmb'], anchors=['top', '_top'])
GDS['carondotaccentcmb'] = GD(name='carondotaccentcmb', w=0, base='caroncmb', accents=['dotaccentcmb'], anchors=['top', '_top'])
GDS['slashlongcmb'] = GD(name='slashlongcmb', w=0, anchors=['_middle'])
GDS['dotmiddlecmb'] = GD(name='dotmiddlecmb', w=0, anchors=['_middle'])
GDS['strokecmb'] = GD(name='strokecmb', w=0, anchors=['_middle'])
GDS['invertedbrevecmb'] = GD(name='invertedbrevecmb', w=0, anchors=['_middle'])
GDS['diagonalstrokecmb'] = GD(name='diagonalstrokecmb', w=0, anchors=['_middle'])
GDS['ringacutecmb'] = GD(name='ringacutecmb', w=0, base='ringcmb', accents=['acutecmb'], anchors=['_top'])
GDS['macronbelowcmb'] = GD(name='macronbelowcmb', uni=0x0331, hex='0331', c='̱', w=0, base='macroncmb', isLower=True, anchors=['bottom', '_bottom'], comment='COMBINING MACRON BELOW')
GDS['dblgravecomb'] = GD(name='dblgravecmb', uni=0x030F, hex='030F', c='̏', w=0, isLower=True, base='gravecmb', accents=['gravecmb'], anchors=['top', '_top'])


if __name__ == '__main__':
    for gName, gd in GDS.items():
        #print('---', gd)
        if gd.base and gd.base not in GDS:
            print('##### Missing base', gName, gd.base)
        for aName in gd.accents:
            if aName not in GDS:
                print('#### Missing accent', gName, aName)

