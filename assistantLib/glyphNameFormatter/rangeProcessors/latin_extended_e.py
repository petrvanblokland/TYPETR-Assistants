

def process(self):
    self.setDraft()

    self.edit("LENIS", "lenis")
    self.edit("WITH CROSSED-TAIL", "tail")
    self.edit("SCRIPT", "script")
    self.edit("BLACKLETTER", "fractur")
    self.edit("REVERSED-SCHWA", "reversedschwa")
    self.edit("WITH INVERTED LAZY S", "lazyinverteds")
    self.edit("OPEN-O", "oopen")
    if self.has("LATIN SMALL LETTER CHI"):
        self.edit("LATIN SMALL LETTER CHI", 'chi')
        self.edit("WITH LOW RIGHT RING", 'lowrightring')
        self.edit("WITH LOW LEFT SERIF", 'lowleftserif')
        self.forceScriptPrefix("latin")

    self.processAs("Latin Extended-C")

    self.edit("MODIFIER", "mod")

    if self.has("GREEK"):
        self.edit("GREEK")
        #self.forceScriptPrefix("greek")
        self.forceScriptPrefix("latin")

    self.edit("-")

    self.compress()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Latin Extended-E")
