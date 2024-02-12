
def process(self):
    self.edit("VOWEL SIGN", "sign")
    self.edit("SIGN NUKTA", "nukta")
    self.edit("SIGN VIRAMA", "virama")
    self.edit("SIGN AVAGRAHA", "avagraha")
    self.edit("SIGN VISARGA", "visarga")
    self.edit("SIGN ANUSVARA", "anusvara")
    self.edit("SIGN CANDRABINDU", "candrabindu")
    self.edit("CANDRA", "candra")

    self.edit("RUPEE MARK", "rupeemark")
    self.edit("RUPEE SIGN", "rupee")

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Helper Indic")
