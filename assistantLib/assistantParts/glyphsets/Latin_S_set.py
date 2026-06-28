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

LATIN_S_SET_NAME = 'Latin S'
LATIN_S_SET_NAME_ITALIC = 'Latin S Italic'

LATIN_S_SET_LANGUAGES = (
    'Abron', 'Acheron', 'Achinese', 'Achuar-Shiwiar', 'Adamawa Fulfulde', 'Adangme', 
    'Afar', 'Afrikaans', 'Aguaruna', 'Amahuaca', 'Amarakaeri', 'Amis', 'Andaandi', 
    'Anuta', 'Ao Naga', 'Apinayé', 'Arabela', 'Aragonese', 'Arbëreshë Albanian', 
    'Arvanitika Albanian', 'Asháninka', 'Ashéninka Perené', 'Asu (Tanzania)', 'Atayal', 
    'Awa-Cuaiquer', 'Baatonum', 'Bafia', 'Bagirmi Fulfulde', 'Balinese', 'Balkan Romani', 
    'Bambara', 'Baoulé', 'Bari', 'Basque', 'Batak Dairi', 'Batak Karo', 'Batak Mandailing', 
    'Batak Simalungun', 'Batak Toba', 'Bemba (Zambia)', 'Bena (Tanzania)', 'Biali', 'Bikol', 
    'Bini', 'Bislama', 'Boko (Benin)', 'Bora', 'Borana-Arsi-Guji Oromo', 'Borgu Fulfulde', 
    'Bosnian', 'Breton', 'Bushi', 'Candoshi-Shapra', 'Caquinte', 'Caribbean Hindustani', 
    'Cashibo-Cacataibo', 'Cashinahua', 'Catalan', 'Cebuano', 'Central Aymara', 
    'Central Kurdish', 'Central Nahuatl', 'Central-Eastern Niger Fulfulde', 'Chachi', 
    'Chamorro', 'Chavacano', 'Chayahuita', 'Chiga', 'Chiltepec Chinantec', 'Chokwe', 
    'Chuukese', 'Cimbrian', 'Cofán', 'Congo Swahili', 'Cook Islands Māori', 'Cornish', 
    'Corsican', 'Creek', 'Crimean Tatar', 'Croatian', 'Czech', 'Danish', 'Dehu', 
    'Dendi (Benin)', 'Dimli', 'Dongolawi', 'Duala', 'Dyula', 'Eastern Abnaki', 
    'Eastern Arrernte', 'Eastern Maninkakan', 'Eastern Oromo', 'Embu', 'English', 
    'Ese Ejja', 'Fanti', 'Faroese', 'Fijian', 'Filipino', 'Finnish', 'French', 
    'Friulian', 'Ga', 'Gagauz', 'Galician', 'Ganda', 'Garifuna', 'Ga’anda', 'German', 
    'Gheg Albanian', 'Gilbertese', 'Gonja', 'Gooniyandi', 'Guadeloupean Creole French', 
    'Gusii', 'Haitian', 'Hani', 'Hausa', 'Hawaiian', 'Hiligaynon', 'Ho-Chunk', 'Hopi', 
    'Huastec', 'Hungarian', 'Hän', 'Ibibio', 'Icelandic', 'Igbo', 'Iloko', 'Inari Sami', 
    'Indonesian', 'Irish', 'Istro Romanian', 'Italian', 'Ixcatlán Mazatec', 
    'Jamaican Creole English', 'Japanese (Rōmaji)', #???
    'Javanese', 'Jola-Fonyi', "K‘iche'", 
    'Kabuverdianu', 'Kaingang', 'Kala Lagaw Ya', 'Kalaallisut', 'Kalenjin', 
    'Kamba (Kenya)', 'Kaonde', 'Kaqchikel', 'Karelian', 'Kashubian', 'Kekchí', 
    'Kenzi', 'Khasi', 'Kikuyu', 'Kimbundu', 'Kinyarwanda', 'Kirmanjki', 'Kituba (DRC)', 
    'Kongo', 'Konzo', 'Koyra Chiini Songhay', 'Koyraboro Senni Songhai', 'Krio', 
    'Kuanyama', 'Kven Finnish', 'Kwasio', 'Kölsch', 'Ladin', 'Ladino', 'Latgalian', 
    'Latin', 'Ligurian', 'Lingala', 'Lithuanian', 'Lombard', 'Low German', 'Lower Sorbian', 
    'Lozi', 'Luba-Katanga', 'Luba-Lulua', 'Lule Sami', 'Luo (Kenya and Tanzania)', 
    'Luxembourgish', 'Maasina Fulfulde', 'Macedo-Romanian', 'Makhuwa', 'Makhuwa-Meetto', 
    'Makonde', 'Makwe', 'Malagasy', 'Malaysian', 'Maltese', 'Mam', 'Manx', 'Maore Comorian', 
    'Maori', 'Mapudungun', 'Marshallese', 'Matsés', 'Mattokki', 'Mauritian Creole', 
    'Mende (Sierra Leone)', 'Meriam Mir', 'Meru', 'Meta’', 'Metlatónoc Mixtec', "Mi'kmaq", 
    'Minangkabau', 'Mirandese', 'Mohawk', 'Montagnais', 'Montenegrin', 'Munsee', 'Murrinh-Patha', 
    'Murui Huitoto', 'Muslim Tat', 'Mwani', 'Mískito', 'Naga Pidgin', 'Ndonga', 'Neapolitan', 
    'Ngazidja Comorian', 'Nigerian Fulfulde', 'Niuean', 'Nobiin', 'Nomatsiguenga', 
    'North Azerbaijani', 'North Marquesan', 'North Ndebele', 'Northern Kissi', 'Northern Kurdish', 
    'Northern Qiandong Miao', 'Northern Uzbek', 'Norwegian', 'Nyamwezi', 'Nyanja', 'Nyankole', 
    'Nyemba', 'Nzima', 'Occitan', 'Ojitlán Chinantec', 'Orma', 'Oroqen', 'Otuho', 'Palauan', 
    'Paluan', 'Pampanga', 'Papantla Totonac', 'Papiamento', 'Paraguayan Guaraní', 'Pedi', 
    'Picard', 'Pichis Ashéninka', 'Piemontese', 'Pijin', 'Pintupi-Luritja', 'Pipil', 'Pohnpeian', 
    'Polish', 'Portuguese', 'Potawatomi', 'Pulaar', 'Purepecha', 'Páez', 'Quechua', 'Romanian', 
    'Romansh', 'Rotokas', 'Rundi', 'Rwa', 'Samburu', 'Samoan', 'Sango', 'Sangu (Tanzania)', 
    'Saramaccan', 'Sardinian', 'Scottish Gaelic', 'Sena', 'Seri', 'Seselwa Creole French', 
    'Shambala', 'Sharanahua', 'Shawnee', 'Shilluk', 'Shipibo-Conibo', 'Shona', 'Shuar', 
    'Sicilian', 'Silesian', 'Slovak', 'Slovenian', 'Soga', 'Somali', 'Soninke', 'South Azerbaijani', 
    'South Marquesan', 'South Ndebele', 'Southern Aymara', 'Southern Dagaare', 
    'Southern Qiandong Miao', 'Southern Sami', 'Southern Sotho', 'Spanish', 'Sranan Tongo', 
    'Standard Estonian', 'Standard Latvian', 'Standard Malay', 'Sundanese', 'Susu', 'Swahili', 
    'Swati', 'Swedish', 'Swiss German', 'Tagalog', 'Tahitian', 'Taita', 'Talysh', 'Tasawaq', 
    'Tedim Chin', 'Teso', 'Tetum', 'Tetun Dili', 'Timne', 'Tiv', 'Toba', 'Tok Pisin', 'Tokelau', 
    'Tonga (Tonga Islands)', 'Tonga (Zambia)', 'Tosk Albanian', 'Tsakhur', 'Tsonga', 'Tswana', 
    'Tumbuka', 'Turkish', 'Turkmen', 'Tuvalu', 'Twi', 'Tzeltal', 'Tzotzil', 'Uab Meto', 'Umbundu', 
    'Upper Guinea Crioulo', 'Upper Sorbian', 'Venetian', 'Veps', 'Vlax Romani', 'Võro', 'Waama', 
    'Wallisian', 'Walloon', 'Walser', 'Wangaaybuwan-Ngiyambaa', 'Waorani', 'Waray (Philippines)', 
    'Warlpiri', 'Wasa', 'Wayuu', 'Welsh', 'West Central Oromo', 'West-Central Limba', 
    'Western Abnaki', 'Western Frisian', 'Western Niger Fulfulde', 'Wik-Mungkan', 'Wiradjuri', 
    'Wolof', 'Xavánte', 'Xhosa', 'Yagua', "Yanesha'", 'Yangben', 'Yanomamö', 'Yao', 'Yapese', 
    'Yindjibarndi', 'Yoruba', 'Yucateco', 'Zapotec', 'Zarma', 'Zulu', 'Zuni', 'Záparo')


