

def process(self):
    self.edit("HANGUL")
    self.edit("LETTER")
    self.edit("-")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Hangul Compatibility Jamo")
