from __future__ import division
import sys
import os
import struct
import yaml
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools import cffLib
from tnbits.compilers.f5 import ttfTools
from tnbits.compilers.f5 import otlTools
from tnbits.compilers.f5.inputFont import InputFontPreprocessor
from tnbits.compilers.f5.fontBuilder import FontBuilder
from tnbits.compilers.f5.otlTools import deleteGlyphs, mergeFeatures
from tnbits.compilers.f5.kernTools import writeKernFeature, writeSinglePosFeature
from tnbits.compilers.f5.ttGlyphBuilder import TTGlyphBuilderPen
from tnbits.compilers.f5.featureBuilder import buildSingleSubstLookup, insertLookup
from tnbits.compilers.f5.codePages import calcCodePages, calcCodePageRangesFromBits, codePagesByID

def parseCharset(path):
    """Parse a unicode character set file and return a set of code points.

        >>> asciiPath = os.path.join(getRepoRoot(), "CharacterSets", "ASCII.txt")
        >>> ascii = parseCharset(asciiPath)
        >>> ascii == set(range(128))
        True
    """
    charset = set()
    data = open(path).read()
    lineCount = 1
    for line in data.splitlines():
        line = line.split("#", 1)[0]
        if not line.strip():
            continue
        for code in line.split(","):
            try:
                code = int(code.strip(), 16)
            except:
                raise ValueError("syntax error in line %s" % lineCount)
            charset.add(code)
        lineCount += 1
    return charset


_charsetCache = {}

def getCharset(name, charsetsFolder):
    """Look for and parse the character set specified by `name`. Results are cached.

        >>> charset = getCharset("Kana", charsetsFolder)
        >>> sorted(charset)[:10]
        [12352, 12353, 12354, 12355, 12356, 12357, 12358, 12359, 12360, 12361]
        >>> charset == getCharset("Kana", charsetsFolder)
        True
        >>> charset is getCharset("Kana", charsetsFolder)
        True
    """
    charset = _charsetCache.get(name)
    if charset is None:
        charsetPath = os.path.join(charsetsFolder, name + ".txt")
        charset = parseCharset(charsetPath)
        _charsetCache[name] = charset
    return charset


def writeStylisticSetsFeatures(stylisticSets, stylisticSetNames):
    from StringIO import StringIO

    featureTags = []
    for i in sorted(stylisticSets):
        featureTag = "ss%02d" % i
        featureTags.append(featureTag)

    ff = StringIO()
    ff.write("feature aalt {\n")
    for featureTag in featureTags:
        ff.write("  feature %s;\n" % featureTag)
    ff.write("} aalt;\n\n")

    for i, mapping in sorted(stylisticSets.items(), reverse=True):
        if not mapping:
            continue
        featureTag = "ss%02d" % i
        ff.write("feature %s {\n" % featureTag)
        ssName = stylisticSetNames.get(i)
        if ssName:
            ff.write("  featureNames {\n")
            # XXX need localized versions of the names
            ff.write("    name \"%s\";\n" % ssName)
            ff.write("  };\n")
        for gn in sorted(mapping):
            sub = mapping[gn]
            ff.write("  sub %s by %s;\n" % (gn, sub))
        ff.write("} %s;\n\n" % featureTag)

    return ff.getvalue()


_os2_usWeightClasses = {
    'thin': 100,
    'extralight': 200,
    'ultralight': 200,
    'light': 300,
    'normal': 400,
    'regular': 400,
    'medium': 500,
    'demibold': 600,
    'semibold': 600,
    'bold': 700,
    'extrabold': 800,
    'ultrabold': 800,
    'black': 900,
    'heavy': 900,
}

def get_usWeightClass(styleName):
    styleName = styleName.replace("-", "").lower()
    styleName = "".join(styleName.split())
    return _os2_usWeightClasses.get(styleName, 400)


