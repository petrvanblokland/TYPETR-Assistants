# -*- coding: UTF-8 -*-
#
#    Assisting the placement of anchors, showing diacritics clouds
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

#WindowClass = Window
WindowClass = FloatingWindow

# Add paths to libs in sibling repositories
PATHS = ['../TYPETR-Assistants/']
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

W, H = 400, 300
M = 20
FAR = 100000 # Put drawing stuff outside the window
MAX_DIACRITICS = 150
MAX_ANCHORS = 10
ANCHOR_MARKER_R = 48 # Radius of an anchor marker
ANCHOR_LOCKED_COLOR = (207/256, 207/256, 15/256, 0.5)
ANCHOR_UNLOCKED_COLOR = (15/256, 256/256, 15/256, 0.6)
ANCHOR_MARKER_STROKE = (207/256, 0, 0, 0.8)

VISITED_MARKER = (15/256, 174/256, 207/256, 1)
DIACRITICS_COLOR = (0.1, 0.1, 0.8, 0.1)
DIACRITICS_SELECTED_COLOR = (0.5, 0.1, 0.8, 0.5)

LIB_KEY = 'TYPETR-AnchorAssistant' # Key to store application settings in the glyph.lib

def getLib(g):
    """Get the dictionary of flags that is stored in g.lib"""
    if not LIB_KEY in g.lib:
        g.lib[LIB_KEY] = {}
    return g.lib[LIB_KEY]

class FontData:
    def __init__(self, f):
        """Build X-ref data from the font. Don't store the font itself, as it may be closed by the calling application."""
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
    
assistant = None # Little cheat, to make the assistant available from the window
        
