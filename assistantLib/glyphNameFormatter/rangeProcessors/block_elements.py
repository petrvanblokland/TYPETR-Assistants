
def process(self):
    self.camelCase()
    self.compress()

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Block Elements")
