
def process(self):
    self.edit("ORIYA")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Oriya")
