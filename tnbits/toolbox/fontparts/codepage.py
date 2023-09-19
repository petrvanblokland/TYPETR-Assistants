# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
from __future__ import division, print_function
import unicodedata
from tnbits.constants import Constants as C
from tnbits.toolbox.transformer import TX
from tnbits.toolbox.fontparts.unicode import UnicodeTX
from tnbits.base.future import chr

class CodepageTX:
    """
    `CodepageTX` provides tools for finding and processing codepages.
    """

    @classmethod
    def codepagesForUnicode(cls, u):
        """
        `codepagesForUnicode` returns list of codepages that contain a unicode value.
        """
        ids = []
        for id, codepage in C.CODEPAGES.items():
            if u in codepage:
                ids.append(id)
        return ids

    @classmethod
    def nameForBit(cls, index):
        """
        `nameForBit` returns a codepage name from a given OS/2 ulCodePageRange bit.
        """
        findCodepage = cls.codePageForBit(index)
        for id, codepage in C.CODEPAGES.items():
            if codepage == findCodepage:
                return id

    @classmethod
    def codePageForBit(cls, index):
        """
        `codePageForBit` returns a codepage from a given OS/2 ulCodePageRange bit.
        """
        for id, bit in C.FONTINFO_OS2_CODEPAGE_RANGES.items():
            if bit == index:
                return C.CODEPAGES.get(id)

    @classmethod
    def codePageForName(cls, name):
        """
        `codePageForName` returns a codepage from a given name.
        """
        return C.CODEPAGES.get(name)

    @classmethod
    def getSupport(cls, codepage, f, omitControls=True):
        """
        `getSupport` splits the glyphs for a font into those included in a _codepage_ and those that are not.
        """
        if codepage:
            contains = []
            doesNotContain = []
            for char in codepage:
                if omitControls and unicodedata.category(chr(char)) == 'Cc':
                    pass
                elif char in UnicodeTX.getUnicodeData(f):
                    contains.append(char)
                else:
                    doesNotContain.append(char)
            return contains, doesNotContain
        return [], []

    @classmethod
    def getOS2CodepageRanges(cls, f, minPresence=1, minProportion=.9, omitControls=True, DEBUG=False):
        """

        `getOS2CodepageRanges`: Given a font _f_, return a tuple of bits for ranges that are supported. By default, it only takes one participating glyph to be admitted to the tuple. This can be changed by _minPresence_, which specifies a minimum number of glyphs, and/or _minProportion_, which specifies that participation much reach a proportion between 0 and 1.

        """
        supportedCodepages = []
        bits = list(C.FONTINFO_OS2_CODEPAGE_RANGES.values())
        bits.sort()
        for bit in bits:
            codePage = cls.codePageForBit(bit)
            if codePage:
                if DEBUG:
                    print(bit, cls.nameForBit(bit))
                newCodepage = []
                if codePage:
                    if omitControls:
                        for u in codePage:
                            if unicodedata.category(chr(u)) != 'Cc':
                                newCodepage.append(u)
                        if DEBUG:
                            print('\tRemoved', len(codePage) - len(newCodepage), 'controls, new total:', len(newCodepage))
                        codePage = newCodepage
                    contains, doesNotContain = cls.getSupport(codePage, f)
                    if DEBUG:
                        print('\tCoverage:', len(contains) / float(len(codePage)))
                        print('\tMissing', len(doesNotContain), 'of', len(codePage),)
                        if len(doesNotContain) < 200:
                            missing = ' '.join([chr(u) for u in doesNotContain])
                            print(missing)
                        else:
                            missing = ' '.join([chr(u) for u in doesNotContain[:200]])
                            print(missing+'.......')
                    if contains:
                        go = True
                        if minPresence and len(contains) < minPresence:
                            go = False
                            if DEBUG: print('\t', 'Fails minimum presence', len(contains), minPresence)
                        if minProportion and len(contains) < len(codePage) * minProportion:
                            go = False
                            if DEBUG: print('\t', 'Fails minimum proportion', len(contains), 'of required', len(codePage) * minProportion)
                        if go:
                            if DEBUG: print('\t', 'Passes')
                            if bit not in supportedCodepages:
                                supportedCodepages.append(bit)
            supportedCodepages.sort()
        return tuple(supportedCodepages)

    @classmethod
    def getOS2CodepageRangesForTTX(cls, os2CodepageRanges=()):
        """
        `getOS2CodepageRangesForTTX`: Given a font _f_, return two binary
        outputs for os_2 ulCodepageRange1 and ulCodepageRange2 that can be
        pasted directly into a TTX file."""
        from ufo2fdk.fontInfoData import intListToNum
        supportedCodepages = os2CodepageRanges
        ulCodePageRange1 = intListToNum(supportedCodepages, 0, 32)
        ulCodePageRange2 = intListToNum(supportedCodepages, 32, 32)
        output1 = TX.formatBinaryForTTX(bin(ulCodePageRange1))
        output2 = TX.formatBinaryForTTX(bin(ulCodePageRange2))
        return output1, output2

if __name__ == "__main__":
    from mojo.roboFont import CurrentFont
    print(CurrentFont())
    print(CodepageTX.getOS2CodepageRanges(CurrentFont(), DEBUG=True, minProportion=.96))
