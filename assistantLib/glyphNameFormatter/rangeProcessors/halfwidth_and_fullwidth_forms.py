from assistantLib.glyphNameFormatter.data.scriptPrefixes import scriptPrefixes


def process(self):

    size = "NOSIZE"
    if self.has("FULLWIDTH"):
        size = "fullwidth"
    elif self.has("HALFWIDTH"):
        size = "halfwidth"
    self.replace("FULLWIDTH")
    self.replace("HALFWIDTH")
    if 0xFF01 <= self.uniNumber <= 0xFF5E:
        self.processAs('Basic Latin')
        self.edit("COMMERCIAL AT", "at")
    elif 0xFF65 <= self.uniNumber <= 0xFF9F:
        self.processAs('Katakana')
        self.forceScriptPrefix('katakana')
    elif 0xFFA0 <= self.uniNumber <= 0xFFDC:
        self.edit("HANGUL LETTER")
        self.processAs('Hangul')
        self.replace("-", '')
        self.lower()
    else:
        self.lower()
    self.scriptTag = scriptPrefixes[size]
    self.scriptPrefix()
    self.compress()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Halfwidth and Fullwidth Forms")
