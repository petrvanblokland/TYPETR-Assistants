# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#    TYPETR tp_previewOverlay.py
#

from vanilla import TextBox, EditText, CheckBox, RadioGroup, Slider

# Import the main entry into RoboFont subscriber and window controller classes and functions.
from mojo.subscriber import (Subscriber, WindowController, 
    registerGlyphEditorSubscriber, disableSubscriberEvents, getRegisteredSubscriberEvents,
    unregisterGlyphEditorSubscriber, registerSubscriberEvent)
from mojo.events import postEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint

from assistantLib.baseAssistant import BaseAssistant, BaseAssistantController, DEFAULT_KEY
from assistantLib.helpers import *

# PreviewOverlay events
EVENT_PREVIEW_OVERLAY_CHANGED = f"{DEFAULT_KEY}.previewOverlayChanged"

class PreviewOverlay(BaseAssistant):

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
            print('--- buildAssistant')

        # This is the place in the current related EditorWindow for Merz objects to draw.
        bcg = self.backgroundContainer 

        # Build the Merz objects, depending on the functions defined in the controller.
        # Previewing current glyphs on left/right side.        
        self.previewGlyphLeft = bcg.appendPathSublayer(
            position=(self.FAR, 0),
            fillColor=(0, 0, 0, 1), # Default as filled black
        )
        self.overlayGlyph = bcg.appendPathSublayer(
            position=(self.FAR, 0),
            fillColor=None, # Default as outline
            strokeColor=(0, 0.5, 0, 1),
            strokeWidth=1,
        )
        self.previewGlyphRight = bcg.appendPathSublayer(
            position=(self.FAR, 0),
            fillColor=(0, 0, 0, 1), # Default as filled black
        )
        self.overlayPointMarkers = []
        for pIndex in range(self.MAX_OVERLAY_POINTS): # Max number of points to display in a glyph
            self.overlayPointMarkers.append(bcg.appendRectangleSublayer(name="previewOverlayPoint%03d" % pIndex,
                position=(self.FAR, 0),
                size=(2 * self.POINT_MARKER_R, 2 * self.POINT_MARKER_R),
                fillColor=None,
                strokeColor=(0, 0.5, 0, 1), # 
                strokeWidth=1,
            ))
        
        """Register the events for this subscriber. The methodName is the method self.<methodName> responds to."""
        registerSubscriberEvent(
            subscriberEventName=EVENT_PREVIEW_OVERLAY_CHANGED,
            methodName="previewOverlayDidChange",
            lowLevelEventNames=[EVENT_PREVIEW_OVERLAY_CHANGED],
            dispatcher="roboFont",
            documentation="Send when the Assistant UI did change parameters.",
            delay=0,
            debug=True
        )

    def glyphEditorDidSetGlyph(self, info):
        if self.VERBOSE:
            print('--- PreviewOverlay.glyphEditorDidSetGlyph /%s' % info['glyph'].name)
        self.previewOverlayDidChange(info)

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
            if self.controller.w.fillPreviewLeft.get():
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
            if self.controller.w.fillPreviewRight.get():
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
            self.overlayGlyph.setPath(glyphPathOverlay)

            if self.controller.w.overlayAlignment.get() == 0:
                x = 0 # Left aligned 
            elif self.controller.w.overlayAlignment.get() == 1:
                x = (g.width - gOverlay.width)/2 # Centered
            else:
                x = g.width - gOverlay.width # Right aligned
            x += round(self.controller.w.overlayXSlider.get())
            y = round(self.controller.w.overlayYSlider.get())
            self.overlayGlyph.setPosition((x, y))
            self.overlayGlyph.setFillColor(self.OVERLAY_FILL_COLOR)
            # Move point markers to this glyph, as much of the list as we need. 
            for contour in gOverlay._contours:
                for p in contour._points:
                    #print(pIndex, len(self.previewPointMarkers))
                    self.overlayPointMarkers[pIndex].setPosition((x+p.x-self.POINT_MARKER_R, p.y-self.POINT_MARKER_R)) 
                    pIndex += 1
        else:
            self.overlayGlyph.setPosition((self.FAR, 0))            

        # Then hide the rest of the point markers
        for n in range(pIndex, len(self.overlayPointMarkers)):
            self.overlayPointMarkers[n].setPosition((self.FAR, 0)) 

