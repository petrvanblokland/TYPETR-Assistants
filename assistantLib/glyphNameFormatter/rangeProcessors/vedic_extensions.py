

def process(self):
    self.edit("VEDIC")
    self.edit("SIGN", "sign")
    self.edit("TONE", "tone")
    self.edit("DOUBLE", "dbl")
    self.edit("TRIPLE", "tpl")
    self.edit("LONG", "long")
    self.edit("REVERSED", "reversed")

    self.processAs("Helper Indic")

    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Vedic Extensions")
