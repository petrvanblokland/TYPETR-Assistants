
def process(self):
    self.edit("PRESENTATION FORM FOR")
    self.edit("LOW LINE", "underscore")
    self.edit("LEFT PARENTHESIS", "parenleft")
    self.edit("RIGHT PARENTHESIS", "parenright")
    self.edit("LEFT CURLY BRACKET", "braceleft")
    self.edit("RIGHT CURLY BRACKET", "braceright")
    self.edit("DOUBLE WAVY", "dblwavy")
    self.replace("DOUBLE", "dbl")
    self.edit("WAVY", "wavy")
    self.edit("DASHED", "dashed")
    self.edit("CENTRELINE", "centerline")

    self.edit("LEFT", "left")
    self.edit("RIGHT", "right")

    self.edit("VERTICAL", "vertical")
    # self.edit("SQUARE", "fullwidth")
    # self.edit("IDEOGRAPHIC TELEGRAPH SYMBOL FOR", "telegraph")
    # self.edit("-")
    # self.processAs("Helper Digit Names")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("CJK Compatibility Forms")
