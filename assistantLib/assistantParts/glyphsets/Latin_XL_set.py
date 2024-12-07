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

from assistantLib.assistantParts.glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_ etc.
from assistantLib.assistantParts.glyphsets.Latin_L_set import LATIN_L_SET

LATIN_XL_SET_NAME = 'Latin XL'

# The "c" attribtes are redundant, if the @uni or @hex atre defined, but they offer easy searching in the source by char.

LATIN_XL_SET = GDS = deepcopy(LATIN_L_SET)

# Latin XL unicodes
# Make this into these codes:
# GDS['aacute.alt'] = GD(name='aacute.alt', base='a.alt', accents=('acutecmb'))
#
#    0x2C70, 0xA7AB, 0xA7B0, 0xA7B1, 0x0299, 0x1D05, 0x0262, 0x029B, 0x029C, 0x1D7B, 0x029F, 0x0274, 0x0276, 0x0280, 
#    0x0281, 0x1D7E, 0x028F, 0x1D90, 0x1D8F, 0x02AD, 0x02AC, 0x1D6C, 0x1D80, 0x0252, 0x0255, 0x0297, 0x02A4, 0x1D91, 
#    0x1D6D, 0x1D81, 0x02A3, 0x02A5, 0x029A, 0x1D93, 0x025C, 0x025E, 0x025D, 0x1D94, 0x1D92, 0x0258, 0x0286, 0x1D8B, 
#    0x1D98, 0x0285, 0x025A, 0x0293, 0x1D9A, 0x02A9, 0x1D6E, 0x1D82, 0x0296, 0x02A1, 0x02A2, 0x1D83, 0x02AE, 0x02AF, 
#    0x1D7C, 0x1D84, 0x029E, 0x026E, 0x026D, 0x1D85, 0xA78E, 0x02AA, 0x02AB, 0x0270, 0x1D6F, 0x1D86, 0x0273, 0x1D70, 
#    0x1D87, 0x0277, 0x1D97, 0x1D71, 0x1D88, 0x02A0, 0x027E, 0x1D73, 0x027F, 0x027B, 0x027C, 0x027A, 0x1D72, 0x1D89, 
#    0x0279, 0x1D95, 0x0282, 0x1D74, 0x1D8A, 0x02A8, 0x1D75, 0x02A6, 0x0287, 0x1D99, 0x1D8C, 0x2C71, 0x028D, 0x1D8D, 
#    0x0291, 0x1D76, 0x1D8E, 0x0290, 0x02B6, 0x1D45, 0x1D9B, 0x1DB2, 0x02B5, 0x02B4, 0x1D5E, 0x1D60, 0x1DA6, 0x1DAB, 
#    0x1DB0, 0x1D44, 0x1D46, 0x1DB1, 0x1D5D, 0x1D9D, 0x1D61, 0x1D9C, 0x1D4B, 0x1D9F, 0x1D51, 0x1DB4, 0x1D9E, 0x1DBE, 
#    0x1DA0, 0x1DA3, 0x1DA4, 0x1DA8, 0x1DA1, 0x1D4F, 0x1DA9, 0x1D5A, 0x1DAC, 0x1DAD, 0x1D50, 0x1DAE, 0x1DAF, 0x1D53, 
#    0xA71C, 0xA71D, 0xA71B, 0x1D4A, 0x1DA2, 0x1DB3, 0x1DB6, 0x1DB7, 0x1DB9, 0x1DBA, 0x1DBD, 0x1DBC, 0xA7F9, 0x200E, 
#    0x200F, 0x2016, 0x203C, 0x203E, 0x203F, 0x2017, 0x201B, 0x201F, 0x02C5, 0x02C2, 0x02C3, 0x02C4, 0x02F9, 0x02FB, 
#    0x02DF, 0x02D5, 0x02FA, 0x02FC, 0x02EF, 0x02F1, 0x02FF, 0x02F2, 0x02F3, 0x02F7, 0x02F0, 0x02F6, 0x02F5, 0x02F4, 
#    0x02FE, 0x02D6, 0x02F8, 0x02DE, 0x02D3, 0x02D2, 0x02FD, 0x02E5, 0x02E9, 0x02E6, 0x02E8, 0x02E7, 0x02ED, 0x02D4, 
#    0x02E4, 0x25CC, 0xFFFD, 0x0363, 0x0368, 0x0369, 0x0364, 0x036A, 0x0365, 0x036B, 0x0366, 0x036C, 0x036D, 0x0367, 
#    0x036E, 0x036F, 0x0343, 0x0344, 0x0345, 0x0305, 0x030E, 0x0314, 0x0316, 0x0317, 0x0318, 0x0319, 0x031A, 0x031C, 
#    0x031D, 0x031E, 0x031F, 0x0321, 0x0322, 0x032A, 0x032B, 0x032C, 0x0333, 0x0336, 0x0337, 0x0338, 0x0339, 0x033A, 
#    0x033B, 0x033C, 0x033D, 0x033E, 0x033F, 0x0340, 0x0341, 0x0346, 0x0347, 0x0348, 0x0349, 0x034A, 0x034B, 0x034C, 
#    0x034D, 0x034E, 0x0350, 0x0351, 0x0352, 0x0353, 0x0354, 0x0355, 0x0356, 0x0357, 0x0359, 0x035A, 0x035B, 0x035E, 
#    0x035F, 0x0360, 0x0362, 0x1DC9, 0x1DC8, 0x02C9, 0x02EA, 0x02EB, 0x02CF, 0x02D1, 0x02D0, 0x02BD, 0x02BA, 0x02CE, 
#    0x02CD, 0x02CC, 0x2C7E, 0x2C7F, 0x023F, 0x0240

#   A

GDS['Alphaturned-latin'] = GD(name='Alphaturned-latin', uni=0x2C70, hex='2C70', c='Ɒ', r='O')

# B

GDS['Bsmall'] = GD(name='Bsmall', uni=0x0299, hex='0299', c='ʙ', r='B', isSc=True, comment='B small')

# D

GDS['Dsmall'] = GD(name='Dsmall', uni=0x1D05, hex='1D05', c='ᴅ', l='D', r='D', isSc=True)

# E

GDS['EreversedOpen'] = GD(name='EreversedOpen', uni=0xA7AB, hex='A7AB', c='Ɜ', anchors=['top'])

# G

GDS['Gsmall'] = GD(name='Gsmall', uni=0x0262, hex='0262', c='ɢ', l='O', r='G', isSc=True)
GDS['Gsmallhook'] = GD(name='Gsmallhook', uni=0x029B, hex='029B', c='ʛ', l='Gsmall', w='Gsmall')

# H

GDS['Hsmall'] = GD(name='Hsmall', uni=0x029C, hex='029C', c='ʜ', isSc=True)

# I

GDS['Ismallsuperior'] = GD(name='Ismallsuperior', uni=0x1DA6, hex='1DA6', c='ᶦ', l='48', r=GD.CAT_MOD_MIN_MARGIN)

# K

GDS['Kturned'] = GD(name='Kturned', uni=0xA7B0, hex='A7B0', c='Ʞ', r2l='K')

