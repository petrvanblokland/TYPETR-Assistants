# -*- coding: UTF-8 -*-
#
#    Bogie Assistant for Gauge N
#
# 
import sys
import importlib
from math import *

from vanilla import *
import drawBot

from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

# Decide on the type of window for the Assistant.
WindowClass = Window # Will hide behind other windows, if not needed.
#WindowClass = FloatingWindow # Is always available, but it can block the view of other windows if the Asistant window grows in size.

W, H = 450, 300
M = 20
BW = 200 - 2*M # Button width
BH = 24 # Button height
FAR = 100000 # Put drawing stuff outside the window
CENTER_POS = 15000
AXIS_HEIGHT = 310
MAX_CENTERLINES = 50
MAX_TANK_COMPARTIMENTS = 20
TRACK_WIDTH = 900
TANK_CENTER_HEIGHT = 800 + 1800/2
TANK_LENGTH = 9030
BOGIE_DISTANCE = 5966 # Distance between the bogie centers

WHEEL_COLOR = 0.5, 0.5, 0.5, 0.4
LAGER_COLOR = 0.5, 0.6, 0.5, 0.5
TRACK_COLOR = 0.3, 0.4, 0.7, 0.2
OVERLAY_COLOR = 0.3, 0.4, 0.7, 0.4
TANK_COLOR = 0.4, 0.1, 0.6, 0.4

CENTER_LINE_COLOR = 1, 0, 0, 1
TANK_COMPARTIMENT_LINE_COLOR = 0, 0.5, 0, 1
        
