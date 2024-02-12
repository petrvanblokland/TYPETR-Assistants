
def process(self):
    self.processAs("Georgian")
    if self.has("GEORGIAN SMALL LETTER"):
        self.suffix("Geok")	#Nuskhuri


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Georgian Supplement")
