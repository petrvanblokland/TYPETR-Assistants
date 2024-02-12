
def process(self):
    self.edit("GURMUKHI")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")
    self.edit("SIGN", "sign")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Gurmukhi")
