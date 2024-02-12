
def process(self):
    self.edit("TELUGU")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.edit("CANDRABINDU", "candrabindu")
    self.processAs("Helper Indic")
    self.edit("ABOVE", "above")
    self.edit("VOWEL SIGN", "sign")
    self.edit("VOWEL")
    self.edit("SIGN", "sign")
    self.processAs("Helper Numbers")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Telugu")
