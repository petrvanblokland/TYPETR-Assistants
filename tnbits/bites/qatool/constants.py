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
#    constants.py
#
from tnbits.base.c import FONTINFO_ATTRS
STYLE_MARKER = {True: u'•', False: ''}
topMenu = 48
line = 20
indent = 80
tabularWidth = 650


ots_path = None

# glyph groups.

ignoredAccentNames = ['threequarters', 'dcaron', 'tbar', 'dcroat',
        'cedilla', 'ring', 'tcaron', 'ldot', 'onehalf', 'grave',
        'dotaccent', 'macron', 'onequarter', 'hbar', 'breve', 'ij',
        'Dcroat', 'commaaccent', 'IJ', 'tilde', 'acute', 'lcaron',
        'jcircumflex', 'hungarumlaut', 'dieresis', 'ogonek']

capGlyphs = ['b', 'd', 'h', 'k', 'l', 'i', 'j']
descenderGlyphs = ['g', 'j', 'p', 'q', 'y']
verticalSizeReportGlyphs = {'capGlyphs': capGlyphs, 'descGlyphs': descenderGlyphs}

ignoredAccentSubstrings = ['cyrillic', 'accent', "afii", 'afii100'
        'cmb', 'comb', 'dotless', 'apostrophe', 'slash', 'bar']

zeroWidthUnicodeAccents = ['0317', '0301', '0341', '032E', '0306', '032F',
        '0311', '0361', '032A', '033A', '0310', '032C', '030C', '0327',
        '032D', '0302', '0313', '0315', '0314', '0312', '0485', '032B',
        '030F', '0333', '033F', '030E', '0344', '0324', '0308', '0307',
        '0323', '031E', '0316', '0300', '0340', '0309', '0321', '0322',
        '031B', '030B', '0343', '031A', '0318', '0332', '0331', '0304',
        '0320', '0328', '0305', '0484', '0342', '031F', '0486', '0319',
        '0325', '030A', '031C', '0339', '033C', '0338', '0337', '033B',
        '0336', '0335', '0330', '0303', '0360', '0334', '033E', '0483',
        '031D', '030D', '0329', '033D', '0345']

symmetricalSidebearingsGlyphs = ['H', 'I', 'O', 'T', 'I.sc', 'O.sc',
        'Tbar.sc', 'i', 'l', 'dotlessi', 'zero', 'zero.dnom', 'zero.numr',
        'zero.salt_slash', 'zero.sc', 'zero.sc_salt_slash', 'zero.tab',
        'zero.tab_salt_slash', 'zero.sinf', 'zero.sups', 'underscore',
        'hyphen', 'endash', 'emdash', 'emdash.salt_em', 'endash.salt_en',
        'endash.tab', 'hyphen.uc', 'endash.uc', 'emdash.uc',
        'emdash.uc_salt_em', 'endash.uc_salt_en', 'exclam', 'period',
        'colon', 'periodcentered', 'dagger', 'daggerdbl', 'bullet',
        'exclam.sc', 'exclamdown.sc', 'comma.tab', 'period.tab',
        'colon.tab', 'periodcentered.uc', 'plus', 'equal', 'bar',
        'plusminus', 'multiply', 'divide', 'minus', 'infinity', 'plus.sc',
        'equal.sc', 'minus.sc', 'plus.tab', 'equal.tab', 'multiply.tab',
        'divide.tab', 'minus.tab', 'brokenbar', 'degree', 'registered',
        'registered.salt_big', 'copyright', 'copyrightsound', 'uni2117',
        'registered.salt_big', 'Delta', 'Omega']

controlSidebearingsGlyphs = ['H', 'O', 'D', 'V', 'zero', 'n', 'o', 'd',
        'v', 'I']

negativeSidebearingsIgnores = ['grave', 'acute', 'ogonek', 'caron',
        'circumflex', 'dieresis', 'tilde', 'dotaccent', 'ring',
        'commaaccent', 'cedilla', 'macron', 'breve', 'hungarumlaut',
        'slash', 'bar', ('horn', ['thorn'])]

spacingGroupsGlyphs = [('f_f', 'f', 'f'), ('dotlessi', 'i', 'i'),
        ('dotlessj', 'j', 'j'), ('f_i', 'f', 'i'), ('f_f_i', 'f', 'i'),
        ('f_l', 'f', 'l'), ('f_f_l', 'f', 'l'), ('f_j', 'f', 'j'), ('ae',
            'a', 'e'), ('oe', 'o', 'e'), ('AE', 'A', 'E'), ('OE', 'O',
                'E'), ('AE.sc', 'A.sc', 'E.sc'), ('OE.sc', 'O.sc', 'E.sc')]

troublesomeGlyphs = ['litre', 'plus', 'minus', 'divide', 'multiply', 'equal',
        'less', 'greater', 'lessequal', 'greaterequal', 'approxequal',
        'notequal', 'logicalnot', 'partialdiff', 'product', 'summation',
        'radical', 'infinity', 'integral', 'dollar', 'cent', 'sterling',
        'currency', 'yen', 'estimated', 'lozenge', 'numbersign', 'percent',
        'per', 'thousand', 'ordfeminine', 'ordmasculine', 'one', 'quarter',
        'onehalf', 'threequarters', 'apple', 'plus', 'minus']

# Categories & functions.

categoryOrder = ('info', 'glyphs', 'outline', 'spacing', 'kerning', 'features', 'openType')
allFunctions = {'info': ['verticalMetrics',
                        'checkOS2Values'],
            'glyphs': ['count', 'compare', 'unicodes'],
            'outline': ['findOpenContours',
                        'crossingHandles',
                        'verticalSizeReport',
                        'controlOvershoots',
                        'findDuplicateComponents',
                        'findMissingComponents',
                        'compareContourOrder',
                        ],
            'kerning': ['countTotalKerns',
                        #'duplexing',
                        'questionablePairs',
                        'glyphsWithNoKerns',
                        'sameGlyphInMultipleGroups',
                        'missingGlyphsInGroups',
                        'missingGroups',
                        'duplicateGlyphsInGroups',
                        'emptyGroups',
                        'zeroValueKerning',
                        'glyphInGroupAndSeparate',
                        'showFlattenedGroups',
                        'flattenWithExceptions',
                        ],

            'spacing': ['accentedWidths',
                        'tabularWidths',
                        'compareTabularWidths',
                        'controlSidebearings',
                        'negativeSidebearings',
                        'symmetricalSidebearings',
                        'spacingGroups'],
            'features': ['missingGroupNames', 'reportSuffixes'],
            'openType': ['sanitiser'],
            }
coreFunctions = ['verticalMetrics', 'controlOvershoots', 'crossingHandles',
                'countTotalKerns', 'accentedWidths', 'findOpenContours']
referenceFunctions = ['verticalMetrics', 'compare', 'compareTabularWidths']
functionArgs = {'verticalMetrics': FONTINFO_ATTRS,
        'verticalSizeReport': verticalSizeReportGlyphs,
        'checkOS2Values': FONTINFO_ATTRS,
        'accentedWidths': {'ignoredNames': ignoredAccentNames,
            'ignoredSubstrings': ignoredAccentSubstrings,
            'zeroWidthUnicodes': zeroWidthUnicodeAccents},
        'controlSidebearings': controlSidebearingsGlyphs,
        'symmetricalSidebearings': symmetricalSidebearingsGlyphs,
        'negativeSidebearings': negativeSidebearingsIgnores,
        'spacingGroups': spacingGroupsGlyphs,
        'questionablePairs': troublesomeGlyphs,
        'sanitiser': {'ots_path': ots_path},
}
