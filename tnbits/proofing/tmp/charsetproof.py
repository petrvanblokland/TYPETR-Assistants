
import sys
import os
import time
from fontTools.ttLib import TTFont
from fontTools.misc.py23 import chr  # capable of "wide" unicode chars
from tnbits.compilers.f5.ttfTools import getBestCmap
from tnbits.compilers.f5.otlTools import findSingleSubstAlts
from tnbits.proofing import installfont
from tnbits.base.future import chr

# NOTE: not used, could be a template?

class ProofFont(object):

    def __init__(self, fontPath):
        self.fontPath = fontPath
        ttFont = TTFont(fontPath)
        self.ttFont = ttFont
        nameRecord = ttFont["name"].getName(6, 3, 1)
        if nameRecord is None:
            nameRecord = ttFont["name"].getName(6, 1, 0)
            assert nameRecord is not None, "can't find PostScript font name"
        self.fontName = nameRecord.toUnicode()
        self.cmap = getBestCmap(ttFont)
        self.glyphNames = ttFont.getGlyphOrder()
        if "GSUB" in self.ttFont:
            self.altMapping = findSingleSubstAlts(self.ttFont["GSUB"])
        else:
            self.altMapping = {}

    def install(self):
        installfont.installFontFile(self.fontPath)

    def uninstall(self):
        installfont.uninstallFontFile(self.fontPath)


class GlyphCell(object):

    def __init__(self, font, uni=None, glyphName=None, featureTags=None):
        self.font = font  # ProofFont
        if glyphName is None:
            assert uni is not None
            glyphName = font.cmap[uni]
        else:
            assert uni is None  # unencoded glyph
        self.uni = uni
        self.glyphName = glyphName
        self.featureTags = featureTags

    def draw(self, pt, formatting):
        from drawBot import FormattedString, save, restore, translate, text, font, fontSize
        # Build the text for the sample glyph.
        txt = FormattedString()
        txt.font(self.font.fontName)
        txt.fontSize(formatting.sampleSize)
        if self.uni is not None:
            txt.append(chr(self.uni))
        elif self.glyphName == ".notdef":
            # Somehow .notdef is not seen as a valid glyph by Cocoa/DrawBot, ignore.
            pass
        else:
            txt.appendGlyph(self.glyphName)

        save()
        x, y = pt
        translate(x, y)
        # Draw the character.
        text(txt, (0, 0))
        # Draw the glyph name and unicode/feature tag labels.
        fontSize(formatting.labelSize)
        text(self.glyphName, (0, -formatting.labelOffset))
        labelText = ""
        if self.uni is not None:
            font("LucidaFax-Demi")
            labelText = "U+%04X" % self.uni
        elif self.featureTags:
            font("LucidaFax-Italic")
            labelText = "|".join(self.featureTags)
        if labelText:
            text(labelText, (0, -formatting.labelOffset - formatting.labelLineDistance))
        restore()


def buildGlyphCellList(prfFont, onlyEncodedGlyphs=False):
    cellsToDraw = []
    doneGlyphs = set()

    encodedGlyphs = {}
    for k, v in prfFont.cmap.items():
        encodedGlyphs[v] = k

    for uni in sorted(prfFont.cmap):
        cell = GlyphCell(prfFont, uni=uni)
        cellsToDraw.append(cell)
        doneGlyphs.add(cell.glyphName)
        # add alt glyphs
        if not onlyEncodedGlyphs:
            for featureTags, glyphName in sorted(prfFont.altMapping.get(cell.glyphName, [])):
                if glyphName == cell.glyphName:
                    # it happens.
                    continue
                if glyphName not in doneGlyphs:
                    altCell = GlyphCell(prfFont, glyphName=glyphName, featureTags=featureTags)
                    cellsToDraw.append(altCell)
                    doneGlyphs.add(glyphName)

    if not onlyEncodedGlyphs:
        for glyphName in prfFont.glyphNames:
            if glyphName not in doneGlyphs:
                cell = GlyphCell(prfFont, glyphName=glyphName)
                cellsToDraw.append(cell)

    return cellsToDraw


def drawPage(pageNumber, fontFileName, cellsToDraw, formatting):
    from drawBot import newPage, font, fontSize, text
    assert len(cellsToDraw) <= formatting.glyphsPerPage
    timeString = time.asctime()
    newPage(formatting.pageWidth, formatting.pageHeight)
    font("LucidaFax")
    fontSize(9)
    text(u"Page %s \u2014 %s \u2014 %s" % (pageNumber, timeString, fontFileName),
            (formatting.leftMargin, formatting.pageHeight - formatting.topMargin))
    x = 0
    y = 0
    for cell in cellsToDraw:
        pt = (formatting.leftMargin + x * formatting.colDist,
                formatting.pageHeight - (formatting.topMargin + (y + 0.667) * formatting.rowDist))
        cell.draw(pt, formatting)
        x += 1
        if x >= formatting.nCols:
            x = 0
            y += 1
    assert y <= formatting.nRows


