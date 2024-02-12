from __future__ import print_function
from assistantLib.glyphNameFormatter.tools import camelCase


doNotProcessAsLigatureRanges = [
    (0xfc5e, 0xfc63), 
    (0xfe70, 0xfe74), 
    #(0xfc5e, 0xfc61), 
    (0xfcf2, 0xfcf4), 
    (0xfe76, 0xfe80), 
]


def process(self):
    # Specifically: do not add suffixes to these ligatures,
    # they're really arabic marks

    for a, b in doNotProcessAsLigatureRanges:
        if a <= self.uniNumber <= b:
            self.replace('TAIL FRAGMENT', "kashida Fina")
            self.replace('INITIAL FORM', "init")
            self.replace('MEDIAL FORM', "medi")
            self.replace('FINAL FORM', "fina")
            self.replace('ISOLATED FORM', "isol")
            self.replace('WITH SUPERSCRIPT', "")
            self.replace('WITH', "")
            self.replace("LIGATURE", "")
            self.replace("ARABIC", "")
            self.replace("SYMBOL", "")
            self.replace("LETTER", "")
            self.lower()
            self.camelCase()
            return True

    return False


if __name__ == "__main__":
    from assistantLib.glyphNameFormatter import GlyphName

    print("\ndoNotProcessAsLigatureRanges", doNotProcessAsLigatureRanges)
    odd = 0xfe76
    for a, b in doNotProcessAsLigatureRanges:
        for u in range(a,b+1):
            try:
                g = GlyphName(uniNumber=u)
                n = g.getName()
                print(hex(u), n, g.uniName)
                
            except:
                import traceback
                traceback.print_exc()
