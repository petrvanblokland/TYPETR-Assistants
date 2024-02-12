
def process(self):
    self.uniNameProcessed = "private_use_%04X"%self.uniNumber

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Private Use Area")
