CYR = """Dzhecyrillic Decyrillic Tsecyrillic Shacyrillic Shchacyrillic Zhedescendercyrillic Kadescendercyrillic Ustraightstrokecyrillic Hadescendercyrillic Chedescendercyrillic""".split(' ')
REMOVE = []
for ext in ('.cl0', '.cm0', '.cm1', '.cm2', '.ct0', '.ct1', '.ct2'):
    for name in CYR:
        REMOVE.append(name + ext)

for f in AllFonts():

    for remove in REMOVE:
        for groupName, group in f.groups.items():
            if remove in group:
                group = list(group)
                group.remove(remove)
                print('remove', remove, 'from', gName)
        if remove in f:
            g = f[remove]
            g.markColor = 0, 0, 1, 1
            f.removeGlyph(remove)
            print(remove)
            
    print('Kerning', len(f.kerning))
    print('Groups', len(f.groups))
    for groupName, group in f.groups.items():
        for gName in group:
            if gName not in f:
                print(gName, groupName, len(group), group)
                group = list(group)
                group.remove(gName)
                f.groups[groupName] = group
        if len(group) == 0:
            del f.groups[groupName]
            print('Remove empty group', groupName)

    for c1, c2 in f.kerning.keys():
        if 'kern' in c1:
            continue
        if c1 not in f:
            print(c1)
        if c2 not in f:
            print(c2)

    f.save()
    f.close()
print('Done')