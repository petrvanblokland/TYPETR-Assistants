# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   TYPETR_full_set.py
#

from copy import deepcopy

from assistantLib.assistantParts.glyphsets.glyphData import GD 
from assistantLib.assistantParts.glyphsets.anchorData import AD
from assistantLib.assistantParts.glyphsets.glyphSet import GlyphSet

class TYPETR_GlyphSet(GlyphSet):
    """GlyphSet for the default TYPETR families

    >>> gs = TYPETR_GlyphSet()
    >>> gs
    <TYPETR_GlyphSet 2533 glyphs>
    >>> gs['A']
    <GlyphData A>
    >>> gs['B']
    <GlyphData B>
    """

    # The "c" attribtes are redundant, if the @uni or @hex atre defined, but they are offer easy searching in the source by char.

    GLYPH_DATA = {
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
        '.notdef': GD(w=500, name='.notdef', anchors=[]),
        '.null': GD(w=0, uni=0x0000, unicodes=(0, 13), name='.null', anchors=[]),
        'dottedCircle': GD(uni=9676, c='◌', name='dottedCircle', hex='25cc', anchors=[AD.TOP_, AD.BOTTOM_]),

        'A': GD(g2='A', g1='A', l2r='A', uni=0x0041, c='A', name='A', comment='A Uppercase Alphabet, Latin'),
        'AE': GD(g2='AE', g1='E', l='A', r='E', uni=0x00c6, c='Æ', name='AE', comment='Æ ligature ae, latin capital'),
        'AEacute': GD(g2='AE', g1='E', l='A', r='E', uni=0x01fc, c='Ǽ', name='AEacute', base='AE', accents=['acutecmb.uc'], comment='Ǽ LATIN CAPITAL LETTER AE WITH ACUTE'),
        'Aacute': GD(g2='A', g1='A', l='A', w='A', uni=0x00c1, c='Á', name='Aacute', base='A', accents=['acutecmb.uc'], comment='Á A WITH ACUTE, LATIN CAPITAL LETTER'),
        'Abreve': GD(g2='A', g1='A', l='A', w='A', uni=0x0102, c='Ă', name='Abreve', base='A', accents=['brevecmb.uc'], comment='Ă LATIN CAPITAL LETTER A WITH BREVE'),
        'Acircumflex': GD(g2='A', g1='A', l='A', w='A', uni=0x00c2, c='Â', name='Acircumflex', base='A', accents=['circumflexcmb.uc'], comment='Â A WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
        'Adieresis': GD(g2='A', g1='A', l='A', w='A', uni=0x00c4, c='Ä', name='Adieresis', base='A', accents=['dieresiscmb.uc'], comment='Ä A WITH DIAERESIS, LATIN CAPITAL LETTER'),
        'Agrave': GD(g2='A', g1='A', l='A', w='A', uni=0x00c0, c='À', name='Agrave', base='A', accents=['gravecmb.uc'], comment='À A WITH GRAVE, LATIN CAPITAL LETTER'),
        'Amacron': GD(g2='A', g1='A', l='A', w='A', uni=0x0100, c='Ā', name='Amacron', base='A', accents=['macroncmb.uc'], comment='Ā Latin, European'),
        'Aogonek': GD(g2='A', g1='A', l='A', w='A', uni=0x0104, c='Ą', name='Aogonek', base='A', accents=['ogonekcmb'], comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),
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
        'Aogonek.sc': GD(g2='A.sc', g1='A.sc', l='A.sc', w='A.sc', name='Aogonek.sc', base='A.sc', accents=['ogonekcmb'], comment='Ą LATIN CAPITAL LETTER A WITH OGONEK'),
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
        'Eng': GD(g2='H', g1='N', l='N', w='N', uni=0x014a, c='Ŋ', name='Eng', comment='Ŋ'),
        'Eogonek': GD(g2='H', g1='E', l='E', w='E', uni=0x0118, c='Ę', name='Eogonek', base='E', accents=['ogonekcmb'], comment='Ę'),
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
        'Eng.sc': GD(g2='H.sc', g1='N.sc', l='N.sc', w='N.sc', name='Eng.sc', comment='Ŋ'),
        'Eogonek.sc': GD(g2='H.sc', g1='E.sc', l='E.sc', w='E.sc', name='Eogonek.sc', base='E.sc', accents=['ogonekcmb'], comment='Ę'),
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
     
        'I': GD(g2='H', g1='H', l='H', r='H', uni=0x0049, c='I', name='I', comment='I'),
        'Iacute': GD(g2='H', g1='H', l='I', w='I', uni=0x00cd, c='Í', name='Iacute', base='I', accents=['acutecmb.uc'], comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
        'Ibreve': GD(g2='H', g1='H', l='I', w='I', uni=0x012c, c='Ĭ', name='Ibreve', base='I', accents=['brevecmb.uc'], comment='Ĭ'),
        'Icircumflex': GD(g2='H', g1='H', l='I', w='I', uni=0x00ce, c='Î', name='Icircumflex', base='I', accents=['circumflexcmb.uc'], comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
        'Idieresis': GD(g2='H', g1='H', l='I', w='I', uni=0x00cf, c='Ï', name='Idieresis', base='I', accents=['dieresiscmb.uc'], comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
        'Idotaccent': GD(g2='H', g1='H', l='I', w='I', uni=0x0130, c='İ', name='Idotaccent', base='I', accents=['dotaccentcmb.uc'], comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
        'Igrave': GD(g2='H', g1='H', l='I', w='I', uni=0x00cc, c='Ì', name='Igrave', base='I', accents=['gravecmb.uc'], comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
        'Imacron': GD(g2='H', g1='H', l='I', w='I', uni=0x012a, c='Ī', name='Imacron', base='I', accents=['macroncmb.uc'], comment='Ī'),
        'Iogonek': GD(g2='H', g1='H', l='I', w='I', uni=0x012e, c='Į', name='Iogonek', base='I', accents=['ogonekcmb'], comment='Į'),
        'Itilde': GD(g2='H', g1='H', l='I', w='I', uni=0x0128, c='Ĩ', name='Itilde', base='I', accents=['tildecmb.uc'], comment='Ĩ'),

        'I.sc': GD(g2='H.sc', g1='H.sc', l='H.sc', r='H.sc', name='I.sc', comment='I.sc'),
        'Iacute.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Iacute.sc', base='I.sc', accents=['acutecmb'], comment='Í I WITH ACUTE, LATIN CAPITAL LETTER'),
        'Ibreve.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Ibreve.sc', base='I.sc', accents=['brevecmb'], comment='Ĭ'),
        'Icircumflex.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Icircumflex.sc', base='I.sc', accents=['circumflexcmb'], comment='Î I WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
        'Idieresis.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Idieresis.sc', base='I.sc', accents=['dieresiscmb'], comment='Ï I WITH DIAERESIS, LATIN CAPITAL LETTER'),
        'Idotaccent.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Idotaccent.sc', base='I.sc', accents=['dotaccentcmb'], comment='İ I WITH DOT ABOVE, LATIN CAPITAL LETTER'),
        'Igrave.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Igrave.sc', base='I.sc', accents=['gravecmb'], comment='Ì I WITH GRAVE, LATIN CAPITAL LETTER'),
        'Imacron.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Imacron.sc', base='I.sc', accents=['macroncmb'], comment='Ī'),
        'Iogonek.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Iogonek.sc', base='I.sc', accents=['ogonekcmb'], comment='Į'),
        'Itilde.sc': GD(g2='H.sc', g1='H.sc', l='I.sc', w='I.sc', name='Itilde.sc', base='I.sc', accents=['tildecmb'], comment='Ĩ'),

        'J': GD(g2='J', g1='J', w='I', uni=74, c='J', name='J', hex='004a', comment='J'), # Manually take margins from /I
        'Jcircumflex': GD(g2='J', g1='J', l='J', w='J', uni=308, c='Ĵ', name='Jcircumflex', hex='0134', base='J', accents=['circumflexcmb.uc'], comment='Ĵ'),
        'IJ': GD(g2='H', g1='J', bl='I', br='J', uni=0x0132, c='Ĳ', name='IJ', hex='0132', base='I', accents=['J'], comment='IJ Dutch ligature'),
        'J.base': GD(g2='J.base', g1='U', r='J', name='J.base'),
        'Jcircumflex.base': GD(g2='J.base', g1='U', l='J.base', w='J.base', name='Jcircumflex.base', base='J.base', accents=['circumflexcmb.uc']),
        
        'J.sc': GD(g2='J.sc', g1='J.sc', w='I.sc', name='J.sc', comment='J', ), # Manually take margins from /I
        'Jcircumflex.sc': GD(g2='J.sc', g1='J.sc', l='J.sc', w='J.sc', name='Jcircumflex.sc', base='J.sc', accents=['circumflexcmb'], comment='Ĵ'),
        'IJ.sc': GD(g2='H.sc', g1='J.sc', bl='I.sc', br='J.sc', name='IJ.sc', base='I.sc', accents=['J.sc'], comment='IJ Dutch ligature'),
        'J.base.sc': GD(g2='J.base.sc', g1='U.sc', r='J.sc', name='J.base.sc'),
        'Jcircumflex.base.sc': GD(g2='J.base.sc', g1='U.sc', l='J.base.sc', w='J.base.sc', name='Jcircumflex.base.sc', base='J.base.sc', accents=['circumflexcmb']),
        
        'K': GD(g2='H', g1='K', l='H', r='A', uni=0x004b, c='K', name='K', comment='K'),
        'Kcommaaccent': GD(g2='H', g1='K', l='K', r='K', uni=0x0136, c='Ķ', name='Kcommaaccent', base='K', accents=['commabelowcmb'], comment='Ķ'),
        
        'K.sc': GD(g2='H.sc', g1='K.sc', l='H.sc', r='A.sc', name='K.sc', comment='K'),
        'Kcommaaccent.sc': GD(g2='H.sc', g1='K.sc', l='K.sc', r='K.sc', name='Kcommaaccent.sc', base='K.sc', accents=['commabelowcmb'], comment='Ķ'),
        
        'L': GD(g2='H', g1='L', l='H', r='E', uni=0x004c, c='L', name='L', comment='L'),
        'Lacute': GD(g2='H', g1='L', l='L', w='L', uni=0x0139, c='Ĺ', name='Lacute', base='L', accents=['acutecmb.uc'], comment='Ĺ'),
        'Lcaron': GD(g2='H', g1='Lcaron', l='L', w='L', uni=0x013d, c='Ľ', name='Lcaron', base='L', accents=['caroncmb.vert'], comment='Ľ'),
        'Lcommaaccent': GD(g2='H', g1='Lcommaaccent', l='L', w='L', uni=0x013b, c='Ļ', name='Lcommaaccent', base='L', accents=['commabelowcmb'], comment='Ļ'),
        'Ldot': GD(g2='H', g1='Ldot',l='L', uni=0x013f, c='Ŀ', name='Ldot', base='L', accents=['dotmiddlecmb'], comment='Ŀ'),
        'Lslash': GD(g2='Eth', g1='L', l='L', w='L', uni=0x0141, c='Ł', base='L', name='Lslash', comment='Ł'),
        
        'L.sc': GD(g2='H.sc', g1='L.sc', l='H.sc', r='E.sc', name='L.sc', comment='L'),
        'Lacute.sc': GD(g2='H.sc', g1='L.sc', l='L.sc', w='L.sc', name='Lacute.sc', base='L.sc', accents=['acutecmb'], comment='Ĺ'),
        'Lcaron.sc': GD(g2='H.sc', g1='Lcaron.sc', l='L.sc', w='L.sc', name='Lcaron.sc', base='L.sc', accents=['caroncmb.vert'], comment='Ľ'),
        'Lcommaaccent.sc': GD(g2='H.sc', g1='Lcommaaccent.sc', l='L.sc', w='L.sc', name='Lcommaaccent.sc', base='L.sc', accents=['commabelowcmb'], comment='Ļ'),
        'Ldot.sc': GD(g2='H.sc', g1='Ldot.sc',l='L.sc', name='Ldot.sc', base='L.sc', accents=['dotmiddlecmb'], comment='Ŀ'),
        'Lslash.sc': GD(g2='Eth.sc', g1='L.sc', l='L.sc', w='L.sc', base='L.sc', name='Lslash.sc', comment='Ł'),
        
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
        
        'O': GD(g2='O', g1='O', l2r='O', uni=0x004f, c='O', name='O', comment='O', useSkewRotate=True, addItalicExtremePoints=True),
        'OE': GD(g2='O', g1='E', l='O', r='E', uni=338, c='Œ', name='OE', hex='0152', comment='Œ'),
        'Oslash': GD(g2='O', g1='O', l='O', w='O', uni=0x00d8, c='Ø', base='O', name='Oslash', comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
        'Oslashacute': GD(g2='O', g1='O', l='O', w='O', uni=0x01fe, c='Ǿ', base='Oslash', accents=['acutecmb.uc'], name='Oslashacute', comment='Ǿ LATIN CAPITAL LETTER O WITH STROKE AND ACUTE'),
        'Oacute': GD(g2='O', g1='O', l='O', w='O', uni=0x00d3, c='Ó', name='Oacute', base='O', accents=['acutecmb.uc'], comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
        'Obreve': GD(g2='O', g1='O', l='O', w='O', uni=0x014e, c='Ŏ', name='Obreve', base='O', accents=['brevecmb.uc'], comment='Ŏ'),
        'Ocircumflex': GD(g2='O', g1='O', l='O', w='O', uni=0x00d4, c='Ô', name='Ocircumflex', base='O', accents=['circumflexcmb.uc'], comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
        'Odieresis': GD(g2='O', g1='O', l='O', w='O', uni=0x00d6, c='Ö', name='Odieresis', base='O', accents=['dieresiscmb.uc'], comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
        'Ograve': GD(g2='O', g1='O', l='O', w='O', uni=0x00d2, c='Ò', name='Ograve', base='O', accents=['gravecmb.uc'], comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
        'Ohungarumlaut': GD(g2='O', g1='O', l='O', w='O', uni=0x0150, c='Ő', name='Ohungarumlaut', base='O', accents=['hungarumlautcmb.uc'], comment='Ő'),
        'Omacron': GD(g2='O', g1='O', l='O', w='O', uni=0x014c, c='Ō', name='Omacron', base='O', accents=['macroncmb.uc'], comment='Ō'),
        'Otilde': GD(g2='O', g1='O', l='O', w='O', uni=0x00d5, c='Õ', name='Otilde', base='O', accents=['tildecmb.uc'], comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),

        'Omega': GD(g2='Omega', g1='Omega', l='T', l2r='Omega', uni=0x03a9, c='Ω', name='Omega', src=('O', 'summation'), comment='Ω (GREEK CAPITAL LETTER OMEGA)'),
        
        'O.sc': GD(g2='O.sc', g1='O.sc', l2r='O.sc', name='O.sc', comment='O', useSkewRotate=True, addItalicExtremePoints=True),
        'OE.sc': GD(g2='O.sc', g1='E.sc', l='O.sc', r='E.sc', name='OE.sc', comment='Œ'),
        'Oslash.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', base='O.sc', name='Oslash.sc', comment='Ø STROKE, LATIN CAPITAL LETTER O WITH'),
        'Oslashacute.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', base='Oslash.sc', accents=['acutecmb'], name='Oslashacute', comment='Ǿ LATIN CAPITAL LETTER O WITH STROKE AND ACUTE'),
        'Oacute.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Oacute.sc', base='O.sc', accents=['acutecmb'], comment='Ó O WITH ACUTE, LATIN CAPITAL LETTER'),
        'Obreve.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Obreve.sc', base='O.sc', accents=['brevecmb'], comment='Ŏ'),
        'Ocircumflex.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Ocircumflex.sc', base='O.sc', accents=['circumflexcmb'], comment='Ô O WITH CIRCUMFLEX, LATIN CAPITAL LETTER'),
        'Odieresis.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Odieresis.sc', base='O.sc', accents=['dieresiscmb'], comment='Ö O WITH DIAERESIS, LATIN CAPITAL LETTER'),
        'Ograve.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Ograve.sc', base='O.sc', accents=['gravecmb'], comment='Ò O WITH GRAVE, LATIN CAPITAL LETTER'),
        'Ohungarumlaut.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Ohungarumlaut.sc', base='O.sc', accents=['hungarumlautcmb'], comment='Ő'),
        'Omacron.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Omacron.sc', base='O.sc', accents=['macroncmb'], comment='Ō'),
        'Otilde.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Otilde.sc', base='O.sc', accents=['tildecmb'], comment='Õ O WITH TILDE, LATIN CAPITAL LETTER'),
        
        'P': GD(g2='H', g1='P', l='H', uni=0x0050, c='P', name='P', comment='P', useSkewRotate=True, addItalicExtremePoints=True),
        
        'P.sc': GD(g2='H.sc', g1='P.sc', l='H.sc', name='P.sc', comment='P.sc', useSkewRotate=True, addItalicExtremePoints=True),
        
        'Q': GD(g2='O', g1='O', l='O', w='O', uni=0x0051, c='Q', name='Q', base='O', comment='Q'), 
        
        'Q.sc': GD(g2='O.sc', g1='O.sc', l='O.sc', w='O.sc', name='Q.sc', base='O.sc', comment='Q.sc'), 

        'R': GD(g2='H', g1='R', l='H', uni=0x0052, c='R', name='R', comment='R', useSkewRotate=True, addItalicExtremePoints=True),
        'Racute': GD(g2='H', g1='R', l='R', w='R', uni=0x0154, c='Ŕ', name='Racute', base='R', accents=['acutecmb.uc'], comment='Ŕ'),
        'Rcaron': GD(g2='H', g1='R', l='R', w='R', uni=0x0158, c='Ř', name='Rcaron', base='R', accents=['caroncmb.uc'], comment='Ř'),
        'Rcommaaccent': GD(g2='H', g1='R', l='R', w='R', uni=0x0156, c='Ŗ', name='Rcommaaccent', base='R', accents=['commabelowcmb'], comment='Ŗ'),
        
        'R.sc': GD(g2='H.sc', g1='R.sc', l='H.sc', name='R.sc', comment='R.sc', useSkewRotate=True, addItalicExtremePoints=True),
        'Racute.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='Racute.sc', base='R.sc', accents=['acutecmb'], comment='Ŕ'),
        'Rcaron.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='Rcaron.sc', base='R.sc', accents=['caroncmb'], comment='Ř'),
        'Rcommaaccent.sc': GD(g2='H.sc', g1='R.sc', l='R.sc', w='R.sc', name='Rcommaaccent.sc', base='R.sc', accents=['commabelowcmb'], comment='Ŗ'),
        
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
        'Uogonek': GD(g2='U', g1='U', l='U', w='U', uni=0x0172, c='Ų', name='Uogonek', base='U', accents=['eogonekcmb'], comment='Ų'),
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
        'Uogonek.sc': GD(g2='U.sc', g1='U.sc', l='U.sc', w='U.sc', name='Uogonek.sc', base='U.sc', accents=['eogonekcmb'], comment='Ų'),
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
        'ae': GD(g2='a', g1='e', bl='a', br='e', uni=0x00e6, c='æ', name='ae', isLower=True, comment='æ small ligature ae, latin'),
        'aeacute': GD(g2='a', g1='o', l='ae', w='ae', uni=0x01fd, c='ǽ', name='aeacute', base='ae', isLower=True, accents=['acutecmb'], comment='ǽ'),
        'agrave': GD(g2='a', g1='a', l='a', w='a', uni=0x00e0, c='à', name='agrave', base='a', isLower=True, accents=['gravecmb'], comment='à A WITH GRAVE, LATIN SMALL LETTER'),
        'amacron': GD(g2='a', g1='a', l='a', w='a', uni=0x0101, c='ā', name='amacron', base='a', isLower=True, accents=['macroncmb'], comment='ā A WITH MACRON, LATIN SMALL LETTER'),
        'aring': GD(g2='a', g1='a', l='a', w='a', uni=0x00e5, c='å', name='aring', isLower=True, base='a', accents=['ringcmb'], comment='å RING ABOVE, LATIN SMALL LETTER A WITH'),
        'atilde': GD(g2='a', g1='a', l='a', w='a', uni=0x00e3, c='ã', name='atilde', isLower=True, base='a', accents=['tildecmb'], comment='ã A WITH TILDE, LATIN SMALL LETTER'),
        'aringacute': GD(g2='a', g1='a', l='aring', w='aring', uni=0x01fb, c='ǻ', isLower=True, name='aringacute', base='a', accents=['ringacutecmb'], comment='ǻ'),
        'aogonek': GD(g2='a', g1='a', l='a', w='a', uni=0x0105, c='ą', name='aogonek', isLower=True, base='a', accents=['ogonekcmb'], comment='ą Latin Small Letter a with Ogonek'),

        'acute': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='acutecmb', uni=0x00b4, c='´', name='acute', isLower=True, anchors=[], comment='´ spacing acute accent'),
        'approxequal': GD(g2='asciitilde', g1='asciitilde', l='equal', w=GD.CAT_MATH_WIDTH, uni=0x2248, c='≈', name='approxequal', src='equal', comment='≈ EQUAL TO, ALMOST', anchors=[]),
        'approxequal.uc': GD(g2='asciitilde', g1='asciitilde', l='equal', w=GD.CAT_MATH_WIDTH, name='approxequal.uc', base='approxequal', comment='≈ EQUAL TO, ALMOST, Uppercase', anchors=[]),
        'asciicircum': GD(uni=0x005e, l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, c='^', base='circumflexcmb', name='asciicircum', anchors=[], comment='^ spacing circumflex accent'),
        'asciitilde': GD(l2r='asciitilde', uni=0x007e, c='~', name='asciitilde', comment='~ tilde, spacing', anchors=[]),
        'asciitilde.uc': GD(g2='asciitilde', g1='asciitilde', l='asciitilde', r='asciitilde', name='asciitilde.uc', base='asciitilde', comment='~ tilde, spacing Uppercase', anchors=[]),
        'asterisk': GD(l2r='asterisk', uni=0x002a, c='*', name='asterisk', comment='* star'),
        'asterisk.uc': GD(g2='asterisk', g1='asterisk', l='asterisk', r='asterisk', name='asterisk.uc', comment='* star Uppercase'),
        'at': GD(g2='O', g1='O', l='O', r='O', uni=0x0040, c='@', name='at', comment='@ COMMERCIAL AT'),
        #'at.alt1': GD(g2='O', g1='O', l='O', r='O', name='at.alt1', src='at', comment='@ COMMERCIAL AT alternate as spiral'),

        'ampersand': GD(l='a', uni=0x0026, c='&', name='ampersand', comment='& AMPERSAND', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
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
        'breve': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02d8, c='˘', name='breve', base='brevecmb', comment='˘ Spacing Clones of Diacritics', anchors=[]),
        'bullet': GD(g2='bullet', g1='bullet', l2r='bullet', uni=0x2022, c='•', name='bullet', comment='• small circle, black', anchors=[]),
        'bullet.uc': GD(g2='bullet', g1='bullet', l='bullet', w='bullet', name='bullet.uc', comment='• small circle, black Uppercase', anchors=[]),
        
        'c': GD(g2='o', g1='c', l='o', uni=0x0063, c='c', name='c', isLower=True, comment='c'),
        'cacute': GD(g2='o', g1='c', l='c', w='c', uni=0x0107, c='ć', name='cacute', isLower=True, base='c', accents=['acutecmb'], comment='ć C WITH ACUTE, LATIN SMALL LETTER'),
        'ccaron': GD(g2='o', g1='c', l='c', w='c', uni=0x010d, c='č', name='ccaron', isLower=True, base='c', accents=['caroncmb'], comment='č C WITH CARON, LATIN SMALL LETTER'),
        'ccedilla': GD(g2='o', g1='c', l='c', w='c', uni=0x00e7, c='ç', name='ccedilla', isLower=True, base='c', accents=['cedillacmb'], comment='ç CEDILLA, LATIN SMALL LETTER C WITH'),
        'ccircumflex': GD(g2='o', g1='c', l='c', w='c', uni=0x0109, c='ĉ', name='ccircumflex', isLower=True, base='c', accents=['circumflexcmb'], comment='ĉ C WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'cdotaccent': GD(g2='o', g1='c', l='c', w='c', uni=0x010b, c='ċ', name='cdotaccent', isLower=True, base='c', accents=['dotaccentcmb']),

        'caron': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02c7, c='ˇ', name='caron', base='caroncmb', comment='ˇ tone, mandarin chinese third', anchors=[]),
        'cedilla': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x00b8, c='¸', name='cedilla', isLower=True, base='cedillacmb', comment='¸ spacing cedilla', anchors=[]),
        'cent': GD(g2='o', g1='c', l='c', r='c', uni=0x00a2, c='¢', base='c', name='cent', isLower=True, comment='¢ CENT SIGN'),
        'cent.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='cent.tab', base='cent', isLower=True, comment='¢ CENT SIGN TAB'),
        'circumflex': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02c6, c='ˆ', name='circumflex', base='circumflexcmb', comment='ˆ CIRCUMFLEX ACCENT, MODIFIER LETTER', anchors=[]),
        'colon': GD(g2='colon', g1='colon', l='period', r='period', uni=0x003a, c=':', name='colon', base='period', accents=['period'], comment='COLON', anchors=[]),
        'comma': GD(g2='comma', g1='comma', uni=0x002c, c=',', name='comma', anchors=[], comment=', separator, decimal'),
        'comma.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='comma.tab', base='comma', comment=', separator, decimal', anchors=[]),
        'copyright': GD(g2='copyright', g1='copyright', l='largecircle', r='largecircle', uni=0x00a9, c='©', name='copyright', base='largecircle', comment='© COPYRIGHT SIGN'),
        'currency': GD(l='O', r='O', uni=0x00a4, c='¤', name='currency', comment='¤ CURRENCY SIGN', anchors=[]),
        
        'd': GD(g2='o', g1='l', l='o', r='l', uni=0x0064, c='d', name='d', isLower=True, comment='d'),
        'dcaron': GD(g2='o', g1='dcaron', l='d', br='comma', rightMin=GD.CAT_MIN_RIGHT, uni=0x010f, c='ď', name='dcaron', isLower=True, base='d', accents=['caroncmb.vert'], comment='ď D WITH CARON, LATIN SMALL LETTER'),
        'dcroat': GD(g2='o', g1='l', l='d', w='d', uni=0x0111, c='đ', name='dcroat', base='d', comment='đ D WITH STROKE, LATIN SMALL LETTER'),
        
        'dagger': GD(l2r='dagger', uni=0x2020, c='†', name='dagger', src='asterisk', comment='† DAGGER'),
        'daggerdbl': GD(g2='daggerdbl', g1='daggerdbl', l='dagger', r='dagger', uni=0x2021, c='‡', name='daggerdbl', src='dagger', comment='‡ DOUBLE DAGGER'),
        'degree': GD(l2r='degree', uni=0x00b0, c='°', name='degree', isLower=True, src='ringcmb', comment='° DEGREE SIGN', useSkewRotate=True, addItalicExtremePoints=True, anchors=[]),
        'dieresis': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x00a8, c='¨', name='dieresis', base='dieresiscmb', comment='¨ spacing diaeresis', anchors=[]),
        'divide': GD(l='plus', w=GD.CAT_MATH_WIDTH, uni=0x00f7, c='÷', name='divide', comment='÷ obelus', anchors=[]),
        'divide.uc': GD(g2='divide', g1='divide', l='divide', w=GD.CAT_MATH_WIDTH, name='divide.uc', comment='÷ obelus Uppercase', anchors=[]),
        'dollar': GD(g2='S', g1='S', l='S', r='S', uni=0x0024, c='$', base='S', name='dollar', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='$ milreis'),
        'dollar.alt1': GD(g2='S', g1='S', l='S', r='S', base='S', name='dollar.alt1', src='dollar', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='$ milreis'),
        'dollar.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='dollar.tab', src='dollar', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='$ milreis TAB'),
        'dollar.alt1.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='dollar.alt1.tab', src='dollar.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='$ milreis TAB'),
        'dotaccent': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02d9, c='˙', name='dotaccent', base='dotaccentcmb', comment='˙ tone, mandarin chinese fifth or neutral', anchors=[]),
        
        'e': GD(g2='o', g1='e', l='o', r='o', uni=0x0065, c='e', name='e', isLower=True, comment='e'),
        'eacute': GD(g2='o', g1='e', l='e', w='e', uni=0x00e9, c='é', name='eacute', isLower=True, base='e', accents=['acutecmb'], comment='é E WITH ACUTE, LATIN SMALL LETTER'),
        'ebreve': GD(g2='o', g1='e', l='e', w='e', uni=0x0115, c='ĕ', name='ebreve', isLower=True, base='e', accents=['brevecmb'], comment='ĕ E WITH BREVE, LATIN SMALL LETTER'),
        'ecaron': GD(g2='o', g1='e', l='e', w='e', uni=0x011b, c='ě', name='ecaron', isLower=True, base='e', accents=['caroncmb'], comment='ě E WITH CARON, LATIN SMALL LETTER'),
        'ecircumflex': GD(g2='o', g1='e', l='e', w='e', uni=0x00ea, c='ê', name='ecircumflex', isLower=True, base='e', accents=['circumflexcmb'], comment='ê E WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'edieresis': GD(g2='o', g1='e', l='e', w='e', uni=0x00eb, c='ë', name='edieresis', isLower=True, base='e', accents=['dieresiscmb'], comment='ë E WITH DIAERESIS, LATIN SMALL LETTER'),
        'edotaccent': GD(g2='o', g1='e', l='e', w='e', uni=0x0117, c='ė', name='edotaccent', isLower=True, base='e', accents=['dotaccentcmb']),
        'egrave': GD(g2='o', g1='e', l='e', w='e', uni=0x00e8, c='è', name='egrave', isLower=True, base='e', accents=['gravecmb'], comment='è E WITH GRAVE, LATIN SMALL LETTER'),
        'emacron': GD(g2='o', g1='e', l='e', w='e', uni=0x0113, c='ē', name='emacron', isLower=True, base='e', accents=['macroncmb'], comment='ē E WITH MACRON, LATIN SMALL LETTER'),
        'eogonek': GD(g2='o', g1='eogonek', l='e', w='e', uni=0x0119, c='ę', name='eogonek', isLower=True, base='e', accents=['eogonekcmb'], comment='ę E WITH OGONEK, LATIN SMALL LETTER'),

        'ellipsis': GD(g2='period', g1='period', bl='period', br='period', uni=0x2026, c='…', name='ellipsis', base='period', accents=['period', 'period'], comment='… three dot leader', anchors=[]), # Not as components of period
        'eng': GD(g2='n', g1='j', l='n', r='jdotless', uni=0x014b, c='ŋ', name='eng', isLower=True, comment='ŋ LATIN SMALL LETTER ENG'),
        'equal': GD(g2='hyphen', g1='hyphen', w=GD.CAT_MATH_WIDTH, uni=0x003d, c='=', name='equal', comment='= EQUALS SIGN', anchors=[]),
        'equal.uc': GD(g2='hyphen', g1='hyphen', l='equal', w=GD.CAT_MATH_WIDTH, name='equal.uc', comment='= EQUALS SIGN Uppercase', anchors=[]),
        'eth': GD(g2='o', g1='O', l='o', uni=0x00f0, c='ð', name='eth', src='six', comment='ð LATIN SMALL LETTER ETH'),
        'exclam': GD(l2r='exclam', uni=0x0021, c='!', name='exclam', comment='! factorial', useSkewRotate=True, addItalicExtremePoints=True),
        'exclamdown': GD(l2r='exclam', r2l='exclam', uni=0x00a1, c='¡', src180='exclam', name='exclamdown', comment='¡ INVERTED EXCLAMATION MARK'),
        'exclamdown.uc': GD(g2='exclamdown.uc', g1='exclamdown.uc', l2r='exclam', r2l='exclam', name='exclamdown.uc', base='exclamdown', comment='¡ INVERTED EXCLAMATION MARK'),

        'emdash': GD(g2='hyphen', g1='hyphen', l=GD.CAT_CENTER, w=GD.CAT_EM, uni=0x2014, c='—', name='emdash', comment='— EM DASH', anchors=[]),
        'emdash.uc': GD(g2='hyphen', g1='hyphen', l='emdash', r='emdash', name='emdash.uc', base='emdash', comment='— EM DASH Uppercase', anchors=[]),
        'endash': GD(g2='hyphen', g1='hyphen', l=GD.CAT_CENTER, w=GD.CAT_EM2, uni=0x2013, c='–', name='endash', comment='– EN DASH', anchors=[]),
        'endash.uc': GD(g2='hyphen', g1='hyphen', l='endash', r='endash', name='endash.uc', base='endash', comment='– EN DASH Uppercase', anchors=[]),
        'underscore': GD(l=GD.CAT_CENTER, w=GD.CAT_EM2, uni=0x005f, c='_', name='underscore', comment='_ underscore, spacing', anchors=[]),
        
        'f': GD(g2='f', g1='f', rightMin=GD.CAT_MIN_RIGHT, fixAnchors=False, uni=0x0066, c='f', name='f', comment='f'),
        'fi': GD(g2='f', g1='i', l='f', br='i', uni=0xfb01, c='ﬁ', name='fi', base='f.ij', accents=['idotless'], comment='ﬁ f_i'),
        'fl': GD(g2='f', g1='l', l='f', br='l', uni=0xfb02, c='ﬂ', name='fl', base='f.short', accents=['l'], comment='ﬂ f_l'),
        'f.overshoot': GD(g2='f', g1='f', l='f', w='f', name='f.overshoot', src='f', comment='f overshoot looped thin flag over diacritics such as /iacute'),
        'f.short': GD(g2='f', l='f', w='f', name='f.short', comment='f with straight thin flag to connect with @f_ascenders'),
        'f.curly': GD(g2='f', l='f', w='f', name='f.curly', comment='f curly looped thin flag to connect with @f_curlyAscenders'),
        'f.small': GD(g2='f', l='f', w='f', name='f.small', comment='f with small flag to connect to figures'),
        'f.ij': GD(g2='f', l='f', w='f', name='f.ij', comment='f with extended flag for f-->i and f-->j'),

        'florin': GD(g2='florin', g1='florin', w='f', uni=0x0192, c='ƒ', name='florin', src='f', comment='ƒ script f, latin small letter'),
        'fraction': GD(g2='fraction', g1='fraction', l=-130, r=-130, name='fraction', uni=0x2044, c='⁄', comment='⁄ solidus', anchors=[]),

        'g': GD(g2='g', g1='g', uni=0x0067, c='g', name='g', isLower=True, comment='g'),
        'earlessg': GD(g2='g', g1='g', l='g', w='g', name='earlessg', isLower=True, src='g', comment='g with ear to accommodate accents'),
        'gbreve': GD(g2='g', g1='g', l='g', w='g', uni=0x011f, c='ğ', name='gbreve', isLower=True, base='earlessg', accents=['brevecmb'], comment='ğ G WITH BREVE, LATIN SMALL LETTER'),
        'gcaron': GD(g2='g', g1='g', l='g', w='g', uni=0x01e7, c='ǧ', name='gcaron', isLower=True, base='earlessg', accents=['caroncmb'], comment='ǧ G WITH CARON, LATIN SMALL LETTER'),
        'gcircumflex': GD(g2='g', g1='g', l='g', w='g', uni=0x011d, c='ĝ', name='gcircumflex', base='earlessg', accents=['circumflexcmb'], comment='ĝ G WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'gcommaaccent': GD(g2='g', g1='g', l='g', w='g', uni=0x0123, c='ģ', name='gcommaaccent', isLower=True, base='earlessg', accents=['commaturnedabovecmb']),
        'gdotaccent': GD(g2='g', g1='g', l='g', w='g', uni=0x0121, c='ġ', name='gdotaccent', base='earlessg', accents=['dotaccentcmb']),
        
        'germandbls': GD(g2='germandbls', g1='germandbls', l='f', r='o', uni=0x00df, c='ß', name='germandbls', isLower=True, comment='ß SHARP S, LATIN SMALL LETTER'),
        'Germandbls': GD(g2='germandbls', g1='germandbls', l='f', r='S', uni=0x1E9E, c='ẞ', name='Germandbls', src='germandbls', isLower=False, comment='ẞ Latin Capital Letter Sharp S'),
        'Germandbls.sc': GD(g2='germandbls', g1='germandbls', l='f', r='S.sc', name='Germandbls.sc', src='Germandbls', isLower=False, comment='ẞ Small caps Latin Capital Letter Sharp S'),
        
        'grave': GD(l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x0060, c='`', name='grave', base='gravecmb', anchors=[], comment='` spacing grave accent'),
        'greater': GD(g2='greater', g1='greater', w=GD.CAT_MATH_WIDTH, uni=0x003e, c='>', name='greater', comment='> GREATER-THAN SIGN', anchors=[]),
        'greater.uc': GD(g2='greater', g1='greater', l='greater', w=GD.CAT_MATH_WIDTH, name='greater.uc', comment='> GREATER-THAN SIGN Uppercase', anchors=[]),
        'greaterequal': GD(g2='greater', g1='greater', l='greater', w=GD.CAT_MATH_WIDTH, uni=0x2265, c='≥', name='greaterequal', comment='≥ GREATER-THAN OR EQUAL TO', anchors=[]),
        'greaterequal.uc': GD(g2='greaterequal', g1='greaterequal', l='greater', w=GD.CAT_MATH_WIDTH, name='greaterequal.uc', comment='≥ GREATER-THAN OR EQUAL TO Uppercase', anchors=[]),
        'guilsinglleft': GD(g2='guilsinglleft', g1='guilsinglleft', l=40, r=40, uni=0x2039, c='‹', name='guilsinglleft', comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK', anchors=[]),
        'guilsinglleft.uc': GD(g2='guilsinglleft', g1='guilsinglleft', l2r='guilsinglleft', name='guilsinglleft.uc', base='guilsinglleft', comment='‹ SINGLE LEFT-POINTING ANGLE QUOTATION MARK', anchors=[]),
        'guilsinglright': GD(g2='guilsinglright', g1='guilsinglright', l='guilsinglleft', r='guilsinglleft', uni=0x203a, c='›', name='guilsinglright', comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK', anchors=[]),
        'guilsinglright.uc': GD(g2='guilsinglright', g1='guilsinglright', l='guilsinglleft', r='guilsinglleft', base='guilsinglright', name='guilsinglright.uc', comment='› SINGLE RIGHT-POINTING ANGLE QUOTATION MARK', anchors=[]),
        'guillemotleft': GD(g2='guilsinglleft', g1='guilsinglleft', bl='guilsinglleft', br='guilsinglleft', uni=0x00AB, c='«', name='guillemotleft', base='guilsinglleft', accents=['guilsinglleft'], anchors=[]),
        'guillemotleft.uc': GD(g2='guilsinglleft', g1='guilsinglleft', bl='guilsinglleft', br='guilsinglleft', name='guillemotleft.uc', base='guilsinglleft', accents=['guilsinglleft'], anchors=[]),
        'guillemotright': GD(g2='guilsinglright', g1='guilsinglright', bl='guilsinglleft', br='guilsinglleft', uni=0x00BB, name='guillemotright', c='»', base='guilsinglright', accents=['guilsinglright'], anchors=[]),
        'guillemotright.uc': GD(g2='guilsinglright', g1='guilsinglright', bl='guilsinglleft', br='guilsinglleft', name='guillemotright.uc', base='guilsinglright', accents=['guilsinglright'], anchors=[]),

        'h': GD(g2='h', g1='n', r='n', uni=0x0068, c='h', name='h', isLower=True, comment='h'), # Source for left spacing in Roman
        'hbar': GD(g2='h', g1='n', l='h', w='h', uni=0x0127, c='ħ', name='hbar', base='h', isLower=True, comment='ħ H WITH STROKE, LATIN SMALL LETTER'),
        'hcircumflex': GD(g2='h', g1='n', l='h', w='h', uni=0x0125, c='ĥ', name='hcircumflex', isLower=True, base='h', accents=['circumflexcmb.uc'], comment='ĥ H WITH CIRCUMFLEX, LATIN SMALL LETTER'),

        'horizontalbar': GD(g2='hyphen', g1='hyphen', l='emdash', r='emdash', uni=0x2015, c='―', name='horizontalbar', base='emdash', anchors=[]),
        'horizontalbar.uc': GD(g2='hyphen', g1='hyphen', l='horizontalbar', r='horizontalbar', name='horizontalbar.uc', comment='Horizontal base Uppercase', anchors=[]),
        'hungarumlaut': GD(g2='hungarumlaut', g1='hungarumlaut', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02dd, c='˝', name='hungarumlaut', base='hungarumlautcmb', comment='˝ DOUBLE ACUTE ACCENT', anchors=[]),
        'hyphen': GD(g2='hyphen', g1='hyphen', l2r='hyphen', uni=0x002d, unicodes=(0x002d, 8208), c='-', name='hyphen', comment='- minus sign, hyphen', anchors=[]),
        'hyphen.uc': GD(g2='hyphen', g1='hyphen', l='hyphen', r='hyphen', name='hyphen.uc', base='hyphen', comment='- minus sign, hyphen', anchors=[]),
        'nbhyphen': GD(g2='hyphen', g1='hyphen', l2r='hyphen', uni=0x2011, c='‑', name='nbhyphen', base='hyphen', comment='‑ minus sign, non breaking hyphen', anchors=[]),
        'nbhyphen.uc': GD(g2='hyphen', g1='hyphen', l2r='hyphen', name='nbhyphen.uc', base='nbhyphen', comment='‑ minus sign, non breaking hyphen for capitals', anchors=[]),
        'softhyphen': GD(uni=0x00ad, name='softhyphen', comment='SOFT HYPHEN, Required by Type Network set.', anchors=[]),

        'idotless': GD(g2='i', g1='i', uni=0x0131, c='ı', src='i', isLower=True, name='idotless'),
        'i': GD(g2='i', g1='i', l='idotless', w='idotless', r='idotless', uni=0x0069, c='i', name='i', isLower=True, comment='i'),
        'i.trk': GD(g2='i', g1='i', l='n', r='n', name='i.trk', isLower=True, comment='i.trk', base='idotless', accents=['dotaccentcmb']),
        'iacute': GD(g2='i', g1='i', l='i', w='i', uni=0x00ed, c='í', isLower=True, name='iacute', base='idotless', accents=['acutecmb'], comment='í I WITH ACUTE, LATIN SMALL LETTER'),
        'ibreve': GD(g2='i', g1='i', l='i', w='i', uni=0x012d, c='ĭ', isLower=True, name='ibreve', base='idotless', accents=['brevecmb'], comment='ĭ I WITH BREVE, LATIN SMALL LETTER'),
        'icircumflex': GD(g2='i', g1='i', l='i', w='i', uni=0x00ee, c='î', isLower=True, name='icircumflex', base='idotless', accents=['circumflexcmb'], comment='î I WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'idieresis': GD(g2='i', g1='i', l='i', w='i', uni=0x00ef, c='ï', isLower=True, name='idieresis', base='idotless', accents=['dieresiscmb'], comment='ï I WITH DIAERESIS, LATIN SMALL LETTER'),
        'igrave': GD(g2='i', g1='i', l='i', w='i', uni=0x00ec, c='ì', name='igrave', isLower=True, base='idotless', accents=['gravecmb'], comment='ì I WITH GRAVE, LATIN SMALL LETTER'),
        'imacron': GD(g2='i', g1='i', l='i', w='i', uni=0x012b, c='ī', name='imacron', isLower=True, base='idotless', accents=['macroncmb'], comment='ī I WITH MACRON, LATIN SMALL LETTER'),
        'iogonek': GD(g2='i', g1='i', l='i', w='i', uni=0x012f, c='į', name='iogonek', isLower=True, base='i', accents=['ogonekcmb'], comment='į I WITH OGONEK, LATIN SMALL LETTER'),
        'itilde': GD(g2='i', g1='i', l='i', w='i', uni=0x0129, c='ĩ', name='itilde', isLower=True, base='idotless', accents=['tildecmb'], comment='ĩ I WITH TILDE, LATIN SMALL LETTER'),
        'ij': GD(g2='i', g1='j', l='i', br='j', uni=0x0133, c='ĳ', name='ij', isLower=True, base='i', accents=['j'], comment='Dutch ij'),

        'infinity': GD(bl='o', br='o', uni=0x221e, c='∞', name='infinity', comment='∞ INFINITY'),
        'integral': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, uni=0x222b, c='∫', name='integral', src='f', anchors=[], comment='∫ Integral Signs'),
        
        'jdotless': GD(g2='j', g1='j', uni=0x0237, c='ȷ', src='j', name='jdotless'),
        'j': GD(g2='j', g1='j', uni=0x006a, c='j', l='jdotless', w='jdotless', name='j', isLower=True, comment='j'),
        'jcircumflex': GD(g2='j', g1='j', l='j', w='j', uni=0x0135, c='ĵ', name='jcircumflex', isLower=True, base='jdotless', accents=['circumflexcmb'], comment='ĵ J WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        
        'k': GD(g2='h', g1='k', l='h', uni=0x006b, c='k', name='k', isLower=True, comment='k'),
        'kcommaaccent': GD(g2='h', g1='k', uni=0x0137, c='ķ', name='kcommaaccent', isLower=True, base='k', accents=['commabelowcmb']),
        #'kgreen': GD(g2='i', g1='k', l='i', r='k', uni=0x0138, c='ĸ', src='k', name='kgreen', isLower=True, comment='ĸ'),
        
        'l': GD(g2='h', g1='l', l='h', r='n', uni=0x006c, c='l', name='l', isLower=True, comment='l'),
        'lacute': GD(g2='h', g1='lacute', bl='l', w='l', uni=0x013a, c='ĺ', name='lacute', isLower=True, base='l', accents=['acutecmb.uc'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER'),
        'lcaron': GD(g2='h', g1='dcaron', bl='l', br='comma', uni=0x013e, c='ľ', name='lcaron', base='l', isLower=True, accents=['caroncmb.vert'], comment='ľ L WITH CARON, LATIN SMALL LETTER'),
        'lcommaaccent': GD(g2='h', g1='l', bl='l', w='l', uni=0x013c, c='ļ', name='lcommaaccent',isLower=True, base='l', accents=['commabelowcmb']),
        'ldot': GD(g2='h', g1='ldot', bl='l', uni=0x0140, c='ŀ', name='ldot', isLower=True, base='l', accents=['dotmiddlecmb'], comment='ŀ MIDDLE DOT, LATIN SMALL LETTER L WITH'),
        'lslash': GD(g2='lslash', g1='lslash', l='l', w='l', uni=0x0142, c='ł', name='lslash', isLower=True, base='l', comment='ł L WITH STROKE, LATIN SMALL LETTER'),

        'less': GD(g2='less', g1='less', w=GD.CAT_MATH_WIDTH, uni=60, c='<', name='less', comment='< LESS-THAN SIGN', anchors=[]),
        'less.uc': GD(g2='less', g1='less', l='less', w=GD.CAT_MATH_WIDTH, name='less.uc', comment='< LESS-THAN SIGN Uppercase', anchors=[]),
        'lessequal': GD(g2='less', g1='less', l='less', w=GD.CAT_MATH_WIDTH, uni=0x2264, c='≤', name='lessequal', comment='≤ LESS-THAN OR EQUAL TO', anchors=[]),
        'lessequal.uc': GD(g2='lessequal', g1='lessequal', l='less', w=GD.CAT_MATH_WIDTH, name='lessequal.uc', comment='≤ LESS-THAN OR EQUAL TO Uppercase', anchors=[]),
        'logicalnot': GD(g2='logicalnot', g1='logicalnot', l='equal', w=GD.CAT_MATH_WIDTH, uni=0x00ac, c='¬', name='logicalnot', comment='¬ NOT SIGN', anchors=[]),
        'logicalnot.uc': GD(g2='logicalnot', g1='logicalnot', l='equal', w=GD.CAT_MATH_WIDTH,  name='logicalnot.uc', comment='¬ NOT SIGN Uppercase', anchors=[]),
        'lozenge': GD(l2r='lozenge', uni=0x25ca, c='◊', name='lozenge', comment='◊ LOZENGE', anchors=[]),

        'm': GD(g2='n', g1='n', l='n', r='n', uni=0x006d, c='m', name='m', isLower=True, comment='m'),
        
        'macron': GD(g2='macron', g1='macron', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x00af, c='¯', name='macron', base='macroncmb', comment='¯ spacing macron', anchors=[]),
        'minus': GD(g2='hyphen', g1='hyphen', l='equal', w=GD.CAT_MATH_WIDTH, uni=0x2212, c='−', name='minus', comment='− MINUS SIGN', anchors=[]),
        'minus.uc': GD(g2='hyphen', g1='hyphen', l='equal', w=GD.CAT_MATH_WIDTH, name='minus.uc', comment='− MINUS SIGN Uppercase', anchors=[]),
        'minute': GD(g2='quotesingle', g1='quotesingle', bl='quotesingle', br='quotesingle', uni=0x2032, c='′', base='quotesingle', name='minute', comment='′ PRIME', anchors=[]),
        'mu': GD(g2='mu', g1='mu', l='u', r='u', uni=0x03bc, c='μ', name='mu', hex='03bc', isLower=True, comment='mu', base='u', anchors=[]),
        'microsign': GD(g2='microsign', g1='microsign', l='u', r='u', uni=0x00b5, c='µ', name='microsign', hex='00b5', isLower=True, comment='mu', base='mu', anchors=[]),
        'multiply': GD(l=GD.CAT_CENTER, w=GD.CAT_MATH_WIDTH, uni=0x00d7, c='×', name='multiply', src='plus', comment='× product, cartesian', anchors=[]),
        'multiply.uc': GD(g2='multiply', g1='multiply', l='multiply', w=GD.CAT_MATH_WIDTH, name='multiply.uc', comment='Multiply Uppercase', anchors=[]),
        
        'n': GD(g2='n', g1='n', uni=0x006e, c='n', name='n', isLower=True, comment='n'),
        'nacute': GD(g2='n', g1='n', l='n', w='n', uni=0x0144, c='ń', name='nacute', isLower=True, base='n', accents=['acutecmb'], comment='ń N WITH ACUTE, LATIN SMALL LETTER'),
        'ncaron': GD(g2='n', g1='n', l='n', w='n', uni=0x0148, c='ň', name='ncaron', isLower=True, base='n', accents=['caroncmb'], comment='ň N WITH CARON, LATIN SMALL LETTER'),
        'ncommaaccent': GD(g2='n', g1='n', l='n', w='n', uni=0x0146, c='ņ', name='ncommaaccent', isLower=True, base='n', accents=['commabelowcmb']),
        'ntilde': GD(g2='n', g1='n', l='n', w='n', uni=0x00f1, c='ñ', name='ntilde', isLower=True, base='n', accents=['tildecmb'], comment='ñ N WITH TILDE, LATIN SMALL LETTER'),
        
        'notequal': GD(g2='hyphen', g1='hyphen', l='equal', w=GD.CAT_MATH_WIDTH, uni=0x2260, c='≠', name='notequal', base='equal', comment='≠ NOT EQUAL TO', anchors=[]),
        'notequal.uc': GD(g2='equal', g1='equal', l='equal', w=GD.CAT_MATH_WIDTH, name='notequal.uc', comment='≠ NOT EQUAL TO Uppercase', anchors=[]),
        'numbersign': GD(g2='numbersign', g1='numbersign', l2r='numbersign', uni=0x0023, c='#', name='numbersign', comment='# pound sign'),
        'numbersign.uc': GD(g2='numbersign', g1='numbersign', l='numbersign', w='numbersign', name='numbersign.uc', comment='# pound sign Uppercase'),
        
        'o': GD(g2='o', g1='o', l2r='o', uni=0x006f, c='o', name='o', isLower=True, comment='o'),
        'oacute': GD(g2='o', g1='o', l='o', w='o', uni=0x00f3, c='ó', name='oacute', isLower=True, base='o', accents=['acutecmb'], comment='ó O WITH ACUTE, LATIN SMALL LETTER'),
        'obreve': GD(g2='o', g1='o', l='o', w='o', uni=0x014f, c='ŏ', name='obreve', isLower=True, base='o', accents=['brevecmb'], comment='ŏ O WITH BREVE, LATIN SMALL LETTER'),
        'ocircumflex': GD(g2='o', g1='o', l='o', w='o', uni=0x00f4, c='ô', name='ocircumflex', isLower=True, base='o', accents=['circumflexcmb'], comment='ô O WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'odieresis': GD(g2='o', g1='o', l='o', w='o', uni=0x00f6, c='ö', name='odieresis', isLower=True, base='o', accents=['dieresiscmb'], comment='ö O WITH DIAERESIS, LATIN SMALL LETTER'),
        'oe': GD(g2='o', g1='e', bl='o', br='e', uni=0x0153, c='œ', name='oe', base='o', accents=['e'], comment='œ SMALL LIGATURE OE, LATIN'),
        'ograve': GD(g2='o', g1='o', l='o', w='o', uni=0x00f2, c='ò', name='ograve', isLower=True, base='o', accents=['gravecmb'], comment='ò O WITH GRAVE, LATIN SMALL LETTER'),
        'ohungarumlaut': GD(g2='o', g1='o', l='o', w='o', uni=0x0151, c='ő', name='ohungarumlaut', isLower=True, base='o', accents=['hungarumlautcmb']),
        'omacron': GD(g2='o', g1='o', l='o', w='o', uni=0x014d, c='ō', name='omacron', isLower=True, base='o', accents=['macroncmb'], comment='ō O WITH MACRON, LATIN SMALL LETTER'),
        'oslash': GD(g2='o', g1='o',l='o', w='o', uni=0x00f8, c='ø', name='oslash', isLower=True, base='o', comment='ø STROKE, LATIN SMALL LETTER O WITH'),
        'oslashacute': GD(g2='o', g1='o',l='o', w='o', uni=0x01ff, c='ǿ', name='oslashacute', isLower=True, base='oslash', accents=['acutecmb'], comment='ǿ'),
        'otilde': GD(g2='o', g1='o',l='o', w='o', uni=0x00f5, c='õ', name='otilde', isLower=True, base='o', accents=['tildecmb'], comment='õ O WITH TILDE, LATIN SMALL LETTER'),

        'ogonek': GD(g2='ogonek', g1='ogonek', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02db, c='˛', name='ogonek',isLower=True,  base='ogonekcmb', comment='˛ OGONEK', anchors=[]),
        'ordfeminine': GD(g1='ordfeminine', g2='ordfeminine', l='ordmasculine', r='ordmasculine', uni=0x00aa, c='ª', name='ordfeminine', comment='ª ORDINAL INDICATOR, FEMININE'),
        'ordmasculine': GD(g1='ordfeminine', g2='ordfeminine', l2r='ordmasculine', uni=0x00ba, c='º', name='ordmasculine', comment='º ORDINAL INDICATOR, MASCULINE', useSkewRotate=True, addItalicExtremePoints=True),
        
        'p': GD(g2='p', g1='o',l='n', r='o', uni=0x0070, c='p', name='p', isLower=True, comment='p'),
        
        'paragraph': GD(g2='T', g1='bar', l='O', r='N', uni=0x00b6, c='¶', name='paragraph', comment='¶ section sign, european'),
        'parenleft': GD(l='O', r='H', uni=0x0028, c='(', name='parenleft', comment='( parenthesis, opening'),
        'parenright': GD(l2r='parenleft', r2l='parenleft', uni=0x0029, c=')', name='parenright', comment=') RIGHT PARENTHESIS'),
        'partialdiff': GD(l='o', r='o', uni=0x2202, c='∂', src='six', name='partialdiff', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='∂ PARTIAL DIFFERENTIAL'),
        'period': GD(g2='period', g1='period', l2r='period', uni=0x002e, c='.', name='period', anchors=[], comment='. point, decimal'),
        'period.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='period.tab', base='period', comment='. point, decimal', anchors=[]),
        'periodcentered': GD(l='period', w='period', uni=0x00b7, c='·', name='periodcentered', base='period', anchors=[]),
        'periodcentered.uc': GD(g2='periodcentered', g1='periodcentered', l='period', w='period', name='periodcentered.uc', anchors=[]),
        'pi': GD(l2r='pi', uni=0x03c0, c='π', name='pi', isLower=True, src='t', anchors=[]),
        'plus': GD(l='equal', w=GD.CAT_MATH_WIDTH, uni=0x002b, c='+', name='plus', comment='+ PLUS SIGN', anchors=[]),
        'plus.uc': GD(g2='equal', g1='plus', l='plus', w=GD.CAT_MATH_WIDTH, name='plus.uc', comment='+ PLUS SIGN Uppercase', anchors=[]),
        'plusminus': GD(l='equal', w=GD.CAT_MATH_WIDTH, uni=0x00b1, c='±', name='plusminus', comment='± PLUS-MINUS SIGN', anchors=[]),
        'plusminus.uc': GD(g2='plusminus', g1='plusminus',l='equal', w=GD.CAT_MATH_WIDTH, name='plusminus.uc', comment='± PLUS-MINUS SIGN Uppercase', anchors=[]),
        'product': GD(l='H', r='H', uni=0x220f, c='∏', src='H', name='product', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='∏ PRODUCT, N-ARY'),
        
        'q': GD(g2='o', g1='q', l='o', uni=0x0071, c='q', name='q', isLower=True, comment='q'),
        'question': GD(l2r='question', uni=0x003f, c='?', name='question', comment='? QUESTION MARK', useSkewRotate=True, addItalicExtremePoints=True),
        'questiondown': GD(l2r='question', r2l='question', uni=0x00bf, c='¿', src180='question', name='questiondown', comment='¿ turned question mark'),
        'questiondown.uc': GD(g2='questiondown.uc', g1='questiondown.uc', l2r='question', r2l='question', name='questiondown.uc', base='questiondown', comment='¿ turned question mark'),
        
        'quoteleft': GD(g2='quoteleft', g1='quoteleft', l2r='comma', r2l='comma', uni=0x2018, c='‘', name='quoteleft', src='comma', comment='‘ turned comma quotation mark, single', anchors=[]),
        'quoteright': GD(g2='quoteright', g1='quoteright', l='comma', r='comma', uni=0x2019, c='’', name='quoteright', base='comma', comment='’ SINGLE QUOTATION MARK, RIGHT', anchors=[]),
        'quotesinglbase': GD(g2='comma', g1='comma', l='comma', r='comma', uni=0x201a, c='‚', name='quotesinglbase', base='comma', comment='‚ SINGLE LOW-9 QUOTATION MARK', anchors=[]),
        'quotesingle': GD(g2='quotesingle', g1='quotesingle', l2r='quotesingle', uni=0x0027, c="'", name='quotesingle', src='exclam', comment="' single quotation mark, neutral", anchors=[]),
        'quotedblleft': GD(g2='quoteleft', g1='quoteleft', bl='comma', br='comma', uni=0x201c, c='“', name='quotedblleft', base='quoteleft', accents=['quoteleft'], comment='“ turned comma quotation mark, double', anchors=[]),
        'quotedblright': GD(g2='quoteright', g1='quoteright', bl='comma', br='comma', uni=0x201d, c='”', name='quotedblright', base='quoteright', accents=['quoteright'], comment='” RIGHT DOUBLE QUOTATION MARK', anchors=[]),
        'quotedblbase': GD(g2='comma', g1='comma', bl='comma', br='comma', uni=0x201e, c='„', name='quotedblbase', base='comma', accents=['comma'], comment='„ quotation mark, low double comma', anchors=[]),
        'quotedbl': GD(g2='quotesingle', g1='quotesingle', bl='quotesingle', br='quotesingle', uni=0x0022, c='"', name='quotedbl', base='quotesingle', accents=['quotesingle'], comment='" quotation mark, neutral', anchors=[]),
        
        'r': GD(g2='n', g1='r', l='n', uni=0x0072, c='r', name='r', isLower=True, comment='r'),
        'racute': GD(g2='n', g1='r', l='r', w='r', uni=0x0155, c='ŕ', name='racute', isLower=True, base='r', accents=['acutecmb'], comment='ŕ R WITH ACUTE, LATIN SMALL LETTER'),
        'rcaron': GD(g2='n', g1='r', l='r', w='r', uni=0x0159, c='ř', name='rcaron', isLower=True, base='r', accents=['caroncmb'], comment='ř R WITH CARON, LATIN SMALL LETTER'),
        'rcommaaccent': GD(g2='n', g1='r', l='r', w='r', uni=0x0157, c='ŗ', name='rcommaaccent', isLower=True, base='r', accents=['commabelowcmb'], comment='ŗ R WITH CEDILLA, LATIN SMALL LETTER'),
        
        'registered': GD(g2='copyright', g1='copyright', l='copyright', r='copyright', uni=0x00ae, c='®', name='registered', base='largecircle', comment='® trade mark sign, registered'),
        'largecircle': GD(g2='largecircle', g1='largecircle', l=40, l2r='largecircle', uni=0x25ef, c='◯', name='largecircle', comment='circle for ® trade mark sign, registered', useSkewRotate=True, addItalicExtremePoints=True),
        'ring': GD(g2='ring', g1='ring', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02da, c='˚', name='ring', base='ringcmb', comment='˚ RING ABOVE', anchors=[]),
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
        'space': GD(g1='space', g2='space', w=GD.CAT_WORD_SPACE, uni=0x0020, c=' ', name='space', comment='  Symbols, ASCII Punctuation and', anchors=[]),
        'sterling': GD(l2r='sterling', uni=0x00a3, c='£', name='sterling', comment='£ sterling, pound', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
        'sterling.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='sterling.tab', src='sterling', comment='£ sterling, pound TAB', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
        'summation': GD(l='H', r='E', uni=0x2211, c='∑', name='summation', src='E', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='∑ SUMMATION, N-ARY'),
        
        't': GD(g2='t', g1='t', uni=0x0074, c='t', name='t', comment='t', isLower=True),
        'tbar': GD(g2='t', g1='t', l='t', w='t', uni=0x0167, c='ŧ', name='tbar', isLower=True, base='t', comment='ŧ T WITH STROKE, LATIN SMALL LETTER'),
        'tcaron': GD(g2='t', g1='tcaron', l='t', w='t', uni=0x0165, c='ť', name='tcaron', isLower=True, base='t', accents=['caroncmb.vert'], comment='ť T WITH CARON, LATIN SMALL LETTER'),
        'tcedilla': GD(g2='t', g1='t', l='t', w='t', uni=0x0163, c='ţ', name='tcedilla', isLower=True, base='t', accents=['cedillacmb'], comment='ţ T WITH CEDILLA, LATIN SMALL LETTER'),
        'tcommaaccent': GD(g2='t', g1='t', l='t', w='t', uni=0x021b, c='ț', name='tcommaaccent', isLower=True, base='t', accents=['commabelowcmb'], comment='ț T WITH COMMA BELOW, LATIN SMALL LETTER'),
        
        'thorn': GD(g2='b', g1='o', l='b', r='p', uni=0x00fe, c='þ', name='thorn', isLower=True, src='p', comment='þ THORN, LATIN SMALL LETTER'),
        'tilde': GD(g2='tilde', g1='tilde', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, uni=0x02dc, c='˜', base='tildecmb', name='tilde', anchors=[]),
        'trademark': GD(g2='trademark', g1='trademark', l='T.sc', r='M.sc', uni=0x2122, c='™', name='trademark', comment='™ TRADE MARK SIGN'),
        
        'u': GD(g2='u', g1='u', r2l='n', l2r='u', uni=0x0075, c='u', name='u', isLower=True, comment='u'),
        'uacute': GD(g2='u', g1='u', l='u', w='u', uni=0x00fa, c='ú', name='uacute', isLower=True, base='u', accents=['acutecmb'], comment='ú U WITH ACUTE, LATIN SMALL LETTER'),
        'ubreve': GD(g2='u', g1='u', l='u', w='u', uni=0x016d, c='ŭ', name='ubreve', isLower=True, base='u', accents=['brevecmb'], comment='ŭ U WITH BREVE, LATIN SMALL LETTER'),
        'ucircumflex': GD(g2='u', g1='u', l='u', w='u', uni=0x00fb, c='û', name='ucircumflex', isLower=True, base='u', accents=['circumflexcmb'], comment='û U WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'udieresis': GD(g2='u', g1='u', l='u', w='u', uni=0x00fc, c='ü', name='udieresis', isLower=True, base='u', accents=['dieresiscmb'], comment='ü U WITH DIAERESIS, LATIN SMALL LETTER'),
        'ugrave': GD(g2='u', g1='u', l='u', w='u', uni=0x00f9, c='ù', name='ugrave', isLower=True, base='u', accents=['gravecmb'], comment='ù U WITH GRAVE, LATIN SMALL LETTER'),
        'uhungarumlaut': GD(g2='u', g1='u', l='u', w='u', uni=0x0171, c='ű', name='uhungarumlaut', isLower=True, base='u', accents=['hungarumlautcmb'], comment='ű U WITH DOUBLE ACUTE, LATIN SMALL LETTER'),
        'umacron': GD(g2='u', g1='u', l='u', w='u', uni=0x016b, c='ū', name='umacron', isLower=True, base='u', accents=['macroncmb'], comment='ū U WITH MACRON, LATIN SMALL LETTER'),
        'uogonek': GD(g2='u', g1='u', l='u', w='u', uni=0x0173, c='ų', name='uogonek', isLower=True, base='u', accents=['ogonekcmb'], comment='ų U WITH OGONEK, LATIN SMALL LETTER'),
        'uring': GD(g2='u', g1='u', l='u', w='u', uni=0x016f, c='ů', name='uring', isLower=True, base='u', accents=['ringcmb'], comment='ů U WITH RING ABOVE, LATIN SMALL LETTER'),
        'utilde': GD(g2='u', g1='u', l='u', w='u', uni=0x0169, c='ũ', name='utilde', isLower=True, base='u', accents=['tildecmb'], comment='ũ U WITH TILDE, LATIN SMALL LETTER'),

        'v': GD(g2='v', g1='v', l2r='v', uni=0x0076, c='v', name='v', isLower=True, comment='v LATIN SMALL LETTER V'),

        'w': GD(g2='v', g1='v', l='v', r='v', uni=0x0077, c='w', name='w', isLower=True, comment='w LATIN SMALL LETTER W'),
        'wacute': GD(g2='v', g1='v', l='w', w='w', uni=0x1e83, c='ẃ', name='wacute',isLower=True,  base='w', accents=['acutecmb'], comment='ẃ W WITH ACUTE, LATIN SMALL LETTER'),
        'wcircumflex': GD(g2='v', g1='v', l='w', w='w', uni=0x0175, c='ŵ', name='wcircumflex', isLower=True, base='w', accents=['circumflexcmb'], comment='ŵ W WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'wdieresis': GD(g2='v', g1='v', l='w', w='w', uni=0x1e85, c='ẅ', name='wdieresis', isLower=True, base='w', accents=['dieresiscmb'], comment='ẅ W WITH DIAERESIS, LATIN SMALL LETTER'),
        'wgrave': GD(g2='v', g1='v', l='w', w='w', uni=0x1e81, c='ẁ', name='wgrave', isLower=True, base='w', accents=['gravecmb'], comment='ẁ W WITH GRAVE, LATIN SMALL LETTER'),

        'x': GD(g2='x', g1='x', r2l='k', r='k', uni=0x0078, c='x', name='x', isLower=True, comment='x LATIN SMALL LETTER X'),

        'y': GD(g2='y', g1='v', uni=0x0079, c='y', name='y', isLower=True, comment='y LATIN SMALL LETTER Y'), # Manually fit to /v
        'yacute': GD(g2='y', g1='v', l='y', w='y', uni=0x00fd, c='ý', name='yacute', isLower=True, base='y', accents=['acutecmb'], comment='ý Y WITH ACUTE, LATIN SMALL LETTER'),
        'ycircumflex': GD(g2='y', g1='v', l='y', w='y', uni=0x0177, c='ŷ', name='ycircumflex', isLower=True, base='y', accents=['circumflexcmb'], comment='ŷ Y WITH CIRCUMFLEX, LATIN SMALL LETTER'),
        'ydieresis': GD(g2='y', g1='v', l='y', w='y', uni=0x00ff, c='ÿ', name='ydieresis', isLower=True, base='y', accents=['dieresiscmb'], comment='ÿ Y WITH DIAERESIS, LATIN SMALL LETTER'),
        'ygrave': GD(g2='y', g1='v', l='y', w='y', uni=0x1ef3, c='ỳ', name='ygrave', isLower=True, base='y', accents=['gravecmb'], comment='ỳ Y WITH GRAVE, LATIN SMALL LETTER'),

        'yen': GD(g2='Y', g1='Y', l='Y', r='Y', uni=0x00a5, c='¥', base='Y', name='yen', comment='¥ yuan sign'),
        'yen.tab': GD(l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='yen.tab', src='yen', comment='¥ yuan sign TAB'),

        'z': GD(g2='z', g1='z', l2r='z', uni=0x007a, c='z', name='z', isLower=True, comment='z LATIN SMALL LETTER Z'),
        'zacute': GD(g2='z', g1='z', l='z', w='z', uni=0x017a, c='ź', name='zacute', isLower=True, base='z', accents=['acutecmb'], comment='ź Z WITH ACUTE, LATIN SMALL LETTER'),
        'zcaron': GD(g2='z', g1='z', l='z', w='z', uni=0x017e, c='ž', name='zcaron', isLower=True, base='z', accents=['caroncmb'], comment='ž Z WITH CARON, LATIN SMALL LETTER'),
        'zdotaccent': GD(g2='z', g1='z', l='z', w='z', uni=0x017c, c='ż', name='zdotaccent', isLower=True, base='z', accents=['dotaccentcmb'], comment='ż Z WITH DOT ABOVE, LATIN SMALL LETTER'),

        'acutecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0301, c='́', name='acutecmb', anchors=[AD._TOP]),
        'brevecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x306, c='̆', name='brevecmb', anchors=[]),
        'caroncmb': GD(g2='cmb', g1='cmb', w=0, uni=0x030c, c='̌', name='caroncmb', src180='circumflexcmb', anchors=[]),
        'caroncmb.vert': GD(g2='cmb', g1='cmb', l='commabelowcmb', w=0, name='caroncmb.vert', src='commabelowcmb', anchors=[AD._VERT]),
        'cedillacmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0327, name='cedillacmb', anchors=[]),
        'circumflexcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0302, name='circumflexcmb', anchors=[]),
        'commabelowcmb': GD(g2='cmb', g1='cmb', l=GD.CAT_CENTER, w=0, uni=0x0326, name='commabelowcmb', src='comma', anchors=[]),
        'commaturnedabovecmb': GD(g2='cmb', g1='cmb', l=GD.CAT_CENTER,w=0, uni=0x0312, c='̒', src='commabelowcmb', name='commaturnedabovecmb', anchors=[AD._TOP]),
        'dieresiscmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0308, name='dieresiscmb', anchors=[]),
        'dotaccentcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0307, name='dotaccentcmb', anchors=[]),
        'dotmiddlecmb': GD(g2='cmb', g1='cmb', l=GD.CAT_CENTER, w=0, src='dotaccentcmb', name='dotmiddlecmb', anchors=(AD._MIDDLE,)),
        'gravecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0300, c='̀', name='gravecmb', anchors=[AD._TOP]),
        'hungarumlautcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x030B, name='hungarumlautcmb', anchors=[]),
        'macroncmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0304, c='̄', name='macroncmb', anchors=[]),
        'ogonekcmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0328, c='̨', name='ogonekcmb', anchors=[]),
        'eogonekcmb': GD(g2='cmb', g1='cmb', w=0, name='eogonekcmb', src='ogonekcmb', anchors=[]),
        'ringacutecmb': GD(g2='cmb', g1='cmb', w=0, name='ringacutecmb', src=['ringcmb.uc', 'acutecmb.uc'], anchors=[]),
        'ringcmb': GD(g2='cmb', g1='cmb', w=0, l=GD.CAT_CENTER, uni=0x030A, name='ringcmb', useSkewRotate=True, addItalicExtremePoints=True, anchors=[]),
        'tildecmb': GD(g2='cmb', g1='cmb', w=0, uni=0x0303,  name='tildecmb', anchors=[]),

        'acutecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='acutecmb.uc', src='acutecmb', anchors=[]),
        'brevecmb.uc': GD(g2='cmb', g1='cmb', w=0, name='brevecmb.uc', src='brevecmb', anchors=[]),
        'caroncmb.uc': GD(g2='cmb', g1='cmb', w=0, name='caroncmb.uc', src180='circumflexcmb.uc', anchors=[]),
        'circumflexcmb.uc': GD(g2='cmb', g1='cmb', w=0, name='circumflexcmb.uc', src='circumflexcmb', anchors=[]),
        'commaturnedabovecmb.uc': GD(g2='cmb', g1='cmb', l=GD.CAT_CENTER, w=0, name='commaturnedabovecmb.uc', src='commabelowcmb', anchors=[AD._TOP]),
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
        'Euro.tab': GD(g2='Euro.tab', g1='Euro.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='Euro.tab', src='Euro'), # Needs to be scaled
        'Euro.tab.sc': GD(g2='Euro.tab.sc', g1='Euro.tab.sc', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='Euro.tab.sc', base='Euro.sc'),
        'apple': GD(g2='largecircle', g1='largecircle', l='largecircle', r='largecircle', uni=0xf8ff, c='', name='apple', src='paragraph', base='largecircle', comment='TYPETR Logo'),
        'checkmark': GD(g2='v', g1='V', l='v', r='V', uni=0x2713, c='✓', src='y', anchors=[], name='checkmark'),
        'uni00A0': GD(g1='space', g2='space', w=200, uni=0x00a0, name='uni00A0', anchors=[]),
        'copyrightsound': GD(g2='copyright', g1='copyright', l='copyright', r='copyright', uni=0x2117, base='largecircle', name='copyrightsound'),
        'bitcoin': GD(g2='B', g1='H', l='B', r='B', uni=0x20bf, c='₿', name='bitcoin', base='B', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),
        'bitcoin.tab': GD(g2='bitcoin.tab', g1='bitcoin.tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, name='bitcoin.tab', src='bitcoin', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT),

        # In combination with smallcaps
        'dollar.sc': GD(g2='S.sc', g1='S.sc', l='S.sc', r='S.sc', base='S.sc', name='dollar.sc'),
        'sterling.sc': GD(l='sterling', r='sterling', src='sterling', name='sterling.sc'),
        'yen.sc': GD(g2='Y.sc', g1='Y.sc', l='Y.sc', r='Y.sc', base='Y.sc', name='yen.sc'),
        'section.sc': GD(l='section', r='section', src='section', name='section.sc'),
        'paragraph.sc': GD(g2='bar', g1='T.sc', l='paragraph', r='paragraph',src='paragraph', name='paragraph.sc'),

        # Directly link to .sups (instead of .numr/.dnom), to avoid nested component links
        'onehalf': GD(g2='one.sups', g1='two.dnom', bl='one.sups', br='two.sups', uni=0x00BD, c='½', name='onehalf', base='one.numr', accents=['fraction', 'two.dnom'], comment='½ VULGAR FRACTION ONE HALF', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'onequarter': GD(g2='one.sups', g1='four.dnom', bl='one.sups', br='four.sups', uni=0x00BC, c='¼', name='onequarter', base='one.numr', accents=['fraction', 'four.dnom'], comment='¼ VULGAR FRACTION ONE QUARTER', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'threequarters': GD(g2='three.sups', g1='four.dnom', bl='three.sups', br='four.sups', uni=0x00BE, c='¾', name='threequarters', base='three.numr', accents=['fraction', 'four.dnom'], comment='¾ VULGAR FRACTION THREE QUARTERS', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'percent': GD(g2='zero.sups', g1='zero.dnom', bl='zero.sups', br='zero.sups', uni=0x0025, c='%', base='zero.numr', accents=['fraction', 'zero.dnom'], name='percent', comment='% PERCENT SIGN', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'percent.sc': GD(g2='zero.sups', g1='zero.dnom', bl='zero.sups', br='zero.sups', name='percent.sc', base='zero.numr', accents=['slash.sc', 'zero.dnom']),
        'perthousand': GD(g2='zero.sups', g1='zero.dnom', bl='zero.sups', br='zero.sups', uni=0x2030, c='‰', name='perthousand', base='zero.numr', accents=['fraction', 'zero.dnom', 'zero.dnom'], comment='‰ per thousand', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'perthousand.sc': GD(g2='zero.sups', g1='zero.dnom', bl='zero.sups', br='zero.sups', name='perthousand.sc', base='zero.numr', accents=['slash.sc', 'zero.dnom', 'zero.dnom']),

        'zero': GD(g2='zero', g1='zero', l2r='zero', uni=0x0030, c='0', name='zero', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='0 Digits, ASCII', useSkewRotate=True, addItalicExtremePoints=True),
        'zeroslash': GD(g2='zero', g1='zero', l='zero', w='zero', name='zeroslash', base='zero', src='slash', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='0 Digits, ASCII'),
        'one': GD(g2='one', g1='one', l2r='one', uni=0x0031, c='1', name='one', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='1'),
        'two': GD(g2='two', g1='two', l2r='two', uni=0x0032, c='2', name='two', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='2'),
        'two.alt1': GD(g2='two', g1='two', l='two', r='two', name='two.alt1', src='two', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='2 alternative'),
        'three': GD(g2='three', g1='three', l2r='three', uni=0x0033, c='3', name='three', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='3'),
        'four': GD(g2='four', g1='four', uni=0x0034, c='4', name='four', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='4'),
        'five': GD(g2='five', g1='five', l2r='five', uni=0x0035, c='5', name='five', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='5'),
        'five.alt1': GD(g2='five', g1='five', l='five', r='five', name='five.alt1', src='five', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='5 alternative'),
        'six': GD(g2='six', g1='six',  l2r='six', uni=0x0036, c='6', name='six', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='6'),
        'seven': GD(g2='seven', g1='seven', uni=0x0037, c='7', name='seven', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='7'),
        'seven.alt1': GD(g2='seven', g1='seven', l='seven', r='seven', name='seven.alt1', src='seven', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='7 alternative'),
        'eight': GD(g2='eight', g1='eight', l2r='eight', uni=0x0038, c='8', name='eight', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='8'),
        'nine': GD(g2='nine', g1='nine', l2r='six', r2l='six', uni=0x0039, c='9', name='nine', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='9'),

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
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'zeroslash.sc': GD(l='zero.sc', w='zero.sc', base='zero.sc', name='zeroslash.sc', src='slash', comment='0 Digits, ASCII Smallcaps', 
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'one.sc': GD(l='one', l2r='one', src='idotless', name='one.sc', comment='1 Smallcaps',
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'two.sc': GD(l='two', r='two', name='two.sc', src='two', comment='2 Smallcaps', addItalicExtremePoints=True,
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'two.sc.alt1': GD(g2='two.sc', g1='two.sc', l='two.sc', r='two.sc', name='two.sc.alt1', src='two.alt1', comment='2 alternative', addItalicExtremePoints=True,
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'three.sc': GD(l='three', r='three', name='three.sc', src='three', comment='3 Smallcaps', addItalicExtremePoints=True,
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'four.sc': GD(l='four', r='four', name='four.sc', src='four', comment='4 Smallcaps',
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'five.sc': GD(l='five', r='five', name='five.sc', src='five', comment='5 Smallcaps',
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'five.sc.alt1': GD(g2='five.sc', g1='five.sc', l='five.sc', r='five.sc', name='five.sc.alt1', src='five.alt1', comment='5 alternative',
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'six.sc': GD(l='six', r='six', name='six.sc', src='six', comment='6 Smallcapse',  addItalicExtremePoints=True,
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'seven.sc': GD(l='seven', r='seven', name='seven.sc', src='seven', comment='7 Smallcaps',
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'seven.sc.alt1': GD(g2='seven.sc', g1='seven.sc', l='seven.sc', r='seven.sc', name='seven.sc.alt1', src='seven.alt1', comment='5 alternative',
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'eight.sc': GD(l='eight', r='eight', name='eight.sc', src='eight', comment='8 Smallcaps', addItalicExtremePoints=True,
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),
        'nine.sc': GD(l='nine', r='nine', name='nine.sc', src='nine', comment='9 Smallcaps', addItalicExtremePoints=True,
            height=GD.CAT_SC_HEIGHT, overshoot=GD.CAT_SC_OVERSHOOT),

        'zero.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, src='zero', name='zero.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='0 Digits, ASCII TAB', useSkewRotate=True, addItalicExtremePoints=True), # Make as outline, because Black needs to be condensed.
        'zeroslash.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='zero.tab', src='slash', name='zeroslash.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='0 Digits, ASCII TAB slash'), 
        'one.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='one', name='one.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='1 TAB'),
        'two.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='two', name='two.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='2 TAB'),
        'three.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='three', name='three.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='3 TAB'),
        'four.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, src='four', name='four.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='4 TAB'),
        'five.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='five', name='five.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='5 TAB'),
        'six.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, src='six', name='six.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='6 TAB'),
        'seven.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, base='seven', name='seven.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='7 TAB'),
        'eight.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, src='eight', name='eight.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='8 TAB'),
        'nine.tab': GD(g2='tab', g1='tab', l=GD.CAT_CENTER, w=GD.CAT_TAB_WIDTH, src='nine', name='nine.tab', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT, comment='9 TAB'),

        'zero.sups': GD(g2='zero.sups', g1='zero.sups', l2r='zero.sups', uni=0x2070, c='⁰', name='zero.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT, useSkewRotate=True, addItalicExtremePoints=True),
        'onesuperior': GD(g2='one.sups', g1='one.sups', l='one.sups', r='one.sups', uni=0x00b9, c='¹', name='onesuperior', base='one.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'one.sups': GD(g2='one.sups', g1='one.sups', l2r='one.sups', name='one.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'twosuperior': GD(g2='two.sups', g1='two.sups', l='two.sups', r='two.sups', uni=0x00b2, c='²', name='twosuperior', base='two.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'two.sups': GD(g2='two.sups', g1='two.sups', l2r='two.sups', name='two.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'threesuperior': GD(g2='sups', g1='sups', l='three.sups', r='three.sups', uni=0x00b3, c='³', name='threesuperior', base='three.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'three.sups': GD(g2='sups', g1='sups', l2r='three.sups', name='three.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT, addItalicExtremePoints=True),
        'four.sups': GD(g2='four.sups', g1='four.sups', uni=0x2074, c='⁴', name='four.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'five.sups': GD(g2='sups', g1='sups', l2r='five.sups', uni=0x2075, c='⁵', name='five.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'six.sups': GD(g2='sups', g1='sups', l2r='six.sups', uni=0x2076, c='⁶', name='six.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT, addItalicExtremePoints=True),
        'seven.sups': GD(g2='seven.sups', g1='seven.sups', l2r='seven.sups', uni=0x2077, c='⁷', name='seven.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'eight.sups': GD(g2='sups', g1='sups', l2r='eight.sups', uni=0x2078, c='⁸', name='eight.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT, addItalicExtremePoints=True),
        'nine.sups': GD(g2='sups', g1='sups', l2r='six.sups', r2l='six.sups', uni=0x2079, c='⁹', name='nine.sups', baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT, addItalicExtremePoints=True),
        'period.sups': GD(g2='period.sups', g1='period.sups', l='period', r='period', name='period.sups', src='dotaccentcmb', anchors=[], baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'comma.sups': GD(g2='period.sups', g1='period.sups', l='comma', r='comma', name='comma.sups', src='comma', anchors=[], baseline=GD.CAT_SUPS_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),

        'zero.dnom': GD(g2='zero.dnom', g1='zero.dnom', l='zero.sups', w='zero.sups', name='zero.dnom', base='zero.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'one.dnom': GD(g2='one.dnom', g1='one.dnom', l='one.sups', w='one.sups', name='one.dnom', base='one.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'two.dnom': GD(g2='two.dnom', g1='two.dnom', l='two.sups', w='two.sups', name='two.dnom', base='two.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'three.dnom': GD(g2='dnom', g1='dnom', l='three.sups', w='three.sups', name='three.dnom', base='three.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'four.dnom': GD(g2='four.dnom', g1='four.dnom', l='four.sups', w='four.sups', name='four.dnom', base='four.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'five.dnom': GD(g2='dnom', g1='dnom', l='five.sups', w='five.sups', name='five.dnom', base='five.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'six.dnom': GD(g2='dnom', g1='dnom', l='six.sups', w='six.sups', name='six.dnom', base='six.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'seven.dnom': GD(g2='seven.dnom', g1='seven.dnom', l='seven.sups', w='seven.sups', name='seven.dnom', base='seven.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'eight.dnom': GD(g2='dnom', g1='dnom', l='eight.sups', w='eight.sups', name='eight.dnom', base='eight.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'nine.dnom': GD(g2='dnom', g1='dnom', l='nine.sups', w='nine.sups', name='nine.dnom', base='nine.sups', baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'period.dnom': GD(g2='period.dnom', g1='period.dnom', l='period', r='period', name='period.dnom', base='period.sups', anchors=[], baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'comma.dnom': GD(g2='period.dnom', g1='period.dnom', l='comma', r='comma', name='comma.dnom', base='comma.sups', anchors=[], baseline=GD.CAT_DNOM_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),

        'zero.numr': GD(g2='zero.numr', g1='zero.numr', l='zero.sups', w='zero.sups', name='zero.numr', base='zero.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'one.numr': GD(g2='one.numr', g1='one.numr', l='one.sups', w='one.sups', name='one.numr', base='one.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'two.numr': GD(g2='two.numr', g1='two.numr', l='two.sups', w='two.sups', name='two.numr', base='two.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'three.numr': GD(g2='numr', g1='numr', l='three.sups', w='three.sups', name='three.numr', base='three.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'four.numr': GD(g2='four.numr', g1='four.numr', l='four.sups', w='four.sups', name='four.numr', base='four.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'five.numr': GD(g2='numr', g1='numr', l='five.sups', w='five.sups', name='five.numr', base='five.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'six.numr': GD(g2='numr', g1='numr', l='six.sups', w='six.sups', name='six.numr', base='six.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'seven.numr': GD(g2='seven.numr', g1='seven.numr', l='seven.sups', w='seven.sups', name='seven.numr', base='seven.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'eight.numr': GD(g2='numr', g1='numr', l='eight.sups', w='eight.sups', name='eight.numr', base='eight.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'nine.numr': GD(g2='numr', g1='numr', l='nine.sups', w='nine.sups', name='nine.numr', base='nine.sups', baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'period.numr': GD(g2='period.numr', g1='period.numr', l='period', r='period', name='period.numr', base='period.sups', anchors=[], baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'comma.numr': GD(g2='period.numr', g1='period.numr', l='comma', r='comma', name='comma.numr', base='comma.sups', anchors=[], baseline=GD.CAT_NUMR_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),

        'zero.sinf': GD(g2='zero.sinf', g1='zero.sinf', l='zero.sups', w='zero.sups', uni=0x2080, c='₀', name='zero.sinf', base='zero.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'one.sinf': GD(g2='one.sinf', g1='one.sinf', l='one.sups', w='one.sups', uni=0x2081, c='₁', name='one.sinf', base='one.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'two.sinf': GD(g2='two.sinf', g1='two.sinf', l='two.sups', w='two.sups', uni=0x2082, c='₂', name='two.sinf', base='two.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'three.sinf': GD(g2='sinf', g1='sinf', l='three.sups', w='three.sups', uni=0x2083, c='₃', name='three.sinf', base='three.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'four.sinf': GD(g2='four.sinf', g1='four.sinf', l='four.sups', w='four.sups', uni=0x2084, c='₄', name='four.sinf', base='four.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'five.sinf': GD(g2='sinf', g1='sinf', l='five.sups', w='five.sups', uni=0x2085, c='₅', name='five.sinf', base='five.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'six.sinf': GD(g2='sinf', g1='sinf', l='six.sups', w='six.sups', uni=0x2086, c='₆', name='six.sinf', base='six.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'seven.sinf': GD(g2='seven.sinf', g1='seven.sinf', l='seven.sups', w='seven.sups', uni=0x2087, c='₇', name='seven.sinf', base='seven.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'eight.sinf': GD(g2='sinf', g1='sinf', l='eight.sups', w='eight.sups', uni=0x2088, c='₈', name='eight.sinf', base='eight.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'nine.sinf': GD(g2='sinf', g1='sinf', l='nine.sups', w='nine.sups', uni=0x2089, c='₉', name='nine.sinf', base='nine.sups', baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'period.sinf': GD(g2='period.sinf', g1='period.sinf', l='period', r='period', name='period.numr', base='period.sups', anchors=[], baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),
        'comma.sinf': GD(g2='period.sinf', g1='period.sinf', l='comma', r='comma', name='comma.numr', base='comma.sups', anchors=[], baseline=GD.CAT_SINF_BASELINE, height=GD.CAT_SUPS_HEIGHT, overshoot=GD.CAT_SUPS_OVERSHOOT),

    }

'''
# Special version for italic with changed spacing rules
GLYPH_DATA_ITALIC = gids = deepcopy(GLYPH_DATA)

# For /a connectors bottom right are the same for roman and italic
# Ignore the left shape difference for /a and /ae in italic: keep in the same group.
gids['ae'] = GD(g2='ae', g1='e', br='e', uni=0x00e6, c='æ', name='ae', isLower=True, comment='æ small ligature ae, latin')
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

gids['b'] = GD(g2='l', g1='o', l='h', r='o', uni=0x0062, c='b', name='b', comment='b')
gids['b.topLeftDown'] = GD(g2='l', g1='b', l='l', w='b', name='b.topLeftDown', base='b', accents=['flourish.topLeftDown2sl'], comment='b simple flourish bottom right upwards')

gids['d'] = GD(g2='o', g1='l', l='o', r='u', uni=0x0064, c='d', name='d', comment='d', anchors=CARON_ANCHORS)
gids['dcaron'].g2 = 'o'
gids['dcroat'].g2 = 'o'

gids['f'] = GD(g2='f', g1='f', rightMin=GD.CAT_MIN_RIGHT, fixAnchors=False, uni=0x0066, c='f', name='f', comment='f')
gids['florin'] = GD(g2='f', g1='f', w='f', uni=0x0192, c='ƒ', name='florin', src='f', comment='ƒ script f, latin small letter')

gids['g'] = GD(g2='o', g1='g', l='o', r='jdotless', uni=0x0067, c='g', name='g', comment='g')
gids['g.topRightUp'] = GD(g2='o', g1='g', l='g', w='g', name='g.topRightUp', base='g', accents=['flourish.topRightUp2'], comment='g simple flourish top right upwards')
# Keep earlessg in italic for compatibility
gids['earlessg'] = GD(g2='o', g1='g', l='g', w='g', name='earlessg', base='g', comment='In Roman g with ear to accommodate accents. Italic is just a g component')
gids['gbreve'] = GD(g2='o', g1='g', l='g', w='g', uni=0x011f, c='ğ', name='gbreve', base='g', accents=['brevecmb'], comment='ğ G WITH BREVE, LATIN SMALL LETTER')
gids['gcaron'] = GD(g2='o', g1='g', l='g', w='g', uni=0x01e7, c='ǧ', name='gcaron', base='g', accents=['caroncmb'], comment='ǧ G WITH CARON, LATIN SMALL LETTER')
gids['gcircumflex'] = GD(g2='o', g1='g', l='g', w='g', uni=0x011d, c='ĝ', name='gcircumflex', base='g', accents=['circumflexcmb'], comment='ĝ G WITH CIRCUMFLEX, LATIN SMALL LETTER')
gids['gcommaaccent'].g2 = 'o'
gids['gdotaccent'].g2 = 'o'

gids['h'] = GD(g2='l', g1='n', r='n', uni=0x0068, c='h', name='h', comment='h')

gids['idotless'] =  GD(g2='i', g1='i', l='n', r='n', name='idotless', comment='i - connector bottom right')
gids['i'] =  GD(g2='i', g1='i', l='idotless', w='idotless', name='i', uni=0x0069, c='i', comment='i - connector bottom right')

gids['k'] = GD(g2='l', g1='k', l='h', uni=0x006b, c='k', name='k', comment='k')

# Italic has round bottom, more line /i than /h
gids['l'] = GD(g2='l', g1='l', l='h', r='n', uni=0x006c, c='l', name='l', comment='l', anchors=CARON_ANCHORS)
gids['l.cbr'] = GD(g2='l', g1='l', l='l', w='l', name='l.cbr', template='l', src='l', anchors=CARON_ANCHORS, comment='l - connector bottom')
gids['lacute'] = GD(g2='l', g1='l', l='l', w='l', uni=0x013a, c='ĺ', name='lacute', isLower=True, base='l', accents=['acutecmb.uc'], comment='ĺ L WITH ACUTE, LATIN SMALL LETTER')
gids['lcaron'] = GD(g2='l', g1='dcaron', l='l', br='comma', uni=0x013e, c='ľ', name='lcaron', base='l', isLower=True, accents=['caroncmb.vert'], comment='ľ L WITH CARON, LATIN SMALL LETTER')
gids['lcommaaccent'] = GD(g2='l', g1='l', l='l', w='l', uni=0x013c, c='ļ', name='lcommaaccent',isLower=True, base='l', accents=['commabelowcmb'])
gids['ldot'] = GD(g2='l', g1='ldot', l='l', uni=0x0140, c='ŀ', name='ldot', isLower=True, base='l', accents=['dotmiddlecmb'], comment='ŀ MIDDLE DOT, LATIN SMALL LETTER L WITH')
gids['lslash'] = GD(g2='l', g1='l', l='l', w='l', uni=0x0142, c='ł', name='lslash', isLower=True, base='l', comment='ł L WITH STROKE, LATIN SMALL LETTER')

gids['thorn'] = GD(g2='l', g1='o', l='h', r='p', uni=0x00fe, c='þ', name='thorn', src='p', comment='þ THORN, LATIN SMALL LETTER')

gids['u'] = GD(g2='u', g1='u', r='a', uni=0x0075, c='u', name='u', comment='u')
gids['uogonek'] = GD(g2='u', g1='u', l='u', w='u', uni=0x0173, c='ų', name='uogonek', isLower=True, base='u', accents=['ogonekcmb'], comment='ų U WITH OGONEK, LATIN SMALL LETTER')

gids['v'] = GD(g2='v', g1='v', uni=0x0076, c='v', name='v', comment='v LATIN SMALL LETTER V')

gids['w'] = GD(g2='v', g1='v', l='v', r='v', uni=0x0077, c='w', name='w', isLower=True, comment='w LATIN SMALL LETTER W')
gids['wacute'].l = 'v'
gids['wcircumflex'].l = 'v'
gids['wdieresis'].l = 'v'
gids['wgrave'].l = 'v'

gids['x'] = GD(g2='x', g1='x', l2r='x', uni=0x0078, c='x', name='x', comment='x LATIN SMALL LETTER X')

gids['y'] = GD(g2='y', g1='y', uni=0x0079, c='y', name='y', comment='y LATIN SMALL LETTER Y')

gids['R'] = GD(g2='H', g1='R', l='H', uni=0x0052, c='R', name='R', comment='R')

gids['ampersand'] = GD(g2='ampersand', g1='ampersand', r2l='three', uni=0x0026, c='&', name='ampersand', comment='& AMPERSAND', height=GD.CAT_CAP_HEIGHT, overshoot=GD.CAT_CAP_OVERSHOOT)
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

'''
