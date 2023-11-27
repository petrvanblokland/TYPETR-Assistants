f = CurrentFont()
for gg in f:
    g = gg.getLayer('background')
    if '.ct' in g.name or '.cm' in g.name:
        changed = False
        for contour in g.contours:
            for p in contour.points:
                if p.labels == ('F96',) or p.labels == ('F98',):
                    print(g.name, p, p.labels)
                    p.labels = []
                    changed = True
        if changed:
            g.changed()
            #break
                
print('Done')