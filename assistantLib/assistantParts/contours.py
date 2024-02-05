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
from assistantLib.assistantParts.glyphsets.glyphSet_anchors import CONNECTED_ANCHORS, EXAMPLE_DIACRITICS


class AssistantPartContours(BaseAssistantPart):
    """Set startpoint and other contour functions
    """
    MAX_DIACRITICS_CLOUD = 40

    def initMerzContours(self, container):
        """Initialize the Merz instances for this assistant part.""" 
        self.contoursDiacritics = [] # Storage of diacritics images
        for dIndex in range(self.MAX_DIACRITICS_CLOUD): # Max number of diacritics in a glyph. @@@ If too low, some diacritics don't show
            self.contoursDiacritics.append(self.backgroundContainer.appendPathSublayer(
                name='diacritics-%d' % dIndex,
                position=(FAR, 0),
                fillColor=(0, 0, 0.5, 0.2),
            ))

    def updateContours(self, info):
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed
        return self.checkFixContours(g)

    def checkFixContours(self, g):
        changed = False
        changed |= self.checkFixComponents(g)
        changed |= self.checkFixComponentPositions(g)
        return changed

    def buildContours(self, y):
        personalKey_e = self.registerKeyStroke('e', 'contoursSetStartPoint')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.setStartPointButton = Button((C2, y, CW, L), 'Set start [%s]' % personalKey_e, callback=self.contourssSetStartPointCallback)
        y += L*1.5

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
            print(f'... Clear {len(g.components)} component(s) of /{g.name}')
            g.clearComponents()
            changed = True
        # 2
        elif not g.components and gd.components: # Create missing components
            for componentName in gd.components:
                print(f'... Append missing component /{componentName} to /{g.name}')
                g.appendComponent(componentName)
            changed = True
        # 3
        elif len(g.components) > len(gd.components): # More components than necessary
            # g.component cannot be set,  so we following the protocol of deleting selected components.
            obsoleteComponents = len(g.components) - len(gd.components)
            components = g.components  # Convert to a list
            for cIndex, component in enumerate(components):
                if cIndex < len(gd.components): # Keep it?
                    component.selected = False
                else: # Select it to be removed
                    component.selected = True
                    changed = True
            if changed:
                print(f'... Remove {obsoleteComponents} obsolete component(s) in /{g.name}')

            g.removeSelection(removePoints=False, removeAnchors=False, removeImages=False)
        # 4
        elif len(g.components) < len(gd.components): # Fewer components than necessary
            for componentName in gd.components[len(g.components):]:
                print(f'... Append component /{componentName} to /{g.name}')
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
        """For all components check if they are on the right poaition. If the base component has an anchor
        and there are diacritic components that have the matching achor, then move the diacritics
        so the positions of the anchors match up."""
        changed = False
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        dIndex = 0 # Index into showing diacritics Merz layers
        assert gd is not None # Otherwise the glyph data does not exist.
        if not g.components: # This must be a base glyph, check for drawing the diacritics cloud of glyphs that have g as base.
            for a in g.anchors:
                """
                accentGlyph = accentGlyphSrc = f[accentName]
                accentAnchor = getAccentAnchor(accentGlyphSrc, accentName)
                if accentAnchor is None: # Anchor does not exist on the accent glyph yet, create it.
                    self.fixAnchors(accentGlyph)
                    accentAnchor = getAccentAnchor(accentGlyphSrc, accentName)

                gAnchor = getBaseAnchor(g, accentName)

                if accentAnchor is not None and gAnchor is not None and cIndex < len(self.diacritics):
                    diacriticsLayer = self.diacritics[cIndex] # Get layer for this diacritics glyph
                    diacriticsPath = accentGlyph.getRepresentation("merz.CGPath") 
                    diacriticsLayer.setPath(diacriticsPath)
                    ax = gAnchor.x - accentAnchor.x
                    ay = gAnchor.y - accentAnchor.y
                    diacriticsLayer.setPosition((ax, ay))
                    cIndex += 1
                """

        else: # Otherwise the components should match their positions with the corresponding anchors
            for component in g.components:
                pass

        return changed

    def XXXXX(self):
        f = g.font
        gd = getGlyphData(f, g.name)
        if gd is None:
            print('### Missing glyph:', g.name, 'in', f.path.split('/')[-1])
            return False
            
        cIndex = 0 # Index of layer slot, showing diacritics
        for compositeName in gd.composites: # @glyph is the base glyph of theses composite glyphs
            if compositeName not in f:
                f.newGlyph(compositeName)
                print('### Create new glyph /%s' % compositeName)
            self.fixFlourishesCloud(f[compositeName])
            self.fixComponents(f[compositeName]) # Check if it needs something
            # If the compositeName glyph is an exception, not to be positioned by an anchor
            # in the base glyph, then this is indicated by the gs.fixAccents flag set to False
            cgd = getGlyphData(f, compositeName)
            if not cgd.fixAccents: # Skip if flag is False
                continue
            
            accentedGlyphSrc = f[compositeName]
            for accentName in cgd.accents: # This is (one of) the accent for this glyph
                # Match position of the accent anchor with the anchor of mg
                if not accentName in f:
                    f.newGlyph(accentName)
                    print('### Create new accent glyph /%s' % accentName)
                self.fixFlourishesCloud(f[accentName])
                self.fixComponents(f[accentName]) # Check if it needs something
                accentGlyph = accentGlyphSrc = f[accentName]
                accentAnchor = getAccentAnchor(accentGlyphSrc, accentName)
                if accentAnchor is None: # Anchor does not exist on the accent glyph yet, create it.
                    self.fixAnchors(accentGlyph)
                    accentAnchor = getAccentAnchor(accentGlyphSrc, accentName)

                gAnchor = getBaseAnchor(g, accentName)

                if accentAnchor is not None and gAnchor is not None and cIndex < len(self.diacritics):
                    diacriticsLayer = self.diacritics[cIndex] # Get layer for this diacritics glyph
                    diacriticsPath = accentGlyph.getRepresentation("merz.CGPath") 
                    diacriticsLayer.setPath(diacriticsPath)
                    ax = gAnchor.x - accentAnchor.x
                    ay = gAnchor.y - accentAnchor.y
                    diacriticsLayer.setPosition((ax, ay))
                    cIndex += 1
                    # Adjust the components if they are not in the right anchor positions 
                    # Check if the accented glyph has the component on the same position
                    # otherwise correct it.
                    changed = False
                    
                    self.fixFlourishesCloud(accentedGlyphSrc)
                    self.fixComponents(accentedGlyphSrc) # Make sure the necessary component exist.
                    for component in accentedGlyphSrc.components:
                        if component.baseGlyph == accentName:
                            t = list(component.transformation)
                            if abs(t[-2] - gAnchor.x + accentAnchor.x) > 0.5 or abs(t[-1] - gAnchor.y + accentAnchor.y) > 0.5:
                                t[-1] = gAnchor.y - accentAnchor.y
                                t[-2] = gAnchor.x - accentAnchor.x
                                print('... Fix accent position "%s --> %s' % (component.baseGlyph, accentedGlyphSrc.name))
                                component.transformation = t
                                changed = True
                    if changed:
                        accentGlyph.changed()
                        accentGlyphSrc.changed()
                        accentedGlyphSrc.changed()
                        #print(component.baseGlyph, accentedAnchor.x - accentAnchor.x, accentedAnchor.x, accentAnchor.x, t[-2], t[-1] )
                        
        for n in range(cIndex, len(self.diacritics)):
            self.diacritics[n].setPosition((FAR, 0)) # Move the unused layers out of view

        if VERBOSE3 and changed :
            print('+++ Changed by fixAccentCloud', )

        return changed
        
