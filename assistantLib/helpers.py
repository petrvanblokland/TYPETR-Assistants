# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR helpers.py
#
#    Basic transformation tools
#

from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint

#   U F O 

def getUfoName(f):
    """Answer the file name of this font. Answer None if there is no path."""
    if f.path is not None: # Untitled fonts don't have a path
        return f.path.split('/')[-1] # Answet the ufo file name
    return None

def getUfoDirPath(f):
    """Answer the directory path that this UFO is in."""
    if f.path is not None:
        return '/'.join(f.path.split('/')[:-1]) + '/'
    return None
    
def getOpenUfoNames():
    """Answer the sorted list of all UFO's with an open interface."""
    refNames = []
    for f in AllFonts(): # Use open fonts as seed to find the folders. 
        refNames.append(getUfoName(f))
    return refNames

# Alternative better: https://gist.github.com/typemytype/45293f9b29f29cd2458157a44f8fad94#file-headlessrobofont-py-L158

def getFont(path, showInterface=False):
    for f in AllFonts():
        if f.path and f.path.endswith(path):
            return f
    return OpenFont(path, showInterface=showInterface)
