
from fontTools.ttLib import TTFont
from tnTestFonts import getFontPath
from tnbits.compilers.f5.otlTools import findAlternateGlyphs

path = getFontPath("Arial Unicode.ttf")
font = TTFont(path)
glyphNames = font.getGlyphOrder()
cmap = font["cmap"].getcmap(3, 1).cmap
encodedGlyphs = set(cmap.values())


composites = {}
components = {}

glyfTable = font["glyf"]

for glyphName in glyphNames:
    glyph = glyfTable[glyphName]
    if glyph.isComposite():
        composites[glyphName] = [component.glyphName for component in glyph.components]
        for compo in composites[glyphName]:
            if compo in components:
                components[compo].append(glyphName)
            else:
                components[compo] = [glyphName]

glyphNames = set(glyphNames)
componentGlyphs = set(components)
unencodedGlyphs = glyphNames - encodedGlyphs
unencodedComponentGlyphs = componentGlyphs - encodedGlyphs
assert unencodedComponentGlyphs == unencodedGlyphs & componentGlyphs
unencodedNonComponentGlyphs = unencodedGlyphs - componentGlyphs
altGlyphs = findAlternateGlyphs(font, encodedGlyphs)

print("number of glyphs:", len(glyphNames))
print("number of encoded glyphs:", len(encodedGlyphs))
print("number of unencoded glyphs:", len(unencodedGlyphs))
print("number component glyphs:", len(componentGlyphs))
print("number of unencoded component glyphs:", len(unencodedComponentGlyphs))
print("number of unencoded non-component glyphs (must be GSUB):", len(unencodedNonComponentGlyphs))
print("number of alt glyphs through GSUB:", len(altGlyphs))
print("number of unencoded alt glyphs through GSUB:", len(altGlyphs & unencodedGlyphs))
print("number of unencoded non-component non-alt glyphs:", len(unencodedNonComponentGlyphs - altGlyphs))
if unencodedNonComponentGlyphs - altGlyphs:
    print("glyphs that don't seem referenced *anywhere*:")
    for glyphName in sorted(unencodedNonComponentGlyphs - altGlyphs):
        print("-", glyphName)
