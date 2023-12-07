from glyphNameFormatter.tools import camelCase

def process(self):
    # If the Arabic ligature names comes with any of these terms then these rules apply on components:

    # Initial ligature: FIRST component is INIT and the REST are MEDI
    # Medial ligature: ALL the components are MEDI
    # Final ligature: the LAST component is FINA and the rest are MEDI
    # Isolate ligature: The LAST components is FINA, the fist components is INIT and the rest are MEDI
    if "WITH" in self.uniName:
        parts = self.uniName.split(" ")
        withIndex = parts.index("WITH")
        withParts = parts[withIndex+1:]
        nameParts = parts[:withIndex]
        if nameParts[0] == 'ARABIC':
            nameParts = nameParts[1:]
        if nameParts[0] == 'LETTER':
            nameParts = nameParts[1:]

        self.edit("WITH")
        self.edit("EXTENDED ARABIC-INDIC")
        self.edit("ARABIC LETTER")
        for p in nameParts:
            self.replace(p, camelCase(p.lower()))
        for p in withParts:
            self.replace(p, camelCase(p.lower()))

    self.compress()
    #if self.has("LIGATURE"):
    #    self.processAs("Helper Arabic Ligature")
    #else:
    #    self.processAs("Arabic")

if __name__ == "__main__":
    from glyphNameFormatter.exporters import printRange
    printRange("Arabic Supplement")
