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
#    simulator.py
#


import traceback

from tnbits.toolbox.transformer import TX
from tnbits.toolbox.storage.stack import Stack
from tnbits.hinting.ttf.objects.vector import Vector
from tnbits.hinting.ttf.graphicsstate import GraphicsState
from tnbits.hinting.ttf.instructions import Instructions
from tnbits.hinting.ttf.flow import Flow
from tnbits.hinting.ttf.ttfaux import Aux
from tnbits.hinting.ttf.log import Log
from tnbits.hinting.ttf.math import Math
from tnbits.hinting.ttf.g import Globals
from tnbits.hinting.ttf.objects.vector import Vector
from tnbits.hinting.ttf.instruction import Instruction
from tnbits.hinting.ttf.mnemonicset import MnemonicSet
from tnbits.hinting.ttf.program import Program
from tnbits.hinting.ttf.errors.exceptions import *
from fontTools.ttLib import *

DEBUG = False

class Simulator(Instructions, Flow, Aux, Log, Math, Globals):
    """
    Main *Simulator* class, reads TrueType file and runs @Instruction@
    instances.
    """

    ttf = None
    em = None
    glyphName = None
    fontName = None
    gstate = None
    fpgm = None
    prep = None
    glyph = None
    valid = True
    mode = None

    i = 0

    _log = []
    _errors = []

    # Initialization, setting up.

    def __init__(self, ttf, fontName='', verbose=False):
        """Create the root adapter and hold the reference.
            >>> from fontTools.ttLib import TTFont
            >>> from tnTestFonts import getFontPath
            >>> from tnbits.model.floqmodel import floqModel
            >>> name = "CusterRE-RegularS2.ttf"
            >>> path = getFontPath(name)
            >>> font = TTFont(path)
            >>> s = Simulator(font)
            >>> s.setGlyph('H', 12)
        """
        print(' * (Simulator) Creating new simulator for %s' % ttf)
        self.ttf = ttf
        self.em = self.ttf['head'].unitsPerEm
        self.fontName = fontName
        self.verbose = verbose

        # Variables for program flow, such as step indices and break points.
        self.lastInstructions = []

        # Indices for stepping, managed by specific functions. Should be
        # remembered over several runs of same font program / preprogram / glyph.
        self.stepIndices = self.initializeStepIndices()

        # Live indices, keeps track of location inside nested program loops. Is reset
        # for each font program / preprogram / glyph run.
        self.loopIndices = {}

        # Manually set breakpoints.
        self.breakPoints = {}
        self.scanFont()

    def initializeStepIndices(self):
        """
        Sets up the dictionary structure for keeping track of the step indices.

        key: mode
        subkey: level

        for each level:

        'index': integer or None
        'program': program name

        At level zero, program can be either 'prep' or 'glyph', one index should always be None,
        while the other is an integer.

        Larger-than-zero (>0) levels should be consecutive.  Any >0 level is a
        call. For example, a level 1 function is started by a call inside
        either the 0-level prep or glyph instruction sets. A level 2 call is
        inside the instructions of a function. Once the program at a >0 level
        has run until the end, the level should be removed from the dictionary.
        """
        indices = {}
        indices['prep'] = {0: {'index': 0, 'program': 'prep'}}
        indices['glyph'] = {0: {'index': None, 'program': 'glyph'}}

        return indices

    def scanFont(self):
        """
        Scans the font for glyph names and character mappings.
        """
        if self.ttf is None:
            return

        self.characterMap = {}
        self.glyphKeys = None

        if 'cmap' in self.ttf:
            print(' * (Simulator) Number of tables in character map is %d' % len(self.ttf['cmap'].tables))

            for table in self.ttf['cmap'].tables:
                # Load just one table. TODO: Which one?

                if table.format == 4:
                    print(' * (Simulator) Using character map with format %d, %d glyphs' % (table.format, len(table.cmap)))
                    for pair in table.cmap.items():
                        self.addToRange(pair)
                    break
                elif table.format == 0:
                    print(' * (Simulator) Using character map with format %d, %d glyphs' % (table.format, len(table.cmap)))
                    for pair in table.cmap.items():
                        self.addToRange(pair)
                    break
                else:
                    print(table.format)

        if 'glyf' in self.ttf:
            self.glyphKeys = self.ttf['glyf'].keys()

    def setGlyph(self, glyphName, ppem):
        """
        Resets the simulator by clearing logs and initializing the graphics
        state. Doesn't clear step indices so the simulator remembers where
        it stopped on the previous run.
        """
        self.glyphName = glyphName
        self.valid = True
        self.resetLogs()
        self.mode = None
        self.gstate = self.newGraphicsState(glyphName, ppem)

    def getTTGlyph(self, glyphName):
        """
        Tries to retrieve the glyph from TrueType.
        """
        if glyphName in self.ttf['glyf']:
            return self.ttf['glyf'][glyphName]
        else:
            ' * (Simulator) Could not find glyph %s in the glyf table' % glyphName

    def newGraphicsState(self, glyphName, ppem):
        """
        Creates a new graphics state for the TrueType font with ``glyphName``
        and size ``ppem``.
        """
        glyph = self.getTTGlyph(glyphName)
        maxp = self.getInitializedMaxP()
        metrics = self.getInitializedMetrics(ppem)
        cvt = self.getCVTAsList()
        return GraphicsState(cvt=cvt, glyph=glyph, metrics=metrics, maxp=maxp, simulator=self)

    # Instructions.

    def stop(self):
        """
        Should be called when all instructions have been executed, removes gstate and
        sets indices to initial values.
        """
        self.gstate = None
        self.resetStepIndices('prep', 0)
        self.resetStepIndices('glyph', None)

    def runFpgm(self, stepIndex=None):
        """
        Chops up the font program into separate functions to be executed
        from the preprogram (PREP).
        """
        print('Running FPGM')

        if isinstance(self.fpgm, Program):
            self.mode = 'fpgm'
            self.runProgram(self.fpgm, stepIndex=stepIndex)

        if self.verbose is True:
            self.message('Ran FPGM.')

    def runPrep(self, stepIndex=None, step=None, topLevelIndex=None, isCall=False):
        """
        TODO: runPrep and RunGlyph in single function?
        Run the Preprogram (PREP).

        Runs to a specific point if ``stepIndex`` is specified. Else, steps
        over or into the next instruction depending on the ``step`` parameter.
        """
        self.resetLogs()
        print('Running PREP')

        if step == 'into':
            assert isCall is True

        i, mode = self.getStepIndex('prep', stepIndex=stepIndex, step=step, topLevelIndex=topLevelIndex)

        if isinstance(self.prep, Program):
            try:
                self.mode = 'prep'
                self.runProgram(self.prep, stepIndex=i, step=step)
            except AssertionError as e:
                print(traceback.format_exc())
                self.valid = False
                raise e

            return i, self.lastInstructions, mode

    def runGlyph(self, stepIndex=None, step=None, topLevelIndex=None, isCall=False):
        """
        TODO: runPrep and RunGlyph in single function?
        Run the glyph program.

        Runs to a specific point if ``stepIndex`` is specified. Else, steps
        over or into the next instruction depending on the ``step`` parameter.
        """
        print('Running GLYPH')
        self.resetLogs()

        if step == 'into':
            assert isCall is True

        i, mode = self.getStepIndex('glyph', stepIndex=stepIndex, step=step, topLevelIndex=topLevelIndex)

        if isinstance(self.glyph, Program):
            try:
                self.mode = 'glyph'
                self.runProgram(self.glyph, stepIndex=i, step=step)
            except AssertionError as e:
                print(traceback.format_exc())
                self.valid = False
                raise e

            if i == len(self.glyph):
                self.stop()
                i = 0
                mode = 'prep'

            return i, self.lastInstructions, mode

    def runProgram(self, program, stepIndex=None, step=None):
        """
        Run a program, which can be the FPGM, PREP or any function. Step index
        should be set to None if the entire program should be run.
        """
        instruction = None

        if stepIndex is None:
            # No step index in call, run the entire program.
            stepIndex = len(program)
        else:
            assert stepIndex <= len(program)


        for index, instruction in enumerate(program):
            success = False

            '''
            # Pseudocode for jump behaviour. While instruction pointer is
            # smaller than offset, do not execute instructions.

            if self.jump is True:
                if self.instructionPointer > self.jumpOffset:
                    continue
                elif self.instructionPointer == self.jumpOffset:
                    self.jump = False
            '''

            if index < stepIndex:
                '''
                While not at the step index, execute the instructions. All
                previous instructions should be executed, except the last one.
                '''
                if program.name != 'FPGM':
                    self.loopIndices[self.gstate.functionLevel] = index

                try:
                    success = self.executeInstruction(instruction)
                except Exception as e:
                    self.stop()
                    print('Failed at index %d, instruction %s' % (index, instruction))
                    print('steps', self.stepIndices, 'loops', self.loopIndices)
                    raise e

            elif index == stepIndex:
                '''
                Try to run all instructions until step index, don't break on
                failure so we collect all errors of the previous instructions.
                '''
                break

        # Keep stack of last instructions.
        if not instruction is None:
            self.lastInstructions.append(instruction)

        '''
        Because the space points are regenerated on every iteration, we need to
        store the current points in the program, to draw their scaled position in
        the next redraw event.
        '''
        program.spacepoints = self.gstate.getZonePointer(0)[-4:]

    def executeInstruction(self, instruction):
        """The *executeInstruction* method combines the name of the
        *instruction* attribute to see if there in a method in *self* that can execute.
        If *instruction* is part of a function definition, then the instruction is
        copied into the function.

        Otherwise, if the @self.gstate@ is not in skipping mode, execute the
        instruction. For the conditional instructions IF, ElSE and EIF is a special
        treatment, because – even in skip mode – we need to keep track of their
        skipping level. If there is a set of params in the instruction, then push
        these values on the stack first in reversed order.
        """
        success = False

        if instruction.mnemonic is not None:
            # The instruction contains a single mnemoni instruction. Execute it.
            success = self.executeMnemonic(instruction)
        elif instruction.method is not None:
            # The instruction contains come kind of method, interpret it.
            # This may call several mnemonics to be executed.
            success = self.executeInstructionMethod(instruction)
        return success

    def executeMnemonic(self, instruction):
        """The @executeMnemonic@ method executes a single *mnemonic* with
        *params*. If the execution is successful, then answer @True@.  Note
        that if the *instruction* holds a method instead of a single mnemonic, then
        the *mnemonic* attribute is not directly defined by the instruction."""
        # There must be a valid mnemonic definition, try to execute it.
        name = TX.mnemonic2NamePart(instruction.mnemonic)

        if self.gstate.isSkip() and not name in (self.C.IF, self.C.ELSE, self.C.EIF):
            '''
            We are currently running in a block that is marked as skipping by if or
            else instruction. Ignore the execution of the instruction, but mark it
            as successful.
            '''
            return True

        elif not self.gstate.functionDef is None and instruction.mnemonic.id != self.C.ENDF:
            if self.verbose is True:
                self.message('Adding %s to function definition %s' % (instruction, self.gstate.functionDef))

            # Inside a function definition.
            return self.gstate.addFunctionInstruction(instruction)
        else:
            # Make dispatch method name.
            method = 'i_' + name

            # When coming this far, we can assume that the skip level is in execution
            # mode the method exists. Check with assertion for debugging.
            assert hasattr(self, method), ('[Simulator.executeInstruction] Has no method "%s"' % method)

            if 'PUSH' in name and instruction.params:
                # Mainly used when decompiling existing TTF. Don't reverse the
                # order of the pushed parameters, since they already have the
                # right order.

                for param in instruction.params:
                    self.gstate.push(TX.asInt(param), self.mode)

            elif not self.gstate.hasStack() and not instruction.params is None:
                '''
                We only use the instruction on-board parameters, if there is nothing on the stack.
                This way it is possible to overwrite the on-board parameters by pushing the
                values first. And also it makes (partial) interpretation of existing assembly
                code easier, where all values are pushed at the start of a program.
                If there are any on-board parameters in the instruction (source), push them on
                stack first.

                We assume that the number of parameters fits and has been checked before.
                Reverse the scan order, so it fits the reverse stack order.
                '''

                # Make a copy, we don't want modify the mnemonic content.
                params = instruction.params[:]
                params.reverse()

                for param in params:
                    self.gstate.push(param, self.mode)

            success = False

            try:
                # Execute the instruction and answer if it was successful.
                success = getattr(self, method)(instruction)
            except Exception as e:
                msg = traceback.format_exc()
                self.message(msg, isError=True)
                raise e

            return success

    def executeInstructionMethod(self, instruction):
        """
        The @executeInstructionMethod@ method executes the instruction macro languages,
        compiling into a set of mnemonic instructions to be executed.
        """
        return False # @@@ For now not available.

    def popParams(self, instruction):
        """
        popParams is where we collect the transformed params for answering.
        """
        params = []

        '''
        Clear the instruction on-board params, we'll get them back from the stack.
        The popped values may come from previous separate pushes or - in case
        there was no previous stack fill - from the on-board params of this
        instruction. In any case the instruction gets the parameters that it needs.
        There still may be an issue of the instruction gets multiple values from
        direct source.
        '''

        for popType in instruction.mnemonic.popTypes:
            try:
                param = self.gstate.pop()
            except Exception as e:
                msg = traceback.format_exc()
                self.message(msg, isError=True)
                raise e

            params.append(param)

        instruction.params = params

        if len(params) == 1:
            params = params[0]
        elif len(params) == 0:
            params = None

        return params

        # FIXME: converts point index to coordinates.
        '''
        if popType in (self.C.PARAMTYPE_POINT, self.C.PARAMTYPE_NPOINT): # Point or point list
            #We need the onboard param in the context of a unique ID. Make sure that it is one.
            #Because the value may come from a direct pushed integer, we need to be sure
            #that it gets translated into a unique ID in the current context of the glyph.
            useparam = self.getPointByIndex(param)
        '''

        '''
        if popType == self.C.PARAMTYPE_CVT:
            #True to get a matching CvtValue instance. If the param is
            #one of the generic CVT type, try to resolve with the current
            #graphics state, so see which CVT values is closest to an existing
            #CVT value of the same type as param.
            if param is not None and param < len(self.gstate.cvt):
                useparam = self.gstate.cvt[param]
        else:
        '''

    def getPointByIndex(self, index):
        """Answer the point that correspondent with the (original) index in the point list.
        Note that the amount of points may have been altered, so we have to check on ID-label
        instead of real index in the list."""
        return self.gstate.points[0] # index instead of 0?

    def getFpgm(self, test=None):
        if test is None:
            if not 'fpgm' in self.ttf:
                self.ttf['fpgm'] = newTable('fpgm')
                print(' * (Simulator) Missing FPGM in font %s, creating new.' % self.ttf)

            if hasattr(self.ttf['fpgm'], 'program'):
                fpgm = self.ttf['fpgm'].program.getAssembly()
                fpgm = '\n'.join(fpgm)
            else:
                fpgm = ''
        elif test == 1:
            fpgm = self.test1
        elif test == 2:
            fpgm = self.test2

        return fpgm

    def getPrep(self, test=None):
        if not 'prep' in self.ttf:
            self.ttf['prep'] = newTable('prep')
            print(' * (Simulator) Missing PREP in font %s, creating new.' % self.ttf)

        if hasattr(self.ttf['prep'], 'program'):
            prep = self.ttf['prep'].program.getAssembly()
            prep = '\n'.join(prep)
        else:
            prep = ''

        return prep

    def getGlyph(self):
        """
        Returns the glyph instructions as a formatted string.
        """
        if self.gstate.glyph is None:
            raise TrueTypeException('No glyph in graphics state for font %s' % self.ttf)

        if hasattr(self.gstate.glyph, 'program'):
            instructions =  self.gstate.glyph.program.getAssembly()
            instructions = '\n'.join(instructions)
        else:
            instructions = ''

        return instructions

    def compileFpgm(self, test=None, debug=False):
        """
        Retrieves the font program (FPGM) from the TrueType file and compiles
        it into a program object.
        """
        fpgm = self.getFpgm(test=test)
        self.fpgm = self.compileProgram('FPGM', fpgm, test=test, debug=debug)
        print(' * (Simulator) Compiled FPGM.')

    def compilePrep(self, test=None, debug=False):
        """
        Retrieves the preprogram (PREP) from the TrueType file and compiles
        it into a program object.
        """
        prep = self.getPrep(test=test)
        self.prep = self.compileProgram('PREP', prep, test=test, debug=debug)
        print(' * (Simulator) Compiled PREP.')

    def compileGlyph(self):
        """
        Retrieves the glyph instructions from the TrueType file and compiles
        it into a program object.
        """
        glyph = self.getGlyph()
        self.glyph = self.compileProgram('GLYPH', glyph)
        print(' * (Simulator) Compiled Glyph program for %s.' % self.glyphName)

    def compileProgram(self, name, opcodes, test=None, debug=False):
        """
        TODO: move to Program.
        Compile the FPGM (Font Program).
        """
        distribute = True
        stack = Stack()
        print(' -- New stack created for %s' % name)
        program = Program(name)
        instruction = None
        freeTokenParts = []

        if 'CALL[' in opcodes.upper():
            distribute = False

        tokens = self.SRC2TOKEN.findall(opcodes)

        for token in tokens:
            opcode, comment, parameter, freeTokenPart = token

            if opcode and not opcode == '':
                instruction = self.getInstruction(opcode, instruction, stack, program, distribute, debug)
            elif comment and not comment == '':
                instruction = self.stripComment(instruction, comment, program)
            elif parameter and not parameter == '':
                self.setParameter(instruction, parameter, stack)
            elif freeTokenPart:
                freeTokenParts.append(freeTokenPart)
                # TODO: Needs to be finished.
                # Conversion using FREEWORDINDEX, etc.

        self.finalizeProgram(instruction, stack, distribute)
        return program

    def getInstruction(self, opcode, instruction, stack, program, distribute, debug):
        """
        TODO: move to Program.
        Takes care of Instruction bookkeeping.
        """

        if instruction is not None and instruction.mnemonic is not None:
            if instruction.mnemonic.isPush() and not distribute:
                '''
                We are not distributing, so let the push instruction keep its own
                parameters.
                '''
                instruction.params = stack.popAll()

                if debug:
                    print('stack: popAll()')
            elif distribute:
                '''
                Add the right amount of parameters from the stack to the current mnemonic
                before we get on to the new one.
                '''
                instruction.params = stack.slicePop(len(instruction.mnemonic.popTypes))

                if debug:
                    print('stack: pop %d' % len(instruction.mnemonic.popTypes))

        # Always a mnemonic, check if we can find it in the MnemonicSet table.
        instruction = Instruction()
        instruction.mnemonic = MnemonicSet.getMnemonic(opcode)

        if debug:
            print('Created new Instruction with opcode %s' % opcode)

        '''
        Push values on the stack if this is a push token, and don't add it to
        the Wing. If we are not distributing push values, then always add the instruction.
        Otherwise do add, since it could be a comment.

        mnemonic is None:       Probably just comments, always output.
        not mnemonic.isPush():  Always output.
        mnemonic.isPush():      Only output if not distributing.
        '''
        if instruction.mnemonic is None or \
                not instruction.mnemonic.isPush() or \
                (instruction.mnemonic.isPush() and not distribute):
            program.append(instruction)

        return instruction

    def setParameter(self, instruction, parameter, stack):
        """
        TODO: move to Program.
        """
        if instruction is None:
            # Error, not supposed to have parameters before a mnemonic.
            error = 'No parameters allowed prior to the first mnemonic, parameter is %s' % parameter
            self.message(error)

        value = TX.asIntOrNone(parameter)

        if value is None:
            # Error, cannot convert the parameter to an integer, back out.
            instruction.error = 'Error in parameters "%s"' % parameter
        else:
            # If distributing the push values, we need these parameters on the stack.
            stack.push(value)

    def finalizeProgram(self, instruction, stack, distribute):
        """
        TODO: move to Program.
        Final steps to see if there are still parameters left on the stack.
        """

        # Only if we are distributing the parameters.
        if instruction is not None and instruction.mnemonic and \
                not instruction.mnemonic.isPush() and \
                distribute:

            # Add the right amount of parameters from the stack to the current
            # mnemonic before we get the new one.
            popTypes = instruction.mnemonic.popTypes

            if popTypes is not None:
                needParams = len(popTypes)

                if len(stack) != needParams:
                    instruction.error = 'Error in amount of pushed parameters'

                if len(stack) >= needParams:
                    instruction.params = stack.slicePop(needParams)

    def stripComment(self, instruction, comment, program):
        """
        TODO: move to Program.
        Strip the comment code.
        """
        comment = self.STRIPCOMMENT.findall(comment)[0].strip()

        if instruction is None:
            # No instruction yet, create one to hold the comment.
            instruction = Instruction()
            program.append(instruction)

        instruction.comment = comment
        return instruction

    # Gstate.

    def setProjectionVector(self, p):
        assert isinstance(p, Vector)

        if self.gstate is not None:
            self.gstate.projectionVector = p

    def getProjectionVector(self):
        if self.gstate is not None:
            return self.gstate.projectionVector

        return None # No running state

    def setFreedomVector(self, f):
        assert isinstance(f, Vector)

        if self.gstate is not None:
            self.gstate.freedomVector = f

    def getFreedomVector(self):
        if self.gstate is not None:
            return self.gstate.freedomVector

        return None # No running state

