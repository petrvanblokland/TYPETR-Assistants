# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   samples.py
#

# FIXME: import from base.
from tnbits.constants import Constants as C
from tnbits.base.constants.sets.dutch import DUTCH_TEXT, IJij_COMBINATIONS
from tnbits.base.constants.sets.spacing import SPACING
from tnbits.base.constants.sets.kerning import EXTENDED_KERNING, CONTEXT_KERNING
from tnbits.base.constants.sets.jillskerning import JILLS_KERNING
from tnbits.base.constants.sets.typetr import TYPETR_RESPONDER, TYPETR_RESPONDER_CONNECTORS
from tnbits.base.constants.sets.cyrillic import (CYRILLIC_NONSLAVIC_TEXT,
        CYRILLIC_SLAVIC_TEXT, CYRILLIC_KERNING_TEXT, CYRILLIC_KERNING,
        GREEK_KERNING)
from tnbits.base.constants.sets.ulcwords import ULCWORDS_PAGE, USCWORDS_PAGE

def flattenSpaces(text):
    fourSpaces = '    '

    #TODO: add carriage return etc.
    newLine = '\n'
    text = text.replace(newLine, ' ')

    while fourSpaces in text:
        text = text.replace(fourSpaces, '')

    return text

def getUnicodeNames(flightPathName):
    """Answer the set with unicodes names from the defined flight path."""
    baseUnicodes = C.FLIGHTPATHS.get(flightPathName)
    unicodeNames = []

    if baseUnicodes is not None:
        for baseUnicode in baseUnicodes:
            unicodeName = C.CMAP_FBGLYPHLIST.get(baseUnicode)
            if unicodeName is not None and not unicodeName[0].startswith('control'):
                unicodeNames.append(unicodeName[0])

    return unicodeNames

DUTCH_TEXT_PAGE = flattenSpaces(DUTCH_TEXT)

#   A N C H O R S
#
# Standard anchor names

ANCHOR_CENTERABOVE = 'centerAbove' # x-axis centering for all anchors above
ANCHOR_CENTERBELOW = 'centerBelow' # x-axis centering for all anchors below
ANCHOR_RIGHTABOVE = 'rightAbove' # x-axis
ANCHOR_RIGHTBELOW = 'rightBelow' # x-axis
ANCHOR_LEFTABOVE = 'leftAbove' # x-axis
ANCHOR_LEFTBELOW = 'leftBelow' # x-axis
ANCHOR_ORIGINX = 'originX' # x-axis baseline
ANCHOR_TOP = 'top' # y-axis, xHeight, scapHeight or capHeight
ANCHOR_MIDDLE = 'middle'
ANCHOR_BOTTOM = 'bottom' # y-axis bottom
ANCHOR_ORIGINY = 'originY' # y-axis baseline

ANCHORS = set((ANCHOR_CENTERABOVE, ANCHOR_CENTERBELOW, ANCHOR_RIGHTABOVE,
    ANCHOR_RIGHTBELOW, ANCHOR_LEFTABOVE, ANCHOR_LEFTBELOW, ANCHOR_TOP,
    ANCHOR_MIDDLE, ANCHOR_BOTTOM, ANCHOR_ORIGINX, ANCHOR_ORIGINY))

BASEGLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 '

