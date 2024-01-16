# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR tp_glyphBrowser.py
#
import os

from vanilla import (TextBox, EditText, CheckBox, RadioGroup, HorizontalRadioGroup, PopUpButton, 
    List, FloatingWindow)

# Import the main entry into RoboFont subscriber and window controller classes and functions.
from mojo.subscriber import (Subscriber, WindowController, 
    registerGlyphEditorSubscriber, disableSubscriberEvents, getRegisteredSubscriberEvents,
    unregisterGlyphEditorSubscriber, registerSubscriberEvent)
from mojo.events import postEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint

from assistantLib.baseAssistant import BaseAssistantSubscriber, BaseAssistantController, DEFAULT_KEY
from assistantLib.helpers import *

# GlyphBrowser events
EVENT_UFO_REFERENCE_CHANGED = f"{DEFAULT_KEY}.ufoReferenceChanged"
EVENT_UFO_REFERENCE_SELECTION_CHANGED = f"{DEFAULT_KEY}.ufoReferenceSelectionChanged"
EVENT_UFO_NAMELIST_CHANGED = f"{DEFAULT_KEY}.ufoNameListChanged"
EVENT_UFO_NAMELIST_SELECTION_CHANGED = f"{DEFAULT_KEY}.ufoNameListSelectionChanged"
EVENT_UFO_NAMELIST_DBLCLICK = f"{DEFAULT_KEY}.ufoNameListDblClick"
EVENT_GLYPH_NAMELIST_CHANGED = f"{DEFAULT_KEY}.glyphNameListChanged"
EVENT_GLYPH_NAMELIST_SELECTION_CHANGED = f"{DEFAULT_KEY}.glyphNameListSelectionChanged"
EVENT_GLYPH_NAMELIST_DBLCLICK = f"{DEFAULT_KEY}.glyphNameListDblClick"

class GlyphBrowser(BaseAssistantSubscriber):

    VERBOSE = False

    MAX_OVERLAY_POINTS = 100 # Number point markers to show on an overlay glyph
    POINT_MARKER_R = 4 # Size of point markers

    OVERLAY_FILL_COLOR = 0.7, 0.7, 0.7, 0.5
    PREVIEW_FILL_COLOR = 0, 0, 0, 0.9
    PREVIEW_STROKE_COLOR = 0, 0, 0, 0.8
    PREVIEW_STROKE_WIDTH = 1
    
    def buildAssistant(self):
        """This instance is part of the BaseAssistantController.helpers list, which defines 
        how the Assistant window is building together.
        Build the rest PreviewOverlay assistant by adding Merz objects into the @subscriber.
        The subscriber should be stored in the helper, since there can be many subscribers 
        for one controller. 
        """
        if self.VERBOSE:
            print('--- GlyphBrowser.buildAssistant')
        
        """Register the events for this subscriber. The methodName is the method self.<methodName> responds to."""
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
        self.ufoReferenceChanged()
        self.ufoNameListChanged()

    #   H E L P E R S

    def getReferenceFont(self):
        ref = None
        refName = self.controller.w.ufoReference.getItem()
        if refName is None:
            return None
        # Find the reference font
        for f in AllFonts():
            if getUfoName(f) == refName:
                return f
        return None

    def XXXgetFont(self, path, showInterface=False):
        # Check if the master is already open, by RoboFont or by self
        for f in AllFonts():
            if f.path is not None and f.path.endswith(path):
                #print('... Selecting open font', path)
                return f
        if path in self.openFonts:
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
        self.openFonts[path] = f
        return f
            
    #   E V E N T S

    def ufoReferenceChanged(self, info=None):
        # Event: EVENT_UFO_REFERENCE_CHANGED
        print('--- GlyphBrowser.ufoReferenceChanged')
        refNames = getOpenUfoNames()
        self.controller.w.ufoReference.setItems(refNames)

    def ufoReferenceSelectionChanged(self, info):
        # Event: EVENT_UFO_REFERENCE_SELECTION_CHANGED
        g = self.getGlyph()
        print('--- GlyphBrowser.ufoReferenceSelectionChanged', g.name)

    def ufoNameListChanged(self, info=None):
        """Update the list of UFOs that are in the same folder as the fonts that are currently open.
        Open them in the background if not already open."""
        # Event: EVENT_UFO_NAMELIST_CHANGED
        g = self.getGlyph()

        if self.VERBOSE:
            print('--- GlyphBrowser.ufoNameListChanged', g.name)

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
                ufo = getFont(ufoPath)
                self.glyphNames = self.glyphNames.union(set(ufo.keys()))
                    
        self.controller.w.ufoNames.set(sorted(ufoNames))
        self.glyphNameListChanged()

    def ufoNameListSelectionChanged(self, info):
        # Event: EVENT_UFO_NAMELIST_SELECTION_CHANGED
        if self.VERBOSE:
            print('--- %s.ufoNameListSelectionChanged' % self.__class__.__name__)

    def ufoNameListDblClick(self, info):
        # Event: EVENT_UFO_NAMELIST_DBLCLICK
        if self.VERBOSE:
            print('--- %s.ufoNameListDblClick' % self.__class__.__name__)
        ref = self.getReferenceFont()
        if ref is None:
            return
        dirPath = getUfoDirPath(ref)

        ufoSelected = self.controller.w.ufoNames.getSelection()
        for ufoIndex in ufoSelected:

            ufoPath = dirPath + self.controller.w.ufoNames[ufoIndex]

            if self.controller.w.selectOpenDblClick.get() == 0: # Open selection as EditWindow
                f = getFont(ufoPath, showInterface=True)
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
        if self.VERBOSE:
            print('--- GlyphBrowser.glyphNameListSelectionChanged')
        # Get the new first selected glyph name
        selection = self.controller.w.glyphNames.getSelection()
        if selection and self.controller.w.openGlyphEditor.get():
            gName = self.controller.w.glyphNames[selection[0]]
            f = self.getCurrentFont()
            if gName in f:
                OpenGlyphWindow(f[gName]) # Open the window or change to

    def glyphNameListDblClick(self, info):
        # Event: EVENT_GLYPH_NAMELIST_DBLCLICK
        g = self.getGlyph()
        if self.VERBOSE:
            print('--- GlyphBrowser.glyphNameListDblClick', g.name)


class GlyphBrowserController(BaseAssistantController):

    WINDOW_CLASS = FloatingWindow 
    subscriberClass = GlyphBrowser
    
    H = 400
    BROWSER_BOTTOM = -36

    TITLE = 'TYPETR Glyph Browser'

    def buildUI(self):
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
        if self.VERBOSE:
            print('--- GlyphBrowserController.buildUI')

        y = 0
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
        self.w.glyphNames = List((self.C0, y, self.CW, self.BROWSER_BOTTOM), items=[], 
            selectionCallback=self.glyphNameListSelectionCallback, doubleClickCallback=self.glyphNameListDblClibkCallback)
        self.w.ufoNames = List((self.C1, y, self.CW2, self.BROWSER_BOTTOM), items=[], 
            selectionCallback=self.ufoNameListSelectionCallback, doubleClickCallback=self.dblClickUfoNamesCallback)
        
        self.w.openGlyphEditor = CheckBox((self.C0+4, self.BROWSER_BOTTOM + self.M, self.CW, self.L), 'Open GlyphEditor', value=True, sizeStyle='small')
        self.w.selectOpenDblClick = RadioGroup((self.C1, self.BROWSER_BOTTOM + self.M, self.CW2, self.L), ('Open GlyphEditor', 'Open FontWindow'), isVertical=False, sizeStyle='small')
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
