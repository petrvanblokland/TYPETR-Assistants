
def process(self):
    self.edit("LETTER")
    self.edit("SMALL", "small")
    self.edit("KATAKANA-HIRAGANA VOICED SOUND MARK", "voicedmarkkana")
    self.edit("KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK", "semivoicedmarkkana")
    self.edit("HIRAGANA ITERATION MARK", "iterationhiragana")
    self.edit("HIRAGANA VOICED ITERATION MARK", "voicediterationhiragana")
    # self.editToFinal("HIRAGANA", "hiragana")
    self.editToFinal("HIRAGANA")
    self.editToFinal("COMBINING", "cmb")
    self.lower()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Hiragana")
