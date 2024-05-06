f = CurrentFont()
#print(sorted(f.groups.keys()))
lt1 = set()
lt2 = set()
cy1 = set()
cy2 = set()
gr1 = set()
gr2 = set()
rest1 = set()
rest2 = set()

def cleaned(s):
    s = s.replace('_lt', '')
    s = s.replace('_cy', '')
    s = s.replace('_gr', '')
    s = s.replace('public.kern1.', '')
    s = s.replace('public.kern2.', '')
    s = s.replace('_sc', '')
    return s
    
for groupName in f.groups.keys():
    if 'kern1' in groupName:
        if groupName.endswith('_lt'):
            lt1.add(cleaned(groupName))
        elif groupName.endswith('_cy'):
            cy1.add(cleaned(groupName))
        elif groupName.endswith('gr'):
            gr1.add(cleaned(groupName))
        else:
            rest1.add(cleaned(groupName))
                
    if 'kern2' in groupName:
        if groupName.endswith('_lt'):
            lt2.add(cleaned(groupName))
        elif groupName.endswith('_cy'):
            cy2.add(cleaned(groupName))
        elif groupName.endswith('gr'):
            gr2.add(cleaned(groupName))
        else:
            rest2.add(cleaned(groupName))
            
print('-'*60)
print('lt1', sorted(lt1))
print('-'*60)
print('cy1', sorted(cy1))
print('-'*60)
print('gr1', sorted(gr1))
print('-'*60)
print('rest1', sorted(rest1))
print('-'*60)

print('-'*60)
print('lt2', sorted(lt2))
print('-'*60)
print('cy2', sorted(cy2))
print('-'*60)
print('gr2', sorted(gr2))
print('-'*60)
print('rest2', sorted(rest2))
print('-'*60)
