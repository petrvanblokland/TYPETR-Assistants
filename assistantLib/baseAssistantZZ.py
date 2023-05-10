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

class BaseAssistantZZ(Subscriber):
    """This class interacts with the glyphs and UFO’s through events. It also holds
    the Merz objects that are drawn in the EditorWindow that belongs to this Assistant subscriber.
    Each EditorWindow gets its own Assistant, so there is not confusion about what the current
    glyph is. 
    All Assistant-Subscriber instances talk to the same AssistantController, sharing the window
    of controls, following up on events. 
    """
    debug = True
    controller = None
    VERBOSE = False # Set to True for debugging the tool

    title = "Assistant"

    openFonts = {} # Storage of fonts that are open to the Assistant, without RF interface.

    glyphNames = [] # Collect the glyph names here for all open fonts.

    FAR = 100000 # Move Merz objects here to get them out of view.
   
    def build(self):
        # Build the Assistant subscriber object
        if self.VERBOSE:
            print('--- build')

        # Get the GlyphEditor that relates to self.
        glyphEditor = self.getGlyphEditor()

        self.foregroundContainer = glyphEditor.extensionContainer(
            identifier="com.typetr.%s.foreground" % self.__class__.__name__,
            location="foreground",
            clear=True
        )
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.typetr.%s.background" % self.__class__.__name__,
            location="background",
            clear=True
        )
        self.buildAssistant() # Build specifics of inheriting assistant classes.

    def buildAssistant(self):
        """Build the rest of the Assistant subscriber, such as adding all Merz drawing object,
        in case the inheriting class wants to draw in the related EditorWindow.
        To be redefined by inheriting Assistant-Subscriber classes.
        Default behavior is to do nothing.
        """
                
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

'''
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
        
    # Event handling if the preview/overlayers is installed in the controller by HAS_PREVIEW_OVERLAYERS_GLYPH = True
    def previewOverlayERSDidChange(self, info):
        if self.VERBOSE:
            print('--- previewOverlayersDidChange')
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
            if self.controller.w.fillLeftOverlayers.get():
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
            if self.controller.w.fillRightOverlayers.get():
                self.previewGlyphRight.setFillColor(self.PREVIEW_FILL_COLOR)
                self.previewGlyphRight.setStrokeColor(None)
            else:
                self.previewGlyphRight.setFillColor(None)
                self.previewGlyphRight.setStrokeColor(self.PREVIEW_STROKE_COLOR)
                self.previewGlyphRight.setStrokeWidth(self.PREVIEW_STROKE_WIDTH)
        else:
            self.previewGlyphRight.setPosition((self.FAR, 0))

        # Show outline preview of the glyph on middle
        overlayersName = self.controller.w.overlayersGlyphName.get()
        if overlayersName == '/?':
            overlayersName = g.name

        pIndex = 0
        if overlayersName and overlayersName in g.font:
            gOverlayers = g.font[overlayersName]
            glyphPathOverlayers = gOverlayers.getRepresentation("merz.CGPath") 
            self.previewOverlayersGlyph.setPath(glyphPathOverlayers)

            if self.controller.w.overlayersAlignment.get() == 0:
                x = 0 # Left aligned 
            elif self.controller.w.overlayersAlignment.get() == 1:
                x = (g.width - gOverlayers.width)/2 # Centered
            else:
                x = g.width - gOverlayers.width # Right aligned
            x += round(self.controller.w.overlayersXSlider.get())
            y = round(self.controller.w.overlayersYSlider.get())
            self.previewOverlayersGlyph.setPosition((x, y))
            self.previewOverlayersGlyph.setFillColor(self.OVERLAYERS_FILL_COLOR)
            # Move point markers to this glyph, as much of the list as we need. 
            for contour in gOverlayers._contours:
                for p in contour._points:
                    #print(pIndex, len(self.previewPointMarkers))
                    self.previewOverlayersPointMarkers[pIndex].setPosition((x+p.x-self.POINT_MARKER_R, p.y-self.POINT_MARKER_R)) 
                    pIndex += 1
        else:
            self.previewOverlayersGlyph.setPosition((self.FAR, 0))            

        # Then hide the rest of the point markers
        for n in range(pIndex, len(self.previewOverlayersPointMarkers)):
            self.previewOverlayersPointMarkers[n].setPosition((self.FAR, 0)) 


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
        refNames = self.getOpenUfoNames()
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
'''

class BaseAssistantController(WindowController):
    """Define the base class the creates the UI window for the assistant tool.
    Inheriting controller classes can define required functions by setting class flags to True.

    This class mostly just defines the window, controls and interactions, calling events
    for the Assistant-Subscriber to perform tasks on glyphs and UFO’s.

    Helpers are generic tools that can perform a series of tasks. They know how to build their
    part of the interface. They instruct the Assistant on which events the want to respond
    and they know how to perform theirs tasks on glyph, current UFO or all UFOs.
    Helpers can draw in the EditorWindow through Merz objects. And they can construct their
    own window or canvas.
    The selection and order of the helpers defines their top-down order in the Assistant window.
    """

    WINDOW_CLASS = Window # Or FloatingWindow
    subscriberClass = BaseAssistantZZ
    debug = True
    
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
    
    TITLE = None # Default is class subscriber class name
    
    def build(self):
        self.w = self.WINDOW_CLASS((self.W, self.H), self.subscriberClass.title)
        self.buildUI()
        self.w.open()

    def buildUI(self):
        pass
        
    def started(self):
        self.subscriberClass.controller = self
        registerGlyphEditorSubscriber(self.subscriberClass)

    def destroy(self):
        unregisterGlyphEditorSubscriber(self.subscriberClass)
        self.subscriberClass.controller = None

    #    P R E V I E W  /  O V E R L A Y
            

    #    B 2 Q 2 B  C O N V E R S I O N
'''
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
        refNames = self.getOpenUfoNames()
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
        
'''
 