
def process(self):
    # edits go here
    self.edit("MONGOLIAN")
    self.edit("DIGIT")

    self.replace("FULL STOP", "period")

    parts = [
        "TODO", "SIBE", "MANCHU", "ALI GALI", "HALF", "THREE",

        "INVERTED",
        ]
    for part in parts:
        self.edit(part, part.lower().replace(" ", ""))

    self.replace("LETTER")

    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Mongolian")
