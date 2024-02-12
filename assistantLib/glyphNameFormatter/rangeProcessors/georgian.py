
def process(self):
    # edits go here
    self.edit("GEORGIAN PARAGRAPH SEPARATOR", "paragraphseparator")
    self.edit("MODIFIER LETTER GEORGIAN NAR", "narmodGeor")
    self.edit("GEORGIAN LETTER HARD SIGN", "hardsignGeor")
    self.edit("GEORGIAN LETTER LABIAL SIGN", "labialsignGeor")

    self.edit("GEORGIAN")
    self.handleCase()
    if self.has("GEORGIAN LETTER") and  self.uniNumber not in [0x10FC, 0x10FE, 0x10FF]:
        self.edit("LETTER")
        self.suffix("Geor") #Mkhedruli
        self.lower()
    elif self.has("GEORGIAN CAPITAL LETTER"):
        self.suffix("Geok") #Asomtavruli
    self.compress()
    if self.has("GEORGIAN PARAGRAPH SEPARATOR"):
        self.scriptPrefix()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Georgian")
