from __future__ import division

import sys
import warnings
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import ControlBoundsPen, BoundsPen
from booleanOperations import BooleanOperationManager
from defcon import Glyph
from tnbits.compilers.f5.otlTools import deleteGlyphs
from tnbits.compilers.f5.ttfTools import getBestCmap, findGlyphsByUnicode
from tnbits.compilers.f5.ttGlyphBuilder import TTGlyphBuilderPen, CubicToQuadFilterPen, glyphsToQuadratic
from tnbits.compilers.f5.kernTools import (getKerningFromGPOS, interpolateKerning,
        filterZeroKerning, scaleKerning, roundKerning, regroupKerning, subsetKerning,
        getSinglePosFromGPOS, interpolateSinglePos, filterZeroSinglePos, scaleSinglePos,
        roundSinglePos, subsetSinglePos)


QUAD_MAX_ERR = 0.5


class InterpolationError(Exception):
    """Exception to be raised whenever an interpolation incompatibility is encountered."""

class InterpolationWarning(Warning):
    """Warning to be used whenever a non-fatal interpolation incompatibility is encountered."""


class InputFontPreprocessor(object):

    def __init__(self, inputFont1, weight1, inputFont2, weight2, inputFontSpec):
        self.inputFont1 = inputFont1
        self.glyphSet1 = inputFont1.getGlyphSet()
        self.weight1 = weight1
        self.inputFont2 = inputFont2
        self.glyphSet2 = inputFont2.getGlyphSet()
        self.weight2 = weight2
        self.inputFontSpec = inputFontSpec
        self.interpolationFactor = None  # will be calculated in setupInterpolation()
        self.interpolationFactorBold = None  # for Var font; may be calculated in setupInterpolation()
        self.variationModel = None  # font Var font
        self.glyphOperations = []
        self.glyphNames = None
        self.subsettedCharacters = None
        self.subsettedGlyphNames = None
        self.missingCharacters = None
        self.interpolationErrors = {}
        self.setupAndCheck()

    @property
    def stylisticSetNumber(self):
        return self.inputFontSpec.get("stylisticSetNumber")

    @property
    def stylisticSetName(self):
        return self.inputFontSpec.get("stylisticSetName")

    @property
    def verticalShift(self):
        return self.inputFontSpec.get("verticalShift", 0)

    @property
    def verticalOriginShift(self):
        return self.inputFontSpec.get("verticalOriginShift", None)

    @property
    def defaultVerticalOrigin(self):
        return self.inputFontSpec.get("defaultVerticalOrigin", None)

    @property
    def scaleFactor(self):
        return self.inputFontSpec.get("scaleFactor", 1.0)

    @property
    def scaleMetrics(self):
        return self.inputFontSpec.get("scaleMetrics", True)

    def setupAndCheck(self):
        upm1 = self.inputFont1["head"].unitsPerEm
        upm2 = self.inputFont2["head"].unitsPerEm
        if upm1 != upm2:
            warnings.warn(InterpolationWarning("fonts have different unitsPerEm: %s %s" % (upm1, upm2)))
        self.unitsPerEm = upm1

        cmap1 = getBestCmap(self.inputFont1)
        cmap2 = getBestCmap(self.inputFont2)
        if cmap1 != cmap2:
            warnings.warn(InterpolationWarning("fonts have different cmaps"))

        go1 = self.inputFont1.getGlyphOrder()
        gs1 = set(go1)
        go2 = self.inputFont2.getGlyphOrder()
        gs2 = set(go2)
        if gs1 != gs2:
            warnings.warn(InterpolationWarning("fonts have different glyph sets"))
            # fall back to the union of both glyph sets
            gs1 = gs1 & gs2
            go1 = [gn for gn in go1 if gn in gs1]
            cmap1 = {code:gn for code, gn in cmap1.items() if gn in gs1}
        elif go1 != go2:
            warnings.warn(InterpolationWarning("fonts have different glyph orders"))

        self.glyphNames = gs1
        self.glyphOrder = go1
        self.cmap = cmap1

        self.isCFF = "CFF " in self.inputFont1
        if ("CFF " in self.inputFont2) != self.isCFF:
            raise InterpolationError("fonts have different curve types")

    def setupSubsetting(self, charset, includeNotdef=False):
        """Discover the glyph names that are needed to render the requested characters."""
        charset = set(charset)
        self.subsettedCharacters = set(self.cmap) & charset
        self.missingCharacters = charset - self.subsettedCharacters
        self.subsettedGlyphNames = findGlyphsByUnicode(self.inputFont1, self.subsettedCharacters)

        revCmap = {}
        for char, glyphName in self.cmap.items():
            if glyphName not in revCmap:
                revCmap[glyphName] = [char]
            else:
                revCmap[glyphName].append(char)

        # Some encoded characters that are not in the specified charset may still end up
        # in the subsettedGlyphNames via GSUB. Let's remove them to avoid conflicts with
        # character sets that do define them.
        glyphsToDrop = set()
        for glyphName in list(self.subsettedGlyphNames):
            if glyphName in revCmap:
                # the glyph is encoded
                for char in revCmap[glyphName]:
                    if char in self.subsettedCharacters:
                        # the glyph's code point belongs to our character set, we'll keep it
                        break
                else:
                    # the glyph's code point does not belong to our character set, we'll drop it
                    glyphsToDrop.add(glyphName)

        if glyphsToDrop:
            # We need to do a full subset of the GSUB table to get an accurate new list of glyphnames to include
            deleteGlyphs(self.inputFont1["GSUB"], (self.glyphNames - self.subsettedGlyphNames) | glyphsToDrop)
            self.subsettedGlyphNames = findGlyphsByUnicode(self.inputFont1, self.subsettedCharacters)
            # Subsetting modified up the GSUB, so let's flush it, so it will be loaded freshly next
            # time it's needed.
            del self.inputFont1.tables["GSUB"]

        self.subsettedGlyphOrder = [gn for gn in self.glyphOrder if gn in self.subsettedGlyphNames]

        if includeNotdef and ".notdef" not in self.subsettedGlyphNames:
            self.subsettedGlyphNames.add(".notdef")
            self.subsettedGlyphOrder.insert(0, ".notdef")

    def setupGlyphPipeline(self, glyphOperations):
        self.glyphOperations = glyphOperations

    def calcInterpolationFactor(self, outputWeight):
        if not (self.weight1 <= outputWeight <= self.weight2):
            # XXX Perhaps this should be a warning?
            raise InterpolationError("requested output weight causes extrapolation: %s %s %s" %
                    (self.weight1, outputWeight, self.weight2))
        interpolationFactor = (outputWeight - self.weight1) / (self.weight2 - self.weight1)
        assert abs(self.weight1 + interpolationFactor * (self.weight2 - self.weight1) - outputWeight) < 0.00001
        return interpolationFactor

    def setupInterpolation(self, outputWeight, outputWeightBold=None):
        self.interpolationFactor = self.calcInterpolationFactor(outputWeight)
        if outputWeightBold is not None:
            self.interpolationFactorBold = self.calcInterpolationFactor(outputWeightBold)

    def getInterpolatedGlyphs(self, glyphName, factors):
        g1 = makeDefconGlyph(glyphName, self.glyphSet1, self.inputFont1, self.defaultVerticalOrigin)
        g2 = makeDefconGlyph(glyphName, self.glyphSet2, self.inputFont2, self.defaultVerticalOrigin)
        glyphs = []
        for factor in factors:
            try:
                g = interpolateGlyphs(g1, g2, factor, glyphName)
            except InterpolationError as error:
                self.interpolationErrors[glyphName] = error
                g = g1  # fallback to the light master
            for glyphOperation, kwargs in self.glyphOperations:
                g = glyphOperation(g, **kwargs)
            glyphs.append(g)
        return glyphs

    def getGlyph(self, glyphName):
        interpolationFactors = [self.interpolationFactor]
        if self.interpolationFactorBold is not None:
            interpolationFactors.append(self.interpolationFactorBold)
        glyphs = self.getInterpolatedGlyphs(glyphName, interpolationFactors)
        if self.interpolationFactorBold is None:
            assert len(glyphs) == 1
            variations = None
            glyph = roundCoordinates(glyphs[0])
        else:
            if self.isCFF:
                glyphsToQuadratic(glyphs, errorMargin=QUAD_MAX_ERR, reverseDirection=True)
            glyphs = [roundCoordinates(g) for g in glyphs]
            variations = getVariationDeltas(glyphs, self.variationModel)
            glyph = glyphs[0]
        return glyph, variations

    def getKerning(self, targetUPM):
        scaleFactor = targetUPM / self.unitsPerEm
        if self.scaleMetrics:
            scaleFactor *= self.scaleFactor
        kerning1 = kerning2 = {}
        if 'GPOS' in self.inputFont1:
            kerning1 = getKerningFromGPOS(self.inputFont1['GPOS'].table)
            kerning1 = subsetKerning(kerning1, self.subsettedGlyphNames)
        if 'GPOS' in self.inputFont2:
            kerning2 = getKerningFromGPOS(self.inputFont2['GPOS'].table)
            kerning2 = subsetKerning(kerning2, self.subsettedGlyphNames)
        kerning = interpolateKerning(kerning1, kerning2, self.interpolationFactor)
        kerning = scaleKerning(kerning, scaleFactor)
        kerning = filterZeroKerning(roundKerning(kerning))
        kerning, groups = regroupKerning(kerning)
        return kerning, groups

    def getSinglePos(self, targetUPM, featureTag):
        scaleFactor = targetUPM / self.unitsPerEm
        if self.scaleMetrics:
            scaleFactor *= self.scaleFactor
        singlePos1 = singlePos2 = {}
        if 'GPOS' in self.inputFont1:
            singlePos1 = getSinglePosFromGPOS(self.inputFont1['GPOS'].table, featureTag)
            singlePos1 = subsetSinglePos(singlePos1, self.subsettedGlyphNames)
        if 'GPOS' in self.inputFont2:
            singlePos2 = getSinglePosFromGPOS(self.inputFont2['GPOS'].table, featureTag)
            singlePos2 = subsetSinglePos(singlePos2, self.subsettedGlyphNames)
        singlePos = interpolateSinglePos(singlePos1, singlePos2, self.interpolationFactor)
        singlePos = scaleSinglePos(singlePos, scaleFactor)
        singlePos = filterZeroSinglePos(roundSinglePos(singlePos))
        return singlePos

    def getTable(self, tableTag):
        return self.inputFont1[tableTag]

    def configure(self, outputFontSpec, variationModel):
        if outputFontSpec["format"].upper() == "TTF-VAR":
            assert variationModel is not None
            self.variationModel = variationModel
            self.setupInterpolation(outputFontSpec["weight"], outputFontSpec["weightBold"])
        else:
            assert variationModel is None
            self.setupInterpolation(outputFontSpec["weight"])

        glyphOperations = []

        if self.scaleFactor != 1.0:
            if self.scaleMetrics:
                glyphOperations.append((scaleGlyph, dict(scaleFactor=self.scaleFactor)))
            else:
                glyphOperations.append((scaleGlyphNoMetrics, dict(scaleFactor=self.scaleFactor)))

        verticalShift = self.verticalShift
        verticalOriginShift = self.verticalOriginShift
        if verticalShift or verticalOriginShift:
            verticalShift = int(round(self.unitsPerEm * verticalShift))
            if verticalOriginShift is not None:
                verticalOriginShift = int(round(self.unitsPerEm * verticalOriginShift))
            glyphOperations.append((verticalShiftGlyph,
                    dict(verticalShift=verticalShift,verticalOriginShift=verticalOriginShift)))

        scaleFactor = outputFontSpec["unitsPerEm"] / self.unitsPerEm
        if scaleFactor != 1.0:
            glyphOperations.append((scaleGlyph, dict(scaleFactor=scaleFactor)))
            # XXX the ifpp should probably know the scaleFactor for other purposes

        if outputFontSpec["removeOverlap"]:
            if self.isCFF:
                glyphOperations.append((removeOverlap, dict()))
            else:
                sys.stderr.write("Warning: remove overlap is not yet supported for TTF sources\n")

        if outputFontSpec["format"].upper() == "TTF":
            if self.isCFF:
                glyphOperations.append((convertToQuadraticCurves, dict()))
        elif outputFontSpec["format"].upper() == "TTF-VAR":
            pass
        elif outputFontSpec["format"].upper() == "OTF":
            if not self.isCFF:
                raise NotImplementedError("conversion fron TTF to CFF is not yet implemented")
        else:
            assert 0, "unknown output format: %r" % outputFontSpec["format"]

        self.setupGlyphPipeline(glyphOperations)


