# This interfaces to the RoboFont font compiler code; mostly doodleFontCompiler.

from copy import deepcopy
from defcon import Font as DefConFont, Glyph as DefConGlyph, Lib as DefConLib
from defcon import Contour as DefConContour, Point as DefConPoint, Anchor as DefConAnchor, Component as DefConComponent
from feaPyFoFum import compileFeatures
from lib.tools.misc import RoboFontError
from lib.tools.defaults import getDefault
from lib.fontObjects.doodleFontCompiler import DoodleOTFFontCompiler, DoodleTTFFontCompiler, DoodlePFAFontCompiler, DoodleVFBCompiler
from lib.tools.bezierTools import roundValue


# Minimal implementations to satisfy the doodleFontCompiler

class Point(DefConPoint):
    def round(self, multiple=1):
        self.x = roundValue(self.x, multiple)
        self.y = roundValue(self.y, multiple)

class Component(DefConComponent):
    def round(self, multiple=1):
        pass  # TODO

class Anchor(DefConAnchor):
    def round(self, multiple=1):
        pass  # TODO

class Contour(DefConContour):
    def join(self):
        if self.open:
            raise ValueError("open paths are not yet supported")  # TODO

    def round(self, multiple=1):
        for p in self:
            p.round(multiple)


class Glyph(DefConGlyph):

    _segmentType = None  # placeholder
    def _get_segmentType(self):
        if self._segmentType is None:
            self._segmentType = self.getParent()._guessedCurveType
        return self._segmentType
    def _set_segmentType(self, segmentType):
        self._segmentType = segmentType
    segmentType = property(_get_segmentType, _set_segmentType)

    template = False

    def round(self, multiple=1):
        for contour in self:
            contour.round(multiple)
        for component in self.components:
            component.round(multiple)
        for anchor in self.anchors:
            anchor.round(multiple)
        self.width = roundValue(self.width, multiple)

    def reverse(self):
        for contour in self:
            contour.reverse()


class Lib(DefConLib):

    def serialize(self):
        return deepcopy(self._dict)

    def deserialize(self, data):
        self._dict = data


def generateFontFromUFO(ufoPath, outputPath, format="otf", decompose=False, checkOutlines=False, autohint=False,
        releaseMode=False, glyphOrder=None, progressBar=None, useMacRoman=False):

    inputFont = DefConFont(ufoPath, glyphClass=Glyph, libClass=Lib, glyphContourClass=Contour, glyphPointClass=Point,
            glyphComponentClass=Component, glyphAnchorClass=Anchor)

    inputFont._guessedCurveType = guessCurveType(inputFont)
    return generateFont(inputFont, path=outputPath, format=format, decompose=decompose,
            checkOutlines=checkOutlines, autohint=autohint,
            releaseMode=releaseMode, glyphOrder=glyphOrder, progressBar=progressBar, useMacRoman=useMacRoman)


def generateFont(inputFont, path=None, format="otf", decompose=False, checkOutlines=False, autohint=False,
        releaseMode=False, glyphOrder=None, progressBar=None, useMacRoman=False):
    """
    Generate a font binary font file from a defcon Font instance.
    - formats are: otf, ttf, woff, eot (the last two aren't yet supported)
    - checkOutlines: removes the overlap
    - autoHint: autoHints the font
    - releaseMode: set the release mode flag
    - glyphOrder: an glyph order
    - progressBar: a progressbar instance, required is an .update().
    """
    if path is None:
        raise RoboFontError("Generating a font requires a path to save the binary font.")

    if glyphOrder is not None:
        if useMacRoman:
            _glyphOrder = list(glyphOrder)
            glyphOrder = [n for n in MacRoman.MacRoman if n in _glyphOrder]
            noneMacRomanGlyphOrder = [n for n in _glyphOrder if n not in glyphOrder]
            glyphOrder.extend(noneMacRomanGlyphOrder)

    savePartsNextToUFO = getDefault("saveFDKPartsNextToUFO", False)
    shouldDecomposeWithCheckOutlines = False

    if format == "otf":
        compiler = DoodleOTFFontCompiler(savePartsNextToUFO=savePartsNextToUFO)
        decompose = False
        shouldDecomposeWithCheckOutlines = True
        if not _canFDKAutoHint(inputFont):  # XXXX defcon
            autohint = False
    elif format == "ttf":
        compiler = DoodleTTFFontCompiler(savePartsNextToUFO=savePartsNextToUFO)
        if autohint and not haveTTFAutoHint:
            autohint = False
    elif format == "pfa":
        compiler = DoodlePFAFontCompiler(savePartsNextToUFO=savePartsNextToUFO)
        decompose = False
        shouldDecomposeWithCheckOutlines = True
        if not _canFDKAutoHint(inputFont):
            autohint = False
    elif format == "vfb":
        compiler = DoodleVFBCompiler()
        checkOutlines = False
        decompose = False
        autohint = False
        shouldDecomposeWithCheckOutlines = False
    # elif format == "woff":
    #     compiler = DoodleWOFFFontCompiler(savePartsNextToUFO=savePartsNextToUFO)
    # elif format == "eot":
    #     compiler = DoodleEOTFontCompiler(savePartsNextToUFO=savePartsNextToUFO)
    else:
        raise RoboFontError("Not supported format (%s)" % format)

    outputFont = prepareCompile(inputFont, format, decompose=decompose, checkOutlines=checkOutlines,
            progressBar=progressBar, shouldDecomposeWithCheckOutlines=shouldDecomposeWithCheckOutlines)

    reports = compiler.compile(outputFont, path, autohint=autohint, releaseMode=releaseMode,
            progressBar=progressBar, glyphOrder=glyphOrder)

    del outputFont

    report = []
    if reports:
        report.append("-"*20)
        for key in ("parts", "checkOutlines", "autohint", "ttfautohint", "makeotf", "otf2pfa", "vfb2ufo"):
            value = reports.get(key)
            if value:
                report.append("")
                report.append("%s Report" % key)
                report.append("")
                report.append(value.strip())
                report.append("")
        report.append("-"*20)
    report = "\n".join(report)
    return report


