
def process(self):
    self.edit("MATHEMATICAL")

    self.edit("EPSILON SYMBOL", "epsilonsymbol")
    self.edit("CAPITAL THETA SYMBOL", "Thetasymbol")
    self.edit("THETA SYMBOL", "thetasymbol")
    self.edit("KAPPA SYMBOL", "kappasymbol")
    self.edit("PHI SYMBOL", "phisymbol")
    self.edit("PI SYMBOL", "pisymbol")
    self.edit("RHO SYMBOL", "rhosymbol")

    self.edit("MONOSPACE", "mono")
    self.edit("BOLD ITALIC", "bolditalic")
    self.edit("ITALIC", "italic")
    self.edit("BOLD", "bold")
    self.edit("SANS-SERIF", "sans")
    self.edit("FRAKTUR", "fraktur")
    self.edit("BLACK-LETTER", "fraktur")
    self.edit("PARTIAL DIFFERENTIAL", "partialdiff")
    self.edit("DOUBLE-STRUCK", "dblstruck")
    self.edit("SCRIPT", "script")
    self.edit("NABLA", "nabla")

    self.handleCase()



    if self.has("DIGIT"):
        self.edit("DIGIT")
        self.lower()

    self.compress()
    #self.scriptPrefix()
    

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Mathematical Alphanumeric Symbols")
