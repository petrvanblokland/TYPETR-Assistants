from __future__ import print_function
import assistantLib.glyphNameFormatter
from assistantLib.glyphNameFormatter.unicodeRangeNames import getRangeByName, getAllRangeNames, getSupportedRangeNames
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
    lines.append("# %s %05X - %05X" % (rangeName, start, end))
    hasSupport = False
    for uniNumber in range(start, end+1):
        glyphName = glyphNameFormatter.GlyphName(uniNumber)
        if glyphName.hasName():
            lines.append("%04X\t%s\t%s" % (uniNumber, glyphName.getName(extension=True), glyphName.uniName))
    dirForNames = "../names/ranges/"
    if not os.path.exists(dirForNames):
        os.makedirs(dirForNames)
    rangeForFileName = "%05X-%05X %s" % (start, end, rangeName.replace(" ", "_").lower())
    path = "../names/ranges/%s.txt" % rangeForFileName
    f = open(path, 'w')
    f.write("\n".join(lines))
    f.close()

if __name__ == "__main__":
    for rangeName in getSupportedRangeNames():
        generateRange(rangeName)
