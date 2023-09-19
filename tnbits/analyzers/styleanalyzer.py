# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     styleanalyzer.py
#
import weakref
from math import sin, pi

from tnbits.constants import Constants
from tnbits.analyzers.glyphanalyzer import GlyphAnalyzer

from tnbits.toolbox.storage.state import State
from tnbits.toolbox.transformer import TX
from tnbits.toolbox.compilers.feature2text import Feature2Text
from tnbits.model.smartlibs.profilegroups import ProfileGroups
from tnbits.model import model
from tnbits.model.objects.style import nakedStyle

class StyleAnalyzer(object):
    """The StyleAnalyzer class is a dictionary of GlyphAnalyzer instances
    related to StyleAnalyzer.styleId. A GlyphAnalyzer holds the analyzed
    information for a single glyph. The StyleAnalyzer.get(glyphName) answers
    the cached glyph analyzer. If it does not exist, it is created and the
    analysis is performed."""
    C = Constants

    GLYPHANALYZER_CLASS = GlyphAnalyzer # Can be modified by inheriting classes

    XHEIGHT_GLYPHS = 'xzyvw' # Several to search, the design may not be complete yet.
    ROUNDXHEIGHT_GLYPHS = 'oepqs'
    FLATCAP_GLYPHS = 'HIEFXBDLMNPYZ'
    ROUNDCAP_GLYPHS = 'CGOQ'
    ASCENDER_GLYPHS = 'lhbdk'
    ROUNDASCENDER_GLYPHS = 'f'
    BASELINE_GLYPHS = 'ABDEFHIKLMNPRTZinmz'
    ROUNDBASELINE_GLYPHS = 'CGSaceo'
    DESCENDER_GLYPHS = 'pq'
    ROUNDDESCENDER_GLYPHS = 'gj'

    def __init__(self, styleKey):
        assert isinstance(styleKey, tuple)
        style = model.getStyle(styleKey)
        self.style = nakedStyle(style)
        self.styleKey = styleKey
        self.analyzers = {} # Dictionary of glyph analyzers
        self._decomposedGlyphNames = None # Cached dictionary of key=baseName, value=dictionary of name/decomposed dict.
        # Feature2Text engine (will be initialized if self.features attribute is addresses.
        self._feature2Text = None
        # Caching profile groups
        #self._profileTolerance = 6 # Profile tolerance, set from the caller, as difference between Gauss average values.
        #self._xHeightProfileSteps = 24 # Default 24 bars of xHeight profile.
        self._profileGroups = None

    def __repr__(self):
        return '[%s of %s]' % (self.__class__.__name__, TX.path2FontName(self.style.path))

    # self[glyphName]
    # Cached glyph analyzers. Answer None if the named glyph does not exist in the style.

    def __getitem__(self, glyphName):
        if self.style is None:
            return None
        if not glyphName in self.analyzers:
            if not glyphName in self.style:
                return None
            self.analyzers[glyphName] = self.GLYPHANALYZER_CLASS(self, glyphName)
        return self.analyzers[glyphName]

    def get(self, glyphOrName):
        # Answer the analyzer of glyph from the floq in the glyph.
        name = glyphOrName
        if not isinstance(glyphOrName, str):
            name = glyphOrName.name
        return self[name]

    def __contains__(self, glyphName):
        if self.style is not None:
            return glyphName in self.style
        return False

    def keys(self):
        if self.style is not None:
            return self.style.keys()
        return []

    def __iter__(self):
        return iter(self.style)

    #   Features

    def _get_featureScripts(self):
        if self._feature2Text is None: # Still needs to be initialized?
            if self.style is not None:
                self._feature2Text = Feature2Text(self.style)
        return self._feature2Text
    featureScripts = property(_get_featureScripts)

    # self.decomposedGlyphNames
    # This gives back information about the base-diacritics relation in the style. It can be used
    # to easily show the relation between diacritics on anchors of a base glyph.

    def _get_decomposedGlyphNames(self):
        if self._decomposedGlyphNames is None:
            self._decomposedGlyphNames = d = {}
            for glyphName in self.keys():
                decomposed = self[glyphName].decomposedName
                baseName = decomposed['baseName'] # Base name includes extensions.
                if not baseName in d:
                    d[baseName] = {}
                d[baseName][decomposed['name']] = decomposed
        return self._decomposedGlyphNames
    decomposedGlyphNames = property(_get_decomposedGlyphNames)

    def glyphChanged(self, glyphName):
        """The glyphChanged method is called by the application if the
        _glyphName_ glyph was changed. The related GlyphAnalyzer entry is
        deleted from self._analyzers which will force the next
        self.get(glyphName) to create an new analyzer on the changed glyph.
        """
        if glyphName in self.analyzers:
            del self.analyzers[glyphName]

    # self.sizeRange

    def _get_sizeRange(self):
        """The sizeRange property calculates a guess about the size range that
        style can best be used.  It does that from a combination of contrast
        (difference between thin part and thick part of a number of base
        glyphs, the total bar/stem width, the size of the counters and the size
        of the spacing."""
        mainStems = self.mainStems
        stem = mainStems.capital or mainStems.capitalRound
        mainBars = self.mainBars
        bar = mainBars.capital or mainBars.capitalRound
        # Now the question is: at what point size is the bar >= 2/3*pixel?
        if bar:
            minSize = self.unitsPerEm / bar
        else:
            minSize = 0 # Unknown
        return minSize, 20
    sizeRange = property(_get_sizeRange)

    # self.mainBars

    def _get_mainBars(self):
        """the getMainBars method tries to get the main bars of this style.
        This is differen from the self.getBars(glyphs) which answers a list of
        bars of the specified glyphs. The self.getMainBars property will try to
        get the bar from the H and O glyphs based on the construction of
        points.  """
        bars = State()
        bars.capital = self.capitalBar
        bars.capitalRound = self.capitalRoundBar
        return bars
    mainBars = property(_get_mainBars)

    # self.capitalBar
    def _get_capitalBar(self):
        """
        Looks for bar size for capital H, E, F respectively.
        """
        bar = None
        style = self.style
        for cName in ('H', 'E', 'F'):
            if cName in style:
                bars = self.getBars('H')
                if bars: # If multiple found, take minimal value to be safe.
                    bar = min(bars.keys())
                    break
        return bar
    capitalBar = property(_get_capitalBar)

    def _get_capitalRoundBar(self):
        """
        Looks for round bar size for capital O or C.
        """
        roundBar = None
        style = self.style
        for cName in ('O', 'C'):
            if cName in style:
                roundBars = self.getRoundBars('O')
                if roundBars: # If found any, take minimal value to be safe
                    roundBar = min(roundBars.keys())
                    break
        return roundBar
    capitalRoundBar = property(_get_capitalRoundBar)

    # self.mainStems

    def _get_mainStems(self):
        """The getMainStems property tries to get the main stems of this
        font. This is different from the self.getStems(glyphs) which answers a
        list of stems of the specified glyphs. The self.getMainStems property
        will try to get the stem from the H glyph, based on the construction of
        points. If that fails a cross-beam is measured on the capital I for y
        is capHeight / 2. The same happens with lower case and figures."""
        stems = State()
        stems.capital = self.capitalStem
        stems.capitalRound = self.capitalRoundStem
        #stems.lowerCase = self.lowerCaseStem
        #stems.figure = self.figureStem
        return stems

    mainStems = property(_get_mainStems)

    # self.lowerCaseStem

    def _get_lowerCaseStem(self):
        """Gets the stem size for the lower cases. Tries to measure n, h,
        dotless i and i respectively.  """
        stem = None # In case it cannot be found
        if self.style is not None:
            for glyphName in ('n', 'h', 'dotlessi', 'i'):
                if not glyphName in self.style:
                    continue
                glyph = self.style[glyphName]
                ga = self.get(glyph) # Get the glyph analyzer for this glyph
                stem = int(round(ga.averageStemSize))
                if stem is not None:
                    break
        return stem
    lowerCaseStem = property(_get_lowerCaseStem)

    # self.figureStem

    def _get_figureStem(self):
        """Gets the stem size for the figure 1."""
        stem = None
        if self.style is not None:
            for glyphName in ('one',):
                if not glyphName in self.style:
                    continue
                glyph = self.style[glyphName]
                ga = self.get(glyph)
                stem = int(round(ga.averageStemSize))
                if stem is not None:
                    break
        return stem
    figureStem = property(_get_figureStem)

    # self.capitalStem
    def _get_capitalStem(self):
        """
        Looks for stem size for capital H and I respectively.
        """
        stem = None
        style = self.style
        if 'H' in style:
            stem = self.getStem('H')

        if not stem and 'I' in style:
            # If stem was still not found, then do a cross-ruler on the capital I.
            stem = self.getStem('I')

        return stem
    capitalStem = property(_get_capitalStem)

    # self.capitalRoundStem
    def _get_capitalRoundStem(self):
        """
        Looks for round stem size for capital O.
        """
        roundStem = None
        style = self.style
        if 'O' in style:
            roundStems = self.getRoundStems('O')
            if roundStems:
                roundStem = min(roundStems.keys())
        return roundStem
    capitalRoundStem = property(_get_capitalRoundStem)

    # self.stemH

    def _get_stemH(self, H='H'):
        """
        Gets the stem size for a capital H.
        """
        # Get the glyph analyzer for this glyph.
        ga = self.get(H)
        return int(round(ga.averageStemSize))

    getStem = _get_stemH
    stemH = property(_get_stemH)

    # self.stemI

    def _get_stemI(self, I='I'):
        """
        Gets the stem size for a capital I.
        """
        stem = None
        # Get the glyph analyzer for the capital I or other glyph as defined.
        ga = self.get(I)
        capHeight = self.getHeight('I')
        '''
        Try on different heights, since there may be something happening on the
        middle position of the capital I (e.g. a corner point or stencil).
        '''
        for offset in (0, 1, -1, 2, -2, 5, -5, 10, -10, 15, -15, 20, -20, 30, -30, 40, -40, 50, -50, 60, -60):
            # Calculate the width by crossing with the line on half capHeight
            intersections = ga.intersectLine((0, capHeight / 2 + offset), (I.width, capHeight / 2 + offset))
            if len(intersections) == 2:
                (p1x, _), (p2x, _) = intersections # (p1x, p1y), (p2x, p2y)
                stem = int(round(abs(p2x - p1x)))
                break # we found it, skip the other offsets
        '''
        If there was no intersection with two points, then the design probably
        does not allow intersecting this way to get the stem width. Measuring
        needs to be manual.
        '''
        return stem

    stemI = property(_get_stemI)

    def getNormalizedStems(self, capStem, lcStem, figStem):
        """Gets the normalized stems of the font, valued against the PPEM, so
        the values can be used as weight parameter to compare font weights.
        Thus ranging from 0 to 1000.  """
        nstems = {}
        nstems['normalized-capital-stem'] = self.normalize(capStem)
        nstems['normalized-lowercase-stem'] = self.normalize(lcStem)
        nstems['normalized-figure-stem'] = self.normalize(figStem)
        return nstems

    def normalize(self, value):
        """Answer the normalized value at 1000 PPEM."""
        return int(round(self.C.NORMALIZED_PPEM / self.style.info.unitsPerEm * value))

    # self.weightValue

    def _get_weightValue(self):
        """Answer the stem width of the capital H, normalized to an em of
        1000."""
        return self.normalize(self.stemH)

    weightValue = property(_get_weightValue)

    # self.widthValue

    def _get_widthValue(self):
        """Answer the width of the capital I, normalized to an em of 1000."""
        return self.normalize(self['I'].glyphWidth)

    widthValue = property(_get_widthValue)

    # self.angle
    # self.italicAngle

    def _get_angle(self):
        """Answer the italic angle of the font."""
        return self.style.info.italicAngle

    italicAngle = angle = property(_get_angle)

    # self.stems

    def _get_stems(self, glyphs=None):
        # TODO: Might change this to a list of glyphNames instead.
        if glyphs is None:
            glyphs = self.style
        stems = {}
        for glyph in glyphs:
            ga = self.get(glyph)
            for size, glyphStems in ga.stems.items():
                if not size in stems:
                    stems[size] = []
                for stem in glyphStems:
                    stems[size].append(stem)
        return stems

    getStems = _get_stems # Allow to call with set of glyphs
    stems = property(_get_stems)

    def getRoundStems(self, glyphs=None):
        # TODO: Might change this to a list of glyphNames instead.
        if glyphs is None:
            glyphs = self.style
        stems = {}
        for glyph in glyphs:
            ga = self.get(glyph)
            for size, glyphStems in ga.roundStems.items():
                if not size in stems:
                    stems[size] = []
                for stem in glyphStems:
                    stems[size].append(stem)
        return stems

    # self.bars

    def _get_bars(self, glyphs=None):
        # TODO: Might change this to a list of glyphNames instead.
        if glyphs is None:
            glyphs = self.style
        bars = {}
        for glyph in glyphs:
            ga = self.get(glyph)
            for size, glyphBars in ga.bars.items():
                if not size in bars:
                    bars[size] = []
                for bar in glyphBars:
                    bars[size].append(bar)
        return bars

    getBars = _get_bars
    bars = property(_get_bars)

    # self.roundBars

    def _get_roundBars(self, glyphs=None):
        # TODO: Might change this to a list of glyphNames instead.
        if glyphs is None:
            glyphs = self.style
        bars = {}
        for glyph in glyphs:
            ga = self.get(glyph)
            for size, glyphBars in ga.roundBars.items():
                if not size in bars:
                    bars[size] = []
                for bar in glyphBars:
                    bars[size].append(bar)
        return bars

    getRoundBars = _get_roundBars
    roundBars = property(_get_roundBars)

    # self.getTops()
    # self.tops

    def _get_tops(self, glyphNames=None):
        """Answer a dictionary, where the keys are found heights and the
        values are lists of glyph names, fitting that key height."""
        tops = {}

        if glyphNames is None:
            glyphNames = self.style.keys()

        for glyphName in glyphNames:
            ga = self.get(glyphName)
            maxY = ga.maxY
            if maxY is not None:
                if not maxY in tops:
                    tops[maxY] = []
                tops[maxY].append(glyphName)
        return tops

    getTops = _get_tops
    tops = property(_get_tops)

    # self.getBottoms()    Get the bottoms of a given list of glyphNames.
    # self.bottoms            Get the bottoms of all glyphs

    def _get_bottoms(self, glyphNames=None):
        bottoms = {}
        if glyphNames is None:
            glyphNames = self.style.keys()
        for glyphName in glyphNames:
            ga = self.get(glyphName)
            minY = ga.minY
            if minY is not None:
                if not minY in bottoms:
                    bottoms[minY] = []
                bottoms[minY].append(glyphName)
        return bottoms

    getBottoms = _get_bottoms
    bottoms = property(_get_bottoms)

    # self.overshoots   Answer the overshoots of /o and /O if available.

    def _get_overshoots(self):
        overshoots = {}
        if 'O' in self.style:
            boundings = self['O'].boundings
            if boundings is not None and not None in boundings:
                overshoots['O'] = (self.capHeight, boundings[3] - self.capHeight), (0, boundings[1])
        if 'O.sc' in self.style and 'H.sc' in self.style:
            boundings = self['O.sc'].boundings
            Hboundings = self['H.sc'].boundings
            if boundings is not None and not None in boundings and Hboundings is not None:
                overshoots['O.sc'] = (Hboundings[3], boundings[3] - Hboundings[3]), (0, boundings[1])
        if 'o' in self.style:
            boundings = self['o'].boundings
            if boundings is not None and not None in boundings:
                overshoots['o'] = (self.xHeight, boundings[3] - self.xHeight), (0, boundings[1])
        if 'n' in self.style:
            boundings = self['n'].boundings
            if boundings is not None and not None in boundings:
                overshoots['n'] = ((self.xHeight, boundings[3] - self.xHeight),)
        return overshoots
    overshoots = property(_get_overshoots)

    # self.scapHeight     Smallcap Height, derived from the flat smallcaps if they exist.

    def _get_scapHeight(self):
        for capName in self.FLATCAP_GLYPHS:
            scapName = capName + '.sc'
            if scapName in self.style and self[scapName].boundings is not None and not None in self[scapName].boundings:
                return self[scapName].boundings[3]
        # No SC control glyph exist yet. Answer 1/4 between xHeight and capHeight as default.
        return self.xHeight + (self.capHeight - self.xHeight)/4
    scapHeight = property(_get_scapHeight)

    # self.capHeight

    def _get_capHeight(self):
        return self.style.info.capHeight
    capHeight = property(_get_capHeight)

    # self.capHeights

    def _get_capHeights(self):
        """Answer the dictionary of cap heights for the glyhps in unicode
        string _glyphs_.  Key if y-position, value is a list of glyphs for
        that position."""
        return self.getTops(self.FLATCAP_GLYPHS)
    capHeights = property(_get_capHeights)

    # self.roundCapHeights

    def _get_roundCapHeights(self):
        """Answer the set of cap heights for the glyphs in unicode string
        _glyphs_."""
        return self.getTops(self.ROUNDCAP_GLYPHS)

    roundCapHeights = property(_get_roundCapHeights)

    # self.ascender

    def _get_ascender(self):
        """Answer the `font.info.ascender`. Note that this is different
        from `self.ascenders` which will answer a list of tops of ascender
        glyphs."""
        return self.style.info.ascender

    ascender = property(_get_ascender)

    # self.ascenders

    def _get_ascenders(self):
        """Answer the dictionary of ascenders for the glyphs in unicode string
        _glyphs_. Key if y-position, value is a list of glyphs for that
        position."""
        return self.getTops(self.ASCENDER_GLYPHS)
    ascenders = property(_get_ascenders)

    # self.roundAscenders    Answer the overschoot ascender

    def _get_roundAscenders(self):
        """Answer the dictionary of round ascenders for the glyphs in unicode string _glyphs_.
        Key if y-position, value is a list of glyphs for that position."""
        return self.getTops(self.ROUNDASCENDER_GLYPHS)
    roundAscenders = property(_get_roundAscenders)

    # self.ascenderHeight Answer the true height of the control ascender(s). None if not existing.
    def _get_ascenderHeight(self):
        """Answer the smallest key value of self.ascenders or
        self.roundAscenders.  Answer None if there is no control ascender
        available."""
        ascenders = self.ascenders
        if ascenders:
            return min(ascenders.keys())
        ascenders = self.roundAscenders
        if ascenders:
            return min(ascenders.keys())
        return None
    ascenderHeight = property(_get_ascenderHeight)

    # self.xHeight

    def _get_xHeight(self):
        return self.style.info.xHeight

    xHeight = property(_get_xHeight)

    # self.xHeights

    def _get_xHeights(self):
        """Get the straight xHeights by searching some standard glyphs,
        assuming they have the right shape and size. We are not using the
        font.info here, as this could be the value to be detected from the
        glyph drawings."""
        return self.getTops(self.XHEIGHT_GLYPHS)

    xHeights = property(_get_xHeights)

    # self.roundxHeights

    def _get_roundxHeights(self):
        """Get the round xHeights by searching some standard glyphs, assuming
        they have the right shape and size. We are not using the font.info
        here, as this could be the value to be detected from the glyph
        drawings."""
        return self.getTops(self.ROUNDXHEIGHT_GLYPHS)

    roundxHeights = property(_get_roundxHeights)

    # self.xOvershoot

    def _get_xOvershoot(self):
        # TODO Not so efficient; much it thrown away in this analysis.
        # Solve this more flat in the future update.
        return self.getRoundedxHeight() - self.xHeight

    xOvershoot = property(_get_xOvershoot)

    # self.maxxHeight

    def _get_maxxHeight(self):
        xHeights, roundxHeights = self.xHeights
        return max(xHeights | roundxHeights)

    maxxHeight = property(_get_maxxHeight)

    # self.baselines

    def _get_baselines(self):
        return self.getBottoms(self.BASELINE_GLYPHS),

    baselines = property(_get_baselines)

    # self.roundBaselines

    def _get_roundBaselines(self):
        return self.getBottoms(self.ROUNDBASELINE_GLYPHS)

    roundBaselines = property(_get_roundBaselines)

    # self.descender

    def _get_descender(self):
        """Answer the font.info.descender. Note that this is different from
        `self.descenders` which will answer a list of bottoms of descender
        glyphs."""
        return self.style.info.descender

    descender = property(_get_descender)

    # self.descenders

    def _get_descenders(self):
        return self.getBottoms(self.DESCENDER_GLYPHS)

    descenders = property(_get_descenders)

    # self.roundDescenders

    def _get_roundDescenders(self):
        return self.getBottoms(self.ROUNDDESCENDER_GLYPHS)

    roundDescenders = property(_get_roundDescenders)

    # self.descenderHeight Answer the true height of the control descender(s). None if not existing.
    def _get_descenderHeight(self):
        """Answer the largest key value of self.descenders or
        self.roundDescenders.  Answer None if there is no control descender
        available."""
        descenders = self.descenders
        if descenders:
            return max(descenders.keys())
        descenders = self.roundDescenders
        if descenders:
            return max(descenders.keys())
        return None

    descenderHeight = property(_get_descenderHeight)

    def getYRange(self, rangeName):
        """Answer the (y1, y2) tuple for the current style that corresponds
        with the vertical range label."""
        y0 = 0
        if rangeName == 'descender':
            y0 = self.descender
            y1 = 0
        elif rangeName == 'xHeight':
            y1 = self.xHeight
        elif rangeName == 'scapHeight':
            y1 = self.scapHeight
        elif rangeName == 'capHeight':
            y1 = self.capHeight
        else: # rangeName == 'ascender'
            y1 = self.ascender
        return y0, y1

    FIGURES_TOP = (
        # Order of "expected flatness")
         'seven', 'five', 'one', 'two', 'three', 'nine', 'four', 'five', 'six', 'eight',
    )

    FIGURES_BASE = (
         'seven', 'five', 'one', 'two', 'three', 'nine', 'four', 'five', 'six', 'eight',
    )

    # self.SINFHeight   Answer the estimated y-position of the .sinf numbers top

    def _get_SINFHeight(self):
        for inferiorName in self.FIGURES_TOP:
            name = inferiorName + '.sinf'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return max(y1, y2)
        return None

    SINFHeight = property(_get_SINFHeight)

    # self.SINFBase   Answer the estimated y-position of the .sinf figures base
    def _get_SINFBase(self):
        for inferiorName in self.FIGURES_BASE:
            name = inferiorName + '.sinf'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return min(y1, y2)
        return None

    SINFBase = property(_get_SINFBase)

    # self.DNOMHeight   Answer the estimated y-position of the .dnom figures top
    def _get_DNOMHeight(self):
        for inferiorName in self.FIGURES_TOP:
            name = inferiorName + '.dnom'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return max(y1, y2)
        return None

    DNOMHeight = property(_get_DNOMHeight)

    # self.DNOMBase   Answer the estimated y-position of the .dnom figures base
    def _get_DNOMBase(self):
        for inferiorName in self.FIGURES_BASE:
            name = inferiorName + '.dnom'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return min(y1, y2)
        return None

    DNOMBase = property(_get_DNOMBase)

    # self.NUMRHeight   Answer the estimated y-position of the .numr figures top
    def _get_NUMRHeight(self):
        for inferiorName in self.FIGURES_TOP:
            name = inferiorName + '.numr'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return max(y1, y2)
        return None

    NUMRHeight = property(_get_NUMRHeight)

    # self.NUMRBase   Answer the estimated y-position of the .numr figures base
    def _get_NUMRBase(self):
        for inferiorName in self.FIGURES_BASE:
            name = inferiorName + '.numr'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return min(y1, y2)
        return None

    NUMRBase = property(_get_NUMRBase)

    # self.SUPSHeight   Answer the estimated y-position of the .sups figures top
    def _get_SUPSHeight(self):
        for inferiorName in self.FIGURES_TOP:
            name = inferiorName + '.sups'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return max(y1, y2)
        return None

    SUPSHeight = property(_get_SUPSHeight)

    # self.SUPSBase   Answer the estimated y-position of the .sups figures base
    def _get_SUPSBase(self):
        for inferiorName in self.FIGURES_BASE:
            name = inferiorName + '.sups'
            if name in self.style:
                ga = self[name]
                _,  y1, _, y2 = ga.boundings
                if not y1 is None:
                    return min(y1, y2)
        return None

    SUPSBase = property(_get_SUPSBase)

    # self.unitsPerEm

    def _get_unitsPerEm(self):
        """Answer the units per em for this font. Identical to `self.style.info.unitsPerEm`."""
        return self.style.info.unitsPerEm

    em = unitsPerEm = property(_get_unitsPerEm)

    def angledP(self, x, y):
        """Answer the (x, y) value for angled y (using the style italic angle),
        where angledY(0, 0) -> (0, 0)."""
        return x+sin(pi*self.angle/180)*y

    # self.metrics

    def _get_metrics(self):
        """Answer a state collection of all relevant metrics of the font."""
        metrics = State()
        metrics.stems = self.getStems('HIEF')
        metrics.roundStems = self.getRoundStems('DOo')
        metrics.bars = self.getBars('HEF')
        metrics.roundBars = self.getRoundBars('Oo')
        metrics.capHeight = self.capHeight
        metrics.capHeights = self.capHeights
        metrics.roundCapheights = self.roundCapHeights
        metrics.xHeight = self.xHeight
        metrics.xHeights = self.xHeights
        metrics.roundxheights = self.roundxHeights
        metrics.baselines = self.baselines
        metrics.roundBaselines = self.roundBaselines
        metrics.ascender = self.ascender
        metrics.ascenders = self.ascenders
        metrics.roundAscenders = self.roundAscenders
        metrics.baselines = self.baselines
        metrics.roundBaselines = self.roundBaselines
        metrics.descender = self.descender
        metrics.descenders = self.descenders
        metrics.roundDescenders = self.roundDescenders
        return metrics

    metrics = property(_get_metrics)

    def show(self):
        s = []
        s.append('=== Font Data %s' % self.style.info)

        s.append('\n\n...STEMS')
        for size, stems in sorted(self.stems.items()):
            s.append('\n% 4d % 4d ' % (size, len(stems)))
            # s.append('\n% 4d %s' % (size, len(stems) * '*'))
            for stem in stems:
                s.append('[%s]' % stem.glyphName)

        s.append('\n\n...ROUND STEMS')
        for size, stems in sorted(self.roundStems.items()):
            s.append('\n% 4d % 4d ' % (size, len(stems)))
            # s.append('\n% 4d %s' % (size, len(stems) * '*'))
            for stem in stems:
                s.append('[%s]' % stem.glyphName)

        s.append('\n\n...BARS')
        for size, bars in sorted(self.bars.items()):
            s.append('\n% 4d % 4d ' % (size, len(stems)))
            # s.append('\n% 4d %s' % (size, len(stems) * '*'))
            for bar in bars:
                s.append('[%s]' % bar.glyphName)

        s.append('\n\n...ROUND BARS')
        for size, bars in sorted(self.roundBars.items()):
            s.append('\n% 4d % 4d ' % (size, len(stems)))
            # s.append('\n% 4d %s' % (size, len(stems) * '*'))
            for bar in bars:
                s.append('[%s]' % bar.glyphName)

        return ''.join(s)

    #   P R O F I L E S

    def _get_profileGroups(self):
        """Answer the ProfileGroups, as cached in the style. Create it, if it does not exists."""
        return ProfileGroups.getLib(self.styleKey)
    profileGroups = property(_get_profileGroups)

    def getProfile(self, sideName, glyphName, rangeName, create=False):
        return self.profileGroups.getProfile(sideName, glyphName, rangeName, create=create)
