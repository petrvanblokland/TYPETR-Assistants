# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   TYPETR_full_set.py
#
from copy import deepcopy

from assistantParts.glyphsets.baseGlyphSet import EGlyph

class GD(BaseEGlyph):

    def __init__(self, uni=None, unicodes=None, c=None, name=None, comment=None,
    src=None, src180=None, base=None, accents=None, template=None, 
    composites=None, anchors=ALL_ANCHORS, hex=None, 
    l=None, r=None, w=None, il=None, ir=None, iw=None, ml=None, mr=None, 
    l2r=None, r2l=None, il2r=None, ir2l=None, isLower=False, useSkewRotate=False, addItalicExtremePoints=False, 
    g1=None, g2=None, 
    smallTrackLeft=SMALL_TRACK, smallTrackRight=SMALL_TRACK, # Flags to add tracking to the left/right margins for Small masters
    copyFromDisplayLeft=True, copyFromDisplayRight=True, # Flags to copy Small margins from Display margins
    # Labels for the type of value, as defined in the MASTERS_DATA.metrics. No values are stored here.
    baseline=BASELINE, height=None, overshoot=None, # Define only in case different from the main font metrics
    fixAccents=True, fixAnchors=True, rightMin=None, topY=None, italic=False, hasErrors=False):
        # Add x-ref and accent-component relations
        if uni is None and c is not None:
            uni = ord(c)
        elif uni is not None and c is None:
            c = chr(uni)
        else:
            assert (uni is None and c is None) or (c is not None and uni == ord(c)), ('### %s %s %s %s %s' % (name, uni, ord(c or ' '), c, chr(uni or 0)))
        self.uni = uni
        self.italic = italic
        if name is None and self.uni is not None:
            name = 'uni%04d' % self.uni
        assert name is not None
        self.name = name

        self.unicodes = unicodes
        self.isLower = isLower
        self.base = base
        if not src:
            src = []
        elif not isinstance(src, (list, tuple)):
            src = [src]
        self.src = src # Only copy from here if no components or contours
        if not src180:
            src180 = []
        elif not isinstance(src180, (list, tuple)):
            src180 = [src180]
        self.src180 = src180
        if not accents:
            accents = []
        self.accents = accents
        self.accents = accents
        self.template = template
        self.anchors = set(anchors) # Default is ALL_ANCHORS, unless specified differently
        if composites is None:
            composites = set()
        self.composites = composites
        if comment is None:
            comment = ''
            if self.c is not None:
                comment += self.c + ' - '
            comment += self.name
        self.comment = comment
        # Auto fill for .uc glyphs, if parameters are undefined
        if name.endswith('.uc'):
            if not base and not 'cmb' in name:
                self.base = name.replace('.uc', '')
            if not l:
                l = base
            if not r:
                r = base
        self.l = l 
        self.r = r
        self.w = w
        self.il = il
        self.ir = ir
        self.iw = iw
        self.ml = ml
        self.mr = mr
        self.l2r = l2r
        self.r2l = r2l
        self.il2r = il2r
        self.ir2l = ir2l

        self.smallTrackLeft = smallTrackLeft # Value to add tracking to left/right margins in Small masters (Default is SMALL_TRACK)
        self.smallTrackRight = smallTrackRight
        self.copyFromDisplayLeft = copyFromDisplayLeft # Flags to copy Small margins from Display margins (Default is True)
        self.copyFromDisplayRight = copyFromDisplayRight

        self.fixAccents = fixAccents
        self.fixAnchors = fixAnchors
        self.rightMin = rightMin
        self.topY = topY
        self.hasErrors = hasErrors
        self.useSkewRotate = useSkewRotate
        self.addItalicExtremePoints = addItalicExtremePoints

        self.g1 = g1 or self.name # Name of group 1, right of glyph, left of kerning pair
        self.g2 = g2 or self.name # Name of group 2, left of glyph, right of kerning pair

        # In case different from the font metrics, None otherwise
        self.baseline = baseline 
        if overshoot is None:
            if self.name.endswith('.sc'):
                overshoot = SC_OVERSHOOT
            elif name[0].upper() == name[0]:
                overshoot = CAP_OVERSHOOT
            else:
                overshoot = OVERSHOOT
        self.overshoot = overshoot
        if height is None:
            if self.name.endswith('.sc'):
                height = SC_HEIGHT
            elif name[0].upper() == name[0]:
                height = CAP_HEIGHT
            else:
                height = XHEIGHT
        self.height = height

    def isUpper(self):
        """Answer the flag if this is an upper case while not being a small cap"""
        if self.name[0] in ('.',):
            return False
        return self.name[0].upper() == self.name[0] and not self.name.endswith('.sc')

    def _get_scm(self):
        if self.name.endswith('.sc'):
            return SCALE_SC_MARGINS # Scale margins by a factor from the original capitals
        return 1 # Scale margins factor, e.g. for small caps.
    scm = property(_get_scm)

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
        
    def __repr__(self):
        if self.c is None:
            c = 'None'
        else:
            c = "'%s'" % self.c
        if self.hex is None:
            hex = 'None'
        else:
            hex = "'%04x'" % self.uni
        s = "%s(uni=%s, c=%s, hex=%s" % (self.__class__.__name__, self.uni, c, hex)
        if self.base is not None:
            s += ", base='%s'" % self.base
        if self.accents:
            s += ", accents=%s" % self.accents
        if self.anchors:
            s += ", anchors=%s" % self.anchors
        if self.composites:
            s += ", composites=%s" % self.composites
        if self.comment:
            s += ', comment="""%s"""' % self.comment
        s += ')'
        return s

    def asCode(self):
        s = "\t'%s': GD(name='%s'" % (self.name, self.name) 
        if self.g1 not in (None, self.name):
            s += ", g1='%s'" % self.g1
        if self.g2 not in (None, self.name):
            s += ", g2='%s'" % self.g2

        if self.l:
            s += ", l='%s'" % self.l
        if self.r:
            s += ", r='%s'" % self.r
        if self.w:
            s += ", w='%s'" % self.w
        if self.il:
            s += ", il='%s'" % self.il
        if self.ir:
            s += ", ir='%s'" % self.ir
        if self.iw:
            s += ", iw='%s'" % self.iw
        if self.ml:
            s += ", ml='%s'" % self.ml
        if self.mr:
            s += ", mr='%s'" % self.mr
        if self.l2r:
            s += ", l2r='%s'" % self.l2r
        if self.r2l:
            s += ", r2l='%s'" % self.r2l
        if self.spacing:
            s += ", spacing='%s'" % self.spacing

        if self.uni is not None:
            s += ", uni=0x%04X" % self.uni
        if self.gid is not None:
            s += ", gid=%d" % self.gid
        if self.italic:
            s += ", italic=True"
        if self.unicodes is not None:
            s += ", unicodes=%s" % self.unicodes
        if self.isLower:
            s += ", isLower=True"
        if self.useSkewRotate:
            s += ", useSkewRotate=True"
        if not self.addItalicExtremePoints:
            s += ", addItalicExtremePoints=False"
        if self.base is not None:
            s += ", base='%s'" % self.base
        if self.src:
            s += ", src=%s" % str(self.src)
        if self.src180:
            s += ", src180=%s" % str(self.src180)
        if self.accents:
            s += ", accents=%s" % str(self.accents)
        if self.anchors:
            s += ", anchors=%s" % self.anchors
        if self.composites:
            s += ", composites=%s" % self.composites

        if not self.fixAccents:
            s += ", fixAccents=False"
        if not self.fixAnchors:
            s += ", fixAnchors=False"

        if self.rightMin:
            s += ", rightMin=%d" % self.rightMin
        if self.topY:
            s += ", topY=%d" % self.topY

        if self.comment not in (None, self.name):
            s += ', comment="""%s"""' % self.comment

        if self.baseline:
            s += ", baseline='%s'" % self.baseline 
        if self.overshoot:
            s += ", overshoot='%s'" % self.overshoot 
        if self.height:
            s += ", height='%s'" % self.height 

        return s + '),'
        
    def __repr__(self):
        s = '<%s /%s' % (self.__class__.__name__, self.name)
        if self.uni is not None:
            s += ' %04x' % self.uni
        if self.italic:
            s += ' Italic'
        if self.l:
            s += ' l=%s' % self.l
        if self.r:
            s += ' r=%s' % self.r
        if self.w:
            s += ' w=%s' % self.w
        if self.l2r:
            s += ' l2r=%s' % self.l2r
        if self.r2l:
            s += ' r2l=%s' % self.r2l
        if self.base:
            s += ' base=%s' % self.base
        if self.accents:
            s += ' accents=%s' % self.accents
        if self.anchors:
            s += ' anchors=%s' % self.anchors
        s += '>'
        return s

    def _get_c(self):
        if self.uni is not None:
            return chr(self.uni)
        return None
    c = property(_get_c)

    def _get_hex(self):
        if self.uni is not None:
            return '%04x' % self.uni
        return None
    hex = property(_get_hex)


GLYPH_DATA = gds = {
    #   Undefined + base = margins of base
    #   Undefined + no base = manual source spacing
    #   l=<int>
    #   l='a'
    #   r=<int>
    #   r='a'
    #   w=<int>
    #   w='a'
    #   il=<int> Optional left side for italic
    #   ir=<int> Optional right side for italic
    #   iw=<int> Optional width for italic
    #   il='a' Optional left side for italic
    #   ir='a' Optional right side for italic
    #   iw='a' Optional width for italic
    #   l2r='a' 
    #   r2l='a' 
    #
    '.notdef': GD(w=500, name='.notdef', anchors=[], copyFromDisplayLeft=False, copyFromDisplayRight=False),
    '.null': GD(w=0, uni=0x0000, unicodes=(0, 13), name='.null', anchors=[], copyFromDisplayLeft=False, copyFromDisplayRight=False),
    'dottedCircle': GD(uni=9676, c='◌', name='dottedCircle', hex='25cc', anchors=[TOP_, BOTTOM_]),

    'A': GD(g2='A', g1='A', l2r='A', uni=0x0041, c='A', name='A', comment='A Uppercase Alphabet, Latin'),
    'AE': GD(g2='AE', g1='E', l='A', r='E', uni=0x00c6, c='Æ', name='AE', comment='Æ ligature ae, latin capital'),
    'AEacute': GD(g2='AE', g1='E', l='A', r='E', uni=0x01fc, c='Ǽ', name='AEacute', base='AE', accents=['acutecmb.uc'], comment='Ǽ LATIN CAPITAL LETTER AE WITH ACUTE'),
    'Aacute': GD(g2='A', g1='A', l='A', w='A', uni=0x00c1, c='Á', name='Aacute', base='A', accents=['acutecmb.uc'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER'),
    'Abreve': GD(g2='A', g1='A', l='A', w='A', uni=0x0102, c='Ă', name='Abreve', base='A', accents=['brevecmb.uc'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE'),
    'Acircumflex': GD(g2='A', g1='A', l='A', w='A', uni=0x00c2, c='Â', name='Acircumflex', base='A', accents=['circumflexcmb.uc'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Adieresis': GD(g2='A', g1='A', l='A', w='A', uni=0x00c4, c='Ä', name='Adieresis', base='A', accents=['dieresiscmb.uc'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Agrave': GD(g2='A', g1='A', l='A', w='A', uni=0x00c0, c='À', name='Agrave', base='A', accents=['gravecmb.uc'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
    'Amacron': GD(g2='A', g1='A', l='A', w='A', uni=0x0100, c='Ā', name='Amacron', base='A', accents=['macroncmb.uc'], comment='Ā Latin, European'),
    'Aogonek': GD(g2='A', g1='A', l='A', w='A', uni=0x0104, c='Ą', name='Aogonek', base='A', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),
    'Aring': GD(g2='A', g1='A', l='A', w='A', uni=0x00c5, c='Å', name='Aring', base='A', accents=['ringcmb.uc'], comment='Å RING ABOVE, LATIN CAPITAL LETTER A WITH'),
    'Aringacute': GD(g2='A', g1='A', l='Aring', w='Aring', uni=506, c='Ǻ', name='Aringacute', hex='01fa', base='A', accents=['ringacutecmb.uc'], comment='Ǻ LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE'),
    'Atilde': GD(g2='A', g1='A', l='A', w='A', uni=0x00c3, c='Ã', name='Atilde', base='A', accents=['tildecmb.uc'], comment='Ã A WITH TILDE, LATIN CAPITAL LETTER'),
    
    'A.sc': GD(g2='A.sc', g1='A.sc', l2r='A.sc', name='A.sc', comment='A.sc Uppercase Alphabet, Latin'),
    'AE.sc': GD(g2='AE.sc', g1='E.sc', l='A.sc', r='E.sc', name='AE.sc', comment='Æ ligature ae, latin capital'),
    'AEacute.sc': GD(g2='AE.sc', g1='E.sc', l='A.sc', r='E.sc', name='AEacute.sc', base='AE.sc', accents=['acutecmb'], comment='Ǽ LATIN CAPITAL LETTER AE WITH ACUTE'),
    'Aacute.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Aacute.sc', base='A.sc', accents=['acutecmb'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER'),
    'Abreve.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Abreve.sc', base='A.sc', accents=['brevecmb'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE'),
    'Acircumflex.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Acircumflex.sc', base='A.sc', accents=['circumflexcmb'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Adieresis.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Adieresis.sc', base='A.sc', accents=['dieresiscmb'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Agrave.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Agrave.sc', base='A.sc', accents=['gravecmb'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
    'Amacron.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Amacron.sc', base='A.sc', accents=['macroncmb'], comment='Ā Latin, European'),
    'Aogonek.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Aogonek.sc', base='A.sc', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),
    'Aring.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Aring.sc', base='A.sc', accents=['ringcmb'], comment='Å RING ABOVE, LATIN CAPITAL LETTER A WITH, using ringcmb'),
    'Aringacute.sc': GD(g2='A.sc', g1='A.sc', l='Aring.sc', w='Aring.sc', name='Aringacute.sc', base='A.sc', accents=['ringacutecmb'], comment='Ǻ LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE'),
    'Atilde.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Atilde.sc', base='A.sc', accents=['tildecmb'], comment='Ã A WITH TILDE, LATIN CAPITAL LETTER'),
    
    'B': GD(g2='H', g1='B', l='H', uni=0x0042, c='B', name='B', comment='B LATIN CAPITAL LETTER B'),
    
    'B.sc': GD(g2='H.sc', g1='B.sc', l='H.sc', name='B.sc', comment='B LATIN CAPITAL LETTER B'),

    'C': GD(g2='O', g1='C', l='O', uni=0x0043, c='C', name='C', comment='C LATIN CAPITAL LETTER C', useSkewRotate=True, addItalicExtremePoints=True),
    'Cacute': GD(g2='O', g1='C', l='C', w='C', uni=0x0106, c='Ć', name='Cacute', base='C', accents=['acutecmb.uc'], comment='Ć LATIN CAPITAL LETTER C WITH ACUTE'),
    'Ccaron': GD(g2='O', g1='C', l='C', w='C', uni=0x010c, c='Č', name='Ccaron', base='C', accents=['caroncmb.uc'], comment='Č LATIN CAPITAL LETTER C WITH CARON'),
    'Ccedilla': GD(g2='O', g1='C', l='C', w='C', uni=0x00c7, c='Ç', name='Ccedilla', base='C', accents=['cedillacmb'], comment='Ç CEDILLA, LATIN CAPITAL LETTER C WITH'),
    'Ccircumflex': GD(g2='O', g1='C', l='C', w='C', uni=0x0108, c='Ĉ', name='Ccircumflex', base='C', accents=['circumflexcmb.uc'], comment='Ĉ LATIN CAPITAL LETTER C WITH CIRCUMFLEX'),
    'Cdotaccent': GD(g2='O', g1='C', l='C', w='C', uni=0x010a, c='Ċ', name='Cdotaccent', base='C', accents=['dotaccentcmb.uc'], comment='Ċ LATIN CAPITAL LETTER C WITH DOT ABOVE'),
    
    'C.sc': GD(g2='O.sc', g1='C.sc', l='O.sc', name='C.sc', comment='C LATIN CAPITAL LETTER C', useSkewRotate=True, addItalicExtremePoints=True),
    'Cacute.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='Cacute.sc', base='C.sc', accents=['acutecmb'], comment='Ć LATIN CAPITAL LETTER C WITH ACUTE'),
    'Ccaron.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='Ccaron.sc', base='C.sc', accents=['caroncmb'], comment='Č LATIN CAPITAL LETTER C WITH CARON'),
    'Ccedilla.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='Ccedilla.sc', base='C.sc', accents=['cedillacmb'], comment='Ç CEDILLA, LATIN CAPITAL LETTER C WITH'),
    'Ccircumflex.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='Ccircumflex.sc', base='C.sc', accents=['circumflexcmb'], comment='Ĉ LATIN CAPITAL LETTER C WITH CIRCUMFLEX'),
    'Cdotaccent.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='Cdotaccent.sc', base='C.sc', accents=['dotaccentcmb'], comment='Ċ LATIN CAPITAL LETTER C WITH DOT ABOVE'),
    
    'D': GD(g2='H', g1='O', l='H', r='O', uni=0x0044, c='D', name='D', comment='D', useSkewRotate=True, addItalicExtremePoints=True),
    'Dcaron': GD(g2='H', g1='O', l='D', w='D', uni=0x010e, c='Ď', name='Dcaron', base='D', accents=['caroncmb.uc'], comment='Ď'),
    'Dcroat': GD(g2='H', g1='O', l='Eth', r='Eth', uni=0x0110, c='Đ', name='Dcroat', base='Eth', comment='Đ'),
    
    'D.sc': GD(g2='H.sc', g1='O.sc', l='H.sc', r='O.sc', name='D.sc', comment='D.sc', useSkewRotate=True, addItalicExtremePoints=True),
    'Dcaron.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='Dcaron.sc', base='D.sc', accents=['caroncmb'], comment='Ď.sc'),
    'Dcroat.sc': GD(g2='H.sc', g1='O.sc', l='Eth.sc', r='Eth.sc', name='Dcroat.sc', base='Eth.sc', comment='Đ.sc'),
    
    'Delta': GD(g2='Delta', g1='Delta', l2r='Delta', uni=0x0394, c='Δ', name='Delta', comment='∆ symmetric difference', anchors=[]),
   
    'E': GD(g2='H', g1='E', l='H', uni=0x0045, c='E', name='E', comment='E'),
    'Eacute': GD(g2='H', g1='E', l='E', w='E', uni=0x00c9, c='É', name='Eacute', base='E', accents=['acutecmb.uc'], comment='É E WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ebreve': GD(g2='H', g1='E', l='E', w='E', uni=0x0114, c='Ĕ', name='Ebreve', base='E', accents=['brevecmb.uc'], comment='Ĕ'),
    'Ecaron': GD(g2='H', g1='E', l='E', w='E', uni=0x011a, c='Ě', name='Ecaron', base='E', accents=['caroncmb.uc'], comment='Ě'),
    'Ecircumflex': GD(g2='H', g1='E', l='E', w='E', uni=0x00ca, c='Ê', name='Ecircumflex', base='E', accents=['circumflexcmb.uc'], comment='Ê E WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Edieresis': GD(g2='H', g1='E', l='E', w='E', uni=0x00cb, c='Ë', name='Edieresis', base='E', accents=['dieresiscmb.uc'], comment='Ë E WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Edotaccent': GD(g2='H', g1='E', l='E', w='E', uni=0x0116, c='Ė', name='Edotaccent', base='E', accents=['dotaccentcmb.uc']),
    'Egrave': GD(g2='H', g1='E', l='E', w='E', uni=0x00c8, c='È', name='Egrave', base='E', accents=['gravecmb.uc'], comment='È E WITH GRAVE, LATIN CAPITAL LETTER'),
    'Emacron': GD(g2='H', g1='E', l='E', w='E', uni=0x0112, c='Ē', name='Emacron', base='E', accents=['macroncmb.uc'], comment='Ē'),
    'Eng': GD(g2='H', g1='N', l='N', w='N', uni=0x014a, c='Ŋ', name='Eng', copyFromDisplayRight=False, comment='Ŋ'),
    'Eogonek': GD(g2='H', g1='E', l='E', w='E', uni=0x0118, c='Ę', name='Eogonek', base='E', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Ę'),
    'Eth': GD(g2='Eth', g1='O', l='D', r='D', uni=0x00d0, c='Ð', name='Eth', base='D', comment='Ð ETH, LATIN CAPITAL LETTER'),
    
    'E.sc': GD(g2='H.sc', g1='E.sc', l='H.sc', name='E.sc', comment='E.sc'),
    'Eacute.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Eacute.sc', base='E.sc', accents=['acutecmb'], comment='É E.sc WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ebreve.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Ebreve.sc', base='E.sc', accents=['brevecmb'], comment='Ĕ'),
    'Ecaron.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Ecaron.sc', base='E.sc', accents=['caroncmb'], comment='Ě'),
    'Ecircumflex.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Ecircumflex.sc', base='E.sc', accents=['circumflexcmb'], comment='Ê E WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Edieresis.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Edieresis.sc', base='E.sc', accents=['dieresiscmb'], comment='Ë E WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Edotaccent.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Edotaccent.sc', base='E.sc', accents=['dotaccentcmb']),
    'Egrave.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Egrave.sc', base='E.sc', accents=['gravecmb'], comment='È E WITH GRAVE, LATIN CAPITAL LETTER'),
    'Emacron.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Emacron.sc', base='E.sc', accents=['macroncmb'], comment='Ē'),
    'Eng.sc': GD(g2='H.sc', g1='N.sc', l='N.sc', w='N.sc', name='Eng.sc', copyFromDisplayRight=False, comment='Ŋ'),
    'Eogonek.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Eogonek.sc', base='E.sc', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Ę'),
    'Eth.sc': GD(g2='Eth.sc', g1='O.sc', l='D.sc', r='D.sc', name='Eth.sc', base='D.sc', comment='Ð ETH, LATIN CAPITAL LETTER'),
    
    'F': GD(g2='H', g1='F', l='H', uni=0x0046, c='F', name='F', comment='F'),
    
    'F.sc': GD(g2='H.sc', g1='F.sc', l='H.sc', name='F.sc', comment='F.sc'),
       
    'G': GD(g2='O', g1='G', l='O', uni=0x0047, c='G', name='G', comment='G', useSkewRotate=True, addItalicExtremePoints=True),
    'Gbreve': GD(g2='O', g1='G', l='G', w='G', uni=0x011e, c='Ğ', name='Gbreve', base='G', accents=['brevecmb.uc'], comment='Ğ'),
    'Gcaron': GD(g2='O', g1='G', l='G', w='G', uni=0x01e6, c='Ǧ', name='Gcaron', base='G', accents=['caroncmb.uc']),
    'Gcircumflex': GD(g2='O', g1='G', l='G', w='G', uni=0x011c, c='Ĝ', name='Gcircumflex', base='G', accents=['circumflexcmb.uc'], comment='Ĝ'),
    'Gcommaaccent': GD(g2='O', g1='G', l='G', w='G', uni=0x0122, c='Ģ', name='Gcommaaccent', base='G', accents=['commabelowcmb'], comment='Ģ'),
    'Gdotaccent': GD(g2='O', g1='G', l='G', w='G', uni=0x0120, c='Ġ', name='Gdotaccent', base='G', accents=['dotaccentcmb.uc'], comment='Ġ'),

    'G.sc': GD(g2='O.sc', g1='G.sc', l='O.sc', name='G.sc', comment='G.sc', useSkewRotate=True, addItalicExtremePoints=True),
    'Gbreve.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='Gbreve.sc', base='G.sc', accents=['brevecmb'], comment='Ğ'),
    'Gcaron.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='Gcaron.sc', base='G.sc', accents=['caroncmb']),
    'Gcircumflex.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='Gcircumflex.sc', base='G.sc', accents=['circumflexcmb'], comment='Ĝ'),
    'Gcommaaccent.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='Gcommaaccent.sc', base='G.sc', accents=['commabelowcmb'], comment='Ģ'),
    'Gdotaccent.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='Gdotaccent.sc', base='G.sc', accents=['dotaccentcmb'], comment='Ġ'),
     
    'H': GD(g2='H', g1='H', l2r='H', uni=0x0048, c='H', name='H', comment='H'),
    'Hbar': GD(g2='H', g1='H', l='H', r='H', uni=0x0126, c='Ħ', name='Hbar', base='H', comment='Ħ'),
    'Hcircumflex': GD(g2='H', g1='H', uni=0x0124, c='Ĥ', name='Hcircumflex', base='H', accents=['circumflexcmb.uc'], comment='Ĥ'),
 
    'H.sc': GD(g2='H.sc', g1='H.sc', l2r='H.sc', name='H.sc', comment='H.sc'),
    'Hbar.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', r='H.sc', name='Hbar.sc', base='H.sc', comment='Ħ.sc'),
    'Hcircumflex.sc': GD(g2='H.sc', g1='H.sc', name='Hcircumflex.sc', base='H.sc', accents=['circumflexcmb'], comment='Ĥ.sc'),
 
    'I': GD(g2='H', g1='H', l='H', r='H', uni=0x0049, c='I', name='I', comment='I', anchors=ALL_IJ_ANCHORS),
    'Iacute': GD(g2='H', g1='H', l='I', w='I', uni=0x00cd, c='Í', name='Iacute', base='I', accents=['acutecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ibreve': GD(g2='H', g1='H', l='I', w='I', uni=0x012c, c='Ĭ', name='Ibreve', base='I', accents=['brevecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ĭ'),
    'Icircumflex': GD(g2='H', g1='H', l='I', w='I', uni=0x00ce, c='Î', name='Icircumflex', base='I', accents=['circumflexcmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Idieresis': GD(g2='H', g1='H', l='I', w='I', uni=0x00cf, c='Ï', name='Idieresis', base='I', accents=['dieresiscmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Idotaccent': GD(g2='H', g1='H', l='I', w='I', uni=0x0130, c='İ', name='Idotaccent', base='I', accents=['dotaccentcmb.uc'], anchors=ALL_IJ_ANCHORS, comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
    'Igrave': GD(g2='H', g1='H', l='I', w='I', uni=0x00cc, c='Ì', name='Igrave', base='I', accents=['gravecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
    'Imacron': GD(g2='H', g1='H', l='I', w='I', uni=0x012a, c='Ī', name='Imacron', base='I', accents=['macroncmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ī'),
    'Iogonek': GD(g2='H', g1='H', l='I', w='I', uni=0x012e, c='Į', name='Iogonek', base='I', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Į'),
    'Itilde': GD(g2='H', g1='H', l='I', w='I', uni=0x0128, c='Ĩ', name='Itilde', base='I', accents=['tildecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ĩ'),

    'I.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', r='H.sc', name='I.sc', comment='I.sc'),
    'Iacute.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Iacute.sc', base='I.sc', accents=['acutecmb'], anchors=ALL_IJ_ANCHORS, comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ibreve.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Ibreve.sc', base='I.sc', accents=['brevecmb'], anchors=ALL_IJ_ANCHORS, comment='Ĭ'),
    'Icircumflex.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Icircumflex.sc', base='I.sc', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS, comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Idieresis.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Idieresis.sc', base='I.sc', accents=['dieresiscmb'], anchors=ALL_IJ_ANCHORS, comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Idotaccent.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Idotaccent.sc', base='I.sc', accents=['dotaccentcmb'], anchors=ALL_IJ_ANCHORS, comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
    'Igrave.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Igrave.sc', base='I.sc', accents=['gravecmb'], anchors=ALL_IJ_ANCHORS, comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
    'Imacron.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Imacron.sc', base='I.sc', accents=['macroncmb'], anchors=ALL_IJ_ANCHORS, comment='Ī'),
    'Iogonek.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Iogonek.sc', base='I.sc', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Į'),
    'Itilde.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Itilde.sc', base='I.sc', accents=['tildecmb'], anchors=ALL_IJ_ANCHORS, comment='Ĩ'),

    'J': GD(g2='J', g1='J', w='I', uni=74, c='J', name='J', hex='004a', comment='J', anchors=ALL_IJ_ANCHORS), # Manually take margins from /I
    'Jcircumflex': GD(g2='J', g1='J', l='J', w='J', uni=308, c='Ĵ', name='Jcircumflex', hex='0134', base='J', accents=['circumflexcmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ĵ'),
    'IJ': GD(g2='H', g1='J', ml='I', mr='J', uni=0x0132, c='Ĳ', name='IJ', hex='0132', base='I', accents=['J'], anchors=ALL_IJ_ANCHORS, comment='IJ Dutch ligature'),
    'J.base': GD(g2='J.base', g1='U', r='J', name='J.base', anchors=ALL_IJ_ANCHORS),
    'Jcircumflex.base': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='Jcircumflex.base', base='J.base', accents=['circumflexcmb.uc'], anchors=ALL_IJ_ANCHORS),
    
    'J.sc': GD(g2='J.sc', g1='J.sc', w='I.sc', name='J.sc', comment='J', anchors=ALL_IJ_ANCHORS, ), # Manually take margins from /I
    'Jcircumflex.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='Jcircumflex.sc', base='J.sc', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS, comment='Ĵ'),
    'IJ.sc': GD(g2='H.sc', g1='J.sc', ml='I.sc', mr='J.sc', name='IJ.sc', base='I.sc', accents=['J.sc'], anchors=ALL_IJ_ANCHORS, comment='IJ Dutch ligature'),
    'J.base.sc': GD(g2='J.base.sc', g1='U.sc', r='J.sc', name='J.base.sc', anchors=ALL_IJ_ANCHORS),
    'Jcircumflex.base.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='Jcircumflex.base.sc', base='J.base.sc', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS),
    
    'K': GD(g2='H', g1='K', l='H', r='A', uni=0x004b, c='K', name='K', comment='K'),
    'Kcommaaccent': GD(g2='H', g1='K', l='K', r='K', uni=0x0136, c='Ķ', name='Kcommaaccent', base='K', accents=['commabelowcmb'], comment='Ķ'),
    
    'K.sc': GD(g2='H.sc', g1='K.sc', l='H.sc', r='A.sc', name='K.sc', comment='K'),
    'Kcommaaccent.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', r='K.sc', name='Kcommaaccent.sc', base='K.sc', accents=['commabelowcmb'], comment='Ķ'),
    
    'L': GD(g2='H', g1='L', l='H', r='E', uni=0x004c, c='L', name='L', smallTrackRight=False, comment='L'),
    'Lacute': GD(g2='H', g1='L', l='L', w='L', uni=0x0139, c='Ĺ', name='Lacute', base='L', accents=['acutecmb.uc'], smallTrackRight=0, comment='Ĺ'),
    'Lcaron': GD(g2='H', g1='Lcaron', l='L', w='L', uni=0x013d, c='Ľ', name='Lcaron', base='L', accents=['caroncmb.vert'], smallTrackRight=0, comment='Ľ'),
    'Lcommaaccent': GD(g2='H', g1='Lcommaaccent', l='L', w='L', uni=0x013b, c='Ļ', name='Lcommaaccent', base='L', accents=['commabelowcmb'], comment='Ļ'),
    'Ldot': GD(g2='H', g1='Ldot',l='L', uni=0x013f, c='Ŀ', name='Ldot', base='L', accents=['dotmiddlecmb'], smallTrackRight=0, comment='Ŀ'),
    'Lslash': GD(g2='Eth', g1='L', l='L', w='L', uni=0x0141, c='Ł', base='L', name='Lslash', copyFromDisplayLeft=False, copyFromDisplayRight=False, smallTrackRight=0, comment='Ł'),
    
    'L.sc': GD(g2='H.sc', g1='L.sc', l='H.sc', r='E.sc', name='L.sc', smallTrackRight=0, comment='L'),
    'Lacute.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='Lacute.sc', base='L.sc', accents=['acutecmb'], smallTrackRight=0, comment='Ĺ'),
    'Lcaron.sc': GD(g2='H.sc', g1='Lcaron.sc', l='L.sc', w='L.sc', name='Lcaron.sc', base='L.sc', accents=['caroncmb.vert'], smallTrackRight=0, comment='Ľ'),
    'Lcommaaccent.sc': GD(g2='H.sc', g1='Lcommaaccent.sc', l='L.sc', w='L.sc', name='Lcommaaccent.sc', base='L.sc', accents=['commabelowcmb'], smallTrackRight=0, comment='Ļ'),
    'Ldot.sc': GD(g2='H.sc', g1='Ldot.sc',l='L.sc', name='Ldot.sc', base='L.sc', accents=['dotmiddlecmb'], smallTrackRight=0, comment='Ŀ'),
    'Lslash.sc': GD(g2='Eth.sc', g1='L.sc', l='L.sc', w='L.sc', base='L.sc', name='Lslash.sc', copyFromDisplayLeft=False, copyFromDisplayRight=False, smallTrackRight=0, comment='Ł'),
    
    'M': GD(g2='N', g1='H', l='H', r='H', uni=0x004d, c='M', name='M', comment='M'),
    
    'M.sc': GD(g2='N.sc', g1='H.sc', l='H.sc', r='H.sc', name='M.sc', comment='M.sc'),
    
    'N': GD(g2='N', g1='N', l='H', r='J', uni=0x004e, c='N', name='N', comment='N'),
    'Nacute': GD(g2='N', g1='N', l='H', r='J', uni=0x0143, c='Ń', name='Nacute', base='N', accents=['acutecmb.uc'], comment='Ń'),
    'Ncaron': GD(g2='N', g1='N', l='H', r='J', uni=0x0147, c='Ň', name='Ncaron', base='N', accents=['caroncmb.uc'], comment='Ň'),
    'Ncommaaccent': GD(g2='N', g1='N', l='H', r='J', uni=0x0145, c='Ņ', name='Ncommaaccent', base='N', accents=['commabelowcmb'], comment='Ņ'),
    'Ntilde': GD(g2='N', g1='N', l='H', r='J', uni=0x00d1, c='Ñ', name='Ntilde', base='N', accents=['tildecmb.uc'], comment='Ñ N WITH TILDE, LATIN CAPITAL LETTER'),
    
    'N.sc': GD(g2='N.sc', g1='N.sc', l='H.sc', r='J.sc', name='N.sc', comment='N.sc'),
    'Nacute.sc': GD(g2='N.sc', g1='N.sc', l='H.sc', r='J.sc', name='Nacute.sc', base='N.sc', accents=['acutecmb'], comment='Ń'),
    'Ncaron.sc': GD(g2='N.sc', g1='N.sc', l='H.sc', r='J.sc', name='Ncaron.sc', base='N.sc', accents=['caroncmb'], comment='Ň'),
    'Ncommaaccent.sc': GD(g2='N.sc', g1='N.sc', l='H.sc', r='J.sc', name='Ncommaaccent.sc', base='N.sc', accents=['commabelowcmb'], comment='Ņ'),
    'Ntilde.sc': GD(g2='N.sc', g1='N.sc', l='H.sc', r='J.sc', name='Ntilde.sc', base='N.sc', accents=['tildecmb'], comment='Ñ N WITH TILDE, LATIN CAPITAL LETTER'),
    
    'O': GD(g2='O', g1='O', l2r='O', uni=0x004f, c='O', name='O', comment='O', useSkewRotate=True, addItalicExtremePoints=True, anchors=ALL_IJ_ANCHORS),
    'OE': GD(g2='O', g1='E', l='O', r='E', uni=338, c='Œ', name='OE', hex='0152', comment='Œ'),
    'Oslash': GD(g2='O', g1='O', l='O', w='O', uni=0x00d8, c='Ø', base='O', name='Oslash', anchors=ALL_IJ_ANCHORS, comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Oslashacute': GD(g2='O', g1='O', l='O', w='O', uni=0x01fe, c='Ǿ', base='Oslash', accents=['acutecmb.uc'], name='Oslashacute', anchors=ALL_IJ_ANCHORS, comment='Ǿ LATIN CAPITAL LETTER O WITH STROKE AND ACUTE'),
    'Oacute': GD(g2='O', g1='O', l='O', w='O', uni=0x00d3, c='Ó', name='Oacute', base='O', accents=['acutecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
    'Obreve': GD(g2='O', g1='O', l='O', w='O', uni=0x014e, c='Ŏ', name='Obreve', base='O', accents=['brevecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ŏ'),
    'Ocircumflex': GD(g2='O', g1='O', l='O', w='O', uni=0x00d4, c='Ô', name='Ocircumflex', base='O', accents=['circumflexcmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Odieresis': GD(g2='O', g1='O', l='O', w='O', uni=0x00d6, c='Ö', name='Odieresis', base='O', accents=['dieresiscmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ograve': GD(g2='O', g1='O', l='O', w='O', uni=0x00d2, c='Ò', name='Ograve', base='O', accents=['gravecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
    'Ohungarumlaut': GD(g2='O', g1='O', l='O', w='O', uni=0x0150, c='Ő', name='Ohungarumlaut', base='O', accents=['hungarumlautcmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ő'),
    'Omacron': GD(g2='O', g1='O', l='O', w='O', uni=0x014c, c='Ō', name='Omacron', base='O', accents=['macroncmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Ō'),
    'Otilde': GD(g2='O', g1='O', l='O', w='O', uni=0x00d5, c='Õ', name='Otilde', base='O', accents=['tildecmb.uc'], anchors=ALL_IJ_ANCHORS, comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),

    'Omega': GD(g2='Omega', g1='Omega', l='T', l2r='Omega', uni=0x03a9, c='Ω', name='Omega', src=('O', 'summation'), comment='Ω (GREEK CAPITAL LETTER OMEGA)'),
    
    'O.sc': GD(g2='O.sc', g1='O.sc', l2r='O.sc', name='O.sc', comment='O', useSkewRotate=True, addItalicExtremePoints=True, anchors=ALL_IJ_ANCHORS),
    'OE.sc': GD(g2='O.sc', g1='E.sc', l='O.sc', r='E.sc', name='OE.sc', comment='Œ'),
    'Oslash.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', base='O.sc', name='Oslash.sc', anchors=ALL_IJ_ANCHORS, comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
    'Oslashacute.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', base='Oslash.sc', accents=['acutecmb'], name='Oslashacute', anchors=ALL_IJ_ANCHORS, comment='Ǿ LATIN CAPITAL LETTER O WITH STROKE AND ACUTE'),
    'Oacute.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Oacute.sc', base='O.sc', accents=['acutecmb'], anchors=ALL_IJ_ANCHORS, comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
    'Obreve.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Obreve.sc', base='O.sc', accents=['brevecmb'], anchors=ALL_IJ_ANCHORS, comment='Ŏ'),
    'Ocircumflex.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Ocircumflex.sc', base='O.sc', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS, comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Odieresis.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Odieresis.sc', base='O.sc', accents=['dieresiscmb'], anchors=ALL_IJ_ANCHORS, comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ograve.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Ograve.sc', base='O.sc', accents=['gravecmb'], anchors=ALL_IJ_ANCHORS, comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
    'Ohungarumlaut.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Ohungarumlaut.sc', base='O.sc', accents=['hungarumlautcmb'], anchors=ALL_IJ_ANCHORS, comment='Ő'),
    'Omacron.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Omacron.sc', base='O.sc', accents=['macroncmb'], anchors=ALL_IJ_ANCHORS, comment='Ō'),
    'Otilde.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Otilde.sc', base='O.sc', accents=['tildecmb'], anchors=ALL_IJ_ANCHORS, comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),
    
    'P': GD(g2='H', g1='P', l='H', uni=0x0050, c='P', name='P', comment='P', useSkewRotate=True, addItalicExtremePoints=True),
    
    'P.sc': GD(g2='H.sc', g1='P.sc', l='H.sc', name='P.sc', comment='P.sc', useSkewRotate=True, addItalicExtremePoints=True),
    
    'Q': GD(g2='O', g1='O', l='O', w='O', uni=0x0051, c='Q', name='Q', base='O', comment='Q'), 
    
    'Q.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Q.sc', base='O.sc', comment='Q.sc'), 

    'R': GD(g2='H', g1='R', l='H', uni=0x0052, c='R', name='R', comment='R', useSkewRotate=True, addItalicExtremePoints=True),
    'R.cbr': GD(g2='H', g1='R.cbr', l='R', w='R', name='R.cbr', template='R', src='R', copyFromDisplayRight=False, comment='R - connector bottom right'),
    'Racute': GD(g2='H', g1='R', l='R', w='R', uni=0x0154, c='Ŕ', name='Racute', base='R', accents=['acutecmb.uc'], comment='Ŕ'),
    'Rcaron': GD(g2='H', g1='R', l='R', w='R', uni=0x0158, c='Ř', name='Rcaron', base='R', accents=['caroncmb.uc'], comment='Ř'),
    'Rcommaaccent': GD(g2='H', g1='R', l='R', w='R', uni=0x0156, c='Ŗ', name='Rcommaaccent', base='R', accents=['commabelowcmb'], comment='Ŗ'),
    
    'R.sc': GD(g2='H.sc', g1='R.sc', l='H.sc', name='R.sc', comment='R.sc', copyFromDisplayRight=False, useSkewRotate=True, addItalicExtremePoints=True),
    'R.cbr.sc': GD(g2='H.sc', g1='R.cbr.sc', l='R.sc', w='R.sc', name='R.cbr.sc', copyFromDisplayRight=False, template='R.sc', src='R.sc', comment='R - connector bottom right.sc'),
    'Racute.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='Racute.sc', base='R.sc', accents=['acutecmb'], copyFromDisplayRight=False, comment='Ŕ'),
    'Rcaron.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='Rcaron.sc', base='R.sc', accents=['caroncmb'], copyFromDisplayRight=False, comment='Ř'),
    'Rcommaaccent.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='Rcommaaccent.sc', base='R.sc', accents=['commabelowcmb'], copyFromDisplayRight=False, comment='Ŗ'),
    
    'S': GD(g2='S', g1='S', l2r='S', uni=0x0053, c='S', name='S', comment='S', useSkewRotate=True, addItalicExtremePoints=True),
    'Sacute': GD(g2='S', g1='S', l='S', w='S', uni=0x015a, c='Ś', name='Sacute', base='S', accents=['acutecmb.uc'], comment='Ś'),
    'Scaron': GD(g2='S', g1='S', l='S', w='S', uni=0x0160, c='Š', name='Scaron', base='S', accents=['caroncmb.uc'], comment='Š'),
    'Scedilla': GD(g2='S', g1='S', l='S', w='S', uni=0x015e, c='Ş', name='Scedilla', base='S', accents=['cedillacmb'], comment='Ş'),
    'Scircumflex': GD(g2='S', g1='S', l='S', w='S', uni=0x015c, c='Ŝ', name='Scircumflex', base='S', accents=['circumflexcmb.uc'], comment='Ŝ'),
    'Scommaaccent': GD(g2='S', g1='S', l='S', w='S', uni=0x0218, c='Ș', name='Scommaaccent', base='S', accents=['commabelowcmb'], comment='Ș'),
    
    'S.sc': GD(g2='S.sc', g1='S.sc', l2r='S.sc', name='S.sc', comment='S.sc', useSkewRotate=True, addItalicExtremePoints=True),
    'Sacute.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', w='S.sc', name='Sacute.sc', base='S.sc', accents=['acutecmb'], comment='Ś'),
    'Scaron.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', w='S.sc', name='Scaron.sc', base='S.sc', accents=['caroncmb'], comment='Š'),
    'Scedilla.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', w='S.sc', name='Scedilla.sc', base='S.sc', accents=['cedillacmb'], comment='Ş'),
    'Scircumflex.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', w='S.sc', name='Scircumflex.sc', base='S.sc', accents=['circumflexcmb'], comment='Ŝ'),
    'Scommaaccent.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', w='S.sc', name='Scommaaccent.sc', base='S.sc', accents=['commabelowcmb'], comment='Ș'),
    
    'Thorn': GD(g2='H', g1='Thorn', l='H', r='P', uni=0x00de, c='Þ', name='Thorn', src='P', comment='Þ THORN, LATIN CAPITAL LETTER'),
    'T': GD(g2='T', g1='T', l2r='T', uni=0x0054, c='T', name='T', comment='T'),
    'Tbar': GD(g2='T', g1='T', l='T', w='T', uni=0x0166, c='Ŧ', name='Tbar', base='T', comment='Ŧ'),
    'Tcaron': GD(g2='T', g1='T', l='T', w='T', uni=0x0164, c='Ť', name='Tcaron', base='T', accents=['caroncmb.uc'], comment='Ť'),
    'Tcedilla': GD(g2='T', g1='T', l='T', w='T', uni=0x0162, c='Ţ', name='Tcedilla', base='T', accents=['cedillacmb'], comment='Ţ'),
    'Tcommaaccent': GD(g2='T', g1='T', l='T', w='T', uni=538, c='Ț', name='Tcommaaccent', hex='021a', base='T', accents=['commabelowcmb'], comment='Ț'),
    
    'Thorn.sc': GD(g2='H.sc', g1='Thorn.sc', l='H.sc', r='P.sc', name='Thorn.sc', src='P.sc', comment='Þ THORN, LATIN CAPITAL LETTER'),
    'T.sc': GD(g2='T.sc', g1='T.sc', l2r='T.sc', name='T.sc', comment='T.sc'),
    'Tbar.sc': GD(g2='T.sc', g1='T.sc', l='T.sc', w='T.sc', name='Tbar.sc', base='T.sc', comment='Ŧ'),
    'Tcaron.sc': GD(g2='T.sc', g1='T.sc', l='T.sc', w='T.sc', name='Tcaron.sc', base='T.sc', accents=['caroncmb'], comment='Ť'),
    'Tcedilla.sc': GD(g2='T.sc', g1='T.sc', l='T.sc', w='T.sc', name='Tcedilla.sc', base='T.sc', accents=['cedillacmb'], comment='Ţ'),
    'Tcommaaccent.sc': GD(g2='T.sc', g1='T.sc', l='T.sc', w='T.sc', name='Tcommaaccent.sc', base='T.sc', accents=['commabelowcmb'], comment='Ț'),
    
    'U': GD(g2='U', g1='U', l2r='U', uni=0x0055, c='U', name='U', comment='U'),
    'Uacute': GD(g2='U', g1='U', l='U', w='U', uni=0x00da, c='Ú', name='Uacute', base='U', accents=['acutecmb.uc'], comment='Ú U WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ubreve': GD(g2='U', g1='U', l='U', w='U', uni=0x016c, c='Ŭ', name='Ubreve', base='U', accents=['brevecmb.uc'], comment='Ŭ'),
    'Ucircumflex': GD(g2='U', g1='U', l='U', w='U', uni=0x00db, c='Û', name='Ucircumflex', base='U', accents=['circumflexcmb.uc'], comment='Û U WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Udieresis': GD(g2='U', g1='U', l='U', w='U', uni=0x00dc, c='Ü', name='Udieresis', base='U', accents=['dieresiscmb.uc'], comment='Ü U WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ugrave': GD(g2='U', g1='U', l='U', w='U', uni=0x00d9, c='Ù', name='Ugrave', base='U', accents=['gravecmb.uc'], comment='Ù U WITH GRAVE, LATIN CAPITAL LETTER'),
    'Uhungarumlaut': GD(g2='U', g1='U', l='U', w='U', uni=0x0170, c='Ű', name='Uhungarumlaut', base='U', accents=['hungarumlautcmb.uc'], comment='Ű'),
    'Umacron': GD(g2='U', g1='U', l='U', w='U', uni=0x016a, c='Ū', name='Umacron', base='U', accents=['macroncmb.uc'], comment='Ū'),
    'Uogonek': GD(g2='U', g1='U', l='U', w='U', uni=0x0172, c='Ų', name='Uogonek', base='U', accents=['eogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Ų'),
    'Uring': GD(g2='U', g1='U', l='U', w='U', uni=0x016e, c='Ů', name='Uring', base='U', accents=['ringcmb.uc'], comment='Ů'),
    'Utilde': GD(g2='U', g1='U', l='U', w='U', uni=0x0168, c='Ũ', name='Utilde', base='U', accents=['tildecmb.uc'], comment='Ũ'),
    
    'U.sc': GD(g2='U.sc', g1='U.sc', l2r='U.sc', name='U.sc', comment='U.sc'),
    'Uacute.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Uacute.sc', base='U.sc', accents=['acutecmb'], comment='Ú U WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ubreve.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Ubreve.sc', base='U.sc', accents=['brevecmb'], comment='Ŭ'),
    'Ucircumflex.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Ucircumflex.sc', base='U.sc', accents=['circumflexcmb'], comment='Û U WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
    'Udieresis.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Udieresis.sc', base='U.sc', accents=['dieresiscmb'], comment='Ü U WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ugrave.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Ugrave.sc', base='U.sc', accents=['gravecmb'], comment='Ù U WITH GRAVE, LATIN CAPITAL LETTER'),
    'Uhungarumlaut.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Uhungarumlaut.sc', base='U.sc', accents=['hungarumlautcmb'], comment='Ű'),
    'Umacron.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Umacron.sc', base='U.sc', accents=['macroncmb'], comment='Ū'),
    'Uogonek.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Uogonek.sc', base='U.sc', accents=['eogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='Ų'),
    'Uring.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Uring.sc', base='U.sc', accents=['ringcmb'], comment='Ů'),
    'Utilde.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Utilde.sc', base='U.sc', accents=['tildecmb'], comment='Ũ'),
    
    'V': GD(g2='V', g1='V', l='A', r='A', uni=0x0056, c='V', name='V', comment='V'),
    
    'V.sc': GD(g2='V.sc', g1='V.sc', l='A.sc', r='A.sc', name='V.sc', comment='V.sc'),

    'W': GD(g2='V', g1='V', l='A', r='A', uni=0x0057, c='W', name='W', comment='W'),
    'Wacute': GD(g2='V', g1='V', l='W', w='W', uni=0x1e82, c='Ẃ', name='Wacute', base='W', accents=['acutecmb.uc'], comment='Ẃ'),
    'Wcircumflex': GD(g2='V', g1='V', l='W', w='W', uni=0x0174, c='Ŵ', name='Wcircumflex', base='W', accents=['circumflexcmb.uc'], comment='Ŵ'),
    'Wdieresis': GD(g2='V', g1='V', l='W', w='W', uni=0x1e84, c='Ẅ', name='Wdieresis', base='W', accents=['dieresiscmb.uc'], comment='Ẅ'),
    'Wgrave': GD(g2='V', g1='V', l='W', w='W', uni=7808, c='Ẁ', name='Wgrave', hex='1e80', base='W', accents=['gravecmb.uc'], comment='Ẁ'),
    
    'W.sc': GD(g2='V.sc', g1='V.sc', l='A.sc', r='A.sc', name='W.sc', comment='W.sc'),
    'Wacute.sc': GD(g2='V.sc', g1='V.sc', l='W.sc', w='W.sc', name='Wacute.sc', base='W.sc', accents=['acutecmb'], comment='Ẃ'),
    'Wcircumflex.sc': GD(g2='V.sc', g1='V.sc', l='W.sc', w='W.sc', name='Wcircumflex.sc', base='W.sc', accents=['circumflexcmb'], comment='Ŵ'),
    'Wdieresis.sc': GD(g2='V.sc', g1='V.sc', l='W.sc', w='W.sc', name='Wdieresis.sc', base='W.sc', accents=['dieresiscmb'], comment='Ẅ'),
    'Wgrave.sc': GD(g2='V.sc', g1='V.sc', l='W.sc', w='W.sc', name='Wgrave.sc', base='W.sc', accents=['gravecmb'], comment='Ẁ'),
    
    'X': GD(g2='X', g1='X', l2r='X', uni=0x0058, c='X', name='X', comment='X'),

    'X.sc': GD(g2='X.sc', g1='X.sc', l2r='X.sc', name='X.sc', comment='X.sc'),
    
    'Y': GD(g2='Y', g1='Y', l='A', r='A', uni=0x0059, c='Y', name='Y', comment='Y'),
    'Yacute': GD(g2='Y', g1='Y', l='Y', w='Y', uni=0x00dd, c='Ý', name='Yacute', base='Y', accents=['acutecmb.uc'], comment='Ý Y WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ycircumflex': GD(g2='Y', g1='Y', l='Y', w='Y', uni=0x0176, c='Ŷ', name='Ycircumflex', base='Y', accents=['circumflexcmb.uc'], comment='Ŷ'),
    'Ydieresis': GD(g2='Y', g1='Y', l='Y', w='Y', uni=0x0178, c='Ÿ', name='Ydieresis', base='Y', accents=['dieresiscmb.uc'], comment='Ÿ Y WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ygrave': GD(g2='Y', g1='Y', l='Y', w='Y', uni=0x1ef2, c='Ỳ', name='Ygrave', base='Y', accents=['gravecmb.uc'], comment='Ỳ'),
    
    'Y.sc': GD(g2='Y.sc', g1='Y.sc', l='A.sc', r='A.sc', name='Y.sc', comment='Y.sc'),
    'Yacute.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Yacute.sc', base='Y.sc', accents=['acutecmb'], comment='Ý Y WITH ACUTE, LATIN CAPITAL LETTER'),
    'Ycircumflex.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Ycircumflex.sc', base='Y.sc', accents=['circumflexcmb'], comment='Ŷ'),
    'Ydieresis.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Ydieresis.sc', base='Y.sc', accents=['dieresiscmb'], comment='Ÿ Y WITH DIAERESIS, LATIN CAPITAL LETTER'),
    'Ygrave.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Ygrave.sc', base='Y.sc', accents=['gravecmb'], comment='Ỳ'),
    
    'Z': GD(g2='Z', g1='Z', l2r='Z', r='Z', uni=0x005a, c='Z', name='Z', comment='Z'),
    'Zacute': GD(g2='Z', g1='Z', l='Z', w='Z', uni=0x0179, c='Ź', name='Zacute', base='Z', accents=['acutecmb.uc'], comment='Ź'),
    'Zcaron': GD(g2='Z', g1='Z', l='Z', w='Z', uni=0x017d, c='Ž', name='Zcaron', base='Z', accents=['caroncmb.uc'], comment='Ž'),
    'Zdotaccent': GD(g2='Z', g1='Z', l='Z', w='Z', uni=0x017b, c='Ż', name='Zdotaccent', base='Z', accents=['dotaccentcmb.uc'], comment='Ż'),
    
    'Z.sc': GD(g2='Z.sc', g1='Z.sc', l2r='Z.sc', r='Z.sc', name='Z.sc', comment='Z.sc'),
    'Zacute.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Zacute.sc', base='Z.sc', accents=['acutecmb'], comment='Ź'),
    'Zcaron.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Zcaron.sc', base='Z.sc', accents=['caroncmb'], comment='Ž'),
    'Zdotaccent.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Zdotaccent.sc', base='Z.sc', accents=['dotaccentcmb'], comment='Ż'),
    
    'a': GD(g2='a', g1='a', uni=0x0061, c='a', name='a', isLower=True, comment='a Small Letters, Latin'),
    'aacute': GD(g2='a', g1='a', l='a', w='a', uni=0x00e1, c='á', name='aacute', isLower=True, base='a', accents=['acutecmb'], comment='á A WITH ACUTE, LATIN SMALL LETTER'),
    'abreve': GD(g2='a', g1='a', l='a', w='a', uni=0x0103, c='ă', name='abreve', isLower=True, base='a', accents=['brevecmb'], comment='ă A WITH BREVE, LATIN SMALL LETTER'),
    'acircumflex': GD(g2='a', g1='a', l='a', w='a', uni=0x00e2, c='â', name='acircumflex', isLower=True, base='a', accents=['circumflexcmb'], comment='â A WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'adieresis': GD(g2='a', g1='a', l='a', w='a', uni=0x00e4, c='ä', name='adieresis', isLower=True, base='a', accents=['dieresiscmb'], comment='ä A WITH DIAERESIS, LATIN SMALL LETTER'),
    'ae': GD(g2='a', g1='e', ml='a', mr='e', uni=0x00e6, c='æ', name='ae', isLower=True, comment='æ small ligature ae, latin'),
    'aeacute': GD(g2='a', g1='o', l='ae', w='ae', uni=0x01fd, c='ǽ', name='aeacute', base='ae', isLower=True, accents=['acutecmb'], comment='ǽ'),
    'agrave': GD(g2='a', g1='a', l='a', w='a', uni=0x00e0, c='à', name='agrave', base='a', isLower=True, accents=['gravecmb'], comment='à A WITH GRAVE, LATIN SMALL LETTER'),
    'amacron': GD(g2='a', g1='a', l='a', w='a', uni=0x0101, c='ā', name='amacron', base='a', isLower=True, accents=['macroncmb'], comment='ā A WITH MACRON, LATIN SMALL LETTER'),
    'aring': GD(g2='a', g1='a', l='a', w='a', uni=0x00e5, c='å', name='aring', isLower=True, base='a', accents=['ringcmb'], comment='å RING ABOVE, LATIN SMALL LETTER A WITH'),
    'atilde': GD(g2='a', g1='a', l='a', w='a', uni=0x00e3, c='ã', name='atilde', isLower=True, base='a', accents=['tildecmb'], comment='ã A WITH TILDE, LATIN SMALL LETTER'),
    'aringacute': GD(g2='a', g1='a', l='aring', w='aring', uni=0x01fb, c='ǻ', isLower=True, name='aringacute', base='a', accents=['ringacutecmb'], comment='ǻ'),
    'aogonek': GD(g2='a', g1='a', l='a', w='a', uni=0x0105, c='ą', name='aogonek', isLower=True, base='a', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='ą Latin Small Letter a with Ogonek'),

    'acute': GD(l=CENTER, w=ACCENT_WIDTH, base='acutecmb', uni=0x00b4, c='´', name='acute', isLower=True, anchors=[], comment='´ spacing acute accent'),
    'approxequal': GD(g2='asciitilde', g1='asciitilde', l='equal', w=MATH_WIDTH, uni=0x2248, c='≈', name='approxequal', src='equal', comment='≈ EQUAL TO, ALMOST', anchors=[]),
    'approxequal.uc': GD(g2='asciitilde', g1='asciitilde', l='equal', w=MATH_WIDTH, name='approxequal.uc', base='approxequal', comment='≈ EQUAL TO, ALMOST, Uppercase', anchors=[]),
    'asciicircum': GD(uni=0x005e, l=CENTER, w=ACCENT_WIDTH, c='^', base='circumflexcmb', name='asciicircum', anchors=[], comment='^ spacing circumflex accent'),
    'asciitilde': GD(l2r='asciitilde', uni=0x007e, c='~', name='asciitilde', comment='~ tilde, spacing', anchors=[]),
    'asciitilde.uc': GD(g2='asciitilde', g1='asciitilde', l='asciitilde', r='asciitilde', name='asciitilde.uc', base='asciitilde', comment='~ tilde, spacing Uppercase', anchors=[]),
    'asterisk': GD(l2r='asterisk', uni=0x002a, c='*', name='asterisk', comment='* star'),
    'asterisk.uc': GD(g2='asterisk', g1='asterisk', l='asterisk', r='asterisk', name='asterisk.uc', comment='* star Uppercase'),
    'at': GD(g2='O', g1='O', l='O', r='O', uni=0x0040, c='@', name='at', comment='@ COMMERCIAL AT'),
    #'at.alt1': GD(g2='O', g1='O', l='O', r='O', name='at.alt1', src='at', comment='@ COMMERCIAL AT alternate as spiral'),

    'ampersand': GD(l='a', uni=0x0026, c='&', name='ampersand', comment='& AMPERSAND', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT),
    'ampersand.sc': GD(l='ampersand', r='ampersand', name='ampersand.sc', src='ampersand', comment='& AMPERSAND Smallcap'),
    
    'b': GD(g2='b', g1='o', r='o', uni=0x0062, c='b', name='b', isLower=True, comment='b'),

    'backslash': GD(l='A', l2r='backslash', uni=0x005c, c='\\', name='backslash', anchors=[], comment='\\ SOLIDUS, REVERSE'),
    'backslash.sc': GD(l='A', l2r='backslash.sc', name='backslash.sc', src='backslash', anchors=[], comment='\\ SOLIDUS, REVERSE smallcap'),
    'bar': GD(g2='bar', g1='bar', l2r='bar', uni=0x007c, c='|', name='bar', comment='| VERTICAL LINE'),
    'brokenbar': GD(g2='bar', g1='bar', l='bar', w='bar', uni=0x00a6, c='¦', name='brokenbar', comment='¦ vertical bar, broken'),
    'braceleft': GD(l2r='braceleft', uni=0x007b, name='braceleft', c='{', comment='opening curly bracket'),
    'braceright': GD(l2r='braceleft', r2l='braceleft', uni=0x007d, c='}', name='braceright', comment='} RIGHT CURLY BRACKET'),
    'bracketleft': GD(uni=0x005b, c='[', name='bracketleft', comment='[ square bracket, opening'),
    'bracketright': GD(l2r='bracketleft', r2l='bracketleft', uni=0x005d, c=']', name='bracketright', comment='] SQUARE BRACKET, RIGHT'),
    'breve': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x02d8, c='˘', name='breve', base='brevecmb', comment='˘ Spacing Clones of Diacritics', anchors=[]),
    'bullet': GD(g2='bullet', g1='bullet', l2r='bullet', uni=0x2022, c='•', name='bullet', comment='• small circle, black', anchors=[]),
    'bullet.uc': GD(g2='bullet', g1='bullet', l='bullet', w='bullet', name='bullet.uc', comment='• small circle, black Uppercase', anchors=[]),
    
    'c': GD(g2='o', g1='c', l='o', uni=0x0063, c='c', name='c', isLower=True, comment='c'),
    'cacute': GD(g2='o', g1='c', l='c', w='c', uni=0x0107, c='ć', name='cacute', isLower=True, base='c', accents=['acutecmb'], comment='ć C WITH ACUTE, LATIN SMALL LETTER'),
    'ccaron': GD(g2='o', g1='c', l='c', w='c', uni=0x010d, c='č', name='ccaron', isLower=True, base='c', accents=['caroncmb'], comment='č C WITH CARON, LATIN SMALL LETTER'),
    'ccedilla': GD(g2='o', g1='c', l='c', w='c', uni=0x00e7, c='ç', name='ccedilla', isLower=True, base='c', accents=['cedillacmb'], comment='ç CEDILLA, LATIN SMALL LETTER C WITH'),
    'ccircumflex': GD(g2='o', g1='c', l='c', w='c', uni=0x0109, c='ĉ', name='ccircumflex', isLower=True, base='c', accents=['circumflexcmb'], comment='ĉ C WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'cdotaccent': GD(g2='o', g1='c', l='c', w='c', uni=0x010b, c='ċ', name='cdotaccent', isLower=True, base='c', accents=['dotaccentcmb']),

    'caron': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x02c7, c='ˇ', name='caron', base='caroncmb', comment='ˇ tone, mandarin chinese third', anchors=[]),
    'cedilla': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x00b8, c='¸', name='cedilla', isLower=True, base='cedillacmb', comment='¸ spacing cedilla', anchors=[]),
    'cent': GD(g2='o', g1='c', l='c', r='c', uni=0x00a2, c='¢', base='c', name='cent', isLower=True, comment='¢ CENT SIGN'),
    'cent.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, name='cent.tab', base='cent', isLower=True, comment='¢ CENT SIGN TAB'),
    'circumflex': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x02c6, c='ˆ', name='circumflex', base='circumflexcmb', comment='ˆ CIRCUMFLEX ACCENT, MODIFIER LETTER', anchors=[]),
    'colon': GD(g2='colon', g1='colon', l='period', r='period', uni=0x003a, c=':', name='colon', base='period', accents=['period'], comment='COLON', anchors=[]),
    'comma': GD(g2='comma', g1='comma', uni=0x002c, c=',', name='comma', anchors=[], comment=', separator, decimal'),
    'comma.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, name='comma.tab', base='comma', comment=', separator, decimal', anchors=[]),
    'copyright': GD(g2='copyright', g1='copyright', l='largecircle', r='largecircle', uni=0x00a9, c='©', name='copyright', base='largecircle', comment='© COPYRIGHT SIGN'),
    'currency': GD(l='O', r='O', uni=0x00a4, c='¤', name='currency', comment='¤ CURRENCY SIGN', anchors=[]),
    
    'd': GD(g2='o', g1='l', l='o', r='l', uni=0x0064, c='d', name='d', isLower=True, comment='d'),
    'd.cbr': GD(g2='o', g1='l', l='d', name='d.cbr', base='d', isLower=True, anchors=CARON_ANCHORS, comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'dcaron': GD(g2='o', g1='dcaron', l='d', mr='comma', rightMin=MIN_RIGHT, uni=0x010f, c='ď', name='dcaron', isLower=True, base='d', accents=['caroncmb.vert'], comment='ď D WITH CARON, LATIN SMALL LETTER'),
    'dcroat': GD(g2='o', g1='l', l='d', w='d', uni=0x0111, c='đ', name='dcroat', base='d', comment='đ D WITH STROKE, LATIN SMALL LETTER'),
    
    'dagger': GD(l2r='dagger', uni=0x2020, c='†', name='dagger', src='asterisk', comment='† DAGGER'),
    'daggerdbl': GD(g2='daggerdbl', g1='daggerdbl', l='dagger', r='dagger', uni=0x2021, c='‡', name='daggerdbl', src='dagger', comment='‡ DOUBLE DAGGER'),
    'degree': GD(l2r='degree', uni=0x00b0, c='°', name='degree', isLower=True, src='ringcmb', comment='° DEGREE SIGN', useSkewRotate=True, addItalicExtremePoints=True, anchors=[]),
    'dieresis': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x00a8, c='¨', name='dieresis', base='dieresiscmb', comment='¨ spacing diaeresis', anchors=[]),
    'divide': GD(l='plus', w=MATH_WIDTH, uni=0x00f7, c='÷', name='divide', comment='÷ obelus', anchors=[]),
    'divide.uc': GD(g2='divide', g1='divide', l='divide', w=MATH_WIDTH, name='divide.uc', comment='÷ obelus Uppercase', anchors=[]),
    'dollar': GD(g2='S', g1='S', l='S', r='S', uni=0x0024, c='$', base='S', name='dollar', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='$ milreis'),
    'dollar.alt1': GD(g2='S', g1='S', l='S', r='S', base='S', name='dollar.alt1', src='dollar', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='$ milreis'),
    'dollar.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, name='dollar.tab', src='dollar', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='$ milreis TAB'),
    'dollar.alt1.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, name='dollar.alt1.tab', src='dollar.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='$ milreis TAB'),
    'dotaccent': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x02d9, c='˙', name='dotaccent', base='dotaccentcmb', comment='˙ tone, mandarin chinese fifth or neutral', anchors=[]),
    
    'e': GD(g2='o', g1='e', l='o', r='o', uni=0x0065, c='e', name='e', isLower=True, comment='e'),
    'eacute': GD(g2='o', g1='e', l='e', w='e', uni=0x00e9, c='é', name='eacute', isLower=True, base='e', accents=['acutecmb'], comment='é E WITH ACUTE, LATIN SMALL LETTER'),
    'ebreve': GD(g2='o', g1='e', l='e', w='e', uni=0x0115, c='ĕ', name='ebreve', isLower=True, base='e', accents=['brevecmb'], comment='ĕ E WITH BREVE, LATIN SMALL LETTER'),
    'ecaron': GD(g2='o', g1='e', l='e', w='e', uni=0x011b, c='ě', name='ecaron', isLower=True, base='e', accents=['caroncmb'], comment='ě E WITH CARON, LATIN SMALL LETTER'),
    'ecircumflex': GD(g2='o', g1='e', l='e', w='e', uni=0x00ea, c='ê', name='ecircumflex', isLower=True, base='e', accents=['circumflexcmb'], comment='ê E WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'edieresis': GD(g2='o', g1='e', l='e', w='e', uni=0x00eb, c='ë', name='edieresis', isLower=True, base='e', accents=['dieresiscmb'], comment='ë E WITH DIAERESIS, LATIN SMALL LETTER'),
    'edotaccent': GD(g2='o', g1='e', l='e', w='e', uni=0x0117, c='ė', name='edotaccent', isLower=True, base='e', accents=['dotaccentcmb']),
    'egrave': GD(g2='o', g1='e', l='e', w='e', uni=0x00e8, c='è', name='egrave', isLower=True, base='e', accents=['gravecmb'], comment='è E WITH GRAVE, LATIN SMALL LETTER'),
    'emacron': GD(g2='o', g1='e', l='e', w='e', uni=0x0113, c='ē', name='emacron', isLower=True, base='e', accents=['macroncmb'], comment='ē E WITH MACRON, LATIN SMALL LETTER'),
    'eogonek': GD(g2='o', g1='eogonek', l='e', w='e', uni=0x0119, c='ę', name='eogonek', isLower=True, base='e', accents=['eogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='ę E WITH OGONEK, LATIN SMALL LETTER'),

    'ellipsis': GD(g2='period', g1='period', ml='period', mr='period', uni=0x2026, c='…', name='ellipsis', base='period', accents=['period', 'period'], comment='… three dot leader', anchors=[]), # Not as components of period
    'eng': GD(g2='n', g1='j', l='n', r='jdotless', uni=0x014b, c='ŋ', name='eng', isLower=True, comment='ŋ LATIN SMALL LETTER ENG'),
    'equal': GD(g2='hyphen', g1='hyphen', w=MATH_WIDTH, uni=0x003d, c='=', name='equal', comment='= EQUALS SIGN', anchors=[]),
    'equal.uc': GD(g2='hyphen', g1='hyphen', l='equal', w=MATH_WIDTH, name='equal.uc', comment='= EQUALS SIGN Uppercase', anchors=[]),
    'eth': GD(g2='o', g1='O', l='o', uni=0x00f0, c='ð', name='eth', src='six', comment='ð LATIN SMALL LETTER ETH'),
    'exclam': GD(l2r='exclam', uni=0x0021, c='!', name='exclam', comment='! factorial', useSkewRotate=True, addItalicExtremePoints=True),
    'exclamdown': GD(l2r='exclam', r2l='exclam', uni=0x00a1, c='¡', src180='exclam', name='exclamdown', comment='¡ INVERTED EXCLAMATION MARK'),
    'exclamdown.uc': GD(g2='exclamdown.uc', g1='exclamdown.uc', l2r='exclam', r2l='exclam', name='exclamdown.uc', base='exclamdown', comment='¡ INVERTED EXCLAMATION MARK'),

    'emdash': GD(g2='hyphen', g1='hyphen', l=CENTER, w=EM, uni=0x2014, c='—', name='emdash', comment='— EM DASH', copyFromDisplayRight=False, anchors=[]),
    'emdash.uc': GD(g2='hyphen', g1='hyphen', l='emdash', r='emdash', name='emdash.uc', base='emdash', comment='— EM DASH Uppercase', copyFromDisplayRight=False, anchors=[]),
    'endash': GD(g2='hyphen', g1='hyphen', l=CENTER, w=EM2, uni=0x2013, c='–', name='endash', comment='– EN DASH', copyFromDisplayRight=False, anchors=[]),
    'endash.uc': GD(g2='hyphen', g1='hyphen', l='endash', r='endash', name='endash.uc', base='endash', comment='– EN DASH Uppercase', copyFromDisplayRight=False, anchors=[]),
    'underscore': GD(l=CENTER, w=EM2, uni=0x005f, c='_', name='underscore', comment='_ underscore, spacing', anchors=[]),
    
    'f': GD(g2='f', g1='f', rightMin=MIN_RIGHT, fixAnchors=False, uni=0x0066, c='f', name='f', comment='f', copyFromDisplayRight=False),
    'fi': GD(g2='f', g1='i', l='f', mr='i', uni=0xfb01, c='ﬁ', name='fi', base='f.ij', accents=['idotless'], comment='ﬁ f_i', anchors=ALL_IJ_ANCHORS),
    'fl': GD(g2='f', g1='l', l='f', mr='l', uni=0xfb02, c='ﬂ', name='fl', base='f.short', accents=['l'], comment='ﬂ f_l', anchors=ALL_IJ_ANCHORS),
    'f.overshoot': GD(g2='f', g1='f', l='f', w='f', name='f.overshoot', src='f', copyFromDisplayRight=False, anchors=ALL_IJ_ANCHORS, comment='f overshoot looped thin flag over diacritics such as /iacute'),
    'f.short': GD(g2='f', l='f', w='f', name='f.short', copyFromDisplayRight=False, anchors=ALL_IJ_ANCHORS, comment='f with straight thin flag to connect with @f_ascenders'),
    'f.curly': GD(g2='f', l='f', w='f', name='f.curly', copyFromDisplayRight=False, anchors=ALL_IJ_ANCHORS, comment='f curly looped thin flag to connect with @f_curlyAscenders'),
    'f.small': GD(g2='f', l='f', w='f', name='f.small', copyFromDisplayRight=False, anchors=ALL_IJ_ANCHORS, comment='f with small flag to connect to figures'),
    'f.ij': GD(g2='f', l='f', w='f', name='f.ij', copyFromDisplayRight=False, anchors=ALL_IJ_ANCHORS, comment='f with extended flag for f-->i and f-->j'),

    'florin': GD(g2='florin', g1='florin', w='f', uni=0x0192, c='ƒ', name='florin', src='f', copyFromDisplayRight=False, comment='ƒ script f, latin small letter'),
    'fraction': GD(g2='fraction', g1='fraction', l=-130, r=-130, name='fraction', uni=0x2044, c='⁄', comment='⁄ solidus', anchors=[]),

    'g': GD(g2='g', g1='g', uni=0x0067, c='g', name='g', isLower=True, comment='g'),
    'earlessg': GD(g2='g', g1='g', l='g', w='g', name='earlessg', isLower=True, src='g', comment='g with ear to accommodate accents', copyFromDisplayRight=False),
    'gbreve': GD(g2='g', g1='g', l='g', w='g', uni=0x011f, c='ğ', name='gbreve', isLower=True, base='earlessg', accents=['brevecmb'], comment='ğ G WITH BREVE, LATIN SMALL LETTER'),
    'gcaron': GD(g2='g', g1='g', l='g', w='g', uni=0x01e7, c='ǧ', name='gcaron', isLower=True, base='earlessg', accents=['caroncmb'], comment='ǧ G WITH CARON, LATIN SMALL LETTER'),
    'gcircumflex': GD(g2='g', g1='g', l='g', w='g', uni=0x011d, c='ĝ', name='gcircumflex', base='earlessg', accents=['circumflexcmb'], comment='ĝ G WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'gcommaaccent': GD(g2='g', g1='g', l='g', w='g', uni=0x0123, c='ģ', name='gcommaaccent', isLower=True, base='earlessg', accents=['commaturnedabovecmb']),
    'gdotaccent': GD(g2='g', g1='g', l='g', w='g', uni=0x0121, c='ġ', name='gdotaccent', base='earlessg', accents=['dotaccentcmb']),
    
    'germandbls': GD(g2='germandbls', g1='germandbls', l='f', r='o', uni=0x00df, c='ß', name='germandbls', isLower=True, copyFromDisplayRight=False, comment='ß SHARP S, LATIN SMALL LETTER'),
    'Germandbls': GD(g2='germandbls', g1='germandbls', l='f', r='S', uni=0x1E9E, c='ẞ', name='Germandbls', src='germandbls', isLower=False, copyFromDisplayRight=False, comment='ẞ Latin Capital Letter Sharp S'),
    'Germandbls.sc': GD(g2='germandbls', g1='germandbls', l='f', r='S.sc', name='Germandbls.sc', src='Germandbls', isLower=False, comment='ẞ Small caps Latin Capital Letter Sharp S'),
    
    'grave': GD(l=CENTER, w=ACCENT_WIDTH, uni=0x0060, c='`', name='grave', base='gravecmb', anchors=[], comment='` spacing grave accent'),
    'greater': GD(g2='greater', g1='greater', w=MATH_WIDTH, uni=0x003e, c='>', name='greater', comment='> GREATER-THAN SIGN', anchors=[]),
    'greater.uc': GD(g2='greater', g1='greater', l='greater', w=MATH_WIDTH, name='greater.uc', comment='> GREATER-THAN SIGN Uppercase', anchors=[]),
    'greaterequal': GD(g2='greater', g1='greater', l='greater', w=MATH_WIDTH, uni=0x2265, c='≥', name='greaterequal', comment='≥ GREATER-THAN OR EQUAL TO', anchors=[]),
    'greaterequal.uc': GD(g2='greaterequal', g1='greaterequal', l='greater', w=MATH_WIDTH, name='greaterequal.uc', comment='≥ GREATER-THAN OR EQUAL TO Uppercase', anchors=[]),
    'guilsinglleft': GD(g2='guilsinglleft', g1='guilsinglleft', l=40, r=40, uni=0x2039, c='‹', name='guilsinglleft', comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK', anchors=[]),
    'guilsinglleft.uc': GD(g2='guilsinglleft', g1='guilsinglleft', l2r='guilsinglleft', name='guilsinglleft.uc', base='guilsinglleft', comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK', anchors=[]),
    'guilsinglright': GD(g2='guilsinglright', g1='guilsinglright', l='guilsinglleft', r='guilsinglleft', uni=0x203a, c='›', name='guilsinglright', comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK', anchors=[]),
    'guilsinglright.uc': GD(g2='guilsinglright', g1='guilsinglright', l='guilsinglleft', r='guilsinglleft', base='guilsinglright', name='guilsinglright.uc', comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK', anchors=[]),
    'guillemotleft': GD(g2='guilsinglleft', g1='guilsinglleft', ml='guilsinglleft', mr='guilsinglleft', uni=0x00AB, c='«', name='guillemotleft', base='guilsinglleft', accents=['guilsinglleft'], anchors=[]),
    'guillemotleft.uc': GD(g2='guilsinglleft', g1='guilsinglleft', ml='guilsinglleft', mr='guilsinglleft', name='guillemotleft.uc', base='guilsinglleft', accents=['guilsinglleft'], anchors=[]),
    'guillemotright': GD(g2='guilsinglright', g1='guilsinglright', ml='guilsinglleft', mr='guilsinglleft', uni=0x00BB, name='guillemotright', c='»', base='guilsinglright', accents=['guilsinglright'], anchors=[]),
    'guillemotright.uc': GD(g2='guilsinglright', g1='guilsinglright', ml='guilsinglleft', mr='guilsinglleft', name='guillemotright.uc', base='guilsinglright', accents=['guilsinglright'], anchors=[]),

    'h': GD(g2='h', g1='n', r='n', uni=0x0068, c='h', name='h', isLower=True, comment='h', topY=TOP_Y), # Source for left spacing in Roman
    'h.cbr': GD(g2='h', g1='n', l='h', w='h', template='h', name='h.cbr', base='h', isLower=True, comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'hbar': GD(g2='h', g1='n', l='h', w='h', uni=0x0127, c='ħ', name='hbar', base='h', isLower=True, comment='ħ H WITH STROKE, LATIN SMALL LETTER'),
    'hcircumflex': GD(g2='h', g1='n', l='h', w='h', uni=0x0125, c='ĥ', name='hcircumflex', isLower=True, base='h', accents=['circumflexcmb.uc'], comment='ĥ H WITH CIRCUMFLEX, LATIN SMALL LETTER'),

    'horizontalbar': GD(g2='hyphen', g1='hyphen', l='emdash', r='emdash', uni=0x2015, c='―', name='horizontalbar', base='emdash', copyFromDisplayRight=False, anchors=[]),
    'horizontalbar.uc': GD(g2='hyphen', g1='hyphen', l='horizontalbar', r='horizontalbar', name='horizontalbar.uc', comment='Horizontal base Uppercase', copyFromDisplayRight=False, anchors=[]),
    'hungarumlaut': GD(g2='hungarumlaut', g1='hungarumlaut', l=CENTER, w=ACCENT_WIDTH, uni=0x02dd, c='˝', name='hungarumlaut', base='hungarumlautcmb', comment='˝ DOUBLE ACUTE ACCENT', anchors=[]),
    'hyphen': GD(g2='hyphen', g1='hyphen', l2r='hyphen', uni=0x002d, unicodes=(0x002d, 8208), c='-', name='hyphen', comment='- minus sign, hyphen', anchors=[]),
    'hyphen.uc': GD(g2='hyphen', g1='hyphen', l='hyphen', r='hyphen', name='hyphen.uc', base='hyphen', comment='- minus sign, hyphen', copyFromDisplayRight=False, anchors=[]),
    'nbhyphen': GD(g2='hyphen', g1='hyphen', l2r='hyphen', uni=0x2011, c='‑', name='nbhyphen', base='hyphen', comment='‑ minus sign, non breaking hyphen', copyFromDisplayRight=False, anchors=[]),
    'nbhyphen.uc': GD(g2='hyphen', g1='hyphen', l2r='hyphen', name='nbhyphen.uc', base='nbhyphen', comment='‑ minus sign, non breaking hyphen for capitals', copyFromDisplayRight=False, anchors=[]),
    'softhyphen': GD(uni=0x00ad, name='softhyphen', comment='SOFT HYPHEN, Required by Type Network set.', anchors=[]),

    'idotless': GD(g2='i', g1='i', uni=0x0131, c='ı', src='i', isLower=True, name='idotless', anchors=ALL_IJ_ANCHORS),
    'i': GD(g2='i', g1='i', l='idotless', w='idotless', r='idotless', uni=0x0069, c='i', name='i', isLower=True, comment='i', anchors=ALL_IJ_ANCHORS),
    'i.trk': GD(g2='i', g1='i', l='n', r='n', name='i.trk', isLower=True, comment='i.trk', base='idotless', accents=['dotaccentcmb'], anchors=ALL_IJ_ANCHORS),
    'i.cbr': GD(g2='i', g1='i', w='i', template='i', name='i.cbr', base='i', isLower=True, anchors=ALL_IJ_ANCHORS, comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'iacute': GD(g2='i', g1='i', l='i', w='i', uni=0x00ed, c='í', isLower=True, name='iacute', base='idotless', accents=['acutecmb'], anchors=ALL_IJ_ANCHORS, comment='í I WITH ACUTE, LATIN SMALL LETTER'),
    'ibreve': GD(g2='i', g1='i', l='i', w='i', uni=0x012d, c='ĭ', isLower=True, name='ibreve', base='idotless', accents=['brevecmb'], anchors=ALL_IJ_ANCHORS, comment='ĭ I WITH BREVE, LATIN SMALL LETTER'),
    'icircumflex': GD(g2='i', g1='i', l='i', w='i', uni=0x00ee, c='î', isLower=True, name='icircumflex', base='idotless', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS, comment='î I WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'idieresis': GD(g2='i', g1='i', l='i', w='i', uni=0x00ef, c='ï', isLower=True, name='idieresis', base='idotless', accents=['dieresiscmb'], anchors=ALL_IJ_ANCHORS, comment='ï I WITH DIAERESIS, LATIN SMALL LETTER'),
    'igrave': GD(g2='i', g1='i', l='i', w='i', uni=0x00ec, c='ì', name='igrave', isLower=True, base='idotless', accents=['gravecmb'], anchors=ALL_IJ_ANCHORS, comment='ì I WITH GRAVE, LATIN SMALL LETTER'),
    'imacron': GD(g2='i', g1='i', l='i', w='i', uni=0x012b, c='ī', name='imacron', isLower=True, base='idotless', accents=['macroncmb'], anchors=ALL_IJ_ANCHORS, comment='ī I WITH MACRON, LATIN SMALL LETTER'),
    'iogonek': GD(g2='i', g1='i', l='i', w='i', uni=0x012f, c='į', name='iogonek', isLower=True, base='i', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='į I WITH OGONEK, LATIN SMALL LETTER'),
    'itilde': GD(g2='i', g1='i', l='i', w='i', uni=0x0129, c='ĩ', name='itilde', isLower=True, base='idotless', accents=['tildecmb'], anchors=ALL_IJ_ANCHORS, comment='ĩ I WITH TILDE, LATIN SMALL LETTER'),
    'ij': GD(g2='i', g1='j', l='i', mr='j', uni=0x0133, c='ĳ', name='ij', isLower=True, base='i', accents=['j'], anchors=ALL_IJ_ANCHORS, comment='Dutch ij'),

    'infinity': GD(ml='o', mr='o', uni=0x221e, c='∞', name='infinity', comment='∞ INFINITY'),
    'integral': GD(l=CENTER, w=TAB, uni=0x222b, c='∫', name='integral', src='f', anchors=[], copyFromDisplayRight=False, comment='∫ Integral Signs'),
    
    'jdotless': GD(g2='j', g1='j', uni=0x0237, c='ȷ', src='j', name='jdotless', anchors=ALL_IJ_ANCHORS),
    'j': GD(g2='j', g1='j', uni=0x006a, c='j', l='jdotless', w='jdotless', name='j', isLower=True, anchors=ALL_IJ_ANCHORS, comment='j'),
    'jcircumflex': GD(g2='j', g1='j', l='j', w='j', uni=0x0135, c='ĵ', name='jcircumflex', isLower=True, base='jdotless', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS, comment='ĵ J WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    
    'k': GD(g2='h', g1='k', l='h', uni=0x006b, c='k', name='k', isLower=True, comment='k'),
    'k.cbr': GD(g2='h', g1='k', l='k', template='k', name='k.cbr', base='k', isLower=True, comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'kcommaaccent': GD(g2='h', g1='k', uni=0x0137, c='ķ', name='kcommaaccent', isLower=True, base='k', accents=['commabelowcmb']),
    #'kgreen': GD(g2='i', g1='k', l='i', r='k', uni=0x0138, c='ĸ', src='k', name='kgreen', isLower=True, comment='ĸ'),
    
    'l': GD(g2='h', g1='l', l='h', r='n', uni=0x006c, c='l', name='l', isLower=True, comment='l', anchors=CARON_ANCHORS, topY=TOP_Y),
    'l.cbr': GD(g2='h', g1='l', ml='l', w='l', template='l', name='l.cbr', base='l', isLower=True, anchors=CARON_ANCHORS, comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'lacute': GD(g2='h', g1='lacute', ml='l', w='l', uni=0x013a, c='ĺ', name='lacute', isLower=True, base='l', accents=['acutecmb.uc'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER'),
    'lcaron': GD(g2='h', g1='dcaron', ml='l', mr='comma', uni=0x013e, c='ľ', name='lcaron', base='l', isLower=True, accents=['caroncmb.vert'], comment='ľ L WITH CARON, LATIN SMALL LETTER'),
    'lcommaaccent': GD(g2='h', g1='l', ml='l', w='l', uni=0x013c, c='ļ', name='lcommaaccent',isLower=True, base='l', accents=['commabelowcmb']),
    'ldot': GD(g2='h', g1='ldot', ml='l', uni=0x0140, c='ŀ', name='ldot', isLower=True, base='l', accents=['dotmiddlecmb'], comment='ŀ MIDDLE DOT, LATIN SMALL LETTER L WITH'),
    'lslash': GD(g2='lslash', g1='lslash', l='l', w='l', uni=0x0142, c='ł', name='lslash', isLower=True, base='l', comment='ł L WITH STROKE, LATIN SMALL LETTER'),

    'less': GD(g2='less', g1='less', w=MATH_WIDTH, uni=60, c='<', name='less', comment='< LESS-THAN SIGN', anchors=[]),
    'less.uc': GD(g2='less', g1='less', l='less', w=MATH_WIDTH, name='less.uc', comment='< LESS-THAN SIGN Uppercase', anchors=[]),
    'lessequal': GD(g2='less', g1='less', l='less', w=MATH_WIDTH, uni=0x2264, c='≤', name='lessequal', comment='≤ LESS-THAN OR EQUAL TO', anchors=[]),
    'lessequal.uc': GD(g2='lessequal', g1='lessequal', l='less', w=MATH_WIDTH, name='lessequal.uc', comment='≤ LESS-THAN OR EQUAL TO Uppercase', anchors=[]),
    'logicalnot': GD(g2='logicalnot', g1='logicalnot', l='equal', w=MATH_WIDTH, uni=0x00ac, c='¬', name='logicalnot', comment='¬ NOT SIGN', anchors=[]),
    'logicalnot.uc': GD(g2='logicalnot', g1='logicalnot', l='equal', w=MATH_WIDTH,  name='logicalnot.uc', comment='¬ NOT SIGN Uppercase', anchors=[]),
    'lozenge': GD(l2r='lozenge', uni=0x25ca, c='◊', name='lozenge', comment='◊ LOZENGE', anchors=[]),

    'm': GD(g2='n', g1='n', l='n', r='n', uni=0x006d, c='m', name='m', isLower=True, comment='m'),
    'm.cbr': GD(g2='n', g1='n', l='m', name='m.cbr', template='m', base='m', isLower=True, comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    
    'macron': GD(g2='macron', g1='macron', l=CENTER, w=ACCENT_WIDTH, uni=0x00af, c='¯', name='macron', base='macroncmb', comment='¯ spacing macron', anchors=[]),
    'minus': GD(g2='hyphen', g1='hyphen', l='equal', w=MATH_WIDTH, uni=0x2212, c='−', name='minus', comment='− MINUS SIGN', anchors=[]),
    'minus.uc': GD(g2='hyphen', g1='hyphen', l='equal', w=MATH_WIDTH, name='minus.uc', comment='− MINUS SIGN Uppercase', anchors=[]),
    'minute': GD(g2='quotesingle', g1='quotesingle', ml='quotesingle', mr='quotesingle', uni=0x2032, c='′', base='quotesingle', name='minute', comment='′ PRIME', anchors=[]),
    'mu': GD(g2='mu', g1='mu', l='u', r='u', uni=0x03bc, c='μ', name='mu', hex='03bc', isLower=True, comment='mu', base='u', anchors=[], copyFromDisplayRight=False, copyFromDisplayLeft=False),
    'microsign': GD(g2='microsign', g1='microsign', l='u', r='u', uni=0x00b5, c='µ', name='microsign', hex='00b5', isLower=True, comment='mu', base='mu', anchors=[], copyFromDisplayRight=False, copyFromDisplayLeft=False),
    'multiply': GD(l=CENTER, w=MATH_WIDTH, uni=0x00d7, c='×', name='multiply', src='plus', comment='× product, cartesian', anchors=[]),
    'multiply.uc': GD(g2='multiply', g1='multiply', l='multiply', w=MATH_WIDTH, name='multiply.uc', comment='Multiply Uppercase', anchors=[]),
    
    'n': GD(g2='n', g1='n', uni=0x006e, c='n', name='n', isLower=True, comment='n'),
    'n.cbr': GD(g2='n', g1='n', l='n', w='n', name='n.cbr', template='n', isLower=True, base='n', comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'nacute': GD(g2='n', g1='n', l='n', w='n', uni=0x0144, c='ń', name='nacute', isLower=True, base='n', accents=['acutecmb'], comment='ń N WITH ACUTE, LATIN SMALL LETTER'),
    'ncaron': GD(g2='n', g1='n', l='n', w='n', uni=0x0148, c='ň', name='ncaron', isLower=True, base='n', accents=['caroncmb'], comment='ň N WITH CARON, LATIN SMALL LETTER'),
    'ncommaaccent': GD(g2='n', g1='n', l='n', w='n', uni=0x0146, c='ņ', name='ncommaaccent', isLower=True, base='n', accents=['commabelowcmb']),
    'ntilde': GD(g2='n', g1='n', l='n', w='n', uni=0x00f1, c='ñ', name='ntilde', isLower=True, base='n', accents=['tildecmb'], comment='ñ N WITH TILDE, LATIN SMALL LETTER'),
    
    'notequal': GD(g2='hyphen', g1='hyphen', l='equal', w=MATH_WIDTH, uni=0x2260, c='≠', name='notequal', base='equal', comment='≠ NOT EQUAL TO', anchors=[]),
    'notequal.uc': GD(g2='equal', g1='equal', l='equal', w=MATH_WIDTH, name='notequal.uc', comment='≠ NOT EQUAL TO Uppercase', anchors=[]),
    'numbersign': GD(g2='numbersign', g1='numbersign', l2r='numbersign', uni=0x0023, c='#', name='numbersign', comment='# pound sign'),
    'numbersign.uc': GD(g2='numbersign', g1='numbersign', l='numbersign', w='numbersign', name='numbersign.uc', comment='# pound sign Uppercase'),
    
    'o': GD(g2='o', g1='o', l2r='o', uni=0x006f, c='o', name='o', isLower=True, comment='o', anchors=ALL_IJ_ANCHORS),
    'oacute': GD(g2='o', g1='o', l='o', w='o', uni=0x00f3, c='ó', name='oacute', isLower=True, base='o', accents=['acutecmb'], anchors=ALL_IJ_ANCHORS, comment='ó O WITH ACUTE, LATIN SMALL LETTER'),
    'obreve': GD(g2='o', g1='o', l='o', w='o', uni=0x014f, c='ŏ', name='obreve', isLower=True, base='o', accents=['brevecmb'], anchors=ALL_IJ_ANCHORS, comment='ŏ O WITH BREVE, LATIN SMALL LETTER'),
    'ocircumflex': GD(g2='o', g1='o', l='o', w='o', uni=0x00f4, c='ô', name='ocircumflex', isLower=True, base='o', accents=['circumflexcmb'], anchors=ALL_IJ_ANCHORS, comment='ô O WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'odieresis': GD(g2='o', g1='o', l='o', w='o', uni=0x00f6, c='ö', name='odieresis', isLower=True, base='o', accents=['dieresiscmb'], anchors=ALL_IJ_ANCHORS, comment='ö O WITH DIAERESIS, LATIN SMALL LETTER'),
    'oe': GD(g2='o', g1='e', ml='o', mr='e', uni=0x0153, c='œ', name='oe', base='o', accents=['e'], anchors=ALL_IJ_ANCHORS, comment='œ SMALL LIGATURE OE, LATIN'),
    'ograve': GD(g2='o', g1='o', l='o', w='o', uni=0x00f2, c='ò', name='ograve', isLower=True, base='o', accents=['gravecmb'], anchors=ALL_IJ_ANCHORS, comment='ò O WITH GRAVE, LATIN SMALL LETTER'),
    'ohungarumlaut': GD(g2='o', g1='o', l='o', w='o', uni=0x0151, c='ő', name='ohungarumlaut', isLower=True, base='o', accents=['hungarumlautcmb'], anchors=ALL_IJ_ANCHORS),
    'omacron': GD(g2='o', g1='o', l='o', w='o', uni=0x014d, c='ō', name='omacron', isLower=True, base='o', accents=['macroncmb'], anchors=ALL_IJ_ANCHORS, comment='ō O WITH MACRON, LATIN SMALL LETTER'),
    'oslash': GD(g2='o', g1='o',l='o', w='o', uni=0x00f8, c='ø', name='oslash', isLower=True, base='o', anchors=ALL_IJ_ANCHORS, comment='ø STROKE, LATIN SMALL LETTER O WITH'),
    'oslashacute': GD(g2='o', g1='o',l='o', w='o', uni=0x01ff, c='ǿ', name='oslashacute', isLower=True, base='oslash', anchors=ALL_IJ_ANCHORS, accents=['acutecmb'], comment='ǿ'),
    'otilde': GD(g2='o', g1='o',l='o', w='o', uni=0x00f5, c='õ', name='otilde', isLower=True, base='o', accents=['tildecmb'], anchors=ALL_IJ_ANCHORS, comment='õ O WITH TILDE, LATIN SMALL LETTER'),

    'ogonek': GD(g2='ogonek', g1='ogonek', l=CENTER, w=ACCENT_WIDTH, uni=0x02db, c='˛', name='ogonek',isLower=True,  base='ogonekcmb', comment='˛ OGONEK', anchors=[]),
    'ordfeminine': GD(g1='ordfeminine', g2='ordfeminine', l='ordmasculine', r='ordmasculine', uni=0x00aa, c='ª', name='ordfeminine', comment='ª ORDINAL INDICATOR, FEMININE'),
    'ordmasculine': GD(g1='ordfeminine', g2='ordfeminine', l2r='ordmasculine', uni=0x00ba, c='º', name='ordmasculine', comment='º ORDINAL INDICATOR, MASCULINE', useSkewRotate=True, addItalicExtremePoints=True),
    
    'p': GD(g2='p', g1='o',l='n', r='o', uni=0x0070, c='p', name='p', isLower=True, comment='p'),
    
    'paragraph': GD(g2='T', g1='bar', l='O', r='N', uni=0x00b6, c='¶', name='paragraph', comment='¶ section sign, european'),
    'parenleft': GD(l='O', r='H', uni=0x0028, c='(', name='parenleft', comment='( parenthesis, opening'),
    'parenright': GD(l2r='parenleft', r2l='parenleft', uni=0x0029, c=')', name='parenright', comment=') RIGHT PARENTHESIS'),
    'partialdiff': GD(l='o', r='o', uni=0x2202, c='∂', src='six', name='partialdiff', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='∂ PARTIAL DIFFERENTIAL'),
    'period': GD(g2='period', g1='period', l2r='period', uni=0x002e, c='.', name='period', anchors=[], comment='. point, decimal'),
    'period.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, name='period.tab', base='period', comment='. point, decimal', anchors=[]),
    'periodcentered': GD(l='period', w='period', uni=0x00b7, c='·', name='periodcentered', base='period', anchors=[]),
    'periodcentered.uc': GD(g2='periodcentered', g1='periodcentered', l='period', w='period', name='periodcentered.uc', anchors=[]),
    'pi': GD(l2r='pi', uni=0x03c0, c='π', name='pi', isLower=True, src='t', anchors=[]),
    'plus': GD(l='equal', w=MATH_WIDTH, uni=0x002b, c='+', name='plus', comment='+ PLUS SIGN', anchors=[]),
    'plus.uc': GD(g2='equal', g1='plus', l='plus', w=MATH_WIDTH, name='plus.uc', comment='+ PLUS SIGN Uppercase', anchors=[]),
    'plusminus': GD(l='equal', w=MATH_WIDTH, uni=0x00b1, c='±', name='plusminus', comment='± PLUS-MINUS SIGN', anchors=[]),
    'plusminus.uc': GD(g2='plusminus', g1='plusminus',l='equal', w=MATH_WIDTH, name='plusminus.uc', comment='± PLUS-MINUS SIGN Uppercase', anchors=[]),
    'product': GD(l='H', r='H', uni=0x220f, c='∏', src='H', name='product', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='∏ PRODUCT, N-ARY'),
    
    'q': GD(g2='o', g1='q', l='o', uni=0x0071, c='q', name='q', isLower=True, comment='q'),
    'question': GD(l2r='question', uni=0x003f, c='?', name='question', comment='? QUESTION MARK', useSkewRotate=True, addItalicExtremePoints=True),
    'questiondown': GD(l2r='question', r2l='question', uni=0x00bf, c='¿', src180='question', name='questiondown', comment='¿ turned question mark'),
    'questiondown.uc': GD(g2='questiondown.uc', g1='questiondown.uc', l2r='question', r2l='question', name='questiondown.uc', base='questiondown', comment='¿ turned question mark'),
    
    'quoteleft': GD(g2='quoteleft', g1='quoteleft', l2r='comma', r2l='comma', uni=0x2018, c='‘', name='quoteleft', src='comma', comment='‘ turned comma quotation mark, single', copyFromDisplayRight=False, anchors=[]),
    'quoteright': GD(g2='quoteright', g1='quoteright', l='comma', r='comma', uni=0x2019, c='’', name='quoteright', base='comma', comment='’ SINGLE QUOTATION MARK, RIGHT', copyFromDisplayRight=False, anchors=[]),
    'quotesinglbase': GD(g2='comma', g1='comma', l='comma', r='comma', uni=0x201a, c='‚', name='quotesinglbase', base='comma', comment='‚ SINGLE LOW-9 QUOTATION MARK', copyFromDisplayRight=False, anchors=[]),
    'quotesingle': GD(g2='quotesingle', g1='quotesingle', l2r='quotesingle', uni=0x0027, c="'", name='quotesingle', src='exclam', comment="' single quotation mark, neutral", copyFromDisplayRight=False, anchors=[]),
    'quotedblleft': GD(g2='quoteleft', g1='quoteleft', ml='comma', mr='comma', uni=0x201c, c='“', name='quotedblleft', base='quoteleft', accents=['quoteleft'], comment='“ turned comma quotation mark, double', copyFromDisplayRight=False, anchors=[]),
    'quotedblright': GD(g2='quoteright', g1='quoteright', ml='comma', mr='comma', uni=0x201d, c='”', name='quotedblright', base='quoteright', accents=['quoteright'], comment='” RIGHT DOUBLE QUOTATION MARK', copyFromDisplayRight=False, anchors=[]),
    'quotedblbase': GD(g2='comma', g1='comma', ml='comma', mr='comma', uni=0x201e, c='„', name='quotedblbase', base='comma', accents=['comma'], comment='„ quotation mark, low double comma', copyFromDisplayRight=False, anchors=[]),
    'quotedbl': GD(g2='quotesingle', g1='quotesingle', ml='quotesingle', mr='quotesingle', uni=0x0022, c='"', name='quotedbl', base='quotesingle', accents=['quotesingle'], comment='" quotation mark, neutral', copyFromDisplayRight=False, anchors=[]),
    
    'r': GD(g2='n', g1='r', l='n', uni=0x0072, c='r', name='r', isLower=True, comment='r'),
    'racute': GD(g2='n', g1='r', l='r', w='r', uni=0x0155, c='ŕ', name='racute', isLower=True, base='r', accents=['acutecmb'], comment='ŕ R WITH ACUTE, LATIN SMALL LETTER'),
    'rcaron': GD(g2='n', g1='r', l='r', w='r', uni=0x0159, c='ř', name='rcaron', isLower=True, base='r', accents=['caroncmb'], comment='ř R WITH CARON, LATIN SMALL LETTER'),
    'rcommaaccent': GD(g2='n', g1='r', l='r', w='r', uni=0x0157, c='ŗ', name='rcommaaccent', isLower=True, base='r', accents=['commabelowcmb'], comment='ŗ R WITH CEDILLA, LATIN SMALL LETTER'),
    
    'registered': GD(g2='copyright', g1='copyright', l='copyright', r='copyright', uni=0x00ae, c='®', name='registered', base='largecircle', comment='® trade mark sign, registered'),
    'largecircle': GD(g2='largecircle', g1='largecircle', l=40, l2r='largecircle', uni=0x25ef, c='◯', name='largecircle', comment='circle for ® trade mark sign, registered', useSkewRotate=True, addItalicExtremePoints=True),
    'ring': GD(g2='ring', g1='ring', l=CENTER, w=ACCENT_WIDTH, uni=0x02da, c='˚', name='ring', base='ringcmb', comment='˚ RING ABOVE', anchors=[]),
    'radical': GD(g2='v', g1='V', l='v', r='V', uni=0x221a, c='√', name='radical', src='V', isLower=True, comment='√ SQUARE ROOT', anchors=[]),
    
    's': GD(g2='s', g1='s', l2r='s', uni=0x0073, c='s', name='s', isLower=True, comment='s'),
    'sacute': GD(g2='s', g1='s', l='s', w='s', uni=0x015b, c='ś', name='sacute', isLower=True, base='s', accents=['acutecmb'], comment='ś S WITH ACUTE, LATIN SMALL LETTER'),
    'scaron': GD(g2='s', g1='s', l='s', w='s', uni=0x0161, c='š', name='scaron', isLower=True, base='s', accents=['caroncmb'], comment='š S WITH CARON, LATIN SMALL LETTER'),
    'scedilla': GD(g2='s', g1='s', l='s', w='s', uni=0x015f, c='ş', name='scedilla', isLower=True, base='s', accents=['cedillacmb'], comment='ş S WITH CEDILLA, LATIN SMALL LETTER'),
    'scircumflex': GD(g2='s', g1='s', l='s', w='s', uni=0x015d, c='ŝ', name='scircumflex', isLower=True, base='s', accents=['circumflexcmb'], comment='ŝ S WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'scommaaccent': GD(g2='s', g1='s', l='s', w='s', uni=0x0219, c='ș', name='scommaaccent', isLower=True, base='s', accents=['commabelowcmb'], comment='ș S WITH COMMA BELOW, LATIN SMALL LETTER'),

    'schwa': GD(g2='o', g1='o', l2r='e', r2l='e', uni=0x0259, c='ə', name='schwa', isLower=True, src180='e', comment='ə SCHWA, LATIN SMALL LETTER'),
    'second': GD(g2='quotesingle', g1='quotesingle', l='minute', r='minute', uni=0x2033, c='″', base='quotesingle', name='second', comment='″ seconds', anchors=[]),
    'section': GD(l='s', r='s', uni=0x00a7, c='§', src='s', name='section', comment='§ SECTION SIGN'),
    'semicolon': GD(g2='colon', g1='colon', l='comma', w='comma', uni=0x003b, c=';', name='semicolon', base='comma', accents=['period'], comment='; SEMICOLON', anchors=[]),
    'slash': GD(l='A', l2r='slash', uni=0x002f, c='/', name='slash', comment='/ virgule', anchors=[]),
    'slash.sc': GD(l='A', l2r='slash.sc', name='slash.sc', src='slash', comment='/ virgule smallcap', anchors=[]),
    'space': GD(g1='space', g2='space', w=WORD_SPACE, uni=0x0020, c=' ', name='space', comment='  Symbols, ASCII Punctuation and', anchors=[]),
    'sterling': GD(l2r='sterling', uni=0x00a3, c='£', name='sterling', comment='£ sterling, pound', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT),
    'sterling.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, name='sterling.tab', src='sterling', comment='£ sterling, pound TAB', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT),
    'summation': GD(l='H', r='E', uni=0x2211, c='∑', name='summation', src='E', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='∑ SUMMATION, N-ARY'),
    
    't': GD(g2='t', g1='t', uni=0x0074, c='t', name='t', comment='t', isLower=True, anchors=CARON_ANCHORS, topY=TOP_Y),
    'tbar': GD(g2='t', g1='t', l='t', w='t', uni=0x0167, c='ŧ', name='tbar', isLower=True, base='t', comment='ŧ T WITH STROKE, LATIN SMALL LETTER'),
    'tcaron': GD(g2='t', g1='tcaron', l='t', w='t', uni=0x0165, c='ť', name='tcaron', isLower=True, base='t', accents=['caroncmb.vert'], comment='ť T WITH CARON, LATIN SMALL LETTER'),
    'tcedilla': GD(g2='t', g1='t', l='t', w='t', uni=0x0163, c='ţ', name='tcedilla', isLower=True, base='t', accents=['cedillacmb'], comment='ţ T WITH CEDILLA, LATIN SMALL LETTER'),
    'tcommaaccent': GD(g2='t', g1='t', l='t', w='t', uni=0x021b, c='ț', name='tcommaaccent', isLower=True, base='t', accents=['commabelowcmb'], comment='ț T WITH COMMA BELOW, LATIN SMALL LETTER'),
    
    'thorn': GD(g2='b', g1='o', l='b', r='p', uni=0x00fe, c='þ', name='thorn', isLower=True, src='p', comment='þ THORN, LATIN SMALL LETTER'),
    'tilde': GD(g2='tilde', g1='tilde', l=CENTER, w=ACCENT_WIDTH, uni=0x02dc, c='˜', base='tildecmb', name='tilde', anchors=[]),
    'trademark': GD(g2='trademark', g1='trademark', l='T.sc', r='M.sc', uni=0x2122, c='™', name='trademark', comment='™ TRADE MARK SIGN'),
    
    'u': GD(g2='u', g1='u', r2l='n', l2r='u', uni=0x0075, c='u', name='u', isLower=True, comment='u', copyFromDisplayRight=False, copyFromDisplayLeft=False),
    'u.cbr': GD(g2='u', g1='u', l='u', name='u.cbr', isLower=True, template='u', base='u', comment='connector bottom, just italic, roman contains placeholder for compatibility'),
    'uacute': GD(g2='u', g1='u', l='u', w='u', uni=0x00fa, c='ú', name='uacute', isLower=True, base='u', accents=['acutecmb'], comment='ú U WITH ACUTE, LATIN SMALL LETTER'),
    'ubreve': GD(g2='u', g1='u', l='u', w='u', uni=0x016d, c='ŭ', name='ubreve', isLower=True, base='u', accents=['brevecmb'], comment='ŭ U WITH BREVE, LATIN SMALL LETTER'),
    'ucircumflex': GD(g2='u', g1='u', l='u', w='u', uni=0x00fb, c='û', name='ucircumflex', isLower=True, base='u', accents=['circumflexcmb'], comment='û U WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'udieresis': GD(g2='u', g1='u', l='u', w='u', uni=0x00fc, c='ü', name='udieresis', isLower=True, base='u', accents=['dieresiscmb'], comment='ü U WITH DIAERESIS, LATIN SMALL LETTER'),
    'ugrave': GD(g2='u', g1='u', l='u', w='u', uni=0x00f9, c='ù', name='ugrave', isLower=True, base='u', accents=['gravecmb'], comment='ù U WITH GRAVE, LATIN SMALL LETTER'),
    'uhungarumlaut': GD(g2='u', g1='u', l='u', w='u', uni=0x0171, c='ű', name='uhungarumlaut', isLower=True, base='u', accents=['hungarumlautcmb'], comment='ű U WITH DOUBLE ACUTE, LATIN SMALL LETTER'),
    'umacron': GD(g2='u', g1='u', l='u', w='u', uni=0x016b, c='ū', name='umacron', isLower=True, base='u', accents=['macroncmb'], comment='ū U WITH MACRON, LATIN SMALL LETTER'),
    'uogonek': GD(g2='u', g1='u', l='u', w='u', uni=0x0173, c='ų', name='uogonek', isLower=True, base='u', accents=['ogonekcmb'], anchors=ALL_IJ_ANCHORS, comment='ų U WITH OGONEK, LATIN SMALL LETTER'),
    'uring': GD(g2='u', g1='u', l='u', w='u', uni=0x016f, c='ů', name='uring', isLower=True, base='u', accents=['ringcmb'], comment='ů U WITH RING ABOVE, LATIN SMALL LETTER'),
    'utilde': GD(g2='u', g1='u', l='u', w='u', uni=0x0169, c='ũ', name='utilde', isLower=True, base='u', accents=['tildecmb'], comment='ũ U WITH TILDE, LATIN SMALL LETTER'),

    'v': GD(g2='v', g1='v', l2r='v', uni=0x0076, c='v', name='v', isLower=True, comment='v LATIN SMALL LETTER V'),

    'w': GD(g2='v', g1='v', l='v', r='v', uni=0x0077, c='w', name='w', isLower=True, comment='w LATIN SMALL LETTER W'),
    'wacute': GD(g2='v', g1='v', l='w', w='w', uni=0x1e83, c='ẃ', name='wacute',isLower=True,  base='w', accents=['acutecmb'], comment='ẃ W WITH ACUTE, LATIN SMALL LETTER'),
    'wcircumflex': GD(g2='v', g1='v', l='w', w='w', uni=0x0175, c='ŵ', name='wcircumflex', isLower=True, base='w', accents=['circumflexcmb'], comment='ŵ W WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'wdieresis': GD(g2='v', g1='v', l='w', w='w', uni=0x1e85, c='ẅ', name='wdieresis', isLower=True, base='w', accents=['dieresiscmb'], comment='ẅ W WITH DIAERESIS, LATIN SMALL LETTER'),
    'wgrave': GD(g2='v', g1='v', l='w', w='w', uni=0x1e81, c='ẁ', name='wgrave', isLower=True, base='w', accents=['gravecmb'], comment='ẁ W WITH GRAVE, LATIN SMALL LETTER'),

    'x': GD(g2='x', g1='x', r2l='k', r='k', uni=0x0078, c='x', name='x', isLower=True, comment='x LATIN SMALL LETTER X'),
    'x.cbr': GD(g2='x', g1='x', l='x', w='x', name='x.cbr', template='x', base='x', isLower=True, comment='connector bottom, just italic, roman contains placeholder for compatibility'),

    'y': GD(g2='y', g1='v', uni=0x0079, c='y', name='y', isLower=True, comment='y LATIN SMALL LETTER Y'), # Manually fit to /v
    'yacute': GD(g2='y', g1='v', l='y', w='y', uni=0x00fd, c='ý', name='yacute', isLower=True, base='y', accents=['acutecmb'], comment='ý Y WITH ACUTE, LATIN SMALL LETTER'),
    'ycircumflex': GD(g2='y', g1='v', l='y', w='y', uni=0x0177, c='ŷ', name='ycircumflex', isLower=True, base='y', accents=['circumflexcmb'], comment='ŷ Y WITH CIRCUMFLEX, LATIN SMALL LETTER'),
    'ydieresis': GD(g2='y', g1='v', l='y', w='y', uni=0x00ff, c='ÿ', name='ydieresis', isLower=True, base='y', accents=['dieresiscmb'], comment='ÿ Y WITH DIAERESIS, LATIN SMALL LETTER'),
    'ygrave': GD(g2='y', g1='v', l='y', w='y', uni=0x1ef3, c='ỳ', name='ygrave', isLower=True, base='y', accents=['gravecmb'], comment='ỳ Y WITH GRAVE, LATIN SMALL LETTER'),

    'yen': GD(g2='Y', g1='Y', l='Y', r='Y', uni=0x00a5, c='¥', base='Y', name='yen', comment='¥ yuan sign'),
    'yen.tab': GD(l=CENTER, w=TAB, name='yen.tab', src='yen', comment='¥ yuan sign TAB'),

    'z': GD(g2='z', g1='z', l2r='z', uni=0x007a, c='z', name='z', isLower=True, comment='z LATIN SMALL LETTER Z'),
    'zacute': GD(g2='z', g1='z', l='z', w='z', uni=0x017a, c='ź', name='zacute', isLower=True, base='z', accents=['acutecmb'], comment='ź Z WITH ACUTE, LATIN SMALL LETTER'),
    'zcaron': GD(g2='z', g1='z', l='z', w='z', uni=0x017e, c='ž', name='zcaron', isLower=True, base='z', accents=['caroncmb'], comment='ž Z WITH CARON, LATIN SMALL LETTER'),
    'zdotaccent': GD(g2='z', g1='z', l='z', w='z', uni=0x017c, c='ż', name='zdotaccent', isLower=True, base='z', accents=['dotaccentcmb'], comment='ż Z WITH DOT ABOVE, LATIN SMALL LETTER'),

    'acutecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0301, c='́', name='acutecmb', anchors=[_TOP]),
    'brevecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x306, c='̆', name='brevecmb', anchors=[]),
    'caroncmb': GD(g2='cmb', g1='cmb', w=0, uni=0x030c, c='̌', name='caroncmb', src180='circumflexcmb', anchors=[]),
    'caroncmb.vert': GD(g2='cmb', g1='cmb', l='commabelowcmb', w=0, name='caroncmb.vert', src='commabelowcmb', anchors=[_VERT]),
    'cedillacmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0327, name='cedillacmb', anchors=[]),
    'circumflexcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0302, name='circumflexcmb', anchors=[]),
    'commabelowcmb': GD(g2='cmb', g1='cmb', l=CENTER, w=0, uni=0x0326, name='commabelowcmb', src='comma', anchors=[]),
    'commaturnedabovecmb': GD(g2='cmb', g1='cmb', l=CENTER,w=0, uni=0x0312, c='̒', src='commabelowcmb', name='commaturnedabovecmb', anchors=[_TOP]),
    'dieresiscmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0308, name='dieresiscmb', anchors=[]),
    'dotaccentcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0307, name='dotaccentcmb', anchors=[]),
    'dotmiddlecmb': GD(g2='cmb', g1='cmb', l=CENTER, w=0, src='dotaccentcmb', name='dotmiddlecmb', anchors=(_MIDDLE,)),
    'gravecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0300, c='̀', name='gravecmb', anchors=[_TOP]),
    'hungarumlautcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x030B, name='hungarumlautcmb', anchors=[]),
    'macroncmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0304, c='̄', name='macroncmb', anchors=[]),
    'ogonekcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0328, c='̨', name='ogonekcmb', anchors=[]),
    'eogonekcmb': GD(g2='cmb', g1='cmb', w=0, name='eogonekcmb', src='ogonekcmb', anchors=[]),
    'ringacutecmb': GD(g2='cmb', g1='cmb', w=0, name='ringacutecmb', src=['ringcmb.uc', 'acutecmb.uc'], anchors=[]),
    'ringcmb': GD(g2='cmb', g1='cmb', w=0, l=CENTER, uni=0x030A, name='ringcmb', useSkewRotate=True, addItalicExtremePoints=True, anchors=[]),
    'tildecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0303,  name='tildecmb', anchors=[]),

    'acutecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='acutecmb.uc', src='acutecmb', anchors=[]),
    'brevecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='brevecmb.uc', src='brevecmb', anchors=[]),
    'caroncmb.uc': GD(g2='cmb', g1='cmb', w=0, name='caroncmb.uc', src180='circumflexcmb.uc', anchors=[]),
    'circumflexcmb.uc': GD(g2='cmb', g1='cmb', w=0, name='circumflexcmb.uc', src='circumflexcmb', anchors=[]),
    'commaturnedabovecmb.uc': GD(g2='cmb', g1='cmb', l=CENTER, w=0, name='commaturnedabovecmb.uc', src='commabelowcmb', anchors=[_TOP]),
    'dieresiscmb.uc': GD(g2='cmb', g1='cmb', w=0, name='dieresiscmb.uc', src='dieresiscmb', anchors=[]),
    'dotaccentcmb.uc': GD(g2='cmb', g1='cmb', w=0, name='dotaccentcmb.uc', src='dotaccentcmb', anchors=[]),
    'gravecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='gravecmb.uc', src='gravecmb', anchors=[]),
    'hungarumlautcmb.uc': GD(g2='cmb', g1='cmb', w=0, name='hungarumlautcmb.uc', src='hungarumlautcmb', anchors=[]),
    'macroncmb.uc': GD(g2='cmb', g1='cmb', w=0, name='macroncmb.uc', src='macroncmb', anchors=[]),
    'ringacutecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='ringacutecmb.uc', src=['ringcmb.uc', 'acutecmb.uc'], anchors=[]),
    'ringcmb.uc': GD(g2='cmb', g1='cmb', w=0, name='ringcmb.uc', src='ringcmb', useSkewRotate=True, addItalicExtremePoints=True, anchors=[]),
    'tildecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='tildecmb.uc', src='tildecmb', anchors=[]),

    'Euro': GD(g1='C', g2='Euro', r='C', uni=0x20AC, c='€', base='C', src=['hyphen', 'hyphen'], name='Euro'),
    'Euro.sc': GD(g1='C.sc', g2='Euro.sc', r='C.sc', base='C.sc', src=['hyphen', 'hyphen'], name='Euro.sc'),
    'Euro.tab': GD(g2='Euro.tab', g1='Euro.tab', l=CENTER, w=TAB, name='Euro.tab', src='Euro'), # Needs to be scaled
    'Euro.tab.sc': GD(g2='Euro.tab.sc', g1='Euro.tab.sc', l=CENTER, w=TAB, name='Euro.tab.sc', base='Euro.sc'),
    'apple': GD(g2='largecircle', g1='largecircle', l='largecircle', r='largecircle', uni=0xf8ff, c='', name='apple', src='paragraph', base='largecircle', comment='TYPETR Logo'),
    'checkmark': GD(g2='v', g1='V', l='v', r='V', uni=0x2713, c='✓', src='y', anchors=[], name='checkmark'),
    'uni00A0': GD(g1='space', g2='space', w=200, uni=0x00a0, name='uni00A0', anchors=[]),
    'copyrightsound': GD(g2='copyright', g1='copyright', l='copyright', r='copyright', uni=0x2117, base='largecircle', name='copyrightsound'),
    'bitcoin': GD(g2='B', g1='H', l='B', r='B', uni=0x20bf, c='₿', name='bitcoin', base='B', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT),
    'bitcoin.tab': GD(g2='bitcoin.tab', g1='bitcoin.tab', l=CENTER, w=TAB, name='bitcoin.tab', src='bitcoin', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT),

    # In combination with smallcaps
    'dollar.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', r='S.sc', base='S.sc', name='dollar.sc'),
    'sterling.sc': GD(l='sterling', r='sterling', src='sterling', name='sterling.sc'),
    'yen.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', r='Y.sc', base='Y.sc', name='yen.sc'),
    'section.sc': GD(l='section', r='section', src='section', name='section.sc'),
    'paragraph.sc': GD(g2='bar', g1='T.sc', l='paragraph', r='paragraph',src='paragraph', name='paragraph.sc'),

    # Directly link to .sups (instead of .numr/.dnom), to avoid nested component links
    'onehalf': GD(g2='one.sups', g1='two.dnom', ml='one.sups', mr='two.sups', uni=0x00BD, c='½', name='onehalf', base='one.numr', accents=['fraction', 'two.dnom'], comment='½ VULGAR FRACTION ONE HALF', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'onequarter': GD(g2='one.sups', g1='four.dnom', ml='one.sups', mr='four.sups', uni=0x00BC, c='¼', name='onequarter', base='one.numr', accents=['fraction', 'four.dnom'], comment='¼ VULGAR FRACTION ONE QUARTER', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'threequarters': GD(g2='three.sups', g1='four.dnom', ml='three.sups', mr='four.sups', uni=0x00BE, c='¾', name='threequarters', base='three.numr', accents=['fraction', 'four.dnom'], comment='¾ VULGAR FRACTION THREE QUARTERS', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'percent': GD(g2='zero.sups', g1='zero.dnom', ml='zero.sups', mr='zero.sups', uni=0x0025, c='%', base='zero.numr', accents=['fraction', 'zero.dnom'], name='percent', comment='% PERCENT SIGN', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'percent.sc': GD(g2='zero.sups', g1='zero.dnom', ml='zero.sups', mr='zero.sups', name='percent.sc', base='zero.numr', accents=['slash.sc', 'zero.dnom']),
    'perthousand': GD(g2='zero.sups', g1='zero.dnom', ml='zero.sups', mr='zero.sups', uni=0x2030, c='‰', name='perthousand', base='zero.numr', accents=['fraction', 'zero.dnom', 'zero.dnom'], comment='‰ per thousand', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'perthousand.sc': GD(g2='zero.sups', g1='zero.dnom', ml='zero.sups', mr='zero.sups', name='perthousand.sc', base='zero.numr', accents=['slash.sc', 'zero.dnom', 'zero.dnom']),

    'zero': GD(g2='zero', g1='zero', l2r='zero', uni=0x0030, c='0', name='zero', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
    'zeroslash': GD(g2='zero', g1='zero', l='zero', w='zero', name='zeroslash', base='zero', src='slash', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='0 Digits, ASCII'),
    'one': GD(g2='one', g1='one', l2r='one', uni=0x0031, c='1', name='one', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='1'),
    'two': GD(g2='two', g1='two', l2r='two', uni=0x0032, c='2', name='two', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='2'),
    'two.alt1': GD(g2='two', g1='two', l='two', r='two', name='two.alt1', src='two', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='2 alternative'),
    'three': GD(g2='three', g1='three', l2r='three', uni=0x0033, c='3', name='three', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='3'),
    'four': GD(g2='four', g1='four', uni=0x0034, c='4', name='four', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='4'),
    'five': GD(g2='five', g1='five', l2r='five', uni=0x0035, c='5', name='five', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='5'),
    'five.alt1': GD(g2='five', g1='five', l='five', r='five', name='five.alt1', src='five', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='5 alternative'),
    'six': GD(g2='six', g1='six',  l2r='six', uni=0x0036, c='6', name='six', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='6'),
    'seven': GD(g2='seven', g1='seven', uni=0x0037, c='7', name='seven', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='7'),
    'seven.alt1': GD(g2='seven', g1='seven', l='seven', r='seven', name='seven.alt1', src='seven', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='7 alternative'),
    'eight': GD(g2='eight', g1='eight', l2r='eight', uni=0x0038, c='8', name='eight', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='8'),
    'nine': GD(g2='nine', g1='nine', l2r='six', r2l='six', uni=0x0039, c='9', name='nine', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='9'),

    # Old style figures
    'zero.onum': GD(g2='zero.onum', g1='zero.onum', l2r='zero.onum', src='o', name='zero.onum', comment='0 Digits, ASCII Old style', useSkewRotate=True, addItalicExtremePoints=True),
    'zeroslash.onum': GD(g2='zero.onum', g1='zero.onum', l='zero.onum', w='zero.onum', base='zero.onum', src='slash', name='zeroslash.onum', comment='0 Digits, ASCII Old style', useSkewRotate=True, addItalicExtremePoints=True),
    'one.onum': GD(g2='one.onum', g1='one.onum', l2r='one.onum', src='idotless', name='one.onum', comment='1 Old style'),
    'two.onum': GD(g2='two.onum', g1='two.onum', l2r='two.onum', name='two.onum', src='two.sc', comment='2 Old style'), # Similar to two.sc small cap with smaller x-height
    'two.onum.alt1': GD(g2='two.onum', g1='two.onum', l='two.onum', r='two.onum', name='two.onum.alt1', src='two.alt1', comment='2 alternative'),
    'three.onum': GD(g2='three.onum', g1='three.onum', l='three', w='three', name='three.onum', base='three', comment='3 Old style'),
    'four.onum': GD(g2='four.onum', g1='four.onum', l2r='four.onum', name='four.onum', src='four', comment='4 Old style'),
    'five.onum': GD(g2='five.onum', g1='five.onum', l='five', w='five', name='five.onum', base='five', comment='5 Old style'),
    'five.onum.alt1': GD(g2='five.onum', g1='five.onum', l='five.onum', r='five.onum', name='five.onum.alt1', base='five.alt1', comment='5 alternative'),
    'six.onum': GD(g2='six.onum', g1='six.onum', l='six', w='six', name='six.onum', base='six', comment='6 Old style'),
    'seven.onum': GD(g2='seven.onum', g1='seven.onum', l='seven', w='seven', name='seven.onum', base='seven', comment='7 Old style'),
    'seven.onum.alt1': GD(g2='seven.onum', g1='seven.onum', l='seven.onum', r='seven.onum', name='seven.onum.alt1', base='seven.alt1', comment='7 alternative'),
    'eight.onum': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.onum', base='eight', comment='8 Old style'), # Still ascender, can be in the same group as /eight
    'nine.onum': GD(g2='nine.onum', g1='nine.onum', l='nine', w='nine', name='nine.onum', base='nine', comment='9 Old style'),

    'zero.sc': GD(l='o', r='o', src='o', name='zero.sc', comment='0 Digits, ASCII Smallcaps', useSkewRotate=True, addItalicExtremePoints=True, 
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'zeroslash.sc': GD(l='zero.sc', w='zero.sc', base='zero.sc', name='zeroslash.sc', src='slash', comment='0 Digits, ASCII Smallcaps', 
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'one.sc': GD(l='one', l2r='one', src='idotless', name='one.sc', comment='1 Smallcaps',
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'two.sc': GD(l='two', r='two', name='two.sc', src='two', comment='2 Smallcaps', addItalicExtremePoints=True,
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'two.sc.alt1': GD(g2='two.sc', g1='two.sc', l='two.sc', r='two.sc', name='two.sc.alt1', src='two.alt1', comment='2 alternative', addItalicExtremePoints=True,
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'three.sc': GD(l='three', r='three', name='three.sc', src='three', comment='3 Smallcaps', addItalicExtremePoints=True,
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'four.sc': GD(l='four', r='four', name='four.sc', src='four', comment='4 Smallcaps',
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'five.sc': GD(l='five', r='five', name='five.sc', src='five', comment='5 Smallcaps',
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'five.sc.alt1': GD(g2='five.sc', g1='five.sc', l='five.sc', r='five.sc', name='five.sc.alt1', src='five.alt1', comment='5 alternative',
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'six.sc': GD(l='six', r='six', name='six.sc', src='six', comment='6 Smallcapse',  addItalicExtremePoints=True,
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'seven.sc': GD(l='seven', r='seven', name='seven.sc', src='seven', comment='7 Smallcaps',
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'seven.sc.alt1': GD(g2='seven.sc', g1='seven.sc', l='seven.sc', r='seven.sc', name='seven.sc.alt1', src='seven.alt1', comment='5 alternative',
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'eight.sc': GD(l='eight', r='eight', name='eight.sc', src='eight', comment='8 Smallcaps', addItalicExtremePoints=True,
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),
    'nine.sc': GD(l='nine', r='nine', name='nine.sc', src='nine', comment='9 Smallcaps', addItalicExtremePoints=True,
        height=SC_HEIGHT, overshoot=SC_OVERSHOOT),

    'zero.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, src='zero', name='zero.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='0 Digits, ASCII TAB', useSkewRotate=True, addItalicExtremePoints=True), # Make as outline, because Black needs to be condensed.
    'zeroslash.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, base='zero.tab', src='slash', name='zeroslash.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='0 Digits, ASCII TAB slash'), 
    'one.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, base='one', name='one.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='1 TAB'),
    'two.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, base='two', name='two.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='2 TAB'),
    'three.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, base='three', name='three.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='3 TAB'),
    'four.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, src='four', name='four.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='4 TAB'),
    'five.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, base='five', name='five.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='5 TAB'),
    'six.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, src='six', name='six.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='6 TAB'),
    'seven.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, base='seven', name='seven.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='7 TAB'),
    'eight.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, src='eight', name='eight.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='8 TAB'),
    'nine.tab': GD(g2='tab', g1='tab', l=CENTER, w=TAB, src='nine', name='nine.tab', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='9 TAB'),

    'zero.sups': GD(g2='zero.sups', g1='zero.sups', l2r='zero.sups', uni=0x2070, c='⁰', name='zero.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT, useSkewRotate=True, addItalicExtremePoints=True),
    'onesuperior': GD(g2='one.sups', g1='one.sups', l='one.sups', r='one.sups', uni=0x00b9, c='¹', name='onesuperior', base='one.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'one.sups': GD(g2='one.sups', g1='one.sups', l2r='one.sups', name='one.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'twosuperior': GD(g2='two.sups', g1='two.sups', l='two.sups', r='two.sups', uni=0x00b2, c='²', name='twosuperior', base='two.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'two.sups': GD(g2='two.sups', g1='two.sups', l2r='two.sups', name='two.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'threesuperior': GD(g2='sups', g1='sups', l='three.sups', r='three.sups', uni=0x00b3, c='³', name='threesuperior', base='three.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'three.sups': GD(g2='sups', g1='sups', l2r='three.sups', name='three.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT, addItalicExtremePoints=True),
    'four.sups': GD(g2='four.sups', g1='four.sups', uni=0x2074, c='⁴', name='four.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'five.sups': GD(g2='sups', g1='sups', l2r='five.sups', uni=0x2075, c='⁵', name='five.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'six.sups': GD(g2='sups', g1='sups', l2r='six.sups', uni=0x2076, c='⁶', name='six.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT, addItalicExtremePoints=True),
    'seven.sups': GD(g2='seven.sups', g1='seven.sups', l2r='seven.sups', uni=0x2077, c='⁷', name='seven.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'eight.sups': GD(g2='sups', g1='sups', l2r='eight.sups', uni=0x2078, c='⁸', name='eight.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT, addItalicExtremePoints=True),
    'nine.sups': GD(g2='sups', g1='sups', l2r='six.sups', r2l='six.sups', uni=0x2079, c='⁹', name='nine.sups', baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT, addItalicExtremePoints=True),
    'period.sups': GD(g2='period.sups', g1='period.sups', l='period', r='period', name='period.sups', src='dotaccentcmb', anchors=[], baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'comma.sups': GD(g2='period.sups', g1='period.sups', l='comma', r='comma', name='comma.sups', src='comma', anchors=[], baseline=SUPS_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),

    'zero.dnom': GD(g2='zero.dnom', g1='zero.dnom', l='zero.sups', w='zero.sups', name='zero.dnom', base='zero.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'one.dnom': GD(g2='one.dnom', g1='one.dnom', l='one.sups', w='one.sups', name='one.dnom', base='one.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'two.dnom': GD(g2='two.dnom', g1='two.dnom', l='two.sups', w='two.sups', name='two.dnom', base='two.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'three.dnom': GD(g2='dnom', g1='dnom', l='three.sups', w='three.sups', name='three.dnom', base='three.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'four.dnom': GD(g2='four.dnom', g1='four.dnom', l='four.sups', w='four.sups', name='four.dnom', base='four.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'five.dnom': GD(g2='dnom', g1='dnom', l='five.sups', w='five.sups', name='five.dnom', base='five.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'six.dnom': GD(g2='dnom', g1='dnom', l='six.sups', w='six.sups', name='six.dnom', base='six.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'seven.dnom': GD(g2='seven.dnom', g1='seven.dnom', l='seven.sups', w='seven.sups', name='seven.dnom', base='seven.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'eight.dnom': GD(g2='dnom', g1='dnom', l='eight.sups', w='eight.sups', name='eight.dnom', base='eight.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'nine.dnom': GD(g2='dnom', g1='dnom', l='nine.sups', w='nine.sups', name='nine.dnom', base='nine.sups', baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'period.dnom': GD(g2='period.dnom', g1='period.dnom', l='period', r='period', name='period.dnom', base='period.sups', anchors=[], baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'comma.dnom': GD(g2='period.dnom', g1='period.dnom', l='comma', r='comma', name='comma.dnom', base='comma.sups', anchors=[], baseline=DNOM_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),

    'zero.numr': GD(g2='zero.numr', g1='zero.numr', l='zero.sups', w='zero.sups', name='zero.numr', base='zero.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'one.numr': GD(g2='one.numr', g1='one.numr', l='one.sups', w='one.sups', name='one.numr', base='one.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'two.numr': GD(g2='two.numr', g1='two.numr', l='two.sups', w='two.sups', name='two.numr', base='two.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'three.numr': GD(g2='numr', g1='numr', l='three.sups', w='three.sups', name='three.numr', base='three.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'four.numr': GD(g2='four.numr', g1='four.numr', l='four.sups', w='four.sups', name='four.numr', base='four.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'five.numr': GD(g2='numr', g1='numr', l='five.sups', w='five.sups', name='five.numr', base='five.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'six.numr': GD(g2='numr', g1='numr', l='six.sups', w='six.sups', name='six.numr', base='six.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'seven.numr': GD(g2='seven.numr', g1='seven.numr', l='seven.sups', w='seven.sups', name='seven.numr', base='seven.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'eight.numr': GD(g2='numr', g1='numr', l='eight.sups', w='eight.sups', name='eight.numr', base='eight.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'nine.numr': GD(g2='numr', g1='numr', l='nine.sups', w='nine.sups', name='nine.numr', base='nine.sups', baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'period.numr': GD(g2='period.numr', g1='period.numr', l='period', r='period', name='period.numr', base='period.sups', anchors=[], baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'comma.numr': GD(g2='period.numr', g1='period.numr', l='comma', r='comma', name='comma.numr', base='comma.sups', anchors=[], baseline=NUMR_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),

    'zero.sinf': GD(g2='zero.sinf', g1='zero.sinf', l='zero.sups', w='zero.sups', uni=0x2080, c='₀', name='zero.sinf', base='zero.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'one.sinf': GD(g2='one.sinf', g1='one.sinf', l='one.sups', w='one.sups', uni=0x2081, c='₁', name='one.sinf', base='one.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'two.sinf': GD(g2='two.sinf', g1='two.sinf', l='two.sups', w='two.sups', uni=0x2082, c='₂', name='two.sinf', base='two.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'three.sinf': GD(g2='sinf', g1='sinf', l='three.sups', w='three.sups', uni=0x2083, c='₃', name='three.sinf', base='three.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'four.sinf': GD(g2='four.sinf', g1='four.sinf', l='four.sups', w='four.sups', uni=0x2084, c='₄', name='four.sinf', base='four.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'five.sinf': GD(g2='sinf', g1='sinf', l='five.sups', w='five.sups', uni=0x2085, c='₅', name='five.sinf', base='five.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'six.sinf': GD(g2='sinf', g1='sinf', l='six.sups', w='six.sups', uni=0x2086, c='₆', name='six.sinf', base='six.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'seven.sinf': GD(g2='seven.sinf', g1='seven.sinf', l='seven.sups', w='seven.sups', uni=0x2087, c='₇', name='seven.sinf', base='seven.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'eight.sinf': GD(g2='sinf', g1='sinf', l='eight.sups', w='eight.sups', uni=0x2088, c='₈', name='eight.sinf', base='eight.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'nine.sinf': GD(g2='sinf', g1='sinf', l='nine.sups', w='nine.sups', uni=0x2089, c='₉', name='nine.sinf', base='nine.sups', baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'period.sinf': GD(g2='period.sinf', g1='period.sinf', l='period', r='period', name='period.numr', base='period.sups', anchors=[], baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),
    'comma.sinf': GD(g2='period.sinf', g1='period.sinf', l='comma', r='comma', name='comma.numr', base='comma.sups', anchors=[], baseline=SINF_BASELINE, height=DNOM_HEIGHT, overshoot=DNOM_OVERSHOOT),

    # Flourishes

    # Increasing complexity and size for Right

    'flourish.topRightUp1': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp1', src='flourish.topRightUp2', comment='Complex top right upwards', anchors=(_TOPRIGHT,)),
    'flourish.topRightUp1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp1s', src='flourish.topRightUp1', comment='Complex top right upwards small', anchors=(_TOPRIGHT,)),
    'flourish.topRightUp1x': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp1x', base='flourish.topRightUp1', comment='Complex top right upwards small', anchors=(_TOPRIGHT,)),
    'flourish.topRightUp2': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp2', comment='Complex top right upwards', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightUp2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp2s', src='flourish.topRightUp2', comment='Complex top right upwards small', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightUp2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp2sl', src='flourish.topRightDown2sl', comment='Complex top right upwards small', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightUp2x': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp2x', src='flourish.topRightUp2', comment='Complex top right upwards small with horizontal offset', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightUp2xs': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp2xs', base='flourish.topRightUp2x', comment='Complex top right upwards small with small horizontal offset', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightUp3': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp3', src='flourish.topRightUp2', comment='Complex top right upwards', anchors=(_TOPRIGHT,)),
    'flourish.topRightUp4': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp4', src='flourish.topRightUp2', comment='Complex top right upwards', anchors=(_TOPRIGHT,)),
    'flourish.topRightUp5': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightUp5', src='flourish.topRightUp2', comment='Complex top right upwards', anchors=(_TOPRIGHT,)),

    'flourish.topRightDown1': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown1', src='flourish.topRightDown2', comment='Complex top right downward', anchors=(_TOPRIGHT,)),
    'flourish.topRightDown1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown1s', src='flourish.topRightDown1', comment='Complex top right downward small', anchors=(_TOPRIGHT,)),
    'flourish.topRightDown2': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown2', comment='Complex top right downward', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightDown2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown2s', src='flourish.topRightDown2', comment='Complex top right downward small', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightDown2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown2sl', src='flourish.topRightDown2s', comment='Complex top right downward small', anchors=(_TOPRIGHT,)), # Default
    'flourish.topRightDown3': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown3', src='flourish.topRightDown2', comment='Complex top right downward', anchors=(_TOPRIGHT,)),
    'flourish.topRightDown4': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown4', src='flourish.topRightDown2', comment='Complex top right downward', anchors=(_TOPRIGHT,)),
    'flourish.topRightDown5': GD(g2='flourish', g1='flourish', w=0, name='flourish.topRightDown5', src='flourish.topRightDown2', comment='Complex top right downward', anchors=(_TOPRIGHT,)),

    'flourish.bottomRightUp1': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp1', src='flourish.bottomRightUp2', comment='Complex bottom right upwards', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightUp1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp1s', src='flourish.bottomRightUp1', comment='Complex bottom right upwards small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightUp2': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp2', comment='Complex bottom right upwards', anchors=(_BOTTOMRIGHT,)), # Default
    'flourish.bottomRightUp2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp2s', src='flourish.bottomRightUp2', comment='Complex bottom right upwards small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightUp2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp2sl', src='flourish.bottomRightUp2s', comment='Complex bottom right upwards small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightUp3': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp3', src='flourish.bottomRightUp2', comment='Complex bottom right upwards', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightUp4': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp4', src='flourish.bottomRightUp2', comment='Complex bottom right upwards', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightUp5': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightUp5', src='flourish.bottomRightUp2', comment='Complex bottom right upwards', anchors=(_BOTTOMRIGHT,)),

    'flourish.bottomRightDown1': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown1', src='flourish.bottomRightDown2', comment='Complex bottom right downward', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown1s', src='flourish.bottomRightDown1', comment='Complex bottom right downward small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown1x': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown1x', base='flourish.bottomRightDown1', comment='Complex bottom right downward small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown2': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown2', comment='Complex bottom right downward', anchors=(_BOTTOMRIGHT,)), # Default
    'flourish.bottomRightDown2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown2s', src='flourish.bottomRightDown2', comment='Complex bottom right downward small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown2sl', src='flourish.bottomRightUp2sl', comment='Complex bottom right downward small', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown2x': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown2x', src='flourish.bottomRightDown2', comment='Complex bottom right downward small with horizontal offset', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown2xs': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown2xs', base='flourish.bottomRightDown2x', comment='Complex bottom right downward small with small horizontal offset', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown3': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown3', src='flourish.bottomRightDown2', comment='Complex bottom right downward', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown4': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown4', src='flourish.bottomRightDown2', comment='Complex bottom right downward', anchors=(_BOTTOMRIGHT,)),
    'flourish.bottomRightDown5': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomRightDown5', src='flourish.bottomRightDown2', comment='Complex bottom right downward', anchors=(_BOTTOMRIGHT,)),

    # Increasing complexity and size for Left

    'flourish.topLeftUp1': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp1', src='flourish.topLeftUp2', comment='Complex top left upwards', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp1s', src='flourish.topLeftUp1', comment='Complex top left upwards small', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp1x': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp1x', base='flourish.topLeftUp1', comment='Complex top left upwards small', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp2': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp2', comment='Complex top left upwards', anchors=(_TOPLEFT,)), # Default
    'flourish.topLeftUp2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp2s', src='flourish.topLeftUp2', comment='Complex top left upwards small', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp2sl', src='flourish.topLeftDown2sl', comment='Complex top left upwards small', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp2x': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp2x', src='flourish.topLeftUp2', comment='Complex top left upwards small with horizontal offset', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp2xs': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp2xs', base='flourish.topLeftUp2x', comment='Complex top left upwards small with small horizontal offset', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp3': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp3', src='flourish.topLeftUp2', comment='Complex top left upwards', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp4': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp4', src='flourish.topLeftUp2', comment='Complex top left upwards', anchors=(_TOPLEFT,)),
    'flourish.topLeftUp5': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftUp5', src='flourish.topLeftUp2', comment='Complex top left upwards', anchors=(_TOPLEFT,)),

    'flourish.topLeftDown1': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown1', src='flourish.topLeftDown2', comment='Complex top left downward', anchors=(_TOPLEFT,)),
    'flourish.topLeftDown1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown1s', src='flourish.topLeftDown1', comment='Complex top left downward small', anchors=(_TOPLEFT,)),
    'flourish.topLeftDown2': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown2', comment='Complex top left downward', anchors=(_TOPLEFT,)), # Default
    'flourish.topLeftDown2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown2s', src='flourish.topLeftDown2', comment='Complex top left downward small', anchors=(_TOPLEFT,)),
    'flourish.topLeftDown2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown2sl', src='flourish.topLeftDown2s', comment='Complex top left downward small', anchors=(_TOPLEFT,)),
    'flourish.topLeftDown3': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown3', src='flourish.topLeftDown2', comment='Complex top left downward', anchors=(_TOPLEFT,)),
    'flourish.topLeftDown4': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown4', src='flourish.topLeftDown2', comment='Complex top left downward', anchors=(_TOPLEFT,)),
    'flourish.topLeftDown5': GD(g2='flourish', g1='flourish', w=0, name='flourish.topLeftDown5', src='flourish.topLeftDown2', comment='Complex top left downward', anchors=(_TOPLEFT,)),

    'flourish.bottomLeftUp1': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp1', src='flourish.bottomLeftUp2', comment='Complex bottom left upwards', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftUp1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp1s', src='flourish.bottomLeftUp1', comment='Complex bottom left upwards small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftUp2': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp2', comment='Complex bottom left upwards', anchors=(_BOTTOMLEFT,)), # Default
    'flourish.bottomLeftUp2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp2s', src='flourish.bottomLeftUp2', comment='Complex bottom left upwards small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftUp2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp2s', src='flourish.bottomLeftUp2s', comment='Complex bottom left upwards small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftUp3': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp3', src='flourish.bottomLeftUp2', comment='Complex bottom left upwards', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftUp4': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp4', src='flourish.bottomLeftUp2', comment='Complex bottom left upwards', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftUp5': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftUp5', src='flourish.bottomLeftUp2', comment='Complex bottom left upwards', anchors=(_BOTTOMLEFT,)),

    'flourish.bottomLeftDown1': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown1', src='flourish.bottomLeftDown2', comment='Complex bottom left downward', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown1s', src='flourish.bottomLeftDown1', comment='Complex bottom left downward small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown1x': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown1x', base='flourish.bottomLeftDown1', comment='Complex bottom left downward small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown2': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown2', comment='Complex bottom left downward', anchors=(_BOTTOMLEFT,)), # Default
    'flourish.bottomLeftDown2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown2s', src='flourish.bottomLeftDown2', comment='Complex bottom left downward small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown2sl': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown2sl', src='flourish.bottomLeftUp2sl', comment='Complex bottom left downward small', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown2x': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown2x', src='flourish.bottomLeftDown2', comment='Complex bottom left downward small with horizontal offset', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown2xs': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown2xs', base='flourish.bottomLeftDown2x', comment='Complex bottom left downward small with small horizontal offset', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown3': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown3', src='flourish.bottomLeftDown2', comment='Complex bottom left downward', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown4': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown4', src='flourish.bottomLeftDown2', comment='Complex bottom left downward', anchors=(_BOTTOMLEFT,)),
    'flourish.bottomLeftDown5': GD(g2='flourish', g1='flourish', w=0, name='flourish.bottomLeftDown5', src='flourish.bottomLeftDown2', comment='Complex bottom left downward', anchors=(_BOTTOMLEFT,)),

    # Connect to vertical stems
    # Increasing complexity and size for Right

    'flourish.middleRightUp1': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp1', src='flourish.middleRightUp2', comment='Complex middle right upwards', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp1s', src='flourish.middleRightUp1', comment='Complex middle right upwards small', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp1d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp1d', src='flourish.middleRightUp1', comment='Complex middle right upwards diagonal', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp2': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp2', comment='Complex middle right upwards', anchors=(_MIDDLERIGHT,)), # Default
    'flourish.middleRightUp2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp2s', src='flourish.middleRightUp2', comment='Complex middle right upwards small', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp2d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp2d', src='flourish.middleRightUp2', comment='Complex middle right upwards diagonal', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp3': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp3', src='flourish.middleRightUp2', comment='Complex middle right upwards', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp4': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp4', src='flourish.middleRightUp2', comment='Complex middle right upwards', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp5': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp5', src='flourish.middleRightUp2', comment='Complex middle right upwards', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightUp6': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightUp6', src='flourish.middleRightUp2', comment='Complex middle right upwards', anchors=(_MIDDLERIGHT,)),

    'flourish.middleRightDown1': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown1', src='flourish.middleRightDown2', comment='Complex middle right downward', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown1s', src='flourish.middleRightDown1', comment='Complex middle right downward small', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown1d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown1d', src='flourish.middleRightDown1', comment='Complex middle right downward diagonal', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown2': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown2', comment='Complex middle right downward', anchors=(_MIDDLERIGHT,)), # Default
    'flourish.middleRightDown2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown2s', src='flourish.middleRightDown2', comment='Complex middle right downward small', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown2d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown2d', src='flourish.middleRightDown2', comment='Complex middle right downward diagonal', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown3': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown3', src='flourish.middleRightDown2', comment='Complex middle right downward', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown4': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown4', src='flourish.middleRightDown2', comment='Complex middle right downward', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown5': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown5', src='flourish.middleRightDown2', comment='Complex middle right downward', anchors=(_MIDDLERIGHT,)),
    'flourish.middleRightDown6': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleRightDown5', src='flourish.middleRightDown2', comment='Complex middle right downward', anchors=(_MIDDLERIGHT,)),

    'flourish.middleLeftUp1': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp1', src='flourish.middleLeftUp2', comment='Complex middle left upwards', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp1s', src='flourish.middleLeftUp1', comment='Complex middle left upwards small', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp1d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp1d', src='flourish.middleLeftUp1', comment='Complex middle left upwards diagonal', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp2': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp2', comment='Complex middle left upwards', anchors=(_MIDDLELEFT,)), # Default
    'flourish.middleLeftUp2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp2s', src='flourish.middleLeftUp2', comment='Complex middle left upwards small', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp2d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp2d', src='flourish.middleLeftUp2', comment='Complex middle left upwards diagonal', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp3': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp3', src='flourish.middleLeftUp2', comment='Complex middle left upwards', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp4': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp4', src='flourish.middleLeftUp2', comment='Complex middle left upwards', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp5': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp5', src='flourish.middleLeftUp2', comment='Complex middle left upwards', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftUp6': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftUp6', src='flourish.middleLeftUp2', comment='Complex middle left upwards', anchors=(_MIDDLELEFT,)),

    'flourish.middleLeftDown1': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown1', src='flourish.middleLeftDown2', comment='Complex middle left downward', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown1s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown1s', src='flourish.middleLeftDown1', comment='Complex middle left downward small', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown1d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown1d', src='flourish.middleLeftDown1', comment='Complex middle left downward diagonal', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown2': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown2', src='flourish.middleLeftDown2', comment='Complex middle left downward', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown2s': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown2s', src='flourish.middleLeftDown2', comment='Complex middle left downward small', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown2d': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown2d', src='flourish.middleLeftDown2', comment='Complex middle left downward diagonal', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown3': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown3', src='flourish.middleLeftDown2', comment='Complex middle left downward', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown4': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown4', src='flourish.middleLeftDown2', comment='Complex middle left downward', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown5': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown5', src='flourish.middleLeftDown2', comment='Complex middle left downward', anchors=(_MIDDLELEFT,)),
    'flourish.middleLeftDown6': GD(g2='flourish', g1='flourish', w=0, name='flourish.middleLeftDown6', src='flourish.middleLeftDown2', comment='Complex middle left downward', anchors=(_MIDDLELEFT,)),

    # Terminals, not connected to glyph, spaced by normal kerning groups
    # Increasing complexity and size
    'flourish.openLeft1': GD(g2='hyphen', g1='hyphen', l='o', r=-32, name='flourish.openLeft1', comment='Open middle left terminal'),
    'flourish.openLeft1.uc': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft1.uc', base='flourish.openLeft1', comment='Open middle left terminal for uppercase'),
    'flourish.openLeft2': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft2', src='flourish.openLeft1', comment='Open middle left terminal'), # Default, same as flourish.openLeft2.uc
    'flourish.openLeft2.uc': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft2.uc', base='flourish.openLeft2', comment='Open middle left terminal for uppercase'), # Default, same as flourish.openLeft2.uc
    'flourish.openLeft3': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft3', src='flourish.openLeft1', comment='Open middle left terminal'),
    'flourish.openLeft3.uc': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft3.uc', base='flourish.openLeft3', comment='Open middle left terminal for uppercase'),
    'flourish.openLeft4': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft4', src='flourish.openLeft1', comment='Open middle left terminal'),
    'flourish.openLeft4.uc': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft4.uc', base='flourish.openLeft4', comment='Open middle left terminal for uppercase'),
    'flourish.openLeft5': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft5', src='flourish.openLeft1', comment='Open middle left terminal'),
    'flourish.openLeft5.uc': GD(g2='hyphen', g1='hyphen', l='flourish.openLeft1', r='flourish.openLeft1', name='flourish.openLeft5.uc', base='flourish.openLeft5', comment='Open middle left terminal for uppercase'),

    # Increasing complexity and size
    'flourish.openRight1': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight1', comment='Open middle right terminal'),
    'flourish.openRight1.uc': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight1.uc', base='flourish.openRight1', comment='Open middle right terminal for uppercase'),
    'flourish.openRight2': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight2', src='flourish.openRight1', comment='Open middle right terminal'),
    'flourish.openRight2.uc': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight2.uc', base='flourish.openRight2', comment='Open middle right terminal for uppercase'),
    'flourish.openRight3': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight3', src='flourish.openRight1', comment='Open middle right terminal'),
    'flourish.openRight3.uc': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight3.uc', base='flourish.openRight3', comment='Open middle right terminal for uppercase'),
    'flourish.openRight4': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight4', src='flourish.openRight1', comment='Open middle right terminal'),
    'flourish.openRight4.uc': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight4.uc', base='flourish.openRight4', comment='Open middle right terminal for uppercase'),
    'flourish.openRight5': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight5', src='flourish.openRight1', comment='Open middle right terminal'),
    'flourish.openRight5.uc': GD(g2='hyphen', g1='hyphen', l2r='flourish.openLeft1', r2l='flourish.openLeft1', name='flourish.openRight5.uc', base='flourish.openRight5', comment='Open middle right terminal for uppercase'),

    # Open/bottom flourishes that connect to OPENTOP and OPENBOTTOM anchors, unconnected to the glyph
    # All glyphs get such an anchor, initially centered on the bounding box with a margin.

    # Increasing complexity and size
    'flourish.openTop1': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openTop1', src='flourish.openTop2', comment='Open top upwards', anchors=(_TOP,)),
    'flourish.openTop2': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openTop2', comment='Open top upwards', anchors=(_TOP,)),
    'flourish.openTop3': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openTop3', src='flourish.openTop2', comment='Open top upwards', anchors=(_TOP,)),
    'flourish.openTop4': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openTop4', src='flourish.openTop2', comment='Open top upwards', anchors=(_TOP,)),
    'flourish.openTop5': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openTop5', src='flourish.openTop2', comment='Open top upwards', anchors=(_TOP,)),

    # Increasing complexity and size
    'flourish.openBottom1': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openBottom1', src='flourish.openTop1', comment='Open bottom downwards', anchors=(_BOTTOM,)),
    'flourish.openBottom2': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openBottom2', src='flourish.openTop2', comment='Open bottom downwards', anchors=(_BOTTOM,)),
    'flourish.openBottom3': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openBottom3', src='flourish.openTop3', comment='Open bottom downwards', anchors=(_BOTTOM,)),
    'flourish.openBottom4': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openBottom4', src='flourish.openTop4', comment='Open bottom downwards', anchors=(_BOTTOM,)),
    'flourish.openBottom5': GD(g2='flourish', g1='flourish', w=0, l=CENTER, name='flourish.openBottom5', src='flourish.openTop5', comment='Open bottom downwards', anchors=(_BOTTOM,)),

    # Flourish base glyphs

    'zero.bottomLeftDown': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.bottomLeftDown', base='zero', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish bottom left downward'),
    'zero.bottomRightDown': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.bottomRightDown', base='zero', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish bottom right downward'),
    'zero.topLeftUp': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.topLeftUp', base='zero', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish top left upwards'),
    'zero.topRightUp': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.topRightUp', base='zero', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish top right upwards'),
    # Flourishes on the side
    'zero.middleLeftDown': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.middleLeftDown', base='zero', accents=['flourish.middleLeftDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish middle left downward'),
    'zero.middleLeftUp': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.middleLeftUp', base='zero', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish middle left upwards'),
    'zero.middleRightDown': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.middleRightDown', base='zero', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish middle right downward'),
    'zero.middleRightUp': GD(g2='zero', g1='zero', l='zero', w='zero', name='zero.middleRightUp', base='zero', accents=['flourish.middleRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='zero simple flourish middle right upwards'),

    'one.bottomLeftDown': GD(g2='one', g1='one', l='one', w='one', name='one.bottomLeftDown', base='one', accents=['flourish.bottomLeftDown2x'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish bottom left downward'),
    'one.bottomLeftUp': GD(g2='one', g1='one', l='one', w='one', name='one.bottomLeftUp', base='one', accents=['flourish.bottomLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish bottom left upwards'),
    'one.bottomRightDown': GD(g2='one', g1='one', l='one', w='one', name='one.bottomRightDown', base='one', accents=['flourish.bottomRightDown2x'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish bottom right downward'),
    'one.bottomRightUp': GD(g2='one', g1='one', l='one', w='one', name='one.bottomRightUp', base='one', accents=['flourish.bottomRightUp1'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish bottom right upwards'),
    'one.topRightUp': GD(g2='one', g1='one', l='one', w='one', name='one.topRightUp', base='one', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish top right upwards'),
    # Flourishes on the side
    'one.middleLeftDown': GD(g2='one', g1='one', l='one', w='one', name='one.middleLeftDown', base='one', accents=['flourish.middleLeftDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish middle left downward'),
    'one.middleLeftUp': GD(g2='one', g1='one', l='one', w='one', name='one.middleLeftUp', base='one', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish middle left upwards'),
    'one.middleRightDown': GD(g2='one', g1='one', l='one', w='one', name='one.middleRightDown', base='one', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish middle right downward'),
    'one.middleRightUp': GD(g2='one', g1='one', l='one', w='one', name='one.middleRightUp', base='one', accents=['flourish.middleRightUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='one simple flourish middle right upwards'),

    'two.bottomLeftDown': GD(g2='two', g1='two', l='two', w='two', name='two.bottomLeftDown', base='two', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish bottom left downward'),
    'two.bottomRightDown': GD(g2='two', g1='two', l='two', w='two', name='two.bottomRightDown', base='two', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish bottom right downward'),
    'two.topLeftUp': GD(g2='two', g1='two', l='two', w='two', name='two.topLeftUp', base='two', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish top left upwards'),
    'two.topRightUp': GD(g2='two', g1='two', l='two', w='two', name='two.topRightUp', base='two', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish top right upwards'),
    # Flourishes on the side
    'two.middleLeftDown': GD(g2='two', g1='two', l='two', w='two', name='two.middleLeftDown', base='two', accents=['flourish.middleLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish middle left downward'),
    'two.middleLeftUp': GD(g2='two', g1='two', l='two', w='two', name='two.middleLeftUp', base='two', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish middle left upwards'),
    'two.middleRightDown': GD(g2='two', g1='two', l='two', w='two', name='two.middleRightDown', base='two', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish middle right downward'),
    'two.middleRightUp': GD(g2='two', g1='two', l='two', w='two', name='two.middleRightUp', base='two', accents=['flourish.middleRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='two simple flourish middle right upwards'),

    'three.bottomLeftDown': GD(g2='three', g1='three', l='three', w='three', name='three.bottomLeftDown', base='three', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish bottom left downward'),
    'three.bottomRightDown': GD(g2='three', g1='three', l='three', w='three', name='three.bottomRightDown', base='three', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish bottom right downward'),
    'three.topLeftUp': GD(g2='three', g1='three', l='three', w='three', name='three.topLeftUp', base='three', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish top left upwards'),
    'three.topRightUp': GD(g2='three', g1='three', l='three', w='three', name='three.topRightUp', base='three', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish top right upwards'),
    # Flourishes on the side
    'three.middleLeftDown': GD(g2='three', g1='three', l='three', w='three', name='three.middleLeftDown', base='three', accents=['flourish.middleLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish middle left downward'),
    'three.middleLeftUp': GD(g2='three', g1='three', l='three', w='three', name='three.middleLeftUp', base='three', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish middle left upwards'),
    'three.middleRightDown': GD(g2='three', g1='three', l='three', w='three', name='three.middleRightDown', base='three', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish middle right downward'),
    'three.middleRightUp': GD(g2='three', g1='three', l='three', w='three', name='three.middleRightUp', base='three', accents=['flourish.middleRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='three simple flourish middle right upwards'),

    'four.bottomLeftDown': GD(g2='four', g1='four', l='four', w='four', name='four.bottomLeftDown', base='four', accents=['flourish.bottomLeftDown2x'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish bottom left downward'),
    'four.bottomRightDown': GD(g2='four', g1='four', l='four', w='four', name='four.bottomRightDown', base='four', accents=['flourish.bottomRightDown2x'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish bottom right downward'),
    'four.bottomRightUp': GD(g2='four', g1='four', l='four', w='four', name='four.bottomRightUp', base='four.cbr', accents=['flourish.bottomRightUp1'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish bottom right upwards'),
    'four.cbr': GD(g2='four', g1='four', l='four', w='four', name='four.cbr', src='four', comment='four - connector bottom right', anchors=(BOTTOM_, BOTTOMLEFT_, BOTTOMRIGHT_, MIDDLELEFT_, MIDDLERIGHT_, TOP_, TOPLEFT_, TOPRIGHT_)),
    'four.topLeftUp': GD(g2='four', g1='four', l='four', w='four', name='four.topLeftUp', base='four', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish top left upwards'),
    'four.topRightUp': GD(g2='four', g1='four', l='four', w='four', name='four.topRightUp', base='four', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish top right upwards'),
    # Flourishes on the side
    'four.middleLeftDown': GD(g2='four', g1='four', l='four', w='four', name='four.middleLeftDown', base='four', accents=['flourish.middleLeftDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish middle left downward'),
    'four.middleLeftUp': GD(g2='four', g1='four', l='four', w='four', name='four.middleLeftUp', base='four', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish middle left upwards'),
    'four.middleRightDown': GD(g2='four', g1='four', l='four', w='four', name='four.middleRightDown', base='four', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish middle right downward'),
    'four.middleRightUp': GD(g2='four', g1='four', l='four', w='four', name='four.middleRightUp', base='four', accents=['flourish.middleRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='four simple flourish middle right upwards'),

    'five.bottomLeftDown': GD(g2='five', g1='five', l='five', w='five', name='five.bottomLeftDown', base='five', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish bottom left downward'),
    'five.bottomRightDown': GD(g2='five', g1='five', l='five', w='five', name='five.bottomRightDown', base='five', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish bottom right downward'),
    'five.topLeftUp': GD(g2='five', g1='five', l='five', w='five', name='five.topLeftUp', base='five', accents=['flourish.topLeftUp2x'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish top left upwards'),
    'five.topRightDown': GD(g2='five', g1='five', l='five', w='five', name='five.topRightDown', base='five', accents=['flourish.topRightDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish top right downward'),
    'five.topRightUp': GD(g2='five', g1='five', l='five', w='five', name='five.topRightUp', base='five', accents=['flourish.topRightUp2x'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish top right upwards'),
    # Flourishes on the side
    'five.middleLeftDown': GD(g2='five', g1='five', l='five', w='five', name='five.middleLeftDown', base='five', accents=['flourish.middleLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish middle left downward'),
    'five.middleLeftUp': GD(g2='five', g1='five', l='five', w='five', name='five.middleLeftUp', base='five', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish middle left upwards'),
    'five.middleRightDown': GD(g2='five', g1='five', l='five', w='five', name='five.middleRightDown', base='five', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish middle right downward'),
    'five.middleRightUp': GD(g2='five', g1='five', l='five', w='five', name='five.middleRightUp', base='five', accents=['flourish.middleRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='five simple flourish middle right upwards'),

    'six.bottomLeftDown': GD(g2='six', g1='six', l='six', w='six', name='six.bottomLeftDown', base='six', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish bottom left downward'),
    'six.bottomRightDown': GD(g2='six', g1='six', l='six', w='six', name='six.bottomRightDown', base='six', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish bottom right downward'),
    'six.topLeftUp': GD(g2='six', g1='six', l='six', w='six', name='six.topLeftUp', base='six', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish top left upwards'),
    'six.topRightUp': GD(g2='six', g1='six', l='six', w='six', name='six.topRightUp', base='six', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish top right upwards'),
    # Flourishes on the side
    'six.middleLeftDown': GD(g2='six', g1='six', l='six', w='six', name='six.middleLeftDown', base='six', accents=['flourish.middleLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish middle left downward'),
    'six.middleLeftUp': GD(g2='six', g1='six', l='six', w='six', name='six.middleLeftUp', base='six', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish middle left upwards'),
    'six.middleRightUp': GD(g2='six', g1='six', l='six', w='six', name='six.middleRightUp', base='six', accents=['flourish.middleRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish middle right upwards'),
    # Unreachable
    #'six.middleRightDown': GD(g2='six', g1='six', l='six', w='six', name='six.middleRightDown', base='six', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='six simple flourish middle right downward'),

    'seven.bottomLeftDown': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.bottomLeftDown', base='seven', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish bottom left downward'),
    'seven.bottomRightDown': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.bottomRightDown', base='seven', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish bottom right downward'),
    'seven.topLeftUp': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.topLeftUp', base='seven', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish top left upwards'),
    'seven.topRightUp': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.topRightUp', base='seven', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish top right upwards'),
    # Flourishes on the side
    'seven.middleLeftDown': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.middleLeftDown', base='seven', accents=['flourish.middleLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish middle left downward'),
    'seven.middleLeftUp': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.middleLeftUp', base='seven', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish middle left upwards'),
    'seven.middleRightDown': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.middleRightDown', base='seven', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish middle right downward'),
    'seven.middleRightUp': GD(g2='seven', g1='seven', l='seven', w='seven', name='seven.middleRightUp', base='seven', accents=['flourish.middleRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='seven simple flourish middle right upwards'),

    'eight.bottomLeftDown': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.bottomLeftDown', base='eight', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish bottom left downward'),
    'eight.bottomRightDown': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.bottomRightDown', base='eight', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish bottom right downward'),
    'eight.topLeftUp': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.topLeftUp', base='eight', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish top left upwards'),
    'eight.topRightUp': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.topRightUp', base='eight', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish top right upwards'),
    # Flourishes on the side
    'eight.middleLeftDown': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.middleLeftDown', base='eight', accents=['flourish.middleLeftDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish middle left downward'),
    'eight.middleLeftUp': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.middleLeftUp', base='eight', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish middle left upwards'),
    'eight.middleRightDown': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.middleRightDown', base='eight', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish middle right downward'),
    'eight.middleRightUp': GD(g2='eight', g1='eight', l='eight', w='eight', name='eight.middleRightUp', base='eight', accents=['flourish.middleRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='eight simple flourish middle right upwards'),

    'nine.bottomLeftDown': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.bottomLeftDown', base='nine', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish bottom left downward'),
    'nine.bottomRightDown': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.bottomRightDown', base='nine', accents=['flourish.bottomRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish bottom right downward'),
    'nine.topLeftUp': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.topLeftUp', base='nine', accents=['flourish.topLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish top left upwards'),
    'nine.topRightUp': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.topRightUp', base='nine', accents=['flourish.topRightUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish top right upwards'),
    # Flourishes on the side
    'nine.middleLeftDown': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.middleLeftDown', base='nine', accents=['flourish.middleLeftDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish middle left downward'),
    'nine.middleLeftUp': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.middleLeftUp', base='nine', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish middle left upwards'),
    'nine.middleRightDown': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.middleRightDown', base='nine', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish middle right downward'),
    'nine.middleRightUp': GD(g2='nine', g1='nine', l='nine', w='nine', name='nine.middleRightUp', base='nine', accents=['flourish.middleRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='nine simple flourish middle right upwards'),

    'ampersand.bottomLeftDown': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.bottomLeftDown', base='ampersand', accents=['flourish.bottomLeftDown2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish bottom left downward'),
    'ampersand.bottomRightDown': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.bottomRightDown', base='ampersand', accents=['flourish.bottomRightDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish bottom right downward'),
    'ampersand.topLeftUp': GD(g2='nine', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.topLeftUp', base='ampersand', accents=['flourish.topLeftUp2s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish top left upwards'),
    'ampersand.topRightUp': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.topRightUp', base='ampersand', accents=['flourish.topRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish top right upwards'),
    # Flourishes on the side
    'ampersand.middleLeftDown': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.middleLeftDown', base='ampersand', accents=['flourish.middleLeftDown2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish middle left downward'),
    'ampersand.middleLeftUp': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.middleLeftUp', base='ampersand', accents=['flourish.middleLeftUp1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish middle left upwards'),
    'ampersand.middleRightDown': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.middleRightDown', base='ampersand', accents=['flourish.middleRightDown1s'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish middle right downward'),
    'ampersand.middleRightUp': GD(g2='ampersand', g1='ampersand', l='ampersand', w='ampersand', name='ampersand.middleRightUp', base='ampersand', accents=['flourish.middleRightUp2'], height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT, comment='ampersand simple flourish middle right upwards'),

    'A.bottomLeftDown': GD(g2='A', g1='A', l='A', w='A', name='A.bottomLeftDown', base='A', accents=['flourish.bottomLeftDown2x'], comment='A simple flourish bottom left downward'),
    'A.bottomLeftUp': GD(g2='A', g1='A', l='A', w='A', name='A.bottomLeftUp', base='A', accents=['flourish.bottomLeftUp1'], comment='A simple flourish bottom left upwards'),
    'A.bottomRightDown': GD(g2='A', g1='A', l='A', w='A', name='A.bottomRightDown', base='A', accents=['flourish.bottomRightDown2x'], comment='A simple flourish bottom right downward'),
    'A.bottomRightUp': GD(g2='A', g1='A', l='A', w='A', name='A.bottomRightUp', base='A', accents=['flourish.bottomRightUp1'], comment='A simple flourish bottom right upwards'),
    'A.topLeftDown': GD(g2='A', g1='A', l='A', w='A', name='A.topLeftDown', base='A', accents=['flourish.topLeftDown2sl'], comment='A simple flourish top left downward'),
    'A.topLeftUp': GD(g2='A', g1='A', l='A', w='A', name='A.topLeftUp', base='A', accents=['flourish.topLeftUp2s'], comment='A simple flourish top left upwards'),
    'A.topRightDown': GD(g2='A', g1='A', l='A', w='A', name='A.topRightDown', base='A', accents=['flourish.topRightDown2sl'], comment='A simple flourish top right downward'),
    'A.topRightUp': GD(g2='A', g1='A', l='A', w='A', name='A.topRightUp', base='A', accents=['flourish.topRightUp2'], comment='A simple flourish top right upwards'),
     # Flourishes on the side
    'A.middleLeftUp': GD(g2='A', g1='A', l='A', w='A', name='A.middleLeftUp', base='A', accents=['flourish.middleLeftUp1'], comment='A simple flourish middle left upwards'),
    'A.middleRightDown': GD(g2='A', g1='X', l='A', w='A', name='A.middleRightDown', base='A', accents=['flourish.middleRightDown2d'], comment='X simple flourish middle right downward'),
    'A.middleRightUp': GD(g2='A', g1='A', l='A', w='A', name='A.middleRightUp', base='A', accents=['flourish.middleRightUp1'], comment='A simple flourish middle right upwards'),

    'B.bottomLeftDown': GD(g2='H', g1='B', l='B', w='B', name='B.bottomLeftDown', base='B', accents=['flourish.bottomLeftDown2x'], comment='B simple flourish bottom left downward'),
    'B.bottomLeftUp': GD(g2='H', g1='B', l='B', w='B', name='B.bottomLeftUp', base='B', accents=['flourish.bottomLeftUp1s'], comment='B simple flourish bottom left upwards'),
    'B.bottomRightDown': GD(g2='H', g1='B', l='B', w='B', name='B.bottomRightDown', base='B', accents=['flourish.bottomRightDown2'], comment='B simple flourish bottom right downward'),
    'B.topLeftDown': GD(g2='H', g1='B', l='B', w='B', name='B.topLeftDown', base='B', accents=['flourish.topLeftDown1s'], comment='B simple flourish top left downward'),
    'B.topLeftUp': GD(g2='H', g1='B', l='B', w='B', name='B.topLeftUp', base='B', accents=['flourish.topLeftUp2x'], comment='B simple flourish top left upwards'),
    'B.topRightUp': GD(g2='H', g1='B', l='B', w='B', name='B.topRightUp', base='B', accents=['flourish.topRightUp2'], comment='B simple flourish top right upwards'),
    # Flourishes on the side
    'B.middleLeftDown': GD(g2='H', g1='B', l='B', w='B', name='B.middleLeftDown', base='B', accents=['flourish.middleLeftDown2s'], comment='B simple flourish middle left downward'),
    'B.middleLeftUp': GD(g2='H', g1='B', l='B', w='B', name='B.middleLeftUp', base='B', accents=['flourish.middleLeftUp1'], comment='B simple flourish middle left upwards'),
    'B.middleRightDown': GD(g2='H', g1='B', l='B', w='B', name='B.middleRightDown', base='B', accents=['flourish.middleRightDown1s'], comment='B simple flourish middle right downward'),
    'B.middleRightUp': GD(g2='H', g1='B', l='B', w='B', name='B.middleRightUp', base='B', accents=['flourish.middleRightUp2'], comment='B simple flourish middle right upwards'),

    'C.bottomLeftDown': GD(g2='O', g1='C', l='C', w='C', name='C.bottomLeftDown', base='C', accents=['flourish.bottomLeftDown2s'], comment='C simple flourish bottom left downward'),
    'C.bottomRightDown': GD(g2='O', g1='C', l='C', w='C', name='C.bottomRightDown', base='C', accents=['flourish.bottomRightDown2'], comment='C simple flourish bottom right downward'),
    'C.topLeftUp': GD(g2='O', g1='C', l='C', w='C', name='C.topLeftUp', base='C', accents=['flourish.topLeftUp2s'], comment='C simple flourish top left upwards'),
    'C.topRightUp': GD(g2='O', g1='C', l='C', w='C', name='C.topRightUp', base='C', accents=['flourish.topRightUp2'], comment='C simple flourish top right upwards'),
    # Flourishes on the side
    'C.middleLeftDown': GD(g2='O', g1='C', l='C', w='C', name='C.middleLeftDown', base='C', accents=['flourish.middleLeftDown2'], comment='C simple flourish middle left downward'),
    'C.middleLeftUp': GD(g2='O', g1='C', l='C', w='C', name='C.middleLeftUp', base='C', accents=['flourish.middleLeftUp1s'], comment='C simple flourish middle left upwards'),
    'C.middleRightDown': GD(g2='O', g1='C', l='C', w='C', name='C.middleRightDown', base='C', accents=['flourish.middleRightDown2s'], comment='C simple flourish middle right downward'),
    'C.middleRightUp': GD(g2='O', g1='C', l='C', w='C', name='C.middleRightUp', base='C', accents=['flourish.middleRightUp1'], comment='C simple flourish middle right upwards'),

    'D.bottomLeftDown': GD(g2='H', g1='O', l='D', w='D', name='D.bottomLeftDown', base='D', accents=['flourish.bottomLeftDown2x'], comment='D simple flourish bottom left downward'),
    'D.bottomLeftUp': GD(g2='H', g1='O', l='D', w='D', name='D.bottomLeftUp', base='D', accents=['flourish.bottomLeftUp2s'], comment='D simple flourish bottom left upwards'),
    'D.bottomRightDown': GD(g2='H', g1='O', l='D', w='D', name='D.bottomRightDown', base='D', accents=['flourish.bottomRightDown2'], comment='D simple flourish bottom right downward'),
    'D.topLeftDown': GD(g2='H', g1='O', l='D', w='D', name='D.topLeftDown', base='D', accents=['flourish.topLeftDown1s'], comment='D simple flourish top left downward'),
    'D.topLeftUp': GD(g2='H', g1='O', l='D', w='D', name='D.topLeftUp', base='D', accents=['flourish.topLeftUp2x'], comment='D simple flourish top left upwards'),
    'D.topRightUp': GD(g2='H', g1='O', l='D', w='D', name='D.topRightUp', base='D', accents=['flourish.topRightUp2'], comment='D simple flourish top right upwards'),
    # Flourishes on the side
    'D.middleLeftDown': GD(g2='H', g1='O', l='D', w='D', name='D.middleLeftDown', base='D', accents=['flourish.middleLeftDown2s'], comment='D simple flourish middle left downward'),
    'D.middleLeftUp': GD(g2='H', g1='O', l='D', w='D', name='D.middleLeftUp', base='D', accents=['flourish.middleLeftUp1'], comment='D simple flourish middle left upwards'),
    'D.middleRightDown': GD(g2='H', g1='O', l='D', w='D', name='D.middleRightDown', base='D', accents=['flourish.middleRightDown1s'], comment='D simple flourish middle right downward'),
    'D.middleRightUp': GD(g2='H', g1='O', l='D', w='D', name='D.middleRightUp', base='D', accents=['flourish.middleRightUp2'], comment='D simple flourish middle right upwards'),

    'E.bottomLeftDown': GD(g2='H', g1='E', l='E', w='E', name='E.bottomLeftDown', base='E', accents=['flourish.bottomLeftDown2x'], comment='E simple flourish bottom left downward'),
    'E.bottomLeftUp': GD(g2='H', g1='E', l='E', w='E', name='E.bottomLeftUp', base='E', accents=['flourish.bottomLeftUp1s'], comment='E simple flourish bottom left upwards'),
    'E.bottomRightDown': GD(g2='H', g1='E', l='E', w='E', name='E.bottomRightDown', base='E', accents=['flourish.bottomRightDown2s'], comment='E simple flourish bottom right downward'),
    'E.topLeftDown': GD(g2='H', g1='E', l='E', w='E', name='E.topLeftDown', base='E', accents=['flourish.topLeftDown1s'], comment='E simple flourish top left downward'),
    'E.topLeftUp': GD(g2='H', g1='E', l='E', w='E', name='E.topLeftUp', base='E', accents=['flourish.topLeftUp2x'], comment='E simple flourish top left upwards'),
    'E.topRightUp': GD(g2='H', g1='E', l='E', w='E', name='E.topRightUp', base='E', accents=['flourish.topRightUp2'], comment='E simple flourish top right upwards'),
    # Flourishes on the side
    'E.middleLeftDown': GD(g2='H', g1='E', l='E', w='E', name='E.middleLeftDown', base='E', accents=['flourish.middleLeftDown2s'], comment='E simple flourish middle left downward'),
    'E.middleLeftUp': GD(g2='H', g1='E', l='E', w='E', name='E.middleLeftUp', base='E', accents=['flourish.middleLeftUp1'], comment='E simple flourish middle left upwards'),
    'E.middleRightDown': GD(g2='H', g1='E', l='E', w='E', name='E.middleRightDown', base='E', accents=['flourish.middleRightDown1s'], comment='E simple flourish middle right downward'),
    'E.middleRightUp': GD(g2='H', g1='E', l='E', w='E', name='E.middleRightUp', base='E', accents=['flourish.middleRightUp1'], comment='E simple flourish middle right upwards'),

    'F.bottomLeftDown': GD(g2='H', g1='F', l='F', w='F', name='F.bottomLeftDown', base='F', accents=['flourish.bottomLeftDown2x'], comment='F simple flourish bottom left downward'),
    'F.bottomLeftUp': GD(g2='H', g1='F', l='F', w='F', name='F.bottomLeftUp', base='F', accents=['flourish.bottomLeftUp2s'], comment='F simple flourish bottom left upwards'),
    'F.bottomRightDown': GD(g2='H', g1='F', l='F', w='F', name='F.bottomRightDown', base='F', accents=['flourish.bottomRightDown2x'], comment='F simple flourish bottom right downward'),
    'F.topLeftDown': GD(g2='H', g1='F', l='F', w='F', name='F.topLeftDown', base='F', accents=['flourish.topLeftDown1s'], comment='F simple flourish top left downward'),
    'F.topLeftUp': GD(g2='H', g1='F', l='F', w='F', name='F.topLeftUp', base='F', accents=['flourish.topLeftUp2x'], comment='F simple flourish top left upwards'),
    'F.topRightUp': GD(g2='H', g1='F', l='F', w='F', name='F.topRightUp', base='F', accents=['flourish.topRightUp2'], comment='F simple flourish top right upwards'),
    # Flourishes on the side, no simple way to connect to right side.
    'F.middleLeftDown': GD(g2='H', g1='F', l='F', w='F', name='F.middleLeftDown', base='F', accents=['flourish.middleLeftDown2s'], comment='F simple flourish middle left downward'),
    'F.middleLeftUp': GD(g2='H', g1='F', l='F', w='F', name='F.middleLeftUp', base='F', accents=['flourish.middleLeftUp1'], comment='F simple flourish middle left upwards'),

    'G.bottomLeftDown': GD(g2='O', g1='G', l='G', w='G', name='G.bottomLeftDown', base='G', accents=['flourish.bottomLeftDown2s'], comment='G simple flourish bottom left downward'),
    'G.bottomRightDown': GD(g2='O', g1='G', l='G', w='G', name='G.bottomRightDown', base='G', accents=['flourish.bottomRightDown2'], comment='G simple flourish bottom right downward'),
    'G.topLeftUp': GD(g2='O', g1='G', l='G', w='G', name='G.topLeftUp', base='G', accents=['flourish.topLeftUp2s'], comment='G simple flourish top left upwards'),
    'G.topRightUp': GD(g2='O', g1='G', l='G', w='G', name='G.topRightUp', base='G', accents=['flourish.topRightUp2'], comment='G simple flourish top right upwards'),
    # Flourishes on the side
    'G.middleLeftDown': GD(g2='O', g1='G', l='G', w='G', name='G.middleLeftDown', base='G', accents=['flourish.middleLeftDown2'], comment='G simple flourish middle left downward'),
    'G.middleLeftUp': GD(g2='O', g1='G', l='G', w='G', name='G.middleLeftUp', base='G', accents=['flourish.middleLeftUp1s'], comment='G simple flourish middle left upwards'),
    'G.middleRightDown': GD(g2='O', g1='G', l='G', w='G', name='G.middleRightDown', base='G', accents=['flourish.middleRightDown1s'], comment='G simple flourish middle right downward'),
    'G.middleRightUp': GD(g2='O', g1='G', l='G', w='G', name='G.middleRightUp', base='G', accents=['flourish.middleRightUp1'], comment='G simple flourish middle right upwards'),

    'H.bottomLeftDown': GD(g2='H', g1='H', l='H', w='H', name='H.bottomLeftDown', base='H', accents=['flourish.bottomLeftDown2x'], comment='H simple flourish bottom left downward'),
    'H.bottomLeftUp': GD(g2='H', g1='H', l='H', w='H', name='H.bottomLeftUp', base='H', accents=['flourish.bottomLeftUp1s'], comment='H simple flourish bottom left upwards'),
    'H.bottomRightDown': GD(g2='H', g1='H', l='H', w='H', name='H.bottomRightDown', base='H', accents=['flourish.bottomRightDown2x'], comment='H simple flourish bottom right downward'),
    'H.bottomRightUp': GD(g2='H', g1='H', l='H', w='H', name='H.bottomRightUp', base='H', accents=['flourish.bottomRightUp1s'], comment='H simple flourish bottom right upwards'),
    'H.topLeftDown': GD(g2='H', g1='H', l='H', w='H', name='H.topLeftDown', base='H', accents=['flourish.topLeftDown1s'], comment='H simple flourish top left downward'),
    'H.topLeftUp': GD(g2='H', g1='H', l='H', w='H', name='H.topLeftUp', base='H', accents=['flourish.topLeftUp2x'], comment='H simple flourish top left upwards'),
    'H.topRightDown': GD(g2='H', g1='H', l='H', w='H', name='H.topRightDown', base='H', accents=['flourish.topRightDown1s'], comment='H simple flourish top right downward'),
    'H.topRightUp': GD(g2='H', g1='H', l='H', w='H', name='H.topRightUp', base='H', accents=['flourish.topRightUp2x'], comment='H simple flourish top right upwards'),
    # Flourishes on the side
    'H.middleLeftDown': GD(g2='H', g1='H', l='H', w='H', name='H.middleLeftDown', base='H', accents=['flourish.middleLeftDown2s'], comment='H simple flourish middle left downward'),
    'H.middleLeftUp': GD(g2='H', g1='H', l='H', w='H', name='H.middleLeftUp', base='H', accents=['flourish.middleLeftUp1'], comment='H simple flourish middle left upwards'),
    'H.middleRightDown': GD(g2='H', g1='H', l='H', w='H', name='H.middleRightDown', base='H', accents=['flourish.middleRightDown1'], comment='H simple flourish middle right downward'),
    'H.middleRightUp': GD(g2='H', g1='H', l='H', w='H', name='H.middleRightUp', base='H', accents=['flourish.middleRightUp2s'], comment='H simple flourish middle right upwards'),

    'I.bottomLeftDown': GD(g2='H', g1='H', l='I', w='I', name='I.bottomLeftDown', base='I', accents=['flourish.bottomLeftDown2x'], comment='I simple flourish bottom left downward'),
    'I.bottomLeftUp': GD(g2='H', g1='H', l='I', w='I', name='I.bottomLeftUp', base='I', accents=['flourish.bottomLeftUp2s'], comment='I simple flourish bottom left upwards'),
    'I.bottomRightDown': GD(g2='H', g1='H', l='I', w='I', name='I.bottomRightDown', base='I', accents=['flourish.bottomRightDown2x'], comment='I simple flourish bottom right downward'),    
    'I.bottomRightUp': GD(g2='H', g1='H', l='I', w='I', name='I.bottomRightUp', base='I', accents=['flourish.bottomRightUp1s'], comment='I simple flourish bottom right upwards'),
    'I.topLeftDown': GD(g2='H', g1='H', l='I', w='I', name='I.topLeftDown', base='I', accents=['flourish.topLeftDown1s'], comment='I simple flourish top left downward'),
    'I.topLeftUp': GD(g2='H', g1='H', l='I', w='I', name='I.topLeftUp', base='I', accents=['flourish.topLeftUp2x'], comment='I simple flourish top left upwards'),
    'I.topRightDown': GD(g2='H', g1='H', l='I', w='I', name='I.topRightDown', base='I', accents=['flourish.topRightDown1s'], comment='I simple flourish top right upwards'),
    'I.topRightUp': GD(g2='H', g1='H', l='I', w='I', name='I.topRightUp', base='I', accents=['flourish.topRightUp2x'], comment='I simple flourish top right upwards'),
    # Flourishes on the side
    'I.middleLeftDown': GD(g2='H', g1='H', l='I', w='I', name='I.middleLeftDown', base='I', accents=['flourish.middleLeftDown2s'], comment='I simple flourish middle left downward'),
    'I.middleLeftUp': GD(g2='H', g1='H', l='I', w='I', name='I.middleLeftUp', base='I', accents=['flourish.middleLeftUp1'], comment='I simple flourish middle left upwards'),
    'I.middleRightDown': GD(g2='H', g1='H', l='I', w='I', name='I.middleRightDown', base='I', accents=['flourish.middleRightDown1'], comment='I simple flourish middle right downward'),
    'I.middleRightUp': GD(g2='H', g1='H', l='I', w='I', name='I.middleRightUp', base='I', accents=['flourish.middleRightUp2s'], comment='I simple flourish middle right upwards'),

    'J.bottomLeftDown': GD(g2='J', g1='J', l='J', w='J', name='J.bottomLeftDown', base='J', accents=['flourish.bottomLeftDown2s'], comment='J simple flourish bottom left downward'),
    'J.bottomLeftUp': GD(g2='J', g1='J', l='J', w='J', name='J.bottomLeftUp', base='J', accents=['flourish.bottomLeftUp1'], comment='J simple flourish bottom left upwards'),
    'J.bottomRightDown': GD(g2='J', g1='J', l='J', w='J', name='J.bottomRightDown', base='J', accents=['flourish.bottomRightDown2s'], comment='J simple flourish bottom right downward'),
    'J.topLeftDown': GD(g2='J', g1='J', l='J', w='J', name='J.topLeftDown', base='J', accents=['flourish.topLeftDown1s'], comment='J simple flourish top left downward'),
    'J.topLeftUp': GD(g2='J', g1='J', l='J', w='J', name='J.topLeftUp', base='J', accents=['flourish.topLeftUp2x'], comment='J simple flourish top left upwards'),
    'J.topRightDown': GD(g2='J', g1='J', l='J', w='J', name='J.topRightDown', base='J', accents=['flourish.topRightDown1s'], comment='J simple flourish top right downward'),
    'J.topRightUp': GD(g2='J', g1='J', l='J', w='J', name='J.topRightUp', base='J', accents=['flourish.topRightUp2x'], comment='J simple flourish top right upwards'),
    # Flourishes on the side
    'J.middleLeftDown': GD(g2='J', g1='J', l='J', w='J', name='J.middleLeftDown', base='J', accents=['flourish.middleLeftDown2s'], comment='J simple flourish middle left downward'),
    'J.middleLeftUp': GD(g2='J', g1='J', l='J', w='J', name='J.middleLeftUp', base='J', accents=['flourish.middleLeftUp1'], comment='J simple flourish middle left upwards'),
    'J.middleRightDown': GD(g2='J', g1='J', l='J', w='J', name='J.middleRightDown', base='J', accents=['flourish.middleRightDown1'], comment='J simple flourish middle right downward'),
    'J.middleRightUp': GD(g2='J', g1='J', l='J', w='J', name='J.middleRightUp', base='J', accents=['flourish.middleRightUp2'], comment='J simple flourish middle right upwards'),

    'J.base.bottomLeftDown': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.bottomLeftDown', base='J.base', accents=['flourish.bottomLeftDown2s'], comment='J simple flourish bottom left downward'),
    'J.base.bottomRightDown': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.bottomRightDown', base='J.base', accents=['flourish.bottomRightDown2s'], comment='J simple flourish bottom right downward'),
    'J.base.topLeftDown': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.topLeftDown', base='J.base', accents=['flourish.topLeftDown1s'], comment='J simple flourish top left downward'),
    'J.base.topLeftUp': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.topLeftUp', base='J.base', accents=['flourish.topLeftUp2x'], comment='J simple flourish top left upwards'),
    'J.base.topRightDown': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.topRightDown', base='J.base', accents=['flourish.topRightDown1s'], comment='J simple flourish top right downward'),
    'J.base.topRightUp': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.topRightUp', base='J.base', accents=['flourish.topRightUp2x'], comment='J simple flourish top right upwards'),
    # Flourishes on the side
    'J.base.middleLeftDown': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.middleLeftDown', base='J.base', accents=['flourish.middleLeftDown2s'], comment='J simple flourish middle left downward'),
    'J.base.middleLeftUp': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.middleLeftUp', base='J.base', accents=['flourish.middleLeftUp1'], comment='J simple flourish middle left upwards'),
    'J.base.middleRightDown': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.middleRightDown', base='J.base', accents=['flourish.middleRightDown1'], comment='J simple flourish middle right downward'),
    'J.base.middleRightUp': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='J.base.middleRightUp', base='J.base', accents=['flourish.middleRightUp2'], comment='J simple flourish middle right upwards'),

    'K.bottomLeftDown': GD(g2='H', g1='K', l='K', w='K', name='K.bottomLeftDown', base='K', accents=['flourish.bottomLeftDown2x'], comment='K simple flourish bottom left downward'),
    'K.bottomLeftUp': GD(g2='H', g1='K', l='K', w='K', name='K.bottomLeftUp', base='K', accents=['flourish.bottomLeftUp1s'], comment='K simple flourish bottom left upwards'),
    'K.bottomRightDown': GD(g2='H', g1='K', l='K', w='K', name='K.bottomRightDown', base='K', accents=['flourish.bottomRightDown2x'], comment='K simple flourish bottom right downward'),
    'K.bottomRightUp': GD(g2='H', g1='K', l='K', w='K', name='K.bottomRightUp', base='K', accents=['flourish.bottomRightUp1s'], comment='K simple flourish bottom right upwards'),
    'K.topLeftDown': GD(g2='H', g1='K', l='K', w='K', name='K.topLeftDown', base='K', accents=['flourish.topLeftDown1s'], comment='K simple flourish top left downward'),
    'K.topLeftUp': GD(g2='H', g1='K', l='K', w='K', name='K.topLeftUp', base='K', accents=['flourish.topLeftUp2x'], comment='K simple flourish top left upwards'),
    'K.topRightDown': GD(g2='H', g1='K', l='K', w='K', name='K.topRightDown', base='K', accents=['flourish.topRightDown1s'], comment='K simple flourish top right downward'),
    'K.topRightUp': GD(g2='H', g1='K', l='K', w='K', name='K.topRightUp', base='K', accents=['flourish.topRightUp2xs'], comment='K simple flourish top right upwards'),
    # Flourishes on left side and top-right
    'K.middleLeftDown': GD(g2='H', g1='K', l='K', w='K', name='K.middleLeftDown', base='K', accents=['flourish.middleLeftDown2s'], comment='K simple flourish middle left downward'),
    'K.middleLeftUp': GD(g2='H', g1='K', l='K', w='K', name='K.middleLeftUp', base='K', accents=['flourish.middleLeftUp1'], comment='K simple flourish middle left upwards'),
    'K.middleRightDown': GD(g2='H', g1='K', l='K', w='K', name='K.middleRightDown', base='K', accents=['flourish.middleRightDown1d'], comment='K simple flourish middle right downward'),
    'K.middleRightUp': GD(g2='H', g1='K', l='K', w='K', name='K.middleRightUp', base='K', accents=['flourish.middleRightUp1d'], comment='K simple flourish middle right upwards'),

    # Too much /P 'L.topRightDown'
    'L.bottomLeftDown': GD(g2='H', g1='L', l='L', w='L', name='L.bottomLeftDown', base='L', accents=['flourish.bottomLeftDown2x'], smallTrackRight=0, comment='L simple flourish bottom left downward'),
    'L.bottomLeftUp': GD(g2='H', g1='L', l='L', w='L', name='L.bottomLeftUp', base='L', accents=['flourish.bottomLeftUp2s'], smallTrackRight=0, comment='L simple flourish bottom left upwards'),
    'L.bottomRightDown': GD(g2='H', g1='L', l='L', w='L', name='L.bottomRightDown', base='L', accents=['flourish.bottomRightDown2'], smallTrackRight=0, comment='L simple flourish bottom right downward'),
    'L.topLeftDown': GD(g2='H', g1='L', l='L', w='L', name='L.topLeftDown', base='L', accents=['flourish.topLeftDown1s'], smallTrackRight=0, comment='L simple flourish top left downward'),
    'L.topLeftUp': GD(g2='H', g1='L', l='L', w='L', name='L.topLeftUp', base='L', accents=['flourish.topLeftUp2x'], smallTrackRight=0, comment='L simple flourish top left upwards'),
    'L.topRightUp': GD(g2='H', g1='L', l='L', w='L', name='L.topRightUp', base='L', accents=['flourish.topRightUp2x'], smallTrackRight=0, comment='L simple flourish top right upwards'),
    # Flourishes on the side
    'L.middleLeftDown': GD(g2='H', g1='L', l='H', w='L', name='L.middleLeftDown', base='L', accents=['flourish.middleLeftDown2s'], smallTrackRight=0, comment='L simple flourish middle left downward'),
    'L.middleLeftUp': GD(g2='H', g1='L', l='L', w='L', name='L.middleLeftUp', base='L', accents=['flourish.middleLeftUp1'], smallTrackRight=0, comment='L simple flourish middle left upwards'),
    'L.middleRightUp': GD(g2='H', g1='L', l='L', w='L', name='L.middleRightUp', base='L', accents=['flourish.middleRightUp1'], smallTrackRight=0, comment='L simple flourish middle right upwards'),

    'M.bottomLeftDown': GD(g2='N', g1='H', l='M', w='M', name='M.bottomLeftDown', base='M', accents=['flourish.bottomLeftDown2x'], comment='M simple flourish bottom left downward'),
    'M.bottomLeftUp': GD(g2='N', g1='H', l='M', w='M', name='M.bottomLeftUp', base='M', accents=['flourish.bottomLeftUp1s'], comment='M simple flourish bottom left upwards'),
    'M.bottomRightDown': GD(g2='N', g1='H', l='M', w='M', name='M.bottomRightDown', base='M', accents=['flourish.bottomRightDown2x'], comment='M simple flourish bottom right downward'),
    'M.bottomRightUp': GD(g2='N', g1='H', l='M', w='M', name='M.bottomRightUp', base='M', accents=['flourish.bottomRightUp1s'], comment='M simple flourish bottom right upwards'),
    'M.topLeftDown': GD(g2='N', g1='H', l='M', w='M', name='M.topLeftDown', base='M', accents=['flourish.topLeftDown1s'], comment='M simple flourish top left downward'),
    'M.topLeftUp': GD(g2='N', g1='H', l='M', w='M', name='M.topLeftUp', base='M', accents=['flourish.topLeftUp2xs'], comment='M simple flourish top left upwards'),
    'M.topRightDown': GD(g2='N', g1='H', l='M', w='M', name='M.topRightDown', base='M', accents=['flourish.topRightDown1s'], comment='M simple flourish top right downward'),
    'M.topRightUp': GD(g2='N', g1='H', l='M', w='M', name='M.topRightUp', base='M', accents=['flourish.topRightUp2xs'], comment='M simple flourish top right upwards'),
    # Flourishes on the side
    'M.middleLeftDown': GD(g2='N', g1='H', l='M', w='M', name='M.middleLeftDown', base='M', accents=['flourish.middleLeftDown2s'], comment='M simple flourish middle left downward'),
    'M.middleLeftUp': GD(g2='N', g1='H', l='M', w='M', name='M.middleLeftUp', base='M', accents=['flourish.middleLeftUp1'], comment='M simple flourish middle left upwards'),
    'M.middleRightDown': GD(g2='N', g1='H', l='M', w='M', name='M.middleRightDown', base='M', accents=['flourish.middleRightDown1'], comment='M simple flourish middle right downward'),
    'M.middleRightUp': GD(g2='N', g1='H', l='M', w='M', name='M.middleRightUp', base='M', accents=['flourish.middleRightUp2s'], comment='M simple flourish middle right upwards'),

    'N.bottomLeftDown': GD(g2='N', g1='N', l='N', w='N', name='N.bottomLeftDown', base='N', accents=['flourish.bottomLeftDown2x'], comment='N simple flourish bottom left downward'),
    'N.bottomLeftUp': GD(g2='N', g1='N', l='N', w='N', name='N.bottomLeftUp', base='N', accents=['flourish.bottomLeftUp2s'], comment='N simple flourish bottom left upwards'),
    'N.bottomRightDown': GD(g2='N', g1='N', l='N', w='N', name='N.bottomRightDown', base='N', accents=['flourish.bottomRightDown2s'], comment='N simple flourish bottom right downward'),
    'N.topLeftDown': GD(g2='N', g1='N', l='N', w='N', name='N.topLeftDown', base='N', accents=['flourish.topLeftDown1s'], comment='N simple flourish top left downward'),
    'N.topLeftUp': GD(g2='N', g1='N', l='N', w='N', name='N.topLeftUp', base='N', accents=['flourish.topLeftUp2xs'], comment='N simple flourish top left upwards'),
    'N.topRightDown': GD(g2='N', g1='N', l='N', w='N', name='N.topRightDown', base='N', accents=['flourish.topRightDown1s'], comment='N simple flourish top right downward'),
    'N.topRightUp': GD(g2='N', g1='N', l='N', w='N', name='N.topRightUp', base='N', accents=['flourish.topRightUp2x'], comment='N simple flourish top right upwards'),
    # Flourishes on the side
    'N.middleLeftDown': GD(g2='N', g1='N', l='N', w='N', name='N.middleLeftDown', base='N', accents=['flourish.middleLeftDown2s'], comment='N simple flourish middle left downward'),
    'N.middleLeftUp': GD(g2='N', g1='N', l='N', w='N', name='N.middleLeftUp', base='N', accents=['flourish.middleLeftUp1'], comment='N simple flourish middle left upwards'),
    'N.middleRightDown': GD(g2='N', g1='N', l='N', w='N', name='N.middleRightDown', base='N', accents=['flourish.middleRightDown1'], comment='N simple flourish middle right downward'),
    'N.middleRightUp': GD(g2='N', g1='N', l='N', w='N', name='N.middleRightUp', base='N', accents=['flourish.middleRightUp2s'], comment='N simple flourish middle right upwards'),

    'O.bottomLeftDown': GD(g2='O', g1='O', l='O', w='O', name='O.bottomLeftDown', base='O', accents=['flourish.bottomLeftDown2s'], comment='O simple flourish bottom left downward'),
    'O.bottomRightDown': GD(g2='O', g1='O', l='O', w='O', name='O.bottomRightDown', base='O', accents=['flourish.bottomRightDown2'], comment='O simple flourish bottom right downward'),
    'O.topLeftUp': GD(g2='O', g1='O', l='O', w='O', name='O.topLeftUp', base='O', accents=['flourish.topLeftUp2s'], comment='O simple flourish top left upwards'),
    'O.topRightUp': GD(g2='O', g1='O', l='O', w='O', name='O.topRightUp', base='O', accents=['flourish.topRightUp2'], comment='O simple flourish top right upwards'),
    # Flourishes on the side
    'O.middleLeftDown': GD(g2='O', g1='O', l='O', w='O', name='O.middleLeftDown', base='O', accents=['flourish.middleLeftDown2'], comment='O simple flourish middle left downward'),
    'O.middleLeftUp': GD(g2='O', g1='O', l='O', w='O', name='O.middleLeftUp', base='O', accents=['flourish.middleLeftUp1s'], comment='O simple flourish middle left upwards'),
    'O.middleRightDown': GD(g2='O', g1='O',  l='O', w='O', name='O.middleRightDown', base='O', accents=['flourish.middleRightDown1s'], comment='O simple flourish middle right downward'),
    'O.middleRightUp': GD(g2='O', g1='O', l='O', w='O', name='O.middleRightUp', base='O', accents=['flourish.middleRightUp2'], comment='O simple flourish middle right upwards'),

    'P.bottomLeftDown': GD(g2='H', g1='P',l='P', w='P', name='P.bottomLeftDown', base='P', accents=['flourish.bottomLeftDown2x'], comment='P simple flourish bottom left downward'),
    'P.bottomLeftUp': GD(g2='H', g1='P',l='P', w='P', name='P.bottomLeftUp', base='P', accents=['flourish.bottomLeftUp1s'], comment='P simple flourish bottom left upwards'),
    'P.bottomRightDown': GD(g2='H', g1='P',l='P', w='P', name='P.bottomRightDown', base='P', accents=['flourish.bottomRightDown2x'], comment='P simple flourish bottom right downward'),
    'P.topLeftDown': GD(g2='H', g1='P',l='P', w='P', name='P.topLeftDown', base='P', accents=['flourish.topLeftDown1s'], comment='P simple flourish top left downward'),
    'P.topLeftUp': GD(g2='H', g1='P',l='P', w='P', name='P.topLeftUp', base='P', accents=['flourish.topLeftUp2x'], comment='P simple flourish top left upwards'),
    'P.topRightUp': GD(g2='H', g1='P', l='P', w='P', name='P.topRightUp', base='P', accents=['flourish.topRightUp2'], comment='P simple flourish top right upwards'),
    # Flourishes on the side
    'P.middleLeftDown': GD(g2='H', g1='P',l='P', w='P', name='P.middleLeftDown', base='P', accents=['flourish.middleLeftDown2s'], comment='P simple flourish middle left downward'),
    'P.middleLeftUp': GD(g2='H', g1='P',l='P', w='P', name='P.middleLeftUp', base='P', accents=['flourish.middleLeftUp1'], comment='P simple flourish middle left upwards'),
    'P.middleRightDown': GD(g2='H', g1='P',l='P', w='P', name='P.middleRightDown', base='P', accents=['flourish.middleRightDown1s'], comment='P simple flourish middle right downward'),
    'P.middleRightUp': GD(g2='H', g1='P',l='P', w='P', name='P.middleRightUp', base='P', accents=['flourish.middleRightUp2'], comment='P simple flourish middle right upwards'),

    'Q.topLeftUp': GD(g2='O', g1='O', l='Q', w='Q', name='Q.topLeftUp', base='Q', accents=['flourish.topLeftUp2s'], comment='Q simple flourish top left upwards'),
    'Q.topRightUp': GD(g2='O', g1='O', l='Q', w='Q', name='Q.topRightUp', base='Q', accents=['flourish.topRightUp2'], comment='Q simple flourish top right upwards'),
    # Flourishes on the side
    'Q.middleLeftUp': GD(g2='O', g1='O', l='Q', w='Q', name='Q.middleLeftUp', base='Q', accents=['flourish.middleLeftUp1s'], comment='Q simple flourish middle left upwards'),
    'Q.middleLeftDown': GD(g2='O', g1='O', l='Q', w='Q', name='Q.middleLeftDown', base='Q', accents=['flourish.middleLeftDown2'], comment='Q simple flourish middle left downward'),
    'Q.middleRightUp': GD(g2='O', g1='O', l='Q', w='Q', name='Q.middleRightUp', base='Q', accents=['flourish.middleRightUp2'], comment='Q simple flourish middle right upwards'),
    'Q.middleRightDown': GD(g2='O', g1='O', l='Q', w='Q', name='Q.middleRightDown', base='Q', accents=['flourish.middleRightDown1s'], comment='Q simple flourish middle right downward'),

    'R.bottomLeftDown': GD(g2='H', g1='R', l='R', w='R', name='R.bottomLeftDown', base='R', accents=['flourish.bottomLeftDown2x'], comment='R simple flourish bottom left downward'),
    'R.bottomLeftUp': GD(g2='H', g1='R', l='R', w='R', name='R.bottomLeftUp', base='R', accents=['flourish.bottomLeftUp2s'], comment='R simple flourish bottom left upwards'),
    'R.bottomRightUp': GD(g2='H', g1='R', l='R', w='R', name='R.bottomRightUp', base='R.cbr', accents=['flourish.bottomRightUp1'], comment='R simple flourish bottom right upwards'),
    'R.topLeftDown': GD(g2='H', g1='R', l='R', w='R', name='R.topLeftDown', base='R', accents=['flourish.topLeftDown1s'], comment='R simple flourish top left downward'),
    'R.topLeftUp': GD(g2='H', g1='R', l='R', w='R', name='R.topLeftUp', base='R', accents=['flourish.topLeftUp2x'], comment='R simple flourish top left upwards'),
    'R.topRightUp': GD(g2='H', g1='R', l='R', w='R', name='R.topRightUp', base='R', accents=['flourish.topRightUp2'], comment='R simple flourish top right upwards'),
    'R.bottomRightDown': GD(g2='H', g1='R', l='R', w='R', name='R.bottomRightDown', base='R.cbr', accents=['flourish.bottomRightDown2'], comment='R simple flourish bottom right downward'),
    # Flourishes on the side
    'R.middleLeftDown': GD(g2='H', g1='R', l='R', w='R', name='R.middleLeftDown', base='R', accents=['flourish.middleLeftDown2s'], comment='R simple flourish middle left downward'),
    'R.middleLeftUp': GD(g2='H', g1='R', l='R', w='R', name='R.middleLeftUp', base='R', accents=['flourish.middleLeftUp1'], comment='R simple flourish middle left upwards'),
    'R.middleRightDown': GD(g2='H', g1='R', l='R', w='R', name='R.middleRightDown', base='R', accents=['flourish.middleRightDown1s'], comment='R simple flourish middle right downward'),
    'R.middleRightUp': GD(g2='H', g1='R', l='R', w='R', name='R.middleRightUp', base='R', accents=['flourish.middleRightUp2s'], comment='R simple flourish middle right upwards'),

    'S.bottomLeftDown': GD(g2='S', g1='S',l='S', w='S', name='S.bottomLeftDown', base='S', accents=['flourish.bottomLeftDown2s'], comment='S simple flourish bottom left downward'),
    'S.bottomRightDown': GD(g2='S', g1='S',l='S', w='S', name='S.bottomRightDown', base='S', accents=['flourish.bottomRightDown2'], comment='S simple flourish bottom right downward'),
    'S.topLeftUp': GD(g2='S', g1='S',l='S', w='S', name='S.topLeftUp', base='S', accents=['flourish.topLeftUp2s'], comment='S simple flourish top left upwards'),
    'S.topRightUp': GD(g2='S', g1='S', l='S', w='S', name='S.topRightUp', base='S', accents=['flourish.topRightUp2'], comment='S simple flourish top right upwards'),
    # Flourishes on the side
    'S.middleLeftDown': GD(g2='S', g1='S',l='S', w='S', name='S.middleLeftDown', base='S', accents=['flourish.middleLeftDown2s'], comment='S simple flourish middle left downward'),
    'S.middleLeftUp': GD(g2='S', g1='S',l='S', w='S', name='S.middleLeftUp', base='S', accents=['flourish.middleLeftUp1s'], comment='S simple flourish middle left upwards'),
    'S.middleRightDown': GD(g2='S', g1='S',l='S', w='S', name='S.middleRightDown', base='S', accents=['flourish.middleRightDown1s'], comment='S simple flourish middle right downward'),
    'S.middleRightUp': GD(g2='S', g1='S',l='S', w='S', name='S.middleRightUp', base='S', accents=['flourish.middleRightUp2s'], comment='S simple flourish middle right upwards'),

    'T.bottomLeftDown': GD(g2='T', g1='T',l='T', w='T', name='T.bottomLeftDown', base='T', accents=['flourish.bottomLeftDown2x'], comment='T simple flourish bottom left downward'),
    'T.bottomLeftUp': GD(g2='T', g1='T',l='T', w='T', name='T.bottomLeftUp', base='T', accents=['flourish.bottomLeftUp1'], comment='T simple flourish bottom left upwards'),
    'T.bottomRightDown': GD(g2='T', g1='T',l='T', w='T', name='T.bottomRightDown', base='T', accents=['flourish.bottomRightDown2x'], comment='T simple flourish bottom right downward'),
    'T.bottomRightUp': GD(g2='T', g1='T',l='T', w='T', name='T.bottomRightUp', base='T', accents=['flourish.bottomRightUp1'], comment='T simple flourish bottom right upwards'),
    'T.topLeftUp': GD(g2='T', g1='T',l='T', w='T', name='T.topLeftUp', base='T', accents=['flourish.topLeftUp2s'], comment='T simple flourish top left upwards'),
    'T.topRightUp': GD(g2='T', g1='T',l='T', w='T', name='T.topRightUp', base='T', accents=['flourish.topRightUp2'], comment='T simple flourish top right upwards'),
    # Flourishes on the side, only #1
    'T.middleLeftDown': GD(g2='T', g1='T',l='T', w='T', name='T.middleLeftDown', base='T', accents=['flourish.middleLeftDown2s'], comment='T simple flourish middle left downward'),
    'T.middleLeftUp': GD(g2='T', g1='T',l='T', w='T', name='T.middleLeftUp', base='T', accents=['flourish.middleLeftUp1'], comment='T simple flourish middle left upwards'),
    'T.middleRightDown': GD(g2='T', g1='T',l='T', w='T', name='T.middleRightDown', base='T', accents=['flourish.middleRightDown1s'], comment='T simple flourish middle right downward'),
    'T.middleRightUp': GD(g2='T', g1='T',l='T', w='T', name='T.middleRightUp', base='T', accents=['flourish.middleRightUp1'], comment='T simple flourish middle right upwards'),

    'Thorn.bottomLeftDown': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.bottomLeftDown', base='Thorn', accents=['flourish.bottomLeftDown2x'], comment='Thorn simple flourish bottom left downward'),
    'Thorn.bottomLeftUp': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.bottomLeftUp', base='Thorn', accents=['flourish.bottomLeftUp2s'], comment='Thorn simple flourish bottom left upwards'),
    'Thorn.bottomRightDown': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.bottomRightDown', base='Thorn', accents=['flourish.bottomRightDown2x'], comment='Thorn simple flourish bottom right downward'),
    'Thorn.topLeftDown': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.topLeftDown', base='Thorn', accents=['flourish.topLeftDown1s'], comment='Thorn simple flourish top left downwards'),
    'Thorn.topLeftUp': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.topLeftUp', base='Thorn', accents=['flourish.topLeftUp2x'], comment='Thorn simple flourish top left upwards'),
    'Thorn.topRightUp': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.topRightUp', base='Thorn', accents=['flourish.topRightUp2x'], comment='Thorn simple flourish top right upwards'),
    # Flourishes on the side
    'Thorn.middleLeftDown': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.middleLeftDown', base='Thorn', accents=['flourish.middleLeftDown2s'], comment='ThornT simple flourish middle left downward'),
    'Thorn.middleLeftUp': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.middleLeftUp', base='Thorn', accents=['flourish.middleLeftUp1'], comment='Thorn simple flourish middle left upwards'),
    'Thorn.middleRightDown': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.middleRightDown', base='Thorn', accents=['flourish.middleRightDown1'], comment='Thorn simple flourish middle right downward'),
    'Thorn.middleRightUp': GD(g2='H', g1='Thorn', l='Thorn', w='Thorn', name='Thorn.middleRightUp', base='Thorn', accents=['flourish.middleRightUp2'], comment='Thorn simple flourish middle right upwards'),

    'U.bottomLeftDown': GD(g2='U', g1='U', l='U', w='U', name='U.bottomLeftDown', base='U', accents=['flourish.bottomLeftDown2s'], comment='U simple flourish bottom left downward'),
    'U.bottomRightDown': GD(g2='U', g1='U', l='U', w='U', name='U.bottomRightDown', base='U', accents=['flourish.bottomRightDown2'], comment='U simple flourish bottom right downward'),
    'U.topLeftDown': GD(g2='U', g1='U', l='U', w='U', name='U.topLeftDown', base='U', accents=['flourish.topLeftDown1s'], comment='U simple flourish top left downward'),
    'U.topLeftUp': GD(g2='U', g1='U', l='U', w='U', name='U.topLeftUp', base='U', accents=['flourish.topLeftUp2x'], comment='U simple flourish top left upwards'),
    'U.topRightDown': GD(g2='U', g1='U', l='U', w='U', name='U.topRightDown', base='U', accents=['flourish.topRightDown1s'], comment='U simple flourish top right downward'),
    'U.topRightUp': GD(g2='U', g1='U', l='U', w='U', name='U.topRightUp', base='U', accents=['flourish.topRightUp2x'], comment='U simple flourish top right upwards'),
    # Flourishes on the side
    'U.middleLeftDown': GD(g2='U', g1='U', l='U', w='U', name='U.middleLeftDown', base='U', accents=['flourish.middleLeftDown2s'], comment='U simple flourish middle left downward'),
    'U.middleLeftUp': GD(g2='U', g1='U', l='U', w='U', name='U.middleLeftUp', base='U', accents=['flourish.middleLeftUp1'], comment='U simple flourish middle left upwards'),
    'U.middleRightDown': GD(g2='U', g1='U', l='U', w='U', name='U.middleRightDown', base='U', accents=['flourish.middleRightDown1'], comment='U simple flourish middle right downward'),
    'U.middleRightUp': GD(g2='U', g1='U', l='U', w='U', name='U.middleRightUp', base='U', accents=['flourish.middleRightUp2s'], comment='U simple flourish middle right upwards'),

    'V.bottomLeftDown': GD(g2='V', g1='V', l='V', w='V', name='V.bottomLeftDown', base='V', accents=['flourish.bottomLeftDown2s'], comment='V simple flourish bottom left downward'),
    'V.bottomLeftUp': GD(g2='V', g1='V', l='V', w='V', name='V.bottomLeftUp', base='V', accents=['flourish.bottomLeftUp2sl'], comment='V simple flourish bottom left upward'),
    'V.bottomRightDown': GD(g2='V', g1='V', l='V', w='V', name='V.bottomRightDown', base='V', accents=['flourish.bottomRightDown2'], comment='V simple flourish bottom right downward'),
    'V.bottomRightUp': GD(g2='V', g1='V', l='V', w='V', name='V.bottomRightUp', base='V', accents=['flourish.bottomRightUp2sl'], comment='V simple flourish bottom right upward'),
    'V.topLeftDown': GD(g2='V', g1='V', l='V', w='V', name='V.topLeftDown', base='V', accents=['flourish.topLeftDown1'], comment='V simple flourish top left downward'),
    'V.topLeftUp': GD(g2='V', g1='V', l='V', w='V', name='V.topLeftUp', base='V', accents=['flourish.topLeftUp2x'], comment='V simple flourish top left upwards'),
    'V.topRightDown': GD(g2='V', g1='V', l='V', w='V', name='V.topRightDown', base='V', accents=['flourish.topRightDown1s'], comment='V simple flourish top right downward'),
    'V.topRightUp': GD(g2='V', g1='V', l='V', w='V', name='V.topRightUp', base='V', accents=['flourish.topRightUp2x'], comment='V simple flourish top right upwards'),
    # Flourishes on the side
    'V.middleLeftDown': GD(g2='V', g1='V', l='V', w='V', name='V.middleLeftDown', base='V', accents=['flourish.middleLeftDown1'], comment='V simple flourish middle left downward'),
    'V.middleLeftUp': GD(g2='V', g1='V', l='V', w='V', name='V.middleLeftUp', base='V', accents=['flourish.middleLeftUp2d'], comment='V simple flourish middle left upwards'),
    'V.middleRightDown': GD(g2='V', g1='V', l='V', w='V', name='V.middleRightDown', base='V', accents=['flourish.middleRightDown1'], comment='V simple flourish middle right downward'),

    'W.bottomLeftDown': GD(g2='W', g1='W', l='W', w='W', name='W.bottomLeftDown', base='W', accents=['flourish.bottomLeftDown2s'], comment='W simple flourish bottom left downward'),
    'W.bottomLeftUp': GD(g2='W', g1='W', l='W', w='W', name='W.bottomLeftUp', base='W', accents=['flourish.bottomLeftUp2sl'], comment='W simple flourish bottom left upward'),
    'W.bottomRightDown': GD(g2='W', g1='W', l='W', w='W', name='W.bottomRightDown', base='W', accents=['flourish.bottomRightDown2'], comment='W simple flourish bottom right downward'),
    'W.bottomRightUp': GD(g2='W', g1='W', l='W', w='W', name='W.bottomRightUp', base='W', accents=['flourish.bottomRightUp2sl'], comment='W simple flourish bottom right upward'),
    'W.topLeftDown': GD(g2='W', g1='W', l='W', w='W', name='W.topLeftDown', base='W', accents=['flourish.topLeftDown1'], comment='W simple flourish top left downward'),
    'W.topLeftUp': GD(g2='W', g1='W', l='W', w='W', name='W.topLeftUp', base='W', accents=['flourish.topLeftUp2x'], comment='W simple flourish top left upwards'),
    'W.topRightDown': GD(g2='W', g1='W', l='W', w='W', name='W.topRightDown', base='W', accents=['flourish.topRightDown1s'], comment='W simple flourish top right downward'),
    'W.topRightUp': GD(g2='W', g1='W', l='W', w='W', name='W.topRightUp', base='W', accents=['flourish.topRightUp2x'], comment='W simple flourish top right upwards'),
    # Flourishes on the side, only #1
    'W.middleLeftDown': GD(g2='W', g1='W', l='W', w='W', name='W.middleLeftDown', base='W', accents=['flourish.middleLeftDown1'], comment='W simple flourish middle left downward'),
    'W.middleLeftUp': GD(g2='W', g1='W', l='W', w='W', name='W.middleLeftUp', base='W', accents=['flourish.middleLeftUp2d'], comment='W simple flourish middle left upwards'),
    'W.middleRightDown': GD(g2='W', g1='W', l='W', w='W', name='W.middleRightDown', base='W', accents=['flourish.middleRightDown1'], comment='W simple flourish middle right downward'),

    'X.bottomLeftDown': GD(g2='X', g1='X', l='X', w='X', name='X.bottomLeftDown', base='X', accents=['flourish.bottomLeftDown2x'], comment='X simple flourish bottom left downward'),
    'X.bottomLeftUp': GD(g2='X', g1='X', l='X', w='X', name='X.bottomLeftUp', base='X', accents=['flourish.bottomLeftUp1'], comment='X simple flourish bottom left upwards'),
    'X.bottomRightDown': GD(g2='X', g1='X', l='X', w='X', name='X.bottomRightDown', base='X', accents=['flourish.bottomRightDown2x'], comment='X simple flourish bottom right downward'),
    'X.bottomRightUp': GD(g2='X', g1='X', l='X', w='X', name='X.bottomRightUp', base='X', accents=['flourish.bottomRightUp1'], comment='X simple flourish bottom right upwards'),
    'X.topLeftDown': GD(g2='X', g1='X', l='X', w='X', name='X.topLeftDown', base='X', accents=['flourish.topLeftDown1'], comment='X simple flourish top left downward'),
    'X.topLeftUp': GD(g2='X', g1='X', l='X', w='X', name='X.topLeftUp', base='X', accents=['flourish.topLeftUp2x'], comment='X simple flourish top left upwards'),
    'X.topRightDown': GD(g2='X', g1='X', l='X', w='X', name='X.topRightDown', base='X', accents=['flourish.topRightDown1s'], comment='X simple flourish top right downward'),
    'X.topRightUp': GD(g2='X', g1='X', l='X', w='X', name='X.topRightUp', base='X', accents=['flourish.topRightUp2x'], comment='X simple flourish top right upwards'),
    # Flourishes on top-right and bottom-left
    'X.middleLeftDown': GD(g2='X', g1='X', l='X', w='X', name='X.middleLeftDown', base='X', accents=['flourish.middleLeftDown1d'], comment='X simple flourish middle left downward'),
    'X.middleLeftUp': GD(g2='X', g1='X', l='X', w='X', name='X.middleLeftUp', base='X', accents=['flourish.middleLeftUp1d'], comment='X simple flourish middle left upwards'),
    'X.middleRightDown': GD(g2='X', g1='X', l='X', w='X', name='X.middleRightDown', base='X', accents=['flourish.middleRightDown1d'], comment='X simple flourish middle right downward'),
    'X.middleRightUp': GD(g2='X', g1='X', l='X', w='X', name='X.middleRightUp', base='X', accents=['flourish.middleRightUp1d'], comment='X simple flourish middle right upwards'),

    'Y.bottomLeftDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.bottomLeftDown', base='Y', accents=['flourish.bottomLeftDown2x'], comment='Y simple flourish bottom left downward'),
    'Y.bottomLeftUp': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.bottomLeftUp', base='Y', accents=['flourish.bottomLeftUp1'], comment='Y simple flourish bottom left upwards'),
    'Y.bottomRightDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.bottomRightDown', base='Y', accents=['flourish.bottomRightDown2x'], comment='Y simple flourish bottom right downward'),
    'Y.bottomRightUp': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.bottomRightUp', base='Y', accents=['flourish.bottomRightUp1'], comment='Y simple flourish bottom right upwards'),
    'Y.topLeftDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.topLeftDown', base='Y', accents=['flourish.topLeftDown1'], comment='Y simple flourish top left downward'),
    'Y.topLeftUp': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.topLeftUp', base='Y', accents=['flourish.topLeftUp2x'], comment='Y simple flourish top left upwards'),
    'Y.topRightDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.topRightDown', base='Y', accents=['flourish.topRightDown1s'], comment='Y simple flourish top right downward'),
    'Y.topRightUp': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.topRightUp', base='Y', accents=['flourish.topRightUp2x'], comment='Y simple flourish top right upwards'),
    # Flourishes on the side, only #1    'Y.middleLeftDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.middleLeftDown', base='Y', accents=['flourish.middleLeftDown1'], comment='Y simple flourish middle left downward'),
    'Y.middleLeftUp': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.middleLeftUp', base='Y', accents=['flourish.middleLeftUp1d'], comment='Y simple flourish middle left diagonal upwards'),
    'Y.middleRightDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.middleRightDown', base='Y', accents=['flourish.middleRightDown1'], comment='Y simple flourish middle right downward'),
    'Y.middleRightUp': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.middleRightUp', base='Y', accents=['flourish.middleRightUp2s'], comment='Y simple flourish middle right downward'),
    'Y.middleLeftDown': GD(g2='Y', g1='Y', l='Y', w='Y', name='Y.middleLeftDown', base='Y', accents=['flourish.middleLeftDown1'], comment='Y simple flourish middle left downward'),

    #'Z.topLeftDown': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.topLeftDown', base='Z', accents=['flourish.topLeftDown1s'], comment='Z simple flourish top left down'),
    'Z.topRightDown': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.topRightDown', base='Z', accents=['flourish.topRightDown1s'], comment='Z simple flourish top right down'),
    'Z.topLeftUp': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.topLeftUp', base='Z', accents=['flourish.topLeftUp2x'], comment='Z simple flourish top left upwards'),
    'Z.topRightUp': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.topRightUp', base='Z', accents=['flourish.topRightUp2x'], comment='Z simple flourish top right upwards'),
    'Z.bottomLeftUp': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.bottomLeftUp', base='Z', accents=['flourish.bottomLeftUp1s'], comment='Z simple flourish bottom left up'),
    #'Z.bottomRightUp': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.bottomRightUp', base='Z', accents=['flourish.bottomRightUp1s'], comment='Z simple flourish bottom right up'),
    'Z.bottomLeftDown': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.bottomLeftDown', base='Z', accents=['flourish.bottomLeftDown2x'], comment='Z simple flourish bottom left downward'),
    'Z.bottomRightDown': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.bottomRightDown', base='Z', accents=['flourish.bottomRightDown2x'], comment='Z simple flourish bottom right downward'),
    # Flourishes on the side
    'Z.middleLeftUp': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.middleLeftUp', base='Z', accents=['flourish.middleLeftUp1'], comment='Z simple flourish middle left upwards'),
    'Z.middleRightUp': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.middleRightUp', base='Z', accents=['flourish.middleRightUp2'], comment='Z simple flourish middle right upwards'),
    'Z.middleLeftDown': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.middleLeftDown', base='Z', accents=['flourish.middleLeftDown2'], comment='Z simple flourish middle left downward'),
    'Z.middleRightDown': GD(g2='Z', g1='Z', l='Z', w='Z', name='Z.middleRightDown', base='Z', accents=['flourish.middleRightDown1'], comment='Z simple flourish middle right downward'),

    'OE.topLeftUp': GD(g2='O', g1='E', l='OE', w='OE', name='OE.topLeftUp', base='OE', accents=['flourish.topLeftUp2s'], comment='OE simple flourish top left upwards'),
    'OE.bottomLeftDown': GD(g2='O', g1='E', l='OE', w='OE', name='OE.bottomLeftDown', base='OE', accents=['flourish.bottomLeftDown2xs'], comment='OE simple flourish bottom left downward'),
    'OE.topRightUp': GD(g2='O', g1='E', l='OE', w='OE', name='OE.topRightUp', base='OE', accents=['flourish.topRightUp2'], comment='OE simple flourish top right upwards'),
    'OE.bottomRightDown': GD(g2='O', g1='E', l='OE', w='OE', name='OE.bottomRightDown', base='OE', accents=['flourish.bottomRightDown2'], comment='OE simple flourish bottom right downward'),
    'OE.middleLeftUp': GD(g2='O', g1='E', l='OE', w='OE', name='OE.middleLeftUp', base='OE', accents=['flourish.middleLeftUp1s'], comment='OE simple flourish middle left upwards'),
    'OE.middleLeftDown': GD(g2='O', g1='E', l='OE', w='OE', name='OE.middleLeftDown', base='OE', accents=['flourish.middleLeftDown2'], comment='OE simple flourish middle left downward'),
    'OE.middleRightUp': GD(g2='O', g1='E', l='OE', w='OE', name='OE.middleRightUp', base='OE', accents=['flourish.middleRightUp1'], comment='OE simple flourish middle right upwards'),
    'OE.middleRightDown': GD(g2='O', g1='E', l='OE', w='OE', name='OE.middleRightDown', base='OE', accents=['flourish.middleRightDown1s'], comment='OE simple flourish middle right downward'),

    'AE.topRightUp': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.topRightUp', base='AE', accents=['flourish.topRightUp2'], comment='AE simple flourish top right upwards'),
    'AE.bottomRightDown': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.bottomRightDown', base='AE', accents=['flourish.bottomRightDown2'], comment='AE simple flourish bottom right downward'),
    'AE.topLeftUp': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.topLeftUp', base='AE', accents=['flourish.topLeftUp2s'], comment='AE simple flourish top left upwards'),
    'AE.topLeftDown': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.topLeftDown', base='AE', accents=['flourish.topLeftDown2sl'], comment='AE simple flourish top left upwards'),
    'AE.bottomLeftUp': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.bottomLeftUp', base='AE', accents=['flourish.bottomLeftUp1'], comment='AEsimple flourish bottom left upwards'),
    'AE.middleLeftUp': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.middleLeftUp', base='AE', accents=['flourish.middleLeftUp1'], comment='AE simple flourish middle left upwards'),
    'AE.bottomLeftDown': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.bottomLeftDown', base='AE', accents=['flourish.bottomLeftDown2x'], comment='AE simple flourish bottom left downward'),
    'AE.middleRightUp': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.middleRightUp', base='AE', accents=['flourish.middleRightUp1'], comment='AE simple flourish middle right upwards'),
    'AE.middleRightDown': GD(g2='AE', g1='E', l='AE', w='AE', name='AE.middleRightDown', base='AE', accents=['flourish.middleRightDown1s'], comment='AE simple flourish middle right downward'),

    # Small caps

    'A.bottomLeftDown.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.bottomLeftDown.sc', base='A.sc', accents=['flourish.bottomLeftDown2x'], comment='A simple flourish bottom left downward'),
    'A.bottomLeftUp.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.bottomLeftUp.sc', base='A.sc', accents=['flourish.bottomLeftUp1'], comment='A simple flourish bottom left upwards'),
    'A.bottomRightDown.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.bottomRightDown.sc', base='A.sc', accents=['flourish.bottomRightDown2x'], comment='A simple flourish bottom right downward'),
    'A.bottomRightUp.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.bottomRightUp.sc', base='A.sc', accents=['flourish.bottomRightUp1'], comment='A simple flourish bottom right upwards'),
    'A.topLeftDown.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.topLeftDown.sc', base='A.sc', accents=['flourish.topLeftDown2sl'], comment='A simple flourish top left upwards'),
    'A.topLeftUp.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.topLeftUp.sc', base='A.sc', accents=['flourish.topLeftUp2s'], comment='A simple flourish top left upwards'),
    'A.topRightDown.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.topRightDown.sc', base='A.sc', accents=['flourish.topRightDown2sl'], comment='A simple flourish top right upwards'),
    'A.topRightUp.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.topRightUp.sc', base='A.sc', accents=['flourish.topRightUp2'], comment='A simple flourish top right upwards'),
     # Flourishes on the side, only #1
    'A.middleLeftUp.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.middleLeftUp.sc', base='A.sc', accents=['flourish.middleLeftUp1s'], comment='A simple flourish middle left upwards'),
    'A.middleRightDown.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.middleRightDown.sc', base='A.sc', accents=['flourish.middleRightDown1d'], comment='A simple flourish middle right downward'),
    'A.middleRightUp.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='A.middleRightUp.sc', base='A.sc', accents=['flourish.middleRightUp1'], comment='A simple flourish middle right upwards'),

    'B.bottomLeftDown.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.bottomLeftDown.sc', base='B.sc', accents=['flourish.bottomLeftDown2x'], comment='B simple flourish bottom left downward'),
    'B.bottomLeftUp.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.bottomLeftUp.sc', base='B.sc', accents=['flourish.bottomLeftUp1s'], comment='B simple flourish bottom left upwards'),
    'B.bottomRightDown.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.bottomRightDown.sc', base='B.sc', accents=['flourish.bottomRightDown2s'], comment='B simple flourish bottom right downward'),
    'B.topLeftDown.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.topLeftDown.sc', base='B.sc', accents=['flourish.topLeftDown1s'], comment='B simple flourish top left downward'),
    'B.topLeftUp.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.topLeftUp.sc', base='B.sc', accents=['flourish.topLeftUp2x'], comment='B simple flourish top left upwards'),
    'B.topRightUp.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.topRightUp.sc', base='B.sc', accents=['flourish.topRightUp2'], comment='B simple flourish top right upwards'),
    # Flourishes on the side
    'B.middleLeftDown.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.middleLeftDown.sc', base='B.sc', accents=['flourish.middleLeftDown1'], comment='B simple flourish middle left downward'),
    'B.middleLeftUp.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.middleLeftUp.sc', base='B.sc', accents=['flourish.middleLeftUp1s'], comment='B simple flourish middle left upwards'),
    'B.middleRightDown.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.middleRightDown.sc', base='B.sc', accents=['flourish.middleRightDown1s'], comment='B simple flourish middle right downward'),
    'B.middleRightUp.sc': GD(g2='H.sc', g1='B.sc', l='B.sc', w='B.sc', name='B.middleRightUp.sc', base='B.sc', accents=['flourish.middleRightUp2'], comment='B simple flourish middle right upwards'),

    'C.bottomLeftDown.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.bottomLeftDown.sc', base='C.sc', accents=['flourish.bottomLeftDown2s'], comment='C simple flourish bottom left downward'),
    'C.bottomRightDown.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.bottomRightDown.sc', base='C.sc', accents=['flourish.bottomRightDown1'], comment='C simple flourish bottom right downward'),
    'C.topLeftUp.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.topLeftUp.sc', base='C.sc', accents=['flourish.topLeftUp2s'], comment='C simple flourish top left upwards'),
    'C.topRightUp.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.topRightUp.sc', base='C.sc', accents=['flourish.topRightUp1'], comment='C simple flourish top right upwards'),
    # Flourishes on the side
    'C.middleLeftDown.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.middleLeftDown.sc', base='C.sc', accents=['flourish.middleLeftDown1'], comment='C simple flourish middle left downward'),
    'C.middleLeftUp.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.middleLeftUp.sc', base='C.sc', accents=['flourish.middleLeftUp1s'], comment='C simple flourish middle left upwards'),
    'C.middleRightDown.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.middleRightDown.sc', base='C.sc', accents=['flourish.middleRightDown1'], comment='C simple flourish middle right downward'),
    'C.middleRightUp.sc': GD(g2='O.sc', g1='C.sc', l='C.sc', w='C.sc', name='C.middleRightUp.sc', base='C.sc', accents=['flourish.middleRightUp1s'], comment='C simple flourish middle right upwards'),

    'D.bottomLeftDown.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.bottomLeftDown.sc', base='D.sc', accents=['flourish.bottomLeftDown2x'], comment='D simple flourish bottom left downward'),
    'D.bottomLeftUp.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.bottomLeftUp.sc', base='D.sc', accents=['flourish.bottomLeftUp2s'], comment='D simple flourish bottom left upwards'),
    'D.bottomRightDown.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.bottomRightDown.sc', base='D.sc', accents=['flourish.bottomRightDown2'], comment='D simple flourish bottom right downward'),
    'D.topLeftDown.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.topLeftDown.sc', base='D.sc', accents=['flourish.topLeftDown1s'], comment='D simple flourish top left downward'),
    'D.topLeftUp.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.topLeftUp.sc', base='D.sc', accents=['flourish.topLeftUp2x'], comment='D simple flourish top left upwards'),
    'D.topRightUp.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.topRightUp.sc', base='D.sc', accents=['flourish.topRightUp2'], comment='D simple flourish top right upwards'),
    # Flourishes on the side
    'D.middleLeftDown.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.middleLeftDown.sc', base='D.sc', accents=['flourish.middleLeftDown1'], comment='D simple flourish middle left downward'),
    'D.middleLeftUp.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.middleLeftUp.sc', base='D.sc', accents=['flourish.middleLeftUp1s'], comment='D simple flourish middle left upwards'),
    'D.middleRightDown.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.middleRightDown.sc', base='D.sc', accents=['flourish.middleRightDown1s'], comment='D simple flourish middle right downward'),
    'D.middleRightUp.sc': GD(g2='H.sc', g1='O.sc', l='D.sc', w='D.sc', name='D.middleRightUp.sc', base='D.sc', accents=['flourish.middleRightUp2'], comment='D simple flourish middle right upwards'),

    'E.bottomLeftDown.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.bottomLeftDown.sc', base='E.sc', accents=['flourish.bottomLeftDown2x'], comment='E simple flourish bottom left downward'),
    'E.bottomLeftUp.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.bottomLeftUp.sc', base='E.sc', accents=['flourish.bottomLeftUp1s'], comment='E simple flourish bottom left upwards'),
    'E.bottomRightDown.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.bottomRightDown.sc', base='E.sc', accents=['flourish.bottomRightDown2'], comment='E simple flourish bottom right downward'),
    'E.topLeftDown.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.topLeftDown.sc', base='E.sc', accents=['flourish.topLeftDown1s'], comment='E simple flourish top left downward'),
    'E.topLeftUp.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.topLeftUp.sc', base='E.sc', accents=['flourish.topLeftUp2x'], comment='E simple flourish top left upwards'),
    'E.topRightUp.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.topRightUp.sc', base='E.sc', accents=['flourish.topRightUp2'], comment='E simple flourish top right upwards'),
    # Flourishes on the side
    'E.middleLeftDown.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.middleLeftDown.sc', base='E.sc', accents=['flourish.middleLeftDown1'], comment='E simple flourish middle left downward'),
    'E.middleLeftUp.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.middleLeftUp.sc', base='E.sc', accents=['flourish.middleLeftUp1s'], comment='E simple flourish middle left upwards'),
    'E.middleRightDown.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.middleRightDown.sc', base='E.sc', accents=['flourish.middleRightDown1s'], comment='E simple flourish middle right downward'),
    'E.middleRightUp.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='E.middleRightUp.sc', base='E.sc', accents=['flourish.middleRightUp1'], comment='E simple flourish middle right upwards'),

    'F.bottomLeftDown.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.bottomLeftDown.sc', base='F.sc', accents=['flourish.bottomLeftDown2x'], comment='F simple flourish bottom left downward'),
    'F.bottomLeftUp.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.bottomLeftUp.sc', base='F.sc', accents=['flourish.bottomLeftUp2s'], comment='F simple flourish bottom left upwards'),
    'F.bottomRightDown.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.bottomRightDown.sc', base='F.sc', accents=['flourish.bottomRightDown2x'], comment='F simple flourish bottom right downward'),
    'F.topLeftDown.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.topLeftDown.sc', base='F.sc', accents=['flourish.topLeftDown1s'], comment='F simple flourish top left downward'),
    'F.topLeftUp.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.topLeftUp.sc', base='F.sc', accents=['flourish.topLeftUp2x'], comment='F simple flourish top left upwards'),
    'F.topRightUp.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.topRightUp.sc', base='F.sc', accents=['flourish.topRightUp2'], comment='F simple flourish top right upwards'),
    # Flourishes on the side, no simple way to connect to right side.
    'F.middleLeftDown.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.middleLeftDown.sc', base='F.sc', accents=['flourish.middleLeftDown1'], comment='F simple flourish middle left downward'),
    'F.middleLeftUp.sc': GD(g2='H.sc', g1='F.sc', l='F.sc', w='F.sc', name='F.middleLeftUp.sc', base='F.sc', accents=['flourish.middleLeftUp1s'], comment='F simple flourish middle left upwards'),

    'G.bottomLeftDown.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.bottomLeftDown.sc', base='G.sc', accents=['flourish.bottomLeftDown2s'], comment='G simple flourish bottom left downward'),
    'G.bottomRightDown.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.bottomRightDown.sc', base='G.sc', accents=['flourish.bottomRightDown1'], comment='G simple flourish bottom right downward'),
    'G.topLeftUp.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.topLeftUp.sc', base='G.sc', accents=['flourish.topLeftUp2s'], comment='G simple flourish top left upwards'),
    'G.topRightUp.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.topRightUp.sc', base='G.sc', accents=['flourish.topRightUp1'], comment='G simple flourish top right upwards'),
    # Flourishes on the side
    'G.middleLeftDown.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.middleLeftDown.sc', base='G.sc', accents=['flourish.middleLeftDown1'], comment='G simple flourish middle left downward'),
    'G.middleLeftUp.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.middleLeftUp.sc', base='G.sc', accents=['flourish.middleLeftUp1s'], comment='G simple flourish middle left upwards'),
    'G.middleRightDown.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.middleRightDown.sc', base='G.sc', accents=['flourish.middleRightDown1s'], comment='G simple flourish middle right downward'),
    'G.middleRightUp.sc': GD(g2='O.sc', g1='G.sc', l='G.sc', w='G.sc', name='G.middleRightUp.sc', base='G.sc', accents=['flourish.middleRightUp1'], comment='G simple flourish middle right upwards'),

    'H.bottomLeftDown.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.bottomLeftDown.sc', base='H.sc', accents=['flourish.bottomLeftDown2x'], comment='H simple flourish bottom left downward'),
    'H.bottomLeftUp.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.bottomLeftUp.sc', base='H.sc', accents=['flourish.bottomLeftUp1s'], comment='H simple flourish bottom left upwards'),
    'H.bottomRightDown.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.bottomRightDown.sc', base='H.sc', accents=['flourish.bottomRightDown2x'], comment='H simple flourish bottom right downward'),
    'H.bottomRightUp.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.bottomRightUp.sc', base='H.sc', accents=['flourish.bottomRightUp1s'], comment='H simple flourish bottom right upwards'),
    'H.topLeftDown.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.topLeftDown.sc', base='H.sc', accents=['flourish.topLeftDown1s'], comment='H simple flourish top left downward'),
    'H.topLeftUp.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.topLeftUp.sc', base='H.sc', accents=['flourish.topLeftUp2x'], comment='H simple flourish top left upwards'),
    'H.topRightDown.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.topRightDown.sc', base='H.sc', accents=['flourish.topRightDown1s'], comment='H simple flourish top right downward'),
    'H.topRightUp.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.topRightUp.sc', base='H.sc', accents=['flourish.topRightUp2x'], comment='H simple flourish top right upwards'),
    # Flourishes on the side
    'H.middleLeftDown.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.middleLeftDown.sc', base='H.sc', accents=['flourish.middleLeftDown1'], comment='H simple flourish middle left downward'),
    'H.middleLeftUp.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.middleLeftUp.sc', base='H.sc', accents=['flourish.middleLeftUp1s'], comment='H simple flourish middle left upwards'),
    'H.middleRightDown.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.middleRightDown.sc', base='H.sc', accents=['flourish.middleRightDown1s'], comment='H simple flourish middle right downward'),
    'H.middleRightUp.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', w='H.sc', name='H.middleRightUp.sc', base='H.sc', accents=['flourish.middleRightUp1'], comment='H simple flourish middle right upwards'),

    'I.bottomLeftDown.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.bottomLeftDown.sc', base='I.sc', accents=['flourish.bottomLeftDown2x'], comment='I simple flourish bottom left downward'),
    'I.bottomLeftUp.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.bottomLeftUp.sc', base='I.sc', accents=['flourish.bottomLeftUp2s'], comment='I simple flourish bottom left upwards'),
    'I.bottomRightDown.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.bottomRightDown.sc', base='I.sc', accents=['flourish.bottomRightDown2x'], comment='I simple flourish bottom right downward'),    
    'I.bottomRightUp.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.bottomRightUp.sc', base='I.sc', accents=['flourish.bottomRightUp1s'], comment='I simple flourish bottom right upwards'),
    'I.topLeftDown.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.topLeftDown.sc', base='I.sc', accents=['flourish.topLeftDown1s'], comment='I simple flourish top left downward'),
    'I.topLeftUp.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.topLeftUp.sc', base='I.sc', accents=['flourish.topLeftUp2x'], comment='I simple flourish top left upwards'),
    'I.topRightDown.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.topRightDown.sc', base='I.sc', accents=['flourish.topRightDown1s'], comment='I simple flourish top right downward'),
    'I.topRightUp.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.topRightUp.sc', base='I.sc', accents=['flourish.topRightUp2x'], comment='I simple flourish top right upwards'),
    # Flourishes on the side
    'I.middleLeftDown.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.middleLeftDown.sc', base='I.sc', accents=['flourish.middleLeftDown1'], comment='I simple flourish middle left downward'),
    'I.middleLeftUp.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.middleLeftUp.sc', base='I.sc', accents=['flourish.middleLeftUp1s'], comment='I simple flourish middle left upwards'),
    'I.middleRightDown.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.middleRightDown.sc', base='I.sc', accents=['flourish.middleRightDown1s'], comment='I simple flourish middle right downward'),
    'I.middleRightUp.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='I.middleRightUp.sc', base='I.sc', accents=['flourish.middleRightUp1'], comment='I simple flourish middle right upwards'),

    'J.bottomLeftDown.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.bottomLeftDown.sc', base='J.sc', accents=['flourish.bottomLeftDown2s'], comment='J simple flourish bottom left downward'),
    'J.bottomLeftUp.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.bottomLeftUp.sc', base='J.sc', accents=['flourish.bottomLeftUp1'], comment='J simple flourish bottom left upwards'),
    'J.bottomRightDown.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.bottomRightDown.sc', base='J.sc', accents=['flourish.bottomRightDown2s'], comment='J simple flourish bottom left downward'),
    'J.topLeftDown.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.topLeftDown.sc', base='J.sc', accents=['flourish.topLeftDown1s'], comment='J simple flourish top left downward'),
    'J.topLeftUp.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.topLeftUp.sc', base='J.sc', accents=['flourish.topLeftUp2x'], comment='J simple flourish top left upwards'),
    'J.topRightDown.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.topRightDown.sc', base='J.sc', accents=['flourish.topRightDown1s'], comment='J simple flourish top right downward'),
    'J.topRightUp.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.topRightUp.sc', base='J.sc', accents=['flourish.topRightUp2x'], comment='J simple flourish top right upwards'),
    # Flourishes on the side
    'J.middleLeftDown.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.middleLeftDown.sc', base='J.sc', accents=['flourish.middleLeftDown1'], comment='J simple flourish middle left downward'),
    'J.middleLeftUp.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.middleLeftUp.sc', base='J.sc', accents=['flourish.middleLeftUp1s'], comment='J simple flourish middle left upwards'),
    'J.middleRightDown.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.middleRightDown.sc', base='J.sc', accents=['flourish.middleRightDown1s'], comment='J simple flourish middle right downward'),
    'J.middleRightUp.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='J.middleRightUp.sc', base='J.sc', accents=['flourish.middleRightUp1'], comment='J simple flourish middle right upwards'),

    'J.base.bottomLeftDown.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.bottomLeftDown.sc', base='J.base.sc', accents=['flourish.bottomLeftDown2s'], comment='J simple flourish bottom left downward'),
    'J.base.bottomRightDown.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.bottomRightDown.sc', base='J.base.sc', accents=['flourish.bottomRightDown2s'], comment='J simple flourish bottom right downward'),
    'J.base.topLeftDown.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.topLeftDown.sc', base='J.base.sc', accents=['flourish.topLeftDown1s'], comment='J simple flourish top left downward'),
    'J.base.topLeftUp.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.topLeftUp.sc', base='J.base.sc', accents=['flourish.topLeftUp2xs'], comment='J simple flourish top left upwards'),
    'J.base.topRightDown.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.topRightDown.sc', base='J.base.sc', accents=['flourish.topRightDown1s'], comment='J simple flourish top right downward'),
    'J.base.topRightUp.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.topRightUp.sc', base='J.base.sc', accents=['flourish.topRightUp2xs'], comment='J simple flourish top right upwards'),
    # Flourishes on the side
    'J.base.middleLeftDown.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.middleLeftDown.sc', base='J.base.sc', accents=['flourish.middleLeftDown2s'], comment='J simple flourish middle left downward'),
    'J.base.middleLeftUp.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.middleLeftUp.sc', base='J.base.sc', accents=['flourish.middleLeftUp1'], comment='J simple flourish middle left upwards'),
    'J.base.middleRightDown.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.middleRightDown.sc', base='J.base.sc', accents=['flourish.middleRightDown1'], comment='J simple flourish middle right downward'),
    'J.base.middleRightUp.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='J.base.middleRightUp.sc', base='J.base.sc', accents=['flourish.middleRightUp1s'], comment='J simple flourish middle right upwards'),

    'K.bottomLeftDown.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.bottomLeftDown.sc', base='K.sc', accents=['flourish.bottomLeftDown2x'], comment='K simple flourish bottom left downward'),
    'K.bottomLeftUp.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.bottomLeftUp.sc', base='K.sc', accents=['flourish.bottomLeftUp1s'], comment='K simple flourish bottom left upwards'),
    'K.bottomRightDown.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.bottomRightDown.sc', base='K.sc', accents=['flourish.bottomRightDown2x'], comment='K simple flourish bottom right downward'),
    'K.bottomRightUp.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.bottomRightUp.sc', base='K.sc', accents=['flourish.bottomRightUp1s'], comment='K simple flourish bottom right upwards'),
    'K.topLeftDown.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.topLeftDown.sc', base='K.sc', accents=['flourish.topLeftDown1'], comment='K simple flourish top left downward'),
    'K.topLeftUp.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.topLeftUp.sc', base='K.sc', accents=['flourish.topLeftUp2x'], comment='K simple flourish top left upwards'),
    'K.topRightDown.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.topRightDown.sc', base='K.sc', accents=['flourish.topRightDown1s'], comment='K simple flourish top right downward'),
    'K.topRightUp.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.topRightUp.sc', base='K.sc', accents=['flourish.topRightUp2x'], comment='K simple flourish top right upwards'),
    # Flourishes on left side and top-right
    'K.middleLeftDown.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.middleLeftDown.sc', base='K.sc', accents=['flourish.middleLeftDown2s'], comment='K simple flourish middle left downward'),
    'K.middleLeftUp.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.middleLeftUp.sc', base='K.sc', accents=['flourish.middleLeftUp1s'], comment='K simple flourish middle left upwards'),
    'K.middleRightDown.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.middleRightDown.sc', base='K.sc', accents=['flourish.middleRightDown1d'], comment='M simple flourish middle right downward'),
    'K.middleRightUp.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', w='K.sc', name='K.middleRightUp.sc', base='K.sc', accents=['flourish.middleRightUp1d'], comment='M simple flourish middle right upwards'),

    # Too much /P 'L.topRightDown'
    'L.bottomLeftDown.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.bottomLeftDown.sc', base='L.sc', accents=['flourish.bottomLeftDown2x'], smallTrackRight=0, comment='L simple flourish bottom left downward'),
    'L.bottomLeftUp.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.bottomLeftUp.sc', base='L.sc', accents=['flourish.bottomLeftUp2s'], smallTrackRight=0, comment='L simple flourish bottom left upwards'),
    'L.bottomRightDown.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.bottomRightDown.sc', base='L.sc', accents=['flourish.bottomRightDown2'], smallTrackRight=0, comment='L simple flourish bottom right downward'),
    'L.topLeftDown.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.topLeftDown.sc', base='L.sc', accents=['flourish.topLeftDown1s'], smallTrackRight=0, comment='L simple flourish top left downward'),
    'L.topLeftUp.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.topLeftUp.sc', base='L.sc', accents=['flourish.topLeftUp2x'], smallTrackRight=0, comment='L simple flourish top left upwards'),
    'L.topRightUp.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.topRightUp.sc', base='L.sc', accents=['flourish.topRightUp2x'], smallTrackRight=0, comment='L simple flourish top right upwards'),
    # Flourishes on the side
    'L.middleLeftDown.sc': GD(g2='H.sc', g1='L.sc', l='H.sc', w='L.sc', name='L.middleLeftDown.sc', base='L.sc', accents=['flourish.middleLeftDown1'], smallTrackRight=0, comment='L simple flourish middle left downward'),
    'L.middleLeftUp.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.middleLeftUp.sc', base='L.sc', accents=['flourish.middleLeftUp1s'], smallTrackRight=0, comment='L simple flourish middle left upwards'),
    'L.middleRightUp.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='L.middleRightUp.sc', base='L.sc', accents=['flourish.middleRightUp1s'], smallTrackRight=0, comment='L simple flourish middle right upwards'),

    'M.bottomLeftDown.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.bottomLeftDown.sc', base='M.sc', accents=['flourish.bottomLeftDown2xs'], comment='M simple flourish bottom left downward'),
    'M.bottomLeftUp.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.bottomLeftUp.sc', base='M.sc', accents=['flourish.bottomLeftUp1s'], comment='M simple flourish bottom left upwards'),
    'M.bottomRightDown.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.bottomRightDown.sc', base='M.sc', accents=['flourish.bottomRightDown2x'], comment='M simple flourish bottom right downward'),
    'M.bottomRightUp.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.bottomRightUp.sc', base='M.sc', accents=['flourish.bottomRightUp1s'], comment='M simple flourish bottom right upwards'),
    'M.topLeftDown.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.topLeftDown.sc', base='M.sc', accents=['flourish.topLeftDown1s'], comment='M simple flourish top left downward'),
    'M.topLeftUp.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.topLeftUp.sc', base='M.sc', accents=['flourish.topLeftUp2xs'], comment='M simple flourish top left upwards'),
    'M.topRightDown.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.topRightDown.sc', base='M.sc', accents=['flourish.topRightDown1s'], comment='M simple flourish top right downward'),
    'M.topRightUp.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.topRightUp.sc', base='M.sc', accents=['flourish.topRightUp2xs'], comment='M simple flourish top right upwards'),
    # Flourishes on the side
    'M.middleLeftDown.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.middleLeftDown.sc', base='M.sc', accents=['flourish.middleLeftDown1'], comment='M simple flourish middle left downward'),
    'M.middleLeftUp.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.middleLeftUp.sc', base='M.sc', accents=['flourish.middleLeftUp1s'], comment='M simple flourish middle left upwards'),
    'M.middleRightDown.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.middleRightDown.sc', base='M.sc', accents=['flourish.middleRightDown1s'], comment='M simple flourish middle right downward'),
    'M.middleRightUp.sc': GD(g2='N.sc', g1='H.sc', l='M.sc', w='M.sc', name='M.middleRightUp.sc', base='M.sc', accents=['flourish.middleRightUp2s'], comment='M simple flourish middle right upwards'),

    'N.bottomLeftDown.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.bottomLeftDown.sc', base='N.sc', accents=['flourish.bottomLeftDown2xs'], comment='N simple flourish bottom left downward'),
    'N.bottomLeftUp.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.bottomLeftUp.sc', base='N.sc', accents=['flourish.bottomLeftUp2s'], comment='N simple flourish bottom left upwards'),
    'N.bottomRightDown.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.bottomRightDown.sc', base='N.sc', accents=['flourish.bottomRightDown2s'], comment='N simple flourish bottom right downward'),
    'N.topLeftDown.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.topLeftDown.sc', base='N.sc', accents=['flourish.topLeftDown1s'], comment='N simple flourish top left downward'),
    'N.topLeftUp.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.topLeftUp.sc', base='N.sc', accents=['flourish.topLeftUp2xs'], comment='N simple flourish top left upwards'),
    'N.topRightDown.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.topRightDown.sc', base='N.sc', accents=['flourish.topRightDown1s'], comment='N simple flourish top right downward'),
    'N.topRightUp.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.topRightUp.sc', base='N.sc', accents=['flourish.topRightUp2x'], comment='N simple flourish top right upwards'),
    # Flourishes on the side
    'N.middleLeftDown.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.middleLeftDown.sc', base='N.sc', accents=['flourish.middleLeftDown1'], comment='N simple flourish middle left downward'),
    'N.middleLeftUp.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.middleLeftUp.sc', base='N.sc', accents=['flourish.middleLeftUp1s'], comment='N simple flourish middle left upwards'),
    'N.middleRightDown.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.middleRightDown.sc', base='N.sc', accents=['flourish.middleRightDown1s'], comment='N simple flourish middle right downward'),
    'N.middleRightUp.sc': GD(g2='N.sc', g1='N.sc', l='N.sc', w='N.sc', name='N.middleRightUp.sc', base='N.sc', accents=['flourish.middleRightUp1'], comment='N simple flourish middle right upwards'),

    'O.bottomLeftDown.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.bottomLeftDown.sc', base='O.sc', accents=['flourish.bottomLeftDown2s'], comment='O simple flourish bottom left downward'),
    'O.bottomRightDown.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.bottomRightDown.sc', base='O.sc', accents=['flourish.bottomRightDown2'], comment='O simple flourish bottom right downward'),
    'O.topLeftUp.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.topLeftUp.sc', base='O.sc', accents=['flourish.topLeftUp2s'], comment='O simple flourish top left upwards'),
    'O.topRightUp.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.topRightUp.sc', base='O.sc', accents=['flourish.topRightUp2'], comment='O simple flourish top right upwards'),
    # Flourishes on the side
    'O.middleLeftDown.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.middleLeftDown.sc', base='O.sc', accents=['flourish.middleLeftDown2'], comment='O simple flourish middle left downward'),
    'O.middleLeftUp.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.middleLeftUp.sc', base='O.sc', accents=['flourish.middleLeftUp1s'], comment='O simple flourish middle left upwards'),
    'O.middleRightDown.sc': GD(g2='O.sc', g1='O.sc',  l='O.sc', w='O.sc', name='O.middleRightDown.sc', base='O.sc', accents=['flourish.middleRightDown1s'], comment='O simple flourish middle right downward'),
    'O.middleRightUp.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='O.middleRightUp.sc', base='O.sc', accents=['flourish.middleRightUp2'], comment='O simple flourish middle right upwards'),

    'P.bottomLeftDown.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.bottomLeftDown.sc', base='P.sc', accents=['flourish.bottomLeftDown2x'], comment='P simple flourish bottom left downward'),
    'P.bottomLeftUp.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.bottomLeftUp.sc', base='P.sc', accents=['flourish.bottomLeftUp1s'], comment='P simple flourish bottom left upwards'),
    'P.bottomRightDown.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.bottomRightDown.sc', base='P.sc', accents=['flourish.bottomRightDown2x'], comment='P simple flourish bottom right downward'),
    'P.topLeftDown.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.topLeftDown.sc', base='P.sc', accents=['flourish.topLeftDown1s'], comment='P simple flourish top left downward'),
    'P.topLeftUp.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.topLeftUp.sc', base='P.sc', accents=['flourish.topLeftUp2x'], comment='P simple flourish top left upwards'),
    'P.topRightUp.sc': GD(g2='H.sc', g1='P.sc', l='P.sc', w='P.sc', name='P.topRightUp.sc', base='P.sc', accents=['flourish.topRightUp2'], comment='P simple flourish top right upwards'),
    # Flourishes on the side
    'P.middleLeftDown.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.middleLeftDown.sc', base='P.sc', accents=['flourish.middleLeftDown1'], comment='P simple flourish middle left downward'),
    'P.middleLeftUp.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.middleLeftUp.sc', base='P.sc', accents=['flourish.middleLeftUp1s'], comment='P simple flourish middle left upwards'),
    'P.middleRightDown.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.middleRightDown.sc', base='P.sc', accents=['flourish.middleRightDown1s'], comment='P simple flourish middle right downward'),
    'P.middleRightUp.sc': GD(g2='H.sc', g1='P.sc',l='P.sc', w='P.sc', name='P.middleRightUp.sc', base='P.sc', accents=['flourish.middleRightUp2'], comment='P simple flourish middle right upwards'),

    'Q.topLeftUp.sc': GD(g2='O.sc', g1='O.sc', l='Q.sc', w='Q.sc', name='Q.topLeftUp.sc', base='Q.sc', accents=['flourish.topLeftUp2s'], comment='Q simple flourish top left upwards'),
    'Q.topRightUp.sc': GD(g2='O.sc', g1='O.sc', l='Q.sc', w='Q.sc', name='Q.topRightUp.sc', base='Q.sc', accents=['flourish.topRightUp2'], comment='Q simple flourish top right upwards'),
    # Flourishes on the side
    'Q.middleLeftDown.sc': GD(g2='O.sc', g1='O.sc', l='Q.sc', w='Q.sc', name='Q.middleLeftDown.sc', base='Q.sc', accents=['flourish.middleLeftDown2'], comment='Q simple flourish middle left downward'),
    'Q.middleLeftUp.sc': GD(g2='O.sc', g1='O.sc', l='Q.sc', w='Q.sc', name='Q.middleLeftUp.sc', base='Q.sc', accents=['flourish.middleLeftUp1s'], comment='Q simple flourish middle left upwards'),
    'Q.middleRightDown.sc': GD(g2='O.sc', g1='O.sc', l='Q.sc', w='Q.sc', name='Q.middleRightDown.sc', base='Q.sc', accents=['flourish.middleRightDown1s'], comment='Q simple flourish middle right downward'),
    'Q.middleRightUp.sc': GD(g2='O.sc', g1='O.sc', l='Q.sc', w='Q.sc', name='Q.middleRightUp.sc', base='Q.sc', accents=['flourish.middleRightUp2'], comment='Q simple flourish middle right upwards'),

    'R.bottomLeftDown.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.bottomLeftDown.sc', base='R.sc', accents=['flourish.bottomLeftDown2x'], comment='R simple flourish bottom left downward'),
    'R.bottomLeftUp.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.bottomLeftUp.sc', base='R.sc', accents=['flourish.bottomLeftUp2s'], comment='R simple flourish bottom left upwards'),
    'R.bottomRightDown.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.bottomRightDown.sc', base='R.cbr.sc', accents=['flourish.bottomRightDown2'], comment='R simple flourish bottom right downward'),
    'R.bottomRightUp.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.bottomRightUp.sc', base='R.cbr.sc', accents=['flourish.bottomRightUp1'], comment='R simple flourish bottom right upwards'),
    'R.topLeftDown.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.topLeftDown.sc', base='R.sc', accents=['flourish.topLeftDown1s'], comment='R simple flourish top left downward'),
    'R.topLeftUp.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.topLeftUp.sc', base='R.sc', accents=['flourish.topLeftUp2x'], comment='R simple flourish top left upwards'),
    'R.topRightUp.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.topRightUp.sc', base='R.sc', accents=['flourish.topRightUp2'], comment='R simple flourish top right upwards'),
    # Flourishes on the side
    'R.middleLeftDown.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.middleLeftDown.sc', base='R.sc', accents=['flourish.middleLeftDown1'], comment='R simple flourish middle left downward'),
    'R.middleLeftUp.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.middleLeftUp.sc', base='R.sc', accents=['flourish.middleLeftUp1s'], comment='R simple flourish middle left upwards'),
    'R.middleRightDown.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.middleRightDown.sc', base='R.sc', accents=['flourish.middleRightDown1'], comment='R simple flourish middle right downward'),
    'R.middleRightUp.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='R.middleRightUp.sc', base='R.sc', accents=['flourish.middleRightUp2'], comment='R simple flourish middle right upwards'),

    'S.bottomLeftDown.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.bottomLeftDown.sc', base='S.sc', accents=['flourish.bottomLeftDown1'], comment='S simple flourish bottom left downward'),
    'S.bottomRightDown.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.bottomRightDown.sc', base='S.sc', accents=['flourish.bottomRightDown2'], comment='S simple flourish bottom right downward'),
    'S.topLeftUp.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.topLeftUp.sc', base='S.sc', accents=['flourish.topLeftUp2s'], comment='S simple flourish top left upwards'),
    'S.topRightUp.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', w='S.sc', name='S.topRightUp.sc', base='S.sc', accents=['flourish.topRightUp1'], comment='S simple flourish top right upwards'),
    # Flourishes on the side
    'S.middleLeftDown.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.middleLeftDown.sc', base='S.sc', accents=['flourish.middleLeftDown2s'], comment='S simple flourish middle left downward'),
    'S.middleLeftUp.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.middleLeftUp.sc', base='S.sc', accents=['flourish.middleLeftUp1s'], comment='S simple flourish middle left upwards'),
    'S.middleRightDown.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.middleRightDown.sc', base='S.sc', accents=['flourish.middleRightDown1s'], comment='S simple flourish middle right downward'),
    'S.middleRightUp.sc': GD(g2='S.sc', g1='S.sc',l='S.sc', w='S.sc', name='S.middleRightUp.sc', base='S.sc', accents=['flourish.middleRightUp2s'], comment='S simple flourish middle right upwards'),

    'T.bottomLeftDown.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.bottomLeftDown.sc', base='T.sc', accents=['flourish.bottomLeftDown2x'], comment='T simple flourish bottom left downward'),
    'T.bottomLeftUp.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.bottomLeftUp.sc', base='T.sc', accents=['flourish.bottomLeftUp1'], comment='T simple flourish bottom left upwards'),
    'T.bottomRightDown.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.bottomRightDown.sc', base='T.sc', accents=['flourish.bottomRightDown2x'], comment='T simple flourish bottom right downward'),
    'T.bottomRightUp.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.bottomRightUp.sc', base='T.sc', accents=['flourish.bottomRightUp1'], comment='T simple flourish bottom right upwards'),
    'T.topLeftUp.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.topLeftUp.sc', base='T.sc', accents=['flourish.topLeftUp2s'], comment='T simple flourish top left upwards'),
    'T.topRightUp.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.topRightUp.sc', base='T.sc', accents=['flourish.topRightUp2'], comment='T simple flourish top right upwards'),
    # Flourishes on the side, only #1
    'T.middleLeftDown.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.middleLeftDown.sc', base='T.sc', accents=['flourish.middleLeftDown1'], comment='T simple flourish middle left downward'),
    'T.middleLeftUp.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.middleLeftUp.sc', base='T.sc', accents=['flourish.middleLeftUp1s'], comment='T simple flourish middle left upwards'),
    'T.middleRightDown.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.middleRightDown.sc', base='T.sc', accents=['flourish.middleRightDown1s'], comment='T simple flourish middle right downward'),
    'T.middleRightUp.sc': GD(g2='T.sc', g1='T.sc',l='T.sc', w='T.sc', name='T.middleRightUp.sc', base='T.sc', accents=['flourish.middleRightUp1'], comment='T simple flourish middle right upwards'),

    'Thorn.bottomLeftDown.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.bottomLeftDown.sc', base='Thorn.sc', accents=['flourish.bottomLeftDown2x'], comment='Thorn simple flourish bottom left downward'),
    'Thorn.bottomLeftUp.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.bottomLeftUp.sc', base='Thorn.sc', accents=['flourish.bottomLeftUp1s'], comment='Thorn simple flourish bottom left upwards'),
    'Thorn.bottomRightDown.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.bottomRightDown.sc', base='Thorn.sc', accents=['flourish.bottomRightDown2x'], comment='Thorn simple flourish bottom right downward'),
    'Thorn.topLeftDown.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.topLeftDown.sc', base='Thorn.sc', accents=['flourish.topLeftDown1'], comment='Thorn simple flourish top left upwards'),
    'Thorn.topLeftUp.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.topLeftUp.sc', base='Thorn.sc', accents=['flourish.topLeftUp2x'], comment='Thorn simple flourish top left upwards'),
    'Thorn.topRightUp.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.topRightUp.sc', base='Thorn.sc', accents=['flourish.topRightUp2x'], comment='Thorn simple flourish top right upwards'),
    # Flourishes on the side
    'Thorn.middleLeftDown.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.middleLeftDown.sc', base='Thorn.sc', accents=['flourish.middleLeftDown1'], comment='ThornT simple flourish middle left downward'),
    'Thorn.middleLeftUp.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.middleLeftUp.sc', base='Thorn.sc', accents=['flourish.middleLeftUp1s'], comment='Thorn simple flourish middle left upwards'),
    'Thorn.middleRightDown.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.middleRightDown.sc', base='Thorn.sc', accents=['flourish.middleRightDown1s'], comment='Thorn simple flourish middle right downward'),
    'Thorn.middleRightUp.sc': GD(g2='H.sc', g1='Thorn.sc', l='Thorn.sc', w='Thorn.sc', name='Thorn.middleRightUp.sc', base='Thorn.sc', accents=['flourish.middleRightUp2'], comment='Thorn simple flourish middle right upwards'),

    'U.bottomLeftDown.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.bottomLeftDown.sc', base='U.sc', accents=['flourish.bottomLeftDown2s'], comment='U simple flourish bottom left downward'),
    'U.bottomRightDown.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.bottomRightDown.sc', base='U.sc', accents=['flourish.bottomRightDown2'], comment='U simple flourish bottom right downward'),
    'U.topLeftDown.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.topLeftDown.sc', base='U.sc', accents=['flourish.topLeftDown1s'], comment='U simple flourish top left downward'),
    'U.topLeftUp.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.topLeftUp.sc', base='U.sc', accents=['flourish.topLeftUp2x'], comment='U simple flourish top left upwards'),
    'U.topRightDown.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.topRightDown.sc', base='U.sc', accents=['flourish.topRightDown1s'], comment='U simple flourish top right downward'),
    'U.topRightUp.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.topRightUp.sc', base='U.sc', accents=['flourish.topRightUp2xs'], comment='U simple flourish top right upwards'),
    # Flourishes on the side
    'U.middleLeftDown.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.middleLeftDown.sc', base='U.sc', accents=['flourish.middleLeftDown2s'], comment='U simple flourish middle left downward'),
    'U.middleLeftUp.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.middleLeftUp.sc', base='U.sc', accents=['flourish.middleLeftUp1s'], comment='U simple flourish middle left upwards'),
    'U.middleRightDown.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.middleRightDown.sc', base='U.sc', accents=['flourish.middleRightDown1s'], comment='U simple flourish middle right downward'),
    'U.middleRightUp.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='U.middleRightUp.sc', base='U.sc', accents=['flourish.middleRightUp2s'], comment='U simple flourish middle right upwards'),

    'V.bottomLeftDown.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.bottomLeftDown.sc', base='V.sc', accents=['flourish.bottomLeftDown2s'], comment='V simple flourish bottom left downward'),
    'V.bottomLeftUp.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.bottomLeftUp.sc', base='V.sc', accents=['flourish.bottomLeftUp2sl'], comment='V simple flourish bottom left downward'),
    'V.bottomRightDown.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.bottomRightDown.sc', base='V.sc', accents=['flourish.bottomRightDown2'], comment='V simple flourish bottom right downward'),
    'V.bottomRightUp.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.bottomRightUp.sc', base='V.sc', accents=['flourish.bottomRightUp2sl'], comment='V simple flourish bottom right upward'),
    'V.topLeftDown.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.topLeftDown.sc', base='V.sc', accents=['flourish.topLeftDown1'], comment='V simple flourish top left downward'),
    'V.topLeftUp.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.topLeftUp.sc', base='V.sc', accents=['flourish.topLeftUp2x'], comment='V simple flourish top left upwards'),
    'V.topRightDown.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.topRightDown.sc', base='V.sc', accents=['flourish.topRightDown1s'], comment='V simple flourish top right downward'),
    'V.topRightUp.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.topRightUp.sc', base='V.sc', accents=['flourish.topRightUp2x'], comment='V simple flourish top right upwards'),
    # Flourishes on the side, only #1
    'V.middleLeftDown.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.middleLeftDown.sc', base='V.sc', accents=['flourish.middleLeftDown1s'], comment='V simple flourish middle left downward'),
    'V.middleLeftUp.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.middleLeftUp.sc', base='V.sc', accents=['flourish.middleLeftUp1d'], comment='V simple flourish middle left diagonal upwards'),
    'V.middleRightDown.sc': GD(g2='V.sc', g1='V.sc', l='V.sc', w='V.sc', name='V.middleRightDown.sc', base='V.sc', accents=['flourish.middleRightDown1s'], comment='V simple flourish middle right downward'),

    'W.bottomLeftDown.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.bottomLeftDown.sc', base='W.sc', accents=['flourish.bottomLeftDown2s'], comment='W simple flourish bottom left downward'),
    'W.bottomLeftUp.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.bottomLeftUp.sc', base='W.sc', accents=['flourish.bottomLeftUp2sl'], comment='W simple flourish bottom left downward'),
    'W.bottomRightDown.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.bottomRightDown.sc', base='W.sc', accents=['flourish.bottomRightDown2'], comment='W simple flourish bottom right downward'),
    'W.bottomRightUp.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.bottomRightDown.sc', base='W.sc', accents=['flourish.bottomRightUp2sl'], comment='W simple flourish bottom right downward'),
    'W.topLeftDown.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.topLeftDown.sc', base='W.sc', accents=['flourish.topLeftDown1'], comment='W simple flourish top left downward'),
    'W.topLeftUp.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.topLeftUp.sc', base='W.sc', accents=['flourish.topLeftUp2x'], comment='W simple flourish top left upwards'),
    'W.topRightDown.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.topRightDown.sc', base='W.sc', accents=['flourish.topRightDown1s'], comment='W simple flourish top right downward'),
    'W.topRightUp.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.topRightUp.sc', base='W.sc', accents=['flourish.topRightUp2x'], comment='W simple flourish top right upwards'),
    # Flourishes on the side, only #1
    'W.middleLeftDown.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.middleLeftDown.sc', base='W.sc', accents=['flourish.middleLeftDown1s'], comment='W simple flourish middle left downward'),
    'W.middleLeftUp.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.middleLeftUp.sc', base='W.sc', accents=['flourish.middleLeftUp1d'], comment='W simple flourish middle left diagonal upwards'),
    'W.middleRightDown.sc': GD(g2='W.sc', g1='W.sc', l='W.sc', w='W.sc', name='W.middleRightDown.sc', base='W.sc', accents=['flourish.middleRightDown1s'], comment='W simple flourish middle right downward'),

    'X.bottomLeftDown.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.bottomLeftDown.sc', base='X.sc', accents=['flourish.bottomLeftDown2xs'], comment='X simple flourish bottom left downward'),
    'X.bottomLeftUp.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.bottomLeftUp.sc', base='X.sc', accents=['flourish.bottomLeftUp1'], comment='X simple flourish bottom left upwards'),
    'X.bottomRightDown.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.bottomRightDown.sc', base='X.sc', accents=['flourish.bottomRightDown2xs'], comment='X simple flourish bottom right downward'),
    'X.bottomRightUp.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.bottomRightUp.sc', base='X.sc', accents=['flourish.bottomRightUp1'], comment='X simple flourish bottom right upwards'),
    'X.topLeftDown.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.topLeftDown.sc', base='X.sc', accents=['flourish.topLeftDown1'], comment='X simple flourish top left downward'),
    'X.topLeftUp.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.topLeftUp.sc', base='X.sc', accents=['flourish.topLeftUp2xs'], comment='X simple flourish top left upwards'),
    'X.topRightDown.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.topRightDown.sc', base='X.sc', accents=['flourish.topRightDown1s'], comment='X simple flourish top right downward'),
    'X.topRightUp.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.topRightUp.sc', base='X.sc', accents=['flourish.topRightUp2x'], comment='X simple flourish top right upwards'),
    # Flourishes on top-right and bottom-left
    'X.middleLeftDown.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.middleLeftDown.sc', base='X.sc', accents=['flourish.middleLeftDown1d'], comment='X simple flourish middle left downward'),
    'X.middleLeftUp.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.middleLeftUp.sc', base='X.sc', accents=['flourish.middleLeftUp1d'], comment='X simple flourish middle left upwards'),
    'X.middleRightDown.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.middleRightDown.sc', base='X.sc', accents=['flourish.middleRightDown1d'], comment='X simple flourish middle right downward'),
    'X.middleRightUp.sc': GD(g2='X.sc', g1='X.sc', l='X.sc', w='X.sc', name='X.middleRightUp.sc', base='X.sc', accents=['flourish.middleRightUp1d'], comment='X simple flourish middle right upwards'),

    'Y.bottomLeftDown.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.bottomLeftDown.sc', base='Y.sc', accents=['flourish.bottomLeftDown2x'], comment='Y simple flourish bottom left downward'),
    'Y.bottomLeftUp.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.bottomLeftUp.sc', base='Y.sc', accents=['flourish.bottomLeftUp1'], comment='Y simple flourish bottom left upwards'),
    'Y.bottomRightDown.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.bottomRightDown.sc', base='Y.sc', accents=['flourish.bottomRightDown2x'], comment='Y simple flourish bottom right downward'),
    'Y.bottomRightUp.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.bottomRightUp.sc', base='Y.sc', accents=['flourish.bottomRightUp1'], comment='Y simple flourish bottom right upwards'),
    'Y.topLeftDown.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.topLeftDown.sc', base='Y.sc', accents=['flourish.topLeftDown1'], comment='Y simple flourish top left downward'),
    'Y.topLeftUp.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.topLeftUp.sc', base='Y.sc', accents=['flourish.topLeftUp2x'], comment='Y simple flourish top left upwards'),
    'Y.topRightDown.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.topRightDown.sc', base='Y.sc', accents=['flourish.topRightDown1s'], comment='Y simple flourish top right downward'),
    'Y.topRightUp.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.topRightUp.sc', base='Y.sc', accents=['flourish.topRightUp2x'], comment='Y simple flourish top right upwards'),
    # Flourishes on the side, only #1
    'Y.middleLeftDown.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.middleLeftDown.sc', base='Y.sc', accents=['flourish.middleLeftDown1s'], comment='Y simple flourish middle left downward'),
    'Y.middleLeftUp.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.middleLeftUp.sc', base='Y.sc', accents=['flourish.middleLeftUp1d'], comment='Y simple flourish middle left diagonal upwards'),
    'Y.middleRightDown.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', w='Y.sc', name='Y.middleRightDown.sc', base='Y.sc', accents=['flourish.middleRightDown1s'], comment='Y simple flourish middle right downward'),

    'Z.topLeftUp.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.topLeftUp.sc', base='Z.sc', accents=['flourish.topLeftUp2x'], comment='Z simple flourish top left upwards'),
    'Z.topRightUp.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.topRightUp.sc', base='Z.sc', accents=['flourish.topRightUp2x'], comment='Z simple flourish top right upwards'),
    #'Z.topLeftDown.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.topLeftDown.sc', base='Z.sc', accents=['flourish.topLeftDown1s'], comment='Z simple flourish top left down'),
    'Z.topRightDown.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.topRightDown.sc', base='Z.sc', accents=['flourish.topRightDown1s'], comment='Z simple flourish top right down'),
    'Z.bottomLeftUp.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.bottomLeftUp.sc', base='Z.sc', accents=['flourish.bottomLeftUp1s'], comment='Z simple flourish bottom left upwards'),
    #'Z.bottomRightUp.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.bottomRightUp.sc', base='Z.sc', accents=['flourish.bottomRightUp1s'], comment='Z simple flourish bottom right upwards'),
    'Z.bottomLeftDown.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.bottomLeftDown.sc', base='Z.sc', accents=['flourish.bottomLeftDown2x'], comment='Z simple flourish bottom left downward'),
    'Z.bottomRightDown.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.bottomRightDown.sc', base='Z.sc', accents=['flourish.bottomRightDown1x'], comment='Z simple flourish bottom right downward'),
    # Flourishes on the side
    'Z.middleLeftUp.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.middleLeftUp.sc', base='Z.sc', accents=['flourish.middleLeftUp1'], comment='Z simple flourish middle left upwards'),
    'Z.middleRightUp.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.middleRightUp.sc', base='Z.sc', accents=['flourish.middleRightUp2'], comment='Z simple flourish middle right upwards'),
    'Z.middleLeftDown.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.middleLeftDown.sc', base='Z.sc', accents=['flourish.middleLeftDown2'], comment='Z simple flourish middle left downward'),
    'Z.middleRightDown.sc': GD(g2='Z.sc', g1='Z.sc', l='Z.sc', w='Z.sc', name='Z.middleRightDown.sc', base='Z.sc', accents=['flourish.middleRightDown1'], comment='Z simple flourish middle right downward'),

    'OE.topLeftUp.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.topLeftUp.sc', base='OE.sc', accents=['flourish.topLeftUp2s'], comment='OE simple flourish top left upwards'),
    'OE.bottomLeftDown.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.bottomLeftDown.sc', base='OE.sc', accents=['flourish.bottomLeftDown2xs'], comment='OE simple flourish bottom left downward'),
    'OE.topRightUp.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.topRightUp.sc', base='OE.sc', accents=['flourish.topRightUp2'], comment='OE simple flourish top right upwards'),
    'OE.bottomRightDown.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.bottomRightDown.sc', base='OE.sc', accents=['flourish.bottomRightDown2'], comment='OE simple flourish bottom right downward'),
    'OE.middleLeftUp.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.middleLeftUp.sc', base='OE.sc', accents=['flourish.middleLeftUp1s'], comment='OE simple flourish middle left upwards'),
    'OE.middleLeftDown.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.middleLeftDown.sc', base='OE.sc', accents=['flourish.middleLeftDown2'], comment='OE simple flourish middle left downward'),
    'OE.middleRightUp.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.middleRightUp.sc', base='OE.sc', accents=['flourish.middleRightUp1'], comment='OE simple flourish middle right upwards'),
    'OE.middleRightDown.sc': GD(g2='O.sc', g1='E.sc', l='OE.sc', w='OE.sc', name='OE.middleRightDown.sc', base='OE.sc', accents=['flourish.middleRightDown1s'], comment='OE simple flourish middle right downward'),

    'AE.topRightUp.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.topRightUp.sc', base='AE.sc', accents=['flourish.topRightUp2'], comment='AE simple flourish top right upwards'),
    'AE.bottomRightDown.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.bottomRightDown.sc', base='AE.sc', accents=['flourish.bottomRightDown2'], comment='AE simple flourish bottom right downward'),
    'AE.topLeftUp.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.topLeftUp.sc', base='AE.sc', accents=['flourish.topLeftUp2s'], comment='AE simple flourish top left upwards'),
    'AE.topLeftDown.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.topLeftDown.sc', base='AE.sc', accents=['flourish.topLeftDown2sl'], comment='AE simple flourish top left downwards'),
    'AE.bottomLeftUp.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.bottomLeftUp.sc', base='AE.sc', accents=['flourish.bottomLeftUp1'], comment='AEsimple flourish bottom left upwards'),
    'AE.bottomLeftDown.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.bottomLeftDown.sc', base='AE.sc', accents=['flourish.bottomLeftDown2xs'], comment='AE simple flourish bottom left downward'),
    'AE.middleLeftUp.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.middleLeftUp.sc', base='AE.sc', accents=['flourish.middleLeftUp1'], comment='AE simple flourish middle left upwards'),
    'AE.middleRightUp.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.middleRightUp.sc', base='AE.sc', accents=['flourish.middleRightUp1'], comment='AE simple flourish middle right upwards'),
    'AE.middleRightDown.sc': GD(g2='AE.sc', g1='E.sc', l='AE.sc', w='AE.sc', name='AE.middleRightDown.sc', base='AE.sc', accents=['flourish.middleRightDown1s'], comment='AE simple flourish middle right downward'),

    # /a Connector is the same for roman and italic
    'a.bottomLeftDown': GD(g2='a', g1='a', l='a', w='a', name='a.bottomLeftDown', isLower=True, base='a', accents=['flourish.bottomLeftDown2s'], comment='a simple flourish bottom left downward'),
    'a.bottomRightDown': GD(g2='a', g1='a', l='a', w='a', name='a.bottomRightDown', isLower=True, base='a.cbr', accents=['flourish.bottomRightDown2'], comment='a simple flourish bottom right downward'),
    'a.bottomRightUp': GD(g2='a', g1='a', l='a', w='a', name='a.bottomRightUp', isLower=True, base='a.cbr', accents=['flourish.bottomRightUp1'], comment='a simple flourish bottom right upwards'),
    'a.cbr': GD(g2='a', g1='a', l='a', w='a', name='a.cbr', src='a', isLower=True, comment='a - connector bottom right'),
    'a.topLeftUp': GD(g2='a', g1='a', l='a', w='a', name='a.topLeftUp', base='a', isLower=True, accents=['flourish.topLeftUp2s'], comment='a simple flourish top left upwards'),
    'a.topRightUp': GD(g2='a', g1='a', l='a', w='a', name='a.topRightUp', base='a', isLower=True, accents=['flourish.topRightUp2'], comment='a simple flourish top right upwards'),
    # Flourishes on the side
    'a.middleLeftDown': GD(g2='a', g1='a', l='a', w='a', name='a.middleLeftDown', isLower=True, base='a', accents=['flourish.middleLeftDown2s'], overshoot=OVERSHOOT, comment='a simple flourish middle left downward'),
    'a.middleLeftUp': GD(g2='a', g1='a', l='a', w='a', name='a.middleLeftUp', isLower=True, base='a', accents=['flourish.middleLeftUp1s'], overshoot=OVERSHOOT, comment='a simple flourish middle left upwards'),
    'a.middleRightDown': GD(g2='a', g1='a',  l='a', w='a', name='a.middleRightDown', isLower=True, base='a', accents=['flourish.middleRightDown1s'], overshoot=OVERSHOOT, comment='a simple flourish middle right downward'),
    'a.middleRightUp': GD(g2='a', g1='a', l='a', w='a', name='a.middleRightUp', isLower=True, base='a', accents=['flourish.middleRightUp2s'], overshoot=OVERSHOOT, comment='a simple flourish middle right upwards'),

    'b.bottomLeftDown': GD(g2='b', g1='o', l='b', w='b', name='b.bottomLeftDown', isLower=True, base='b', accents=['flourish.bottomLeftDown2s'], comment='b simple flourish bottom left downward'),
    'b.bottomRightDown': GD(g2='b', g1='o', l='b', w='b', name='b.bottomRightDown', isLower=True, base='b', accents=['flourish.bottomRightDown2'], comment='b simple flourish bottom right downward'),
    'b.topLeftDown': GD(g2='b', g1='o', l='b', w='b', name='b.topLeftDown', isLower=True, base='b', accents=['flourish.topLeftDown1'], comment='b simple flourish top left downward'),
    'b.topLeftUp': GD(g2='b', g1='o', l='b', w='b', name='b.topLeftUp', isLower=True, base='b', accents=['flourish.topLeftUp2xs'], comment='b simple flourish top left upwards'),
    'b.topRightUp': GD(g2='b', g1='o', l='b', w='b', name='b.topRightUp', isLower=True, base='b', accents=['flourish.topRightUp2'], comment='b simple flourish top right upwards'),
    # Flourishes on the side
    'b.middleLeftDown': GD(g2='b', g1='o', l='b', w='b', name='b.middleLeftDown', isLower=True, base='b', accents=['flourish.middleLeftDown2s'], comment='b simple flourish middle left downward'),
    'b.middleLeftUp': GD(g2='b', g1='o', l='b', w='b', name='b.middleLeftUp', isLower=True, base='b', accents=['flourish.middleLeftUp1s'], comment='b simple flourish middle left upwards'),
    'b.middleRightDown': GD(g2='b', g1='o',  l='b', w='b', name='b.middleRightDown', isLower=True, base='b', accents=['flourish.middleRightDown1s'], comment='b simple flourish middle right downward'),
    'b.middleRightUp': GD(g2='b', g1='o', l='b', w='b', name='b.middleRightUp', isLower=True, base='b', accents=['flourish.middleRightUp2s'], comment='b simple flourish middle right upwards'),

    'c.bottomLeftDown': GD(g2='o', g1='c', l='c', w='c', name='c.bottomLeftDown', isLower=True, base='c', accents=['flourish.bottomLeftDown2s'], comment='c simple flourish bottom left downward'),
    'c.bottomRightDown': GD(g2='o', g1='c', l='c', w='c', name='c.bottomRightDown', isLower=True, base='c', accents=['flourish.bottomRightDown2'], comment='c simple flourish bottom right downward'),
    'c.topLeftUp': GD(g2='o', g1='c', l='c', w='c', name='c.topLeftUp', isLower=True, base='c', accents=['flourish.topLeftUp2s'], comment='c simple flourish top left upwards'),
    'c.topRightUp': GD(g2='o', g1='c', l='c', w='c', name='c.topRightUp', isLower=True, base='c', accents=['flourish.topRightUp2'], comment='c simple flourish top right upwards'),
    # Flourishes on the side
    'c.middleLeftDown': GD(g2='o', g1='c', l='c', w='c', name='c.middleLeftDown', isLower=True, base='c', accents=['flourish.middleLeftDown2s'], comment='c simple flourish middle left downward'),
    'c.middleLeftUp': GD(g2='o', g1='c', l='c', w='c', name='c.middleLeftUp', isLower=True, base='c', accents=['flourish.middleLeftUp1s'], comment='c simple flourish middle left upwards'),
    'c.middleRightDown': GD(g2='o', g1='c',  l='c', w='c', name='c.middleRightDown', isLower=True, base='c', accents=['flourish.middleRightDown1s'], comment='c simple flourish middle right downward'),
    'c.middleRightUp': GD(g2='o', g1='c', l='c', w='c', name='c.middleRightUp', isLower=True, base='c', accents=['flourish.middleRightUp2s'], comment='c simple flourish middle right upwards'),

    'd.bottomLeftDown': GD(g2='o', g1='l', l='d', w='d', name='d.bottomLeftDown', isLower=True, base='d', accents=['flourish.bottomLeftDown2s'], comment='d simple flourish bottom left downward'),
    'd.bottomRightDown': GD(g2='o', g1='l', l='d', w='d', name='d.bottomRightDown', isLower=True, base='d.cbr', accents=['flourish.bottomRightDown2xs'], comment='d simple flourish bottom right downward'),
    'd.bottomRightUp': GD(g2='o', g1='l', l='d', w='d', name='d.bottomRightUp', isLower=True, base='d.cbr', accents=['flourish.bottomRightUp1'], comment='d simple flourish bottom right upwards'),
    'd.topLeftDown': GD(g2='o', g1='l', l='d', w='d', name='d.topLeftDown', isLower=True, base='d', accents=['flourish.topLeftUp2sl'], comment='d simple flourish top left upwards'),
    'd.topLeftUp': GD(g2='o', g1='l', l='d', w='d', name='d.topLeftUp', isLower=True, base='d', accents=['flourish.topLeftUp2xs'], comment='d simple flourish top left upwards'),
    'd.topRightUp': GD(g2='o', g1='o', l='d', w='d', name='d.topRightUp', isLower=True, base='d', accents=['flourish.topRightUp2xs'], comment='d simple flourish top right upwards'),
    # Flourishes on the side
    'd.middleLeftDown': GD(g2='o', g1='l', l='d', w='d', name='d.middleLeftDown', isLower=True, base='d', accents=['flourish.middleLeftDown2s'], comment='d simple flourish middle left downward'),
    'd.middleLeftUp': GD(g2='o', g1='l', l='d', w='d', name='d.middleLeftUp', isLower=True, base='d', accents=['flourish.middleLeftUp1s'], comment='d simple flourish middle left upwards'),
    'd.middleRightDown': GD(g2='o', g1='l',  l='d', w='d', name='d.middleRightDown', isLower=True, base='d', accents=['flourish.middleRightDown1s'], comment='d simple flourish middle right downward'),
    'd.middleRightUp': GD(g2='o', g1='l', l='d', w='d', name='d.middleRightUp', isLower=True, base='d', accents=['flourish.middleRightUp2s'], comment='d simple flourish middle right upwards'),

    'e.bottomLeftDown': GD(g2='o', g1='o', l='e', w='e', name='e.bottomLeftDown', isLower=True, base='e', accents=['flourish.bottomLeftDown2s'], comment='e simple flourish bottom left downward'),
    'e.bottomRightDown': GD(g2='o', g1='o', l='e', w='e', name='e.bottomRightDown', isLower=True, base='e', accents=['flourish.bottomRightDown2'], comment='e simple flourish bottom right downward'),
    'e.topLeftUp': GD(g2='o', g1='o', l='e', w='e', name='e.topLeftUp', isLower=True, base='e', accents=['flourish.topLeftUp2s'], comment='e simple flourish top left upwards'),
    'e.topRightUp': GD(g2='o', g1='o', l='e', w='e', name='e.topRightUp', isLower=True, base='e', accents=['flourish.topRightUp2'], comment='e simple flourish top right upwards'),
    # Flourishes on the side
    'e.middleLeftDown': GD(g2='o', g1='o', l='e', w='e', name='e.middleLeftDown', isLower=True, base='e', accents=['flourish.middleLeftDown2s'], comment='e simple flourish middle left downward'),
    'e.middleLeftUp': GD(g2='o', g1='o', l='e', w='e', name='e.middleLeftUp', isLower=True, base='e', accents=['flourish.middleLeftUp1s'], comment='e simple flourish middle left upwards'),
    'e.middleRightUp': GD(g2='o', g1='o', l='e', w='e', name='e.middleRightUp', isLower=True, base='e', accents=['flourish.middleRightUp1s'], comment='e simple flourish middle right upwards'),

    'f.bottomLeftDown': GD(g2='f', g1='f', l='f', w='f', name='f.bottomLeftDown', isLower=True, base='f', accents=['flourish.bottomLeftDown2x'], copyFromDisplayRight=False, comment='f simple flourish bottom left downward'),
    'f.bottomLeftUp': GD(g2='f', g1='f', l='f', w='f', name='f.bottomLeftUp', isLower=True, base='f', accents=['flourish.bottomLeftUp1'], copyFromDisplayRight=False, comment='f simple flourish bottom left upwards'),
    'f.bottomRightDown': GD(g2='f', g1='f', l='f', w='f', name='f.bottomRightDown', isLower=True, base='f', accents=['flourish.bottomRightDown2x'], copyFromDisplayRight=False, comment='f simple flourish bottom right downward'),
    'f.bottomRightUp': GD(g2='f', g1='f', l='f', w='f', name='f.bottomRightUp', isLower=True, base='f', accents=['flourish.bottomRightUp1'], copyFromDisplayRight=False, comment='f simple flourish bottom right upwards'),
    'f.topLeftUp': GD(g2='f', g1='f', l='f', w='f', name='f.topLeftUp', isLower=True, base='f', accents=['flourish.topLeftUp2s'], copyFromDisplayRight=False, comment='f simple flourish top left upwards'),
    'f.topRightUp': GD(g2='f', g1='f', l='f', w='f', name='f.topRightUp', isLower=True, base='f', accents=['flourish.topRightUp2'], copyFromDisplayRight=False, comment='f simple flourish top right upwards'),
    # Flourishes on the side
    'f.middleLeftDown': GD(g2='f', g1='f', l='f', w='f', name='f.middleLeftDown', isLower=True, base='f', accents=['flourish.middleLeftDown2s'], copyFromDisplayRight=False, comment='f simple flourish middle left downward'),
    'f.middleLeftUp': GD(g2='f', g1='f', l='f', w='f', name='f.middleLeftUp', isLower=True, base='f', accents=['flourish.middleLeftUp1s'], copyFromDisplayRight=False, comment='f simple flourish middle left upwards'),
    'f.middleRightDown': GD(g2='f', g1='f',  l='f', w='f', name='f.middleRightDown', isLower=True, base='f', accents=['flourish.middleRightDown1s'], copyFromDisplayRight=False, comment='f simple flourish middle right downward'),
    'f.middleRightUp': GD(g2='f', g1='f', l='f', w='f', name='f.middleRightUp', isLower=True, base='f', accents=['flourish.middleRightUp2s'], copyFromDisplayRight=False, comment='f simple flourish middle right upwards'),

    'g.bottomLeftDown': GD(g2='g', g1='g', l='g', w='g', name='g.bottomLeftDown', isLower=True, base='g', accents=['flourish.bottomLeftDown2s'], comment='g simple flourish bottom left downward'),
    'g.bottomRightDown': GD(g2='g', g1='g', l='g', w='g', name='g.bottomRightDown', isLower=True, base='g', accents=['flourish.bottomRightDown2'], comment='g simple flourish bottom right downward'),
    'g.topLeftUp': GD(g2='g', g1='g', l='g', w='g', name='g.topLeftUp', isLower=True, base='g', accents=['flourish.topLeftUp2s'], comment='g simple flourish top left upwards'),
    'g.topRightUp': GD(g2='g', g1='g', l='g', w='g', name='g.topRightUp', isLower=True, base='g', accents=['flourish.topRightUp2'], comment='g simple flourish top right upwards'),
    # Flourishes on the side
    'g.middleLeftDown': GD(g2='g', g1='g', l='g', w='g', name='g.middleLeftDown', isLower=True, base='g', accents=['flourish.middleLeftDown2s'], comment='g simple flourish middle left downward'),
    'g.middleLeftUp': GD(g2='g', g1='g', l='g', w='g', name='g.middleLeftUp', isLower=True, base='g', accents=['flourish.middleLeftUp1s'], comment='g simple flourish middle left upwards'),
    'g.middleRightDown': GD(g2='g', g1='g',  l='g', w='g', name='g.middleRightDown', isLower=True, base='g', accents=['flourish.middleRightDown1s'], comment='g simple flourish middle right downward'),
    'g.middleRightUp': GD(g2='g', g1='g', l='g', w='g', name='g.middleRightUp', isLower=True, base='g', accents=['flourish.middleRightUp2s'], comment='g simple flourish middle right upwards'),

    'h.bottomLeftDown': GD(g2='l', g1='n', l='h', w='h', name='h.bottomLeftDown', isLower=True, base='h', accents=['flourish.bottomLeftDown2x'], comment='h simple flourish bottom left downward'),
    'h.bottomLeftUp': GD(g2='l', g1='n', l='h', w='h', name='h.bottomLeftUp', isLower=True, base='h', accents=['flourish.bottomLeftUp1'], comment='h simple flourish bottom left upwards'),
    'h.bottomRightDown': GD(g2='l', g1='n', l='h', w='h', name='h.bottomRightDown', isLower=True, base='h', accents=['flourish.bottomRightDown2x'], comment='h simple flourish bottom right downward'),
    'h.bottomRightUp': GD(g2='l', g1='n', l='h', w='h', name='h.bottomRightUp', isLower=True, base='h', accents=['flourish.bottomRightUp1'], comment='h simple flourish bottom right upwards'),
    'h.topLeftDown': GD(g2='l', g1='n', l='h', w='h', name='h.topLeftDown', isLower=True, base='h', accents=['flourish.topLeftDown1'], comment='h simple flourish top left downward'),
    'h.topLeftUp': GD(g2='l', g1='n', l='h', w='h', name='h.topLeftUp', isLower=True, base='h', accents=['flourish.topLeftUp2xs'], comment='h simple flourish top left upwards'),
    'h.topRightUp': GD(g2='l', g1='n', l='h', w='h', name='h.topRightUp', isLower=True, base='h', accents=['flourish.topRightUp2'], comment='h simple flourish top right upwards'),
    # Flourishes on the side
    'h.middleLeftDown': GD(g2='l', g1='n', l='h', w='h', name='h.middleLeftDown', isLower=True, base='h', accents=['flourish.middleLeftDown2s'], comment='h simple flourish middle left downward'),
    'h.middleLeftUp': GD(g2='l', g1='n', l='h', w='h', name='h.middleLeftUp', isLower=True, base='h', accents=['flourish.middleLeftUp1s'], comment='h simple flourish middle left upwards'),
    'h.middleRightDown': GD(g2='l', g1='n',  l='h', w='h', name='h.middleRightDown', isLower=True, base='h', accents=['flourish.middleRightDown1s'], comment='h simple flourish middle right downward'),
    'h.middleRightUp': GD(g2='l', g1='n', l='h', w='h', name='h.middleRightUp', isLower=True, base='h', accents=['flourish.middleRightUp2s'], comment='h simple flourish middle right upwards'),

    'i.bottomLeftDown': GD(g2='i', g1='i', l='i', w='i', name='i.bottomLeftDown', isLower=True, base='i', accents=['flourish.bottomLeftDown2x'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish bottom left downward'),
    'i.bottomLeftUp': GD(g2='i', g1='i', l='i', w='i', name='i.bottomLeftUp', isLower=True, base='i', accents=['flourish.bottomLeftUp1'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish bottom left upwards'),
    'i.bottomRightDown': GD(g2='i', g1='i', l='i', w='i', name='i.bottomRightDown', isLower=True, base='i', accents=['flourish.bottomRightDown2x'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish bottom right downward'),
    'i.bottomRightUp': GD(g2='i', g1='i', l='i', w='i', name='i.bottomRightUp', isLower=True, base='i', accents=['flourish.bottomRightUp1'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish bottom right upwards'),
    'i.topLeftDown': GD(g2='i', g1='i', l='i', w='i', name='i.topLeftDown', isLower=True, base='i', accents=['flourish.topLeftDown1'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish top left downward'),
    'i.topLeftUp': GD(g2='i', g1='i', l='i', w='i', name='i.topLeftUp', isLower=True, base='idotless', accents=['flourish.topLeftUp2xs'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish top left upwards'),
    'i.topRightUp': GD(g2='i', g1='i', l='i', w='i', name='i.topRightUp', isLower=True, base='idotless', accents=['flourish.topRightUp2'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish top right upwards'),
    # Flourishes on the side
    'i.middleLeftDown': GD(g2='i', g1='i', l='i', w='i', name='i.middleLeftDown', isLower=True, base='i', accents=['flourish.middleLeftDown2s'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish middle left downward'),
    'i.middleLeftUp': GD(g2='i', g1='i', l='i', w='i', name='i.middleLeftUp', isLower=True, base='i', accents=['flourish.middleLeftUp1s'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish middle left upwards'),
    'i.middleRightDown': GD(g2='i', g1='i',  l='i', w='i', name='i.middleRightDown', isLower=True, base='i', accents=['flourish.middleRightDown1s'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish middle right downward'),
    'i.middleRightUp': GD(g2='i', g1='i', l='i', w='i', name='i.middleRightUp', isLower=True, base='i', accents=['flourish.middleRightUp2s'], anchors=ALL_IJ_ANCHORS, comment='i simple flourish middle right upwards'),

    'j.bottomLeftDown': GD(g2='j', g1='j', l='j', w='j', name='j.bottomLeftDown', isLower=True, base='j', accents=['flourish.bottomLeftDown2s'], comment='j simple flourish bottom left downward'),
    'j.bottomLeftUp': GD(g2='j', g1='j', l='j', w='j', name='j.bottomLeftUp', isLower=True, base='j', accents=['flourish.bottomLeftUp1'], comment='j simple flourish bottom left upwards'),
    'j.bottomRightDown': GD(g2='j', g1='j', l='j', w='j', name='j.bottomRightDown', isLower=True, base='j', accents=['flourish.bottomRightDown2'], comment='j simple flourish bottom right downward'),
    'j.topLeftDown': GD(g2='j', g1='j', l='j', w='j', name='j.topLeftDown', isLower=True, base='j', accents=['flourish.topLeftDown1'], comment='j simple flourish top left downward'),
    'j.topLeftUp': GD(g2='j', g1='j', l='j', w='j', name='j.topLeftUp', isLower=True, base='jdotless', accents=['flourish.topLeftUp2xs'], comment='j simple flourish top left upwards'),
    'j.topRightUp': GD(g2='j', g1='j', l='j', w='j', name='j.topRightUp', isLower=True, base='jdotless', accents=['flourish.topRightUp2'], comment='j simple flourish top right upwards'),
    # Flourishes on the side
    'j.middleLeftDown': GD(g2='j', g1='j', l='j', w='j', name='j.middleLeftDown', isLower=True, base='j', accents=['flourish.middleLeftDown2s'], comment='j simple flourish middle left downward'),
    'j.middleLeftUp': GD(g2='j', g1='j', l='j', w='j', name='j.middleLeftUp', isLower=True, base='j', accents=['flourish.middleLeftUp1s'], comment='j simple flourish middle left upwards'),
    'j.middleRightDown': GD(g2='j', g1='j',  l='j', w='j', name='j.middleRightDown', isLower=True, base='j', accents=['flourish.middleRightDown1s'], comment='j simple flourish middle right downward'),
    'j.middleRightUp': GD(g2='j', g1='j', l='j', w='j', name='j.middleRightUp', isLower=True, base='j', accents=['flourish.middleRightUp2s'], comment='j simple flourish middle right upwards'),

    'k.bottomLeftDown': GD(g2='l', g1='k', l='k', w='k', name='k.bottomLeftDown', isLower=True, base='k', accents=['flourish.bottomLeftDown2xs'], comment='k simple flourish bottom left downward'),
    'k.bottomLeftUp': GD(g2='l', g1='k', l='k', w='k', name='k.bottomLeftUp', isLower=True, base='k', accents=['flourish.bottomLeftUp1'], comment='k simple flourish bottom left upwards'),
    'k.bottomRightDown': GD(g2='l', g1='k', l='k', w='k', name='k.bottomRightDown', isLower=True, base='k', accents=['flourish.bottomRightDown2x'], comment='k simple flourish bottom right downward'),
    'k.bottomRightUp': GD(g2='l', g1='k', l='k', w='k', name='k.bottomRightUp', isLower=True, base='k', accents=['flourish.bottomRightUp1'], comment='k simple flourish bottom right upwards'),
    'k.topLeftDown': GD(g2='l', g1='k', l='k', w='k', name='k.topLeftDown', isLower=True, base='k', accents=['flourish.topLeftDown1'], comment='k simple flourish top left downward'),
    'k.topLeftUp': GD(g2='l', g1='k', l='k', w='k', name='k.topLeftUp', isLower=True, base='k', accents=['flourish.topLeftUp2xs'], comment='k simple flourish top left upwards'),
    'k.topRightDown': GD(g2='l', g1='k', l='k', w='k', name='k.topRightDown', isLower=True, base='k', accents=['flourish.topRightDown1'], comment='k simple flourish top right downward'),
    'k.topRightUp': GD(g2='l', g1='k', l='k', w='k', name='k.topRightUp', isLower=True, base='k', accents=['flourish.topRightUp2xs'], comment='k simple flourish top right upwards'),
    # Flourishes on the side
    'k.middleLeftDown': GD(g2='l', g1='k', l='k', w='k', name='k.middleLeftDown', isLower=True, base='k', accents=['flourish.middleLeftDown2s'], comment='k simple flourish middle left downward'),
    'k.middleLeftUp': GD(g2='l', g1='k', l='k', w='k', name='k.middleLeftUp', isLower=True, base='k', accents=['flourish.middleLeftUp1s'], comment='k simple flourish middle left upwards'),
    'k.middleRightDown': GD(g2='l', g1='k',  l='k', w='k', name='k.middleRightDown', isLower=True, base='k', accents=['flourish.middleRightDown1d'], comment='k simple flourish middle right downward'),
    'k.middleRightUp': GD(g2='l', g1='k', l='k', w='k', name='k.middleRightUp', isLower=True, base='k', accents=['flourish.middleRightUp1d'], comment='k simple flourish middle right upwards'),

    # Too much /P 'l.topRightDown'
    'l.bottomLeftDown': GD(g2='l', g1='l', l='l', w='l', name='l.bottomLeftDown', isLower=True, base='l', accents=['flourish.bottomLeftDown2x'], comment='l simple flourish bottom left downward'),
    'l.bottomLeftUp': GD(g2='l', g1='l', l='l', w='l', name='l.bottomLeftUp', isLower=True, base='l', accents=['flourish.bottomLeftUp1'], comment='l simple flourish bottom left upwards'),
    'l.bottomRightDown': GD(g2='l', g1='l', l='l', w='l', name='l.bottomRightDown', isLower=True, base='l', accents=['flourish.bottomRightDown2x'], comment='l simple flourish bottom right downward'),    
    'l.bottomRightUp': GD(g2='l', g1='l', l='l', w='l', name='l.bottomRightUp', isLower=True, base='l', accents=['flourish.bottomRightUp1s'], comment='l simple flourish bottom right upward'),    
    'l.topLeftDown': GD(g2='l', g1='l', l='l', w='l', name='l.topLeftDown', isLower=True, base='l', accents=['flourish.topLeftDown1'], comment='l simple flourish top left downward'),
    'l.topLeftUp': GD(g2='l', g1='l', l='l', w='l', name='l.topLeftUp', isLower=True, base='l', accents=['flourish.topLeftUp2xs'], comment='l simple flourish top left upwards'),
    'l.topRightUp': GD(g2='l', g1='l', l='l', w='l', name='l.topRightUp', isLower=True, base='l', accents=['flourish.topRightUp2xs'], comment='l simple flourish top right upwards'),
    # Flourishes on the side
    'l.middleLeftDown': GD(g2='l', g1='l', l='l', w='l', name='l.middleLeftDown', isLower=True, base='l', accents=['flourish.middleLeftDown2s'], comment='l simple flourish middle left downward'),
    'l.middleLeftUp': GD(g2='l', g1='l', l='l', w='l', name='l.middleLeftUp', isLower=True, base='l', accents=['flourish.middleLeftUp1s'], comment='l simple flourish middle left upwards'),
    'l.middleRightDown': GD(g2='l', g1='l',  l='l', w='l', name='l.middleRightDown', isLower=True, base='l', accents=['flourish.middleRightDown1s'], comment='l simple flourish middle right downward'),
    'l.middleRightUp': GD(g2='l', g1='l', l='l', w='l', name='l.middleRightUp', isLower=True, base='l', accents=['flourish.middleRightUp2s'], comment='l simple flourish middle right upwards'),

    'm.bottomLeftDown': GD(g2='n', g1='n', l='m', w='m', name='m.bottomLeftDown', isLower=True, base='m', accents=['flourish.bottomLeftDown2x'], comment='m simple flourish bottom left downward'),
    'm.bottomLeftUp': GD(g2='n', g1='n', l='m', w='m', name='m.bottomLeftUp', isLower=True, base='m', accents=['flourish.bottomLeftUp1'], comment='m simple flourish bottom left upwards'),
    'm.bottomRightDown': GD(g2='n', g1='n', l='m', w='m', name='m.bottomRightDown', isLower=True, base='m', accents=['flourish.bottomRightDown2x'], comment='m simple flourish bottom right downward'),
    'm.bottomRightUp': GD(g2='n', g1='n', l='m', w='m', name='m.bottomRightUp', isLower=True, base='m', accents=['flourish.bottomRightUp1'], comment='m simple flourish bottom right upwards'),
    'm.topLeftDown': GD(g2='n', g1='n', l='m', w='m', name='m.topLeftDown', isLower=True, base='m', accents=['flourish.topLeftDown1'], comment='m simple flourish top left downward'),
    'm.topLeftUp': GD(g2='n', g1='n', l='m', w='m', name='m.topLeftUp', isLower=True, base='m', accents=['flourish.topLeftUp2xs'], comment='m simple flourish top left upwards'),
    'm.topRightUp': GD(g2='n', g1='n', l='m', w='m', name='m.topRightUp', isLower=True, base='m', accents=['flourish.topRightUp2'], comment='m simple flourish top right upwards'),
    # Flourishes on the side
    'm.middleLeftDown': GD(g2='n', g1='n', l='m', w='m', name='m.middleLeftDown', isLower=True, base='m', accents=['flourish.middleLeftDown2s'], comment='m simple flourish middle left downward'),
    'm.middleLeftUp': GD(g2='n', g1='n', l='m', w='m', name='m.middleLeftUp', isLower=True, base='m', accents=['flourish.middleLeftUp1s'], comment='m simple flourish middle left upwards'),
    'm.middleRightDown': GD(g2='n', g1='n',  l='m', w='m', name='m.middleRightDown', isLower=True, base='m', accents=['flourish.middleRightDown1s'], comment='m simple flourish middle right downward'),
    'm.middleRightUp': GD(g2='n', g1='n', l='m', w='m', name='m.middleRightUp', isLower=True, base='m', accents=['flourish.middleRightUp2s'], comment='m simple flourish middle right upwards'),

    'n.bottomLeftDown': GD(g2='n', g1='n', l='n', w='n', name='n.bottomLeftDown', isLower=True, base='n', accents=['flourish.bottomLeftDown2x'], comment='n simple flourish bottom left downward'),
    'n.bottomLeftUp': GD(g2='n', g1='n', l='n', w='n', name='n.bottomLeftUp', isLower=True, base='n', accents=['flourish.bottomLeftUp1'], comment='n simple flourish bottom left upwards'),
    'n.bottomRightDown': GD(g2='n', g1='n', l='n', w='n', name='n.bottomRightDown', isLower=True, base='n', accents=['flourish.bottomRightDown2x'], comment='n simple flourish bottom right downward'),
    'n.bottomRightUp': GD(g2='n', g1='n', l='n', w='n', name='n.bottomRightUp', isLower=True, base='n', accents=['flourish.bottomRightUp1'], comment='n simple flourish bottom right upwards'),
    'n.topLeftDown': GD(g2='n', g1='n', l='n', w='n', name='n.topLeftDown', isLower=True, base='n', accents=['flourish.topLeftDown1'], comment='n simple flourish top left downward'),
    'n.topLeftUp': GD(g2='n', g1='n', l='n', w='n', name='n.topLeftUp', isLower=True, base='n', accents=['flourish.topLeftUp2xs'], comment='n simple flourish top left upwards'),
    'n.topRightUp': GD(g2='n', g1='n', l='n', w='n', name='n.topRightUp', isLower=True, base='n', accents=['flourish.topRightUp2'], comment='n simple flourish top right upwards'),
    # Flourishes on the side
    'n.middleLeftDown': GD(g2='n', g1='n', l='n', w='n', name='n.middleLeftDown', isLower=True, base='n', accents=['flourish.middleLeftDown2s'], comment='n simple flourish middle left downward'),
    'n.middleLeftUp': GD(g2='n', g1='n', l='n', w='n', name='n.middleLeftUp', isLower=True, base='n', accents=['flourish.middleLeftUp1s'], comment='n simple flourish middle left upwards'),
    'n.middleRightDown': GD(g2='n', g1='n',  l='n', w='n', name='n.middleRightDown', isLower=True, base='n', accents=['flourish.middleRightDown1s'], comment='n simple flourish middle right downward'),
    'n.middleRightUp': GD(g2='n', g1='n', l='n', w='n', name='n.middleRightUp', isLower=True, base='n', accents=['flourish.middleRightUp2s'], comment='n simple flourish middle right upwards'),

    'o.bottomLeftDown': GD(g2='o', g1='o', l='o', w='o', name='o.bottomLeftDown', isLower=True, base='o', accents=['flourish.bottomLeftDown2s'], comment='o simple flourish bottom left downward'),
    'o.bottomRightDown': GD(g2='o', g1='o', l='o', w='o', name='o.bottomRightDown', isLower=True, base='o', accents=['flourish.bottomRightDown2'], comment='o simple flourish bottom right downward'),
    'o.topLeftUp': GD(g2='o', g1='o', l='o', w='o', name='o.topLeftUp', isLower=True, base='o', accents=['flourish.topLeftUp2s'], comment='o simple flourish top left upwards'),
    'o.topRightUp': GD(g2='o', g1='o', l='o', w='o', name='o.topRightUp', isLower=True, base='o', accents=['flourish.topRightUp2'], comment='o simple flourish top right upwards'),
    # Flourishes on the side
    'o.middleLeftDown': GD(g2='o', g1='o', l='o', w='o', name='o.middleLeftDown', isLower=True, base='o', accents=['flourish.middleLeftDown2s'], comment='o simple flourish middle left downward'),
    'o.middleLeftUp': GD(g2='o', g1='o', l='o', w='o', name='o.middleLeftUp', isLower=True, base='o', accents=['flourish.middleLeftUp1s'], comment='o simple flourish middle left upwards'),
    'o.middleRightDown': GD(g2='o', g1='o',  l='o', w='o', name='o.middleRightDown', isLower=True, base='o', accents=['flourish.middleRightDown1s'], comment='o simple flourish middle right downward'),
    'o.middleRightUp': GD(g2='o', g1='o', l='o', w='o', name='o.middleRightUp', isLower=True, base='o', accents=['flourish.middleRightUp2s'], comment='o simple flourish middle right upwards'),

    'p.bottomLeftDown': GD(g2='p', g1='o', l='p', w='p', name='p.bottomLeftDown', isLower=True, base='p', accents=['flourish.bottomLeftDown2x'], comment='p simple flourish bottom left upwards'),
    'p.bottomLeftUp': GD(g2='p', g1='o', l='p', w='p', name='p.bottomLeftUp', isLower=True, base='p', accents=['flourish.bottomLeftUp1'], comment='p simple flourish bottom left upwards'),
    'p.bottomRightDown': GD(g2='p', g1='o', l='p', w='p', name='p.bottomRightDown', isLower=True, base='p', accents=['flourish.bottomRightDown2x'], comment='p simple flourish bottom right downward'),
    'p.bottomRightUp': GD(g2='p', g1='o', l='p', w='p', name='p.bottomRightUp', isLower=True, base='p', accents=['flourish.bottomRightUp1s'], comment='p simple flourish bottom right upward'),
    'p.topLeftDown': GD(g2='p', g1='o', l='p', w='p', name='p.topLeftDown', isLower=True, base='p', accents=['flourish.topLeftDown1'], comment='p simple flourish top left downward'),
    'p.topLeftUp': GD(g2='p', g1='o', l='p', w='p', name='p.topLeftUp', isLower=True, base='p', accents=['flourish.topLeftUp2xs'], comment='p simple flourish top left upwards'),
    'p.topRightUp': GD(g2='p', g1='o', l='p', w='p', name='p.topRightUp', isLower=True, base='p', accents=['flourish.topRightUp2'], comment='p simple flourish top right upwards'),
    # Flourishes on the side
    'p.middleLeftDown': GD(g2='p', g1='o', l='p', w='p', name='p.middleLeftDown', isLower=True, base='p', accents=['flourish.middleLeftDown2s'], comment='p simple flourish middle left downward'),
    'p.middleLeftUp': GD(g2='p', g1='o', l='p', w='p', name='p.middleLeftUp', isLower=True, base='p', accents=['flourish.middleLeftUp1s'], comment='p simple flourish middle left upwards'),
    'p.middleRightDown': GD(g2='p', g1='o',  l='p', w='p', name='p.middleRightDown', isLower=True, base='p', accents=['flourish.middleRightDown1s'], comment='p simple flourish middle right downward'),
    'p.middleRightUp': GD(g2='p', g1='o', l='p', w='p', name='p.middleRightUp', isLower=True, base='p', accents=['flourish.middleRightUp2s'], comment='p simple flourish middle right upwards'),

    'q.bottomLeftDown': GD(g2='o', g1='q', l='q', w='q', name='q.bottomLeftDown', isLower=True, base='q', accents=['flourish.bottomLeftDown2x'], comment='q simple flourish bottom left downward'),
    'q.bottomRightDown': GD(g2='o', g1='q', l='q', w='q', name='q.bottomRightDown', isLower=True, base='q', accents=['flourish.bottomRightDown2x'], comment='q simple flourish bottom left downward'),
    'q.bottomRightUp': GD(g2='o', g1='q', l='q', w='q', name='q.bottomRightUp', isLower=True, base='q', accents=['flourish.bottomRightUp1'], comment='q simple flourish bottom right upwards'),
    'q.topLeftUp': GD(g2='o', g1='q', l='q', w='q', name='q.topLeftUp', isLower=True, base='q', accents=['flourish.topLeftUp2s'], comment='q simple flourish top left upwards'),
    'q.topRightUp': GD(g2='o', g1='q', l='q', w='q', name='q.topRightUp', isLower=True, base='q', accents=['flourish.topRightUp2'], comment='q simple flourish top right upwards'),
    # Flourishes on the side
    'q.middleLeftDown': GD(g2='o', g1='q', l='q', w='q', name='q.middleLeftDown', isLower=True, base='q', accents=['flourish.middleLeftDown2s'], comment='q simple flourish middle left downward'),
    'q.middleLeftUp': GD(g2='o', g1='q', l='q', w='q', name='q.middleLeftUp', isLower=True, base='q', accents=['flourish.middleLeftUp1s'], comment='q simple flourish middle left upwards'),
    'q.middleRightDown': GD(g2='o', g1='q',  l='q', w='q', name='q.middleRightDown', isLower=True, base='q', accents=['flourish.middleRightDown1s'], comment='q simple flourish middle right downward'),
    'q.middleRightUp': GD(g2='o', g1='q', l='q', w='q', name='q.middleRightUp', isLower=True, base='q', accents=['flourish.middleRightUp2s'], comment='q simple flourish middle right upwards'),

    'r.bottomLeftDown': GD(g2='n', g1='r', l='r', w='r', name='r.bottomLeftDown', isLower=True, base='r', accents=['flourish.bottomLeftDown2x'], comment='r simple flourish bottom left downward'),
    'r.bottomLeftUp': GD(g2='n', g1='r', l='r', w='r', name='r.bottomLeftUp', isLower=True, base='r', accents=['flourish.bottomLeftUp1'], comment='r simple flourish bottom left upwards'),
    'r.bottomRightDown': GD(g2='n', g1='r', l='r', w='r', name='r.bottomRightDown', isLower=True, base='r', accents=['flourish.bottomRightDown2x'], comment='r simple flourish bottom right upward'),
    'r.bottomRightUp': GD(g2='n', g1='r', l='r', w='r', name='r.bottomRightUp', isLower=True, base='r', accents=['flourish.bottomRightUp1s'], comment='r simple flourish bottom right downward'),
    'r.topLeftDown': GD(g2='n', g1='r', l='r', w='r', name='r.topLeftDown', isLower=True, base='r', accents=['flourish.topLeftDown1'], comment='r simple flourish top left downward'),
    'r.topLeftUp': GD(g2='n', g1='r', l='r', w='r', name='r.topLeftUp', isLower=True, base='r', accents=['flourish.topLeftUp2xs'], comment='r simple flourish top left upwards'),
    'r.topRightUp': GD(g2='n', g1='r', l='r', w='r', name='r.topRightUp', isLower=True, base='r', accents=['flourish.topRightUp2'], comment='r simple flourish top right upwards'),
    # Flourishes on the side
    'r.middleLeftDown': GD(g2='n', g1='r', l='r', w='r', name='r.middleLeftDown', isLower=True, base='r', accents=['flourish.middleLeftDown2s'], comment='r simple flourish middle left downward'),
    'r.middleLeftUp': GD(g2='n', g1='r', l='r', w='r', name='r.middleLeftUp', isLower=True, base='r', accents=['flourish.middleLeftUp1s'], comment='r simple flourish middle left upwards'),
    'r.middleRightDown': GD(g2='n', g1='r',  l='r', w='r', name='r.middleRightDown', isLower=True, base='r', accents=['flourish.middleRightDown1s'], comment='r simple flourish middle right downward'),
    'r.middleRightUp': GD(g2='n', g1='r', l='r', w='r', name='r.middleRightUp', isLower=True, base='r', accents=['flourish.middleRightUp2s'], comment='r simple flourish middle right upwards'),

    's.bottomLeftDown': GD(g2='s', g1='s', l='s', w='s', name='s.bottomLeftDown', isLower=True, base='s', accents=['flourish.bottomLeftDown2s'], comment='s simple flourish bottom left downward'),
    's.bottomRightDown': GD(g2='s', g1='s', l='s', w='s', name='s.bottomRightDown', isLower=True, base='s', accents=['flourish.bottomRightDown2'], comment='s simple flourish bottom right downward'),
    's.topLeftUp': GD(g2='s', g1='s', l='s', w='s', name='s.topLeftUp', isLower=True, base='s', accents=['flourish.topLeftUp2s'], comment='s simple flourish top left upwards'),
    's.topRightUp': GD(g2='s', g1='s', l='s', w='s', name='s.topRightUp', isLower=True, base='s', accents=['flourish.topRightUp2'], comment='s simple flourish top right upwards'),
    # Flourishes on the side
    's.middleLeftDown': GD(g2='s', g1='s', l='s', w='s', name='s.middleLeftDown', isLower=True, base='s', accents=['flourish.middleLeftDown1s'], comment='s simple flourish middle left upwards'),
    's.middleRightUp': GD(g2='s', g1='s',  l='s', w='s', name='s.middleRightDown', isLower=True, base='s', accents=['flourish.middleRightUp1s'], comment='s simple flourish middle right downward'),
    's.middleLeftUp': GD(g2='s', g1='s', l='s', w='s', name='s.middleLeftUp', isLower=True, base='s', accents=['flourish.middleLeftUp1s'], comment='s simple flourish middle left upwards'),
    's.middleRightDown': GD(g2='s', g1='s',  l='s', w='s', name='s.middleRightDown', isLower=True, base='s', accents=['flourish.middleRightDown1s'], comment='s simple flourish middle right downward'),

    't.bottomLeftDown': GD(g2='t', g1='t', l='t', w='t', name='t.bottomLeftDown', isLower=True, base='t', accents=['flourish.bottomLeftDown2s'], comment='t simple flourish bottom left downward'),
    't.bottomRightDown': GD(g2='t', g1='t', l='t', w='t', name='t.bottomRightDown', isLower=True, base='t', accents=['flourish.bottomRightDown2'], comment='t simple flourish bottom right downward'),
    't.topLeftDown': GD(g2='t', g1='t', l='t', w='t', name='t.topLeftDown', isLower=True, base='t', accents=['flourish.topLeftDown2sl'], comment='t simple flourish top left downward'),
    't.topLeftUp': GD(g2='t', g1='t', l='t', w='t', name='t.topLeftUp', isLower=True, base='t', accents=['flourish.topLeftUp2'], comment='t simple flourish top left upwards'),
    't.topRightDown': GD(g2='t', g1='t', l='t', w='t', name='t.topRightDown', isLower=True, base='t', accents=['flourish.topRightDown2sl'], comment='t simple flourish top right downward'),
    't.topRightUp': GD(g2='t', g1='t', l='t', w='t', name='t.topRightUp', isLower=True, base='t', accents=['flourish.topRightUp2'], comment='t simple flourish top right upwards'),
    # Flourishes on the side
    't.middleLeftDown': GD(g2='t', g1='t', l='t', w='t', name='t.middleLeftDown', isLower=True, base='t', accents=['flourish.middleLeftDown2s'], comment='t simple flourish middle left downward'),
    't.middleLeftUp': GD(g2='t', g1='t', l='t', w='t', name='t.middleLeftUp', isLower=True, base='t', accents=['flourish.middleLeftUp1s'], comment='t simple flourish middle left upwards'),
    't.middleRightUp': GD(g2='t', g1='t', l='t', w='t', name='t.middleRightUp', isLower=True, base='t', accents=['flourish.middleRightUp1s'], comment='t simple flourish middle right upwards'),

    'u.bottomLeftDown': GD(g2='u', g1='u',l='u', w='u', name='u.bottomLeftDown', isLower=True, base='u', accents=['flourish.bottomLeftDown2s'], comment='u simple flourish bottom left downward'),
    'u.bottomRightDown': GD(g2='u', g1='u',l='u', w='u', name='u.bottomRightDown', isLower=True, base='u', accents=['flourish.bottomRightDown2xs'], comment='u simple flourish bottom right downward'),
    'u.bottomRightUp': GD(g2='u', g1='u', l='u', w='u', name='u.bottomRightUp', isLower=True, base='u', accents=['flourish.bottomRightUp1'], comment='u simple flourish bottom right upwards'),
    'u.topLeftDown': GD(g2='u', g1='u',l='u', w='u', name='u.topLeftDown', isLower=True, base='u', accents=['flourish.topLeftDown1'], comment='u simple flourish top left downward'),
    'u.topLeftUp': GD(g2='u', g1='u',l='u', w='u', name='u.topLeftUp', isLower=True, base='u', accents=['flourish.topLeftUp2xs'], comment='u simple flourish top left upwards'),
    'u.topRightUp': GD(g2='u', g1='u',l='u', w='u', name='u.topRightUp', isLower=True, base='u', accents=['flourish.topRightUp2xs'], comment='u simple flourish top right upwards'),
    'u.topRightDown': GD(g2='u', g1='u',l='u', w='u', name='u.topRightDown', isLower=True, base='u', accents=['flourish.topRightDown2sl'], comment='u simple flourish top right upwards'),
    # Flourishes on the side
    'u.middleLeftDown': GD(g2='u', g1='u', l='u', w='u', name='u.middleLeftDown', isLower=True, base='u', accents=['flourish.middleLeftDown2s'], comment='u simple flourish middle left downward'),
    'u.middleLeftUp': GD(g2='u', g1='u', l='u', w='u', name='u.middleLeftUp', isLower=True, base='u', accents=['flourish.middleLeftUp1s'], comment='u simple flourish middle left upwards'),
    'u.middleRightDown': GD(g2='u', g1='u',  l='u', w='u', name='u.middleRightDown', isLower=True, base='u', accents=['flourish.middleRightDown1s'], comment='u simple flourish middle right downward'),
    'u.middleRightUp': GD(g2='u', g1='u', l='u', w='u', name='u.middleRightUp', isLower=True, base='u', accents=['flourish.middleRightUp2s'], comment='u simple flourish middle right upwards'),

    'v.bottomLeftDown': GD(g2='v', g1='v', l='v', w='v', name='v.bottomLeftDown', isLower=True, base='v', accents=['flourish.bottomLeftDown2s'], comment='v simple flourish bottom left downward'),
    'v.bottomRightDown': GD(g2='v', g1='v', l='v', w='v', name='v.bottomRightDown', isLower=True, base='v', accents=['flourish.bottomRightDown2'], comment='v simple flourish bottom right downward'),
    'v.topLeftDown': GD(g2='v', g1='v', l='v', w='v', name='v.topLeftDown', isLower=True, base='v', accents=['flourish.topLeftDown1s'], comment='v simple flourish top left downward'),
    'v.topLeftUp': GD(g2='v', g1='v', l='v', w='v', name='v.topLeftUp', isLower=True, base='v', accents=['flourish.topLeftUp2xs'], comment='v simple flourish top left upwards'),
    'v.topRightDown': GD(g2='v', g1='v', l='v', w='v', name='v.topRightDown', isLower=True, base='v', accents=['flourish.topRightDown1s'], comment='v simple flourish top right downward'),
    'v.topRightUp': GD(g2='v', g1='v', l='v', w='v', name='v.topRightUp', isLower=True, base='v', accents=['flourish.topRightUp2xs'], comment='v simple flourish top right upwards'),
    # Flourishes on the side
    'v.middleLeftDown': GD(g2='v', g1='v', l='v', w='v', name='v.middleLeftDown', isLower=True, base='v', accents=['flourish.middleLeftDown2s'], comment='v simple flourish middle left downward'),
    'v.middleLeftUp': GD(g2='v', g1='v', l='v', w='v', name='v.middleLeftUp', isLower=True, base='v', accents=['flourish.middleLeftUp1d'], comment='v simple flourish middle left upwards'),
    'v.middleRightDown': GD(g2='v', g1='v',  l='v', w='v', name='v.middleRightDown', isLower=True, base='v', accents=['flourish.middleRightDown1s'], comment='v simple flourish middle right downward'),

    'w.bottomLeftDown': GD(g2='v', g1='v', l='w', w='w', name='w.bottomLeftDown', isLower=True, base='w', accents=['flourish.bottomLeftDown2s'], comment='w simple flourish bottom left downward'),
    'w.bottomRightDown': GD(g2='v', g1='v', l='w', w='w', name='w.bottomRightDown', isLower=True, base='w', accents=['flourish.bottomRightDown2'], comment='w simple flourish bottom right downward'),
    'w.topLeftDown': GD(g2='v', g1='v', l='w', w='w', name='w.topLeftDown', isLower=True, base='w', accents=['flourish.topLeftDown1s'], comment='w simple flourish top left downward'),
    'w.topLeftUp': GD(g2='v', g1='v', l='w', w='w', name='w.topLeftUp', isLower=True, base='w', accents=['flourish.topLeftUp2xs'], comment='w simple flourish top left upwards'),
    'w.topRightDown': GD(g2='v', g1='v', l='w', w='w', name='w.topRightDown', isLower=True, base='w', accents=['flourish.topRightDown1s'], comment='w simple flourish top right downward'),
    'w.topRightUp': GD(g2='v', g1='v', l='w', w='w', name='w.topRightUp', isLower=True, base='w', accents=['flourish.topRightUp2xs'], comment='w simple flourish top right upwards'),
    # Flourishes on the side
    'w.middleLeftDown': GD(g2='v', g1='v', l='w', w='w', name='w.middleLeftDown', isLower=True, base='w', accents=['flourish.middleLeftDown2s'], comment='w simple flourish middle left downward'),
    'w.middleLeftUp': GD(g2='v', g1='v', l='w', w='w', name='w.middleLeftUp', isLower=True, base='w', accents=['flourish.middleLeftUp1d'], comment='w simple flourish middle left upwards'),
    'w.middleRightDown': GD(g2='v', g1='v',  l='w', w='w', name='w.middleRightDown', isLower=True, base='w', accents=['flourish.middleRightDown1s'], comment='w simple flourish middle right downward'),

    'x.bottomLeftDown': GD(g2='x', g1='x', l='x', w='x', name='x.bottomLeftDown', isLower=True, base='x', accents=['flourish.bottomLeftDown2x'], comment='x simple flourish bottom left downward'),
    'x.bottomLeftUp': GD(g2='x', g1='x', l='x', w='x', name='x.bottomLeftUp', isLower=True, base='x', accents=['flourish.bottomLeftUp1'], comment='x simple flourish bottom left upwards'),
    'x.bottomRightDown': GD(g2='x', g1='x', l='x', w='x', name='x.bottomRightDown', isLower=True, base='x', accents=['flourish.bottomRightDown2x'], comment='x simple flourish bottom right downward'),
    'x.bottomRightUp': GD(g2='x', g1='x', l='x', w='x', name='x.bottomRightUp', isLower=True, base='x', accents=['flourish.bottomRightUp1'], comment='x simple flourish bottom right upwards'),
    'x.topLeftDown': GD(g2='x', g1='x', l='x', w='x', name='x.topLeftDown', isLower=True, base='x', accents=['flourish.topLeftDown1'], comment='x simple flourish top left downward'),
    'x.topLeftUp': GD(g2='x', g1='x', l='x', w='x', name='x.topLeftUp', isLower=True, base='x', accents=['flourish.topLeftUp2x'], comment='x simple flourish top left upwards'),
    'x.topRightDown': GD(g2='x', g1='x', l='x', w='x', name='x.topRightDown', isLower=True, base='x', accents=['flourish.topRightDown1'], comment='x simple flourish top right downward'),
    'x.topRightUp': GD(g2='x', g1='x', l='x', w='x', name='x.topRightUp', isLower=True, base='x', accents=['flourish.topRightUp2x'], comment='x simple flourish top right upwards'),
    # Flourishes on the side
    'x.middleLeftDown': GD(g2='x', g1='x', l='x', w='x', name='x.middleLeftDown', isLower=True, base='x', accents=['flourish.middleLeftDown1d'], comment='x simple flourish middle left downward'),
    'x.middleLeftUp': GD(g2='x', g1='x', l='x', w='x', name='x.middleLeftUp', isLower=True, base='x', accents=['flourish.middleLeftUp1d'], comment='x simple flourish middle left upwards'),
    'x.middleRightDown': GD(g2='x', g1='x',  l='x', w='x', name='x.middleRightDown', isLower=True, base='x', accents=['flourish.middleRightDown1d'], comment='x simple flourish middle right downward'),
    'x.middleRightUp': GD(g2='x', g1='x', l='x', w='x', name='x.middleRightUp', isLower=True, base='x', accents=['flourish.middleRightUp1d'], comment='x simple flourish middle right upwards'),

    'y.topLeftDown': GD(g2='y', g1='y', l='y', w='y', name='y.topLeftDown', isLower=True, base='y', accents=['flourish.topLeftDown1s'], comment='y simple flourish top left downward'),
    'y.topLeftUp': GD(g2='y', g1='y', l='y', w='y', name='y.topLeftUp', isLower=True, base='y', accents=['flourish.topLeftUp2x'], comment='y simple flourish top left upwards'),
    'y.topRightDown': GD(g2='y', g1='y', l='y', w='y', name='y.topRightDown', isLower=True, base='y', accents=['flourish.topRightDown1s'], comment='y simple flourish top right downward'),
    'y.topRightUp': GD(g2='y', g1='y', l='y', w='y', name='y.topRightUp', isLower=True, base='y', accents=['flourish.topRightUp2xs'], comment='y simple flourish top right upwards'),
    # Flourishes on the side
    'y.middleLeftDown': GD(g2='y', g1='y', l='y', w='y', name='y.middleLeftDown', isLower=True, base='y', accents=['flourish.middleLeftDown2s'], comment='y simple flourish middle left downward'),
    'y.middleLeftUp': GD(g2='y', g1='y', l='y', w='y', name='y.middleLeftUp', isLower=True, base='y', accents=['flourish.middleLeftUp1s'], comment='y simple flourish middle left upwards'),
    'y.middleRightDown': GD(g2='y', g1='y',  l='y', w='y', name='y.middleRightDown', isLower=True, base='y', accents=['flourish.middleRightDown1s'], comment='y simple flourish middle right downward'),

    'z.bottomLeftDown': GD(g2='z', g1='z', l='z', w='z', name='z.bottomLeftDown', isLower=True, base='z', accents=['flourish.bottomLeftDown2x'], comment='z simple flourish bottom left downward'),
    'z.bottomRightDown': GD(g2='z', g1='z', l='z', w='z', name='z.bottomRightDown', isLower=True, base='z', accents=['flourish.bottomRightDown2xs'], comment='z simple flourish bottom right downward'),
    'z.topLeftUp': GD(g2='z', g1='z', l='z', w='z', name='z.topLeftUp', isLower=True, base='z', accents=['flourish.topLeftUp2xs'], comment='z simple flourish top left upwards'),
    'z.topRightUp': GD(g2='z', g1='z', l='z', w='z', name='z.topRightUp', isLower=True, base='z', accents=['flourish.topRightUp2x'], comment='z simple flourish top right upwards'),
    # Flourishes on the side
    'z.middleLeftUp': GD(g2='z', g1='z', l='z', w='z', name='z.middleLeftUp', isLower=True, base='z', accents=['flourish.middleLeftUp1s'], comment='z simple flourish middle left upwards'),
    'z.middleRightUp': GD(g2='z', g1='z', l='z', w='z', name='z.middleRightUp', isLower=True, base='z', accents=['flourish.middleRightUp2s'], comment='z simple flourish middle right upwards'),
    'z.middleLeftDown': GD(g2='z', g1='z',  l='z', w='z', name='z.middleLeftDown', isLower=True, base='z', accents=['flourish.middleLeftDown2s'], comment='z simple flourish middle left downward'),
    'z.middleRightDown': GD(g2='z', g1='z',  l='z', w='z', name='z.middleRightDown', isLower=True, base='z', accents=['flourish.middleRightDown1s'], comment='z simple flourish middle right downward'),

    'exclam.bottomLeftDown': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.bottomLeftDown', base='exclam', accents=['flourish.bottomLeftDown2s'], comment='exclam simple flourish bottom left downward'),
    'exclam.bottomRightDown': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.bottomRightDown', base='exclam', accents=['flourish.bottomRightDown2'], comment='exclam simple flourish bottom right downward'),
    'exclam.topLeftUp': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.topLeftUp', base='exclam', accents=['flourish.topLeftUp2s'], comment='exclam simple flourish top left upwards'),
    'exclam.topRightUp': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.topRightUp', base='exclam', accents=['flourish.topRightUp2'], comment='exclam simple flourish top right upwards'),
    # Flourishes on the side
    'exclam.middleLeftDown': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.middleLeftDown', base='exclam', accents=['flourish.middleLeftDown2'], comment='exclam simple flourish middle left downward'),
    'exclam.middleLeftUp': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.middleLeftUp', base='exclam', accents=['flourish.middleLeftUp1s'], comment='exclam simple flourish middle left upwards'),
    'exclam.middleRightDown': GD(g2='exclam', g1='exclam',  l='exclam', w='exclam', name='exclam.middleRightDown', base='exclam', accents=['flourish.middleRightDown1s'], comment='exclam simple flourish middle right downward'),
    'exclam.middleRightUp': GD(g2='exclam', g1='exclam', l='exclam', w='exclam', name='exclam.middleRightUp', base='exclam', accents=['flourish.middleRightUp2'], comment='exclam simple flourish middle right upwards'),

    'question.bottomLeftDown': GD(g2='question', g1='question', l='question', w='question', name='question.bottomLeftDown', base='question', accents=['flourish.bottomLeftDown2s'], comment='question simple flourish bottom left downward'),
    'question.bottomRightDown': GD(g2='question', g1='question', l='question', w='question', name='question.bottomRightDown', base='question', accents=['flourish.bottomRightDown2'], comment='question simple flourish bottom right downward'),
    'question.topLeftUp': GD(g2='question', g1='question', l='question', w='question', name='question.topLeftUp', base='question', accents=['flourish.topLeftUp2s'], comment='question simple flourish top left upwards'),
    'question.topRightUp': GD(g2='question', g1='question', l='question', w='question', name='question.topRightUp', base='question', accents=['flourish.topRightUp2'], comment='question simple flourish top right upwards'),
    # Flourishes on the side
    'question.middleLeftDown': GD(g2='question', g1='question', l='question', w='question', name='question.middleLeftDown', base='question', accents=['flourish.middleLeftDown2'], comment='question simple flourish middle left downward'),
    'question.middleLeftUp': GD(g2='question', g1='question', l='question', w='question', name='question.middleLeftUp', base='question', accents=['flourish.middleLeftUp1s'], comment='question simple flourish middle left upwards'),
    'question.middleRightDown': GD(g2='question', g1='question',  l='question', w='question', name='question.middleRightDown', base='question', accents=['flourish.middleRightDown1s'], comment='question simple flourish middle right downward'),
    'question.middleRightUp': GD(g2='question', g1='question', l='question', w='question', name='question.middleRightUp', base='question', accents=['flourish.middleRightUp2'], comment='question simple flourish middle right upwards'),

    'exclamdown.bottomLeftDown': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.bottomLeftDown', base='exclamdown', accents=['flourish.bottomLeftDown2s'], comment='exclamdown simple flourish bottom left downward'),
    'exclamdown.bottomRightDown': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.bottomRightDown', base='exclamdown', accents=['flourish.bottomRightDown2'], comment='exclamdown simple flourish bottom right downward'),
    'exclamdown.topLeftUp': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.topLeftUp', base='exclamdown', accents=['flourish.topLeftUp2s'], comment='exclamdown simple flourish top left upwards'),
    'exclamdown.topRightUp': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.topRightUp', base='exclamdown', accents=['flourish.topRightUp2'], comment='exclamdown simple flourish top right upwards'),
    # Flourishes on the side
    'exclamdown.middleLeftDown': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.middleLeftDown', base='exclamdown', accents=['flourish.middleLeftDown2'], comment='exclamdown simple flourish middle left downward'),
    'exclamdown.middleLeftUp': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.middleLeftUp', base='exclamdown', accents=['flourish.middleLeftUp1s'], comment='exclamdown simple flourish middle left upwards'),
    'exclamdown.middleRightDown': GD(g2='exclamdown', g1='exclamdown',  l='exclamdown', w='exclamdown', name='exclamdown.middleRightDown', base='exclamdown', accents=['flourish.middleRightDown1s'], comment='exclamdown simple flourish middle right downward'),
    'exclamdown.middleRightUp': GD(g2='exclamdown', g1='exclamdown', l='exclamdown', w='exclamdown', name='exclamdown.middleRightUp', base='exclamdown', accents=['flourish.middleRightUp2'], comment='exclamdown simple flourish middle right upwards'),

    'questiondown.bottomLeftDown': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.bottomLeftDown', base='questiondown', accents=['flourish.bottomLeftDown2s'], comment='questiondown simple flourish bottom left downward'),
    'questiondown.bottomRightDown': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.bottomRightDown', base='questiondown', accents=['flourish.bottomRightDown2'], comment='questiondown simple flourish bottom right downward'),
    'questiondown.topLeftUp': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.topLeftUp', base='questiondown', accents=['flourish.topLeftUp2s'], comment='questiondown simple flourish top left upwards'),
    'questiondown.topRightUp': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.topRightUp', base='questiondown', accents=['flourish.topRightUp2'], comment='questiondown simple flourish top right upwards'),
    # Flourishes on the side
    'questiondown.middleLeftDown': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.middleLeftDown', base='questiondown', accents=['flourish.middleLeftDown2'], comment='questiondown simple flourish middle left downward'),
    'questiondown.middleLeftUp': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.middleLeftUp', base='questiondown', accents=['flourish.middleLeftUp1s'], comment='questiondown simple flourish middle left upwards'),
    'questiondown.middleRightDown': GD(g2='questiondown', g1='questiondown',  l='questiondown', w='questiondown', name='questiondown.middleRightDown', base='questiondown', accents=['flourish.middleRightDown1s'], comment='questiondown simple flourish middle right downward'),
    'questiondown.middleRightUp': GD(g2='questiondown', g1='questiondown', l='questiondown', w='questiondown', name='questiondown.middleRightUp', base='questiondown', accents=['flourish.middleRightUp2'], comment='questiondown simple flourish middle right upwards'),

    'at.bottomLeftDown': GD(g2='at', g1='at', l='at', w='at', name='at.bottomLeftDown', base='at', accents=['flourish.bottomLeftDown2s'], comment='at simple flourish bottom left downward'),
    'at.bottomRightDown': GD(g2='at', g1='at', l='at', w='at', name='at.bottomRightDown', base='at', accents=['flourish.bottomRightDown2'], comment='at simple flourish bottom right downward'),
    'at.topLeftUp': GD(g2='at', g1='at', l='at', w='at', name='at.topLeftUp', base='at', accents=['flourish.topLeftUp2s'], comment='at simple flourish top left upwards'),
    'at.topRightUp': GD(g2='at', g1='at', l='at', w='at', name='at.topRightUp', base='at', accents=['flourish.topRightUp2'], comment='at simple flourish top right upwards'),
    # Flourishes on the side
    'at.middleLeftDown': GD(g2='at', g1='at', l='at', w='at', name='at.middleLeftDown', base='at', accents=['flourish.middleLeftDown2'], comment='at simple flourish middle left downward'),
    'at.middleLeftUp': GD(g2='at', g1='at', l='at', w='at', name='at.middleLeftUp', base='at', accents=['flourish.middleLeftUp1s'], comment='at simple flourish middle left upwards'),
    'at.middleRightDown': GD(g2='at', g1='at',  l='at', w='at', name='at.middleRightDown', base='at', accents=['flourish.middleRightDown1s'], comment='at simple flourish middle right downward'),
    'at.middleRightUp': GD(g2='at', g1='at', l='at', w='at', name='at.middleRightUp', base='at', accents=['flourish.middleRightUp2'], comment='at simple flourish middle right upwards'),

}

# Special version for italic with changed spacing rules
GLYPH_DATA_ITALIC = gids = deepcopy(GLYPH_DATA)

# For /a connectors bottom right are the same for roman and italic
# Ignore the left shape difference for /a and /ae in italic: keep in the same group.
gids['ae'] = GD(g2='ae', g1='e', mr='e', uni=0x00e6, c='æ', name='ae', isLower=True, comment='æ small ligature ae, latin')
gids['aeacute'] = GD(g2='ae', g1='e', l='ae', w='ae', uni=0x01fd, c='ǽ', name='aeacute', base='ae', isLower=True, accents=['acutecmb'], comment='ǽ')

gids['a'] = GD(g2='o', g1='a', l='o', uni=0x0061, c='a', name='a', comment='a Small Letters, Latin')
gids['aacute'].g2 = 'o'
gids['abreve'].g2 = 'o'
gids['acircumflex'].g2 = 'o'
gids['adieresis'].g2 = 'o'
gids['agrave'].g2 = 'o'
gids['amacron'].g2 = 'o'
gids['aring'].g2 = 'o'
gids['atilde'].g2 = 'o'
gids['aringacute'].g2 = 'o'
gids['aogonek'].g2 = 'o'

gids['a.bottomLeftDown'].g2 = 'o'
gids['a.bottomRightDown'].g2 = 'o'
gids['a.bottomRightUp'].g2 = 'o'
gids['a.cbr'].g2 = 'o'
gids['a.topLeftUp'].g2 = 'o'
gids['a.topRightUp'].g2 = 'o'
gids['a.middleLeftDown'].g2 = 'o'
gids['a.middleLeftUp'].g2 = 'o'
gids['a.middleRightDown'].g2 = 'o'
gids['a.middleRightUp'].g2 = 'o'

gids['b'] = GD(g2='l', g1='o', l='h', r='o', uni=0x0062, c='b', name='b', comment='b')
gids['b.topLeftDown'] = GD(g2='l', g1='b', l='l', w='b', name='b.topLeftDown', base='b', accents=['flourish.topLeftDown2sl'], comment='b simple flourish bottom right upwards')

gids['d'] = GD(g2='o', g1='l', l='o', r='u', uni=0x0064, c='d', name='d', comment='d', anchors=CARON_ANCHORS)
gids['d.cbr'] = GD(g2='o', g1='l', l='d', w='d', name='d.cbr', template='d', src='d', copyFromDisplayRight=False, anchors=CARON_ANCHORS, comment='d Small Letters, Latin - connector bottom')
gids['d.topLeftDown'] = GD(g2='o', g1='l', l='d', w='d', name='d.topLeftDown', base='d', copyFromDisplayRight=False, accents=['flourish.topLeftUp2sl'], comment='d simple flourish bottom right upwards')
gids['d.bottomRightUp'] = GD(g2='o', g1='l', l='d', w='d', name='d.bottomRightUp', base='d.cbr', copyFromDisplayRight=False, accents=['flourish.bottomRightUp1s'], comment='d simple flourish bottom right upwards')
gids['d.bottomRightDown'] = GD(g2='o', g1='l', l='d', w='d', name='d.bottomRightDown', base='d.cbr', copyFromDisplayRight=False, accents=['flourish.bottomRightDown2s'], comment='d simple flourish bottom right downward')
gids['dcaron'].g2 = 'o'
gids['dcroat'].g2 = 'o'
gids['d.bottomLeftDown'].g2 = 'o'
gids['d.bottomRightUp'].g2 = 'o'
gids['d.topLeftDown'].g2 = 'o'
gids['d.topLeftUp'].g2 = 'o'
gids['d.topRightUp'].g2 = 'o'
gids['d.middleLeftDown'].g2 = 'o'
gids['d.middleLeftUp'].g2 = 'o'
gids['d.middleRightDown'].g2 = 'o'
gids['d.middleRightUp'].g2 = 'o'

gids['f'] = GD(g2='f', g1='f', rightMin=MIN_RIGHT, fixAnchors=False, uni=0x0066, c='f', name='f', comment='f', copyFromDisplayRight=False)
gids['f.bottomLeftDown'] = GD(g2='f', g1='f', l='f', w='f', name='f.bottomLeftDown', base='f', accents=['flourish.bottomLeftDown2'], copyFromDisplayRight=False, comment='f simple flourish bottom left downward')
gids['florin'] = GD(g2='f', g1='f', w='f', uni=0x0192, c='ƒ', name='florin', src='f', copyFromDisplayRight=False, comment='ƒ script f, latin small letter')
# Does not exist in Presti Italic
del gids['f.bottomRightUp']
del gids['f.bottomRightDown']

gids['g'] = GD(g2='o', g1='g', l='o', r='jdotless', uni=0x0067, c='g', name='g', comment='g')
gids['g.topRightUp'] = GD(g2='o', g1='g', l='g', w='g', name='g.topRightUp', base='g', accents=['flourish.topRightUp2'], comment='g simple flourish top right upwards')
# Keep earlessg in italic for compatibility
gids['earlessg'] = GD(g2='o', g1='g', l='g', w='g', name='earlessg', base='g', comment='In Roman g with ear to accommodate accents. Italic is just a g component')
gids['gbreve'] = GD(g2='o', g1='g', l='g', w='g', uni=0x011f, c='ğ', name='gbreve', base='g', accents=['brevecmb'], comment='ğ G WITH BREVE, LATIN SMALL LETTER')
gids['gcaron'] = GD(g2='o', g1='g', l='g', w='g', uni=0x01e7, c='ǧ', name='gcaron', base='g', accents=['caroncmb'], comment='ǧ G WITH CARON, LATIN SMALL LETTER')
gids['gcircumflex'] = GD(g2='o', g1='g', l='g', w='g', uni=0x011d, c='ĝ', name='gcircumflex', base='g', accents=['circumflexcmb'], comment='ĝ G WITH CIRCUMFLEX, LATIN SMALL LETTER')
gids['gcommaaccent'].g2 = 'o'
gids['gdotaccent'].g2 = 'o'

gids['g.bottomLeftDown'].g2 = 'o'
gids['g.bottomRightDown'].g2 = 'o'
gids['g.topLeftUp'].g2 = 'o'
gids['g.topRightUp'].g2 = 'o'
gids['g.middleLeftDown'].g2 = 'o'
gids['g.middleLeftUp'].g2 = 'o'
gids['g.middleRightDown'].g2 = 'o'
gids['g.middleRightUp'].g2 = 'o'

gids['h'] = GD(g2='l', g1='n', r='n', uni=0x0068, c='h', name='h', comment='h', topY=TOP_Y)
gids['h.cbr'] = GD(g2='l', g1='n', l='l', w='h', template='h', src='h', name='h.cbr', copyFromDisplayRight=False, comment='h Small Letters, Latin - connector bottom')
gids['h.topLeftDown'] = GD(g2='l', g1='n', l='h', w='h', name='h.topLeftDown', base='h', copyFromDisplayRight=False, accents=['flourish.topLeftDown2sl'], comment='h simple flourish bottom right upwards')
gids['h.bottomRightUp'] = GD(g2='l', g1='n', l='h', w='h.cbr', name='h.bottomRightUp', copyFromDisplayRight=False, base='h.cbr', accents=['flourish.bottomRightUp1s'], comment='h simple flourish bottom right upwards')
gids['h.bottomRightDown'] = GD(g2='l', g1='n', l='h', w='h.cbr', name='h.bottomRightDown', copyFromDisplayRight=False, base='h.cbr', accents=['flourish.bottomRightDown2s'], comment='h simple flourish bottom right downward')
gids['h.bottomLeftUp'] = GD(g2='l', g1='n', l='h', w='h', name='h.bottomLeftUp', base='h', accents=['flourish.bottomLeftUp2sl'], comment='h simple flourish bottom left upward')
gids['h.bottomLeftDown'] = GD(g2='l', g1='n', l='h', w='h', name='h.bottomLeftDown', base='h', accents=['flourish.bottomLeftDown2s'], comment='h simple flourish bottom left downward')

gids['idotless'] =  GD(g2='i', g1='i', l='n', r='n', name='idotless', comment='i - connector bottom right', anchors=ALL_IJ_ANCHORS)
gids['i'] =  GD(g2='i', g1='i', l='idotless', w='idotless', name='i', uni=0x0069, c='i', comment='i - connector bottom right', anchors=ALL_IJ_ANCHORS)
gids['i.cbr'] =  GD(g2='i', g1='i', l='n', w='i', name='i.cbr', copyFromDisplayRight=False, comment='i - connector bottom right', anchors=ALL_IJ_ANCHORS)
gids['i.topLeftDown'] = GD(g2='i', g1='i', l='i', w='i', name='i.topLeftDown', base='i', accents=['flourish.topLeftDown2sl'], comment='i simple flourish top left downward', anchors=ALL_IJ_ANCHORS)
gids['i.bottomRightUp'] = GD(g2='i', g1='i', l='i', w='i.cbr', name='i.bottomRightUp', base='i.cbr', accents=['flourish.bottomRightUp1s'], comment='i simple flourish bottom right upwards', anchors=ALL_IJ_ANCHORS)
gids['i.bottomRightDown'] = GD(g2='i', g1='i', l='i', w='i.cbr', name='i.bottomRightDown', base='i.cbr', accents=['flourish.bottomRightDown2s'], comment='i simple flourish bottom right downward', anchors=ALL_IJ_ANCHORS)
gids['i.bottomLeftUp'] = GD(g2='i', g1='i', l='i', w='i', name='i.bottomLeftUp', base='i', accents=['flourish.bottomLeftUp2sl'], comment='i simple flourish bottom left upward', anchors=ALL_IJ_ANCHORS)
gids['i.bottomLeftDown'] = GD(g2='i', g1='i', l='i', w='i', name='i.bottomLeftDown', base='i', accents=['flourish.bottomLeftDown2s'], comment='i simple flourish bottom left downward', anchors=ALL_IJ_ANCHORS)

gids['k'] = GD(g2='l', g1='k', l='h', uni=0x006b, c='k', name='k', comment='k')
gids['k.cbr'] = GD(g2='l', g1='k', l='l', w='k', name='k.cbr', template='k', src='k', copyFromDisplayRight=False, comment='k - connector bottom')
gids['kcommaaccent'] = GD(g2='l', g1='k', uni=0x0137, c='ķ', name='kcommaaccent', isLower=True, base='k', accents=['commabelowcmb'])
gids['k.topRightUp'] = GD(g2='l', g1='k', l='k', w='k', name='k.topRightUp', base='k.cbr', accents=['flourish.topRightUp2'], comment='k simple flourish bottom right upwards')
gids['k.topRightDown'] = GD(g2='l', g1='k', l='k', w='k', name='k.topRightDown', base='k', accents=['flourish.topRightDown2sl'], comment='k simple flourish top right downwards')
gids['k.topLeftDown'] = GD(g2='l', g1='k', l='k', w='k', name='k.topLeftDown', base='k', accents=['flourish.topLeftDown2sl'], comment='k simple flourish top left downwards')
gids['k.bottomRightUp'] = GD(g2='l', g1='k', l='k', w='k.cbr', name='k.bottomRightUp', base='k.cbr', accents=['flourish.bottomRightUp1s'], comment='k simple flourish bottom right upwards')
gids['k.bottomRightDown'] = GD(g2='l', g1='k', l='k', w='k.cbr', name='k.bottomRightDown', base='k.cbr', accents=['flourish.bottomRightDown2'], comment='k simple flourish bottom right downward')
gids['k.bottomLeftUp'] = GD(g2='l', g1='k', l='k', w='k', name='k.bottomLeftUp', base='k', accents=['flourish.bottomLeftUp2sl'], comment='k simple flourish bottom left upward')
gids['k.bottomLeftDown'] = GD(g2='l', g1='k', l='k', w='k', name='k.bottomLeftDown', base='k', accents=['flourish.bottomLeftDown2s'], comment='k simple flourish bottom left downward')
gids['k.middleRightDown'] = GD(g2='l', g1='k',  l='k', w='k', name='k.middleRightDown', isLower=True, base='k', accents=['flourish.middleRightDown1'], comment='k simple flourish middle right downward')
gids['k.middleRightUp'] = GD(g2='l', g1='k', l='k', w='k', name='k.middleRightUp', isLower=True, base='k', accents=['flourish.middleRightUp1'], comment='k simple flourish middle right upwards')

# Italic has round bottom, more line /i than /h
gids['l'] = GD(g2='l', g1='l', l='h', r='n', uni=0x006c, c='l', name='l', comment='l', anchors=CARON_ANCHORS, topY=TOP_Y)
gids['l.cbr'] = GD(g2='l', g1='l', l='l', w='l', name='l.cbr', template='l', src='l', copyFromDisplayRight=False, anchors=CARON_ANCHORS, comment='l - connector bottom')
gids['lacute'] = GD(g2='l', g1='l', l='l', w='l', uni=0x013a, c='ĺ', name='lacute', isLower=True, base='l', accents=['acutecmb.uc'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER')
gids['lcaron'] = GD(g2='l', g1='dcaron', l='l', mr='comma', uni=0x013e, c='ľ', name='lcaron', base='l', isLower=True, accents=['caroncmb.vert'], comment='ľ L WITH CARON, LATIN SMALL LETTER')
gids['lcommaaccent'] = GD(g2='l', g1='l', l='l', w='l', uni=0x013c, c='ļ', name='lcommaaccent',isLower=True, base='l', accents=['commabelowcmb'])
gids['ldot'] = GD(g2='l', g1='ldot', l='l', uni=0x0140, c='ŀ', name='ldot', isLower=True, base='l', accents=['dotmiddlecmb'], comment='ŀ MIDDLE DOT, LATIN SMALL LETTER L WITH')
gids['lslash'] = GD(g2='l', g1='l', l='l', w='l', uni=0x0142, c='ł', name='lslash', isLower=True, base='l', comment='ł L WITH STROKE, LATIN SMALL LETTER')

gids['l.topLeftDown'] = GD(g2='l', g1='l', l='l', w='l', name='l.topLeftDown', base='l', accents=['flourish.topLeftDown2sl'], comment='l simple flourish top left downward')
gids['l.bottomRightUp'] = GD(g2='l', g1='l', l='l', w='l.cbr', name='l.bottomRightUp', base='l.cbr', accents=['flourish.bottomRightUp1s'], comment='l simple flourish bottom right upwards')
gids['l.bottomRightDown'] = GD(g2='l', g1='l', l='l', w='l.cbr', name='l.bottomRightDown', base='l.cbr', accents=['flourish.bottomRightDown2s'], comment='l simple flourish bottom right downward')
gids['l.bottomLeftDown'] = GD(g2='l', g1='l', l='l', w='l', name='l.bottomLeftDown', base='l', accents=['flourish.bottomLeftDown2'], comment='l simple flourish bottom left downward')
del gids['l.bottomLeftUp'] # Not for italic

gids['m.cbr'] = GD(g2='n', l='n', w='m', name='m.cbr', template='m', src='m', copyFromDisplayRight=False, comment='m - connector bottom')
gids['m.topLeftDown'] = GD(g2='n', g1='n', l='m', w='m', name='m.topLeftDown', base='m', accents=['flourish.topLeftDown2sl'], comment='n simple flourish top left downward')
gids['m.bottomRightUp'] = GD(g2='n', g1='n', l='m', w='m', name='m.bottomRightUp', base='m.cbr', accents=['flourish.bottomRightUp1s'], comment='m simple flourish bottom right upwards')
gids['m.bottomRightDown'] = GD(g2='n', g1='n', l='m', w='m', name='m.bottomRightDown', base='m.cbr', accents=['flourish.bottomRightDown2'], comment='m simple flourish bottom right downward')
gids['m.bottomLeftUp'] = GD(g2='n', g1='n', l='m', w='m', name='m.bottomLeftUp', base='m', accents=['flourish.bottomLeftUp2sl'], comment='m simple flourish bottom left upward')
gids['m.bottomLeftDown'] = GD(g2='n', g1='n', l='m', w='m', name='m.bottomLeftDown', base='m', accents=['flourish.bottomLeftDown2s'], comment='m simple flourish bottom left downward')

gids['n.cbr'] = GD(g2='n', l='n', w='n', name='n.cbr', template='n', src='n', copyFromDisplayRight=False, comment='n - connector bottom')
gids['n.topLeftDown'] = GD(g2='n', g1='n', l='n', w='n', name='n.topLeftDown', base='n', accents=['flourish.topLeftDown2sl'], comment='n simple flourish top left downward')
gids['n.bottomRightUp'] = GD(g2='n', g1='n', l='n', w='n', name='n.bottomRightUp', base='n.cbr', accents=['flourish.bottomRightUp1s'], comment='n simple flourish bottom right upwards')
gids['n.bottomRightDown'] = GD(g2='n', g1='n', l='n', w='n', name='n.bottomRightDown', base='n.cbr', accents=['flourish.bottomRightDown2'], comment='n simple flourish bottom right downward')
gids['n.bottomLeftUp'] = GD(g2='n', g1='n', l='n', w='n', name='n.bottomLeftUp', base='n', accents=['flourish.bottomLeftUp2sl'], comment='n simple flourish bottom left upward')
gids['n.bottomLeftDown'] = GD(g2='n', g1='n', l='n', w='n', name='n.bottomLeftDown', base='n', accents=['flourish.bottomLeftDown2s'], comment='n simple flourish bottom left downward')

gids['r.bottomLeftUp'] = GD(g2='n', g1='r', l='r', w='r', name='r.bottomLeftUp', base='r', accents=['flourish.bottomLeftUp2sl'], comment='r simple flourish bottom left upward')
gids['r.bottomLeftDown'] = GD(g2='n', g1='r', l='r', w='r', name='r.bottomLeftDown', base='r', accents=['flourish.bottomLeftDown2s'], comment='r simple flourish bottom left downward')
gids['r.bottomRightDown'] = GD(g2='n', g1='r', l='r', w='r', name='r.bottomRightDown', base='r', accents=['flourish.bottomRightDown2'], comment='r simple flourish bottom left downward')

gids['p.bottomRightDown'] = GD(g2='p', g1='o', l='p', w='p', name='p.bottomRightDown', base='p', accents=['flourish.bottomRightDown2'], comment='p simple flourish bottom right downward')
gids['p.bottomLeftDown'] = GD(g2='p', g1='o', l='p', w='p', name='p.bottomLeftDown', base='p', accents=['flourish.bottomLeftDown2'], comment='p simple flourish bottom left upwards')
gids['p.bottomLeftUp'] = GD(g2='p', g1='o', l='p', w='p', name='p.bottomLeftUp', base='p', accents=['flourish.bottomLeftUp2sl'], comment='p simple flourish bottom left upward')
gids['p.bottomRightUp'] = GD(g2='p', g1='o', l='p', w='p', name='p.bottomRightUp', base='p', accents=['flourish.bottomRightUp2sl'], comment='p simple flourish bottom right upwards')

gids['q.bottomRightDown'] = GD(g2='o', g1='q', l='q', w='q', name='q.bottomRightDown', base='q', accents=['flourish.bottomRightDown2s'], comment='q simple flourish bottom left downward')
gids['q.bottomLeftDown'] = GD(g2='o', g1='q', l='q', w='q', name='q.bottomLeftDown', base='q', accents=['flourish.bottomLeftDown2s'], comment='q simple flourish bottom left downward')
del gids['q.bottomRightUp'] # Does not exist in Presti Italic

gids['thorn'] = GD(g2='l', g1='o', l='h', r='p', uni=0x00fe, c='þ', name='thorn', src='p', comment='þ THORN, LATIN SMALL LETTER')

gids['u'] = GD(g2='u', g1='u', r='a', uni=0x0075, c='u', name='u', comment='u')
gids['uogonek'] = GD(g2='u', g1='u', l='u', w='u', uni=0x0173, c='ų', name='uogonek', isLower=True, base='u', accents=['ogonekcmb'], comment='ų U WITH OGONEK, LATIN SMALL LETTER')
gids['u.cbr'] = GD(g2='u', g1='u', l='u', w='u', name='u.cbr', template='u', src='u', copyFromDisplayRight=False, comment='n - connector bottom')
gids['u.bottomRightDown'] = GD(g2='u', g1='u', l='u', w='u', name='u.bottomRightDown', base='u.cbr', accents=['flourish.bottomRightDown2'], comment='u simple flourish bottom right downward')
gids['u.bottomRightUp'] = GD(g2='u', g1='u', l='u', w='u', name='u.bottomRightUp', base='u.cbr', accents=['flourish.bottomRightUp1s'], comment='u simple flourish bottom right upwards')
gids['u.topLeftDown'] = GD(g2='u', g1='u', l='u', w='u', name='u.topLeftDown', base='u', accents=['flourish.topLeftDown2sl'], comment='u simple flourish top left downwards')
gids['u.topRightDown'] = GD(g2='u', g1='u', l='u', w='u', name='u.topRightDown', base='u', accents=['flourish.topRightDown2sl'], comment='u simple flourish top right downward')
gids['u.topRightUp'] = GD(g2='u', g1='u', l='u', w='u', name='u.topRightUp', base='u', accents=['flourish.topRightUp2'], comment='u simple flourish top right downward')

gids['v'] = GD(g2='v', g1='v', uni=0x0076, c='v', name='v', comment='v LATIN SMALL LETTER V')
gids['v.topLeftDown'] = GD(g2='v', g1='v', l='v', w='v', name='v.topLeftDown', base='v', accents=['flourish.topLeftDown2sl'], comment='v simple flourish bottom left downward')
gids['v.topRightDown'] = GD(g2='v', g1='v', l='v', w='v', name='v.topRightDown', base='v', accents=['flourish.topRightDown2sl'], comment='v simple flourish top right downward')
gids['v.topRightUp'] = GD(g2='v', g1='v', l='v', w='v', name='v.topRightUp', base='v', accents=['flourish.topRightUp2s'], comment='v simple flourish top right upward')
gids['v.middleLeftDown'] = GD(g2='v', g1='v',  l='v', w='v', name='v.middleLeftDown', base='v', accents=['flourish.middleLeftDown2'], comment='v simple flourish middle left downward')
gids['v.middleLeftUp'] = GD(g2='v', g1='v', l='v', w='v', name='v.middleLeftUp', base='v', accents=['flourish.middleLeftUp1'], comment='v simple flourish middle left upwards')
gids['v.middleRightDown'] = GD(g2='v', g1='v',  l='v', w='v', name='v.middleRightDown', base='v', accents=['flourish.middleRightDown1s'], comment='v simple flourish middle right downward')
# Does not exist in Presti Roman
gids['v.middleRightUp'] = GD(g2='v', g1='v', l='v', w='v', name='v.middleRightUp', base='v', accents=['flourish.middleRightUp1s'], comment='v simple flourish middle right upwards')

gids['w'] = GD(g2='v', g1='v', l='v', r='v', uni=0x0077, c='w', name='w', isLower=True, comment='w LATIN SMALL LETTER W')
gids['wacute'].l = 'v'
gids['wcircumflex'].l = 'v'
gids['wdieresis'].l = 'v'
gids['wgrave'].l = 'v'
gids['w.topLeftDown'] = GD(g2='v', g1='v', l='v', w='w', name='w.topLeftDown', base='w', accents=['flourish.topLeftDown2sl'], comment='w simple flourish bottom left downward')
gids['w.topRightDown'] = GD(g2='v', g1='v', l='v', w='w', name='w.topRightDown', base='w', accents=['flourish.topRightDown2sl'], comment='w simple flourish top right downward')
gids['w.topRightUp'] = GD(g2='v', g1='v', l='v', w='w', name='w.topRightUp', base='w', accents=['flourish.topRightUp2s'], comment='w simple flourish top right upward')
gids['w.middleLeftDown'] = GD(g2='v', g1='v',  l='v', w='w', name='w.middleLeftDown', base='w', accents=['flourish.middleLeftDown2'], comment='w simple flourish middle left downward')
gids['w.middleLeftUp'] = GD(g2='v', g1='v', l='v', w='w', name='w.middleLeftUp', base='w', accents=['flourish.middleLeftUp1'], comment='w simple flourish middle left upwards')
gids['w.middleRightDown'] = GD(g2='v', g1='v',  l='v', w='w', name='w.middleRightDown', base='w', accents=['flourish.middleRightDown1s'], comment='w simple flourish middle right downward')
# Does not exist in Presti Roman
gids['w.middleRightUp'] = GD(g2='v', g1='v', l='v', w='w', name='w.middleRightUp', base='w', accents=['flourish.middleRightUp1s'], comment='w simple flourish middle right upwards')

gids['x'] = GD(g2='x', g1='x', l2r='x', uni=0x0078, c='x', name='x', comment='x LATIN SMALL LETTER X')
gids['x.cbr'] = GD(g2='x', g1='x', l='x', name='x.cbr', template='x', src='x', copyFromDisplayRight=False, comment='x LATIN SMALL LETTER X')
gids['x.bottomLeftDown'] = GD(g2='x', g1='x', l='x', w='x', name='x.bottomLeftDown', base='x', accents=['flourish.bottomLeftDown2s'], comment='x simple flourish bottom left downwards')
gids['x.bottomLeftUp'] = GD(g2='x', g1='x', l='x', w='x', name='x.bottomLeftUp', base='x', accents=['flourish.bottomLeftUp2sl'], comment='x simple flourish bottom left upwards')
gids['x.bottomRightDown'] = GD(g2='x', g1='x', l='x', w='x', name='x.bottomRightDown', base='x.cbr', accents=['flourish.bottomRightDown2s'], comment='x simple flourish bottom right downward')
gids['x.bottomRightUp'] = GD(g2='x', g1='x', l='x', w='x', name='x.bottomRightUp', base='x.cbr', accents=['flourish.bottomRightUp2sl'], comment='x simple flourish bottom right upward')
gids['x.topLeftUp'] = GD(g2='x', g1='x', l='x', w='x', name='x.topLeftUp', base='x', accents=['flourish.topLeftUp2s'], comment='x simple flourish top right upwards')
gids['x.topRightDown'] = GD(g2='x', g1='x', l='x', w='x', name='x.topRightDown', base='x', accents=['flourish.topRightDown2sl'], comment='x simple flourish top right upwards')
gids['x.topRightUp'] = GD(g2='x', g1='x', l='x', w='x', name='x.topRightUp', base='x', accents=['flourish.topRightUp2'], comment='x simple flourish top right upwards')
gids['x.middleLeftDown'] = GD(g2='x', g1='x', l='x', w='x', name='x.middleLeftDown', isLower=True, base='x', accents=['flourish.middleLeftDown1'], comment='x simple flourish middle left downward')
gids['x.middleLeftUp'] = GD(g2='x', g1='x', l='x', w='x', name='x.middleLeftUp', isLower=True, base='x', accents=['flourish.middleLeftUp1'], comment='x simple flourish middle left upwards')
gids['x.middleRightDown'] = GD(g2='x', g1='x',  l='x', w='x', name='x.middleRightDown', isLower=True, base='x', accents=['flourish.middleRightDown1'], comment='x simple flourish middle right downward')
gids['x.middleRightUp'] = GD(g2='x', g1='x', l='x', w='x', name='x.middleRightUp', isLower=True, base='x', accents=['flourish.middleRightUp1'], comment='x simple flourish middle right upwards')

gids['y'] = GD(g2='y', g1='y', uni=0x0079, c='y', name='y', comment='y LATIN SMALL LETTER Y', smallTrackRight=0)
gids['y.topLeftUp'] = GD(g2='y', g1='y', l='y', w='y', name='y.topLeftUp', isLower=True, base='y', accents=['flourish.topLeftUp2xs'], comment='y simple flourish top left upwards')
del gids['y.topRightDown'] # Does not exist in Presti Italic
gids['y.topLeftDown'].smallTrackRight = 0
gids['y.topLeftUp'].smallTrackRight = 0
gids['y.topRightUp'].smallTrackRight = 0
gids['y.topRightUp'].accents=['flourish.topRightUp2']
gids['y.middleLeftDown'].smallTrackRight = 0
gids['y.middleLeftDown'].accents = ['flourish.middleLeftUp1d']
gids['y.middleLeftUp'].tracksmallTrackRightRight = 0
gids['y.middleLeftUp'].accents = ['flourish.middleLeftDown1d']
gids['y.middleRightDown'].trasmallTrackRightckRight = 0

gids['z.bottomLeftDown'] = GD(g2='z', g1='z', l='z', w='z', name='z.bottomLeftDown', base='z', accents=['flourish.bottomLeftDown2'], comment='z simple flourish bottom left downward')
gids['z.bottomRightDown'] = GD(g2='z', g1='z', l='z', w='z', name='z.bottomRightDown', base='z', accents=['flourish.bottomRightDown2s'], comment='z simple flourish bottom right downward')
gids['z.topLeftUp'] = GD(g2='z', g1='z', l='z', w='z', name='z.topLeftUp', base='z', accents=['flourish.topLeftUp2s'], comment='z simple flourish top left upwards')
gids['z.topRightUp'] = GD(g2='z', g1='z', l='z', w='z', name='z.topRightUp', base='z', accents=['flourish.topRightUp2'], comment='z simple flourish top right upwards')

gids['R'] = GD(g2='H', g1='R', l='H', uni=0x0052, c='R', name='R', comment='R')

gids['ampersand'] = GD(g2='ampersand', g1='ampersand', r2l='three', uni=0x0026, c='&', name='ampersand', comment='& AMPERSAND', height=CAP_HEIGHT, overshoot=CAP_OVERSHOOT)
gids['ampersand.sc'] = GD(g2='ampersand.sc', g1='ampersand.sc', l='ampersand', r='ampersand', name='ampersand.sc', src='ampersand', comment='& AMPERSAND Smallcap')

gids['largecircle'] = GD(g2='largecircle', g1='largecircle', l='copyright', l2r='copyright', uni=0x25ef, c='◯', name='largecircle', comment='circle for ® trade mark sign, registered', useSkewRotate=True, addItalicExtremePoints=True)

for name, gd in GLYPH_DATA_ITALIC.items():
    gd.italic = True

UNICODE2GLYPH = {} # Key is unicode, value is name (only for glyphs that have a unicode)

for gds in (GLYPH_DATA, GLYPH_DATA_ITALIC):

    for gName, gd in sorted(gds.items()):
        
        if gd.uni:
            #assert gd.uni not in UNICODE2GLYPH, ("Unicode %04x already defined for /%s" % (gd.uni, gName))
            UNICODE2GLYPH[gd.uni] = gd.name
        
    for gName, gd in sorted(gds.items()):
        gdBase = None
        if gd.base is not None: # Make the x-ref base reference.
            gdBase = gds[gd.base]
            gdBase.composites.add(gName)
        for accentName in gd.accents: # It's an accent, x-ref this glyph to accents
            if accentName in ACCENT_DATA:
                ad = ACCENT_DATA[accentName]
                ad['composites'].add(gName)
                accentAnchor = ad['anchor']
                if gdBase is not None:  
                    gdBase.anchors.add(CONNECTED_ANCHORS[accentAnchor])
                gdAccent = gds[accentName]
                gdAccent.anchors.add(accentAnchor)

# Collect all source glyph with their depending glyphs for margins
GLYPH2SPACING_CHILDREN = {}
GLYPH2SPACING_CHILDREN_ITALIC = {}
for glyphDataSet, glyphSpacingSet in (
        (GLYPH_DATA, GLYPH2SPACING_CHILDREN), 
        (GLYPH_DATA_ITALIC, GLYPH2SPACING_CHILDREN_ITALIC)):
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
UNI2GLYPH_DATA_ITALIC = {}
CHAR2GLYPH_DATA = {}
CHAR2GLYPH_DATA_ITALIC = {}
for glyphDataSet, uni2GlyphData, char2GlyphData in (
        (GLYPH_DATA, UNI2GLYPH_DATA, CHAR2GLYPH_DATA),
        (GLYPH_DATA_ITALIC, UNI2GLYPH_DATA_ITALIC, CHAR2GLYPH_DATA_ITALIC)):

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

GROUPS1_ITALIC = {}
GROUPS2_ITALIC = {}
GLYPH2GROUP1_ITALIC = {} # Key is glyph name, value is name of group 1
GLYPH2GROUP2_ITALIC = {}

GLYPH_NOT_IN_GROUPS1 = ['.notdef', '.null']
GLYPH_NOT_IN_GROUPS2 = ['.notdef', '.null']
for gName in GLYPH_DATA.keys():
    if '.tab' in gName or 'cmb' in gName: #'flourish' in gName or 
        GLYPH_NOT_IN_GROUPS1.append(gName)
        GLYPH_NOT_IN_GROUPS2.append(gName)
    elif '.cbr' in gName:
        GLYPH_NOT_IN_GROUPS1.append(gName)

GLYPH_NOT_IN_GROUPS1_ITALIC = ['.notdef', '.null']
GLYPH_NOT_IN_GROUPS2_ITALIC = ['.notdef', '.null']
for gName in GLYPH_DATA_ITALIC.keys():
    if '.tab' in gName or 'cmb' in gName: #'flourish' in gName or 
        GLYPH_NOT_IN_GROUPS1_ITALIC.append(gName)
        GLYPH_NOT_IN_GROUPS2_ITALIC.append(gName)
    elif '.cbr' in gName:
        GLYPH_NOT_IN_GROUPS1_ITALIC.append(gName)

for gds, groups1, groups2, g2g1, g2g2, not1, not2 in (
    (GLYPH_DATA, 
        GROUPS1, GROUPS2, 
        GLYPH2GROUP1, GLYPH2GROUP2,
        GLYPH_NOT_IN_GROUPS1, GLYPH_NOT_IN_GROUPS2),
    (GLYPH_DATA_ITALIC, 
        GROUPS1_ITALIC, GROUPS2_ITALIC, 
        GLYPH2GROUP1_ITALIC, GLYPH2GROUP2_ITALIC,
        GLYPH_NOT_IN_GROUPS1_ITALIC, GLYPH_NOT_IN_GROUPS2_ITALIC),
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
    if not isinstance(f, str):
        f = f.path
    if 'Italic' in f:
        return GLYPH_DATA_ITALIC
    return GLYPH_DATA

#print(GLYPH_DATA['A'])
#print(GLYPH_DATA['Agrave'])
#print(GLYPH_DATA['e'])
#print(GLYPH_DATA['gravecmb'])

GROUPS1 = {}
GROUPS1_ITALIC = {}
GROUPS2 = {}
GROUPS2_ITALIC = {}
GLYPH2GROUP1 = {}
GLYPH2GROUP1_ITALIC = {}
GLYPH2GROUP2 = {}
GLYPH2GROUP2_ITALIC = {}
GLYPH2GROUPNAME1 = {}
GLYPH2GROUPNAME1_ITALIC = {}
GLYPH2GROUPNAME2 = {}
GLYPH2GROUPNAME2_ITALIC = {}

for glyphDataSet, groups1, groups2, glyph2Group1, glyph2Group2, glyph2GroupName1, glyph2GroupName2,  in (
        (GLYPH_DATA, GROUPS1, GROUPS2, GLYPH2GROUP1, GLYPH2GROUP2, GLYPH2GROUPNAME1, GLYPH2GROUPNAME2),
        (GLYPH_DATA_ITALIC, GROUPS1_ITALIC, GROUPS2_ITALIC, 
            GLYPH2GROUP1_ITALIC, GLYPH2GROUP2_ITALIC, GLYPH2GROUPNAME1_ITALIC, GLYPH2GROUPNAME2_ITALIC)): 
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

#print(GROUPS1['a'])
#print(GROUPS2['a'])
#print(GROUPS1_ITALIC['a'])
#print(GROUPS1_ITALIC['o'])
#print(GROUPS2_ITALIC['o'])
