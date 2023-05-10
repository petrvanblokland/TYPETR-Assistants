# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
#     Version 004
# ..............................................................................
#
#     TYPETR Assistant
#
#     A fast and flexible collection of helpers for type projects.
#
import importlib

import assistantLib
from assistantLib import baseAssistant
from assistantLib import helpers
from assistantLib import tp_previewOverlay
from assistantLib import tp_glyphBrowser
from assistantLib.tp_glyphBrowser import GlyphBrowser
from assistantLib.tp_glyphBrowser import GlyphBrowserController
from assistantLib import tp_previewDesignspace
from assistantLib.tp_previewDesignspace import PreviewDesignspace
from assistantLib.tp_previewDesignspace import PreviewDesignspaceController

importlib.reload(assistantLib)
importlib.reload(assistantLib.baseAssistant)
importlib.reload(assistantLib.helpers)
importlib.reload(assistantLib.tp_previewDesignspace)
importlib.reload(assistantLib.tp_previewOverlay)
importlib.reload(assistantLib.tp_glyphBrowser)

from assistantLib.tp_previewDesignspace import PreviewDesignspace, PreviewDesignspaceController
from assistantLib.tp_previewOverlay import PreviewOverlay, PreviewOverlayController
from assistantLib.tp_glyphBrowser import GlyphBrowser, GlyphBrowserController

class UpgradePreviewDesignspaceController(PreviewDesignspaceController):
    UFO_PATH = '_ufo/'
    
    MASTER_LOCATIONS = {
        UFO_PATH + 'Upgrade-UltraBlack_Condensed_226.ufo': dict(wght=212, wdth=50),
        UFO_PATH + 'Upgrade-UltraBlack_276.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-UltraBlack_Extended_414.ufo': dict(wght=212, wdth=150),

        UFO_PATH + 'Upgrade-Black_Condensed_196.ufo': dict(wght=212, wdth=50),        UFO_PATH + 'Upgrade-Black_212.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Black_Extended_250.ufo': dict(wght=212, wdth=150),        
        UFO_PATH + 'Upgrade-Semibold_Condensed_136.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Semibold_140.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Semibold_Extended_156.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Regular_Condensed_82.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Regular_84.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Regular_Extended_86.ufo': dict(wght=212, wdth=100),        
        UFO_PATH + 'Upgrade-Light_Condensed_31.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Light_32.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Light_Extended_32.ufo': dict(wght=212, wdth=100),        
        UFO_PATH + 'Upgrade-Hairline_Condensed_8.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Hairline_8.ufo': dict(wght=212, wdth=100),        UFO_PATH + 'Upgrade-Hairline_Extended_8.ufo': dict(wght=212, wdth=100),        
        
    }
if __name__ == '__main__':
    #OpenWindow(PreviewOverlayController)
    #OpenWindow(GlyphBrowserController)
    OpenWindow(PreviewDesignspaceController)
    
    
  
  