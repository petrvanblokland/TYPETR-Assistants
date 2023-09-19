# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   TnBitsException.py
#

class TnBitsException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

