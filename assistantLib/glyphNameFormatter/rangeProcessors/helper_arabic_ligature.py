from __future__ import print_function
from assistantLib.glyphNameFormatter.tools import camelCase


def process(self):
    # interpret an arabic ligature from the parts

    # If the Arabic ligature names comes with any of these terms then these rules apply on components:
    # Initial ligature: FIRST component is INIT and the REST are MEDI
    # Medial ligature: ALL the components are MEDI
    # Final ligature: the LAST component is FINA and the rest are MEDI
    # Isolate ligature: The LAST components is FINA, the fist components is INIT and the rest are MEDI

    parts = self.uniName.split(" ")

    # get the type, initial, medial, final or isolated.
    ligatureType = 'other'
    lastNameIndex=len(parts)
    if parts[-2] == "INITIAL" and parts[-1] == "FORM":
        ligatureType = "initial"
        lastNameIndex=-2
    elif parts[-2] == "MEDIAL" and parts[-1] == "FORM":
        ligatureType = "medial"
        lastNameIndex=-2
    elif parts[-2] == "FINAL" and parts[-1] == "FORM":
        ligatureType = "final"
        lastNameIndex=-2
    elif parts[-2] == "ISOLATED" and parts[-1] == "FORM":
        ligatureType = "isolated"
        lastNameIndex=-2
    ligatureMarkIndex = parts.index("LIGATURE")

    # next, find out how many ligating parts we have in this name
    # assume all parts are connected with "WITH"*
    # (there are other ligatures that we can not reconstruct.)
    withCount = parts.count("WITH")
    ligatureParts = []
    if withCount == 0:
        # ligatures with 1 ligating part
        nameParts = parts[ligatureMarkIndex+1:lastNameIndex]
        ligatureParts = [nameParts]
    elif withCount == 1:
        # ligatures with 2 ligating part
        withIndex1 = parts.index("WITH")
        nameParts1 = parts[ligatureMarkIndex+1:withIndex1]
        nameParts2 = parts[withIndex1+1:lastNameIndex]
        ligatureParts = [nameParts1, nameParts2]
    elif withCount == 2:
        # ligatures with 3 ligating part
        withIndex1 = parts.index("WITH")
        withIndex2 = parts.index("WITH", withIndex1+1)
        nameParts1 = parts[ligatureMarkIndex+1:withIndex1]
        nameParts2 = parts[withIndex1+1:withIndex2]
        nameParts3 = parts[withIndex2+1:lastNameIndex]
        ligatureParts = [nameParts1, nameParts2, nameParts3]
    elif withCount > 2:
        # ligatures with 2 ligating part
        print("ERROR: more than 2 ligating parts")
        print("\n", self.uniName)
        print("\t", len(ligatureParts), ligatureParts[0])
        print("\t", ligatureType)
        return

    # now let's add the initial, medial, final, isolated form extension to the ligating parts.
    if len(ligatureParts)==1:
        # logotypes and so on
        # camel case
        self.uniNameProcessed = "".join([camelCase(p) for p in ligatureParts[0]])
    elif len(ligatureParts)>=2:
        if ligatureType == "initial":
            # Initial ligature: FIRST component is INIT and the REST are MEDI
            ligatureParts[0].append(".init")
            for part in ligatureParts[1:]:
                part.append(".medi")
        elif ligatureType == "medial":
            # Medial ligature: ALL the components are MEDI
            for part in ligatureParts:
                part.append(".medi")
        elif ligatureType == "final":
            # Final ligature: the LAST component is FINA and the rest are MEDI
            for part in ligatureParts[:-1]:
                part.append(".medi")
            ligatureParts[-1].append(".fina")
        elif ligatureType == "isolated":
            # Isolate ligature: The LAST components is FINA, the fist components is INIT and the rest are MEDI
            for part in ligatureParts[1:-1]:
                part.append(".medi")
            ligatureParts[-1].append(".fina")
            ligatureParts[0].append(".init")
        else:
            print("ERROR: unknown ligature structure")
            print("\n", self.uniName)
            print("\t", len(ligatureParts), ligatureParts[0])
            print("\t", ligatureType)
            return
        # assembly
        self.uniNameProcessed = ""
        ligaName = []
        for p in ligatureParts:
            ligaName.append("".join(p).lower())
        self.uniNameProcessed = "_".join(ligaName)

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter import GlyphName
    assert GlyphName(uniNumber=0xFDFA).getName() == "SallallahouAlayheWasallam"
    assert GlyphName(uniNumber=0xFDC4).getName() == "ain.init_jeem.medi_meem.medi"
    assert GlyphName(uniNumber=0xFC5D).getName() == "alefmaksura.init_superscriptalef.fina"
    assert GlyphName(uniNumber=0xFC40).getName() == "lam.init_hah.fina"
    assert GlyphName(uniNumber=0xFBFC).getName() == "yehfarsi.isol"

    print("\ndoNotProcessAsLigatureRanges", doNotProcessAsLigatureRanges)
    odd = 0xfe76
    for a, b in doNotProcessAsLigatureRanges:
        print('\nrange:',hex(a) , hex(odd), hex(b))
        print( a <= odd <= b,)
        for u in range(a,b+1):
            try:
                g = GlyphName(uniNumber=u)
                n = g.getName()
                # print(g.uniNumber)
                print(u, hex(a), hex(u), hex(b), n, g.uniName)
                #print( a <= u <= b,)
                
            except:
                import traceback
                traceback.print_exc()
