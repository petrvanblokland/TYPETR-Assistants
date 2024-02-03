# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   contours.py
#
import sys
from math import *
from vanilla import *
import importlib

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart, FAR


class AssistantPartContours(BaseAssistantPart):
    """Set startpoint and other contour functions
    """
    def initMerzContours(self, container):
        pass

    def updateContours(self, info):
        c = self.getController()
        g = info['glyph']
        if g is None:
            return
        self.checkFixContours(g)

    def checkFixContours(self, g):
        changed = False
        changed |= self.checkFixComponents(g)
        changed |= self.checkFixComponentPositions(g)
        if changed:
            g.changed()

    def buildContours(self, y):
        personalKey_e = self.registerKeyStroke('e', 'contoursSetStartPoint')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.setStartPointButton = Button((C2, y, CW, L), 'Set start [%s]' % personalKey_e, callback=self.contourssSetStartPointCallback)
        y += L

        return y

    #    C O N T O U R S

    def contourssSetStartPointCallback(self, sender):
        g = self.getCurrentGlyph()
        if g is not None:
            self.curvesSetStartPoint(g)

    def contoursSetStartPoint(self, g, c=None, event=None):
        """Set the start point to the selected points on [e]. Auto select the point on [E] key."""
        changed = False
        doSelect = True
        doAuto = c is None or c != c.upper() # Auto select if lowercase of key was used
        selectedContours = []
        autoContours = []
        openContours = []

        g.prepareUndo()
        for cIndex, contour in enumerate(g.contours):
            selected = auto = x = y = None
            points = contour.points
            numPoints = len(points)
            if contour.open: # Just select between the start and end point
                openContours.append((cIndex, contour))
            else:
                for pIndex, point in enumerate(points):
                    if point.type == 'offcurve':
                        continue
                    if point.selected:
                        selected = pIndex
                    if auto is None or x is None or y is None or point.y < y or (point.y == y and point.x < x):
                        auto = pIndex
                        x = point.x
                        y = point.y
                if selected:
                    selectedContours.append((selected, contour))
                if auto:
                    autoContours.append((auto, contour))

        if openContours:
            for cIndex, contour in openContours:
                p0 = contour.points[0]
                p1 = contour.points[-1]
                if p0.y > p1.y or (p0.y == p1.y and p0.x > p1.x):
                    print(f'... Altering startpoint of open contour {cIndex}')
                    contour.reverse()
                    changed = True

        if doAuto: # Find the best match, ignoring any selections
            #print('... %s: Auto start for %d contours' % (glyph.name, len(autoContours)))
            for pIndex, contour in autoContours:
                if pIndex:
                    # Make x show same as angled value in EditorWindow
                    x = contour.points[pIndex].x - int(round((tan(radians(-g.font.info.italicAngle or 0)) * contour.points[pIndex].y)))
                    print(f'... Altering startpoint to {(x, contour.points[pIndex].y)}')
                    contour.naked().setStartPoint(pIndex)
                    changed = True

        elif doSelect and selectedContours: # Uppercase key stroke: only do the selected points
            #print('... %s: Set start for %d contours' % (glyph.name, len(selectedContours)))
            for pIndex, contour in selectedContours:
                contour.naked().setStartPoint(pIndex)
                changed = True

        if changed:
            g.changed()

    def checkFixComponents(self, g):
        """Check the existence of gd.base and gd.accent component. Create them when necessary.
        And delete components that are not defined in the GlyphData.
        These are the checks:
        1 There are components but there should be none
        2 There are no components but there should be one or more
        3 The number of existing components is larger than it should be
        4 The number of existing components is smaller than it should be
        5 The number of components it right,  but their baseGlyph names are wrong
        6 The number and names of existing components are just right
         """
        changed = False
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        if gd is None:
            print(f'### checkFixComponents: Glyph /{g.name} does not exist in glyphset {gd.__class__.__name__}')
            return False
        # 1
        if g.components and not gd.components: # Clear existing components
            print(f'... Clear {len(g.components)} components of /{g.name}')
            g.clearComponents()
            changed = True
        # 2
        elif not g.components and gd.components: # Create missing components
            for componentName in gd.components:
                g.appendComponent(componentName)
            changed = True
        # 3
        elif len(g.components) > len(gd.components): # More components than necessary
            # @@@ Seems to update the whole glyph, recreating the anchorts too?
            components = g.components  # Convert to a list
            g.clearComponents()
            for n in range(len(g.components) - len(gd.components)): # Recontruct the amount components that we need
                print(f'... Remove {len(g.components) - len(gd.components)} component(s) from /{g.name}')
                g.appendComponent(g.baseGlyph, transformation=component.transformation)
            changed = True
        # 4
        elif len(g.components) < len(gd.components): # Fewer components than necessary
            for componentName in gd.components[len(g.components):]:
                print(f'... Add component {componentName} to /{g.name}')
                g.appendComponent(componentName)
            changed = True
        # 5 # Recheck all of the above the for the right baseGlyph reference
        if len(g.components) == len(gd.components): # May still not be eqaul, due to recursive update from lines above.
            for cIndex, component in enumerate(g.components):
                if component.baseGlyph != gd.components[cIndex]:
                    print(f'... Rename component {cIndex} {component.baseGlyph} to {gd.components[cIndex]} in /{g.name}')
                    component.baseGlyph = gd.components[cIndex]
                    changed = True
        # 6 All done
        return changed

    def checkFixComponentPositions(self, g):
        """For all components check if they are in place. If the base component has an anchor
        and there are diacritic components that have the matching achor, then move the diacritics
        so the positions of the anchors match up."""
        if not g.components: # This must be a base glyph, check for drawing the diacritics cloud of glyphs that have g as base.
            pass
        else:
            for component in g.components:
                pass

        return False