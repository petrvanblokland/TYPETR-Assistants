# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   smartset.py
#
from tnbits.constants import Constants as C

#   A N C H O R S
#
# Standard anchor names

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

ANCHORS = set((ANCHOR_CENTERABOVE, ANCHOR_CENTERBELOW, ANCHOR_RIGHTABOVE, ANCHOR_RIGHTBELOW,
    ANCHOR_LEFTABOVE, ANCHOR_LEFTBELOW, ANCHOR_TOP, ANCHOR_MIDDLE, ANCHOR_BOTTOM, ANCHOR_ORIGINX, ANCHOR_ORIGINY))

ULCWORDS = (
    'Aardvark Ablution Acrimonious Adventures Aeolian Africa Agamemnon Ahoy Aileron Ajax Akimbo Altruism America Anecdote Aorta Aptitude Aquarium Arcade Aspartame Attrition Aurelius Avuncular Awning Axminster Ayers Azure',
    'Banishment Benighted Bhagavad Biblical Bjorn Blancmange Bolton Brusque Burnish Bwana Byzantium',
    'Cabbala Cetacean Charlemagne Cicero Clamorous Cnidarian Conifer Crustacean Ctenoid Culled Cynosure Czarina',
    'Dalmatian Delphi Dhurrie Dinner Djinn Document Drill Dunleary Dvorak Dwindle Dynamo',
    'Eames Ebullient Echo Edify Eels Eftsoons Egress Ehrlich Eindhoven Eject Ekistics Elzevir Eminence Ennoble Eocene Ephemeral Equator Erstwhile Estienne Etiquette Eucalyptus Everyman Ewen Exeter Eyelet Ezekiel',
    'Fanfare Ferocious Ffestiniog Finicky Fjord Flanders Forestry Frills Furniture Fylfot',
    'Garrulous Generous Ghastly Gimlet Glorious Gnomon Golfer Grizzled Gumption Gwendolyn Gymkhana',
    'Harrow Heifer Hindemith Horace Hsi Hubris Hybrid',
    'Iambic Ibarra Ichthyology Identity Ievgeny Ifrit Ignite Ihre Ikon Iliad Imminent Innovation Iolanthe Ipanema Irascible Island Italic Ivory Iwis Ixtapa Iyar Izzard',
    'Janacek Jenson Jitter Joinery Jr. Jungian',
    'Kaiser Kenilworth Khaki Kindred Klondike Knowledge Kohlrabi Kraken Kudzu Kvetch Kwacha Kyrie',
    'Labrador Lent Lhasa Liniment Llama Longboat Luddite Lyceum',
    'Mandarin Mbandaka Mcintyre Mdina Mendacious Mfg. Mg Millinery Mlle. Mme. Mnemonic Moribund Mr. Ms. Mtn. Munitions Myra',
    'Narragansett Nefarious Nguyen Nile Nkoso Nnenna Nonsense Nr. Nunnery Nyack',
    'Oarsman Oblate Ocular Odessa Oedipus Often Ogre Ohms Oilers Okra Olfactory Ominous Onerous Oogamous Opine Ornate Ossified Othello Oubliette Ovens Owlish Oxen Oyster Ozymandias',
    'Parisian Pb Pd. Penrose Pfennig Pg. Pharmacy Pirouette Pleistocene Pneumatic Porridge Pp. Principle Psaltery Ptarmigan Pundit Pyrrhic',
    'Qaid Qed Qibris Qom Quill Quadratic Quantum',
    'Ransom Rb. Rd. Renfield Rheumatic Ringlet Rm. Ronsard Rp. Rte. Runcible Rwanda Rye',
    'Salacious Sbeitla Scherzo Serpentine Sforza Shackles Sinful Sjoerd Skull Slalom Smelting Snipe Sorbonne Spartan Squire Sri Stultified Summoner Svelte Swarthy Sykes Szentendre',
    'Tarragon Tblisi Tcherny Tennyson Thaumaturge Tincture Tlaloc Toreador Treacherous Tsunami Turkey Twine Tyrolean Tzara',
    'Ubiquitous Ucello Udder Ufology Ugric Uhlan Uitlander Ukulele Ulster Umber Unguent Uomo Uplift Ursine Usurious Utrecht Uvula Uxorious Uzbek',
    'Vanished Vd. Venomous Vindicate Voracious Vrillier Vs. Vt. Vulnerable Vying',
    'Washington Wendell Wharf Window Wm. Worth Wrung Wt. Wunderman Wyes',
    'Xanthan Xenon Xiao Xmas Xray Xuxa Xylem',
    'Yarrow Ybarra Ycair Yds. Yellowstone Yggdrasil Yin Ylang Yours Ypsilanti Yquem Yrs. Ys. Ytterbium Yunnan Yvonne',
    'Zanzibar Zero Zhora Zinfandel Zone Zuni Zwieback Zygote'
)
ULCWORDS = ' '.join(ULCWORDS).split(' ')

SIMPLE_LC = 'abcdefghijklmnopqrstuvwxyz'
SIMPLE_UC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Replace all lc by equivalent smallcap name.
USCWORDS = []
ULCUSCWORDS = [] # Cap-lc Cap-uc words
for word in ULCWORDS:
    wordLC = ''
    wordSC = ''
    for c in word:
        wordLC += '/'+c
        if c in SIMPLE_LC:
            c = '%s.sc' % c.upper()
        wordSC += '/'+c
    USCWORDS.append(wordSC)
    ULCUSCWORDS.append(wordLC)
    ULCUSCWORDS.append(wordSC)

ULCWORDS_PAGE = ' '.join(ULCWORDS)
USCWORDS_PAGE = '/space'.join(USCWORDS)
ULCUSCWORDS_PAGE = '/space'.join(ULCUSCWORDS)

SPACING = (
    u'''HH!H HH"H HH#H HH$H HH%H HH&H HH'H HH(H HH)H HH*H HH+H HH,H HH.H HH/H HH0H HH1H HH2H HH3H HH4H HH5H HH6H HH7H HH8H '''+\
    u'''HH9H HH:H HH;H HH<H HH=H HH>H HH?H HH@H HHAH HHBH HHCH HHDH HHEH HHFH HHGH HHHH HHIH HHJH HHKH HHLH HHMH HHNH HHOH '''+\
    u'''HHPH HHQH HHRH HHSH HHTH HHUH HHVH HHWH HHXH HHYH HHZH HH[H HH\H HH]H HH`H HH{H HH|H HH}H HH~H HHÄH HHÅH HHÇH HHÉH '''+\
    u'''HHÑH HHÖH HHÜH HH†H HH°H HH¢H HH£H HH§H HH•H HH¶H HH®H HH©H HH™H HH´H HH¨H HH≠H HHÆH HHØH HH∞H HH±H HH≤H HH≥H HH¥H '''+\
    u'''HHμH HH∂H HH∑H HH∏H HHπH HH∫H HHªH HHºH HHΩH HH¿H HH¡H HH¬H HH√H HHƒH HH≈H HH∆H HH«H HH»H HHÀH HHÃH HHÕH HHŒH HH–H '''+\
    u'''HH“H HH”H HH‘H HH’H HH÷H HH◊H HHŸH HH⁄H HH‹H HH›H HH‡H HH∙H HH‚H HH„H HH‰H HHÂH HHÊH HHÁH HHËH HHÈH HHÍH HHÎH HHÏH '''+\
    u'''HHÌH HHÓH HHÔH HHH HHÒH HHÚH HHÛH HHÙH HHıH HHˆH HHˉH HH˜H HH˘H HH˙H HH˚H HH-H HH–H HH—H''',

    u'''OO!O OO"O OO#O OO$O OO%O OO&O OO'O OO(O OO)O OO*O OO+O OO,O OO.O OO/O OO0O OO1O OO2O OO3O OO4O OO5O OO6O OO7O OO8O '''+\
    u'''OO9O OO:O OO;O OO<O OO=O OO>O OO?O OO@O OOAO OOBO OOCO OODO OOEO OOFO OOGO OOHO OOIO OOJO OOKO OOLO OOMO OONO OOOO '''+\
    u'''OOPO OOQO OORO OOSO OOTO OOUO OOVO OOWO OOXO OOYO OOZO OO[O OO\O OO]O OO`O OO{O OO|O OO}O OO~O OOÄO OOÅO OOÇO OOÉO '''+\
    u'''OOÑO OOÖO OOÜO OO†O OO°O OO¢O OO£O OO§O OO•O OO¶O OO®O OO©O OO™O OO´O OO¨O OO≠O OOÆO OOØO OO∞O OO±O OO≤O OO≥O OO¥O '''+\
    u'''OOμO OO∂O OO∑O OO∏O OOπO OO∫O OOªO OOºO OOΩO OO¿O OO¡O OO¬O OO√O OOƒO OO≈O OO∆O OO«O OO»O OOÀO OOÃO OOÕO OOŒO OO–O '''+\
    u'''OO“O OO”O OO‘O OO’O OO÷O OO◊O OOŸO OO⁄O OO‹O OO›O OOﬁO OOﬂO OO‡O OO∙O OO‚O OO„O OO‰O OOÂO OOÊO OOÁO OOËO OOÈO OOÍO '''+\
    u'''OOÎO OOÏO OOÌO OOÓO OOÔO OOO OOÒO OOÚO OOÛO OOÙO OOıO OOˆO OOˉO OO˜O OO˘O OO˙O OO˚O OO-O OO–O OO—O''',

    u'''nnan nnbn nncn nndn nnen nnfn nngn nnhn nnin nnjn nnkn nnln nnmn nnnn nnon nnpn nnqn nnrn nnsn nntn nnun nnvn nnwn '''+\
    u'''nnxn nnyn nnzn nnán nnàn nnân nnän nnãn nnån nnçn nnén nnèn nnên nnën nnín nnìn nnîn nnïn nnñn nnón nnòn nnôn nnön '''+\
    u'''nnõn nnún nnùn nnûn nnün nnøn nnœn nnæn nnﬁn nnﬂn nnßn nnÿn''',

    u'''ooao oobo ooco oodo ooeo oofo oogo ooho ooio oojo ooko oolo oomo oono oooo oopo ooqo ooro ooso ooto oouo oovo oowo '''+\
    u'''ooxo ooyo oozo ooáo ooào ooâo ooäo ooão ooåo ooço ooéo ooèo ooêo ooëo ooío ooìo ooîo ooïo ooño ooóo ooòo ooôo ooöo '''+\
    u'''ooõo ooúo ooùo ooûo ooüo ooøo ooœo ooæo ooﬁo ooﬂo ooßo ooÿo''',
)
EXTENDED_KERNING = (
    u'áán ààn åån ään ábn àbn ăbn âbn åbn äbn ābn áčn äčn āčn áðn áén áfn àfn ăfn âfn åfn äfn āfn âğn āģn áhn àhn åhn ähn áin '+\
        u'áín àin ăin âin åin äin āin ájn ăjn åjn äjn ājn ákn âkn åkn äkn ākn āķn áln áľn àln ăln âln åln äln āln āļn áňn áñn '+\
        u'áón äön ářn ášn āšn äßn átn áťn àtn ătn ățn âtn âțn åtn ätn äťn ātn ážn āžn áþn',
    u'čán čān ćbn čbn ččn ċċn čėn čēn ćfn čfn ċħn ćin čin čín čīn ċin ćjn čjn ċjn ćkn čkn ċkn ćln čln čľn ċln čňn čŕn čšn čtn '+\
        u'ċtn čún čůn čūn dán dàn dăn dân dån dän dãn dān ďan ďán ðán dčn dén dèn děn dën dēn dħn dìn dîn dīn đin ðín ďkn ďmn '+\
        u'dňn ďnn dòn dôn dön dőn dõn ďon ðón ðön dřn dšn ďsn ďtn dùn důn dün dūn ďun džn ďžn',
    u'éán éân éån ébn èbn ěbn ëbn ēbn éčn ěčn ėčn éðn ěďn één éèn éfn èfn ëfn ēfn ēģn éhn ěhn ëhn éin èin êin ëin ėin éjn èjn '+\
        u'ějn ëjn ėjn ējn ékn ěkn ëkn ēkn ēķn éln èln êln ěln ëln ēln ēļn ěňn éřn ěřn éšn ěšn ėšn ēšn étn ètn êtn ětn ěťn ëtn '+\
        u'ėtn ētn éün éžn ěžn ėžn ēžn fán fàn făn fân fån fän fãn fān fén fèn fên fën fėn fēn fħn fín fīn fňn fón fòn fön főn '+\
        u'fõn fšn fún fûn fůn fün fűn fūn',
    u'ġàn ģān ğbn ģēn ğfn ġġn ğin ġin ģīn ġjn ğln ğtn ġtn ğün ġżn',
    u'hán ħġn ħħn',
    u'ián iàn iân iån iän iãn iān íán íbn ïbn ībn ićn ičn iċn íčn īčn iđn íðn ién ièn iên iën iėn iēn íén įėn ífn ïfn īfn iğn '+\
        u'iġn īģn iħn íhn īhn iín iîn iïn ïïn iīn íin îin íjn ïjn ījn íkn îkn ïkn īkn īķn íln íľn îln ïln īln īļn iňn iñn íňn '+\
        u'íñn ión iòn iôn iön iőn iõn íón iřn ířn iśn išn íšn įšn īšn ítn íťn ìtn îtn îțn ïtn ītn iùn iůn iün iūn iźn ižn iżn '+\
        u'ížn įžn īžn íþn',
    u'ján jàn jăn jân jån jän jãn jān jčn jċn jén jèn jën jėn jēn jġn jħn jín jīn jňn jón jòn jôn jön jőn jõn jřn jśn jšn jún '+\
        u'jůn jün jūn jžn jżn lán làn lăn lân lån län lãn lān ľan ļān ľbn lčn ľčn ľdn lén lèn lên lën lēn ļēn lğn ľgn lħn ľhn '+\
        u'lìn lîn līn ļīn ľjn ľkn ļķn ľmn lńn lňn ĺňn ľnn ľňn lòn lôn lön lőn lõn ľon łón ľrn lšn ľsn ľšn ļšn ľtn łtn lùn lůn '+\
        u'lün lūn ľun ľún ļūn ľvn lžn ĺžn ľžn ļžn',
    u'ňán ñán ñén ňhn ñin ñín ńkn ňkn ñón ňůn',
    u'óán öän őán óbn ôbn öbn őbn õbn óčn ôčn óðn öðn óén őén ófn öfn őfn öğn óhn ôhn öhn őhn õhn óin óín öin őin őín õin ójn '+\
        u'ôjn öjn őjn õjn ókn ôkn ökn őkn õkn óln ółn ôln ôľn öln őln õln óňn ôňn óón óön öön öõn őón őön őőn õõn óśn ôšn ößn '+\
        u'ótn ôtn ôťn ötn őtn õtn óún óün őún őün óźn óžn óżn ôžn óþn',
    u'řán řbn ŕčn řčn ŕhn řin řín řkn řln ŕňn řňn ŕšn řšn ŕtn řtn řůn ŕžn',
    u'šán šān śbn šbn śćn šćn ščn šén šėn šēn šģn šhn šin šín šįn šīn šjn škn šķn śln šln šľn šļn śńn šňn ššn ßön štn šťn šún '+\
        u'šůn šün šūn šžn',
    u'tán tàn tăn tân tån tän tãn tān ťan ťán țăn țân tċn ťcn ťčn ťdn tén tèn tên těn tën tėn tēn tħn ťhn tìn tîn tīn ťjn ťkn '+\
        u'ťln ťmn tňn ťnn tón tòn tôn tön tőn tõn ťon ťpn tŕn třn ťrn tšn ťsn ťšn ťtn tùn tůn tün tūn ťun ťůn tžn',
    u'úán üän úbn ůbn übn űbn ūbn účn ůčn ūčn úðn üén üèn úfn üfn űfn ūfn üğn úhn ůhn ühn űhn ūhn úin úín üin üín űin újn ůjn '+\
        u'üjn űjn ūjn úkn ůkn ükn űkn ūkn ūķn úln úľn ûln ůln üln űln ūln ūļn úňn úñn úřn ůřn úšn ūšn üßn útn úťn ûtn ůtn ütn '+\
        u'űtn ūtn üün úžn ůžn ūžn',
    u'ýán ýbn ýčn ýðn ýfn ýhn ýin ýjn ýkn ýln ýľn ýňn ýón ýön ýřn ýšn ýtn ýťn ýžn ýþn',
    u'žán žän žān źbn žbn zčn źćn žčn žđn žén žėn žēn żèn žfn žģn žhn žin žín žįn žīn żin źjn žjn żjn źkn žkn źln žln žľn źńn '+\
        u'žňn żón žšn žtn žún žůn žün žūn žžn żżn',
    u'ągn ąjn ąpn ççn çgn çpn ęgn ępn gļn gșn įgn įjn įpn jçn jįn jųn ķgn ļgn ļģn ļjn ļļn ļņn ļpn ņgn ņjn ņķn ņņn ņpn pșn şçn '+\
        u'şgn şpn șpn şşn şyn ųjn ųpn yçn yşn',
    u'Bħn Bìn Bîn Bīn Břn',
    u'Càn Căn Cân Cän Cãn Cān Čān Çàn Çãn Cčn Ččn Ċċn Cèn Cên Cën Cėn Cēn Čėn Čēn Çën Ćfn Čfn Ċħn Cín Cìn Cîn Cīn Čín Čīn Cłn '+\
        u'Cňn Čňn Cón Còn Côn Cön Cõn Çón Çòn Çön Çõn Čŕn Cšn Čšn Cún Cůn Cün Cūn Čún Čůn Čūn Çún Çün Cžn',
    u'Dħn Dín Dìn Dîn Dīn Đin Ðín Dŕn Dřn',
    u'Eàn Eăn Eân Eän Eãn Eān Éân Ečn Éčn Ěčn Ėčn Éðn Eên Eën Eēn Éèn Eğn Eħn Eín Eîn Eïn Eīn Ełn Ęłn Eńn Eňn Eñn Ěňn Eón Eòn '+\
        u'Eön Eõn Eøn Eřn Éřn Ěřn Eśn Ešn Éšn Ěšn Ėšn Ęśn Ęšn Ēšn Eún Eůn Eün Eūn Éün Eźn Ežn Eżn Éžn Ězn Ěžn Ėžn Ęźn Ęžn Ężn '+\
        u'Ēžn',
    u'Fán Fàn Făn Fân Fån Fän Fãn Fān Fén Fèn Fên Fën Fėn Fēn Fħn Fín Fīn Fňn Fón Fòn Fön Főn Fõn Fšn Fún Fûn Fůn Fün Fűn Fūn '+\
        u'Fýn',
    u'Gàn Găn Gân Gån Gän Gãn Gān Ġàn Ģān Gén Gèn Gên Gën Gėn Gēn Ģēn Ğfn Ġfn Gġn Ġġn Għn Gín Gìn Gīn Ğin Ġin Ģīn Głn Gón Gòn '+\
        u'Gôn Gön Gőn Gõn Gřn Gšn Gún Gùn Gůn Gün Gűn Gūn Ğün Gýn Gžn Gżn Ġżn',
    u'Hán Hàn Hăn Hân Hån Hän Hãn Hān Hčn Hén Hèn Hên Hën Hėn Hēn Ħġn Ħħn Hín Hìn Hīn Hĺn Hłn Hňn Hón Hòn Hôn Hön Hőn Hõn Hŕn '+\
        u'Hřn Hśn Hšn Hún Hůn Hün Hűn Hūn Hýn Hžn Hżn Ħżn',
    u'Ián Iàn Iân Iån Iän Iãn Iān Íán Íbn Ïbn Ībn Ićn Ičn Iċn Íčn Īčn Ién Ièn Iên Iën Iėn Iēn Íén Įėn Ífn Ïfn Īfn Iğn Iġn Īģn '+\
        u'Iħn Íhn Īhn Iín Iîn Ïïn Iïn Iīn Íin Îin Íjn Ïjn Ījn Íkn Îkn Ïkn Īkn Īķn Iłn Íln Íľn Îln Ïln Īln Īļn Ińn Iňn Iñn Íňn '+\
        u'Íñn Ión Iòn Iôn Iön Iőn Iõn Íon Íón Iřn Ířn Iśn Išn Íšn Įšn Īšn Ítn Íťn Ìtn Îtn Îțn Ïtn Ītn Iún Iùn Iůn Iün Iűn Iūn '+\
        u'Iźn Ižn Iżn Ížn Įžn Īžn Íþn Iğn Iön Jħn Jín Jīn Jłn Jřn',
    u'Kàn Kăn Kân Kån Kän Kān Ķān Kćn Kčn Kċn Kén Kèn Kên Kën Kėn Kēn Ķēn Kħn Kín Kīn Ķīn Kĺn Kłn Kňn Kón Kòn Kôn Kön Kőn Kõn '+\
        u'Køn Kŕn Křn Kśn Kšn Ķšn Kún Kůn Kün Kűn Kūn Ķūn Kýn Kžn Kżn',
    u'Ľbn Ľčn Ľdn Ľhn Ľjn Ľkn Ľňn Ľšn Ľtn Ľún Ľvn Łwn Łyn Ľžn',
    u'Mħn Mín Mìn Mīn Młn Mřn Nħn Nín Nìn Nîn Nīn Ñin Ñín',
    u'Oín Oîn Oïn Oīn Óín Őín Øin Øjn Økn Øln Ořn',
    u'Pán Pàn Păn Pân Pån Pän Pãn Pān Pćn Pčn Pén Pèn Pên Pěn Pën Pėn Pēn Pín Pìn Pîn Pīn Płn Pńn Pňn Pón Pòn Pôn Pön Pőn Põn '+\
        u'Pŕn Přn Pšn Pún Půn Pün Pűn Pūn Pýn Pžn Ràn Răn Rân Rån Rän Rãn Rān Řán Rćn Rčn Rċn Ŕčn Řčn Rén Rèn Rên Rën Rėn Rēn '+\
        u'Rġn Rħn Rín Rìn Rîn Rīn Řin Řín Rłn Rňn Ŕňn Řňn Rón Ròn Rôn Rön Rőn Rõn Røn Rśn Ršn Ŕšn Řšn Rún Rùn Rûn Růn Rün Rűn '+\
        u'Rūn Řůn Rýn Ržn Rżn Ŕžn',
    u'Sán Sàn Săn Sân Sån Sän Sãn Sān Šán Šān Șăn Șân Sčn Śćn Šćn Ščn Sén Sèn Sên Sën Sėn Sēn Šén Šėn Šēn Šģn Sħn Sín Sìn Sîn '+\
        u'Sīn Šín Šīn Słn Sňn Śńn Šňn Són Sòn Sôn Sön Sőn Sõn Şön Sšn Ššn Sún Sùn Sûn Sůn Sün Sűn Sūn Šún Šůn Šün Šūn Şün Sýn '+\
        u'Sžn Šžn',
    u'Tán Tàn Tăn Tân Tån Tän Tãn Tān Ťán Țăn Țân Tčn Tċn Ťčn Tén Tèn Tên Těn Tën Tėn Tēn Tħn Tín Tìn Tîn Tīn Ťjn Ťkn Tĺn Tłn '+\
        u'Ťln Tňn Tón Tòn Tôn Tön Tőn Tõn Tøn Tŕn Třn Tšn Ťšn Tún Tùn Tůn Tün Tűn Tūn Ťůn Týn Tžn',
    u'Uħn Uín Uìn Uîn Uïn Uīn Úin Úín Üín Uřn Úřn Ůřn',
    u'Ván Vàn Văn Vân Vån Vän Vãn Vān Včn Vén Vèn Vên Věn Vën Vėn Vēn Vín Vìn Vīn Vĺn Vňn Vón Vòn Vôn Vön Vőn Võn Vøn Vŕn Vřn '+\
        u'Všn Vún Vůn Vün Vűn Vūn Výn Vžn',
    u'Wán Wàn Wän Wén Wèn Wên Wġn Wħn Wín Wîn Włn Wón Wön Wśn Wün Wżn',
    u'Xán Xàn Xăn Xån Xãn Xén Xèn Xên Xën Xħn Xín Xón Xòn Xôn Xõn Xøn Xún Xůn Xýn',
    u'Yán Yàn Yån Yän Ýan Ýán Ýbn Yćn Yčn Ýcn Ýčn Ýdn Ýðn Yén Yèn Yín Yłn Yńn Yňn Ýňn Yón Yòn Yön Yőn Yøn Ýón Ýön Yřn Ýřn Yśn '+\
        u'Yšn Ýšn Yún Yůn Yün Yűn Yźn Yžn Yżn Ýžn Ýþn',
    u'Zín Zîn Zīn Žín Žīn Złn Żłn Zŕn Zřn Zýn',
    u'Ągn Ąjn Ąpn Ççn Çgn Çpn Çyn Ęgn Ępn Įgn Įjn Įpn Ķgn Ļgn Ļģn Ļjn Ļķn Ļļn Ļņn Ļpn Ņgn Ņģn Ņjn Ņķn Ņņn Ņpn Şçn Şgn Şpn Șpn '+\
        u'Şşn Şyn Ųjn Ųpn'
)
CONTEXT_KERNING = u'ááábáčáéáðáfáháiáíájákáláľáňáñáóářášátáťáþážăbăfăiăjălătățâbâfâğâiâkâlâtâțäääbäčäfäßähäiäjäkäläöätäťàààbàfàhàiàlàtābā'+\
    u'čāfāģāiājākāķālāļāšātāžåååbåfåhåiåjåkålåtćbćfćićjćkćlčáčāčbčččėčēčfčičíčīčjčkčlčľčňčřčščtčúčūčůċċċħċiċjċkċlċtdádădâdädàdādådãdčdéděd'+\
    u'ëdèdēdħdîdìdīdňdôdödòdődõdřdšdüdùdūdůdžďaďáďkďmďnďoďsďtďuďžđiéáéâéåébéčéééèéðéféhéiéjékéléřéšétéüéžěběčěďěhějěkělěňěřěšětěťěžêiêlêtë'+\
    u'bëfëhëiëjëkëlëtėčėiėjėšėtėžèbèfèièjèlètēbēfēģējēkēķēlēļēšētēžðáðíðóðöfáfăfâfäfàfāfåfãféfêfëfėfèfēfħfífīfňfóföfòfőfõfšfúfûfüfűfūfůğbğ'+\
    u'fğiğlğtğüģāģēģīġàġġġiġjġtġżßöháħġħħiáiâiäiàiāiåiãićičiċiđiéiêiëiėièiēiğiġiħiíiîiïiīiňiñióiôiöiòiőiõiřiśišiüiùiūiůiźižiżíáíbíčíéíðífí'+\
    u'híiíjíkílíľíňíñíóíříšítíťíþížîiîkîlîtîțïbïfïïïjïkïlïtìtībīčīfīģīhījīkīķīlīļīšītīžįėįšįžjájăjâjäjàjājåjãjčjċjéjëjėjèjējġjħjíjījňjójôj'+\
    u'öjòjőjõjřjśjšjújüjūjůjžjżlálălâlälàlālålãlčlélêlëlèlēlğlħlîlìlīlńlňlôlölòlőlõlšlülùlūlůlžĺňĺžľaľbľčľdľgľhľjľkľmľnľňľoľrľsľšľtľuľúľvľ'+\
    u'žļāļēļīļķļšļūļžłółtńkňáňhňkňůñáñéñiñíñóóáóbóčóéóðófóhóióíójókólółóňóóóöóśótóþóúóüóźóžóżôbôčôhôjôkôlôľôňôšôtôťôžöäöböðöföğößöhöiöjökö'+\
    u'löööõötőáőbőéőfőhőiőíőjőkőlőóőöőőőtőúőüõbõhõiõjõkõlõõõtřářbřčřhřiřířkřlřňřšřtřůřžśbśćślśńšášāšbšćščšéšėšēšģšhšišíšīšįšjškšķšlšľšļšňš'+\
    u'šštšťšúšüšūšůšžtátătâtätàtātåtãtċtétětêtëtėtètētħtîtìtītňtótôtötòtőtõtřtštütùtūtůtžťaťáťcťčťdťhťjťkťlťmťnťoťpťrťsťšťtťuťůțățâúáúbúčú'+\
    u'ðúfúhúiúíújúkúlúľúňúñúřúšútúťúžûlûtüäübüéüèüfüğüßühüiüíüjükülütüüűbűfűhűiűjűkűlűtūbūčūfūhūjūkūķūlūļūšūtūžůbůčůhůjůkůlůřůtůžýáýbýčýðý'+\
    u'fýhýiýjýkýlýľýňýóýöýřýšýtýťýþýžzčźbźćźjźkźlźńžážäžāžbžčžđžéžėžēžfžģžhžižížīžįžjžkžlžľžňžšžtžúžüžūžůžžżèżiżjżóżżągąjąpçççgçpęgępgļgșį'+\
    u'gįjįpjçjįjųķgļgļģļjļļļņļpņgņjņķņņņppșşçşgşpşşşyșpųjųpyçyşBħBîBìBīBřCăCâCäCàCāCãCčCêCëCėCèCēCíCîCìCīCłCňCóCôCöCòCõCšCúCüCūCůCžĆfČāČčČ'+\
    u'ėČēČfČíČīČňČřČšČúČūČůÇàÇãÇëÇóÇöÇòÇõÇúÇüĊċĊħDħDíDîDìDīDřĐiĐíEăEâEäEàEāEãEčEêEëEēEğEħEíEîEïEīEłEńEňEñEóEöEòEøEõEřEśEšEúEüEūEůEźEžEżÉâÉ'+\
    u'čÉèÉðÉřÉšÉüÉžĚčĚňĚřĚšĚzĚžĖčĖšĖžĒšĒžĘłĘśĘšĘźĘžĘżFáFăFâFäFàFāFåFãFéFêFëFėFèFēFħFíFīFňFóFöFòFőFõFšFúFûFüFűFūFůFýGăGâGäGàGāGåGãGéGêGëGėG'+\
    u'èGēGġGħGíGìGīGłGóGôGöGòGőGõGřGšGúGüGùGűGūGůGýGžGżĞfĞiĞüĢāĢēĢīĠàĠfĠġĠiĠżHáHăHâHäHàHāHåHãHčHéHêHëHėHèHēHíHìHīHĺHłHňHóHôHöHòHőHõHřHśHšH'+\
    u'úHüHűHūHůHýHžHżĦġĦħĦżIáIâIäIàIāIåIãIćIčIċIéIêIëIėIèIēIğIġIħIíIîIïIīIłIńIňIñIóIôIöIòIőIõIřIśIšIúIüIùIűIūIůIźIžIżÍáÍbÍčÍéÍfÍhÍiÍjÍkÍlÍ'+\
    u'ľÍňÍñÍoÍóÍřÍšÍtÍťÍþÍžÎiÎkÎlÎtÎțÏbÏfÏïÏjÏkÏlÏtÌtĪbĪčĪfĪģĪhĪjĪkĪķĪlĪļĪšĪtĪžĮėĮšĮžJħJíJīJłJřKăKâKäKàKāKåKćKčKċKéKêKëKėKèKēKħKíKīKĺKłKňK'+\
    u'óKôKöKòKőKøKõKřKśKšKúKüKűKūKůKýKžKżĶāĶēĶīĶšĶūĽbĽčĽdĽhĽjĽkĽňĽšĽtĽúĽvĽžŁwŁyMħMíMìMīMłMřNħNíNîNìNīÑiÑíOíOîOïOīOřÓíŐíØiØjØkØlPáPăPâPäPàP'+\
    u'āPåPãPćPčPéPěPêPëPėPèPēPíPîPìPīPłPńPňPóPôPöPòPőPõPřPšPúPüPűPūPůPýPžRăRâRäRàRāRåRãRćRčRċRéRêRëRėRèRēRġRħRíRîRìRīRłRňRóRôRöRòRőRøRõRśR'+\
    u'šRúRûRüRùRűRūRůRýRžRżŔčŔňŔšŔžŘáŘčŘiŘíŘňŘšŘůSáSăSâSäSàSāSåSãSčSéSêSëSėSèSēSħSíSîSìSīSłSňSóSôSöSòSőSõSšSúSûSüSùSűSūSůSýSžŚćŚńŠáŠāŠćŠčŠ'+\
    u'éŠėŠēŠģŠíŠīŠňŠšŠúŠüŠūŠůŠžŞöŞüȘăȘâTáTăTâTäTàTāTåTãTčTċTéTěTêTëTėTèTēTħTíTîTìTīTĺTłTňTóTôTöTòTőTøTõTřTšTúTüTùTűTūTůTýTžŤáŤčŤjŤkŤlŤšŤůȚ'+\
    u'ăȚâUħUíUîUïUìUīUřÚiÚíÚřÜíŮřVáVăVâVäVàVāVåVãVčVéVěVêVëVėVèVēVíVìVīVĺVňVóVôVöVòVőVøVõVřVšVúVüVűVūVůVýVžWáWäWàWéWêWèWġWħWíWîWłWóWöWśWüW'+\
    u'żXáXăXàXåXãXéXêXëXèXħXíXóXôXòXøXõXúXůXýYáYäYàYåYćYčYéYèYíYłYńYňYóYöYòYőYøYřYśYšYúYüYűYůYźYžYżÝaÝáÝbÝcÝčÝdÝðÝňÝóÝöÝřÝšÝþÝžZíZîZīZłZřZ'+\
    u'ýŽíŽīŻłĄgĄjĄpÇçÇgÇpÇyĘgĘpĮgĮjĮpĶgĻgĻģĻjĻķĻļĻņĻpŅgŅģŅjŅķŅņŅpŞçŞgŞpŞşŞyȘpŲjŲp'

JILL_KERNING = (
    # Lowercase
    u'aaeaoaiauacadahamanarasatabagafalapavawayajakaqaxazaeeoeieuecedehemeneresetebegefelepeveweyejekeqeexezeooiouocodohomonorosotobogofol'+\
    u'opovowoyojokoqoxozoiiuicidihiminirisitibigifilipiviwiyijikiqixiziuucuduhumunurusutubugufulupuvuwuyujukuquxuzuccdchcmcncrcsctcbcgcfcl'+\
    u'cpcvcwcycjckcqcxczcddhdmdndrdsdtdbdgdfdldpdvdwdydjdkdqdxdzdhhmhnhrhshthbhghfhlhphvhwhyhjhkhqhxhzhmmmnmrmsmtmbmgmfmlmpmvmwmymjmkmqmxm'+\
    u'zmnnrnsntnbngnfnlnpnvnwnynjnknqnxnznrrsrtrbrgrfrlrprvrwryrjrkrqrxrzrsstsbsgsfslspsvswsysjsksqsxszsttbtgtftltptvtwtytjtktqtxtztbbgbfb'+\
    u'lbpbvbwbybjbkbqbxbzbggfglgpgvgwgygjgkgqgxgzgfflfpfvfwfyfjfkfqfxfzfllplvlwlyljlkllqlxlzlppvpwpypjpkpqppxpzpvvwvyvjvkvqvxvzvyywyyyjyky'+\
    u'qyxyzyjjkjqjxjzjkkkqkxkzkqqxqzqxxzxzzaaeaoaiauacadahamanaraasatabagafalapavawayajakaqaxaeazaeeoeieuecedehemeneresetebegefelepeveweye'+\
    u'jekeqeexezeooiouocodohomonoroosotobogofolopovowoyojokoqooxozoiiuicidihiminirisiitibigifilipiviwiyijikiqixiziuucuduhumunurusutuubuguf'+\
    u'ulupuvuwuyujukuquxuzucccdchcmcncrcsctcbcgcfclccpcvcwcycjckcqcxczcddhdmdnddrdsdtdbdgdfdldpdvdwdydjddkdqdxdzdhhmhnhrhshthbhgfhlhphvhwh'+\
    u'yhjhkhqhxhzhmmnmrmsmtmbmgmfmlmpmvmwmymmjmkmqmxmzmnnrnsntnbngnfnlnpnvnwnynjnknqnxnznrrsrrtrbrgrfrlrprvrwryrjrkrrqrxrzrsstsbsgsfslspsv'+\
    u'swsyssjsksqsxszsttbtgtftltptvtwttytjtktqtxtztbbgbfblbpbbvbwbybjbkbqbxbzbggfglgpggvgwgygjgkgqgxgzgfflfpfvffwfyfjfkfqfxfzfllplvlwlyljl'+\
    u'lklqlxlzlppvpwpypjpkpqppxpzpvvwvyvjvkvqvxvzvyywyyyjykyqyxyzyjjkjqjxjzjkkkqkkxkzkqqxqzqxxzxzz'+\
    u'he is but an it at the she do on his not like of them are as they can both be for or be in with his too in from were by only some her '+\
    u'have to after that than which you also had either ',

    # Capitals
    u'AAEAOAIAUACADAHAMANARASATABAGAFALAPAVAWAYAJAKAQAXAZAEEOEIEUECEDEHEMENERESETEBEGEFELEPEVEWEYEJEKEQEEXEZEOOIOUOCODOHOMONOROSOTOBOGOFOL'+\
    u'OPOVOWOYOJOKOQOXOZOIIUICIDIHIMINIRISITIBIGIFILIPIVIWIYIJIKIQIXIZIUUCUDUHUMUNURUSUTUBUGUFULUPUVUWUYUJUKUQUXUZUCCDCHCMCNCRCSCTCBCGCFCL'+\
    u'CPCVCWCYCJCKCQCXCZCDDHDMDNDRDSDTDBDGDFDLDPDVDWDYDJDKDQDXDZDHHMHNHRHSHTHBHGHFHLHPHVHWHYHJHKHQHXHZHMMMNMRMSMTMBMGMFMLMPMVMWMYMJMKMQMXM'+\
    u'ZMNNRNSNTNBNGNFNLNPNVNWNYNJNKNQNXNZNRRSRTRBRGRFRLRPRVRWRYRJRKRQRXRZRSSTSBSGSFSLSPSVSWSYSJSKSQSXSZSTTBTGTFTLTPTVTWTYTJTKTQTXTZTBBGBFB'+\
    u'LBPBVBWBYBJBKBQBXBZBGGFGLGPGVGWGYGJGKGQGXGZGFFLFPFVFWFYFJFKFQFXFZFLLPLVLWLYLJLKLLQLXLZLPPVPWPYPJPKPQPPXPZPVVWVYVJVKVQVXVZVYYWYYYJYKY'+\
    u'QYXYZYJJKJQJXJZJKKKQKXKZKQQXQZQXXZXZZAAEAOAIAUACADAHAMANARAASATABAGAFALAPAVAWAYAJAKAQAXAEAZAEEOEIEUECEDEHEMENERESETEBEGEFELEPEVEWEYE'+\
    u'JEKEQEEXEZEOOIOUOCODOHOMONOROOSOTOBOGOFOLOPOVOWOYOJOKOQOOXOZOIIUICIDIHIMINIRISIITIBIGIFILIPIVIWIYIJIKIQIXIZIUUCUDUHUMUNURUSUTUUBUGUF'+\
    u'ULUPUVUWUYUJUKUQUXUZUCCCDCHCMCNCRCSCTCBCGCFCLCCPCVCWCYCJCKCQCXCZCDDHDMDNDDRDSDTDBDGDFDLDPDVDWDYDJDDKDQDXDZDHHMHNHRHSHTHBHGFHLHPHVHWH'+\
    u'YHJHKHQHXHZHMMNMRMSMTMBMGMFMLMPMVMWMYMMJMKMQMXMZMNNRNSNTNBNGNFNLNPNVNWNYNJNKNQNXNZNRRSRRTRBRGRFRLRPRVRWRYRJRKRRQRXRZRSSTSBSGSFSLSPSV'+\
    u'SWSYSSJSKSQSXSZSTTBTGTFTLTPTVTWTTYTJTKTQTXTZTBBGBFBLBPBBVBWBYBJBKBQBXBZBGGFGLGPGGVGWGYGJGKGQGXGZGFFLFPFVFFWFYFJFKFQFXFZFLLPLVLWLYLJL'+\
    u'LKLQLXLZLPPVPWPYPJPKPQPPXPZPVVWVYVJVKVQVXVZVYYWYYYJYKYQYXYZYJJKJQJXJZJKKKQKKXKZKQQXQZQXXZXZZ'+\
    u'HE IS BUT AN IT AT THE SHE DO ON HIS NOT LIKE OF THEM ARE AS THEY CAN BOTH BE FOR OR BE IN WITH HIS TOO IN FROM WERE BY ONLY SOME HER '+\
    u'HAVE TO AFTER THAT THAN WHICH YOU ALSO HAD EITHER.',

    # Capitals + lower case
    u'TaTbTcTdTeTfTgThTiTjTkTlTmTnToTpTqTrTsTtTuTvTwTxTyTzTœTæTßTfiTflVaVbVcVdVeVfVgVhViVjVkVlVmVnVoVpVqVrVsVtVuVvVwVxVyVzVœVæVßVfiVflWaWb'+\
    u'WcWdWeWfWgWhWiWjWkWlWmWnWoWpWqWrWsWtWuWvWwWxWyWzWœWæWßWfiWflYaYbYcYdYeYfYgYhYiYjYkYlYmYnYoYpYqYrYsYtYuYvYwYxYyYzYœYæYßYfiYflKaKbKcKd'+\
    u'KeKfKgKhKiKjKkKlKmKnKoKpKqKrKsKtKuKvKwKxKyKzRaRbRcRdReRfRgRhRiRjRkRlRmRnRoRpRqRrRsRtRuRvRwRxRyRzJaJbJcJdJeJfJgJhJiJjJkJlJmJnJoJpJqJr'+\
    u'JsJtJuJvJwJxJyJzPaPbPcPdPePfPgPhPiPjPkPlPmPnPoPpPqPrPsPtPuPvPwPxPyPzFaFbFcFdFeFfFgFhFiFjFkFlFmFnFoFpFqFrFsFtFuFvFwFxFyFzAaAbAcAdAeAf'+\
    u'AgAhAiAjAkAlAmAnAoApAqArAsAtAuAvAwAxAyAzAœAæAßAfiAflFœFæFßFfiFflKœKæKßKfiKflPœPæPßPfiPflLaLbLcLdLeLfLgLhLiLjLkLlLmLnLoLpLqLrLsLtLuLv'+\
    u'LwLxLyLzLœLæLßLfiLflBaBbBcBdBeBfBgBhBiBjBkBlBmBnBoBpBqBrBsBtBuBvBwBxByBzBœBæBßBfiBflRœRæRßRfiRflSaSbScSdSeSfSgShSiSjSkSlSmSnSoSpSqSr'+\
    u'SsStSuSvSwSxSySzSœSæSßSfiSflCaCbCcCdCeCfCgChCiCjCkClCmCnCoCpCqCrCsCtCuCvCwCxCyCzCœCæCßCfiCflDaDbDcDdDeDfDgDhDiDjDkDlDmDnDoDpDqDrDsDt'+\
    u'DuDvDwDxDyDzDœDæDßDfiDflEaEbEcEdEeEfEgEhEiEjEkElEmEnEoEpEqErEsEtEuEvEwExEyEzEœEæEßEfiEflNaNbNcNdNeNfNgNhNiNjNkNlNmNnNoNpNqNrNsNtNuNv'+\
    u'NwNxNyNzNœNæNßNfiNflGaGbGcGdGeGfGgGhGiGjGkGlGmGnGoGpGqGrGsGtGuGvGwGxGyGzGœGæGßGfiGflOaObOcOdOeOfOgOhOiOjOkOlOmOnOoOpOqOrOsOtOuOvOwOx'+\
    u'OyOzOœOæOßOfiOflQaQbQcQdQeQfQgQhQiQjQkQlQmQnQoQpQqQrQsQtQuQvQwQxQyQzQœQæQßQfiQflHaHbHcHdHeHfHgHhHiHjHkHlHmHnHoHpHqHrHsHtHuHvHwHxHyHz'+\
    u'HœHæHßHfiHflIaIbIcIdIeIfIgIhIiIjIkIlImInIoIpIqIrIsItIuIvIwIxIyIzIœIæIßIfiIflJœJæJßJfiJflMaMbMcMdMeMfMgMhMiMjMkMlMmMnMoMpMqMrMsMtMuMv'+\
    u'MwMxMyMzMœMæMßMfiMflUaUbUcUdUeUfUgUhUiUjUkUlUmUnUoUpUqUrUsUtUuUvUwUxUyUzUœUæUßUfiUflXaXbXcXdXeXfXgXhXiXjXkXlXmXnXoXpXqXrXsXtXuXvXwXx'+\
    u'XyXzXœXæXßXfiXflZaZbZcZdZeZfZgZhZiZjZkZlZmZnZoZpZqZrZsZtZuZvZwZxZyZzZœZæZßZfiZfl'+\
    u'The His She Her It Some Only It’s Also That There Is He She They Any Who Which You What Where To On As At We If Any This In One Are '+\
    u'After All How When Many My Do You Their ',

    # Capitals + Smallcaps
    u'/T/A.sc/T/B.sc/T/C.sc/T/D.sc/T/E.sc/T/F.sc/T/G.sc/T/H.sc/T/I.sc/T/J.sc/T/K.sc/T/L.sc/T/M.sc/T/N.sc/T/O.sc/T/P.sc/T/Q.sc/T/R.sc/T/S.sc'+\
    u'/T/T.sc/T/U.sc/T/V.sc/T/W.sc/T/X.sc/T/Y.sc/T/Z.sc/T/OE.sc/T/AE.sc/T/ß/T/F.sc/I.sc/T/F.sc/L.sc/V/A.sc/V/B.sc/V/C.sc/V/D.sc/V/E.sc/V/F.sc'+\
    u'/V/G.sc/V/H.sc/V/I.sc/V/J.sc/V/K.sc/V/L.sc/V/M.sc/V/N.sc/V/O.sc/V/P.sc/V/Q.sc/V/R.sc/V/S.sc/V/T.sc/V/U.sc/V/V.sc/V/W.sc/V/X.sc/V/Y.sc'+\
    u'/V/Z.sc/V/Œ.sc/V/AE.sc/V/ß/V/F.sc/I.sc/V/F.sc/L.sc/W/A.sc/W/B.sc/W/C.sc/W/D.sc/W/E.sc/W/F.sc/W/G.sc/W/H.sc/W/I.sc/W'+\
    u'/J.sc/W/K.sc/W/L.sc/W/M.sc/W/N.sc/W/O.sc/W/P.sc/W/Q.sc/W/R.sc/W/S.sc/W/T.sc/W/U.sc/W/V.sc/W/W.sc/W/X.sc/W/Y.sc/W/Z.sc/W/OE.sc/W/AE.sc'+\
    u'/W/ß/W/F.sc/I.sc/W/F.sc/L.sc/Y/A.sc/Y/B.sc/Y/C.sc/Y/D.sc/Y/E.sc/Y/F.sc/Y/G.sc/Y/H.sc/Y/I.sc/Y/J.sc/Y/K.sc/Y/L.sc/Y/M.sc/Y/N.sc/Y/O.sc'+\
    u'/Y/P.sc/Y/Q.sc/Y/R.sc/Y/S.sc/Y/T.sc/Y/U.sc/Y/V.sc/Y/W.sc/Y/X.sc/Y/Y.sc/Y/Z.sc/Y/OE.sc/Y/AE.sc/Y/ß/Y/F.sc/I.sc/Y/F.sc/L.sc/K/A.sc/K/B.sc'+\
    u'/K/C.sc/K/D.sc/K/E.sc/K/F.sc/K/G.sc/K/H.sc/K/I.sc/K/J.sc/K/K.sc/K/L.sc/K/M.sc/K/N.sc/K/O.sc/K/P.sc/K/Q.sc/K/R.sc/K/S.sc/K/T.sc'+\
    u'/K/U.sc/K/V.sc/K/W.sc/K/X.sc/K/Y.sc/K/Z.sc/R/A.sc/R/B.sc/R/C.sc/R/D.sc/R/E.sc/R/F.sc/R/G.sc/R/H.sc/R/I.sc/R/J.sc/R/K.sc/R/L.sc/R/M.sc'+\
    u'/R/N.sc/R/O.sc/R/P.sc/R/Q.sc/R/R.sc/R/S.sc/R/T.sc/R/U.sc/R/V.sc/R/W.sc/R/X.sc/R/Y.sc/R/Z.sc/J/A.sc/J/B.sc/J/C.sc/J/D.sc/J/E.sc/J/F.sc'+\
    u'/J/G.sc/J/H.sc/J/I.sc/J/J.sc/J/K.sc/J/L.sc/J/M.sc/J/N.sc/J/O.sc/J/P.sc/J/Q.sc/J/R.sc/J/S.sc/J/T.sc/J/U.sc/J/V.sc/J/W.sc/J/X.sc/J/Y.sc'+\
    u'/J/Z.sc/P/A.sc/P/B.sc/P/C.sc/P/D.sc/P/E.sc/P/F.sc/P/G.sc/P/H.sc/P/I.sc/P/J.sc/P/K.sc/P/L.sc/P/M.sc/P/N.sc/P/O.sc/P/P.sc/P/Q.sc/P/R.sc'+\
    u'/P/S.sc/P/T.sc/P/U.sc/P/V.sc/P/W.sc/P/X.sc/P/Y.sc/P/Z.sc/F/A.sc/F/B.sc/F/C.sc/F/D.sc/F/E.sc/F/F.sc/F/G.sc/F/H.sc/F/I.sc/F/J.sc/F/K.sc'+\
    u'/F/L.sc/F/M.sc/F/N.sc/F/O.sc/F/P.sc/F/Q.sc/F/R.sc/F/S.sc/F/T.sc/F/U.sc/F/V.sc/F/W.sc/F/X.sc/F/Y.sc/F/Z.sc/A/A.sc/A/B.sc/A/C.sc/A/D.sc'+\
    u'/A/E.sc/A/F.sc/A/G.sc/A/H.sc/A/I.sc/A/J.sc/A/K.sc/A/L.sc/A/M.sc/A/N.sc/A/O.sc/A/P.sc/A/Q.sc/A/R.sc/A/S.sc/A/T.sc/A/U.sc/A/V.sc/A/W.sc'+\
    u'/A/X.sc/A/Y.sc/A/Z.sc/A/OE.sc/A/AE.sc/A/ß/A/F.sc/I.sc/A/F.sc/L.sc/F/OE.sc/F/AE.sc/F/ß/F/F.sc/I.sc/F/F.sc/L.sc/K/OE.sc/K/AE.sc/K/ß/K'+\
    u'/F.sc/I.sc/K/F.sc/L.sc/P/OE.sc/P/AE.sc/P/ß/P/F.sc/I.sc/P/F.sc/L.sc/L/A.sc/L/B.sc/L/C.sc/L/D.sc/L/E.sc/L/F.sc/L/G.sc/L/H.sc/L/I.sc/L'+\
    u'/J.sc/L/K.sc/L/L.sc/L/M.sc/L/N.sc/L/O.sc/L/P.sc/L/Q.sc/L/R.sc/L/S.sc/L/T.sc/L/U.sc/L/V.sc/L/W.sc/L/X.sc/L/Y.sc/L/Z.sc/L/OE.sc/L/AE.sc'+\
    u'/L/ß/L/F.sc/I.sc/L/F.sc/L.sc/B/A.sc/B/B.sc/B/C.sc/B/D.sc/B/E.sc/B/F.sc/B/G.sc/B/H.sc/B/I.sc/B/J.sc/B/K.sc/B/L.sc/B/M.sc/B/N.sc/B/O.sc'+\
    u'/B/P.sc/B/Q.sc/B/R.sc/B/S.sc/B/T.sc/B/U.sc/B/V.sc/B/W.sc/B/X.sc/B/Y.sc/B/Z.sc/B/OE.sc/B/AE.sc/B/ß/B/F.sc/I.sc/B/F.sc/L.sc/R/OE.sc'+\
    u'/R/AE.sc/R/ß/R/F.sc/I.sc/R/F.sc/L.sc/S/A.sc/S/B.sc/S/C.sc/S/D.sc/S/E.sc/S/F.sc/S/G.sc/S/H.sc/S/I.sc/S/J.sc/S/K.sc/S/L.sc/S/M.sc/S/N.sc'+\
    u'/S/O.sc/S/P.sc/S/Q.sc/S/R.sc/S/S.sc/S/T.sc/S/U.sc/S/V.sc/S/W.sc/S/X.sc/S/Y.sc/S/Z.sc/S/OE.sc/S/AE.sc/S/ß/S/F.sc/I.sc/S/F.sc/L.sc/C/A.sc'+\
    u'/C/B.sc/C/C.sc/C/D.sc/C/E.sc/C/F.sc/C/G.sc/C/H.sc/C/I.sc/C/J.sc/C/K.sc/C/L.sc/C/M.sc/C/N.sc/C/O.sc/C/P.sc/C/Q.sc/C/R.sc/C/S.sc/C/T.sc'+\
    u'/C/U.sc/C/V.sc/C/W.sc/C/X.sc/C/Y.sc/C/Z.sc/C/OE.sc/C/AE.sc/C/ß/C/F.sc/I.sc/C/F.sc/L.sc/D/A.sc/D/B.sc/D/C.sc/D/D.sc/D/E.sc/D/F.sc/D/G.sc'+\
    u'/D/H.sc/D/I.sc/D/J.sc/D/K.sc/D/L.sc/D/M.sc/D/N.sc/D/O.sc/D/P.sc/D/Q.sc/D/R.sc/D/S.sc/D/T.sc/D/U.sc/D/V.sc/D/W.sc/D/X.sc/D/Y.sc/D/Z.sc'+\
    u'/D/OE.sc/D/AE.sc/D/ß/D/F.sc/I.sc/D/F.sc/L.sc/E/A.sc/E/B.sc/E/C.sc/E/D.sc/E/E.sc/E/F.sc/E/G.sc/E/H.sc/E/I.sc/E/J.sc/E/K.sc/E/L.sc/E/M.sc'+\
    u'/E/N.sc/E/O.sc/E/P.sc/E/Q.sc/E/R.sc/E/S.sc/E/T.sc/E/U.sc/E/V.sc/E/W.sc/E/X.sc/E/Y.sc/E/Z.sc/E/OE.sc/E/AE.sc/E/ß/E/F.sc/I.sc/E/F.sc/L.sc'+\
    u'/N/A.sc/N/B.sc/N/C.sc/N/D.sc/N/E.sc/N/F.sc/N/G.sc/N/H.sc/N/I.sc/N/J.sc/N/K.sc/N/L.sc/N/M.sc/N/N.sc/N/O.sc/N/P.sc/N/Q.sc/N/R.sc/N/S.sc'+\
    u'/N/T.sc/N/U.sc/N/V.sc/N/W.sc/N/X.sc/N/Y.sc/N/Z.sc/N/OE.sc/N/AE.sc/N/ß/N/F.sc/I.sc/N/F.sc/L.sc/G/A.sc/G/B.sc/G/C.sc/G/D.sc/G/E.sc/G/F.sc'+\
    u'/G/G.sc/G/H.sc/G/I.sc/G/J.sc/G/K.sc/G/L.sc/G/M.sc/G/N.sc/G/O.sc/G/P.sc/G/Q.sc/G/R.sc/G/S.sc/G/T.sc/G/U.sc/G/V.sc/G/W.sc/G/X.sc/G/Y.sc'+\
    u'/G/Z.sc/G/OE.sc/G/AE.sc/G/ß/G/F.sc/I.sc/G/F.sc/L.sc/O/A.sc/O/B.sc/O/C.sc/O/D.sc/O/E.sc/O/F.sc/O/G.sc/O/H.sc/O/I.sc/O/J.sc/O/K.sc/O/L.sc'+\
    u'/O/M.sc/O/N.sc/O/O.sc/O/P.sc/O/Q.sc/O/R.sc/O/S.sc/O/T.sc/O/U.sc/O/V.sc/O/W.sc/O/X.sc/O/Y.sc/O/Z.sc/O/OE.sc/O/AE.sc/O/ß/O/F.sc/I.sc/O/F.sc'+\
    u'/L.sc/Q/A.sc/Q/B.sc/Q/C.sc/Q/D.sc/Q/E.sc/Q/F.sc/Q/G.sc/Q/H.sc/Q/I.sc/Q/J.sc/Q/K.sc/Q/L.sc/Q/M.sc/Q/N.sc/Q/O.sc/Q/P.sc/Q/Q.sc/Q/R.sc/Q/S.sc'+\
    u'/Q/T.sc/Q/U.sc/Q/V.sc/Q/W.sc/Q/X.sc/Q/Y.sc/Q/Z.sc/Q/OE.sc/Q/AE.sc/Q/ß/Q/F.sc/I.sc/Q/F.sc/L.sc/H/A.sc/H/B.sc/H/C.sc/H/D.sc/H/E.sc/H/F.sc'+\
    u'/H/G.sc/H/H.sc/H/I.sc/H/J.sc/H/K.sc/H/L.sc/H/M.sc/H/N.sc/H/O.sc/H/P.sc/H/Q.sc/H/R.sc/H/S.sc/H/T.sc/H/U.sc/H/V.sc/H/W.sc/H/X.sc/H/Y.sc/H/Z.sc'+\
    u'/H/OE.sc/H/AE.sc/H/ß/H/F.sc/I.sc/H/F.sc/L.sc/I/A.sc/I/B.sc/I/C.sc/I/D.sc/I/E.sc/I/F.sc/I/G.sc/I/H.sc/I/I.sc/I/J.sc/I/K.sc/I/L.sc/I/M.sc'+\
    u'/I/N.sc/I/O.sc/I/P.sc/I/Q.sc/I/R.sc/I/S.sc/I/T.sc/I/U.sc/I/V.sc/I/W.sc/I/X.sc/I/Y.sc/I/Z.sc/I/OE.sc/I/AE.sc/I/ß/I/F.sc/I.sc/I/F.sc/L.sc'+\
    u'/J/OE.sc/J/AE.sc/J/ß/J/F.sc/I.sc/J/F.sc/L.sc/M/A.sc/M/B.sc/M/C.sc/M/D.sc/M/E.sc/M/F.sc/M/G.sc/M/H.sc/M/I.sc/M/J.sc/M/K.sc/M/L.sc/M/M.sc'+\
    u'/M/N.sc/M/O.sc/M/P.sc/M/Q.sc/M/R.sc/M/S.sc/M/T.sc/M/U.sc/M/V.sc/M/W.sc/M/X.sc/M/Y.sc/M/Z.sc/M/OE.sc/M/AE.sc/M/ß/M/F.sc/I.sc/M/F.sc/L.sc'+\
    u'/U/A.sc/U/B.sc/U/C.sc/U/D.sc/U/E.sc/U/F.sc/U/G.sc/U/H.sc/U/I.sc/U/J.sc/U/K.sc/U/L.sc/U/M.sc/U/N.sc/U/O.sc/U/P.sc/U/Q.sc/U/R.sc/U/S.sc/U'+\
    u'/T.sc/U/U.sc/U/V.sc/U/W.sc/U/X.sc/U/Y.sc/U/Z.sc/U/OE.sc/U/AE.sc/U/ß/U/F.sc/I.sc/U/F.sc/L.sc/X/A.sc/X/B.sc/X/C.sc/X/D.sc/X/E.sc/X/F.sc/X'+\
    u'/G.sc/X/H.sc/X/I.sc/X/J.sc/X/K.sc/X/L.sc/X/M.sc/X/N.sc/X/O.sc/X/P.sc/X/Q.sc/X/R.sc/X/S.sc/X/T.sc/X/U.sc/X/V.sc/X/W.sc/X/X.sc/X/Y.sc/X/Z.sc'+\
    u'/X/OE.sc/X/AE.sc/X/ß/X/F.sc/I.sc/X/F.sc/L.sc/Z/A.sc/Z/B.sc/Z/C.sc/Z/D.sc/Z/E.sc/Z/F.sc/Z/G.sc/Z/H.sc/Z/I.sc/Z/J.sc/Z/K.sc/Z/L.sc/Z/M.sc'+\
    u'/Z/N.sc/Z/O.sc/Z/P.sc/Z/Q.sc/Z/R.sc/Z/S.sc/Z/T.sc/Z/U.sc/Z/V.sc/Z/W.sc/Z/X.sc/Z/Y.sc/Z/Z.sc/Z/OE.sc/Z/AE.sc/Z/ß/Z/F.sc/I.sc/Z/F.sc/L.sc'+\
    u'/H.sc/E.sc/space/H/I.sc/S.sc/space/S/H.sc/E.sc/space/H/E.sc/R.sc/space/I/T.sc/space/S/O.sc/M.sc/E.sc/space/O/N.sc/L.sc/Y.sc/space/I/T.sc'+\
    u'/’/S.sc/space/A/L.sc/S.sc/O.sc/space/T/H.sc/A.sc/T.sc/space/T/H.sc/E.sc/R.sc/E.sc/space/I/S.sc/space/H/E.sc/space/S/H.sc/E.sc/space'+\
    u'/T/H.sc/E.sc/Y.sc /A/N.sc/Y.sc /W/H.sc/O.sc/space/W/H.sc/I.sc/C.sc/H.sc/space/Y/O.sc/U.sc/space/W/H.sc/A.sc/T.sc/space/W/H.sc/E.sc'+\
    u'/R.sc/E.sc/space/T/O.sc/space/O/N.sc/space/A/S.sc/space/A/T.sc/space/W/E.sc/space/I/F.sc/A/N.sc/Y.sc/space/T/H.sc/I.sc/S.sc/space/I'+\
    u'/N.sc/space/O/N.sc/E.sc/space/A/R.sc/E.sc/A/F.sc/T.sc/E.sc/R.sc/space/A/L.sc/L.sc/space/H/O.sc/W.sc/space/W/H.sc/E.sc/N.sc'+\
    u'/space/M/A.sc/N.sc/Y.sc/space/M/Y.sc/space/D/O.sc/space/Y/O.sc/U.sc/space/T/H.sc/E.sc/I.sc/R.sc',

    # Smallcaps
    u'/A.sc/A.sc/E.sc/A.sc/O.sc/A.sc/I.sc/A.sc/U.sc/A.sc/C.sc/A.sc/D.sc/A.sc/H.sc/A.sc/M.sc/A.sc/N.sc/A.sc/R.sc/A.sc/S.sc/A.sc/T.sc/A.sc/B.sc'+\
    u'/A.sc/G.sc/A.sc/F.sc/A.sc/L.sc/A.sc/P.sc/A.sc/V.sc/A.sc/W.sc/A.sc/Y.sc/A.sc/J.sc/A.sc/K.sc/A.sc/Q.sc/A.sc/X.sc/A.sc/Z.sc/A.sc/E.sc/E.sc'+\
    u'/O.sc/E.sc/I.sc/E.sc/U.sc/E.sc/C.sc/E.sc/D.sc/E.sc/H.sc/E.sc/M.sc/E.sc/N.sc/E.sc/R.sc/E.sc/S.sc/E.sc/T.sc/E.sc/B.sc/E.sc/G.sc/E.sc/F.sc'+\
    u'/E.sc/L.sc/E.sc/P.sc/E.sc/V.sc/E.sc/W.sc/E.sc/Y.sc/E.sc/J.sc/E.sc/K.sc/E.sc/Q.sc/E.sc/E.sc/X.sc/E.sc/Z.sc/E.sc/O.sc/O.sc/I.sc/O.sc/U.sc'+\
    u'/O.sc/C.sc/O.sc/D.sc/O.sc/H.sc/O.sc/M.sc/O.sc/N.sc/O.sc/R.sc/O.sc/S.sc/O.sc/T.sc/O.sc/B.sc/O.sc/G.sc/O.sc/F.sc/O.sc/L.sc'+\
    u'/O.sc/P.sc/O.sc/V.sc/O.sc/W.sc/O.sc/Y.sc/O.sc/J.sc/O.sc/K.sc/O.sc/Q.sc/O.sc/X.sc/O.sc/Z.sc/O.sc/I.sc/I.sc/U.sc/I.sc/C.sc/I.sc/D.sc/I.sc'+\
    u'/H.sc/I.sc/M.sc/I.sc/N.sc/I.sc/R.sc/I.sc/S.sc/I.sc/T.sc/I.sc/B.sc/I.sc/G.sc/I.sc/F.sc/I.sc/L.sc/I.sc/P.sc/I.sc/V.sc/I.sc/W.sc/I.sc/Y.sc'+\
    u'/I.sc/J.sc/I.sc/K.sc/I.sc/Q.sc/I.sc/X.sc/I.sc/Z.sc/I.sc/U.sc/U.sc/C.sc/U.sc/D.sc/U.sc/H.sc/U.sc/M.sc/U.sc/N.sc/U.sc/R.sc/U.sc/S.sc/U.sc'+\
    u'/T.sc/U.sc/B.sc/U.sc/G.sc/U.sc/F.sc/U.sc/L.sc/U.sc/P.sc/U.sc/V.sc/U.sc/W.sc/U.sc/Y.sc/U.sc/J.sc/U.sc/K.sc/U.sc/Q.sc/U.sc/X.sc/U.sc/Z.sc'+\
    u'/U.sc/C.sc/C.sc/D.sc/C.sc/H.sc/C.sc/M.sc/C.sc/N.sc/C.sc/R.sc/C.sc/S.sc/C.sc/T.sc/C.sc/B.sc/C.sc/G.sc/C.sc/F.sc/C.sc/L.sc'+\
    u'/C.sc/P.sc/C.sc/V.sc/C.sc/W.sc/C.sc/Y.sc/C.sc/J.sc/C.sc/K.sc/C.sc/Q.sc/C.sc/X.sc/C.sc/Z.sc/C.sc/D.sc/D.sc/H.sc/D.sc/M.sc/D.sc/N.sc/D.sc'+\
    u'/R.sc/D.sc/S.sc/D.sc/T.sc/D.sc/B.sc/D.sc/G.sc/D.sc/F.sc/D.sc/L.sc/D.sc/P.sc/D.sc/V.sc/D.sc/W.sc/D.sc/Y.sc/D.sc/J.sc/D.sc/K.sc/D.sc/Q.sc'+\
    u'/D.sc/X.sc/D.sc/Z.sc/D.sc/H.sc/H.sc/M.sc/H.sc/N.sc/H.sc/R.sc/H.sc/S.sc/H.sc/T.sc/H.sc/B.sc/H.sc/G.sc/H.sc/F.sc/H.sc/L.sc/H.sc/P.sc/H.sc'+\
    u'/V.sc/H.sc/W.sc/H.sc/Y.sc/H.sc/J.sc/H.sc/K.sc/H.sc/Q.sc/H.sc/X.sc/H.sc/Z.sc/H.sc/M.sc/M.sc/M.sc/N.sc/M.sc/R.sc/M.sc/S.sc/M.sc/T.sc/M.sc'+\
    u'/B.sc/M.sc/G.sc/M.sc/F.sc/M.sc/L.sc/M.sc/P.sc/M.sc/V.sc/M.sc/W.sc/M.sc/Y.sc/M.sc/J.sc/M.sc/K.sc/M.sc/Q.sc/M.sc/X.sc/M.sc'+\
    u'/Z.sc/M.sc/N.sc/N.sc/R.sc/N.sc/S.sc/N.sc/T.sc/N.sc/B.sc/N.sc/G.sc/N.sc/F.sc/N.sc/L.sc/N.sc/P.sc/N.sc/V.sc/N.sc/W.sc/N.sc/Y.sc/N.sc/J.sc'+\
    u'/N.sc/K.sc/N.sc/Q.sc/N.sc/X.sc/N.sc/Z.sc/N.sc/R.sc/R.sc/S.sc/R.sc/T.sc/R.sc/B.sc/R.sc/G.sc/R.sc/F.sc/R.sc/L.sc/R.sc/P.sc/R.sc/V.sc/R.sc'+\
    u'/W.sc/R.sc/Y.sc/R.sc/J.sc/R.sc/K.sc/R.sc/Q.sc/R.sc/X.sc/R.sc/Z.sc/R.sc/S.sc/S.sc/T.sc/S.sc/B.sc/S.sc/G.sc/S.sc/F.sc/S.sc/L.sc/S.sc/P.sc'+\
    u'/S.sc/V.sc/S.sc/W.sc/S.sc/Y.sc/S.sc/J.sc/S.sc/K.sc/S.sc/Q.sc/S.sc/X.sc/S.sc/Z.sc/S.sc/T.sc/T.sc/B.sc/T.sc/G.sc/T.sc/F.sc/T.sc/L.sc/T.sc'+\
    u'/P.sc/T.sc/V.sc/T.sc/W.sc/T.sc/Y.sc/T.sc/J.sc/T.sc/K.sc/T.sc/Q.sc/T.sc/X.sc/T.sc/Z.sc/T.sc/B.sc/B.sc/G.sc/B.sc/F.sc/B.sc'+\
    u'/L.sc/B.sc/P.sc/B.sc/V.sc/B.sc/W.sc/B.sc/Y.sc/B.sc/J.sc/B.sc/K.sc/B.sc/Q.sc/B.sc/X.sc/B.sc/Z.sc/B.sc/G.sc/G.sc/F.sc/G.sc/L.sc/G.sc/P.sc'+\
    u'/G.sc/V.sc/G.sc/W.sc/G.sc/Y.sc/G.sc/J.sc/G.sc/K.sc/G.sc/Q.sc/G.sc/X.sc/G.sc/Z.sc/G.sc/F.sc/F.sc/L.sc/F.sc/P.sc/F.sc/V.sc/F.sc/W.sc/F.sc'+\
    u'/Y.sc/F.sc/J.sc/F.sc/K.sc/F.sc/Q.sc/F.sc/X.sc/F.sc/Z.sc/F.sc/L.sc/L.sc/P.sc/L.sc/V.sc/L.sc/W.sc/L.sc/Y.sc/L.sc/J.sc/L.sc/K.sc/L.sc/L.sc'+\
    u'/Q.sc/L.sc/X.sc/L.sc/Z.sc/L.sc/P.sc/P.sc/V.sc/P.sc/W.sc/P.sc/Y.sc/P.sc/J.sc/P.sc/K.sc/P.sc/Q.sc/P.sc/P.sc/X.sc/P.sc/Z.sc/P.sc/V.sc/V.sc'+\
    u'/W.sc/V.sc/Y.sc/V.sc/J.sc/V.sc/K.sc/V.sc/Q.sc/V.sc/X.sc/V.sc/Z.sc/V.sc/Y.sc/Y.sc/W.sc/Y.sc/Y.sc/Y.sc/J.sc/Y.sc/K.sc/Y.sc'+\
    u'/Q.sc/Y.sc/X.sc/Y.sc/Z.sc/Y.sc/J.sc/J.sc/K.sc/J.sc/Q.sc/J.sc/X.sc/J.sc/Z.sc/J.sc/K.sc/K.sc/K.sc/Q.sc/K.sc/X.sc/K.sc/Z.sc/K.sc/Q.sc/Q.sc'+\
    u'/X.sc/Q.sc/Z.sc/Q.sc/X.sc/X.sc/Z.sc/X.sc/Z.sc/Z.sc/A.sc/A.sc/E.sc/A.sc/O.sc/A.sc/I.sc/A.sc/U.sc/A.sc/C.sc/A.sc/D.sc/A.sc/H.sc/A.sc/M.sc'+\
    u'/A.sc/N.sc/A.sc/R.sc/A.sc/A.sc/S.sc/A.sc/T.sc/A.sc/B.sc/A.sc/G.sc/A.sc/F.sc/A.sc/L.sc/A.sc/P.sc/A.sc/V.sc/A.sc/W.sc/A.sc/Y.sc/A.sc/J.sc'+\
    u'/A.sc/K.sc/A.sc/Q.sc/A.sc/X.sc/A.sc/E.sc/A.sc/Z.sc/A.sc/E.sc/E.sc/O.sc/E.sc/I.sc/E.sc/U.sc/E.sc/C.sc/E.sc/D.sc/E.sc/H.sc/E.sc/M.sc/E.sc'+\
    u'/N.sc/E.sc/R.sc/E.sc/S.sc/E.sc/T.sc/E.sc/B.sc/E.sc/G.sc/E.sc/F.sc/E.sc/L.sc/E.sc/P.sc/E.sc/V.sc/E.sc/W.sc/E.sc/Y.sc/E.sc'+\
    u'/J.sc/E.sc/K.sc/E.sc/Q.sc/E.sc/E.sc/X.sc/E.sc/Z.sc/E.sc/O.sc/O.sc/I.sc/O.sc/U.sc/O.sc/C.sc/O.sc/D.sc/O.sc/H.sc/O.sc/M.sc/O.sc/N.sc/O.sc'+\
    u'/R.sc/O.sc/O.sc/S.sc/O.sc/T.sc/O.sc/B.sc/O.sc/G.sc/O.sc/F.sc/O.sc/L.sc/O.sc/P.sc/O.sc/V.sc/O.sc/W.sc/O.sc/Y.sc/O.sc/J.sc/O.sc/K.sc/O.sc'+\
    u'/Q.sc/O.sc/O.sc/X.sc/O.sc/Z.sc/O.sc/I.sc/I.sc/U.sc/I.sc/C.sc/I.sc/D.sc/I.sc/H.sc/I.sc/M.sc/I.sc/N.sc/I.sc/R.sc/I.sc/S.sc/I.sc/I.sc/T.sc'+\
    u'/I.sc/B.sc/I.sc/G.sc/I.sc/F.sc/I.sc/L.sc/I.sc/P.sc/I.sc/V.sc/I.sc/W.sc/I.sc/Y.sc/I.sc/J.sc/I.sc/K.sc/I.sc/Q.sc/I.sc/X.sc/I.sc/Z.sc/I.sc'+\
    u'/U.sc/U.sc/C.sc/U.sc/D.sc/U.sc/H.sc/U.sc/M.sc/U.sc/N.sc/U.sc/R.sc/U.sc/S.sc/U.sc/T.sc/U.sc/U.sc/B.sc/U.sc/G.sc/U.sc/F.sc'+\
    u'/U.sc/L.sc/U.sc/P.sc/U.sc/V.sc/U.sc/W.sc/U.sc/Y.sc/U.sc/J.sc/U.sc/K.sc/U.sc/Q.sc/U.sc/X.sc/U.sc/Z.sc/U.sc/C.sc/C.sc/C.sc/D.sc/C.sc/H.sc'+\
    u'/C.sc/M.sc/C.sc/N.sc/C.sc/R.sc/C.sc/S.sc/C.sc/T.sc/C.sc/B.sc/C.sc/G.sc/C.sc/F.sc/C.sc/L.sc/C.sc/C.sc/P.sc/C.sc/V.sc/C.sc/W.sc/C.sc/Y.sc'+\
    u'/C.sc/J.sc/C.sc/K.sc/C.sc/Q.sc/C.sc/X.sc/C.sc/Z.sc/C.sc/D.sc/D.sc/H.sc/D.sc/M.sc/D.sc/N.sc/D.sc/D.sc/R.sc/D.sc/S.sc/D.sc/T.sc/D.sc/B.sc'+\
    u'/D.sc/G.sc/D.sc/F.sc/D.sc/L.sc/D.sc/P.sc/D.sc/V.sc/D.sc/W.sc/D.sc/Y.sc/D.sc/J.sc/D.sc/D.sc/K.sc/D.sc/Q.sc/D.sc/X.sc/D.sc/Z.sc/D.sc/H.sc'+\
    u'/H.sc/M.sc/H.sc/N.sc/H.sc/R.sc/H.sc/S.sc/H.sc/T.sc/H.sc/B.sc/H.sc/G.sc/F.sc/H.sc/L.sc/H.sc/P.sc/H.sc/V.sc/H.sc/W.sc/H.sc'+\
    u'/Y.sc/H.sc/J.sc/H.sc/K.sc/H.sc/Q.sc/H.sc/X.sc/H.sc/Z.sc/H.sc/M.sc/M.sc/N.sc/M.sc/R.sc/M.sc/S.sc/M.sc/T.sc/M.sc/B.sc/M.sc/G.sc/M.sc/F.sc'+\
    u'/M.sc/L.sc/M.sc/P.sc/M.sc/V.sc/M.sc/W.sc/M.sc/Y.sc/M.sc/M.sc/J.sc/M.sc/K.sc/M.sc/Q.sc/M.sc/X.sc/M.sc/Z.sc/M.sc/N.sc/N.sc/R.sc/N.sc/S.sc'+\
    u'/N.sc/T.sc/N.sc/B.sc/N.sc/G.sc/N.sc/F.sc/N.sc/L.sc/N.sc/P.sc/N.sc/V.sc/N.sc/W.sc/N.sc/Y.sc/N.sc/J.sc/N.sc/K.sc/N.sc/Q.sc/N.sc/X.sc/N.sc'+\
    u'/Z.sc/N.sc/R.sc/R.sc/S.sc/R.sc/R.sc/T.sc/R.sc/B.sc/R.sc/G.sc/R.sc/F.sc/R.sc/L.sc/R.sc/P.sc/R.sc/V.sc/R.sc/W.sc/R.sc/Y.sc/R.sc/J.sc/R.sc'+\
    u'/K.sc/R.sc/R.sc/Q.sc/R.sc/X.sc/R.sc/Z.sc/R.sc/S.sc/S.sc/T.sc/S.sc/B.sc/S.sc/G.sc/S.sc/F.sc/S.sc/L.sc/S.sc/P.sc/S.sc/V.sc'+\
    u'/S.sc/W.sc/S.sc/Y.sc/S.sc/S.sc/J.sc/S.sc/K.sc/S.sc/Q.sc/S.sc/X.sc/S.sc/Z.sc/S.sc/T.sc/T.sc/B.sc/T.sc/G.sc/T.sc/F.sc/T.sc/L.sc/T.sc/P.sc'+\
    u'/T.sc/V.sc/T.sc/W.sc/T.sc/T.sc/Y.sc/T.sc/J.sc/T.sc/K.sc/T.sc/Q.sc/T.sc/X.sc/T.sc/Z.sc/T.sc/B.sc/B.sc/G.sc/B.sc/F.sc/B.sc/L.sc/B.sc/P.sc'+\
    u'/B.sc/B.sc/V.sc/B.sc/W.sc/B.sc/Y.sc/B.sc/J.sc/B.sc/K.sc/B.sc/Q.sc/B.sc/X.sc/B.sc/Z.sc/B.sc/G.sc/G.sc/F.sc/G.sc/L.sc/G.sc/P.sc/G.sc/G.sc'+\
    u'/V.sc/G.sc/W.sc/G.sc/Y.sc/G.sc/J.sc/G.sc/K.sc/G.sc/Q.sc/G.sc/X.sc/G.sc/Z.sc/G.sc/F.sc/F.sc/L.sc/F.sc/P.sc/F.sc/V.sc/F.sc/F.sc/W.sc/F.sc'+\
    u'/Y.sc/F.sc/J.sc/F.sc/K.sc/F.sc/Q.sc/F.sc/X.sc/F.sc/Z.sc/F.sc/L.sc/L.sc/P.sc/L.sc/V.sc/L.sc/W.sc/L.sc/Y.sc/L.sc/J.sc/L.sc'+\
    u'/L.sc/K.sc/L.sc/Q.sc/L.sc/X.sc/L.sc/Z.sc/L.sc/P.sc/P.sc/V.sc/P.sc/W.sc/P.sc/Y.sc/P.sc/J.sc/P.sc/K.sc/P.sc/Q.sc/P.sc/P.sc/X.sc/P.sc/Z.sc'+\
    u'/P.sc/V.sc/V.sc/W.sc/V.sc/Y.sc/V.sc/J.sc/V.sc/K.sc/V.sc/Q.sc/V.sc/X.sc/V.sc/Z.sc/V.sc/Y.sc/Y.sc/W.sc/Y.sc/Y.sc/Y.sc/J.sc/Y.sc/K.sc/Y.sc'+\
    u'/Q.sc/Y.sc/X.sc/Y.sc/Z.sc/Y.sc/J.sc/J.sc/K.sc/J.sc/Q.sc/J.sc/X.sc/J.sc/Z.sc/J.sc/K.sc/K.sc/K.sc/Q.sc/K.sc/K.sc/X.sc/K.sc/Z.sc/K.sc/Q.sc'+\
    u'/Q.sc/X.sc/Q.sc/Z.sc/Q.sc/X.sc/X.sc/Z.sc/X.sc/Z.sc/Z.sc'+\
    u'/H.sc/E.sc/space/I.sc/S.sc/ /B.sc/U.sc/T.sc/space/A.sc/N.sc/space/I.sc/T.sc/space/A.sc/T.sc/space/T.sc/H.sc/E.sc/space/S.sc/H.sc/E.sc/space/D.sc/O.sc/space/O.sc/N.sc/space'+\
    u'/H.sc/I.sc/S.sc/space/N.sc/O.sc/T.sc/space/L.sc/I.sc/K.sc/E.sc/space/O.sc/F.sc/space/T.sc/H.sc/E.sc/M.sc/ /A.sc/R.sc/E.sc/ /A.sc/S.sc/space/T.sc/H.sc/E.sc/Y.sc/space'+\
    u'/C.sc/A.sc/N.sc/space/B.sc/O.sc/T.sc/H.sc/space/B.sc/E.sc/space/F.sc/O.sc/R.sc/space/O.sc/R.sc/space/B.sc/E.sc/space/I.sc/N.sc/space/W.sc/I.sc/T.sc/H.sc/space/H.sc/I.sc/S.sc/space'+\
    u'/T.sc/O.sc/O.sc/space/I.sc/N.sc/space/F.sc/R.sc/O.sc/M.sc/space/W.sc/E.sc/R.sc/E.sc/space/B.sc/Y.sc/space/O.sc/N.sc/L.sc/Y.sc/space/S.sc/O.sc/M.sc/E.sc/space'+\
    u'/H.sc/E.sc/R.sc/space/H.sc/A.sc/V.sc/E.sc/space/T.sc/O.sc/space/A.sc/F.sc/T.sc/E.sc/R.sc/space/T.sc/H.sc/A.sc/T.sc/space/T.sc/H.sc/A.sc/N.sc/space'+\
    u'/W.sc/H.sc/I.sc/C.sc/H.sc/space/Y.sc/O.sc/U.sc/space/A.sc/L.sc/S.sc/O.sc/space/H.sc/A.sc/D.sc/space/E.sc/I.sc/T.sc/H.sc/E.sc/R.sc/.',

    # Figures and exceptions
    u'010203040506070809000.0,0;0:00<0>0=0+0$000£000¥000ƒ000#000§000¶000000%000‰000¢000ª000º112131415161718191011.1,1;1:1<1>1=1+1$100£100¥'+\
    u'100ƒ100#100§100¶100001%001‰001¢001ª001º212232425262728292022.2,2;2:22<2>2=2+2$200£200¥200ƒ200#200§200¶200002%002‰002¢002ª002º3132334'+\
    u'35363738393033.3,3;3:33<3>3=3+3$300£300¥300ƒ300#300§300¶300003%003‰003¢003ª003º414243445464748494044.4,4;4:44<4>4=4+4$400£400¥400ƒ40'+\
    u'0#400§400¶400004%004‰004¢004ª004º515253545565758595055.5,5;5:55<5>5=5+5$500£500¥500ƒ500#500§500¶500005%005‰005¢005ª005º6162636465667'+\
    u'68696066.6,6;6:66<6>6=6+6$600£600¥600ƒ600#600§600¶600006%006‰006¢006ª006º717273747576778797077.7,7;7:77<7>7=7+7$700£700¥700ƒ700#700§'+\
    u'700¶700007%007‰007¢007ª007º818283848586878898088.8,8;8:88<8>8=8+8$800£800¥800ƒ800#800§800¶800008%008‰008¢008ª008º9192939495969798990'+\
    u'99.9,9;9:9<9>9=9+9$900£900¥900ƒ900#900§900¶900009%009‰009¢009ª009º0/slash/one/slash/two/slash/three/slash/four/slash/five/slash/six/slash/seven/slash/eight/slash/nine/slash/zero/slash .a.b.c.d.e.f.g.h.i.j.k.'+\
    u'l.m.n.o.p.q.r.s.t.u.v.w.x.y.z.,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/'+\
    u'y/z/\\a\\b\\c\\d\\e\\f\\g\\h\\i\\j\\k\\l\\m\\n\\o\\p\\q\\r\\s\\t\\u\\v\\w\\x\\y\\z\\a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z:a;b;c;d;e;f;g;h;i;j;k;l'+\
    u';m;n;o;p;q;r;s;t;u;v;w;x;y;z;¡a!¡b!¡c!¡d!¡e!¡f!¡g!¡h!¡i!¡j!¡k!¡l!¡m!¡n!¡o!¡p!¡q!¡r!¡s!¡t!¡u!¡v!¡w!¡x!¡y!¡z!¿a?¿b?¿c?¿d?¿e?¿f?¿g?¿h?¿'+\
    u'i?¿j?¿k?¿l?¿m?¿n?¿o?¿p?¿q?¿r?¿s?¿t?¿u?¿v?¿w?¿x?¿y?¿z?(a)(b)(c)(d)(e)(f)(g)(h)(i)(j)(k)(l)(m)(n)(o)(p)(q)(r)(s)(t)(u)(v)(w)(x)(y)(z)['+\
    u'a][b][c][d][e][f][g][h][i][j][k][l][m][n][o][p][q][r][s][t][u][v][w][x][y][z]{a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n}{o}{p}{q}{r}{'+\
    u's}{t}{u}{v}{w}{x}{y}{z}“a”“b”“c”“d”“e”“f”“g”“h”“i”“j”“k”“l”“m”“n”“o”“p”“q”“r”“s”“t”“u”“v”“w”“x”“y”“z”‘a’‘b’‘c’‘d’‘e’‘f’‘g’‘h’‘i’‘j’‘'+\
    u'k’‘l’‘m’‘n’‘o’‘p’‘q’‘r’‘s’‘t’‘u’‘v’‘w’‘x’‘y’‘z’’a’b’c’d’e’f’g’h’i’j’k’l’m’n’o’p’q’r’s’t’u’v’w’x’y’z’«a»«b»«c»«d»«e»«f»«g»«h»«i»«j»«k'+\
    u'»«l»«m»«n»«o»«p»«q»«r»«s»«t»«u»«v»«w»«x»«y»«z»‹a›‹b›‹c›‹d›‹e›‹f›‹g›‹h›‹i›‹j›‹k›‹l›‹m›‹n›‹o›‹p›‹q›‹r›‹s›‹t›‹u›‹v›‹w›‹x›‹y›‹z›»a«»b«»c'+\
    u'«»d«»e«»f«»g«»h«»i«»j«»k«»l«»m«»n«»o«»p«»q«»r«»s«»t«»u«»v«»w«»x«»y«»z«›a‹›b‹›c‹›d‹›e›f‹›g‹›h‹›i‹›j‹›k‹›l‹›m‹›n‹›o‹›p‹›q‹›r‹›s‹›t‹›u‹'+\
    u'›v‹›w‹›x‹›y‹›z‹*a*b*c*d*e*f*g*h*i*j*k*l*m*n*o*p**q*r*s*t*u*v*w*x*y*z*®a®b®c®d®e®f®g®h®i®j®k®l®m®n®o®p®q®r®s®t®u®v®w®x®y®z®™a™b™c™d™e'+\
    u'™f™g™h™i™j™k™l™m™n™o™p™q™r™s™t™u™v™w™x™y™z™&a@a@b@c@d@e@f@g@h@i@j@k@l@m@n@o@p@q@r@s@t@u@v@w@x@y@z@-a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q'+\
    u'-r-s-t-u-v-w-x-y-z--a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z-æaæbæcædææeæfægæhæiæjækælæmænæoææpæqæræsætæuævæwæxæyæzæœaœbœ'+\
    u'cœdœeœfœgœhœiœjœkœlœmœœnœoœpœqœrœsœtœuœvœwœxœyœzœßaßbßcßdßeßfßgßhßißjßkßßlßmßnßoßpßqßrßsßtßußvßwßxßyßzß .A.B.C.D.E.F.G.H.I.J.K.L.M.N'+\
    u'.O.P.Q.R.S.T.U.V.W.X.Y.Z.,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,/slash/A/slash/B/slash/C/slash/D/slash/E/slash/F/slash/G/slash/H/slash/I/slash/J/slash/K/slash/L/slash/M/slash/N/slash/O/slash/P/slash/Q/slash/R/slash/S/slash/T/slash/U/slash/V/slash/W/slash/X/slash/Y/slash/Z/slash/\\A'+\
    u'\\B\\C\\D\\E\\F\\G\\H\\I\\J\\K\\L\\M\\N\\O\\P\\Q\\R\\S\\T\\U\\V\\W\\X\\Y\\Z\\A:B:C:D:E:F:G:H:I:J:K:L:M:N:O:P:Q:R:S:T:U:V:W:X:Y:Z:A;B;C;D;E;F;G;H;I;J;K;L;M;N;O'+\
    u';P;Q;R;S;T;U;V;W;X;Y;Z;¡A!¡B!¡C!¡D!¡E!¡F!¡G!¡H!¡I!¡J!¡K!¡L!¡M!¡N!¡O!¡P!¡Q!¡R!¡S!¡T!¡U!¡V!¡W!¡X!¡Y!¡Z!¿A?¿B?¿C?¿D?¿E?¿F?¿G?¿H?¿I?¿J?'+\
    u'¿K?¿L?¿M?¿N?¿O?¿P?¿Q?¿R?¿S?¿T?¿U?¿V?¿W?¿X?¿Y?¿Z?(A)(B)(C)(D)(E)(F)(G)(H)(I)(J)(K)(L)(M)(N)(O)(P)(Q)(R)(S)(T)(U)(V)(W)(X)(Y)(Z)[A][B'+\
    u'][C][D][E][F][G][H][I][J][K][L][M][N][O][P][Q][R][S][T][U][V][W][X][Y][Z]{A}{B}{C}{D}{E}{F}{G}{H}{I}{J}{K}{L}{M}{N}{O}{P}{Q}{R}{S}{T'+\
    u'}{U}{V}{W}{X}{Y}{Z}“A”“B”“C”“D”“E”“F”“G”“H”“I”“J”“K”“L”“M”“N”“O”“P”“Q”“R”“S”“T”“U”“V”“W”“X”“Y”“Z”‘A’‘B’‘C’‘D’‘E’‘F’‘G’‘H’‘I’‘J’‘K’‘L'+\
    u'’‘M’‘N’‘O’‘P’‘Q’‘R’‘S’‘T’‘U’‘V’‘W’‘X’‘Y’‘Z’’A’B’C’D’E’F’G’H’I’J’K’L’M’N’O’P’Q’R’S’T’U’V’W’X’Y’Z’«A»«B»«C»«D»«E»«F»«G»«H»«I»«J»«K»«L»«'+\
    u'M»«N»«O»«P»«Q»«R»«S»«T»«U»«V»«W»«X»«Y»«Z»‹A›‹B›‹C›‹D›‹E›‹F›‹G›‹H›‹I›‹J›‹K›‹L›‹M›‹N›‹O›‹P›‹Q›‹R›‹S›‹T›‹U›‹V›‹W›‹X›‹Y›‹Z›»A«»B«»C«»D«»E'+\
    u'«»F«»G«»H«»I«»J«»K«»L«»M«»N«»O«»P«»Q«»R«»S«»T«»U«»V«»W«»X«»Y«»Z«›A‹›B‹›C‹›D‹›E›F‹›G‹›H‹›I‹›J‹›K‹›L‹›M‹›N‹›O‹›P‹›Q‹›R‹›S‹›T‹›U‹›V‹›W‹›'+\
    u'X‹›Y‹›Z‹*A*B*C*D*E*F*G*H*I*J*K*L*M*N*O*P**Q*R*S*T*U*V*W*X*Y*Z*®A®B®C®D®E®F®G®H®I®J®K®L®M®N®O®P®Q®R®S®T®U®V®W®X®Y®Z®™A™B™C™D™E™F™G™H™I'+\
    u'™J™K™L™M™N™O™P™Q™R™S™T™U™V™W™X™Y™Z™&A@A@B@C@D@E@F@G@H@I@J@K@L@M@N@O@P@Q@R@S@T@U@V@W@X@Y@Z@-A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-'+\
    u'V-W-X-Y-Z--A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-V-W-X-Y-Z-æAæBæCæDææEæFæGæHæIæJæKæLæMæNæOææPæQæRæSæTæUæVæWæXæYæZæœAœBœCœDœEœFœGœ'+\
    u'HœIœJœKœLœMœœNœOœPœQœRœSœTœUœVœWœXœYœZœßAßBßCßDßEßFßGßHßIßJßKßßLßMßNßOßPßQßRßSßTßUßVßWßXßYßZß “¿Que?” “¡Que!” “nn.” “nn,” “nn”. “nn”,  Fin.'
)
CYRILLIC_SLAVIC_TEXT = (
    u"Russian Sample (pangrams) "+\
    u"Подъём с затонувшего эсминца легко бьющейся древнегреческой амфоры сопряжён с техническими трудностями. Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций. Шалящий фавн прикинул объём горячих звезд этих вьюжных царств. Эх, жирафы честно в цель шагают, да щук объять за память ёлкой... Расчешись! Объявляю: туфли у камина, где этот хищный ёж цаплю задел. Съел бы ёж лимонный пьезокварц, где электрическая юла яшму с туфом похищает. Съел бы ёж лимонный пьезокварц, где электрическая юла яшму с туфом похищает. Эти ящерицы чешут вперёд за ключом, но багаж в сейфах, поди подъедь... Эх, взъярюсь, толкну флегматика: «Дал бы щец жарчайших, Пётр!» Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд. Художник-эксперт с компьютером всего лишь яйца в объёмный низкий ящик чохом фасовал. Юный директор целиком сжевал весь объём продукции фундука (товара дефицитного и деликатесного), идя энергично через хрустящий камыш. Мюзикл-буфф «Огнедышащий простужается ночью». Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка. Безмозглый широковещательный цифровой передатчик сужающихся экспонент. Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду. Вопрос футбольных энциклопедий замещая чушью: эй, где съеден ёж? Борец за идею Чучхэ выступил с гиком, шумом, жаром и фырканьем на съезде — и в ящик. Твёрдый, как ъ, но и мягкий, словно ь, юноша из Бухары ищет фемину-москвичку для просмотра цветного экрана жизни. Пиши: зять съел яйцо, ещё чан брюквы... эх! Ждем фигу! Флегматичная эта верблюдица жует у подъезда засыхающий горький шиповник. Подъехал шофёр на рефрижераторе грузить яйца для обучающихся элитных медиков. Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства. Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!\n"+\
    u"ЛИНГВИСТЫ В УЖАСЕ: ФИГ ВЫГОВОРИШЬ ЭТЮД: «ПОДЪЁМ ЧЕЛЯБИНСКИЙ, ЗАПАХ ЩЕЦ». ВСЁ УСКОРЯЮЩАЯСЯ ЭВОЛЮЦИЯ КОМПЬЮТЕРНЫХ ТЕХНОЛОГИЙ ПРЕДЪЯВИЛА ЖЁСТКИЕ ТРЕБОВАНИЯ К ПРОИЗВОДИТЕЛЯМ КАК СОБСТВЕННО ВЫЧИСЛИТЕЛЬНОЙ ТЕХНИКИ, ТАК И ПЕРИФЕРИЙНЫХ УСТРОЙСТВ. ШАЛЯЩИЙ ФАВН ПРИКИНУЛ ОБЪЁМ ГОРЯЧИХ ЗВЕЗД ЭТИХ ВЬЮЖНЫХ ЦАРСТВ. ЭХ, ЖИРАФЫ ЧЕСТНО В ЦЕЛЬ ШАГАЮТ, ДА ЩУК ОБЪЯТЬ ЗА ПАМЯТЬ ЁЛКОЙ... ЭКС-ГРАФ? ПЛЮШ ИЗЪЯТ. БЬЁМ ЧУЖДЫЙ ЦЕН ХВОЩ! ЭЙ, ЖЛОБ! ГДЕ ТУЗ? ПРЯЧЬ ЮНЫХ СЪЁМЩИЦ В ШКАФ. ЛЮБЯ, СЪЕШЬ ЩИПЦЫ, — ВЗДОХНЁТ МЭР, — КАЙФ ЖГУЧ. ЮЖНО-ЭФИОПСКИЙ ГРАЧ УВЁЛ МЫШЬ ЗА ХОБОТ НА СЪЕЗД ЯЩЕРИЦ. АЭРОФОТОСЪЁМКА ЛАНДШАФТА УЖЕ ВЫЯВИЛА ЗЕМЛИ БОГАЧЕЙ И ПРОЦВЕТАЮЩИХ КРЕСТЬЯН. ШИФРОВАЛЬЩИЦА ПОПРОСТУ ЗАБЫЛА РЯД КЛЮЧЕВЫХ МНОЖИТЕЛЕЙ И ТЭГОВ.",

    u"Ukrainian Sample (pangrams) "+\
    u"Чуєш їх, доцю, га? Кумедна ж ти, прощайся без ґольфів! Жебракують філософи при ґанку церкви в Гадячі, ще й шатро їхнє п’яне знаємо.\n",
    u"Sample (text) "+\
    u"Для запису української мови використовують адаптовану кирилицю («гражданка»), зрідка — латинку в різних варіантах. Правила української мови регулює Національна академія наук України, зокрема Інститут української мови НАНУ (історія, граматика, лексикологія, термінологія, ономастика, стилістика та культура мови, діалектологія, соціолінгвістика), Український мовно-інформаційний фонд НАНУ (комп'ютерна лінгвістика, словники), Інститут мовознавства ім. О. О. Потебні НАНУ (українська мова у зв'язках з іншими мовами). Щороку 9 листопада в Україні відзначають День української писемності та мови.\n"\
    u"Фрідріх Штовассер народився 1928 року в родині австрійського інженера Ернста Штовассера та Ельзи Штовассер. Його батько помер від апендициту коли Гундертвассеру було лише рік, відтак його вихованням опікувалася мати. Під час навчання у школі Монтессорі у Відні вчителі відзначали у хлопця «незвичайне відчуття фарб та форм». 1935 року Гундервассера охрестили як католика, незважаючи на те, що його мати була єврейкою. Після аншлюсу Австрії до нацистської Німеччини Гундертвассер 1938 року вступив до Гітлер’югенду. 1943 року тітку.\n"+\
    u"1948 року художник протягом трьох місяців навчався у Віденській академії мистецтв, де одним з його викладачів був професор Робін Крістіан Андресен. В цей час Гундертвассер відвідав виставки Вальтера Кампмана та Егона Шиле у Відні, а також відвідав доповідь під назвою «Кожен має бути творчим». Ці події справили враження на митця. Саме тоді художник почав підписувати свої картини псевдонімом Гундертвассер модифікувавши своє справжнє прізвище заміною слова «сто» на «гундерт», що означає «100» німецькою. Пізніше художник дізнався, що «сто» (Sto) походить не від слов’янського числівника, а від німецького «Stau», Stauwasser — стояча вода. Після того, як Гундертвассер облишив навчання, у квітні 1948 року він вперше відвідав Італію.\n"\
    u"Щойно виданий новий „Український правопис” (К., 1990) поновлює написання літери ґ в давнозапозичених і зукраїнізованих словах та українських прізвищах. Оскільки в ньому зазначено як приклади всього 30 слів і два прізвища з літерою ґ, а новий орфографічний словник навіть не заповідається, гадаємо, аж ніяк не зайвим буде подати для щоденної практичної потреби наших читачів ширший перелік таких слів, складений за авторитетними джерелами.\n"+\
    u"Sample (ґ letter) "\
    u"ґестка ґешефт ґиґнути ґирлиґа ґлей (клей) ґніт (у лампі) ґоґель-моґель ґонта ґрати ґречний ґринджоли гроно ґрунт ґудз(ь) ґудзик ґуля гума дзиґа дзиґар дзиґлик дриґати зиґзаґ резиґнація ремиґати риґувати сновиґати уджиґнути фіґа фіґлі-міґлі хуґа хурдиґа та їхні похідні",

    u"Belorussian Sample (text) "\
    u"Замак — умацаванае жытло феадала — не меў у мінулым тыпалагічных прыкладаў, іыў вынікам афармлення феадальнага ладу. У асновеудовы замку ляжалі не тыя ці іншыя кампазіцыйныя прынцыпы, а схемы, вымушаныя стратэгічнымі патрабаваннямі часу і рэгіёну. Фактычным прататыпам сярэднявечнага замка лічаццаургі германцаў, у якіх схема забудаванага франкскага двара спалучана з вежай, абкружанай равамі і палісадамі. Такія вежыудавалі рымляне, а потым франкі (рэшткі захаваліся, напрыклад, у Ніжняй Саксоніі — Дрыбург, Пірмант і інш.)\n"+\
    u"Эвалюцыя сярэднявечнай крапасной архітэктуры кепска паддаецца звычайнай перыядызацыі з падзелам на раманскую і гатычную. Крапасныя пабудовы сістэматычна перабудоўваліся ў адпаведнасці з наяўнымі патрэбамі, і элементы пэўнага стылю маглі з’яўляцца ў пабудове значна пазней за ўсталяванне стылю ў грамадзянскім і царкоўнымδудаўніцтве.\n"+\
    u"У 1-ю сусветную вайну ў дзеючай расійскай арміі. Удзельнік з'езда беларускіх нацыянальных арганізацый у Мінску (сакавік 1917), з'езда настаўнікаў Мінскай губерніі (май 1917). З снежня 1917 у Вільні, удзельнік стварэння Беларускага навуковага таварыства, у студзені 1918 абраны ў склад Віленскай беларускай рады, удзельнічаў у сесіі Рады БНР у Мінску (24-25.3.1918). У лістападзе 1918 кааптаваны ў склад Літоўскай Тарыбы. Пасля прыходу ў Вільню Чырвонай Арміі працаваў у літаратурна-выдавецкім аддзеле Наркамасветы Літоўска-Беларускай ССР, загадваў беларускім выдавецтвам «Веда». У час польска-савецкай вайны 1919—1920 гадоў член Цэнтральнай беларускай рады Віленшчыны і Гродзеншчыны, прэзідыума Беларускай цэнтральнай школьнай рады.",

    u"Bulgarian Sample (pangrams) "\
    u"Ах чудна българска земьо, полюшквай цъфтящи жита.  Жълтата дюля беше щастлива, че пухът, който цъфна, замръзна като гьон. За миг бях в чужд плюшен скърцащ фотьойл. Вкъщи не яж сьомга с фиде без ракийка и хапка люта чушчица! Шугав льохман, държащ птицечовка без сейф и ютия. Под южно дърво, цъфтящо в синьо, бягаше малко пухкаво зайч.Я, пазачът Вальо уж бди, а скришом хапва кюфтенца зад щайгите. Хълцайки много, въздесъщият позьор, Юрий жабока, фучеше. Гномът Доцьо приключи спящ в шейна за жаби. Щиглецът се яде само пържен в юфка без чушки и хвойна. Хълцащ змей плюе шофьор стигнал чуждия бивак. Щурчо Цоньо хапваше ловджийско кюфте с бяла гъмза.\n"+\
    u"Sample (text) "+\
    u"След Освобождението народните представители решават, че официалният български език ще бъде по североизточните наречия, както е и до днес, според изказа на източната говорна група, най-вероятно защото населението на най-големите тогава градове в страната — Русе, Велико Търново, Шумен, Габрово, Стара Загора и Пловдив, са били в единна позиция по отношение на ятовата граница. С това се подчертава разграничението между литературния език и западните говори. Така особено ясно се отделят като диалекти шопският — Софийско, Пернишко, Кюстендилско, Самоковско и в Северозападна България, а също така и македонският диалект (който днес в Р. Македония се опитват да легитимират като отделен език от българския) в Разложко, Петричко, Струмишко, Благоевградско и други.\n"+\
    u"В развоя на новобългарския книжовен език се различават три главни периода: 1. От началото на XIX в. до Освобождението на България от османско робство; 2. От Освобождението до 9 септември 1944 г.;\n"+\
    u"В хода на историческото развитие на българския език и контактите му със съседните неславянски езици на Балканския полуостров настъпват значителни промени в сравнение с останалите славянски езици. Те обхващат промени в морфологията и синтаксиса, характеризиращи се с почти пълно отпадане на падежните форми (падежни остатъци има при местоименията, личните имена, съществителните и прилагателни имена от мъжки род в именителен падеж), възникване и употреба на определителен член, запазване на славянските прости глаголни времена (минало свършено време и минало несвършено време) и развитие на нови, възникване на дублирано пряко и непряко допълнение, изчезване на инфинитива и развитие на несвидетелски форми при глаголите и др. Тези промени разграничават като цяло развитието на морфологията и синтаксиса в българския език от посоката на развитие на останалите славянски езици.",

    u"Serbian Sample (pangrams) "+\
    u"Љубазни фењерџија чађавог лица хоће да ми покаже штос. Ајшо, лепото и чежњо, за љубав срца мога дођи у Хаџиће на кафу. Чешће цeђење мрeжастим џаком побољшава фертилизацију генских хибрида. "+\
    u"Sample (text) "+\
    u"Српски језик је словенски језик. Као и македонски, бугарски, хрватски, бошњачки и словеначки, он је јужнословенски језик.\n"+\
    u"Од осталих словенских језика, јужнословенски говори су се по свему судећи издвојили још пре преласка на Балканско полуострво. То се закључује на основу заједничких особина које имају најзападнији словеначки и чешки говори, као и најјужнији словачки и српско-хрватски говори.\n"+\
    u"У ранијој фази, пре тих диференцијација, постојао је један јединствен језик који се технички назива прасловенским, протословенским или протосрпским. Тај заједнички језик свих Словена није оставио никакав траг. Њему је врло близак говор Ћирила и Методија, такозвани старословенски, који је по својим особинама источнојужнословенског типа. Иако чува седам падежа, дуал, затим конјуктив и оптатив, он се ипак разликује битно од реконструисаног прасловенског језика. Једна од најупадљивијих разлика је што је у старословенском, као и у српском, већ тада дошло до метатезе ликвида.\n"+\
    u"Прасловенски језик је дериват (такође само реконструисаног) протоиндоевропског језика. То је назив за реконструисан језик који је предак словенским, балтичким, германским, италским (латински), грчким, албанским, хетитским, тохарским, иранским, индијским и другим савременим и изумрлим језицима. Нема сумње да је некада давно, вероватно пре око 7000 година постојала заједница која је користила језик који је предак свих побројаних, али није јасно нити где је она била (помишља се на данашњу Украјину, јужни Кавказ), нити које је гране у првој фази свог распада дала. Извесно је да фази прасловенског претходи балтословенска фаза- она је заједничка балтичким и словенским језицима. Балтички језици су још конзервативнији од словенских и представљају најархаичније живе индоевропске језике.",

    u"Serbo-Croatian Sample (text) "+\
    u"Српскохрватски језик (хрватскосрпски, хрватски или српски, српски или хрватски) је стандарднојезичка форма настала из српског и хрватског језика, која је постојала у СФРЈ између 1945. и почетка деведесетих година 20. века, када су се језичке норме поново одвојиле. Условно се може рећи да је ова стандарднојезичка форма постојала од половине 19. века. Српскохрватски је био један од службених језика Социјалистичке Федеративне Републике Југославије, а његов простор дефинисао се као простор новоштокавског наречја, од торлачког најјужнијег дела јужне Србије на југоистоку до кајкавског Загорја у Хрватској на северозападу, изузевши чакавске делове Далмације и Истре.",

    u"Macedonian Sample (pangrams) "+\
    u"Ѕидарски пејзаж: шугав билмез со чудење џвака ќофте и кељ на туѓ цех. Бучниов жолт џин ѕида куќа со фурна меѓу полиња за цреши, хмељ и грозје. Долг Џош, сторив женење, црн ѕид! Фрчат хмељ, ќумбе, ѓупки, зајак. Мојот дружељубив коњ со тих галоп фаќа брз џиновски глушец по туѓо ѕитче.\n"+\
    u"Sample (text) "+\
    u"Верувам дека постојат многумина што многу постручно би ги раскажале приказните за меровиншките кралеви, сионските загатки, розенкројцери, илуминати и слични езотерици - сите оние мотиви од кои се напојувал Ден Браун при конструирањето на својот хит-роман „Кодот на Да Винчи“. Но јас имам една блага тактичка предност пред другите раскажувачи - своевремено бев на местото на кое е родена легендата!\n"+\
    u"Веднаш да признаам: оваа колумна, којашто поради нејзината должина ќе биде објавена во неколку продолженија, ја пишувам по наговор на некои блиски пријатели. Јас досега на овие страници пишував за филм, за религија, за музика, за политика, но никогаш за алтернативната историја и нејзините мистични петна. Притоа не се сметам себеси за експерт во оваа тема; верувам дека постојат многумина што многу постручно би ги раскажале приказните за меровиншките кралеви, сионските загатки, розенкројцери, илуминати и слични езотерици - сите оние мотиви од кои се напојувал Ден Браун при конструирањето на својот хит-роман „Кодот на Да Винчи“. Но јас имам една блага тактичка предност пред другите раскажувачи - своевремено бев на местото на кое е родена легендата! Неодамна тие свои сеќавања ги споделив со некои мои драги луѓе, а на нивен наговор - ги споделувам и со вас, почитувани читатели. Се надевам дека ќе уживате во мојата приказна.",

    u"Rusyn Sample (text) "+\
    u"Історія русиньского языка охоплює дакілько сторіч. Лем од другой половины XIX. ст. ся розлічны варіанты русиньского языка зачали вжывати в школах, публікаціях, періодічных выданях і в уряднім контактї. Але непозераючі на то, же русиньскый язык нїґда не быв штатным языком, у розлічнім часї і в розлічных країнах, де жыли Русины, русиньскый язык набывав офіціалный статус в рамках автономных теріторій, як наприклад, у міджівойновій Підкарпатьскій Руси як части Чеськословеньска і по другій світовій войнї у Войводині, бывшій Югославії.\n"+\
    u"Повойновый час (од 1945 року) быв окреме тяжкый про русиньскый язык. Стало так зато, бо по другій світовій войнї і по приходї до влады комуністів у вшыткых европскых країнах, де жыли Русины (окрем бывшой Югославії), русиньскый язык быв выголошеный за діалект україньского языка. Хоць русиньскы діалекты ся продовжовали вжывати, літературна форма языка была вышмарена зо школ, періодічных выдань і публікацій. Докінця діалектны тексты у фолклорных зборниках або приклады русиньской белетрістікы у літературных антолоґіях, вшыткы мусили быти „українізованы“ перед тым, як ся зачали друковати.\n"+\
    u"Така сітуація ся радікално змінила внаслїдку револуцій 1989 року і впаджіня комунізму в Совєтьскім союзї. Од того часу русиньскый язык ся назад вжывать в розлічных сполоченьскых діскурзах. Як підкреслёвав знамый славіста, академік Нікіта Ільїч Тольстой, высвітлюючі возроджіня інтересу к русиньскому языку, „ідея того літературного языка не є плодом фантазії або представ окремых особ або ґруп, але презентує природне желаня людей мати язык, котрый бы не зіставав лем яковсь письменнов, мертвов формов, але абы быв шыроковжываный, т. є. вжывав бы ся в розлічных сферах жывота“. В усилю реалізовати тоту ідею, было дакілько спроб кодіфіковати язык. У Новембрї 1992 року вдяка події, яка ся стала знама як Першый конґрес русиньского языка, публіцісты і учены з розлічных штатів ся стрітили в Словеньску і вырїшыли прияти такзваный „романшскый прінціп“, значіть процес кодіфікації языка зреалізованый ретороманшсков меншинов у Швайчарьску. То значіло створити літературну форму про кажду країну, де Русины жыли (у Польску, Словеньску, Українї і бывшій Югославії), а потім тыж продіскутовати можность створити з тых штирёх варіантів шпеціфічне койне або єден літературный язык про вшыткы реґіоны.",
)

CYRILLIC_NONSLAVIC_TEXT = (
    u"Rusyn Sample (text) "+\
    u"Історія русиньского языка охоплює дакілько сторіч. Лем од другой половины XIX. ст. ся розлічны варіанты русиньского языка зачали вжывати в школах, публікаціях, періодічных выданях і в уряднім контактї. Але непозераючі на то, же русиньскый язык нїґда не быв штатным языком, у розлічнім часї і в розлічных країнах, де жыли Русины, русиньскый язык набывав офіціалный статус в рамках автономных теріторій, як наприклад, у міджівойновій Підкарпатьскій Руси як части Чеськословеньска і по другій світовій войнї у Войводині, бывшій Югославії.\n"+\
    u"Повойновый час (од 1945 року) быв окреме тяжкый про русиньскый язык. Стало так зато, бо по другій світовій войнї і по приходї до влады комуністів у вшыткых европскых країнах, де жыли Русины (окрем бывшой Югославії), русиньскый язык быв выголошеный за діалект україньского языка. Хоць русиньскы діалекты ся продовжовали вжывати, літературна форма языка была вышмарена зо школ, періодічных выдань і публікацій. Докінця діалектны тексты у фолклорных зборниках або приклады русиньской белетрістікы у літературных антолоґіях, вшыткы мусили быти „українізованы“ перед тым, як ся зачали друковати.\n"+\
    u"Така сітуація ся радікално змінила внаслїдку револуцій 1989 року і впаджіня комунізму в Совєтьскім союзї. Од того часу русиньскый язык ся назад вжывать в розлічных сполоченьскых діскурзах. Як підкреслёвав знамый славіста, академік Нікіта Ільїч Тольстой, высвітлюючі возроджіня інтересу к русиньскому языку, „ідея того літературного языка не є плодом фантазії або представ окремых особ або ґруп, але презентує природне желаня людей мати язык, котрый бы не зіставав лем яковсь письменнов, мертвов формов, але абы быв шыроковжываный, т. є. вжывав бы ся в розлічных сферах жывота“. В усилю реалізовати тоту ідею, было дакілько спроб кодіфіковати язык. У Новембрї 1992 року вдяка події, яка ся стала знама як Першый конґрес русиньского языка, публіцісты і учены з розлічных штатів ся стрітили в Словеньску і вырїшыли прияти такзваный „романшскый прінціп“, значіть процес кодіфікації языка зреалізованый ретороманшсков меншинов у Швайчарьску. То значіло створити літературну форму про кажду країну, де Русины жыли (у Польску, Словеньску, Українї і бывшій Югославії), а потім тыж продіскутовати можность створити з тых штирёх варіантів шпеціфічне койне або єден літературный язык про вшыткы реґіоны.",

    u"Kazakh Sample "+\
    u"Қазақ жазуы бірнеше рет өзгеріске ұшыраған. 1929 жылға дейін Қазақстанда қазақ араб жазуы пайдаланылды. 20 ғасыр басында Ахмет Байтұрсынұлы ұсынысымен қазақ фонетикасының ерекшеліктері ескеріліп жасалған, араб графикасына негізделген төте жазу пайдаланылған. Қазіргі кезге дейін Қытай еліндегі қазақтар осы жазу үлгісін пайдаланады. 1929 жылдан 1940 жылға дейін латын графикасы қолданылып, 1940 жылдан қазірге дейін кирилл әліпбиі қолданылуда. 2025 жылдан қазақ тілі латын графикасына ауысуы жобалануда. Түркия мен Батыс елдердегі қазақтар әртүрлі латын жазуына негізделген әліпбиді пайдаланады. 2000 жылдан бастап Тура Жазу енгізіле басталды, латын және кирилше түрінде. Тура Жазу Ахмет Байтұрсынұлы дыбыс жүйесін қолданады, оны енгізумен жекеменшік, мемлекеттік емес орталық айналысады.\n"+\
    u"Дауыссыз дыбыстар сөйлеу мүшелерінің бір-бірімен жанасуы немесе толық қабысуы арқылы пайда болады. Дауыссыздардың басты ерекшеліктері: - дауыссыздардың жасалатын орны – ауыз және көмей қуыстары; - дауыссыз қатаңдарда мүлде үн болмаса, ұяңдарда – үннің қатысы жартылай болады да, ал үнділерде - бәсең үн болады; - дауыссыз қатаң және ұяңдардың ішкі сапасы – таза салдырдан тұрады деуге болады ал, үнділерде сөйлеу мүшелерінің (тіл, ерін, жақ) бір-біріне жуықтауы, түрленуі, көлемін өзгертуі көмей арқылы келген ауаға пәлендей кедергі бола алмайды; - дауыссыз қатаң және ұяңдарды - көтеруге, созуға, әуенін өзгертуге мүлде болмаса, ал үнділерді керісінше – көтеруге, созуға, әуенін өзгертуге болады; - дауыссыздардың үн сапасында - жаңғырық болмайды; - дауыссыздар сөз ішінде жалқы тұрып буын құрай алмайды.\n"+\
    u"Қазақ тілінде сөз алдында тұратын көмекші сөздер орнына, сөз артынан келетін шылау не тиісті жалғау қолданылады (мысалы: қазақ тілі туралы мақаланы энциклопедияға қосу).\n"+\
    u"Тілдін функцияларын аныктауға 20 ғ.-да көңіл бөлінді. Оған дейін “функция” сөзі тіл бірліктерінін синтаксистік (мысaлы, бастауышгын кызметі, толыктауыштын кызметі), морфологиялык (мысалы, формалардын кызметі) кызметін ғана білдіріп, герминдік мәнде жүмсалмады. Кейін ол форма мен күрылымнын мағынасын түсіндіретін мәнде колданыла бастады. “Прага тіл үйірмесінін тезистерінде” (1929) тілдін функционалды жүйе екені аныкталып, сөйлеу кызметінін карым- катынастык және поэтикалык деп аталатын екі функниясы көрсетілді. 20 ғ. 70—80 жж.\n"+\
    u"Тілдін функцияларын тіл жүйесі мен күрылымында жүзеге асыратын аппаратпен байланыстыруға әрекет жасалды. Ю. С. Степанов семиотикалык гіринниптер негізінде Тілдін функцияларынын: номинативтік, синтаксистік, прагматикалык деп аталатын үш түрін аныктады. Бұлар жалпы семиотикада тілдін жан-жакты касиетін білдіретін үш саласына.",

    u"Mongolian Sample (pangram)" +\
    u"Щётканы фермд пийшин цувъя. Бөгж зогсч хэльюү. \n"+\
    u"Sample (text) "+\
    u"Монгол хэл нь монгол үндэстний эх хэл юм. Гарал үүслийн хувьд түрэг хэл, тунгус хэл зэрэгтэй адил Алтай хэлний язгуурт багтдаг. Солонгос хэл, япон хэлний адил нэр үг нь өгүүлбэрийн эхэнд, үйл үг нь өгүүлбэрийн сүүлд байдгаараа онцлогтой. Явцуу утгаараа Монгол улс дахь халх аялгуунд тулгуурлаж ярих хэлийг хэлэх бөгөөд өргөн утгаараа монгол үндэстний ярих хэл яриаг хэлнэ. Өөрөөр хэлбэл тусгаар тогтносон Монгол Улсын монголчууд болон, Xятад улсын нутаг дахь Өвөр Монголын Өөртөө Засах Орны Өвөр Монголчууд, Орос улс дахь Халимаг, Буриадуудын ярих хэлийг хэлдэг.\n"+\
    u"Эх хэлнийхээ дархлааг сайжруулахын тулд хүүхэд багачуудыг зөв ярьж, бичиж хэвшүүлэх нэн шаадлагатай байна. Ингэхийн тулд ерөнхий боловсролын сургуульд монгол хэл зааж байна гээд мэргэжлийн түвшинд үзэж судалдаг хэл шинжлэлтэн хүний мэдвэл зохих зүйлсийг зааж хүүхдийн толгойг хий дэмий зүйлсээр их дүүргэх юм. Тэр нь амьдрал практикт ямар ч хэрэг болдоггүй, тухайн үед багшаас дүн авахын тулд цээжилсэн болоод л өнгөрдөг зүйлс байх юм. Үүний оронд хүүхдийн хэл ярианы сэтгэхүйг эх хэлнийхээ баялаг сайхан эх хэрэглэгдэхүүнээр хөгжүүлэх, тэднийг зөв сэтгэн аргазүйд сургахын тулд монгол хэл, уран зохиолын багш нар нэгийг бодож, ул суурьтайхан хандах цаг болсныг анхаарах цаг нэгэнт болжээ. Эс тэгвэл эх хэл маань эвдэрч, түүгээр яригчдийн сэтгэхүй элий балай болох нь байна шүү. Энэ хэлэлцүүлэгт эх хэлнийхээ тансаг сайхныг хүүхэд багачууддаа хэрхэн мэдрүүлж, хэл ярианы зөв найруулгатай урсам сайхан ярьж сургахын тулд юуг хийх, хэрхэн хамтран ажиллах тугайгаа ярилцах хэрэгтэй юм биш үү.\n"+\
    u"Хэл гэдэг нь хүний ерөнхий ойлголт, үзэл бодол, утга санаа зэргийг илэрхийлж хоорондоо харицахад хэрэглэгддэг дохио зангаа, дүрэм зүй, тэмдэглэгээ, дуудлага, үг зэргийг бүхэлд нь хамруулсан систем юм. Фердинанд де Саушюр нь анхлан хэл судлалыг кодчилон судлаж, шинжлэх ухааны түвшинд авчран нийтэд хүргэсэн байна.\n"+\
    u"Хэл шинжлэл нь хүний хэлийг шинжлэх ухааны үүднээс тайлбарладаг хүмүүнлэгийн ухааны салбар шинжлэх ухаан юм. Хүн төрөлхтний хэл, түүний гарал үүсэл, мөн чанар, үүрэг, түүнчлэн дэлхийн олон хэлний бүтэц, тогтолцоо, хөгжил, зүй тогтол, төрөл, хэв маягийг судалдаг шинжлэх ухааныг хэл шинжлэл гэнэ.\n"+\
    u"Хэл шинжлэлийн ухаан нь XIX зууны эхэн үеэс шинжлэх ухаан болон хөгжиж ирсэн гэж үзэж болно. Хэл шинжлэлийн ухааны хөгжлийн тоймыг авч үзвэл хэл шинжлэлийн судлах зүйл, судалгааны арга, салбар ухаан зэргийг тогтооход чиглэгдэж байв. Хэлний тухай шинжлэх ухааныг хэл шинжлэл гэдэг. Хүмүүс өөр хоорондоо харилцаж, саналаа солилцож, улмаар нийгмээ хөгжүүлж, урагшуулж байдаг маш чухал хэрэглүүр болох хэлний үүсэн хөгжиж ирсэн түүхэн зүй тогтол, мөн чанар хийгээд хөгжлийн ирээдүйн төлөвийг хэл шинжлэл судалдаг.",

    u"Tatar Sample (text) "+\
    u"Татар теле — татарларның милли теле, Татарстанның дәүләт теле, Русиядә таралу     буенча икенче тел. Төрки телләрнең кыпчак төркеменә керә. ЮНЕСКО игълан иткән 14 иң коммуникатив тел исемлегенә керә.\n"+\
    u"Лексика ягыннан татар теленә иң якын тел — башкорт теле, аннары ногай, каракалпак, казакъ, балкар, үзбәк, уйгур һәм комык телләре бара.\n"+\
    u"Татар теле Татарстан Республикасында, шулай ук Башкортстан, Мари Ил, Удмуртия, Мордовия республикаларында, Төмән, Сембер һәм Сарытау өлкәләрендә киң таралган. Русиянең барлык төбәкләрендә татарлар яши, шуңа күрә барлык төбәктә дә татарча сөйләшүче бар. Татар телендә Русиядә 5,3 млн. якын кеше сөйләшә (2002 елның халык исәбе). Татар теле шулай ук башкортлар (524 399 мең кеше),руслар (136617 кеше), марилар(42892 кеше), удмуртлар(26242 кеше) һәм чуашлар(68624 кеше) арасында таралган. 2002 елның халык исәбенә күрә Русия татарларының 81%ы татар телен белә(5554601 кешедән 4488330 кеше) (2002 елның халык исәбе).\n"+\
    u"Дөньяда татарча белгәннәрнең саны мәгълүм түгел. Бу сан якынча 6 миллионнан 8 миллионга кадәр. Татар теле Үзбәкстан, Казакъстан, Азәрбайҗан, Кыргызстан, Таҗикстан һәм Төрекмәнстан илләрендә таралган. Татарча сөйләшкәннәр хәтта Австралиядә дә бар.\n"+\
    u"Татар теле Идел буе һәм Урал алды районнарында башка туган һәм шулай ук туган булмаган телләр нигезендә формалашты. Татар теленә мари, мордва, удмурт, гарәб, фарсы, рус телләре йогынтысы аеруча зур булды.\n"+\
    u"Сакланып калган әдәби мирасның иң борынгысы – XIII гасырда Bolgar tamgase.jpg Идел буе Болгары шагыйре Кол Гали язган «Кыйссаи Йосыф» поэмасы. Поэма язылган тел үзендә болгар һәм кыпчак телләре элементларын берләштерә. Алтын Урда чорында рәсми тел буларак Идел буе төркиләренең кыпчак теле кулланыла. Flag of the Kazan Khanate.svg Казан ханлыгы чорында искетатар теле формалаша, бу телгә гарәб һәм фарсы телләреннән алынмалар хас була.\n"+\
    u"Татарстанда татар теле, рус теле белән беррәттән, дәүләт теле булып санала. Татар телендә рәсми буларак кирилл әлифбасы кулланыла. Кайбер татарлар, күбесенчә чит илләрдә, латин һәм гарәп әлифбасын да куллана.\n"+\
    u"Татарстанда татар мәктәпләре күп. Югары уку йортларында татар теле факультетлары бар.\n"+\
    u"Татарстан Көнчыгыш Аурупа тигезлегенең көнчыгыш өлешенә урнашкан һәм аның төп үзенчәлекләренә ия. Гомумән, Татарстанның җир өсте төзелеше дулкын-сыман тигезлектән гыйбарәт. Аның уртача биеклеге диңгез өстеннән 170 м га, ә аерым урыннары 300—350 м га җитә. Күбесенчә, биеклеге 100 м дан узмаган түбәнлекләрдән тора.\n"+\
    u"Көнчыгыш Аурупа тигезлеге Иделдән алып көнчыгышка, Урал тауларына таба күтәрелә бара. Татарстанның җир өсте өчен дә бу үзенчәлек хас: аның иң түбән урыннары — Идел аръягының көнбатышына, ә иң биек җирләре көнчыгышына таба урнашкан. Биредә, республиканың көньяк-көнчыгышында, Бөгелмә-Бәләбәй калкулыгы ята.\n"+\
    u"Республиканың көньяк-көнбатыш өлешенә 200—250 м биеклегендәге Идел буе калкулыгы тармаклары кергән. Иделнең төп уңъяк ярының биек һәм текә булуы шушы калкулыкның Иделгә якын ук килеп җитүе һәм аның Идел суы агымы тәэсирендә җимерелүе белән аңлатыла.",

    u"Tajik Sample (text) "+\
    u"Забони тоҷикӣ, ки дар Эрон: форсӣ, ва дар Афғонистон дарӣ номида мешавад, забони давлатии кишварҳои Тоҷикистон, Эрон ва Афғонистон мебошад. Дар Ӯзбакистон, агарчӣ забони ақаллият тоҷикӣ маҳсуб мешавад, вале дар Ӯзбакистон зиёда аз 15 миллион нафар ба тоҷикӣ гуфтугӯ мекунанд. Ин забон ба хонаводаи забонҳои ҳинду-аврупоӣ дохил мешавад. Дар маҷмӯъ: порсигӯёни асил(форсӣ, тоҷикӣ, дарӣ) зиёда аз 122 млн мардум мебошанд. Аммо тамоми порсигӯёни ҷаҳон 222 млн ҳастанд. Фақат ба гӯиши тоҷикӣ 44 миллион нафар гап мезананд. Забони точикӣ, яке аз забонҳои бостонтарини ҷаҳон ба шумор меравад. Давраи нави инкишофи он дар асрҳои 7-8 сар шудааст. Бо ин забон шоирону нависандагони бузург Рӯдакӣ, Фирдавcӣ, Хайём, Сино, Ҷомӣ,Мавлоно, Ҳофиз, Дониш, Айнӣ, Лоҳутӣ, Турсунзода ва дигарон асарҳо эҷод кардаанд.\n"+\
    u"Забони точикӣ диққати олимон ва нависандагони оламро ба худ ҷалб кардааст. Ба омӯзиши забони порсӣ-точикӣ яке аз асосгузорони коммунизми илмӣ Фридрих Энгелс мароқ зоҳир карда буд. Забони тоҷикӣ рӯз то рӯз рушд мекунад ва садҳо вожаҳои нав ба таркиби луғавии забони тоҷикӣ ворид мешаванд.\n"+\
    u"Забони тоҷикӣ, ки аз хонаводаи забонҳои ҳинду-аврупоӣ порсӣ - тоҷикӣ ва порсӣ - дарӣ дар асл форсӣ = порсӣ мибошад, ба забонҳои эронӣ дохил мешавад. Забони тоҷикӣ ба забонҳои порсиву дарӣ хеле монанд аст ва аҳолии кишварҳои Эрон, Ӯзбакистон, Кирғизистон, Қазоқистон, Афғонистон ва Покистон, инчунин дар Тошқурғони Ҷумҳурии Халқии Чин бо ин забон гуфтугӯ мекунанд. Солҳои баъди Истиқлоли ҶТ тоҷикони зиёде ба муҳоҷират ба Руссия барои кор рафтаанд ва баъзеҳояшон онҷо муқимӣ гаштанд, алалхусус дар шаҳрҳои калони Россия. Ҳоло тоҷиконро дар тамоми гӯшаву канори ФР пайдо кардан мумкин аст. Аз рӯи ҳисоби омории Руссия, ҳоло дар Руссия зиёда аз 222 ҳазор мардуми тоҷик муқимӣ гаштаанд. Муҳоҷирони тоҷик бошанд дар Руссия зиёда аз 1,5 млн шахсро фарогир ҳастанд.\n"+\
    u"Забони адабии тоҷикӣ аз ҷиҳати фонетикӣ ва луғавӣ байни ин ойилайи сегона ҳам ба форсии классикӣ ва ҳам ба паҳлавӣ аз ҳама бештар наздикӣ дорад. Яъне, забони тоҷикӣ қадимтар аст, фонетика (дар инҷо кобулӣ ба тоҷикӣ наздиктар аст) ва таркиби луғавии oн дар тули асрҳо дигар нашуда ва бинобарин архаикӣ мондааст. Ҳолоонки тарзи талаффузи эрониҳо баройи гушҳои тоҷикон ва афғонистониҳо бегона мерасад, чунки модернтар ва мулойимтар аст. Ибораҳо, стилистика ва тарзи ҷумлабандии тоҷикон то ҳудудӣ дигаранд. Дар натиҷайи ҳамзистии мардуми тоҷик бо мардуми туркзабон, хусусан бо халқи ӯзбак дар тули асрҳо, ба забони тоҷикии гуфтугуйӣ ва лаҳҷаҳойи он зиёдтар калимаҳойи баромадашон туркӣ ворид гаштаанд. Баръакс фойизи лексикайи арабӣ дар гӯиши Тоҷикистон нею дар гӯишҳои Эрон ва Афғонистон, яъне забонҳойи давлатҳойи исломӣ баландтар аст. Ҳам ба тоҷикии aдабӣ, ҳам ба тоҷикии гуфтугуйӣ муддати шаст-ҳафтод соли охир забони русӣ та'сири бузург расонидааст ва расонида истодааст. Ҳаминтавр, калимаҳойи байналмилалиро гуиши тоҷикистон аз русӣ иқтибос карда меояд то ҳануз, дар ҳоле ки теҳронӣ аз фаронсавӣ ва инглисӣ ва кобулиҳо аз инглисӣ истифода мекунанд. Рост аст, ки имрузҳо метавон дар матбуот ва телевизиони Тоҷикистон ба шакли фаронсавӣ-теҳронии kалимаҳойи хориҷӣ дучор омад, ки корбаст карда мешаванд ба ҷойи пешина тарзи рус навишти онҳо, масалан конфронс ба ҷойи конферентсия. Вале ҷиддитарин фарқияти гуиши тоҷикиро аз кобулию теҳронӣ дар грамматика пайхас мекунем. Чунин шаклҳо мисли “рафта истодаам; падарама ҷойи корасон”-тоҷикон ё “дорам мирам, исмиш Фирийдун ҳастиш”-и эрониҳо байни ҳамдигари онҳо фаҳмо нестанд. Ва албатта, наметавон қайд накард ин нуктаро, ки тамоми адабиёти форсии kлассикӣ ба хатти форсӣ навишта шуда ва ин хат то ҳануз дар Эрону Афгонистон ҷорӣ аст, миллати тоҷик бошад, аз сабабҳойи сиёсӣ ду бор тайи 80 соли охир алифбояшро дигар кард, аввал аз ҳуруфи форсӣ ба лотинӣ, баъд ба кириллик гузашт. Ин яке аз омилҳойи асосийест, ки ин гӯишҳоро боз ҳам аз якдигар дуртар сохтааст.",

    u"Kyrgyz Sample "+\
    u"Көпчүлүк окумуштуулардын пикиринде Хакасиядагы, Тувадагы, Тоолуу Алтайдагы, Моңголиядагы, Таластагы, Кочкордогу жазуу эстеликтеринде сакталып калган жазуулар б. з. ч. 3 к. - б. з. 10-11-кк. чейин кыргыздар колдонуп келген тил болуп эсептелет. Бирок аталган тил андан мурунку доорлордо кезигерин унутпашыбыз керек. Мисалы, кийинки түркологдордун кээ бири (кара: Дроздов Ю.Н. Тюркская этнонимия древнеевропейских народов. М., 2008) сактардын тили дагы түрк (кыргыз) тилине жакын экендигин далилдеп жатат. Бул жерде «түрк» деген сөз жалпылама мааниде колдонулуп жүрүшү мүмкүн экендигин эстен чыгарбоо керек (кара: Кононов А.Н. Опыт анализа термина «турк». //СЭ. № I, 1949). Ал эми байыркы кытай маалыматтарында сакталып калган хунндардын 20 чакты сөзүнүн (мисалы, ch’eng-li - «көк» = «асман»; hiep-hō - χiәp-γәu = «йабгу», «жабгу»; eu-ta - wo-lu-to, ao-t’ot = «ордо», «кынгырак» - байыркы түрк. kɨŋrak = эки миздүү ийри бычак) уңгусу түрк тилине келип такалат. Демек, кыргыз тилинде колдонулган жазуулар Орхондогу жазуу эстеликтеринен эрте пайда болуп, кийин архаикалык мааниде айрым фонетикалык, грамматикалык, структуралык өзгөрүүлөргө ээ болушу мүмкүн. Орхон түрктөрү өз жазуу системасын түзүүдө байыркы кыргыздардын жазуу маданиятындагы тажрыйбаны пайдаланышкан (Шилтеме керек). Бул жазуу системасы ошол учурдагы кыргыздар пайдаланган тил катары мамлекеттик иш-кагаздарынын, дипломатиялык алакалардын талабына толук жооп берген дешке болот.\n"+\
    u"10-кылымга чейин саясий-согуштук кырдаалдар, согуштук аракеттер, миграциялар, кыргыз тилинин эволюциялык ѳнүгүүсүнѳ тийгизген таасири тууралуу ѳз алдынча изилдѳѳлѳр азырынча жүрѳ элек. Бирок Махмуд Кашгариде Киркиз, Кифжак, Угуз, Тухси, Йагма, Жикил, Уграк жана Жаруктардын тили – бир, таза түрк тили [туркиййя мах̣д̣а луг̣а вāх̣ида] экенин, Йамак менен Башгирт тили аларга жакын экени эскертилет. Ошону менен эле бир катар «бардык Йагма, Тухси, Кифжак, Йабаку, Татар, Кай, Жумул жана Огуздар «з» тыбышын «й» менен алмаштырып салышарын, башкача айтканда бул топтогулардан башкалар (анын ичинде кыргыздар дагы) кайыңды (жыгач, бак) «казиң», кийизди «кизиз», кездеменин кыйыгын (кыйык) «кузук» деп сүйлѳѳрү белгиленген. Негизи окшоштугу жагынан Махмуд Кашгаринин сѳздүгүндѳ колдонулган сѳздѳр дээрлик азыркы кыргыз тилинде, эң эскилерин алиге чейин түштүк кыргыздары колдонорун белгилѳѳгѳ болот. Мисалы, Махмуд Кашгариде «курум» – «аска-таш», «амаж» – соко. Азыркы учурда жергеталдыктар үйүлүп калган шагыл ташты курум дешсе, жалпы түштүктө сокону амач деп аташат. Бирок байыркы Энесайлык кыргыздардын жазуу тили азыркы кыргыздардын тилине тийгизген таасирин так кесе айтууга болбойт. Мисалы, кээ бир окумуштуулар (кара: Петров. К.И. Очерки происхождения киргизского народа. Фр., 1963) «XIII-XV кылымдарда Тянь-Шанда калыптанган тилдин моңголдордун чабуулуна чейинки (XIII кылымга чейинки)Тянь-Шанда жашаган калк жана енисейлик кыргыздарга тиешелүү тилге жатпагандыгын» баса белгилеген. Кыргыз тилинин моңголдордун чабуулуна чейин ѳзгѳрүүгѳ учураганын академик Болот Жунусалиев (Юнусалиев) дагы кѳрсѳтѳт. Мисалы, «кыргыз-алтай тилинде лексика, фонетика жана морфологиядагы окшоштуктардан тышкары кыргыздын тагай, адигине уруулары колдонуп, бирок ичкиликтерде кезикпеген өзүнчө сөз тобу бар.",

    u"Chechen Sample "+\
    u"Америкин Цхьанатоьхна Штаташ я (Ӏамерикин Цхьанатоьхна Штаташ) — (en. United States of America) Къилбаседa Ӏмерикан мохк бу, къилбехь Мексикац къилбаседехь Канадац доза а долуш. Ӏамерикан мехкаш малхбалехьа, малхбузехь, Атлантик а кӀорга хӀордац ара болуш болун мохк бу.\n"+\
    u"Викингаш дӀабоьвлча Керла-Дуьненан йисте испанхой кхаьчча.1492 шарахь октябрь баттахь испански экспедици кхечир Сан-Сальвадор аьлла гӀайре тӀе,шайн куьгаллехь Христофор Колумб а волуш. 1507 шарахь лотарингийн географо Мартин Вальдземюллерс Керла-Дуьненан Ӏамерика аьлла цӀе тилла сацам бина, флорентийн хӀордталлархочун цӀарах Америго Веспуччи. Эцу хенахь Ӏамерика таллам болабелла. 1513 шарахь испанхойн конкистадорас Хуан Понсе де Леонс дӀабилна гӀайренах Флорида, циггахь 1565 шарахь кхоллаелла дуьххьарлера даиман йолу европейски колони, цара кхоьллана Сент-Огастин аьлла шахьар.1530 шо чекхдолуш Эрнандо де Сотос дӀайилна Миссисипи, кхи дӀа Арканзас хи долче кхаьчча иза.\n"+\
    u"ХӀара мохк карийнарг Христофор Колумб ву, испанхо а волуш ша къомах. Цунна ша дӀайилнаг Инди ю моьттуш хилла, амма иза бакъ ца хиллера. Европахой хӀорд-кеманахь адамаш далош АЦШ махкахь шай колониш кхолла буьйлабелира, амма индейш шайбоца наханна реза бацара.\n"+\
    u"Таханалерачу дийнахь АЦШ дуьненчохь уггаре чогӀа пачхьалкх лораш ю.",

    u"Bashkir Sample "+\
    u"Илебеҙ етәксеһенең тышҡы сәйәсәттәге уңыштары һоҡландырырлыҡ. Яңыраҡ ҡына Мысырҙа эш сәфәре менән булып ҡайтҡан ине. Унан алда иһә — Төркиәлә яңы газ контракты төҙөүе, декабрҙә Һиндостанға уңышлы эш сәфәре, Ҡытай, Латин Америкаһы илдәре менән хеҙмәттәшлекте нығытыуы... Әле килеп Европаның үҙәгендәге Венгрия менән хеҙ­мәттәшлек килешеүенә ҡул ҡуйыуы сәйәси еңеүҙәр иҫәбен арттырҙы.\n"+\
    u"Венгрия премьер-министры Виктор Орбан Будапешт ҡалаһында Владимир Путинды бик йылы ҡаршы алды. Осрашыу барышында Венгрияны газ һәм нефть менән тәьмин итеү буйынса ике яҡ өсөн дә файҙалы килешеүгә ҡул ҡуйылды. Шуныһын да билдәләп үтергә кәрәк: илебеҙ быға тиклем дә Венгрия менән бәй­ләнеш тота ине. Айырыуса атом энерге­тикаһы өлкәһендә. Ә углеводород сеймалының 75-80 процентын Венгрия Рәсәйҙән һатып ала. Рәсәй-Венгрия мөнәсәбәттәренең яйланып китеүен, әлбиттә, Европа союзында ла, күр­шеләге Болгарияла ла бик өнәп еткермәнеләр. Билдәле булыуынса, “Көньяҡ ағым” исеме алған газ үткәргес торбалар Ҡара диңгеҙ төбө аша һуҙылып, Болгария биләмәһе аша Европаның башҡа илдәренә таралырға тейеш ине. Болгария был төҙөлөшкә һуңғы сиккә тиклем рөхсәт бирмәй килде. Тап шул саҡта илебеҙ етәкселеге Болгария биләмәһе аша үтәсәк газ үткәргескә альтернатива эҙләп тапты ла инде – торбаларҙы Төркиә аша һуҙыу мәсьәләһе хәл ителде. Төркиәнән Рәсәй газы Греция аша Македония, Сербия һәм Венгрияға тараласаҡ.\n"+\
    u"Европала Венгрия Рәсәйҙең ҙур стратегик партнеры булып тора. Иҡтисади хеҙмәттәшлек итеү буйынса был дәүләт, Германия һәм Австриянан ғына ҡалышып, өсөнсө баҫҡысты биләй. Әйткәндәй, Европала ике ил – Венгрия менән Бөйөк Британия — һәр саҡ рәсми Брюссель сәйәсәтенә ҡаршы сығыусылар булараҡ билдәле. Рәсми Лондон иһә бына нисәмә йыл инде ЕС-тан айырылып сығыу менән янай, Брюсселде АҠШ алып барған сәйәсәттән тайпылыуҙа ғәйепләй. Ә Венгрия иһә ЕС сәйәсәте менән башҡа яҡтан риза түгеллеген белдерә килә. Шуға ла уларҙың беҙҙең ил менән яҡынайырға ынтылыуын аңларға була. Әлбиттә, Венгрия – ЕС һәм НАТО ағзаһы. Шулай булыуға ҡарамаҫтан, был ил үҙен­сәлекле сәйәсәт алып бара. Ҡайһылай ғына булмаһын, Владимир Путиндың әлеге эш сәфәре ҙур әһәмиәткә эйә",

    u"Chuvash Sample "+\
    u"Чăваш чĕлхи — тĕрĕк чĕлхисенчен пĕри, пăлхар ушкăнне кĕрекен пĕртен-пĕр чĕрĕ чĕлхе. Ку ушкăна тата Атăлçи пăлхарпа хазар чĕлхи те кĕнĕ. Чăваш чĕлхи Чăваш республикинче вырăс чĕлхипе пĕр тан патшалăх чĕлхи шутланать. Чăваш чĕлхине пĕлекен йышĕ — 1,3 млн. çын яхăн (2002 çулхи кăтарту). Унăн виçĕ диалект пур: тури (вирьял), анатри тата мал (е анат) енчи. Чӑваш чӗлхине халаллас тӗллевпе ака уйăхĕн 25-мĕшĕнче Чăваш Енре Чӑваш чӗлхи кунне палăртаççĕ. Юлашки çулсенчи тĕпчев ĕçĕсене хисеплесе, хальхи чăваш чĕлхинче тăватă диалект палăртнă: у-калакан, о-калакан, касса хăваракан аффикслă, «-ке» диалекчĕ.\n"+\
    u"Чăваш халăхĕн чылайăшĕ у-калакан диалекчĕпе усă курать. Вĕсен йышне анатри тата анат енчи чăвашсем кĕреççĕ.\n"+\
    u"О-калакан диалекчĕпе вирьял е тури чăвашсем калаçаççĕ.\n"+\
    u"Касса хăваракан аффикăслă диалекчĕпе калаçакансем — Шăмăршă тата Патăрьел районĕсенче пурăнакан чăвашсем.\n"+\
    u"«-Ке» диалекчĕпе Чăваш Енри Элĕк, Муркаш, Çĕмĕрле тата Етĕрне районĕсен чăвашĕсем пуплеççĕ.\n"+\
    u"Чĕлхен çак диалекчĕсем кашни хăй тĕллĕн чылай тапхăр хушши аталанса пынă, çавăнпа та вĕсем халĕ те пĕр-пĕрин çине пусăм-сĕм яраймаççĕ.\n"+\
    u"Кашни чăваш диалекчĕн авал хăйĕн патшалăхĕ пулнă. Хальхи чăваш халăхĕ авалхи 5-6 патшалăхĕсенче пурăннă теме сăлтавсен никĕсĕсем пур. Каçпиçум сăварĕсем ячĕпе чăвашсен аслă аттисем Атăл çине куçса килнĕ те паянкунхи чăваш тĕнчин никĕсне çирĕплетсе тăраççĕ.\n"+\
    u"XX вĕçĕнче — XXI ĕмĕр пуçламăшĕнче чăваш чĕлхин аталану хăвачĕ чакать. Çакăн пек пулса тухнине мĕнпур тĕнчери лару-тăрăва (кашни 10 çул хушшинче тĕнчере информаци шучĕ-пуянлăхĕ икĕ хут ӳсет) пула, çаплах Совет Союзĕ арканнă хыççăн пĕтĕм пурнăç асапа кĕрсе ӳкнипе те ăнлантарма пулать.\n"+\
    u"ЮНЕСКО евичĕпе, чăваш чĕлхи тĕнчери чĕрĕ халăхсен çухалса пыракан чĕлхесен ушкăнне лекнĕ.\n"+\
    u"Саккун йĕркипе, Чăваш Енĕн официаллă чĕлхи тесе çирĕплетнĕ пулсан та, республика пуçлăхĕсем вырăс чĕлхипе нумай пуплеççĕ, район пуçлăхĕсем, хуçалăх ертӳçисем, пĕрлĕх ĕçтĕшĕсем хут ĕçĕсене майлаштараççĕ. Кулленхи хутшăнусенче те чăваш çынни хальхи саманари пулăмсене ăнлантарма чăваш терминĕсем çуккипе вырăсла пĕлтерĕшсемпе усă курать. Çак вара каллех хальхи тапхăрти чĕлхен пăтăрмахне хăрушлатать.\n"+\
    u"Паянкун чăвашсем хушшинче чăвашла-вырăсла хутăш пупленине тăтăшах илтме пулать, сăмахран: “Эп ĕнер сан патне шăнкăравлаймарăм, уçăлса çуреме чĕнесшĕнччĕ.”",

    u"Ossetian Sample "+\
    u"Ирон адæм (ир, ирæттæ) cты адæмыхатт, сæ фылдæр хай цæры Ирыстоны (уыдонæй Цæгат Ирыстоны 409 мин адæймаджы). Ирæттæ дзурынц ирон æвзагыл, уыдонæй се ’ппæт дæр сты дывзагон (зонынц ма уырыссаг æвзаг, цалдæр раны та — гуырдзиаг кæнæ туркаг).\n"+\
    u"Ирон æвзаг дих кæны дыууæ диалектыл: ирон æмæ дыгурон. Уыдоныл дзурæг адæмы хонынц ир æмæ дыгур.\n"+\
    u"Ирон адæмы истори нын куыд амоны, афтæмæй сæ рагфыдæлтæ — скифтæ, сæрмæттæ æмæ алантæ — кодтой цæугæ цард. Фæстагмæ сæ байзæддæгтæ æрбынат кодтой Кавказы хæхты хуссар æмæ цæгат фæрстыл. Кодтой зæххы куыст, дардтой фос, цыдысты æххуырсты æмæ кодтой цуан дæр. Сæ царды сæм иууыл пайдайагдæр фæкастис фос дарын, уæлдайдæр та лыстæг фос: фыстæ, сæгътæ.",

    u"Mari (Western and Eastern dialects) Sample "+\
    u"Мари́й йы́лме финн-угор тӱшкаш пурышо йылме. Кутырышо-влак кокла гыч эн шукынжо марий улыт, тӱҥ шотышто Марий Элыште да Пошкырт Элыште илыше-влак. Финн тӱшкемыш (балто-финн, саам, мордва, одо да коми йылме-влак дене пырля) пура. Марий Эл деч посна тыгак Виче вӱдкундемыште да эрвел могырышто, Урал марте шарлыме. Марий йылмыште кок кундемой уло: курыкмарий, тӱҥ шотышто Юлын курык серыште (Чыкма воктене) да изиш олык серыште шарлыме, да олыкмарий, олык серыште веле (Йошкар-Ола воктене) шарлыме; олыкмарий кундемойыш тугак эрвел кутыртышвлак пурат.\n"+\
    u"Мары йӹлмӹ (алыкмарла Марий йылме) — ик финн-угр йӹлмӹвлӓ гыц. Кучылтымо марывлӓ коклаште, тӹнг шотышты Мары Элыштӹ да Пошкырт Элыштӹ.\n"+\
    u"Финн тӱшкемыш (балтофинн, саам, мордва, удмурт да коми йӹлмӹвлӓ доно иквареш) пыра. Мары Эл гыц пасна тенгеок Вичӹ вӹдкымдемӹштӹ да ирвел монгырышты, Урал якте шарлен. Мары йӹлмӹштӹ кок тынг йӹлмӹ улы: кырык мары, тӹнг шотышты Йылын Кырык сирӹштӹ да кожла сирӹштӹ шарлен, да алык мары, алык сирӹштӹ веле (Йошкар-Ола лишнӹ) шарлен; алык мары йӹлмӹш тенгеок ирвел хытыртышвла пырат.",

    u"Sakha Sample "+\
    u"Сахалар диэн түүр тыллаах омук, Саха Сирин төрүт олохтоохторо. Саха тыла түүр тылларын бөлөҕөр киирэр. 2010 сыллааҕы биэрэпис түмүгүнэн 480 тыһ. кэриҥэ киһи сахабын дэммит. Бу дьон үксэ Саха Сиригэр, уонна Иркутскай, Магадан уобаластарыгар, Хабаровскай уонна Красноярскай кыраайдарга, Таймыырга уонна Эбэҥки аутоном уокуругар олороллор. Сахалар Саха Сирин олохтоохторун 49 % буолаллар, уонна бу көрдөрүүнэн өрөспүүбүлүкэҕэ саамай элбэх ахсаннаах омуктар буолаллар.\n"+\
    u"Сорох үөрэхтээхтэр этэллэринэн сахалар Байкал күөл аттыттан Өлүөнэ, Бүлүү, Алдан өрүстэр кытылларыгар XII үйэҕэ көһөн кэлбиттэрэ. Сахалар былыр-былыргыттан сылгы, сүөһү иитэллэрэ, атыынан-эргиэнинэн дьарыктаналлара, бэйэлэрэ туспа Таҥара үөрэхтээхтэрэ, сэрии, сэп сэбиргэл туомун тутуһаллара, тимир уһаараллара. Сибииргэ уонна хотугулуу-илин Азияҕа култуура сайдарыгар сабыдыаллара улахан этэ.\n"+\
    u"Тас сахалар — бу тиэрмин икки сүрүн суолталаах. Бастакыта — билиҥҥи Саха сирин тула өттүгэр былыр-былыргыттан түөлбэлээн олорор саха тыллаах дьон. Иккис өйдөбүлэ — бастакы бөлөҕү киллэрэн туран өссө Арассыыйа атын сирдэригэр уонна кыраныысса таһыгар олорор, үөрэнэр-үлэлиир сахалар, ол аата Саха сирин тас өттүгэр олохсуйбут, төрөөбүт эбэтэр быстах кэмҥэ гынан баран балачча өр (холобура үөрэх, уһун командировка кэмигэр) олорор сахалар барыта.",

    u"Karachay-Balkar Sample "+\
    u"Къарачай-малкъар тил — тюрк тилледен бириди. Къарачайлыла бла малкъарлыла сёлешген тилди. Эки диалектге бёлюнеди: къарачай-басхан-чегем («ч»-диалект) эмда малкъар («ц»-диалект). Россияда къарачай-малкъар тилде сёлешгенлени саны 303 минг адамды (2002 джыл халкъ тергеуге кёре).\n"+\
    u"Литература къарачай-малкъар тил, къарачай-басхан-чегем диалектни тамалында къуралгъанды. Джазыу система 1920-24 дждж. араб джазыуну тамалында болгъанды (аджам), 1924-36 дждж. латин алфавитни тамалында, 1936 джылдан бери — кирилл алфавит бла тамалланады.\n"+\
    u"Къарачай-малкъар тил, Къарачай-Черкес («Къарачай-Черкес Республиканы миллетлерини тиллерини юсюнден» Закон, 1996) бла Къабарты-Малкъар («Къабарты-Малкъар Республиканы миллетлерини тиллерини юсюнден» Закон, 1995) республикалада кърал тилди.\n"+\
    u"Къарачай-малкъар тилде «Къарачай» бла «Заман» газетле эмда «Минги тау», «Нюр», «Лячин» журналла чыгъадыла.\n"+\
    u"Дж хариф Къарачай-Черкесияда хайырланады. Дагъыда Къарачай-Черкесияда 1970-чи джыллагъа дери Ў ў бла Нъ нъ (Нг нг харифни орнуна) харифле хайырланнгандыла, алай а тилни Къарачай-Черкесияда бла Къабарты-Малкъарда джюрюген вариантларын унификация этер умутда, бу харифле къоратылгъандыла.",

    u"Lakku Sample "+\
    u"Лакку мазрал цӀанасса тагьарданияту тамансса чивчуну бур. Мадарасса шаттирдугу лавсун бур иш-тагьар къулай дан.\n"+\
    u"Вай калимардаву пикри цалийн букӀлай бакъар. Чичрулул мазну я бухгъумучиял, ягу цӀугъумучиял лугъатру тачӀав къабивкӀссар, цӀанагу бакъассар. Гъумучиял лугъат буссар адабиятсса лакку мазрал (чичрулул бикӀу, гъалгъалул бикӀу) гьануну (Гьанумур гъалгъа).",

    u"Komi Sample "+\
    u"Коми кыв — финн-йӧгра кывъясысь ӧти, коми войтырлӧн чужан кыв. Коми кывйын кызь гӧгӧр сёрнисикас да кык гижӧда кыв: зырян коми да перым коми. Коми кыв — Коми Республикаын каналан кыв (кыдзи и роч кыв). Комиӧн сёрнитӧны Коми Республикаса вужвойтыр — комияс (зыряна, матӧ 156 сюрс морт). Лунвылынджык, Перым Коми кытшын, перым комияслӧн (пермякъяслӧн, матӧ 63 сюрс морт) сӧвмӧ ас гижӧд кыв. Комиясыд и сэні вужвойтыр.\n"+\
    u"Роч Федерацияса да Коми Республикаса Подувгижӧдъяс (Конституцияяс) серти Коми Республика лоӧ Роч Федерациялы кутантор пыдди. Комиыд пырӧ Рочмулӧн Рытыв-войвывса федерал кытшӧ да Войвывса овмöс районӧ.\n"+\
    u"Коми Республика пукалӧ Европа асыв-войвыв пельӧсын, Гринвидзсянь асывлань 45° 21' да 65° 15' костын, а му сяркоссянь войланьыс 59° 12' да 68° 25' костын.",

    u"EXTRA historical Komi alphabet (until 1938) "+\
    u"А/а Б/б В/в Г/г Ԁ/ԁ Ԃ/ԃ Е/е Ж/ж Җ/җ Ԅ/ԅ Ԇ/ԇ I/і Ј/ј К/к Л/л Ԉ/ԉ М/м Н/н Ԋ/ԋ О/о Ӧ/ӧ П/п Р/р С/с Ԍ/ԍ Т/т Ԏ/ԏ У/у Ч/ч Ш/ш Щ/щ Ы/ы",

    u"Komi-Permyak Sample "+\
    u"Ассиныс лыддьӧтан кыв перем комиэз зорӧтӧны XVIII вексянь. Кыв вӧлі нормируйтӧм Коми кытшын 1921'–1938' воэз сьӧрна. Ӧння нормаэз кодифицируйтӧмӧсь 1938' годӧ.\n"+\
    u"Перем коми кыв лыддисьӧ кыв стандартӧн Перем ладорись Коми кытшын, кытӧн коми отирыс (перем комиэз нето коми пермяккез) баитӧны коми кывлӧн кык сёрнитан вылын. Этӧ лоӧны ойвыв перем да лунвыв перем сёрнитаннэз.\n"+\
    u"Перем коми кыв лӧсьӧтікӧ подыс туйӧ бӧрйӧмась лунвыв сёрнитансис вылісь иньва диалект, кӧда перем диалекттэз коласын баитіссез лыд сьӧрті лоӧ медыджыт. Сэтчӧ пыртӧмась л шы, медбы лыддьӧтан кыв лӧсяліс и лунвыв перем, и ойвыв перем сёрнитана коми отирлӧ.",
)

CYRILLIC_KERNING_TEXT = (
    # http://typophile.com/node/99518
    """lc-to-lc аар аби авг агр адм аеж ажу азб аиб айс акв алк амо анг аор апр арф асо ато аук афи ахи аце ачь ашу ащ аър аыр аьв аэр аюш аят аёл бар бба бвя бгр бде бен бжд бзо биз бйм бка блю бма бня бор бпр бры бск бтр бух бфу бха бцо бчи бши бще бъе быв бье бэк бюд бяз бёр вас вбо ввр вгм вда вел вжу взо виз вйт вку вло вма вне вой впе ври вся вто вур вфу вхо вцы вчу вши вщи въм выс вью вэк вюр вяз вёл гар гбю гво ггн где гем гжк гза гим гйп гко гля гме гна гос гпр гру гси гте гум гфи гха гцв гче гшр гщи гъх гым гьх гэй гюс гях гёъ дар дбр дво дгл дду дем джу дзы дин дйо дки дли дми дня док дпе дру дса дтв дуф дфе дху дцы дчи дшп дще дъю дык дьб дэх дюг дяд дёх еаз ебр евч егу еда еес ежи езб еис ейз екр ель емк ень еол епа ера еск етл еуж ефи ехо еци ечь ешь ещу еъх еых еьх еэк еющ еят еёл ёах ёба ёви ёга ёдо ёех ёжи ёзы ёих ёйх ёка ёлк ёмн ёны ёох ёпк ёрс ёсн ёте ёух ёфа ёха ёцк ёчк ёша ёща ёъх ёых ёьх ёэх ёюх ёях ёёх жаб жба жва жгу жда жел жжё жзр жив жйх жка жло жму жны жо жпe жра жсе жт жур жфа жхо жце жчи жшт жщх жъ жы жье жэф жю жяз жёл заи збу зве згл здр зел зжо ззе зим зйх зко зла зме зна зом зпа зрм зск зта зуб зфр зхо зца зчи зши зщх зъе зыб зья зэк зюд зяе зёл иар ибе ивр игл идт иез ижд изк ии ий ик ил им ин иол ип ирт иск ито иул ифе ихр ица иче иши ищ иъх иы иь иэ ию ият иёд йар йбо йве йга йде йем йжи йз йит ййх йк йле йм йны йог йпн йра йсб йти йус йфи йха йца йча йшл йщ йъ йы йь йэ йю йя йё кал кбе ква кга кдо кей кж кза кил кйх кку кле кмо кн кон кп кре ксп кту куз кф кх кц кча кш кщ къ кы кь кэ кюр кях кё лан лб лв лгу лд лем лж лзе лик лйх лка лло лма лн лом лпы лрт лст лта луб лфе лхо лци лчб лше лщ лъх лыж лью лэр люс ляж лён мар мбо мво мгл мду меб мжи мзд миз мйо мка мла ммо мне моз мпе мря мса мтр муз мфи мхо мци мча мши мще мъе мы мья мэр мюз мяг мёд нав нбл нве нгр нда неф нже нзу ним нй нко нла нме нну нор нпа нра нса нтр нум нфо нхр нцс нчо нш нщ нъе ны нь нэ ню ня нё оах обр овл оги оды оев оже озо ои ойк ока олт ома онь оол опе ори ост отд оул офи охр оце очь оше ощу оъх оыт оьх оэт оюз ояз оёх пар пба пве пгр пдж пек пжх пзм пид пй пка пле пме пне пор ппа при пса пти пун пфр пхи пц пч пш пщ пъ пы пье пэр пюр пят пёт рак рбу рва ргу рду рев ржа рзу риц рйм рка рло рмя рна ром рпи рр рс рта руб рфе рхи рц рч рш рщ ръ ры рь рэ рюм ря рёк саф сбо сва сгр сди сег сжа сза сил сйх ска сло смо сна сол спи сре сс стр сув сфе схл сци счи сше сщ съе сыр сьм сэс сюд сяч сём тал тбр тва тге тде тес тжа тзо тик тйм тк тлу тма тно тоц тпа тра тск тте туг тф тхо тц тч тш тще тъе тык тьф тэм тюр тяж тёз уал убр увс угл удо уе уже узк уи уйт ука ул умн ун уор уп ура усн утк yф ух уц учи уш ущ уъ уы уьх уэ ую уя уё фас фбр фви фга фде фер фжх фза фир фйх фка фло фме фны фор фпх фро фсо фто фун ффе фхъ фцх фчи фш фщ фъ фы фь фэ фю фя фёд ха хб хв хг хд хе хже хза хин хй хка хло хма хн хор хп хра хс хт хул хфа ххо хц хч хш хщ хъю хы хья хэ хю хя хё цад цбу цве цгр цдо цер цж цзя цир цйх цки цле цма цно цор цп цру цст цт цу цфт цх цца цч цш цщ цъх цы ць цэ цю цях цё чаб чба чве чгх чди чер чжу чзх чил чйх чка члю чма чны чог чпх чре чсс чту чуд чфх чхо чце чче чш чщ чъх чы чья чэх чюх чях чёр шаг шба шва шге шдо шев шж шз шиз шй шк шля шма шны шоф шпи шра шс шт шу шф шх шц шч шшо шщх шъх шы шья шэх шюр шях шёл щал щб щво щга щдр щел щжи щзо щив щйх щкр щле щм щн що щпх щре щст щтх щув щфо щху щце щчх щш щщ щъ щы щь щэ щю щях щёт ъах ъбх ъвх ъгх ъдх ъес ъжх ъзх ъиз ъйх ъкх ълх ъмн ънх ъох ъпх ърх ъсо ътх ъух ъфх ъхы ъцх ъчх ъшх ъщх ъъх ъых ъьх ъэх ъюг ъят ъём ыа ыбо ыв ыг ыд ые ыж ыз ыи ыйс ыкл ыло ыма ын ыон ыпа ыра ыс ыт ыу ыф ых ыцв ыче ыша ыще ыъх ыых ыь ыэ ыю ыя ыё ьа ьби ьвт ьго ьда ьез ьжа ьзе ьин ьйм ька ьло ьми ьне ьор ьпи ьре ься ьте ьуф ьфе ьха ьци ьче ьшо ьща ьъх ьых ььх ьэт ьют ьям ьёр эар эб эвр эго эдр эез эжо эзы эиг эйн эк эль эми эн эо эп эр эс эт эу эфи эха эце эч эш эщ эъ эы эь ээ эю эя эё юа юбк юве юго юдо юе южо юз юи юй юк юля юма юно юо юп юра юс ют юу юф юх юц юч юш ющ юъ юы юь юэ юю юя юё яар ябл яво яго яду яем яжн язг яи яйц якн ялк ям янь яо яп ярм яст яте яуз яф ях яц яч яш ящи яъх яых яьх яэх яющ яях яёх""",
    """UC-to-UC А+ МААРОВ БАБОЧЕК БЕЖАВШЕГО БЛАГА ВКЛАДЫВАЕМ ВПАДАЕТ ВРАЖДА ВЫЛАЗКА ЗАИГРАЛА КРАЙНЕГО ЛАКОМСТВА ЛАСКАЛИ ЛЕСКАМИ ЛИАНОЙ НАОБОРОТ НАПАВШИХ НАРОДАМ НАСЕСТА НАТИСК НАУКЕ НАФТАЛИНОМ НАХОДИЛА РЕПУТАЦИЕЙ РЫБАЧАЩЕГО СОГЛАШАЕТСЯ СОКРАЩАТЬ СПЛЕТАЮТСЯ БОЛЬШАЯ""",
    """+А ГОРБАТОЙ ГРИВАМИ ДВИГАВШАЯСЯ ДОГАДАВШИСЬ НЕРЕАЛЬНЫЙ НОЖАМИ ОБВЯЗАННЫЙ ОФИЦИАЛЬНО ПАЛКАМИ ПАСЛАСЬ ПЛЮМАЖИ ПОГНАЛСЯ КЛОАКА КОМПАНИЕЙ КОНТРАСТУ КУСАЕТ КУСТАМИ ВУАЛЬ ШАРФАМИ БЕЗДЫХАННОЕ БРЯЦАЮЩИЕ БУРЧАНИЯ ВМЕШАЛСЯ ВРАЩАЯСЬ""",
    """Б+ ВЫРАБАТЫВАТЬ ОББИТЫ ОБВЕВАЛ ОБГОНЯЮЩЕМ ОБДУМАВ ОБЕГАЯ ОБЖИГАЕТ ОБИДЕЛ РОБКИМ САБЛЕЙ ОБМАНАХ ОБНАЖАЯ ОБОГНАЛИ ОБРАЗАХ РАБСТВЕ ХРЕБТОМ БАБУШКА НЕОБХОДИМ ЗУБЦАМИ ОБШИРНАЯ ОБЩАЛСЯ ВСЕОБЪЕМЛЮЩИЙ ГОЛУБЫМ ДОБЬЕМСЯ КЛУБЯЩЕГОСЯ""",
    """+Б ОГРАБИЛИ ВБЕГАТЬ СОГБЕННОГО КЛАДБИЩЕ КОЛЕБАЛСЯ ЛОЖБИНЫ НЕИЗБЕЖНОЙ НИБУДЬ ПОЛБУТЫЛКИ ТУМБЫ УДОБНЕЕ УЩЕРБНАЯ СБЕГАВШЕЙ ПАСТБИЩА ПЕРЕРУБИЛ РЫБАКИ СУДЬБОЙ ВОЗЛЮБЛЕННЫЙ ЗАРЯБИЛА""",
    """В+ ЗАСТАВАЛ ВБЕЖАЛ ВВЕДЕН ВГЛУБЬ НЕПРАВДОЙ НЕУВЕРЕННО ПРЕВЗОЙДЕТ ПРЕДВИГАЛИСЬ ПРИВЛЕК СОВМЕСТНАЯ СРАВНЕНИИ СТВОЛАМИ ВПАДИНОЙ ВРАЖДА ДЕДОВСКОГО ЗАВТРАК ЗАЗВУЧАЛ ВХОДИЛИ ОВЦАМ ПЕВЧИХ ПЛЫВШЕГО ГОДОВЩИНА ВЪЕЗЖАТЬ ВЫБЕРЕМ ГОТОВЬТЕСЬ ДАВЯЩУЮ""",
    """+В ДВИГАВШАЯСЯ ЗАБВЕНИЕМ ПРИГВОЗДЕН ПРИДВИГАЛАСЬ ПРИСЕВШАЯ ЖВАЧКУ ЗАЗВЕНЕЛ ЗАЛИВАЛА БЕЗМОЛВНЫХ СИМВОЛОМ КОНВЕРТ КОРОВОЙ ОБОРВАН ОСВЕТЯТ ОТВЕДЕМ ОТДУВАТЬСЯ ПЕРЕХВАТИВ ПРОЦВЕТАЛИ БЕСПОЧВЕННО ПОДОШВАМИ ПОДПЛЫВАЛО ЛЬВИНЫЙ КЛЮВОМ КОСТЛЯВЫХ""",
    """Г+ КРУГАМИ СОГБЕННОГО ПРИГВОЗДЕН ВСЕГДАШНЯЯ ЛАГЕРЕ ЗИГЗАГООБРАЗНОЙ ИЗГИБА КОСОГЛАЗОГО ЛЯГНУЛ МНОГОГО НАГРАДА БЕГСТВА КОГТЕЙ ЛЯГУШКА ОБЛЕГЧАЛАСЬ ВТОРГШИХСЯ""",
    """+Г ДОТРАГИВАТЬСЯ ОБГОНЯЮЩЕМ ВГЛУБЬ НАДГРОБЬЯ НАЛЕГКЕ ПОДОЖДАЛ РАЗГАДАЕТ СЖИГАЮТ ВОЛГЛЫЙ ПОЛУМГЛА ФЛАНГОВ ЧЕТКОГО АРЬЕРГАРД ПОЛУСГНИВШЕГО ОТГАДАТЬ ОТПУГНУЛО ПЕРЕПРЫГИВАЛ ВУЛЬГАРНОЕ ЮГИ БРОДЯГАМИ""",
    """Д+ ВИДАМИ КЛАДБИЩЕ МЕДВЕДИЦА НАДГРОБЬЯ ПОДДАВАЛИСЬ ПОДЕВАЛИСЬ ПОДЖАРИМ ПОДЗАРАБОТАТЬ ПОДИВИЛСЯ ПОДЛЕЖИТ ПОДМИГНУЛ ПОДНЕСЛА ПОДОБАЕТ НАДПИСИ НЕДРАХ ПОДСКАЖЕТ ПОДТАЧИВАЯ ПОДУМАВ ПОДХВАТИВ ПЯТНАДЦАТИ РАЗВЕДЧИК УВЯДШЕГО ПОДЪЕЗЖАЛИ ПОДЫСКИВАЕТ СЕДЬМОГО ГАДЮКИ ГЛЯДЯЩИЕ""",
    """+Д ГРАДОМ НЕОБДУМАННЫЕ ОПРАВДАВШУЮ ВСЕГДАШНЯЯ ВЫЕДУТ ВЫНУЖДЕНЫ ГНЕЗДИЛСЯ ДОЖИДАЯСЬ ДОЙДЕМ ЗАКОЛДОВАНА КАЛЕНДАРЕ ЛОДКАМИ ЛОРДОМ СДАДУТСЯ ОТДАВАЛ ПРИБУДЕТ ДВУХДНЕВНОЙ ПЛАЦДАРМ ПРЕДЫДУЩЕГО ПЯТЬДЕСЯТ СОБЛЮДАЙТЕ УВЯДАНИЕ""",
    """Е+ ГЕНЕАЛОГИИ ГРЕБИТЕ ДЕВАЛСЯ ЕЖЕГОДНУЮ ЖАЛЕЕТ НЕВЕЖЕСТВЕНЕН НЕЗАДОЛГО ПРЕИМУЩЕСТВА РЕЙНДЖЕР САБЛЕЛЬ СВОЕВРЕМЕННАЯ СВОЕНРАВЕН СВОЕОБРАЗНОЙ СКРЕПЛЯЮЩЕГО СМЕРТНОГО СНЕСЕН СОБЕРЕТСЯ НЕУВЕРЕННО НЕХОРОША СПЕЦАЛЬНО СТЕРЕЧЬ СЪЕШЬТЕ ТРЕЩАЛ ТУСКНЕЮТ УСЕЯЛИ""",
    """+Е УСПЕВАЕШЬ ЯБЕДНИКА БЕЗВЕКИМИ ЛАГЕРЕЙ ЛЕДЕНИТ ЛЖЕЦОМ НАЗЕМЬ НЕДОЛГИЕ ФЕЙЕРВЕКОВ ФЛЕЙТАХ ХМЕЛЯ ХРАНЕНИЕ ЮЖНОЕ АППЕТИТ АПРЕЛЬСКОЕ АРСЕНАЛ АРХИТЕКТУРЕ ДУЕТ КАРТОФЕЛИН ПОХЕ ПОЦЕЛОВАВ ПОЧЕРКОВ ПОШЕВЕЛИВШИСЬ ПРОЩЕНИЯ РАЗЪЕДИНИНТЬ РВАНЫЕ РУЧЬЕВ ВОЮЕМ МЕНЯЕТСЯ""",
    """Ж+ НОЖАМИ СЛУЖБЫ ЖВАЧКУ ЗАЖГИТЕ ЗАЖДАЛАСЬ ЗАЖЕЧЬ ЗАЖЖЕНЫ ЗАЖИВЕМ НЕВЕЖЛИВО НЕЖНОСТЬ ПРОЖОРЛИВЫХ СОЖРАНА СТЫЖУСЬ МУЖЧИНАМ СВЕЖЫМ ДРОЖЬЮ""",
    """+Ж ЖАЖДАЛ ОБЖИГАЕТ ПОДЖАРИМ ПОЛЕЖАЛИ ПРИЕЗЖАЛ ПРИЖАВ ПРОДОЛЖАЯ НЕВОЗОМЖНО КИНЖАЛ КОЖАННАЯ ОДЕРЖАТЬ СЖАЛИСЬ СКОНФУЖЕН СТЫЖУСЬ ДЮЖИНА ЗАВЯЖЕТСЯ""",
    """З+ ИСЧЕЗАЛО НЕИЗБЕЖЕН НЕИЗВЕСТЕН ОБЕЗГЛАВЛЕНЫ ОПОЗДАВШИХ ОТВЕЗЕНЫ ВИЗЖАТЬ БЕЗЗАБОТНО ВИЗИТОМ ВОЗЛОЖЕНА ВОЗМЕСТИТЬ ВОЗНИК ВОЗОБЛАДАТЬ ВОЗРАЖАЕМ ГРЫЗТЬ ГРЫЗУЩИМ ОБРАЗЦУ РЕЗЧИК НИЗШИХ РАЗЪЕЗДЫ РАЗЫСКАЛ РЕЗЬБОЙ РЕЗЮМИРОВАЛ ХОЗЯЕВА""",
    """+З АЛМАЗОМ МАВЗОЛЕИ ЗИГЗАГООБРАЗНОЙ ПОДЗЕМЕЛИЙ ПОДРЕЗАВШИЙ БЕЛИЗНОЙ ПЕЙЗАЖИ ПОЛЗАЕТ КАМЗОЛЕ ПРЕТЕНЗИИ ПРОВОЗГЛАСИЛ РАЗВЕРЗШЕЙСЯ СЗАДИ ОТЗЫВАЛИСЬ ПОГРУЗИВШИСЬ РАЗГРЫЗУ СКОЛЬЗКИЕ СОЮЗАХ УВЯЗАЛИ""",
    """Г+ ГИАЦИНТОМ ГИБЕЛИ ГОВАРИВАЛ ДВИГАВШАЯСЯ ДОЖИДАЯСЬ ЗАНЯТИЕМ ЗИЖДЕТСЯ ИЗБАВИЛ КОПИИ КОПИЙ КОРЧИЛСЯ КРИМПАТУЛ КРЫСИННОЙ ЛЕГИОНАМ ЛИПКИЙ МАРШИРОВАЛА МГЛИСТЫМИ МЕДЛИТЕЛЕН ПРИУНЫЛ ГРИФЕЛЬНАЯ ДВОИХ КОННИЦА КОРИЧНЕВАЯ ЛИШАЕТ НИЩЕГО ОСТАЛИЬ ПЕНИЮ ПОЧТЕНИЯ""",
    """+И ПРИТАИЛИСЬ ПРОБИВАЕТ ПРОВИЗИИ ПРОТЯГИВАЛ РАДИУС РАССЕИВАЕТСЯ РАСХАЖИВАТЬ СБЛИЗИЛИСЬ СБЛИЗИЛИСЬ СЕДЫМИ СИДЕНИЕМ СТАНОИЛИСЬ СТОЛПИЛИСЬ СЮРПРИЗОМ ТРЯСИНОЙ УГОСТИЛИ ПОЛУИСПУГАННЫМИ САПФИРА СТИХИЯ ГИАЦИНТОМ ГОРЧИЛА ДУШИЛИ ДЫМЯЩИЙСЯ ВЫИГРАВ ОЛЕНЬИМ ХОЗЯИНОМ""",
    """Й+ ВЗОЙДЕТ ФЕЙЕРВЕКОВ ПЕЙЗАЖИ СТОЙЛА ВЗАЙМЫ ВОЙНАХ РАЙОНАМ СВОЙСТВА СМЕЙТЕСЬ СЕЙФА УБИЙЦАМ УСТОЙЧИВЕЙ МАЛЕЙШЕГО""",
    """+Й МЕШАЙТЕ МЛАДШИЙ НАЗЫВАЕМЙ ПРОСТОРЫНЙ ПРОСЬБОЙ ОХОТЙ РАДУЙТЕСЬ РОВНЫЙ ДЮЙМ ТЕРЯЙТЕ""",
    """К+ АРКАМИ БУКВАМИ ЛАКЕЕМ ТАКЖЕ ТАКИМИ НЕАККУРАТНЫЕ НЕПРЕКЛОННЫЙ ВЫСОКМИ ЗАИКНУЛСЯ ЗАКОВАТЬ ЗАКРЕПИ ЛЕКСИРЫ ОКТЯБРЬ ОТКУДА СТАРКХОРН ФУНКЦИЯМ УВЛЕКШИСЬ""",
    """+К УПАКОВАЛ ГИБКИХ КИВКАМИ ЛЕГКИЕ ЛОДКИ НАМЕКНУЛ НОЖНЫ ПОВОЗКИ ПОКРИКИВАЯ СТОЙКИЕ СТОЛКНУЛ ГРОМКИЙ ЗВОНКИЙ ИСТОКИ КРЕПКИЙ МЕРКНУВШИЙ МОРСКИЕ НАТКНУЛСЯ НЕУКЛЮЖЕ ТКАЦКИЙ БОЧКИ ДЕВУШКИ МУЗЫКИ НЯНЬКИ ТЮКИ ВСЯКИЕ""",
    """Л+ УГЛАМ ПОЛБУТЫЛКИ ЗАМОЛВИТЕ НАДОЛГО ОКОЛДОВАЛ ОЛЕДЕНИЛ ДОЛЖЕН ЗАПОЛЗАТЬ ЗАРЫЛИСЬ ИЛЛЮМИНИРОВАННЫМ ПОЛМИЛИ ПОЛНЕЙШЕМУ ПОЛОВИНА ПОЛПУТИ ПРИЖАЛСЯ БОЛТАТЬ ВГЛУБЬ СОЛЦНЕ ТОЛЧКОМ ВОЛШЕБНА ТОЛЩИНЕ ТУСКЛЫМИ УДОВОЛЬСТВИЕ УЛЮЛЮКАТЬ УМОЛЯЛИ""",
    """+Л БАЛКОЙ БЕЗОБЛАЧНО ВОВЛЕКЛО ВОЗГЛАВЛЯЕТ ДОЖДЛИВОГО ДОСТРЕЛИТЬ НЕВЕЖЛИВО НЕВЗЛЮБИЛИ НЕПОСИЛЬНЫМ СТОЙЛА АЛЛЕИ ДРЕМЛЮТ СОНЛИВ СПОЛЗАЕТ ТЕПЛАЯ ТЕРЛИСЬ ТРУСЛИВЫЕ УСТЛАНО УТКНУЛСЯ ВАФЛИ ВСХЛИПНУЛ НОЧЛЕГА ОБОШЛОСЬ ПОДОЩЛИ ПОКРЫЛАСЬ ПОКРЫЛАСЬ УЛЮЛЮКАТЬ УЧУЯЛИ""",
    """М+ ФЕРМАМИ АМБАРАМИ СИМВОЛ СТРЕМГЛАВ СУМЕРЕК НЕВОЗОМЖНО КАМЗОЛ КАМИНЕ НАЗЫВАЕМЙ ОБРАМЛЕН ОГРОМНАЯ ОСМОТРЕВ ВЫМПЕЛЫ ОМРАЧАЛО ОСТАЕМСЯ ИДЕМТЕ ИЗМУЧЕННЫЕ КОМФОРТ МХАМИ БЕЗУМЦЕВ ГРОМЧЕ САМШИТА ТЮРЕМЩИКОМ УМЫВАНИЯ ВОСЕМЬДЕСЯТ ГРЕМЯЩИМ""",
    """+М ДАМБЫ ОБМАНЕМ СОВМЕСТНО ПОДМИГНУЛ ПОДЪЕМОМ ПРЕВОЗМОЧЬ ПРЕИМУЩЕСТВА ВЗАЙМЫ ПОЛМИЛИ ПОМАНИЛ ПРОБОРМОТАЛ ПРОСМОТРЕТЬ РИТМИЧНЫЕ РУМЯНЫМ УХМЫЛЬНУЛСЯ БАШМАКАМИ БЕЗЫМЯННОГО ВЕСЬМА ПЛЮМАЖИ ПОЛЯМИ""",
    """Н+ ПОМИНАЛЬНЫЙ КОНВЕРТ ФЛАНГОВ ШЛЕНДРА ЯСЕНЕВЫЙ КИНЖАЛ ПРЕТЕНЗИИ ПРИНИМАЕМ ПРОСТОРЫНЙ СОНЛИВОСТИ СОННЫЕ СОСНОВОМ ПОНРАВИТЬСЯ СТРАНСТВИЕ ФАНТАЗИИ ШЕПНУЛ ИНФОРМАЦИЯ КАРМАНЦАХ КОНЧАВШИЙСЯ ПЛАНШИР ПОГОНЩИК ПОДОБНЫМИ ПОМЕНЬШЕ ПОНЮХАЛ ПОНЯВШИЙ""",
    """+Н ПОРАНЕНА ПОТРЕБНОСТИ РАВНИНА РАЗГНЕВАЛ РОДНИКОВ РОЖДЕННЫЕ СЛОЖНЕЕ СОЗНАВАТЬ СОЧИНЕНИЯ СПОКОЙНОЙ БЕССОЛНЕЧНОГО ВОСЕМНАДЦАТИ ВЫГОНЯЮТ ДОСТУПНЫМИ ЗАРНИЦА ИСКУСНЫМИ КУРЯТНИКЕ ЛУННАЯ МАХНУЛ МЕЧНИКИ ОРЕШНИКА ПОМОЩНИКОВ ПУСТЫНЕН ПЫЛЬНОЙ СЛЮНТЯЯ СТЕКЛЯННОЙ""",
    """О+ КЛОАКА АКРОБАТИКОЙ АЛЬКОВЫ БЛАГОГОВЕЙНОГО БЛАГОДАРЕН БОЕВОЙ ВЛОЖИВ ВОЗБУЖДЕНА ВОИНАМИ ВОЙДЕТЕ ВПОЛГОЛОСА ВСПОМИНАЕТ ВЫГОНЯЮТ ЗИГЗАГООБРАЗНОЙ КОПАЙТЕ КОРАБЕЛЬНОГО КОСТЕЙ КОТЕНКА НЕДОУМЕНИЕ ПРОСТОФИЛЕЙ ПРОХЛАДА ПРОЦВЕТАЛИ ПРОЧЕГО ПРОШЕДШЕЕ ПРОЩАЕТСЯ РОВНОЫЕ РОЮТСЯ РУКОЯТКИ""",
    """+О ХАОСЕ ЯСТРЕБОВ БЕЗВОДНЫЕ БЕРЕГОВЫХ ВДОВОЛЬ ВСЕОБЩЕГО НОЖОМ ОБЕЗОБРАЖЕННОЙ ПРИОБОДРИВШИЕСЯ РАЙОНАМ ШАЛОПАЙ ЮМОРУ ЮНОГО ВОСПОЛНИТЬ ВПРОЧЕМ ВЫСОВЫВАЛИ ВЫСТОЯЛ ПОЛУОТКРЫТА БЕСФОРМЕННАЯ ВЕРХОВАЯ ОТЦОВСКОГО БОЧОНКА МЕШОЧЕК ЧАЩОБУ БАТАЛЬОНЫ""",
    """П+ БЕЗОПАСЕН БЕЗУСПЕШНО ВОПИЛИ ВОПЛОТИЛИСЬ ЗАПНУВШИСЬ ЗАПОДОЗРИЛ АППЕТИТА БЕЗУПРЕЧНА РАБОЛЕПСТВОВАЛ РАСТОПТАЛИ РЕПУТАЦИЕЙ САПФИРА ПХОЖЕ ЩИПЦАМИ ТОПЧЕМСЯ ОСЛЕПШАЯ ОЩУПЫВАЛ ПОПЬЕМ КАПЮШОН КИПЯТКОМ""",
    """+П КРАПИВА СОВПАДАЕТ НАДПИСИ НЕЛЕПОСТЕЙ ПОСКРИПЫВАЛИ СТОЛПИЛИСЬ ВЫМПЕЛЫ ВЫТОПТАНА ГРУППАМИ ИСЧЕРПАНА НАСПЕХ ОТПЕЧАТКИ ОТСТУПАВШИЕ ПРИШПОРИВ ПРОСЫПАЕТСЯ СКУЛЬПТОРУ ХЛЮПАЮЩЕЕ ШЛЯПАХ""",
    """Р+ ШРАМА ВЫЩЕРБЛЕНА ИЗОРВАЛАСЬ КУРГАНА ЛОРДОМ МУДРЕЙШЕГО НАСТОРЖИЛИСЬ РАЗВЕРЗШЕЙСЯ СГОВОРИТЬСЯ СКОРЛУПКЕ СФОРМИРОВАЛСЯ ТЕРНОВНИКА ТОРОПИВШИХСЯ УЗУРПАТОРЫ БАРРИКАДЕ БАРСУКАХ ВЕРТЕЛИСЬ ВООРУЖАТЬСЯ ТОРФЯНИКОВ ВЕРХНЕГО ГАРЦУЮЩЕГО ГОРЧИЛА ЗАВЕРШЕНИЕ МОРЩИЛСЯ МУДРЫМИ ОКТЯБРЬСКОГО УГРЮМАЯ УДАРЯВШИЕ""",
    """+Р УДАРЯЛА ХРАБРЕЙШИЕ БЕЗВРЕМЕННОМ ВЗГРЫЗЛИ ВЗДРАГИВАЛ ВЗЪЕРОШЕННОЙ СОЖРАНА БЕЗРАССУДНОЙ СПИРАЛЬЮ ОМРАЧАЛО ПОНРАВИЛАСЬ ПОРАБОТАЛИ ПОСПРИНЯЛИ НЕПОСРЕДСТВЕННО ОБВЕТРЕННОГО ОБЕСКУРАЖЕНЫ РАСШИФРОВЫВАЕТСЯ СОХРАНЕНИЕ ЧРЕВЕ ШРАМА ИСПЕЩРЕННЫМ НЫРНУВ ТРОЮРОДНЫМ БОЯРЫШНИКА""",
    """С+ БРОСАВШИЙ СБЕГАВШЕЙ БЕСПРОСВЕТНОЙ НЕСГИБАЮЩИЕСЯ СДАВАЛА ВЕСЕЛА СЖАЛАСЬ СЗАДИ СИГНАЛА БЕССЛОВНЫХ БЕССМЕРТЕН БЛЕСНУЛА РИСОВАЛИ БЕЗУСПЕШНО НЕПОСРЕДСТВЕННО НЕССЯ НЕСТЕРПИМО НЕСУРАЗИЦА АТМОСФЕРЫ ВОСХВАЛЯЛИ ИСЦЕЛЕНИЕ ИСЧАХЛИ НАВИСШИЕ РАСЩЕЛИНА СЪЕДЕНЫ СЫГРАЕТ УДАЛОСЬ ВСЮДУ ВСЯКИЕ""",
    """+С ВЫБРАСЫВАЛ НЕУДОБСТВА ОТОВСЮДУ БЕГСТВА БЕДСТВИЕ ВОСКРЕСЕНЬЯ ВТИСНУТО ДЕЙСТВИЕ КАСАЛСЯ ЛАКОМСТВА СТРАНСТВИЕ СУЩНОСТИ РАБОЛЕПСТВОВАЛ ЦАРСТВЕ БОГАТСТВАХ БРУСТВЕР ССОХСЯ ПУТЕШСТВИЕ РАЗЫСКАЛ СЕЛЬСКУЮ ЧЕЛЮСТЯМИ ВЫЯСНИТЬ""",
    """Т+ ГОРТАННОМ ОТБЕЖАЛИ ЧЕТВЕРГ ОТГАДАЕТ ОТДАВАЛИ ОТЕЧЕСТВО ОТЗЫВАЛИСЬ ОТКАТИЛАСЬ ОХОТЙ ПАТЛАТЫЙ РИТМИЧНЫЕ СКРЫТНОСТЬ СМЕРТОНОСНО ОТПЕР РАССТРАИВАЮСЬ СМЕЮТСЯ АТТРАКЦИОНОВ ВСТУПАЕМ ПЛАТФОРМА ЗАТХЛЫЙ ОТЦАМИ ОТЧАИВАЕМСЯ ОБВЕТШАЛЫХ ТЩЕТНО ОТЪЕВ ОТЫСКАЛ ОХОТЬТЕСЬ АВАНТЮРИСТ БЛЕСТЯЩЕГО""",
    """+Т БЛИСТАТЕЛЬНО ОБТЕКАЯ ПОВТОРИЛ КОГТИСТЫХ ПОДТАЧИВАЯ ПОЛЕТЕЛИ ПОЛЗТИ ПОЛИТИКА ПРОЙТИ БОЛТАТЬ ИДЕМТЕ ИНТЕРВАЛАМИ КОЛОТУШКИ ПОШЕПТАТЬСЯ РАЗВЕРТЫВАЛИ РАСПУСТИВШИЙСЯ БУТЫЛИ НАФТАЛИНОМ ПИХТАМИ ПОЧТАЛЬОНЫ КАШТАНОВЫЕ КОПЫТАХ РЕЗУЛЬТАТ РОЮТСЯ РУКОЯТКОЙ""",
    """У+ ВУАЛЬЮ ВЫРУБАЛИ ДВИНУВШИСЬ ДРУГАЯ ДУДКИ ЖАЛУЕМСЯ ЖЕМЧУЖИНАМИ КУЗЕН ПОСТУИЛИ РАДУЙТЕСЬ РВАНУЛСЯ РУМЯНЫМ РУНАМИ ПОЛУОТКРЫТА ПОЛУПОДТЯГИВАЯСЬ ПУРПУРНУЮ РАСПУСКАТЬ РАСПУТИЦЫ ПОЛУУДИВЛЕННО ТУФЛИ БЛАГОУХАННЫ УЦЕЛЕВШИЕ УЧАСТВОВАЛ ХЛОПУШЕК ЦВЕТУЩЕГО ЗАСТИГНУЫЙ ЗЛУЮ ЛЮБУЯСЬ""",
    """+У НАУКЕ НЕЗАБУДКИ НОВУЮ ОТРЕГУЛИРОВАЛИ ПЕРЕДУМАЛ ПЕРЕУБЕДИЛ ПРОМЕЖУТКИ РАЗУЗНАВАЯ ТРИУМФА УГЛУБИЛАСЬ ХМУРИЛИСЬ ЩЕЛКНУЛИ БЛАГОУХАННЫ ВЫПУКЛОЕ ВЫРУБАЛИ ВЫСУНУЛ ДОСТУПЕН СКОНФУЖЕН СУХУЮ ТАНЦУЮЩИЕ УЧУЮТ ЧЕШУЕК НАЩУПАЛ ВЫУДИЛ""",
    """Ф+ ШАРФАМИ АТМОСФЕРЫ ГЕОГРАФИЧЕСКИХ ТУФЛИ БЕСФОРМЕННАЯ РАСШИФРОВЫВАЕТСЯ НАФТАЛИНОМ СКОНФУЖЕН ФФЕКТИВНЫМ ЗАФЫРКАЛ ТОРФЯНИКОВ""",
    """+Ф ШАФРАНОВОГО ГРИФЕЛЬНАЯ СЕЙФА ТРИУМФАЛЬНЫЙ ИНФОРМАЦИЕЙ КАРТОФЕЛИН САПФИРА ТОРФЯНИКОВ АТМОСФЕРЫ ПЛАТФОРМА ТУФЛИ ТЬФУ""",
    """Х+ УЕХАЛИ УХВАТИВ ДВУХДНЕВНОЙ ПОХЕ ПОХИТИТЕЛЯМИ ПОХЛЕБКУ ШАХМАТНОЙ АХНУЛИ ВЕРХОВАЯ ВИХРЕВЫЕ ДВУХСОТ ДВУХТАЖНЫХ ИСХУДАЛ ВЫСОХШЕГО СВЕРХЪЕСТЕСТВЕННЫЕ""",
    """+Х СТРАХАМ НЕОБХОДИМ ВХОД ВЪЕХАВ ДВИГАВШИХСЯ МХАМИ НЕОХОТНО ПХОЖЕ ВЕРХНЕГО ВОСХВАЛЯЛИ ЗАТХЛЫЙ КУХНЯ ЛИЧНЫХ ОЛЬХАМИ ПОНЮХАЛ СЕМЬЯХ""",
    """Ц+ СЕРДЦАМИ БЕСЦВЕТНЫЕ ПЛАЦДАРМ ПОЛИЦЕЙСКАЯ ПРОЦИТИРОВАТЬ СОЛЦНЕ ОТЦОВСКОГО ТАНЦУЮЩИЕ ЦЫПЛЯТА""",
    """+Ц ГИАЦИНТОМ ЗУБЦАМИ ОВЦАМ ОДИНАДЦАТИ СПЕЦАЛЬНО ОБРАЗЦУ ОТРИЦАТЬ УБИЙЦАМ СОЛЦНЕ ИНОЗЕМЦАМ КОНЦАМИ МНОГОЦВЕТНОЙ ЩИПЦАМИ ГАРЦУЮЩЕГО ИСЦЕЛЕНИЕ ОТЦАМИ УЦЕЛЕЕТ МЫШЦАМИ РЫЦАРЕЙ КОЛЬЦАМИ БРЯЦАЮЩИЕ""",
    """Ч+ БУРЧАНИЯ ПОЧВОЙ ПОЧЕРКОВ ПОЧИНЕННЫЙ НОЧЛЕГА НОЧНОГО БОЧОНКАХ ЧРЕВЕ МАЧТАМИ МЕЧУЩЕГОСЯ УЛУЧШАЛОСЬ БЫЧЬЕГО""",
    """+Ч ВНАЧАЛЕ ЗАБЫВЧИВ ОБЛЕГЧАЛАСЬ ПОДЧЕРКИВАЯ ПОМЕЧАЕТ МУЖЧИН НАВЯЗЧИВЕЙ НАЛИЧИИ НАСТОЙЧИВО ПОЛЧАСА ПОМЧАЛАСЬ ТОНЧАЙШИЕ ТОЧИТЕ ШЕПЧУТСЯ БУРЧАНИЯ ДОНОСЧИКОВ КРАТЧАЙШЕЙ КУЧЕРА НЕОБЫЧАЙНО ВСПЫЛЬЧИВОГО ВЬЮЧНОМУ ГОРЯЧЕГО""",
    """Ш+ ДЫШАЩЕГО ПОДОШВАМИ ПОДОШЕДШИЙ ПОШИРЕ ПОШЛЕМ БАШМАКАМИ БАШНИ КОВШОМ ПРИШПОРИВ ШРАМА ПУТЕШСТВИЕ КАШТАНОВЫЕ ПИШУТ МЫШЦАМИ СШЫЛНО СЪЕШЬТЕ""",
    """+Ш УКРАШЕН ОБШИРЕН ОДЕВШИСЬ ВТОРГШИХСЯ МЛАДШЕЙ НЕРЕШИТЕЛЬНО НИЗШИХ НИЩЕГО МАЛЕЙШЕГО ВОЛШЕБНА САМШИТА ТРАНШЕИ ХОРОШЕГО ОСЛЕПШАЯ СВЕРШИТЕ СУМАСШЕДШЕГО ОБВЕТШАЛЫХ ОБРУШАТСЯ ВЫСОХШЕГО ЛУЧШАЯ МАЛЫШАМИ МЕНЬШАЯ ДЯДЮШКИ СЕГОДНЯШНЕГО""",
    """Щ+ СМУЩАЯСЬ СМУЩЕНИЕ СООБЩИЛИ ПОДОЩЛИ ПОМОЩНИК ПЛАЩОМ УХИЩРЕНИЯ БЕГУЩУЮ ПЕРЕКРЕЩИВАЮЩХСЯ ВЕЩЬЮ""",
    """+Щ ВРАЩАЯСЬ ВСЕОБЩЕГО ГОДОВЩИНА ЗАВЕЩАЛА ЗАЩИЩАЙТЕ ТОЛЩИНЕ ТЮРЕМЩИКОМ ЖЕНЩИНА ИСТОЩИЛИ МОРЩИЛСЯ РАСЩЕЛИНА ТЩЕТНО ТЯНУЩЕГО ВЫЩЕРБЛЕНА КУРИЛЬЩИКАМИ КУСАЮЩИЕСЯ ЛЕТЯЩИЕ""",
    """Ъ+ ОБЪЕДИНЕНИЕ ОБЪЯВИЛ""",
    """+Ъ ОБЪЯВИЛ ВЪЕЗД ПОДЪЕЗЖАЛИ РАЗЪЕДИНИНТЬ СЪЕДЕНЫ ОТЪЕВ СВЕРХЪЕСТЕСТВЕННЫЕ""",
    """Ы+ УЛЫБАЕТСЯ УМЫВАНИЯ ВСПРЫГИВАЯ ВЫДАВАЛ ДУРНЫЕ ЛОДЫЖЕК ОГРЫЗНУЛСЯ ВЫИГРАВ ВЫЙДЕМ ВЫЛАЗКА ВЫМАЗАН ВЫНЕС ВЫПАВШИЙ ВЫРАЖАЛ ВЫСЕКЛИ ВЫТАЩЕНЫ ВЫУДИЛ ВЫХВАТИВ ВЫЦВЕЛ ВЫЧИСТИЛ ВЫШИНЕ ВЫЩЕРБЛЕНА ВЫЯСНИТЬ""",
    """+Ы ГОЛУБЫМ ГОТОВЫЙ ДОГАДЫВАЕТЕСЬ СВЕЖЫМ СВЯЗЫВАВШЕГО СЛЫХАЛ СМЫВАЕТ СОЛЕНЫЙ РОВНОЫЕ СВИРЕПЫЙ СЕРЫЙ УСЫНОВЛЕНИЕ УТЫКАН ЗАСТИГНУЫЙ ЗАФЫРКАЛ ПТИЦЫ СШЫЛНО""",
    """Ь+ БОРЬБОЙ ЛЬВИНЫЙ ВУЛЬГАРНОЕ ГЕРОЛЬДИЧЕСКИЕ ДОБЬЕМСЯ ИСПОЛЬЗОВАЛ ОЛЕНЬИМ ПИСЬМЕНА ПЫЛЬНАЯ БАТАЛЬОНЫ СКУЛЬПТОРУ СОРИТЬСЯ РЕЗУЛЬТАТ ТЬФУ ОЛЬХАМИ ПАЛЬЦЫ ВСПЫЛЬЧИВОГО МЕНЬШИЕ НОСИЛЬЩИКАМ ПАСТЬЮ ПЕРЬЯМИ""",
    """+Ь ПОБЬЕТ СЫНОВЬЯМИ ХОДЬБЕ ДРОЖЬЮ ДРУЗЬЯМИ ОСТАЛИЬ ОСТАЛЬНАЯ СЕМЬИ СИДЕНЬЮ КОПЬЕМ НАГОРЬЮ НАХОДЯСЬ НАЧАТЬСЯ НИЧЬЯ ПОЕШЬТЕ ПОМОЩЬЮ""",
    """Э+ ЭБОНИТ ЭВАКУАЦИЯ ЭГЛАНТЕРИЯ ЭДИП ЭЙФОРИЯ ЭКСТРАКТ ЭЛЕМЕНТ ЭМАЛИРОВАНИЕ ЭНЕРГИЯ ЭПИГРАФ ЭРЕКЦИЯ ЭСКАДРОН ЭТАЖЕ ЭФИОПСКИЙ ЭХО ЭШЕЛОН""",
    """+Э АЭРОСАНИ МОЗГРОМБЭНЦЕФАЛОН САЛЬПИНГЭКТОМИЯ ПРЕЭКЛАМПСИЯ ДЗЭН ОВАРИЭКТОМИЯ МЭРА КОЭФФИЦИЕНТ ПЭРА НЕВРЭКТОМИЯ СЭР КВИНТЭССЕНЦИЯ ПИРУЭТ""",
    """Ю+ ВОЗЛЮБЛЕННЫЙ КЛЮВОМ ЮГИ БЕЗЛЮДНЫХ ВОЮЕМ ДЮЖИНА СОЮЗНИКАМИ ДЮЙМОВ ЗАУЛЮЛЮКАЛИ ИЛЛЮМИНИРОВАННЫМ ИЮНЬ ХЛЮПАЮЩЕЕ ЮРКНУЛ ЯВЛЮСЬ АБСОЛЮТНАЯ БРЮХО ДЯДЮШКИ ЖУЮЩЕЙ ВЕЧЕРНЮЮ ВОЮЯ""",
    """+Ю ВПАДАЮЩИХ ГАДЮКИ ГРЕЮЩЕГОСЯ РЕЗЮМИРОВАЛ СГНИЮТ СЛЮНА ВИНЮ ВОЮЕМ КАПЮШОН КАСТРЮЛИ ОТСЮДА ТЮКИ УЧУЮТ ЧАСТЬЮ ЗИЯЮЩАЯ""",
    """Я+ ЗЯБЛИКА КУДРЯВЕЙ ЛЯГНУЛ НАРЯДАМИ ОХРАНЯЕМОГО ПОТЯЖЕЛЕЛО ПРИВЯЗАНА ХОЗЯИНА ХОЗЯЙКОЙ ШЛЯЛСЯ ЯМКУ ЯМЫ БЕЗЫМЯННОГО ТРЯПКИ БОЯРЫШНИКА БОЯСЬ БОЯТЬСЯ ВИХРЯХ БРЯЦАЮЩИЕ ВИСЯЧИХ СЕГОДНЯШНИЙ СИДЯЩИЕ СИЯЮЩАЯ СРЕДНЯЯ""",
    """+Я СТАЯМИ ТРУБЯЩИХ УВЯДАЕТ УХОДЯЩАЯ БЕЗДЕЯТЕЛЕН ВЗЯЛИ ВЛИЯНИЕ ВОПЛЯМИ ГРЕМЯЩИМ ДНЯМИ НАСТОЯЩАЯ СКРИПЯЩИХ СМОТРЯЩИЕ СОРВАЛСЯ СОСТЯЗАНИИ СТАТУЯМИ ТОРФЯНИКОВ ИЗЪЯЗВИЛИ ВЫЯСНИЛОСЬ ДЕРЕВЬЯМИ ВОЮЯ""",
    """UC-to-LC  Абсолютная Авангард Ага Ада Ажурная Аккуратно Алая Амбар Анемонами Аплодировали Аргументы Атака Аудитории Ахнули Бабочек Бдений Бег Библиотек Блага Бобов Браконьеров Бугра Бывает Бьет Важен Вбегать Введен Вглубь Вдавалась Ведении Взад Вид Вкладываем Владевшего Вместе Вначале Вовлекло Впавшие Враг Всадник Втащил Вуаль Вход Вцепившись Вчера Въезд Выбегавшей Вьется Вяз Гаваней Гвардейцев Где Гей Гиацинтом Глав Гнал Говаривал Грабежа Губ Дав Два Девал Диван Длилась Дна Добавив Драгоценен Дуб Дыбом Дьявола Дюжин Дяди Его Еда Ежевика Езда Еле Ему Ерунда Если Ехал Ешь Еще Жабу Жвачку Жгли Ждавшая Жевал Жжет Жив Жребий Жует Забавляла Звавший Здание Зевак Зигзагообразной Зла Змеи Знавал Зов Зрачки Зуб Зяблика Ибо Ивами Игл Идеей Избавившись Или Имевшие Иначе Ирония Искажает Итак Ища Июль Кабан Квадратная Кедра Кивает Кладбище Книг Кобыла Крадешь Кскорт Кто Кубка Лабиринтах Лба Лгал Лебедей Лжет Лианой Лоб Луг Лысой Ль Любая Ля Мааров Мблема Мгла Мебели Миг Младшей Мне Мог Мр Мстить Мудр Мха Мчал Мщения Мыла Мягка Набалдашником Неаккуратные Нибудь Нобходимо Нравилась Нужда Ными Нюх Нянчить Оба Овальное Огибает Одевали Ожерелье Озабочен Ока Олдарок Омою Она Опавшей Орали Осада Отбежал Официально Охапка Оценив Очаг Ошарашены Ощетинившись Павильон Певец Пива Плавал Пни Побаивалось Прав Пса Птенца Пугает Пхоже Пчела Пшеница Пылавшего Пьедестал Пятам Ра Рва Ре Ржавеет Ринулись Робки Рта Рубашка Ры Ряби Сабель Сбегавшей Свадебный Сгибал Сдавала Себе Сжав Сзади Сигнал Скаал Слаб Смазал Сна Собак Спавшее Ср Ссора Ста Субботу Сформировался Схватив Счастлив Сшитый Съедены Сыграет Сюда Сядем Та Твари Тебе Ти Тканей Тлела То Трав Ту Тщательнее Тыл Тьма Тюк Тяготели Убаюканный Уважаем Угадавший Удав Уединении Ужами Узами Уйдем Указал Улавливал Ума Унаследовала Упав Ура Усадил Утаили Уха Уцелевшие Участвовал Ушам Ущелий Уют Фавориты Фейервеков Фигур Флаг Фокусник Фразу Функциям Ффективным Фыркала Ха Хвалебную Хижин Хладнокровие Хмеля Хныкал Хо Храбр Худ Царапался Цвели Цела Циновка Цоканье Цыплята Чадящих Чего Чинят Член Чреве Чтения Чувств Чье Шаг Швырнув Шевелил Шило Шкатулку Шла Шныряет Шок Шпилем Шрам Шторм Шум Щебет Щипайся Щупалец Юга Южан Юмору Юная Юркает Ябедника Явившегося Ягод Яда Язва Яйцах Якобы Яма Ярд Ясен Ящик""",
    """а+ мааров бабочек бежавшего блага вкладываем впадает вражда вылазка заиграла крайнего лакомства ласкали лесками лианой наоборот напавших народам насеста натиск науке нафталином находила репутацией рыбачащего соглашается сокращать сплетаются большая""",
    """+а горбатой гривами двигавшаяся догадавшись нереальный ножами обвязанный официально палками паслась плюмажи погнался клоака компанией контрасту кусает кустами вуаль шарфами бездыханное бряцающие бурчания вмешался вращаясь""",
    """б+ вырабатывать оббиты обвевал обгоняющем обдумав обегая обжигает обидел робким саблей обманах обнажая обогнали образах рабстве хребтом бабушка необходим зубцами обширная общался всеобъемлющий голубым добьемся клубящегося""",
    """+б ограбили вбегать согбенного кладбище колебался ложбины неизбежной нибудь полбутылки тумбы удобнее ущербная сбегавшей пастбища перерубил рыбаки судьбой возлюбленный зарябила""",
    """в+ заставал вбежал введен вглубь неправдой неуверенно превзойдет предвигались привлек совместная сравнении стволами впадиной вражда дедовского завтрак зазвучал входили овцам певчих плывшего годовщина въезжать выберем готовьтесь давящую""",
    """+в двигавшаяся забвением пригвозден придвигалась присевшая жвачку зазвенел заливала безмолвных символом конверт коровой оборван осветят отведем отдуваться перехватив процветали беспочвенно подошвами подплывало львиный клювом костлявых""",
    """г+ кругами согбенного пригвозден всегдашняя лагере зигзагообразной изгиба косоглазого лягнул многого награда бегства когтей лягушка облегчалась вторгшихся""",
    """+г дотрагиваться обгоняющем вглубь надгробья налегке подождал разгадает сжигают волглый полумгла флангов четкого арьергард полусгнившего отгадать отпугнуло перепрыгивал вульгарное юги бродягами""",
    """д+ видами кладбище медведица надгробья поддавались подевались поджарим подзаработать подивился подлежит подмигнул поднесла подобает надписи недрах подскажет подтачивая подумав подхватив пятнадцати разведчик увядшего подъезжали подыскивает седьмого гадюки глядящие""",
    """+д градом необдуманные оправдавшую всегдашняя выедут вынуждены гнездился дожидаясь дойдем заколдована календаре лодками лордом сдадутся отдавал прибудет двухдневной плацдарм предыдущего пятьдесят соблюдайте увядание""",
    """е+ генеалогии гребите девался ежегодную жалеет невежественен незадолго преимущества рейнджер саблель своевременная своенравен своеобразной скрепляющего смертного снесен соберется неуверенно нехороша спецально стеречь съешьте трещал тускнеют усеяли""",
    """+е успеваешь ябедника безвекими лагерей леденит лжецом наземь недолгие фейервеков флейтах хмеля хранение южное аппетит апрельское арсенал архитектуре дует картофелин похе поцеловав почерков пошевелившись прощения разъедининть рваные ручьев воюем меняется""",
    """ж+ ножами службы жвачку зажгите заждалась зажечь зажжены заживем невежливо нежность прожорливых сожрана стыжусь мужчинам свежым дрожью""",
    """+ж жаждал обжигает поджарим полежали приезжал прижав продолжая невозомжно кинжал кожанная одержать сжались сконфужен стыжусь дюжина завяжется""",
    """з+ исчезало неизбежен неизвестен обезглавлены опоздавших отвезены визжать беззаботно визитом возложена возместить возник возобладать возражаем грызть грызущим образцу резчик низших разъезды разыскал резьбой резюмировал хозяева""",
    """+з алмазом мавзолеи зигзагообразной подземелий подрезавший белизной пейзажи ползает камзоле претензии провозгласил разверзшейся сзади отзывались погрузившись разгрызу скользкие союзах увязали""",
    """г+ гиацинтом гибели говаривал двигавшаяся дожидаясь занятием зиждется избавил копии копий корчился кримпатул крысинной легионам липкий маршировала мглистыми медлителен приуныл грифельная двоих конница коричневая лишает нищего осталиь пению почтения""",
    """+и притаились пробивает провизии протягивал радиус рассеивается расхаживать сблизились сблизились седыми сидением станоились столпились сюрпризом трясиной угостили полуиспуганными сапфира стихия гиацинтом горчила душили дымящийся выиграв оленьим хозяином""",
    """й+ взойдет фейервеков пейзажи стойла взаймы войнах районам свойства смейтесь сейфа убийцам устойчивей малейшего""",
    """+й мешайте младший называемй просторынй просьбой охотй радуйтесь ровный дюйм теряйте""",
    """к+ арками буквами лакеем также такими неаккуратные непреклонный высокми заикнулся заковать закрепи лексиры октябрь откуда старкхорн функциям увлекшись""",
    """+к упаковал гибких кивками легкие лодки намекнул ножны повозки покрикивая стойкие столкнул громкий звонкий истоки крепкий меркнувший морские наткнулся неуклюже ткацкий бочки девушки музыки няньки тюки всякие""",
    """л+ углам полбутылки замолвите надолго околдовал оледенил должен заползать зарылись иллюминированным полмили полнейшему половина полпути прижался болтать вглубь солцне толчком волшебна толщине тусклыми удовольствие улюлюкать умоляли""",
    """+л балкой безоблачно вовлекло возглавляет дождливого дострелить невежливо невзлюбили непосильным стойла аллеи дремлют сонлив сползает теплая терлись трусливые устлано уткнулся вафли всхлипнул ночлега обошлось подощли покрылась покрылась улюлюкать учуяли""",
    """м+ фермами амбарами символ стремглав сумерек невозомжно камзол камине называемй обрамлен огромная осмотрев вымпелы омрачало остаемся идемте измученные комфорт мхами безумцев громче самшита тюремщиком умывания восемьдесят гремящим""",
    """+м дамбы обманем совместно подмигнул подъемом превозмочь преимущества взаймы полмили поманил пробормотал просмотреть ритмичные румяным ухмыльнулся башмаками безымянного весьма плюмажи полями""",
    """н+ поминальный конверт флангов шлендра ясеневый кинжал претензии принимаем просторынй сонливости сонные сосновом понравиться странствие фантазии шепнул информация карманцах кончавшийся планшир погонщик подобными поменьше понюхал понявший""",
    """+н поранена потребности равнина разгневал родников рожденные сложнее сознавать сочинения спокойной бессолнечного восемнадцати выгоняют доступными зарница искусными курятнике лунная махнул мечники орешника помощников пустынен пыльной слюнтяя стеклянной""",
    """о+ клоака акробатикой альковы благоговейного благодарен боевой вложив возбуждена воинами войдете вполголоса вспоминает выгоняют зигзагообразной копайте корабельного костей котенка недоумение простофилей прохлада процветали прочего прошедшее прощается ровноые роются рукоятки""",
    """+о хаосе ястребов безводные береговых вдоволь всеобщего ножом обезображенной приободрившиеся районам шалопай юмору юного восполнить впрочем высовывали выстоял полуоткрыта бесформенная верховая отцовского бочонка мешочек чащобу батальоны""",
    """п+ безопасен безуспешно вопили воплотились запнувшись заподозрил аппетита безупречна раболепствовал растоптали репутацией сапфира пхоже щипцами топчемся ослепшая ощупывал попьем капюшон кипятком""",
    """+п крапива совпадает надписи нелепостей поскрипывали столпились вымпелы вытоптана группами исчерпана наспех отпечатки отступавшие пришпорив просыпается скульптору хлюпающее шляпах""",
    """р+ шрама выщерблена изорвалась кургана лордом мудрейшего насторжились разверзшейся сговориться скорлупке сформировался терновника торопившихся узурпаторы баррикаде барсуках вертелись вооружаться торфяников верхнего гарцующего горчила завершение морщился мудрыми октябрьского угрюмая ударявшие""",
    """+р ударяла храбрейшие безвременном взгрызли вздрагивал взъерошенной сожрана безрассудной спиралью омрачало понравилась поработали посприняли непосредственно обветренного обескуражены расшифровывается сохранение чреве шрама испещренным нырнув троюродным боярышника""",
    """с+ бросавший сбегавшей беспросветной несгибающиеся сдавала весела сжалась сзади сигнала бессловных бессмертен блеснула рисовали безуспешно непосредственно несся нестерпимо несуразица атмосферы восхваляли исцеление исчахли нависшие расщелина съедены сыграет удалось всюду всякие""",
    """+с выбрасывал неудобства отовсюду бегства бедствие воскресенья втиснуто действие касался лакомства странствие сущности раболепствовал царстве богатствах бруствер ссохся путешствие разыскал сельскую челюстями выяснить""",
    """т+ гортанном отбежали четверг отгадает отдавали отечество отзывались откатилась охотй патлатый ритмичные скрытность смертоносно отпер расстраиваюсь смеются аттракционов вступаем платформа затхлый отцами отчаиваемся обветшалых тщетно отъев отыскал охотьтесь авантюрист блестящего""",
    """+т блистательно обтекая повторил когтистых подтачивая полетели ползти политика пройти болтать идемте интервалами колотушки пошептаться развертывали распустившийся бутыли нафталином пихтами почтальоны каштановые копытах результат роются рукояткой""",
    """у+ вуалью вырубали двинувшись другая дудки жалуемся жемчужинами кузен постуили радуйтесь рванулся румяным рунами полуоткрыта полуподтягиваясь пурпурную распускать распутицы полуудивленно туфли благоуханны уцелевшие участвовал хлопушек цветущего застигнуый злую любуясь""",
    """+у науке незабудки новую отрегулировали передумал переубедил промежутки разузнавая триумфа углубилась хмурились щелкнули благоуханны выпуклое вырубали высунул доступен сконфужен сухую танцующие учуют чешуек нащупал выудил""",
    """ф+ шарфами атмосферы географических туфли бесформенная расшифровывается нафталином сконфужен ффективным зафыркал торфяников""",
    """+ф шафранового грифельная сейфа триумфальный информацией картофелин сапфира торфяников атмосферы платформа туфли тьфу""",
    """х+ уехали ухватив двухдневной похе похитителями похлебку шахматной ахнули верховая вихревые двухсот двухтажных исхудал высохшего сверхъестественные""",
    """+х страхам необходим вход въехав двигавшихся мхами неохотно пхоже верхнего восхваляли затхлый кухня личных ольхами понюхал семьях""",
    """ц+ сердцами бесцветные плацдарм полицейская процитировать солцне отцовского танцующие цыплята""",
    """+ц гиацинтом зубцами овцам одинадцати спецально образцу отрицать убийцам солцне иноземцам концами многоцветной щипцами гарцующего исцеление отцами уцелеет мышцами рыцарей кольцами бряцающие""",
    """ч+ бурчания почвой почерков починенный ночлега ночного бочонках чреве мачтами мечущегося улучшалось бычьего""",
    """+ч вначале забывчив облегчалась подчеркивая помечает мужчин навязчивей наличии настойчиво полчаса помчалась тончайшие точите шепчутся бурчания доносчиков кратчайшей кучера необычайно вспыльчивого вьючному горячего""",
    """ш+ дышащего подошвами подошедший пошире пошлем башмаками башни ковшом пришпорив шрама путешствие каштановые пишут мышцами сшылно съешьте""",
    """+ш украшен обширен одевшись вторгшихся младшей нерешительно низших нищего малейшего волшебна самшита траншеи хорошего ослепшая свершите сумасшедшего обветшалых обрушатся высохшего лучшая малышами меньшая дядюшки сегодняшнего""",
    """щ+ смущаясь смущение сообщили подощли помощник плащом ухищрения бегущую перекрещивающхся вещью""",
    """+щ вращаясь всеобщего годовщина завещала защищайте толщине тюремщиком женщина истощили морщился расщелина тщетно тянущего выщерблена курильщиками кусающиеся летящие""",
    """ъ+ объединение объявил""",
    """+ъ объявил въезд подъезжали разъедининть съедены отъев сверхъестественные""",
    """ы+ улыбается умывания вспрыгивая выдавал дурные лодыжек огрызнулся выиграв выйдем вылазка вымазан вынес выпавший выражал высекли вытащены выудил выхватив выцвел вычистил вышине выщерблена выяснить""",
    """+ы голубым готовый догадываетесь свежым связывавшего слыхал смывает соленый ровноые свирепый серый усыновление утыкан застигнуый зафыркал птицы сшылно""",
    """ь+ борьбой львиный вульгарное герольдические добьемся использовал оленьим письмена пыльная батальоны скульптору сориться результат тьфу ольхами пальцы вспыльчивого меньшие носильщикам пастью перьями""",
    """+ь побьет сыновьями ходьбе дрожью друзьями осталиь остальная семьи сиденью копьем нагорью находясь начаться ничья поешьте помощью""",
    """э+ эбонит эвакуация эглантерия эдип эйфория экстракт элемент эмалирование энергия эпиграф эрекция эскадрон этаже эфиопский эхо эшелон""",
    """+э аэросани мозгромбэнцефалон сальпингэктомия преэклампсия дзэн овариэктомия мэра коэффициент пэра неврэктомия сэр квинтэссенция пируэт""",
    """ю+ возлюбленный клювом юги безлюдных воюем дюжина союзниками дюймов заулюлюкали иллюминированным июнь хлюпающее юркнул явлюсь абсолютная брюхо дядюшки жующей вечернюю воюя""",
    """+ю впадающих гадюки греющегося резюмировал сгниют слюна виню воюем капюшон кастрюли отсюда тюки учуют частью зияющая""",
    """я+ зяблика кудрявей лягнул нарядами охраняемого потяжелело привязана хозяина хозяйкой шлялся ямку ямы безымянного тряпки боярышника боясь бояться вихрях бряцающие висячих сегодняшний сидящие сияющая средняя""",
    """+я стаями трубящих увядает уходящая бездеятелен взяли влияние воплями гремящим днями настоящая скрипящих смотрящие сорвался состязании статуями торфяников изъязвили выяснилось деревьями воюя""",
)

CYRILLIC_KERNING = """аабавагадаеажазаиакаламанаоапарасатауафахаацачаџашaщaъaыaьaэaюaяaђaєaїaѕaіaјaљaњaћaбаббвбгбдбебжбзбибкблбмбнбобпбрбсбтбубфбхббцбчбџбшбщбъбыбьбэбюбябђбєбїбѕбібјбљбњбћбвавбввгвдвевжвзвивквлвмвнвовпврвсвтвувфвхввцвчвџвшвщвъвывьвэвювявђвєвївѕвівјвљвњвћвгагбгвггдгегжгзгигкглгмгнгогпгргсгтгугфгхггцгчгџгшгщгъгыгьгэгюгягђгєгїгѕгігјгљгњгћгдадбдвдгддедждздидкдлдмдндодпдрдсдтдудфдхддцдчдџдшдщдъдыдьдэдюдядђдєдїдѕдідјдљдњдћдеаебевегедеежезеиекелеменеоепересетеуефехеецечеџешещеъеыеьеэеюеяеђеєеїеѕеіејељењећежажбжвжгжджежжзжижкжлжмжнжожпжржсжтжужфжхжжцжчжџжшжщжъжыжьжэжюжяжђжєжїжѕжіжјжљжњжћжзазбзвзгздзезжззизкзлзмзнзозпзрзсзтзузфзхззцзчзџзшзщзъзызьзэзюзязђзєзїзѕзізјзљзњзћзиаибивигидиеижизиикилиминиоипириситиуифихиицичиџишищиъиыиьиэиюияиђиєиїиѕиіијиљињићикакбквкгкдкекжкзкикклкмкнкокпкркскткукфкхккцкчкџкшкщкъкыкькэкюкякђкєкїкѕкікјкљкњкћклалблвлглдлелжлзлилкллмлнлолплрлслтлулфлхллцлчлџлшлщлълыльлэлюлялђлєлїлѕлілјлљлњлћлмамбмвмгмдмемжмзмимкмлммнмомпмрмсмтмумфмхммцмчмџмшмщмъмымьмэмюмямђмємїмѕмімјмљмњмћмнанбнвнгндненжнзнинкнлнмннонпнрнснтнунфнхннцнчнџншнщнъныньнэнюнянђнєнїнѕнінјнљнњнћноаобовогодоеожозоиоколомоноопоросотоуофохооцочоџошощоъоыоьоэоюояођоєоїоѕоіојољоњоћопапбпвпгпдпепжпзпипкплпмпнпоппрпсптпупфпхппцпчпџпшпщпъпыпьпэпюпяпђпєпїпѕпіпјпљпњпћпрарбрвргрдрержрзриркрлрмрнрорпррсртрурфрхррцрчрџршрщрърырьрэрюрярђрєрїрѕрірјрљрњрћрсасбсвсгсдсесжсзсискслсмснсоспсрсстсусфсхссцсчсџсшсщсъсысьсэсюсясђсєсїсѕсісјсљсњсћстатбтвтгтдтетжтзтитктлтмтнтотптртсттутфтхттцтчтџтштщтътытьтэтютятђтєтїтѕтітјтљтњтћтуаубувугудуеужузуиукулумунуоупурусутууфухууцучуџушущуъуыуьуэуюуяуђуєуїуѕуіујуљуњућуфафбфвфгфдфефжфзфифкфлфмфнфофпффрфсфтфуффхфцфчфџфшфщфъфыфьфэффюфяфђфєфїфѕфіфјфљфњфћф
хахбхвхгхдхехжхзхихкхлхмхнхохпхрхсхтхухфхххцхчхџхшхщхъхыхьхэхюхяхђхєхїхѕхіхјхљхњхћхцацбцвцгцдцецжцзцицкцлцмцнцоцпцрцсцтцуцфцхцццчцџцшцщцъцыцьцэцюцяцђцєцїцѕціцјцљцњцћцчачбчвчгчдчечжчзчичкчлчмчнчочпчрчсчтчучфчхччцччџчшчщчъчычьчэчючячђчєчїчѕчічјчљчњчћчџаџбџвџгџдџеџжџзџиџкџлџмџнџоџпџрџсџтџуџфџхџџцџчџџшџщџъџыџьџэџюџяџђџєџїџѕџіџјџљџњџћџшашбшвшгшдшешжшзшишкшлшмшшншошпшршсштшушфшхшшцшчшџшшщшъшышьшэшюшяшђшєшїшѕшішјшљшњшћшщащбщвщгщдщещжщзщищкщлщмщнщощпщрщсщтщущщфщхщщцщчщџщшщщъщыщьщэщющящђщєщїщѕщіщјщщљщњщћщъаъбъвъгъдъеъжъзъиъкълъмънъоъпъръсътъуъфъхъъцъчъџъшъщъъыъьъэъюъяъђъєъїъѕъіъјъљъњъћъыаыбывыгыдыеыжызыиыкылымыныоыпырысытыуыфыхыыцычыџышыщыъыыьыэыюыяыђыєыїыѕыіыјыљыњыћыьаьбьвьгьдьеьжьзьиькьльмьньоьпьрьсьтьуьфьхььцьчьџьшьщьъьыььэьюьяьђьєьїьѕьіьјьљьњьћьэаэбэвэгэдэеэжэзэиэкэлэмэнэоэпэрэсэтэуэфэхээцэчэџэшэщэъэыэьээюэяэђэєэїэѕэіэјэљэњэћэюаюбювюгюдюеюжюзюиюкюлюмюнюоюпюрюсютюуюфюхююцючюџюшющюъюыюьюэююяюђюєюїюѕюіюјюљюњюћюяаябявягядяеяжязяиякялямяняояпярясятяуяфяхяяцячяџяшящяъяыяьяэяюяяђяєяїяѕяіяјяљяњяћяђађбђвђгђдђеђжђзђиђкђлђмђнђођпђрђсђтђуђфђхђђцђчђџђшђщђъђыђьђэђюђяђђєђїђѕђіђјђљђњђћђєаєбєвєгєдєеєжєзєиєкєлємєнєоєпєрєсєтєуєфєхєєцєчєџєшєщєъєыєьєэєюєяєђєєїєѕєієјєљєњєћєїаїбївїгїдїеїжїзїиїкїлїмїнїоїпїрїсїтїуїфїхїїцїчїџїшїщїъїыїьїэїюїяїђїєїїѕїіїјїљїњїћїѕаѕбѕвѕгѕдѕеѕжѕзѕиѕкѕлѕмѕнѕоѕпѕрѕсѕтѕуѕфѕхѕѕцѕчѕџѕшѕщѕъѕыѕьѕэѕюѕяѕђѕєѕїѕѕіѕјѕљѕњѕћѕіаібівігідіеіжізіиікілімініоіпірісітіуіфіхііцічіџішіщіъіыіьіэіюіяіђієіїіѕііјіљіњіћіјајбјвјгјдјејжјзјијкјлјмјнјојпјрјсјтјујфјхјјцјчјџјшјщјъјыјьјэјюјяјђјєјїјѕјіјјљјњјћјљаљбљвљгљдљељжљзљиљкљлљмљнљољпљрљсљтљуљфљхљцљчљџљшљщљъљыљьљэљюљяљђљєљїљѕљіљјљљњљћљњањбњвњгњдњењжњзњињкњлњмњнњоњпњрњсњтњуњфњхњцњчњџњшњщњъњыњьњэњюњяњђњєњїњѕњіњјњљњњћњћаћбћвћгћдћећжћзћићкћлћмћнћоћпћрћсћтћућфћхћћцћчћџћшћщћъћыћьћэћюћяћђћєћїћѕћіћјћљћњћћ
Аап Абп Авп Агп Адп Аеп Ажп Азп Аип Акп Алп Амп Анп Аоп Апп Арп Асп Атп Ауп Афп Ахп Ацп Ачп Ашп Ащп Аъп Аып Аьп Аэп Аюп Аяп Ађп Аєп Аїп Аѕп Аіп Ајп Аљп Ањп Аћп Аџп Бап Ббп Бвп Бгп Бдп Беп Бжп Бзп Бип Бкп Блп Бмп Бнп Боп Бпп Брп Бсп Бтп Буп Бфп Бхп Бцп Бчп Бшп Бщп Бъп Бып Бьп Бэп Бюп Бяп Бђп Бєп Бїп Бѕп Біп Бјп Бљп Бњп Бћп Бџп Вап Вбп Ввп Вгп Вдп Веп Вжп Взп Вип Вкп Влп Вмп Внп Воп Впп Врп Всп Втп Вуп Вфп Вхп Вцп Вчп Вшп Вщп Въп Вып Вьп Вэп Вюп Вяп Вђп Вєп Вїп Вѕп Віп Вјп Вљп Вњп Вћп Вџп Гап Гбп Гвп Ггп Гдп Геп Гжп Гзп Гип Гкп Глп Гмп Гнп Гоп Гпп Грп Гсп Гтп Гуп Гфп Гхп Гцп Гчп Гшп Гщп Гъп Гып Гьп Гэп Гюп Гяп Гђп Гєп Гїп Гѕп Гіп Гјп Гљп Гњп Гћп Гџп Дап Дбп Двп Дгп Ддп Деп Джп Дзп Дип Дкп Длп Дмп Днп Доп Дпп Дрп Дсп Дтп Дуп Дфп Дхп Дцп Дчп Дшп Дщп Дъп Дып Дьп Дэп Дюп Дяп Дђп Дєп Дїп Дѕп Діп Дјп Дљп Дњп Дћп Дџп Еап Ебп Евп Егп Едп Ееп Ежп Езп Еип Екп Елп Емп Енп Еоп Епп Ерп Есп Етп Еуп Ефп Ехп Ецп Ечп Ешп Ещп Еъп Еып Еьп Еэп Еюп Еяп Еђп Еєп Еїп Еѕп Еіп Ејп Ељп Ењп Ећп Еџп Жап Жбп Жвп Жгп Ждп Жеп Жжп Жзп Жип Жкп Жлп Жмп Жнп Жоп Жпп Жрп Жсп Жтп Жуп Жфп Жхп Жцп Жчп Жшп Жщп Жъп Жып Жьп Жэп Жюп Жяп Жђп Жєп Жїп Жѕп Жіп Жјп Жљп Жњп Жћп Жџп Зап Збп Звп Згп Здп Зеп Зжп Ззп Зип Зкп Злп Змп Знп Зоп Зпп Зрп Зсп Зтп Зуп Зфп Зхп Зцп Зчп Зшп Зщп Зъп Зып Зьп Зэп Зюп Зяп Зђп Зєп Зїп Зѕп Зіп Зјп Зљп Зњп Зћп Зџп Иап Ибп Ивп Игп Идп Иеп Ижп Изп Иип Икп Илп Имп Инп Иоп Ипп Ирп Исп Итп Иуп Ифп Ихп Ицп Ичп Ишп Ищп Иъп Иып Иьп Иэп Июп Ияп Иђп Иєп Иїп Иѕп Иіп Ијп Иљп Ињп Ићп Иџп Кап Кбп Квп Кгп Кдп Кеп Кжп Кзп Кип Ккп Клп Кмп Кнп Коп Кпп Крп Ксп Ктп Куп Кфп Кхп Кцп Кчп Кшп Кщп Къп Кып Кьп Кэп Кюп Кяп Кђп Кєп Кїп Кѕп Кіп Кјп Кљп Књп Кћп Кџп Лап Лбп Лвп Лгп Лдп Леп Лжп Лзп Лип Лкп Ллп Лмп Лнп Лоп Лпп Лрп Лсп Лтп Луп Лфп Лхп Лцп Лчп Лшп Лщп Лъп Лып Льп Лэп Люп Ляп Лђп Лєп Лїп Лѕп Ліп Лјп Лљп Лњп Лћп Лџп Мап Мбп Мвп Мгп Мдп Меп Мжп Мзп Мип Мкп Млп Ммп Мнп Моп Мпп Мрп Мсп Мтп Муп Мфп Мхп Мцп Мчп Мшп Мщп Мъп Мып Мьп Мэп Мюп Мяп Мђп Мєп Мїп Мѕп Міп Мјп Мљп Мњп Мћп Мџп Нап Нбп Нвп Нгп Ндп Неп Нжп Нзп Нип Нкп Нлп Нмп Ннп Ноп Нпп Нрп Нсп Нтп Нуп Нфп Нхп Нцп Нчп Ншп Нщп Нъп Нып Ньп Нэп Нюп Няп Нђп Нєп Нїп Нѕп Ніп Нјп Нљп Нњп Нћп Нџп Оап Обп Овп Огп Одп Оеп Ожп Озп Оип Окп Олп Омп Онп Ооп Опп Орп Осп Отп Оуп Офп Охп Оцп Очп Ошп Ощп Оъп Оып Оьп Оэп Оюп Ояп Ођп Оєп Оїп Оѕп Оіп Ојп Ољп Оњп Оћп Оџп Пап Пбп Пвп Пгп Пдп Пеп Пжп Пзп Пип Пкп Плп Пмп Пнп Поп Ппп Прп Псп Птп Пуп Пфп Пхп Пцп Пчп Пшп Пщп Пъп Пып Пьп Пэп Пюп Пяп Пђп Пєп Пїп Пѕп Піп Пјп Пљп Пњп Пћп Пџп Рап Рбп Рвп Ргп Рдп Реп Ржп Рзп Рип Ркп Рлп Рмп Рнп Роп Рпп Ррп Рсп Ртп Руп Рфп Рхп Рцп Рчп Ршп Рщп Ръп Рып Рьп Рэп Рюп Ряп Рђп Рєп Рїп Рѕп Ріп Рјп Рљп Рњп Рћп Рџп Сап Сбп Свп Сгп Сдп Сеп Сжп Сзп Сип Скп Слп Смп Снп Соп Спп Срп Ссп Стп Суп Сфп Схп Сцп Счп Сшп Сщп Съп Сып Сьп Сэп Сюп Сяп Сђп Сєп Сїп Сѕп Сіп Сјп Сљп Сњп Сћп Сџп Тап Тбп Твп Тгп Тдп Теп Тжп Тзп Тип Ткп Тлп Тмп Тнп Топ Тпп Трп Тсп Ттп Туп Тфп Тхп Тцп Тчп Тшп Тщп Тъп Тып Тьп Тэп Тюп Тяп Тђп Тєп Тїп Тѕп Тіп Тјп Тљп Тњп Тћп Тџп Уап Убп Увп Угп Удп Уеп Ужп Узп Уип Укп Улп Умп Унп Уоп Упп Урп Усп Утп Ууп Уфп Ухп Уцп Учп Ушп Ущп Уъп Уып Уьп Уэп Уюп Уяп Уђп Уєп Уїп Уѕп Уіп Ујп Уљп Уњп Ућп Уџп Фап Фбп Фвп Фгп Фдп Феп Фжп Фзп Фип Фкп Флп Фмп Фнп Фоп Фпп Фрп Фсп Фтп Фуп Ффп Фхп Фцп Фчп Фшп Фщп Фъп Фып Фьп Фэп Фюп Фяп Фђп Фєп Фїп Фѕп Фіп Фјп Фљп Фњп Фћп Фџп Хап Хбп Хвп Хгп Хдп Хеп Хжп Хзп Хип Хкп Хлп Хмп Хнп Хоп Хпп Хрп Хсп Хтп Хуп Хфп Ххп Хцп Хчп Хшп Хщп Хъп Хып Хьп Хэп Хюп Хяп Хђп Хєп Хїп Хѕп Хіп Хјп Хљп Хњп Хћп Хџп Цап Цбп Цвп Цгп Цдп Цеп Цжп Цзп Цип Цкп Цлп Цмп Цнп Цоп Цпп Црп Цсп Цтп Цуп Цфп Цхп Ццп Цчп Цшп Цщп Цъп Цып Цьп Цэп Цюп Цяп Цђп Цєп Цїп Цѕп Ціп Цјп Цљп Цњп Цћп Цџп Чап Чбп Чвп Чгп Чдп Чеп Чжп Чзп Чип Чкп Члп Чмп Чнп Чоп Чпп Чрп Чсп Чтп Чуп Чфп Чхп Чцп Ччп Чшп Чщп Чъп Чып Чьп Чэп Чюп Чяп Чђп Чєп Чїп Чѕп Чіп Чјп Чљп Чњп Чћп Чџп Ћап Ћбп Ћвп Ћгп Ћдп Ћеп Ћжп Ћзп Ћип Ћкп Ћлп Ћмп Ћнп Ћоп Ћпп Ћрп Ћсп Ћтп Ћуп Ћфп Ћхп Ћцп Ћчп Ћшп Ћщп Ћъп Ћып Ћьп Ћэп Ћюп Ћяп Ћђп Ћєп Ћїп Ћѕп Ћіп Ћјп Ћљп Ћњп Ћћп Ћџп Џап Џбп Џвп Џгп Џдп Џеп Џжп Џзп Џип Џкп Џлп Џмп Џнп Џоп Џпп Џрп Џсп Џтп Џуп Џфп Џхп Џцп Џчп Џшп Џщп Џъп Џып Џьп Џэп Џюп Џяп Џђп Џєп Џїп Џѕп Џіп Џјп Џљп Џњп Џћп Џџп Шап Шбп Швп Шгп Шдп Шеп Шжп Шзп Шип Шкп Шлп Шмп Шнп Шоп Шпп Шрп Шсп Штп Шуп Шфп Шхп Шцп Шчп Шшп Шщп Шъп Шып Шьп Шэп Шюп Шяп Шђп Шєп Шїп Шѕп Шіп Шјп Шљп Шњп Шћп Шџп Щап Щбп Щвп Щгп Щдп Щеп Щжп Щзп Щип Щкп Щлп Щмп Щнп Щоп Щпп Щрп Щсп Щтп Щуп Щфп Щхп Щцп Щчп Щшп Щщп Щъп Щып Щьп Щэп Щюп Щяп Щђп Щєп Щїп Щѕп Щіп Щјп Щљп Щњп Щћп Щџп Ъап Ъбп Ъвп Ъгп Ъдп Ъеп Ъжп Ъзп Ъип Ъкп Ълп Ъмп Ънп Ъоп Ъпп Ърп Ъсп Ътп Ъуп Ъфп Ъхп Ъцп Ъчп Ъшп Ъщп Ъъп Ъып Ъьп Ъэп Ъюп Ъяп Ъђп Ъєп Ъїп Ъѕп Ъіп Ъјп Ъљп Ъњп Ъћп Ъџп Ыап Ыбп Ывп Ыгп Ыдп Ыеп Ыжп Ызп Ыип Ыкп Ылп Ымп Ынп Ыоп Ыпп Ырп Ысп Ытп Ыуп Ыфп Ыхп Ыцп Ычп Ышп Ыщп Ыъп Ыып Ыьп Ыэп Ыюп Ыяп Ыђп Ыєп Ыїп Ыѕп Ыіп Ыјп Ыљп Ыњп Ыћп Ыџп Ьап Ьбп Ьвп Ьгп Ьдп Ьеп Ьжп Ьзп Ьип Ькп Ьлп Ьмп Ьнп Ьоп Ьпп Ьрп Ьсп Ьтп Ьуп Ьфп Ьхп Ьцп Ьчп Ьшп Ьщп Ьъп Ьып Ььп Ьэп Ьюп Ьяп Ьђп Ьєп Ьїп Ьѕп Ьіп Ьјп Ьљп Ьњп Ьћп Ьџп Эап Эбп Эвп Эгп Эдп Эеп Эжп Эзп Эип Экп Элп Эмп Энп Эоп Эпп Эрп Эсп Этп Эуп Эфп Эхп Эцп Эчп Эшп Эщп Эъп Эып Эьп Ээп Эюп Эяп Эђп Эєп Эїп Эѕп Эіп Эјп Эљп Эњп Эћп Эџп Юап Юбп Ювп Югп Юдп Юеп Южп Юзп Юип Юкп Юлп Юмп Юнп Юоп Юпп Юрп Юсп Ютп Юуп Юфп Юхп Юцп Ючп Юшп Ющп Юъп Юып Юьп Юэп Ююп Юяп Юђп Юєп Юїп Юѕп Юіп Юјп Юљп Юњп Юћп Юџп Яап Ябп Явп Ягп Ядп Яеп Яжп Язп Яип Якп Ялп Ямп Янп Яоп Япп Ярп Ясп Ятп Яуп Яфп Яхп Яцп Ячп Яшп Ящп Яъп Яып Яьп Яэп Яюп Яяп Яђп Яєп Яїп Яѕп Яіп Яјп Яљп Яњп Яћп Яџп Ђап Ђбп Ђвп Ђгп Ђдп Ђеп Ђжп Ђзп Ђип Ђкп Ђлп Ђмп Ђнп Ђоп Ђпп Ђрп Ђсп Ђтп Ђуп Ђфп Ђхп Ђцп Ђчп Ђшп Ђщп Ђъп Ђып Ђьп Ђэп Ђюп Ђяп Ђђп Ђєп Ђїп Ђѕп Ђіп Ђјп Ђљп Ђњп Ђћп Ђџп Єап Єбп Євп Єгп Єдп Єеп Єжп Єзп Єип Єкп Єлп Ємп Єнп Єоп Єпп Єрп Єсп Єтп Єуп Єфп Єхп Єцп Єчп Єшп Єщп Єъп Єып Єьп Єэп Єюп Єяп Єђп Єєп Єїп Єѕп Єіп Єјп Єљп Єњп Єћп Єџп Їап Їбп Ївп Їгп Їдп Їеп Їжп Їзп Їип Їкп Їлп Їмп Їнп Їоп Їпп Їрп Їсп Їтп Їуп Їфп Їхп Їцп Їчп Їшп Їщп Їъп Їып Їьп Їэп Їюп Їяп Їђп Їєп Їїп Їѕп Їіп Їјп Їљп Їњп Їћп Їџп Ѕап Ѕбп Ѕвп Ѕгп Ѕдп Ѕеп Ѕжп Ѕзп Ѕип Ѕкп Ѕлп Ѕмп Ѕнп Ѕоп Ѕпп Ѕрп Ѕсп Ѕтп Ѕуп Ѕфп Ѕхп Ѕцп Ѕчп Ѕшп Ѕщп Ѕъп Ѕып Ѕьп Ѕэп Ѕюп Ѕяп Ѕђп Ѕєп Ѕїп Ѕѕп Ѕіп Ѕјп Ѕљп Ѕњп Ѕћп Ѕџп Іап Ібп Івп Ігп Ідп Іеп Іжп Ізп Іип Ікп Ілп Імп Інп Іоп Іпп Ірп Ісп Ітп Іуп Іфп Іхп Іцп Ічп Ішп Іщп Іъп Іып Іьп Іэп Іюп Іяп Іђп Ієп Іїп Іѕп Ііп Іјп Іљп Іњп Іћп Іџп Јап Јбп Јвп Јгп Јдп Јеп Јжп Јзп Јип Јкп Јлп Јмп Јнп Јоп Јпп Јрп Јсп Јтп Јуп Јфп Јхп Јцп Јчп Јшп Јщп Јъп Јып Јьп Јэп Јюп Јяп Јђп Јєп Јїп Јѕп Јіп Јјп Јљп Јњп Јћп Јџп Љап Љбп Љвп Љгп Љдп Љеп Љжп Љзп Љип Љкп Љлп Љмп Љнп Љоп Љпп Љрп Љсп Љтп Љуп Љфп Љхп Љцп Љчп Љшп Љщп Љъп Љып Љьп Љэп Љюп Љяп Љђп Љєп Љїп Љѕп Љіп Љјп Љљп Љњп Љћп Љџп Њап Њбп Њвп Њгп Њдп Њеп Њжп Њзп Њип Њкп Њлп Њмп Њнп Њоп Њпп Њрп Њсп Њтп Њуп Њфп Њхп Њцп Њчп Њшп Њщп Њъп Њып Њьп Њэп Њюп Њяп Њђп Њєп Њїп Њѕп Њіп Њјп Њљп Њњп Њћп Њџп Ћап Ћбп Ћвп Ћгп Ћдп Ћеп Ћжп Ћзп Ћип Ћкп Ћлп Ћмп Ћнп Ћоп Ћпп Ћрп Ћсп Ћтп Ћуп Ћфп Ћхп Ћцп Ћчп Ћшп Ћщп Ћъп Ћып Ћьп Ћэп Ћюп Ћяп Ћђп Ћєп Ћїп Ћѕп Ћіп Ћјп Ћљп Ћњп Ћћп Ћџп
ААБАВАГАДАЕАЖАЗАИАКАЛАМАНАОАПАРАСАТАУАФАХААЦАЧАЏАШAЩAЪAЫAЬAЭAЮAЯAЂAЄAЇAЅAІAЈAЉAЊAЋAБАББВБГБДБЕБЖБЗБИБКБЛБМБНБОБПБРБСБТБУБФБХББЦБЧБЏБШБЩБЪБЫБЬБЭБЮБЯБЂБЄБЇБЅБІБЈБЉБЊБЋБВАВБВВГВДВЕВЖВЗВИВКВЛВМВНВОВПВРВСВТВУВФВХВВЦВЧВЏВШВЩВЪВЫВЬВЭВЮВЯВЂВЄВЇВЅВІВЈВЉВЊВЋВГАГБГВГГДГЕГЖГЗГИГКГЛГМГНГОГПГРГСГТГУГФГХГГЦГЧГЏГШГЩГЪГЫГЬГЭГЮГЯГЂГЄГЇГЅГІГЈГЉГЊГЋГДАДБДВДГДДЕДЖДЗДИДКДЛДМДНДОДПДРДСДТДУДФДДХДЦДЧДЏДШДЩДЪДЫДЬДЭДДЮДЯДЂДЄДЇДЅДІДЈДЉДЊДЋДЕАЕБЕВЕГЕДЕЕЖЕЗЕИЕКЕЛЕМЕНЕОЕПЕРЕСЕТЕУЕФЕХЕЕЦЕЧЕЏЕШЕЩЕЪЕЫЕЬЕЭЕЮЕЯЕЂЕЄЕЇЕЅЕІЕЈЕЉЕЊЕЋЕЖАЖБЖВЖГЖДЖЕЖЖЗЖИЖКЖЛЖМЖНЖОЖПЖРЖСЖЖТЖУЖФЖХЖЦЖЧЖЏЖШЖЩЖЪЖЫЖЬЖЭЖЮЖЯЖЂЖЖЄЖЇЖЅЖІЖЈЖЉЖЊЖЋЖЗАЗБЗВЗГЗДЗЕЗЖЗЗИЗКЗЛЗМЗНЗОЗПЗРЗСЗТЗУЗФЗХЗЗЦЗЧЗЏЗШЗЩЗЪЗЫЗЬЗЭЗЮЗЯЗЂЗЄЗЇЗЅЗІЗЈЗЉЗЊЗЋЗИАИБИВИГИДИЕИЖИЗИИКИЛИМИНИОИПИРИСИТИУИФИХИИЦИЧИЏИШИЩИЪИЫИЬИЭИЮИЯИЂИЄИЇИЅИІИЈИЉИЊИЋИКАКБКВКГКДКЕКЖКЗКИККЛКМКНКОКПКРКСКТКУКФКХККЦКЧКЏКШКЩКЪКЫКЬКЭКЮКЯКЂКЄКЇКЅКІКЈКЉКЊКЋКЛАЛБЛВЛГЛДЛЕЛЖЛЗЛИЛКЛЛМЛНЛОЛПЛРЛСЛТЛУЛФЛХЛЛЦЛЧЛЏЛШЛЩЛЪЛЫЛЬЛЭЛЮЛЯЛЂЛЄЛЇЛЅЛІЛЈЛЉЛЊЛЋЛМАМБМВМГМДМЕМЖМЗМИМКМЛММНМОМПМРМСМТМУММФМХМЦМЧМЏМШМЩМЪМЫМЬМЭММЮМЯМЂМЄМЇМЅМІМЈМЉМЊМЋМ
НАНБНВНГНДНЕНЖНЗНИНКНЛНМННОНПНРНСНТНУНФНХННЦНЧНЏНШНЩНЪНЫНЬНЭНЮНЯНЂНЄНЇНЅНІНЈНЉНЊНЋНОАОБОВОГОДОЕОЖОЗОИОКОЛОМОНООПОРОСОТОУОФОХООЦОЧОЏОШОЩОЪОЫОЬОЭОЮОЯОЂОЄОЇОЅОІОЈОЉОЊОЋОПАПБПВПГПДПЕПЖПЗПИПКПЛПМПНПОППРПСПТПУПФПХППЦПЧПЏПШПЩПЪПЫПЬПЭПЮПЯПЂПЄПЇПЅПІПЈПЉПЊПЋПРАРБРВРГРДРЕРЖРЗРИРКРЛРМРНРОРПРРСРТРУРФРХРРЦРЧРЏРШРЩРЪРЫРЬРЭРЮРЯРЂРЄРЇРЅРІРЈРЉРЊРЋРСАСБСВСГСДСЕСЖСЗСИСКСЛСМСНСОСПСРССТСУСФСХССЦСЧСЏСШСЩСЪСЫСЬСЭСЮСЯСЂСЄСЇСЅСІСЈСЉСЊСЋСТАТБТВТГТДТЕТЖТЗТИТКТЛТМТНТОТПТРТСТТУТФТХТТЦТЧТЏТШТЩТЪТЫТЬТЭТЮТЯТЂТЄТЇТЅТІТЈТЉТЊТЋТУАУБУВУГУДУЕУЖУЗУИУКУЛУМУНУОУПУРУСУТУУФУХУУЦУЧУЏУШУЩУЪУЫУЬУЭУЮУЯУЂУЄУЇУЅУІУЈУЉУЊУЋУФАФБФВФГФДФЕФЖФЗФИФКФЛФМФНФОФПФРФСФТФУФФХФЦФЧФЏФШФЩФЪФЫФЬФЭФЮФФЯФЂФЄФЇФЅФІФЈФЉФЊФЋФХАХБХВХГХДХЕХЖХЗХИХКХЛХМХНХОХПХРХСХТХУХФХХХЦХЧХЏХШХЩХЪХЫХЬХЭХЮХЯХЂХЄХЇХЅХІХЈХЉХЊХЋХЦАЦБЦВЦГЦДЦЕЦЖЦЗЦИЦКЦЛЦМЦНЦОЦПЦРЦСЦТЦУЦФЦХЦЦЧЦЏЦШЦЩЦЪЦЫЦЬЦЭЦЮЦЯЦЂЦЄЦЇЦЅЦІЦЈЦЉЦЊЦЋЦЧАЧБЧВЧГЧДЧЕЧЖЧЗЧИЧКЧЛЧМЧНЧОЧПЧРЧСЧТЧУЧФЧХЧЧЦЧЧЏЧШЧЩЧЪЧЫЧЬЧЭЧЮЧЯЧЂЧЄЧЇЧЅЧІЧЈЧЉЧЊЧЋЧЏАЏБЏВЏГЏДЏЕЏЖЏЗЏИЏКЏЛЏМЏНЏОЏПЏРЏСЏТЏУЏФЏХЏЏЦЏЧЏЏШЏЩЏЪЏЫЏЬЏЭЏЮЏЯЏЂЏЄЏЇЏЅЏІЏЈЏЉЏЊЏЋЏШАШБШВШГШДШЕШЖШЗШИШКШЛШМШНШОШПШРШШСШТШУШФШХШЦШЧШЏШШЩШЪШЫШЬШЭШЮШЯШШЂШЄШЇШЅШІШЈШШЉШЊШЋШЩАЩБЩВЩГЩДЩЕЩЖЩЗЩИЩКЩЛЩМЩНЩОЩПЩРЩСЩТЩУЩФЩХЩЦЩЧЩЏЩШЩЩЪЩЫЩЬЩЭЩЮЩЯЩЂЩЄЩЇЩЩЅЩІЩЈЩЉЩЊЩЋЩЪАЪБЪВЪГЪДЪЕЪЖЪЗЪИЪКЪЛЪМЪНЪОЪПЪРЪСЪТЪУЪФЪХЪЪЦЪЧЪЏЪШЪЩЪЪЫЪЬЪЭЪЮЪЯЪЂЪЄЪЇЪЅЪІЪЈЪЉЪЊЪЋЪЫАЫБЫВЫГЫДЫЕЫЖЫЗЫИЫКЫЛЫМЫНЫОЫПЫРЫСЫТЫУЫФЫХЫЦЫЧЫЏЫШЫЩЫЪЫЫЬЫЭЫЫЮЫЯЫЂЫЄЫЇЫЅЫІЫЈЫЉЫЊЫЋЫЬАЬБЬВЬГЬДЬЕЬЖЬЗЬИЬКЬЛЬМЬНЬОЬПЬРЬСЬТЬУЬФЬХЬЬЦЬЧЬЏЬШЬЩЬЪЬЫЬЬЭЬЮЬЯЬЂЬЄЬЇЬЅЬІЬЈЬЉЬЊЬЋЬЭАЭБЭВЭГЭДЭЕЭЖЭЗЭИЭКЭЛЭМЭНЭОЭПЭРЭСЭТЭУЭФЭХЭЭЦЭЧЭЏЭШЭЩЭЪЭЫЭЬЭЭЮЭЯЭЂЭЄЭЇЭЅЭІЭЈЭЉЭЊЭЋЭЮАЮБЮВЮГЮДЮЕЮЖЮЗЮИЮКЮЛЮМЮНЮОЮПЮРЮЮСЮТЮУЮФЮХЮЦЮЧЮЏЮШЮЩЮЪЮЫЮЬЮЭЮЮЯЮЮЂЮЄЮЇЮЅЮІЮЈЮЉЮЊЮЮЋЮ
ЯАЯБЯВЯГЯДЯЕЯЖЯЗЯИЯКЯЛЯМЯНЯОЯПЯРЯСЯТЯУЯФЯХЯЯЦЯЧЯЏЯШЯЩЯЪЯЫЯЬЯЭЯЮЯЯЂЯЄЯЇЯЅЯІЯЈЯЉЯЊЯЋЯЂАЂБЂВЂГЂДЂЕЂЖЂЗЂИЂКЂЛЂМЂНЂОЂПЂРЂСЂТЂУЂФЂХЂЦЂЧЂЏЂШЂЩЂЪЂЫЂЬЂЭЂЮЂЯЂЂЄЂЇЂЅЂІЂЈЂЉЂЊЂЋЄАЄБЄВЄГЄДЄЕЄЖЄЗЄИЄКЄЛЄМЄНЄОЄПЄРЄСЄТЄУЄФЄХЄЄЦЄЧЄЏЄШЄЩЄЪЄЫЄЬЄЭЄЮЄЯЄЂЄЄЇЄЅЄІЄЈЄЉЄЊЄЋЄЇАЇБЇВЇГЇДЇЕЇЖЇЗЇИЇКЇЛЇМЇНЇОЇПЇРЇСЇТЇУЇФЇХЇЦЇЧЇЏЇШЇЩЇЇЪЇЫЇЬЇЭЇЮЇЯЇЂЇЄЇЇЅЇІЇЈЇЉЇЊЇЋЇЅАЅБЅВЅГЅДЅЕЅЖЅЗЅИЅКЅЛЅМЅНЅОЅПЅРЅСЅТЅУЅФЅХЅЅЦЅЧЅЏЅШЅЩЅЪЅЫЅЬЅЭЅЮЅЯЅЂЅЄЅЇЅЅІЅЈЅЉЅЊЅЋЅІАІБІВІГІДІЕІЖІЗІИІКІЛІМІНІОІПІРІСІТІУІФІХІІЦІЧІЏІШІЩІЪІЫІЬІЭІЮІЯІЂІЄІЇІЅІІЈІЉІЊІЋІЈАЈБЈВЈГЈДЈЕЈЖЈЗЈИЈКЈЛЈМЈНЈОЈПЈРЈСЈТЈУЈФЈХЈЈЦЈЧЈЏЈШЈЩЈЪЈЫЈЬЈЭЈЮЈЯЈЂЈЄЈЇЈЅЈІЈЈЉЈЊЈЋЈЉАЉБЉВЉГЉДЉЕЉЖЉЗЉИЉКЉЛЉМЉНЉОЉПЉРЉСЉТЉУЉФЉХЉЦЉЧЉЏЉШЉЩЉЪЉЫЉЬЉЭЉЮЉЯЉЂЉЄЉЇЉЅЉІЉЈЉЉЊЉЋЉЊАЊБЊВЊГЊДЊЕЊЖЊЗЊИЊКЊЛЊМЊНЊОЊПЊРЊСЊТЊУЊФЊХЊЦЊЧЊЏЊШЊЩЊЪЊЫЊЬЊЭЊЮЊЯЊЂЊЄЊЇЊЅЊІЊЈЊЉЊЊЋЊЋАЋБЋВЋГЋДЋЕЋЖЋЗЋИЋКЋЛЋМЋНЋОЋПЋРЋСЋТЋУЋФЋХЋЦЋЧЋЏЋШЋЩЋЪЋЫЋЬЋЭЋЮЋЯЋЂЋЄЋЇЋЅЋІЋЈЋЉЋЊЋ
.а.б.в.г.д.е.ж.з.и.к.л.м.н.о.п.р.с.т.у.ф.х.ц.ч.џ.ш.щ.ъ.ы.ь.э.ю.я.ђ..є.ї.ѕ.і.ј.љ.њ.ћ.,а,б,в,г,д,е,ж,з,и,к,л,м,н,о,п,р,с,т,у,ф,х,ц,ч,џ,ш,щ,ъ,ы,ь,э,ю,я,ђ,.є,ї,ѕ,і,ј,љ,њ,ћ,/а/б/в/г/д/е/ж/з/и/к/л/м/н/о/п/р/с/т/у/ф/х/ц/ч/џ/ш/щ//ъ/ы/ь/э/ю/я/ђ/є/ї/ѕ/і/ј/љ/њ/ћ/\\а\\б\\в\\г\\д\\е\\ж\\з\\и\\к\\л\\м\\н\\о\\п\\р\\с\\т\\у\\ф\\х\\ц\\ч\\џ\\ш\\щ\\ъ\\ы\\ь\\э\\ю\\я\\ђ\\є\\ї\\ѕ\\і\\ј\\љ\\њ\\ћ\\а: б: в: г: д: е: ж: з: и: к: л: м: н: о: п: р: с: т: у: ф: х: ц: ч: џ: ш: щ: ъ: ы: ь: э: ю: я: ђ: є: ї: ѕ: і: ј: љ: њ: ћ: а; б; в; г; д; е; ж; з; и; к; л; м; н; о; п; р; с; т; у; ф; х; ц; ч; џ; ш; щ; ъ; ы; ь; э; ю; я; ђ; є; ї; ѕ; і; ј; љ; њ; ћ;  а! б! в! г! д! е! ж! з! и! к! л! м! н! о! п! р! с! т! у! ф! х! ц! ч! џ! ш! щ! ъ! ы! ь! э! ю! я! ђ! є! ї! ѕ! і! ј! љ! њ! ћ! а? б? в? г? д? е? ж? з? и? к? л? м? н? о? п? р? с? т? у? ф? х? ц? ч? џ? ш? щ? ъ? ы? ь? э? ю? я? ђ? є? ї? ѕ? і? ј? љ? њ? ћ? (а) (б) (в) (г) (д) (е) (ж) (з) (и) (к) (л) (м) (н) (о) (п) (р) (с) (т) (у) (ф) (х) (ц) (ч) (џ) (ш) (щ) (ъ) (ы) (ь) (э) (ю) (я) (ђ) (є) (ї) (ѕ) (і) (ј) (љ) (њ) (ћ) [а] [б] [в] [г] [д] [е] [ж] [з] [и] [к] [л] [м] [н] [о] [п] [р] [с] [т] [у] [ф] [х] [ц] [ч] [џ] [ш] [щ] [ъ] [ы] [ь] [э] [ю] [я] [ђ] [є] [ї] [ѕ] [і] [ј] [љ] [њ] [ћ]{а} {б} {в} {г} {д} {е} {ж} {з} {и} {к} {л} {м} {н} {о} {п} {р} {с} {т} {у} {ф} {х} {ц} {ч} {џ} {ш} {щ} {ъ} {ы} {ь} {э} {ю} {я} {ђ} {є} {ї} {ѕ} {і} {ј} {љ} {њ} {ћ} –а– –б– –в– –г– –д– –е– –ж– –з– –и– –к– –л– –м– –н– –о– –п– –р– –с– –т– –у– –ф– –х– –ц– –ч– –џ– –ш– –щ– –ъ– –ы– –ь– –э– –ю– –я– –ђ– –є– –ї– –ѕ– –і– –ј– –љ– –њ– –ћ– -а- -б- -в- -г- -д- -е- -ж- -з- -и- -к- -л- -м- -н- -о- -п- -р- -с- -т- -у- -ф- -х- -ц- -ч- -џ- -ш- -щ- -ъ- -ы- -ь- -э- -ю- -я- -ђ- -є- -ї- -ѕ- -і- -ј- -љ- -њ- -ћ- —а— —б— —в— —г— —д— —е— —ж— —з— —и— —к— —л— —м— —н— —о— —п— —р— —с— —т— —у— —ф— —х— —ц— —ч— —џ— —ш— —щ— —ъ— —ы— —ь— —э— —ю— —я— —ђ— —є— —ї— —ѕ— —і— —ј— —љ— —њ— —ћ— „а“ „б“ „в“ „г“ „д“ „е“ „ж“ „з“ „и“ „к“ „л“ „м“ „н“ „о“ „п“ „р“ „с“ „т“ „у“ „ф“ „х“ „ц“ „ч“ „џ“ „ш“ „щ“ „ъ“ „ы“ „ь“ „э“ „ю“ „я“ „ђ“ „є“ „ї“ „ѕ“ „і“ „ј“ „љ“ „њ“ „ћ“ «а» «б» «в» «г» «д» «е» «ж» «з» «и» «к» «л» «м» «н» «о» «п» «р» «с» «т» «у» «ф» «х» «ц» «ч» «џ» «ш» «щ» «ъ» «ы» «ь» «э» «ю» «я» «ђ» «є» «ї» «ѕ» «і» «ј» «љ» «њ» «ћ» •а•б•в•г•д•е•ж•з•и•к•л•м•н•о•п•р•с•т•у•ф•х••ц•ч•џ•ш•щ•ъ•ы•ь•э•ю•я•ђ•є•ї•ѕ•і•ј•љ•њ•ћ•·а·б·в·г·д·е·ж·з·и·к·л·м·н·о·п·р·с·т·у·ф·х·ц·ч·џ·ш·щ·ъ·ы·ь·э·ю·я·ђ·є·ї·ѕ·і·ј·љ·њ·ћ·*а*б*в*г*д*е*ж*з*и*к*л*м*н*о*п*р*с*т*у*ф*х**ц*ч*џ*ш*щ*ъ*ы*ь*э*ю*я*ђ*є*ї*ѕ*і*ј*љ*њ*ћ*†а†б†в†г†д†е†ж†з†и†к†л†м†н†о†п†р†с†т†у†ф†х†ц†ч†џ†ш†щ†ъ†ы†ь†э†ю†я†ђ†є†ї†ѕ†і†ј†љ†њ†ћ‡а‡б‡в‡г‡д‡е‡ж‡з‡и‡к‡л‡м‡н‡о‡п‡р‡с‡т‡у‡ф‡х‡ц‡ч‡џ‡ш‡щ‡ъ‡ы‡ь‡э‡ю‡я‡ђ‡є‡ї‡ѕ‡і‡ј‡љ‡њ‡ћа®б®в®г®д®е®ж®з®и®к®л®м®н®о®п®р®с®т®у®ф®х®ц®ч®џ®ш®щ®ъ®ы®ь®э®ю®я®ђ®є®ї®ѕ®і®ј®љ®њ®ћ®©а©б©в©г©д©е©ж©з©и©к©л©м©н©о©п©р©с©т©у©ф©х©ц©ч©џ©ш©щ©ъ©ы©ь©э©ю©я©ђ©є©ї©ѕ©і©ј©љ©њ©ћ@а@б@в@г@д@е@ж@з@и@к@л@м@н@о@п@р@с@т@у
ф@х@ц@ч@џ@ш@щ@ъ@ы@ь@э@ю@я@ђ@є@ї@ѕ@і@јљ@њ@ћ@а™б™в™г™д™е™ж™з™и™к™л™м™н™о™п™р™с™т™у™ф™х™ц™ч™џ™ш™щ™ъ™ы™ь™э™ю™я™ђ™є™ї™ѕ™і™ј™љ™њ™ћ™
.А.Б.В.Г.Д.Е.Ж.З.И.К.Л.М.Н.О.П.Р.С.Т.У.Ф.Х.Ц.Ч.Џ.Ш.Щ.Ъ.Ы.Ь.Э..Ю.Я.Ђ.Є.Ї.Ѕ.І.Ј.Љ.Њ.Ћ.,А,Б,В,Г,Д,Е,Ж,З,И,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Џ,Ш,Щ,Ъ,Ы,Ь,Э,,Ю,Я,Ђ,Є,Ї,Ѕ,І,Ј,Љ,Њ,Ћ,/А/Б/В/Г/Д/Е/Ж/З/И/К/Л/М/Н/О/П/Р/С/Т/У/Ф/Х/Ц/Ч/Џ//Ш/Щ/Ъ/Ы/Ь/Э/Ю/Я/Ђ/Є/Ї/Ѕ/І/Ј/Љ/Њ/Ћ/\\А\\Б\\В\\Г\\Д\\Е\\Ж\\З\\И\\К\\Л\\М\\Н\\О\\П\\Р\\С\\Т\\У\\Ф\\Х\\Ц\\Ч\\Џ\\Ш\\Щ\\Ъ\\Ы\\Ь\\Э\\Ю\\Я\\Ђ\\Є\\Ї\\Ѕ\\І\\Ј\\Љ\\Њ\\Ћ\\А: Б: В: Г: Д: Е: Ж: З: И: К: Л: М: Н: О: П: Р: С: Т: У: Ф: Х: Ц: Ч: Џ: Ш: Щ: Ъ: Ы: Ь: Э: Ю: Я: Ђ: Є: Ї: Ѕ: І: Ј: Љ: Њ: Ћ: А; Б; В; Г; Д; Е; Ж; З; И; К; Л; М; Н; О; П; Р; С; Т; У; Ф; Х; Ц; Ч; Џ; Ш; Щ; Ъ; Ы; Ь; Э; Ю; Я; Ђ; Є; Ї; Ѕ; І; Ј; Љ; Њ; Ћ;  А! Б! В! Г! Д! Е! Ж! З! И! К! Л! М! Н! О! П! Р! С! Т! У! Ф! Х! Ц! Ч! Џ! Ш! Щ! Ъ! Ы! Ь! Э! Ю! Я! Ђ! Є! Ї! Ѕ! І! Ј! Љ! Њ! Ћ! А? Б? В? Г? Д? Е? Ж? З? И? К? Л? М? Н? О? П? Р? С? Т? У? Ф? Х? Ц? Ч? Џ? Ш? Щ? Ъ? Ы? Ь? Э? Ю? Я? Ђ? Є? Ї? Ѕ? І? Ј? Љ? Њ? Ћ? (А) (Б) (В) (Г) (Д) (Е) (Ж) (З) (И) (К) (Л) (М) (Н) (О) (П) (Р) (С) (Т) (У) (Ф) (Х) (Ц) (Ч) (Џ) (Ш) (Щ) (Ъ) (Ы) (Ь) (Э) (Ю) (Я) (Ђ) (Є) (Ї) (Ѕ) (І) (Ј) (Љ) (Њ) (Ћ) [А] [Б] [В] [Г] [Д] [Е] [Ж] [З] [И] [К] [Л] [М] [Н] [О] [П] [Р] [С] [Т] [У] [Ф] [Х] [Ц] [Ч] [Џ] [Ш] [Щ] [Ъ] [Ы] [Ь] [Э] [Ю] [Я] [Ђ] [Є] [Ї] [Ѕ] [І] [Ј] [Љ] [Њ] [Ћ]{А} {Б} {В} {Г} {Д} {Е} {Ж} {З} {И} {К} {Л} {М} {Н} {О} {П} {Р} {С} {Т} {У} {Ф} {Х} {Ц} {Ч} {Џ} {Ш} {Щ} {Ъ} {Ы} {Ь} {Э} {Ю} {Я} {Ђ} {Є} {Ї} {Ѕ} {І} {Ј} {Љ} {Њ} {Ћ} –А– –Б– –В– –Г– –Д– –Е– –Ж– –З– –И– –К– –Л– –М– –Н– –О– –П– –Р– –С– –Т– –У– –Ф– –Х– –Ц– –Ч– –Џ– –Ш– –Щ– –Ъ– –Ы– –Ь– –Э– –Ю– –Я– –Ђ– –Є– –Ї– –Ѕ– –І– –Ј– –Љ– –Њ– –Ћ– -А- -Б- -В- -Г- -Д- -Е- -Ж- -З- -И- -К- -Л- -М- -Н- -О- -П- -Р- -С- -Т- -У- -Ф- -Х- -Ц- -Ч- -Џ- -Ш- -Щ- -Ъ- -Ы- -Ь- -Э- -Ю- -Я- -Ђ- -Є- -Ї- -Ѕ- -І- -Ј- -Љ- -Њ- -Ћ- —А— —Б— —В— —Г— —Д— —Е— —Ж— —З— —И— —К— —Л— —М— —Н— —О— —П— —Р— —С— —Т— —У— —Ф— —Х— —Ц— —Ч— —Џ— —Ш— —Щ— —Ъ— —Ы— —Ь— —Э— —Ю— —Я— —Ђ— —Є— —Ї— —Ѕ— —І— —Ј— —Љ— —Њ— —Ћ— „А“ „Б“ „В“ „Г“ „Д“ „Е“ „Ж“ „З“ „И“ „К“ „Л“ „М“ „Н“ „О“ „П“ „Р“ „С“ „Т“ „У“ „Ф“ „Х“ „Ц“ „Ч“ „Џ“ „Ш“ „Щ“ „Ъ“ „Ы“ „Ь“ „Э“ „Ю“ „Я“ „Ђ“ „Є“ „Ї“ „Ѕ“ „І“ „Ј“ „Љ“ „Њ“ „Ћ“ «А» «Б» «В» «Г» «Д» «Е» «Ж» «З» «И» «К» «Л» «М» «Н» «О» «П» «Р» «С» «Т» «У» «Ф» «Х» «Ц» «Ч» «Џ» «Ш» «Щ» «Ъ» «Ы» «Ь» «Э» «Ю» «Я» «Ђ» «Є» «Ї» «Ѕ» «І» «Ј» «Љ» «Њ» «Ћ» •А•Б•В•Г•Д•Е•Ж•З•И•К•Л•М•Н•О•П•Р•С•Т•У•Ф•Х•Ц•Ч•Џ•Ш•Щ•Ъ•Ы•Ь•Э•Ю•Я•Ђ•Є•Ї•Ѕ•І•Ј•Љ•Њ•Ћ•·А·Б·В·Г·Д·Е·Ж·З·И·К·Л·М·Н·О·П·Р·С·Т·У·Ф·Х·Ц·Ч·Џ·Ш·Щ·Ъ·Ы·Ь·Э··Ю·Я·Ђ·Є·Ї·Ѕ·І·Ј·Љ·Њ·Ћ·*А*Б*В*Г*Д*Е*Ж*З*И*К*Л*М*Н*О*П*Р*С*Т*У*Ф*Х*Ц*Ч*Џ**Ш*Щ*Ъ*Ы*Ь*Э*Ю*Я*Ђ*Є*Ї*Ѕ*І*Ј*Љ*Њ*Ћ*†А†Б†В†Г†Д†Е†Ж†З†И†К†Л†М†Н†О†П†Р†С†Т†У†Ф†Х†Ц†Ч†Џ†Ш†Щ†Ъ†Ы†Ь†Э†Ю†Я†Ђ†Є†Ї†Ѕ†І†Ј†Љ†Њ†Ћ‡А‡Б‡В‡Г‡Д‡Е‡Ж‡З‡И‡К‡Л‡М‡Н‡О‡П‡Р‡С‡Т‡У‡Ф‡Х‡Ц‡Ч‡Џ‡Ш‡Щ‡Ъ‡Ы‡Ь‡Э‡Ю‡Я‡Ђ‡Є‡Ї‡Ѕ‡І‡Ј‡Љ‡Њ‡ЋА®Б®В®Г®Д®Е®Ж®З®И®К®Л®М®Н®О®П®Р®С®Т®У®Ф®Х®Ц®Ч®Џ®Ш®Щ®Ъ®Ы®Ь®Э®Ю®Я®Ђ®Є®Ї®Ѕ®І®Ј®Љ®Њ®Ћ®©А©Б©В©Г©Д©Е©Ж©З©И©К©Л©М©Н©О©П©Р©С©Т©У©Ф©Х©Ц©Ч©Џ©Ш©Щ©Ъ©Ы©Ь©Э©Ю©Я©Ђ©Є©Ї©Ѕ©І©Ј©Љ©Њ©Ћ@А@Б@В@Г@Д@Е@Ж@З@И@К@Л@М@Н@О@П@Р@С@Т
У@Ф@Х@Ц@Ч@Џ@Ш@Щ@Ъ@Ы@Ь@Э@Ю@Я@Ђ@Є@Ї@ЅІ@Ј@Љ@Њ@Ћ@А™Б™В™Г™Д™Е™Ж™З™И™К™Л™М™Н™О™П™Р™С™Т™У™Ф™Х™Ц™Ч™Џ™Ш™Щ™Ъ™Ы™Ь™Э™Ю™Я™Ђ™Є™Ї™Ѕ™І™Ј™Љ™Њ™Ћ™
"""

GREEK_KERNING = """ααβαγαδαεαζαηαθαιακαλαναξαοαπαραςασαταυαφαχαψαωαβαβaβγβδβεβζβηβθβιβκβλβνβξβοβπβρβςβσβτβυβφβχβψβωβγαγβγγδγεγζγηγθγιγκγλγνγξγογπγργςγσγτγυγφγχγψγωγδαδβδγδδεδζδηδθδιδκδλδνδξδοδπδρδςδσδτδυδφδχδψδωδεαεβεγεδεεζεηεθειεκελενεξεοεπερεςεσετευεφεχεψεωεζαζβζγζδζεζζηζθζιζκζλζνζξζοζπζρζςζσζτζυζφζχζψζωζηαηβηγηδηεηζηηθηιηκηληνηξηοηπηρηςησητηυηφηχηψηωηθαθβθγθδθεθζθηθθιθκθλθνθξθοθπθθρθςθσθτθυθφθχθψθωθιαιβιγιδιειζιηιθιικιλινιξιοιπιριςισιτιυιφιχιψιωικακβκγκδκεκζκηκθκικκλκνκξκοκπκρκςκσκτκυκφκχκψκωκλαλβλγλδλελζληλθλιλκλλνλξλολπλρλςλσλτλυλφλχλψλωλνανβνγνδνενζνηνθνινκνλννξνονπνρνςνσντνυνφνχνψνωνξαξβξγξδξεξζξηξθξιξκξλξνξξοξπξρξςξσξτξυξφξχξψξωξοαοβογοδοεοζοηοθοιοκολονοξοοποροςοσοτουοφοχοψοωοπαπβπγπδπεπζπηπθπιπκπλπνπξποπρπςπσπτπυπφπχπψπωπραρβργρδρερζρηρθριρκρλρνρξρορπρρςρσρτρυρφρχρψρωρςαςβςγςδςεςζςηςθςιςκςλςνςξςοςπςρςςσςτςυςφςχςψςωςσασβσγσδσεσζσησθσισκσλσνσξσοσπσρσςσστσυσφσχσψσωστατβτγτδτετζτητθτιτκτλτντξτοτπτρτςτσττυτφτχτψτωτυαυβυγυδυευζυηυθυιυκυλυνυξυουπυρυςυσυτυυφυχυψυωυφαφβφγφδφεφζφηφθφιφκφλφνφξφοφφπφρφςφσφτφυφφχφψφωφχαχβχγχδχεχζχηχθχιχκχλχνχξχοχπχρχςχσχτχυχφχχψχωχψαψβψγψδψεψζψηψθψιψκψλψνψξψοψπψψρψςψσψτψυψφψχψψωψωαωβωγωδωεωζωηωθωιωκωλωνωξωοωωπωρωςωσωτωυωφωχωψωω
Ααπ Αβπ Αγπ Αδπ Αεπ Αζπ Αηπ Αθπ Αιπ Ακπ Αλπ Ανπ Αξπ Αοπ Αππ Αρπ Αςπ Ασπ Ατπ Αυπ Αφπ Αχπ Αψπ Αωπ Βαπ Ββπ Βγπ Βδπ Βεπ Βζπ Βηπ Βθπ Βιπ Βκπ Βλπ Βνπ Βξπ Βοπ Βππ Βρπ Βςπ Βσπ Βτπ Βυπ Βφπ Βχπ Βψπ Βωπ Γαπ Γβπ Γγπ Γδπ Γεπ Γζπ Γηπ Γθπ Γιπ Γκπ Γλπ Γνπ Γξπ Γοπ Γππ Γρπ Γςπ Γσπ Γτπ Γυπ Γφπ Γχπ Γψπ Γωπ Εαπ Εβπ Εγπ Εδπ Εεπ Εζπ Εηπ Εθπ Ειπ Εκπ Ελπ Ενπ Εξπ Εοπ Εππ Ερπ Εςπ Εσπ Ετπ Ευπ Εφπ Εχπ Εψπ Εωπ Ζαπ Ζβπ Ζγπ Ζδπ Ζεπ Ζζπ Ζηπ Ζθπ Ζιπ Ζκπ Ζλπ Ζνπ Ζξπ Ζοπ Ζππ Ζρπ Ζςπ Ζσπ Ζτπ Ζυπ Ζφπ Ζχπ Ζψπ Ζωπ Ηαπ Ηβπ Ηγπ Ηδπ Ηεπ Ηζπ Ηηπ Ηθπ Ηιπ Ηκπ Ηλπ Ηνπ Ηξπ Ηοπ Ηππ Ηρπ Ηςπ Ησπ Ητπ Ηυπ Ηφπ Ηχπ Ηψπ Ηωπ Θαπ Θβπ Θγπ Θδπ Θεπ Θζπ Θηπ Θθπ Θιπ Θκπ Θλπ Θνπ Θξπ Θοπ Θππ Θρπ Θςπ Θσπ Θτπ Θυπ Θφπ Θχπ Θψπ Θωπ Ιαπ Ιβπ Ιγπ Ιδπ Ιεπ Ιζπ Ιηπ Ιθπ Ιιπ Ικπ Ιλπ Ινπ Ιξπ Ιοπ Ιππ Ιρπ Ιςπ Ισπ Ιτπ Ιυπ Ιφπ Ιχπ Ιψπ Ιωπ Καπ Κβπ Κγπ Κδπ Κεπ Κζπ Κηπ Κθπ Κιπ Κκπ Κλπ Κνπ Κξπ Κοπ Κππ Κρπ Κςπ Κσπ Κτπ Κυπ Κφπ Κχπ Κψπ Κωπ Λαπ Λβπ Λγπ Λδπ Λεπ Λζπ Ληπ Λθπ Λιπ Λκπ Λλπ Λνπ Λξπ Λοπ Λππ Λρπ Λςπ Λσπ Λτπ Λυπ Λφπ Λχπ Λψπ Λωπ Μαπ Μβπ Μγπ Μδπ Μεπ Μζπ Μηπ Μθπ Μιπ Μκπ Μλπ Μνπ Μξπ Μοπ Μππ Μρπ Μςπ Μσπ Μτπ Μυπ Μφπ Μχπ Μψπ Μωπ Ναπ Νβπ Νγπ Νδπ Νεπ Νζπ Νηπ Νθπ Νιπ Νκπ Νλπ Ννπ Νξπ Νοπ Νππ Νρπ Νςπ Νσπ Ντπ Νυπ Νφπ Νχπ Νψπ Νωπ Ξαπ Ξβπ Ξγπ Ξδπ Ξεπ Ξζπ Ξηπ Ξθπ Ξιπ Ξκπ Ξλπ Ξνπ Ξξπ Ξοπ Ξππ Ξρπ Ξςπ Ξσπ Ξτπ Ξυπ Ξφπ Ξχπ Ξψπ Ξωπ Οαπ Οβπ Ογπ Οδπ Οεπ Οζπ Οηπ Οθπ Οιπ Οκπ Ολπ Ονπ Οξπ Οοπ Οππ Ορπ Οςπ Οσπ Οτπ Ουπ Οφπ Οχπ Οψπ Οωπ Παπ Πβπ Πγπ Πδπ Πεπ Πζπ Πηπ Πθπ Πιπ Πκπ Πλπ Πνπ Πξπ Ποπ Πππ Πρπ Πςπ Πσπ Πτπ Πυπ Πφπ Πχπ Πψπ Πωπ Ραπ Ρβπ Ργπ Ρδπ Ρεπ Ρζπ Ρηπ Ρθπ Ριπ Ρκπ Ρλπ Ρνπ Ρξπ Ροπ Ρππ Ρρπ Ρςπ Ρσπ Ρτπ Ρυπ Ρφπ Ρχπ Ρψπ Ρωπ Σαπ Σβπ Σγπ Σδπ Σεπ Σζπ Σηπ Σθπ Σιπ Σκπ Σλπ Σνπ Σξπ Σοπ Σππ Σρπ Σςπ Σσπ Στπ Συπ Σφπ Σχπ Σψπ Σωπ Ταπ Τβπ Τγπ Τδπ Τεπ Τζπ Τηπ Τθπ Τιπ Τκπ Τλπ Τνπ Τξπ Τοπ Τππ Τρπ Τςπ Τσπ Ττπ Τυπ Τφπ Τχπ Τψπ Τωπ Υαπ Υβπ Υγπ Υδπ Υεπ Υζπ Υηπ Υθπ Υιπ Υκπ Υλπ Υνπ Υξπ Υοπ Υππ Υρπ Υςπ Υσπ Υτπ Υυπ Υφπ Υχπ Υψπ Υωπ Φαπ Φβπ Φγπ Φδπ Φεπ Φζπ Φηπ Φθπ Φιπ Φκπ Φλπ Φνπ Φξπ Φοπ Φππ Φρπ Φςπ Φσπ Φτπ Φυπ Φφπ Φχπ Φψπ Φωπ Χαπ Χβπ Χγπ Χδπ Χεπ Χζπ Χηπ Χθπ Χιπ Χκπ Χλπ Χνπ Χξπ Χοπ Χππ Χρπ Χςπ Χσπ Χτπ Χυπ Χφπ Χχπ Χψπ Χωπ Ψαπ Ψβπ Ψγπ Ψδπ Ψεπ Ψζπ Ψηπ Ψθπ Ψιπ Ψκπ Ψλπ Ψνπ Ψξπ Ψοπ Ψππ Ψρπ Ψςπ Ψσπ Ψτπ Ψυπ Ψφπ Ψχπ Ψψπ Ψωπ Ωαπ Ωβπ Ωγπ Ωδπ Ωεπ Ωζπ Ωηπ Ωθπ Ωιπ Ωκπ Ωλπ Ωνπ Ωξπ Ωοπ Ωππ Ωρπ Ωςπ Ωσπ Ωτπ Ωυπ Ωφπ Ωχπ Ωψπ Ωωπ ΑΑΒΑΓΑΕΑΖΑΗΑΘΑΙΑΚΑΛΑΜΑΝΑΑΞΑΟΑΠΑΡΑΣΑΤΑΥΑΦΑΧΑΨΑΩΑΒΑΒΒΓΒΕΒΖΒΗΒΘΒΙΒΚΒΛΒΜΒΝΒΒΞΒΟΒΠΒΡΒΣΒΤΒΥΒΦΒΧΒΨΒΩΒΓΑΓΒΓΓΕΓΖΓΗΓΘΓΙΓΚΓΛΓΜΓΝΓΞΓΟΓΠΓΡΓΣΓΤΓΥΓΦΓΧΓΨΓΩΓΕΑΕΒΕΓΕΕΖΕΗΕΘΕΙΕΚΕΛΕΜΕΝΕΞΕΟΕΠΕΡΕΣΕΤΕΥΕΦΕΧΕΨΕΩΕΖΑΖΒΖΓΖΕΖΖΗΖΘΖΙΖΚΖΛΖΜΖΝΖΞΖΟΖΠΖΡΖΣΖΤΖΥΖΦΖΧΖΨΖΩΖΗΑΗΒΗΓΗΕΗΖΗΗΘΗΙΗΚΗΛΗΜΗΝΗΗΞΗΟΗΠΗΡΗΣΗΤΗΥΗΦΗΧΗΨΗΩΗΘΑΘΒΘΓΘΕΘΖΘΗΘΘΙΘΚΘΛΘΜΘΝΘΘΞΘΟΘΠΘΡΘΣΘΤΘΥΘΦΘΧΘΨΘΩΘΙΑΙΒΙΓΙΕΙΖΙΗΙΘΙΙΚΙΛΙΜΙΝΙΞΙΟΙΠΙΡΙΣΙΤΙΥΙΦΙΧΙΨΙΩΙΚΑΚΒΚΓΚΕΚΖΚΗΚΘΚΙΚΚΛΚΜΚΝΚΚΞΚΟΚΠΚΡΚΣΚΤΚΥΚΦΚΧΚΨΚΩΚΛΑΛΒΛΓΛΕΛΖΛΗΛΘΛΙΛΚΛΛΜΛΝΛΛΞΛΟΛΠΛΡΛΣΛΤΛΥΛΦΛΧΛΨΛΩΛΜΑΜΒΜΓΜΕΜΖΜΗΜΘΜΙΜΚΜΛΜΜΝΜΜΞΜΟΜΠΜΡΜΣΜΤΜΥΜΦΜΧΜΨΜΩΜΝΑΝΒΝΓΝΕΝΖΝΗΝΘΝΙΝΚΝΛΝΜΝΝΝΞΝΟΝΠΝΡΝΣΝΤΝΥΝΦΝΧΝΨΝΩΝΞΑΞΒΞΓΞΕΞΖΞΗΞΘΞΙΞΚΞΛΞΜΞΝΞΞΞΟΞΠΞΡΞΣΞΤΞΥΞΦΞΧΞΨΞΩΞΟΑΟΒΟΓΟΕΟΖΟΗΟΘΟΙΟΚΟΛΟΜΟΝΟΟΞΟΟΠΟΡΟΣΟΤΟΥΟΦΟΧΟΨΟΩΟΠΑΠΒΠΓΠΕΠΖΠΗΠΘΠΙΠΚΠΛΠΜΠΝΠΠΞΠΟΠΠΡΠΣΠΤΠΥΠΦΠΧΠΨΠΩΠΡΑΡΒΡΓΡΕΡΖΡΗΡΘΡΙΡΚΡΛΡΜΡΝΡΡΞΡΟΡΠΡΡΣΡΤΡΥΡΦΡΧΡΨΡΩΡΣΑΣΒΣΓΣΕΣΖΣΗΣΘΣΙΣΚΣΛΣΜΣΝΣΞΣΟΣΠΣΡΣΣΤΣΥΣΦΣΧΣΨΣΩΣΤΑΤΒΤΓΤΕΤΖΤΗΤΘΤΙΤΚΤΛΤΜΤΝΤΞΤΟΤΠΤΡΤΣΤΤΥΤΦΤΧΤΨΤΩΤΥΑΥΒΥΓΥΕΥΖΥΗΥΘΥΙΥΚΥΛΥΜΥΝΥΞΥΟΥΠΥΡΥΣΥΤΥΥΦΥΧΥΨΥΩΥΦΑΦΒΦΓΦΕΦΖΦΗΦΘΦΙΦΚΦΛΦΜΦΝΦΦΞΦΟΦΠΦΡΦΣΦΤΦΥΦΦΧΦΨΦΩΦΧΑΧΒΧΓΧΕΧΖΧΗΧΘΧΙΧΚΧΛΧΜΧΝΧΧΞΧΟΧΠΧΡΧΣΧΤΧΥΧΦΧΧΨΧΩΧΨΑΨΒΨΓΨΕΨΖΨΗΨΘΨΙΨΚΨΛΨΜΨΝΨΨΞΨΟΨΠΨΡΨΣΨΤΨΥΨΦΨΧΨΨΩΨΩΑΩΒΩΓΩΕΩΖΩΗΩΘΩΙΩΚΩΛΩΜΩΝΩΩΞΩΟΩΠΩΡΩΣΩΤΩΥΩΦΩΧΩΨΩΩ
.α.β.γ.δ.ε.ζ.η.θ.ι.κ.λ.ν.ξ.ο.π.ρ.ς.σ.τ.υ.φ.χ.ψ.ω.,α,β,γ,δ,ε,ζ,η,θ,ι,κ,λ,ν,ξ,ο,π,ρ,ς,σ,τ,υ,φ,χ,ψ,ω,/α/β/γ/δ/ε/ζ/η/θ/ι/κ/λ/ν/ξ/ο/π/ρ/ς/σ/τ/υ/φ/χ/ψ/ω/\\α\\β\\γ\\δ\\ε\\ζ\\η\\θ\\ι\\κ\\λ\\ν\\ξ\\ο\\π\\ρ\\ς\\σ\\τ\\υ\\φ\\χ\\ψ\\ω\\α: β: γ: δ: ε: ζ: η: θ: ι: κ: λ: ν: ξ: ο: π: ρ: ς: σ: τ: υ: φ: χ: ψ: ω: α; β; γ; δ; ε; ζ; η; θ; ι; κ; λ; ν; ξ; ο; π; ρ; ς; σ; τ; υ; φ; χ; ψ; ω; α! β! γ! δ! ε! ζ! η! θ! ι! κ! λ! ν! ξ! ο! π! ρ! ς! σ! τ! υ! φ! χ! ψ! ω! (α) (β) (γ) (δ) (ε) (ζ) (η) (θ) (ι) (κ) (λ) (ν) (ξ) (ο) (π) (ρ) (ς) (σ) (τ) (υ) (φ) (χ) (ψ) (ω)[α] [β] [γ] [δ] [ε] [ζ] [η] [θ] [ι] [κ] [λ] [ν] [ξ] [ο] [π] [ρ] [ς] [σ] [τ] [υ] [φ] [χ] [ψ] [ω]{α} {β} {γ} {δ} {ε} {ζ} {η} {θ} {ι} {κ} {λ} {ν} {ξ} {ο} {π} {ρ} {ς} {σ} {τ} {υ} {φ} {χ} {ψ} {ω} –α– –β– –γ– –δ– –ε– –ζ– –η– –θ– –ι– –κ– –λ– –ν– –ξ– –ο– –π– –ρ– –ς– –σ– –τ– –υ– –φ– –χ– –ψ– –ω– -α- -β- -γ- -δ- -ε- -ζ- -η- -θ- -ι- -κ- -λ- -ν- -ξ- -ο- -π- -ρ- -ς- -σ- -τ- -υ- -φ- -χ- -ψ- -ω- —α— —β— —γ— —δ— —ε— —ζ— —η— —θ— —ι— —κ— —λ— —ν— —ξ— —ο— —π— —ρ— —ς— —σ— —τ— —υ— —φ— —χ— —ψ— —ω— “α” “β” “γ” “δ” “ε” “ζ” “η” “θ” “ι” “κ” “λ” “ν” “ξ” “ο” “π” “ρ” “ς” “σ” “τ” “υ” “φ” “χ” “ψ” “ω” «α» «β» «γ» «δ» «ε» «ζ» «η» «θ» «ι» «κ» «λ» «ν» «ξ» «ο» «π» «ρ» «ς» «σ» «τ» «υ» «φ» «χ» «ψ» «ω»•α•β•γ•δ•ε•ζ•η•θ•ι•κ•λ•ν•ξ•ο•π•ρ•ς•σ•τ•υ•φ•χ•ψ•ω•·α·β·γ·δ·ε·ζ·η·θ·ι·κ·λ·ν·ξ·ο·π·ρ·ς·σ·τ·υ·φ·χ·ψ·ω·*α*β*γ*δ*ε*ζ*η*θ*ι*κ*λ*ν*ξ*ο*π*ρ*ς*σ*τ*υ*φ*χ*ψ*ω*†α†β†γ†δ†ε†ζ†η†θ†ι†κ†λ†ν†ξ†ο†π†ρ†ς†σ†τ†υ†φ†χ†ψ†ω‡α‡β‡γ‡δ‡ε‡ζ‡η‡θ‡ι‡κ‡λ‡ν‡ξ‡ο‡π‡ρ‡ς‡σ‡τ‡υ‡φ‡χ‡ψ‡ωα®β®γ®δ®ε®ζ®η®θ®ι®κ®λ®ν®ξ®ο®π®ρ®ς®σ®τ®υ®φ®χ®ψ®ω®©α©β©γ©δ©ε©ζ©η©θ©ι©κ©λ©ν©ξ©ο©π©ρ©ς©σ©τ©υ©φ©χ©ψ©ω@α@β@γ@δ@ε@ζ@η@θ@ι@κ@λ@ν
ξ@ο@π@ρ@ς@σ@τ@υ@φ@χ@ψ@ω@α™β™γ™δ™ε™ζ™η™θ™ι™κ™λ™ν™ξ™ο™π™ρ™ς™σ™τ™υ™φ™χ™ψ™ω™
.Α.Β.Γ.Ε.Ζ.Η.Θ.Ι.Κ.Λ.Μ.Ν.Ξ.Ο.Π.Ρ.Σ.Τ.Υ.Φ.Χ.Ψ.Ω.,Α,Β,Γ,Ε,Ζ,Η,Θ,Ι,Κ,Λ,Μ,Ν,Ξ,Ο,Π,Ρ,Σ,Τ,Υ,Φ,Χ,Ψ,Ω,/Α/Β/Γ/Ε/Ζ/Η/Θ/Ι/Κ/Λ/Μ/Ν/Ξ/Ο/Π/Ρ/Σ/Τ/Υ/Φ/Χ/Ψ/Ω/\\Α\\Β\\Γ\\Ε\\Ζ\\Η\\Θ\\Ι\\Κ\\Λ\\Μ\\Ν\\Ξ\\Ο\\Π\\Ρ\\Σ\\Τ\\Υ\\Φ\\Χ\\Ψ\\Ω\\Α: Β: Γ: Ε: Ζ: Η: Θ: Ι: Κ: Λ: Μ: Ν: Ξ: Ο: Π: Ρ: Σ: Τ: Υ: Φ: Χ: Ψ: Ω:Α; Β; Γ; Ε; Ζ; Η; Θ; Ι; Κ; Λ; Μ; Ν; Ξ; Ο; Π; Ρ; Σ; Τ; Υ; Φ; Χ; Ψ; Ω;  Α! Β! Γ! Ε! Ζ! Η! Θ! Ι! Κ! Λ! Μ! Ν! Ξ! Ο! Π! Ρ! Σ! Τ! Υ! Φ! Χ! Ψ! Ω!(Α) (Β) (Γ) (Ε) (Ζ) (Η) (Θ) (Ι) (Κ) (Λ) (Μ) (Ν) (Ξ) (Ο) (Π) (Ρ) (Σ) (Τ) (Υ) (Φ) (Χ) (Ψ) (Ω) [Α] [Β] [Γ] [Ε] [Ζ] [Η] [Θ] [Ι] [Κ] [Λ] [Μ] [Ν] [Ξ] [Ο] [Π] [Ρ] [Σ] [Τ] [Υ] [Φ] [Χ] [Ψ] [Ω] {Α} {Β} {Γ} {Ε} {Ζ} {Η} {Θ} {Ι} {Κ} {Λ} {Μ} {Ν} {Ξ} {Ο} {Π} {Ρ} {Σ} {Τ} {Υ} {Φ} {Χ} {Ψ} {Ω}  –Α– –Β– –Γ– –Ε– –Ζ– –Η– –Θ– –Ι– –Κ– –Λ– –Μ– –Ν– –Ξ– –Ο– –Π– –Ρ– –Σ– –Τ– –Υ– –Φ– –Χ– –Ψ– –Ω– -Α- -Β- -Γ- -Ε- -Ζ- -Η- -Θ- -Ι- -Κ- -Λ- -Μ- -Ν- -Ξ- -Ο- -Π- -Ρ- -Σ- -Τ- -Υ- -Φ- -Χ- -Ψ- -Ω- —Α— —Β— —Γ— —Ε— —Ζ— —Η— —Θ— —Ι— —Κ— —Λ— —Μ— —Ν— —Ξ— —Ο— —Π— —Ρ— —Σ— —Τ— —Υ— —Φ— —Χ— —Ψ— —Ω— “Α” “Β” “Γ” “Ε” “Ζ” “Η” “Θ” “Ι” “Κ” “Λ” “Μ” “Ν” “Ξ” “Ο” “Π” “Ρ” “Σ” “Τ” “Υ” “Φ” “Χ” “Ψ” “Ω” «Α» «Β» «Γ» «Ε» «Ζ» «Η» «Θ» «Ι» «Κ» «Λ» «Μ» «Ν» «Ξ» «Ο» «Π» «Ρ» «Σ» «Τ» «Υ» «Φ» «Χ» «Ψ» «Ω» •Α•Β•Γ•Ε•Ζ•Η•Θ•Ι•Κ•Λ•Μ•Ν•Ξ•Ο•Π•Ρ•Σ•Τ•Υ•Φ•Χ•Ψ•Ω•·Α·Β·Γ·Ε·Ζ·Η·Θ·Ι·Κ·Λ·Μ·Ν·Ξ·Ο·Π·Ρ·Σ·Τ·Υ·Φ·Χ·Ψ·Ω·*Α*Β*Γ*Ε*Ζ*Η*Θ*Ι*Κ*Λ*Μ*Ν*Ξ*Ο*Π*Ρ*Σ*Τ*Υ*Φ*Χ*Ψ*Ω*†Α†Β†Γ†Ε†Ζ†Η†Θ†Ι†Κ†Λ†Μ†Ν†Ξ†Ο†Π†Ρ†Σ†Τ†Υ†Φ†Χ†Ψ†Ω‡Α‡Β‡Γ‡Ε‡Ζ‡Η‡Θ‡Ι‡Κ‡Λ‡Μ‡Ν‡Ξ‡Ο‡Π‡Ρ‡Σ‡Τ‡Υ‡Φ‡Χ‡Ψ‡Ω‡
®Α®Β®Γ®Ε®Ζ®Η®Θ®Ι®Κ®Λ®Μ®Ν®Ξ®Ο®Π®Ρ®Σ®Τ®Υ®Φ®Χ®Ψ®Ω®©Α©Β©Γ©Ε©Ζ©Η©Θ©Ι©Κ©Λ©Μ©Ν©Ξ©Ο©Π©Ρ©Σ©Τ©Υ©Φ©Χ©Ψ©Ω@Α@Β@Γ@Ε@Ζ@Η@Θ@Ι@Κ@Λ@Μ@ΝΞ@Ο@Π@Ρ@Σ@Τ@Υ@Φ@Χ@Ψ@Ω@Α™Β™Γ™Ε™Ζ™Η™Θ™Ι™Κ™Λ™Μ™Ν™Ξ™Ο™Π™Ρ™Σ™Τ™Υ™Φ™Χ™Ψ™Ω™
"""
GREEK_KERNING_SAMPLES = """
Lower case combinations (all possible combinations)
νηπιάας καράβι σαγανάκι καιάδας αέρας 
νάζια μάης ψάθα κεραία φάκα σαλάτα σαματάς μανούλα αταξία αορτή κάπα παράθυρο αφασία καταρρίπτω αυτιά ράφια μαχαλάς καψαλίζω φάω πας. βαρκούλα αββάς έβγαλε βδέλα μανιβέλα βζιν βλάβη βίδα τάβλα σβούρα αβρός βυτίο ράβω. αγάπη αγγαρία έγδυσε αγέρας σαγήνη σκάγια αγκαλιά γλαφυρός σίγμα αγνοώ έλεγξα 
αγόρι αγρός γύρω αγχώδης αγώνας. αδαής 
σαδδουκαίος άδεια αδημονώ παιδί κάδμος αφίδναι ειδοποίηση αμυδρός δυαδικός εδώ. αθέατη ανέβα σέγα μεδούλι λέει τέζα δέηση πεθαμένος ρειάκι καρέκλα σέλα δέμα αναμένα έβρεξα θεός λεπτό τέρας μπέσα βέτο πεύκο νεφέλη έβρεχα κλεψιά λέω θες. ζάχαρη μαζεύω έζησα νάζια ζλότι αζναβούρ αζόρες έζρα αζτέκος ζυμώνω ζώα. 
πίθηαι ήβη πηγάδι αηδία ήειδε πήζω λήθη 
καθεστυκηία σηκώνω ψηλά σημάδι μήνας ήξερα οδυσσήος σήπεται χήρα έζησα θήτα νηυσίν ηφαίστειο άηχος σήψη τεθνηώτος ζωής. καθαρός αθέατος άνθησε καλάθια κάθκαρτ αθλητής ασθμαίνω θνητός θολούρα θρόισμα θυμιατό αθώος αδιάβαστος λίβας σιγά παιδάκι σείεται ρίζα πνοιής είθε προίκα μίλα αίμα είναι μίξα άγριος πίπα χαίρομαι κάθισα επαίτης ιυ σιφώνι σιχαίνομαι δίψα λιώμα ελπίς άκακος έκβαση εκδίκαση ακέφαλος έκζεμα κήπος έκθεση χαλάκια εκκλησία έκλαψε ακμή οκνηρός ακοή εκπλήρωση έκρηξη έκτακτο κυοφορία έκφραση σάκχαρο εκών νικς. λαός χαλβάς άλγος αλδινό πλειάδα έλζα αλήθεια έλθει σάλια αλκαλικό αλλά αλμύρα χαλνώ έλξη άλογο ελπίδα έλροϊ άλσος ψάλτης αλυσίδα άλφα κάλχας αλώβητος βαλς. αμάθεια άμβωνας έμδεν εμμένω αμήχανος λάμια σίμκα κάμλα βάμμα αμνηστία ομόνεια ρόμπα αμριτσάρ κομσομόλ καμτσίκι αμυδρά εμφανής καμχής λάμψη άμωμος έιμπραμς ανανάς ανβάρ ένδεια ανέχεια ανζού ανήσυχος ενθύμιο ανία κονκάρδα καραμανλής μάννα εννοώ μονρόε πένσα αντλία νύχτα ανφάς μάνχαϊμ ανώγι χανς εξαπτέρυγο αξεσουάρ εξήγηση αξία αξλ ξόανο εξπέρ έξυσε εξωτερικό. στοά κόβω λόγος οδός 
ροές ρόζος βοήθεια πόθος κοιλιά πρόκα χολή ρόμπα μονάχος οξεία κλόουν ρόπτρο πόρτα όστια ποτό ρούχο λόφος οχιά κόψιμο προώθηση πράος. απάτη περίπου πηλίκιο πιθάρι έπκοτ απλός άπνοια απόσταση κάππα έπραξε απτός πύον πφφ απώτερο καπς. αράδα αρβύλα 
αργά γιάρδα παρέα τερζής κρητικός πάρθιος ψάρια μάρκα αρλούμπα αρμενίζω αρνί ξέρξης πρότερο αρπαγή θάρρος άρση χαρτί δάκρυα ερφούρτη αρχή τέρψη ήρωας αρς. κάσα ασβός σγουρός βασδέκης ασεβής ασήμαντος ασθενής όσιος σκηφτός ασλάνης χάσμα σνομπ πασούμι 
ράσπα καρλσρούη θάλασσα μαστός ασύδοτος ασφάλεια έσχατος άσωτος σς. τασάκι ετβά καλλιτεχνικός ατζαμής έστησα κάτθανε μάτια άτλαντας ατμός πατούσα άτρακτος πίτσα θάλαττα στυφός κατώι κατς. μυαλό κουβάς αυγό άναυδος μυελός ούζο εύηχος αύθα υιός καύκαλο παύλα τραύμα μαούνα σύξυλος λουόμενος τρύπα αύρα καθυστέρηση αυτιά 
καύφαλο ευχή υψηλός λύω ναυς. φαγητό αφγανιστάν εφεξής αφηνιασμένος άφθονος μαφία κάφκαλο καράφλα έξαφνα αφορμή αφρός φσιτ αφτιά φυτικό φχαριστώ φωταψίες παφς χάρακας χειρότερος όχημα αχθοφόρος 
αχινός αχλάδι αιχμηρό πάχνη αχούρι σαχπασίδης

Mix case combinations (all possible combinations)
Ααρών Άβατο Αγύριστος Αδικαιολόγητα Αέναος Αζήτητα Αήττητος Αθηναίος Αίαντας Ακαταστασία Αλλαγή Αμήχανα Αναμασώ Αξίνα Αόρατος Απείραχτος Αριβιστής Ασυγχώρητος Αττίλας Αυταρέσκεια Αφουγκράζομαι Αχέροντας Αψίδα 
Αώο Ας. Βάμμα Βγήκα Βδέλλα Βερόνα Βηματοδότης Βιρμανία Βλέψη Βολταϊκός Βρασίδας Βυθός Βωξ. Γαλοπούλα Γδύνω Γεράνι Γήρας Γιατί Γκαρίζω Γλαφυρός Γνέφω Γομάρι Γραικός Γυρεύω Γωνία. Δάδα Δγυρίζω Δέντρο 
Δη Διορίζω Δοκάρι Δπαίζω Δράκος Δύο Δφάληρο Δώμα. Εαρινός Έβαινα Εγώ Έδωσα Έζησα Έθιμο Είμαστε Έκλειψη Έλαμψα Έμενα Ενίοτε Εξαίρεση Εορτασμός Έπρεπε Έρχεται 
Εσωτερικός Ετοιμόλογος Ευτυχώς Εφεδρικός Έχει Έψησα Έως Ες. Ζαρωμένος Ζβόλος Ζγάτα Ζέα Ζην Ζιγκολό Ζλότι Ζορζ Ζυγαριά Ζωγράφος. Ηβικός Ηγεμόνας Ηδύποτο Ήθελα 
Ηκέτης Ηλιακός Ήμερος Ηνίο Ήξερα Ηπατικός Ηριδανός Ησαΐας Ήττα Ηυξημένος Ήφαιστος Ηχείο Ηψηλά Ης. Θαλάμι Θέλημα Θζήτημα Θηρίο Θιάσος Θκάππα Θνητός Θολούρα Θρασύς Θυμάρι Θφακός Θωμάς. Ιανός Ιβηρικός Ιγμόρειο Ιδιαίτερος Ιερεμίας Ίζημα Ιησουίτης Ιθαγένεια Ίκτερος Ιλαρά Ιμιτασιόν Ινία Ιξός Ίος Ιππικός Ίριδα Ισσός Ιτιά Ιύφαλος Ιφακός Ιχθύς Ίψεν Ιωβηλαίο Ις. Κακία Κβαντική Κένταυρος Κηδεία Κιάτο Κλέβω Κνήμη Κοροϊδία Κράση Κτήμα Κύμα Κωδεΐνη. Λαμία Λέρα Λζήτω Λήθη Λιώμα Λοβοτομή Λυδία Λωτός. Μαδέρι Μειδίαμα Μζάρι Μην Μιάου Μνήμα Μόδα Μπαρμπούνι Μύδια Μωρία Μς. Νανούρισμα Νεότερος Νήπιο Νίκη Νκακία Νοοτροπία Νταμάρι Νυμφαίο Νώε Νς. Ξανά Ξημέρωσε Ξιπόλητος Ξόρκι Ξυράφι Ξωκλήσι Ξς. Όαση Οβελίας Ογδόντα Οδοιπόρος Όζον Οθέλος Οικονομία Οκλαχόμα Ολόκληρος Ομόνοια Όνειρο Όξινος Όπερα Ορός Όσιος Όταν Ουρανία Όφελος Οχιά Όψιμος Ος. Παπαρούνα Περιβόλι Πζάρι Πήγαινα Πίνω Πλένω Πνεύμα Ποτήρι Πρωτιά Πυρίμαχος Πώς Πς. Ρεμάλι Ρήγμα Ρίζα Ρόπτρο Ρυμουλκό Ρωμαϊκός Ρς. Σαβάνα Σβήνω Σγουρός Σδένω Σελήνη Σήμερα Σθένος Σιρόπι Σκελέα Σλιπ Σμέρνα Σνιφάρω Σοπράνο Σπιούνος Σρι λάνκα Σσερσέμης Σταλιά Σύμμαχος Σφετεριστής Σχήμα Σωθικά Σς. Ταβέρνα Τεμάχιο Τζάμι Τηγάνι Τιβέριος Τμήμα Τοπογραφικό Τριβιζάς Τσέχος Τυφώνας Τώρα Τς. Υάκινθος Υβριδικός Υγεία Υδάτινος Υεμένη Υιός Υκαρμίνα Υλικός Υμών Υνί Υπέρ Ύστατος Ύφαλος Υχροιά Ύψος Υς. Φαγητό Φευγαλέος Φήμη Φθιώτιδα Φιλικός Φλύαρος Φνακ Φορτωμένος Φραγή Φτυάρι Φυσάει Φωκίδα Φς. Χαρούλα Χεβιμεταλάς Χήνα Χιώτης Χλοερός Χμ Χνάρι Χολέρα  Χριστιανέ Χτένι Χυτά Χωμενίδης

Χς. Ψαρόβαρκα Ψεύτικα Ψησταριά Ψιλικά Ψοφόκρυο Ψυχή Ψωμί Ψς. Ωά Ωγυγία Ωδείο Ώθηση Ωκεανός Ωλένη Ωμός Ωνάσης Ωοειδής Ωράριο Ώσμωση Ώτα Ωφέλιμος Ωχ! Ως.

Upper case combinations (all possible combinations)
ΝΗΠΙΑΑΣ ΚΑΡΑΒΙ ΣΑΓΑΝΑΚ Ι ΚΑΙΑΔΑΣ ΑΕΡΑΣ ΝΑΖΙΑ ΜΑΗΣ ΨΑΘΑ ΚΕΡΑΙΑ ΦΑΚΑ ΣΑΛΑΤΑ ΣΑΜΑΤΑΣ ΜΑΝΟΥΛΑ ΑΤΑΞΙΑ ΑΟΡΤ Η ΚΑΠΑ ΠΑΡΑΘΥΡΟ ΑΦΑΣΙΑ ΚΑΤΑΡΡΙΠΤ Ω ΑΥΤ ΙΑ ΡΑΦΙΑ ΜΑΧΑΛΑΣ ΚΑΨΑΛΙΖΩ ΦΑΩ ΠΑΣ. ΒΑΡΚΟΥΛΑ ΑΒΒΑΣ ΕΒΓΑΛΕ ΒΔΕΛΑ ΜΑΝΙΒΕΛΑ ΒΖΙΝ ΒΛΑΒΗ ΒΙΔΑ ΤΑΒΛΑ ΣΒΟΥΡΑ ΑΒΡΟΣ ΒΥΤ ΙΟ ΡΑΒΩ. ΑΓΑΠΗ ΑΓΓΑΡΙΑ ΕΓΔΥΣΕ ΑΓΕΡΑΣ ΣΑΓΗΝΗ ΣΚΑΓΙΑ ΑΓΚΑΛΙΑ ΓΛΑΦΥΡΟΣ ΣΙΓΜΑ ΑΓΝΟΩ ΕΛΕΓΞΑ ΑΓΟΡΙ ΑΓΡΟΣ ΓΥΡΩ ΑΓΧΩΔΗΣ ΑΓΩΝΑΣ. ΑΔΑΗΣ ΣΑΔΔΟΥΚΑΙΟΣ ΑΔΕΙΑ ΑΔΗΜΟΝΩ ΠΑΙΔΙ ΚΑΔΜΟΣ ΑΦΙΔΝΑΙ ΕΙΔΟΠΟΙΗΣΗ ΑΜΥΔΡΟΣ ΔΥΑΔΙΚΟΣ ΕΔΩ. ΑΘΕΑΤ Η ΑΝΕΒΑ ΣΕΓΑ ΜΕΔΟΥΛΙ ΛΕΕΙ Τ ΕΖΑ ΔΕΗΣΗ ΠΕΘΑΜΕΝΟΣ ΡΕΙΑΚ Ι Κ Ι ΚΑΡΕΚΛΑ ΣΕΛΑ ΔΕΜΑ ΑΝΑΜΕΝΑ ΕΒΡΕΞΑ ΘΕΟΣ ΛΕΠΤ Ο Τ ΕΡΑΣ ΜΠΕΣΑ ΒΕΤ Ο ΠΕΥΚΟ ΝΕΦΕΛΗ ΕΒΡΕΧΑ ΚΛΕΨΙΑ ΛΕΩ ΘΕΣ. ΖΑΧΑΡΗ ΜΑΖΕΥΩ ΕΖΗΣΑ ΝΑΖΙΑ ΖΛΟΤ Ι ΑΖΝΑΒΟΥΡ ΑΖΟΡΕΣ ΕΖΡΑ ΑΖΤΕΚΟΣ ΖΥΜΩΝΩ ΖΩΑ. ΠΙΘΗΑΙ ΗΒΗ ΠΗΓΑΔΙ ΑΗΔΙΑ ΗΕΙΔΕ ΠΗΖΩ ΛΗΘΗ ΚΑΘΕΣ Τ ΥΚ ΗΙΑ ΣΗΚΩΝΩ ΨΗΛΑ ΣΗΜΑΔΙ ΜΗΝΑΣ ΗΞΕ ΡΑ ΟΔΥΣΣΗΟΣ ΣΗΠΕΤΑΙ ΧΗΡΑ ΕΖΗΣΑ ΘΗΤΑ ΝΗΥΣΙΝ ΗΦΑΙΣΤΕΙΟ ΑΗΧΟΣ ΣΗΨΗ Τ ΕΘΝΗΩΤ ΟΣ ΖΩΗΣ. ΚΑΘΑΡΟΣ ΑΘΕΑΤ ΟΣ ΑΝΘΗΣΕ ΚΑΛΑΘΙΑ ΚΑΘΚΑΡΤ ΑΘΛΗΤ ΗΣ ΑΣΘΜΑΙΝΩ ΘΝΗΤ ΟΣ ΘΟΛΟΥΡΑ ΘΡΟΪΣΜΑ ΘΥΜΙΑΤΟ ΑΘΩΟΣ ΑΔΙΑΒΑΣΤΟΣ ΛΙΒΑΣ ΣΙΓΑ ΠΑΙΔΑΚΙ ΣΕΙΕΤΑΙ ΡΙΖΑ ΠΝΟΙΗΣ ΕΙΘΕ ΠΡΟΙΚΑ ΜΙΛΑ ΑΙΜΑ ΕΙΝΑΙ ΜΙΞΑ ΑΓ ΕΙΝΑΙ ΜΙΞΑ ΑΓΡΙΟΣ ΠΙΠΑ ΧΑΙΡΟΜΑΙ ΚΑΘΙΣΑ ΕΠΑΙΤ ΗΣ ΙΥ ΣΙΦΩΝΙ ΣΙΧΑΙΝΟΜΑΙ ΔΙ ΨΑ ΛΙΩΜΑ ΕΛΠ ΙΣ Α ΚΑ ΚΟΣ Ε Κ ΒΑΣΗ Ε ΚΔΙ ΚΑΣΗ Α ΚΕΦΑΛΟΣ ΕΚΖΕΜΑ Κ ΗΠΟΣ ΕΚΘΕΣΗ ΧΑΛΑΚ ΙΑ ΕΚ ΚΛΗΣΙΑ ΕΚΛΑΨΕ ΑΚΜΗ ΟΚΝΗΡΟΣ ΑΚΟΗ ΕΚΠΛΗΡΩΣΗ ΕΚ ΡΗΞΗ ΕΚΤΑΚΤ Ο Κ ΥΟΦΟΡΙΑ ΕΚΦΡΑΣΗ ΣΑΚΧΑΡΟ ΕΚΩΝ ΝΙΚΣ. ΛΑΟΣ ΧΑΛΒΑ Σ ΑΛΓΟΣ ΑΛΔΙΝΟ ΠΛΕΙΑΔΑ ΕΛΖΑ ΑΛΗΘΕΙΑ ΕΛΘΕΙ ΣΑΛΙΑ ΑΛΚΑΛΙΚΟ ΑΛΛΑ ΑΛΜΥΡΑ ΧΑΛΝΩ ΕΛΞΗ ΑΛΟΓΟ ΕΛΠΙΔΑ ΕΛΡΟΪ ΑΛΣΟΣ ΨΑΛΤ ΗΣ ΑΛΥΣΙΔΑ ΑΛΦΑ ΚΑΛΧΑΣ ΑΛΩΒΗΤΟΣ ΒΑΛΣ. ΑΜΑΘΕΙΑ ΑΜΒΩΝΑΣ ΕΜΔΕΝ ΕΜΜΕΝΩ ΑΜΗΧΑΝΟΣ ΛΑΜΙΑ ΣΙΜΚΑ ΚΑΜΛΑ ΒΑΜΜΑ ΑΜΝΗΣ Τ ΙΑ ΟΜΟΝΕΙΑ ΡΟΜΠΑ ΑΜΡΙΤΣΑΡ ΚΟΜΣΟΜΟΛ ΚΑΜΤΣΙΚ Ι ΤΣΙΚ Ι ΑΜΥΔΡΑ

ΕΜΦΑΝΗΣ ΚΑΜΧΗΣ ΛΑΜΨΗ ΑΜΩΜΟΣ Ε ΪΜΠ ΡΑΜΣ ΑΝΑΝΑΣ ΑΝΒΑ Ρ ΕΝΔΕΙΑ ΑΝΕΧΕΙΑ ΑΝΖΟΥ ΑΝΗΣΥΧΟΣ ΕΝΘΥΜΙΟ ΑΝΙΑ ΚΟΝΚΑΡΔΑ ΚΑΡΑΜΑΝΛΗΣ ΜΑΝΝΑ ΕΝΝΟΩ ΜΟΝΡΟΕ ΠΕΝΣΑ ΑΝΤΛΙΑ ΝΥΧΤΑ ΑΝΦΑΣ ΜΑΝΧΑΪΜ ΑΝΩΓΙ ΧΑΝΣ ΕΞΑΠΤ ΕΡΥΓΟ ΑΞΕΣΟΥΑΡ ΕΞΗΓΗΣΗ ΑΞΙΑ ΑΞΛ ΞΟΑΝΟ ΕΞΠΕΡ ΕΞΥΣΕ ΕΞΩΤΕΡΙΚΟ. ΣΤΟΑ ΚΟΒΩ ΛΟΓΟΣ ΟΔΟΣ ΡΟΕΣ ΡΟΖΟΣ ΒΟΗΘΕΙΑ ΠΟΘΟΣ ΚΟΙΛΙΑ ΠΡΟΚΑ ΧΟΛΗ ΡΟΜΠΑ ΜΟΝΑΧΟΣ ΟΞΕ ΙΑ ΚΛΟΟΥΝ ΡΟΠΤ ΡΟ ΠΟΡΤΑ ΟΣ Τ ΙΑ ΠΟΤ Ο ΡΟΥΧΟ ΛΟΦΟΣ ΟΧΙΑ ΚΟΨΙΜΟ ΠΡΟΩΘΗΣΗ ΠΡΑΟΣ. ΑΠΑΤ Η ΠΕΡΙΠΟΥ ΠΗΛΙΚ ΙΟ ΠΙΘΑΡΙ ΕΠΚΟΤ ΑΠΛΟΣ ΑΠΝΟΙΑ ΑΠΟΣΤΑΣΗ ΚΑΠΠΑ ΕΠΡΑΞΕ ΑΠΤΟΣ ΠΥΟΝ ΠΦΦ ΑΠΩΤΕΡΟ ΚΑΠΣ. ΑΡΑΠΣ. ΑΡΑΔΑ
Α Ρ Β ΥΛΑ Α ΡΓ Α ΓΙΑ ΡΔ Α Π Α ΡΕ Α Τ Ε ΡΖ ΗΣ Κ Ρ ΗΤ Ι ΚΟΣ Π Α ΡΘ ΙΟΣ ΨΑΡΙΑ ΜΑΡΚΑ ΑΡΛΟΥΜΠΑ ΑΡΜΕΝΙΖΩ ΑΡΝΙ ΞΕΡΞΗΣ ΠΡΟΤΕΡΟ ΑΡΠΑΓΗ ΘΑΡΡΟΣ ΑΡΣΗ ΧΑΡΤ Ι ΔΑΚ ΡΥΑ ΕΡΦΟΥΡΤ Η ΑΡΧΗ Τ ΕΡΨΗ ΗΡΩΑΣ ΑΡΣ. ΚΑΣΑ ΑΣΒΟΣ ΣΓΟΥΡΟΣ ΒΑΣΔΕΚ ΗΣ ΑΣΕΒΗΣ ΑΣΗΜΑΝ Τ ΟΣ ΑΣΘΕΝΗΣ ΟΣΙΟΣ ΣΚ ΗΦΤ ΟΣ ΑΣΛΑΝΗΣ ΧΑΣΜΑ ΣΝΟΜΠ ΠΑΣΟΥΜΙ ΡΑΣΠΑ ΚΑΡΛΣΡΟΥΗ ΘΑΛΑΣΣΑ ΜΑΣΤΟΣ ΑΣΥΔΟΤΟΣ ΑΣΦΑΛΕΙΑ ΕΣΧΑΤ ΟΣ ΑΣΩΤ ΟΣ ΣΣ. ΤΑΣΑΚ Ι ΕΤ ΒΑ ΚΑΛΛΙΤ ΕΧΝΙ ΚΟΣ ΑΤΖΑΜΗΣ ΕΣΤ ΗΣΑ ΚΑΤΘΑΝΕ ΜΑΤ ΙΑ ΑΤΛΑΝΤΑΣ ΑΤΜΟΣ ΠΑΤΟΥΣΑ ΑΤ ΡΑΚΤΟΣ ΠΙΤΣΑ ΘΑΛΑΤΤΑ ΣΤ ΥΦΟΣ ΚΑΤΩΪ ΚΑΤΣ. ΜΥΑΛΟ ΚΟΥΒΑΣ ΑΥΓΟ ΑΝΑΥΔΟΣ ΜΥΕΛΟΣ ΟΥΖΟ ΕΥΗΧΟΣ ΑΥΘΑ ΥΙΟΣ ΘΑ ΥΙΟΣ ΚΑΥΚΑΛΟ ΠΑΥΛΑ Τ ΡΑΥΜΑ ΜΑΟΥΝΑ ΣΥΞΥΛΟΣ ΛΟΥΟΜΕΝΟΣ Τ Ρ ΥΠ Α Α ΥΡΑ ΚΑΘ ΥΣ Τ Ε Ρ ΗΣΗ Α ΥΤ ΙΑ ΚΑ ΥΦΑΛΟ Ε ΥΧΗ ΥΨΗΛΟΣ ΛΥΩ ΝΑΥΣ. ΦΑΓΗΤΟ ΑΦΓΑΝΙΣΤΑΝ ΕΦΕΞΗΣ ΑΦΗΝΙΑΣΜΕΝΟΣ ΑΦΘΟΝΟΣ ΜΑΦΙΑ ΚΑΦΚΑΛΟ ΚΑΡΑΦΛΑ ΕΞΑΦΝΑ ΑΦΟΡΜΗ ΑΦΡΟΣ ΦΣΙΤ ΑΦΤ ΙΑ ΦΥΤ ΙΚΟ ΦΧΑΡΙΣΤΩ ΦΩΤΑΨΙΕΣ ΠΑΦΣ ΧΑΡΑΚΑΣ ΧΕΙΡΟΤΕΡΟΣ ΟΧΗΜΑ ΑΧΘΟΦΟΡΟΣ ΑΧΙΝΟΣ ΑΧΛΑΔΙ ΑΙΧΜΗΡΟ ΠΑΧΝΗ ΑΧΟΥΡΙ ΣΑΧΠΑΣΙΔΗΣ ΑΧΡΕΙΑΣΤΟΣ ΟΧΤΩΗΧΟΣ ΑΧΥΡΩΝΑΣ ΑΔΙΑΧΩΡΗΤΟ
ΧΣ. ΚΑΨΑΛΙΖΩ ΨΕΙΡΕΣ ΑΨΗΦΩ ΤΑΨΙΑ ΑΨΟΓΟΣ ΕΜΨΥΧΟΣ ΨΩΡΑ. ΖΩΑ ΙΩΒΗΛΑΙΟΣ ΔΙΩΓΜΟΣ ΩΔΗ ΖΩΕΣ ΕΣΩΖΕ ΖΩΗ ΩΘΗΣΗ ΩΙΜΕ ΕΣΩΚΛΕ ΙΣ Τ Ο ΚΩΛΥΜΑ ΛΙΩΜΑ ΑΜΒΩΝΑΣ ΒΩΞ ΙΤ ΗΣ ΖΩΟΣ ΖΩΟΝ ΑΝΑΖΩΠ ΥΡΩΣΗ Τ ΩΡΑ ΕΣΩσα ρωτάω ζωύφιο κωφός μολώχ μύωψ ζώων πως
πεζά-lowercase (all combinations)
ααβαγαδαεαζαηαθαιακαλαμαναξαπαρασαταυαφαχαψαωας βαββγβδβεβζβηβθβιβκβλβμβνβξβπβρβσβτβυβφβχβψβωβς γαγβγγδγεγζγηγθγιγκγλγμγνγξγπγργσγτγυγφγχγψγωγς

δαδβδγδδεδζδηδθδιδκδλδμδνδξδπδρδσδτδυδφδχδψδωδς εαεβεγεδεεζεηεθειεκελεμενεξεπερεσετευεφεχεψεωες ζαζβζγζδζεζζηζθζιζκζλζμζνζξζπζρζσζτζυζφζχζψζωζς ηαηβηγηδηεηζηηθηιηκηλημηνηξηπηρησητηυηφηχηψηωης θαθβθγθδθεθζθηθθιθκθλθμθνθξθπθρθσθτθυθφθχθψθωθς ιαιβιγιδιειζιηιθιικιλιμινιξιπιρισιτιυιφιχιψιωις ίαίβίγίδίείζίηίθίίκίλίμίνίξίπίρίσίτίυίφίχίψίωίς ϊαϊβϊγϊδϊεϊζϊηϊθϊϊκϊλϊμϊνϊξϊπϊρϊσϊτϊυϊφϊχϊψϊωϊς ΐαΐβΐγΐδΐεΐζΐηΐθΐΐκΐλΐμΐνΐξΐπΐρΐσΐτΐυΐφΐχΐψΐωΐς κακβκγκδκεκζκηκθκικκλκμκνκξκπκρκσκτκυκφκχκψκωκς λαλβλγλδλελζληλθλιλκλλμλνλξλπλρλσλτλυλφλχλψλωλς μαμβμγμδμεμζμημθμιμκμλμμνμξμπμρμσμτμυμφμχμψμωμς νανβνγνδνενζνηνθνινκνλνμνννξνπνρνσντνυνφνχνψνωνς ξαξβξγξδξεξζξηξθξιξκξλξμξνξξπξρξσξτξυξφξχξψξωξς οαοβογοδοεοζοηοθοιοκολομονοξοποροσοτουοφοχοψοωος παπβπγπδπεπζπηπθπιπκπλπμπνπξποπρπσπτπυπφπχπψπωπς ραρβργρδρερζρηρθριρκρλρμρνρξρορπρσρτρυρφρχρψρωρς σασβσγσδσεσζσησθσισκσλσμσνσξσοσπσρστσυσφσχσψσωσς
τατβτγτδτετζτητθτιτκτλτμτντξτοτπτρτστυτφτχτψτωτς υαυβυγυδυευζυηυθυιυκυλυμυνυξυουπυρυσυτυφυχυψυωυς ύαύβύγύδύεύζύηύθύύκύλύμύνύξύπύρύσύτύυύφύχύψύωύς ϋαϋβϋγϋδϋεϋζϋηϋθϋϋκϋλϋμϋνϋξϋπϋρϋσϋτϋυϋφϋχϋψϋωϋς ΰαΰβΰγΰδΰεΰζΰηΰθΰΰκΰλΰμΰνΰξΰπΰρΰσΰτΰυΰφΰχΰψΰωΰς φαφβφγφδφεφζφηφθφιφκφλφμφνφξφοφπφρφσφτφυφχφψφωφς χαχβχγχδχεχζχηχθχιχκχλχμχνχξχοχπχρχσχτχυχφχψχωχς ψαψβψγψδψεψζψηψθψιψκψλψμψνψξψοψπψρψσψτψυψφψχψωψς ωαωβωγωδωεωζωηωθωιωκωλωμωνωξωοωπωρωσωτωυωφωχωψως
κεφαλαία-uppercase (all combinations):
ΑΑΑΒΑΓΑΔΑΕΑΖΑΗΑΘΑΙΑΚΑΛΑΜΑΝΑΞΑΟΑΠΑΡΑΣΑΤΑΥΑΦΑΧΑΨΑΩ ΒΑΒΒΒΓΒΔΒΕΒΖΒΗΒΘΒΙΒΚΒΛΒΜΒΝΒΞΒΟΒΠΒΡΒΣΒΤΒΥΒΦΒΧΒΨΒΩ
Γ ΑΓΒΓΓΓΔΓΕΓΖΓΗΓΘΓΙΓΚΓΛΓΜΓΝΓΞΓΟΓΠΓΡΓΣΓΤΓΥΓΦΓΧΓΨΓΩ ΔΑΔΒΔΓΔΔΔΕΔΖΔΗΔΘΔΙΔΚΔΛΔΜΔΝΔΞΔΟΔΠΔΡΔΣΔΤΔΥΔΦΔΧΔΨΔΩ ΕΑΕΒΕΓΕΔΕΕΕΖΕΗΕΘΕΙΕΚΕΛΕΜΕΝΕΞΕΟΕΠΕΡΕΣΕΤ ΕΥΕΦΕΧΕΨΕΩ
ΖΑΖ ΒΖΓΖΔΖΕΖΖΖ ΗΖΘΖ ΙΖ ΚΖΛΖΜΖΝΖΞΖΟΖΠΖ ΡΖΣΖΤΖ ΥΖΦΖΧΖ ΨΖΩ ΗΑΗΒΗΓΗΔΗΕΗΖΗΗΗΘΗΙΗΚΗΛΗΜΗΝΗΞΗΟΗΠΗΡΗΣΗΤΗΥΗΦΗΧΗΨΗΩ ΘΑΘΒΘΓΘΔΘΕΘΖΘΗΘΘΘΙΘΚΘΛΘΜΘΝΘΞΘΟΘΠΘΡΘΣΘΤΘΥΘΦΘΧΘΨΘΩ ΙΑΙΒΙΓΙΔΙΕΙΖΙΗΙΘΙΙΙΚΙΛΙΜΙΝΙΞΙΟΙΠΙΡΙΣΙΤΙΥΙΦΙΧΙΨΙΩ
ΪΑΪΒΪΓΪΔΪΕΪΖΪΗΪΘΪΚ ΪΛΪΜΪΝΪΞΪΟΪΠΪΡΪΣΪΤ ΪΥΪΦΪΧΪΨΪΩ ΚΑΚΒΚΓΚΔΚΕΚΖΚΗΚΘΚΙΚΚΚΛΚΜΚΝΚΞΚΟΚΠΚΡΚΣΚΤΚΥΚΦΚΧΚΨΚΩ ΛΑΛΒΛΓΛΔΛΕΛΖΛΗΛΘΛΙΛΚΛΛΛΜΛΝΛΞΛΟΛΠΛΡΛΣΛΤΛΥΛΦΛΧΛΨΛΩ

ΜΑΜΒΜΓΜΔΜΕΜΖΜΗΜΘΜΙΜΚΜΛΜΜΜΝΜΞΜΟΜΠΜΡΜΣΜΤΜΥΜΚΜΦΜΧΜ‐ ΨΜΩ
ΝΑΝΒΝΓΝΔΝΕΝΖΝΗΝΘΝΙΝΚΝΛΝΜΝΝΝΞΝΟΝΠΝΡΝΣΝ ΤΝΥΝΦΝΧΝΨΝΩ
ΞΑΞ ΒΞΓΞΔΞΕΞΖΞ ΗΞΘΞ ΙΞ ΚΞΛΞΜΞΝΞΞΞΟΞΠΞ ΡΞΣΞΤΞ ΥΞΦΞΧΞ ΨΞΩ ΟΑΟΒΟΓΟΔΟΕΟΖΟΗΟΘΟΙΟΚΟΛΟΜΟΝΟΞΟΟΟΠΟΡΟΣΟΤ ΟΥΟΦΟΧΟΨΟΩΟ
Π ΑΠ ΒΠΓΠΔΠΕΠΖΠ ΗΠΘΠ ΙΠ ΚΠΛΠΜΠΝΠΞΠΟΠΠΠ ΡΠΣΠΤΠ ΥΠΦΠΧΠ ΨΠΩΠ ΡΑΡΒΡΓΡΔΡΕΡΖΡΗΡΘΡΙΡΚΡΛΡΜΡΝΡΞΡΟΡΠΡΡΡΣΡΤΡΥΡΦΡΧΡΨΡΩ
Σ ΑΣΒΣΓΣΔΣΕΣΖΣΗΣΘΣΙΣΚΣΛΣΜΣΝΣΞΣΟΣΠΣΡΣΣΣ ΤΣΥΣΦΣΧΣΨΣΩ
ΤΑ Τ ΒΤΓΤΔΤ Ε ΤΖΤ ΗΤΘΤ ΙΤ ΚΤΛΤΜΤΝ ΤΞΤ ΟΤΠΤ ΡΤΣ Τ Τ Τ ΥΤΦΤ ΧΤ ΨΤ Ω ΥΑΥΒΥΓΥΔΥΕΥΖΥΗΥΘΥΙΥΚΥΛΥΜΥΝΥΞΥΟΥΠΥΡΥΣΥΤΥΥΥΦΥΧΥΨΥΩ ΫΑΫΒΫΓΫΔΫΕΫΖΫΗΫΘΫΙΫΚΫΛΫΜΫΝΫΞΫΟΫΠΫΡΫΣΫΤΫΦΫΧΫΨΫΩ ΦΑΦΒΦΓΦΔΦΕΦΖΦΗΦΘΦΙΦΚΦΛΦΜΦΝΦΞΦΟΦΠΦΡΦΣΦΤΦΥΦΦΦΧΦΨΦΩ ΧΑΧΒΧΓΧΔΧΕΧΖΧΗΧΘΧΙΧΚΧΛΧΜΧΝΧΞΧΟΧΠΧΡΧΣΧΤ ΧΥΧΦΧΧΧΨΧΩ ΨΑΨΒΨΓΨΔΨΕΨΖΨΗΨΘΨΙΨΚΨΛΨΜΨΝΨΞΨΟΨΠΨΡΨΣΨΤΨΥΨΦΨΧΨΨ‐ ΨΩ
ΩΑΩΒΩΓΩΔΩΕΩΖΩΗΩΘΩΙΩΚΩΛΩΜΩΝΩΞΩΟΩΠΩΡΩΣΩΤ ΩΥΩΦΩΧΩΨΩΩ
κεφαλαία+πεζά-UC+lc (all combinations):
ΑαΑβΑγΑδΑεΑζΑηΑθΑιΑκΑλΑμΑνΑξΑοΑπΑρΑσΑτΑυΑφΑχΑψΑωΑςΑάΑίΑήΑέΑόΑύ‐ ΑώΑϊΑϋΑΐΑΰ ΒαΒβΒγΒδΒεΒζΒηΒθΒιΒκΒλΒμΒνΒξΒοΒπΒρΒσΒτΒυΒφΒχΒψΒωΒςΒάΒίΒήΒέΒόΒύΒώ ΓαΓβΓγΓδΓεΓζΓηΓθΓιΓκΓλΓμΓνΓξΓοΓπΓρΓσΓτΓυΓφΓχΓψΓωΓςΓάΓίΓήΓέΓόΓύΓώ ΔαΔβΔγΔδΔεΔζΔηΔθΔιΔκΔλΔμΔνΔξΔοΔπΔρΔσΔτΔυΔφΔχΔψΔωΔςΔάΔίΔήΔέΔόΔύ‐ Δώ ΕαΕβΕγΕδΕεΕζΕηΕθΕιΕκΕλΕμΕνΕξΕοΕπΕρΕσΕτΕυΕφΕχΕψΕωΕςΕάΕίΕήΕέΕόΕύΕώΕϊΕϋΕΐΕΰ ΖαΖβΖγΖδΖεΖζΖηΖθΖιΖκΖλΖμΖνΖξΖοΖπΖρΖσΖτΖυΖφΖχΖψΖωΖςΖάΖίΖήΖέΖόΖύΖώ ΗαΗβΗγΗδΗεΗζΗηΗθΗιΗκΗλΗμΗνΗξΗοΗπΗρΗσΗτΗυΗφΗχΗψΗωΗςΗάΗίΗήΗέΗόΗύΗώ‐ ΗϊΗϋΗΐΗΰ ΘαΘβΘγΘδΘεΘζΘηΘθΘιΘκΘλΘμΘνΘξΘοΘπΘρΘσΘτΘυΘφΘχΘψΘωΘςΘάΘίΘήΘέΘόΘύΘώ ΙαΙβΙγΙδΙεΙζΙηΙθΙιΙκΙλΙμΙνΙξΙοΙπΙρΙσΙτΙυΙφΙχΙψΙωΙςΙάΙίΙήΙέΙόΙύΙώΙϊΙϋΙΐΙΰ ΚαΚβΚγΚδΚεΚζΚηΚθΚιΚκΚλΚμΚνΚξΚοΚπΚρΚσΚτΚυΚφΚχΚψΚωΚςΚάΚίΚήΚέΚόΚύΚώ ΛαΛβΛγΛδΛεΛζΛηΛθΛιΛκΛλΛμΛνΛξΛοΛπΛρΛσΛτΛυΛφΛχΛψΛωΛςΛάΛίΛήΛέΛόΛύΛώ ΜαΜβΜγΜδΜεΜζΜηΜθΜιΜκΜλΜμΜνΜξΜοΜπΜρΜσΜτΜυΜφΜχΜψΜωΜςΜάΜί‐ ΜήΜέΜόΜύΜώ ΝαΝβΝγΝδΝεΝζΝηΝθΝιΝκΝλΝμΝνΝξΝοΝπΝρΝσΝτΝυΝφΝχΝψΝωΝςΝάΝίΝήΝέΝόΝύΝώ ΞαΞβΞγΞδΞεΞζΞηΞθΞιΞκΞλΞμΞΞΞξΞοΞπΞρΞσΞτΞυΞφΞχΞψΞωΞςΞάΞίΞήΞέΞόΞύΞώ ΟαΟβΟγΟδΟεΟζΟηΟθΟιΟκΟλΟμΟνΟξΟοΟπΟρΟσΟτΟυΟφΟχΟψΟωΟςΟάΟίΟήΟέΟόΟύΟώ‐ ΟϊΟϋΟΐΟΰ ΠαΠβΠγΠδΠεΠζΠηΠθΠιΠκΠλΠμΠνΠξΠοΠπΠρΠσΠτΠυΠφΠχΠψΠωΠςΠάΠίΠήΠέΠόΠύΠώ ΡαΡβΡγΡδΡεΡζΡηΡθΡιΡκΡλΡμΡνΡξΡοΡπΡρΡσΡτΡυΡφΡχΡψΡωΡςΡάΡίΡήΡέΡόΡύΡώ ΣαΣβΣγΣδΣεΣζΣηΣθΣιΣκΣλΣμΣνΣξΣοΣπΣρΣσΣτΣυΣφΣχΣψΣωΣςΣάΣίΣήΣέΣόΣύΣώ

ΤαΤβΤγΤδΤεΤζΤηΤθΤιΤκΤλΤμΤνΤξΤοΤπΤρΤσΤτΤυΤφΤχΤψΤωΤςΤάΤ ίΤήΤέΤόΤύΤώ ΥαΥβΥγΥδΥεΥζΥηΥθΥιΥκΥλΥμΥνΥξΥοΥπΥρΥσΥτΥυΥφΥχΥψΥωΥςΥάΥίΥήΥέΥόΥύΥώΥϊΥϋΥΐΥΰ ΦαΦβΦγΦδΦεΦζΦηΦθΦιΦκΦλΦμΦνΦξΦοΦπΦρΦσΦτΦυΦφΦχΦψΦωΦςΦάΦίΦήΦέ‐ ΦόΦύΦώ ΧαΧβΧγΧδΧεΧζΧηΧθΧιΧκΧλΧμΧνΧξΧοΧπΧρΧσΧτΧυΧφΧχΧψΧωΧςΧάΧίΧήΧέΧόΧύΧώ ΨαΨβΨγΨδΨεΨζΨηΨθΨιΨκΨλΨμΨνΨξΨοΨπΨρΨσΨτΨυΨφΨχΨψΨωΨςΨάΨίΨήΨέ‐ ΨόΨύΨώ ΩαΩβΩγΩδΩεΩζΩηΩθΩιΩκΩλΩμΩνΩξΩοΩπΩρΩσΩτΩυΩφΩχΩψΩωΩςΩάΩίΩήΩέΩόΩύΩ‐ ώΩϊΩϋΩΐΩΰ
πεζά+στίξη-lc+punctuation:
.α.β.γ.δ.ε.ζ.η.θ.ι.κ.λ.μ.ν.ξ.ο.π.ρ.σ.τ.υ.φ.χ.ψ.ω.ς. ·α·β·γ·δ·ε·ζ·η·θ·ι·κ·λ·μ·ν·ξ·ο·π·ρ·σ·τ·υ·φ·χ·ψ·ω·ς· ,α,β,γ,δ,ε,ζ,η,θ,ι,κ,λ,μ,ν,ξ,ο,π,ρ,σ,τ,υ,φ,χ,ψ,ω,ς, !α!β!γ!δ!ε!ζ!η!θ!ι!κ!λ!μ!ν!ξ!ο!π!ρ!σ!τ!υ!φ!χ!ψ!ω!ς! ;α;β;γ;δ;ε;ζ;η;θ;ι;κ;λ;μ;ν;ξ;ο;π;ρ;σ;τ;υ;φ;χ;ψ;ω;ς (α(β(γ(δ(ε(ζ(η(θ(ι(κ(λ(μ(ν(ξ(ο(π(ρ(σ(τ(υ(φ(χ(ψ(ω(ς( )α)β)γ)δ)ε)ζ)η)θ)ι)κ)λ)μ)ν)ξ)ο)π)ρ)σ)τ)υ)φ)χ)ψ)ω)ς) [α[β[γ[δ[ε[ζ[η[θ[ι[κ[λ[μ[ν[ξ[ο[π[ρ[σ[τ[υ[φ[χ[ψ[ω[ς[ ]α]β]γ]δ]ε]ζ]η]θ]ι]κ]λ]μ]ν]ξ]ο]π]ρ]σ]τ]υ]φ]χ]ψ]ω]ς] {α{β{γ{δ{ε{ζ{η{θ{ι{κ{λ{μ{ν{ξ{ο{π{ρ{σ{τ{υ{φ{χ{ψ{ω{ς{ }α}β}γ}δ}ε}ζ}η}θ}ι}κ}λ}μ}ν}ξ}ο}π}ρ}σ}τ}υ}φ}χ}ψ}ω}ς} /α/β/γ/δ/ε/ζ/η/θ/ι/κ/λ/μ/ν/ξ/ο/π/ρ/σ/τ/υ/φ/χ/ψ/ω/ς/ ¦α¦β¦γ¦δ¦ε¦ζ¦η¦θ¦ι¦κ¦λ¦μ¦ν¦ξ¦ο¦π¦ρ¦σ¦τ¦υ¦φ¦χ¦ψ¦ω¦ς¦ |α|β|γ|δ|ε|ζ|η|θ|ι|κ|λ|μ|ν|ξ|ο|π|ρ|σ|τ|υ|φ|χ|ψ|ω|ς| “α“β“γ“δ“ε“ζ“η“θ“ι“κ“λ“μ“ν“ξ“ο“π“ρ“σ“τ“υ“φ“χ“ψ“ω“ς ‘α‘β‘γ‘δ‘ε‘ζ‘η‘θ‘ι‘κ‘λ‘μ‘ν‘ξ‘ο‘π‘ρ‘σ‘τ‘υ‘φ‘χ‘ψ‘ω‘ς 'α'β'γ'δ'ε'ζ'η'θ'ι'κ'λ'μ'ν'ξ'ο'π'ρ'σ'τ'υ'φ'χ'ψ'ω'ς *α*β*γ*δ*ε*ζ*η*θ*ι*κ*λ*μ*ν*ξ*ο*π*ρ*σ*τ*υ*φ*χ*ψ*ω*ς «α«β«γ«δ«ε«ζ«η«θ«ι«κ«λ«μ«ν«ξ«ο«π«ρ«σ«τ«υ«φ«χ«ψ«ω«ς »α»β»γ»δ»ε»ζ»η»θ»ι»κ»λ»μ»ν»ξ»ο»π»ρ»σ»τ»υ»φ»χ»ψ»ω»ς ...α...β...γ...δ...ε...ζ...η...θ...ι...κ...λ...μ...ν...ξ...ο...π...ρ...σ...τ...υ...φ...χ...ψ...ω...ς :α:β:γ:δ:ε:ζ:η:θ:ι:κ:λ:μ:ν:ξ:ο:π:ρ:σ:τ:υ:φ:χ:ψ:ω:ς _α_β_γ_δ_ε_ζ_η_θ_ι_κ_λ_μ_ν_ξ_ο_π_ρ_σ_τ_υ_φ_χ_ψ_ω_ς  ̄α ̄β ̄γ ̄δ ̄ε ̄ζ ̄η ̄θ ̄ι ̄κ ̄λ ̄μ ̄ν ̄ξ ̄ο ̄π ̄ρ ̄σ ̄τ ̄υ ̄φ ̄χ ̄ψ ̄ω ̄ς –α–β–γ–δ–ε–ζ–η–θ–ι–κ–λ–μ–ν–ξ–ο–π–ρ–σ–τ–υ–φ–χ–ψ–ω–ς ‐α‐β‐γ‐δ‐ε‐ζ‐η‐θ‐ι‐κ‐λ‐μ‐ν‐ξ‐ο‐π‐ρ‐σ‐τ‐υ‐φ‐χ‐ψ‐ω‐ς ——α—β—γ—δ—ε—ζ—η—θ—ι—κ—λ—μ—ν—ξ—ο—π—ρ—σ—τ—υ—φ—χ—ψ—ω—ς ‚α‚β‚γ‚δ‚ε‚ζ‚η‚θ‚ι‚κ‚λ‚μ‚ν‚ξ‚ο‚π‚ρ‚σ‚τ‚υ‚φ‚χ‚ψ‚ω‚ς §α§β§γ§δ§ε§ζ§η§θ§ι§κ§λ§μ§ν§ξ§ο§π§ρ§σ§τ§υ§φ§χ§ψ§ω§ς #α#β#γ#δ#ε#ζ#η#θ#ι#κ#λ#μ#ν#ξ#ο#π#ρ#σ#τ#υ#φ#χ#ψ#ω#ς

¶α¶β¶γ¶δ¶ε¶ζ¶η¶θ¶ι¶κ¶λ¶μ¶ν¶ξ¶ο¶π¶ρ¶σ¶τ¶υ¶φ¶χ¶ψ¶ω¶ς †α†β†γ†δ†ε†ζ†η†θ†ι†κ†λ†μ†ν†ξ†ο†π†ρ†σ†τ†υ†φ†χ†ψ†ω†ς \α\β\γ\δ\ε\ζ\η\θ\ι\κ\λ\μ\ν\ξ\ο\π\ρ\σ\τ\υ\φ\χ\ψ\ω\ς ~α~β~γ~δ~ε~ζ~η~θ~ι~κ~λ~μ~ν~ξ~ο~π~ρ~σ~τ~υ~φ~χ~ψ~ω~ς
κεφαλαία+στίξη-UC+punctuation:
. Α. Β.Γ.Δ.Ε.Ζ. Η.Θ. Ι. Κ.Λ.Μ.Ν.Ξ.Ο.Π. Ρ.Σ.Τ. Υ.Φ.Χ. Ψ.Ω.Ά.Έ. Ή. Ί.Ό. Ύ.Ώ. ·α·β·γ·δ·ε·ζ·η·θ·ι·κ·λ·μ·ν·ξ·ο·π·ρ·σ·τ·υ·φ·χ·ψ·ω·ς·Ά·Έ·Ή·Ί·Ό·Ύ·Ώ·
, Α, Β,Γ,Δ,Ε,Ζ, Η,Θ, Ι, Κ,Λ,Μ,Ν,Ξ,Ο,Π, Ρ,Σ,Τ, Υ,Φ,Χ, Ψ,Ω,Ά,Έ, Ή, Ί,Ό, Ύ,Ώ,
!Α! Β!Γ!Δ!Ε!Ζ! Η!Θ! Ι! Κ!Λ!Μ!Ν!Ξ!Ο!Π! Ρ!Σ!Τ ! Υ!Φ!Χ! Ψ!Ω!Ά!Έ! Ή! Ί!Ό! Ύ!Ώ! ;Α;Β;Γ;Δ;Ε;Ζ;Η;Θ;Ι;Κ;Λ;Μ;Ν;Ξ;Ο;Π;Ρ;Σ;Τ;Υ;Φ;Χ;Ψ;Ω;Ά;Έ;Ή;Ί;Ό;Ύ;Ώ; (Α(Β(Γ(Δ(Ε(Ζ(Η(Θ(Ι(Κ(Λ(Μ(Ν(Ξ(Ο(Π(Ρ(Σ(Τ(Υ(Φ(Χ(Ψ(Ω(Ά(Έ(Ή(Ί(Ό(Ύ(Ώ )Α)Β)Γ)Δ)Ε )Ζ)Η)Θ)Ι)Κ)Λ)Μ)Ν)Ξ)Ο)Π)Ρ)Σ)Τ)Υ)Φ)Χ)Ψ)Ω)Ά)Έ )Ή)Ί)Ό)Ύ)Ώ [Α[Β[Γ[Δ[Ε[Ζ[Η[Θ[Ι[Κ[Λ[Μ[Ν[Ξ[Ο[Π[Ρ[Σ[Τ[Υ[Φ[Χ[Ψ[Ω[Ά[Έ[Ή[Ί[Ό[Ύ[Ώ ]Α]Β]Γ]Δ]Ε ]Ζ]Η]Θ]Ι]Κ]Λ]Μ]Ν]Ξ]Ο]Π]Ρ]Σ]Τ]Υ]Φ]Χ]Ψ]Ω]Ά]Έ ]Ή]Ί]Ό]Ύ]Ώ {Α{Β{Γ{Δ{Ε{Ζ{Η{Θ{Ι{Κ{Λ{Μ{Ν{Ξ{Ο{Π{Ρ{Σ{Τ{Υ{Φ{Χ{Ψ{Ω{Ά{Έ{Ή{Ί{Ό{Ύ{Ώ }Α}Β}Γ}Δ}Ε }Ζ}Η}Θ}Ι}Κ}Λ}Μ}Ν}Ξ}Ο}Π}Ρ}Σ}Τ}Υ}Φ}Χ}Ψ}Ω}Ά}Έ }Ή}Ί}Ό}Ύ}Ώ *Α*Β*Γ*Δ*Ε*Ζ*Η*Θ*Ι*Κ*Λ*Μ*Ν*Ξ*Ο*Π*Ρ*Σ*Τ *Υ*Φ*Χ*Ψ*Ω*Ά*Έ*Ή*Ί*Ό*Ύ*Ώ •Α•Β•Γ•Δ•Ε •Ζ•Η•Θ•Ι•Κ•Λ•Μ•Ν•Ξ•Ο•Π•Ρ•Σ•Τ•Υ•Φ•Χ•Ψ•Ω•Ά•Έ •Ή•Ί•Ό•Ύ•Ώ —Α—Β—Γ—Δ—Ε —Ζ—Η—Θ—Ι—Κ—Λ—Μ—Ν—Ξ—Ο—Π—Ρ—Σ—Τ—Υ—Φ—Χ—Ψ—Ω—Ά—Έ —Ή— Ί—Ό—Ύ—Ώ
–Α–Β–Γ–Δ–Ε –Ζ–Η–Θ–Ι–Κ–Λ–Μ–Ν–Ξ–Ο–Π–Ρ–Σ–Τ–Υ–Φ–Χ–Ψ–Ω–Ά–Έ –Ή–Ί–Ό–Ύ–Ώ ‐Α‐Β‐Γ‐Δ‐Ε ‐Ζ‐Η‐Θ‐Ι‐Κ‐Λ‐Μ‐Ν‐Ξ‐Ο‐Π‐Ρ‐Σ‐Τ‐Υ‐Φ‐Χ‐Ψ‐Ω‐Ά‐Έ ‐Ή‐Ί‐Ό‐Ύ‐Ώ _Α_Β_Γ_Δ_Ε_Ζ_Η_Θ_Ι_Κ_Λ_Μ_Ν_Ξ_Ο_Π_Ρ_Σ_Τ_Υ_Φ_Χ_Ψ_Ω_Ά_Έ_Ή_Ί_Ό_Ύ_Ώ
Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ ΥΦ Χ Ψ Ω Σ ΆΈ Ή Ί Ό ΎΏ
/Α/ Β/Γ/Δ/Ε/Ζ/ Η/Θ/ Ι/ Κ/Λ/Μ/Ν/Ξ/Ο/Π/ Ρ/Σ/ Τ/ Υ/Φ/Χ/ Ψ/Ω/Σ/Ά/Έ/ Ή/ Ί/Ό/ Ύ/Ώ
¦Α¦ Β¦Γ¦Δ¦Ε¦Ζ¦ Η¦Θ¦ Ι¦ Κ¦Λ¦Μ¦Ν¦Ξ¦Ο¦Π¦ Ρ¦Σ¦Τ¦ Υ¦Φ¦Χ¦ Ψ¦Ω¦Σ¦Ά¦Έ¦ Ή¦ Ί¦Ό¦ Ύ¦Ώ |Α|Β|Γ|Δ|Ε|Ζ|Η|Θ|Ι|Κ|Λ|Μ|Ν|Ξ|Ο|Π|Ρ|Σ|Τ|Υ|Φ|Χ|Ψ|Ω|Σ|Ά|Έ|Ή|Ί|Ό|Ύ|Ώ “Α“Β“Γ“Δ“Ε“Ζ“Η“Θ“Ι“Κ“Λ“Μ“Ν“Ξ“Ο“Π“Ρ“Σ“Τ “Υ“Φ“Χ“Ψ“Ω“Σ“Ά“Έ“Ή“Ί“Ό“Ύ“Ώ ‘Α‘Β‘Γ‘Δ‘Ε‘Ζ‘Η‘Θ‘Ι‘Κ‘Λ‘Μ‘Ν‘Ξ‘Ο‘Π‘Ρ‘Σ‘Τ ‘Υ‘Φ‘Χ‘Ψ‘Ω‘Σ‘Ά‘Έ‘Ή‘Ί‘Ό‘Ύ‘Ώ 'Α'Β'Γ'Δ'Ε'Ζ'Η'Θ'Ι'Κ'Λ'Μ'Ν'Ξ'Ο'Π'Ρ'Σ'Τ 'Υ'Φ'Χ'Ψ'Ω'Σ'Ά'Έ'Ή'Ί'Ό'Ώ «Α«Β«Γ«Δ«Ε «Ζ«Η«Θ«Ι«Κ«Λ«Μ«Ν«Ξ«Ο«Π«Ρ«Σ«Τ«Υ«Φ«Χ«Ψ«Ω«Σ«Ά«Έ «Ή«Ί‐ «Ό«Ύ«Ώ
»Α»Β»Γ»Δ»Ε »Ζ»Η»Θ»Ι»Κ»Λ»Μ»Ν»Ξ»Ο»Π»Ρ»Σ»Τ»Υ»Φ»Χ»Ψ»Ω»Σ»Ά»Έ »Ή»Ί‐ »Ό»Ύ»Ώ
... Α... Β...Γ...Δ...Ε...Ζ... Η...Θ... Ι... Κ...Λ...Μ...Ν...Ξ...Ο...Π... Ρ...Σ...Τ... Υ...Φ...Χ... Ψ...Ω... Σ...Ά...Έ... Ή... Ί...Ό... Ύ...Ώ :Α:Β:Γ:Δ:Ε:Ζ:Η:Θ:Ι:Κ:Λ:Μ:Ν:Ξ:Ο:Π:Ρ:Σ:Τ:Υ:Φ:Χ:Ψ:Ω:Σ:Ά:Έ:Ή:Ί:Ό:Ύ:Ώ _Α_Β_Γ_Δ_Ε_Ζ_Η_Θ_Ι_Κ_Λ_Μ_Ν_Ξ_Ο_Π_Ρ_Σ_Τ_Υ_Φ_Χ_Ψ_Ω_ Σ_Ά_Έ_Ή_Ί_Ό_Ύ_Ώ  ̄Α ̄Β ̄Γ ̄Δ ̄Ε ̄Ζ ̄Η ̄Θ ̄Ι ̄Κ ̄Λ ̄Μ ̄Ν ̄Ξ ̄Ο ̄Π ̄Ρ ̄Σ ̄Τ ̄Υ ̄Φ ̄Χ ̄Ψ ̄Ω ̄Σ ̄Ά ̄Έ ̄Ή ̄Ί ̄Ό ̄Ύ ̄Ώ

–Α–Β–Γ–Δ–Ε –Ζ–Η–Θ–Ι–Κ–Λ–Μ–Ν–Ξ–Ο–Π–Ρ–Σ–Τ–Υ–Φ–Χ–Ψ–Ω–Σ–Ά–Έ –Ή– Ί–Ό–Ύ–Ώ
‐Α‐Β‐Γ‐Δ‐Ε ‐Ζ‐Η‐Θ‐Ι‐Κ‐Λ‐Μ‐Ν‐Ξ‐Ο‐Π‐Ρ‐Σ‐Τ‐Υ‐Φ‐Χ‐Ψ‐Ω‐Σ‐Ά‐Έ ‐Ή‐Ί‐Ό‐Ώ ——Α—Β—Γ—Δ—Ε —Ζ—Η—Θ—Ι—Κ—Λ—Μ—Ν—Ξ—Ο—Π—Ρ—Σ—Τ—Υ—Φ—Χ—Ψ— Ω—Σ—Ά—Έ—Ή—Ί—Ό—Ύ—Ώ
‚ Α‚ Β‚Γ‚Δ‚Ε‚Ζ‚ Η‚Θ‚ Ι‚ Κ‚Λ‚Μ‚Ν‚Ξ‚Ο‚Π‚ Ρ‚Σ‚Τ‚ Υ‚Φ‚Χ‚ Ψ‚Ω‚Σ‚Ά‚Έ‚ Ή‚ Ί‚Ό‚ Ύ‚Ώ §Α§Β§Γ§Δ§Ε§Ζ§Η§Θ§Ι§Κ§Λ§Μ§Ν§Ξ§Ο§Π§Ρ§Σ§Τ§Υ§Φ§Χ§‐ Ψ§Ω§Σ§Ά§Έ§Ή§Ί§Ό§Ύ§Ώ #Α#Β#Γ#Δ#Ε#Ζ#Η#Θ#Ι#Κ#Λ#Μ#Ν#Ξ#Ο#Π#Ρ#Σ#Τ#Υ#Φ#Χ#‐ Ψ#Ω#Σ#Ά#Έ#Ή#Ί#Ό#Ύ#Ώ ¶Α¶Β¶Γ¶Δ¶Ε¶Ζ¶Η¶Θ¶Ι¶Κ¶Λ¶Μ¶Ν¶Ξ¶Ο¶Π¶Ρ¶Σ¶Τ¶Υ¶Φ¶Χ¶‐ Ψ¶Ω¶Σ¶Ά¶Έ¶Ή¶Ί¶Ό¶Ύ¶Ώ †Α†Β†Γ†Δ†Ε†Ζ†Η†Θ†Ι†Κ†Λ†Μ†Ν†Ξ†Ο†Π†Ρ†Σ†Τ†Υ†Φ†Χ†Ψ†Ω†‐ Σ†Ά†Έ†Ή†Ί†Ό†Ύ†Ώ \Α\Β\Γ\Δ\Ε\Ζ\Η\Θ\Ι\Κ\Λ\Μ\Ν\Ξ\Ο\Π\Ρ\Σ\Τ\Υ\Φ\Χ\Ψ\Ω\Σ\Ά\Έ\Ή\Ί\Ό\Ή\ Ύ\Ώ
~Α~Β~Γ~Δ~Ε ~Ζ~Η~Θ~Ι~Κ~Λ~Μ~Ν~Ξ~Ο~Π~Ρ~Σ~Τ~Υ~Φ~Χ~‐ Ψ~Ω~Σ~Ά~Έ~Ή~Ί~Ό~Ύ~Ώ
"""

# TODO: Make these work in the sample pages.
AAA = {
    'Kern Cyr-lc-sorts': """/zhecyrillic/period /zhecyrillic/comma /zhecyrillic/colon /zhecyrillic/semicolon /zhecyrillic/exclam /zhecyrillic/question /parenleft/zhecyrillic /zhecyrillic/parenright /bracketleft/zhecyrillic /zhecyrillic/bracketright /zhecyrillic/hyphen /zhecyrillic/bullet /quoteleft/zhecyrillic /zhecyrillic/quoteright /quotesinglbase/zhecyrillic /zhecyrillic/quoteleft /guillemotleft/zhecyrillic /zhecyrillic/guillemotright /zhecyrillic/slash /zhecyrillic/backslash /zhecyrillic/asterisk /zhecyrillic/dagger /zhecyrillic/daggerdbl /zhecyrillic/trademark /zhecyrillic/at /zhecyrillic/registered /zhecyrillic/copyright /kacyrillic/period /kacyrillic/comma /kacyrillic/colon /kacyrillic/semicolon /kacyrillic/exclam /kacyrillic/question /parenleft/kacyrillic /kacyrillic/parenright /bracketleft/kacyrillic /kacyrillic/bracketright /kacyrillic/hyphen /kacyrillic/bullet /quoteleft/kacyrillic /kacyrillic/quoteright /quotesinglbase/kacyrillic /kacyrillic/quoteleft /guillemotleft/kacyrillic /kacyrillic/guillemotright /kacyrillic/slash /kacyrillic/backslash /kacyrillic/asterisk /kacyrillic/dagger /kacyrillic/daggerdbl /kacyrillic/trademark /kacyrillic/at /kacyrillic/registered /kacyrillic/copyright /ucyrillic/period /ucyrillic/comma /ucyrillic/colon /ucyrillic/semicolon /ucyrillic/exclam /ucyrillic/question /parenleft/ucyrillic /ucyrillic/parenright /bracketleft/ucyrillic /ucyrillic/bracketright /ucyrillic/hyphen /ucyrillic/bullet /quoteleft/ucyrillic /ucyrillic/quoteright /quotesinglbase/ucyrillic /ucyrillic/quoteleft /guillemotleft/ucyrillic /ucyrillic/guillemotright /ucyrillic/slash /ucyrillic/backslash /ucyrillic/asterisk /ucyrillic/dagger /ucyrillic/daggerdbl /ucyrillic/trademark /ucyrillic/at /ucyrillic/registered /ucyrillic/copyright /ustraightstrokecyrillic/period /ustraightstrokecyrillic/comma /ustraightstrokecyrillic/colon /ustraightstrokecyrillic/semicolon /ustraightstrokecyrillic/exclam /ustraightstrokecyrillic/question /parenleft/ustraightstrokecyrillic /ustraightstrokecyrillic/parenright /bracketleft/ustraightstrokecyrillic /ustraightstrokecyrillic/bracketright /ustraightstrokecyrillic/hyphen /ustraightstrokecyrillic/bullet /quoteleft/ustraightstrokecyrillic /ustraightstrokecyrillic/quoteright /quotesinglbase/ustraightstrokecyrillic /ustraightstrokecyrillic/quoteleft /guillemotleft/ustraightstrokecyrillic /ustraightstrokecyrillic/guillemotright /ustraightstrokecyrillic/slash /ustraightstrokecyrillic/backslash /ustraightstrokecyrillic/asterisk /ustraightstrokecyrillic/dagger /ustraightstrokecyrillic/daggerdbl /ustraightstrokecyrillic/trademark /ustraightstrokecyrillic/at /ustraightstrokecyrillic/registered /ustraightstrokecyrillic/copyright /khacyrillic/period /khacyrillic/comma /khacyrillic/colon /khacyrillic/semicolon /khacyrillic/exclam /khacyrillic/question /parenleft/khacyrillic /khacyrillic/parenright /bracketleft/khacyrillic /khacyrillic/bracketright /khacyrillic/hyphen /khacyrillic/bullet /quoteleft/khacyrillic /khacyrillic/quoteright /quotesinglbase/khacyrillic /khacyrillic/quoteleft /guillemotleft/khacyrillic /khacyrillic/guillemotright /khacyrillic/slash /khacyrillic/backslash /khacyrillic/asterisk /khacyrillic/dagger /khacyrillic/daggerdbl /khacyrillic/trademark /khacyrillic/at /khacyrillic/registered /khacyrillic/copyright
/becyrillic/period /becyrillic/comma /becyrillic/colon /becyrillic/semicolon /becyrillic/exclam /becyrillic/question /parenleft/becyrillic /becyrillic/parenright /bracketleft/becyrillic /becyrillic/bracketright /becyrillic/hyphen /becyrillic/bullet /quoteleft/becyrillic /becyrillic/quoteright /quotesinglbase/becyrillic /becyrillic/quoteleft /guillemotleft/becyrillic /becyrillic/guillemotright /becyrillic/slash /becyrillic/backslash /becyrillic/asterisk /becyrillic/dagger /becyrillic/daggerdbl /becyrillic/trademark /becyrillic/at /becyrillic/registered /becyrillic/copyright /iecyrillic/period /iecyrillic/comma /iecyrillic/colon /iecyrillic/semicolon /iecyrillic/exclam /iecyrillic/question /parenleft/iecyrillic /iecyrillic/parenright /bracketleft/iecyrillic /iecyrillic/bracketright /iecyrillic/hyphen /iecyrillic/bullet /quoteleft/iecyrillic /iecyrillic/quoteright /quotesinglbase/iecyrillic /iecyrillic/quoteleft /guillemotleft/iecyrillic /iecyrillic/guillemotright /iecyrillic/slash /iecyrillic/backslash /iecyrillic/asterisk /iecyrillic/dagger /iecyrillic/daggerdbl /iecyrillic/trademark /iecyrillic/at /iecyrillic/registered /iecyrillic/copyright /ocyrillic/period /ocyrillic/comma /ocyrillic/colon /ocyrillic/semicolon /ocyrillic/exclam /ocyrillic/question /parenleft/ocyrillic /ocyrillic/parenright /bracketleft/ocyrillic /ocyrillic/bracketright /ocyrillic/hyphen /ocyrillic/bullet /quoteleft/ocyrillic /ocyrillic/quoteright /quotesinglbase/ocyrillic /ocyrillic/quoteleft /guillemotleft/ocyrillic /ocyrillic/guillemotright /ocyrillic/slash /ocyrillic/backslash /ocyrillic/asterisk /ocyrillic/dagger /ocyrillic/daggerdbl /ocyrillic/trademark /ocyrillic/at /ocyrillic/registered /ocyrillic/copyright /ercyrillic/period /ercyrillic/comma /ercyrillic/colon /ercyrillic/semicolon /ercyrillic/exclam /ercyrillic/question /parenleft/ercyrillic /ercyrillic/parenright /bracketleft/ercyrillic /ercyrillic/bracketright /ercyrillic/hyphen /ercyrillic/bullet /quoteleft/ercyrillic /ercyrillic/quoteright /quotesinglbase/ercyrillic /ercyrillic/quoteleft /guillemotleft/ercyrillic /ercyrillic/guillemotright /ercyrillic/slash /ercyrillic/backslash /ercyrillic/asterisk /ercyrillic/dagger /ercyrillic/daggerdbl /ercyrillic/trademark /ercyrillic/at /ercyrillic/registered /ercyrillic/copyright /escyrillic/period /escyrillic/comma /escyrillic/colon /escyrillic/semicolon /escyrillic/exclam /escyrillic/question /parenleft/escyrillic /escyrillic/parenright /bracketleft/escyrillic /escyrillic/bracketright /escyrillic/hyphen /escyrillic/bullet /quoteleft/escyrillic /escyrillic/quoteright /quotesinglbase/escyrillic /escyrillic/quoteleft /guillemotleft/escyrillic /escyrillic/guillemotright /escyrillic/slash /escyrillic/backslash /escyrillic/asterisk /escyrillic/dagger /escyrillic/daggerdbl /escyrillic/trademark /escyrillic/at /escyrillic/registered /escyrillic/copyright /efcyrillic/period /efcyrillic/comma /efcyrillic/colon /efcyrillic/semicolon /efcyrillic/exclam /efcyrillic/question /parenleft/efcyrillic /efcyrillic/parenright /bracketleft/efcyrillic /efcyrillic/bracketright /efcyrillic/hyphen /efcyrillic/bullet /quoteleft/efcyrillic /efcyrillic/quoteright /quotesinglbase/efcyrillic /efcyrillic/quoteleft /guillemotleft/efcyrillic /efcyrillic/guillemotright /efcyrillic/slash /efcyrillic/backslash /efcyrillic/asterisk /efcyrillic/dagger /efcyrillic/daggerdbl /efcyrillic/trademark /efcyrillic/at /efcyrillic/registered /efcyrillic/copyright /iucyrillic/period /iucyrillic/comma /iucyrillic/colon /iucyrillic/semicolon /iucyrillic/exclam /iucyrillic/question /parenleft/iucyrillic /iucyrillic/parenright /bracketleft/iucyrillic /iucyrillic/bracketright /iucyrillic/hyphen /iucyrillic/bullet /quoteleft/iucyrillic /iucyrillic/quoteright /quotesinglbase/iucyrillic /iucyrillic/quoteleft /guillemotleft/iucyrillic /iucyrillic/guillemotright /iucyrillic/slash /iucyrillic/backslash /iucyrillic/asterisk /iucyrillic/dagger /iucyrillic/daggerdbl /iucyrillic/trademark /iucyrillic/at /iucyrillic/registered /iucyrillic/copyright
/ecyrillic/period /ecyrillic/comma /ecyrillic/colon /ecyrillic/semicolon /ecyrillic/exclam /ecyrillic/question /parenleft/ecyrillic /ecyrillic/parenright /bracketleft/ecyrillic /ecyrillic/bracketright /ecyrillic/hyphen /ecyrillic/bullet /quoteleft/ecyrillic /ecyrillic/quoteright /quotesinglbase/ecyrillic /ecyrillic/quoteleft /guillemotleft/ecyrillic /ecyrillic/guillemotright /ecyrillic/slash /ecyrillic/backslash /ecyrillic/asterisk /ecyrillic/dagger /ecyrillic/daggerdbl /ecyrillic/trademark /ecyrillic/at /ecyrillic/registered /ecyrillic/copyright /ereversedcyrillic/period /ereversedcyrillic/comma /ereversedcyrillic/colon /ereversedcyrillic/semicolon /ereversedcyrillic/exclam /ereversedcyrillic/question /parenleft/ereversedcyrillic /ereversedcyrillic/parenright /bracketleft/ereversedcyrillic /ereversedcyrillic/bracketright /ereversedcyrillic/hyphen /ereversedcyrillic/bullet /quoteleft/ereversedcyrillic /ereversedcyrillic/quoteright /quotesinglbase/ereversedcyrillic /ereversedcyrillic/quoteleft /guillemotleft/ereversedcyrillic /ereversedcyrillic/guillemotright /ereversedcyrillic/slash /ereversedcyrillic/backslash /ereversedcyrillic/asterisk /ereversedcyrillic/dagger /ereversedcyrillic/daggerdbl /ereversedcyrillic/trademark /ereversedcyrillic/at /ereversedcyrillic/registered /ereversedcyrillic/copyright
/becyrillic/period /becyrillic/comma /becyrillic/colon /becyrillic/semicolon /becyrillic/exclam /becyrillic/question /parenleft/becyrillic /becyrillic/parenright /bracketleft/becyrillic /becyrillic/bracketright /becyrillic/hyphen /becyrillic/bullet /quoteleft/becyrillic /becyrillic/quoteright /quotesinglbase/becyrillic /becyrillic/quoteleft /guillemotleft/becyrillic /becyrillic/guillemotright /becyrillic/slash /becyrillic/backslash /becyrillic/asterisk /becyrillic/dagger /becyrillic/daggerdbl /becyrillic/trademark /becyrillic/at /becyrillic/registered /becyrillic/copyright /hardsigncyrillic/period /hardsigncyrillic/comma /hardsigncyrillic/colon /hardsigncyrillic/semicolon /hardsigncyrillic/exclam /hardsigncyrillic/question /parenleft/hardsigncyrillic /hardsigncyrillic/parenright /bracketleft/hardsigncyrillic /hardsigncyrillic/bracketright /hardsigncyrillic/hyphen /hardsigncyrillic/bullet /quoteleft/hardsigncyrillic /hardsigncyrillic/quoteright /quotesinglbase/hardsigncyrillic /hardsigncyrillic/quoteleft /guillemotleft/hardsigncyrillic /hardsigncyrillic/guillemotright /hardsigncyrillic/slash /hardsigncyrillic/backslash /hardsigncyrillic/asterisk /hardsigncyrillic/dagger /hardsigncyrillic/daggerdbl /hardsigncyrillic/trademark /hardsigncyrillic/at /hardsigncyrillic/registered /hardsigncyrillic/copyright /softsigncyrillic/period /softsigncyrillic/comma /softsigncyrillic/colon /softsigncyrillic/semicolon /softsigncyrillic/exclam /softsigncyrillic/question /parenleft/softsigncyrillic /softsigncyrillic/parenright /bracketleft/softsigncyrillic /softsigncyrillic/bracketright /softsigncyrillic/hyphen /softsigncyrillic/bullet /quoteleft/softsigncyrillic /softsigncyrillic/quoteright /quotesinglbase/softsigncyrillic /softsigncyrillic/quoteleft /guillemotleft/softsigncyrillic /softsigncyrillic/guillemotright /softsigncyrillic/slash /softsigncyrillic/backslash /softsigncyrillic/asterisk /softsigncyrillic/dagger /softsigncyrillic/daggerdbl /softsigncyrillic/trademark /softsigncyrillic/at /softsigncyrillic/registered /softsigncyrillic/copyright /njecyrillic/period /njecyrillic/comma /njecyrillic/colon /njecyrillic/semicolon /njecyrillic/exclam /njecyrillic/question /parenleft/njecyrillic /njecyrillic/parenright /bracketleft/njecyrillic /njecyrillic/bracketright /njecyrillic/hyphen /njecyrillic/bullet /quoteleft/njecyrillic /njecyrillic/quoteright /quotesinglbase/njecyrillic /njecyrillic/quoteleft /guillemotleft/njecyrillic /njecyrillic/guillemotright /njecyrillic/slash /njecyrillic/backslash /njecyrillic/asterisk /njecyrillic/dagger /njecyrillic/daggerdbl /njecyrillic/trademark /njecyrillic/at /njecyrillic/registered /njecyrillic/copyright /ljecyrillic/period /ljecyrillic/comma /ljecyrillic/colon /ljecyrillic/semicolon /ljecyrillic/exclam /ljecyrillic/question /parenleft/ljecyrillic /ljecyrillic/parenright /bracketleft/ljecyrillic /ljecyrillic/bracketright /ljecyrillic/hyphen /ljecyrillic/bullet /quoteleft/ljecyrillic /ljecyrillic/quoteright /quotesinglbase/ljecyrillic /ljecyrillic/quoteleft /guillemotleft/ljecyrillic /ljecyrillic/guillemotright /ljecyrillic/slash /ljecyrillic/backslash /ljecyrillic/asterisk /ljecyrillic/dagger /ljecyrillic/daggerdbl /ljecyrillic/trademark /ljecyrillic/at /ljecyrillic/registered /ljecyrillic/copyright /elcyrillic/period /elcyrillic/comma /elcyrillic/colon /elcyrillic/semicolon /elcyrillic/exclam /elcyrillic/question /parenleft/elcyrillic /elcyrillic/parenright /bracketleft/elcyrillic /elcyrillic/bracketright /elcyrillic/hyphen /elcyrillic/bullet /quoteleft/elcyrillic /elcyrillic/quoteright /quotesinglbase/elcyrillic /elcyrillic/quoteleft /guillemotleft/elcyrillic /elcyrillic/guillemotright /elcyrillic/slash /elcyrillic/backslash /elcyrillic/asterisk /elcyrillic/dagger /elcyrillic/daggerdbl /elcyrillic/trademark /elcyrillic/at /elcyrillic/registered /elcyrillic/copyright
/decyrillic/period /decyrillic/comma /decyrillic/colon /decyrillic/semicolon /decyrillic/exclam /decyrillic/question /parenleft/decyrillic /decyrillic/parenright /bracketleft/decyrillic /decyrillic/bracketright /decyrillic/hyphen /decyrillic/bullet /quoteleft/decyrillic /decyrillic/quoteright /quotesinglbase/decyrillic /decyrillic/quoteleft /guillemotleft/decyrillic /decyrillic/guillemotright /decyrillic/slash /decyrillic/backslash /decyrillic/asterisk /decyrillic/dagger /decyrillic/daggerdbl /decyrillic/trademark /decyrillic/at /decyrillic/registered /decyrillic/copyright /tsecyrillic/period /tsecyrillic/comma /tsecyrillic/colon /tsecyrillic/semicolon /tsecyrillic/exclam /tsecyrillic/question /parenleft/tsecyrillic /tsecyrillic/parenright /bracketleft/tsecyrillic /tsecyrillic/bracketright /tsecyrillic/hyphen /tsecyrillic/bullet /quoteleft/tsecyrillic /tsecyrillic/quoteright /quotesinglbase/tsecyrillic /tsecyrillic/quoteleft /guillemotleft/tsecyrillic /tsecyrillic/guillemotright /tsecyrillic/slash /tsecyrillic/backslash /tsecyrillic/asterisk /tsecyrillic/dagger /tsecyrillic/daggerdbl /tsecyrillic/trademark /tsecyrillic/at /tsecyrillic/registered /tsecyrillic/copyright /chedescendercyrillic/period /chedescendercyrillic/comma /chedescendercyrillic/colon /chedescendercyrillic/semicolon /chedescendercyrillic/exclam /chedescendercyrillic/question /parenleft/chedescendercyrillic /chedescendercyrillic/parenright /bracketleft/chedescendercyrillic /chedescendercyrillic/bracketright /chedescendercyrillic/hyphen /chedescendercyrillic/bullet /quoteleft/chedescendercyrillic /chedescendercyrillic/quoteright /quotesinglbase/chedescendercyrillic /chedescendercyrillic/quoteleft /guillemotleft/chedescendercyrillic /chedescendercyrillic/guillemotright /chedescendercyrillic/slash /chedescendercyrillic/backslash /chedescendercyrillic/asterisk /chedescendercyrillic/dagger /chedescendercyrillic/daggerdbl /chedescendercyrillic/trademark /chedescendercyrillic/at /chedescendercyrillic/registered /chedescendercyrillic/copyright /shchacyrillic/period /shchacyrillic/comma /shchacyrillic/colon /shchacyrillic/semicolon /shchacyrillic/exclam /shchacyrillic/question /parenleft/shchacyrillic /shchacyrillic/parenright /bracketleft/shchacyrillic /shchacyrillic/bracketright /shchacyrillic/hyphen /shchacyrillic/bullet /quoteleft/shchacyrillic /shchacyrillic/quoteright /quotesinglbase/shchacyrillic /shchacyrillic/quoteleft /guillemotleft/shchacyrillic /shchacyrillic/guillemotright /shchacyrillic/slash /shchacyrillic/backslash /shchacyrillic/asterisk /shchacyrillic/dagger /shchacyrillic/daggerdbl /shchacyrillic/trademark /shchacyrillic/at /shchacyrillic/registered /shchacyrillic/copyright /tsecyrillic/period /tsecyrillic/comma /tsecyrillic/colon /tsecyrillic/semicolon /tsecyrillic/exclam /tsecyrillic/question /parenleft/tsecyrillic /tsecyrillic/parenright /bracketleft/tsecyrillic /tsecyrillic/bracketright /tsecyrillic/hyphen /tsecyrillic/bullet /quoteleft/tsecyrillic /tsecyrillic/quoteright /quotesinglbase/tsecyrillic /tsecyrillic/quoteleft /guillemotleft/tsecyrillic /tsecyrillic/guillemotright /tsecyrillic/slash /tsecyrillic/backslash /tsecyrillic/asterisk /tsecyrillic/dagger /tsecyrillic/daggerdbl /tsecyrillic/trademark /tsecyrillic/at /tsecyrillic/registered /tsecyrillic/copyright
/gecyrillic/period /gecyrillic/comma /gecyrillic/colon /gecyrillic/semicolon /gecyrillic/exclam /gecyrillic/question /parenleft/gecyrillic /gecyrillic/parenright /bracketleft/gecyrillic /gecyrillic/bracketright /gecyrillic/hyphen /gecyrillic/bullet /quoteleft/gecyrillic /gecyrillic/quoteright /quotesinglbase/gecyrillic /gecyrillic/quoteleft /guillemotleft/gecyrillic /gecyrillic/guillemotright /gecyrillic/slash /gecyrillic/backslash /gecyrillic/asterisk /gecyrillic/dagger /gecyrillic/daggerdbl /gecyrillic/trademark /gecyrillic/at /gecyrillic/registered /gecyrillic/copyright /tecyrillic/period /tecyrillic/comma /tecyrillic/colon /tecyrillic/semicolon /tecyrillic/exclam /tecyrillic/question /parenleft/tecyrillic /tecyrillic/parenright /bracketleft/tecyrillic /tecyrillic/bracketright /tecyrillic/hyphen /tecyrillic/bullet /quoteleft/tecyrillic /tecyrillic/quoteright /quotesinglbase/tecyrillic /tecyrillic/quoteleft /guillemotleft/tecyrillic /tecyrillic/guillemotright /tecyrillic/slash /tecyrillic/backslash /tecyrillic/asterisk /tecyrillic/dagger /tecyrillic/daggerdbl /tecyrillic/trademark /tecyrillic/at /tecyrillic/registered /tecyrillic/copyright /gheupturncyrillic/period /gheupturncyrillic/comma /gheupturncyrillic/colon /gheupturncyrillic/semicolon /gheupturncyrillic/exclam /gheupturncyrillic/question /parenleft/gheupturncyrillic /gheupturncyrillic/parenright /bracketleft/gheupturncyrillic /gheupturncyrillic/bracketright /gheupturncyrillic/hyphen /gheupturncyrillic/bullet /quoteleft/gheupturncyrillic /gheupturncyrillic/quoteright /quotesinglbase/gheupturncyrillic /gheupturncyrillic/quoteleft /guillemotleft/gheupturncyrillic /gheupturncyrillic/guillemotright /gheupturncyrillic/slash /gheupturncyrillic/backslash /gheupturncyrillic/asterisk /gheupturncyrillic/dagger /gheupturncyrillic/daggerdbl /gheupturncyrillic/trademark /gheupturncyrillic/at /gheupturncyrillic/registered /gheupturncyrillic/copyright
/vecyrillic/period /vecyrillic/comma /vecyrillic/colon /vecyrillic/semicolon /vecyrillic/exclam /vecyrillic/question /parenleft/vecyrillic /vecyrillic/parenright /bracketleft/vecyrillic /vecyrillic/bracketright /vecyrillic/hyphen /vecyrillic/bullet /quoteleft/vecyrillic /vecyrillic/quoteright /quotesinglbase/vecyrillic /vecyrillic/quoteleft /guillemotleft/vecyrillic /vecyrillic/guillemotright /vecyrillic/slash /vecyrillic/backslash /vecyrillic/asterisk /vecyrillic/dagger /vecyrillic/daggerdbl /vecyrillic/trademark /vecyrillic/at /vecyrillic/registered /vecyrillic/copyright /zecyrillic/period /zecyrillic/comma /zecyrillic/colon /zecyrillic/semicolon /zecyrillic/exclam /zecyrillic/question /parenleft/zecyrillic /zecyrillic/parenright /bracketleft/zecyrillic /zecyrillic/bracketright /zecyrillic/hyphen /zecyrillic/bullet /quoteleft/zecyrillic /zecyrillic/quoteright /quotesinglbase/zecyrillic /zecyrillic/quoteleft /guillemotleft/zecyrillic /zecyrillic/guillemotright /zecyrillic/slash /zecyrillic/backslash /zecyrillic/asterisk /zecyrillic/dagger /zecyrillic/daggerdbl /zecyrillic/trademark /zecyrillic/at /zecyrillic/registered /zecyrillic/copyright /iacyrillic/period /iacyrillic/comma /iacyrillic/colon /iacyrillic/semicolon /iacyrillic/exclam /iacyrillic/question /parenleft/iacyrillic /iacyrillic/parenright /bracketleft/iacyrillic /iacyrillic/bracketright /iacyrillic/hyphen /iacyrillic/bullet /quoteleft/iacyrillic /iacyrillic/quoteright /quotesinglbase/iacyrillic /iacyrillic/quoteleft /guillemotleft/iacyrillic /iacyrillic/guillemotright /iacyrillic/slash /iacyrillic/backslash /iacyrillic/asterisk /iacyrillic/dagger /iacyrillic/daggerdbl /iacyrillic/trademark /iacyrillic/at /iacyrillic/registered /iacyrillic/copyright
/checyrillic/period /checyrillic/comma /checyrillic/colon /checyrillic/semicolon /checyrillic/exclam /checyrillic/question /parenleft/checyrillic /checyrillic/parenright /bracketleft/checyrillic /checyrillic/bracketright /checyrillic/hyphen /checyrillic/bullet /quoteleft/checyrillic /checyrillic/quoteright /quotesinglbase/checyrillic /checyrillic/quoteleft /guillemotleft/checyrillic /checyrillic/guillemotright /checyrillic/slash /checyrillic/backslash /checyrillic/asterisk /checyrillic/dagger /checyrillic/daggerdbl /checyrillic/trademark /checyrillic/at /checyrillic/registered /checyrillic/copyright
/dzecyrillic/period /dzecyrillic/comma /dzecyrillic/colon /dzecyrillic/semicolon /dzecyrillic/exclam /dzecyrillic/question /parenleft/dzecyrillic /dzecyrillic/parenright /bracketleft/dzecyrillic /dzecyrillic/bracketright /dzecyrillic/hyphen /dzecyrillic/bullet /quoteleft/dzecyrillic /dzecyrillic/quoteright /quotesinglbase/dzecyrillic /dzecyrillic/quoteleft /guillemotleft/dzecyrillic /dzecyrillic/guillemotright /dzecyrillic/slash /dzecyrillic/backslash /dzecyrillic/asterisk /dzecyrillic/dagger /dzecyrillic/daggerdbl /dzecyrillic/trademark /dzecyrillic/at /dzecyrillic/registered /dzecyrillic/copyright /acyrillic/period /acyrillic/comma /acyrillic/colon /acyrillic/semicolon /acyrillic/exclam /acyrillic/question /parenleft/acyrillic /acyrillic/parenright /bracketleft/acyrillic /acyrillic/bracketright /acyrillic/hyphen /acyrillic/bullet /quoteleft/acyrillic /acyrillic/quoteright /quotesinglbase/acyrillic /acyrillic/quoteleft /guillemotleft/acyrillic /acyrillic/guillemotright /acyrillic/slash /acyrillic/backslash /acyrillic/asterisk /acyrillic/dagger /acyrillic/daggerdbl /acyrillic/trademark /acyrillic/at /acyrillic/registered /acyrillic/copyright
/icyrillic/period /icyrillic/comma /icyrillic/colon /icyrillic/semicolon /icyrillic/exclam /icyrillic/question /parenleft/icyrillic /icyrillic/parenright /bracketleft/icyrillic /icyrillic/bracketright /icyrillic/hyphen /icyrillic/bullet /quoteleft/icyrillic /icyrillic/quoteright /quotesinglbase/icyrillic /icyrillic/quoteleft /guillemotleft/icyrillic /icyrillic/guillemotright /icyrillic/slash /icyrillic/backslash /icyrillic/asterisk /icyrillic/dagger /icyrillic/daggerdbl /icyrillic/trademark /icyrillic/at /icyrillic/registered /icyrillic/copyright /dzhecyrillic/period /dzhecyrillic/comma /dzhecyrillic/colon /dzhecyrillic/semicolon /dzhecyrillic/exclam /dzhecyrillic/question /parenleft/dzhecyrillic /dzhecyrillic/parenright /bracketleft/dzhecyrillic /dzhecyrillic/bracketright /dzhecyrillic/hyphen /dzhecyrillic/bullet /quoteleft/dzhecyrillic /dzhecyrillic/quoteright /quotesinglbase/dzhecyrillic /dzhecyrillic/quoteleft /guillemotleft/dzhecyrillic /dzhecyrillic/guillemotright /dzhecyrillic/slash /dzhecyrillic/backslash /dzhecyrillic/asterisk /dzhecyrillic/dagger /dzhecyrillic/daggerdbl /dzhecyrillic/trademark /dzhecyrillic/at /dzhecyrillic/registered /dzhecyrillic/copyright /emcyrillic/period /emcyrillic/comma /emcyrillic/colon /emcyrillic/semicolon /emcyrillic/exclam /emcyrillic/question /parenleft/emcyrillic /emcyrillic/parenright /bracketleft/emcyrillic /emcyrillic/bracketright /emcyrillic/hyphen /emcyrillic/bullet /quoteleft/emcyrillic /emcyrillic/quoteright /quotesinglbase/emcyrillic /emcyrillic/quoteleft /guillemotleft/emcyrillic /emcyrillic/guillemotright /emcyrillic/slash /emcyrillic/backslash /emcyrillic/asterisk /emcyrillic/dagger /emcyrillic/daggerdbl /emcyrillic/trademark /emcyrillic/at /emcyrillic/registered /emcyrillic/copyright /encyrillic/period /encyrillic/comma /encyrillic/colon /encyrillic/semicolon /encyrillic/exclam /encyrillic/question /parenleft/encyrillic /encyrillic/parenright /bracketleft/encyrillic /encyrillic/bracketright /encyrillic/hyphen /encyrillic/bullet /quoteleft/encyrillic /encyrillic/quoteright /quotesinglbase/encyrillic /encyrillic/quoteleft /guillemotleft/encyrillic /encyrillic/guillemotright /encyrillic/slash /encyrillic/backslash /encyrillic/asterisk /encyrillic/dagger /encyrillic/daggerdbl /encyrillic/trademark /encyrillic/at /encyrillic/registered /encyrillic/copyright /pecyrillic/period /pecyrillic/comma /pecyrillic/colon /pecyrillic/semicolon /pecyrillic/exclam /pecyrillic/question /parenleft/pecyrillic /pecyrillic/parenright /bracketleft/pecyrillic /pecyrillic/bracketright /pecyrillic/hyphen /pecyrillic/bullet /quoteleft/pecyrillic /pecyrillic/quoteright /quotesinglbase/pecyrillic /pecyrillic/quoteleft /guillemotleft/pecyrillic /pecyrillic/guillemotright /pecyrillic/slash /pecyrillic/backslash /pecyrillic/asterisk /pecyrillic/dagger /pecyrillic/daggerdbl /pecyrillic/trademark /pecyrillic/at /pecyrillic/registered /pecyrillic/copyright /shacyrillic/period /shacyrillic/comma /shacyrillic/colon /shacyrillic/semicolon /shacyrillic/exclam /shacyrillic/question /parenleft/shacyrillic /shacyrillic/parenright /bracketleft/shacyrillic /shacyrillic/bracketright /shacyrillic/hyphen /shacyrillic/bullet /quoteleft/shacyrillic /shacyrillic/quoteright /quotesinglbase/shacyrillic /guillemotleft/shacyrillic /shacyrillic/guillemotright /shacyrillic/slash /shacyrillic/backslash /shacyrillic/asterisk /shacyrillic/dagger /shacyrillic/daggerdbl /shacyrillic/trademark /shacyrillic/at /shacyrillic/registered /shacyrillic/copyright /yericyrillic/period /yericyrillic/comma /yericyrillic/colon /yericyrillic/semicolon /yericyrillic/exclam /yericyrillic/question /parenleft/yericyrillic /yericyrillic/parenright /bracketleft/yericyrillic /yericyrillic/bracketright /yericyrillic/hyphen /yericyrillic/bullet /quoteleft/yericyrillic /yericyrillic/quoteright /quotesinglbase/yericyrillic /guillemotleft/yericyrillic /yericyrillic/guillemotright /yericyrillic/slash /yericyrillic/backslash /yericyrillic/asterisk /yericyrillic/dagger /yericyrillic/daggerdbl /yericyrillic/trademark /yericyrillic/at /yericyrillic/registered /yericyrillic/copyright""",

    'Kern Cyr-lc-diag': """/zhecyrillic/zhecyrillic /zhecyrillic/kacyrillic /zhecyrillic/ucyrillic /zhecyrillic/ustraightstrokecyrillic /zhecyrillic/khacyrillic /kacyrillic/kacyrillic /kacyrillic/ucyrillic /kacyrillic/ustraightstrokecyrillic /kacyrillic/khacyrillic /ucyrillic/ucyrillic /ucyrillic/ustraightstrokecyrillic /ucyrillic/khacyrillic /ustraightstrokecyrillic/ustraightstrokecyrillic /ustraightstrokecyrillic/khacyrillic /khacyrillic/khacyrillic
#rounds /zhecyrillic/becyrillic /zhecyrillic/iecyrillic /zhecyrillic/ocyrillic /zhecyrillic/ercyrillic /zhecyrillic/escyrillic /zhecyrillic/efcyrillic /zhecyrillic/iucyrillic /kacyrillic/becyrillic /kacyrillic/iecyrillic /kacyrillic/ocyrillic /kacyrillic/ercyrillic /kacyrillic/escyrillic /kacyrillic/efcyrillic /kacyrillic/iucyrillic /ucyrillic/becyrillic /ucyrillic/iecyrillic /ucyrillic/ocyrillic /ucyrillic/ercyrillic /ucyrillic/escyrillic /ucyrillic/efcyrillic /ucyrillic/iucyrillic /ustraightstrokecyrillic/becyrillic /ustraightstrokecyrillic/iecyrillic /ustraightstrokecyrillic/ocyrillic /ustraightstrokecyrillic/ercyrillic /ustraightstrokecyrillic/escyrillic /ustraightstrokecyrillic/efcyrillic /ustraightstrokecyrillic/iucyrillic /khacyrillic/becyrillic /khacyrillic/iecyrillic /khacyrillic/ocyrillic /khacyrillic/ercyrillic /khacyrillic/escyrillic /khacyrillic/efcyrillic /khacyrillic/iucyrillic
#round es /zhecyrillic/ecyrillic /zhecyrillic/ereversedcyrillic /kacyrillic/ecyrillic /kacyrillic/ereversedcyrillic /ucyrillic/ecyrillic /ucyrillic/ereversedcyrillic /ustraightstrokecyrillic/ecyrillic /ustraightstrokecyrillic/ereversedcyrillic /khacyrillic/ecyrillic /khacyrillic/ereversedcyrillic
#halfround_right /zhecyrillic/hardsigncyrillic /zhecyrillic/softsigncyrillic /zhecyrillic/njecyrillic /zhecyrillic/ljecyrillic /zhecyrillic/elcyrillic /kacyrillic/hardsigncyrillic /kacyrillic/softsigncyrillic /kacyrillic/njecyrillic /kacyrillic/ljecyrillic /kacyrillic/elcyrillic /ucyrillic/hardsigncyrillic /ucyrillic/softsigncyrillic /ucyrillic/njecyrillic /ucyrillic/ljecyrillic /ucyrillic/elcyrillic /ustraightstrokecyrillic/hardsigncyrillic /ustraightstrokecyrillic/softsigncyrillic /ustraightstrokecyrillic/njecyrillic /ustraightstrokecyrillic/ljecyrillic /ustraightstrokecyrillic/elcyrillic /khacyrillic/hardsigncyrillic /khacyrillic/softsigncyrillic /khacyrillic/njecyrillic /khacyrillic/ljecyrillic /khacyrillic/elcyrillic
#tail_right /zhecyrillic/decyrillic /zhecyrillic/tsecyrillic /zhecyrillic/chedescendercyrillic /zhecyrillic/shchacyrillic /kacyrillic/decyrillic /kacyrillic/tsecyrillic /kacyrillic/chedescendercyrillic /kacyrillic/shchacyrillic /ucyrillic/decyrillic /ucyrillic/tsecyrillic /ucyrillic/chedescendercyrillic /ucyrillic/shchacyrillic /ustraightstrokecyrillic/decyrillic /ustraightstrokecyrillic/tsecyrillic /ustraightstrokecyrillic/chedescendercyrillic /ustraightstrokecyrillic/shchacyrillic /khacyrillic/decyrillic /khacyrillic/tsecyrillic /khacyrillic/chedescendercyrillic /khacyrillic/shchacyrillic
#crossbars /zhecyrillic/gecyrillic /zhecyrillic/tecyrillic /zhecyrillic/gheupturncyrillic /kacyrillic/gecyrillic /kacyrillic/tecyrillic /kacyrillic/gheupturncyrillic /ucyrillic/gecyrillic /ucyrillic/tecyrillic /ucyrillic/gheupturncyrillic /ustraightstrokecyrillic/gecyrillic /ustraightstrokecyrillic/tecyrillic /ustraightstrokecyrillic/gheupturncyrillic /khacyrillic/gecyrillic /khacyrillic/tecyrillic /khacyrillic/gheupturncyrillic
#B/like /zhecyrillic/vecyrillic /zhecyrillic/zecyrillic /zhecyrillic/iacyrillic /kacyrillic/vecyrillic /kacyrillic/zecyrillic /kacyrillic/iacyrillic /ucyrillic/vecyrillic /ucyrillic/zecyrillic /ucyrillic/iacyrillic /ustraightstrokecyrillic/vecyrillic /ustraightstrokecyrillic/zecyrillic /ustraightstrokecyrillic/iacyrillic /khacyrillic/vecyrillic /khacyrillic/zecyrillic /khacyrillic/iacyrillic
#assymetric /zhecyrillic/checyrillic /kacyrillic/checyrillic /ucyrillic/checyrillic /ustraightstrokecyrillic/checyrillic /khacyrillic/checyrillic
#s /zhecyrillic/dzecyrillic /zhecyrillic/acyrillic /kacyrillic/dzecyrillic /kacyrillic/acyrillic /ucyrillic/dzecyrillic /ucyrillic/acyrillic /ustraightstrokecyrillic/dzecyrillic /ustraightstrokecyrillic/acyrillic /khacyrillic/dzecyrillic /khacyrillic/acyrillic""",
    'Kern Cyr-lc-rounds': """#rounds /becyrillic/becyrillic /becyrillic/iecyrillic /becyrillic/ocyrillic /becyrillic/ercyrillic /becyrillic/escyrillic /becyrillic/efcyrillic /becyrillic/iucyrillic /iecyrillic/iecyrillic /iecyrillic/ocyrillic /iecyrillic/ercyrillic /iecyrillic/escyrillic /iecyrillic/efcyrillic /iecyrillic/iucyrillic /ocyrillic/ocyrillic /ocyrillic/ercyrillic /ocyrillic/escyrillic /ocyrillic/efcyrillic /ocyrillic/iucyrillic /ercyrillic/ercyrillic /ercyrillic/escyrillic /ercyrillic/efcyrillic /ercyrillic/iucyrillic /escyrillic/escyrillic /escyrillic/efcyrillic /escyrillic/iucyrillic /efcyrillic/efcyrillic /efcyrillic/iucyrillic /iucyrillic/iucyrillic
#round es /becyrillic/ecyrillic /becyrillic/ereversedcyrillic /iecyrillic/ecyrillic /iecyrillic/ereversedcyrillic /ocyrillic/ecyrillic /ocyrillic/ereversedcyrillic /ercyrillic/ecyrillic /ercyrillic/ereversedcyrillic /escyrillic/ecyrillic /escyrillic/ereversedcyrillic /efcyrillic/ecyrillic /efcyrillic/ereversedcyrillic /iucyrillic/ecyrillic /iucyrillic/ereversedcyrillic
#halfround_right /becyrillic/hardsigncyrillic /becyrillic/softsigncyrillic /becyrillic/njecyrillic /becyrillic/ljecyrillic /becyrillic/elcyrillic /iecyrillic/hardsigncyrillic /iecyrillic/softsigncyrillic /iecyrillic/njecyrillic /iecyrillic/ljecyrillic /iecyrillic/elcyrillic /ocyrillic/hardsigncyrillic /ocyrillic/softsigncyrillic /ocyrillic/njecyrillic /ocyrillic/ljecyrillic /ocyrillic/elcyrillic /ercyrillic/hardsigncyrillic /ercyrillic/softsigncyrillic /ercyrillic/njecyrillic /ercyrillic/ljecyrillic /ercyrillic/elcyrillic /escyrillic/hardsigncyrillic /escyrillic/softsigncyrillic /escyrillic/njecyrillic /escyrillic/ljecyrillic /escyrillic/elcyrillic /efcyrillic/hardsigncyrillic /efcyrillic/softsigncyrillic /efcyrillic/njecyrillic /efcyrillic/ljecyrillic /efcyrillic/elcyrillic /iucyrillic/hardsigncyrillic /iucyrillic/softsigncyrillic /iucyrillic/njecyrillic /iucyrillic/ljecyrillic /iucyrillic/elcyrillic
#tail_right /becyrillic/decyrillic /becyrillic/tsecyrillic /becyrillic/chedescendercyrillic /becyrillic/shchacyrillic /iecyrillic/decyrillic /iecyrillic/tsecyrillic /iecyrillic/chedescendercyrillic /iecyrillic/shchacyrillic /ocyrillic/decyrillic /ocyrillic/tsecyrillic /ocyrillic/chedescendercyrillic /ocyrillic/shchacyrillic /ercyrillic/decyrillic /ercyrillic/tsecyrillic /ercyrillic/chedescendercyrillic /ercyrillic/shchacyrillic /escyrillic/decyrillic /escyrillic/tsecyrillic /escyrillic/chedescendercyrillic /escyrillic/shchacyrillic /efcyrillic/decyrillic /efcyrillic/tsecyrillic /efcyrillic/chedescendercyrillic /efcyrillic/shchacyrillic /iucyrillic/decyrillic /iucyrillic/tsecyrillic /iucyrillic/chedescendercyrillic /iucyrillic/shchacyrillic
#crossbars /becyrillic/gecyrillic /becyrillic/tecyrillic /becyrillic/gheupturncyrillic /iecyrillic/gecyrillic /iecyrillic/tecyrillic /iecyrillic/gheupturncyrillic /ocyrillic/gecyrillic /ocyrillic/tecyrillic /ocyrillic/gheupturncyrillic /ercyrillic/gecyrillic /ercyrillic/tecyrillic /ercyrillic/gheupturncyrillic /escyrillic/gecyrillic /escyrillic/tecyrillic /escyrillic/gheupturncyrillic /efcyrillic/gecyrillic /efcyrillic/tecyrillic /efcyrillic/gheupturncyrillic /iucyrillic/gecyrillic /iucyrillic/tecyrillic /iucyrillic/gheupturncyrillic
#B like /becyrillic/vecyrillic /becyrillic/zecyrillic /becyrillic/iacyrillic /iecyrillic/vecyrillic /iecyrillic/zecyrillic /iecyrillic/iacyrillic /ocyrillic/vecyrillic /ocyrillic/zecyrillic /ocyrillic/iacyrillic /ercyrillic/vecyrillic /ercyrillic/zecyrillic /ercyrillic/iacyrillic /escyrillic/vecyrillic /escyrillic/zecyrillic /escyrillic/iacyrillic /efcyrillic/vecyrillic /efcyrillic/zecyrillic /efcyrillic/iacyrillic /iucyrillic/vecyrillic /iucyrillic/zecyrillic /iucyrillic/iacyrillic
#assymetric /becyrillic/checyrillic /iecyrillic/checyrillic /ocyrillic/checyrillic /ercyrillic/checyrillic /escyrillic/checyrillic /efcyrillic/checyrillic /iucyrillic/checyrillic
#s /becyrillic/dzecyrillic /becyrillic/acyrillic /iecyrillic/dzecyrillic /iecyrillic/acyrillic /ocyrillic/dzecyrillic /ocyrillic/acyrillic /ercyrillic/dzecyrillic /ercyrillic/acyrillic /escyrillic/dzecyrillic /escyrillic/acyrillic /efcyrillic/dzecyrillic /efcyrillic/acyrillic /iucyrillic/dzecyrillic /iucyrillic/acyrillic""",
    'Kern Cyr-lc-round es': """#round es /ecyrillic/ecyrillic /ecyrillic/ereversedcyrillic /ereversedcyrillic/ereversedcyrillic
#round es to halfround_right /ecyrillic/hardsigncyrillic /ecyrillic/softsigncyrillic /ecyrillic/njecyrillic /ecyrillic/ljecyrillic /ecyrillic/elcyrillic /ereversedcyrillic/hardsigncyrillic /ereversedcyrillic/softsigncyrillic /ereversedcyrillic/njecyrillic /ereversedcyrillic/ljecyrillic /ereversedcyrillic/elcyrillic
#round es to tail_right /ecyrillic/decyrillic /ecyrillic/tsecyrillic /ecyrillic/chedescendercyrillic /ecyrillic/shchacyrillic /ereversedcyrillic/decyrillic /ereversedcyrillic/tsecyrillic /ereversedcyrillic/chedescendercyrillic /ereversedcyrillic/shchacyrillic
#round es to crossbars /ecyrillic/gecyrillic /ecyrillic/tecyrillic /ecyrillic/gheupturncyrillic /ereversedcyrillic/gecyrillic /ereversedcyrillic/tecyrillic /ereversedcyrillic/gheupturncyrillic
#round es to B/like /ecyrillic/vecyrillic /ecyrillic/zecyrillic /ecyrillic/iacyrillic /ereversedcyrillic/vecyrillic /ereversedcyrillic/zecyrillic /ereversedcyrillic/iacyrillic
#round es to assymetric /ecyrillic/checyrillic /ereversedcyrillic/checyrillic
#round es to s /ecyrillic/dzecyrillic /ecyrillic/acyrillic /ereversedcyrillic/dzecyrillic /ereversedcyrillic/acyrillic
#halfround_right to halfround_right /hardsigncyrillic/hardsigncyrillic /hardsigncyrillic/softsigncyrillic /hardsigncyrillic/njecyrillic /hardsigncyrillic/ljecyrillic /hardsigncyrillic/elcyrillic /softsigncyrillic/softsigncyrillic /softsigncyrillic/njecyrillic /softsigncyrillic/ljecyrillic /softsigncyrillic/elcyrillic /njecyrillic/njecyrillic /njecyrillic/ljecyrillic /njecyrillic/elcyrillic /ljecyrillic/ljecyrillic /ljecyrillic/elcyrillic /elcyrillic/elcyrillic
#halfround_right to tail_right /hardsigncyrillic/decyrillic /hardsigncyrillic/tsecyrillic /hardsigncyrillic/chedescendercyrillic /hardsigncyrillic/shchacyrillic /softsigncyrillic/decyrillic /softsigncyrillic/tsecyrillic /softsigncyrillic/chedescendercyrillic /softsigncyrillic/shchacyrillic /njecyrillic/decyrillic /njecyrillic/tsecyrillic /njecyrillic/chedescendercyrillic /njecyrillic/shchacyrillic /ljecyrillic/decyrillic /ljecyrillic/tsecyrillic /ljecyrillic/chedescendercyrillic /ljecyrillic/shchacyrillic /elcyrillic/decyrillic /elcyrillic/tsecyrillic /elcyrillic/chedescendercyrillic /elcyrillic/shchacyrillic
#halfround_right to crossbars /hardsigncyrillic/gecyrillic /hardsigncyrillic/tecyrillic /hardsigncyrillic/gheupturncyrillic /softsigncyrillic/gecyrillic /softsigncyrillic/tecyrillic /softsigncyrillic/gheupturncyrillic /njecyrillic/gecyrillic /njecyrillic/tecyrillic /njecyrillic/gheupturncyrillic /ljecyrillic/gecyrillic /ljecyrillic/tecyrillic /ljecyrillic/gheupturncyrillic /elcyrillic/gecyrillic /elcyrillic/tecyrillic /elcyrillic/gheupturncyrillic
#halfround_right to B/like /hardsigncyrillic/vecyrillic /hardsigncyrillic/zecyrillic /hardsigncyrillic/iacyrillic /softsigncyrillic/vecyrillic /softsigncyrillic/zecyrillic /softsigncyrillic/iacyrillic /njecyrillic/vecyrillic /njecyrillic/zecyrillic /njecyrillic/iacyrillic /ljecyrillic/vecyrillic /ljecyrillic/zecyrillic /ljecyrillic/iacyrillic /elcyrillic/vecyrillic /elcyrillic/zecyrillic /elcyrillic/iacyrillic
#halfround_right to assymetric /hardsigncyrillic/checyrillic /softsigncyrillic/checyrillic /njecyrillic/checyrillic /ljecyrillic/checyrillic /elcyrillic/checyrillic
#halfround_right to s /hardsigncyrillic/dzecyrillic /hardsigncyrillic/acyrillic /softsigncyrillic/dzecyrillic /softsigncyrillic/acyrillic /njecyrillic/dzecyrillic /njecyrillic/acyrillic /ljecyrillic/dzecyrillic /ljecyrillic/acyrillic /elcyrillic/dzecyrillic /elcyrillic/acyrillic
#crossbars to crossbars /gecyrillic/gecyrillic /gecyrillic/tecyrillic /gecyrillic/gheupturncyrillic /tecyrillic/tecyrillic /tecyrillic/gheupturncyrillic /gheupturncyrillic/gheupturncyrillic
#crossbars to B/like /gecyrillic/vecyrillic /gecyrillic/zecyrillic /gecyrillic/iacyrillic /tecyrillic/vecyrillic /tecyrillic/zecyrillic /tecyrillic/iacyrillic /gheupturncyrillic/vecyrillic /gheupturncyrillic/zecyrillic /gheupturncyrillic/iacyrillic
#crossbars to assymetric /gecyrillic/checyrillic /tecyrillic/checyrillic /gheupturncyrillic/checyrillic
#crossbars to s /gecyrillic/dzecyrillic /gecyrillic/acyrillic /tecyrillic/dzecyrillic /tecyrillic/acyrillic /gheupturncyrillic/dzecyrillic /gheupturncyrillic/acyrillic
#B/like to B/like /vecyrillic/vecyrillic /vecyrillic/zecyrillic /vecyrillic/iacyrillic /zecyrillic/zecyrillic /zecyrillic/iacyrillic /iacyrillic/iacyrillic
#B/like to assymetric /vecyrillic/checyrillic /zecyrillic/checyrillic /iacyrillic/checyrillic
#B/like to s /vecyrillic/dzecyrillic /vecyrillic/acyrillic /zecyrillic/dzecyrillic /zecyrillic/acyrillic /iacyrillic/dzecyrillic /iacyrillic/acyrillic
#assymetric to assymetric /checyrillic/checyrillic
#assymetric to s /checyrillic/dzecyrillic /checyrillic/acyrillic
#s to s /dzecyrillic/dzecyrillic /dzecyrillic/acyrillic /acyrillic/acyrillic
#tail_right to tail_right /decyrillic/decyrillic /decyrillic/tsecyrillic /decyrillic/chedescendercyrillic /decyrillic/shchacyrillic /tsecyrillic/tsecyrillic /tsecyrillic/chedescendercyrillic /tsecyrillic/shchacyrillic /chedescendercyrillic/chedescendercyrillic /chedescendercyrillic/shchacyrillic /shchacyrillic/shchacyrillic
#tail_right to crossbars /decyrillic/gecyrillic /decyrillic/tecyrillic /decyrillic/gheupturncyrillic /tsecyrillic/gecyrillic /tsecyrillic/tecyrillic /tsecyrillic/gheupturncyrillic /chedescendercyrillic/gecyrillic /chedescendercyrillic/tecyrillic /chedescendercyrillic/gheupturncyrillic /shchacyrillic/gecyrillic /shchacyrillic/tecyrillic /shchacyrillic/gheupturncyrillic
#tail_right to B/like /decyrillic/vecyrillic /decyrillic/zecyrillic /decyrillic/iacyrillic /tsecyrillic/vecyrillic /tsecyrillic/zecyrillic /tsecyrillic/iacyrillic /chedescendercyrillic/vecyrillic /chedescendercyrillic/zecyrillic /chedescendercyrillic/iacyrillic /shchacyrillic/vecyrillic /shchacyrillic/zecyrillic /shchacyrillic/iacyrillic
#tail_right to assymetric /decyrillic/checyrillic /tsecyrillic/checyrillic /chedescendercyrillic/checyrillic /shchacyrillic/checyrillic
#tail_right to s /decyrillic/dzecyrillic /decyrillic/acyrillic /tsecyrillic/dzecyrillic /tsecyrillic/acyrillic /chedescendercyrillic/dzecyrillic /chedescendercyrillic/acyrillic /shchacyrillic/dzecyrillic /shchacyrillic/acyrillic
#diagonals to straights /zhecyrillic/icyrillic /zhecyrillic/dzhecyrillic /zhecyrillic/emcyrillic /zhecyrillic/encyrillic /zhecyrillic/pecyrillic /zhecyrillic/shacyrillic /zhecyrillic/yericyrillic /kacyrillic/icyrillic /kacyrillic/dzhecyrillic /kacyrillic/emcyrillic /kacyrillic/encyrillic /kacyrillic/pecyrillic /kacyrillic/shacyrillic /kacyrillic/yericyrillic /ucyrillic/icyrillic /ucyrillic/dzhecyrillic /ucyrillic/emcyrillic /ucyrillic/encyrillic /ucyrillic/pecyrillic /ucyrillic/shacyrillic /ucyrillic/yericyrillic /ustraightstrokecyrillic/icyrillic /ustraightstrokecyrillic/dzhecyrillic /ustraightstrokecyrillic/emcyrillic /ustraightstrokecyrillic/encyrillic /ustraightstrokecyrillic/pecyrillic /ustraightstrokecyrillic/shacyrillic /ustraightstrokecyrillic/yericyrillic /khacyrillic/icyrillic /khacyrillic/dzhecyrillic /khacyrillic/emcyrillic /khacyrillic/encyrillic /khacyrillic/pecyrillic /khacyrillic/shacyrillic /khacyrillic/yericyrillic
#rounds to straights /becyrillic/icyrillic /becyrillic/dzhecyrillic /becyrillic/emcyrillic /becyrillic/encyrillic /becyrillic/pecyrillic /becyrillic/shacyrillic /becyrillic/yericyrillic /iecyrillic/icyrillic /iecyrillic/dzhecyrillic /iecyrillic/emcyrillic /iecyrillic/encyrillic /iecyrillic/pecyrillic /iecyrillic/shacyrillic /iecyrillic/yericyrillic /ocyrillic/icyrillic /ocyrillic/dzhecyrillic /ocyrillic/emcyrillic /ocyrillic/encyrillic /ocyrillic/pecyrillic /ocyrillic/shacyrillic /ocyrillic/yericyrillic /ercyrillic/icyrillic /ercyrillic/dzhecyrillic /ercyrillic/emcyrillic /ercyrillic/encyrillic /ercyrillic/pecyrillic /ercyrillic/shacyrillic /ercyrillic/yericyrillic /escyrillic/icyrillic /escyrillic/dzhecyrillic /escyrillic/emcyrillic /escyrillic/encyrillic /escyrillic/pecyrillic /escyrillic/shacyrillic /escyrillic/yericyrillic /efcyrillic/icyrillic /efcyrillic/dzhecyrillic /efcyrillic/emcyrillic /efcyrillic/encyrillic /efcyrillic/pecyrillic /efcyrillic/shacyrillic /efcyrillic/yericyrillic /iucyrillic/icyrillic /iucyrillic/dzhecyrillic /iucyrillic/emcyrillic /iucyrillic/encyrillic /iucyrillic/pecyrillic /iucyrillic/shacyrillic /iucyrillic/yericyrillic
#round/es to straights /ecyrillic/icyrillic /ecyrillic/dzhecyrillic /ecyrillic/emcyrillic /ecyrillic/encyrillic /ecyrillic/pecyrillic /ecyrillic/shacyrillic /ecyrillic/yericyrillic /ereversedcyrillic/icyrillic /ereversedcyrillic/dzhecyrillic /ereversedcyrillic/emcyrillic /ereversedcyrillic/encyrillic /ereversedcyrillic/pecyrillic /ereversedcyrillic/shacyrillic /ereversedcyrillic/yericyrillic
#halfround_right to straights /hardsigncyrillic/icyrillic /hardsigncyrillic/dzhecyrillic /hardsigncyrillic/emcyrillic /hardsigncyrillic/encyrillic /hardsigncyrillic/pecyrillic /hardsigncyrillic/shacyrillic /hardsigncyrillic/yericyrillic /softsigncyrillic/icyrillic /softsigncyrillic/dzhecyrillic /softsigncyrillic/emcyrillic /softsigncyrillic/encyrillic /softsigncyrillic/pecyrillic /softsigncyrillic/shacyrillic /softsigncyrillic/yericyrillic /njecyrillic/icyrillic /njecyrillic/dzhecyrillic /njecyrillic/emcyrillic /njecyrillic/encyrillic /njecyrillic/pecyrillic /njecyrillic/shacyrillic /njecyrillic/yericyrillic /ljecyrillic/icyrillic /ljecyrillic/dzhecyrillic /ljecyrillic/emcyrillic /ljecyrillic/encyrillic /ljecyrillic/pecyrillic /ljecyrillic/shacyrillic /ljecyrillic/yericyrillic /elcyrillic/icyrillic /elcyrillic/dzhecyrillic /elcyrillic/emcyrillic /elcyrillic/encyrillic /elcyrillic/pecyrillic /elcyrillic/shacyrillic /elcyrillic/yericyrillic
#tail_right to straights /decyrillic/icyrillic /decyrillic/dzhecyrillic /decyrillic/emcyrillic /decyrillic/encyrillic /decyrillic/pecyrillic /decyrillic/shacyrillic /decyrillic/yericyrillic /tsecyrillic/icyrillic /tsecyrillic/dzhecyrillic /tsecyrillic/emcyrillic /tsecyrillic/encyrillic /tsecyrillic/pecyrillic /tsecyrillic/shacyrillic /tsecyrillic/yericyrillic /chedescendercyrillic/icyrillic /chedescendercyrillic/dzhecyrillic /chedescendercyrillic/emcyrillic /chedescendercyrillic/encyrillic /chedescendercyrillic/pecyrillic /chedescendercyrillic/shacyrillic /chedescendercyrillic/yericyrillic /shchacyrillic/icyrillic /shchacyrillic/dzhecyrillic /shchacyrillic/emcyrillic /shchacyrillic/encyrillic /shchacyrillic/pecyrillic /shchacyrillic/shacyrillic /shchacyrillic/yericyrillic
#crossbars to straights /gecyrillic/icyrillic /gecyrillic/dzhecyrillic /gecyrillic/emcyrillic /gecyrillic/encyrillic /gecyrillic/pecyrillic /gecyrillic/shacyrillic /gecyrillic/yericyrillic /tecyrillic/icyrillic /tecyrillic/dzhecyrillic /tecyrillic/emcyrillic /tecyrillic/encyrillic /tecyrillic/pecyrillic /tecyrillic/shacyrillic /tecyrillic/yericyrillic /gheupturncyrillic/icyrillic /gheupturncyrillic/dzhecyrillic /gheupturncyrillic/emcyrillic /gheupturncyrillic/encyrillic /gheupturncyrillic/pecyrillic /gheupturncyrillic/shacyrillic /gheupturncyrillic/yericyrillic
#B/like to straights /vecyrillic/icyrillic /vecyrillic/dzhecyrillic /vecyrillic/emcyrillic /vecyrillic/encyrillic /vecyrillic/pecyrillic /vecyrillic/shacyrillic /vecyrillic/yericyrillic /zecyrillic/icyrillic /zecyrillic/dzhecyrillic /zecyrillic/emcyrillic /zecyrillic/encyrillic /zecyrillic/pecyrillic /zecyrillic/shacyrillic /zecyrillic/yericyrillic /iacyrillic/icyrillic /iacyrillic/dzhecyrillic /iacyrillic/emcyrillic /iacyrillic/encyrillic /iacyrillic/pecyrillic /iacyrillic/shacyrillic /iacyrillic/yericyrillic
#assymetric to straights /checyrillic/icyrillic /checyrillic/dzhecyrillic /checyrillic/emcyrillic /checyrillic/encyrillic /checyrillic/pecyrillic /checyrillic/shacyrillic /checyrillic/yericyrillic
#s to straights /dzecyrillic/icyrillic /dzecyrillic/dzhecyrillic /dzecyrillic/emcyrillic /dzecyrillic/encyrillic /dzecyrillic/pecyrillic /dzecyrillic/shacyrillic /dzecyrillic/yericyrillic /acyrillic/icyrillic /acyrillic/dzhecyrillic /acyrillic/emcyrillic /acyrillic/encyrillic /acyrillic/pecyrillic /acyrillic/shacyrillic /acyrillic/yericyrillic
#straights to straights /icyrillic/icyrillic /icyrillic/dzhecyrillic /icyrillic/emcyrillic /icyrillic/encyrillic /icyrillic/pecyrillic /icyrillic/shacyrillic /icyrillic/yericyrillic /dzhecyrillic/dzhecyrillic /dzhecyrillic/emcyrillic /dzhecyrillic/encyrillic /dzhecyrillic/pecyrillic /dzhecyrillic/shacyrillic /dzhecyrillic/yericyrillic /emcyrillic/emcyrillic /emcyrillic/encyrillic /emcyrillic/pecyrillic /emcyrillic/shacyrillic /emcyrillic/yericyrillic /encyrillic/encyrillic /encyrillic/pecyrillic /encyrillic/shacyrillic /encyrillic/yericyrillic /pecyrillic/pecyrillic /pecyrillic/shacyrillic /pecyrillic/yericyrillic /shacyrillic/shacyrillic /shacyrillic/yericyrillic /yericyrillic/yericyrillic /""",

}

BASEGLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 '
LOREM_IPSUM_TEXT = (
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque eu elit placerat, tristique arcu sed, gravida nunc. """+\
        """Nulla sollicitudin vulputate ex, sit amet ullamcorper neque pellentesque at. Maecenas ut lectus lobortis, consequat lectus ut, imperdiet sapien. """,
    """Sed porta scelerisque massa et iaculis. Donec in ante eget lectus pulvinar euismod. Suspendisse potenti. Nam viverra sed sapien sit amet iaculis. """+\
        """In vestibulum purus nec dapibus tempor. Curabitur porta feugiat ex in ultrices. Sed ultricies lobortis tristique. """,
    """Sed eu arcu venenatis, sodales justo congue, faucibus leo. Aliquam volutpat gravida nulla, at elementum est condimentum non. """,
    """Aenean ac luctus elit, sed pretium lorem. Sed cursus pharetra finibus. Etiam vitae tortor vitae sem faucibus condimentum.  """+\
        """Ut et varius massa, eget gravida eros. Phasellus sagittis lacinia augue a porta. Quisque vitae lacinia ipsum. Morbi tincidunt orci nec risus vulputate aliquam. """,
    """Curabitur eget enim porttitor, dapibus nunc non, blandit dolor. Nam porta nunc nec eros elementum, id ornare erat elementum. """+\
        """Quisque sit amet tincidunt lorem, condimentum lobortis magna. Sed id quam vitae sapien consectetur dapibus. """,
    """Praesent dictum et risus vitae tincidunt. Fusce id eleifend dolor, vitae convallis nunc. Nunc euismod dui ante. Sed id faucibus libero. """+\
        """Sed rhoncus tortor eget porta molestie. Vestibulum libero massa, sagittis sed justo vitae, vulputate molestie felis. """,
    """Fusce finibus, sem et rutrum gravida, ipsum dolor rhoncus ex, pulvinar feugiat nisi ante at ex. Etiam varius consectetur risus sed cursus. """+\
        """Donec aliquet augue nulla, quis imperdiet augue facilisis vitae. Donec nec viverra diam, ac vulputate turpis. Class aptent taciti sociosqu ad litora. """,
    """Torquent per conubia nostra, per inceptos himenaeos. Sed varius elementum erat, sed viverra neque euismod eget. Aenean maximus magna a luctus euismod. Vivamus ultrices suscipit pellentesque. """+\
        """Praesent fringilla arcu sed arcu hendrerit sagittis eu sed velit. Mauris sagittis lorem nec eros placerat volutpat. """,
    """Praesent purus libero, tempor et hendrerit at, venenatis vel odio. Quisque vel ultricies felis. Aliquam at facilisis velit, in lobortis neque. """+\
        """Nullam ultricies non ipsum et gravida. Vestibulum at ex justo. Aenean efficitur, odio ut tempor mollis, est magna suscipit sem, ut condimentum ipsum lectus sit amet enim. """,
    """Donec vitae eros non eros semper ultricies eget sit amet ipsum. Quisque et tempor nibh. Aenean sed magna urna. Sed eget lectus velit. Ut ornare non erat vel facilisis. """+\
        """Vivamus congue vestibulum blandit. Proin a ultrices metus. Pellentesque sit amet mauris efficitur, porttitor tellus eget, auctor dui. """,
    """Curabitur dapibus lectus vestibulum nulla aliquet, id sodales orci efficitur. Aliquam ac felis fringilla, faucibus dui a, facilisis urna. """+\
        """Duis tempor ornare mauris a malesuada."""
)
LOREM_IPSUM_PAGE = '/ '.join(LOREM_IPSUM_TEXT)

QUICK_BROWN_FOX_TEXT = "A Quick Brown Fox Jumps Over The Lazy Dog 0123456789"

DUTCH_TEXT = (
    """“Met gepaste trots houdt de ontwerper Het Karton met Het Idee nog even afgedekt. Een goed idee heeft eerst toelichting nodig, want als je het meteen bij een opdrachtgever op tafel gooit, dan snapt die er niks van. Zoals bij elke bevalling is het belangrijk dat deze goed wordt ingeleid. """,
    """De ontwerper, die ook ruime les-ervaring heeft met het in beweging krijgen van ongeïnteresseerde groepen, houdt een betoog over de importantie van Het Idee. Over maatschappelijk relevantie. Over engagement. Over het belang van Het Idee op de iPad. Over hoe origineel dit Idee is, bedacht door een ingehuurde Kunstenaar. En over het feit dat alle onduidelijkheid bij voldoende inzicht uit zichzelf verdwijnt. """,
    """De ontwerper weet de spanning tot het uiterste op te voeren. Het Idee, nu nog onzichtbaar, zal aan alle verwachtingen voldoen. En meer dan dat. Wat nu nog rest is de onthulling zelf. Het moment suprême is daar…” """,
    """Wat de ontwerper laat zien? We zullen het niet weten. Deze scène stopt abrupt en laat de lezer met frustratie achter. We kunnen alleen vermoeden waarom het verhaal een open einde heeft. Het is een conceptuele beslissing van de auteur, boven elke kritiek verheven, want een kunstenaar heeft altijd gelijk. Zelfs als dat niet zo is. """,
    """Maar goed, stel even dat we proberen om het verhaal zelf af te maken. Na de uitgebreide inleiding zou de ontwerper kunnen concluderen dat van alle denkbare logo namen, het woord “Concept” alles verklaart. Over de visie van de opdrachtgever en over het innovatieve karakter van alle toekomstige ontwikkelingen. """,
    """Het enige nadeel van deze woordkeuze is dat het zoeken in Google meer dan 800.000.000 hits oplevert, maar daar heeft de ontwerper een conceptuele oplossing voor. Na onderzoek van wel 5 minuten is duidelijk dat verdubbeling van letters een steeds unieker resultaat oplevert. Dus hoeveel zijn er nodig? “Cooncept” is maar 16.600 hits en pas bij “Cooooooooooooncept” is het aantal gevonden pagina’s – medio december 2012 – tot nul gereduceerd. Een uniek ontwerp dus. Overigens heeft de naam Google minstens 12 o’s nodig om uniek te zijn. De rest is in gebruik door meelifters. """,
    """Het “Concept” is een buitengewoon belangrijk en onmisbaar onderdeel van het ontwerpproces. Ontwerpen zonder concept is als reizen zonder droom. “Concept” is hot. """,
    """Maar “Concept” is te hot. Zoeken op “concept+ontwerpen” levert wel 745.000 – uitsluitend Nederlandse – resultaten. Het “Concept” is de Haarlemmer olie voor ontwerpers, je kunt het overal voor gebruiken. Kritiek op een ontwerpbeslissing is eenvoudig te pareren met “Het is nog in concept”. En als het ontwerp in praktijk niet blijkt te werken volstaat het verweer dat het “Conceptueel toch erg goed in elkaar zit”. """,
    """Concept-ontwerpers kunnen beweren dat dit geen goed beeld geeft van wat “Conceptueel denken” precies is. Maar die bewering zelf is het bewijs van de stelling. “Concept” is per definitie ongrijpbaar, want het woord beschrijft zichzelf. Van Dale denkt er ook zo over: “Conceptuele kunst is een richting in de kunst volgens welke de keuze van de kunstenaar van een object dit reeds tot kunst kan maken”. Kan niet missen dus, altijd goed. Overigens zou ik niet weten hoe niet-conceptuele kunst er uitziet, maar dat kan aan mij liggen. Ik ben per slot ontwerper, geen kunstenaar. """,
    """“Concept” is misschien veel beter te definiëren als “datgene wat je maakt, voordat je het ergens over de schutting gooit”. Verdiepen is niet nodig. Ultieme ontwerpers-luiheid dus. """,
    """Je moet ontwerpstudenten – een heersend idee op academies – vooral niet belasten met hoe en waarom vragen, want dan haken ze af. En dat kost tegenwoordig veel geld. Toetsen op conceptuele resultaten is veel veiliger, niet aan te vechten en makkelijk aan te passen als te veel studenten het niet lijken halen. Maar is het op termijn wenselijk? """,
    """Misschien is het een idee als de ideeën-hebbers, de brain-stormers en de concept-vormgevers gewoon eens aan het werk gaan. Mocht je het daar niet mee eens zijn: dit verhaal is nog maar een concept."""
)
DUTCH_TEXT_PAGE = '/ '.join(DUTCH_TEXT)

SURNAMES = (
    u"McAdams McBain McClure McDermott McElhenny McFadden MacGyver McHale McIver McJunkins McKnabb McLure McMurray "+\
    u"McNight McOwer McPeter McQuaid McRoberts McStoots McTighe McUmber McVittie McWilliam McZeal DaCosta DaFonesca "+\
    u"DaMotta DaSilva DeAngelo DeBois DeCicco DeDoming DeEspinosa DeFries DeGroot DeHart DeIsaac DeJesu DeKorte DeLuna "+\
    u"DeMena DeNevers DeOlcotes DePalma DeQuerton DeRevere DeStefano DeTurk DeUmbria DeVito DeWitt DeYoe DeZinnia ",\
    u"DiAgostino DiBenedetto DiCesare DiDomenico DiGiaimo DiLemme DiMarco DiNunzio DiRusso DiStefano DuBois DuFrane ",\
    u"DuGuher DuPille DuToit",
)

# Accents need the _anchor name, e.g. Agrave had "top" anchor and grave has "_top" anchor at the bottom.
# Define the general anchor position that this accents needs to be attached to.
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

TN_CONTROLS = ('D','H','O','n','o','p','zero','one','period','comma','emdash','slash','plus')
TN_LC = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
TN_UC = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
TN_SC = []
for c in TN_UC:
    TN_SC.append(c+'.sc')

TN_FIGURES = ('zero','one','two','three','four','five','six','seven','eight','nine')
TN_PRIMARY = TN_UC + TN_LC + TN_FIGURES + ('parenleft','bracketleft','braceleft','guillemotleft','guilsinglleft',
    'exclam','question','quotesingle', 'quotedbl','quoteright','quotedblright','underscore','hyphen','emdash','endash',
    'colon','period','comma', 'semicolon','numbersign','percent','ampersand','asterisk','at')

TN_SECONDARY_LC = ('lslash','mu1', 'germandbls','ae','eth','oslash','oe','thorn','dotlessi')
TN_SECONDARY_UC = ('AE','Thorn','Eth','Oslash','OE','Lslash')
TN_SECONDARY_SC = []
for c in TN_SECONDARY_UC:
    TN_SECONDARY_SC.append(c+'.sc')

TN_SECONDARY_LIGATURES = ("f_i", "f_l", "f_f", "f_f_i", "f_f_l", "f_j", "f_t", "f_f_j", "f_f_t", "f_b",
    "f_f_b", "f_h", "f_f_h", "f_k", "f_f_k")
TN_CURRENCY = ('dollar','cent','sterling','Euro','florin','currency',
    'yen','brokenbar','product','Omega','summation','partialdiff','increment','pi','radical','fraction','slash','integral',
    'plus','minus','less','lessequal','equal','asciitilde','logicalnot','plusminus','multiply','divide','infinity',
    'asciicircum','bar','brokenbar','dagger','daggerdbl','section','paragraph','quotesinglbase','quotedblbase',
    'ellipsis','bullet','bullet','Schwa','schwa','armeniandram','afghani','rupeemarkbengali','rupeesignbengali',
    'gujaratirupee','tamilrupee','bahtthai','khmer','ecu','colonsign','cruzeiro','franc','lira','mill','naira','peseta',
    'rupee','won','sheqel','dong','kip','tugrik','dragma','germanpenny','peso','guarani','austral','hryvnia','cedi',
    'livretournois','spesmilo','indianrupee','turkishlira','nordicmark','manat','ruble','numero','trademark','scriptm',
    'rialarabic')
TN_SECONDARY = TN_SECONDARY_UC + TN_SECONDARY_LC + TN_SECONDARY_LIGATURES + TN_CURRENCY

TN_SCALARPOLATES = ('ordfeminine','ordmasculine','parenright','bracketright','braceright','guilsinglright',
    'guillemotright','quoteleft','quotedblleft','exclamdown','periodcentered','periodcentered','questiondown',
    'trademark','copyright','registered','copyrightsound','degree','one.sups','two.sups','three.sups','lozenge',
    'greater','greaterequal','approxequal','notequal')

# For convenience in spacing and reference the base capitals are also added to this list.
TN_COMPOSITES_LC = ('a', 'aacute', 'abreve', 'acircumflex', 'adieresis', 'ae', 'aeacute', 'agrave', 'amacron', 'aogonek', 'aring',
    'aringacute', 'atilde', 'b', 'c', 'cacute', 'ccaron', 'ccedilla', 'ccircumflex', 'cdotaccent', 'ckreska', 'd', 'dcaron', 'dcroat', 'dotlessi',
    'dotlessj', 'e', 'eacute', 'ebreve', 'ecaron', 'ecircumflex', 'edieresis', 'edotaccent', 'egrave', 'emacron', 'eng', 'eogonek', 'eth', 'f', 'g',
    'gbreve', 'gcircumflex', 'gcommaaccent', 'gdotaccent', 'germandbls', 'h', 'hbar', 'hcircumflex', 'i', 'iacute', 'ibreve', 'icircumflex',
    'idieresis', 'igrave', 'ij', 'imacron', 'iogonek', 'itilde', 'k', 'jcircumflex', 'k', 'kcommaaccent', 'kgreenlandic', 'l', 'lacute', 'lcaron',
    'lcommaaccent', 'ldot', 'lslash', 'm', 'n', 'nacute', 'napostrophe', 'ncaron', 'ncommaaccent', 'nkreska', 'ntilde', 'o', 'oacute', 'obreve',
    'ocircumflex', 'ocreska', 'odieresis', 'oe', 'ograve', 'ohorn', 'ohungarumlaut', 'omacron', 'oslash', 'oslashacute', 'otilde',
    'p', 'q', 'r', 'racute', 'rcaron', 'rcommaaccent', 's', 'sacute', 'scaron', 'scedilla', 'schwa', 'scircumflex', 'scommaaccent', 'skreska', 't', 'tbar',
    'tcaron', 'tcedilla', 'tcommaaccent', 'thorn', 'u', 'uacute', 'ubreve', 'ucircumflex', 'udieresis', 'ugrave', 'uhorn', 'uhungarumlaut',
    'umacron', 'uogonek', 'uring', 'utilde', 'v', 'w', 'wacute', 'wcircumflex', 'wdieresis', 'wgrave', 'x', 'y', 'yacute', 'ycircumflex', 'ydieresis',
    'ygrave', 'z', 'zacute', 'zcaron', 'zdotaccent', 'zkreska')

# For convenience in spacing and reference the base capitals are also added to this list.
TN_COMPOSITES_UC = ('A', 'AE', 'AEacute', 'Aacute', 'Abreve', 'Acircumflex', 'Adieresis', 'Agrave', 'Amacron', 'Aogonek',
    'Aring', 'Atilde', 'B', 'C', 'Cacute', 'Ccaron', 'Ccedilla', 'Ccircumflex', 'Cdotaccent', 'Ckreska', 'Dcaron', 'D', 'Dcroat', 'E', 'Eacute',
    'Ebreve', 'Ecaron', 'Ecircumflex', 'Edieresis', 'Edotaccent', 'Egrave', 'Emacron', 'Eng', 'Eogonek', 'Eth', 'F', 'G', 'Gbreve',
    'Gcircumflex', 'Gcommaaccent', 'Gdotaccent', 'H', 'Hbar', 'Hcircumflex', 'I', 'IJ', 'Iacute', 'Ibreve', 'Icircumflex', 'Idieresis',
    'Idotaccent', 'Igrave', 'Imacron', 'Iogonek', 'Itilde', 'J', 'Jcircumflex', 'K', 'Kcommaaccent', 'L', 'Lacute', 'Lcaron', 'Lcommaaccent',
    'Ldot', 'Lslash', 'N', 'Nacute', 'Ncaron', 'Ncommaaccent', 'Nkreska', 'Ntilde', 'M', 'O', 'OE', 'Oacute', 'Obreve', 'Ocircumflex',
    'Odieresis', 'Ograve', 'Ohorn', 'Ohungarumlaut', 'Okreska', 'Omacron', 'Oslash', 'Oslashacute', 'Otilde', 'P', 'Q', 'R', 'Racute',
    'Rcaron', 'Rcommaaccent', 'S', 'Sacute', 'Scaron', 'Scedilla', 'Scircumflex', 'Scommaaccent', 'Skreska', 'T', 'Tbar', 'Tcaron',
    'Tcedilla', 'Tcommaaccent', 'Thorn', 'U', 'Uacute', 'Ubreve', 'Ucircumflex', 'Udieresis', 'Ugrave', 'Uhorn', 'Uhungarumlaut',
    'Umacron', 'Uogonek', 'Uring', 'Utilde', 'V', 'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 'Wgrave', 'X', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis',
    'Ygrave', 'Z', 'Zacute', 'Zcaron', 'Zdotaccent', 'Zkreska')
TN_COMPOSITES_SC = []
TN_COMPOSITES_LCSC = []
for c in TN_COMPOSITES_UC:
    # For convenience in spacing and reference the base smallcaps are also added to this list.
    TN_COMPOSITES_SC.append(c+'.sc')
    TN_COMPOSITES_LCSC.append(c.lower() + '.sc')

TM_COMPOSITE_FRACTIONS = ('onequarter','onehalf','threequarters', 'percent', 'perthousand',)
TN_COMPOSITES = TN_COMPOSITES_UC + TN_COMPOSITES_LC + TM_COMPOSITE_FRACTIONS

TN_ACCENT2CMB = {
    'circumflex': 'circumflexcmb',
    'caron': 'caroncmb',
    'grave': 'gravecmb',
    'dieresis': 'dieresiscmb',
    'macron': 'macroncmb',
    'acute': 'acutecmb',
    'cedilla': 'cedillacmb',
    'breve': 'brevecmb',
    'dotaccent': 'dotaccentcmb',
    'ring': 'ringcmb',
    'ogonek': 'ogonekcmb',
    'tilde': 'tildecmb',
    'hungarumlaut': 'hungarumlautcmb',
    'hook': 'hookcmb',
    'caron.vert': 'caroncmb.vert',
}
TN_CMB2ACCENT = {}
for accent, cmb in TN_ACCENT2CMB.items():
    TN_CMB2ACCENT[cmb] = accent
TN_COMBINATES = sorted(TN_ACCENT2CMB.keys())

TN_GREEKPRIMARYCONTROLS = ('H','O','pi','o','rho','zero','one','period','comma','emdash','slash','plus')
TN_GREEKPRIMARY = ('Alpha','Beta','Gamma','Delta','Epsilon','Zeta','Eta','Theta','Iota','Kappa','Lambda','Mu','Nu','Xi','Omicron',
    'Pi','Rho','Sigma','Tau','Upsilon','Phi','Chi','Psi','Omega','alpha','beta','gamma','delta','epsilon','zeta','eta',
    'theta','iota','kappa','lambda','mu','nu','xi','omicron','pi','rho','sigma1','sigma','tau','upsilon','phi','chi',
    'psi','omega')
TN_GREEKCOMPOSITES = ('Alphatonos','Epsilontonos','Etatonos','Iotatonos','Omicrontonos','Upsilontonos','Omegatonos','Iotadieresis',
    'Upsilondieresis','alphatonos','epsilontonos','etatonos','iotatonos','upsilondieresistonos','iotadieresis',
    'iotadieresistonos','upsilondieresis','omicrontonos','upsilontonos','omegatonos')
TN_GREEKACCENT2CMB = {
    'tonos': 'tonoscmb',
    'dieresistonos': 'dieresistonoscmb',
    'periodcentered': 'periodcenteredcmb',
}
TN_CMB2GREEKACCENT = {}
for accent, cmb in TN_GREEKACCENT2CMB.items():
    TN_CMB2GREEKACCENT[cmb] = accent
TN_GREEKCOMBINATES = sorted(TN_GREEKACCENT2CMB.keys())
TN_CYRILLICPRIMARYCONTROLS = ('Ercyrillic','H','O','pecyrillic','ocyrillic','ercyrillic','zero','one','period','comma','emdash','slash','plus')
TN_CYRILLICPRIMARY = ('Acyrillic','Vecyrillic','Becyrillic','Gecyrillic','Decyrillic','Iecyrillic','Zhecyrillic','Zhedescendercyrillic',
    'Zecyrillic','Iicyrillic','Kacyrillic','Kadescendercyrillic','Elcyrillic','Icyrillic','Emcyrillic','Encyrillic',
    'Jecyrillic','Ocyrillic','Pecyrillic','Ercyrillic','Escyrillic','Dzecyrillic','Tecyrillic','Ucyrillic','Efcyrillic',
    'Khacyrillic','Hadescendercyrillic','Tsecyrillic','Ljecyrillic','Njecyrillic','Tshecyrillic','Djecyrillic','Checyrillic',
    'Chedescendercyrillic','Hardsigncyrillic','Yericyrillic','Softsigncyrillic','Dzhecyrillic','Shacyrillic','Shchacyrillic',
    'Ereversedcyrillic','Ecyrillic','IUcyrillic','IAcyrillic','Gheupturncyrillic','Ustraightstrokecyrillic','acyrillic',
    'vecyrillic','becyrillic','gecyrillic','decyrillic','iecyrillic','zhecyrillic','zhedescendercyrillic','zecyrillic',
    'iicyrillic','kacyrillic','kadescendercyrillic','elcyrillic','emcyrillic','encyrillic','jecyrillic','ocyrillic',
    'pecyrillic','ercyrillic','escyrillic','tecyrillic','ucyrillic','efcyrillic','khacyrillic','hadescendercyrillic',
    'tsecyrillic','checyrillic','chedescendercyrillic','shacyrillic','shchacyrillic','hardsigncyrillic','yericyrillic',
    'softsigncyrillic','ereversedcyrillic','iucyrillic','iacyrillic','djecyrillic','ecyrillic','dzecyrillic','icyrillic',
    'ljecyrillic','njecyrillic','tshecyrillic','dzhecyrillic','gheupturncyrillic','ustraightstrokecyrillic')
TN_CYRILLICCOMPOSITES = ('IEgravecyrillic','Iocyrillic','Gjecyrillic','Yicyrillic','Kjecyrillic','Igravecyrillic','Ushortcyrillic',
    'Iishortcyrillic','iishortcyrillic','iegravecyrillic','iocyrillic','gjecyrillic','yicyrillic','kjecyrillic',
    'igravecyrillic','ushortcyrillic')

SS_CONTROLS = ('O', 'H', 'V', 'o', 'h', 'v')
SS_UC = TN_UC + TN_COMPOSITES_UC
SS_LC = TN_LC + TN_COMPOSITES_LC

SS_SC = []
for c in SS_UC:
    SS_SC.append(c+'.sc')

SS_SORTS_MC = ("period", "comma", "colon", "semicolon", "ellipsis", "exclamdown", "exclam", "exclamdbl",
    "questiondown", "question", "parenleft", "parenright", "bracketleft", "bracketright", "braceleft",
    "braceright", "hyphen", "underscore", "endash", "endash.salt_en", "emdash", "emdash.salt_em", "quoteleft",
    "quoteright", "quotedblleft", "quotedblright", "quotesinglbase", "quotedblbase", "guillemotleft",
    "guillemotright", "guilsinglleft", "guilsinglright", "brokenbar", "slash", "backslash", "bar", "asterisk",
    "dagger", "daggerdbl", "periodcentered", "bullet", "quotesingle", "quotedbl", "at", "registered", "copyright",
    "uni2117", "trademark", "apple")

SS_SORTS_UC = ("exclamdown.uc", "exclam.uc", "exclamdbl.uc", "questiondown.uc", "question.uc", "parenleft.uc",
    "parenright.uc", "bracketleft.uc", "bracketright.uc", "braceleft.uc", "braceright.uc", "hyphen.uc", "endash.uc",
    "endash.salt_en.uc", "emdash.uc", "emdash.salt_em.uc", "guillemotleft.uc", "guillemotright.uc",
    "guilsinglleft.uc", "guilsinglright.uc", "periodcentered.uc", "bullet.uc", "at.uc")

SS_SORTS_SC = ("exclamdown.sc", "exclam.sc", "exclamdbl.sc", "questiondown.sc", "question.sc", "parenleft.sc",
    "parenright.sc", "bracketleft.sc", "bracketright.sc", "braceleft.sc", "braceright.sc", "hyphen.sc",
    "endash.sc", "endash.salt_en.sc", "emdash.sc", "emdash.salt_em.sc", "quoteleft.sc", "quoteright.sc",
    "quotedblleft.sc", "quotedblright.sc", "quotesinglbase.sc", "quotedblbase.sc", "guillemotleft.sc",
    "guillemotright.sc", "guilsinglleft.sc", "guilsinglright.sc", "brokenbar.sc", "slash.sc", "backslash.sc",
    "bar.sc", "asterisk.sc", "dagger.sc", "daggerdbl.sc", "periodcentered.sc", "bullet.sc", "quotesingle.sc",
    "quotedbl.sc", "at.sc", "registered.sc", "copyright.sc", "uni2117.sc", "trademark.sc")

SS_FIGURES_MC = TN_FIGURES + ("plus", "minus", "multiply", "divide", "equal", "less", "greater", "dollar",
    "cent", "Euro", "sterling", "yen", "florin", "numbersign", "section", "paragraph", "percent",
    "perthousand", "degree", "minute", "second", "ordfeminine", "ordmasculine", "equivalent", )

SS_FIGURES_SC = []
SS_FIGURES_LC = []
SS_FIGURES_TAB = []
for c in SS_FIGURES_MC:
    SS_FIGURES_SC.append(c+'.sc')
    SS_FIGURES_LC.append(c+'.lc')
    SS_FIGURES_TAB.append(c+'.tab')
SS_FIGURESMATH = ("asciicircum", "asciitilde", "lessequal", "greaterequal", "plusminus", "approxequal",
    "notequal", "logicalnot", "radical", "infinity", "lozenge", "currency", "mu", "summation",
    "product", "pi", "integral", "Omega", "partialdiff", "Delta", "estimated", "checkmark")

SS_FIGURES_SUPSSINF = (
    "zero.sups", "one.sups", "two.sups", "three.sups", "four.sups", "five.sups", "six.sups", "seven.sups",
    "eight.sups", "nine.sups", "zero.sinf", "one.sinf", "two.sinf", "three.sinf", "four.sinf", "five.sinf",
    "six.sinf", "seven.sinf", "eight.sinf", "nine.sinf")

SS_FIGURES_FRACTION = ("fraction", "space.frac", "zero.numr", "one.numr", "two.numr", "three.numr",
    "four.numr", "five.numr", "six.numr", "seven.numr", "eight.numr", "nine.numr", "zero.dnom", "one.dnom",
    "two.dnom", "three.dnom", "four.dnom", "five.dnom", "six.dnom", "seven.dnom", "eight.dnom", "nine.dnom",
    "oneeighth", "onehalf", "onequarter", "seveneighths", "threeeighths", "threequarters", "fiveeighths",
)

SS_SPACES = ("space", "space.en", "space.em", "space.thin", "space.hair")

SS_ALPHA_SUPS = ("a.sups", "b.sups", "c.sups", "d.sups", "e.sups", "egrave.sups", "f.sups", "g.sups",
    "h.sups", "i.sups", "j.sups", "k.sups", "l.sups", "m.sups", "n.sups", "o.sups", "p.sups",
    "q.sups", "r.sups", "s.sups", "t.sups", "u.sups", "v.sups", "w.sups", "x.sups", "y.sups", "z.sups")

SS_LIGATURES_DIPHTHONGS = TN_SECONDARY_LIGATURES + ('oe','OE','ae','AE')

SS_LIGATURES_DISCRETIONARY = ("w_w_w", "c_t", "s_t", "s_p") # c_k, s_k, c_h, s_h, c_p, s_p

SS_CURRENCY = (
    "won", "sheqel", "peseta", "numero", "lira", "franc", "dong", "cruzeiro", "colonsign", "bahtthai",
    "rupeesignbengali", "rupeemarkbengali", "dollar", "cent", "Euro", "sterling", "kip",
    "turkishlira", "tugrik", "tenge", "sheqel", "scriptm", "rupee", "ruble", "rialarabic",
    "peso", "nordicmark", "naira", "mill", "manat", "livretournois", "indianrupee", "hryvnia",
    "guarani", "germanpenny", "dragma", "cedi", "austral", "armeniandram", "afghani", "gujaratirupee",
    "tamilrupee", 'khmer', 'ecu', "spesmilo",
)
SS_CYRILLIC_UC = ("Abrevecyrillic","Acyrillic","Adieresiscyrillic","Aiecyrillic","Becyrillic","Cheabkhasiancyrillic",
    "Checyrillic","Chedescenderabkhasiancyrillic","Chedescendercyrillic","Chedieresiscyrillic",
    "Chekhakassiancyrillic","Cheverticalstrokecyrillic","Decyrillic","Djecyrillic","Dzeabkhasiancyrillic",
    "Dzecyrillic","Dzhecyrillic","Ecyrillic","Efcyrillic","Eiotifiedcyrillic","Elcyrillic","Emcyrillic",
    "Encyrillic","Endescendercyrillic","Enghecyrillic","Enhookcyrillic","Ercyrillic","Ereversedcyrillic",
    "Escyrillic","Esdescendercyrillic","Fitacyrillic","Gecyrillic","Ghemiddlehookcyrillic",
    "Ghestrokecyrillic","Gheupturncyrillic","Gjecyrillic","Haabkhasiancyrillic","Hadescendercyrillic",
    "Hardsigncyrillic","IAcyrillic","IEgravecyrillic","IUcyrillic","Icyrillic","Idieresiscyrillic",
    "Iebrevecyrillic","Iecyrillic","Igravecyrillic","Iicyrillic","Iishortcyrillic","Imacroncyrillic",
    "Iocyrillic","Izhitsacyrillic","Izhitsadblgravecyrillic","Jecyrillic","Kabashkircyrillic",
    "Kacyrillic","Kadescendercyrillic","Kahookcyrillic","Kastrokecyrillic","Kaverticalstrokecyrillic",
    "Khacyrillic","Kjecyrillic","Koppacyrillic","Ksicyrillic","Ljecyrillic","Njecyrillic","Obarredcyrillic",
    "Obarreddieresiscyrillic","Ocyrillic","Odieresiscyrillic","Omegacyrillic","Omegaroundcyrillic",
    "Omegatitlocyrillic","Otcyrillic","Pecyrillic","Pemiddlehookcyrillic","Psicyrillic","Schwacyrillic",
    "Schwadieresiscyrillic","Shacyrillic","Shchacyrillic","Shhacyrillic","Softsigncyrillic","Tecyrillic",
    "Tedescendercyrillic","Tetsecyrillic","Tsecyrillic","Tshecyrillic","Ucyrillic","Udieresiscyrillic",
    "Uhungarumlautcyrillic","Ukcyrillic","Umacroncyrillic","Ushortcyrillic","Ustraightcyrillic",
    "Ustraightstrokecyrillic","Vecyrillic","Yatcyrillic","Yericyrillic","Yerudieresiscyrillic",
    "Yicyrillic","Yusbigcyrillic","Yusbigiotifiedcyrillic","Yuslittlecyrillic","Yuslittleiotifiedcyrillic",
    "Zecyrillic","Zedescendercyrillic","Zedieresiscyrillic","Zhebrevecyrillic","Zhecyrillic",
    "Zhedescendercyrillic","Zhedieresiscyrillic",)
    # Using brevecyrillic
SS_CYRILLIC_LC = ("abrevecyrillic","acyrillic","adieresiscyrillic",
    "aiecyrillic","becyrillic","cheabkhasiancyrillic","checyrillic","chedescenderabkhasiancyrillic",
    "chedescendercyrillic","chedieresiscyrillic","chekhakassiancyrillic","cheverticalstrokecyrillic",
    "dasiapneumatacyrilliccmb","decyrillic","djecyrillic","dzeabkhasiancyrillic","dzecyrillic","dzhecyrillic",
    "ecyrillic","efcyrillic","eiotifiedcyrillic","elcyrillic","emcyrillic","encyrillic","endescendercyrillic",
    "enghecyrillic","enhookcyrillic","ercyrillic","ereversedcyrillic","escyrillic","esdescendercyrillic",
    "fitacyrillic","gecyrillic","ghemiddlehookcyrillic","ghestrokecyrillic","gheupturncyrillic",
    "gjecyrillic","haabkhasiancyrillic","hadescendercyrillic","hardsigncyrillic","iacyrillic","icyrillic",
    "idieresiscyrillic","iebrevecyrillic","iecyrillic","iegravecyrillic","igravecyrillic","iicyrillic",
    "iishortcyrillic","imacroncyrillic","iocyrillic","iucyrillic","izhitsacyrillic","izhitsadblgravecyrillic",
    "jecyrillic","kabashkircyrillic","kacyrillic","kadescendercyrillic","kahookcyrillic","kastrokecyrillic",
    "kaverticalstrokecyrillic","khacyrillic","kjecyrillic","koppacyrillic","ksicyrillic","ljecyrillic",
    "njecyrillic","obarredcyrillic","obarreddieresiscyrillic","ocyrillic","odieresiscyrillic","omegacyrillic",
    "omegaroundcyrillic","omegatitlocyrillic","otcyrillic","palatalizationcyrilliccmb","palochkacyrillic",
    "pecyrillic","pemiddlehookcyrillic","psicyrillic","psilipneumatacyrilliccmb","schwacyrillic",
    "schwadieresiscyrillic","shacyrillic","shchacyrillic","shhacyrillic","softsigncyrillic","tecyrillic",
    "tedescendercyrillic","tetsecyrillic","thousandcyrillic","titlocyrilliccmb","tsecyrillic","tshecyrillic",
    "ucyrillic","udieresiscyrillic","uhungarumlautcyrillic","ukcyrillic","umacroncyrillic","ushortcyrillic",
    "ustraightcyrillic","ustraightstrokecyrillic","vecyrillic","yatcyrillic","yericyrillic",
    "yerudieresiscyrillic","yicyrillic","yusbigcyrillic","yusbigiotifiedcyrillic","yuslittlecyrillic",
    "yuslittleiotifiedcyrillic","zecyrillic","zedescendercyrillic","zedieresiscyrillic","zhebrevecyrillic",
    "zhecyrillic","zhedescendercyrillic","zhedieresiscyrillic")
SS_CYRILLIC = SS_CYRILLIC_UC + SS_CYRILLIC_LC

SS_GREEK_UC = ('Alpha','Alphatonos','Beta','Chi','Delta*','Epsilon','Epsilontonos','Eta','Etatonos','Gamma','Iota',
    'Iotadieresis','Iotatonos','Kappa','Lambda','Mu','Nu','Omega*','Omegatonos','Omicron','Omicrontonos',
    'Phi','Pi','Psi','Rho','Sigma','Tau','Theta','Upsilon','Upsilondieresis','Upsilontonos','Xi','Zeta',)
SS_GREEK_LC = ('alpha','alphatonos','anoteleia','beta','chi','delta','dieresistonos','epsilon','epsilontonos','eta',
    'etatonos','gamma','iota','iotadieresis','iotadieresistonos','iotatonos','kappa','lambda','mu','nu',
    'omega','omegatonos','omicron','omicrontonos','phi','pi','psi','rho','sigma','sigma1','tau','theta',
    'tonos','upsilon','upsilondieresis','upsilondieresistonos','upsilontonos','xi','zeta')
SS_GREEK = SS_GREEK_UC + SS_GREEK_LC

SS_ASCII = ("space", "exclam", "quotedbl", "numbersign", "dollar", "percent", "ampersand", "quotesingle",
    "parenleft", "parenright", "asterisk", "plus", "comma", "hyphen", "period", "slash", "zero",
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "colon", "semicolon",
    "less", "equal", "greater", "question", "at") + TN_UC + ("bracketleft",
    "backslash", "bracketright", "asciicircum", "underscore", "grave") + TN_LC + (
    "braceleft", "bar", "braceright", "asciitilde")

SS_BOXES = (
    "block","dbldnhorzbxd","dbldnleftbxd","dbldnrightbxd","dblhorzbxd","dbluphorzbxd","dblupleftbxd",
    "dbluprightbxd","dblvertbxd","dblverthorzbxd","dblvertleftbxd","dblvertrightbxd","dnblock",
    "dndblhorzsngbxd","dndblleftsngbxd","dndblrightsngbxd","dneighthblock","dnfiveeighthsblock",
    "dnhalfblock","dnheavyhorzlightbxd","dnheavyleftlightbxd","dnheavyleftuplightbxd","dnheavyrightlightbxd",
    "dnheavyrightuplightbxd","dnheavyuphorzlightbxd","dnlighthorzheavybxd","dnlightleftheavybxd",
    "dnlightleftupheavybxd","dnlightrightheavybxd","dnlightrightupheavybxd","dnlightuphorzheavybxd",
    "dnquarterblock","dnseveneighthsblock","dnsnghorzdblbxd","dnsngleftdblbxd","dnsngrightdblbxd",
    "dnthreeeighthsblock","dnthreequartersblock","fullblock","heavydbldashhorzbxd","heavydbldashvertbxd",
    "heavydnbxd","heavydnhorzbxd","heavydnleftbxd","heavydnrightbxd","heavyhorzbxd","heavyleftbxd",
    "heavyleftlightrightbxd","heavyquaddashhorzbxd","heavyquaddashvertbxd","heavyrightbxd",
    "heavytrpldashhorzbxd","heavytrpldashvertbxd","heavyupbxd","heavyuphorzbxd","heavyupleftbxd",
    "heavyuplightdnbxd","heavyuprightbxd","heavyvertbxd","heavyverthorzbxd","heavyvertleftbxd",
    "heavyvertrightbxd","leftdnheavyrightuplightbxd","lefteighthblock","leftfiveeighthsblock",
    "lefthalfblock","leftheavyrightdnlightbxd","leftheavyrightuplightbxd","leftheavyrightvertlightbxd",
    "leftlightrightdnheavybxd","leftlightrightupheavybxd","leftlightrightvertheavybxd","leftquarterblock",
    "leftseveneighthsblock","leftthreeeighthsblock","leftthreequartersblock","leftupheavyrightdnlightbxd",
    "lfblock","lightarcdnleftbxd","lightarcdnrightbxd","lightarcupleftbxd","lightarcuprightbxd",
    "lightdbldashhorzbxd","lightdbldashvertbxd","lightdiagcrossbxd","lightdiagupleftdnrightbxd",
    "lightdiaguprightdnleftbxd","lightdnbxd","lightdnhorzbxd","lightdnleftbxd","lightdnrightbxd",
    "lighthorzbxd","lightleftbxd","lightleftheavyrightbxd","lightquaddashhorzbxd","lightquaddashvertbxd",
    "lightrightbxd","lighttrpldashhorzbxd","lighttrpldashvertbxd","lightupbxd","lightupheavydnbxd",
    "lightuphorzbxd","lightupleftbxd","lightuprightbxd","lightvertbxd","lightverthorzbxd",
    "lightvertleftbxd","lightvertrightbxd","rightdnheavyleftuplightbxd","righteighthblock",
    "righthalfblock","rightheavyleftdnlightbxd","rightheavyleftuplightbxd","rightheavyleftvertlightbxd",
    "rightlightleftdnheavybxd","rightlightleftupheavybxd","rightlightleftvertheavybxd",
    "rightupheavyleftdnlightbxd","rtblock","upblock","updblhorzsngbxd","updblleftsngbxd","updblrightsngbxd",
    "upeighthblock","uphalfblock","upheavydnhorzlightbxd","upheavyhorzlightbxd","upheavyleftdnlightbxd",
    "upheavyleftlightbxd","upheavyrightdnlightbxd","upheavyrightlightbxd","uplightdnhorzheavybxd",
    "uplighthorzheavybxd","uplightleftdnheavybxd","uplightleftheavybxd","uplightrightdnheavybxd",
    "uplightrightheavybxd","upsnghorzdblbxd","upsngleftdblbxd","upsngrightdblbxd","vertdblhorzsngbxd",
    "vertdblleftsngbxd","vertdblrightsngbxd","vertheavyhorzlightbxd","vertheavyleftlightbxd",
    "vertheavyrightlightbxd","vertlighthorzheavybxd","vertlightleftheavybxd","vertlightrightheavybxd",
    "vertsnghorzdblbxd","vertsngleftdblbxd","vertsngrightdblbxd",
    "darkshade", "mediumshade", "orthogonal", "blackcircle", "blackdownpointingtriangle", "blacksmallsquare",
    "blackuppointingtriangle", "circle",
)
SS_ARROWS = (
    "arrowboth", "arrowdown", "arrowup", "arrowleft", "arrowright", "arrowupdn",
)
# Group sorting
SS_GROUP_SORTING = (
    set(SS_UC), set(SS_LC), set(SS_SC), set(SS_SORTS_MC), set(SS_SORTS_UC),
    set(SS_SORTS_SC), set(SS_FIGURES_MC), set(SS_FIGURES_SC), set(SS_FIGURES_LC), set(SS_FIGURES_TAB),
    set(SS_FIGURESMATH), set(SS_FIGURES_SUPSSINF), set(SS_FIGURES_FRACTION), set(SS_ACCENTSCMB.keys()),
    set(SS_SPACES), set(SS_ALPHA_SUPS), set(SS_LIGATURES_DIPHTHONGS), set(SS_LIGATURES_DISCRETIONARY),
    set(SS_ASCII), set(SS_CURRENCY), set(SS_CYRILLIC), set(SS_GREEK), set(SS_BOXES), set(SS_ARROWS),
)
# Dynamic fractions and compare with composite percent and perthousand and standard fractions.
#TM_COMPOSITE_FRACTIONS = ('onequarter','onehalf','threequarters', 'percent', 'perthousand',)
FRACTIONS = '/'+'/'.join(TM_COMPOSITE_FRACTIONS) + '/one.numr/fraction/two.dnom/space/one.numr/fraction/two.dnom/space/three.numr/fraction/four.dnom/space/zero.numr/fraction/zero.dnom/space/zero.numr/fraction/zero.dnom/zero.dnom'
figures = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
for i1 in figures:
    for i2 in figures:
         FRACTIONS += '/space/two.numr/fraction/%s.dnom/%s.dnom' % (i1, i2) # Escape slash to differentiate from /glyphname.
for i1 in figures:
    for i2 in figures:
         FRACTIONS += '/space/%s.numr/%s.numr/fraction/two.dnom' % (i1, i2) # Escape slash to differentiate from /glyphname.

# Superior and inferior samples
SUPERIORS_PAGE = ''
for c in SS_ALPHA_SUPS:
    c = c.split('.')[0]
    SUPERIORS_PAGE += '/i.sups/%s.sups' % c
for c in SS_ALPHA_SUPS:
    c = c.split('.')[0]
    SUPERIORS_PAGE += '/o.sups/%s.sups' % c
for c in figures:
    SUPERIORS_PAGE += '/i.sups/%s.sups' % c
for c in figures:
    SUPERIORS_PAGE += '/o.sups/%s.sups' % c
SUPERIORS_PAGE += '\n'
for c in SS_ALPHA_SUPS:
    c = c.split('.')[0]
    SUPERIORS_PAGE += '/i.sinf/%s.sinf' % c
for c in SS_ALPHA_SUPS:
    c = c.split('.')[0]
    SUPERIORS_PAGE += '/o.sinf/%s.sinf' % c
for c in figures:
    SUPERIORS_PAGE += '/i.sinf/%s.sinf' % c
for c in figures:
    SUPERIORS_PAGE += '/o.sinf/%s.sinf' % c
SUPERIORS_PAGE += '\n\n'
i = 0
for ext in ('sinf', 'sups'):
    for c in SS_ALPHA_SUPS:
        c = c.split('.')[0]
        f = figures[i]
        for cc in TN_UC+TN_LC:
            SUPERIORS_PAGE += '/%s/%s.%s/%s.%s/ ' % (cc, c, ext, f, ext)
        i += 1
        if i >= len(figures):
            i = 0
    for c in figures:
        f = figures[i]
        for cc in TN_UC+TN_LC:
            SUPERIORS_PAGE += '/%s/%s.%s/%s.%s/ ' % (cc, c, ext, f, ext)
        i += 1
        if i >= len(figures):
            i = 0
    SUPERIORS_PAGE += '\n'

# Used for ordering of master->instance in spacing groups. Used by Builder and TextCenter2
SPACE_LC = ('n','o','v','a','b','c','d','e','f','g','h','i','j','k','l','m','p','q','r','s','t','u','w','x','y','z')
SPACE_UC = ('H','O','V','A','B','C','D','E','F','G','I','J','K','L','M','N','P','Q','R','S','T','U','W','X','Y','Z')
SPACE_SC = []
for c in SPACE_UC:
    SPACE_SC.append(c+'sc')

# Space categories are used by the profile builders, to make sure that only glyphs inside a group get compater.
# This way we avoid that "A" and "/" are joining the same space group accidentally.
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
# TODO: Languages To be added as smart sets.
'''

        </array>
        <key>query</key>


        Unicode Ranges

        140332504344736

    <dict>
        <key>group</key>
        <array>
            <dict>
                <key>glyphNames</key>
                <array>
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Ocircumflex
                    ocircumflex
                    Ucircumflex
                </array>
                <key>query</key>
                Name IN {"Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Ocircumflex", "ocircumflex", "Ucircumflex"}

                Afrikaans

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccedilla
                    ccedilla
                    Schwa
                    schwa
                    Gbreve
                    gbreve
                    Idotaccent
                    dotlessi
                    Odieresis
                    odieresis
                    Scedilla
                    scedilla
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Ccedilla", "ccedilla", "Schwa", "schwa", "Gbreve", "gbreve", "Idotaccent", "dotlessi", "Odieresis", "odieresis", "Scedilla", "scedilla", "Udieresis", "udieresis"}

                Azeri

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Sacute
                    sacute
                    Scaron
                    scaron
                    Ubreve
                    ubreve
                    Zacute
                    zacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Lslash", "lslash", "Nacute", "nacute", "Sacute", "sacute", "Scaron", "scaron", "Ubreve", "ubreve", "Zacute", "zacute", "Zcaron", "zcaron"}

                Belarussian

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Scaron", "scaron", "Zcaron", "zcaron"}

                Bosnian

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Ecircumflex
                    ecircumflex
                    Ntilde
                    ntilde
                    Ocircumflex
                    ocircumflex
                    Ugrave
                    ugrave
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Ecircumflex", "ecircumflex", "Ntilde", "ntilde", "Ocircumflex", "ocircumflex", "Ugrave", "ugrave", "Udieresis", "udieresis"}

                Breton

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Ccedilla
                    ccedilla
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Idieresis
                    idieresis
                    Ldot
                    ldot
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Ccedilla", "ccedilla", "Egrave", "egrave", "Eacute", "eacute", "Iacute", "iacute", "Idieresis", "idieresis", "Ldot", "ldot", "Ograve", "ograve", "Oacute", "oacute", "Uacute", "uacute", "Udieresis", "udieresis"}

                Catalan

            <dict>
                <key>glyphNames</key>
                <array>
                    Wcircumflex
                    wcircumflex
                </array>
                <key>query</key>
                Name IN {"Wcircumflex", "wcircumflex"}

                Chichewa

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Ccaron
                    ccaron
                    Dcaron
                    dcaron
                    Eacute
                    eacute
                    Ecaron
                    ecaron
                    Iacute
                    iacute
                    Ncaron
                    ncaron
                    Oacute
                    oacute
                    Rcaron
                    rcaron
                    Scaron
                    scaron
                    Tcaron
                    tcaron
                    Uacute
                    uacute
                    Uring
                    uring
                    Yacute
                    yacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Ccaron", "ccaron", "Dcaron", "dcaron", "Eacute", "eacute", "Ecaron", "ecaron", "Iacute", "iacute", "Ncaron", "ncaron", "Oacute", "oacute", "Rcaron", "rcaron", "Scaron", "scaron", "Tcaron", "tcaron", "Uacute", "uacute", "Uring", "uring", "Yacute", "yacute", "Zcaron", "zcaron"}

                Czech

            <dict>
                <key>glyphNames</key>
                <array>
                    Aring
                    aring
                    AE
                    ae
                    Eacute
                    eacute
                    Oslash
                    oslash
                </array>
                <key>query</key>
                Name IN {"Aring", "aring", "AE", "ae", "Eacute", "eacute", "Oslash", "oslash"}

                Danish

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Odieresis
                    odieresis
                    germandbls
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Odieresis", "odieresis", "germandbls", "Udieresis", "udieresis"}

                German

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Ntilde
                    ntilde
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Ntilde", "ntilde", "Oacute", "oacute", "Uacute", "uacute", "Udieresis", "udieresis"}

                Spanish

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Otilde
                    otilde
                    Odieresis
                    odieresis
                    Scaron
                    scaron
                    Udieresis
                    udieresis
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Otilde", "otilde", "Odieresis", "odieresis", "Scaron", "scaron", "Udieresis", "udieresis", "Zcaron", "zcaron"}

                Estonian

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccedilla
                    ccedilla
                    Ntilde
                    ntilde
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Ccedilla", "ccedilla", "Ntilde", "ntilde", "Udieresis", "udieresis"}

                Basque

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Odieresis
                    odieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Odieresis", "odieresis"}

                Finnish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Iacute
                    iacute
                    Idieresis
                    idieresis
                    IJ
                    ij
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Odieresis
                    odieresis
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Acircumflex", "acircumflex", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Iacute", "iacute", "Idieresis", "idieresis", "IJ", "ij", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Odieresis", "odieresis", "Uacute", "uacute", "Ucircumflex", "ucircumflex"}

                Flemish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    AE
                    ae
                    Eth
                    eth
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Oslash
                    oslash
                    Uacute
                    uacute
                    Yacute
                    yacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "AE", "ae", "Eth", "eth", "Iacute", "iacute", "Oacute", "oacute", "Oslash", "oslash", "Uacute", "uacute", "Yacute", "yacute"}

                Faroese

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Acircumflex
                    acircumflex
                    Ccedilla
                    ccedilla
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Ocircumflex
                    ocircumflex
                    OE
                    oe
                    Ugrave
                    ugrave
                    Ucircumflex
                    ucircumflex
                    Udieresis
                    udieresis
                    Ydieresis
                    ydieresis
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Acircumflex", "acircumflex", "Ccedilla", "ccedilla", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Ocircumflex", "ocircumflex", "OE", "oe", "Ugrave", "ugrave", "Ucircumflex", "ucircumflex", "Udieresis", "udieresis", "Ydieresis", "ydieresis"}

                French

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Ecircumflex
                    ecircumflex
                    Icircumflex
                    icircumflex
                    Ocircumflex
                    ocircumflex
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Ecircumflex", "ecircumflex", "Icircumflex", "icircumflex", "Ocircumflex", "ocircumflex", "Uacute", "uacute", "Ucircumflex", "ucircumflex"}

                Frisian

            <dict>
                <key>glyphNames</key>
                <array>
                    Bhook
                    bhook
                    Dhook
                    dhook
                    Eng
                    eng
                    nhookleft
                </array>
                <key>query</key>
                Name IN {"Bhook", "bhook", "Dhook", "dhook", "Eng", "eng", "nhookleft"}

                Fulani

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Igrave
                    igrave
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ugrave
                    ugrave
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Egrave", "egrave", "Eacute", "eacute", "Igrave", "igrave", "Ograve", "ograve", "Oacute", "oacute", "Ugrave", "ugrave"}

                Gaelic

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Ntilde
                    ntilde
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Ntilde", "ntilde", "Oacute", "oacute", "Uacute", "uacute", "Udieresis", "udieresis"}

                Galician

            <dict>
                <key>glyphNames</key>
                <array>
                    Aring
                    aring
                    AE
                    ae
                    Oslash
                    oslash
                </array>
                <key>query</key>
                Name IN {"Aring", "aring", "AE", "ae", "Oslash", "oslash"}

                Greenlandic

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    atilde
                    Eacute
                    eacute
                    etilde
                    uE005
                    Iacute
                    iacute
                    itilde
                    Ntilde
                    ntilde
                    Oacute
                    oacute
                    otilde
                    Uacute
                    uacute
                    utilde
                    ytilde
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "atilde", "Eacute", "eacute", "etilde", "uE005", "Iacute", "iacute", "itilde", "Ntilde", "ntilde", "Oacute", "oacute", "otilde", "Uacute", "uacute", "utilde", "ytilde"}

                Guarani

            <dict>
                <key>glyphNames</key>
                <array>
                    Bhook
                    bhook
                    Dhook
                    dhook
                </array>
                <key>query</key>
                Name IN {"Bhook", "bhook", "Dhook", "dhook"}

                Hausa

            <dict>
                <key>glyphNames</key>
                <array>
                    Amacron
                    amacron
                    Emacron
                    emacron
                    Imacron
                    imacron
                    Omacron
                    omacron
                    Umacron
                    umacron
                </array>
                <key>query</key>
                Name IN {"Amacron", "amacron", "Emacron", "emacron", "Imacron", "imacron", "Omacron", "omacron", "Umacron", "umacron"}

                Hawaiian

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Scaron", "scaron", "Zcaron", "zcaron"}

                Croatian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Odieresis
                    odieresis
                    Ohungarumlaut
                    ohungarumlaut
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                    Uhungarumlaut
                    uhungarumlaut
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Oacute", "oacute", "Odieresis", "odieresis", "Ohungarumlaut", "ohungarumlaut", "Uacute", "uacute", "Udieresis", "udieresis", "Uhungarumlaut", "uhungarumlaut"}

                Hungarian

            <dict>
                <key>glyphNames</key>
                <array>
                    Idotbelow
                    idotbelow
                    Odotbelow
                    odotbelow
                    Udotbelow
                    udotbelow
                </array>
                <key>query</key>
                Name IN {"Idotbelow", "idotbelow", "Odotbelow", "odotbelow", "Udotbelow", "udotbelow"}

                Igbo

            <dict>
                <key>glyphNames</key>
                <array>
                    Eacute
                    eacute
                </array>
                <key>query</key>
                Name IN {"Eacute", "eacute"}

                Indonesian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Oacute", "oacute", "Uacute", "uacute"}

                Irish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    AE
                    ae
                    Eth
                    eth
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Odieresis
                    odieresis
                    Thorn
                    thorn
                    Uacute
                    uacute
                    Yacute
                    yacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "AE", "ae", "Eth", "eth", "Eacute", "eacute", "Iacute", "iacute", "Oacute", "oacute", "Odieresis", "odieresis", "Thorn", "thorn", "Uacute", "uacute", "Yacute", "yacute"}

                Icelandic

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Adieresis
                    adieresis
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Eng
                    eng
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Acircumflex", "acircumflex", "Adieresis", "adieresis", "Ccaron", "ccaron", "Dcroat", "dcroat", "Eng", "eng", "Scaron", "scaron", "Zcaron", "zcaron"}

                Inari Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Igrave
                    igrave
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ugrave
                    ugrave
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Egrave", "egrave", "Eacute", "eacute", "Igrave", "igrave", "Ograve", "ograve", "Oacute", "oacute", "Ugrave", "ugrave"}

                Italian

            <dict>
                <key>glyphNames</key>
                <array>
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Ugrave
                    ugrave
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Eacute", "eacute", "Iacute", "iacute", "Ugrave", "ugrave", "Uacute", "uacute"}

                Kurdish

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Ecaron
                    ecaron
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Racute
                    racute
                    Sacute
                    sacute
                    Scaron
                    scaron
                    Zacute
                    zacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Ecaron", "ecaron", "Lslash", "lslash", "Nacute", "nacute", "Racute", "racute", "Sacute", "sacute", "Scaron", "scaron", "Zacute", "zacute", "Zcaron", "zcaron"}

                Lower Sorbian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Ntilde
                    ntilde
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Adieresis", "adieresis", "Aring", "aring", "Ntilde", "ntilde"}

                Lule Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Aogonek
                    aogonek
                    Ccaron
                    ccaron
                    Eogonek
                    eogonek
                    Edotaccent
                    edotaccent
                    Iogonek
                    iogonek
                    Scaron
                    scaron
                    Uogonek
                    uogonek
                    Umacron
                    umacron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aogonek", "aogonek", "Ccaron", "ccaron", "Eogonek", "eogonek", "Edotaccent", "edotaccent", "Iogonek", "iogonek", "Scaron", "scaron", "Uogonek", "uogonek", "Umacron", "umacron", "Zcaron", "zcaron"}

                Lithuanian

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Eacute
                    eacute
                    Edieresis
                    edieresis
                    Odieresis
                    odieresis
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Eacute", "eacute", "Edieresis", "edieresis", "Odieresis", "odieresis", "Udieresis", "udieresis"}

                Luxembourgish

            <dict>
                <key>glyphNames</key>
                <array>
                    Amacron
                    amacron
                    Ccaron
                    ccaron
                    Emacron
                    emacron
                    Gcommaaccent
                    gcommaaccent
                    Imacron
                    imacron
                    Kcommaaccent
                    kcommaaccent
                    Lcommaaccent
                    lcommaaccent
                    Ncommaaccent
                    ncommaaccent
                    Scaron
                    scaron
                    Umacron
                    umacron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Amacron", "amacron", "Ccaron", "ccaron", "Emacron", "emacron", "Gcommaaccent", "gcommaaccent", "Imacron", "imacron", "Kcommaaccent", "kcommaaccent", "Lcommaaccent", "lcommaaccent", "Ncommaaccent", "ncommaaccent", "Scaron", "scaron", "Umacron", "umacron", "Zcaron", "zcaron"}

                Latvian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    uE010
                    uE011
                    Ocircumflex
                    ocircumflex
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "uE010", "uE011", "Ocircumflex", "ocircumflex"}

                Malagasy

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Abreve
                    abreve
                    Icircumflex
                    icircumflex
                    Scommaaccent
                    scommaaccent
                    Tcommaaccent
                    tcommaaccent
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Abreve", "abreve", "Icircumflex", "icircumflex", "Scommaaccent", "scommaaccent", "Tcommaaccent", "tcommaaccent"}

                Moldavian

            <dict>
                <key>glyphNames</key>
                <array>
                    Amacron
                    amacron
                    Emacron
                    emacron
                    Imacron
                    imacron
                    Omacron
                    omacron
                    Umacron
                    umacron
                </array>
                <key>query</key>
                Name IN {"Amacron", "amacron", "Emacron", "emacron", "Imacron", "imacron", "Omacron", "omacron", "Umacron", "umacron"}

                Maori

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Cdotaccent
                    cdotaccent
                    Egrave
                    egrave
                    Gdotaccent
                    gdotaccent
                    Hbar
                    hbar
                    Igrave
                    igrave
                    Icircumflex
                    icircumflex
                    Ograve
                    ograve
                    Ugrave
                    ugrave
                    Zdotaccent
                    zdotaccent
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Cdotaccent", "cdotaccent", "Egrave", "egrave", "Gdotaccent", "gdotaccent", "Hbar", "hbar", "Igrave", "igrave", "Icircumflex", "icircumflex", "Ograve", "ograve", "Ugrave", "ugrave", "Zdotaccent", "zdotaccent"}

                Maltese

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Iacute
                    iacute
                    Idieresis
                    idieresis
                    IJ
                    ij
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Odieresis
                    odieresis
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Acircumflex", "acircumflex", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Iacute", "iacute", "Idieresis", "idieresis", "IJ", "ij", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Odieresis", "odieresis", "Uacute", "uacute", "Ucircumflex", "ucircumflex"}

                Dutch

            <dict>
                <key>glyphNames</key>
                <array>
                    AE
                    ae
                    Oslash
                    oslash
                    Aring
                    aring
                </array>
                <key>query</key>
                Name IN {"AE", "ae", "Oslash", "oslash", "Aring", "aring"}

                Norwegian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Eng
                    eng
                    Scaron
                    scaron
                    Tbar
                    tbar
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Eng", "eng", "Scaron", "scaron", "Tbar", "tbar", "Zcaron", "zcaron"}

                Northern Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccircumflex
                    ccircumflex
                    Gcircumflex
                    gcircumflex
                    Hcircumflex
                    hcircumflex
                    Jcircumflex
                    jcircumflex
                    Scircumflex
                    scircumflex
                    Ubreve
                    ubreve
                </array>
                <key>query</key>
                Name IN {"Ccircumflex", "ccircumflex", "Gcircumflex", "gcircumflex", "Hcircumflex", "hcircumflex", "Jcircumflex", "jcircumflex", "Scircumflex", "scircumflex", "Ubreve", "ubreve"}

                Esperanto

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Ccedilla
                    ccedilla
                    Eacute
                    eacute
                    Egrave
                    egrave
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Agrave", "agrave", "Ccedilla", "ccedilla", "Eacute", "eacute", "Egrave", "egrave", "Iacute", "iacute", "Oacute", "oacute", "Ograve", "ograve", "Uacute", "uacute"}

                Occitan

            <dict>
                <key>glyphNames</key>
                <array>
                    Ntilde
                    ntilde
                </array>
                <key>query</key>
                Name IN {"Ntilde", "ntilde"}

                Pilipino

            <dict>
                <key>glyphNames</key>
                <array>
                    Aogonek
                    aogonek
                    Cacute
                    cacute
                    Eogonek
                    eogonek
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Oacute
                    oacute
                    Sacute
                    sacute
                    Zacute
                    zacute
                    Zdotaccent
                    zdotaccent
                </array>
                <key>query</key>
                Name IN {"Aogonek", "aogonek", "Cacute", "cacute", "Eogonek", "eogonek", "Lslash", "lslash", "Nacute", "nacute", "Oacute", "oacute", "Sacute", "sacute", "Zacute", "zacute", "Zdotaccent", "zdotaccent"}

                Polish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Ccedilla
                    ccedilla
                    Eacute
                    eacute
                    Egrave
                    egrave
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Agrave", "agrave", "Ccedilla", "ccedilla", "Eacute", "eacute", "Egrave", "egrave", "Iacute", "iacute", "Oacute", "oacute", "Ograve", "ograve", "Uacute", "uacute"}

                Provencal

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Atilde
                    atilde
                    Ccedilla
                    ccedilla
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Otilde
                    otilde
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Acircumflex", "acircumflex", "Atilde", "atilde", "Ccedilla", "ccedilla", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Iacute", "iacute", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Otilde", "otilde", "Uacute", "uacute", "Udieresis", "udieresis"}

                Portuguese

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Igrave
                    igrave
                    Icircumflex
                    icircumflex
                    Ograve
                    ograve
                    Ugrave
                    ugrave
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Egrave", "egrave", "Eacute", "eacute", "Igrave", "igrave", "Icircumflex", "icircumflex", "Ograve", "ograve", "Ugrave", "ugrave"}

                Rhaeto-Romanic

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Abreve
                    abreve
                    Icircumflex
                    icircumflex
                    Scommaaccent
                    scommaaccent
                    Tcommaaccent
                    tcommaaccent
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Abreve", "abreve", "Icircumflex", "icircumflex", "Scommaaccent", "scommaaccent", "Tcommaaccent", "tcommaaccent"}

                Romanian

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccaron
                    Scaron
                    Zcaron
                    ccaron
                    scaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Ccaron", "Scaron", "Zcaron", "ccaron", "scaron", "zcaron"}

                Romany

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Ezh
                    ezh
                    Ezhcaron
                    ezhcaron
                    Gcaron
                    gcaron
                    Gstroke
                    gstroke
                    Kcaron
                    kcaron
                    Eng
                    eng
                    Otilde
                    otilde
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Adieresis", "adieresis", "Aring", "aring", "Ccaron", "ccaron", "Dcroat", "dcroat", "Ezh", "ezh", "Ezhcaron", "ezhcaron", "Gcaron", "gcaron", "Gstroke", "gstroke", "Kcaron", "kcaron", "Eng", "eng", "Otilde", "otilde", "Scaron", "scaron", "Zcaron", "zcaron"}

                Skolt Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Adieresis
                    adieresis
                    Ccaron
                    ccaron
                    Dcaron
                    dcaron
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Lacute
                    lacute
                    Lcaron
                    lcaron
                    Ncaron
                    ncaron
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Racute
                    racute
                    Scaron
                    scaron
                    Tcaron
                    tcaron
                    Uacute
                    uacute
                    Yacute
                    yacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Adieresis", "adieresis", "Ccaron", "ccaron", "Dcaron", "dcaron", "Eacute", "eacute", "Iacute", "iacute", "Lacute", "lacute", "Lcaron", "lcaron", "Ncaron", "ncaron", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Racute", "racute", "Scaron", "scaron", "Tcaron", "tcaron", "Uacute", "uacute", "Yacute", "yacute", "Zcaron", "zcaron"}

                Slovak

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccaron
                    ccaron
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Ccaron", "ccaron", "Scaron", "scaron", "Zcaron", "zcaron"}

                Slovenian

            <dict>
                <key>glyphNames</key>
                <array>
                    Ecircumflex
                    ecircumflex
                    Ocircumflex
                    ocircumflex
                    Scaron
                    scaron
                </array>
                <key>query</key>
                Name IN {"Ecircumflex", "ecircumflex", "Ocircumflex", "ocircumflex", "Scaron", "scaron"}

                Sotho

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccedilla
                    ccedilla
                    Edieresis
                    edieresis
                </array>
                <key>query</key>
                Name IN {"Ccedilla", "ccedilla", "Edieresis", "edieresis"}

                Albanian

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Scaron", "scaron", "Zcaron", "zcaron"}

                Serbian

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Odieresis
                    odieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Aring", "aring", "Odieresis", "odieresis"}

                Southern Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Eacute
                    eacute
                    Odieresis
                    odieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Aring", "aring", "Eacute", "eacute", "Odieresis", "odieresis"}

                Swedish

            <dict>
                <key>glyphNames</key>
                <array>
                    Schwa
                    schwa
                    Ccedilla
                    ccedilla
                    Gbreve
                    gbreve
                    Idotaccent
                    dotlessi
                    uE01A
                    uE01B
                    uE01C
                    uE01D
                    Scedilla
                    scedilla
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Schwa", "schwa", "Ccedilla", "ccedilla", "Gbreve", "gbreve", "Idotaccent", "dotlessi", "uE01A", "uE01B", "uE01C", "uE01D", "Scedilla", "scedilla", "Udieresis", "udieresis"}

                Tatar

            <dict>
                <key>glyphNames</key>
                <array>
                    Zcaron
                    zcaron
                    Yacute
                    yacute
                    Ncaron
                    ncaron
                    Odieresis
                    odieresis
                    Udieresis
                    udieresis
                    Ccedilla
                    ccedilla
                    Scedilla
                    scedilla
                    Adieresis
                    adieresis
                </array>
                <key>query</key>
                Name IN {"Zcaron", "zcaron", "Yacute", "yacute", "Ncaron", "ncaron", "Odieresis", "odieresis", "Udieresis", "udieresis", "Ccedilla", "ccedilla", "Scedilla", "scedilla", "Adieresis", "adieresis"}

                Turkmen

            <dict>
                <key>glyphNames</key>
                <array>
                    Ecircumflex
                    ecircumflex
                    Ocircumflex
                    ocircumflex
                    Scaron
                    scaron
                </array>
                <key>query</key>
                Name IN {"Ecircumflex", "ecircumflex", "Ocircumflex", "ocircumflex", "Scaron", "scaron"}

                Tswana

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Ccedilla
                    ccedilla
                    Gbreve
                    gbreve
                    Icircumflex
                    icircumflex
                    Idotaccent
                    dotlessi
                    Odieresis
                    odieresis
                    Scedilla
                    scedilla
                    Ucircumflex
                    ucircumflex
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Ccedilla", "ccedilla", "Gbreve", "gbreve", "Icircumflex", "icircumflex", "Idotaccent", "dotlessi", "Odieresis", "odieresis", "Scedilla", "scedilla", "Ucircumflex", "ucircumflex", "Udieresis", "udieresis"}

                Turkish

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Ecaron
                    ecaron
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Oacute
                    oacute
                    Rcaron
                    rcaron
                    Scaron
                    scaron
                    Zacute
                    zacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Ecaron", "ecaron", "Lslash", "lslash", "Nacute", "nacute", "Oacute", "oacute", "Rcaron", "rcaron", "Scaron", "scaron", "Zacute", "zacute", "Zcaron", "zcaron"}

                Upper Sorbian

            <dict>
                <key>glyphNames</key>
                <array>
                    uE012
                    uE013
                    uE014
                    uE015
                </array>
                <key>query</key>
                Name IN {"uE012", "uE013", "uE014", "uE015"}

                Uzbek

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Acircumflexgrave
                    acircumflexgrave
                    Acircumflexacute
                    acircumflexacute
                    Acircumflextilde
                    acircumflextilde
                    Acircumflexhookabove
                    acircumflexhookabove
                    Acircumflexdotbelow
                    acircumflexdotbelow
                    Atilde
                    atilde
                    Abreve
                    abreve
                    Abrevegrave
                    abrevegrave
                    Abreveacute
                    abreveacute
                    Abrevetilde
                    abrevetilde
                    Abrevehookabove
                    abrevehookabove
                    Abrevedotbelow
                    abrevedotbelow
                    Ahookabove
                    ahookabove
                    Adotbelow
                    adotbelow
                    Dcroat
                    dcroat
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Ecircumflexgrave
                    ecircumflexgrave
                    Ecircumflexacute
                    ecircumflexacute
                    Ecircumflextilde
                    ecircumflextilde
                    Ecircumflexhookabove
                    ecircumflexhookabove
                    Ecircumflexdotbelow
                    ecircumflexdotbelow
                    Etilde
                    etilde
                    Ehookabove
                    ehookabove
                    Edotbelow
                    edotbelow
                    Igrave
                    igrave
                    Iacute
                    iacute
                    Itilde
                    itilde
                    Ihookabove
                    ihookabove
                    Idotbelow
                    idotbelow
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Ocircumflexgrave
                    ocircumflexgrave
                    Ocircumflexacute
                    ocircumflexacute
                    Ocircumflextilde
                    ocircumflextilde
                    Ocircumflexhookabove
                    ocircumflexhookabove
                    Ocircumflexdotbelow
                    ocircumflexdotbelow
                    Otilde
                    otilde
                    Ohookabove
                    ohookabove
                    Ohorn
                    ohorn
                    Ohorngrave
                    ohorngrave
                    Ohornacute
                    ohornacute
                    Ohorntilde
                    ohorntilde
                    Ohornhookabove
                    ohornhookabove
                    Ohorndotbelow
                    ohorndotbelow
                    Odotbelow
                    odotbelow
                    Ugrave
                    ugrave
                    Uacute
                    uacute
                    Utilde
                    utilde
                    Uhookabove
                    uhookabove
                    Uhorn
                    uhorn
                    Uhorngrave
                    uhorngrave
                    Uhornacute
                    uhornacute
                    Uhorntilde
                    uhorntilde
                    Uhornhookabove
                    uhornhookabove
                    Uhorndotbelow
                    uhorndotbelow
                    Udotbelow
                    udotbelow
                    Ygrave
                    ygrave
                    Yacute
                    yacute
                    Ytilde
                    ytilde
                    Yhookabove
                    yhookabove
                    Ydotbelow
                    ydotbelow
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Acircumflex", "acircumflex", "Acircumflexgrave", "acircumflexgrave", "Acircumflexacute", "acircumflexacute", "Acircumflextilde", "acircumflextilde", "Acircumflexhookabove", "acircumflexhookabove", "Acircumflexdotbelow", "acircumflexdotbelow", "Atilde", "atilde", "Abreve", "abreve", "Abrevegrave", "abrevegrave", "Abreveacute", "abreveacute", "Abrevetilde", "abrevetilde", "Abrevehookabove", "abrevehookabove", "Abrevedotbelow", "abrevedotbelow", "Ahookabove", "ahookabove", "Adotbelow", "adotbelow", "Dcroat", "dcroat", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Ecircumflexgrave", "ecircumflexgrave", "Ecircumflexacute", "ecircumflexacute", "Ecircumflextilde", "ecircumflextilde", "Ecircumflexhookabove", "ecircumflexhookabove", "Ecircumflexdotbelow", "ecircumflexdotbelow", "Etilde", "etilde", "Ehookabove", "ehookabove", "Edotbelow", "edotbelow", "Igrave", "igrave", "Iacute", "iacute", "Itilde", "itilde", "Ihookabove", "ihookabove", "Idotbelow", "idotbelow", "Ograve", "ograve", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Ocircumflexgrave", "ocircumflexgrave", "Ocircumflexacute", "ocircumflexacute", "Ocircumflextilde", "ocircumflextilde", "Ocircumflexhookabove", "ocircumflexhookabove", "Ocircumflexdotbelow", "ocircumflexdotbelow", "Otilde", "otilde", "Ohookabove", "ohookabove", "Ohorn", "ohorn", "Ohorngrave", "ohorngrave", "Ohornacute", "ohornacute", "Ohorntilde", "ohorntilde", "Ohornhookabove", "ohornhookabove", "Ohorndotbelow", "ohorndotbelow", "Odotbelow", "odotbelow", "Ugrave", "ugrave", "Uacute", "uacute", "Utilde", "utilde", "Uhookabove", "uhookabove", "Uhorn", "uhorn", "Uhorngrave", "uhorngrave", "Uhornacute", "uhornacute", "Uhorntilde", "uhorntilde", "Uhornhookabove", "uhornhookabove", "Uhorndotbelow", "uhorndotbelow", "Udotbelow", "udotbelow", "Ygrave", "ygrave", "Yacute", "yacute", "Ytilde", "ytilde", "Yhookabove", "yhookabove", "Ydotbelow", "ydotbelow"}

                Vietnamese

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Acircumflex
                    acircumflex
                    Adieresis
                    adieresis
                    Eacute
                    eacute
                    Egrave
                    egrave
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Iacute
                    iacute
                    Igrave
                    igrave
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Ocircumflex
                    ocircumflex
                    Odieresis
                    odieresis
                    Uacute
                    uacute
                    Ugrave
                    ugrave
                    Ucircumflex
                    ucircumflex
                    Udieresis
                    udieresis
                    Yacute
                    yacute
                    Ygrave
                    ygrave
                    Ycircumflex
                    ycircumflex
                    Ydieresis
                    ydieresis
                    Wcircumflex
                    wcircumflex
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Agrave", "agrave", "Acircumflex", "acircumflex", "Adieresis", "adieresis", "Eacute", "eacute", "Egrave", "egrave", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Iacute", "iacute", "Igrave", "igrave", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Oacute", "oacute", "Ograve", "ograve", "Ocircumflex", "ocircumflex", "Odieresis", "odieresis", "Uacute", "uacute", "Ugrave", "ugrave", "Ucircumflex", "ucircumflex", "Udieresis", "udieresis", "Yacute", "yacute", "Ygrave", "ygrave", "Ycircumflex", "ycircumflex", "Ydieresis", "ydieresis", "Wcircumflex", "wcircumflex"}

                Welsh

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Atilde
                    atilde
                    Eacute
                    eacute
                    Edieresis
                    edieresis
                    Ntilde
                    ntilde
                    Eng
                    eng
                    Oacute
                    oacute
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Atilde", "atilde", "Eacute", "eacute", "Edieresis", "edieresis", "Ntilde", "ntilde", "Eng", "eng", "Oacute", "oacute"}

                Wolof

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Acaron
                    acaron
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Ecaron
                    ecaron
                    Edotbelow
                    edotbelow
                    Igrave
                    igrave
                    Iacute
                    iacute
                    Icircumflex
                    icircumflex
                    Icaron
                    icaron
                    uE000
                    uE001
                    Nacute
                    nacute
                    uE00C
                    uE00D
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Ocaron
                    ocaron
                    Odotbelow
                    odotbelow
                    Sdotbelow
                    sdotbelow
                    Ugrave
                    ugrave
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                    Ucaron
                    ucaron
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Acircumflex", "acircumflex", "Acaron", "acaron", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Ecaron", "ecaron", "Edotbelow", "edotbelow", "Igrave", "igrave", "Iacute", "iacute", "Icircumflex", "icircumflex", "Icaron", "icaron", "uE000", "uE001", "Nacute", "nacute", "uE00C", "uE00D", "Ograve", "ograve", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Ocaron", "ocaron", "Odotbelow", "odotbelow", "Sdotbelow", "sdotbelow", "Ugrave", "ugrave", "Uacute", "uacute", "Ucircumflex", "ucircumflex", "Ucaron", "ucaron"}

                Yoruba

        </array>
        <key>query</key>


        Lang Support (Req)

        140627487105360

    <dict>
        <key>group</key>
        <array>
            <dict>
                <key>glyphNames</key>
                <array>
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Ocircumflex
                    ocircumflex
                    Ucircumflex
                </array>
                <key>query</key>
                Name IN {"Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Ocircumflex", "ocircumflex", "Ucircumflex"}

                Afrikaans

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccedilla
                    ccedilla
                    Schwa
                    schwa
                    Gbreve
                    gbreve
                    Idotaccent
                    dotlessi
                    Odieresis
                    odieresis
                    Scedilla
                    scedilla
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Ccedilla", "ccedilla", "Schwa", "schwa", "Gbreve", "gbreve", "Idotaccent", "dotlessi", "Odieresis", "odieresis", "Scedilla", "scedilla", "Udieresis", "udieresis"}

                Azeri

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Sacute
                    sacute
                    Scaron
                    scaron
                    Ubreve
                    ubreve
                    Zacute
                    zacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Lslash", "lslash", "Nacute", "nacute", "Sacute", "sacute", "Scaron", "scaron", "Ubreve", "ubreve", "Zacute", "zacute", "Zcaron", "zcaron"}

                Belarussian

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Scaron", "scaron", "Zcaron", "zcaron"}

                Bosnian

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Ecircumflex
                    ecircumflex
                    Ntilde
                    ntilde
                    Ocircumflex
                    ocircumflex
                    Ugrave
                    ugrave
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Ecircumflex", "ecircumflex", "Ntilde", "ntilde", "Ocircumflex", "ocircumflex", "Ugrave", "ugrave", "Udieresis", "udieresis"}

                Breton

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Ccedilla
                    ccedilla
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Idieresis
                    idieresis
                    Ldot
                    ldot
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                    Ntilde
                    ntilde
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Ccedilla", "ccedilla", "Egrave", "egrave", "Eacute", "eacute", "Iacute", "iacute", "Idieresis", "idieresis", "Ldot", "ldot", "Ograve", "ograve", "Oacute", "oacute", "Uacute", "uacute", "Udieresis", "udieresis", "Ntilde", "ntilde"}

                Catalan

            <dict>
                <key>glyphNames</key>
                <array>
                    Wcircumflex
                    wcircumflex
                </array>
                <key>query</key>
                Name IN {"Wcircumflex", "wcircumflex"}

                Chichewa

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Ccaron
                    ccaron
                    Dcaron
                    dcaron
                    Eacute
                    eacute
                    Ecaron
                    ecaron
                    Iacute
                    iacute
                    Ncaron
                    ncaron
                    Oacute
                    oacute
                    Rcaron
                    rcaron
                    Scaron
                    scaron
                    Tcaron
                    tcaron
                    Uacute
                    uacute
                    Uring
                    uring
                    Yacute
                    yacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Ccaron", "ccaron", "Dcaron", "dcaron", "Eacute", "eacute", "Ecaron", "ecaron", "Iacute", "iacute", "Ncaron", "ncaron", "Oacute", "oacute", "Rcaron", "rcaron", "Scaron", "scaron", "Tcaron", "tcaron", "Uacute", "uacute", "Uring", "uring", "Yacute", "yacute", "Zcaron", "zcaron"}

                Czech

            <dict>
                <key>glyphNames</key>
                <array>
                    Aring
                    aring
                    AE
                    ae
                    Eacute
                    eacute
                    Oslash
                    oslash
                    Aacute
                    aacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Yacute
                    yacute
                </array>
                <key>query</key>
                Name IN {"Aring", "aring", "AE", "ae", "Eacute", "eacute", "Oslash", "oslash", "Aacute", "aacute", "Iacute", "iacute", "Oacute", "oacute", "Uacute", "uacute", "Yacute", "yacute"}

                Danish

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Odieresis
                    odieresis
                    germandbls
                    Udieresis
                    udieresis
                    Agrave
                    agrave
                    Eacute
                    eacute
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Odieresis", "odieresis", "germandbls", "Udieresis", "udieresis", "Agrave", "agrave", "Eacute", "eacute"}

                German

            <dict>
                <key>glyphNames</key>
                <array>
                    AE
                    ae
                    Ccedilla
                    ccedilla
                    Idieresis
                    idieresis
                    Ocircumflex
                    ocircumflex
                </array>
                <key>query</key>
                Name IN {"AE", "ae", "Ccedilla", "ccedilla", "Idieresis", "idieresis", "Ocircumflex", "ocircumflex"}

                English

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Ntilde
                    ntilde
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                    Ccedilla
                    ccedilla
                    Idieresis
                    idieresis
                    ordfeminine
                    ordmasculine
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Ntilde", "ntilde", "Oacute", "oacute", "Uacute", "uacute", "Udieresis", "udieresis", "Ccedilla", "ccedilla", "Idieresis", "idieresis", "ordfeminine", "ordmasculine"}

                Spanish

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Otilde
                    otilde
                    Odieresis
                    odieresis
                    Scaron
                    scaron
                    Udieresis
                    udieresis
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Otilde", "otilde", "Odieresis", "odieresis", "Scaron", "scaron", "Udieresis", "udieresis", "Zcaron", "zcaron"}

                Estonian

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccedilla
                    ccedilla
                    Ntilde
                    ntilde
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Ccedilla", "ccedilla", "Ntilde", "ntilde", "Udieresis", "udieresis"}

                Basque

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Odieresis
                    odieresis
                    Aring
                    aring
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Odieresis", "odieresis", "Aring", "aring", "Scaron", "scaron", "Zcaron", "zcaron"}

                Finnish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Iacute
                    iacute
                    Idieresis
                    idieresis
                    IJ
                    ij
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Odieresis
                    odieresis
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                    Adieresis
                    adieresis
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Acircumflex", "acircumflex", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Iacute", "iacute", "Idieresis", "idieresis", "IJ", "ij", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Odieresis", "odieresis", "Uacute", "uacute", "Ucircumflex", "ucircumflex", "Adieresis", "adieresis", "Udieresis", "udieresis"}

                Flemish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    AE
                    ae
                    Eth
                    eth
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Oslash
                    oslash
                    Uacute
                    uacute
                    Yacute
                    yacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "AE", "ae", "Eth", "eth", "Iacute", "iacute", "Oacute", "oacute", "Oslash", "oslash", "Uacute", "uacute", "Yacute", "yacute"}

                Faroese

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Acircumflex
                    acircumflex
                    Ccedilla
                    ccedilla
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Ocircumflex
                    ocircumflex
                    OE
                    oe
                    Ugrave
                    ugrave
                    Ucircumflex
                    ucircumflex
                    Udieresis
                    udieresis
                    Ydieresis
                    ydieresis
                    AE
                    ae
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Acircumflex", "acircumflex", "Ccedilla", "ccedilla", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Ocircumflex", "ocircumflex", "OE", "oe", "Ugrave", "ugrave", "Ucircumflex", "ucircumflex", "Udieresis", "udieresis", "Ydieresis", "ydieresis", "AE", "ae"}

                French

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Ecircumflex
                    ecircumflex
                    Icircumflex
                    icircumflex
                    Ocircumflex
                    ocircumflex
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                    Eacute
                    eacute
                    Adieresis
                    adieresis
                    Edieresis
                    edieresis
                    Idieresis
                    idieresis
                    Odieresis
                    odieresis
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Ecircumflex", "ecircumflex", "Icircumflex", "icircumflex", "Ocircumflex", "ocircumflex", "Uacute", "uacute", "Ucircumflex", "ucircumflex", "Eacute", "eacute", "Adieresis", "adieresis", "Edieresis", "edieresis", "Idieresis", "idieresis", "Odieresis", "odieresis", "Udieresis", "udieresis"}

                Frisian

            <dict>
                <key>glyphNames</key>
                <array>
                    Bhook
                    bhook
                    Dhook
                    dhook
                    Eng
                    eng
                    nhookleft
                </array>
                <key>query</key>
                Name IN {"Bhook", "bhook", "Dhook", "dhook", "Eng", "eng", "nhookleft"}

                Fulani

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Igrave
                    igrave
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ugrave
                    ugrave
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Egrave", "egrave", "Eacute", "eacute", "Igrave", "igrave", "Ograve", "ograve", "Oacute", "oacute", "Ugrave", "ugrave"}

                Gaelic

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Ntilde
                    ntilde
                    Oacute
                    oacute
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Ntilde", "ntilde", "Oacute", "oacute", "Uacute", "uacute", "Udieresis", "udieresis"}

                Galician

            <dict>
                <key>glyphNames</key>
                <array>
                    Aring
                    aring
                    AE
                    ae
                    Oslash
                    oslash
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Atilde
                    atilde
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Iacute
                    iacute
                    Icircumflex
                    icircumflex
                    Itilde
                    itilde
                    kgreenlandic
                    Ocircumflex
                    ocircumflex
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                    Utilde
                    utilde
                </array>
                <key>query</key>
                Name IN {"Aring", "aring", "AE", "ae", "Oslash", "oslash", "Aacute", "aacute", "Acircumflex", "acircumflex", "Atilde", "atilde", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Iacute", "iacute", "Icircumflex", "icircumflex", "Itilde", "itilde", "kgreenlandic", "Ocircumflex", "ocircumflex", "Uacute", "uacute", "Ucircumflex", "ucircumflex", "Utilde", "utilde"}

                Greenlandic

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    atilde
                    Eacute
                    eacute
                    etilde
                    uE005
                    Iacute
                    iacute
                    itilde
                    Ntilde
                    ntilde
                    Oacute
                    oacute
                    otilde
                    Uacute
                    uacute
                    utilde
                    ytilde
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "atilde", "Eacute", "eacute", "etilde", "uE005", "Iacute", "iacute", "itilde", "Ntilde", "ntilde", "Oacute", "oacute", "otilde", "Uacute", "uacute", "utilde", "ytilde"}

                Guarani

            <dict>
                <key>glyphNames</key>
                <array>
                    Bhook
                    bhook
                    Dhook
                    dhook
                </array>
                <key>query</key>
                Name IN {"Bhook", "bhook", "Dhook", "dhook"}

                Hausa

            <dict>
                <key>glyphNames</key>
                <array>
                    Amacron
                    amacron
                    Emacron
                    emacron
                    Imacron
                    imacron
                    Omacron
                    omacron
                    Umacron
                    umacron
                </array>
                <key>query</key>
                Name IN {"Amacron", "amacron", "Emacron", "emacron", "Imacron", "imacron", "Omacron", "omacron", "Umacron", "umacron"}

                Hawaiian

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Scaron", "scaron", "Zcaron", "zcaron"}

                Croatian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Odieresis
                    odieresis
                    Ohungarumlaut
                    ohungarumlaut
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                    Uhungarumlaut
                    uhungarumlaut
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Oacute", "oacute", "Odieresis", "odieresis", "Ohungarumlaut", "ohungarumlaut", "Uacute", "uacute", "Udieresis", "udieresis", "Uhungarumlaut", "uhungarumlaut"}

                Hungarian

            <dict>
                <key>glyphNames</key>
                <array>
                    Idotbelow
                    idotbelow
                    Odotbelow
                    odotbelow
                    Udotbelow
                    udotbelow
                </array>
                <key>query</key>
                Name IN {"Idotbelow", "idotbelow", "Odotbelow", "odotbelow", "Udotbelow", "udotbelow"}

                Igbo

            <dict>
                <key>glyphNames</key>
                <array>
                    Eacute
                    eacute
                </array>
                <key>query</key>
                Name IN {"Eacute", "eacute"}

                Indonesian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Eacute", "eacute", "Iacute", "iacute", "Oacute", "oacute", "Uacute", "uacute"}

                Irish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    AE
                    ae
                    Eth
                    eth
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Odieresis
                    odieresis
                    Thorn
                    thorn
                    Uacute
                    uacute
                    Yacute
                    yacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "AE", "ae", "Eth", "eth", "Eacute", "eacute", "Iacute", "iacute", "Oacute", "oacute", "Odieresis", "odieresis", "Thorn", "thorn", "Uacute", "uacute", "Yacute", "yacute"}

                Icelandic

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Adieresis
                    adieresis
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Eng
                    eng
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Acircumflex", "acircumflex", "Adieresis", "adieresis", "Ccaron", "ccaron", "Dcroat", "dcroat", "Eng", "eng", "Scaron", "scaron", "Zcaron", "zcaron"}

                Inari Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Igrave
                    igrave
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ugrave
                    ugrave
                    Aacute
                    aacute
                    Iacute
                    iacute
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Egrave", "egrave", "Eacute", "eacute", "Igrave", "igrave", "Ograve", "ograve", "Oacute", "oacute", "Ugrave", "ugrave", "Aacute", "aacute", "Iacute", "iacute", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Uacute", "uacute"}

                Italian

            <dict>
                <key>glyphNames</key>
                <array>
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Ugrave
                    ugrave
                    Uacute
                    uacute
                    Ccedilla
                    ccedilla
                    Ecircumflex
                    ecircumflex
                    Icircumflex
                    icircumflex
                    Scedilla
                    scedilla
                    Ucircumflex
                    ucircumflex
                </array>
                <key>query</key>
                Name IN {"Eacute", "eacute", "Iacute", "iacute", "Ugrave", "ugrave", "Uacute", "uacute", "Ccedilla", "ccedilla", "Ecircumflex", "ecircumflex", "Icircumflex", "icircumflex", "Scedilla", "scedilla", "Ucircumflex", "ucircumflex"}

                Kurdish

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Ecaron
                    ecaron
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Racute
                    racute
                    Sacute
                    sacute
                    Scaron
                    scaron
                    Zacute
                    zacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Ecaron", "ecaron", "Lslash", "lslash", "Nacute", "nacute", "Racute", "racute", "Sacute", "sacute", "Scaron", "scaron", "Zacute", "zacute", "Zcaron", "zcaron"}

                Lower Sorbian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Ntilde
                    ntilde
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Adieresis", "adieresis", "Aring", "aring", "Ntilde", "ntilde"}

                Lule Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Aogonek
                    aogonek
                    Ccaron
                    ccaron
                    Eogonek
                    eogonek
                    Edotaccent
                    edotaccent
                    Iogonek
                    iogonek
                    Scaron
                    scaron
                    Uogonek
                    uogonek
                    Umacron
                    umacron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aogonek", "aogonek", "Ccaron", "ccaron", "Eogonek", "eogonek", "Edotaccent", "edotaccent", "Iogonek", "iogonek", "Scaron", "scaron", "Uogonek", "uogonek", "Umacron", "umacron", "Zcaron", "zcaron"}

                Lithuanian

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Eacute
                    eacute
                    Edieresis
                    edieresis
                    Odieresis
                    odieresis
                    Udieresis
                    udieresis
                    Acircumflex
                    acircumflex
                    Egrave
                    egrave
                    Ecircumflex
                    ecircumflex
                    Icircumflex
                    icircumflex
                    Ocircumflex
                    ocircumflex
                    Ucircumflex
                    ucircumflex
                    germandbls
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Eacute", "eacute", "Edieresis", "edieresis", "Odieresis", "odieresis", "Udieresis", "udieresis", "Acircumflex", "acircumflex", "Egrave", "egrave", "Ecircumflex", "ecircumflex", "Icircumflex", "icircumflex", "Ocircumflex", "ocircumflex", "Ucircumflex", "ucircumflex", "germandbls"}

                Luxembourgish

            <dict>
                <key>glyphNames</key>
                <array>
                    Amacron
                    amacron
                    Ccaron
                    ccaron
                    Emacron
                    emacron
                    Gcommaaccent
                    gcommaaccent
                    Imacron
                    imacron
                    Kcommaaccent
                    kcommaaccent
                    Lcommaaccent
                    lcommaaccent
                    Ncommaaccent
                    ncommaaccent
                    Scaron
                    scaron
                    Umacron
                    umacron
                    Zcaron
                    zcaron
                    Omacron
                    omacron
                    Rcommaaccent
                    rcommaaccent
                </array>
                <key>query</key>
                Name IN {"Amacron", "amacron", "Ccaron", "ccaron", "Emacron", "emacron", "Gcommaaccent", "gcommaaccent", "Imacron", "imacron", "Kcommaaccent", "kcommaaccent", "Lcommaaccent", "lcommaaccent", "Ncommaaccent", "ncommaaccent", "Scaron", "scaron", "Umacron", "umacron", "Zcaron", "zcaron", "Omacron", "omacron", "Rcommaaccent", "rcommaaccent"}

                Latvian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    uE010
                    uE011
                    Ocircumflex
                    ocircumflex
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "uE010", "uE011", "Ocircumflex", "ocircumflex"}

                Malagasy

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Abreve
                    abreve
                    Icircumflex
                    icircumflex
                    Scommaaccent
                    scommaaccent
                    Tcommaaccent
                    tcommaaccent
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Abreve", "abreve", "Icircumflex", "icircumflex", "Scommaaccent", "scommaaccent", "Tcommaaccent", "tcommaaccent"}

                Moldavian

            <dict>
                <key>glyphNames</key>
                <array>
                    Amacron
                    amacron
                    Emacron
                    emacron
                    Imacron
                    imacron
                    Omacron
                    omacron
                    Umacron
                    umacron
                </array>
                <key>query</key>
                Name IN {"Amacron", "amacron", "Emacron", "emacron", "Imacron", "imacron", "Omacron", "omacron", "Umacron", "umacron"}

                Maori

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Cdotaccent
                    cdotaccent
                    Egrave
                    egrave
                    Gdotaccent
                    gdotaccent
                    Hbar
                    hbar
                    Igrave
                    igrave
                    Icircumflex
                    icircumflex
                    Ograve
                    ograve
                    Ugrave
                    ugrave
                    Zdotaccent
                    zdotaccent
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Cdotaccent", "cdotaccent", "Egrave", "egrave", "Gdotaccent", "gdotaccent", "Hbar", "hbar", "Igrave", "igrave", "Icircumflex", "icircumflex", "Ograve", "ograve", "Ugrave", "ugrave", "Zdotaccent", "zdotaccent"}

                Maltese

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Iacute
                    iacute
                    Idieresis
                    idieresis
                    IJ
                    ij
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Odieresis
                    odieresis
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                    Adieresis
                    adieresis
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Acircumflex", "acircumflex", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Iacute", "iacute", "Idieresis", "idieresis", "IJ", "ij", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Odieresis", "odieresis", "Uacute", "uacute", "Ucircumflex", "ucircumflex", "Adieresis", "adieresis", "Udieresis", "udieresis"}

                Dutch

            <dict>
                <key>glyphNames</key>
                <array>
                    AE
                    ae
                    Oslash
                    oslash
                    Aring
                    aring
                    Agrave
                    agrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Ocircumflex
                    ocircumflex
                </array>
                <key>query</key>
                Name IN {"AE", "ae", "Oslash", "oslash", "Aring", "aring", "Agrave", "agrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Oacute", "oacute", "Ograve", "ograve", "Ocircumflex", "ocircumflex"}

                Norwegian

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Eng
                    eng
                    Scaron
                    scaron
                    Tbar
                    tbar
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Eng", "eng", "Scaron", "scaron", "Tbar", "tbar", "Zcaron", "zcaron"}

                Northern Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccircumflex
                    ccircumflex
                    Gcircumflex
                    gcircumflex
                    Hcircumflex
                    hcircumflex
                    Jcircumflex
                    jcircumflex
                    Scircumflex
                    scircumflex
                    Ubreve
                    ubreve
                </array>
                <key>query</key>
                Name IN {"Ccircumflex", "ccircumflex", "Gcircumflex", "gcircumflex", "Hcircumflex", "hcircumflex", "Jcircumflex", "jcircumflex", "Scircumflex", "scircumflex", "Ubreve", "ubreve"}

                Esperanto

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Ccedilla
                    ccedilla
                    Eacute
                    eacute
                    Egrave
                    egrave
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Agrave", "agrave", "Ccedilla", "ccedilla", "Eacute", "eacute", "Egrave", "egrave", "Iacute", "iacute", "Oacute", "oacute", "Ograve", "ograve", "Uacute", "uacute"}

                Occitan

            <dict>
                <key>glyphNames</key>
                <array>
                    Ntilde
                    ntilde
                </array>
                <key>query</key>
                Name IN {"Ntilde", "ntilde"}

                Pilipino

            <dict>
                <key>glyphNames</key>
                <array>
                    Aogonek
                    aogonek
                    Cacute
                    cacute
                    Eogonek
                    eogonek
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Oacute
                    oacute
                    Sacute
                    sacute
                    Zacute
                    zacute
                    Zdotaccent
                    zdotaccent
                </array>
                <key>query</key>
                Name IN {"Aogonek", "aogonek", "Cacute", "cacute", "Eogonek", "eogonek", "Lslash", "lslash", "Nacute", "nacute", "Oacute", "oacute", "Sacute", "sacute", "Zacute", "zacute", "Zdotaccent", "zdotaccent"}

                Polish

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Ccedilla
                    ccedilla
                    Eacute
                    eacute
                    Egrave
                    egrave
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Uacute
                    uacute
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Agrave", "agrave", "Ccedilla", "ccedilla", "Eacute", "eacute", "Egrave", "egrave", "Iacute", "iacute", "Oacute", "oacute", "Ograve", "ograve", "Uacute", "uacute"}

                Provencal

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Atilde
                    atilde
                    Ccedilla
                    ccedilla
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Iacute
                    iacute
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Otilde
                    otilde
                    Uacute
                    uacute
                    Udieresis
                    udieresis
                    ordfeminine
                    ordmasculine
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Acircumflex", "acircumflex", "Atilde", "atilde", "Ccedilla", "ccedilla", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Iacute", "iacute", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Otilde", "otilde", "Uacute", "uacute", "Udieresis", "udieresis", "ordfeminine", "ordmasculine"}

                Portuguese

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Igrave
                    igrave
                    Icircumflex
                    icircumflex
                    Ograve
                    ograve
                    Ugrave
                    ugrave
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Egrave", "egrave", "Eacute", "eacute", "Igrave", "igrave", "Icircumflex", "icircumflex", "Ograve", "ograve", "Ugrave", "ugrave"}

                Rhaeto-Romanic

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Abreve
                    abreve
                    Icircumflex
                    icircumflex
                    Scommaaccent
                    scommaaccent
                    Tcommaaccent
                    tcommaaccent
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Abreve", "abreve", "Icircumflex", "icircumflex", "Scommaaccent", "scommaaccent", "Tcommaaccent", "tcommaaccent"}

                Romanian

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccaron
                    Scaron
                    Zcaron
                    ccaron
                    scaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Ccaron", "Scaron", "Zcaron", "ccaron", "scaron", "zcaron"}

                Romany

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Ezh
                    ezh
                    Ezhcaron
                    ezhcaron
                    Gcaron
                    gcaron
                    Gstroke
                    gstroke
                    Kcaron
                    kcaron
                    Eng
                    eng
                    Otilde
                    otilde
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Adieresis", "adieresis", "Aring", "aring", "Ccaron", "ccaron", "Dcroat", "dcroat", "Ezh", "ezh", "Ezhcaron", "ezhcaron", "Gcaron", "gcaron", "Gstroke", "gstroke", "Kcaron", "kcaron", "Eng", "eng", "Otilde", "otilde", "Scaron", "scaron", "Zcaron", "zcaron"}

                Skolt Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Adieresis
                    adieresis
                    Ccaron
                    ccaron
                    Dcaron
                    dcaron
                    Eacute
                    eacute
                    Iacute
                    iacute
                    Lacute
                    lacute
                    Lcaron
                    lcaron
                    Ncaron
                    ncaron
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Racute
                    racute
                    Scaron
                    scaron
                    Tcaron
                    tcaron
                    Uacute
                    uacute
                    Yacute
                    yacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Adieresis", "adieresis", "Ccaron", "ccaron", "Dcaron", "dcaron", "Eacute", "eacute", "Iacute", "iacute", "Lacute", "lacute", "Lcaron", "lcaron", "Ncaron", "ncaron", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Racute", "racute", "Scaron", "scaron", "Tcaron", "tcaron", "Uacute", "uacute", "Yacute", "yacute", "Zcaron", "zcaron"}

                Slovak

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccaron
                    ccaron
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                    Cacute
                    cacute
                    Dcroat
                    dcroat
                    Adieresis
                    adieresis
                    Odieresis
                    odieresis
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Ccaron", "ccaron", "Scaron", "scaron", "Zcaron", "zcaron", "Cacute", "cacute", "Dcroat", "dcroat", "Adieresis", "adieresis", "Odieresis", "odieresis", "Udieresis", "udieresis"}

                Slovenian

            <dict>
                <key>glyphNames</key>
                <array>
                    Ecircumflex
                    ecircumflex
                    Ocircumflex
                    ocircumflex
                    Scaron
                    scaron
                </array>
                <key>query</key>
                Name IN {"Ecircumflex", "ecircumflex", "Ocircumflex", "ocircumflex", "Scaron", "scaron"}

                Sotho

            <dict>
                <key>glyphNames</key>
                <array>
                    Ccedilla
                    ccedilla
                    Edieresis
                    edieresis
                </array>
                <key>query</key>
                Name IN {"Ccedilla", "ccedilla", "Edieresis", "edieresis"}

                Albanian

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Dcroat
                    dcroat
                    Scaron
                    scaron
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Dcroat", "dcroat", "Scaron", "scaron", "Zcaron", "zcaron"}

                Serbian

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Odieresis
                    odieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Aring", "aring", "Odieresis", "odieresis"}

                Southern Sami

            <dict>
                <key>glyphNames</key>
                <array>
                    Adieresis
                    adieresis
                    Aring
                    aring
                    Eacute
                    eacute
                    Odieresis
                    odieresis
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Edieresis
                    edieresis
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Adieresis", "adieresis", "Aring", "aring", "Eacute", "eacute", "Odieresis", "odieresis", "Aacute", "aacute", "Agrave", "agrave", "Edieresis", "edieresis", "Udieresis", "udieresis"}

                Swedish

            <dict>
                <key>glyphNames</key>
                <array>
                    Schwa
                    schwa
                    Ccedilla
                    ccedilla
                    Gbreve
                    gbreve
                    Idotaccent
                    dotlessi
                    uE01A
                    uE01B
                    uE01C
                    uE01D
                    Scedilla
                    scedilla
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Schwa", "schwa", "Ccedilla", "ccedilla", "Gbreve", "gbreve", "Idotaccent", "dotlessi", "uE01A", "uE01B", "uE01C", "uE01D", "Scedilla", "scedilla", "Udieresis", "udieresis"}

                Tatar

            <dict>
                <key>glyphNames</key>
                <array>
                    Zcaron
                    zcaron
                    Yacute
                    yacute
                    Ncaron
                    ncaron
                    Odieresis
                    odieresis
                    Udieresis
                    udieresis
                    Ccedilla
                    ccedilla
                    Scedilla
                    scedilla
                    Adieresis
                    adieresis
                </array>
                <key>query</key>
                Name IN {"Zcaron", "zcaron", "Yacute", "yacute", "Ncaron", "ncaron", "Odieresis", "odieresis", "Udieresis", "udieresis", "Ccedilla", "ccedilla", "Scedilla", "scedilla", "Adieresis", "adieresis"}

                Turkmen

            <dict>
                <key>glyphNames</key>
                <array>
                    Ecircumflex
                    ecircumflex
                    Ocircumflex
                    ocircumflex
                    Scaron
                    scaron
                </array>
                <key>query</key>
                Name IN {"Ecircumflex", "ecircumflex", "Ocircumflex", "ocircumflex", "Scaron", "scaron"}

                Tswana

            <dict>
                <key>glyphNames</key>
                <array>
                    Acircumflex
                    acircumflex
                    Ccedilla
                    ccedilla
                    Gbreve
                    gbreve
                    Icircumflex
                    icircumflex
                    Idotaccent
                    dotlessi
                    Odieresis
                    odieresis
                    Scedilla
                    scedilla
                    Ucircumflex
                    ucircumflex
                    Udieresis
                    udieresis
                </array>
                <key>query</key>
                Name IN {"Acircumflex", "acircumflex", "Ccedilla", "ccedilla", "Gbreve", "gbreve", "Icircumflex", "icircumflex", "Idotaccent", "dotlessi", "Odieresis", "odieresis", "Scedilla", "scedilla", "Ucircumflex", "ucircumflex", "Udieresis", "udieresis"}

                Turkish

            <dict>
                <key>glyphNames</key>
                <array>
                    Cacute
                    cacute
                    Ccaron
                    ccaron
                    Ecaron
                    ecaron
                    Lslash
                    lslash
                    Nacute
                    nacute
                    Oacute
                    oacute
                    Rcaron
                    rcaron
                    Scaron
                    scaron
                    Zacute
                    zacute
                    Zcaron
                    zcaron
                </array>
                <key>query</key>
                Name IN {"Cacute", "cacute", "Ccaron", "ccaron", "Ecaron", "ecaron", "Lslash", "lslash", "Nacute", "nacute", "Oacute", "oacute", "Rcaron", "rcaron", "Scaron", "scaron", "Zacute", "zacute", "Zcaron", "zcaron"}

                Upper Sorbian

            <dict>
                <key>glyphNames</key>
                <array>
                    uE012
                    uE013
                    uE014
                    uE015
                </array>
                <key>query</key>
                Name IN {"uE012", "uE013", "uE014", "uE015"}

                Uzbek

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Acircumflexgrave
                    acircumflexgrave
                    Acircumflexacute
                    acircumflexacute
                    Acircumflextilde
                    acircumflextilde
                    Acircumflexhookabove
                    acircumflexhookabove
                    Acircumflexdotbelow
                    acircumflexdotbelow
                    Atilde
                    atilde
                    Abreve
                    abreve
                    Abrevegrave
                    abrevegrave
                    Abreveacute
                    abreveacute
                    Abrevetilde
                    abrevetilde
                    Abrevehookabove
                    abrevehookabove
                    Abrevedotbelow
                    abrevedotbelow
                    Ahookabove
                    ahookabove
                    Adotbelow
                    adotbelow
                    Dcroat
                    dcroat
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Ecircumflexgrave
                    ecircumflexgrave
                    Ecircumflexacute
                    ecircumflexacute
                    Ecircumflextilde
                    ecircumflextilde
                    Ecircumflexhookabove
                    ecircumflexhookabove
                    Ecircumflexdotbelow
                    ecircumflexdotbelow
                    Etilde
                    etilde
                    Ehookabove
                    ehookabove
                    Edotbelow
                    edotbelow
                    Igrave
                    igrave
                    Iacute
                    iacute
                    Itilde
                    itilde
                    Ihookabove
                    ihookabove
                    Idotbelow
                    idotbelow
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Ocircumflexgrave
                    ocircumflexgrave
                    Ocircumflexacute
                    ocircumflexacute
                    Ocircumflextilde
                    ocircumflextilde
                    Ocircumflexhookabove
                    ocircumflexhookabove
                    Ocircumflexdotbelow
                    ocircumflexdotbelow
                    Otilde
                    otilde
                    Ohookabove
                    ohookabove
                    Ohorn
                    ohorn
                    Ohorngrave
                    ohorngrave
                    Ohornacute
                    ohornacute
                    Ohorntilde
                    ohorntilde
                    Ohornhookabove
                    ohornhookabove
                    Ohorndotbelow
                    ohorndotbelow
                    Odotbelow
                    odotbelow
                    Ugrave
                    ugrave
                    Uacute
                    uacute
                    Utilde
                    utilde
                    Uhookabove
                    uhookabove
                    Uhorn
                    uhorn
                    Uhorngrave
                    uhorngrave
                    Uhornacute
                    uhornacute
                    Uhorntilde
                    uhorntilde
                    Uhornhookabove
                    uhornhookabove
                    Uhorndotbelow
                    uhorndotbelow
                    Udotbelow
                    udotbelow
                    Ygrave
                    ygrave
                    Yacute
                    yacute
                    Ytilde
                    ytilde
                    Yhookabove
                    yhookabove
                    Ydotbelow
                    ydotbelow
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Acircumflex", "acircumflex", "Acircumflexgrave", "acircumflexgrave", "Acircumflexacute", "acircumflexacute", "Acircumflextilde", "acircumflextilde", "Acircumflexhookabove", "acircumflexhookabove", "Acircumflexdotbelow", "acircumflexdotbelow", "Atilde", "atilde", "Abreve", "abreve", "Abrevegrave", "abrevegrave", "Abreveacute", "abreveacute", "Abrevetilde", "abrevetilde", "Abrevehookabove", "abrevehookabove", "Abrevedotbelow", "abrevedotbelow", "Ahookabove", "ahookabove", "Adotbelow", "adotbelow", "Dcroat", "dcroat", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Ecircumflexgrave", "ecircumflexgrave", "Ecircumflexacute", "ecircumflexacute", "Ecircumflextilde", "ecircumflextilde", "Ecircumflexhookabove", "ecircumflexhookabove", "Ecircumflexdotbelow", "ecircumflexdotbelow", "Etilde", "etilde", "Ehookabove", "ehookabove", "Edotbelow", "edotbelow", "Igrave", "igrave", "Iacute", "iacute", "Itilde", "itilde", "Ihookabove", "ihookabove", "Idotbelow", "idotbelow", "Ograve", "ograve", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Ocircumflexgrave", "ocircumflexgrave", "Ocircumflexacute", "ocircumflexacute", "Ocircumflextilde", "ocircumflextilde", "Ocircumflexhookabove", "ocircumflexhookabove", "Ocircumflexdotbelow", "ocircumflexdotbelow", "Otilde", "otilde", "Ohookabove", "ohookabove", "Ohorn", "ohorn", "Ohorngrave", "ohorngrave", "Ohornacute", "ohornacute", "Ohorntilde", "ohorntilde", "Ohornhookabove", "ohornhookabove", "Ohorndotbelow", "ohorndotbelow", "Odotbelow", "odotbelow", "Ugrave", "ugrave", "Uacute", "uacute", "Utilde", "utilde", "Uhookabove", "uhookabove", "Uhorn", "uhorn", "Uhorngrave", "uhorngrave", "Uhornacute", "uhornacute", "Uhorntilde", "uhorntilde", "Uhornhookabove", "uhornhookabove", "Uhorndotbelow", "uhorndotbelow", "Udotbelow", "udotbelow", "Ygrave", "ygrave", "Yacute", "yacute", "Ytilde", "ytilde", "Yhookabove", "yhookabove", "Ydotbelow", "ydotbelow"}

                Vietnamese

            <dict>
                <key>glyphNames</key>
                <array>
                    Aacute
                    aacute
                    Agrave
                    agrave
                    Acircumflex
                    acircumflex
                    Adieresis
                    adieresis
                    Eacute
                    eacute
                    Egrave
                    egrave
                    Ecircumflex
                    ecircumflex
                    Edieresis
                    edieresis
                    Iacute
                    iacute
                    Igrave
                    igrave
                    Icircumflex
                    icircumflex
                    Idieresis
                    idieresis
                    Oacute
                    oacute
                    Ograve
                    ograve
                    Ocircumflex
                    ocircumflex
                    Odieresis
                    odieresis
                    Uacute
                    uacute
                    Ugrave
                    ugrave
                    Ucircumflex
                    ucircumflex
                    Udieresis
                    udieresis
                    Yacute
                    yacute
                    Ygrave
                    ygrave
                    Ycircumflex
                    ycircumflex
                    Ydieresis
                    ydieresis
                    Wcircumflex
                    wcircumflex
                </array>
                <key>query</key>
                Name IN {"Aacute", "aacute", "Agrave", "agrave", "Acircumflex", "acircumflex", "Adieresis", "adieresis", "Eacute", "eacute", "Egrave", "egrave", "Ecircumflex", "ecircumflex", "Edieresis", "edieresis", "Iacute", "iacute", "Igrave", "igrave", "Icircumflex", "icircumflex", "Idieresis", "idieresis", "Oacute", "oacute", "Ograve", "ograve", "Ocircumflex", "ocircumflex", "Odieresis", "odieresis", "Uacute", "uacute", "Ugrave", "ugrave", "Ucircumflex", "ucircumflex", "Udieresis", "udieresis", "Yacute", "yacute", "Ygrave", "ygrave", "Ycircumflex", "ycircumflex", "Ydieresis", "ydieresis", "Wcircumflex", "wcircumflex"}

                Welsh

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Atilde
                    atilde
                    Eacute
                    eacute
                    Edieresis
                    edieresis
                    Ntilde
                    ntilde
                    Eng
                    eng
                    Oacute
                    oacute
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Atilde", "atilde", "Eacute", "eacute", "Edieresis", "edieresis", "Ntilde", "ntilde", "Eng", "eng", "Oacute", "oacute"}

                Wolof

            <dict>
                <key>glyphNames</key>
                <array>
                    Agrave
                    agrave
                    Aacute
                    aacute
                    Acircumflex
                    acircumflex
                    Acaron
                    acaron
                    Egrave
                    egrave
                    Eacute
                    eacute
                    Ecircumflex
                    ecircumflex
                    Ecaron
                    ecaron
                    Edotbelow
                    edotbelow
                    Igrave
                    igrave
                    Iacute
                    iacute
                    Icircumflex
                    icircumflex
                    Icaron
                    icaron
                    uE000
                    uE001
                    Nacute
                    nacute
                    uE00C
                    uE00D
                    Ograve
                    ograve
                    Oacute
                    oacute
                    Ocircumflex
                    ocircumflex
                    Ocaron
                    ocaron
                    Odotbelow
                    odotbelow
                    Sdotbelow
                    sdotbelow
                    Ugrave
                    ugrave
                    Uacute
                    uacute
                    Ucircumflex
                    ucircumflex
                    Ucaron
                    ucaron
                </array>
                <key>query</key>
                Name IN {"Agrave", "agrave", "Aacute", "aacute", "Acircumflex", "acircumflex", "Acaron", "acaron", "Egrave", "egrave", "Eacute", "eacute", "Ecircumflex", "ecircumflex", "Ecaron", "ecaron", "Edotbelow", "edotbelow", "Igrave", "igrave", "Iacute", "iacute", "Icircumflex", "icircumflex", "Icaron", "icaron", "uE000", "uE001", "Nacute", "nacute", "uE00C", "uE00D", "Ograve", "ograve", "Oacute", "oacute", "Ocircumflex", "ocircumflex", "Ocaron", "ocaron", "Odotbelow", "odotbelow", "Sdotbelow", "sdotbelow", "Ugrave", "ugrave", "Uacute", "uacute", "Ucircumflex", "ucircumflex", "Ucaron", "ucaron"}

                Yoruba

        </array>
        <key>query</key>


        Lang Support (All)

        140627486650128

</array>
</plist>

}
'''
