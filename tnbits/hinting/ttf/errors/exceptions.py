# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------------------------
#    xierpa server
#    (c) 2007-2012 buro@petr.com, www.petr.com
#
#    X I E R P A
#
#    No distribution without permission.
#
# ----------------------------------------------------------------------------------------------------------------------
#
#    exceptions.py

class HintingException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        msg = '!!! ' + self.value
        return msg

class HintingPopException(HintingException):
    pass

class HintingParamsException(HintingException):
    pass

class HintingBreakPointException(HintingException):
    pass

class HintingLevelException(HintingException):
    pass

class TrueTypeException(HintingException):
    pass
