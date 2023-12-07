from __future__ import print_function
import glyphNameFormatter
from glyphNameFormatter.unicodeRangeNames import getRangeByName, getAllRangeNames
import os

skipped = {}

def generateRange(rangeName):
    # generate all the names in the range
    lines = []
    r = getRangeByName(rangeName)
    if r is None:
        print("unknown range name", rangeName)
        return
    start, end = r
    lines.append("# %s %04X - %04X" % (rangeName, start, end))
    for uniNumber in range(start, end+1):
        glyphName = glyphNameFormatter.GlyphName(uniNumber)
        if glyphName.hasName():
            lines.append("%04X\t%s\t%s" % (uniNumber, glyphName.getName(extension=True), glyphName.uniName))
    dirForNames = "../names/ranges/"
    if not os.path.exists(dirForNames):
        os.makedirs(dirForNames)
    path = "../names/ranges/names_%s.txt" % rangeName.replace(" ", "_").lower()
    f = open(path, 'w')
    f.write("\n".join(lines))
    f.close()

if __name__ == "__main__":
    for rangeName in getAllRangeNames():
        generateRange(rangeName)
