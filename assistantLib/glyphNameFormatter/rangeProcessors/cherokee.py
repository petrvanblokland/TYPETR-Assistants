
def process(self):
    self.setDraft()
    self.edit("CHEROKEE")
    self.edit("LETTER")
    self.edit("SMALL", "small")
    self.lower()
    self.scriptPrefix()
    

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Cherokee")
