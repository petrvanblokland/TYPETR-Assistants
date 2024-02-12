

def process(self):
    # edits go here
    self.edit("LATIN")

    self.forceScriptPrefix("latin", "CAPITAL LETTER ALPHA", "Alpha")
    self.forceScriptPrefix("latin", "CAPITAL LETTER TURNED ALPHA", "Alphaturned")

    self.replace("LETTER SMALL CAPITAL TURNED E", "Esmallturned")

    self.edit("DOUBLE", "dbl")
    self.edit("BAR", "bar")
    self.edit("SUBSCRIPT", ".inferior")
    self.edit("HALF", "half")
    self.edit("TAILLESS", "tailless")

    self.edit("DIAGONAL")
    self.edit("WITH")

    self.processAs("Helper Diacritics")
    self.processAs("Helper Shapes")
    self.handleCase()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Latin Extended-C")
