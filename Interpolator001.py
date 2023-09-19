# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR Interpolator.py
#
#    How to make a TYPETR helper
#    Define the base subscriber class that responds to RoboFont event.
#    Define the base class the creates the UI window for the helper/assistant tool.
#    Inheriting controller classes can define required functions by setting class flags to True.
#    This class mostly just defines the window, controls and interactions, calling events
#    for the Assistant-Subscriber to perform tasks on glyphs and UFO’s.
#
#    In this example the Subscriber and Controller and combined in the GlyphBrowser class.
#    
#    Helpers are generic tools that can perform a series of tasks. They know how to build their
#    part of the interface. They instruct the Assistant on which events they want to respond
#    and they know how to perform theirs tasks on glyph, current UFO or all UFOs.
#    Helpers can draw in the EditorWindow through Merz objects. And they can construct their
#    own window or canvas.

# Generic system imports
import os, sys

# Import of resources available in RoboFont
from vanilla import (Window, FloatingWindow, TextBox, HorizontalRadioGroup, EditText, PopUpButton, 
    List, CheckBox, RadioGroup, Button)
import merz
from mojo.subscriber import Subscriber, WindowController, registerRoboFontSubscriber
from mojo.roboFont import AllFonts, OpenFont, CurrentFont
from mojo.UI import OpenGlyphWindow

# Add the local assistantLib library to the RoboFont sys paths if it does not already exist.
# This ways we can just start this script without the need to install it into RoboFont.
# Maybe not entirely user friendly (the script is running from the source, instead of making
# it available from a menu), but the iterative concept of helpers and assistants make them
# closer to be viewed as source.
# The PATH can also be used to access other resources in this repository.
PATH = '/'.join(__file__.split('/')[:-1]) + '/' # Get the directory path that this script is in.
if not PATH in sys.path: # Is it not already defined in RoboFont
    sys.path.append(PATH) # Then add it.
import assistantLib # Now we can import local helper/assistant stuff 

# Define the GlyphBrowser class, inheriting from Subsriber (which responds to RoboFont events)
# and WindowController (which knows how to deal with the user interface).
# In principle these could be two separate classes (GlyphBrowserSubscriber and GlyphBrowserController)
# but in simple helper applications like this it’s also good to combine the functions.