class AnchorAssistant(Subscriber):

    def build(self):
        global assistant
        assistant = self

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
    
        # Define Merz drawing components.
        self.diacriticsCloud = [] # Cloud of found diacritics, that may fit individual anchors. 
        for n in range(MAX_DIACRITICS):
            self.diacriticsCloud.append(self.backgroundContainer.appendPathSublayer(
                name='diacriticsCloud%d' % n,
                position=(FAR, 0),
                fillColor=DIACRITICS_COLOR, # Opaque diacritics cloud
            ))

        self.anchorMarkers = [] # Larger colored circle markers around the anchor to make them better visible.
        for n in range(MAX_ANCHORS):
            self.anchorMarkers.append(self.backgroundContainer.appendOvalSublayer(name="anchorMarkers%d" % n,
                position=(FAR, 0),
                size=(ANCHOR_MARKER_R*2, ANCHOR_MARKER_R*2),
                fillColor=ANCHOR_LOCKED_COLOR,
                strokeColor=ANCHOR_MARKER_STROKE,
                strokeWidth=1,
            ))
    
    def getFontData(self, f):
        """Answer the cached FontData instance. If it does not exist, create it and let it in mine X-refs from the @f. 
        Don't store the font itself, as it may get closed by the applications."""
        if not f.path in self.fontDatas:
            self.fontDatas[f.path] = FontData(f) # Make a FontData instance with X-ref data of the font.
        return self.fontDatas[f.path]

    #self.glyphEditorGlyphDidChange(info)
    #self.glyphEditorGlyphDidChangeInfo(info)
    #self.glyphEditorGlyphDidChangeOutline(info)
    #self.glyphEditorGlyphDidChangeComponents(info)
    #self.glyphEditorGlyphDidChangeAnchors(info)
    #self.glyphEditorGlyphDidChangeGuidelines(info)
    #self.glyphEditorGlyphDidChangeImage(info)
    #self.glyphEditorGlyphDidChangeMetrics(info)
    #self.glyphEditorGlyphDidChangeContours(info)

    def glyphEditorDidMouseDown(self, info):
        #event = extractNSEvent(info['NSEvent'])
        g = info['glyph']
        if g is None:
            return
        self.updateCloud(g)
            
    def glyphEditorGlyphDidChange(self, info):
        """The editor selected another glyph. Update the visible Merz elements for the new glyph."""
        g = info['glyph']
        self.getAnchorLocks(g)
        self.updateCloud(g)
           
    def glyphEditorDidSetGlyph(self, info):
        """The editor selected another glyph. Update the visible Merz elements for the new glyph."""
        g = info['glyph'] # Get the current glyph
        #fd = self.getFontData(g.font)
        #print(g.name, fd.components)
        #print('-----', fd.glyphAnchors)
        #print('-----', fd.unicodes)
        # Set the markColor for this glyphs, since it was visited.
        if g.markColor != VISITED_MARKER: # NO_MARKER
            g.markColor = VISITED_MARKER

        self.getAnchorLocks(g) # Get the anchor locking flag from the g.lib[self.LIB_KEY]
        self.updateCloud(g)
        self.update(g)
         
    def getAnchorLocks(self, g):
        """Update the anchor lock checkboxes from info stored in the glyph.lib"""
        d = getLib(g)
        for a in g.anchors:
            if a.name == 'top':
                self.controller.w.lockAnchorTop.set(d.get(a.name, False))
                self.controller.w.useBaseAnchorTopX.set(d.get('useBaseAnchorTopX', True))
                self.controller.w.useBaseAnchorTopY.set(d.get('useBaseAnchorTopY', True))
            elif a.name == 'middle':
                self.controller.w.lockAnchorMiddle.set(d.get(a.name, False))
                self.controller.w.useBaseAnchorMiddleX.set(d.get('useBaseAnchorMiddleX', True))
                self.controller.w.useBaseAnchorMiddleY.set(d.get('useBaseAnchorMiddleY', True))
            elif a.name == 'bottom':
                self.controller.w.lockAnchorBottom.set(d.get(a.name, False))
                self.controller.w.useBaseAnchorBottomX.set(d.get('useBaseAnchorBottomX', True))
                self.controller.w.useBaseAnchorBottomY.set(d.get('useBaseAnchorBottomY', True))
            elif a.name == 'dot':
                self.controller.w.lockAnchorDot.set(d.get(a.name, False))
                self.controller.w.useBaseAnchorDotX.set(d.get('useBaseAnchorDotX', True))
                self.controller.w.useBaseAnchorDotY.set(d.get('useBaseAnchorDotY', True))
            elif a.name == 'ogonek':
                self.controller.w.lockAnchorOgonek.set(d.get(a.name, False))
                self.controller.w.useBaseAnchorOgonekX.set(d.get('useBaseAnchorOgonekX', True))
                self.controller.w.useBaseAnchorOgonekY.set(d.get('useBaseAnchorOgonekY', True))
            elif a.name == 'vert':
                self.controller.w.lockAnchorVert.set(d.get(a.name, False))
                self.controller.w.useBaseAnchorVertX.set(d.get('useBaseAnchorVertX', True))
                self.controller.w.useBaseAnchorVertY.set(d.get('useBaseAnchorVertY', True))
        # Use baseGlyph for positioning anchors
        self.controller.w.centerOnBounds.set(d.get('centerOnBounds', False))

    def saveAnchorLocks(self, g):
        """Save the anchor lock checkboxes info stored in the glyph.lib"""
        d = getLib(g)
        d['top'] = self.controller.w.lockAnchorTop.get()
        d['useBaseAnchorTopX'] = self.controller.w.useBaseAnchorTopX.get()
        d['useBaseAnchorTopY'] = self.controller.w.useBaseAnchorTopY.get()

        d['middle'] = self.controller.w.lockAnchorMiddle.get()
        d['useBaseAnchorMiddleX'] = self.controller.w.useBaseAnchorMiddleX.get()
        d['useBaseAnchorMiddleY'] = self.controller.w.useBaseAnchorMiddleY.get()
        
        d['bottom'] = self.controller.w.lockAnchorBottom.get()
        d['useBaseAnchorBottomX'] = self.controller.w.useBaseAnchorBottomX.get()
        d['useBaseAnchorBottomY'] = self.controller.w.useBaseAnchorBottomY.get()
        
        d['dot'] = self.controller.w.lockAnchorDot.get()
        d['useBaseAnchorDotX'] = self.controller.w.useBaseAnchorDotX.get()
        d['useBaseAnchorDotY'] = self.controller.w.useBaseAnchorDotY.get()
        
        d['ogonek'] = self.controller.w.lockAnchorOgonek.get()
        d['useBaseAnchorOgonekX'] = self.controller.w.useBaseAnchorOgonekX.get()
        d['useBaseAnchorOgonekY'] = self.controller.w.useBaseAnchorOgonekY.get()

        d['vert'] = self.controller.w.lockAnchorVert.get()
        d['useBaseAnchorVertX'] = self.controller.w.useBaseAnchorVertX.get()
        d['useBaseAnchorVertY'] = self.controller.w.useBaseAnchorVertY.get()

        # Use baseGlyph for positioning anchors
        d['centerOnBounds'] = self.controller.w.centerOnBounds.get()
                                           
    def _updateAnchorPosition(self, aIndex, g, a, bounds):
        """Try to guess the anchor position, based the position of outlines. The user can lock the anchor if manual changes were done."""
        fd = self.getFontData(g.font)
        if g.components: # Better to use the bounds of the base compobent glyph?
            gg = g.font[g.components[0].baseGlyph]
            gBound = gg.bounds
        else:
            gg = gBounds = None
            
        xMin, yMin, xMax, yMax = bounds
        ml = g.angledLeftMargin
        mr = g.angledRightMargin
        f = g.font
        d = getLib(g)
        changed = False
                
        if not a.name:
            return # New or undefined anchor: ignore until it gets name.
        elif a.name == 'top' and not d.get(a.name): # Try to fit it on xHeight - 16. Otherwise fit to highest y.
            x = y = None # Try to guess the values to fill in.
            if gg is not None: # There is a base 
                baseAnchors = fd.glyphAnchors.get(gg.name)
                if baseAnchors is not None and a.name in baseAnchors:  
                    bx, by = baseAnchors[a.name]
                    if d.get('useBaseAnchorTopX'):
                        x = bx
                    if d.get('useBaseAnchorTopY'):
                        y = by
                                
            if y is None: # Not filled yet?
                if f.info.capHeight - 100 < yMax < f.info.capHeight + 100: # Probably diacritics
                    y = f.info.capHeight - 16
                else:
                    y = int(round(f.info.xHeight - 16))
            if x is None:
                x = int(round(ml + (g.width - mr - ml)/2) + y*tan(radians(-g.font.info.italicAngle or 0)))
            if abs(a.x - x) >= 1 or abs(a.y - y) >= 1: # Did it change from the current position of the anchor?
                print(f'... Move /{g.name} anchor {a.name} to {(x, y)}')
                a.x = x
                a.y = y
                changed = True
                
        elif a.name == 'middle' and not d.get(a.name): # Try to fit it on baseline + 16. Otherwise fit to lowest y.
            x = y = None # Try to guess the values to fill in.
            if gg is not None: # There is a base 
                baseAnchors = fd.glyphAnchors.get(gg.name)
                if baseAnchors is not None and a.name in baseAnchors:  
                    bx, by = baseAnchors[a.name]
                    if d.get('useBaseAnchorMiddleX'):
                        x = bx
                    if d.get('useBaseAnchorMiddleY'):
                        y = by
            if y is None: # Not filled yet?
                if f.info.capHeight - 100 < yMax < f.info.capHeight + 100: # Probably diacrtics
                    y = int(round(f.info.capHeight/2))
                else:
                    y = int(round(f.info.xHeight/2))
            if x is None:
                x = int(round(ml + (g.width - mr - ml)/2) + y*tan(radians(-g.font.info.italicAngle or 0)))
            if abs(a.x - x) >= 1 or abs(a.y - y) >= 1:
                print(f'... Move /{g.name} anchor {a.name} to {(x, y)}')
                a.x = x
                a.y = y
                changed = True
                
        elif a.name == 'bottom' and not d.get(a.name): # Try to fit it on baseline + 16. Otherwise fit to lowest y.
            x = y = None # Try to guess the values to fill in.
            if gg is not None: # There is a base 
                baseAnchors = fd.glyphAnchors.get(gg.name)
                if baseAnchors is not None and a.name in baseAnchors:  
                    bx, by = baseAnchors[a.name]
                    if d.get('useBaseAnchorBottomX'):
                        x = bx
                    if d.get('useBaseAnchorBottomY'):
                        y = by
            if y is None: # Not filled yet?
                if yMin > -16:
                    y = 16
                else:
                    y = yMin + 16
            if x is None:
                x = int(round(ml + (g.width - mr - ml)/2) + y*tan(radians(-g.font.info.italicAngle or 0)))
            if abs(a.x - x) >= 1 or abs(a.y - y) >= 1:
                print(f'... Move /{g.name} anchor {a.name} to {(x, y)}')
                a.x = x
                a.y = y
                changed = True
                
        elif a.name == 'dot' and not d.get(a.name): # Try to fit it on baseline + 16. Otherwise fit to lowest y.
            if f.info.capHeight - 100 < yMax < f.info.capHeight + 100: # Probably diacrtics
                y = int(round(f.info.capHeight/2))
            else:
                y = int(round(f.info.xHeight/2))
            x = int(round(ml + (g.width - mr - ml)/2) + 32 + y*tan(radians(-g.font.info.italicAngle or 0)))
            if abs(a.x - x) >= 1 or abs(a.y - y) >= 1:
                print(f'... /{g.name} Move anchor {a.name} to {(x, y)}')
                a.x = x
                a.y = y
                changed = True
                
        elif a.name == 'ogonek' and not d.get(a.name): # Try to fit it on xHeight - 16. Otherwise fit to highest y.
            y = 16
            x = int(round(ml + (g.width - mr - ml)*0.75) + y*tan(radians(-g.font.info.italicAngle or 0)))
            if abs(a.x - x) >= 1 or abs(a.y - y) >= 1:
                print(f'... /{g.name} Move anchor {a.name} to {(x, y)}')
                a.x = x
                a.y = y
                changed = True
                
        elif a.name == 'vert' and not d.get(a.name): # Try to fit it on xHeight - 16. Otherwise fit to highest y.
            y = 1570
            x = int(round(g.width - mr + y*tan(radians(-g.font.info.italicAngle or 0))))
            if abs(a.x - x) >= 1 or abs(a.y - y) >= 1:
                print(f'... /{g.name} Move anchor {a.name} to {(x, y)}')
                a.x = x
                a.y = y
                changed = True
                
        if d.get(a.name):
            anchorColor = ANCHOR_UNLOCKED_COLOR 
        else:
            anchorColor = ANCHOR_LOCKED_COLOR
        self.anchorMarkers[aIndex].setFillColor(anchorColor)
        self.anchorMarkers[aIndex].setPosition((a.x - ANCHOR_MARKER_R, a.y - ANCHOR_MARKER_R))
        
        if changed:
            g.changed()
                 
    def updateCloud(self, g):
        """Update the position of related diacritics and place the anchor marker on their position"""
        if not g.contours and not g.components:
            # Nothing to fix here on diacritics and anchorsl
            return
        fd = self.getFontData(g.font)
        bounds = g.bounds # Cache the retangle, since we need it for each a anchor
        dIndex = 0 # Index to Merz diacritics objects
        aIndex = 0
        for a in g.anchors: # For all anchors, show the cloud related diacritics for that anchor
            self._updateAnchorPosition(aIndex, g, a, bounds)

            if a.selected:
                fillColor = DIACRITICS_SELECTED_COLOR
            else:
                fillColor = DIACRITICS_COLOR
            
            if not a.name.startswith('_') and '_' + a.name in fd.anchors:
                for refName in fd.anchors['_' + a.name]:
                    if dIndex < MAX_DIACRITICS: # Still slots available?
                        #print(refName, fd.glyphAnchors[refName])
                        diacriticsGlyph = g.font[refName]
                        refX, refY = fd.glyphAnchors[refName]['_' + a.name] 
                        #print(g.name, refName, refX, refY, a.name, a.x, a.y)
                        y = a.y - refY
                        x = a.x - refX #+ tan(radians(-g.font.info.italicAngle or 0)) * y # Correct for italic angle offset in x
                        self.diacriticsCloud[dIndex].setPath(diacriticsGlyph.getRepresentation("merz.CGPath"))
                        self.diacriticsCloud[dIndex].setPosition((x, y))
                        self.diacriticsCloud[dIndex].setFillColor(fillColor)
                        dIndex += 1 #  We used a slot for the diacritics
            aIndex += 1
            
        for n in range(dIndex, MAX_DIACRITICS):
            self.diacriticsCloud[n].setPosition((FAR, 0))
        for n in range(aIndex, MAX_ANCHORS):
            self.anchorMarkers[n].setPosition((FAR, 0))
                    
    def update(self, g):
        fd = self.getFontData(g.font) # Mainly to make sure that the FontData instance exists.
        
        
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/2
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
BH = 24 # Button height

