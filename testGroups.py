for f in AllFonts():
    f.save()
    f.close()
    continue
    #f = CurrentFont()
    for (c1, c2), k in sorted(f.kerning.items()):
        if c2 == 'sfthyphen':
            del f.kerning[(c1, c2)]
        if (c1 in f.groups or c1 in f) and (c2 in f.groups or c2 in f):
            continue
        print(c1, c2, k, c1 in f.groups, c1 in f, c2 in f.groups, c2 in f, f.path)

    if 'sfthyphen' in f:
        f.removeGlyph('sfthyphen')

    if not 'softhyphen' in f:
        f.newGlyph('softhyphen')
        f['softhyphen'].width = 0
        f['softhyphen'].unicode = 0x00Ad
        print('Add softhyphen', f.path)
        

print('Done')