if __name__ == "__main__":
    """
    Usage:

    python simulator.py or ./simulator.py

    Should yield a bunch of test results for debugging purposes.
    """

    #s = Simulator(None)

    # Test 1.

    '''
    print('\n-Compiling test 1-\n')
    s.compileFpgm(test=1)
    print('\n-Program Dump-\n')
    print(s.fpgm.dump())
    '''

    # Test 2.

    '''
    print('\n-Compiling test 2-\n')
    s.compileFpgm(test=2)
    print('\n-Program Dump-\n')
    print(s.fpgm.dump())
    '''

    # Test on a font so we have a valid stack to run on.

    import tnTestFonts
    from fontTools.ttLib import TTFont
    fontName = 'CusterRE-RegularS2.ttf'
    fontPath = tnTestFonts.getFontPath(fontName)
    ttf = TTFont(fontPath)

    verbose = True
    s = Simulator(ttf, verbose=verbose)
    print('\n-Compiling %s-\n' % fontName)
    fpgm = s.getFpgm()
    s.compileFpgm()

    s.setGlyph('H', 12)
    s.compileGlyph()

    '''
    print('\n-Program Dump-\n')
    print(s.fpgm.dump(maxLines=30))
    s.runFpgm()
    print(s.gstate)
    '''

    '''
    for key, value in s.gstate.functions.items():
        print('Key:', key, value)
    '''

    print('\n-Compiling %s-\n' % fontName)
    s.compilePrep()
    print('\n-Program Dump-\n')
    print(s.prep.dump(maxLines=30))

    #s.runPrep(2)
