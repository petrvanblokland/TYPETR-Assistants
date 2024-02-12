
def process(self):
    self.edit("THAI")
    self.edit("CHARACTER")
    self.edit("CURRENCY")
    self.edit("SYMBOL")
    self.edit("DIGIT")
    self.processAs("Helper Digit Names")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Thai")
