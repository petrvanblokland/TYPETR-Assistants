# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    factory.py
#

from tnbits.proofing.allmetrics import AllMetrics
from tnbits.proofing.kerningmap import KerningMap
from tnbits.proofing.overlay import Overlay
from tnbits.proofing.pagewide import PageWide
from tnbits.proofing.stylesperline import StylesPerLine
from tnbits.proofing.textprogression import TextProgression

class Factory(object):
    """Factory to create template objects."""

    def get(self, templateIdentifier, **kwargs):
        """Returns template object for proofs based on identifier."""
        if templateIdentifier == "PageWide":
            return PageWide(**kwargs)
        elif templateIdentifier == "TextProgression":
            return TextProgression(**kwargs)
        elif templateIdentifier == "Overlay":
            return Overlay(**kwargs)
        elif templateIdentifier == "AllMetrics":
            return AllMetrics(**kwargs)
        elif templateIdentifier == "KerningMap":
            return KerningMap(**kwargs)
        elif templateIdentifier == "StylesPerLine":
            return StylesPerLine(**kwargs)
