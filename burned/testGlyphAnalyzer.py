
import importlib

import assistantLib
from assistantLib.toolbox.glyphAnalyzer import GlyphAnalyzer

importlib.reload(assistantLib.toolbox.glyphAnalyzer)
from assistantLib.toolbox.glyphAnalyzer import GlyphAnalyzer

g = CurrentGlyph()
ga = GlyphAnalyzer(g)

if 0:
    for a, diagonal in sorted(ga.diagonals.items()):
        print('Diagonal', a, diagonal)
    print('---')
    for x, vertical in sorted(ga.verticals.items()):
        print('Vertical', x, vertical)
    print('---')
    for x, vertical in sorted(ga.roundVerticals.items()):
        print('Round vertical', x, vertical)
    print('---')
    for x, vertical in sorted(ga.straightVerticals.items()):
        print('Straight vertical', x, vertical)
    print('---')

    for y, horizontal in sorted(ga.horizontals.items()):
        print('Horizontal', y, horizontal)
    print('---')
    for y, horizontal in sorted(ga.roundHorizontals.items()):
        print('Round horizontal', y, horizontal)
    print('---')
    for y, horizontal in sorted(ga.straightHorizontals.items()):
        print('Straight horizontal', y, horizontal)
    print('---')


print(ga.stems)
print(ga.bars)