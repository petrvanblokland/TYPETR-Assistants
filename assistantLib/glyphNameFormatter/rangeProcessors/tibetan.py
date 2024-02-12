
def process(self):
    self.edit("TIBETAN")
    if self.has("DIGIT"):
        self.edit("DIGIT")
        self.lower()

    self.edit("RIGHT-FACING SVASTI SIGN WITH DOTS", "svastirightdot")
    self.edit("LEFT-FACING SVASTI SIGN WITH DOTS", "svastileftdot")
    self.edit("RIGHT-FACING SVASTI SIGN", "svastiright")
    self.edit("LEFT-FACING SVASTI SIGN", "svastileft")

    self.edit("VOCALIC", "vocalic")
    self.edit("SYLLABLE", "syllable")
    self.edit("VOWEL", "vowel")
    self.edit("LOGOTYPE", "logotype")
    self.edit("INITIAL", 'initial')
    self.edit("CANTILLATION", "cantillation")
    self.edit("CLOSING", "closing")
    self.edit("SYMBOL", "symbol")
    self.edit("SUBJOINED", "subjoined")
    self.edit("FIXED-FORM", "fixed")
    self.edit("SIGN", 'sign')
    self.edit("MARK", 'mark')
    self.edit("LEFT", "left")
    self.edit("RIGHT", "right")

    self.edit("-A", "AA")  # Old name TIBETAN LETTER AA
    self.edit("-")
    self.edit("LETTER")

    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Tibetan")
