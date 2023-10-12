import sys

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/', '../TYPETR-Segoe-UI/')
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from scriptsLib.diacritics import ACCENT_DATA

f = CurrentFont()
diacritics = set()
for g in f:
    for component in g.components:
        if component.baseGlyph in ACCENT_DATA:
            diacritics.add(component.baseGlyph)
        else:
            print('---', component.baseGlyph)
        
print(sorted(diacritics))
        