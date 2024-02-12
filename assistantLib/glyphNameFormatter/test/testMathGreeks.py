

from assistantLib.glyphNameFormatter import GlyphName
from assistantLib.glyphNameFormatter.unicodeRangeNames import *

greekSymbols = []
pi = []
theta = []
for name in getAllRangeNames():
    if name in ['Ancient Greek Musical Notation', 'Mathematical Alphanumeric Symbols']: continue
    a, b = getRangeByName(name)
    for uniNumber in range(a,b):
        g = GlyphName(uniNumber)
        if g.uniName is None: continue
        if "GREEK" in g.uniName and g.isMath:
            greekSymbols.append(g)

        if "GREEK" in g.uniName and ("LETTER PI" in g.uniName or "PI SYMBOL" in g.uniName):
            pi.append(g)

        if "GREEK" in g.uniName and ("LETTER THETA" in g.uniName or "THETA SYMBOL" in g.uniName):
            theta.append(g)


print("\n\ngreek and math")
for g in greekSymbols:
    print(g, g.uniRangeName, g.isMath)

print("\n\ntheta")
for g in theta:
    print(g, g.uniRangeName, g.isMath)

print("\n\npi")
for g in pi:
    print(g, g.uniRangeName, g.isMath)