def prepareCompile(inputFont, format, decompose=False, checkOutlines=False,  progressBar=None, shouldDecomposeWithCheckOutlines=False):
    if progressBar is not None:
        progressBar.update("Preparing...")

    # TODO: this copying may be skippable if we're running from a one-shot script.
    outputFont = inputFont.__class__(glyphClass=inputFont._glyphClass,
                            glyphContourClass=inputFont._glyphContourClass,
                            glyphPointClass=inputFont._glyphPointClass,
                            glyphComponentClass=inputFont._glyphComponentClass,
                            glyphAnchorClass=inputFont._glyphAnchorClass,
                            kerningClass=inputFont._kerningClass,
                            infoClass=inputFont._infoClass,
                            groupsClass=inputFont._groupsClass,
                            featuresClass=inputFont._featuresClass,
                            libClass=inputFont._libClass,
                        )
    outputFont._path = inputFont.path
    outputFont.lib.deserialize(inputFont.lib.serialize())
    if hasattr(inputFont.kerning, "serialize"):
        outputFont.kerning.deserialize(inputFont.kerning.serialize())
        outputFont.groups.deserialize(inputFont.groups.serialize())
        outputFont.info.deserialize(inputFont.info.serialize())
        outputFont.features.deserialize(inputFont.features.serialize())
    else:
        outputFont._kerning = inputFont.kerning
        outputFont._groups = inputFont.groups
        outputFont._info = inputFont.info
        outputFont._features = inputFont.features
    outputFont._ufoFormatVersion = inputFont._ufoFormatVersion

    # solve an anoying problem
    if outputFont.info.openTypeOS2WinDescent is not None and outputFont.info.openTypeOS2WinDescent < 0:
        outputFont.info.openTypeOS2WinDescent = abs(outputFont.info.openTypeOS2WinDescent)

    outputFont.info.postscriptNominalWidthX = None
    # outputFont.info.postscriptDefaultWidthX = None

    checkComponentMatrix = getDefault("fontGenerateCheckComponentMatrix", True)

    glyphs = [glyph for glyph in inputFont if not glyph.template]

    if progressBar is not None:
        progressBar.update("Compiling %s glyphs..." % len(glyphs))
        # progressBar.setTickCount(len(glyphs)-1)

    for glyph in glyphs:
        if glyph.template:
            continue
        preCompiled = glyph.getRepresentation("doodle.preCompiledGlyph",
                        format=format,
                        decomposeAllComponents=decompose,
                        removeOverlap=checkOutlines,
                        shouldDecomposeWithRemoveOverlap=shouldDecomposeWithCheckOutlines,
                        checkComponentMatrix=checkComponentMatrix)

        outputFont._glyphs[preCompiled.name] = preCompiled
        outputFont._keys.add(preCompiled.name)
        outputFont.unicodeData.addGlyphData(preCompiled.name, preCompiled.unicodes)
        preCompiled.setParent(outputFont)

        # if progressBar is not None:
        #    progressBar.update()

    # compile features with feaPyFoFum
    if outputFont.lib.get("com.typesupply.feaPyFoFum.compileFeatures", False):
        outputFont.features.text = compileFeatures(outputFont.features.text, outputFont, compileReferencedFiles=True)
    return outputFont


def _canFDKAutoHint(font):
    if hasattr(font.info, "canFDKAutoHint"):
        return font.info.canFDKAutoHint()
    else:
        return True  # XXXX


def guessCurveType(font):
    for glyph in font:
        for contour in glyph:
            for point in contour:
                if point.segmentType == "qcurve":
                    return "qcurve"
                elif point.segmentType == "curve":
                    return "curve"
    return None  # can't guess, no curves in the font


if __name__ == "__main__":
    import os
    import tnTestFonts
    # print(dir(tnTestFonts))
    from tnTestFonts import getFontPath
    ufoPath = getFontPath("Condor-Bold.ufo")
    # ufoPath = getFontPath("CusterRE-RegularS2-test.ufo")

    ttfPath = ufoPath + ".test.ttf"
    otfPath = ufoPath + ".test.otf"
    report = generateFontFromUFO(ufoPath, otfPath, format="otf", checkOutlines=True, autohint=True)
    # report = generateFontFromUFO(ufoPath, ttfPath, format="ttf")
    print(report)
