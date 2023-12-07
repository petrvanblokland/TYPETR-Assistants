for f in AllFonts():
    if 'Responder_P-Regular.ufo' in f.path:
        src = f
        
for f in AllFonts():
    if src.path == f.path:
        continue
    f.groups.clear()
    for groupName, group in src.groups.items():
        f.groups[groupName] = group
        
    f.save()
    f.close()