# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_A_set.py
#    From https://foundrysupport.monotype.com/hc/en-us/articles/360029280752-Recommended-Character-Set:
#
#    Latin A “Ascii” 
#    The following character set contains 186 glyphs and is our recommended minimum for Latin-based display fonts. 
#    This is the character set used by our font validator in Foundry Platform. 
#    Please note that this limited character set supports a few major Western languages only. 
#    We encourage you to add additional characters and language support.
#
#    Latin “Ascii” (Smallest set accorting to Monotype)
#    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789¹²³ªº
#    %$€¥£¢&*@#|áâàäåãæçéêèëíîìïıñóôòöõøœšßúûùüýÿžÂÀÄÅÃÆÇÉÊÈËÍÎÌÏÑÓÔÒÖÕØŒŠÛÙÜÝŸ
#    ,:;-–—•.…“‘’‘ ‚ “”„‹›«»/\?!¿¡()[]{}©®§+×=_°
#
from copy import deepcopy

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

LATIN_A_SET_NAME = 'Latin A'
LATIN_A_SET_NAME_ITALIC = 'Latin A Italic'

# The "c" attribtes are redundant, if the @uni or @hex are defined, but they are offer easy searching in the source by char.
LATIN_A_SET = GDS = {

    '.notdef': GD(name='.notdef'),
    '.null': GD(name='.null', uni=0x0000, hex='0000'),
    'uni000D': GD(name='uni000D', uni=0x000D, hex='000D'),
    'uni00A0': GD(name='uni00A0', uni=0x00A0, hex='00A0', w=GD.CAT_SPACE_WIDTH, c=' ', srcName='nonbreakingspace', isLower=False, comment='  Symbols, Latin-1 Punctuation and'),
    'space': GD(name='space', uni=0x0020, hex='0020', w=GD.CAT_SPACE_WIDTH, c=' ', isLower=False, comment='  Symbols, ASCII Punctuation and'),
    'emspace': GD(name='emspace', uni=0x2003, hex='2003', w=GD.CAT_EM_WIDTH, c=' ', isLower=False),
    'enspace': GD(name='enspace', uni=0x2002, hex='2002', w=GD.CAT_EN_WIDTH, c=' ', isLower=False),
    'figurespace': GD(name='figurespace', uni=0x2007, w=GD.CAT_FIGURE_WIDTH, hex='2007', c=' ', isLower=False),
    'hairspace': GD(name='hairspace', uni=0x200A, hex='200A', w=GD.CAT_HAIR_WIDTH, c=' ', isLower=False),
    'spacemarker': GD(name='spacemarker', w=0),
    'narrownbspace': GD(name='narrownbspace', uni=0x202F, w=GD.CAT_HAIR_WIDTH, hex='202F', c=' ', isLower=False),
    'space.tab': GD(name='narrownbspace', w=GD.CAT_TAB_WIDTH, c=' ', isLower=False),
    'apple': GD(name='apple', l=48, r=48, hex='F8FF', uni=0xF8FF, c='', isLower=False), # Logo TYPETR

    'colon': GD(name='colon', uni=0x003A, hex='003A', c=':', l='period', r='period', isLower=True, comment=': COLON'),
    'cent': GD(name='cent', uni=0x00A2, hex='00A2', c='¢', l='center', w='mathWidth', isLower=True, comment='¢ CENT SIGN'),
    'comma': GD(name='comma', uni=0x002C, hex='002C', c=',', l='off', isLower=True, comment=', separator, decimal'),
    'copyright': GD(name='copyright', uni=0x00A9, hex='00A9', c='©', l='O', r='O', base='largecircle', isLower=True, comment='© COPYRIGHT SIGN'),
    'exclam': GD(name='exclam', uni=0x0021, hex='0021', c='!', l2r='self', isLower=True, comment='! factorial'),
    'exclamdown': GD(name='exclamdown', uni=0x00A1, hex='00A1', c='¡', l2r='exclam', r2l='exclam', isLower=True, comment='¡ INVERTED EXCLAMATION MARK'),
    'hyphen': GD(name='hyphen', uni=0x002D, hex='002D', c='-', l2r='self', isLower=True, comment='- minus sign, hyphen'),
    'endash': GD(name='endash', uni=0x2013, hex='2013', c='–', l='center', w='emWidth/2', isLower=True, comment='– EN DASH'),
    'emdash': GD(name='emdash', uni=0x2014, hex='2014', c='—', l='center', w='emWidth', g1='hyphen', g2='hyphen', isLower=True, comment='— EM DASH'),
    'parenleft': GD(name='parenleft', uni=0x0028, hex='0028', c='(', isLower=True, comment='( parenthesis, opening'),
    'parenright': GD(name='parenright', uni=0x0029, hex='0029', c=')', l2r='parenleft', r2l='parenleft', isLower=True, comment=') RIGHT PARENTHESIS'),
    'percent': GD(name='percent', uni=0x0025, hex='0025', c='%', l='zerosuperior', r='zerosuperior', isLower=True, overshoot="superiorOvershoot", height="supsHeight", baseline="numrBaseline", comment='% PERCENT SIGN'),
    'period': GD(name='period', uni=0x002E, hex='002E', c='.', l2r='self', isLower=True, fixSpacing=False, comment='. point, decimal'),
    'ellipsis': GD(name='ellipsis', uni=0x2026, hex='2026', c='…', l='period', r='period', isLower=True, comment='… three dot leader'),
    'question': GD(name='question', uni=0x003F, hex='003F', c='?', isLower=True, comment='? QUESTION MARK'),
    'questiondown': GD(name='questiondown', uni=0x00BF, hex='00BF', c='¿', l2r='question', r2l='question', isLower=True, comment='¿ turned question mark'),
    'registered': GD(name='registered', uni=0x00AE, hex='00AE', c='®', l='copyright', r='copyright', base='largecircle', isLower=True, comment='® trade mark sign, registered'),
    'section': GD(name='section', uni=0x00A7, hex='00A7', c='§', l='s', r='s', isLower=True, comment='§ SECTION SIGN'),
    'semicolon': GD(name='semicolon', uni=0x003B, hex='003B', c=';', l='comma', r='comma', isLower=True, comment='; SEMICOLON'),
    'slash': GD(name='slash', uni=0x002F, hex='002F', c='/', l2r='self', comment='/ virgule'),
    'sterling': GD(name='sterling', uni=0x00A3, hex='00A3', c='£', l='center', w='mathWidth', isLower=True, comment='£ sterling, pound'),
    'underscore': GD(name='underscore', uni=0x005F, hex='005F', c='_', isLower=True, comment='_ underscore, spacing'),
    'onesuperior': GD(name='onesuperior', uni=0x00B9, hex='00B9', c='¹', l='plussuperior', r='plussuperior', isLower=True, comment='¹ SUPERSCRIPT ONE'),
    'twosuperior': GD(name='twosuperior', uni=0x00B2, hex='00B2', c='²', l='plussuperior', r='plussuperior', comment='² TWO, SUPERSCRIPT'),
    'threesuperior': GD(name='threesuperior', uni=0x00B3, hex='00B3', c='³', l='plussuperior', r='plussuperior', comment='³ THREE, SUPERSCRIPT'),
    'numbersign': GD(name='numbersign', uni=0x0023, hex='0023', c='#', l2r='self', isLower=True, comment='# pound sign'),
    'degree': GD(name='degree', uni=0x00B0, hex='00B0', c='°', isLower=True, comment='° DEGREE SIGN'),
    'ordfeminine': GD(name='ordfeminine', uni=0x00AA, hex='00AA', c='ª', isLower=True, comment='ª ORDINAL INDICATOR, FEMININE'),
    'ordmasculine': GD(name='ordmasculine', uni=0x00BA, hex='00BA', c='º', isLower=True, comment='º ORDINAL INDICATOR, MASCULINE'),
    'plus': GD(name='plus', uni=0x002B, hex='002B', c='+', l='center', w='mathWidth', isLower=True, comment='+ PLUS SIGN'),
    'multiply': GD(name='multiply', uni=0x00D7, hex='00D7', c='×', l='center', w='mathWidth', isLower=True, comment='× product, cartesian'),
    'equal': GD(name='equal', uni=0x003D, hex='003D', c='=', l='center', w='mathWidth', isLower=True, comment='= EQUALS SIGN'),
    'dollar': GD(name='dollar', uni=0x0024, hex='0024', c='$', l='center', w='mathWidth', base='S', comment='$ milreis'),
    'yen': GD(name='yen', uni=0x00A5, hex='00A5', c='¥', l='center', w='mathWidth', isLower=True, comment='¥ yuan sign'),
    'A': GD(name='A', uni=0x0041, hex='0041', c='A', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='A Uppercase Alphabet, Latin'),
    'AE': GD(name='AE', uni=0x00C6, hex='00C6', c='Æ', l='A', r='E', anchors=['bottom', 'middle', 'top'], comment='Æ ligature ae, latin capital'),
    'Acircumflex': GD(name='Acircumflex', uni=0x00C2, hex='00C2', c='Â', l='A', r='A', base='A', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Adieresis': GD(name='Adieresis', uni=0x00C4, hex='00C4', c='Ä', l='A', r='A', base='A', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Agrave': GD(name='Agrave', uni=0x00C0, hex='00C0', c='À', l='A', r='A', base='A', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
    'Atilde': GD(name='Atilde', uni=0x00C3, hex='00C3', c='Ã', l='A', r='A', base='A', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ã A WITH TILDE, LATIN CAPITAL LETTER'),
    'Aring': GD(name='Aring', uni=0x00C5, hex='00C5', c='Å', l='A', r='A', base='A', accents=['ringcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Å RING ABOVE, LATIN CAPITAL LETTER A WITH'),
    'B': GD(name='B', uni=0x0042, hex='0042', c='B', l='H', anchors=['bottom', 'middle', 'top'], comment='B LATIN CAPITAL LETTER B'),
    'C': GD(name='C', uni=0x0043, hex='0043', c='C', l='O', anchors=['bottom', 'dot', 'middle', 'top'], comment='C LATIN CAPITAL LETTER C'),
    'Ccedilla': GD(name='Ccedilla', uni=0x00C7, hex='00C7', c='Ç', l='O', r='C', base='C', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ç CEDILLA, LATIN CAPITAL LETTER C WITH'),
    'D': GD(name='D', uni=0x0044, hex='0044', c='D', l='H', r='O', anchors=['bottom', 'middle', 'top'], comment='D'),
    'E': GD(name='E', uni=0x0045, hex='0045', c='E', l='H', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='E'),
    'Eacute': GD(name='Eacute', uni=0x00C9, hex='00C9', c='É', l='H', r='E', base='E', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='É E WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ecircumflex': GD(name='Ecircumflex', uni=0x00CA, hex='00CA', c='Ê', l='H', r='E', base='E', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ê E WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Edieresis': GD(name='Edieresis', uni=0x00CB, hex='00CB', c='Ë', l='H', r='E', base='E', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ë E WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Egrave': GD(name='Egrave', uni=0x00C8, hex='00C8', c='È', l='H', r='E', base='E', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='È E WITH GRAVE, LATIN CAPITAL LETTER'),
    'Euro': GD(name='Euro', uni=0x20AC, hex='20AC', c='€', l='center', w='mathWidth', g1='C', srcName='C'),
    'F': GD(name='F', uni=0x0046, hex='0046', c='F', l='H', anchors=['bottom', 'middle', 'top'], comment='F'),
    'G': GD(name='G', uni=0x0047, hex='0047', c='G', l='O', anchors=['bottom', 'middle', 'top'], comment='G'),
    'H': GD(name='H', uni=0x0048, hex='0048', c='H', l2r='self', anchors=['bottom', 'middle', 'top', 'topleft'], comment='H'),
    'I': GD(name='I', uni=0x0049, hex='0049', c='I', l='H', r='H', srcName='H', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='I'),
    'Iacute': GD(name='Iacute', uni=0x00CD, hex='00CD', c='Í', w='I', bl='I', base='I', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
    'Icircumflex': GD(name='Icircumflex', uni=0x00CE, hex='00CE', c='Î', w='I', bl='I', base='I', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Idieresis': GD(name='Idieresis', uni=0x00CF, hex='00CF', c='Ï', w='I', bl='I', base='I', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Igrave': GD(name='Igrave', uni=0x00CC, hex='00CC', c='Ì', w='I', bl='I', base='I', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
    'J': GD(name='J', uni=0x004A, hex='004A', c='J', anchors=['bottom', 'middle', 'top'], comment='J'),
    'K': GD(name='K', uni=0x004B, hex='004B', c='K', l='H', anchors=['bottom', 'middle', 'top'], comment='K'),
    'L': GD(name='L', uni=0x004C, hex='004C', c='L', l='H', anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='L'),
    'M': GD(name='M', uni=0x004D, hex='004D', c='M', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='M'),
    'N': GD(name='N', uni=0x004E, hex='004E', c='N', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='N'),
    'Ntilde': GD(name='Ntilde', uni=0x00D1, hex='00D1', c='Ñ', l='H', r='H', base='N', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ñ N WITH TILDE, LATIN CAPITAL LETTER'),
    'O': GD(name='O', uni=0x004F, hex='004F', c='O', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='O'),
    'OE': GD(name='OE', uni=0x0152, hex='0152', c='Œ', l='O', r='E', anchors=['bottom', 'middle', 'top'], comment='Œ'),
    'Oacute': GD(name='Oacute', uni=0x00D3, hex='00D3', c='Ó', l='O', r='O', base='O', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ocircumflex': GD(name='Ocircumflex', uni=0x00D4, hex='00D4', c='Ô', l='O', r='O', base='O', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Odieresis': GD(name='Odieresis', uni=0x00D6, hex='00D6', c='Ö', l='O', r='O', base='O', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ograve': GD(name='Ograve', uni=0x00D2, hex='00D2', c='Ò', l='O', r='O', base='O', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
    'Oslash': GD(name='Oslash', uni=0x00D8, hex='00D8', c='Ø', l='O', w='O', srcName='O', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Otilde': GD(name='Otilde', uni=0x00D5, hex='00D5', c='Õ', l='O', r='O', base='O', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),
    'P': GD(name='P', uni=0x0050, hex='0050', c='P', l='H', anchors=['bottom', 'middle', 'top', 'topleft'], comment='P'),
    'Q': GD(name='Q', uni=0x0051, hex='0051', c='Q', l='O', w='O', anchors=['bottom', 'middle', 'top'], comment='Q'),
    'R': GD(name='R', uni=0x0052, hex='0052', c='R', bl='H', anchors=['bottom', 'middle', 'top'], comment='R'),
    'S': GD(name='S', uni=0x0053, hex='0053', c='S', l2r='self', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='S'),
    'Scaron': GD(name='Scaron', uni=0x0160, hex='0160', c='Š', l='S', w='S', base='S', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Š'),
    'T': GD(name='T', uni=0x0054, hex='0054', c='T', l2r='self', anchors=['bottom', 'middle', 'top'], comment='T'),
    'U': GD(name='U', uni=0x0055, hex='0055', c='U', l='off', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='U'),
    'Ucircumflex': GD(name='Ucircumflex', uni=0x00DB, hex='00DB', c='Û', l='U', r='U', base='U', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Û U WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Udieresis': GD(name='Udieresis', uni=0x00DC, hex='00DC', c='Ü', l='U', r='U', base='U', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ü U WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ugrave': GD(name='Ugrave', uni=0x00D9, hex='00D9', c='Ù', l='U', r='U', base='U', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ù U WITH GRAVE, LATIN CAPITAL LETTER'),
    'V': GD(name='V', uni=0x0056, hex='0056', c='V', l='A', r='A', anchors=['bottom', 'middle', 'top'], comment='V'),
    'W': GD(name='W', uni=0x0057, hex='0057', c='W', l='V', r='V', anchors=['bottom', 'middle', 'top'], comment='W'),
    'X': GD(name='X', uni=0x0058, hex='0058', c='X', l2r='self', anchors=['bottom', 'middle', 'top'], comment='X'),
    'Y': GD(name='Y', uni=0x0059, hex='0059', c='Y', l2r='self', anchors=['bottom', 'middle', 'top', 'topleft'], comment='Y'),
    'Yacute': GD(name='Yacute', uni=0x00DD, hex='00DD', c='Ý', l='Y', r='Y', base='Y', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ý Y WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ydieresis': GD(name='Ydieresis', uni=0x0178, hex='0178', c='Ÿ', l='Y', r='Y', base='Y', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ÿ Y WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Z': GD(name='Z', uni=0x005A, hex='005A', c='Z', l2r='self', anchors=['bottom', 'middle', 'top'], comment='Z'),
    'a': GD(name='a', uni=0x0061, hex='0061', c='a', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='a Small Letters, Latin'),
    'aacute': GD(name='aacute', uni=0x00E1, hex='00E1', c='á', w='a', bl='a', base='a', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='á A WITH ACUTE, LATIN SMALL LETTER'),
    'acircumflex': GD(name='acircumflex', uni=0x00E2, hex='00E2', c='â', w='a', bl='a', base='a', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='â A WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'adieresis': GD(name='adieresis', uni=0x00E4, hex='00E4', c='ä', w='a', bl='a', base='a', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ä A WITH DIAERESIS, LATIN SMALL LETTER'),
    'ae': GD(name='ae', uni=0x00E6, hex='00E6', c='æ', l='a', r='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='æ small ligature ae, latin'),
    'agrave': GD(name='agrave', uni=0x00E0, hex='00E0', c='à', w='a', bl='a', base='a', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='à A WITH GRAVE, LATIN SMALL LETTER'),
    'aring': GD(name='aring', uni=0x00E5, hex='00E5', c='å', base='a', accents=['ringcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='å RING ABOVE, LATIN SMALL LETTER A WITH'),
    'atilde': GD(name='atilde', uni=0x00E3, hex='00E3', c='ã', base='a', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ã A WITH TILDE, LATIN SMALL LETTER'),
    'ampersand': GD(name='ampersand', uni=0x0026, hex='0026', c='&', l='off', r='t', comment='& AMPERSAND'),
    'asterisk': GD(name='asterisk', uni=0x002A, hex='002A', c='*', l2r='self', isLower=True, comment='* star'),
    'at': GD(name='at', uni=0x0040, hex='0040', c='@', l='O', l2r='self', isLower=True, comment='@ COMMERCIAL AT'),
    'b': GD(name='b', uni=0x0062, hex='0062', c='b', l='off', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='b'),
    'backslash': GD(name='backslash', uni=0x005C, hex='005C', c="\\" , l2r='self', isLower=True, comment='\\ SOLIDUS, REVERSE'),
    'bar': GD(name='bar', uni=0x007C, hex='007C', c='|', l='bracketleft', r='bracketright', isLower=True, comment='| VERTICAL LINE'),
    'braceleft': GD(name='braceleft', uni=0x007B, hex='007B', c='{', isLower=True, comment='{ opening curly bracket'),
    'braceright': GD(name='braceright', uni=0x007D, hex='007D', c='}', l2r='braceleft', r2l='braceleft', isLower=True, comment='} RIGHT CURLY BRACKET'),
    'bracketleft': GD(name='bracketleft', uni=0x005B, hex='005B', c='[', isLower=True, comment='[ square bracket, opening'),
    'bracketright': GD(name='bracketright', uni=0x005D, hex='005D', c=']', l2r='bracketleft', r2l='bracketleft', isLower=True, comment='] SQUARE BRACKET, RIGHT'),
    'bullet': GD(name='bullet', uni=0x2022, hex='2022', c='•', l2r='self', isLower=True, comment='• small circle, black'),
    'c': GD(name='c', uni=0x0063, hex='0063', c='c', isLower=True, anchors=['bottom', 'dot', 'middle', 'top'], comment='c'),
    'ccedilla': GD(name='ccedilla', uni=0x00E7, hex='00E7', c='ç', base='c', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ç CEDILLA, LATIN SMALL LETTER C WITH'),
    'd': GD(name='d', uni=0x0064, hex='0064', c='d', isLower=True, anchors=['bottom', 'middle', 'top', 'vert'], comment='d'),
    'e': GD(name='e', uni=0x0065, hex='0065', c='e', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='e'),
    'eacute': GD(name='eacute', uni=0x00E9, hex='00E9', c='é', base='e', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='é E WITH ACUTE, LATIN SMALL LETTER'),
    'ecircumflex': GD(name='ecircumflex', uni=0x00EA, hex='00EA', c='ê', base='e', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ê E WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'edieresis': GD(name='edieresis', uni=0x00EB, hex='00EB', c='ë', w='e', base='e', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ë E WITH DIAERESIS, LATIN SMALL LETTER'),
    'egrave': GD(name='egrave', uni=0x00E8, hex='00E8', c='è', w='e', bl='e', base='e', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='è E WITH GRAVE, LATIN SMALL LETTER'),
    'f': GD(name='f', uni=0x0066, hex='0066', c='f', l='t', rightMin='-100', isLower=True, anchors=['bottom', 'middle', 'top'], comment='f'),
    'g': GD(name='g', uni=0x0067, hex='0067', c='g', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g'),
    'germandbls': GD(name='germandbls', uni=0x00DF, hex='00DF', c='ß', l='f', r='s', isLower=True, comment='ß SHARP S, LATIN SMALL LETTER'),
    'guillemotleft': GD(name='guillemotleft', uni=0x00AB, hex='00AB', c='«', l2r='self', isLower=True),
    'guillemotright': GD(name='guillemotright', uni=0x00BB, hex='00BB', c='»', l='guillemotleft', r='guillemotleft', isLower=True),
    'guilsinglleft': GD(name='guilsinglleft', uni=0x2039, hex='2039', c='‹', l='guillemotleft', r='guillemotleft', isLower=True, comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglright': GD(name='guilsinglright', uni=0x203A, hex='203A', c='›', l='guillemotleft', r='guillemotleft', isLower=True, comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK'),
    'h': GD(name='h', uni=0x0068, hex='0068', c='h', isLower=True, anchors=['bottom', 'dot', 'middle', 'top'], comment='h'),
    'i': GD(name='i', uni=0x0069, hex='0069', c='i', l='n', r='idotless', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='i'),
    'idotless': GD(name='idotless', uni=0x0131, hex='0131', c='ı', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'iacute': GD(name='iacute', uni=0x00ED, hex='00ED', c='í', w='i', bl='idotless', base='idotless', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='í I WITH ACUTE, LATIN SMALL LETTER'),
    'icircumflex': GD(name='icircumflex', uni=0x00EE, hex='00EE', c='î', w='i', bl='idotless', base='idotless', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='î I WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'idieresis': GD(name='idieresis', uni=0x00EF, hex='00EF', c='ï', w='i', bl='idotless', base='idotless', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ï I WITH DIAERESIS, LATIN SMALL LETTER'),
    'igrave': GD(name='igrave', uni=0x00EC, hex='00EC', c='ì', w='i', bl='idotless', base='idotless', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ì I WITH GRAVE, LATIN SMALL LETTER'),
    'j': GD(name='j', uni=0x006A, hex='006A', c='j', l='off', r='off', isLower=True, anchors=['bottom', 'middle'], comment='j'),
    'k': GD(name='k', uni=0x006B, hex='006B', c='k', l='h', r='x', isLower=True, anchors=['bottom', 'middle', 'top'], comment='k'),
    'l': GD(name='l', uni=0x006C, hex='006C', c='l', l='h', r='idotless', isLower=True, anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='l'),
    'm': GD(name='m', uni=0x006D, hex='006D', c='m', l='n', r='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='m'),
    'n': GD(name='n', uni=0x006E, hex='006E', c='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='n'),
    'ntilde': GD(name='ntilde', uni=0x00F1, hex='00F1', c='ñ', base='n', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ñ N WITH TILDE, LATIN SMALL LETTER'),
    'o': GD(name='o', uni=0x006F, hex='006F', c='o', l2r='self', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='o'),
    'oacute': GD(name='oacute', uni=0x00F3, hex='00F3', c='ó', l='o', r='o', base='o', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ó O WITH ACUTE, LATIN SMALL LETTER'),
    'ocircumflex': GD(name='ocircumflex', uni=0x00F4, hex='00F4', c='ô', w='o', bl='o', base='o', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ô O WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'odieresis': GD(name='odieresis', uni=0x00F6, hex='00F6', c='ö', w='o', bl='o', base='o', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ö O WITH DIAERESIS, LATIN SMALL LETTER'),
    'oe': GD(name='oe', uni=0x0153, hex='0153', c='œ', l='o', r='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='œ SMALL LIGATURE OE, LATIN'),
    'ograve': GD(name='ograve', uni=0x00F2, hex='00F2', c='ò', l='o', r='o', base='o', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ò O WITH GRAVE, LATIN SMALL LETTER'),
    'oslash': GD(name='oslash', uni=0x00F8, hex='00F8', c='ø', l2r='o', srcName='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'otilde': GD(name='otilde', uni=0x00F5, hex='00F5', c='õ', base='o', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='õ O WITH TILDE, LATIN SMALL LETTER'),
    'p': GD(name='p', uni=0x0070, hex='0070', c='p', l='n', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='p'),
    'q': GD(name='q', uni=0x0071, hex='0071', c='q', l='o', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='q'),
    'quotedblbase': GD(name='quotedblbase', uni=0x201E, hex='201E', c='„', l='quotesingle', r='quotesingle', isLower=True, comment='„ quotation mark, low double comma'),
    'quotedblleft': GD(name='quotedblleft', uni=0x201C, hex='201C', c='“', l='quotesingle', r='quotesingle', isLower=True, comment='“ turned comma quotation mark, double'),
    'quotedblright': GD(name='quotedblright', uni=0x201D, hex='201D', c='”', l='quotesingle', r='quotesingle', isLower=True, comment='” RIGHT DOUBLE QUOTATION MARK'),
    'quoteleft': GD(name='quoteleft', uni=0x2018, hex='2018', c='‘', l='quotesingle', r='quotesingle', isLower=True, comment='‘ turned comma quotation mark, single'),
    'quoteright': GD(name='quoteright', uni=0x2019, hex='2019', c='’', l='quotesingle', r='quotesingle', isLower=True, comment='’ SINGLE QUOTATION MARK, RIGHT'),
    'quotesinglbase': GD(name='quotesinglbase', uni=0x201A, hex='201A', c='‚', l='quotesingle', r='quotesingle', isLower=True, comment='‚ SINGLE LOW-9 QUOTATION MARK'),
    'r': GD(name='r', uni=0x0072, hex='0072', c='r', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='r'),
    's': GD(name='s', uni=0x0073, hex='0073', c='s', l='off', l2r='self', isLower=True, useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='s'),
    'scaron': GD(name='scaron', uni=0x0161, hex='0161', c='š', l='s', r='s', base='s', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='š S WITH CARON, LATIN SMALL LETTER'),
    't': GD(name='t', uni=0x0074, hex='0074', c='t', l='off', r='off', isLower=True, anchors=['bottom', 'middle', 'top', 'vert'], comment='t'),
    'u': GD(name='u', uni=0x0075, hex='0075', c='u', l2r='n', r2l='n', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='u'),
    'uacute': GD(name='uacute', uni=0x00FA, hex='00FA', c='ú', l='u', r='u', base='u', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ú U WITH ACUTE, LATIN SMALL LETTER'),
    'ucircumflex': GD(name='ucircumflex', uni=0x00FB, hex='00FB', c='û', l='u', r='u', base='u', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='û U WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'udieresis': GD(name='udieresis', uni=0x00FC, hex='00FC', c='ü', l='u', r='u', base='u', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ü U WITH DIAERESIS, LATIN SMALL LETTER'),
    'ugrave': GD(name='ugrave', uni=0x00F9, hex='00F9', c='ù', l='u', r='u', base='u', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ù U WITH GRAVE, LATIN SMALL LETTER'),
    'v': GD(name='v', uni=0x0076, hex='0076', c='v', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='v LATIN SMALL LETTER V'),
    'w': GD(name='w', uni=0x0077, hex='0077', c='w', l='v', r='v', isLower=True, anchors=['bottom', 'middle', 'top'], comment='w LATIN SMALL LETTER W'),
    'x': GD(name='x', uni=0x0078, hex='0078', c='x', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='x LATIN SMALL LETTER X'),
    'y': GD(name='y', uni=0x0079, hex='0079', c='y', l='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='y LATIN SMALL LETTER Y'),
    'yacute': GD(name='yacute', uni=0x00FD, hex='00FD', c='ý', l='y', r='y', base='y', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ý Y WITH ACUTE, LATIN SMALL LETTER'),
    'ydieresis': GD(name='ydieresis', uni=0x00FF, hex='00FF', c='ÿ', l='y', r='y', base='y', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ÿ Y WITH DIAERESIS, LATIN SMALL LETTER'),
    'z': GD(name='z', uni=0x007A, hex='007A', c='z', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='z LATIN SMALL LETTER Z'),
    'zcaron': GD(name='zcaron', uni=0x017E, hex='017E', c='ž', l='z', r='z', base='z', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ž Z WITH CARON, LATIN SMALL LETTER'),
    'zero': GD(name='zero', uni=0x0030, hex='0030', c='0', l2r='self', useSkewRotate=True, comment='0 Digits, ASCII'),
    'one': GD(name='one', uni=0x0031, hex='0031', c='1', l2r='self', comment='1'),
    'two': GD(name='two', uni=0x0032, hex='0032', c='2', l2r='self', comment='2'),
    'three': GD(name='three', uni=0x0033, hex='0033', c='3', r='B', comment='3'),
    'four': GD(name='four', uni=0x0034, hex='0034', c='4', comment='4'),
    'five': GD(name='five', uni=0x0035, hex='0035', c='5', l='off', r='off', comment='5'),
    'six': GD(name='six', uni=0x0036, hex='0036', c='6', l2r='self', comment='6'),
    'seven': GD(name='seven', uni=0x0037, hex='0037', c='7', comment='7'),
    'eight': GD(name='eight', uni=0x0038, hex='0038', c='8', l2r='self', comment='8'),
    'nine': GD(name='nine', uni=0x0039, hex='0039', c='9', l2r='six', r2l='six', comment='9'),

    # Supporting components and diacritics
    'largecircle': GD(l='O', r='O', uni=0x25ef, c='◯', name='largecircle', comment='circle for ® trade mark sign, registered', useSkewRotate=True, addItalicExtremePoints=True),
    'gravecmb': GD(name='gravecmb', uni=0x0300, hex='0300', c='̀', anchorTopY='TopY', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'gravecmb.uc': GD(name='gravecmb.uc', w=0, anchorTopY='TopY', srcName='gravecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'acutecmb': GD(name='acutecmb', uni=0x0301, anchorTopY='TopY', hex='0301', c='́', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'acutecmb.uc': GD(name='acutecmb.uc', w=0, anchorTopY='TopY', isLower=False, srcName='acutecmb', autoFixComponentPositions=False, autoFixMargins=False, anchors=['_top', 'top']),
    'tildecmb': GD(name='tildecmb', uni=0x0303, anchorTopY='TopY', hex='0303', c='̃', w=0, srcName='tilde', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'tildecmb.uc': GD(name='tildecmb.uc', w=0, anchorTopY='TopY', srcName='tildecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'circumflexcmb': GD(name='circumflexcmb', uni=0x0302, anchorTopY='TopY', hex='0302', c='̂', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'circumflexcmb.uc': GD(name='circumflexcmb.uc', w=0, anchorTopY='TopY', srcName='circumflexcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dieresiscmb': GD(name='dieresiscmb', uni=0x0308, hex='0308', anchorTopY='TopY', c='̈', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dieresiscmb.uc': GD(name='dieresiscmb.uc', w=0, anchorTopY='TopY', srcName='dieresiscmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'ringcmb': GD(name='ringcmb', uni=0x030A, hex='030A', anchorTopY='TopY', c='̊', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'ringcmb.uc': GD(name='ringcmb.uc', w=0, anchorTopY='TopY', srcName='ringcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'cedillacmb': GD(name='cedillacmb', uni=0x0327, hex='0327', c='̧', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
    'caroncmb': GD(name='caroncmb', uni=0x030C, hex='030C', anchorTopY='TopY', c='̌', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'caroncmb.uc': GD(name='caroncmb.uc', w=0, anchorTopY='TopY', srcName='caroncmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

}

# Used by GlyphSet class to add tab glyph data records. 
TAB_NAMES = (
    # These glyphs don't need a separate tab-width version, since the width is already on math-width
    # 'plusminus', 'plus', 'minus', 'multiply', 'divide', 'numbersign', 'equal', 'notequal', 
    # 'greater', 'greaterequal', 'less', 'lessequal', 'logicalnot', 'lozenge', 'approxequal'
    # 'cent', 'cent.alt', 'dollar', 'dollar.alt', 'yen', 'sterling', 'bitcoin', 'bitcoin.alt'
    #
    'zero', 'zeroslash', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'asterisk',  'percent', 'perthousand', 'degree', 'period', 'comma', 'colon', 'semicolon',
    'parenleft', 'parenright', 'bracketleft', 'bracketright', 'braceleft', 'braceright',
    'quoteleft', 'quoteright', 'quotedblleft', 'quotedblright', 
    'hyphen', 'endash', 'minute', 'second', 'slash', 'backslash', 'numbersign',
)

# Make exceptions for Italic glyphs and spacing rules
LATIN_A_SET_ITALIC = GDSI = deepcopy(LATIN_A_SET)
GDSI['g'] = GD(name='g', uni=0x0067, hex='0067', c='g', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g')
GDSI['eogonek'] = GD(name='eogonek', uni=0x0119, hex='0119', c='ę', base='e', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ę E WITH OGONEK, LATIN SMALL LETTER')
GDSI['dcroat'] = GD(name='dcroat', uni=0x0111, hex='0111', c='đ', l='d', r='hyphen', base='d', isLower=True, anchorTopY='TopY', comment='đ D WITH STROKE, LATIN SMALL LETTER')
 
# Left spacing different from /t in italic. Manual spacing instead.

GDSI['a'].l = 'off'
GDSI['b'].r = None
GDSI['b'].l2r = 'a'
GDSI['d'].l = 'a'
GDSI['e'].l = 'c'
GDSI['f'].l = GDSI['f'].r ='off'
GDSI['g'].l = 'a' 
GDSI['g'].r ='off'
GDSI['i'].l = 'n' 
GDSI['i'].r = 'u'
GDSI['p'].r = 'b'
GDSI['q'].l = 'a'
GDSI['v'].l = GDSI['v'].r = 'off'
GDSI['y'].l = GDSI['y'].r = 'v'
GDSI['germandbls'].l = 'off'
GDSI['ampersand'].r = 'off'



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

    chars = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789¹²³ªº
        %$€¥£¢&*@#|áâàäåãæçéêèëíîìïıñóôòöõøœšßúûùüýÿžÂÀÄÅÃÆÇÉÊÈËÍÎÌÏÑÓÔÒÖÕØŒŠÛÙÜÝŸ
        ,:;-–—•.…“‘’‘ ‚ “”„‹›«»/\\?!¿¡()[]{}©®§+×=_°
    """
    names = []
    for gName, gd in GDS.items():
        if gd.uni and chr(gd.uni) in chars:
            names.append(gd.asSourceLine())

    #print(''.join(names))

if 0:
    # Build simple example source with onlt margins as attributes.

    for gName, gd in sorted(LATIN_A_SET.items()):
        s = f"\t'{gName}': GD(name='{gName}'"
        if gd.l is not None:
            s += f", l='{gd.l}'"
        if gd.r is not None:
            s += f", r='{gd.r}'"
        if gd.w is not None:
            s += f", w='{gd.w}'"
        if gd.l2r is not None:
            s += f", l2r='{gd.l2r}'"
        if gd.r2l is not None:
            s += f", r2l='{gd.r2l}'"
        s += '),'
        print(s)


