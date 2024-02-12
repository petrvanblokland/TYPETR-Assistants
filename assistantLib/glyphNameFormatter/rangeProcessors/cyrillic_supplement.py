
def process(self):
    # edits go here
    # self.edit("ARMENIAN")
    # self.handleCase()
    # self.compress()
    #self.edit("REVERSED")
    if self.has("REVERSED"):
    	self.replace("REVERSED", "reversed")
    if self.has("MIDDLE"):
        self.replace("MIDDLE", "middle")
        self.edit("WITH")
    self.processAs("Cyrillic")
    self.compress()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Cyrillic Supplement")
