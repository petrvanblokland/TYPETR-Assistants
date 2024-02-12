
def process(self):
    self.edit("HANGZHOU NUMERAL", "hangzhou")

    self.edit("JAPANESE INDUSTRIAL STANDARD SYMBOL", "jis")
    self.edit("CIRCLED POSTAL MARK", "circlepostalmark")
    self.edit("REVERSED DOUBLE PRIME QUOTATION MARK", "quotedblprimereversed")
    self.edit("DOUBLE PRIME QUOTATION MARK", "quotedblprime")
    self.edit("LEFT DOUBLE ANGLE BRACKET", "dblanglebracketleft")
    self.edit("RIGHT DOUBLE ANGLE BRACKET", "dblanglebracketright")
    self.edit("IDEOGRAPHIC NUMBER ZERO", "ideographiczero")
    self.edit("REVERSED", "reversed")
    self.edit("CLOSING MARK", "close")
    self.edit("FULL STOP", "period")
    self.edit("DOUBLE ANGLE", "dblangle")
    self.edit("DOUBLE", "dbl")
    self.edit("LEFT", "left")
    self.edit("RIGHT", "right")
    self.processAs("Helper Digit Names")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("CJK Symbols and Punctuation")
