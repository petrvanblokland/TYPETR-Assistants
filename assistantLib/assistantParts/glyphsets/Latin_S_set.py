# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_S_set.py
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
#    Latin S
#    AÁĂǍÂÄẠÀĀĄÅÃÆBḄƁCĆČÇĈĊDÐĎĐḌƊEÉĔĚÊËĖẸÈĒĘƐƎẼFGĞĜĢĠḠǦHĦĤḦḤIÍĬǏÎÏİỊÌĪĮƗĨJĴKĶƘLĹĽĻŁMNŃŇŅṄṆƝÑŊ
#    OÓŎǑÔÖỌÒŐŌƆØÕŒPṖÞQRŔŘŖSŚŠŞŜȘṢẞƏTŤŢȚUÚŬǓÛÜỤÙŰŪŲŮŨVɅWẂŴẄẀXẌYÝŶŸỲƳỸȲZŹŽŻẒaáăǎâäạàāąåãæbḅɓcć
#    čçĉċdðďđḍɗeéĕěêëėẹèēęɛẽǝəfgğĝģġḡǧhħĥḧḥiıíĭǐîïịìīįɨĩjȷĵkķƙlĺľļłmnńňņṅṇɲñŋoóŏǒôöọòőōɔøõœpṗ
#    þqrŕřŗsśšşŝșṣßtťţțuúŭǔûüụùűūųůũvʌwẃŵẅẁxẍyýŷÿỳƴỹȳzźžżẓ₵₡₲₺₼₦₹ ̈ ̇ ̀ ́ ̋ ̂ ̌ ̆ ̊ ̃ ̄ ̒ ̣ ̦ ̧ ̨ʼʻ ̵
#
#    See README.md for list of supported languages and recommendations for the OpenType code.
#
if __name__ == '__main__': # Used for doc tests to find assistantLib
    import os, sys
    PATH = '/'.join(__file__.split('/')[:-4]) # Relative path to this respository that holds AssistantLib
    if not PATH in sys.path:
        sys.path.append(PATH)

from assistantLib.assistantParts.glyphsets.glyphData import *
from assistantLib.assistantParts.glyphsets.anchorData import AD

# Values to be implemented by MasterData for each master
#MIN_MARGIN = 24
#EM_WIDTH = 1000
#EN_WIDTH = int(EM_WIDTH/2)
#SPACE_WIDTH = int(EM_WIDTH/5)
#FIGURE_WIDTH = 650 # 1265 for Segoe UI 2048-EM
#ACCENT_WIDTH = FIGURE_WIDTH/2
#FRACTION_WIDTH = FIGURE_WIDTH/4
#HAIR_WIDTH = int(EM_WIDTH/8)
#MOD_MIN = 48 # Constant margin for some superior and unferiot glyphs

LATIN_S_SET_NAME = 'LatinS'

