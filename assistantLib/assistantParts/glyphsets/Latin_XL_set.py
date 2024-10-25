# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_XL_set.py
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
#    Latin XL
#    Latin XL fills up Adobe Latin 5, including characters for IPA and APA. I don’t know if this makes sense.
#
#    Latin S + Latin M + Latin L + Latin XL
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
#    ⱰꞫꞰꞱɒʙᴅɢʛʜᵻʟɴɶʀʁᵾʏᶐᶏʭʬᵬᶀɕʗʤᶑᵭᶁʣʥʚᶓɜɞɝᶔᶒɘʆᶋᶘʅɚʓᶚʩᵮᶂʖʡʢᶃʮʯᵼᶄʞɮɭᶅꞎʪʫɰᵯᶆɳᵰᶇɷᶗᵱᶈʠɾᵳɿɻɼɺᵲᶉɹᶕʂᵴᶊ
#    ʨᵵʦʇᶙᶌⱱʍᶍʑᵶᶎʐʶᵅᶛᶲʵʴᵞᵠᶦᶫᶰᵄᵆᶱᵝᶝᵡᶜᵋᶟᵑᶴᶞᶾᶠᶣᶤᶨᶡᵏᶩᵚᶬᶭᵐᶮᶯᵓꜜꜝꜛᵊᶢᶳᶶᶷᶹᶺᶽᶼꟹ ‎ ‏‖‼‾‿‗‛‟
#    ˅˂˃˄˹˻˟˕˺˼˯˱˿˲˳˷˰˶˵˴˾˖˸˞˓˒˽˥˩˦˨˧˭˔ˤ◌� ͣ ͨ ͩ ͤ ͪ ͥ ͫ ͦ ͬ ͭ ͧ ͮ ͯ ̓ ̈́ ͅ ̅ ̎ ̔ ̖ ̗ ̘ ̙ ̚ ̜ ̝ ̞ ̟ ̡ ̢ ̪ ̫ ̬ ̳
#    ̶ ̷ ̸ ̹ ̺ ̻ ̼ ̽ ̾ ̿ ̀ ́ ͆ ͇ ͈ ͉ ͊ ͋ ͌ ͍ ͎ ͐ ͑ ͒ ͓ ͔ ͕ ͖ ͗ ͙ ͚ ͛ ͞ ͟ ͠ ͢ ᷉ ᷈ˉ˪˫ˏˑːʽʺˎˍˌⱾⱿȿɀ
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
from assistantLib.assistantModules.glyphsets.Latin_L_set import LATIN_L_SET

LATIN_XL_SET_NAME = 'Latin XL'

# The "c" attribtes are redundant, if the @uni or @hex atre defined, but they offer easy searching in the source by char.

LATIN_XL_SET = GDS = deepcopy(LATIN_L_SET)

# Latin L unicodes
# Make this into these codes:
# GDS['aacute.alt'] = GD(name='aacute.alt', base='a.alt', accents=('acutecmb'))
#
# 0x2C70 0xA7AB 0xA7B0 0xA7B1 0x0299 0x1D05 0x0262 0x029B 0x029C 0x1D7B 0x029F 0x0274 0x0276 0x0280 
# 0x0281 0x1D7E 0x028F 0x1D90 0x1D8F 0x02AD 0x02AC 0x1D6C 0x1D80 0x0252 0x0255 0x0297 0x02A4 0x1D91 
# 0x1D6D 0x1D81 0x02A3 0x02A5 0x029A 0x1D93 0x025C 0x025E 0x025D 0x1D94 0x1D92 0x0258 0x0286 0x1D8B 
# 0x1D98 0x0285 0x025A 0x0293 0x1D9A 0x02A9 0x1D6E 0x1D82 0x0296 0x02A1 0x02A2 0x1D83 0x02AE 0x02AF 
# 0x1D7C 0x1D84 0x029E 0x026E 0x026D 0x1D85 0xA78E 0x02AA 0x02AB 0x0270 0x1D6F 0x1D86 0x0273 0x1D70 
# 0x1D87 0x0277 0x1D97 0x1D71 0x1D88 0x02A0 0x027E 0x1D73 0x027F 0x027B 0x027C 0x027A 0x1D72 0x1D89 
# 0x0279 0x1D95 0x0282 0x1D74 0x1D8A 0x02A8 0x1D75 0x02A6 0x0287 0x1D99 0x1D8C 0x2C71 0x028D 0x1D8D 
# 0x0291 0x1D76 0x1D8E 0x0290 0x02B6 0x1D45 0x1D9B 0x1DB2 0x02B5 0x02B4 0x1D5E 0x1D60 0x1DA6 0x1DAB 
# 0x1DB0 0x1D44 0x1D46 0x1DB1 0x1D5D 0x1D9D 0x1D61 0x1D9C 0x1D4B 0x1D9F 0x1D51 0x1DB4 0x1D9E 0x1DBE 
# 0x1DA0 0x1DA3 0x1DA4 0x1DA8 0x1DA1 0x1D4F 0x1DA9 0x1D5A 0x1DAC 0x1DAD 0x1D50 0x1DAE 0x1DAF 0x1D53 
# 0xA71C 0xA71D 0xA71B 0x1D4A 0x1DA2 0x1DB3 0x1DB6 0x1DB7 0x1DB9 0x1DBA 0x1DBD 0x1DBC 0xA7F9 0x200E 
# 0x200F 0x2016 0x203C 0x203E 0x203F 0x2017 0x201B 0x201F 0x02C5 0x02C2 0x02C3 0x02C4 0x02F9 0x02FB 
# 0x02DF 0x02D5 0x02FA 0x02FC 0x02EF 0x02F1 0x02FF 0x02F2 0x02F3 0x02F7 0x02F0 0x02F6 0x02F5 0x02F4 
# 0x02FE 0x02D6 0x02F8 0x02DE 0x02D3 0x02D2 0x02FD 0x02E5 0x02E9 0x02E6 0x02E8 0x02E7 0x02ED 0x02D4 
# 0x02E4 0x25CC 0xFFFD 0x0363 0x0368 0x0369 0x0364 0x036A 0x0365 0x036B 0x0366 0x036C 0x036D 0x0367 
# 0x036E 0x036F 0x0343 0x0344 0x0345 0x0305 0x030E 0x0314 0x0316 0x0317 0x0318 0x0319 0x031A 0x031C 
# 0x031D 0x031E 0x031F 0x0321 0x0322 0x032A 0x032B 0x032C 0x0333 0x0336 0x0337 0x0338 0x0339 0x033A 
# 0x033B 0x033C 0x033D 0x033E 0x033F 0x0340 0x0341 0x0346 0x0347 0x0348 0x0349 0x034A 0x034B 0x034C 
# 0x034D 0x034E 0x0350 0x0351 0x0352 0x0353 0x0354 0x0355 0x0356 0x0357 0x0359 0x035A 0x035B 0x035E 
# 0x035F 0x0360 0x0362 0x1DC9 0x1DC8 0x02C9 0x02EA 0x02EB 0x02CF 0x02D1 0x02D0 0x02BD 0x02BA 0x02CE 
# 0x02CD 0x02CC 0x2C7E 0x2C7F 0x023F 0x0240


