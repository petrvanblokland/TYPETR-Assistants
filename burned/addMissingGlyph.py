for f in AllFonts():
    if not 'jecyrillic.cm2' in f:
        f.newGlyph('jecyrillic.cm2')
        print('jecyrillic.cm2')
        f.changed()
        
print('Done')