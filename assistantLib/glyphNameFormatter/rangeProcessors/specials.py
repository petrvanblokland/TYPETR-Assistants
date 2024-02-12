

def process(self):
    self.edit("ANNOTATION")
    self.edit("CHARACTER", "char")
    self.edit("OBJECT", "obj")
    self.lower()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Specials")
