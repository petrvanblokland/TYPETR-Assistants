f = CurrentFont()
for groupName, group in f.groups.items():
    isCm0 = isCm2 = False
    cm0 = None
    for gName in group:
        if '.cm0' in gName:
            isCm0 = True
            cm0 = gName
        elif '.cm2' in gName:
            isCm2 = True
    if isCm0 != isCm2:
        group = list(group)
        print(groupName, group)
        group.append(cm0.replace('cm0', 'cm2'))
        f.groups[groupName] = group

f.save()
f.close()
        
print('Done')