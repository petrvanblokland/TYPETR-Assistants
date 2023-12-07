
def process(self):
    self.edit("BENGALI")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.edit("VOWEL SIGN VOCALIC", "vocalsign")
    self.edit("VOWEL SIGN", "sign")
    self.edit("VOCALIC", "vocal")

    self.edit("NUMERATOR ONE LESS THAN THE DENOMINATOR", "oneless")
    self.edit("CURRENCY NUMERATOR", "currency", "numerator")
    self.edit("CURRENCY DENOMINATOR", "currency", "denominator")
    self.edit("RUPEE MARK", "rupeemark")
    self.edit("RUPEE SIGN", "rupee")
    self.edit("WITH MIDDLE DIAGONAL", "middiagonal")
    self.edit("WITH LOWER DIAGONAL", "lowdiagonal")

    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Bengali")