class FormattingParameters(object):

    def __init__(self, paperSize=None, sampleSize=24, labelSize=5, leftMargin=30, topMargin=40):
        from drawBot import sizes
        if paperSize is None:
            paperSize = sizes("A4")
        elif isinstance(paperSize, str):
            paperSize = sizes(paperSize)
        pageWidth, pageHeight = paperSize
        self.pageWidth = pageWidth
        self.pageHeight = pageHeight
        self.sampleSize = sampleSize
        self.rowDist = sampleSize * 1.83
        self.colDist = sampleSize * 1.75
        self.labelSize = labelSize
        self.labelOffset = sampleSize * 0.45
        self.labelLineDistance = labelSize * 1.1
        self.leftMargin = leftMargin
        self.topMargin = topMargin
        self.nRows = int((pageHeight - self.topMargin) / self.rowDist) - 1
        self.nCols = int((pageWidth - 1.5 * self.leftMargin) / self.colDist)
        self.glyphsPerPage = self.nRows * self.nCols


def proofFont(fontPath, pdfPath, startPage=None, endPage=None, formatting=None,
              paperSize=None, onlyEncodedGlyphs=False):
    from drawBot import saveImage
    fontFileName = os.path.basename(fontPath)

    if formatting is None:
        formatting = FormattingParameters(paperSize=paperSize)
    else:
        assert paperSize is None, "Can't specify both formatting and paperSize."

    print("Setting up proof...")
    prfFont = ProofFont(fontPath)
    cellsToDraw = buildGlyphCellList(prfFont, onlyEncodedGlyphs)

    nPages = len(cellsToDraw) // formatting.glyphsPerPage
    if len(cellsToDraw) % formatting.glyphsPerPage:
        nPages += 1

    if startPage is None:
        startPage = 1
    if endPage is None:
        endPage = nPages
    assert startPage >= 1
    assert endPage <= nPages
    assert startPage <= endPage

    prfFont.install()
    try:
        for pageNumber in range(startPage, endPage + 1):
            print("Creating page %s" % pageNumber)
            index = (pageNumber - 1) * formatting.glyphsPerPage
            cells = cellsToDraw[index:index+formatting.glyphsPerPage]
            drawPage(pageNumber, fontFileName, cells, formatting)

        print("Saving pdf...")
        saveImage(pdfPath)
    finally:
        prfFont.uninstall()


def _silenceQuartzWarnings():
    #
    # This is a terrible hack to silence an insane amount of insane warnings
    # that Quartz outputs. We silence the low-level stderr (which is where the
    # warnings are written) and redirect Python's stderr to stdout (where we
    # receive any tracebacks and Python warnings).
    #
    # Normally (ie. running this from RoboFont or DrawBot) these warnings go
    # to Console.app and are therefore easy to ignore, but as a command line
    # app they will be in your face.
    #
    # TODO: verify if the warnings still exist under El Capitan.
    #
    os.dup2(os.open("/dev/null", 0), 2)
    sys.stderr = sys.stdout


def main():
    from drawBot import newDrawing
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("fontfile", help="A font file to proof.", nargs="+")
    parser.add_argument("-o", "--output", help="Output directory for the generated PDFs.")
    parser.add_argument("-p", "--pagesize",
        help="The page size for the PDF, defaults to 'A4', but can be 'Letter' or anything DrawBot's sizes() function accepts.",
        default="A4")
    parser.add_argument("-s", "--size", help="The point size of the proofed chars.", default=24, type=int)
    parser.add_argument("-e", "--encoded", help="Show only encoded glyphs.", action="store_true", default=False)

    args = parser.parse_args()

    formatting = FormattingParameters(paperSize=args.pagesize, sampleSize=args.size)

    if args.output:
        assert os.path.isdir(args.output)

    _silenceQuartzWarnings()

    for fontPath in args.fontfile:
        fontFileName = os.path.split(fontPath)[1]
        print("processing", fontFileName)
        if args.output:
            pdfPath = os.path.join(args.output, fontFileName + ".pdf")
        else:
            pdfPath = fontPath + ".pdf"
        newDrawing()
        proofFont(fontPath, pdfPath, formatting=formatting, onlyEncodedGlyphs=args.encoded)


if __name__ == "__main__":
    main()