class PreviewOverlayController(BaseAssistantController):

    subscriberClass = PreviewOverlay

    # Left/right position of the slider
    MIN_PREVIEW_ALIGN = -500
    MAX_PREVIEW_ALIGN = 500
    
    H = 180
    
    TITLE = 'TYPETR Preview & Overlay'

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
            print('--- PreviewOverlayController.buildUI')

        y = 0
        self.w.previewGlyphLeftLabel = TextBox((self.C0, y, self.CW, self.L), 'Preview Left /?')
        self.w.overlayGlyphLabel = TextBox((self.C1, y, self.CW, self.L), 'Overlay /?')
        self.w.previewGlyphRightLabel = TextBox((self.C2, y,self.CW, self.L), 'Preview Right /?')

        y += self.L
        self.w.previewGlyphLeftName = EditText((self.C0, y, self.CW, self.L), callback=self.previewOverlayCallback)
        self.w.overlayGlyphName = EditText((self.C1, y, self.CW, self.L), callback=self.previewOverlayCallback)
        self.w.previewGlyphRightName = EditText((self.C2, y, self.CW, self.L), callback=self.previewOverlayCallback)

        y += self.L
        self.w.fillPreviewLeft = CheckBox((self.C0+4, y, self.CW, self.L), 'Fill Left', value=True, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.flipOverlayH = CheckBox((self.C1+4, y, self.CW, self.L), 'Flip V', value=False, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.flipOverlayV = CheckBox((self.C1 + self.CW/2, y, self.CW, self.L), 'Flip H', value=False, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.fillPreviewRight = CheckBox((self.C2+4, y, self.CW, self.L), 'Fill Right', value=True, sizeStyle='small', 
            callback=self.previewOverlayCallback)

        y += self.L
        self.w.previewKerned = CheckBox((self.C0+4, y, self.CW, self.L), 'Preview kerned', value=False, sizeStyle='small', 
            callback=self.previewOverlayCallback)
        self.w.overlayAlignment = RadioGroup((self.C1, y, self.CW, self.L), ('L', 'C', 'R'), isVertical=False, sizeStyle='small', 
            callback=self.previewOverlayRadioCallback)
        self.w.overlayAlignment.set(0)
        self.w.snapKeyLabel = TextBox((self.C2 + self.CW/4, y, self.CW/2, self.L), 'Snap key')
        self.w.snapKey = EditText((self.C2, y, self.CW/4, self.L), 'G', sizeStyle='small')

        y += self.L*1.2        
        # Vertical position of overlays
        self.w.overlayYSliderLabel = TextBox((self.C0, y+4, 16, self.L), 'Y', sizeStyle='small')
        self.w.overlayYSlider = Slider((self.C0+16, y, -self.M, self.L), 
            minValue=self.MIN_PREVIEW_ALIGN, maxValue=self.MAX_PREVIEW_ALIGN, value=0, sizeStyle='small', 
            continuous=True, callback=self.previewOverlayCallback, tickMarkCount=11)
        y += self.L*1.2    
        # Horizontal position of overlays
        self.w.overlayXSliderLabel = TextBox((self.C0, y+4, 16, self.L), 'X', sizeStyle='small')
        self.w.overlayXSlider = Slider((self.C0+16, y, -self.M, self.L), 
            minValue=self.MIN_PREVIEW_ALIGN, maxValue=self.MAX_PREVIEW_ALIGN, value=0, sizeStyle='small', 
            continuous=True, callback=self.previewOverlayCallback, tickMarkCount=11)
        y += self.L*1.2        
        # Rotation of overlays
        self.w.overlayRSliderLabel = TextBox((self.C0, y+4, 16, self.L), '↻', sizeStyle='small')
        self.w.overlayRSlider = Slider((self.C0+16, y, -self.M, self.L), 
            minValue=self.MIN_PREVIEW_ALIGN, maxValue=self.MAX_PREVIEW_ALIGN, value=0, sizeStyle='small', 
            continuous=True, callback=self.previewOverlayCallback, tickMarkCount=360/45)

    def previewOverlayCallback(self, sender):
        postEvent(EVENT_PREVIEW_OVERLAY_CHANGED)

    def previewOverlayRadioCallback(self, sender):
        """Reset the sliders."""
        self.w.overlayXSlider.set(0)
        self.w.overlayYSlider.set(0)
        self.w.overlayRSlider.set(0)
        postEvent(EVENT_PREVIEW_OVERLAY_CHANGED)



