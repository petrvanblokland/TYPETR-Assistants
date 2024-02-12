
def process(self):
    self.replace("THERE DOES NOT EXIST", "notexistential")
    self.replace("DOES NOT CONTAIN AS MEMBER", "notcontains")

    self.edit("DOUBLE", "dbl")
    self.edit("TRIPLE", "tpl")
    self.edit("CONTOUR", "contour")
    self.edit("SURFACE", "surface")
    self.edit("VOLUME", "volume")
    self.edit("ANTICLOCKWISE", "anticlockwise")
    self.edit("CLOCKWISE", "clockwise")
    self.edit("SMALL", "small")
    self.edit("N-ARY", "array")
    self.edit("REVERSED", "reversed")
    self.edit("INVERTED", "inverted")
    self.edit("MIDLINE", "mid")
    self.edit("VERTICAL BAR", "verticalbar")
    self.edit("VERTICAL", "vertical")
    self.edit("HORIZONTAL BAR", "horizontalbar")
    self.edit("HORIZONTAL", "horizontal")
    self.edit("DIAGONAL", "diagonal")
    self.edit("UP", "up")
    self.edit("DOWN", "down")
    self.edit("RIGHT", "right")
    self.edit("LEFT", "left")
    self.edit("STROKE", "stroke")

    self.replace("LESS-THAN", "less")
    self.replace("GREATER-THAN", "greater")
    self.replace("OPERATOR", "operator")
    self.replace("WITH")
    self.replace("LONG", "long")
    self.replace("SIGN")
    self.replace("-OR-")
    self.replace("TO")
    self.replace("THE")
    self.replace("AT END")
    self.replace("OF")

    self.lower()
    self.compress()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Mathematical Operators")
