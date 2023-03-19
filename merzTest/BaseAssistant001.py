import vanilla
import merz
from mojo.subscriber import Subscriber

WindowClass = vanilla.FloatingWindow
WindowClass = vanilla.Window

class BaseAssistant(Subscriber):

    NAME = 'Base Assistant'
    debug = True

    def build(self):
        self.glyph = CurrentGlyph()

        self.w = WindowClass((self.glyph.width/2 + 40, 400), self.NAME, minSize=(50, 300))
        self.merzView = merz.MerzView("auto")

        self.button = vanilla.Button("auto",
                                     "🌛",
                                     callback=self.buttonCallback)

        self.w.stack = vanilla.VerticalStackView(
            (0, 0, 0, 0),
            views=[dict(view=self.merzView), dict(view=self.button)],
            spacing=10,
            edgeInsets=(10, 20, 10, 20)
        )
        container = self.merzView.getMerzContainer()

        # a layer for the glyph and the baseline
        self.backgroundLayer = container.appendBaseSublayer(
            size=(self.glyph.width/2, self.glyph.font.info.unitsPerEm/2),
            backgroundColor=(1, 1, 1, 1)
        )

        self.glyphLayer = self.backgroundLayer.appendPathSublayer(
            position=(0, -self.glyph.font.info.descender/2),
        )
        glyphPath = self.glyph.getRepresentation("merz.CGPath")
        self.glyphLayer.setPath(glyphPath)

        self.lineLayer = self.backgroundLayer.appendLineSublayer(
            startPoint=(0, -self.glyph.font.info.descender/2),
            endPoint=(self.glyph.width/2, -self.glyph.font.info.descender/2),
            strokeWidth=1,
            strokeColor=(1, 0, 0, 1)
        )

    def started(self):
        self.w.open()

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info['glyph']
        glyphPath = self.glyph.getRepresentation("merz.CGPath")
        self.glyphLayer.setPath(glyphPath)
        self.backgroundLayer.setSize((self.glyph.width, self.glyph.font.info.unitsPerEm))
        self.lineLayer.setEndPoint((self.glyph.width, -self.glyph.font.info.descender))

    def _switchToDarkMode(self):
        self.glyphLayer.setFillColor((1, 1, 1, 1))
        self.backgroundLayer.setBackgroundColor((0, 0, 0, 1))

    def _switchToLightMode(self):
        self.glyphLayer.setFillColor((0, 0, 0, 1))
        self.backgroundLayer.setBackgroundColor((1, 1, 1, 1))

    def buttonCallback(self, sender):
        if sender.getTitle() == "🌛":
            self._switchToDarkMode()
            sender.setTitle('🌞')
        else:
            self._switchToLightMode()
            sender.setTitle('🌛')


if __name__ == '__main__':
    BaseAssistant()