class AnchorAssistantController(WindowController):

    assistantGlyphEditorSubscriberClass = AnchorAssistant
    
    NAME = 'Anchor Assistant'

    def build(self):        

        f = CurrentFont()

        y = M
        self.w = WindowClass((50, 50, W, H), self.NAME, minSize=(W, H))

        y = M
        self.w.lockAnchorTop = CheckBox((M, y, CW, 24), 'Lock anchor Top', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorTopX = CheckBox((CW + M, y, 36, 24), 'X', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorTopY = CheckBox((CW + M + 36, y, CW, 24), 'Y Use base', callback=self.updateAnchorCallback)
        y += L
        self.w.lockAnchorMiddle = CheckBox((M, y, CW, 24), 'Lock anchor Middle', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorMiddleX = CheckBox((CW + M, y, 36, 24), 'X', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorMiddleY = CheckBox((CW + M + 36, y, CW, 24), 'Y Use base', callback=self.updateAnchorCallback)
        y += L
        self.w.lockAnchorBottom = CheckBox((M, y, CW, 24), 'Lock anchor Bottom', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorBottomX = CheckBox((CW + M, y, 36, 24), 'X', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorBottomY = CheckBox((CW + M + 36, y, CW, 24), 'Y Use base', callback=self.updateAnchorCallback)
        y += L
        self.w.lockAnchorDot = CheckBox((M, y, CW, 24), 'Lock anchor Dot', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorDotX = CheckBox((CW + M, y, 36, 24), 'X', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorDotY = CheckBox((CW + M + 36, y, CW, 24), 'Y Use base', callback=self.updateAnchorCallback)
        y += L
        self.w.lockAnchorOgonek = CheckBox((M, y, CW, 24), 'Lock anchor Ogonek', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorOgonekX = CheckBox((CW + M, y, 36, 24), 'X', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorOgonekY = CheckBox((CW + M + 36, y, CW, 24), 'Y Use base', callback=self.updateAnchorCallback)
        y += L
        self.w.lockAnchorVert = CheckBox((M, y, CW, 24), 'Lock anchor Vert', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorVertX = CheckBox((CW + M, y, 36, 24), 'X', callback=self.updateAnchorCallback)
        self.w.useBaseAnchorVertY = CheckBox((CW + M + 36, y, CW, 24), 'Y Use base', callback=self.updateAnchorCallback)

        y += L * 2
        self.w.centerOnBounds = CheckBox((M, y, CW, 24), 'Center on width', value=True, callback=self.updateAnchorCallback)

        y = H - M - BH
        self.w.fixAllButton = Button((M, y, CW, BH), 'Fix all', callback=self.fixAllButtonCallback)
        
        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None

    def updateAnchorCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            assistant.saveAnchorLocks(g)
            g.changed()
    
    def fixAllButtonCallback(self, sender):
        g = CurrenGlyph()
        for gg in g.font:
            pass
                    
if __name__ == '__main__':
    OpenWindow(AnchorAssistantController)
