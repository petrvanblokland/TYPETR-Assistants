# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     analyzer.py
#
import traceback
from tnbits.constants import Constants
from tnbits.analyzers.styleanalyzer import StyleAnalyzer
from tnbits.model.objects.style import getStyleKey
from tnbits.model import model

class AnalyzerManager(object):
    """The AnalyzerManager instance is a singleton dictionary of analyzers on
    open fonts.

    >>> # Analyzing a RoboFont font(=style)
    >>> from tnTestFonts import getFontPath
    >>> from tnbits.analyzers.analyzermanager import analyzerManager
    >>> from tnbits.toolbox.transformer import TX
    >>> from lib.fontObjects.factories import registerAllDoodleFactories
    >>> registerAllDoodleFactories()
    >>> path = getFontPath('Promise-Bold.ufo')
    >>> style = OpenFont('%s' % path, showUI=False)
    >>> sa = analyzerManager.getStyleAnalyzer(style=style)
    >>> print(TX.path2FileName(sa.style.path))
    Promise-Bold.ufo
    >>> ga = sa['H'] # GlyphAnalyzer from StyleAnalyzer
    >>> ga is analyzerManager.getGlyphAnalyzer(style['H']) # Or directly: same thing.
    True
    >>> print(ga.glyph.name, ga.glyph.width # The analyzer has a weakref to the glyph instance.)
    H 1640
    >>> print(len(ga.stems), sorted(ga.stems) # Analyzer can find the stems in the glyph.)
    13 [40, 48, 336, 357, 376, 405, 512, 520, 560, 648, 677, 896, 917]

    """

    C = Constants

    def __init__(self):
        self._styleAnalyzers = {}

    def getStyleAnalyzer(self, styleKey=None, style=None):
        # StyleKey has format (familyPath, fileName)
        if not styleKey and not style:
            return

        if style:
            styleKey = getStyleKey(style)

        if not styleKey in self._styleAnalyzers:
            # FIXME: Check if in RoboFont earlier.
            try:
                from mojo.events import addObserver as addMojoObserver
                addMojoObserver(self, 'styleWillClose', self.C.EVENT_FONTWILLCLOSE)
            except (ImportError, TypeError, IOError) as e:
                print(e)
                print(traceback.format_exc())

            self._styleAnalyzers[styleKey] = StyleAnalyzer(styleKey)

        # Make sure the family is open on this style.
        try:
            model.openFamily(styleKey=styleKey)
        except Exception as e:
            print(e)
            print(styleKey)
            print(traceback.format_exc())

        return self._styleAnalyzers[styleKey]

    def getGlyphAnalyzer(self, glyph, parent=None):
        if parent is None:
            parent = glyph.font

        styleAnalyzer = self.getStyleAnalyzer(style=parent)
        return styleAnalyzer[glyph.name]

    def styleWillClose(self, style):
        """Style is closing. Remove the delete style analyzer."""
        # TODO: restore observers.
        #style.removeObserver(self, self.C.EVENT_FONTWILLCLOSE)
        #self.removeStyle(style)
        pass

    def removeStyle(self, style):
        """Removes the style analyzer. This also will delete all cached glyph
        analyzers and free the reference to style and glyph instances."""
        styleKey = getStyleKey(style) # Format (familyPath, fileName)
        if styleKey in self._styleAnalyzers:
            del self._styleAnalyzers[styleKey] # Delete style analyzer and cached glyphs.

analyzerManager = AnalyzerManager()
