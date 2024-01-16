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

class AssistantPartInterpolate(BaseAssistantPart):
    """The Interpolate assistant part, checks on interpolation errors and
    interpolates glyphs is the UFO is defined as instance, instead of master.
    """
    def initInterpolation(self, container):
        pass

    def updateInterpolation(self, info):
        pass

    def buildInterpolation(self, y):
        pass
        return y

