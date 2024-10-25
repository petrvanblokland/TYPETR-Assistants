# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    Latin_M_set.py
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
#    Latin S + Latin M
#    AÁĂǍÂÄẠÀĀĄÅÃÆBḄƁCĆČÇĈĊDÐĎĐḌƊEÉĔĚÊËĖẸÈĒĘƐƎẼFGĞĜĢĠḠǦHĦĤḦḤIÍĬǏÎÏİỊÌĪĮƗĨJĴKĶƘLĹĽĻŁMNŃŇŅṄṆƝÑŊ
#    OÓŎǑÔÖỌÒŐŌƆØÕŒPṖÞQRŔŘŖSŚŠŞŜȘṢẞƏTŤŢȚUÚŬǓÛÜỤÙŰŪŲŮŨVɅWẂŴẄẀXẌYÝŶŸỲƳỸȲZŹŽŻẒaáăǎâäạàāąåãæbḅɓcć
#    čçĉċdðďđḍɗeéĕěêëėẹèēęɛẽǝəfgğĝģġḡǧhħĥḧḥiıíĭǐîïịìīįɨĩjȷĵkķƙlĺľļłmnńňņṅṇɲñŋoóŏǒôöọòőōɔøõœpṗ
#    þqrŕřŗsśšşŝșṣßtťţțuúŭǔûüụùűūųůũvʌwẃŵẅẁxẍyýŷÿỳƴỹȳzźžżẓ₵₡₲₺₼₦₹ ̈ ̇ ̀ ́ ̋ ̂ ̌ ̆ ̊ ̃ ̄ ̒ ̣ ̦ ̧ ̨ʼʻ ̵
#    ẮẶẰẲẴẤẬẦẨẪẢǢḎẾỆỀỂỄẺḪḨỈḲḴḶḸḺṀṂṈỐỘỒỔỖỎƠỚỢỜỞỠṘṚṜṞṬṮǗǙǛǕỦƯỨỰỪỬỮẈẎỴỶẔ
#    ắặằẳẵấậầẩẫảǣḏếệềểễẻḫḩẖỉḳḵḷḹḻṁṃṉốộồổỗỏơớợờởỡṙṛṝṟṭṯǘǚǜǖủưứựừửữẉẏỵỷẕ₫
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
from assistantLib.assistantModules.glyphsets.Latin_S_set import LATIN_S_SET

LATIN_M_SET_NAME = 'Latin M'

# The "c" attribtes are redundant, if the @uni or @hex atre defined, but they offer easy searching in the source by char.

LATIN_M_SET = GDS = deepcopy(LATIN_S_SET)

# Latin M unicodes
# Make this into these codes:
# GDS['aacute.alt'] = GD(name='aacute.alt', base='a.alt', accents=('acutecmb'))
#
# 0x01a0 0x01a1 0x01af 0x01b0 0x01d5 0x01d6 0x01d7 0x01d8 0x01d9 0x01da 0x01db 0x01dc 0x01e2 0x01e3 
# 0x02be 0x02bf 0x0309 0x031b 0x032e 0x0331 0x1e0e 0x1e0f 0x1e28 0x1e29 0x1e2a 0x1e2b 0x1e32 0x1e33 
# 0x1e34 0x1e35 0x1e36 0x1e37 0x1e38 0x1e39 0x1e3a 0x1e3b 0x1e40 0x1e41 0x1e42 0x1e43 0x1e48 0x1e49 
# 0x1e58 0x1e59 0x1e5a 0x1e5b 0x1e5c 0x1e5d 0x1e5e 0x1e5f 0x1e6c 0x1e6d 0x1e6e 0x1e6f 0x1e88 0x1e89 
# 0x1e8e 0x1e8f 0x1e94 0x1e95 0x1e96 0x1ea2 0x1ea3 0x1ea4 0x1ea5 0x1ea6 0x1ea7 0x1ea8 0x1ea9 0x1eaa 
# 0x1eab 0x1eac 0x1ead 0x1eae 0x1eaf 0x1eb0 0x1eb1 0x1eb2 0x1eb3 0x1eb4 0x1eb5 0x1eb6 0x1eb7 0x1eba 
# 0x1ebb 0x1ebe 0x1ebf 0x1ec0 0x1ec1 0x1ec2 0x1ec3 0x1ec4 0x1ec5 0x1ec6 0x1ec7 0x1ec8 0x1ec9 0x1ece 
# 0x1ecf 0x1ed0 0x1ed1 0x1ed2 0x1ed3 0x1ed4 0x1ed5 0x1ed6 0x1ed7 0x1ed8 0x1ed9 0x1eda 0x1edb 0x1edc 
# 0x1edd 0x1ede 0x1edf 0x1ee0 0x1ee1 0x1ee2 0x1ee3 0x1ee6 0x1ee7 0x1ee8 0x1ee9 0x1eea 0x1eeb 0x1eec 
# 0x1eed 0x1eee 0x1eef 0x1ef0 0x1ef1 0x1ef4 0x1ef5 0x1ef6 0x1ef7 0x20ab

