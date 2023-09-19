from fontTools.ttLib import TTFont
from tnTestFonts import getFontPath
from tnbits.compilers.f5 import ttfTools, featureBuilder


def swashFilter(gn, glyphID):
    return gn + ".swash"


font1 = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
font2 = TTFont(getFontPath("SaunaPro-RegularItalicSwash.ttf"))

# Force font2 to have alternate glyph names
ttfTools.patchGlyphNames(font2, swashFilter)

# Do the actual merging of the fonts
ttfTools.mergeFonts(font1, font2)

# Create a mapping from "regular" to "swash" glyphs
swashMapping = {}
glyphNames1 = set(font1.getGlyphOrder())
glyphNames2 = set(font2.getGlyphOrder())
for glyphName1 in glyphNames1:
    glyphName2 = swashFilter(glyphName1, None)
    if glyphName2 in glyphNames2:
        swashMapping[glyphName1] = glyphName2


featureBuilder.addSingleSubstFeature(font1["GSUB"], swashMapping, "swsh")

ttfTools.stripInstructions(font1)

# XXX set/rename name table entries

font1.save("TestSaunaMerge.ttf")
