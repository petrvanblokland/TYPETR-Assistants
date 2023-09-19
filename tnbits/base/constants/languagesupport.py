# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
class LanguageSupport(object):
    """
    THIS IS JUST A START.

    It is hard to capture.

    SPECIAL_CHARS_BY_LANGUAGE_REQUIRED: Mostly sourced from
    <http://www.eki.ee/letter/>. These are required special characters for the
    basic typesetting of each language. It is assumed that Basic Latin is
    required to write all of them, even though. Caveats simplified or commented
    out where possible.

    SPECIAL_CHARS_BY_LANGUAGE_IMPORTANT: Mostly sourced from
    <http://www.eki.ee/letter/>. These are letters which are important to the
    language, but not required in everday setting. Mostly due to common
    loanwords or regional names/placenames.

    SPECIAL_SORTS_BY_LANGUAGE: Not done yet. Thinking about special currency
    glyphs or quotation glyphs that are used.
    <http://en.wikipedia.org/wiki/Non-English_usage_of_quotation_marks>

    Issues:
        - Special characters for Cyrillic is missing.
        - OpenType language tags do not cover all of the language listings. We
          may want to switch to (openTypeScript, ISOcode) tuples.
        - Different sources have different results. Need to some how get
          everything on the same page.
    """

    ROMAN_NUMERAL_VALUES = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}

    SPECIAL_CHARS_BY_LANGUAGE_REQUIRED = {
    # Afrikaans
    'AFK': [200, 232, 201, 233, 202, 234, 203, 235, 206, 238, 207, 239, 212, 244, 219],
    # Azeri
    'AZE': [199, 231, 399, 601, 286, 287, 304, 305, 214, 246, 350, 351, 220, 252],
    # Belarusian
    'BEL': [262, 263, 268, 269, 321, 322, 323, 324, 346, 347, 352, 353, 364,
        365, 377, 378, 381, 382],
    # Bislama
    'BIS': [201, 233, 207, 239, 57344, 57345, 57346, 57347, 220, 252],
    # Bosnian
    'BOS': [262, 263, 268, 269, 272, 273, 352, 353, 381, 382],
    # Breton
    'BRE': [194, 226, 202, 234, 209, 241, 212, 244, 217, 249, 220, 252],
    # Catalan
    'CAT': [192, 224, 199, 231, 200, 232, 201, 233, 205, 237, 207, 239, 319,
        320, 210, 242, 211, 243, 218, 250, 220, 252],
    #Czech
    'CSY': [193, 225, 268, 269, 270, 271, 201, 233, 282, 283, 205, 237, 327,
        328, 211, 243, 344, 345, 352, 353, 356, 357, 218, 250, 366, 367, 221,
        253, 381, 382],
    #Welsh
    'WEL': [193, 225, 192, 224, 194, 226, 196, 228, 201, 233, 200, 232, 202,
        234, 203, 235, 205, 237, 204, 236, 206, 238, 207, 239, 211, 243, 210,
        242, 212, 244, 214, 246, 218, 250, 217, 249, 219, 251, 220, 252, 221,
        253, 7922, 7923, 374, 375, 376, 255, 372, 373],
    #Danish
    'DAN': [197, 229, 198, 230, 201, 233, 216, 248],
    #German
    'DEU': [196, 228, 214, 246, 223, 220, 252],
    #Esperanto
    'NTO': [264, 265, 284, 285, 292, 293, 308, 309, 348, 349, 364, 365],
    #Spanish
    'ESP': [193, 225, 201, 233, 205, 237, 209, 241, 211, 243, 218, 250, 220, 252],
    #Estonian
    'ETI': [196, 228, 213, 245, 214, 246, 352, 353, 220, 252, 381, 382],
    #Basque
    'EUQ': [199, 231, 209, 241, 220, 252],
    #Finnish
    'FIN': [196, 228, 214, 246],
    #Faroese
    'FOS': [193, 225, 198, 230, 208, 240, 205, 237, 211, 243, 216, 248, 218, 250, 221, 253],
    #French
    'FRA': [192, 224, 194, 226, 199, 231, 200, 232, 201, 233, 202, 234, 203, 235, 206, 238, 207, 239, 212, 244, 338, 339, 217, 249, 219, 251, 220, 252, 376, 255],
    #Frisian
    'FRI': [194, 226, 202, 234, 206, 238, 212, 244, 218, 250, 219, 251],
    #Irish (Irish Gaelic?)
    'IRI': [193, 225, 201, 233, 205, 237, 211, 243, 218, 250],
    #Gaelic
    'GAE': [192, 224, 193, 225, 200, 232, 201, 233, 204, 236, 210, 242, 211, 243, 217, 249],
    #Galican
    'GAL': [193, 225, 201, 233, 205, 237, 209, 241, 211, 243, 218, 250, 220, 252],
    #Guarani
    'GUA': [193, 225, 227, 201, 233, 7869, 57349, 205, 237, 297, 209, 241, 211, 243, 245, 218, 250, 361, 7929],
    #Hausa
    'HAU': [385, 595, 394, 599],
    #Fulani
    'FUL': [385, 595, 394, 599, 330, 331, 626],
    #Hawaiian
    'HAW': [256, 257, 274, 275, 298, 299, 332, 333, 362, 363],
    #Croatian
    'HRV': [262, 263, 268, 269, 272, 273, 352, 353, 381, 382],
    #Hungarian
    'HUN': [193, 225, 201, 233, 205, 237, 211, 243, 214, 246, 336, 337, 218, 250, 220, 252, 368, 369],
    #Ibo
    'IBO': [7882, 7883, 7884, 7885, 7908, 7909],
    #Indonesian
    'IND': [201, 233],
    #Icelandic
    'ISL': [193, 225, 198, 230, 208, 240, 201, 233, 205, 237, 211, 243, 214, 246, 222, 254, 218, 250, 221, 253],
    #Italian
    'ITA': [192, 224, 200, 232, 201, 233, 204, 236, 210, 242, 211, 243, 217, 249],
    #Greenlandic
    'GRN': [197, 229, 198, 230, 216, 248],
    #Kashubian
    'CSB': [260, 261, 195, 227, 201, 233, 203, 235, 321, 322, 323, 324, 210, 242, 211, 243, 212, 244, 217, 249, 379, 380],
    #Kurdish
    'KUR': [201, 233, 205, 237, 217, 249, 218, 250],
    #Luxembourgish
    'LTZ': [196, 228, 201, 233, 203, 235, 214, 246, 220, 252],
    #Lithuanian
    'LTH': [260, 261, 268, 269, 280, 281, 278, 279, 302, 303, 352, 353, 370, 371, 362, 363, 381, 382],
    #Latvian
    'LVI': [256, 257, 268, 269, 274, 275, 290, 291, 298, 299, 310, 311, 315, 316, 325, 326, 352, 353, 362, 363, 381, 382],
    #Marshallese
    'MAH': [256, 257, 315, 316, 57354, 57355, 57356, 57357, 325, 326, 332, 333, 57358, 57359, 362, 363],
    #Malagasy
    'MLG': [193, 225, 57360, 57361, 212, 244],
    #Maori
    'MRI': [256, 257, 274, 275, 298, 299, 332, 333, 362, 363],
    #Maltese
    'MTS': [192, 224, 266, 267, 200, 232, 288, 289, 294, 295, 204, 236, 206, 238, 210, 242, 217, 249, 379, 380],
    #Dutch
    'NLD': [193, 225, 194, 226, 200, 232, 201, 233, 202, 234, 203, 235, 205, 237, 207, 239, 306, 307, 211, 243, 212, 244, 214, 246, 218, 250, 219, 251],
    #Flemish (Beligan Dutch)
    'FLE': [193, 225, 194, 226, 200, 232, 201, 233, 202, 234, 203, 235, 205, 237, 207, 239, 306, 307, 211, 243, 212, 244, 214, 246, 218, 250, 219, 251], # Flemish is same as dutch
    #Norwegian
    'NOR': [198, 230, 216, 248, 197, 229],
    #Northern Sotho
    'SOT': [202, 234, 212, 244, 352, 353], # this is northern sotho
    #Chichewa
    'CHI': [372, 373],
    #Occitan
    'OCI': [193, 225, 192, 224, 199, 231, 201, 233, 200, 232, 205, 237, 211, 243, 210, 242, 218, 250],
    #Provencal (dialect of Occitan)
    'PRO': [193, 225, 192, 224, 199, 231, 201, 233, 200, 232, 205, 237, 211, 243, 210, 242, 218, 250], # same as occitan?
    #Polish
    'PLK': [260, 261, 262, 263, 280, 281, 321, 322, 323, 324, 211, 243, 346, 347, 377, 378, 379, 380],
    #Portuguese
    'PTG': [192, 224, 193, 225, 194, 226, 195, 227, 199, 231, 201, 233, 202, 234, 205, 237, 211, 243, 212, 244, 213, 245, 218, 250, 220, 252],
    #Rhaeto-Romanic
    'RMS': [192, 224, 200, 232, 201, 233, 204, 236, 206, 238, 210, 242, 217, 249],
    #Romanian
    'ROM': [194, 226, 258, 259, 206, 238, 536, 537, 538, 539], # PLUS S and T with Cedilla for backwards support?
    #Moldovan (Adopted Romanian alphabet)
    'MOL': [194, 226, 258, 259, 206, 238, 536, 537, 538, 539], # Same as romanian?
    #Sami - Inari
    'ISM': [193, 225, 194, 226, 196, 228, 268, 269, 272, 273, 330, 331, 352, 353, 381, 382],
    #Sami - Northern
    'NSM': [193, 225, 268, 269, 272, 273, 330, 331, 352, 353, 358, 359, 381, 382],
    #Sami - Lule
    'LSM': [193, 225, 196, 228, 197, 229, 209, 241],
    #Sami - Skolt
    'SKS': [194, 226, 196, 228, 197, 229, 268, 269, 272, 273, 439, 658, 494, 495, 486, 487, 484, 485, 488, 489, 330, 331, 213, 245, 352, 353, 381, 382],
    #Sami - Southern
    'SSM': [196, 228, 197, 229, 214, 246],
    #Slovak
    'SKY': [193, 225, 196, 228, 268, 269, 270, 271, 201, 233, 205, 237, 313, 314, 317, 318, 327, 328, 211, 243, 212, 244, 340, 341, 352, 353, 356, 357, 218, 250, 221, 253, 381, 382],
    #Slovenian
    'SLV': [268, 269, 352, 353, 381, 382],
    #Lower Sorbian
    'LSB': [262, 263, 268, 269, 282, 283, 321, 322, 323, 324, 340, 341, 346, 347, 352, 353, 377, 378, 381, 382],
    #Upper Sorbian
    'USB': [262, 263, 268, 269, 282, 283, 321, 322, 323, 324, 211, 243, 344, 345, 352, 353, 377, 378, 381, 382],
    #Albanian
    'SQI': [199, 231, 203, 235],
    #Serbian
    'SRB': [262, 263, 268, 269, 272, 273, 352, 353, 381, 382],
    #Swedish
    'SVE': [196, 228, 197, 229, 201, 233, 214, 246],
    #Turkmen
    'TKM': [381, 382, 221, 253, 327, 328, 214, 246, 220, 252, 199, 231, 350, 351, 196, 228],
    #Tagalog (Pilipino)
    'PIL': [209, 241],
    #Tswana
    'TNA': [202, 234, 212, 244, 352, 353],
    #Turkish
    'TRK': [194, 226, 199, 231, 286, 287, 206, 238, 304, 305, 214, 246, 350, 351, 219, 251, 220, 252],
    #Tatar
    'TAT': [399, 601, 199, 231, 286, 287, 304, 305, 57370, 57371, 57372, 57373, 350, 351, 220, 252],
    #Uzbek
    'UZB': [57362, 57363, 57364, 57365],
    #Vietnamese
    'VIT': [192, 224, 193, 225, 194, 226, 7846, 7847, 7844, 7845, 7850, 7851,
            7848, 7849, 7852, 7853, 195, 227, 258, 259, 7856, 7857, 7854, 7855,
            7860, 7861, 7858, 7859, 7862, 7863, 7842, 7843, 7840, 7841, 272,
            273, 200, 232, 201, 233, 202, 234, 7872, 7873, 7870, 7871, 7876,
            7877, 7874, 7875, 7878, 7879, 7868, 7869, 7866, 7867, 7864, 7865,
            204, 236, 205, 237, 296, 297, 7880, 7881, 7882, 7883, 210, 242,
            211, 243, 212, 244, 7890, 7891, 7888, 7889, 7894, 7895, 7892, 7893,
            7896, 7897, 213, 245, 7886, 7887, 416, 417, 7900, 7901, 7898, 7899,
            7904, 7905, 7902, 7903, 7906, 7907, 7884, 7885, 217, 249, 218, 250,
            360, 361, 7910, 7911, 431, 432, 7914, 7915, 7912, 7913, 7918, 7919,
            7916, 7917, 7920, 7921, 7908, 7909, 7922, 7923, 221, 253, 7928,
            7929, 7926, 7927, 7924, 7925],
    #Wolof
    'WLF': [192, 224, 195, 227, 201, 233, 203, 235, 209, 241, 330, 331, 211, 243],
    #Walloon
    'WLN': [197, 229, 194, 226, 199, 231, 202, 234, 201, 233, 200, 232, 206,
            238, 212, 244, 219, 251],
    #Yapese
    'YAP': [196, 228, 203, 235, 214, 246],
    #Yoruba
    'YBA': [192, 224, 193, 225, 194, 226, 461, 462, 200, 232, 201, 233, 202,
            234, 282, 283, 7864, 7865, 204, 236, 205, 237, 206, 238, 463, 464,
            57344, 57345, 323, 324, 57356, 57357, 210, 242, 211, 243, 212, 244,
            465, 466, 7884, 7885, 7778, 7779, 217, 249, 218, 250, 219, 251,
            467, 468],
    #####################################################

    'ROY': [268, 352, 381, 269, 353, 382], # from wikipedia
    ######################################################
    # SUPPORTED LANGUAGES WITHOUT SPECIAL CHARACTERS
    #English
    'ENG': [],
    #Fijian
    'FJI': [],
    #Latin
    'LAT': [],
    #Malay
    'MLY': [],
    #Samoan
    'SMO': [],
    #Swahili
    'SWK': [],
    ##################################################
    #Languages not in OpenType spec
    'Ulithian': [278, 279, 558, 559],
    }

    SPECIAL_CHARS_BY_LANGUAGE_IMPORTANT = {
    #Afrikaans
    #'AFK': [251], # override because napostrophe is out of date
    #Azeri
    #'AZE': [196, 228], # A with diaeresis is important only as a replacement character for schwa if the latter cannot be used. These cases should be avoided!
    #Catalan
    'CAT': [209, 241], #ntilde
    #Danish
    'DAN': [193, 225, 205, 237, 211, 243, 218, 250, 221, 253],
    #German
    'DEU': [192, 224, 201, 233],
    #English
    'ENG': [198, 230, 199, 231, 207, 239, 212, 244],
    #Spanish
    'ESP': [199, 231, 207, 239] + [170, 186], # including ordfeminine and ordmasculine
    #Finnish
    'FIN': [197, 229, 352, 353, 381, 382],  #There are geographical names in North Saami orthography.
    #French
    'FRA': [198, 230],
    #Frisian
    'FRI': [201, 233, 196, 228, 203, 235, 207, 239, 214, 246, 220, 252],
    #Italian
    'ITA': [193, 225, 205, 237, 206, 238, 207, 239, 218, 250],
    #Greenlandic
    'GRN': [193, 225, 194, 226, 195, 227, 201, 233, 202, 234, 205, 237, 206, 238, 296, 297, 312, 212, 244, 218, 250, 219, 251, 360, 361], #Note: Modern Greenlandic uses only basic latin alphabet
    #Kurdish
    'KUR': [199, 231, 202, 234, 206, 238, 350, 351, 219, 251],
    #Luxembourgish
    #'LTZ': [194, 226, 200, 232, 202, 234, 206, 238, 57350, 57351, 57352, 57353, 212, 244, 219, 251, 223],
    #Support for mcircumflex and ncircumflex is no longer needed
    'LTZ': [194, 226, 200, 232, 202, 234, 206, 238, 212, 244, 219, 251, 223],
    #Latvian
    'LVI': [332, 333, 342, 343],
    #Dutch
    'NLD': [196, 228, 220, 252],
    #Flemish
    'FLE': [196, 228, 220, 252],
    #Norwegian
    'NOR': [192, 224, 201, 233, 202, 234, 211, 243, 210, 242, 212, 244],
    #Portuguese
    # 'PTG': [200, 232, 210, 242], #these characters are out of use
    'PTG': [170, 186], # including ordfeminine and ordmasculine
    #Slovenian
    'SLV': [262, 263, 272, 273, 196, 228, 214, 246, 220, 252],
    #Swedish
    'SVE': [193, 225, 192, 224, 203, 235, 220, 252],
    #Tagalog/Pilipino
    #Only n~ is required for everyday use.
    #'PIL': [192, 224, 193, 225, 194, 226, 200, 232, 201, 233, 202, 234, 57348, 57349, 204, 236, 205, 237, 206, 238, 210, 242, 211, 243, 217, 249, 218, 250, 219, 251],
    #Yoruba
    # old orthography
    #'YBA': [195, 227, 7868, 7869, 296, 297, 213, 245, 360, 361],
    }

    SPECIAL_SORTS_BY_LANGUAGE = {}

    # This is the semi-official list of languages supported by the new text spec
    SUPPORT_NTS = ['AFK', 'SQI', 'EUQ', 'BRE', 'BOS', 'CAT', 'HRV', 'CSY',
            'DAN', 'NLD', 'ENG', 'NTO', 'ETI', 'FOS', 'FJI', 'FIN', 'FLE',
            'FRA', 'FRI', 'DEU', 'GRN', 'HAW', 'HUN', 'ISL', 'IND', 'IRI',
            'ITA', 'LAT', 'LVI', 'LTH', 'MLY', 'MTS', 'MRI', 'MOL', 'NOR',
            'PLK', 'PTG', 'PRO', 'RMS', 'ROM', 'ROY', 'ISM', 'LSM', 'NSM',
            'SSM', 'SMO', 'GAE', 'SKY', 'SLV', 'SRB', 'ESP', 'SWK', 'SVE',
            'PIL', 'TRK', 'WEL'],

    # This lists language support by codepage. THESE ARE NOT WELL-SOURCED
    # LISTS, and may conflict with language information given elsewhere.

    SUPPORT_BY_CODEPAGE = {
                           # Latin-1 Basic Latin
                           'ISO_8859_1': ['AFK', 'SQI', 'BRE', 'CAT', 'DAN',
                               'ENG', 'FOS', 'GAL', 'DEU', 'ISL', 'IRI', 'ITA',
                               'KUR', 'LAT', 'LTZ', 'NOR', 'OCI', 'PTO', 'RMS',
                               'GAE', 'ESP', 'SWK', 'SVE', 'EUQ', 'Waloon',
                               'Leonese'] + ['NLD', 'FLE', 'ESI', 'FRA',
                                   'FIN'],

                            # Latin-2
                            'ISO_8859_2': ['BOS', 'HRV', 'CSY', 'HUN', 'PLK', 'ROM', 'SRB', 'SKY', 'SLV', 'USB', 'LSB'],

                            # Latin-3 (TRK superseded with 8859-9)
                            'ISO_8859_3': ['TRK', 'MTS', 'NTO'],

                            # Latin-4, Northern European, superseded by ISO 8859-10
                            'ISO_8859_4': ['ETI', 'LVI', 'LTH', 'GRN'],
                            # Also Sami but I don't know which one(s)!?

                            # Latin-5 Turkish
                            'ISO_8859_9': ['TRK'],

                            # Latin-6 Nordic
                            'ISO_8859_10': ['ISK', 'FOS', 'NOR', 'DAN', 'SVE'] + ['Gutnish'],

                            # Latin-7 Baltic
                            'ISO_8859_13': ['LVI', 'LTH'],

                            # Latin 9
                            'ISO_8859_15': ['AFK', 'SQI', 'BRE', 'CAT', 'DAN', 'NLD', 'FLE', 'ENG', 'ESI', 'FOS', 'FIN', 'FRA', 'GAL', 'DEU', 'ISL', 'IRI', 'ITA', 'KUR', 'LAT', 'LTZ', 'MLY','NOR', 'OCI', 'PTO', 'RMS', 'GAE', 'ESP', 'SWK', 'SVE', 'PIL', 'EUQ', 'Waloon', 'Leonese'],
                            # Latin-10 Southeastern Europe
                            'ISO_8859_16': ['SQI', 'HRV', 'HUN', 'PLK', 'ROM', 'SLV', 'FRA', 'DEU', 'ITA', 'IRI'],

                            # Windows 1251 Cyrillic
                            'WINDOWS_1251': ['AZE', 'BEL', 'BOS', 'BGR', 'KAZ', 'MKD', 'MOL', 'MNG', 'RUS', 'SRB', 'TAT', 'UKR', 'UZB', 'Kyrgyz'],

                            # Windows 1254 Turkish
                            'WINDOWS_1253': ['AZE', 'KUR', 'TRK', 'UZB'],

                            # Windows 1257 Baltic
                            'WINDOWS_1257': ['ESI', 'LVI', 'LTH'],


                           }

