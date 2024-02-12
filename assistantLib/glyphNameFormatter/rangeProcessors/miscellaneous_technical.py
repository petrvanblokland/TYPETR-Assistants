
def process(self):
    # edits go here
    # self.edit("ARMENIAN")
    # self.handleCase()
    self.edit("X IN A RECTANGLE BOX", "clear")

    self.edit("UPPER LEFT OR LOWER RIGHT", "upleftlowerright")
    self.edit("UPPER RIGHT OR LOWER LEFT", "uprightlowerleft")

    self.edit("SYMBOL")
    self.edit("WITH")
    self.edit("LIGHT")
    self.edit("LINE-")
    self.edit("BETWEEN")
    self.edit("KEY")
    self.edit("TO THE")
    self.edit("APL")
    self.edit("I-BEAM", "beam")
    self.edit("LESS-THAN", "less")
    self.edit("GREATER-THAN", "greater")

    self.edit("UPWARDS", "up")
    self.edit("UPPER", "up")
    self.edit("DOWNWARDS", "down")
    self.edit("LEFTWARDS", "left")
    self.edit("RIGHTWARDS", "right")

    self.replace("UNDERBAR", "underline")

    self.edit("TORTOISE SHELL", "shell")
    self.replace("PARENTHESIS", "paren")

    self.edit("OPEN-CIRCUIT-OUTPUT", "opencircuit")
    self.edit("PASSIVE-PULL-DOWN-OUTPUT", "passivedown")
    self.edit("PASSIVE-PULL-UP", "passiveup")
    self.replace("-TYPE", "type")

    parts = [
        "UP", "DOWN", "TOP", "BOTTOM",
        "TURNED",
        "HORIZONTAL", "VERTICAL",
        "LEFT", "RIGHT",
        "SQUARE", "CURLY",
        "METRICAL",
        "WHITE",
        ]
    for part in parts:
        self.edit(part, part.lower())

    self.processAs("helper_numbers")

    self.edit("FUNCTIONAL", "func")

    self.edit("AND")
    self.edit("-")

    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Miscellaneous Technical")
