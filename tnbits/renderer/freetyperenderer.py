#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    freetyperenderer.py
#

import freetype
import traceback
from tnbits.toolbox.character import CharacterTX
from tnbits.renderer.bitmap import bitmapToPNG
from tnbits.toolbox.transformer import TX
from tnbits.base.future import chr

class FreetypeRenderer(object):
    """Renders a font to a certain pixel size. See also:

    https://github.com/rougier/freetype-py/blob/master/examples/glyph-vector-2.py
    https://github.com/rougier/freetype-py/blob/master/examples/agg-trick.py
    """

    # Initialization.

    def __init__(self, path, size, pixelFraction=64):
        """Sets up a renderer for a font at path."""
        self.path = path
        self.familyName = TX.path2FamilyName(path)
        self.styleName = TX.path2StyleName(path)
        self.size = size
        self.pixelFraction = pixelFraction
        self.face = freetype.Face(path)
        self.face.set_char_size(size*pixelFraction)
        self.numberOfGlyphs = self.face.num_glyphs
        self.charCodes = {}
        self.setCharCodeIndices()
        self.glyphsDict = {}
        self.bitmapsDict = {}
        self.setAllCharacters()
        self.lastLoaded = None

    def setCharCodeIndices(self):
        """Maps all existing char codes to the corresponding glyph indices."""
        charCode, gindex = self.face.get_first_char()
        self.charCodes[charCode] = gindex

        for i in range(self.numberOfGlyphs - 1):
            charCode, gindex = self.face.get_next_char(charCode, gindex)
            self.charCodes[charCode] = gindex

    def setAllCharacters(self):
        """Loads all glyphNames in tuples with corresponding Unicode names and
        TTF char codes."""
        for charCode in self.charCodes.keys():
            unicodeName = chr(charCode)
            glyphName = CharacterTX.char2GlyphName(unicodeName)
            self.glyphsDict[glyphName] = (unicodeName, charCode)

    # Load.

    def loadGlyphByCharCode(self, cc):
        """Takes a decimal Unicode value and loads the corresponding glyph if
        present. Loads glyph by character code, needed because loading by glyph
        _name_ only works for the base set of Latin names."""
        assert cc in self.charCodes
        gindex = self.charCodes[cc]
        self.face.load_glyph(gindex)
        self.update()
        self.lastLoaded = cc

    def loadGlyphByName(self, glyphName):
        """Loads glyph by glyph name, only works for the base set of Latin
        names."""
        assert glyphName in self.glyphsDict.keys()
        self.face.load_char(glyphName)
        self.update()
        _, charCode = self.glyphsDict[glyphName]
        self.lastLoaded = charCode

    def update(self):
        """Copies some glyph values for quicker access. Should be called every
        time a new glyph is loaded."""
        self.width = self.face.glyph.metrics.horiAdvance # Post-hinting width as verified by Just.
        self.bitmap = self.face.glyph.bitmap
        self.bitmapWidth = self.face.glyph.bitmap.width
        self.rows = self.face.glyph.bitmap.rows
        self.pitch = self.face.glyph.bitmap.pitch
        self.bitmapLeft = self.face.glyph.bitmap_left
        self.bitmapTop = self.face.glyph.bitmap_top
        self.bitmapBaseLine = self.rows - self.bitmapTop

    # Glyph.

    def getGlyph(self):
        return self.face.glyph

    def getGlyphNameByCharCode(self, charCode):
        """Looks up glyph name for given character code in stored dictionary."""
        for glyphName, (_, cc) in self.glyphsDict.items():
            if charCode == cc:
                return glyphName

    def getOutline(self):
        """"""
        return self.face.glyph.outline

    # Info.

    def getInfo(self):
        print('--- %s %s ---' % (self.familyName, self.styleName))
        print("Scalable:         ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_SCALABLE))
        print("Fixed sizes:      ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_FIXED_SIZES))
        print("Fixed width:      ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_FIXED_WIDTH))
        print("SFNT:             ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_SFNT))
        print("Horizontal:       ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_HORIZONTAL))
        print("Vertical:         ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_VERTICAL))
        print("Kerning:          ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_KERNING))
        print("Fast glyphs:      ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_FAST_GLYPHS))
        print("Multiple masters: ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_MULTIPLE_MASTERS))
        print("Glyph names:      ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_GLYPH_NAMES))
        print("External stream:  ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_EXTERNAL_STREAM))
        print("Hinter:           ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_HINTER))
        print("CID Keyed:        ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_CID_KEYED))
        print("Tricky:           ", bool(self.face.face_flags & freetype.FT_FACE_FLAG_TRICKY))

    # Bitmap.

    def getBitmap(self):
        """Loads the bitmap data as a nested list.
        TODO: reshape as numpy array.
        """
        bitmap = []

        for i in range(self.rows):
            rowData = []

            for n in range(self.bitmapLeft):
                rowData.append(0)

            rowData.extend(self.bitmap.buffer[i * self.pitch:i * self.pitch + self.bitmapWidth])
            bitmap.append(rowData)

        return bitmap

    def addWhitespaceRows(self, bitmap, l):
        """
        Adds rows of zeros. FIXME: better way to do this with numpy?
        """
        fullWidth = self.bitmapLeft + self.bitmapWidth

        for n in range(l):
            rowData = []

            for r in range(fullWidth):
                rowData.append(0)

            bitmap.insert(0, rowData)

        return bitmap

    def getInvertedBitmap(self):
        """Inverts greyscale values."""
        inverted = []
        bitmap = self.getBitmap()

        for row in bitmap:
            rowData = []

            for value in row:
                rowData.append(256 - value)

            inverted.append(rowData)

        return inverted

    def saveBitmap(self, folder, inverted=True):
        """Converts a bitmap to a PNG file."""
        glyphName = self.getGlyphNameByCharCode(self.lastLoaded)

        if glyphName is None:
            return 'Cannot find glyphName for %d' % self.lastLoaded

        if inverted:
            bitmap = self.getInvertedBitmap()
        else:
            bitmap = self.getBitmap()

        l = len(bitmap)
        msg = '%s: %d\n' % (glyphName, l)

        if l == 0:
            msg = (msg, 'warning')

        if glyphName.isupper():
            name = glyphName.lower() + '_upper'
        else:
            name = glyphName.lower() + '_lower'

        fileName = '%s-%s-%s-%dpx' % (familyName, styleName, name, self.size)
        bitmapToPNG(bitmap, folder, fileName)
        return msg

    # Kerning.

    """NOTE: not fully supported, using FontTools for actual kerning lookup.

    From the FreeType documentation:

    “Not all font formats contain kerning information, and not all kerning
    formats are supported by FreeType; in particular, for TrueType fonts,
    the API can only access kerning via the ‘kern’ table. OpenType kerning
    via the ‘GPOS’ table is not supported! You need a higher-level library
    like HarfBuzz, Pango, or ICU, since GPOS kerning requires contextual
    string handling.”
    """

    def getKerning(self, glyphName0, glyphName1):
        kerning = self.face.get_kerning(glyphName0, glyphName1, freetype.FT_KERNING_DEFAULT)

    def hasKerning(self):
        return self.face.has_kerning

    def showAllKerningValues(self):
        """Loops over all glyph indices twice to see if getKerning yields
        results.  Doesn't seem to give any results."""
        messages = []
        indices = self.charCodes.values()

        for i in indices:
            for j in indices:
                if i == j:
                    continue
                messages.append(fr.getKerning(i, j))


        for m in messages:
            if m is not None:
                print(m)

if __name__ == '__main__':
    """Loads the renderer and tests it on a glyph."""
    import tnTestFonts
    from tnbits.base.samples import QUICK_BROWN_FOX_TEXT
    size = 32
    familyName = 'Gasket'
    styleName = 'Regular'
    path = tnTestFonts.getFontPath('%s-%s.ttf' % (familyName, styleName))
    base = '/Users/michiel/Desktop/DeepSpace'
    fr = FreetypeRenderer(path, size)

    # Loads glyphs, saves them to PNG files.
    for char in QUICK_BROWN_FOX_TEXT:
        glyphName = CharacterTX.char2GlyphName(char)

        if glyphName == 'space':
            continue

        print(' * ', glyphName)

        unicodeName, charCode = fr.glyphsDict[glyphName]
        fr.loadGlyphByCharCode(charCode)
        b = fr.getInvertedBitmap()
        h = len(b)
        w = len(b[0])

        try:
            fr.saveBitmap(base)
        except Exception as e:
            print(traceback.format_exc())

    #path = tnTestFonts.getFontPath('Gasket-Regular.ttf')
    #fr = FreetypeRenderer(path, size)
    from tnbits.deepspace.obtain import collectTrueTypes
    path = '/Users/michiel/Fonts/TypeNetwork'

    tts = collectTrueTypes(path, maximum=100)
    from fontTools.ttLib import TTFont

    for tt in tts:
        #fr = FreetypeRenderer(tt, size)
        f = TTFont(tt)
        if 'gpos' in f:
            gpos = f['gpos']
            print('GPOS', type(gpos), len(gpos))

        if 'kern' in f:
            kern = f['kern'].kernTables[0].kernTable

            # Can be faster to make a copy.
            #for pair, value in kern.items():
            #    print(pair, value)
            print('KERN', type(kern), len(kern))

        #if fr.hasKerning():
        #    fr.showAllKerningValues()
