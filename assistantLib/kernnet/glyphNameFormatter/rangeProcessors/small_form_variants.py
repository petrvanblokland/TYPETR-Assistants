from glyphNameFormatter.data.scriptPrefixes import scriptPrefixes


def process(self):
    self.edit("SMALL")
    self.edit("IDEOGRAPHIC", "ideographic")
    self.processAs("Basic Latin")
    self.processAs("General Punctuation")
    self.scriptTag = scriptPrefixes["Small Form Variants"]

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Small Form Variants")
