# Using joiningtypes we can predict which connecting variants are needed for a specific
# Arabic unicode. We can add the init, medi, fina extensions. Some of these new names
# might also have their own, deprecated, presentation form unicode value. 
# Bahman advises to add these presentation form unicodes for legacy reasons.
# Well, if we have the data, why not. 
# This script finds out which generateed variant names do not habe matching presentation form unicodes.
# This should not be a problem - but if there are names that do have values, but perhaps
# there is a naming mismatch that could be adjusted. 

import os
from pprint import pprint
from assistantLib.glyphNameFormatter.reader import *
arabicRanges = []
for name in rangeNames:
    if "Ara" in name:
        arabicRanges.append(name)
print(arabicRanges)

def getAllNames(name):
    global joiningTypes
    # based on the category data, give suggestion for which extensions we need for any unicode
    extensions = {
        # XXXX no idea if it works this way...
        #   D Dual_Joining
        # 		&----G----&
        'D': ['init', 'medi', 'fina'],
        #   C Join_Causing
        # 		&----G----&		????
        'C': [         					   ],
        #   R Right_Joining
        # 		   x G----&
        'R': [ 				 'fina'],
        #   L Left_Joining
        # 		&----G x
        'L': ['init',		 'fina'],
        #   U Non_Joining
        # 	       x G x
        'U': [         					   ],
        #   T Transparent
        # 	       x G x
        'T': [         					   ],
    }

    if joiningTypes is not None:
        variants = [name]
        uniValue = n2u(name)
        if uniValue is not None:
            ext = joiningTypes.get(uniValue)
            ext = extensions.get(ext)
            if ext:
                for e in ext:
                    variants.append("%s.%s"%(name, e))
    return variants

def readJoiningTypes(path):
    # read the joiningTypes.txt
    joiningTypes = {}
    f = open(path, 'r')
    d = f.read()
    f.close()
    lines = d.split("\n")
    for l in lines:
        if not l: continue
        if l[0] == "#": continue
        parts = l.split("\t")
        uni = int('0x'+parts[0], 0)
        jT = parts[1]
        joiningTypes[uni] = jT
    return joiningTypes

import assistantLib.glyphNameFormatter
jTPath = os.path.join(os.path.dirname(glyphNameFormatter.__file__), "data", "joiningTypes.txt")
joiningTypes = readJoiningTypes(jTPath)
#print('joiningTypes', joiningTypes)

noPresentationForms = {}
for rangeName in arabicRanges:
    rangeMin, rangeMax = getRangeByName(rangeName)
    for num in range(rangeMin, rangeMax):
        name = u2n(num)
        allNames = getAllNames(name)
        show = False
        for variantName in allNames:
            variantUniValue = n2u(variantName)
            if variantUniValue is None:
                if variantName is None:
                    continue
                if not show:
                    show = True
                    noPresentationForms[hex(num)] = allNames

#print(len(noPresentationForms), "connecting variants without presentation forms according to our list.")

print("these univalues + names have no presentation form unicode values")
pprint(noPresentationForms)