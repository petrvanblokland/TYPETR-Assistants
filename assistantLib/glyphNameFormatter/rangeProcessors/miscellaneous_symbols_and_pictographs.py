
def process(self):
    self.replace("EUROPE-AFRICA", "Europe Africa")
    self.replace("ASIA-AUSTRALIA", "Asia Australia")
    self.edit("SYMBOL", "")
    self.replace("FORK AND KNIFE", "fork knife")
    self.replace("WITH PLATE", "plate")
    self.replace("SNOW CAPPED", "snowcapped")
    self.edit("WITH", "")
    self.replace("JACK-O-LANTERN", "jack O Lantern")
    self.edit("UP-POINTING", "Up")
    self.edit("UP-POINTING", "Up")
    self.edit("DOWN-POINTING", "DOwn")
    self.replace("PERFORMING", "Performing")

    self.edit("FOR", "")
    self.camelCase()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Miscellaneous Symbols and Pictographs")
