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
#    exception.py
#

class QAException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        msg = '!!! ' + self.value
        return msg
