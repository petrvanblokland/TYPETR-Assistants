

def process(self):
    # edits go here
    self.edit("BOPOMOFO")
    self.edit("LETTER")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Bopomofo")
