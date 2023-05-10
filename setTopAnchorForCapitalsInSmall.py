for f in AllFonts(): # Needs to be Small for Regular, Light, Hairline

    print(f.path)
    for g in f:
        for a in g.anchors:
            if a.y == 1356:
                print(g.name)
                a.y = 1388
                g.changed()
            
print('Done')