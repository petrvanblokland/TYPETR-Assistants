from mojo.roboFont import OpenWindow
from mojo.subscriber import WindowController
from merz import MerzView
from vanilla import Window

W = H = 300
M = 10
MB = 30

CELL_X = CELL_Y = 20 # Number of cells in the grid
GRID_LINE = 0.25
GRID_COLOR = (0.25, 0.25, 0.25, 1)
DIAGONAL_COLOR = (0.85, 0.85, 0.85, 1)

class CurvePalette(WindowController):

    debug = True
    fillColor = (1, 0, 0, .25)
    brushRadius = 40

    def build(self):
        self.w = Window((W+2*M, H+M+MB), "Curve Palette")
        self.w.view = MerzView(
            (M, M, -M, -MB),
            backgroundColor=(1, 1, 1, 1),
            delegate=self
        )
        container = self.w.view.getMerzContainer()
        cw = W/CELL_X
        for x in range(CELL_X):
            y = x
            container.appendRectangleSublayer(
               position=(x*cw, y*cw),
               size=(cw, cw),
               fillColor=DIAGONAL_COLOR,
            )
        for x in range(CELL_X):
            container.appendLineSublayer(
               startPoint=(x*cw, 0),
               endPoint=(x*cw, H),
               strokeWidth=GRID_LINE,
               strokeColor=GRID_COLOR,
            )
        for y in range(CELL_Y):
            container.appendLineSublayer(
               startPoint=(0, y*cw),
               endPoint=(W, y*cw),
               strokeWidth=GRID_LINE,
               strokeColor=GRID_COLOR,
            )
        self.w.open()

    def acceptsFirstResponder(self, sender):
        # necessary for accepting mouse events
        return True

    def acceptsMouseMoved(self, sender):
        # necessary for tracking mouse movement
        return True

    def destroy(self):
        container = self.w.view.getMerzContainer()
        container.clearSublayers()

    def mouseMoved(self, view, event):
        x, y = event.locationInWindow()
        #self.pointerLayer.setPosition((x, y))

    def mouseDragged(self, view, event):
        x, y = event.locationInWindow()
        #self.pointerLayer.setPosition((x, y))
        #self.brushLayer.appendOvalSublayer(
        #    position=(x, y),
        #    anchor=(.5, .5),
        #    size=(self.brushRadius*2, self.brushRadius*2),
        #    fillColor=self.fillColor
        #)

    def mouseUp(self, view, event):
        pass
        #self.brushLayer.clearSublayers()


if __name__ == '__main__':
    OpenWindow(CurvePalette)
