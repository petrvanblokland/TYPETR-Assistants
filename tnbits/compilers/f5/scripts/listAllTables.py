"""Traverse all the .ttf and .otf fonts in the tnTestFonts package, and report which tables
are used by which fonts. This way we can easily find a font that contains a specific table.
"""


import os
from pprint import pprint
from tnTestFonts import getAllFontPaths
from fontTools.ttLib import TTFont


allTables = {}

for p in getAllFontPaths("ttf", "otf"):
    fn = os.path.basename(p)

    f = TTFont(p)

    for table in f.keys():
        if table == "GlyphOrder":
            continue
        if table not in allTables:
            allTables[table] = []
        allTables[table].append(fn)


pprint(allTables)
