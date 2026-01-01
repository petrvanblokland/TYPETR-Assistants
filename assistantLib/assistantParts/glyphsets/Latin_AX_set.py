# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_AX_set.py
#    From https://foundrysupport.monotype.com/hc/en-us/articles/360029280752-Recommended-Character-Set:
#
#    Latin AX “Ascii Extended” 
#    The following character set contains 327 glyphs and is our recommended minimum for Latin-based display fonts,
#    and then extended with all diacrities for Eurpean/EU/USA usage.
#
#    Latin “Ascii” (Smallest set accorting to Monotype, exteded for all European/EU/USA languages)
#    !#$%&()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]_`abcdefghijklmnopqrstuvwxyz
#    {|}¡¢£¥§¨©ª«®¯°²³´¸¹º»¿ÀÀÂÂÃÃÄÄÅÅÆÆÇÇÈÈÉÊÊËËÌÌÍÎÎÏÏÐÑÑÒÒÓÓÔÔÕÕÖÖ×ØØÙÙÚÛÛÜÜÝÝÞßß
#    ààáââããääååææççèèéêêëëììíîîïïðññòòóóôôõõööøøùùúúûûüüýýþÿÿ
#    ĀāĂăĄąĊċČčĎďĐđĒēĖėĘęĚěĞğĠġĦħĪīĮįİıĽľŁłŇňŌōŐőŒŒœœŔŕŘřŚśŠŠššŤťŪūŰűŲųŸŸŹźŻżŽžžȘșȚțˆ
#    ˇ˘˙˛˜˝–—‘‘’‚““”„•…‹›€
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

LATIN_AX_SET_NAME = 'Latin AX'
LATIN_AX_SET_NAME_ITALIC = 'Latin AX Italic'

