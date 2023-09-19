# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#            autofbhint.py
#
#    http://www.freetype.org/freetype2/docs/glyphs/glyphs-6.html
#    Start point in UFO
#    http://unifiedfontobject.org/versions/ufo2/glif.html
#
from tnbits.constants import Constants
from tnbits.hinting.autohint.autohintbase import AutohintBase

Super = AutohintBase

class AutoFBHinter(Super):

    def autohintGlyph(self, glyph, hintType):
        """

        The `autohintGlyph` is the dispatcher for glyph specific
        hinter methods. Otherwise a generic method gives comment.

        """
        #bars = self.findBars(horizontals, cvtbar)
        i = [] # Collecting instructions
        # Save and set the current glyph, to avoid it as parameter in all  methods.
        savegGlyph = self.getGlyph()
        self.setGlyph(glyph)
        """
        gd = GlyphAnalyzer(glyph)
        gd.show()

        hook = 'autohint_' + glyph.name
        if hasattr(self, hook):
            getattr(self, hook)(hintType, gd, i)
        else:
            self.autohintGeneric(hintType, gd, i)
        # Reset the current glyph
        self.setGlyph(glyph)
        """
        return i # Answer the instructions as list

    def autohintGeneric(self, hintType, gd, i):
        self.autohintHorizontal(hintType, gd, i)
        self.autohintVertical(hintType, gd, i)
        self.autohintDiagonal(hintType, gd, i)
        self.autohintInterpolateUntouched(gd, i)

    def autohintHorizontal(self, hintType, gd, i):
        stems = gd.getStems()
        glyph = gd.getGlyph()

        i.append("""# (X) Autohints for %s""" % glyph.name)
        i.append('x')
        if hintType == self.C.WINGCOMMAND_ANTIALIASING:
            stem = None # Mark the current stem of the loop, end used for RSB
            for index, x in enumerate(sorted(stems.keys())):
                stem = stems[x]
                if index == 0: # If first, then handle left sidebearing and set reference point
                    self.autohintLsbLeftRight(stem, gd, i)
                else: # Otherwise this is a counter, round and set reference point
                    self.autohintRoundSetReferencePoint(stem, gd, i)
                self.autohintStemLeftRight(stem, gd, i)
            if stem is not None:
                self.autohintRsbLeftRight(stem, gd, i)

    def autohintLsbLeftRight(self, stem, gd, i):
        # Scale the left side bearing from @origin
        i.append('reference0 @origin') # SRP0[]
        i.append('indirect reference round white %d %s' % (stem.getLeftBase().index, gd.getCvtLsb().name)) # MIRP[M>RWh]

    def autohintRsbLeftRight(self, stem, gd, i):
        # Scale the right side bearing from @width
        i.append('reference0 @width') # SRP0[]
        i.append('indirect min round white @width %s' % gd.getCvtRsb().name) # MIRP[m<RWh]

    def autohintRoundSetReferencePoint(self, stem, gd, i):
        i.append('reference round gray %d' % stem.getLeftBase().index) # MDRP[M>RGr]

    def autohintStemLeftRight(self, stem, gd, i):
        # Assumed that the reference point is set to the left base already.
        # For now these instructions are for left-right unconstrained anti-aliased.
        for p in stem.getLeftAlternates():
            i.append('shift %d' % p.index) # SHP[0]
        base = stem.getRightBase()
        cvt = stem.getCVT()
        i.append('indirect black %d %s' % (base.index, cvt.name)) # MIRP[m>rBl]
        for p in stem.getRightAlternates():
            i.append('indirect black %d %s' % (p.index, cvt.name)) # MIRP[m>rBl]
            """ Alternative by DB is SHP or IP. Sort this out
            if base.x == p.x: # Shift if x are exactly the same
                i.append('shift %d' % p.index) # SHP[0]
            else: # Otherwise interpolate
                i.append('interpolate %d' % p.index) # IP[]
            """
    def autohintVertical(self, hintType, gd, i):
        glyph = self.getGlyph()
        i.append("""# (Y) Autohints for %s""" % glyph.name)
        i.append('y') # SVTCA[Y]
        #horizontals = self.findHorizontal()
        #if not horizontals:
        #    self.error('No horizontal found')

    def autohintBar(self, bar, hintType, gd, i):
        pass

    def autohintDiagonal(self, diagonal, hintType, gd, i):
        pass

    def autohintInterpolateUntouched(self, gd, i):
        i.append('interpolate x') # IUP[X]
        i.append('interpolate y') # IUP[Y]
