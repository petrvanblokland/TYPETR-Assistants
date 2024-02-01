# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   spacer.py
#
import sys
from math import *
from vanilla import *

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR
from assistantLib.assistantParts.data import * # Import anchors names

class AssistantPartSpacer(BaseAssistantPart):
    """The Spacer assistant part handles all margins and widths that can be automated.
    It makes guesses based on the names of glyphs, existing components, values in the MasterData
    and Erik van Blokland's Similarity.
    The assistant part gives feedback about where the automated values came from, so it's easier to debug.
    """

    SPACER_FIXED_WIDTH_MARKER_COLOR = 0.5, 0.5, 0.5, 0.5
    SPACER_FIXED_MARGIN_MARKER_COLOR = 0.8, 0.2, 0.4, 0.7
    SPACER_LABEL_SIZE = 18
    SPACER_MARKER_R = 22 # Radius of space marker

    def initMerzSpacer(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""

        self.fixedSpaceMarkerLeft = container.appendOvalSublayer(name="spaceMarkerLeft",
            position=(-self.SPACER_MARKER_R, -self.SPACER_MARKER_R),
            size=(self.SPACER_MARKER_R*2, self.SPACER_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.leftSpaceSourceLabel = container.appendTextLineSublayer(name="leftSpaceSourceLabel",
            position=(FAR, -self.SPACER_MARKER_R*2),
            text='LSB',
            font='Courier',
            pointSize=self.SPACER_LABEL_SIZE,
            fillColor=(0, 0, 0, 1),
        )
        self.leftSpaceSourceLabel.setHorizontalAlignment('center')
        
        self.fixedSpaceMarkerRight = container.appendOvalSublayer(name="spaceMarkerRight",
            position=(1000-self.SPACER_MARKER_R, -self.SPACER_MARKER_R),
            size=(self.SPACER_MARKER_R*2, self.SPACER_MARKER_R*2),
            fillColor=None,
            strokeColor=None,
            strokeWidth=1,
        )
        self.rightSpaceSourceLabel = container.appendTextLineSublayer(name="rightSpaceSourceLabel",
            position=(FAR, -self.SPACER_MARKER_R*2),
            text='RSB',
            font='Courier',
            pointSize=self.SPACER_LABEL_SIZE,
            fillColor=(0, 0, 0, 1),
        )
        self.rightSpaceSourceLabel.setHorizontalAlignment('center')

    def updateSpacer(self, info):
        """If the checkbox is set, then try to check and fix automated margins and width."""
        g = info['glyph']
        if g is None:
            return
        changed = False

        changed |= self.checkFixGlyphLeftMargin(g)
        changed |= self.checkFixGlyphRightMargin(g)
        changed |= self.checkFixGlyphWidth(g)
        if changed:
            g.changed()

    KEY_CENTER_GLYPH = '='

    def buildSpacer(self, y):
        """Build the assistant UI for anchor controls."""
        personalKey = self.registerKeyStroke(self.KEY_CENTER_GLYPH, 'spacerCenterGlyph')

        c = self.getController()
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
        c.w.centerGlyphButton = Button((C0, y, CW, L), 'Center width [%s]' % personalKey, callback=self.spacerCenterGlyphCallback)
        c.w.autoSpace = CheckBox((C1, y, CW, L), 'Auto space', value=True, sizeStyle='small')
        y += L + LL

        return y

    #   G U E S S  S P A C I N G  &  K E R N I N G

    def _fixGlyphWidth(self, g, width):
        if g.width != width:
            print(f'... Fix glyph width: Set /{g.name} width from {g.width} to {width}')
            g.width = width
            return True
        return False

    def _fixGlyphLeftMargin(self, g, lm):
        if abs(g.angledLeftMargin - lm) >= 1:
            print(f'... Fix left margin: Set /{g.name} from {g.angledLeftMargin} to {lm}')
            g.angledLeftMargin = lm
            return True
        return False

    def _fixGlyphhRightMargin(self, g, rm):
        if abs(g.angledRightMargin - rm) >= 1:
            print(f'... Fix left margin: Set /{g.name} from {g.angledRightMargin} to {rm}')
            g.angledRightMargin = rm
            return True
        return False

    def checkFixGlyphWidth(self, g):
        """Check if this glyph should have its width altered. If it has components, then fix those first.
        If something changed, then answer True."""
        changed = False
        label = ''
        color = 0, 0, 0, 0
        km = self.getKerningManager(g.font)
        width = km.getWidth(g)
        if width is not None:
            changed = self._fixGlyphWidth(g, width)
            label = 'Width=%d' % g.width
            color = self.SPACER_FIXED_WIDTH_MARKER_COLOR

        self.fixedSpaceMarkerRight.setPosition((g.width - self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setPosition((g.width, -self.SPACER_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setText(label)

        return changed

    def checkFixGlyphLeftMargin(self, g):
        changed = False
        label = ''
        color = 0, 0, 0, 0
        km = self.getKerningManager(g.font)
        lm = km.getLeftMargin(g)
        if lm is not None:
            changed = self._fixGlyphLeftMargin(g, lm)
            label = 'Left=%d' % g.width
            color = self.SPACER_FIXED_MARGIN_MARKER_COLOR

        self.fixedSpaceMarkerLeft.setPosition((-self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setPosition((0, -self.SPACER_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setText(label)

        return False

    def checkFixGlyphRightMargin(self, g):
        changed = False
        label = ''
        color = 0, 0, 0, 0
        km = self.getKerningManager(g.font)
        lm = km.getLeftMargin(g)
        if lm is not None:
            changed = self._fixGlyphLeftMargin(g, lm)
            label = 'Right=%d' % g.width
            color = self.SPACER_FIXED_MARGIN_MARKER_COLOR

        self.fixedSpaceMarkerLeft.setPosition((-self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setPosition((0, -self.SPACER_MARKER_R*1.5))
        self.rightSpaceSourceLabel.setText(label)


        return False
    
    def spacerCenterGlyphCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.spacerCenterGlyhph(g)

    def spacerCenterGlyph(self, g, c, event):     
        """Snap the selected points of the current glyph onto points that are within range on the background glyph."""
        lm = g.angledLeftMargin
        rm = g.angledRightMargin
        w = g.width
        if lm is not None:
            g.angledLeftMargin = (lm + rm)/2
            g.width = w
            g.changed()
