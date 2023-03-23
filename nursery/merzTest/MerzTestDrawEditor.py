"""
Visualizing data in the glyph editor

This example shows how to visualize data in the glyph editor.
The visualization is done within the glyph editing space with
the merz library. The visualization is done atop the glyph editor
with the vanilla library. The visualization is updated automatically
when the glyph in the editor is switched and when the data within
the glyph is changed. Different timings are used to demonstrate
optimization possibilities.
"""
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber


class GlyphEditorWithUISubscriberDemo(Subscriber):

    debug = True

    def build(self):
        glyphEditor = self.getGlyphEditor()
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.GlyphEditorDrawingSubscriberDemo.background",
            location="background",
            clear=True
        )
        self.foregroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.GlyphEditorDrawingSubscriberDemo.foreground",
            location="foreground",
            clear=True
        )

    def destroy(self):
        self.backgroundContainer.clearSublayers()
        self.foregroundContainer.clearSublayers()

    def glyphEditorDidSetGlyph(self, info):
        self.backgroundContainer.clearSublayers()
        self.foregroundContainer.clearSublayers()
        glyph = info["glyph"]
        if glyph is None:
            return
        self.glyphEditorGlyphDidChange(info)
        self.glyphEditorGlyphDidChangeInfo(info)
        self.glyphEditorGlyphDidChangeOutline(info)
        self.glyphEditorGlyphDidChangeComponents(info)
        self.glyphEditorGlyphDidChangeAnchors(info)
        self.glyphEditorGlyphDidChangeGuidelines(info)
        self.glyphEditorGlyphDidChangeImage(info)
        self.glyphEditorGlyphDidChangeMetrics(info)
        self.glyphEditorGlyphDidChangeContours(info)

    def glyphEditorGlyphDidChange(self, info):
        pass
    # - editor overlay in upper left corner:
    # -- changes since started editing

    def glyphEditorGlyphDidChangeInfo(self, info):
        pass
    # - editor overlay in lower left corner:
    # -- glyph name and unicodes

    glyphEditorGlyphDidChangeMetricsDelay = 0

    def glyphEditorGlyphDidChangeMetrics(self, info):
        glyph = info["glyph"]
        font = glyph.font
        verticalMetrics = [
            font.info.descender,
            0,
            font.info.xHeight,
            font.info.capHeight,
            font.info.ascender
        ]
        bottom = min(verticalMetrics) - 100
        top = max(verticalMetrics) + 100
        middle = (bottom + top) / 2
        height = top - bottom
        headSegment = height * 0.125
        y1 = bottom
        y2 = bottom + headSegment
        y3 = middle
        y4 = top - headSegment
        y5 = top
        l1 = 0
        l2 = -200
        l3 = -250
        r1 = glyph.width
        r2 = r1 + 200
        r3 = r1 + 250
        pathLayer = self.backgroundContainer.getSublayer("metrics")
        if pathLayer is None:
            pathLayer = self.backgroundContainer.appendPathSublayer(
                fillColor=(1, 1, 0, 0.6),
                name="metrics"
            )
        pen = pathLayer.getPen()
        pen.moveTo((l1, y3))
        pen.lineTo((l2, y1))
        pen.lineTo((l2, y2))
        pen.lineTo((l3, y2))
        pen.lineTo((l3, y4))
        pen.lineTo((l2, y4))
        pen.lineTo((l2, y5))
        pen.closePath()
        pen.moveTo((r1, y3))
        pen.lineTo((r2, y1))
        pen.lineTo((r2, y2))
        pen.lineTo((r3, y2))
        pen.lineTo((r3, y4))
        pen.lineTo((r2, y4))
        pen.lineTo((r2, y5))
        pen.closePath()

    def glyphEditorGlyphDidChangeOutline(self, info):
        pass
    # - editor overlay in upper right corner:
    # -- list of contours with segment counts and bounds
    # -- list of components and bounds

    glyphEditorGlyphDidChangeContoursChangeDelay = 0

    def glyphEditorGlyphDidChangeContours(self, info):
        glyph = info["glyph"]
        containerLayer = self.backgroundContainer.getSublayer("contours")
        if containerLayer is not None:
            containerLayer.clearSublayers()
        else:
            containerLayer = self.backgroundContainer.appendBaseSublayer(
                name="contours"
            )
        segmentColors = [
            (1, 0, 0, 0.5),
            (0, 1, 0, 0.5),
            (0, 0, 1, 0.5),
            (1, 1, 0, 0.5),
            (1, 0, 1, 0.5),
            (0, 1, 1, 0.5)
        ]
        pens = {}
        for color in segmentColors:
            pathLayer = containerLayer.appendPathSublayer(
                fillColor=None,
                strokeColor=color,
                strokeWidth=40
            )
            pens[color] = pathLayer.getPen()
        for contour in glyph.contours:
            if not len(contour.segments):
                continue
            colors = list(segmentColors)
            previous = contour.segments[-1]
            for segment in contour.segments:
                color = colors.pop(0)
                if previous.onCurve is not None:
                    pen = pens[color]
                    previousX = previous.onCurve.x
                    previousY = previous.onCurve.y
                    pen.moveTo((previousX, previousY))
                    points = [(point.x, point.y) for point in segment]
                    if segment.type == "line":
                        pen.lineTo(*points)
                    elif segment.type == "curve":
                        pen.curveTo(*points)
                previous = segment
                colors.append(color)
        for pen in pens.values():
            pen.endPath()

    glyphEditorGlyphDidChangeComponentsDelay = 0

    def glyphEditorGlyphDidChangeComponents(self, info):
        glyph = info["glyph"]
        componentLayer = self.backgroundContainer.getSublayer("components")
        if componentLayer is not None:
            componentLayer.clearSublayers()
        else:
            componentLayer = self.backgroundContainer.appendBaseSublayer(
                name="components"
            )
        for component in glyph.components:
            pathLayer = componentLayer.appendPathSublayer(
                fillColor=(0, 0, 1, 0.1)
            )
            x, y, xMax, yMax = component.bounds
            w = xMax - x
            h = yMax - y
            pen = pathLayer.getPen()
            pen.rect((x, y, w, h))

    def glyphEditorGlyphDidChangeAnchors(self, info):
        glyph = info["glyph"]
        anchorLayer = self.backgroundContainer.getSublayer("anchors")
        if anchorLayer is not None:
            anchorLayer.clearSublayers()
        else:
            anchorLayer = self.backgroundContainer.appendBaseSublayer(
                name="anchors",
                opacity=0.4
            )
        for anchor in glyph.anchors:
            x1 = anchor.x
            y1 = anchor.y
            x2 = x1 - 100
            y2 = y1 - 100
            anchorLayer.appendLineSublayer(
                startPoint=(x1, y1),
                endPoint=(x2, y2),
                strokeColor=(0, 1, 0, 1),
                strokeWidth=5,
                startSymbol=dict(
                    name="star",
                    pointCount=14,
                    size=(40, 40),
                    fillColor=(0, 1, 0, 1)
                ),
                endSymbol=dict(
                    name="oval",
                    size=(20, 20),
                    fillColor=(0, 1, 0, 1)
                )
            )
            text = f"{anchor.name}\n({anchor.x}, {anchor.y})"
            anchorLayer.appendTextLineSublayer(
                position=(x2, y2),
                offset=(-10, -10),
                text=text,
                pointSize=15,
                weight="bold",
                horizontalAlignment="right",
                verticalAlignment="top",
                fillColor=(0, 1, 0, 1)
            )

    def glyphEditorGlyphDidChangeGuidelines(self, info):
        glyph = info["glyph"]
        guidelineLayer = self.backgroundContainer.getSublayer("guidelines")
        if guidelineLayer is not None:
            guidelineLayer.clearSublayers()
        else:
            guidelineLayer = self.backgroundContainer.appendBaseSublayer(
                name="guidelines",
                opacity=0.4
            )
        for guideline in glyph.guidelines:
            x1 = guideline.x
            y1 = guideline.y
            x2 = x1 + 100
            y2 = y1 + 100
            guidelineLayer.appendLineSublayer(
                startPoint=(x1, y1),
                endPoint=(x2, y2),
                strokeColor=(1, 0, 0, 1),
                strokeWidth=5,
                startSymbol=dict(
                    name="triangle",
                    size=(20, 40),
                    fillColor=(1, 0, 0, 1)
                )
            )
            text = f"{guideline.name}\n({guideline.x}, {guideline.y})\n{guideline.angle}°"
            guidelineLayer.appendTextLineSublayer(
                position=(x2, y2),
                offset=(-10, -10),
                padding=(10, 10),
                cornerRadius=15,
                text=text,
                pointSize=15,
                weight="bold",
                horizontalAlignment="left",
                verticalAlignment="bottom",
                fillColor=(1, 1, 1, 1),
                backgroundColor=(1, 0, 0, 1)
            )

    def glyphEditorGlyphDidChangeImage(self, info):
        glyph = info["glyph"]
        image = glyph.image
        textLayer = self.foregroundContainer.getSublayer("image")
        if textLayer is None:
            textLayer = self.foregroundContainer.appendTextBoxSublayer(
                name="image",
                pointSize=15,
                fillColor=(0, 0, 0, 1)
            )
        data = image.data
        if data is None:
            textLayer.setText("")
            return
        data = str(data)[:5000]
        x, y = image.offset
        w = 200
        h = 200
        textLayer.setPosition((x, y))
        textLayer.setSize((w, h))
        textLayer.setText(data)


if __name__ == '__main__':
    registerGlyphEditorSubscriber(GlyphEditorWithUISubscriberDemo)