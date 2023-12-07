

def process(self):
    self.edit("TILE")
    self.replace("-", "_")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from glyphNameFormatter.test import printRange
    printRange("Domino Tiles")