class BogieAssistant(Subscriber):

    def build(self):

        glyphEditor = self.getGlyphEditor()
        
        self.foregroundContainer = container = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        
        self.backgroundContainer = background = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )
        
        # Wheels
        
        self.wheelImage1 = background.appendPathSublayer(
            name='wheel1',
            position=(FAR, 0),
            fillColor=WHEEL_COLOR,
            strokeColor=None,
        )
        self.wheelImage2 = background.appendPathSublayer(
            name='wheel2',
            position=(FAR, 0),
            fillColor=WHEEL_COLOR,
            strokeColor=None,
        )
        self.wheelImage3 = background.appendPathSublayer(
            name='wheel3',
            position=(FAR, 0),
            fillColor=WHEEL_COLOR,
            strokeColor=None,
        )

        # Lagers
        
        self.lagerLeft = background.appendPathSublayer(
            name='lagerLeft',
            position=(FAR, 0),
            fillColor=LAGER_COLOR,
            strokeColor=None,
        )
        self.lagerRight = background.appendPathSublayer(
            name='lagerRight',
            position=(FAR, 0),
            fillColor=LAGER_COLOR,
            strokeColor=None,
        )

        # Sides (e.g. viewing from top)
        
        self.sides = background.appendPathSublayer(
            name='sides.top',
            position=(FAR, 0),
            fillColor=LAGER_COLOR,
            strokeColor=None,
        )

        # Quarters, quarterBottomRight --> .base 
        
        self.quarterTopRight = background.appendPathSublayer(
            name='quarterTopRight',
            position=(0, 0),
            fillColor=TRACK_COLOR,
            strokeColor=None,
        )
        self.quarterTopLeft = background.appendPathSublayer(
            name='quarterTopLeft',
            position=(0, 0),
            fillColor=TRACK_COLOR,
            strokeColor=None,
        )
        self.quarterBottomLeft = background.appendPathSublayer(
            name='quarterBottomLeft',
            position=(0, 0),
            fillColor=TRACK_COLOR,
            strokeColor=None,
        )

        # Overlay
        
        self.overlay = background.appendPathSublayer(
            name='overlay',
            position=(0, 0),
            fillColor=OVERLAY_COLOR,
            strokeColor=None,
        )
                
        # Track
        
        self.trackImage = background.appendPathSublayer(
            name='trackImage',
            position=(0, 0),
            fillColor=TRACK_COLOR,
            strokeColor=None,
        )

        # Tank image
        self.tankImage = background.appendPathSublayer(
            name='tankImage',
            position=(0, 0),
            fillColor=TANK_COLOR,
            strokeColor=None,
        )
                
        # Center lines
        
        self.centerLines = []
        for n in range(MAX_CENTERLINES):
            self.centerLines.append(background.appendLineSublayer(
                name='centerLine%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 0),
                strokeWidth=1,
                strokeColor=CENTER_LINE_COLOR
            ))

        # Tank compartiments
        
        self.tankCompartiments = []
        for n in range(MAX_TANK_COMPARTIMENTS):
            self.tankCompartiments.append(background.appendLineSublayer(
                name='tankCompartiment%d' % n,
                startPoint=(FAR, 0),
                endPoint=(FAR, 0),
                strokeWidth=1,
                strokeColor=TANK_COMPARTIMENT_LINE_COLOR
            ))
        
    #self.glyphEditorGlyphDidChange(info)
    #self.glyphEditorGlyphDidChangeInfo(info)
    #self.glyphEditorGlyphDidChangeOutline(info)
    #self.glyphEditorGlyphDidChangeComponents(info)
    #self.glyphEditorGlyphDidChangeAnchors(info)
    #self.glyphEditorGlyphDidChangeGuidelines(info)
    #self.glyphEditorGlyphDidChangeImage(info)
    #self.glyphEditorGlyphDidChangeMetrics(info)
    #self.glyphEditorGlyphDidChangeContours(info)
    
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        self.update(g)
           
    def glyphEditorDidSetGlyph(self, info):
        g = info['glyph']
        self.update(g)
                    
    def update(self, g):
        
        # Wheel left & lager
        try:
            dist1 = int(self.controller.w.wheelDistance1.get())
        except ValueError:
            dist1 = FARs
        try:
            dist2 = int(self.controller.w.wheelDistance2.get())
        except ValueError:
            dist2 = FAR

        overlayName = self.controller.w.overlay.get()
        if not overlayName:
            if g.name.endswith('.top'):
                overlayName = 'tankCombined.top'
            elif g.name.endswith('.side'):
                overlayName = 'tankCombined.side'
            elif g.name.endswith('.front'):
                overlayName = 'tankCombined.front'
        if overlayName and overlayName in g.font:
            overlay = g.font[overlayName]
            overlayImage = overlay.getRepresentation("merz.CGPath")
            self.overlay.setPath(overlayImage)
            self.overlay.setPosition((0, 0))
        else:
            self.overlay.setPosition((FAR, 0))
            
        tankCompartiments = (-1317, -1017, -170, 170, 886, 1407, 2983, 4559, 5080, 5796, 6136, 6983, 7283)
                        
        if g.name.endswith('.side'):
            
            lines = (
                # Start, end
                ((dist1, -CENTER_POS), (dist1, CENTER_POS)), # #3 Left wheel center                
                ((dist2, -CENTER_POS), (dist2, CENTER_POS)), # #4 Right wheel center                
                ((dist1+BOGIE_DISTANCE, -CENTER_POS), (dist1+BOGIE_DISTANCE, CENTER_POS)), # #3 Left wheel center                
                ((dist2+BOGIE_DISTANCE, -CENTER_POS), (dist2+BOGIE_DISTANCE, CENTER_POS)), # #4 Right wheel center                
                ((0, -CENTER_POS), (0, CENTER_POS)), # Vertical origin
                ((BOGIE_DISTANCE, -CENTER_POS), (BOGIE_DISTANCE, CENTER_POS)), # #4 Right bogie wheel center                
                ((-1148+TANK_LENGTH/2, 0), (-1148+TANK_LENGTH/2, 3000)), # Horizontal center of tank
                ((-CENTER_POS, 0), (CENTER_POS, 0)), # Baseline
                ((-CENTER_POS, AXIS_HEIGHT), (CENTER_POS, AXIS_HEIGHT)), # Center track
                ((-CENTER_POS, TANK_CENTER_HEIGHT), (CENTER_POS, TANK_CENTER_HEIGHT)), # Vertical center tank
            )
            wheels = g.font['wheels.side']
            wheelsImage = wheels.getRepresentation("merz.CGPath")

            lager = g.font['lager.side']
            lagerImage = lager.getRepresentation('merz.CGPath')

            self.wheelImage1.setPath(wheelsImage)
            self.wheelImage1.setPosition((dist1, 0))            

            self.wheelImage2.setPath(wheelsImage)
            self.wheelImage2.setPosition((dist2, 0))            

            self.lagerLeft.setPath(lagerImage)
            self.lagerLeft.setPosition((dist1, 0))

            self.lagerRight.setPath(lagerImage)
            self.lagerRight.setPosition((dist2, 0))

            # Remove from view
            self.sides.setPosition((FAR, 0))
            self.quarterTopRight.setPosition((FAR, 0))
            self.quarterTopLeft.setPosition((FAR, 0))
            self.quarterBottomLeft.setPosition((FAR, 0))
            self.tankImage.setPosition((FAR, 0))

        elif g.name.endswith('.front'):
            tankCompartiments = []
            lines = (
                ((-CENTER_POS, 0), (CENTER_POS, 0)), # Baseline
                ((-CENTER_POS, AXIS_HEIGHT), (CENTER_POS, AXIS_HEIGHT)), # Center track
                ((0, -CENTER_POS), (0, CENTER_POS)), # Vertical center
                ((-TRACK_WIDTH/2, -CENTER_POS), (-TRACK_WIDTH/2, CENTER_POS)), # #3 Left wheel center                
                ((TRACK_WIDTH/2, -CENTER_POS), (TRACK_WIDTH/2, CENTER_POS)), # #4 Right wheel center                
            )
            wheels = g.font['wheels.front']
            wheelsImage = wheels.getRepresentation("merz.CGPath")
            lager = g.font['lager.front']
            lagerImage = lager.getRepresentation('merz.CGPath')

            self.wheelImage1.setPath(wheelsImage)
            self.wheelImage1.setPosition((0, 0))

            self.lagerLeft.setPath(lagerImage)
            self.lagerLeft.setPosition((0, 0))

            tank = g.font('tankBaseFork.bottom')
            self.tankImage = tank.getRepresentation('merz.CGPath')
            
            # Remove from view
            self.wheelImage2.setPosition((FAR, 0))
            self.lagerRight.setPosition((FAR, 0))
            self.sides.setPosition((FAR, 0))
            self.quarterTopRight.setPosition((FAR, 0))
            self.quarterTopLeft.setPosition((FAR, 0))
            self.quarterBottomLeft.setPosition((FAR, 0))

        else: # Top view
            lines = (
                # Start, end
                ((-CENTER_POS, 0), (CENTER_POS, 0)), # Track 1
                ((-CENTER_POS, 900), (CENTER_POS, 900)), # Track 2
                ((0, -CENTER_POS), (0, CENTER_POS)), # Vertical center
                ((dist1, -CENTER_POS), (dist1, CENTER_POS)), # #3 Left wheel center                
                ((dist2, -CENTER_POS), (dist2, CENTER_POS)), # #4 Right wheel center                
                ((dist1+BOGIE_DISTANCE, -CENTER_POS), (dist1+BOGIE_DISTANCE, CENTER_POS)), # #3 Left wheel center                
                ((dist2+BOGIE_DISTANCE, -CENTER_POS), (dist2+BOGIE_DISTANCE, CENTER_POS)), # #4 Right wheel center                
                ((-CENTER_POS, 450), (CENTER_POS, 450)), # Center track
                # Verical buffer positions
                ((-CENTER_POS, -100), (CENTER_POS, -100)), 
                ((-CENTER_POS, 1000), (CENTER_POS, 1000)), 
            )
            wheels = g.font['wheels']
            wheelsImage = wheels.getRepresentation("merz.CGPath")
            lager = g.font['lager']
            lagerImage = lager.getRepresentation('merz.CGPath')
            sides = g.font['sides.top']
            sidesImage = sides.getRepresentation('merz.CGPath')

            self.wheelImage1.setPath(wheelsImage)
            self.wheelImage1.setPosition((dist1, 0))
            self.lagerLeft.setPath(lagerImage)
            self.lagerLeft.setPosition((dist1, 0))

            self.wheelImage2.setPath(wheelsImage)
            self.wheelImage2.setPosition((dist2, 0))
            self.lagerRight.setPath(lagerImage)
            self.lagerRight.setPosition((dist2, 0))

            self.sides.setPath(sidesImage)
            self.sides.setPosition((0, 0))

        for n, (start, end) in enumerate(lines):
            self.centerLines[n].setStartPoint(start)
            self.centerLines[n].setEndPoint(end)

        for n, x in enumerate(tankCompartiments):
            self.tankCompartiments[n].setStartPoint((x, 3000))
            self.tankCompartiments[n].setEndPoint((x, -500))

        quarterName = g.name.replace('.base', '.tr')
        found = False
        if g.name != quarterName and quarterName in g.font:
            gg = g.font[quarterName]
            if gg.components:
                gg.components[0].transformation = (1, 0, 0, -1, 0, 900)
                gg.components[0].baseGlyph = g.name
                gg.changed()
                image = g.font[quarterName].getRepresentation('merz.CGPath')
                self.quarterTopRight.setPath(image)
                self.quarterTopRight.setPosition((0, 0))
                found = True            
        if not found:
            self.quarterTopRight.setPosition((FAR, 0))
            
        quarterName = g.name.replace('.base', '.tl')
        found = False
        if g.name != quarterName and quarterName in g.font:
            gg = g.font[quarterName]
            if gg.components:
                gg.components[0].transformation = (-1, 0, 0, -1, 0, 900)
                gg.components[0].baseGlyph = g.name
                gg.changed()
                image = g.font[quarterName].getRepresentation('merz.CGPath')
                self.quarterTopLeft.setPath(image)
                self.quarterTopLeft.setPosition((0, 0))
                found = True            
        if not found:
            self.quarterTopLeft.setPosition((FAR, 0))
            
        quarterName = g.name.replace('.base', '.bl')
        found = False
        if g.name != quarterName and quarterName in g.font:
            gg = g.font[quarterName]
            if gg.components:
                gg.components[0].transformation = (-1, 0, 0, 1, 0, 0)
                gg.components[0].baseGlyph = g.name
                gg.changed()
                image = g.font[quarterName].getRepresentation('merz.CGPath')
                self.quarterBottomLeft.setPath(image)
                self.quarterBottomLeft.setPosition((0, 0))
                found = True            
        if not found:
            self.quarterBottomLeft.setPosition((FAR, 0))
            

        #try:
        #    dist3 = int(self.controller.w.wheelDistance3.get())
        #except ValueError:
        #    dist3 = FAR
        #self.wheelImage3.setPath(image)
        #self.wheelImage3.setPosition((dist3, 0))
        
        track = g.font['track']
        image = track.getRepresentation("merz.CGPath")
        self.trackImage.setPath(image)
        if self.controller.w.showTrack.get():
            x = -track.width/2
        else:
            x = FAR
        self.trackImage.setPosition((x, 0))

                
