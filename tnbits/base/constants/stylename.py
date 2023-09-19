# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

from collections import OrderedDict
import re

STYLENAME_DEFAULT_VALUES = {
                            'optical': 500.0,
                            'grade': 0.0,
                            'width': 500.0,
                            'weight': 400.0,
                            'posture': 0.0,
                            'decorative': 0.0,
                            }

STYLENAME_DEFAULT_ORDER = ['optical', 'grade', 'width', 'weight', 'posture',
        'decorative']

STYLENAME_PREFERRED_VALUES = OrderedDict()

STYLENAME_PREFERRED_VALUES['optical'] = (
    ('Micro',    100),
    ('Reading Edge',    150),
    ('Agate',    200),
    ('Caption',    300),
    ('Text',    400),
    ('',        500.0),
    ('Deck',    600),
    ('Subhead',    700),
    ('Display',    800),
    ('Banner',    900),
)

STYLENAME_PREFERRED_VALUES['grade'] = (
    ('Zero',        0.0),
    ('One',        100),
    ('Two',        200),
    ('Three',    300),
    ('Four',        400),
    ('Five',        500),
    ('Six',        600),
    ('Seven',    700),
    ('Eight',    800),
    ('Nine',        900),
)

    ##this one is a dict
    #NAME_ORDERING['grade'] = {
    #    'Zero':        0.0,
    #    'One':        100,
    #    'Two':        200,
    #    'Three':    300,
    #    'Four':        400,
    #    'Five':        500,
    #    'Six':        600,
    #    'Seven':    700,
    #    'Eight':    800,
    #    'Nine':        900,
    #}

STYLENAME_PREFERRED_VALUES['width'] = (
    ('Skyline',                100),
    ('Extra Compressed',    140),
    ('Compressed',            200),
    ('Extra Condensed',        300),
    ('Condensed',            400),
    ('Narrow',                440),
    ('Normal',                500.0),
    ('Wide',                600),
    ('Extended',            700),
    ('Extra Extended',        800),
    ('Ultra Extended',        900),
)

STYLENAME_PREFERRED_VALUES['weight'] = (
    ('Hairline',    100),
    ('Thin',        150),
    ('Extra Light',    200),
    ('Light',        300),
    ('Semi Light', 325),
    ('Book',        350),
    ('Regular',        400.0),
    ('Standard',    450),
    ('Medium',        500),
    ('Semibold',      600),
    ('Semi Bold',    600),
    ('Bold',        700),
    ('Extra Bold',    750),
    ('Heavy', 760),
    ('Black',        800),
    ('Extra Black',    850),
    ('Ultra', 860),
    ('Ultra Black',    900),
)

STYLENAME_PREFERRED_VALUES['posture'] = (
    ('',        0.0),
    ('Italic',    1),
)

STYLENAME_PREFERRED_VALUES['decorative'] = (
    ('Solid',    0.0),
    ('Inline',    10),
    ('Open',    20),
    ('Outline',    30),
)

# This is from chris's thing, which replaced metaInfo

STYLENAME_REPLACE = (

    # ('unambigious abbreviation', ('list','of','real-life','terms'))

    # first item in the right-hand list is the "official" full-length term
    #  which should be referenced in NAME_ORDERING below
    # lists of partial words should be LONGEST FIRST, e.g. ('Italic', 'Itali', 'Ital', 'Ita')

    #things on the right will be replaced with abbreviations on the left,
    # then the abbreviations will be re-replaced with the first thing in the list

    # the upshot is: anything on the line will be replaced with the first item in the list

    # short / ambiguous things should be up top, so that the longer ones down below work correctly

    ('Ex', ('Extra', 'Extr', 'Ext',)), #this needs to be before all the multi-word Extra things
    ('Bd', ('Bold','Bld','Bol',)), #this needs to be before Semi Bold etc.

    ('Com', ('Compressed','Comp',)),
    ('Con', ('Condensed','Cond',)), #this needs to be before Narrow

    ('Nar', ('Narrow', 'Semi Condensed', 'Narr', 'Nrrw',)), #this needs to be above "Sem"
    ('Nrm', ('Normal', 'Norm', 'Nrml', 'Nor',)),
    ('Wd', ('Wide',)),
    ('Extd', ('Extended', 'Expanded', 'Expd',)),

    ('Hair', ('Hairline',)),
    ('Thi', ('Thin',)),
    ('Lt', ('Light','Lig',)),
    ('Bk', ('Book',)),
    ('Reg', ('Regular','Roman','Lean','Rom',)),
    ('Med', ('Medium',)),
    ('Sem', ('Semi Bold', 'Demi Bold', 'Semibold', 'Demibold', 'Semibld', 'Demibld', 'Semi','Demi','Dem',)),
#bold is up above to make Semi Bold work
    ('Bla', ('Black','Blk','Fat',)),
    ('ExtBla', ('Extra Black', 'Extrablack',)),
    ('Ult', ('Ultra Black','Ultra Bold', 'Ultrablack', 'Ultrabold', 'Ultra')), #NOTE this will replace Ultra * with Ultra Black *
    ('Hvy', ('Extra Bold', 'Extrabold', 'Heavy',)),

#this is needed because Ultra Condensed just got converted to Ultra Black Condensed above
    ('UltCnd', ('Ultra Condensed', 'Ultra Black Condensed',)),
    ('UltLt', ('Ultra Light', 'Ultra Black Light',)),

    ('Capt', ('Caption',)),
    ('Subhd', ('Subhead',)),
    ('Disp', ('Display',)),
    ('Ban', ('Banner',)),

    ('It', ('Italic', 'Itali', 'Ital', 'Ita',)),

    ('Mod', ('Modern',)),

    ('SC', ('Small Caps', 'Smallcaps',)),
    ('LF', ('Lining Figures',)),
    ('OSF', ('Old-style Figures', 'Old-Style Figures', 'Oldstyle Figures', 'Oldstyle', 'OsF',)),
    ('TF', ('Tabular Figures','Tab',)),
    ('CE', ('Central European',)),
    ('Exp', ('Expert',)),
    ('sOT', ('Simple OpenType',)),
    ('Swa', ('Swash',)),
    ('Pre', ('Premium',)),
    ('Alt', ('Alternates','Alternate',)),
)