def makeDefconGlyph(glyphName, glyphSet, ttFont, defaultVerticalOrigin=None):
    """Take a glyph object from a TTFont glyph set, and build a defcon Glyph from it."""
    ttg = glyphSet[glyphName]
    dg = Glyph()
    ttg.draw(dg.getPen())
    dg.width = ttg.width

    if "vmtx" in ttFont:
        height, tsb = ttFont["vmtx"].metrics[glyphName]
        dg.advanceHeight = height
        if "VORG" in ttFont:
            dg.verticalOrigin = ttFont["VORG"][glyphName]
        else:
            if "CFF " in ttFont:
                # It seems AFDKO uses the "inkbox" for tsb calculation
                pen = BoundsPen(glyphSet)
            else:
                pen = ControlBoundsPen(glyphSet)
            dg.draw(pen)
            if pen.bounds:
                yMax = pen.bounds[3]
            else:
                yMax = 0
            dg.verticalOrigin = int(round(yMax + tsb))
    else:
        # fallbacks
        dg.advanceHeight = ttFont["head"].unitsPerEm
        if defaultVerticalOrigin is not None:
            dg.verticalOrigin = defaultVerticalOrigin * ttFont["head"].unitsPerEm
        else:
            dg.verticalOrigin = ttFont["OS/2"].sTypoAscender  # "it's something"
    return dg


