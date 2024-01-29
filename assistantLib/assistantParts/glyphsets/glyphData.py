# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   glyphData.py
#
#   GlyphData is the container for all parameters of one glyph.
#   It functions as model for what an RGlyph should contain. 
#   That's why we cannot derive the info from CurrentGlyph, etc. 
#   Assistants use this info to fill the parameters in their related RGlyph instances.
#   Values, such as width and vertical metrics, use category names instead of real values.
#   The actual values are derived from their settings in the MasterData instance for easch master.
#
# Note that names cannot start with an underscore, or else the cannot be imported by other sources.
TOP = '_top'
TOP_ = 'top'
BOTTOM = '_bottom'
BOTTOM_ = 'bottom'
RING = '_ring'
RING_ = 'ring'
OGONEK = '_ogonek'
OGONEK_ = 'ogonek'
VERT = '_vert'
VERT_ = 'vert'
DOT = '_dot'
DOT_ = 'dot'
TILDE = '_tilde'
TILDE_ = 'tilde'
TONOS = '_tonos'
TONOS_ = 'tonos'
HORN = '_horn'
HORN_ = 'horn'
MIDDLE = '_middle'
MIDDLE_ = 'middle'

CONNECTED_ANCHORS = {
    TOP: TOP_,
    BOTTOM: BOTTOM_,
    RING: RING_,
    OGONEK: OGONEK_,
    VERT: VERT_,
    DOT: DOT_,
    TILDE: TILDE_,
    TONOS: TONOS_, # Also anchor of the other -uc accents
    HORN: HORN_,
    MIDDLE: MIDDLE_,
}

# Types of mods, parts of glyph names
MOD_SUPERIOR = 'superior'
MOD_INFERIOR = 'inferior'
MOD_SINF = 'sinf'
MOD_SUPS = 'sups'
MOD_NUMR = 'numr'
MOD_DNOM = 'dnom'
MOD = 'mod'

# Categories of spacing and size
CAT_EM = 'em'
CAT_EM2 = 'em2'
CAT_CENTER = 'center'
CAT_MIN_RIGHT = 'minRight'
# Categories of width
CAT_ACCENT_WIDTH = 'accentWidth'
CAT_TAB_WIDTH = 'tabWidth'
CAT_MATH_WIDTH = 'mathWidth'
CAT_EM_WIDTH = 'emWidth'
CAT_EM2_WIDTH = 'em2Width' # Half emWidth
CAT_WORD_SPACE = 'wordSpace'
# Categories of height
CAT_XHEIGHT = 'xHeight'
CAT_CAP_HEIGHT = 'capHeight'
CAT_SC_HEIGHT = 'scHeight'
CAT_SUPS_HEIGHT = 'supsHeight' # Height of .sups, .sinf, .numr, .dnom and mod
# Categories of overshoot
CAT_OVERSHOOT = 'overshoot'
CAT_CAP_OVERSHOOT = 'capOvershoot'
CAT_SUPS_OVERSHOOT = 'supsOvershoot'
CAT_SC_OVERSHOOT = 'scOvershoot'
# Categories of baselines
CAT_BASELINE = 'baseline'
CAT_MOD_BASELINE = 'modBaseline'
CAT_NUMR_BASELINE = 'numrBaseline'
CAT_SINF_BASELINE = 'sinfBaseline'
CAT_SUPS_BASELINE = 'supsBaseline'
CAT_DNOM_BASELINE = 'dnomBaseline'

# Allowed category names
CAT_OVERSHOOTS = (None, CAT_OVERSHOOT, CAT_CAP_OVERSHOOT, CAT_SUPS_OVERSHOOT, CAT_SC_OVERSHOOT)
CAT_BASELINES = (None, CAT_BASELINE, CAT_MOD_BASELINE, CAT_NUMR_BASELINE, CAT_SINF_BASELINE, CAT_SUPS_BASELINE, CAT_DNOM_BASELINE)
CAT_HEIGHTS = (None, CAT_XHEIGHT, CAT_CAP_HEIGHT, CAT_SC_HEIGHT, CAT_SUPS_HEIGHT)
CAT_WIDTHS = (None, CAT_ACCENT_WIDTH, CAT_TAB_WIDTH, CAT_MATH_WIDTH, CAT_EM_WIDTH, CAT_EM2_WIDTH, CAT_WORD_SPACE)

