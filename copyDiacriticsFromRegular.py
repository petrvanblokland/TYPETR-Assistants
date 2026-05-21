src = CurrentFont()

COPY_THEM = ('asciitilde', 'acutecmb.uc', )
COPY_THEM = ('questiondown', )

for f in AllFonts():
    if f.path.endswith('Segoe_Serif_Display-Regular_MA168.ufo'):
        continue
    for g in src:
        #if 'cmb' in g.name or g.name in COPY_THEM:
        if g.name in COPY_THEM:
            f[g.name] = g
            f[g.name].changed()
            print(g.name, f.path)
            
    f.save()