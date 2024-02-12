
def process(self):
    self.replace("BOX DRAWINGS")
    self.replace("AND")
    self.replace("TO")
    self.replace("LIGHT", "light")
    self.replace("HEAVY", "heavy")
    self.replace("VERTICAL", "vert")
    self.replace("HORIZONTAL", "horz")
    self.replace("DIAGONAL", "diag")
    self.replace("SINGLE", "sng")
    self.replace("DOUBLE", "dbl")
    self.replace("TRIPLE", "trpl")
    self.replace("QUADRUPLE", "quad")
    self.replace("QUAD", "quad")
    self.replace("UPPER", "up")
    self.replace("DOWN", "dn")
    self.replace("LOWER", "dn")
    self.replace("DASH", "dash")
    self.replace("LEFT", "left")
    self.replace("RIGHT", "right")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Box Drawing")
