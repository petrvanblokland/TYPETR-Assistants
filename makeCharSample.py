unis = []
for g in CurrentFont():
    if g.unicode:
        unis.append(g.unicode)
        
s = ''
for uni in sorted(unis):
    s += chr(uni) + '&shy;'
    
    
print(s)
