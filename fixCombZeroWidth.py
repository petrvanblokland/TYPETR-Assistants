for f in AllFonts():
    for g in f:
        if 'comb' in g.name:
            if 'pnum' in g.name:
                if round(g.angledLeftMargin) or round(g.angledRightMargin):
                    print(g.name, g.width, f.path)
                    g.angledLeftMargin = 0
                    g.angledRightMargin = 0
                    g.changed()
            elif g.width != 0:
                print(g.name, g.width, f.path)
                g.width = 0
                g.changed()
                
    f.save()
    #f.close()
            
            
print('Done')