# L

GDS['Lsmall'] = GD(name='Lsmall', uni=0x029F, hex='029F', c='ʟ', l='Hsmall', r='L', isSc=True)
GDS['Lsmallsuperior'] = GD(name='Lsmallsuperior', uni=0x1DAB, hex='1DAB', c='ᶫ', l='Hsmall', r='Lsmall')

# N

GDS['Nsmall'] = GD(name='Nsmall', uni=0x0274, hex='0274', c='ɴ', isSc=True)
GDS['Nsmallsuperior'] = GD(name='Nsmallsuperior', uni=0x1DB0, hex='1DB0', c='ᶰ', l='Hsuperior', r='Hsuperior')

# O

GDS['OEsmall'] = GD(name='OEsmall', uni=0x0276, hex='0276', c='ɶ', r='Esmall', isSc=True)

# R

GDS['Rsmall'] = GD(name='Rsmall', uni=0x0280, hex='0280', c='ʀ', r='R', isSc=True)
GDS['Rsmallinverted'] = GD(name='Rsmallinverted', uni=0x0281, hex='0281', c='ʁ', l='Rsuperior', r='Rsuperior')
GDS['Rsmallinvertedsuperior'] = GD(name='Rsmallinvertedsuperior', uni=0x02B6, hex='02B6', c='ʶ', l='Rsuperior', r='Rsuperior')

# S

GDS['Sswashtail'] = GD(name='Sswashtail', uni=0x2C7E, hex='2C7E', c='Ȿ', l='S', w='S')

# T

GDS['Tturned'] = GD(name='Tturned', uni=0xA7B1, hex='A7B1', c='Ʇ', l='T', r='T')

# Y

GDS['Ysmall'] = GD(name='Ysmall', uni=0x028F, hex='028F', c='ʏ', l='v', r='v', isSc=True)

# Z

GDS['Zswashtail'] = GD(name='Zswashtail', uni=0x2C7F, hex='2C7F', c='Ɀ', l='Z', w='Z')

# a

