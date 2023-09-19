# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     ttfcompiler.py
#

import os
from ufo2fdk.outlineOTF import OutlineOTFCompiler
from fontTools.ttLib import TTFont, newTable

from tnbits.compilers.subsetting.gsubcompiler import GSUBCompiler
from tnbits.compilers.subsetting.gposcompiler import GPOSCompiler
from tnbits.compilers.subsetting.gdefcompiler import GDEFCompiler
from tnbits.compilers.subsetting.states import GPOSState, GSUBState, GDEFState

# TODO: move to constants.
HEAD = 'head'
MAXP = 'maxp'
CMAP = 'cmap'
GLYF = 'glyf'
GSUB = 'GSUB'
GPOS = 'GPOS'
GDEF = 'GDEF'
GASP = 'gasp'
HMTX = 'hmtx'
HHEA = 'hhea'
LOCA = 'loca'
KERN = 'kern'
NAME = 'name'
FPGM = 'fpgm'
PREP = 'prep'
OS2 = 'OS/2'
CFF = 'CFF'
CVT = 'cvt'

TIGHT_GLYPH_COMPARE = False
SUBSTITUTE_MISSING_GLYPHS = True
SUBSET_GPOSGSUB = True
SUBSET_INCLUDEKERN = True

class TTFCompiler(OutlineOTFCompiler):

    def setupTable_maxp(self):
        self.otf[MAXP] = maxp = self.ufo.maxp
        maxp.numGlyphs = len(self.glyphOrder)

    def setupTable_glyf(self):
        self.otf[GLYF] = glyf = newTable(GLYF)
        glyf.glyphs = glyphs = {}
        glyf.glyphOrder = self.glyphOrder
        for glyphName in glyf.glyphOrder:
            ttfglyph = self.ufo[glyphName]
            if ttfglyph is None:
                print('### [TrueTypeFont.setupTable_glyf] Cannot find expected glyph "%s"' % glyphName)
            else:
                glyphs[glyphName] = ttfglyph.getGlyf()

    def setupTable_kern(self):
        self.otf[KERN] = self.ufo.kern

    def setupTable_name(self):
        # Copy name table from source font
        self.otf[NAME] = self.ufo.name

    def setupTable_loca(self):
        # Create empty loca table, will be filled when compiling the font
        self.otf[LOCA] = newTable(LOCA)

    def setupTable_os2(self):
        # Copy OS/2 table from source font
        self.otf[OS2] = self.ufo.os2

    def setupTable_head(self):
        # Copy head table from source font
        self.otf[HEAD] = self.ufo.head

    def setupTable_hhea(self):
        self.otf[HHEA] = self.ufo.hhea

    def setupTable_hmtx(self):
        self.otf[HMTX] = self.ufo.hmtx

    def setupTable_cmap(self):
        self.otf[CMAP] = self.ufo.cmap

    def setupTable_cvt(self):
        # Copy cvt table from source font
        self.otf[CVT] = self.ufo.cvt.cvt

    def setupTable_fpgm(self):
        # Copy fpgm table from source font
        self.otf[FPGM] = self.ufo.fpgm

    def setupTable_prep(self):
        # Copy prep table from source font
        self.otf[PREP] = self.ufo.prep

    def setupTable_gasp(self):
        # Copy gasp table from source font
        self.otf[GASP] = self.ufo.gasp

    def setupTable_gsub(self):
        """
        Copy GSUB table from source font. If it is a GDUBState instance, then
        compile to the FontTools table GSUB first."""
        gsub = self.ufo.gsub
        if isinstance(gsub, GSUBState):
            gsub = GSUBCompiler().compile2Table(gsub, self.ufo)
        self.otf[GSUB] = gsub

    def setupTable_gpos(self):
        """Copy GPOS table from source font. If it is a GPOSState instance, then
        compile to FontTools table GPOS first."""
        gpos = self.ufo.gpos
        if isinstance(gpos, GPOSState):
            gpos = GPOSCompiler().compile2Table(gpos, self.ufo)
        self.otf[GPOS] = gpos

    def setupTable_gdef(self):
        """Copy GDEF gtable from source font. If it is a GDEFState instance, then
        #compiler to the FontTools table GDEF first."""
        gdef = self.ufo.gdef
        if isinstance(gdef, GDEFState):
            gdef = GDEFCompiler().compile2Table(gdef, self.ufo)
        self.otf[GDEF] = gdef

    def compile(self):
        """Compile the TTF. The self._ttfont is already a full TTX font, except that
        changes to e.g. the glyph should reflect in the other tables."""
        self.otf = TTFont()
        self.otf.glyphOrder = self.glyphOrder
        # populate basic tables
        self.setupTable_head()
        self.setupTable_hhea()
        self.setupTable_hmtx()
        self.setupTable_name()

        self.setupTable_cmap()
        self.setupTable_OS2()
        self.setupTable_post() # Calculated by FontTools
        #self.otf[POST].glyphOrder = self.glyphOrder
        self.setupTable_glyf()
        self.setupTable_maxp()

        self.setupTable_loca()

        # feature stuff
        if SUBSET_GPOSGSUB:
            self.setupTable_gdef()
            self.setupTable_gpos()
            self.setupTable_gsub()

        # copy obsolete kern table?
        if SUBSET_INCLUDEKERN:
            self.setupTable_kern()

        # hint stuff
        self.setupTable_cvt()
        self.setupTable_fpgm()
        self.setupTable_prep()
        self.setupTable_gasp()

        self.setupOtherTables()
        # clean up entries, if tables became None. This should never happen?
        for tableName, table in self.otf.tables.items():
            if table is None:
                del self.otf.tables[tableName]
                print('### [TrueTypeFont.compile] Warning: removed empty table "%s" from output font' % tableName)
        # if the file exists, delete it first
        if os.path.exists(self.path):
            os.remove(self.path)
        # write the actual file
        #self.otf.saveXML(self.path + '.xml', tables=['OS/2'])
        self.otf.save(self.path)
        # discard the object
        # self.otf.close()
        del self.otf
