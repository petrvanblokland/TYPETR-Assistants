for f in AllFonts():
    
    print(f.path)
    for g in f:
        for a in g.anchors:
            if a.y in (1388, 1373):
                print(g.name)
                a.y = 1356
                g.changed()
            
print('Done')