# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     flighterror.py

class FlightError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
