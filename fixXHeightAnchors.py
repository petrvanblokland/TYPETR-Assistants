f = CurrentFont()
for g in f:
    for a in g.anchors:
        if a.y == 1040:
            print(g.name)
            a.y = 1008
            g.changed()
            
print('Done')