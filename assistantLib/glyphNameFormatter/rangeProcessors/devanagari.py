
def process(self):
    self.edit("DEVANAGARI")

    # parts
    self.edit("LETTER")
    self.edit("DIGIT")
    self.edit("VOWEL SIGN", "sign")

    self.edit("SIGN CANDRABINDU", "candrabindu")
    self.edit("SIGN INVERTED CANDRABINDU", "candrabinduinverted")

    self.edit("CANDRA", "candra")
    self.edit("DOUBLE", "dbl")
    self.edit("SHORT", "short")
    self.edit("LONG", "long")


    self.processAs("Helper Indic")

    self.edit("DANDA", "danda")
    self.edit("GRAVE ACCENT", "grave")
    self.edit("ACUTE ACCENT", "acute")

    self.edit("STRESS SIGN")
    self.edit("PRISHTHAMATRA", "prishthamatra")
    self.edit("ABBREVIATION SIGN", "abbreviation")
    self.edit("SIGN HIGH SPACING DOT", "dothigh")
    self.edit("HEAVY", "heavy")
    self.edit("GLOTTAL STOP", "glottalstop")

    self.processAs("Helper Digit Names")

    # AGD uses camelcase, but there do not seem to be casing differences between the letters
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Devanagari")
    from assistantLib.glyphNameFormatter.tools import debug
    debug(0x0955)
    debug(0x0900)    
    debug(0x0901)        