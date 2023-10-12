for f in AllFonts():
    if 0:
        for g in f:
            for component in g.components:
                if component.baseGlyph == 'l':
                    print(g.name, component.baseGlyph)
                elif component.baseGlyph == 'L.sc':
                    print(g.name, component.baseGlyph)
                
        for gName, group in f.groups.items():
            if 'l' in group: # or 'L.sc' in group: 
                print(gName, group, f.path)
            elif 'L.sc' in group: # or 'L.sc' in group: 
                print(gName, group, f.path)

    if 0:            
        for (c1, c2), k in f.kerning.items():
            if c1 == 'public.kern1.l_lt':
                print(c1, c2, k) 
            
        for (c1, c2), k in f.kerning.items():
            if c1 == 'public.kern2.l_lt':
                print(c1, c2, k) 
        
    for (c1, c2), k in f.kerning.items():
        if c1.endswith('_lt') and c2.endswith('_lt_sc'):
            print(c1, c2, k) 

    for (c1, c2), k in f.kerning.items():
        if c1.endswith('_lt_sc') and c2.endswith('_lt'):
            print(c1, c2, k) 
