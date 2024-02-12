from __future__ import print_function
from assistantLib.glyphNameFormatter.unicodeRangeNames import getRangeName, getAllRangeNames, rangeNameToModuleName

from assistantLib.glyphNameFormatter.data import name2unicode_AGD
import importlib


#   find which unicode ranges are needed to cover the AGD names
#   so we can prioritize the support

def testAGDCoverage():
    wantRanges = []
    glyphCount = {}
    for name in name2unicode_AGD:
        uniNumber = name2unicode_AGD[name]
        thisRange = getRangeName(uniNumber)
        if thisRange == "Private Use Area":
            continue
        if thisRange not in glyphCount:
            glyphCount[thisRange] = 0
        glyphCount[thisRange] += 1
        if thisRange is None:
            continue
        if thisRange not in wantRanges:
            wantRanges.append(thisRange)
    supported = []
    notSupported = []
    notNeeded = []
    for name in wantRanges:
        if name == "Private Use Area":
            continue
        moduleName = rangeNameToModuleName(name)
        try:
            module = importlib.import_module('glyphNameFormatter.rangeProcessors.%s' % moduleName)
            supported.append(name)
        except ImportError:
            notSupported.append(name)
    for name in getAllRangeNames():
        if name not in supported and name not in notSupported:
            notNeeded.append(name)
    supported.sort()
    notSupported.sort()
    notNeeded.sort()
    supportedTotal = 0
    notSupportedTotal = 0
    print("Available range processors for AGD:")
    for n in supported:
        print("\t%8d\t%s" % (glyphCount[n], n))
        supportedTotal += glyphCount[n]
    print("\nMissing range processors for AGD:")
    for n in notSupported:
        print("\t%8d\t%s" % (glyphCount[n], n))
        notSupportedTotal += glyphCount[n]
    print("Supported total", supportedTotal+notSupportedTotal)
    print("AGD supported total", supportedTotal)
    print("AGD total", len(name2unicode_AGD))
    print("Coverage complete: %3.1f%%" % (100.0*supportedTotal/len(name2unicode_AGD)))
    
    print("\nRange processors not needed for AGD:")
    for n in notNeeded:
       print("\t", n)


if __name__ == "__main__":
    testAGDCoverage()
