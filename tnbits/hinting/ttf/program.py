# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     program.py
#
class Program(object):

    def __init__(self, name):
        self.name = name
        self._instructions = []

    def __getitem__(self, index):
        if 0 <= index < len(self._instructions):
            return self._instructions[index]

        return None

    def __setitem__(self, index, instruction):
        self._instructions[index] = instruction

    def __len__(self):
        return len(self._instructions)

    def __repr__(self):
        s = '[Program length:%d]' % len(self._instructions)
        for i in self._instructions:
            s += '\n\t' + str(i)

        return s

    def asList(self):
        """Transform the list of instructions to a list of VTT mnemonic sources."""
        instructionsList = []

        for instruction in self._instructions:
            instructionsList.append(instruction.asVtt())

        return instructionsList

    def append(self, instruction):
        self._instructions.append(instruction)

    #   self.instructions

    def _get_instructions(self):
        return self._instructions

    def _set_instructions(self, instructions):
        self._instructions = instructions

    def dump(self, maxLines=None):
        """
        Answers the program source dump.
        """
        t = []
        i = 0

        for instruction in self._instructions:
            t.append(str(instruction))
            i += 1
            if not maxLines is None and i >= maxLines:
                break

        if not maxLines is None and maxLines < len(self._instructions):
            t.append('...')

        return '\n'.join(t)

    instructions = property(_get_instructions, _set_instructions)
