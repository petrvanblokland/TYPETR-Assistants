# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR baseAssistant.py
#
#    The BaseAssistant provides both an example template as base class for writing Assistant tools,
#    with specific knowledge about a typedesign project.
#

import os

# Import the main entry into RoboFont subscriber and window controller classes and functions.
from mojo.subscriber import (Subscriber, WindowController, 
    registerGlyphEditorSubscriber, disableSubscriberEvents, getRegisteredSubscriberEvents,
    unregisterGlyphEditorSubscriber, registerSubscriberEvent)
from mojo.events import postEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint

# Get the vanilla controls that are used in the UI window
from vanilla import (Window, FloatingWindow, TextBox, EditText, PopUpButton, RadioGroup, 
    CheckBox, Slider, List, Button, HorizontalRadioGroup)

# Unique key to identify Assistant events coming from helpers.
DEFAULT_KEY = 'com.typetr.Assistant'

EVENT_PREVIEW_OVERLAY_CHANGED = f"{DEFAULT_KEY}.previewOverlayChanged"

EVENT_Q2B = f"{DEFAULT_KEY}.Q2B"
EVENT_B2Q = f"{DEFAULT_KEY}.B2Q"

EVENT_UFO_REFERENCE_CHANGED = f"{DEFAULT_KEY}.ufoReferenceChanged"
EVENT_UFO_REFERENCE_SELECTION_CHANGED = f"{DEFAULT_KEY}.ufoReferenceSelectionChanged"
EVENT_UFO_NAMELIST_CHANGED = f"{DEFAULT_KEY}.ufoNameListChanged"
EVENT_UFO_NAMELIST_SELECTION_CHANGED = f"{DEFAULT_KEY}.ufoNameListSelectionChanged"
EVENT_UFO_NAMELIST_DBLCLICK = f"{DEFAULT_KEY}.ufoNameListDblClick"
EVENT_GLYPH_NAMELIST_CHANGED = f"{DEFAULT_KEY}.glyphNameListChanged"
EVENT_GLYPH_NAMELIST_SELECTION_CHANGED = f"{DEFAULT_KEY}.glyphNameListSelectionChanged"
EVENT_GLYPH_NAMELIST_DBLCLICK = f"{DEFAULT_KEY}.glyphNameListDblClick"

