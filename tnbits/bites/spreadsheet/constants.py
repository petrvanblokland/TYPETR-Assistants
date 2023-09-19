
# Glyph set presets.

BASE_LC = 'l n o p v'
LC = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
LC_PLUS = 'ae oe germandbls ampersand ij eng thorn mu pi'
LC_SLASH = 'oslash hbar tbar lslash dcroat slash backslash fraction'
BASE_UC = 'H O V'
UC = LC.upper()
UC_PLUS = 'AE OE IJ Eng Thorn'
UC_SLASH = 'Oslash Hbar Tbar Lslash Dcroat slash backslash fraction'
BASE_SC = 'H.sc O.sc V.sc'
SC = 'A.sc B.sc C.sc D.sc E.sc F.sc G.sc H.sc I.sc J.sc K.sc L.sc M.sc N.sc \
O.sc P.sc Q.sc R.sc S.sc T.sc U.sc V.sc W.sc X.sc Y.sc Z.sc'
SC_SLASH = 'Oslash.sc Hbar.sc Tbar.sc slash backslash fraction'
SC_PLUS = 'AE.sc OE.sc IJ.sc Thorn.sc'
LIGATURES = 'f_i f_l f_f f_j f_t f_b f_h f_f_i f_f_l'
FIGURES = 'zero one two three four five six seven eight nine'
SUPERIORS = '0.sup 1.sup 2.sup 3.sup 4.sup 5.sup 6.sup 7.sup 8.sup 9.sup \
ordfeminine ordmasculin percent perthousand'
INFERIORS = '0.inf 1.inf 2.inf 3.inf 4.inf 5.inf 6.inf 7.inf 8.inf 9.inf \
percent perthousand'
PUNCTUATIONS = 'period comma colon semicolon bullet periodcentered ellipsis'
MATH = 'minus plus plusminus equal notequal less greater greaterequal lessequal \
multiply product divide partialdiff radical approxequal Delta infinity'
CURRENCY = 'dollar yen Euro lira sterling cent currency florin percent \
numbersign estimated'
QUOTES = 'quotesingle quotedbl guillemotleft guillemotright quotedblleft \
quotedblright quoteleft quoteright quotesinglbase quotedblbase'
DIACRITICS = 'dotlessi dotlessj acutecmb gravecmb dieresiscmb circumflexcmb \
tildecmb asciitilde brevecmb dotaccentcmb ringcmb cedillacmb hungarumlautcmb \
ogonekcmb caroncmb macroncmb'
DIACRITICS_UC = 'A* B* C* D* E* F* G* H* I* J* K* L* M* N* O* P* Q* R* S* T* U* \
V* W* Y* Z*'
DIACRITICS_LC = 'a* b* c* d* e* f* g* h* i* j* k* l* m* n* o* p* q* r* s* t* u* \
*v *w *x* y* z*'
DIACRITICS_SC = 'A*.sc B*.sc C*.sc D*.sc E*.sc F*.sc G*.sc H*.sc I*.sc J*.sc \
K*.sc L*.sc M*.sc N*.sc O*.sc P*.sc Q*.sc R*.sc S*.sc T*.sc U*.sc V*.sc W*.sc \
X*.sc Y*.sc Z*.sc'
MARKS = 'at copyright registered trademark numbersign exclam exclamdown \
question questiondown asterisk section paragraph'
FRACTIONS = 'fraction onequarter onehalf threequarters percent perthousand'
BARS = 'Hbar Tbar hbar tbar hyphen sfthyphen.endash emdash underscore bar \
brokenbar macroncmb minus plus plusminus equal notequal logicalnot divide \
dagger daggerdbl'
ROUNDS = 'C G O Oslash Q S C.sc G.sc O.sc Oslash.sc Q.sc S.sc o zero zero.sup \
zero.inf ring degree ordmasculin'
BRACKETS = 'braceleft braceright bracketleft bracketright parenleft parenright'
GREEK_BASE_LC = 'alpha beta mu o'
GREEK_LC = 'alpha beta epsilon eta zeta gamma theta iota kappa lambda mu nu xi \
o rho sigma upsilon chi psi omega'
DIACRITICS_GREEK_LC = 'alpha* beta* epsilon* eta* zeta* gamma* theta* iota* \
kappa* lambda* mu* nu* xi* o* rho* sigma* upsilon* chi* psi* omega*'
GREEK_BASE_UC = 'A B E O P T Y Z'
GREEK_UC = 'A B E Eta I K Lambda M N Xi O P Theta Pi Z Sigma T Y Psi Omega'
DIACRITICS_GREEK_UC = 'A* B* E* Eta* I* K* Lambda* M* N* Xi* O* P* Theta* Pi* \
Z* Sigma* T* Y* Psi* Omega*'

PRESETS_SOURCE = (
    ('base (lower case)', BASE_LC),
    ('base (upper case)', BASE_UC),
    ('a-z', LC),
    ('a-z+',  LC_PLUS + ' ' + LC),
    ('A-Z', UC),
    ('A-Z+',  UC_PLUS + ' ' + UC),
    ('slashed', LC_SLASH + ' ' + UC_SLASH),
    ('punctuation', PUNCTUATIONS),
    ('diacritics', DIACRITICS),
    ('diacritics (lower case)', DIACRITICS_LC),
    ('diacritics (upper case)', DIACRITICS_UC),
    ('diacritics (small caps)', DIACRITICS_SC),
    ('quotes', QUOTES),
    ('bars', BARS),
    ('currency', CURRENCY),
    ('marks', MARKS),
    ('rounds', ROUNDS),
    ('ligatures', LIGATURES),
    ('brackets', BRACKETS),
    ('figures', FIGURES),
    ('fractions', FRACTIONS),
    ('superiors', SUPERIORS),
    ('inferiors', INFERIORS),
    ('all', None),
)

PRESETS_ORDER = []
PRESETS = {}

for key, value in PRESETS_SOURCE:
    PRESETS[key] = value
    PRESETS_ORDER.append(key)

STYLES_HEADERS = ('Glyphs', 'Units Per Em', 'Ascender', 'Descender', 'Cap Height', \
        'Smallcap Height', 'X Height', 'Italic Angle')

GLYPHS_HEADERS = ('GlyphName', 'Contours', 'Components', 'Width', 'LSB', 'RSB', \
        'Points', 'Y Min', 'Y Max', 'Stems', 'Bars', 'R-Bars', 'Diagonals')
