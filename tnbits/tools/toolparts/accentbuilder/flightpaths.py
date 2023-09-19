from tnbits.tools.constantsparts.codepages import CodePages
from tnbits.tools.toolparts.accentbuilder.instructions import INSTRUCTIONS
#from glyphNameFormatter.data import unicode2name_AGD

FLIGHTPATHS_INSTRUCTIONS = {}
for flightpath, unicodes in CodePages.DEFAULT_FLIGHTPATHS.items():
    FLIGHTPATHS_INSTRUCTIONS[flightpath] = {}
    '''
    for unicode in unicodes:
        if unicode in unicode2name_AGD:
            name = unicode2name_AGD[unicode]
            if name in INSTRUCTIONS.keys():
                FLIGHTPATHS_INSTRUCTIONS[flightpath][name] = INSTRUCTIONS[name]
    '''
