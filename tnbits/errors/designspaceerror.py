# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     designspaceerror.py

class DesignSpaceError(Exception):
    """Custom error to be raised from design space."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '%s' % self.msg
