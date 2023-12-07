
def process(self):
    self.edit("TELUGU")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.edit("VOWEL")
    self.edit("SIGN", "sign")
    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Telugu")
