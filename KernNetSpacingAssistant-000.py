# -*- coding: UTF-8 -*-
#
#    Template to build Assistants
#    It works on the current font.
#
# 
import sys
import importlib
from math import *
import urllib.request

from vanilla import *
import drawBot

from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

import assistantLib
importlib.reload(assistantLib)

# Decide on the type of window for the Assistant.
WindowClass = Window # Will hide behind other windows, if not needed.
#WindowClass = FloatingWindow # Is always available, but it can block the view of other windows if the Asistant window grows in size.

# Add paths to libs in sibling repositories. The assistantLib module contains generic code for Asistanta.s
PATHS = ['../TYPETR-Assistants/']
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

W, H = 400, 300
M = 20
BW = 200 - 2*M # Button width
BH = 24 # Button height
FAR = 100000 # Put drawing stuff outside the window
MAX_DIACRITICS = 150

KERN_GLYPH_COLOR = (0, 0, 0, 0.7)

class FontData:
    def __init__(self, f):
        """Build X-ref data from the from. Don't store the font itself, as it may be close by the calling application."""
        self.path = f.path
        # Fins all glyphs that use this glyph as component
        self.base = {} # Key is glyphName. Value is list of component.baseGlyph names
        # Find all diacritics and match them with the referring glyphs.
        self.diacritics = {} # Key is diacritics name. Value is list of glyph names that use this diacritic as component.
        # All glyphs that are in the same cloud of diacritics (affected by the position of the same anchor)
        self.diacriticsCloud = {} # Key is glyhName
        # All glyphs usage of anchors
        self.glyphAnchors = {} # Key is glyphName, Value is dict of ancbhor.name --> (x, y).
        self.anchors = {} # Key is anchor name. Value is list of glyphs that use this anchor
        # Unicode --> Glyph name
        self.unicodes = {} # Key is unicode (if it exists). Value is glyph name.
        for g in f:
            self.base[g.name] = [] # These glyphs have components refering to g.
            if g.name.endswith('cmb') or g.name.endswith('comb'):
                if g.unicode and g.name not in self.diacritics: # Only for real floating diacritics that have a unicode
                    self.diacritics[g.name] = []
        for g in f:
            self.base[g.name] = bb = []
            for component in g.components:
                bb.append(component.baseGlyph)
                if component.baseGlyph in self.diacritics: # Only for real diacritics (that have a unicode)
                    self.diacritics[component.baseGlyph].append(g.name)
                    
            # glyphName --> dict of anchors
            self.glyphAnchors[g.name] = aa = {}
            for a in g.anchors:
                aa[a.name] = a.x, a.y
                # anchorName --> List of glyph that are using it
                if a.name not in self.anchors:
                    self.anchors[a.name] = []
                self.anchors[a.name].append(g.name)
            if g.unicode:
                self.unicodes[g.unicode] = g.name
                                
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.path.split("/")[-1]}>'
            
