for f in AllFonts():
    f.kerning.clear()
    f.groups.clear()
    f.save()
    
    for g in f:
        for component in g.components:
            if component.baseGlyph == 'l':
                print(g.name, component.baseGlyph, f.path)
print('Done')