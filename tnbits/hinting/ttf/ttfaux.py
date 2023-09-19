
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    ttfaux.py
#    Was aux.py before, but there is an issue with "aux" files on windows.
#


from tnbits.toolbox.storage.adict import ADict
from tnbits.hinting.ttf.objects.vector import Vector

class Aux(object):

    def getInitializedMaxP(self):
        """
        Put the TrueType maxp values in a dictionary.
        """
        # TODO: smarter attribute copying;
        maxp = {}

        # No 'version' attribute?
        attributes = ['numGlyphs', 'maxPoints', 'maxContours', 'maxCompositePoints',
        'maxCompositeContours', 'maxZones', 'maxTwilightPoints', 'maxStorage',
        'maxFunctionDefs', 'maxInstructionDefs', 'maxStackElements',
        'maxSizeOfInstructions', 'maxComponentElements', 'maxComponentDepth']

        if 'maxp' in self.ttf:
            for attr in attributes:
                if hasattr(self.ttf['maxp'], attr):
                    maxp[attr] = getattr(self.ttf['maxp'], attr)
                else:
                    print('No attribute %s.' % attr)

        return maxp

    def getInitializedMetrics(self, ppem):
        """
        Gets metrics values from TrueType.
        """
        # Amount of units in the em for a point coordinate, e.g. 512
        scale = self.em / ppem # Scale of point coordinates to 1 pixel in 64 fixed value

        # FIXME: should be derived from ttf somehow.
        rotated = False
        stretched = False
        resolution = 72 # TODO: pass as arguments, twice as large for retina screens?

        return ADict(dict(scale=Vector(scale, scale), ppem=ppem, em=self.em, \
                        rotated=rotated, stretched=stretched,\
                        resolution=resolution, compensations=[1,1,1,1,1,1,1,1,1,1,1,1]))

    def getCVTAsList(self):
        """
        Makes a copy of the CVT table, to prevent signed short integer errors when
        writing values that are too large.
        """
        cvt = []

        if 'cvt ' in self.ttf:
            for v in self.ttf['cvt ']:
                cvt.append(v)

        return cvt

    # Unicode.

    def addToRange(self, pair):
        """
        Gets a code, name pair.
        """
        code, _ = pair

        for key, value in self.C.UNICODE_RANGES.items():
            if code >= key[0] and code <= key[1]:
                if not value in self.characterMap:
                    self.characterMap[value] = []
                self.characterMap[value].append(pair)
                continue

    def getUnicodeRangeNames(self):
        """
        Returns all unicode ranges names from character map.
        """
        return sorted(self.characterMap.keys())

    def getGlyphNames(self, unicodeRangeName):
        """
        Returns all glyph names for a certain ``unicodeRangeName``.
        """
        pairs = self.characterMap[unicodeRangeName]
        return sorted(zip(*pairs)[1])

    def getGlyphCode(self, unicodeRangeName, glyphName):
        """
        Returns the code for a certain ``glyphName`` in the Unicode range
        with ``unicodeRangeName``.
        """
        pairs = self.characterMap[unicodeRangeName]
        codes, names = zip(*pairs)
        i = names.index(glyphName)
        return codes[i]

