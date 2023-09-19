# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     truetypefont.py
#


import traceback
from tnbits.objects.truetypeglyph import TrueTypeGlyph
from tnbits.objects.ttfcompiler import TTFCompiler
from fontTools.ttLib import TTFont #, newTable


from extractor.formats.opentype import extractOpenTypeInfo, extractOpenTypeGlyphs


from tnbits.compilers.subsetting.gsubcompiler import GSUBCompiler
from tnbits.compilers.subsetting.gposcompiler import GPOSCompiler
from tnbits.compilers.subsetting.gdefcompiler import GDEFCompiler
from tnbits.compilers.subsetting.states import State

# G L Y P H names
#GLYPH_NULL = '.null'
#GLYPH_NOTDEF = '.notdef'

# T A B L E names
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
CFF = 'CFF '
CVT = 'cvt '
POST = 'post'
BASE = 'BASE'
VORG = 'VORG'
VHEA = 'vhea'
VMTX = 'vmtx'

PROGRAM = 'program'

class TrueTypeCvt(object):

    def __init__(self, cvt):
        self._cvt = cvt

    def __getitem__(self, index):
        return self._cvt.values[index]

    def __setitem__(self, index, value):
        self._cvt.values[index] = value

    def __iter__(self):
        for value in self._cvt.values:
            yield value

    def __len__(self):
        return len(self._cvt.values)

    # cvt

    def _get_cvt(self):
        return self._cvt

    def _set_cvt(self, cvt):
        self._cvt = cvt  # Must be table__c_v_t

    cvt = property(_get_cvt, _set_cvt)