class F5FontMerger(object):

    supportedSinglePosFeatures = ["halt", "palt", "vhal", "vpal"]

    @classmethod
    def fromConfigFile(cls, configPath, charsetFolder=None):
        configPath = os.path.abspath(configPath)
        configData = open(configPath).read()
        configFolder = os.path.dirname(configPath)
        return cls.fromConfigData(configData, configFolder, charsetFolder)

    @classmethod
    def fromConfigData(cls, configData, configFolder, charsetFolder=None):
        config = yaml.safe_load(configData)
        return cls(config, configFolder=configFolder, charsetFolder=charsetFolder)

    def __init__(self, inputFonts, configFolder, charsetFolder=None):
        self.inputFonts = inputFonts
        self.configFolder = configFolder
        if charsetFolder is None:
            charsetFolder = self.makePath("../CharacterSets")
        self.charsetFolder = charsetFolder
        self.preprocessors = None
        self.testSubsetCharCount = None
        self.variationAxes = None
        self.variationInstances = None

    def makePath(self, path):
        path = os.path.join(self.configFolder, path)
        path = os.path.normpath(path)
        return path

    def makeInputFont(self, path, index):
        ttf = TTFont(self.makePath(path))
        ttfTools.patchGlyphNames(ttf, makeGlyphRenamer(index))
        return ttf

    def makeCharset(self, inputFontSpec):
        charset = set()
        for name in inputFontSpec["charset"]:
            op = "add"
            if name[0] == "-":
                op = "sub"
                name = name[1:]
            if name[:2] == "U+":
                s = set([int(name[2:], 16)])
            else:
                s = getCharset(name, self.charsetFolder)
            if op == "add":
                charset |= s
            else:
                charset -= s
        return charset

    def buildTTGlyphs(self, outFont, glyphs, boundingBoxes):
        ttGlyphs = {}
        for glyphName in glyphs:
            glyph = glyphs[glyphName]
            bounds = boundingBoxes[glyphName]
            pen = TTGlyphBuilderPen()
            glyph.draw(pen)
            ttGlyph = pen.buildTTGlyph(reverseContours=False)
            if bounds:
                ttGlyph.xMin, ttGlyph.yMin, ttGlyph.xMax, ttGlyph.yMax = bounds
            else:
                ttGlyph.xMin, ttGlyph.yMin, ttGlyph.xMax, ttGlyph.yMax = (0, 0, 0, 0)
            ttGlyphs[glyphName] = ttGlyph
        return ttGlyphs

    def buildT2Glyphs(self, outFont, glyphs, nominalWidthX, defaultWidthX):
        t2Glyphs = {}
        for glyphName in glyphs:
            glyph = glyphs[glyphName]
            if glyph.width == defaultWidthX:
                width = None
            else:
                width = glyph.width - nominalWidthX
            pen = T2CharStringPen(width, None)
            glyph.draw(pen)
            charString = pen.getCharString()
            t2Glyphs[glyphName] = charString
        return t2Glyphs

    def buildFont(self, outputFontSpec):
        print("Configuring preprocessors")
        self.configurePreprocessors(outputFontSpec)

        print("Preparing cmaps and stylistic sets")
        cmapping, stylisticSets, stylisticSetNames = self.buildMappings()
        outputGlyphOrder = self.buildGlyphOrder(cmapping)

        print("Processing glyphs")
        glyphs, variations = self.buildGlyphs(len(outputGlyphOrder))

        print("Assembling output font")

        unitsPerEm = outputFontSpec["unitsPerEm"]

        # XXX typoAscender needs to be specified somewhere, see:
        #    https://github.com/TypeNetwork/F5MultiLanguageFont/issues/14
        typoAscender = int(round(unitsPerEm * 0.850))
        typoDescender = -(unitsPerEm - typoAscender)
        otherAscender = int(round(unitsPerEm * 1.000))
        otherDescender = int(round(unitsPerEm * -0.250))

        format = outputFontSpec["format"].lower()
        outFont = FontBuilder(unitsPerEm, isTTF=(format != "otf"))

        # FontTools will only recalc various bbox-based info for TTF.
        # We also need CFF, so we do it all here, and we'll skip the FontTools recalc.
        # XXX see how much of this can move to FontBuilder
        outFont.font.recalcBBoxes = False

        fontInfo = dict(version=1.004, copyright="Copyright 2017 F5")  # XXX get from info file

        nameStrings = makeNameTableStrings(outputFontSpec["familyName"],
                outputFontSpec.get("styleName"), fontInfo=fontInfo)
        outFont.setupNameTable(nameStrings)

        outFont.setupGlyphOrder(outputGlyphOrder)
        outFont.setupCharacterMap(cmapping)
        outFont.setupPost(keepGlyphNames=outputFontSpec.get("keepGlyphNames", False))

        print("Building metrics")
        fontBBox, boundingBoxes, hMetrics, vMetrics, verticalOrigins, hHeaInfo, vHeaInfo = self.buildMetrics(glyphs)
        xMin, yMin, xMax, yMax = fontBBox

        outFont.updateHead(xMin=xMin, yMin=yMin, xMax=xMax, yMax=yMax, fontRevision=fontInfo.get("version", 1.0))

        print("Building output glyphs")
        if format == "otf":
            nominalWidthX, defaultWidthX = _calcNominalAndDefaultWidth(hMetrics)
            t2Glyphs = self.buildT2Glyphs(outFont, glyphs, nominalWidthX, defaultWidthX)
            psName = nameStrings['psName']
            fontInfoDict = dict(
                FullName=nameStrings['fullName'],
                FamilyName=nameStrings['familyName'],
                Weight=nameStrings['styleName'],
                FontMatrix=[1.0/unitsPerEm, 0, 0, 1.0/unitsPerEm, 0, 0],
                version=nameStrings['version'],
                Notice=nameStrings['copyright'],
                FontBBox=fontBBox,
            )
            privateDict = dict(nominalWidthX=nominalWidthX, defaultWidthX=defaultWidthX)
            outFont.setupCFF(psName, fontInfoDict, t2Glyphs, privateDict)
            outFont.setupVerticalOrigins(verticalOrigins)
        else:
            ttGlyphs = self.buildTTGlyphs(outFont, glyphs, boundingBoxes)
            outFont.setupGlyf(ttGlyphs)

        outFont.setupMetrics("hmtx", hMetrics)
        outFont.setupHorizontalHeader(ascent=otherAscender, descent=otherDescender, **hHeaInfo)
        outFont.setupMetrics("vmtx", vMetrics)
        outFont.setupVerticalHeader(ascent=unitsPerEm//2, descent=-unitsPerEm//2, **vHeaInfo)

        if variations:
            outFont.setupFvar(self.variationAxes, self.variationInstances)
            outFont.setupGvar(variations)

        print("Adding OpenType features")

        featureFile = outputFontSpec.get("featureFile")
        if featureFile:
            featureFile = self.makePath(featureFile)
            customFeatures = "# custom features\n\n" + open(featureFile).read() + "\n# end custom features\n\n"
        else:
            customFeatures = ""

        kerning, groups = self.getKerning(targetUPM=unitsPerEm)
        if kerning:
            kernFeature = writeKernFeature(kerning, groups)
        else:
            kernFeature = ""

        singlePosFeatures = ""
        for featureTag in self.supportedSinglePosFeatures:
            singlePos = self.getSinglePos(targetUPM=unitsPerEm, featureTag=featureTag)
            if singlePos:
                singlePosFeatures += writeSinglePosFeature(singlePos, featureTag)

        stylisticSetsFeature = writeStylisticSetsFeatures(stylisticSets, stylisticSetNames)
        features = customFeatures + stylisticSetsFeature + kernFeature + singlePosFeatures
        outputFolder = outputFontSpec.get("outputFolder")
        if outputFolder is not None:
            outputFolder = self.makePath(outputFolder)
        else:
            outputFolder = "."
        fontFileName = outputFontSpec.get("fileName")
        if fontFileName is None:
            extension = format
            if extension == "ttf-var":
                extension = "ttf"
            fontFileName = "%s.%s" % (nameStrings["psName"], extension)
        outPath = os.path.join(outputFolder, fontFileName)

        if outputFontSpec.get("saveFeatures", False):
            f = open(outPath + ".fea", "w")
            f.write(features)
            f.close()

        outFont.addOpenTypeFeatures(features)
        self.mergeGsubFeatures(outFont)
        merge_vrt2_lookups(outFont)

        if ord("x") in cmapping:
            xHeight = boundingBoxes[cmapping[ord("x")]][3]
        else:
            xHeight = 0
        if ord("H") in cmapping:
            capHeight = boundingBoxes[cmapping[ord("H")]][3]
        else:
            capHeight = 0

        codePageBits = calcCodePages(set(cmapping))
        # XXX the next manual additions should come from fontInfo or better heuristics
        codePageBits.add(codePagesByID["cp932"])  #  JIS/Japan
        codePageBits.add(codePagesByID["cp936"])  #  Chinese: Simplified chars--PRC and Singapore
        codePageBits.add(codePagesByID["cp949"])  #  Korean Wansung
        codePageBits.add(codePagesByID["cp950"])  #  Chinese: Traditional chars--Taiwan and Hong Kong
        codePageBits.add(codePagesByID["cp1361"]) #  Korean Johab
        ulCodePageRange1, ulCodePageRange2 = calcCodePageRangesFromBits(codePageBits)

        outFont.setupOS2(achVendID=fontInfo.get("vendor", "TNWK"),
            sTypoAscender=typoAscender, sTypoDescender=typoDescender,
            usWinAscent=otherAscender, usWinDescent=abs(otherDescender),
            usWeightClass=get_usWeightClass(outputFontSpec.get("styleName", "regular")),
            usMaxContext=otlTools.calcMaxContext(outFont.font),
            sxHeight=xHeight, sCapHeight=capHeight,
            ulCodePageRange1=ulCodePageRange1, ulCodePageRange2=ulCodePageRange2)

        outFont.setupDSIG()

        print("Compiling and saving output font to %r" % outPath)
        if format != "otf":
            outFont.font["maxp"].recalc(outFont.font)
            outFont.save(outPath)
        else:
            # make CFF CID-Keyed
            self.convertCFFToCIDKeyed(outFont.font)
            # We'll temporarily monkeypatch cffLib's getCIDfromName() so we can
            # provide our own glyph name -> CID mapping. (For now: GID == CID.)
            revGlyphOrder = {gn: gid for gid, gn in enumerate(outputGlyphOrder)}
            def getCIDfromName(name, strings):
                return revGlyphOrder[name]
            original_getCIDfromName = cffLib.getCIDfromName
            try:
                cffLib.getCIDfromName = getCIDfromName
                outFont.save(outPath)
            finally:
                cffLib.getCIDfromName = original_getCIDfromName

    def convertCFFToCIDKeyed(self, ttFont):
        glyphOrder = ttFont.glyphOrder
        fontName = ttFont["CFF "].cff.keys()[0]
        topDict = ttFont["CFF "].cff.values()[0]
        assert topDict.Encoding == "StandardEncoding"
        assert topDict.charset == glyphOrder

        topDict.ROS = ("Adobe", "Identity", 0)  # ???
        fontMatrix = topDict.FontMatrix
        fontDict = cffLib.FontDict()
        fontDict.FontName = fontName
        fontDict.FontMatrix = fontMatrix
        fontDict.Private = topDict.Private
        del topDict.Private
        topDict.FDArray = cffLib.FDArrayIndex()
        topDict.FDArray.append(fontDict)

        topDict.FDSelect = cffLib.FDSelect()
        topDict.FDSelect.format = None
        topDict.FDSelect.gidArray = [0] * len(glyphOrder)
        topDict.CIDCount = len(glyphOrder)

    def getKerning(self, targetUPM):
        allKerning = {}
        allGroups = {}
        for ifpp in self.preprocessors:
            kerning, groups = ifpp.getKerning(targetUPM=targetUPM)
            allKerning.update(kerning)
            assert len(groups) + len(allGroups) == len(set(groups) | set(allGroups))
            allGroups.update(groups)
        return allKerning, allGroups

    def getSinglePos(self, targetUPM, featureTag):
        allSinglePos = {}
        for ifpp in self.preprocessors:
            singlePos = ifpp.getSinglePos(targetUPM=targetUPM, featureTag=featureTag)
            allSinglePos.update(singlePos)
        return allSinglePos

    def mergeGsubFeatures(self, outFont):
        outGsub = outFont.font["GSUB"]
        for index, ifpp in enumerate(self.preprocessors):
            gsub = ifpp.inputFont1.get("GSUB")
            if gsub is not None:
                # first we need to subset the GSUB table
                deleteGlyphs(gsub, ifpp.glyphNames - ifpp.subsettedGlyphNames)
                ensure_vert_and_vrt2(gsub)
                mergeFeatures(outGsub, gsub)
                # Merging messed up the input fonts GSUB, so let's flush it,
                # so it will be loaded freshly next time it's needed.
                del ifpp.inputFont1.tables["GSUB"]

    def buildGlyphOrder(self, cmap=None):
        outputGlyphOrder = []
        for ifpp in self.preprocessors:
            outputGlyphOrder.extend(ifpp.subsettedGlyphOrder)
        assert len(outputGlyphOrder) <= 0xffff, "too many glyphs"
        assert outputGlyphOrder[0] == ".notdef"
        if cmap is None:
            return outputGlyphOrder
        # reorder by unicode
        reorderedGlyphOrder = [".notdef"]
        glyphNames = set(reorderedGlyphOrder)
        for code, glyphName in sorted(cmap.items()):
            if glyphName not in glyphNames:
                glyphNames.add(glyphName)
                reorderedGlyphOrder.append(glyphName)
        for glyphName in outputGlyphOrder:
            if glyphName not in glyphNames:
                glyphNames.add(glyphName)
                reorderedGlyphOrder.append(glyphName)
        assert len(reorderedGlyphOrder) == len(outputGlyphOrder)
        return reorderedGlyphOrder

    def buildMappings(self):
        cmapping = {}
        stylisticSets = {}
        stylisticSetNames = {}
        for index, ifpp in enumerate(self.preprocessors):
            stylisticSetMapping = {}

            for char in sorted(ifpp.subsettedCharacters):
                gn = ifpp.cmap[char]
                if char not in cmapping:
                    cmapping[char] = gn
                else:
                    stylisticSetMapping[cmapping[char]] = gn

            if stylisticSetMapping:
                assert ifpp.stylisticSetNumber is not None, "There are overlapping code points but no assigned stylistic set for input font #%s" % index
                stylisticSetNames[ifpp.stylisticSetNumber] = ifpp.stylisticSetName
                if ifpp.stylisticSetNumber not in stylisticSets:
                    stylisticSets[ifpp.stylisticSetNumber] = stylisticSetMapping
                else:
                    stylisticSets[ifpp.stylisticSetNumber].update(stylisticSetMapping)

        return cmapping, stylisticSets, stylisticSetNames

    def buildGlyphs(self, numGlyphs):
        glyphCounter = 0
        glyphs = {}
        variations = {}
        for index, ifpp in enumerate(self.preprocessors):
            for gn in ifpp.subsettedGlyphOrder:
                if not (glyphCounter % 100):
                    print("Building glyph %s of %s" % (glyphCounter, numGlyphs))
                ttGlyph, glyphVariations = ifpp.getGlyph(gn)
                assert gn not in glyphs
                glyphs[gn] = ttGlyph
                if glyphVariations:
                    variations[gn] = glyphVariations
                glyphCounter += 1
        return glyphs, variations

    def buildMetrics(self, glyphs):
        boundingBoxes = {}
        verticalOrigins = {}
        hMetrics = {}
        vMetrics = {}
        fontBBox = None
        advanceWidthMax = 0
        advanceHeightMax = 0
        INFINITY = 100000
        minLeftSideBearing = INFINITY
        minRightSideBearing = INFINITY
        minTopSideBearing = INFINITY
        minBottomSideBearing = INFINITY
        xMaxExtent = 0
        yMaxExtent = 0

        for gn, glyph in glyphs.items():
            glyphBounds = _getGlyphControlBounds(glyph, glyphs)
            boundingBoxes[gn] = glyphBounds
            verticalOrigins[gn] = glyph.verticalOrigin
            fontBBox = _updateBoundingBox(fontBBox, glyphBounds)
            if glyphBounds:
                xMin, yMin, xMax, yMax = glyphBounds
                lsb = xMin
                rsb = glyph.width - lsb - (xMax - xMin)
                tsb = glyph.verticalOrigin - yMax
                bsb = glyph.advanceHeight - tsb - (yMax - yMin)
                xExtent = lsb + (xMax - xMin)
                yExtent = tsb + (yMax - yMin)
                minLeftSideBearing = min(minLeftSideBearing, lsb)
                minRightSideBearing = min(minRightSideBearing, rsb)
                minTopSideBearing = min(minTopSideBearing, tsb)
                minBottomSideBearing = min(minBottomSideBearing, bsb)
                xMaxExtent = max(xMaxExtent, xExtent)
                yMaxExtent = max(yMaxExtent, yExtent)
            else:
                lsb = 0
                tsb = glyph.verticalOrigin
            hMetrics[gn] = (glyph.width, lsb)
            vMetrics[gn] = (glyph.advanceHeight, tsb)
            advanceWidthMax = max(advanceWidthMax, glyph.width)
            advanceHeightMax = max(advanceHeightMax, glyph.advanceHeight)

        hHeaInfo = dict(
            advanceWidthMax=advanceWidthMax,
            minLeftSideBearing=minLeftSideBearing,
            minRightSideBearing=minRightSideBearing,
            xMaxExtent=xMaxExtent
        )
        vHeaInfo = dict(
            advanceHeightMax=advanceHeightMax,
            minTopSideBearing=minTopSideBearing,
            minBottomSideBearing=minBottomSideBearing,
            yMaxExtent=yMaxExtent
        )
        return fontBBox, boundingBoxes, hMetrics, vMetrics, verticalOrigins, hHeaInfo, vHeaInfo

    def reportErrors(self):
        for index, ifpp in enumerate(self.preprocessors):
            inputFontSpec = self.inputFonts[index]
            fp1 = os.path.basename(inputFontSpec["inputFont1"])
            fp2 = os.path.basename(inputFontSpec["inputFont2"])
            if ifpp.missingCharacters:
                sys.stderr.write("%s characters are missing from %s and %s\n" % (len(ifpp.missingCharacters), fp1, fp2))
            if ifpp.interpolationErrors:
                sys.stderr.write("%s glyphs could not be interpolated from %s and %s\n" %
                        (len(ifpp.interpolationErrors), fp1, fp2))

    def setupPreprocessors(self):
        self.preprocessors = []

        if self.testSubsetCharCount:
            sys.stderr.write("Warning: using a subset of the glyphs for faster testing\n")

        for index, inputFontSpec in enumerate(self.inputFonts):
            inputFont1 = self.makeInputFont(inputFontSpec["inputFont1"], index)
            inputFont2 = self.makeInputFont(inputFontSpec["inputFont2"], index)
            charset = self.makeCharset(inputFontSpec)

            ifpp = InputFontPreprocessor(inputFont1, inputFontSpec["weight1"],
                                         inputFont2, inputFontSpec["weight2"],
                                         inputFontSpec)

            if self.testSubsetCharCount:
                charset = set(ifpp.cmap) & charset
                keepSet = charset & set([0x005C, 0x00A5, 0x20A9]) # backslash, yen, won, for custom feature testing
                charset = sorted(charset)
                charset = set(charset[:self.testSubsetCharCount//2] + charset[-self.testSubsetCharCount//2:])
                charset |= keepSet

            ifpp.setupSubsetting(charset, includeNotdef=(index==0))

            self.preprocessors.append(ifpp)

    def setupVariations(self, outputFontSpec):
        from fontTools.varLib import models
        minValue = defaultValue = int(round(1000 * outputFontSpec["weight"]))
        maxValue = int(round(1000 * outputFontSpec["weightBold"]))
        axisList = [
            ("wght", minValue, defaultValue, maxValue, "Weight"),
        ]
        locations = [
            {},
            {"wght": maxValue},
        ]
        axisSupports = {}
        for tag, minValue, defaultValue, maxValue, _ in axisList:
            axisSupports[tag] = (minValue, defaultValue, maxValue)
        locations = [models.normalizeLocation(m, axisSupports) for m in locations]
        variationModel = models.VariationModel(locations)
        familyName = outputFontSpec["familyName"]
        instances = [
            {"stylename": "Regular", "location": {"wght": minValue},
                "postscriptfontname": familyName + "-" + "Regular"},
            {"stylename": "Bold", "location": {"wght": maxValue},
                "postscriptfontname": familyName + "-" + "Bold"},
        ]
        return variationModel, axisList, instances

    def configurePreprocessors(self, outputFontSpec):
        if outputFontSpec["format"].upper() == "TTF-VAR":
            variationModel, self.variationAxes, self.variationInstances = self.setupVariations(outputFontSpec)
        else:
            variationModel = None

        for ifpp in self.preprocessors:
            ifpp.configure(outputFontSpec, variationModel)


def _findMostFrequent(values):
    bag = {}
    for v in values:
        if v not in bag:
            bag[v] = 1
        else:
            bag[v] += 1
    byFreq = sorted(bag, key=lambda v: bag[v], reverse=True)
    return byFreq[0]


def _calcNominalAndDefaultWidth(hMetrics):
    widths = [hMetrics[gn][0] for gn in hMetrics]
    nominalWidth = int(round(sum(widths) / len(widths)))
    defaultWidth = _findMostFrequent(widths)
    return nominalWidth, defaultWidth


def _getGlyphControlBounds(glyph, glyphSet):
    pen = ControlBoundsPen(glyphSet)
    glyph.draw(pen)
    bounds = pen.bounds
    return bounds


def _updateBoundingBox(box1, box2):
    if box1 is None:
        return box2
    if box2 is None:
        return box1
    xMin1, yMin1, xMax1, yMax1 = box1
    xMin2, yMin2, xMax2, yMax2 = box2
    return (min(xMin1, xMin2), min(yMin1, yMin2), max(xMax1, xMax2), max(yMax1, yMax2))


def makeGlyphRenamer(index):
    if not index:
        def renameFunc(gn, gi):
            return gn
    else:
        def renameFunc(gn, gi, fontIndex=index):
            return gn + ".%d" % fontIndex
    return renameFunc


def makeNameTableStrings(familyName, styleName, psName=None, fontInfo=None):
    from tnbits.compilers.f5 import __version__ as engineVersion
    if not psName:
        psName = familyName
        if styleName:
            psName = psName + "-" + styleName
        psName = "".join(psName.split())
    if styleName:
        fullName = familyName + " " + styleName
    else:
        fullName = familyName
        styleName = "Regular"
    if fontInfo is None:
        fontInfo = {}
    version = str(fontInfo.get("version", 1.0))
    copyright = fontInfo.get("copyright", "Copyright F5")
    vendor = fontInfo.get("vendor", "TNWK")
    nameStrings = dict(
                 copyright = copyright,
                familyName = familyName,
                 styleName = styleName,
                  fullName = fullName,
                    psName = psName,
                identifier = "%s;%s;%s;F5FontMerger;engine v. %s" % (version, vendor, fullName, engineVersion),
                   version = "Version %s" % version,
         typographicFamily = familyName,
      typographicSubfamily = styleName,
    )
    return nameStrings


def _updateLangSys(langSys, indexMapping):
    """If the langSys refers to a 'vert' feature index, append the corresponding
    'vrt2' feature index.
    """
    if langSys is None:
        return
    vrt2Indices = []
    for vertIndex, vrt2Index in indexMapping:
        if vertIndex in langSys.FeatureIndex:
            assert vrt2Index not in langSys.FeatureIndex
            vrt2Indices.append(vrt2Index)
    langSys.FeatureIndex = langSys.FeatureIndex + vrt2Indices


def ensure_vert_and_vrt2(gsub):
    """If the GSUB table contains a 'vert' feature but not a 'vrt2' feature, create
    the 'vrt2' feature by duplicating 'vert'.
    """
    from fontTools.ttLib.tables.otTables import FeatureRecord, Feature
    gsub = gsub.table
    featureIndices = {}
    for index, fr in enumerate(gsub.FeatureList.FeatureRecord):
        if fr.FeatureTag not in featureIndices:
            featureIndices[fr.FeatureTag] = set([index])
        else:
            featureIndices[fr.FeatureTag].add(index)

    if "vert" in featureIndices and not "vrt2" in featureIndices:
        indexMapping = []
        for index in featureIndices["vert"]:
            featureRecord = gsub.FeatureList.FeatureRecord[index]
            newFeatureRecord = FeatureRecord()
            newFeatureRecord.FeatureTag = "vrt2"
            newFeatureRecord.Feature = Feature()
            newFeatureRecord.Feature.FeatureParams = featureRecord.Feature.FeatureParams
            newFeatureRecord.Feature.LookupListIndex = list(featureRecord.Feature.LookupListIndex)
            newFeatureIndex = len(gsub.FeatureList.FeatureRecord)
            gsub.FeatureList.FeatureRecord.append(newFeatureRecord)
            indexMapping.append((index, newFeatureIndex))
        for scriptRecord in gsub.ScriptList.ScriptRecord:
            _updateLangSys(scriptRecord.Script.DefaultLangSys, indexMapping)
            for langSys in [lsr.LangSys for lsr in scriptRecord.Script.LangSysRecord]:
                _updateLangSys(langSys, indexMapping)
        # Make sure the feature list is sorted
        otlTools.sortFeatureList(gsub)


def merge_vrt2_lookups(outFont):
    #
    # We will fold all vrt2 lookups into a single Lookup with one SingleSubst
    # subtable so we adhere to some old requirements that, if not met, will
    # make Windows reject a font. See:
    #   https://www.microsoft.com/typography/otspec/features_uz.htm#vrt2
    #
    # In doing so we will assume there are no differences in vrt2 behavior
    # between scripts and languages.
    #
    gsub = outFont.font["GSUB"].table

    # Collect the lookup indices referenced by vrt2 features
    vrt2Lookups = set()
    for featureRecord in gsub.FeatureList.FeatureRecord:
        if featureRecord.FeatureTag == "vrt2":
            vrt2Lookups.update(featureRecord.Feature.LookupListIndex)

    if not vrt2Lookups:
        # nothing to do!
        return

    # Make one big substitution mapping
    vrt2Mapping = {}
    for lookupIndex in sorted(vrt2Lookups):
        lookup = gsub.LookupList.Lookup[lookupIndex]
        for subTable in lookup.SubTable:
            if subTable.LookupType == 7:
                subTable = subTable.ExtSubTable
            assert subTable.LookupType == 1
            assert not (set(vrt2Mapping) & set(subTable.mapping))
            vrt2Mapping.update(subTable.mapping)

    # Find the lookups that are _only_ used by vrt2
    # These ones we can mess with. We assume we find at least one,
    # we will replace it with a newly built lookup, and we'll delete
    # the others
    uniqueVrt2Lookups = set(vrt2Lookups)
    for featureRecord in gsub.FeatureList.FeatureRecord:
        if featureRecord.FeatureTag != "vrt2":
            indices = set(featureRecord.Feature.LookupListIndex)
            uniqueVrt2Lookups -= indices

    if not uniqueVrt2Lookups:
        # if not, we need to insertLookup() the lookup in the right place
        raise NotImplementedError()

    vrt2LookupIndex = min(uniqueVrt2Lookups)
    lookupsToDelete = uniqueVrt2Lookups - set([vrt2LookupIndex])

    newVrt2Lookup = buildSingleSubstLookup(vrt2Mapping)
    gsub.LookupList.Lookup[vrt2LookupIndex] = newVrt2Lookup

    for featureRecord in gsub.FeatureList.FeatureRecord:
        if featureRecord.FeatureTag == "vrt2":
            featureRecord.Feature.LookupListIndex = [vrt2LookupIndex]

    assert vrt2LookupIndex not in lookupsToDelete

    indicesBefore = range(len(gsub.LookupList.Lookup))
    for i in sorted(lookupsToDelete, reverse=True):
        del indicesBefore[i]
        del gsub.LookupList.Lookup[i]
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)  # this should be redundant
    indicesAfter = range(len(indicesBefore))
    lookupRemap = dict(zip(indicesBefore, indicesAfter))
    otlTools.remapLookups(gsub, lookupRemap)


def myBool(value):
    if value is None:
        return None
    value = value.lower().strip()
    _values = dict(no=False, yes=True, false=False, true=True, n=False, y=True, f=False, t=True)
    return _values[value]


outputParameters = [
    # parm name, default, type, help
    ("familyName",     None, str,    "The family name."),
    ("styleName",      None, str,    "The style name."),
    ("format",         None, str,    "The desired output format: ttf, otf or ttf-var."),
    ("weight",         None, float,  "The desired 'equivalent latin stem weight', as a fraction of the UPM."),
    ("weightBold",     None, float,  "For a Variable Font, this specifies the weight for the Bold master, "
                                     "as a fraction of the UPM."),
    ("unitsPerEm",     None, int,    "The Units Per Em value."),
    ("keepGlyphNames", None, myBool, "Keep the glyph names in the output font."),
    ("removeOverlap",  None, myBool, "Perform remove overlap."),
    ("outputFolder",   None, str,    "Folder to save the output font into."),
    ("fileName",       None, str,    "File name for the output font. If omitted, it will be constructed from "
                                     "the font name and format."),
    #
    ("saveFeatures",   None, myBool, "Save the generated features next to the output font as a .fea file."),
    ("subset",         None, int,    "Use an arbitrary subset for faster testing."),
]

def main(args):
    import argparse
    parser = argparse.ArgumentParser(description=
        "Merge and interpolate a set of fonts as specified by a set of config files. "
        "An output font is either specified by an output configuration file, or "
        "a set of command line arguments, or a combination. Command line options "
        "will override the values in the config file.")
    parser.add_argument(dest='inputSpec', metavar="INPUTSPEC", help="The input configuration file to use.")
    parser.add_argument('--outputSpec', '-o', metavar="OUTPUTSPEC", help="The output specification file to use.", nargs="+")

    for parm, default, tp, help in outputParameters:
        parser.add_argument('--' + parm, default=default, type=tp, help=help)

    args = parser.parse_args(args)

    overrideParameters = {}
    for parm, default, tp, help in outputParameters:
        value = getattr(args, parm)
        if value is not None:
            overrideParameters[parm] = value

    if "outputFolder" in overrideParameters:
        overrideParameters["outputFolder"] = os.path.abspath(overrideParameters["outputFolder"])

    fm = F5FontMerger.fromConfigFile(args.inputSpec)
    if args.subset is not None:
        fm.testSubsetCharCount = args.subset

    print("Setting up preprocessors")
    fm.setupPreprocessors()

    if args.outputSpec:
        outputFontSpecs = []
        for outputSpecPath in args.outputSpec:
            outputFontSpec = yaml.safe_load(open(outputSpecPath))
            outputFontSpec.update(overrideParameters)
            outputFontSpecs.append(outputFontSpec)
    else:
        outputFontSpec = dict(unitsPerEm=1000, keepGlyphNames=True, format="ttf")
        outputFontSpec.update(overrideParameters)
        outputFontSpecs = [outputFontSpec]

    for outputFontSpec in outputFontSpecs:
        fm.buildFont(outputFontSpec)

    fm.reportErrors()


if __name__ == "__main__":
    main(sys.argv[1:])
