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
#    featureview.py
#
from tnbits.base.console import Console

class FeatureView(object):
    """
    >>> from fontTools.ttLib import TTFont
    >>> f = TTFont(srcPath)
    >>> condSubst = [
    ...     # A list of (Region, Substitution) tuples.
    ...     ([{"wght": (0.5, 1.0)}], {"dollar": "dollar.rvrn"}),
    ...     ([{"wdth": (0.5, 1.0)}], {"cent": "cent.rvrn"}),
    ... ]
    >>> addConditionalSubstitutions(f, condSubst)
    >>> f.save(dstPath)
    >>> f = TTFont(dstPath)
    >>> f.saveXML(dstPath + ".ttx", tables=["GSUB"])
    """


    def __init__(self, controller, pos=(0, 0, -0, -0)):
        self.controller = controller
        self.editor = Console(self, pos=pos)
        #self.editor.message(str(example_gsub))
        self.editor.setLines()
        self.editor.show(False)
        #self.tool.set('editor', self.editor.getView())
