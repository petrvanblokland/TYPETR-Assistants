
def process(self):
    self.replace("EURO-CURRENCY", "euroarchaic")
    self.replace("EURO", "Euro")
    self.replace("SIGN")
    self.compress()
    if not self.has("EURO"):
        self.lower()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Currency Symbols")
