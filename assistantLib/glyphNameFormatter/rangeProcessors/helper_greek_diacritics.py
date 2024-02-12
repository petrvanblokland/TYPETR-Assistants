
def process(self):

    parts = {
        'PROSGEGRAMMENI'    :   "iotasub",
        'YPOGEGRAMMENI'     :   "iotasub",
        'PERISPOMENI'       :   "tilde",
        'VARIA'             :   "grave",
        'PSILI'             :   "lenis",
        'DIALYTIKA'         :   "dieresis",
        'VRACHY'            :   "breve",
        'OXIA'              :   "acute",
        'DASIA'             :   "asper",
        "TONOS"             :   "tonos",
    }

    for prefix in ["WITH ", "AND ", ""]:
        for p in parts.keys():
            self.replace(prefix+p, parts[p])
    # output from Greek and Coptic will be lowercase
    for prefix in ["with ", "and ", ""]:
        for p in parts.keys():
            self.replace((prefix+p).lower(), parts[p])

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    from assistantLib.glyphNameFormatter.tools import debug
    printRange("Greek Extended")
    debug(0x1FF2)
