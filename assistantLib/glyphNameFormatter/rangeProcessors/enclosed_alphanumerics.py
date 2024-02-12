
def process(self):
    self.processAs("Helper Digit Names")
    self.edit("DOUBLE CIRCLED", "circledbl")
    self.edit("CIRCLED", "circle")
    self.edit("DIGIT")
    self.edit("LATIN")
    self.edit("NUMBER")
    self.edit("PARENTHESIZED", "parenthesized")
    self.edit("FULL STOP", "period")
    self.edit("NEGATIVE", "black")
    self.handleCase()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Enclosed Alphanumerics")