GDS['aTurnedsuperior'] = GD(name='aTurnedsuperior', uni=0x1D44, hex='1D44', c='ᵄ', l2r='asuperior', r2l='asuperior')
GDS['acmb'] = GD(name='acmb', uni=0x0363, hex='0363', c='ͣ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['acutebelowcmb'] = GD(name='acutebelowcmb', uni=0x0317, hex='0317', c='̗', w=0, base='acutecmb', isLower=True, anchors=['_bottom', 'bottom'])
GDS['acutegraveacutecmb'] = GD(name='acutegraveacutecmb', uni=0x1DC9, hex='1DC9', c='᷉', w=0, isLower=True, anchors=['_top', 'top'])
GDS['acutelowsuperior'] = GD(name='acutelowsuperior', uni=0x02CF, hex='02CF', c='ˏ', base='acutecmb', isLower=True)
GDS['acutetonecmb'] = GD(name='acutetonecmb', uni=0x0341, hex='0341', c='́', w=0, base='acutecmb', isLower=True, anchors=['_top', 'top'])
GDS['aeTurnedsuperior'] = GD(name='aeTurnedsuperior', uni=0x1D46, hex='1D46', c='ᵆ', l2r='asuperior', r2l='esuperior')
GDS['almostequaltoabovecmb'] = GD(name='almostequaltoabovecmb', uni=0x034C, hex='034C', c='͌', w=0, isLower=True, anchors=['_top', 'top'])
GDS['alphasuperior-latin'] = GD(name='alphasuperior-latin', uni=0x1D45, hex='1D45', c='ᵅ', l='osuperior', l2r='nsuperior')
GDS['alpharetroflexhook'] = GD(name='alpharetroflexhook', uni=0x1D90, hex='1D90', c='ᶐ', r='off', base='alpha-latin', isLower=True)
GDS['alphaturned-latin'] = GD(name='alphaturned-latin', uni=0x0252, hex='0252', c='ɒ', l2r='alpha-latin', r2l='alpha-latin', isLower=True)
GDS['alphaturnedsuperior-latin'] = GD(name='alphaturnedsuperior-latin', uni=0x1D9B, hex='1D9B', c='ᶛ', l2r='alphasuperior-latin', r2l='alphasuperior-latin')
GDS['aretroflexhook'] = GD(name='aretroflexhook', uni=0x1D8F, hex='1D8F', c='ᶏ', l='a', w='a', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['asteriskbelowcmb'] = GD(name='asteriskbelowcmb', uni=0x0359, hex='0359', c='͙', w=0, isLower=True, anchors=['_bottom', 'bottom'])

GDS['arrowdoublerightbelowcmb'] = GD(name='arrowdoublerightbelowcmb', uni=0x0362, hex='0362', c='͢', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['arrowheaddownsuperior'] = GD(name='arrowheaddownsuperior', uni=0x02C5, hex='02C5', c='˅', l='48', r='48', isLower=True)
GDS['arrowheadleftbelowcmb'] = GD(name='arrowheadleftbelowcmb', uni=0x0354, hex='0354', c='͔', w=0, base='lowleftarrowheadsuperior', isLower=True, anchors=['_bottom', 'bottom'])
GDS['arrowheadleftsuperior'] = GD(name='arrowheadleftsuperior', uni=0x02C2, hex='02C2', c='˂', l='48', r='48', isLower=True)
GDS['arrowheadrightabovecmb'] = GD(name='arrowheadrightabovecmb', uni=0x0350, hex='0350', c='͐', w=0, base='lowrightarrowheadsuperior', isLower=True, anchors=['_top', 'top'])
GDS['arrowheadrightbelowcmb'] = GD(name='arrowheadrightbelowcmb', uni=0x0355, hex='0355', c='͕', w=0, base='lowrightarrowheadsuperior', isLower=True, anchors=['_bottom', 'bottom'])
GDS['arrowheadrightheadupbelowcmb'] = GD(name='arrowheadrightheadupbelowcmb', uni=0x0356, hex='0356', c='͖', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['arrowheadrightsuperior'] = GD(name='arrowheadrightsuperior', uni=0x02C3, hex='02C3', c='˃', l='48', r='48', isLower=True)
GDS['arrowheadupsuperior'] = GD(name='arrowheadupsuperior', uni=0x02C4, hex='02C4', c='˄', l='48', r='48', isLower=True)
GDS['arrowleftrightbelowcmb'] = GD(name='arrowleftrightbelowcmb', uni=0x034D, hex='034D', c='͍', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['arrowupbelowcmb'] = GD(name='arrowupbelowcmb', uni=0x034E, hex='034E', c='͎', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['arrowupsuperior'] = GD(name='arrowupsuperior', uni=0xA71B, hex='A71B', c='ꜛ', comment='superior Letter Raised Up Arrow')
GDS['arrowdownsuperior'] = GD(name='arrowdownsuperior', uni=0xA71C, hex='A71C', c='ꜜ', comment='superior Letter Raised Down Arrow')

# b

GDS['barredsuperior'] = GD(name='barredsuperior', uni=0x1DB1, hex='1DB1', c='ᶱ', l='osuperior', r='osuperior')
GDS['beginhightonesuperior'] = GD(name='beginhightonesuperior', uni=0x02F9, hex='02F9', c='˹', l='48', r='48', isLower=True)
GDS['beginlowtonesuperior'] = GD(name='beginlowtonesuperior', uni=0x02FB, hex='02FB', c='˻', l='48', r='48', isLower=True)
GDS['betasuperior'] = GD(name='betasuperior', uni=0x1D5D, hex='1D5D', c='ᵝ', gid=919)
GDS['bidentalpercussive'] = GD(name='bidentalpercussive', uni=0x02AD, hex='02AD', c='ʭ', l='H', r='H')
GDS['bilabialpercussive'] = GD(name='bilabialpercussive', uni=0x02AC, hex='02AC', c='ʬ')
GDS['bmiddletilde'] = GD(name='bmiddletilde', uni=0x1D6C, hex='1D6C', c='ᵬ', l='asciitilde', base='b', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['bpalatalhook'] = GD(name='bpalatalhook', uni=0x1D80, hex='1D80', c='ᶀ', l='b', r='b', base='b', accents=['bpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['bridgebelowcmb'] = GD(name='bridgebelowcmb', uni=0x032A, hex='032A', c='̪', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['bridgeinvertedbelowcmb'] = GD(name='bridgeinvertedbelowcmb', uni=0x033A, hex='033A', c='̺', l='center', w=0, base='shelfsuperior', isLower=True, anchors=['_bottom', 'bottom'])

# c

GDS['caronbelowcmb'] = GD(name='caronbelowcmb', uni=0x032C, hex='032C', c='̬', w=0, base='caroncmb', isLower=True, anchors=['_bottom', 'bottom'])
GDS['ccmb'] = GD(name='ccmb', uni=0x0368, hex='0368', c='ͨ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['ccurl'] = GD(name='ccurl', uni=0x0255, hex='0255', c='ɕ', isLower=True, comment='The Unicode glyph 0255 (U+0255) is the code point for the Latin small letter c with curl, which is used in the International Phonetic Alphabet (IPA) to represent a voiceless alveolar fricative sound. This sound is similar to the "sh" sound in English words like "ship" and "nation", but is produced with the tongue touching the alveolar ridge (the hard ridge behind the upper front teeth) rather than the roof of the mouth. The IPA is used by linguists, language learners, and speech therapists to accurately transcribe and describe the sounds of human languages. The use of Unicode characters to represent IPA symbols allows for consistent representation and sharing of transcriptions across different computer systems and platforms. So if you"re working with the IPA, you might use the glyph 0255 to represent the voiceless alveolar fricative sound in your transcriptions.')
GDS['ccurlsuperior'] = GD(name='ccurlsuperior', uni=0x1D9D, hex='1D9D', c='ᶝ', l='osuperior', r='osuperior', comment='The glyph unicode 1d9d (ᶝ) is a phonetic symbol used in the International Phonetic Alphabet (IPA) to represent the voiced velar fricative sound. It is typically used in linguistic research, language teaching and learning, and in the production of phonetic transcriptions of speech. The symbol helps to accurately represent the pronunciation of words and sounds across different languages and dialects, allowing for better communication and understanding between speakers of different languages.')
GDS['chisuperior'] = GD(name='chisuperior', uni=0x1D61, hex='1D61', c='ᵡ', l='xsuperior', r='xsuperior', gid=921)
GDS['csuperior'] = GD(name='csuperior', uni=0x1D9C, hex='1D9C', c='ᶜ', l='osuperior')
GDS['colontriangularhalfsuperior'] = GD(name='colontriangularhalfsuperior', uni=0x02D1, hex='02D1', c='ˑ', isLower=True)
GDS['colontriangularsuperior'] = GD(name='colontriangularsuperior', uni=0x02D0, hex='02D0', c='ː', isLower=True)
GDS['commareversedabovecmb'] = GD(name='commareversedabovecmb', uni=0x0314, hex='0314', c='̔', w=0, base='dasia', isLower=True, anchors=['_top', 'top'])
GDS['commareversedsuperior'] = GD(name='commareversedsuperior', uni=0x02BD, hex='02BD', c='ʽ')
GDS['crossaccentsuperior'] = GD(name='crossaccentsuperior', uni=0x02DF, hex='02DF', c='˟', l='48', r='48', isLower=True)
GDS['cstretched'] = GD(name='cstretched', uni=0x0297, hex='0297', c='ʗ', l='c', r='c', isLower=True)

# d

GDS['dblarchinvertedbelowcmb'] = GD(name='dblarchinvertedbelowcmb', uni=0x032B, hex='032B', c='̫', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['dbllowlinecmb'] = GD(name='dbllowlinecmb', uni=0x0333, hex='0333', c='̳', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['dblmacronbelowcmb'] = GD(name='dblmacronbelowcmb', uni=0x035F, hex='035F', c='͟', w=0, isLower=True, anchors=['_bottom', 'bottom'], comment='COMBINING DOUBLE MACRON BELOW')
GDS['dbloverlinecmb'] = GD(name='dbloverlinecmb', uni=0x033F, hex='033F', c='̿', w=0, base='underscoredbl', isLower=True, anchors=['_top', 'top'])
GDS['dblverticalbar'] = GD(name='dblverticalbar', uni=0x2016, hex='2016', c='‖', base='bar', accents=['bar'], isLower=True)
GDS['dblverticallineabovecmb'] = GD(name='dblverticallineabovecmb', uni=0x030E, hex='030E', c='̎', w=0, isLower=True, anchors=['_top', 'top'])
GDS['dcmb'] = GD(name='dcmb', uni=0x0369, hex='0369', c='ͩ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['dezh'] = GD(name='dezh', uni=0x02A4, hex='02A4', c='ʤ', l='d', r='three', isLower=True)
GDS['dhookandtail'] = GD(name='dhookandtail', uni=0x1D91, hex='1D91', c='ᶑ', l='a', r='aretroflexhook', isLower=True)
GDS['dialytikatonoscmb'] = GD(name='dialytikatonoscmb', uni=0x0344, hex='0344', c='̈́', w=0, base='dialytikaoxia', isLower=True, anchors=['_top', 'top'])
GDS['dmiddletilde'] = GD(name='dmiddletilde', uni=0x1D6D, hex='1D6D', c='ᵭ', r='asciitilde', base='d', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['dottedCircle'] = GD(name='dottedCircle', uni=0x25CC, hex='25CC', c='◌', isLower=True, anchors=['bottom', 'top'])
GDS['doublemacroncmb'] = GD(name='doublemacroncmb', uni=0x035E, hex='035E', c='͞', w=0, isLower=True, anchors=['_top', 'top'])
GDS['doubleringbelowcmb'] = GD(name='doubleringbelowcmb', uni=0x035A, hex='035A', c='͚', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['doubleverticallinebelowcmb'] = GD(name='doubleverticallinebelowcmb', uni=0x0348, hex='0348', c='͈', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['downtackbelowcmb'] = GD(name='downtackbelowcmb', uni=0x031E, hex='031E', c='̞', w=0, base='downtacksuperior', isLower=True, anchors=['_bottom', 'bottom'])
GDS['downtacksuperior'] = GD(name='downtacksuperior', uni=0x02D5, hex='02D5', c='˕', l='48', r='48', isLower=True)
GDS['dpalatalhook'] = GD(name='dpalatalhook', uni=0x1D81, hex='1D81', c='ᶁ', l='d', r='jdotless', base='d', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['dzaltone'] = GD(name='dzaltone', uni=0x02A3, hex='02A3', c='ʣ', l='d', r='z', isLower=True)
GDS['dzcurl'] = GD(name='dzcurl', uni=0x02A5, hex='02A5', c='ʥ', l='d', r='zcurl', isLower=True)
GDS['dasia'] = GD(name='dasia', uni=0x1FFE, hex='1FFE', c='῾', w=0, isLower=True, anchors=['top', '_top'], gid=1405)
GDS['dialytikaoxia'] = GD(name='dialytikaoxia', uni=0x1FEE, hex='1FEE', c='΅', w=0, isLower=True, anchors=['top', '_top'], gid=1392)

GDS['doubleprimesuperior'] = GD(name='doubleprimesuperior', uni=0x02BA, hex='02BA', c='ʺ', base='quotedblright', isLower=True)

# e

GDS['eReversedopensuperior'] = GD(name='eReversedopensuperior', uni=0x1D9F, hex='1D9F', c='ᶟ')
GDS['ecmb'] = GD(name='ecmb', uni=0x0364, hex='0364', c='ͤ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['endhightonesuperior'] = GD(name='endhightonesuperior', uni=0x02FA, hex='02FA', c='˺', l='48', r='48', isLower=True)
GDS['endlowtonesuperior'] = GD(name='endlowtonesuperior', uni=0x02FC, hex='02FC', c='˼', l='48', r='48', isLower=True)
GDS['engsuperior'] = GD(name='engsuperior', uni=0x1D51, hex='1D51', c='ᵑ', l='nsuperior', r='nsuperior')
GDS['eopenclosed'] = GD(name='eopenclosed', uni=0x029A, hex='029A', c='ʚ', l='o', isLower=True)
GDS['eopenretroflexhook'] = GD(name='eopenretroflexhook', uni=0x1D93, hex='1D93', c='ᶓ', w='epsilon', base='epsilon', isLower=True, anchors=['top'])
GDS['eopenreversed'] = GD(name='eopenreversed', uni=0x025C, hex='025C', c='ɜ', l='three', r='three', isLower=True)
GDS['eopenreversedclosed'] = GD(name='eopenreversedclosed', uni=0x025E, hex='025E', c='ɞ', r='three', isLower=True)
GDS['eopenreversedhook'] = GD(name='eopenreversedhook', uni=0x025D, hex='025D', c='ɝ', l='three', r='0', isLower=True)
GDS['eopenreversedretroflexhook'] = GD(name='eopenreversedretroflexhook', uni=0x1D94, hex='1D94', c='ᶔ', isLower=True, anchors=['top'])
GDS['equalbelowcmb'] = GD(name='equalbelowcmb', uni=0x0347, hex='0347', c='͇', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['eretroflexhook'] = GD(name='eretroflexhook', uni=0x1D92, hex='1D92', c='ᶒ', w='e', bl='e', base='e', accents=['retroflexhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ereversed'] = GD(name='ereversed', uni=0x0258, hex='0258', c='ɘ', l2r='e', r2l='e', isLower=True)
GDS['eshcurl'] = GD(name='eshcurl', uni=0x0286, hex='0286', c='ʆ', isLower=True)
GDS['eshsuperior'] = GD(name='eshsuperior', uni=0x1DB4, hex='1DB4', c='ᶴ')
GDS['eshpalatalhook'] = GD(name='eshpalatalhook', uni=0x1D8B, hex='1D8B', c='ᶋ', r='jdotless', base='esh', accents=['dpalatalhookcmb', 'gpalatalhookcmb'], isLower=True, anchors=['bottom'])
GDS['eshretroflexhook'] = GD(name='eshretroflexhook', uni=0x1D98, hex='1D98', c='ᶘ', isLower=True)
GDS['eshsquatreversed'] = GD(name='eshsquatreversed', uni=0x0285, hex='0285', c='ʅ', isLower=True)
GDS['ethsuperior'] = GD(name='ethsuperior', uni=0x1D9E, hex='1D9E', c='ᶞ', l='osuperior', r='osuperior')
GDS['exclamdouble'] = GD(name='exclamdouble', uni=0x203C, hex='203C', c='‼', l='exclam', r='exclam', base='exclam', accents=['exclam'], srcName='exclamdbl', isLower=True, gid=1427)
GDS['ezhcurl'] = GD(name='ezhcurl', uni=0x0293, hex='0293', c='ʓ', l='osuperior', r='0', isLower=True)
GDS['ezhsuperior'] = GD(name='ezhsuperior', uni=0x1DBE, hex='1DBE', c='ᶾ')
GDS['ezhretroflexhook'] = GD(name='ezhretroflexhook', uni=0x1D9A, hex='1D9A', c='ᶚ', r='o', r2l='c', isLower=True)
GDS['exclamationsuperior'] = GD(name='exclamationsuperior', uni=0xA71B, hex='A71B', c='ꜝ', comment='superior Letter Raised Exclamation Mark')

GDS['eOpensuperior'] = GD(name='eOpensuperior', uni=0x1D4B, hex='1D4B', c='ᵋ')

# f

GDS['fengdigraph'] = GD(name='fengdigraph', uni=0x02A9, hex='02A9', c='ʩ', isLower=True)
GDS['fermatacmb'] = GD(name='fermatacmb', uni=0x0352, hex='0352', c='͒', w=0, isLower=True, anchors=['_top', 'top'])
GDS['firsttonechinese'] = GD(name='firsttonechinese', uni=0x02C9, hex='02C9', c='ˉ', w=0, isLower=True, anchors=['_top', 'top'], gid=1643)
GDS['fmiddletilde'] = GD(name='fmiddletilde', uni=0x1D6E, hex='1D6E', c='ᵮ', base='f', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['fpalatalhook'] = GD(name='fpalatalhook', uni=0x1D82, hex='1D82', c='ᶂ', l='f', w='f', base='dpalatalhookcmb', anchors=['bottom', 'middle', 'top'])

GDS['fsuperior'] = GD(name='fsuperior', uni=0x1DA0, hex='1DA0', c='ᶠ')

# g

GDS['gbridgeabovecmb'] = GD(name='gbridgeabovecmb', uni=0x0346, hex='0346', c='͆', w=0, isLower=True, anchors=['_top', 'top'])
GDS['glottalstopinverted'] = GD(name='glottalstopinverted', uni=0x0296, hex='0296', c='ʖ', l='question', r='question')
GDS['glottalstopreversedsuperior'] = GD(name='glottalstopreversedsuperior', uni=0x02E4, hex='02E4', c='ˤ', base='glottalstopreversedsuperior')
GDS['glottalstopstroke'] = GD(name='glottalstopstroke', uni=0x02A1, hex='02A1', c='ʡ', l='question', r='question')
GDS['glottalstopstrokereversed'] = GD(name='glottalstopstrokereversed', uni=0x02A2, hex='02A2', c='ʢ', l2r='question', r2l='question')
GDS['gpalatalhook'] = GD(name='gpalatalhook', uni=0x1D83, hex='1D83', c='ᶃ', l='g', r='jdotless', base='g', accents=['dpalatalhookcmb', 'gpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['graveacutegravecmb'] = GD(name='graveacutegravecmb', uni=0x1DC8, hex='1DC8', c='᷈', w=0, isLower=True, anchors=['_top', 'top'])
GDS['gravebelowcmb'] = GD(name='gravebelowcmb', uni=0x0316, hex='0316', c='̖', w=0, base='gravecmb', isLower=True, anchors=['_bottom', 'bottom'])
GDS['gravelowsuperior'] = GD(name='gravelowsuperior', uni=0x02CE, hex='02CE', c='ˎ', base='gravecmb', isLower=True)
GDS['gravetonecmb'] = GD(name='gravetonecmb', uni=0x0340, hex='0340', c='̀', w=0, base='gravecmb', isLower=True, anchors=['_top', 'top'])

GDS['gammasuperior'] = GD(name='gammasuperior', uni=0x1D5E, hex='1D5E', c='ᵞ', gid=920)

# h

GDS['hcmb'] = GD(name='hcmb', uni=0x036A, hex='036A', c='ͪ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['homotheticabovecmb'] = GD(name='homotheticabovecmb', uni=0x034B, hex='034B', c='͋', w=0, isLower=True, anchors=['_top', 'top'])
GDS['hturnedfishhook'] = GD(name='hturnedfishhook', uni=0x02AE, hex='02AE', c='ʮ', isLower=True)
GDS['hturnedfishhookandtail'] = GD(name='hturnedfishhookandtail', uni=0x02AF, hex='02AF', c='ʯ', l='hturnedfishhook', l2r='hturnedfishhook', isLower=True)

GDS['hturnedsuperior'] = GD(name='hturnedsuperior', uni=0x1DA3, hex='1DA3', c='ᶣ')

# i

GDS['icmb'] = GD(name='icmb', uni=0x0365, hex='0365', c='ͥ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['idotlessstroke'] = GD(name='idotlessstroke', uni=0x1D7B, hex='1D7B', c='ᵻ', r='Esmall', r2l='Esmall', srcName='uni1D7B', isLower=True, gid=922)
GDS['iotastroke'] = GD(name='iotastroke', uni=0x1D7C, hex='1D7C', c='ᵼ', isLower=True, anchors=['top'])
GDS['istrokesuperior'] = GD(name='istrokesuperior', uni=0x1DA4, hex='1DA4', c='ᶤ', r2l='istrokesuperior')
GDS['jcrossedtailsuperior'] = GD(name='jcrossedtailsuperior', uni=0x1DA8, hex='1DA8', c='ᶨ')
GDS['jdotlessstrokesuperior'] = GD(name='jdotlessstrokesuperior', uni=0x1DA1, hex='1DA1', c='ᶡ', l2r='fsuperior]', r2l='fsuperior')

GDS['indepartingtonesuperior'] = GD(name='indepartingtonesuperior', uni=0x02EA, hex='02EA', c='˪', isLower=True)

# k

GDS['koroniscmb'] = GD(name='koroniscmb', uni=0x0343, hex='0343', c='̓', w=0, base='koronis', isLower=True, anchors=['_top', 'top'])
GDS['kpalatalhook'] = GD(name='kpalatalhook', uni=0x1D84, hex='1D84', c='ᶄ', r='jdotless', bl='k', base='k', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['kturned'] = GD(name='kturned', uni=0x029E, hex='029E', c='ʞ', l2r='k', r2l='k', isLower=True)

GDS['ksuperior'] = GD(name='ksuperior', uni=0x1D4F, hex='1D4F', c='ᵏ', l='hsuperior]', srcName='uni1D4F', gid=912)

# l

GDS['leftangleabovecmb'] = GD(name='leftangleabovecmb', uni=0x031A, hex='031A', c='̚', w=0, isLower=True, anchors=['_top', 'top'])
GDS['leftanglebelowcmb'] = GD(name='leftanglebelowcmb', uni=0x0349, hex='0349', c='͉', w=0, base='endhightonesu[erior]', isLower=True, anchors=['_bottom', 'bottom'])
GDS['lefthalfringabovecmb'] = GD(name='lefthalfringabovecmb', uni=0x0351, hex='0351', c='͑', w=0, isLower=True, anchors=['_top', 'top'])
GDS['lefttackbelowcmb'] = GD(name='lefttackbelowcmb', uni=0x0318, hex='0318', c='̘', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['lefttorightmark'] = GD(name='lefttorightmark', uni=0x200E, hex='200E', c='‎', w=0, isLower=True)
GDS['lezh'] = GD(name='lezh', uni=0x026E, hex='026E', c='ɮ', l='H', r='three', isLower=True)
GDS['lhookretroflex'] = GD(name='lhookretroflex', uni=0x026D, hex='026D', c='ɭ', l='l', w='l', isLower=True)
GDS['lowringsuperior]'] = GD(name='lowringsu[erior]', uni=0x02F3, hex='02F3', c='˳', l='48', r='48', base='ringcmb', isLower=True)
GDS['lowtildesu[erior]'] = GD(name='lowtildesuperior', uni=0x02F7, hex='02F7', c='˷', l='48', r='48', base='tildecmb', isLower=True)
GDS['lowuparrowheadsuperior]'] = GD(name='lowuparrowheadsuperior', uni=0x02F0, hex='02F0', c='˰', l='48', r='48', isLower=True)
GDS['lpalatalhook'] = GD(name='lpalatalhook', uni=0x1D85, hex='1D85', c='ᶅ', l='l', r='jdotless', base='l', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['lretroflexhookandbelt'] = GD(name='lretroflexhookandbelt', uni=0xA78E, hex='A78E', c='ꞎ', l='osuperior', r='t', isLower=True)
GDS['lretroflexhooksuperior'] = GD(name='lretroflexhooksuperior]', uni=0x1DA9, hex='1DA9', c='ᶩ')
GDS['lsdigraph'] = GD(name='lsdigraph', uni=0x02AA, hex='02AA', c='ʪ', l='l', r='s', isLower=True)
GDS['lzdigraph'] = GD(name='lzdigraph', uni=0x02AB, hex='02AB', c='ʫ', l='l', r='z', isLower=True)

GDS['lowdownarrowheadsuperior'] = GD(name='lowdownarrowheadsuperior', uni=0x02EF, hex='02EF', c='˯', l='48', r='48', isLower=True)
GDS['lowleftarrowheadsuperior'] = GD(name='lowleftarrowheadsuperior', uni=0x02F1, hex='02F1', c='˱', l='48', r='48', srcName='uni02F1', isLower=True, gid=485)
GDS['lowleftarrowsuperior'] = GD(name='lowleftarrowsuperior', uni=0x02FF, hex='02FF', c='˿', l='48', r='48', isLower=True)
GDS['lowrightarrowheadsuperior'] = GD(name='lowrightarrowheadsuperior', uni=0x02F2, hex='02F2', c='˲', l='48', r='48', srcName='uni02F2', isLower=True, gid=486)

# m

GDS['mcmb'] = GD(name='mcmb', uni=0x036B, hex='036B', c='ͫ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['mlonglegturned'] = GD(name='mlonglegturned', uni=0x0270, hex='0270', c='ɰ', isLower=True)
GDS['mmiddletilde'] = GD(name='mmiddletilde', uni=0x1D6F, hex='1D6F', c='ᵯ', l='asciitilde', r='asciitilde', base='m', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['mpalatalhook'] = GD(name='mpalatalhook', uni=0x1D86, hex='1D86', c='ᶆ', l='m', r='jdotless', base='m', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])

GDS['msuperior'] = GD(name='msuperior', uni=0x1D50, hex='1D50', c='ᵐ', l='nsuperior', r='nsuperior', srcName='uni1D50', gid=913)
GDS['mTurnedsuperior'] = GD(name='mTurnedsuperior', uni=0x1D5A, hex='1D5A', c='ᵚ', l2r='msuperior', r2l='msuperior')
GDS['macronlowsuperior'] = GD(name='macronlowsuperior', uni=0x02CD, hex='02CD', c='ˍ', isLower=True)
GDS['mhooksuperior'] = GD(name='mhooksuperior', uni=0x1DAC, hex='1DAC', c='ᶬ', l='engsuperior', r='nsuperior')
GDS['mlonglegturnedsuperior'] = GD(name='mlonglegturnedsuperior', uni=0x1DAD, hex='1DAD', c='ᶭ')
GDS['middledoubleacuteaccentsuperior'] = GD(name='middledoubleacuteaccentsuperior', uni=0x02F6, hex='02F6', c='˶', l='48', r='48', base='hungarumlautcmb', isLower=True)
GDS['middledoublegraveaccentsuperior'] = GD(name='middledoublegraveaccentsuperior', uni=0x02F5, hex='02F5', c='˵', l='48', r='48', base='dblgravecmb', isLower=True)
GDS['middlegraveaccentsuperior'] = GD(name='middlegraveaccentsuperior', uni=0x02F4, hex='02F4', c='˴', l='center', w='620.0', base='gravecmb', isLower=True)

# n

GDS['nhookretroflex'] = GD(name='nhookretroflex', uni=0x0273, hex='0273', c='ɳ', l='n', w='n', isLower=True)
GDS['nmiddletilde'] = GD(name='nmiddletilde', uni=0x1D70, hex='1D70', c='ᵰ', l='asciitilde', r='asciitilde', base='n', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['nottildeabovecmb'] = GD(name='nottildeabovecmb', uni=0x034A, hex='034A', c='͊', w=0, isLower=True, anchors=['_top', 'top'])
GDS['npalatalhook'] = GD(name='npalatalhook', uni=0x1D87, hex='1D87', c='ᶇ', l='n', r='jdotless', base='n', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['nretroflexhooksuperior'] = GD(name='nretroflexhooksuperior', uni=0x1DAF, hex='1DAF', c='ᶯ', l='nsuperior', w='nsuperior')

GDS['nlefthooksuperior'] = GD(name='nlefthooksuperior', uni=0x1DAE, hex='1DAE', c='ᶮ', r='nsuperior', w='nsuperior')

# o

GDS['ocmb'] = GD(name='ocmb', uni=0x0366, hex='0366', c='ͦ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['omegaclosed-latin'] = GD(name='omegaclosed-latin', uni=0x0277, hex='0277', c='ɷ', l='o', r='o', isLower=True)
GDS['oopenretroflexhook'] = GD(name='oopenretroflexhook', uni=0x1D97, hex='1D97', c='ᶗ', base='oopen', isLower=True, anchors=['top'])
GDS['overline'] = GD(name='overline', uni=0x203E, hex='203E', c='‾', srcName='radicalex', isLower=True, gid=1428, comment='‾ spacing overscore')

GDS['oOpensuperior'] = GD(name='oOpensuperior', uni=0x1D53, hex='1D53', c='ᵓ', r='osuperior', r2l='csuperior')
GDS['oesuperior'] = GD(name='oesuperior', uni=0xA7F9, hex='A7F9', c='ꟹ', l='osuperior', r='esuperior')
GDS['openshelfsuperior'] = GD(name='openshelfsuperior', uni=0x02FE, hex='02FE', c='˾', l='48', r='48')

GDS['overlinecmb'] = GD(name='overlinecmb', uni=0x0305, hex='0305', c='̅', l='center', w=0, base='overline', isLower=True, anchors=['_top', 'top'])

# p

GDS['palatalhookcmb'] = GD(name='palatalhookcmb', uni=0x0321, hex='0321', c='̡', w=0, srcName='uni0321', isLower=True, anchors=['_bottom', 'bottom'], gid=502)
GDS['phisuperior-latin'] = GD(name='phisuperior-latin', uni=0x1DB2, hex='1DB2', c='ᶲ', isLower=True)
GDS['plussuperior'] = GD(name='plussuperior', uni=0x02D6, hex='02D6', c='˖', l='48', r='48')
GDS['pmiddletilde'] = GD(name='pmiddletilde', uni=0x1D71, hex='1D71', c='ᵱ', bl='p', base='p', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ppalatalhook'] = GD(name='ppalatalhook', uni=0x1D88, hex='1D88', c='ᶈ', r='p', bl='p', base='p', accents=['bpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['prosgegrammeni'] = GD(name='prosgegrammeni', uni=0x1FBE, hex='1FBE', c='ι', w=0, isLower=True, anchors=['bottom', '_bottom'], gid=1348)

GDS['phisuperior'] = GD(name='phisuperior', uni=0x1D50, hex='1D50', c='ᵠ', comment='superior Letter Small Greek Phi')

GDS['plusbelowcmb'] = GD(name='plusbelowcmb', uni=0x031F, hex='031F', c='̟', w=0, anchors=['_bottom', 'bottom'])

# q

GDS['qhook'] = GD(name='qhook', uni=0x02A0, hex='02A0', c='ʠ', w='q', isLower=True)
GDS['quotedblrightreversed'] = GD(name='quotedblrightreversed', uni=0x201F, hex='201F', c='‟', isLower=True)
GDS['quotereversed'] = GD(name='quotereversed', uni=0x201B, hex='201B', c='‛', l='quotesingle', r='quotesingle', isLower=True, gid=1414)

# r

GDS['rcmb'] = GD(name='rcmb', uni=0x036C, hex='036C', c='ͬ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['rfishhook'] = GD(name='rfishhook', uni=0x027E, hex='027E', c='ɾ', l='asciitilde', srcName='uni027E', isLower=True, gid=465)
GDS['rfishhookmiddletilde'] = GD(name='rfishhookmiddletilde', uni=0x1D73, hex='1D73', c='ᵳ', base='rfishhook', isLower=True)
GDS['rfishhookreversed'] = GD(name='rfishhookreversed', uni=0x027F, hex='027F', c='ɿ', r2l='r', isLower=True)
GDS['rhookturned'] = GD(name='rhookturned', uni=0x027B, hex='027B', c='ɻ', w='r', r2l='r', isLower=True)
GDS['rhotichooksuperior'] = GD(name='rhotichooksuperior', uni=0x02DE, hex='02DE', c='˞', l='48', r='48')
GDS['righttoleftmark'] = GD(name='righttoleftmark', uni=0x200F, hex='200F', c='‏', w=0, isLower=True)
GDS['ringhalfleftcentered'] = GD(name='ringhalfleftcentered', uni=0x02D3, hex='02D3', c='˓', l='center', w=0, base='ringhalfleft', isLower=True, anchors=['_middle', 'middle'])
GDS['ringhalfrightcentered'] = GD(name='ringhalfrightcentered', uni=0x02D2, hex='02D2', c='˒', l='center', w=0, base='ringhalfright', isLower=True, anchors=['_middle', 'middle'])
GDS['rlongleg'] = GD(name='rlongleg', uni=0x027C, hex='027C', c='ɼ', isLower=True)
GDS['rlonglegturned'] = GD(name='rlonglegturned', uni=0x027A, hex='027A', c='ɺ', r2l='r', isLower=True)
GDS['rmiddletilde'] = GD(name='rmiddletilde', uni=0x1D72, hex='1D72', c='ᵲ', l='asciitilde', base='r', isLower=True, fixAccents=False, anchors=['bottom', 'middle', 'top'])
GDS['rpalatalhook'] = GD(name='rpalatalhook', uni=0x1D89, hex='1D89', c='ᶉ', r='r', bl='r', base='r', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['rturned'] = GD(name='rturned', uni=0x0279, hex='0279', c='ɹ', r2l='r', isLower=True)
GDS['replacementchar'] = GD(name='replacementchar', uni=0xFFFD, hex='FFFD', c='�', comment='Replacement Character')

GDS['raisedcolonsuperior'] = GD(name='raisedcolonsuperior', uni=0x02F8, hex='02F8', c='˸', l='colon', r='colon', base='colon')
GDS['rturnedsuperior'] = GD(name='rturnedsuperior', uni=0x02B4, hex='02B4', c='ʴ')
GDS['rhookturnedsuperior'] = GD(name='rhookturnedsuperior', uni=0x02B5, hex='02B5', c='ʵ', rightMin='minRight')

GDS['retroflexhookcmb'] = GD(name='retroflexhookcmb', uni=0x0322, hex='0322', c='̢', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['righthalfringabovecmb'] = GD(name='righthalfringabovecmb', uni=0x0357, hex='0357', c='͗', w=0, isLower=True, anchors=['_top', 'top'])
GDS['righttackbelowcmb'] = GD(name='righttackbelowcmb', uni=0x0319, hex='0319', c='̙', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['ringhalfleftbelowcmb'] = GD(name='ringhalfleftbelowcmb', uni=0x031C, hex='031C', c='̜', l='center', w=0, base='ringhalfleft', isLower=True, anchors=['_bottom', 'bottom'])
GDS['ringhalfrightbelowcmb'] = GD(name='ringhalfrightbelowcmb', uni=0x0339, hex='0339', c='̹', w=0, base='ringhalfright', isLower=True, anchors=['_bottom', 'bottom'])

# s

GDS['schwahook'] = GD(name='schwahook', uni=0x025A, hex='025A', c='ɚ', l='schwa', r='0', rightMin='minRight', isLower=True, comment='The glyph Unicode 025a represents the vowel sound "ɚ" (schwa with rhotic hook) which is commonly used in phonetic transcription to represent the unstressed syllable in words such as "butter" or "teacher." It is also used in the International Phonetic Alphabet (IPA) to represent the same sound.')
GDS['schwaretroflexhook'] = GD(name='schwaretroflexhook', uni=0x1D95, hex='1D95', c='ᶕ', l2r='schwaretroflexhook', base='schwa', accents=['retroflexhookcmb', 'gpalatalhookcmb'], isLower=True, anchors=['top'])
GDS['shook'] = GD(name='shook', uni=0x0282, hex='0282', c='ʂ', l='s', r='s', isLower=True)
GDS['smiddletilde'] = GD(name='smiddletilde', uni=0x1D74, hex='1D74', c='ᵴ', l='asciitilde', r='asciitilde', base='s', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['spalatalhook'] = GD(name='spalatalhook', uni=0x1D8A, hex='1D8A', c='ᶊ', l='s', r='jdotless', base='s', accents=['dpalatalhookcmb', 'gpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['sswashtail'] = GD(name='sswashtail', uni=0x023F, hex='023F', c='ȿ', l='s', w='s', isLower=True)
GDS['strokelongcmb'] = GD(name='strokelongcmb', uni=0x0336, hex='0336', c='̶', w=0, isLower=True, anchors=['_middle', 'middle'])

GDS['schwasuperior'] = GD(name='schwasuperior', uni=0x1D4A, hex='1D4A', c='ᵊ', l2r='esuperior', r2l='esuperior', srcName='uni1D4A', gid=910)
GDS['scriptgsuperior'] = GD(name='scriptgsuperior', uni=0x1DA2, hex='1DA2', c='ᶢ', l='gsuperior', r='gsuperior', base='gsuperior')
GDS['shooksuperior'] = GD(name='shooksuperior', uni=0x1DB3, hex='1DB3', c='ᶳ', l='ssuperior', r='ssuperior')
GDS['shelfsuperior'] = GD(name='shelfsuperior', uni=0x02FD, hex='02FD', c='˽', l='48', r='48')

GDS['seagullbelowcmb'] = GD(name='seagullbelowcmb', uni=0x033C, hex='033C', c='̼', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['slashlongcmb'] = GD(name='slashlongcmb', uni=0x0338, hex='0338', c='̸', w=0, srcName='uni0338', anchors=['_middle', 'middle'], gid=507)
GDS['slashshortcmb'] = GD(name='slashshortcmb', uni=0x0337, hex='0337', c='̷', w=0, isLower=True, anchors=['_middle', 'middle'])
GDS['squarebelowcmb'] = GD(name='squarebelowcmb', uni=0x033B, hex='033B', c='̻', l='center', w=0, isLower=True, anchors=['_bottom', 'bottom'])

# t

GDS['tccurl'] = GD(name='tccurl', uni=0x02A8, hex='02A8', c='ʨ', l='t', r='c', isLower=True)
GDS['tmiddletilde'] = GD(name='tmiddletilde', uni=0x1D75, hex='1D75', c='ᵵ', l='asciitilde', r='asciitilde', base='t', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ts'] = GD(name='ts', uni=0x02A6, hex='02A6', c='ʦ', l='t', r='s', isLower=True)
GDS['tturned'] = GD(name='tturned', uni=0x0287, hex='0287', c='ʇ', l2r='t', r2l='t', isLower=True)

GDS['tonebarextrahighsuperior'] = GD(name='tonebarextrahighsuperior', uni=0x02E5, hex='02E5', c='˥', l='48', r='H', isLower=True)
GDS['tonebarextralowsuperior'] = GD(name='tonebarextralowsuperior', uni=0x02E9, hex='02E9', c='˩', l='48', r='H', isLower=True)
GDS['tonebarhighsuperior'] = GD(name='tonebarhighsuperior', uni=0x02E6, hex='02E6', c='˦', l='48', r='H', isLower=True)
GDS['tonebarlowsuperior'] = GD(name='tonebarlowsuperior', uni=0x02E8, hex='02E8', c='˨', l='48', r='H', isLower=True)
GDS['tonebarmidsuperior'] = GD(name='tonebarmidsuperior', uni=0x02E7, hex='02E7', c='˧', l='48', r='H', isLower=True)

GDS['tcmb'] = GD(name='tcmb', uni=0x036D, hex='036D', c='ͭ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['tildedoublecmb'] = GD(name='tildedoublecmb', uni=0x0360, hex='0360', c='͠', w=0, isLower=True, anchors=['_top', 'top'])
GDS['tildeverticalcmb'] = GD(name='tildeverticalcmb', uni=0x033E, hex='033E', c='̾', w=0, isLower=True, anchors=['_top', 'top'])

# u

GDS['underscoredbl'] = GD(name='underscoredbl', uni=0x2017, hex='2017', c='‗', isLower=True, gid=1410)
GDS['uretroflexhook'] = GD(name='uretroflexhook', uni=0x1D99, hex='1D99', c='ᶙ', w='u', base='u', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['ustroke'] = GD(name='ustroke', uni=0x1D7E, hex='1D7E', c='ᵾ', l='hyphen', r='hyphen', isLower=True)
GDS['undertie'] = GD(name='undertie', uni=0x203F, hex='203F', c='‿', comment='Undertie')

GDS['ubarsuperior'] = GD(name='ubarsuperior', uni=0x1DB6, hex='1DB6', c='ᶶ', l='48', r='48')
GDS['unaspiratedsuperior'] = GD(name='unaspiratedsuperior', uni=0x02ED, hex='02ED', c='˭', l=GD.CAT_MOD_MIN_MARGIN, r=GD.CAT_MOD_MIN_MARGIN, isLower=True)
GDS['upsilonsuperior'] = GD(name='upsilonsuperior', uni=0x1DB7, hex='1DB7', c='ᶷ', l='osuperior', r='osuperior')
GDS['uptacksuperior'] = GD(name='uptacksuperior', uni=0x02D4, hex='02D4', c='˔', l=GD.CAT_MOD_MIN_MARGIN, r=GD.CAT_MOD_MIN_MARGIN, isLower=True)

GDS['ucmb'] = GD(name='ucmb', uni=0x0367, hex='0367', c='ͧ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['uptackbelowcmb'] = GD(name='uptackbelowcmb', uni=0x031D, hex='031D', c='̝', l='center', w=0, base='uptacksuperior', isLower=True, anchors=['_bottom', 'bottom'])

# v

GDS['vcmb'] = GD(name='vcmb', uni=0x036E, hex='036E', c='ͮ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['vpalatalhook'] = GD(name='vpalatalhook', uni=0x1D8C, hex='1D8C', c='ᶌ', l='v', r='jdotless', base='v', accents=['dpalatalhookcmb', 'gpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['vrighthook'] = GD(name='vrighthook', uni=0x2C71, hex='2C71', c='ⱱ', isLower=True, anchors=['top'])

GDS['vhooksuperior'] = GD(name='vhooksuperior', uni=0x1DB9, hex='1DB9', c='ᶹ')
GDS['verticallinelowsuperior'] = GD(name='verticallinelowsuperior', uni=0x02CC, hex='02CC', c='ˌ', base='verticallinesuperior', isLower=True)
GDS['vturnedsuperior'] = GD(name='vturnedsuperior', uni=0x1DBA, hex='1DBA', c='ᶺ', l='vsuperior', r='vsuperior')

# w

GDS['wturned'] = GD(name='wturned', uni=0x028D, hex='028D', c='ʍ', l='v', r='v', isLower=True)
GDS['xabovecmb'] = GD(name='xabovecmb', uni=0x033D, hex='033D', c='̽', l='center', w=0, base='xbelowcmb', isLower=True, anchors=['_top', 'top'])
GDS['xbelowcmb'] = GD(name='xbelowcmb', uni=0x0353, hex='0353', c='͓', w=0, isLower=True, anchors=['_bottom', 'bottom'])
GDS['xcmb'] = GD(name='xcmb', uni=0x036F, hex='036F', c='ͯ', w=0, isLower=True, anchors=['_top', 'top'])
GDS['xpalatalhook'] = GD(name='xpalatalhook', uni=0x1D8D, hex='1D8D', c='ᶍ', l='x', r='jdotless', base='x', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])

# y

GDS['yangdepartingtone'] = GD(name='yangdepartingtone', uni=0x02EB, hex='02EB', c='˫', isLower=True)
GDS['ypogegrammenicmb'] = GD(name='ypogegrammenicmb', uni=0x0345, hex='0345', c='ͅ', w=0, base='prosgegrammeni', isLower=True, anchors=['_bottom', 'bottom'], gid=508)

# z

GDS['zcurl'] = GD(name='zcurl', uni=0x0291, hex='0291', c='ʑ', isLower=True)
GDS['zmiddletilde'] = GD(name='zmiddletilde', uni=0x1D76, hex='1D76', c='ᵶ', l='asciitilde', r='asciitilde', base='z', isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['zpalatalhook'] = GD(name='zpalatalhook', uni=0x1D8E, hex='1D8E', c='ᶎ', l='z', r='jdotless', base='z', accents=['dpalatalhookcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
GDS['zretroflexhook'] = GD(name='zretroflexhook', uni=0x0290, hex='0290', c='ʐ', w='z', isLower=True)
GDS['zretroflexhooksuperior'] = GD(name='zretroflexhooksuperior', uni=0x1DBC, hex='1DBC', c='ᶼ', l='zsuperior')
GDS['zswashtail'] = GD(name='zswashtail', uni=0x0240, hex='0240', c='ɀ', l='z', w='z', isLower=True)

GDS['zcurlsuperior'] = GD(name='zcurlsuperior', uni=0x1DBD, hex='1DBD', c='ᶽ', l='zsuperior')

GDS['zigzagabovecmb'] = GD(name='zigzagabovecmb', uni=0x035B, hex='035B', c='͛', w=0, isLower=True, anchors=['_top', 'top'])

# Accents & Components

GDS['bpalatalhookcmb'] = GD(name='bpalatalhookcmb', w=0)
GDS['dpalatalhookcmb'] = GD(name='dpalatalhookcmb', w=0)
GDS['gpalatalhookcmb'] = GD(name='gpalatalhookcmb', w=0)

if __name__ == '__main__':
    for gName, gd in GDS.items():
        #print('---', gd)
        if gd.base and gd.base not in GDS:
            print('##### Missing base', gName, gd.base)
        for aName in gd.accents:
            if aName not in GDS:
                print('#### Missing accent', gName, aName)


