# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     floqerror.py

class FloqError(Exception):
    """Custom error to be raised from inside floq model."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
