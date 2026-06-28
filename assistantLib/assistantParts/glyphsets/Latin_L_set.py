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
from assistantLib.assistantParts.glyphsets.Latin_M_set import (
    LATIN_M_SET_LANGUAGES, LATIN_M_SET, LATIN_M_SET_ITALIC)

LATIN_L_SET_NAME = 'Latin L'
LATIN_L_SET_NAME_ITALIC = 'Latin L Italic'

LATIN_L_SET_LANGUAGES = (
    'Abron', 'Acheron', 'Achinese', 'Achuar-Shiwiar', 'Adamawa Fulfulde', 'Adangme', 
    'Afar', 'Afrikaans', 'Aghem', 'Aguaruna', 'Aja (Benin)', 'Amahuaca', 'Amarakaeri', 
    'Amis', 'Andaandi', 'Anii', 'Anuta', 'Ao Naga', 'Apinayé', 'Arabela', 'Aragonese', 
    'Arbëreshë Albanian', 'Arvanitika Albanian', 'Asháninka', 'Ashéninka Perené', 
    'Asu (Tanzania)', 'Atayal', 'Awa-Cuaiquer', 'Awetí', 'Baatonum', 'Bafia', 
    'Bagirmi Fulfulde', 'Balinese', 'Balkan Romani', 'Bambara', 'Baoulé', 'Bari', 
    'Basa (Cameroon)', 'Basque', 'Batak Dairi', 'Batak Karo', 'Batak Mandailing', 
    'Batak Simalungun', 'Batak Toba', 'Bemba (Zambia)', 'Bena (Tanzania)', 'Biali', 
    'Bikol', 'Bini', 'Bislama', 'Boko (Benin)', 'Bora', 'Borana-Arsi-Guji Oromo', 
    'Borgu Fulfulde', 'Bosnian', 'Bouna Kulango', 'Breton', 'Buginese', 'Bushi', 
    'Candoshi-Shapra', 'Caquinte', 'Caribbean Hindustani', 'Cashibo-Cacataibo', 'Cashinahua', 
    'Catalan', 'Cebuano', 'Central Alaskan Yupik', 'Central Atlas Tamazight', 'Central Aymara', 
    'Central Kurdish', 'Central Mazahua', 'Central Nahuatl', 'Central-Eastern Niger Fulfulde', 
    'Chachi', 'Chamorro', 'Chavacano', 'Chayahuita', 'Chickasaw', 'Chiga', 'Chiltepec Chinantec', 
    'Chokwe', 'Chuukese', 'Cimbrian', 'Cofán', 'Congo Swahili', 'Cook Islands Māori', 'Cornish', 
    'Corsican', 'Creek', 'Crimean Tatar', 'Croatian', 'Czech', 'Dagbani', 'Danish', 'Dehu', 
    'Dendi (Benin)', 'Dimli', 'Dinka', 'Ditammari', 'Dongolawi', 'Duala', 'Dutch', 'Dyula', 
    'Eastern Abnaki', 'Eastern Arrernte', 'Eastern Maninkakan', 'Eastern Oromo', 'Embu', 
    'English', 'Ese Ejja', 'Ewe', 'Ewondo', 'Fanti', 'Faroese', 'Fijian', 'Filipino', 'Finnish', 
    'Fon', 'Foodo', 'French', 'Friulian', 'Ga', 'Gagauz', 'Galician', 'Ganda', 'Garifuna', 
    'Ga’anda', 'Gen', 'German', 'Gheg Albanian', 'Gilbertese', 'Gonja', 'Gooniyandi', 
    'Guadeloupean Creole French', 'Guinea Kpelle', 'Gusii', 'Gwichʼin', 'Haitian', 'Hani', 
    'Hausa', 'Hawaiian', 'Hiligaynon', 'Ho-Chunk', 'Hopi', 'Huastec', 'Hungarian', 'Hän', 
    'Ibibio', 'Icelandic', 'Igbo', 'Iloko', 'Inari Sami', 'Indonesian', 'Irish', 'Istro Romanian', 
    'Italian', 'Ixcatlán Mazatec', 'Jamaican Creole English', 'Japanese', 'Javanese', 'Jola-Fonyi', 
    "K'iche'", 'Kabiyè', 'Kabuverdianu', 'Kabyle', 'Kaingang', 'Kako', 'Kala Lagaw Ya', 
    'Kalaallisut', 'Kalenjin', 'Kamba (Kenya)', 'Kanuri', 'Kaonde', 'Kaqchikel', 'Kara-Kalpak', 
    'Karelian', 'Karo', 'Kasem', 'Kashubian', 'Kekchí', 'Kenzi', 'Khasi', 'Khoekhoe', 'Kikuyu', 
    'Kimbundu', 'Kinyarwanda', 'Kirmanjki', 'Kituba (DRC)', 'Kongo', 'Konzo', 
    'Koyra Chiini Songhay', 'Koyraboro Senni Songhai', 'Krio', 'Kuanyama', 'Kven Finnish', 
    'Kwasio', 'Kölsch', 'Ladin', 'Ladino', 'Lakota', "Lamnso'", 'Langi', 'Latgalian', 'Latin', 
    'Ligurian', 'Lingala', 'Lithuanian', 'Lobi', 'Lombard', 'Low German', 'Lower Sorbian', 'Lozi', 
    'Luba-Katanga', 'Luba-Lulua', 'Lukpa', 'Lule Sami', 'Luo (Kenya and Tanzania)', 'Luxembourgish', 
    'Maasina Fulfulde', 'Macedo-Romanian', 'Makhuwa', 'Makhuwa-Meetto', 'Makonde', 'Makwe', 
    'Malagasy', 'Malaysian', 'Maltese', 'Mam', 'Manx', 'Maore Comorian', 'Maori', 'Mapudungun', 
    'Marshallese', 'Masai', 'Matsés', 'Mattokki', 'Mauritian Creole', 'Mbelime', 'Megleno Romanian', 
    'Mende (Sierra Leone)', 'Meriam Mir', 'Meru', 'Meta’', 'Metlatónoc Mixtec', "Mi'kmaq", 
    'Minangkabau', 'Mirandese', 'Miyobe', 'Moba', 'Mohawk', 'Montagnais', 'Montenegrin', 'Mossi', 
    'Mundang', 'Munsee', 'Murrinh-Patha', 'Murui Huitoto', 'Muslim Tat', 'Mwani', 'Mískito', 'Naga Pidgin', 
    'Nateni', 'Navajo', 'Ndonga', 'Neapolitan', 'Ngazidja Comorian', 'Ngiemboon', 'Ngomba', 'Nigerian Fulfulde', 
    'Niuean', 'Nobiin', 'Nomatsiguenga', 'North Azerbaijani', 'North Marquesan', 'North Ndebele', 
    'Northeastern Dinka', 'Northern Kissi', 'Northern Kurdish', 'Northern Qiandong Miao', 
    'Northern Sami', 'Northern Uzbek', 'Norwegian', 'Nuer', 'Nyamwezi', 'Nyanja', 'Nyankole', 
    'Nyemba', 'Nzima', 'Occitan', 'Ojitlán Chinantec', 'Orma', 'Oroqen', 'Otuho', 'Palauan', 
    'Paluan', 'Pampanga', 'Papantla Totonac', 'Papiamento', 'Paraguayan Guaraní', 'Pedi', 
    'Picard', 'Pichis Ashéninka', 'Piemontese', 'Pijin', 'Pintupi-Luritja', 'Pipil', 'Pite Sami', 
    'Pohnpeian', 'Polish', 'Portuguese', 'Potawatomi', 'Prussian', 'Pulaar', 'Pular', 'Purepecha', 
    'Páez', 'Quechua', 'Romanian', 'Romansh', 'Rotokas', 'Rundi', 'Rwa', 'Samburu', 'Samoan', 
    'Sango', 'Sangu (Tanzania)', 'Saramaccan', 'Sardinian', 'Scots', 'Scottish Gaelic', 'Sena', 
    'Serbian', 'Serer', 'Seri', 'Seselwa Creole French', 'Shambala', 'Sharanahua', 'Shawnee', 
    'Shilluk', 'Shipibo-Conibo', 'Shona', 'Shuar', 'Sicilian', 'Silesian', 'Skolt Sami', 'Slovak', 
    'Slovenian', 'Soga', 'Somali', 'Soninke', 'South Azerbaijani', 'South Marquesan', 
    'South Ndebele', 'Southern Aymara', 'Southern Dagaare', 'Southern Qiandong Miao', 
    'Southern Sami', 'Southern Sotho', 'Spanish', 'Sranan Tongo', 'Standard Estonian', 
    'Standard Latvian', 'Standard Malay', 'Sukuma', 'Sundanese', 'Susu', 'Swahili', 'Swati', 
    'Swedish', 'Swiss German', 'Tachelhit', 'Tagalog', 'Tahitian', 'Taita', 'Talysh', 
    'Tasawaq', 'Tedim Chin', 'Tem', 'Teso', 'Tetum', 'Tetun Dili', 'Ticuna', 'Timne', 
    'Tiv', 'Toba', 'Tojolabal', 'Tok Pisin', 'Tokelau', 'Tonga (Tonga Islands)', 
    'Tonga (Zambia)', 'Tosk Albanian', 'Tsafiki', 'Tsakhur', 'Tsonga', 'Tswana', 'Tumbuka', 
    'Turkish', 'Turkmen', 'Tuvalu', 'Twi', 'Tzeltal', 'Tzotzil', 'Uab Meto', 'Umbundu', 
    'Ume Sami', 'Upper Guinea Crioulo', 'Upper Sorbian', 'Urarina', 'Venda', 'Venetian', 
    'Veps', 'Vlax Romani', 'Võro', 'Waama', 'Waci Gbe', 'Wallisian', 'Walloon', 'Walser', 
    'Wangaaybuwan-Ngiyambaa', 'Waorani', 'Waray (Philippines)', 'Warlpiri', 'Wasa', 'Wayuu', 
    'Welsh', 'West Central Oromo', 'West-Central Limba', 'Western Abnaki', 'Western Frisian', 
    'Western Niger Fulfulde', 'Wik-Mungkan', 'Wiradjuri', 'Wolof', 'Xavánte', 'Xhosa', 
    'Xwela Gbe', 'Yagua', "Yanesha'", 'Yangben', 'Yanomamö', 'Yao', 'Yapese', 'Yindjibarndi', 
    'Yom', 'Yoruba', 'Yucateco', 'Zapotec', 'Zarma', 'Zulu', 'Zuni', 'Záparo', 
)

print(set(LATIN_M_SET_LANGUAGES).difference(set(LATIN_L_SET_LANGUAGES)))

# The "c" attributes are redundant, if the @uni or @hex are defined, but they offer easy searching in the source by char.

LATIN_L_SET = deepcopy(LATIN_M_SET)
LATIN_L_SET_ITALIC = deepcopy(LATIN_M_SET_ITALIC)

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

