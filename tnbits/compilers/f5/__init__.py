"""The f5 package is a set of tools to manipulate, subset and combine OTF and TTF files.


The main submodules and their main entry points are:

mergeFonts:
    - f5MergeFonts() Merge a set of fonts into a new font.

ttfTools:
    - subsetFont() Delete specified glyphs from the font.
    - mergeFonts() Merge one font into another.
    - scaleFont() Scale all design space values to a new UPM value.
    - convertFontToTTF() Convert a CFF-flavored OTF into TTF.
    - patchGlyphNames() Rename the glyphs in the font.
    - stripInstructions() Remove all TT instructions from the font.
    - findComponentGlyphs() Find glyphs that are used as components.
    - findGlyphsByUnicode() Find glyphs that are needed to render a given set of unicode values.
    - getBestCmap() Find the 'best' cmap in a font and return the cmap dict.
    - setUnicodeRanges()

featureBuilder:
    - addSingleSubstFeature() Create and add a new SingleSubst feature.


Additional submodules:

otlTools: tools to inspect and manipulate GPOS and GSUB tables
unicodeRanges: tools to query and otherwise deal with unicode ranges, mostly in the OS/2 sense
ttGlyphBuilder: building TT glyph data, converting cubic beziers to quadratics.
"""

__version__ = "2.0"