L = 22
M = 8 # Margin of UI and gutter of colums
CW = (W-4*M)/3
C0 = M
C1 = C0 + CW + M
C15 = C0 + (CW + M) * 1.5
C2 = C1 + CW + M

class BogieAssistantController(WindowController):

    assistantGlyphEditorSubscriberClass = BogieAssistant
    
    NAME = 'Bogie Assistant (N)'

    def build(self):        

        f = CurrentFont()
        g = CurrentGlyph()
        
        y = M
        self.w = WindowClass((W, H), self.NAME, minSize=(W, H))

        self.w.wheelDistanceLabel = TextBox((C0, y, CW, 24), 'Wheel distances', sizeStyle='small')

        y += L
        self.w.wheelDistance1 = EditText((C0, y, CW, 24), '-580', callback=self.updateEditorCallback)
        self.w.wheelDistance2 = EditText((C1, y, CW, 24), '580', callback=self.updateEditorCallback)
        self.w.wheelDistance3 = EditText((C2, y, CW, 24), '', callback=self.updateEditorCallback)
        y += L
        self.w.showTrack = CheckBox((C0, y, CW, 24), 'Show Track', callback=self.updateEditorCallback)
        y += L
        self.w.overlayLabel = TextBox((C0, y, CW, 24), 'Overlay glyph', sizeStyle='small')
        y += L
        self.w.overlay = EditText((C0, y, CW, 24), '', callback=self.updateEditorCallback)
        
        self.w.open()
        
    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None
    
    def updateEditorCallback(self, sender):
        g = CurrentGlyph()
        if g is not None:
            g.changed()
                                   
if __name__ == '__main__':
    OpenWindow(BogieAssistantController)
