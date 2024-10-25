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

from assistantLib.assistantModules.glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_ etc.
from assistantLib.assistantModules.glyphsets.Latin_M_set import LATIN_M_SET

LATIN_L_SET_NAME = 'Latin L'

# The "c" attribtes are redundant, if the @uni or @hex atre defined, but they offer easy searching in the source by char.

LATIN_L_SET = GDS = deepcopy(LATIN_M_SET)

# Latin L unicodes
# Make this into these codes:
# GDS['aacute.alt'] = GD(name='aacute.alt', base='a.alt', accents=('acutecmb'))
#
# 0x0200 0x01DE 0x0226 0x01E0 0x0202 0x2C6D 0x01FA 0x1E00 0x023A 0x2C6F 0x01FC 0x1E02 0xA7B4 0x1E06 
# 0x0243 0x1E08 0xA7B3 0x0187 0x023B 0x01F1 0x01C4 0x0189 0x1E10 0x1E12 0x1E0A 0x01F2 0x01C5 0x0228 
# 0x1E1C 0x1E18 0x0204 0x0206 0x1E16 0x1E14 0x01A9 0x0246 0x1E1A 0x01B7 0x01EE 0x01B8 0xA798 0x1E1E 
# 0x0191 0x01F4 0x0193 0x0241 0xA7AC 0x01E4 0x021C 0x021E 0x1E22 0xA726 0xA7AA 0xA78D 0x0132 0x0208 
# 0x1E2E 0x020A 0x0196 0x1E2C 0xA7AE 0xA7B2 0x0248 0x1E30 0x01E8 0xA740 0x01C7 0x023D 0xA7AD 0x1E3C 
# 0x013F 0x2C60 0x2C62 0x01C8 0x1E3E 0x2C6E 0x019C 0x01CA 0x1E4A 0x01F8 0x01CB 0x0220 0x019F 0x020C 
# 0x022A 0x022E 0x0230 0x020E 0x1E52 0x1E50 0xA7B6 0x01EA 0x01EC 0x01FE 0x1E4C 0x1E4E 0x022C 0x0222 
# 0x1E54 0x01A4 0x2C63 0x024A 0x0210 0x0212 0x024C 0x2C64 0x1E64 0xA78B 0x1E66 0x1E60 0x1E68 0xA7A8 
# 0x0166 0x1E70 0x023E 0x1E6A 0x01AC 0x01AE 0x0244 0x1E76 0x0214 0x1E72 0x0216 0x1E7A 0x01B1 0x1E78 
# 0x1E74 0xA7B8 0x0194 0x1E7E 0x01B2 0x1E7C 0x1E86 0x2C72 0x1E8A 0x024E 0x1E90 0x01B5 0x0392 0x0395 
# 0x0398 0x039B 0x03A9 0x0201 0x01DF 0x0227 0x01E1 0x0203 0x0251 0x1E9A 0x01FB 0x1E01 0x2C65 0x0250 
# 0x01FD 0x1E03 0xA7B5 0x0298 0x1E07 0x0180 0x1E09 0xAB53 0x0188 0x2184 0x023C 0x0238 0x1E11 0x1E13 
# 0x1E0B 0x0256 0x01F3 0x01C6 0x0229 0x1E1D 0x1E19 0x0205 0x0207 0x1E17 0x1E15 0x0283 0x01AA 0x0247 
# 0x1E1B 0x0292 0x01EF 0x01B9 0xA799 0x1E1F 0x0192 0x01F5 0x0263 0x0260 0x0294 0x0295 0x0242 0x0261 
# 0x01E5 0x021D 0x021F 0x1E23 0xA727 0x0267 0x0266 0x0265 0x0209 0x1E2F 0x020B 0x0133 0x0269 0x1E2D 
# 0x026A 0x01F0 0x029D 0x025F 0x0284 0x0249 0x1E31 0x01E9 0xA741 0x0138 0x019B 0x019A 0x026C 0x1E3D 
# 0x0140 0x2C61 0x026B 0x01C9 0x1E3F 0x0271 0x026F 0x0149 0x1E4B 0x01F9 0x01CC 0x019E 0x0275 0x020D 
# 0x022B 0x022F 0x0231 0x020F 0x1E53 0x1E51 0xA7B7 0x01EB 0x01ED 0x01FF 0x1E4D 0x1E4F 0x022D 0x0223 
# 0x1E55 0x0278 0x01A5 0x1D7D 0x024B 0x0239 0x0264 0x0211 0x027D 0x0213 0x024D 0x1E65 0xA78C 0x1E67 
# 0x1E61 0x1E69 0xA7A9 0x017F 0x1E9B 0x0167 0x1E71 0x2C66 0x1E97 0x1E6B 0x02A7 0x01AD 0x0288 0x0289 
# 0x1E77 0x0215 0x1E73 0x0217 0x1E7B 0x028A 0x1E79 0x1E75 0xA7B9 0x1E7F 0x028B 0x1E7D 0x1E87 0x2C73 
# 0x1E98 0x1E8B 0x1E99 0x024F 0x028E 0x1E91 0x01B6 0x03B2 0x03B5 0x03B8 0x03BB 0x03C9 0x01C2 0x01C0 
# 0x01C1 0x01C3 0x2090 0x2091 0x02B1 0x02B0 0x2071 0x02B2 0x02E1 0x207F 0x2092 0x02B3 0x2094 0x02E2 
# 0x02B7 0x2093 0x02E3 0x02B8 0x2095 0x2096 0x2097 0x2098 0x2099 0x209A 0x209B 0x1DBF 0x209C 0x1D58 
# 0x1D5B 0x1DBB 0x02C0 0x02C1 0x02B9 0x02C8 0xA789 0x02EE 0x02D7 0xA78A 0x1DC7 0x1DC6 0x1DC5 0x1DC4 
# 0x030D 0x030F 0x0311 0x0313 0x0315 0x0320 0x0324 0x0325 0x0329 0x032D 0x032F 0x0330 0x0332 0x035C 
# 0x035D 0x0361 0x1DCA 0x0334 0x0358 0x02CA 0x02CB

