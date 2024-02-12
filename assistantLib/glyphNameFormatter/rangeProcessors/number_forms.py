
def process(self):

    # nmbr:oneeighth -> oneeighth
    # nmbr:onetenth -> onetenth
    # nmbr:onefifth -> onefifth
    self.replace("FRACTION NUMERATOR ONE", "onefraction")
    self.replace("LATIN SMALL LETTER REVERSED C", "creversed")

    self.replace("VULGAR FRACTION")

    self.editToFinal("SMALL ROMAN", ".romansmall")
    self.editToFinal("ROMAN", ".roman")

    self.replace("NUMERAL")

    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Number Forms")
