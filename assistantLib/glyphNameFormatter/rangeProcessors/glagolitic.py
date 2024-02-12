
def process(self):
    self.setDraft()
    self.edit("GLAGOLITIC")
    self.handleCase()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Glagolitic")
