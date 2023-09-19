# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    function.py
#
from tnbits.hinting.ttf.program import Program

class Function(Program):
    pass

    def __init__(self, functionDef):
        self.functionDef = functionDef
        super(Function, self).__init__(functionDef)

    def __repr__(self):
        s = '[Function def: %d, length: %d]' % (self.functionDef, len(self._instructions))

        for i in self._instructions:
            s += '\n\t' + str(i)

        return s
