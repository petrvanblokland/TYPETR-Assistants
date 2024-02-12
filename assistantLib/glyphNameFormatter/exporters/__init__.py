# -*- coding: UTF-8 -*-
from __future__ import print_function

from assistantLib.glyphNameFormatter.unicodeRangeNames import getRangeByName
from assistantLib.glyphNameFormatter import GlyphName

from assistantLib.glyphNameFormatter.data import unicode2name_AGD, unicode2name_GLYPHS


def _rangeNameToRange(rangeName):
    if isinstance(rangeName, tuple):
        return rangeName
    start, end = getRangeByName(rangeName)
    return start, end+1


def printRange(rangeName, toFile=None):
    out = [
        "{0:<50s}{1:<30}{2:<30}{3}{4:<5}{5}".format("Generated Name", "AGD", "Glyphs", "uni    ", " ", "uni name"),
        ""

    ]
    for u in range(*_rangeNameToRange(rangeName)):
        g = GlyphName(uniNumber=u)
        name = g.getName()
        if name is None:
            continue
        AGDName = unicode2name_AGD.get(g.uniNumber)
        if AGDName is None:
            AGDName = "-"
        elif AGDName == name:
            AGDName = u"👍"
        GLYPHSName = unicode2name_GLYPHS.get(g.uniNumber)
        if GLYPHSName is None:
            GLYPHSName = "-"
        elif GLYPHSName == name:
            GLYPHSName = ""
        txt = name.ljust(50)
        txt += AGDName.ljust(30)
        txt += GLYPHSName.ljust(30)
        txt += "%04X   " % g.uniNumber
        txt += g.uniLetter.ljust(5)
        txt += g.uniName
        out.append(txt)
    out = "\n".join(out)
    if toFile:
        toFile.write(out)
    else:
        print(out)
    testDoubles(rangeName, toFile)
    testGLIFFileName(rangeName, toFile)


def testDoubles(rangeName, toFile=None):
    """
    test if there are doubles
    """
    names = set()
    doubles = set()
    r = _rangeNameToRange(rangeName)
    for u in range(*r):
        g = GlyphName(uniNumber=u)
        name = g.getName()
        if name is None:
            # ignore
            continue
        if name in names:
            doubles.add(name)
        else:
            names.add(name)
    if doubles:
        rangeText = "%04X - %04X" % (r[0], r[1])
        txt = "\n\ndouble names for range %s:\n\t%s" % (rangeText, "\n\t".join(sorted(doubles)))
        if toFile:
            toFile.write(txt)
        else:
            print(txt)


def testGLIFFileName(rangeName, toFile=None):
    """
    test on glif file name
    """
    # support both UFO2 as UFO3
    try:
        # UFO3 ufoLib
        from fontTools.ufoLib.filenames import userNameToFileName

        def nameToFileName(name):
            return userNameToFileName(name)
    except:
        # UFO2 robofab
        from robofab.tools.glyphNameSchemes import glyphNameToShortFileName

        def nameToFileName(name):
            return glyphNameToShortFileName(name, None)
    existing = set()
    doubles = set()
    r = _rangeNameToRange(rangeName)
    for u in range(*r):
        g = GlyphName(uniNumber=u)
        name = g.getName()
        if name is None:
            # ignore
            continue
        glifFileName = nameToFileName(name)
        if glifFileName in existing:
            doubles.add(glifFileName)
        else:
            existing.add(glifFileName)
    if doubles:
        rangeText = "%04X - %04X" % (r[0], r[1])
        txt = "\n\ndouble glif file names for range %s:\n\t%s" % (rangeText, "\n\t".join(sorted(doubles)))

        if toFile:
            toFile.write(txt)
        else:
            print(txt)


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.unicodeRangeNames import getAllRangeNames

    # time test
    import time
    t = time.time()
    for rangeName in getAllRangeNames():
        r = _rangeNameToRange(rangeName)
        for u in range(*r):
            g = GlyphName(uniNumber=u)
            name = g.getName()
    print(time.time() - t)