for GDS in (LATIN_L_SET, LATIN_L_SET_ITALIC):

    # A

    GDS['AEacute'] = GD(name='AEacute', uni=0x01FC, hex='01FC', c='Ǽ', l='A', r='E', base='AE', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'], comment='Ǽ LATIN CAPITAL LETTER AE WITH ACUTE')
    GDS['Adblgrave'] = GD(name='Adblgrave', uni=0x0200, hex='0200', c='Ȁ', l='A', r='A', base='A', accents=['dblgravecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Adieresismacron'] = GD(name='Adieresismacron', uni=0x01DE, hex='01DE', c='Ǟ', l='A', r='A', base='A', accents=['dieresismacroncmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Adotaccent'] = GD(name='Adotaccent', uni=0x0226, hex='0226', c='Ȧ', l='A', r='A', base='A', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Adotaccentmacron'] = GD(name='Adotaccentmacron', uni=0x01E0, hex='01E0', c='Ǡ', l='A', r='A', base='A', accents=['dotaccentmacroncmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Ainvertedbreve'] = GD(name='Ainvertedbreve', uni=0x0202, hex='0202', c='Ȃ', l='A', r='A', base='A', accents=['invertedbrevecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Alpha_latin'] = GD(name='Alpha_latin', uni=0x2C6D, hex='2C6D', c='Ɑ', l='O', r='off')
    GDS['Aringacute'] = GD(name='Aringacute', uni=0x01FA, hex='01FA', c='Ǻ', l='A', r='A', base='Aring', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ǻ LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE')
    GDS['Aringbelow'] = GD(name='Aringbelow', uni=0x1E00, hex='1E00', c='Ḁ', l='A', r='A', base='A', accents=['ringbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Astroke'] = GD(name='Astroke', uni=0x023A, hex='023A', c='Ⱥ', l='A', w='A', base='A', accents=['strokecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Aturned'] = GD(name='Aturned', uni=0x2C6F, hex='2C6F', c='Ɐ', l2r='A', r2l='A', srcName='A')
    GDS['Ahookabove'] = GD(name='Ahookabove', uni=0x1EA2, hex='1EA2', c='Ả', l='A', r='A', base='A', accents=['hookabovecmb.uc'], anchors=['top', 'middle', 'bottom'], comment='Ả LATIN CAPITAL LETTER A WITH HOOK ABOVE')
    # Seperate definition, since Arighthalfring does not exist as unicode. 
    #GDS['Arighthalfring'] = GD(name='Arighthalfring', base='A', accents=['ringhalfrightcmb'], isLower=False, anchors=['bottom', 'middle', 'top'])

    GDS['Asuperior'] = GD(name='Asuperior', l='A.sc', l2r='Asuperior', isMod=True)
    GDS['Ainferior'] = GD(name='Ainferior', l='Asuperior', r='Asuperior', base='Asuperior', isLower=True) # Undefined unicode

    # B

    GDS['Bdotaccent'] = GD(name='Bdotaccent', uni=0x1E02, hex='1E02', c='Ḃ', l='H', r='B', base='B', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Beta'] = GD(name='Beta', uni=0x0392, hex='0392', c='Β', l='H', r='B', base='B', anchors=['bottom', 'middle', 'top'])
    GDS['Beta_latin'] = GD(name='Beta_latin', uni=0xA7B4, hex='A7B4', c='Ꞵ', l='B', r='B', srcName='B')
    GDS['Blinebelow'] = GD(name='Blinebelow', uni=0x1E06, hex='1E06', c='Ḇ', l='H', r='B', base='B', accents=['macronbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Bstroke'] = GD(name='Bstroke', uni=0x0243, hex='0243', c='Ƀ', l='Eth', base='B', anchors=['bottom', 'middle', 'top'])

    GDS['Bsuperior'] = GD(name='Bsuperior', l='Hsuperior', r='B.sc', isMod=True)
    GDS['Binferior'] = GD(name='Binferior', l='Bsuperior', r='Bsuperior', base='Bsuperior', isLower=True) # Undefined unicode

    # C

    GDS['Ccedillaacute'] = GD(name='Ccedillaacute', uni=0x1E08, hex='1E08', c='Ḉ', l='O', r='C', base='Ccedilla', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Chi_latin'] = GD(name='Chi_latin', uni=0xA7B3, hex='A7B3', c='Ꭓ', base='X', anchors=['bottom', 'middle', 'top'])
    GDS['Chook'] = GD(name='Chook', uni=0x0187, hex='0187', w='C', l='O', srcName='C')
    GDS['Cstroke'] = GD(name='Cstroke', uni=0x023B, hex='023B', c='Ȼ', l='C', w='C', autoFixComponentPositions=False, base='C', accents=['strokecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Creversed'] = GD(name='Creversed', uni=0x2183, hex='2183', c='Ↄ', l2r='C', r2l='C', srcName='C', isLower=False)

    GDS['Csuperior'] = GD(name='Csuperior', l='Osuperior', r='C.sc', isMod=True)
    GDS['Cinferior'] = GD(name='Cinferior', l='Csuperior', r='Csuperior', base='Csuperior', isLower=True) # Undefined unicode

    # D

    GDS['Dafrican'] = GD(name='Dafrican', uni=0x0189, hex='0189', c='Ɖ', l='Eth', r='D', base='Eth', comment='Ɖ D, LATIN CAPITAL LETTER AFRICAN')
    GDS['Dcedilla'] = GD(name='Dcedilla', uni=0x1E10, hex='1E10', c='Ḑ', l='D', r='D', base='D', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Dcircumflexbelow'] = GD(name='Dcircumflexbelow', uni=0x1E12, hex='1E12', c='Ḓ', l='D', r='D', base='D', accents=['circumflexbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Ddotaccent'] = GD(name='Ddotaccent', uni=0x1E0A, hex='1E0A', c='Ḋ', l='D', r='D', base='D', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])

    GDS['DZ'] = GD(name='DZ', uni=0x01F1, hex='01F1', c='Ǳ', l='D', r='Z', base='D', anchorTopY='Z', anchorTopX='Z', accents=['Z'], anchors=['top']) # /Z as base to make anchors go there. /D has negative position on left.
    GDS['DZcaron'] = GD(name='DZcaron', uni=0x01C4, hex='01C4', c='Ǆ', l='D', r='Z', base='DZ', accents=['caroncmb.uc'], anchors=['top'])
    GDS['Dz'] = GD(name='Dz', uni=0x01F2, hex='01F2', c='ǲ', l='D', r='z', base='z', anchorTopY='z', anchorTopX='z', isLower=True, accents=['D'], anchors=['top']) # /z as base to make anchors go there. /D has negative position on left.
    GDS['Dzcaron'] = GD(name='Dzcaron', uni=0x01C5, hex='01C5', c='ǅ', l='D', r='z', base='Dz', isLower=True, accents=['caroncmb'], anchors=['top'])
    GDS['DZ.sc'] = GD(name='DZ.sc', l='D', r='Z', base='D.sc', anchorTopY='Z.sc', anchorTopX='Z.sc', accents=['Z.sc'], anchors=['top'])
    GDS['DZcaron.sc'] = GD(name='DZcaron.sc', l='D.sc', r='Z.sc', base='DZ.sc', accents=['caroncmb.uc'], anchors=['top'])

    GDS['Dsuperior'] = GD(name='Dsuperior', l='Hsuperior', r='Osuperior', isMod=True)
    GDS['Dinferior'] = GD(name='Dinferior', l='Dsuperior', r='Dsuperior', base='Dsuperior', isLower=True) # Unicode undefined

    # E

    GDS['Ecedilla'] = GD(name='Ecedilla', uni=0x0228, hex='0228', c='Ȩ', base='E', accents=['cedillacmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Ecedillabreve'] = GD(name='Ecedillabreve', uni=0x1E1C, hex='1E1C', c='Ḝ', l='H', r='E', base='Ecedilla', accents=['brevecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Ecircumflexbelow'] = GD(name='Ecircumflexbelow', uni=0x1E18, hex='1E18', c='Ḙ', l='H', w='E', base='E', accents=['circumflexbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Edblgrave'] = GD(name='Edblgrave', uni=0x0204, hex='0204', c='Ȅ', bl='E', base='E', accents=['dblgravecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Einvertedbreve'] = GD(name='Einvertedbreve', uni=0x0206, hex='0206', c='Ȇ', base='E', accents=['invertedbrevecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Emacronacute'] = GD(name='Emacronacute', uni=0x1E16, hex='1E16', c='Ḗ', l='H', r='E', base='E', accents=['macronacutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Emacrongrave'] = GD(name='Emacrongrave', uni=0x1E14, hex='1E14', c='Ḕ', l='H', r='E', base='E', accents=['macrongravecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Epsilon'] = GD(name='Epsilon', uni=0x0395, hex='0395', c='Ε', l='E', r='E', base='E', anchors=['bottom', 'middle', 'top'])
    GDS['Esh'] = GD(name='Esh', uni=0x01A9, hex='01A9', c='Ʃ', l='summation', r='summation')
    GDS['Estroke'] = GD(name='Estroke', uni=0x0246, hex='0246', c='Ɇ', base='E', accents=['strokecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Etildebelow'] = GD(name='Etildebelow', uni=0x1E1A, hex='1E1A', c='Ḛ', base='E', accents=['tildebelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Ezh'] = GD(name='Ezh', uni=0x01B7, hex='01B7', c='Ʒ', r2l='C', r='B', anchors=['top'], comment='Ʒ EZH, LATIN CAPITAL LETTER')
    GDS['Ezhcaron'] = GD(name='Ezhcaron', uni=0x01EE, hex='01EE', c='Ǯ', l='Ezh', r='Ezh', base='Ezh', accents=['caroncmb.uc'], anchors=['top'])
    GDS['Ezhreversed'] = GD(name='Ezhreversed', uni=0x01B8, hex='01B8', c='Ƹ', l2r='Ezh', r2l='Ezh')

    GDS['Esuperior'] = GD(name='Esuperior', l='Hsuperior', r='E.sc', isMod=True)
    GDS['Einferior'] = GD(name='Einferior', l='Esuperior', r='Esuperior', base='Esuperior', isLower=True) # Unicode undefined

    # F

    GDS['Fstroke'] = GD(name='FStroke', uni=0xA798, hex='A798', c='Ꞙ', l='J', r='F', srcName='F')
    GDS['Fdotaccent'] = GD(name='Fdotaccent', uni=0x1E1E, hex='1E1E', c='Ḟ', base='F', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Fhook'] = GD(name='Fhook', uni=0x0191, hex='0191', c='Ƒ', l='off', r='F', srcName='F', comment='Ƒ LATIN CAPITAL LETTER F WITH HOOK')

    GDS['Fsuperior'] = GD(name='Fsuperior', l='Hsuperior', r='F.sc', isMod=True)
    GDS['Finferior'] = GD(name='Finferior', l='Fsuperior', r='Fsuperior', base='Fsuperior', isLower=True) # Unicode undefined

    # G

    GDS['Gacute'] = GD(name='Gacute', uni=0x01F4, hex='01F4', c='Ǵ', l='G', r='G', base='G', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Gammaafrican'] = GD(name='Gammaafrican', uni=0x0194, hex='0194', c='Ɣ', comment='Ɣ GAMMA, LATIN CAPITAL LETTER')
    GDS['Ghook'] = GD(name='Ghook', uni=0x0193, hex='0193', c='Ɠ', l='G', w='G', srcName='G')
    GDS['Glottalstop'] = GD(name='Glottalstop', uni=0x0241, hex='0241', c='Ɂ', r2l='C', r='O')
    GDS['Glottalstop.sc'] = GD(name='glottalstopsmall', uni=0x0242, hex='0242', c='ɂ', r2l='C', r='O', isSc=True)
    GDS['Gscript'] = GD(name='Gscript', uni=0xA7AC, hex='A7AC', c='Ɡ', l='O', r='jdotless', srcName='g')
    GDS['Gstroke'] = GD(name='Gstroke', uni=0x01E4, hex='01E4', c='Ǥ', l='G', r='G', base='G')

    GDS['Gsuperior'] = GD(name='Gsuperior', l='Osuperior', r='G.sc', isMod=True)
    GDS['Ginferior'] = GD(name='Ginferior', l='Gsuperior', r='Gsuperior', base='Gsuperior', isLower=True) # Unicode undefined.

    # H

    GDS['Hcaron'] = GD(name='Hcaron', uni=0x021E, hex='021E', c='Ȟ', base='H', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Hdotaccent'] = GD(name='Hdotaccent', uni=0x1E22, hex='1E22', c='Ḣ', l='H', r='H', base='H', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Heng'] = GD(name='Heng', uni=0xA726, hex='A726', c='Ꜧ', l='H', r='J', srcName='H')
    GDS['Hhook'] = GD(name='Hhook', uni=0xA7AA, hex='A7AA', c='Ɦ', l='Bhook', r='B', base='H')
    GDS['Hturned'] = GD(name='Hturned', uni=0xA78D, hex='A78D', c='Ɥ', l='H', r='H', srcName='H')

    GDS['Hsuperior'] = GD(name='Hsuperior', l='H.sc', r='H.sc', isMod=True)
    GDS['Hinferior'] = GD(name='Hinferior', l='Hsuperior', r='Hsuperior', base='Hsuperior', isLower=True) # Undefined unicode

    # I

    GDS['IJ'] = GD(name='IJ', uni=0x0132, hex='0132', c='Ĳ', l='I', r='J', base='I', accents=['J'], anchors=['bottom', 'middle', 'top'], comment='Ĳ')
    GDS['Idblgrave'] = GD(name='Idblgrave', uni=0x0208, hex='0208', c='Ȉ', w='I', bl='I', base='I', accents=['dblgravecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Idieresisacute'] = GD(name='Idieresisacute', uni=0x1E2E, hex='1E2E', c='Ḯ', w='I', bl='Idieresis', base='I', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Iinvertedbreve'] = GD(name='Iinvertedbreve', uni=0x020A, hex='020A', c='Ȋ', w='I', bl='I', base='I', accents=['invertedbrevecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Iotaafrican'] = GD(name='Iotaafrican', uni=0x0196, hex='0196', c='Ɩ', l2r='J', r2l='J', srcName='J')
    GDS['Ismall'] = GD(name='Ismall', uni=0x026A, hex='026A', c='ɪ', l='I.sc', r='I.sc', base='I.sc', isSc=True) # Should not refer to small caps here
    GDS['Itildebelow'] = GD(name='Itildebelow', uni=0x1E2C, hex='1E2C', c='Ḭ', w='I', bl='I', base='I', accents=['tildebelowcmb'], anchors=['bottom', 'middle', 'top'])

    GDS['Isuperior'] = GD(name='Isuperior', l='I.sc', r='I.sc', isMod=True)
    GDS['Iinferior'] = GD(name='Iinferior', l='Isuperior', r='Isuperior', base='Isuperior', isLower=True) # Unicode undefined

    # J

    GDS['Jcrossedtail'] = GD(name='Jcrossedtail', uni=0xA7B2, hex='A7B2', c='Ʝ', l='J', r='J')
    GDS['Jstroke'] = GD(name='Jstroke', uni=0x0248, hex='0248', c='Ɉ', l='J', r='Eth', base='J', anchors=['bottom', 'middle', 'top'])

    GDS['J.base'] = GD(g2='J.base', g1='U', r='J', name='J.base', anchors=['bottom', 'middle', 'top'])
    GDS['Jcircumflex.base'] = GD(g2='J.base', g1='U', l='J.base', w='J.base', name='Jcircumflex.base', base='J.base', accents=['circumflexcmb.uc'], anchors=['bottom', 'middle', 'top'])

    GDS['Jsuperior'] = GD(name='Jsuperior', l='J.sc', r='J.sc', isMod=True)
    GDS['Jinferior'] = GD(name='Jinferior', l='Jsuperior', r='Jsuperior', base='Jsuperior', isLower=True) # Undefined unicode

    # K

    GDS['Kacute'] = GD(name='Kacute', uni=0x1E30, hex='1E30', c='Ḱ', l='H', r='K', base='K', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Kcaron'] = GD(name='Kcaron', uni=0x01E8, hex='01E8', c='Ǩ', l='H', r='K', base='K', accents=['caroncmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Kstroke'] = GD(name='Kstroke', uni=0xA740, hex='A740', c='Ꝁ', l='Eth', r='K', base='K', anchors=['bottom', 'middle', 'top'])

    GDS['Ksuperior'] = GD(name='Ksuperior', l='Hsuperior', r='X.sc', isMod=True)
    GDS['Kinferior'] = GD(name='Kinferior', l='Ksuperior', r='Ksuperior', base='Ksuperior', isLower=True) # Undefined unicode

    # L

    GDS['LJ'] = GD(name='LJ', uni=0x01C7, hex='01C7', c='Ǉ', l='H', r='J', base='L', accents=['J'], anchors=[])
    GDS['Lambda'] = GD(name='Lambda', uni=0x039B, hex='039B', c='Λ', l='A', r='A', comment='Λ')
    GDS['Lbar'] = GD(name='Lbar', uni=0x023D, hex='023D', c='Ƚ', l='Eth', base='L', anchors=['bottom', 'middle', 'top'])
    GDS['Lbelt'] = GD(name='Lbelt', uni=0xA7AD, hex='A7AD', c='Ɬ', l='o', r='L')
    GDS['Lcircumflexbelow'] = GD(name='Lcircumflexbelow', uni=0x1E3C, hex='1E3C', c='Ḽ', l='H', r='L', base='L', accents=['circumflexbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Ldot'] = GD(name='Ldot', uni=0x013F, hex='013F', c='Ŀ', l='H', r='L', base='L', accents=['dotmiddlecmb'], anchors=['bottom', 'middle', 'top'], comment='Ŀ')
    GDS['Ldoublebar'] = GD(name='Ldoublebar', uni=0x2C60, hex='2C60', c='Ⱡ', l='Eth', r='L', base='L', anchors=['bottom', 'middle', 'top'])
    GDS['Lj'] = GD(name='Lj', uni=0x01C8, hex='01C8', c='ǈ', l='H', r='j', base='L', accents=['j'], anchors=[])
    GDS['Lmiddletilde'] = GD(name='Lmiddletilde', uni=0x2C62, hex='2C62', c='Ɫ', l=GD.CAT_MIN_MARGIN, r='L', base='L', anchors=['bottom', 'middle', 'top'])

    GDS['Lsuperior'] = GD(name='Lsuperior', l='Hsuperior', r='L.sc', isMod=True)
    GDS['Linferior'] = GD(name='Linferior', l='Lsuperior', r='Lsuperior', base='Lsuperior', isLower=True) # Undefined unicode

    # M

    GDS['Macute'] = GD(name='Macute', uni=0x1E3E, hex='1E3E', c='Ḿ', l='H', r='H', base='M', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Mhook'] = GD(name='Mhook', uni=0x2C6E, hex='2C6E', c='Ɱ', l='M', r='J')
    GDS['Mturned'] = GD(name='Mturned', uni=0x019C, hex='019C', c='Ɯ', l2r='M', r2l='M')

    GDS['Msuperior'] = GD(name='Msuperior', l='M.sc', r='M.sc', isMod=True)
    GDS['Minferior'] = GD(name='Minferior', l='Msuperior', r='Msuperior', base='Msuperior', isLower=True) # Unicode undefined

    # N

    GDS['NJ'] = GD(name='NJ', uni=0x01CA, hex='01CA', c='Ǌ', l='H', r='J', base='N', accents=['J'])
    GDS['Ncircumflexbelow'] = GD(name='Ncircumflexbelow', uni=0x1E4A, hex='1E4A', c='Ṋ', l='H', r='H', base='N', accents=['circumflexbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Ngrave'] = GD(name='Ngrave', uni=0x01F8, hex='01F8', c='Ǹ', l='H', r='H', base='N', accents=['gravecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Nj'] = GD(name='Nj', uni=0x01CB, hex='01CB', c='ǋ', l='N', r='j', base='N', accents=['j'])
    GDS['Nlongrightleg'] = GD(name='Nlongrightleg', uni=0x0220, hex='0220', c='Ƞ', r='H')

    GDS['Nsuperior'] = GD(name='Nsuperior', l='N.sc', r='N.sc', isMod=True)
    GDS['Ninferior'] = GD(name='Ninferior', l='Nsuperior', r='Nsuperior', base='Nsuperior', isLower=True) # Undefined unicode

    # O

    GDS['OU'] = GD(name='OU', uni=0x0222, hex='0222', c='Ȣ', l='O', r='O')
    GDS['Ocenteredtilde'] = GD(name='Ocenteredtilde', uni=0x019F, hex='019F', c='Ɵ', l='O', r='O', base='O', srcName='asciitilde')
    GDS['Odblgrave'] = GD(name='Odblgrave', uni=0x020C, hex='020C', c='Ȍ', bl='O', base='O', accents=['dblgravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Odieresismacron'] = GD(name='Odieresismacron', uni=0x022A, hex='022A', c='Ȫ', base='O', accents=['dieresismacroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Odotaccent'] = GD(name='Odotaccent', uni=0x022E, hex='022E', c='Ȯ', base='O', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Odotaccentmacron'] = GD(name='Odotaccentmacron', uni=0x0230, hex='0230', c='Ȱ', base='O', accents=['dotaccentmacroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Oinvertedbreve'] = GD(name='Oinvertedbreve', uni=0x020E, hex='020E', c='Ȏ', base='O', accents=['invertedbrevecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Omacronacute'] = GD(name='Omacronacute', uni=0x1E52, hex='1E52', c='Ṓ', l='O', r='O', base='O', accents=['macronacutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Omacrongrave'] = GD(name='Omacrongrave', uni=0x1E50, hex='1E50', c='Ṑ', l='O', r='O', base='O', accents=['macrongravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Omega'] = GD(name='Omega', uni=0x03A9, hex='03A9', c='Ω', anchors=['bottom', 'top'])
    GDS['Omega_latin'] = GD(name='Omega_latin', uni=0xA7B6, hex='A7B6', c='Ꞷ', base='Omega')
    GDS['Oogonek'] = GD(name='Oogonek', uni=0x01EA, hex='01EA', c='Ǫ', l='O', r='O', base='O', accents=['ogonekcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Oogonekmacron'] = GD(name='Oogonekmacron', uni=0x01EC, hex='01EC', c='Ǭ', l='O', r='O', base='Oogonek', accents=['macroncmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Otildeacute'] = GD(name='Otildeacute', uni=0x1E4C, hex='1E4C', c='Ṍ', l='O', r='O', base='O', accents=['tildeacutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Otildedieresis'] = GD(name='Otildedieresis', uni=0x1E4E, hex='1E4E', c='Ṏ', l='O', r='O', base='O', accents=['tildedieresiscmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Otildemacron'] = GD(name='Otildemacron', uni=0x022C, hex='022C', c='Ȭ', base='O', accents=['tildemacroncmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Oslashacute'] = GD(name='Oslashacute', uni=0x01FE, hex='01FE', c='Ǿ', l='O', r='O', base='Oslash', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ǿ')
    GDS['Oslashacute.alt'] = GD(name='Oslashacute.alt', l='O', r='O', base='Oslash.alt', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'], comment='Ǿ')

    GDS['Osuperior'] = GD(name='Osuperior', l='O.sc', l2r='Osuperior', isMod=True)
    GDS['Oinferior'] = GD(name='Oinferior', l='Osuperior', r='Osuperior', base='Osuperior', isLower=True) # Undefined unicode

    # P

    GDS['Pacute'] = GD(name='Pacute', uni=0x1E54, hex='1E54', c='Ṕ', l='P', w='P', base='P', accents=['acutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Phook'] = GD(name='Phook', uni=0x01A4, hex='01A4', c='Ƥ', l='Bhook', r='P', base='P')
    GDS['Pstroke'] = GD(name='Pstroke', uni=0x2C63, hex='2C63', c='Ᵽ', l='Eth', r='P', base='P', anchors=['bottom', 'middle', 'top'])

    GDS['Psuperior'] = GD(name='Psuperior', l='Hsuperior', r='P.sc', isMod=True)
    GDS['Pinferior'] = GD(name='Pinferior', l='Hsuperior', r='Hsuperior', base='Psuperior', isLower=True) # Undefined unicode

    # Q

    GDS['Qhooktail'] = GD(name='Qhooktail', uni=0x024A, hex='024A', c='Ɋ', l='O', r='off')

    GDS['Qsuperior'] = GD(name='Qsuperior', l='Osuperior', r='Osuperior', isMod=True)
    GDS['Qinferior'] = GD(name='Qinferior', l='Oinferior', r='Oinferior', base='Qsuperior', isLower=True) # Undefined unicode

    # R

    GDS['Rdblgrave'] = GD(name='Rdblgrave', uni=0x0210, hex='0210', c='Ȑ', l='R', r='R', base='R', accents=['dblgravecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Rinvertedbreve'] = GD(name='Rinvertedbreve', uni=0x0212, hex='0212', c='Ȓ', base='R', accents=['invertedbrevecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Rstroke'] = GD(name='Rstroke', uni=0x024C, hex='024C', c='Ɍ', l='Eth', base='R', anchors=['bottom', 'middle', 'top'])
    GDS['Rtail'] = GD(name='Rtail', uni=0x2C64, hex='2C64', c='Ɽ', l='H', r='R')

    GDS['Rsuperior'] = GD(name='Rsuperior', l='Hsuperior', r='R.sc', isMod=True)
    GDS['Rinferior'] = GD(name='Rinferior', l='Rsuperior', r='Rsuperior', base='Rsuperior', isLower=True) # Undefined unicode

    # S

    GDS['Sacutedotaccent'] = GD(name='Sacutedotaccent', uni=0x1E64, hex='1E64', c='Ṥ', l='S', w='S', base='S', accents=['acutedotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Saltillo'] = GD(name='Saltillo', uni=0xA78B, hex='A78B', c='Ꞌ', l='quotesingle', r='quotesingle')
    GDS['Scarondotaccent'] = GD(name='Scarondotaccent', uni=0x1E66, hex='1E66', c='Ṧ', l='S', w='S', base='S', accents=['carondotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Sdotaccent'] = GD(name='Sdotaccent', uni=0x1E60, hex='1E60', c='Ṡ', l='S', w='S', base='S', accents=['dotaccentcmb.uc'], srcName='S', anchors=['bottom', 'middle', 'top'])
    GDS['Sdotbelowdotaccent'] = GD(name='Sdotbelowdotaccent', uni=0x1E68, hex='1E68', c='Ṩ', l='S', w='S', base='S', accents=['dotaccentcmb.uc', 'dotbelowcmb'], srcName='S', anchors=['bottom', 'middle', 'top'])
    GDS['Sobliquestroke'] = GD(name='Sobliquestroke', uni=0xA7A8, hex='A7A8', c='Ꞩ', w='S', srcName='S', anchors=['bottom', 'middle', 'top'])

    GDS['Ssuperior'] = GD(name='Ssuperior', l='S.sc', l2r='Ssuperior', isMod=True)
    GDS['Sinferior'] = GD(name='Sinferior', l='Ssuperior', r='Ssuperior', base='Ssuperior', isLower=True) # Unicode undefined

    # T

    GDS['Tbar'] = GD(name='Tbar', uni=0x0166, hex='0166', c='Ŧ', l='T', r='T', base='T', comment='Ŧ')
    GDS['Tcircumflexbelow'] = GD(name='Tcircumflexbelow', uni=0x1E70, hex='1E70', c='Ṱ', l='T', r='T', base='T', accents=['circumflexbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Tdiagonalstroke'] = GD(name='Tdiagonalstroke', uni=0x023E, hex='023E', c='Ⱦ', w='T', l='T', base='T', anchors=['bottom', 'middle', 'top'])
    GDS['Tdotaccent'] = GD(name='Tdotaccent', uni=0x1E6A, hex='1E6A', c='Ṫ', l='T', r='T', base='T', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Theta'] = GD(name='Theta', uni=0x0398, hex='0398', c='Θ', base='O', l='O', r='O')
    GDS['Thook'] = GD(name='Thook', uni=0x01AC, hex='01AC', c='Ƭ', srcName='T', l='Bhook', r='T')
    GDS['Tretroflexhook'] = GD(name='Tretroflexhook', uni=0x01AE, hex='01AE', c='Ʈ', l='T', w='T', srcName='T')
    # Tdieresis does exist as unicode. Capital T: U+0054 → T + Combining Diaeresis: U+0308 → ** ̈** = T̈
    # Included here as placeholder for smallcap [c2sc] conversion
    GDS['Tdieresis'] = GD(name='Tdieresis', hex='0054 + 0308', c='T̈', l='T', r='T', base='T', accents=['dieresiscmb.uc'], anchors=['bottom', 'middle', 'top'], comment='T̈')

    GDS['Tsuperior'] = GD(name='Tsuperior', l='T.sc', r='T.sc', isMod=True)
    GDS['Tinferior'] = GD(name='Tinferior', l='Tsuperior', r='Tsuperior', base='Tsuperior', isLower=True) # Undefined unicode

    # U

    GDS['Ucircumflexbelow'] = GD(name='Ucircumflexbelow', uni=0x1E76, hex='1E76', c='Ṷ', l='U', r='U', base='U', accents=['circumflexbelowcmb'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Udblgrave'] = GD(name='Udblgrave', uni=0x0214, hex='0214', c='Ȕ', base='U', accents=['dblgravecmb.uc'], anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Udieresisbelow'] = GD(name='Udieresisbelow', uni=0x1E72, hex='1E72', c='Ṳ', l='U', r='U', base='U', accents=['dieresisbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Uinvertedbreve'] = GD(name='Uinvertedbreve', uni=0x0216, hex='0216', c='Ȗ', base='U', accents=['invertedbrevecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Umacrondieresis'] = GD(name='Umacrondieresis', uni=0x1E7A, hex='1E7A', c='Ṻ', l='U', r='U', base='U', accents=['macrondieresiscmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Upsilonafrican'] = GD(name='Upsilonafrican', uni=0x01B1, hex='01B1', c='Ʊ', l='Omega', r='Omega')
    GDS['Utildeacute'] = GD(name='Utildeacute', uni=0x1E78, hex='1E78', c='Ṹ', l='U', r='U', base='U', accents=['tildeacutecmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Utildebelow'] = GD(name='Utildebelow', uni=0x1E74, hex='1E74', c='Ṵ', l='U', r='U', base='U', accents=['tildebelowcmb'], anchors=['bottom', 'middle', 'top'])
    # Changed to /Ustroke, /Ustroke.sc and /ustroke
    #GDS['Ubar'] = GD(name='Ubar', uni=0x0244, hex='0244', c='Ʉ', l='Eth', l2r='Eth', base='U', anchors=['bottom', 'middle', 'ogonek', 'top'])
    GDS['Ustroke'] = GD(name='Ustroke', uni=0x0244, hex='0244', c='Ʉ', l='U', r='U', base='U', isLower=False, anchors=['bottom', 'middle', 'top'], comment="LATIN CAPITAL LETTER U BAR")
    GDS['Ustroke.sc'] = GD(name='Ustroke.sc', uni=0x1D7e, hex='1D7e', c='ᵾ', l='U.sc', r='U.sc', base='U.sc', isLower=False, anchors=['bottom', 'middle', 'top'], comment="LATIN SMALL CAPITAL LETTER U WITH STROKE")

    GDS['Usuperior'] = GD(name='Usuperior', l='U.sc', r='U.sc', isMod=True)
    GDS['Uinferior'] = GD(name='Uinferior', l='Usuperior', r='Usuperior', base='Usuperior', isLower=True) # Unicode undefined

    # V 

    GDS['Vdotbelow'] = GD(name='Vdotbelow', uni=0x1E7E, hex='1E7E', c='Ṿ', l='V', r='V', base='V', accents=['dotbelowcmb'], anchors=['bottom', 'middle', 'top'])
    GDS['Vhook'] = GD(name='Vhook', uni=0x01B2, hex='01B2', c='Ʋ', l='U', r='O', srcName='U', comment='Ʋ v, latin capital letter script')
    GDS['Vtilde'] = GD(name='Vtilde', uni=0x1E7C, hex='1E7C', c='Ṽ', l='V', r='V', base='V', accents=['tildecmb.uc'], anchors=['bottom', 'middle', 'top'])

    GDS['Vsuperior'] = GD(name='Vsuperior', l='V.sc', r='V.sc', isMod=True)
    GDS['Vinferior'] = GD(name='Vinferior', l='Vsuperior', r='Vsuperior', base='Vsuperior', isLower=True) # Undefined unicode

    # W

    GDS['Wdotaccent'] = GD(name='Wdotaccent', uni=0x1E86, hex='1E86', c='Ẇ', l='W', r='W', base='W', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])
    GDS['Whook'] = GD(name='Whook', uni=0x2C72, hex='2C72', l='W', srcName='W', c='Ⱳ')
    # Wring does exist as unicode. W (U+0057) followed by ◌̊ (U+030A combining ring above), i.e., W̊
    # Included here as placeholder for smallcap [c2sc] conversion
    # Ring is ringcmb version, otherwise too low on the /W 
    GDS['Wring'] = GD(name='Wring', c='W̊', l='W', r='W', base='W', accents=['ringcmb'], anchors=['bottom', 'middle', 'top'], comment='W̊')

    GDS['Wsuperior'] = GD(name='Wsuperior', l='W.sc', r='W.sc', isMod=True)
    GDS['Winferior'] = GD(name='Winferior', l='Wsuperior', r='Wsuperior', base='Wsuperior', isLower=True) # Unicode undefined

    # X

    GDS['Xdotaccent'] = GD(name='Xdotaccent', uni=0x1E8A, hex='1E8A', c='Ẋ', base='X', accents=['dotaccentcmb.uc'], anchors=['bottom', 'middle', 'top'])

    GDS['Xsuperior'] = GD(name='Xsuperior', l='X.sc', r='X.sc', isMod=True)
    GDS['Xinferior'] = GD(name='Xinferior', l='Xsuperior', r='Xsuperior', base='Xsuperior', isLower=True) # Undefined unicode

    # Y

    GDS['Yogh'] = GD(name='Yogh', uni=0x021C, hex='021C', c='Ȝ', l='three', r='three')
    GDS['Ystroke'] = GD(name='Ystroke', uni=0x024E, hex='024E', c='Ɏ', base='Y', anchors=['bottom', 'middle', 'top'])
    GDS['Zcircumflex'] = GD(name='Zcircumflex', uni=0x1E90, hex='1E90', c='Ẑ', l='Z', r='Z', base='Z', accents=['circumflexcmb.uc'], srcName='Z', anchors=['bottom', 'middle', 'top'])
    GDS['Zstroke'] = GD(name='Zstroke', uni=0x01B5, hex='01B5', c='Ƶ', l='Z', r='Z', base='Z', anchors=['bottom', 'middle', 'top'])

    GDS['Ysuperior'] = GD(name='Ysuperior', l='Y.sc', r='Y.sc', isMod=True)
    GDS['Yinferior'] = GD(name='Yinferior', l='Ysuperior', r='Ysuperior', base='Ysuperior', isLower=True) # Unicode undefined

    # Z

    GDS['Zsuperior'] = GD(name='Zsuperior', l='Z.sc', l2r='Z.sc', isMod=True)
    GDS['Zinferior'] = GD(name='Zinferior', l='Zsuperior', r='Zsuperior', base='Zsuperior', isLower=True) # Unicode undefined

    # a

    GDS['adblgrave'] = GD(name='adblgrave', uni=0x0201, hex='0201', c='ȁ', bl='a', w='a', base='a', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['adieresismacron'] = GD(name='adieresismacron', uni=0x01DF, hex='01DF', c='ǟ', w='a', bl='a', base='a', accents=['dieresismacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['adotaccent'] = GD(name='adotaccent', uni=0x0227, hex='0227', c='ȧ', w='a', bl='a', base='a', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['adotaccentmacron'] = GD(name='adotmacron', uni=0x01E1, hex='01E1', c='ǡ', w='a', bl='a', base='a', accents=['dotaccentmacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['aeacute'] = GD(name='aeacute', uni=0x01FD, hex='01FD', c='ǽ', r='e', bl='a', base='ae', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ǽ')
    GDS['ainvertedbreve'] = GD(name='ainvertedbreve', uni=0x0203, hex='0203', c='ȃ', base='a', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['alpha_latin'] = GD(name='alpha_latin', uni=0x0251, hex='0251', c='ɑ', isLower=True)
    GDS['arighthalfring'] = GD(name='arighthalfring', uni=0x1E9A, hex='1E9A', c='ẚ', base='a', accents=['ringhalfrightcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['aringacute'] = GD(name='aringacute', uni=0x01FB, hex='01FB', c='ǻ', base='a', accents=['ringacutecmb'], isLower=True, fixAccents=False, anchors=['bottom', 'middle', 'top'], comment='ǻ')
    GDS['aringbelow'] = GD(name='aringbelow', uni=0x1E01, hex='1E01', c='ḁ', base='a', accents=['ringbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['astroke'] = GD(name='astroke', uni=0x2C65, hex='2C65', c='ⱥ', base='a', accents=['strokecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['aturned'] = GD(name='aturned', uni=0x0250, hex='0250', c='ɐ', l2r='a', r2l='a', srcName='a', isLower=True)

    GDS['acutemacroncmb'] = GD(name='acutemacroncmb', uni=0x1DC7, hex='1DC7', c='᷇', w=0, srcName='acutecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top'])
    GDS['acutemacroncmb.uc'] = GD(name='acutemacroncmb.uc', w=0, srcName='acutemacroncmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top'])

    GDS['asuperior'] = GD(name='asuperior', uni=0x1D43, hex='1D43', c='ᵃ', l='osuperior', r='nsuperior', isLower=False, isMod=True)
    GDS['ainferior'] = GD(name='ainferior', uni=0x2090, hex='2090', c='ₐ', l='asuperior', r='asuperior', base='asuperior', isLower=True)

    # b

    GDS['bdotaccent'] = GD(name='bdotaccent', uni=0x1E03, hex='1E03', c='ḃ', base='b', accents=['dotaccentcmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['beta'] = GD(name='beta', uni=0x03B2, hex='03B2', c='β', isLower=True)
    GDS['beta_latin'] = GD(name='beta_latin', uni=0xA7B5, hex='A7B5', c='ꞵ', base='beta', isLower=True)
    GDS['bilabialclick'] = GD(name='bilabialclick', uni=0x0298, hex='0298', c='ʘ', l='zero', r='zero', base='zero',)
    GDS['blinebelow'] = GD(name='blinebelow', uni=0x1E07, hex='1E07', c='ḇ', base='b', accents=['macronbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    # For Serif type. For Sans use l='hyphen' instead.
    GDS['bstroke'] = GD(name='bstroke', uni=0x0180, hex='0180', c='ƀ', l='b', r='b', base='b', isLower=True)

    GDS['invertedbrevebelowcmb'] = GD(name='invertedbrevebelowcmb', uni=0x032F, hex='032F', c='̯', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, base='invertedbrevecmb', isLower=True, anchors=['_bottom', 'bottom'])
    GDS['invertedbrevecmb'] = GD(name='invertedbrevecmb', uni=0x0311, hex='0311', c='̑', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top'])
    GDS['invertedbrevecmb.uc'] = GD(name='invertedbrevecmb.uc', l=GD.CAT_CENTER, w=0, base='invertedbrevecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top'])
    GDS['invertedbrevedoublecmb'] = GD(name='invertedbrevedoublecmb', uni=0x0361, hex='0361', c='͡', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top'])
    GDS['invertedbrevedoublecmb.uc'] = GD(name='invertedbrevedoublecmb.uc', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top'])

    GDS['bsuperior'] = GD(name='bsuperior', uni=0x1D47, hex='1D47', c='ᵇ', l='off', r='osuperior', isLower=False, isMod=True)
    GDS['binferior'] = GD(name='binferior', l='bsuperior', r='osuperior', base='bsuperior', isLower=False, isMod=True) # Undefined unicode

    # c

    GDS['ccedillaacute'] = GD(name='ccedillaacute', uni=0x1E09, hex='1E09', c='ḉ', base='ccedilla', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['chi_latin'] = GD(name='chi_latin', uni=0xAB53, hex='AB53', c='ꭓ', isLower=True, comment='Based on Greek /chi')
    GDS['chook'] = GD(name='chook', uni=0x0188, hex='0188', c='ƈ', l='c', w='c', srcName='c', isLower=True)
    GDS['clickalveolar'] = GD(name='clickalveolar', uni=0x01C2, hex='01C2', c='ǂ', isLower=True)
    GDS['clickdental'] = GD(name='clickdental', uni=0x01C0, hex='01C0', c='ǀ', l='bar', r='bar', base='bar', isLower=True)
    GDS['clicklateral'] = GD(name='clicklateral', uni=0x01C1, hex='01C1', c='ǁ', l='bar', r='bar', base='bar', accents=['bar'], isLower=True)
    GDS['clickretroflex'] = GD(name='clickretroflex', uni=0x01C3, hex='01C3', c='ǃ', base='exclam', isLower=True)
    GDS['cstroke'] = GD(name='cstroke', uni=0x023C, hex='023C', c='ȼ', base='c', autoFixComponentPositions=False, accents=['strokecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['creversed'] = GD(name='creversed', uni=0x2184, hex='2184', c='ↄ', l2r='c', r2l='C', srcName='c')

    GDS['commaabovecmb'] = GD(name='commaabovecmb', uni=0x0313, hex='0313', c='̓', w=0, srcName='comma', isLower=True, anchors=['_top', 'top'])
    GDS['commaabovecmb.uc'] = GD(name='commaabovecmb.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='commaabovecmb', isLower=False, anchors=['_top', 'top'])
    GDS['commaaboverightcmb'] = GD(name='commaaboverightcmb', uni=0x0315, hex='0315', c='̕', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='psili', isLower=True, anchors=['_top', 'top']    )
    GDS['commaaboverightcmb.uc'] = GD(name='commaaboverightcmb.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='commaaboverightcmb', isLower=False, anchors=['_top', 'top'])
    GDS['circumflexbelowcmb'] = GD(name='circumflexbelowcmb', uni=0x032D, hex='032D', c='̭', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='circumflexcmb', isLower=True, anchors=['_bottom', 'bottom'])

    GDS['csuperior'] = GD(name='csuperior', uni=0x1D9C, hex='1D9C', c='ᶜ', l='osuperior', isLower=False, isMod=True)
    GDS['cinferior'] = GD(name='cinferior', l='csuperior', r='csuperior', base='csuperior', isLower=True) # Undefined unicode
    GDS['colonsuperior'] = GD(name='colonsuperior', uni=0xA789, hex='A789', c='꞉', l='periodsuperior', r='periodsuperior', isLower=True, isMod=True)

    # d

    GDS['dbdigraph'] = GD(name='dbdigraph', uni=0x0238, hex='0238', c='ȸ', l='d', r='b', isLower=True)
    GDS['dcedilla'] = GD(name='dcedilla', uni=0x1E11, hex='1E11', c='ḑ', base='d', accents=['cedillacmb'], autoFixComponentPositions=False, isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['dcircumflexbelow'] = GD(name='dcircumflexbelow', uni=0x1E13, hex='1E13', c='ḓ', base='d', accents=['circumflexbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ddotaccent'] = GD(name='ddotaccent', uni=0x1E0B, hex='1E0B', c='ḋ', base='d', accents=['dotaccentcmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['dtail'] = GD(name='dtail', uni=0x0256, hex='0256', c='ɖ', l='d', r='off', isLower=True, comment='Glyph unicode 0256 is the lowercase letter "ɖ" in the International Phonetic Alphabet (IPA). It is used to represent a voiced retroflex plosive sound in various languages, including African languages such as Igbo, Yoruba, and Ewe. It is also used in some Native American languages such as Navajo and Tlingit. In linguistics, the IPA is commonly used to transcribe the sounds of human speech, and the glyph unicode 0256 helps to accurately represent this specific sound.')
    GDS['dz'] = GD(name='dz', uni=0x01F3, hex='01F3', c='ǳ', l='d', r='z', anchorTopY='z', anchorTopX='z', base='d', accents=['z'], isLower=True, anchors=['top'])
    GDS['dzcaron'] = GD(name='dzcaron', uni=0x01C6, hex='01C6', c='ǆ', l='d', r='z', base='dz', accents=['caroncmb'], isLower=True, anchors=['top'])

    GDS['dsuperior'] = GD(name='dsuperior', l='osuperior', r='lsuperior', isLower=False, isMod=True)
    GDS['dinferior'] = GD(name='dinferior', l='dsuperior', r='dsuperior', base='dsuperior', isLower=True) # Undefined unicode

    #GDS['dblquotesuperior'] = GD(name='dblquotesuperior', uni=0x02EE, hex='02EE', c='ˮ', isLower=True, isMod=True)

    # e

    GDS['ecedilla'] = GD(name='ecedilla', uni=0x0229, hex='0229', c='ȩ', base='e', accents=['cedillacmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ecedillabreve'] = GD(name='ecedillabreve', uni=0x1E1D, hex='1E1D', c='ḝ', w='e', base='ecedilla', accents=['brevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ecircumflexbelow'] = GD(name='ecircumflexbelow', uni=0x1E19, hex='1E19', c='ḙ', w='e', base='e', accents=['circumflexbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['edblgrave'] = GD(name='edblgrave', uni=0x0205, hex='0205', c='ȅ', w='e', bl='e', base='e', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['einvertedbreve'] = GD(name='einvertedbreve', uni=0x0207, hex='0207', c='ȇ', base='e', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['emacronacute'] = GD(name='emacronacute', uni=0x1E17, hex='1E17', c='ḗ', w='e', bl='e', base='e', accents=['macronacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['emacrongrave'] = GD(name='emacrongrave', uni=0x1E15, hex='1E15', c='ḕ', bl='e', base='e', accents=['macrongravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['epsilon'] = GD(name='epsilon', uni=0x03B5, hex='03B5', c='ε', isLower=True, anchors=['top'], comment='ε')
    GDS['esh'] = GD(name='esh', uni=0x0283, hex='0283', c='ʃ', r2l='ghook', r='ghook', isLower=True)
    GDS['eshreversedloop'] = GD(name='eshreversedloop', uni=0x01AA, hex='01AA', c='ƪ', r='off', isLower=True)
    GDS['estroke'] = GD(name='estroke', uni=0x0247, hex='0247', c='ɇ', base='e', accents=['strokecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['etildebelow'] = GD(name='etildebelow', uni=0x1E1B, hex='1E1B', c='ḛ', l='e', r='e', base='e', accents=['tildebelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ezh'] = GD(name='ezh', uni=0x0292, hex='0292', c='ʒ', l='off', r='three', isLower=True, anchors=['top'])
    GDS['ezhcaron'] = GD(name='ezhcaron', uni=0x01EF, hex='01EF', c='ǯ', base='ezh', accents=['caroncmb'], isLower=True, anchors=['top'])
    GDS['ezhreversed'] = GD(name='ezhreversed', uni=0x01B9, hex='01B9', c='ƹ', l='o', l2r='three', isLower=True)

    GDS['esuperior'] = GD(name='esuperior', uni=0x1D49, hex='1D49', c='ᵉ', l='osuperior', r='osuperior', isLower=False, isMod=True)
    GDS['einferior'] = GD(name='einferior', uni=0x2091, hex='2091', c='ₑ', l='esuperior', r='esuperior', base='esuperior', isLower=True)
    GDS['egravesuperior'] = GD(name='egravesuperior', l='esuperior', r='esuperior', srcName='esuperior', isLower=False, isMod=True)
    GDS['egraveinferior'] = GD(name='egraveinferior', l='egravesuperior', r='egravesuperior', base='egravesuperior', isLower=True)

    # f

    GDS['fstroke'] = GD(name='fstroke', uni=0xA799, hex='A799', c='ꞙ', base='f', l= 'f', r= 'f', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['fdotaccent'] = GD(name='fdotaccent', uni=0x1E1F, hex='1E1F', c='ḟ', rightMin='-100', base='f', accents=['dotaccentcmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['fourthtonechinese'] = GD(name='fourthtonechinese', uni=0x02CB, hex='02CB', c='ˋ', l=GD.CAT_CENTER, w=0, base='gravecmb', anchors=['_top', 'top'])
    #GDS['firsttonechinese'] = GD(name='firsttonechinese', uni=0x02C9, hex='02C9', w=0, c='ˉ', base='macroncmb', isLower=True, anchors=['_top', 'top'])

    GDS['fsuperior'] = GD(name='fsuperior', isLower=False, isMod=True)
    GDS['finferior'] = GD(name='finferior', l='fsuperior', r='fsuperior', base='fsuperior', isLower=True) # Undefined unicode

    # g

    GDS['gacute'] = GD(name='gacute', uni=0x01F5, hex='01F5', c='ǵ', base='g', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['gamma_latin'] = GD(name='gamma_latin', uni=0x0263, hex='0263', c='ɣ', isLower=True)
    GDS['ghook'] = GD(name='ghook', uni=0x0260, hex='0260', c='ɠ', l='o', r='off', isLower=True) # Italic-shaped roman better spaces as /o on the left.
    GDS['glottalstop'] = GD(name='glottalstop', uni=0x0294, hex='0294', c='ʔ', r2l='C', r='O', isLower=True)
    GDS['glottalstopreversed'] = GD(name='glottalstopreversed', uni=0x0295, hex='0295', c='ʕ', l2r='glottalstop', r2l='glottalstop', srcName='question')
    GDS['gravemacroncmb'] = GD(name='gravemacroncmb', uni=0x1DC5, hex='1DC5', c='᷅', w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='gravecmb', isLower=True, anchors=['_top', 'top'])
    GDS['gravemacroncmb.uc'] = GD(name='gravemacroncmb.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='gravemacroncmb', isLower=False, anchors=['_top', 'top'])
    GDS['gsingle'] = GD(name='gsingle', uni=0x0261, hex='0261', c='ɡ', base='g', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['gstroke'] = GD(name='gstroke', uni=0x01E5, hex='01E5', c='ǥ', l='g', r='g', base='g', isLower=True)

    GDS['gsuperior'] = GD(name='gsuperior', uni=0x1D4D, hex='1D4D', c='ᵍ', l='osuperior', r='off', isLower=False, isMod=True)
    GDS['ginferior'] = GD(name='ginferior', l='gsuperior', r='gsuperior', base='gsuperior', isLower=True) # Undefined unicode

    #GDS['glottalstopreversedsuperior'] = GD(name='glottalstopreversedsuperior', uni=0x02C1, hex='02C1', c='ˁ', isMod=True)
    #GDS['glottalstopsuperior'] = GD(name='glottalstopsuperior', uni=0x02C0, hex='02C0', c='ˀ', isMod=True)

    # h

    GDS['hcaron'] = GD(name='hcaron', uni=0x021F, hex='021F', c='ȟ', base='h', accents=['caroncmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['hdotaccent'] = GD(name='hdotaccent', uni=0x1E23, hex='1E23', c='ḣ', base='h', accents=['dotaccentcmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['heng'] = GD(name='heng', uni=0xA727, hex='A727', c='ꜧ', l='h', r='j', srcName='h', isLower=True)
    GDS['henghook'] = GD(name='henghook', uni=0x0267, hex='0267', c='ɧ', l='khook', r='jdotless', isLower=True) # Not left of /h because missing top serif
    GDS['hhook'] = GD(name='hhook', uni=0x0266, hex='0266', c='ɦ', l='khook', r='h', srcName='h', isLower=True) # Not left of /h because missing top serif
    GDS['hturned'] = GD(name='hturned', uni=0x0265, hex='0265', c='ɥ', l2r='h', r2l='h', srcName='h', isLower=True)

    GDS['hsuperior'] = GD(name='hsuperior', uni=0x02B0, hex='02B0', c='ʰ', l='nsuperior', r='nsuperior', isMod=True)
    GDS['hinferior'] = GD(name='hinferior', c='ₕ', uni=0x2095, hex='2095', l='hsuperior', r='hsuperior', base='hsuperior', isLower=True)
    #GDS['hhooksuperior'] = GD(name='hhooksuperior', uni=0x02B1, hex='02B1', c='ʱ', l='nsuperior', r='nsuperior', isMod=True)
    #GDS['hhookinferior'] = GD(name='hhookinferior', base='hhooksuperior', l='nsuperior', r='nsuperior', isMod=True)

    # i

    GDS['idblgrave'] = GD(name='idblgrave', uni=0x0209, hex='0209', c='ȉ', w='idotless', bl='idotless', base='idotless', accents=['dblgravecmb'], isLower=True, anchors=['top'])
    GDS['idblgrave_short'] = GD(name='idblgrave_short', w='i', bl='idotless', anchorTopY='TopY', base='idotless', isLower=True, anchors=['bottom', 'middle', 'ogonek', 'top'], comment='ì I WITH DOUBLE GRAVE, LATIN SMALL LETTER, combination with /f')
    GDS['idieresisacute'] = GD(name='idieresisacute', uni=0x1E2F, hex='1E2F', c='ḯ', w='idotless', bl='idotless', base='idieresis', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['iinvertedbreve'] = GD(name='iinvertedbreve', uni=0x020B, hex='020B', c='ȋ', w='idotless', bl='idotless', base='idotless', accents=['invertedbrevecmb'], isLower=True, anchors=['top'])
    GDS['ij'] = GD(name='ij', uni=0x0133, hex='0133', c='ĳ', l='i', r='j', base='i', accents=['j'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ĳ SMALL LIGATURE IJ, LATIN')
    GDS['iota_latin'] = GD(name='iota_latin', uni=0x0269, hex='0269', c='ɩ', r2l='j', r='t', isLower=True)
    GDS['itildebelow'] = GD(name='itildebelow', uni=0x1E2D, hex='1E2D', c='ḭ', w='idotless', bl='i', base='i', accents=['tildebelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['integral'] = GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, uni=0x222b, c='∫', name='integral', src='f', anchors=[], comment='∫ Integral Signs')

    GDS['isuperior'] = GD(name='isuperior', uni=0x2071, hex='2071', c='ⁱ', l2r='isuperior', isMod=True, comment="i superior")
    GDS['iinferior'] = GD(name='iinderior', uni=0x1d62, hex='1d62', l='isuperior', r='isuperior', base='isuperior', isMod=True)

    # j

    GDS['jcaron'] = GD(name='jcaron', uni=0x01F0, hex='01F0', c='ǰ', bl='j', w='j', base='jdotless', accents=['caroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['jcrossedtail'] = GD(name='jcrossedtail', uni=0x029D, hex='029D', c='ʝ', rightMin='minRight', isLower=True)
    GDS['jdotlessstroke'] = GD(name='jdotlessstroke', uni=0x025F, hex='025F', c='ɟ', l='jdotless', base='jdotless', r='hyphen', isLower=True)
    GDS['jdotlessstrokehook'] = GD(name='jdotlessstrokehook', uni=0x0284, hex='0284', c='ʄ', l='jdotless',  base='jdotless', accents=['hookabovecmb'], isLower=True)
    GDS['jstroke'] = GD(name='jstroke', uni=0x0249, hex='0249', c='ɉ', bl='j', r='hyphen', base='j', isLower=True, anchors=['bottom', 'middle'])

    GDS['jsuperior'] = GD(name='jsuperior', uni=0x02B2, hex='02B2', c='ʲ', isMod=True)
    GDS['jinferior'] = GD(name='jsuperior', uni=0x2C7C, hex='2C7C', l='jsuperior', r='jsuperior', base='jsuperior', isMod=True)

    # k

    GDS['kacute'] = GD(name='kacute', uni=0x1E31, hex='1E31', c='ḱ', base='k', accents=['acutecmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['kcaron'] = GD(name='kcaron', uni=0x01E9, hex='01E9', c='ǩ', base='k', accents=['caroncmb.uc'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['kgreenlandic'] = GD(name='kgreenlandic', uni=0x0138, hex='0138', c='ĸ', l='K.sc', w='K.sc', base='ka_cy', isLower=True, anchors=['top'], comment='ĸ LATIN SMALL LETTER KRA')
    GDS['kstroke'] = GD(name='kstroke', uni=0xA741, hex='A741', c='ꝁ', l='hyphen', r='k', base='k', isLower=True, anchors=['bottom', 'middle', 'top'])
    #GDS['koronis'] = GD(name='koronis', uni=0x1FBD, hex='1FBD', c='᾽', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True)

    GDS['ksuperior'] = GD(name='ksuperior', uni=0x1D4F, hex='1D4F', c='ᵏ', l='hsuperior', isLower=False, isMod=True)
    GDS['kinferior'] = GD(name='kinferior', c='ₖ', uni=0x2096, hex='2096', l='ksuperior', r='ksuperior', base='ksuperior') 

    # l

    GDS['lambda'] = GD(name='lambda', uni=0x03BB, hex='03BB', c='λ', l='v', r='v', isLower=True)
    GDS['lambdastroke'] = GD(name='lambdastroke', uni=0x019B, hex='019B', c='ƛ', l='lambda', w='lambda', base='lambda', isLower=True)
    GDS['lbar'] = GD(name='lbar', uni=0x019A, hex='019A', c='ƚ', l='hyphen', r='hyphen', base='l', isLower=True)
    GDS['lbelt'] = GD(name='lbelt', uni=0x026C, hex='026C', c='ɬ', l='osuperior', r='off', base='l', isLower=True)
    GDS['lcircumflexbelow'] = GD(name='lcircumflexbelow', uni=0x1E3D, hex='1E3D', c='ḽ', w='l', bl='l', base='l', accents=['circumflexbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ldot'] = GD(name='ldot', uni=0x0140, hex='0140', c='ŀ', l='l', r='off', base='l', accents=['dotmiddlecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ŀ MIDDLE DOT, LATIN SMALL LETTER L WITH')
    GDS['ldoublebar'] = GD(name='ldoublebar', uni=0x2C61, hex='2C61', c='ⱡ', base='l', l='hyphen', r='hyphen', isLower=True)
    GDS['lj'] = GD(name='lj', uni=0x01C9, hex='01C9', c='ǉ', l='l', r='j', base='l', accents=['j'], isLower=True)
    GDS['lmiddletilde'] = GD(name='lmiddletilde', uni=0x026B, hex='026B', c='ɫ', l='asciitilde', r='asciitilde', base='l', isLower=True)
    GDS['longs'] = GD(name='longs', uni=0x017F, hex='017F', c='ſ', l='f', w='f', anchorTopX='TopX', anchorTopY='TopY', isLower=True, fixAccents=False, anchors=['top'], comment='ſ S, LATIN SMALL LETTER LONG')
    GDS['longsdotaccent'] = GD(name='longsdotaccent', uni=0x1E9B, hex='1E9B', c='ẛ', w='longs', l='longs', base='longs', accents=['dotaccentcmb.uc'], isLower=True, anchors=['top'])
    GDS['lowlinecmb'] = GD(name='lowlinecmb', uni=0x0332, hex='0332', c='̲', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom'])

    GDS['lsuperior'] = GD(name='lsuperior', uni=0x02E1, hex='02E1', c='ˡ', l='hsuperior', r='nsuperior', isMod=True)
    GDS['linferior'] = GD(name='linferior', uni=0x2097, hex='2097', c='ₗ', l='lsuperior', r='lsuperior', base='lsuperior', isLower=True)

    # m

    GDS['macute'] = GD(name='macute', uni=0x1E3F, hex='1E3F', c='ḿ', base='m', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['mhook'] = GD(name='mhook', uni=0x0271, hex='0271', c='ɱ', srcName='m', l='m', r='j', isLower=True)
    GDS['mturned'] = GD(name='mturned', uni=0x026F, hex='026F', srcName='m', l2r='m', r2l='m', c='ɯ', isLower=True)
    GDS['mu'] = GD(name='mu', uni=0x03BC, hex='03BC', c='μ', l='verticalbar', r='u', isLower=True, comment='mu')

    GDS['minusphonetic'] = GD(name='minusphonetic', uni=0x02D7, hex='02D7', c='˗', r2l='minus', r='minus', srcName='minus', isLower=True, isMod=False, comment='Short /minus, spaced as not "mod"')
    GDS['minusbelowcmb'] = GD(name='minusbelowcmb', uni=0x0320, hex='0320', c='̠', l=GD.CAT_CENTER, w=0, base='minussuperior', autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_bottom', 'bottom'])

    GDS['msuperior'] = GD(name='msuperior', uni=0x1D50, hex='1D50', c='ᵐ', l='nsuperior', r='nsuperior', isLower=False, isMod=True)
    GDS['minferior'] = GD(name='minferior', uni=0x2098, hex='2098', c='ₘ', l='msuperior', r='msuperior', base='msuperior', isLower=True)

    # n

    GDS['napostrophe'] = GD(name='napostrophe', uni=0x0149, hex='0149', c='ŉ', base='quoteright', l='quoteright', r='n', accents=['n'], isLower=True, comment='ŉ')
    GDS['Napostrophe.sc'] = GD(name='Napostrophe.sc', base='quoteright', l='quoteright', r='N.sc', accents=['N.sc'], isLower=True, comment='Smallcap version of ŉ')
    GDS['ncircumflexbelow'] = GD(name='ncircumflexbelow', uni=0x1E4B, hex='1E4B', c='ṋ', base='n', accents=['circumflexbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ngrave'] = GD(name='ngrave', uni=0x01F9, hex='01F9', c='ǹ', w='n', bl='n', base='n', accents=['gravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['nj'] = GD(name='nj', uni=0x01CC, hex='01CC', c='ǌ', base='n', l='n', r='j', accents=['j'], isLower=True)
    GDS['nlegrightlong'] = GD(name='nlegrightlong', uni=0x019E, hex='019E', c='ƞ', l='n', r='n', isLower=True)

    GDS['nsuperior'] = GD(name='nsuperior', uni=0x207F, hex='207F', c='ⁿ', isMod=True)
    GDS['ninferior'] = GD(name='ninferior', uni=0x2099, hex='2099', c='ₙ', l='nsuperior', r='nsuperior', base='nsuperior')

    # o

    GDS['obarred'] = GD(name='obarred', uni=0x0275, hex='0275', c='ɵ', base='o', isLower=True, anchors=['top'])
    GDS['odblgrave'] = GD(name='odblgrave', uni=0x020D, hex='020D', c='ȍ', bl='o', base='o', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['odieresismacron'] = GD(name='odieresismacron', uni=0x022B, hex='022B', c='ȫ', w='o', bl='o', base='o', accents=['dieresismacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['odotaccent'] = GD(name='odotaccent', uni=0x022F, hex='022F', c='ȯ', w='o', bl='o', base='o', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['odotaccentmacron'] = GD(name='odotaccentmacron', uni=0x0231, hex='0231', c='ȱ', w='o', bl='o', base='o', accents=['dotaccentmacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['oinvertedbreve'] = GD(name='oinvertedbreve', uni=0x020F, hex='020F', c='ȏ', base='o', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['omacronacute'] = GD(name='omacronacute', uni=0x1E53, hex='1E53', c='ṓ', l='o', r='o', base='o', accents=['macronacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['omacrongrave'] = GD(name='omacrongrave', uni=0x1E51, hex='1E51', c='ṑ', l='o', r='o', base='o', accents=['macrongravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['omega'] = GD(name='omega', uni=0x03C9, hex='03C9', c='ω', isLower=True, fixSpacing=False, anchors=['bottom', 'top'], comment='ω')
    GDS['omega_latin'] = GD(name='omega_latin', uni=0xA7B7, hex='A7B7', c='ꞷ', base='omega', isLower=True, anchors=['bottom', 'top'])
    GDS['oogonek'] = GD(name='oogonek', uni=0x01EB, hex='01EB', c='ǫ', base='o', accents=['ogonekcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['oogonekmacron'] = GD(name='oogonekmacron', uni=0x01ED, hex='01ED', c='ǭ', base='oogonek', accents=['macroncmb'], isLower=True, anchors=['top'])
    GDS['oslashacute'] = GD(name='oslashacute', uni=0x01FF, hex='01FF', c='ǿ', base='oslash', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ǿ')
    GDS['oslashacute.alt'] = GD(name='oslashacute.alt', base='oslash.alt', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], comment='ǿ')
    GDS['otildeacute'] = GD(name='otildeacute', uni=0x1E4D, hex='1E4D', c='ṍ', base='o', accents=['tildeacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['otildedieresis'] = GD(name='otildedieresis', uni=0x1E4F, hex='1E4F', c='ṏ', base='otilde', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['otildemacron'] = GD(name='otildemacron', uni=0x022D, hex='022D', c='ȭ', base='o', accents=['tildemacroncmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ou'] = GD(name='ou', uni=0x0223, hex='0223', c='ȣ', l='o', r='o')

    GDS['osuperior'] = GD(name='osuperior', uni=0x1D52, hex='1D52', c='ᵒ', l2r='osuperior', isLower=False, isMod=True)
    GDS['oinferior'] = GD(name='oinferior', uni=0x2092, hex='2092', c='ₒ', l='osuperior', r='osuperior', base='osuperior', isLower=True)

    # p

    GDS['pacute'] = GD(name='pacute', uni=0x1E55, hex='1E55', c='ṕ', l='p', w='p', base='p', accents=['acutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['phi_latin'] = GD(name='phi_latin', uni=0x0278, hex='0278', c='ɸ', l='phi', r='phi', base='ef_cy', isLower=True)
    GDS['phook'] = GD(name='phook', uni=0x01A5, hex='01A5', c='ƥ', l='khook', r='p', isLower=True)
    GDS['pstroke'] = GD(name='pstroke', uni=0x1D7D, hex='1D7D', c='ᵽ', l='hyphen', r='hyphen', base='p', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['psili'] = GD(name='psili', uni=0x1FBF, hex='1FBF', c='᾿', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, isLower=True)
    GDS['product'] = GD(l='H', r='H', uni=0x220f, c='∏', src='H', name='product', isLower=False, height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='∏ PRODUCT, N-ARY')

    GDS['psuperior'] = GD(name='psuperior', uni=0x1D56, hex='1D56', c='ᵖ', l='tsuperior', r='bsuperior', isLower=False, isMod=True)
    GDS['pinferior'] = GD(name='pinferior', uni=0x209A, hex='209A', c='ₚ', l='psuperior', r='psuperior', base='psuperior')
    #GDS['primesuperior'] = GD(name='primesuperior', uni=0x02B9, hex='02B9', c='ʹ', base='quoteright', isMod=True)

    # q

    GDS['qhooktail'] = GD(name='qhooktail', uni=0x024B, hex='024B', c='ɋ', l='o', w='q', srcName='q', isLower=True)
    GDS['qpdigraph'] = GD(name='qpdigraph', uni=0x0239, hex='0239', c='ȹ', l='q', r='p', isLower=True)
    GDS['quotesinglbase'] = GD(name='quotesinglbase', uni=0x201A, hex='201A', c='‚', l='quotesingle', r='quotesingle', isLower=True, base='comma', comment='‚ SINGLE LOW-9 QUOTATION MARK')

    GDS['qsuperior'] = GD(name='qsuperior', l='oinferior', r='linferior', isMod=True)
    GDS['qinferior'] = GD(name='qinferior', l='qsuperior', r='qsuperior', base='qsuperior', isMod=True) # Undefined unicode

    # r

    GDS['ramshorn'] = GD(name='ramshorn', uni=0x0264, hex='0264', c='ɤ', l='Y', r='Y', isLower=True)
    GDS['rdblgrave'] = GD(name='rdblgrave', uni=0x0211, hex='0211', c='ȑ', w='r', bl='r', base='r', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['rhook'] = GD(name='rhook', uni=0x027D, hex='027D', c='ɽ', l='r', w='r', isLower=True)
    GDS['rinvertedbreve'] = GD(name='rinvertedbreve', uni=0x0213, hex='0213', c='ȓ', base='r', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['rstroke'] = GD(name='rstroke', uni=0x024D, hex='024D', c='ɍ', base='r', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['radical'] = GD(name='radical', uni=0x221A, hex='221A', c='√', l='r', r='r', rightMin=-100, isLower=True, comment='√ SQUARE ROOT')

    GDS['rsuperior'] = GD(name='rsuperior', uni=0x02B3, hex='02B3', c='ʳ', l='nsuperior', r='r', isMod=True)
    GDS['rinferior'] = GD(name='rinferior', uni=0x1d63, hex='1d63', l='rsuperior', r='rsuperior', base='rsuperior', isMod=True)

    #GDS['rbelowcmb'] = GD(name='rbelowcmb', uni=0x1DCA, hex='1DCA', c='᷊', w=0, base='rsuperior', anchors=['_bottom', 'bottom'])

    # s

    GDS['sacutedotaccent'] = GD(name='sacutedotaccent', uni=0x1E65, hex='1E65', c='ṥ', l='s', w='s', base='s', accents=['acutedotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['saltillo'] = GD(name='saltillo', uni=0xA78C, hex='A78C', c='ꞌ', base='quotesingle', isLower=True)
    GDS['scarondotaccent'] = GD(name='scarondotaccent', uni=0x1E67, hex='1E67', c='ṧ', l='s', r='s', base='s', accents=['carondotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['sdotaccent'] = GD(name='sdotaccent', uni=0x1E61, hex='1E61', c='ṡ', l='s', r='s', base='s', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['sdotbelowdotaccent'] = GD(name='sdotbelowdotaccent', uni=0x1E69, hex='1E69', c='ṩ', l='s', r='s', base='sdotaccent', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['sobliquestroke'] = GD(name='sobliquestroke', uni=0xA7A9, hex='A7A9', c='ꞩ', srcName='s', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['secondtonechinese'] = GD(name='secondtonechinese', uni=0x02CA, hex='02CA', c='ˊ', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='acutecmb', isLower=True)
    GDS['summation'] = GD(l='H', r='E', uni=0x2211, c='∑', name='summation', src='E', isLower=False, height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='∑ SUMMATION, N-ARY')

    GDS['ssuperior'] = GD(name='ssuperior', uni=0x02E2, hex='02E2', c='ˢ', l2r='ssuperior', isMod=True)
    GDS['sinferior'] = GD(name='sinferior', uni=0x209B, hex='209B', c='ₛ', l='ssuperior', r='ssuperior', base='ssuperior', isLower=True)
    #GDS['schwasuperior'] = GD(name='schwasuperior', uni=0x1D4A, hex='1D4A', c='ᵊ', l2r='esuperior', r2l='esuperior', isLower=False, isMod=True)
    #GDS['schwainferior'] = GD(name='schwainferior', uni=0x2094, hex='2094', c='ₔ', l='schwasuperior', r='schwasuperior', base='schwasuperior', isLower=True)
    #GDS['shortequalsuperior'] = GD(name='shortequalsuperior', uni=0xA78A, srcName='equal', hex='A78A', c='꞊', l=plussuperior, r=plussuperior, isLower=True, isMod=True)

    GDS['equalinferior'] = GD(name='equalinferior', uni=0x208C, hex='208C', c='₌', l='plussuperior', r='plussuperior', base='equalsuperior', isLower=True)
    GDS['equalsuperior'] = GD(name='equalsuperior', uni=0x207C, hex='207C', c='⁼', l='plussuperior', r='plussuperior', srcName='shortequalsuperior', isLower=True)

    # t

    GDS['tbar'] = GD(name='tbar', uni=0x0167, hex='0167', c='ŧ', l='t', r='t', base='t', isLower=True, comment='ŧ T WITH STROKE, LATIN SMALL LETTER')
    GDS['tcircumflexbelow'] = GD(name='tcircumflexbelow', uni=0x1E71, hex='1E71', c='ṱ', base='t', accents=['circumflexbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['tdiagonalstroke'] = GD(name='tdiagonalstroke', uni=0x2C66, hex='2C66', c='ⱦ', w='t', bl='t', base='t', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['tdieresis'] = GD(name='tdieresis', uni=0x1E97, hex='1E97', c='ẗ', w='t', bl='t', base='t', accents=['dieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['tdotaccent'] = GD(name='tdotaccent', uni=0x1E6B, hex='1E6B', c='ṫ', base='t', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['tesh'] = GD(name='tesh', uni=0x02A7, hex='02A7', c='ʧ', l='t', r='off', base='t', isLower=True)
    GDS['theta'] = GD(name='theta', uni=0x03B8, hex='03B8', c='θ')
    GDS['thook'] = GD(name='thook', uni=0x01AD, hex='01AD', c='ƭ', l='t', w='t', srcName='t', isLower=True)
    GDS['tildebelowcmb'] = GD(name='tildebelowcmb', uni=0x0330, hex='0330', c='̰', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='tildecmb', isLower=True, anchors=['_bottom', 'bottom'])
    # Not separate /tildebelow with spacing without unicide. 
    #GDS['tildebelow'] = GD(name='tildebelow', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='tildebelowcmb', anchors=[], isLower=True, gid=1706)
    GDS['tildeoverlaycmb'] = GD(name='tildeoverlaycmb', uni=0x0334, hex='0334', c='̴', autoFixComponentPositions=False, autoFixMargins=False, w=0, base='tildecmb', isLower=True, anchors=['_middle', 'middle'])
    GDS['tretroflexhook'] = GD(name='tretroflexhook', uni=0x0288, hex='0288', c='ʈ', l='t', r='t', srcName='t', isLower=True)

    GDS['tsuperior'] = GD(name='tsuperior', isLower=True, anchors=[]) # No unicode for this one. uni=0x0000, hex='0000', c='????', 
    GDS['tinferior'] = GD(name='tinferior', uni=0x209C, hex='209C', c='ₜ', l='tsuperior', r='tsuperior', base='tsuperior', isLower=True)

    # u

    GDS['ucircumflexbelow'] = GD(name='ucircumflexbelow', uni=0x1E77, hex='1E77', c='ṷ', l='u', r='u', base='u', accents=['circumflexbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['udblgrave'] = GD(name='udblgrave', uni=0x0215, hex='0215', c='ȕ', w='u', bl='u', base='u', accents=['dblgravecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['udieresisbelow'] = GD(name='udieresisbelow', uni=0x1E73, hex='1E73', c='ṳ', l='u', r='u', base='u', accents=['dieresisbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['uinvertedbreve'] = GD(name='uinvertedbreve', uni=0x0217, hex='0217', c='ȗ', base='u', accents=['invertedbrevecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['umacrondieresis'] = GD(name='umacrondieresis', uni=0x1E7B, hex='1E7B', c='ṻ', l='u', r='u', base='u', accents=['macrondieresiscmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['uniA7AE'] = GD(name='uniA7AE', uni=0xA7AE, hex='A7AE', c='Ɪ', r='I.sc', l2r='I.sc', base='I.sc', isLower=True)
    GDS['upsilon_latin'] = GD(name='upsilon_latin', uni=0x028A, hex='028A', c='ʊ', l='o', r='o', isLower=True)
    GDS['utildeacute'] = GD(name='utildeacute', uni=0x1E79, hex='1E79', c='ṹ', base='u', accents=['tildeacutecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['utildebelow'] = GD(name='utildebelow', uni=0x1E75, hex='1E75', c='ṵ', base='u', accents=['tildebelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    # Change from /ubar
    GDS['ustroke'] = GD(name='ustroke', uni=0x0289, hex='0289', c='ʉ', l='u', r='u', base='u', isLower=True, anchors=['bottom', 'middle', 'top'], comment="LATIN SMALL LETTER U BAR")

    GDS['usuperior'] = GD(name='usuperior', uni=0x1D58, hex='1D58', c='ᵘ', l2r='nsuperior', r2l='nsuperior', isMod=True)
    GDS['uinferior'] = GD(name='uinferior', uni=0x1D64, hex='1D64', l='usuperior', r='usuperior', base='usuperior', isMod=True)

    # v

    GDS['vdotbelow'] = GD(name='vdotbelow', uni=0x1E7F, hex='1E7F', c='ṿ', base='v', accents=['dotbelowcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['vhook'] = GD(name='vhook', uni=0x028B, hex='028B', c='ʋ', isLower=True)
    GDS['vtilde'] = GD(name='vtilde', uni=0x1E7D, hex='1E7D', c='ṽ', l='v', r='v', base='v', accents=['tildecmb'], isLower=True, anchors=['bottom', 'middle', 'top'])

    GDS['vsuperior'] = GD(name='vsuperior', uni=0x1D5B, hex='1D5B', c='ᵛ', l2r='vsuperior', isMod=True)
    GDS['vinferior'] = GD(name='vinferior', uni=0x1D65, hex='1D65', l='vsuperior', r='vsuperior', base='vsuperior', isMod=True)
 
    GDS['verticallinesuperior'] = GD(name='verticallinesuperior', uni=0x02C8, hex='02C8', r2l='jsuperior', r='jsuperior', c='ˈ', isMod=True)
    GDS['verticallineinferior'] = GD(name='verticallineinferior', uni=0x02CC, hex='02CC', c='ˌ',base='verticallinesuperior', l='verticallinesuperior', r='verticallinesuperior', isMod=True)

    GDS['verticallineabovecmb'] = GD(name='verticallineabovecmb', uni=0x030D, hex='030D', c='̍', l=GD.CAT_CENTER, w=0, isLower=True, anchors=['_top', 'top'])
    GDS['verticallinebelowcmb'] = GD(name='verticallinebelowcmb', uni=0x0329, hex='0329', c='̩', l=GD.CAT_CENTER, w=0, isLower=True, anchors=['_bottom', 'bottom'])

    # w

    GDS['wdotaccent'] = GD(name='wdotaccent', uni=0x1E87, hex='1E87', c='ẇ', l='w', r='w', base='w', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['whook'] = GD(name='whook', uni=0x2C73, hex='2C73', c='ⱳ', l='w', isLower=True)
    GDS['wring'] = GD(name='wring', uni=0x1E98, hex='1E98', c='ẘ', l='w', r='w', base='w', accents=['ringcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['won'] = GD(name='won', uni=0x20A9, hex='20A9', c='₩', l='W', l2r='W', srcName='W', isLower=False)

    GDS['wsuperior'] = GD(name='wsuperior', uni=0x02B7, hex='02B7', c='ʷ', l='vsuperior', r='vsuperior', isMod=True)
    GDS['winferior'] = GD(name='winferior', l='wsuperior', r='wsuperior', base='wsuperior', isMod=True) # Undefined unicode

    # x

    GDS['xdotaccent'] = GD(name='xdotaccent', uni=0x1E8B, hex='1E8B', c='ẋ', l='x', r='x', base='x', accents=['dotaccentcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])

    GDS['xsuperior'] = GD(name='xsuperior', uni=0x02E3, hex='02E3', c='ˣ', l2r='xsuperior', isMod=True)
    GDS['xinferior'] = GD(name='xinferior', uni=0x2093, hex='2093', c='ₓ', l='xsuperior', r='xsuperior', base='xsuperior', isLower=True)

    # y

    GDS['yogh'] = GD(name='yogh', uni=0x021D, hex='021D', c='ȝ', l='three', r='three', base='three', isLower=True)
    GDS['yring'] = GD(name='yring', uni=0x1E99, hex='1E99', c='ẙ', l='y', r='y', base='y', accents=['ringcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['Yring.sc'] = GD(name='Yring.sc', l='Y.sc', r='Y.sc', base='Y.sc', accents=['ringcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['ystroke'] = GD(name='ystroke', uni=0x024F, hex='024F', c='ɏ', l='hyphen', r='hyphen', base='y', isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['yturned'] = GD(name='yturned', uni=0x028E, hex='028E', c='ʎ', w='y', r2l='y', isLower=True)

    GDS['ysuperior'] = GD(name='ysuperior', uni=0x02B8, hex='02B8', c='ʸ', isMod=True)
    GDS['yinferior'] = GD(name='yinferior', l='ysuperior', r='ysuperior', base='ysuperior', isMod=True) # Undefined unicode

    # z

    GDS['zcircumflex'] = GD(name='zcircumflex', uni=0x1E91, hex='1E91', c='ẑ', l='z', r='z', base='z', accents=['circumflexcmb'], isLower=True, anchors=['bottom', 'middle', 'top'])
    GDS['zstroke'] = GD(name='zstroke', uni=0x01B6, hex='01B6', c='ƶ', l='z', r='z', base='z', isLower=True)

    GDS['zsuperior'] = GD(name='zsuperior', uni=0x1DBB, hex='1DBB', c='ᶻ', l2r='zsuperior', isMod=True)
    GDS['zinferior'] = GD(name='zinferior', l='zsuperior', r='zsuperior', base='zsuperior', isMod=True) # Undefined unicode

    # Figures for fractions

    GDS['one.dnom'] = GD(name='one.dnom', l='onesuperior', r='onesuperior', base='onesuperior', isLower=False)
    GDS['two.dnom'] = GD(name='two.dnom', l='twosuperior', r='twosuperior', base='twosuperior', isLower=False)
    GDS['three.dnom'] = GD(name='three.dnom', l='threesuperior', r='threesuperior', base='threesuperior', isLower=False)
    GDS['four.dnom'] = GD(name='four.dnom', l='foursuperior', r='foursuperior', base='foursuperior', isLower=False)
    GDS['five.dnom'] = GD(name='five.dnom', l='fivesuperior', r='fivesuperior', base='fivesuperior', isLower=False)
    GDS['six.dnom'] = GD(name='six.dnom', l='sixsuperior', r='sixsuperior', base='sixsuperior', isLower=False)
    GDS['seven.dnom'] = GD(name='seven.dnom', l='sevensuperior', r='sevensuperior', base='sevensuperior', isLower=False)
    GDS['eight.dnom'] = GD(name='eight.dnom', l='eightsuperior', r='eightsuperior', base='eightsuperior', isLower=False)
    GDS['nine.dnom'] = GD(name='nine.dnom', l='ninesuperior', r='ninesuperior', base='ninesuperior', isLower=False)
    GDS['zero.dnom'] = GD(name='zero.dnom', l='zerosuperior', r='zerosuperior', base='zerosuperior', isLower=False)

    GDS['one.numr'] = GD(name='one.numr', l='onesuperior', r='onesuperior', base='onesuperior', isLower=False)
    GDS['two.numr'] = GD(name='two.numr', l='twosuperior', r='twosuperior', base='twosuperior', isLower=False)
    GDS['three.numr'] = GD(name='three.numr', l='threesuperior', r='threesuperior', base='threesuperior', isLower=False)
    GDS['four.numr'] = GD(name='four.numr', l='foursuperior', r='foursuperior', base='foursuperior', isLower=False)
    GDS['five.numr'] = GD(name='five.numr', l='fivesuperior', r='fivesuperior', base='fivesuperior', isLower=False)
    GDS['six.numr'] = GD(name='six.numr', l='sixsuperior', r='sixsuperior', base='sixsuperior', isLower=False)
    GDS['seven.numr'] = GD(name='seven.numr', l='sevensuperior', r='sevensuperior', base='sevensuperior', isLower=False)
    GDS['eight.numr'] = GD(name='eight.numr', l='eightsuperior', r='eightsuperior', base='eightsuperior', isLower=False)
    GDS['nine.numr'] = GD(name='nine.numr', l='ninesuperior', r='ninesuperior', base='ninesuperior', isLower=False)
    GDS['zero.numr'] = GD(name='zero.numr', l='zerosuperior', r='zerosuperior', base='zerosuperior', isLower=False)
    
    GDS['zeroslash.onum'] = GD(name='zeroslash.onum', l='zero.onum', r='zero.onum', isLower=False)

    # Accents

    GDS['tildebelowcmb'] = GD(name='tildebelowcmb', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='tildecmb', isLower=True, anchors=['bottom', '_bottom'])
    GDS['slashlongcmb'] = GD(name='slashlongcmb', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_middle'])
    GDS['dotmiddlecmb'] = GD(name='dotmiddlecmb', w=0, anchors=['_dot'], autoFixComponentPositions=False, autoFixMargins=False, isLower=True, base='dotaccentcmb')
    GDS['strokecmb'] = GD(name='strokecmb', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_middle'])
    GDS['invertedbrevecmb'] = GD(name='invertedbrevecmb', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, anchors=['_top', 'top'], srcName='brevecmb')
    GDS['macronbelowcmb'] = GD(name='macronbelowcmb', uni=0x0331, hex='0331', c='̱', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='macroncmb', isLower=True, anchors=['bottom', '_bottom'], comment='COMBINING MACRON BELOW')
    GDS['ringbelowcmb'] = GD(name='ringbelowcmb', uni=0x0325, hex='0325', c='̥', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, base='ringcmb', isLower=True, anchors=['_bottom', 'bottom'], comment='COMBINING RING BELOW')

    GDS['dblgravecmb'] = GD(name='dblgravecmb', uni=0x030F, hex='030F', c='̏', l=GD.CAT_CENTER, w=0, anchorTopX=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, base='gravecmb', accents=['gravecmb'], anchors=['top', '_top'])
    GDS['dblgravecmb.uc'] = GD(name='dblgravecmb.uc', l=GD.CAT_CENTER, w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='dblgravecmb', isLower=False, anchors=['_top', 'top'])
    GDS['dotaboverightcmb'] = GD(name='dotaboverightcmb', uni=0x0358, hex='0358', c='͘', w=0, autoFixComponentPositions=False, autoFixMargins=False, base='dotaccentcmb', isLower=True, anchors=['_top', 'top'])
    GDS['dotaboverightcmb.uc'] = GD(name='dotaboverightcmb.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, srcName='dotaboverightcmb', isLower=False, anchors=['_top', 'top'])
    GDS['doublebrevebelowcmb'] = GD(name='doublebrevebelowcmb', uni=0x035C, hex='035C', c='͜', w=0 , autoFixComponentPositions=False, autoFixMargins=False, base='doublebrevecmb', isLower=True, anchors=['_bottom', 'bottom'])
    GDS['doublebrevecmb'] = GD(name='doublebrevecmb', uni=0x035D, hex='035D', c='͝', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=True, anchors=['_top', 'top'])
    GDS['doublebrevecmb.uc'] = GD(name='doublebrevecmb.uc', w=0, srcName='doublebrevecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top'])

    GDS['slashlongcmb.uc'] = GD(name='slashlongcmb.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_middle'])
    GDS['strokecmb.uc'] = GD(name='strokecmb.uc', w=0, srcName='strokecmb', autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_middle'])
    GDS['invertedbrevecmb.uc'] = GD(name='invertedbrevecmb.uc', w=0, autoFixComponentPositions=False, autoFixMargins=False, isLower=False, anchors=['_top', 'top'], srcName='brevecmb.uc')

    # Fractions

    GDS['onefraction'] = GD(name='onefraction', uni=0x215F, hex='215F', c='⅟', base='one.numr', accents=['fraction'], isLower=False)
    GDS['onehalf'] = GD(name='onehalf', uni=0x00BD, hex='00BD', c='½', base='one.numr', accents=['fraction', 'two.dnom'], isLower=False, gid=126, comment='½ VULGAR FRACTION ONE HALF')
    GDS['onethird'] = GD(name='onethird', uni=0x2153, hex='2153', c='⅓', l='one.numr', r='three.dnom', base='one.numr', accents=['fraction', 'three.dnom'], isLower=False)
    GDS['onequarter'] = GD(name='onequarter', uni=0x00BC, hex='00BC', c='¼', l='one.numr', r='four.dnom', base='one.numr', accents=['fraction', 'four.dnom'], isLower=True, gid=125, comment='¼ VULGAR FRACTION ONE QUARTER')
    GDS['onefifth'] = GD(name='onefifth', uni=0x2155, hex='2155', c='⅕', l='one.numr', r='five.dnom', base='one.numr', accents=['fraction', 'five.dnom'], isLower=False)
    GDS['onesixth'] = GD(name='onesixth', uni=0x2159, hex='2159', c='⅙', l='one.numr', r='six.dnom', base='one.numr', accents=['fraction', 'six.dnom'], isLower=False)
    GDS['oneseventh'] = GD(name='oneseventh', uni=0x2150, hex='2150', c='⅐', l='one.numr', r='seven.dnom', base='one.numr', accents=['fraction', 'seven.dnom'], isLower=False)
    GDS['oneeighth'] = GD(name='oneeighth', uni=0x215B, hex='215B', c='⅛', l='one.numr', r='eight.dnom', base='one.numr', accents=['fraction', 'eight.dnom'], isLower=False, gid=1472, comment='⅛ Fractions Eighths')
    GDS['oneninth'] = GD(name='oneninth', uni=0x2151, hex='2151', c='⅑', l='one.numr', r='nine.dnom', base='one.numr', accents=['fraction', 'nine.dnom'], isLower=False)
    GDS['onetenth'] = GD(name='onetenth', uni=0x2152, hex='2152', c='⅒', l='one.numr', r='zero.dnom', base='one.numr', accents=['fraction', 'one.dnom', 'zero.dnom'], isLower=False)

    GDS['twothirds'] = GD(name='twothirds', uni=0x2154, hex='2154', c='⅔', l='two.numr', r='three.dnom', base='two.numr', accents=['fraction', 'three.dnom'], isLower=False)
    GDS['twofifths'] = GD(name='twofifths', uni=0x2156, hex='2156', c='⅖', l='two.numr', r='five.dnom', base='two.numr', accents=['fraction', 'five.dnom'], isLower=False)

    GDS['threequarters'] = GD(name='threequarters', uni=0x00BE, hex='00BE', c='¾', l='three.numr', r='four.dnom', base='three.numr', accents=['fraction', 'four.dnom'], isLower=False, gid=127, comment='¾ VULGAR FRACTION THREE QUARTERS')
    GDS['threefifths'] = GD(name='threefifths', uni=0x2157, hex='2157', c='⅗', l='three.numr', r='five.dnom', base='three.numr', accents=['fraction', 'five.dnom'], isLower=False)
    GDS['threeeighths'] = GD(name='threeeighths', uni=0x215C, hex='215C', c='⅜', l='three.numr', r='eight.dnom', base='three.numr', accents=['fraction', 'eight.dnom'], isLower=False, gid=1473, comment='⅜')

    GDS['fourfifths'] = GD(name='fourfifths', uni=0x2158, hex='2158', c='⅘', l='four.numr', r='five.dnom', base='four.numr', accents=['fraction', 'five.dnom'], isLower=False)

    GDS['fivesixths'] = GD(name='fivesixths', uni=0x215A, hex='215A', c='⅚', l='five.numr', r='six.dnom', base='five.numr', accents=['fraction', 'six.dnom'], isLower=False)
    GDS['fiveeighths'] = GD(name='fiveeighths', uni=0x215D, hex='215D', c='⅝', l='five.numr', r='eight.dnom', base='five.numr', accents=['fraction', 'eight.dnom'], isLower=False, gid=1474, comment='⅝')

    GDS['seveneighths'] = GD(name='seveneighths', uni=0x215E, hex='215E', c='⅞', l='seven.numr', r='eight.dnom', base='seven.numr', accents=['fraction', 'eight.dnom'], isLower=False, gid=1475, comment='⅞')

# Make exceptions here for Italic glyphs and spacing rules in LATIN_L_SET_ITALIC

GDSI = LATIN_L_SET_ITALIC
GDSI['qhooktail'].l = 'a'
GDSI['hturned'].l = 'u'
GDSI['hturned'].r = 'q'
GDSI['vhook'].l = GDSI['vhook'].r = 'v'
GDSI['gstroke'].r = 'hyphen'
GDSI['phook'].l = 'bhook'
GDSI['hhook'].l = 'bhook'
GDSI['henghook'].l = 'bhook'



if __name__ == '__main__':
    for gName, gd in LATIN_L_SET.items():
        #print('---', gd)
        if gd.base and gd.base not in LATIN_L_SET:
            print('##### Missing base', gName, gd.base)
        for aName in gd.accents:
            if aName not in GDS:
                print('#### Missing accent', gName, aName)