class KernNetSpacingAssistant(Subscriber):

    def build(self):
        self.fontDatas = {} # Key is font path, value is FontData instance that holds mined X-ref data on the font.

        glyphEditor = self.getGlyphEditor()
        
        self.foregroundContainer = container = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )

        self.kernGlyphImage1 = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage1',
            position=(FAR, 0),
            fillColor=KERN_GLYPH_COLOR, # Opaque diacritics cloud
        )
        self.kernGlyphImage = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage',
            position=(FAR, 0),
            fillColor=KERN_GLYPH_COLOR, # Sets to light gray if not equal to current glyph.
        )
        self.kernGlyphImage2 = self.backgroundContainer.appendPathSublayer(
            name='kernGlyphImage2',
            position=(FAR, 0),
            fillColor=KERN_GLYPH_COLOR, # Opaque diacritics cloud
        )
        self.kerning1Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning1Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning1Value.setHorizontalAlignment('center')
        self.kerning2Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning2Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning2Value.setHorizontalAlignment('center')

        #self.glyphEditorGlyphDidChange(info)
        #self.glyphEditorGlyphDidChangeInfo(info)
        #self.glyphEditorGlyphDidChangeOutline(info)
        #self.glyphEditorGlyphDidChangeComponents(info)
        #self.glyphEditorGlyphDidChangeAnchors(info)
        #self.glyphEditorGlyphDidChangeGuidelines(info)
        #self.glyphEditorGlyphDidChangeImage(info)
        #self.glyphEditorGlyphDidChangeMetrics(info)
        #self.glyphEditorGlyphDidChangeContours(info)

    def getFontData(self, f):
        """Answer the cached FontData instance. If it does not exist, create it and let it in mine X-refs from the @f. """
        if not f.path in self.fontDatas:
            self.fontDatas[f.path] = FontData(f)
        return self.fontDatas[f.path]
    
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        self.update(g)
           
    def glyphEditorDidSetGlyph(self, info):
        g = info['glyph']
        #fd = self.getFontData(g.font)
        #print(g.name, fd.components)
        #print('-----', fd.glyphAnchors)
        #print('-----', fd.unicodes)
        self.update(g)
                    
    def update(self, g):
        self.autoMargins(g)
        gName1 = self.controller.w.kerningGlyph1.get()
        gName2 = self.controller.w.kerningGlyph2.get()
        self.autoKern(gName1, g, gName2)
        
    def autoMargins(self, g):
        """Try to guess what the margins for @h should be, based on the Similarity groups and on /H/H kerning == 0."""
        
    def autoKern(self, gName1, g, gName2):
        k1 = k2 = 0
        f = g.font
        if gName1 and gName1 in f:
            g1 = f[gName1]
            k1 = self.getKernNetKerning(g1, g)
            self.kernGlyphImage1.setPath(g1.getRepresentation("merz.CGPath"))
            self.kernGlyphImage1.setPosition((-g1.width - k1, 0))
        else:
            self.kernGlyphImage1.setPosition((FAR, 0))
                        
        self.kernGlyphImage.setPath(g.getRepresentation("merz.CGPath"))
        self.kernGlyphImage.setPosition((0, 0))

        if gName2 and gName2 in f:
            g2 = f[gName2]
            k2 = self.getKernNetKerning(g, g2)
            self.kernGlyphImage2.setPath(g2.getRepresentation("merz.CGPath"))
            self.kernGlyphImage2.setPosition((g.width + k1, 0))
        else:
            self.kernGlyphImage2.setPosition((FAR, 0))

        y4 = -150 # Position of current kerning values

        if k1 < 0:
            kernColor = 1, 0, 0, 1
        if k1 > 0:
            kernColor = 0, 0.5, 0, 1
        else:
            kernColor = 0.6, 0.6, 0.6, 1
        self.kerning1Value.setFillColor(kernColor)
        self.kerning1Value.setPosition((k1, y4))
        self.kerning1Value.setText(f'{k1}')
            
        if k2 < 0:
            kernColor = 1, 0, 0, 1
        if k2 > 0:
            kernColor = 0, 0.5, 0, 1
        else:
            kernColor = 0.6, 0.6, 0.6, 1
        self.kerning2Value.setFillColor(kernColor)
        self.kerning2Value.setPosition((g.width + k2, y4))        
        self.kerning2Value.setText(f'{k2}')
        
    FACTOR = 0.8
    FACTOR = 1.5
    UNIT = 4
    
    def getKernNetKerning(self, g1, g2):
        """Gernerate the kerning test image.
        Answer the KernNet predicted kerning for @g1 amd @g2. This assumes the KernNet server to be running on localhost:8080"""
        f = g1.font
        imageName = 'test.png'
        kernImagePath = '/'.join(__file__.split('/')[:-1]) + '/assistantLib/kernnet3/_imagePredict/' + imageName
        iw = ih = 32
        scale = ih/f.info.unitsPerEm
        y = -f.info.descender 

        im1 = g1.getRepresentation("defconAppKit.NSBezierPath")
        im2 = g2.getRepresentation("defconAppKit.NSBezierPath")
        s = iw / g1.font.info.unitsPerEm
        y = -g1.font.info.descender

        #if abs(k) >= 4 and not os.path.exists(imagePath): # Ignore k == 0
        drawBot.newDrawing()
        drawBot.newPage(iw, ih)
        #drawBot.fill(1, 0, 0, 1)
        #drawBot.rect(0, 0, iw, ih)
        drawBot.fill(0)
        drawBot.scale(s, s)
        drawBot.save()
        drawBot.translate(iw/s/2 - g1.width, y)
        drawBot.drawPath(im1)
        drawBot.restore()
        drawBot.translate(iw/s/2, y)
        drawBot.drawPath(im2)
        drawBot.saveImage(kernImagePath)

        page = urllib.request.urlopen(f'http://localhost:8080/{g1.name}/{g2.name}/{imageName}')
        
        # Returns value is glyphName1/glyphName2/predictedKerningValue
        # The glyph names are returned to check validity of the kerning value.
        # Since the call is ansynchronic to the server, we may get the answer here from a previous query.
        parts = str(page.read())[2:-1].split('/')
        if not len(parts) == 3 or parts[0] != g1.name or parts[1] != g2.name:
            print('### Predicted kerning query not value', parts)
            return None
        k = float(parts[-1])
        print(k, k - abs(self.FACTOR * k), abs(self.FACTOR * k), int(round(k * f.info.unitsPerEm/1000/self.UNIT))*self.UNIT)
        k = k - abs(self.FACTOR * k)
        k = k * self.FACTOR
        
        # Calculate the rouned-truncated value of the floating         
        ki = int(round(k * f.info.unitsPerEm/1000/self.UNIT))*self.UNIT # Scale the kerning value to our Em-size.  
        if abs(ki) <= self.UNIT:
            ki = 0 # Apply threshold for very small kerning values
        print(f'... Predicted kerning {g1.name} -- {g2.name} k={k} kk={ki}')
            
        return ki
        
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
C2 = C1 + CW + M

class KernNetSpacingAssistantController(WindowController):

    assistantGlyphEditorSubscriberClass = KernNetSpacingAssistant
    
    NAME = 'KernNet Assistant'

    def build(self):        

        f = CurrentFont()

        y = M
        self.w = WindowClass((W, H), self.NAME, minSize=(W, H))

        self.w.kerningGlyph1 = EditText((C0, y, CW, L), callback=self.updateKerningCallback) # Use  kerning find button to go there.
        self.w.kerningGlyph2 = EditText((C1, y, CW, L), callback=self.updateKerningCallback)
        self.w.kerningGlyph1.set('T')
        self.w.kerningGlyph2.set('T')
        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None
                           
    def updateKerningCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            g.changed()
            
if __name__ == '__main__':
    OpenWindow(KernNetSpacingAssistantController)