# The "c" attribtes are redundant, if the @uni or @hex are defined, but they are offer easy searching in the source by char.
LATIN_S_SET = GDS = {

    #   .

    '.notdef': GD(name='.notdef'),
    '.null': GD(name='.null', uni=0x0000, hex='0000'),
    'uni000D': GD(name='uni000D', uni=0x000D, hex='000D'),
    'nbspace': GD(name='nbspace', uni=0x00A0, hex='00A0', w=GD.CAT_SPACE_WIDTH, c=' ', srcName='nonbreakingspace', isLower=False, comment='  Symbols, Latin-1 Punctuation and'),
    'space': GD(name='space', uni=0x0020, hex='0020', w=GD.CAT_SPACE_WIDTH, c=' ', isLower=False, comment='  Symbols, ASCII Punctuation and'),
    'emspace': GD(name='emspace', uni=0x2003, hex='2003', w=GD.CAT_EM_WIDTH, c=' ', isLower=False),
    'enspace': GD(name='enspace', uni=0x2002, hex='2002', w=GD.CAT_EN_WIDTH, c=' ', isLower=False),
    'figurespace': GD(name='figurespace', uni=0x2007, w=GD.CAT_FIGURE_WIDTH, hex='2007', c=' ', isLower=False),
    'hairspace': GD(name='hairspace', uni=0x200A, hex='200A', w=GD.CAT_HAIR_WIDTH, c=' ', isLower=False),
    'spacemarker': GD(name='spacemarker', w=0),
    'narrownbspace': GD(name='narrownbspace', uni=0x202F, w=GD.CAT_HAIR_WIDTH, hex='202F', c=' ', isLower=False),

    # rest of ascii

    'colon': GD(name='colon', uni=0x003A, hex='003A', c=':', l='period', r='period', isLower=True, comment=': COLON'),
    'cedilla': GD(name='cedilla', base='cedillacmb', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True),
    'cent': GD(name='cent', uni=0x00A2, hex='00A2', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='¢', isLower=True, comment='¢ CENT SIGN'),
    'cent.alt': GD(name='cent.alt', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='¢ CENT SIGN'),
    'comma': GD(name='comma', uni=0x002C, hex='002C', c=',', l='off', isLower=True, comment=', separator, decimal'),
    'copyright': GD(name='copyright', uni=0x00A9, hex='00A9', c='©', l='O', r='O', isLower=True, base='largecircle', comment='© COPYRIGHT SIGN'),
    'copyrightsound': GD(l='copyright', r='copyright', uni=0x2117, base='largecircle', name='copyrightsound'),
    'largecircle': GD(l='O', r='O', uni=0x25ef, c='◯', name='largecircle', comment='circle for ® trade mark sign, registered', useSkewRotate=True, addItalicExtremePoints=True),
    'currency': GD(name='currency', uni=0x00A4, hex='00A4', c='¤', isLower=True, l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, comment='¤ CURRENCY SIGN'),

    'degree': GD(name='degree', uni=0x00B0, hex='00B0', c='°', isLower=True, comment='° DEGREE SIGN'),
    'divide': GD(name='divide', uni=0x00F7, hex='00F7', c='÷', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='÷ obelus'),
    'dollar': GD(name='dollar', uni=0x0024, hex='0024', c='$', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='S', isLower=False, comment='$ milreis'),
    'dollar.alt': GD(name='dollar.alt', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='S', isLower=False, comment='$ milreis'),
    'bitcoin': GD(uni=0x20bf, c='₿', name='bitcoin', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='B', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
    'bitcoin.alt': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='bitcoin.alt', base='B', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),

    'exclam': GD(name='exclam', uni=0x0021, hex='0021', c='!', l='H', l2r='self', isLower=True, comment='! factorial'),
    'exclamdown': GD(name='exclamdown', uni=0x00A1, hex='00A1', c='¡', l2r='exclam', r2l='exclam', isLower=True, comment='¡ INVERTED EXCLAMATION MARK'),
    'exclamdown.uc': GD(name='exclamdown.uc', c='¡', l='exclamdown', r='exclamdown', base='exclamdown', isLower=True, comment='¡ INVERTED EXCLAMATION MARK'),
    'equal': GD(name='equal', uni=0x003D, hex='003D', c='=', isLower=True, comment='= EQUALS SIGN'),

    'hyphen': GD(name='hyphen', uni=0x002D, hex='002D', c='-', l2r='self', unicodes=(45, 8208), isLower=True, comment='- minus sign, hyphen'),
    'hyphen.uc': GD(name='hyphen.uc', l='hyphen', r='hyphen', base='hyphen', comment='- minus sign, hyphen'),
    'endash': GD(name='endash', uni=0x2013, hex='2013', c='–', isLower=True, comment='– EN DASH'),
    'endash.uc': GD(name='endash.uc', isLower=True, base='endash', comment='– EN DASH'),
    'emdash': GD(g2='hyphen', g1='hyphen', w=GD.CAT_EM, uni=0x2014, c='—', name='emdash', comment='— EM DASH', anchors=[]),
    'emdash.uc': GD(g2='hyphen', g1='hyphen', l='emdash', r='emdash', name='emdash.uc', base='emdash', comment='— EM DASH Uppercase', anchors=[]),
    'horizontalbar': GD(g2='hyphen', g1='hyphen', l='emdash', r='emdash', uni=0x2015, c='―', name='horizontalbar', base='emdash', anchors=[]),
    'horizontalbar.uc': GD(g2='hyphen', g1='hyphen', l='horizontalbar', r='horizontalbar', name='horizontalbar.uc', comment='Horizontal base Uppercase', anchors=[]),

    'hungarumlaut': GD(name='hungarumlaut', uni=0x02DD, hex='02DD', c='˝', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='hungarumlautcmb', isLower=True, comment='˝ DOUBLE ACUTE ACCENT'),

    'less': GD(name='less', uni=0x003C, hex='003C', c='<', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='< LESS-THAN SIGN'),
    'lessequal': GD(name='lessequal', uni=0x2264, hex='2264', c='≤', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='≤ LESS-THAN OR EQUAL TO'),
    'logicalnot': GD(name='logicalnot', uni=0x00AC, hex='00AC', c='¬', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='¬ NOT SIGN'),
    'lozenge': GD(l2r='lozenge', uni=0x25ca, c='◊', name='lozenge', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, comment='◊ LOZENGE', anchors=[]),

    'macron': GD(name='macron', uni=0x00AF, hex='00AF', c='¯', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='macroncmb', srcName='uni00AF', isLower=True, comment='¯ spacing macron'),
    'multiply': GD(name='multiply', uni=0x00D7, hex='00D7', c='×', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='× product, cartesian'),
    
    'numbersign': GD(name='numbersign', uni=0x0023, hex='0023', c='#', l2r='self', isLower=True, comment='# pound sign'),
    'notequal': GD(name='notequal', uni=0x2260, hex='2260', c='≠', base='equal', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='≠ NOT EQUAL TO'),

    'ordfeminine': GD(name='ordfeminine', uni=0x00AA, hex='00AA', c='ª', isLower=True, comment='ª ORDINAL INDICATOR, FEMININE'),
    'ordmasculine': GD(name='ordmasculine', uni=0x00BA, hex='00BA', c='º', isLower=True, comment='º ORDINAL INDICATOR, MASCULINE'),

    'paragraph': GD(name='paragraph', uni=0x00B6, hex='00B6', c='¶', l='zerosuperior', r='H', isLower=True, comment='¶ section sign, european'),
    'parenleft': GD(name='parenleft', uni=0x0028, hex='0028', c='(', isLower=True, comment='( parenthesis, opening'),
    'parenleft.uc': GD(name='parenleft.uc', srcName='parenleft', comment='( parenthesis, opening for capitals'),
    'parenright': GD(name='parenright', uni=0x0029, hex='0029', c=')', l2r='parenleft', r2l='parenleft', isLower=True, comment=') RIGHT PARENTHESIS'),
    'parenright.uc': GD(name='parenright.uc', srcName='parenright', l2r='parenleft', r2l='parenleft', comment='( parenthesis, for capitals'),
    'percent': GD(name='percent', uni=0x0025, hex='0025', c='%', l='zerosuperior', r='zerosuperior', isLower=True, comment='% PERCENT SIGN', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPERIOR_HEIGHT, overshoot=GD.CAT_SUPERIOR_OVERSHOOT),
    'percent.tab': GD(name='percent.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, comment='% PERCENT SIGN TAB'),
    'perthousand': GD(l='zerosuperior', r='zerosuperior', uni=0x2030, c='‰', name='perthousand', comment='‰ per thousand', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPERIOR_HEIGHT, overshoot=GD.CAT_SUPERIOR_OVERSHOOT),
    'period': GD(name='period', uni=0x002E, hex='002E', c='.', l2r='self', isLower=True, fixSpacing=False, comment='. point, decimal'),
    'period.uc': GD(name='period.uc', l2r='self', isLower=True, fixSpacing=False, base='period', comment='. point, decimal'),
    'ellipsis': GD(name='ellipsis', uni=0x2026, hex='2026', c='…', l='period', r='period', isLower=True, comment='… three dot leader'),
    'periodcentered': GD(name='periodcentered', uni=0x00B7, hex='00B7', c='·', l='period', r='period', isLower=True),
    'periodcentered.uc': GD(name='periodcentered.uc', base='periodcentered', l='period', r='period', isLower=True),
    'partialdiff': GD(name='partialdiff', uni=0x2202, hex='2202', c='∂', l='o', r='O', isLower=True, comment='∂ PARTIAL DIFFERENTIAL'),

    'plusminus': GD(name='plusminus', uni=0x00B1, hex='00B1', c='±', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='± PLUS-MINUS SIGN'),
    'plus': GD(name='plus', uni=0x002B, hex='002B', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='+', isLower=True, comment='+ PLUS SIGN'),
    'minus': GD(name='minus', uni=0x2212, hex='2212', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='−', isLower=True, comment='− MINUS SIGN'),
    'pi': GD(name='pi', uni=0x03C0, hex='03C0', c='π', isLower=True),

    'question': GD(name='question', uni=0x003F, hex='003F', c='?', isLower=True, comment='? QUESTION MARK'),
    'questiondown': GD(name='questiondown', uni=0x00BF, hex='00BF', c='¿', l2r='question', r2l='question', isLower=True, comment='¿ turned question mark'),
    'questiondown.uc': GD(name='questiondown.uc', l='questiondown', r='questiondown', base='questiondown', isLower=True, comment='¿ turned question mark'),

    'registered': GD(name='registered', uni=0x00AE, hex='00AE', c='®', l='copyright', r='copyright', base='largecircle', isLower=True, comment='® trade mark sign, registered'),
    'ring': GD(name='ring', base='ringcmb', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True, comment='˚ RING'),

    'section': GD(name='section', uni=0x00A7, hex='00A7', c='§', l='s', r='s', isLower=True, comment='§ SECTION SIGN'),
    'semicolon': GD(name='semicolon', uni=0x003B, hex='003B', c=';', l='comma', r='comma', isLower=True, comment='; SEMICOLON'),
    'slash': GD(name='slash', uni=0x002F, hex='002F', c='/', l2r='self', isLower=False, comment='/ virgule'),
    'sterling': GD(name='sterling', uni=0x00A3, hex='00A3', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='£', isLower=True, comment='£ sterling, pound'),

    'trademark': GD(name='trademark', uni=0x2122, hex='2122', c='™', isLower=True, comment='™ TRADE MARK SIGN'),

    'underscore': GD(name='underscore', uni=0x005F, hex='005F', c='_', isLower=True, comment='_ underscore, spacing'),

    'yen': GD(name='yen', uni=0x00A5, hex='00A5', c='¥', isLower=True, l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='Y', comment='¥ yuan sign'),

    # Fixed fractions

    'onesuperior': GD(name='onesuperior', uni=0x00B9, hex='00B9', c='¹', isLower=True, comment='¹ SUPERSCRIPT ONE'),
    'twosuperior': GD(name='twosuperior', uni=0x00B2, hex='00B2', c='²', isLower=False, comment='² TWO, SUPERSCRIPT'),
    'threesuperior': GD(name='threesuperior', uni=0x00B3, hex='00B3', c='³', isLower=False, comment='³ THREE, SUPERSCRIPT'),

    'onehalf': GD(name='onehalf', uni=0x00BD, hex='00BD', c='½', base='one.numr', accents=['fraction', 'two.dnom'], isLower=False, comment='½ VULGAR FRACTION ONE HALF'),
    'onequarter': GD(name='onequarter', uni=0x00BC, hex='00BC', c='¼', base='one.numr', accents=['fraction', 'four.dnom'], isLower=True, comment='¼ VULGAR FRACTION ONE QUARTER'),
    'oneseventh': GD(name='oneseventh', uni=0x2150, hex='2150', c='⅐', l='one.numr', r='seven.dnom', base='one.numr', accents=['fraction', 'seven.dnom'], isLower=False),
    'onesixth': GD(name='onesixth', uni=0x2159, hex='2159', c='⅙', l='one.numr', r='six.dnom', base='one.numr', accents=['fraction', 'six.dnom'], isLower=False),
    'threequarters': GD(name='threequarters', uni=0x00BE, hex='00BE', c='¾', base='three.numr', accents=['fraction', 'four.dnom'], isLower=False, comment='¾ VULGAR FRACTION THREE QUARTERS'),

    'fraction': GD(l=GD.CAT_CENTER, w=GD.CAT_FRACTION_WIDTH, name='fraction', uni=0x2044, c='⁄', isLower=False, comment='⁄ solidus'),
   
    # A

    'A': GD(name='A', uni=0x0041, hex='0041', c='A', l2r='self', anchorTopX='TopX',anchorTopY='TopY', anchors=['bottom', 'middle', 'ogonek', 'tonos', 'top'], comment='A Uppercase Alphabet, Latin'),
    'AE': GD(name='AE', uni=0x00C6, hex='00C6', c='Æ', l='A', r='E', anchorTopX='TopX', anchors=['bottom', 'middle', 'top'], comment='Æ ligature ae, latin capital'),

    'Aacute': GD(name='Aacute', uni=0x00C1, hex='00C1', c='Á', l='A', r='A', base='A', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER'),
    'Abreve': GD(name='Abreve', uni=0x0102, hex='0102', c='Ă', l='A', r='A', base='A', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE'),
    'Acaron': GD(name='Acaron', uni=0x01CD, hex='01CD', c='Ǎ', l='A', r='A', base='A', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek']),
    'Acircumflex': GD(name='Acircumflex', uni=0x00C2, hex='00C2', c='Â', l='A', r='A', base='A', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Adieresis': GD(name='Adieresis', uni=0x00C4, hex='00C4', c='Ä', l='A', r='A', base='A', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Adotbelow': GD(name='Adotbelow', uni=0x1EA0, hex='1EA0', c='Ạ', l='A', r='A', base='A', accents=['dotbelowcmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ạ LATIN CAPITAL LETTER A WITH DOT BELOW'),
    'Agrave': GD(name='Agrave', uni=0x00C0, hex='00C0', c='À', l='A', r='A', base='A', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
    'Amacron': GD(name='Amacron', uni=0x0100, hex='0100', c='Ā', l='A', r='A', base='A', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ā Latin, European'),
    'Aogonek': GD(name='Aogonek', uni=0x0104, hex='0104', c='Ą', l='A', r='A', base='A', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),
    'Aring': GD(name='Aring', uni=0x00C5, hex='00C5', c='Å', l='A', r='A', anchorTopY='TopY', base='A', accents=['ringcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Å RING ABOVE, LATIN CAPITAL LETTER A WITH'),
    'Atilde': GD(name='Atilde', uni=0x00C3, hex='00C3', c='Ã', l='A', r='A', base='A', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ã A WITH TILDE, LATIN CAPITAL LETTER'),

    # B

    'B': GD(name='B', uni=0x0042, hex='0042', c='B', l='H', anchors=['bottom', 'middle', 'top'], comment='B LATIN CAPITAL LETTER B'),
    'Bdotbelow': GD(name='Bdotbelow', uni=0x1E04, hex='1E04', c='Ḅ', l='H', r='B', base='B', accents=['dotbelowcmb.uc'], srcName='uni1E04', anchors=['bottom', 'middle', 'top']),
    'Bhook': GD(name='Bhook', uni=0x0181, hex='0181', c='Ɓ', l=GD.CAT_HAIR_WIDTH, r='B', base='B', comment='Ɓ B WITH HOOK, LATIN CAPITAL LETTER'),

    # C

    'C': GD(name='C', uni=0x0043, hex='0043', c='C', l='O', anchorTopX='TopX', anchorBottomX='BottomX', anchors=['bottom', 'dot', 'middle', 'top'], comment='C LATIN CAPITAL LETTER C'),
    'Cacute': GD(name='Cacute', uni=0x0106, hex='0106', c='Ć', l='O', r='C', base='C', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ć LATIN CAPITAL LETTER C WITH ACUTE'),
    'Ccaron': GD(name='Ccaron', uni=0x010C, hex='010C', c='Č', l='O', r='C', base='C', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Č LATIN CAPITAL LETTER C WITH CARON'),
    'Ccedilla': GD(name='Ccedilla', uni=0x00C7, hex='00C7', c='Ç', l='O', r='C', base='C', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ç CEDILLA, LATIN CAPITAL LETTER C WITH'),
    'Ccircumflex': GD(name='Ccircumflex', uni=0x0108, hex='0108', c='Ĉ', l='O', r='C', base='C', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ĉ LATIN CAPITAL LETTER C WITH CIRCUMFLEX'),
    'Cdotaccent': GD(name='Cdotaccent', uni=0x010A, hex='010A', c='Ċ', l='O', r='C', base='C', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ċ LATIN CAPITAL LETTER C WITH DOT ABOVE'),

    # D

    'D': GD(name='D', uni=0x0044, hex='0044', c='D', l='H', r='O', anchors=['bottom', 'middle', 'top'], comment='D'),
    'Dcaron': GD(name='Dcaron', uni=0x010E, hex='010E', c='Ď', l='D', r='D', base='D', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ď'),
    'Dcroat': GD(name='Dcroat', uni=0x0110, hex='0110', c='Đ', base='Eth', comment='Đ'),
    'Ddotbelow': GD(name='Ddotbelow', uni=0x1E0C, hex='1E0C', c='Ḍ', l='D', r='D', base='D', accents=['dotbelowcmb.uc'], srcName='uni1E0C', anchors=['bottom', 'middle', 'top']),
    'Dhook': GD(name='Dhook', uni=0x018A, hex='018A', c='Ɗ', l=GD.CAT_HAIR_WIDTH, r='D', base='D', comment='Ɗ D WITH HOOK, LATIN CAPITAL LETTER'),
    'Delta': GD(name='Delta', uni=0x0394, hex='0394', c='Δ', l='off', l2r='self', comment='∆ symmetric difference'),

    # E

    'E': GD(name='E', uni=0x0045, hex='0045', c='E', l='H', anchorBottomX='BottomX', anchors=['bottom', 'middle', 'ogonek', 'tonos', 'top'], comment='E'),
    'Eacute': GD(name='Eacute', uni=0x00C9, hex='00C9', c='É', l='H', r='E', base='E', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='É E WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ebreve': GD(name='Ebreve', uni=0x0114, hex='0114', c='Ĕ', l='H', r='E', base='E', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ĕ'),
    'Ecaron': GD(name='Ecaron', uni=0x011A, hex='011A', c='Ě', l='H', r='E', base='E', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ě'),
    'Ecircumflex': GD(name='Ecircumflex', uni=0x00CA, hex='00CA', c='Ê', l='H', r='E', base='E', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ê E WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Edieresis': GD(name='Edieresis', uni=0x00CB, hex='00CB', c='Ë', l='H', r='E', base='E', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ë E WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Edotaccent': GD(name='Edotaccent', uni=0x0116, hex='0116', c='Ė', l='H', r='E', base='E', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Edotbelow': GD(name='Edotbelow', uni=0x1EB8, hex='1EB8', c='Ẹ', l='H', r='E', base='E', accents=['dotbelowcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ẹ LATIN CAPITAL LETTER E WITH DOT BELOW'),
    'Egrave': GD(name='Egrave', uni=0x00C8, hex='00C8', c='È', l='H', r='E', base='E', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='È E WITH GRAVE, LATIN CAPITAL LETTER'),
    'Emacron': GD(name='Emacron', uni=0x0112, hex='0112', c='Ē', l='H', r='E', base='E', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ē'),
    'Eng': GD(name='Eng', uni=0x014A, hex='014A', c='Ŋ', l='N', r='N', comment='Ŋ'),
    'Eogonek': GD(name='Eogonek', uni=0x0118, hex='0118', c='Ę', l='E', w='E', base='E', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ę'),
    'Eopen': GD(name='Eopen', uni=0x0190, hex='0190', c='Ɛ', r='C', r2l='B', srcName='uni0190', comment='Ɛ OPEN E, LATIN CAPITAL LETTER'),
    'Ereversed': GD(name='Ereversed', uni=0x018E, hex='018E', c='Ǝ', r2l='E', l2r='E', srcName='E', comment='Ǝ turned e, latin capital letter'),
    'Eth': GD(name='Eth', uni=0x00D0, hex='00D0', c='Ð', r='D', base='D', comment='Ð ETH, LATIN CAPITAL LETTER'),
    'Etilde': GD(name='Etilde', uni=0x1EBC, hex='1EBC', c='Ẽ', l='E', r='E', base='E', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ẽ LATIN CAPITAL LETTER E WITH TILDE'),
    'Euro': GD(g1='C', g2='Euro', r='C', uni=0x20AC, c='€', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, src=['C', 'hyphen', 'hyphen'], name='Euro'),

    # F

    'F': GD(name='F', uni=0x0046, hex='0046', c='F', l='H', anchors=['bottom', 'middle', 'top'], comment='F'),

    # G

    'G': GD(name='G', uni=0x0047, hex='0047', c='G', l='O', anchorTopX='TopX', anchorBottomX='BottomX', anchors=['bottom', 'middle', 'top'], comment='G'),
    'Gbreve': GD(name='Gbreve', uni=0x011E, hex='011E', c='Ğ', l='G', r='G', base='G', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ğ'),
    'Gcaron': GD(name='Gcaron', uni=0x01E6, hex='01E6', c='Ǧ', l='G', r='G', base='G', accents=['caroncmb.uc'], srcName='uni01E6', anchors=['bottom', 'middle', 'top']),
    'Gcircumflex': GD(name='Gcircumflex', uni=0x011C, hex='011C', c='Ĝ', l='G', r='G', base='G', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ĝ'),
    'Gcommaaccent': GD(name='Gcommaaccent', uni=0x0122, hex='0122', c='Ģ', l='G', r='G', base='G', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ģ'),
    'Gdotaccent': GD(name='Gdotaccent', uni=0x0120, hex='0120', c='Ġ', l='G', r='G', base='G', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ġ'),
    'Germandbls': GD(name='Germandbls', uni=0x1E9E, hex='1E9E', c='ẞ', srcName='uni1E9E'),
    'Gmacron': GD(name='Gmacron', uni=0x1E20, hex='1E20', c='Ḡ', l='G', r='G', base='G', accents=['macroncmb.uc'], srcName='uni1E20', anchors=['bottom', 'middle', 'top']),

    # H

    'H': GD(name='H', uni=0x0048, hex='0048', c='H', l2r='self', anchors=['bottom', 'middle', 'tonos', 'top'], comment='H'),
    'Hbar': GD(name='Hbar', uni=0x0126, hex='0126', c='Ħ', l='Eth', l2r='self', base='H', comment='Ħ'),
    'Hcircumflex': GD(name='Hcircumflex', uni=0x0124, hex='0124', c='Ĥ', l='H', r='H', base='H', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ĥ'),
    'Hdieresis': GD(name='Hdieresis', uni=0x1E26, hex='1E26', c='Ḧ', l='H', r='H', base='H', accents=['dieresiscmb.uc'], srcName='uni1E26', anchors=['bottom', 'middle', 'top']),
    'Hdotbelow': GD(name='Hdotbelow', uni=0x1E24, hex='1E24', c='Ḥ', l='H', r='H', base='H', accents=['dotbelowcmb.uc'], srcName='uni1E24', anchors=['bottom', 'middle', 'top']),

    # I

    'I': GD(name='I', uni=0x0049, hex='0049', c='I', l='H', r='H', anchors=['bottom', 'middle', 'ogonek', 'tonos', 'top'], comment='I'),
    'Iacute': GD(name='Iacute', uni=0x00CD, hex='00CD', c='Í', w='I', bl='I', base='I', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ibreve': GD(name='Ibreve', uni=0x012C, hex='012C', c='Ĭ', w='I', bl='I', base='I', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ĭ'),
    'Icaron': GD(name='Icaron', uni=0x01CF, hex='01CF', c='Ǐ', w='I', bl='I', base='I', accents=['caroncmb.uc'], srcName='uni01CF', anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Icircumflex': GD(name='Icircumflex', uni=0x00CE, hex='00CE', c='Î', w='I', bl='I', base='I', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Idieresis': GD(name='Idieresis', uni=0x00CF, hex='00CF', c='Ï', w='I', bl='I', base='I', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Idotaccent': GD(name='Idotaccent', uni=0x0130, hex='0130', c='İ', w='I', bl='I', base='I', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
    'Idotbelow': GD(name='Idotbelow', uni=0x1ECA, hex='1ECA', c='Ị', w='I', bl='I', base='I', accents=['dotbelowcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ị LATIN CAPITAL LETTER I WITH DOT BELOW'),
    'Igrave': GD(name='Igrave', uni=0x00CC, hex='00CC', c='Ì', w='I', bl='I', base='I', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
    'Imacron': GD(name='Imacron', uni=0x012A, hex='012A', c='Ī', w='I', bl='I', base='I', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ī'),
    'Iogonek': GD(name='Iogonek', uni=0x012E, hex='012E', c='Į', w='I', bl='I', base='I', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Į'),
    'Istroke': GD(name='Istroke', uni=0x0197, hex='0197', c='Ɨ', l='hyphen', l2r='self', base='I'),
    'Itilde': GD(name='Itilde', uni=0x0128, hex='0128', c='Ĩ', w='I', bl='I', base='I', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ĩ'),

    # J

    'J': GD(name='J', uni=0x004A, hex='004A', c='J', anchors=['bottom', 'middle', 'top'], comment='J'),
    'Jcircumflex': GD(name='Jcircumflex', uni=0x0134, hex='0134', c='Ĵ', w='J', bl='J', base='J', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ĵ'),


    # K

    'K': GD(name='K', uni=0x004B, hex='004B', c='K', l='H', anchors=['bottom', 'middle', 'top'], comment='K'),
    'Kcommaaccent': GD(name='Kcommaaccent', uni=0x0136, hex='0136', c='Ķ', l='H', r='K', base='K', accents=['cedillacmb.noconnect'], anchors=['bottom', 'middle', 'top'], comment='Ķ'),
    'Khook': GD(name='Khook', uni=0x0198, hex='0198', c='Ƙ', l='H', w='K', srcName='K', comment='Ƙ LATIN CAPITAL LETTER K WITH HOOK'),

    # L

    'L': GD(name='L', uni=0x004C, hex='004C', c='L', l='H', anchorTopX='TopX', anchorBottomX='BottomX', anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='L'),
    'Lacute': GD(name='Lacute', uni=0x0139, hex='0139', c='Ĺ', l='H', r='L', base='L', accents=['acutecmb.uc'], fixAccents=False, anchors=['bottom', 'middle', 'top'], comment='Ĺ'),
    'Lcaron': GD(name='Lcaron', uni=0x013D, hex='013D', c='Ľ', l='H', w='L', base='L', accents=['caroncmb.vert'], anchors=['bottom', 'middle', 'top'], comment='Ľ'),
    'Lcommaaccent': GD(name='Lcommaaccent', uni=0x013B, hex='013B', c='Ļ', l='H', r='L', base='L', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ļ'),
    'Lslash': GD(name='Lslash', uni=0x0141, hex='0141', c='Ł', r='L', base='L', comment='Ł'),

    # M

    'M': GD(name='M', uni=0x004D, hex='004D', c='M', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='M'),

    # N

    'N': GD(name='N', uni=0x004E, hex='004E', c='N', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='N'),
    'Nacute': GD(name='Nacute', uni=0x0143, hex='0143', c='Ń', l='H', r='H', base='N', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ń'),
    'Ncaron': GD(name='Ncaron', uni=0x0147, hex='0147', c='Ň', l='H', r='H', base='N', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ň'),
    'Ncommaaccent': GD(name='Ncommaaccent', uni=0x0145, hex='0145', c='Ņ', l='H', r='H', base='N', accents=['cedillacmb.noconnect'], anchors=['bottom', 'middle', 'top'], comment='Ņ'),
    'Ndotaccent': GD(name='Ndotaccent', uni=0x1E44, hex='1E44', c='Ṅ', l='H', r='H', base='N', accents=['dotaccentcmb.uc'], srcName='uni1E44', anchors=['bottom', 'middle', 'top']),
    'Ndotbelow': GD(name='Ndotbelow', uni=0x1E46, hex='1E46', c='Ṇ', l='H', r='H', base='N', accents=['dotbelowcmb.uc'], srcName='uni1E46', anchors=['bottom', 'middle', 'top']),
    'Nhookleft': GD(name='Nhookleft', uni=0x019D, hex='019D', c='Ɲ', l='off', r='N', srcName='N'),
    'Ntilde': GD(name='Ntilde', uni=0x00D1, hex='00D1', c='Ñ', l='H', r='H', base='N', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ñ N WITH TILDE, LATIN CAPITAL LETTER'),

    # O

    'O': GD(name='O', uni=0x004F, hex='004F', c='O', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'tonos', 'top'], comment='O'),
    'OE': GD(name='OE', uni=0x0152, hex='0152', c='Œ', l='O', r='E', anchors=['bottom', 'middle', 'top'], comment='Œ'),
    'Oacute': GD(name='Oacute', uni=0x00D3, hex='00D3', c='Ó', l='O', r='O', base='O', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
    'Obreve': GD(name='Obreve', uni=0x014E, hex='014E', c='Ŏ', l='O', r='O', base='O', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ŏ'),
    'Ocaron': GD(name='Ocaron', uni=0x01D1, hex='01D1', c='Ǒ', l='O', r='O', base='O', accents=['caroncmb.uc'], srcName='uni01D1', anchors=['bottom', 'middle', 'top']),
    'Ocircumflex': GD(name='Ocircumflex', uni=0x00D4, hex='00D4', c='Ô', l='O', r='O', base='O', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Odieresis': GD(name='Odieresis', uni=0x00D6, hex='00D6', c='Ö', l='O', r='O', base='O', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Odotbelow': GD(name='Odotbelow', uni=0x1ECC, hex='1ECC', c='Ọ', l='O', r='O', base='O', accents=['dotbelowcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ọ LATIN CAPITAL LETTER O WITH DOT BELOW'),
    'Ograve': GD(name='Ograve', uni=0x00D2, hex='00D2', c='Ò', l='O', r='O', base='O', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
    'Ohungarumlaut': GD(name='Ohungarumlaut', uni=0x0150, hex='0150', c='Ő', base='O', accents=['hungarumlautcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ő'),
    'Omacron': GD(name='Omacron', uni=0x014C, hex='014C', c='Ō', l='O', r='O', base='O', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ō'),
    'Oopen': GD(name='Oopen', uni=0x0186, hex='0186', c='Ɔ', r='O', r2l='C', srcName='O', comment='Ɔ OPEN O, LATIN CAPITAL LETTER'),
    'Oslash': GD(name='Oslash', uni=0x00D8, hex='00D8', c='Ø', l='O', w='O', base='O', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Oslash.alt': GD(name='Oslash.alt', l='O', w='O', base='O', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Otilde': GD(name='Otilde', uni=0x00D5, hex='00D5', c='Õ', l='O', r='O', base='O', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),

    # P

    'P': GD(name='P', uni=0x0050, hex='0050', c='P', l='H', anchors=['bottom', 'middle', 'tonos', 'top'], comment='P'),
    'Pdotaccent': GD(name='Pdotaccent', uni=0x1E56, hex='1E56', c='Ṗ', l='P', w='P', base='P', accents=['dotaccentcmb.uc'], srcName='uni1E56', anchors=['bottom', 'middle', 'top']),

    # Q

    'Q': GD(name='Q', uni=0x0051, hex='0051', c='Q', l='O', w='O', anchors=['bottom', 'middle', 'top'], comment='Q'),

    # R

    'R': GD(name='R', uni=0x0052, hex='0052', c='R', l='H', anchors=['bottom', 'middle', 'top'], comment='R'),
    'Racute': GD(name='Racute', uni=0x0154, hex='0154', c='Ŕ', bl='H', r='R', base='R', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŕ'),
    'Rcaron': GD(name='Rcaron', uni=0x0158, hex='0158', c='Ř', bl='H', r='R', base='R', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ř'),
    'Rcommaaccent': GD(name='Rcommaaccent', uni=0x0156, hex='0156', c='Ŗ', bl='H', r='R', base='R', accents=['cedillacmb.noconnect'], anchors=['bottom', 'middle', 'top'], comment='Ŗ'),

    # S

    'S': GD(name='S', uni=0x0053, hex='0053', c='S', l2r='self', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='S'),
    'Sacute': GD(name='Sacute', uni=0x015A, hex='015A', c='Ś', l='S', w='S', base='S', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ś'),
    'Scaron': GD(name='Scaron', uni=0x0160, hex='0160', c='Š', l='S', w='S', base='S', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Š'),
    'Scedilla': GD(name='Scedilla', uni=0x015E, hex='015E', c='Ş', l='S', w='S', base='S', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ş'),
    'Schwa': GD(name='Schwa', uni=0x018F, hex='018F', c='Ə', l='O', r='O', srcName='uni018F', anchors=['top'], comment='Ə SCHWA, LATIN CAPITAL LETTER'),
    'Scircumflex': GD(name='Scircumflex', uni=0x015C, hex='015C', c='Ŝ', l='S', w='S', base='S', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŝ'),
    'Scommaaccent': GD(name='Scommaaccent', uni=0x0218, hex='0218', c='Ș', l='S', w='S', base='S', accents=['cedillacmb.noconnect'], anchors=['bottom', 'middle', 'top'], comment='Ș'),
    'Sdotbelow': GD(name='Sdotbelow', uni=0x1E62, hex='1E62', c='Ṣ', l='S', w='S', base='S', accents=['dotbelowcmb.uc'], srcName='uni1E62', anchors=['bottom', 'middle', 'top'], comment='Ṣ LATIN CAPITAL LETTER S WITH DOT BELOW'),

    # T

    'T': GD(name='T', uni=0x0054, hex='0054', c='T', l2r='self', anchors=['bottom', 'middle', 'top'], comment='T'),
    'Tcaron': GD(name='Tcaron', uni=0x0164, hex='0164', c='Ť', l='T', r='T', base='T', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ť'),
    'Tcedilla': GD(name='Tcedilla', uni=0x0162, hex='0162', c='Ţ', l='T', r='T', base='T', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ţ'),
    'Tcommaaccent': GD(name='Tcommaaccent', uni=0x021A, hex='021A', c='Ț', l='T', r='T', base='T', accents=['cedillacmb.noconnect'], anchors=['bottom', 'middle', 'top'], comment='Ț'),
    'Thorn': GD(name='Thorn', uni=0x00DE, hex='00DE', c='Þ', l='H', r='P', comment='Þ THORN, LATIN CAPITAL LETTER'),

    # U

    'U': GD(name='U', uni=0x0055, hex='0055', c='U', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='U'),
    'Uacute': GD(name='Uacute', uni=0x00DA, hex='00DA', c='Ú', l='U', r='U', base='U', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ú U WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ubreve': GD(name='Ubreve', uni=0x016C, hex='016C', c='Ŭ', l='U', r='U', base='U', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ŭ'),
    'Ucaron': GD(name='Ucaron', uni=0x01D3, hex='01D3', c='Ǔ', l='U', r='U', base='U', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Ucircumflex': GD(name='Ucircumflex', uni=0x00DB, hex='00DB', c='Û', l='U', r='U', base='U', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle','ogonek',  'top'], comment='Û U WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Udieresis': GD(name='Udieresis', uni=0x00DC, hex='00DC', c='Ü', l='U', r='U', base='U', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ü U WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Udotbelow': GD(name='Udotbelow', uni=0x1EE4, hex='1EE4', c='Ụ', l='U', r='U', base='U', accents=['dotbelowcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ụ LATIN CAPITAL LETTER U WITH DOT BELOW'),
    'Ugrave': GD(name='Ugrave', uni=0x00D9, hex='00D9', c='Ù', l='U', r='U', base='U', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ù U WITH GRAVE, LATIN CAPITAL LETTER'),
    'Uhungarumlaut': GD(name='Uhungarumlaut', uni=0x0170, hex='0170', c='Ű', l='U', r='U', base='U', accents=['hungarumlautcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ű'),
    'Umacron': GD(name='Umacron', uni=0x016A, hex='016A', c='Ū', l='U', r='U', base='U', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ū'),
    'Uogonek': GD(name='Uogonek', uni=0x0172, hex='0172', c='Ų', l='U', r='U', base='U', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ų'),
    'Uring': GD(name='Uring', uni=0x016E, hex='016E', c='Ů', l='U', r='U', base='U', accents=['ringcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ů'),
    'Utilde': GD(name='Utilde', uni=0x0168, hex='0168', c='Ũ', l='U', r='U', base='U', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ũ'),

    # V

    'V': GD(name='V', uni=0x0056, hex='0056', c='V', l2r='self', anchors=['bottom', 'middle', 'top'], comment='V'),
    'Vturned': GD(name='Vturned', uni=0x0245, hex='0245', c='Ʌ', l2r='V', r2l='V'),

    # W

    'W': GD(name='W', uni=0x0057, hex='0057', c='W', l='V', r='V', anchors=['bottom', 'middle', 'top'], comment='W'),
    'Wacute': GD(name='Wacute', uni=0x1E82, hex='1E82', c='Ẃ', l='W', r='W', base='W', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ẃ'),
    'Wcircumflex': GD(name='Wcircumflex', uni=0x0174, hex='0174', c='Ŵ', l='W', r='W', base='W', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŵ'),
    'Wdieresis': GD(name='Wdieresis', uni=0x1E84, hex='1E84', c='Ẅ', l='W', r='W', base='W', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ẅ'),
    'Wgrave': GD(name='Wgrave', uni=0x1E80, hex='1E80', c='Ẁ', l='W', r='W', base='W', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ẁ'),

    # X

    'X': GD(name='X', uni=0x0058, hex='0058', c='X', l2r='self', anchors=['bottom', 'middle', 'top'], comment='X'),
    'Xdieresis': GD(name='Xdieresis', uni=0x1E8C, hex='1E8C', c='Ẍ', base='X', accents=['dieresiscmb.uc'], srcName='uni1E8C', anchors=['bottom', 'middle', 'top']),

    # Y

    'Y': GD(name='Y', uni=0x0059, hex='0059', c='Y', l2r='self', anchors=['bottom', 'middle', 'tonos', 'top'], comment='Y'),
    'Yacute': GD(name='Yacute', uni=0x00DD, hex='00DD', c='Ý', l='Y', r='Y', base='Y', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ý Y WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ycircumflex': GD(name='Ycircumflex', uni=0x0176, hex='0176', c='Ŷ', l='Y', r='Y', base='Y', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŷ'),
    'Ydieresis': GD(name='Ydieresis', uni=0x0178, hex='0178', c='Ÿ', l='Y', r='Y', base='Y', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ÿ Y WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ygrave': GD(name='Ygrave', uni=0x1EF2, hex='1EF2', c='Ỳ', l='Y', r='Y', base='Y', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ỳ'),
    'Yhook': GD(name='Yhook', uni=0x01B3, hex='01B3', c='Ƴ', l='Y', r='Y', srcName='Y', anchors=['bottom', 'middle', 'top'], comment='Ƴ LATIN CAPITAL LETTER Y WITH HOOK'),
    'Ymacron': GD(name='Ymacron', uni=0x0232, hex='0232', c='Ȳ', base='Y', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top']),
    'Ytilde': GD(name='Ytilde', uni=0x1EF8, hex='1EF8', c='Ỹ', l='Y', r='Y', base='Y', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ỹ LATIN CAPITAL LETTER Y WITH TILDE'),

    # Z

    'Z': GD(name='Z', uni=0x005A, hex='005A', c='Z', l2r='self', anchors=['bottom', 'middle', 'top'], comment='Z'),
    'Zacute': GD(name='Zacute', uni=0x0179, hex='0179', c='Ź', l='Z', r='Z', base='Z', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ź'),
    'Zcaron': GD(name='Zcaron', uni=0x017D, hex='017D', c='Ž', l='Z', r='Z', base='Z', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ž'),
    'Zdotaccent': GD(name='Zdotaccent', uni=0x017B, hex='017B', c='Ż', l='Z', r='Z', base='Z', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ż'),
    'Zdotbelow': GD(name='Zdotbelow', uni=0x1E92, hex='1E92', c='Ẓ', l='Z', r='Z', base='Z', accents=['dotbelowcmb.uc'], srcName='uni1E92', anchors=['bottom', 'middle', 'top']),

    # a

    'a': GD(name='a', uni=0x0061, hex='0061', c='a', isLower=True, anchorTopX='TopX', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='a Small Letters, Latin'),
    'aacute': GD(name='aacute', uni=0x00E1, hex='00E1', c='á', w='a', bl='a', base='a', anchorTopY='TopY',accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='á A WITH ACUTE, LATIN SMALL LETTER'),
    'abreve': GD(name='abreve', uni=0x0103, hex='0103', c='ă', w='a', bl='a', base='a', anchorTopY='TopY',accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ă A WITH BREVE, LATIN SMALL LETTER'),
    'acaron': GD(name='acaron', uni=0x01CE, hex='01CE', c='ǎ', w='a', bl='a', base='a', anchorTopY='TopY',accents=['caroncmb'], srcName='uni01CE', isLower=True, anchors=['bottom', 'middle', 'top']),
    'acircumflex': GD(name='acircumflex', uni=0x00E2, hex='00E2', c='â', w='a', bl='a', base='a', anchorTopY='TopY', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='â A WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'adieresis': GD(name='adieresis', uni=0x00E4, hex='00E4', c='ä', w='a', bl='a', base='a', anchorTopY='TopY', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ä A WITH DIAERESIS, LATIN SMALL LETTER'),
    'adotbelow': GD(name='adotbelow', uni=0x1EA1, hex='1EA1', c='ạ', w='a', bl='a', base='a', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ạ A WITH DOT BELOW, LATIN SMALL LETTER'),
    'ae': GD(name='ae', uni=0x00E6, hex='00E6', c='æ', l='a', r='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='æ small ligature ae, latin'),
    'agrave': GD(name='agrave', uni=0x00E0, hex='00E0', c='à', w='a', bl='a', base='a', anchorTopY='TopY', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='à A WITH GRAVE, LATIN SMALL LETTER'),
    'amacron': GD(name='amacron', uni=0x0101, hex='0101', c='ā', base='a', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ā A WITH MACRON, LATIN SMALL LETTER'),
    'aogonek': GD(name='aogonek', uni=0x0105, hex='0105', c='ą', base='a', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ą A WITH OGONEK, LATIN SMALL LETTER'),
    'aring': GD(name='aring', uni=0x00E5, hex='00E5', c='å', base='a', anchorTopY='TopY', accents=['ringcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='å RING ABOVE, LATIN SMALL LETTER A WITH'),
    'atilde': GD(name='atilde', uni=0x00E3, hex='00E3', c='ã', base='a', anchorTopY='TopY', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ã A WITH TILDE, LATIN SMALL LETTER'),

    'ampersand': GD(name='ampersand', uni=0x0026, hex='0026', c='&', r2l='B', r='t', isLower=False, comment='& AMPERSAND'), # For italic shape
    'asciicircum': GD(name='asciicircum', uni=0x005E, hex='005E', c='^', l2r='self', isLower=True, comment='^ spacing circumflex accent'),
    'asciitilde': GD(name='asciitilde', uni=0x007E, hex='007E', c='~', l2r='asciitilde', isLower=True, comment='~ tilde, spacing'),
    'asterisk': GD(name='asterisk', uni=0x002A, hex='002A', c='*', l2r='self', isLower=True, comment='* star'),
    'at': GD(name='at', uni=0x0040, hex='0040', c='@', l2r='self', l='O', isLower=True, comment='@ COMMERCIAL AT'),

    'acute': GD(name='acute', uni=0x00B4, hex='00B4', c='´', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='acutecmb', isLower=True, comment='´ spacing acute accent'),

    'acutecmb': GD(name='acutecmb', uni=0x0301, anchorTopY='TopY', hex='0301', c='́', w=0, isLower=True, anchors=['_top', 'top']),
    'acutecmb.uc': GD(name='acutecmb.uc', w=0, anchorTopY='TopY', isLower=True, srcName='acutecmb', anchors=['_top', 'top']),

    'quotesuperior': GD(name='quotesuperior', uni=0x02BC, hex='02BC', c='ʼ', isLower=True, isMod=True),

    # b

    'b': GD(name='b', uni=0x0062, hex='0062', c='b', l='h', r='o', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'top'], comment='b'),
    'bdotbelow': GD(name='bdotbelow', uni=0x1E05, hex='1E05', c='ḅ', base='b', accents=['dotbelowcmb'], srcName='uni1E05', isLower=True, anchors=['bottom', 'middle', 'top']),
    'bhook': GD(name='bhook', uni=0x0253, hex='0253', c='ɓ', l='b', r='b', isLower=True),
    'backslash': GD(name='backslash', uni=0x005C, hex='005C', c="\\" , l2r='self', isLower=True, comment='\\ SOLIDUS, REVERSE'),
    'bar': GD(name='bar', uni=0x007C, hex='007C', c='|', l='H', r='H', isLower=True, comment='| VERTICAL LINE'),
    'braceleft': GD(name='braceleft', uni=0x007B, hex='007B', c='{', isLower=True, comment='{ opening curly bracket'),
    'braceleft.uc': GD(name='bracelef.uct', srcName='braceleft', comment='{ opening curly bracket'),
    'braceright': GD(name='braceright', uni=0x007D, hex='007D', c='}', l2r='braceleft', r2l='braceleft', isLower=True, comment='} RIGHT CURLY BRACKET'),
    'braceright.uc': GD(name='braceright.uc', l2r='braceleft', r2l='braceleft', srcName='braceright', isLower=True, comment='} RIGHT CURLY BRACKET'),
    'bracketleft': GD(name='bracketleft', uni=0x005B, hex='005B', c='[', isLower=True, comment='[ square bracket, opening'),
    'bracketleft.uc': GD(name='bracketleft.uc', srcName='bracketleft', comment='[ square bracket, opening'),
    'bracketright': GD(name='bracketright', uni=0x005D, hex='005D', c=']', l2r='bracketleft', r2l='bracketleft', isLower=True, comment='] SQUARE BRACKET, RIGHT'),
    'bracketright.uc': GD(name='bracketright.uc', l2r='bracketleft', r2l='bracketleft', srcName='bracketright', comment='] SQUARE BRACKET, RIGHT'),
    'brokenbar': GD(name='brokenbar', uni=0x00A6, hex='00A6', c='¦', isLower=True, comment='¦ vertical bar, broken'),
    'bullet': GD(name='bullet', uni=0x2022, hex='2022', c='•', isLower=True, l2r='self', comment='• small circle, black'),
    'bullet.uc': GD(name='bullet.uc', l='bullet', r='bullet', base='bullet', isLower=True, comment='• small circle, black'),

    'breve': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02d8, c='˘', name='breve', base='brevecmb', comment='˘ Spacing Clones of Diacritics', anchors=[]),
    'brevecmb': GD(name='brevecmb', uni=0x0306, hex='0306', anchorTopY='TopY', c='̆', w=0, srcName='uni0306', isLower=True, anchors=['_top', 'top']),
    'brevecmb.uc': GD(name='brevecmb.uc', w=0, anchorTopY='TopY', srcName='brevecmb', isLower=True, anchors=['_top', 'top']),

    # c

    'c': GD(name='c', uni=0x0063, hex='0063', c='c', isLower=True, anchorTopX='TopX', anchorBottomX='BottomX',anchors=['bottom', 'dot', 'middle', 'top'], comment='c'),
    'cacute': GD(name='cacute', uni=0x0107, hex='0107', c='ć', anchorTopY='TopY', base='c', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ć C WITH ACUTE, LATIN SMALL LETTER'),
    'ccaron': GD(name='ccaron', uni=0x010D, hex='010D', c='č', anchorTopY='TopY', base='c', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='č C WITH CARON, LATIN SMALL LETTER'),
    'ccedilla': GD(name='ccedilla', uni=0x00E7, hex='00E7', c='ç', base='c', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ç CEDILLA, LATIN SMALL LETTER C WITH'),
    'ccircumflex': GD(name='ccircumflex', uni=0x0109, hex='0109', c='ĉ', anchorTopY='TopY', base='c', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĉ C WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'cdotaccent': GD(name='cdotaccent', uni=0x010B, hex='010B', c='ċ', anchorTopY='TopY', base='c', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'cedi': GD(name='cedi', uni=0x20B5, hex='20B5', c='₵', base='C', l='C', r='C', isLower=True),
    'colonsign': GD(name='colonsign', uni=0x20A1, hex='20A1', c='₡', isLower=True),
    'caron': GD(name='caron', uni=0x02C7, hex='02C7', c='ˇ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True, base='caroncmb', comment='ˇ tone, mandarin chinese third'),

    'commaturnedsuperior': GD(name='commaturnedsuperior', uni=0x02BB, hex='02BB', c='ʻ', isMod=True),

    # d

    'd': GD(name='d', uni=0x0064, hex='0064', c='d', isLower=True, anchorTopY='TopY', anchors=['bottom', 'middle', 'top', 'vert'], comment='d'),
    'dcaron': GD(name='dcaron', uni=0x010F, hex='010F', c='ď', l='d', r='comma', anchorTopY='TopY', base='d', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ď D WITH CARON, LATIN SMALL LETTER'),
    'dcroat': GD(name='dcroat', uni=0x0111, hex='0111', c='đ', l='d', r='hyphen', isLower=True, anchorTopY='TopY', base='d', comment='đ D WITH STROKE, LATIN SMALL LETTER'),
    'ddotbelow': GD(name='ddotbelow', uni=0x1E0D, hex='1E0D', c='ḍ', base='d', accents=['dotbelowcmb'], srcName='uni1E0D', isLower=True, anchors=['bottom', 'middle', 'top']),
    'dhook': GD(name='dhook', uni=0x0257, hex='0257', c='ɗ', w='d', anchorTopY='TopY', isLower=True),
    'dagger': GD(name='dagger', uni=0x2020, hex='2020', c='†', l2r='self', isLower=True, comment='† DAGGER'),
    'daggerdbl': GD(name='daggerdbl', uni=0x2021, hex='2021', c='‡', l='dagger', r='dagger', isLower=True, comment='‡ DOUBLE DAGGER'),

    'dieresis': GD(name='dieresis', uni=0x00A8, hex='00A8', c='¨', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='dieresiscmb', isLower=True, comment='¨ spacing diaeresis'),
    'dieresiscmb': GD(name='dieresiscmb', uni=0x0308, hex='0308', anchorTopY='TopY', c='̈', w=0, isLower=True, anchors=['_top', 'top']),
    'dieresiscmb.uc': GD(name='dieresiscmb.uc', w=0, anchorTopY='TopY', srcName='dieresiscmb', isLower=True, anchors=['_top', 'top']),
    'dotaccentcmb': GD(name='dotaccentcmb', uni=0x0307, anchorTopY='TopY', hex='0307', c='̇', w=0, isLower=True, anchors=['_top', 'top']),
    'dotaccentcmb.uc': GD(name='dotaccentcmb.uc', w=0, anchorTopY='TopY', srcName='dotaccentcmb', isLower=True, anchors=['_top', 'top']),
    'dotbelowcmb': GD(name='dotbelowcmb', uni=0x0323, hex='0323', c='̣', w=0, base='dotaccentcmb', isLower=True, anchors=['_bottom', 'bottom']),
    'dotbelowcmb.uc': GD(name='dotbelowcmb.uc', w=0, srcName='dotbelowcmb', isLower=True, anchors=['_bottom', 'bottom']),

    # e

    'e': GD(name='e', uni=0x0065, hex='0065', c='e', isLower=True, anchorTopX='TopX', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='e'),
    'eacute': GD(name='eacute', uni=0x00E9, hex='00E9', c='é', anchorTopY='TopY', base='e', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='é E WITH ACUTE, LATIN SMALL LETTER'),
    'ebreve': GD(name='ebreve', uni=0x0115, hex='0115', c='ĕ', anchorTopY='TopY', base='e', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĕ E WITH BREVE, LATIN SMALL LETTER'),
    'ecaron': GD(name='ecaron', uni=0x011B, hex='011B', c='ě', anchorTopY='TopY', base='e', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ě E WITH CARON, LATIN SMALL LETTER'),
    'ecircumflex': GD(name='ecircumflex', uni=0x00EA, hex='00EA', c='ê', anchorTopY='TopY', base='e', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ê E WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'edieresis': GD(name='edieresis', uni=0x00EB, hex='00EB', c='ë', w='e', anchorTopY='TopY', base='e', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ë E WITH DIAERESIS, LATIN SMALL LETTER'),
    'edotaccent': GD(name='edotaccent', uni=0x0117, hex='0117', c='ė', w='e', anchorTopY='TopY', base='e', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'edotbelow': GD(name='edotbelow', uni=0x1EB9, hex='1EB9', c='ẹ', w='e', anchorTopY='TopY', base='e', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ẹ E WITH DOT BELOW, LATIN SMALL LETTER'),
    'egrave': GD(name='egrave', uni=0x00E8, hex='00E8', c='è', w='e', bl='e', anchorTopY='TopY', base='e', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='è E WITH GRAVE, LATIN SMALL LETTER'),
    'emacron': GD(name='emacron', uni=0x0113, hex='0113', c='ē', base='e', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ē E WITH MACRON, LATIN SMALL LETTER'),
    'eng': GD(name='eng', uni=0x014B, hex='014B', c='ŋ', l='n', isLower=True, comment='ŋ LATIN SMALL LETTER ENG'),
    'eogonek': GD(name='eogonek', uni=0x0119, hex='0119', c='ę', base='e', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ę E WITH OGONEK, LATIN SMALL LETTER'),
    'eopen': GD(name='eopen', uni=0x025B, hex='025B', c='ɛ', isLower=True, anchors=['top']),
    'eth': GD(name='eth', uni=0x00F0, hex='00F0', c='ð', isLower=True, comment='ð LATIN SMALL LETTER ETH'),
    'etilde': GD(name='etilde', uni=0x1EBD, hex='1EBD', c='ẽ', l='e', r='e', base='e', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ẽ E WITH TILDE, LATIN SMALL LETTER'),
    'eturned': GD(name='eturned', uni=0x01DD, hex='01DD', c='ǝ', l='e', r='e', srcName='uni01DD', isLower=True, anchors=['top'], comment='ǝ TURNED E, LATIN SMALL LETTER'),

    # f

    'f': GD(name='f', uni=0x0066, hex='0066', c='f', l='t', rightMin='-100', anchorTopX='TopX', isLower=True, fixAccents=True, anchors=['bottom', 'middle', 'top'], comment='f'),
    'f.alt': GD(name='f.alt', l='f', rightMin='-100', anchorTopX='TopX', isLower=True, fixAccents=True, srcName='f', anchors=['bottom', 'middle', 'top'], comment='f.alt, allowing for serif-terminal alternative.'), 
    'fi': GD(name='fi', uni=0xFB01, hex='FB01', c='ﬁ', l='f', r='i', base='f.alt_connect', accents=['idotless'], isLower=True, comment='ﬁ f_i'),
    'fl': GD(name='fl', uni=0xFB02, hex='FB02', c='ﬂ', l='f', r='l', isLower=True, base='f.alt_noconnect', accents=['l'], comment='ﬂ f_l'),
    # Minimal 2 alternatives for connecting (long flag) and not-connecting (short flag)
    'f.alt_connect': GD(name='f.alt_connect', l='f', rightMin='-100', anchorTopX='TopX', isLower=True, fixAccents=True, srcName='f', anchors=['bottom', 'middle', 'top'], comment='f.alt, allowing for serif-terminal alternative.'), 
    'f.alt_noconnect': GD(name='f.alt_noconnect', l='f', rightMin='-100', anchorTopX='TopX', isLower=True, fixAccents=True, srcName='f', anchors=['bottom', 'middle', 'top'], comment='f.alt, allowing for serif-terminal alternative.'), 

    # g

    'g': GD(name='g', uni=0x0067, hex='0067', c='g', l2r='l', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g'),
    'gbreve': GD(name='gbreve', uni=0x011F, hex='011F', c='ğ', anchorTopY='TopY', base='g', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ğ G WITH BREVE, LATIN SMALL LETTER'),
    'gcaron': GD(name='gcaron', uni=0x01E7, hex='01E7', c='ǧ', anchorTopY='TopY', base='g', accents=['caroncmb'], srcName='uni01E7', isLower=True, anchors=['bottom', 'middle', 'top']),
    'gcircumflex': GD(name='gcircumflex', uni=0x011D, hex='011D', c='ĝ', anchorTopY='TopY', base='g', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĝ G WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'gcommaaccent': GD(name='gcommaaccent', uni=0x0123, hex='0123', c='ģ', anchorTopY='TopY', base='g', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'gdotaccent': GD(name='gdotaccent', uni=0x0121, hex='0121', c='ġ', anchorTopY='TopY', base='g', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'germandbls': GD(name='germandbls', uni=0x00DF, hex='00DF', c='ß', isLower=True, comment='ß SHARP S, LATIN SMALL LETTER'),
    'gmacron': GD(name='gmacron', uni=0x1E21, hex='1E21', c='ḡ', anchorTopY='TopY', base='g', accents=['macroncmb'], srcName='uni1E21', isLower=True, anchors=['bottom', 'middle', 'top']),
    'guarani': GD(name='guarani', uni=0x20B2, hex='20B2', c='₲', isLower=True),
    'greater': GD(name='greater', uni=0x003E, hex='003E', c='>', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='> GREATER-THAN SIGN'),
    'greaterequal': GD(name='greaterequal', uni=0x2265, hex='2265', c='≥', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='≥ GREATER-THAN OR EQUAL TO'),
    'guillemotleft': GD(name='guillemotleft', uni=0x00AB, hex='00AB', l2r='self', c='«', isLower=True),
    'guillemotleft.uc': GD(name='guillemotleft.uc', l2r='self', base='guillemotleft', isLower=True),
    'guillemotright': GD(name='guillemotright', uni=0x00BB, hex='00BB', l='guillemotleft', r='guillemotleft', c='»', isLower=True),
    'guillemotright.uc': GD(name='guillemotright.uc',  l='guillemotleft', r='guillemotleft',  base='guillemotright', isLower=True),
    'guilsinglleft': GD(name='guilsinglleft', uni=0x2039, hex='2039', l='guillemotleft', r='guillemotleft', c='‹', isLower=True, comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglleft.uc': GD(name='guilsinglleft.uc', l='guilsinglleft', r='guilsinglleft', base='guilsinglleft', isLower=True, comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglright': GD(name='guilsinglright', uni=0x203A, hex='203A', l='guillemotleft', r='guillemotleft', c='›', isLower=True, comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglright.uc': GD(name='guilsinglright.uc', l='guilsinglright', r='guilsinglright', base='guilsinglright', isLower=True, comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK'),

    'grave': GD(name='grave', uni=0x0060, hex='0060', c='`', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='gravecmb', isLower=True, comment='` spacing grave accent'),
    'gravecmb': GD(name='gravecmb', uni=0x0300, hex='0300', c='̀', anchorTopY='TopY', w=0, isLower=True, anchors=['_top', 'top']),
    'gravecmb.uc': GD(name='gravecmb.uc', w=0, isLower=True, anchorTopY='TopY', srcName='gravecmb', anchors=['_top', 'top']),

    # h

    'h': GD(name='h', uni=0x0068, hex='0068', c='h', isLower=True, anchorTopY='TopY', anchors=['bottom', 'dot', 'middle', 'top'], comment='h'),
    'hbar': GD(name='hbar', uni=0x0127, hex='0127', c='ħ', l='hyphen', r='h', base='h', isLower=True, comment='ħ H WITH STROKE, LATIN SMALL LETTER'),
    'hcircumflex': GD(name='hcircumflex', uni=0x0125, hex='0125', c='ĥ', anchorTopY='TopY', base='h', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĥ H WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'hdieresis': GD(name='hdieresis', uni=0x1E27, hex='1E27', c='ḧ', anchorTopY='TopY', base='h', accents=['dieresiscmb'], srcName='uni1E27', isLower=True, anchors=['bottom', 'middle', 'top']),
    'hdotbelow': GD(name='hdotbelow', uni=0x1E25, hex='1E25', c='ḥ', anchorTopY='TopY', base='h', accents=['dotbelowcmb'], srcName='uni1E25', isLower=True, anchors=['bottom', 'middle', 'top']),
    
    'hungarumlautcmb': GD(name='hungarumlautcmb', uni=0x030B, anchorTopY='TopY', hex='030B', c='̋', w=0, isLower=True, anchors=['_top', 'top']),
    'hungarumlautcmb.uc': GD(name='hungarumlautcmb.uc', w=0, anchorTopY='TopY', srcName='hungarumlautcmb', isLower=True, anchors=['_top', 'top']),

    # i

    'i': GD(name='i', uni=0x0069, hex='0069', c='i', l='off', w='idotless', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='i'),
    'iacute': GD(name='iacute', uni=0x00ED, hex='00ED', c='í', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='í I WITH ACUTE, LATIN SMALL LETTER'),
    'ibreve': GD(name='ibreve', uni=0x012D, hex='012D', c='ĭ', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ĭ I WITH BREVE, LATIN SMALL LETTER'),
    'icaron': GD(name='icaron', uni=0x01D0, hex='01D0', c='ǐ', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'icircumflex': GD(name='icircumflex', uni=0x00EE, hex='00EE', c='î', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='î I WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'idieresis': GD(name='idieresis', uni=0x00EF, hex='00EF', c='ï', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ï I WITH DIAERESIS, LATIN SMALL LETTER'),
    'idotbelow': GD(name='idotbelow', uni=0x1ECB, hex='1ECB', c='ị', w='idotless', bl='idotless', anchorTopY='TopY', base='i', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ị I WITH DOT BELOW, LATIN SMALL LETTER'),
    'idotless': GD(name='idotless', uni=0x0131, hex='0131', c='ı', l='l', r='off', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'igrave': GD(name='igrave', uni=0x00EC, hex='00EC', c='ì', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ì I WITH GRAVE, LATIN SMALL LETTER'),
    'imacron': GD(name='imacron', uni=0x012B, hex='012B', c='ī', w='idotless', bl='idotless', anchorTopY='TopY', base='idotless', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ī I WITH MACRON, LATIN SMALL LETTER'),
    'iogonek': GD(name='iogonek', uni=0x012F, hex='012F', c='į', anchorTopY='TopY', base='i', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='į I WITH OGONEK, LATIN SMALL LETTER'),
    'istroke': GD(name='istroke', uni=0x0268, hex='0268', c='ɨ', l='hyphen', r='hyphen', base='i', isLower=True),
    'itilde': GD(name='itilde', uni=0x0129, hex='0129', c='ĩ', bl='idotless', anchorTopY='TopY', base='idotless', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ĩ I WITH TILDE, LATIN SMALL LETTER'),
    'infinity': GD(name='infinity', uni=0x221E, hex='221E', c='∞', l='o', r='o', isLower=False, comment='∞ INFINITY'),
    
    # j
    'j': GD(name='j', uni=0x006A, hex='006A', c='j', l='off', r='off', isLower=True, anchors=['bottom', 'middle'], comment='j'),
    'jcircumflex': GD(name='jcircumflex', uni=0x0135, hex='0135', c='ĵ', l='j', w='j', base='jdotless', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĵ J WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'jdotless': GD(name='jdotless', uni=0x0237, hex='0237', c='ȷ', l='j', r='j', isLower=True, anchors=['bottom', 'middle', 'top']),

    # k

    'k': GD(name='k', uni=0x006B, hex='006B', c='k', l='h', r='x', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'top'], comment='k'),
    'kcommaaccent': GD(name='kcommaaccent', uni=0x0137, hex='0137', c='ķ', anchorTopY='TopY', base='k', accents=['cedillacmb.noconnect'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'khook': GD(name='khook', uni=0x0199, hex='0199', c='ƙ', l='k', anchorTopY='TopY', srcName='uni0199', isLower=True, comment='ƙ K WITH HOOK, LATIN SMALL LETTER'),

    # l

    'l': GD(name='l', uni=0x006C, hex='006C', c='l', l='h', r='idotless', anchorTopY='TopY', isLower=True, anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='l'),
    'lacute': GD(name='lacute', uni=0x013A, hex='013A', c='ĺ', w='l', bl='l', anchorTopY='TopY', base='l', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER'),
    'lcaron': GD(name='lcaron', uni=0x013E, hex='013E', c='ľ', rightMin='minRight', anchorTopY='TopY', base='l', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ľ L WITH CARON, LATIN SMALL LETTER'),
    'lcommaaccent': GD(name='lcommaaccent', uni=0x013C, hex='013C', c='ļ', w='l', anchorTopY='TopY', base='l', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'liraTurkish': GD(name='liraTurkish', uni=0x20BA, hex='20BA', c='₺', srcName='l', isLower=True),
    'lslash': GD(name='lslash', uni=0x0142, hex='0142', c='ł', base='l', l='hyphen', r='hyphen', isLower=True, comment='ł L WITH STROKE, LATIN SMALL LETTER'),

    # m

    'm': GD(name='m', uni=0x006D, hex='006D', c='m', l='n', r='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='m'),
    'manat': GD(name='manat', uni=0x20BC, hex='20BC', c='₼', l='O', r='O', srcName='O', isLower=True),

    'macroncmb': GD(name='macroncmb', uni=0x0304, anchorTopY='TopY', hex='0304', c='̄', w=0, srcName='uni0304', isLower=True, anchors=['_top', 'top']),
    'macroncmb.uc': GD(name='macroncmb.uc', w=0, anchorTopY='TopY', srcName='macroncmb', isLower=True, anchors=['_top', 'top']),

    # n

    'n': GD(name='n', uni=0x006E, hex='006E', c='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='n'),
    'nacute': GD(name='nacute', uni=0x0144, hex='0144', c='ń', base='n', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ń N WITH ACUTE, LATIN SMALL LETTER'),
    'naira': GD(name='naira', uni=0x20A6, hex='20A6', c='₦'),
    'ncaron': GD(name='ncaron', uni=0x0148, hex='0148', c='ň', base='n', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ň N WITH CARON, LATIN SMALL LETTER'),
    'ncommaaccent': GD(name='ncommaaccent', uni=0x0146, hex='0146', c='ņ', base='n', accents=['cedillacmb.noconnect'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'ndotaccent': GD(name='ndotaccent', uni=0x1E45, hex='1E45', c='ṅ', base='n', accents=['dotaccentcmb'], srcName='uni1E45', isLower=True, anchors=['bottom', 'middle', 'top']),
    'ndotbelow': GD(name='ndotbelow', uni=0x1E47, hex='1E47', c='ṇ', base='n', accents=['dotbelowcmb'], srcName='uni1E47', isLower=True, anchors=['bottom', 'middle', 'top']),
    'nhookleft': GD(name='nhookleft', uni=0x0272, hex='0272', c='ɲ', isLower=True),
    'ntilde': GD(name='ntilde', uni=0x00F1, hex='00F1', c='ñ', base='n', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ñ N WITH TILDE, LATIN SMALL LETTER'),

    # o

    'o': GD(name='o', uni=0x006F, hex='006F', c='o', l2r='self', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='o'),
    'oacute': GD(name='oacute', uni=0x00F3, hex='00F3', c='ó', l='o', r='o', base='o', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ó O WITH ACUTE, LATIN SMALL LETTER'),
    'obreve': GD(name='obreve', uni=0x014F, hex='014F', c='ŏ', w='o', bl='o', base='o', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ŏ O WITH BREVE, LATIN SMALL LETTER'),
    'ocaron': GD(name='ocaron', uni=0x01D2, hex='01D2', c='ǒ', w='o', bl='o', base='o', accents=['caroncmb'], srcName='uni01D2', isLower=True, anchors=['bottom', 'middle', 'top']),
    'ocircumflex': GD(name='ocircumflex', uni=0x00F4, hex='00F4', c='ô', w='o', bl='o', base='o', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ô O WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'odieresis': GD(name='odieresis', uni=0x00F6, hex='00F6', c='ö', w='o', bl='o', base='o', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ö O WITH DIAERESIS, LATIN SMALL LETTER'),
    'odotbelow': GD(name='odotbelow', uni=0x1ECD, hex='1ECD', c='ọ', w='o', bl='o', base='o', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ọ O WITH DOT BELOW, LATIN SMALL LETTER'),
    'oe': GD(name='oe', uni=0x0153, hex='0153', c='œ', l='o', r='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='œ SMALL LIGATURE OE, LATIN'),
    'ograve': GD(name='ograve', uni=0x00F2, hex='00F2', c='ò', l='o', r='o', base='o', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle','ogonek', 'top'], comment='ò O WITH GRAVE, LATIN SMALL LETTER'),
    'ohungarumlaut': GD(name='ohungarumlaut', uni=0x0151, hex='0151', c='ő', w='o', base='o', accents=['hungarumlautcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'omacron': GD(name='omacron', uni=0x014D, hex='014D', c='ō', l='o', r='o', base='o', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ō O WITH MACRON, LATIN SMALL LETTER'),
    'oopen': GD(name='oopen', uni=0x0254, hex='0254', c='ɔ', r2l='c', srcName='o', isLower=True, anchors=['dot'], comment='ɔ OPEN O, LATIN SMALL LETTER'),
    'oslash': GD(name='oslash', uni=0x00F8, hex='00F8', c='ø', base='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'oslash.alt': GD(name='oslash.alt', base='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'otilde': GD(name='otilde', uni=0x00F5, hex='00F5', c='õ', base='o', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='õ O WITH TILDE, LATIN SMALL LETTER'),
    'oogonek': GD(name='oogonek', uni=0x01EB, hex='01EB', c='ǫ', base='o', accents=['ogonekcmb'],  isLower=True, anchors=['top', 'middle', 'bottom']),

    'ogonekcmb': GD(name='ogonekcmb', uni=0x0328, hex='0328', c='̨', w=0, isLower=True, anchors=['_ogonek', 'bottom']),

    # p

    'p': GD(name='p', uni=0x0070, hex='0070', c='p', l='n', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='p'),
    'pdotaccent': GD(name='pdotaccent', uni=0x1E57, hex='1E57', c='ṗ', base='p', accents=['dotaccentcmb'], srcName='uni1E57', isLower=True, anchors=['bottom', 'middle', 'top']),

    # q

    'q': GD(name='q', uni=0x0071, hex='0071', c='q', l='o', r='off', # r='jdotless', # Only for Sans
        isLower=True, anchors=['bottom', 'middle', 'top'], comment='q'),

    'quotedbl': GD(name='quotedbl', uni=0x0022, hex='0022', c='"', l='quotesingle', r='quotesingle', isLower=True, comment='" quotation mark, neutral'),
    'quotedblbase': GD(name='quotedblbase', uni=0x201E, hex='201E', c='„', l='quotesingle', r='quotesingle', isLower=True, comment='„ quotation mark, low double comma'),
    'quotedblleft': GD(name='quotedblleft', uni=0x201C, hex='201C', c='“', l='quotesingle', r='quotesingle', isLower=True, comment='“ turned comma quotation mark, double'),
    'quotedblright': GD(name='quotedblright', uni=0x201D, hex='201D', c='”', l='quotesingle', r='quotesingle', isLower=True, comment='” RIGHT DOUBLE QUOTATION MARK'),
    'quotedblrightreversed': GD(name='quotedblrightreversed', uni=0x201F, hex='201F', c='‟', isLower=True),
    'quoteleft': GD(name='quoteleft', uni=0x2018, hex='2018', c='‘', l='quotesingle', r='quotesingle', isLower=True, comment='‘ turned comma quotation mark, single'),
    'quotereversed': GD(name='quotereversed', uni=0x201B, hex='201B', c='‛', l='quotesingle', r='quotesingle', isLower=True),
    'quoteright': GD(name='quoteright', uni=0x2019, hex='2019', c='’', l='quotesingle', r='quotesingle', isLower=True, comment='’ SINGLE QUOTATION MARK, RIGHT'),
    'quotesinglbase': GD(name='quotesinglbase', uni=0x201A, hex='201A', c='‚', l='quotesingle', r='quotesingle', isLower=True, comment='‚ SINGLE LOW-9 QUOTATION MARK'),
    'quotesingle': GD(name='quotesingle', uni=0x0027, hex='0027', c="'" , l2r='self', isLower=True, comment='" single quotation mark, neutral'),

    'minute': GD(name='minute', uni=0x2032, hex='2032', c='′', l='quotesingle', r='quotesingle', isLower=True, comment='′ PRIME'),
    'second': GD(name='second', uni=0x2033, hex='2033', c='″', l='quotesingle', r='quotesingle', isLower=True, comment='″ seconds'),

    # r

    'r': GD(name='r', uni=0x0072, hex='0072', c='r', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='r'),
    'racute': GD(name='racute', uni=0x0155, hex='0155', c='ŕ', l='r', r='r', rightMin='-100', base='r', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŕ R WITH ACUTE, LATIN SMALL LETTER'),
    'rcaron': GD(name='rcaron', uni=0x0159, hex='0159', c='ř', r='r', bl='r', rightMin='-100', base='r', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ř R WITH CARON, LATIN SMALL LETTER'),
    'rcommaaccent': GD(name='rcommaaccent', uni=0x0157, hex='0157', c='ŗ', w='r', rightMin='-100', base='r', accents=['cedillacmb.noconnect'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŗ R WITH CEDILLA, LATIN SMALL LETTER'),
    'rupeeIndian': GD(name='rupeeIndian', uni=0x20B9, hex='20B9', c='₹', srcName='Rupee'),

    # s

    's': GD(name='s', uni=0x0073, hex='0073', c='s', l2r='self', isLower=True, anchorTopX='TopX', anchorBottomX='BottomX', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='s'),
    'sacute': GD(name='sacute', uni=0x015B, hex='015B', c='ś', l='s', r='s', base='s', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ś S WITH ACUTE, LATIN SMALL LETTER'),
    'scaron': GD(name='scaron', uni=0x0161, hex='0161', c='š', l='s', r='s', base='s', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='š S WITH CARON, LATIN SMALL LETTER'),
    'scedilla': GD(name='scedilla', uni=0x015F, hex='015F', c='ş', l='s', r='s', base='s', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ş S WITH CEDILLA, LATIN SMALL LETTER'),
    'schwa': GD(name='schwa', uni=0x0259, hex='0259', c='ə', anchorTopX='TopX', base='eturned', srcName='uni0259', isLower=True, anchors=['top'], comment='ə SCHWA, LATIN SMALL LETTER'),
    'scircumflex': GD(name='scircumflex', uni=0x015D, hex='015D', c='ŝ', l='s', r='s', base='s', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŝ S WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'scommaaccent': GD(name='scommaaccent', uni=0x0219, hex='0219', c='ș', l='s', r='s', base='s', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ș S WITH COMMA BELOW, LATIN SMALL LETTER'),
    'sdotbelow': GD(name='sdotbelow', uni=0x1E63, hex='1E63', c='ṣ', l='s', r='s', base='s', accents=['dotbelowcmb'], srcName='uni1E63', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ṣ S WITH DOT BELOW, LATIN SMALL LETTER'),
    'strokeshortcmb': GD(name='strokeshortcmb', uni=0x0335, hex='0335', c='̵', w=0, isLower=True, anchors=['_middle', 'middle']),

    # t

    't': GD(name='t', uni=0x0074, hex='0074', c='t', isLower=True, anchorTopY='TopY', anchors=['bottom', 'middle', 'top', 'vert'], comment='t'),
    'tcaron': GD(name='tcaron', uni=0x0165, hex='0165', c='ť', anchorTopY='TopY', base='t', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ť T WITH CARON, LATIN SMALL LETTER'),
    'tcedilla': GD(name='tcedilla', uni=0x0163, hex='0163', c='ţ', anchorTopY='TopY', base='t', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ţ T WITH CEDILLA, LATIN SMALL LETTER'),
    'tcommaaccent': GD(name='tcommaaccent', uni=0x021B, hex='021B', c='ț', anchorTopY='TopY', base='t', accents=['cedillacmb.noconnect'], srcName='uni021B', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ț T WITH COMMA BELOW, LATIN SMALL LETTER'),
    'thorn': GD(name='thorn', uni=0x00FE, hex='00FE', c='þ', anchorTopY='TopY', isLower=True, comment='þ THORN, LATIN SMALL LETTER'),
    'tilde': GD(name='tilde', uni=0x02DC, hex='02DC', c='˜', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='tildecmb', isLower=True),

    # u

    'u': GD(name='u', uni=0x0075, hex='0075', c='u', l2r='n', r2l='n', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='u'),
    'uacute': GD(name='uacute', uni=0x00FA, hex='00FA', c='ú', l='u', r='u', base='u', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ú U WITH ACUTE, LATIN SMALL LETTER'),
    'ubreve': GD(name='ubreve', uni=0x016D, hex='016D', c='ŭ', l='u', r='u', base='u', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ŭ U WITH BREVE, LATIN SMALL LETTER'),
    'ucaron': GD(name='ucaron', uni=0x01D4, hex='01D4', c='ǔ', l='u', r='u', base='u', accents=['caroncmb'], srcName='uni01D4', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'ucircumflex': GD(name='ucircumflex', uni=0x00FB, hex='00FB', c='û', l='u', r='u', base='u', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='û U WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'udieresis': GD(name='udieresis', uni=0x00FC, hex='00FC', c='ü', l='u', r='u', base='u', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ü U WITH DIAERESIS, LATIN SMALL LETTER'),
    'udotbelow': GD(name='udotbelow', uni=0x1EE5, hex='1EE5', c='ụ', l='u', r='u', base='u', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ụ U WITH DOT BELOW, LATIN SMALL LETTER'),
    'ugrave': GD(name='ugrave', uni=0x00F9, hex='00F9', c='ù', l='u', r='u', base='u', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ù U WITH GRAVE, LATIN SMALL LETTER'),
    'uhungarumlaut': GD(name='uhungarumlaut', uni=0x0171, hex='0171', c='ű', l='u', w='u', base='u', accents=['hungarumlautcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ű U WITH DOUBLE ACUTE, LATIN SMALL LETTER'),
    'umacron': GD(name='umacron', uni=0x016B, hex='016B', c='ū', l='u', r='u', base='u', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ū U WITH MACRON, LATIN SMALL LETTER'),
    'uogonek': GD(name='uogonek', uni=0x0173, hex='0173', c='ų', w='u', bl='u', base='u', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ų U WITH OGONEK, LATIN SMALL LETTER'),
    'uring': GD(name='uring', uni=0x016F, hex='016F', c='ů', base='u', accents=['ringcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ů U WITH RING ABOVE, LATIN SMALL LETTER'),
    'utilde': GD(name='utilde', uni=0x0169, hex='0169', c='ũ', base='u', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ũ U WITH TILDE, LATIN SMALL LETTER'),

    # v

    'v': GD(name='v', uni=0x0076, hex='0076', c='v', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='v LATIN SMALL LETTER V'),
    'vturned': GD(name='vturned', uni=0x028C, hex='028C', c='ʌ', l2r='v', r2l='v', srcName='v', isLower=True),

    # w

    'w': GD(name='w', uni=0x0077, hex='0077', c='w', l='v', r='v', isLower=True, anchors=['bottom', 'middle', 'top'], comment='w LATIN SMALL LETTER W'),
    'wacute': GD(name='wacute', uni=0x1E83, hex='1E83', c='ẃ', l='w', r='w', base='w', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ẃ W WITH ACUTE, LATIN SMALL LETTER'),
    'wcircumflex': GD(name='wcircumflex', uni=0x0175, hex='0175', c='ŵ', l='w', r='w', base='w', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŵ W WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'wdieresis': GD(name='wdieresis', uni=0x1E85, hex='1E85', c='ẅ', l='w', r='w', base='w', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ẅ W WITH DIAERESIS, LATIN SMALL LETTER'),
    'wgrave': GD(name='wgrave', uni=0x1E81, hex='1E81', c='ẁ', l='w', r='w', base='w', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ẁ W WITH GRAVE, LATIN SMALL LETTER'),

    # x

    'x': GD(name='x', uni=0x0078, hex='0078', c='x', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='x LATIN SMALL LETTER X'),
    'xdieresis': GD(name='xdieresis', uni=0x1E8D, hex='1E8D', c='ẍ', l='x', r='x', base='x', accents=['dieresiscmb'], srcName='uni1E8D', isLower=True, anchors=['bottom', 'middle', 'top']),

    # y

    'y': GD(name='y', uni=0x0079, hex='0079', c='y', l='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='y LATIN SMALL LETTER Y'),
    'yacute': GD(name='yacute', uni=0x00FD, hex='00FD', c='ý', l='y', r='y', base='y', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ý Y WITH ACUTE, LATIN SMALL LETTER'),
    'ycircumflex': GD(name='ycircumflex', uni=0x0177, hex='0177', c='ŷ', l='y', r='y', base='y', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŷ Y WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'ydieresis': GD(name='ydieresis', uni=0x00FF, hex='00FF', c='ÿ', l='y', r='y', base='y', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ÿ Y WITH DIAERESIS, LATIN SMALL LETTER'),
    'ygrave': GD(name='ygrave', uni=0x1EF3, hex='1EF3', c='ỳ', l='y', r='y', base='y', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ỳ Y WITH GRAVE, LATIN SMALL LETTER'),
    'yhook': GD(name='yhook', uni=0x01B4, hex='01B4', c='ƴ', l='y', r='y', srcName='uni01B4', isLower=True, comment='ƴ Y WITH HOOK, LATIN SMALL LETTER'),
    'ymacron': GD(name='ymacron', uni=0x0233, hex='0233', c='ȳ', base='y', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'ytilde': GD(name='ytilde', uni=0x1EF9, hex='1EF9', c='ỹ', l='y', r='y', base='y', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ỹ Y WITH TILDE, LATIN SMALL LETTER'),

    # z

    'z': GD(name='z', uni=0x007A, hex='007A', c='z', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='z LATIN SMALL LETTER Z'),
    'zacute': GD(name='zacute', uni=0x017A, hex='017A', c='ź', l='z', r='z', base='z', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ź Z WITH ACUTE, LATIN SMALL LETTER'),
    'zcaron': GD(name='zcaron', uni=0x017E, hex='017E', c='ž', l='z', r='z', base='z', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ž Z WITH CARON, LATIN SMALL LETTER'),
    'zdotaccent': GD(name='zdotaccent', uni=0x017C, hex='017C', c='ż', l='z', r='z', base='z', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ż Z WITH DOT ABOVE, LATIN SMALL LETTER'),
    'zdotbelow': GD(name='zdotbelow', uni=0x1E93, hex='1E93', c='ẓ', l='z', r='z', base='z', accents=['dotbelowcmb'], srcName='uni1E93', isLower=True, anchors=['bottom', 'middle', 'top']),

    # Figures

    'zero': GD(g2='zero', g1='zero', l2r='self', uni=0x0030, c='0', name='zero', isLower=False, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
    'zeroslash': GD(g2='zero', g1='zero', l='zero', w='zero', name='zeroslash', base='zero', isLower=False, srcName='slash', comment='0 Digits, ASCII'),
    'one': GD(g2='one', g1='one', l2r='self', uni=0x0031, c='1', name='one', isLower=False, comment='1'),
    'two': GD(g2='two', g1='two', l2r='self', uni=0x0032, c='2', name='two', isLower=False, comment='2'),
    'three': GD(g2='three', g1='three', l2r='self', uni=0x0033, c='3', name='three', isLower=False, comment='3'),
    'four': GD(g2='four', g1='four', uni=0x0034, c='4', name='four', isLower=False, comment='4'),
    'five': GD(g2='five', g1='five', l2r='self', uni=0x0035, c='5', name='five', isLower=False, comment='5'),
    'six': GD(g2='six', g1='six',  l2r='self', uni=0x0036, c='6', name='six', isLower=False, comment='6'),
    'seven': GD(g2='seven', g1='seven', uni=0x0037, c='7', name='seven', isLower=False, comment='7'),
    'eight': GD(g2='eight', g1='eight', l2r='self', uni=0x0038, c='8', name='eight', isLower=False, comment='8'),
    'nine': GD(g2='nine', g1='nine', l2r='six', r2l='six', uni=0x0039, c='9', name='nine', isLower=False, comment='9'),

    # Diacritics

    'ringcmb': GD(name='ringcmb', uni=0x030A, hex='030A', anchorTopY='TopY', c='̊', w=0, isLower=True, anchors=['_top', 'top']),
    'ringcmb.uc': GD(name='ringcmb.uc', w=0, anchorTopY='TopY', srcName='ringcmb', isLower=True, anchors=['_top', 'top']),

    'hungarumlautcmb': GD(name='hungarumlautcmb', anchorTopY='TopY', uni=0x030B, hex='030B', c='̋', w=0, isLower=True, anchors=['top', '_top']),
    'hungarumlautcmb,uc': GD(name='hungarumlautcmb', anchorTopY='TopY', w=0, isLower=True, anchors=['top', '_top']),

    'tildecmb': GD(name='tildecmb', uni=0x0303, anchorTopY='TopY', hex='0303', c='̃', w=0, srcName='tilde', isLower=True, anchors=['_top', 'top']),
    'tildecmb.uc': GD(name='tildecmb.uc', w=0, anchorTopY='TopY', srcName='tildecmb', isLower=True, anchors=['_top', 'top']),

    'quoteleftcmb': GD(name='quoteright', srcName='quoteleft', w=0),
    'quoterightcmb': GD(name='quoterightcmb', srcName='quoteright', w=0),

    'cedillacmb': GD(name='cedillacmb', uni=0x0327, hex='0327', c='̧', w=0, isLower=True, anchors=['_bottom', 'bottom']),
    'cedillacmb.noconnect': GD(name='cedillacmb.noconnect', w=0, srcName='cedillacmb', isLower=True, anchors=['_bottom', 'bottom']),
    'caroncmb': GD(name='caroncmb', uni=0x030C, hex='030C', anchorTopY='TopY', c='̌', w=0, isLower=True, anchors=['_top', 'top']),
    'caroncmb.uc': GD(name='caroncmb.uc', w=0, anchorTopY='TopY', srcName='caroncmb', isLower=True, anchors=['_top', 'top']),
    'caroncmb.vert': GD(name='caroncmb.vert', l=GD.CAT_CENTER, w=0, base='commaaccentcmb', anchors=[AD._VERT]),
    'commaaccentcmb': GD(name='commaaccentcmb', uni=0x0326, anchorTopY='TopY', hex='0326', c='̦', w=0, isLower=True, anchors=['_bottom', 'bottom']),
    'commaaccentcmb.uc': GD(name='commaaccentcmb.uc', w=0, anchorTopY='TopY', srcName='commaaccentcmb', isLower=True, anchors=['_bottom', 'bottom']),
    'commaturnedabovecmb': GD(name='commaturnedabovecmb', anchorTopY='TopY', uni=0x0312, hex='0312', c='̒', w=0, isLower=True, anchors=['_top', 'top']),
    'commaturnedabovecmb.uc': GD(name='commaturnedabovecmb.uc', anchorTopY='TopY', w=0, srcName='commaturnedabovecmb', isLower=True, anchors=['_top', 'top']),
    'circumflex': GD(name='circumflex', uni=0x02C6, hex='02C6', c='ˆ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='circumflexcmb', isLower=True, comment='ˆ Legacy CIRCUMFLEX ACCENT, MODIFIER LETTER'),
    'circumflexcmb': GD(name='circumflexcmb', uni=0x0302, anchorTopY='TopY', hex='0302', c='̂', w=0, isLower=True, anchors=['_top', 'top']),
    'circumflexcmb.uc': GD(name='circumflexcmb.uc', w=0, anchorTopY='TopY', srcName='circumflexcmb', isLower=True, anchors=['_top', 'top']),
}

# Used by GlyphSet class to add small cap glyph data records. 
SC_NAMES = (
    'A', 'AE', 'AEacute', 'Aacute', 'Abreve', 'Acaron', 'Acircumflex', 'Adieresis', 'Adotbelow', 'Agrave', 'Amacron', 'Aogonek', 'Aring', 'Aringacute', 'Atilde', 
    'B', 'Bdotbelow', 'Bhook', 
    'C', 'Cacute', 'Ccaron', 'Ccedilla', 'Ccircumflex', 'Cdotaccent', 
    'D', 'Dcaron', 'Dcroat', 'Ddotbelow', 'Dhook', 
    'E', 'Eacute', 'Ebreve', 'Ecaron', 'Ecircumflex', 'Edieresis', 'Edotaccent', 'Edotbelow', 'Egrave', 'Emacron', 'Eng', 'Eogonek', 'Eopen', 'Ereversed', 'Eth', 'Etilde', 
    'F', 
    'G', 'Gbreve', 'Gcaron', 'Gcircumflex', 'Gcommaaccent', 'Gdotaccent', 'Germandbls', 'Gmacron', 
    'H', 'Hbar', 'Hcircumflex', 'Hdieresis', 'Hdotbelow', 
    'I', 'Iacute', 'Ibreve', 'Icaron', 'Icircumflex', 'Idieresis', 'Idotaccent', 'Idotbelow', 'Igrave', 'Imacron', 'Iogonek', 'Istroke', 'Itilde', 
    'J', 'Jcircumflex', 'IJ', 'J.base', 'Jcircumflex.base',
    'K', 'Kcommaaccent', 'Khook', 
    'L', 'Lacute', 'Lcaron', 'Lcommaaccent', 'Lslash', 'Ldot', 
    'M', 
    'N', 'Nacute', 'Ncaron', 'Ncommaaccent', 'Ndotaccent', 'Ndotbelow', 'Nhookleft', 'Ntilde', 
    'O', 'OE', 'Oacute', 'Obreve', 'Ocaron', 'Ocircumflex', 'Odieresis', 'Odotbelow', 'Ograve', 'Ohungarumlaut', 'Omacron', 'Oopen', 'Oslash', 'Oslash.alt', 'Otilde', 'Oslashacute', 'Oslashacute.alt', 
    'P', 'Pdotaccent', 
    'Q', 
    'R', 'Racute', 'Rcaron', 'Rcommaaccent', 
    'S', 'Sacute', 'Scaron', 'Scedilla', 'Schwa', 'Scircumflex', 'Scommaaccent', 'Sdotbelow', 
    'T', 'Tcaron', 'Tcedilla', 'Tcommaaccent', 'Thorn', 'Tbar',
    'U', 'Uacute', 'Ubreve', 'Ucaron', 'Ucircumflex', 'Udieresis', 'Udotbelow', 'Ugrave', 'Uhungarumlaut', 'Umacron', 'Uogonek', 'Uring', 'Utilde', 
    'V', 'Vturned', 
    'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 'Wgrave', 
    'X', 'Xdieresis', 
    'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ygrave', 'Yhook', 'Ymacron', 'Ytilde', 
    'Z', 'Zacute', 'Zcaron', 'Zdotaccent', 'Zdotbelow',
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'zeroslash', 'question', 
    'slash', 'Euro', 'degree', 'germandbls', 'yen', 'ampersand', 'questiondown', 'backslash', 'sterling', 'dollar', 'dollar.alt', 'bitcoin', 'bitcoin.alt',
    'parenleft', 'parenright', 'bracketleft', 'bracketright', 'exclam', 'exclamdown', 'braceleft', 'braceright',

    # In case CYRILLIC_SET is included, these need to become smallcaps too
    'A-cy', 'Abreve-cy', 'Adieresis-cy', 'Aie-cy', 'Be-cy', 'Che-cy', 'Cheabkhasian-cy', 'Chedescender-cy', 'Chedescenderabkhasian-cy', 'Chedieresis-cy', 
    'Chekhakassian-cy', 'Cheverticalstroke-cy', 'De-cy', 'Dje-cy', 'Dze-cy', 'Dzhe-cy', 'E-cy', 'Edieresis-cy', 'Ef-cy', 'Eiotified-cy', 'El-cy', 'Eltail-cy', 
    'Em-cy', 'Emtail-cy', 'En-cy', 'Endescender-cy', 'Enghe-cy', 'Enhook-cy', 'Entail-cy', 'Er-cy', 'Ereversed-cy', 'Ertick-cy', 'Es-cy', 'Esdescender-cy', 
    'Fita-cy', 'Ge-cy', 'Gedescender-cy', 'Gestrokehook-cy', 'Ghemiddlehook-cy', 'Ghestroke-cy', 'Gheupturn-cy', 'Gje-cy', 'Ha-cy', 'Haabkhasian-cy', 
    'Hadescender-cy', 'Hahook-cy', 'Hardsign-cy', 'Hastroke-cy', 'I-cy', 'Ia-cy', 'Idieresis-cy', 'Ie-cy', 'Iebreve-cy', 'Iegrave-cy', 'Ii-cy', 'Iigrave-cy', 
    'Iishort-cy', 'Iishorttail-cy', 'Imacron-cy', 'Io-cy', 'Iu-cy', 'Izhitsa-cy', 'Izhitsadblgrave-cy', 'Je-cy', 'Ka-cy', 'Kabashkir-cy', 'Kadescender-cy', 
    'Kahook-cy', 'Kastroke-cy', 'Kaverticalstroke-cy', 'Kje-cy', 'Koppa-cy', 'Ksi-cy', 'Lje-cy', 'Nje-cy', 'O-cy', 'Obarred-cy', 'Obarreddieresis-cy', 
    'Odieresis-cy', 'Omega-cy', 'Palochka-cy', 'Pe-cy', 'Pedescender-cy', 'Pemiddlehook-cy', 'Psi-cy', 'Schwa-cy', 'Schwadieresis-cy', 'Semisoftsign-cy', 
    'Sha-cy', 'Shcha-cy', 'Shha-cy', 'Softsign-cy', 'Te-cy', 'Tedescender-cy', 'Tetse-cy', 'Tse-cy', 'Tshe-cy', 'U-cy', 'Udieresis-cy', 'Uhungarumlaut-cy', 
    'Uk-cy', 'Umacron-cy', 'Ushort-cy', 'Ustrait-cy', 'Ustraitstroke-cy', 'Ve-cy', 'Yat-cy', 'Yeru-cy', 'Yerudieresis-cy', 'Yi-cy', 'Yusbig-cy', 'Yusbigiotified-cy', 
    'Yuslittle-cy', 'Yuslittleiotified-cy', 'Ze-cy', 'Zedescender-cy', 'Zedieresis-cy', 'Zhe-cy', 'Zhebreve-cy', 'Zhedescender-cy', 'Zhedieresis-cy',

    # In case GREEK_SET is inlcuded, these need to be come smallcaps too
    'Alpha', 'Alphatonos', 'Archaicsampi', 'Beta', 'Chi', 'Dei-coptic', 'Delta', 'Digamma', 'Epsilon', 'Epsilontonos', 'Eta', 'Etatonos', 'Fei-coptic', 
    'Gamma', 'Gangia-coptic', 'Heta', 'Hori-coptic', 'Iota', 'Iotadieresis', 'Iotatonos', 'KaiSymbol', 'Kappa', 'Khei-coptic', 'Koppa', 'KoppaArchaic', 
    'Lambda', 'Mu', 'Nu', 'Omega', 'Omegatonos', 'Omicron', 'Omicrontonos', 'Pamphyliandigamma', 'Phi', 'Pi', 'Psi', 'Rho', 'Sampi', 'San', 'Shei-coptic', 
    'Shima-coptic', 'Sho', 'Sigma', 'SigmaLunateDottedReversedSymbol', 'SigmaLunateDottedSymbol', 'SigmaLunateReversedSymbol', 'SigmaLunateSymbol', 
    'Stigma', 'Tau', 'Theta', 'ThetaSymbol', 'Upsilon', 'UpsilonacutehookSymbol', 'Upsilondieresis', 'UpsilondieresishookSymbol', 'UpsilonhookSymbol', 
    'Upsilontonos', 'Xi', 'Yot', 'Zeta',

)
# Used by GlyphSet class to add sinf/dnom/numr/subs glyph data records. 
# Alternative naming for letter glyphs: /amod and /ainferior
SUPS_SINF_NAMES = (
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'cent', 'cent.alt', 'dollar', 'dollar.alt', 'Euro', 'yen', 'sterling',
    'period', 'comma', 'colon', 'semicolon',
    'plus', 'minus', 'equal', 'notequal', 'less', 'greater', 'lessequal', 'greaterequal', 
    'multiply', 'divide', 'asterisk', 
    'percent', 'degree',
    'parenleft', 'parenright', 'bracketleft', 'bracketright',
    'quoteleft', 'quoteright', 'quotedblleft', 'quotedblright',
    'hyphen', 'endash'
)
# Used by GlyphSet class to add sinf/dnom/numr/subs glyph data records. These combine with /fraction
NUMR_DNOM_NAMES = (
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
)
# Used by GlyphSet class to add tab glyph data records. 
TAB_NAMES = (
    'zero', 'zeroslash', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'cent', 'cent.alt', 'dollar', 'dollar.alt', 'Euro', 'yen', 'sterling', 'bitcoin', 'bitcoin.alt', 
    'period', 'comma', 'colon', 'semicolon',
    'plus', 'minus', 'equal', 'notequal', 'less', 'greater', 'lessequal', 'greaterequal', 
    'multiply', 'divide', 'asterisk', 
    'percent', 'perthousand', 'degree', 'approxequal', 'plusminus',  
    'parenleft', 'parenright', 'bracketleft', 'bracketright', 'braceleft', 'braceright',
    'quoteleft', 'quoteright', 'quotedblleft', 'quotedblright',
    'hyphen', 'endash', 'minute', 'second', 'slash', 'backslash', 'numbersign',
)
# Used by GlyphSet class to add oldstyle figures glyph data records with .onum extension
ONUM_NAMES = (
    'zero', 'zeroslash', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'zero.tab', 'zeroslash.tab', 'one.tab', 'two.tab', 'three.tab', 'four.tab', 'five.tab', 'six.tab', 'seven.tab', 'eight.tab', 'nine.tab',

)

if __name__ == '__main__':
    for gName, gd in GDS.items():
        #print('---', gd)
        if gd.base and gd.base not in GDS:
            print('##### Missing base', gName, gd.base)
        for aName in gd.accents:
            if aName not in GDS:
                print('#### Missing accent', gName, aName)


for gName, gd in GDS.items():
    if len(gd.accents) >= 2:
        print(gName, gd.accents)

