
ukrainian = "ukr"


def process(self):
    self.edit("CYRILLIC")
    if self.uniNumber == 0x042D:
        self.uniNameProcessed = "Ereversed"
        return
    if self.uniNumber == 0x044D:
        self.uniNameProcessed = "ereversed"
        return

    self.edit("CAPITAL LIGATURE EN GHE", "Enge")
    self.edit("SMALL LIGATURE EN GHE", "enge")
    self.edit("CAPITAL LIGATURE A IE", "Aie")
    self.edit("SMALL LIGATURE A IE", "aie")
    self.edit("CAPITAL LIGATURE TE TSE", "Tetse")
    self.edit("SMALL LIGATURE TE TSE", "tetse")
    self.edit("CAPITAL LETTER HARD SIGN", "Hard")
    self.edit("CAPITAL LETTER SOFT SIGN", "Soft")

    # corrections from Ilya
    self.edit("CAPITAL LETTER UKRAINIAN IE", "E%s" % ukrainian)
    self.edit("SMALL LETTER UKRAINIAN IE", "e%s" % ukrainian)
    self.edit("CAPITAL LETTER YI", "Y%s" % ukrainian)
    self.edit("SMALL LETTER YI", "y%s" % ukrainian)
    self.edit("CAPITAL LETTER HA WITH DESCENDER", "Xatail")
    self.edit("SMALL LETTER HA WITH DESCENDER", "xatail")
    self.edit("CAPITAL LETTER CHE WITH VERTICAL STROKE", "Chevert")
    self.edit("SMALL LETTER CHE WITH VERTICAL STROKE", "chevert")
    self.edit("CAPITAL LETTER E WITH DIAERESIS", "Ereverseddieresis")
    self.edit("SMALL LETTER E WITH DIAERESIS", "ereverseddieresis")

    self.edit("CAPITAL LETTER YERU", "Ylong")
    self.edit("SMALL LETTER YERU", "ylong")
    self.edit("CAPITAL LETTER GHE", "Ge")
    self.edit("SMALL LETTER GHE", "ge")

    self.edit("SMALL LETTER PALOCHKA", "palochka")
    self.edit("LETTER PALOCHKA", "Palochka")

    self.edit("BIG", "big")         # Yus
    self.edit("LITTLE", "little")   # yus
    self.edit("BARRED", "bar")
    self.edit("STRAIGHT", "straight")
    self.edit("SHORT", "short")
    self.edit("IOTIFIED", "iotified")
    self.edit("WITH TITLO", 'titlo')
    self.edit("TITLO", 'titlo')

    self.edit("ABKHASIAN", "abkh")
    self.edit("BASHKIR", "bashk")
    self.edit("KHAKASSIAN", "khakas")

    self.edit("WITH UPTURN", "up")
    self.edit("WITH DESCENDER", "tail")
    self.edit("WITH VERTICAL STROKE", "verticalstroke")
    self.edit("WITH TAIL", "sharptail")
    self.edit("WITH TICK", "tick")
    self.edit("WITH MIDDLE HOOK", "hook")

    self.edit("HARD SIGN", "hard")
    self.edit("SOFT SIGN", "soft")

    self.edit("ROUND", "round")
    self.edit("KOMI", 'komi')
    self.edit("BYELORUSSIAN-UKRAINIAN", ukrainian)
    self.edit("UKRAINIAN", "ukr")

    self.edit("ALEUT", "aleut")

    self.edit("HUNDRED THOUSANDS SIGN", "hundredthousands")
    self.edit("MILLIONS SIGN", "millions")
    self.edit("THOUSANDS SIGN", "thousands")
    self.edit("POKRYTIE", "pokrytie")
    self.edit("PALATALIZATION", "palat")
    self.edit("DASIA PNEUMATA", "dasia")
    self.edit("PSILI PNEUMATA", "psili")

    self.edit("COMBINING", "cmb")

    self.processAs("Helper Diacritics")

    self.handleCase()
    # cleanup
    self.edit("CAPITAL")
    self.edit("LETTER")
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Cyrillic")
