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
#
from assistantLib.assistantParts.glyphsets.anchorData import AD 

class GlyphData:
    """Glyph data element that contains all individual data for glyphs.

    >>> gd = GlyphData(l2r='A', uni=65, c='A', name='A', srcName='A', hex='0041', comment='A Uppercase Alphabet, Latin', gid=35)
    >>> gd
    <GlyphData A>
    >>> gd.uni
    65
    >>> gd = GlyphData = GD(uni=193, name='Aacute', base='A', accents=['acutecmb'])
    >>> gd.c
    'Á'
    >>> gd.hex
    '00C1'
    >>> gd.components
    ['A', 'acutecmb']
    """    
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
    CAT_EM_WIDTH2 = 'emWidth/2' # Half emWidth
    CAT_WORD_SPACE = 'wordSpace'
    # Categories of height
    CAT_XHEIGHT = 'xHeight'
    CAT_XHEIGHT2 = 'xHeight/2'
    CAT_CAP_HEIGHT = 'capHeight'
    CAT_CAP_HEIGHT2 = 'capHeight/2'
    CAT_SC_HEIGHT = 'scHeight'
    CAT_SC_HEIGHT2 = 'scHeight/2'
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
    CAT_WIDTHS = (None, CAT_ACCENT_WIDTH, CAT_TAB_WIDTH, CAT_MATH_WIDTH, CAT_EM_WIDTH, CAT_EM_WIDTH2, CAT_WORD_SPACE)

    def __init__(self, uni=None, c=None, gid=None, name=None, srcName=None, hex=None, composites=None,
            unicodes=None, 
            # Define component reference glyph names.
            base=None, accents=None, 
            comment=None, spacing=None, fixAccents=True, fixSpacing=True, fixAnchors=False, 
            rightMin=None, top_y=None, 
            # Anchors
            # Force list of anchor names. Otherwise try to compose the list from the anchors that this glyph is associated with in AD.ANCHORS. 
            anchors=None, 
            anchorSrc=None, # Master name to copy anchors from
            anchorTopX=None, # Constructor method name or glyph name to copy guessed horizontal anchor positions from, overwriting the search for base glyph, fixed positions and bounds matching
            anchorTopY=None, # Constructor method name or glyph name to copy guessed vertical anchor positions from, overwriting the search for base glyph, fixed positions and bounds matching
            anchorMiddleX=None, 
            anchorMiddleY=None, 
            anchorBottomX=None, 
            anchorBottomY=None, 
            # Force spacing dependencies
            l=None, r=None, w=None, 
            bl=None, br=None, # Based glyph references
            l2r=None, r2l=None, bl2r=None, br2l=None, l2br=None, r2bl=None, bl2br=None, br2bl=None, # Switch margins
            # Type of glyph. Guess if undefined as None.
            isLower=None, isMod=None, isSc=None,
            # Italicize forcing conversion behavior
            useSkewRotate=False, addItalicExtremePoints=True, 
            # Glyphs to copy from, initially before editing starts
            src=None, # Not used here
            src180=None, # Not used here
            # Components
            autoFixComponentPositions=True,
            # Groups
            g1=None, g2=None, 
            ascender=None, descender=None, 
            # In case hard value needs to overwrite category value, use numbers
            # Otherwise categories of vertical metrics or None. They overwrite the master-wide guessed value by parent MasterData
            overshoot=None, height=None, baseline=None, width=None,
            ): 
        self.parent = None # 
        self.uni = uni
        self.unicodes = unicodes
        if c is None and uni:
            c = chr(uni)
        self.c = c
        if uni is not None:
            uniHex = '%04X' % uni
            if hex is not None:
                hex = hex.upper()
                assert hex == uniHex, (hex, uniHex)
            hex = uniHex
        self.hex = hex
        self.gid = gid # Glyph id
        assert name is not None
        self.name = name
        if srcName == name:
            srcName = None
        self.srcName = srcName

        self.composites = set() # Glyph names that refer to self as component. Collected by GlyphSet

        # If anchors is not defined (overwriting legacy data), then compose the anchor list from AD.ANCHORS
        if anchors is None:
            anchors = []
            for anchorName, glyphNames in AD.GLYPH_ANCHORS.items():
                if self.name in glyphNames:
                    anchors.append(anchorName)
        self.anchors = sorted(anchors) # (Sorted) list of anchor names for this glyph
        self.anchorSrc = anchorSrc # Master name to copy anchors from
        # More to be added if needed in the future
        self.anchorTopX = anchorTopX # Constructor method name or glyph name to copy guessed horizontal anchor positions from, overwriting the search for base glyph, fixed positions and bounds matching
        self.anchorTopY = anchorTopY # Constructor method name or glyph name to copy guessed vertical anchor positions from, overwriting the search for base glyph, fixed positions and bounds matching
        self.anchorMiddleX = anchorMiddleX 
        self.anchorMiddleY = anchorMiddleY 
        self.anchorBottomX = anchorBottomX 
        self.anchorBottomY = anchorBottomY 

        # Flag to prevent assistant moving components, even in auto mode. They will be name fixed and created still
        self.autoFixComponentPositions = autoFixComponentPositions 

        self._isLower = isLower # If not None, force the flag. Otherwise try to guess.
        self._isSc = isSc # Is smallcap
        self._isMod = isMod # Glyph is a modifier.

        self.base = base # Base component if used
        self.accents = accents or [] # List of other component names, besides the base. Tested on by property self.hasDiacritics

        self.comment = comment or ''
        self.spacing = spacing # Obsolete?

        self.l = l # Overall angled left margin of referenced glyph
        self.r = r # Overall angled right margin of referenced glyph
        self.w = w # Width of referenced glyph
        self.bl = bl # Left of base glyph
        self.br = br # Right of base glyph
        self.l2r = l2r # Switch margins
        self.r2l = r2l
        self.bl2r = bl2r # Base left to right
        self.br2l = br2l # Base right to left
        self.l2br = l2br # Left to base right
        self.r2bl = r2bl # Right to base left
        self.bl2br = bl2br # Base left to base right
        self.br2bl = br2bl # Base right to base left

        # Deprecated legacy references
        #self.il = il
        #self.ir = ir
        #self.iw = iw
        #self.il2r = il2r
        #self.ir2l = ir2l 

        self.fixAccents = fixAccents
        self.fixAnchors = fixAnchors
        self.fixSpacing = fixSpacing
        self.rightMin = rightMin

        self.g1 = g1 or self.name # Name of group 1, right of glyph, left of kerning pair
        self.g2 = g2 or self.name # Name of group 2, left of glyph, right of kerning pair

        self.useSkewRotate = useSkewRotate # Boolean flag if this glyph uses the combination of skew+rotate (as defined in the MasterData)
        self.addItalicExtremePoints = addItalicExtremePoints # If italic rotation is done, then add new extreme points

        self.ascender = ascender
        self.descender = descender

        # These values must be valid category names or real numbers or can be None
        assert overshoot in self.CAT_OVERSHOOTS or isinstance(overshoot, (int, float))
        assert height in self.CAT_HEIGHTS or isinstance(height, (int, float))
        assert baseline in self.CAT_BASELINES or isinstance(baseline, (int, float))
        assert width in self.CAT_WIDTHS or isinstance(width, (int, float))
        self.overshoot = overshoot # Hard value or category name
        self.height = height
        self.baseline = baseline
        self.width = width

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
        return self.name.endswith(self.MOD)
    isMod = property(_get_isMod)

    def _get_isSups(self):
        return self.name.endswith(self.MOD_SUPS)
    isSups = property(_get_isSups)
            
    def _get_isSinf(self):
        return self.name.endswith(self.MOD_SINF)
    isSinf = property(_get_isSinf)
            
    def _get_isNumr(self):
        return self.name.endswith(self.MOD_NUMR)
    isNumr = property(_get_isNumr)
            
    def _get_isDnom(self):
        return self.name.endswith(self.MOD_DNOM)
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
    
    def _get_isDiacritic(self):
        """Answer the boolean flag if this glyph is a diacritic."""
        return self.name in AD.ACCENT_DATA
    isDiacritic = property(_get_isDiacritic)

    def _get_hasDiacritics(self):
        """Answer the boolean flag is this glyph has diacritics components."""
        for componentName in self.accents:
            if componentName in AD.ACCENT_DATA:
                return True
        return False
    hasDiacritics = property(_get_hasDiacritics)
    
    def _get_components(self):
        """Answer the list of all component names. An empty list if there are no components in the glyph."""
        components = []
        if self.base is not None:
            components.append(self.base)
        if self.accents:
            components += self.accents 
        return components
    components = property(_get_components)

    def asSourceLine(self):
        """Answer the string of self as Python code that will reproduce self as instance."""
        out = f"""       '{self.name}': GD(name='{self.name}'"""
        if self.uni is not None:
            if self.name == '.null': # Special case
                out += """, uni=0x%04X, hex='%04X'""" % (self.uni, self.uni)
            elif self.name == 'quotesingle': # Special case
                out += """, uni=0x%04X, hex='%04X', c="%s" """ % (self.uni, self.uni, chr(self.uni))
            elif self.name == 'backslash': # Special case
                out += """, uni=0x%04X, hex='%04X', c="\\%s" """ % (self.uni, self.uni, chr(self.uni))
            else:
                out += ", uni=0x%04X, hex='%04X', c='%s'" % (self.uni, self.uni, chr(self.uni))
        if self.unicodes:
            out += f", unicodes=%s" % str(self.unicodes)
        for spaceType in ('l', 'r', 'w', 'bl', 'br', 'l2r', 'r2l', 'bl2r', 'br2l', 'l2br', 'r2bl', 'bl2br', 'br2bl', ):
            v = getattr(self, spaceType)
            if v is not None:
                out += ", %s='%s'" % (spaceType, v)
        if self.rightMin:
            out += f", rightMin='%s'" % self.rightMin
        if self.g1 and self.g1 != self.name:
            out += f", g1='{self.g1}'"
        if self.g2 and self.g2 != self.name:
            out += f", g2='{self.g2}'"
        if self.base:
            out += f", base='{self.base}'"
        if self.accents:
            out += f""", accents=['{"', '".join(self.accents)}']"""
        if self.srcName: # Glyph name of source to copy from
            out += ", srcName='%s'" % self.srcName
        if self.isLower:
            out += ", isLower=True"
        if self.isMod:
            out += ", isMod=True"
        if self.isSc:
            out += ", isSc=True"
        if not self.fixAccents: # Default is True
            out += ', fixAccents=False'
        if not self.fixSpacing: # Default is True
            out += ', fixSpacing=False'
        if self.fixAnchors: # Default is False
            out += ', fixAnchors=True'
        if self.useSkewRotate: # Default is False
            out += ', useSkewRotate=True'
        if not self.addItalicExtremePoints: # Default is True
            out += ', addItalicExtremePoints=False'
        if self.ascender is not None: # Allows overwriting per glyph
            out += ', ascender=%d' % self.ascender
        
        # Anchors
        if self.anchors:
            out += f", anchors={self.anchors}"

        # Actual values
        if self.descender is not None: 
            out += ', descender=%d' % self.descender
        if self.overshoot is not None: # Allows overwriting per glyph
            out += ', overshoot=%d' % self.overshoot
        if self.height is not None: 
            out += ', height=%d' % self.height
        if self.baseline is not None: # Allows overwriting per glyph
            out += ', baseline=%d' % self.baseline
        if self.width is not None: # Allows overwriting per glyph
            out += ', width=%d' % self.width
        
        if self.gid: # Glyph ID
            out += ", gid=%d" % self.gid
        if self.comment: 
            out += ", comment='%s'" % self.comment.replace('\\', '\\\\').replace("""'""", '''"''')
        out += '),\n'
        return out

    def _set_w(self, w):
        self._w = w
    def _get_w(self):
        return self._w
    w = property(_get_w, _set_w)

    def _get_fixedLeft(self):
        return bool(self.l or self.bl or self.r2l or self.br2l or self.r2bl or self.br2bl)
    fixedLeft = property(_get_fixedLeft)
    
    def _get_fixedRight(self):
        return bool(self.r or self.mr or self.l2r or self.bl2r or self.l2br or self.bl2br or self.w)
    fixedRight = property(_get_fixedRight)
    
    def _get_leftSpaceSource(self):
        return self.l or self.bl or self.r2l or self.br2l or self.r2bl or self.br2bl or None
    leftSpaceSource = property(_get_leftSpaceSource)
    
    def _get_rightSpaceSource(self):
        return self.r or self.mr or self.l2r or self.bl2r or self.l2br or self.bl2br or self.w
    rightSpaceSource = property(_get_rightSpaceSource)
    
    def _get_leftSpaceSourceLabel(self):
        """Answer the string where this space gets from. Answer None if there is non source."""
        if self.l is not None:
            return f'Left /{self.l}'
        if self.bl is not None:
            return f'Base left /{self.bl}'
        if self.r2l is not None:
            return f'R-->L /{self.r2l}'
        if self.br2l is not None:
            return f'Base R-->L /{self.br2l}'
        if self.r2bl is not None:
            return f'R-->Base L /{self.r2bl}'
        if self.br2bl is not None:
            return f'Base R-->Base L /{self.br2bl}'
        if self.base is not None:
            return f'Base /{self.base}'
        return None
    leftSpaceSourceLabel = property(_get_leftSpaceSourceLabel)
        
    def _get_rightSpaceSourceLabel(self):
        """Answer the string where this space gets from. Answer None if there is non source."""
        if self.w is not None:
            return f'Width /{self.w}'
        if self.r is not None:
            return f'Right /{self.r}'
        if self.br is not None:
            return f'Base left /{self.br}'
        if self.l2r is not None:
            return f'L-->R /{self.l2r}'
        if self.bl2r is not None:
            return f'Base L-->R /{self.bl2r}'
        if self.l2br is not None:
            return f'L-->Base R /{self.l2br}'
        if self.bl2br is not None:
            return f'Base L-->Base R /{self.bl2br}'
        if self.base is not None:
            return f'Base /{self.base}'
        return None
    rightSpaceSourceLabel = property(_get_rightSpaceSourceLabel)

GD = GlyphData