LOREM_IPSUM_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing
    elit. Quisque eu elit placerat, tristique arcu sed, gravida nunc. Nulla
    sollicitudin vulputate ex, sit amet ullamcorper neque pellentesque at.
    Maecenas ut lectus lobortis, consequat lectus ut, imperdiet sapien.
    Sed porta scelerisque massa et iaculis. Donec in ante eget lectus
    pulvinar euismod. Suspendisse potenti. Nam viverra sed sapien sit amet
    iaculis. In vestibulum purus nec dapibus tempor. Curabitur porta
    feugiat ex in ultrices. Sed ultricies lobortis tristique. Sed eu arcu
    venenatis, sodales justo congue, faucibus leo. Aliquam volutpat gravida
    nulla, at elementum est condimentum non. Aenean ac luctus elit, sed
    pretium lorem. Sed cursus pharetra finibus. Etiam vitae tortor vitae
    sem faucibus condimentum. Ut et varius massa, eget gravida eros.
    Phasellus sagittis lacinia augue a porta. Quisque vitae lacinia ipsum.
    Morbi tincidunt orci nec risus vulputate aliquam. Curabitur eget enim
    porttitor, dapibus nunc non, blandit dolor. Nam porta nunc nec eros
    elementum, id ornare erat elementum. Quisque sit amet tincidunt lorem,
    condimentum lobortis magna. Sed id quam vitae sapien consectetur
    dapibus. Praesent dictum et risus vitae tincidunt. Fusce id eleifend
    dolor, vitae convallis nunc. Nunc euismod dui ante. Sed id faucibus
    libero. Sed rhoncus tortor eget porta molestie. Vestibulum libero
    massa, sagittis sed justo vitae, vulputate molestie felis. Fusce
    finibus, sem et rutrum gravida, ipsum dolor rhoncus ex, pulvinar
    feugiat nisi ante at ex. Etiam varius consectetur risus sed cursus.
    Donec aliquet augue nulla, quis imperdiet augue facilisis vitae. Donec
    nec viverra diam, ac vulputate turpis. Class aptent taciti sociosqu ad
    litora. Torquent per conubia nostra, per inceptos himenaeos. Sed
    varius elementum erat, sed viverra neque euismod eget. Aenean maximus
    magna a luctus euismod. Vivamus ultrices suscipit pellentesque.
    Praesent fringilla arcu sed arcu hendrerit sagittis eu sed velit.
    Mauris sagittis lorem nec eros placerat volutpat. Praesent purus
    libero, tempor et hendrerit at, venenatis vel odio. Quisque vel
    ultricies felis. Aliquam at facilisis velit, in lobortis neque. Nullam
    ultricies non ipsum et gravida. Vestibulum at ex justo. Aenean
    efficitur, odio ut tempor mollis, est magna suscipit sem, ut
    condimentum ipsum lectus sit amet enim. Donec vitae eros non eros
    semper ultricies eget sit amet ipsum. Quisque et tempor nibh. Aenean
    sed magna urna. Sed eget lectus velit. Ut ornare non erat vel
    facilisis. Vivamus congue vestibulum blandit. Proin a ultrices metus.
    Pellentesque sit amet mauris efficitur, porttitor tellus eget, auctor
    dui. Curabitur dapibus lectus vestibulum nulla aliquet, id sodales
    orci efficitur. Aliquam ac felis fringilla, faucibus dui a, facilisis
    urna. Duis tempor ornare mauris a malesuada."""

LOREM_IPSUM_PAGE = flattenSpaces(LOREM_IPSUM_TEXT)

QUICK_BROWN_FOX_TEXT = "A Quick Brown Fox Jumps Over The Lazy Dog 0123456789"

SURNAMES = """McAdams McBain McClure McDermott McElhenny McFadden MacGyver
    McHale McIver McJunkins McKnabb McLure McMurray McNight McOwer McPeter
    McQuaid McRoberts McStoots McTighe McUmber McVittie McWilliam McZeal
    DaCosta DaFonesca DaMotta DaSilva DeAngelo DeBois DeCicco DeDoming
    DeEspinosa DeFries DeGroot DeHart DeIsaac DeJesu DeKorte DeLuna DeMena
    DeNevers DeOlcotes DePalma DeQuerton DeRevere DeStefano DeTurk DeUmbria
    DeVito DeWitt DeYoe DeZinnia DiAgostino DiBenedetto DiCesare DiDomenico
    DiGiaimo DiLemme DiMarco DiNunzio DiRusso DiStefano DuBois DuFrane DuGuher
    DuPille DuToit"""

SURNAMES = flattenSpaces(SURNAMES)

# Accents need the _anchor name, e.g. Agrave had "top" anchor and grave has
# "_top" anchor at the bottom. Define the general anchor position that this
# accents needs to be attached to.

SS_ACCENTSCMB = {
    'acutecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'gravecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'brevecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'brevecyrilliccmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'circumflexcmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'dieresiscmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'macroncmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'tildecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'hookcmb': (ANCHOR_RIGHTABOVE, ANCHOR_TOP),
    'cedillacmb': (ANCHOR_CENTERBELOW, ANCHOR_ORIGINY),
    'caroncmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'commaaccentcmb': (ANCHOR_CENTERBELOW, ANCHOR_ORIGINY),
    'commaaccentabovecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'commaturnedabovecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'horncmb': (ANCHOR_RIGHTABOVE, ANCHOR_TOP),
    'ringcmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'ringacutecmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'hungarumlautcmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'tonoscmb': (ANCHOR_LEFTABOVE, ANCHOR_TOP),
    'dieresistonoscmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    'dotbelowcmb': (ANCHOR_CENTERBELOW, ANCHOR_BOTTOM), # Previously periodcmb or dotcmb
    'barcmb': (ANCHOR_CENTERABOVE, ANCHOR_MIDDLE),
    'dotcmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    # http://www.twardoch.com/download/polishhowto/kreska.html
    # https://glyphsapp.com/tutorials/localize-your-font-polish-kreska
    'kreskacmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    # http://www.twardoch.com/download/polishhowto/ogonek.html
    'ogonekcmb': (ANCHOR_RIGHTBELOW, ANCHOR_ORIGINY),
    # http://www.twardoch.com/download/polishhowto/kropka.html
    'dotaccentcmb': (ANCHOR_CENTERABOVE, ANCHOR_TOP),
    # http://www.twardoch.com/download/polishhowto/stroke.html
}

SS_ACCENTS = set()
SS_TOPACCENTS = set()

for accentNameCmb, (x, y) in SS_ACCENTSCMB.items():
    accentName = accentNameCmb[:-3]
    if y == ANCHOR_TOP:
        SS_TOPACCENTS.add(accentName)
    SS_ACCENTS.add(accentName)

#   S M A R T S E T S

TN_CONTROLS = ('D', 'H', 'O', 'n', 'o', 'p', 'zero', 'one', 'period', 'comma',
        'emdash', 'slash', 'plus')
TN_LC = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
TN_UC = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
TN_SC = []

for c in TN_UC:
    TN_SC.append(c+'.sc')

TN_FIGURES = ('zero','one','two','three','four','five','six','seven','eight','nine')
TN_PRIMARY = TN_UC + TN_LC + TN_FIGURES + ('parenleft', 'bracketleft',
        'braceleft', 'guillemotleft', 'guilsinglleft', 'exclam', 'question',
        'quotesingle', 'quotedbl', 'quoteright', 'quotedblright', 'underscore',
        'hyphen', 'emdash', 'endash', 'colon', 'period', 'comma', 'semicolon',
        'numbersign', 'percent', 'ampersand', 'asterisk', 'at')

TN_SECONDARY_LC = ('lslash', 'mu1',  'germandbls', 'ae', 'eth', 'oslash', 'oe',
        'thorn', 'dotlessi')
TN_SECONDARY_UC = ('AE', 'Thorn', 'Eth', 'Oslash', 'OE', 'Lslash')
TN_SECONDARY_SC = []
for c in TN_SECONDARY_UC:
    TN_SECONDARY_SC.append(c+'.sc')

TN_SECONDARY_LIGATURES = ("f_i", "f_l", "f_f", "f_f_i", "f_f_l", "f_j", "f_t",
        "f_f_j", "f_f_t", "f_b", "f_f_b", "f_h", "f_f_h", "f_k", "f_f_k")

TN_CURRENCY = ('dollar', 'cent', 'sterling', 'Euro', 'florin', 'currency',
        'yen', 'brokenbar', 'product', 'Omega', 'summation', 'partialdiff',
        'increment', 'pi', 'radical', 'fraction', 'slash', 'integral', 'plus',
        'minus', 'less', 'lessequal', 'equal', 'asciitilde', 'logicalnot',
        'plusminus', 'multiply', 'divide', 'infinity', 'asciicircum', 'bar',
        'brokenbar', 'dagger', 'daggerdbl', 'section', 'paragraph',
        'quotesinglbase', 'quotedblbase', 'ellipsis', 'bullet', 'bullet',
        'Schwa', 'schwa', 'armeniandram', 'afghani', 'rupeemarkbengali',
        'rupeesignbengali', 'gujaratirupee', 'tamilrupee', 'bahtthai', 'khmer',
        'ecu', 'colonsign', 'cruzeiro', 'franc', 'lira', 'mill', 'naira',
        'peseta', 'rupee', 'won', 'sheqel', 'dong', 'kip', 'tugrik', 'dragma',
        'germanpenny', 'peso', 'guarani', 'austral', 'hryvnia', 'cedi',
        'livretournois', 'spesmilo', 'indianrupee', 'turkishlira',
        'nordicmark', 'manat', 'ruble', 'numero', 'trademark', 'scriptm',
        'rialarabic')

TN_SECONDARY = TN_SECONDARY_UC + TN_SECONDARY_LC + TN_SECONDARY_LIGATURES + TN_CURRENCY

TN_SCALARPOLATES = ('ordfeminine', 'ordmasculine', 'parenright',
        'bracketright', 'braceright', 'guilsinglright', 'guillemotright',
        'quoteleft', 'quotedblleft', 'exclamdown', 'periodcentered',
        'periodcentered', 'questiondown', 'trademark', 'copyright',
        'registered', 'copyrightsound', 'degree', 'one.sups', 'two.sups',
        'three.sups', 'lozenge', 'greater', 'greaterequal', 'approxequal',
        'notequal')

# For convenience in spacing and reference the base capitals are also added to this list.
TN_COMPOSITES_LC = ('a', 'aacute', 'abreve', 'acircumflex', 'adieresis', 'ae',
        'aeacute', 'agrave', 'amacron', 'aogonek', 'aring', 'aringacute',
        'atilde', 'b', 'c', 'cacute', 'ccaron', 'ccedilla', 'ccircumflex',
        'cdotaccent', 'ckreska', 'd', 'dcaron', 'dcroat', 'dotlessi',
        'dotlessj', 'e', 'eacute', 'ebreve', 'ecaron', 'ecircumflex',
        'edieresis', 'edotaccent', 'egrave', 'emacron', 'eng', 'eogonek',
        'eth', 'f', 'g', 'gbreve', 'gcircumflex', 'gcommaaccent', 'gdotaccent',
        'germandbls', 'h', 'hbar', 'hcircumflex', 'i', 'iacute', 'ibreve',
        'icircumflex', 'idieresis', 'igrave', 'ij', 'imacron', 'iogonek',
        'itilde', 'k', 'jcircumflex', 'k', 'kcommaaccent', 'kgreenlandic', 'l',
        'lacute', 'lcaron', 'lcommaaccent', 'ldot', 'lslash', 'm', 'n',
        'nacute', 'napostrophe', 'ncaron', 'ncommaaccent', 'nkreska', 'ntilde',
        'o', 'oacute', 'obreve', 'ocircumflex', 'ocreska', 'odieresis', 'oe',
        'ograve', 'ohorn', 'ohungarumlaut', 'omacron', 'oslash', 'oslashacute',
        'otilde', 'p', 'q', 'r', 'racute', 'rcaron', 'rcommaaccent', 's',
        'sacute', 'scaron', 'scedilla', 'schwa', 'scircumflex', 'scommaaccent',
        'skreska', 't', 'tbar', 'tcaron', 'tcedilla', 'tcommaaccent', 'thorn',
        'u', 'uacute', 'ubreve', 'ucircumflex', 'udieresis', 'ugrave', 'uhorn',
        'uhungarumlaut', 'umacron', 'uogonek', 'uring', 'utilde', 'v', 'w',
        'wacute', 'wcircumflex', 'wdieresis', 'wgrave', 'x', 'y', 'yacute',
        'ycircumflex', 'ydieresis', 'ygrave', 'z', 'zacute', 'zcaron',
        'zdotaccent', 'zkreska')

# For convenience in spacing and reference the base capitals are also added to
# this list.
TN_COMPOSITES_UC = ('A', 'AE', 'AEacute', 'Aacute', 'Abreve', 'Acircumflex',
        'Adieresis', 'Agrave', 'Amacron', 'Aogonek', 'Aring', 'Atilde', 'B',
        'C', 'Cacute', 'Ccaron', 'Ccedilla', 'Ccircumflex', 'Cdotaccent',
        'Ckreska', 'Dcaron', 'D', 'Dcroat', 'E', 'Eacute', 'Ebreve', 'Ecaron',
        'Ecircumflex', 'Edieresis', 'Edotaccent', 'Egrave', 'Emacron', 'Eng',
        'Eogonek', 'Eth', 'F', 'G', 'Gbreve', 'Gcircumflex', 'Gcommaaccent',
        'Gdotaccent', 'H', 'Hbar', 'Hcircumflex', 'I', 'IJ', 'Iacute',
        'Ibreve', 'Icircumflex', 'Idieresis', 'Idotaccent', 'Igrave',
        'Imacron', 'Iogonek', 'Itilde', 'J', 'Jcircumflex', 'K',
        'Kcommaaccent', 'L', 'Lacute', 'Lcaron', 'Lcommaaccent', 'Ldot',
        'Lslash', 'N', 'Nacute', 'Ncaron', 'Ncommaaccent', 'Nkreska', 'Ntilde',
        'M', 'O', 'OE', 'Oacute', 'Obreve', 'Ocircumflex', 'Odieresis',
        'Ograve', 'Ohorn', 'Ohungarumlaut', 'Okreska', 'Omacron', 'Oslash',
        'Oslashacute', 'Otilde', 'P', 'Q', 'R', 'Racute', 'Rcaron',
        'Rcommaaccent', 'S', 'Sacute', 'Scaron', 'Scedilla', 'Scircumflex',
        'Scommaaccent', 'Skreska', 'T', 'Tbar', 'Tcaron', 'Tcedilla',
        'Tcommaaccent', 'Thorn', 'U', 'Uacute', 'Ubreve', 'Ucircumflex',
        'Udieresis', 'Ugrave', 'Uhorn', 'Uhungarumlaut', 'Umacron', 'Uogonek',
        'Uring', 'Utilde', 'V', 'W', 'Wacute', 'Wcircumflex', 'Wdieresis',
        'Wgrave', 'X', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ygrave',
        'Z', 'Zacute', 'Zcaron', 'Zdotaccent', 'Zkreska')

TN_COMPOSITES_SC = []
TN_COMPOSITES_LCSC = []
for c in TN_COMPOSITES_UC:
    # For convenience in spacing and reference the base smallcaps are also
    # added to this list.
    TN_COMPOSITES_SC.append(c+'.sc')
    TN_COMPOSITES_LCSC.append(c.lower() + '.sc')

TN_COMPOSITE_FRACTIONS = ('onequarter', 'onehalf', 'threequarters',  'percent',
        'perthousand', )

TN_COMPOSITES = TN_COMPOSITES_UC + TN_COMPOSITES_LC + TN_COMPOSITE_FRACTIONS

TN_ACCENT2CMB = { 'circumflex': 'circumflexcmb', 'caron': 'caroncmb', 'grave':
        'gravecmb', 'dieresis': 'dieresiscmb', 'macron': 'macroncmb', 'acute':
        'acutecmb', 'cedilla': 'cedillacmb', 'breve': 'brevecmb', 'dotaccent':
        'dotaccentcmb', 'ring': 'ringcmb', 'ogonek': 'ogonekcmb', 'tilde':
        'tildecmb', 'hungarumlaut': 'hungarumlautcmb', 'hook': 'hookcmb',
        'caron.vert': 'caroncmb.vert',
}

TN_CMB2ACCENT = {}

for accent, cmb in TN_ACCENT2CMB.items():
    TN_CMB2ACCENT[cmb] = accent

TN_COMBINATES = sorted(TN_ACCENT2CMB.keys())

TN_GREEKPRIMARYCONTROLS = ('H', 'O', 'pi', 'o', 'rho', 'zero', 'one', 'period',
        'comma', 'emdash', 'slash', 'plus')

TN_GREEKPRIMARY = ('Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta',
        'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi',
        'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
        'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho',
        'sigma1', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega')

TN_GREEKCOMPOSITES = ('Alphatonos', 'Epsilontonos', 'Etatonos', 'Iotatonos',
        'Omicrontonos', 'Upsilontonos', 'Omegatonos', 'Iotadieresis',
        'Upsilondieresis', 'alphatonos', 'epsilontonos', 'etatonos',
        'iotatonos', 'upsilondieresistonos', 'iotadieresis',
        'iotadieresistonos', 'upsilondieresis', 'omicrontonos', 'upsilontonos',
        'omegatonos')

TN_GREEKACCENT2CMB = { 'tonos': 'tonoscmb', 'dieresistonos':
        'dieresistonoscmb', 'periodcentered': 'periodcenteredcmb'}

TN_CMB2GREEKACCENT = {}

for accent, cmb in TN_GREEKACCENT2CMB.items():
    TN_CMB2GREEKACCENT[cmb] = accent
TN_GREEKCOMBINATES = sorted(TN_GREEKACCENT2CMB.keys())

TN_CYRILLICPRIMARYCONTROLS = ('Ercyrillic', 'H', 'O', 'pecyrillic',
        'ocyrillic', 'ercyrillic', 'zero', 'one', 'period', 'comma', 'emdash',
        'slash', 'plus')

TN_CYRILLICPRIMARY = ('Acyrillic', 'Vecyrillic', 'Becyrillic', 'Gecyrillic',
        'Decyrillic', 'Iecyrillic', 'Zhecyrillic', 'Zhedescendercyrillic',
        'Zecyrillic', 'Iicyrillic', 'Kacyrillic', 'Kadescendercyrillic',
        'Elcyrillic', 'Icyrillic', 'Emcyrillic', 'Encyrillic', 'Jecyrillic',
        'Ocyrillic', 'Pecyrillic', 'Ercyrillic', 'Escyrillic', 'Dzecyrillic',
        'Tecyrillic', 'Ucyrillic', 'Efcyrillic', 'Khacyrillic',
        'Hadescendercyrillic', 'Tsecyrillic', 'Ljecyrillic', 'Njecyrillic',
        'Tshecyrillic', 'Djecyrillic', 'Checyrillic', 'Chedescendercyrillic',
        'Hardsigncyrillic', 'Yericyrillic', 'Softsigncyrillic', 'Dzhecyrillic',
        'Shacyrillic', 'Shchacyrillic', 'Ereversedcyrillic', 'Ecyrillic',
        'IUcyrillic', 'IAcyrillic', 'Gheupturncyrillic',
        'Ustraightstrokecyrillic', 'acyrillic', 'vecyrillic', 'becyrillic',
        'gecyrillic', 'decyrillic', 'iecyrillic', 'zhecyrillic',
        'zhedescendercyrillic', 'zecyrillic', 'iicyrillic', 'kacyrillic',
        'kadescendercyrillic', 'elcyrillic', 'emcyrillic', 'encyrillic',
        'jecyrillic', 'ocyrillic', 'pecyrillic', 'ercyrillic', 'escyrillic',
        'tecyrillic', 'ucyrillic', 'efcyrillic', 'khacyrillic',
        'hadescendercyrillic', 'tsecyrillic', 'checyrillic',
        'chedescendercyrillic', 'shacyrillic', 'shchacyrillic',
        'hardsigncyrillic', 'yericyrillic', 'softsigncyrillic',
        'ereversedcyrillic', 'iucyrillic', 'iacyrillic', 'djecyrillic',
        'ecyrillic', 'dzecyrillic', 'icyrillic', 'ljecyrillic', 'njecyrillic',
        'tshecyrillic', 'dzhecyrillic', 'gheupturncyrillic',
        'ustraightstrokecyrillic')

TN_CYRILLICCOMPOSITES = ('IEgravecyrillic', 'Iocyrillic', 'Gjecyrillic',
        'Yicyrillic', 'Kjecyrillic', 'Igravecyrillic', 'Ushortcyrillic',
        'Iishortcyrillic', 'iishortcyrillic', 'iegravecyrillic', 'iocyrillic',
        'gjecyrillic', 'yicyrillic', 'kjecyrillic', 'igravecyrillic',
        'ushortcyrillic')

SS_CONTROLS = ('O', 'H', 'V', 'o', 'h', 'v')
SS_UC = TN_UC + TN_COMPOSITES_UC
SS_LC = TN_LC + TN_COMPOSITES_LC

SS_SC = []
for c in SS_UC:
    SS_SC.append(c+'.sc')

SS_SORTS_MC = ("period", "comma", "colon", "semicolon", "ellipsis",
        "exclamdown", "exclam", "exclamdbl", "questiondown", "question",
        "parenleft", "parenright", "bracketleft", "bracketright", "braceleft",
        "braceright", "hyphen", "underscore", "endash", "endash.salt_en",
        "emdash", "emdash.salt_em", "quoteleft", "quoteright", "quotedblleft",
        "quotedblright", "quotesinglbase", "quotedblbase", "guillemotleft",
        "guillemotright", "guilsinglleft", "guilsinglright", "brokenbar",
        "slash", "backslash", "bar", "asterisk", "dagger", "daggerdbl",
        "periodcentered", "bullet", "quotesingle", "quotedbl", "at",
        "registered", "copyright", "uni2117", "trademark", "apple")

SS_SORTS_UC = ("exclamdown.uc", "exclam.uc", "exclamdbl.uc", "questiondown.uc",
        "question.uc", "parenleft.uc", "parenright.uc", "bracketleft.uc",
        "bracketright.uc", "braceleft.uc", "braceright.uc", "hyphen.uc",
        "endash.uc", "endash.salt_en.uc", "emdash.uc", "emdash.salt_em.uc",
        "guillemotleft.uc", "guillemotright.uc", "guilsinglleft.uc",
        "guilsinglright.uc", "periodcentered.uc", "bullet.uc", "at.uc")

SS_SORTS_SC = ("exclamdown.sc", "exclam.sc", "exclamdbl.sc", "questiondown.sc",
        "question.sc", "parenleft.sc", "parenright.sc", "bracketleft.sc",
        "bracketright.sc", "braceleft.sc", "braceright.sc", "hyphen.sc",
        "endash.sc", "endash.salt_en.sc", "emdash.sc", "emdash.salt_em.sc",
        "quoteleft.sc", "quoteright.sc", "quotedblleft.sc", "quotedblright.sc",
        "quotesinglbase.sc", "quotedblbase.sc", "guillemotleft.sc",
        "guillemotright.sc", "guilsinglleft.sc", "guilsinglright.sc",
        "brokenbar.sc", "slash.sc", "backslash.sc", "bar.sc", "asterisk.sc",
        "dagger.sc", "daggerdbl.sc", "periodcentered.sc", "bullet.sc",
        "quotesingle.sc", "quotedbl.sc", "at.sc", "registered.sc",
        "copyright.sc", "uni2117.sc", "trademark.sc")

SS_FIGURES_MC = TN_FIGURES + ("plus", "minus", "multiply", "divide", "equal",
        "less", "greater", "dollar", "cent", "Euro", "sterling", "yen",
        "florin", "numbersign", "section", "paragraph", "percent",
        "perthousand", "degree", "minute", "second", "ordfeminine",
        "ordmasculine", "equivalent", )

SS_FIGURES_SC = []
SS_FIGURES_LC = []
SS_FIGURES_TAB = []

for c in SS_FIGURES_MC:
    SS_FIGURES_SC.append(c+'.sc')
    SS_FIGURES_LC.append(c+'.lc')
    SS_FIGURES_TAB.append(c+'.tab')

SS_FIGURESMATH = ("asciicircum", "asciitilde", "lessequal", "greaterequal",
        "plusminus", "approxequal", "notequal", "logicalnot", "radical",
        "infinity", "lozenge", "currency", "mu", "summation", "product", "pi",
        "integral", "Omega", "partialdiff", "Delta", "estimated", "checkmark")

SS_FIGURES_SUPSSINF = ("zero.sups", "one.sups", "two.sups", "three.sups",
        "four.sups", "five.sups", "six.sups", "seven.sups", "eight.sups",
        "nine.sups", "zero.sinf", "one.sinf", "two.sinf", "three.sinf",
        "four.sinf", "five.sinf", "six.sinf", "seven.sinf", "eight.sinf",
        "nine.sinf")

SS_FIGURES_FRACTION = ("fraction", "space.frac", "zero.numr", "one.numr",
        "two.numr", "three.numr", "four.numr", "five.numr", "six.numr",
        "seven.numr", "eight.numr", "nine.numr", "zero.dnom", "one.dnom",
        "two.dnom", "three.dnom", "four.dnom", "five.dnom", "six.dnom",
        "seven.dnom", "eight.dnom", "nine.dnom", "oneeighth", "onehalf",
        "onequarter", "seveneighths", "threeeighths", "threequarters",
        "fiveeighths",)

SS_SPACES = ("space", "space.en", "space.em", "space.thin", "space.hair")

SS_ALPHA_SUPS = ("a.sups", "b.sups", "c.sups", "d.sups", "e.sups",
        "egrave.sups", "f.sups", "g.sups", "h.sups", "i.sups", "j.sups",
        "k.sups", "l.sups", "m.sups", "n.sups", "o.sups", "p.sups", "q.sups",
        "r.sups", "s.sups", "t.sups", "u.sups", "v.sups", "w.sups", "x.sups",
        "y.sups", "z.sups")

SS_LIGATURES_DIPHTHONGS = TN_SECONDARY_LIGATURES + ('oe','OE','ae','AE')

SS_LIGATURES_DISCRETIONARY = ("w_w_w", "c_t", "s_t", "s_p") # c_k, s_k, c_h, s_h, c_p, s_p

SS_CURRENCY = ( "won", "sheqel", "peseta", "numero", "lira", "franc", "dong",
        "cruzeiro", "colonsign", "bahtthai", "rupeesignbengali",
        "rupeemarkbengali", "dollar", "cent", "Euro", "sterling", "kip",
        "turkishlira", "tugrik", "tenge", "sheqel", "scriptm", "rupee",
        "ruble", "rialarabic", "peso", "nordicmark", "naira", "mill", "manat",
        "livretournois", "indianrupee", "hryvnia", "guarani", "germanpenny",
        "dragma", "cedi", "austral", "armeniandram", "afghani",
        "gujaratirupee", "tamilrupee", 'khmer', 'ecu', "spesmilo",)

SS_CYRILLIC_UC = ("Abrevecyrillic", "Acyrillic", "Adieresiscyrillic",
        "Aiecyrillic", "Becyrillic", "Cheabkhasiancyrillic", "Checyrillic",
        "Chedescenderabkhasiancyrillic", "Chedescendercyrillic",
        "Chedieresiscyrillic", "Chekhakassiancyrillic",
        "Cheverticalstrokecyrillic", "Decyrillic", "Djecyrillic",
        "Dzeabkhasiancyrillic", "Dzecyrillic", "Dzhecyrillic", "Ecyrillic",
        "Efcyrillic", "Eiotifiedcyrillic", "Elcyrillic", "Emcyrillic",
        "Encyrillic", "Endescendercyrillic", "Enghecyrillic", "Enhookcyrillic",
        "Ercyrillic", "Ereversedcyrillic", "Escyrillic", "Esdescendercyrillic",
        "Fitacyrillic", "Gecyrillic", "Ghemiddlehookcyrillic",
        "Ghestrokecyrillic", "Gheupturncyrillic", "Gjecyrillic",
        "Haabkhasiancyrillic", "Hadescendercyrillic", "Hardsigncyrillic",
        "IAcyrillic", "IEgravecyrillic", "IUcyrillic", "Icyrillic",
        "Idieresiscyrillic", "Iebrevecyrillic", "Iecyrillic", "Igravecyrillic",
        "Iicyrillic", "Iishortcyrillic", "Imacroncyrillic", "Iocyrillic",
        "Izhitsacyrillic", "Izhitsadblgravecyrillic", "Jecyrillic",
        "Kabashkircyrillic", "Kacyrillic", "Kadescendercyrillic",
        "Kahookcyrillic", "Kastrokecyrillic", "Kaverticalstrokecyrillic",
        "Khacyrillic", "Kjecyrillic", "Koppacyrillic", "Ksicyrillic",
        "Ljecyrillic", "Njecyrillic", "Obarredcyrillic",
        "Obarreddieresiscyrillic", "Ocyrillic", "Odieresiscyrillic",
        "Omegacyrillic", "Omegaroundcyrillic", "Omegatitlocyrillic",
        "Otcyrillic", "Pecyrillic", "Pemiddlehookcyrillic", "Psicyrillic",
        "Schwacyrillic", "Schwadieresiscyrillic", "Shacyrillic",
        "Shchacyrillic", "Shhacyrillic", "Softsigncyrillic", "Tecyrillic",
        "Tedescendercyrillic", "Tetsecyrillic", "Tsecyrillic", "Tshecyrillic",
        "Ucyrillic", "Udieresiscyrillic", "Uhungarumlautcyrillic",
        "Ukcyrillic", "Umacroncyrillic", "Ushortcyrillic", "Ustraightcyrillic",
        "Ustraightstrokecyrillic", "Vecyrillic", "Yatcyrillic", "Yericyrillic",
        "Yerudieresiscyrillic", "Yicyrillic", "Yusbigcyrillic",
        "Yusbigiotifiedcyrillic", "Yuslittlecyrillic",
        "Yuslittleiotifiedcyrillic", "Zecyrillic", "Zedescendercyrillic",
        "Zedieresiscyrillic", "Zhebrevecyrillic", "Zhecyrillic",
        "Zhedescendercyrillic", "Zhedieresiscyrillic", )

    # Using brevecyrillic
SS_CYRILLIC_LC = ("abrevecyrillic", "acyrillic", "adieresiscyrillic",
        "aiecyrillic", "becyrillic", "cheabkhasiancyrillic", "checyrillic",
        "chedescenderabkhasiancyrillic", "chedescendercyrillic",
        "chedieresiscyrillic", "chekhakassiancyrillic",
        "cheverticalstrokecyrillic", "dasiapneumatacyrilliccmb", "decyrillic",
        "djecyrillic", "dzeabkhasiancyrillic", "dzecyrillic", "dzhecyrillic",
        "ecyrillic", "efcyrillic", "eiotifiedcyrillic", "elcyrillic",
        "emcyrillic", "encyrillic", "endescendercyrillic", "enghecyrillic",
        "enhookcyrillic", "ercyrillic", "ereversedcyrillic", "escyrillic",
        "esdescendercyrillic", "fitacyrillic", "gecyrillic",
        "ghemiddlehookcyrillic", "ghestrokecyrillic", "gheupturncyrillic",
        "gjecyrillic", "haabkhasiancyrillic", "hadescendercyrillic",
        "hardsigncyrillic", "iacyrillic", "icyrillic", "idieresiscyrillic",
        "iebrevecyrillic", "iecyrillic", "iegravecyrillic", "igravecyrillic",
        "iicyrillic", "iishortcyrillic", "imacroncyrillic", "iocyrillic",
        "iucyrillic", "izhitsacyrillic", "izhitsadblgravecyrillic",
        "jecyrillic", "kabashkircyrillic", "kacyrillic", "kadescendercyrillic",
        "kahookcyrillic", "kastrokecyrillic", "kaverticalstrokecyrillic",
        "khacyrillic", "kjecyrillic", "koppacyrillic", "ksicyrillic",
        "ljecyrillic", "njecyrillic", "obarredcyrillic",
        "obarreddieresiscyrillic", "ocyrillic", "odieresiscyrillic",
        "omegacyrillic", "omegaroundcyrillic", "omegatitlocyrillic",
        "otcyrillic", "palatalizationcyrilliccmb", "palochkacyrillic",
        "pecyrillic", "pemiddlehookcyrillic", "psicyrillic",
        "psilipneumatacyrilliccmb", "schwacyrillic", "schwadieresiscyrillic",
        "shacyrillic", "shchacyrillic", "shhacyrillic", "softsigncyrillic",
        "tecyrillic", "tedescendercyrillic", "tetsecyrillic",
        "thousandcyrillic", "titlocyrilliccmb", "tsecyrillic", "tshecyrillic",
        "ucyrillic", "udieresiscyrillic", "uhungarumlautcyrillic",
        "ukcyrillic", "umacroncyrillic", "ushortcyrillic", "ustraightcyrillic",
        "ustraightstrokecyrillic", "vecyrillic", "yatcyrillic", "yericyrillic",
        "yerudieresiscyrillic", "yicyrillic", "yusbigcyrillic",
        "yusbigiotifiedcyrillic", "yuslittlecyrillic",
        "yuslittleiotifiedcyrillic", "zecyrillic", "zedescendercyrillic",
        "zedieresiscyrillic", "zhebrevecyrillic", "zhecyrillic",
        "zhedescendercyrillic", "zhedieresiscyrillic")

SS_CYRILLIC = SS_CYRILLIC_UC + SS_CYRILLIC_LC

SS_GREEK_UC = ('Alpha', 'Alphatonos', 'Beta', 'Chi', 'Delta*', 'Epsilon',
        'Epsilontonos', 'Eta', 'Etatonos', 'Gamma', 'Iota', 'Iotadieresis',
        'Iotatonos', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Omega*', 'Omegatonos',
        'Omicron', 'Omicrontonos', 'Phi', 'Pi', 'Psi', 'Rho', 'Sigma', 'Tau',
        'Theta', 'Upsilon', 'Upsilondieresis', 'Upsilontonos', 'Xi', 'Zeta', )

SS_GREEK_LC = ('alpha', 'alphatonos', 'anoteleia', 'beta', 'chi', 'delta',
        'dieresistonos', 'epsilon', 'epsilontonos', 'eta', 'etatonos', 'gamma',
        'iota', 'iotadieresis', 'iotadieresistonos', 'iotatonos', 'kappa',
        'lambda', 'mu', 'nu', 'omega', 'omegatonos', 'omicron', 'omicrontonos',
        'phi', 'pi', 'psi', 'rho', 'sigma', 'sigma1', 'tau', 'theta', 'tonos',
        'upsilon', 'upsilondieresis', 'upsilondieresistonos', 'upsilontonos',
        'xi', 'zeta')

SS_GREEK = SS_GREEK_UC + SS_GREEK_LC

SS_ASCII = ("space", "exclam", "quotedbl", "numbersign", "dollar", "percent",
        "ampersand", "quotesingle", "parenleft", "parenright", "asterisk",
        "plus", "comma", "hyphen", "period", "slash", "zero", "one", "two",
        "three", "four", "five", "six", "seven", "eight", "nine", "colon",
        "semicolon", "less", "equal", "greater", "question", "at") + TN_UC + \
        ("bracketleft", "backslash", "bracketright", "asciicircum", "underscore",
        "grave") + TN_LC + ( "braceleft", "bar", "braceright", "asciitilde")

SS_BOXES = ( "block", "dbldnhorzbxd", "dbldnleftbxd", "dbldnrightbxd",
        "dblhorzbxd", "dbluphorzbxd", "dblupleftbxd", "dbluprightbxd",
        "dblvertbxd", "dblverthorzbxd", "dblvertleftbxd", "dblvertrightbxd",
        "dnblock", "dndblhorzsngbxd", "dndblleftsngbxd", "dndblrightsngbxd",
        "dneighthblock", "dnfiveeighthsblock", "dnhalfblock",
        "dnheavyhorzlightbxd", "dnheavyleftlightbxd", "dnheavyleftuplightbxd",
        "dnheavyrightlightbxd", "dnheavyrightuplightbxd",
        "dnheavyuphorzlightbxd", "dnlighthorzheavybxd", "dnlightleftheavybxd",
        "dnlightleftupheavybxd", "dnlightrightheavybxd",
        "dnlightrightupheavybxd", "dnlightuphorzheavybxd", "dnquarterblock",
        "dnseveneighthsblock", "dnsnghorzdblbxd", "dnsngleftdblbxd",
        "dnsngrightdblbxd", "dnthreeeighthsblock", "dnthreequartersblock",
        "fullblock", "heavydbldashhorzbxd", "heavydbldashvertbxd",
        "heavydnbxd", "heavydnhorzbxd", "heavydnleftbxd", "heavydnrightbxd",
        "heavyhorzbxd", "heavyleftbxd", "heavyleftlightrightbxd",
        "heavyquaddashhorzbxd", "heavyquaddashvertbxd", "heavyrightbxd",
        "heavytrpldashhorzbxd", "heavytrpldashvertbxd", "heavyupbxd",
        "heavyuphorzbxd", "heavyupleftbxd", "heavyuplightdnbxd",
        "heavyuprightbxd", "heavyvertbxd", "heavyverthorzbxd",
        "heavyvertleftbxd", "heavyvertrightbxd", "leftdnheavyrightuplightbxd",
        "lefteighthblock", "leftfiveeighthsblock", "lefthalfblock",
        "leftheavyrightdnlightbxd", "leftheavyrightuplightbxd",
        "leftheavyrightvertlightbxd", "leftlightrightdnheavybxd",
        "leftlightrightupheavybxd", "leftlightrightvertheavybxd",
        "leftquarterblock", "leftseveneighthsblock", "leftthreeeighthsblock",
        "leftthreequartersblock", "leftupheavyrightdnlightbxd", "lfblock",
        "lightarcdnleftbxd", "lightarcdnrightbxd", "lightarcupleftbxd",
        "lightarcuprightbxd", "lightdbldashhorzbxd", "lightdbldashvertbxd",
        "lightdiagcrossbxd", "lightdiagupleftdnrightbxd",
        "lightdiaguprightdnleftbxd", "lightdnbxd", "lightdnhorzbxd",
        "lightdnleftbxd", "lightdnrightbxd", "lighthorzbxd", "lightleftbxd",
        "lightleftheavyrightbxd", "lightquaddashhorzbxd",
        "lightquaddashvertbxd", "lightrightbxd", "lighttrpldashhorzbxd",
        "lighttrpldashvertbxd", "lightupbxd", "lightupheavydnbxd",
        "lightuphorzbxd", "lightupleftbxd", "lightuprightbxd", "lightvertbxd",
        "lightverthorzbxd", "lightvertleftbxd", "lightvertrightbxd",
        "rightdnheavyleftuplightbxd", "righteighthblock", "righthalfblock",
        "rightheavyleftdnlightbxd", "rightheavyleftuplightbxd",
        "rightheavyleftvertlightbxd", "rightlightleftdnheavybxd",
        "rightlightleftupheavybxd", "rightlightleftvertheavybxd",
        "rightupheavyleftdnlightbxd", "rtblock", "upblock", "updblhorzsngbxd",
        "updblleftsngbxd", "updblrightsngbxd", "upeighthblock", "uphalfblock",
        "upheavydnhorzlightbxd", "upheavyhorzlightbxd",
        "upheavyleftdnlightbxd", "upheavyleftlightbxd",
        "upheavyrightdnlightbxd", "upheavyrightlightbxd",
        "uplightdnhorzheavybxd", "uplighthorzheavybxd",
        "uplightleftdnheavybxd", "uplightleftheavybxd",
        "uplightrightdnheavybxd", "uplightrightheavybxd", "upsnghorzdblbxd",
        "upsngleftdblbxd", "upsngrightdblbxd", "vertdblhorzsngbxd",
        "vertdblleftsngbxd", "vertdblrightsngbxd", "vertheavyhorzlightbxd",
        "vertheavyleftlightbxd", "vertheavyrightlightbxd",
        "vertlighthorzheavybxd", "vertlightleftheavybxd",
        "vertlightrightheavybxd", "vertsnghorzdblbxd", "vertsngleftdblbxd",
        "vertsngrightdblbxd", "darkshade", "mediumshade", "orthogonal",
        "blackcircle",  "blackdownpointingtriangle", "blacksmallsquare",
        "blackuppointingtriangle",  "circle", )

SS_ARROWS = ("arrowboth", "arrowdown", "arrowup", "arrowleft", "arrowright",
        "arrowupdn",)

# Group sorting
SS_GROUP_SORTING = (
    set(SS_UC), set(SS_LC), set(SS_SC), set(SS_SORTS_MC), set(SS_SORTS_UC),
    set(SS_SORTS_SC), set(SS_FIGURES_MC), set(SS_FIGURES_SC),
    set(SS_FIGURES_LC), set(SS_FIGURES_TAB), set(SS_FIGURESMATH),
    set(SS_FIGURES_SUPSSINF), set(SS_FIGURES_FRACTION),
    set(SS_ACCENTSCMB.keys()), set(SS_SPACES), set(SS_ALPHA_SUPS),
    set(SS_LIGATURES_DIPHTHONGS), set(SS_LIGATURES_DISCRETIONARY),
    set(SS_ASCII), set(SS_CURRENCY), set(SS_CYRILLIC), set(SS_GREEK),
    set(SS_BOXES), set(SS_ARROWS),
)

CONNECTED_SCRIPTS = """/zero.sups/one.sups/two.sups/three.sups/four.sups/five.sups/six.sups/seven.sups/eight.sups/nine.sups/a.sups/b.sups/c.sups/d.sups/e.sups/egrave.sups/f.sups/g.sups/h.sups/i.sups/j.sups/k.sups/l.sups/m.sups/n.sups/o.sups/p.sups/q.sups/r.sups/s.sups/t.sups/u.sups/v.sups/w.sups/x.sups/y.sups/z.sups/zero.sinf/one.sinf/two.sinf/three.sinf/four.sinf/five.sinf/six.sinf/seven.sinf/eight.sinf/nine.sinf/a.sinf/b.sinf/c.sinf/d.sinf/e.sinf/egrave.sinf/f.sinf/g.sinf/h.sinf/i.sinf/j.sinf/k.sinf/l.sinf/m.sinf/n.sinf/o.sinf/p.sinf/q.sinf/r.sinf/s.sinf/t.sinf/u.sinf/v.sinf/w.sinf/x.sinf/y.sinf/z.sinf/zero.dnom/one.dnom/two.dnom/three.dnom/four.dnom/five.dnom/six.dnom/seven.dnom/eight.dnom/nine.dnom/zero.numr/one.numr/two.numr/three.numr/four.numr/five.numr/six.numr/seven.numr/eight.numr/nine.numr/percent/perthousand/onesuperior/twosuperior/threesuperior/onequarter/onehalf/threequarters/space/nbspace/A/A.alt1/A.alt2/Agrave/Aacute/Acircumflex/Atilde/Adieresis/Aring/Amacron/Abreve/Aogonek/Aringacute/B/B.alt1/B.alt2/C/C.alt1/C.alt2/Ccedilla/Cacute/Ccircumflex/Cdotaccent/Ccaron/D/D.alt1/D.alt2/Dcaron/E/E.alt1/E.alt2/Egrave/Eacute/Ecircumflex/Edieresis/Emacron/Ebreve/Edotaccent/Eogonek/Ecaron/F/F.alt1/F.alt2/G/G.alt1/G.alt2/Gcircumflex/Gbreve/Gdotaccent/Gcommaaccent/Gcaron/H/H.alt1/H.alt2/Hcircumflex/I/I.alt1/I.alt2/Igrave/Iacute/Icircumflex/Idieresis/Itilde/Imacron/Ibreve/Iogonek/Idotaccent/J/J.alt1/J.alt2/Jcircumflex/K/K.alt1/K.alt2/Kcommaaccent/L/L.alt1/L.alt2/Lacute/Lcommaaccent/Lcaron/M/M.alt1/M.alt2/N/N.alt1/N.alt2/Ntilde/Nacute/Ncommaaccent/Ncaron/O/O.alt1/O.alt2/Ograve/Oacute/Ocircumflex/Otilde/Odieresis/Omacron/Obreve/Ohungarumlaut/P/P.alt1/P.alt2/Q/Q.alt1/Q.alt2/R/R.alt1/R.alt2/Racute/Rcommaaccent/Rcaron/S/S.alt1/S.alt2/Sacute/Scircumflex/Scedilla/Scaron/Scommaaccent/T/T.alt1/T.alt2/Tcommaaccent/Tcaron/U/U.alt1/U.alt2/Ugrave/Uacute/Ucircumflex/Udieresis/Utilde/Umacron/Ubreve/Uring/Uhungarumlaut/Uogonek/V/V.alt1/V.alt2/W/W.alt1/W.alt2/Wcircumflex/Wgrave/Wacute/Wdieresis/X/X.alt1/X.alt2/Y/Y.alt1/Y.alt2/Yacute/Ycircumflex/Ydieresis/Ygrave/Z/Z.alt1/Z.alt2/Zacute/Zdotaccent/Zcaron/AE/AE.alt1/AE.alt2/AEacute/Eth/Oslash/Oslash.alt1/Oslash.alt2/Oslashacute/Thorn/Dcroat/Hbar/IJ/Ldot/Lslash/Eng/OE/OE.alt1/OE.alt2/Tbar/Omegatonos/Omegatonos.alt1/Omegatonos.alt2/Alpha/Alpha.alt1/Alpha.alt2/Alphatonos/Alphatonos.alt1/Alphatonos.alt2/Beta/Beta.alt1/Beta.alt2/Gamma/Gamma.alt1/Gamma.alt2/Delta/Delta.alt1/Delta.alt2/Epsilon/Epsilon.alt1/Epsilon.alt2/Epsilontonos/Epsilontonos.alt1/Epsilontonos.alt2/Zeta/Zeta.alt1/Zeta.alt2/Eta/Eta.alt1/Eta.alt2/Theta/Theta.alt1/Theta.alt2/Iota/Iota.alt1/Iota.alt2/Iotatonos/Iotatonos.alt1/Iotatonos.alt2/Iotadieresis/Iotadieresis.alt1/Iotadieresis.alt2/Kappa/Kappa.alt1/Kappa.alt2/Lambda/Lambda.alt1/Lambda.alt2/Mu/Mu.alt1/Mu.alt2/Nu/Nu.alt1/Nu.alt2/Xi/Xi.alt1/Xi.alt2/Omicron/Omicron.alt1/Omicron.alt2/Omicrontonos/Omicrontonos.alt1/Omicrontonos.alt2/Pi/Pi.alt1/Pi.alt2/Rho/Rho.alt1/Rho.alt2/Sigma/Sigma.alt1/Sigma.alt2/Tau/Tau.alt1/Tau.alt2/Upsilon/Upsilon.alt1/Upsilon.alt2/Upsilontonos/Upsilontonos.alt1/Upsilontonos.alt2/Upsilondieresis/Upsilondieresis.alt1/Upsilondieresis.alt2/Phi/Phi.alt1/Phi.alt2/Chi/Chi.alt1/Chi.alt2/Psi/Psi.alt1/Psi.alt2/Omega/Omega.alt1/Omega.alt2/Djecyrillic/Djecyrillic.alt1/Djecyrillic.alt2/Ecyrillic/Ecyrillic.alt1/Ecyrillic.alt2/Dzecyrillic/Dzecyrillic.alt1/Dzecyrillic.alt2/Icyrillic/Icyrillic.alt1/Icyrillic.alt2/Yicyrillic/Yicyrillic.alt1/Yicyrillic.alt2/Jecyrillic/Jecyrillic.alt1/Jecyrillic.alt2/Ljecyrillic/Ljecyrillic.alt1/Ljecyrillic.alt2/Njecyrillic/Njecyrillic.alt1/Njecyrillic.alt2/Tshecyrillic/Tshecyrillic.alt1/Tshecyrillic.alt2/Dzhecyrillic/Dzhecyrillic.alt1/Dzhecyrillic.alt2/Acyrillic/Acyrillic.alt1/Acyrillic.alt2/Becyrillic/Becyrillic.alt1/Becyrillic.alt2/Vecyrillic/Vecyrillic.alt1/Vecyrillic.alt2/Gecyrillic/Gecyrillic.alt1/Gecyrillic.alt2/Gjecyrillic/Gjecyrillic.alt1/Gjecyrillic.alt2/Decyrillic/Decyrillic.alt1/Decyrillic.alt2/Iecyrillic/Iecyrillic.alt1/Iecyrillic.alt2/IEgravecyrillic/IEgravecyrillic.alt1/IEgravecyrillic.alt2/Iocyrillic/Iocyrillic.alt1/Iocyrillic.alt2/Zhecyrillic/Zhecyrillic.alt1/Zhecyrillic.alt2/Zecyrillic/Zecyrillic.alt1/Zecyrillic.alt2/Iicyrillic/Iicyrillic.alt1/Iicyrillic.alt2/Igravecyrillic/Igravecyrillic.alt1/Igravecyrillic.alt2/Iishortcyrillic/Iishortcyrillic.alt1/Iishortcyrillic.alt2/Kacyrillic/Kacyrillic.alt1/Kacyrillic.alt2/Kjecyrillic/Kjecyrillic.alt1/Kjecyrillic.alt2/Elcyrillic/Elcyrillic.alt1/Elcyrillic.alt2/Emcyrillic/Emcyrillic.alt1/Emcyrillic.alt2/Encyrillic/Encyrillic.alt1/Encyrillic.alt2/Ocyrillic/Ocyrillic.alt1/Ocyrillic.alt2/Pecyrillic/Pecyrillic.alt1/Pecyrillic.alt2/Ercyrillic/Ercyrillic.alt1/Ercyrillic.alt2/Escyrillic/Escyrillic.alt1/Escyrillic.alt2/Tecyrillic/Tecyrillic.alt1/Tecyrillic.alt2/Ucyrillic/Ucyrillic.alt1/Ucyrillic.alt2/Ushortcyrillic/Ushortcyrillic.alt1/Ushortcyrillic.alt2/Efcyrillic/Efcyrillic.alt1/Efcyrillic.alt2/Khacyrillic/Khacyrillic.alt1/Khacyrillic.alt2/Tsecyrillic/Tsecyrillic.alt1/Tsecyrillic.alt2/Checyrillic/Checyrillic.alt1/Checyrillic.alt2/Shacyrillic/Shacyrillic.alt1/Shacyrillic.alt2/Shchacyrillic/Shchacyrillic.alt1/Shchacyrillic.alt2/Hardsigncyrillic/Hardsigncyrillic.alt1/Hardsigncyrillic.alt2/Yericyrillic/Yericyrillic.alt1/Yericyrillic.alt2/Softsigncyrillic/Softsigncyrillic.alt1/Softsigncyrillic.alt2/Ereversedcyrillic/Ereversedcyrillic.alt1/Ereversedcyrillic.alt2/IUcyrillic/IUcyrillic.alt1/IUcyrillic.alt2/IAcyrillic/IAcyrillic.alt1/IAcyrillic.alt2/Gheupturncyrillic/Gheupturncyrillic.alt1/Gheupturncyrillic.alt2/Zhedescendercyrillic/Zhedescendercyrillic.alt1/Zhedescendercyrillic.alt2/Kadescendercyrillic/Kadescendercyrillic.alt1/Kadescendercyrillic.alt2/Ustraightstrokecyrillic/Ustraightstrokecyrillic.alt1/Ustraightstrokecyrillic.alt2/Hadescendercyrillic/Hadescendercyrillic.alt1/Hadescendercyrillic.alt2/Chedescendercyrillic/Chedescendercyrillic.alt1/Chedescendercyrillic.alt2/a/a.alt1/a.alt2/agrave/aacute/acircumflex/atilde/adieresis/aring/amacron/abreve/aogonek/aringacute/b/b.alt1/b.alt2/c/c.alt1/c.alt2/ccedilla/cacute/ccircumflex/cdotaccent/ccaron/d/d.alt1/d.alt2/dcaron/e/e.alt1/e.alt2/egrave/eacute/ecircumflex/edieresis/emacron/ebreve/edotaccent/eogonek/ecaron/f/f.alt1/f.alt2/g/g.alt1/g.alt2/gcircumflex/gbreve/gdotaccent/gcommaaccent/gcaron/h/h.alt1/h.alt2/hcircumflex/i/i.alt1/i.alt2/igrave/iacute/icircumflex/idieresis/itilde/imacron/ibreve/iogonek/j/j.alt1/j.alt2/jcircumflex/k/k.alt1/k.alt2/kcommaaccent/l/l.alt1/l.alt2/lacute/lcommaaccent/lcaron/m/m.alt1/m.alt2/n/n.alt1/n.alt2/ntilde/nacute/ncommaaccent/ncaron/o/o.alt1/o.alt2/ograve/oacute/ocircumflex/otilde/odieresis/omacron/obreve/ohungarumlaut/p/p.alt1/p.alt2/q/q.alt1/q.alt2/r/r.alt1/r.alt2/racute/rcommaaccent/rcaron/s/s.alt1/s.alt2/sacute/scircumflex/scedilla/scaron/scommaaccent/t/t.alt1/t.alt2/tcedilla/tcaron/tcommaaccent/u/u.alt1/u.alt2/ugrave/uacute/ucircumflex/udieresis/utilde/umacron/ubreve/uring/uhungarumlaut/uogonek/v/v.alt1/v.alt2/w/w.alt1/w.alt2/wcircumflex/wgrave/wacute/wdieresis/x/x.alt1/x.alt2/y/y.alt1/y.alt2/yacute/ydieresis/ycircumflex/ygrave/z/z.alt1/z.alt2/zacute/zdotaccent/zcaron/germandbls/ae/aeacute/eth/oslash/oslashacute/thorn/dcroat/hbar/dotlessi/dotlessi.alt1/dotlessi.alt2/ij/ldot/lslash/eng/oe/tbar/dotlessj/schwa/alpha/alpha.alt1/alpha.alt2/alphatonos/alphatonos.alt1/alphatonos.alt2/beta/beta.alt1/beta.alt2/gamma/gamma.alt1/gamma.alt2/delta/delta.alt1/delta.alt2/epsilon/epsilon.alt1/epsilon.alt2/epsilontonos/epsilontonos.alt1/epsilontonos.alt2/zeta/zeta.alt1/zeta.alt2/eta/eta.alt1/eta.alt2/etatonos/etatonos.alt1/etatonos.alt2/theta/theta.alt1/theta.alt2/iota/iota.alt1/iota.alt2/iotadieresistonos/iotadieresistonos.alt1/iotadieresistonos.alt2/iotatonos/iotatonos.alt1/iotatonos.alt2/iotadieresis/iotadieresis.alt1/iotadieresis.alt2/kappa/kappa.alt1/kappa.alt2/lambda/lambda.alt1/lambda.alt2/mu/nu/nu.alt1/nu.alt2/xi/xi.alt1/xi.alt2/omicron/omicron.alt1/omicron.alt2/omicrontonos/omicrontonos.alt1/omicrontonos.alt2/pi/pi.alt1/pi.alt2/rho/rho.alt1/rho.alt2/sigma1/sigma1.alt1/sigma1.alt2/sigma/sigma.alt1/sigma.alt2/tau/tau.alt1/tau.alt2/upsilon/upsilon.alt1/upsilon.alt2/upsilondieresistonos/upsilondieresistonos.alt1/upsilondieresistonos.alt2/upsilondieresis/upsilondieresis.alt1/upsilondieresis.alt2/upsilontonos/upsilontonos.alt1/upsilontonos.alt2/phi/phi.alt1/phi.alt2/chi/chi.alt1/chi.alt2/psi/psi.alt1/psi.alt2/omega/omega.alt1/omega.alt2/omegatonos/omegatonos.alt1/omegatonos.alt2/acyrillic/acyrillic.alt1/acyrillic.alt2/becyrillic/becyrillic.alt1/becyrillic.alt2/vecyrillic/vecyrillic.alt1/vecyrillic.alt2/gecyrillic/gecyrillic.alt1/gecyrillic.alt2/gjecyrillic/gjecyrillic.alt1/gjecyrillic.alt2/decyrillic/decyrillic.alt1/decyrillic.alt2/iecyrillic/iecyrillic.alt1/iecyrillic.alt2/iegravecyrillic/iegravecyrillic.alt1/iegravecyrillic.alt2/iocyrillic/iocyrillic.alt1/iocyrillic.alt2/zhecyrillic/zhecyrillic.alt1/zhecyrillic.alt2/zecyrillic/zecyrillic.alt1/zecyrillic.alt2/iicyrillic/iicyrillic.alt1/iicyrillic.alt2/iishortcyrillic/iishortcyrillic.alt1/iishortcyrillic.alt2/igravecyrillic/igravecyrillic.alt1/igravecyrillic.alt2/kacyrillic/kacyrillic.alt1/kacyrillic.alt2/kjecyrillic/kjecyrillic.alt1/kjecyrillic.alt2/elcyrillic/elcyrillic.alt1/elcyrillic.alt2/emcyrillic/emcyrillic.alt1/emcyrillic.alt2/encyrillic/encyrillic.alt1/encyrillic.alt2/ocyrillic/ocyrillic.alt1/ocyrillic.alt2/pecyrillic/pecyrillic.alt1/pecyrillic.alt2/ercyrillic/ercyrillic.alt1/ercyrillic.alt2/escyrillic/escyrillic.alt1/escyrillic.alt2/tecyrillic/tecyrillic.alt1/tecyrillic.alt2/ucyrillic/ucyrillic.alt1/ucyrillic.alt2/ushortcyrillic/ushortcyrillic.alt1/ushortcyrillic.alt2/efcyrillic/efcyrillic.alt1/efcyrillic.alt2/khacyrillic/khacyrillic.alt1/khacyrillic.alt2/tsecyrillic/tsecyrillic.alt1/tsecyrillic.alt2/checyrillic/checyrillic.alt1/checyrillic.alt2/shacyrillic/shacyrillic.alt1/shacyrillic.alt2/shchacyrillic/shchacyrillic.alt1/shchacyrillic.alt2/hardsigncyrillic/hardsigncyrillic.alt1/hardsigncyrillic.alt2/yericyrillic/yericyrillic.alt1/yericyrillic.alt2/softsigncyrillic/softsigncyrillic.alt1/softsigncyrillic.alt2/ereversedcyrillic/ereversedcyrillic.alt1/ereversedcyrillic.alt2/iucyrillic/iucyrillic.alt1/iucyrillic.alt2/iacyrillic/iacyrillic.alt1/iacyrillic.alt2/djecyrillic/djecyrillic.alt1/djecyrillic.alt2/ecyrillic/ecyrillic.alt1/ecyrillic.alt2/dzecyrillic/dzecyrillic.alt1/dzecyrillic.alt2/icyrillic/icyrillic.alt1/icyrillic.alt2/yicyrillic/yicyrillic.alt1/yicyrillic.alt2/jecyrillic/jecyrillic.alt1/jecyrillic.alt2/ljecyrillic/ljecyrillic.alt1/ljecyrillic.alt2/njecyrillic/njecyrillic.alt1/njecyrillic.alt2/tshecyrillic/tshecyrillic.alt1/tshecyrillic.alt2/dzhecyrillic/dzhecyrillic.alt1/dzhecyrillic.alt2/gheupturncyrillic/gheupturncyrillic.alt1/gheupturncyrillic.alt2/zhedescendercyrillic/zhedescendercyrillic.alt1/zhedescendercyrillic.alt2/kadescendercyrillic/kadescendercyrillic.alt1/kadescendercyrillic.alt2/ustraightstrokecyrillic/ustraightstrokecyrillic.alt1/ustraightstrokecyrillic.alt2/hadescendercyrillic/hadescendercyrillic.alt1/hadescendercyrillic.alt2/chedescendercyrillic/chedescendercyrillic.alt1/chedescendercyrillic.alt2/ordfeminine/ordmasculine/zero/zero.alt1/zero.alt2/one/one.alt1/one.alt2/two/two.alt1/two.alt2/three/three.alt1/three.alt2/four/four.alt1/four.alt2/five/five.alt1/five.alt2/six/six.alt1/six.alt2/seven/seven.alt1/seven.alt2/eight/eight.alt1/eight.alt2/nine/nine.alt1/nine.alt2/onesuperior/twosuperior/threesuperior/onequarter/onehalf/threequarters/underscore/hyphen/endash/emdash/horizontalbar/parenleft/parenright/bracketleft/bracketright/braceleft/braceright/numbersign/percent/perthousand/quotesingle/quotedbl/quoteleft/quoteright/quotedblleft/quotedblright/quotesinglbase/quotedblbase/guilsinglleft/guilsinglright/guillemotleft/guillemotright/asterisk/dagger/daggerdbl/period/period.alt1/period.alt2/comma/comma.alt1/comma.alt2/colon/colon.alt1/colon.alt2/semicolon/semicolon.alt1/semicolon.alt2/ellipsis/exclam/exclam.alt1/exclam.alt2/exclamdown/question/question.alt1/question.alt2/questiondown/slash/backslash/fraction/bar/brokenbar/at/ampersand/section/paragraph/periodcentered/bullet/minute/second/plus/minus/plusminus/divide/multiply/equal/less/greater/lessequal/greaterequal/approxequal/notequal/logicalnot/partialdiff/product/summation/radical/infinity/integral/dollar/dollar.alt1/dollar.alt2/cent/sterling/currency/yen/yen.alt1/yen.alt2/Euro/Euro.alt1/Euro.alt2/florin/asciicircum/asciitilde/acute/grave/hungarumlaut/circumflex/caron/breve/tilde/macron/dieresis/dotaccent/ring/cedilla/ogonek/copyright/registered/trademark/degree/lozenge/checkmark/commaaccent/Tcedilla/apple/bitcoin/copyrightsound/idotaccent/sfthyphen/fi/fl/space.em/space.en/space.frac/space.thin/parenleft.uc/parenright.uc/bracketleft.uc/bracketright.uc/braceleft.uc/braceright.uc/guilsinglleft.uc/guilsinglright.uc/guillemotleft.uc/guillemotright.uc/exclamdown.uc/questiondown.uc/J.base/Jcircumflex.base/J.base_sc/Jcircumflex.base_sc/i.trk/A.sc/A.sc.alt1/A.sc.alt2/Agrave.sc/Aacute.sc/Acircumflex.sc/Atilde.sc/Adieresis.sc/Aring.sc/Amacron.sc/Abreve.sc/Aogonek.sc/Aringacute.sc/B.sc/B.sc.alt1/B.sc.alt2/C.sc/C.sc.alt1/C.sc.alt2/Ccedilla.sc/Cacute.sc/Ccircumflex.sc/Cdotaccent.sc/Ccaron.sc/D.sc/D.sc.alt1/D.sc.alt2/Dcaron.sc/E.sc/E.sc.alt1/E.sc.alt2/Egrave.sc/Eacute.sc/Ecircumflex.sc/Edieresis.sc/Emacron.sc/Ebreve.sc/Edotaccent.sc/Eogonek.sc/Ecaron.sc/F.sc/F.sc.alt1/F.sc.alt2/G.sc/G.sc.alt1/G.sc.alt2/Gcircumflex.sc/Gbreve.sc/Gdotaccent.sc/Gcommaaccent.sc/Gcaron.sc/H.sc/H.sc.alt1/H.sc.alt2/Hcircumflex.sc/I.sc/I.sc.alt1/I.sc.alt2/Igrave.sc/Iacute.sc/Icircumflex.sc/Idieresis.sc/Itilde.sc/Imacron.sc/Ibreve.sc/Iogonek.sc/Idotaccent.sc/J.sc/J.sc.alt1/J.sc.alt2/Jcircumflex.sc/K.sc/K.sc.alt1/K.sc.alt2/Kcommaaccent.sc/L.sc/L.sc.alt1/L.sc.alt2/Lacute.sc/Lcommaaccent.sc/Lcaron.sc/M.sc/M.sc.alt1/M.sc.alt2/N.sc/N.sc.alt1/N.sc.alt2/Ntilde.sc/Nacute.sc/Ncommaaccent.sc/Ncaron.sc/O.sc/O.sc.alt1/O.sc.alt2/Ograve.sc/Oacute.sc/Ocircumflex.sc/Otilde.sc/Odieresis.sc/Omacron.sc/Obreve.sc/Ohungarumlaut.sc/P.sc/P.sc.alt1/P.sc.alt2/Q.sc/Q.sc.alt1/Q.sc.alt2/R.sc/R.sc.alt1/R.sc.alt2/Racute.sc/Rcommaaccent.sc/Rcaron.sc/S.sc/S.sc.alt1/S.sc.alt2/Sacute.sc/Scircumflex.sc/Scedilla.sc/Scaron.sc/Scommaaccent.sc/T.sc/T.sc.alt1/T.sc.alt2/Tcommaaccent.sc/Tcaron.sc/U.sc/U.sc.alt1/U.sc.alt2/Ugrave.sc/Uacute.sc/Ucircumflex.sc/Udieresis.sc/Utilde.sc/Umacron.sc/Ubreve.sc/Uring.sc/Uhungarumlaut.sc/Uogonek.sc/V.sc/V.sc.alt1/V.sc.alt2/W.sc/W.sc.alt1/W.sc.alt2/Wcircumflex.sc/Wgrave.sc/Wacute.sc/Wdieresis.sc/X.sc/X.sc.alt1/X.sc.alt2/Y.sc/Y.sc.alt1/Y.sc.alt2/Yacute.sc/Ycircumflex.sc/Ydieresis.sc/Ygrave.sc/Z.sc/Z.sc.alt1/Z.sc.alt2/Zacute.sc/Zdotaccent.sc/Zcaron.sc/AE.sc/AE.sc.alt1/AE.sc.alt2/AEacute.sc/Eth.sc/Oslash.sc/Oslash.sc.alt1/Oslash.sc.alt2/Oslashacute.sc/Thorn.sc/Dcroat.sc/Hbar.sc/Ldot.sc/Lslash.sc/Eng.sc/OE.sc/OE.sc.alt1/OE.sc.alt2/Tbar.sc/germandbls.sc/zero.sc/one.sc/two.sc/three.sc/four.sc/five.sc/six.sc/seven.sc/eight.sc/nine.sc/parenleft.sc/parenright.sc/bracketleft.sc/bracketright.sc/braceleft.sc/braceright.sc/exclam.sc/exclamdown.sc/question.sc/questiondown.sc/numbersign.sc/ampersand.sc/section.sc/paragraph.sc/slash.sc/backslash.sc/dollar.sc/cent.sc/sterling.sc/yen.sc/Euro.sc/florin.sc/degree.sc/Tcedilla.sc/bitcoin.sc/ordfeminine.lc/ordmasculine.lc/zero.lc/one.lc/two.lc/three.lc/four.lc/five.lc/six.lc/seven.lc/eight.lc/nine.lc/guilsinglleft.lc/guilsinglright.lc/guillemotleft.lc/guillemotright.lc/numbersign.lc/percent.lc/perthousand.lc/section.lc/paragraph.lc/minute.lc/second.lc/plus.lc/minus.lc/plusminus.lc/divide.lc/multiply.lc/equal.lc/less.lc/greater.lc/lessequal.lc/greaterequal.lc/approxequal.lc/notequal.lc/logicalnot.lc/dollar.lc/sterling.lc/yen.lc/Euro.lc/florin.lc/degree.lc/bitcoin.lc/A.ct0/b/A.ct0/b.alt1/A.ct0/b.alt2/A.ct0/h/A.ct0/h.alt1/A.ct0/h.alt2/A.ct0/i/A.ct0/i.alt1/A.ct0/i.alt2/A.ct0/j/A.ct0/j.alt1/A.ct0/j.alt2/A.ct0/k/A.ct0/k.alt1/A.ct0/k.alt2/A.ct0/l/A.ct0/l.alt1/A.ct0/l.alt2/A.ct0/m/A.ct0/m.alt1/A.ct0/m.alt2/A.ct0/n/A.ct0/n.alt1/A.ct0/n.alt2/A.ct0/p/A.ct0/p.alt1/A.ct0/p.alt2/A.ct0/r/A.ct0/r.alt1/A.ct0/r.alt2/A.ct0/u/A.ct0/u.alt1/A.ct0/u.alt2/A.ct0/v/A.ct0/v.alt1/A.ct0/v.alt2/A.ct0/w/A.ct0/w.alt1/A.ct0/w.alt2/A.ct0/x/A.ct0/x.alt1/A.ct0/x.alt2/A.ct0/y/A.ct0/y.alt1/A.ct0/y.alt2/A.ct0/z/A.ct0/z.alt1/A.ct0/z.alt2/A.ct1/b/A.ct1/b.alt1/A.ct1/b.alt2/A.ct1/h/A.ct1/h.alt1/A.ct1/h.alt2/A.ct1/i/A.ct1/i.alt1/A.ct1/i.alt2/A.ct1/j/A.ct1/j.alt1/A.ct1/j.alt2/A.ct1/k/A.ct1/k.alt1/A.ct1/k.alt2/A.ct1/l/A.ct1/l.alt1/A.ct1/l.alt2/A.ct1/m/A.ct1/m.alt1/A.ct1/m.alt2/A.ct1/n/A.ct1/n.alt1/A.ct1/n.alt2/A.ct1/p/A.ct1/p.alt1/A.ct1/p.alt2/A.ct1/r/A.ct1/r.alt1/A.ct1/r.alt2/A.ct1/u/A.ct1/u.alt1/A.ct1/u.alt2/A.ct1/v/A.ct1/v.alt1/A.ct1/v.alt2/A.ct1/w/A.ct1/w.alt1/A.ct1/w.alt2/A.ct1/x/A.ct1/x.alt1/A.ct1/x.alt2/A.ct1/y/A.ct1/y.alt1/A.ct1/y.alt2/A.ct1/z/A.ct1/z.alt1/A.ct1/z.alt2/A.ct2/b/A.ct2/b.alt1/A.ct2/b.alt2/A.ct2/h/A.ct2/h.alt1/A.ct2/h.alt2/A.ct2/i/A.ct2/i.alt1/A.ct2/i.alt2/A.ct2/j/A.ct2/j.alt1/A.ct2/j.alt2/A.ct2/k/A.ct2/k.alt1/A.ct2/k.alt2/A.ct2/l/A.ct2/l.alt1/A.ct2/l.alt2/A.ct2/m/A.ct2/m.alt1/A.ct2/m.alt2/A.ct2/n/A.ct2/n.alt1/A.ct2/n.alt2/A.ct2/p/A.ct2/p.alt1/A.ct2/p.alt2/A.ct2/r/A.ct2/r.alt1/A.ct2/r.alt2/A.ct2/u/A.ct2/u.alt1/A.ct2/u.alt2/A.ct2/v/A.ct2/v.alt1/A.ct2/v.alt2/A.ct2/w/A.ct2/w.alt1/A.ct2/w.alt2/A.ct2/x/A.ct2/x.alt1/A.ct2/x.alt2/A.ct2/y/A.ct2/y.alt1/A.ct2/y.alt2/A.ct2/z/A.ct2/z.alt1/A.ct2/z.alt2/A.cm0/a/A.cm0/a.alt1/A.cm0/a.alt2/A.cm0/c/A.cm0/c.alt1/A.cm0/c.alt2/A.cm0/d/A.cm0/d.alt1/A.cm0/d.alt2/A.cm0/e/A.cm0/e.alt1/A.cm0/e.alt2/A.cm0/g/A.cm0/g.alt1/A.cm0/g.alt2/A.cm0/o/A.cm0/o.alt1/A.cm0/o.alt2/A.cm0/q/A.cm0/q.alt1/A.cm0/q.alt2/A.cm1/a/A.cm1/a.alt1/A.cm1/a.alt2/A.cm1/c/A.cm1/c.alt1/A.cm1/c.alt2/A.cm1/d/A.cm1/d.alt1/A.cm1/d.alt2/A.cm1/e/A.cm1/e.alt1/A.cm1/e.alt2/A.cm1/g/A.cm1/g.alt1/A.cm1/g.alt2/A.cm1/o/A.cm1/o.alt1/A.cm1/o.alt2/A.cm1/q/A.cm1/q.alt1/A.cm1/q.alt2/A.cm2/a/A.cm2/a.alt1/A.cm2/a.alt2/A.cm2/c/A.cm2/c.alt1/A.cm2/c.alt2/A.cm2/d/A.cm2/d.alt1/A.cm2/d.alt2/A.cm2/e/A.cm2/e.alt1/A.cm2/e.alt2/A.cm2/g/A.cm2/g.alt1/A.cm2/g.alt2/A.cm2/o/A.cm2/o.alt1/A.cm2/o.alt2/A.cm2/q/A.cm2/q.alt1/A.cm2/q.alt2/A.ct0/n/A.ct0/i/A.ct0/u/A.ct1/n/A.ct1/i/A.ct1/u/A.ct2/n/A.ct2/i/A.ct2/u/A.cm0/e/A.cm0/a/A.cm0/o/A.cm1/e/A.cm1/a/A.cm1/o/A.cm2/e/A.cm2/a/A.cm2/o/C.ct0/n/C.ct0/i/C.ct0/u/C.ct1/n/C.ct1/i/C.ct1/u/C.ct2/n/C.ct2/i/C.ct2/u/C.cm0/e/C.cm0/a/C.cm0/o/C.cm1/e/C.cm1/a/C.cm1/o/C.cm2/e/C.cm2/a/C.cm2/o/D.ct0/n/D.ct0/i/D.ct0/u/D.ct1/n/D.ct1/i/D.ct1/u/D.ct2/n/D.ct2/i/D.ct2/u/D.cm0/e/D.cm0/a/D.cm0/o/D.cm1/e/D.cm1/a/D.cm1/o/D.cm2/e/D.cm2/a/D.cm2/o/E.ct0/n/E.ct0/i/E.ct0/u/E.ct1/n/E.ct1/i/E.ct1/u/E.ct2/n/E.ct2/i/E.ct2/u/E.cm0/e/E.cm0/a/E.cm0/o/E.cm1/e/E.cm1/a/E.cm1/o/E.cm2/e/E.cm2/a/E.cm2/o/G.ct0/n/G.ct0/i/G.ct0/u/G.ct1/n/G.ct1/i/G.ct1/u/G.ct2/n/G.ct2/i/G.ct2/u/G.cm0/e/G.cm0/a/G.cm0/o/G.cm1/e/G.cm1/a/G.cm1/o/G.cm2/e/G.cm2/a/G.cm2/o/H.ct0/n/H.ct0/i/H.ct0/u/H.ct1/n/H.ct1/i/H.ct1/u/H.ct2/n/H.ct2/i/H.ct2/u/H.cm0/e/H.cm0/a/H.cm0/o/H.cm1/e/H.cm1/a/H.cm1/o/H.cm2/e/H.cm2/a/H.cm2/o/I.ct0/n/I.ct0/i/I.ct0/u/I.ct1/n/I.ct1/i/I.ct1/u/I.ct2/n/I.ct2/i/I.ct2/u/I.cm0/e/I.cm0/a/I.cm0/o/I.cm1/e/I.cm1/a/I.cm1/o/I.cm2/e/I.cm2/a/I.cm2/o/K.ct0/n/K.ct0/i/K.ct0/u/K.ct1/n/K.ct1/i/K.ct1/u/K.ct2/n/K.ct2/i/K.ct2/u/K.cm0/e/K.cm0/a/K.cm0/o/K.cm1/e/K.cm1/a/K.cm1/o/K.cm2/e/K.cm2/a/K.cm2/o/L.ct0/n/L.ct0/i/L.ct0/u/L.ct1/n/L.ct1/i/L.ct1/u/L.ct2/n/L.ct2/i/L.ct2/u/L.cm0/e/L.cm0/a/L.cm0/o/L.cm1/e/L.cm1/a/L.cm1/o/L.cm2/e/L.cm2/a/L.cm2/o/M.ct0/n/M.ct0/i/M.ct0/u/M.ct1/n/M.ct1/i/M.ct1/u/M.ct2/n/M.ct2/i/M.ct2/u/M.cm0/e/M.cm0/a/M.cm0/o/M.cm1/e/M.cm1/a/M.cm1/o/M.cm2/e/M.cm2/a/M.cm2/o/R.ct0/n/R.ct0/i/R.ct0/u/R.ct1/n/R.ct1/i/R.ct1/u/R.ct2/n/R.ct2/i/R.ct2/u/R.cm0/e/R.cm0/a/R.cm0/o/R.cm1/e/R.cm1/a/R.cm1/o/R.cm2/e/R.cm2/a/R.cm2/o/S.ct0/n/S.ct0/i/S.ct0/u/S.ct1/n/S.ct1/i/S.ct1/u/S.ct2/n/S.ct2/i/S.ct2/u/S.cm0/e/S.cm0/a/S.cm0/o/S.cm1/e/S.cm1/a/S.cm1/o/S.cm2/e/S.cm2/a/S.cm2/o/X.ct0/n/X.ct0/i/X.ct0/u/X.ct1/n/X.ct1/i/X.ct1/u/X.ct2/n/X.ct2/i/X.ct2/u/X.cm0/e/X.cm0/a/X.cm0/o/X.cm1/e/X.cm1/a/X.cm1/o/X.cm2/e/X.cm2/a/X.cm2/o/Z.ct0/n/Z.ct0/i/Z.ct0/u/Z.ct1/n/Z.ct1/i/Z.ct1/u/Z.ct2/n/Z.ct2/i/Z.ct2/u/Z.cm0/e/Z.cm0/a/Z.cm0/o/Z.cm1/e/Z.cm1/a/Z.cm1/o/Z.cm2/e/Z.cm2/a/Z.cm2/o/a.ct0/n/a.ct0/i/a.ct0/u/a.ct1/n/a.ct1/i/a.ct1/u/a.ct2/n/a.ct2/i/a.ct2/u/a.cm0/e/a.cm0/a/a.cm0/o/a.cm1/e/a.cm1/a/a.cm1/o/a.cm2/e/a.cm2/a/a.cm2/o/c.ct0/n/c.ct0/i/c.ct0/u/c.ct1/n/c.ct1/i/c.ct1/u/c.ct2/n/c.ct2/i/c.ct2/u/c.cm0/e/c.cm0/a/c.cm0/o/c.cm1/e/c.cm1/a/c.cm1/o/c.cm2/e/c.cm2/a/c.cm2/o/d.ct0/n/d.ct0/i/d.ct0/u/d.ct1/n/d.ct1/i/d.ct1/u/d.ct2/n/d.ct2/i/d.ct2/u/d.cm0/e/d.cm0/a/d.cm0/o/d.cm1/e/d.cm1/a/d.cm1/o/d.cm2/e/d.cm2/a/d.cm2/o/e.ct0/n/e.ct0/i/e.ct0/u/e.ct1/n/e.ct1/i/e.ct1/u/e.ct2/n/e.ct2/i/e.ct2/u/e.cm0/e/e.cm0/a/e.cm0/o/e.cm1/e/e.cm1/a/e.cm1/o/e.cm2/e/e.cm2/a/e.cm2/o/e.cm0b/e/e.cm0b/a/e.cm0b/o/e.cm1b/e/e.cm1b/a/e.cm1b/o/e.cm2b/e/e.cm2b/a/e.cm2b/o/e.ct0b/n/e.ct0b/i/e.ct0b/u/e.ct1b/n/e.ct1b/i/e.ct1b/u/e.ct2b/n/e.ct2b/i/e.ct2b/u/f.ct0/n/f.ct0/i/f.ct0/u/f.ct1/n/f.ct1/i/f.ct1/u/f.ct2/n/f.ct2/i/f.ct2/u/f.cm0/e/f.cm0/a/f.cm0/o/f.cm1/e/f.cm1/a/f.cm1/o/f.cm2/e/f.cm2/a/f.cm2/o/h.ct0/n/h.ct0/i/h.ct0/u/h.ct1/n/h.ct1/i/h.ct1/u/h.ct2/n/h.ct2/i/h.ct2/u/h.cm0/e/h.cm0/a/h.cm0/o/h.cm1/e/h.cm1/a/h.cm1/o/h.cm2/e/h.cm2/a/h.cm2/o/i.ct0/n/i.ct0/i/i.ct0/u/i.ct1/n/i.ct1/i/i.ct1/u/i.ct2/n/i.ct2/i/i.ct2/u/i.cm0/e/i.cm0/a/i.cm0/o/i.cm1/e/i.cm1/a/i.cm1/o/i.cm2/e/i.cm2/a/i.cm2/o/k.ct0/n/k.ct0/i/k.ct0/u/k.ct1/n/k.ct1/i/k.ct1/u/k.ct2/n/k.ct2/i/k.ct2/u/k.cm0/e/k.cm0/a/k.cm0/o/k.cm1/e/k.cm1/a/k.cm1/o/k.cm2/e/k.cm2/a/k.cm2/o/l.ct0/n/l.ct0/i/l.ct0/u/l.ct1/n/l.ct1/i/l.ct1/u/l.ct2/n/l.ct2/i/l.ct2/u/l.cm0/e/l.cm0/a/l.cm0/o/l.cm1/e/l.cm1/a/l.cm1/o/l.cm2/e/l.cm2/a/l.cm2/o/m.ct0/n/m.ct0/i/m.ct0/u/m.ct1/n/m.ct1/i/m.ct1/u/m.ct2/n/m.ct2/i/m.ct2/u/m.cm0/e/m.cm0/a/m.cm0/o/m.cm1/e/m.cm1/a/m.cm1/o/m.cm2/e/m.cm2/a/m.cm2/o/n.ct0/n/n.ct0/i/n.ct0/u/n.ct1/n/n.ct1/i/n.ct1/u/n.ct2/n/n.ct2/i/n.ct2/u/n.cm0/e/n.cm0/a/n.cm0/o/n.cm1/e/n.cm1/a/n.cm1/o/n.cm2/e/n.cm2/a/n.cm2/o/o.ct0/n/o.ct0/i/o.ct0/u/o.ct1/n/o.ct1/i/o.ct1/u/o.ct2/n/o.ct2/i/o.ct2/u/o.cm0/e/o.cm0/a/o.cm0/o/o.cm1/e/o.cm1/a/o.cm1/o/o.cm2/e/o.cm2/a/o.cm2/o/r.ct0/n/r.ct0/i/r.ct0/u/r.ct1/n/r.ct1/i/r.ct1/u/r.ct2/n/r.ct2/i/r.ct2/u/r.cm0/e/r.cm0/a/r.cm0/o/r.cm1/e/r.cm1/a/r.cm1/o/r.cm2/e/r.cm2/a/r.cm2/o/s.ct0/n/s.ct0/i/s.ct0/u/s.ct1/n/s.ct1/i/s.ct1/u/s.ct2/n/s.ct2/i/s.ct2/u/s.cm0/e/s.cm0/a/s.cm0/o/s.cm1/e/s.cm1/a/s.cm1/o/s.cm2/e/s.cm2/a/s.cm2/o/t.ct0/n/t.ct0/i/t.ct0/u/t.ct1/n/t.ct1/i/t.ct1/u/t.ct2/n/t.ct2/i/t.ct2/u/t.cm0/e/t.cm0/a/t.cm0/o/t.cm1/e/t.cm1/a/t.cm1/o/t.cm2/e/t.cm2/a/t.cm2/o/u.ct0/n/u.ct0/i/u.ct0/u/u.ct1/n/u.ct1/i/u.ct1/u/u.ct2/n/u.ct2/i/u.ct2/u/u.cm0/e/u.cm0/a/u.cm0/o/u.cm1/e/u.cm1/a/u.cm1/o/u.cm2/e/u.cm2/a/u.cm2/o/v.ct0/n/v.ct0/i/v.ct0/u/v.ct1/n/v.ct1/i/v.ct1/u/v.ct2/n/v.ct2/i/v.ct2/u/v.cm0/e/v.cm0/a/v.cm0/o/v.cm1/e/v.cm1/a/v.cm1/o/v.cm2/e/v.cm2/a/v.cm2/o/w.ct0/n/w.ct0/i/w.ct0/u/w.ct1/n/w.ct1/i/w.ct1/u/w.ct2/n/w.ct2/i/w.ct2/u/w.cm0/e/w.cm0/a/w.cm0/o/w.cm1/e/w.cm1/a/w.cm1/o/w.cm2/e/w.cm2/a/w.cm2/o/x.ct0/n/x.ct0/i/x.ct0/u/x.ct1/n/x.ct1/i/x.ct1/u/x.ct2/n/x.ct2/i/x.ct2/u/x.cm0/e/x.cm0/a/x.cm0/o/x.cm1/e/x.cm1/a/x.cm1/o/x.cm2/e/x.cm2/a/x.cm2/o/y.ct0/n/y.ct0/i/y.ct0/u/y.ct1/n/y.ct1/i/y.ct1/u/y.ct2/n/y.ct2/i/y.ct2/u/z.ct0/n/z.ct0/i/z.ct0/u/z.ct1/n/z.ct1/i/z.ct1/u/z.ct2/n/z.ct2/i/z.ct2/u/z.cm0/e/z.cm0/a/z.cm0/o/z.cm1/e/z.cm1/a/z.cm1/o/z.cm2/e/z.cm2/a/z.cm2/o/dotlessi.ct0/n/dotlessi.ct0/i/dotlessi.ct0/u/dotlessi.ct1/n/dotlessi.ct1/i/dotlessi.ct1/u/dotlessi.ct2/n/dotlessi.ct2/i/dotlessi.ct2/u/dotlessi.cm0/e/dotlessi.cm0/a/dotlessi.cm0/o/dotlessi.cm1/e/dotlessi.cm1/a/dotlessi.cm1/o/dotlessi.cm2/e/dotlessi.cm2/a/dotlessi.cm2/o"""

# Dynamic fractions and compare with composite percent and perthousand and
# standard fractions.
FRACTIONS = ['/onequarter','/onehalf','/threequarters', '/percent',
    '/perthousand', '/one.numr', '/fraction', '/two.dnom', '/one.numr',
    '/fraction', '/two.dnom', '/three.numr', '/fraction', '/four.dnom',
    '/zero.numr', '/fraction', '/zero.dnom', '/zero.numr', '/fraction',
    '/zero.dnom', '/zero.dnom',]

FRACTIONS = ''.join(FRACTIONS)

figures = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
        'eight', 'nine')

for i1 in figures:
    for i2 in figures:
         # Escape slash to differentiate from /glyphname.
         FRACTIONS += '/space/two.numr/fraction/%s.dnom/%s.dnom' % (i1, i2)

for i1 in figures:
    for i2 in figures:
         # Escape slash to differentiate from /glyphname.
         FRACTIONS += '/space/%s.numr/%s.numr/fraction/two.dnom' % (i1, i2)

# Used for ordering of master->instance in spacing groups. Used by Builder and
# TextCenter.

SPACE_LC = ('n', 'o', 'v', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z')
SPACE_UC = ('H', 'O', 'V', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K',
        'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z')
SPACE_SC = []
for c in SPACE_UC:
    SPACE_SC.append(c+'sc')

# Superior and inferior samples
SUPERIORS_PAGE = ''

for c in SS_ALPHA_SUPS:
    c = c.split('.')[0]
    SUPERIORS_PAGE += '/i.sups/%s.sups' % c

for c in SS_ALPHA_SUPS:
    c = c.split('.')[0]
    SUPERIORS_PAGE += '/i.sinf/%s.sinf' % c

i = 0

for ext in ('sinf', 'sups'):
    for gName in SPACE_UC + SPACE_LC:
        for f in figures:
            SUPERIORS_PAGE += '/%s/%s.%s/ ' % (gName, f, ext)
        f = figures[i]
        for c in SS_ALPHA_SUPS:
            c = c.split('.')[0]
            SUPERIORS_PAGE += '/%s/%s.%s/%s.%s/ ' % (gName, c, ext, f, ext)
    i += 1

    if i >= len(figures):
        i = 0

# Space categories are used by the profile builders, to make sure that only
# glyphs inside a group get compared. This way we avoid that "A" and "/" are
# joining the same space group accidentally.

SPACE_CATEGORIES = {
    'capHeight': set(SPACE_UC + TN_SECONDARY_UC + TN_COMPOSITES_UC + SS_GREEK_UC + SS_CYRILLIC_UC),
    'scapHeight': set(SPACE_SC + TN_SECONDARY_SC + TN_COMPOSITES_SC + TN_COMPOSITES_LCSC),
    'xHeight': set(SPACE_LC + TN_SECONDARY_LC + TN_COMPOSITES_LC + TN_SECONDARY_LIGATURES + SS_GREEK_LC + SS_CYRILLIC_LC),
    'textElements': set(TN_SCALARPOLATES + SS_FIGURES_MC + TN_CURRENCY),
}

SPACE_SAMPLES = (
    SPACE_UC + TN_SECONDARY_UC + TN_COMPOSITES_UC,
    SPACE_SC + TN_SECONDARY_SC + TN_COMPOSITES_SC,
    SPACE_LC + TN_SECONDARY_LC + TN_COMPOSITES_LC,
    TN_SCALARPOLATES
)

SPACE_MASTERS = (SPACE_UC, SPACE_LC, TN_SECONDARY_UC, TN_COMPOSITES_UC, SPACE_LC, TN_SECONDARY_LC, TN_COMPOSITES_LC,
    TN_SCALARPOLATES)

SMARTSETDATA = [
    # === External
    #('Ascii', None, None),
    #('Adobe Latin-1', None, None),
    #('MS WGL4'),

    # === Custom
    #('Base on standards', None, None),
    #('Other', None, None),

    # === Internal
    # Process subset
    ('TN Process', (
        ('Primary Controls', None, TN_CONTROLS),
        ('Primary', None, TN_PRIMARY),
        ('Secondary', None, TN_SECONDARY),
        ('Scalarpolates', None, TN_SCALARPOLATES),
        ('Composites', None, TN_COMPOSITES),
        ('Combinates', None, TN_COMBINATES),
        ('Greek Primary Controls', None, TN_GREEKPRIMARYCONTROLS),
        ('Greek Primary', None, TN_GREEKPRIMARY),
        ('Greek Composites', None,TN_GREEKCOMPOSITES),
        ('Greek Combinates', None, TN_GREEKCOMBINATES),
        ('Cyrillic Primary Controls', None, TN_CYRILLICPRIMARYCONTROLS),
        ('Cyrillic Primary', None, TN_CYRILLICPRIMARY),
        ('Cyrillic Composites', None, TN_CYRILLICCOMPOSITES),
    )),
    ('Process', (
        ('Controls', None, SS_CONTROLS),
        ('Empty', """Contours == 0 AND Components == 0""", None),
        ('Not empty', """Contours > 0 Or Components > 0""", None),
        ('Only components', """Contours == 0 AND Components > 0""", None),
        ('No components', """Contours > 0 AND Components == 0""", None),
        #('Side bearings', None, None),
        #('Alignment type'),
        ('Capitals', None, SS_UC),
        ('Lower case', None, SS_LC),
        ('All figures', """Name BEGINSWITH "zero" OR Name BEGINSWITH "one" OR Name BEGINSWITH "two" OR
                       Name BEGINSWITH "three" OR Name BEGINSWITH "four" OR Name BEGINSWITH "five" OR
                       Name BEGINSWITH "six" OR Name BEGINSWITH "seven" OR Name BEGINSWITH "eight" OR
                       Name BEGINSWITH "nine" """, None),
        #('Style features', None, None),
        #('Occupational feature groups', None, None),
        ('Base "cmb" accents', None, SS_ACCENTSCMB.keys()),
        ('Small caps', 'Name ENDSWITH ".sc"', None),
    )),
    # === Flight path (glyph sets)
    ('Flight path', (
        ('ASCII', None, SS_ASCII),
        ('Latin 1', None, getUnicodeNames('Latin 1')),
        ('Latin TN Extended', None, getUnicodeNames('Latin FB Extended')),
        ('OGL', None, getUnicodeNames('OGL')),
        ('MS WGL4', None, getUnicodeNames('WGL')),
        ('Mac OS Roman', None, getUnicodeNames('Mac Roman'))
    )),
    # === Unicode ranges
    ('Unicode ranges', (
        ('Basic Latin', "Unicode > -1 AND Unicode < 127", None),
        ('Latin 1 Supplement', "Unicode > 127 AND Unicode < 255", None),
        ('Latin Extended-A', "Unicode > 255 AND Unicode < 383", None),
        ('Latin Extended-B', "Unicode > 383 AND Unicode < 591", None),
        ('IPA Extensions', "Unicode > 591 AND Unicode < 687", None),
        ('Phonetic Extensions', "Unicode > 7423 AND Unicode < 7551", None),
        ('Phonetic Extensions Supplement', "Unicode > 7551 AND Unicode < 7615", None),
        ('Spacing Modifier Letters', "Unicode > 687 AND Unicode < 767", None),
        ('Modifier Tone Letters', "Unicode > 42751 AND Unicode < 42783", None),
        ('Combining Diacritical Marks', "Unicode > 767 AND Unicode < 879", None),
        ('Combining Diacritical Marks Supplement', "Unicode > 7615 AND Unicode < 7679", None),
    )),
    # === Scripts
    ('Scripts', (
        ('Greek and Coptic', "Unicode > 879 AND Unicode < 1023", None),
        ('Coptic', "Unicode > 11391 AND Unicode < 11519", None),
        ('Cyrillic', "Unicode > 1023 AND Unicode < 1279", None),
        ('Cyrillic Supplement', "Unicode > 1279 AND Unicode < 1327", None),
        ('Cyrillic Extended-A', "Unicode > 11743 AND Unicode < 11775", None),
        ('Cyrillic Extended-B', "Unicode > 42559 AND Unicode < 42655", None),
        ('Armenian', "Unicode > 1327 AND Unicode < 1423", None),
        ('Hebrew', "Unicode > 1423 AND Unicode < 1535", None),
        ('Vai', "Unicode > 42239 AND Unicode < 42559", None),
        ('Arabic', "Unicode > 1535 AND Unicode < 1791", None),
        ('Arabic Supplement', "Unicode > 1871 AND Unicode < 1919", None),
        ('NKo', "Unicode > 1983 AND Unicode < 2047", None),
        ('Devanagari', "Unicode > 2303 AND Unicode < 2431", None),
        ('Bengali', "Unicode > 2431 AND Unicode < 2559", None),
        ('Gurmukhi', "Unicode > 2559 AND Unicode < 2687", None),
        ('Gujarati', "Unicode > 2687 AND Unicode < 2815", None),
        ('Oriya', "Unicode > 2815 AND Unicode < 2943", None),
        ('Tamil', "Unicode > 2943 AND Unicode < 3071", None),
        ('Telugu', "Unicode > 3071 AND Unicode < 3199", None),
        ('Kannada', "Unicode > 3199 AND Unicode < 3327", None),
        ('Malayalam', "Unicode > 3327 AND Unicode < 3455", None),
        ('Thai', "Unicode > 3583 AND Unicode < 3711", None),
        ('Lao', "Unicode > 3711 AND Unicode < 3839", None),
        ('Georgian', "Unicode > 4255 AND Unicode < 4351", None),
        ('Georgian Supplement', "Unicode > 11519 AND Unicode < 11567", None),
        ('Balinese', "Unicode > 6911 AND Unicode < 7039", None),
        ('Hangul Jamo', "Unicode > 4351 AND Unicode < 4607", None),
        ('Latin Extended Additional', "Unicode > 7679 AND Unicode < 7935", None),
        ('Latin Extended-C', "Unicode > 11359 AND Unicode < 11391", None),
        ('Latin Extended-D', "Unicode > 42783 AND Unicode < 43007", None),
        ('Greek Extended', "Unicode > 7935 AND Unicode < 8191", None),
        ('General Punctuation', "Unicode > 8191 AND Unicode < 8303", None),
        ('Supplemental Punctuation', "Unicode > 11775 AND Unicode < 11903", None),
        ('Superscripts And Subscripts', "Unicode > 8303 AND Unicode < 8351", None),
        ('Currency Symbols', "Unicode > 8351 AND Unicode < 8399", None),
        ('Combining Diacritical Marks For Symbols', "Unicode > 8399 AND Unicode < 8447", None),
        ('Letterlike Symbols', "Unicode > 8447 AND Unicode < 8527", None),
        ('Number Forms', "Unicode > 8527 AND Unicode < 8591", None),
        ('Arrows', "Unicode > 8591 AND Unicode < 8703", None),
        ('Supplemental Arrows-A', "Unicode > 10223 AND Unicode < 10239", None),
        ('Supplemental Arrows-B', "Unicode > 10495 AND Unicode < 10623", None),
        ('Miscellaneous Symbols and Arrows', "Unicode > 11007 AND Unicode < 11263", None),
        ('Mathematical Operators', "Unicode > 8703 AND Unicode < 8959", None),
        ('Supplemental Mathematical Operators', "Unicode > 10751 AND Unicode < 11007", None),
        ('Miscellaneous Mathematical Symbols-A', "Unicode > 10175 AND Unicode < 10223", None),
        ('Miscellaneous Mathematical Symbols-B', "Unicode > 10623 AND Unicode < 10751", None),
        ('Miscellaneous Technical', "Unicode > 8959 AND Unicode < 9215", None),
        ('Control Pictures', "Unicode > 9215 AND Unicode < 9279", None),
        ('Optical Character Recognition', "Unicode > 9279 AND Unicode < 9311", None),
        ('Enclosed Alphanumerics', "Unicode > 9311 AND Unicode < 9471", None),
        ('Box Drawing', "Unicode > 9471 AND Unicode < 9599", None),
        ('Block Elements', "Unicode > 9599 AND Unicode < 9631", None),
        ('Geometric Shapes', "Unicode > 9631 AND Unicode < 9727", None),
        ('Miscellaneous Symbols', "Unicode > 9727 AND Unicode < 9983", None),
        ('Dingbats', "Unicode > 9983 AND Unicode < 10175", None),
        ('CJK Symbols And Punctuation', "Unicode > 12287 AND Unicode < 12351", None),
        ('Hiragana', "Unicode > 12351 AND Unicode < 12447", None),
        ('Katakana', "Unicode > 12447 AND Unicode < 12543", None),
        ('Katakana Phonetic Extensions', "Unicode > 12783 AND Unicode < 12799", None),
        ('Bopomofo', "Unicode > 12543 AND Unicode < 12591", None),
        ('Bopomofo Extended', "Unicode > 12703 AND Unicode < 12735", None),
        ('Hangul Compatibility Jamo', "Unicode > 12591 AND Unicode < 12687", None),
        ('Phags-pa', "Unicode > 43071 AND Unicode < 43135", None),
        ('Enclosed CJK Letters And Months', "Unicode > 12799 AND Unicode < 13055", None),
        ('CJK Compatibility', "Unicode > 13055 AND Unicode < 13311", None),
        ('Hangul Syllables', "Unicode > 44031 AND Unicode < 55215", None),
        ('Non-Plane 0 *', "Unicode > 55295 AND Unicode < 57343", None),
        ('Phoenician', "Unicode > 67839 AND Unicode < 67871", None),
        ('CJK Unified Ideographs', "Unicode > 19967 AND Unicode < 40959", None),
        ('CJK Radicals Supplement', "Unicode > 11903 AND Unicode < 12031", None),
        ('Kangxi Radicals', "Unicode > 12031 AND Unicode < 12255", None),
        ('Ideographic Description Characters', "Unicode > 12271 AND Unicode < 12287", None),
        ('CJK Unified Ideographs Extension A', "Unicode > 13311 AND Unicode < 19903", None),
        ('CJK Unified Ideographs Extension B', "Unicode > 131071 AND Unicode < 173791", None),
        ('Kanbun', "Unicode > 12687 AND Unicode < 12703", None),
        ('Private Use Area ((plane 0)', "Unicode > 57343 AND Unicode < 63743", None),
        ('CJK Strokes', "Unicode > 12735 AND Unicode < 12783", None),
        ('CJK Compatibility Ideographs', "Unicode > 63743 AND Unicode < 64255", None),
        ('CJK Compatibility Ideographs Supplement', "Unicode > 194559 AND Unicode < 195103", None),
        ('Alphabetic Presentation Forms', "Unicode > 64255 AND Unicode < 64335", None),
        ('Arabic Presentation Forms-A', "Unicode > 64335 AND Unicode < 65023", None),
        ('Combining Half Marks', "Unicode > 65055 AND Unicode < 65071", None),
        ('Vertical Forms', "Unicode > 65039 AND Unicode < 65055", None),
        ('CJK Compatibility Forms', "Unicode > 65071 AND Unicode < 65103", None),
        ('Small Form Variants', "Unicode > 65103 AND Unicode < 65135", None),
        ('Arabic Presentation Forms-B', "Unicode > 65135 AND Unicode < 65279", None),
        ('Halfwidth And Fullwidth Forms', "Unicode > 65279 AND Unicode < 65519", None),
        ('Specials', "Unicode > 65519 AND Unicode < 65535", None),
        ('Tibetan', "Unicode > 3839 AND Unicode < 4095", None),
        ('Syriac', "Unicode > 1791 AND Unicode < 1871", None),
        ('Thaana', "Unicode > 1919 AND Unicode < 1983", None),
        ('Sinhala', "Unicode > 3455 AND Unicode < 3583", None),
        ('Myanmar', "Unicode > 4095 AND Unicode < 4255", None),
        ('Ethiopic', "Unicode > 4607 AND Unicode < 4991", None),
        ('Ethiopic Supplement', "Unicode > 4991 AND Unicode < 5023", None),
        ('Ethiopic Extended', "Unicode > 11647 AND Unicode < 11743", None),
        ('Cherokee', "Unicode > 5023 AND Unicode < 5119", None),
        ('Unified Canadian Aboriginal Syllabics', "Unicode > 5119 AND Unicode < 5759", None),
        ('Ogham', "Unicode > 5759 AND Unicode < 5791", None),
        ('Runic', "Unicode > 5791 AND Unicode < 5887", None),
        ('Khmer', "Unicode > 6015 AND Unicode < 6143", None),
        ('Khmer Symbols', "Unicode > 6623 AND Unicode < 6655", None),
        ('Mongolian', "Unicode > 6143 AND Unicode < 6319", None),
        ('Braille Patterns', "Unicode > 10239 AND Unicode < 10495", None),
        ('Yi Syllables', "Unicode > 40959 AND Unicode < 42127", None),
        ('Yi Radicals', "Unicode > 42127 AND Unicode < 42191", None),
        ('Tagalog', "Unicode > 5887 AND Unicode < 5919", None),
        ('Hanunoo', "Unicode > 5919 AND Unicode < 5951", None),
        ('Buhid', "Unicode > 5951 AND Unicode < 5983", None),
        ('Tagbanwa', "Unicode > 5983 AND Unicode < 6015", None),
        ('Old Italic', "Unicode > 66303 AND Unicode < 66351", None),
        ('Gothic', "Unicode > 66351 AND Unicode < 66383", None),
        ('Deseret', "Unicode > 66559 AND Unicode < 66639", None),
        ('Byzantine Musical Symbols', "Unicode > 118783 AND Unicode < 119039", None),
        ('Musical Symbols', "Unicode > 119039 AND Unicode < 119295", None),
        ('Ancient Greek Musical Notation', "Unicode > 119295 AND Unicode < 119375", None),
        ('Mathematical Alphanumeric Symbols', "Unicode > 119807 AND Unicode < 120831", None),
        ('Private Use (plane 15)', "Unicode > 1044479 AND Unicode < 1048573", None),
        ('Private Use (plane 16)', "Unicode > 1048575 AND Unicode < 1114109", None),
        ('Variation Selectors', "Unicode > 65023 AND Unicode < 65039", None),
        ('Variation Selectors Supplement', "Unicode > 917759 AND Unicode < 917999", None),
        ('Tags', "Unicode > 917503 AND Unicode < 917631", None),
        ('Limbu', "Unicode > 6399 AND Unicode < 6479", None),
        ('Tai Le', "Unicode > 6479 AND Unicode < 6527", None),
        ('New Tai Lue', "Unicode > 6527 AND Unicode < 6623", None),
        ('Buginese', "Unicode > 6655 AND Unicode < 6687", None),
        ('Glagolitic', "Unicode > 11263 AND Unicode < 11359", None),
        ('Tifinagh', "Unicode > 11567 AND Unicode < 11647", None),
        ('Yijing Hexagram Symbols', "Unicode > 19903 AND Unicode < 19967", None),
        ('Syloti Nagri', "Unicode > 43007 AND Unicode < 43055", None),
        ('Linear B Syllabary', "Unicode > 65535 AND Unicode < 65663", None),
        ('Linear B Ideograms', "Unicode > 65663 AND Unicode < 65791", None),
        ('Aegean Numbers', "Unicode > 65791 AND Unicode < 65855", None),
        ('Ancient Greek Numbers', "Unicode > 65855 AND Unicode < 65935", None),
        ('Ugaritic', "Unicode > 66431 AND Unicode < 66463", None),
        ('Old Persian', "Unicode > 66463 AND Unicode < 66527", None),
        ('Shavian', "Unicode > 66639 AND Unicode < 66687", None),
        ('Osmanya', "Unicode > 66687 AND Unicode < 66735", None),
        ('Cypriot Syllabary', "Unicode > 67583 AND Unicode < 67647", None),
        ('Kharoshthi', "Unicode > 68095 AND Unicode < 68191", None),
        ('Tai Xuan Jing Symbols', "Unicode > 119551 AND Unicode < 119647", None),
        ('Cuneiform', "Unicode > 73727 AND Unicode < 74751", None),
        ('Cuneiform Numbers and Punctuation', "Unicode > 74751 AND Unicode < 74879", None),
        ('Counting Rod Numerals', "Unicode > 119647 AND Unicode < 119679", None),
        ('Sundanese', "Unicode > 7039 AND Unicode < 7103", None),
        ('Lepcha', "Unicode > 7167 AND Unicode < 7247", None),
        ('Ol Chiki', "Unicode > 7247 AND Unicode < 7295", None),
        ('Saurashtra', "Unicode > 43135 AND Unicode < 43231", None),
        ('Kayah Li', "Unicode > 43263 AND Unicode < 43311", None),
        ('Rejang', "Unicode > 43311 AND Unicode < 43359", None),
        ('Cham', "Unicode > 43519 AND Unicode < 43615", None),
        ('Ancient Symbols', "Unicode > 65935 AND Unicode < 65999", None),
        ('Phaistos Disc', "Unicode > 65999 AND Unicode < 66047", None),
        ('Carian', "Unicode > 66207 AND Unicode < 66271", None),
        ('Lycian', "Unicode > 66175 AND Unicode < 66207", None),
        ('Lydian', "Unicode > 67871 AND Unicode < 67903", None),
        ('Domino Tiles', "Unicode > 127023 AND Unicode < 127135", None),
        ('Mahjong Tiles', "Unicode > 126975 AND Unicode < 127023", None),
    )),
    # === Languages

    # === Features
    ('Features', (
        ('Alpha Latin UC', None, SS_UC),
        ('Alpha Latin LC', None, SS_LC),
        ('Alpha Latin SC', None, SS_SC),
        ('Sorts MC', None, SS_SORTS_MC),
        ('Sorts UC', None, SS_SORTS_UC),
        ('Sorts SC', None, SS_SORTS_SC),
        ('Figures MC', None, SS_FIGURES_MC),
        ('Figures SC', None, SS_FIGURES_SC),
        ('Figures LC', None, SS_FIGURES_LC),
        ('Figures MC Tab', None, SS_FIGURES_TAB),
        ('Figures Adv Math MC', None, SS_FIGURESMATH),
        ('Figures sups/sinf', None, SS_FIGURES_SUPSSINF),
        ('Figures fraction', None, SS_FIGURES_FRACTION),
        ('Diacritics MC', None, SS_ACCENTSCMB.keys()),
        ('Spaces', None, SS_SPACES),
        ('Alpha sups', None, SS_ALPHA_SUPS),
        ('Ligatures/diphthongs', None, SS_LIGATURES_DIPHTHONGS),
        ('Discretionary Ligatures', None, SS_LIGATURES_DISCRETIONARY)
    )),

    # === Misc
    ('Misc', (
        ('Currency', None, SS_CURRENCY),
        ('Boxes', None, SS_BOXES),
        ('Arrows', None, SS_ARROWS),
    )),
]
