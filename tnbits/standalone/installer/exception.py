# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Type Network installer appication.
#    Copyright (c) 2017+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    exception.py

class InstallerException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        msg = '!!! ' + self.value
        return msg
