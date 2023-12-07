

def process(self):
    self.setExperimental()

    self.edit("LENIS", "lenis")
    self.edit("WITH CROSSED-TAIL", "tail")
    self.edit("SCRIPT", "script")
    self.edit("BLACKLETTER", "fractur")
    self.edit("REVERSED-SCHWA", "reversedschwa")
    self.edit("WITH INVERTED LAZY S", "lazyinverteds")
    self.edit("OPEN-O", "oopen")

    self.processAs("Latin Extended-C")

    self.edit("MODIFIER", "mod")

    if self.has("GREEK"):
        self.edit("GREEK")
        self.forceScriptPrefix("greek")

    self.edit("-")

    self.compress()


if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Latin Extended-E")
