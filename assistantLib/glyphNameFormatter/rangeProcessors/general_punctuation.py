from assistantLib.glyphNameFormatter.data.scriptPrefixes import scriptPrefixes


def process(self):
    self.replace("VERTICAL LINE", "verticalbar")
    self.replace("QUESTION MARK", "question")
    self.replace("EXCLAMATION QUESTION", "exclam")
    self.replace("DOUBLE HIGH-REVERSED-9 QUOTATION MARK", "quotedblreversed")

    self.replace("TRIPLE PRIME", "millisecond")
    self.replace("DOUBLE PRIME", "second")
    self.replace("PRIME", "minute")

    self.replace("LEFT-TO-RIGHT", "lefttoright")
    self.replace("RIGHT-TO-LEFT", "righttoleft")

    self.edit("DOUBLE", "dbl")
    self.edit("REVERSED", "reversed")

    self.edit("LEFT", "left")
    self.edit("RIGHT", "right")
    self.edit("SQUARE", "square")
    self.edit("WITH QUILL", "quill")
    self.edit("EMBEDDING", "embed")

    self.replace("-")
    self.compress()
    self.lower()

    if not self.has("HYPHEN"):
        # solve conflict with HYPHEN-MINUS 002D
        self.scriptTag = scriptPrefixes["latin"]

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("General Punctuation")
