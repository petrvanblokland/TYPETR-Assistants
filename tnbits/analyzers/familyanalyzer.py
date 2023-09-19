# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     familyanalyzer.py
#

from tnbits.constants import Constants
from tnbits.analyzers.styleanalyzer import StyleAnalyzer

class FamilyAnalyzer(object):
    """The FamilyAnalyzer class is a dictionary of StyleAnalyzer instances
    related to StyleAnalyzer.styleId."""
    C = Constants

    STYLEANALYZER_CLASS = StyleAnalyzer
    #
    # TODO: To be developed.
    # Which functions should go here, that are not part of the family,
    # extending the StyleAnalyzer functions on family level?

