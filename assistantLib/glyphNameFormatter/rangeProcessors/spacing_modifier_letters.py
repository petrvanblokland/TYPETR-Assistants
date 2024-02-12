

def process(self):
    self.scriptTag = ""
    if self.has("MODIFIER LETTER CIRCUMFLEX ACCENT"):
        return

    self.replace("MODIFIER")

    # self.replace("LETTER SMALL CAPITAL INVERTED R", "Rsmallinvertedsupmod")

    self.edit("COLON", "colon")
    self.edit("TRIANGULAR", "triangular")
    self.edit("RING", "ring")
    self.edit("DEPARTING TONE MARK", "tone")
    self.edit("TONE MARK", "tone")
    self.edit("TONE", "tone")
    self.edit("DOUBLE", "dbl")
    self.edit("WITH HOOK", "hook")
    self.edit("HOOK", "hook")
    self.edit("TURNED", "turned")
    self.edit("HALF", "half")
    self.edit("SMALL", "sup")
    self.edit("BAR", "bar")
    self.edit("HALF", "half")
    self.edit("LEFT", "left")
    self.edit("RIGHT", "right")
    self.edit("UP", "up")
    self.edit("DOWN", "down")
    self.edit("EXTRA-LOW", "extralow")
    self.edit("LOW", "low")
    self.edit("MIDDLE", "middle")
    self.edit("MID", "mid")
    self.edit("EXTRA-HIGH", "extrahigh")
    self.edit("HIGH", "high")
    self.edit("BEGIN", "begin")
    self.edit("END", "end")

    self.edit("RAISED", "raised")
    self.edit("SHELF", "shelf")

    self.processAs("Helper Shapes")

    self.replace("ACCENT")
    self.replace("LETTER")

    self.handleCase()
    if not self.has("CAPITAL"):
        self.lower()
    if self.has("MODIFIER"):
        self.suffix("mod")
    self.compress()



if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Spacing Modifier Letters")

