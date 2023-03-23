"""
Window showing info about the current glyph

This example shows a floating window that displays information
about the current glyph. The window knows when the user has
switched the current glyph and updates accordingly. The displayed
information is updated when the data within the current glyph
is changed.
"""

import vanilla
import merz
from mojo.subscriber import Subscriber, WindowController, registerCurrentGlyphSubscriber


class BaseAssistant(Subscriber, WindowController):

    debug = True

    def build(self):
        self.w = vanilla.FloatingWindow((300, 0), "Useless Glyph Data")
        self.pointsView = merz.MerzView("auto", backgroundColor=(0.75, 0.75, 0.75, 1))
        self.nameTextBox = vanilla.TextBox("auto", "")
        self.contoursTextBox = vanilla.TextBox("auto", "")
        self.componentsTextBox = vanilla.TextBox("auto", "")
        self.anchorsTextBox = vanilla.TextBox("auto", "")
        self.guidelinesTextBox = vanilla.TextBox("auto", "")
        views = [
            dict(
                view=self.pointsView,
                height=300,
                gravity="top",
            ),
            self.nameTextBox,
            self.contoursTextBox,
            self.componentsTextBox,
            self.anchorsTextBox,
            self.guidelinesTextBox
        ]
        self.w.stackView = vanilla.VerticalStackView(
            "auto",
            views=views,
            spacing=10,
            alignment="leading"
        )
        metrics = dict(
            margin=15
        )
        rules = [
            "H:|-margin-[stackView]-margin-|",
            "V:|-margin-[stackView]-margin-|"
        ]
        self.w.addAutoPosSizeRules(rules, metrics)

    def started(self):
        self.w.open()

    def currentGlyphDidSetGlyph(self, info):
        self.currentGlyphInfoDidChange(info)
        self.currentGlyphContoursDidChange(info)
        self.currentGlyphComponentsDidChange(info)
        self.currentGlyphAnchorsDidChange(info)
        self.currentGlyphGuidelinesDidChange(info)

    def currentGlyphInfoDidChange(self, info):
        glyph = info["glyph"]
        text = ""
        if glyph is not None:
            text = f"This glyph is named {glyph.name}."
        self.nameTextBox.set(text)

    def currentGlyphContoursDidChange(self, info):
        glyph = info["glyph"]
        text = ""
        if glyph is not None:
            text = f"This glyph contains {len(glyph.contours)} contours."
        self.contoursTextBox.set(text)
        view = self.pointsView
        container = view.getMerzContainer()
        container.clearSublayers()
        if glyph is not None:
            viewWidth = view.width()
            viewHeight = view.height()
            font = glyph.font
            verticalMetrics = [
                font.info.descender,
                font.info.xHeight,
                font.info.capHeight,
                font.info.ascender
            ]
            bottom = min(verticalMetrics)
            top = max(verticalMetrics)
            contentHeight = top - bottom
            fitHeight = viewHeight * 0.8
            scale = fitHeight / contentHeight
            x = (viewWidth - (glyph.width * scale)) / 2
            y = (viewHeight - fitHeight) / 2
            container.setSublayerTransformation((scale, 0, 0, scale, x, y))
            glyphLayer = container.appendRectangleSublayer(
                size=(glyph.width, contentHeight),
                fillColor=(1, 1, 1, 1)
            )
            with glyphLayer.sublayerGroup():
                for contour in glyph.contours:
                    for point in contour.points:
                        if point.type == "move":
                            glyphLayer.appendSymbolSublayer(
                                position=(point.x, point.y),
                                imageSettings=dict(
                                    name="star",
                                    pointCount=8,
                                    size=(100, 100),
                                    fillColor=(1, 1, 0, 0.5)
                                )
                            )
                        elif point.type == "line":
                            glyphLayer.appendSymbolSublayer(
                                position=(point.x, point.y),
                                imageSettings=dict(
                                    name="rectangle",
                                    size=(40, 40),
                                    fillColor=(0, 0, 1, 0.2)
                                )
                            )
                        elif point.type == "curve":
                            glyphLayer.appendSymbolSublayer(
                                position=(point.x, point.y),
                                imageSettings=dict(
                                    name="oval",
                                    size=(50, 50),
                                    fillColor=(0, 1, 0, 0.2)
                                )
                            )
                        elif point.type == "qcurve":
                            glyphLayer.appendSymbolSublayer(
                                position=(point.x, point.y),
                                imageSettings=dict(
                                    name="triangle",
                                    size=(50, 50),
                                    fillColor=(1, 0, 0, 0.2)
                                )
                            )
                        elif point.type == "offcurve":
                            glyphLayer.appendSymbolSublayer(
                                position=(point.x, point.y),
                                imageSettings=dict(
                                    name="oval",
                                    size=(75, 75),
                                    fillColor=None,
                                    strokeColor=(0, 0, 0, 0.2),
                                    strokeWidth=1
                                )
                            )

    def currentGlyphComponentsDidChange(self, info):
        glyph = info["glyph"]
        text = "No glyph selected"
        if glyph is not None:
            text = f"This glyph contains {len(glyph.components)} components"
        self.componentsTextBox.set(text)

    def currentGlyphAnchorsDidChange(self, info):
        glyph = info["glyph"]
        text = ""
        if glyph is not None:
            text = f"This glyph contains {len(glyph.anchors)} anchors."
        self.anchorsTextBox.set(text)

    def currentGlyphGuidelinesDidChange(self, info):
        glyph = info["glyph"]
        text = ""
        if glyph is not None:
            text = f"This glyph contains {len(glyph.guidelines)} guidelines."
        self.guidelinesTextBox.set(text)


registerCurrentGlyphSubscriber(BaseAssistant)

