import os


COLORLIBKEY = 'com.typenetwork.colorinfo'


def hasColorInfo(font):
    return COLORLIBKEY in font.lib


def getCachedColorFont(font, create=False):
    nakedFont = font.naked()
    if not hasattr(nakedFont, "_fbColorFont"):
        if create or hasColorInfo(font):
            nakedFont._fbColorFont = ColorFont(font)
        else:
            nakedFont._fbColorFont = None
    return nakedFont._fbColorFont


class ColorFont(object):

    def __init__(self, font):
        self.font = font
        self.layers = []
        self.readFromFontLib()

    def updateLayers(self, layers):
        self.layers = layers

    def newLayerFromFont(self, sourceFont):
        paintStyle = PaintStyle(fillColor=(0, 0, 0, 1))
        layerInfo = ColorFontLayerInfo(sourceFont, "", "foreground", paintStyle, True, False)
        self.layers.append(layerInfo)
        return layerInfo

    def getGlyphWidth(self, glyphName):
        if not self.layers:
            return None
        width = None
        for layer in self.layers:
            if layer.useMetrics:
                width = layer.getGlyphWidth(glyphName)
                break
        if width is None:
            # fall back to the first available width
            for layer in self.layers:
                width = layer.getGlyphWidth(glyphName)
                if width is not None:
                    break
        return width

    def drawGlyph(self, glyphName, drawingTools):
        layers = self.layers
        for layer in layers:
            layer.drawGlyph(glyphName, drawingTools)

    # serializing

    def readFromFontLib(self):
        self.fromDict(self.font.lib.get(COLORLIBKEY, {}))

    def writeToFontLib(self):
        serialized = self.toDict()
        old = self.font.lib.get(COLORLIBKEY, {})
        if old != serialized:
            self.font.lib[COLORLIBKEY] = serialized
            self.font.naked().dirty = True

    def fromDict(self, data):
        layers = []
        for layerDict in data.get("layers", []):
            layerInfo = ColorFontLayerInfo.fromDict(layerDict, self.font)
            layers.append(layerInfo)
        self.updateLayers(layers)

    def toDict(self):
        layerInfoList = []
        for layerInfo in self.layers:
            layerInfoList.append(layerInfo.toDict(self.font))
        return dict(layers=layerInfoList)


class ColorFontLayerInfo(object):

    @classmethod
    def fromDict(cls, data, masterFont):
        sourceFontPath = data.get("sourceFontPath", "")
        if not sourceFontPath:
            sourceFont = masterFont
        else:
            dirName = getFontDirectory(masterFont)
            if dirName:
                sourceFontPath = makeAbsolutePath(sourceFontPath, dirName)
            sourceFont = findSourceFont(sourceFontPath)
        sourceGlyphNameExtension = data.get("sourceGlyphNameExtension", "")
        sourceGlyphLayerName = data.get("sourceGlyphLayerName", "foreground")
        paintStyle = PaintStyle.fromDict(data["paintStyle"])
        visible = data.get("visible", True)
        useMetrics = data.get("useMetrics", False)
        return cls(sourceFont, sourceGlyphNameExtension, sourceGlyphLayerName,
                paintStyle, visible, useMetrics)

    def __init__(self, sourceFont, sourceGlyphNameExtension, sourceGlyphLayerName,
            paintStyle, visible, useMetrics):
        self.sourceFont = sourceFont  # font object
        self.sourceGlyphNameExtension = sourceGlyphNameExtension  # may be ""
        self.sourceGlyphLayerName = sourceGlyphLayerName  # may be "" (= foreground)
        self.paintStyle = paintStyle
        self.visible = visible
        self.useMetrics = useMetrics

    def getGlyph(self, glyphName):
        if self.sourceGlyphNameExtension:
            glyphName += self.sourceGlyphNameExtension
        if glyphName not in self.sourceFont:
            return None
        glyph = self.sourceFont[glyphName]
        if self.sourceGlyphLayerName:
            glyph = glyph.getLayer(self.sourceGlyphLayerName)
        return glyph

    def getGlyphWidth(self, glyphName):
        glyph = self.getGlyph(glyphName)
        if glyph is not None:
            return glyph.width
        else:
            return None

    def drawGlyph(self, glyphName, drawingTools):
        if not self.visible:
            return None
        glyph = self.getGlyph(glyphName)
        if glyph is None:
            return None
        path = glyph.getRepresentation("defconAppKit.NSBezierPath")
        self.paintStyle.set(drawingTools)
        drawingTools.drawPath(path)

    def toDict(self, masterFont):
        data = dict(
            paintStyle=self.paintStyle.toDict(),
        )
        if self.sourceFont != masterFont:
            sourcePath = self.sourceFont.path
            dirName = getFontDirectory(masterFont)
            if dirName:
                sourcePath = makeRelativePath(sourcePath, dirName)
            data['sourceFontPath'] = sourcePath
        if not self.visible:
            data['visible'] = self.visible
        if self.sourceGlyphNameExtension:
            data['sourceGlyphNameExtension'] = self.sourceGlyphNameExtension
        if self.sourceGlyphLayerName and self.sourceGlyphLayerName != "foreground":
            data['sourceGlyphLayerName'] = self.sourceGlyphLayerName
        if self.useMetrics:
            data['useMetrics'] = True
        return data

        
class PaintStyle(object):

    @classmethod
    def fromDict(cls, data):
        fillColor = data.get("fillColor", None)
        if fillColor:
            fillColor = dictToRGBA(fillColor)
        strokeColor = data.get("strokeColor", None)
        if strokeColor:
            strokeColor = dictToRGBA(strokeColor)
        strokeWidth = data.get("strokeWidth", 1)
        return cls(fillColor=fillColor, strokeColor=strokeColor, strokeWidth=strokeWidth)  ### XXX

    def __init__(self, fillColor=None, strokeColor=None, strokeWidth=1):
        self.fillColor = fillColor
        self.strokeColor = strokeColor
        self.doFill = fillColor is not None
        self.doStroke = strokeColor is not None
        self.strokeWidth = strokeWidth

    def toDict(self):
        data = dict()
        if self.doFill:
            data['fillColor'] = rgbaToDict(self.fillColor)
        if self.doStroke:
            data['strokeColor'] = rgbaToDict(self.strokeColor)
            data['strokeWidth'] = self.strokeWidth
        return data

    def set(self, drawingTools):
        # eg. mojo/drawbot-style
        if self.doFill:
            drawingTools.fill(*self.fillColor)
        else:
            drawingTools.fill(None)
        if self.doStroke:
            drawingTools.strokeWidth(self.strokeWidth)
            drawingTools.strokeWidth(30)  # XXXX
            drawingTools.stroke(*self.strokeColor)
        else:
            drawingTools.stroke(None)


def getFontDirectory(font):
    path = font.path
    if path:
        return os.path.dirname(path)
    else:
        return None

def findSourceFont(path):
    # XXX this calls into RF UI code, it should probably use the tnbits font manager
    from mojo.roboFont import AllFonts, OpenFont
    for font in AllFonts():
        if font.path == path:
            return font
    return OpenFont(path)

def makeRelativePath(path, rootDir):
    return os.path.relpath(path, rootDir)

def makeAbsolutePath(path, rootDir):
    path = os.path.join(rootDir, path)
    return os.path.normpath(path)

def rgbaToDict(rgba):
    r, g, b, a = rgba
    return dict(red=r, green=g, blue=b, alpha=a)

def dictToRGBA(data):
    r = data["red"]
    g = data["green"]
    b = data["blue"]
    a = data["alpha"]
    return (r, g, b, a)
