# -*- coding: UTF-8 -*-
#
#    Similar Assistant for RoboFont4
#    It works on the current font.
#
# 
import sys
import importlib

if 0:
    import os
    import codecs
    import merz
    import weakref
    from random import choice
    from copy import copy
    from math import *
    from AppKit import *

from vanilla import *
import drawBot

if 0:
    from mojo.events import extractNSEvent
    from mojo.UI import OpenGlyphWindow
    from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint
    from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

    from fontTools.misc.transform import Transform

    import assistantLib
    importlib.reload(assistantLib)
    import assistantLib.kerningSamples
    importlib.reload(assistantLib.kerningSamples)
    import assistantLib.kerningSamples.ulcwords
    importlib.reload(assistantLib.kerningSamples.ulcwords)
    import assistantLib.tp_kerningManager
    importlib.reload(assistantLib.tp_kerningManager)

    from assistantLib.kerningSamples.ulcwords import ULCWORDS

from mojo.UI import OpenGlyphWindow

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/', '../TYPETR-Segoe-UI/')
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

import assistantLib
import assistantLib.tp_kerningManager
importlib.reload(assistantLib)
importlib.reload(assistantLib.tp_kerningManager)

from assistantLib.tp_kerningManager import KerningManager, SPACING_TYPES_LEFT, SPACING_TYPES_RIGHT

W, H = 500, 300
M = 20
CW = (W - 5*M)/4
BW = CW # Button width
BH = 24 # Button height


