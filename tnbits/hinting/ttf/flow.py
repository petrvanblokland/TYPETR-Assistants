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
#    flow.py
#

class Flow(object):
    """
    Hinter flow functionality. Auxiliary functions to keep track of stepping and loops.
    """

    # Step indices.

    def getStepIndex(self, mode, stepIndex=None, step=None, topLevelIndex=None):
        """
        Keeps track of step indices. Resets if a `stepIndex` is passed, else
        sets it based on the `step` value.
        """

        if not stepIndex is None:
            # Hard index, reset previous step indices.
            self.resetStepIndices(mode, stepIndex)
            otherMode = self.getOtherStepMode(mode)
            self.resetStepIndices(otherMode, None)
            i = stepIndex
        elif not topLevelIndex is None:
            i, mode = self.setTopLevelIndex(mode, topLevelIndex)
        elif stepIndex is None and not step is None:
            # Calling step (into, out or over), calculate the step index from
            # the previous one.
            i, mode = self.setStepIndices(mode, step)
        else:
            # Run all programs until the end, runProgram() will take care of
            # stepIndex.
            i = None
            self.resetStepIndices(mode, i)

        return i, mode

    def getStepMode(self):
        """
        Returns either 'prep' or 'glyph'.
        """
        if not self.stepIndices['prep'][0]['index'] is None:
            return 'prep'
        else:
            return 'glyph'

    def setStepIndices(self, mode, step):
        """
        Sets step indices depending on step type.
        """
        assert not step is None
        level = max(self.stepIndices[mode].keys()) # Gets top level.

        if step == 'into':
            # Increase current level by one.
            self.stepIndices[mode][level]['index'] += 1
            # Add one level so stepping will continue inside
            # function.
            level += 1
            self.stepIndices[mode][level] = {'index': 0}
        elif step == 'out':
            # Remove top level.
            self.deleteTopStepLevel(mode)
        elif step == 'over':
            # Goes to the next instruction in the current program or jumps from PREP
            # to glyph program if the PREP's end has been reached.

            if self.stepIndices['prep'][0]['index'] == len(self.prep) - 1:
                # Switch from PREP to glyph program.
                self.stepIndices['prep'][0]['index'] = None
                self.stepIndices['glyph'][0]['index'] = 0
                mode = 'glyph'
            elif self.stepIndices['glyph'][0]['index'] > len(self.glyph):
                # End of instructions, finish.
                # FIXME: called twice?
                #self.stop()
                #mode = 'prep'
                pass
            else:
                # Still inside same program, Step one further in current level.
                self.stepIndices[mode][level]['index'] += 1

        return self.stepIndices[mode][0]['index'], mode

    def resetStepIndices(self, mode, stepIndex):
        """
        Empties out levels for indices in mode ``mode`` to ``stepIndex`` at lowest level.
        """
        self.stepIndices[mode] = {}
        self.stepIndices[mode][0] = {'index': stepIndex, 'program': mode}

    def getOtherStepMode(self, mode):
        """
        Flips between 'prep' and 'glyph'.
        """
        if mode == 'prep':
            return 'glyph'
        elif mode == 'glyph':
            return 'prep'

    # Function levels.

    def setTopLevelIndex(self, mode, index):
        level = self.getTopStepLevel(mode)
        self.stepIndices[mode][level]['index'] = index
        return self.stepIndices[mode][0]['index'], mode

    def getLevelStepIndex(self, mode, level):
        """
        Returns step index for given level.
        """
        if level in self.stepIndices[mode].keys():
            return self.stepIndices[mode][level]['index']

    def getTopStepIndex(self, mode):
        """
        Returns function ``stepIndex`` and ``functionId`` for top function
        call if there is one, if running in preprogram return None.
        """
        level = self.getTopStepLevel(mode)
        return self.stepIndices[mode][level]['index']

    def deleteTopStepLevel(self, mode):
        level = self.getTopStepLevel(mode)
        del self.stepIndices[mode][level]

    def getTopStepLevel(self, mode):
        """
        Returns the top step level, which is the largest integer key for the
        current mode.
        """
        return max(self.stepIndices[mode].keys())

    # Functions.

    def isInsideCall(self, mode):
        level = self.getTopStepLevel(mode)
        return level > 0

    def getFunctionStepIndex(self, mode, level, functionId):
        """
        Returns step index for a known function.
        """
        if level in self.stepIndices[mode].keys():
            if 'program' in self.stepIndices[mode][level]:
                if self.stepIndices[mode][level]['program'] == 'function %d' % functionId:
                    return self.stepIndices[mode][level]['index']

    def removeFunctionStepIndex(self, mode, level):
        """
        Removes a function step index when all instructions have been
        executed.
        """
        assert level == max(self.stepIndices[mode].keys()) # Assert top level.

        if level in self.stepIndices[mode]:
            del self.stepIndices[mode][level]
            return True
        return False

    def setFunctionId(self, mode, level, functionId):
        """
        Sets function ID after a 'step into', level and index have already been added
        to stop inside the call, the function ID is popped after the fact however, so we
        should assign it once it is known.
        """

        # Check if this is the last instruction of the calling program.
        maxIndexPreviousLevel = self.stepIndices[mode][level - 1]['index'] - 1
        indexPreviousLevel = self.loopIndices[level - 1]

        if maxIndexPreviousLevel == indexPreviousLevel:
            self.stepIndices[mode][level]['program'] = 'function %d' % functionId

    def getFunctionId(self, mode):
        """
        Returns the function ID, stored in the stepIndices dictionary under the
        'program' key.
        """
        level = max(self.stepIndices[mode])

        if level > 0:
            if 'program' in self.stepIndices[mode][level]:
                functionName = self.stepIndices[mode][level]['program']
                return int(functionName.split(' ')[-1])

    def getFunctionIds(self):
        """
        Returns all function keys.
        """
        return self.gstate.functions.keys()

    def hasFunctions(self):
        """
        Checks if the graphics state contains functions.
        """
        if self.gstate is None:
            return False

        if len(self.gstate.functions) > 0:
            return True

        return False