def interpolateGlyphs(g1, g2, interpolationFactor, glyphName):
    """Take two defcon glyph objects and return an interpolated glyph."""
    newGlyph = Glyph()
    if len(g1.components) != len(g2.components):
        raise InterpolationError("%s: number of components does not match" % glyphName)
    else:
        for componentIndex, (compo1, compo2) in enumerate(zip(g1.components, g2.components)):
            if compo1.baseGlyph != compo2.baseGlyph:
                raise InterpolationError("%s: baseGlyph doesn't match in component #%s" % (glyphName, componentIndex))
            raise NotImplementedError()  # if all input fonts are CFF, support for components will not be needed

    if len(g1) != len(g2):
        raise InterpolationError("%s: number of contours doesn't match" % glyphName)

    pen = newGlyph.getPointPen()
    for contourIndex, (c1, c2) in enumerate(zip(g1, g2)):
        pen.beginPath()
        if len(c1) != len(c2):
            raise InterpolationError("%s: number of points doesn't match in contour #%s" % (glyphName, contourIndex))
        else:
            for p1, p2 in zip(c1, c2):
                if p1.segmentType != p2.segmentType:
                    raise InterpolationError("%s: segmentType mismatch in contour #%s" % (glyphName, contourIndex))
                x = p1.x + interpolationFactor * (p2.x - p1.x)
                y = p1.y + interpolationFactor * (p2.y - p1.y)
                pen.addPoint((x, y), p1.segmentType)
        pen.endPath()

    newGlyph.width = g1.width + interpolationFactor * (g2.width - g1.width)
    newGlyph.advanceHeight = g1.advanceHeight + interpolationFactor * (g2.advanceHeight - g1.advanceHeight)
    newGlyph.verticalOrigin = g1.verticalOrigin + interpolationFactor * (g2.verticalOrigin - g1.verticalOrigin)
    return newGlyph


