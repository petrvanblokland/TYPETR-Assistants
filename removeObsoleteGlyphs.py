from assistantLib.assistantParts.glyphsets.TYPETR_full_set import *


for f in AllFonts():
    for gName in sorted(f.keys()):
        g = f[gName]
        if not g.name in TYPETR_GlyphSet.GLYPH_DATA:
            s = f"\tgds['{g.name}'] = GD(name='{g.name}'"
            if g.components:
                s += f", base='{g.components[0].baseGlyph}'"
                if len(g.components) > 1:
                    accents = []
                    for component in g.components[1:]:
                        if component.baseGlyph != g.components[0].baseGlyph:
                            accents.append(component.baseGlyph)
                    if accents:
                        s += f""", accents=('{", ".join(accents)}')"""
            s += f')' # # {len(g.components)}'
            print(s)
    break
    