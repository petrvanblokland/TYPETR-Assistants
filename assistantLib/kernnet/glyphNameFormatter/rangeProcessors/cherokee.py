
def process(self):
    self.setExperimental()
    self.edit("CHEROKEE")
    self.edit("LETTER")
    self.edit("SMALL", "small")
    self.lower()
    self.scriptPrefix()
    

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Cherokee")
