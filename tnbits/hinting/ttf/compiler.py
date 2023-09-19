#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    wingcompiler.py
#

import re
from tnbits.toolbox.transformer import TX
from tnbits.toolbox.storage.stack import Stack
from tnbits.hinting.ttf.instruction import Instruction
from tnbits.hinting.ttf.program import Program
from tnbits.hinting.ttf.mnemonicset import MnemonicSet

#from tnbits.hinting.storage.hintlib import HintLib

class HintingCompiler:
    """
    The @HintingCompiler@ takes a source of TTX or VTT hints and compiles
    it into a Wing, containing a list of Instructions, one for each mnemonic, supporting
    multiline code, comments, and TTX/VTT like parameters. Seperators between numbers
    can be either comma's or whitespace. The mnemonics are stripped from all white space
    before checked on their name. This allows kinda free format in coding.
    Compiles this source

    src = '''
        NPUSHB[ ]  /* 13 values pushed */  34 0 71 0 7 20 20 5 29 2 7 13 40
        SVTCA[0]
        SRP0[ ]
        MDRP[00100]
        SHP[0]
        MIRP[00100] /* 13 values pushed */
        SHP[0]
        12 23
        43 45
        SVTCA[1],23,34,45 44
        SHP[1]
        MDAP[1]
        SHP[1]
        SHP[1]
        SROUND[ ]
        MDAP[1]
        SHP[1]
        IUP[0]
        IUP[1]
    '''

    into a list of Instructions, that represent:

    ['NPUSHB[ ]',
     '/* 13 values pushed */',
     '34 0 71 0 7 20 20 5 29 2 7 13 40\n',
     'SVTCA[0]',
     'SRP0[ ]',
     'MDRP[00100]',
     'SHP[0]',
     'MIRP[00100]',
     '/* 13 values pushed */',
     'SHP[0]',
     '12 23 43 45\n',
     'SVTCA[1]',
     '23,
    34,
    45 44\n',
     'SHP[1]',
     'MDAP[1]',
     'SHP[1]',
     'SHP[1]',
     'SROUND[ ]',
     'MDAP[1]',
     'SHP[1]',
     'IUP[0]',
     'IUP[1]',
     '']

    Instructions answer different kind of sources, depending on the way their mnemonic is approached.
    Note that the mnemonics have point indices “as is”. No correction has been done yet
    in relation to the inserted points (labeled as such) when the font was read from raw TTF.
    The calling application needs to adjust the point indices in Instructions accordingly.
    """

    # Separate the tokens into (<VTTmnemonic>, <comment>, <number>, <partOfFree>)
    SRC2TOKEN = re.compile(r'[,\s]*([A-Za-z][A-Za-z0123]*\[[A-Za-z0-9\<\>\s]*\])|(/\*.*?\*/)|([0-9\-]+[,\s]*)|([a-z]+[a-z0-9]*)[,\s]*', re.DOTALL)
    STRIPCOMMENT = re.compile('/\*(.*)\*/', re.DOTALL)

    @classmethod
    def compile(cls, src, distributingPushes=True):
        """Compile the TTX of VTT src and generate a set of Instructions from it. The *src*
        attribute can be a string or list/tuple of string."""
        stack = Stack()
        program = Program()
        instruction = None # Holds the current Instruction, in order to add comment or parameters
        freeTokenParts = [] # Hold the free token parts as the are parsed, but not yet recognized.

        if isinstance(src, (list, tuple)):
            src = '\n'.join(src)

        '''
        Raw method for now to see if there are function calls in the src. If
        there are, we cannot do any distribution of pushed values, as it is
        unclear how many values the calls will be using or how many values to
        push back on stack again.

        This a problem, e.g. with Georgia, which has many CALL[] statements in
        the glyph program. In general this may be less of a problem, as glyph
        programs tend to be less optimized and just contain a straight sequence
        of code.

        @@@ Note that the current test assumes no "CALL[" string to be used in
        any comment.

        @@@ Should be parsed more intelligently.
        '''
        if 'CALL[' in src.upper():
            distributingPushes = False

        '''
        Split the source into vttToken, comment, parameter, freeTokenPart,
        where only one of the fields will be filled at the time. So after
        processing one, we can continue to the next set, without checking the
        other values.
        '''

        for vttToken, comment, parameter, freeTokenPart in cls.SRC2TOKEN.findall(src or ''):

            # VTT token is something like MIAP[m<RWh]
            if vttToken:
                '''
                See if there are left over stack values that need to be appended to the
                current (old) instruction, before we make a new new instruction for the current token.
                Clear any leftovers from unrecognized freeToken parts.
                '''
                if instruction is not None and instruction.mnemonic is not None:
                    if instruction.mnemonic.isPush() and not distributingPushes:
                        # We are not distributing, so let the push instruction keep its own
                        # parameters
                        instruction.params = stack.popAll()
                        print('popped all')
                    elif distributingPushes:
                        # Add the right amount of parameters from the stack to the current mnemonic
                        # before we get on to the new one.
                        instruction.params = stack.slicePop(len(instruction.mnemonic.popTypes))
                        print('popped %d' % len(instruction.mnemonic.popTypes))

                # It must be a mnemonic, check if we can find it.
                instruction = Instruction()
                instruction.mnemonic = m = MnemonicSet.getMnemonic(vttToken)
                print('Created new Instruction with opcode %s' % vttToken)

                '''
                Push values on the stack if this is a push token, and don't add it to
                the Wing. If we are not distributing push values, then aways add the instruction.
                Otherwise do add, since it could be a comment.
                m is None: this probably is a instruction with just comments, always output
                not m.isPush: always output
                m.isPush(): only output if not distributingPushes
                '''
                if m is None or not m.isPush() or (m.isPush() and not distributingPushes):
                    program.append(instruction)
                continue

            if comment:
                # Strip the comment code.
                comment = cls.STRIPCOMMENT.findall(comment)[0].strip()
                if instruction is None:
                    instruction = Instruction() # No instruction yet, create one to hold the comment
                    program.append(instruction)
                instruction.comment = comment
                continue

            # Parameter "23"
            if parameter:
                if instruction is None:
                    # Error, not supposed to have parameters before a mnemonic
                    instruction.error = 'No parameters allowed prior to the first mnemonic'

                value = TX.asIntOrNone(parameter)

                if value is None:
                    # Error, cannot convert the parameter to an integer, backout
                    instruction.error = 'Error in parameters "%s"' % parameter
                else:
                    # If distributing the push values, we need these parameters on the stack
                    stack.push(value)

                continue

            # Part of free token
            if freeTokenPart:
                freeTokenParts.append(freeTokenPart)
                # @@@@ Needs to be finished.
                # Conversion using FREEWORDINDEX, etc.
                continue

        '''
        Finalize the last token with the remaining parameters on the stack.
        This amount must match.

        FIXME: Should we check on that? Hint programs might be broken in
        practice.
        '''
        # Just do this, if we are distributing the parameters
        if instruction is not None and instruction.mnemonic and not instruction.mnemonic.isPush() and distributingPushes:
            # Add the right amount of parameters from the stack to the current mnemonic
            # before we get the new one.
            popTypes = instruction.mnemonic.popTypes

            if popTypes is not None:
                needParams = len(popTypes)

                if len(stack) != needParams:
                    instruction.error = 'Error in amount of pushed parameters'

                if len(stack) >= needParams:
                    instruction.params = stack.slicePop(needParams)

        # Answer the compiled wingList and indicate that there are no errors.
        return program, stack

    # ---------------------------------------------------------------------------------------------------------
    #    C O M P I L E  P R O G R A M

    @classmethod
    def compileData(cls, fontOrGlyph, id):
        """
        Force the assembly to be compiled and stored where the TTF font builder
        is expecting it, if doesn't exist yet. It takes the value if it exists,
        otherwise compile a new one. This way it works like a cache, getting
        cleared when the source is replaced.
        """
        assembly = HintLib.getData(fontOrGlyph, id)

        if not assembly:
            # It's not there yet or the source changed, clearing the assembly
            src = HintLib.getSrc(fontOrGlyph, id)

            if src:
                # Force to get the TTX syntax program from this src, as the RoboFont
                # ttxFontCompiler needs TTX syntax, not VTT or free format.
                instructions, error = cls.getInstructionsFromSrc(src)

                if not error:
                    assembly = cls.instructions2Assembly(instructions, ignoreComment=True)
                    HintLib.setData(fontOrGlyph, id, assembly)

        return assembly

    # ---------------------------------------------------------------------------------------------------------
    #    W I N G L E T  S T U F F

    @classmethod
    def getInstructions(cls, glyphOrFont, id=None, distributePushes=False):
        if glyphOrFont is None:
            return None, None # No error, but we just did not get a glyph
        # Always get the src key
        src = HintLib.getSrc(glyphOrFont, id or 'glyf')
        return cls.getInstructionsFromSrc(src, distributePushes)

    @classmethod
    def getInstructionsFromSrc(cls, src, distributePushes=True):
        instructions, error = cls.compile(src, distributePushes)
        if error is None:
            # Check if this is raw data, otherwise perform a point index conversion
            pass
        return instructions, error

    @classmethod
    def getAssembly(cls, glyphOrFont, id=None, ignoreComment=False):
        """
        Get instructions without distributed pushes
        This assembly is compiled live, not taken from the font/glyph lib.
        For recompile of that cache, set the source (in any format) in the
        lib through HintLib.setData(), which will clear the assembly.
        Which will force the compileData to work for the next font that
        is generated.
        """
        instructions, error = cls.getInstructions(glyphOrFont, id or 'glyf', False)
        return cls.instructions2Assembly(instructions, ignoreComment)

    @classmethod
    def instructions2Assembly(cls, instructions, ignoreComment=False):
        output = []
        for instruction in instructions:
            output.append(instruction.asAssembly(ignoreComment))
        return '\n'.join(output)

    @classmethod
    def getVtt(cls, glyphOrFont, id=None):
        # Distribute the pushes is default
        instructions, error = cls.getInstructions(glyphOrFont, id or 'glyf', True)
        return cls.instructions2Vtt(instructions)

    @classmethod
    def instructions2Vtt(cls, instructions):
        output = []
        for instruction in instructions:
            output.append(instruction.asVtt())
        return '\n'.join(output)

    @classmethod
    def getFree(cls, glyphOrFont, id=None):
        # Distribute the pushes is default
        instructions, error = cls.getInstructions(glyphOrFont, id or 'glyf', True)
        return cls.instructions2Free(instructions)

    @classmethod
    def instructions2Free(cls, instructions):
        output = []
        for instruction in instructions:
            output.append(instruction.asFree())
        return '\n'.join(output)

if __name__ == "__main__":
    sources = ['''
        NPUSHB[ ]  /* 13 values pushed */ 34 0 71 0 7 20 20 5 29 2 7 13 40
        SVTCA[0]
        SRP0[ ]
        MDRP[00100]
        SHP[0]
        MIRP[00100]
        SHP[0]
        SVTCA[1]
        SHP[1]
        MDAP[1]
        SHP[1]
        SHP[1]
        SROUND[]
        MDAP[1]
        SHP[1]
        IUP[0]
        IUP[1]
        ''',

        '''
        PUSHB[] 12 32 34 45 56
        CALL[]
        SVTCA[1]
        SVTCA[0]
        MDRP[01001] /* Both formats allowed */
        MDRP[m>rBl]
        PUSHB[] 23 34 45 56
        LOOPCALL[]
        PUSHB[] 56 67 78
        LOOPCALL[]
        ''',
    ]
    for src in sources:
        print('-Running-')
        program, stack = HintingCompiler.compile(src)
        print('-Program Result-')
        print(program.dump())
        print(stack)
