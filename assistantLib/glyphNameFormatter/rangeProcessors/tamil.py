
def process(self):
    self.edit("TAMIL")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.edit("NUMBER")
    self.processAs("Helper Indic")
    self.processAs("Helper Numbers")
    self.replace("-")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Tamil")