# The "c" attribtes are redundant, if the @uni or @hex are defined, but they are offer easy searching in the source by char.
LATIN_AX_SET = GDS = {

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
    'Aacute': GD(name='Aacute', uni=0x00C1, hex='00C1', c='Á', l='A', r='A', base='A', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER'),
    'AE': GD(name='AE', uni=0x00C6, hex='00C6', c='Æ', l='A', r='E', anchors=['bottom', 'middle', 'top'], comment='Æ ligature ae, latin capital'),
    'Acircumflex': GD(name='Acircumflex', uni=0x00C2, hex='00C2', c='Â', l='A', r='A', base='A', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Adieresis': GD(name='Adieresis', uni=0x00C4, hex='00C4', c='Ä', l='A', r='A', base='A', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Agrave': GD(name='Agrave', uni=0x00C0, hex='00C0', c='À', l='A', r='A', base='A', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
    'Atilde': GD(name='Atilde', uni=0x00C3, hex='00C3', c='Ã', l='A', r='A', base='A', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ã A WITH TILDE, LATIN CAPITAL LETTER'),
    'Aring': GD(name='Aring', uni=0x00C5, hex='00C5', c='Å', l='A', r='A', base='A', accents=['ringcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Å RING ABOVE, LATIN CAPITAL LETTER A WITH'),
    'Abreve': GD(name='Abreve', uni=0x0102, hex='0102', c='Ă', l='A', r='A', base='A', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE'),
    'Amacron': GD(name='Amacron', uni=0x0100, hex='0100', c='Ā', l='A', r='A', base='A', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ā Latin, European'),
    'Aogonek': GD(name='Aogonek', uni=0x0104, hex='0104', c='Ą', l='A', r='A', base='A', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),

    'B': GD(name='B', uni=0x0042, hex='0042', c='B', l='H', anchors=['bottom', 'middle', 'top'], comment='B LATIN CAPITAL LETTER B'),

    'C': GD(name='C', uni=0x0043, hex='0043', c='C', l='O', anchors=['bottom', 'dot', 'middle', 'top'], comment='C LATIN CAPITAL LETTER C'),
    'Ccedilla': GD(name='Ccedilla', uni=0x00C7, hex='00C7', c='Ç', l='O', r='C', base='C', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ç CEDILLA, LATIN CAPITAL LETTER C WITH'),
    'Cacute': GD(name='Cacute', uni=0x0106, hex='0106', c='Ć', l='O', r='C', base='C', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ć LATIN CAPITAL LETTER C WITH ACUTE'),
    'Ccaron': GD(name='Ccaron', uni=0x010C, hex='010C', c='Č', l='O', r='C', base='C', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Č LATIN CAPITAL LETTER C WITH CARON'),
    'Cdotaccent': GD(name='Cdotaccent', uni=0x010A, hex='010A', c='Ċ', l='O', r='C', base='C', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ċ LATIN CAPITAL LETTER C WITH DOT ABOVE'),

    'D': GD(name='D', uni=0x0044, hex='0044', c='D', l='H', r='O', anchors=['bottom', 'middle', 'top'], comment='D'),
    'Dcaron': GD(name='Dcaron', uni=0x010E, hex='010E', c='Ď', l='D', r='D', base='D', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ď'),
    'Dcroat': GD(name='Dcroat', uni=0x0110, hex='0110', c='Đ', base='Eth', comment='Đ'),

    'E': GD(name='E', uni=0x0045, hex='0045', c='E', l='H', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='E'),
    'Eacute': GD(name='Eacute', uni=0x00C9, hex='00C9', c='É', l='H', r='E', base='E', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='É E WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ecircumflex': GD(name='Ecircumflex', uni=0x00CA, hex='00CA', c='Ê', l='H', r='E', base='E', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ê E WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Edieresis': GD(name='Edieresis', uni=0x00CB, hex='00CB', c='Ë', l='H', r='E', base='E', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ë E WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Egrave': GD(name='Egrave', uni=0x00C8, hex='00C8', c='È', l='H', r='E', base='E', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='È E WITH GRAVE, LATIN CAPITAL LETTER'),
    'Euro': GD(name='Euro', uni=0x20AC, hex='20AC', c='€', l='center', w='mathWidth', g1='C', srcName='C'),
    'Ecaron': GD(name='Ecaron', uni=0x011A, hex='011A', c='Ě', l='H', r='E', base='E', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ě'),
    'Edotaccent': GD(name='Edotaccent', uni=0x0116, hex='0116', c='Ė', l='H', r='E', base='E', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Emacron': GD(name='Emacron', uni=0x0112, hex='0112', c='Ē', l='H', r='E', base='E', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ē'),
    'Eogonek': GD(name='Eogonek', uni=0x0118, hex='0118', c='Ę', l='E', w='E', base='E', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ę'),
    'Eth': GD(name='Eth', uni=0x00D0, hex='00D0', c='Ð', r='D', base='D', comment='Ð ETH, LATIN CAPITAL LETTER'),

    'F': GD(name='F', uni=0x0046, hex='0046', c='F', l='H', anchors=['bottom', 'middle', 'top'], comment='F'),

    'G': GD(name='G', uni=0x0047, hex='0047', c='G', l='O', anchors=['bottom', 'middle', 'top'], comment='G'),
    'Gbreve': GD(name='Gbreve', uni=0x011E, hex='011E', c='Ğ', l='G', r='G', base='G', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ğ'),
    'Gdotaccent': GD(name='Gdotaccent', uni=0x0120, hex='0120', c='Ġ', l='G', r='G', base='G', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ġ'),

    'H': GD(name='H', uni=0x0048, hex='0048', c='H', l2r='self', anchors=['bottom', 'middle', 'top', 'topleft'], comment='H'),
    'Hbar': GD(name='Hbar', uni=0x0126, hex='0126', c='Ħ', l='Eth', l2r='self', base='H', comment='Ħ'),

    'I': GD(name='I', uni=0x0049, hex='0049', c='I', l='H', r='H', srcName='H', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='I'),
    'Iacute': GD(name='Iacute', uni=0x00CD, hex='00CD', c='Í', w='I', bl='I', base='I', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
    'Icircumflex': GD(name='Icircumflex', uni=0x00CE, hex='00CE', c='Î', w='I', bl='I', base='I', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Idieresis': GD(name='Idieresis', uni=0x00CF, hex='00CF', c='Ï', w='I', bl='I', base='I', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Igrave': GD(name='Igrave', uni=0x00CC, hex='00CC', c='Ì', w='I', bl='I', base='I', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
    'Idotaccent': GD(name='Idotaccent', uni=0x0130, hex='0130', c='İ', w='I', bl='I', base='I', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
    'Imacron': GD(name='Imacron', uni=0x012A, hex='012A', c='Ī', w='I', bl='I', base='I', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ī'),
    'Iogonek': GD(name='Iogonek', uni=0x012E, hex='012E', c='Į', w='I', bl='I', base='I', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Į'),

    'J': GD(name='J', uni=0x004A, hex='004A', c='J', anchors=['bottom', 'middle', 'top'], comment='J'),

    'K': GD(name='K', uni=0x004B, hex='004B', c='K', l='H', anchors=['bottom', 'middle', 'top'], comment='K'),

    'L': GD(name='L', uni=0x004C, hex='004C', c='L', l='H', anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='L'),
    'Lacute': GD(name='Lacute', uni=0x0139, hex='0139', c='Ĺ', l='H', r='L', base='L', accents=['acutecmb.uc'], fixAccents=False, anchors=['bottom', 'middle', 'top'], comment='Ĺ'),
    'Lcaron': GD(name='Lcaron', uni=0x013D, hex='013D', c='Ľ', l='H', w='L', base='L', accents=['caroncmb.vert'], anchors=['bottom', 'middle', 'top'], comment='Ľ'),
    'Lslash': GD(name='Lslash', uni=0x0141, hex='0141', c='Ł', r='L', base='L', comment='Ł'),

    'M': GD(name='M', uni=0x004D, hex='004D', c='M', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='M'),

    'N': GD(name='N', uni=0x004E, hex='004E', c='N', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='N'),
    'Ntilde': GD(name='Ntilde', uni=0x00D1, hex='00D1', c='Ñ', l='H', r='H', base='N', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ñ N WITH TILDE, LATIN CAPITAL LETTER'),
    'Nacute': GD(name='Nacute', uni=0x0143, hex='0143', c='Ń', l='H', r='H', base='N', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ń'),
    'Ncaron': GD(name='Ncaron', uni=0x0147, hex='0147', c='Ň', l='H', r='H', base='N', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ň'),

    'O': GD(name='O', uni=0x004F, hex='004F', c='O', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top', 'topleft'], comment='O'),
    'OE': GD(name='OE', uni=0x0152, hex='0152', c='Œ', l='O', r='E', anchors=['bottom', 'middle', 'top'], comment='Œ'),
    'Oacute': GD(name='Oacute', uni=0x00D3, hex='00D3', c='Ó', l='O', r='O', base='O', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ocircumflex': GD(name='Ocircumflex', uni=0x00D4, hex='00D4', c='Ô', l='O', r='O', base='O', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Odieresis': GD(name='Odieresis', uni=0x00D6, hex='00D6', c='Ö', l='O', r='O', base='O', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ograve': GD(name='Ograve', uni=0x00D2, hex='00D2', c='Ò', l='O', r='O', base='O', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
    'Oslash': GD(name='Oslash', uni=0x00D8, hex='00D8', c='Ø', l='O', w='O', srcName='O', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Otilde': GD(name='Otilde', uni=0x00D5, hex='00D5', c='Õ', l='O', r='O', base='O', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),
    'Ohungarumlaut': GD(name='Ohungarumlaut', uni=0x0150, hex='0150', c='Ő', base='O', accents=['hungarumlautcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ő'),
    'Omacron': GD(name='Omacron', uni=0x014C, hex='014C', c='Ō', l='O', r='O', base='O', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ō'),

    'P': GD(name='P', uni=0x0050, hex='0050', c='P', l='H', anchors=['bottom', 'middle', 'top', 'topleft'], comment='P'),

    'Q': GD(name='Q', uni=0x0051, hex='0051', c='Q', l='O', w='O', anchors=['bottom', 'middle', 'top'], comment='Q'),

    'R': GD(name='R', uni=0x0052, hex='0052', c='R', bl='H', anchors=['bottom', 'middle', 'top'], comment='R'),
    'Racute': GD(name='Racute', uni=0x0154, hex='0154', c='Ŕ', r='R', bl='H', base='R', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŕ'),
    'Rcaron': GD(name='Rcaron', uni=0x0158, hex='0158', c='Ř', r='R', bl='H', base='R', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ř'),

    'S': GD(name='S', uni=0x0053, hex='0053', c='S', l2r='self', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='S'),
    'Scaron': GD(name='Scaron', uni=0x0160, hex='0160', c='Š', l='S', w='S', base='S', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Š'),
    'Sacute': GD(name='Sacute', uni=0x015A, hex='015A', c='Ś', l='S', w='S', base='S', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ś'),
    'Scommaaccent': GD(name='Scommaaccent', uni=0x0218, hex='0218', c='Ș', l='S', w='S', base='S', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ș'),

    'T': GD(name='T', uni=0x0054, hex='0054', c='T', l2r='self', anchors=['bottom', 'middle', 'top'], comment='T'),
    'Tcaron': GD(name='Tcaron', uni=0x0164, hex='0164', c='Ť', l='T', r='T', base='T', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ť'),
    'Tcommaaccent': GD(name='Tcommaaccent', uni=0x021A, hex='021A', c='Ț', l='T', r='T', base='T', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ț'),
    'Thorn': GD(name='Thorn', uni=0x00DE, hex='00DE', c='Þ', l='H', r='P', comment='Þ THORN, LATIN CAPITAL LETTER'),

    'U': GD(name='U', uni=0x0055, hex='0055', c='U', l='off', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='U'),
    'Ucircumflex': GD(name='Ucircumflex', uni=0x00DB, hex='00DB', c='Û', l='U', r='U', base='U', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Û U WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Udieresis': GD(name='Udieresis', uni=0x00DC, hex='00DC', c='Ü', l='U', r='U', base='U', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ü U WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ugrave': GD(name='Ugrave', uni=0x00D9, hex='00D9', c='Ù', l='U', r='U', base='U', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ù U WITH GRAVE, LATIN CAPITAL LETTER'),
    'Uacute': GD(name='Uacute', uni=0x00DA, hex='00DA', c='Ú', l='U', r='U', base='U', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ú U WITH ACUTE, LATIN CAPITAL LETTER'),
    'Uhungarumlaut': GD(name='Uhungarumlaut', uni=0x0170, hex='0170', c='Ű', l='U', r='U', base='U', accents=['hungarumlautcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ű'),
    'Umacron': GD(name='Umacron', uni=0x016A, hex='016A', c='Ū', l='U', r='U', base='U', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ū'),
    'Uogonek': GD(name='Uogonek', uni=0x0172, hex='0172', c='Ų', l='U', r='U', base='U', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ų'),

    'V': GD(name='V', uni=0x0056, hex='0056', c='V', l='A', r='A', anchors=['bottom', 'middle', 'top'], comment='V'),

    'W': GD(name='W', uni=0x0057, hex='0057', c='W', l='V', r='V', anchors=['bottom', 'middle', 'top'], comment='W'),

    'X': GD(name='X', uni=0x0058, hex='0058', c='X', l2r='self', anchors=['bottom', 'middle', 'top'], comment='X'),

    'Y': GD(name='Y', uni=0x0059, hex='0059', c='Y', l2r='self', anchors=['bottom', 'middle', 'top', 'topleft'], comment='Y'),
    'Yacute': GD(name='Yacute', uni=0x00DD, hex='00DD', c='Ý', l='Y', r='Y', base='Y', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ý Y WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ydieresis': GD(name='Ydieresis', uni=0x0178, hex='0178', c='Ÿ', l='Y', r='Y', base='Y', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ÿ Y WITH DIAERESIS, LATIN CAPITAL LETTER'),

    'Z': GD(name='Z', uni=0x005A, hex='005A', c='Z', l2r='self', anchors=['bottom', 'middle', 'top'], comment='Z'),
    'Zacute': GD(name='Zacute', uni=0x0179, hex='0179', c='Ź', l='Z', r='Z', base='Z', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ź'),
    'Zcaron': GD(name='Zcaron', uni=0x017D, hex='017D', c='Ž', l='Z', r='Z', base='Z', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ž'),
    'Zdotaccent': GD(name='Zdotaccent', uni=0x017B, hex='017B', c='Ż', l='Z', r='Z', base='Z', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ż'),

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
    'abreve': GD(name='abreve', uni=0x0103, hex='0103', c='ă', w='a', bl='a', base='a', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ă A WITH BREVE, LATIN SMALL LETTER'),
    'acute': GD(name='acute', uni=0x00B4, hex='00B4', c='´', l='center', w='accentWidth', base='acutecmb', isLower=True, comment='´ spacing acute accent'),
    'amacron': GD(name='amacron', uni=0x0101, hex='0101', c='ā', base='a', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ā A WITH MACRON, LATIN SMALL LETTER'),
    'aogonek': GD(name='aogonek', uni=0x0105, hex='0105', c='ą', base='a', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ą A WITH OGONEK, LATIN SMALL LETTER'),

    'b': GD(name='b', uni=0x0062, hex='0062', c='b', l='off', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='b'),
    'backslash': GD(name='backslash', uni=0x005C, hex='005C', c="\\" , l2r='self', isLower=True, comment='\\ SOLIDUS, REVERSE'),
    'bar': GD(name='bar', uni=0x007C, hex='007C', c='|', l='bracketleft', r='bracketright', isLower=True, comment='| VERTICAL LINE'),
    'braceleft': GD(name='braceleft', uni=0x007B, hex='007B', c='{', isLower=True, comment='{ opening curly bracket'),
    'braceright': GD(name='braceright', uni=0x007D, hex='007D', c='}', l2r='braceleft', r2l='braceleft', isLower=True, comment='} RIGHT CURLY BRACKET'),
    'bracketleft': GD(name='bracketleft', uni=0x005B, hex='005B', c='[', isLower=True, comment='[ square bracket, opening'),
    'bracketright': GD(name='bracketright', uni=0x005D, hex='005D', c=']', l2r='bracketleft', r2l='bracketleft', isLower=True, comment='] SQUARE BRACKET, RIGHT'),
    'bullet': GD(name='bullet', uni=0x2022, hex='2022', c='•', l2r='self', isLower=True, comment='• small circle, black'),

    'c': GD(name='c', uni=0x0063, hex='0063', c='c', isLower=True, anchors=['bottom', 'dot', 'middle', 'top'], comment='c'),
    'cacute': GD(name='cacute', uni=0x0107, hex='0107', c='ć', anchorTopY='TopY', base='c', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ć C WITH ACUTE, LATIN SMALL LETTER'),
    'ccaron': GD(name='ccaron', uni=0x010D, hex='010D', c='č', anchorTopY='TopY', base='c', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='č C WITH CARON, LATIN SMALL LETTER'),
    'ccedilla': GD(name='ccedilla', uni=0x00E7, hex='00E7', c='ç', base='c', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ç CEDILLA, LATIN SMALL LETTER C WITH'),
    'ccircumflex': GD(name='ccircumflex', uni=0x0109, hex='0109', c='ĉ', anchorTopY='TopY', base='c', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĉ C WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'cdotaccent': GD(name='cdotaccent', uni=0x010B, hex='010B', c='ċ', anchorTopY='TopY', base='c', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'caron': GD(name='caron', uni=0x02C7, hex='02C7', c='ˇ', l='center', w='accentWidth', base='caroncmb', isLower=True, comment='ˇ tone, mandarin chinese third'),
    'cedilla': GD(name='cedilla', uni=0x00B8, hex='00B8', c='¸', l='center', w='accentWidth', base='cedillacmb', isLower=True),
    'circumflex': GD(name='circumflex', uni=0x02C6, hex='02C6', c='ˆ', l='center', w='accentWidth', base='circumflexcmb', isLower=True, comment='ˆ Legacy CIRCUMFLEX ACCENT, MODIFIER LETTER'),

    'd': GD(name='d', uni=0x0064, hex='0064', c='d', isLower=True, anchors=['bottom', 'middle', 'top', 'vert'], comment='d'),
    'dcaron': GD(name='dcaron', uni=0x010F, hex='010F', c='ď', l='d', w='d', base='d', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ď D WITH CARON, LATIN SMALL LETTER'),
    'dcroat': GD(name='dcroat', uni=0x0111, hex='0111', c='đ', l='d', r='hyphen', isLower=True, comment='đ D WITH STROKE, LATIN SMALL LETTER'),
    'dieresis': GD(name='dieresis', uni=0x00A8, hex='00A8', c='¨', l='center', w='accentWidth', base='dieresiscmb', isLower=True, comment='¨ spacing diaeresis'),
    'dotaccent': GD(name='dotaccent', uni=0x02D9, hex='02D9', c='˙', l='center', w='accentWidth', base='dotaccentcmb', isLower=True, gid=480, comment='˙ tone, mandarin chinese fifth or neutral'),

    'e': GD(name='e', uni=0x0065, hex='0065', c='e', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='e'),
    'eacute': GD(name='eacute', uni=0x00E9, hex='00E9', c='é', base='e', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='é E WITH ACUTE, LATIN SMALL LETTER'),
    'ecircumflex': GD(name='ecircumflex', uni=0x00EA, hex='00EA', c='ê', base='e', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ê E WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'edieresis': GD(name='edieresis', uni=0x00EB, hex='00EB', c='ë', w='e', base='e', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ë E WITH DIAERESIS, LATIN SMALL LETTER'),
    'egrave': GD(name='egrave', uni=0x00E8, hex='00E8', c='è', w='e', bl='e', base='e', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='è E WITH GRAVE, LATIN SMALL LETTER'),
    'ecaron': GD(name='ecaron', uni=0x011B, hex='011B', c='ě', base='e', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ě E WITH CARON, LATIN SMALL LETTER'),
    'edotaccent': GD(name='edotaccent', uni=0x0117, hex='0117', c='ė', w='e', base='e', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'emacron': GD(name='emacron', uni=0x0113, hex='0113', c='ē', base='e', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ē E WITH MACRON, LATIN SMALL LETTER'),
    'eogonek': GD(name='eogonek', uni=0x0119, hex='0119', c='ę', base='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ę E WITH OGONEK, LATIN SMALL LETTER'),
    'eth': GD(name='eth', uni=0x00F0, hex='00F0', c='ð', l='o', r='o', isLower=True, comment='ð LATIN SMALL LETTER ETH'),

    'f': GD(name='f', uni=0x0066, hex='0066', c='f', l='t', rightMin='-100', isLower=True, anchors=['bottom', 'middle', 'top'], comment='f'),

    'g': GD(name='g', uni=0x0067, hex='0067', c='g', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g'),
    'germandbls': GD(name='germandbls', uni=0x00DF, hex='00DF', c='ß', l='f', r='s', isLower=True, comment='ß SHARP S, LATIN SMALL LETTER'),
    'guillemotleft': GD(name='guillemotleft', uni=0x00AB, hex='00AB', c='«', l2r='self', isLower=True),
    'guillemotright': GD(name='guillemotright', uni=0x00BB, hex='00BB', c='»', l='guillemotleft', r='guillemotleft', isLower=True),
    'guilsinglleft': GD(name='guilsinglleft', uni=0x2039, hex='2039', c='‹', l='guillemotleft', r='guillemotleft', isLower=True, comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglright': GD(name='guilsinglright', uni=0x203A, hex='203A', c='›', l='guillemotleft', r='guillemotleft', isLower=True, comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK'),
    'gbreve': GD(name='gbreve', uni=0x011F, hex='011F', c='ğ', base='g', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ğ G WITH BREVE, LATIN SMALL LETTER'),
    'gdotaccent': GD(name='gdotaccent', uni=0x0121, hex='0121', c='ġ', base='g', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'grave': GD(name='grave', uni=0x0060, hex='0060', c='`', l='center', w='accentWidth', base='gravecmb', isLower=True, comment='` spacing grave accent'),

    'h': GD(name='h', uni=0x0068, hex='0068', c='h', isLower=True, anchors=['bottom', 'dot', 'middle', 'top'], comment='h'),
    'hbar': GD(name='hbar', uni=0x0127, hex='0127', c='ħ', l='h', r='h', base='h', isLower=True, comment='ħ H WITH STROKE, LATIN SMALL LETTER'),
    'hungarumlaut': GD(name='hungarumlaut', uni=0x02DD, hex='02DD', c='˝', l='center', w='accentWidth', base='hungarumlautcmb', isLower=True, comment='˝ DOUBLE ACUTE ACCENT'),

    'i': GD(name='i', uni=0x0069, hex='0069', c='i', bl='n', w='idotless', base='idotless', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='i'),
    'idotless': GD(name='idotless', uni=0x0131, hex='0131', c='ı', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'iacute': GD(name='iacute', uni=0x00ED, hex='00ED', c='í', w='i', bl='idotless', base='idotless', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='í I WITH ACUTE, LATIN SMALL LETTER'),
    'icircumflex': GD(name='icircumflex', uni=0x00EE, hex='00EE', c='î', w='i', bl='idotless', base='idotless', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='î I WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'idieresis': GD(name='idieresis', uni=0x00EF, hex='00EF', c='ï', w='i', bl='idotless', base='idotless', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ï I WITH DIAERESIS, LATIN SMALL LETTER'),
    'igrave': GD(name='igrave', uni=0x00EC, hex='00EC', c='ì', w='i', bl='idotless', base='idotless', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ì I WITH GRAVE, LATIN SMALL LETTER'),
    'imacron': GD(name='imacron', uni=0x012B, hex='012B', c='ī', w='i', bl='idotless', base='idotless', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ī I WITH MACRON, LATIN SMALL LETTER'),
    'iogonek': GD(name='iogonek', uni=0x012F, hex='012F', c='į', w='i', bl='idotless', base='i', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='į I WITH OGONEK, LATIN SMALL LETTER'),

    'j': GD(name='j', uni=0x006A, hex='006A', c='j', l='off', r='off', isLower=True, anchors=['bottom', 'middle'], comment='j'),

    'k': GD(name='k', uni=0x006B, hex='006B', c='k', l='h', r='x', isLower=True, anchors=['bottom', 'middle', 'top'], comment='k'),

    'l': GD(name='l', uni=0x006C, hex='006C', c='l', l='h', r='idotless', isLower=True, anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='l'),
    'lacute': GD(name='lacute', uni=0x013A, hex='013A', c='ĺ', w='l', bl='l', anchorTopY='TopY', base='l', accents=['acutecmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER'),
    'lcaron': GD(name='lcaron', uni=0x013E, hex='013E', c='ľ', l='off', w='l', base='l', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ľ L WITH CARON, LATIN SMALL LETTER'),
    'lslash': GD(name='lslash', uni=0x0142, hex='0142', c='ł', l='off', l2r='self', base='l', isLower=True, comment='ł L WITH STROKE, LATIN SMALL LETTER'),

    'm': GD(name='m', uni=0x006D, hex='006D', c='m', l='n', r='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='m'),
    'macron': GD(name='macron', uni=0x00AF, hex='00AF', c='¯', l='center', w='accentWidth', base='macroncmb', isLower=True, comment='¯ spacing macron'),

    'n': GD(name='n', uni=0x006E, hex='006E', c='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='n'),
    'ntilde': GD(name='ntilde', uni=0x00F1, hex='00F1', c='ñ', base='n', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ñ N WITH TILDE, LATIN SMALL LETTER'),
    'nacute': GD(name='nacute', uni=0x0144, hex='0144', c='ń', base='n', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ń N WITH ACUTE, LATIN SMALL LETTER'),
    'ncaron': GD(name='ncaron', uni=0x0148, hex='0148', c='ň', base='n', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ň N WITH CARON, LATIN SMALL LETTER'),

    'o': GD(name='o', uni=0x006F, hex='006F', c='o', l2r='self', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='o'),
    'oacute': GD(name='oacute', uni=0x00F3, hex='00F3', c='ó', l='o', r='o', base='o', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ó O WITH ACUTE, LATIN SMALL LETTER'),
    'ocircumflex': GD(name='ocircumflex', uni=0x00F4, hex='00F4', c='ô', w='o', bl='o', base='o', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ô O WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'odieresis': GD(name='odieresis', uni=0x00F6, hex='00F6', c='ö', w='o', bl='o', base='o', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ö O WITH DIAERESIS, LATIN SMALL LETTER'),
    'oe': GD(name='oe', uni=0x0153, hex='0153', c='œ', l='o', r='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='œ SMALL LIGATURE OE, LATIN'),
    'ograve': GD(name='ograve', uni=0x00F2, hex='00F2', c='ò', l='o', r='o', base='o', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ò O WITH GRAVE, LATIN SMALL LETTER'),
    'oslash': GD(name='oslash', uni=0x00F8, hex='00F8', c='ø', l2r='o', srcName='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'otilde': GD(name='otilde', uni=0x00F5, hex='00F5', c='õ', base='o', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='õ O WITH TILDE, LATIN SMALL LETTER'),
    'ogonek': GD(name='ogonek', uni=0x02DB, hex='02DB', c='˛', l='center', w='accentWidth', base='ogonekcmb', isLower=True, gid=482, comment='˛ OGONEK'),
    'ohungarumlaut': GD(name='ohungarumlaut', uni=0x0151, hex='0151', c='ő', w='o', base='o', accents=['hungarumlautcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'omacron': GD(name='omacron', uni=0x014D, hex='014D', c='ō', l='o', r='o', base='o', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ō O WITH MACRON, LATIN SMALL LETTER'),

    'p': GD(name='p', uni=0x0070, hex='0070', c='p', l='n', r='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='p'),

    'q': GD(name='q', uni=0x0071, hex='0071', c='q', l='o', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='q'),
    'quotedblbase': GD(name='quotedblbase', uni=0x201E, hex='201E', c='„', l='quotesingle', r='quotesingle', isLower=True, comment='„ quotation mark, low double comma'),
    'quotedblleft': GD(name='quotedblleft', uni=0x201C, hex='201C', c='“', l='quotesingle', r='quotesingle', isLower=True, comment='“ turned comma quotation mark, double'),
    'quotedblright': GD(name='quotedblright', uni=0x201D, hex='201D', c='”', l='quotesingle', r='quotesingle', isLower=True, comment='” RIGHT DOUBLE QUOTATION MARK'),
    'quoteleft': GD(name='quoteleft', uni=0x2018, hex='2018', c='‘', l='quotesingle', r='quotesingle', isLower=True, comment='‘ turned comma quotation mark, single'),
    'quoteright': GD(name='quoteright', uni=0x2019, hex='2019', c='’', l='quotesingle', r='quotesingle', isLower=True, comment='’ SINGLE QUOTATION MARK, RIGHT'),
    'quotesinglbase': GD(name='quotesinglbase', uni=0x201A, hex='201A', c='‚', l='quotesingle', r='quotesingle', isLower=True, comment='‚ SINGLE LOW-9 QUOTATION MARK'),

    'r': GD(name='r', uni=0x0072, hex='0072', c='r', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='r'),
    'racute': GD(name='racute', uni=0x0155, hex='0155', c='ŕ', l='r', r='r', rightMin='-100', base='r', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŕ R WITH ACUTE, LATIN SMALL LETTER'),
    'rcaron': GD(name='rcaron', uni=0x0159, hex='0159', c='ř', r='r', bl='r', rightMin='-100', base='r', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ř R WITH CARON, LATIN SMALL LETTER'),

    's': GD(name='s', uni=0x0073, hex='0073', c='s', l='off', l2r='self', isLower=True, useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='s'),
    'scaron': GD(name='scaron', uni=0x0161, hex='0161', c='š', l='s', r='s', base='s', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='š S WITH CARON, LATIN SMALL LETTER'),
    'sacute': GD(name='sacute', uni=0x015B, hex='015B', c='ś', l='s', r='s', base='s', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ś S WITH ACUTE, LATIN SMALL LETTER'),
    'scommaaccent': GD(name='scommaaccent', uni=0x0219, hex='0219', c='ș', l='s', r='s', base='s', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ș S WITH COMMA BELOW, LATIN SMALL LETTER'),

    't': GD(name='t', uni=0x0074, hex='0074', c='t', l='off', r='off', isLower=True, anchors=['bottom', 'middle', 'top', 'vert'], comment='t'),
    'tcaron': GD(name='tcaron', uni=0x0165, hex='0165', c='ť', l='t', w='t', base='t', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ť T WITH CARON, LATIN SMALL LETTER'),
    'tcommaaccent': GD(name='tcommaaccent', uni=0x021B, hex='021B', c='ț', base='t', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ț T WITH COMMA BELOW, LATIN SMALL LETTER'),
    'thorn': GD(name='thorn', uni=0x00FE, hex='00FE', c='þ', r='o', isLower=True, comment='þ THORN, LATIN SMALL LETTER'),
    'tilde': GD(name='tilde', uni=0x02DC, hex='02DC', c='˜', l='center', w='accentWidth', base='tildecmb', isLower=True),

    'u': GD(name='u', uni=0x0075, hex='0075', c='u', l2r='n', r2l='n', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='u'),
    'uacute': GD(name='uacute', uni=0x00FA, hex='00FA', c='ú', l='u', r='u', base='u', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ú U WITH ACUTE, LATIN SMALL LETTER'),
    'ucircumflex': GD(name='ucircumflex', uni=0x00FB, hex='00FB', c='û', l='u', r='u', base='u', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='û U WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'udieresis': GD(name='udieresis', uni=0x00FC, hex='00FC', c='ü', l='u', r='u', base='u', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ü U WITH DIAERESIS, LATIN SMALL LETTER'),
    'ugrave': GD(name='ugrave', uni=0x00F9, hex='00F9', c='ù', l='u', r='u', base='u', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ù U WITH GRAVE, LATIN SMALL LETTER'),
    'uhungarumlaut': GD(name='uhungarumlaut', uni=0x0171, hex='0171', c='ű', l='u', w='u', base='u', accents=['hungarumlautcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ű U WITH DOUBLE ACUTE, LATIN SMALL LETTER'),
    'umacron': GD(name='umacron', uni=0x016B, hex='016B', c='ū', l='u', r='u', base='u', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ū U WITH MACRON, LATIN SMALL LETTER'),
    'uogonek': GD(name='uogonek', uni=0x0173, hex='0173', c='ų', w='u', bl='u', base='u', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ų U WITH OGONEK, LATIN SMALL LETTER'),

    'v': GD(name='v', uni=0x0076, hex='0076', c='v', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='v LATIN SMALL LETTER V'),

    'w': GD(name='w', uni=0x0077, hex='0077', c='w', l='v', r='v', isLower=True, anchors=['bottom', 'middle', 'top'], comment='w LATIN SMALL LETTER W'),

    'x': GD(name='x', uni=0x0078, hex='0078', c='x', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='x LATIN SMALL LETTER X'),

    'y': GD(name='y', uni=0x0079, hex='0079', c='y', l='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='y LATIN SMALL LETTER Y'),
    'yacute': GD(name='yacute', uni=0x00FD, hex='00FD', c='ý', l='y', r='y', base='y', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ý Y WITH ACUTE, LATIN SMALL LETTER'),
    'ydieresis': GD(name='ydieresis', uni=0x00FF, hex='00FF', c='ÿ', l='y', r='y', base='y', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ÿ Y WITH DIAERESIS, LATIN SMALL LETTER'),

    'z': GD(name='z', uni=0x007A, hex='007A', c='z', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='z LATIN SMALL LETTER Z'),
    'zcaron': GD(name='zcaron', uni=0x017E, hex='017E', c='ž', l='z', r='z', base='z', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ž Z WITH CARON, LATIN SMALL LETTER'),
    'zacute': GD(name='zacute', uni=0x017A, hex='017A', c='ź', l='z', r='z', base='z', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ź Z WITH ACUTE, LATIN SMALL LETTER'),
    'zdotaccent': GD(name='zdotaccent', uni=0x017C, hex='017C', c='ż', l='z', r='z', base='z', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ż Z WITH DOT ABOVE, LATIN SMALL LETTER'),

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
    'macroncmb': GD(name='macroncmb', uni=0x0304, anchorTopY='TopY', hex='0304', c='̄', w=0, srcName='uni0304', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'macroncmb.uc': GD(name='macroncmb.uc', w=0, anchorTopY='TopY', srcName='macroncmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'breve': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02d8, c='˘', name='breve', base='brevecmb', comment='˘ Spacing Clones of Diacritics', anchors=[]),
    'brevecmb': GD(name='brevecmb', uni=0x0306, hex='0306', anchorTopY='TopY', c='̆', w=0, srcName='uni0306', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'brevecmb.uc': GD(name='brevecmb.uc', w=0, anchorTopY='TopY', srcName='brevecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dotaccentcmb': GD(name='dotaccentcmb', uni=0x0307, anchorTopY='TopY', hex='0307', c='̇', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dotaccentcmb.uc': GD(name='dotaccentcmb.uc', w=0, anchorTopY='TopY', srcName='dotaccentcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'hungarumlautcmb': GD(name='hungarumlautcmb', uni=0x030B, anchorTopY='TopY', hex='030B', c='̋', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'hungarumlautcmb.uc': GD(name='hungarumlautcmb.uc', w=0, anchorTopY='TopY', srcName='hungarumlautcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'caroncmb.vert': GD(name='caroncmb.vert', w=0, srcName='quotesingle', anchors=[AD._VERT]),
    'commaaccentcmb': GD(name='commaaccentcmb', uni=0x0326, anchorTopY='TopY', hex='0326', c='̦', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),

    # Below
    'dotbelowcmb': GD(name='dotbelowcmb', uni=0x0323, hex='0323', c='̣', w=0, base='dotaccentcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
    'dieresisbelowcmb': GD(name='dieresisbelowcmb', uni=0x0324, hex='0324', c='̤', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='dieresiscmb',isLower=True, anchors=['_bottom', 'bottom']),
    'commabelowcmb': GD(g2='cmb', g1='cmb', l=GD.CAT_CENTER, w=0, uni=0x0326, name='commabelowcmb', src='comma', anchors=[]),
    'ogonekcmb': GD(name='ogonekcmb', uni=0x0328, hex='0328', c='̨', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_ogonek', 'bottom']),
    'cedillacmb': GD(name='cedillacmb', uni=0x0327, hex='0327', c='̧', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
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
LATIN_AX_SET_ITALIC = GDSI = deepcopy(LATIN_AX_SET)
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

from assistantLib.assistantParts.glyphsets.Latin_L_set import LATIN_L_SET


glyphs = {

    "Oacute": {"unicode": "00D3", "char": "Ó", "category": "precomposed"},
    "oacute": {"unicode": "00F3", "char": "ó", "category": "precomposed"},
    "Racute": {"unicode": "0154", "char": "Ŕ", "category": "precomposed"},
    "racute": {"unicode": "0155", "char": "ŕ", "category": "precomposed"},
    "Sacute": {"unicode": "015A", "char": "Ś", "category": "precomposed"},
    "sacute": {"unicode": "015B", "char": "ś", "category": "precomposed"},
    "Uacute": {"unicode": "00DA", "char": "Ú", "category": "precomposed"},
    "uacute": {"unicode": "00FA", "char": "ú", "category": "precomposed"},
    "Yacute": {"unicode": "00DD", "char": "Ý", "category": "precomposed"},
    "yacute": {"unicode": "00FD", "char": "ý", "category": "precomposed"},
    "Zacute": {"unicode": "0179", "char": "Ź", "category": "precomposed"},
    "zacute": {"unicode": "017A", "char": "ź", "category": "precomposed"},

    # Grave
    "Agrave": {"unicode": "00C0", "char": "À", "category": "precomposed"},
    "agrave": {"unicode": "00E0", "char": "à", "category": "precomposed"},
    "Egrave": {"unicode": "00C8", "char": "È", "category": "precomposed"},
    "egrave": {"unicode": "00E8", "char": "è", "category": "precomposed"},
    "Igrave": {"unicode": "00CC", "char": "Ì", "category": "precomposed"},
    "igrave": {"unicode": "00EC", "char": "ì", "category": "precomposed"},
    "Ograve": {"unicode": "00D2", "char": "Ò", "category": "precomposed"},
    "ograve": {"unicode": "00F2", "char": "ò", "category": "precomposed"},
    "Ugrave": {"unicode": "00D9", "char": "Ù", "category": "precomposed"},
    "ugrave": {"unicode": "00F9", "char": "ù", "category": "precomposed"},

    # Circumflex
    "Acircumflex": {"unicode": "00C2", "char": "Â", "category": "precomposed"},
    "acircumflex": {"unicode": "00E2", "char": "â", "category": "precomposed"},
    "Ecircumflex": {"unicode": "00CA", "char": "Ê", "category": "precomposed"},
    "ecircumflex": {"unicode": "00EA", "char": "ê", "category": "precomposed"},
    "Icircumflex": {"unicode": "00CE", "char": "Î", "category": "precomposed"},
    "icircumflex": {"unicode": "00EE", "char": "î", "category": "precomposed"},
    "Ocircumflex": {"unicode": "00D4", "char": "Ô", "category": "precomposed"},
    "ocircumflex": {"unicode": "00F4", "char": "ô", "category": "precomposed"},
    "Ucircumflex": {"unicode": "00DB", "char": "Û", "category": "precomposed"},
    "ucircumflex": {"unicode": "00FB", "char": "û", "category": "precomposed"},

    # Diaeresis
    "Adieresis": {"unicode": "00C4", "char": "Ä", "category": "precomposed"},
    "adieresis": {"unicode": "00E4", "char": "ä", "category": "precomposed"},
    "Edieresis": {"unicode": "00CB", "char": "Ë", "category": "precomposed"},
    "edieresis": {"unicode": "00EB", "char": "ë", "category": "precomposed"},
    "Idieresis": {"unicode": "00CF", "char": "Ï", "category": "precomposed"},
    "idieresis": {"unicode": "00EF", "char": "ï", "category": "precomposed"},
    "Odieresis": {"unicode": "00D6", "char": "Ö", "category": "precomposed"},
    "odieresis": {"unicode": "00F6", "char": "ö", "category": "precomposed"},
    "Udieresis": {"unicode": "00DC", "char": "Ü", "category": "precomposed"},
    "udieresis": {"unicode": "00FC", "char": "ü", "category": "precomposed"},
    "Ydieresis": {"unicode": "0178", "char": "Ÿ", "category": "precomposed"},
    "ydieresis": {"unicode": "00FF", "char": "ÿ", "category": "precomposed"},

    # Tilde
    "Atilde": {"unicode": "00C3", "char": "Ã", "category": "precomposed"},
    "atilde": {"unicode": "00E3", "char": "ã", "category": "precomposed"},
    "Ntilde": {"unicode": "00D1", "char": "Ñ", "category": "precomposed"},
    "ntilde": {"unicode": "00F1", "char": "ñ", "category": "precomposed"},
    "Otilde": {"unicode": "00D5", "char": "Õ", "category": "precomposed"},
    "otilde": {"unicode": "00F5", "char": "õ", "category": "precomposed"},

    # Macron
    "Amacron": {"unicode": "0100", "char": "Ā", "category": "precomposed"},
    "amacron": {"unicode": "0101", "char": "ā", "category": "precomposed"},
    "Emacron": {"unicode": "0112", "char": "Ē", "category": "precomposed"},
    "emacron": {"unicode": "0113", "char": "ē", "category": "precomposed"},
    "Imacron": {"unicode": "012A", "char": "Ī", "category": "precomposed"},
    "imacron": {"unicode": "012B", "char": "ī", "category": "precomposed"},
    "Omacron": {"unicode": "014C", "char": "Ō", "category": "precomposed"},
    "omacron": {"unicode": "014D", "char": "ō", "category": "precomposed"},
    "Umacron": {"unicode": "016A", "char": "Ū", "category": "precomposed"},
    "umacron": {"unicode": "016B", "char": "ū", "category": "precomposed"},

    # Breve
    "Abreve": {"unicode": "0102", "char": "Ă", "category": "precomposed"},
    "abreve": {"unicode": "0103", "char": "ă", "category": "precomposed"},
    "Gbreve": {"unicode": "011E", "char": "Ğ", "category": "precomposed"},
    "gbreve": {"unicode": "011F", "char": "ğ", "category": "precomposed"},

    # Ring
    "Aring": {"unicode": "00C5", "char": "Å", "category": "precomposed"},
    "aring": {"unicode": "00E5", "char": "å", "category": "precomposed"},

    # Cedilla / comma-below-ish
    "Ccedilla": {"unicode": "00C7", "char": "Ç", "category": "precomposed"},
    "ccedilla": {"unicode": "00E7", "char": "ç", "category": "precomposed"},
    "Gcedilla": {"unicode": "0122", "char": "Ģ", "category": "precomposed"},
    "uni0123": {"unicode": "0123", "char": "ģ", "category": "precomposed"},
    "uni0136": {"unicode": "0136", "char": "Ķ", "category": "precomposed"},
    "uni0137": {"unicode": "0137", "char": "ķ", "category": "precomposed"},
    "uni013B": {"unicode": "013B", "char": "Ļ", "category": "precomposed"},
    "uni013C": {"unicode": "013C", "char": "ļ", "category": "precomposed"},
    "uni0145": {"unicode": "0145", "char": "Ņ", "category": "precomposed"},
    "uni0146": {"unicode": "0146", "char": "ņ", "category": "precomposed"},

    # Ogonek
    "Aogonek": {"unicode": "0104", "char": "Ą", "category": "precomposed"},
    "aogonek": {"unicode": "0105", "char": "ą", "category": "precomposed"},
    "Eogonek": {"unicode": "0118", "char": "Ę", "category": "precomposed"},
    "eogonek": {"unicode": "0119", "char": "ę", "category": "precomposed"},
    "Iogonek": {"unicode": "012E", "char": "Į", "category": "precomposed"},
    "iogonek": {"unicode": "012F", "char": "į", "category": "precomposed"},
    "Uogonek": {"unicode": "0172", "char": "Ų", "category": "precomposed"},
    "uogonek": {"unicode": "0173", "char": "ų", "category": "precomposed"},

    # Dot above
    "Edotaccent": {"unicode": "0116", "char": "Ė", "category": "precomposed"},
    "edotaccent": {"unicode": "0117", "char": "ė", "category": "precomposed"},
    "Zdotaccent": {"unicode": "017B", "char": "Ż", "category": "precomposed"},
    "zdotaccent": {"unicode": "017C", "char": "ż", "category": "precomposed"},
    "Cdotaccent": {"unicode": "010A", "char": "Ċ", "category": "precomposed"},
    "cdotaccent": {"unicode": "010B", "char": "ċ", "category": "precomposed"},

    # Caron
    "Ccaron": {"unicode": "010C", "char": "Č", "category": "precomposed"},
    "ccaron": {"unicode": "010D", "char": "č", "category": "precomposed"},
    "Dcaron": {"unicode": "010E", "char": "Ď", "category": "precomposed"},
    "dcaron": {"unicode": "010F", "char": "ď", "category": "precomposed"},
    "Ecaron": {"unicode": "011A", "char": "Ě", "category": "precomposed"},
    "ecaron": {"unicode": "011B", "char": "ě", "category": "precomposed"},
    "Lcaron": {"unicode": "013D", "char": "Ľ", "category": "precomposed"},
    "lcaron": {"unicode": "013E", "char": "ľ", "category": "precomposed"},
    "Ncaron": {"unicode": "0147", "char": "Ň", "category": "precomposed"},
    "ncaron": {"unicode": "0148", "char": "ň", "category": "precomposed"},
    "Rcaron": {"unicode": "0158", "char": "Ř", "category": "precomposed"},
    "rcaron": {"unicode": "0159", "char": "ř", "category": "precomposed"},
    "Scaron": {"unicode": "0160", "char": "Š", "category": "precomposed"},
    "scaron": {"unicode": "0161", "char": "š", "category": "precomposed"},
    "Tcaron": {"unicode": "0164", "char": "Ť", "category": "precomposed"},
    "tcaron": {"unicode": "0165", "char": "ť", "category": "precomposed"},
    "Zcaron": {"unicode": "017D", "char": "Ž", "category": "precomposed"},
    "zcaron": {"unicode": "017E", "char": "ž", "category": "precomposed"},

    # Double acute
    "Ohungarumlaut": {"unicode": "0150", "char": "Ő", "category": "precomposed"},
    "ohungarumlaut": {"unicode": "0151", "char": "ő", "category": "precomposed"},
    "Uhungarumlaut": {"unicode": "0170", "char": "Ű", "category": "precomposed"},
    "uhungarumlaut": {"unicode": "0171", "char": "ű", "category": "precomposed"},

    # Stroke / special letters
    "Lslash": {"unicode": "0141", "char": "Ł", "category": "precomposed"},
    "lslash": {"unicode": "0142", "char": "ł", "category": "precomposed"},
    "Dcroat": {"unicode": "0110", "char": "Đ", "category": "precomposed"},
    "dcroat": {"unicode": "0111", "char": "đ", "category": "precomposed"},
    "Hbar": {"unicode": "0126", "char": "Ħ", "category": "precomposed"},
    "hbar": {"unicode": "0127", "char": "ħ", "category": "precomposed"},
    "Oslash": {"unicode": "00D8", "char": "Ø", "category": "precomposed"},
    "oslash": {"unicode": "00F8", "char": "ø", "category": "precomposed"},

    # Ligatures
    "AE": {"unicode": "00C6", "char": "Æ", "category": "precomposed"},
    "ae": {"unicode": "00E6", "char": "æ", "category": "precomposed"},
    "OE": {"unicode": "0152", "char": "Œ", "category": "precomposed"},
    "oe": {"unicode": "0153", "char": "œ", "category": "precomposed"},

    # German sharp s
    "germandbls": {"unicode": "00DF", "char": "ß", "category": "precomposed"},
    "uni1E9E": {"unicode": "1E9E", "char": "ẞ", "category": "precomposed"},

    # Turkish I / dotless i
    "Idotaccent": {"unicode": "0130", "char": "İ", "category": "precomposed"},
    "dotlessi": {"unicode": "0131", "char": "ı", "category": "precomposed"},

    # Romanian comma below
    "Scommaaccent": {"unicode": "0218", "char": "Ș", "category": "precomposed"},
    "scommaaccent": {"unicode": "0219", "char": "ș", "category": "precomposed"},
    "Tcommaaccent": {"unicode": "021A", "char": "Ț", "category": "precomposed"},
    "tcommaaccent": {"unicode": "021B", "char": "ț", "category": "precomposed"},

    # Icelandic
    "Eth": {"unicode": "00D0", "char": "Ð", "category": "precomposed"},
    "eth": {"unicode": "00F0", "char": "ð", "category": "precomposed"},
    "Thorn": {"unicode": "00DE", "char": "Þ", "category": "precomposed"},
    "thorn": {"unicode": "00FE", "char": "þ", "category": "precomposed"},

    # Maltese
    "Gdotaccent": {"unicode": "0120", "char": "Ġ", "category": "precomposed"},
    "gdotaccent": {"unicode": "0121", "char": "ġ", "category": "precomposed"},

    # -----------------------------
    # SPACING DIACRITICS (optional)
    # -----------------------------
    "acute": {"unicode": "00B4", "char": "´", "category": "spacing"},
    "grave": {"unicode": "0060", "char": "`", "category": "spacing"},
    "circumflex": {"unicode": "005E", "char": "^", "category": "spacing"},
    "tilde": {"unicode": "007E", "char": "~", "category": "spacing"},
    "dieresis": {"unicode": "00A8", "char": "¨", "category": "spacing"},
    "cedilla": {"unicode": "00B8", "char": "¸", "category": "spacing"},
    "macron": {"unicode": "00AF", "char": "¯", "category": "spacing"},
    "breve": {"unicode": "02D8", "char": "˘", "category": "spacing"},
    "caron": {"unicode": "02C7", "char": "ˇ", "category": "spacing"},
    "ogonek": {"unicode": "02DB", "char": "˛", "category": "spacing"},
    "dotaccent": {"unicode": "02D9", "char": "˙", "category": "spacing"},
    "hungarumlaut": {"unicode": "02DD", "char": "˝", "category": "spacing"},
}

if 0:
    chars = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789¹²³ªº
    %$€¥£¢&*@#|áâàäåãæçéêèëíîìïıñóôòöõøœšßúûùüýÿžÂÀÄÅÃÆÇÉÊÈËÍÎÌÏÑÓÔÒÖÕØŒŠÛÙÜÝŸ
    ,:;-–—•.…“‘’‘ ‚ “”„‹›«»/\\?!¿¡()[]{}©®§+×=_°
    """

    names = []
    for gName in sorted(glyphs.keys()):
        if gName in LATIN_L_SET and gName not in LATIN_AX_SET:  
            names.append(LATIN_L_SET[gName].asSourceLine())
            chars += chr(LATIN_L_SET[gName].uni)
    print(''.join(names))
    print(len(chars), ''.join(sorted(chars)))

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
    # Build simple example source with only margins as attributes.

    for gName, gd in sorted(LATIN_AX_SET.items()):
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


