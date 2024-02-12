
def process(self):
    self.edit("PRESENTATION FORM FOR")
    self.edit("LENTICULAR")
    self.edit("EXCLAMATION MARK", "exclam")
    self.edit("QUESTION MARK", "question")
    self.edit("VERTICAL")
    self.edit("HORIZONTAL", "hor")
    self.edit("WHITE", "white")
    self.edit("LEFT", "left")
    self.edit("RIGHT", "right")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Vertical Forms")
