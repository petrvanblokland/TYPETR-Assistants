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
#    view.py

class View(object):
    """Shared functions for views controlled by a BaseController object."""

    def getView(self):
        return self.view

    def getDesignSpace(self):
        return self.getController().getDesignSpace()

    def setDesignSpace(self, name):
        return self.getController().setDesignSpace(name)

    def getFamily(self):
        return self.getController().getFamily()

    def getStyle(self, styleKey):
        return self.getController().getStyle(styleKey)

    def getController(self):
        raise NotImplementedError
