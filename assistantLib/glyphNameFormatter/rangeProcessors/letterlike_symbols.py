
def process(self):
    self.replace("CONSTANT")
    self.replace("TO THE")
    self.replace("SIGN")
    self.replace("RECORDING")
    self.replace("TAKE")
    self.replace("SYMBOL")
    self.replace("SOURCE")
    self.replace("N-ARY")

    self.replace("SCRIPT SMALL L", "litre")
    self.replace("TURNED GREEK SMALL LETTER IOTA", "iotaturned")

    self.edit("DOUBLE-STRUCK", "dblstruck")
    self.edit("PRESCRIPTION", "prescription")
    self.edit("SCRIPT", "script")
    self.edit("BLACK-LETTER", "fraktur")
    self.edit("OVER TWO PI", "twopi")
    self.edit("INVERTED", "inverted")
    self.edit("TURNED", "turned")
    self.edit("ROTATED", "rotated")
    self.edit("REVERSED", "reversed")
    self.edit("SANS-SERIF", "sans")
    self.edit("ITALIC", "italic")

    self.compress()
    self.handleCase()
    if not self.has("CAPITAL"):
        self.lower()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Letterlike Symbols")