class Interpolator(Subscriber, WindowController):
    """The SimpleAssistant is a demo class to show how events work between inside the 
        Assistant as well as from the EditorWindow. 
    """
    debug = True

    WINDOW_CLASS = Window # FloatingWindow or Window
    debug = True
    VERBOSE = False

    TITLE = 'GlyphBrowser'

    # Layout paratemers. Not using Ezui right now, just layout math.
    X = Y = 50 # Position of the window, should eventually come from RF preference storage.
    W, H = 500, 600 # Width and height of controller window, should eventually come from RF preference storage.
    MINW, MINH, MAXW, MAXH = W, H, 3 * W, 3 * H # Min/max size of the window
    M = 8 # Margin and gutter
    L = 20 # Line height between controls
    LL = 32 # Line height between functions
    BH = 32 # Button height
    TBH = 24 # Text box height
    LH = 24 # Label height
    POBH = 24 # Popup button height
    CW = (W - 4 * M) / 3 # Column width
    CW2 = 2 * CW + M # Column width
    C0 = M # X position of column 0
    C1 = C0 + CW + M # X position of column 1
    C2 = C1 + CW + M # X position of column 2
    BROWSER_BOTTOM = -36 # Save room at the bottom of the lists to add buttons.

    def build(self):
        self.fonts = {} # Storage of opened fonts without an interface.
        self.glyphNames = set() # Combined set of all glyph names of all fonts

        self.w = self.WINDOW_CLASS((self.X, self.Y, self.W, self.H), self.TITLE, 
            minSize=(self.MINW, self.MINH), maxSize=(self.MAXW, self.MAXH))
        self.buildUI()
        self.w.open()

    def buildUI(self):
        """Build the controls for preview/overlay glyph functions:
            [        ] - Select glyphs with a name that starts with this pattern
            [        ] - Select glyphs with a name that contains this pattern
            [        ] - Select glyphs with a name that ends with this pattern
            [        ] - List of glyph names, full set of all ufo’s or subset by patterns
            [x] Open GlyphEditor on double click on glyph names
            (o) Roman ( ) Italic - Select fonts w/o 'Italic' in the file name
            (UFO name) - Reference ufo selection
            [        ] - List of ufo names that are in the same directory as the selected reference ufo.
            (o) Open GlyphEditor (o) Open FontEditor on double click on font names
        """
        if self.VERBOSE:
            print('--- GlyphBrowserController.buildUI')
        
        y = self.L / 2
        self.w.labelUnicode = TextBox((self.M, y, self.CW/3, 24), 'Unicode', sizeStyle='small')
        
        y += self.L * 2/3
        self.w.unicode = TextBox((self.M, y, self.CW/3, 24), '')
        
        y += self.L*1.2
        self.w.filterPatternLabelStart = TextBox((self.M, y, self.CW/3, 24), 'Starts', sizeStyle='small')
        self.w.filterPatternLabelHas = TextBox((self.M+self.CW/3, y, self.CW/3, 24), 'Has', sizeStyle='small')
        self.w.filterPatternLabelEnd = TextBox((self.M+2*self.CW/3, y, self.CW/3, 24), 'Ends', sizeStyle='small')
        self.w.referenceUfo = TextBox((self.C1, y, self.CW, self.TBH), 'Reference UFO', sizeStyle='small')
        self.w.filterItalicUfo = HorizontalRadioGroup((self.C2, y, self.CW, self.TBH), ('Roman', 'Italic'), 
            callback=self.updateCallback, sizeStyle='small')
        self.w.filterItalicUfo.set(0)
        y += self.L
        self.w.filterPatternStart = EditText((self.M, y, self.CW/3, self.TBH), continuous=True, callback=self.glyphNameListCallback)
        self.w.filterPatternHas = EditText((self.M+self.CW/3, y, self.CW/3, self.TBH), continuous=True, callback=self.glyphNameListCallback)
        self.w.filterPatternEnd = EditText((self.M+2*self.CW/3, y, self.CW/3, self.TBH), continuous=True, callback=self.glyphNameListCallback)

        # List of currently open fonts, that can be used as reference.
        refNames = self.getOpenUfoNames()
        self.w.ufoReference = PopUpButton((self.C1, y, -self.M, self.POBH), refNames, callback=self.ufoReferenceSelectionCallback)
        
        y += self.L*1.2
        self.w.glyphNames = List((self.C0, y, self.CW, self.BROWSER_BOTTOM), items=[], # Will later be updated.
            doubleClickCallback=self.glyphNameListDblClickCallback)
        self.w.ufoNames = List((self.C1, y, -self.M, self.BROWSER_BOTTOM), items=[], # Will later be updated. 
            doubleClickCallback=self.dblClickUfoNamesCallback)
        
        self.w.selectOpenDblClick = CheckBox((self.C1, self.BROWSER_BOTTOM + self.M, self.CW2, self.L), 'Open interface', sizeStyle='small')
        self.w.selectOpenDblClick.set(0)
                
        # Update the referenced ufo names and the glyph list.
        self.updateUfoListCallback()
        self.filterNamesCallback()

        return y + self.LL

    def started(self):
        pass

    def destroy(self):
        for ufoPath, f in self.fonts.items():
            f.save() # Make sure to save them.
            f.close()

    #   H E L P E R S

    def getCurrentFont(self, showInterface=False):
        """Answer the currently open font. Answer None if no font is open."""
        f = CurrentFont()
        if f is None: # No current font open, then try one from the list.
            f = self.getSelectedFont(showInterface)
            if f is None:
                f = self.getReferenceFont(showInterface)
        return f
        
    def getUfoName(self, f):
        """Answer the file name of this font. Answer None if there is no path."""
        if f.path is not None: # Untitled fonts don't have a path
            return f.path.split('/')[-1] # Answer the ufo file name
        return None

    def getUfoDirPath(self, f):
        """Answer the directory path that this UFO is in."""
        if f.path is not None:
            return '/'.join(f.path.split('/')[:-1]) + '/'
        return None

    def getReferenceFont(self):
        """Answer the font that is referred to in the popup. Just search in the fonts that are
        opened with an interface."""
        ref = None
        refName = self.w.ufoReference.getItem()
        if refName is None: # No referece font selected
            return None
        # Find the reference font, just search in the open fonts.
        for f in AllFonts():
            if refName == self.getUfoName(f):
                return f
        return None

    def getSelectedFont(self, showInterface=False):
        """Answer the font that is selected in the ufo list.If @showInterface is True, then make sure
        that the font is/will be opened in RoboFont"""
        f = None
        selectedUfoName = self.w.ufoNames.getSelection()
        if selectedUfoName:
            f = self.getFontByName(self.w.ufoNames.get()[selectedUfoName[0]], showInterface)
            if f is None: # Did we find one from the ufo list selection
                f = self.getReferenceFont(showInterface) # Otherwise try the referrenced font
        return f
        
    def getFontByName(self, ufoName, showInterface=False):
        """Answer the font that has this ufo file name. If @showInterface is True, then make sure
        that the font is/will be opened in RoboFont"""
        ref = self.getReferenceFont()
        if ref is not None:
            dirPath = self.getUfoDirPath(ref)
            if dirPath is not None:
                ufoPath = dirPath + ufoName
                f = self.getFont(ufoPath, showInterface)
                if f is not None:
                    return f
        return None
        
    def getFont(self, fullPath, showInterface=False):
        """Check if the path exists as open font. Then answer that.
        Otherwise check if we already have the font opened without interface. Then answer that.
        Otherwise open the fonnt without an interface and store it in self.fonts."""

        assert fullPath.endswith('.ufo')
        if not os.path.exists(fullPath): # Don't try.
            return None
        
        for f in AllFonts():
            if f.path == fullPath:
                # If we already have it open without interface, then delete it.
                if fullPath in self.fonts:
                    del self.fonts[fullPath]
                return f
                
        # It's not currently open with Interface in RoboFont.
        if showInterface: # If it should be open with interface, then do that.
            # If we already have it open without interface, then delete it.
            if fullPath in self.fonts:
                del self.fonts[fullPath]
            f = OpenFont(fullPath, showInterface=showInterface)
            self.fonts[fullPath] = f
            return f
            
        if fullPath in self.fonts:
            return self.fonts[fullPath]
        
        f = OpenFont(fullPath, showInterface=False)
        self.fonts[fullPath] = f
        return f
        
    def getOpenUfoNames(self):
        """Answer the list of ufo names are are currently open."""
        ufoNames = []
        for f in AllFonts():
            ufoNames.append(f.path.split('/')[-1])
        return ufoNames

    def getReferencedUfoNames(self):
        """Answer the list of ufo names that are in the same folder as the referred ufo.
        Filter on 'Italic' in the name, corresponding to the status of the reference ufo."""
        ufoNames = []

        ref = self.getReferenceFont()
        if ref is not None:
            dirPath = self.getUfoDirPath(ref) # Get the path where the reference font is in.
            refName = self.getUfoName(ref) # Get the ufo file name of the reference font. 
        
            for ufoName in os.listdir(dirPath):
                if not ufoName.endswith('.ufo'): # Only search for ufo files
                    continue
                # Check if we have this font open yet, otherwise open it without interface.
                ufoPath = dirPath + ufoName
                ufo = self.getFont(ufoPath) # This will make sure it could be opened or already was.
                if ufo is not None:
                    # Check on similarity for italic 
                    select = bool('Italic' in refName) == bool('Italic' in ufoName)
                    if select:
                        ufoNames.append(ufoName)
                        self.glyphNames = self.glyphNames.union(set(ufo.keys()))

        return ufoNames
        
    #   C A L L B A C K S
    
    def updateUfoListCallback(self, sender=None):
        """Update the list of UFOs that are in the same folder as the fonts that are currently open.
        Open them in the background if not already open."""
        self.glyphNames = set()
        ufoNames = self.getReferencedUfoNames()
        self.w.ufoNames.set(sorted(ufoNames))
        self.filterNamesCallback() # Calculate the new overall set of glyph names for the new ufo list

    def filterNamesCallback(self, sender=None):
        print('--- filterNamesCallback')
        filteredGlyphNames = []
        filterPatternStart = self.w.filterPatternStart.get().strip()
        filterPatternHas = self.w.filterPatternHas.get().strip()
        filterPatternEnd = self.w.filterPatternEnd.get().strip()
        # Search for component patterns
        componentPatternStart = componentPatternHas = componentPatternEnd = None
        if '@' in filterPatternStart:
            componentPatternStart = filterPatternStart.split('@')[1]
            filterPatternStart = filterPatternStart.split('@')[0]
        if '@' in filterPatternHas:
            filterPatternHas = filterPatternHas.split('@')[1]
            filterPatternHas = filterPatternHas.split('@')[0] # In there is a combined pattern A@
        if '@' in filterPatternEnd:
            componentPatternEnd = filterPatternEnd.split('@')[1]
            filterPatternEnd = filterPatternEnd.split('@')[0]
        
        ref = self.getReferenceFont()
        for glyphName in sorted(self.glyphNames):
            selected = None
            if ((not filterPatternStart or glyphName.startswith(filterPatternStart)) and
                (not filterPatternHas or filterPatternHas in glyphName) and
                (not filterPatternEnd or glyphName.endswith(filterPatternEnd))):
                selected = glyphName
            # Test on component filter too
            if ref is not None and selected is not None and (
                componentPatternStart is not None or componentPatternHas is not None or componentPatternEnd):
                selectedByComponent = None
                for component in ref[selected].components:
                    if componentPatternStart is not None and component.baseGlyph.startswith(componentPatternStart):
                        selectedByComponent = selected
                        break
                    if componentPatternHas is not None and componentPatternHas in component.baseGlyph:
                        selectedByComponent = selected
                        break
                    if componentPatternEnd is not None and component.baseGlyph.endswith(componentPatternEnd):
                        selectedByComponent = selected
                        break
                selected = selectedByComponent # Not this one.
            if selected is not None:
                filteredGlyphNames.append(selected)
                
        self.w.glyphNames.set(sorted(filteredGlyphNames))

    def ufoReferenceSelectionCallback(self, sender):
        print('--- ufoReferenceSelectionCallback')
        
    def glyphNameListCallback(self, sender=None):
        """Something happened to the glyph name list. Update it."""
        self.filterNamesCallback()
        #self.updateGlyphInfo()
        #self.update()
        # Don't call editor open on selection, because it will make typing in the filter impossible.
                                        
    def glyphNameListDblClickCallback(self, sender):
        """Open the selected glyph in the current font (independent from which font is selected in the ufo names list).
        If there is no current font, then try selecting from the ufo list or the reference font."""
        # Get the new first selected glyph name
        selection = self.w.glyphNames.getSelection()
        if selection:
            gName = self.w.glyphNames[selection[0]]
            f = self.getCurrentFont()
            if f is not None and gName in f:
                OpenGlyphWindow(f[gName]) # Open the window or change to

    def dblClickUfoNamesCallback(self, sender):
        """Open the selected glyph in the selected font.
        If there is no current font, then try selecting from the ufo list or the reference font."""
        # Get the new first selected glyph name
        print('--- dblClickUfoNamesCallback')
        selectedGlyph = self.w.glyphNames.getSelection()
        if selectedGlyph:
            gName = self.w.glyphNames[selectedGlyph[0]]
            openInterface = self.w.selectOpenDblClick.get()
            f = self.getSelectedFont(openInterface)
            if f is not None and gName in f:
                OpenGlyphWindow(f[gName]) # Open the window or change to
        else:
            openInterface = self.w.selectOpenDblClick.get()
            self.getSelectedFont(openInterface)
            

    def updateCallback(self, sender):
        pass
                
    #   E V E N T S
    
    def fontDocumentWindowDidOpen(self, info):
        self.filterNamesCallback()
        
    def fontDocumentDidClose(self, info):
        #self.update()
        pass
        
    def update(self):
        #refNames = self.getOpenUfoNames()
        #self.w.ufoReference.setItems(refNames)
        #self.updateUfoListCallback()
        #self.filterNamesCallback()
        pass
        
    def updateGlyphInfo(self):
        """Update the info about the glyph (such as unicode) from the selected glyph in the list.
        Blank the info if no glyph is selected."""
        selection = self.w.glyphNames.getSelection()
        if selection:
            gName = self.w.glyphNames[selection[0]]
            f = self.getCurrentFont()
            g = f[gName]
            if g.unicode:
                unicode = '%04X' % g.unicode
            else:
                unicode = '----'
            
        else:
            unicode = ''
        self.w.unicode.set(unicode)
                                
if __name__ == '__main__':
    registerRoboFontSubscriber(GlyphBrowser)

