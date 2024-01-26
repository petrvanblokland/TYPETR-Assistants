# -*- coding: UTF-8 -*-

import sys
from math import *
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR
from assistantLib.assistantParts.data import * # Import anchors names

class AssistantPartGuidelines(BaseAssistantPart):
    """The Guidelines assistant part handles all guideline positions
    """

    def initMerzGuidelines(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        self.registerKeyStroke('±', 'makeGuidelines')

    def updateGuidelines(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width."""
        g = info['glyph']
        if g is None:
            return

    def buildGuidelines(self, y):
        """Build the assistant UI for anchor controls."""
        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        c.w.makeGuides = Button((C0, y, CW, L), 'Make guides', callback=self.makeGuidesCallback)
        y += L + LL

        return y

    def makeGuidesCallback(self, sender):
        pass