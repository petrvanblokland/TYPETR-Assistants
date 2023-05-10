# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
#     Version 001
# ..............................................................................
#
#     TYPETR Assistant
#
#     A fast and flexible version collections of helpers for type projects.
#

from mojo.subscriber import Subscriber, WindowController
from vanilla import (Window, FloatingWindow, TextBox, EditText, PopUpButton, RadioGroup, List, Button)

W, H = 500, 450
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/2
CW2 = (CW-M)/2
C0 = M
C1 = C0 + CW + M
VT = 120 # Vertical tab from bottom
FAR = 100000 # Move stuff out of view

WindowClass = Window
#WindowClass = FloatingWindow

class Typolator(Subscriber, WindowController):
    debug = True

    #    B U I L D I N G
    
    def build(self):

        y = M
        self.w = WindowClass((W, H), 'Typolator', minSize=(W, H))

        self.w.filterPatternLabelStart = TextBox((M, y, CW/3, 24), 'Starts')
        self.w.filterPatternLabelHas = TextBox((M+CW/3, y, CW/3, 24), 'Has')
        self.w.filterPatternLabelEnd = TextBox((M+2*CW/3, y, CW/3, 24), 'Ends')
        self.w.referenceUfo = TextBox((C1, y, CW, 24), 'Reference UFO')
        #self.w.filterItalicUfo = vanilla.HorizontalRadioGroup((C2, y, CW, 24), ('Roman', 'Italic'), callback=self.updateUfoListCallback)
        #self.w.filterItalicUfo.set(0)
        y += L
        self.w.filterPatternStart = EditText((M, y, CW/3, 24), continuous=True, callback=self.filterNamesCallback)
        self.w.filterPatternHas = EditText((M+CW/3, y, CW/3, 24), continuous=True, callback=self.filterNamesCallback)
        self.w.filterPatternEnd = EditText((M+2*CW/3, y, CW/3, 24), continuous=True, callback=self.filterNamesCallback)

        # List of currently open fonts, that can be used as reference.
        self.w.referenceSelection = PopUpButton((C1, y, CW, 24), [], callback=self.updateUfoListCallback)
        
        y += L*1.2
        self.w.glyphNames = List((M, y, CW, -VT), items=[], doubleClickCallback=self.dblClickGlyphNamesCallback)
        self.w.ufoNames = List((M+M+CW, y, CW, -VT), items=[], doubleClickCallback=self.dblClickUfoNamesCallback)
        y = -VT
        self.w.selectOpenDblClick = RadioGroup((C1, y, CW, L), ('Open GlyphEditor', 'Open FontWindow'), isVertical=False, sizeStyle='small')
        self.w.selectOpenDblClick.set(0)
        y += L
        #self.w.checkInterpolation = vanilla.Button((C1, y, CW, 32), 'Check/Fix', callback=self.checkInterpolationCallback)
        #y += L*1.1
        self.w.saveAll = Button((C1, y, CW2, 32), 'Save all', callback=self.saveAllCallback)
        self.w.saveCloseAll = Button((C1 + CW2 + M, y, CW2, 32), 'Save/Close all', callback=self.saveCloseAllCallback)
    
        self.glyphgNames = []
        self.updateRefPopup() 
        self.updateUfoListCallback()

    def started(self):
        self.w.open()

    def currentGlyphMetricsDidChange(self, info):
        glyph = info['glyph']
        print('--- currentGlyphMetricsDidChange', glyph.name)
        
    #    E V E N T S

    def fontDocumentDidOpen(self, info):
        print('--- fontDocumentDidOpen', info.keys())
        
    def fontDocumentWindowDidOpen(self, info):
        print('--- fontDocumentWindowDidOpen', info.keys())

    def fontDocumentWillClose(self, info):
        print('--- fontDocumentWillClose', info['font'].path)

    #    C A L L B A C K S

    def filterNamesCallback(self, sender=None):
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

        f = CurrentFont()
        for glyphName in sorted(self.glyphNames):
            selected = None
            if ((not filterPatternStart or glyphName.startswith(filterPatternStart)) and
                (not filterPatternHas or filterPatternHas in glyphName) and
                (not filterPatternEnd or glyphName.endswith(filterPatternEnd))):
                selected = glyphName
            # Test on component filter too
            if f is not None and selected is not None and selected in f and (
                componentPatternStart is not None or componentPatternHas is not None or componentPatternEnd):
                selectedByComponent = None
                for component in f[selected].components:
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

    def dblClickUfoNamesCallback(self, sender):
        ref = self.getReferenceFont()
        if ref is None:
            self.w.referenceSelection.setItems([])
            self.w.glyphNames.setItems([])
            self.w.ufoNames.siteItems([])
            return
        dirPath = getUfoDirPath(ref)

        ufoSelected = sender.getSelection()
        for ufoIndex in ufoSelected:

            ufoPath = dirPath + sender[ufoIndex]

            if self.w.selectOpenDblClick.get() == 0:
                f = getMaster(ufoPath, showInterface=True)
                selected = self.w.glyphNames.getSelection()
                for index in selected:
                    glyphName = self.w.glyphNames[index]
                    if glyphName in f:
                        OpenGlyphWindow(f[glyphName])
                
            else:
                pass
                                    
    def dblClickGlyphNamesCallback(self, sender):
        """Double click on one of the glyphs. Open the glyph editor on the selectyed UFO and otherwise
        on the current font"""
        selected = sender.getSelection()
        for index in selected:
            glyphName = sender[index]
            ufoSelection = self.w.ufoNames.getSelection()
            f = None
            if ufoSelection:
                ref = self.getReferenceFont()
                if ref is not None:
                    dirPath = getUfoDirPath(ref) # Get the directory of the reference.
                    f = getMaster(dirPath + self.w.ufoNames[ufoSelection[0]])
            else:
                f = CurrentFont()
            if f is not None:
                g = f[glyphName]
                if self.w.selectOpenDblClick.get() == 0:
                    OpenGlyphWindow(g) # Open the editor window on the selected glyph name.
                else:
                    for fontWindow in AllFontWindows():
                        if fontWindow._font == f.naked():
                            fontWindow.window().show()
                            
    def updateUfoListCallback(self, sender=None):
        """Update the list of UFOs that are in the same folder as the fonts that are currently open.
        Open them in the background if not already open."""
        self.glyphNames = set()
        ufoNames = []

        ref = self.getReferenceFont()
        if ref is None:
            return

        dirPath = getUfoDirPath(ref)
        refName = getUfoName(ref)
        
        for fileName in os.listdir(dirPath):
            if not fileName.endswith('.ufo'):
                continue
            ufoPath = dirPath + fileName
            select = bool('Italic' in refName) == bool('Italic' in fileName)
            if select:
                ufoNames.append(fileName)
                ufo = getMaster(ufoPath, False)
                self.glyphNames = self.glyphNames.union(set(ufo.keys()))
                    
        self.w.ufoNames.set(sorted(ufoNames))
        self.filterNamesCallback()

    def saveCloseAllCallback(self, sender):
        # Save and close all open fonts
        for f in AllFonts():
            f.save()
            f.close()
         
    def saveAllCallback(self, sender):
        # Save and close all open fonts
        for f in AllFonts():
            f.save()
 
    #    G E T T I N G  D A T A
    
    def getReferenceFont(self):
        ref = None
        refName = self.w.referenceSelection.getItem()
        if refName is None:
            return None
        # Find the reference font
        for f in AllFonts():
            if getUfoName(f) == refName:
                return f
        return None
                    
    #    U P D A T I N G
    
    def updateRefPopup(self):
        refNames = []
        for f in AllFonts(): # Use open fonts as seed to find the folders. 
            refNames.append(getUfoName(f))
        self.w.referenceSelection.setItems(refNames)
              
            
if __name__ == '__main__':
    Typolator(currentGlyph=True)
    