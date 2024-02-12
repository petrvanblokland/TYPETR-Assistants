
def process(self):
    # If the Arabic ligature names comes with any of these terms then these rules apply on components:

    # Initial ligature: FIRST component is INIT and the REST are MEDI
    # Medial ligature: ALL the components are MEDI
    # Final ligature: the LAST component is FINA and the rest are MEDI
    # Isolate ligature: The LAST components is FINA, the fist components is INIT and the rest are MEDI

    # and now we're using camelcase?

    # inevitableExceptions = {
    # #    "ARABIC LIGATURE SHADDA WITH DAMMATAN ISOLATED FORM":   "shaddadamatan",
    # }
    # for k, v in inevitableExceptions.items():
    #     if k == self.uniName:
    #         self.edit(k, v)
    #         return




    if self.processAs("Helper Arabic Ligature Exceptions"):
        return 
        
    if self.has("LIGATURE"):
        self.processAs("Helper Arabic Ligature")
    else:
        self.processAs("Arabic")

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Arabic Presentation Forms-A")
