
def process(self):
    self.edit("LATIN")
    self.edit("DIGIT")

    self.edit("TORTOISE SHELL BRACKETED", "shell")
    self.edit("PARENTHESIZED", "parens")
    self.edit("ITALIC", "italic")
    self.edit("CROSSED", "cross")
    self.edit("SQUARED", "square")
    self.edit("CIRCLED", "circle")
    self.edit("NEGATIVE", "black")

    shouldHandleCase = True
    keepCaps = [
        "SA", "PA", "IC", "PPV", "SS", "SD", "MV", "HV",
        "WZ", "CD",
        ]
    for c in keepCaps:
        if self.has(" %s" % c):
            self.lower()
            self.replace(c.lower(), c)
            shouldHandleCase = False

    if shouldHandleCase:
        self.handleCase()
        if not self.has("CAPITAL"):
            self.lower()

    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Enclosed Alphanumeric Supplement")
