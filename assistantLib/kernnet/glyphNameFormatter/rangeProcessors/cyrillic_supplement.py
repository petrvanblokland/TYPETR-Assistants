
def process(self):
    # edits go here
    # self.edit("ARMENIAN")
    # self.handleCase()
    # self.compress()
    self.edit("REVERSED")
    self.processAs("Cyrillic")


if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Cyrillic Supplement")
