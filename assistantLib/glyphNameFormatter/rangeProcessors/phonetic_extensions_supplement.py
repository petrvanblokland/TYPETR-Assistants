

def process(self):
    # edits go here
    self.edit("CROSSED-TAIL", "crossedtail")
    self.edit("WITH HOOK AND TAIL", "hooktail")
    self.processAs("Phonetic Extensions")
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Phonetic Extensions Supplement")
