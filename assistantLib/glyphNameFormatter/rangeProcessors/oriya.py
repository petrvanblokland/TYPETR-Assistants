
def process(self):
    self.edit("ORIYA")
    self.edit("LETTER")
    self.edit("VOWEL SIGN", "sign")
    self.edit("DIGIT")
    self.edit("FRACTION")
    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")


    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Oriya")