class TrueTypeFont(object):
    """The TrueTypeFont class is a wrapper class around a fontTools.TTFont
    that offers an API with a higher level of abstraction. This way tables can
    be manipulated without going all the way towards storing the font as a UFO
    while losing data -- not all tables can be stored in UFO."""

    # Flags to indicate if expansion should be done during construction of the
    # instance or later.
    EXTRACT_GSUB = True
    EXTRACT_GPOS = True
    EXTRACT_GLYPHS = True

    # Table names are used as "alternative" glyph names, so the TrueTypeFont
    # can be used for both glyph access (font['a']) and table access
    # (font[HEAD]), to make the TrueTypeFont instance be compatible with both
    # RoboFont fonts and TTFont. Assumption is that there will be no overlap
    # between the table names and the glyph names. In that case the table
    # prefers.

    TABLENAMES = (BASE, CFF, CMAP, CVT, FPGM, GLYF, GPOS, GSUB, GDEF, GASP, HEAD,
        HHEA, HMTX, KERN, LOCA, MAXP, NAME, OS2, POST, PREP, 'GlyphOrder',
        VORG, VHEA, VMTX)

    def __init__(self, path, extractGlyphs=EXTRACT_GLYPHS):
        self._path = path
        self._ttfont = TTFont(path)
        self._info = None  # To be initialized when requested.
        self._glyphSetName = None  # Undefined, unless a subset is made.
        self._componentRefs = None  # Caching for the component frequency counter.
        self._glyphs = {}
        self._unicodes = None  # Caching for access of glyphs that have their Unicode value set.
        self._gsub = None  # Storage of the decompiled GSUBState data construct.
        self._gpos = None  # Storage of the decompiled GPOSState data construct.
        self._gdef = None  # Storage of the decompiled GDEFState data construct.
        self._cff = None # Storage of the decompiled CFFState data construct.

        if extractGlyphs:
            try:
                extractOpenTypeGlyphs(self._ttfont, self)
            except:
                pass

        # TODO: Kind of hack: make sure these are initialized.
        # Should become part of attribute list, to check on for every type of table.
        # Otherwise Segoe mistake in Thai font: Lookup uni0E33 changes to uni0E32 ???
        if self.EXTRACT_GSUB:
            self.gsub
        if self.EXTRACT_GPOS:
            self.gpos

        # Defcon font compatibility
        layerName = 'foreground'

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._path.split('/')[-1])

    #     G L Y P H  S U P P O R T

    def __getitem__(self, name):
        """Table names are used as "alternative" glyph names, so the
        TrueTypeFont can be used for both glyph access (font['a']) and table
        access (font[HEAD]), to make the TrueTypeFont instance be compatible
        with both RoboFont fonts and TTFont. Assumption is that there will be
        no overlap between the table names and the glyph names, but if they do
        overlap the table prefers the glyph."""
        if name in self.TABLENAMES:
            return self._ttfont[name]
        return self._glyphs.get(name)

    def __setitem__(self, name, glyphOrTable):
        if name in self.TABLENAMES:
            self._ttfont[name] = glyphOrTable
        else:
            assert isinstance(glyphOrTable, TrueTypeGlyph)
            glyphOrTable.name = name
            self._glyphs[name] = glyphOrTable

    def newGlyph(self, glyphName):
        """Note that we take the glyphName as such here. The calling
        application should take care to translate the afiiXXXX glyphName to
        unicode glyphName."""
        if self.glyf: # If there currently is a glyf table
            if not glyphName in self.glyf:
                self.glyf[glyphName] = None
            self._glyphs[glyphName] = TrueTypeGlyph(glyphName, self.glyf[glyphName], self)
        else:
            self._glyphs[glyphName] = TrueTypeGlyph(glyphName, None, self)

    def ttkeys(self):
        if GLYF in self._ttfont:
            return self._ttfont[GLYF].keys()
        else:
            return self._glyphs.keys()

    def keys(self):
        return self._glyphs.keys()

    def keysWithUnicode(self):
        """Answers the set of glyphNames, where the glyphs has a Unicode
        value."""
        glyphNames = []
        for glyphName in self.keys():
            if self[glyphName].unicode:
                glyphNames.append(glyphName)
        return glyphNames

    def values(self):
        """Answer all glyphs in an unsorted list."""
        return self._glyphs.values()

    def getTableNames(self):
        """Answer a list of names of all (raw) tables in the TTFont."""
        return self._ttfont.keys()

    def getTable(self, tableName):
        """Answer the wrapper of the table if it exists. Answer the TTFont
        table instance instead. Answer None if the table does not exist in the TTFont."""
        if tableName in self.TABLENAMES:
            if hasattr(self, tableName):
                return getattr(self, tableName)
            return self[tableName] # Answer the raw TTFont[tableName] instead.
        return None

    def deleteTable(self, tableName):
        """Delete the table if it exists in the TTFont. Otherwise raise an error."""
        del self._ttfont[tableName]

    def __contains__(self, key):
        try:
            self._glyphs[key]  # Test if it is there
            return True
        except (KeyError, TypeError):
            return False

    def get(self, key):
        return self._glyphs.get(key)

    def __delitem__(self, glyphName):
        """Deletes the glyph named by key."""
        glyph = self._glyphs.get(glyphName)
        if glyph is None:
            # Trying to delete a glyph that no longer exists. Skip it.
            return
        # Just in the self._glyphs. All depending tables are recreated on save.
        del self._glyphs[glyphName]
        # Delete the name from the font self.glyphOrder too.
        glyphOrder = self.glyphOrder
        del glyphOrder[glyphOrder.index(glyphName)]
        self.glyphOrder = glyphOrder

    def __iter__(self):
        names = sorted(self.keys())
        while names:
            name = names[0]
            yield self[name]
            names = names[1:]

    def __contains__(self, name):
        return name in self.keys()

    # self.verbose flag of the ttFont

    def _get_verbose(self):
        return self._ttfont

    def _set_verbose(self, verbose):
        self._ttfont = verbose

    verbose = property(_get_verbose, _set_verbose)

    # self.unicodes

    def _get_unicodes(self):
        """Answers the set of Unicodes associated with the glyphNames. If the self._unicodes cache does not
        exist, build it from the reverse of self.cmap."""
        if self._unicodes is None:
            self._unicodes = us = {}
            for uniCode, glyphName in self.getCmap().items():
                if not glyphName in us:
                    us[glyphName] = set()
                us[glyphName].add(uniCode)
        return self._unicodes

    unicodes = property(_get_unicodes)

    def glyphByUnicode(self, unicodes):
        """Answers the glyph that is associated with this Unicode. The Unicode’s attribute can be either
        an integer or a list of integers. If the Unicode cannot be found in the cmap, then do a better
        search in the glyph dictionary and repair the cmap accordingly."""
        glyph = None
        if not isinstance(unicodes, (set, list, tuple)):
            unicodes = [unicodes]
        #cmap = self.getCmap() # Unused
        for unicodeValue in unicodes:
            glyph = self.get(self.getCmap().get(unicodeValue))
            if glyph is None: # Maybe it is in the font, but not in the cmap, do a better search.
                for _, g in self.glyphs.items(): # name, g
                    if g.unicode == unicodeValue:
                        glyph = g # We found it, but it's name is not in the cmap. Repair that.
                        self.getCmap()[unicodeValue] = glyph.name
                        break
            if glyph is not None:
                break
        return glyph

    # self.glyphs

    def _get_glyphs(self):
        return self._glyphs

    def _set_glyphs(self, glyphs):
        self._glyphs = glyphs

    glyphs = property(_get_glyphs, _set_glyphs)

    # self.glyphOrder

    def _get_glyphOrder(self):
        return self._ttfont.getGlyphOrder()

    def _set_glyphOrder(self, glyphOrder):
        self._ttfont.setGlyphOrder(glyphOrder)

    glyphOrder = property(_get_glyphOrder, _set_glyphOrder)

    # self.name

    def _get_name(self):
        return self._ttfont[NAME]

    name = property(_get_name)

    # self.base BASE table

    def _get_base(self):
        try:
            base = self._ttfont[BASE]
        except KeyError as e:
            print('No BASE table found.')
            return None
        return base

    def _set_base(self, base):
        self._ttfont[BASE] = base

    base = property(_get_base, _set_base)

    # self.vorg VORG table

    def _get_vorg(self):
        try:
            vorg = self._ttfont[VORG]
        except KeyError as e:
            print('No VORG table found.')
            return None
        return vorg

    def _set_vorg(self, vorg):
        self._ttfont[VORG] = vorg

    vorg = property(_get_vorg, _set_vorg)

    # self.vhea table

    def _get_vhea(self):
        try:
            vhea = self._ttfont[VHEA]
        except KeyError as e:
            print('No VHEA table found.')
            return None
        return vhea

    def _set_vhea(self, vhea):
        self._ttfont[VHEA] = vhea

    vhea = property(_get_vhea, _set_vhea)

    # self.vmtx table

    def _get_vmtx(self):
        try:
            vmtx = self._ttfont[VMTX]
        except KeyError as e:
            print('No VMTX table found.')
            return None
        return vmtx

    def _set_vmtx(self, vmtx):
        self._ttfont[VMTX] = vmtx

    vmtx = property(_get_vmtx, _set_vmtx)

    # self.gasp

    def _get_gasp(self):
        try:
            gasp = self._ttfont[GASP]
        except KeyError as e:
            print('No GASP table found.')
            return None
        return gasp

    def _set_gasp(self, gasp):
        self._ttfont[GASP] = gasp

    gasp = property(_get_gasp, _set_gasp)

    # self.glyf

    def _get_glyf(self):
        if GLYF in self._ttfont:
            return self._ttfont[GLYF]
        return None

    def _set_glyf(self, glyf):
        if GLYF in self._ttfont:
            self._ttfont[GLYF] = glyf

    glyf = property(_get_glyf, _set_glyf)

    # self.path & self.fileName

    def _get_path(self):
        return self._path

    def _set_path(self, path):
        self._path = path

    fileName = path = property(_get_path, _set_path)

    # self.fontName

    def _get_fontName(self):
        return self.path.split('/')[-1]

    fontName = property(_get_fontName)

    # self.info

    def _get_info(self):
        if self._info is None:
            self._info = State()
            extractOpenTypeInfo(self._ttfont, self)
        return self._info

    info = property(_get_info)

    # self.ttfont

    def _get_ttfont(self):
        return self._ttfont

    ttfont = property(_get_ttfont)

    # self.gpos GPOS table

    def _get_gpos(self):
        if self._gpos is None and GPOS in self._ttfont:
            self._gpos = GPOSCompiler().decompile(self._ttfont[GPOS])
        return self._gpos

    def _set_gpos(self, gpos):
        # Needs to be set to self._ttfont[GPOS] still.
        # gsub needs to be a GSUBState instance.
        self._gpos = gpos

    gpos = property(_get_gpos, _set_gpos)

    # self.gsub GSUB table

    def _get_gsub(self):
        if self._gsub is None and GSUB in self._ttfont:
            try:
                self._gsub = GSUBCompiler().decompile(self._ttfont[GSUB])
            except AttributeError as e:
                print(traceback.format_exc())
                print(self._ttfont[GSUB])
        return self._gsub

    def _set_gsub(self, gsub):
        # Needs to be set to self._ttfont[GSUB] still.
        # gsub needs to be a GSUBState instance.
        self._gsub = gsub

    gsub = property(_get_gsub, _set_gsub)

    # self.gdef GDEF table

    def _get_gdef(self):
        if self._gdef is None and GDEF in self._ttfont:
            self._gdef = GDEFCompiler().decompile(self._ttfont[GDEF])
        return self._gdef

    def _set_gdef(self, gdef):
        # Needs to be set to self._ttfont[GDEF] still.
        # gdef needs to be a GDEFState instance
        self._gdef = gdef

    gdef = property(_get_gdef, _set_gdef)

    # head

    def _get_head(self):
        try:
            return self._ttfont[HEAD]
        except KeyError:
            return None

    head = property(_get_head)

    # hhea

    def _get_hhea(self):
        try:
            return self._ttfont[HHEA]
        except KeyError as e:
            print(e)
            return None

    hhea = property(_get_hhea)

    # hmtx

    def _get_hmtx(self):
        return self._ttfont[HMTX]

    hmtx = property(_get_hmtx)

    # kern

    def _get_kern(self):
        if not KERN in self._ttfont:
            return None
        return self._ttfont[KERN]

    def _set_kern(self, kern):
        self._ttfont[KERN] = kern

    kern = property(_get_kern, _set_kern)

    # maxp

    def _get_maxp(self):
        return self._ttfont[MAXP]

    maxp = property(_get_maxp)

    # cmap

    def getCmap(self):
        # Answer the {unicode:glyphName} dictionary of cmap (assuming for now that there is only one)
        return self.cmap.tables[0].cmap

    def _get_cmap(self):
        return self._ttfont[CMAP]

    cmap = property(_get_cmap)

    # fpgmAssembly

    def _get_fpgmAssembly(self):
        return self._ttfont[FPGM].program.getAssembly()

    # def _set_fpgm(self, fpgmAssembly):
    #     self._ttfont[FPGM] = fpgmAssembly

    fpgmAssembly = property(_get_fpgmAssembly)

    # fpgm

    def _get_fpgm(self):
        return self._ttfont[FPGM]

    def _set_fpgm(self, fpgm):
        self._ttfont[FPGM] = fpgm

    fpgm = property(_get_fpgm, _set_fpgm)

    # prepAssembly

    def _get_prepAssembly(self):
        return self._ttfont[PREP].program.getAssembly()

    # def _set_prep(self, prepAssembly):
    #     self._ttfont[PREP] = prepAssembly

    prepAssembly = property(_get_prepAssembly)

        # prep

    def _get_prep(self):
        return self._ttfont[PREP]

    def _set_prep(self, prep):
        self._ttfont[PREP] = prep

    prep = property(_get_prep)

    # cvt

    def _get_cvt(self):
        try:
            table = self._ttfont[CVT]
        except KeyError as e:
            print('No CVT table found.')
            return None
        return TrueTypeCvt(self._ttfont[CVT])

    # def _set_cvt(self, cvt):
    #     self._ttfont[CVT] = cvt

    cvt = property(_get_cvt)

    # cff

    def _get_cff(self):
        try:
            return self._ttfont[CFF]
        except KeyError:
            return None

    cff = property(_get_cff)

    # post

    def _get_post(self):
        try:
            return self._ttfont[POST]
        except KeyError:
            return None

    post = property(_get_post)

    # OS/2

    def _get_os2(self):
        try:
            return self._ttfont[OS2]
        except KeyError:
            return None

    os2 = property(_get_os2)

    def TTFCompilerClass(self):
        """Allow inheriting classes from TrueTypeFont define their own
        compiler class.  E.g. to define alternative handling of certain tables,
        such as the copy of of OS/2 values in Segoe, instead of recalculating
        them."""
        return TTFCompiler

    def save(self, path=None):
        compiler = self.TTFCompilerClass()(self, path or self._path, glyphOrder=self.glyphOrder)
        compiler.compile()

    '''
    def getModelFont(self):
        # Answer the model font of this script.
        # The model font may contain the glyphs that need to go into the output.
        # It can have glyphs with names different from the source, so we may have to match on outlines.
        # If modelFont cannot be found, then answer self.
        modelFont = self._modelFont
        if modelFont is None:
            modelpath = self.path.replace('/Source', '/Model')  # scriptName is already part of the path
            if os.path.exists(modelpath):
                self._modelFont = modelFont = self.__class__(modelpath)
        # For now we always need a model. Otherwise ignore this script
        # if modelFont is None:
        #     modelFont = self
        return modelFont
    '''
