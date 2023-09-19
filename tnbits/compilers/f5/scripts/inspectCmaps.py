
import os
from pprint import pprint
from fontTools.ttLib import TTFont
from tnTestFonts import getAllFontPaths
from tnbits.compilers.f5 import unicodeRanges


def reportRanges(ranges, unicodeRangeBits):
    def getKey(item):
        if item[0] is None:
            return None
        else:
            return unicodeRanges.getUnicodeRangeByName(item[0])
    items = ranges.items()
    items.sort(key=getKey)
    keys = [k for k, v in items]

    usedBits = set()
    for key in keys:
        count, size = ranges[key]
        if key is None:
            print("*** Characters outside of ranges: %s" % count)
        else:
            bitNum = unicodeRanges.getUnicodeRangeByName(key)[0]
            usedBits.add(bitNum)
            percent = 100 * count / float(size)
            print("%5.1f %%  %3s  %s  %s  (%s of %s)" % (percent, bitNum, [".", "*"][bitNum in unicodeRangeBits], key, count, size))

    unusedBits = unicodeRangeBits - usedBits
    if unusedBits:
        print
        print("unicodeRangeBit set, but no characters found within the range:")
        for bitNum in sorted(unusedBits):
            names = [item[0] for item in unicodeRanges.getUnicodeRangeByBit(bitNum)]
            print("%3d  %s" % (bitNum, ", ".join(names)))


def inspectCmap(path):
    print("=" * 80)
    print(path)
    print
    f = TTFont(path)
    print("unitsPerEm:", f["head"].unitsPerEm)
    print

    os2Table = f["OS/2"]
    unicodeRangeBits = unicodeRanges.unpackRangeBits(os2Table.ulUnicodeRange1, os2Table.ulUnicodeRange2, os2Table.ulUnicodeRange3, os2Table.ulUnicodeRange4)
    print("ulUnicodeRange1-4:  %08X  %08X  %08X  %08X" % (os2Table.ulUnicodeRange1, os2Table.ulUnicodeRange2, os2Table.ulUnicodeRange3, os2Table.ulUnicodeRange4))
    print("bits set:", str(sorted(unicodeRangeBits))[1:-1])
    print

    cmapTable = f["cmap"]
    cmap3_1 = cmapTable.getcmap(3, 1)
    #if cmap3_1 is None:
    #    print("***** no 3,1 cmap")
    cmap0_3 = cmapTable.getcmap(0, 3)
    cmap3_10 = cmapTable.getcmap(3, 10)
    if cmap3_1 is not None and cmap3_10 is not None:
        # is 3_10 a superset of 3_1?
        assert set(cmap3_1.cmap) - set(cmap3_10.cmap) == set(), "3,10 cmap is expected to be superset of 3,1"
    if cmap3_10 is not None:
        preferredCmap = cmap3_10
    elif cmap3_1 is not None:
        preferredCmap = cmap3_1
    elif cmap0_3 is not None:
        preferredCmap = cmap0_3
    else:
        print("***** no usable or supported cmap found")
        preferredCmap = None

    print("cmaps:")
    for subTable in cmapTable.tables:
        print(subTable.platformID, subTable.platEncID, subTable.language, len(subTable.cmap))
    if cmap0_3 is not None and cmap3_1 is not None:
        print("(both 3,1 and 0,3 are available, they are %sequal.)" % ["not ", ""][cmap0_3.cmap == cmap3_1.cmap])

    print
    print("number of glyphs:", len(f.getGlyphNames()))
    if preferredCmap is not None:
        print("number of characters:", len(preferredCmap.cmap))
        print
        print("unicode ranges from cmap %s,%s:" % (preferredCmap.platformID, preferredCmap.platEncID))
        reportRanges(unicodeRanges.countCoverageByRangeName(preferredCmap.cmap.keys()), unicodeRangeBits)
    print


if __name__ == "__main__":
    import sys, os
    if sys.argv[1:]:
        paths = sys.argv[1:]
    else:
        from tnTestFonts import getAllFontPaths
        paths = getAllFontPaths("ttf", "otf")
    for path in paths:
        inspectCmap(path)