#http://www.eki.ee/letter/

    """
    The following languages (some represented by romanization systems) do not
    require any additional characters to basic Latin: Armenian, Aymara,
    Belarusian, Creole, English, Fijian, Georgian, Greenlandic, Ikiribati,
    Kinyarwanda, Kirundi, Kosraean, Latin, Malay, Maldivian, Nauruan, Ndebele,
    Neomelanesian (Tok Pisin), Nukuoro, Palauan, Papiamento, Pedi, Ponapean,
    Quechua, Sesotho, siSwati, Somali, Soninke, Swahili, Thai, Toucouleur,
    Trukese, Tsonga, Tuvaluan, Ukrainian, Woleaian, Xhosa, Zulu.

    FRA
    Y and U with diaeresis are only used in certain geographical names and
    proper names plus their derivatives.  Only ISO 8859-15, Windows 1252 or Mac
    Roman contain the full character repertoire needed.

    Regional languages in France use C with cedilla more often.

    The French from France use very seldom accented capitals. Nevertheless they
    are still part of the typographic tradition, kept up by dictionaries and
    some book publishing houses. Quebec, for instance, and some other
    French-speaking places do insist on using accented uppercase.

    Accents are an essential element of French spelling; they are not optional,
    and their omission is always a mistake. Unfortunately, typewriter
    manufacturers found they could not fit the accents above the uppercase
    letters because of the standard heights of the type heads. As a result, a
    couple of generations of French typists grew up being _unable_ to type with
    accents over uppercase letters. This trait was further strengthened by
    incompatibilities in code pages (IBM 437 and 863, ISO 8859-1) and
    inconvenient computer keyboard layouts. Still, it is perverse to claim that
    the practices forced on French typists by a manufacturing errors should now
    be accepted as some sort of orthographic standard.

    Quality French book, newspaper and magazine typography has always continued
    to use both upper- and lowercase accented letters, as is necessary to the
    correct spelling of the French language. Spelling is never 'a matter of
    style'.

    The current everyday use always drops the accent marks on the word-initial
    capital and often but not always on all chraracters when the whole word is
    written in upper case.


    ITA
    J, K, W, X and Y are rarely used foreign letters.
    Diacritical marks distinguish homophones and indicate irregular stress.
    I and U with acute were moved from required to important as obsolete.
    Current use favours grave instead of acute.
    I with circumflex is added as important.
    The circumflex is used on an -i ending that was anciently written -ii (or
    -ji, -ij, -j, etc.) to distinguish homograph plurals and verb forms; e.g.
    princip (p. of principio = principle) from principi (p. of principe =
    price), gen (p. of genio = genius) from geni (p. of gene = gene), etc.
    A with acute is added as important.
    While it does not occur in ordinary running texts, geographical names on
    maps are often written only with acute accents.


    KUR
    No common alphabet has yet been agreed on.
    The required characters section above is taken from the unified Kurdish
    alphabet as proposed by Kurdish Academy of Language. This alphabet
    additionally has JH, LL, RR and SH as separate characters and fits into ISO
    8859-1 character set.
    Other Latin alphabets (apart from Cyrillic and Arabic) exist for Kurdish of
    which Kurmanji (containing E, I and U with circumflex, C and S with
    cedilla) is perceived as the most widespread. Kurmanjî characters are
    listed as important.
    The repertoire proposed by Kurdish Worldwide Resources site also includes
    letter AE.


    LVI
    Latvian diacritical marks are used to indicate
    macron - longitude of the vowel,
    cedilla (comma below) - palatalization of the consonant,
    caron - over c, s and z indicates the English sounds, ch, sh, and s (as in "leisure"), respectively.
    The government of the Latvian SSR decreed that the letters R WITH CEDILLA
    and O WITH MACRON, along with the LIGATURE CH be removed from written
    Latvian. Since then, there have existed two different Latvian writing
    systems. The Latvian community outside of Latvia continues to use the
    pre-occupation system, while in Latvia the changes made by the Soviet
    regime are still in use today. There really has been no major move to
    reform Latvian or to completely adopt either system. So, for the moment,
    these differences are likely to remain.

    NLD
    > One official unicode source says Dutch needs:
    The acute accent is used as a stress marker in Dutch. It's pretty much
    equivalent to writing a word in bold or italics. The accent can be placed
    on any vowel or vowel combination. A typical example is the numeral "een"
    (one), which is often written as "n" to distinguish it from the article
    "een" (a, an).

    >     (but not ; can you give an example using ?)

    A rare example is the biblical name "Kanan", which is pronounced with three
    syllables. Without the dieresis "naan" would stand for one syllable. We
    also used to write "napen" ('na' after + 'apen' = to ape, to mimick), but
    since the 1995 spelling reform, the dieresis is replaced by a hyphen:
    "na-apen".

    Letter Database comments:  is used in vacum.

    >

    Accents occur in French loanwords only as in , caf, crme, enqute, reu,
    matre. Those loanwords that have been fully adopted into the Dutch language
    lose accents on all vowels except 'e'. Hence "caf", "controle", "crpe",
    "pat", "ragout", "scne", "volire".

    The letter combination "ij" is a Dutch diphthong that sounds like "eille"
    in the French name "Mireille". In certain word endings "ij" is just a
    schwa. You could consider it a letter in its own right, because the
    uppercase version is not "Ij" but "IJ", e.g. "IJsland" (Iceland). But then
    again, all authoritative dictionaries alphabetize "ij" as simply i + j.

    Since "ij" is a vowel (a diphthong, to be precise), it can also carry a
    stress marker. If technically possible, an acute accent should be written
    over i as well as j, so the spelling rule says. But usually that isn't
    possible at all, so we write "j" instead.

    There's no such thing as a Flemish language. The northern half of Belgium
    is called Flanders and the people who live there are the Flemish. But their
    mother-tongue is 'Nederlands' (Dutch, Niederlndisch, nerlandais, etc.).
    Apart from a recognizable southern accent and some typical regionalisms in
    the vocabulary, it's the same language as the one spoken in the
    Netherlands. Spelling rules are identical in both countries and, as a rule,
    major Dutch dictionaries and grammar books are compiled and edited by a
    mixed staff of Dutch and Flemish linguists. Contrary to what many people
    believe, the Dutch language in Belgium is officially NOT called 'Flemish'.




    PTG

    acute accent opens the vowel
    circumflex accent closes the vowel
    tilde nasalizes the vowel
    grave accent is used when there is a contraction of preposition a with an
    article or pronoun: a + a = à (à casa, to the house).
    EGRAVE and OGRAVE are used in geographical names outside Europe and not
    part of the language proper. The now abandoned practice was to indicate
    underlying stress in words ending in -mente -- se`mente, u`ltimamente etc.
    K, W and Y are used only in foreign words.

    The diaeresis on U is now used only in Brazil.

    Feminine and masculine ordinal indicators (U+00AA and U+00BA) are used in
    Portuguese.



    SLV
    The 'important' characters are not part of the alphabet. Dictionaries
    additionally use ortographic signs for stress and pronunciation:
    A, E, I, O, U with grave
    A, E, I, O, U with acute
    E, O with circumflex

    SVE

    A WITH GRAVE is added to the original data. After all, AltaVista suggests
    that there exist more than 10 million pages in Swedish containing this
    character.
    Saami place-names use special orthography on older maps, conversion to the
    new Saami orthography is in progress. Swedish Saami Council has proposed
    that Ume Saami orthography be used additionally, adding D WITH STROKE and T
    WITH STROKE to the character repertoires of South, Lule and North Saami.

    TKM

    Y may alternately appear as Y with umlaut or Y with bar and corresponds to short i in cyrillic script.
    N with caron may alternately appear as N with tilde
    Other letters with alternate shapes are:
    $ - S with cedilla
    s - s with cedilla
    Z - Z with caron
    z - z with caron


    PIL
    Only n~ is required for everyday use.
    The accented vowels are used in dictionaries to indicate pronunciation, g with tilde is only present in older works.


    YBA
    Although the "dot below" diacritic is widely used, purists prefer a short
    vertical underbar (Unicode COMBINING VERTICAL LINE BELOW U+0329) - this
    resembles the IPA notation for a syllabic consonant, attached to the base
    of the letter (E, O or S).
    The seven Yoruba vowels (A, E, E underbar, I, O, O underbar, U) can be
    uttered in three different tones: high (acute accent); middle (no accent)
    and low (grave accent).
    The letters M and N, when written without diacritics, indicate nasalisation
    of the preceding vowel.
    M and N also occur as syllabics - in these circumstances, they take acute
    or grave tonal diacritics, like the vowels. Middle tone is also marked
    (with a macron) to differentiate it from the unmarked nasalising
    consonants.
    A tilde was used in older orthography to indicate a double vowel. This was
    tonally ambiguous, and has now been replaced by showing the paired vowels,
    each marked with the appropriate tones.
    However, where a double vowel has the tonal sequence high-low or low-high,
    it may optionally be replaced by a single vowel with a circumflex
    (high-low) or caron (low-high), eg. A acute + A grave = A circumflex; A
    grave + A acute = A caron.
    Tilde characters are "important" rather than "required", since they are
    only used to render the old orthography.

    Yoruba precomposed characters were rejected by the Unicode Technical Committee in 1996.


    ROY
    did not use #'ROY': [196, 228, 262, 263, 268, 269, 202, 234, 486, 487, 206, 238, 488, 489, 317, 318, 327, 328, 214, 246] # from omniglot, found nowhere else
    """

