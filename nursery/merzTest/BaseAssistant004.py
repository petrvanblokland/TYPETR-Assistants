import vanilla
import merz
import weakref
from AppKit import (NSCommandKeyMask, NSShiftKeyMask, NSControlKeyMask, NSAlternateKeyMask,
        NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey)

from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber
from random import random
from mojo.canvas import CanvasGroup

WindowClass = vanilla.FloatingWindow
WindowClass = vanilla.Window

W, H = 600, 150
M = 32

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
BLUE = (0, 0, 0.5, 1)
RED = (1, 0, 0, 1)
GREEN = (0, 0.5, 0, 1)
GRAY = (0.5, 0.5, 0.5, 1)
LTGRAY = (0.8, 0.8, 0.8, 1)
EID = 0

# Sets of keys that his tool responds to
KEY_SPACE = ' '
KEY_NEWLINE = '\n'
KEY_RETURN = '\r'

class MerzElement:
    
    def __init__(self, name=None, parent=None):
        global EID
        self.eId = EID # Automatic element identifier
        EID += 1
        self.merzLayer = None # Merz layer of this element, to be defined by inheritig classes.
        # Element tree
        # Preset, so it exists for checking when appending parent.
        self._x = self._y = 0
        self._w = self._h = 100
        self._scale = None # Force to used scale of parent
        self.name = name or ('%s%d' % (self.__class__.__name__, self.eId)) # Optional name, can be None
        self.elements = []
        
        assert parent is None or isinstance(parent, MerzElement), ('### %s' % parent.__class__.__name__)
        # Add and set weakref to parent element or None, if it is the root.
        # Caller must add self to its elements separately. Set references
        # in both directions. Remove any previous parent links.
        self.parent = parent
        
    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if 0 < self.x < 1:
            s += ' x=%0.2f' % self.x
        else:
            s += ' x=%d' % self.x
        if 0 < self.y < 1:
            s += ' y=%0.2f' % self.y
        else:
            s += ' y=%d' % self.y
        if 0 < self.w < 1:
            s += ' w=%0.2f' % self.w
        else:
            s += ' w=%d' % self.w
        if 0 < self.h < 1:
            s += ' h=%0.2f' % self.h
        else:
            s += ' h=%d' % self.h
        if self.name is not None:
            s += ' name=%s' % self.name
        if self.parent is not None:
            s += ' parent=%s' % self.parent.name
        if len(self.elements):
            s += ' e=%d' % len(self.elements)
        return s + '>'
    
    def printTree(self, s='', tab=0):
        """Answer a tabbed list, showing the parent-child elements."""
        s += '%s%s\n' % (tab * '\t', self)
        for me in self.elements:
            s = me.printTree(s, tab+1)
        return s
        
    def _get_parent(self):
        """Answers the parent of the element, if it exists, by weakref
        reference. Answers None if no parent is defined or if the parent
        not longer exists."""
        if self._parent is not None:
            return self._parent()
        return None
    def _set_parent(self, parent):
        # Note that the calling function must add self to its elements.
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent
    parent = property(_get_parent, _set_parent)
    
    def _get_root(self):
        """Answer the root element at top of the tree. Answer self if it is the root.
        """
        if self.parent is None:
            return self
        return self.parent.root
    root = property(_get_root)
    
    def _get_merzRootLayer(self):
        """Answer the root.merzRootLayer"""
        return self.root.merzLayer
    merzRootLayer = property(_get_merzRootLayer)
                        
    def _get_merzParentLayer(self):
        """Answer the self.parent.merzLayer or self.merzRootLayer if parent is not defined."""
        if self.parent is not None:
            return self.parent.merzLayer
        return self.merzRootLayer
    merzParentLayer = property(_get_merzParentLayer)
                        
    def addElement(self, me):
        self.elements.append(me)
        if me.parent is None:
            me.parent = self

    def _get_x(self):
        return self._x
    def _set_x(self, x):
        self._x = x
        # Set the position of self.merzLayer
        self.merzLayer.setPosition((self.gx, self.gy))
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._y
    def _set_y(self, y):
        self._y = y
        # Set the position of self.merzLayer
        self.merzLayer.setPosition((self.gx, self.gy))
    y = property(_get_y, _set_y)
    
    def _get_gx(self):
        gx = self.x
        if self.parent is not None:
            if -1 <= gx < 0:
                gx = self.parent.gw * (1 + gx)
            elif gx < 0:
                gx = self.parent.gw + gx
            elif 0 < gx <= 1: # Factor inside parent width
                gx = self.parent.gw * gx
        return gx
    gx = property(_get_gx)
    
    def _get_gy(self):
        gy = self.y
        if self.parent is not None:
            if -1 <= gy < 0:
                gy = self.parent.gy * (1 + gy)
            elif gy < 0:
                gy = self.parent.gh + gy
            elif 0 < gy <= 1: # Factor inside parent height
                gy = self.parent.gh * gy
        return gy
    gy = property(_get_gy)
    
    def _get_w(self):
        return self._w
    def _set_w(self, w):
        self._w = w # Can be fraction of parent width
        # Set the global width of self.merzLayer
        self.merzLayer.setSize((self.gw, self.gh))
    w = property(_get_w, _set_w)
    
    def _get_h(self):
        return self._h
    def _set_h(self, h):
        self._h = h # Can be fraction of parent height
        # Set the global height of self.merzLayer
        self.merzLayer.setSize((self.gw, self.gh))
    h = property(_get_h, _set_h)

    def _get_gw(self):
        """Answer the global transformed width of self, relative to the parent tree.
        By default this is equal to the scaled width, in case child elements query self.sw."""
        gw = self.w
        if gw < 0: # In case < 0, then use the value from the right side.
            gw = self.parent.sw - self.x + gw
        if 0 < gw <= 1: # In case it is a franction, use it a factor of self.parent.w
            gw = self.parent.sw * gw
        return gw
    gw = sw = property(_get_gw)
                      
    def _get_gh(self):
        """Answer the global transformed height of self, relative to the parent tree.
        By default htis is equal to the scaled height, in case child elements query self.sh."""
        gh = self.h
        if gh < 0: # In case < 0, then use the value from the top.
            gh = self.parent.sh - self.y + gh
        if 0 < gh <= 1: # In case it is a franction, use it a factor of self.parent.h
            gh = self.parent.sh * gh
        return gh
    gh = sh = property(_get_gh)
                     
    def _get_fill(self):
        return self._fill
    def _set_fill(self, fill):
        self.merzLayer.setFillColor(fill)
        self._fill = fill
    fill = property(_get_fill, _set_fill)
    
    def _get_strokeWidth(self):
        return self._strokeWidth
    def _set_strokeWidth(self, strokeWidth):
        self.merzLayer.setStrokeWidth(strokeWidth)
        self._strokeWidth = strokeWidth
    strokeWidth = property(_get_strokeWidth, _set_strokeWidth)
    
    def _get_stroke(self):
        return self._stroke
    def _set_stroke(self, stroke):
        self.merzLayer.setStrokeColor(stroke)
        self._stroke = stroke
    stroke = property(_get_stroke, _set_stroke)

    # Event handlers
    
    def meGlyphEditorGlyphDidChange(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)
    
    def meGlyphEditorGlyphDidChangeInfo(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChangeInfo(glyph)

    def meGlyphEditorDidSetGlyph(self, info):
        for e in self.elements:
            e.meGlyphEditorDidSetGlyph(info)
        
    def updatePosSize(self):      
        """Update the position, size and scale of all child elements."""  
        self.merzLayer.setSize((self.gw, self.gh))
        self.merzLayer.setPosition((self.gx, self.gy))
        for me in self.elements:
            me.updatePosSize()

    # Constructors
    
    def newText(self, s, x=0, y=0, fill=None, backgroundColor=None, offset=None, padding=None, cornerRadius=0, pointSize=None,
            weight=None, horizontalAlignment=None, verticalAlignment=None, name=None, parent=None):
        if parent is None:
            parent = self
        e = MerzText(s=s, x=x, y=y, fill=fill, backgroundColor=backgroundColor, offset=offset, padding=padding, 
            cornerRadius=cornerRadius, pointSize=pointSize,
            weight=weight, horizontalAlignment=horizontalAlignment, verticalAlignment=verticalAlignment, name=name, parent=parent)
        parent.addElement(e)
        return e
        
    def newRect(self, x=0, y=0, w=100, h=100, fill=None, strokeWidth=1, stroke=None, name=None, parent=None):
        if parent is None:
            parent = self
        e = MerzRect(x=x, y=y, w=w, h=h, fill=fill, strokeWidth=strokeWidth, stroke=stroke, name=name, parent=parent)
        parent.addElement(e)
        return e
        
    def newLine(self, x=0, y=0, w=1, h=0, strokeWidth=1, stroke=0, name=None, parent=None):
        if parent is None:
            parent = self
        e = MerzLine(x=x, y=y, w=w, h=h, strokeWidth=strokeWidth, stroke=stroke, name=name, parent=parent)
        parent.addElement(e)
        return e
        
    def newGlyphPath(self, glyph, x=0, y=0, fill=None, name=None, parent=None):
        if parent is None:
            parent = self
        e = MerzGlyphPath(glyph, x=x, y=y, fill=fill, name=name, parent=parent)
        parent.addElement(e)        
        return e
        
    def newGlyph(self, glyph, x=0, y=0, h=1, fill=None, name=None, parent=None, showMetrics=True, showBox=True):
        if parent is None:
            parent = self
        e = MerzGlyph(glyph, x=x, y=y, h=h, fill=fill, name=name, parent=parent, 
            showMetrics=showMetrics, showBox=showBox)
        parent.addElement(e)        
        return e

    def newGlyphLine(self, glyphNames, font, x=0, y=0, h=1, fill=None, name=None, parent=None, showMetrics=True, showBox=True):
        if parent is None:
            parent = self
        e = MerzGlyphLine(glyphNames, font, x=x, y=y, h=h, fill=fill, name=name, parent=parent, 
            showMetrics=showMetrics, showBox=showBox)
        parent.addElement(e)        
        return e

           
class MerzRect(MerzElement):
    def __init__(self, x=0, y=0, w=1, h=1, fill=None, strokeWidth=1, stroke=None, name=None, parent=None):
        # Store parameters in element
        MerzElement.__init__(self, name, parent)
        self._x, self._y, self._w, self._h = x, y, w, h
        self._fill, self._strokeWidth, self._stroke = fill, strokeWidth, stroke or None
        self.merzLayer = self.merzParentLayer.appendRectangleSublayer(
            name=self.name,
            position=(self.gx, self.gy),
            size=(self.gw, self.gh),
            fillColor=self._fill,
            strokeWidth=self._strokeWidth,
            strokeColor=self._stroke
        )           
            
class MerzLine(MerzElement):
    def __init__(self, x=0, y=0, w=1, h=0, strokeWidth=1, stroke=0, name=None, parent=None):
        MerzElement.__init__(self, name, parent)
        self._x, self._y, self._w, self._h = x, y, w, h
        self._strokeWidth, self._stroke = strokeWidth, stroke or BLACK
        self.merzLayer = self.merzParentLayer.appendLineSublayer(
            name=self.name,
            startPoint=(self.gx, self.gy),
            endPoint=(self.gx+self.gw, self.gy+self.gh),
            strokeWidth=self._strokeWidth,
            strokeColor=self._stroke,
        )

class MerzText(MerzElement):
    def __init__(self, s, x=0, y=0, fill=None, backgroundColor=None, offset=None, padding=None, cornerRadius=0, pointSize=None,
            weight=None, horizontalAlignment=None, verticalAlignment=None, name=None, parent=None):
        MerzElement.__init__(self, name, parent)
        self._x, self._y, = x, y
        self._fill = fill or BLACK
        self.merzLayer = self.merzParentLayer.appendTextLineSublayer(
                position=(self.gx, self.gy),
                offset=offset or (0, 0),
                padding=padding or (10, 10),
                cornerRadius=cornerRadius or 0,
                text=s,
                pointSize=pointSize or 12,
                weight=weight or 'regular', # ('regular', 'bold),
                horizontalAlignment=horizontalAlignment or 'left',
                verticalAlignment=verticalAlignment or 'bottom',
                fillColor=self._fill,
                backgroundColor=backgroundColor,
            )

    def setText(self, s):
        self.merzLayer.setText(s)
        
class MerzGlyphPath(MerzElement):
    def __init__(self, glyph, x=0, y=0, fill=None, strokeWidth=1, stroke=None,
        name=None, parent=None):
        MerzElement.__init__(self, name, parent)
        self.glyph = glyph
        self._x, self._y = x, y
        self._fill, self._strokeWidth, self._stroke = fill or BLACK, strokeWidth, stroke

        self.merzLayer = self.merzParentLayer.appendPathSublayer(
            position=(self.gx, self.gy),
            size=(glyph.width, glyph.font.info.unitsPerEm),
            fillColor=self._fill,
            strokeWidth=self._strokeWidth,
            strokeColor=self._stroke,
        )
        self.setGlyph(glyph)
                
    def setGlyph(self, glyph):
        self.glyph = glyph
        glyphPath = glyph.getRepresentation("merz.CGPath")
        self.merzLayer.setPath(glyphPath)

    def updatePosSize(self):
        """
        The outside of the element is in posSize, relative to the parent.
        The width is defined by the scaled glyph width.
        Internally the posSize is defined by (glyph.width and glyph.font.info.unitsPerEm) in RF em coordinates.
        """
        self.w = self.glyph.width
        fontInfo = self.glyph.font.info
        self.merzLayer.setPosition((self.gx, self.gy))
        # Broadcast, just in case there are child elements
        for me in self.elements:
            me.updatePosSize()  

     
class MerzGlyph(MerzElement):
    def __init__(self, glyph, x=0, y=0, h=1, fill=None, strokeWidth=1, stroke=None, 
        name=None, parent=None, showBox=True, showMetrics=True):
        MerzElement.__init__(self, name, parent)
        self.glyph = glyph
        self._x, self._y, self._h = x, y, h
        self._fill, self._strokeWidth, self._stroke = fill or WHITE, strokeWidth, stroke or None
        self.showBox = showBox
        self.showMetrics = showMetrics
               
        fontInfo = glyph.font.info
        scale = self.gh / fontInfo.unitsPerEm
        
        self.merzLayer = self.parent.merzLayer.appendRectangleSublayer(
            name=self.name,
            position=(self.gx/scale, self.gy/scale),
            size=(glyph.width, fontInfo.unitsPerEm),
            fillColor=self._fill,
            strokeWidth=self._strokeWidth,
            strokeColor=self._stroke
        )
        self.merzLayer.addScaleTransformation(scale)

        baseY = -fontInfo.descender
        # Add the filling glyph path, that works inside a scaled full-em coordinate system 
        self.glyphPath = self.newGlyphPath(glyph, y=baseY)
        # Internal to the MerzGlyph, baseline-descender shift and em-scale are compatible to RF-em coordinates.
        if showMetrics:
            self.newLine(x=0, y=baseY, w=1, stroke=RED)     
            self.newLine(x=0, y=baseY+fontInfo.xHeight, w=1, stroke=BLUE)   
            self.newLine(x=0, y=baseY+fontInfo.capHeight, w=1, stroke=BLUE)   

        self.kerningLabel = self.newText('')

        if showBox:
            self.glyphBox = self.newRect(x=0, y=baseY+font.info.descender, w=0, h=self.font.info.unitsPerEm, fill=None, stroke=LTGRAY)

        #print(self.printTree())
        
    def updatePosSize(self):      
        """Update the position, size and scale of all child elements."""  
        fontInfo = self.glyph.font.info
        scale = self.gh / fontInfo.unitsPerEm
        self.merzLayer.setPosition((self.gx/scale, self.gy/scale))
        self.merzLayer.setSize((self.glyph.width, fontInfo.unitsPerEm))
        self.merzLayer.addScaleTransformation(scale)
        for me in self.elements:
            me.updatePosSize()
        if self.showBox:
            self.glyphBox.x = 0
            self.glyphBox.w = self.glyph.width
            
    def _get_sw(self):
        """Answer the scaled width of self, in case child elements query self.sw."""
        return self.glyph.width
    sw = property(_get_sw)
                      
    def _get_sh(self):
        """Answer the scaled height of self, in case child elements query self.sh."""
        return self.glyph.font.info.unitsPerEm
    sh = property(_get_sh)
            
    def meGlyphEditorGlyphDidChange(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)
        self.setGlyph(glyph)
    
    def setGlyph(self, glyph):
        self.glyph = glyph
        self.glyphPath.setGlyph(glyph)
        self.updatePosSize()

    def glyphEditorGlyphDidChangeInfo(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)

    def meGlyphEditorDidSetGlyph(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)
        self.setGlyph(glyph)

class MerzGlyphLine(MerzElement):

    def __init__(self, glyphNames, font, x=0, y=0, h=1, fill=None, strokeWidth=1, stroke=None, 
        name=None, parent=None, showBox=True, showMetrics=True):
        MerzElement.__init__(self, name, parent)
        self.glyphNames = glyphNames
        self.font = font
        self._x, self._y, self._h = x, y, h
        self._fill, self._strokeWidth, self._stroke = fill or WHITE, strokeWidth, stroke or None
        self.showBox = showBox
        self.showMetrics = showMetrics
        
        # Unpack kerning from groups
        self.glyph2Group1 = {}
        self.glyph2Group2 = {}
        for gName, group in font.groups.items():
            if 'kern1' in gName:
                for glyphName in group:
                    self.glyph2Group1[glyphName] = gName
            if 'kern2' in gName:
                for glyphName in group:
                    self.glyph2Group2[glyphName] = gName
            
        scale = self.gh / font.info.unitsPerEm
        
        self.merzLayer = self.parent.merzLayer.appendRectangleSublayer(
            name=self.name,
            position=(self.gx/scale, self.gy/scale),
            size=(1000, font.info.unitsPerEm),
            fillColor=self._fill,
            strokeWidth=self._strokeWidth,
            strokeColor=self._stroke
        )
        self.merzLayer.addScaleTransformation(scale)

        self.glyphPaths = []
        self.kerningLabels = []
        
        baseY = -font.info.descender
        x = 0
        for glyphName in self.glyphNames:
            if glyphName == '/?': # Will be replaced by current EditorWindow glyph
                glyphName = 'space' # For now, placeholder
            glyph = self.font[glyphName]
            # Add the filling glyph path, that works inside a scaled full-em coordinate system 
            self.glyphPaths.append(self.newGlyphPath(glyph, x=x, y=baseY))
            self.kerningLabels.append(self.newText(''))

            x += glyph.width
        # Internal to the MerzGlyph, baseline-descender shift and em-scale are compatible to RF-em coordinates.
        #self.newLine(x=0, y=0, stroke=BLUE)   
        self.newLine(x=0, y=baseY, w=1, stroke=RED)     
        self.newLine(x=0, y=baseY+font.info.xHeight, w=1, stroke=BLUE)   
        self.newLine(x=0, y=baseY+font.info.capHeight, w=1, stroke=BLUE)   

        #print(self.printTree())
        
    def updatePosSize(self):      
        """Update the position, size and scale of all child elements."""  
        fontInfo = self.font.info
        scale = self.gh / fontInfo.unitsPerEm
        self.merzLayer.setPosition((self.gx/scale, self.gy/scale))
        self.merzLayer.setSize((self.sw, fontInfo.unitsPerEm))
        self.merzLayer.addScaleTransformation(scale)
        for me in self.elements:
            me.updatePosSize()

    def _get_sw(self):
        """Answer the scaled width of self, in case child elements query self.sw."""
        return 10000
    sw = property(_get_sw)
                      
    def _get_sh(self):
        """Answer the scaled height of self, in case child elements query self.sh."""
        return self.glyph.font.info.unitsPerEm
    sh = property(_get_sh)
            
    def meGlyphEditorGlyphDidChange(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)
        self.setGlyph(glyph)
    
    def setGlyph(self, glyph):
        x = 0
        prevName = None
        for gIndex, glyphName in enumerate(self.glyphNames):
            if glyphName == '/?':
                glyphName = glyph.name
            g = self.font[glyphName]
            if prevName is not None:
                group1 = self.glyph2Group1.get(prevName, '')
                group2 = self.glyph2Group2.get(g.name, '')
                k = self.font.kerning.get((group1, group2), 0)
                group1Name = group1.replace('public.kern1.', '')
                group2Name = group2.replace('public.kern2.', '')
                x += k
                self.kerningLabels[gIndex].setText('[%s] %s %d %s [%s]' % 
                    (group1Name or 'NO GROUP', prevName, k, g.name, group2Name or 'NO GROUP'))
                if k < 0:
                    c = RED
                elif k > 0:
                    c = GREEN
                else:
                    c = GRAY
                self.kerningLabels[gIndex].fill = c
                self.kerningLabels[gIndex].x = x
            prevName = g.name
            self.glyphPaths[gIndex].x = x
            self.glyphPaths[gIndex].setGlyph(g)
            x += g.width
        self.updatePosSize()

    def glyphEditorGlyphDidChangeInfo(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)

    def meGlyphEditorDidSetGlyph(self, glyph):
        for e in self.elements:
            e.meGlyphEditorGlyphDidChange(glyph)
        self.setGlyph(glyph)
   
class MerzRoot(MerzElement):
    """
    Merz root element, wrapper that is able to draw "complex elements" in Merz context.
    """
    def __init__(self, glyph, w, h, fill=None, name=None):
        MerzElement.__init__(self, None, name)
        self._w, self._h = w, h
        self.glyph = glyph # Current glyph showing
        self.merzView = merz.MerzView("auto")
        self.container = self.merzView.getMerzContainer()        
        self.merzLayer = self.container.appendBaseSublayer(
            name='canvas', 
            size=(w, h), # Pixel layer size of the window
            backgroundColor= fill or (1, 1, 1, 1)
        )
        self._fill = fill

                     
    def _get_root(self):
        """Answer the root element at top of the tree. Answer self if it is the root.
        """
        return self
    root = property(_get_root)
                         
class BaseAssistant(Subscriber):
    """The assistant supports two important functions:
        * Open a window and create a MerzCanvas to draw there.
        * Support self.backgroundContainer and self.foregroundContainer for drawing in the current EditWindow.

    self.mr --> MerRoot in the assistant window.
    <WindowClass> self.w 
        <VerticalStackView> self.w.stack
            <Button> self.button
            <MerzView> self.mr.merzView 
                <Container> self.mr.container
                    <Base> self.mr.merzLayer            
    """
    NAME = 'Base Assistant'
    debug = True
    
    def __init__(self, glyphEditor):
        Subscriber.__init__(self, glyphEditor)
        self.sampleIndex = 0
    
    def getSampleLength(self):
        return 40

    def showSidesBlack(self, c):
        self.w.showSidesBlack.set(not self.w.showSidesBlack.get()) # Toggle the value
        self.update()

    def notImplementedKey(self, c):
        print('Not implemented yet', c)
        
    FUNCTION_KEYS = {
        '=': showSidesBlack,
        '+': notImplementedKey,
        'y': notImplementedKey, 
        'n': notImplementedKey, 
        'N': notImplementedKey, 
        'm': notImplementedKey, 
        'M': notImplementedKey, 
        'u': notImplementedKey, 
        'i': notImplementedKey, 
        'o': notImplementedKey, 
        'p': notImplementedKey, 
        'U': notImplementedKey, 
        'I': notImplementedKey, 
        'O': notImplementedKey, 
        'P': notImplementedKey, 
        '.': notImplementedKey, 
        ',': notImplementedKey, 
        '<': notImplementedKey, 
        '>': notImplementedKey,
        # RF related
        KEY_SPACE: notImplementedKey,
        KEY_NEWLINE: notImplementedKey,
        KEY_RETURN: notImplementedKey,
        # Arrow keys
        NSUpArrowFunctionKey: notImplementedKey, 
        NSDownArrowFunctionKey: notImplementedKey,
        NSLeftArrowFunctionKey: notImplementedKey, 
        NSRightArrowFunctionKey: notImplementedKey, 
        NSPageUpFunctionKey: notImplementedKey,
        NSPageDownFunctionKey: notImplementedKey, 
        NSHomeFunctionKey: notImplementedKey, 
        NSEndFunctionKey: notImplementedKey,
    }
    def keyDown(self, event):
        try:
            characters = event.characters()
        except (AttributeError, TypeError):
            return

        modifiers = event.modifierFlags()
        commandDown = modifiers & NSCommandKeyMask
        shiftDown = modifiers & NSShiftKeyMask
        controlDown = modifiers & NSControlKeyMask
        alternateDown = modifiers & NSAlternateKeyMask
           
        #if not alternateDown:
        #    return
        if characters in FUNCTION_KEYS:
            FUNCTION_KEYS[characters](characters)
            """
            if characters == 'y':
                self.w.showSidesBlack.set(not self.w.showSidesBlack.get()) # Toggle the value
                self.update()
            elif characters == '/':
                self.w.showMetrics.set(not self.w.showMetrics.get()) # Toggle the value
                self.update()
            elif characters == '+': # Bubble
                print('Implement bubble kern here as bubbleKern()')
            elif characters == '=': # Go to last saved sample index. 
                if len(self.lastSampleIndex) > 1:  
                    self.sampleIndex = self.lastSampleIndex[-1]
                    self.setSampleLines()
                    self.updateFontGoggles()
                    self.selectGlyph() # Does set new sample lines and update.
                    self.lastSampleIndex = self.lastSampleIndex[:-2] # Remove last two from the stack
            elif characters == 'u': # Decrement left margin by 4    
                self._adjustLeftMargin(-1)
                self.update()
            elif characters == 'U': # Decrement left margin by 20
                self._adjustLeftMargin(-5)
                self.update()
            elif characters == 'i': # Increment left margin by 4
                self._adjustLeftMargin(1)
                self.update()
            elif characters == 'I': # Increment left margin by 20
                self._adjustLeftMargin(5)
                self.update()

            elif characters == 'o': # Decrement left margin by 4    
                self._adjustRightMargin(-1)
                self.update()
            elif characters == 'O': # Decrement left margin by 20
                self._adjustRightMargin(-5)
                self.update()
            elif characters == 'p': # Increment left margin by 4
                self._adjustRightMargin(1)
                self.update()
            elif characters == 'P': # Increment left margin by 20
                self._adjustRightMargin(5)
                self.update()

            elif characters == 'n': # Decrement left kerning by 4    
                self._adjustKernLeftPair(1)
                self.update()
            elif characters == 'N': # Decrement left kerming by 20                 self.update()
            elif characters == 'm': # Increment left kerning by 4
                self._adjustKernLeftPair(-1)
                self.update()
            elif characters == 'M': # Increment left kerming by 20
                self._adjustKernLeftPair(-5)
                self.update()

            elif characters == ',': # Decrement left kerning by 4    
                self._adjustKernRightPair(-1)
                self.update()
            elif characters == '<': # Decrement left kerming by 20
                self._adjustKernRightPair(-5)
                self.update()
            elif characters == '.': # Increment left kerning by 4
                self._adjustKernRightPair(1)
                self.update()
            elif characters == '>': # Increment left kerming by 20
                self._adjustKernRightPair(5)
                self.update()
            #print(characters)
                                       
        #elif alternateDown and characters in ARROW_KEYS:
        elif characters in ARROW_KEYS:

            if characters in NSHomeFunctionKey:
                self.sampleIndex = 0
                #print('NSHomeFunctionKey', shiftDown, controlDown)
                self.updateFontGoggles()
                self.selectGlyph() # Does set new sample lines and update.
            elif characters in NSEndFunctionKey:
                self.sampleIndex = len(self.sample)-1
                #print('NSEndFunctionKey', shiftDown, controlDown)
                self.updateFontGoggles()
                self.selectGlyph() # Does set new sample lines and update.
            elif characters == NSUpArrowFunctionKey:
                self.lineFocus = 0
                if shiftDown:
                    self.sampleIndex = max(self.sampleIndex-self.getSampleLength()*8, 0)
                else:
                    self.sampleIndex = max(self.sampleIndex-self.getSampleLength(), 0)
                self.updateFontGoggles()
                self.selectGlyph() # Does set new sample lines and update.
                #print('NSUpArrowFunctionKey', shiftDown, controlDown)
            elif characters == NSDownArrowFunctionKey:
                self.lineFocus = 0
                if shiftDown:
                    self.sampleIndex = min(self.sampleIndex+self.getSampleLength()*8, len(self.sample))
                else:
                    self.sampleIndex = min(self.sampleIndex+self.getSampleLength(), len(self.sample))
                self.updateFontGoggles()
                self.selectGlyph() # Does set new sample lines and update.
                #print('NSDownArrowFunctionKey', shiftDown, controlDown)
            elif characters == NSLeftArrowFunctionKey:
                if controlDown:
                    if shiftDown:
                        self._adjustKernRightPair(-5)
                    else:                
                         self._adjustKernRightPair(-1)
                    self.update()
                elif shiftDown:
                    self.lineFocus = 1
                    self.sampleCursor -= 1
                    if self.sampleCursor < 0:
                        self.sampleCursor = len(self.sampleLines[1])-1
                else:
                    self.lineFocus = 0
                    self.sampleIndex = max(self.sampleIndex-1, 0)
                    self.updateFontGoggles()
                self.selectGlyph(-1) # Does set new sample lines and update.
                #print('NSLeftArrowFunctionKey', shiftDown, controlDown)
            elif characters == NSRightArrowFunctionKey:
                if controlDown:
                    if shiftDown:
                        self._adjustKernRightPair(5)
                    else:                
                         self._adjustKernRightPair(1)
                    self.update()
                elif shiftDown:
                    self.lineFocus = 1
                    self.sampleCursor += 1
                    if self.sampleCursor >= len(self.sampleLines[1]):
                        self.sampleCursor = 0
                else:
                    self.lineFocus = 0
                    self.sampleIndex = min(self.sampleIndex+1, len(self.sample))
                    self.updateFontGoggles()
                self.selectGlyph() # Does set new sample lines and update.
                #print('NSRightArrowFunctionKey', shiftDown, controlDown)
            elif characters == NSPageUpFunctionKey:
                #self.sampleIndex = max(0, self.sampleIndex-1)
                #self.sampleY = 0
                print('NSPageUpFunctionKey', shiftDown, controlDown)
                self.update()
            elif characters == NSPageDownFunctionKey:
                #self.sampleIndex += 1
                #if self.sampleIndex >= len(SAMPLES):
                #    self.sampleIndex = 0
                #self.sampleY = 0
                print('NSPageDownFunctionKey', shiftDown, controlDown)
                self.update()
            """

    def build(self):
        glyph = CurrentGlyph()
        assert glyph is not None
        #self.glyph2FontGroups1 = {} # Key font.path, value glyph2Groups dictionary
        #self.glyph2FontGroups2 = {} # Key font.path, value glyph2Groups dictionary
        
        w, h = W, H

        self.mr = MerzRoot(glyph, w, h, fill=(0.9, 0.9, 0.9, 1))
        name = self.getName()
        self.w = WindowClass((w, h), name, minSize=(50, H))
        self.w.t = CanvasGroup((0, 0, 0, 0), delegate=self)
        self.w.bind('resize', self.windowResized)
        self.w.bind('close', self.windowCloseCallback)

        # Create the Vanilla controls for this window.
        #self.button = vanilla.Button("auto", "🌛", callback=self.buttonCallback)

        # Add the Vanilla controls as part of a window stack view
        self.w.stack = vanilla.VerticalStackView(
            (0, 0, 0, 0),
            #views=[dict(view=self.mr.merzView), dict(view=self.button)],
            views=[dict(view=self.mr.merzView)],
            spacing=0, # 10,
            edgeInsets=(0, 0, 0, 0), #(10, 10, 10, 10)
        )
        M = 16
        # Create the Merz element in self.w that draws the glyph and metrics
        self.mr.newGlyphLine(('V', '/?', 'V', 'H', '/?', 'H', 'O', '/?', 'O', 'n', '/?', 'n'), glyph.font, x=M, y=M, h=-M)
        # Build a drawing connection to the current EditWindow
        self.buildGlyphEditorContainers()

        # Open the window with the sample text pattern
        self.w.open()

    def windowCloseCallback(self, sender):
        """Window is closing, remove the observers"""
        self.destroy()

    def buildGlyphEditorContainers(self):
        glyphEditor = self.getGlyphEditor()
        if glyphEditor is None:
            print('No GlyphEditor open')
            self.backgroundContainer = None
            self.foregroundContainer = None
        else:
            self.backgroundContainer = glyphEditor.extensionContainer(
                identifier="com.roboFont.GlyphEditorDrawingSubscriberDemo.background",
                location="background",
                clear=True
            )
            self.foregroundContainer = glyphEditor.extensionContainer(
                identifier="com.roboFont.GlyphEditorDrawingSubscriberDemo.foreground",
                location="foreground",
                clear=True
            )

    def destroy(self):
        if self.foregroundContainer is not None:
            self.backgroundContainer.clearSublayers()
            self.foregroundContainer.clearSublayers()

        #removeObserver(self, "currentGlyphChanged")
        #removeObserver(self, 'Glyph.Changed')
        #removeObserver(self, "keyDown")
        #removeObserver(self, "drawBackground")
        #removeObserver(self, "fontDidOpen")
        #removeObserver(self, "fontDidClose")

        #removeObserver(self, "mouseUp")
        #removeObserver(self, "mouseDown")
        #removeObserver(self, "mouseDragged")

    def viewDidChangeGlyph(self, info):
        print('viewDidChangeGlyph', info)
        
    glyphEditorDidSetGlyphDelay = 0

    def glyphEditorDidSetGlyph(self, info):
        glyph = info['glyph']
        if glyph is None:
            return
        if self.w._window is not None:
            self.w.setTitle('%s | %s' % (self.getName(), glyph.name))
            #self.w._window.setTitle_('%s | %s' % (self.getName(), glyph.name))
        self.updateGroupInfo(glyph)
        self.mr.meGlyphEditorDidSetGlyph(glyph)
        self.mr.meGlyphEditorGlyphDidChange(glyph)
        self.mr.meGlyphEditorGlyphDidChangeInfo(glyph)
        
        #self.glyphEditorGlyphDidChangeOutline(info)
        #self.glyphEditorGlyphDidChangeComponents(info)
        #self.glyphEditorGlyphDidChangeAnchors(info)
        #self.glyphEditorGlyphDidChangeGuidelines(info)
        #self.glyphEditorGlyphDidChangeImage(info)
        #self.glyphEditorGlyphDidChangeMetrics(info)
        #self.glyphEditorGlyphDidChangeContours(info)

        #self.ld.emLayer.setSize((self.glyph.width, self.glyph.font.info.unitsPerEm))
        #for lineLayer in self.ld.metricsLines:
        #    px, py = lineLayer.getEndPoint()
        #    lineLayer.setEndPoint((self.OX + self.glyph.width, py))
            
    def glyphEditorGlyphDidChange(self, info):
        """Broadcasting on all elements. Only elements that have a reference to the current
        glyph will update themselves."""
        glyph = info['glyph']
        self.mr.meGlyphEditorGlyphDidChange(glyph)

    def glyphEditorGlyphDidChangeInfo(self, info):
        """Broadcasting on all elements. Only elements that have a reference to the current
        glyph will update the info themselves."""
        glyph = info['glyph']
        self.mr.meGlyphEditorGlyphDidChangeInfo(glyph)
            
    def windowResized(self, w):
        """The window resized. Calculate a new Em scale factor, adjust the size of the canvas, 
        and update all Merz components to the new scale."""
        size = self.w._window.frame().size
        self.mr.w, self.mr.h = size.width, size.height
        self.mr.updatePosSize() # Update position, size and scale for all child elements
           
    def getName(self):
        if self.mr.glyph is not None:
            return '%s %s' % (self.mr.glyph.font.info.familyName, self.mr.glyph.font.info.styleName)
        return self.NAME
    
    def updateGroupInfo(self, glyph):
        if glyph is not None:
            #print(glyph.font.groups.keys())
            #for groupName, group in glyph.font.groups.items():
            #    print(groupName)
            pass
            
    def started(self):
        self.w.open()

    """
    def _switchToDarkMode(self):
        self.ld.glyphLayer.setFillColor((1, 1, 1, 1))
        self.ld.canvas.setBackgroundColor((0, 0, 0, 1))

    def _switchToLightMode(self):
        self.ld.glyphLayer.setFillColor((0, 0, 0, 1))
        self.ld.canvas.setBackgroundColor((1, 1, 1, 1))

    def buttonCallback(self, sender):
        if sender.getTitle() == "🌛":
            self._switchToDarkMode()
            sender.setTitle('🌞')
        else:
            self._switchToLightMode()
            sender.setTitle('🌛')
    """

if __name__ == '__main__':
    registerGlyphEditorSubscriber(BaseAssistant)
    
    