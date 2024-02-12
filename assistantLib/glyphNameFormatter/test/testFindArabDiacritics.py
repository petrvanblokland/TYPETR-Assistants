#coding:utf8


#
#
#   make a list of arabic marks

inevitableExceptions = [
    1552,
    1553,
    1554,
    1555,
    1758,
    1772,
]

biditypes = {}
from assistantLib.glyphNameFormatter import GlyphName
for uniNumber in range(1, 0xffff):
    g = GlyphName(uniNumber)
    if not g.bidiType in biditypes:
        biditypes[g.bidiType] = []
    biditypes[g.bidiType].append(uniNumber)

candidates = []
for u in biditypes["NSM"]:
    g = GlyphName(u)
    if g.uniRangeName.find("Arabic") != -1 and g.uniNumber not in inevitableExceptions:
        candidates.append(u)
        print(g.uniNumber, g.uniName)
print(candidates)
