from __future__ import division

__all__ = ["calcCodePages", "calcCodePageRangesFromBits", "calcCodePageRanges",
        "codePagesByID", "codePagesByBit", "codePagesNames"]


_codePages = """\
0        cp1252     Latin 1
1        cp1250     Latin 2: Eastern Europe
2        cp1251     Cyrillic
3        cp1253     Greek
4        cp1254     Turkish
5        cp1255     Hebrew
6        cp1256     Arabic
7        cp1257     Windows Baltic
8        cp1258     Vietnamese
9-15     .          Reserved for Alternate ANSI
16       cp874      Thai
17       cp932      JIS/Japan
18       cp936      Chinese: Simplified chars--PRC and Singapore
19       cp949      Korean Wansung
20       cp950      Chinese: Traditional chars--Taiwan and Hong Kong
21       cp1361     Korean Johab
22-28    .          Reserved for Alternate ANSI & OEM
29       macroman   Macintosh Character Set (US Roman)
30       .          OEM Character Set
31       .          Symbol Character Set
32-47    .          Reserved for OEM
48       cp869      IBM Greek
49       cp866      MS-DOS Russian
50       cp865      MS-DOS Nordic
51       cp864      Arabic
52       cp863      MS-DOS Canadian French
53       cp862      Hebrew
54       cp861      MS-DOS Icelandic
55       cp860      MS-DOS Portuguese
56       cp857      IBM Turkish
57       cp855      IBM Cyrillic; primarily Russian
58       cp852      Latin 2
59       cp775      MS-DOS Baltic
60       cp737      Greek; former 437 G
61       cp708      Arabic; ASMO 708
62       cp850      WE/Latin 1
63       cp437      US
"""

def _parseCodePages():
    codePagesByID = {}
    codePagesByBit = {}
    codePagesNames = {}
    for line in _codePages.splitlines():
        bit, cp, name = line.split(None, 2)
        if "-" not in bit:
            bit = int(bit)
        codePagesByID[cp] = bit
        codePagesNames[cp] = name
        codePagesByBit[bit] = cp
    return codePagesByID, codePagesByBit, codePagesNames

codePagesByID, codePagesByBit, codePagesNames = _parseCodePages()


def calcCodePages(chars):
    asciiBasedCharset = "".join([chr(i) for i in range(32, 256)])

    supportedCodePages = set()
    for cp in codePagesByID:
        if cp == ".":
            continue
        try:
            unicodeCharset = asciiBasedCharset.decode(cp, "ignore")
        except:
            pass
        else:
            unicodeCharset = set(ord(c) for c in unicodeCharset)
            fontChars = chars & unicodeCharset
            coverage = len(fontChars) / len(unicodeCharset)
            if coverage > 0.98:
                bit = codePagesByID[cp]
                supportedCodePages.add(bit)

    return supportedCodePages


def calcCodePageRangesFromBits(bits):
    ulCodePageRange1 = 0
    ulCodePageRange2 = 0
    for bit in bits:
        if bit < 32:
            ulCodePageRange1 |= 1 << (bit)
        else:
            ulCodePageRange2 |= 1 << (bit - 32)
    return ulCodePageRange1, ulCodePageRange2


def calcCodePageRanges(chars):
    return calcCodePageRangesFromBits(calcCodePages(chars))


if __name__ == "__main__":
    import sys
    from fontTools.misc.textTools import num2binary
    from tnbits.compilers.f5.ttfTools import getBestCmap
    from fontTools.ttLib import TTFont

    for p in sys.argv[1:]:
        f = TTFont(p, lazy=True)
        cmap = getBestCmap(f)
        supportedCodePages = calcCodePages(set(cmap))
        for bit in sorted(supportedCodePages):
            cp = codePagesByBit[bit]
            name = codePagesNames[cp]
            print("%2s  %8s  %s" % (bit, cp, name))

        ulCodePageRange1, ulCodePageRange2 = calcCodePageRanges(set(cmap))
        print("ulCodePageRange1:", num2binary(ulCodePageRange1))
        print("ulCodePageRange2:", num2binary(ulCodePageRange2))
