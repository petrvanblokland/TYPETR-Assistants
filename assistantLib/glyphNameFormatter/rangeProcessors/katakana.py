
def process(self):
    self.edit("KATAKANA-HIRAGANA", "kana")
    self.edit("SOUND MARK")
    self.edit("MARK")
    self.edit("LETTER")
    self.edit("SMALL", "small")
    self.edit("KATAKANA")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Katakana")