def getOpenUfoNames():
    refNames = []
    for f in AllFonts(): # Use open fonts as seed to find the folders. 
        refNames.append(getUfoName(f))
    return refNames

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

    
class BaseAssistant(Subscriber):
    """
    Tool can only ask for information to the palette

    """

    debug = True
    controller = None

    VERBOSE = False # Set to True for debugging the tool
    FAR = 100000 # Move Merz objects here to get them out of view.

    MAX_OVERLAY_POINTS = 100 # Number point markers to show on an overlay glyph
    POINT_MARKER_R = 4 # Size of point markers

    OVERLAY_FILL_COLOR = 0.7, 0.7, 0.7, 0.5
    PREVIEW_FILL_COLOR = 0, 0, 0, 0.9
    PREVIEW_STROKE_COLOR = 0, 0, 0, 0.8
    PREVIEW_STROKE_WIDTH = 1
    
    def build(self):
        # Build the Assistant subscriber tool
        
        self.glyphNames = [] # Collect the glyph names here for all open fonts.
        
        # Get the GlyphEditor that relates to self.
        glyphEditor = self.getGlyphEditor()

        self.foregroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )
        
        # Build the Merz objects, depending on the functions defined in the controller.
        if self.controller.HAS_PREVIEW_OVERLAY_GLYPH:
            # Previewing current glyphs on left/right side.        
            self.previewGlyphLeft = self.backgroundContainer.appendPathSublayer(
                position=(self.FAR, 0),
                fillColor=(0, 0, 0, 1), # Default as filled black
            )
            self.previewOverlayGlyph = self.backgroundContainer.appendPathSublayer(
                position=(self.FAR, 0),
                fillColor=None, # Default as outline
                strokeColor=(0, 0.5, 0, 1),
                strokeWidth=1,
            )
            self.previewGlyphRight = self.backgroundContainer.appendPathSublayer(
                position=(self.FAR, 0),
                fillColor=(0, 0, 0, 1), # Default as filled black
            )
            self.previewOverlayPointMarkers = []
            for pIndex in range(self.MAX_OVERLAY_POINTS): # Max number of points to display in a glyph
                self.previewOverlayPointMarkers.append(self.backgroundContainer.appendRectangleSublayer(name="previewOverlayPoint%03d" % pIndex,
                    position=(self.FAR, 0),
                    size=(self.POINT_MARKER_R*2, self.POINT_MARKER_R*2),
                    fillColor=None,
                    strokeColor=(0, 0.5, 0, 1), # 
                    strokeWidth=1,
                ))
        
        self.ufoReferenceChanged()
        self.ufoNameListChanged()
                
    def destroy(self):
        """This is called if the glyphEditor is about to get closed. 
        All containers are released there and so it the event binding."""
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(DEFAULT_KEY, location='background')
        container.clearSublayers()

    def getGlyph(self):
        """Answer the glyph in the GlyphEditor that relates to this subscriber"""
        glyphEditor = self.getGlyphEditor()
        return glyphEditor.getGlyph()

    def glyphEditorDidSetGlyph(self, info):
        print('Subscriber --- glyphEditorDidSetGlyph /%s' % info['glyph'].name)

    def glyphEditorDidMouseUp(self, info):
        print('Subscriber --- glyphEditorDidMouseUp /%s' % info['glyph'].name)

    def glyphEditorDidMouseDrag(self, info):
        print('Subscriber --- glyphEditorDidMouseDrag /%s' % info['glyph'].name)

    def glyphEditorGlyphDidChangeSelection(self, info):
        print('Subscriber --- glyphEditorGlyphDidChangeSelection /%s' % info['glyph'].name)

    def fontDocumentDidOpen(self, info):
        print('Subscriber --- fontDocumentDidOpen')
        
    def fontDocumentDidClose(self, info):
        print('Subscriber --- fontDocumentDidClose')

    #    G L Y P H  &  F O N T

    def getFont(self, path, showInterface=False):
        # Check if the master is already open, by RoboFont or by self
        for f in AllFonts():
            if f.path is not None and f.path.endswith(path):
                #print('... Selecting open font', path)
                return f
        if path in self.controller.openFonts:
            f = self.controller.openFonts[path]
            if showInterface:
                f.openInterface()
            return f
        # Not open yet, open it in the background and cache the master
        # In case "showUI" error here, then start venv
        f = OpenFont(path, showInterface=showInterface)
        if f is None:
            print('### Cannot open font', path)
            return None
        self.controller.openFonts[path] = f
        return f

    #    P R E V I E W  /  O V E R L A Y
        
    # Event handling if the preview/overlay is installed in the controller by HAS_PREVIEW_OVERLAY_GLYPH = True
    def previewOverlayDidChange(self, info):
        if self.VERBOSE:
            print('--- previewOverlayDidChange')
        g = self.getGlyph()
        # Show filled preview of the glyph on left side
        glyphPathLeft = glyphPathRight = glyphPath = g.getRepresentation("merz.CGPath")
        leftName = self.controller.w.previewGlyphLeftName.get()
        if leftName == '/?': 
            leftName = g.name
        if leftName and leftName in g.font:
            gLeft = g.font[leftName]
            glyphPathLeft = gLeft.getRepresentation("merz.CGPath") 
            self.previewGlyphLeft.setPath(glyphPathLeft)
            self.previewGlyphLeft.setPosition((-gLeft.width, 0))
            if self.controller.w.fillLeftOverlay.get():
                self.previewGlyphLeft.setFillColor(self.PREVIEW_FILL_COLOR)
                self.previewGlyphRight.setStrokeColor(None)
            else:
                self.previewGlyphLeft.setFillColor(None)
                self.previewGlyphLeft.setStrokeColor(self.PREVIEW_STROKE_COLOR)
                self.previewGlyphLeft.setStrokeWidth(self.PREVIEW_STROKE_WIDTH)
        else:
            self.previewGlyphLeft.setPosition((self.FAR, 0)) # Far, far awayPREVIEW_STROKE_COLOR
            
        # Show filled preview of the glyph on right side
        rightName = self.controller.w.previewGlyphRightName.get()
        if rightName == '/?':
            rightName = g.name
        if rightName and rightName in g.font:
            gRight = g.font[rightName]
            glyphPathRight = gRight.getRepresentation("merz.CGPath") 
            self.previewGlyphRight.setPath(glyphPathRight)
            self.previewGlyphRight.setPosition((g.width, 0))
            if self.controller.w.fillRightOverlay.get():
                self.previewGlyphRight.setFillColor(self.PREVIEW_FILL_COLOR)
                self.previewGlyphRight.setStrokeColor(None)
            else:
                self.previewGlyphRight.setFillColor(None)
                self.previewGlyphRight.setStrokeColor(self.PREVIEW_STROKE_COLOR)
                self.previewGlyphRight.setStrokeWidth(self.PREVIEW_STROKE_WIDTH)
        else:
            self.previewGlyphRight.setPosition((self.FAR, 0))

        # Show outline preview of the glyph on middle
        overlayName = self.controller.w.overlayGlyphName.get()
        if overlayName == '/?':
            overlayName = g.name

        pIndex = 0
        if overlayName and overlayName in g.font:
            gOverlay = g.font[overlayName]
            glyphPathOverlay = gOverlay.getRepresentation("merz.CGPath") 
            self.previewOverlayGlyph.setPath(glyphPathOverlay)

            if self.controller.w.overlayAlignment.get() == 0:
                x = 0 # Left aligned 
            elif self.controller.w.overlayAlignment.get() == 1:
                x = (g.width - gOverlay.width)/2 # Centered
            else:
                x = g.width - gOverlay.width # Right aligned
            x += round(self.controller.w.overlayXSlider.get())
            y = round(self.controller.w.overlayYSlider.get())
            self.previewOverlayGlyph.setPosition((x, y))
            self.previewOverlayGlyph.setFillColor(self.OVERLAY_FILL_COLOR)
            # Move point markers to this glyph, as much of the list as we need. 
            for contour in gOverlay._contours:
                for p in contour._points:
                    #print(pIndex, len(self.previewPointMarkers))
                    self.previewOverlayPointMarkers[pIndex].setPosition((x+p.x-self.POINT_MARKER_R, p.y-self.POINT_MARKER_R)) 
                    pIndex += 1
        else:
            self.previewOverlayGlyph.setPosition((self.FAR, 0))            

        # Then hide the rest of the point markers
        for n in range(pIndex, len(self.previewOverlayPointMarkers)):
            self.previewOverlayPointMarkers[n].setPosition((self.FAR, 0)) 


    #    B 2 Q 2 B  C O N V E R S I O N

    def convertQ2B(self, info):
        g = self.getGlyph()
        print('--- convertQ2B: Needs QBQConverter.py', g.name)   
             
    def convertB2Q(self, info):
        g = self.getGlyph()
        print('--- convertB2Q: Needs QBQConverter.py', g.name)   
    
    #    G L Y P H - U F O  B R O W S E R
    
    def getReferenceFont(self):
        refName = self.controller.w.ufoReference.getItem()
        if refName is None:
            return None
        # Find the reference font
        for f in AllFonts():
            if getUfoName(f) == refName:
                return f
        return None
        
    #    E V E N T S
    
    def ufoReferenceChanged(self, info=None):
        # Event: EVENT_UFO_REFERENCE_CHANGED
        print('Subscriber --- ufoReferenceChanged')
        refNames = getOpenUfoNames()
        self.controller.w.ufoReference.setItems(refNames)

    def ufoReferenceSelectionChanged(self, info):
        # Event: EVENT_UFO_REFERENCE_SELECTION_CHANGED
        g = self.getGlyph()
        print('Subscriber --- ufoReferenceSelectionChanged', g.name)

    def ufoNameListChanged(self, info=None):
        """Update the list of UFOs that are in the same folder as the fonts that are currently open.
        Open them in the background if not already open."""
        # Event: EVENT_UFO_NAMELIST_CHANGED
        g = self.getGlyph()
        print('Subscriber --- ufoNameListChanged', g.name)

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
                ufo = self.getFont(ufoPath)
                self.glyphNames = self.glyphNames.union(set(ufo.keys()))
                    
        self.controller.w.ufoNames.set(sorted(ufoNames))
        self.glyphNameListChanged()

    def ufoNameListSelectionChanged(self, info):
        # Event: EVENT_UFO_NAMELIST_SELECTION_CHANGED
        g = self.getGlyph()
        print('Subscriber --- ufoNameListSelectionChanged', g.name)

    def ufoNameListDblClick(self, info):
        # Event: EVENT_UFO_NAMELIST_DBLCLICK
        print('Subscriber --- ufoNameListDblClick')
        ref = self.getReferenceFont()
        if ref is None:
            return
        dirPath = getUfoDirPath(ref)

        ufoSelected = self.controller.w.ufoNames.getSelection()
        for ufoIndex in ufoSelected:

            ufoPath = dirPath + self.controller.w.ufoNames[ufoIndex]

            if self.controller.w.selectOpenDblClick.get() == 0: # Open selection as EditWindow
                f = self.getFont(ufoPath, showInterface=True)
                selected = self.controller.w.glyphNames.getSelection()
                for index in selected:
                    glyphName = self.controller.w.glyphNames[index]
                    if glyphName in f:
                        OpenGlyphWindow(f[glyphName])
                
            else: # Open selection as FontWindow
                pass
    
    def glyphNameListChanged(self, info=None):
        # Event: EVENT_UFO_REFERENCE_SELECTION_CHANGED
        g = self.getGlyph()
        
        filteredGlyphNames = []
        filterPatternStart = self.controller.w.filterPatternStart.get().strip()
        filterPatternHas = self.controller.w.filterPatternHas.get().strip()
        filterPatternEnd = self.controller.w.filterPatternEnd.get().strip()
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

        for glyphName in sorted(self.glyphNames):
            selected = None
            if ((not filterPatternStart or glyphName.startswith(filterPatternStart)) and
                (not filterPatternHas or filterPatternHas in glyphName) and
                (not filterPatternEnd or glyphName.endswith(filterPatternEnd))):
                selected = glyphName
            # Test on component filter too
            if selected is not None and selected in g.font and (
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
                
        self.controller.w.glyphNames.set(sorted(filteredGlyphNames))

    def glyphNameListSelectionChanged(self, info):
        # Event: EVENT_GLYPH_NAMELIST_SELECTION_CHANGED
        print('Subscriber --- glyphNameListSelectionChanged')

    def glyphNameListDblClick(self, info):
        # Event: EVENT_GLYPH_NAMELIST_DBLCLICK
        g = self.getGlyph()
        print('Subscriber --- glyphNameListDblClick', g.name)
        
    #    U P D A T I N G 
             
    def update(self):
        if self.VERBOSE:
            print('--- update')

class BaseAssistantController(WindowController):
    """Define the base class the creates the UI window for the assistant tool.
    Inheriting controller classes can define required functions by setting class flags to True.
    """

    WINDOW_CLASS = Window # Or FloatingWindow
    subscriberClass = BaseAssistant
    debug = True
    openFonts = {} # All open fonts (even without UI). Key is their full path.
    
    W = 400 # Width of controller window
    H = 600
    M = 8 # Margin and gutter
    L = 20 # Line height between controls
    LL = 32 # Line height between functions
    CW = (W - 4 * M) / 3 # Column width
    CW2 = 2 * CW + M # Column width
    C0 = M # X position of column 0
    C1 = C0 + CW + M # X position of column 1
    C2 = C1 + CW + M # X position of column 2

    # These flags select various standard functions
    HAS_PREVIEW_OVERLAY_GLYPH = True
    HAS_Q2B2Q = True
    HAS_GLYPH_UFO_BROWSER = True
    
    TITLE = None # Default is class subscriber class name
    
    def build(self):
        self.w = self.WINDOW_CLASS((self.W, self.H), self.TITLE or self.subscriberClass.__name__)
        self.buildControls()        
        self.w.open()

        #postEvent(EVENT_UFO_REFERENCE_CHANGED)
        #postEvent(EVENT_UFO_NAMELIST_CHANGED)

    def started(self):
        self.subscriberClass.controller = self
        registerGlyphEditorSubscriber(self.subscriberClass)

    def destroy(self):
        unregisterGlyphEditorSubscriber(self.subscriberClass)
        self.subscriberClass.controller = None

    def buildControls(self):
        """Build all controls for this tools. Redefine this method if another order and selection of tools is required.
        The order of the build calls defines the interface from top to bottom. Each build call needs to return
        the current position of y.
        """
        y = self.M
        if self.HAS_PREVIEW_OVERLAY_GLYPH:
            y = self.buildPreviewOverlayGlyph(y)
            
        if self.HAS_GLYPH_UFO_BROWSER:
            y = self.buildGlyphUfoBrowser(y) 

        if self.HAS_Q2B2Q:
            y = self.buildCubicQuadraticConverter(y) 
            
            
    #    P R E V I E W  /  O V E R L A Y
            
    MIN_PREVIEW_ALIGN = -500
    MAX_PREVIEW_ALIGN = 500
    
    def buildPreviewOverlayGlyph(self, y):
        """Build the controls for preview/overlay glyph functions:
            [        ] - Optional name of the glyph to show on the left side. /? shows current glyph
            [        ] - Overlay glyph to show as outline
            [x] Fill Left - Draw left overlay as black or outline
            [x] Preview kerned - Space preview left and right kerned from the current glyph
            (o) L  ( ) C  ( ) R - Left/Center/Right alignment of overlay glyph. Does reset the slider values to 0
            [        ] - Optional name of the glyph to show on the right side. /? shows current glyph
            [x] Fill Right - Draw right overlay as black or outline
            X [---|----] - Slider horizontal position, relative to the alignment. 
            Y [---|----] - Slider horizontal position, relative to the alignment. 
            ↻ [---|----] - Slider rotation of overlay glyph. 
        """
        registerSubscriberEvent(
            subscriberEventName=EVENT_PREVIEW_OVERLAY_CHANGED,
            methodName="previewOverlayDidChange",
            lowLevelEventNames=[EVENT_PREVIEW_OVERLAY_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )

        self.w.previewGlyphLeftLabel = TextBox((self.C0, y, self.CW, self.L), 'Preview Left /?')
        self.w.previewGlyphLabel = TextBox((self.C1, y, self.CW, self.L), 'Overlay /?')
        self.w.previewGlyphRightLabel = TextBox((self.C2, y, self.CW, self.L), 'Preview Right /?')

        y += self.L
        self.w.previewGlyphLeftName = EditText((self.C0, y, self.CW, self.L), callback=self.previewOverlayCallback)
        self.w.overlayGlyphName = EditText((self.C1, y, self.CW, self.L), callback=self.previewOverlayCallback)
        self.w.previewGlyphRightName = EditText((self.C2, y, self.CW, self.L), callback=self.previewOverlayCallback)

        y += self.L
        self.w.fillLeftOverlay = CheckBox((self.C0+4, y, self.CW, self.L), 'Fill Left', value=True, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.flipOverlayH = CheckBox((self.C1+4, y, self.CW, self.L), 'Flip V', value=False, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.flipOverlayV = CheckBox((self.C1 + self.CW/2, y, self.CW, self.L), 'Flip H', value=False, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.fillRightOverlay = CheckBox((self.C2+4, y, self.CW, self.L), 'Fill Right', value=True, sizeStyle='small', 
            callback=self.previewOverlayCallback)

        y += self.L
        self.w.previewKerned = CheckBox((self.C0+4, y, self.CW, self.L), 'Preview kerned', value=False, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.overlayAlignment = RadioGroup((self.C1, y, self.CW, self.L), ('L', 'C', 'R'), isVertical=False, sizeStyle='small', 
            callback=self.previewOverlayRadioCallback)
        self.w.overlayAlignment.set(0)
        self.w.snapKeyLabel = TextBox((self.C2 + self.CW/4, y, self.CW/2, self.L), 'Snap key')
        self.w.snapKey = EditText((self.C2, y, self.CW/4, self.L), 'G', sizeStyle='small')

        y += self.L        
        # Vertical position of overlays
        self.w.overlayYSliderLabel = TextBox((self.C0, y+4, 16, self.L), 'Y', sizeStyle='small')
        self.w.overlayYSlider = Slider((self.C0+16, y, self.CW-16, self.L), 
            minValue=self.MIN_PREVIEW_ALIGN, maxValue=self.MAX_PREVIEW_ALIGN, value=0, sizeStyle='small', 
            continuous=True, callback=self.previewOverlayCallback, tickMarkCount=11)
        # Horizontal position of overlays
        self.w.overlayXSliderLabel = TextBox((self.C1, y+4, 16, self.L), 'X', sizeStyle='small')
        self.w.overlayXSlider = Slider((self.C1+16, y, self.CW-16, self.L), 
            minValue=self.MIN_PREVIEW_ALIGN, maxValue=self.MAX_PREVIEW_ALIGN, value=0, sizeStyle='small', 
            continuous=True, callback=self.previewOverlayCallback, tickMarkCount=11)
        # Rotation of overlays
        self.w.overlayRSliderLabel = TextBox((self.C2, y+4, 16, self.L), '↻', sizeStyle='small')
        self.w.overlayRSlider = Slider((self.C2+16, y, self.CW-16, self.L), 
            minValue=self.MIN_PREVIEW_ALIGN, maxValue=self.MAX_PREVIEW_ALIGN, value=0, sizeStyle='small', 
            continuous=True, callback=self.previewOverlayCallback, tickMarkCount=360/45)

        return y + self.LL # Answer the next vertical position for controls

    def previewOverlayCallback(self, sender):
        postEvent(EVENT_PREVIEW_OVERLAY_CHANGED)

    def previewOverlayRadioCallback(self, sender):
        """Reset the sliders."""
        self.w.overlayXSlider.set(0)
        self.w.overlayYSlider.set(0)
        self.w.overlayRSlider.set(0)
        postEvent(EVENT_PREVIEW_OVERLAY_CHANGED)

    #    B 2 Q 2 B  C O N V E R S I O N

    def buildCubicQuadraticConverter(self, y):
        """Build the buttons that convert between Cubic (Bezier) and Quadratic."""
        registerSubscriberEvent(
            subscriberEventName=EVENT_Q2B,
            methodName="convertQ2B",
            lowLevelEventNames=[EVENT_Q2B],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_B2Q,
            methodName="convertB2Q",
            lowLevelEventNames=[EVENT_B2Q],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        self.w.Q2BButton = Button((self.C0, y, self.CW, 32), 'Q --> B', callback=self.Q2BCallback)
        self.w.B2QButton = Button((self.C1, y, self.CW, 32), 'B --> Q', callback=self.B2QCallback)
    
        return y + self.LL 

    def Q2BCallback(self, sender):
        postEvent(f"{DEFAULT_KEY}.Q2B")
                                             
    def B2QCallback(self, sender):
        postEvent(f"{DEFAULT_KEY}.B2Q")
        
    #    G L Y P H - U F O  B R O W S E R

    BROWSER_HEIGHT = 300
    
    def buildGlyphUfoBrowser(self, y):

        registerSubscriberEvent(
            subscriberEventName=EVENT_UFO_REFERENCE_CHANGED,
            methodName="ufoReferenceChanged",
            lowLevelEventNames=[EVENT_UFO_REFERENCE_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_UFO_REFERENCE_SELECTION_CHANGED,
            methodName="ufoReferenceSelectionChanged",
            lowLevelEventNames=[EVENT_UFO_REFERENCE_SELECTION_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_UFO_NAMELIST_CHANGED,
            methodName="ufoNameListChanged",
            lowLevelEventNames=[EVENT_UFO_NAMELIST_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_UFO_NAMELIST_SELECTION_CHANGED,
            methodName="ufoNameListSelectionChanged",
            lowLevelEventNames=[EVENT_UFO_NAMELIST_SELECTION_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_UFO_NAMELIST_DBLCLICK,
            methodName="ufoNameListDblClick",
            lowLevelEventNames=[EVENT_UFO_NAMELIST_DBLCLICK],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_GLYPH_NAMELIST_CHANGED,
            methodName="glyphNameListChanged",
            lowLevelEventNames=[EVENT_GLYPH_NAMELIST_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_GLYPH_NAMELIST_SELECTION_CHANGED,
            methodName="glyphNameListSelectionChanged",
            lowLevelEventNames=[EVENT_GLYPH_NAMELIST_SELECTION_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
        registerSubscriberEvent(
            subscriberEventName=EVENT_GLYPH_NAMELIST_DBLCLICK,
            methodName="glyphNameListDblClick",
            lowLevelEventNames=[EVENT_GLYPH_NAMELIST_DBLCLICK],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )
                                       
        self.w.filterPatternLabelStart = TextBox((self.M, y, self.CW/3, 24), 'Starts')
        self.w.filterPatternLabelHas = TextBox((self.M+self.CW/3, y, self.CW/3, 24), 'Has')
        self.w.filterPatternLabelEnd = TextBox((self.M+2*self.CW/3, y, self.CW/3, 24), 'Ends')
        self.w.referenceUfo = TextBox((self.C1, y, self.CW, 24), 'Reference UFO')
        self.w.filterItalicUfo = HorizontalRadioGroup((self.C2, y, self.CW, 24), ('Roman', 'Italic'), callback=self.ufoNameListSelectionCallback, sizeStyle='small')
        self.w.filterItalicUfo.set(0)
        y += self.L
        self.w.filterPatternStart = EditText((self.M, y, self.CW/3, 24), continuous=True, callback=self.glyphNameListCallback)
        self.w.filterPatternHas = EditText((self.M+self.CW/3, y, self.CW/3, 24), continuous=True, callback=self.glyphNameListCallback)
        self.w.filterPatternEnd = EditText((self.M+2*self.CW/3, y, self.CW/3, 24), continuous=True, callback=self.glyphNameListCallback)

        # List of currently open fonts, that can be used as reference.
        refNames = getOpenUfoNames()
        self.w.ufoReference = PopUpButton((self.C1, y, self.CW2, 24), refNames, callback=self.ufoReferenceSelectionCallback)
        
        y += self.L*1.2
        self.w.glyphNames = List((self.C0, y, self.CW, self.BROWSER_HEIGHT), items=[], 
            selectionCallback=self.glyphNameListSelectionCallback, doubleClickCallback=self.glyphNameListDblClibkCallback)
        self.w.ufoNames = List((self.C1, y, self.CW2, self.BROWSER_HEIGHT), items=[], 
            selectionCallback=self.ufoNameListSelectionCallback, doubleClickCallback=self.dblClickUfoNamesCallback)
        
        y += self.BROWSER_HEIGHT
        self.w.selectOpenDblClick = RadioGroup((self.C1, y, self.CW2, self.L), ('Open GlyphEditor', 'Open FontWindow'), isVertical=False, sizeStyle='small')
        self.w.selectOpenDblClick.set(0)
        
        return y + self.LL

    def ufoReferenceSelectionCallback(self, sender):
        postEvent(EVENT_UFO_REFERENCE_SELECTION_CHANGED)
    
    def ufoNameListSelectionCallback(self, sender):
        postEvent(EVENT_UFO_NAMELIST_SELECTION_CHANGED)
    
    def glyphNameListCallback(self, sender=None):
        postEvent(EVENT_GLYPH_NAMELIST_CHANGED)
                    
    def glyphNameListSelectionCallback(self, sender=None):
        postEvent(EVENT_GLYPH_NAMELIST_SELECTION_CHANGED)
                    
    def glyphNameListDblClibkCallback(self, sender):
        postEvent(EVENT_GLYPH_NAMELIST_DBLCLICK)
        
    def dblClickUfoNamesCallback(self, sender):
        postEvent(EVENT_UFO_NAMELIST_DBLCLICK)
        
if __name__ == '__main__':
    AssistantController = BaseAssistantController
    OpenWindow(AssistantController)


 