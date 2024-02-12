

def process(self):
    self.edit("OCR")
    self.edit("DOUBLE", "dbl")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Optical Character Recognition")
