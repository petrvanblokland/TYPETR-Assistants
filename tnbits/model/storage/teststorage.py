# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     teststorage.py
#

import json
from tnTestFonts import getFontPath
from tnbits.model.storage.basestorage import getStorage

def testOneStorage(storage):
    glyphNames = storage.getGlyphNames()
    print(len(glyphNames))
    print(glyphNames[:20])
    if "aring" in glyphNames:
        print(json.dumps(storage.getGlyphPack("aring"), indent=2, sort_keys=True))
    if "a" in glyphNames:
        print(json.dumps(storage.getGlyphPack("a"), indent=2, sort_keys=True))
    print(json.dumps(storage.getGlyphPack(glyphNames[3]), indent=2, sort_keys=True))  # glyph index 3)
    print(storage.getIdentifiersPack())
    print(storage.getDimensionsPack())
    print(storage.getBoundariesPack())

def testStorage():
    for fontName in ["CusterRE-RegularS2.ttf", "Condor-Regular.ufo", "ProW6.otf"]:
        path = getFontPath(fontName)
        storage = getStorage(path) # Note that storage can be None, in case of a new untitled unsaved style.
        testOneStorage(storage)

if __name__ == "__main__":
    testStorage()