def scaleGlyph(inGlyph, scaleFactor):
    outGlyph = Glyph()
    pen = TransformPen(outGlyph.getPen(), [scaleFactor, 0, 0, scaleFactor, 0, 0])
    inGlyph.draw(pen)
    outGlyph.width = inGlyph.width * scaleFactor
    outGlyph.advanceHeight = inGlyph.advanceHeight * scaleFactor
    outGlyph.verticalOrigin = inGlyph.verticalOrigin * scaleFactor
    return outGlyph

def scaleGlyphNoMetrics(inGlyph, scaleFactor):
    cx = inGlyph.width / 2
    cy = 0  # or: inGlyph.verticalOrigin - inGlyph.advanceHeight / 2
    dx = cx - cx * scaleFactor
    dy = cy - cy * scaleFactor
    outGlyph = Glyph()
    pen = TransformPen(outGlyph.getPen(), [scaleFactor, 0, 0, scaleFactor, dx, dy])
    inGlyph.draw(pen)
    outGlyph.width = inGlyph.width
    outGlyph.advanceHeight = inGlyph.advanceHeight
    outGlyph.verticalOrigin = inGlyph.verticalOrigin
    return outGlyph

def verticalShiftGlyph(inGlyph, verticalShift, verticalOriginShift=None):
    if verticalOriginShift is None:
        verticalOriginShift = verticalShift
    outGlyph = Glyph()
    pen = outGlyph.getPen()
    if verticalShift:
        pen = TransformPen(pen, [1, 0, 0, 1, 0, verticalShift])
    inGlyph.draw(pen)
    outGlyph.width = inGlyph.width
    outGlyph.advanceHeight = inGlyph.advanceHeight
    outGlyph.verticalOrigin = inGlyph.verticalOrigin + verticalOriginShift
    return outGlyph

