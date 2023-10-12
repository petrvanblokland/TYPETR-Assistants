f = CurrentFont()
names = []
for gName in sorted(f.keys()):
    if 'cyrillic' in gName and '.ct' in gName:
        names.append(gName)
        
        
print(' '.join(names))