
def process(self):

	#GUJARATI VOWEL SIGN CANDRA E
	#GUJARATI VOWEL CANDRA E

    self.edit("GUJARATI")
    self.edit("LETTER")
    self.edit("DIGIT")
    self.processAs("Helper Indic")
    self.edit("VOWEL SIGN", "sign")
    self.edit("VOWEL")
    self.edit("SIGN")

    self.edit("THREE-DOT NUKTA ABOVE", "threedotnuktaabove")
    self.edit("TWO-CIRCLE NUKTA ABOVE", "twocirclenuktaabove")

    self.processAs("Helper Numbers")
    self.lower()
    self.compress()
    self.scriptPrefix()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    from assistantLib.glyphNameFormatter.tools import debug
    printRange("Gujarati")
    debug(0x0AFA)