# The "c" attribtes are redundant, if the @uni or @hex are defined, but they are offer easy searching in the source by char.
LATIN_S_SET = GDS = {

    #   .

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

    # rest of ascii

    'colon': GD(name='colon', uni=0x003A, hex='003A', c=':', l='period', r='period', isLower=True, comment=': COLON'),
    'cedilla': GD(name='cedilla', base='cedillacmb', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True),
    'cent': GD(name='cent', uni=0x00A2, hex='00A2', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='¢', isLower=True, comment='¢ CENT SIGN'),
    'cent.alt': GD(name='cent.alt', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='¢ CENT SIGN'),
    'comma': GD(name='comma', uni=0x002C, hex='002C', c=',', l='off', isLower=True, comment=', separator, decimal'),
    'copyright': GD(name='copyright', uni=0x00A9, hex='00A9', c='©', l='O', r='O', isLower=True, base='largecircle', comment='© COPYRIGHT SIGN'),
    'copyright.uc': GD(name='copyright.uc', l='copyright', r='copyright', base='copyright', isLower=False, comment='© COPYRIGHT SIGN'),
    'copyrightsound': GD(l='copyright', r='copyright', uni=0x2117, base='largecircle', name='copyrightsound'),
    'copyrightsound.uc': GD(l='copyright', r='copyright', base='copyrightsound', name='copyrightsound.uc'),
    'largecircle': GD(l='O', r='O', uni=0x25ef, c='◯', name='largecircle', comment='circle for ® trade mark sign, registered', useSkewRotate=True, addItalicExtremePoints=True),

    'exclam': GD(name='exclam', uni=0x0021, hex='0021', c='!', l2r='self', isLower=True, comment='! factorial'),
    'exclamdown': GD(name='exclamdown', uni=0x00A1, hex='00A1', c='¡', l2r='exclam', r2l='exclam', isLower=True, comment='¡ INVERTED EXCLAMATION MARK'),
    'exclamdown.uc': GD(name='exclamdown.uc', c='¡', l='exclamdown', r='exclamdown', base='exclamdown', isLower=False, comment='¡ INVERTED EXCLAMATION MARK'),

    'hyphen': GD(name='hyphen', uni=0x002D, hex='002D', c='-', l2r='self', isLower=True, comment='- minus sign, hyphen'),
    'hyphen.uc': GD(name='hyphen.uc', l='hyphen', r='hyphen', base='hyphen', isLower=False, comment='- minus sign, hyphen'),
    'endash': GD(name='endash', uni=0x2013, hex='2013', c='–', l=GD.CAT_CENTER, w=GD.CAT_EM_WIDTH2, isLower=True, comment='– EN DASH'),
    'endash.uc': GD(name='endash.uc', isLower=False, l=GD.CAT_CENTER, w=GD.CAT_EM_WIDTH2, base='endash', comment='– EN DASH'),
    'emdash': GD(g2='hyphen', g1='hyphen', l=GD.CAT_CENTER, w=GD.CAT_EM_WIDTH, uni=0x2014, c='—', name='emdash', comment='— EM DASH', anchors=[]),
    'emdash.uc': GD(g2='hyphen', g1='hyphen', l=GD.CAT_CENTER, w=GD.CAT_EM_WIDTH, name='emdash.uc', base='emdash', isLower=False, comment='— EM DASH Uppercase', anchors=[]),
    'horizontalbar': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, uni=0x2015, c='―', name='horizontalbar', srcName='emdash', anchors=[]),
    'horizontalbar.uc': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='horizontalbar.uc', base='horizontalbar', isLower=False, comment='Horizontal base Uppercase', anchors=[]),

    'hungarumlaut': GD(name='hungarumlaut', uni=0x02DD, hex='02DD', c='˝', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='hungarumlautcmb', isLower=True, comment='˝ DOUBLE ACUTE ACCENT'),

    'macron': GD(name='macron', uni=0x00AF, hex='00AF', c='¯', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='macroncmb', srcName='uni00AF', isLower=True, comment='¯ spacing macron'),

    'paragraph': GD(name='paragraph', uni=0x00B6, hex='00B6', c='¶', l='zerosuperior', r='H', isLower=True, comment='¶ section sign, european'),
    'parenleft': GD(name='parenleft', uni=0x0028, hex='0028', c='(', isLower=True, comment='( parenthesis, opening'),
    #'parenleft.uc': GD(name='parenleft.uc', srcName='parenleft', l='parenleft', r='parenleft', isLower=False, comment='( parenthesis, opening for capitals'),
    'parenright': GD(name='parenright', uni=0x0029, hex='0029', c=')', l2r='parenleft', r2l='parenleft', isLower=True, comment=') RIGHT PARENTHESIS'),
    #'parenright.uc': GD(name='parenright.uc', srcName='parenright', l2r='parenleft', r2l='parenleft', isLower=False, comment='( parenthesis, for capitals'),
    'percent': GD(name='percent', uni=0x0025, hex='0025', c='%', l='zerosuperior', r='zerosuperior', isLower=True, base='zero.numr', accents=['fraction', 'zero.dnom'], comment='% PERCENT SIGN', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPERIOR_HEIGHT, overshoot=GD.CAT_SUPERIOR_OVERSHOOT),
    'percent.tab': GD(name='percent.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, comment='% PERCENT SIGN TAB'),
    'perthousand': GD(l='zerosuperior', r='zerosuperior', uni=0x2030, c='‰', name='perthousand', base='percent', accents=['zero.dnom'], comment='‰ per thousand', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPERIOR_HEIGHT, overshoot=GD.CAT_SUPERIOR_OVERSHOOT),
    'perthousand.tab': GD(name='perthousand.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH),
    'period': GD(name='period', uni=0x002E, hex='002E', c='.', l2r='self', isLower=True, fixSpacing=False, comment='. point, decimal'),
    #'period.uc': GD(name='period.uc', l2r='self', isLower=False, fixSpacing=False, base='period', comment='. point, decimal'),
    'ellipsis': GD(name='ellipsis', uni=0x2026, hex='2026', c='…', l='period', r='period', isLower=True, comment='… three dot leader'),
    'periodcentered': GD(name='periodcentered', uni=0x00B7, hex='00B7', c='·', l='period', r='period', isLower=True),
    'periodcentered.uc': GD(name='periodcentered.uc', base='periodcentered', l='period', r='period', isLower=False),
    'partialdiff': GD(name='partialdiff', uni=0x2202, hex='2202', c='∂', l='o', r='O', isLower=True, comment='∂ PARTIAL DIFFERENTIAL'),

    'pi': GD(name='pi', uni=0x03C0, hex='03C0', c='π', isLower=True),

    'question': GD(name='question', uni=0x003F, hex='003F', c='?', isLower=True, comment='? QUESTION MARK'),
    'questiondown': GD(name='questiondown', uni=0x00BF, hex='00BF', c='¿', l2r='question', r2l='question', isLower=True, comment='¿ turned question mark'),
    'questiondown.uc': GD(name='questiondown.uc', l='questiondown', r='questiondown', base='questiondown', isLower=False, comment='¿ turned question mark'),

    'registered': GD(name='registered', uni=0x00AE, hex='00AE', c='®', l='copyright', r='copyright', base='largecircle', isLower=True, comment='® trade mark sign, registered'),
    'registered.uc': GD(name='registered.uc', l='copyright', r='copyright', base='registered', isLower=False, comment='® trade mark sign, registered'),

    'section': GD(name='section', uni=0x00A7, hex='00A7', c='§', l='s', r='s', isLower=True, comment='§ SECTION SIGN'),
    'semicolon': GD(name='semicolon', uni=0x003B, hex='003B', c=';', l='comma', r='comma', isLower=True, comment='; SEMICOLON'),
    'slash': GD(name='slash', uni=0x002F, hex='002F', c='/', l2r='self', isLower=False, comment='/ virgule'),
    'sterling': GD(name='sterling', uni=0x00A3, hex='00A3', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='£', isLower=True, comment='£ sterling, pound'),

    'trademark': GD(name='trademark', uni=0x2122, hex='2122', c='™', isLower=True, comment='™ TRADE MARK SIGN'),

    'underscore': GD(name='underscore', uni=0x005F, hex='005F', c='_', isLower=True, comment='_ underscore, spacing'),

    # Standard superiors and inferiors, spaced by margins of /plussuperior and /periodsuperior

    'plussuperior': GD(name='plussuperior', uni=0x207A, hex='207A', c='⁺', l2r='self', ), # Source of margins
    'minussuperior': GD(name='minussuperior', uni=0x207B, hex='207B', c='⁻', l='plussuperior', r='plussuperior', srcName='plussuperior'),
    'equalsuperior': GD(name='equalsuperior', uni=0x207C, hex='207C', c='⁼', l='plussuperior', r='plussuperior', ),

    'plusinferior': GD(name='plusinferior', uni=0x208A, hex='208A', c='₊', base='plussuperior', l='plussuperior', r='zerosuperior', ),
    'minusinferior': GD(name='minusinferior', uni=0x208B, hex='208B', c='₋', base='minussuperior', l='minussuperior', r='zerosuperior', ),
    'equalinferior': GD(name='equalinferior', uni=0x208C, hex='208C', c='₌', base='equalsuperior', l='equalsuperior', r='zerosuperior', ),

    'periodsuperior': GD(name='periodsuperior', l2r='self', ),
    'commasuperior': GD(name='commasuperior', l='periodsuperior', r='periodsuperior', ),
    'parenleftsuperior': GD(name='parenleftsuperior', uni=0x207D, hex='207D', c='⁽', l='plussuperior', r='plussuperior', ),
    'parenrightsuperior': GD(name='parenrightsuperior', uni=0x207E, hex='207E', c='⁾', l='plussuperior', r='plussuperior', ),

    'periodinferior': GD(name='periodinferior', base='periodsuperior', l='periodsuperior', r='periodsuperior', ),
    'commainferior': GD(name='commainferior', base='commasuperior', l='commasuperior', r='commasuperior', ),
    'parenleftinferior': GD(name='parenleftinferior', uni=0x208D, hex='208D', c='₍', base='parenleftsuperior', l='parenleftsuperior', r='parenleftsuperior', ),
    'parenrightinferior': GD(name='parenrightinferior', uni=0x208E, hex='208E', c='₎', base='parenrightsuperior', l='parenrightsuperior', r='parenrightsuperior', ),

    'semicolonsuperior': GD(name='semicolonsuperior', l='periodsuperior', r='periodsuperior'),
    'quotedblrightsuperior': GD(name='quotedblrightsuperior', l='periodsuperior', r='periodsuperior', isLower=False),
    'quoteleftsuperior': GD(name='quoteleftsuperior', l='periodsuperior', r='periodsuperior', isLower=False),
    'quoterightsuperior': GD(name='quoterightsuperior', l='periodsuperior', r='periodsuperior', isLower=False),
    'quotedblleftsuperior': GD(name='quotedblleftsuperior', l='periodsuperior', r='periodsuperior', isLower=False),

    'zerosuperior': GD(name='zerosuperior', uni=0x2070, hex='2070', c='⁰', l='plussuperior', r='plussuperior', isLower=True, comment='¹ SUPERSCRIPT ZERO'),
    'onesuperior': GD(name='onesuperior', uni=0x00B9, hex='00B9', c='¹', l='plussuperior', r='plussuperior', isLower=True, comment='¹ SUPERSCRIPT ONE'),
    'twosuperior': GD(name='twosuperior', uni=0x00B2, hex='00B2', c='²', l='plussuperior', r='plussuperior', isLower=False, comment='² TWO, SUPERSCRIPT'),
    'threesuperior': GD(name='threesuperior', uni=0x00B3, hex='00B3', c='³', l='plussuperior', r='plussuperior', isLower=False, comment='³ THREE, SUPERSCRIPT'),
    'foursuperior': GD(name='foursuperior', uni=0x2074, hex='2074', c='⁴', l='plussuperior', r='plussuperior', isLower=False, comment='³ FOUR, SUPERSCRIPT'),
    'fivesuperior': GD(name='fivesuperior', uni=0x2075, hex='2075', c='⁵', l='plussuperior', r='plussuperior', isLower=False, comment='³ FIVE, SUPERSCRIPT'),
    'sixsuperior': GD(name='sixsuperior', uni=0x2076, hex='2076', c='⁶', l='plussuperior', r='plussuperior', isLower=False, comment='³ SIX, SUPERSCRIPT'),
    'sevensuperior': GD(name='sevensuperior', uni=0x2077, hex='2077', c='⁷', l='plussuperior', r='plussuperior', isLower=False, comment='³ SEVEN, SUPERSCRIPT'),
    'eightsuperior': GD(name='eightsuperior', uni=0x2078, hex='2078', c='⁸', l='plussuperior', r='plussuperior', isLower=False, comment='³ EIGHT, SUPERSCRIPT'),
    'ninesuperior': GD(name='ninesuperior', uni=0x2079, hex='2079', c='⁹', l='plussuperior', r='plussuperior', isLower=False, comment='³ NINE, SUPERSCRIPT'),

    'zeroinferior': GD(name='zeroinferior', uni=0x2080, hex='2080', c='₀', l='zerosuperior', r='zerosuperior', base='zerosuperior', isLower=True, comment='¹ SUPERSCRIPT ZERO'),
    'oneinferior': GD(name='oneinferior', uni=0x2081, hex='2081', c='₁', l='onesuperior', r='onesuperior', base='onesuperior', isLower=True, comment='¹ SUPERSCRIPT ONE'),
    'twoinferior': GD(name='twoinferior', uni=0x2082, hex='2082', c='₂', l='twosuperior', r='twosuperior', base='twosuperior', isLower=False, comment='² TWO, SUPERSCRIPT'),
    'threeinferior': GD(name='threeinferior', uni=0x2083, hex='2083', c='₃', l='threesuperior', r='threesuperior', base='threesuperior', isLower=False, comment='³ THREE, SUPERSCRIPT'),
    'fourinferior': GD(name='fourinferior', uni=0x2084, hex='2084', c='₄', l='foursuperior', r='foursuperior', base='foursuperior', isLower=False, comment='³ FOUR, SUPERSCRIPT'),
    'fiveinferior': GD(name='fiveinferior', uni=0x2085, hex='2085', c='₅', l='fivesuperior', r='fivesuperior', base='fivesuperior', isLower=False, comment='³ FIVE, SUPERSCRIPT'),
    'sixinferior': GD(name='sixinferior', uni=0x2086, hex='2086', c='₆', l='sixsuperior', r='sixsuperior', base='sixsuperior', isLower=False, comment='³ SIX, SUPERSCRIPT'),
    'seveninferior': GD(name='seveninferior', uni=0x2087, hex='2087', c='₇', l='sevensuperior', r='sevensuperior', base='sevensuperior', isLower=False, comment='³ SEVEN, SUPERSCRIPT'),
    'eightinferior': GD(name='eightinferior', uni=0x2088, hex='2088', c='₈', l='eightsuperior', r='eightsuperior', base='eightsuperior', isLower=False, comment='³ EIGHT, SUPERSCRIPT'),
    'nineinferior': GD(name='nineinferior', uni=0x2089, hex='2089', c='₉', l='ninesuperior', r='ninesuperior', base='ninesuperior', isLower=False, comment='³ NINE, SUPERSCRIPT'),

    'zero.numr': GD(name='zero.numr', base='zerosuperior', l='zerosuperior', r='zerosuperior', isLower=True, comment='⁰ SUPERSCRIPT ZERO'),
    'one.numr': GD(name='one.numr', base='onesuperior', l='onesuperior', r='onesuperior', isLower=True, comment='¹ SUPERSCRIPT ONE'),
    'two.numr': GD(name='two.numr', base='twosuperior', l='twosuperior', r='twosuperior', isLower=False, comment='² TWO, SUPERSCRIPT'),
    'three.numr': GD(name='three.numr', base='threesuperior', l='threesuperior', r='threesuperior', isLower=False, comment='³ THREE, SUPERSCRIPT'),
    'four.numr': GD(name='four.numr', base='foursuperior', l='foursuperior', r='foursuperior', isLower=False, comment='⁴ FOUR, SUPERSCRIPT'),
    'five.numr': GD(name='five.numr', base='fivesuperior', l='fivesuperior', r='fivesuperior', isLower=False, comment='⁵ FIVE, SUPERSCRIPT'),
    'six.numr': GD(name='six.numr', base='sixsuperior', l='sixsuperior', r='sixsuperior', isLower=False, comment='⁶ SIX, SUPERSCRIPT'),
    'seven.numr': GD(name='seven.numr', base='sevensuperior', l='sevensuperior', r='sevensuperior', isLower=False, comment='⁷ SEVEN, SUPERSCRIPT'),
    'eight.numr': GD(name='eight.numr', base='eightsuperior', l='eightsuperior', r='eightsuperior', isLower=False, comment='⁸ EIGHT, SUPERSCRIPT'),
    'nine.numr': GD(name='nine.numr', base='ninesuperior', l='ninesuperior', r='ninesuperior', isLower=False, comment='⁹ NINE, SUPERSCRIPT'),

    'zero.dnom': GD(name='zero.dnom', base='zerosuperior', l='zerosuperior', r='zerosuperior', isLower=True, comment='¹ SUBSCRIPT ZERO'),
    'one.dnom': GD(name='one.dnom', base='onesuperior', l='onesuperior', r='onesuperior', isLower=True, comment='¹ SUBSCRIPT ONE'),
    'two.dnom': GD(name='two.dnom', base='twosuperior', l='twosuperior', r='twosuperior', isLower=False, comment='² TWO, SUBSCRIPT'),
    'three.dnom': GD(name='three.dnom', base='threesuperior', l='threesuperior', r='threesuperior', isLower=False, comment='³ THREE, SUBSCRIPT'),
    'four.dnom': GD(name='four.dnom', base='foursuperior', l='foursuperior', r='foursuperior', isLower=False, comment='³ FOUR, SUBSCRIPT'),
    'five.dnom': GD(name='five.dnom', base='fivesuperior', l='fivesuperior', r='fivesuperior', isLower=False, comment='³ FIVE, SUBSCRIPT'),
    'six.dnom': GD(name='six.dnom', base='sixsuperior', l='sixsuperior', r='sixsuperior', isLower=False, comment='³ SIX, SUBSCRIPT'),
    'seven.dnom': GD(name='seven.dnom', base='sevensuperior', l='sevensuperior', r='sevensuperior', isLower=False, comment='³ SEVEN, SUBSCRIPT'),
    'eight.dnom': GD(name='eight.dnom', base='eightsuperior', l='eightsuperior', r='eightsuperior', isLower=False, comment='³ EIGHT, SUBSCRIPT'),
    'nine.dnom': GD(name='nine.dnom', base='ninesuperior', l='ninesuperior', r='ninesuperior', isLower=False, comment='³ NINE, SUBSCRIPT'),

    # Old-style figures (exception)
    'one.onum': GD(name='one.onum', l='off', l2r='self', srcName='I.sc', isLower=True, comment='¹Old-style one'),

    # Math not on math-width
        
    'numbersign': GD(name='numbersign', uni=0x0023, hex='0023', c='#', l2r='self', isLower=True, comment='# pound sign'),
    'numbersign.uc': GD(name='numbersign.uc', l='numbersign', r='numbersign', base='numbersign', isLower=False, comment='# pound sign for capitals'),
    'degree': GD(name='degree', uni=0x00B0, hex='00B0', c='°', isLower=True, comment='° DEGREE SIGN'),
    'ordfeminine': GD(name='ordfeminine', uni=0x00AA, hex='00AA', c='ª', isLower=True, comment='ª ORDINAL INDICATOR, FEMININE'),
    'ordmasculine': GD(name='ordmasculine', uni=0x00BA, hex='00BA', c='º', isLower=True, comment='º ORDINAL INDICATOR, MASCULINE'),

    # Math on math-width ( == tab-width)

    'plusminus': GD(name='plusminus', uni=0x00B1, hex='00B1', c='±', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='± PLUS-MINUS SIGN'),
    'plus': GD(name='plus', uni=0x002B, hex='002B', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='+', isLower=True, comment='+ PLUS SIGN'),
    'minus': GD(name='minus', uni=0x2212, hex='2212', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, c='−', isLower=True, srcName='plus', comment='− MINUS SIGN'),
    'multiply': GD(name='multiply', uni=0x00D7, hex='00D7', c='×', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='× product, cartesian'),
    'divide': GD(name='divide', uni=0x00F7, hex='00F7', c='÷', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='÷ obelus'),
    'numbersign.tab': GD(name='numbersign.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='numbersign', isLower=True, comment='# pound sign tabular'),
    'equal': GD(name='equal', uni=0x003D, hex='003D', c='=', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, comment='= EQUALS SIGN'),
    'notequal': GD(name='notequal', uni=0x2260, hex='2260', c='≠', base='equal', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='≠ NOT EQUAL TO'),
    'greater': GD(name='greater', uni=0x003E, hex='003E', c='>', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='> GREATER-THAN SIGN'),
    'greaterequal': GD(name='greaterequal', uni=0x2265, hex='2265', c='≥', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='≥ GREATER-THAN OR EQUAL TO'),
    'less': GD(name='less', uni=0x003C, hex='003C', c='<', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='< LESS-THAN SIGN'),
    'lessequal': GD(name='lessequal', uni=0x2264, hex='2264', c='≤', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='≤ LESS-THAN OR EQUAL TO'),
    'logicalnot': GD(name='logicalnot', uni=0x00AC, hex='00AC', c='¬', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, comment='¬ NOT SIGN'),
    'lozenge': GD(l2r='lozenge', uni=0x25ca, c='◊', name='lozenge', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, comment='◊ LOZENGE', anchors=[]),
    'approxequal': GD(name='approxequal', uni=0x2248, hex='2248', c='≈', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='asciitilde', accents=['asciitilde'], isLower=True, gid=1496, comment='≈ EQUAL TO, ALMOST'),

    # Currencies: By default all are centered on math-width == figure-width

    'dollar': GD(name='dollar', uni=0x0024, hex='0024', c='$', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='S', isLower=False, comment='$ milreis'),
    'dollar.alt': GD(name='dollar.alt', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='S', isLower=False, comment='$ milreis'),
    'bitcoin': GD(uni=0x20bf, c='₿', name='bitcoin', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, base='B', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
    'bitcoin.alt': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='bitcoin.alt', base='B', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
    'won': GD(name='won', uni=0x20A9, hex='20A9', c='₩', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False, srcName='W', comment="South Korean Won"),
    'yen': GD(name='yen', uni=0x00A5, hex='00A5', c='¥', isLower=True, l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, comment='¥ yuan sign'),
    #/Fhook/florin (Ƒƒ)
    # In African languages, lowercase f with hook is an actual letter, even if it shares the codepoint with the Florin currency.    
    'florin': GD(name='florin', uni=0x0192, hex='0192', l='off', r='f', comment='ƒ script f, latin small letter, same as African fhook'),
    'rupeeIndian': GD(name='rupeeIndian', uni=0x20B9, hex='20B9', c='₹', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, srcName='Rupee'),
    'newsheqel': GD(name='newsheqel', uni=0x20AA, hex='20AA', c='₪', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH),
    'peso': GD(name='peso', uni=0x20B1, hex='20B1', c='₱', base='P',l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False),
    'hryvnia': GD(name='hryvnia', uni=0x20B4, hex='20B4', c='₴', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=False),
    'dong': GD(name='dong', uni=0x20AB, hex='20AB', c='₫', base='d', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, isLower=True, gid=1444, comment='₫ vietnamese currency'),
    'cedi': GD(name='cedi', uni=0x20B5, hex='20B5', c='₵', base='C', l='C', r='C', isLower=True, comment='₵100 means 100 Ghanaian cedis'),
    'currency': GD(name='currency', uni=0x00A4, hex='00A4', c='¤', isLower=True, l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, comment='¤ CURRENCY SIGN'),

    # Superior currency

    'yensuperior': GD(name='yensuperior', l='zerosuperior', r='zerosuperior', isLower=False),
    'eurosuperior': GD(name='eurosuperior', l='zerosuperior', r='zerosuperior', isLower=False),
    'dollarsuperior': GD(name='dollarsuperior', l='zerosuperior', r='zerosuperior', isLower=False),
    'centsuperior': GD(name='centsuperior', l='zerosuperior', r='zerosuperior', isLower=False),
    'sterlingsuperior': GD(name='sterlingsuperior', l='zerosuperior', r='zerosuperior', isLower=False),

    # Fixed fractions

    'fraction': GD(l=GD.CAT_CENTER, w=GD.CAT_FRACTION_WIDTH, name='fraction', uni=0x2044, c='⁄', isLower=False, comment='⁄ solidus'),

    'onehalf': GD(name='onehalf', uni=0x00BD, hex='00BD', c='½', base='one.numr', accents=['fraction', 'two.dnom'], isLower=False, comment='½ VULGAR FRACTION ONE HALF'),
    'onequarter': GD(name='onequarter', uni=0x00BC, hex='00BC', c='¼', base='one.numr', accents=['fraction', 'four.dnom'], isLower=True, comment='¼ VULGAR FRACTION ONE QUARTER'),
    'oneseventh': GD(name='oneseventh', uni=0x2150, hex='2150', c='⅐', l='one.numr', r='seven.dnom', base='one.numr', accents=['fraction', 'seven.dnom'], isLower=False),
    'onesixth': GD(name='onesixth', uni=0x2159, hex='2159', c='⅙', l='one.numr', r='six.dnom', base='one.numr', accents=['fraction', 'six.dnom'], isLower=False),
    'threequarters': GD(name='threequarters', uni=0x00BE, hex='00BE', c='¾', base='three.numr', accents=['fraction', 'four.dnom'], isLower=False, comment='¾ VULGAR FRACTION THREE QUARTERS'),
   
    # A

    'A': GD(name='A', uni=0x0041, hex='0041', c='A', l2r='self', anchorTopX='TopX',anchorTopY='TopY', anchors=['bottom', 'middle', 'ogonek', 'topleft', 'top'], comment='A Uppercase Alphabet, Latin'),
    'AE': GD(name='AE', uni=0x00C6, hex='00C6', c='Æ', l='A', r='E', anchorTopX='TopX', anchors=['bottom', 'middle', 'top'], comment='Æ ligature ae, latin capital'),

    'Aacute': GD(name='Aacute', uni=0x00C1, hex='00C1', c='Á', l='A', r='A', base='A', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER'),
    'Abreve': GD(name='Abreve', uni=0x0102, hex='0102', c='Ă', l='A', r='A', base='A', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE'),
    'Acaron': GD(name='Acaron', uni=0x01CD, hex='01CD', c='Ǎ', l='A', r='A', base='A', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek']),
    'Acircumflex': GD(name='Acircumflex', uni=0x00C2, hex='00C2', c='Â', l='A', r='A', base='A', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Adieresis': GD(name='Adieresis', uni=0x00C4, hex='00C4', c='Ä', l='A', r='A', base='A', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Adotbelow': GD(name='Adotbelow', uni=0x1EA0, hex='1EA0', c='Ạ', l='A', r='A', base='A', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ạ LATIN CAPITAL LETTER A WITH DOT BELOW'),
    'Agrave': GD(name='Agrave', uni=0x00C0, hex='00C0', c='À', l='A', r='A', base='A', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
    'Amacron': GD(name='Amacron', uni=0x0100, hex='0100', c='Ā', l='A', r='A', base='A', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ā Latin, European'),
    'Aogonek': GD(name='Aogonek', uni=0x0104, hex='0104', c='Ą', l='A', r='A', base='A', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),
    'Atilde': GD(name='Atilde', uni=0x00C3, hex='00C3', c='Ã', l='A', r='A', base='A', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top', 'ogonek'], comment='Ã A WITH TILDE, LATIN CAPITAL LETTER'),
    # Fix ring position manually for italics.
    'Aring': GD(name='Aring', uni=0x00C5, hex='00C5', c='Å', l='A', r='A', base='A', autoFixComponentPositions=False, accents=['ringcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Å RING ABOVE, LATIN CAPITAL LETTER A WITH'),

    # B

    'B': GD(name='B', uni=0x0042, hex='0042', c='B', l='H', anchors=['bottom', 'middle', 'top'], comment='B LATIN CAPITAL LETTER B'),
    'Bdotbelow': GD(name='Bdotbelow', uni=0x1E04, hex='1E04', c='Ḅ', l='H', r='B', base='B', accents=['dotbelowcmb'], srcName='uni1E04', anchors=['bottom', 'middle', 'top']),
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
    'Ddotbelow': GD(name='Ddotbelow', uni=0x1E0C, hex='1E0C', c='Ḍ', l='D', r='D', base='D', accents=['dotbelowcmb'], srcName='uni1E0C', anchors=['bottom', 'middle', 'top']),
    'Dhook': GD(name='Dhook', uni=0x018A, hex='018A', c='Ɗ', l=GD.CAT_HAIR_WIDTH, r='D', base='D', comment='Ɗ D WITH HOOK, LATIN CAPITAL LETTER'),
    'Delta': GD(name='Delta', uni=0x0394, hex='0394', c='Δ', l='off', l2r='self', comment='∆ symmetric difference'),

    # E

    'E': GD(name='E', uni=0x0045, hex='0045', c='E', l='H', anchorBottomX='BottomX', anchors=['bottom', 'middle', 'ogonek', 'topleft', 'top'], comment='E'),
    'Eacute': GD(name='Eacute', uni=0x00C9, hex='00C9', c='É', l='H', r='E', base='E', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='É E WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ebreve': GD(name='Ebreve', uni=0x0114, hex='0114', c='Ĕ', l='H', r='E', base='E', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ĕ'),
    'Ecaron': GD(name='Ecaron', uni=0x011A, hex='011A', c='Ě', l='H', r='E', base='E', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ě'),
    'Ecircumflex': GD(name='Ecircumflex', uni=0x00CA, hex='00CA', c='Ê', l='H', r='E', base='E', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ê E WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Edieresis': GD(name='Edieresis', uni=0x00CB, hex='00CB', c='Ë', l='H', r='E', base='E', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ë E WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Edotaccent': GD(name='Edotaccent', uni=0x0116, hex='0116', c='Ė', l='H', r='E', base='E', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Edotbelow': GD(name='Edotbelow', uni=0x1EB8, hex='1EB8', c='Ẹ', l='H', r='E', base='E', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ẹ LATIN CAPITAL LETTER E WITH DOT BELOW'),
    'Egrave': GD(name='Egrave', uni=0x00C8, hex='00C8', c='È', l='H', r='E', base='E', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='È E WITH GRAVE, LATIN CAPITAL LETTER'),
    'Emacron': GD(name='Emacron', uni=0x0112, hex='0112', c='Ē', l='H', r='E', base='E', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ē'),
    'Eng': GD(name='Eng', uni=0x014A, hex='014A', c='Ŋ', l='N', r='N', comment='Ŋ'),
    'Eogonek': GD(name='Eogonek', uni=0x0118, hex='0118', c='Ę', l='E', w='E', base='E', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ę'),
    'Eopen': GD(name='Eopen', uni=0x0190, hex='0190', c='Ɛ', r='off', r2l='B', srcName='uni0190', comment='Ɛ OPEN E, LATIN CAPITAL LETTER'),
    'Ereversed': GD(name='Ereversed', uni=0x018E, hex='018E', c='Ǝ', r2l='E', l2r='E', srcName='E', comment='Ǝ turned e, latin capital letter'),
    'Eth': GD(name='Eth', uni=0x00D0, hex='00D0', c='Ð', r='D', base='D', comment='Ð ETH, LATIN CAPITAL LETTER'),
    'Etilde': GD(name='Etilde', uni=0x1EBC, hex='1EBC', c='Ẽ', l='E', r='E', base='E', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ẽ LATIN CAPITAL LETTER E WITH TILDE'),
    'Euro': GD(g1='C', g2='Euro', uni=0x20AC, c='€', l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, srcName='C', name='Euro'),
    'Euro.tab': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, srcName='Euro', name='Euro.tab'),

    # F

    'F': GD(name='F', uni=0x0046, hex='0046', c='F', l='H', anchors=['bottom', 'middle', 'top'], comment='F'),

    # G

    'G': GD(name='G', uni=0x0047, hex='0047', c='G', l='O', anchorTopX='TopX', anchorBottomX='BottomX', anchors=['bottom', 'middle', 'top'], comment='G'),
    'Gbreve': GD(name='Gbreve', uni=0x011E, hex='011E', c='Ğ', l='G', r='G', base='G', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ğ'),
    'Gcaron': GD(name='Gcaron', uni=0x01E6, hex='01E6', c='Ǧ', l='G', r='G', base='G', accents=['caroncmb.uc'], srcName='uni01E6', anchors=['bottom', 'middle', 'top']),
    'Gcircumflex': GD(name='Gcircumflex', uni=0x011C, hex='011C', c='Ĝ', l='G', r='G', base='G', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ĝ'),
    'Gcommaaccent': GD(name='Gcommaaccent', uni=0x0122, hex='0122', c='Ģ', l='G', r='G', base='G', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ģ'),
    'Gdotaccent': GD(name='Gdotaccent', uni=0x0120, hex='0120', c='Ġ', l='G', r='G', base='G', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ġ'),
    'Germandbls': GD(name='Germandbls', uni=0x1E9E, hex='1E9E', c='ẞ', l='f', r='s', srcName='uni1E9E'),
    'Germandbls.alt': GD(name='Germandbls', l='Germandbls', r='Germandbls', srcName='uni1E9E'),
    'Gmacron': GD(name='Gmacron', uni=0x1E20, hex='1E20', c='Ḡ', l='G', r='G', base='G', accents=['macroncmb.uc'], srcName='uni1E20', anchors=['bottom', 'middle', 'top']),

    # H

    'H': GD(name='H', uni=0x0048, hex='0048', c='H', l2r='self', anchors=['bottom', 'middle', 'topleft', 'top'], comment='H'),
    'Hbar': GD(name='Hbar', uni=0x0126, hex='0126', c='Ħ', l='Eth', l2r='self', base='H', comment='Ħ'),
    'Hcircumflex': GD(name='Hcircumflex', uni=0x0124, hex='0124', c='Ĥ', l='H', r='H', base='H', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ĥ'),
    'Hdieresis': GD(name='Hdieresis', uni=0x1E26, hex='1E26', c='Ḧ', l='H', r='H', base='H', accents=['dieresiscmb.uc'], srcName='uni1E26', anchors=['bottom', 'middle', 'top']),
    'Hdotbelow': GD(name='Hdotbelow', uni=0x1E24, hex='1E24', c='Ḥ', l='H', r='H', base='H', accents=['dotbelowcmb'], srcName='uni1E24', anchors=['bottom', 'middle', 'top']),

    # I

    'I': GD(name='I', uni=0x0049, hex='0049', c='I', l='H', r='H', srcName='H', anchors=['bottom', 'middle', 'ogonek', 'topleft', 'top'], comment='I'),
    'Iacute': GD(name='Iacute', uni=0x00CD, hex='00CD', c='Í', w='I', bl='I', base='I', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ibreve': GD(name='Ibreve', uni=0x012C, hex='012C', c='Ĭ', w='I', bl='I', base='I', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ĭ'),
    'Icaron': GD(name='Icaron', uni=0x01CF, hex='01CF', c='Ǐ', w='I', bl='I', base='I', accents=['caroncmb.uc'], srcName='uni01CF', anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Icircumflex': GD(name='Icircumflex', uni=0x00CE, hex='00CE', c='Î', w='I', bl='I', base='I', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Idieresis': GD(name='Idieresis', uni=0x00CF, hex='00CF', c='Ï', w='I', bl='I', base='I', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Idotaccent': GD(name='Idotaccent', uni=0x0130, hex='0130', c='İ', w='I', bl='I', base='I', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
    'Idotbelow': GD(name='Idotbelow', uni=0x1ECA, hex='1ECA', c='Ị', w='I', bl='I', base='I', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ị LATIN CAPITAL LETTER I WITH DOT BELOW'),
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
    'Kcommaaccent': GD(name='Kcommaaccent', uni=0x0136, hex='0136', c='Ķ', l='H', r='K', base='K', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ķ'),
    'Khook': GD(name='Khook', uni=0x0198, hex='0198', c='Ƙ', l='H', w='K', srcName='K', comment='Ƙ LATIN CAPITAL LETTER K WITH HOOK'),

    # L

    'L': GD(name='L', uni=0x004C, hex='004C', c='L', l='H', anchorTopX='TopX', anchorBottomX='BottomX', anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='L'),
    'Lacute': GD(name='Lacute', uni=0x0139, hex='0139', c='Ĺ', l='H', r='L', base='L', accents=['acutecmb.uc'], fixAccents=False, anchors=['bottom', 'middle', 'top'], comment='Ĺ'),
    'Lcaron': GD(name='Lcaron', uni=0x013D, hex='013D', c='Ľ', l='H', w='L', base='L', accents=['caroncmb.vert'], anchors=['bottom', 'middle', 'top'], comment='Ľ'),
    'Lcommaaccent': GD(name='Lcommaaccent', uni=0x013B, hex='013B', c='Ļ', l='H', r='L', base='L', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ļ'),
    'Lslash': GD(name='Lslash', uni=0x0141, hex='0141', c='Ł', r='L', base='L', comment='Ł'),

    # M

    'M': GD(name='M', uni=0x004D, hex='004D', c='M', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='M'),

    # N

    'N': GD(name='N', uni=0x004E, hex='004E', c='N', l='H', r='H', anchors=['bottom', 'middle', 'top'], comment='N'),
    'Nacute': GD(name='Nacute', uni=0x0143, hex='0143', c='Ń', l='H', r='H', base='N', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ń'),
    'Ncaron': GD(name='Ncaron', uni=0x0147, hex='0147', c='Ň', l='H', r='H', base='N', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ň'),
    'Ncommaaccent': GD(name='Ncommaaccent', uni=0x0145, hex='0145', c='Ņ', l='H', r='H', base='N', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ņ'),
    'Ndotaccent': GD(name='Ndotaccent', uni=0x1E44, hex='1E44', c='Ṅ', l='H', r='H', base='N', accents=['dotaccentcmb.uc'], srcName='uni1E44', anchors=['bottom', 'middle', 'top']),
    'Ndotbelow': GD(name='Ndotbelow', uni=0x1E46, hex='1E46', c='Ṇ', l='H', r='H', base='N', accents=['dotbelowcmb'], srcName='uni1E46', anchors=['bottom', 'middle', 'top']),
    'Nhookleft': GD(name='Nhookleft', uni=0x019D, hex='019D', c='Ɲ', l='off', r='N', srcName='N'),
    'Ntilde': GD(name='Ntilde', uni=0x00D1, hex='00D1', c='Ñ', l='H', r='H', base='N', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ñ N WITH TILDE, LATIN CAPITAL LETTER'),

    # O

    'O': GD(name='O', uni=0x004F, hex='004F', c='O', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'topleft', 'top'], comment='O'),
    'OE': GD(name='OE', uni=0x0152, hex='0152', c='Œ', l='O', r='E', anchors=['bottom', 'middle', 'top'], comment='Œ'),
    'Oacute': GD(name='Oacute', uni=0x00D3, hex='00D3', c='Ó', l='O', r='O', base='O', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
    'Obreve': GD(name='Obreve', uni=0x014E, hex='014E', c='Ŏ', l='O', r='O', base='O', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ŏ'),
    'Ocaron': GD(name='Ocaron', uni=0x01D1, hex='01D1', c='Ǒ', l='O', r='O', base='O', accents=['caroncmb.uc'], srcName='uni01D1', anchors=['bottom', 'middle', 'top']),
    'Ocircumflex': GD(name='Ocircumflex', uni=0x00D4, hex='00D4', c='Ô', l='O', r='O', base='O', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Odieresis': GD(name='Odieresis', uni=0x00D6, hex='00D6', c='Ö', l='O', r='O', base='O', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Odotbelow': GD(name='Odotbelow', uni=0x1ECC, hex='1ECC', c='Ọ', l='O', r='O', base='O', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'], comment='Ọ LATIN CAPITAL LETTER O WITH DOT BELOW'),
    'Ograve': GD(name='Ograve', uni=0x00D2, hex='00D2', c='Ò', l='O', r='O', base='O', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
    'Ohungarumlaut': GD(name='Ohungarumlaut', uni=0x0150, hex='0150', c='Ő', base='O', accents=['hungarumlautcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ő'),
    'Omacron': GD(name='Omacron', uni=0x014C, hex='014C', c='Ō', l='O', r='O', base='O', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ō'),
    'Oopen': GD(name='Oopen', uni=0x0186, hex='0186', c='Ɔ', r='O', r2l='C', srcName='O', comment='Ɔ OPEN O, LATIN CAPITAL LETTER'),
    'Oslash': GD(name='Oslash', uni=0x00D8, hex='00D8', c='Ø', l='O', w='O', srcName='O', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Oslash.alt': GD(name='Oslash.alt', l='O', w='O', base='O', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Otilde': GD(name='Otilde', uni=0x00D5, hex='00D5', c='Õ', l='O', r='O', base='O', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),

    # P

    'P': GD(name='P', uni=0x0050, hex='0050', c='P', l='H', anchors=['bottom', 'middle', 'topleft', 'top'], comment='P'),
    'Pdotaccent': GD(name='Pdotaccent', uni=0x1E56, hex='1E56', c='Ṗ', l='P', w='P', base='P', accents=['dotaccentcmb.uc'], srcName='uni1E56', anchors=['bottom', 'middle', 'top']),

    # Q

    'Q': GD(name='Q', uni=0x0051, hex='0051', c='Q', l='O', w='O', anchors=['bottom', 'middle', 'top'], comment='Q'),

    # R

    'R': GD(name='R', uni=0x0052, hex='0052', c='R', bl='H', anchors=['bottom', 'middle', 'top'], comment='R'),
    'Racute': GD(name='Racute', uni=0x0154, hex='0154', c='Ŕ', bl='H', r='R', base='R', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŕ'),
    'Rcaron': GD(name='Rcaron', uni=0x0158, hex='0158', c='Ř', bl='H', r='R', base='R', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ř'),
    'Rcommaaccent': GD(name='Rcommaaccent', uni=0x0156, hex='0156', c='Ŗ', bl='H', r='R', base='R', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ŗ'),

    # S

    'S': GD(name='S', uni=0x0053, hex='0053', c='S', l2r='self', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='S'),
    'Sacute': GD(name='Sacute', uni=0x015A, hex='015A', c='Ś', l='S', w='S', base='S', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ś'),
    'Scaron': GD(name='Scaron', uni=0x0160, hex='0160', c='Š', l='S', w='S', base='S', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Š'),
    'Scedilla': GD(name='Scedilla', uni=0x015E, hex='015E', c='Ş', l='S', w='S', base='S', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ş'),
    'Schwa': GD(name='Schwa', uni=0x018F, hex='018F', c='Ə', l='O', r='O', srcName='uni018F', anchors=['top'], comment='Ə SCHWA, LATIN CAPITAL LETTER'),
    'Scircumflex': GD(name='Scircumflex', uni=0x015C, hex='015C', c='Ŝ', l='S', w='S', base='S', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŝ'),
    'Scommaaccent': GD(name='Scommaaccent', uni=0x0218, hex='0218', c='Ș', l='S', w='S', base='S', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ș'),
    'Sdotbelow': GD(name='Sdotbelow', uni=0x1E62, hex='1E62', c='Ṣ', l='S', w='S', base='S', accents=['dotbelowcmb'], srcName='uni1E62', anchors=['bottom', 'middle', 'top'], comment='Ṣ LATIN CAPITAL LETTER S WITH DOT BELOW'),

    # T

    'T': GD(name='T', uni=0x0054, hex='0054', c='T', l2r='self', anchors=['bottom', 'middle', 'top'], comment='T'),
    'Tcaron': GD(name='Tcaron', uni=0x0164, hex='0164', c='Ť', l='T', r='T', base='T', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ť'),
    'Tcedilla': GD(name='Tcedilla', uni=0x0162, hex='0162', c='Ţ', l='T', r='T', base='T', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'], comment='Ţ'),
    'Tcommaaccent': GD(name='Tcommaaccent', uni=0x021A, hex='021A', c='Ț', l='T', r='T', base='T', accents=['commaaccentcmb'], anchors=['bottom', 'middle', 'top'], comment='Ț'),
    'Thorn': GD(name='Thorn', uni=0x00DE, hex='00DE', c='Þ', l='H', r='P', comment='Þ THORN, LATIN CAPITAL LETTER'),

    # U

    'U': GD(name='U', uni=0x0055, hex='0055', c='U', l='off', l2r='self', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='U'),
    'Uacute': GD(name='Uacute', uni=0x00DA, hex='00DA', c='Ú', l='U', r='U', base='U', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ú U WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ubreve': GD(name='Ubreve', uni=0x016C, hex='016C', c='Ŭ', l='U', r='U', base='U', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ŭ'),
    'Ucaron': GD(name='Ucaron', uni=0x01D3, hex='01D3', c='Ǔ', l='U', r='U', base='U', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top']),
    'Ucircumflex': GD(name='Ucircumflex', uni=0x00DB, hex='00DB', c='Û', l='U', r='U', base='U', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle','ogonek',  'top'], comment='Û U WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Udieresis': GD(name='Udieresis', uni=0x00DC, hex='00DC', c='Ü', l='U', r='U', base='U', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ü U WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Udotbelow': GD(name='Udotbelow', uni=0x1EE4, hex='1EE4', c='Ụ', l='U', r='U', base='U', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ụ LATIN CAPITAL LETTER U WITH DOT BELOW'),
    'Ugrave': GD(name='Ugrave', uni=0x00D9, hex='00D9', c='Ù', l='U', r='U', base='U', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ù U WITH GRAVE, LATIN CAPITAL LETTER'),
    'Uhungarumlaut': GD(name='Uhungarumlaut', uni=0x0170, hex='0170', c='Ű', l='U', r='U', base='U', accents=['hungarumlautcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ű'),
    'Umacron': GD(name='Umacron', uni=0x016A, hex='016A', c='Ū', l='U', r='U', base='U', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ū'),
    'Uogonek': GD(name='Uogonek', uni=0x0172, hex='0172', c='Ų', l='U', r='U', base='U', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'], comment='Ų'),
    'Utilde': GD(name='Utilde', uni=0x0168, hex='0168', c='Ũ', l='U', r='U', base='U', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ũ'),
    # Fix ring positions manually, hard to do automatic for italic anchors.
    'Uring': GD(name='Uring', uni=0x016E, hex='016E', c='Ů', l='U', r='U', base='U', autoFixComponentPositions=False, accents=['ringcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ů'),

    # V

    'V': GD(name='V', uni=0x0056, hex='0056', c='V', l='A', r='A', anchors=['bottom', 'middle', 'top'], comment='V'),
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

    'Y': GD(name='Y', uni=0x0059, hex='0059', c='Y', l2r='self', anchors=['bottom', 'middle', 'topleft', 'top'], comment='Y'),
    'Yacute': GD(name='Yacute', uni=0x00DD, hex='00DD', c='Ý', l='Y', r='Y', base='Y', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ý Y WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ycircumflex': GD(name='Ycircumflex', uni=0x0176, hex='0176', c='Ŷ', l='Y', r='Y', base='Y', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ŷ'),
    'Ydieresis': GD(name='Ydieresis', uni=0x0178, hex='0178', c='Ÿ', l='Y', r='Y', base='Y', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ÿ Y WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ygrave': GD(name='Ygrave', uni=0x1EF2, hex='1EF2', c='Ỳ', l='Y', r='Y', base='Y', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ỳ'),
    'Yhook': GD(name='Yhook', uni=0x01B3, hex='01B3', c='Ƴ', l='Y', r='Y', anchorBottomX='BottomX', srcName='Y', anchors=['bottom', 'middle', 'top'], comment='Ƴ LATIN CAPITAL LETTER Y WITH HOOK'),
    'Ymacron': GD(name='Ymacron', uni=0x0232, hex='0232', c='Ȳ', base='Y', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top']),
    'Ytilde': GD(name='Ytilde', uni=0x1EF8, hex='1EF8', c='Ỹ', l='Y', r='Y', base='Y', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ỹ LATIN CAPITAL LETTER Y WITH TILDE'),

    # Z

    'Z': GD(name='Z', uni=0x005A, hex='005A', c='Z', l2r='self', anchors=['bottom', 'middle', 'top'], comment='Z'),
    'Zacute': GD(name='Zacute', uni=0x0179, hex='0179', c='Ź', l='Z', r='Z', base='Z', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ź'),
    'Zcaron': GD(name='Zcaron', uni=0x017D, hex='017D', c='Ž', l='Z', r='Z', base='Z', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ž'),
    'Zdotaccent': GD(name='Zdotaccent', uni=0x017B, hex='017B', c='Ż', l='Z', r='Z', base='Z', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ż'),
    'Zdotbelow': GD(name='Zdotbelow', uni=0x1E92, hex='1E92', c='Ẓ', l='Z', r='Z', base='Z', accents=['dotbelowcmb'], srcName='uni1E92', anchors=['bottom', 'middle', 'top']),

    # a

    'a': GD(name='a', uni=0x0061, hex='0061', c='a', l='o', l2r='n', isLower=True, anchorTopX='TopX', anchors=['bottom', 'middle', 'ogonek', 'top'], comment='a Small Letters, Latin'),
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

    'ampersand': GD(name='ampersand', uni=0x0026, hex='0026', c='&', l='off', r='t', isLower=False, comment='& AMPERSAND'), # For italic shape
    'asciicircum': GD(name='asciicircum', uni=0x005E, hex='005E', c='^', l2r='self', isLower=True, comment='^ spacing circumflex accent'),
    'asciitilde': GD(name='asciitilde', uni=0x007E, hex='007E', c='~', l2r='asciitilde', isLower=True, comment='~ tilde, spacing'),
    'asciitilde.uc': GD(name='asciitilde.uc', l='asciitilde', r='asciitilde', base='asciitilde', isLower=False, comment='~ tilde, spacing, for capitals'),
    'asterisk': GD(name='asterisk', uni=0x002A, hex='002A', c='*', l2r='self', isLower=True, comment='* star'),
    'asterisk.uc': GD(name='asterisk.uc', l='asterisk', r='asterisk', base='asterisk', isLower=False, comment='* star, for capitals'),
    'at': GD(name='at', uni=0x0040, hex='0040', c='@', l2r='self', l='O', isLower=True, comment='@ COMMERCIAL AT'),
    'at.uc': GD(name='at.uc', l='at', w='at', isLower=False, base='at', comment='@ COMMERCIAL AT, for capitals'),

    'acute': GD(name='acute', uni=0x00B4, hex='00B4', c='´', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='acutecmb', isLower=True, comment='´ spacing acute accent'),

    'acutecmb': GD(name='acutecmb', uni=0x0301, anchorTopY='TopY', hex='0301', c='́', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'acutecmb.uc': GD(name='acutecmb.uc', w=0, anchorTopY='TopY', isLower=False, srcName='acutecmb', autoFixComponentPositions=False, autoFixMargins=False, anchors=['_top', 'top']),

    'quotesuperior': GD(name='quotesuperior', uni=0x02BC, hex='02BC', c='ʼ', isLower=True, isMod=True),

    # b

    'b': GD(name='b', uni=0x0062, hex='0062', c='b', l='off', r='o', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'top'], comment='b'),
    'bdotbelow': GD(name='bdotbelow', uni=0x1E05, hex='1E05', c='ḅ', base='b', accents=['dotbelowcmb'], srcName='uni1E05', isLower=True, anchors=['bottom', 'middle', 'top']),
    'bhook': GD(name='bhook', uni=0x0253, hex='0253', c='ɓ', r2l='jdotless', r='b', isLower=True),
    'backslash': GD(name='backslash', uni=0x005C, hex='005C', c="\\" , l2r='self', isLower=True, comment='\\ SOLIDUS, REVERSE'),
    'bar': GD(name='bar', uni=0x007C, hex='007C', c='|', l='bracketleft', r='bracketright', isLower=True, comment='| VERTICAL LINE'),
    'braceleft': GD(name='braceleft', uni=0x007B, hex='007B', c='{', isLower=True, comment='{ opening curly bracket'),
    #'braceleft.uc': GD(name='bracelef.uct', srcName='braceleft', l='braceleft', r='braceleft', isLower=False, comment='{ opening curly bracket'),
    'braceright': GD(name='braceright', uni=0x007D, hex='007D', c='}', l2r='braceleft', r2l='braceleft', isLower=True, comment='} RIGHT CURLY BRACKET'),
    #'braceright.uc': GD(name='braceright.uc', l2r='braceleft', r2l='braceleft', srcName='braceright', isLower=False, comment='} RIGHT CURLY BRACKET'),
    'bracketleft': GD(name='bracketleft', uni=0x005B, hex='005B', c='[', isLower=True, comment='[ square bracket, opening'),
    'bracketleft.tab': GD(name='bracketleft.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='bracketleft', isLower=True, comment='[ square bracket, opening'),
    'bracketleft.sc': GD(name='bracketleft.sc', l='bracketleft', r='bracketleft', srcName='bracketleft', isLower=True, comment='[ square bracket, opening'),
    #'bracketleft.uc': GD(name='bracketleft.uc', l='bracketleft', r='bracketleft', srcName='bracketleft', isLower=False, comment='[ square bracket, opening'),
    'bracketright': GD(name='bracketright', uni=0x005D, hex='005D', c=']', l2r='bracketleft', r2l='bracketleft', isLower=True, comment='] SQUARE BRACKET, RIGHT'),
    'bracketright.tab': GD(name='bracketright.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='bracketright', isLower=True, comment='] SQUARE BRACKET, RIGHT'),
    'bracketright.sc': GD(name='bracketright.sc', l='bracketright', r='bracketright', srcName='bracketright', isLower=True, comment='] square bracket, opening'),
    #'bracketright.uc': GD(name='bracketright.uc', l2r='bracketleft', r2l='bracketleft', srcName='bracketright', isLower=False, comment='] SQUARE BRACKET, RIGHT'),
    'brokenbar': GD(name='brokenbar', uni=0x00A6, hex='00A6', c='¦', l='H', r='H', isLower=True, comment='¦ vertical bar, broken'),
    'bullet': GD(name='bullet', uni=0x2022, hex='2022', c='•', isLower=True, l2r='self', comment='• small circle, black'),
    'bullet.uc': GD(name='bullet.uc', l='bullet', r='bullet', base='bullet', isLower=False, comment='• small circle, black'),

    'breve': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02d8, c='˘', name='breve', base='brevecmb', comment='˘ Spacing Clones of Diacritics', anchors=[]),
    'brevecmb': GD(name='brevecmb', uni=0x0306, hex='0306', anchorTopY='TopY', c='̆', w=0, srcName='uni0306', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'brevecmb.uc': GD(name='brevecmb.uc', w=0, anchorTopY='TopY', srcName='brevecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    # c

    'c': GD(name='c', uni=0x0063, hex='0063', c='c', isLower=True, anchorTopX='TopX', anchorBottomX='BottomX',anchors=['bottom', 'dot', 'middle', 'top'], comment='c'),
    'cacute': GD(name='cacute', uni=0x0107, hex='0107', c='ć', anchorTopY='TopY', base='c', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ć C WITH ACUTE, LATIN SMALL LETTER'),
    'ccaron': GD(name='ccaron', uni=0x010D, hex='010D', c='č', anchorTopY='TopY', base='c', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='č C WITH CARON, LATIN SMALL LETTER'),
    'ccedilla': GD(name='ccedilla', uni=0x00E7, hex='00E7', c='ç', base='c', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ç CEDILLA, LATIN SMALL LETTER C WITH'),
    'ccircumflex': GD(name='ccircumflex', uni=0x0109, hex='0109', c='ĉ', anchorTopY='TopY', base='c', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĉ C WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'cdotaccent': GD(name='cdotaccent', uni=0x010B, hex='010B', c='ċ', anchorTopY='TopY', base='c', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'colonsign': GD(name='colonsign', uni=0x20A1, hex='20A1', c='₡', base='C', l='C', r='C', isLower=True),
    'caron': GD(name='caron', uni=0x02C7, hex='02C7', c='ˇ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True, base='caroncmb', comment='ˇ tone, mandarin chinese third'),
    'cedilla': GD(name='cedilla', uni=0x00B8, hex='00B8', c='¸', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True, base='cedillacmb'),

    #'commaturnedsuperior': GD(name='commaturnedsuperior', uni=0x02BB, hex='02BB', c='ʻ', isMod=True),

    # d

    'd': GD(name='d', uni=0x0064, hex='0064', c='d', isLower=True, anchorTopY='TopY', anchors=['bottom', 'middle', 'top', 'vert'], comment='d'),
    # Spaced as /d, overlap solved by kerning
    'dcaron': GD(name='dcaron', uni=0x010F, hex='010F', c='ď', l='d', w='d', anchorTopY='TopY', base='d', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ď D WITH CARON, LATIN SMALL LETTER'),
    'dcroat': GD(name='dcroat', uni=0x0111, hex='0111', c='đ', l='d', r='hyphen', isLower=True, anchorTopY='TopY', comment='đ D WITH STROKE, LATIN SMALL LETTER'),
    'ddotbelow': GD(name='ddotbelow', uni=0x1E0D, hex='1E0D', c='ḍ', base='d', accents=['dotbelowcmb'], srcName='uni1E0D', isLower=True, anchors=['bottom', 'middle', 'top']),
    'dhook': GD(name='dhook', uni=0x0257, hex='0257', c='ɗ', l='d', w='d', anchorTopY='TopY', isLower=True),
    'dagger': GD(name='dagger', uni=0x2020, hex='2020', c='†', l2r='self', isLower=True, comment='† DAGGER'),
    'daggerdbl': GD(name='daggerdbl', uni=0x2021, hex='2021', c='‡', l='dagger', r='dagger', isLower=True, comment='‡ DOUBLE DAGGER'),

    'dieresis': GD(name='dieresis', uni=0x00A8, hex='00A8', c='¨', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='dieresiscmb', isLower=True, comment='¨ spacing diaeresis'),
    'dieresiscmb': GD(name='dieresiscmb', uni=0x0308, hex='0308', anchorTopY='TopY', c='̈', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dieresiscmb.uc': GD(name='dieresiscmb.uc', w=0, anchorTopY='TopY', srcName='dieresiscmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dotaccentcmb': GD(name='dotaccentcmb', uni=0x0307, anchorTopY='TopY', hex='0307', c='̇', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dotaccentcmb.uc': GD(name='dotaccentcmb.uc', w=0, anchorTopY='TopY', srcName='dotaccentcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dotbelowcmb': GD(name='dotbelowcmb', uni=0x0323, hex='0323', c='̣', w=0, base='dotaccentcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
    'dieresisbelowcmb': GD(name='dieresisbelowcmb', uni=0x0324, hex='0324', c='̤', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='dieresiscmb',isLower=True, anchors=['_bottom', 'bottom']),

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
    'eng': GD(name='eng', uni=0x014B, hex='014B', c='ŋ', l='n', r='j', isLower=True, comment='ŋ LATIN SMALL LETTER ENG'),
    'eogonek': GD(name='eogonek', uni=0x0119, hex='0119', c='ę', base='e', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ę E WITH OGONEK, LATIN SMALL LETTER'),
    'eopen': GD(name='eopen', uni=0x025B, hex='025B', c='ɛ', isLower=True, r2l='B', l2r='three', anchors=['top']),
    'eth': GD(name='eth', uni=0x00F0, hex='00F0', c='ð', l='o', r='o', isLower=True, comment='ð LATIN SMALL LETTER ETH'),
    'etilde': GD(name='etilde', uni=0x1EBD, hex='1EBD', c='ẽ', l='e', r='e', base='e', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ẽ E WITH TILDE, LATIN SMALL LETTER'),
    'eturned': GD(name='eturned', uni=0x01DD, hex='01DD', c='ǝ', l2r='e', r2l='e', anchorTopX='TopX', srcName='e', isLower=True, anchors=['top'], comment='ǝ TURNED E, LATIN SMALL LETTER'),

    # f

    'f': GD(name='f', uni=0x0066, hex='0066', c='f', l='t', rightMin='-100', anchorTopX='TopX', anchorTopY='TopY', isLower=True, fixAccents=True, anchors=['bottom', 'middle', 'top'], comment='f'),
    'f.alt': GD(name='f.alt', l='f', rightMin='-100', isLower=True, anchorTopX='TopX', anchorTopY='TopY', fixAccents=True, srcName='f', anchors=['bottom', 'middle', 'top'], comment='f.alt, allowing for serif-terminal alternative.'), 
    'fi': GD(name='fi', uni=0xFB01, hex='FB01', c='ﬁ', l='f', r='i', anchorTopX='TopX', anchorTopY='TopY', base='f.alt_connect', accents=['idotless'], isLower=True, comment='ﬁ f_i'),
    'fl': GD(name='fl', uni=0xFB02, hex='FB02', c='ﬂ', l='f', r='l', anchorTopX='TopX', anchorTopY='TopY', isLower=True, base='f.alt_noconnect', accents=['l'], comment='ﬂ f_l'),
    # Minimal 2 alternatives for connecting (long flag) and not-connecting (short flag)
    'f.alt_connect': GD(name='f.alt_connect', l='f', rightMin='-100', anchorTopX='TopX', isLower=True, fixAccents=True, srcName='f', anchors=['bottom', 'middle', 'top'], comment='f.alt, allowing for serif-terminal alternative.'), 
    'f.alt_noconnect': GD(name='f.alt_noconnect', l='f', rightMin='-100', anchorTopX='TopX', isLower=True, fixAccents=True, srcName='f', anchors=['bottom', 'middle', 'top'], comment='f.alt, allowing for serif-terminal alternative.'), 

    # g

    'g': GD(name='g', uni=0x0067, hex='0067', c='g', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g'),
    'gbreve': GD(name='gbreve', uni=0x011F, hex='011F', c='ğ', anchorTopY='TopY', base='g', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ğ G WITH BREVE, LATIN SMALL LETTER'),
    'gcaron': GD(name='gcaron', uni=0x01E7, hex='01E7', c='ǧ', anchorTopY='TopY', base='g', accents=['caroncmb'], srcName='uni01E7', isLower=True, anchors=['bottom', 'middle', 'top']),
    'gcircumflex': GD(name='gcircumflex', uni=0x011D, hex='011D', c='ĝ', anchorTopY='TopY', base='g', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĝ G WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'gcommaaccent': GD(name='gcommaaccent', uni=0x0123, hex='0123', c='ģ', anchorTopY='TopY', base='g', accents=['commaturnedabovecmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'gdotaccent': GD(name='gdotaccent', uni=0x0121, hex='0121', c='ġ', anchorTopY='TopY', base='g', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'germandbls': GD(name='germandbls', uni=0x00DF, hex='00DF', c='ß', l='f', r='s', isLower=True, comment='ß SHARP S, LATIN SMALL LETTER'),
    'gmacron': GD(name='gmacron', uni=0x1E21, hex='1E21', c='ḡ', anchorTopY='TopY', base='g', accents=['macroncmb'], srcName='uni1E21', isLower=True, anchors=['bottom', 'middle', 'top']),
    'guarani': GD(name='guarani', uni=0x20B2, hex='20B2', c='₲', srcName='G', isLower=True),
    'guillemotleft': GD(name='guillemotleft', uni=0x00AB, hex='00AB', l2r='self', c='«', isLower=True),
    'guillemotleft.uc': GD(name='guillemotleft.uc', l2r='self', base='guillemotleft', isLower=False),
    'guillemotright': GD(name='guillemotright', uni=0x00BB, hex='00BB', l='guillemotleft', r='guillemotleft', c='»', isLower=True),
    'guillemotright.uc': GD(name='guillemotright.uc',  l='guillemotleft', r='guillemotleft',  base='guillemotright', isLower=False),
    'guilsinglleft': GD(name='guilsinglleft', uni=0x2039, hex='2039', l='guillemotleft', r='guillemotleft', c='‹', isLower=True, comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglleft.uc': GD(name='guilsinglleft.uc', l='guilsinglleft', r='guilsinglleft', base='guilsinglleft', isLower=False, comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglright': GD(name='guilsinglright', uni=0x203A, hex='203A', l='guillemotleft', r='guillemotleft', c='›', isLower=True, comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK'),
    'guilsinglright.uc': GD(name='guilsinglright.uc', l='guilsinglright', r='guilsinglright', base='guilsinglright', isLower=False, comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK'),

    'grave': GD(name='grave', uni=0x0060, hex='0060', c='`', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='gravecmb', isLower=True, comment='` spacing grave accent'),
    'gravecmb': GD(name='gravecmb', uni=0x0300, hex='0300', c='̀', anchorTopY='TopY', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'gravecmb.uc': GD(name='gravecmb.uc', w=0, anchorTopY='TopY', srcName='gravecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    # h

    'h': GD(name='h', uni=0x0068, hex='0068', c='h', isLower=True, anchorTopY='TopY', anchors=['bottom', 'dot', 'middle', 'top'], comment='h'),
    'hbar': GD(name='hbar', uni=0x0127, hex='0127', c='ħ', l='h', r='h', base='h', isLower=True, comment='ħ H WITH STROKE, LATIN SMALL LETTER'),
    'hcircumflex': GD(name='hcircumflex', uni=0x0125, hex='0125', c='ĥ', anchorTopY='TopY', base='h', accents=['circumflexcmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĥ H WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'hdieresis': GD(name='hdieresis', uni=0x1E27, hex='1E27', c='ḧ', anchorTopY='TopY', base='h', accents=['dieresiscmb.uc'], srcName='uni1E27', isLower=True, anchors=['bottom', 'middle', 'top']),
    'hdotbelow': GD(name='hdotbelow', uni=0x1E25, hex='1E25', c='ḥ', anchorTopY='TopY', base='h', accents=['dotbelowcmb'], srcName='uni1E25', isLower=True, anchors=['bottom', 'middle', 'top']),
    
    'hungarumlautcmb': GD(name='hungarumlautcmb', uni=0x030B, anchorTopY='TopY', hex='030B', c='̋', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'hungarumlautcmb.uc': GD(name='hungarumlautcmb.uc', w=0, anchorTopY='TopY', srcName='hungarumlautcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    # i

    # For serif stems
    'i': GD(name='i', uni=0x0069, hex='0069', c='i', l='n', r='n', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='i'),
    'idotless': GD(name='idotless', uni=0x0131, hex='0131', c='ı', l='n', r='n', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'iacute': GD(name='iacute', uni=0x00ED, hex='00ED', c='í', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='í I WITH ACUTE, LATIN SMALL LETTER'),
    'ibreve': GD(name='ibreve', uni=0x012D, hex='012D', c='ĭ', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ĭ I WITH BREVE, LATIN SMALL LETTER'),
    'icaron': GD(name='icaron', uni=0x01D0, hex='01D0', c='ǐ', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'icircumflex': GD(name='icircumflex', uni=0x00EE, hex='00EE', c='î', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='î I WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'idieresis': GD(name='idieresis', uni=0x00EF, hex='00EF', c='ï', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ï I WITH DIAERESIS, LATIN SMALL LETTER'),
    'idotbelow': GD(name='idotbelow', uni=0x1ECB, hex='1ECB', c='ị', w='i', bl='idotless', anchorTopY='TopY', base='i', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ị I WITH DOT BELOW, LATIN SMALL LETTER'),
    'igrave': GD(name='igrave', uni=0x00EC, hex='00EC', c='ì', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ì I WITH GRAVE, LATIN SMALL LETTER'),
    'igrave_short': GD(name='igrave_short', w='i', bl='idotless', anchorTopY='TopY', base='idotless', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ì I WITH GRAVE, LATIN SMALL LETTER, combination with /f'),
    'imacron': GD(name='imacron', uni=0x012B, hex='012B', c='ī', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ī I WITH MACRON, LATIN SMALL LETTER'),
    'iogonek': GD(name='iogonek', uni=0x012F, hex='012F', c='į', bl='idotless', w='i', anchorTopY='TopY', base='i', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='į I WITH OGONEK, LATIN SMALL LETTER'),
    'istroke': GD(name='istroke', uni=0x0268, hex='0268', c='ɨ', l='hyphen', r='hyphen', base='i', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'itilde': GD(name='itilde', uni=0x0129, hex='0129', c='ĩ', w='i', bl='idotless', anchorTopY='TopY', base='idotless', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ĩ I WITH TILDE, LATIN SMALL LETTER'),
    'infinity': GD(name='infinity', uni=0x221E, hex='221E', c='∞', l='o', r='o', isLower=False, comment='∞ INFINITY'),
    # Needed for floating diacritics: i̊i̋i̍i̓i᷆i᷇j̀j́j̃j̄j̈į̀į́į̂į̃į̄į̌ɨ̀ɨ́ɨ̂ɨ̃ɨ̄ɨ̈ɨ̋ɨ̌ɨ̏ɨ̧̀ɨ̧́ɨ̧̂ɨ̧̌ɨ̱̀ɨ̱́ɨ̱̈і́ḭ̀ḭ́ḭ̄ị̀ị́ị̂ị̃ị̄i̇i̒i᷄i᷅i̛̇i̛̊i̛̋i̛̍i̛̒i̛̓i̛᷄i̛᷅i̛᷆i̛᷇i̠̇i̠̊i̠̋i̠̍i̠̒i̤̇i̤̊i̤̋i̤̍i̤̒i̤̓i̤᷄i̤᷅i̤᷆i̤᷇i̥̇i̥̊i̥̋i̥̍i̥̒i̥̓i̥᷄i̥᷅i̥᷆i̥᷇
    'idotlessogonek': GD(name='idotlessogonek', l='idotless', w='idotless', base='idotless', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='į I WITH OGONEK, LATIN SMALL LETTER'),
    'idotlessstroke': GD(name='idotlessstroke', l='istroke', w='istroke', base='idotless', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'idotlessdotbelow': GD(name='idotlessdotbelow', l='idotbelow', w='idotbelow', base='idotless', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ị I WITH DOT BELOW, LATIN SMALL LETTER'),
    'idotlesstildebelow': GD(name='idotlesstildebelow', bl='idotless', w='itildebelow', base='idotless', accents=['tildebelowcmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ĩ I WITH TILDE, LATIN SMALL LETTER'),
    'idotlesshorn': GD(name='idotlesshorn', l='idotless', r='uhorn', base='idotless', anchorTopY='idotless', autoFixComponentPositions=False, isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top']),
    'idotlessdieresisbelow': GD(name='idotlessdieresisbelow', bl='idotless', w='idotless', base='idotless', accents=['dieresisbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='Dotless /i with dieresis below'),
    'idotlessringbelow': GD(name='idotlessringbelow', bl='idotless', w='idotless', base='idotless', accents=['ringbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='Dotless /i with ring below'),

    # j
    'j': GD(name='j', uni=0x006A, hex='006A', c='j', l='off', r='off', isLower=True, anchors=['bottom', 'middle'], comment='j'),
    'jcircumflex': GD(name='jcircumflex', uni=0x0135, hex='0135', c='ĵ', bl='j', w='j', base='jdotless', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĵ J WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'jdotless': GD(name='jdotless', uni=0x0237, hex='0237', c='ȷ', l='j', r='j', isLower=True, anchors=['bottom', 'middle', 'top']),

    # k

    'k': GD(name='k', uni=0x006B, hex='006B', c='k', l='h', r='x', anchorTopY='TopY', isLower=True, anchors=['bottom', 'middle', 'top'], comment='k'),
    'kcommaaccent': GD(name='kcommaaccent', uni=0x0137, hex='0137', c='ķ', anchorTopY='TopY', base='k', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    # Manually space from l='k', since the top serif of the /k makes leftmargin different.
    'khook': GD(name='khook', uni=0x0199, hex='0199', c='ƙ', l='off', r='k', anchorTopY='TopY', srcName='uni0199', isLower=True, comment='ƙ K WITH HOOK, LATIN SMALL LETTER'),

    # l

    'l': GD(name='l', uni=0x006C, hex='006C', c='l', l='h', r='idotless', anchorTopY='TopY', isLower=True, anchors=['bottom', 'dot', 'middle', 'top', 'vert'], comment='l'),
    'lacute': GD(name='lacute', uni=0x013A, hex='013A', c='ĺ', w='l', bl='l', anchorTopY='TopY', base='l', accents=['acutecmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER'),
    # Spaced as /l, overlap solved by kerning
    'lcaron': GD(name='lcaron', uni=0x013E, hex='013E', c='ľ', l='off', w='l', anchorTopY='TopY', base='l', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ľ L WITH CARON, LATIN SMALL LETTER'),
    'lcommaaccent': GD(name='lcommaaccent', uni=0x013C, hex='013C', c='ļ', w='l', anchorTopY='TopY', base='l', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'liraTurkish': GD(name='liraTurkish', uni=0x20BA, hex='20BA', c='₺', srcName='l', isLower=True),
    'lslash': GD(name='lslash', uni=0x0142, hex='0142', c='ł', base='l', l='off', l2r='self', isLower=True, comment='ł L WITH STROKE, LATIN SMALL LETTER'),

    # m

    'm': GD(name='m', uni=0x006D, hex='006D', c='m', l='n', r='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='m'),
    'manat': GD(name='manat', uni=0x20BC, hex='20BC', c='₼', l='O', r='O', srcName='O', isLower=True),

    # n

    'n': GD(name='n', uni=0x006E, hex='006E', c='n', isLower=True, anchors=['bottom', 'middle', 'top'], comment='n'),
    'nacute': GD(name='nacute', uni=0x0144, hex='0144', c='ń', base='n', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ń N WITH ACUTE, LATIN SMALL LETTER'),
    'naira': GD(name='naira', uni=0x20A6, hex='20A6', c='₦', base='N', l='N', r='N'),
    'ncaron': GD(name='ncaron', uni=0x0148, hex='0148', c='ň', base='n', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ň N WITH CARON, LATIN SMALL LETTER'),
    'ncommaaccent': GD(name='ncommaaccent', uni=0x0146, hex='0146', c='ņ', base='n', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'ndotaccent': GD(name='ndotaccent', uni=0x1E45, hex='1E45', c='ṅ', base='n', accents=['dotaccentcmb'], srcName='uni1E45', isLower=True, anchors=['bottom', 'middle', 'top']),
    'ndotbelow': GD(name='ndotbelow', uni=0x1E47, hex='1E47', c='ṇ', base='n', accents=['dotbelowcmb'], srcName='uni1E47', isLower=True, anchors=['bottom', 'middle', 'top']),
    'nhookleft': GD(name='nhookleft', uni=0x0272, hex='0272', c='ɲ', l='j', r='n', isLower=True),
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
    'oopen': GD(name='oopen', uni=0x0254, hex='0254', c='ɔ', l='off', l2r='o', srcName='o', isLower=True, anchors=['dot'], comment='ɔ OPEN O, LATIN SMALL LETTER'),
    'oslash': GD(name='oslash', uni=0x00F8, hex='00F8', c='ø', l2r='o', srcName='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'oslash.alt': GD(name='oslash.alt', base='o', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'otilde': GD(name='otilde', uni=0x00F5, hex='00F5', c='õ', base='o', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='õ O WITH TILDE, LATIN SMALL LETTER'),
    'oogonek': GD(name='oogonek', uni=0x01EB, hex='01EB', c='ǫ', base='o', accents=['ogonekcmb'],  isLower=True, anchors=['top', 'middle', 'bottom']),

    'ogonekcmb': GD(name='ogonekcmb', uni=0x0328, hex='0328', c='̨', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_ogonek', 'bottom']),

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
    'quotedblrightreversed': GD(name='quotedblrightreversed', uni=0x201F, hex='201F', c='‟', base='quotereversed', accents=['quotereversed'], isLower=True),
    'quoteleft': GD(name='quoteleft', uni=0x2018, hex='2018', c='‘', l='quotesingle', r='quotesingle', isLower=True, comment='‘ turned comma quotation mark, single'),
    'quotereversed': GD(name='quotereversed', uni=0x201B, hex='201B', c='‛', srcName='quoteright', l='quotesingle', r='quotesingle', isLower=True),
    'quoteright': GD(name='quoteright', uni=0x2019, hex='2019', c='’', l='quotesingle', r='quotesingle', isLower=True, comment='’ SINGLE QUOTATION MARK, RIGHT'),
    'quotesinglbase': GD(name='quotesinglbase', uni=0x201A, hex='201A', c='‚', l='quotesingle', r='quotesingle', isLower=True, comment='‚ SINGLE LOW-9 QUOTATION MARK'),
    'quotesingle': GD(name='quotesingle', uni=0x0027, hex='0027', c="'" , l2r='self', isLower=True, comment='" single quotation mark, neutral'),

    'minute': GD(name='minute', uni=0x2032, hex='2032', c='′', l='quotesingle', r='quotesingle', isLower=True, comment='′ PRIME'),
    'second': GD(name='second', uni=0x2033, hex='2033', c='″', l='quotesingle', r='quotesingle', base='minute', accents=['minute'], isLower=True, comment='″ seconds'),

    # r

    'r': GD(name='r', uni=0x0072, hex='0072', c='r', l='n', r='off', isLower=True, anchors=['bottom', 'middle', 'top'], comment='r'),
    'racute': GD(name='racute', uni=0x0155, hex='0155', c='ŕ', l='r', r='r', rightMin='-100', base='r', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŕ R WITH ACUTE, LATIN SMALL LETTER'),
    'rcaron': GD(name='rcaron', uni=0x0159, hex='0159', c='ř', r='r', bl='r', rightMin='-100', base='r', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ř R WITH CARON, LATIN SMALL LETTER'),
    'rcommaaccent': GD(name='rcommaaccent', uni=0x0157, hex='0157', c='ŗ', w='r', rightMin='-100', base='r', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŗ R WITH CEDILLA, LATIN SMALL LETTER'),
    'ringabove': GD(name='ringabove', uni=0x02DA, hex='02DA', c='˚', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='ringcmb'),

    # s

    's': GD(name='s', uni=0x0073, hex='0073', c='s', l='off', l2r='self', isLower=True, anchorTopX='TopX', anchorBottomX='BottomX', useSkewRotate=True, anchors=['bottom', 'middle', 'top'], comment='s'),
    'sacute': GD(name='sacute', uni=0x015B, hex='015B', c='ś', l='s', r='s', base='s', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ś S WITH ACUTE, LATIN SMALL LETTER'),
    'scaron': GD(name='scaron', uni=0x0161, hex='0161', c='š', l='s', r='s', base='s', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='š S WITH CARON, LATIN SMALL LETTER'),
    'scedilla': GD(name='scedilla', uni=0x015F, hex='015F', c='ş', l='s', r='s', base='s', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ş S WITH CEDILLA, LATIN SMALL LETTER'),
    'schwa': GD(name='schwa', uni=0x0259, hex='0259', c='ə', anchorTopX='TopX', base='eturned', srcName='uni0259', isLower=True, anchors=['top'], comment='ə SCHWA, LATIN SMALL LETTER'),
    'scircumflex': GD(name='scircumflex', uni=0x015D, hex='015D', c='ŝ', l='s', r='s', base='s', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŝ S WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'scommaaccent': GD(name='scommaaccent', uni=0x0219, hex='0219', c='ș', l='s', r='s', base='s', accents=['commaaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ș S WITH COMMA BELOW, LATIN SMALL LETTER'),
    'sdotbelow': GD(name='sdotbelow', uni=0x1E63, hex='1E63', c='ṣ', l='s', r='s', base='s', accents=['dotbelowcmb'], srcName='uni1E63', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ṣ S WITH DOT BELOW, LATIN SMALL LETTER'),
    
    'strokeshortcmb': GD(name='strokeshortcmb', uni=0x0335, hex='0335', c='̵', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_middle', 'middle']),
    'ringbelowcmb': GD(name='ringbelowcmb', uni=0x0325, hex='0325', c='̥', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, base='ringcmb', isLower=True, anchors=['_bottom', 'bottom'], comment='COMBINING RING BELOW'),

    # t

    't': GD(name='t', uni=0x0074, hex='0074', c='t', l='off', r='off', isLower=True, anchorTopY='TopY', anchors=['bottom', 'middle', 'top', 'vert'], comment='t'),
    # Spaced as /t, overlap solved by kerning
    'tcaron': GD(name='tcaron', uni=0x0165, hex='0165', c='ť', anchorTopY='TopY', l='t', w='t', base='t', accents=['caroncmb.vert'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ť T WITH CARON, LATIN SMALL LETTER'),
    'tcedilla': GD(name='tcedilla', uni=0x0163, hex='0163', c='ţ', anchorTopY='TopY', base='t', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ţ T WITH CEDILLA, LATIN SMALL LETTER'),
    'tcommaaccent': GD(name='tcommaaccent', uni=0x021B, hex='021B', c='ț', anchorTopY='TopY', base='t', accents=['commaaccentcmb'], srcName='uni021B', isLower=True, anchors=['bottom', 'middle', 'top'], comment='ț T WITH COMMA BELOW, LATIN SMALL LETTER'),
    'thorn': GD(name='thorn', uni=0x00FE, hex='00FE', c='þ', r='o', anchorTopY='TopY', isLower=True, comment='þ THORN, LATIN SMALL LETTER'),
    'tilde': GD(name='tilde', uni=0x02DC, hex='02DC', c='˜', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='tildecmb', isLower=True),
    'tildebelowcmb': GD(name='tildebelowcmb', uni=0x0330, hex='0330', c='̰', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='tildecmb', isLower=True, anchors=['_bottom', 'bottom']),

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
    'yhook': GD(name='yhook', uni=0x01B4, hex='01B4', c='ƴ', l='y', srcName='uni01B4', isLower=True, comment='ƴ Y WITH HOOK, LATIN SMALL LETTER'),
    'ymacron': GD(name='ymacron', uni=0x0233, hex='0233', c='ȳ', base='y', accents=['macroncmb'], isLower=True, anchors=['bottom', 'middle', 'top']),
    'ytilde': GD(name='ytilde', uni=0x1EF9, hex='1EF9', c='ỹ', l='y', r='y', base='y', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ỹ Y WITH TILDE, LATIN SMALL LETTER'),

    # z

    'z': GD(name='z', uni=0x007A, hex='007A', c='z', l2r='self', isLower=True, anchors=['bottom', 'middle', 'top'], comment='z LATIN SMALL LETTER Z'),
    'zacute': GD(name='zacute', uni=0x017A, hex='017A', c='ź', l='z', r='z', base='z', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ź Z WITH ACUTE, LATIN SMALL LETTER'),
    'zcaron': GD(name='zcaron', uni=0x017E, hex='017E', c='ž', l='z', r='z', base='z', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ž Z WITH CARON, LATIN SMALL LETTER'),
    'zdotaccent': GD(name='zdotaccent', uni=0x017C, hex='017C', c='ż', l='z', r='z', base='z', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ż Z WITH DOT ABOVE, LATIN SMALL LETTER'),
    'zdotbelow': GD(name='zdotbelow', uni=0x1E93, hex='1E93', c='ẓ', l='z', r='z', base='z', accents=['dotbelowcmb'], srcName='uni1E93', isLower=True, anchors=['bottom', 'middle', 'top']),

    # Figures

    'zero': GD(l2r='self', uni=0x0030, c='0', name='zero', isLower=False, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
    'zeroslash': GD(l='zero', w='zero', name='zeroslash', base='zero', isLower=False, srcName='slash', comment='0 Digits, ASCII'),
    'zero.tab': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='zero.tab', srcName='zero', isLower=False, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
    'zeroslash.tab': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='zeroslash.tab', srcName='zeroslash', isLower=False, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
    'zeroslash.sc': GD(l='zeroslash.onum', w='zeroslash.onum', name='zeroslash.sc', srcName='zeroslash.onum', isLower=False, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),   
    'zeroslash.tab.sc': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='zeroslash.tab.sc', srcName='zeroslash.sc', base='zeroslash.sc', isLower=False, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
    'one': GD(g2='one', g1='one', l2r='self', uni=0x0031, c='1', name='one', isLower=False, comment='1'),
    'two': GD(g2='two', g1='two', l2r='self', uni=0x0032, c='2', name='two', isLower=False, comment='2'),
    'three': GD(g2='three', g1='three', r='B', uni=0x0033, c='3', name='three', isLower=False, comment='3'),
    'four': GD(g2='four', g1='four', uni=0x0034, c='4', name='four', isLower=False, comment='4'),
    'five': GD(g2='five', g1='five', l='off', r='off', uni=0x0035, c='5', name='five', isLower=False, comment='5'),
    'six': GD(g2='six', g1='six',  l2r='self', uni=0x0036, c='6', name='six', isLower=False, comment='6'),
    'seven': GD(g2='seven', g1='seven', uni=0x0037, c='7', name='seven', isLower=False, comment='7'),
    'eight': GD(g2='eight', g1='eight', l2r='self', uni=0x0038, c='8', name='eight', isLower=False, comment='8'),
    'nine': GD(g2='nine', g1='nine', l2r='six', r2l='six', uni=0x0039, c='9', name='nine', isLower=False, comment='9'),

    # Special tabs

    'minute.tab': GD(name='minute.tab', base='minute', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'colon.tab': GD(name='colon.tab', base='colon', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'semicolon.tab': GD(name='semicolon.tab', base='semicolon', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'second.tab': GD(name='second.tab', base='second', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'quotedblright.tab': GD(name='quotedblright.tab', base='quotedblright', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'quotedblleft.tab': GD(name='quotedblleft.tab', base='quotedblleft', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'quoteright.tab': GD(name='quoteright.tab', base='quoteright', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),
    'quoteleft.tab': GD(name='quoteleft.tab', base='quoteleft', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, isLower=True),

    # Diacritics

    'ringcmb': GD(name='ringcmb', uni=0x030A, hex='030A', anchorTopY='TopY', c='̊', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'ringcmb.uc': GD(name='ringcmb.uc', w=0, anchorTopY='TopY', srcName='ringcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'hungarumlautcmb': GD(name='hungarumlautcmb', anchorTopY='TopY', uni=0x030B, hex='030B', c='̋', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['top', '_top']),
    'hungarumlautcmb.uc': GD(name='hungarumlautcmb.uc', anchorTopY='TopY', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['top', '_top']),

    'tildecmb': GD(name='tildecmb', uni=0x0303, anchorTopY='TopY', hex='0303', c='̃', w=0, srcName='tilde', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'tildecmb.uc': GD(name='tildecmb.uc', w=0, anchorTopY='TopY', srcName='tildecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'quoteleftcmb': GD(name='quoteright', srcName='quoteleft', uni=0x0314, hex='0314', c='◌̔', autoFixComponentPositions=False, autoFixMargins=False, w=0, anchors=['_top', 'top']),
    'quoterightcmb': GD(name='quoterightcmb', srcName='quoteright', uni=0x0313, hex='0313', c='◌̓', autoFixComponentPositions=False, autoFixMargins=False, w=0, anchors=['_top', 'top']),

    'cedillacmb': GD(name='cedillacmb', uni=0x0327, hex='0327', c='̧', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
    #'cedillacmb.noconnect': GD(name='cedillacmb.noconnect', w=0, srcName='cedillacmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
    'caroncmb': GD(name='caroncmb', uni=0x030C, hex='030C', anchorTopY='TopY', c='̌', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'caroncmb.uc': GD(name='caroncmb.uc', w=0, anchorTopY='TopY', srcName='caroncmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'caroncmb.vert': GD(name='caroncmb.vert', w=0, srcName='quotesingle', anchors=[AD._VERT]),
    'commaaccentcmb': GD(name='commaaccentcmb', uni=0x0326, anchorTopY='TopY', hex='0326', c='̦', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom']),
    'commaturnedabovecmb': GD(name='commaturnedabovecmb', anchorTopY='TopY', uni=0x0312, hex='0312', c='̒', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    #'commaturnedayi_cybovecmb.uc': GD(name='commaturnedabovecmb.uc', anchorTopY='TopY', w=0, srcName='commaturnedabovecmb', isLower=False, anchors=['_top', 'top']),
    'circumflex': GD(name='circumflex', uni=0x02C6, hex='02C6', c='ˆ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='circumflexcmb', isLower=True, comment='ˆ Legacy CIRCUMFLEX ACCENT, MODIFIER LETTER'),
    'circumflexcmb': GD(name='circumflexcmb', uni=0x0302, anchorTopY='TopY', hex='0302', c='̂', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'circumflexcmb.uc': GD(name='circumflexcmb.uc', w=0, anchorTopY='TopY', srcName='circumflexcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'ogonek': GD(name='ogonek', uni=0x02DB, hex='02DB', c='˛', l= GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='ogonekcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, gid=482, comment='˛ OGONEK'),
    'dotaccent': GD(name='dotaccent', uni=0x02D9, hex='02D9', c='˙', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='dotaccentcmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, gid=480, comment='˙ tone, mandarin chinese fifth or neutral'),

    # Stacked diacritics
    #
    # Avoiding the problem of vertical kerning, needed for stacked diacritics, we'll create them as separate combined components
    # Using the .uc diacritics everywhere to reduce vertical space
    #
    'testcmb': GD(name='testcmb', l='off', w=0, isLower=True, anchors=['_top', 'top', ]),
    'testcmb.uc': GD(name='testcmb.uc', l='off', w=0, isLower=False, anchors=['_top', 'top']),
    'testbelowcmb': GD(name='testbelowcmb', l='off', w=0, isLower=True, anchors=['_bottom', 'bottom']),
    
    'acutedotaccentcmb': GD(name='acutedotaccentcmb', l='off', w=0, base='acutedotaccentcmb.uc', autoFixComponentPositions=False, isLower=True, anchors=['_top', 'top']),
    'acutedotaccentcmb.uc': GD(name='acutedotaccentcmb.uc', l='off', w=0, base='acutecmb.uc', accents=['dotaccentcmb.uc'], autoFixComponentPositions=False, isLower=False, anchors=['_top', 'top']),

    'brevetildecmb': GD(name='brevetildecmb', l='off', w=0, base='brevetildecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'brevetildecmb.uc': GD(name='brevetildecmb.uc', l='off', w=0, base='brevecmb.uc', accents=['tildecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'breveacutecmb': GD(name='breveacutecmb', l='off', w=0, base='breveacutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'breveacutecmb.uc': GD(name='breveacutecmb.uc', l='off', w=0, base='brevecmb.uc', accents=['acutecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'brevegravecmb': GD(name='brevegravecmb', l='off', w=0, base='brevegravecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'brevegravecmb.uc': GD(name='brevegravecmb.uc', l='off', w=0, base='brevecmb.uc', accents=['gravecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'brevehookabovecmb': GD(name='brevehookabovecmb', l='off', w=0, base='brevehookabovecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'brevehookabovecmb.uc': GD(name='brevehookabovecmb.uc', l='off', w=0, base='brevecmb.uc', accents=['hookabovecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'carondotaccentcmb': GD(name='carondotaccentcmb', l='off', w=0, base='carondotaccentcmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'carondotaccentcmb.uc': GD(name='carondotaccentcmb.uc', l='off', w=0, base='caroncmb.uc', accents=['dotaccentcmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'circumflextildecmb': GD(name='circumflextildecmb', l='off', w=0, base='circumflextildecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'circumflextildecmb.uc': GD(name='circumflextildecmb.uc', l='off', w=0, base='circumflexcmb.uc', accents=['tildecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'circumflexacutecmb': GD(name='circumflexacutecmb', l='off', w=0, base='circumflexacutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'circumflexacutecmb.uc': GD(name='circumflexacutecmb.uc', l='off', w=0, base='circumflexcmb.uc', accents=['acutecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'circumflexgravecmb': GD(name='circumflexgravecmb', l='off', w=0, base='circumflexgravecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'circumflexgravecmb.uc': GD(name='circumflexgravecmb.uc', l='off', w=0, base='circumflexcmb.uc', accents=['gravecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'circumflexhookabovecmb': GD(name='circumflexhookabovecmb', l='off', w=0, base='circumflexhookabovecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'circumflexhookabovecmb.uc': GD(name='circumflexhookabovecmb.uc', l='off', w=0, base='circumflexcmb.uc', accents=['hookabovecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'dotaccentmacroncmb': GD(name='dotaccentmacroncmb', l='off', w=0, base='dotaccentmacroncmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dotaccentmacroncmb.uc': GD(name='dotaccentmacroncmb.uc', l='off', w=0, base='dotaccentcmb.uc', accents=['macroncmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    
    'dieresiscaroncmb': GD(name='dieresiscaroncmb', l='off', w=0, base='dieresiscaroncmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dieresiscaroncmb.uc': GD(name='dieresiscaroncmb.uc', l='off', w=0, base='dieresiscmb.uc', accents=['caroncmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dieresismacroncmb': GD(name='dieresismacroncmb', l='off', w=0, base='dieresismacroncmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dieresismacroncmb.uc': GD(name='dieresismacroncmb.uc', l='off', w=0, base='dieresiscmb.uc', accents=['macroncmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dieresisacutecmb': GD(name='dieresisacutecmb', l='off', w=0, base='dieresisacutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dieresisacutecmb.uc': GD(name='dieresisacutecmb.uc', l='off', w=0, base='dieresiscmb.uc', accents=['acutecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'dieresisgravecmb': GD(name='dieresisgravecmb', l='off', w=0, base='dieresisgravecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'dieresisgravecmb.uc': GD(name='dieresisgravecmb.uc', l='off', w=0, base='dieresiscmb.uc', accents=['gravecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'hookabovecmb': GD(name='hookabovecmb', w=0, isLower=True, autoFixComponentPositions=False, autoFixMargins=False, anchors=['top', '_top']),
    'hookabovecmb.uc': GD(name='hookabovecmb.uc', srcName='hookabovecmb', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['top', '_top']),
  
    'macroncmb': GD(name='macroncmb', uni=0x0304, anchorTopY='TopY', hex='0304', c='̄', w=0, srcName='uni0304', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'macroncmb.uc': GD(name='macroncmb.uc', w=0, anchorTopY='TopY', srcName='macroncmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'macrondieresiscmb': GD(name='macrondieresiscmb', l='off', w=0, base='macrondieresiscmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'macrondieresiscmb.uc': GD(name='macrondieresiscmb.uc', l='off', w=0, base='macroncmb.uc', accents=['dieresiscmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'macronacutecmb': GD(name='macronacutecmb', uni=0x1DC4, hex='1DC4', c='᷄', l='off', w=0, base='macronacutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'macronacutecmb.uc': GD(name='macronacutecmb.uc', l='off', w=0, base='macroncmb.uc', accents=['acutecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'macrongravecmb': GD(name='macrongravecmb', uni=0x1DC6, hex='1DC6', c='᷆', l='off', w=0, base='macrongravecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'macrongravecmb.uc': GD(name='macrongravecmb.uc', l='off', w=0, base='macroncmb.uc', accents=['gravecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'ringacutecmb': GD(name='ringacutecmb', l='off', w=0, base='ringacutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'ringacutecmb.uc': GD(name='ringacutecmb.uc', l='off', w=0, base='ringcmb.uc', accents=['acutecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),

    'tildeacutecmb': GD(name='tildeacutecmb', l='off', w=0, base='tildeacutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'tildeacutecmb.uc': GD(name='tildeacutecmb.uc', l='off', w=0, base='tildecmb.uc', accents=['acutecmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'tildedieresiscmb': GD(name='tildedieresiscmb', l='off', w=0, base='tildedieresiscmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'tildedieresiscmb.uc': GD(name='tildedieresiscmb.uc', l='off', w=0, base='tildecmb.uc', accents=['dieresiscmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
    'tildemacroncmb': GD(name='tildemacroncmb', l='off', w=0, base='tildemacroncmb.uc', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top']),
    'tildemacroncmb.uc': GD(name='tildemacroncmb.uc', l='off', w=0, base='tildecmb.uc', accents=['macroncmb.uc'], autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top']),
}

# Used by GlyphSet class to add small cap glyph data records. 
SC_NAMES = (
    'A', 'AE', 'AEacute', 'Aacute', 'Abreve', 'Acaron', 'Acircumflex', 'Adieresis', 'Adotbelow', 'Agrave', 
        'Amacron', 'Aogonek', 'Aring', 'Aringacute', 'Atilde', 'Adotaccent', 'Adblgrave', 'Ainvertedbreve',
        'Aringbelow', 'AEmacron', 'Abreveacute', 'Abrevedotbelow', 'Abrevegrave', 'Abrevehookabove', 
        'Abrevetilde', 'Acircumflexacute', 'Acircumflexdotbelow', 'Acircumflexgrave', 'Acircumflexhookabove', 
        'Acircumflextilde', 'Adieresismacron', 'Adotaccentmacron', 'Ahookabove', 'Astroke', 
    'B', 'Bdotbelow', 'Bhook', 'Bdotaccent', 'Blinebelow', 'Bstroke', 
    'C', 'Cacute', 'Ccaron', 'Ccedilla', 'Ccircumflex', 'Cdotaccent', 'Ccedillaacute', 'Chi_latin', 'Cstroke', 'cedi',  
    'D', 'Dcaron', 'Dcroat', 'Ddotbelow', 'Dhook', 'bracketcaron', 'Dafrican', 'Dcedilla', 'Dcircumflexbelow', 'Ddotaccent', 'Dlinebelow', 'Dzcaron',  
    'E', 'Eacute', 'Ebreve', 'Ecaron', 'Ecircumflex', 'Edieresis', 'Edotaccent', 'Edotbelow', 'Egrave', 'Emacron', 'Eng', 
        'Eogonek', 'Eopen', 'Ereversed', 'Eth', 'Etilde', 'Ecedilla', 'Ecedillabreve', 'Ecircumflexacute', 'Ecircumflexbelow', 
        'Ecircumflexdotbelow', 'Ecircumflexgrave', 'Ecircumflexhookabove', 'Ecircumflextilde', 'Edblgrave', 'Ehookabove', 
        'Einvertedbreve', 'Emacronacute', 'Emacrongrave', 'Estroke', 'Etildebelow', 'Fdotaccent', 
    'F', 'Fhook', 'Fstroke', 
    'G', 'Gbreve', 'Gcaron', 'Gcircumflex', 'Gcommaaccent', 'Gdotaccent', 'Germandbls', 'Gmacron', 'Gacute', 'Gstroke', 
    'H', 'Hbar', 'Hcircumflex', 'Hdieresis', 'Hdotbelow', 'Hbrevebelow', 'Hcaron', 'Hcedilla', 'Hdotaccent', 'Heng', 'Hturned', 'Hhook', 
    'I', 'Iacute', 'Ibreve', 'Icaron', 'Icircumflex', 'Idieresis', 'Idotaccent', 'Idotbelow', 'Igrave', 'Imacron', 'Iogonek', 
        'Istroke', 'Itilde', 'Idblgrave', 'Idieresisacute', 'Ihookabove', 'Iinvertedbreve', 'Itildebelow', 
    'J', 'Jcircumflex', 'IJ', 'J.base', 'Jcircumflex.base', 'Jcrossedtail', 'Jstroke', 
    'K', 'Kcommaaccent', 'Khook', 'Kacute', 'Kcaron', 'Kdotbelow', 'Klinebelow', 'Kstroke', 
    'L', 'Lacute', 'Lcaron', 'Lcommaaccent', 'Lslash', 'Ldot', 'LJ', 'Lbar', 'Lbelt', 'Lcircumflexbelow', 'Ldotbelow', 
        'Ldotbelowmacron', 'Ldoublebar', 'Llinebelow', 'Lmiddletilde', 
    'M', 'Macute', 'Mdotaccent', 'Mdotbelow', 'Mhook', 
    'N', 'Nacute', 'Ncaron', 'Ncommaaccent', 'Ndotaccent', 'Ndotbelow', 'Nhookleft', 'Ntilde', 'Ncircumflexbelow', 'Ngrave', 'Nlinebelow', 'NJ', 
    'O', 'OE', 'Oacute', 'Obreve', 'Ocaron', 'Ocircumflex', 'Odieresis', 'Odotbelow', 'Ograve', 'Ohungarumlaut', 
        'Omacron', 'Oopen', 'Oslash', 'Oslash.alt', 'Otilde', 'Otildemacron', 'Oslashacute', 'Oslashacute.alt', 
        'Ohorn', 'Ohornacute', 'Ohorndotbelow', 'Ohorngrave', 'Ohornhookabove', 'Ohorntilde', 
        'Ocircumflexacute', 'Ocircumflexdotbelow', 'Ocircumflexgrave', 'Ocircumflexhookabove', 'Ocircumflextilde', 'Odblgrave', 
        'Odieresismacron', 'Odotaccentmacron', 'Ohookabove', 'Oinvertedbreve', 'Omacronacute', 'Omacrongrave', 
        'Oogonek', 'Oogonekmacron', 'Otildeacute', 'Otildedieresis', 
    'P', 'Pdotaccent', 'Pacute', 'Pstroke', 'Phook', 
    'Q', 
    'R', 'Racute', 'Rcaron', 'Rcommaaccent', 'Rdblgrave', 'Rdotaccent', 'Rdotbelow', 'Rdotbelowmacron', 'Rinvertedbreve', 'Rlinebelow', 'Rtail',  
    'S', 'Sacute', 'Scaron', 'Scedilla', 'Schwa', 'Scircumflex', 'Scommaaccent', 'Sdotbelow', 
         'Sacutedotaccent', 'Scarondotaccent', 'Sdotaccent', 'Sdotbelowdotaccent', 'Sobliquestroke', 
    'T', 'Tcaron', 'Tcedilla', 'Tcommaaccent', 'Thorn', 'Tbar', 'Tcircumflexbelow', 'Tdiagonalstroke', 'Tdotaccent', 'Tdotbelow', 'Tlinebelow', 'Tdieresis',
    'U', 'Uacute', 'Ubreve', 'Ucaron', 'Ucircumflex', 'Udieresis', 'Udotbelow', 'Ugrave', 'Uhungarumlaut', 'Umacron', 'Uogonek', 
        'Uring', 'Utilde', 'Ucircumflexbelow', 'Udblgrave', 'Udieresisacute', 'Udieresisbelow', 'Udieresiscaron', 'Udieresisgrave', 
        'Udieresismacron', 'Uhookabove', 'Uhorn', 'Uhornacute', 'Uhorndotbelow', 'Uhorngrave', 'Uhornhookabove', 'Uhorntilde', 
        'Uinvertedbreve', 'Umacrondieresis', 'Utildeacute', 'Utildebelow', 'Ustroke',   
    'V', 'Vturned', 'Vdotbelow', 'Vtilde', 'Vhook', 
    'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 'Wgrave', 'Wdotaccent', 'Wdotbelow', 'Whook', 'Wring',
    'X', 'Xdieresis', 'Xdotaccent',  
    'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ygrave', 'Yhook', 'Ymacron', 'Ytilde', 'Ydotaccent', 'Ydotbelow', 'Yhookabove', 'Ystroke', 
    'Z', 'Zacute', 'Zcaron', 'Zdotaccent', 'Zdotbelow', 'Zcircumflex', 'Zlinebelow', 'Zstroke',
    'Ezh', 'Ezhcaron', 'Ezhreversed',
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'zeroslash', 'question', 'section', 'numbersign', 'zeroslash.tab', 
    'slash', 'degree', 'germandbls', 'ampersand', 'questiondown', 'backslash', 
    'parenleft', 'parenright', 'bracketleft', 'bracketright', 'exclam', 'exclamdown', 'braceleft', 'braceright',

    # In case CYRILLIC_SET is included, these need to become smallcaps too
    'A_cy', 'Abreve_cy', 'Adieresis_cy', 'Aie_cy', 'Be_cy', 'Che_cy', 'Cheabkhasian_cy', 'Chedescender_cy', 'Chedescenderabkhasian_cy', 'Chedieresis_cy', 
    'Chekhakassian_cy', 'Cheverticalstroke_cy', 'De_cy', 'De_cy.loclBGR', 'Dje_cy', 'Dze_cy', 'Dzhe_cy', 'Dzeabkh_cy', 'E_cy', 'Edieresis_cy', 'Ef_cy', 
    'El_cy', 'El_cy.loclBGR', 'Eltail_cy', 'Em_cy', 'Emtail_cy', 'En_cy', 'Endescender_cy', 'Enghe_cy', 'Enhook_cy', 'Entail_cy', 'Er_cy', 'Ereversed_cy', 
    'Ertick_cy', 'Es_cy', 'Esdescender_cy', 'Ge_cy', 'Gedescender_cy', 'Gehookstroke_cy',
    'Ghemiddlehook_cy', 'Ghestroke_cy', 'Gheupturn_cy', 'Gje_cy', 'Ha_cy', 'Haabkhasian_cy', 'Hadescender_cy', 'Hahook_cy', 'Hardsign_cy', 'Hastroke_cy', 
    'I_cy', 'Ia_cy', 'Idieresis_cy', 'Ie_cy', 'Iebreve_cy', 'Iegrave_cy', 'Ii_cy', 'Iigrave_cy', 'Iishort_cy', 'Iishorttail_cy', 'Imacron_cy', 'Io_cy', 
    'Iu_cy', 'Je_cy', 'Ka_cy', 'Kabashkir_cy', 'Kadescender_cy', 'Kahook_cy', 'Kastroke_cy', 'Kaverticalstroke_cy', 
    'Kje_cy', 'Lje_cy', 'Nje_cy', 'O_cy', 'Obarred_cy', 'Obarreddieresis_cy', 'Odieresis_cy', 'Palochka_cy', 'Pe_cy', 
    'Pedescender_cy', 'Pedescender_cy.component', 'Pemiddlehook_cy', 'Schwa_cy', 'Schwadieresis_cy', 'Semisoftsign_cy', 'Sha_cy', 'Shcha_cy', 
    'Shha_cy', 'Softsign_cy', 'Te_cy', 'Tedescender_cy', 'Tetse_cy', 'Tse_cy', 'Tshe_cy', 'U_cy', 'Udieresis_cy', 'Uhungarumlaut_cy', 'Umacron_cy', 
    'Ushort_cy', 'Ustrait_cy', 'Ustraitstroke_cy', 'Ve_cy', 'Yeru_cy', 'Yerudieresis_cy', 'Yi_cy',
    'Ze_cy', 'Zedescender_cy', 'Zedieresis_cy', 'Zhe_cy', 'Zhebreve_cy', 'Zhedescender_cy', 'Zhedieresis_cy', 
    #'tail.component_cy.case',
    'Dzeabkh_cy', 

    # In case GREEK_SET is included, these need to be come smallcaps too
    # c2sc OT-features
    'Alpha', 'Alphatonos', 'Archaicsampi', 
    'Beta', 
    'Chi', 
    'Dei_coptic', 'Delta', 'Digamma', 
    'Epsilon', 'Epsilontonos', 
    'Eta', 'Etatonos', 
    'Fei_coptic', 
    'Gamma', 'Gangia_coptic', 
    'Heta', 'Hori_coptic', 
    'Iota', 'Iotadieresis', 'Iotatonos', 
    'KaiSymbol', 'Kappa', 'Khei_coptic', 'Koppa', 'KoppaArchaic', 
    'Lambda', 
    'Mu', 
    'Nu', 
    'Omega', 'Omegatonos', 'Omicron', 'Omicrontonos', 
    'Pamphyliandigamma', 
    'Phi', 
    'Pi', 
    'Psi', 
    'Rho', 
    'Sampi', 'San', 'Shei_coptic', 'Shima_coptic', 'Sho', 'Sigma', 'SigmaLunateDottedReversedSymbol', 'SigmaLunateDottedSymbol', 'SigmaLunateReversedSymbol', 'SigmaLunateSymbol', 'Stigma', 
    'Tau', 'Theta', 'ThetaSymbol', 
    'Upsilon', 'UpsilonacutehookSymbol', 'Upsilondieresis', 'Upsilondieresistonos', 'UpsilondieresishookSymbol', 'UpsilonhookSymbol', 'Upsilontonos', 
    'Xi', 
    'Yot', 
    'Zeta',

)
# Used by GlyphSet class to add sinf/dnom/numr/subs glyph data records. These combine with /fraction
# No longer used, better to ad them as separate entries in the GlyhpData tables.
#NUMR_DNOM_NAMES = (
#    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
#    'parenleft', 'parenright', 'plus', 'minus', 'equal', 
#    #'comma', 'hyphen', 'degree', 'period',  
#)
# Used by GlyphSet class to add sinf/dnom/numr/subs glyph data records. These combine with /fraction
#SUPS_SINF_NAMES = NUMR_DNOM_NAMES

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
# Used by GlyphSet class to add oldstyle figures glyph data records with .onum extension
ONUM_NAMES = (
    'zero', 'zeroslash', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'zero.tab', 'zeroslash.tab', 'one.tab', 'two.tab', 'three.tab', 'four.tab', 'five.tab', 'six.tab', 'seven.tab', 'eight.tab', 'nine.tab',

)

# Make exceptions for Italic glyphs and spacing rules
LATIN_S_SET_ITALIC = GDSI = deepcopy(LATIN_S_SET)
GDSI['g'] = GD(name='g', uni=0x0067, hex='0067', c='g', isLower=True, anchors=['bottom', 'middle', 'top'], comment='g')
GDSI['eogonek'] = GD(name='eogonek', uni=0x0119, hex='0119', c='ę', base='e', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ę E WITH OGONEK, LATIN SMALL LETTER')
GDSI['dcroat'] = GD(name='dcroat', uni=0x0111, hex='0111', c='đ', l='d', r='hyphen', base='d', isLower=True, anchorTopY='TopY', comment='đ D WITH STROKE, LATIN SMALL LETTER')
 
# Left spacing different from /t in italic. Manual spacing instead.

GDSI['Schwa'].l = 'off'
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
GDSI['thorn'].r = 'b'
GDSI['ampersand'].r = 'off'
GDSI['Germandbls'].l = 'off'
GDSI['Germandbls.alt'].l = 'off'
GDSI['khook'].l = 'bhook'



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

if 0:
    # Build simple example source with onlt margins as attributes.

    for gName, gd in sorted(LATIN_S_SET.items()):
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


