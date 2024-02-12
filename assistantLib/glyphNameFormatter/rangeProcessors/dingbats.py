
def process(self):
    self.replace("MARK")
    self.replace("SYMBOL")
    self.replace("TRIFOLIATE")

    self.replace("RECTILINEAR", "compas")

    self.edit("TEARDROP-SPOKED", "teardrop")
    self.edit("TEARDROP-BARBED", "teardrop")
    self.edit("TEARDROP-SHANKED", "teardrop")

    self.edit("BALLOON-SPOKED", "balloon")
    self.edit("CLUB-SPOKED", "club")

    self.edit("RIGHT-SHADOWED", "shadow")
    self.edit("DROP-SHADOWED", "shadow")

    self.edit("RIGHTWARDS", "right")
    self.edit("LEFTWARDS", "left")
    self.edit("OPEN-OUTLINED", "outlinedopen")
    self.edit("WEDGE-TAILED", "wedge")
    self.edit("-FEATHERED", "feathered")
    self.edit("NOTCHED", "notched")

    self.edit("FRONT-TILTED", "fronttilted")
    self.edit("BACK-TILTED", "backtilted")

    self.edit("RIGHT-SHADED", "rightshaded")
    self.edit("LEFT-SHADED", "leftshaded")

    self.edit("CONCAVE-POINTED", "pointed")
    self.edit("RIGHT-POINTING", "rightpointed")
    self.edit("LEFT-POINTING", "leftpointed")

    self.edit("ROUND-TIPPED", "round")
    self.edit("TRIANGLE-HEADED", "triangle")
    self.edit("WIDE-HEADED", "wide")

    self.edit("THREE-D", "threeD")

    self.edit("BOTTOM-LIGHTED", "bottomlight")
    self.edit("TOP-LIGHTED", "toplight")

    self.edit("SANS-SERIF", "sans")
    self.edit("NEGATIVE", "negative")

    self.edit("CURVED UPWARDS", "curveup")
    self.edit("CURVED DOWNWARDS", "curvedown")

    self.edit("DRAFTING POINT", "pointed")

    self.edit("TORTOISE SHELL", "shell")

    self.edit("COMMA QUOTATION", "comma")
    self.replace("SINGLE")

    self.editToFinal("SOUTH", "S")
    self.editToFinal("NORTH", "N")
    self.editToFinal("EAST", "E")
    self.editToFinal("WEST", "W")

    hasDingbat = self.has("DINGBAT")

    parts = [
        "VICTORY", "WRITING",
        "UPPER", "LOWER", "CENTRE",
        "RIGHT", "LEFT",
        "OUTLINED", "OPEN", "SHADOWED", "POINTED", "DASHED", "SQUAT", "ANGLE", "FLATTENED", "ROTATED",
        "BLADE", "STRESS", "CIRCLED", "OPEN", "PINWHEEL", "PETALLED", "PROPELLER", "TIGHT",

        "BLACK", "WHITE", "HEAVY", "LIGHT", "MEDIUM", "DOUBLE", "TURNED", "ORNAMENT"
        ]

    if not hasDingbat:
        parts.extend([
            "SIXTEEN", "FOUR", "SIX", "EIGHT", "TWELVE",
            ])

    for part in parts:
        self.edit(part, part.lower())

    if hasDingbat:
        self.replace("DINGBAT")
        self.replace("NUMBER")
        self.replace("DIGIT")
        # self.final(".dingbat")

    self.replace("AND")

    self.compress()
    self.lower()
    #self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Dingbats")
