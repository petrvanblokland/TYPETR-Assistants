

def process(self):
    # processor for rangeName
    self.setExperimental()

    self.edit("PLAYING CARD")
    self.edit("-")
    self.lower()
    self.compress()
    self.scriptPrefix()


if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Playing Cards")
