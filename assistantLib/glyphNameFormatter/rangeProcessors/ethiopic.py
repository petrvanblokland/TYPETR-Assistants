
def process(self):
    pass
    self.edit("ETHIOPIC")
    self.edit("SYLLABLE")
    self.edit("GLOTTAL", "glottal")
    self.processAs("Helper Digit Names")
    self.edit("NUMBER")
    self.edit("DIGIT")
    self.edit("COMBINING", "cmb")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Ethiopic")
