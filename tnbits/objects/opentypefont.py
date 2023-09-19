# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     opentypefont.py
#
from truetypefont import TrueTypeFont
from tnbits.compilers.subsetting.cffcompiler import CFFCompiler

class OpenTypeFont(TrueTypeFont):
    """Specifically define the behavior of the OpenTypeFont as different from
    the TrueTypeFont."""

    CFF = 'CFF '

    # self.CFF table

    def _get_cff(self):
        if self._cff is None and self.CFF in self._ttfont:
            self._cff = CFFCompiler().decompile(self._ttfont[self.CFF])
        return self._cff

    def _set_cff(self, cff):
        # Needs to be set to self._ttfont[self.CFF] still.
        self._cff = cff

    cff = property(_get_cff, _set_cff)

