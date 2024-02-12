
def process(self):
    self.edit("QUESTION MARK", "question")
    self.edit("SQUARED", "square")
    self.edit("PARENTHESIS", "paren")
    self.edit("DOUBLE", "dbl")
    self.edit("WITH QUILL", "quill")
    self.edit("WITH DOT BELOW", "dotbelow")
    self.edit("WITH DOT ABOVE", "dotaccent")
    self.edit("WITH RING ABOVE", "ring")
    self.edit("WITH DIAERESIS", self.prefSpelling_dieresis)
    self.edit("DOWNWARDS", "down")
    self.edit("UPWARDS", "up")
    self.edit("RAISED OMISSION", "raised")

    self.replace("QUOTATION", "quote")
    self.replace("MARKER", "marker")
    self.edit("MARK")
    self.edit("PUNCTUATION")
    self.edit("SIDEWAYS")

    self.edit("LOW-REVERSED-9", "lowreversed")
    self.edit("TWO-", "dbl")
    self.edit("THREE-", "tpl")
    parts = [
        "HALF", "DOTTED", "RAISED", "INTERPOLATION", "TRANSPOSITION", "SUBSTITUTION",
        "RING", "VERTICAL", "PARAPHRASE", "FORKED", "EDITORIAL",
        "REVERSED", "INVERTED", "OBLIQUE",
        "FOUR",
        "BOTTOM", "TOP", "LOW",
        "LEFT", "RIGHT",
        ]
    for part in parts:
        self.edit(part, part.lower())

    self.replace("-POINTING")

    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Supplemental Punctuation")