class SimilarSpacer:

    def __init__(self):
        self.kerningManagers = {}
        self.kerningSample = None
        self.base1 = [] # Dictionary of similar base1 glyphs. Will be defined once there is font open.
        self.base2 = [] # Same for similar base2 glyphs
        
        x = M
        y = H - M - BH
        self.w = Window((300, 50, W, H), self.__class__.__name__, minSize=(W, H), maxSize=(W, 10*H))
        
        self.w.baseGlyphsLeft = List((x, M, CW, -M-BH-M), self.base1, selectionCallback=self.baseGlyphsLeftCallback, doubleClickCallback=self.openBaseGlyphsLeftCallback)
        self.w.similarGlyphsLeft = List((x + CW + M, M, CW, -M-BH-M), [], selectionCallback=self.similarGlyphsLeftCallback, doubleClickCallback=self.openSimilarGlyphsLeftCallback)
        self.w.baseGlyphsRight = List((x + 2*(CW + M), M, CW, -M-BH-M), self.base2, selectionCallback=self.baseGlyphsRightCallback, doubleClickCallback=self.openBaseGlyphsRightCallback)
        self.w.similarGlyphsRight = List((x + 3*(CW + M), M, CW, -M-BH-M), [], selectionCallback=self.similarGlyphsRightCallback, doubleClickCallback=self.openSimilarGlyphsRightCallback)

        self.w.spaceButton = Button((x, -M-BH, BW, BH), 'Sides', callback=self.spaceCallback)

        f = CurrentFont()
        if f is not None:
            self.getKerningManager(f) # Will call self.initBaseLists                        
        
        self.w.open()

    #    K E R N I N G

    def getKerningManager(self, f):
        """Answer the kerning manager for this font. Since we want to be comparing sides for the entire glyphset,
        set the flags to ignore difference of the same category and the same script.
        """
        if f.path:
            if f.path not in self.kerningManagers:
                #  First sample will be initialzed, others will be copied
                self.kerningManagers[f.path] = KerningManager(f, sample=self.kerningSample, simSameCategory=False, simSameScript=False)
            km = self.kerningManagers[f.path]
            self.kerningSample = km.sample
            
            if not self.base1: # Not initialized, try again with this font.
                self.base2 = km.getSimilarBaseNames2()
                self.w.baseGlyphsLeft.set(sorted(self.base2.keys()))
                self.base1 = km.getSimilarBaseNames1()
                self.w.baseGlyphsRight.set(sorted(self.base1.keys()))

            return km
        return None
    
    # Interaction with the left lists
    
    def baseGlyphsLeftCallback(self, sender):
        index = sender.getSelection()
        g = CurrentGlyph()
        if index and g is not None:
            selectedGlyphName = sender[index[0]]
            if selectedGlyphName in g.font:
                self.w.similarGlyphsLeft.set(self.base2.get(selectedGlyphName, []))
        
    def openBaseGlyphsLeftCallback(self, sender):
        index = sender.getSelection()
        g = CurrentGlyph()
        if index and g is not None:
            selectedGlyphName = sender[index[0]]
            if selectedGlyphName in g.font:
                gg = g.font[selectedGlyphName]
                OpenGlyphWindow(gg) # Open the window or change to

    def similarGlyphsLeftCallback(self, sender):
        pass
        
    def openSimilarGlyphsLeftCallback(self, sender):
        index = sender.getSelection()
        g = CurrentGlyph()
        if index and g is not None:
            selectedGlyphName = sender[index[0]]
            if selectedGlyphName in g.font:
                gg = g.font[selectedGlyphName]
                OpenGlyphWindow(gg) # Open the window or change to

    # Interaction with the right lists
   
    def baseGlyphsRightCallback(self, sender):
        index = sender.getSelection()
        g = CurrentGlyph()
        if index and g is not None:
            selectedGlyphName = sender[index[0]]
            if selectedGlyphName in g.font:
                self.w.similarGlyphsRight.set(self.base1.get(selectedGlyphName, []))
                
    def openBaseGlyphsRightCallback(self, sender):
        index = sender.getSelection()
        g = CurrentGlyph()
        if index and g is not None:
            selectedGlyphName = sender[index[0]]
            if selectedGlyphName in g.font:
                gg = g.font[selectedGlyphName]
                OpenGlyphWindow(gg) # Open the window or change to

    def similarGlyphsRightCallback(self, sender):
        pass

    def openSimilarGlyphsRightCallback(self, sender):
        index = sender.getSelection()
        g = CurrentGlyph()
        if index and g is not None:
            selectedGlyphName = sender[index[0]]
            if selectedGlyphName in g.font:
                gg = g.font[selectedGlyphName]
                OpenGlyphWindow(gg) # Open the window or change to
    
    def spaceCallback(self, sender):
        """Try spacing and kerning @f."""
        f = CurrentFont()
        km = self.getKerningManager(f)
        print(f'--- Similarity/KernNet spacing for {f.path}')
        # Run through the left list of base glyphs
        # Check that none of them have components (or otherwise the order of setting the side gets really important).
        baseGlyphs = sorted(self.w.baseGlyphsLeft.get())
        done = set()
        for baseName2 in baseGlyphs:
            base = f[baseName2]
            if base.components:
                print(f'### Base for left has {len(base.components)} components {baseName2}')
                continue
            # First do all glyphs without components, because the component glyphs may get altered too
            for gName in sorted(km.getSimilarNames2(base)):
                g = f[gName]
                if g.components or gName in baseGlyphs or gName in done:
                    continue
                if abs(base.angledLeftMargin - g.angledLeftMargin) > 1:
                    print(f'... Set left margin /{baseName2} {round(base.angledLeftMargin)} --> /{gName} {round(g.angledLeftMargin)}')
                    g.angledLeftMargin = base.angledLeftMargin
                    g.changed()
                done.add(gName)
            # Then do all glyphs with components
            for gName in sorted(km.getSimilarNames2(base)):
                g = f[gName]
                if not g.components or gName in baseGlyphs or gName in done:
                    continue
                if abs(base.angledLeftMargin - g.angledLeftMargin) > 1:
                    print(f'... Set left margin /{baseName2} {round(base.angledLeftMargin)} --> /{gName} {round(g.angledLeftMargin)}')
                    g.angledLeftMargin = base.angledLeftMargin
                    g.changed()
                done.add(gName)

        baseGlyphs = sorted(self.w.baseGlyphsRight.get())
        done = set()
        for baseName1 in baseGlyphs:
            base = f[baseName1]
            if base.components:
                print(f'### Base for right has {len(base.components)} components {baseName1}')
                continue
            # First do all glyphs without components, because the component glyphs may get altered too
            for gName in sorted(km.getSimilarNames1(base)):
                g = f[gName]
                if g.components or gName in baseGlyphs or gName in done:
                    continue
                if abs(base.angledRightMargin - g.angledRightMargin) > 1:
                    print(f'... Set right margin /{baseName1} {round(base.angledRightMargin)} --> /{gName} {round(g.angledRightMargin)}')
                    g.angledRightMargin = base.angledRightMargin
                    g.changed()
                done.add(gName)
            # Then do all glyphs with components
            for gName in sorted(km.getSimilarNames1(base)):
                g = f[gName]
                if not g.components or gName in baseGlyphs or gName in done:
                    continue
                if abs(base.angledRightMargin - g.angledRightMargin) > 1:
                    print(f'... Set right margin /{baseName1} {round(base.angledRightMargin)} --> /{gName} {round(g.angledRightMargin)}')
                    g.angledRightMargin = base.angledRightMargin
                    g.changed()
                done.add(gName)
               
    def predictKerning(self, f, gName1, gName2):
        """Generate a kerning test image for the based of the groups that gName1 and gName2 are in.
        If there is no group for those glyphs, then use the glyphs themselves."""
        f = CurrentFont()     
        km = self.getKerningManager(f)       
        imageName = 'test.png'
        kernImagePath = '/'.join(__file__.split('/')[:-1]) + '/assistantLib/kernnet/_imagePredict/' + imageName
        iw = ih = 32
        r = 12
        r2 = 2*r
        scale = ih/f.info.unitsPerEm
        y = -f.info.descender 

        drawBot.newDrawing()
        drawBot.newPage(iw, ih)
        drawBot.fill(0)

        # Experimental: Try equalize left and right part of the image
        drawBot.rect(0, 0, iw*1/6, ih)
        drawBot.rect(iw*5/6, 0, iw*1/6, ih)    
        
        drawBot.scale(scale)
        drawBot.save()

        # Use the base of the group instead of gName1 itself for more consistent result of the AI-kerning
        # bewtween the different glyphs in on group.
        g = f[gName1]
        g1 = km.getRightMarginGroupBaseGlyph(g)
        if g1 is None:
            g1 = g
        path1 = g1.getRepresentation("defconAppKit.NSBezierPath")
        drawBot.translate(iw/2/scale-g1.width, y)
        drawBot.drawPath(path1)
        drawBot.restore()        
        drawBot.save()
        # Use the base of the group instead of gName1 itself for more consistent result of the AI-kerning
        # bewtween the different glyphs in on group.
        g = f[gName2]
        g2 = km.getLeftMarginGroupBaseGlyph(g)
        if g2 is None: # Not part of any group
            g2 = g
        path2 = g2.getRepresentation("defconAppKit.NSBezierPath")
        drawBot.translate(iw/2/scale, y)
        drawBot.drawPath(path2)
        
        drawBot.saveImage(kernImagePath)
        
        import urllib.request
        page = urllib.request.urlopen(f'http://localhost:8080/{g1.name}/{g2.name}/{imageName}')
        
        # For some reason, predicted kerning seems to be best when subrachting this amount
        # Value is for 1000 EM.
        CALIBRATE = 1 #.4 #-36 
        # Returns value is glyphName1/glyphName2/predictedKerningValue
        # The glyph names are returned to check validity of the kerning value.
        # Since the call is ansynchronic to the server, we may get the answer here from a previous query.
        parts = str(page.read())[2:-1].split('/')
        print('@@@', parts)
        if not len(parts) == 3 or parts[0] != g1.name or parts[1] != g2.name:
            print('### Predicted kerning query not value', parts)
            return None
        
        #print('Predicted kerning', ss, len(ss), int(ss[2:-1]))
        #print('===', int(str(page.read())[2:-1]))
        unit = 4
        k = float(parts[-1])
        kk = int(round(k * f.info.unitsPerEm/1000/unit))*unit # Scale the kerning value to our Em-size.  
        #kk = int(round(k * CALIBRATE/4))*4
        if abs(kk) <= unit:
            kk = 0 # Apply threshold for very small kerning values
        print(f'... Predicted kerning {g1.name} {(gName1)} -- {g2.name} {(gName2)} k={k} kk={kk}')
            
        return kk
                            
if __name__ == '__main__':
    ss = SimilarSpacer()
  