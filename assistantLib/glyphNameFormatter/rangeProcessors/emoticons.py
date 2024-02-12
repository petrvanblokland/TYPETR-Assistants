

def process(self):
    # just to test unicode 8 stuff
    # not complete
    self.replace("-", " ")
    self.camelCase()
    self.compress()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Emoticons")
