
def process(self):
    self.setDraft()
    self.edit("RUNIC")
    self.edit("LETTER")
    self.scriptPrefix()
    self.replace("-", "_")
    self.replace(" ", "_")
    self.compress()
    self.lower()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Runic")
