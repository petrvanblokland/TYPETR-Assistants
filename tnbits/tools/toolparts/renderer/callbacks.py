# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    callbacks.py
#

import os
import traceback
import fontParts.world

from tnbits.renderer.freetyperenderer import FreetypeRenderer
from tnbits.toolbox.transformer import TX
from tnbits.analyzers.analyzermanager import analyzerManager
from tnbits.toolbox.glyphparts.glyphname import GlyphNameTX

class Callbacks(object):
    """
    GUI callbacks.
    """

    def renderCallback(self, sender):
        try:
            self.renderFreetypeFonts()
        except Exception as e:
            tracebackMessage = traceback.format_exc()
            self.renderTraceback = tracebackMessage
            print(tracebackMessage)

    def savePreferencesCallback(self, sender):
        view = self.getView()

        # Sets value selected from interface.
        self._minFontSize = self.FONTSIZES[view.selectMinFontSize.get()]
        self._maxFontSize = self.FONTSIZES[view.selectMaxFontSize.get()]

        # Stores in preferences.
        self.setPreference('minFontSize', self._minFontSize)
        self.setPreference('maxFontSize', self._maxFontSize)
        self.setPreference('scaledEm', view.scaledEm.get())
        self.setPreference('roundWidthUp', view.roundWidthUp.get())
        self.setPreference('exportTTF', view.exportTTF.get())

    def renderFreetypeFonts(self):
        """
        """
        styleKeys = self.getSelectedStyleKeys()
        view = self.getView()
        minSize = self._minFontSize
        maxSize = self._maxFontSize
        paths = []

        for styleKey in styleKeys:
            familyPath, styleName = styleKey

            if self.isTruetypeOpentype(styleName):
                parts = familyPath.split('/')
                path = '/'.join(parts[:-1]) + '/' + styleName
                paths.append(path)

        for path in paths:
            for size in range(minSize, maxSize+1):
                self.renderFreetypeFont(path, size)

    def renderFreetypeFont(self, path, size):
        f = fontParts.nonelab.RFont()
        fr = FreetypeRenderer(path, size)

        for glyphName, (_, charCode)  in fr.glyphsDict.items():
            try:
                self.renderGlyph(fr, f, path, glyphName, charCode, size)
            except Exception as e:
                print(e)
                continue

        f.update()
        self.saveFont(f, path, size)

    def printCharacterMap(self, f):
        cmap = f.getCharacterMapping()
        print('number of glyphs', len(cmap))

        for key in cmap.keys():
            print(key, cmap[key])

    def saveFont(self, f, path, size):
        view = self.getView()
        exportUfoPath = TX.path2FamilyDir(path) + '/export/scaled/ufo'
        exportTtfPath = TX.path2FamilyDir(path) + '/export/scaled/ttf'

        try:
            os.makedirs(exportUfoPath)
        except OSError:
            pass
        try:
            os.makedirs(exportTtfPath)
        except OSError:
            pass

        filePath = TX.path2FileName(path)
        # Save to make analyzer work.
        exportUfoFilePath = exportUfoPath + '/%s' % filePath.replace('.ttf','-%dpx.ufo' % size )
        exportTtfFilePath = exportTtfPath + '/%s' % filePath.replace('.ttf','-%dpx.ttf' % size )
        f.save(exportUfoFilePath)

        scaledEm = view.scaledEm.get()

        # Fill values that we know and save.
        f.info.familyName = TX.path2FamilyName(path)
        f.info.styleName = TX.path2StyleName(path) + ' Scaled %dpx' % size

        if scaledEm == 0:
            # Standard for OTF from whatever te original font was. Likely to gives horizontal rounding of width = interference of pixels.
            em = f.info.unitsPerEm
            asc = f.info.ascender
        elif scaledEm == 1:
            # Multiple of 64 fixed FreeType units. Makes the px sizes equal for all rendered sizes.
            em = 16 * 64
            asc = int(round(size*2/3))*64
        else:
            # Multiple of 64 fixed FreeType units. Set RF grid to 64 to see matching grid lines. Only way of having no horizontal round = pixel grid fit.
            em = size * 64
            asc = int(round(size*2/3))*64

        f.info.unitsPerEm = em
        f.info.ascender = asc
        f.info.descender = f.info.ascender - f.info.unitsPerEm

        # Let the analyzer guess vertical metrics.
        sa = analyzerManager.getStyleAnalyzer(style=f)
        f.info.xHeight = max(sa.xHeights.keys())
        f.info.capHeight = max(sa.capHeights.keys())

        # Export as plain TFF (without hinting)?
        if view.exportTTF.get():
            f.generate(exportTtfFilePath, format='ttf',
                checkOutlines=False,
                autohint=False,
                releaseMode=False,
                glyphOrder=None,
                useMacRoman=False
            )

        f.save()

    def renderGlyph(self, fr, f, path, glyphName, charCode, size):
        """Renders a single glyph."""
        view = self.getView()

        if charCode is None:
            print('Missing character code for glyph %s' % glyphName)
            return

        if glyphName not in f:
            f.newGlyph(glyphName)

        glyph = f[glyphName]
        u = glyph.unicode

        if u is None:
            glyph.unicode = charCode

        fr.loadGlyphByCharCode(u)
        glyph.width = fr.width
        pen = glyph.getPen()
        self.drawFreetypePoints(fr, pen)

        # Round right side up if there is < pixel/2 sidebearing in beam level.
        if view.roundWidthUp.get():
            # Better set width in hdmx table?
            #ga = analyzerManager.getGlyphAnalyzer(glyph)
            if glyph.rightMargin <= 16:
                glyph.width += 64
