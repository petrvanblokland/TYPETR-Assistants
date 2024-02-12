

def process(self):
    # edits go here
    self.edit("JAVANESE")
    self.edit("SIGN")
    self.edit("LETTER")

    parts = [
        "VOWEL", "CONSONANT",
        "LEFT", "RIGHT",
        "PADA"
        ]
    for part in parts:
        self.edit(part, part.lower())

    self.edit("DIGIT")
    self.processAs("Helper Digit Names")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Javanese")
