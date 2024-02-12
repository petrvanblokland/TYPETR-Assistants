
def process(self):
    self.replace("BRAILLE PATTERN BLANK", "brblank")
    self.replace("BRAILLE PATTERN DOTS", "dots")
    self.replace("-", "")
   

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Braille Patterns")
