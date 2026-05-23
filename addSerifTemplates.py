for f in AllFonts():
    if 'a.br.serif' not in f:
        f.newGlyph('a.br.serif')
        print('a.br.serif', f.path)
        
    if 'Italic' in f.path:
        f['a.br.serif'] = f['n.br.serif']
        
    f.save()    
print('Done')