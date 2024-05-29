for f in AllFonts():
    for g in f:
        if 'enclosingkeycapcomb' in g.name:
            print(g.name, g.angledLeftMargin, g.angledRightMargin, f.path.split("/")[-1])
            g.angledLeftMargin = f['H'].angledLeftMargin
            g.angledRightMargin = f['H'].angledRightMargin
            g.changed()
            
            
print('Done')