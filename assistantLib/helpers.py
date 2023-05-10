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

openFonts = {} # Storage of fonts that are open to the Assistant, without RF interface.
glyphNames = [] # Collect the combined set of glyph names here for all open fonts.

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
    
def getCurrentDirectory(f):
    """Answer the path of this font."""
    if f.path is None:
        return None
    return '/'.join(f.path.split('/')[:-1]) + '/'

def getOpenUfoNames():
    """Answer the sorted list of all UFO's with an open interface."""
    refNames = []
    for f in AllFonts(): # Use open fonts as seed to find the folders. 
        refNames.append(getUfoName(f))
    return refNames

def getFont(path, showInterface=False):
    global openFonts
    print('... Opening', path)
    # Check if the master is already open, by RoboFont or by self
    for f in AllFonts():
        if f.path is not None and f.path.endswith(path):
            print('... Selecting open font', path)
            if showInterface:
                print('... Open interface', path)
                f.openInterface()
            return f
    if path in openFonts:
        f = openFonts[path]
        if showInterface:
            print('... Open interface', path)
            f.openInterface()
        return f
    # Not open yet, open it in the background and cache the master
    # In case "showUI" error here, then start venv
    f = OpenFont(path, showInterface=showInterface)
    if f is None:
        print('### Cannot open font', path)
        return None
    openFonts[path] = f
    return f
