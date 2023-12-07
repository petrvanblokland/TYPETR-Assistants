
def process(self):
    self.edit("TAMIL")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.edit("VOWEL")
    self.edit("SIGN", "sign")
    self.edit("NUMBER")
    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")
    self.replace("-")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Tamil")
