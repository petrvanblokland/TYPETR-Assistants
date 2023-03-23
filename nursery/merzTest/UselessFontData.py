import vanilla
import merz
import defcon
from mojo.subscriber import Subscriber, WindowController, registerCurrentFontSubscriber

WHITE = (1, 1, 1, 1)
RED = (1, 0, 0, 1)
BLUE = (0, 0, 1, 1)
GREEN = (0, 1, 0, 1)
YELLOW = (1, 1, 0, 1)
CYAN = (0, 1, 1, 1)

class CurrentFontWithUISubscriberDemo(Subscriber, WindowController):

    debug = True

    def build(self):
        self.w = vanilla.FloatingWindow((0, 0), "Useless Font Data")
        self.fontNameTextBox = vanilla.TextBox(posSize="auto", text="")
        self.kerningView = merz.MerzView(posSize="auto")
        self.infoView = merz.MerzView(posSize="auto")
        self.featuresList = vanilla.List(
            "auto",
            items=[],
            columnDescriptions=[
                dict(
                    title="character",
                    width=30
                ),
                dict(
                    title="count"
                )
            ],
            showColumnTitles=False
        )
        self.pointsView = merz.MerzView(
            "auto"
        )
        columnDescriptions = [
            dict(
                columnPlacement="trailing"
            ),
            dict(
                width=100,
                columnPlacement="fill"
            )
        ]
        rows = [
            (
                vanilla.TextBox("auto", "Font:"),
                self.fontNameTextBox
            ),
            dict(
                height=100,
                cells=(
                    vanilla.TextBox("auto", "Kerning:"),
                    self.kerningView
                )
            ),
            dict(
                height=100,
                cells=(
                    vanilla.TextBox("auto", "Font Info:"),
                    self.infoView
                )
            ),
            dict(
                height=100,
                cells=(
                    vanilla.TextBox("auto", "Features:"),
                    self.featuresList
                )
            ),
            dict(
                height=100,
                cells=(
                    vanilla.TextBox("auto", "Outline:"),
                    self.pointsView
                )
            ),
        ]
        self.w.gridView = vanilla.GridView(
            "auto",
            rows,
            columnDescriptions=columnDescriptions,
            columnWidth=75,
            columnSpacing=10,
            rowHeight=25,
            rowSpacing=10
        )
        metrics = dict(
            margin=15
        )
        rules = ["H:|-margin-[gridView]-margin-|",
                 "V:|-margin-[gridView]-margin-|"]

        self.w.addAutoPosSizeRules(rules, metrics)

    def started(self):
        self.w.open()

    def currentFontDidSetFont(self, info):
        font = info["font"]
        if font is not None:
            info["layer"] = font.defaultLayer
        if font is None:
            name = ""
        else:
            name = f"{font.info.familyName}-{font.info.styleName}"
        self.fontNameTextBox.set(name)
        self.currentFontInfoDidChange(info)
        self.currentFontKerningDidChange(info)
        self.currentFontFeaturesDidChange(info)
        self.currentFontLayerDidChange(info)

    def currentFontInfoDidChange(self, info):
        font = info["font"]
        container = self.infoView.getMerzContainer()
        container.clearSublayers()
        if font is None:
            return
        base = container.appendRectangleSublayer(
            name="base",
            position=(0, 0),
            size=(100, 100),
            fillColor=WHITE
        )
        copyright = font.info.copyright
        if copyright is None:
            copyright = ""
        copyright = len(copyright)
        trademark = font.info.trademark
        if trademark is None:
            trademark = ""
        trademark = len(trademark)
        license = font.info.openTypeNameLicense
        if license is None:
            license = ""
        license = len(license)
        total = copyright + trademark + license
        if total:
            copyright /= total
            copyright *= 100
            base.appendRectangleSublayer(
                position=(0, 0),
                size=(100, copyright),
                fillColor=RED
            )
            trademark /= total
            trademark *= 100
            base.appendRectangleSublayer(
                position=(0, copyright),
                size=(100, trademark),
                fillColor=GREEN
            )
            license /= total
            license *= 100
            base.appendRectangleSublayer(
                position=(0, copyright + trademark),
                size=(100, license),
                fillColor=BLUE
            )

    def currentFontKerningDidChange(self, info):
        font = info["font"]
        container = self.kerningView.getMerzContainer()
        container.clearSublayers()
        if font is None:
            return
        negative = 0
        positive = 0
        zero = 0
        for value in font.kerning.values():
            if value > 0:
                positive += 1
            elif value < 0:
                negative += 1
            else:
                zero += 1
        total = sum((negative, positive, zero))
        negativeAngle = 0
        zeroAngle = 0
        if total:
            if negative:
                negativeAngle = negative / total
                negativeAngle *= 360
            if zero:
                zeroAngle = zero / total
                zeroAngle *= 360
        zeroAngle += negativeAngle
        slices = [
            dict(
                startAngle=0,
                endAngle=negativeAngle,
                fillColor=RED
            ),
            dict(
                startAngle=negativeAngle,
                endAngle=zeroAngle,
                fillColor=YELLOW
            ),
            dict(
                startAngle=zeroAngle,
                endAngle=0,
                fillColor=GREEN
            )
        ]
        makePieChart(container, slices)

    def currentFontFeaturesDidChange(self, info):
        font = info["font"]
        items = []
        if font is not None:
            text = font.features.text
            counter = {}
            if text:
                for line in text.splitlines():
                    for c in line:
                        if c not in counter:
                            counter[c] = 0
                        counter[c] += 1
            for character, count in sorted(counter.items()):
                item = dict(character=character, count=str(count))
                items.append(item)
        self.featuresList.set(items)

    def currentFontLayerDidChange(self, info):
        font = info["font"]
        container = self.pointsView.getMerzContainer()
        container.clearSublayers()
        if font is None:
            return
        layer = font.defaultLayer
        counter = {}
        for glyph in layer:
            glyphCounter = glyph.getRepresentation("com.robofont.subscriberDemo.pointCounts")
            for type, count in glyphCounter.items():
                if type not in counter:
                    counter[type] = 0
                counter[type] += count
        colors = dict(
            move=YELLOW,
            line=GREEN,
            curve=BLUE,
            qCurve=RED,
            offcurve=CYAN,
        )
        if not counter:
            slices = []
        else:
            slices = []
            total = sum(counter.values())
            previousAngle = 0
            for type, color in colors.items():
                count = counter.get(type)
                if not count:
                    continue
                angle = previousAngle + (360 * count / total)
                slices.append(dict(
                    startAngle=previousAngle,
                    endAngle=angle,
                    fillColor=color
                ))
                previousAngle = angle
        makePieChart(container, slices)

def makePieChart(container, slices):
    base = container.appendOvalSublayer(
        position=(0, 0),
        size=(100, 100),
        fillColor=WHITE
    )
    for slice in slices:
        fillColor = slice["fillColor"]
        startAngle = slice["startAngle"]
        endAngle = slice["endAngle"]
        pathLayer = base.appendPathSublayer(
            fillColor=fillColor
        )
        pen = pathLayer.getPen()
        pen.moveTo((50, 50))
        pen.arc((50, 50), 50, startAngle, endAngle, clockwise=False)
        pen.closePath()

def getPointCountsFactory(glyph):
    counter = {}
    for contour in glyph:
        for point in contour:
            t = point.segmentType
            if t is None:
                t = "offcurve"
            if t not in counter:
                counter[t] = 0
            counter[t] += 1
    return counter


defcon.registerRepresentationFactory(
    defcon.Glyph,
    "com.robofont.subscriberDemo.pointCounts",
    getPointCountsFactory,
    destructiveNotifications=[
        "Glyph.ContoursChanged"
    ]
)

registerCurrentFontSubscriber(CurrentFontWithUISubscriberDemo)
