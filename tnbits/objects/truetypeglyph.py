# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     truetypeglyph.py
#
import weakref
from tnbits.hinting.ttf.program import Program

BIGINT = 10000000000

class DummyPen():

    def moveTo(self, p):
        pass

    def lineTo(self, p):
        pass

    def qCurveTo(self, *args):
        pass

    def closePath(self):
        pass

    def addComponent(self, componentName, transformation):
        pass

class TrueTypePoint(object):
    """
    Contains an (x, y) coordinate and an onCurve boolean.
    """

    def __init__(self, x, y, onCurve=True):
        self.x = x
        self.y = y
        self.onCurve = onCurve

    def __repr__(self):
        return 'Point(%s, %s, %s)' % (self.x, self.y, self.onCurve)

class TrueTypeGlyph(object):
    """
    Represents a single TrueType glyph. Holds the Unicode value if it exists.
    """

    def __init__(self, name, ttglyf, font):
        self._font = weakref.ref(font)
        self.unicode = None # To be assigned if available.
        self.name = name
        self._glyf = ttglyf
        self.width = font.hmtx[name]

    def __repr__(self):
        if self.unicode:
            return 'Glyph(%s, #%04X, %s points)' % (self.name, self.unicode, len(self))
        return 'Glyph(%s, %s points)' % (self.name, len(self))

    def getGlyf(self):
        return self._glyf

    def getPen(self):
        # Not really drawing for now, as we have all the points in place.
        return DummyPen()

    def __setitem(self, index, point):
        assert isinstance(point, TrueTypePoint)
        self.coordinates[index] = [point.x, point.y]
        self._glyf.flags[index] = {True:1, False:0}[bool(point.onCurve)]

    def __getitem__(self, index):
        x, y = self._glyf.coordinates[index]
        return TrueTypePoint(x, y, self._glyf.flags[index])

    def __len__(self):
        if hasattr(self._glyf, 'coordinates'):
            return len(self._glyf.coordinates)
        return 0

    def getGlyfCoordinates(self):
        try:
            return self._glyf.coordinates
        except AttributeError:
            return None

    def getGlyfFlags(self):
        try:
            return self._glyf.flags
        except AttributeError:
            return None

    def getEndPtsOfContours(self):
        try:
            return self._glyf.endPtsOfContours
        except AttributeError:
            return None

    def compare(self, glyph, compareComponents=True, comparePoints=True):
        """Point structures again for every glyph compare. Compares that are fastest and most
        likely to be different."""
        result = []
        numPoints = len(self)
        if self.width != glyph.width:
            result.append('width')

        if (not numPoints and not self.components) or (not len(glyph) and not glyph.components):
            # If both glyphs are empty, we cannot compare, so by definition not equal
            result.append('empty glyph(s)')

        if not result and compareComponents:
            # Compare the components
            if len(self.components) != len(glyph.components):
                result.append('component count')
            else:
                glyphComponents = glyph.components
                for index, component in enumerate(self.components):
                    glyphComponent = glyphComponents[index]
                    if component.x != glyphComponent.x or component.y != glyphComponent.y:
                        result.append('component position')
                        break
                    # Now compare the component references. Note that they come from separate fonts
                    if not component.glyphName in self.font or not glyphComponent.glyphName in glyph.font:
                        result.append('missing component source')
                        break
                    glyph1 = self.font[component.glyphName]
                    glyph2 = glyph.font[glyphComponent.glyphName]
                    compare, reason = glyph1.compare(glyph2, compareComponents=compareComponents, comparePoints=comparePoints)
                    if not compare:
                        result.append('component reference: (%s)' % ', '.join(reason))
                        break

        if not result and comparePoints:
            if numPoints and numPoints != len(glyph):
                result.append('point count')
            else:
                # Compare the points:
                points = self.getGlyfCoordinates()
                glyphPoints = glyph.getGlyfCoordinates()
                # flags = self.getGlyfFlags()
                # glyphFlags = glyph.getGlyfFlags()
                if (points is None and glyphPoints is not None) or (points is None and glyphPoints is not None):
                    result.append('incompatible point lists')
                elif points is not None and glyphPoints is not None:
                    for index, point in enumerate(points):
                        gp = glyphPoints[index]
                        if point[0] != gp[0] or point[1] != gp[1]:
                            # Cannot compare empty glyphs. Otherwise test if the coordinates or flags are different
                            result.append('empty glyph')
                            break

        return not bool(result), result

    def getComponentNames(self):
        """
        Answers the list of component names. Check if the component glyphs also contain components, then add
        these names too. The name of self glyphs is not added to the list. The names answered as a set, to
        remove duplicate glyph references."""
        names = []
        for components in self.components:
            name = components.glyphName
            if name in self.font:  # Run through component chain, in case of multiple levels of reference
                names.append(name)
                names += self.font[name].getComponentNames()
        return set(names)

    def draw(self, pen):
        pass

        # font (weakref)

    def _get_font(self):
        return self._font()

    font = property(_get_font)

        # components

    def _get_components(self):
        components = []
        if hasattr(self._glyf, 'components'):
            for component in self._glyf.components:
                components.append(component)
        return components

    components = property(_get_components)

        # assembly

    def _get_assembly(self):
        return self.program.getAssembly()

    def _set_assembly(self, assembly):
        self.program = program = Program()
        if program is not None:
            program.fromAssembly(program)

    assembly = property(_get_assembly, _set_assembly)

        # program

    def _get_program(self):
        if hasattr(self._glyf, 'program'):
            return self._glyf.program
        return None

    def _set_program(self, program):
        self._glyf.program = program

    program = property(_get_program, _set_program)

        # points

    def _get_points(self):
        points = []
        try:
            flags = self._glyf.flags
            for index, (x, y) in enumerate(self._glyf.coordinates):
                points.append(TrueTypePoint(x, y, flags[index]))
        except AttributeError:  # No coordinates in this glyph: ignore
            pass
        return points

    def _set_points(self, points):
        pts = []
        flags = []
        for point in points:
            pts.append([point.x, point.y])
            flags.append({True:1, False:0}[bool(point.onCurve)])
        self._glyf.coordinates = pts
        self._glyf.flags = flags

    points = property(_get_points, _set_points)

        # bounds

    def _get_bounds(self):
        components = self.components
        found = False
        if components:
            minx = miny = BIGINT
            maxx = maxy = -BIGINT
            for component in components:
                if component.glyphName in self.font:
                    cminx, cminy, cmaxx, cmaxy = self.font[component.glyphName].bounds
                    minx = min(minx, cminx)
                    miny = min(miny, cminy)
                    maxx = max(maxx, cmaxx)
                    maxy = max(maxy, cmaxy)
            found = True
        points = self.points
        if points:
            minx = miny = BIGINT
            maxx = maxy = -BIGINT
            for point in self.points:
                minx = min(minx, point.x)
                maxx = max(maxx, point.x)
                miny = min(miny, point.y)
                maxy = max(maxy, point.y)
            found = True
        if not found:
            minx = miny = maxx = maxy = 0
        return minx, miny, maxx, maxy

    bounds = property(_get_bounds)

        # unicodes

    def _get_unicodes(self):
        return self.font.unicodes.get(self.name, [])

    unicodes = property(_get_unicodes)

        # leftMargin

    def _get_leftMargin(self):
        minx, _, _, _ = self.bounds
        return minx

    leftMargin = property(_get_leftMargin)

    def _get_rightMargin(self):
        _, _, maxx, _ = self.bounds
        return self.width - maxx

    def _set_rightMargin(self, margin):
        _, _, maxx, _ = self.bounds
        self.width = maxx + margin

    rightMargin = property(_get_rightMargin, _set_rightMargin)
