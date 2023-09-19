# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     instructionbase.py
#
from tnbits.constants import Constants
from tnbits.toolbox.transformer import TX

class InstructionBase(dict):
    """
    The @InstructionBase@ is the base class for all @Instructions@.
    """
    C = Constants

    LABEL_UNTITLED = 'Untitled'

    @classmethod
    def fromJson(cls, json):
        if json is None:
            instructionbase = cls()
        else:
            instructionbase = cls(TX.json2Dict(json))
        return instructionbase

    def asJson(self):
        return TX.dict2Json(self)

    def asDict(self):
        return dict(self)

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_ID

    def _get_id(self):
        id = self.get(self.C.WINGFIELD_ID)
        if id is None:
            id = TX.uniqueID()
            self[self.C.WINGFIELD_ID] = id # It is prevented to use self.id = id
        return id

    def _set_id(self, id):
        raise ValueError('[%s.id] Cannot be changed as attribute.' % self.__class__.__name__)

    id = property(_get_id, _set_id, "InstructionBase.id")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_SELECTED

    def deselect(self):
        # Initialize the selection attribute for InstructionBase inheritance that need it.
        self._selected = None

    def getFirstChild(self):
        # To be redefined by the inheriting Wing class that has children.
        return None

    def _get_selected(self):
        # If None is selected, then answer the first of the ordered list.
        t = self._selected
        if self._selected is None:
            return self.getFirstChild()

        return self._selected

    def _set_selected(self, instructionbase):
        assert instructionbase is None or isinstance(instructionbase, InstructionBase)
        self._selected = instructionbase

    selected = property(_get_selected, _set_selected, "InstructionBase.selected")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_NAME

    def _get_name(self):
        return self.get(self.C.WINGFIELD_NAME, self.LABEL_UNTITLED)

    def _set_name(self, name):
        assert isinstance(name, str)
        self[self.C.WINGFIELD_NAME] = name

    name = property(_get_name, _set_name, "InstructionBase.name")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_AXIS

    USE_FIELDAXIS = False

    def _get_axis(self):
        name = self.name.lower()
        # If there is an axis marker in the name, then update the axis cell
        if self.C.TITLE_AXISY in name:
            axis = self.C.Y
        elif self.C.TITLE_AXISX in name:
            axis = self.C.X
        elif self.C.TITLE_AXISD in name:
            axis = self.C.D
        elif self.USE_FIELDAXIS and self.get(self.C.WINGFIELD_AXIS) is not None:
            axis = self.get(self.C.WINGFIELD_AXIS)
        else:
            axis = ''

        return axis

    def _set_axis(self, axis):
        if not isinstance(axis, str):
            axis = repr(axis)

        if self.C.X in axis:
            axis = self.C.X
        elif self.C.Y in axis:
            axis = self.C.Y
        elif self.C.D in axis:
            axis = self.C.D
        else:
            axis = ''

        self[self.C.WINGFIELD_AXIS] = axis

    axis = property(_get_axis, _set_axis, "InstructionBase.axis")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_COMMENT

    def _get_comment(self):
        return self.get(self.C.WINGFIELD_COMMENT)

    def _set_comment(self, comment):
        # Takes glyph instance or name
        assert comment is None or isinstance(comment, str)

        if comment is not None:
            comment = comment.strip()
        self[self.C.WINGFIELD_COMMENT] = comment

    comment = property(_get_comment, _set_comment, "InstructionBase.comment")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_ERROR

    def _get_error(self):
        return self.get(self.C.WINGFIELD_ERROR)

    def _set_error(self, error):
        # Takes glyph instance or name
        assert error is None or isinstance(error, str)

        if error is not None:
            error = error.strip()
        self[self.C.WINGFIELD_ERROR] = error

    error = property(_get_error, _set_error, "InstructionBase.error")

    # ---------------------------------------------------------------------------------------------------------
    #    WINGFIELD_SRC

    def _get_src(self):
        return self.get(self.C.WINGFIELD_SRC)

    def _set_src(self, src):
        # Takes string or list/tuple
        if isinstance(src, (tuple, list)):
            src = '\n'.join(src)

        assert src is None or isinstance(src, str)
        self[self.C.WINGFIELD_SRC] = src

    src = property(_get_src, _set_src, "InstructionBase.src")
