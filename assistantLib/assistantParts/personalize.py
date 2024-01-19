# -*- coding: UTF-8 -*-

import sys
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR

class AssistantPartPersonalize(BaseAssistantPart):
    """The Interpolate assistant part, allows part of the behavior to adapt to
    the designer that is working with in RoboFont.

    - Personalized marker colors for visited glyphs in the FontWindow
    - Personalized dictionary for function keys
    """
    # Select the color by user
    VISITED_MARKERS = [
        #('/Users/petr/Desktop/TYPETR-git', (40/255, 120/255, 255/255, 0.6)), # "Final" marker Blue (Petr))    
        ('/Users/petr/Desktop/TYPETR-git', (50/255, 70/255, 230/255, 0.8)), # "Final" marker Blue (Petr))    
        ('/Users/edwarddzulaj/Documents', (92/255, 149/255, 190/255, 1)), # Edward
        ('/Users/graemeswank/Documents', (255/255, 83/255, 73/255, 1)),
        ('/Users/graeme/Documents', (255/255, 83/255, 73/255, 1)),
        ('/Users/caterinasantullo/Desktop', (226/255, 69/255, 0/255, 1)),
        ('/Users/til/Documents', (0.9, 0.75, 1.0, 1.0)),
        ('/Users/anna/Downloads/Dropbox', (57/255, 163/255, 160/255, 1)),
        ('/Users/lenalepommelet/Documents', (138/255, 43/255,  226/255, 1))
    ]
    VISITED_MARKER = None
    for path, color in VISITED_MARKERS:
        if __file__.startswith(path):
            VISITED_MARKER = color
            print('User color for',  path, color)
            break
    if VISITED_MARKER is None:
        VISITED_MARKER = (1, 1, 1, 1) # Clear to white

    def initMerzPersonalize(self, container):
        pass

    def updateMerzPersonalize(self, info):
        g = info['glyph']
        if g is not None and g.markColor != self.VISITED_MARKER: # NO_MARKER
            g.markColor = self.VISITED_MARKER

    def buildPersonalize(self, y):
        pass
        return y

