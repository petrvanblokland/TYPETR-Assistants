# -*- coding: UTF-8 -*-

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
    SPACER_LABEL_SIZE = 18
    SPACER_MARKER_R = 22 # Radius of space marker

    # Dictionaries with spacing values and names of glyphs. To be redefined by inheriting assistant classes.
    # These tables can be redefined by inheriting spacer classes
    SPACER_FIXED_MARGIN_LEFT_PATTERNS = {
        0:  ('enclosingkeycapcomb',)
    }
    SPACER_FIXED_MARGIN_RIGHT_PATTERNS = {
        0:  ('enclosingkeycapcomb',)
    }
    SPACER_FIXED_WIDTH_PATTERNS = {
        0: ('cmb|', 'comb|', '.component'), # "|" matches pattern on end of name"
        650: ('.tab|', '.tnum|')
    }

    def initMerzSpacer(self, container):
        """Define the Merz elements for feedback about where margins/width comes from."""
        self.registerKeyStroke('=', 'spacerCenterGlyph')

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

        #changed |= self.checkFixGlyphLeftMargin(g)
        #changed |= self.checkFixGlyphRightMargin(g)
        changed |= self.checkFixGlyphWidth(g)
        if changed:
            g.changed()

    def buildSpacer(self, y):
        """Build the assistant UI for anchor controls."""
        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L
        LL = 18
 
        self.w.autoSpace = CheckBox((C0, y, CW, L), 'Auto space', value=True, sizeStyle='small')
        y += L + LL

        return y

    #   G U E S S  W I D T H S

    def _fixGlyphWidth(self, g, width):
        if g.width != width:
            print(f'... Fix glyph width: Set /{g.name} width from {g.width} to {width}')
            g.width = width
            return True
        return False

    def _fixLeftMargin(self, g, lm):
        if abs(g.angledLeftMargin - lm) >= 1:
            print(f'... Fix left margin: Set /{g.name} from {g.angledLeftMargin} to {lm}')
            g.angledLeftMargin = lm
            return True
        return False

    def _fixRightMargin(self, g, rm):
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
        for width, patterns in self.SPACER_FIXED_WIDTH_PATTERNS.items(): # Predefined list by inheriting assistant class
            for pattern in patterns:
                if (pattern.endswith('|') and g.name.endswith(pattern[:-1])) or pattern in g.name:
                    changed |= self._fixGlyphWidth(g, width)
                    label = 'Width=%d' % g.width
                    color = self.SPACER_FIXED_WIDTH_MARKER_COLOR
                    break
            if changed:
                break

        self.fixedSpaceMarkerRight.setPosition((g.width - self.SPACER_MARKER_R, -self.SPACER_MARKER_R))
        self.fixedSpaceMarkerRight.setFillColor(color)
        self.rightSpaceSourceLabel.setText(label)
        self.rightSpaceSourceLabel.setPosition((g.width, -self.SPACER_MARKER_R*1.5))

        return changed

    def checkFixGlyphLeftMargin(self, g, fixedGlyphs=None):
        """Check if this glyph should have spacing altered. If it has components, then fix those first.
        If something changed, then answer True."""
        if fixedGlyphs is None: # Optization to not re-check glyphs are are already done.
            fixedGlyphs = set()
        if g.name in fixedGlyphs: # Already done this one, back out
            return False
        fixedGlyphs.add(g.name)
        changed = False
        for component in g.components:
            if component.baseGlyph in fixedGlyph:
                continue
            if not component.baseGlyph in g.font:
                print('### Missing base blyph /{component.baseGlyph} in /{g.name}')
                continue
            baseG = g.font[component.baseGlyph]
            self.checkFixGlyphLeftMargin(baseG) # Recursively check-fix the spacing of the base glyph

        # Now we check all the components that may influence the margins, check on the glyph itself.
        # First we do all hard coded rules

        for width, patterns in self.SPACER_FIXED_WIDTH_PATTERNS.items(): # Predefined list by inheriting assistant class
            for pattern in patterns:
                if pattern.endswith('|') and g.name.endswith(pattern[:-1]):
                    changed |= self._fixGlyphWidth(g, width)
                    return True
                if pattern in g.name:
                    self._fixGlyphWidth(g, width)
                    return True
        return False

        if g.name in self.SPACER_ZERO_WIDTH:
                return self._fixGlyphWidth(g, 0)
        # Nothing defined, try to guess based on name
        for pattern in self.SPACER_ZERO_WIDTH_END_PATTERNS:
            if g.name.endswith(pattern):
                return self._fixGlyphWidth(g, 0)
        for pattern in self.SPACER_ZERO_WIDTH_PATTERNS:
            if pattern in g.name:
                return self._fixGlyphWidth(g, 0)

        return False

    def checkFixGlyphLeftMargin(g):
        pass

    def checkFixGlyphRightMargin(g):
        pass

    def spacerCenterGlyph(self, g, c, event):     
        """Snap the selected points of the current glyph onto points that are within range on the background glyph."""
        lm = g.angledLeftMargin
        rm = g.angledRightMargin
        w = g.width
        if lm is not None:
            g.angledLeftMargin = (lm + rm)/2
            g.width = w
            g.changed()
