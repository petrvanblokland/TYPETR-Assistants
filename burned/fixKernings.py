for f in AllFonts():
    f.kerning[('public.kern1.A_sc_lt_sc', 'public.kern2.T_sc_lt_sc')] = -80
    f.kerning[('public.kern1.T_sc_lt_sc', 'public.kern2.A_sc_lt_sc')] = -80
    for (c1, c2), k in f.kerning.items():
        if 'A.sc' in f.groups[c1] or 'T.sc' in f.groups[c2]:
            print(c1, c2, k, f.path.split('/')[-1])
            
    for gName, group in f.groups.items():
        if 'A.sc' in group:
            print(gName)
            break
            
    for gName, group in f.groups.items():
        if 'T.sc' in group:
            print(gName)
            break
    f.save()