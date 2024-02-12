
def process(self):

    self.edit("IDEOGRAPHIC TELEGRAPH SYMBOL FOR", "telegraph")
    self.edit("PARENTHESIZED IDEOGRAPH", "ideographicparen")
    self.editToFinal("PARENTHESIZED", "paren")
    self.edit("CIRCLED IDEOGRAPH", "ideographiccircled")
    self.edit("CIRCLED NUMBER", "circle")
    self.replace("IDEOGRAPH", "ideographic")

    self.edit("KOREAN CHARACTER")
    self.edit("ON BLACK SQUARE", "square")
    self.edit("CIRCLED KATAKANA", "circlekatakana")
    self.edit("CIRCLED HANGUL", "circlekorean")  # or hangul?

    self.edit("LIMITED LIABILITY SIGN", 'LTDfullwidth')
    self.edit("SQUARE HG", "Hgfullwidth")
    self.edit("SQUARE ERG", "ergfullwidth")
    self.edit("SQUARE EV", "eVfullwidth")
    self.edit("PARTNERSHIP SIGN", "partnership")

    self.edit("CIRCLED", "circle")

    self.processAs("Helper Digit Names")
    self.compress()
    self.lower()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Enclosed CJK Letters and Months")
