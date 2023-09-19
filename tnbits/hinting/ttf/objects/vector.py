# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    vector.py
#
from tnbits.constants import Constants as C

class Vector:
    """
    (x, y) vector.
    """

    def __init__(self, x, y=None):
        """
        Initializes with another Vector, list or tuple, or x, y coordinates
        (two parameters).
        """
        if y is None:
            if isinstance(x, Vector):
                x, y = x.x, x.y
            elif isinstance(x, (list, tuple)):
                x, y = x

        self.x = x
        self.y = y

    def __repr__(self):
            return 'Vector(%s,%s)' % (self.x, self.y)

    def isX(self):
        """
        Answers if this vector is in X direction.
        """
        return self.x == C.AXISUNIT and self.y == 0

    def isY(self):
        """
        Answers if this vector is in Y direction.
        """
        return self.x == 0 and self.y == C.AXISUNIT
