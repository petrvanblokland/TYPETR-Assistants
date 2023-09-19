# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    glyphsheet.py
#

import traceback
from vanilla import Group
from tnbits.base.constants.tool import *
from tnbits.base.view import View
from tnbits.spreadsheet.spreadsheet import Spreadsheet
from tnbits.spreadsheet.cell import Cell
from tnbits.model.objects.glyph import getContours, getComponents, getPoints, \
       getBounds
from tnbits.model.objects.style import getStyleKey
from tnbits.bites.spreadsheet.constants import *

try:
    from mojo.roboFont import CurrentFont
    from mojo.UI import OpenGlyphWindow
    IN_ROBOFONT = True
except:
    print('Not in RoboFont')
    IN_ROBOFONT = False

W = 5*UNIT + PADDING

def patternMatch(pattern, target, exactMatch=True, ignoreCase=False):
    """Checks if a glyph name matches a selection pattern. Global function,
    should go into other tools as well. Simple matching for now, to be extended
    later."""
    pattern = pattern.strip()
    if not pattern:
        return True
    if ignoreCase:
        pattern = pattern.lower()
        target = target.lower()
    parts = pattern.split(' ')
    match = False
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '*' in part:
            if part.startswith('*') and part.endswith('*'):
                if part[1:-1] in target:
                    match = True
                    break
            elif part.startswith('*'):
                if target.endswith(part[1:]):
                    match = True
                    break
            elif part.endswith('*'):
                if target.startswith(part[:-1]):
                    match = True
                    break
            else: # Break into start and end
                p = part.split('*')
                if target.startswith(p[0]) and target.endswith(p[-1]):
                    match = True
                    break
        elif exactMatch and part == target:
            # Just look for an exact match
            match = True
            break
        elif not exactMatch and part in target:
            match = True
            break

    return match

class GlyphSheet(View):

    def __init__(self, parent, pos=(0, 0, -0, -0), cellChangedCallback=None):
        self.parent = parent
        self.cellChangedCallback = cellChangedCallback

        self.descriptions = None
        self.view = Group(pos)
        self.setSpreadsheet()

    def getController(self):
        return self.parent.controller

    def setSpreadsheet(self):
        self.descriptions = self.getDescriptions()
        self.identifierKey = self.descriptions[0]['key']
        data = self.getData()
        self.spreadsheet = Spreadsheet(self, descriptions=self.descriptions,
                data=data, cellChangedCallback=self.cellChangedCallback,
                doubleClickCallback=self.doubleClickCallback,
                menuItems=self.getMenuItems())
        self.view.spreadsheet = self.spreadsheet

    def getMenuItems(self):
        return [
                dict(title='Open', callback='openCallback:', shortcut='O'),
        ]

    def getData(self, formats=None):
        data = []
        controller = self.getController()
        y = 0

        if controller.style is None:
            return data

        # TODO: sorting that makes sense.
        glyphNames = sorted(controller.style.keys())
        preset = PRESETS[controller.presetName]
        glyphNames = self.filterGlyphNames(glyphNames, preset)

        for glyphName in glyphNames:
            l = self.getGlyphData(glyphName, y)
            data.append(l)
            y += 1
        return data

    def getShortFloat(self, value):
        if isinstance(value, float):
            value = "%.2f" % value

        return value

    def getGlyphData(self, glyphName, y):
        x = 0
        glyph, ga = self.getController().getGlyph(glyphName)
        cell = Cell(identifier=(x, y), value=glyphName)
        l = [cell]
        x += 1

        contours = len(getContours(glyph))
        cell = Cell(identifier=(x, y), value=contours)
        l.append(cell)
        x += 1

        components = len(getComponents(glyph))
        cell = Cell(identifier=(x, y), value=components)
        l.append(cell)
        x += 1

        value = self.getShortFloat(glyph.width)
        cell = Cell(identifier=(x, y), value=value)
        l.append(cell)
        x += 1

        value = self.getShortFloat(glyph.leftMargin)
        cell = Cell(identifier=(x, y), value=value)
        l.append(cell)
        x += 1

        value = self.getShortFloat(glyph.rightMargin)
        cell = Cell(identifier=(x, y), value=value)
        l.append(cell)
        x += 1

        cell = Cell(identifier=(x, y), value=len(getPoints(glyph)))
        l.append(cell)
        x += 1

        bounds = getBounds(glyph)

        if bounds:
            xMin, yMin, xMax, yMax = bounds
        else:
            xMin = None
            yMin = None
            xMax = None
            yMax = None

        value = self.getShortFloat(yMin)
        cell = Cell(identifier=(x, y), value=value)
        l.append(cell)
        x += 1

        value = self.getShortFloat(yMax)
        cell = Cell(identifier=(x, y), value=value)
        l.append(cell)
        x += 1

        stems = None
        bars = None
        roundBars = None
        diagonals = None

        if ga:
            try:
                stems = len(ga.stems)
                bars = len(ga.bars)
                roundBars = len(ga.roundBars)
                diagonals = len(ga.diagonals)
            except Exception as e:
                # TODO: write to errors console.
                print(e)
                print(traceback.format_exc())

        cell = Cell(identifier=(x, y), value=stems)
        l.append(cell)
        x += 1

        cell = Cell(identifier=(x, y), value=bars)
        l.append(cell)
        x += 1

        cell = Cell(identifier=(x, y), value=roundBars)
        l.append(cell)
        x += 1

        cell = Cell(identifier=(x, y), value=diagonals)
        l.append(cell)
        x += 1

        return l

    def getGlyphName(self, cellID):
        """Gets the style ID stored in the cell value"""
        x, y = cellID
        cell = self.spreadsheet[(0, y)]
        return cell.value

    def doubleClickCallback(self, cell):
        glyphName = self.getGlyphName(cell)
        controller = self.getController()
        glyph, ga = controller.getGlyph(glyphName)
        controller.update(updateGlyph=True)

    def filterGlyphNames(self, glyphNames, preset):
        if preset is None:
            return glyphNames
        else:
            matchingGlyphNames = []

            for glyphName in glyphNames:
                if patternMatch(preset, glyphName):
                    matchingGlyphNames.append(glyphName)

            return matchingGlyphNames

    def getDescriptions(self):
        """Sets headers and data structure."""
        descriptions = []
        for h in GLYPHS_HEADERS:
            d = dict(title=h, key=h.lower(), width=100, editable=False)
            descriptions.append(d)

        return descriptions

    def openCallback_(self, menuItem):
        if not IN_ROBOFONT:
            return

        x, y = self.spreadsheet.currentCell
        cellID = (0, y)
        cell = self.spreadsheet[cellID]
        glyphName = cell.value
        style = self.getController().style
        styleKey = getStyleKey(style)
        self.getController().openStyle([styleKey])
        f = CurrentFont()
        g = f[glyphName]
        OpenGlyphWindow(g)

    def update(self):
        """
        TODO: reload spreadsheet contents without deleting.
        """
        self.deleteSpreadsheet()
        self.setSpreadsheet()

    def deleteSpreadsheet(self):
        del self.view.spreadsheet
