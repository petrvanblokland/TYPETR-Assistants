
def process(self):
    self.edit("VOWEL SIGN VOCALIC", "vocalsign")
    self.edit("VOWEL SIGN", "sign")
    self.edit("VOCALIC", "vocal")
    self.edit("SIGN NUKTA", "nukta")
    self.edit("SIGN VIRAMA", "virama")
    self.edit("SIGN AVAGRAHA", "avagraha")
    self.edit("SIGN VISARGA", "visarga")
    self.edit("SIGN ANUSVARA", "anusvara")
    self.edit("SIGN CANDRABINDU", "candrabindu")
    self.edit("CANDRA", "candra")

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Helper Indic")
