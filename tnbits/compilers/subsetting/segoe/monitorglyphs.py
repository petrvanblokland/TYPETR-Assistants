# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    monitorglyphs.py
#
from tnbits.toolbox.transformer import TX
from tnbits.objects.truetypefont import TABLENAMES, TrueTypeFont

MONITOR_GLYPHS = (417, 768)

PATH_ROOT = '/FontDevelopment/_TTF/SegoeWorkSpace/'
PATH_TARGET = PATH_ROOT + 'Delivery#5-3/SegoeUI-Regular-Vietnamese.ttf'
PATH_MODEL = PATH_ROOT + 'Models/Vietnamese/SegoeUI-Regular-Vietnamese.ttf'
PATH_SOURCE = PATH_ROOT + 'Sources/SegoeUI-Regular-All.ttf'
PATHS = (PATH_MODEL, PATH_TARGET, PATH_SOURCE)

class MonitorFont(TrueTypeFont):
    READ_GSUB = True
    READ_GPOS = True
    EXTRACT_GLYPHS = True

class Monitor(object):

    def __init__(self, path):
        print('::::::Monitor', path)
        self.font = MonitorFont(path)
        self.unicodes = self.unicodesOf(self.font)

    def unicodesOf(self, font):
        unicodes = {}
        for glyphName in font.glyphs.keys():
            glyph = font[glyphName]
            if glyph.unicode:
                unicodes[glyph.unicode] = glyph
        return unicodes

    def unicode2Name(self, unicodeValue):
        if unicodeValue in self.unicodes:
            return self.unicodes[unicodeValue].name
        return unicodeValue

    def testGPOS(self, glyphNames):
        t = []
        names = []
        for glyphName in glyphNames:
            names.append(self.unicode2Name(glyphName))
        t.append('Testing glyphs %s' % ','.join(glyphName))
        for usage in self.font.gpos.glyphUsage(glyphNames):
            t.append(usage)
        return t

    def checkLookups(self, table, glyphNames):
        lookups = table.getLookupsOfGlyphs(glyphNames)
        print('===== Lookups:', len(lookups))
        for index, lookup in enumerate(lookups):
            print('XXXXX', index, lookup, lookup.getGlyphNames())

for path in PATHS:
    monitor = Monitor(path)
    for usage in monitor.testGPOS(MONITOR_GLYPHS):
        print(usage)