@classmethod
def STYLENAME_ORDER_RE(cls):
    NAME_ORDER_RE = {}

    for k, vv in cls.STYLENAME_REPLACE:
        NAME_ORDER_RE[k] = re.compile(r'\b{0}\b'.format(k),re.I)
        for v in vv:
            NAME_ORDER_RE[v] = re.compile(r'\b{0}\b'.format(v),re.I)


    for l in cls.STYLENAME_PREFERRED_VALUES.values():
        if isinstance(l,tuple):
            for k,_ in l:
                if k and k not in NAME_ORDER_RE:
                    NAME_ORDER_RE[k] = re.compile(r'\b{0}\b'.format(k),re.I)

    NAME_ORDER_RE['grade_numbers'] = re.compile(r'\b(Zero|One|Two|Three|Four|Five|Six|Seven|Eight|Nine)\b',re.I)
    return NAME_ORDER_RE

PREFERRED_ABBREVIATIONS_GENERIC = {
    'Extra': 'Ex',
}

PREFERRED_ABBREVIATIONS_SUBSET = {
    'Modern': 'Mod',
    'Small Caps': 'SC',
    'Lining Figures': 'LF',
    'Old-style Figures': 'OSF',
    'Tabular Figures': 'TF',
    'Central European': 'CE',
    'Expert': 'Exp',
    'Simple OpenType': 'sOT',
    'Swash': 'Swa',
    'Premium': 'Pre',
    'Alternates': 'Alt',
}

PREFERRED_ABBREVIATIONS_OPTICAL = {
    'Caption': 'Capt',
    'Subhead': 'Subhd',
    'Display': 'Disp',
    'Banner': 'Ban',
                                   }

PREFERRED_ABBREVIATIONS_WEIGHT = {
    'Bold': 'Bd',
    'Hairline': 'Hair',
    'Thin': 'Thi',
    'Light': 'Lt',
    'Book': 'Bk',
    'Regular': 'Reg',
    'Medium': 'Med',
    'Semi Bold': 'Sem',
    'Black': 'Bla',
    'Extra Black': 'Ex Bla',
    'Ultra Black': 'Ult',
    'Extra Bold': 'Ex Bold',
    'Heavy': 'Hvy',
    'Ultra Light': 'Ult Lt',
}

PREFERRED_ABBREVIATIONS_WIDTH = {
    'Compressed': 'Comp',
    'Condensed': 'Cond',
    'Narrow': 'Nar',
    'Normal': 'Nrm',
    'Wide': 'Wd',
    'Extended': 'Extd',
    'Ultra Condensed': 'Ult Cnd',

}

PREFERRED_ABBREVIATIONS_POSTURE = {
    'Italic': 'It',
    'Roman': 'Rom',
}

PREFERRED_ABBREVIATIONS = {}
PREFERRED_ABBREVIATIONS.update(PREFERRED_ABBREVIATIONS_GENERIC)
PREFERRED_ABBREVIATIONS.update(PREFERRED_ABBREVIATIONS_SUBSET)
PREFERRED_ABBREVIATIONS.update(PREFERRED_ABBREVIATIONS_OPTICAL)
PREFERRED_ABBREVIATIONS.update(PREFERRED_ABBREVIATIONS_WEIGHT)
PREFERRED_ABBREVIATIONS.update(PREFERRED_ABBREVIATIONS_WIDTH)
PREFERRED_ABBREVIATIONS.update(PREFERRED_ABBREVIATIONS_POSTURE)

if __name__ == "__main__":
    print(PREFERRED_ABBREVIATIONS)
