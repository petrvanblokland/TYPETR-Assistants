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
#    variations.py
#

import traceback

from tnbits.base.view import View
from tnbits.base.constants.colors import *
from tnbits.canvas.canvas import Canvas
from tnbits.canvas.kit import CanvasKit
from tnbits.canvas.slider import Slider
from tnbits.canvas.eventhandler import CanvasEventHandler
from tnbits.model.storage.otfstorage import OTFStorage
from tnbits.spreadsheet.cell import EditCell

PADDING = 30

class Variations(View):
    """Canvas showing variations controls."""

    def __init__(self, controller):
        self.controller = controller
        self.kit = CanvasKit()
        self.canvas = Canvas((0, 0, -0, -0), delegate=self, canvasSize=(300,
            300), flipped=True, backgroundColor=NSColor.whiteColor())
        self.eventHandler = CanvasEventHandler(self.canvas)
        self.sliders = {}
        self.setEditCell()

    def setEditCell(self):
        """Editable cell to be moved to a cell position on enter."""
        # FIXME: should be drawn on the canvas view.
        self.editCell = EditCell((0, 0, 30, 20), "", callback=self.editCellCallback)
        self.editCell.editCellEnded = self.closeEditCell
        self.editCell.show(False)
        self.editCellIsVisible = False

    def openEditCell(self, bla):
        self.editCell.setPosSize((0, 0, 30, 20))
        self.editCell.set('bla')
        self.editCell.show(True)
        self.editCell.getNSTextField().becomeFirstResponder()
        self.editCellIsVisible = True
        #print('opened %s' % self.editCell)

    def editCellCallback(self, sender):
        """Processes cell contents during edit?"""
        #escapeKey = chr(53)
        pass

    def closeEditCell(self):
        pass

    def getController(self):
        return self.controller

    def update(self):
        self.canvas.update()

    def getView(self):
        return self.canvas.getScrollView()

    def setStyle(self, style):
        if not style:
            return

        if not hasattr(style, 'storage') or not isinstance(style.storage, OTFStorage):
            return

        if not style in self.sliders:
            self.initSliders(style)
        else:
            self.setSliderValues(style)

    def initSliders(self, style):
        x = PADDING
        y = PADDING
        boxWidth = 150
        self.sliders[style] = []

        for key, values in style.axes.items():
            minValue, defaultValue, maxValue = values
            p0 = (x, y)
            p1 = (x + boxWidth, y)
            slider = Slider(self, self.kit, key, p0, p1, minValue=minValue,
                    defaultValue=defaultValue, maxValue=maxValue,
                    updateCallback=self.sliderCallback, flipped=True)
            self.sliders[style].append(slider)
            y += 30

    def setSliderValues(self, style):
        for slider in self.getSliders():
            axisID = slider.identifier
            value = style.location[axisID]
            #print(value)
            #slider.set(value)

    def getSliders(self):
            s = self.controller.style

            if s in self.sliders:
                return self.sliders[s]

            return []

    def draw(self, rect):
        try:
            for slider in self.getSliders():
                slider.draw()
            if not self.editCellIsVisible:
                self.openEditCell('bla')
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def sliderCallback(self, pct):
        style = self.controller.style
        l = {}

        for slider in self.getSliders():
            axisID = slider.identifier
            value = slider.getValue()
            l[axisID] = value

        style.setLocation(l)

    def mouseDown(self, event):
        """Checks if a pin is selected."""
        mouse = self.eventHandler.mouseDown(event)
        self.kit.clearSelected()

        for o in self.kit.objects:
            if isinstance(o, Slider):
                if o.on(mouse):
                    o.select()
                    o.update(mouse)

        self.update()

    def mouseDragged(self, event):
        """Checks if a pin is selected and drags within range.
        """
        mouse = self.eventHandler.mouseDragged(event)

        for o in self.kit.objects:
            if isinstance(o, Slider):
                if not o.isSelected:
                    continue

                o.update(mouse)

        self.update()
