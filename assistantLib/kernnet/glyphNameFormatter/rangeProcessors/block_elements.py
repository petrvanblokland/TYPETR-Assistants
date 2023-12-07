
def process(self):
    self.editToFinal("BLOCK", "block")
    self.replace("AND")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Block Elements")
