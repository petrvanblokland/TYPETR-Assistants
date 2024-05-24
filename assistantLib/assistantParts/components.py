# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   components.py
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

from assistantLib.assistantParts.baseAssistantPart import BaseAssistantPart
from assistantLib.assistantParts.glyphsets.anchorData import AD


class AssistantPartComponents(BaseAssistantPart):
    """Fix components, positions and baseGlyph. Add component and delete components as defined in the GlyphData.
    """

    def initMerzComponents(self, container):
        """Initialize the Merz instances for this assistant part.""" 

    def updateComponents(self, info):
        c = self.getController()
        g = info['glyph']
        if g is None:
            return False # Nothing changed
        return self.checkFixComponents(g)

    def checkFixComponents(self, g):
        changed = False
        changed |= self.checkFixComponentsExist(g)
        changed |= self.checkFixComponentsPosition(g)
        return changed

    def buildComponents(self, y):
        #personalKey_c = self.registerKeyStroke('c', 'componentFixAllKey')
        personalKey_C = self.registerKeyStroke('C', 'componentFixGlyphAllMastersKey')

        C0, C1, C2, CW, L = self.C0, self.C1, self.C2, self.CW, self.L

        c = self.getController()
        c.w.checkFixAllMasterComponents = CheckBox((C1, y, CW, L), f'Fix all masters [{personalKey_C}]', value=True, sizeStyle='small')
        c.w.autoFixComponentPositions = CheckBox((C2, y, CW, L), 'Auto fix components', value=True, sizeStyle='small')
        y += L + L/5
        c.w.componentsEndLine = HorizontalLine((self.M, y, -self.M, 1))
        c.w.componentsEndLine2 = HorizontalLine((self.M, y, -self.M, 1)) # Double for slightly darker line
        y += L/5

        return y

    #   C O M P O N E N T S

    def componentFixGlyphAllMastersKey(self, g, c=None, event=None):
        """Fix the components for all glyphs in the current font."""
        self.componentFixGlyphAllMasters(g)
    
    def componentFixGlyphAllMasters(self, g):
        """Fix the components for the current glyph in all masters in ufo/"""
        if self.getController().w.checkFixAllMasterComponents.get():
            fonts = []
            parentPath = self.filePath2ParentPath(g.font.path)
            for fIndex, pth in enumerate(self.getUfoPaths(parentPath)):
                fullPath = self.path2FullPath(pth)
                f = self.getFont(fullPath, showInterface=g.font.path == fullPath) # Make sure RoboFont opens the current font.
                fonts.append(f)
        else:
            fonts = [g.font]

        for f in fonts:
            if g.name in f:
                #print(f"... Check/fix components for /{g.name} in {f.path.split('/')[-1]}")
                gg = f[g.name]
                changed = self.checkFixComponentsExist(gg)
                changed |= self.checkFixComponentsPosition(gg)
                gg.changed()

    def componentFixAllKey(self, g, c=None, event=None):
        """Fix the components for all glyphs in the current font."""
        changed = self.componentFixAll(g.font)
        if changed:
            g.font.changed()

    def componentFixAll(self, f):
        """Fix the components for all glyphs in the current font."""
        fontChanged = False
        for g in f:
            changed = self.checkFixComponentsExist(g)
            changed |= self.checkFixComponentsPosition(g)
            if changed:
                fontChanged = True
                g.changed()
        return fontChanged

    def checkFixComponentsExist(self, g):
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
        c = self.getController()
        if c is None: # Controller may have been closed
            return False # Nothing changed

        changed = False
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        if gd is None:
            print(f'### checkFixComponents: Glyph /{g.name} does not exist in glyphset {gd.__class__.__name__}')
            return False
        # Check if autofixing
        if not c.w.autoFixComponentPositions.get():
            return False

        # 1
        if g.components and not gd.components: # Clear existing components
            print(f'... Clear {len(g.components)} component(s) of /{g.name}')
            g.clearComponents()
            changed = True
        # 2
        elif not g.components and gd.components: # Create missing components
            for componentName in gd.components:
                assert componentName != g.name, (f'### Component can not refer to itself {componentName}')
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
                    print(f'... Rename component {cIndex} /{component.baseGlyph} to /{gd.components[cIndex]} in /{g.name}')
                    component.baseGlyph = gd.components[cIndex]
                    changed = True
        # 6 All done
        return changed

    def checkFixComponentsPosition(self, g):
        """For all components check if they are on the right poaition. If the base component has an anchor
        and there are diacritic components that have the matching achor, then move the diacritics
        so the positions of the anchors match up."""
        c = self.getController()
        changed = False
        md = self.getMasterData(g.font)
        gd = md.glyphSet.get(g.name)
        # Check if autofixing
        dIndex = 0 # Index into showing diacritics Merz layers
        assert gd is not None, (f'### Glyph data for /{g.name} not found') # Otherwise the glyph data does not exist.
        if not g.components: # This must be a base glyph, check for drawing the diacritics cloud of glyphs that have g as base.
            """
            # Here stuff goes to checkFix the position of all glyphs that have the current glyph as component
            for a in g.anchors:
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

        elif gd.autoFixComponentPositions and c.w.autoFixComponentPositions.get():
            # Otherwise the components should match their positions with the corresponding anchors
            assert gd.base, (f'### Missing base in glyphData of /{g.name}. If there are components, there always must be a base glyph defined.')
            baseG = g.font[gd.base]
            baseAnchors = self.getAnchorsDict(baseG) # Collect the anchors that are used in the base glyph
            found = False
            tx = ty = 0 # Just to be sure, although there always should be a base glyph defined to get the base ofsset from.
            for component in g.components:
                if component.baseGlyph == gd.base: # Skip the base component, after getting its offset
                    tx, ty = component.transformation[-2:]
                    continue
                componentGlyph = g.font[component.baseGlyph]
                for a in componentGlyph.anchors:
                    if a.name in AD.DIACRITICS_ANCHORS:
                        baseAnchor = self.getCorrespondingAnchor(baseG, a.name) # Find the corresponding anchor in the base glyph _TOP --> TOP_ 
                        if baseAnchor is not None: # Did we find a matching pair, then move the component accordingly
                            dx = baseAnchor.x - a.x + tx # Add transformation of the base glyph
                            dy = baseAnchor.y - a.y + ty
                            t = list(component.transformation)
                            if abs(t[-2] - dx) > 1 or abs(t[-1] - dy) > 1: # Is moving needed?
                                print(f'... Move component /{component.baseGlyph} in /{g.name} to ({dx}, {dy})')
                                t[-2] = dx
                                t[-1] = dy 
                                component.transformation = t
                                found = changed = True
                                break
                    if found:
                        break

        return changed

