# -*- coding: UTF-8 -*-
#
#    Similar Assistant for RoboFont4
#    It works on the current font.
#
# 
if 0:
    import sys
    import os
    import codecs
    import merz
    import weakref
    import importlib
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
    
from assistantLib.tp_kerningManager import KerningManager, SPACING_TYPES_LEFT, SPACING_TYPES_RIGHT

W, H = 400, 300
M = 20
BW = 200 - 2*M # Button width
BH = 24 # Button height

BASE = [ # Glyph nanes that are used as base for the seeds for the similarity checks
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    
    'period',
    
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

]
BBB = [
    'Iegrave-cy', 'Io-cy', 'Dje-cy', 'Gje-cy', 'E-cy', 'Dze-cy', 'I-cy', 'Yi-cy', 'Je-cy', 'Lje-cy', 'Nje-cy', 'Tshe-cy', 'Kje-cy', 'Iigrave-cy', 'Ushort-cy', 'Dzhe-cy', 
    'A-cy', 'Be-cy', 'Ve-cy', 'Ge-cy', 'De-cy', 'Ie-cy', 'Zhe-cy', 'Ze-cy', 'Ii-cy', 'Iishort-cy', 'Ka-cy', 'El-cy', 'Em-cy', 'En-cy', 'O-cy', 'Pe-cy', 'Er-cy', 'Es-cy', 
    'Te-cy', 'U-cy', 'Ef-cy', 'Ha-cy', 'Tse-cy', 'Che-cy', 'Sha-cy', 'Shcha-cy', 'Hardsign-cy', 'Yeru-cy', 'Softsign-cy', 'Ereversed-cy', 'Iu-cy', 'Ia-cy', 
    
    'a-cy', 'be-cy', 've-cy', 'ge-cy', 'de-cy', 'ie-cy', 'zhe-cy', 'ze-cy', 'ii-cy', 'iishort-cy', 'ka-cy', 'el-cy', 'em-cy', 'en-cy', 'o-cy', 'pe-cy', 'er-cy', 
    'es-cy', 'te-cy', 'u-cy', 'ef-cy', 'ha-cy', 'tse-cy', 'che-cy', 'sha-cy', 'shcha-cy', 'hardsign-cy', 'yeru-cy', 'softsign-cy', 'ereversed-cy', 'iu-cy', 
    'ia-cy', 'iegrave-cy', 'io-cy', 'dje-cy', 'gje-cy', 'e-cy', 'dze-cy', 'i-cy', 'yi-cy', 'je-cy', 'lje-cy', 'nje-cy', 'tshe-cy', 'kje-cy', 'iigrave-cy', 
    'ushort-cy', 'dzhe-cy', 'Omega-cy', 'omega-cy', 'Yat-cy', 'yat-cy', 'Eiotified-cy', 'eiotified-cy', 'Yuslittle-cy', 'yuslittle-cy', 'Yuslittleiotified-cy', 
    'yuslittleiotified-cy', 'Yusbig-cy', 'yusbig-cy', 'Yusbigiotified-cy', 'yusbigiotified-cy', 'Ksi-cy', 'ksi-cy',

    'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',    
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigmafinal', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
]
class SimilarSpacer:

    def __init__(self):
        self.kerningManagers = {}
        self.kerningSample = None

        x = M
        y = H - M - BH
        self.w = Window((W, H), self.__class__.__name__, minSize=(W, H))
        self.w.spaceButton = Button((x, y, BW, BH), 'Space', callback=self.spaceCallback)
        
        self.w.open()
        
    def spaceCallback(self, sender):
        """Try spacing and kerning @f."""
        f = CurrentFont()
        print(f'--- Similarity/KernNet spacing for {f.path}')
        km = self.getKerningManager(f)
        similarSeeds1 = {}
        similarXRef1 = {}
        similarSeeds2 = {}
        similarXRef2 = {}
        for gName in BASE:
            g = f[gName]
            if gName not in similarXRef1:
                similarGlyphs1 = km.getSimilarGroupsNames1(g)
                if gName not in similarSeeds1:
                    similarSeeds1[gName] = set([gName])
                for gName1 in similarGlyphs1:
                    similarSeeds1[gName].add(gName1)
                    similarXRef1[gName1] = gName 
            
            if gName not in similarXRef2:
                similarGlyphs2 = km.getSimilarGroupsNames2(g)
                if gName not in similarSeeds2:
                    similarSeeds2[gName] = set([gName])
                for gName2 in similarGlyphs2:
                    similarSeeds2[gName].add(gName2)
                    similarXRef2[gName2] = gName 
                    
        print(f'similarSeeds1 {len(similarSeeds1)}')
        print(f'similarSeeds2 {len(similarSeeds2)}')
    
        if 0:
            for g in f:
                if g.name not in similarXRef1:
                    print('... Missing 1:', g.name)
                
            for g in f:
                if g.name not in similarXRef2:
                    print('... Missing 2:', g.name)
                
    def getKerningManager(self, f):
        if f.path:
            if f.path not in self.kerningManagers:
                self.kerningManagers[f.path] = KerningManager(f, sample=self.kerningSample) #  First sample will be initialzed, others will be copied
            km = self.kerningManagers[f.path]
            self.kerningSample = km.sample
            return km
        return None
         
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
  