def removeOverlap(inGlyph):
    outGlyph = Glyph()
    bm = BooleanOperationManager()
    bm.union(list(inGlyph), outGlyph.getPointPen())
    outGlyph.width = inGlyph.width
    outGlyph.advanceHeight = inGlyph.advanceHeight
    outGlyph.verticalOrigin = inGlyph.verticalOrigin
    return outGlyph

def convertToQuadraticCurves(inGlyph, errorMargin=QUAD_MAX_ERR):
    glyphsToQuadratic([inGlyph], errorMargin=errorMargin, reverseDirection=True)
    return inGlyph

def roundCoordinates(inGlyph):
    for contour in inGlyph:
        for pt in contour:
            pt.x = int(round(pt.x))
            pt.y = int(round(pt.y))
    # XXX skipping components, we currently don't have them
    assert len(inGlyph.components) == 0, "components not yet supported for rounding"
    inGlyph.width = int(round(inGlyph.width))
    inGlyph.advanceHeight = int(round(inGlyph.advanceHeight))
    inGlyph.verticalOrigin = int(round(inGlyph.verticalOrigin))
    return inGlyph

def buildTTGlyphFromCubics(inGlyph, reverseContours=True, quadErrorMargin=0.5, cubicToQuadConverter=None):
    glyphBuilderPen = TTGlyphBuilderPen()
    pen = CubicToQuadFilterPen(glyphBuilderPen, errorMargin=quadErrorMargin,
            cubicToQuadConverter=cubicToQuadConverter)
    inGlyph.draw(pen)
    ttg = glyphBuilderPen.buildTTGlyph(reverseContours)
    # Adding unofficial metrics attributes, so we can that information together with the glyph
    ttg.advanceWidth = inGlyph.width
    ttg.advanceHeight = inGlyph.advanceHeight
    ttg.verticalOrigin = inGlyph.verticalOrigin
    return ttg

