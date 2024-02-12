from assistantLib.glyphNameFormatter.tools import camelCase


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
        self.replace("UPWARDS", "UP")
        self.replace("DOWNWARDS", "DOWN")
        self.replace("POINTING", "")
        self.replace("AND", "")
        self.edit("WITH")
        self.edit("EXTENDED ARABIC-INDIC")
        self.edit("ARABIC LETTER")
        self.camelCase()
    self.compress()


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Arabic Supplement")
