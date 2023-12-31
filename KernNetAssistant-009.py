# -*- coding: UTF-8 -*-
#
#    Template to build Assistants
#    It works on the current font.
#
# 
import sys
import importlib
from math import *

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
            
class AnchorAssistant(Subscriber):

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

        self.diacriticsCloud = []
        for n in range(MAX_DIACRITICS):
            self.diacriticsCloud.append(self.backgroundContainer.appendPathSublayer(
                name='diacriticsCloud%d' % n,
                position=(FAR, 0),
                fillColor=(0.1, 0.1, 0.8, 0.1), # Opaque diacritics cloud
            ))

    def getFontData(self, f):
        """Answer the cached FontData instance. If it does not exist, create it and let it in mine X-refs from the @f. """
        if not f.path in self.fontDatas:
            self.fontDatas[f.path] = FontData(f)
        return self.fontDatas[f.path]
    
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        self.updateCloud(g)
           
    def glyphEditorDidSetGlyph(self, info):
        g = info['glyph']
        #fd = self.getFontData(g.font)
        #print(g.name, fd.components)
        #print('-----', fd.glyphAnchors)
        #print('-----', fd.unicodes)
        self.updateCloud(g)
        self.update(g)

    def updateCloud(self, g):
        fd = self.getFontData(g.font)
        aIndex = 0 # Index to Merz objects
        for a in g.anchors: # For all anchors, show the cloud related diacritics for that anchor
            if not a.name.startswith('_') and '_' + a.name in fd.anchors:
                for refName in fd.anchors['_' + a.name]:
                    if aIndex < MAX_DIACRITICS: # Still slots available?
                        #print(refName, fd.glyphAnchors[refName])
                        diacriticsGlyph = g.font[refName]
                        refX, refY = fd.glyphAnchors[refName]['_' + a.name] 
                        #print(g.name, refName, refX, refY, a.name, a.x, a.y)
                        y = a.y - refY
                        x = a.x - refX #+ tan(radians(-g.font.info.italicAngle or 0)) * y # Correct for italic angle offset in x
                        self.diacriticsCloud[aIndex].setPath(diacriticsGlyph.getRepresentation("merz.CGPath"))
                        self.diacriticsCloud[aIndex].setPosition((x, y))
                        aIndex += 1 #  We used a slot
        for n in range(aIndex, MAX_DIACRITICS):
            self.diacriticsCloud[n].setPosition((FAR, 0))
                    
    def update(self, g):
        fd = self.getFontData(g.font)
        
        
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
C2 = C1 + CW + M

class AnchorAssistantController(WindowController):

    assistantGlyphEditorSubscriberClass = AnchorAssistant
    
    NAME = 'Anchor Assistant'

    def build(self):        

        f = CurrentFont()

        y = M
        self.w = WindowClass((W, H), self.NAME, minSize=(W, H))

        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None
                           
if __name__ == '__main__':
    OpenWindow(AnchorAssistantController)