class GlyphData:
    """Glyph data element that contains all individual data for glyphs.

    >>> gd = GlyphData(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', comment='A Uppercase Alphabet, Latin', gid=35)
    >>> gd
    <GlyphData A>
    >>> gd.uni
    65
    """    
    def __init__(self, uni=None, c=None, gid=None, name=None, srcName=None, hex=None, composites=None,
            unicodes=None, 
            # Define component reference glyph names.
            base=None, accents=None, 
            comment=None, spacing=None, fixAccents=True,
            fixSpacing=True, fixAnchors=False, rightMin=None, top_y=None, blackVersion=1, 
            # Anchors
            anchors=None, # Force list of anchor names
            anchorSrc=None, # Glyph name to copy anchors from
            # Force spacing dependencies
            l=None, r=None, w=None, il=None, ir=None, iw=None, ml=None, mr=None, 
            l2r=None, r2l=None, il2r=None, ir2l=None, 
            # Type of glyph. Guess if undefined as None.
            isLower=None, isMod=None, isSc=None,
            # Italicize
            useSkewRotate=False, addItalicExtremePoints=False, 
            # Glyphs to copy from, initially before editing starts
            src=None, # Not used here
            src180=None, # Not used here
            g1=None, g2=None, 
            ascender=None, descender=None, 
            # # In case hard value needs to overwrite category value
            overshoot=None, height=None, baseline=None, width=None,
            # Categories of vertical metrics, if not None they overwrite the master-wide guessed value by parent MasterData
            catOvershoot=None, catHeight=None, catBaseline=None, catWidth=None, 
            ): 
        self.parent = None # 
        self.uni = uni
        self.unicodes = unicodes
        if c is None and uni:
            c = chr(uni)
        self.c = c
        if uni is not None:
            uniHex = '%04x' % uni
            if hex is not None:
                hex = hex.lower()
                assert hex == uniHex, (hex, uniHex)
            hex = uniHex
        self.hex = hex
        self.gid = gid # Glyph id
        assert name is not None
        self.name = name
        if srcName == name:
            srcName = None
        self.srcName = srcName
        
        self._isLower = isLower # If not None, force the flag. Otherwise try to guess.
        self._isSc = isSc # Is smallcap
        self._isMod = isMod # Glyph is a modifier.

        self.base = base # Base component if used
        self.accents = accents or [] # List of other component names, besides the base
        self.comment = comment or ''
        self.spacing = spacing # Obsolete?

        self.fixAccents = fixAccents
        self.fixAnchors = fixAnchors
        self.fixSpacing = fixSpacing
        self.rightMin = rightMin

        self.g1 = g1 or self.name # Name of group 1, right of glyph, left of kerning pair
        self.g2 = g2 or self.name # Name of group 2, left of glyph, right of kerning pair

        self.useSkewRotate = useSkewRotate
        self.addItalicExtremePoints = addItalicExtremePoints

        self.overshoot = overshoot # In case hard value needs to overwrite category value of self.catOvershoot
        self.height = height # In case hard value needs to overwrite category value of self.catHeight
        self.baseline = baseline # In case hard value needs to overwrite category value of self.catBaseline
        self.width = width # In case hard value needs to overwrite category value of self.catHeight

        # Categories of vertical metrics, if not None they overwrite the master-wide guessed value by parent MasterData
        assert catOvershoot in CAT_OVERSHOOTS
        assert catHeight in CAT_HEIGHTS
        assert catBaseline in CAT_BASELINES
        assert catWidth in CAT_WIDTHS

        self.catOvershoot = catOvershoot
        self.catHeight = catHeight 
        self.catBaseline = catBaseline 
        self.catWidth = catWidth 

    def __repr__(self):
        return(f'<{self.__class__.__name__} {self.name}>')

    def _get_isUpper(self):
        return not self.isLower
    isUpper = property(_get_isUpper)

    def _get_isLower(self):
        """Answer the boolean flag if this glyph is lowercase. If the flag is undefined in self._isLower
        then take a guess.
        """
        if self._isLower is not None:
            return self._isLower
        return bool(self.name[0].upper() != self.name[0]) # This is an uppercase.
    isLower = property(_get_isLower)

    def _get_isMod(self):
        """Answer the boolean flag if this glyph is a modifier. If the flag is undefined in self._isMod
        then take a guess.
        """
        if self._isMod is not None:
            return self._isMod
        return self.name.endswith(MOD)
    isMod = property(_get_isMod)

    def _get_isSups(self):
        return self.name.endswith(MOD_SUPS)
    isSups = property(_get_isSups)
            
    def _get_isSinf(self):
        return self.name.endswith(MOD_SINF)
    isSinf = property(_get_isSinf)
            
    def _get_isNumr(self):
        return self.name.endswith(MOD_NUMR)
    isNumr = property(_get_isNumr)
            
    def _get_isDnom(self):
        return self.name.endswith(MOD_DNOM)
    isDnom = property(_get_isDnom)
            
    def _get_isSc(self):
        """Answer the boolean flag if this glyph is a smallcap. If the flag is undefined in self._isSc
        then take a guess.
        """
        if self._isSc is not None:
            return self._isSc
        for ext in ('.sc', 'small'):
            if self.name.endswith(ext):
                return True
        return False
    isSc = property(_get_isSc)
        
    '''
        self.top_y = top_y
        self.blackVersion = blackVersion # Default (1) Latin. 
        if isLower is None: # Undefined, try to guess
            isLower = bool(name[0].upper() != name[0]) # This is an uppercase.
        self.isLower = isLower # Use this flag to guess the right guide positions
        if height is None:
            if 'inferior' in name:
                height = SINF_HEIGHT 
            elif name.endswith('mod') or 'mod-' in name:
                height = MOD_HEIGHT
            elif 'small' in name:
                height = XHEIGHT
            elif isLower:
                height = XHEIGHT
            else:
                height = CAP_HEIGHT
        if overshoot is None:
            if 'inferior' in name:
                overshoot = SINF_OVERSHOOT
            elif name.endswith('mod') or 'mod-' in name:
                overshoot = MOD_OVERSHOOT
            elif isLower:
                overshoot = CAP_OVERSHOOT
            else:
                overshoot = OVERSHOOT
        if ascender is None:
            if 'inferior' in name:
                ascender = SINF_ASCENDER
            elif name.endswith('mod') or 'mod-' in name:
                ascender = MOD_ASCENDER
        if descender is None:
            if 'inferior' in name:
                descender = SINF_DESCENDER
            elif name.endswith('mod') or 'mod-' in name:
                descender = MOD_DESCENDER
        if baseline is None:
            if 'inferior' in name:
                baseline = SINF_BASELINE
            elif name.endswith('mod') or 'mod-' in name:
                baseline = MOD_BASELINE
        # These are label names of vertical metrics, not values
        self.height = height 
        self.ascender = ascender or ASCENDER
        self.descender = descender or DESCENDER
        self.baseline = baseline or BASELINE
        self.overshoot = overshoot
        # Composites
        if composites is None:
            composites = set()
        self.composites = composites
        self.anchors = set(anchors or []) 
        self.anchorSrc = anchorSrc # Optional name of the glyph to copy anchor positions from.
        self.src = src # Not used here
        self.src180 = src180 # Not used here

        self.hasErrors = False

        # Spacing sources
        self.l = l 
        self.r = r
        self._w = w
        self.il = il
        self.ir = ir
        self.iw = iw
        self.ml = ml
        self.mr = mr
        self.l2r = l2r
        self.r2l = r2l
        self.il2r = il2r
        self.ir2l = ir2l

    def _set_w(self, w):
        self._w = w
        ss = ff
    def _get_w(self):
        return self._w
    w = property(_get_w, _set_w)

    def _get_fixedLeft(self):
        return bool(self.l or self.il or self.ml or self.r2l or self.ir2l)
    fixedLeft = property(_get_fixedLeft)
    
    def _get_fixedRight(self):
        return bool(self.r or self.ir or self.mr or self.l2r or self.il2r or self.w)
    fixedRight = property(_get_fixedRight)
    
    def _get_leftSpaceSource(self):
        return self.l or self.il or self.ml or self.r2l or self.ir2l or None
    leftSpaceSource = property(_get_leftSpaceSource)
    
    def _get_rightSpaceSource(self):
        return self.r or self.ir or self.mr or self.l2r or self.il2r or self.w or None
    rightSpaceSource = property(_get_rightSpaceSource)
    
    def _get_leftSpaceSourceLabel(self):
        """Answer the string where this space gets from. Answer None if there is non source."""
        if self.l:
            return 'Left %s' % self.l
        if self.il:
            return 'iLeft %s' % self.il
        if self.ml:
            return 'mLeft %s' % self.ml
        if self.r2l:
            return 'R-->L %s' % self.r2l
        if self.ir2l:
            return 'iR-->L %s' % self.ir2l
        return None
    leftSpaceSourceLabel = property(_get_leftSpaceSourceLabel)
        
    def _get_rightSpaceSourceLabel(self):
        """Answer the string where this space gets from. Answer None if there is non source."""
        if self.r:
            return 'Right %s' % self.r
        if self.ir:
            return 'iLeft %s' % self.ir
        if self.mr:
            return 'mLeft %s' % self.mr
        if self.l2r:
            return 'L-->R %s' % self.l2r
        if self.il2r:
            return 'iL-->R %s' % self.il2r
        if self.w:
            return 'W %s' % self.w
        return None
    rightSpaceSourceLabel = property(_get_rightSpaceSourceLabel)
  
    # Fix to fill the base and accent parameters into the GLYPH_DATA, as derived from the standard master Text Regualar
    USED_COMPONENTS = {'dagger': [], 'umod': [], 'lmiddlering': [], 'rumrotunda': [], 'U': [], 'eacute': ['e', 'acute'], 'Ohorndotbelow': ['Ohorn', 'dotbelowcomb'], 'ebarred': [], 'ringhalfleft': [], 'eshsquatreversed': [], 'uni2580': [], 'Alphaoxia': ['A', 'oxia-uc'], 'Aturned': [], 'Odieresis-cy': ['O', 'dieresis'], 'dialytikaoxia': [], 'leftArrow': [], 'Hori-coptic': [], 'Acircumflexhookabove': ['A', 'hookabovecomb.component'], 'hundredthousandssigncomb-cy': [], 'ringhalfleftbelowcomb': ['ringhalfleft'], 'einferior': ['emod'], 'upsilonpsilioxia': ['upsilon', 'psilioxia'], 'Tlinebelow': ['T', 'macronbelow'], 'OeVolapuk': [], 'alphatonos': ['alpha', 'tonos'], 'one.numr': [], 'BbarredSmall': [], 'ydotbelow': ['y', 'dotbelowcomb'], 'omegadasiaperispomeni': ['omega', 'dasiaperispomeni'], 'k': [], 'uni20E3': [], 'uni2563': [], 'cruzeiro': [], 'dong': [], 'alphamod-latin': [], 'olowringinside': [], 'seagullbelowcomb': [], 'Tmod': [], 'twofifths': ['two.numr', 'fraction', 'five.dnom'], 'Etapsilivariaprosgegrammeni': ['H', 'psilivaria-uc', 'prosgegrammeni'], 'Etapsilioxia': ['H', 'psilioxia-uc'], 'hturnedfishhookandtail': [], 'righttoleftoverride': [], 'Nlongrightleg': [], 'tpalatalhookmod': [], 'Wgrave': ['W', 'grave'], 'psilivaria': [], 'Yi-cy': ['I', 'dieresis'], 'eopenreversedclosed': [], 'Uring': ['U', 'ring'], 'icircumflex': ['idotless', 'circumflex'], 'Acircumflex': ['A', 'circumflex'], 'tonefive': [], 'whiteBullet': [], 'Egrave': ['E', 'grave'], 'zretroflexhookmod': [], 'tturned': [], 'downArrow': [], 'Adblgrave': ['A', 'dblgravecomb'], 'ou': [], 'longs': [], 'K': [], 'rfishhookreversed': [], 'whook': [], 'millionssigncomb-cy': [], 'mSidewaysTurned': [], 'dieresistonos': [], 'Chi-latin': ['X'], 'lsinvertedlazy': [], 'uni047C': [], 'E-cy': [], 'Palochka-cy': ['I'], 'Cstroke': ['C', 'Astroke.component'], 'hookabovecomb': [], 'AEsmall': [], 'five.blackCircled': [], 'acutebelowcomb': ['acute'], 'shha-cy': ['h'], 'bridgeinvertedbelowcomb': ['shelfmod'], 'Wacute': ['W', 'acute'], 'Gangia-coptic': [], 'Semisoftsign-cy': [], 'Umod': [], 'ii-cy': [], 'Ge-cy': ['Gamma'], 'uhookabove': ['u', 'hookabovecomb'], 'oneseventh': ['one.numr', 'fraction', 'seven.numr'], 'three.pnum_enclosingkeycapcomb': [], 'nonbreakinghyphen': ['hyphen'], 'iishorttail-cy': ['iishort-cy', 'tail.component'], 'uni2514': [], 'periodcentered': [], 'Archaicsampi': [], 'fourinferior': ['four.numr'], 'onefifth': ['one.numr', 'fraction', 'five.dnom'], 'ruble': [], 'Kdescender': [], 'Lcommaaccent': ['L', 'cedillacomb.component'], 'Ndotaccent': ['N', 'dotaccent'], 'Omegadasiaperispomeniprosgegrammeni': ['Ohm', 'dasiaperispomeni-uc', 'prosgegrammeni'], 'be-cy': [], 'Esdescender-cy': [], 'Nobliquestroke': ['N'], 'minute': [], 'uni2567': [], 'Udotbelow': ['U', 'dotbelowcomb'], 'palatalizationcomb-cy': [], 'gsingle': ['g'], 'zacute': ['z', 'acute'], 'lozenge': [], 'Phi': [], 'Hwair': [], 'SigmaLunateDottedReversedSymbol': ['SigmaLunateReversedSymbol', 'dotmiddle.component'], 'hturnedfishhook': [], 'uni2569': [], 'edblgrave': ['e', 'dblgravecomb'], 'kobliquestroke': ['k'], 'ocircumflexdotbelow': ['o', 'circumflex', 'dotbelowcomb'], 'olongstroke': [], 'Es-cy': ['C'], 'zigzagabovecomb': [], 'tonos': [], 'sha-cy': [], 'rcommaaccent': ['r', 'cedillacomb.component'], 'acutedottedcomb': [], 'Ohornhookabove': ['Ohorn', 'hookabovecomb'], 'vsubscript': ['vmod'], 'Alphadasiaprosgegrammeni': ['A', 'dasia-uc', 'prosgegrammeni'], 'Etaprosgegrammeni': ['H', 'prosgegrammeni'], 'strokelongcomb': ['overline'], 'Is': [], 'lbar': [], 'O-cy': ['O'], 'ghemiddlehook-cy': [], 'rdotaccent': ['r', 'dotaccent'], 'ucaron': ['u', 'caron'], 'Oinvertedbreve': ['O', 'perispomeni'], 'commaabovecomb': ['koronis'], 'five.numr': [], 'chi-latin': ['chi'], 'DZcaron': ['D', 'Z', 'caron'], 'Chedescender-cy': [], 'Ddotaccent': ['D', 'dotaccent'], 'wcircumflex': ['w', 'circumflex'], 'arrowheadupmod': [], 'Agrave': ['A', 'grave'], 'ecircumflextilde': ['e', 'tildecomb.component'], 'Zhe-cy': [], 'downtackmod': [], 'etatonos': ['eta', 'tonos'], 'Fdotaccent': ['F', 'dotaccent'], 'RreversedSmall': [], 'ecircumflexhookabove': ['e', 'hookabovecomb.component'], 'Pdotaccent': ['P', 'dotaccent'], 'Ecircumflexbelow': ['E', 'circumflexbelow'], 'colontriangularmod': [], 'Germandbls': [], 'equivalence': [], 'Nu': ['N'], 'Psi': [], 'Sswashtail': [], 'oSidewaysOpen': [], 'Cuatrillo': [], 'circumflex': [], 'Idotbelow': ['I', 'dotbelowcomb'], 'aeacute': ['ae', 'acute'], 'chilowrightring': [], 'dpalatalhook': ['d', 'dpalatalhook.component'], 'kaverticalstroke-cy': [], 'rmod': [], 'four.tnum': [], 'acutecomb.component1': [], 'Imod': [], 'etadasiaperispomeni': ['eta', 'dasiaperispomeni'], 'seven.pnum_enclosingkeycapcomb': [], 'Mmod': [], 'utildebelow': ['u', 'tildebelow'], 'Zedieresis-cy': ['Ze-cy', 'dieresis'], 'Rtail': [], 'nine.numr': [], 'ay': [], 'Kabashkir-cy': [], 'uni2559': [], 'schwaretroflexhook': ['schwa', 'aretroflexhook.component', 'gpalatalhook.component'], 'heartBlackSuit': [], 'yot': ['j'], 'Iotaafrican': [], 'rmiddletilde': ['r'], 'arrowheadrightbelowcomb': ['lowrightarrowheadmod'], 'circumflexcomb': [], 'dialytikatonoscomb': ['dialytikaoxia'], 'overlinecomb': ['overline'], 'hturned': [], 'minus.component': [], 'Klinebelow': ['K', 'macronbelow'], 'ereversed-cy': [], 'Rstroke': ['R'], 'zedieresis-cy': ['ze-cy', 'dieresis'], 'Et': [], 'palochka-cy': ['l'], 'Heng': [], 'Aring': [], 'gravecomb.component': [], 'kaiSymbol': [], 'one.tnum': [], 'oneinferior': ['one.numr'], 'Abrevetilde': ['A', 'Abreve.component3'], 'ldotbelow': ['l', 'dotbelowcomb'], 'alef-egyptological': [], 'dieresiscomb': ['dieresis'], 'psilioxia': [], 'ezhretroflexhook': [], 'parenleftinferior': ['parenleft.component'], 'two.tnum': [], 'vrighthook': ['izhitsa-cy'], 'upsilondialytikaperispomeni': ['upsilon', 'dialytikaperispomeni'], 'three.dnom': ['three.numr'], 'E': [], 'Imacron-cy': ['Ii-cy', 'macron'], 'zdotbelow': ['z', 'dotbelowcomb'], 'hdotaccent': ['h', 'dotmiddle.component'], 'vy': [], 'Emod': [], 'idieresisacute': ['idotless', 'idieresis.component'], 'registered': [], 'epsilonvaria': ['epsilon', 'varia'], 'Abreve-cy': ['A', 'brevecomb.component'], 'Ocenteredtilde': [], 'rumsmall': ['Rsmall'], 'Etapsili': ['H', 'psili-uc'], 'downtackbelowcomb': ['downtackmod'], 'longsdiagonalstroke': [], 'four': [], 'ucircumflexbelow': ['u', 'circumflexbelow'], 'upsilon-latin': [], 'zmod': [], 'tum': [], 'Vend': [], 'dbllowlinecomb': ['underscoredbl'], 'plusinferior': ['plus.component'], 'ccomb': [], 'OEsmall': [], 'ubarshortrightleg': [], 'pmiddletilde': ['p'], 'C': [], 'Iotapsili': ['I', 'psili-uc'], 'Je-cy': ['J'], 'ringbelow': [], 'sixperemspace': [], 'Wynn': [], 'arrowheadrightmod': [], 'finsular': [], 'uni047E.component': [], 'zpalatalhook': ['z', 'dpalatalhook.component'], 'macrongravecomb': ['firsttonechinese', 'grave'], 'Iu-cy': [], 'idblgrave': ['idotless', 'dblgravecomb'], 'lefthalfringabovecomb': [], 'three': [], 'upsilondialytikaoxia': ['upsilon', 'dialytikaoxia'], 'San': [], 'ustrait-cy': [], 'rstroke': ['r'], 'etapsiliperispomeni': ['eta', 'psiliperispomeni'], 'Idieresis': ['I', 'dieresis'], 'omegapsilioxia': ['omega', 'psilioxia'], 'quoteright': [], 'yhookabove': ['y', 'hookabovecomb'], 'Dz': ['D', 'z'], 'Yerudieresis-cy': ['Yeru-cy', 'dieresis'], 'O': [], 'alphaturnedmod-latin': [], 'clickalveolar': [], 'brokenbar': [], 'Hcedilla': ['H', 'cedilla'], 'Gje-cy': ['Gamma', 'acute'], 'ef-cy': [], 'abrevehookabove': ['a', 'abreve.component2'], 'Epsilondasiavaria': ['E', 'dasiavaria-uc'], 'Hcircumflex': ['H', 'circumflex'], 'delta-latin': ['delta'], 'ncaron': ['n', 'caron'], 'Y': [], 'Epsilonvaria': ['E', 'varia-uc'], 'uni2320': [], 'uhorntilde': ['uhorn', 'tilde'], 'vhook': [], 'uni2500': [], 'spadeBlackSuit': [], 'Ohookabove': ['O', 'hookabovecomb'], 'Glottalstop': [], 'Enghe-cy': [], 'Abreve.component3': [], 'istrokemod': [], 'Fita-cy': [], 'Abrevehookabove': ['A', 'Abreve.component2'], 'Bdotaccent': ['B', 'dotaccent'], 'Dinsular': [], 'braceright': [], 'Etapsiliperispomeniprosgegrammeni': ['H', 'psiliperispomeni-uc', 'prosgegrammeni'], 'seven.tnum': [], 'uni266b': [], 'tildeoverlaycomb': ['tilde'], 'Gstroke': [], 'uni047E': ['Omega-cy', 'uni047E.component'], 'entail-cy': ['en-cy', 'tail.component'], 'alphainverted-latin': [], 'Chi': ['X'], 'bhook': [], 'ppalatalhook': ['p', 'bpalatalhook.component'], 'bracketright': [], 'upsilon': [], 'tonetwo': [], 'Ao': [], 'whiteSquare': [], 'Ncircumflexbelow': ['N', 'circumflexbelow'], 'dieresis': [], 'otildemacron': ['o', 'otilde.component1'], 'turnedrtail': [], 'udieresisSideways': [], 'oeturnedstroke': [], 'tcomb': [], 'jcaron': ['jdotless', 'caron'], 'vhookmod': [], 'upsilonvrachy': ['upsilon', 'brevecomb'], 'uni252c': [], 'Amacron': ['A', 'macron'], 'yturned': [], 'epsilon': [], 'twothirds': ['two.numr', 'fraction', 'three.dnom'], 'omega-cy': [], 'blackSquare': [], 'Te-cy': ['T'], 'AVhorizontalbar': [], 'Lcaron': ['L', 'caronvert.component'], 'Gdotaccent': ['G', 'dotaccent'], 'acaron': ['a', 'caron'], 'ohorntilde': ['ohorn', 'tilde'], 'Mscript': [], 'sigmaLunateReversedSymbol': ['oopen'], 'Kadescender-cy': [], 'a-cy': ['a'], 'ringhalfrightbelowcomb': ['ringhalfright'], 'uniAB60': [], 'zeta': [], 'BBarredmod': [], 'hhookmod': [], 'uptackmod': [], 'Oi': [], 'hyphen': [], 'clickretroflex': ['exclam'], 'dzaltone': [], 'nlinebelow': ['n', 'macronbelow'], 'varia': [], 'Rsmallinvertedmod': [], 'dieresisbelow': [], 'dje-cy': [], 'arrowheadleftbelowcomb': ['lowleftarrowheadmod'], 'cheverticalstroke-cy': ['che-cy'], 'dotaccentcomb': ['dotaccent'], 'seven': [], 'Zhebreve-cy': ['Zhe-cy', 'brevecomb.component'], 'shcha-cy': [], 'Kacute': ['K', 'acute'], 'omegapsilivaria': ['omega', 'psilivaria'], 'fiveeighths': ['five.numr', 'fraction', 'eight.numr'], 'rstirrup': [], 'udieresisbelow': ['u', 'dieresisbelow'], 'mdotaccent': ['m', 'dotaccent'], 'Omacrongrave': ['O', 'gravecomb.component1'], 'fourfifths': ['four.numr', 'fraction', 'five.dnom'], 'fraction': [], 'y': [], 'Btopbar': [], 'iota-latin': [], 'de-cy': [], 'gravelowmod': ['grave'], 'vcurl': [], 'ordfeminine': [], 'iogonek': ['i', 'ogonek'], 'agrave': ['a', 'grave'], 'h': [], 'I': [], 'uni263c': [], 'uretroflexhook': ['u'], 'Kdotbelow': ['K', 'dotbelowcomb'], 'Edotaccent': ['E', 'dotaccent'], 'mcomb': [], 'alphadasiavaria': ['alpha', 'dasiavaria'], 'ohungarumlaut': ['o', 'hungarumlaut'], 'Alpha': ['A'], 'Estroke': ['E', 'slashlongcomb'], 'Ibreve': ['I', 'breve'], 'zswashtail': [], 'degree': [], 'Epsilon': ['E'], 'apostrophemod': ['quoteright'], 'oopenretroflexhook': ['oopen', 'aretroflexhook.component'], 'abreve.component2': [], 'cPalatalhook': ['c'], 'ezhcaron': ['ezh', 'caron'], 'upsilondasiavaria': ['upsilon', 'dasiavaria'], 'npalatalhook': ['n', 'dpalatalhook.component'], 'Ldot': ['L', 'dotmiddle.component'], 'dze-cy': ['s'], 'ae': [], 'zerowidthnonjoiner': [], 'Creverseddot': ['SigmaLunateDottedReversedSymbol'], 'zeroinferior': ['zero.numr'], 'Jcrossedtail': [], 'imacron': ['idotless', 'macron'], 'rcrossedtail': [], 'kcommaaccent': ['k', 'cedillacomb.component'], 'threeinferior': ['three.numr'], 'quotedblright': [], 'vmod': [], 'nordicMark': [], 'alphabarred': [], 'cstroke': ['c'], 'Sampi': [], 'Tau': ['T'], 'schwadieresis-cy': ['eturned', 'dieresis'], 'phi-latin': [], 'period': [], 'five.dnom': ['five.numr'], 'chedescender-cy': [], 'uniFB03': [], 'vend': [], 'gbridgeabovecomb': [], 'idotless': [], 'Asmall': [], 'Rdotbelowmacron': ['R', 'macron', 'dotbelowcomb'], 'Uhookabove': ['U', 'hookabovecomb'], 'bracketleft': [], 'Omegatonos': ['Ohm', 'tonos-uc'], 'parenleft': [], 'Shei-coptic': [], 'Alphatonos': ['A', 'tonos-uc'], 'alphapsili': ['alpha', 'psili'], 'Ismallmod': [], 'bilabialclick': [], 'delta': [], 'rturnedmod': [], 'seven.numr': [], 'Iotapsilivaria': ['I', 'psilivaria-uc'], 'candrabinducomb': ['breve', 'dotaccent'], 'BFlourish': [], 'equalsuperior': ['equal.component'], 'Tcaron': ['T', 'caron'], 'Rlinebelow': ['R', 'macronbelow'], 'qpdigraph': [], 'vturned': [], 'grave': [], 'pinferior': ['pmod'], 'kappa': [], 'ebreve': ['e', 'breve'], 'Etatonos': ['H', 'tonos-uc'], 'Ntilde': ['N', 'tilde'], 'Hadescender-cy': [], 'abreve': ['a', 'breve'], 'sigmaLunateDottedReversedSymbol': ['oopen', 'dotmiddle.component'], 'alphapsiliperispomeniypogegrammeni': ['alpha', 'psiliperispomeni', 'prosgegrammeni'], 'mum': ['m'], 'zcaron': ['z', 'caron'], 'titlocomb-cy': [], 'Ocaron': ['O', 'caron'], 'Thornstroke': ['Thorn'], 'righthalfringabovecomb': [], 'gestrokehook-cy': ['ghestroke-cy', 'Gestrokehook-cy.component'], 'uogonek': ['u', 'ogonek'], 'lefttorightoverride': [], 'uni256c': [], 'uni21a8': ['uni2195', 'macronbelow'], 'minusbelowcomb': ['minusmod'], 'Omicronpsili': ['O', 'psili-uc'], 'Scommaaccent': ['S', 'cedillacomb.component'], 'ddotaccent': ['d', 'dotaccent'], 'uni2518': [], 'dzhe-cy': [], 'lbroken': [], 'dhook': [], 'minusmod': [], 'Ecedilla': ['E', 'cedilla'], 'six.tnum': [], 'Xi': [], 'Ycircumflex': ['Y', 'circumflex'], 'ldoublebar': [], 'Hardsign-cy': [], 'Ezhcaron': ['Ezh', 'caron'], 'rdotbelowmacron': ['r', 'macron', 'dotbelowcomb'], 'adotaccent': ['a', 'dotaccent'], 'partialdiff': [], 'lmiddletilde': [], 'Uhungarumlaut-cy': ['U-cy', 'hungarumlaut'], 'oslashSideways': ['oSideways'], 'zhedescender-cy': [], 'oinvertedbreve': ['o', 'perispomeni'], 'f': [], 'radical': [], 'uni2556': [], 'verticallinelowmod': ['verticallinemod'], 'mhook': [], 'ts': [], 'Fepigraphicreversed': [], 'A': [], 'Utildebelow': ['U', 'tildebelow'], 'Ismall': [], 'gcommaaccent': ['g'], 'integral': [], 'alphaoxiaypogegrammeni': ['alpha', 'oxia', 'prosgegrammeni'], 'bidentalpercussive': [], 'Tcircumflexbelow': ['T', 'circumflexbelow'], 'Gsmallhook': [], 'Schwa-cy': ['Schwa'], 'Acircumflextilde': ['A', 'tildecomb.component'], 'ringcomb': [], 'dcedilla': ['d', 'cedillacomb.component1'], 'Dtopbar': [], 'hengmod': [], 'uni047F': ['omega-cy', 'uni047E.component'], 'six.blackCircled': [], 'glottalstopreversed': [], 'kje-cy': ['kgreenlandic', 'acute'], 'rfishhook': [], 'shelfmod': [], 'quotedblleft': [], 'ue': [], 'Alphavrachy': ['A', 'breve'], 'hcircumflex': ['h', 'circumflex'], 'uni2568': [], 'Ydotbelow': ['Y', 'dotbelowcomb'], 'ampersand': [], 'Ecircumflextilde': ['E', 'tildecomb.component'], 'oslashacute': ['oslash', 'acute'], 'perispomenicomb': ['tilde'], 'hungarumlautcomb': [], 'tdotaccent': ['t', 'dotaccent'], 'narrownbspace': [], 'rhotichookmod': [], 'udotbelow': ['u', 'dotbelowcomb'], 'Iishort-cy': ['Ii-cy', 'brevecomb.component'], 'ccurl': [], 'onequarter': ['one.numr', 'fraction', 'four.numr'], 'raisedcolonmod': ['colon'], 'ezhmod': [], 'Etapsilivaria': ['H', 'psilivaria-uc'], 'ksi-cy': [], 'Qhooktail': [], 'kstrokediagonalstroke': ['k'], 'Alphapsiliperispomeniprosgegrammeni': ['A', 'psiliperispomeni-uc', 'prosgegrammeni'], 'uni2642': [], 'Thook': [], 'eshreversedloop': [], 'glottalstop': [], 'oTophalf': [], 'Rdotaccent': ['R', 'dotaccent'], 'Ysmall': [], 'xcomb': [], 'eight': [], 'istroke': [], 'upsilonvaria': ['upsilon', 'varia'], 'iinvertedbreve': ['idotless', 'breveinvertedcomb'], 'omegadasiavaria': ['omega', 'dasiavaria'], 'Cuatrillocomma': [], 'Otildeacute': ['O', 'acutecomb.component3'], 'eshmod': [], 'strokeshortcomb': [], 'Yusbigiotified-cy': [], 'dasiaperispomeni': [], 'tshe-cy': [], 'bstroke': [], 'oBottomhalfmod': [], 'uni2552': [], 'otilde.component1': [], 'Omegaprosgegrammeni': ['Ohm', 'prosgegrammeni'], 'Ohornacute': ['Ohorn', 'acute'], 'Omega-latin': [], 'quotesinglbase': [], 'Omegadasiaoxiaprosgegrammeni': ['Ohm', 'dasiaoxia-uc', 'prosgegrammeni'], 'alphapsiliperispomeni': ['alpha', 'psiliperispomeni'], 'chilowleftserif': [], 'lowringmod': ['ring'], 'Lbar': ['L', 'firsttonechinese'], 'shortequalmod': [], 'upsilondasiaoxia': ['upsilon', 'dasiaoxia'], 'scommaaccent': ['s', 'cedillacomb.component'], 'uniFB00': [], 'rupee': [], 'almostequaltoabovecomb': [], 'greaterequal': [], 'uni2553': [], 'Obreve': ['O', 'breve'], 'section': [], 'Entail-cy': ['H', 'tail.component'], 'cuatrillocomma': [], 'four.pnum_enclosingkeycapcomb': [], 'micro': [], 'Ecedillabreve': ['E', 'cedilla', 'breve'], 'AEModifier': [], 'Odieresismacron': ['O', 'macroncomb.component'], 'careof': [], 'dottedCircle': [], 'Dzeabkhasian-cy': [], 'onefraction': ['one.numr', 'fraction'], 'sampi': [], 'Kstroke': ['K'], 'abrevedotbelow': ['a', 'breve', 'dotbelowcomb'], 'leftangleabovecomb': [], 'fermatacomb': [], 'Rinvertedbreve': ['R', 'perispomeni'], 'ghook': [], 'Upsilondieresis': ['Y', 'dieresis'], 'iotaoxia': ['iota', 'oxia'], 'rhook': [], 'ncommaaccent': ['n', 'cedillacomb.component'], 'Igrave': ['I', 'grave'], 'Zvisigothic': [], 'hahook-cy': [], 'Oacute': ['O', 'acute'], 'Ihookabove': ['I', 'hookabovecomb'], 'Omegapsilioxiaprosgegrammeni': ['Ohm', 'psilioxia-uc', 'prosgegrammeni'], 'yen': [], 'lcaron': ['l', 'caronvert.component'], 'IstrokeSmallmod': [], 'quotedblrightreversed': [], 'uinvertedbreve': ['u', 'perispomeni'], 'Ccircumflex': ['C', 'circumflex'], 'Ecircumflexacute': ['E', 'acutecomb.component'], 'ogonekcomb': ['ogonek'], 'ymod': [], 'nineinferior': ['nine.numr'], 'Jsmall': [], 'aktieselskab': [], 'R': [], 'o': [], 'uhorn': [], 'Sha-cy': [], 'parenleft.component': [], 'Qstrokethroughdescender': ['Q'], 'udieresisacute': ['u', 'acutecomb.component5'], 'gheupturn-cy': [], 'yeru-cy': [], 'rinvertedbreve': ['r', 'perispomeni'], 'zero.dnom': ['zero.numr'], 'tmiddletilde': ['t'], 'Gheupturn-cy': [], 'sinferior': ['smod'], 'fturned': [], 'hryvnia': [], 'commaaccentcomb': [], 'Eng': [], 'lowlinecomb': ['underscore'], 'obarred-cy': [], 'Eltail-cy': ['El-cy', 'tail.component'], 'kdescender': [], 'Etadasiavariaprosgegrammeni': ['H', 'dasiavaria-uc', 'prosgegrammeni'], 'Z': [], 'Gestrokehook-cy.component': [], 'ha-cy': ['x'], 'anoteleia': [], 'con': [], 'mhookmod': [], 'paragraphseparator': [], 'racute': ['r', 'acute'], 'Ndescender': ['N'], 'Imacron': ['I', 'macron'], 'Msmall': ['em-cy'], 'dblmacronbelowcomb': ['macronbelowcomb', 'macronbelowcomb'], 'tesh': [], 'eightsuperior': ['eight.numr'], 'Udieresis': ['U', 'dieresis'], 'etaperispomeniypogegrammeni': ['eta', 'perispomeni', 'prosgegrammeni'], 'chedescenderabkhasian-cy.component': [], 'franc': [], 'fivesuperior': ['five.numr'], 'abrevegrave': ['a', 'abreve.component1'], 'onethird': ['one.numr', 'fraction', 'three.numr'], 'qhook': [], 'exclamdouble': ['exclam', 'exclam'], 'uni2588': [], 'Vdotbelow': ['V', 'dotbelowcomb'], 'Ginsular': [], 'wacute': ['w', 'acute'], 'Chedescenderabkhasian-cy.component': [], 'OU': [], 'De-cy': [], 'aa': [], 'Dafrican': ['Eth'], 'Zeta': ['Z'], 'Odotaccent': ['O', 'dotaccent'], 'eta': [], 'Abrevedotbelow': ['A', 'breve', 'dotbelowcomb'], 'figuredash': [], 'ohookabove': ['o', 'hookabovecomb'], 'obreve': ['o', 'breve'], 'Odieresis': ['O', 'dieresis'], 'zhebreve-cy': ['zhe-cy', 'brevecomb.component'], 'lari': [], 'Hcaron': ['H', 'caron'], 'Dmod': [], 'upsilonpsiliperispomeni': ['upsilon', 'psiliperispomeni'], 'TturnedSmall': [], 'otildedieresis': ['o', 'otilde.component'], 'breveinvertedbelowcomb': ['perispomeni'], 'slashlongcomb': [], 'tonebarextrahighmod': [], 'engmod': [], 'lowdownarrowheadmod': [], 'piSymbol': [], 'tse-cy': [], 'qstrokethroughdescender': ['q'], 'Wdieresis': ['W', 'dieresis'], 'oe': [], 'uni256a': [], 'arrowupbelowcomb': [], 'dotaboverightcomb': ['dotaccent'], 'endlowtonemod': [], 'linferior': [], 'upsilondialytikavaria': ['upsilon', 'dialytikavaria'], 'yuslittleiotified-cy': [], 'Upsilonmacron': ['Y', 'macroncomb'], 'Emacron': ['E', 'macron'], 'Sobliquestroke': ['S'], 'colon': [], 'Alphadasiavariaprosgegrammeni': ['A', 'dasiavaria-uc', 'prosgegrammeni'], 'Ncaron': ['N', 'caron'], 'OopenSmall': ['oopen'], 'sigma': [], 'eiotified-cy': [], 'Udieresisgrave': ['U', 'gravecomb.component3'], 'Mepigraphicarchaic': [], 'uni2557': [], 'blackSmallSquare': [], 'kgreenlandic': [], 'sho': ['thorn'], 'rscript': [], 'Ain-egyptological': [], 'thstrikethrough': ['t', 'h', 'thstrikethrough.component'], 'Iotaoxia': ['I', 'oxia-uc'], 'Dze-cy': ['S'], 'udieresis-cy': ['y', 'dieresis'], 'uni2195': [], 'rhookturned': [], 'notequal': [], 'koppa-cy': [], 'A-cy': ['A'], 'Zhedieresis-cy': ['Zhe-cy', 'dieresis'], 'hcomb': [], 'Omicrondasiavaria': ['O', 'dasiavaria-uc'], 'hPalatalhook': ['h', 'dpalatalhook.component'], 'Iotapsilioxia': ['I', 'psilioxia-uc'], 'parenleftsuperior': ['parenleft.component'], 'Omod': [], 'Udieresiscaron': ['U', 'Udieresis.component'], 'fivesixths': ['five.numr', 'fraction', 'six.dnom'], 'product': [], 'Abreve.component': [], 'published': [], 'chimod': [], 'i-cy': ['i'], 'zcurl': [], 'minus': [], 'eight.numr': [], 'Zdescender': [], 'egrave': ['e', 'grave'], 'Mdotaccent': ['M', 'dotaccent'], 'quotedblbase': [], 'Ncommaaccent': ['N', 'cedillacomb.component'], 'Ve-cy': ['B'], 'lowuparrowheadmod': [], 'acircumflextilde': ['a', 'tildecomb.component'], 'asteriskbelowcomb': [], 'UpsilonhookSymbol': [], 'Ldoublebar': ['L'], 'uni2302': [], 'Yot': ['J'], 'einvertedbreve': ['e', 'perispomeni'], 'underscore': [], 'underscoredbl': [], 'gravecomb': [], 'dbdigraph': [], 'ge-cy': [], 'imacron-cy': ['ii-cy', 'macron'], 'shook': [], 'Alphadasia': ['A', 'dasia-uc'], 'wdotaccent': ['w', 'dotaccent'], 'foursuperior': ['four.numr'], 'at': [], 'lcommaaccent': ['l', 'cedillacomb.component'], 'less': [], 'betamod': [], 'four.blackCircled': [], 'uni2554': [], 'cedillacomb': ['cedilla'], 'ezhtail': [], 'uni256b': [], 'Halfh': [], 'sigmaLunateDottedSymbol': ['c', 'dotmiddle.component'], 'schwa-cy': ['eturned'], 'epsilonLunateSymbol': [], 'yacute': ['y', 'acute'], 'tilde': [], 'otilde': ['o', 'tilde'], 'breve': [], 'u': [], 'Lsmallmod': [], 'jcircumflex': ['jdotless', 'circumflex'], 'xpalatalhook': ['x', 'dpalatalhook.component'], 'dz': ['d', 'z'], 'abreve.component3': [], 'endash': [], 'epsilonoxia': ['epsilon', 'oxia'], 'rcaron': ['r', 'caron'], 'ringhalfright': [], 'eopen': ['epsilon'], 'Gestrokehook-cy': ['Ghestroke-cy', 'Gestrokehook-cy.component'], 'brevecomb': ['breve'], 'hv': [], 'ydieresis': ['y', 'dieresis'], 'nje-cy': [], 'Osmall': ['o'], 'Zstroke': [], 'Tcommaaccent': ['T', 'cedillacomb.component'], 'Xdotaccent': ['X', 'dotaccent'], 'uni2566': [], 'ainferior': ['amod'], 'yusbig-cy': [], 'G': [], 'Ohm': [], 'uring': ['u', 'ring'], 'Dcedilla': ['D', 'cedillacomb.component1'], 'upsilonmacron': ['upsilon', 'macroncomb'], 'Yuslittle-cy': [], 'commareversedabovecomb': ['dasia'], 'etildebelow': ['e', 'tildebelow'], 'Av': [], 'upsilonoxia': ['upsilon', 'oxia'], 'cuatrillo': [], 'kinferior': ['kmod'], 'omegapsiliperispomeniypogegrammeni': ['omega', 'psiliperispomeni', 'prosgegrammeni'], 'phiModifier-latin': [], 'acutecomb': [], 'Hdotbelow': ['H', 'dotbelowcomb'], 'Con': [], 'Ldotbelowmacron': ['L', 'macron', 'dotbelowcomb'], 'primemod': ['quoteright'], 'sharp-musical': [], 'eopenretroflexhook': ['epsilon'], 'Lje-cy': [], 'southWestArrow': [], 'ubarmod': [], 'alphaoxia': ['alpha', 'oxia'], 'ddotbelow': ['d', 'dotbelowcomb'], 'lowcircumflexmod': ['circumflex'], 'ecircumflexacute': ['e', 'acutecomb.component'], 'quotereversed': [], 'w': [], 'breveinvertedcomb': ['perispomeni'], 'nmod': [], 'rum': ['r'], 'uhornhookabove': ['uhorn', 'hookabovecomb'], 'numero': [], 'a': [], 'thetaSymbol': [], 'Etadasiavaria': ['H', 'dasiavaria-uc'], 'thook': [], 'plus': [], 'bFlourish': [], 'kstroke': ['k'], 'Che-cy': [], 'nine.tnum': [], 'ecircumflexdotbelow': ['e', 'circumflex', 'dotbelowcomb'], 'cacute': ['c', 'acute'], 'Ytilde': ['Y', 'tilde'], 'doubleapostrophemod': ['quotedblright'], 'qdiagonalstroke': ['q'], 'Yat-cy': [], 'Oopen': [], 'ethmod': [], 'upBlackTriangle': [], 'ainmod': [], 'Uhorn': [], 'dotaccent': [], 'emspace': [], 'threefifths': ['three.numr', 'fraction', 'five.dnom'], 'Khei-coptic': [], 'Adotmacron': ['A', 'macroncomb.component1'], 'mturned': [], 'ydotaccent': ['y', 'dotaccent'], 'adotbelow': ['a', 'dotbelowcomb'], 'AE': [], 'Ccaron': ['C', 'caron'], 'Abreve.component1': [], 'Omicrontonos': ['O', 'tonos-uc'], 'fpalatalhook': ['f', 'dpalatalhook.component'], 'ainvertedbreve': ['a', 'perispomeni'], 'interrobang': [], 'psquirreltail': [], 'ecaron': ['e', 'caron'], 'bmiddletilde': ['b'], 'Ertick-cy': ['Er-cy'], 'Etadasiaoxia': ['H', 'dasiaoxia-uc'], 'etapsiliypogegrammeni': ['eta', 'psili', 'prosgegrammeni'], 'sinologicaldot': ['periodcentered'], 'Pemiddlehook-cy': [], 'divide': [], 'g': [], 'ohornacute': ['ohorn', 'acute'], 'barredomod': [], 'bpalatalhook.component': [], 'two.numr': [], 'onehalf': ['one.numr', 'fraction', 'two.numr'], 'Kappa': ['K'], 'semicolon': [], 'iotadialytikavaria': ['iota', 'dialytikavaria'], 'Scedilla': ['S', 'cedilla'], 'gturned': [], 'glottalstopsmall': [], 'dbloverlinecomb': ['underscoredbl'], 'tedescender-cy': [], 'Vsmall': ['v'], 'uni255e': [], 'Tse-cy': [], 'epsilonpsilioxia': ['epsilon', 'psilioxia'], 'eopenreversedretroflexhook': ['ze-cy'], 'guilsinglright': [], 'Edblgrave': ['E', 'dblgravecomb'], 'aTurnedmod': [], 'lowleftarrowmod': [], 'mediumspace-math': [], 'Eacute': ['E', 'acute'], 'uni2560': [], 'increment': ['Delta'], 'udieresis.component': [], 'adblgrave': ['a', 'dblgravecomb'], 'ihookabove': ['idotless', 'hookabovecomb'], 'Ubar': ['U'], 'upsilondasia': ['upsilon', 'dasia'], 'omicronpsilioxia': ['o', 'psilioxia'], 'Adotbelow': ['A', 'dotbelowcomb'], 'ringbelowcomb': ['ringbelow'], 'manat': [], 'Vtilde': ['V', 'tilde'], 'ucircumflex': ['u', 'circumflex'], 'omegadasiaypogegrammeni': ['omega', 'dasia', 'prosgegrammeni'], 'ncurl': [], 'perthousand': [], 'phi': [], 'gangia-coptic': [], 'onesuperior': ['one.numr'], 'alphadasiaoxia': ['alpha', 'dasiaoxia'], 'softsigncomb-cy': [], 'eightinferior': ['eight.numr'], 'aeVolapuk': [], 'Zcircumflex': ['Z', 'circumflex'], 'uhungarumlaut-cy': ['y', 'hungarumlaut'], 'pdotaccent': ['p', 'dotaccent'], 'Tresillo': [], 'Schwa': [], 'Digamma': [], 'Tretroflexhook': [], 'oxia-uc': [], 'Upsilondasia': ['Y', 'dasia-uc'], 'ohorndotbelow': ['ohorn', 'dotbelowcomb'], 'beginhightonemod': [], 'xabovecomb': ['xbelowcomb'], 'mmiddletilde': ['m'], 'Bstroke': ['B'], 'peso': [], 'ezhcurl': [], 'doublebrevecomb': [], 'etadasiavaria': ['eta', 'dasiavaria'], 'oeturnedwithhorizontalstroke': [], 'Dei-coptic': [], 'germanpenny': [], 'infinity': [], 'psilioxia-uc': [], 'edotbelow': ['e', 'dotbelowcomb'], 'Otildedieresis': ['O', 'Otilde.component'], 'Lmod': [], 'circumflexbelow': [], 'rscriptring': [], 'etadasiavariaypogegrammeni': ['eta', 'dasiavaria', 'prosgegrammeni'], 'Iota': ['I'], 'approxequal': [], 'cedillacomb.component1': [], 'rlonglegturned': [], 'unif002': ['fl'], 'unaspiratedmod': [], 'pmod': [], 'cedilla': [], 'Esmallturned': [], 'Etapsiliperispomeni': ['H', 'psiliperispomeni-uc'], 'macronbelow': [], 'tcaron': ['t', 'caronvert.component'], 'Iotatonos': ['I', 'tonos-uc'], 'wynn': [], 'Schwadieresis-cy': ['Schwa', 'dieresis'], 'Tshe-cy': [], 'ecedillabreve': ['e', 'cedilla', 'breve'], 'bullet': [], 'emod': [], 'lje-cy': [], 'wgrave': ['w', 'grave'], 'dei-coptic': [], 'ehookabove': ['e', 'hookabovecomb'], 'omegavaria': ['omega', 'varia'], 'Ainvertedbreve': ['A', 'perispomeni'], 'Iotadasiaoxia': ['I', 'dasiaoxia-uc'], 'Astroke.component': [], 'schwainferior': ['schwamod'], 'usmod': [], 'Thorn': [], 'Upsilondasiaperispomeni': ['Y', 'dasiaperispomeni-uc'], 'lefttorightembedding': [], 'vtilde': ['v', 'tilde'], 'ordmasculine': [], 'Upsilontonos': ['Y', 'tonos-uc'], 'questiondown': [], 'epsilonpsili': ['epsilon', 'psili'], 'acutelowmod': ['acute'], 'leftanglebelowcomb': ['endhightonemod'], 'Alphapsilioxiaprosgegrammeni': ['A', 'psilioxia-uc', 'prosgegrammeni'], 'chi': [], 'two.blackCircled': [], 'overline': [], 'ezhreversed': [], 'Omegapsilioxia': ['Ohm', 'psilioxia-uc'], 'Rdotbelow': ['R', 'dotbelowcomb'], 'Tturned': [], 'jdotlessstrokemod': [], 'etapsilivaria': ['eta', 'psilivaria'], 'q': [], 'Ydieresis': ['Y', 'dieresis'], 'Udieresis-cy': ['U-cy', 'dieresis'], 'qhooktail': [], 'Edieresis': ['E', 'dieresis'], 'udieresis': ['u', 'dieresis'], 'umacron': ['u', 'macron'], 'Astroke': ['A', 'Astroke.component'], 'uSideways': [], 'abrevetilde': ['a', 'abreve.component3'], 'Alphavaria': ['A', 'varia-uc'], 'es-cy': ['c'], 'Rsmallinverted': [], 'xdieresis': ['x', 'dieresis'], 'edotaccent': ['e', 'dotaccent'], 'Ecircumflex': ['E', 'circumflex'], 'mu': [], 'dcroat': [], 'six.numr': [], 'etapsilivariaypogegrammeni': ['eta', 'psilivaria', 'prosgegrammeni'], 'aturned': [], 'Pstrokethroughdescender': ['P'], 'Tz': [], 'Oslash': [], 'caronbelowcomb': ['caron'], 'Epsilondasia': ['E', 'dasia-uc'], 'izhitsadblgrave-cy': ['izhitsa-cy', 'dblgravecomb'], 'omegaperispomeni': ['omega', 'perispomeni'], 'Hbar': [], 'ginsular': [], 'sinsular': [], 'Omegadasiavariaprosgegrammeni': ['Ohm', 'dasiavaria-uc', 'prosgegrammeni'], 'kabashkir-cy': [], 'Gturnedinsular': [], 'inverseBullet': [], 'alpha-latin': [], 'tonebarmidmod': [], 'verticallineabovecomb': ['verticallinemod'], 'Kturned': [], 'hookabovecomb.component': [], 'hhook': [], 'Ucaron': ['U', 'caron'], 'aogonek': ['a', 'ogonek'], 'Ie-cy': ['E'], 'eshcurl': [], 'germandbls': [], 'UeVolapuk': [], 'glottalstopmod': [], 'oo': [], 'hdieresis': ['h', 'dieresis'], 'cedi': [], 'nottildeabovecomb': [], 'openshelfmod': [], 'Pacute': ['P', 'acute'], 'Alphapsiliprosgegrammeni': ['A', 'psili-uc', 'prosgegrammeni'], 'lzdigraph': [], 'Yeru-cy': [], 'kdotbelow': ['k', 'dotbelowcomb'], 'zcircumflex': ['z', 'circumflex'], 'graveacutegravecomb': ['grave', 'acute', 'grave'], 'yat-cy': [], 'Sigma': [], 'lineseparator': [], 'Etadasiaoxiaprosgegrammeni': ['H', 'dasiaoxia-uc', 'prosgegrammeni'], 'breveinvertedbrevemod': [], 'Etapsiliprosgegrammeni': ['H', 'psili-uc', 'prosgegrammeni'], 'lowtildemod': ['tilde'], 'otildeacute': ['o', 'acutecomb.component3'], 'Cheabkhasian-cy': [], 'Ii-cy': [], 'Omicronoxia': ['O', 'oxia-uc'], 'ocircumflexacute': ['o', 'acutecomb.component'], 'tugrik': [], 'zdotaccent': ['z', 'dotaccent'], 'I-cy': ['I'], 'oogonekmacron': ['oogonek', 'macron'], 'schwa': ['eturned'], 'thorn': [], 'Zlinebelow': ['Z', 'macronbelow'], 'bilabialpercussive': [], 'parenrightinferior': ['parenright.component'], 'Alphapsili': ['A', 'psili-uc'], 'AeVolapuk': [], 'uniFB06': [], 'Rho': ['P'], 'B': [], 'Omegadasiaoxia': ['Ohm', 'dasiaoxia-uc'], 'Rmod': [], 'dasiavaria': [], 'nretroflexhookmod': [], 'Gcommaaccent': ['G', 'cedillacomb.component'], 'Iogonek': ['I', 'ogonek'], 'Gmacron': ['G', 'macron'], 'Iotadasia': ['I', 'dasia-uc'], 'Usmall': [], 'equalinferior': ['equal.component'], 'amod': [], 'Omegapsiliperispomeniprosgegrammeni': ['Ohm', 'psiliperispomeni-uc', 'prosgegrammeni'], 'Racute': ['R', 'acute'], 'omegapsiliperispomeni': ['omega', 'psiliperispomeni'], 'chekhakassian-cy': [], 'Pedescender-cy': [], 'Vhook': [], 'ycircumflex': ['y', 'circumflex'], 'doubleverticallinebelowcomb': [], 'pi': [], 'halfh': [], 'schwahook': [], 'cmod': [], 'quotedbl': [], 'pedescender-cy': [], 'acutemacroncomb': ['firsttonechinese', 'acute'], 'oOpenmod': [], 'Finsular': [], 'dasiaoxia-uc': [], 'glottalstopstroke': [], 'oi': [], 'sdotbelow': ['s', 'dotbelowcomb'], 'Zdotaccent': ['Z', 'dotaccent'], 'ograve': ['o', 'grave'], 'Uhorntilde': ['Uhorn', 'tilde'], 'Udieresis.component': [], 'omegadasiaoxia': ['omega', 'dasiaoxia'], 'umacron.component': [], 'omicrondasiavaria': ['o', 'dasiavaria'], 'vpalatalhook': ['v', 'dpalatalhook.component', 'gpalatalhook.component'], 'Uhorngrave': ['Uhorn', 'grave'], 'dhookandtail': ['dhook'], 'Mepigraphicinverted': [], 'dcomb': [], 'iacute': ['idotless', 'acute'], 'Omacronacute': ['O', 'acutecomb.component1'], 'guarani': [], 'Aogonek': ['A', 'ogonek'], 'rpalatalhook': ['r', 'dpalatalhook.component'], 'Ucircumflexbelow': ['U', 'circumflexbelow'], 'pamphyliandigamma': ['ii-cy'], 'Omega': ['Ohm'], 'atilde': ['a', 'tilde'], 'oneninth': ['nine.dnom', 'fraction', 'one.numr'], 'gscriptcrossedtail': [], 'uni2565': [], 'questiongreek': ['semicolon'], 'Dcroat': ['Eth'], 'exclam': [], 'eshretroflexhook': [], 'middlegraveaccentmod': ['grave'], 'equal': [], 'epsilontonos': ['epsilon', 'tonos'], 'softhyphen': ['hyphen'], 'uni047D': [], 'ohorngrave': ['ohorn', 'grave'], 'eOpenmod': [], 'n': [], 'tretroflexhook': [], 'Llinebelow': ['L', 'macronbelow'], 'parenright.component': [], 'Alphadasiavaria': ['A', 'dasiavaria-uc'], 'Ecaron': ['E', 'caron'], 'euro': [], 'Umacron.component': [], 'wturned': [], 'rcomb': [], 'rnohandle': [], 'uni2562': [], 'Gscript': [], 'Psmall': [], 'dmod': [], 'suspensioncomb': [], 'nhookretroflex': [], 'Ushort-cy': ['U-cy', 'brevecomb.component'], 'Gmod': [], 'inverseWhiteCircle': [], 'ereversed': [], 'engcrossedtail': [], 'uni250c': [], 'alphadasiaperispomeniypogegrammeni': ['alpha', 'dasiaperispomeni', 'prosgegrammeni'], 'upsilondieresistonos': ['upsilon', 'dieresistonos'], 'tcircumflexbelow': ['t', 'circumflexbelow'], 'dasia': [], 'eng': [], 'Yacute': ['Y', 'acute'], 'kturned': [], 'NreversedSmall': ['ii-cy'], 'sobliquestroke': ['s'], 'percent': [], 'klinebelow': ['k', 'macronbelow'], 'omegaypogegrammeni': ['omega', 'prosgegrammeni'], 'Iotavrachy': ['I', 'brevecomb'], 'dcircumflexbelow': ['d', 'circumflexbelow'], 'ncrossedtail': [], 'Yhookabove': ['Y', 'hookabovecomb'], 'Lj': ['L', 'j'], 'abreve.component': [], 'ndotbelow': ['n', 'dotbelowcomb'], 'Alef-egyptological': [], 'Robliquestroke': ['R'], 'iotastroke': ['iota', 'firsttonechinese'], 'yi-cy': ['idotless', 'dieresis'], 'righttoleftmark': [], 'edieresis': ['e', 'dieresis'], 'Esmall': [], 'smiddletilde': ['s'], 'Aie-cy': ['AE'], 'Nlinebelow': ['N', 'macronbelow'], 'slash': [], 'gpalatalhook': ['g', 'dpalatalhook.component', 'gpalatalhook.component'], 'oinferior': ['omod'], 'Wdotbelow': ['W', 'dotbelowcomb'], 'Omegapsilivariaprosgegrammeni': ['Ohm', 'psilivaria-uc', 'prosgegrammeni'], 'Shha-cy': [], 'equal.component': [], 'Beta': ['B'], 'bar': [], 'T': [], 'Scircumflex': ['S', 'circumflex'], 'Thornstrokethroughdescender': ['Thorn'], 'kastroke-cy': [], 'V': [], 'iotaperispomeni': ['iota', 'perispomeni'], 'archaicsampi': [], 'pstrokethroughdescender': ['p'], 'circumflexbelowcomb': ['circumflexbelow'], 'digamma': [], 'udblgrave': ['u', 'dblgravecomb'], 'flenis': ['f'], 'dtail': [], 'upsilonstroke': ['upsilon-latin'], 'etadasiaoxiaypogegrammeni': ['eta', 'dasiaoxia', 'prosgegrammeni'], 'alphaperispomeni': ['alpha', 'perispomeni'], 'b': [], 'tdotbelow': ['t', 'dotbelowcomb'], 'dagesh-hb': [], 'Ygrave': ['Y', 'grave'], 'Hdieresis': ['H', 'dieresis'], 'obarred': ['obarred-cy'], 'Aringacute': ['Aring', 'acute'], 'bulletoperator': ['periodcentered'], 'Alpha-latin': [], 'fourperemspace': [], 'Sacute': ['S', 'acute'], 'Tcedilla': ['T', 'cedilla'], 'jdotless': [], 'Rsmall': [], 'ldotbelowmacron': ['l', 'macron', 'dotbelowcomb'], 'nmiddletilde': ['n'], 'arighthalfring': ['a', 'ringhalfright'], 'ugrave': ['u', 'grave'], 'L': [], 'ypogegrammeni': ['ypogegrammenicomb'], 'gravecomb.component3': [], 'nine.dnom': ['nine.numr'], 'uhungarumlaut': ['u', 'hungarumlaut'], 'Gsmall': [], 'icomb': [], 'Hbrevebelow': ['H', 'brevebelow'], 'ocircumflexhookabove': ['o', 'hookabovecomb.component'], 'Tdotaccent': ['T', 'dotaccent'], 'hairspace': [], 'odotaccent': ['o', 'dotaccent'], 'Izhitsadblgrave-cy': ['Izhitsa-cy', 'dblgravecomb'], 'gbreve': ['g', 'breve'], 'Ksmall': ['kgreenlandic'], 'rhoStrokeSymbol': ['rho', 'firsttonechinese'], 'Ystroke': ['Y'], 'betaSymbol': [], 'rrightleg': [], 'kadescender-cy': [], 'ubreve': ['u', 'breve'], 'tdieresis': ['t', 'dieresis'], 'nu': [], 'Icircumflex': ['I', 'circumflex'], 'Kmod': [], 'iotadialytikaoxia': ['iota', 'dialytikaoxia'], 'arrowheadrightheadupbelowcomb': [], 'Eopen': [], 'threeperemspace': [], 'utilde': ['u', 'tilde'], 'Qdiagonalstroke': [], 'ohorn': [], 'wmod': [], 'lambda': [], 'varia-uc': [], 'alphaypogegrammeni': ['alpha', 'prosgegrammeni'], 'Mhook': [], 'tresillo': [], 'Tinsular': [], 'hcedilla': ['h', 'cedilla'], 'arrowheadrightheaddownbelow': [], 'Kaverticalstroke-cy': [], 'deltaturned': [], 'lpalatalhookmod': [], 'quotesingle': [], 'fmiddletilde': ['f'], 'peseta': [], 'robliquestroke': ['r'], 'ain': [], 'Eogonek': ['E', 'ogonek'], 'sacute.component': [], 'fdotaccent': ['f', 'dotaccent'], 'Etildebelow': ['E', 'tildebelow'], 'Icaron': ['I', 'caron'], 'oeinverted': [], 'Zswashtail': [], 'koroniscomb': ['koronis'], 'Ccedillaacute': ['C', 'cedilla', 'acute'], 'Zhook': [], 'Scaron': ['S', 'caron'], 'dinsular': [], 'Scarondotaccent': ['S', 'Scaron.component'], 'austral': [], 'scaron.component': [], 'uni2215': ['slash'], 'FStroke': [], 'c': [], 'adieresis': ['a', 'dieresis'], 'oogonek': ['o', 'ogonek'], 'u-cy': ['y'], 'sswashtail': [], 'EthSmall': [], 'um': [], 'Yusbig-cy': [], 'ccedilla': ['c', 'cedilla'], 'uni20BF': [], 'four.numr': [], 'koppa': [], 'bmod': [], 'Ksi-cy': [], 'breveinverteddoublecomb': [], 'uni266a': [], 'clickdental': ['bar'], 'umacrondieresis': ['u', 'umacron.component'], 'won': [], 'Pepigraphicreversed': [], 'one.dnom': ['one.numr'], 'Mturned': [], 'alphadasiavariaypogegrammeni': ['alpha', 'dasiavaria', 'prosgegrammeni'], 'macroncomb': [], 'Nj': ['N', 'j'], 'alphapsiliypogegrammeni': ['alpha', 'psili', 'prosgegrammeni'], 'onesixth': ['one.numr', 'fraction', 'six.dnom'], 'pstroke': ['p'], 'dlinebelow': ['d', 'macronbelow'], 'mdotbelow': ['m', 'dotbelowcomb'], 'Gammaafrican': [], 'oloop': [], 'doublebrevebelowcomb': ['doublebrevecomb'], 'Nje-cy': [], 'ccedillaacute': ['c', 'cedilla', 'acute'], 'kdiagonalstroke': ['k'], 'Zedescender-cy': [], 'esh': [], 'intersection': [], 'colonsign': [], 'Ereversed-cy': [], 'Ocircumflexdotbelow': ['O', 'circumflex', 'dotbelowcomb'], 'brevecomb.component': [], 'eReversedopenmod': [], 'nhookleft': [], 'uni255f': [], 'Edieresis-cy': ['Ereversed-cy', 'dieresis'], 'gammamod': [], 'omegadasiaoxiaypogegrammeni': ['omega', 'dasiaoxia', 'prosgegrammeni'], 'liraTurkish': [], 'Acircumflexgrave': ['A', 'gravecomb.component'], 'upsilondasiaperispomeni': ['upsilon', 'dasiaperispomeni'], 'Upsilon': ['Y'], 'alphadasiaoxiaypogegrammeni': ['alpha', 'dasiaoxia', 'prosgegrammeni'], 'Sdotaccent': ['S', 'dotaccent'], 'oTophalfmod': [], 'mmod': [], 'Bdotbelow': ['B', 'dotbelowcomb'], 'dzcurl': [], 'm': [], 'iotapsilivaria': ['iota', 'psilivaria'], 'tildecomb': [], 'Iishorttail-cy': ['Iishort-cy', 'tail.component'], 'rrotunda': [], 'macroncomb.component1': [], 'tonos-uc': [], 'gpalatalhook.component': [], 'Etadasia': ['H', 'dasia-uc'], 'en-cy': [], 'Gcircumflex': ['G', 'circumflex'], 'heng': [], 'oopenstroke-blackletter': [], 'Iotadasiavaria': ['I', 'dasiavaria-uc'], 'ushort-cy': ['y', 'brevecomb.component'], 'yhook': [], 'vturnedmod': [], 'plusbelowcomb': ['plusmod'], 'Gbreve': ['G', 'breve'], 'Ecircumflexhookabove': ['E', 'hookabovecomb.component'], 'tonesix': [], 'Nhookleft': [], 'xdotaccent': ['x', 'dotaccent'], 'omacronacute': ['o', 'acutecomb.component1'], 'Acircumflexdotbelow': ['A', 'circumflex', 'dotbelowcomb'], 'iotamacron': ['iota', 'macroncomb'], 'homotheticabovecomb': [], 'alphadasia': ['alpha', 'dasia'], 'Enhook-cy': [], 'oeTurned': [], 'glottalinvertedstroke': [], '.null': [], 'Hhook': [], 'amacron': ['a', 'macron'], 'chook': [], 'uni258c': [], 'zero.pnum_enclosingkeycapcomb': [], 'ypogegrammenicomb': ['prosgegrammeni'], 'hardsigncomb-cy': [], 'one.pnum_enclosingkeycapcomb': [], 'Iotamacron': ['I', 'macroncomb'], 'Ubreve': ['U', 'breve'], 'ccurlmod': [], 'omicron': ['o'], 'eshbaseline': ['esh'], 'pedescender-cy.component': [], 'AA': [], 'tdiagonalstroke': ['t', 'slashlongcomb'], 'Epsilonpsilivaria': ['E', 'psilivaria-uc'], 'ahookabove': ['a', 'hookabovecomb'], 'X': [], 'xlongleftlegandlowrightring': [], 'alphapsilivariaypogegrammeni': ['alpha', 'psilivaria', 'prosgegrammeni'], 'sixinferior': ['six.numr'], 'snakebelowcomb': [], 'zhedieresis-cy': ['zhe-cy', 'dieresis'], 'Omegadasiavaria': ['Ohm', 'dasiavaria-uc'], 'igrave': ['idotless', 'grave'], 'tripleprime': [], 'Delta': [], 'em-cy': [], 'U-cy': [], 'eogonek': ['e', 'ogonek'], 'dblgravecomb': [], 'Lmiddletilde': ['L'], 'oacute': ['o', 'acute'], 'tmod': [], 'gravetonecomb': ['grave'], 'uk-cy': [], 'uniA7AE': [], 'Sho': ['Thorn'], 'colonmod': ['colon'], 'uni2524': [], 'Hdescender': ['Endescender-cy'], 'Koppa': [], 'tz': [], 'palatalhookcomb': [], 'Lsmall': [], 'uhorngrave': ['uhorn', 'grave'], 'dblverticalbar': ['bar', 'bar'], 'iotadasiavaria': ['iota', 'dasiavaria'], 'Uhorndotbelow': ['Uhorn', 'dotbelowcomb'], 'ncircumflexbelow': ['n', 'circumflexbelow'], 'Upsilonoxia': ['Y', 'oxia-uc'], 'tildecomb.component': [], 'rinsular': [], 'asciicircum': [], 'iotadieresistonos': ['iota', 'dieresistonos'], 'W': [], 'num': ['n'], 'macronbelowcomb': ['macronbelow'], 'equalbelowcomb': [], 'uni2592': [], 'kip': [], 'J': [], 'et': [], 'astroke': ['a', 'slashlongcomb'], 'iotapsilioxia': ['iota', 'psilioxia'], 'ostrokeopenoturned': [], 'dialytikavaria': [], 'Ecircumflexgrave': ['E', 'gravecomb.component'], 'five.pnum_enclosingkeycapcomb': [], 'Longaepigraphici': [], 'brevebelow': [], 'second': [], 'horncomb': [], 'seven.dnom': ['seven.numr'], 'florin': [], 'threequarters': ['three.numr', 'fraction', 'four.numr'], 'nlegrightlong': [], 'acute': [], 'gravecomb.component1': [], 'two.dnom': ['two.numr'], 'Idieresis-cy': ['Ii-cy', 'dieresis'], 'gamma': [], 'eTurnedopenmod': [], 'tildebelow': [], 'lpalatalhook': ['l', 'dpalatalhook.component'], 'oopenoturned': [], 'plusmod': [], 'upsilontonos': ['upsilon', 'tonos'], 'Dje-cy': [], 'Etadasiaprosgegrammeni': ['H', 'dasia-uc', 'prosgegrammeni'], 'sdotbelowdotaccent': ['s', 'dotbelowcomb', 'dotaccent'], 'Nmod': [], 'iu-cy': [], 'Emacrongrave': ['E', 'gravecomb.component1'], 'pemiddlehook-cy': [], 'perispomeni': [], 'Rhodasia': ['P', 'dasia-uc'], 'spesmilo': [], 'epsilonpsilivaria': ['epsilon', 'psilivaria'], 'El-cy': [], 'lefttorightmark': [], 'shookmod': [], 'acircumflexgrave': ['a', 'gravecomb.component'], 'jdotlessstrokehook': [], 'five': [], 'pflourish': [], 's': [], 'heta': [], 'o-blackletter': [], 'Ucircumflex': ['U', 'circumflex'], 'Tonefive': [], 'omegatonos': ['omega', 'tonos'], 'threeeighths': ['three.numr', 'fraction', 'eight.numr'], 'Ocircumflex': ['O', 'circumflex'], 'zvisigothic': [], 'spirantVoicedlaryngeal': [], 'Omega-cy': [], 'etapsiliperispomeniypogegrammeni': ['eta', 'psiliperispomeni', 'prosgegrammeni'], 'four.dnom': ['four.numr'], 'Bsmall': [], 'iotapsiliperispomeni': ['iota', 'psiliperispomeni'], 'Oogonekmacron': ['O', 'macron', 'ogonek'], 'shima-coptic': [], 'hturnedmod': [], 'psiliperispomeni': [], 'Hahook-cy': [], 'omegaclosed-latin': [], 'Kahook-cy': [], 'jcrossedtail': [], 'uacute': ['u', 'acute'], 'scriptgmod': ['gmod'], 'zlinebelow': ['z', 'macronbelow'], 'ocaron': ['o', 'caron'], 'Ebreve': ['E', 'breve'], 'ulefthook': [], 'softsign-cy': [], 'Be-cy': [], 'scedilla': ['s', 'cedilla'], 'fi': [], 'ldot': ['l', 'dotmiddle.component'], 'omicrondasia': ['o', 'dasia'], 'thstrikethrough.component': [], 'Udieresisacute': ['U', 'acutecomb.component5'], 'Wdotaccent': ['W', 'dotaccent'], 'space': [], 'utildeacute': ['u', 'acutecomb.component3'], 'nacute': ['n', 'acute'], 'Hturned': [], 'glottalstopstrokereversed': [], 'lmod': [], 'ulefthookmod': [], 'asterisk': [], 'emtail-cy': ['em-cy', 'tail.component'], 'lturned': [], 'Istroke': [], 'squarebelowcomb': [], 'Aacute': ['A', 'acute'], 'Ia-cy': [], 'obarreddieresis-cy': ['obarred-cy', 'dieresis'], 'Csmall': ['c'], 'ezh': [], 'rdotbelow': ['r', 'dotbelowcomb'], 'VY': [], 'pe-cy': [], 'zerosuperior': ['zero.numr'], 'commaturnedabovecomb': [], 'Otildemacron': ['O', 'Otilde.component1'], 'mlonglegturned': [], 'question': [], 'itilde': ['idotless', 'tilde'], 'lowrightarrowheadmod': [], 'lum': [], 'lhighstroke': [], 'Beta-latin': [], 'NReversedmod': [], 'Nsmall': [], 'Pstroke': ['P'], 'uni263a': [], 'horizontalbar': ['emdash'], 'zdescender': [], 'ueVolapuk': [], 'Einvertedbreve': ['E', 'perispomeni'], 'iishort-cy': ['ii-cy', 'brevecomb.component'], 'rbelowcomb': ['rmod'], 'tildedoublecomb': [], 'hinferior': [], 'bridgebelowcomb': [], 'Dzcaron': ['D', 'z', 'caron'], 'EzhSmall': [], 'gstroke': [], 'Saltillo': [], 'Tsmall': ['te-cy'], 'Jcircumflex': ['J', 'circumflex'], 'ytilde': ['y', 'tilde'], 'logicalnot': [], 've-cy': [], 'Chedieresis-cy': ['Che-cy', 'dieresis'], 'Dcaron': ['D', 'caron'], 'Lbroken': [], 'khook': [], 'Yr': [], 'Eiotified-cy': [], 'Zhedescender-cy': [], 'iegrave-cy': ['e', 'grave'], 'yring': ['y', 'ring'], 'Idblgrave': ['I', 'dblgravecomb'], 'etapsilioxia': ['eta', 'psilioxia'], 'plussuperior': ['plus.component'], 'upsilonmod': [], 'ntilde': ['n', 'tilde'], 'commaturnedmod': [], 'x': [], 'Ghemiddlehook-cy': [], 'Emacronacute': ['E', 'acutecomb.component1'], 'AEacute': ['AE', 'acute'], 'edieresis-cy': ['ereversed-cy', 'dieresis'], 'idieresis-cy': ['ii-cy', 'dieresis'], 'uni255d': [], 'Yuslittleiotified-cy': [], 'acutegraveacutecomb': ['acute', 'grave', 'acute'], 'one': [], 'iotadasiaperispomeni': ['iota', 'dasiaperispomeni'], 'zedescender-cy': [], 'blinebelow': ['b', 'macronbelow'], 'lmiddletildemod': [], 'san': [], 'Ka-cy': ['K'], 'downBlackTriangle': [], 'uni2564': [], 'Atilde': ['A', 'tilde'], 'Chekhakassian-cy': [], 'indepartingtonemod': [], 'cbar': ['c'], 'dcurl': [], 'Etilde': ['E', 'tilde'], 'nun-hb': [], 'UpsilonacutehookSymbol': ['UpsilonhookSymbol', 'tonos-uc'], 'eturned': [], 'lacute': ['l', 'acute'], 'eight.tnum': [], 'odieresismacron': ['o', 'macroncomb.component'], 'adotmacron': ['a', 'macroncomb.component1'], 'Eta': ['H'], 'dialytikaperispomeni': [], 'bdotbelow': ['b', 'dotbelowcomb'], 'Tdotbelow': ['T', 'dotbelowcomb'], 'Sdotbelow': ['S', 'dotbelowcomb'], 'Omicronvaria': ['O', 'varia-uc'], 'lambdastroke': [], 'uni2591': [], 'alphaturned-latin': [], 'Upsilonafrican': [], 'ninferior': [], 'jcrossedtailmod': [], 'Omicron': ['O'], 'tinferior': ['tmod'], 'Omegaoxia': ['Ohm', 'oxia-uc'], 'cent': [], 'uniFB04': [], 'Adieresis': ['A', 'dieresis'], 'uhorndotbelow': ['uhorn', 'dotbelowcomb'], 'd': [], 'glottalstopinverted': [], 'haabkhasian-cy': [], 'Pi': [], 'omicronpsili': ['o', 'psili'], 'Nacute': ['N', 'acute'], 'Chook': [], 'arrowheaddownmod': [], 'ogonek': [], 'therefore': [], 'Haabkhasian-cy': [], 'au': [], 'Omegapsiliperispomeni': ['Ohm', 'psiliperispomeni-uc'], 'arrowheadleftmod': [], 'etapsilioxiaypogegrammeni': ['eta', 'psilioxia', 'prosgegrammeni'], 'eshpalatalhook': ['esh', 'dpalatalhook.component', 'gpalatalhook.component'], 'nine.blackCircled': [], 'xmod': [], 'dasiavaria-uc': [], 'psi': [], 'fiveinferior': ['five.numr'], 'omegaperispomeniypogegrammeni': ['omega', 'perispomeni', 'prosgegrammeni'], 'eretroflexhook': ['e', 'aretroflexhook.component'], 'dasiaoxia': [], 'llinebelow': ['l', 'macronbelow'], 'comma': [], 'hadescender-cy': [], 'epsilonLunateReversedSymbol': [], 'zhe-cy': [], 'hbrevebelow': ['h', 'brevebelow'], 'Iotavaria': ['I', 'varia-uc'], 'iotadasiaoxia': ['iota', 'dasiaoxia'], 'vdiagonalstroke': ['v'], 'napostrophe': ['n', 'quoteright'], 'Etaoxia': ['H', 'oxia-uc'], 'scarondotaccent': ['s', 'scaron.component'], 'exclamdown': [], 'guilsinglleft': [], 'Alphadasiaperispomeniprosgegrammeni': ['A', 'dasiaperispomeni-uc', 'prosgegrammeni'], 'numeral-greek': [], 'Edotbelow': ['E', 'dotbelowcomb'], 'doubleringbelowcomb': [], 'uni2550': [], 'LJ': ['L', 'J'], 'Obarreddieresis-cy': ['Obarred-cy', 'dieresis'], 'Phook': [], 'gmacron': ['g', 'macron'], 'eight.blackCircled': [], 'iotadasia': ['iota', 'dasia'], 'whiteCircle': [], 'Etavaria': ['H', 'varia-uc'], 'Upsilondasiaoxia': ['Y', 'dasiaoxia-uc'], 'six': [], 'sigmaLunateSymbol': ['c'], 'fmod': [], 'uni2593': [], 'ij': ['i', 'j'], 'yusbigiotified-cy': [], 'icaron': ['idotless', 'caron'], 'omega': [], 'Iacute': ['I', 'acute'], 'yuslittle-cy': [], 'filledRect': [], 'lsinvertedlazymod': [], 'uhornacute': ['uhorn', 'acute'], 'Cbar': ['C'], 'Lturned': [], 'Ze-cy': [], 'je-cy': ['j'], 'macute': ['m', 'acute'], 'multiply': [], 'Mu': ['M'], 'eltail-cy': ['el-cy', 'tail.component'], 'Odotbelow': ['O', 'dotbelowcomb'], 'zero': [], 'lowleftarrowheadmod': [], 'arrowdoublerightbelowcomb': [], 'mlonglegturnedmod': [], 'ia-cy': [], 'acircumflexhookabove': ['a', 'hookabovecomb.component'], 'Xdieresis': ['X', 'dieresis'], 'omicrontonos': ['o', 'tonos'], 'upArrow': [], 'Alphapsilioxia': ['A', 'psilioxia-uc'], 'Uogonek': ['U', 'ogonek'], 'SigmaLunateDottedSymbol': ['C', 'dotmiddle.component'], 'acutecomb.component3': [], 'doubleprimemod': ['quotedblright'], 'ymacron': ['y', 'firsttonechinese'], 'tenge': [], 'l': [], 'eight.dnom': ['eight.numr'], 'ecomb': [], 'zero.tnum': [], 'psi-cy': [], 'Omegadasiaprosgegrammeni': ['Ohm', 'dasia-uc', 'prosgegrammeni'], 'Yogh': [], 'Omegadasia': ['Ohm', 'dasia-uc'], 'Ocircumflexgrave': ['O', 'gravecomb.component'], 'khei-coptic': [], 'gedescender-cy': [], 'scaron': ['s', 'caron'], 'Iepigraphicsideways': [], 'seveneighths': ['seven.numr', 'fraction', 'eight.numr'], 'e-blackletter': [], 'Kcommaaccent': ['K', 'cedillacomb.component'], 'Cacute': ['C', 'acute'], 'minferior': ['mmod'], 'hungarumlaut': [], 'rhodasia': ['rho', 'dasia'], 'Ezhreversed': [], 'tlinebelow': ['t', 'macronbelow'], 'middledoubleacuteaccentmod': ['hungarumlaut'], 'gacute': ['g', 'acute'], 'Cdotaccent': ['C', 'dotaccent'], 'omegapsilioxiaypogegrammeni': ['omega', 'psilioxia', 'prosgegrammeni'], 'udieresiscaron': ['u', 'udieresis.component'], 'thinspace': [], 'gturnedinsular': [], 'alphavaria': ['alpha', 'varia'], 'iota': [], 'dollar.alt1': [], 'uniAB63': [], 'Macute': ['M', 'acute'], 'imod': [], 'aringbelow': ['a', 'ringbelow'], 'tail.component': [], 'EReversedmod': [], 'Idieresis.component': [], 'uni2321': [], 'hmod': [], 'tbar': [], 'uni2534': [], 'Epsilontonos': ['E', 'tonos-uc'], 'Adotaccent': ['A', 'dotaccent'], 'omegadasiavariaypogegrammeni': ['omega', 'dasiavaria', 'prosgegrammeni'], 'Pedescender-cy.component': [], 'etaypogegrammeni': ['eta', 'prosgegrammeni'], 'ui': [], 'seveninferior': ['seven.numr'], 'three.numr': [], 'omacrongrave': ['o', 'gravecomb.component1'], 'koronis': [], 'dpalatalhook.component': [], 'Ddotbelow': ['D', 'dotbelowcomb'], 'etavariaypogegrammeni': ['eta', 'varia', 'prosgegrammeni'], 'Ydotaccent': ['Y', 'dotaccent'], 'Uinvertedbreve': ['U', 'perispomeni'], 'Ugrave': ['U', 'grave'], 'En-cy': ['H'], 'dotmiddle.component': [], 'gobliquestroke': ['g'], 'ocircumflextilde': ['o', 'tildecomb.component'], 'Wmod': [], 'sigmafinal': [], 'middledoublegraveaccentmod': ['dblgravecomb'], 'ucomb': [], 'abreveacute': ['a', 'abreve.component'], 'Ereversed': [], 'chedescenderabkhasian-cy': ['cheabkhasian-cy', 'chedescenderabkhasian-cy.component'], 'iotadieresis': ['iota', 'dieresis'], 'righttoleftembedding': [], 'Ymacron': ['Y', 'firsttonechinese'], 'ocircumflexgrave': ['o', 'gravecomb.component'], 'uni2502': [], 'omicronvaria': ['o', 'varia'], 'uni2584': [], 'tcedilla': ['t', 'cedilla'], 'upsilonpsilivaria': ['upsilon', 'psilivaria'], 'Umacron-cy': ['U-cy', 'macron'], 'Ef-cy': [], 'alpha': [], 'Umacrondieresis': ['U', 'Umacron.component'], 'Utilde': ['U', 'tilde'], 'Upsilondasiavaria': ['Y', 'dasiavaria-uc'], 'verticallinebelowcomb': ['verticallinemod'], 'RumRotunda': [], 'three.tnum': [], 'adieresismacron': ['a', 'macroncomb.component'], 'ndescender': ['n'], 'gmod': [], 'graphemejoinercomb': [], 'Rcommaaccent': ['R', 'cedillacomb.component'], 'iotatonos': ['iota', 'tonos'], 'Ohorntilde': ['Ohorn', 'tilde'], 'H': [], 'endescender-cy': [], 'uni2510': [], 'Mturnedsmall': [], 'Olongstroke': ['O'], 'Odotaccentmacron': ['O', 'macroncomb.component1'], 'Oslashacute': ['Oslash', 'acute'], 'diamondBlackSuit': [], 'lretroflexhookmod': [], 'fengdigraph': [], 'Eth': [], 'hlinebelow': ['h', 'macronbelow'], 'lretroflexhookandbelt': [], 'Acaron': ['A', 'caron'], 'rhopsili': ['rho', 'psili'], 'iigrave-cy': ['ii-cy', 'grave'], 'M': [], 'ka-cy': ['kgreenlandic'], 'adieresis-cy': ['a', 'dieresis'], 'nlefthookmod': [], 'tcurl': [], 'Rrotunda': [], 'ninesuperior': ['nine.numr'], 'omicronoxia': ['o', 'oxia'], 'Ha-cy': ['X'], 'jmod': [], 'Aringbelow': ['A', 'ringbelow'], 'thousand-cy': [], 'ie-cy': ['e'], 'aacute': ['a', 'acute'], 'Iotapsiliperispomeni': ['I', 'psiliperispomeni-uc'], 'Gobliquestroke': ['G'], 'iretroflexhook': ['i', 'aretroflexhook.component'], 'Wsmall': ['w'], 'idotlessstroke': [], 'ngrave': ['n', 'grave'], 'gcircumflex': ['g', 'circumflex'], 'backslash': [], 'is': [], 'plusminus': [], 'uni047B': [], 'Kastroke-cy': [], 'zero.numr': [], 'currency': [], 'oneeighth': ['one.numr', 'fraction', 'eight.numr'], 'uni047A': [], 'S': [], 'DZ': ['D', 'Z'], 'rdoublecrossedtail': [], 'uni253c': [], 'kcaron': ['k', 'caron'], 'Adieresis-cy': ['A', 'dieresis'], 'Ustrait-cy': ['Y'], 'leftBlackPointer': [], 'guillemetleft': [], 'cedillacomb.component': [], 'tonebarhighmod': [], 'minussuperior': ['minus.component'], 'colontriangularhalfmod': [], 'zhook': [], 'Umacron': ['U', 'macron'], 'asciitilde': [], 'uiturned': [], 'Dlinebelow': ['D', 'macronbelow'], 'Ghook': [], 'taillessphi': [], 'leftRightArrow': [], 'rsubscript': ['rmod'], 'iTurnedmod': [], 'uni2310': [], 'Tbar': [], 'etavaria': ['eta', 'varia'], 'lcircumflexbelow': ['l', 'circumflexbelow'], 'Hsmall': ['en-cy'], 'pokrytiecomb-cy': [], 'Vturned': ['Lambda'], 'fita-cy': [], 'Omicrondasia': ['O', 'dasia-uc'], 'five.tnum': [], 'acircumflex': ['a', 'circumflex'], 'dasiaperispomeni-uc': [], 'elementoflonghorizontalstroke': [], 'estimated': [], 'Q': [], 'omegaoxiaypogegrammeni': ['omega', 'oxia', 'prosgegrammeni'], 'zero.blackCircled': [], 'AY': [], 'alphadasiaypogegrammeni': ['alpha', 'dasia', 'prosgegrammeni'], 'Kcaron': ['K', 'caron'], 'emdash': [], 'Ghestroke-cy': [], 'gravedottedcomb': [], 'yerudieresis-cy': ['yeru-cy', 'dieresis'], 'Abreveacute': ['A', 'Abreve.component'], 'Gedescender-cy': [], 'Chedescenderabkhasian-cy': ['Cheabkhasian-cy', 'Chedescenderabkhasian-cy.component'], 'KaiSymbol': [], 'nbspace': [], 'Sacutedotaccent': ['S', 'Sacute.component'], 'henghook': [], 'psili': [], 'punctuationspace': [], 'ccircumflex': ['c', 'circumflex'], 'dblarchinvertedbelowcomb': [], 'rightBlackPointer': [], 'uni2551': [], 'Au': [], 'Obarred-cy': [], 'iotadialytikaperispomeni': ['iota', 'dialytikaperispomeni'], 'Wcircumflex': ['W', 'circumflex'], 'fourthtonechinese': ['grave'], 'ccaron': ['c', 'caron'], 'rupeeIndian': [], 'dzeabkhasian-cy': ['ezh'], 'p': [], 'oopen': [], 'Gamma': [], 'twostroke': [], 'emacronacute': ['e', 'acutecomb.component1'], 'Ccedilla': ['C', 'cedilla'], 'Ograve': ['O', 'grave'], 'braceleft': [], 'hdescender': [], 'UpsilondieresishookSymbol': ['UpsilonhookSymbol', 'dieresis'], 'retroflexhookcomb': [], 'OE': [], 'dasiapneumatacomb-cy': ['dasia'], 'abreve-cy': ['a', 'brevecomb.component'], 'two.pnum_enclosingkeycapcomb': [], 'Khook': [], 'Lhighstroke': [], 'omega-latin': ['omega'], 'Emtail-cy': ['M', 'tail.component'], 'oeVolapuk': [], 'aretroflexhook.component': [], 'rfishhookmiddletilde': ['rfishhook'], 'bdotaccent': ['b', 'dotaccent'], 'Idieresisacute': ['I', 'Idieresis.component'], 'Acircumflexacute': ['A', 'acutecomb.component'], 'eight.pnum_enclosingkeycapcomb': [], 'SigmaLunateSymbol': [], 'Tetse-cy': [], 'hdotbelow': ['h', 'dotbelowcomb'], 'Koppa-cy': [], 'enspace': [], 'uni251c': [], 'aring': ['a', 'ring'], 'abreve.component1': [], 'Zcaron': ['Z', 'caron'], 'aie-cy': ['ae'], 'psilivaria-uc': [], 'Sinsular': [], 'Ngrave': ['N', 'grave'], 'Ehookabove': ['E', 'hookabovecomb'], 'rhookturnedmod': [], 'Pflourish': [], 'Endescender-cy': [], 'Hbarmod': [], 'arrowleftrightbelowcomb': [], 'zretroflexhook': [], 'trademark': [], 'tonebarextralowmod': [], 'Abreve': ['A', 'breve'], 'aschwareversed': [], 'etaperispomeni': ['eta', 'perispomeni'], 'figurespace': [], 'oemod': [], 'te-cy': [], 'emquad': [], 'Stigma': [], 'uSidewaysmod': [], 'Epsilonoxia': ['E', 'oxia-uc'], 'udieresismacron': ['u', 'macroncomb.component'], 'rlongleg': [], 'Alphaturned-latin': [], 'Blinebelow': ['B', 'macronbelow'], 'koppaArchaic': [], 'Otilde.component': [], 'arrowheadleftabovecomb': [], 'jstroke': ['j'], 'usubscript': ['umod'], 'OUmod': [], 'OUsmall': [], 'uni2640': [], 'dasia-uc': [], 'iotavaria': ['iota', 'varia'], 'twosuperior': ['two.numr'], 'ellipsis': [], 'jsubscript': [], 'etaoxiaypogegrammeni': ['eta', 'oxia', 'prosgegrammeni'], 'Dsmall': [], 'Shcha-cy': [], 'Ohorngrave': ['Ohorn', 'grave'], 'Otilde': ['O', 'tilde'], 'Abrevegrave': ['A', 'Abreve.component1'], 'SigmaLunateReversedSymbol': [], 'Ssmall': [], 'two': [], 'acutecomb.component5': [], 'Omegavaria': ['Ohm', 'varia-uc'], 'etadasiaypogegrammeni': ['eta', 'dasia', 'prosgegrammeni'], 'hardsign-cy': [], 'jdotlessstroke': [], 'Epsilondasiaoxia': ['E', 'dasiaoxia-uc'], 'Lcircumflexbelow': ['L', 'circumflexbelow'], 'Alphapsilivariaprosgegrammeni': ['A', 'psilivaria-uc', 'prosgegrammeni'], 'enhook-cy': [], 'Esh': ['Sigma'], 'glottalstopreversedsuperior': ['glottalstopreversedmod'], 'ao': [], 'mcrossedtail': [], 'seven.blackCircled': [], 'oslash': [], 'Ohungarumlaut': ['O', 'hungarumlaut'], 'ringhalfleftcentered': ['ringhalfleft'], 'gamma-latin': [], 'semisoftsign-cy': [], 'Shima-coptic': [], 'acutecomb.component': [], 'Amod': [], 'r.salt': [], 'NJ': ['N', 'J'], 'whiteSmallSquare': [], 'xlowrightring': [], 'Bmod': [], 'etaoxia': ['eta', 'oxia'], 'Udieresisbelow': ['U', 'dieresisbelow'], 'upsilonpsili': ['upsilon', 'psili'], 'Adieresismacron': ['A', 'macroncomb.component'], 'ecedilla': ['e', 'cedilla'], 'esdescender-cy': [], 'kahook-cy': [], 'udieresisgrave': ['u', 'gravecomb.component3'], 'sheqel': [], 'omacron': ['o', 'macron'], 'Alphaprosgegrammeni': ['A', 'prosgegrammeni'], 'Ocircumflextilde': ['O', 'tildecomb.component'], 'itildebelow': ['i', 'tildebelow'], 'parenrightsuperior': ['parenright.component'], 'Lacute': ['L', 'acute'], 'Usmallmod': [], 'Ocircumflexacute': ['O', 'acutecomb.component'], 'cheabkhasian-cy': [], 'ze-cy': [], 'xlongleftlegserif': [], 'odieresis-cy': ['o', 'dieresis'], 'macroncomb.component': [], 'fStroke': ['f'], '.notdef': [], 'rhoSymbol': [], 'omegapsiliypogegrammeni': ['omega', 'psili', 'prosgegrammeni'], 'kmod': [], 'Idotaccent': ['I', 'dotaccent'], 'iotapsili': ['iota', 'psili'], 'kappaSymbol': [], 'rho': [], 'omegavariaypogegrammeni': ['omega', 'varia', 'prosgegrammeni'], 'plus.component': [], 'acircumflexdotbelow': ['a', 'circumflex', 'dotbelowcomb'], 'Bhook': [], 'dzcaron': ['d', 'z', 'caron'], 'Psi-cy': [], 'tccurl': [], 'Alphamacron': ['A', 'macroncomb'], 'righttackbelowcomb': [], 'Tdiagonalstroke': ['T', 'Astroke.component'], 'sevensuperior': ['seven.numr'], 'lslash': [], 'Heta': [], 'av': [], 'Zdotbelow': ['Z', 'dotbelowcomb'], 'hastroke-cy': [], 'hori-coptic': [], 'wring': ['w', 'ring'], 'Uhornhookabove': ['Uhorn', 'hookabovecomb'], 'Uk-cy': [], 'cdotaccent': ['c', 'dotaccent'], 'daggerdbl': [], 'Tedescender-cy': [], 'P': [], 'alphadasiaperispomeni': ['alpha', 'dasiaperispomeni'], 'Rinsular': [], 'northEastArrow': [], 'sdotaccent': ['s', 'dotaccent'], 'oxia': [], 'smod': [], 'dum': ['d'], 'er-cy': ['p'], 'yshortrightleg': [], 'Fhook': [], 'bpalatalhook': ['b', 'bpalatalhook.component'], 'eopenreversedhook': [], 'Ndotbelow': ['N', 'dotbelowcomb'], 'rdblgrave': ['r', 'dblgravecomb'], 'alphavrachy': ['alpha', 'breve'], 'ibreve': ['idotless', 'breve'], 'Cheverticalstroke-cy': ['Che-cy'], 'omicronpsilivaria': ['o', 'psilivaria'], 'KoppaArchaic': [], 'Itilde': ['I', 'tilde'], 'fei-coptic': [], 'Iebreve-cy': ['E', 'brevecomb.component'], 'thornstroke': ['thorn'], 'ecircumflex': ['e', 'circumflex'], 'Alphapsilivaria': ['A', 'psilivaria-uc'], 'z': [], 'Softsign-cy': [], 'omegadasia': ['omega', 'dasia'], 'uni2555': [], 'isubscript': [], 'ubar': ['u'], 'dtopbar': [], 'Rcaron': ['R', 'caron'], 'mill': ['m'], 'Nsmallmodifier': [], 'pacute': ['p', 'acute'], 'uni263b': [], 'lefttackbelowcomb': [], 'macronacutecomb': ['firsttonechinese', 'acute'], 'uniAB61': [], 'Itildebelow': ['I', 'tildebelow'], 'Omicronpsilioxia': ['O', 'psilioxia-uc'], 'Mdotbelow': ['M', 'dotbelowcomb'], 'gravebelowcomb': ['grave'], 'longsdotaccent': ['longs', 'dotaccent'], 'ostroke-blackletter': [], 'uni2558': [], 'Oogonek': ['O', 'ogonek'], 'Pmod': [], 'Theta': [], 'rlinebelow': ['r', 'macronbelow'], 'umacron-cy': ['y', 'macron'], 'firsttonechinese': [], 'quoteleft': [], 'io-cy': ['e', 'dieresis'], 'dblverticallineabovecomb': [], 'thornstrokethroughdescender': ['thorn'], 'odotaccentmacron': ['o', 'macroncomb.component1'], 'tildeverticalcomb': [], 'unif001': ['fi'], 'Ezh': [], 'eTurnedopen': [], 'Vmod': [], 'eopenreversed': [], 'Kdiagonalstroke': ['K'], 'aretroflexhook': ['a'], 'N': [], 'shei-coptic': [], 'etilde': ['e', 'tilde'], 'chedieresis-cy': ['che-cy', 'dieresis'], 'IJ': ['I', 'J'], 'beta-latin': ['beta'], 'D': [], 'Psquirreltail': [], 'nj': ['n', 'j'], 'phiSymbol': [], 'Udblgrave': ['U', 'dblgravecomb'], 'sacutedotaccent': ['s', 'sacute.component'], 'dezh': [], 'gdotaccent': ['g', 'dotaccent'], 'six.pnum_enclosingkeycapcomb': [], 'beginlowtonemod': [], 'Rdblgrave': ['R', 'dblgravecomb'], 'i': [], 'acutetonecomb': ['acute'], 'alphaperispomeniypogegrammeni': ['alpha', 'perispomeni', 'prosgegrammeni'], 'Alphadasiaperispomeni': ['A', 'dasiaperispomeni-uc'], 'vcomb': [], 'Utildeacute': ['U', 'acutecomb.component3'], 'Omicronpsilivaria': ['O', 'psilivaria-uc'], 'cstretched': [], 'upsilonperispomeni': ['upsilon', 'perispomeni'], 'spalatalhook': ['s', 'dpalatalhook.component', 'gpalatalhook.component'], 'Scaron.component': [], 'zerowidthjoiner': [], 'lcurl': [], 'tetse-cy': [], 'Lambda': [], 'asteriskabovecomb': ['asterisk'], 'Uacute': ['U', 'acute'], 'ertick-cy': ['p'], 'mTurnedmod': [], 'enghe-cy': [], 'acircumflexacute': ['a', 'acutecomb.component'], 'aemacron': ['ae', 'macron'], 'enotch': [], 'phook': [], 'Iegrave-cy': ['E', 'grave'], 'e': [], 'idieresis': ['idotless', 'dieresis'], 'twoinferior': ['two.numr'], 'lira': [], 'psili-uc': [], 'uniAB62': [], 'Vdiagonalstroke': ['V'], 'Uhornacute': ['Uhorn', 'acute'], 'gammamod-latin': [], 'epsilondasiavaria': ['epsilon', 'dasiavaria'], 'etadasiaoxia': ['eta', 'dasiaoxia'], 'Jmod': [], 'numbersign_enclosingkeycapcomb': [], 'oSideways': [], 'wdotbelow': ['w', 'dotbelowcomb'], 'Zsmall': ['z'], 'verticallinemod': [], 'xinferior': ['xmod'], 'Alphapsiliperispomeni': ['A', 'psiliperispomeni-uc'], 'lbelt': [], 'odotbelow': ['o', 'dotbelowcomb'], 'six.dnom': ['six.numr'], 'rturned': [], 'uni255a': [], 'yangdepartingtone': [], 'btopbar': [], 'Omacron': ['O', 'macron'], 'Pe-cy': ['Pi'], 'otilde.component': [], 'threesuperior': ['three.numr'], 'longshighstroke': [], 'aeTurned': [], 'ringhalfrightcentered': ['ringhalfright'], 'Abreve.component2': [], 'Odblgrave': ['O', 'dblgravecomb'], 'etapsili': ['eta', 'psili'], 'Hmod': [], 'scircumflex': ['s', 'circumflex'], 'sixsuperior': ['six.numr'], 'xi': [], 'lhookretroflex': [], 'onetenth': ['one.numr', 'fraction', 'one.dnom', 'zero.dnom'], 'omegapsili': ['omega', 'psili'], 'livreTournois': [], 'heartWhiteSuit': [], 'odblgrave': ['o', 'dblgravecomb'], 'popdirectionalformatting': [], 'eflourish': [], 'Izhitsa-cy': [], 'psilipneumatacomb-cy': ['psili'], 'xbelowcomb': [], 'iebreve-cy': ['e', 'brevecomb.component'], 'ygrave': ['y', 'grave'], 'EreversedOpen': ['Ze-cy'], 'emacron': ['e', 'macron'], 'Epsilonpsilioxia': ['E', 'psilioxia-uc'], 'ustraitstroke-cy': [], 'Omicrondasiaoxia': ['O', 'dasiaoxia-uc'], 'alphavariaypogegrammeni': ['alpha', 'varia', 'prosgegrammeni'], 'ramshorn': [], 'r': [], 'rightArrow': [], 'ushortrightleg': [], 'nine': [], 'Upsilonvrachy': ['Y', 'brevecomb'], 'Etapsilioxiaprosgegrammeni': ['H', 'psilioxia-uc', 'prosgegrammeni'], 'enquad': [], 'Iotadieresis': ['I', 'dieresis'], 'summation': [], 'zmiddletilde': ['z'], 'aringacute': ['a', 'ring', 'acute'], 'ghestroke-cy': [], 'vdotbelow': ['v', 'dotbelowcomb'], 'Etadasiaperispomeniprosgegrammeni': ['H', 'dasiaperispomeni-uc', 'prosgegrammeni'], 'Dhook': [], 'sterling': [], 'v': [], 'gje-cy': ['ge-cy', 'acute'], 'omegapsilivariaypogegrammeni': ['omega', 'psilivaria', 'prosgegrammeni'], 'tcommaaccent': ['t', 'cedillacomb.component'], 'dcaron': ['d', 'caronvert.component'], 'alphamacron': ['alpha', 'macroncomb'], 'secondtonechinese': ['acute'], 'ohornhookabove': ['ohorn', 'hookabovecomb'], 'tinsular': [], 'ThetaSymbol': ['Obarred-cy'], 'xlongleftleg': [], 'ain-egyptological': [], 'ecircumflexgrave': ['e', 'gravecomb.component'], 'ecircumflexbelow': ['e', 'circumflexbelow'], 'one_zero.blackCircled': [], 'ustroke': [], 'beta': [], 'odieresis': ['o', 'dieresis'], 'naira': [], 'zerowidthspace': [], 'aeTurnedmod': [], 'wdieresis': ['w', 'dieresis'], 'Fsmall': [], 'Kje-cy': ['K', 'acute'], 'alpharetroflexhook': ['alpha-latin'], 'uniFB05': [], 'omegaoxia': ['omega', 'oxia'], 'Hdotaccent': ['H', 'dotaccent'], 'Epsilonpsili': ['E', 'psili-uc'], 'hcaron': ['h', 'caron'], 'ring': [], 'slashshortcomb': [], 't': [], 'Sacute.component': [], 'commaaboverightcomb': ['psili'], 'doublemacroncomb': [], 'upsilondieresis': ['upsilon', 'dieresis'], 'paragraph': [], 'voicingmod': ['caron'], 'dollar': [], 'euro-currency': [], 'Ocircumflexhookabove': ['O', 'hookabovecomb.component'], 'lowernumeral-greek': [], 'Uhungarumlaut': ['U', 'hungarumlaut'], 'izhitsa-cy': [], 'kacute': ['k', 'acute'], 'Dcircumflexbelow': ['D', 'circumflexbelow'], 'Tonesix': [], 'dmiddletilde': ['d'], 'epsilondasiaoxia': ['epsilon', 'dasiaoxia'], 'numbersign': [], 'minusinferior': ['minus.component'], 'ocomb': [], 'AEmacron': ['AE', 'macron'], 'psiliperispomeni-uc': [], 'etadasia': ['eta', 'dasia'], 'Tonetwo': [], 'emacrongrave': ['e', 'gravecomb.component1'], 'Em-cy': ['M'], 'F': [], 'schwamod': [], 'omicrondasiaoxia': ['o', 'dasiaoxia'], 'Fei-coptic': [], 'Zacute': ['Z', 'acute'], 'creverseddot': ['sigmaLunateDottedReversedSymbol'], 'Ohorn': [], 'j': [], 'literSign': [], 'Io-cy': ['E', 'dieresis'], 'omegadasiaperispomeniypogegrammeni': ['omega', 'dasiaperispomeni', 'prosgegrammeni'], 'verticalfourdots': ['period', 'period', 'period', 'period'], 'Pamphyliandigamma': ['Ii-cy'], 'Hastroke-cy': [], 'Iinvertedbreve': ['I', 'perispomeni'], 'e-cy': [], 'zcurlmod': [], 'stigma': [], 'Kobliquestroke': ['K'], 'ocircumflex': ['o', 'circumflex'], 'Jstroke': ['J'], 'nine.pnum_enclosingkeycapcomb': [], 'Lslash': [], 'nobliquestroke': ['n'], 'Iotadasiaperispomeni': ['I', 'dasiaperispomeni-uc'], 'Sdotbelowdotaccent': ['S', 'dotaccent', 'dotbelowcomb'], 'Iigrave-cy': ['Ii-cy', 'grave'], 'prosgegrammeni': [], 'acomb': [], 'tonebarlowmod': [], 'sacute': ['s', 'acute'], 'macronlowmod': [], 'oBottomhalf': [], 'tav-hb': [], 'Oloop': [], 'zstroke': [], 'eopenclosed': [], 'hbar': [], 'arrowheadrightabovecomb': ['lowrightarrowheadmod'], 'Etadasiaperispomeni': ['H', 'dasiaperispomeni-uc'], 'uni255c': [], 'gravemacroncomb': ['firsttonechinese', 'grave'], 'gcaron': ['g', 'caron'], 'Udieresismacron': ['U', 'macroncomb.component'], 'glottalstopreversedmod': [], 'Omegadasiaperispomeni': ['Ohm', 'dasiaperispomeni-uc'], 'Alphadasiaoxiaprosgegrammeni': ['A', 'dasiaoxia-uc', 'prosgegrammeni'], 'guillemetright': [], 'macron': [], 'Er-cy': ['P'], 'caroncomb': [], 'lezh': [], 'iotamod': [], 'commareversedmod': [], 'Whook': [], 'caronvert.component': ['cedillacomb.component'], 'iotavrachy': ['iota', 'brevecomb'], 'dotbelowcomb': [], 'caron': [], 'Omegapsilivaria': ['Ohm', 'psilivaria-uc'], 'Kstrokediagonalstroke': ['K'], 'Otilde.component1': [], 'epsilondasia': ['epsilon', 'dasia'], 'uptackbelowcomb': ['uptackmod'], 'etadasiaperispomeniypogegrammeni': ['eta', 'dasiaperispomeni', 'prosgegrammeni'], 'three.blackCircled': [], 'OO': [], 'alphapsilioxia': ['alpha', 'psilioxia'], 'blackCircle': [], 'parenright': [], 'Upsilonvaria': ['Y', 'varia-uc'], 'tau': [], 'Ahookabove': ['A', 'hookabovecomb'], 'Ldotbelow': ['L', 'dotbelowcomb'], 'alphapsilivaria': ['alpha', 'psilivaria'], 'uni255b': [], 'Ecircumflexdotbelow': ['E', 'circumflex', 'dotbelowcomb'], 'endhightonemod': [], 'Gcaron': ['G', 'caron'], 'crossaccentmod': [], 'idieresis.component': [], 'eth': [], 'Omegapsiliprosgegrammeni': ['Ohm', 'psili-uc', 'prosgegrammeni'], 'yogh': [], 'theta': [], 'idotbelow': ['i', 'dotbelowcomb'], 'lj': ['l', 'j'], 'Omegapsili': ['Ohm', 'psili-uc'], 'alphapsilioxiaypogegrammeni': ['alpha', 'psilioxia', 'prosgegrammeni'], 'uni2590': [], 'LstrokeSmall': [], 'avhorizontalbar': [], 'greater': [], 'Gacute': ['G', 'acute'], 'ystroke': ['y'], 'ldoublemiddletilde': ['l'], 'one.blackCircled': [], 'Yhook': ['UpsilonhookSymbol'], 'orthogonal': [], 'ratio': [], 'fl': [], 'mpalatalhook': ['m', 'dpalatalhook.component'], 'ndotaccent': ['n', 'dotaccent'], 'Dzhe-cy': [], 'clubBlackSuit': [], 'lessequal': [], 'Alphadasiaoxia': ['A', 'dasiaoxia-uc'], 'o-cy': ['o'], 'Lbelt': [], 'omod': [], 'clicklateral': ['bar', 'bar'], 'el-cy': [], 'saltillo': ['quotesingle'], 'drachma': [], 'Ustraitstroke-cy': [], 'uni2561': [], 'kpalatalhook': ['k', 'dpalatalhook.component'], 'tpalatalhook': [], 'copyright': [], 'rdouble': [], 'iTurned': [], 'che-cy': [], 'lsdigraph': []}
    # Now fill them into the GLYPH_DATA
    for gName, components in USED_COMPONENTS.items():
        gd = GLYPH_DATA[gName]
        if not components:
            gd.base = None
            gd.accents = []
        else:
            gd.base = components[0]
            gd.accents = components[1:]

    #gd = GLYPH_DATA['eacute']
    #print(gd.name, gd.base, gd.accents)

    # Add needed anchors
    TOP_ = 'top'
    MIDDLE_ = 'middle'
    BOTTOM_ = 'bottom'
    OGONEK_ = 'ogonek'
    DOT_ = 'dot'
    TONOS_ = 'tonos'
    VERT_ = 'vert'

    _TOP = '_top'
    _MIDDLE = '_middle'
    _BOTTOM = '_bottom'
    _OGONEK = '_ogonek'
    _DOT = '_dot'
    _TONOS = '_tonos'
    _VERT = '_vert'

    TOP_ANCHORS = ['A', 'A-cy', 'AE', 'AEacute', 'AEmacron', 'Aacute', 'Abreve', 'Abreve-cy', 'Abreve.component', 'Abreve.component1', 'Abreve.component2', 
        'Abreve.component3', 'Abreveacute', 'Abrevedotbelow', 'Abrevegrave', 'Abrevehookabove', 'Abrevetilde', 'Acaron', 'Acircumflex', 'Acircumflexacute', 
        'Acircumflexdotbelow', 'Acircumflexgrave', 'Acircumflexhookabove', 'Acircumflextilde', 'Adblgrave', 'Adieresis', 'Adieresis-cy', 'Adieresismacron', 
        'Adotaccent', 'Adotbelow', 'Adotmacron', 'Agrave', 'Ahookabove', 'Aie-cy', 'Ainvertedbreve', 'Alpha', 'Alphadasia', 'Alphadasiaoxia', 
        'Alphadasiaoxiaprosgegrammeni', 'Alphadasiaperispomeni', 'Alphadasiaperispomeniprosgegrammeni', 'Alphadasiaprosgegrammeni', 'Alphadasiavaria', 
        'Alphadasiavariaprosgegrammeni', 'Alphamacron', 'Alphaoxia', 'Alphaprosgegrammeni', 'Alphapsili', 'Alphapsilioxia', 'Alphapsilioxiaprosgegrammeni', 
        'Alphapsiliperispomeni', 'Alphapsiliperispomeniprosgegrammeni', 'Alphapsiliprosgegrammeni', 'Alphapsilivaria', 'Alphapsilivariaprosgegrammeni', 
        'Alphatonos', 'Alphavaria', 'Alphavrachy', 'Amacron', 'Aogonek', 'Aring', 'Aringacute', 'Aringbelow', 'Astroke', 'Atilde', 'B', 'Bdotaccent', 'Bdotbelow', 
        'Beta', 'Blinebelow', 'Bstroke', 'C', 'Cacute', 'Cbar', 'Ccaron', 'Ccedilla', 'Ccedillaacute', 'Ccircumflex', 'Cdotaccent', 'Che-cy', 'Chedieresis-cy', 
        'Cheverticalstroke-cy', 'Chi', 'Chi-latin', 'Csmall', 'Cstroke', 'D', 'DZ', 'DZcaron', 'Dcaron', 'Dcedilla', 'Dcircumflexbelow', 'Ddotaccent', 'Ddotbelow', 
        'Dlinebelow', 'Dz', 'Dzcaron', 'Dze-cy', 'E', 'Eacute', 'Ebreve', 'Ecaron', 'Ecedilla', 'Ecedillabreve', 'Ecircumflex', 'Ecircumflexacute', 'Ecircumflexbelow', 
        'Ecircumflexdotbelow', 'Ecircumflexgrave', 'Ecircumflexhookabove', 'Ecircumflextilde', 'Edblgrave', 'Edieresis', 'Edieresis-cy', 'Edotaccent', 'Edotbelow', 
        'Egrave', 'Ehookabove', 'Einvertedbreve', 'Em-cy', 'Emacron', 'Emacronacute', 'Emacrongrave', 'Emtail-cy', 'En-cy', 'Entail-cy', 'Eogonek', 'Epsilon', 'Epsilondasia', 
        'Epsilondasiaoxia', 'Epsilondasiavaria', 'Epsilonoxia', 'Epsilonpsili', 'Epsilonpsilioxia', 'Epsilonpsilivaria', 'Epsilontonos', 'Epsilonvaria', 'Er-cy', 
        'Ereversed-cy', 'EreversedOpen', 'Es-cy', 'Estroke', 'Eta', 'Etadasia', 'Etadasiaoxia', 'Etadasiaoxiaprosgegrammeni', 'Etadasiaperispomeni', 
        'Etadasiaperispomeniprosgegrammeni', 'Etadasiaprosgegrammeni', 'Etadasiavaria', 'Etadasiavariaprosgegrammeni', 'Etaoxia', 'Etaprosgegrammeni', 
        'Etapsili', 'Etapsilioxia', 'Etapsilioxiaprosgegrammeni', 'Etapsiliperispomeni', 'Etapsiliperispomeniprosgegrammeni', 'Etapsiliprosgegrammeni', 
        'Etapsilivaria', 'Etapsilivariaprosgegrammeni', 'Etatonos', 'Etavaria', 'Etilde', 'Etildebelow', 'Ezh', 'Ezhcaron', 'F', 'Fdotaccent', 'G', 'Gacute', 
        'Gamma', 'Gbreve', 'Gcaron', 'Gcircumflex', 'Gcommaaccent', 'Gdotaccent', 'Ge-cy', 'Gje-cy', 'Gmacron', 'Gobliquestroke', 'H', 'Ha-cy', 'Hbrevebelow', 
        'Hcaron', 'Hcedilla', 'Hcircumflex', 'Hdieresis', 'Hdotaccent', 'Hdotbelow', 'I', 'I-cy', 'IJ', 'Iacute', 'Ibreve', 'Icaron', 'Icircumflex', 'Idblgrave', 
        'Idieresis', 'Idieresis-cy', 'Idieresis.component', 'Idieresisacute', 'Idotaccent', 'Idotbelow', 'Ie-cy', 'Iebreve-cy', 'Iegrave-cy', 'Igrave', 'Ihookabove', 
        'Ii-cy', 'Iigrave-cy', 'Iinvertedbreve', 'Iishort-cy', 'Imacron', 'Imacron-cy', 'Io-cy', 'Iogonek', 'Iota', 'Iotadasia', 'Iotadasiaoxia', 'Iotadasiaperispomeni', 
        'Iotadasiavaria', 'Iotadieresis', 'Iotamacron', 'Iotaoxia', 'Iotapsili', 'Iotapsilioxia', 'Iotapsiliperispomeni', 'Iotapsilivaria', 'Iotatonos', 'Iotavaria', 
        'Iotavrachy', 'Itilde', 'Itildebelow', 'Izhitsa-cy', 'Izhitsadblgrave-cy', 'J', 'Jcircumflex', 'Je-cy', 'Jstroke', 'K', 'Ka-cy', 'Kacute', 'Kappa', 'Kcaron', 
        'Kcommaaccent', 'Kdiagonalstroke', 'Kdotbelow', 'Kje-cy', 'Klinebelow', 'Kobliquestroke', 'Ksmall', 'Kstroke', 'Kstrokediagonalstroke', 'L', 'LJ', 'Lacute', 
        'Lbar', 'Lcaron', 'Lcircumflexbelow', 'Lcommaaccent', 'Ldot', 'Ldotbelow', 'Ldotbelowmacron', 'Ldoublebar', 'Lj', 'Llinebelow', 'Lmiddletilde', 'M', 'Macute', 
        'Mdotaccent', 'Mdotbelow', 'Mu', 'N', 'NJ', 'Nacute', 'Ncaron', 'Ncircumflexbelow', 'Ncommaaccent', 'Ndescender', 'Ndotaccent', 'Ndotbelow', 'Ngrave', 'Nj', 
        'Nlinebelow', 'Nobliquestroke', 'NreversedSmall', 'Ntilde', 'Nu', 'O', 'O-cy', 'OE', 'Oacute', 'Obarred-cy', 'Obarreddieresis-cy', 'Obreve', 'Ocaron', 
        'Ocircumflex', 'Ocircumflexacute', 'Ocircumflexdotbelow', 'Ocircumflexgrave', 'Ocircumflexhookabove', 'Ocircumflextilde', 'Odblgrave', 'Odieresis', 'Odieresis-cy', 
        'Odieresismacron', 'Odotaccent', 'Odotaccentmacron', 'Odotbelow', 'Ograve', 'Ohm', 'Ohookabove', 'Ohorn', 'Ohornacute', 'Ohorndotbelow', 'Ohorngrave', 'Ohornhookabove', 
        'Ohorntilde', 'Ohungarumlaut', 'Oinvertedbreve', 'Olongstroke', 'Omacron', 'Omacronacute', 'Omacrongrave', 'Omega', 'Omega-cy', 'Omegadasia', 'Omegadasiaoxia', 
        'Omegadasiaoxiaprosgegrammeni', 'Omegadasiaperispomeni', 'Omegadasiaperispomeniprosgegrammeni', 'Omegadasiaprosgegrammeni', 'Omegadasiavaria', 
        'Omegadasiavariaprosgegrammeni', 'Omegaoxia', 'Omegaprosgegrammeni', 'Omegapsili', 'Omegapsilioxia', 'Omegapsilioxiaprosgegrammeni', 'Omegapsiliperispomeni', 
        'Omegapsiliperispomeniprosgegrammeni', 'Omegapsiliprosgegrammeni', 'Omegapsilivaria', 'Omegapsilivariaprosgegrammeni', 'Omegatonos', 'Omegavaria', 'Omicron', 
        'Omicrondasia', 'Omicrondasiaoxia', 'Omicrondasiavaria', 'Omicronoxia', 'Omicronpsili', 'Omicronpsilioxia', 'Omicronpsilivaria', 'Omicrontonos', 'Omicronvaria', 
        'Oogonek', 'Oogonekmacron', 'Oslash', 'Oslashacute', 'Osmall', 'Otilde', 'Otilde.component', 'Otilde.component1', 'Otildeacute', 'Otildedieresis', 'Otildemacron', 
        'P', 'Pacute', 'Palochka-cy', 'Pamphyliandigamma', 'Pdotaccent', 'Pstroke', 'Pstrokethroughdescender', 'Q', 'Qstrokethroughdescender', 'R', 'Racute', 'Rcaron', 
        'Rcommaaccent', 'Rdblgrave', 'Rdotaccent', 'Rdotbelow', 'Rdotbelowmacron', 'Rho', 'Rhodasia', 'Rinvertedbreve', 'Rlinebelow', 'Robliquestroke', 'Rstroke', 
        'S', 'Sacute', 'Sacute.component', 'Sacutedotaccent', 'Scaron', 'Scaron.component', 'Scarondotaccent', 'Scedilla', 'Schwa', 'Schwa-cy', 
        'Schwadieresis-cy', 'Scircumflex', 'Scommaaccent', 'Sdotaccent', 'Sdotbelow', 'Sdotbelowdotaccent', 'SigmaLunateDottedSymbol', 'Sobliquestroke', 'T', 'Tau', 
        'Tcaron', 'Tcedilla', 'Tcircumflexbelow', 'Tcommaaccent', 'Tdiagonalstroke', 'Tdotaccent', 'Tdotbelow', 'Te-cy', 'ThetaSymbol', 'Tlinebelow', 'U', 'U-cy', 
        'Uacute', 'Ubar', 'Ubreve', 'Ucaron', 'Ucircumflex', 'Ucircumflexbelow', 'Udblgrave', 'Udieresis', 'Udieresis-cy', 'Udieresis.component', 'Udieresisacute', 
        'Udieresisbelow', 'Udieresiscaron', 'Udieresisgrave', 'Udieresismacron', 'Udotbelow', 'Ugrave', 'Uhookabove', 'Uhorn', 'Uhornacute', 'Uhorndotbelow', 
        'Uhorngrave', 'Uhornhookabove', 'Uhorntilde', 'Uhungarumlaut', 'Uhungarumlaut-cy', 'Uinvertedbreve', 'Umacron', 'Umacron-cy', 'Umacron.component', 'Umacrondieresis', 
        'Uogonek', 'Upsilon', 'UpsilonacutehookSymbol', 'Upsilondasia', 'Upsilondasiaoxia', 'Upsilondasiaperispomeni', 'Upsilondasiavaria', 'Upsilondieresis', 
        'UpsilondieresishookSymbol', 'UpsilonhookSymbol', 'Upsilonmacron', 'Upsilonoxia', 'Upsilontonos', 'Upsilonvaria', 'Upsilonvrachy', 'Uring', 'Ushort-cy', 
        'Ustrait-cy', 'Utilde', 'Utildeacute', 'Utildebelow', 'V', 'Vdiagonalstroke', 'Vdotbelow', 'Ve-cy', 'Vsmall', 'Vtilde', 'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 
        'Wdotaccent', 'Wdotbelow', 'Wgrave', 'Wsmall', 'X', 'Xdieresis', 'Xdotaccent', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ydotaccent', 'Ydotbelow', 'Yeru-cy', 
        'Yerudieresis-cy', 'Ygrave', 'Yhook', 'Yhookabove', 'Yi-cy', 'Ymacron', 'Yot', 'Ystroke', 'Ytilde', 'Z', 'Zacute', 'Zcaron', 'Zcircumflex', 'Zdotaccent', 
        'Zdotbelow', 'Ze-cy', 'Zedieresis-cy', 'Zeta', 'Zhe-cy', 'Zhebreve-cy', 'Zhedieresis-cy', 'Zlinebelow', 'Zsmall', 'a', 'a-cy', 'aacute', 'abreve', 'abreve-cy', 
        'abreve.component', 'abreve.component1', 'abreve.component2', 'abreve.component3', 'abreveacute', 'abrevedotbelow', 'abrevegrave', 'abrevehookabove', 'abrevetilde', 
        'acaron', 'acircumflex', 'acircumflexacute', 'acircumflexdotbelow', 'acircumflexgrave', 'acircumflexhookabove', 'acircumflextilde', 'acomb', 'acute', 'acutecomb', 
        'acutecomb.component', 'acutecomb.component1', 'acutecomb.component3', 'acutecomb.component5', 'acutedottedcomb', 'acutegraveacutecomb', 
        'acutemacroncomb', 'acutetonecomb', 'adblgrave', 'adieresis', 'adieresis-cy', 'adieresismacron', 'adotaccent', 'adotbelow', 'adotmacron', 'ae', 'aeacute', 'aemacron', 
        'agrave', 'ahookabove', 'aie-cy', 'ainvertedbreve', 'almostequaltoabovecomb', 'alpha', 'alphadasia', 'alphadasiaoxia', 'alphadasiaoxiaypogegrammeni', 
        'alphadasiaperispomeni', 'alphadasiaperispomeniypogegrammeni', 'alphadasiavaria', 'alphadasiavariaypogegrammeni', 'alphadasiaypogegrammeni', 'alphamacron', 
        'alphaoxia', 'alphaoxiaypogegrammeni', 'alphaperispomeni', 'alphaperispomeniypogegrammeni', 'alphapsili', 'alphapsilioxia', 'alphapsilioxiaypogegrammeni', 
        'alphapsiliperispomeni', 'alphapsiliperispomeniypogegrammeni', 'alphapsilivaria', 'alphapsilivariaypogegrammeni', 'alphapsiliypogegrammeni', 'alphatonos', 
        'alphavaria', 'alphavariaypogegrammeni', 'alphavrachy', 'alphaypogegrammeni', 'amacron', 'aogonek', 'aretroflexhook',  
        'arighthalfring', 'aring', 'aringacute', 'aringbelow', 'arrowheadleftabovecomb', 'arrowheadrightabovecomb', 'asteriskabovecomb', 'astroke', 'atilde', 'b', 
        'bdotaccent', 'bdotbelow', 'blinebelow', 'bmiddletilde', 'bpalatalhook', 'breve', 'brevecomb', 'brevecomb.component', 
        'breveinvertedcomb', 'breveinverteddoublecomb', 'c', 'cPalatalhook', 'cacute', 'candrabinducomb', 'caron', 'caroncomb', 'cbar', 'ccaron', 'ccedilla', 
        'ccedillaacute', 'ccircumflex', 'ccomb', 'cdotaccent', 'che-cy', 'chedieresis-cy', 'cheverticalstroke-cy', 'circumflex', 'circumflexcomb', 'commaabovecomb', 
        'commaaboverightcomb', 'commareversedabovecomb', 'commaturnedabovecomb', 'cstroke', 'd', 'dasia', 'dasiaoxia', 'dasiaperispomeni', 'dasiapneumatacomb-cy', 'dasiavaria', 
        'dblgravecomb', 'dbloverlinecomb', 'dblverticallineabovecomb', 'dcaron', 'dcedilla', 'dcircumflexbelow', 'dcomb', 'ddotaccent', 'ddotbelow', 'dialytikaoxia', 
        'dialytikaperispomeni', 'dialytikatonoscomb', 'dialytikavaria', 'dieresis', 'dieresiscomb', 'dieresistonos', 'dlinebelow', 'dmiddletilde', 'dotaboverightcomb', 
        'dotaccent', 'dotaccentcomb', 'doublebrevecomb', 'doublemacroncomb', 'dpalatalhook', 'dum', 'dz', 'dzcaron', 'dze-cy', 'dzeabkhasian-cy', 'e', 'eacute', 'ebreve', 
        'ecaron', 'ecedilla', 'ecedillabreve', 'ecircumflex', 'ecircumflexacute', 'ecircumflexbelow', 'ecircumflexdotbelow', 'ecircumflexgrave', 'ecircumflexhookabove', 
        'ecircumflextilde', 'ecomb', 'edblgrave', 'edieresis', 'edieresis-cy', 'edotaccent', 'edotbelow', 'egrave', 'ehookabove', 'einvertedbreve', 'emacron', 'emacronacute', 
        'emacrongrave', 'eogonek', 'eopen', 'eopenretroflexhook', 'eopenreversedretroflexhook', 'epsilon', 'epsilondasia', 'epsilondasiaoxia', 'epsilondasiavaria', 
        'epsilonoxia', 'epsilonpsili', 'epsilonpsilioxia', 'epsilonpsilivaria', 'epsilontonos', 'epsilonvaria', 'er-cy', 'eretroflexhook', 'ereversed-cy', 'ertick-cy', 
        'es-cy', 'estroke', 'eta', 'etadasia', 'etadasiaoxia', 'etadasiaoxiaypogegrammeni', 'etadasiaperispomeni', 'etadasiaperispomeniypogegrammeni', 'etadasiavaria', 
        'etadasiavariaypogegrammeni', 'etadasiaypogegrammeni', 'etaoxia', 'etaoxiaypogegrammeni', 'etaperispomeni', 'etaperispomeniypogegrammeni', 'etapsili', 'etapsilioxia', 
        'etapsilioxiaypogegrammeni', 'etapsiliperispomeni', 'etapsiliperispomeniypogegrammeni', 'etapsilivaria', 'etapsilivariaypogegrammeni', 'etapsiliypogegrammeni', 
        'etatonos', 'etavaria', 'etavariaypogegrammeni', 'etaypogegrammeni', 'etilde', 'etildebelow', 'eturned', 'ezh', 'ezhcaron', 'f', 'fStroke', 'fdotaccent', 'fermatacomb', 
        'firsttonechinese', 'flenis', 'fmiddletilde', 'fourthtonechinese', 'fpalatalhook', 'g', 'gacute', 'gbreve', 'gbridgeabovecomb', 'gcaron', 'gcircumflex', 'gcommaaccent', 
        'gdotaccent', 'ge-cy', 'gje-cy', 'gmacron', 'gobliquestroke', 'gpalatalhook', 'graphemejoinercomb', 'grave', 'graveacutegravecomb', 'gravecomb', 'gravecomb.component', 
        'gravecomb.component1', 'gravecomb.component3', 'gravedottedcomb', 'gravemacroncomb', 'gravetonecomb', 'gsingle', 'h', 'hPalatalhook', 'ha-cy', 
        'hbrevebelow', 'hcaron', 'hcedilla', 'hcircumflex', 'hcomb', 'hdieresis', 'hdotaccent', 'hdotbelow', 'hlinebelow', 'homotheticabovecomb', 'hookabovecomb', 
        'hookabovecomb.component', 'horncomb', 'hungarumlaut', 'hungarumlautcomb', 'i', 'i-cy', 'iacute', 'ibreve', 'icaron', 'icircumflex', 'icomb', 'idblgrave', 'idieresis', 
        'idieresis-cy', 'idieresis.component', 'idieresisacute', 'idotbelow', 'idotless', 'ie-cy', 'iebreve-cy', 'iegrave-cy', 'igrave', 'ihookabove', 'ii-cy', 
        'iigrave-cy', 'iinvertedbreve', 'iishort-cy', 'iishorttail-cy', 'ij', 'imacron', 'imacron-cy', 'io-cy', 'iogonek', 'iota', 'iotadasia', 'iotadasiaoxia', 
        'iotadasiaperispomeni', 'iotadasiavaria', 'iotadialytikaoxia', 'iotadialytikaperispomeni', 'iotadialytikavaria', 'iotadieresis', 'iotadieresistonos', 'iotamacron', 
        'iotaoxia', 'iotaperispomeni', 'iotapsili', 'iotapsilioxia', 'iotapsiliperispomeni', 'iotapsilivaria', 'iotastroke', 'iotatonos', 'iotavaria', 'iotavrachy', 
        'iretroflexhook', 'itilde', 'itildebelow', 'izhitsa-cy', 'izhitsadblgrave-cy', 'jcaron', 'jcircumflex', 'jdotless', 'k', 'ka-cy', 'kacute', 'kcaron', 'kcommaaccent', 
        'kdiagonalstroke', 'kdotbelow', 'kgreenlandic', 'kje-cy', 'klinebelow', 'kobliquestroke', 'koronis', 'koroniscomb', 'kpalatalhook', 'kstroke', 'kstrokediagonalstroke', 
        'l', 'lacute', 'lcaron', 'lcircumflexbelow', 'lcommaaccent', 'ldot', 'ldotbelow', 'ldotbelowmacron', 'ldoublemiddletilde', 'leftangleabovecomb', 'lefthalfringabovecomb', 
        'lj', 'llinebelow', 'longs', 'longsdotaccent', 'lowcircumflexmod', 'lowtildemod', 'lpalatalhook', 'm', 'macron', 'macronacutecomb', 'macroncomb', 
        'macroncomb.component', 'macroncomb.component1', 'macrongravecomb', 'macute', 'mcomb', 'mdotaccent', 'mdotbelow', 'mill', 'mmiddletilde', 
        'mpalatalhook', 'mum', 'n', 'nacute', 'napostrophe', 'ncaron', 'ncircumflexbelow', 'ncommaaccent', 'ndescender', 'ndotaccent', 'ndotbelow', 'ngrave', 'nj', 'nlinebelow', 
        'nmiddletilde', 'nobliquestroke', 'nottildeabovecomb', 'npalatalhook', 'ntilde', 'num', 'o', 'o-cy', 'oacute', 'obarred', 'obarred-cy', 
        'obarreddieresis-cy', 'obreve', 'ocaron', 'ocircumflex', 'ocircumflexacute', 'ocircumflexdotbelow', 'ocircumflexgrave', 'ocircumflexhookabove', 'ocircumflextilde', 
        'ocomb', 'odblgrave', 'odieresis', 'odieresis-cy', 'odieresismacron', 'odotaccent', 'odotaccentmacron', 'odotbelow', 'oe','ograve', 'ohookabove', 
        'ohorn', 'ohornacute', 'ohorndotbelow', 'ohorngrave', 'ohornhookabove', 'ohorntilde', 'ohungarumlaut', 'oinvertedbreve', 'omacron', 'omacronacute', 'omacrongrave', 
        'omega', 'omega-cy', 'omega-latin', 'omegadasia', 'omegadasiaoxia', 'omegadasiaoxiaypogegrammeni', 'omegadasiaperispomeni', 'omegadasiaperispomeniypogegrammeni', 
        'omegadasiavaria', 'omegadasiavariaypogegrammeni', 'omegadasiaypogegrammeni', 'omegaoxia', 'omegaoxiaypogegrammeni', 'omegaperispomeni', 'omegaperispomeniypogegrammeni', 
        'omegapsili', 'omegapsilioxia', 'omegapsilioxiaypogegrammeni', 'omegapsiliperispomeni', 'omegapsiliperispomeniypogegrammeni', 'omegapsilivaria', 
        'omegapsilivariaypogegrammeni', 'omegapsiliypogegrammeni', 'omegatonos', 'omegavaria', 'omegavariaypogegrammeni', 'omegaypogegrammeni', 'omicron', 'omicrondasia', 
        'omicrondasiaoxia', 'omicrondasiavaria', 'omicronoxia', 'omicronpsili', 'omicronpsilioxia', 'omicronpsilivaria', 'omicrontonos', 'omicronvaria', 'oogonek', 
        'oogonekmacron', 'oopenretroflexhook', 'oslash', 'oslashacute', 'otilde', 'otilde.component', 'otilde.component1', 'otildeacute', 'otildedieresis', 'otildemacron', 
        'overlinecomb', 'oxia', 'p', 'pacute', 'palatalizationcomb-cy', 'palochka-cy', 'pamphyliandigamma', 'pdotaccent', 'perispomeni', 'perispomenicomb', 'pmiddletilde', 
        'pokrytiecomb-cy', 'ppalatalhook', 'psili', 'psilioxia', 'psiliperispomeni', 'psilipneumatacomb-cy', 'psilivaria', 'pstroke', 'pstrokethroughdescender', 'q', 
        'qdiagonalstroke', 'qstrokethroughdescender', 'r', 'r.salt', 'racute', 'rcaron', 'rcomb', 'rcommaaccent', 'rdblgrave', 'rdotaccent', 'rdotbelow', 'rdotbelowmacron', 'rho', 
        'rhoStrokeSymbol', 'rhodasia', 'rhopsili', 'righthalfringabovecomb', 'ring', 'ringcomb', 'ringhalfright', 'rinvertedbreve', 'rlinebelow', 
        'rmiddletilde', 'robliquestroke', 'rpalatalhook', 'rstroke', 'rum', 's', 'sacute', 'sacute.component', 'sacutedotaccent', 'scaron', 'scaron.component', 
        'scarondotaccent', 'scedilla', 'schwa', 'schwa-cy', 'schwadieresis-cy', 'schwaretroflexhook', 'scircumflex', 'scommaaccent', 'sdotaccent', 'sdotbelow', 
        'sdotbelowdotaccent', 'secondtonechinese', 'shha-cy', 'sigmaLunateDottedSymbol', 'sigmaLunateSymbol', 'smiddletilde', 'sobliquestroke', 'spalatalhook', 
         'suspensioncomb', 't', 'tcaron', 'tcedilla', 'tcircumflexbelow', 'tcomb', 'tcommaaccent', 'tdiagonalstroke', 
        'tdieresis', 'tdotaccent', 'tdotbelow', 'thstrikethrough', 'tilde', 'tildecomb', 'tildecomb.component', 'tildedoublecomb', 'tildeverticalcomb', 
        'titlocomb-cy', 'tlinebelow', 'tmiddletilde', 'tonos', 'u', 'u-cy', 'uacute', 'ubar', 'ubreve', 'ucaron', 'ucircumflex', 'ucircumflexbelow', 'ucomb', 'udblgrave', 
        'udieresis', 'udieresis-cy', 'udieresis.component', 'udieresisacute', 'udieresisbelow', 'udieresiscaron', 'udieresisgrave', 'udieresismacron', 'udotbelow', 'ugrave', 
        'uhookabove', 'uhorn', 'uhornacute', 'uhorndotbelow', 'uhorngrave', 'uhornhookabove', 'uhorntilde', 'uhungarumlaut', 'uhungarumlaut-cy', 'uinvertedbreve', 'umacron', 
        'umacron-cy', 'umacron.component', 'umacrondieresis', 'uni047E', 'uni047E.component', 'uni047F', 'uogonek', 'upsilon', 'upsilondasia', 'upsilondasiaoxia', 
        'upsilondasiaperispomeni', 'upsilondasiavaria', 'upsilondialytikaoxia', 'upsilondialytikaperispomeni', 'upsilondialytikavaria', 'upsilondieresis', 
        'upsilondieresistonos', 'upsilonmacron', 'upsilonoxia', 'upsilonperispomeni', 'upsilonpsili', 'upsilonpsilioxia', 'upsilonpsiliperispomeni', 'upsilonpsilivaria', 
        'upsilontonos', 'upsilonvaria', 'upsilonvrachy', 'uretroflexhook', 'uring', 'ushort-cy', 'utilde', 'utildeacute', 'utildebelow', 'v', 'varia', 'vcomb', 'vdiagonalstroke', 
        'vdotbelow', 'verticallineabovecomb', 'vpalatalhook', 'vrighthook', 'vtilde', 'w', 'wacute', 'wcircumflex', 'wdieresis', 'wdotaccent', 'wdotbelow', 
        'wgrave', 'wring', 'x', 'xabovecomb', 'xcomb', 'xdieresis', 'xdotaccent', 'xpalatalhook', 'y', 'yacute', 'ycircumflex', 'ydieresis', 'ydotaccent', 'ydotbelow', 
        'yeru-cy', 'yerudieresis-cy', 'ygrave', 'yhookabove', 'yi-cy', 'ymacron', 'yring', 'ystroke', 'ytilde', 'z', 'zacute', 'zcaron', 'zcircumflex', 'zdotaccent', 
        'zdotbelow', 'ze-cy', 'zedieresis-cy', 'zhe-cy', 'zhebreve-cy', 'zhedieresis-cy', 'zigzagabovecomb', 'zlinebelow', 'zmiddletilde', 'zpalatalhook',
        'dottedCircle', 'ringhalfleft',
    ]

    MIDDLE_ANCHORS = ['A', 'A-cy', 'AE', 'AEacute', 'AEmacron', 'Aacute', 'Abreve', 'Abreve-cy', 'Abreveacute', 'Abrevedotbelow', 
        'Abrevegrave', 'Abrevehookabove', 'Abrevetilde', 'Acaron', 'Acircumflex', 'Acircumflexacute', 'Acircumflexdotbelow', 
        'Acircumflexgrave', 'Acircumflexhookabove', 'Acircumflextilde', 'Adblgrave', 'Adieresis', 'Adieresis-cy', 'Adieresismacron', 
        'Adotaccent', 'Adotbelow', 'Adotmacron', 'Agrave', 'Ahookabove', 'Aie-cy', 'Ainvertedbreve', 'Alpha', 'Alphadasia', 
        'Alphadasiaoxia', 'Alphadasiaoxiaprosgegrammeni', 'Alphadasiaperispomeni', 'Alphadasiaperispomeniprosgegrammeni', 
        'Alphadasiaprosgegrammeni', 'Alphadasiavaria', 'Alphadasiavariaprosgegrammeni', 'Alphamacron', 'Alphaoxia', 
        'Alphaprosgegrammeni', 'Alphapsili', 'Alphapsilioxia', 'Alphapsilioxiaprosgegrammeni', 'Alphapsiliperispomeni', 
        'Alphapsiliperispomeniprosgegrammeni', 'Alphapsiliprosgegrammeni', 'Alphapsilivaria', 'Alphapsilivariaprosgegrammeni', 
        'Alphatonos', 'Alphavaria', 'Alphavrachy', 'Amacron', 'Aogonek', 'Aringbelow', 'Astroke', 'Atilde', 'B', 'Bdotaccent', 
        'Bdotbelow', 'Beta', 'Blinebelow', 'Bstroke', 'C', 'Cacute', 'Cbar', 'Ccaron', 'Ccedilla', 'Ccedillaacute', 'Ccircumflex', 
        'Cdotaccent', 'Chi', 'Chi-latin', 'Csmall', 'Cstroke', 'D', 'DZ', 'DZcaron', 'Dcaron', 'Dcedilla', 'Dcircumflexbelow', 
        'Ddotaccent', 'Ddotbelow', 'Dlinebelow', 'Dz', 'Dzcaron', 'Dze-cy', 'E', 'Eacute', 'Ebreve', 'Ecaron', 'Ecedilla', 
        'Ecedillabreve', 'Ecircumflex', 'Ecircumflexacute', 'Ecircumflexbelow', 'Ecircumflexdotbelow', 'Ecircumflexgrave', 
        'Ecircumflexhookabove', 'Ecircumflextilde', 'Edblgrave', 'Edieresis', 'Edotaccent', 'Edotbelow', 'Egrave', 'Ehookabove', 
        'Einvertedbreve', 'Em-cy', 'Emacron', 'Emacronacute', 'Emacrongrave', 'Emtail-cy', 'En-cy', 'Entail-cy', 'Eogonek', 
        'Epsilon', 'Epsilondasia', 'Epsilondasiaoxia', 'Epsilondasiavaria', 'Epsilonoxia', 'Epsilonpsili', 'Epsilonpsilioxia', 
        'Epsilonpsilivaria', 'Epsilontonos', 'Epsilonvaria', 'Er-cy', 'Es-cy', 'Estroke', 'Eta', 'Etadasia', 'Etadasiaoxia', 
        'Etadasiaoxiaprosgegrammeni', 'Etadasiaperispomeni', 'Etadasiaperispomeniprosgegrammeni', 'Etadasiaprosgegrammeni', 
        'Etadasiavaria', 'Etadasiavariaprosgegrammeni', 'Etaoxia', 'Etaprosgegrammeni', 'Etapsili', 'Etapsilioxia', 
        'Etapsilioxiaprosgegrammeni', 'Etapsiliperispomeni', 'Etapsiliperispomeniprosgegrammeni', 'Etapsiliprosgegrammeni', 
        'Etapsilivaria', 'Etapsilivariaprosgegrammeni', 'Etatonos', 'Etavaria', 'Etilde', 'Etildebelow', 'F', 'Fdotaccent', 'G', 
        'Gacute', 'Gbreve', 'Gcaron', 'Gcircumflex', 'Gcommaaccent', 'Gdotaccent', 'Gmacron', 'Gobliquestroke', 'H', 'Ha-cy', 
        'Hbrevebelow', 'Hcaron', 'Hcedilla', 'Hcircumflex', 'Hdieresis', 'Hdotaccent', 'Hdotbelow', 'I', 'I-cy', 'IJ', 'Iacute', 
        'Ibreve', 'Icaron', 'Icircumflex', 'Idblgrave', 'Idieresis', 'Idieresisacute', 'Idotaccent', 'Idotbelow', 'Ie-cy', 
        'Iebreve-cy', 'Iegrave-cy', 'Igrave', 'Ihookabove', 'Iinvertedbreve', 'Imacron', 'Io-cy', 'Iogonek', 'Iota', 'Iotadasia', 
        'Iotadasiaoxia', 'Iotadasiaperispomeni', 'Iotadasiavaria', 'Iotadieresis', 'Iotamacron', 'Iotaoxia', 'Iotapsili', 
        'Iotapsilioxia', 'Iotapsiliperispomeni', 'Iotapsilivaria', 'Iotatonos', 'Iotavaria', 'Iotavrachy', 'Itilde', 'Itildebelow', 
        'J', 'Jcircumflex', 'Je-cy', 'Jstroke', 'K', 'Ka-cy', 'Kacute', 'Kappa', 'Kcaron', 'Kcommaaccent', 'Kdiagonalstroke', 
        'Kdotbelow', 'Kje-cy', 'Klinebelow', 'Kobliquestroke', 'Kstroke', 'Kstrokediagonalstroke', 'L', 'LJ', 'Lacute', 'Lbar', 
        'Lcaron', 'Lcircumflexbelow', 'Lcommaaccent', 'Ldot', 'Ldotbelow', 'Ldotbelowmacron', 'Ldoublebar', 'Lj', 'Llinebelow', 
        'Lmiddletilde', 'M', 'Macute', 'Mdotaccent', 'Mdotbelow', 'Mu', 'N', 'NJ', 'Nacute', 'Ncaron', 'Ncircumflexbelow', 
        'Ncommaaccent', 'Ndescender', 'Ndotaccent', 'Ndotbelow', 'Ngrave', 'Nj', 'Nlinebelow', 'Nobliquestroke', 'Ntilde', 
        'Nu', 'O', 'O-cy', 'OE', 'Oacute', 'Obreve', 'Ocaron', 'Ocircumflex', 'Ocircumflexacute', 'Ocircumflexdotbelow', 
        'Ocircumflexgrave', 'Ocircumflexhookabove', 'Ocircumflextilde', 'Odblgrave', 'Odieresis', 'Odieresis-cy', 'Odieresismacron', 
        'Odotaccent', 'Odotaccentmacron', 'Odotbelow', 'Ograve', 'Ohookabove', 'Ohungarumlaut', 'Oinvertedbreve', 'Olongstroke', 
        'Omacron', 'Omacronacute', 'Omacrongrave', 'Omicron', 'Omicrondasia', 'Omicrondasiaoxia', 'Omicrondasiavaria', 'Omicronoxia', 
        'Omicronpsili', 'Omicronpsilioxia', 'Omicronpsilivaria', 'Omicrontonos', 'Omicronvaria', 'Oogonek', 'Oogonekmacron', 
        'Oslash', 'Oslashacute', 'Osmall', 'Otilde', 'Otildeacute', 'Otildedieresis', 'Otildemacron', 'P', 'Pacute', 'Palochka-cy', 
        'Pdotaccent', 'Pstroke', 'Pstrokethroughdescender', 'Q', 'Qstrokethroughdescender', 'R', 'Racute', 'Rcaron', 'Rcommaaccent', 
        'Rdblgrave', 'Rdotaccent', 'Rdotbelow', 'Rdotbelowmacron', 'Rho', 'Rhodasia', 'Rinvertedbreve', 'Rlinebelow', 'Robliquestroke', 
        'Rstroke', 'S', 'Sacute', 'Sacutedotaccent', 'Scaron', 'Scarondotaccent', 'Scedilla', 'Scircumflex', 'Scommaaccent', 
        'Sdotaccent', 'Sdotbelow', 'Sdotbelowdotaccent', 'SigmaLunateDottedSymbol', 'Sobliquestroke', 'T', 'Tau', 'Tcaron', 
        'Tcedilla', 'Tcircumflexbelow', 'Tcommaaccent', 'Tdiagonalstroke', 'Tdotaccent', 'Tdotbelow', 'Te-cy', 'Tlinebelow', 'U', 
        'Uacute', 'Ubar', 'Ubreve', 'Ucaron', 'Ucircumflex', 'Ucircumflexbelow', 'Udblgrave', 'Udieresis', 'Udieresisacute', 
        'Udieresisbelow', 'Udieresiscaron', 'Udieresisgrave', 'Udieresismacron', 'Udotbelow', 'Ugrave', 'Uhookabove', 'Uhungarumlaut', 
        'Uinvertedbreve', 'Umacron', 'Umacrondieresis', 'Uogonek', 'Upsilon', 'Upsilondasia', 'Upsilondasiaoxia', 
        'Upsilondasiaperispomeni', 'Upsilondasiavaria', 'Upsilondieresis', 'Upsilonmacron', 'Upsilonoxia', 'Upsilontonos', 
        'Upsilonvaria', 'Upsilonvrachy', 'Uring', 'Ustrait-cy', 'Utilde', 'Utildeacute', 'Utildebelow', 'V', 'Vdiagonalstroke', 
        'Vdotbelow', 'Ve-cy', 'Vsmall', 'Vtilde', 'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 'Wdotaccent', 'Wdotbelow', 'Wgrave', 
        'Wsmall', 'X', 'Xdieresis', 'Xdotaccent', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ydotaccent', 'Ydotbelow', 'Ygrave', 
        'Yhookabove', 'Yi-cy', 'Ymacron', 'Yot', 'Ystroke', 'Ytilde', 'Z', 'Zacute', 'Zcaron', 'Zcircumflex', 'Zdotaccent', 
        'Zdotbelow', 'Zeta', 'Zlinebelow', 'Zsmall', 'a', 'a-cy', 'aacute', 'abreve', 'abreve-cy', 'abreveacute', 'abrevedotbelow', 
        'abrevegrave', 'abrevehookabove', 'abrevetilde', 'acaron', 'acircumflex', 'acircumflexacute', 'acircumflexdotbelow', 
        'acircumflexgrave', 'acircumflexhookabove', 'acircumflextilde', 'adblgrave', 'adieresis', 'adieresis-cy', 'adieresismacron', 
        'adotaccent', 'adotbelow', 'adotmacron', 'ae', 'aeacute', 'aemacron', 'agrave', 'ahookabove', 'aie-cy', 'ainvertedbreve', 
        'amacron', 'aogonek', 'aretroflexhook', 'arighthalfring', 'aring', 'aringacute', 'aringbelow', 'astroke', 'atilde', 'b', 'bdotaccent', 
        'bdotbelow', 'blinebelow', 'bmiddletilde', 'bpalatalhook', 'c', 'cPalatalhook', 'cacute', 'cbar', 'ccaron', 'ccedilla', 'ccedillaacute', 
        'ccircumflex', 'cdotaccent', 'cstroke', 'd', 'dcaron', 'dcedilla', 'dcircumflexbelow', 'ddotaccent', 'ddotbelow', 'dlinebelow', 'dmiddletilde', 
        'dpalatalhook', 'dum', 'dz', 'dzcaron', 'dze-cy', 'e', 'eacute', 'ebreve', 'ecaron', 'ecedilla', 'ecedillabreve', 'ecircumflex', 'ecircumflexacute', 
        'ecircumflexbelow', 'ecircumflexdotbelow', 'ecircumflexgrave', 'ecircumflexhookabove', 'ecircumflextilde', 'edblgrave', 'edieresis', 'edotaccent', 
        'edotbelow', 'egrave', 'ehookabove', 'einvertedbreve', 'emacron', 'emacronacute', 'emacrongrave', 'eogonek', 'er-cy', 'eretroflexhook', 'ertick-cy', 
        'es-cy', 'estroke', 'etilde', 'etildebelow', 'f', 'fStroke', 'fdotaccent', 'flenis', 'fmiddletilde', 'fpalatalhook', 'g', 'gacute', 'gbreve', 
        'gcaron', 'gcircumflex', 'gcommaaccent', 'gdotaccent', 'gmacron', 'gobliquestroke', 'gpalatalhook', 'gsingle', 'h', 'hPalatalhook', 'ha-cy', 
        'hbrevebelow', 'hcaron', 'hcedilla', 'hcircumflex', 'hdieresis', 'hdotaccent', 'hdotbelow', 'hlinebelow', 'i', 'i-cy', 'idotbelow', 'ie-cy', 
        'iebreve-cy', 'iegrave-cy', 'ij', 'io-cy', 'iogonek', 'iretroflexhook', 'itildebelow', 'j', 'jcaron', 'jcircumflex', 'jdotless', 'je-cy', 'jstroke', 
        'k', 'kacute', 'kcaron', 'kcommaaccent', 'kdiagonalstroke', 'kdotbelow', 'klinebelow', 'kobliquestroke', 'kpalatalhook', 'kstroke', 'kstrokediagonalstroke', 
        'l', 'lacute', 'lcaron', 'lcircumflexbelow', 'lcommaaccent', 'ldot', 'ldotbelow', 'ldotbelowmacron', 'ldoublemiddletilde', 'lj', 'llinebelow', 'lpalatalhook', 
        'm', 'macute', 'mdotaccent', 'mdotbelow', 'mill', 'mmiddletilde', 'mpalatalhook', 'mum', 'n', 'nacute', 'napostrophe', 'ncaron', 'ncircumflexbelow', 
        'ncommaaccent', 'ndescender', 'ndotaccent', 'ndotbelow', 'ngrave', 'nj', 'nlinebelow', 'nmiddletilde', 'nobliquestroke', 'npalatalhook', 'ntilde', 'num', 
        'o', 'o-cy', 'oacute', 'obreve', 'ocaron', 'ocircumflex', 'ocircumflexacute', 'ocircumflexdotbelow', 'ocircumflexgrave', 'ocircumflexhookabove', 
        'ocircumflextilde', 'odblgrave', 'odieresis', 'odieresis-cy', 'odieresismacron', 'odotaccent', 'odotaccentmacron', 'odotbelow', 'oe', 'ograve', 
        'ohookabove', 'ohungarumlaut', 'oinvertedbreve', 'omacron', 'omacronacute', 'omacrongrave', 'omicron', 'omicrondasia', 'omicrondasiaoxia', 
        'omicrondasiavaria', 'omicronoxia', 'omicronpsili', 'omicronpsilioxia', 'omicronpsilivaria', 'omicrontonos', 'omicronvaria', 'oogonek', 'oslash', 
        'oslashacute', 'otilde', 'otildeacute', 'otildedieresis', 'otildemacron', 'p', 'pacute', 'palochka-cy', 'pdotaccent', 'pmiddletilde', 'ppalatalhook', 
        'pstroke', 'pstrokethroughdescender', 'q', 'qdiagonalstroke', 'qstrokethroughdescender', 'r', 'r.salt', 'racute', 'rcaron', 'rcommaaccent', 'rdblgrave', 
        'rdotaccent', 'rdotbelow', 'rdotbelowmacron', 'rinvertedbreve', 'rlinebelow', 'rmiddletilde', 'robliquestroke', 'rpalatalhook', 'rstroke', 'rum', 
        's', 'sacute', 'sacutedotaccent', 'scaron', 'scarondotaccent', 'scedilla', 'scircumflex', 'scommaaccent', 'sdotaccent', 'sdotbelow', 'sdotbelowdotaccent', 
        'shha-cy', 'sigmaLunateDottedSymbol', 'sigmaLunateSymbol', 'smiddletilde', 'sobliquestroke', 'spalatalhook', 't', 'tcaron', 'tcedilla', 'tcircumflexbelow', 
        'tcommaaccent', 'tdiagonalstroke', 'tdieresis', 'tdotaccent', 'tdotbelow', 'thstrikethrough', 'tlinebelow', 'tmiddletilde', 'u', 'u-cy', 'uacute', 'ubar', 
        'ubreve', 'ucaron', 'ucircumflex', 'ucircumflexbelow', 'udblgrave', 'udieresis', 'udieresis-cy', 'udieresisacute', 'udieresisbelow', 'udieresiscaron', 
        'udieresisgrave', 'udieresismacron', 'udotbelow', 'ugrave', 'uhookabove', 'uhungarumlaut', 'uhungarumlaut-cy', 'uinvertedbreve', 'umacron', 'umacron-cy', 
        'umacrondieresis', 'uogonek', 'uretroflexhook', 'uring', 'ushort-cy', 'utilde', 'utildeacute', 'utildebelow', 'v', 'vdiagonalstroke', 'vdotbelow', 'vpalatalhook', 
        'vtilde', 'w', 'wacute', 'wcircumflex', 'wdieresis', 'wdotaccent', 'wdotbelow', 'wgrave', 'wring', 'x', 'xdieresis', 'xdotaccent', 'xpalatalhook', 'y', 'yacute', 
        'ycircumflex', 'ydieresis', 'ydotaccent', 'ydotbelow', 'ygrave', 'yhookabove', 'ymacron', 'yot', 'yring', 'ystroke', 'ytilde', 'z', 'zacute', 'zcaron', 
        'zcircumflex', 'zdotaccent', 'zdotbelow', 'zlinebelow', 'zmiddletilde', 'zpalatalhook', 
        'tildeoverlaycomb', 'strokeshortcomb', 'strokelongcomb', 'slashshortcomb', 'slashlongcomb',  'idieresisacute', 'ihookabove', 'igrave',
        'iacute','icircumflex', 'idieresis', 
        ]

    BOTTOM_ANCHORS = ['A', 'A-cy', 'AE', 'AEacute', 'AEmacron', 'Aacute', 'Abreve', 'Abreve-cy', 'Abreveacute', 'Abrevedotbelow', 
        'Abrevegrave', 'Abrevehookabove', 'Abrevetilde', 'Acaron', 'Acircumflex', 'Acircumflexacute', 'Acircumflexdotbelow', 
        'Acircumflexgrave', 'Acircumflexhookabove', 'Acircumflextilde', 'Adblgrave', 'Adieresis', 'Adieresis-cy', 'Adieresismacron', 
        'Adotaccent', 'Adotbelow', 'Adotmacron', 'Agrave', 'Ahookabove', 'Aie-cy', 'Ainvertedbreve', 'Alpha', 'Alphadasia', 
        'Alphadasiaoxia', 'Alphadasiaoxiaprosgegrammeni', 'Alphadasiaperispomeni', 'Alphadasiaperispomeniprosgegrammeni', 
        'Alphadasiaprosgegrammeni', 'Alphadasiavaria', 'Alphadasiavariaprosgegrammeni', 'Alphamacron', 'Alphaoxia', 
        'Alphaprosgegrammeni', 'Alphapsili', 'Alphapsilioxia', 'Alphapsilioxiaprosgegrammeni', 'Alphapsiliperispomeni', 
        'Alphapsiliperispomeniprosgegrammeni', 'Alphapsiliprosgegrammeni', 'Alphapsilivaria', 'Alphapsilivariaprosgegrammeni', 
        'Alphatonos', 'Alphavaria', 'Alphavrachy', 'Amacron', 'Aogonek', 'Aringbelow', 'Astroke', 'Atilde', 'B', 'Bdotaccent', 
        'Bdotbelow', 'Beta', 'Blinebelow', 'Bstroke', 'C', 'Cacute', 'Cbar', 'Ccaron', 'Ccedilla', 'Ccedillaacute', 'Ccircumflex', 
        'Cdotaccent', 'Chi', 'Chi-latin', 'Csmall', 'Cstroke', 'D', 'DZ', 'DZcaron', 'Dcaron', 'Dcedilla', 'Dcircumflexbelow', 
        'Ddotaccent', 'Ddotbelow', 'Dlinebelow', 'Dz', 'Dzcaron', 'Dze-cy', 'E', 'Eacute', 'Ebreve', 'Ecaron', 'Ecedilla', 
        'Ecedillabreve', 'Ecircumflex', 'Ecircumflexacute', 'Ecircumflexbelow', 'Ecircumflexdotbelow', 'Ecircumflexgrave', 
        'Ecircumflexhookabove', 'Ecircumflextilde', 'Edblgrave', 'Edieresis', 'Edotaccent', 'Edotbelow', 'Egrave', 'Ehookabove', 'Einvertedbreve', 'Em-cy', 
        'Emacron', 'Emacronacute', 'Emacrongrave', 'Emtail-cy', 'En-cy', 'Entail-cy', 'Eogonek', 'Epsilon', 'Epsilondasia', 'Epsilondasiaoxia', 'Epsilondasiavaria', 
        'Epsilonoxia', 'Epsilonpsili', 'Epsilonpsilioxia', 'Epsilonpsilivaria', 'Epsilontonos', 'Epsilonvaria', 'Er-cy', 'Es-cy', 'Estroke', 'Eta', 'Etadasia', 
        'Etadasiaoxia', 'Etadasiaoxiaprosgegrammeni', 'Etadasiaperispomeni', 'Etadasiaperispomeniprosgegrammeni', 'Etadasiaprosgegrammeni', 'Etadasiavaria', 
        'Etadasiavariaprosgegrammeni', 'Etaoxia', 'Etaprosgegrammeni', 'Etapsili', 'Etapsilioxia', 'Etapsilioxiaprosgegrammeni', 'Etapsiliperispomeni', 
        'Etapsiliperispomeniprosgegrammeni', 'Etapsiliprosgegrammeni', 'Etapsilivaria', 'Etapsilivariaprosgegrammeni', 'Etatonos', 'Etavaria', 'Etilde', 'Etildebelow', 
        'F', 'Fdotaccent', 'G', 'Gacute', 'Gbreve', 'Gcaron', 'Gcircumflex', 'Gcommaaccent', 'Gdotaccent', 'Gmacron', 'Gobliquestroke', 'H', 'Ha-cy', 'Hbrevebelow', 
        'Hcaron', 'Hcedilla', 'Hcircumflex', 'Hdieresis', 'Hdotaccent', 'Hdotbelow', 'I', 'I-cy', 'IJ', 'Iacute', 'Ibreve', 'Icaron', 'Icircumflex', 'Idblgrave', 
        'Idieresis', 'Idieresisacute', 'Idotaccent', 'Idotbelow', 'Ie-cy', 'Iebreve-cy', 'Iegrave-cy', 'Igrave', 'Ihookabove', 'Iinvertedbreve', 'Imacron', 'Io-cy', 
        'Iogonek', 'Iota', 'Iotadasia', 'Iotadasiaoxia', 'Iotadasiaperispomeni', 'Iotadasiavaria', 'Iotadieresis', 'Iotamacron', 'Iotaoxia', 'Iotapsili', 'Iotapsilioxia', 
        'Iotapsiliperispomeni', 'Iotapsilivaria', 'Iotatonos', 'Iotavaria', 'Iotavrachy', 'Itilde', 'Itildebelow', 'J', 'Jcircumflex', 'Je-cy', 'Jstroke', 'K', 'Ka-cy', 'Kacute', 
        'Kappa', 'Kcaron', 'Kcommaaccent', 'Kdiagonalstroke', 'Kdotbelow', 'Kje-cy', 'Klinebelow', 'Kobliquestroke', 'Kstroke', 'Kstrokediagonalstroke', 'L', 'LJ', 'Lacute', 
        'Lbar', 'Lcaron', 'Lcircumflexbelow', 'Lcommaaccent', 'Ldot', 'Ldotbelow', 'Ldotbelowmacron', 'Ldoublebar', 'Lj', 'Llinebelow', 'Lmiddletilde', 'M', 'Macute', 'Mdotaccent', 
        'Mdotbelow', 'Mu', 'N', 'NJ', 'Nacute', 'Ncaron', 'Ncircumflexbelow', 'Ncommaaccent', 'Ndescender', 'Ndotaccent', 'Ndotbelow', 'Ngrave', 'Nj', 'Nlinebelow', 
        'Nobliquestroke', 'Ntilde', 'Nu', 'O', 'O-cy', 'OE', 'Oacute', 'Obreve', 'Ocaron', 'Ocircumflex', 'Ocircumflexacute', 'Ocircumflexdotbelow', 'Ocircumflexgrave', 
        'Ocircumflexhookabove', 'Ocircumflextilde', 'Odblgrave', 'Odieresis', 'Odieresis-cy', 'Odieresismacron', 'Odotaccent', 'Odotaccentmacron', 'Odotbelow', 'Ograve', 
        'Ohm', 'Ohookabove', 'Ohorn', 'Ohornacute', 'Ohorndotbelow', 'Ohorngrave', 'Ohornhookabove', 'Ohorntilde', 'Ohungarumlaut', 'Oinvertedbreve', 'Olongstroke', 
        'Omacron', 'Omacronacute', 'Omacrongrave', 'Omega', 'Omegadasia', 'Omegadasiaoxia', 'Omegadasiaoxiaprosgegrammeni', 'Omegadasiaperispomeni', 
        'Omegadasiaperispomeniprosgegrammeni', 'Omegadasiaprosgegrammeni', 'Omegadasiavaria', 'Omegadasiavariaprosgegrammeni', 'Omegaoxia', 'Omegaprosgegrammeni', 
        'Omegapsili', 'Omegapsilioxia', 'Omegapsilioxiaprosgegrammeni', 'Omegapsiliperispomeni', 'Omegapsiliperispomeniprosgegrammeni', 'Omegapsiliprosgegrammeni', 
        'Omegapsilivaria', 'Omegapsilivariaprosgegrammeni', 'Omegatonos', 'Omegavaria', 'Omicron', 'Omicrondasia', 'Omicrondasiaoxia', 'Omicrondasiavaria', 'Omicronoxia', 
        'Omicronpsili', 'Omicronpsilioxia', 'Omicronpsilivaria', 'Omicrontonos', 'Omicronvaria', 'Oogonek', 'Oogonekmacron', 'Oslash', 'Oslashacute', 'Osmall', 'Otilde', 
        'Otildeacute', 'Otildedieresis', 'Otildemacron', 'P', 'Pacute', 'Palochka-cy', 'Pdotaccent', 'Pstroke', 'Pstrokethroughdescender', 'Q', 'Qstrokethroughdescender', 
        'R', 'Racute', 'Rcaron', 'Rcommaaccent', 'Rdblgrave', 'Rdotaccent', 'Rdotbelow', 'Rdotbelowmacron', 'Rho', 'Rhodasia', 'Rinvertedbreve', 'Rlinebelow', 
        'Robliquestroke', 'Rstroke', 'S', 'Sacute', 'Sacutedotaccent', 'Scaron', 'Scarondotaccent', 'Scedilla', 'Scircumflex', 'Scommaaccent', 'Sdotaccent', 'Sdotbelow', 
        'Sdotbelowdotaccent', 'SigmaLunateDottedSymbol', 'Sobliquestroke', 'T', 'Tau', 'Tcaron', 'Tcedilla', 'Tcircumflexbelow', 'Tcommaaccent', 'Tdiagonalstroke', 
        'Tdotaccent', 'Tdotbelow', 'Te-cy', 'Tlinebelow', 'U', 'Uacute', 'Ubar', 'Ubreve', 'Ucaron', 'Ucircumflex', 'Ucircumflexbelow', 'Udblgrave', 'Udieresis', 
        'Udieresisacute', 'Udieresisbelow', 'Udieresiscaron', 'Udieresisgrave', 'Udieresismacron', 'Udotbelow', 'Ugrave', 'Uhookabove', 'Uhorn', 'Uhornacute', 'Uhorndotbelow', 
        'Uhorngrave', 'Uhornhookabove', 'Uhorntilde', 'Uhungarumlaut', 'Uinvertedbreve', 'Umacron', 'Umacrondieresis', 'Uogonek', 'Upsilon', 'Upsilondasia', 'Upsilondasiaoxia', 
        'Upsilondasiaperispomeni', 'Upsilondasiavaria', 'Upsilondieresis', 'Upsilonmacron', 'Upsilonoxia', 'Upsilontonos', 'Upsilonvaria', 'Upsilonvrachy', 'Uring', 'Ustrait-cy', 
        'Utilde', 'Utildeacute', 'Utildebelow', 'V', 'Vdiagonalstroke', 'Vdotbelow', 'Ve-cy', 'Vsmall', 'Vtilde', 'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 'Wdotaccent', 
        'Wdotbelow', 'Wgrave', 'Wsmall', 'X', 'Xdieresis', 'Xdotaccent', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ydotaccent', 'Ydotbelow', 'Ygrave', 'Yhookabove', 'Yi-cy', 
        'Ymacron', 'Yot', 'Ystroke', 'Ytilde', 'Z', 'Zacute', 'Zcaron', 'Zcircumflex', 'Zdotaccent', 'Zdotbelow', 'Zeta', 'Zlinebelow', 'Zsmall', 'a', 'a-cy', 'aacute', 
        'abreve', 'abreve-cy', 'abreveacute', 'abrevedotbelow', 'abrevegrave', 'abrevehookabove', 'abrevetilde', 'acaron', 'acircumflex', 'acircumflexacute', 
        'acircumflexdotbelow', 'acircumflexgrave', 'acircumflexhookabove', 'acircumflextilde', 'acutebelowcomb', 'adblgrave', 'adieresis', 'adieresis-cy', 
        'adieresismacron', 'adotaccent', 'adotbelow', 'adotmacron', 'ae', 'aeacute', 'aemacron', 'agrave', 'ahookabove', 'aie-cy', 'ainvertedbreve', 'alpha', 
        'alphadasia', 'alphadasiaoxia', 'alphadasiaoxiaypogegrammeni', 'alphadasiaperispomeni', 'alphadasiaperispomeniypogegrammeni', 'alphadasiavaria', 
        'alphadasiavariaypogegrammeni', 'alphadasiaypogegrammeni', 'alphamacron', 'alphaoxia', 'alphaoxiaypogegrammeni', 'alphaperispomeni', 'alphaperispomeniypogegrammeni', 
        'alphapsili', 'alphapsilioxia', 'alphapsilioxiaypogegrammeni', 'alphapsiliperispomeni', 'alphapsiliperispomeniypogegrammeni', 'alphapsilivaria', 
        'alphapsilivariaypogegrammeni', 'alphapsiliypogegrammeni', 'alphatonos', 'alphavaria', 'alphavariaypogegrammeni', 'alphavrachy', 'alphaypogegrammeni', 
        'amacron', 'aogonek', 'aretroflexhook', 'arighthalfring', 'aring', 'aringacute', 'aringbelow', 'arrowdoublerightbelowcomb', 'arrowheadleftbelowcomb', 
        'arrowheadrightbelowcomb', 'arrowheadrightheadupbelowcomb', 'arrowleftrightbelowcomb', 'arrowupbelowcomb', 'asteriskbelowcomb', 'astroke', 'atilde', 'b', 
        'bdotaccent', 'bdotbelow', 'blinebelow', 'bmiddletilde', 'bpalatalhook', 'brevebelow', 'breveinvertedbelowcomb', 'bridgebelowcomb', 'bridgeinvertedbelowcomb', 'c', 
        'cPalatalhook', 'cacute', 'caronbelowcomb', 'cbar', 'ccaron', 'ccedilla', 'ccedillaacute', 'ccircumflex', 'cdotaccent', 'cedilla', 'cedillacomb', 'cedillacomb.component', 
        'circumflexbelow', 'circumflexbelowcomb', 'commaaccentcomb', 'cstroke', 'd', 'dblarchinvertedbelowcomb', 'dbllowlinecomb', 'dblmacronbelowcomb', 
        'dcaron', 'dcedilla', 'dcircumflexbelow', 'ddotaccent', 'ddotbelow', 'dieresisbelow', 'dlinebelow', 'dmiddletilde', 'dotbelowcomb', 'doublebrevebelowcomb', 
        'doubleringbelowcomb', 'doubleverticallinebelowcomb', 'downtackbelowcomb', 'dpalatalhook', 'dum', 'dz', 'dzcaron', 'dze-cy', 'e', 
        'eacute', 'ebreve', 'ecaron', 'ecedilla', 'ecedillabreve', 'ecircumflex', 'ecircumflexacute', 'ecircumflexbelow', 'ecircumflexdotbelow', 'ecircumflexgrave', 
        'ecircumflexhookabove', 'ecircumflextilde', 'edblgrave', 'edieresis', 'edotaccent', 'edotbelow', 'egrave', 'ehookabove', 'einvertedbreve', 'emacron', 'emacronacute', 
        'emacrongrave', 'eogonek', 'equalbelowcomb', 'er-cy', 'eretroflexhook', 'ertick-cy', 'es-cy', 'eshpalatalhook', 'estroke', 'eta', 'etadasia', 'etadasiaoxia', 
        'etadasiaoxiaypogegrammeni', 'etadasiaperispomeni', 'etadasiaperispomeniypogegrammeni', 'etadasiavaria', 'etadasiavariaypogegrammeni', 'etadasiaypogegrammeni', 
        'etaoxia', 'etaoxiaypogegrammeni', 'etaperispomeni', 'etaperispomeniypogegrammeni', 'etapsili', 'etapsilioxia', 'etapsilioxiaypogegrammeni', 
        'etapsiliperispomeni', 'etapsiliperispomeniypogegrammeni', 'etapsilivaria', 'etapsilivariaypogegrammeni', 'etapsiliypogegrammeni', 'etatonos', 
        'etavaria', 'etavariaypogegrammeni', 'etaypogegrammeni', 'etilde', 'etildebelow', 'f', 'fStroke', 'fdotaccent', 'flenis', 'fmiddletilde', 
        'fpalatalhook', 'g', 'gacute', 'gbreve', 'gcaron', 'gcircumflex', 'gcommaaccent', 'gdotaccent', 'gmacron', 'gobliquestroke', 'gpalatalhook', 
        'gravebelowcomb', 'gsingle', 'h', 'hPalatalhook', 'ha-cy', 'hbrevebelow', 'hcaron', 'hcedilla', 'hcircumflex', 'hdieresis', 'hdotaccent', 
        'hdotbelow', 'hlinebelow', 'i', 'i-cy', 'idotbelow', 'idotless', 'ie-cy', 'iebreve-cy', 'iegrave-cy', 'ij', 'io-cy', 'iogonek', 
        'iretroflexhook', 'itildebelow', 'j', 'jcaron', 'jcircumflex', 'jdotless', 'je-cy', 'jstroke', 'k', 'kacute', 'kcaron', 'kcommaaccent', 
        'kdiagonalstroke', 'kdotbelow', 'klinebelow', 'kobliquestroke', 'kpalatalhook', 'kstroke', 'kstrokediagonalstroke', 'l', 'lacute', 'lcaron', 
        'lcircumflexbelow', 'lcommaaccent', 'ldot', 'ldotbelow', 'ldotbelowmacron', 'ldoublemiddletilde', 'leftanglebelowcomb', 'lefttackbelowcomb', 
        'lj', 'llinebelow', 'lowlinecomb', 'lpalatalhook', 'm', 'macronbelow', 'macronbelowcomb', 'macute', 'mdotaccent', 'mdotbelow', 'mill', 
        'minusbelowcomb', 'mmiddletilde', 'mpalatalhook', 'mum', 'n', 'nacute', 'napostrophe', 'ncaron', 'ncircumflexbelow', 'ncommaaccent', 
        'ndescender', 'ndotaccent', 'ndotbelow', 'ngrave', 'nj', 'nlinebelow', 'nmiddletilde', 'nobliquestroke', 'npalatalhook', 'ntilde', 
        'num', 'o', 'o-cy', 'oacute', 'obreve', 'ocaron', 'ocircumflex', 'ocircumflexacute', 'ocircumflexdotbelow', 'ocircumflexgrave',
         'ocircumflexhookabove', 'ocircumflextilde', 'odblgrave', 'odieresis', 'odieresis-cy', 'odieresismacron', 'odotaccent', 'odotaccentmacron', 
         'odotbelow', 'oe', 'ogonekcomb', 'ograve', 'ohookabove', 'ohorn', 'ohornacute', 'ohorndotbelow', 'ohorngrave', 'ohornhookabove', 'ohorntilde', 
         'ohungarumlaut', 'oinvertedbreve', 'omacron', 'omacronacute', 'omacrongrave', 'omega', 'omega-latin', 'omegadasia', 'omegadasiaoxia', 
         'omegadasiaoxiaypogegrammeni', 'omegadasiaperispomeni', 'omegadasiaperispomeniypogegrammeni', 'omegadasiavaria', 'omegadasiavariaypogegrammeni', 
         'omegadasiaypogegrammeni', 'omegaoxia', 'omegaoxiaypogegrammeni', 'omegaperispomeni', 'omegaperispomeniypogegrammeni', 'omegapsili', 'omegapsilioxia', 
         'omegapsilioxiaypogegrammeni', 'omegapsiliperispomeni', 'omegapsiliperispomeniypogegrammeni', 'omegapsilivaria', 'omegapsilivariaypogegrammeni', 
         'omegapsiliypogegrammeni', 'omegatonos', 'omegavaria', 'omegavariaypogegrammeni', 'omegaypogegrammeni', 'omicron', 'omicrondasia', 'omicrondasiaoxia', 
         'omicrondasiavaria', 'omicronoxia', 'omicronpsili', 'omicronpsilioxia', 'omicronpsilivaria', 'omicrontonos', 'omicronvaria', 'oogonek', 'oslash', 
         'oslashacute', 'otilde', 'otildeacute', 'otildedieresis', 'otildemacron', 'p', 'pacute', 'palatalhookcomb', 'palochka-cy', 'pdotaccent', 
         'plusbelowcomb', 'pmiddletilde', 'ppalatalhook', 'prosgegrammeni', 'pstroke', 'pstrokethroughdescender', 'q', 'qdiagonalstroke', 
         'qstrokethroughdescender', 'r', 'r.salt', 'racute', 'rbelowcomb', 'rcaron', 'rcommaaccent', 'rdblgrave', 'rdotaccent', 'rdotbelow', 'rdotbelowmacron', 
         'righttackbelowcomb', 'ringbelow', 'ringbelowcomb', 'ringhalfleftbelowcomb', 'ringhalfrightbelowcomb', 'rinvertedbreve', 'rlinebelow', 'rmiddletilde', 
         'robliquestroke', 'rpalatalhook', 'rstroke', 'rum', 's', 'sacute', 'sacutedotaccent', 'scaron', 'scarondotaccent', 'scedilla', 'scircumflex', 
         'scommaaccent', 'sdotaccent', 'sdotbelow', 'sdotbelowdotaccent', 'seagullbelowcomb', 'shha-cy', 'sigmaLunateDottedSymbol', 'sigmaLunateSymbol', 
         'smiddletilde', 'snakebelowcomb', 'sobliquestroke', 'spalatalhook', 'squarebelowcomb', 't', 'tcaron', 'tcedilla', 'tcircumflexbelow', 'tcommaaccent', 
         'tdiagonalstroke', 'tdieresis', 'tdotaccent', 'tdotbelow', 'thstrikethrough', 'tildebelow', 'tlinebelow', 'tmiddletilde', 'u', 'u-cy', 'uacute', 'ubar', 
         'ubreve', 'ucaron', 'ucircumflex', 'ucircumflexbelow', 'udblgrave', 'udieresis', 'udieresis-cy', 'udieresisacute', 'udieresisbelow', 'udieresiscaron', 
         'udieresisgrave', 'udieresismacron', 'udotbelow', 'ugrave', 'uhookabove', 'uhorn', 'uhornacute', 'uhorndotbelow', 'uhorngrave', 'uhornhookabove', 
         'uhorntilde', 'uhungarumlaut', 'uhungarumlaut-cy', 'uinvertedbreve', 'umacron', 'umacron-cy', 'umacrondieresis', 'uni2195', 'uni21a8', 'uogonek', 
         'uptackbelowcomb', 'uretroflexhook', 'uring', 'ushort-cy', 'utilde', 'utildeacute', 'utildebelow', 'v', 'vdiagonalstroke', 'vdotbelow', 
         'verticallinebelowcomb', 'vpalatalhook', 'vtilde', 'w', 'wacute', 'wcircumflex', 'wdieresis', 'wdotaccent', 'wdotbelow', 'wgrave', 'wring', 
         'x', 'xbelowcomb', 'xdieresis', 'xdotaccent', 'xpalatalhook', 'y', 'yacute', 'ycircumflex', 'ydieresis', 'ydotaccent', 
         'ydotbelow', 'ygrave', 'yhookabove', 'ymacron', 'yot', 'ypogegrammeni', 'ypogegrammenicomb', 'yring', 'ystroke', 'ytilde', 'z', 'zacute', 
         'zcaron', 'zcircumflex', 'zdotaccent', 'zdotbelow', 'zlinebelow', 'zmiddletilde', 'zpalatalhook','dottedCircle', 'idieresisacute', 'ihookabove',
         'arrowheadrightheaddownbelow', 'igrave', 'iacute', 'icircumflex', 'idieresis',  
    ]

    OGONEK_ANCHORS = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']

    DOT_ANCHORS = ['C', 'L', 'SigmaLunateReversedSymbol', 'c', 'h', 'l', 'oopen']

    TONOS_ANCHORS = ['A', 'E', 'H', 'I', 'O', 'Ohm', 'P', 'UpsilonhookSymbol', 'Y']

    VERT_ANCHORS = ['L', 'd', 'l', 't']

    # Tilde anchors changed into top anchor.
    #TILDE_ANCHORS = ['Utilde', 'ytilde', 'lowtildemod', 'atilde', 'ohorntilde', 'utilde', 'Uhorntilde', 'Ntilde', 'Ytilde', 'Otilde', 
    #    'uhorntilde', 'Etilde', 'Ohorntilde', 'otilde', 'ntilde', 'vtilde', 'Atilde', 'tildeoverlaycomb', 'perispomenicomb', 
    #    'Vtilde', 'Itilde', 'etilde', 'itilde']

    _TOP_ANCHORS = ['Abreve.component', 'Abreve.component1', 'Abreve.component2', 'Abreve.component3', 'Idieresis.component', 'Otilde.component', 
        'Otilde.component1', 'Sacute.component', 'Scaron.component', 'Udieresis.component', 'Umacron.component', 'abreve.component', 
        'abreve.component1', 'abreve.component2', 'abreve.component3', 'acomb', 'acutecomb', 'acutecomb.component', 'acutecomb.component1', 
        'acutecomb.component3', 'acutecomb.component5', 'acutedottedcomb', 'acutegraveacutecomb', 'acutemacroncomb', 'acutetonecomb', 'almostequaltoabovecomb', 
        'arrowheadleftabovecomb', 'arrowheadrightabovecomb', 'asteriskabovecomb', 'brevecomb', 
        'brevecomb.component', 'breveinvertedcomb', 'breveinverteddoublecomb', 'candrabinducomb', 'caroncomb', 'ccomb', 'circumflexcomb', 
        'commaabovecomb', 'commaaboverightcomb', 'commareversedabovecomb', 'commaturnedabovecomb', 'dasiapneumatacomb-cy', 
        'dblgravecomb', 'dbloverlinecomb', 'dblverticallineabovecomb', 'dcomb', 'dialytikatonoscomb', 
        'dieresiscomb', 'dotaboverightcomb', 'dotaccentcomb', 'doublebrevecomb', 'doublemacroncomb', 'ecomb', 'fermatacomb', 
        'gbridgeabovecomb', 'graphemejoinercomb', 'graveacutegravecomb', 'gravecomb', 'gravecomb.component', 'gravecomb.component1', 
        'gravecomb.component3', 'gravedottedcomb', 'gravemacroncomb', 'gravetonecomb', 'hardsigncomb-cy', 'hcomb', 'homotheticabovecomb', 'hookabovecomb', 
        'hookabovecomb.component', 'horncomb', 'hungarumlaut', 'hungarumlautcomb', 'icomb', 'idieresis.component', 'koroniscomb', 'leftangleabovecomb', 
        'lefthalfringabovecomb', 'macron', 'macronacutecomb', 'macroncomb', 'macroncomb.component', 'macroncomb.component1', 'macrongravecomb', 'mcomb', 
        'nottildeabovecomb', 'ocomb', 'otilde.component', 'otilde.component1', 'overlinecomb', 'palatalizationcomb-cy', 
        'perispomenicomb', 'pokrytiecomb-cy', 'psilipneumatacomb-cy', 'rcomb', 'righthalfringabovecomb', 
        'ring', 'ringcomb', 'ringhalfright', 'sacute.component', 'scaron.component', 'softsigncomb-cy', 'suspensioncomb', 'tcomb', 'tilde', 
        'tildecomb', 'tildecomb.component', 'tildedoublecomb', 'tildeverticalcomb', 'titlocomb-cy', 'tonos', 'ucomb', 'udieresis.component', 
        'umacron.component', 'uni047E.component', 'vcomb', 'verticallineabovecomb', 'xabovecomb', 'xcomb', 'zigzagabovecomb',
        'ringhalfleft', 
        
        #'six.pnum_enclosingkeycapcomb',
        #'three.pnum_enclosingkeycapcomb',
        #'five.pnum_enclosingkeycapcomb',
        #'millionssigncomb-cy',
        #'seven.pnum_enclosingkeycapcomb',
        #'eight.pnum_enclosingkeycapcomb',
        #'hundredthousandssigncomb-cy',
        #'four.pnum_enclosingkeycapcomb',
        #'nine.pnum_enclosingkeycapcomb',
        #'zero.pnum_enclosingkeycapcomb',
        #'one.pnum_enclosingkeycapcomb',
        #'two.pnum_enclosingkeycapcomb]',
    ]

    _MIDDLE_ANCHORS = ['slashlongcomb', 'strokelongcomb', 'strokeshortcomb', 'slashshortcomb', 'tildeoverlaycomb',
        'middlegraveaccentmod', 'dagesh-hb',]

    _BOTTOM_ANCHORS = ['acutebelowcomb', 'arrowdoublerightbelowcomb', 'arrowheadleftbelowcomb', 'arrowheadrightbelowcomb', 'arrowheadrightheadupbelowcomb', 
    'arrowleftrightbelowcomb', 'arrowupbelowcomb', 'asteriskbelowcomb', 'brevebelow', 'breveinvertedbelowcomb', 'bridgebelowcomb', 'bridgeinvertedbelowcomb', 
    'caronbelowcomb', 'cedillacomb', 'cedillacomb.component', 'circumflexbelow', 'circumflexbelowcomb', 'commaaccentcomb', 
    'dblarchinvertedbelowcomb', 'dbllowlinecomb', 'dieresisbelow', 'dotbelowcomb', 'doublebrevebelowcomb', 'doubleringbelowcomb', 'doubleverticallinebelowcomb', 
    'downtackbelowcomb', 'equalbelowcomb', 'gravebelowcomb', 'leftanglebelowcomb', 'lefttackbelowcomb', 'lowlinecomb', 'macronbelow', 
    'macronbelowcomb', 'minusbelowcomb', 'ogonekcomb', 'palatalhookcomb', 'plusbelowcomb', 'prosgegrammeni', 'rbelowcomb', 'retroflexhookcomb', 'righttackbelowcomb', 
    'ringbelow', 'ringbelowcomb', 'ringhalfleftbelowcomb', 'ringhalfrightbelowcomb', 'seagullbelowcomb', 'snakebelowcomb', 'squarebelowcomb', 'tildebelow', 
    'uptackbelowcomb', 'verticallinebelowcomb', 'xbelowcomb', 'ypogegrammenicomb', 'dblmacronbelowcomb', 'voicingmod', 'lowringmod',
    'arrowheadrightheaddownbelow',
        #'six.pnum_enclosingkeycapcomb',
        #'three.pnum_enclosingkeycapcomb',
        #'five.pnum_enclosingkeycapcomb',
        #'millionssigncomb-cy',
        #'seven.pnum_enclosingkeycapcomb',
        #'eight.pnum_enclosingkeycapcomb',
        #'hundredthousandssigncomb-cy',
        #'four.pnum_enclosingkeycapcomb',
        #'nine.pnum_enclosingkeycapcomb',
        #'zero.pnum_enclosingkeycapcomb',
        #'one.pnum_enclosingkeycapcomb',
        #'two.pnum_enclosingkeycapcomb]',
    ]

    _OGONEK_ANCHORS = ['ogonek']

    _DOT_ANCHORS = ['dotmiddle.component']

    _TONOS_ANCHORS = ['dasia-uc', 'dasiaoxia-uc', 'dasiaperispomeni-uc', 'dasiavaria-uc', 'oxia-uc', 'psili-uc', 'psilioxia-uc', 'psiliperispomeni-uc', 
    'psilivaria-uc', 'tonos-uc', 'varia-uc']

    _VERT_ANCHORS = ['caronvert.component']

    ANCHORS = {
        TOP_: TOP_ANCHORS,
        MIDDLE_: MIDDLE_ANCHORS,
        BOTTOM_: BOTTOM_ANCHORS,
        OGONEK_: OGONEK_ANCHORS, 
        DOT_: DOT_ANCHORS, 
        TONOS_: TONOS_ANCHORS,
        VERT_: VERT_ANCHORS,
        _TOP: _TOP_ANCHORS, 
        _MIDDLE: _MIDDLE_ANCHORS, 
        _BOTTOM: _BOTTOM_ANCHORS,
        _OGONEK: _OGONEK_ANCHORS, 
        _DOT: _DOT_ANCHORS, 
        _TONOS: _TONOS_ANCHORS,
        _VERT: _VERT_ANCHORS,
    }

    for anchorName, gNames in ANCHORS.items():
        for gName in gNames:
            GLYPH_DATA[gName].anchors.add(anchorName)

    # Add gid
    """
    uni = {}
    for name, d in GLYPHSET4.items():
        if d['uni']:
            uni[d['uni']] = (name, d)
    gid = 2
    for uni, (name, d) in sorted(uni.items()):
        if not 'gid' in GLYPHSET4[name]:
            GLYPHSET4[name]['gid'] = gid
            gid += 1
    for name, d in sorted(GLYPHSET4.items()):
        if not 'gid' in GLYPHSET4[name]:
            GLYPHSET4[name]['gid'] = gid
            gid += 1
    """
    # Add tonos spacing
    # Glyph that contain a tonos anchor (== they have a component with "-uc" in the name)
    
    TONOS = """Alphatonos Alphapsili Alphadasia Alphapsilivaria Alphadasiavaria Alphapsilioxia Alphadasiaoxia Alphapsiliperispomeni Alphadasiaperispomeni Alphavaria Epsilontonos Epsilonpsili Epsilondasia Epsilonpsilivaria Epsilondasiavaria Epsilonpsilioxia Epsilondasiaoxia Epsilonvaria Etatonos Etapsili Etadasia Etapsilivaria Etadasiavaria Etapsilioxia Etadasiaoxia Etapsiliperispomeni Etadasiaperispomeni Etavaria Iotatonos Iotapsili Iotadasia Iotapsilivaria Iotadasiavaria Iotapsilioxia Iotadasiaoxia Iotapsiliperispomeni Iotadasiaperispomeni Iotavaria Omicrontonos Omicronpsili Omicrondasia Omicronpsilivaria Omicrondasiavaria Omicronpsilioxia Omicrondasiaoxia Omicronvaria Rhodasia Upsilontonos Upsilondasia Upsilondasiavaria Upsilondasiaoxia Upsilondasiaperispomeni Upsilonvaria Omegatonos Omegapsili Omegadasia Omegapsilivaria Omegadasiavaria Omegapsilioxia Omegadasiaoxia Omegapsiliperispomeni Omegadasiaperispomeni Omegavaria UpsilonacutehookSymbol Alphaoxia Epsilonoxia Etaoxia Iotaoxia Upsilonoxia Omicronoxia Omegaoxia Alphapsiliprosgegrammeni Alphadasiaprosgegrammeni Alphapsilivariaprosgegrammeni Alphadasiavariaprosgegrammeni Alphapsilioxiaprosgegrammeni Alphadasiaoxiaprosgegrammeni Alphapsiliperispomeniprosgegrammeni Alphadasiaperispomeniprosgegrammeni Etapsiliprosgegrammeni Etadasiaprosgegrammeni Etapsilivariaprosgegrammeni Etadasiavariaprosgegrammeni Etapsilioxiaprosgegrammeni Etadasiaoxiaprosgegrammeni Etapsiliperispomeniprosgegrammeni Etadasiaperispomeniprosgegrammeni Omegapsiliprosgegrammeni Omegadasiaprosgegrammeni Omegapsilivariaprosgegrammeni Omegadasiavariaprosgegrammeni Omegapsilioxiaprosgegrammeni Omegadasiaoxiaprosgegrammeni Omegapsiliperispomeniprosgegrammeni Omegadasiaperispomeniprosgegrammeni"""
    TONOS = set(TONOS.split(' '))
    for name, gd in GLYPHSET4.items():
        if name in TONOS:
            d.spacing'] = 'tonos'
    for name, d in sorted(GLYPHSET4.items()):
        print("\t'%s': %s," % (name, d))
    

    gid = 3000
    GID = {}
    for name, gd in GLYPH_DATA.items():
        if not gd.gid:
            gd.gid = gid
            gid += 1
        GID[gd.gid] = name

    GLYPH_ORDER = []
    for gid, name in sorted(GID.items()):
        GLYPH_ORDER.append(name)
    UNI = {}
    for name, gd in GLYPH_DATA.items():
        if gd.uni:
            UNI[gd.uni] = gd

    # X-ref on unicode and the usage of components.
    # GLYPH_DATA['E'].composites now is a list with all glyphs that use /E as a base component.

    UNICODE2GLYPH = {} # Key is unicode, value is name (only for glyphs that have a unicode)

    for gName, gd in sorted(GLYPH_DATA.items()):
        
        if gd.uni:
            #assert gd.uni not in UNICODE2GLYPH, ("Unicode %04x already defined for /%s" % (gd.uni, gName))
            UNICODE2GLYPH[gd.uni] = gd.name
        
    for gName, gd in sorted(GLYPH_DATA.items()):
        gdBase = None
        if gd.base is not None: # Make the x-ref base reference.
            gdBase = GLYPH_DATA[gd.base]
            gdBase.composites.add(gName)
        for accentName in gd.accents: # It's an accent, x-ref this glyph to accents
            if accentName in ACCENT_DATA:
                ad = ACCENT_DATA[accentName]
                if not 'composites' in ad:
                    ad['composites'] = set()
                ad['composites'].add(gName)
                for accentAnchor in ad['anchors']:
                    if gdBase is not None:  
                        gdBase.anchors.add(CONNECTED_ANCHORS[accentAnchor])
                    gdAccent = GLYPH_DATA[accentName]
                    gdAccent.anchors.add(accentAnchor)

    #print(GLYPH_DATA['alpha'].composites)
    #print('alphapsilivariaypogegrammeni' in GLYPH_DATA['alpha'].composites)
    #print('alphadasiavariaypogegrammeni' in GLYPH_DATA['alpha'].composites)



    ACCENTED_BASE = {} # Key is base glyph, value is list of accented glyphs
    ACCENTS_ON_GLYHPS = {} # X-ref of all glyphs (value) that have an accent (key)
    for glyphName, gd in GLYPH_DATA.items():
        if gd.base not in ACCENTED_BASE:
            ACCENTED_BASE[gd.base] = [] # Store the base name of glyphs that need an accent
        ACCENTED_BASE[gd.base].append(glyphName)
        for accentName in gd.accents:
            if accentName not in ACCENTS_ON_GLYHPS:
                ACCENTS_ON_GLYHPS[accentName] = []
            ACCENTS_ON_GLYHPS[accentName].append(glyphName)

    # X-ref for all glyphs that have components referring to them
    # Key is base glyph, value is list of referring glyph names 
    COMPOSITES_BASE = {}
    for glyphName, gd in GLYPH_DATA.items():
        if gd.uni and (gd.base or gd.accents):
            componentNames = [gd.base] + list(gd.accents)
            for componentName in componentNames:
                if not componentName in COMPOSITES_BASE:
                    COMPOSITES_BASE[componentName] = []
                COMPOSITES_BASE[componentName].append(glyphName)

    # Split the black into versions
    #   V1 Latin (including all glyphs that already have been done by Léna) + diacritics
    #   V2 Cyrillic
    #   V3 Greek + Greek diacritics
    #   V4 Superiors, inferiors, currency, graphic symbols, figures in circles/squares
    for name, gd in GLYPH_DATA.items():
        if '-cy' in name:
            gd.blackVersion = 2

    # Collect all source glyph with their depending glyphs for margins
    GLYPH2SPACING_CHILDREN = {}
    for glyphDataSet, glyphSpacingSet in (
            (GLYPH_DATA, GLYPH2SPACING_CHILDREN),):
        for name, gd in glyphDataSet.items():
            if gd.leftSpaceSource is not None:
                if gd.leftSpaceSource not in glyphSpacingSet:
                    glyphSpacingSet[gd.leftSpaceSource] = set()
                glyphSpacingSet[gd.leftSpaceSource].add(name)
            if gd.rightSpaceSource is not None:
                if gd.rightSpaceSource not in glyphSpacingSet:
                    glyphSpacingSet[gd.rightSpaceSource] = set()
                glyphSpacingSet[gd.rightSpaceSource].add(name)

    UNI2GLYPH_DATA = {}
    CHAR2GLYPH_DATA = {}
    for glyphDataSet, uni2GlyphData, char2GlyphData in [
            (GLYPH_DATA, UNI2GLYPH_DATA, CHAR2GLYPH_DATA),
        ]:
        for name, gd in glyphDataSet.items():
            if gd.uni:
                uni2GlyphData[gd.uni] = gd 
                char2GlyphData[chr(gd.uni)] = gd

        # Check if all GLYPH_SUBSET have a glyph data entry.
        for gName, gd in glyphDataSet.items():
            if gName in ('.notdef', '.null'):
                continue
            if gd.c and not ord(gd.c) in uni2GlyphData:  
                print('### No glyph data %s %04x for CHARS_SUBSET' % (gd.c, ord(gd.c)))

    # Build groups from fields gd.g1 and gd.g2 of individual glyphs
    GROUPS1 = {} # Key is group name, value is set/list of glyph names
    GROUPS2 = {} # Key is group name, value is set/list of glyph names
    GLYPH2GROUP1 = {} # Key is glyph name, value is name of group 1
    GLYPH2GROUP2 = {}

    GLYPH_NOT_IN_GROUPS1 = ['.notdef', '.null']
    GLYPH_NOT_IN_GROUPS2 = ['.notdef', '.null']
    for gName in GLYPH_DATA.keys():
        if '.tab' in gName or 'cmb' in gName: #'flourish' in gName or 
            GLYPH_NOT_IN_GROUPS1.append(gName)
            GLYPH_NOT_IN_GROUPS2.append(gName)
        elif '.cbr' in gName:
            GLYPH_NOT_IN_GROUPS1.append(gName)

    for gds, groups1, groups2, g2g1, g2g2, not1, not2 in (
        (GLYPH_DATA, 
            GROUPS1, GROUPS2, 
            GLYPH2GROUP1, GLYPH2GROUP2,
            GLYPH_NOT_IN_GROUPS1, GLYPH_NOT_IN_GROUPS2),
        ):
            for gName, gd in gds.items():
                # Build groups and x-ref glyph-->group dictionarys
                if gName not in not1:
                    gd.g1 = gd.g1 or gd.base or gName
                    if gName.endswith('.sc') and not gd.g1.endswith('.sc'):
                        gd.g1 += '.sc'
                    if gd.g1 not in groups1:
                        groups1[gd.g1] = []
                    groups1[gd.g1].append(gName)
                    assert gName not in g2g1 # Glyph to group1 
                    g2g1[gName] = gd.g1

                if gName not in not2:
                    gd.g2 = gd.g2 or gd.base or gName
                    if gName.endswith('.sc') and not gd.g2.endswith('.sc'):
                        gd.g2 += '.sc'
                    if gd.g2 not in groups2:
                        groups2[gd.g2] = []
                    groups2[gd.g2].append(gName)
                    assert gName not in g2g2 # Glyph to group2 
                    g2g2[gName] = gd.g2

    #print('GROUPS 2', GROUPS2.keys())
    #print(GLYPH_NOT_IN_GROUPS1)
    #print('-----')
    #print('GROUPS 1', GROUPS1.keys())
    #print(GLYPH_NOT_IN_GROUPS2)
    #print('=====')

    def getGlyphData(f):
        return GLYPH_DATA

    #print(GLYPH_DATA['A'])
    #print(GLYPH_DATA['Agrave'])
    #print(GLYPH_DATA['e'])
    #print(GLYPH_DATA['gravecmb'])

    GROUPS1 = {}
    GROUPS2 = {}
    GLYPH2GROUP1 = {}
    GLYPH2GROUP2 = {}
    GLYPH2GROUPNAME1 = {}
    GLYPH2GROUPNAME2 = {}

    for glyphDataSet, groups1, groups2, glyph2Group1, glyph2Group2, glyph2GroupName1, glyph2GroupName2,  in [
            (GLYPH_DATA, GROUPS1, GROUPS2, GLYPH2GROUP1, GLYPH2GROUP2, GLYPH2GROUPNAME1, GLYPH2GROUPNAME2)]:
        for name, gd in glyphDataSet.items():
            if not gd.g1 in groups1:
                groups1[gd.g1] = []
            groups1[gd.g1].append(name)
            if not gd.g2 in groups2:
                groups2[gd.g2] = []
            groups2[gd.g2].append(name)
            glyph2Group1[name] = groups1[gd.g1]
            glyph2Group2[name] = groups2[gd.g2]
            glyph2GroupName1[name] = 'public.kern1.' + gd.g1
            glyph2GroupName2[name] = 'public.kern2.' + gd.g2

class GlyphSet:
    """Offers functions for the glyphset."""
    MIN_RIGHT = -200
    WORD_SPACE = 200 # Defailt word space
    TOP_Y = 700
    ANCHOR_OFFSET = 16

    SMALL_TRACK = 6 # Value to add to Small margins when copied from Display masters. Glyph can have individual corrections.

    SCALE_SC_MARGINS = 1 # No scaling? Copy from capital spacin on SC. instead of 0.85

    # Standard anchor names
    _TOP = '_top'
    TOP_ = 'top'
    _BOTTOM = '_bottom'
    BOTTOM_ = 'bottom'
    _RING = '_ring'
    RING_ = 'ring'
    _OGONEK = '_ogonek'
    OGONEK_ = 'ogonek'
    _VERT = '_vert'
    VERT_ = 'vert'
    _DOT = '_dot'
    DOT_ = 'dot'
    _TILDE = '_tilde'
    TILDE_ = 'tilde'
    #_TONOS = '_tonos'
    #TONOS_ = 'tonos'
    #_HORN = '_horn'
    #HORN_ = 'horn'
    _MIDDLE = '_middle'
    MIDDLE_ = 'middle'
    # Flourish connector anchors, 9 optional connection points
    _TOPLEFT = '_topLeft'
    TOPLEFT_ = 'topLeft'
    _TOPCENTER = '_topCenter'
    TOPCENTER_ = 'topCenter'
    _TOPRIGHT = '_topRight'
    TOPRIGHT_ = 'topRight'

    _MIDDLELEFT = '_middleLeft'
    MIDDLELEFT_ = 'middleLeft'
    _MIDDLECENTER = '_middleCenter'
    MIDDLECENTER_ = 'middleCenter'
    _MIDDLERIGHT = '_middleRight'
    MIDDLERIGHT_ = 'middleRight'

    _BOTTOMLEFT = '_bottomLeft'
    BOTTOMLEFT_ = 'bottomLeft'
    _BOTTOMCENTER = '_bottomCenter'
    BOTTOMCENTER_ = 'bottomCenter'
    _BOTTOMRIGHT = '_bottomRight'
    BOTTOMRIGHT_ = 'bottomRight'

    _OPENLEFT = '_openLeft'
    OPENLEFT_ = 'openLeft'
    _OPENRIGHT = '_openRight'
    OPENRIGHT_ = 'openRight'

    _OPENTOP = '_openTop'
    OPENTOP_ = 'openTop'
    _OPENBOTTOM = '_openBottom'
    OPENBOTTOM_ = 'openBottom'

    CONNECTED_ANCHORS = {
        _TOP: TOP_,
        _BOTTOM: BOTTOM_,
        _RING: RING_,
        _OGONEK: OGONEK_,
        _VERT: VERT_,
        _DOT: DOT_,
        _TILDE: TILDE_,
        #_TONOS: TONOS_, # Also anchor of the other -uc accents
        #_HORN: HORN_,
        _MIDDLE: MIDDLE_,
        # Flourishes connector anchors
        _TOPLEFT: TOPLEFT_,
        _TOPCENTER: TOPCENTER_,
        _TOPRIGHT: TOPRIGHT_,
        _MIDDLELEFT: MIDDLELEFT_,
        _MIDDLECENTER: MIDDLECENTER_,
        _MIDDLERIGHT: MIDDLERIGHT_,
        _BOTTOMLEFT: BOTTOMLEFT_,
        _BOTTOMCENTER: BOTTOMCENTER_,
        _BOTTOMRIGHT: BOTTOMRIGHT_,
        # Open terminals, not connected to glyphs in case top/bottom/middleLeft/middleRight don't exist
        _OPENLEFT: OPENLEFT_,
        _OPENRIGHT: OPENRIGHT_,
        _OPENTOP: OPENTOP_,
        _OPENBOTTOM: OPENBOTTOM_,
    }

    CENTER = 'CENTER'

    ACCENT_DATA = {
        'acutecmb': dict(anchor=_TOP, composites=set()),
        'brevecmb': dict(anchor=_TOP, composites=set()),
        'caroncmb': dict(anchor=_TOP, composites=set()),
        'caroncmb.vert': dict(anchor=_VERT, composites=set()),
        'cedillacmb': dict(anchor=_BOTTOM, composites=set()),
        'circumflexcmb': dict(anchor=_TOP, composites=set()),
        'macroncmb': dict(anchor=_TOP, composites=set()),
        'ogonekcmb': dict(anchor=_OGONEK, composites=set()),
        'eogonekcmb': dict(anchor=_OGONEK, composites=set()),
        'dieresiscmb': dict(anchor=_TOP, composites=set()),
        'dotaccentcmb': dict(anchor=_TOP, composites=set()),
        'gravecmb': dict(anchor=_TOP, composites=set()),
        'hungarumlautcmb': dict(anchor=_TOP, composites=set()),
        'ringcmb': dict(anchor=_TOP, composites=set()),
        'ringacutecmb': dict(anchor=_TOP, composites=set()),
        'tildecmb': dict(anchor=_TOP, composites=set()),
        'dotmiddlecmb': dict(anchor=_MIDDLE, composites=set()),
        'commabelowcmb': dict(anchor=_BOTTOM, composites=set()),
        'commaturnedabovecmb': dict(anchor=_TOP, composites=set()),
        #'commaaccenttopcmb': dict(anchor=_TOP, composites=set()),

        'acutecmb.uc': dict(anchor=_TOP, composites=set()),
        'brevecmb.uc': dict(anchor=_TOP, composites=set()),
        'caroncmb.uc': dict(anchor=_TOP, composites=set()),
        'circumflexcmb.uc': dict(anchor=_TOP, composites=set()),
        'macroncmb.uc': dict(anchor=_TOP, composites=set()),
        'dieresiscmb.uc': dict(anchor=_TOP, composites=set()),
        'dotaccentcmb.uc': dict(anchor=_TOP, composites=set()),
        'gravecmb.uc': dict(anchor=_TOP, composites=set()),
        'hungarumlautcmb.uc': dict(anchor=_TOP, composites=set()),
        'ringcmb.uc': dict(anchor=_TOP, composites=set()),
        'ringacutecmb.uc': dict(anchor=_TOP, composites=set()),
        'tildecmb.uc': dict(anchor=_TOP, composites=set()),
        'commaturnedabovecmb.uc': dict(anchor=_TOP, composites=set()),
    }
    ANCHOR_FLOURISH_SAMPLE = {}
    for accentName, ad in sorted(ACCENT_DATA.items()):
        anchorName = CONNECTED_ANCHORS[ad['anchor']]
        if anchorName not in ANCHOR_FLOURISH_SAMPLE and accentName.startswith('flourish'): # Just need one sample per anchor
            ANCHOR_FLOURISH_SAMPLE[anchorName] = accentName

    ALL_ANCHORS = (BOTTOM_, BOTTOMLEFT_, BOTTOMRIGHT_, MIDDLERIGHT_, MIDDLELEFT_, TOP_, TOPLEFT_, TOPRIGHT_)
    ALL_IJ_ANCHORS = (BOTTOM_, BOTTOMLEFT_, BOTTOMRIGHT_, MIDDLERIGHT_, MIDDLELEFT_, TOP_, TOPLEFT_, TOPRIGHT_, OGONEK_)
    CARON_ANCHORS = (BOTTOM_, BOTTOMLEFT_, BOTTOMRIGHT_, MIDDLERIGHT_, MIDDLELEFT_, TOP_, TOPLEFT_, TOPRIGHT_, VERT_)
    '''

GD = GlyphData

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