def buildTTGlyphFromQuadradics(inGlyph, reverseContours=False):
    glyphBuilderPen = TTGlyphBuilderPen()
    inGlyph.draw(glyphBuilderPen)
    ttg = glyphBuilderPen.buildTTGlyph(reverseContours)
    # Adding unofficial metrics attributes, so we can that information together with the glyph
    ttg.advanceWidth = inGlyph.width
    ttg.advanceHeight = inGlyph.advanceHeight
    ttg.verticalOrigin = inGlyph.verticalOrigin
    return ttg


#
# Variable Font support
#

def getVariationDeltas(glyphs, model):
    from fontTools.ttLib.tables.TupleVariation import TupleVariation

    allCoords = [getVarCoordinates(g) for g in glyphs]

    variations = []
    deltas = model.getDeltas(allCoords)
    supports = model.supports
    assert len(deltas) == len(supports)
    for i, (delta, support) in enumerate(zip(deltas[1:], supports[1:])):
        var = TupleVariation(support, delta)
        variations.append(var)
    return variations

def getVarCoordinates(glyph):
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

    coordinates = []
    for contour in glyph:
        for pt in contour:
            coordinates.append((pt.x, pt.y))
    leftSideX = 0
    rightSideX = glyph.width

    coordinates.extend([(leftSideX, 0),
                  (rightSideX, 0),
                  (0, glyph.verticalOrigin),
                  (0, glyph.verticalOrigin - glyph.advanceHeight)])

    return GlyphCoordinates(coordinates)


if __name__ == "__main__":
    import os, yaml
    from fontTools.ttLib import TTFont
    d = os.path.dirname
    gitFolder = d(d(d(d(d(d(__file__))))))
    f5Folder = os.path.join(gitFolder, "F5MultiLanguageFont")
    configFolder = os.path.join(f5Folder, "Configuration")
    configPath = os.path.join(configFolder, "input-config.yaml")
    config = yaml.safe_load(open(configPath).read())
    outputConfigPath = os.path.join(configFolder, "output-regular.yaml")
    #outputConfigPath = os.path.join(configFolder, "output-var.yaml")
    outputSpec = yaml.safe_load(open(outputConfigPath).read())
    inputFontSpec = config[0]
    p1 = os.path.normpath(os.path.join(configFolder, inputFontSpec["inputFont1"]))
    p2 = os.path.normpath(os.path.join(configFolder, inputFontSpec["inputFont2"]))
    f1 = TTFont(p1, lazy=True)
    f2 = TTFont(p2, lazy=True)
    processor = InputFontPreprocessor(f1, inputFontSpec["weight1"], f2, inputFontSpec["weight2"], inputFontSpec)
    processor.setupInterpolation(outputSpec["weight"], outputSpec.get("weightBold"))
    g, variations = processor.getGlyph("a")
    print("variations:", variations)
    print(g.width, g.advanceHeight, g.verticalOrigin, "========")
    assert "a" in processor.glyphNames
    assert "aaaa" not in processor.glyphNames
    print(g.bounds, g.width)
    g2 = scaleGlyph(g, 2)
    print(g2.bounds, g2.width, g2.verticalOrigin)
    g2 = verticalShiftGlyph(g2, 100, -100)
    g2 = verticalShiftGlyph(g2, 0, -100)
    print(g2.bounds, g2.width, g2.verticalOrigin)
    processor.glyphOperations.append((scaleGlyph, dict(scaleFactor=3.0)))
    processor.glyphOperations.append((removeOverlap, dict()))
    g, variations = processor.getGlyph("a")
    print(g.bounds, g.width)
    g3 = removeOverlap(g)
    print(buildTTGlyphFromCubics(g))
    processor.setupSubsetting([ord("a"), 2000])
    print(processor.missingCharacters)
    print(processor.subsettedGlyphNames)
    print(processor.subsettedCharacters)
