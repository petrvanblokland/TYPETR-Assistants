# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from tnbits.toolbox.file import File
import string
from tnbits.toolbox.transformer import TX

class GlyphOrderTX:
    """`GlyphOrder` provides some shortcuts for managing robofont glyphOrders,
    and converting between FontLab encodings and glyphOrders."""

    ########
    # SETTING GLYPH ORDERS
    ########

    @classmethod
    def getSortedGlyphs(cls, f):
        """Instead of the random processing order in `for g in f`,
        `getSortedGlyphs` returns glyphs in the font's glyph order."""
        glyphs = []
        for gname in f.glyphOrder:
            glyphs.append(f[gname])
        return glyphs

    @classmethod
    def sortGlyphs(cls):
        """Some shortcuts for unicode, alphabetical sorting, etc."""
        pass

    #######
    # IMPORT / EXPORT
    #######

    @classmethod
    def write(cls, glyphOrder, path=None, suggestedFileName = 'glyphOrder.json'):
        """Given a list of glyph names, `writePlist` creates a plist file at
        the specified path for storing and sharing purposes."""
        j = TX.list2Json(glyphOrder)
        if j:
            File.write(j, path, fileMessage='Write json glyphOrder', fileName='glyphOrder.json')

    @classmethod
    def read(cls, path=None):
        """Given a list of glyph names, `write` creates a json file at the
        specified path for storing and sharing purposes."""
        input = File.read(path, fileMessage='Get json glyphOrder')
        return TX.json2List(input)

    @classmethod
    def writePlist(cls, glyphOrder, path=None):
        """
        DEPRECATED. Given a list of glyph names, `writePlist` creates a plist file at the specified path.
        """
        from fontTools.ufoLib import writePlistAtomically
        if not path:
            from vanilla.dialogs import putFile
            path = putFile('Save PLIST as')
        glyphOrderDict = {'glyphOrder': glyphOrder}
        writePlistAtomically(glyphOrderDict, path)

    ##########
    # FONTLAB ENCODINGS
    ##########

    @classmethod
    def getIndexPairs(cls, glyphOrder):
        """Given a list of glyph names, `getIndexPairs` retuns that same glyph
        followed by its index number in the list. This is used to create
        FontLab encodings."""
        pairs = []
        tick = 0
        for gName in glyphOrder:
            pairs.append((gName, tick))
            tick += 1
        return pairs

    @classmethod
    def getFLEncodingRandomVersion(cls):
        """`getFLEncodingRandomVersion` returns a random number to distinguish
        it from other FontLab encodings. I don't know why."""
        import random
        return random.randint(1, 100000)

    @classmethod
    def getFLEncodingDefaultTitle(cls):
        """`getFLEncodingDefaultTitle` returns a generic title."""
        return 'Untitled'

    @classmethod
    def writeFLEncoding(cls, glyphOrder, title=None, version=None, path=None):
        """Given a list of glyph names, `writeFLEncoding` returns a
        FontLab-compatible encoding file."""
        result = ''
        if not title:
            title = cls.getFLEncodingDefaultTitle()
        if not version:
            version = cls.getFLEncodingRandomVersion()

        result += '%%FONTLAB ENCODING: ' + str(title) + '; ' + str(version)
        pairs = cls.getIndexPairs(glyphOrder)
        for gName, index in pairs:
            result += '\r%s %s' %(gName, index)
        File.write(result, path, fileMessage='Save Encoding as', fileName=str(title)+'.enc')

    @classmethod
    def readFLEncoding(cls, encPath=None, keepMetaData=False):
        """Given a path to a FontLab encoding file (.enc), `readFLEncoding`
        interprets it and returns a simple list of glyph names. Optionally, if
        _keepMetaData_ is true, it will also include a dict with the title and
        version."""

        GlyphOrderFile = File.read(encPath, 'Get GlyphOrder...')
        if GlyphOrderFile.find('\n') == -1:
            encLines = GlyphOrderFile.split('\r')
        else:
            encLines = GlyphOrderFile.split('\n')
        metaData = {}
        glyphList = []
        for l in encLines:
            if len(l) >= 1:
                if l[0] != '%':
                    lineList = l.split(' ')
                    if len(lineList) >= 1:
                        gName = lineList[0]
                        if gName not in glyphList:
                            glyphList.append(gName)
                        else:
                            print('\treadFLEncoding: Skipping duplicate glyph', gName)
                elif len(l) > 1 and l[0:2] == '%%':
                    l = l[2:]
                    key, value = l.split(':')
                    key = key.strip()
                    value = value.strip()
                    if key == 'FONTLAB GlyphOrder':
                        try:
                            uid, title = value.split(';')
                            uid = uid.strip()
                            title = title.strip()
                            metaData['title'] = title
                            metaData['id'] = uid
                        except:
                            pass
                    else:
                        metaData[key] = value
        if keepMetaData:
            return glyphList, metaData
        else:
            return glyphList
