
def process(self):

    self.replace("SQUARE WITH UPPER LEFT TO LOWER RIGHT FILL", "squareupperlefttolowerrightfill")
    self.replace("SQUARE WITH UPPER RIGHT TO LOWER LEFT FILL", "squareupperrighttolowerleftfill")

    ignores = [
        "WITH"
        ]
    for ignore in ignores:
        self.replace(ignore)

    self.replace("ROUNDED CORNERS", "round")
    self.replace("CONTAINING", "with")

    self.replace("WHITE SQUARE", "squarewhite")
    self.replace("BLACK SQUARE", "squareblack")
    self.replace("WHITE DIAMOND", "diamondwhite")
    self.replace("BLACK DIAMOND", "diamondblack")

    self.edit("UP-POINTING", "up")
    self.edit("RIGHT-POINTING", "right")
    self.edit("LEFT-POINTING", "left")
    self.edit("DOWN-POINTING", "down")

    parts = [
        "INVERSE",
        "VERTICAL", "HORIZONTAL",
        "SMALL", "FILL",
        "DOTTED", "MEDIUM", "LEFT", "RIGHT", "BLACK", "WHITE"
        ]
    for part in parts:
        self.edit(part, part.lower())

    self.compress()
    self.lower()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Geometric Shapes")
