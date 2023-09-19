# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     instruction.py

from tnbits.toolbox.transformer import TX
from tnbits.hinting.ttf.mnemonicset import MnemonicSet
from tnbits.hinting.ttf.mnemonic import Mnemonic
from tnbits.hinting.ttf.instructionbase import InstructionBase

class Instruction(InstructionBase):
    """
    The *Instruction* class is a *dict* data structure that holds a single hint
    instruction, a macro reference or any other future coding that can expand
    into hinting.

    *Instruction* inherits from *InstructionBase* which is directly inheriting from
    *dict*. This assures the automatic saving when stored in
    @glyph.lib@.
    """
    def __repr__(self):
        return '[Instruction %s]' % (self.asVtt())

    def isValid(self):
        """
        The @isValue@ method answers if this is a valid executable
        instruction. If there is just comment that also counts as valid.
        """
        return bool(self.mnemonic or self.method or self.comment)

    def getInfo(self):
        """
        Show the help info of the current instruction.
        """

        if self.mnemonic is not None:
            s = str(self.mnemonic)
            l = len(self.params)

            if l > 0:
                if l == 1:
                    s += 'Parameter: ['
                else:
                    s += 'Parameters: ['

                s += str(self.params[0])
                if l > 1:
                    for p in self.params[1:]:
                        s += ' %s' % str(p)

                s += ']'

        elif self.method is not None:
            s = 'Method: %s.' % self.method

        return s

    def asVtt(self):
        # As mnemonic.vtt with comments, this is default behavior
        return self.asSource('vtt')

    def asFree(self):
        return self.asSource('freeName')

    def asAssembly(self, ignoreComment=False):
        # As TTX, but the without comments
        return self.asSource('assembly', ignoreComment)

    def asCode(self): # As hex code
        return self.asSource('code')

    def asSource(self, format=None, ignoreComment=False):
        """
        Builds the source, depending on the type of format. There are several valid options:

        code        Show as mnemonic.code
        assembly    Show as mnemonic.base (equals TTX code, without the parameters, need to be pushed separate)
        freeName    Show as free format programming language
        vtt         Show as mnemonic.vtt (default)
        """
        pushed = ''
        s = []
        mnemonic = self.mnemonic # Save multiple retrievals

        if mnemonic:
            if format == 'assembly': # Same as PUSH + BASE for TTX
                s.append(mnemonic.base)

                if self.params:
                    if mnemonic.isPush():
                        '''
                        Use this mnemonic, otherwise we cannot find out if the
                        original was a word or byte push. Especially the 0 pushes
                        cannot be decided on, when the original code needs to be
                        restored.
                        '''
                        for param in self.params:
                            s.append('%s' % param) # List of integers, cannot be joined.
                    elif self.params:
                        '''
                        Assembly must have all parameters as pushes, but only push if this
                        mnemonic itself isn't a push.

                        Split them into sequences of PUSHB, PUSHW, NPUSHB and NPUSHW

                        @@@ Note that it is tricky to reconstruct if this should be
                        byte or word pushes.
                        '''
                        pushed = MnemonicSet.push(self.params)
            elif format == 'code':
                s.append(mnemonic.code)
            elif format == 'freeName':
                s.append(mnemonic.freeName)
            elif format == 'vtt':
                s.append(mnemonic.vtt)
            else:
                raise ValueError('Wrong Instruction format request "%s". Should never happen.' % format)

        if mnemonic and format != 'assembly' and self.params:
            # Assembly cannot have parameters in other mnemonics than pushes
            for param in self.params:
                s.append('%s' % param) # List of integers, cannot be joined.

        if self.comment and not ignoreComment:
            # Always output the comment, even if the mnemonic is not filled
            # Where ever the comment originally was positioned in the line of code,
            # it always moves to the end on decompile.
            s.append('/* %s */' % self.comment)

        # Append any pushed output to the start of the string, in case of assembly format.
        return pushed + ' '.join(s)

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_CODE

    def _get_code(self):
        # instruction.code is always a string, empty if the attribute does not exist
        return self.get(self.C.WINGFIELD_CODE, '')

    def _set_code(self, code):
        code = code or ''
        assert isinstance(code, str)
        self[self.C.WINGFIELD_CODE] = code

    code = property(_get_code, _set_code, "Instruction.code")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_PARENT

    def _get_parent(self):
        return self.get(self.C.WINGFIELD_PARENT) or None

    def _set_parent(self, parent):
        if parent is not None and not isinstance(parent, str):
            parent = parent.uniqueID
        assert not parent or TX.isUniqueID(parent), 'Illegal value for Instruction.parent: "%s"' % parent
        self[self.C.WINGFIELD_PARENT] = parent or ''

    parent = property(_get_parent, _set_parent, "Instruction parent")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_POINT

    def _get_point(self):
        return self.get(self.C.WINGFIELD_POINT) or None

    def _set_point(self, point):
        if point is not None and not isinstance(point, str):
            point = point.uniqueID
        assert not point or TX.isUniqueID(point), 'Illegal value for Instruction.point: "%s"' % point
        self[self.C.WINGFIELD_POINT] = point or ''

    point = property(_get_point, _set_point, "Instruction point")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_COLOR
    #    Should be done automatically, depending on glyph point and axis.

    def _get_color(self):
        return self.get(self.C.WINGFIELD_COLOR)

    def _set_color(self, color):
        assert  'Illegal value for Instruction.color: "%s"' % color
        self[self.C.WINGFIELD_COLOR] = color

    color = property(_get_color, _set_color, "Instruction color")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_LINENUMBER

    def _get_linenumber(self):
        return self.get(self.C.WINGFIELD_LINENUMBER)

    def _set_linenumber(self, linenumber):
        self[self.C.WINGFIELD_LINENUMBER] = linenumber

    linenumber = property(_get_linenumber, _set_linenumber, "Instruction linenumber")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_CVT

    def _get_cvt(self):
        return self.get(self.C.WINGFIELD_CVT)

    def _set_cvt(self, cvt):
        assert cvt is None or isinstance(cvt, (int, str))
        self[self.C.WINGFIELD_CVT] = cvt

    cvt = property(_get_cvt, _set_cvt, "Instruction cvt")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_UNIQUEID

    def _get_uniqueID(self):
        if self.parent and self.point:
            return self.parent + self.point
        return None

    def _set_uniqueID(self, uniqueID):
        raise AttributeError('[Winglabel.set] The Instruction parent+point cannot be set')

    uniqueID = property(_get_uniqueID, _set_uniqueID, "Instruction uniqueID")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_TYPE

    def _get_type(self):
        return self.get(self.C.WINGFIELD_TYPE)

    def _set_type(self, type):
        assert type is None or type in self.C.WINGTYPES
        self[self.C.WINGFIELD_TYPE] = type

    type = property(_get_type, _set_type, "Instruction type (of CVT type)")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_WINGLABEL

    def _get_winglabel(self):
        return self.get(self.C.WINGFIELD_WINGLABEL)

    def _set_winglabel(self, winglabel):
        assert winglabel is None or winglabel in (str, int)
        self[self.C.WINGFIELD_WINGLABEL] = winglabel

    winglabel = property(_get_winglabel, _set_winglabel, "Instruction reference to Instruction")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_MNEMONIC

    def _get_mnemonic(self):
        # Store just the name, since the caller knows the amount of params
        return MnemonicSet.getMnemonic(self.get(self.C.WINGFIELD_MNEMONIC), len(self.params))

    def _set_mnemonic(self, mnemonic):
        assert mnemonic is None or isinstance(mnemonic, (Mnemonic, str))
        if isinstance(mnemonic, Mnemonic):
            mnemonic = mnemonic.vtt
        self[self.C.WINGFIELD_MNEMONIC] = mnemonic

    mnemonic = property(_get_mnemonic, _set_mnemonic, "Instruction mnemonic ID")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_METHOD

    def _get_method(self):
        return self.get(self.C.WINGFIELD_METHOD) or None

    def _set_method(self, method):
        self[self.C.WINGFIELD_METHOD] = method

    method = property(_get_method, _set_method, "Instruction method")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_POPTYPES

    def _get_poptypes(self):
        mnemonic = self.mnemonic
        if mnemonic is not None:
            return mnemonic.poptypes
        return None

    poptypes = property(_get_poptypes, "Instruction.mnemonic.poptypes")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_PUSHTYPES

    def _get_pushtypes(self):
        mnemonic = self.mnemonic
        if mnemonic is not None:
            return mnemonic.pushtypes
        return None

    pushtypes = property(_get_pushtypes, "Instruction.mnemonic.pushtypes")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_PARAMS

    def _get_params(self):
        params = self.get(self.C.WINGFIELD_PARAMS)
        if params is None:
            self.params = params = []
        return params

    def _set_params(self, params):
        assert params is None or isinstance(params, (list, tuple))
        self[self.C.WINGFIELD_PARAMS] = params

    params = property(_get_params, _set_params, "Instruction params")

    # ---------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    from tnbits.constants import Constants
    w = Instruction()
    w.params = [123]
    w.color = Constants.WINGCOLOR_BLACK
    print(w)
