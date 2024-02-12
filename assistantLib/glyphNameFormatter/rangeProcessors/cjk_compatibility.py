
def process(self):


    self.replace("SQUARED", "2")
    self.replace("CUBED", "3")
    # self.replace("C OVER KG", "coverkg")
    # self.replace("M OVER S", "movers")
    # self.replace("RAD OVER S", "radovers")
    self.replace("DAY", "day")
    # self.replace("V OVER M", "voverm")
    # self.replace("A OVER M", "aoverm")

    if 0x33E0 <= self.uniNumber <= 0x33FE:
        self.edit("IDEOGRAPHIC TELEGRAPH SYMBOL FOR", "telegraph")

    fullWidthSections = [
        (0x3371, 0x337A),
        (0x3380, 0x33DF)
    ]
    changed = False
    for start, end in fullWidthSections:
        if start <= self.uniNumber <= end:
            self.edit("SQUARE", "fullwidth")
            changed = True
    if not changed:
        self.edit("SQUARE", "square")

    # mixedCases = {
    # # "RAD OVER S SQUARED":    "radoverssquared",
    # # "ERA NAME TAISYOU":    "eranametaisyou",
    # # "M OVER S SQUARED":    "moverssquared",
    # # "ERA NAME HEISEI":    "eranameheisei",
    # # "ERA NAME SYOUWA":    "eranamesyouwa",
    # # "ERA NAME MEIZI":    "eranamemeizi",
    # # "CORPORATION":    "corporation",
    # # "KIROMEETORU":    "kiromeetoru",
    # # "KIROGURAMU":    "kiroguramu",
    # # "CM SQUARED":    "cmsquared",
    # # "DM SQUARED":    "dmsquared",
    # # "KM CAPITAL":    "kmcapital",
    # # "KM SQUARED":    "kmsquared",
    # # "MM SQUARED":    "mmsquared",
    # # "GURAMUTON":    "guramuton",
    # # "HEKUTAARU":    "hekutaaru",
    # # "KIROWATTO":    "kirowatto",
    # # "KURUZEIRO":    "kuruzeiro",
    # # "MIRIBAARU":    "miribaaru",
    # # "PIASUTORU":    "piasutoru",
    # # "RAD OVER S":    "radovers",
    # # "M SQUARED":    "msquared",
    # # "BUSSYERU":    "bussyeru",
    # # "C OVER KG":    "coverkg",
    # # "ESUKUUDO":    "esukuudo",
    # # "HUARADDO":    "huaraddo",
    # # "PAASENTO":    "paasento",
    # # "RENTOGEN":    "rentogen",
    # # "SANTIIMU":    "santiimu",
    # # "CM CUBED":    "cmcubed",
    # # "DM CUBED":    "dmcubed",
    # # "KM CUBED":    "kmcubed",
    # # "MB SMALL":    "mbsmall",
    # # "MM CUBED":    "mmcubed",
    # # "A OVER M":    "aoverm",
    # # "BAARERU":    "baareru",
    # # "GIRUDAA":    "girudaa",
    # # "KARATTO":    "karatto",
    # # "KARORII":    "karorii",
    # # "KUROONE":    "kuroone",
    # # "M OVER S":    "movers",
    # # "MAIKURO":    "maikuro",
    # # "MANSYON":    "mansyon",
    # # "MEETORU":    "meetoru",
    # # "MEGATON":    "megaton",
    # # "MIKURON":    "mikuron",
    # # "RITTORU":    "rittoru",
    # # "RUUBURU":    "ruuburu",
    # # "SAIKURU":    "saikuru",
    # # "SIRINGU":    "siringu",
    # # "V OVER M":    "voverm",
    # # "M CUBED":    "mcubed",
    # # "MV MEGA":    "mvmega",
    # # "MW MEGA":    "mwmega",
    # # "PA AMPS":    "paamps",
    # # "APAATO":    "apaato",
    # # "ARUHUA":    "aruhua",
    # # "BORUTO":    "boruto",
    # # "GURAMU":    "guramu",
    # # "HERUTU":    "herutu",
    # # "HUIITO":    "huiito",
    # # "ININGU":    "iningu",
    # # "KORUNA":    "koruna",
    # # "KYURII":    "kyurii",
    # # "MARUKU":    "maruku",
    # # "PENIHI":    "penihi",
    # # "PIKURU":    "pikuru",
    # # "POINTO":    "pointo",
    # # "ANPEA":    "anpea",
    # # "BEETA":    "beeta",
    # # "DAASU":    "daasu",
    # # "EEKAA":    "eekaa",
    # # "GANMA":    "ganma",
    # # "GARON":    "garon",
    # # "GINII":    "ginii",
    # # "HAITU":    "haitu",
    # # "HOORU":    "hooru",
    # # "HURAN":    "huran",
    # # "KAIRI":    "kairi",
    # # "KEESU":    "keesu",
    # # "KOOPO":    "koopo",
    # # "MAHHA":    "mahha",
    # # "MAIRU":    "mairu",
    # # "NOTTO":    "notto",
    # # "PAATU":    "paatu",
    # # "PEEZI":    "peezi",
    # # "PENSU":    "pensu",
    # # "PONDO":    "pondo",
    # # "RUPII":    "rupii",
    # # "SENTI":    "senti",
    # # "SENTO":    "sento",
    # # "WATTO":    "watto",
    # # "YAADO":    "yaado",
    # # "YAARU":    "yaaru",
    # "K OHM":    "kOhm",
    # "M OHM":    "MOhm",
    # # "AARU":    "aaru",
    # # "BIRU":    "biru",
    # # "DESI":    "desi",
    # # "DORU":    "doru",
    # # "GIGA":    "giga",
    # # "HOON":    "hoon",
    # # "INTI":    "inti",
    # # "KCAL":    "kcal",
    # # "KIRO":    "kiro",
    # # "MEGA":    "mega",
    # # "MIRI":    "miri",
    # # "NANO":    "nano",
    # # "ONSU":    "onsu",
    # # "OOMU":    "oomu",
    # # "PESO":    "peso",
    # # "PIKO":    "piko",
    # # "REMU":    "remu",
    # # "RIRA":    "rira",
    # # "YUAN":    "yuan",
    # "MU A":    "muA",
    # "MU F":    "muF",
    # "MU G":    "muG",
    # # "MU L":    "mul",
    # # "MU M":    "mum",
    # # "MU S":    "mus",
    # # "MU V":    "muv",
    # "MU W":    "muW",
    # "BAR":    "bar",
    # "CAL":    "cal",
    # "GHZ":    "GHz",
    # "GPA":    "GPa",
    # # "HON":    "hon",
    # "HPA":    "hPa",
    # "KHZ":    "kHz",
    # "KPA":    "kPa",
    # # "LOG":    "log",
    # "MHZ":    "MHz",
    # # "MIL":    "mil",
    # # "MOL":    "mol",
    # "MPA":    "MPa",
    # "PPM":    "PPM",
    # # "RAD":    "rad",
    # "THZ":    "THz",
    # # "TON":    "ton",
    # # "UON":    "uon",
    # "AM":    "am",
    # "AU":    "AU",
    # "BQ":    "Bq",
    # # "CC":    "cc",
    # # "CD":    "cd",
    # # "CM":    "cm",
    # "CO":    "co",
    # "DA":    "da",
    # "DB":    "db",
    # "DL":    "dl",
    # "DM":    "dm",
    # "FM":    "fm",
    # "GB":    "gb",
    # "GY":    "gy",
    # "HA":    "ha",
    # "HP":    "hp",
    # "HZ":    "hz",
    # "IN":    "in",
    # "IU":    "iu",
    # "KA":    "ka",
    # "KB":    "kb",
    # "KG":    "kg",
    # "KK":    "kk",
    # "KL":    "kl",
    # "KM":    "km",
    # "KT":    "kt",
    # "KV":    "kv",
    # "KW":    "kw",
    # "LM":    "lm",
    # "LN":    "ln",
    # "LX":    "lx",
    # "MA":    "ma",
    # "MB":    "mb",
    # "MG":    "mg",
    # "ML":    "ml",
    # "MM":    "mm",
    # "MS":    "ms",
    # "MV":    "mv",
    # "MW":    "mw",
    # "NA":    "na",
    # "NF":    "nf",
    # "NM":    "nm",
    # "NS":    "ns",
    # "NV":    "nv",
    # "NW":    "nw",
    # "OV":    "ov",
    # "PA":    "pa",
    # "PC":    "pc",
    # "PF":    "pf",
    # "PH":    "ph",
    # "PM":    "pm",
    # "PR":    "pr",
    # "PS":    "ps",
    # "PV":    "pv",
    # "PW":    "pw",
    # "SR":    "sr",
    # "SV":    "sv",
    # "WB":    "wb",    }
    # allowMixedCase = False
    # for k, v in mixedCases.items():
    #     if self.has(k):
    #         self.replace(k, v)
    #         allowMixedCase = True
    #         break
    # # but then do these anyway
    # if 0x3300 <= self.uniNumber <= 0x3357:
    #     self.lower()

    # self.edit("MEGA", "mega")
    self.processAs("Helper Digit Names")

    self.edit("-")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("CJK Compatibility")
